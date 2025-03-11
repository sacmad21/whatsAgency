import { useState, useEffect } from 'react';

export default function Broadcast() {
  const [users, setUsers] = useState([]);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [content, setContent] = useState('');

  useEffect(() => {
    fetch('/api/users')
      .then((res) => res.json())
      .then((data) => setUsers(data));
  }, []);

  const sendBroadcast = async () => {
    const response = await fetch('/api/broadcast/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_ids: selectedUsers, content }),
    });
    const data = await response.json();
    alert(`Broadcast sent to ${data.responses.length} users!`);
  };

  return (
    <div>
      <h1>Broadcast Message</h1>
      <textarea
        placeholder="Message Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      ></textarea>
      <h2>Select Users</h2>
      {users.map((user) => (
        <div key={user.user_id}>
          <input
            type="checkbox"
            value={user.user_id}
            onChange={(e) => {
              const userId = parseInt(e.target.value, 10);
              setSelectedUsers((prev) =>
                e.target.checked ? [...prev, userId] : prev.filter((id) => id !== userId)
              );
            }}
          />
          {user.name}
        </div>
      ))}
      <button onClick={sendBroadcast}>Send Broadcast</button>
    </div>
  );
}
