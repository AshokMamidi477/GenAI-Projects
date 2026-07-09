import { useState } from 'react'
import InputForm from './components/InputForm'
import InstructionCard from './components/InstructionCard'

export default function App() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(formData) {
    setLoading(true); setError('')
    try {
      const res = await fetch('http://localhost:8000/generate-instructions', {
        method: 'POST', headers: {'Content-Type':'application/json'},
        body: JSON.stringify(formData),
      })
      if (!res.ok) { const e = await res.json(); throw new Error(e.detail) }
      setData(await res.json())
    } catch(e) { setError(e.message) }
    finally { setLoading(false) }
  }

  return (
    <div style={{fontFamily:'system-ui',maxWidth:900,margin:'0 auto',padding:24}}>
      <h1>Patient Discharge Instructions</h1>
      <InputForm onSubmit={handleSubmit} loading={loading} />
      {error && <p style={{color:'red'}}>Error: {error}</p>}
      {data && <InstructionCard data={data} />}
    </div>
  )
}
