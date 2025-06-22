import React, { useState } from 'react';
import ResumeMatchSection from '../components/ResumeMatchSection';
import OneToOneMatchSection from '../components/OneToOneMatchSection';
import { motion, AnimatePresence } from 'framer-motion';
 
export default function RecruiterDashboard({ onLogout }) {
  const [jdFile, setJdFile] = useState(null);
  const [resumeFile, setResumeFile] = useState(null);
  const [activeSection, setActiveSection] = useState('upload');
 
  const handleJDUpload = (e) => setJdFile(e.target.files[0]);
  const handleResumeUpload = (e) => setResumeFile(e.target.files[0]);
 
  return (
    <div className="relative w-full max-w-screen-md mx-auto px-4 py-6 space-y-10">
      {/* 🔴 Logout Button */}
      <button
        onClick={onLogout}
        className="absolute top-4 right-6 bg-red-500 text-white px-4 py-1 rounded hover:bg-red-600"
      >
        Logout
      </button>
 
      {/* Tab Buttons */}
      <div className="flex justify-center gap-4 mb-6 flex-wrap">
        <button
          onClick={() => setActiveSection('upload')}
          className={`px-5 py-2 rounded-full text-sm font-semibold ${
            activeSection === 'upload'
              ? 'bg-accent text-black'
              : 'bg-gray-700 text-white hover:bg-gray-600'
          }`}
        >
          📤 Upload JD
        </button>
        <button
          onClick={() => setActiveSection('resume')}
          className={`px-5 py-2 rounded-full text-sm font-semibold ${
            activeSection === 'resume'
              ? 'bg-accent text-black'
              : 'bg-gray-700 text-white hover:bg-gray-600'
          }`}
        >
          🔄 Resume → JD
        </button>
        <button
          onClick={() => setActiveSection('onetoone')}
          className={`px-5 py-2 rounded-full text-sm font-semibold ${
            activeSection === 'onetoone'
              ? 'bg-accent text-black'
              : 'bg-gray-700 text-white hover:bg-gray-600'
          }`}
        >
          🔗 One-to-One
        </button>
      </div>
 
      {/* Upload Section */}
      {activeSection === 'upload' && (
        <section className="bg-[#151515] border border-gray-700 rounded-2xl p-8 shadow-lg space-y-6">
          <h2 className="text-xl font-bold text-accent">
            Upload Job Description & Resumes
          </h2>
          <div className="space-y-4">
            <div className="relative w-full">
              <label className="bg-gray-800 text-white border border-gray-600 px-4 py-2 rounded cursor-pointer inline-block w-full text-center hover:bg-gray-700 transition">
                📎 Choose JD File
                <input
                  type="file"
                  onChange={handleJDUpload}
                  className="hidden"
                />
              </label>
              {jdFile && (
                <p className="text-sm text-green-400 mt-2">
✅Uploaded: {jdFile.name}
                </p>
              )}
            </div>
 
            <div className="relative w-full">
              <label className="bg-gray-800 text-white border border-gray-600 px-4 py-2 rounded cursor-pointer inline-block w-full text-center hover:bg-gray-700 transition">
                📎 Choose Resume File
                <input
                  type="file"
                  onChange={handleResumeUpload}
                  className="hidden"
                />
              </label>
              {resumeFile && (
                <p className="text-sm text-green-400 mt-2">
✅Uploaded: {resumeFile.name}
                </p>
              )}
            </div>
 
            <button className="bg-accent text-black font-semibold py-2 px-6 rounded-lg hover:bg-cyan-400 transition">
              🔍 Run Match
            </button>
          </div>
        </section>
      )}
 
      {/* Resume Match Section */}
      {activeSection === 'resume' && (
        <section className="bg-[#151515] border border-gray-700 rounded-2xl p-8 shadow-lg">
          <ResumeMatchSection />
        </section>
      )}
 
      {/* One-to-One Match Section */}
      {activeSection === 'onetoone' && (
        <section className="bg-[#151515] border border-gray-700 rounded-2xl p-8 shadow-lg">
          <OneToOneMatchSection />
        </section>
      )}
    </div>
  );
}