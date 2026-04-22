import logging

logger = logging.getLogger('products')

logger.setLevel('INFO')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console = logging.StreamHandler()

console.setLevel(logging.INFO)

console.setFormatter(formatter)

logger.addHandler(console)

logger.info('Программа запущена')

if __name__ == "__main__":
    logger.debug("debug сообщение")
    logger.info("info сообщение")
    logger.warning("warning сообщение")
    logger.error("error сообщение")
    logger.critical("critical сообщение")
