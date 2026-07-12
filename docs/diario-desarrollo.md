## Sesión 22/06/2026

Se realizó la primera integración con PostgreSQL.

Se creó la base de datos agenda360 y se configuró la conexión usando variables de entorno para evitar almacenar credenciales directamente en el código fuente.

Se implementó un endpoint de prueba que permitió validar exitosamente la comunicación entre FastAPI y PostgreSQL.

Estado del proyecto: Backend conectado a base de datos y listo para comenzar la definición de modelos.

## Sesión 24/06/2026

Se implementó el primer modelo de negocio del sistema: Usuario.

Durante esta sesión se creó la estructura base para trabajar con SQLAlchemy, se construyó el modelo User, el esquema de validación UserCreate y el endpoint POST /users.

También se implementó una validación para evitar registros con correos duplicados y se realizaron pruebas exitosas de almacenamiento en PostgreSQL.

Estado del proyecto: Gestión básica de usuarios funcional.

## Sesión 25/06/2026

Durante esta sesión se completó la funcionalidad de consulta de usuarios registrados.

Se implementó el endpoint GET /users para recuperar información desde PostgreSQL y posteriormente se mejoró la seguridad mediante la creación del esquema UserResponse, evitando que las contraseñas sean enviadas en las respuestas de la API.

También se reforzó la organización del proyecto definiendo como regla trabajar Git desde la raíz del repositorio y FastAPI desde la carpeta backend.

Estado actual:
- Creación de usuarios funcional.
- Listado de usuarios funcional.
- Validación de correos duplicados funcional.
- Respuestas seguras implementadas.

## Sesión 26/06/2026

Durante esta sesión se implementó la funcionalidad para consultar un usuario específico mediante su identificador.

Se creó el endpoint GET /users/{id}, utilizando parámetros dinámicos en la URL para realizar consultas individuales a la base de datos. Además, se implementó el manejo de excepciones con HTTPException, permitiendo devolver un código HTTP 404 cuando el usuario solicitado no existe.

Con esta funcionalidad se reforzaron conceptos importantes como las rutas con parámetros, las consultas específicas mediante SQLAlchemy y el manejo adecuado de respuestas HTTP en una API REST.

Estado actual del módulo de usuarios:
- Creación de usuarios funcional.
- Listado de usuarios funcional.
- Consulta de usuario por ID funcional.
- Validación de correos duplicados implementada.
- Respuestas seguras sin exponer contraseñas.

## 29/06/2026

Durante esta sesión se completó el módulo CRUD de usuarios con la implementación de las operaciones de actualización y eliminación.

Durante las pruebas surgieron varios inconvenientes que fueron solucionados de manera progresiva. Inicialmente se detectó la ausencia de la librería `email-validator`, necesaria para utilizar el tipo `EmailStr` de Pydantic. Posteriormente se corrigió una inconsistencia entre los nombres de los atributos `name` y `nombre`, causada por la adaptación del proyecto al español. Finalmente se ajustó la definición de la ruta del endpoint `PUT`, evitando la duplicación del prefijo `/users`.

Con estas correcciones el CRUD quedó completamente funcional y probado mediante Swagger, validando tanto los casos exitosos como el manejo adecuado de errores cuando el usuario no existe.

Este módulo servirá como plantilla para el desarrollo de los próximos recursos del sistema.

## 30 de junio de 2026

La sesión estuvo enfocada en iniciar el módulo de seguridad del sistema. Antes de comenzar con la autenticación se construyó un componente independiente encargado de gestionar la encriptación de contraseñas.

Durante las pruebas apareció una incompatibilidad entre las versiones de `Passlib` y `bcrypt`, la cual fue analizada y corregida utilizando una versión compatible de la librería. Posteriormente se validó el correcto funcionamiento del algoritmo `bcrypt`, comprobando que una misma contraseña genera hashes diferentes en cada ejecución gracias al uso de un "salt" aleatorio, manteniendo siempre la posibilidad de verificar correctamente la contraseña original.

Con esta base, Agenda 360 ya cuenta con la infraestructura necesaria para comenzar la implementación del registro seguro de usuarios y la autenticación mediante JWT.

# Sesión de desarrollo - 01/07/2026

Durante esta sesión se completó la integración del sistema de autenticación mediante JWT dentro del backend de Agenda 360.

Inicialmente se adaptó el proceso de login para utilizar OAuth2PasswordRequestForm, permitiendo la integración nativa con Swagger UI. Posteriormente se instaló la dependencia python-multipart, necesaria para el procesamiento de formularios enviados durante la autenticación.

Una vez configurado el login, se realizaron pruebas utilizando el botón Authorize de Swagger, verificando la generación automática del token JWT y su almacenamiento temporal durante la sesión.

Finalmente se protegió el endpoint de listado de usuarios utilizando la dependencia obtener_usuario_actual, comprobando que únicamente los usuarios autenticados pueden acceder a la información. También se validó el comportamiento del sistema al cerrar sesión, verificando que el acceso a los recursos protegidos es rechazado cuando no existe un token válido.

Con esta implementación se concluye la primera etapa del sistema de seguridad del proyecto, dejando preparada la arquitectura para la incorporación de roles, permisos y control de acceso específico para cada tipo de usuario del sistema.

## 06/07/2026

Durante esta jornada se inició el desarrollo del módulo de Barberos, el cual constituye uno de los componentes principales del flujo operativo de Agenda 360. Se diseñó el modelo de datos estableciendo una relación uno a muchos entre barberías y barberos mediante el uso de claves foráneas y relaciones bidireccionales con SQLAlchemy.

Posteriormente se implementaron los esquemas necesarios para la creación, actualización y respuesta de la API, así como el primer endpoint encargado del registro de nuevos barberos. Como parte de las buenas prácticas de desarrollo, se incorporó una validación que verifica la existencia de la barbería antes de permitir el registro del barbero, garantizando así la consistencia de la información almacenada.

Durante las pruebas se presentó un inconveniente relacionado con la importación del esquema barber_schema.py, el cual fue identificado y solucionado. Finalmente se realizaron pruebas funcionales desde Swagger registrando exitosamente la primera barbería y su primer barbero, confirmando el correcto funcionamiento de la relación entre ambas entidades.

## Fecha: 07 de julio de 2026

## Objetivo de la sesión

Finalizar el desarrollo del CRUD del módulo Barberos, verificando el correcto funcionamiento de cada endpoint y consolidando este módulo como parte del MVP de Agenda 360.

## Desarrollo realizado

Durante esta jornada se implementaron los endpoints pendientes para la administración de barberos utilizando FastAPI y SQLAlchemy.

Se desarrollaron las operaciones de consulta general, consulta por identificador, actualización y eliminación de registros, reutilizando la estructura de trabajo implementada previamente en los módulos de Usuarios y Barberías.

Durante las pruebas se detectó un error generado por Pydantic relacionado con la definición del esquema BarberUpdate. Después de analizar el mensaje de error y revisar la estructura del proyecto, se identificó que el esquema no había sido importado dentro del archivo barber_api.py. Una vez corregido este detalle, la documentación de Swagger volvió a generarse correctamente y todas las pruebas fueron exitosas.

Finalmente se verificó el funcionamiento completo del CRUD mediante pruebas realizadas desde Swagger, comprobando tanto las respuestas exitosas como el manejo adecuado de errores cuando el recurso solicitado no existía.

## 12/07/2026

Durante esta sesión se desarrolló completamente el módulo Servicios, correspondiente a la gestión de los servicios ofrecidos por cada barbero.

Inicialmente se creó el modelo Service, definiendo los atributos necesarios para representar cada servicio y estableciendo la relación con el modelo Barber mediante SQLAlchemy. Posteriormente se registró el modelo dentro de la aplicación para permitir la creación automática de la tabla services en PostgreSQL.

Se implementaron los esquemas de validación utilizando Pydantic (ServiceCreate, ServiceUpdate y ServiceResponse), incorporando el esquema reutilizable BarberSimple con el objetivo de mantener una arquitectura limpia y reutilizable entre módulos.

A continuación se desarrolló el CRUD completo utilizando FastAPI, incluyendo las operaciones de creación, consulta, actualización y eliminación de servicios. Durante el desarrollo se validó previamente la existencia del barbero antes de registrar o actualizar un servicio, garantizando la integridad de la información.

Finalmente se realizaron pruebas completas desde Swagger, verificando el correcto funcionamiento de todos los endpoints. Como validación adicional se creó un segundo servicio únicamente para comprobar el funcionamiento del endpoint DELETE, eliminándolo posteriormente para dejar la base de datos organizada.

Con este avance quedó finalizado el cuarto módulo funcional del proyecto Agenda 360, consolidando la estructura principal sobre la cual se construirá el módulo de horarios y posteriormente el sistema de agendamiento inteligente mediante WhatsApp.
