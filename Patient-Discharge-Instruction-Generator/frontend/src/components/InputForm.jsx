import { useState } from 'react'
export default function InputForm({ onSubmit, loading }) {
  const [note, setNote] = useState('')
  const [level, setLevel] = useState('8th grade')
  const [name, setName] = useState('')
  function handleSubmit(e) { e.preventDefault(); onSubmit({note, reading_level:level, patient_name:name||'Patient'}) }
  return (
    <form onSubmit={handleSubmit} style={{marginBottom:24}}>
      <div style={{marginBottom:12}}>
        <label><b>Patient Name (optional)</b></label><br/>
        <input value={name} onChange={e=>setName(e.target.value)} placeholder="e.g. Sarah"
          style={{width:'100%',padding:8,marginTop:4}}/>
      </div>
      <div style={{marginBottom:12}}>
        <label><b>Reading Level</b></label><br/>
        <select value={level} onChange={e=>setLevel(e.target.value)} style={{padding:8,marginTop:4}}>
          <option>5th grade</option><option>8th grade</option><option>adult</option>
        </select>
      </div>
      <div style={{marginBottom:12}}>
        <label><b>Clinical Discharge Note *</b></label><br/>
        <textarea value={note} onChange={e=>setNote(e.target.value)} rows={8} required minLength={50}
          placeholder="Paste the clinical discharge note here..."
          style={{width:'100%',padding:8,marginTop:4,fontFamily:'monospace'}}/>
      </div>
      <button type="submit" disabled={loading} style={{padding:'10px 24px',cursor:'pointer'}}>
        {loading ? 'Generating...' : 'Generate Instructions'}
      </button>
    </form>
  )
}
