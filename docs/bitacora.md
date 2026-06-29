# Bitácora del proyecto

## Día 1

- Git instalado correctamente.
- Repositorio agenda-360 creado.
- Se detectó Python 3.14 como versión activa.
- Se evaluará usar Python 3.13 por compatibilidad.

## 22/06/2026

### Objetivo
Configurar la conexión entre FastAPI y PostgreSQL.

### Actividades realizadas
- Creación de la base de datos agenda360.
- Instalación de SQLAlchemy.
- Instalación de psycopg2-binary.
- Instalación de python-dotenv.
- Creación del archivo .env.
- Configuración de variables de entorno.
- Creación del módulo de conexión a PostgreSQL.
- Prueba exitosa de conexión mediante endpoint /test-db.

### Resultado
La aplicación Agenda 360 quedó conectada correctamente a PostgreSQL mediante SQLAlchemy.

## 24/06/2026

### Objetivo
Implementar el primer modelo de negocio del sistema.

### Actividades realizadas
- Creación de la clase Base para SQLAlchemy.
- Creación del modelo User.
- Creación automática de la tabla users.
- Creación del esquema UserCreate.
- Creación de dependencias para la base de datos.
- Creación del endpoint POST /users.
- Validación de correos duplicados.
- Pruebas exitosas de inserción en PostgreSQL.

### Resultado
El sistema permite registrar usuarios y almacenarlos correctamente en la base de datos agenda360.

## 25/06/2026

### Objetivo
Continuar el desarrollo del módulo de usuarios y mejorar la seguridad de las respuestas de la API.

### Actividades realizadas
- Creación del endpoint GET /users.
- Consulta de usuarios almacenados en PostgreSQL.
- Verificación de funcionamiento mediante Swagger.
- Creación del esquema UserResponse.
- Implementación de respuesta segura para ocultar contraseñas.
- Aplicación de response_model en FastAPI.

### Resultado
El sistema permite listar usuarios registrados sin exponer información sensible como las contraseñas.

## 26/06/2026

### Objetivo
Ampliar el módulo de usuarios implementando la consulta de un usuario específico mediante su identificador.

### Actividades realizadas
- Implementación del endpoint GET /users/{id}.
- Consulta de un usuario por su ID utilizando SQLAlchemy.
- Implementación del manejo de errores mediante HTTPException.
- Respuesta con código HTTP 404 cuando el usuario no existe.
- Pruebas exitosas del endpoint desde Swagger para usuarios existentes e inexistentes.

### Resultado
El sistema permite consultar un usuario específico por su identificador y responde adecuadamente cuando el registro solicitado no existe, siguiendo buenas prácticas en el desarrollo de APIs REST.

## Fecha: 29/06/2026

### Objetivo
Finalizar el CRUD de usuarios implementando los endpoints de actualización y eliminación.

### Actividades realizadas
- Se creó el esquema `UserUpdate` para la actualización de usuarios.
- Se implementó el endpoint `PUT /users/{id}` para modificar la información de un usuario.
- Se implementó el endpoint `DELETE /users/{id}` para eliminar usuarios de la base de datos.
- Se corrigió la nomenclatura del atributo `nombre` para mantener consistencia entre el modelo y los esquemas.
- Se corrigió la ruta del endpoint `PUT`, eliminando la duplicación del prefijo `/users`.
- Se instaló la dependencia `email-validator` requerida por `EmailStr` de Pydantic.
- Se realizaron pruebas exitosas en Swagger para los endpoints `PUT` y `DELETE`, incluyendo casos exitosos y errores 404.

## Fecha: 30 de junio de 2026

### Actividades realizadas

- Se creó el módulo `security.py` para centralizar las funciones relacionadas con la seguridad de la aplicación.
- Se configuró el algoritmo `bcrypt` mediante `Passlib` para el manejo seguro de contraseñas.
- Se implementaron las funciones para generar hashes de contraseñas y verificar credenciales.
- Se instaló la librería `python-jose` como base para la futura implementación de autenticación mediante JWT.
- Se realizaron pruebas funcionales utilizando un endpoint temporal para validar el proceso de encriptación y verificación de contraseñas.
- Se identificó y solucionó una incompatibilidad entre `passlib` y `bcrypt` utilizando una versión estable compatible.
- Se actualizó el archivo `requirements.txt` con las nuevas dependencias del proyecto.

### Resultado

Quedó preparada la infraestructura inicial de seguridad que permitirá implementar el sistema de autenticación y autorización de Agenda 360 en las siguientes etapas del desarrollo.