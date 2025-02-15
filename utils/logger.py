import logging

from constants import ROOT_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f'{ROOT_DIR}/test.log'),
    ]
)

logger = logging.getLogger(__name__)
