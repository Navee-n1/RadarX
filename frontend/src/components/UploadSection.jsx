import React, { useRef, useState } from 'react'
import { FaFileUpload } from 'react-icons/fa'

export default function UploadSection({ onUploadJD, onUploadResume }) {
  const jdInput = useRef(null)
  const resumeInput = useRef(null)
  const [jdUploaded, setJdUploaded] = useState(false)
  const [resumeUploaded, setResumeUploaded] = useState(false)

  const handleJDChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      onUploadJD(file)
      setJdUploaded(true)
    }
  }

  const handleResumeChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      onUploadResume(file)
      setResumeUploaded(true)
    }
  }

  return (
    <div className="space-y-6">
      {/* JD Upload */}
      <div className="flex items-center justify-between bg-[#141414] p-4 rounded-xl shadow-inner border border-gray-700">
        <div className="relative w-full">
  <label className="bg-gray-800 text-white border border-gray-600 px-4 py-2 rounded cursor-pointer inline-block w-full text-center hover:bg-gray-700 transition">
    📎 Choose JD File
    <input type="file" onChange={handleJDUpload} className="hidden" />
  </label>
  {jdUploaded && <p className="text-sm text-green-400 mt-2">✅ {jdUploaded.name}</p>}
</div>

        <button
          onClick={() => jdInput.current.click()}
          className="bg-accent text-black py-1 px-4 rounded-lg font-medium flex items-center gap-2"
        >
          <FaFileUpload />
          JD File
        </button>
        <input
          ref={jdInput}
          type="file"
          accept=".pdf,.docx,.txt"
          className="hidden"
          onChange={handleJDChange}
        />
      </div>

      {/* Resume Upload */}
      <div className="flex items-center justify-between bg-[#141414] p-4 rounded-xl shadow-inner border border-gray-700">
        <div className="flex flex-col">
          <span className="font-semibold">Upload Consultant Resume</span>
          {resumeUploaded && <span className="text-sm text-green-400">✅ Resume Uploaded</span>}
        </div>
        <button
          onClick={() => resumeInput.current.click()}
          className="bg-accent text-black py-1 px-4 rounded-lg font-medium flex items-center gap-2"
        >
          <FaFileUpload />
          Resume File
        </button>
        <input
          ref={resumeInput}
          type="file"
          accept=".pdf,.docx,.txt"
          className="hidden"
          onChange={handleResumeChange}
        />
      </div>
    </div>
  )
}
