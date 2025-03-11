import { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Toolbar } from 'primereact/toolbar';
import { Button } from 'primereact/button';
import { Dialog } from 'primereact/dialog';
import { InputText } from 'primereact/inputtext';
import { Dropdown } from 'primereact/dropdown';
 
import 'primereact/resources/themes/saga-blue/theme.css';    // or your preferred theme
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';
import 'primeflex/primeflex.css';

export default function Pricing() {
  const [pricingData, setPricingData] = useState([]);
  const [selectedPricing, setSelectedPricing] = useState(null);
  const [showDialog, setShowDialog] = useState(false);
  const [pricingForm, setPricingForm] = useState({
    country: '',
    conversationPrice: '',
    messagePrice: '',
  });

  useEffect(() => {
    fetch('/api/pricing/getAll')
      .then((res) => res.json())
      .then((data) => setPricingData(data));
  }, []);

  const savePricing = async () => {
    const endpoint = selectedPricing ? '/api/pricing/update' : '/api/pricing/create';
    const method = selectedPricing ? 'PUT' : 'POST';

    await fetch(endpoint, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...pricingForm, id: selectedPricing?.id }),
    });

    setShowDialog(false);
    location.reload(); // Refresh data
  };

  const deletePricing = async (id) => {
    await fetch('/api/pricing/delete', {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id }),
    });

    location.reload(); // Refresh data
  };

  const actionBodyTemplate = (rowData) => (
    <>
      <Button icon="pi pi-pencil" onClick={() => editPricing(rowData)} />
      <Button icon="pi pi-trash" onClick={() => deletePricing(rowData.id)} className="ml-2" />
    </>
  );

  const editPricing = (rowData) => {
    setSelectedPricing(rowData);
    setPricingForm(rowData);
    setShowDialog(true);
  };

  return (
    <div>
      <Toolbar
        className="mb-4"
        left={<Button label="New" icon="pi pi-plus" onClick={() => setShowDialog(true)} />}
      />
      <DataTable
        value={pricingData}
        selectionMode="single"
        paginator
        rows={10}
        dataKey="id"
      >
        <Column field="country" header="Country" />
        <Column field="conversationPrice" header="Conversation Price" />
        <Column field="messagePrice" header="Message Price" />
        <Column body={actionBodyTemplate} />
      </DataTable>

      <Dialog visible={showDialog} onHide={() => setShowDialog(false)}>
        <div>
          <Dropdown
            value={pricingForm.country}
            onChange={(e) => setPricingForm({ ...pricingForm, country: e.value })}
            options={[{ label: 'India', value: 'IN' }, { label: 'US', value: 'US' }]}
            placeholder="Select Country"
          />
          <InputText
            value={pricingForm.conversationPrice}
            onChange={(e) => setPricingForm({ ...pricingForm, conversationPrice: e.target.value })}
            placeholder="Conversation Price"
          />
          <InputText
            value={pricingForm.messagePrice}
            onChange={(e) => setPricingForm({ ...pricingForm, messagePrice: e.target.value })}
            placeholder="Message Price"
          />
          <Button label="Save" onClick={savePricing} />
        </div>
      </Dialog>
    </div>
  );
}
