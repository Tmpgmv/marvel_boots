# Санкт-Петербургское государственное бюджетное профессиональное образовательное учреждение "Политехнический колледж городского хозяйства"

## 09.02.07 Информационные системы и программирование (Программист)

---

## Экзаменационная работа `Чудо Обувь`
Выполнил: Граблевский Михаил Владимирович

Сеть магазинов обуви


## Создание виртуального окружения
```bash 
python -m venv .venv
```

## Активация виртуального окружения
```bash 
.venv\Scripts\activate  # Windows

source .venv/bin/activate # Linux/MacOS
```

## Установка зависимостей
```bash 
pip install --no-index --find-links=D:\dependencies -r requirements.txt
```

## Применение миграций
```bash
python manage.py migrate
```

## Создать суперпользователя (по необходимости)
```bash
python manage.py createsuperuser
```

## Создать пользователей
```bash
python manage.py createusers
```


## Запуск сервера
```bash
python manage.py runserver
```

## Выполнение тестов
```bash
python manage.py test
```

