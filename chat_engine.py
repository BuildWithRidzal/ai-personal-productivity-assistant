import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


def _build_system_instruction(chat: dict) -> str:
    tone = chat.get("tone", "Santai")
    mode = chat.get("mode", "Daily Planner")
    instructions = chat.get("instructions", "")

    return f"""
Kamu adalah AI Personal Productivity Assistant bernama ChatinMe.

Mode saat ini: {mode}
Gaya bahasa: {tone}

Tugas utama:
- Membantu user membuat jadwal harian
- Membantu memecah tugas besar menjadi langkah kecil
- Membantu membuat prioritas kerja
- Membantu membuat catatan, checklist, dan rencana belajar
- Jawab dengan bahasa Indonesia yang jelas dan praktis

Instruksi tambahan dari user:
{instructions}
"""


def generate_response(
    prompt: str,
    chat: dict,
    model_name: str,
    files=None,
    audio_file=None,
) -> str:
    if not GEMINI_API_KEY or client is None:
        return (
            "API key Gemini belum ditemukan. "
            "Pastikan file .env berisi GEMINI_API_KEY=api_key_kamu."
        )

    try:
        system_instruction = _build_system_instruction(chat)

        history_text = ""
        for msg in chat.get("messages", [])[-8:]:
            role = msg.get("role", "")
            content = msg.get("content", "")
            history_text += f"{role}: {content}\n"

        final_prompt = f"""
Riwayat percakapan:
{history_text}

Pertanyaan terbaru user:
{prompt}
"""

        response = client.models.generate_content(
            model=model_name,
            contents=final_prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
                max_output_tokens=1024,
            ),
        )

        return response.text or "Maaf, Gemini tidak mengembalikan jawaban."

    except Exception as e:
        return f"Terjadi error saat memanggil Gemini API: {e}"