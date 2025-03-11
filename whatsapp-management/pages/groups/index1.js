import React, { useEffect, useRef, useState } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { InputTextarea } from 'primereact/inputtextarea';
import { TabView, TabPanel } from 'primereact/tabview';

import 'primereact/resources/themes/saga-blue/theme.css';    // or your preferred theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';

export default function GroupList() {
  const [groups, setGroups] = useState([]);
  const [participants, setParticipants] = useState([]);
  const [selectedGroups, setSelectedGroups] = useState(null);
  const [globalFilter, setGlobalFilter] = useState('');

  const [participantDialog, setParticipantDialog] = useState(false);
  const [broadcastDialog, setBroadcastDialog] = useState(false);
  const [broadcastType, setBroadcastType] = useState('Text');
  const [broadcastMessage, setBroadcastMessage] = useState('');
  const [templateName, setTemplateName] = useState('');
  const [templateVariables, setTemplateVariables] = useState('');
  const [mediaPath, setMediaPath] = useState('');

  const dt = useRef(null);

  useEffect(() => {
    fetchGroups();
  }, []);

  async function fetchGroups() {
    const res = await fetch('/api/groups');
    const data = await res.json();
    setGroups(data);
  }

  async function fetchParticipants(groupId) {
    const res = await fetch(`/api/group-participants?groupId=${groupId}`);
    const data = await res.json();
    setParticipants(data);
    setParticipantDialog(true);
  }

  function hideParticipantDialog() {
    setParticipantDialog(false);
  }

  function hideBroadcastDialog() {
    setBroadcastDialog(false);
    setBroadcastType('Text');
    setBroadcastMessage('');
    setTemplateName('');
    setTemplateVariables('');
    setMediaPath('');
  }

  const openBroadcastDialog = (rowData) => {
    setSelectedGroups([rowData]);
    setBroadcastDialog(true);
  };

  const sendBroadcast = async () => {
    const group = selectedGroups[0];

    if (broadcastType === 'Text') {
      await fetch('/api/whatsapp/broadcast-text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ groupId: group.id, messageText: broadcastMessage }),
      });
    } else if (broadcastType === 'Template') {
      await fetch('/api/whatsapp/broadcast-template', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          groupId: group.id,
          templateName,
          templateVariables: JSON.parse(templateVariables),
        }),
      });
    } else if (broadcastType === 'Media') {
      await fetch('/api/whatsapp/broadcast-media', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ groupId: group.id, mediaPath, mediaType: 'image', caption: broadcastMessage }),
      });
    }

    alert('Broadcast sent successfully!');
    hideBroadcastDialog();
  };

  const participantBodyTemplate = (rowData) => {
    return (
      <Button
        label="View Participants"
        icon="pi pi-users"
        className="p-button-info"
        onClick={() => fetchParticipants(rowData.id)}
      />
    );
  };

  const actionBodyTemplate = (rowData) => {
    return (
      <Button
        icon="pi pi-whatsapp"
        label="Broadcast"
        className="p-button-success"
        onClick={() => openBroadcastDialog(rowData)}
      />
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

  return (
    <div className="card">
      <Toolbar className="mb-4" />
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
      >
        <Column field="id" header="ID" sortable />
        <Column field="name" header="Name" sortable />
        <Column field="description" header="Description" />
        <Column header="Participants" body={participantBodyTemplate} />
        <Column header="Actions" body={actionBodyTemplate} />
      </DataTable>

      {/* Participant Management Dialog */}
      <Dialog
        visible={participantDialog}
        style={{ width: '600px' }}
        header="Participants"
        modal
        onHide={hideParticipantDialog}
      >
        <DataTable value={participants} dataKey="id">
          <Column field="participant.phoneNumber" header="Phone Number" />
          <Column field="role" header="Role" />
          <Column field="joinedAt" header="Joined At" />
        </DataTable>
      </Dialog>

      {/* Broadcast Dialog */}
      <Dialog
        visible={broadcastDialog}
        style={{ width: '600px' }}
        header="Broadcast Message"
        modal
        onHide={hideBroadcastDialog}
      >
        <TabView>
          <TabPanel header="Text Message">
            <div className="field">
              <label htmlFor="messageText">Message Text</label>
              <InputTextarea
                id="messageText"
                value={broadcastMessage}
                onChange={(e) => setBroadcastMessage(e.target.value)}
                rows={4}
              />
            </div>
          </TabPanel>
          <TabPanel header="Template Message">
            <div className="field">
              <label htmlFor="templateName">Template Name</label>
              <InputText
                id="templateName"
                value={templateName}
                onChange={(e) => setTemplateName(e.target.value)}
              />
            </div>
            <div className="field">
              <label htmlFor="templateVariables">Template Variables (JSON)</label>
              <InputTextarea
                id="templateVariables"
                value={templateVariables}
                onChange={(e) => setTemplateVariables(e.target.value)}
                rows={4}
              />
            </div>
          </TabPanel>
          <TabPanel header="Media Message">
            <div className="field">
              <label htmlFor="mediaPath">Media Path</label>
              <InputText
                id="mediaPath"
                value={mediaPath}
                onChange={(e) => setMediaPath(e.target.value)}
              />
            </div>
            <div className="field">
              <label htmlFor="caption">Caption</label>
              <InputTextarea
                id="caption"
                value={broadcastMessage}
                onChange={(e) => setBroadcastMessage(e.target.value)}
                rows={4}
              />
            </div>
          </TabPanel>
        </TabView>
        <Button label="Send Broadcast" icon="pi pi-check" onClick={sendBroadcast} />
      </Dialog>
    </div>
  );
}
