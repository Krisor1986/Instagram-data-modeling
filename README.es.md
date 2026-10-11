# Modelado de datos de Instagram

[English](README.md) · [Español](README.es.md) · [Português](README.pt.md)

Ejercicio de modelado con SQLAlchemy de 4Geeks Academy. La entrega incluye cinco modelos relacionados y un diagrama entidad-relación; no requiere implementar un frontend ni una API.

## Modelos

| Modelo | Propósito |
| --- | --- |
| User | Nombre de usuario y correo únicos, perfil, contraseña y estado activo |
| Post | Texto de publicación, fecha de creación y autor |
| Media | URL de imagen o vídeo perteneciente a una publicación |
| Comment | Texto del comentario, autor y publicación |
| Follower | Relación dirigida entre dos usuarios |

Un usuario tiene muchas publicaciones y comentarios. Una publicación tiene muchos archivos multimedia y comentarios. Follower conecta usuarios mediante dos claves foráneas: la clave primaria compuesta impide seguimientos duplicados y una restricción impide seguirse a uno mismo. Media acepta únicamente `image` o `video`. Al eliminar una publicación mediante el ORM, se eliminan sus archivos multimedia y comentarios. La serialización excluye la contraseña; una implementación de autenticación debe almacenar su hash.

## Ejecución local

Requisitos: Python 3.13, Pipenv y el ejecutable nativo de Graphviz (`dot`) en PATH. El paquete Python `graphviz` no instala `dot`. En este Mac, Graphviz ya está disponible en el entorno Pipenv del proyecto.

```bash
pipenv install
pipenv run diagram
pipenv run test
```

También puedes generar el diagrama con `pipenv run python src/models.py`. El resultado es `diagram.png` en la raíz. La generación y las pruebas no necesitan un servidor de base de datos ni un archivo `.env`. Las pruebas utilizan SQLite real en memoria con claves foráneas habilitadas.

![Diagrama entidad-relación](diagram.png)

Leyenda: PK = clave primaria, FK = clave foránea, UQ = único, * = obligatorio. Las líneas representan relaciones uno a muchos. Las restricciones del tipo de multimedia y de seguimiento están en `src/models.py`.

## Fuentes

Este repositorio es un fork del [ejercicio oficial](https://github.com/breatheco-de/exercise-instagram-data-modeling). Los archivos iniciales de Flask proceden del [template flask-rest-hello de la escuela](https://github.com/4GeeksAcademy/flask-rest-hello). El modelo sigue el diagrama de referencia de cinco entidades. Se conservan los archivos de API, despliegue y migraciones del template; están fuera del alcance de esta entrega. No hace falta un Codespace.
