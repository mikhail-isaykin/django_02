import logging

logger = logging.getLogger('products')

logger.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console = logging.StreamHandler()

console.setLevel(logging.DEBUG)

console.setFormatter(formatter)

logger.addHandler(console)

file = logging.FileHandler('app.log', encoding='utf-8')

file.setLevel(logging.DEBUG)

file.setFormatter(formatter)

logger.addHandler(file)

logger.debug('Начало выполнения')
logger.info('Сообщение')
logger.warning('Скоро закончится место на диске')
logger.error('Файл не найден')
logger.critical('Система недоступна')


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        logger.error('Деление на ноль', exc_info=True)


result1 = divide(10, 2)
print(f'Результат деления 10 на 2: {result1}')

result2 = divide(10, 0)
print(f'Результат деления 10 на 0: {result2}')

"""
try:
    file = open(
        'missing_file.txt',
        mode='r',
        encoding='utf-8',
    )
except FileNotFoundError:
    logger.exception('Файла не существует')
"""
def multiply(a, b):
    logger.info(f'Выполняем умножение {a} * {b}')
    result = a * b
    logger.debug(f'Результат: {result}')
    return result

if __name__ == '__main__':
    logger.debug('debug сообщение')
    for num in range(1, 6):
        if num == 3:
            logger.warning(f'Особое число {num}')
        else:
            logger.info(f'Текущее число: {num}')
    #logger.info(f'Текущее число: {num}')
    #logger.warning('warning сообщение')
    logger.error('error сообщение')
    logger.critical('critical сообщение')
    
product = multiply(5, 3)