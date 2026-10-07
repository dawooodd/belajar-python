"""
================================================================================
MODUL 01: DASAR PEMROGRAMAN PYTHON
FILE 02: Operator, Ekspresi, Presedensi & Walrus Operator (:=)
================================================================================
Tujuan Pembelajaran:
1. Memahami operator aritmatika, pembagian float vs floor division (//).
2. Mekanisme Short-Circuit Evaluation pada operator logika (and, or).
3. Operator Bitwise dan penerapannya pada sistem Permission/Flags.
4. Penggunaan Walrus Operator (:=) untuk efisiensi komputasi dalam if/while.
5. Memahami Presedensi Operator agar tidak terjadi bug logika tersembunyi.
================================================================================
"""

# ------------------------------------------------------------------------------
# 1. Operator Aritmatika & Perbedaan Pembagian
# ------------------------------------------------------------------------------
print("=" * 70)
print("--- [1] Operator Aritmatika & Pembagian ---")

a = 17
b = 5

print(f"Penjumlahan ({a} + {b})       = {a + b}")
print(f"Pengurangan ({a} - {b})       = {a - b}")
print(f"Perkalian ({a} * {b})         = {a * b}")
print(f"Pembagian Float ({a} / {b})   = {a / b} (Hasil selalu float)")
print(f"Floor Division ({a} // {b})   = {a // b} (Pembulatan ke bawah)")
print(f"Modulus/Sisa Bagi ({a} % {b}) = {a % b}")
print(f"Pangkat ({a} ** {b})          = {a ** b}")

# Catatan penting pembagian bilangan negatif:
# Floor division selalu membulatkan ke arah minus tak hingga
print(f"-17 // 5 = {-17 // 5}  (Bukan -3, melainkan -4 karena dibulatkan ke bawah)")


# ------------------------------------------------------------------------------
# 2. Operator Logika & Short-Circuit Evaluation
# ------------------------------------------------------------------------------
print("\n--- [2] Short-Circuit Evaluation (and, or) ---")
# 'and' akan langsung berhenti jika operand pertama FALSY (karena hasil pasti False)
# 'or'  akan langsung berhenti jika operand pertama TRUTHY (karena hasil pasti True)

def fungsi_berat() -> bool:
    print("  -> [PERINGATAN] Fungsi berat dijalankan!")
    return True

print("Kasus 1: False and fungsi_berat()")
hasil_1 = False and fungsi_berat()
print(f"Hasil: {hasil_1} (fungsi_berat TIDAK dieksekusi)")

print("\nKasus 2: True or fungsi_berat()")
hasil_2 = True or fungsi_berat()
print(f"Hasil: {hasil_2} (fungsi_berat TIDAK dieksekusi)")

# Nilai balik ekspresi logika di Python mengembalikan OPERAND TERAKHIR YANG DIEVALUASI,
# bukan sekadar True/False!
nama_default = "" or "Guest"  # "" adalah falsy, berlanjut ke "Guest"
print(f"\nNilai default pattern: {nama_default=}")


# ------------------------------------------------------------------------------
# 3. Bitwise Operator & Implementasi Real-World Permission Flag
# ------------------------------------------------------------------------------
print("\n--- [3] Bitwise Operator & Sistem Role / Permission ---")
# Dalam sistem backend berskala besar, izin sering disimpan dalam bentuk bit flags (int)
# 1 = Read (001), 2 = Write (010), 4 = Delete (100), 8 = Admin (1000)

PERM_READ   = 1 << 0  # 1 (0001)
PERM_WRITE  = 1 << 1  # 2 (0010)
PERM_DELETE = 1 << 2  # 4 (0100)
PERM_ADMIN  = 1 << 3  # 8 (1000)

# Memberi izin baca dan tulis ke user menggunakan bitwise OR (|)
user_permissions = PERM_READ | PERM_WRITE
print(f"User Permissions Bitmask: {bin(user_permissions)} (Desimal: {user_permissions})")

# Memeriksa izin menggunakan bitwise AND (&)
bisa_baca = (user_permissions & PERM_READ) != 0
bisa_hapus = (user_permissions & PERM_DELETE) != 0
print(f"Apakah user boleh READ?   : {bisa_baca}")
print(f"Apakah user boleh DELETE? : {bisa_hapus}")

# Mencabut izin tulis menggunakan bitwise AND dengan bitwise NOT (~)
user_permissions &= ~PERM_WRITE
bisa_tulis = (user_permissions & PERM_WRITE) != 0
print(f"Setelah izin tulis dicabut, boleh WRITE? : {bisa_tulis}")


# ------------------------------------------------------------------------------
# 4. Walrus Operator (:=) (Assignment Expressions - PEP 572)
# ------------------------------------------------------------------------------
print("\n--- [4] Walrus Operator (:=) ---")
# Memungkinkan assignment nilai ke variabel DI DALAM ekspresi kondisi

data_teks = "Python Mastery 2026"

# CARA LAMA (2 Langkah):
panjang = len(data_teks)
if panjang > 10:
    print(f"[Cara Lama] Teks panjang: {panjang} karakter")

# CARA MODERN DENGAN WALRUS OPERATOR (1 Langkah):
if (n := len(data_teks)) > 10:
    print(f"[Walrus Operator] Teks panjang: {n} karakter (variabel 'n' tersimpan)")

# Contoh praktis pada list filtering:
angka_list = [10, 25, 30, 45, 50, 65, 80]
# Menghitung kuadrat hanya jika kuadrat > 1000 dan langsung simpan nilainya
kuadrat_besar = [kuadrat for x in angka_list if (kuadrat := x**2) > 1000]
print(f"Kuadrat > 1000: {kuadrat_besar}")


# ------------------------------------------------------------------------------
# 5. Presedensi Operator
# ------------------------------------------------------------------------------
print("\n--- [5] Presedensi Operator & Pentingnya Kurung () ---")
# Urutan prioritas dari tertinggi ke terendah:
# 1. () Tanda kurung
# 2. ** Pangkat
# 3. +x, -x, ~x (Unary)
# 4. *, /, //, % (Perkalian & Pembagian)
# 5. +, - (Penjumlahan & Pengurangan)
# 6. <<, >> (Bitwise Shift)
# 7. & (Bitwise AND)
# 8. ^ (Bitwise XOR)
# 9. | (Bitwise OR)
# 10. ==, !=, <, <=, >, >=, in, is (Perbandingan)
# 11. not, and, or (Logika)
# 12. := (Walrus)

hasil_tanpa_kurung = 5 + 3 * 2 ** 3
hasil_dengan_kurung = (5 + 3) * (2 ** 3)
print(f"5 + 3 * 2 ** 3       = {hasil_tanpa_kurung}  (2**3=8 -> 3*8=24 -> 5+24=29)")
print(f"(5 + 3) * (2 ** 3)   = {hasil_dengan_kurung}  (8 * 8 = 64)")


print("\n" + "=" * 70)
print("✅ KESIMPULAN & BEST PRACTICE FILE 02:")
print("1. Gunakan // jika Anda mengharapkan hasil bilangan bulat tanpa fraksi.")
print("2. Manfaatkan Short-circuit evaluation untuk guard clause (misal: if obj and obj.is_valid:).")
print("3. Gunakan bitwise flags jika performa dan hemat memori pada state sangat krusial.")
print("4. Gunakan Walrus Operator (:=) untuk mencegah evaluasi ganda fungsi yang lambat.")
print("5. Jangan ragu menggunakan tanda kurung () eksplisit demi keterbacaan tim engineer.")
print("=" * 70)
