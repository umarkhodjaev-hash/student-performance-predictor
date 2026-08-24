document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById("themeToggle");
    const savedTheme = localStorage.getItem("theme");

    // Apply saved theme
    if (savedTheme === "light") {
        document.body.classList.add("light-theme");
    } else {
        document.body.classList.remove("light-theme");
    }

    function updateThemeIcon() {
        if (!themeToggle) return;

        const isLight = document.body.classList.contains("light-theme");

        themeToggle.textContent = isLight ? "☀️" : "🌙";
        themeToggle.setAttribute(
            "aria-label",
            isLight ? "Switch to dark mode" : "Switch to light mode"
        );
    }

    updateThemeIcon();

    if (!themeToggle) return;

    themeToggle.addEventListener("click", () => {
        document.body.classList.toggle("light-theme");

        const isLight = document.body.classList.contains("light-theme");

        localStorage.setItem(
            "theme",
            isLight ? "light" : "dark"
        );

        updateThemeIcon();
    });
});