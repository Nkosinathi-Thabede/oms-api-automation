import logging
import os


def setup_logging(level: str = "INFO") -> None:
    os.makedirs("reports", exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("reports/test_run.log", mode="w")
        ]
    )
