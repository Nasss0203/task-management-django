# Hướng dẫn cài đặt và khởi chạy dự án Django + MySQL

## 1. Tạo và kích hoạt môi trường ảo:

    python -m venv .venv
    .venv\Scripts\activate

## 2. Cài đặt thư viện phụ thuộc:

    Nếu chưa có:
        pip install django
        pip install djangorestframework
        pip install djangorestframework-simplejwt
        pip install django-cors-headers
        pip install cryptography
        pip install pymysql
        pip install openpyxl

## 3. Cấu hình kết nối MySQL trong settings.py:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'tên_database',
            'USER': 'tên_user',
            'PASSWORD': 'mật_khẩu',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }

## 4. Quản lý cơ sở dữ liệu:

    Tạo migration:

        python manage.py makemigrations

    Áp dụng migration:

        python manage.py migrate

## 5. Chạy ứng dụng:

    .venv\Scripts\activate

    python manage.py runserver

    Truy cập: http://127.0.0.1:8000
