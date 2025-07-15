# Automatización n8n: Top 5 Noticias por Tema vía WhatsApp

// Todavia no probé el RSS

Este documento describe la lógica y requisitos para dos flujos de n8n que generan y envían un resumen de las 5 noticias principales ("Los 5 del día") de una categoría temática seleccionada, utilizando fuentes RSS o FireCrawl, y entregando el resultado vía WhatsApp mediante una API local.

---

## 1. Fuentes de Datos

### RSS

- [ABC Nacionales](https://www.abc.com.py/arc/outboundfeeds/rss/nacionales/?outputType=xml)
- [ABC Noticias del Día](https://www.abc.com.py/arc/outboundfeeds/rss/noticias-del-dia/?outputType=xml)
- [ABC Mundo](https://www.abc.com.py/arc/outboundfeeds/rss/mundo/?outputType=xml)
- [IP Economía](https://www.ip.gov.py/ip/economia/feed/)
- [Economía.com.py](https://economia.com.py/feed/) _(principal fuente)_

### FireCrawl

- Permite obtener contenido en formato Markdown desde páginas como:  
   [Indicadores Económicos](https://economia.com.py/category/economia/indicadores-economicos/)

---

## 2. Categorías Disponibles

Las categorías pueden ser seleccionadas dinámicamente por el primer nodo de fetch (RSS o FireCrawl). Ejemplos de categorías:

- [Economía](https://economia.com.py/category/economia/)
  - [Desarrollo Económico](https://economia.com.py/category/economia/desarrollo-economico/)
  - [Energía](https://economia.com.py/category/economia/energia/)
  - [Gasto Público](https://economia.com.py/category/economia/gasto-publico/)
  - [Indicadores Económicos](https://economia.com.py/category/economia/indicadores-economicos/)
  - [Índices de Inflación](https://economia.com.py/category/economia/indices-de-inflacion/)
- [Finanzas](https://economia.com.py/category/finanzas/)
  - [Banco Central](https://economia.com.py/category/finanzas/banco-central/)
  - [Bancos y Financieras](https://economia.com.py/category/finanzas/bancos-y-financieras/)
  - [Cooperativas](https://economia.com.py/category/finanzas/cooperativas/)
  - [Criptomonedas](https://economia.com.py/category/finanzas/criptomonedas/)
  - [Mercado Bursátil](https://economia.com.py/category/finanzas/mercado-bursatil/)
- [Estilo](https://economia.com.py/category/estilo/)
  - [Autos](https://economia.com.py/category/estilo/autos/)
  - [Cultura](https://economia.com.py/category/estilo/cultura/)
  - [Eventos](https://economia.com.py/category/estilo/eventos/)
  - [Hoteles](https://economia.com.py/category/estilo/hoteles/)
  - [Moda](https://economia.com.py/category/estilo/moda/)
- [Negocios](https://economia.com.py/category/negocios/)
  - [Agronegocios](https://economia.com.py/category/negocios/agronegocios/)
  - [Comercios](https://economia.com.py/category/negocios/comercios/)
  - [Emprendedores](https://economia.com.py/category/negocios/emprendedores/)
  - [Empresas](https://economia.com.py/category/negocios/empresas/)
  - [Gremios](https://economia.com.py/category/negocios/gremios/)
  - [Industrias](https://economia.com.py/category/negocios/industrias/)
  - [Inmobiliario](https://economia.com.py/category/negocios/inmobiliario-negocios/)
  - [Inversión](https://economia.com.py/category/negocios/inversion/)
  - [Mipymes](https://economia.com.py/category/negocios/mipymes/)
- [Internacional](https://economia.com.py/category/internacional/)
  - [Mercosur](https://economia.com.py/category/internacional/mercosur/)
  - [Mundo](https://economia.com.py/category/internacional/mundo/)

---

## 3. Flujo General

### A. Fetch de Noticias

- El flujo inicia con la obtención de noticias desde RSS o FireCrawl según la categoría seleccionada.

### B. Filtrado y Resumen

- Un LLM filtra y selecciona las 5 noticias más relevantes del día para la categoría.
- El LLM genera un resumen breve para cada noticia.

### C. Envío a WhatsApp

- Los resúmenes se envían mediante un POST HTTP a una API local que conecta con WhatsApp.

---

## 4. Ejemplo de Estructura de Respuesta

```json
{
    "categoria": "Indicadores Económicos",
    "fecha": "2025-07-11",
    "noticias": [
        {
            "titulo": "Rodio y platino disparan sus precios y pelean al oro como refugio de valor",
            "url": "https://economia.com.py/rodio-y-platino-disparan-sus-precios-y-pelean-al-oro-como-refugio-de-valor-crisis-sudafricana-impulsa-el-auge-de-metales-industriales/",
            "resumen": "El rodio, el metal más caro del mundo, sube más de 25% en 2025 por escasez y problemas de suministro en Sudáfrica. El platino también destaca por su rebote industrial."
        },
        ...
    ]
}
```

---

## 5. Consideraciones Técnicas

- El flujo debe ser configurable para seleccionar la categoría.
- El procesamiento y resumen debe ser robusto para entradas tanto RSS como Markdown.
- El envío a WhatsApp debe manejar errores y reintentos.
- No incluir imágenes en el resumen final para WhatsApp.

---

## 6. Ejemplo de RSS

```xml
<item>
    <title>Rodio y platino disparan sus precios...</title>
    <link>https://economia.com.py/rodio-y-platino-disparan-sus-precios...</link>
    <pubDate>Fri, 11 Jul 2025 17:11:36 +0000</pubDate>
    <category><![CDATA[Industrias]]></category>
    <description><![CDATA[El rodio, considerado el metal más caro del mundo...]]></description>
</item>
```

---

## 7. Enlaces Útiles

- [Facebook](https://www.facebook.com/economiayfinanzaspy/)
- [Instagram](https://www.instagram.com/economia_com/?hl=es-la)
- [Youtube](https://www.youtube.com/channel/UCVWXVGsKAnA8moFVHewK1XA)

---

> **Nota:** Este documento sirve como base para prompting y generación de flujos n8n que automaticen la entrega diaria de noticias resumidas por categoría vía WhatsApp.
