from database import get_connection
from mysql.connector import Error


# ═══════════════════════════════════════════════════════════
# PROGRAM YÖNETİMİ
# ═══════════════════════════════════════════════════════════

def admin_get_programs() -> list:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.program_id, p.program_adi, p.program_tipi, p.yayin_yili,
                   p.bolum_sayisi, p.bolum_uzunluk_dk, p.aciklama,
                   p.ortalama_puan, p.toplam_izlenme,
                   GROUP_CONCAT(t.tur_adi ORDER BY t.tur_adi SEPARATOR ', ') AS turler
            FROM Program p
            LEFT JOIN ProgramTur pt ON p.program_id = pt.program_id
            LEFT JOIN Tur t         ON pt.tur_id = t.tur_id
            GROUP BY p.program_id
            ORDER BY p.program_adi
        """)
        rows = cursor.fetchall()
        cursor.close(); conn.close()
        return rows
    except Error as e:
        print(f"admin_get_programs hata: {e}")
        return []


def admin_add_program(program_adi, aciklama, program_tipi, yayin_yili,
                      bolum_sayisi, bolum_uzunluk_dk, tur_ids: list) -> tuple:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Program (program_adi, aciklama, program_tipi, yayin_yili,
                                 bolum_sayisi, bolum_uzunluk_dk)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (program_adi, aciklama, program_tipi, yayin_yili,
              bolum_sayisi, bolum_uzunluk_dk))
        program_id = cursor.lastrowid
        for tur_id in tur_ids:
            cursor.execute(
                "INSERT INTO ProgramTur (program_id, tur_id) VALUES (%s,%s)",
                (program_id, tur_id)
            )
        conn.commit(); cursor.close(); conn.close()
        return True, None
    except Error as e:
        return False, str(e)


def admin_update_program(program_id, program_adi, aciklama, program_tipi,
                         yayin_yili, bolum_sayisi, bolum_uzunluk_dk,
                         tur_ids: list) -> tuple:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Program
            SET program_adi=%s, aciklama=%s, program_tipi=%s, yayin_yili=%s,
                bolum_sayisi=%s, bolum_uzunluk_dk=%s
            WHERE program_id=%s
        """, (program_adi, aciklama, program_tipi, yayin_yili,
              bolum_sayisi, bolum_uzunluk_dk, program_id))

        # Türleri sil + yeniden ekle
        cursor.execute("DELETE FROM ProgramTur WHERE program_id=%s", (program_id,))
        for tur_id in tur_ids:
            cursor.execute(
                "INSERT INTO ProgramTur (program_id, tur_id) VALUES (%s,%s)",
                (program_id, tur_id)
            )
        conn.commit(); cursor.close(); conn.close()
        return True, None
    except Error as e:
        return False, str(e)


def admin_delete_program(program_id) -> tuple:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Program WHERE program_id=%s", (program_id,))
        conn.commit(); cursor.close(); conn.close()
        return True, None
    except Error as e:
        return False, str(e)


# ═══════════════════════════════════════════════════════════
# TÜR YÖNETİMİ
# ═══════════════════════════════════════════════════════════

def admin_get_turler() -> list:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.tur_id, t.tur_adi,
                   COUNT(DISTINCT pt.program_id) AS program_sayisi
            FROM Tur t
            LEFT JOIN ProgramTur pt ON t.tur_id = pt.tur_id
            GROUP BY t.tur_id
            ORDER BY t.tur_adi
        """)
        rows = cursor.fetchall()
        cursor.close(); conn.close()
        return rows
    except Error as e:
        print(f"admin_get_turler hata: {e}")
        return []


def admin_add_tur(tur_adi: str) -> tuple:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Tur (tur_adi) VALUES (%s)", (tur_adi,))
        conn.commit(); cursor.close(); conn.close()
        return True, None
    except Error as e:
        return False, str(e)


def admin_update_tur(tur_id: int, tur_adi: str) -> tuple:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE Tur SET tur_adi=%s WHERE tur_id=%s", (tur_adi, tur_id))
        conn.commit(); cursor.close(); conn.close()
        return True, None
    except Error as e:
        return False, str(e)


def admin_delete_tur(tur_id: int) -> tuple:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Bağlı içerik kontrolü
        cursor.execute(
            "SELECT COUNT(*) AS cnt FROM ProgramTur WHERE tur_id=%s", (tur_id,)
        )
        cnt = cursor.fetchone()["cnt"]
        if cnt > 0:
            cursor.close(); conn.close()
            return False, f"Bu türe bağlı {cnt} içerik var. Önce içerikleri güncelleyiniz."

        cursor.execute("DELETE FROM Tur WHERE tur_id=%s", (tur_id,))
        conn.commit(); cursor.close(); conn.close()
        return True, None
    except Error as e:
        return False, str(e)


# ═══════════════════════════════════════════════════════════
# KULLANICI YÖNETİMİ
# ═══════════════════════════════════════════════════════════

def admin_get_kullanicilar() -> list:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT k.kullanici_id, k.ad, k.soyad, k.email,
                   k.ulke, k.kayit_tarihi, k.aktif, r.rol_adi,
                   COALESCE(SUM(kp.toplam_sure_dk), 0) AS toplam_sure_dk,
                   COUNT(DISTINCT kp.program_id)        AS izlenen_icerik
            FROM Kullanici k
            JOIN Rol r ON k.rol_id = r.rol_id
            LEFT JOIN KullaniciProgram kp ON k.kullanici_id = kp.kullanici_id
            GROUP BY k.kullanici_id
            ORDER BY k.kayit_tarihi DESC
        """)
        rows = cursor.fetchall()
        cursor.close(); conn.close()
        return rows
    except Error as e:
        print(f"admin_get_kullanicilar hata: {e}")
        return []


def admin_get_kullanici_detay(kullanici_id: int) -> dict | None:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT k.*, r.rol_adi,
                   COALESCE(SUM(kp.toplam_sure_dk), 0)  AS toplam_sure_dk,
                   COUNT(DISTINCT kp.program_id)         AS izlenen_icerik,
                   ROUND(AVG(kp.puan), 1)                AS ort_puan
            FROM Kullanici k
            JOIN Rol r ON k.rol_id = r.rol_id
            LEFT JOIN KullaniciProgram kp ON k.kullanici_id = kp.kullanici_id
            WHERE k.kullanici_id = %s
            GROUP BY k.kullanici_id
        """, (kullanici_id,))
        row = cursor.fetchone()

        if row:
            # Favori türler
            cursor.execute("""
                SELECT t.tur_adi FROM KullaniciTur kt
                JOIN Tur t ON kt.tur_id = t.tur_id
                WHERE kt.kullanici_id = %s
            """, (kullanici_id,))
            row["favori_turler"] = [r["tur_adi"] for r in cursor.fetchall()]

        cursor.close(); conn.close()
        return row
    except Error as e:
        print(f"admin_get_kullanici_detay hata: {e}")
        return None


def admin_get_kullanici_gecmis(kullanici_id: int) -> list:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.program_adi, p.program_tipi,
                   il.bolum_no, il.izleme_tarihi, il.izlenen_dk, il.tamamlandi,
                   kp.puan
            FROM IzlemeLog il
            JOIN Program p ON il.program_id = p.program_id
            LEFT JOIN KullaniciProgram kp
                   ON kp.program_id = il.program_id AND kp.kullanici_id = il.kullanici_id
            WHERE il.kullanici_id = %s
            ORDER BY il.izleme_tarihi DESC
        """, (kullanici_id,))
        rows = cursor.fetchall()
        cursor.close(); conn.close()
        return rows
    except Error as e:
        return []


def admin_toggle_aktif(kullanici_id: int, aktif: bool) -> tuple:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Kullanici SET aktif=%s WHERE kullanici_id=%s",
            (1 if aktif else 0, kullanici_id)
        )
        conn.commit(); cursor.close(); conn.close()
        return True, None
    except Error as e:
        return False, str(e)
