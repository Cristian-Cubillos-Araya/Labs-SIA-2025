**Laboratorio: Sistema de Procesamiento de Transacciones (TPS)**

**Objetivos de Aprendizaje**
- Comprender el propósito y alcance de un TPS en organizaciones.
- Identificar y describir los componentes clave: entrada, procesamiento, almacenamiento, salida y retroalimentación.
- Analizar casos reales y modelar transacciones de negocio (ventas, reservas).
- Diseñar y construir un mini TPS funcional con énfasis en integridad y consistencia.
- Diferenciar TPS de otros sistemas (MIS, DSS, ESS) y su rol en el ecosistema SI.
- Elaborar un informe técnico con hallazgos, decisiones de diseño y conclusiones.

**Duración y Materiales Necesarios**
- Duración: 2 semanas
- Materiales: computador con internet, editor (VS Code), `Python 3.x`, `SQLite` o DB embebida; alternativa: formulario web simple (HTML/JS) o microservicio (Flask/Node) para registrar transacciones.
- Herramientas de apoyo: `sqlite3` CLI, Postman/Thunder Client (opcional), navegador web, diagramas (Draw.io/Lucidchart).

**Marco Teórico Breve**
- Definición: Un TPS (Transaction Processing System) captura, valida, procesa y persiste transacciones operacionales recurrentes (ventas, pagos, reservas) asegurando integridad, consistencia y disponibilidad.
- Propósito: Automatizar operaciones, reducir errores, proveer trazabilidad, alimentar sistemas superiores (MIS/DSS) con datos confiables.
- Ejemplos: Banca (transferencias, depósitos), retail (ventas POS), reservas (aéreas/hotel), nómina.
- Componentes:
  - Entrada: capturas de datos (formularios, sensores, APIs).
  - Procesamiento: validaciones, reglas de negocio, cálculos.
  - Almacenamiento: base de datos transaccional, índices, logs.
  - Salida: confirmaciones, recibos, reportes.
  - Retroalimentación: errores, mensajes, controles de calidad.
- Propiedades clave: ACID (Atomicidad, Consistencia, Aislamiento, Durabilidad); control de concurrencia; manejo de errores y recuperación.
- Diferencias con otros sistemas:
  - MIS: reportes gerenciales, agregación, no necesariamente en tiempo real transaccional.
  - DSS: soporte a decisiones, modelos analíticos, simulaciones.
  - ESS: tableros ejecutivos, indicadores estratégicos.
  - TPS: foco operativo, volumen alto, disponibilidad y exactitud al detalle.

**Actividades Prácticas (Semana 1 y Semana 2)**
- Semana 1: Fundamentos y diseño
  - Identificar caso: ventas minoristas o reservas de salas/recursos.
  - Mapear procesos: actores, eventos, datos, reglas de negocio, excepciones.
  - Definir transacciones: alta de venta/reserva, cancelación, consulta, ajuste.
  - Modelado de datos:
    - Ventas: `customers(id, name, email)`, `products(id, name, price, stock)`, `sales(id, customer_id, total, created_at)`, `sale_items(id, sale_id, product_id, qty, unit_price)`.
    - Reservas: `clients`, `resources`, `bookings(client_id, resource_id, start, end, status)`.
  - Preparar entorno: instalar `Python` y `SQLite`; crear esquema inicial; probar inserciones y consultas.
  - Mini práctica: validar datos de entrada y mensajería de retroalimentación.
- Semana 2: Implementación y evaluación
  - Construir el mini TPS:
    - Funciones de transacción: crear, listar, cancelar/ajustar.
    - Usar transacciones DB (`BEGIN`, `COMMIT`, `ROLLBACK`); validar stock/disponibilidad.
    - Aplicar restricciones: claves foráneas, `CHECK`, `UNIQUE`, `NOT NULL`.
  - Manejo de errores y logs: registrar errores, intentos fallidos, auditoría mínima.
  - Pruebas: casos exitosos y fallidos; concurrencia simulada (serializar operaciones o bloqueo simple).
  - Salidas: recibo de operación, resumen diario de operaciones.
  - Entregables: código funcional, demo breve, informe técnico y conclusiones.

**Ejemplo de Mini TPS (Flask + SQLite en contenedor)**
- Estructura del proyecto (carpeta `Lab2`):
  - `Laboratorio_TPS.md` (esta guía)
  - `Dockerfile` y `app/requirements.txt`
  - `app/app.py`, `app/templates/`, `app/static/`

- Funcionalidad:
  - Registrar ventas: cliente, producto, cantidad.
  - Ver listado de ventas y estado de stock.
  - Control ACID con `BEGIN/COMMIT/ROLLBACK` y restricciones SQLite.

- Cómo ejecutar (requiere Docker):
  1. Construir imagen: `docker build -t sia-lab2-tps .` (en carpeta `Lab2`).
  2. Ejecutar contenedor: `docker run --rm -p 5000:5000 --name sia-lab2-tps sia-lab2-tps`.
  3. Abrir `http://localhost:5000` para usar el formulario.

**Preguntas de Análisis y Discusión**
- ¿Qué tipo de transacciones procesa su sistema y cómo se clasifican?
- ¿Cómo se garantiza la integridad y consistencia de los datos (ACID, restricciones)?
- ¿Qué riesgos de concurrencia existen y cómo los mitigaría?
- ¿Qué diferencias observa entre TPS y MIS/DSS/ESS en propósito y diseño?
- ¿Cómo se maneja la retroalimentación ante errores y validaciones?
- ¿Qué métricas de desempeño serían relevantes para su TPS?
- ¿Qué implicancias tendría escalar el TPS (sharding, colas, idempotencia)?

**Criterios de Evaluación**
- Funcionamiento del mini TPS (40%): operaciones básicas, manejo de errores, transacciones DB.
- Diseño de datos y reglas (25%): esquema correcto, restricciones, trazabilidad, claridad de modelos.
- Análisis y reflexión (25%): respuestas fundamentadas, comparación TPS vs MIS/DSS/ESS, propuestas de mejora.
- Calidad del código y documentación (10%): estructura, claridad, comentarios, instrucciones de ejecución.

**Entregables**
- Código fuente o simulación funcional del mini TPS.
- Informe técnico breve (2–4 páginas): caso elegido, modelo de datos, flujo de transacciones, decisiones de diseño, pruebas realizadas, resultados y limitaciones.
- Conclusiones y reflexiones respondiendo las preguntas planteadas.

**Conclusión**
- Un TPS bien diseñado asegura operaciones confiables y eficientes, sirviendo como base de información para niveles superiores. Con este laboratorio, los estudiantes integran teoría y práctica al construir un sistema que aplica principios de transacciones, integridad y control de concurrencia, y conectan su rol dentro del ecosistema de los Sistemas de Información.