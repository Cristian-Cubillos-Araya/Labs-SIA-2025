# Laboratorio de Sistemas de Información: Sistema de Gestión de Inventario

Este laboratorio consiste en una aplicación web simple desarrollada con Python y Flask para la gestión de inventario. La aplicación permite realizar operaciones básicas CRUD (Crear, Leer, Actualizar, Eliminar) sobre productos en un inventario.

## Objetivos de Aprendizaje

- Comprender los conceptos básicos de Sistemas de Información
- Familiarizarse con el desarrollo de aplicaciones web utilizando Flask
- Entender el patrón de arquitectura MVC (Modelo-Vista-Controlador)
- Aprender sobre almacenamiento y persistencia de datos
- Analizar aspectos de seguridad, escalabilidad y mantenimiento de sistemas

## Requisitos Previos

- Python 3.6 o superior
- Conocimientos básicos de HTML, CSS y JavaScript
- Familiaridad con conceptos de programación web

## Estructura del Proyecto

```
/
├── app.py                     # Aplicación principal de Flask
├── inventario.json            # Archivo de almacenamiento de datos (se crea automáticamente)
├── static/                    # Archivos estáticos
│   └── css/
│       └── styles.css         # Estilos personalizados
├── templates/                 # Plantillas HTML
│   ├── index.html             # Página principal (lista de productos)
│   ├── agregar.html           # Formulario para agregar productos
│   └── editar.html            # Formulario para editar productos
├── preguntas_laboratorio.md   # Preguntas relacionadas con el laboratorio
├── respuestas_laboratorio.md  # Respuestas a las preguntas del laboratorio
├── requirements.txt           # Dependencias del proyecto
├── Dockerfile                 # Configuración para crear la imagen Docker
├── docker-compose.yml         # Configuración para orquestar contenedores
└── README.md                  # Este archivo
```

## Instalación

### Opción 1: Instalación Local

1. Clona o descarga este repositorio en tu máquina local

2. Crea un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   ```

3. Activa el entorno virtual:

   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

### Opción 2: Instalación con Docker

1. Asegúrate de tener Docker y Docker Compose instalados en tu sistema

2. Clona o descarga este repositorio en tu máquina local

## Ejecución

### Opción 1: Ejecución Local

1. Ejecuta la aplicación:

   ```bash
   python app.py
   ```

2. Abre tu navegador y visita [http://localhost:5000](http://localhost:5000)

### Opción 2: Ejecución con Docker

1. Construye y ejecuta el contenedor con Docker Compose:

   ```bash
   docker-compose up
   ```

   O para ejecutarlo en segundo plano:

   ```bash
   docker-compose up -d
   ```

2. Abre tu navegador y visita [http://localhost:5000](http://localhost:5000)

3. Para detener el contenedor:

   ```bash
   docker-compose down
   ```

## Funcionalidades

- **Ver Inventario**: La página principal muestra todos los productos en el inventario
- **Agregar Producto**: Permite añadir nuevos productos al inventario
- **Editar Producto**: Permite modificar la información de productos existentes
- **Eliminar Producto**: Permite eliminar productos del inventario

## Actividades del Laboratorio

1. **Exploración de la Aplicación**:
   - Ejecuta la aplicación y familiarízate con su funcionamiento
   - Añade, edita y elimina algunos productos de prueba

2. **Análisis del Código**:
   - Revisa el código fuente de la aplicación
   - Identifica los componentes del patrón MVC
   - Comprende cómo se manejan los datos y las solicitudes

3. **Respuesta a Preguntas**:
   - Revisa el archivo `preguntas_laboratorio.md`
   - Responde a las preguntas basándote en tu análisis y comprensión
   - Compara tus respuestas con las proporcionadas en `respuestas_laboratorio.md`

4. **Mejoras Opcionales**:
   - Implementa autenticación de usuarios
   - Añade categorías a los productos
   - Implementa búsqueda y filtrado
   - Mejora la interfaz de usuario
   - Migra el almacenamiento a una base de datos SQL

## Recursos Adicionales

- [Documentación oficial de Flask](https://flask.palletsprojects.com/)
- [Tutorial de Flask](https://flask.palletsprojects.com/en/2.0.x/tutorial/)
- [Documentación de Bootstrap](https://getbootstrap.com/docs/5.0/getting-started/introduction/)
- [Fundamentos de Sistemas de Información](https://www.tutorialspoint.com/management_information_system/index.htm)

## Notas

- Esta aplicación es solo para fines educativos y no debe utilizarse en un entorno de producción sin implementar medidas de seguridad adecuadas
- El almacenamiento en archivos JSON es simple pero no adecuado para aplicaciones reales con múltiples usuarios o grandes volúmenes de datos