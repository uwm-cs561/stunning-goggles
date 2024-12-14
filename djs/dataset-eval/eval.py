import os

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from unsloth import FastLanguageModel
from transformers import TextStreamer
import evaluate
from load_zip import get_ans, get_ctx, get_test
import json
from unsloth import torch
from datetime import datetime, timezone
from itertools import islice

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
        inputs = None
        outputs = None
        try:
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

            # why +13? Not sure, but somehow the character counts get off by 13
            yield decoded_outputs[len(input_chars) + 13 :]
        except Exception as e:
            yield e
        finally:
            # free up GPU memory
            del inputs
            del outputs
            torch.cuda.empty_cache()


def main(test_begin_index, test_end_index):
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")

    run_identifier = f"{test_begin_index}-{test_end_index}-{timestamp}"

    test_file_infos = get_test()
    slice_ = slice(test_begin_index, test_end_index)
    file_info_iterator = islice(test_file_infos, test_begin_index, test_end_index)

    bleu = evaluate.load("bleu")

    outputs = []
    references = []
    for output in inference(file_infos=test_file_infos[slice_], stream_outputs=True):
        reference = get_ans(next(file_info_iterator))
        references.append(reference)

        if isinstance(output, Exception):
            # todo
            outputs.append("")
            result = {"error": str(output)}
        else:
            outputs.append(output)
            result = bleu.compute(predictions=[output], references=[reference])

        with open(
            get_relative_path(f"results/progress-{run_identifier}.jsonl"), "a"
        ) as f:
            json.dump(result, f)
            f.write("\n")

    results = bleu.compute(predictions=outputs, references=references)
    print(results)

    with open(
        get_relative_path(
            f"results/{test_begin_index}-{test_end_index}-{timestamp}.json"
        ),
        "w",
    ) as f:
        json.dump(
            results,
            f,
            indent=2,
        )


if __name__ == "__main__":
    main(8, 16)
