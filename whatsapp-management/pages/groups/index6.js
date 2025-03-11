import React, { useEffect, useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';

import 'primereact/resources/themes/saga-blue/theme.css';    // or your preferred theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';


export default function GroupListWithParticipants() {
  const [groups, setGroups] = useState([]);
  const [expandedRows, setExpandedRows] = useState(null);

  // Fetch all groups with participants
  useEffect(() => {
    fetchGroups();
  }, []);

  async function fetchGroups() {
    const res = await fetch('/api/groups');
    const data = await res.json();
    setGroups(data);
  }

  // Template to show the nested table for participants
  const participantsTableTemplate = (groupData) => {
    return (
      <DataTable value={groupData.participants} dataKey="id" responsiveLayout="scroll">
        <Column field="id" header="Participant ID" style={{ minWidth: '6rem' }} />
        <Column
          field="participant.phoneNumber"
          header="Phone Number"
          body={(rowData) => rowData.participant.phoneNumber}
          style={{ minWidth: '10rem' }}
        />
        <Column field="role" header="Role" style={{ minWidth: '6rem' }} />
        <Column
          field="joinedAt"
          header="Joined At"
          body={(rowData) => new Date(rowData.joinedAt).toLocaleString()}
          style={{ minWidth: '10rem' }}
        />
        <Column
          header="Actions"
          body={(rowData) => (
            <Button
              label="Message"
              icon="pi pi-whatsapp"
              className="p-button-sm p-button-success"
              onClick={() => handleSendMessage(rowData)}
            />
          )}
          style={{ minWidth: '8rem' }}
        />
      </DataTable>
    );
  };

  // Handle WhatsApp message action
  const handleSendMessage = (participant) => {
    alert(`Sending message to ${participant.participant.phoneNumber}`);
    // Call WhatsApp API to send message
  };

  // Row expansion icon template
  const rowExpansionTemplate = (rowData) => participantsTableTemplate(rowData);

  // Header for the main DataTable
  const header = (
    <div className="table-header">
      <h4 className="m-0">Manage Groups</h4>
    </div>
  );

  return (
    <div className="card">
      <DataTable
        value={groups}
        dataKey="id"
        expandedRows={expandedRows}
        onRowToggle={(e) => setExpandedRows(e.data)}
        rowExpansionTemplate={rowExpansionTemplate}
        responsiveLayout="scroll"
        paginator
        rows={10}
        header={header}
      >
        {/* Expander Column */}
        <Column expander style={{ width: '3em' }} />

        {/* Group Fields */}
        <Column field="id" header="ID" sortable style={{ minWidth: '5rem' }} />
        <Column field="groupId" header="Group ID" sortable style={{ minWidth: '8rem' }} />
        <Column field="name" header="Name" sortable style={{ minWidth: '10rem' }} />
        <Column field="description" header="Description" style={{ minWidth: '12rem' }} />
        <Column
          field="createdAt"
          header="Created At"
          body={(rowData) => new Date(rowData.createdAt).toLocaleString()}
          sortable
          style={{ minWidth: '10rem' }}
        />
        <Column
          field="updatedAt"
          header="Updated At"
          body={(rowData) => new Date(rowData.updatedAt).toLocaleString()}
          sortable
          style={{ minWidth: '10rem' }}
        />
      </DataTable>
    </div>
  );
}
