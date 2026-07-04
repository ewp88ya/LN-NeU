require("dotenv").config();

const express = require("express");
const cors = require("cors");
const axios = require("axios");
const jwt = require("jsonwebtoken");
const bcrypt = require("bcryptjs");
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

db.connect();

// ================= AUTH MIDDLEWARE =================
function auth(req, res, next) {
  const token = req.headers.authorization;

  if (!token) return res.status(401).json({ error: "no token" });

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded;
    next();
  } catch {
    return res.status(401).json({ error: "invalid token" });
  }
}

// ================= HEALTH =================
app.get("/", (req, res) => {
  res.json({ status: "SAAS AI READY 🚀" });
});

// ================= REGISTER =================
app.post("/register", async (req, res) => {
  try {
    const { email, password } = req.body;

    const hash = await bcrypt.hash(password, 10);

    await db.query(
      "INSERT INTO users(email, password) VALUES($1, $2)",
      [email, hash]
    );

    res.json({ status: "registered" });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ================= LOGIN =================
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

    const valid = await bcrypt.compare(password, user.rows[0].password);

    if (!valid) {
      return res.status(401).json({ error: "wrong password" });
    }

    const token = jwt.sign(
      { id: user.rows[0].id, email },
      process.env.JWT_SECRET
    );

    res.json({ token });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ================= CHAT (PER USER) =================
app.post("/chat", auth, async (req, res) => {
  try {
    const { message } = req.body;

    await db.query(
      "INSERT INTO chats(role, message, user_id) VALUES($1,$2,$3)",
      ["user", message, req.user.id]
    );

    let reply;

    try {
      const openai = await axios.post(
        "http://ai:8000/ask",
        { prompt: message }
      );

      reply = openai.data.response;
    } catch {
      reply = "AI fallback response";
    }

    await db.query(
      "INSERT INTO chats(role, message, user_id) VALUES($1,$2,$3)",
      ["ai", reply, req.user.id]
    );

    res.json({ user: message, ai: reply });

  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ================= CHAT HISTORY =================
app.get("/chats", auth, async (req, res) => {
  try {
    const result = await db.query(
      "SELECT * FROM chats WHERE user_id=$1 ORDER BY id ASC",
      [req.user.id]
    );

    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ================= START =================
app.listen(3000, "0.0.0.0", () => {
  console.log("Backend SaaS running on 3000");
});

console.log("TEST FROM VS CODE");