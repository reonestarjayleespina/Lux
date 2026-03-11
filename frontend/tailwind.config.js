/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        accent: '#5eead4',
        ink: '#0a0a0b',
        panel: 'rgba(24, 24, 27, 0.55)',
      },
      boxShadow: {
        lens: '0 0 50px -12px rgba(255,255,255,0.2)',
      },
      backgroundImage: {
        'hero-radial': 'radial-gradient(circle at top, rgba(94,234,212,0.16), transparent 38%), radial-gradient(circle at bottom, rgba(56,189,248,0.12), transparent 35%)',
      },
    },
  },
  plugins: [],
}