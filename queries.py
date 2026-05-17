from database import get_connection
from mysql.connector import Error


def get_favoriler(kullanici_id: int) -> list:
    """Kullanıcının favori içeriklerini türleriyle birlikte döner."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                p.program_id, p.program_adi, p.program_tipi,
                p.yayin_yili, p.bolum_sayisi, p.bolum_uzunluk_dk,
                p.ortalama_puan, p.toplam_izlenme,
                f.ekleme_tarihi,
                GROUP_CONCAT(t.tur_adi ORDER BY t.tur_adi SEPARATOR ', ') AS turler
            FROM Favori f
            JOIN Program p    ON f.program_id = p.program_id
            LEFT JOIN ProgramTur pt ON p.program_id = pt.program_id
            LEFT JOIN Tur t         ON pt.tur_id = t.tur_id
            WHERE f.kullanici_id = %s
            GROUP BY p.program_id, f.ekleme_tarihi
            ORDER BY f.ekleme_tarihi DESC
        """, (kullanici_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        print(f"get_favoriler hata: {e}")
        return []


def get_profil(kullanici_id: int) -> dict | None:
    """Kullanıcının profil bilgilerini ve istatistiklerini döner."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Temel bilgiler + istatistikler
        cursor.execute("""
            SELECT
                k.kullanici_id, k.ad, k.soyad, k.email,
                k.dogum_tarihi, k.cinsiyet, k.ulke, k.kayit_tarihi,
                COALESCE(SUM(kp.toplam_sure_dk), 0)      AS toplam_sure_dk,
                COUNT(DISTINCT kp.program_id)             AS izlenen_icerik,
                ROUND(AVG(kp.puan), 1)                   AS ortalama_puan
            FROM Kullanici k
            LEFT JOIN KullaniciProgram kp ON k.kullanici_id = kp.kullanici_id
            WHERE k.kullanici_id = %s
            GROUP BY k.kullanici_id
        """, (kullanici_id,))
        profil = cursor.fetchone()

        if profil:
            # Favori türler
            cursor.execute("""
                SELECT t.tur_id, t.tur_adi
                FROM KullaniciTur kt
                JOIN Tur t ON kt.tur_id = t.tur_id
                WHERE kt.kullanici_id = %s
            """, (kullanici_id,))
            profil["favori_turler"] = cursor.fetchall()

        cursor.close()
        conn.close()
        return profil
    except Error as e:
        print(f"get_profil hata: {e}")
        return None


def update_profil(kullanici_id: int, ad: str, soyad: str, email: str,
                  dogum_tarihi, ulke: str, cinsiyet: str) -> tuple:
    """Kullanıcının temel bilgilerini günceller."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # E-mail başkasına ait mi?
        cursor.execute(
            "SELECT kullanici_id FROM Kullanici WHERE email=%s AND kullanici_id != %s",
            (email, kullanici_id)
        )
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Bu e-mail adresi başka bir kullanıcıya aittir."

        cursor.execute("""
            UPDATE Kullanici
            SET ad=%s, soyad=%s, email=%s, dogum_tarihi=%s, ulke=%s, cinsiyet=%s
            WHERE kullanici_id=%s
        """, (ad, soyad, email, dogum_tarihi, ulke, cinsiyet, kullanici_id))
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        return False, str(e)


def update_sifre(kullanici_id: int, eski_sifre: str, yeni_sifre: str) -> tuple:
    """Şifreyi doğrulayıp günceller."""
    import bcrypt
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT sifre_hash FROM Kullanici WHERE kullanici_id=%s",
            (kullanici_id,)
        )
        row = cursor.fetchone()
        if not row:
            cursor.close(); conn.close()
            return False, "Kullanıcı bulunamadı."

        if not bcrypt.checkpw(eski_sifre.encode(), row["sifre_hash"].encode()):
            cursor.close(); conn.close()
            return False, "Mevcut şifre hatalı."

        yeni_hash = bcrypt.hashpw(yeni_sifre.encode(), bcrypt.gensalt()).decode()
        cursor.execute(
            "UPDATE Kullanici SET sifre_hash=%s WHERE kullanici_id=%s",
            (yeni_hash, kullanici_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        return False, str(e)


def update_favori_turler(kullanici_id: int, tur_ids: list) -> tuple:
    """Kullanıcının favori türlerini günceller (sil + tekrar ekle)."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM KullaniciTur WHERE kullanici_id=%s", (kullanici_id,))
        for tur_id in tur_ids:
            cursor.execute(
                "INSERT INTO KullaniciTur (kullanici_id, tur_id) VALUES (%s,%s)",
                (kullanici_id, tur_id)
            )
        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        return False, str(e)


def get_all_programs(kullanici_id: int) -> list:
    """Tüm programları türleriyle, favori ve izleme durumunu birlikte döner."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT
                p.program_id,
                p.program_adi,
                p.program_tipi,
                p.yayin_yili,
                p.bolum_sayisi,
                p.bolum_uzunluk_dk,
                p.ortalama_puan,
                p.toplam_izlenme,
                GROUP_CONCAT(t.tur_adi ORDER BY t.tur_adi SEPARATOR ', ') AS turler,
                IF(f.favori_id IS NOT NULL, 1, 0)  AS favori,
                IF(kp.kp_id IS NOT NULL, 1, 0)     AS izlendi,
                COALESCE(kp.tamamlandi, 0)         AS tamamlandi
            FROM Program p
            LEFT JOIN ProgramTur pt  ON p.program_id = pt.program_id
            LEFT JOIN Tur t          ON pt.tur_id = t.tur_id
            LEFT JOIN Favori f       ON p.program_id = f.program_id AND f.kullanici_id = %s
            LEFT JOIN KullaniciProgram kp ON p.program_id = kp.program_id AND kp.kullanici_id = %s
            GROUP BY p.program_id
            ORDER BY p.program_adi
        """, (kullanici_id, kullanici_id))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error as e:
        print(f"get_all_programs hata: {e}")
        return []


def toggle_favori(kullanici_id: int, program_id: int) -> bool:
    """Favori yoksa ekler, varsa çıkarır. Güncel durum (True=favori) döner."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT favori_id FROM Favori WHERE kullanici_id=%s AND program_id=%s",
            (kullanici_id, program_id)
        )
        row = cursor.fetchone()
        if row:
            cursor.execute("DELETE FROM Favori WHERE kullanici_id=%s AND program_id=%s",
                           (kullanici_id, program_id))
            conn.commit()
            result = False
        else:
            cursor.execute("INSERT INTO Favori (kullanici_id, program_id) VALUES (%s, %s)",
                           (kullanici_id, program_id))
            conn.commit()
            result = True
        cursor.close()
        conn.close()
        return result
    except Error as e:
        print(f"toggle_favori hata: {e}")
        return False


def get_watching_state(kullanici_id: int, program_id: int) -> dict | None:
    """Kullanıcının bu programdaki kaldığı yeri döner."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT son_bolum_no, son_izleme_dk, tamamlandi
            FROM KullaniciProgram
            WHERE kullanici_id=%s AND program_id=%s
        """, (kullanici_id, program_id))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Error:
        return None


def get_program_detail(program_id: int) -> dict | None:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.*,
                   GROUP_CONCAT(t.tur_adi ORDER BY t.tur_adi SEPARATOR ', ') AS turler
            FROM Program p
            LEFT JOIN ProgramTur pt ON p.program_id = pt.program_id
            LEFT JOIN Tur t         ON pt.tur_id = t.tur_id
            WHERE p.program_id = %s
            GROUP BY p.program_id
        """, (program_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Error:
        return None


def get_bolumler(program_id: int) -> list:
    """Dizinin tüm bölümlerini döner."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT bolum_id, bolum_no, bolum_adi, sure_dk
            FROM Bolum
            WHERE program_id = %s
            ORDER BY bolum_no
        """, (program_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error:
        return []


def get_kullanici_program(kullanici_id: int, program_id: int) -> dict | None:
    """Kullanıcının bu programa ait izleme + puan kaydını döner."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT kp_id, puan, tamamlandi, son_bolum_no, son_izleme_dk, toplam_sure_dk,
                   ilk_izleme_tarihi, son_izleme_tarihi
            FROM KullaniciProgram
            WHERE kullanici_id = %s AND program_id = %s
        """, (kullanici_id, program_id))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row
    except Error:
        return None


def get_izleme_gecmisi(kullanici_id: int) -> list:
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT il.log_id, p.program_adi, p.program_tipi,
                   il.bolum_no, il.izleme_tarihi, il.izlenen_dk,
                   il.tamamlandi, kp.puan
            FROM IzlemeLog il
            JOIN Program p ON il.program_id = p.program_id
            LEFT JOIN KullaniciProgram kp
                   ON kp.program_id = il.program_id AND kp.kullanici_id = il.kullanici_id
            WHERE il.kullanici_id = %s
            ORDER BY il.izleme_tarihi DESC
        """, (kullanici_id,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Error:
        return []


def izlened_dk_kaldi(izlenen_dk: int, tamamlandi: bool) -> int:
    """Tamamlandıysa kaldığı dakikayı 0 yap."""
    return 0 if tamamlandi else izlenen_dk


def kaydet_izleme(kullanici_id: int, program_id: int, bolum_no: int,
                  izlenen_dk: int, tamamlandi: bool):
    """
    KullaniciProgram ve IzlemeLog tablolarını günceller/ekler.
    Programa ait toplam_izlenme sayacını bir artırır.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT bolum_uzunluk_dk FROM Program WHERE program_id=%s",
            (program_id,)
        )
        program_row = cursor.fetchone()
        max_sure = int((program_row or {}).get("bolum_uzunluk_dk") or 0)
        if max_sure > 0 and izlenen_dk > max_sure:
            cursor.close()
            conn.close()
            return False, "İzleme süresi bölüm süresini aşamaz."

        # KullaniciProgram — varsa güncelle, yoksa ekle
        cursor.execute(
            "SELECT kp_id, toplam_sure_dk FROM KullaniciProgram "
            "WHERE kullanici_id=%s AND program_id=%s",
            (kullanici_id, program_id)
        )
        row = cursor.fetchone()

        kaldi_dk = izlened_dk_kaldi(izlenen_dk, tamamlandi)

        if row:
            yeni_sure = (row["toplam_sure_dk"] or 0) + izlenen_dk
            cursor.execute("""
                UPDATE KullaniciProgram
                SET son_bolum_no=%s, son_izleme_dk=%s, tamamlandi=%s,
                    toplam_sure_dk=%s, son_izleme_tarihi=NOW(),
                    ilk_izleme_tarihi=COALESCE(ilk_izleme_tarihi, NOW())
                WHERE kullanici_id=%s AND program_id=%s
            """, (bolum_no, kaldi_dk, 1 if tamamlandi else 0,
                  yeni_sure, kullanici_id, program_id))
        else:
            cursor.execute("""
                INSERT INTO KullaniciProgram
                    (kullanici_id, program_id, tamamlandi, son_bolum_no,
                     son_izleme_dk, toplam_sure_dk, ilk_izleme_tarihi, son_izleme_tarihi)
                VALUES (%s,%s,%s,%s,%s,%s,NOW(),NOW())
            """, (kullanici_id, program_id, 1 if tamamlandi else 0,
                  bolum_no, kaldi_dk, izlenen_dk))

        # IzlemeLog — her izleme oturumu için yeni kayıt
        cursor.execute("""
            INSERT INTO IzlemeLog (kullanici_id, program_id, bolum_no, izlenen_dk, tamamlandi)
            VALUES (%s,%s,%s,%s,%s)
        """, (kullanici_id, program_id, bolum_no, izlenen_dk, 1 if tamamlandi else 0))

        # Program toplam izlenme +1
        cursor.execute(
            "UPDATE Program SET toplam_izlenme = toplam_izlenme + 1 WHERE program_id=%s",
            (program_id,)
        )

        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        return False, str(e)


def kaydet_puan(kullanici_id: int, program_id: int, puan: int):
    """KullaniciProgram'a puan yazar; program ortalama puanını günceller."""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT kp_id FROM KullaniciProgram WHERE kullanici_id=%s AND program_id=%s",
            (kullanici_id, program_id)
        )
        if cursor.fetchone():
            cursor.execute(
                "UPDATE KullaniciProgram SET puan=%s WHERE kullanici_id=%s AND program_id=%s",
                (puan, kullanici_id, program_id)
            )
        else:
            cursor.execute(
                "INSERT INTO KullaniciProgram (kullanici_id, program_id, puan) VALUES (%s,%s,%s)",
                (kullanici_id, program_id, puan)
            )

        # Ortalama puanı güncelle
        cursor.execute("""
            UPDATE Program SET ortalama_puan = (
                SELECT ROUND(AVG(puan),1) FROM KullaniciProgram
                WHERE program_id=%s AND puan IS NOT NULL
            ) WHERE program_id=%s
        """, (program_id, program_id))

        conn.commit()
        cursor.close()
        conn.close()
        return True, None
    except Error as e:
        return False, str(e)


def get_recommendations_for_user(kullanici_id: int) -> list:
    """
    Kullanıcıya özel öneri listesi döner.
    Kriter: favori türler + yüksek puan verilen türler + en çok izlenen içerikler.
    Daha önce izlenmiş içerikler öneri listesinden çıkarılır.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # 1. Kullanıcının favori/beğenilen tür ID'leri
        cursor.execute("""
            SELECT DISTINCT pt.tur_id
            FROM KullaniciTur kt
            LEFT JOIN ProgramTur pt ON pt.tur_id = kt.tur_id
            WHERE kt.kullanici_id = %s
            UNION
            SELECT DISTINCT pt2.tur_id
            FROM KullaniciProgram kp
            JOIN ProgramTur pt2 ON kp.program_id = pt2.program_id
            WHERE kp.kullanici_id = %s AND kp.puan >= 7
        """, (kullanici_id, kullanici_id))
        tur_ids = [r["tur_id"] for r in cursor.fetchall() if r["tur_id"]]

        # 2. Daha önce izlenmiş program ID'leri
        cursor.execute("""
            SELECT program_id FROM KullaniciProgram WHERE kullanici_id = %s
        """, (kullanici_id,))
        izlenen_ids = {r["program_id"] for r in cursor.fetchall()}

        sonuclar = []

        # 3. Favori/yüksek puanlı türlerden öneriler
        if tur_ids:
            fmt = ",".join(["%s"] * len(tur_ids))
            cursor.execute(f"""
                SELECT DISTINCT
                    p.program_id, p.program_adi, p.program_tipi,
                    p.yayin_yili, p.bolum_sayisi, p.bolum_uzunluk_dk,
                    p.ortalama_puan, p.toplam_izlenme,
                    GROUP_CONCAT(t2.tur_adi ORDER BY t2.tur_adi SEPARATOR ', ') AS turler
                FROM Program p
                JOIN ProgramTur pt ON p.program_id = pt.program_id
                LEFT JOIN ProgramTur pt2 ON p.program_id = pt2.program_id
                LEFT JOIN Tur t2 ON pt2.tur_id = t2.tur_id
                WHERE pt.tur_id IN ({fmt})
                GROUP BY p.program_id
                ORDER BY p.ortalama_puan DESC
                LIMIT 12
            """, tur_ids)
            for row in cursor.fetchall():
                if row["program_id"] not in izlenen_ids:
                    row["kaynak"] = "Favori Türleriniz"
                    sonuclar.append(row)
                    izlenen_ids.add(row["program_id"])

        # 4. Genel popüler içerikler (yetersizse tamamla)
        if len(sonuclar) < 6:
            cursor.execute("""
                SELECT
                    p.program_id, p.program_adi, p.program_tipi,
                    p.yayin_yili, p.bolum_sayisi, p.bolum_uzunluk_dk,
                    p.ortalama_puan, p.toplam_izlenme,
                    GROUP_CONCAT(t.tur_adi ORDER BY t.tur_adi SEPARATOR ', ') AS turler
                FROM Program p
                LEFT JOIN ProgramTur pt ON p.program_id = pt.program_id
                LEFT JOIN Tur t ON pt.tur_id = t.tur_id
                GROUP BY p.program_id
                ORDER BY p.toplam_izlenme DESC, p.ortalama_puan DESC
                LIMIT 20
            """)
            for row in cursor.fetchall():
                if row["program_id"] not in izlenen_ids:
                    row["kaynak"] = "Popüler İçerikler"
                    sonuclar.append(row)
                    izlenen_ids.add(row["program_id"])
                if len(sonuclar) >= 12:
                    break

        cursor.close()
        conn.close()
        return sonuclar[:12]
    except Error as e:
        print("get_recommendations_for_user hata:", e)
        return []
