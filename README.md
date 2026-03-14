# Django Training Project

Проект содержит обучающие модели и данные для практики Django ORM: `F`, `Q`, `annotate`, `Window`, `ExpressionWrapper`, `Rank`, `Concat` и другим.

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/username/training_project.git
cd training_project
```

### 2. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Восстановление базы данных

Убедись что PostgreSQL установлен и запущен, затем восстанови базу из дампа:
```bash
createdb training_db
psql -U <ваш_пользователь> -d training_db -f dump.sql
```

### 5. Настройка подключения к БД

В файле `training_project/settings.py` укажи свои параметры:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'training_db',
        'USER': 'ваш_пользователь',
        'PASSWORD': 'ваш_пароль',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 6. Запуск
```bash
python manage.py runserver
```

---

## Темы

- Базовый ORM: `filter`, `get`, `update`, `create`, `delete`
- Агрегации: `Count`, `Avg`, `Sum`
- Аннотации и выражения: `annotate`, `F`, `Q`, `ExpressionWrapper`
- Продвинутые конструкции: `Case`, `When`, `Window`, `DenseRank`, `Rank`
- Работа с датами и временем
