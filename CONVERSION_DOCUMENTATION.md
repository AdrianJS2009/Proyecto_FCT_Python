
# Java to Python Project Conversion with Django and DRF

This documentation outlines the process and decisions made to migrate a Java project based on Spring Boot to a Python project using Django and Django REST Framework (DRF). It explains the project structure, the dependencies used, the business logic, and the improvements implemented (such as automatic documentation with drf-spectacular).

---

## Table of Contents

- [Java to Python Project Conversion with Django and DRF](#java-to-python-project-conversion-with-django-and-drf)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Summary of the Original Project (Java)](#summary-of-the-original-project-java)
  - [Technologies and Dependencies Used](#technologies-and-dependencies-used)
    - [Java Project](#java-project)
    - [Python Project](#python-project)
  - [Project Structure in Python](#project-structure-in-python)
  - [Component Conversion](#component-conversion)
  - [Integration of Documentation with drf‑spectacular](#integration-of-documentation-with-drfspectacular)
    - [Challenges Faced](#challenges-faced)
    - [Documentation Consulted](#documentation-consulted)
  - [References](#references)

---

## Introduction

The objective of this project was to migrate a drone management application developed in Java with Spring Boot to Python, leveraging the Django framework and its extension Django REST Framework to build REST APIs quickly and robustly. The original components (models, DTOs, services, controllers) were replicated and adapted to the conventions and best practices of the Python/Django ecosystem.

---

## Summary of the Original Project (Java)

The original Java project included:

- Domain Entities: `Drone`, `Matrix`, `Orientation`, etc.
- DTOs: For requests and responses (CreateDroneRequest, DroneDto, MatrixDto, etc.)
- Services: Business logic in classes like `DroneService`, `FlightService`, and `MatrixService`.
- Repositories: Interfaces extending `JpaRepository` for database access.
- Controllers: REST endpoints exposed using Spring MVC.
- Validations and Exception Handling.

---

## Technologies and Dependencies Used

### Java Project

- Spring Boot 3.x
- Spring Data JPA
- Hibernate
- Lombok
- MySQL/H2
- Swagger/OpenAPI

### Python Project

- Django 5.1.7
- Django REST Framework (DRF)
- drf-spectacular
- SQLite

---

## Project Structure in Python

```
└── Proyecto_FCT_Python/
    ├── AeroMatrix/
    │   ├── AeroMatrix/
    │   │   ├── __init__.py
    │   │   ├── asgi.py
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   └── wsgi.py
    │   ├── db.sqlite3
    │   ├── drones/
    │   │   ├── __init__.py
    │   │   ├── __pycache__/
    │   │   ├── admin.py
    │   │   ├── apps.py
    │   │   ├── exceptions.py
    │   │   ├── models.py
    │   │   ├── repositories.py
    │   │   ├── serializers.py
    │   │   ├── services.py
    │   │   ├── tests.py
    │   │   ├── urls.py
    │   │   └── views.py
    │   └── manage.py
    ├── CONVERSION_DOCUMENTATION.md
    ├── README.md
    └── requirements.txt
```

---

## Component Conversion

- **Models:** Directly migrated to `models.py` using Django's ORM.
- **DTOs:** Converted to serializers (`serializers.py`) using DRF.
- **Services:** Business logic modularized in `services.py`.
- **Repositories:** Custom queries handled in `repositories.py`.
- **Exceptions:** Moved to `exceptions.py` and adapted to `APIException`.
- **Controllers:** Implemented as `ViewSet` or `APIView` in `views.py`.

---

## Integration of Documentation with drf‑spectacular

1. Installed with `pip install drf-spectacular`.
2. In `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

3. Added routes:

```python
path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
```

---

### Challenges Faced

- **Learning Curve:** Coming from a Java background, adjusting to Python’s dynamic typing and indentation-based syntax required effort.
- **ORM Differences:** JPA/Hibernate and Django ORM differ in philosophy. Query optimization, lazy loading, and related model behaviors had to be relearned.
- **Error Handling:** Mapping Java-style checked exceptions to Pythonic exception handling with DRF required careful planning.
- **Documentation Tools:** DRF does not provide Swagger UI out of the box, so third-party tools like `drf-spectacular` were explored and integrated.

### Documentation Consulted

- [Django Official Documentation](https://docs.djangoproject.com/en/stable/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- Community articles, GitHub examples, and StackOverflow threads were essential in resolving practical implementation issues.

---

## References

- https://www.djangoproject.com/
- https://www.django-rest-framework.org/
- https://drf-spectacular.readthedocs.io/
