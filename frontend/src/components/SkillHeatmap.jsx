import React from 'react'
import { Chart as ChartJS, Tooltip, Title, Legend, CategoryScale, LinearScale, BarElement } from 'chart.js'
import { Bar } from 'react-chartjs-2'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default function SkillHeatmap({ jdSkills, topMatches }) {
  const labels = jdSkills

  const datasets = topMatches.map((match, index) => ({
    label: match.file,
    data: labels.map(skill =>
      match.explanation.skills_matched.includes(skill) ? 1 :
      match.explanation.skills_missing.includes(skill) ? 0 :
      0.5
    ),
    backgroundColor: `rgba(${60 + index * 50}, 150, 255, 0.6)`
  }))

  const data = {
    labels,
    datasets
  }

  const options = {
    indexAxis: 'y',
    scales: {
      x: { max: 1, title: { display: true, text: "Match Strength" } },
      y: { ticks: { autoSkip: false } }
    },
    plugins: {
      legend: { position: 'bottom' },
      tooltip: { mode: 'index' }
    }
  }

  return (
    <div className="bg-[#1a1a1a] border border-gray-700 rounded-xl p-6 mt-8 shadow-xl">
      <h2 className="text-lg font-bold mb-4 text-accent">Skill Match Heatmap</h2>
      <Bar data={data} options={options} />
    </div>
  )
}
