import React, { useState, useEffect } from 'react';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Calendar } from 'primereact/calendar';
import { Button } from 'primereact/button';

export default function ParticipantDialog({ visible, onHide, onSave, initialData, groupId }) {
  const [participant, setParticipant] = useState(initialData || {});
  const [roles] = useState([
    { label: 'Admin', value: 'ADMIN' },
    { label: 'Member', value: 'MEMBER' },
  ]);
  const [availablePhoneNumbers, setAvailablePhoneNumbers] = useState([]);

  // Fetch phone numbers when dialog is opened
  useEffect(() => {
    if (visible) fetchPhoneNumbers();
  }, [visible]);

  useEffect(() => {
    setParticipant(initialData || { groupId, role: '', joinedAt: new Date() });
  }, [initialData, groupId]);

  const fetchPhoneNumbers = async () => {
    try {
      const res = await fetch('/api/phone-numbers'); // Example endpoint to fetch phone numbers
      const data = await res.json();
      setAvailablePhoneNumbers(
        data.map((phone) => ({ label: phone.phoneNumber, value: phone.id }))
      );
    } catch (error) {
      console.error('Error fetching phone numbers:', error);
    }
  };

  const handleSave = () => {
    onSave(participant);
  };

  return (
    <Dialog
      visible={visible}
      style={{ width: '450px' }}
      header={initialData ? 'Edit Participant' : 'Add Participant'}
      modal
      className="p-fluid"
      footer={
        <>
          <Button
            label="Cancel"
            icon="pi pi-times"
            className="p-button-text"
            onClick={onHide}
          />
          <Button
            label="Save"
            icon="pi pi-check"
            className="p-button-text"
            onClick={handleSave}
          />
        </>
      }
      onHide={onHide}
    >
      {/* groupId (read-only) */}
      <div className="field">
        <label htmlFor="groupId">Group ID</label>
        <InputText id="groupId" value={participant.groupId} disabled />
      </div>

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

      {/* role (dropdown) */}
      <div className="field">
        <label htmlFor="role">Role</label>
        <Dropdown
          id="role"
          value={participant.role}
          options={roles}
          onChange={(e) =>
            setParticipant({ ...participant, role: e.value })
          }
          placeholder="Select a Role"
        />
      </div>

      {/* joinedAt (datetime picker) */}
      <div className="field">
        <label htmlFor="joinedAt">Joined At</label>
        <Calendar
          id="joinedAt"
          value={new Date(participant.joinedAt)}
          onChange={(e) =>
            setParticipant({ ...participant, joinedAt: e.value })
          }
          showTime
          dateFormat="yy-mm-dd"
        />
      </div>
    </Dialog>
  );
}
