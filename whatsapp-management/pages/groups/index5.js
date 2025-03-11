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
  const [participants, setParticipants] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [globalFilter, setGlobalFilter] = useState('');

  const [groupDialog, setGroupDialog] = useState(false);
  const [participantDialog, setParticipantDialog] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);

  const [currentGroup, setCurrentGroup] = useState({});
  const [currentParticipant, setCurrentParticipant] = useState({});
  const [availableParticipants, setAvailableParticipants] = useState([]);

  const dt = useRef(null);

  useEffect(() => {
    fetchGroups();
    fetchAvailableParticipants();
  }, []);

  async function fetchGroups() {
    const res = await fetch('/api/groups');
    const data = await res.json();
    setGroups(data);
  }

  async function fetchAvailableParticipants() {
    const res = await fetch('/api/users'); // Assuming users are stored in /api/users
    const data = await res.json();
    setAvailableParticipants(data);
  }

  async function fetchParticipants(groupId) {
    const res = await fetch(`/api/group-participants?groupId=${groupId}`);
    const data = await res.json();
    setParticipants(data);
    setParticipantDialog(true);
  }

  function openNewGroup() {
    setCurrentGroup({ name: '', description: '' });
    setIsEditMode(false);
    setGroupDialog(true);
  }

  function openEditGroup(rowData) {
    setCurrentGroup(rowData);
    setIsEditMode(true);
    setGroupDialog(true);
  }

  function hideGroupDialog() {
    setGroupDialog(false);
  }

  function hideParticipantDialog() {
    setParticipantDialog(false);
  }

  async function saveGroup() {
    if (isEditMode) {
      await fetch(`/api/groups/${currentGroup.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentGroup),
      });
    } else {
      await fetch('/api/groups', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentGroup),
      });
    }
    fetchGroups();
    setGroupDialog(false);
  }

  async function deleteGroup(rowData) {
    if (window.confirm(`Are you sure you want to delete the group "${rowData.name}"?`)) {
      await fetch(`/api/groups/${rowData.id}`, { method: 'DELETE' });
      fetchGroups();
    }
  }

  async function addParticipantToGroup() {
    await fetch('/api/group-participants', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentParticipant),
    });
    fetchParticipants(currentParticipant.groupId);
  }

  async function removeParticipant(participantId) {
    await fetch(`/api/group-participants/${participantId}`, { method: 'DELETE' });
    fetchParticipants(selectedGroup.id);
  }

  const participantActionsTemplate = (rowData) => {
    return (
      <Button
        icon="pi pi-trash"
        className="p-button-rounded p-button-danger"
        onClick={() => removeParticipant(rowData.id)}
        tooltip="Remove Participant"
      />
    );
  };

  const groupActionsTemplate = (rowData) => {
    return (
      <>
        <Button
          icon="pi pi-pencil"
          className="p-button-rounded p-button-warning mr-2"
          onClick={() => openEditGroup(rowData)}
          tooltip="Edit Group"
        />
        <Button
          icon="pi pi-trash"
          className="p-button-rounded p-button-danger mr-2"
          onClick={() => deleteGroup(rowData)}
          tooltip="Delete Group"
        />
        <Button
          icon="pi pi-users"
          className="p-button-rounded p-button-info"
          onClick={() => fetchParticipants(rowData.id)}
          tooltip="Manage Participants"
        />
      </>
    );
  };

  const groupDialogFooter = (
    <>
      <Button
        label="Cancel"
        icon="pi pi-times"
        className="p-button-text"
        onClick={hideGroupDialog}
      />
      <Button
        label="Save"
        icon="pi pi-check"
        className="p-button-text"
        onClick={saveGroup}
      />
    </>
  );

  const participantDialogFooter = (
    <>
      <Button
        label="Close"
        icon="pi pi-times"
        className="p-button-text"
        onClick={hideParticipantDialog}
      />
    </>
  );

  const toolbarLeftTemplate = () => (
    <Button
      label="New Group"
      icon="pi pi-plus"
      className="p-button-success"
      onClick={openNewGroup}
    />
  );

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

  return (
    <div className="card">
      <Toolbar className="mb-4" left={toolbarLeftTemplate} />
      <DataTable
        ref={dt}
        value={groups}
        globalFilter={globalFilter}
        dataKey="id"
        paginator
        rows={10}
        header={header}
        responsiveLayout="scroll"
      >
        <Column field="id" header="ID" />
        <Column field="name" header="Name" sortable />
        <Column field="description" header="Description" />
        <Column header="Actions" body={groupActionsTemplate} />
      </DataTable>

      {/* Group Dialog */}
      <Dialog
        visible={groupDialog}
        style={{ width: '450px' }}
        header={isEditMode ? 'Edit Group' : 'New Group'}
        modal
        footer={groupDialogFooter}
        onHide={hideGroupDialog}
      >
        <div className="field">
          <label htmlFor="name">Name</label>
          <InputText
            id="name"
            value={currentGroup.name}
            onChange={(e) =>
              setCurrentGroup({ ...currentGroup, name: e.target.value })
            }
          />
        </div>
        <div className="field">
          <label htmlFor="description">Description</label>
          <InputTextarea
            id="description"
            value={currentGroup.description}
            onChange={(e) =>
              setCurrentGroup({ ...currentGroup, description: e.target.value })
            }
          />
        </div>
      </Dialog>

      {/* Participant Dialog */}
      <Dialog
        visible={participantDialog}
        style={{ width: '600px' }}
        header="Manage Participants"
        modal
        footer={participantDialogFooter}
        onHide={hideParticipantDialog}
      >
        <DataTable value={participants} dataKey="id" responsiveLayout="scroll">
          <Column field="participant.phoneNumber" header="Phone Number" />
          <Column field="role" header="Role" />
          <Column header="Actions" body={participantActionsTemplate} />
        </DataTable>
        <div className="field mt-4">
          <label htmlFor="participant">Add Participant</label>
          <Dropdown
            id="participant"
            value={currentParticipant.participantId}
            options={availableParticipants}
            onChange={(e) =>
              setCurrentParticipant({
                ...currentParticipant,
                participantId: e.value,
                groupId: selectedGroup.id,
              })
            }
            optionLabel="phoneNumber"
            placeholder="Select a participant"
          />
          <Button
            label="Add"
            icon="pi pi-plus"
            className="mt-2"
            onClick={addParticipantToGroup}
          />
        </div>
      </Dialog>
    </div>
  );
}
