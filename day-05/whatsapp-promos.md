# Documentación del flujo: WhatsApp Promos Automation

## Descripción general

Este flujo de n8n automatiza el envío de promociones de un local a través de WhatsApp Business, utilizando datos almacenados en Google Sheets. El flujo se ejecuta automáticamente todos los días a las 9 AM y envía mensajes promocionales personalizados a los clientes según la programación definida en la hoja de promociones.

## Estructura del flujo

- **Cron Trigger:** Ejecuta el flujo diariamente a las 9 AM.
- **Read Promos Sheet:** Lee la hoja de Google Sheets que contiene las promociones programadas.
- **Obtener Promo Hoy:** Filtra las promociones para enviar solo las que corresponden a la fecha actual (YYYY-MM-DD).
- **Read Clients Sheet:** Lee la hoja de Google Sheets con la lista de clientes.
- **Map Promo to Client:** Combina los datos de la promoción seleccionada con los datos de cada cliente y renderiza el mensaje personalizado.
- **Send WhatsApp Message:** Envía el mensaje de WhatsApp usando la API local.

## Formato de datos esperados

### Hoja de Promociones (Promos Sheet)

Columnas requeridas:

- `Template`: Plantilla del mensaje con sintaxis Jinja (ej: "Hola {{ cliente }}, hoy tenemos promocion de x")
- `Fecha`: Fecha de la promoción en formato YYYY-MM-DD (ej: "2025-07-16")

### Hoja de Clientes (Clients Sheet)

Columnas requeridas:

- `Cliente`: Nombre del cliente
- `Numero_Telefono`: Número de teléfono del cliente (formato internacional)

## Explicación de cada nodo

### 1. Cron Trigger

- **Función:** Dispara el flujo a las 9 AM todos los días
- **Configuración:** Programado para ejecutarse diariamente a las 09:00 UTC

### 2. Read Promos Sheet

- **Función:** Obtiene las promociones desde Google Sheets
- **Configuración:** Lee el rango A:C de la hoja de promociones
- **Output:** Datos de todas las promociones disponibles

### 3. Obtener Promo Hoy

- **Función:** Filtra promociones por fecha actual
- **Lógica:**
  - Obtiene la fecha actual en formato YYYY-MM-DD
  - Filtra promociones que coincidan con la fecha actual
  - Retorna array vacío si no hay promociones para hoy (detiene el flujo)

### 4. Read Clients Sheet

- **Función:** Obtiene la lista de clientes desde Google Sheets
- **Configuración:** Lee el rango A:C de la hoja de clientes
- **Output:** Lista completa de clientes con nombres y números

### 5. Map Promo to Client

- **Función:** Combina datos de promoción con cada cliente y renderiza mensajes
- **Lógica:**
  - Obtiene la promoción del día desde el nodo anterior
  - Itera sobre cada cliente
  - Reemplaza `{{ cliente }}` en la plantilla con el nombre real del cliente
  - Genera un objeto por cliente con mensaje personalizado y datos de contacto

### 6. Send WhatsApp Message

- **Función:** Envía mensaje de WhatsApp usando API local
- **Endpoint:** `http://172.17.0.1:3000/send-message/`
- **Método:** POST
- **Body:** `{ "message": "mensaje_personalizado", "to": "numero_telefono" }`

## Ejemplo de funcionamiento

### Datos de entrada:

**Promociones:**

```
Template: "Hola {{ cliente }}, hoy tenemos promocion de pizza 50% off"
Fecha: "2025-07-16"
```

**Clientes:**

```
Cliente: "Marcos", Numero_Telefono: "595985609659"
Cliente: "Ana", Numero_Telefono: "595987654321"
```

### Resultado:

- Para Marcos: "Hola Marcos, hoy tenemos promocion de pizza 50% off" → 595985609659
- Para Ana: "Hola Ana, hoy tenemos promocion de pizza 50% off" → 595987654321

## Configuración requerida

### Credenciales de Google Sheets

- OAuth2 configurado para acceso a las hojas de cálculo
- Permisos de lectura en las hojas de promociones y clientes

### API de WhatsApp

- Servidor local ejecutándose en `http://172.17.0.1:3000`
- Endpoint `/send-message/` disponible y funcional

## Manejo de errores

- **Sin promoción para hoy:** El flujo se detiene sin enviar mensajes
- **Datos faltantes:** Los campos vacíos pueden causar errores en el renderizado
- **API no disponible:** El nodo HTTP Request fallará si el servidor no responde

## Aspectos importantes para la implementación

- Las credenciales de Google Sheets deben estar correctamente configuradas en n8n
- El servidor de WhatsApp debe estar ejecutándose y accesible
- El formato de fecha debe ser exactamente YYYY-MM-DD
- Los nombres de columnas en las hojas deben coincidir exactamente con los especificados

---

Este flujo está diseñado para ser ejecutado y probado en el servidor n8n MCP, siguiendo las mejores prácticas de integración y automatización.
