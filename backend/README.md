# 🛰️ AeroMatrix - Drone Management API

AeroMatrix is a backend API project for managing drones flying within defined grid matrices. This project was originally developed in Java using Spring Boot and has been successfully migrated to Python using Django and Django REST Framework (DRF).

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.1-green?logo=django)
![DRF](https://img.shields.io/badge/DRF-REST_Framework-red?logo=django)

---

## 🚀 Features

- 📦 Drone and Matrix management (CRUD)
- 📡 Execute flight commands (turn, move, batch, multi-drone)
- 🚧 Collision and boundary validation
- 💥 Validation of input, logic conflicts, and duplicates
- 🧪 Custom exception handling with consistent error responses
- 📘 Auto-generated API documentation (Swagger & ReDoc)

---

## 🏗️ Project Structure

```plaintext
AeroMatrix/
├── AeroMatrix/
│   ├── settings.py            # ⚙️ Django project settings
│   ├── urls.py                # 🌍 Global URL configuration
├── drones/
│   ├── models.py              # 🧠 Data models: Drone, Matrix, Enums
│   ├── serializers/           # 📦 Drone and Matrix serializers
│   ├── interfaces/            # 🌐 ViewSets and controllers
│   ├── application/           # 🔧 Business logic and services
│   ├── domain/                # 🧱 Domain layer (repositories, exceptions)
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

```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Apply migrations and run server
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

### 🛩️ Drone Endpoints

| Method | Endpoint                             | Description                 |
| ------ | ------------------------------------ | --------------------------- |
| GET    | `/api/drones/`                       | List all drones             |
| POST   | `/api/drones/`                       | Create a new drone          |
| GET    | `/api/drones/{id}/`                  | Retrieve a specific drone   |
| PUT    | `/api/drones/{id}/`                  | Update a specific drone     |
| DELETE | `/api/drones/{id}/`                  | Delete a specific drone     |
| POST   | `/api/drones/{id}/execute_commands/` | Execute commands on a drone |

### 🚀 Flight Command Endpoints

| Method | Endpoint                        | Description                                                 |
| ------ | ------------------------------- | ----------------------------------------------------------- |
| POST   | `/api/flights/`                 | Execute same commands for multiple drones (via query param) |
| POST   | `/api/flights/drones/commands/` | Execute same commands for drones (IDs in body)              |
| POST   | `/api/flights/batch-commands/`  | Execute different commands on different drones              |

### 🗺️ Matrix Endpoints

| Method | Endpoint              | Description                    |
| ------ | --------------------- | ------------------------------ |
| GET    | `/api/matrices/`      | List all matrices              |
| POST   | `/api/matrices/`      | Create a new matrix            |
| GET    | `/api/matrices/{id}/` | Retrieve a specific matrix     |
| PUT    | `/api/matrices/{id}/` | Update a specific matrix       |
| DELETE | `/api/matrices/{id}/` | Delete a matrix (if no drones) |

---

## 💡 Example Commands

```json
POST /api/flights/drones/commands/
{
  "drone_ids": [1, 2, 3],
  "commands": ["TURN_LEFT", "MOVE_FORWARD"]
}
```

```json
POST /api/flights/batch-commands/
{
  "commands": [
    { "drone_id": 1, "commands": ["MOVE_FORWARD"] },
    { "drone_id": 2, "commands": ["TURN_LEFT", "MOVE_FORWARD"] }
  ]
}
```

---

## 🔐 Roles and Permissions

### Defined Groups

- **Operator**

  - ✅ Can view drones and matrices.
  - ❌ Cannot add, edit, or delete.

- **Drone Manager**

  - ✅ Can view, add, and modify drones.
  - ❌ Cannot delete drones or manage matrices.

- **Supervisor**

  - ✅ Can view, add, and modify matrices.
  - ❌ Cannot delete matrices or manage drones.

- **Superuser**
  - 🔓 Full access.

### Matrix of Permissions

| Group         | Model  | View | Add | Edit | Delete |
| ------------- | ------ | ---- | --- | ---- | ------ |
| Operator      | Drone  | ✅   | ❌  | ❌   | ❌     |
| Operator      | Matrix | ✅   | ❌  | ❌   | ❌     |
| Drone Manager | Drone  | ✅   | ✅  | ✅   | ❌     |
| Drone Manager | Matrix | ❌   | ❌  | ❌   | ❌     |
| Supervisor    | Drone  | ❌   | ❌  | ❌   | ❌     |
| Supervisor    | Matrix | ✅   | ✅  | ✅   | ❌     |
| Superuser     | Both   | ✅   | ✅  | ✅   | ✅     |

---

## 🙋‍♂️ Author

Developed by [@ajsantiago](mailto:ajsantiago@example.com) as part of a learning process and FCT internship project.
