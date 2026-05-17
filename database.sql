-- ============================================================
-- Netflix Benzeri Platform - MySQL Veritabanı Scripti
-- ============================================================

CREATE DATABASE IF NOT EXISTS netflix_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_turkish_ci;
USE netflix_platform;

-- ------------------------------------------------------------
-- 1. ROL
-- ------------------------------------------------------------
CREATE TABLE Rol (
    rol_id   INT          AUTO_INCREMENT PRIMARY KEY,
    rol_adi  VARCHAR(50)  NOT NULL UNIQUE   -- 'kullanici', 'yonetici'
);

INSERT INTO Rol (rol_adi) VALUES ('kullanici'), ('yonetici');

-- ------------------------------------------------------------
-- 2. KULLANICI
-- ------------------------------------------------------------
CREATE TABLE Kullanici (
    kullanici_id      INT           AUTO_INCREMENT PRIMARY KEY,
    ad                VARCHAR(100)  NOT NULL,
    soyad             VARCHAR(100)  NOT NULL,
    email             VARCHAR(150)  NOT NULL UNIQUE,
    sifre_hash        VARCHAR(255)  NOT NULL,
    dogum_tarihi      DATE          NOT NULL,
    cinsiyet          ENUM('Erkek','Kadın','Diğer') NOT NULL,
    ulke              VARCHAR(100)  NOT NULL,
    rol_id            INT           NOT NULL DEFAULT 1,
    aktif             TINYINT(1)    NOT NULL DEFAULT 1,
    kayit_tarihi      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_kullanici_rol FOREIGN KEY (rol_id) REFERENCES Rol(rol_id)
);

-- ------------------------------------------------------------
-- 3. TÜR
-- ------------------------------------------------------------
CREATE TABLE Tur (
    tur_id   INT          AUTO_INCREMENT PRIMARY KEY,
    tur_adi  VARCHAR(100) NOT NULL UNIQUE
);

-- ------------------------------------------------------------
-- 4. KULLANICI TÜR (Favori Türler - kayıtta seçilen 3 tür)
-- ------------------------------------------------------------
CREATE TABLE KullaniciTur (
    kullanici_tur_id  INT  AUTO_INCREMENT PRIMARY KEY,
    kullanici_id      INT  NOT NULL,
    tur_id            INT  NOT NULL,
    CONSTRAINT fk_kt_kullanici FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    CONSTRAINT fk_kt_tur       FOREIGN KEY (tur_id)       REFERENCES Tur(tur_id)             ON DELETE CASCADE,
    CONSTRAINT uq_kt           UNIQUE (kullanici_id, tur_id)
);

-- ------------------------------------------------------------
-- 5. PROGRAM (Film veya Dizi)
-- ------------------------------------------------------------
CREATE TABLE Program (
    program_id        INT           AUTO_INCREMENT PRIMARY KEY,
    program_adi       VARCHAR(255)  NOT NULL,
    aciklama          TEXT,
    program_tipi      ENUM('Film','Dizi') NOT NULL,
    yayin_yili        YEAR          NOT NULL,
    bolum_sayisi      INT           NOT NULL DEFAULT 1,   -- Film için 1
    bolum_uzunluk_dk  INT           NOT NULL DEFAULT 0,   -- Dakika cinsinden
    toplam_izlenme    INT           NOT NULL DEFAULT 0,
    ortalama_puan     DECIMAL(3,1)  NOT NULL DEFAULT 0.0,
    eklenme_tarihi    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ------------------------------------------------------------
-- 6. PROGRAM TÜR (Çoktan Çoğa)
-- ------------------------------------------------------------
CREATE TABLE ProgramTur (
    program_tur_id  INT  AUTO_INCREMENT PRIMARY KEY,
    program_id      INT  NOT NULL,
    tur_id          INT  NOT NULL,
    CONSTRAINT fk_pt_program FOREIGN KEY (program_id) REFERENCES Program(program_id) ON DELETE CASCADE,
    CONSTRAINT fk_pt_tur     FOREIGN KEY (tur_id)     REFERENCES Tur(tur_id)         ON DELETE RESTRICT,
    CONSTRAINT uq_pt         UNIQUE (program_id, tur_id)
);

-- ------------------------------------------------------------
-- 7. BÖLÜM (Diziler için)
-- ------------------------------------------------------------
CREATE TABLE Bolum (
    bolum_id      INT           AUTO_INCREMENT PRIMARY KEY,
    program_id    INT           NOT NULL,
    bolum_no      INT           NOT NULL,
    bolum_adi     VARCHAR(255),
    sure_dk       INT           NOT NULL DEFAULT 0,
    CONSTRAINT fk_bolum_program FOREIGN KEY (program_id) REFERENCES Program(program_id) ON DELETE CASCADE,
    CONSTRAINT uq_bolum         UNIQUE (program_id, bolum_no)
);

-- ------------------------------------------------------------
-- 8. FAVORİ
-- ------------------------------------------------------------
CREATE TABLE Favori (
    favori_id     INT       AUTO_INCREMENT PRIMARY KEY,
    kullanici_id  INT       NOT NULL,
    program_id    INT       NOT NULL,
    ekleme_tarihi DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_fav_kullanici FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    CONSTRAINT fk_fav_program   FOREIGN KEY (program_id)   REFERENCES Program(program_id)     ON DELETE CASCADE,
    CONSTRAINT uq_fav           UNIQUE (kullanici_id, program_id)
);

-- ------------------------------------------------------------
-- 9. KULLANICI PROGRAM (İzleme + Puanlama)
-- ------------------------------------------------------------
CREATE TABLE KullaniciProgram (
    kp_id              INT           AUTO_INCREMENT PRIMARY KEY,
    kullanici_id       INT           NOT NULL,
    program_id         INT           NOT NULL,
    puan               INT           CHECK (puan BETWEEN 1 AND 10),
    tamamlandi         TINYINT(1)    NOT NULL DEFAULT 0,
    son_bolum_no       INT           NOT NULL DEFAULT 1,
    son_izleme_dk      INT           NOT NULL DEFAULT 0,   -- Kaldığı dakika
    toplam_sure_dk     INT           NOT NULL DEFAULT 0,
    ilk_izleme_tarihi  DATETIME,
    son_izleme_tarihi  DATETIME,
    CONSTRAINT fk_kp_kullanici FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    CONSTRAINT fk_kp_program   FOREIGN KEY (program_id)   REFERENCES Program(program_id)     ON DELETE CASCADE,
    CONSTRAINT uq_kp           UNIQUE (kullanici_id, program_id)
);

-- ------------------------------------------------------------
-- 10. İZLEME LOG (Her izleme oturumu kaydı)
-- ------------------------------------------------------------
CREATE TABLE IzlemeLog (
    log_id        INT       AUTO_INCREMENT PRIMARY KEY,
    kullanici_id  INT       NOT NULL,
    program_id    INT       NOT NULL,
    bolum_no      INT       NOT NULL DEFAULT 1,
    izleme_tarihi DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    izlenen_dk    INT       NOT NULL DEFAULT 0,
    tamamlandi    TINYINT(1) NOT NULL DEFAULT 0,
    CONSTRAINT fk_il_kullanici FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE,
    CONSTRAINT fk_il_program   FOREIGN KEY (program_id)   REFERENCES Program(program_id)     ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- 11. OTURUM LOG (Giriş/Çıkış kayıtları)
-- ------------------------------------------------------------
CREATE TABLE OturumLog (
    oturum_id     INT       AUTO_INCREMENT PRIMARY KEY,
    kullanici_id  INT       NOT NULL,
    giris_tarihi  DATETIME  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cikis_tarihi  DATETIME,
    ip_adresi     VARCHAR(45),
    CONSTRAINT fk_ol_kullanici FOREIGN KEY (kullanici_id) REFERENCES Kullanici(kullanici_id) ON DELETE CASCADE
);


