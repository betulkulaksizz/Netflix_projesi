USE netflix_platform;


INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Recep İvedik 6', 'Aksiyon ve Macera', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Recep İvedik 6'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Assassın''s Creed', 'Aksiyon ve Macera, Bilim Kurgu ve Fantastik Yapımlar', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Assassın''s Creed'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Assassın''s Creed'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Alaca Karanlık', 'Aksiyon ve Macera, Romantik', 'Film', 2024, 1, 100, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Alaca Karanlık'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Alaca Karanlık'
AND t.tur_adi = 'Romantik';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Yüzüklerin Efendisi İki Kule', 'Aksiyon ve Macera, Bilim Kurgu ve Fantastik Yapımlar', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Yüzüklerin Efendisi İki Kule'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Yüzüklerin Efendisi İki Kule'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Maske', 'Aksiyon ve Macera, Bilim Kurgu ve Fantastik Yapımlar', 'Film', 2024, 1, 70, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Maske'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Maske'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Kara Şövalye', 'Aksiyon ve Macera, Bilim Kurgu ve Fantastik Yapımlar', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kara Şövalye'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kara Şövalye'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Sherlock Holmes', 'Aksiyon ve Macera', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Sherlock Holmes'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Yüzüklerin Efendisi kralın Dönüşü', 'Aksiyon ve Macera, Bilim Kurgu ve Fantastik Yapımlar', 'Film', 2024, 1, 50, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Yüzüklerin Efendisi kralın Dönüşü'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Yüzüklerin Efendisi kralın Dönüşü'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Transformers Kayıp Çağ', 'Aksiyon ve Macera', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Transformers Kayıp Çağ'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Başlangıç', 'Aksiyon ve Macera', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Başlangıç'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Interstellar', 'Aksiyon ve Macera, Drama', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Interstellar'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Interstellar'
AND t.tur_adi = 'Drama';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Harry Potter lüm Yadigarları', 'Aksiyon ve Macera, Bilim Kurgu ve Fantastik Yapımlar, Çocuk ve Aile', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Harry Potter lüm Yadigarları'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Harry Potter lüm Yadigarları'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Harry Potter lüm Yadigarları'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Jurassic World', 'Aksiyon ve Macera', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Jurassic World'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Fantastik Canavarlar', 'Aksiyon ve Macera, Çocuk ve Aile', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Fantastik Canavarlar'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Fantastik Canavarlar'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Ninja Kaplumbağalar', 'Aksiyon ve Macera, Bilim Kurgu ve Fantastik Yapımlar', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Ninja Kaplumbağalar'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Ninja Kaplumbağalar'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Kuşlarla Dans', 'Belgesel', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kuşlarla Dans'
AND t.tur_adi = 'Belgesel';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Mission Blue', 'Belgesel', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Mission Blue'
AND t.tur_adi = 'Belgesel';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Mercan Peşinde', 'Belgesel', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Mercan Peşinde'
AND t.tur_adi = 'Belgesel';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Dream Big', 'Belgesel', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Dream Big'
AND t.tur_adi = 'Belgesel';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Ay''daki Son Adam', 'Belgesel', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Ay''daki Son Adam'
AND t.tur_adi = 'Belgesel';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Plastik Okyanus', 'Belgesel', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Plastik Okyanus'
AND t.tur_adi = 'Belgesel';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Rakamlarla Tahmin', 'Belgesel', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Rakamlarla Tahmin'
AND t.tur_adi = 'Belgesel';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Ben Efsaneyim', 'Bilim Kurgu ve Fantastik Yapımlar', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Ben Efsaneyim'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Arif V 216', 'Bilim Kurgu ve Fantastik Yapımlar, Komedi', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Arif V 216'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Arif V 216'
AND t.tur_adi = 'Komedi';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('pk', 'Bilim Kurgu ve Fantastik Yapımlar, Romantik', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'pk'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'pk'
AND t.tur_adi = 'Romantik';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Örümcek Adam', 'Aksiyon ve Macera, Bilim Kurgu ve Fantastik Yapımlar', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Örümcek Adam'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Örümcek Adam'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Jurassıc Park', 'Bilim Kurgu ve Fantastik Yapımlar, Aksiyon', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Jurassıc Park'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Jurassıc Park'
AND t.tur_adi = 'Aksiyon';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Frankestein', 'Bilim Kurgu ve Fantastik Yapımlar, Aksiyon, Korku', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu ve Fantastik Yapımlar');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Frankestein'
AND t.tur_adi = 'Bilim Kurgu ve Fantastik Yapımlar';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Frankestein'
AND t.tur_adi = 'Aksiyon';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Korku');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Frankestein'
AND t.tur_adi = 'Korku';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Gezegenimiz', 'Belgesel, Bilim ve Doğa', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Gezegenimiz'
AND t.tur_adi = 'Belgesel';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim ve Doğa');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Gezegenimiz'
AND t.tur_adi = 'Bilim ve Doğa';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('72 sevimli hayvan', 'Belgesel, Bilim ve Doğa', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = '72 sevimli hayvan'
AND t.tur_adi = 'Belgesel';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim ve Doğa');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = '72 sevimli hayvan'
AND t.tur_adi = 'Bilim ve Doğa';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Kuşçular', 'Belgesel, Bilim ve Doğa', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kuşçular'
AND t.tur_adi = 'Belgesel';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim ve Doğa');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kuşçular'
AND t.tur_adi = 'Bilim ve Doğa';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Marsta Keşif', 'Belgesel, Bilim ve Doğa', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Marsta Keşif'
AND t.tur_adi = 'Belgesel';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim ve Doğa');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Marsta Keşif'
AND t.tur_adi = 'Bilim ve Doğa';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Gezegenimiz', 'Belgesel, Bilim ve Doğa', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Gezegenimiz'
AND t.tur_adi = 'Belgesel';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim ve Doğa');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Gezegenimiz'
AND t.tur_adi = 'Bilim ve Doğa';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Pandemic', 'Belgesel, Bilim ve Doğa', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Belgesel');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Pandemic'
AND t.tur_adi = 'Belgesel';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim ve Doğa');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Pandemic'
AND t.tur_adi = 'Bilim ve Doğa';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Pokemon', 'Çocuk ve Aile', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Pokemon'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Şirinler', 'Çocuk ve Aile, Komedi', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Şirinler'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Şirinler'
AND t.tur_adi = 'Komedi';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Charlie''nin Çikolata Fabrikası', 'Çocuk ve Aile, Komedi', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Charlie''nin Çikolata Fabrikası'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Charlie''nin Çikolata Fabrikası'
AND t.tur_adi = 'Komedi';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Alvin ve Sincaplar', 'Çocuk ve Aile', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Alvin ve Sincaplar'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Scooby-Doo', 'Çocuk ve Aile', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Scooby-Doo'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Kung Fu Panda', 'Çocuk ve Aile, Aksiyon ve Macera', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kung Fu Panda'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kung Fu Panda'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Mr. Bean Tatilde', 'Çocuk ve Aile', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Mr. Bean Tatilde'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Shrek', 'Çocuk ve Aile, Komedi', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Shrek'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Shrek'
AND t.tur_adi = 'Komedi';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Mega Zeka', 'Çocuk ve Aile, Komedi', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Mega Zeka'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Mega Zeka'
AND t.tur_adi = 'Komedi';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Bizi Hatırla', 'Drama', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Bizi Hatırla'
AND t.tur_adi = 'Drama';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Delibal', 'Drama, Romantik', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Delibal'
AND t.tur_adi = 'Drama';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Delibal'
AND t.tur_adi = 'Romantik';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Kardeşim Benim', 'Drama, Komedi', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kardeşim Benim'
AND t.tur_adi = 'Drama';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kardeşim Benim'
AND t.tur_adi = 'Komedi';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Dangal', 'Drama', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Dangal'
AND t.tur_adi = 'Drama';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Yerçekimi', 'Bilim Kurgu, Drama', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Bilim Kurgu');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Yerçekimi'
AND t.tur_adi = 'Bilim Kurgu';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Yerçekimi'
AND t.tur_adi = 'Drama';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Jaws', 'Gerilim', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Gerilim');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Jaws'
AND t.tur_adi = 'Gerilim';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Da Vinci Şifresi', 'Gerilim', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Gerilim');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Da Vinci Şifresi'
AND t.tur_adi = 'Gerilim';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Marwel'' Iron Fist', 'Aksiyon ve Macera', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Marwel'' Iron Fist'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Ejderhalar', 'Çocuk ve Aile, Aksiyon ve Macera', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Ejderhalar'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Ejderhalar'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Diriliş Ertuğrul', 'Aksiyon ve Macera', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Diriliş Ertuğrul'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Trol Avcıları: Arcadia Hikayeleri', 'Çocuk ve Aile, Aksiyon ve Macera', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Trol Avcıları: Arcadia Hikayeleri'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Trol Avcıları: Arcadia Hikayeleri'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('How I met your mother', 'Romantik', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'How I met your mother'
AND t.tur_adi = 'Romantik';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Leyla ile Mecnun', 'Romantik', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Leyla ile Mecnun'
AND t.tur_adi = 'Romantik';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Beni Böyle Sev', 'Drama, Romantik', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Beni Böyle Sev'
AND t.tur_adi = 'Drama';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Beni Böyle Sev'
AND t.tur_adi = 'Romantik';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Patron Bebek Yine İş başında', 'Çocuk ve Aile, Komedi', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Patron Bebek Yine İş başında'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Patron Bebek Yine İş başında'
AND t.tur_adi = 'Komedi';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Atiye', 'Aksiyon ve Macera, Romantik', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Atiye'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Romantik');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Atiye'
AND t.tur_adi = 'Romantik';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Maşa ve Koca Ayı', 'Çocuk ve Aile', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Maşa ve Koca Ayı'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Sünger Bob', 'Çocuk ve Aile, Komedi', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Sünger Bob'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Sünger Bob'
AND t.tur_adi = 'Komedi';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Stranger Tings', 'Aksiyon ve Macera, Korku', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Stranger Tings'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Korku');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Stranger Tings'
AND t.tur_adi = 'Korku';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('The Originals', 'Drama, Korku', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Drama');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'The Originals'
AND t.tur_adi = 'Drama';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Korku');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'The Originals'
AND t.tur_adi = 'Korku';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Angry Birds', 'Çocuk ve Aile, Komedi', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Angry Birds'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Komedi');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Angry Birds'
AND t.tur_adi = 'Komedi';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Criminal', 'Gerilim', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Gerilim');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Criminal'
AND t.tur_adi = 'Gerilim';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Beyblade', 'Anime, Çocuk ve Aile', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Anime');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Beyblade'
AND t.tur_adi = 'Anime';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Çocuk ve Aile');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Beyblade'
AND t.tur_adi = 'Çocuk ve Aile';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Sonic X', 'Anime, Aksiyon ve Macera', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Anime');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Sonic X'
AND t.tur_adi = 'Anime';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Sonic X'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Kung Fu Panda Muhteşem Sırlar', 'Aksiyon ve Macera', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Kung Fu Panda Muhteşem Sırlar'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('The Blacklist', 'Aksiyon ve Macera, Gerilim', 'Dizi', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Aksiyon ve Macera');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'The Blacklist'
AND t.tur_adi = 'Aksiyon ve Macera';

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Gerilim');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'The Blacklist'
AND t.tur_adi = 'Gerilim';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Dünyanın En Sıra Dışı Evleri', 'Reality Program', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Reality Program');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Dünyanın En Sıra Dışı Evleri'
AND t.tur_adi = 'Reality Program';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Car Masters', 'Reality Program', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Reality Program');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Car Masters'
AND t.tur_adi = 'Reality Program';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Büyük Tasarımlar', 'Reality Program', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Reality Program');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Büyük Tasarımlar'
AND t.tur_adi = 'Reality Program';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Basketball or Nothing', 'Reality Program', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Reality Program');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Basketball or Nothing'
AND t.tur_adi = 'Reality Program';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('The Big Family Cooking', 'Reality Program', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Reality Program');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'The Big Family Cooking'
AND t.tur_adi = 'Reality Program';

INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('Sıradışı Kulübeler', 'Reality Program', 'Film', 2024, 1, 120, 0, 0.0);

INSERT IGNORE INTO Tur (tur_adi)
VALUES ('Reality Program');

INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p, Tur t
WHERE p.program_adi = 'Sıradışı Kulübeler'
AND t.tur_adi = 'Reality Program';
