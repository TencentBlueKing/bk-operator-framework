import logging

logger = logging.getLogger("bof")
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter("[%(asctime)s] %(name)-20.20s [%(levelname)-8.8s] %(message)s")
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
