// pages/message/index.js
import React, { useState, useEffect, useRef } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import DialogManager from '../../components/MessageDialogs'; // Ensure correct import
// ... import other prime components as needed

import 'primereact/resources/themes/saga-blue/theme.css';    // or your preferred theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';


export default function MessageList() {
  const [messages, setMessages] = useState([]);
  const [selectedMessages, setSelectedMessages] = useState([]);
  const [globalFilter, setGlobalFilter] = useState('');

  // For dialogs
  const [visibleDialog, setVisibleDialog] = useState(false);
  const [dialogType, setDialogType] = useState(''); 
  const [currentRowData, setCurrentRowData] = useState(null);

  const dt = useRef(null);

  useEffect(() => {
    // Fetch messages from your DB (Next.js API)
    fetch('/api/message')
      .then((res) => res.json())
      .then((data) => {
        // data could be an array of messages
        setMessages(data);
      });
  }, []);

  // Toolbar actions
  const leftToolbarTemplate = () => {
    return (
      <React.Fragment>
        <Button
          label="New Message"
          icon="pi pi-plus"
          className="p-button-success mr-2"
          onClick={() => {
            setDialogType('create');
            setCurrentRowData(null);
            setVisibleDialog(true);
          }}
        />
      </React.Fragment>
    );
  };

  const rightToolbarTemplate = () => {
    return (
      <React.Fragment>
        {/* Example of multi-row action: Mark as Read */}
        <Button
          label="Mark As Read"
          icon="pi pi-eye"
          className="p-button-info mr-2"
          onClick={() => {
            setDialogType('markMultipleRead');
            setVisibleDialog(true);
          }}
        />
        {/* Another multi-row action could be: Delete, Resend, etc. */}
      </React.Fragment>
    );
  };

  const header = (
    <div className="table-header">
      <h5 className="m-0">Manage Messages</h5>
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

  // Row-level actions
  const actionBodyTemplate = (rowData) => {
    return (
      <React.Fragment>
        <Button
          icon="pi pi-send"
          className="p-button-rounded p-button-success mr-2"
          tooltip="Send (re-send if not sent)"
          onClick={() => {
            setDialogType('send');
            setCurrentRowData(rowData);
            setVisibleDialog(true);
          }}
        />
        <Button
          icon="pi pi-eye"
          className="p-button-rounded p-button-info mr-2"
          tooltip="Mark as Read"
          onClick={() => {
            setDialogType('markRead');
            setCurrentRowData(rowData);
            setVisibleDialog(true);
          }}
        />
        <Button
          icon="pi pi-refresh"
          className="p-button-rounded p-button-warning mr-2"
          tooltip="Resend"
          onClick={() => {
            setDialogType('resend');
            setCurrentRowData(rowData);
            setVisibleDialog(true);
          }}
        />
        <Button
          icon="pi pi-trash"
          className="p-button-rounded p-button-danger"
          tooltip="Delete"
          onClick={() => {
            setDialogType('delete');
            setCurrentRowData(rowData);
            setVisibleDialog(true);
          }}
        />
      </React.Fragment>
    );
  };

  return (
    <div className="card">
      <Toolbar className="mb-4" left={leftToolbarTemplate} right={rightToolbarTemplate}></Toolbar>

      <DataTable
        ref={dt}
        value={messages}
        selection={selectedMessages}
        onSelectionChange={(e) => setSelectedMessages(e.value)}
        dataKey="id"
        paginator
        rows={10}
        rowsPerPageOptions={[5, 10, 25]}
        paginatorTemplate="FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink CurrentPageReport RowsPerPageDropdown"
        currentPageReportTemplate="Showing {first} to {last} of {totalRecords} messages"
        globalFilter={globalFilter}
        header={header}
      >
        <Column selectionMode="multiple" exportable={false}></Column>
        <Column hidden ="true" field="messageId" header="Message ID" sortable style={{ minWidth: '12rem' }}></Column>
        <Column field="type" header="Type" sortable style={{ minWidth: '8rem' }}></Column>
        <Column field="senderPhoneNumber" header="Sender" sortable style={{ minWidth: '8rem' }}></Column>
        <Column field="recipientPhoneNumber" header="Receiver" sortable style={{ minWidth: '8rem' }}></Column>
        <Column field="content" header="Content" sortable style={{ minWidth: '16rem' }}></Column>
        <Column field="status" header="Status" sortable style={{ minWidth: '8rem' }}></Column>
        <Column field="direction" header="Direction" sortable style={{ minWidth: '8rem' }}></Column>
        <Column field="createdAt" header="Created" sortable style={{ minWidth: '12rem' }}></Column>
        <Column body={actionBodyTemplate} exportable={false} style={{ minWidth: '14rem' }}></Column>
      </DataTable>

      {/* Dialog component(s) for each action */}
      {visibleDialog && (
        <DialogManager
          dialogType={dialogType}
          rowData={currentRowData}
          selectedMessages={selectedMessages}
          onClose={() => setVisibleDialog(false)}
        />
      )}
    </div>
  );
}
