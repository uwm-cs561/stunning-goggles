from unsloth import FastLanguageModel
from transformers import TextStreamer
import evaluate
import os
from load_zip import get_ans, get_ctx, get_test
import json
from unsloth import torch

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
        input_chars = prompt_template.format(
            ctx,  # input
            "",  # output - leave this blank unless we want to start it off with something
        )

        inputs = tokenizer(
            [input_chars],
            return_tensors="pt",
        ).to("cuda")

        if stream_outputs and len(file_infos) < 5:
            text_streamer = TextStreamer(tokenizer)
        else:
            text_streamer = None

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                streamer=text_streamer,
                max_new_tokens=1024,
                # use_cache=True
            )

        (decoded_outputs,) = tokenizer.batch_decode(outputs)

        print(torch.cuda.memory_summary(abbreviated=True))

        # free up GPU memory
        del inputs
        del outputs
        torch.cuda.empty_cache()

        print(torch.cuda.memory_summary(abbreviated=True))

        # why +13? Not sure, but somehow the character counts get off by 13
        yield decoded_outputs[len(input_chars) + 13 :]


def main():
    test_file_infos = get_test()
    test_begin_index, test_end_index = 4, 12
    slice_ = slice(test_begin_index, test_end_index)
    outputs = list(inference(file_infos=test_file_infos[slice_], stream_outputs=True))
    references = [get_ans(file_info) for file_info in test_file_infos[slice_]]

    bleu = evaluate.load("bleu")
    results = bleu.compute(predictions=outputs, references=references)
    print(results)
    with open(
        get_relative_path(f"results-{test_begin_index}-{test_end_index}.json"), "w"
    ) as f:
        json.dump(
            results,
            f,
            indent=2,
        )


if __name__ == "__main__":
    main()
    # for file_info in get_test()[2:4]:
    #     print("<>BEG<>")
    #     print(get_ctx(file_info))
    #     print("<>MID<>")
    #     print(get_ans(file_info))
    #     print("<>END<>")
    #     print()
