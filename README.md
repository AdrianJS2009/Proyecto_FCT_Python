# 🛰️ AeroMatrix - Drone Management API

AeroMatrix is a backend API project for managing drones flying within defined grid matrices. This project was originally developed in Java using Spring Boot and has been successfully migrated to Python using Django and Django REST Framework (DRF).

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.1-green?logo=django)
![DRF](https://img.shields.io/badge/DRF-REST_Framework-red?logo=django)

---

## 🚀 Features

- 📦 Drone and Matrix management (CRUD)
- 📡 Execute flight commands (turn, move, batch)
- 🚧 Collision and boundary validation
- 📘 Auto-generated API documentation (Swagger & ReDoc)
- 🧪 Custom exception handling

---

## 🏗️ Project Structure

```plaintext
AeroMatrix/
├── AeroMatrix/
│   ├── settings.py            # ⚙️ Django project settings
│   ├── urls.py                # 🌍 Global URL configuration
├── drones/
│   ├── models.py              # 🧠 Data models: Drone, Matrix, Enums
│   ├── serializers.py         # 📦 Serializers (DTOs) for input/output
│   ├── exceptions.py          # 🚨 Custom exceptions & handlers
│   ├── repositories.py        # 🔎 Custom ORM queries
│   ├── services.py            # 🔧 Business logic
│   ├── views.py               # 🌐 API views and ViewSets
│   ├── urls.py                # 📍 Local routes for the app
├── manage.py                  # 🚀 Django entrypoint
```

---

## 📦 Requirements

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

Main dependencies:

- `django`
- `djangorestframework`
- `drf-spectacular`

---

## ⚙️ Running the Project

1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac
```

2. Run migrations and start the development server:

```bash
python manage.py migrate
python manage.py runserver
```

---

## 🔍 API Documentation

- Swagger UI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- ReDoc: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)
- OpenAPI Schema (JSON): [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)

---

## 📌 Endpoints Overview

### Drone Endpoints

- `GET /api/drones/` - List all drones
- `POST /api/drones/` - Create a new drone
- `GET /api/drones/{id}/` - Retrieve a specific drone
- `PUT /api/drones/{id}/` - Update a specific drone
- `DELETE /api/drones/{id}/` - Delete a specific drone
- `POST /api/drones/{id}/execute_commands/` - Execute commands for a specific drone

### Flight Endpoints

- `POST /api/flights/` - Execute commands in sequence for multiple drones (query param: `droneIds`)

### Batch Command Endpoints

- `POST /api/flights/batch-commands/` - Execute batch commands for multiple drones

### Matrix Endpoints

- `GET /api/matrices/` - List all matrices
- `POST /api/matrices/` - Create a new matrix
- `GET /api/matrices/{id}/` - Retrieve a specific matrix
- `PUT /api/matrices/{id}/` - Update a specific matrix
- `DELETE /api/matrices/{id}/` - Delete a specific matrix

---

## 🙋‍♂️ Author

Developed by [@ajsantiago](mailto:ajsantiago@example.com) as part of a learning process and FCT internship project.

---
