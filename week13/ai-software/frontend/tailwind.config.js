/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          dark: '#0B0F19',
          card: 'rgba(17, 24, 39, 0.7)',
          accent: '#6366F1',
          neonCyan: '#06B6D4',
          neonPurple: '#A855F7',
          neonGreen: '#10B981',
          border: 'rgba(55, 65, 81, 0.3)',
        }
      },
      fontFamily: {
        sans: ['Outfit', 'Inter', 'sans-serif'],
      },
      boxShadow: {
        'glow-indigo': '0 0 15px rgba(99, 102, 241, 0.4)',
        'glow-cyan': '0 0 15px rgba(6, 182, 212, 0.4)',
        'glow-purple': '0 0 15px rgba(168, 85, 247, 0.4)',
        'glow-green': '0 0 15px rgba(16, 185, 129, 0.4)',
      }
    },
  },
  plugins: [],
}
