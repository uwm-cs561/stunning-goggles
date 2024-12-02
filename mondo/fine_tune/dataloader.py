import os
from unsloth import (
    apply_chat_template,
    to_sharegpt,
    standardize_sharegpt,
    get_chat_template,
)
from datasets import load_dataset, Dataset
import json


CHAT_TEMPLATE = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an expert DevOps engineer. You are examining some logs. Your first task is to find which Lines, if any, contain errors. Examine the following logs.<|eot_id|><|start_header_id|>user<|end_header_id|>

{INPUT}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

{OUTPUT}<|eot_id|>"""

DATA_PATH = "../bugswarm-data/data/exported/data.json"


def get_relative_path(filename):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_path, filename)


def apply_template(filename, tokenizer):
    # TODO: align train test split with dan
    dataset = load_dataset("json", data_files=filename, split="train[0:4000]")
    dataset = dataset.rename_column("context", "input")
    dataset = dataset.rename_column("hunk", "output")
    dataset = to_sharegpt(dataset, merged_prompt="{input}")
    dataset = standardize_sharegpt(dataset)

    return apply_chat_template(
        dataset,
        chat_template=CHAT_TEMPLATE,
        tokenizer=tokenizer,
    )
