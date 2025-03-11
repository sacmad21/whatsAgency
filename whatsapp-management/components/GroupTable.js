// components/GroupTable.js
import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Button } from 'primereact/button';

export default function GroupTable() {
  const [groups, setGroups] = useState([]);
  const [expandedRows, setExpandedRows] = useState(null);

  // Fetch groups with participants
  useEffect(() => {
    async function fetchGroups() {
      const response = await fetch('/api/groups');
      const data = await response.json();
      setGroups(data);
    }
    fetchGroups();
  }, []);

  // Template for the expanded row (nested participants table)
  const rowExpansionTemplate = (data) => {
    return (
      <DataTable
        value={data.participants}
        dataKey="id"
        responsiveLayout="scroll"
        header={`Participants of Group: ${data.name}`}
      >
        <Column field="id" header="Participant ID" style={{ minWidth: '10rem' }} />
        <Column
          field="participant.phoneNumber"
          header="Phone Number"
          style={{ minWidth: '15rem' }}
          body={(rowData) => rowData.participant.phoneNumber}
        />
        <Column field="role" header="Role" style={{ minWidth: '10rem' }} />
        <Column field="joinedAt" header="Joined At" style={{ minWidth: '15rem' }} />
      </DataTable>
    );
  };

  // Action buttons for each group row
  const actionBodyTemplate = (rowData) => {
    return (
      <div className="actions">
        <Button
          icon="pi pi-pencil"
          className="p-button-rounded p-button-warning mr-2"
          tooltip="Edit Group"
        />
        <Button
          icon="pi pi-trash"
          className="p-button-rounded p-button-danger"
          tooltip="Delete Group"
        />
      </div>
    );
  };

  return (
    <div className="card">
      <h3 className="mb-4">Group Management</h3>
      <DataTable
        value={groups}
        dataKey="id"
        expandedRows={expandedRows}
        onRowToggle={(e) => setExpandedRows(e.data)}
        rowExpansionTemplate={rowExpansionTemplate}
        responsiveLayout="scroll"
        paginator
        rows={10}
        rowsPerPageOptions={[5, 10, 25]}
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} groups"
        header="List of Groups"
      >
        <Column expander style={{ width: '3em' }} />
        <Column field="id" header="Group ID" sortable style={{ minWidth: '10rem' }} />
        <Column field="groupId" header="Unique Group ID" sortable style={{ minWidth: '15rem' }} />
        <Column field="name" header="Name" sortable style={{ minWidth: '10rem' }} />
        <Column
          field="creator.phoneNumber"
          header="Creator Phone"
          body={(rowData) => rowData.creator.phoneNumber}
          style={{ minWidth: '15rem' }}
        />
        <Column field="createdAt" header="Created At" style={{ minWidth: '15rem' }} sortable />
        <Column body={actionBodyTemplate} style={{ minWidth: '12rem' }} />
      </DataTable>
    </div>
  );
}
