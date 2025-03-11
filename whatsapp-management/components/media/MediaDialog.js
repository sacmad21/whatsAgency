import React, { useState, useEffect, useRef } from 'react';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
import { Button } from 'primereact/button';
import { FileUpload } from 'primereact/fileupload';

// Example placeholder for detecting media types
// (You might implement more robust logic using file-type libraries).
function detectMimeTypeFromFilename(filename = '') {
  const ext = filename.split('.').pop().toLowerCase();
  switch (ext) {
    case 'png':
    case 'jpg':
    case 'jpeg':
      return 'image/' + (ext === 'jpg' ? 'jpeg' : ext);
    case 'gif':
      return 'image/gif';
    case 'mp4':
      return 'video/mp4';
    case 'pdf':
      return 'application/pdf';
    default:
      return 'application/octet-stream';
  }
}

// Example placeholders for actual Azure integration logic:
async function uploadFileToAzure(file) {
  // 1. Upload the file (blob) to Azure.
  // 2. Return { url: 'https://.../file.ext', size: number, mimeType: '...' }
  // This is a stub. Implement with Azure Blob SDK.
  return {
    url: 'https://myAzureContainer/blob/autoUploadedFile.ext',
    size: file.size,
    mimeType: file.type || detectMimeTypeFromFilename(file.name),
  };
}

async function downloadFileFromUrlToAzure(fileUrl) {
  // 1. Download file from fileUrl to a temporary buffer.
  // 2. Upload that buffer to Azure.
  // 3. Return { url: 'https://.../file.ext', size: number, mimeType: '...' }
  // This is a stub. Implement with fetch/axios + Azure Blob SDK.
  return {
    url: 'https://myAzureContainer/blob/urlDownloadedFile.ext',
    size: 123456, // size in bytes
    mimeType: 'image/png', // or detect from headers
  };
}

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
  const [type, setType] = useState('IMAGE'); // defaulting to 'IMAGE'
  const [fileName, setFileName] = useState('');
  const [status, setStatus] = useState('SENT'); // defaulting to 'SENT'
  const [urlOrFile, setUrlOrFile] = useState(''); // user can provide a URL or we store a local file object
  const [uploadedFile, setUploadedFile] = useState(null); // File object from local upload

  // The following fields are *auto-calculated*:
  const [size, setSize] = useState(0);
  const [mimeType, setMimeType] = useState('');

  // We hide or disable these from user input
  // because they will be derived automatically.

  useEffect(() => {
    if (editingMedia) {
      setMediaId(editingMedia.mediaId || '');
      setType(editingMedia.type || 'IMAGE');
      setFileName(editingMedia.fileName || '');
      setStatus(editingMedia.status || 'SENT');
      // The user will see the existing URL if you want, or we can hide it.
      setUrlOrFile(editingMedia.url || '');
      setSize(editingMedia.size || 0);
      setMimeType(''); // you might set it from editingMedia if stored
      setUploadedFile(null);
    } else {
      resetFields();
    }
  }, [editingMedia]);

  const resetFields = () => {
    setMediaId('');
    setType('IMAGE');
    setFileName('');
    setStatus('SENT');
    setUrlOrFile('');
    setUploadedFile(null);
    setSize(0);
    setMimeType('');
  };

  // Validations:
  const isValid = () => {
    // We must have either a *non-empty URL* or *one uploaded file*:
    if (!urlOrFile.trim() && !uploadedFile) {
      alert('Please provide either a file URL or upload a local file.');
      return false;
    }
    // If both are provided, let’s require only one or handle the logic accordingly:
    if (urlOrFile.trim() && uploadedFile) {
      alert('Please provide either a URL or upload a file, not both.');
      return false;
    }
    // If user wants to store custom fileName, we can allow it, or fallback to actual name
    return true;
  };

  const handleSave = async () => {
    if (!isValid()) return;

    try {
      let uploadedBlobInfo = null;

      // If user provided a local file
      if (uploadedFile) {
        // 1. Upload to Azure
        uploadedBlobInfo = await uploadFileToAzure(uploadedFile);
        // => { url, size, mimeType }
      } 
      // If user provided a URL
      else if (urlOrFile.trim()) {
        // 1. Download from the given URL and store in Azure
        uploadedBlobInfo = await downloadFileFromUrlToAzure(urlOrFile.trim());
      }

      // If no upload happened (which shouldn’t be the case due to isValid checks)
      if (!uploadedBlobInfo) {
        alert('Upload to Azure failed or returned no data.');
        return;
      }

      // Update local state with auto-calculated values
      const finalUrl = uploadedBlobInfo.url;
      const finalSize = uploadedBlobInfo.size || 0;
      const finalMimeType = uploadedBlobInfo.mimeType || 'application/octet-stream';

      // Derive fileName if none was provided by user
      let finalFileName = fileName;
      if (!finalFileName.trim()) {
        // If we have an uploadedFile, use its name
        if (uploadedFile?.name) {
          finalFileName = uploadedFile.name;
        }
        // Or parse from the finalUrl
        else {
          const urlSegments = finalUrl.split('/');
          finalFileName = urlSegments[urlSegments.length - 1] || 'untitled';
        }
      }

      // Now store data in your local DB:
      const payload = {
        // If editing an existing record, we’ll keep its existing ID, etc.
        mediaId,
        type,
        url: finalUrl,
        fileName: finalFileName,
        size: finalSize,
        status,
      };

      let endpoint = '/api/media';
      let method = 'POST';

      if (editingMedia) {
        endpoint = `/api/media/${editingMedia.id}`;
        method = 'PUT';
      }

      const response = await fetch(endpoint, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.error || 'Failed to save media.');
      }

      await onRefresh();
      onHide();
    } catch (error) {
      console.error(error);
      alert(error.message);
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

  // We either show an Input for URL or a FileUpload component
  // The user picks which method they want
  // “File Type” can still be selected from the dropdown if desired
  return (
    <Dialog
      visible={visible}
      style={{ width: '600px' }}
      header={editingMedia ? 'Edit Media' : 'New Media'}
      modal
      onHide={onHide}
      footer={renderFooter()}
    >
      <div className="p-fluid formgrid grid">
        {/* Media ID (WhatsApp ID) */}
        <div className="field col-12">
          <label htmlFor="mediaId">WhatsApp Media ID (Optional)</label>
          <InputText
            id="mediaId"
            value={mediaId}
            onChange={(e) => setMediaId(e.target.value)}
          />
        </div>

        {/* Type Dropdown */}
        <div className="field col-6">
          <label htmlFor="type">Type</label>
          <Dropdown
            id="type"
            options={MEDIA_TYPES}
            value={type}
            onChange={(e) => setType(e.value)}
            placeholder="Select Type"
          />
        </div>

        {/* Status Dropdown */}
        <div className="field col-6">
          <label htmlFor="status">Status</label>
          <Dropdown
            id="status"
            options={MESSAGE_STATUSES}
            value={status}
            onChange={(e) => setStatus(e.value)}
            placeholder="Select Status"
          />
        </div>

        {/* URL Input */}
        <div className="field col-12">
          <label htmlFor="url">File URL (Optional)</label>
          <InputText
            id="url"
            value={urlOrFile}
            onChange={(e) => {
              setUrlOrFile(e.target.value);
              // If user starts typing a URL, clear the local file
              if (uploadedFile) setUploadedFile(null);
            }}
            placeholder="Enter a public file URL..."
          />
        </div>

        {/* File Upload */}
        <div className="field col-12">
          <label htmlFor="fileUpload">Upload File (Optional)</label>
          <FileUpload
            name="file"
            mode="basic"
            accept="*/*"
            auto
            customUpload
            uploadHandler={(event) => {
              // event.files is an array
              const file = event.files?.[0];
              if (!file) return;
              setUploadedFile(file);
              // Clear the URL if any
              setUrlOrFile('');
            }}
            chooseLabel="Choose File"
          />
        </div>

        {/* File Name Input (Optional if user wants to override) */}
        <div className="field col-12">
          <label htmlFor="fileName">File Name (Optional)</label>
          <InputText
            id="fileName"
            value={fileName}
            onChange={(e) => setFileName(e.target.value)}
            placeholder="Defaults to actual file name if empty"
          />
        </div>

        {/* Readonly / Disabled fields for size, mimeType if you want to show them */}
        <div className="field col-6">
          <label htmlFor="size">Size (Auto-Calcuated)</label>
          <InputText
            id="size"
            value={size}
            disabled
          />
        </div>
        <div className="field col-6">
          <label htmlFor="mimeType">MIME Type (Auto-Calcuated)</label>
          <InputText
            id="mimeType"
            value={mimeType}
            disabled
          />
        </div>
      </div>
    </Dialog>
  );
}
