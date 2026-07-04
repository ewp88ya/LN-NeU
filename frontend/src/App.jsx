import { useState } from "react";

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    const userMsg = input;
    setInput("");

    setMessages((prev) => [...prev, { role: "user", text: userMsg }]);

    const res = await fetch("http://localhost:3000/chat-stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMsg }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    let aiText = "";

    setMessages((prev) => [...prev, { role: "ai", text: "" }]);

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;

      aiText += decoder.decode(value);

      setMessages((prev) => {
        const copy = [...prev];
        copy[copy.length - 1].text = aiText;
        return copy;
      });
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>ChatGPT SaaS 🚀</h2>

      <div style={{ height: 400, overflow: "auto" }}>
        {messages.map((m, i) => (
          <div key={i}>
            <b>{m.role}:</b> {m.text}
          </div>
        ))}
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        style={{ width: 300 }}
      />

      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
