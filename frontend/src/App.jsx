import { useState } from 'react'

export default function App(){
  const [file, setFile] = useState(null)
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [jd, setJd] = useState("")
  const [matches, setMatches] = useState([])

  async function upload(){
    const fd = new FormData()
    fd.append("file", file)
    fd.append("name", name)
    fd.append("email", email)
    const res = await fetch("/api/upload_resume", { method: "POST", body: fd })
    alert(JSON.stringify(await res.json()))
  }
  async function search(){
    const fd = new FormData()
    fd.append("jd_text", jd)
    fd.append("top_k", 5)
    const res = await fetch("/api/match", { method: "POST", body: fd })
    const json = await res.json()
    setMatches(json)
  }

  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h2>AI Resume Screening</h2>
      <div style={{marginBottom:12}}>
        <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />{' '}
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />{' '}
        <input type="file" onChange={e=>setFile(e.target.files[0])} />
        <button onClick={upload}>Upload</button>
      </div>
      <div style={{marginBottom:12}}>
        <textarea rows={6} cols={60} placeholder="Paste Job Description" value={jd} onChange={e=>setJd(e.target.value)} />
        <div><button onClick={search}>Find Matches</button></div>
      </div>
      <div>
        {matches.map(m=>(
          <div key={m.id} style={{border:'1px solid #ddd', padding:8, margin:6}}>
            <div><strong>{m.name}</strong> — score: {m.score.toFixed(3)}</div>
            <pre style={{whiteSpace:'pre-wrap'}}>{m.summary}</pre>
          </div>
        ))}
      </div>
    </div>
  )
}
