# pip install transformers == 4.33.1
# pip install sentencepiece == 0.1.99
# pip install sacremoses == 0.0.53

import transformers
import random
import parameters


# Se entrena modelo con traductor español - inglés
def traductor(pregunta: str) -> str:
    """Tranducir una frase que se ingrese del español al inglés

    Args:
        pregunta (str): Pregunta en español a ser traducida

    Returns:
        str: Pregunta en inglés
    """
    translator = transformers.pipeline(
        "translation_es_to_en", model="Helsinki-NLP/opus-mt-es-en"
    )
    english_quesion = translator(
        pregunta, clean_up_tokenization_spaces=True, truncation=True
    )
    return english_quesion[0]["translation_text"]


def run_predict(args, text):
    # load saved finetuned model
    model = transformers.TFT5ForConditionalGeneration.from_pretrained(args.save_dir)
    # load saved tokenizer
    tokenizer = transformers.RobertaTokenizer.from_pretrained(args.save_dir)

    # encode texts by prepending the task for input sequence and appending the test sequence
    query = args.prefix + text
    encoded_text = tokenizer(
        query,
        return_tensors="tf",
        padding="max_length",
        truncation=True,
        max_length=args.max_input_length,
    )

    # inference
    generated_code = model.generate(
        encoded_text["input_ids"],
        attention_mask=encoded_text["attention_mask"],
        max_length=args.max_target_length,
        top_p=0.95,
        top_k=50,
        repetition_penalty=2.0,
        num_return_sequences=1,
    )

    # decode generated tokens
    decoded_code = tokenizer.decode(generated_code.numpy()[0], skip_special_tokens=True)
    return decoded_code


def predict_from_dataset(args):
    # load using hf datasets
    dataset = load_dataset("json", data_files="../working/mbpp.jsonl")
    # train test split
    dataset = dataset["train"].train_test_split(0.1, shuffle=False)
    test_dataset = dataset["test"]

    # randomly select an index from the validation dataset
    index = random.randint(0, len(test_dataset))
    text = test_dataset[index]["text"]
    code = test_dataset[index]["code"]

    # run-predict on text
    decoded_code = run_predict(args, text)

    print("#" * 25)
    print("QUERY: ", text)
    print()
    print("#" * 25)
    print("ORIGINAL: ")
    print("\n", code)
    print()
    print("#" * 25)
    print("GENERATED: ")
    print("\n", decoded_code)


def predict_from_text(args, text, text_spanish: str = ""):
    # run-predict on text
    decoded_code = run_predict(args, text)
    if text_spanish != "":
        print("#" * 25)
        print(f"QUERY IN SPANISH: {text_spanish}\n")

    print("#" * 25)
    print(f"QUERY: {text}\n")
    print("#" * 25)
    print(f"GENERATED:\n{decoded_code}")

    return text_spanish, text, decoded_code


def generate_text_to_code_en(query: str) -> str:
    # initialize training arguments
    args = parameters.Args()
    return predict_from_text(args, query)


def generate_text_to_code_es(query: str) -> str:
    # initialize training arguments
    args = parameters.Args()
    question = traductor(query)
    return predict_from_text(args, question, query)


def generate_text_to_code(query: str, idioma: str) -> tuple[str]:
    if str(idioma.lower()) == "english":
        return generate_text_to_code_en(query)
    elif str(idioma.lower()) == "spanish":
        return generate_text_to_code_es(query)
    else:
        print("Just two possible languages (English or Spanish). Try Again.")


if __name__ == "__main__":
    generate_text_to_code("Funcion que divida por numeros pares", "spanish")
    generate_text_to_code(
        "Generate a Function that raise to the power of any number", "english"
    )
