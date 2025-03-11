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
import { TabView, TabPanel } from 'primereact/tabview';
import ParticipantTable from '../../components/ParticipantData';

import 'primereact/resources/themes/saga-blue/theme.css';    // or your preferred theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';


export default function GroupList() {
    const [groups, setGroups] = useState([]);
    const [selectedGroup, setSelectedGroup] = useState(null);
    const [selectedGroups, setSelectedGroups] = useState(null);
    const [globalFilter, setGlobalFilter] = useState('');

    const [groupDialog, setGroupDialog] = useState(false);
    const [currentGroup, setCurrentGroup] = useState({});

    const [isEditMode, setIsEditMode] = useState(false);
    const [broadcastDialog, setBroadcastDialog] = useState(false);
    const [broadcastMessage, setBroadcastMessage] = useState('');

    const [templateName, setTemplateName] = useState('');
    const [templateVariables, setTemplateVariables] = useState('');
    const [mediaPath, setMediaPath] = useState('');
    const [showParticipantsDialog, setShowParticipantsDialog] = useState(false);
    const [broadcastType, setBroadcastType] = useState('Text');


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
            createdBy: 2 // Example: might set default or let user pick
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
                    templateLanguage:"en",
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



    const openParticipantsDialog = (group) => {
        setSelectedGroup(group);
        setShowParticipantsDialog(true);
    };

    const hideParticipantsDialog = () => {
        setShowParticipantsDialog(false);
        setSelectedGroup(null);
    };


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
                    icon="pi pi-users"
                    className="p-button-rounded p-button-info mr-2"
                    onClick={() => openParticipantsDialog(rowData)}
                    tooltip="Show Participants"
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
            {/* Broadcast Dialog */}
            <Dialog
                visible={broadcastDialog}
                style={{ width: '600px' }}
                header="Broadcast Message"
                modal
                onHide={hideBroadcastDialog}
            >
                <TabView>
                    <TabPanel header="Text">
                        <div className="field">
                            <label htmlFor="messageText">Message Text</label>
                            <InputTextarea
                                id="messageText"
                                value={broadcastMessage}
                                onChange={(e) => { setBroadcastMessage(e.target.value) ; setBroadcastType("Text"); }}
                                rows={4}
                            />
                        </div>
                    </TabPanel>
                    <TabPanel header="Template">
                        <div className="field">
                            <label htmlFor="templateName">Template Name</label>
                            <InputText
                                id="templateName"
                                value={templateName}
                                onChange={(e) => { setTemplateName(e.target.value); setBroadcastType("Template"); }}
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
                                onChange={(e) => { setMediaPath(e.target.value); setBroadcastType("Media"); }}
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



            {/* Participant Table Dialog */}
            <Dialog
                visible={showParticipantsDialog}
                style={{ width: '800px' }}
                header={`Participants in Group: ${selectedGroup?.name || ''}`}
                modal
                className="p-fluid"
                onHide={hideParticipantsDialog}
            >
                {selectedGroup && (
                    <ParticipantTable groupId={selectedGroup.id} />
                )}
            </Dialog>


        </div>
    );
}
