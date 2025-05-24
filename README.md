# 🛡️ Building a Secure Online Exam System with Django and Permit.io

This project demonstrates how to build a secure, role-based online exam platform using **Django** and **Permit.io**.

It allows:
- 🧑‍🏫 Admins to create exams, assign questions, and view student results.
- 👨‍🎓 Students to attempt time-based exams and view only their own results.
- 🔐 Role-based access control powered by [Permit.io](https://www.permit.io/).

## 🚀 Features

- Custom `User` model with roles (admin/student)
- Secure login and registration flow
- Exam creation with dynamic question management
- Student exam-taking interface
- Role-based views and Permit.io authorization checks
- Bootstrap UI with clear layout and navigation

## 🏁 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/online-exam-system.git
cd online-exam-system
```

### 2. Set Up Environment
Create a .env file with:
```env
DJANGO_SECRET_KEY=your-secret-key
DB_NAME=exam_system
DB_USER=your_db_user
DB_PASSWORD=your_password
PERMIT_API_KEY=your_permit_api_key
PERMIT_PDP_URL=https://cloudpdp.api.permit.io
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

### 5. Sync Roles & Permissions with Permit.io
```bash
python permit_setup.py
```

🔐 Access Control Powered by Permit.io
Permit.io enforces role-based and attribute-based access control for:
- Attempting exams
- Viewing results
- Managing content visibility

Policies can be customized directly from the Permit dashboard.
