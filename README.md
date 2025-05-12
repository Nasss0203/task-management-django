# Hướng dẫn cài đặt và khởi chạy dự án Django + MySQL

## 1. Tạo và kích hoạt môi trường ảo:

    - Windows:

        python -m venv .venv
        .venv\Scripts\activate

    - macOS / Linux:

        python3 -m venv .venv
        source .venv/bin/activate

## 2. Cài đặt thư viện phụ thuộc:

    Nếu chưa có:
        pip install django
        pip install djangorestframework
        pip install mysqlclient
        (hoặc thay bằng: pip install pymysql)

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

    Nếu dùng pymysql, thêm vào __init__.py (trong cùng thư mục với settings.py):

        import pymysql
        pymysql.install_as_MySQLdb()

## 4. Quản lý cơ sở dữ liệu:

    Tạo migration:

        python manage.py makemigrations

    Áp dụng migration:

        python manage.py migrate

    Nếu đã có CSDL và muốn đánh dấu migrate ban đầu:

        python manage.py migrate --fake-initial

    Truy cập shell Django:

        python manage.py shell

    Sinh model từ database có sẵn:

        python manage.py inspectdb

## 5. Chạy ứng dụng:

    source .venv/bin/activate

    python manage.py runserver

    Truy cập: http://127.0.0.1:8000
