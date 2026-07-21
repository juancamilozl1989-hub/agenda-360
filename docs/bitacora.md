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

## Sesión de desarrollo – Módulo de Servicios

## Fecha: 12 de julio de 2026

## Objetivo de la sesión

Desarrollar el módulo Servicios, permitiendo registrar los servicios que ofrece cada barbero, establecer la relación entre barberos y servicios, implementar el CRUD completo mediante FastAPI y verificar su correcto funcionamiento desde Swagger.

Actividades realizadas
Se creó el modelo Service con los campos correspondientes:
nombre
descripción
precio
duración
barber_id
Se estableció la relación entre Barber y Service utilizando SQLAlchemy.
Se registró el nuevo modelo para crear automáticamente la tabla services en PostgreSQL.
Se desarrollaron los esquemas (ServiceCreate, ServiceUpdate y ServiceResponse) utilizando Pydantic.
Se creó el esquema reutilizable BarberSimple para evitar duplicación de código entre módulos.
Se implementó el CRUD completo del módulo Servicios:
Crear servicio
Consultar todos los servicios
Consultar un servicio por ID
Actualizar un servicio
Eliminar un servicio
Se registró el router del módulo en main.py.
Se realizaron pruebas funcionales desde Swagger para validar todos los endpoints.
Se verificó el correcto funcionamiento de las relaciones entre Barberías, Barberos y Servicios.
Se realizaron pruebas adicionales creando y eliminando registros para validar el correcto comportamiento del CRUD.

## Resultado de la sesión

El módulo Servicios quedó completamente funcional y conectado con el módulo de Barberos. Se confirmó el correcto funcionamiento de las relaciones ORM, la persistencia de datos en PostgreSQL y la validación de los endpoints mediante Swagger.

## Sesión de desarrollo – Módulo de Horarios

## Fecha: 13 de julio de 2026

## Objetivo de la sesión

Desarrollar el módulo Horarios, permitiendo registrar la disponibilidad laboral de cada barbero, establecer la relación entre barberos y horarios, implementar el CRUD completo mediante FastAPI y validar su funcionamiento desde Swagger.

Actividades realizadas
Se creó el modelo Schedule con los campos:
día de la semana
hora de inicio
hora de finalización
barber_id
Se implementó el tipo de dato Time para almacenar correctamente las horas de trabajo.
Se estableció la relación entre Barber y Schedule mediante SQLAlchemy.
Se registró el modelo para crear automáticamente la tabla schedules en PostgreSQL.
Se desarrollaron los esquemas ScheduleCreate, ScheduleUpdate y ScheduleResponse.
Se implementó el CRUD completo del módulo Horarios:
Crear horario
Consultar todos los horarios
Consultar un horario por ID
Actualizar un horario
Eliminar un horario
Se registró el router del módulo en main.py.
Se realizaron pruebas funcionales desde Swagger para validar todos los endpoints.
Se verificó la correcta relación entre Barberos y Horarios.
Se realizaron pruebas adicionales creando y eliminando registros para validar el funcionamiento del endpoint DELETE.
Resultado de la sesión

El módulo Horarios quedó completamente funcional y conectado con el módulo de Barberos. Se validó el almacenamiento de horas mediante el tipo Time, el correcto funcionamiento de las relaciones ORM y la persistencia de la información en PostgreSQL.

## Sesión de desarrollo – Módulo de Clientes

## Fecha: 14 de julio de 2026

## Objetivo de la sesión

Desarrollar el módulo Clientes, permitiendo registrar los clientes pertenecientes a una barbería, implementar la relación con el módulo de Barberías y construir el CRUD completo utilizando FastAPI y PostgreSQL.

Actividades realizadas
Se creó el modelo Client con los campos:
nombre
teléfono
correo electrónico
barbershop_id
Se estableció la relación entre Client y Barbershop mediante SQLAlchemy.
Se actualizó el modelo Barbershop para incluir la relación con los clientes.
Se registró el modelo para generar automáticamente la tabla clients en PostgreSQL.
Se desarrollaron los esquemas ClientCreate, ClientUpdate y ClientResponse.
Se implementó el CRUD completo del módulo Clientes:
Crear cliente
Consultar todos los clientes
Consultar un cliente por ID
Actualizar cliente
Eliminar cliente
Se registró el router correspondiente en main.py.
Se realizaron pruebas funcionales desde Swagger para validar todos los endpoints.
Se verificó la correcta relación entre Clientes y Barberías.
Se realizaron pruebas adicionales creando y eliminando un segundo cliente para validar el funcionamiento del endpoint DELETE.
Resultado de la sesión

El módulo Clientes quedó completamente funcional e integrado con el módulo de Barberías. Se verificó el correcto funcionamiento de las relaciones ORM, la persistencia de los datos en PostgreSQL y la ejecución satisfactoria de todas las operaciones CRUD.

## Sesión de desarrollo – Módulo de Citas

## Fecha: 15 de julio de 2026

## Objetivo de la sesión

Desarrollar el módulo Citas, encargado de registrar reservas entre clientes, barberos y servicios, implementando las relaciones necesarias y el CRUD completo utilizando FastAPI y PostgreSQL.

Actividades realizadas
Se creó el modelo Appointment.
Se definieron los campos:
fecha
hora
estado
client_id
barber_id
service_id
Se establecieron las relaciones ORM entre:
Appointment y Client.
Appointment y Barber.
Appointment y Service.
Se actualizaron los modelos relacionados para incluir la colección de citas.
Se registró el modelo para generar automáticamente la tabla appointments.
Se desarrollaron los esquemas:
AppointmentCreate
AppointmentUpdate
AppointmentResponse
Se implementó el CRUD completo del módulo Citas:
Crear cita.
Consultar todas las citas.
Consultar una cita por ID.
Actualizar cita.
Eliminar cita.
Se realizaron validaciones para comprobar la existencia del cliente, barbero y servicio antes de registrar o actualizar una cita.
Se registró el router correspondiente en main.py.
Se realizaron pruebas funcionales desde Swagger para validar todos los endpoints.
Se resolvió un inconveniente en VS Code relacionado con el intérprete de Python, configurando correctamente el entorno virtual (venv).
Resultado de la sesión

El módulo Citas quedó completamente funcional, consolidando la estructura principal del backend. El sistema ya puede registrar reservas reales relacionando correctamente clientes, barberos y servicios mediante SQLAlchemy y PostgreSQL.

## 20 de julio de 2026

### Módulo de Citas

Se fortaleció la lógica de negocio del módulo de citas implementando nuevas validaciones tanto para la creación (POST) como para la actualización (PUT) de registros.

### Validaciones implementadas

- Se impide registrar o actualizar citas con fechas anteriores a la fecha actual.
- Se valida que el servicio seleccionado pertenezca al barbero asignado a la cita.
- Se evita que un mismo barbero tenga dos citas programadas para la misma fecha y hora.
- Se incorporó un Enum (`AppointmentStatus`) para restringir los estados permitidos de una cita a: Pendiente, Confirmada, Cancelada y Completada.

### Pruebas realizadas

Se verificó correctamente:

- Creación de citas válidas.
- Rechazo de citas con fechas pasadas.
- Rechazo de servicios asociados a otro barbero.
- Rechazo de citas duplicadas.
- Validación del Enum mediante Swagger.
- Actualización de citas respetando todas las reglas de negocio.

### Resultado

El módulo de citas quedó protegido contra las principales inconsistencias de negocio tanto en el endpoint de creación como en el de actualización.

## Fecha: 21 de julio de 2026

### Actividades realizadas

- Se inició la implementación de la capa de servicios (Services) para el módulo de citas.
- Se creó el archivo `appointment_service.py`.
- Se trasladó la lógica del endpoint `POST /appointments` desde el router hacia la capa de servicios.
- Se verificó el correcto funcionamiento del endpoint mediante pruebas en Swagger.
- Se confirmó que las validaciones de negocio continúan funcionando correctamente después de la refactorización:
  - No permitir citas en fechas pasadas.
  - Validación de cliente existente.
  - Validación de barbero existente.
  - Validación de servicio existente.
  - Validación de correspondencia entre servicio y barbero.
  - Prevención de citas duplicadas.
- Se definió la estrategia de refactorización para continuar separando la lógica de negocio del acceso a datos mediante la futura implementación de la capa Repository.

### Estado del proyecto

La primera migración hacia una arquitectura por capas fue exitosa. El endpoint de creación de citas ya utiliza la nueva capa de servicios sin afectar el funcionamiento del sistema.

### Próximas actividades

- Crear la capa Repository para el módulo de citas.
- Refactorizar el resto del CRUD de citas utilizando Services y Repositories.
- Preparar el backend para iniciar el desarrollo del frontend.