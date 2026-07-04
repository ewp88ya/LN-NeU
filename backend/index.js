const express = require("express");
const axios = require("axios");
const { Client } = require("pg");

const app = express();
app.use(express.json());

// ================= DATABASE =================
const db = new Client({
  host: "postgres",
  user: "dev",
  password: "123",
  database: "appdb",
  port: 5432,
});

// retry connect DB (WAJIB untuk docker)
async function connectDB() {
  while (true) {
    try {
      await db.connect();
      console.log("DB connected");
      break;
    } catch (err) {
      console.log("DB not ready, retrying...");
      await new Promise((r) => setTimeout(r, 3000));
    }
  }
}

// init table
async function initDB() {
  try {
    await db.query(`
      CREATE TABLE IF NOT EXISTS chats (
        id SERIAL PRIMARY KEY,
        msg TEXT
      )
    `);
    console.log("Table ready");
  } catch (err) {
    console.log("Init DB error:", err.message);
  }
}

// ================= ROUTES =================

// health check
app.get("/", (req, res) => {
  res.json({ message: "Backend OK 🚀" });
});

// save message
app.get("/save", async (req, res) => {
  try {
    const msg = req.query.msg;
    await db.query("INSERT INTO chats(msg) VALUES($1)", [msg]);

    res.json({
      status: "saved",
      msg,
    });
  } catch (err) {
    res.status(500).json({
      error: "Failed to save message",
      detail: err.message,
    });
  }
});

// get all chats
app.get("/chats", async (req, res) => {
  try {
    const result = await db.query("SELECT * FROM chats ORDER BY id DESC");
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({
      error: "Failed to fetch chats",
      detail: err.message,
    });
  }
});

// get chat by id
app.get("/chat/:id", async (req, res) => {
  try {
    const result = await db.query(
      "SELECT * FROM chats WHERE id = $1",
      [req.params.id]
    );

    res.json(result.rows[0] || {});
  } catch (err) {
    res.status(500).json({
      error: "Failed to fetch chat",
      detail: err.message,
    });
  }
});

// ================= AI INTEGRATION =================
app.get("/api/ask-ai", async (req, res) => {
  const prompt = req.query.prompt;

  try {
    const aiResponse = await axios.post("http://ai:8000/ask", {
      prompt: prompt,
    });

    res.json({
      prompt,
      ai_response: aiResponse.data,
    });
  } catch (err) {
    res.status(500).json({
      error: "AI service not reachable",
      detail: err.message,
    });
  }
});

// ================= START SERVER =================
app.listen(3000, () => {
  console.log("Backend running on port 3000");
});

// ================= STARTUP ORDER (IMPORTANT) =================
(async () => {
  await connectDB();
  await initDB();
})();
