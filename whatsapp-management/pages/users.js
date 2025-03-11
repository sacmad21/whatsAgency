import { useState, useEffect } from 'react';
import Link from 'next/link';

export default function UsersPage() {
  const [users, setUsers] = useState([]);
  const [newUser, setNewUser] = useState({ phoneNumber: '', name: '', optInStatus: true });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch('/api/users');
      const data = await response.json();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setNewUser((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const addUser = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newUser),
      });
      if (response.ok) {
        setNewUser({ phoneNumber: '', name: '', optInStatus: true });
        fetchUsers();
      } else {
        console.error('Failed to add user');
      }
    } catch (error) {
      console.error('Error adding user:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Users</h1>
      <form onSubmit={addUser}>
        <div>
          <label>
            Phone Number:
            <input
              type="text"
              name="phoneNumber"
              value={newUser.phoneNumber}
              onChange={handleInputChange}
              required
            />
          </label>
        </div>
        <div>
          <label>
            Name:
            <input
              type="text"
              name="name"
              value={newUser.name}
              onChange={handleInputChange}
            />
          </label>
        </div>
        <div>
          <label>
            Opt-in Status:
            <input
              type="checkbox"
              name="optInStatus"
              checked={newUser.optInStatus}
              onChange={handleInputChange}
            />
          </label>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Adding...' : 'Add User'}
        </button>
      </form>

      <h2>User List</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>
            {user.phoneNumber} - {user.name} ({user.optInStatus ? 'Opted In' : 'Opted Out'})
            <Link href={`/users/${user.id}`}>
              View
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
