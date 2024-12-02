from unsloth import FastLanguageModel
from unsloth import is_bfloat16_supported
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
from datetime import datetime
import os

from dataloader import apply_template, get_relative_path

SAVED_WEIGHTS_DIR = "saved_weights"
max_seq_length = 2048  # Supports RoPE Scaling interally, so choose any!

date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def lora_finetune(*, training_data_filename, model_output_dir):
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
        max_seq_length=max_seq_length,
        dtype=None,
        load_in_4bit=True,
    )

    dataset = apply_template(get_relative_path(training_data_filename), tokenizer)

    # Do model patching and add fast LoRA weights
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        lora_alpha=16,
        lora_dropout=0,  # Supports any, but = 0 is optimized
        bias="none",  # Supports any, but = "none" is optimized
        # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
        use_gradient_checkpointing="unsloth",  # True or "unsloth" for very long context
        random_state=3407,
        max_seq_length=max_seq_length,
        use_rslora=False,  # We support rank stabilized LoRA
        loftq_config=None,  # And LoftQ
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=dataset,
        dataset_text_field="text",
        max_seq_length=max_seq_length,
        tokenizer=tokenizer,
        args=TrainingArguments(
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=10,
            max_steps=1,  # 60,
            fp16=not is_bfloat16_supported(),
            bf16=is_bfloat16_supported(),
            logging_steps=1,
            output_dir="outputs",
            optim="adamw_8bit",
            seed=3407,
        ),
    )

    trainer.train()

    save_to_dir = os.path.join(SAVED_WEIGHTS_DIR, model_output_dir)
    model.save_pretrained(save_to_dir)
    tokenizer.save_pretrained(save_to_dir)


if __name__ == "__main__":
    lora_finetune(
        training_data_filename="../bugswarm-data/data/exported/data.json",
        model_output_dir=f"trained_model-{date}",
    )
