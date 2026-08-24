const translations = {
    en: {
        home: "Home",
        predictor: "Predictor",
        how: "How It Works",
        improve: "Improve",
        about: "About",
        analyze: "Analyze Now",
        analyzeAgain: "Analyze Again"
    },

    ru: {
        home: "Главная",
        predictor: "Прогноз",
        how: "Как это работает",
        improve: "Улучшить",
        about: "О проекте",
        analyze: "Анализировать",
        analyzeAgain: "Анализировать снова"
    },

    uz: {
        home: "Bosh sahifa",
        predictor: "Prognoz",
        how: "Qanday ishlaydi",
        improve: "Yaxshilash",
        about: "Loyiha haqida",
        analyze: "Tahlil qilish",
        analyzeAgain: "Qayta tahlil qilish"
    },

    tr: {
        home: "Ana Sayfa",
        predictor: "Tahmin",
        how: "Nasıl Çalışır",
        improve: "Geliştir",
        about: "Hakkında",
        analyze: "Analiz Et",
        analyzeAgain: "Tekrar Analiz Et"
    },

    de: {
        home: "Startseite",
        predictor: "Prognose",
        how: "So funktioniert es",
        improve: "Verbessern",
        about: "Über uns",
        analyze: "Jetzt analysieren",
        analyzeAgain: "Erneut analysieren"
    },

    fr: {
        home: "Accueil",
        predictor: "Prédiction",
        how: "Comment ça marche",
        improve: "Améliorer",
        about: "À propos",
        analyze: "Analyser",
        analyzeAgain: "Analyser à nouveau"
    },

    es: {
        home: "Inicio",
        predictor: "Predicción",
        how: "Cómo funciona",
        improve: "Mejorar",
        about: "Acerca de",
        analyze: "Analizar",
        analyzeAgain: "Analizar de nuevo"
    },

    it: {
        home: "Home",
        predictor: "Previsione",
        how: "Come funziona",
        improve: "Migliora",
        about: "Informazioni",
        analyze: "Analizza",
        analyzeAgain: "Analizza di nuovo"
    },

    ar: {
        home: "الرئيسية",
        predictor: "التوقع",
        how: "كيف يعمل",
        improve: "تحسين",
        about: "حول",
        analyze: "تحليل",
        analyzeAgain: "تحليل مرة أخرى"
    },

    zh: {
        home: "首页",
        predictor: "预测",
        how: "工作原理",
        improve: "提升",
        about: "关于",
        analyze: "开始分析",
        analyzeAgain: "再次分析"
    }
};

function changeLanguage(lang) {
    const selectedLanguage = translations[lang];

    if (!selectedLanguage) {
        return;
    }

    // Translate all elements that have data-i18n
    document.querySelectorAll("[data-i18n]").forEach((element) => {
        const key = element.getAttribute("data-i18n");

        if (selectedLanguage[key]) {
            element.textContent = selectedLanguage[key];
        }
    });

    // Save selected language
    localStorage.setItem("language", lang);

    // Update page language
    document.documentElement.lang = lang;

    // Arabic uses right-to-left layout
    if (lang === "ar") {
        document.documentElement.dir = "rtl";
    } else {
        document.documentElement.dir = "ltr";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const switcher = document.getElementById("languageSwitcher");

    if (!switcher) {
        return;
    }

    // Load saved language or use English by default
    const savedLanguage = localStorage.getItem("language") || "en";

    // Make sure saved language still exists
    const activeLanguage = translations[savedLanguage]
        ? savedLanguage
        : "en";

    switcher.value = activeLanguage;

    changeLanguage(activeLanguage);

    // Change language when user selects another option
    switcher.addEventListener("change", (event) => {
        const selectedLanguage = event.target.value;

        changeLanguage(selectedLanguage);
    });
});

