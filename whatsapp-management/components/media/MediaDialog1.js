import React, { useState, useEffect } from 'react';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Button } from 'primereact/button';

// Suppose these are your enumerations
const MEDIA_TYPES = [
  { label: 'IMAGE', value: 'IMAGE' },
  { label: 'VIDEO', value: 'VIDEO' },
  { label: 'AUDIO', value: 'AUDIO' },
  { label: 'DOCUMENT', value: 'DOCUMENT' },
  { label: 'STICKER', value: 'STICKER' },
];

const MESSAGE_STATUSES = [
  { label: 'SENT', value: 'SENT' },
  { label: 'DELIVERED', value: 'DELIVERED' },
  { label: 'READ', value: 'READ' },
  { label: 'FAILED', value: 'FAILED' },
];

export default function MediaDialog({ visible, onHide, editingMedia, onRefresh }) {
  const [mediaId, setMediaId] = useState('');
  const [type, setType] = useState('');
  const [url, setUrl] = useState('');
  const [fileName, setFileName] = useState('');
  const [size, setSize] = useState(0);
  const [status, setStatus] = useState('');

  useEffect(() => {
    if (editingMedia) {
      setMediaId(editingMedia.mediaId || '');
      setType(editingMedia.type || '');
      setUrl(editingMedia.url || '');
      setFileName(editingMedia.fileName || '');
      setSize(editingMedia.size || 0);
      setStatus(editingMedia.status || '');
    } else {
      resetFields();
    }
  }, [editingMedia]);

  const resetFields = () => {
    setMediaId('');
    setType('');
    setUrl('');
    setFileName('');
    setSize(0);
    setStatus('');
  };

  const handleSave = async () => {
    try {
      const payload = { mediaId, type, url, fileName, size, status };
      let endpoint = '/api/media';
      let method = 'POST';

      if (editingMedia) {
        endpoint = `/api/media/${editingMedia.id}`;
        method = 'PUT';
      }

      await fetch(endpoint, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      onRefresh();
      onHide();
    } catch (error) {
      console.error(error);
      alert('Error saving Media');
    }
  };

  const renderFooter = () => {
    return (
      <div>
        <Button
          label="Cancel"
          icon="pi pi-times"
          onClick={onHide}
          className="p-button-text"
        />
        <Button
          label="Save"
          icon="pi pi-check"
          onClick={handleSave}
          autoFocus
        />
      </div>
    );
  };

  return (
    <Dialog
      visible={visible}
      style={{ width: '500px' }}
      header={editingMedia ? 'Edit Media' : 'New Media'}
      modal
      onHide={onHide}
      footer={renderFooter()}
    >
      <div className="p-fluid">
        <div className="p-field">
          <label htmlFor="mediaId">Media ID</label>
          <InputText
            id="mediaId"
            value={mediaId}
            onChange={(e) => setMediaId(e.target.value)}
          />
        </div>

        <div className="p-field">
          <label htmlFor="type">Type</label>
          <Dropdown
            id="type"
            options={MEDIA_TYPES}
            value={type}
            onChange={(e) => setType(e.value)}
            placeholder="Select Type"
          />
        </div>

        <div className="p-field">
          <label htmlFor="url">URL</label>
          <InputText
            id="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>

        <div className="p-field">
          <label htmlFor="fileName">File Name</label>
          <InputText
            id="fileName"
            value={fileName}
            onChange={(e) => setFileName(e.target.value)}
          />
        </div>

        <div className="p-field">
          <label htmlFor="size">Size</label>
          <InputText
            id="size"
            keyfilter="int"
            value={size}
            onChange={(e) => setSize(parseInt(e.target.value) || 0)}
          />
        </div>

        <div className="p-field">
          <label htmlFor="status">Status</label>
          <Dropdown
            id="status"
            options={MESSAGE_STATUSES}
            value={status}
            onChange={(e) => setStatus(e.value)}
            placeholder="Select Status"
          />
        </div>
      </div>
    </Dialog>
  );
}
