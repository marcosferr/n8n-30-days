const express = require("express");
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

const app = express();
const port = 3000;

// Middleware para parsear JSON
app.use(express.json());

// Inicializar cliente de WhatsApp
const client = new Client({
  authStrategy: new LocalAuth(),
});

// Variable para controlar si el cliente está listo
let isClientReady = false;

// Generar código QR
client.on("qr", (qr) => {
  console.log("📱 Escanea el siguiente código QR con WhatsApp:");
  qrcode.generate(qr, { small: true });
});

// Cliente autenticado
client.on("authenticated", () => {
  console.log("✅ Cliente autenticado correctamente");
});

// Cliente listo para usar
client.on("ready", () => {
  console.log("🚀 Cliente de WhatsApp está listo");
  isClientReady = true;
});

// Error de autenticación
client.on("auth_failure", (msg) => {
  console.error("❌ Error de autenticación:", msg);
});

// Desconexión del cliente
client.on("disconnected", (reason) => {
  console.log("🔌 Cliente desconectado:", reason);
  isClientReady = false;
});

// Inicializar cliente
client.initialize();

// Endpoint para enviar mensajes
app.post("/send-message", async (req, res) => {
  try {
    const { to, message } = req.body;

    // Validar que el cliente esté listo
    if (!isClientReady) {
      return res.status(503).json({
        success: false,
        error:
          "El cliente de WhatsApp no está listo. Por favor, escanea el código QR.",
      });
    }

    // Validar datos requeridos
    if (!to || !message) {
      return res.status(400).json({
        success: false,
        error: 'Los campos "to" y "message" son requeridos',
      });
    }

    // Validar formato del número (debe ser solo números)
    const phoneRegex = /^\d+$/;
    if (!phoneRegex.test(to)) {
      return res.status(400).json({
        success: false,
        error:
          "El número de teléfono debe contener solo números (ejemplo: 595985609659)",
      });
    }

    // Formatear número para WhatsApp (agregar @c.us)
    const chatId = `${to}@c.us`;

    // Verificar si el número existe en WhatsApp
    const isRegistered = await client.isRegisteredUser(chatId);
    if (!isRegistered) {
      return res.status(400).json({
        success: false,
        error: "El número no está registrado en WhatsApp",
      });
    }

    // Enviar mensaje
    const sentMessage = await client.sendMessage(chatId, message);

    console.log(`📤 Mensaje enviado a ${to}: ${message}`);

    res.json({
      success: true,
      message: "Mensaje enviado correctamente",
      messageId: sentMessage.id.id,
      to: to,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    console.error("❌ Error al enviar mensaje:", error);
    res.status(500).json({
      success: false,
      error: "Error interno del servidor al enviar el mensaje",
    });
  }
});

// Endpoint para verificar estado del cliente
app.get("/status", (req, res) => {
  res.json({
    clientReady: isClientReady,
    status: isClientReady
      ? "Listo para enviar mensajes"
      : "Esperando autenticación",
  });
});

// Endpoint de salud
app.get("/health", (req, res) => {
  res.json({
    status: "ok",
    timestamp: new Date().toISOString(),
  });
});

// Iniciar servidor
app.listen(port, () => {
  console.log(`🌐 Servidor ejecutándose en http://localhost:${port}`);
  console.log(`📊 Estado del cliente: GET /status`);
  console.log(`📨 Enviar mensaje: POST /send-message`);
  console.log(`\n⚠️  Para usar la aplicación:`);
  console.log(`1. Escanea el código QR que aparecerá a continuación`);
  console.log(`2. Espera a que aparezca "Cliente de WhatsApp está listo"`);
  console.log(`3. Envía mensajes usando el endpoint POST /send-message`);
  console.log(`\n📝 Ejemplo de uso con curl:`);
  console.log(`curl -X POST http://localhost:3000/send-message \\`);
  console.log(`  -H "Content-Type: application/json" \\`);
  console.log(`  -d '{"to": "595985609659", "message": "Hola desde la API!"}'`);
});

// Manejo de cierre graceful
process.on("SIGINT", async () => {
  console.log("\n🔄 Cerrando aplicación...");
  await client.destroy();
  process.exit(0);
});

process.on("SIGTERM", async () => {
  console.log("\n🔄 Cerrando aplicación...");
  await client.destroy();
  process.exit(0);
});
