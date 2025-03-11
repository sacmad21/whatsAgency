import React, { useState, useEffect, useRef } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import MediaDialog from '../../components/media/MediaDialog';

import 'primeicons/primeicons.css';
import 'primereact/resources/primereact.min.css';
import 'primereact/resources/themes/saga-blue/theme.css'; // Or your chosen theme
import 'primeflex/primeflex.css';

export default function MediaPage() {
    const [mediaList, setMediaList] = useState([]);
    const [selectedMedia, setSelectedMedia] = useState(null);
    const [globalFilter, setGlobalFilter] = useState('');
    const [mediaDialogVisible, setMediaDialogVisible] = useState(false);
    const [editingMedia, setEditingMedia] = useState(null);
    const dt = useRef(null);

    useEffect(() => {
        fetchMediaList();
    }, []);

    const fetchMediaList = async () => {
        const res = await fetch('/api/media');
        const data = await res.json();
        setMediaList(data);
    };

    // Toolbar buttons
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

    const rightToolbarTemplate = () => {
        return (
            <React.Fragment>
                {/* Future: Add multi-row WhatsApp triggers or filters here */}
            </React.Fragment>
        );
    };

    // Action column
    const actionBodyTemplate = (rowData) => {
        return (
            <React.Fragment>
                <Button
                    icon="pi pi-pencil"
                    className="p-button-rounded p-button-success mr-2"
                    onClick={() => {
                        setEditingMedia(rowData);
                        setMediaDialogVisible(true);
                    }}
                />
                <Button
                    icon="pi pi-trash"
                    className="p-button-rounded p-button-danger"
                    onClick={() => handleDelete(rowData.id)}
                />
                <Button
                    icon="pi pi-arrow-up"
                    className="p-button-rounded p-button-info mr-2"
                    tooltip="Upload to WhatsApp"
                    onClick={() => handleWhatsAppUpload(rowData)}
                />
                <Button
                    icon="pi pi-pencil"
                    className="p-button-rounded p-button-success mr-2"
                    onClick={() => {
                        setEditingMedia(rowData);
                        setMediaDialogVisible(true);
                    }}
                />
                <Button
                    icon="pi pi-trash"
                    className="p-button-rounded p-button-danger"
                    onClick={() => handleDelete(rowData.id)}
                />

            </React.Fragment>
        );
    };

    // Delete media
    const handleDelete = async (id) => {
        if (window.confirm('Are you sure you want to delete this Media?')) {
            await fetch(`/api/media/${id}`, { method: 'DELETE' });
            await fetchMediaList();
        }
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
            <DataTable
                ref={dt}
                value={mediaList}
                paginator
                rows={10}
                rowsPerPageOptions={[5, 10, 25]}
                dataKey="id"
                globalFilter={globalFilter}
                header={header}
                selectionMode="multiple" // if needed
                selection={selectedMedia}
                onSelectionChange={(e) => setSelectedMedia(e.value)}
            >
                <Column selectionMode="multiple" exportable={false} style={{ width: '3em' }}></Column>
                <Column field="id" header="ID" sortable style={{ minWidth: '8rem' }}></Column>
                <Column field="mediaId" header="Media ID" sortable style={{ minWidth: '12rem' }}></Column>
                <Column field="type" header="Type" sortable style={{ minWidth: '10rem' }}></Column>
                <Column field="url" header="URL" style={{ minWidth: '14rem' }}></Column>
                <Column field="fileName" header="File Name" style={{ minWidth: '12rem' }}></Column>
                <Column field="size" header="Size" style={{ minWidth: '8rem' }} sortable></Column>
                <Column field="status" header="Status" style={{ minWidth: '10rem' }} sortable></Column>
                <Column
                    body={actionBodyTemplate}
                    exportable={false}
                    style={{ minWidth: '10rem' }}
                ></Column>
            </DataTable>

            {/* Dialog for create/update */}
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
