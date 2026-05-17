import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",
    "password": "Eyldz*611",          # root şifren varsa buraya yaz
    "database": "netflix_platform",
    "charset":  "utf8mb4",
}


def get_connection():
    """Yeni bir veritabanı bağlantısı döner."""
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection


def test_connection():
    """Bağlantıyı test eder ve sonucu ekrana yazdırır."""
    try:
        conn = get_connection()
        if conn.is_connected():
            info = conn.get_server_info()
            print(f"[OK] MySQL bağlantısı başarılı. Sunucu sürümü: {info}")
            cursor = conn.cursor()
            cursor.execute("SELECT DATABASE();")
            db_name = cursor.fetchone()[0]
            print(f"[OK] Aktif veritabanı: {db_name}")
            cursor.close()
    except Error as e:
        print(f"[HATA] Bağlantı kurulamadı: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()


if __name__ == "__main__":
    test_connection()
