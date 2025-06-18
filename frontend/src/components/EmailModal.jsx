import React, { useState } from 'react'
import axios from 'axios'

export default function EmailModal({ jdId, onClose }) {
  const [toEmail, setToEmail] = useState('')
  const [cc, setCc] = useState('')
  const [sending, setSending] = useState(false)
  const [status, setStatus] = useState(null)

 

const sendEmail = async (jdId, toEmail, ccList, topMatches) => {
  const res = await axios.post("http://127.0.0.1:5000/send-email", {
    jd_id: jdId,
    to: toEmail,
    cc: ccList, // Array like ["hr@hexaware.com"]
  });
  alert(res.data.message);
};

  return (
    <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">
      <div className="bg-[#1f1f1f] text-white rounded-xl p-8 w-full max-w-md shadow-lg">
        <h2 className="text-xl font-bold mb-4">📧 Send Email – JD {jdId}</h2>

        <label className="block mb-2 font-medium">To (Recruiter Email):</label>
        <input
          type="email"
          value={toEmail}
          onChange={(e) => setToEmail(e.target.value)}
          className="w-full p-2 rounded bg-gray-800 mb-4 border border-gray-700"
          placeholder="recruiter@example.com"
        />

        <label className="block mb-2 font-medium">CC (comma-separated):</label>
        <input
          type="text"
          value={cc}
          onChange={(e) => setCc(e.target.value)}
          className="w-full p-2 rounded bg-gray-800 mb-4 border border-gray-700"
          placeholder="manager@example.com,hr@example.com"
        />

        <div className="flex justify-end gap-4">
          <button
            onClick={onClose}
            className="text-sm text-gray-400 hover:underline"
          >
            Cancel
          </button>

          <button
            onClick={sendEmail}
            disabled={sending || !toEmail}
            className="bg-accent text-black font-semibold py-2 px-6 rounded-lg shadow-md hover:bg-cyan-400 disabled:opacity-50"
          >
            {sending ? 'Sending...' : 'Send Email'}
          </button>
        </div>

        {status && (
          <div className="mt-4 text-sm font-medium text-green-400">
            {status}
          </div>
        )}
      </div>
    </div>
  )
}
