import { useState, useEffect } from 'react';

export default function Alerts() {
  const [alertData, setAlertData] = useState(null);

  useEffect(() => {
    const fetchAlerts = async () => {
      const response = await fetch('/api/dashboard/alerts');
      const result = await response.json();
      setAlertData(result);
    };
    fetchAlerts();
  }, []);

  return (
    <div>
      <h1>Cost Alerts</h1>
      {alertData ? (
        <div>
          <p>{alertData.message}</p>
          {alertData.alert && <strong style={{ color: 'red' }}>Take Action!</strong>}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}
