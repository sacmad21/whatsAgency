import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import axios from 'axios';



import 'primereact/resources/themes/saga-blue/theme.css';    // or your preferred theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';


export default function Conversations() {
  const [conversations, setConversations] = useState([]);
  const [selectedConversations, setSelectedConversations] = useState([]);
  const [dialogVisible, setDialogVisible] = useState(false);
  const [dialogType, setDialogType] = useState('create'); // 'create' or 'update'
  const [formData, setFormData] = useState({ phoneNumberId: '', conversationType: '' });
  const [phoneNumbers, setPhoneNumbers] = useState([]);
  const [globalFilter, setGlobalFilter] = useState(null);

  useEffect(() => {
    fetchConversations();
    fetchPhoneNumbers();
  }, []);

  const fetchConversations = async () => {
    const response = await axios.get('/api/conversations');
    setConversations(response.data);
  };

  const fetchPhoneNumbers = async () => {
    const response = await axios.get('/api/phoneNumbers'); // Replace with actual API
    setPhoneNumbers(response.data);
  };

  const saveConversation = async () => {
    if (dialogType === 'create') {
      await axios.post('/api/conversations', formData);
    } else {
      await axios.put('/api/conversations', formData);
    }
    fetchConversations();
    setDialogVisible(false);
  };

  const deleteConversation = async (id) => {
    await axios.delete('/api/conversations', { data: { id } });
    fetchConversations();
  };

  const openCreateDialog = () => {
    setDialogType('create');
    setFormData({ phoneNumberId: '', conversationType: '' });
    setDialogVisible(true);
  };

  const openEditDialog = (conversation) => {
    setDialogType('update');
    setFormData(conversation);
    setDialogVisible(true);
  };

  const toolbarTemplate = () => (
    <React.Fragment>
      <Button label="New Conversation" icon="pi pi-plus" className="p-button-success mr-2" onClick={openCreateDialog} />
      <Button
        label="Delete Selected"
        icon="pi pi-trash"
        className="p-button-danger"
        onClick={() => selectedConversations.forEach((c) => deleteConversation(c.id))}
        disabled={!selectedConversations.length}
      />
    </React.Fragment>
  );

  const actionBodyTemplate = (rowData) => (
    <React.Fragment>
      <Button icon="pi pi-pencil" className="p-button-rounded p-button-success mr-2" onClick={() => openEditDialog(rowData)} />
      <Button icon="pi pi-trash" className="p-button-rounded p-button-danger" onClick={() => deleteConversation(rowData.id)} />
    </React.Fragment>
  );

  return (
    <div className="p-grid">
      <div className="p-col-12">
        <Toolbar className="mb-4" left={toolbarTemplate} />
        <DataTable
          value={conversations}
          selection={selectedConversations}
          onSelectionChange={(e) => setSelectedConversations(e.value)}
          dataKey="id"
          paginator
          rows={10}
          rowsPerPageOptions={[5, 10, 25]}
          paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
          currentPageReportTemplate="Showing {first} to {last} of {totalRecords} conversations"
          globalFilter={globalFilter}
          header={<InputText placeholder="Search..." onInput={(e) => setGlobalFilter(e.target.value)} />}
        >
          <Column selectionMode="multiple" exportable={false}></Column>
          <Column field="id" header="ID" sortable style={{ minWidth: '6rem' }}></Column>
          <Column field="phoneNumber.phoneNumber" header="Phone Number" sortable style={{ minWidth: '10rem' }}></Column>
          <Column field="conversationType" header="Type" sortable style={{ minWidth: '10rem' }}></Column>
          <Column field="createdAt" header="Created At" sortable style={{ minWidth: '12rem' }}></Column>
          <Column field="updatedAt" header="Updated At" sortable style={{ minWidth: '12rem' }}></Column>
          <Column body={actionBodyTemplate} exportable={false} style={{ minWidth: '10rem' }}></Column>
        </DataTable>

        <Dialog
          visible={dialogVisible}
          header={dialogType === 'create' ? 'New Conversation' : 'Edit Conversation'}
          modal
          onHide={() => setDialogVisible(false)}
          footer={
            <React.Fragment>
              <Button label="Cancel" icon="pi pi-times" className="p-button-text" onClick={() => setDialogVisible(false)} />
              <Button label="Save" icon="pi pi-check" className="p-button-text" onClick={saveConversation} />
            </React.Fragment>
          }
        >
          <div className="p-fluid">
            <div className="p-field">
              <label htmlFor="phoneNumberId">Phone Number</label>
              <Dropdown
                id="phoneNumberId"
                value={formData.phoneNumberId}
                options={phoneNumbers.map((p) => ({ label: p.phoneNumber, value: p.id }))}
                onChange={(e) => setFormData({ ...formData, phoneNumberId: e.value })}
                placeholder="Select a phone number"
              />  
            </div>
            <div className="p-field">
              <label htmlFor="conversationType">Conversation Type</label>
              <Dropdown
                id="conversationType"
                value={formData.conversationType}
                options={[
                  { label: 'Incoming', value: 'INCOMING' },
                  { label: 'Outgoing', value: 'OUTGOING' },
                ]}
                onChange={(e) => setFormData({ ...formData, conversationType: e.value })}
                placeholder="Select conversation type"
              />
            </div>
          </div>
        </Dialog>
      </div>
    </div>
  );
}
