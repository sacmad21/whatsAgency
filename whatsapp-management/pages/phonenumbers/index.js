// /pages/phoneNumber/index.jsx
import React, { useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/router';
import { Button } from 'primereact/button';
import { Toolbar } from 'primereact/toolbar';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown'; 
import { Toast } from 'primereact/toast';

import 'primeicons/primeicons.css';
import 'primereact/resources/primereact.min.css';
import 'primereact/resources/themes/saga-blue/theme.css'; // Or your chosen theme
import 'primeflex/primeflex.css';

export default function PhoneNumberPage() {
  const [phoneNumbers, setPhoneNumbers] = useState([]);
  const [selectedPhoneNumbers, setSelectedPhoneNumbers] = useState(null);
  const [globalFilter, setGlobalFilter] = useState('');
  const [visibleCreate, setVisibleCreate] = useState(false);
  const [visibleEdit, setVisibleEdit] = useState(false);
  const [formData, setFormData] = useState({});
  const [whatsAppDialog, setWhatsAppDialog] = useState(false);
  const [whatsAppData, setWhatsAppData] = useState({ message: '' });

  const toast = useRef(null);
  const dt = useRef(null);


  const router = useRouter();


  // *** 1. Fetch PhoneNumber Data ***
  const fetchPhoneNumbers = async () => {
    const res = await fetch('/api/phoneNumber');
    const data = await res.json();
    setPhoneNumbers(data);
  };

  useEffect(() => {
    fetchPhoneNumbers();
  }, []);

  // *** 2. Toolbar Actions ***
  const leftToolbarTemplate = () => {
    return (
      <React.Fragment>
        <Button
          label="New"
          icon="pi pi-plus"
          className="p-button-success mr-2"
          onClick={() => {
            setFormData({ phoneNumber: '', status: '', twoStepVerificationStatus: '' });
            setVisibleCreate(true);
          }}
        />
      </React.Fragment>
    );
  };

  const rightToolbarTemplate = () => {
    return (
      <React.Fragment>
        <Button
          label="WhatsApp Broadcast"
          icon="pi pi-send"
          className="p-button-help"
          onClick={() => handleWhatsAppBroadcast()}
          disabled={!selectedPhoneNumbers || selectedPhoneNumbers.length === 0}
        />
      </React.Fragment>
    );
  };

  // *** 3. CRUD Handlers ***
  const createPhoneNumber = async () => {
    await fetch('/api/phoneNumber', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    setVisibleCreate(false);
    toast.current.show({ severity: 'success', summary: 'Created' });
    fetchPhoneNumbers();
  };

  const updatePhoneNumber = async () => {
    await fetch(`/api/phoneNumber/${formData.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    });
    setVisibleEdit(false);
    toast.current.show({ severity: 'success', summary: 'Updated' });
    fetchPhoneNumbers();
  };

  const deletePhoneNumber = async (id) => {
    if (!window.confirm('Are you sure you want to delete this phone number?')) return;
    await fetch(`/api/phoneNumber/${id}`, { method: 'DELETE' });
    toast.current.show({ severity: 'info', summary: 'Deleted' });
    fetchPhoneNumbers();
  };


  const sendWhatsAppMessage = async () => {
    await fetch('/api/phoneNumber/whatsapp/sendMessage', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(whatsAppData),
    });
    toast.current.show({ severity: 'success', summary: 'Message Sent' });
    setWhatsAppDialog(false);
  };



  // *** 4. WhatsApp Handlers ***
  const handleWhatsAppSingle = (rowData) => {
    // Example: open a dialog to send a message
    setWhatsAppData({ ...whatsAppData, id: rowData.id, message: '', tonumber:rowData.phoneNumber, broadcast:false });
    setWhatsAppDialog(true);
  };



  const handleWhatsAppBroadcast = async () => {
    if (!selectedPhoneNumbers || selectedPhoneNumbers.length === 0) {
      toast.current.show({ severity: 'warn', summary: 'No Selection', detail: 'Please select contacts to broadcast.' });
      return;
    }
    const phoneNumbers = selectedPhoneNumbers.map((contact) => contact.phoneNumber); // Extract phone numbers
    const phoneNumbersIds = selectedPhoneNumbers.map((contact) => contact.id); // Extract phone numbers
    
    setWhatsAppData({ ...whatsAppData, phoneNumbers, phoneNumbersIds, message: '', broadcast:true }); // Prepare broadcast data
    setWhatsAppDialog(true); // Open dialog to collect message
  };





  const sendBroadcastMessage = async () => {
    try {
      const response = await fetch('/api/phoneNumber/whatsapp/broadcast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          phoneNumbersIds: whatsAppData.phoneNumbersIds, // List of selected phone numbers
          phoneNumbers: whatsAppData.phoneNumbers, // List of selected phone numbers
          message: whatsAppData.message, // Broadcast message
        }),
      });
  
      const result = await response.json();
  
      if (result.success) {
        toast.current.show({ severity: 'success', summary: 'Broadcast Sent', detail: `${result.sentCount} messages sent.` });
      } else {
        toast.current.show({ severity: 'error', summary: 'Broadcast Failed', detail: result.error || 'Unknown error occurred.' });
      }
  
      setWhatsAppDialog(false); // Close dialog
    } catch (error) {
      console.error(error);
      toast.current.show({ severity: 'error', summary: 'Error', detail: 'Failed to send broadcast.' });
    }
  };





  // *** 5. DataTable Column Templates ***
  const actionBodyTemplate = (rowData) => {
    return (
      <React.Fragment>
        <Button
          icon="pi pi-pencil"
          className="p-button-rounded p-button-warning mr-2"
          onClick={() => {
            setFormData(rowData);
            setVisibleEdit(true);
          }}
        />
        <Button
          icon="pi pi-trash"
          className="p-button-rounded p-button-danger mr-2"
          onClick={() => deletePhoneNumber(rowData.id)}
        />
        <Button
          icon="pi pi-send"
          className="p-button-rounded p-button-success"
          onClick={() => handleWhatsAppSingle(rowData)}
        />
      </React.Fragment>
    );
  };

  // *** 6. Render ***
  const header = (
    <div className="flex flex-column md:flex-row md:justify-content-between md:align-items-center">
      <h5 className="m-0">Manage Phone Numbers</h5>
      <span className="p-input-icon-left">
        <i className="pi pi-search" />
        <InputText type="search" onInput={(e) => setGlobalFilter(e.target.value)} placeholder="Search..." />
      </span>
    </div>
  );

  return (
    <div className="p-mx-2 p-my-4">
      <Toast ref={toast} />

      <div className="card">
        <Toolbar className="mb-4" left={leftToolbarTemplate} right={rightToolbarTemplate}></Toolbar>

        <DataTable
          ref={dt}
          value={phoneNumbers}
          selection={selectedPhoneNumbers}
          onSelectionChange={(e) => setSelectedPhoneNumbers(e.value)}
          dataKey="id"
          paginator
          rows={10}
          rowsPerPageOptions={[5, 10, 25]}
          paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
          currentPageReportTemplate="Showing {first} to {last} of {totalRecords} phoneNumbers"
          globalFilter={globalFilter}
          header={header}
        >
          <Column selectionMode="multiple" exportable={false} style={{ width: '3em' }}></Column>
          <Column field="id" header="ID" sortable style={{ minWidth: '4rem' }}></Column>
          <Column field="phoneNumber" header="Phone Number" sortable style={{ minWidth: '12rem' }}></Column>
          <Column field="status" header="Status" sortable style={{ minWidth: '10rem' }}></Column>
          <Column field="twoStepVerificationStatus" header="2FA Status" sortable style={{ minWidth: '12rem' }}></Column>
          <Column field="createdAt" header="Created At" style={{ minWidth: '12rem' }}></Column>
          <Column field="updatedAt" header="Updated At" style={{ minWidth: '12rem' }}></Column>
          <Column body={actionBodyTemplate} exportable={false} style={{ minWidth: '12rem' }}></Column>
        </DataTable>
      </div>

      {/* Create Dialog */}
      <Dialog
        visible={visibleCreate}
        style={{ width: '450px' }}
        header="Create Phone Number"
        modal
        onHide={() => setVisibleCreate(false)}
      >
        <div className="field">
          <label htmlFor="phoneNumber">Phone Number</label>
          <InputText
            id="phoneNumber"
            value={formData.phoneNumber}
            onChange={(e) => setFormData({ ...formData, phoneNumber: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="status">Status</label>
          <Dropdown
            id="status"
            value={formData.status}
            options={['REGISTERED', 'UNREGISTERED', 'BLOCKED', 'PENDING'].map((v) => ({ label: v, value: v }))}
            onChange={(e) => setFormData({ ...formData, status: e.value })}
            placeholder="Select Status"
          />
        </div>
        <div className="field">
          <label htmlFor="twoStep">2FA Status</label>
          <Dropdown
            id="twoStep"
            value={formData.twoStepVerificationStatus}
            options={['ENABLED', 'DISABLED'].map((v) => ({ label: v, value: v }))}
            onChange={(e) => setFormData({ ...formData, twoStepVerificationStatus: e.value })}
            placeholder="Select Two-Step Verification Status"
          />
        </div>
        <div className="flex justify-content-end mt-3">
          <Button label="Cancel" icon="pi pi-times" onClick={() => setVisibleCreate(false)} className="p-button-text" />
          <Button label="Save" icon="pi pi-check" onClick={createPhoneNumber} autoFocus />
        </div>
      </Dialog>

      {/* Edit Dialog */}
      <Dialog
        visible={visibleEdit}
        style={{ width: '450px' }}
        header="Edit Phone Number"
        modal
        onHide={() => setVisibleEdit(false)}
      >
        <div className="field">
          <label>ID</label>
          <InputText value={formData.id} disabled />
        </div>
        <div className="field">
          <label htmlFor="phoneNumber">Phone Number</label>
          <InputText
            id="phoneNumber"
            value={formData.phoneNumber}
            onChange={(e) => setFormData({ ...formData, phoneNumber: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="status">Status</label>
          <Dropdown
            id="status"
            value={formData.status}
            options={['REGISTERED', 'UNREGISTERED', 'BLOCKED', 'PENDING'].map((v) => ({ label: v, value: v }))}
            onChange={(e) => setFormData({ ...formData, status: e.value })}
            placeholder="Select Status"
          />
        </div>
        <div className="field">
          <label htmlFor="twoStep">2FA Status</label>
          <Dropdown
            id="twoStep"
            value={formData.twoStepVerificationStatus}
            options={['ENABLED', 'DISABLED'].map((v) => ({ label: v, value: v }))}
            onChange={(e) => setFormData({ ...formData, twoStepVerificationStatus: e.value })}
            placeholder="Select Two-Step Verification Status"
          />
        </div>
        <div className="flex justify-content-end mt-3">
          <Button label="Cancel" icon="pi pi-times" onClick={() => setVisibleEdit(false)} className="p-button-text" />
          <Button label="Update" icon="pi pi-check" onClick={updatePhoneNumber} autoFocus />
        </div>
      </Dialog>

      {/* WhatsApp Dialog */}
      <Dialog
        visible={whatsAppDialog}
        style={{ width: '450px' }}
        header="Send WhatsApp Message"
        modal
        onHide={() => setWhatsAppDialog(false)}
      >
        <div className="field">
          <label htmlFor="message">Message</label>
          <InputText
            id="message"
            value={whatsAppData.message}
            onChange={(e) => setWhatsAppData({ ...whatsAppData, message: e.target.value })}
          />
        </div>
        <div className="flex justify-content-end mt-3">
          <Button  label="Cancel" icon="pi pi-times" onClick={() => setWhatsAppDialog(false)} className="p-button-text" />
          <Button visible={!whatsAppData.broadcast} label="Send" icon="pi pi-check" onClick={sendWhatsAppMessage}  />
          <Button visible={whatsAppData.broadcast} label="Broadcast" icon="pi pi-check" onClick={sendBroadcastMessage}  />
          
        </div>
      </Dialog>
      


    </div>
  );
}
