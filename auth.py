import re
import bcrypt
from datetime import date
from functools import lru_cache
from database import get_connection
from mysql.connector import Error
from babel import Locale


def validate_email(email: str) -> bool:
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None


def validate_name(name: str) -> bool:
    """Ad/soyad alanı yalnızca harfler, boşluklar ve kesme işareti içermelidir."""
    value = name.strip()
    if len(value) < 2:
        return False
    # Sadece harfler, boşluklar, kısa çizgi ve kesme işareti izin ver
    return all(ch.isalpha() or ch in " -'" for ch in value)


def validate_country(ulke: str) -> bool:
    """Ülkenin gerçek bir ülke adı olup olmadığını doğrular."""
    value = ulke.strip()
    if not value:
        return False
    if not _has_valid_country_chars(value):
        return False
    return _normalized_country_name(value) in _country_name_set()


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().casefold())


def _has_valid_country_chars(value: str) -> bool:
    return all(ch.isalpha() or ch in " -'" for ch in value)


@lru_cache(maxsize=1)
def _country_name_set() -> set[str]:
    names = set()
    for locale_code in ("tr", "en"):
        locale = Locale.parse(locale_code)
        for territory_code, territory_name in locale.territories.items():
            if len(territory_code) != 2:
                continue
            names.add(_normalize_text(territory_name))
    return names


def _normalized_country_name(value: str) -> str:
    return _normalize_text(value)


def login_user(email: str, password: str):
    """
    Kullanıcıyı doğrular.
    Başarılıysa kullanıcı dict'i döner: {kullanici_id, ad, soyad, email, rol_id}
    Hatalıysa None döner.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT kullanici_id, ad, soyad, email, sifre_hash, rol_id, aktif "
            "FROM Kullanici WHERE email = %s",
            (email,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user is None:
            return None, "Bu e-mail ile kayıtlı kullanıcı bulunamadı."
        if not user["aktif"]:
            return None, "Hesabınız pasif durumdadır. Yönetici ile iletişime geçin."
        if not bcrypt.checkpw(password.encode(), user["sifre_hash"].encode()):
            return None, "Şifre hatalı."

        return user, None

    except Error as e:
        return None, f"Veritabanı hatası: {e}"


def get_all_genres():
    """Tüm türleri döner: [{'tur_id': ..., 'tur_adi': ...}, ...]"""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT tur_id, tur_adi FROM Tur ORDER BY tur_adi")
        genres = cursor.fetchall()
        cursor.close()
        conn.close()
        return genres
    except Error:
        return []


def register_user(ad, soyad, email, sifre, dogum_tarihi, cinsiyet, ulke, tur_ids):
    """
    Yeni kullanıcı kaydeder.
    Başarılıysa (True, None) döner.
    Hatalıysa (False, hata_mesajı) döner.
    """
    # E-mail format
    if not validate_email(email):
        return False, "Geçerli bir e-mail adresi giriniz."

    # Ülke adı
    if not validate_country(ulke):
        return False, "Geçerli bir ülke adı giriniz. Sayı kullanmayınız."

    # Şifre uzunluğu
    if len(sifre) < 6:
        return False, "Şifre en az 6 karakter olmalıdır."

    # Doğum tarihi bugünden büyük olamaz
    if dogum_tarihi > date.today():
        return False, "Doğum tarihi bugünden ileri bir tarih olamaz."

    # 3 tür seçilmeli
    if len(tur_ids) != 3:
        return False, "Lütfen tam olarak 3 favori tür seçiniz."

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # E-mail tekrar kontrolü
        cursor.execute("SELECT kullanici_id FROM Kullanici WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Bu e-mail adresi zaten kayıtlıdır."

        # Şifreyi hashle
        sifre_hash = bcrypt.hashpw(sifre.encode(), bcrypt.gensalt()).decode()

        # Kullanıcıyı ekle
        cursor.execute(
            """INSERT INTO Kullanici (ad, soyad, email, sifre_hash, dogum_tarihi, cinsiyet, ulke, rol_id, aktif)
               VALUES (%s, %s, %s, %s, %s, %s, %s, 1, 1)""",
            (ad, soyad, email, sifre_hash, dogum_tarihi, cinsiyet, ulke)
        )
        kullanici_id = cursor.lastrowid

        # Favori türleri ekle
        for tur_id in tur_ids:
            cursor.execute(
                "INSERT INTO KullaniciTur (kullanici_id, tur_id) VALUES (%s, %s)",
                (kullanici_id, tur_id)
            )

        conn.commit()
        cursor.close()
        conn.close()
        return True, None

    except Error as e:
        return False, f"Veritabanı hatası: {e}"


def get_recommendations_by_genres(tur_ids: list) -> list:
    """
    Verilen 3 tür ID'sine göre her türden en yüksek puanlı 2 içerik döner.
    Toplam 6 öneri (her tür için ayrı ayrı 2 içerik, tekrar olabilir).
    """
    results = []
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        for tur_id in tur_ids:
            cursor.execute("""
                SELECT p.program_id, p.program_adi, p.program_tipi,
                       p.ortalama_puan, p.toplam_izlenme, t.tur_adi
                FROM Program p
                JOIN ProgramTur pt ON p.program_id = pt.program_id
                JOIN Tur t         ON t.tur_id = pt.tur_id
                WHERE pt.tur_id = %s AND p.ortalama_puan > 0
                ORDER BY p.ortalama_puan DESC
                LIMIT 2
            """, (tur_id,))
            rows = cursor.fetchall()
            results.extend(rows)
        cursor.close()
        conn.close()
    except Error:
        pass
    return results
