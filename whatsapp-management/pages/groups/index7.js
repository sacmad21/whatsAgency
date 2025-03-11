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



export default function GroupManagement() {
  const [groups, setGroups] = useState([]);
  const [participants, setParticipants] = useState([]);
  const [selectedGroup, setSelectedGroup] = useState(null);
  const [groupDialog, setGroupDialog] = useState(false);
  const [participantDialog, setParticipantDialog] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [newGroup, setNewGroup] = useState({
    groupId: '',
    name: '',
    description: '',
    createdBy: 1, // Replace with a dynamic user ID dropdown if applicable.
  });
  const [newParticipant, setNewParticipant] = useState({
    participantId: '',
    role: 'MEMBER',
  });
  const [roles] = useState([{ label: 'Admin', value: 'ADMIN' }, { label: 'Member', value: 'MEMBER' }]);

  const dt = useRef(null);

  useEffect(() => {
    fetchGroups();
  }, []);

  // Fetch all groups
  const fetchGroups = async () => {
    const res = await fetch('/api/groups');
    const data = await res.json();
    setGroups(data);
  };

  // Fetch participants for a group
  const fetchParticipants = async (groupId) => {
    const res = await fetch(`/api/group-participants?groupId=${groupId}`);
    const data = await res.json();
    setParticipants(data);
    setParticipantDialog(true);
  };

  // Save Group (Add or Update)
  const saveGroup = async () => {
    const url = isEditMode ? `/api/groups/${newGroup.id}` : '/api/groups';
    const method = isEditMode ? 'PUT' : 'POST';

    await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newGroup),
    });

    fetchGroups();
    setGroupDialog(false);
  };

  // Delete Group
  const deleteGroup = async (groupId) => {
    if (window.confirm('Are you sure you want to delete this group?')) {
      await fetch(`/api/groups/${groupId}`, { method: 'DELETE' });
      fetchGroups();
    }
  };

  // Add Participant
  const addParticipant = async () => {
    await fetch('/api/group-participants', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...newParticipant, groupId: selectedGroup.id }),
    });

    fetchParticipants(selectedGroup.id);
    setNewParticipant({ participantId: '', role: 'MEMBER' });
  };

  // Delete Participant
  const deleteParticipant = async (participantId) => {
    if (window.confirm('Are you sure you want to delete this participant?')) {
      await fetch(`/api/group-participants/${participantId}`, { method: 'DELETE' });
      fetchParticipants(selectedGroup.id);
    }
  };

  // Open Add Group Dialog
  const openNewGroupDialog = () => {
    setNewGroup({ groupId: '', name: '', description: '', createdBy: 1 });
    setIsEditMode(false);
    setGroupDialog(true);
  };

  // Open Edit Group Dialog
  const openEditGroupDialog = (group) => {
    setNewGroup(group);
    setIsEditMode(true);
    setGroupDialog(true);
  };

  const header = (
    <div className="flex justify-content-between">
      <h4 className="m-0">Manage Groups</h4>
      <Button label="Add Group" icon="pi pi-plus" className="p-button-success" onClick={openNewGroupDialog} />
    </div>
  );

  const actionBodyTemplate = (rowData) => (
    <div className="flex gap-2">
      <Button
        icon="pi pi-pencil"
        className="p-button-rounded p-button-warning"
        onClick={() => openEditGroupDialog(rowData)}
      />
      <Button
        icon="pi pi-trash"
        className="p-button-rounded p-button-danger"
        onClick={() => deleteGroup(rowData.id)}
      />
      <Button
        icon="pi pi-users"
        className="p-button-rounded p-button-info"
        onClick={() => {
          setSelectedGroup(rowData);
          fetchParticipants(rowData.id);
        }}
      />
    </div>
  );

  const participantActionTemplate = (rowData) => (
    <Button
      icon="pi pi-trash"
      className="p-button-rounded p-button-danger"
      onClick={() => deleteParticipant(rowData.id)}
    />
  );

  const groupDialogFooter = (
    <div>
      <Button label="Cancel" icon="pi pi-times" className="p-button-text" onClick={() => setGroupDialog(false)} />
      <Button label="Save" icon="pi pi-check" className="p-button-text" onClick={saveGroup} />
    </div>
  );

  const participantDialogFooter = (
    <div>
      <Button label="Close" icon="pi pi-times" className="p-button-text" onClick={() => setParticipantDialog(false)} />
    </div>
  );

  return (
    <div className="card">
      <Toolbar className="mb-4" left={header} />
      <DataTable
        ref={dt}
        value={groups}
        paginator
        rows={10}
        globalFilter=""
        header="Manage Groups"
        responsiveLayout="scroll"
      >
        <Column field="id" header="ID" sortable></Column>
        <Column field="name" header="Name" sortable></Column>
        <Column field="description" header="Description"></Column>
        <Column header="Actions" body={actionBodyTemplate}></Column>
      </DataTable>

      {/* Group Dialog */}
      <Dialog
        visible={groupDialog}
        header={isEditMode ? 'Edit Group' : 'New Group'}
        modal
        className="p-fluid"
        footer={groupDialogFooter}
        onHide={() => setGroupDialog(false)}
      >
        <div className="field">
          <label htmlFor="groupId">Group ID</label>
          <InputText
            id="groupId"
            value={newGroup.groupId}
            onChange={(e) => setNewGroup({ ...newGroup, groupId: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="name">Name</label>
          <InputText id="name" value={newGroup.name} onChange={(e) => setNewGroup({ ...newGroup, name: e.target.value })} />
        </div>
        <div className="field">
          <label htmlFor="description">Description</label>
          <InputTextarea
            id="description"
            value={newGroup.description}
            onChange={(e) => setNewGroup({ ...newGroup, description: e.target.value })}
          />
        </div>
      </Dialog>

      {/* Participant Dialog */}
      <Dialog
        visible={participantDialog}
        header={`Participants for ${selectedGroup?.name}`}
        modal
        className="p-fluid"
        footer={participantDialogFooter}
        onHide={() => setParticipantDialog(false)}
      >
        <DataTable value={participants} paginator rows={5} responsiveLayout="scroll">
          <Column field="participant.phoneNumber" header="Phone Number"></Column>
          <Column field="role" header="Role"></Column>
          <Column field="joinedAt" header="Joined At"></Column>
          <Column header="Actions" body={participantActionTemplate}></Column>
        </DataTable>

        <h5>Add New Participant</h5>
        <div className="field">
          <label htmlFor="participantId">Participant ID</label>
          <InputText
            id="participantId"
            value={newParticipant.participantId}
            onChange={(e) => setNewParticipant({ ...newParticipant, participantId: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="role">Role</label>
          <Dropdown
            id="role"
            value={newParticipant.role}
            options={roles}
            onChange={(e) => setNewParticipant({ ...newParticipant, role: e.value })}
            placeholder="Select Role"
          />
        </div>
        <Button label="Add Participant" icon="pi pi-check" onClick={addParticipant} />
      </Dialog>
    </div>
  );
}
