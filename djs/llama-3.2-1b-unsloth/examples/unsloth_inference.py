from unsloth import FastLanguageModel
from unsloth import is_bfloat16_supported
import torch
from trl import SFTTrainer
from transformers import TrainingArguments
from transformers import TextStreamer
from datasets import load_dataset

max_seq_length = 2048  # Supports RoPE Scaling interally, so choose any!

# 4bit pre quantized models we support for 4x faster downloading + no OOMs.
fourbit_models = [
    "unsloth/Llama-3.2-1B-bnb-4bit",  # NEW! Llama 3.2 models
    "unsloth/Llama-3.2-1B-Instruct-bnb-4bit",
    "unsloth/Llama-3.2-3B-bnb-4bit",
    "unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
]  # More models at https://huggingface.co/unsloth

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
    max_seq_length=max_seq_length,
    dtype=None,
    load_in_4bit=True,
)

alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

FastLanguageModel.for_inference(model)  # Enable native 2x faster inference
inputs = tokenizer(
    [
        alpaca_prompt.format(
            "Continue the fibonnaci sequence.",  # instruction
            "1, 1, 2, 3, 5, 8",  # input
            "",  # output - leave this blank for generation!
        )
    ],
    return_tensors="pt",
).to("cuda")

print()
print(f"Input tokens: {len(inputs[0])}")
print()

text_streamer = TextStreamer(tokenizer)

outputs = model.generate(
    **inputs,
    streamer=text_streamer,
    max_new_tokens=128,
    # use_cache=True
)

(decoded_outputs,) = tokenizer.batch_decode(outputs)

print()

print(f"Tokens output: {len(outputs[0])}")
print(f"Final token: {tokenizer.decode(outputs[0][-1])}")
# print(decoded_outputs)
