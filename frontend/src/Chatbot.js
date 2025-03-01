import React, { useState } from "react";
import "./Chatbot.css"; // Import CSS for styling

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Add user message to chat
    const newMessages = [...messages, { text: input, sender: "user" }];
    setMessages(newMessages);
    setInput("");

    // Display "Thinking..." while waiting for API response
    setMessages([...newMessages, { text: "Thinking...", sender: "bot" }]);

    try {
      const response = await fetch("https://api.openai.com/v1/chat/completions", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`,
        },
        body: JSON.stringify({
          model: "gpt-4", // Use "gpt-3.5-turbo" if preferred
          messages: [{ role: "user", content: input }],
        }),
      });

      const data = await response.json();
      const botMessage = data.choices?.[0]?.message?.content || "I'm not sure how to respond.";

      // Update chat with bot's response
      setMessages([...newMessages, { text: botMessage, sender: "bot" }]);
    } catch (error) {
      setMessages([...newMessages, { text: "Error fetching response.", sender: "bot" }]);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">Avalanche - Your Crypto Trading Assistant</div>
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
          placeholder="Ask me about crypto trading..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chatbot;
