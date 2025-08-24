from mlx_lm import load


class ModelManager:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load_model(self):
        ## 모델 input을 받아서 로드하도록 하기.
        self.model, self.tokenizer = load(
            "/Users/yoohyuntak/workspace/models/mlx/Qwen2.5-7B-Instruct"
        )
