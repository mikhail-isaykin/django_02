import logging

logger = logging.getLogger('products')

logger.setLevel('INFO')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console = logging.StreamHandler()

console.setLevel(logging.INFO)

console.setFormatter(formatter)

logger.addHandler(console)

logger.info('Программа запущена')

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logger.error('Деление на ноль', exc_info=True)

result1 = divide(10, 2)
print(f"Результат деления 10 на 2: {result1}")
                  

result2 = divide(10, 0)
print(f"Результат деления 10 на 0: {result2}")

if __name__ == "__main__":
    logger.debug("debug сообщение")
    logger.info("info сообщение")
    logger.warning("warning сообщение")
    logger.error("error сообщение")
    logger.critical("critical сообщение")
