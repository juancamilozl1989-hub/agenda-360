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