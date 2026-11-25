# 🎬 Netflix Clone – Movie & TV Series Platform

A desktop-based movie and TV series streaming platform inspired by Netflix, developed using **Python, PyQt6, and MySQL**.

The application provides a user-friendly interface where users can explore movies and TV series, manage their favorite content, rate programs, track their watching history, and receive personalized content recommendations.

It also includes an administrator panel for managing users and platform content.

## ✨ Features

### 👤 User Management & Authentication
- User registration and login system
- Secure password hashing using BCrypt
- Role-based access control (User / Administrator)
- User profile management
- Account information management

### 🎥 Content Management
- Browse movies and TV series
- View detailed information about programs
- Explore content by genre
- Display movie and TV series information
- Track viewing progress

### ⭐ Personalization
- Add and remove movies or TV series from favorites
- Rate content using a 1–10 rating system
- Personalized recommendations based on user preferences and selected genres
- Track previously watched content
- Continue watching from the last saved position

### 📊 Watch History
- Record individual viewing sessions
- Track watched episodes and viewing duration
- Monitor completed and unfinished content
- View total watching time

### 🛠️ Administrator Panel
- Administrator authentication and authorization
- User management
- View user details
- Manage platform data
- Access administrative operations

## 🧰 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| PyQt6 | Desktop graphical user interface |
| MySQL | Relational database management |
| mysql-connector-python | Python–MySQL connection |
| bcrypt | Password hashing |
| Babel | Localization and formatting |

## 🗄️ Database Architecture

The application uses a relational MySQL database named `netflix_platform`.

The database includes the following main tables:

- `Rol` – User roles
- `Kullanici` – User information
- `Tur` – Content genres
- `KullaniciTur` – User genre preferences
- `Program` – Movies and TV series
- `ProgramTur` – Program and genre relationships
- `Bolum` – TV series episodes
- `Favori` – Favorite programs
- `KullaniciProgram` – User ratings and viewing progress
- `IzlemeLog` – Viewing session records
- `OturumLog` – Login and logout records

The database design uses primary keys, foreign keys, unique constraints, and relational associations to maintain data integrity.

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/betulkulaksizz/Netflix_projesi.git
```

Navigate to the project directory:

```bash
cd Netflix_projesi
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**macOS / Linux**
```bash
source venv/bin/activate
```

**Windows**
```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database

- Install and start MySQL Server.
- Open MySQL Workbench or your preferred MySQL client.
- Execute the `database.sql` script to create the database and tables.
- Configure your MySQL connection settings in `database.py`.

Make sure to configure your own database credentials. Do not commit passwords or other sensitive information to GitHub.

### 5. Run the Application

After completing the database configuration, run the main application entry point:

```bash
python main.py
```

## 📁 Project Structure

The project is organized into separate modules for authentication, database operations, user interfaces, content management, and administrative operations.

```text
Netflix_projesi/
│
├── main.py
├── auth.py
├── database.py
├── database.sql
├── queries.py
├── queries_admin.py
├── excel_to_sql.py
│
├── login_page.py
├── register_page.py
├── home_page.py
├── detail_page.py
├── watch_page.py
├── favorites_page.py
├── history_page.py
├── profile_page.py
├── recommendation_page.py
├── user_recommendation_page.py
│
├── admin_panel.py
├── admin_dialogs.py
├── admin_user_detail.py
│
├── rating_dialog.py
├── requirements.txt
└── test_suite.py
```

## 🧪 Testing

The project includes a test suite (`test_suite.py`) and a test report (`test_report.txt`) to support application testing.

## 🎯 Project Objectives

This project was developed to gain practical experience in:

- Object-oriented programming with Python
- Desktop application development using PyQt6
- Relational database design and SQL queries
- Database integration and data management
- User authentication and role-based authorization
- Modular software architecture
- Application testing and debugging

## 👩‍💻 Developer

**Betül Kulaksız**

Computer Engineering Student

- GitHub: [@betulkulaksizz](https://github.com/betulkulaksizz)
- Project Repository: [Netflix_projesi](https://github.com/betulkulaksizz/Netflix_projesi)

---

⭐ If you find this project interesting, feel free to explore the repository!
