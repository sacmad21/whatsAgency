import Link from 'next/link';

export default function Home() {
  return (
    <div style={{ fontFamily: 'Arial, sans-serif', margin: '20px' }}>
      <h1>Main Navigation</h1>
      <p>Welcome to the WhatsApp API Management Application. Choose an action below:</p>
      
      <h2>Manage WhatsApp APIs</h2>
      <ul>
        <li>
          <Link href="/contacts">Contact Management</Link>
        </li>
        <li>
          <Link href="/media">Media Management</Link>
        </li>
        <li>
          <Link href="/messages">Message Management</Link>
        </li>
        <li>
          <Link href="/groups">Group Management</Link>
        </li>
        <li>
          <Link href="/broadcasts">Broadcast Messaging</Link>
        </li>
        <li>
          <Link href="/metrics">Insights & Metrics</Link>
        </li>
        <li>
          <Link href="/webhooks">Webhook Management</Link>
        </li>
      </ul>
      
      <h2>Database Management</h2>
      <ul>
        <li>
          <Link href="/tenants">Tenant Management</Link>
        </li>
        <li>
          <Link href="/users">User Management</Link>
        </li>
        <li>
          <Link href="/groups">Group Table Management</Link>
        </li>
        <li>
          <Link href="/messages">Message Records</Link>
        </li>
        <li>
          <Link href="/media">Media Table Management</Link>
        </li>
      </ul>
      
      <h2>Settings</h2>
      <ul>
        <li>
          <Link href="/settings">API Credentials & Configurations</Link>
        </li>
      </ul>
    </div>
  );
}
