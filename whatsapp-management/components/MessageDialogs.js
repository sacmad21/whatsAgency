// components/MessageDialogs.js
import React, { useState, useEffect } from 'react';
import { Dialog } from 'primereact/dialog';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';

export default function DialogManager({ dialogType, rowData, selectedMessages, onClose }) {
  const [visible, setVisible] = useState(true);
  const [content, setContent] = useState('');
  const [phoneNumber, setPhoneNumber] = useState('');

  useEffect(() => {
    // Prefill or fetch data from rowData if needed
    if (rowData) {
      setContent(rowData.content || '');
      setPhoneNumber(rowData.recipientPhoneNumber || ''); // if available
    }
  }, [rowData]);

  const hideDialog = () => {
    setVisible(false);
    onClose && onClose();
  };

  const handleConfirm = async () => {
    switch (dialogType) {
      case 'send':
        await sendMessage();
        break;
      case 'markRead':
        await markRead();
        break;
      case 'delete':
        await deleteMessage();
        break;
      case 'resend':
        await resendMessage();
        break;
      case 'markMultipleRead':
        await markMultipleRead();
        break;
      // ... other multi-row actions
      default:
        break;
    }
    hideDialog();
  };

  const sendMessage = async () => {
    // Example call to our /api/message/send
    await fetch('/api/message/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recipientPhoneNumber: phoneNumber,
        content,
        type: 'text',
      }),
    });
    alert('Message sent!');
  };

  const markRead = async () => {
    // Example call to /api/message/markRead
    if (!rowData) return;
    await fetch('/api/message/markRead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ messageId: rowData.messageId }),
    });
    alert('Message marked as read!');
  };

  const markMultipleRead = async () => {
    // Mark multiple selected messages as read
    if (!selectedMessages?.length) return;
    for (const msg of selectedMessages) {
      await fetch('/api/message/markRead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messageId: msg.messageId }),
      });
    }
    alert('All selected messages marked as read!');
  };

  const deleteMessage = async () => {
    // Example call to /api/message/deleteMessage
    if (!rowData) return;
    await fetch(`/api/message/deleteMessage?messageId=${rowData.messageId}`, {
      method: 'DELETE',
    });
    alert('Message deleted!');
  };

  const resendMessage = async () => {
    if (!rowData) return;
    await fetch('/api/message/resend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messageId: rowData.messageId,
        recipientPhoneNumber: phoneNumber, // or rowData.recipientPhoneNumber
        content: content || rowData.content,
      }),
    });
    alert('Message resent!');
  };

  const dialogHeader = () => {
    switch (dialogType) {
      case 'send':
        return 'Send a New Message';
      case 'markRead':
        return 'Mark Message as Read';
      case 'markMultipleRead':
        return 'Mark Multiple Messages as Read';
      case 'delete':
        return 'Delete Message';
      case 'resend':
        return 'Resend Message';
      default:
        return 'Action';
    }
  };

  return (
    <Dialog
      visible={visible}
      style={{ width: '450px' }}
      header={dialogHeader()}
      modal
      closable
      onHide={hideDialog}
      footer={
        <div>
          <Button label="Cancel" icon="pi pi-times" onClick={hideDialog} className="p-button-text" />
          <Button label="Confirm" icon="pi pi-check" onClick={handleConfirm} autoFocus />
        </div>
      }
    >
      {dialogType === 'send' || dialogType === 'resend' ? (
        <>
          <div className="field">
            <label htmlFor="phoneNumber">Recipient Phone Number</label>
            <InputText
              id="phoneNumber"
              value={phoneNumber}
              onChange={(e) => setPhoneNumber(e.target.value)}
            />
          </div>
          <div className="field">
            <label htmlFor="content">Message Content</label>
            <InputText
              id="content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
          </div>
        </>
      ) : null}

      {dialogType === 'markRead' && rowData && (
        <p>Mark this message ({rowData.messageId}) as read?</p>
      )}

      {dialogType === 'markMultipleRead' && selectedMessages?.length > 0 && (
        <p>Mark {selectedMessages.length} messages as read?</p>
      )}

      {dialogType === 'delete' && rowData && (
        <p>Delete this message ({rowData.messageId})?</p>
      )}

      {dialogType === 'resend' && rowData && (
        <p>Resend this message ({rowData.messageId})?</p>
      )}
    </Dialog>
  );
}
