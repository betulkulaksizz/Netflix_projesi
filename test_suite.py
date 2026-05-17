#!/usr/bin/env python3
"""
TEST SUITE - PROLAB22 Yazılım Doğrulama
Tüm bileşenleri test etmek için kapsamlı test uygulaması.
"""

import sys
import time
from datetime import datetime, date

# Modülleri import et
from auth import validate_email, validate_name, validate_country, login_user
from database import get_connection, test_connection
from queries import (
    get_favoriler, get_profil, update_profil, kaydet_izleme,
    kaydet_puan, toggle_favori, get_all_programs
)

# Test sonuçlarını tutmak için
test_results = {
    "toplam": 0,
    "basarili": 0,
    "basarisiz": 0,
    "detaylar": []
}

# Renkli çıktı için
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'


def print_test(name: str, result: bool, message: str = ""):
    """Test sonucunu yazdır."""
    test_results["toplam"] += 1
    status = f"{Colors.GREEN}✓ GEÇTI{Colors.RESET}" if result else f"{Colors.RED}✗ BAŞARISIZ{Colors.RESET}"
    
    if result:
        test_results["basarili"] += 1
    else:
        test_results["basarisiz"] += 1
    
    test_results["detaylar"].append({
        "test": name,
        "sonuc": "GEÇTI" if result else "BAŞARISIZ",
        "mesaj": message
    })
    
    msg = f"{status} | {name}"
    if message:
        msg += f" ({message})"
    print(msg)


def separator(title: str = ""):
    """Bölüm ayırıcı yazdır."""
    print(f"\n{Colors.BLUE}{'='*70}")
    if title:
        print(f"  {title}")
        print('='*70 + f"{Colors.RESET}\n")
    else:
        print(f"{Colors.RESET}\n")


def test_database():
    """Veritabanı bağlantı testleri."""
    separator("1. VERİTABANI BAĞLANTISI TESTLERİ")
    
    try:
        conn = get_connection()
        is_connected = conn.is_connected()
        print_test("Veritabanı Bağlantısı", is_connected, "MySQL bağlantısı kuruldu" if is_connected else "Bağlantı başarısız")
        
        if is_connected:
            cursor = conn.cursor(dictionary=True)
            
            # Tablo var mı kontrol et
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='netflix_platform'")
            tables = [row["TABLE_NAME"] for row in cursor.fetchall()]
            expected_tables = ["Kullanici", "Rol", "Program", "Tur", "ProgramTur", "Bolum", "KullaniciProgram", "KullaniciTur", "Favori", "IzlemeLog", "OturumLog"]
            
            missing = [t for t in expected_tables if t not in tables]
            all_exist = len(missing) == 0
            print_test(
                "Tüm Gerekli Tablolar Mevcut",
                all_exist,
                f"Toplam tablo: {len(tables)}, Eksik: {missing if missing else 'Yok'}"
            )
            
            cursor.close()
        
        conn.close()
    except Exception as e:
        print_test("Veritabanı Bağlantısı", False, str(e))


def test_validations():
    """Email, ad/soyad ve ülke doğrulama testleri."""
    separator("2. DOĞRULAMA FONKSİYONLARI TESTLERİ")
    
    # Email Doğrulama
    print(f"\n{Colors.YELLOW}Email Doğrulama:{Colors.RESET}")
    email_tests = [
        ("test@example.com", True),
        ("user.name@domain.co.uk", True),
        ("invalid.email@", False),
        ("@example.com", False),
        ("notanemail", False),
    ]
    for email, expected in email_tests:
        result = validate_email(email)
        print_test(f"  Email: '{email}'", result == expected, f"Beklenen: {expected}, Sonuç: {result}")
    
    # Ad/Soyad Doğrulama
    print(f"\n{Colors.YELLOW}Ad/Soyad Doğrulama:{Colors.RESET}")
    name_tests = [
        ("Ali", True),
        ("Jean-Paul", True),
        ("O'Brien", True),
        ("Müller", True),
        ("Ali123", False),
        ("Ali@", False),
        ("M", False),
        ("", False),
    ]
    for name, expected in name_tests:
        result = validate_name(name)
        print_test(f"  Ad: '{name}'", result == expected, f"Beklenen: {expected}, Sonuç: {result}")
    
    # Ülke Doğrulama
    print(f"\n{Colors.YELLOW}Ülke Doğrulama:{Colors.RESET}")
    country_tests = [
        ("Türkiye", True),
        ("United States", True),
        ("Amerika Birleşik Devletleri", True),
        ("123", False),
        ("Ali", False),
        ("xyz", False),
        ("", False),
    ]
    for country, expected in country_tests:
        result = validate_country(country)
        print_test(f"  Ülke: '{country}'", result == expected, f"Beklenen: {expected}, Sonuç: {result}")


def test_database_operations():
    """Veritabanı işlemleri testleri."""
    separator("3. VERİTABANI İŞLEMLERİ TESTLERİ")
    
    try:
        # Test kullanıcı
        test_user_id = 1
        test_program_id = 1
        
        # get_profil
        profil = get_profil(test_user_id)
        print_test(
            "get_profil()",
            profil is not None,
            f"Kullanıcı profili alındı: {profil['ad'] if profil else 'Bulunamadı'}"
        )
        
        # get_all_programs
        programlar = get_all_programs(test_user_id)
        print_test(
            "get_all_programs()",
            isinstance(programlar, list) and len(programlar) > 0,
            f"Bulunan program sayısı: {len(programlar)}"
        )
        
        # get_favoriler
        favoriler = get_favoriler(test_user_id)
        print_test(
            "get_favoriler()",
            isinstance(favoriler, list),
            f"Bulunan favori sayısı: {len(favoriler)}"
        )
        
    except Exception as e:
        print_test("Veritabanı İşlemleri", False, str(e))


def test_input_validation():
    """İzleme süresi validasyonu testleri."""
    separator("4. İZLEME SÜRESİ VALIDASYONU TESTLERİ")
    
    try:
        # İzleme kaydı testi (geçerli süre)
        ok, err = kaydet_izleme(1, 1, 1, 60, tamamlandi=False)
        print_test(
            "Geçerli İzleme Süresi (60 dk)",
            ok,
            f"Sonuç: {err if not ok else 'Başarılı'}"
        )
        
        # İzleme kaydı testi (geçersiz süre - aşırı büyük)
        ok, err = kaydet_izleme(1, 1, 1, 500, tamamlandi=False)
        print_test(
            "Geçersiz İzleme Süresi (500 dk - aşırı)",
            not ok,
            f"Sonuç: {err if not ok else 'Başarısız kontrol'}"
        )
        
    except Exception as e:
        print_test("İzleme Süresi Validasyonu", False, str(e))


def test_user_authentication():
    """Kullanıcı giriş testleri."""
    separator("5. KULLANICI GİRİŞ TESTLERİ")
    
    try:
        # Test hesabı (veritabanında olması gerekli)
        # NOT: Gerçek test için geçerli email/şifre gerekli
        
        # Yanlış email
        user, err = login_user("nonexistent@example.com", "password123")
        print_test(
            "Yanlış Email Giriş",
            user is None and err is not None,
            f"Hata mesajı: {err}"
        )
        
        # Geçerli email, yanlış şifre (test hesabı varsa)
        # user, err = login_user("valid@example.com", "wrongpassword")
        # print_test("Yanlış Şifre Giriş", user is None, f"Hata mesajı: {err}")
        
    except Exception as e:
        print_test("Kullanıcı Giriş Testleri", False, str(e))


def test_favorite_operations():
    """Favori işlemleri testleri."""
    separator("6. FAVORİ İŞLEMLERİ TESTLERİ")
    
    try:
        test_user_id = 1
        test_program_id = 2
        
        # Favori ekle/çıkar (toggle)
        ok = toggle_favori(test_user_id, test_program_id)
        print_test(
            "Favori Toggle (Ekle/Çıkar)",
            isinstance(ok, bool),
            f"Sonuç: {ok}"
        )
        
        # Favorileri getir
        favoriler = get_favoriler(test_user_id)
        print_test(
            "Favorileri Getirme",
            isinstance(favoriler, list),
            f"Favori sayısı: {len(favoriler)}"
        )
        
    except Exception as e:
        print_test("Favori İşlemleri", False, str(e))


def test_rating_operations():
    """Puan işlemleri testleri."""
    separator("7. PUAN İŞLEMLERİ TESTLERİ")
    
    try:
        # Puan tablosu varsa test et
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA='netflix_platform' AND TABLE_NAME='Puan'")
        puan_table_exists = cursor.fetchone() is not None
        cursor.close()
        conn.close()
        
        if not puan_table_exists:
            print_test("Puan İşlemleri", True, "Puan tablosu veritabanında yok (isteğe bağlı)")
            return
        
        test_user_id = 1
        test_program_id = 1
        
        # Puan kaydet
        ok, err = kaydet_puan(test_user_id, test_program_id, 8)
        print_test(
            "Puan Kaydetme",
            ok,
            f"Sonuç: {err if not ok else 'Başarılı (8/10)'}"
        )
        
        # Puan güncelle
        ok, err = kaydet_puan(test_user_id, test_program_id, 9)
        print_test(
            "Puan Güncelleme",
            ok,
            f"Sonuç: {err if not ok else 'Başarılı (9/10)'}"
        )
        
    except Exception as e:
        print_test("Puan İşlemleri", False, str(e))


def test_profile_update():
    """Profil güncelleme testleri."""
    separator("8. PROFIL GÜNCELLEME TESTLERİ")
    
    try:
        test_user_id = 1
        
        # Geçerli profil güncelleme
        ok, err = update_profil(
            test_user_id,
            "Test",
            "Kullanıcı",
            "test@example.com",
            date(1990, 1, 1),
            "Türkiye",
            "Erkek"
        )
        print_test(
            "Profil Güncelleme (Geçerli)",
            ok,
            f"Sonuç: {err if not ok else 'Başarılı'}"
        )
        
        # Alınan email ile güncelleme (başarısız olmalı)
        ok, err = update_profil(
            2,
            "Test",
            "Kullanıcı",
            "test@example.com",  # Zaten kullanıcı 1'in emaili
            date(1990, 1, 1),
            "Türkiye",
            "Kadın"
        )
        print_test(
            "Profil Güncelleme (Alınan Email)",
            not ok,
            f"Sonuç: {err if not ok else 'Hata: Email kontrol başarısız'}"
        )
        
    except Exception as e:
        print_test("Profil Güncelleme", False, str(e))


def print_summary():
    """Test özeti yazdır."""
    separator("TEST ÖZETİ")
    
    print(f"{Colors.BLUE}Toplam Testler: {test_results['toplam']}{Colors.RESET}")
    print(f"{Colors.GREEN}Geçen Testler: {test_results['basarili']}{Colors.RESET}")
    print(f"{Colors.RED}Başarısız Testler: {test_results['basarisiz']}{Colors.RESET}")
    
    if test_results['toplam'] > 0:
        yuzde = (test_results['basarili'] / test_results['toplam']) * 100
        print(f"\n{Colors.BLUE}Başarı Oranı: {yuzde:.1f}%{Colors.RESET}\n")
    
    # Başarısız testleri listele
    if test_results['basarisiz'] > 0:
        print(f"{Colors.RED}Başarısız Testler:{Colors.RESET}")
        for detail in test_results['detaylar']:
            if detail['sonuc'] == "BAŞARISIZ":
                print(f"  • {detail['test']}: {detail['mesaj']}")


def run_all_tests():
    """Tüm testleri çalıştır."""
    print(f"\n{Colors.BLUE}{'='*70}")
    print("  PROLAB22 - YAZILIM TEST SÜRECİ")
    print(f"  Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}{Colors.RESET}\n")
    
    start_time = time.time()
    
    # Testleri çalıştır
    test_database()
    test_validations()
    test_database_operations()
    test_input_validation()
    test_user_authentication()
    test_favorite_operations()
    test_rating_operations()
    test_profile_update()
    
    # Özet
    print_summary()
    
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"{Colors.BLUE}Toplam Süre: {elapsed:.2f} saniye{Colors.RESET}\n")
    
    # Test rapor dosyasını kaydet
    save_test_report()


def save_test_report():
    """Test raporunu dosyaya kaydet."""
    with open("test_report.txt", "w", encoding="utf-8") as f:
        f.write("PROLAB22 - YAZILIM TEST RAPORU\n")
        f.write(f"Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        f.write(f"Toplam Testler: {test_results['toplam']}\n")
        f.write(f"Geçen Testler: {test_results['basarili']}\n")
        f.write(f"Başarısız Testler: {test_results['basarisiz']}\n")
        
        if test_results['toplam'] > 0:
            yuzde = (test_results['basarili'] / test_results['toplam']) * 100
            f.write(f"Başarı Oranı: {yuzde:.1f}%\n\n")
        
        f.write("DETAYLI TEST SONUÇLARI:\n")
        f.write("-"*70 + "\n")
        for detail in test_results['detaylar']:
            f.write(f"\nTest: {detail['test']}\n")
            f.write(f"Sonuç: {detail['sonuc']}\n")
            if detail['mesaj']:
                f.write(f"Açıklama: {detail['mesaj']}\n")
    
    print(f"{Colors.GREEN}Test raporu 'test_report.txt' dosyasına kaydedildi.{Colors.RESET}")


if __name__ == "__main__":
    run_all_tests()
