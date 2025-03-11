// media/index.js

import React, { useState, useEffect, useRef } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { Tooltip } from 'primereact/tooltip';
import { InputText } from 'primereact/inputtext';
import { SpeedDial } from 'primereact/speeddial'; // For the WhatsApp SpeedDial
import MediaDialog from '../../components/media/MediaDialog1';

import 'primeicons/primeicons.css';
import 'primereact/resources/primereact.min.css';
import 'primereact/resources/themes/saga-blue/theme.css'; // Or your chosen theme
import 'primeflex/primeflex.css';

export default function MediaPage() {
  const [mediaList, setMediaList] = useState([]);
  const [selectedMedia, setSelectedMedia] = useState([]);
  const [globalFilter, setGlobalFilter] = useState('');
  const [mediaDialogVisible, setMediaDialogVisible] = useState(false);
  const [editingMedia, setEditingMedia] = useState(null);
  const dt = useRef(null);

  useEffect(() => {
    fetchMediaList();
  }, []);

  const fetchMediaList = async () => {
    try {
      const res = await fetch('/api/media');
      const data = await res.json();
      // Ensure data is an array to avoid slice() errors
      setMediaList(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error fetching media list:', error);
      setMediaList([]);
    }
  };

  // Single Row: Upload to WhatsApp
  const handleWhatsAppUpload = async (mediaItem) => {
    try {
      // Example: your logic to retrieve file from Azure / local, then call /api/whatsapp/media/upload
      // For demo, we'll just alert:
      alert(`Uploading media "${mediaItem.fileName}" with ID ${mediaItem.id} to WhatsApp...`);
      // After successful upload, you'd store the returned WhatsApp media_id in DB, etc.
    } catch (err) {
      console.error(err);
      alert('Upload to WhatsApp failed: ' + err.message);
    }
  };

  // Single Row: Delete from WhatsApp
  const handleWhatsAppDelete = async (mediaItem) => {
    try {
      if (!mediaItem.mediaId) {
        alert('No WhatsApp mediaId found for this record!');
        return;
      }
      if (!window.confirm(`Are you sure to delete mediaId "${mediaItem.mediaId}" from WhatsApp?`)) {
        return;
      }
      alert(`Deleting mediaId "${mediaItem.mediaId}" from WhatsApp...`);
      // Call /api/whatsapp/media/delete?mediaId=...
    } catch (err) {
      console.error(err);
      alert('Delete from WhatsApp failed: ' + err.message);
    }
  };

  // Single Row: Edit
  const handleEdit = (rowData) => {
    setEditingMedia(rowData);
    setMediaDialogVisible(true);
  };

  // Single Row: Delete from DB
  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this Media (DB record)?')) {
      await fetch(`/api/media/${id}`, { method: 'DELETE' });
      await fetchMediaList();
    }
  };

  // 1.1 actionBodyTemplate with tooltips
  const actionBodyTemplate = (rowData) => {
    return (
      <React.Fragment>
        {/* Tooltip demonstration; each button gets a tooltip via data-pr-tooltip */}
        <Button
          icon="pi pi-cloud-upload"
          className="p-button-rounded p-button-info mr-2"
          data-pr-tooltip="Upload to WhatsApp"
          onClick={() => handleWhatsAppUpload(rowData)}
        />
        <Button
          icon="pi pi-pencil"
          className="p-button-rounded p-button-success mr-2"
          data-pr-tooltip="Edit Record"
          onClick={() => handleEdit(rowData)}
        />
        <Button
          icon="pi pi-cloud"
          className="p-button-rounded p-button-warning mr-2"
          data-pr-tooltip="Delete from WhatsApp"
          onClick={() => handleWhatsAppDelete(rowData)}
        />
        <Button
          icon="pi pi-trash"
          className="p-button-rounded p-button-danger"
          data-pr-tooltip="Delete from Database"
          onClick={() => handleDelete(rowData.id)}
        />
      </React.Fragment>
    );
  };

  // Attach the tooltip to the entire document or a container
  useEffect(() => {
    Tooltip.active && Tooltip.deactivateAll();
  }, [mediaList]);

  // 2. SpeedDial for WhatsApp-Specific Bulk Actions
  const speedDialItems = [
    {
      label: 'Bulk Upload',
      icon: 'pi pi-cloud-upload',
      command: () => handleBulkUpload(),
    },
    {
      label: 'Bulk Delete',
      icon: 'pi pi-cloud',
      command: () => handleBulkDelete(),
    },
  ];

  // 3. Implement handleBulkUpload and handleBulkDelete
  const handleBulkUpload = async () => {
    if (!selectedMedia || selectedMedia.length === 0) {
      alert('No media selected for bulk upload!');
      return;
    }
    // Example logic: for each media item, do handleWhatsAppUpload or custom logic
    for (const mediaItem of selectedMedia) {
      await handleWhatsAppUpload(mediaItem);
    }
    alert('Bulk upload to WhatsApp completed!');
  };

  const handleBulkDelete = async () => {
    if (!selectedMedia || selectedMedia.length === 0) {
      alert('No media selected for bulk delete!');
      return;
    }
    if (!window.confirm(`Are you sure you want to delete ${selectedMedia.length} items from WhatsApp?`)) {
      return;
    }
    for (const mediaItem of selectedMedia) {
      await handleWhatsAppDelete(mediaItem);
    }
    alert('Bulk delete from WhatsApp completed!');
  };

  // Toolbar for left side
  const leftToolbarTemplate = () => {
    return (
      <React.Fragment>
        <Button
          label="New Media"
          icon="pi pi-plus"
          className="p-button mr-2"
          onClick={() => {
            setEditingMedia(null);
            setMediaDialogVisible(true);
          }}
        />
      </React.Fragment>
    );
  };

  // For the right side, we can keep it empty or add filters, etc.
  const rightToolbarTemplate = () => {
    return <React.Fragment>{/* Additional controls if needed */}</React.Fragment>;
  };

  const header = (
    <div className="table-header flex flex-row justify-content-between">
      <h5 className="m-0">Manage Media</h5>
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
    <div>
      <Toolbar className="mb-4" left={leftToolbarTemplate} right={rightToolbarTemplate}></Toolbar>
      {/* SpeedDial for WhatsApp actions */}
      <SpeedDial
        model={speedDialItems}
        direction="up"
        style={{ position: 'fixed', bottom: '2rem', right: '2rem' }}
        buttonClassName="p-button-rounded p-button-info"
        showIcon="pi pi-whatsapp"
        hideIcon="pi pi-times"
        tooltip="WhatsApp Bulk Actions"
      />

      <DataTable
        ref={dt}
        value={mediaList}
        paginator
        rows={10}
        rowsPerPageOptions={[5, 10, 25]}
        dataKey="id"
        globalFilter={globalFilter}
        header={header}
        selectionMode="multiple"
        selection={selectedMedia}
        onSelectionChange={(e) => setSelectedMedia(e.value)}
      >
        <Column selectionMode="multiple" exportable={false} style={{ width: '3em' }}></Column>
        <Column field="id" header="ID" sortable style={{ minWidth: '6rem' }}></Column>
        <Column field="mediaId" header="Media ID" sortable style={{ minWidth: '10rem' }}></Column>
        <Column field="type" header="Type" sortable style={{ minWidth: '8rem' }}></Column>
        <Column field="url" header="URL" style={{ minWidth: '14rem' }}></Column>
        <Column field="fileName" header="File Name" style={{ minWidth: '10rem' }}></Column>
        <Column field="size" header="Size" style={{ minWidth: '8rem' }} sortable></Column>
        <Column field="status" header="Status" style={{ minWidth: '8rem' }} sortable></Column>
        <Column
          body={actionBodyTemplate}
          exportable={false}
          style={{ minWidth: '12rem' }}
        ></Column>
      </DataTable>

      {mediaDialogVisible && (
        <MediaDialog
          visible={mediaDialogVisible}
          onHide={() => setMediaDialogVisible(false)}
          editingMedia={editingMedia}
          onRefresh={fetchMediaList}
        />
      )}
    </div>
  );
}
