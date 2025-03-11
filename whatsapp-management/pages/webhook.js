import { useState, useEffect } from 'react';

export default function Webhooks() {
  const [webhookUrl, setWebhookUrl] = useState('');
  const [currentWebhook, setCurrentWebhook] = useState('');

  useEffect(() => {
    const fetchWebhook = async () => {
      const response = await fetch('/api/webhooks/get');
      const data = await response.json();
      setCurrentWebhook(data.url || 'Not Set');
    };
    fetchWebhook();
  }, []);

  const setWebhook = async () => {
    const response = await fetch('/api/webhooks/set', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ webhookUrl }),
    });
    const data = await response.json();
    alert('Webhook URL set successfully!');
    setCurrentWebhook(webhookUrl);
  };

  return (
    <div>
      <h1>Webhook Management</h1>
      <p>Current Webhook URL: {currentWebhook}</p>
      <input
        type="text"
        placeholder="Enter Webhook URL"
        value={webhookUrl}
        onChange={(e) => setWebhookUrl(e.target.value)}
      />
      <button onClick={setWebhook}>Set Webhook URL</button>
    </div>
  );
}
