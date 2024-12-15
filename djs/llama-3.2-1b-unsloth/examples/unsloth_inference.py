from unsloth import FastLanguageModel
from transformers import TextStreamer
import os

SAVED_WEIGHTS_DIR = "saved_weights"
max_seq_length = 2048  # Supports RoPE Scaling interally, so choose any!

# 4bit pre quantized models we support for 4x faster downloading + no OOMs.
fourbit_models = [
    "unsloth/Llama-3.2-1B-bnb-4bit",  # NEW! Llama 3.2 models
    "unsloth/Llama-3.2-1B-Instruct-bnb-4bit",
    "unsloth/Llama-3.2-3B-bnb-4bit",
    "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
]  # More models at https://huggingface.co/unsloth


alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


def inference(*, local_model_name=None):
    model_name = (
        os.path.join(SAVED_WEIGHTS_DIR, local_model_name)
        if local_model_name is not None
        else "unsloth/Llama-3.2-3B-Instruct-bnb-4bit"
    )

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=model_name,
        max_seq_length=max_seq_length,
        dtype=None,
        load_in_4bit=True,
    )

    FastLanguageModel.for_inference(model)  # Enable native 2x faster inference

    inputs = tokenizer(
        [
            alpaca_prompt.format(
                "Identify the error in the following log diff.",  # instruction
                "TypeError: expected type int",  # input
                "",  # output - leave this blank for generation!
            )
        ],
        return_tensors="pt",
    ).to("cuda")

    n_input_tokens = len(inputs[0])

    print()

    text_streamer = TextStreamer(tokenizer)

    outputs = model.generate(
        **inputs,
        streamer=text_streamer,
        max_new_tokens=256,
        # use_cache=True
    )

    (decoded_outputs,) = tokenizer.batch_decode(outputs)

    print()

    print(f"Tokens output: {len(outputs[0]) - n_input_tokens}")
    print(f"Complete? {outputs[0][-1] == tokenizer.eos_token_id}")

    # print(decoded_outputs)


if __name__ == "__main__":
    inference()
    # inference()
