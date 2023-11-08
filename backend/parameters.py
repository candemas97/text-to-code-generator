class Args:
    # define training arguments

    # MODEL
    model_type = "t5"
    tokenizer_name = "Salesforce/codet5-base"
    model_name_or_path = "Salesforce/codet5-base"

    # DATA
    train_batch_size = 8
    validation_batch_size = 8
    max_input_length = 48
    max_target_length = 128
    prefix = "Generate Python: "

    # OPTIMIZER
    learning_rate = 3e-4
    weight_decay = 1e-4
    warmup_ratio = 0.2
    adam_epsilon = 1e-8

    # TRAINING
    seed = 2022
    epochs = 20

    # DIRECTORIES
    output_dir = "runs/"
    logging_dir = f"{output_dir}/logs/"
    checkpoint_dir = f"checkpoint"
    save_dir = f"{output_dir}/saved_model/"  # HERE YOU MUST ADD THE COMPLETE PATH WHERE THE PRETRAINED MODEL IS
    cache_dir = "../working/"
