'use client'
import { useState } from 'react';

export default function ChatPage() {
  const [messages, setMessages] = useState<{role: string, text: string}[]>([]);
  const [input, setInput] = useState('');

  const send = async () => {
    const res = await fetch('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message: input, session_id: 'user_123' })
    });
    const data = await res.json();
    setMessages([...messages, {role: 'user', text: input}, {role: 'bot', text: data.response}]);
    setInput('');
  };

  return (
    <div className="p-10">
      {messages.map((m, i) => <div key={i}><b>{m.role}:</b> {m.text}</div>)}
      <input className="border" value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={send}>Send</button>
    </div>
  );
}
