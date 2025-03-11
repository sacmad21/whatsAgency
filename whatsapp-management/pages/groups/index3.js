// pages/groups/index.js
import React, { useEffect, useRef, useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { InputTextarea } from 'primereact/inputtextarea';
import { Dropdown } from 'primereact/dropdown';

import 'primereact/resources/themes/saga-blue/theme.css';    // or your preferred theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';


export default function GroupList() {
  const [groups, setGroups] = useState([]);
  const [selectedGroups, setSelectedGroups] = useState(null);
  const [globalFilter, setGlobalFilter] = useState('');

  const [groupDialog, setGroupDialog] = useState(false);
  const [currentGroup, setCurrentGroup] = useState({});
  const [isEditMode, setIsEditMode] = useState(false);

  const [broadcastDialog, setBroadcastDialog] = useState(false);
  const [broadcastMessage, setBroadcastMessage] = useState('');

  const dt = useRef(null);

  // Fetch all groups
  useEffect(() => {
    fetchGroups();
  }, []);

  async function fetchGroups() {
    const res = await fetch('/api/groups');
    const data = await res.json();
    setGroups(data);
  }

  // Toolbar actions
  const leftToolbarTemplate = () => {
    return (
      <React.Fragment>
        <Button
          label="New Group"
          icon="pi pi-plus"
          className="p-button-success mr-2"
          onClick={() => openNew()}
        />
      </React.Fragment>
    );
  };

  const rightToolbarTemplate = () => {
    return (
      <>
        {/* Example multi-row broadcast from toolbar */}
        <Button
          label="Broadcast to Selected"
          icon="pi pi-whatsapp"
          className="p-button-info ml-2"
          onClick={openBroadcastDialogForMultiple}
          disabled={!selectedGroups || selectedGroups.length === 0}
        />
      </>
    );
  };

  function openNew() {
    setCurrentGroup({
      groupId: '',
      name: '',
      description: '',
      createdBy: 1 // Example: might set default or let user pick
    });
    setIsEditMode(false);
    setGroupDialog(true);
  }

  function hideDialog() {
    setGroupDialog(false);
  }

  function hideBroadcastDialog() {
    setBroadcastDialog(false);
    setBroadcastMessage('');
  }

  // Edit a single group
  async function editGroup(groupData) {
    setCurrentGroup({ ...groupData });
    setIsEditMode(true);
    setGroupDialog(true);
  }

  async function saveGroup() {
    if (isEditMode) {
      // update
      await fetch(`/api/groups/${currentGroup.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentGroup)
      });
    } else {
      // create
      await fetch('/api/groups', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentGroup)
      });
    }
    fetchGroups();
    setGroupDialog(false);
  }

  // Delete a single group
  async function deleteGroup(groupData) {
    if (!window.confirm(`Are you sure you want to delete ${groupData.name}?`)) return;
    await fetch(`/api/groups/${groupData.id}`, { method: 'DELETE' });
    fetchGroups();
  }

  // Broadcast - row-level
  function openBroadcastDialogForRow(rowData) {
    setSelectedGroups([rowData]);
    setBroadcastDialog(true);
  }

  // Broadcast - multi-row from toolbar
  function openBroadcastDialogForMultiple() {
    setBroadcastDialog(true);
  }

  // Confirm broadcast
  async function confirmBroadcast() {
    // For this example, we’ll just broadcast text
    for (const grp of selectedGroups) {
      await fetch('/api/whatsapp/broadcast-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ groupId: grp.id, messageText: broadcastMessage })
      });
    }
    alert('Broadcast(s) sent!');
    hideBroadcastDialog();
  }



  
  // Row body templates
  const actionBodyTemplate = (rowData) => {
    return (
      <React.Fragment>
        <Button
          icon="pi pi-pencil"
          className="p-button-rounded p-button-warning mr-2"
          onClick={() => editGroup(rowData)}
        />
        <Button
          icon="pi pi-trash"
          className="p-button-rounded p-button-danger mr-2"
          onClick={() => deleteGroup(rowData)}
        />
        <Button
          icon="pi pi-whatsapp"
          className="p-button-rounded p-button-success"
          onClick={() => openBroadcastDialogForRow(rowData)}
          tooltip="Broadcast to this Group"
        />
      </React.Fragment>
    );
  };

  const header = (
    <div className="flex justify-content-between">
      <h4 className="m-0">Manage Groups</h4>
      <span className="p-input-icon-left">
        <i className="pi pi-search" />
        <InputText
          type="search"
          onInput={(e) => setGlobalFilter(e.target.value)}
          placeholder="Search..."
        />
      </span>
    </div>
  );

  // Dialog footer for Create/Update
  const groupDialogFooter = (
    <React.Fragment>
      <Button
        label="Cancel"
        icon="pi pi-times"
        className="p-button-text"
        onClick={hideDialog}
      />
      <Button
        label="Save"
        icon="pi pi-check"
        className="p-button-text"
        onClick={saveGroup}
      />
    </React.Fragment>
  );

  // Broadcast dialog footer
  const broadcastDialogFooter = (
    <React.Fragment>
      <Button
        label="Cancel"
        icon="pi pi-times"
        className="p-button-text"
        onClick={hideBroadcastDialog}
      />
      <Button
        label="Send"
        icon="pi pi-check"
        className="p-button-text"
        onClick={confirmBroadcast}
      />
    </React.Fragment>
  );

  return (
    <div className="card">
      <Toolbar className="mb-4" left={leftToolbarTemplate} right={rightToolbarTemplate} />
      <DataTable
        ref={dt}
        value={groups}
        selection={selectedGroups}
        onSelectionChange={(e) => setSelectedGroups(e.value)}
        dataKey="id"
        paginator
        rows={10}
        rowsPerPageOptions={[5, 10, 25]}
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} groups"
        globalFilter={globalFilter}
        header={header}
        responsiveLayout="scroll"
      >
        {/* Enable multi-row selection */}
        <Column selectionMode="multiple" exportable={false} style={{ width: '3em' }}></Column>

        <Column field="id" header="ID" sortable style={{ minWidth: '5rem' }}></Column>
        <Column field="groupId" header="Group ID" sortable style={{ minWidth: '8rem' }}></Column>
        <Column field="name" header="Name" sortable style={{ minWidth: '10rem' }}></Column>
        <Column field="description" header="Description" style={{ minWidth: '12rem' }}></Column>
        <Column
          field="creator.phoneNumber"
          header="Creator Phone"
          style={{ minWidth: '10rem' }}
        ></Column>
        <Column
          header="Participants"
          body={(rowData) => rowData.participants.length}
          style={{ minWidth: '8rem' }}
        />
        <Column body={actionBodyTemplate} exportable={false} style={{ minWidth: '10rem' }} />
      </DataTable>

      {/* Create / Update Dialog */}
      <Dialog
        visible={groupDialog}
        style={{ width: '450px' }}
        header={isEditMode ? 'Edit Group' : 'New Group'}
        modal
        className="p-fluid"
        footer={groupDialogFooter}
        onHide={hideDialog}
      >
        <div className="field">
          <label htmlFor="groupId">Group ID</label>
          <InputText
            id="groupId"
            value={currentGroup.groupId}
            onChange={(e) => setCurrentGroup({ ...currentGroup, groupId: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="name">Name</label>
          <InputText
            id="name"
            value={currentGroup.name}
            onChange={(e) => setCurrentGroup({ ...currentGroup, name: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="description">Description</label>
          <InputTextarea
            id="description"
            value={currentGroup.description}
            onChange={(e) => setCurrentGroup({ ...currentGroup, description: e.target.value })}
          />
        </div>
        {/* createdBy could be a dropdown if referencing PhoneNumber IDs */}
      </Dialog>

      {/* Broadcast Dialog */}
      <Dialog
        visible={broadcastDialog}
        style={{ width: '450px' }}
        header="Broadcast WhatsApp Message"
        modal
        className="p-fluid"
        footer={broadcastDialogFooter}
        onHide={hideBroadcastDialog}
      >
        <div className="field">
          <label htmlFor="messageText">Message Text</label>
          <InputTextarea
            id="messageText"
            value={broadcastMessage}
            onChange={(e) => setBroadcastMessage(e.target.value)}
            rows={4}
          />
        </div>
      </Dialog>
    </div>
  );
}
