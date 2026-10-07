"""
================================================================================
MODUL 03: TINGKAT MAHIR (ADVANCED PYTHON)
FILE 03: Asynchronous Programming (asyncio), TaskGroup & Structured Concurrency
================================================================================
Tujuan Pembelajaran:
1. Memahami Event Loop, Coroutine, dan mekanisme Non-blocking I/O.
2. Menguasai asyncio.gather() dan asyncio.TaskGroup (Python 3.11+ Structured Concurrency).
3. Membuat Async Context Manager (__aenter__, __aexit__).
4. Pola Produsen-Konsumen (Producer-Consumer) menggunakan asyncio.Queue.
5. Manajemen Timeout dan pembatalan task secara elegan.
================================================================================
"""

import asyncio
import time
from typing import Any

print("=" * 70)
print("--- [1] Coroutine Sederhana & Non-blocking Sleep ---")

async def fetch_data(sumber: str, delay: float) -> dict[str, Any]:
    print(f"📡 [Mulai Request] Sumber: {sumber}...")
    await asyncio.sleep(delay)  # Melepaskan kendali kembali ke event loop secara non-blocking
    print(f"✅ [Selesai] Sumber: {sumber} ({delay}s)")
    return {"sumber": sumber, "data": f"Payload dari {sumber}"}


# ------------------------------------------------------------------------------
# 2. Modern Structured Concurrency: asyncio.TaskGroup (Python 3.11+)
# ------------------------------------------------------------------------------
async def demo_task_group():
    print("\n--- [2] Structured Concurrency: asyncio.TaskGroup ---")
    waktu_mulai = time.perf_counter()

    # TaskGroup menjamin bahwa jika satu task gagal, task lain dalam grup akan
    # dibatalkan secara bersih dan error dibungkus dalam ExceptionGroup.
    async with asyncio.TaskGroup() as tg:
        t1 = tg.create_task(fetch_data("API Pembayaran", 0.3))
        t2 = tg.create_task(fetch_data("API Inventori", 0.2))
        t3 = tg.create_task(fetch_data("API Rekomendasi AI", 0.4))

    total_waktu = time.perf_counter() - waktu_mulai
    print(f"\nSemua task selesai secara bersamaan dalam {total_waktu:.3f} detik!")
    print(f"Hasil T1: {t1.result()}")
    print(f"Hasil T2: {t2.result()}")
    print(f"Hasil T3: {t3.result()}")


# ------------------------------------------------------------------------------
# 3. Async Context Manager & Async Iterator
# ------------------------------------------------------------------------------
class KoneksiWebSocketAsync:
    """Simulasi koneksi websocket async dengan protokol __aenter__ dan __aexit__."""
    async def __aenter__(self):
        print("\n🔌 [WebSocket] Membuka koneksi...")
        await asyncio.sleep(0.1)
        print("🔌 [WebSocket] Terhubung!")
        return self

    async def kirim_pesan(self, pesan: str) -> None:
        print(f"  -> Mengirim: {pesan}")
        await asyncio.sleep(0.05)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("🔌 [WebSocket] Menutup koneksi secara aman...")
        await asyncio.sleep(0.05)
        print("🔌 [WebSocket] Koneksi ditutup.")


# ------------------------------------------------------------------------------
# 4. Pola Produsen - Konsumen (Producer-Consumer dengan asyncio.Queue)
# ------------------------------------------------------------------------------
async def produsen(antrean: asyncio.Queue, jumlah: int):
    for i in range(1, jumlah + 1):
        item = f"Pekerjaan-#{i}"
        await antrean.put(item)
        print(f"🏭 Produsen memasukkan: {item}")
        await asyncio.sleep(0.1)
    # Sentinel penanda selesai untuk worker
    await antrean.put(None)

async def konsumen(antrean: asyncio.Queue):
    while True:
        item = await antrean.get()
        if item is None:
            antrean.task_done()
            break
        print(f"⚙️  Konsumen memproses: {item}")
        await asyncio.sleep(0.15)
        antrean.task_done()


# ------------------------------------------------------------------------------
# Master Runner
# ------------------------------------------------------------------------------
async def main():
    # 1. Jalankan demo TaskGroup
    await demo_task_group()

    # 2. Uji Async Context Manager
    async with KoneksiWebSocketAsync() as ws:
        await ws.kirim_pesan("AUTH_TOKEN_XYZ")
        await ws.kirim_pesan("SUBSCRIBE_MARKET_TICKER")

    # 3. Uji Producer-Consumer Queue
    print("\n--- [3] Pola Producer-Consumer Queue ---")
    antrean: asyncio.Queue = asyncio.Queue()
    await asyncio.gather(
        produsen(antrean, 3),
        konsumen(antrean)
    )

if __name__ == "__main__":
    asyncio.run(main())
    print("\n" + "=" * 70)
    print("✅ KESIMPULAN & BEST PRACTICE FILE 03 (MAHIR):")
    print("1. Gunakan asyncio untuk aplikasi web server, microservice I/O intensif, dan websocket.")
    print("2. Hindari `time.sleep()` di dalam async function — selalu gunakan `await asyncio.sleep()`.")
    print("3. Di Python 3.11+, gunakan `asyncio.TaskGroup()` untuk structured concurrency yang tangguh.")
    print("4. Manfaatkan `asyncio.Queue` untuk memisahkan beban kerja antara penghasil data dan pemroses data.")
    print("=" * 70)
