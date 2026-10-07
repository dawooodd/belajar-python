"""
================================================================================
MODUL 01: DASAR PEMROGRAMAN PYTHON
FILE 07: Latihan Tantangan Praktis & Evaluasi Otomatis (Self-Assessment)
================================================================================
File ini berisi 5 studi kasus pemecahan masalah algoritma & struktur data dasar
yang sering dijumpai dalam technical interview dan proyek nyata.
Dilengkapi fungsi verifikasi otomatis (assert test suite) untuk menguji hasil.
================================================================================
"""

from collections import defaultdict
import string

print("=" * 70)
print("🎯 MODUL 01: SUITE EVALUASI DAN LATIHAN TANTANGAN ALGORITMA")
print("=" * 70)

# ==============================================================================
# TANTANGAN 1: Pembersih Teks & Deteksi Palindrom
# Deskripsi: Mengabaikan spasi, tanda baca, dan huruf besar/kecil.
# Contoh: "Kasur ini rusak" -> True
# ==============================================================================

def is_palindrom(teks: str) -> bool:
    """Memeriksa apakah string adalah palindrom setelah dibersihkan."""
    tanda_baca = set(string.punctuation + " ")
    teks_bersih = "".join(c.lower() for c in teks if c not in tanda_baca)
    return teks_bersih == teks_bersih[::-1]


# ==============================================================================
# TANTANGAN 2: Pengelompokan Anagram (Group Anagrams)
# Input : ["eat", "tea", "tan", "ate", "nat", "bat"]
# Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
# Kompleksitas: O(N * K log K)
# ==============================================================================

def group_anagrams(daftar_kata: list[str]) -> list[list[str]]:
    """Mengelompokkan kata-kata yang merupakan anagram satu sama lain."""
    kelompok = defaultdict(list)
    for kata in daftar_kata:
        kunci_terurut = "".join(sorted(kata.lower()))
        kelompok[kunci_terurut].append(kata)
    return list(kelompok.values())


# ==============================================================================
# TANTANGAN 3: Dua Angka yang Menghasilkan Target (Two Sum)
# Temukan indeks dua angka yang jika dijumlahkan bernilai sama dengan target.
# Gunakan hash map (dict) untuk mencapai kecepatan O(N) alih-alih O(N^2).
# ==============================================================================

def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Mengembalikan pasangan indeks (i, j) yang nilainya jika dijumlah = target."""
    seen: dict[int, int] = {}
    for i, num in enumerate(nums):
        selisih = target - num
        if selisih in seen:
            return (seen[selisih], i)
        seen[num] = i
    return None


# ==============================================================================
# TANTANGAN 4: Kompresi String Run-Length Simple
# Contoh: "AAABBBCCCDD" -> "A3B3C3D2"
# Jika hasil kompresi tidak lebih pendek dari teks asli, kembalikan teks asli.
# ==============================================================================

def kompresi_string(s: str) -> str:
    """Melakukan kompresi string sederhana berbasis frekuensi berurutan."""
    if not s:
        return ""
    
    hasil = []
    karakter_sekarang = s[0]
    hitung = 1
    
    for c in s[1:]:
        if c == karakter_sekarang:
            hitung += 1
        else:
            hasil.append(f"{karakter_sekarang}{hitung}")
            karakter_sekarang = c
            hitung = 1
    hasil.append(f"{karakter_sekarang}{hitung}")
    
    terkompresi = "".join(hasil)
    return terkompresi if len(terkompresi) < len(s) else s


# ==============================================================================
# TANTANGAN 5: Rotasi Matriks 90 Derajat Searah Jarum Jam
# Matriks N x N.
# ==============================================================================

def putar_matriks_90(matriks: list[list[int]]) -> list[list[int]]:
    """Memutar matriks N x N 90 derajat searah jarum jam."""
    # Langkah 1: Transpos matriks (tukar baris jadi kolom)
    # Langkah 2: Balik setiap baris (reverse)
    n = len(matriks)
    # Shallow clone agar matriks asli tidak bermutasi
    hasil = [baris[:] for baris in matriks]
    for i in range(n):
        for j in range(i, n):
            hasil[i][j], hasil[j][i] = hasil[j][i], hasil[i][j]
    for i in range(n):
        hasil[i].reverse()
    return hasil


# ==============================================================================
# TEST SUITE OTOMATIS: Menjalankan Seluruh Kasus Uji
# ==============================================================================

def jalankan_pengujian():
    print("Memulai verifikasi otomatis kode Anda...\n")
    skor_lulus = 0
    total_soal = 5

    # Test 1
    assert is_palindrom("Kasur ini rusak") is True, "Test 1A Gagal"
    assert is_palindrom("A man, a plan, a canal: Panama") is True, "Test 1B Gagal"
    assert is_palindrom("Belajar Python") is False, "Test 1C Gagal"
    print("✅ Tantangan 1: Deteksi Palindrom LULUS!")
    skor_lulus += 1

    # Test 2
    hasil_anagram = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
    assert len(hasil_anagram) == 3, "Test 2 Gagal"
    print("✅ Tantangan 2: Pengelompokan Anagram LULUS!")
    skor_lulus += 1

    # Test 3
    idx = two_sum([2, 7, 11, 15], 9)
    assert idx == (0, 1), f"Test 3 Gagal: {idx}"
    idx2 = two_sum([3, 2, 4], 6)
    assert idx2 == (1, 2), f"Test 3B Gagal: {idx2}"
    print("✅ Tantangan 3: Two Sum Algoritma O(N) LULUS!")
    skor_lulus += 1

    # Test 4
    assert kompresi_string("aabcccccaaa") == "a2b1c5a3", "Test 4A Gagal"
    assert kompresi_string("abcd") == "abcd", "Test 4B Gagal (panjang sama/lebih)"
    print("✅ Tantangan 4: Kompresi Teks LULUS!")
    skor_lulus += 1

    # Test 5
    m_awal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]
    m_rotasi = putar_matriks_90(m_awal)
    m_target = [
        [7, 4, 1],
        [8, 5, 2],
        [9, 6, 3]
    ]
    assert m_rotasi == m_target, f"Test 5 Gagal: {m_rotasi}"
    print("✅ Tantangan 5: Rotasi Matriks 90 Derajat LULUS!")
    skor_lulus += 1

    print("\n" + "=" * 70)
    print(f"🎉 SEMPURNA! Skor Evaluasi: {skor_lulus}/{total_soal} (100% Berhasil)")
    print("Fondasi Modul 01 Anda sudah sangat solid untuk melangkah ke Modul 02 (Menengah)!")
    print("=" * 70)


if __name__ == "__main__":
    jalankan_pengujian()
