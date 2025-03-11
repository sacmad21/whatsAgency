import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Textarea } from 'primereact/textarea';
import axios from 'axios';

export default function Templates() {
  const [templates, setTemplates] = useState([]);
  const [selectedTemplates, setSelectedTemplates] = useState(null);
  const [templateDialog, setTemplateDialog] = useState(false);
  const [template, setTemplate] = useState({});
  const [isEdit, setIsEdit] = useState(false);
  const [whatsappDialog, setWhatsappDialog] = useState(false);

  const statusOptions = [
    { label: 'Draft', value: 'Draft' },
    { label: 'Approved', value: 'Approved' },
    { label: 'Rejected', value: 'Rejected' },
  ];

  const categoryOptions = [
    { label: 'Transactional', value: 'Transactional' },
    { label: 'Marketing', value: 'Marketing' },
  ];

  const languageOptions = [
    { label: 'English', value: 'English' },
    { label: 'Spanish', value: 'Spanish' },
  ];

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    const response = await axios.get('/api/templates/list');
    setTemplates(response.data.templates || []);
  };

  const openNew = () => {
    setTemplate({});
    setIsEdit(false);
    setTemplateDialog(true);
  };

  const editTemplate = (rowData) => {
    setTemplate({ ...rowData });
    setIsEdit(true);
    setTemplateDialog(true);
  };

  const saveTemplate = async () => {
    if (isEdit) {
      await axios.post('/api/templates/update', template);
    } else {
      await axios.post('/api/templates/create', template);
    }
    setTemplateDialog(false);
    fetchTemplates();
  };

  const deleteTemplate = async (rowData) => {
    await axios.delete('/api/templates/delete', {
      data: { template_name: rowData.name },
    });
    fetchTemplates();
  };

  const previewTemplate = (rowData) => {
    setTemplate({ ...rowData });
    setWhatsappDialog(true);
  };

  const leftToolbarTemplate = () => (
    <React.Fragment>
      <Button label="New" icon="pi pi-plus" className="p-button-success mr-2" onClick={openNew} />
    </React.Fragment>
  );

  const actionBodyTemplate = (rowData) => (
    <React.Fragment>
      <Button
        icon="pi pi-pencil"
        className="p-button-rounded p-button-success mr-2"
        onClick={() => editTemplate(rowData)}
      />
      <Button
        icon="pi pi-trash"
        className="p-button-rounded p-button-danger mr-2"
        onClick={() => deleteTemplate(rowData)}
      />
      <Button
        icon="pi pi-eye"
        className="p-button-rounded p-button-info"
        onClick={() => previewTemplate(rowData)}
      />
    </React.Fragment>
  );

  return (
    <div>
      <h2>Manage Templates</h2>
      <Toolbar className="mb-4" left={leftToolbarTemplate}></Toolbar>

      <DataTable
        value={templates}
        selection={selectedTemplates}
        onSelectionChange={(e) => setSelectedTemplates(e.value)}
        dataKey="id"
        paginator
        rows={10}
        rowsPerPageOptions={[5, 10, 25]}
      >
        <Column selectionMode="multiple" headerStyle={{ width: '3em' }}></Column>
        <Column field="id" header="ID" sortable></Column>
        <Column field="name" header="Name" sortable></Column>
        <Column field="status" header="Status" sortable></Column>
        <Column field="category" header="Category" sortable></Column>
        <Column field="language" header="Language" sortable></Column>
        <Column field="content" header="Content"></Column>
        <Column body={actionBodyTemplate}></Column>
      </DataTable>

      <Dialog
        visible={templateDialog}
        header={isEdit ? 'Edit Template' : 'New Template'}
        modal
        onHide={() => setTemplateDialog(false)}
      >
        <div className="field">
          <label htmlFor="name">Name</label>
          <InputText
            id="name"
            value={template.name || ''}
            onChange={(e) => setTemplate({ ...template, name: e.target.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="status">Status</label>
          <Dropdown
            id="status"
            value={template.status || ''}
            options={statusOptions}
            onChange={(e) => setTemplate({ ...template, status: e.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="category">Category</label>
          <Dropdown
            id="category"
            value={template.category || ''}
            options={categoryOptions}
            onChange={(e) => setTemplate({ ...template, category: e.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="language">Language</label>
          <Dropdown
            id="language"
            value={template.language || ''}
            options={languageOptions}
            onChange={(e) => setTemplate({ ...template, language: e.value })}
          />
        </div>
        <div className="field">
          <label htmlFor="content">Content</label>
          <Textarea
            id="content"
            value={template.content || ''}
            onChange={(e) => setTemplate({ ...template, content: e.target.value })}
          />
        </div>
        <Button label="Save" icon="pi pi-check" onClick={saveTemplate} />
      </Dialog>

      <Dialog
        visible={whatsappDialog}
        header="Preview Template"
        modal
        onHide={() => setWhatsappDialog(false)}
      >
        <p>Preview WhatsApp API functionality here.</p>
      </Dialog>
    </div>
  );
}
