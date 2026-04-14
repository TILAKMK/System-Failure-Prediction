/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        "primary": "#38bdf8",
        "success": "#22c55e",
        "danger": "#ef4444",
        "warning": "#f59e0b",
        "purple": "#8b5cf6",
        "surface": "rgba(15, 23, 42, 0.56)",
        "surface-strong": "rgba(15, 23, 42, 0.74)",
        "border": "rgba(148, 163, 184, 0.20)",
        "text": "#e2e8f0",
        "muted": "#94a3b8",
      },
      fontFamily: {
        sans: ["Space Grotesk", "sans-serif"],
      },
      boxShadow: {
        "dashboard": "0 14px 32px rgba(2, 6, 23, 0.34)",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideInUp: {
          "0%": { opacity: "0", transform: "translateY(15px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        gradientShift: {
          "0%": { backgroundPosition: "0% 50%" },
          "50%": { backgroundPosition: "100% 50%" },
          "100%": { backgroundPosition: "0% 50%" },
        },
      },
      animation: {
        fadeIn: "fadeIn 0.7s ease-out",
        slideInUp: "slideInUp 0.6s ease-out",
        gradientShift: "gradientShift 8s linear infinite",
      },
    },
  },
  plugins: [],
};
