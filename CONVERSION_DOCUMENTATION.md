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

El objetivo de este proyecto fue migrar una aplicación de gestión de drones desarrollada en Java con Spring Boot a Python, aprovechando el framework Django y su extensión Django REST Framework para construir APIs REST de manera rápida y robusta. Se replicaron los componentes originales (modelos, DTOs, servicios, controladores) y se adaptaron a las convenciones y buenas prácticas propias del ecosistema Python/Django.

---

## Summary of the Original Project (Java)

El proyecto Java original incluía:

- Entidades de Dominio: `Drone`, `Matrix`, `Orientation`, etc.
- DTOs: Para solicitudes y respuestas (CreateDroneRequest, DroneDto, MatrixDto, etc.)
- Servicios: Lógica de negocio en clases como `DroneService`, `FlightService` y `MatrixService`.
- Repositorios: Interfaces que extendían de `JpaRepository` para acceder a la base de datos.
- Controladores: Endpoints REST expuestos mediante Spring MVC.
- Validaciones y Manejo de Excepciones.

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

````plaintext
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
    │   │   ├── __pycache/
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

```nage.py
````

---

## Component Conversion

- **Modelos:** Se trasladaron directamente a `models.py` usando el ORM de Django.
- **DTOs:** Convertidos a serializers (`serializers.py`) usando DRF.
- **Servicios:** Lógica de negocio modularizada en `services.py`.
- **Repositorios:** Consultas personalizadas en `repositories.py`.
- **Excepciones:** Se trasladaron a `exceptions.py` y adaptadas a `APIException`.
- **Controladores:** Implementados como `ViewSet` o `APIView` en `views.py`.

---

## Integration of Documentation with drf‑spectacular

1. Se instaló con `pip install drf-spectacular`.
2. En `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
```

3. Se añadieron rutas:

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

## References

- https://www.djangoproject.com/
- https://www.django-rest-framework.org/
- https://drf-spectacular.readthedocs.io/
