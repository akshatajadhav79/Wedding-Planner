# 💍 Wedding Planner

A full-featured **Wedding Planning Management System** built with **Django** — designed to help customers, organizers, and admins seamlessly manage every aspect of a wedding event.

---

## 📁 Project Structure

```
WEDDING_PLANNER/
│
├── Admin/                  # Admin panel app
│   ├── migrations/         # Database migrations
│   ├── middleware/         # Custom middleware
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── Customer/               # Customer-facing app
├── DataAccess/             # Data access layer / shared DB logic
├── Organizer/              # Organizer/vendor management app
│
├── assets/                 # Static assets (images, icons, etc.)
├── staticfiles/            # Collected static files
├── Templates/              # HTML templates
│
├── wedding_planner/        # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── db.sqlite3              # SQLite database (development)
└── manage.py               # Django management script
```

---

## 🚀 Features

- 👤 **Customer Portal** — Browse, book, and manage wedding packages
- 🗂️ **Admin Dashboard** — Manage users, bookings, vendors, and events
- 🏢 **Organizer Module** — Organizers can manage their services and schedules
- 🔐 **Role-based Access** — Separate flows for Customers, Organizers, and Admins
- 🗄️ **Centralized Data Access Layer** — Clean separation of DB logic

---

## 🛠️ Tech Stack

| Layer       | Technology        |
|-------------|-------------------|
| Backend     | Python, Django    |
| Database    | SQLite (dev)      |
| Frontend    | HTML, CSS, JS     |
| Templating  | Django Templates  |

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/wedding-planner.git
cd wedding-planner
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌐 URL Structure

| URL Prefix     | Module        | Description                  |
|----------------|---------------|------------------------------|
| `/admin/`      | Django Admin  | Built-in admin interface     |
| `/customer/`   | Customer      | Customer-facing pages        |
| `/organizer/`  | Organizer     | Organizer dashboard & tools  |
| `/panel/`      | Admin App     | Custom admin panel           |

---

## 🗃️ Database

The project uses **SQLite** (`db.sqlite3`) for development.

For production, it is recommended to switch to **PostgreSQL** or **MySQL** by updating `DATABASES` in `wedding_planner/settings.py`.

---

## 📦 Requirements

Make sure you have the following installed:

- Python 3.9+
- Django 4.x
- pip

Generate `requirements.txt` with:
```bash
pip freeze > requirements.txt
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

For queries or contributions, feel free to reach out via GitHub Issues.
