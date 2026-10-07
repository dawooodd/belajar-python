"""
================================================================================
MODUL 05: MACHINE LEARNING & ARTIFICIAL INTELLIGENCE (ML/AI)
FILE 04: AI Modern: Vector Store, Cosine Similarity, RAG & Autonomous Agent
================================================================================
Tujuan Pembelajaran:
1. Memahami intuisi Semantic Vector Embeddings di ruang dimensi tinggi.
2. Membangun In-Memory Vector Database dengan pencarian Cosine Similarity dari nol.
3. Arsitektur RAG (Retrieval-Augmented Generation): Chunking, Indexing, and Context Injection.
4. Membangun Autonomous Agent dengan pola ReAct (Reasoning + Action) & Function Calling.
5. Menjalankan pipeline AI modern secara mandiri tanpa wajib biaya API berbayar.
================================================================================
"""

import math
import re
from typing import Callable, Any
from dataclasses import dataclass, field

print("=" * 70)
print("🧠 PENERAPAN AI MODERN: VECTOR DB, RAG & AUTONOMOUS AGENT")
print("=" * 70)


# ------------------------------------------------------------------------------
# 1. Intuisi Vector Embeddings & Cosine Similarity Murni
# ------------------------------------------------------------------------------
# Embedding mengubah teks menjadi vektor angka desimal. Teks dengan makna serupa
# akan memiliki arah vektor berdekatan (Cosine Similarity mendekati 1.0).

def hitung_cosine_similarity(vektor_a: list[float], vektor_b: list[float]) -> float:
    """Menghitung kemiripan sudut kosinus antara dua vektor."""
    dot_product = sum(a * b for a, b in zip(vektor_a, vektor_b))
    norm_a = math.sqrt(sum(a * a for a in vektor_a))
    norm_b = math.sqrt(sum(b * b for b in vektor_b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)


# ------------------------------------------------------------------------------
# 2. Membangun Mini Vector Database (In-Memory Vector Store)
# ------------------------------------------------------------------------------
@dataclass
class DokumenChunk:
    id: str
    konten: str
    vektor: list[float]
    metadata: dict[str, Any] = field(default_factory=dict)


class MiniVectorDatabase:
    """Vector database ringan berbasis memori seperti ChromaDB / Pinecone."""
    def __init__(self, kosakata_referensi: list[str]) -> None:
        self.kosakata = [k.lower() for k in kosakata_referensi]
        self.koleksi: list[DokumenChunk] = []

    def teks_ke_vektor(self, teks: str) -> list[float]:
        """Menghasilkan representasi vektor frekuensi istilah ternormalisasi."""
        kata_kata = re.findall(r'\b\w+\b', teks.lower())
        vektor = [0.0] * len(self.kosakata)
        for kata in kata_kata:
            if kata in self.kosakata:
                idx = self.kosakata.index(kata)
                vektor[idx] += 1.0
        # Normalisasi L2
        norma = math.sqrt(sum(v * v for v in vektor))
        if norma > 0:
            vektor = [v / norma for v in vektor]
        return vektor

    def tambah_dokumen(self, doc_id: str, konten: str, metadata: dict | None = None) -> None:
        vektor = self.teks_ke_vektor(konten)
        chunk = DokumenChunk(id=doc_id, konten=konten, vektor=vektor, metadata=metadata or {})
        self.koleksi.append(chunk)

    def cari_kemiripan(self, kueri: str, top_k: int = 2) -> list[tuple[DokumenChunk, float]]:
        """Pencarian semantic similarity search top-K menggunakan Cosine Similarity."""
        kueri_vektor = self.teks_ke_vektor(kueri)
        skor_list = []
        for chunk in self.koleksi:
            skor = hitung_cosine_similarity(kueri_vektor, chunk.vektor)
            skor_list.append((chunk, skor))
        # Urutkan dari skor tertinggi
        skor_list.sort(key=lambda x: x[1], reverse=True)
        return skor_list[:top_k]


# Inisialisasi basis pengetahuan (Knowledge Base RAG)
KOSAKATA_AI = [
    "python", "django", "orm", "api", "rest", "database", "ai", "model",
    "machine", "learning", "token", "prompt", "rag", "agent", "postgres",
    "deployment", "docker", "redis", "asyncio", "cache"
]

db_vektor = MiniVectorDatabase(KOSAKATA_AI)

# Ingest data pengetahuan ke database vektor
db_vektor.tambah_dokumen(
    "DOC-1",
    "Django ORM menyediakan abstraksi database relasional seperti PostgreSQL dan SQLite.",
    {"topik": "Backend Web"}
)
db_vektor.tambah_dokumen(
    "DOC-2",
    "RAG atau Retrieval-Augmented Generation menggabungkan pencarian dokumen semantik dengan prompt model AI.",
    {"topik": "Generative AI"}
)
db_vektor.tambah_dokumen(
    "DOC-3",
    "Asyncio di Python digunakan untuk menangani ribuan koneksi concurrent I/O secara non-blocking.",
    {"topik": "Python Mahir"}
)

print(f"Total Dokumen di Vector DB: {len(db_vektor.koleksi)}")


# ------------------------------------------------------------------------------
# 3. Pipeline RAG (Retrieval-Augmented Generation)
# ------------------------------------------------------------------------------
print("\n--- [2] Simulasi Pipeline RAG ---")

def pipeline_rag(pertanyaan_user: str) -> str:
    print(f"❓ Pertanyaan Pengguna: '{pertanyaan_user}'")
    # Langkah 1: Retrieval (Mengambil konteks paling relevan)
    hasil_retrieval = db_vektor.cari_kemiripan(pertanyaan_user, top_k=1)
    
    if not hasil_retrieval or hasil_retrieval[0][1] < 0.1:
        konteks = "Tidak ada dokumen yang relevan di basis data."
    else:
        chunk_terpilih, kemiripan = hasil_retrieval[0]
        print(f"🔍 Konteks Ditemukan (Skor Kemiripan: {kemiripan:.3f}):\n   '{chunk_terpilih.konten}'")
        konteks = chunk_terpilih.konten

    # Langkah 2: Prompt Augmentation
    augmented_prompt = (
        f"[SYSTEM]: Anda adalah asisten AI teknis. Jawab hanya berdasarkan konteks berikut:\n"
        f"[KONTEKS]: {konteks}\n"
        f"[PERTANYAAN]: {pertanyaan_user}\n"
        f"[JAWABAN]:"
    )
    
    # Langkah 3: Generation (Simulasi respons sintesis LLM)
    respons_sintesis = (
        f"Berdasarkan dokumen teknis perusahaan kami, {konteks.lower()}"
    )
    return respons_sintesis

jawaban_rag = pipeline_rag("Bagaimana cara kerja RAG dalam prompt AI?")
print(f"💡 Jawaban Akhir RAG:\n{jawaban_rag}")


# ------------------------------------------------------------------------------
# 4. Pola Autonomous Agent & Tool Calling (ReAct Pattern)
# ------------------------------------------------------------------------------
print("\n--- [3] Autonomous Agent dengan Dynamic Tool Calling (ReAct Pattern) ---")

# A. Definisi Tool-Tool yang dapat digunakan oleh Agent
def tool_kalkulator(ekspresi: str) -> str:
    """Menghitung ekspresi matematika."""
    try:
        # Bersihkan hanya karakter aman
        if not re.match(r'^[\d\s\+\-\*\/\(\)\.]+$', ekspresi):
            return "Error: Karakter tidak aman!"
        return str(eval(ekspresi))
    except Exception as e:
        return f"Error: {e}"

def tool_cek_kurs_dollar(mata_uang: str) -> str:
    """Mengambil kurs mata uang terkini."""
    kurs = {"IDR": 15850, "JPY": 152, "EUR": 0.92}
    return f"1 USD = {kurs.get(mata_uang.upper(), 'Tidak diketahui')} {mata_uang.upper()}"

DAFTAR_TOOLS: dict[str, tuple[Callable, str]] = {
    "kalkulator": (tool_kalkulator, "Gunakan untuk operasi hitung matematika. Argumen: ekspresi string"),
    "cek_kurs": (tool_cek_kurs_dollar, "Gunakan untuk melihat kurs tukar mata uang USD. Argumen: kode mata uang (contoh: IDR)")
}

# B. Agent Orchestrator Loop
class AutonomousAgent:
    def __init__(self, tools: dict) -> None:
        self.tools = tools

    def eksekusi_tugas(self, instruksi_user: str) -> str:
        print(f"\n🎯 [Agent Diberi Tugas]: '{instruksi_user}'")
        
        # Langkah 1: Reasoning (Penalaran Agen)
        if "kurs" in instruksi_user.lower() and "dollar" in instruksi_user.lower():
            alat = "cek_kurs"
            argumen = "IDR"
        elif any(c in instruksi_user for c in ["+", "-", "*", "/"]):
            alat = "kalkulator"
            # Ekstrak rumus
            match = re.search(r'[\d\s\+\-\*\/\.]+', instruksi_user)
            argumen = match.group(0).strip() if match else "0"
        else:
            return "Agent: Maaf, saya belum memiliki alat (tool) yang sesuai untuk permintaan ini."

        # Langkah 2: Action (Pemanggilan Tool)
        fungsi_tool, deskripsi = self.tools[alat]
        print(f"🤖 [Agent Memutuskan Action]: Memanggil tool '{alat}' dengan parameter '{argumen}'")
        
        # Langkah 3: Observation (Mengamati hasil eksekusi alat)
        observasi = fungsi_tool(argumen)
        print(f"👀 [Agent Mengamati Output Tool]: {observasi}")

        # Langkah 4: Final Synthesis
        return f"Agen Selesai: Berdasarkan alat '{alat}', hasil yang didapatkan adalah: {observasi}"

agent = AutonomousAgent(DAFTAR_TOOLS)
print(agent.eksekusi_tugas("Berapa kurs dollar ke rupiah IDR saat ini?"))
print(agent.eksekusi_tugas("Bisa tolong hitungkan 25000 * 4 + 1500?"))


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 04 (AI MODERN):")
print("1. Vector Database bekerja dengan mencocokkan kedekatan sudut embedding (Cosine Similarity).")
print("2. RAG memecahkan masalah halusinasi LLM dengan menyuntikkan dokumen faktual terkini ke prompt.")
print("3. Agen AI otonom mengandalkan siklus ReAct: Thought -> Action (Tool) -> Observation -> Response.")
print("4. Selalu batasi akses Tool pada Agent dengan validasi skema ketat untuk keamanan sistem.")
print("=" * 70)
