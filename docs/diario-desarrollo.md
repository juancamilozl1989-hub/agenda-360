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