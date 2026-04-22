import logging

'''
class SmartFileHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.errors_log_plus = open('errors.log', 'a', encoding='utf-8')
        self.info_log_plus = open('info.log', 'a', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.setFormatter(formatter)

    def emit(self, record):
        msg = self.format(record)
        if record.levelno >= logging.ERROR:
            self.errors_log_plus.write(msg + '\n')
        elif record.levelno >= logging.INFO:
            self.info_log_plus.write(msg + '\n')
'''


logger = logging.getLogger()

logger.setLevel('DEBUG')

formatter = logging.Formatter('[%(asctime)s] %(name)s | %(levelname)-8s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console = logging.StreamHandler()

console.setLevel(logging.DEBUG)

console.setFormatter(formatter)

logger.addHandler(console)

file = logging.FileHandler('system.log', 'a', encoding='utf-8')

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
        logger.exception('Ошибка деления')


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
    logger.info(f'{__name__}: Начало работы программы')
    #logger.warning('warning сообщение')
    logger.error('error сообщение')
    logger.critical('critical сообщение')
    
product = multiply(5, 3)

name = input('Введите имя: ')
if name:
    logger.info(f'Пользователь ввёл имя: {name}')
else:
    logger.warning('Имя не введено')


app_logger = logging.getLogger('products')
app_logger.setLevel('DEBUG')
file = logging.FileHandler('products.log', 'a', encoding='utf-8')
file.setLevel(logging.DEBUG)
app_formatter = logging.Formatter('[%(asctime)s] %(name)s | %(levelname)-8s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file.setFormatter(app_formatter)
app_logger.addHandler(file)

db_logger = logging.getLogger('db')
db_logger.setLevel('DEBUG')
file = logging.FileHandler('db.log', 'a', encoding='utf-8')
file.setLevel(logging.DEBUG)
db_formatter = logging.Formatter('[%(asctime)s] DB | %(levelname)-8s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file.setFormatter(db_formatter)
db_logger.addHandler(file)
