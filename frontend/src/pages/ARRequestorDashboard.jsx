import React, { useState } from 'react'
import ResumeMatchSection from '../components/ResumeMatchSection'
import OneToOneMatchSection from '../components/OneToOneMatchSection'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'




export default function ARRequestorDashboard({onLogout}) {
  const [activeSection, setActiveSection] = useState('upload')
  const [jdFile, setJdFile] = useState(null)
  const [jdId, setJdId] = useState(null)
  const [status, setStatus] = useState('')
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState({
    compared: false,
    ranked: false,
    emailed: false,
  })
  const [toEmail, setToEmail] = useState('')
const [cc, setCc] = useState('')
const [topMatches, setTopMatches] = useState([]);

  const handleFileChange = (e) => setJdFile(e.target.files[0])

  const uploadJD = async () => {
    if (!jdFile) return
    setLoading(true)
    const formData = new FormData()
    formData.append('file', jdFile)
    formData.append('uploaded_by', 'ar@hexaware.com')
    formData.append('project_code', 'HEX-JD-BULK')
    const res = await axios.post('http://127.0.0.1:5000/upload-jd', formData)
    setJdId(res.data.jd_id)
    setProgress((p) => ({ ...p, compared: true }))
    setStatus('✅ JD uploaded. Matching resumes...')
    runMatching(res.data.jd_id)
  }

  const runMatching = async (jdId) => {
    const res = await axios.post('http://127.0.0.1:5000/match/jd-to-resumes', { jd_id: jdId })
    if (res.data.top_matches.length > 0) {
      setTopMatches(res.data.top_matches); 
      setProgress((p) => ({ ...p, ranked: true }))
      setStatus('✅ Profiles ranked. Recruiter notified.')
    } else {
      setStatus('⚠️ No matches found.')
    }
    setProgress((p) => ({ ...p, emailed: true }))
    setLoading(false)
  }
const handleSendEmail = async () => {
  if (!toEmail) return alert("To email required");

  try {
    const res = await axios.post("http://127.0.0.1:5000/send-email/manual", {
      jd_id: jdId,
      to_email: toEmail,
      cc_list: cc.split(',').map(e => e.trim()).filter(Boolean),
      attachments: topMatches.map(m => m.file_path), // assuming this exists
      subject: `Top Matches for JD ${jdId}`,
      body: `Hello,\n\nPlease find the top matches for JD ID ${jdId}.\n\nRegards,\nRadarX`
    });

    alert(res.data.message);
  } catch (err) {
    console.error("❌ Email failed", err);
    alert("❌ Email failed. See console.");
  }
};

  return (
      <div className="relative w-full max-w-screen-md mx-auto px-4 py-6 space-y-10">
      {/* 🔴 Logout Button */}
      <button
        onClick={onLogout}
        className="absolute top-4 right-6 bg-red-500 text-white px-4 py-1 rounded hover:bg-red-600"
      >
        Logout
      </button>
      
      {/* Tabs */}
      <div className="flex justify-center gap-4 mb-6 flex-wrap">
        <button onClick={() => setActiveSection('upload')} className={`px-5 py-2 rounded-full text-sm font-semibold ${activeSection === 'upload' ? 'bg-accent text-black' : 'bg-gray-700 text-white hover:bg-gray-600'}`}>📤 Upload JD</button>
        <button onClick={() => setActiveSection('resume')} className={`px-5 py-2 rounded-full text-sm font-semibold ${activeSection === 'resume' ? 'bg-accent text-black' : 'bg-gray-700 text-white hover:bg-gray-600'}`}>🔄 Resume → JD</button>
        <button onClick={() => setActiveSection('onetoone')} className={`px-5 py-2 rounded-full text-sm font-semibold ${activeSection === 'onetoone' ? 'bg-accent text-black' : 'bg-gray-700 text-white hover:bg-gray-600'}`}>🔗 One-to-One</button>
      </div>

      <AnimatePresence mode="wait">
      {activeSection === 'upload' && (
        <motion.section
      key="upload"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className="bg-[#151515] border border-gray-700 rounded-2xl p-8 shadow-lg space-y-6"
    >
        
          <h2 className="text-xl font-bold text-accent">Upload JD to Start Matching</h2>
          <div className="relative w-full">
  <label className="bg-gray-800 text-white border border-gray-600 px-4 py-2 rounded cursor-pointer inline-block w-full text-center hover:bg-gray-700 transition">
    📎 Choose JD File
    <input type="file"  onChange={handleFileChange} className="hidden" />
  </label>
  {jdFile && <p className="text-sm text-green-400 mt-2">✅ {jdFile.name}</p>}
</div>

          
          
          <button
            onClick={uploadJD}
            disabled={!jdFile || loading}
            className="bg-accent text-black font-semibold py-2 px-6 rounded-lg hover:bg-cyan-400 transition disabled:opacity-40"
          >
            {loading ? 'Processing...' : '🔍 Upload & Match'}
          </button>
          {status && <p className="text-sm text-accent">{status}</p>}

          {jdId && (
            <div className="mt-6 bg-[#222] p-5 rounded-lg border border-gray-700 space-y-2">
              <h3 className="text-md font-semibold mb-2">Progress Tracker</h3>
              <ProgressItem label="JD Compared" active={progress.compared} />
              <ProgressItem label="Profiles Ranked" active={progress.ranked} />
              <ProgressItem label="Email Sent" active={progress.emailed} />
            </div>
          )}
       </motion.section>
      )}
      {progress.emailed && (
  <div className="mt-6 bg-[#222] p-6 rounded-xl border border-gray-600 space-y-4">
    <h3 className="text-lg font-semibold">📧 Email Top Matches</h3>
    <input
      type="email"
      placeholder="Recruiter Email (To)"
      value={toEmail}
      onChange={(e) => setToEmail(e.target.value)}
      className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded"
    />
    <input
      type="text"
      placeholder="CC Emails (comma-separated)"
      value={cc}
      onChange={(e) => setCc(e.target.value)}
      className="w-full px-3 py-2 bg-gray-800 border border-gray-600 rounded"
    />
    <button
      onClick={handleSendEmail}
      className="bg-accent text-black font-semibold py-2 px-6 rounded hover:bg-cyan-400 transition"
    >
      📩 Send Email
    </button>
  </div>
)}


      {activeSection === 'resume' && (
        <motion.section
      key="resume"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className="bg-[#151515] border border-gray-700 rounded-2xl p-8 shadow-lg"
    >
        
          <ResumeMatchSection />
        
        </motion.section>
      )}

      {activeSection === 'onetoone' && (
        <motion.section
      key="onetoone"
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      className="bg-[#151515] border border-gray-700 rounded-2xl p-8 shadow-lg"
    >
          <OneToOneMatchSection />
        </motion.section>
      )}
      </AnimatePresence>
    </div>
  )
}

function ProgressItem({ label, active }) {
  return (
    <div className="flex items-center gap-3 text-sm">
      <div className={`w-4 h-4 rounded-full ${active ? 'bg-accent' : 'bg-gray-600'}`} />
      <span className={active ? 'text-white' : 'text-gray-400'}>{label}</span>
    </div>
  )
}
