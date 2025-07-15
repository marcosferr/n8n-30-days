# Documentación del flujo: WhatsApp Promos Automation

## Descripción general

Este flujo de n8n automatiza el envío de promociones de un local a través de WhatsApp Business, utilizando datos almacenados en Google Sheets. El flujo se ejecuta automáticamente todos los días a las 9 AM y envía mensajes promocionales personalizados a los clientes según la programación definida en la hoja de promociones.

## Estructura del flujo

- **Trigger (Cron):** Ejecuta el flujo diariamente a las 9 AM.
- **Read Promos Sheet:** Lee la hoja de Google Sheets que contiene las promociones programadas.
- **Filter by Date:** Filtra las promociones para enviar solo las que corresponden a la fecha actual.
- **Read Clients Sheet:** Lee la hoja de Google Sheets con la lista de clientes.
- **Merge Promo & Client:** Combina los datos de la promoción seleccionada con los datos de cada cliente.
- **Send WhatsApp Promo:** Envía el mensaje de WhatsApp usando la plantilla y los datos personalizados de cada cliente.

## Explicación de cada nodo

- **Cron Trigger:** Dispara el flujo a las 9 AM todos los días.
- **Read Promos Sheet:** Obtiene las promociones desde una hoja de Google Sheets. Se espera que la hoja tenga las columnas: `Nombre_Promo`, `Plantilla`, `Fecha`.
- **Filter by Date:** Filtra las promociones para que solo se procesen las que tienen la fecha igual a la del día de ejecución.
- **Read Clients Sheet:** Obtiene la lista de clientes desde otra hoja de Google Sheets. Se espera que la hoja tenga las columnas: `Nombre`, `Apellido`, `Numero_Telefono`.
- **Merge Promo & Client:** Une los datos de la promoción seleccionada con cada cliente para personalizar el mensaje.
- **Send WhatsApp Promo:** Envía el mensaje de WhatsApp usando la API de WhatsApp Business Cloud, utilizando la plantilla y los datos personalizados.

## Aspectos importantes

- Las credenciales de Google Sheets y WhatsApp Business Cloud deben estar correctamente configuradas en n8n.
- Las variables de entorno `SHEET_ID_PROMOS`, `SHEET_ID_CLIENTES` y `WHATSAPP_NUMBER_ID` deben estar definidas.
- Las plantillas de WhatsApp deben estar previamente aprobadas y configuradas en Meta.
- El formato de fecha en la hoja de promociones debe ser `YYYY-MM-DD`.

## Requisitos previos y dependencias

- Acceso a Google Sheets con permisos de lectura.
- Acceso a WhatsApp Business Cloud API con plantillas configuradas.
- Configuración de variables de entorno en n8n para los IDs de las hojas y el número de WhatsApp.

---

Este flujo está diseñado para ser ejecutado y probado en el servidor n8n MCP, siguiendo las mejores prácticas de integración y automatización.
