/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        clay: {
          900: "#f7f0ea",
          800: "#fcf5ef",
          700: "#fffaf5",
        },
        mint: {
          50: "#f0faf7",
          100: "#d5f0e8",
          200: "#b8e0d2",
          300: "#9ad1bc",
        },
        powder: {
          50: "#f2f7fc",
          100: "#dde9f5",
          200: "#b0d0e8",
          300: "#8fb8db",
        },
        liquid: {
          yellow: "#fcd34d",
          glow: "rgba(252, 211, 77, 0.15)",
          shimmer: "rgba(255,255,255,0.6)",
        },
        bg: "#fcf5ef",
      },
      fontFamily: {
        mono: ["'JetBrains Mono'", "monospace"],
        sans: ["'Inter'", "system-ui", "sans-serif"],
      },
      boxShadow: {
        'clay': 'inset 0 2px 4px rgba(255,255,255,0.6), inset 0 -2px 4px rgba(0,0,0,0.05), 0 12px 24px rgba(0,0,0,0.08), 0 4px 8px rgba(0,0,0,0.04)',
        'clay-hover': 'inset 0 2px 4px rgba(255,255,255,0.8), inset 0 -2px 4px rgba(0,0,0,0.05), 0 16px 32px rgba(0,0,0,0.12), 0 0 20px rgba(252, 211, 77, 0.08)',
        'clay-outer': '0 20px 40px rgba(0,0,0,0.06), 0 10px 20px rgba(0,0,0,0.04)',
        'glass': '0 8px 32px rgba(0,0,0,0.04), inset 0 0 0 1px rgba(255,255,255,0.6)',
        'glass-hover': '0 12px 48px rgba(0,0,0,0.08), inset 0 0 0 1px rgba(255,255,255,0.8)',
      },
      backgroundImage: {
        'glass-gradient': 'linear-gradient(135deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.3) 100%)',
        'shimmer': 'linear-gradient(105deg, transparent 40%, rgba(255,255,255,0.3) 50%, transparent 60%)',
      },
      animation: {
        shimmer: 'shimmer 3s infinite',
        float: 'float 20s ease-in-out infinite',
        pulseSoft: 'pulseSoft 4s ease-in-out infinite',
      },
      keyframes: {
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' },
        },
        float: {
          '0%, 100%': { transform: 'translate(0, 0) scale(1)' },
          '33%': { transform: 'translate(30px, -50px) scale(1.1)' },
          '66%': { transform: 'translate(-20px, 20px) scale(0.9)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: 0.6 },
          '50%': { opacity: 1 },
        },
      },
    },
  },
  plugins: [],
}