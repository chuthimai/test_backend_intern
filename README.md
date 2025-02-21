# CRM System

##  Giới Thiệu
Dự án **CRM System** được xây dựng bằng **Django Rest Framework (DRF)** nhằm quản lý khách hàng, nhân viên, sản phẩm và bảng công việc. Dự án sử dụng **JWT authentication** để xác thực người dùng và **drf-spectacular** để tạo tài liệu API.

##  Công Nghệ Sử Dụng
- **Python** (Django, Django REST Framework)
- SQLite
- **JWT Authentication** (SimpleJWT)
- **Swagger UI** (drf-spectacular)

## Tổ chức thư mục
- Trong folder **crm_system**:
  - Các file trong folder **api** viết các lớp trả về methods cho các đối tượng
  - File **models.py** lưu cấu hình các model sử dụng
  - Các file trong folder **dao** sử dụng để lấy dữ liệu từ các model + xử lý
  - File **serializers.py** viết các lớp chuyển đổi model thành JSON
  - File **views.py** viết các function cho các đường link đăng ký, đăng nhập, đăng xuất
  - File **admin.py** đăng ký các lớp quản lý bởi admin có sẵn của Django

---
##  Cài Đặt
###  Clone Repository
```bash
git clone https://github.com/chuthimai/test_backend_intern.git
```

### Tạo Virtual Environment & Cài Đặt Packages
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Chạy Migration & Tạo Superuser
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Chạy Server
```bash
python manage.py runserver
```

---
## Xác Thực (JWT Authentication)
Sử dụng **SimpleJWT** để đăng nhập và nhận JWT Token.

**Login API**
```
POST /login/
{
    "email": "user@gmail.com",
    "password": "123"
}
```

**Response**
```json
{
    "refresh": "eyJhbGciOiJIUzI1...",
    "access": "eyJhbGciOiJIUzI1..."
}
```

**Sử dụng Token để truy cập API**
```
Authorization: Bearer <access_token>
```

---
## Tài Liệu API (Swagger UI)
Dự án sử dụng **drf-spectacular** để tự động tạo tài liệu API.

- **Schema API**: `http://127.0.0.1:8000/schema/`
- **Swagger UI**: `http://127.0.0.1:8000/docs/`
- **Redoc UI**: `http://127.0.0.1:8000/redoc/`
