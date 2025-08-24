import logging
import logging.handlers
import sys
from pathlib import Path


class LoggerManager:
    def __init__(self, log_dir: str = "logs", level: int = logging.INFO) -> None:
        self.is_configured = False
        self.log_dir = Path(log_dir)
        self.level = level
        self._setup_directories()
        self._setup_logging()

    def get_logger(self, name: str) -> logging.Logger:
        return logging.getLogger(name)

    def _setup_directories(self):
        self.log_dir.mkdir(exist_ok=True)

    def _setup_logging(self):
        # 싱글톤 패턴을 넣는거 같은데..
        if not self.is_configured:
            # 날짜별 + 크기 기반 핸들러 생성
            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=self.log_dir / "app.log",
                when="midnight",  # 매일 자정에 새 파일
                interval=1,  # 1일 간격
                backupCount=30,  # 30일간 보관
                encoding="utf-8",
            )

            # 콘솔 핸들러
            console_handler = logging.StreamHandler(sys.stdout)

            # 포맷터 설정
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)

            logging.basicConfig(
                level=self.level,
                handlers=[file_handler, console_handler],
            )
            self.is_configured = True


logging_manager = LoggerManager()
