import { useState, useEffect } from 'react';
import io from 'socket.io-client';

let socket;

export default function Dashboard() {
  const [insights, setInsights] = useState(null);

  useEffect(() => {
    // Fetch initial data
    const fetchData = async () => {
      const response = await fetch('/api/dashboard/insights');
      const data = await response.json();
      setInsights(data);
    };
    fetchData();

    // Connect to WebSocket server
    if (!socket) {
      socket = io({
        path: '/api/socket',
      });

      socket.on('connect', () => {
        console.log('Connected to WebSocket server');
      });

      // Listen for updates
      socket.on('updateConversations', (newConversations) => {
        console.log('Received new conversations:', newConversations);
        // Update state with new data
        fetchData(); // Refetch updated data
      });Observe Updates: Open the dashboard page. As new conversations are added or costs change, the dashboard should update in real time.
    }

    return () => {
      if (socket) {
        socket.disconnect();
      }
    };
  }, []);

  return (
    <div>
      <h1>Real-Time Dashboard</h1>
      {insights ? (
        <div>
          <h2>Active Conversations</h2>
          <p>{insights.activeConversations}</p>

          <h2>Total Cost</h2>
          <p>${insights.totalCost.toFixed(2)}</p>

          <h2>Category Breakdown</h2>
          <table>
            <thead>
              <tr>
                <th>Category</th>
                <th>Count</th>
                <th>Total Cost</th>
              </tr>
            </thead>
            <tbody>
              {insights.categoryBreakdown.map((category) => (
                <tr key={category.type}>
                  <td>{category.type}</td>
                  <td>{category._count.type}</td>
                  <td>${category._sum.pricing_amount.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
