# Гайд как развернуть тестовое задание у себя на машинке

## 1. Подготовка сервера

### Установка необходимых пакетов
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv nginx postgresql
```
### Создание пользователя для приложения 
```bash
sudo adduser --system --group flaskapp
```
## 2. Настройка проекта

### Клонирование репозитория
```bash
sudo mkdir -p /var/www/flaskapp
sudo chown -R flaskapp:flaskapp /var/www/flaskapp
sudo -u flaskapp git clone https://github.com/imajunnow/nshj34127.git /var/www/flaskapp
```
В корневом каталоге проекта необходимо создать файл .env с содержимым:
```code
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://username:password@localhost/dbname
```
Для этого можно использовать команды 
```code
touch .env
nano .env
```
### Настройка виртуального окружения
```bash
cd /var/www/flaskapp
sudo -u flaskapp python3 -m venv venv
source venv/bin/activate
pip install -r req.txt gunicorn
```

## 3. Настройка базы данных PostgreSQL
### Создание БД и пользователя
```bash
sudo -u postgres psql
CREATE DATABASE flaskdb;
CREATE USER flaskuser WITH PASSWORD 'ваш_пароль';
GRANT ALL PRIVILEGES ON DATABASE flaskdb TO flaskuser;
\q
```

## 4. Конфигурация Gunicorn
### Создание конфигурационного файла
> /var/www/flaskapp/gunicorn.conf.py:

```python 
bind = 'unix:/run/flaskapp.sock'
workers = 3
threads = 2
timeout = 120
user = 'flaskapp'
group = 'www-data'
accesslog = '/var/log/gunicorn/access.log'
errorlog = '/var/log/gunicorn/error.log'
```

### Настройка systemd сервиса
> /etc/systemd/system/flaskapp.service:
```ini
[Unit]
Description=definitely not a test
After=network.target postgresql.service

[Service]
User=flaskapp
Group=www-data
WorkingDirectory=/var/www/flaskapp
Environment="PATH=/var/www/flaskapp/venv/bin"
Environment="DATABASE_URL=postgresql://flaskuser:ваш_пароль@localhost/flaskdb"
ExecStart=/var/www/flaskapp/venv/bin/gunicorn --config /var/www/flaskapp/gunicorn.conf.py wsgi:app

[Install]
WantedBy=multi-user.target
```

## 5. Настройка Nginx
### Базовая конфигурация
> /etc/nginx/sites-available/flaskapp:
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/flaskapp.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static/ {
        alias /var/www/flaskapp/static/;
        expires 30d;
    }
}
```

### Активация конфигурации
```bash
sudo ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
```

## 6. Настройка прав доступа
```bash
sudo chown -R flaskapp:www-data /var/www/flaskapp
sudo chmod -R 750 /var/www/flaskapp
sudo mkdir -p /var/log/gunicorn
sudo chown flaskapp:www-data /var/log/gunicorn
sudo touch /run/flaskapp.sock
sudo chown flaskapp:www-data /run/flaskapp.sock
sudo chmod 660 /run/flaskapp.sock
```

## 7. Запуск сервисов
```bash
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
sudo systemctl restart nginx
```
### Либо запустите run.py файл 
## 8. Итоговая проверка
### Проверка работы приложения
### Откройте в браузере: http://localhost или http://127.0.0.1:8000

### Проверка статуса сервисов
```bash
sudo systemctl status flaskapp
sudo systemctl status nginx
sudo systemctl status postgresql
```
### Проверка подключения к БД
```bash
sudo -u postgres psql -d flaskdb -U flaskuser -W
```
