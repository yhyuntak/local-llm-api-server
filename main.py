from mlx_lm import generate, load


def main():
    print("Hello from local-llm-api-server!")

    model, tokenizer = load(
        "/Users/yoohyuntak/workspace/models/mlx/Qwen2.5-7B-Instruct"
    )
    response = generate(model, tokenizer, prompt="Hello, how are you?", verbose=True)
    print(response)


if __name__ == "__main__":
    main()
