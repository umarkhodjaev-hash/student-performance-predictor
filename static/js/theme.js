document.addEventListener("DOMContentLoaded", function () {

    const themeToggle = document.getElementById("themeToggle");

    // Get saved theme
    const savedTheme = localStorage.getItem("theme");

    // Apply saved theme
    if (savedTheme === "light") {
        document.body.classList.add("light-theme");
    }

    // Change button icon
    function updateThemeIcon() {

        if (!themeToggle) return;

        if (document.body.classList.contains("light-theme")) {
            themeToggle.textContent = "☀️";
            themeToggle.setAttribute(
                "aria-label",
                "Switch to dark mode"
            );
        } else {
            themeToggle.textContent = "🌙";
            themeToggle.setAttribute(
                "aria-label",
                "Switch to light mode"
            );
        }
    }

    updateThemeIcon();


    // Switch theme when button is clicked
    if (themeToggle) {

        themeToggle.addEventListener("click", function () {

            document.body.classList.toggle("light-theme");

            if (document.body.classList.contains("light-theme")) {

                localStorage.setItem("theme", "light");

            } else {

                localStorage.setItem("theme", "dark");

            }

            updateThemeIcon();

        });

    }

});