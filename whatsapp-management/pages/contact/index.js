import { useState, useEffect, useRef } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Toast } from 'primereact/toast';
import { InputNumber } from 'primereact/inputnumber';
import { Checkbox } from 'primereact/checkbox';
import { Dropdown } from 'primereact/dropdown';


import 'primereact/resources/themes/saga-blue/theme.css';    // or your preferred theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';


export default function ContactPage() {
  const [contacts, setContacts] = useState([]);
  const [selectedContacts, setSelectedContacts] = useState(null);
  const [contactDialog, setContactDialog] = useState(false);
  const [currentContact, setCurrentContact] = useState(null);
  const [globalFilter, setGlobalFilter] = useState('');
  const toast = useRef(null);

  // Fetch contacts
  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    const res = await fetch('/api/contact');
    const data = await res.json();
    setContacts(data);
  };

  const handleNewContact = () => {
    setCurrentContact({});
    setContactDialog(true);
  };

  const handleEditContact = (rowData) => {
    setCurrentContact(rowData);
    setContactDialog(true);
  };

  const handleDeleteContact = async (rowData) => {
    if (confirm('Are you sure you want to delete this contact?')) {
      await fetch(`/api/contact/${rowData.id}`, { method: 'DELETE' });
      toast.current.show({ severity: 'success', summary: 'Success', detail: 'Contact deleted' });
      fetchContacts();
    }
  };

  const handleSaveContact = async () => {
    const method = currentContact.id ? 'PUT' : 'POST';
    const url = currentContact.id ? `/api/contact/${currentContact.id}` : '/api/contact';

    await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentContact),
    });

    toast.current.show({ severity: 'success', summary: 'Success', detail: 'Contact saved' });
    setContactDialog(false);
    fetchContacts();
  };

  const handleWhatsAppStatus = async () => {
    const phoneNumbers = selectedContacts.map((c) => c.phoneNumber);
    const res = await fetch('/api/whatsapp/contact/checkStatus', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phoneNumbers }),
    });
    const data = await res.json();
    toast.current.show({ severity: 'info', summary: 'WhatsApp Status', detail: JSON.stringify(data) });
  };

  const actionBodyTemplate = (rowData) => (
    <>
      <Button icon="pi pi-pencil" className="p-button-rounded p-button-success mr-2" onClick={() => handleEditContact(rowData)} />
      <Button icon="pi pi-trash" className="p-button-rounded p-button-danger" onClick={() => handleDeleteContact(rowData)} />
    </>
  );

  const leftToolbarTemplate = () => (
    <>
      <Button label="New" icon="pi pi-plus" className="p-button-success mr-2" onClick={handleNewContact} />
      <Button label="Check WhatsApp Status" icon="pi pi-whatsapp" className="p-button-info" onClick={handleWhatsAppStatus} disabled={!selectedContacts || !selectedContacts.length} />
    </>
  );

  const dialogFooter = (
    <div>
      <Button label="Cancel" icon="pi pi-times" className="p-button-text" onClick={() => setContactDialog(false)} />
      <Button label="Save" icon="pi pi-check" className="p-button-text" onClick={handleSaveContact} />
    </div>
  );

  return (
    <div>
      <Toast ref={toast} />
      <Toolbar className="mb-4" left={leftToolbarTemplate}></Toolbar>
      <DataTable
        value={contacts}
        selection={selectedContacts}
        onSelectionChange={(e) => setSelectedContacts(e.value)}
        paginator rows={10} rowsPerPageOptions={[5, 10, 25]}
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} contacts"
        globalFilter={globalFilter}
        header={
          <span className="p-input-icon-left">
            <i className="pi pi-search" />
            <InputText type="search" placeholder="Search..." onInput={(e) => setGlobalFilter(e.target.value)} />
          </span>
        }
      >
        <Column selectionMode="multiple" exportable={false}></Column>
        <Column field="name" header="Name" sortable></Column>
        <Column field="phoneNumber" header="Phone Number" sortable></Column>
        <Column field="email" header="Email" sortable></Column>
        <Column field="facebookid" header="Facebook ID"></Column>
        <Column field="instaid" header="Instagram ID"></Column>
        <Column field="xid" header="X ID"></Column>
        <Column field="address" header="Address"></Column>
        <Column body={actionBodyTemplate}></Column>
      </DataTable>

      <Dialog visible={contactDialog} header="Contact Details" modal className="p-fluid" footer={dialogFooter} onHide={() => setContactDialog(false)}>
        <div className="field">
          <label htmlFor="name">Name</label>
          <InputText id="name" value={currentContact?.name || ''} onChange={(e) => setCurrentContact({ ...currentContact, name: e.target.value })} />
        </div>

        <div className="field">
          <label htmlFor="phoneNumber">Phone Number</label>
          <InputText id="phoneNumber" value={currentContact?.phoneNumber || ''} onChange={(e) => setCurrentContact({ ...currentContact, phoneNumber: e.target.value })} />
        </div>

        <div className="field-checkbox">
          <Checkbox
            inputId="phoneverified"
            checked={currentContact?.phoneverified || false}
            onChange={(e) => setCurrentContact({ ...currentContact, phoneverified: e.checked })}
          />
          <label htmlFor="phoneverified">Phone Verified</label>
        </div>

        <div className="field">
          <label htmlFor="email">Email</label>
          <InputText id="email" value={currentContact?.email || ''} onChange={(e) => setCurrentContact({ ...currentContact, email: e.target.value })} />
        </div>

        <div className="field-checkbox">
          <Checkbox
            inputId="emailverified"
            checked={currentContact?.emailverified || false}
            onChange={(e) => setCurrentContact({ ...currentContact, emailverified: e.checked })}
          />
          <label htmlFor="emailverified">Email Verified</label>
        </div>

        <div className="field">
          <label htmlFor="facebookid">Facebook ID</label>
          <InputText id="facebookid" value={currentContact?.facebookid || ''} onChange={(e) => setCurrentContact({ ...currentContact, facebookid: e.target.value })} />
        </div>

        <div className="field-checkbox">
          <Checkbox
            inputId="facebookverified"
            checked={currentContact?.facebookverified || false}
            onChange={(e) => setCurrentContact({ ...currentContact, facebookverified: e.checked })}
          />
          <label htmlFor="facebookverified">Facebook Verified</label>
        </div>

        <div className="field">
          <label htmlFor="instaid">Instagram ID</label>
          <InputText id="instaid" value={currentContact?.instaid || ''} onChange={(e) => setCurrentContact({ ...currentContact, instaid: e.target.value })} />
        </div>

        <div className="field-checkbox">
          <Checkbox
            inputId="instaidverified"
            checked={currentContact?.instaidverified || false}
            onChange={(e) => setCurrentContact({ ...currentContact, instaidverified: e.checked })}
          />
          <label htmlFor="instaidverified">Instagram Verified</label>
        </div>

        <div className="field">
          <label htmlFor="xid">X ID</label>
          <InputText id="xid" value={currentContact?.xid || ''} onChange={(e) => setCurrentContact({ ...currentContact, xid: e.target.value })} />
        </div>

        <div className="field-checkbox">
          <Checkbox
            inputId="xverified"
            checked={currentContact?.xverified || false}
            onChange={(e) => setCurrentContact({ ...currentContact, xverified: e.checked })}
          />
          <label htmlFor="xverified">X Verified</label>
        </div>

        <div className="field">
          <label htmlFor="address">Address</label>
          <InputText id="address" value={currentContact?.address || ''} onChange={(e) => setCurrentContact({ ...currentContact, address: e.target.value })} />
        </div>

        <div className="field">
          <label htmlFor="conversationType">Conversation Type</label>
          <Dropdown
            id="conversationType"
            value={currentContact?.conversationType || ''}
            options={[
              { label: 'Chat', value: 'chat' },
              { label: 'Call', value: 'call' },
              { label: 'Email', value: 'email' },
            ]}
            onChange={(e) => setCurrentContact({ ...currentContact, conversationType: e.value })}
            placeholder="Select a type"
          />
        </div>

        <div className="field">
          <label htmlFor="pincode">Pincode</label>
          <InputNumber
            id="pincode"
            value={currentContact?.pincode || ''}
            onValueChange={(e) => setCurrentContact({ ...currentContact, pincode: e.value })}
          />
        </div>

        <div className="field">
          <label htmlFor="country">Country</label>
          <Dropdown
            id="country"
            value={currentContact?.country || ''}
            options={[
              { label: 'India', value: 'India' },
              { label: 'United States', value: 'United States' },
              { label: 'United Kingdom', value: 'United Kingdom' },
            ]}
            onChange={(e) => setCurrentContact({ ...currentContact, country: e.value })}
            placeholder="Select a country"
          />
        </div>

        <div className="field-checkbox">
          <Checkbox
            inputId="registered"
            checked={currentContact?.registered || false}
            onChange={(e) => setCurrentContact({ ...currentContact, registered: e.checked })}
          />
          <label htmlFor="registered">Registered</label>
        </div>
      </Dialog>
    </div>
  );
}
