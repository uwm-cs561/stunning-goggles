= Contributions

== Mondo
- Infrastructure setup (docker container with ssh access)
- Data downloading (non-trivial due to rate limit)
- Data preprocessing
- Model fine-tuning (primary)
- Writing this report

== Daniel
- Infrastructure setup (department-provided GPU machines)
- Exploratory testing
- Model fine-tuning (some assistance)
- Model evaluation
- Writing this report


= Example of Hunk and Context<h-appx-eghunk>

#figure(
  image("figure/log_hunk.png"),
  caption: [An example of Hunk and Context]
)


= Training Code Excerpt

```python
    dataset = load_dataset("json", data_files=data_files, split="train")

    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/Llama-3.2-3B-Instruct-bnb-4bit",
        max_seq_length=max_seq_length,
        dtype=None,
        load_in_4bit=True,
    )

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
        lora_dropout=0,  
        bias="none", 
        
        use_gradient_checkpointing="unsloth",
        random_state=3407,
        max_seq_length=max_seq_length,
        use_rslora=False,  
        loftq_config=None, 
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
            max_steps=60,
            fp16=not is_bfloat16_supported(),
            bf16=is_bfloat16_supported(),
            logging_steps=1,
            output_dir="outputs",
            optim="adamw_8bit",
            seed=3407,
        ),
    )

    trainer.train()
```
