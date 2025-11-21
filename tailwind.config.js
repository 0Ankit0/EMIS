/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/**/templates/**/*.html',
    './static/**/*.js',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f7ff',
          100: '#ebf0ff',
          200: '#d6e0ff',
          300: '#b8c9ff',
          400: '#94a9ff',
          500: '#667eea',
          600: '#5568d3',
          700: '#4555b8',
          800: '#37449c',
          900: '#2c3780',
        },
        secondary: {
          50: '#f9f5ff',
          100: '#f3ebff',
          200: '#e7d6ff',
          300: '#d6b8ff',
          400: '#c094ff',
          500: '#764ba2',
          600: '#653a8b',
          700: '#552f74',
          800: '#45265d',
          900: '#371e4a',
        },
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial', 'sans-serif'],
      },
      boxShadow: {
        'sm': '0 2px 8px rgba(0,0,0,0.06)',
        'md': '0 4px 16px rgba(0,0,0,0.1)',
        'lg': '0 8px 30px rgba(0,0,0,0.15)',
      },
    },
  },
  plugins: [],
}
