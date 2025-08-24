from mlx_lm import load


class ModelManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load_model(self):
        self.model, self.tokenizer = load(
            "/Users/yoohyuntak/workspace/models/mlx/Qwen2.5-7B-Instruct"
        )
