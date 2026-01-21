/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
        "./public/index.html"
    ],
    theme: {
        extend: {
            fontFamily: {
                display: ["'Space Grotesk'", "'Manrope'", "system-ui", "sans-serif"],
                body: ["'Inter'", "system-ui", "sans-serif"]
            },
            colors: {
                ink: {
                    900: "#0b1220",
                    800: "#0f172a",
                    700: "#111827"
                },
                plasma: "#7c3aed",
                cyanEdge: "#22d3ee"
            },
            boxShadow: {
                card: "0 18px 45px -15px rgba(0,0,0,0.35)"
            }
        }
    },
    plugins: []
};
