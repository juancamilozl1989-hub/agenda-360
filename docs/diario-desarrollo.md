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

## 13/07/2026

Durante esta sesión se desarrolló completamente el módulo Horarios, encargado de administrar la disponibilidad laboral de los barberos.

Se inició creando el modelo Schedule, utilizando el tipo de dato Time para representar correctamente las horas de inicio y finalización de la jornada laboral. Posteriormente se estableció la relación entre los modelos Barber y Schedule, permitiendo que un barbero pueda tener múltiples horarios registrados.

Después se implementaron los esquemas de validación utilizando Pydantic y se desarrolló el CRUD completo mediante FastAPI. Las operaciones incluyen la creación, consulta, actualización y eliminación de horarios, verificando previamente la existencia del barbero para garantizar la integridad de los datos.

Finalmente se realizaron pruebas completas desde Swagger, comprobando el funcionamiento de todos los endpoints. Como parte de las pruebas se creó un horario adicional para validar el endpoint DELETE y posteriormente se eliminó, dejando únicamente los horarios necesarios para continuar el desarrollo del proyecto.

Con este avance Agenda 360 cuenta ahora con cinco módulos completamente funcionales, consolidando la estructura necesaria para iniciar el desarrollo de los módulos de Clientes y Citas, que serán la base del sistema de agendamiento inteligente.

## 14 de julio de 2026

Durante esta sesión se desarrolló completamente el módulo Clientes, encargado de administrar la información de los clientes pertenecientes a cada barbería.

Se inició con la creación del modelo Client, estableciendo la relación con Barbershop mediante SQLAlchemy para garantizar que cada cliente pertenezca a una barbería registrada. Posteriormente se implementaron los esquemas de validación utilizando Pydantic y se desarrolló el CRUD completo mediante FastAPI.

Las operaciones implementadas permiten registrar, consultar, actualizar y eliminar clientes, validando previamente la existencia de la barbería para mantener la integridad de la información.

Finalmente se realizaron pruebas funcionales desde Swagger para comprobar el correcto funcionamiento de todos los endpoints. Como parte de las pruebas se creó un segundo cliente para validar el endpoint DELETE y posteriormente se eliminó, dejando únicamente el registro principal para continuar con el desarrollo del proyecto.

Con este avance, Agenda 360 cuenta ya con seis módulos completamente funcionales, consolidando la estructura principal del backend y dejando preparado el entorno para iniciar el desarrollo del módulo de Citas (Appointments), el componente central del sistema de agendamiento.

## 15/07/2026

Durante esta sesión se desarrolló completamente el módulo Citas, considerado el componente central del sistema Agenda 360.

Se inició con la creación del modelo Appointment, estableciendo relaciones con los módulos de Clientes, Barberos y Servicios. Posteriormente se implementaron los esquemas de validación mediante Pydantic y el CRUD completo utilizando FastAPI.

Durante el desarrollo también se resolvió un inconveniente relacionado con el entorno de desarrollo en Visual Studio Code, donde el analizador utilizaba un intérprete de Python diferente al entorno virtual del proyecto. Tras configurar correctamente el intérprete del venv, desaparecieron las advertencias y el proyecto continuó funcionando con normalidad.

Se realizaron pruebas funcionales desde Swagger verificando la creación, consulta, actualización y eliminación de citas. Como parte de las pruebas se creó una segunda cita para validar el endpoint DELETE y posteriormente se eliminó, conservando únicamente la cita principal.

Con este avance, Agenda 360 dispone de todos los módulos fundamentales del backend y ya puede gestionar el flujo principal de reservas entre clientes, barberos y servicios.

# Diario de Desarrollo

## Fecha

20 de julio de 2026

## Objetivo de la sesión

Fortalecer el módulo de citas implementando reglas de negocio para garantizar la consistencia de la información durante la creación y actualización de citas.

## Actividades realizadas

- Implementación de validación para impedir citas con fechas pasadas.
- Validación de correspondencia entre servicio y barbero.
- Validación para impedir citas duplicadas en la misma fecha y hora.
- Implementación de un Enum para controlar los estados permitidos de las citas.
- Replicación de todas las validaciones en el endpoint PUT.
- Ejecución de pruebas funcionales utilizando Swagger.
- Verificación del correcto funcionamiento de todas las reglas implementadas.

## Resultado

El módulo de citas quedó completamente validado para las operaciones de creación y actualización, reduciendo la posibilidad de inconsistencias en la base de datos.

## Próximos pasos

- Revisar nuevas reglas de negocio para fortalecer el sistema.
- Refactorizar la lógica de negocio hacia una arquitectura más modular.
- Implementar autenticación mediante JWT y control de acceso por roles.

# Diario de Desarrollo

## 21 de julio de 2026

Durante esta sesión se dio inicio al proceso de refactorización del backend con el objetivo de implementar una arquitectura por capas.

Se creó el archivo `appointment_service.py`, donde se trasladó la lógica de negocio correspondiente a la creación de citas. Posteriormente, el endpoint `POST /appointments` fue modificado para consumir dicha capa de servicios, reduciendo considerablemente la responsabilidad del router.

Después de realizar la refactorización se ejecutaron diferentes pruebas funcionales desde Swagger, verificando tanto la creación correcta de citas como las validaciones implementadas previamente. Los resultados confirmaron que el comportamiento del sistema se mantiene intacto.

También se definió la estrategia para la siguiente fase del proyecto, la cual consistirá en implementar la capa Repository con el fin de separar completamente el acceso a la base de datos de la lógica de negocio.

Esta evolución permitirá que Agenda 360 adopte una arquitectura más limpia, escalable y fácil de mantener antes de comenzar el desarrollo del frontend.

## Fecha: 23/07/2026

Durante esta sesión se dio inicio al desarrollo del frontend del proyecto Agenda 360. Se configuró el entorno de trabajo utilizando React con TypeScript y se instalaron las dependencias necesarias para la construcción de la interfaz de usuario.

Posteriormente se organizó la estructura de carpetas del proyecto siguiendo una arquitectura escalable que facilitará el crecimiento de la aplicación.

También se creó una primera versión de la pantalla principal, reemplazando la plantilla predeterminada de Vite por una vista personalizada con la identidad del proyecto.

Finalmente se revisó el material gráfico real de la Barbería Juanda, el cual servirá como referencia para mantener una línea visual consistente durante todo el desarrollo del sistema.

## 24 de julio de 2026

Durante esta jornada se continuó el desarrollo del frontend de Agenda 360.

Inicialmente se realizaron mejoras visuales sobre la pantalla de autenticación, incorporando una distribución moderna de dos paneles, una imagen representativa del entorno de barbería y una identidad visual basada en tonos negros y dorados.

Posteriormente se desarrolló el primer componente reutilizable del proyecto denominado `CustomTextField`, cuyo objetivo es centralizar la configuración visual de todos los campos de entrada que utilizará la aplicación.

Durante el proceso se identificaron y solucionaron incompatibilidades derivadas de la integración entre React 19, Material UI 7 y TypeScript 6, relacionadas principalmente con el tipado de las propiedades del componente `TextField`. Finalmente se adaptó el componente utilizando una definición de tipos compatible con la versión actual del entorno de desarrollo.

Con esta implementación se establece una base reutilizable para los formularios de Clientes, Barberos, Servicios, Citas y Usuarios, reduciendo la duplicación de código y facilitando el mantenimiento del proyecto.

# Diario - 27/07/2026

Hoy se trabajó en la construcción del Dashboard principal del sistema Agenda 360.

Se implementó una arquitectura basada en componentes reutilizables utilizando React, TypeScript y Material UI.

Durante el desarrollo se realizaron ajustes en la organización del proyecto, separando correctamente layouts, páginas y componentes.

Se construyeron los siguientes elementos:

- Sidebar
- Header
- DashboardLayout
- DashboardPage
- StatCard
- WeeklyIncomeChart
- UpcomingAppointments
- TopServices

El Dashboard ya presenta una apariencia muy cercana a un sistema comercial real.

También se dejó preparada la estructura para comenzar el módulo Agenda en la siguiente sesión.

# Diario de desarrollo - 28/07/2026

## Objetivo

Comenzar la construcción del módulo Agenda siguiendo una arquitectura modular y reutilizable.

## Desarrollo realizado

Durante esta sesión se diseñó la estructura inicial del módulo Agenda.

Se desarrolló el componente `AppointmentCard`, encargado de representar visualmente cada cita mediante una tarjeta con la información del cliente, servicio, barbero y estado.

Posteriormente se creó el componente `AppointmentStatus`, con el propósito de centralizar la representación visual de los estados de las citas (Confirmada, Pendiente y Finalizada), facilitando el mantenimiento del código.

También se implementó el componente `TimeLine`, encargado de renderizar múltiples citas reutilizando `AppointmentCard`.

Finalmente se integró la Agenda dentro de `AgendaPage`, incorporando un encabezado, pestañas de navegación y el botón para crear nuevas citas.

## Resultado

Se obtuvo la primera versión funcional del módulo Agenda con una arquitectura basada en componentes reutilizables, preparada para evolucionar hacia una agenda profesional y para integrarse posteriormente con FastAPI y PostgreSQL.

## Próxima sesión

- Configurar React Router de forma profesional.
- Implementar navegación entre módulos.
- Conectar Sidebar con las rutas.
- Preparar la estructura para autenticación mediante login.

## Día de desarrollo 29/07/2026

## Durante esta sesión se consolidó la arquitectura del Frontend de Agenda 360.

El proyecto dejó de utilizar páginas individuales renderizadas directamente y pasó a implementar una navegación profesional mediante React Router.

Se construyeron componentes reutilizables (PageHeader y DataTable) que permitirán reducir considerablemente la duplicación de código en los módulos de Clientes, Barberos, Servicios y Reportes.

También se implementó un Sidebar completamente funcional con navegación dinámica y detección automática de la ruta activa, mejorando la experiencia de usuario.

El módulo de Clientes quedó preparado para evolucionar posteriormente hacia un CRUD conectado con FastAPI y PostgreSQL.

## Día de desarrollo 02/08/2026

## Durante esta sesión se finalizó el módulo de Clientes del sistema Agenda 360.

Se implementó un CRUD completo con operaciones de crear, editar y eliminar registros, utilizando un único formulario reutilizable para las operaciones de creación y edición.

Se desarrollaron dos componentes reutilizables (AppSnackbar y ConfirmDialog), los cuales serán utilizados en todos los módulos del proyecto para mantener una interfaz consistente.

Finalmente se incorporó una búsqueda dinámica en tiempo real, permitiendo filtrar clientes por nombre, teléfono o correo electrónico.

El módulo quedó preparado para ser conectado posteriormente al backend desarrollado en FastAPI.

## Día de desarrollo 03/08/2026

## Durante esta sesión se desarrollaron completamente los módulos de Barberos y Servicios.

Se reutilizaron los componentes creados anteriormente (DataTable, ConfirmDialog, AppSnackbar y PageHeader), permitiendo mantener una arquitectura consistente y reducir la duplicación de código.

Los módulos implementan operaciones CRUD completas, búsqueda dinámica y notificaciones visuales, dejando preparada la aplicación para la siguiente fase de integración con el backend desarrollado en FastAPI y PostgreSQL.

## Fecha: 04/08/2026

Durante esta sesión se realizó una revisión detallada de la arquitectura actual del backend del proyecto Agenda 360. Inicialmente se identificó que gran parte de la estructura ya se encontraba implementada, incluyendo modelos, esquemas y endpoints para diferentes módulos del sistema.

A partir de este análisis se decidió cambiar la metodología de desarrollo, dejando de crear componentes nuevos para enfocarse en mantener y completar la arquitectura existente.

Se actualizaron los módulos de Clientes, Barberos y Servicios, agregando los nuevos atributos definidos durante el diseño funcional del sistema, tales como estado, especialidad y categoría. Estos cambios fueron aplicados de manera consistente en los modelos, los esquemas de validación y los endpoints de FastAPI.

Al finalizar la jornada, el backend quedó completamente sincronizado para estos tres módulos, permitiendo continuar el desarrollo sobre una base sólida y organizada.

Como siguiente objetivo se estableció la revisión de los módulos de Horarios y Citas, para posteriormente iniciar la integración del frontend desarrollado en React con la API de FastAPI y la base de datos PostgreSQL.

## 13 de agosto de 2026

Se continuó con el desarrollo del backend de Agenda-360. Se terminó la implementación del módulo de servicios y se realizaron las pruebas correspondientes en Swagger.

Durante las pruebas se encontraron algunos campos que faltaban en las tablas de PostgreSQL, los cuales fueron agregados desde pgAdmin. Después de realizar las correcciones, los endpoints funcionaron correctamente.

Finalmente se guardaron los cambios en Git y se realizó el push al repositorio de GitHub.

Estado: Módulo de servicios terminado y funcionando correctamente.

## Día de desarrollo 14/09/2026

Durante esta sesión el enfoque estuvo en cerrar brechas de seguridad del backend antes de avanzar con la integración del frontend. Se identificó que la clave secreta usada para firmar los tokens JWT estaba escrita directamente en el código, y que la mayoría de los endpoints de gestión no exigían autenticación, permitiendo que cualquier persona pudiera consultarlos o modificarlos sin haber iniciado sesión.

Se corrigió trasladando la clave a una variable de entorno y añadiendo la dependencia de autenticación a los routers de barberías, barberos, servicios, horarios, clientes y citas, dejando accesibles sin token únicamente las rutas de registro y login.

Con el backend ya protegido, se avanzó en conectar el frontend a la API real. Se construyó un cliente HTTP centralizado con axios, un contexto de autenticación para manejar la sesión en toda la aplicación, y un componente de ruta privada que impide entrar directamente a las páginas internas sin haber iniciado sesión.

La página de Login, que hasta ahora era solo una maqueta visual, pasó a estar completamente conectada: valida los campos, llama al backend, muestra un mensaje si las credenciales son incorrectas y redirige al Dashboard cuando el ingreso es exitoso. También se añadió un botón para cerrar sesión y se actualizó el Sidebar para mostrar el correo real del usuario autenticado en lugar de un nombre fijo de prueba.

Durante las pruebas surgieron algunos inconvenientes propios de la integración: una carpeta con un nombre distinto al esperado en las importaciones, ausencia de configuración CORS en el backend (lo que bloqueaba las peticiones del navegador) y un archivo de variables de entorno del frontend que no llegó a crearse correctamente. Cada uno se fue diagnosticando y corrigiendo de forma independiente hasta lograr el flujo completo de inicio de sesión funcionando de extremo a extremo.

## Resultado

Agenda 360 cuenta ahora con un flujo de autenticación real y funcional entre el frontend y el backend, con las rutas protegidas correctamente y una base de seguridad sólida para continuar el desarrollo.

## Próxima sesión

- Conectar los módulos de Clientes, Barberos, Servicios y Agenda con la información real del backend.
- Comenzar el diseño de la integración con la API de WhatsApp Business.

## Día de desarrollo 16/10/2026

Esta fue una jornada larga de integración. El objetivo era que el panel dejara de mostrar datos de ejemplo y trabajara con la base de datos real, así que cada módulo pasó a tener su propio servicio de API en el frontend y una forma común de mostrar los errores que devuelve FastAPI. Clientes, Barberos, Servicios, Agenda y el Dashboard quedaron leyendo y guardando en PostgreSQL, y la sección de Reportes, que estaba marcada como fuera de servicio, por fin quedó funcionando con indicadores reales.

En paralelo se armaron las pruebas automatizadas con pytest. Para poder importar la aplicación sin tener PostgreSQL encendido hubo que mover la creación de tablas a un evento de arranque. Las pruebas ayudaron a encontrar un error de lógica que no se veía a simple vista: una cita cancelada seguía bloqueando la hora del barbero.

Al ejecutar todo en mi equipo aparecieron problemas que en las pruebas no salían. El panel decía que no se podía conectar con el servidor aunque uvicorn respondía 200; era el navegador bloqueando las respuestas por CORS. Se resolvió con un proxy en Vite, de modo que el frontend llama a `/api` y Vite reenvía al backend. Después la agenda no cargaba porque la tabla de clientes, creada en fases anteriores, no tenía la columna `estado`: `create_all` crea tablas, pero no agrega columnas a las que ya existen. Para no tener que corregir esto a mano desde pgAdmin cada vez, el backend ahora revisa al arrancar y agrega las columnas que falten. También noté que el sistema me dejó crear una cita para las 9 de la mañana cuando ya eran casi las 11 de la noche, así que se agregó la validación de la hora.

## Día de desarrollo 17/10/2026

Probando la creación de citas me di cuenta de que el diseño no se ajustaba a la idea del proyecto. Cada servicio estaba amarrado a un barbero, entonces al elegir un barbero solo aparecía un servicio y el cliente no podía escoger con quién atenderse. Además, la agenda no tenía en cuenta los horarios de los barberos ni cuánto dura cada servicio: solo rechazaba una cita si era exactamente a la misma hora.

Pensando en el bot de WhatsApp, donde es el cliente quien elige el día y la hora según la disponibilidad, se replanteó esa parte. Los servicios ahora son el catálogo de la barbería, la agenda solo acepta citas dentro del horario del barbero y compara las citas como intervalos de tiempo según la duración del servicio. Se creó la consulta de disponibilidad (`GET /availability/`), que será la base del bot, y en el panel se agregó la pantalla de Horarios y un selector que solo ofrece horas libres.

Todo quedó probado: 112 pruebas aprobadas en SQLite y en PostgreSQL. Con estos cambios se actualizó el informe de la Fase 3, rehaciendo los diagramas y las capturas para que coincidan con lo que realmente está construido.

## Día de desarrollo 21/10/2026

Hoy se construyó el bot de WhatsApp. Usé la Cloud API de Meta con el número de prueba que da la plataforma y ngrok para que Meta pudiera llegar al backend que corre en mi equipo. El bot no tiene reglas propias: llama a las mismas funciones de disponibilidad y de creación de citas del panel, así que lo que no se puede agendar en el panel tampoco se puede por WhatsApp.

La conexión costó más que el código. Meta verificaba el webhook, pero los mensajes nunca llegaban; faltaba suscribir la aplicación a la cuenta de WhatsApp Business, y para no repetirlo a mano quedó un script. Luego el bot dejó de responder de un momento a otro: el token temporal de Meta vence a las 24 horas, hay que cambiarlo en el `.env` y reiniciar uvicorn.

Al probar desde el celular salieron detalles de uso. Con un barbero que solo atiende los martes, el bot ofrecía días en los que no había nada y tocaba probar uno por uno; ahora solo muestra los días con espacio. Las horas de la tarde no se podían elegir porque la lista se cortaba en 12; se agregó «Ver más horas». Y en el panel, una cita del mes siguiente no aparecía en ninguna pestaña de la agenda, así que se agregó «Próximas».

Quedaron 149 pruebas aprobadas en SQLite y PostgreSQL, y se actualizó el informe con la sección del bot y las capturas de la conversación.

## Próxima sesión

- Token permanente de Meta y despliegue con HTTPS.
- Recordatorios de citas con plantillas de WhatsApp.
