export default function InstructionCard({ data }) {
  return (
    <div style={{border:'1px solid #dee2e6',borderRadius:8,padding:24}}>
      <h2>Your Discharge Instructions</h2>
      {data.what_happened && <section><h3>What Happened</h3><p>{data.what_happened}</p></section>}
      {data.medications?.length > 0 && (
        <section>
          <h3>Your Medications</h3>
          <table style={{width:'100%',borderCollapse:'collapse'}}>
            <thead><tr style={{background:'#f8f9fa'}}>
              <th style={{padding:8,textAlign:'left'}}>Medicine</th>
              <th style={{padding:8,textAlign:'left'}}>Dose</th>
              <th style={{padding:8,textAlign:'left'}}>When</th>
              <th style={{padding:8,textAlign:'left'}}>Why</th>
            </tr></thead>
            <tbody>{data.medications.map((m,i)=>(
              <tr key={i} style={{borderTop:'1px solid #dee2e6'}}>
                <td style={{padding:8}}>{m.name}</td>
                <td style={{padding:8}}>{m.dose||'As prescribed'}</td>
                <td style={{padding:8}}>{m.frequency||'—'}</td>
                <td style={{padding:8}}>{m.purpose||'—'}</td>
              </tr>
            ))}</tbody>
          </table>
        </section>
      )}
      {data.home_care_instructions?.length > 0 && (
        <section><h3>What To Do At Home</h3>
        <ol>{data.home_care_instructions.map((i,idx)=><li key={idx}>{i}</li>)}</ol></section>
      )}
      {data.warning_signs?.length > 0 && (
        <section style={{background:'#fff3cd',border:'1px solid #ffc107',borderRadius:6,padding:16}}>
          <h3>Call Us Immediately If You Have</h3>
          <ul>{data.warning_signs.map((s,i)=><li key={i}>{s}</li>)}</ul>
        </section>
      )}
      {data.followup && (
        <section style={{background:'#d1ecf1',borderRadius:6,padding:16,marginTop:16}}>
          <h3>Your Follow-Up</h3><p>{data.followup}</p>
        </section>
      )}
      <button onClick={()=>window.print()} style={{marginTop:16,padding:'8px 20px'}}>Print Instructions</button>
    </div>
  )
}
