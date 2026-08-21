const translations = {
    en: {
        home: "Home",
        predictor: "Predictor",
        how: "How It Works",
        improve: "Improve",
        about: "About",
        analyze: "Analyze Now"
    },

    ru: {
        home: "Главная",
        predictor: "Прогноз",
        how: "Как это работает",
        improve: "Улучшить",
        about: "О проекте",
        analyze: "Анализировать"
    },

    uz: {
        home: "Bosh sahifa",
        predictor: "Prognoz",
        how: "Qanday ishlaydi",
        improve: "Yaxshilash",
        about: "Loyiha haqida",
        analyze: "Tahlil qilish"
    },

    tr: {
        home: "Ana Sayfa",
        predictor: "Tahmin",
        how: "Nasıl Çalışır",
        improve: "Geliştir",
        about: "Hakkında",
        analyze: "Analiz Et"
    },

    de: {
        home: "Startseite",
        predictor: "Prognose",
        how: "So funktioniert es",
        improve: "Verbessern",
        about: "Über uns",
        analyze: "Jetzt analysieren"
    },

    fr: {
        home: "Accueil",
        predictor: "Prédiction",
        how: "Comment ça marche",
        improve: "Améliorer",
        about: "À propos",
        analyze: "Analyser"
    },

    es: {
        home: "Inicio",
        predictor: "Predicción",
        how: "Cómo funciona",
        improve: "Mejorar",
        about: "Acerca de",
        analyze: "Analizar"
    },

    it: {
        home: "Home",
        predictor: "Previsione",
        how: "Come funziona",
        improve: "Migliora",
        about: "Informazioni",
        analyze: "Analizza"
    },

    ar: {
        home: "الرئيسية",
        predictor: "التوقع",
        how: "كيف يعمل",
        improve: "تحسين",
        about: "حول",
        analyze: "تحليل"
    },

    zh: {
        home: "首页",
        predictor: "预测",
        how: "工作原理",
        improve: "提升",
        about: "关于",
        analyze: "开始分析"
    }
};

function changeLanguage(lang) {
    const selectedLanguage = translations[lang];

    if (!selectedLanguage) return;

    document.querySelectorAll("[data-i18n]").forEach(element => {
        const key = element.dataset.i18n;

        if (selectedLanguage[key]) {
            element.textContent = selectedLanguage[key];
        }
    });

    localStorage.setItem("language", lang);

    document.documentElement.lang = lang;

    if (lang === "ar") {
        document.documentElement.dir = "rtl";
    } else {
        document.documentElement.dir = "ltr";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const switcher = document.getElementById("languageSwitcher");

    if (!switcher) return;

    const savedLanguage = localStorage.getItem("language") || "en";

    switcher.value = savedLanguage;
    changeLanguage(savedLanguage);

    switcher.addEventListener("change", (event) => {
        changeLanguage(event.target.value);
    });
});