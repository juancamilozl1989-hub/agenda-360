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

## 01/07/2026

### Actividades realizadas

- Se integró completamente el sistema de autenticación mediante JWT.
- Se implementó el endpoint de login utilizando OAuth2PasswordRequestForm.
- Se configuró Swagger UI para autenticarse mediante el botón Authorize.
- Se protegió el endpoint de listado de usuarios utilizando Depends(obtener_usuario_actual).
- Se realizaron pruebas de autenticación y autorización verificando el acceso únicamente con un token válido.
- Se instaló la dependencia python-multipart requerida por OAuth2.
- Se verificó el correcto funcionamiento del flujo completo de autenticación desde Swagger.

### Resultado

Agenda 360 cuenta ahora con un sistema de autenticación basado en JWT completamente funcional, permitiendo proteger los endpoints de la API y sentando las bases para la implementación futura de roles y permisos.

## 06/07/2026

## Actividades realizadas

- Se creó el modelo Barber para representar los barberos de cada establecimiento.
- Se implementó la relación uno a muchos entre las entidades Barbershop y Barber utilizando ForeignKey, relationship() y back_populates.
- Se configuró la eliminación en cascada (cascade="all, delete") para mantener la integridad de los datos.
- Se registró el nuevo modelo en SQLAlchemy y se verificó la creación de la tabla barbers en PostgreSQL.
- Se desarrollaron los esquemas BarberCreate, BarberUpdate y BarberResponse.
- Se implementó el primer endpoint para registrar barberos.
- Se agregó una validación para impedir el registro de barberos asociados a barberías inexistentes.
- Se registró el router del nuevo módulo dentro de la aplicación.
-Se realizaron pruebas exitosas desde Swagger creando la primera barbería y el primer barbero asociados correctamente.

## 07 de julio de 2026

## Actividad realizada

Durante esta sesión se continuó con el desarrollo del módulo Barberos dentro del proyecto Agenda 360 SIC. Se implementó el CRUD completo para la gestión de barberos utilizando FastAPI, SQLAlchemy y PostgreSQL.

Se desarrollaron los siguientes endpoints:

Listar todos los barberos (GET /barbers/).
Consultar un barbero por su identificador (GET /barbers/{id}).
Actualizar la información de un barbero (PUT /barbers/{id}).
Eliminar un barbero (DELETE /barbers/{id}).

Durante el desarrollo se presentó un error relacionado con Pydantic (class-not-fully-defined), ocasionado por la ausencia de la importación del esquema BarberUpdate. Se realizó el proceso de análisis del error, se identificó la causa y se corrigió la importación correspondiente, permitiendo nuevamente la generación de la documentación OpenAPI y el funcionamiento correcto de la aplicación.

Posteriormente se realizaron pruebas funcionales desde Swagger verificando el correcto comportamiento de cada uno de los endpoints implementados, validando tanto los casos exitosos como las respuestas ante registros inexistentes.

## Resultado

El módulo Barberos quedó completamente funcional, con operaciones de creación, consulta, actualización y eliminación correctamente implementadas y verificadas sobre la base de datos PostgreSQL