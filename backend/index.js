const express = require("express");
const cors = require("cors");
const axios = require("axios");
const { Client } = require("pg");

const app = express();
app.use(cors());
app.use(express.json());

// ================= DB =================
const db = new Client({
  host: "postgres",
  user: "dev",
  password: "123",
  database: "appdb",
});

db.connect().catch((err) => {
  console.log("DB connection error:", err.message);
});

// ================= HEALTH =================
app.get("/", (req, res) => {
  res.json({ status: "Backend OK 🚀" });
});

// ================= REGISTER =================
app.post("/register", async (req, res) => {
  try {
    const { email, password } = req.body;

    await db.query(
      "INSERT INTO users(email, password) VALUES($1, $2)",
      [email, password]
    );

    res.json({ status: "registered" });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ================= LOGIN (simple version, no bcrypt biar stabil) =================
app.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body;

    const user = await db.query(
      "SELECT * FROM users WHERE email=$1",
      [email]
    );

    if (!user.rows[0]) {
      return res.status(401).json({ error: "user not found" });
    }

    if (user.rows[0].password !== password) {
      return res.status(401).json({ error: "wrong password" });
    }

    res.json({ status: "login success", user: user.rows[0] });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ================= CHAT STREAM (SAFE VERSION) =================
app.post("/chat-stream", async (req, res) => {
  const message = req.body.message;

  res.setHeader("Content-Type", "text/plain; charset=utf-8");
  res.setHeader("Transfer-Encoding", "chunked");

  try {
    const ai = await axios.post("http://ai:8000/ask", {
      prompt: message,
    });

    res.write(ai.data.response || "AI offline");
    res.end();
  } catch (err) {
    res.write("AI service error");
    res.end();
  }
});

// ================= SAVE CHAT =================
app.post("/chat", async (req, res) => {
  try {
    const { message } = req.body;

    const result = await db.query(
      "INSERT INTO chats(role, message) VALUES($1, $2) RETURNING *",
      ["user", message]
    );

    res.json(result.rows[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ================= GET CHATS =================
app.get("/chats", async (req, res) => {
  try {
    const result = await db.query(
      "SELECT * FROM chats ORDER BY id ASC"
    );

    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ================= START (DOCKER SAFE) =================
app.listen(3000, "0.0.0.0", () => {
  console.log("Backend running on port 3000");
});
