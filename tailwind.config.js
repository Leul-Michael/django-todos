module.exports = {
  content: ["./base/templates/**/*.html", "./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        background: "hsl(245, 32%, 7%)",
        border: "hsl(217.2 32.6% 15%)",
        color: "#f0f0f0",
        "color-light": "#c9c9c9",
        "color-foreground": "#0f0f0f",
        accent: "hsl(108 100% 65%)",
        "accent-dark": "#635fd8",
      },
      gridTemplateColumns: {
        "layout-200": "repeat(auto-fill, minmax(200px, 1fr))",
        "layout-250": "repeat(auto-fill, minmax(250px, 1fr))",
        "layout-300": "repeat(auto-fill, minmax(300px, 1fr))",
      },
    },
  },
  plugins: [],
}
