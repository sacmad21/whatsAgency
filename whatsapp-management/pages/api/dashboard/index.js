import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [insights, setInsights] = useState(null);
  const [alerts, setAlerts] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const [insightsResponse, alertsResponse] = await Promise.all([
        fetch('/api/dashboard/insights'),
        fetch('/api/dashboard/alerts'),
      ]);

      const insightsData = await insightsResponse.json();
      const alertsData = await alertsResponse.json();

      setInsights(insightsData);
      setAlerts(alertsData);
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
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
        <p>Loading Insights...</p>
      )}

      <h2>Alerts</h2>
      {alerts ? (
        <div>
          <p>{alerts.message}</p>
          {alerts.alert && <strong style={{ color: 'red' }}>Take Action!</strong>}
        </div>
      ) : (
        <p>Loading Alerts...</p>
      )}
    </div>
  );
}
