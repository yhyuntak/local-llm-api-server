import logging
import sys
from pathlib import Path


class LoggerManager:
    def __init__(self, log_dir: str = "logs", level: int = logging.INFO) -> None:
        self.is_configured = False
        self.log_dir = Path(log_dir)
        self.level = level
        self._setup_directories()
        self._setup_logging()

    def _setup_directories(self):
        self.log_dir.mkdir(exist_ok=True)

    def _setup_logging(self):
        # 싱글톤 패턴을 넣는거 같은데..
        if not self.is_configured:
            logging.basicConfig(
                level=self.level,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                handlers=[
                    logging.FileHandler(self.log_dir / "app.log"),
                    logging.StreamHandler(sys.stdout),
                ],
            )
            self.is_configured = True

    def get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)


logging_manager = LoggerManager()
