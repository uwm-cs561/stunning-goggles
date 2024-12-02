from unsloth import FastLanguageModel
from transformers import TextStreamer
import os
from traintest import get_ans, get_ctx, get_test

SAVED_WEIGHTS_DIR = "saved_weights"
max_seq_length = 2048  # Supports RoPE Scaling interally, so choose any!


prompt_template = """You are an expert DevOps engineer. You are examining some logs. Your first task is to find which lines, if any, contain errors. Examine the following logs.

### Logs:
{}

### Instructions:
Find the lines that contain the errors and repeat them verbatim, and then stop. Do not include the irrelevant lines that do not contain any errors.

### Response:
{}"""


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


def inference(*, file_infos, local_model_name=None, stream_outputs=False):
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

    for file_info in file_infos:
        ctx = get_ctx(file_info)
        inputs = tokenizer(
            [
                prompt_template.format(
                    ctx,  # input
                    "",  # output - leave this blank unless we want to start it off with something
                )
            ],
            return_tensors="pt",
        ).to("cuda")

        n_input_tokens = len(inputs[0])

        if stream_outputs and len(file_infos) < 10:
            text_streamer = TextStreamer(tokenizer)
        else:
            text_streamer = None

        outputs = model.generate(
            **inputs,
            streamer=text_streamer,
            max_new_tokens=1024,
            # use_cache=True
        )

        (decoded_outputs,) = tokenizer.batch_decode(outputs)

        yield decoded_outputs


if __name__ == "__main__":
    test_file_infos = get_test()
    for output in inference(file_infos=test_file_infos[:2]):
        print(output)
