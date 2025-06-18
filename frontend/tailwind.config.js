module.exports = {
  content: ['./src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        accent: '#22d3ee', // Cyan
      },
      fontFamily: {
        sans: ['Helvetica Neue', 'Inter', 'Segoe UI', 'sans-serif'],
      },
      backgroundImage: {
        glass: 'linear-gradient(to right, rgba(255,255,255,0.03), rgba(255,255,255,0.02))',
      },
    },
  },
  plugins: [],
}
