USER = "user"
PASSWORD = "" # fcrc0808

import logging
logging.basicConfig(
    filename='docFinder_loggers.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8',
    level=logging.INFO
)
logger = logging.getLogger(__name__)