APP_NAME = "ChatinMe - AI Personal Productivity Assistant"

MODEL_OPTIONS = {
    "Gemini 2.0 Flash": "gemini-2.0-flash",
    "Gemini 1.5 Flash": "gemini-1.5-flash",
    "Gemini 1.5 Pro": "gemini-1.5-pro",
}

TONE_OPTIONS = [
    "Santai",
    "Profesional",
    "Motivatif",
    "Ringkas",
]

MODE_OPTIONS = [
    "Daily Planner",
    "Task Breakdown",
    "Study Assistant",
    "Meeting Notes",
    "Priority Coach",
]

SUGGESTIONS = [
    {
        "icon": "🗓️",
        "title": "Buat Jadwal",
        "desc": "Susun agenda harian",
        "prompt": "Buatkan jadwal produktif saya untuk hari ini dengan prioritas yang jelas.",
    },
    {
        "icon": "✅",
        "title": "Pecah Tugas",
        "desc": "Ubah target besar jadi langkah kecil",
        "prompt": "Bantu saya memecah tugas besar menjadi checklist kecil yang mudah dikerjakan.",
    },
    {
        "icon": "🎯",
        "title": "Tentukan Prioritas",
        "desc": "Pilih tugas paling penting",
        "prompt": "Bantu saya menentukan prioritas tugas berdasarkan urgensi dan dampaknya.",
    },
]