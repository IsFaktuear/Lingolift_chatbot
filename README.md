# LingoLift

LingoLift adalah chatbot pembelajaran bahasa Inggris berbasis Streamlit dengan fitur:

- Dashboard progres belajar
- Lesson listening, speaking, dan grammar
- Audio practice
- Chat dengan AI tutor berbasis OpenAI-compatible API
- Vocabulary bank dengan pencarian

## Kebutuhan

- Python 3.10 atau lebih baru
- Internet untuk instalasi package, provider AI, font UI, dan audio practice
- API key OpenAI-compatible jika ingin memakai AI live. API key bersifat opsional karena aplikasi memiliki demo mode.

## Menjalankan di Windows

Buka PowerShell dari folder project, lalu jalankan:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Buat file `.env` di root project jika ingin mengaktifkan AI live:

```powershell
New-Item .env -ItemType File
```

Isi `.env` dengan konfigurasi provider yang digunakan. Contoh Agent Router:

```dotenv
OPENAI_API_KEY=isi_api_key_di_sini
OPENAI_BASE_URL=https://agentrouter.org/v1
OPENAI_MODEL=deepseek-v4-flash
```

Jalankan aplikasi:

```powershell
streamlit run app.py
```

Buka alamat yang ditampilkan Streamlit, biasanya `http://localhost:8501`.

## Demo mode

Jika `OPENAI_API_KEY` belum diisi, aplikasi tetap bisa dijalankan. Chatbot akan memakai respons demo dan fitur dashboard, lesson, audio, serta vocabulary tetap tersedia.

## Provider lain

Provider lain yang kompatibel dengan OpenAI bisa digunakan dengan mengganti `OPENAI_BASE_URL` dan `OPENAI_MODEL` di `.env`.

## Troubleshooting

- Jika PowerShell menolak aktivasi virtual environment, gunakan `.venv\Scripts\python.exe -m pip install -r requirements.txt`.
- Jika package belum terbaca, pastikan virtual environment aktif dan jalankan ulang `pip install -r requirements.txt`.
- Jangan commit file `.env` karena berisi API key.

## Struktur fitur

- `app.py`: entry point dan routing halaman native Streamlit.
- `services.py`: service chatbot dan konfigurasi provider AI.
- `content.py` dan `models.py`: data serta model lesson dan vocabulary.
- `ui/dashboard.py`: dashboard, lesson, audio, dan quick practice.
- `ui/chat.py`: percakapan dengan AI tutor.
- `ui/vocabulary.py`: pencarian vocabulary.
- `ui/styles.py`: tampilan bersama.
