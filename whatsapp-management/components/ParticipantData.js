import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';


function ParticipantTable({ groupId }) {

  const [participants, setParticipants] = useState([]);
  const [participantDialog, setParticipantDialog] = useState(false);
  const [deleteDialog, setDeleteDialog] = useState(false);
  const [currentParticipant, setCurrentParticipant] = useState({});
  const [isEditMode, setIsEditMode] = useState(false);
  const [participant, setParticipant] = useState({});
  const [availablePhoneNumbers, setAvailablePhoneNumbers] = useState([]);


  const [roles] = useState([
    { label: 'Admin', value: 'ADMIN' },
    { label: 'Member', value: 'MEMBER' },
  ]);


  useEffect(() => {
    fetchParticipants();
    fetchPhoneNumbers();
  }, [groupId]);

  
  const fetchParticipants = async () => {
    try {
      const res = await fetch(`/api/group-participants?groupId=${groupId}`);
      const data = await res.json();
      setParticipants(data);
    } catch (error) {
      console.error('Error fetching participants:', error);
    }
  };

  const fetchPhoneNumbers = async () => {
    try {

      console.log("Fetching all phonenumbers ::: ");
      const res = await fetch('/api/phoneNumber'); // Example endpoint to fetch phone numbers
      const data = await res.json();

      setAvailablePhoneNumbers(
        data.map((phone) => ({ label: phone.phoneNumber, value: phone.id }))
      );

    } catch (error) {
      console.error('Error fetching phone numbers:', error);
    }
  };



  const openNewParticipantDialog = () => {
    setCurrentParticipant({ groupId, participantId: '', role: '' });
    setIsEditMode(false);
    setParticipantDialog(true);
  };

  const openEditParticipantDialog = (participant) => {
    setCurrentParticipant({ ...participant });
    setIsEditMode(true);
    setParticipantDialog(true);
  };

  const hideParticipantDialog = () => {
    setParticipantDialog(false);
  };

  const hideDeleteDialog = () => {
    setDeleteDialog(false);
  };

  const saveParticipant = async () => {
    const url = isEditMode
      ? `/api/group-participants/${currentParticipant.id}`
      : `/api/group-participants`;
    const method = isEditMode ? 'PUT' : 'POST';

    try {
      await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentParticipant),
      });
      fetchParticipants();
      setParticipantDialog(false);
    } catch (error) {
      console.error('Error saving participant:', error);
    }
  };

  const confirmDeleteParticipant = async () => {
    try {
      await fetch(`/api/group-participants/${currentParticipant.id}`, {
        method: 'DELETE',
      });
      fetchParticipants();
      setDeleteDialog(false);
    } catch (error) {
      console.error('Error deleting participant:', error);
    }
  };

  const openDeleteDialog = (participant) => {
    setCurrentParticipant(participant);
    setDeleteDialog(true);
  };

  const actionBodyTemplate = (rowData) => {
    return (
      <React.Fragment>
        <Button
          icon="pi pi-pencil"
          className="p-button-rounded p-button-warning mr-2"
          onClick={() => openEditParticipantDialog(rowData)}
        />
        <Button
          icon="pi pi-trash"
          className="p-button-rounded p-button-danger"
          onClick={() => openDeleteDialog(rowData)}
        />
      </React.Fragment>
    );
  };

  const toolbarTemplate = () => (
    <Button
      label="Add Participant"
      icon="pi pi-plus"
      className="p-button-success"
      onClick={openNewParticipantDialog}
    />
  );

  const participantDialogFooter = (
    <React.Fragment>
      <Button
        label="Cancel"
        icon="pi pi-times"
        className="p-button-text"
        onClick={hideParticipantDialog}
      />
      <Button
        label="Save"
        icon="pi pi-check"
        className="p-button-text"
        onClick={saveParticipant}
      />
    </React.Fragment>
  );

  const deleteDialogFooter = (
    <React.Fragment>
      <Button
        label="No"
        icon="pi pi-times"
        className="p-button-text"
        onClick={hideDeleteDialog}
      />
      <Button
        label="Yes"
        icon="pi pi-check"
        className="p-button-text"
        onClick={confirmDeleteParticipant}
      />
    </React.Fragment>
  );

  return (
    <div className="card">
      <Toolbar className="mb-4" left={toolbarTemplate} />
      <DataTable
        value={participants}
        dataKey="id"
        paginator
        rows={10}
        rowsPerPageOptions={[5, 10, 25]}
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} participants"
        responsiveLayout="scroll"
      >
        <Column field="participant.phoneNumber" header="Phone Number" sortable />
        <Column field="role" header="Role" sortable />
        <Column field="joinedAt" header="Joined At" sortable />
        <Column body={actionBodyTemplate} header="Actions" />
      </DataTable>



      {/* Participant Dialog */}
      <Dialog
        visible={participantDialog}
        style={{ width: '450px' }}
        header={isEditMode ? 'Edit Participant' : 'Add Participant'}
        modal
        className="p-fluid"
        footer={participantDialogFooter}
        onHide={hideParticipantDialog}
      >

        {/* participantId (dropdown) */}
        <div className="field">
          <label htmlFor="participantId">Participant</label>
          <Dropdown
            id="participantId"
            value={participant.participantId}
            options={availablePhoneNumbers}
            onChange={(e) =>
              setParticipant({ ...participant, participantId: e.value })
            }
            placeholder="Select a Phone Number"
          />
        </div>

        <div className="field">
          <label htmlFor="role">Role</label>
          <Dropdown
            id="role"
            value={currentParticipant.role}
            options={roles}
            onChange={(e) =>
              setCurrentParticipant({ ...currentParticipant, role: e.value })
            }
            placeholder="Select a Role"
          />
        </div>
      </Dialog>



      {/* Delete Confirmation Dialog */}
      <Dialog
        visible={deleteDialog}
        style={{ width: '450px' }}
        header="Confirm Delete"
        modal
        footer={deleteDialogFooter}
        onHide={hideDeleteDialog}
      >
        <div className="confirmation-content">
          <i
            className="pi pi-exclamation-triangle mr-3"
            style={{ fontSize: '2rem' }}
          />
          {currentParticipant && (
            <span>
              Are you sure you want to delete participant{' '}
              <b>{currentParticipant.participant?.phoneNumber}</b>?
            </span>
          )}
        </div>
      </Dialog>
    </div>
  );
}

export default ParticipantTable;
