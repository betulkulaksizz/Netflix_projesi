-- ============================================================
-- Netflix Benzeri Platform - Fake Data
-- ============================================================

USE netflix_platform;

-- ------------------------------------------------------------
-- TÜR
-- ------------------------------------------------------------
INSERT INTO Tur (tur_adi) VALUES
('Aksiyon'),
('Komedi'),
('Drama'),
('Korku'),
('Bilim Kurgu'),
('Romantik'),
('Belgesel'),
('Animasyon'),
('Gerilim'),
('Suç');

-- ------------------------------------------------------------
-- KULLANICI (rol_id=1 normal, rol_id=2 yönetici)
-- şifre_hash değerleri "sifre123" in bcrypt hash'i (örnek)
-- ------------------------------------------------------------
INSERT INTO Kullanici (ad, soyad, email, sifre_hash, dogum_tarihi, cinsiyet, ulke, rol_id, aktif) VALUES
('Admin',    'User',      'admin@netflix.com',   '$2b$12$adminHashExample000001', '1990-01-01', 'Erkek',  'Türkiye', 2, 1),
('Ahmet',    'Yılmaz',    'ahmet@mail.com',       '$2b$12$userHashExample0000001', '1995-03-15', 'Erkek',  'Türkiye', 1, 1),
('Ayşe',     'Kaya',      'ayse@mail.com',        '$2b$12$userHashExample0000002', '1998-07-22', 'Kadın',  'Türkiye', 1, 1),
('Mehmet',   'Demir',     'mehmet@mail.com',      '$2b$12$userHashExample0000003', '1993-11-05', 'Erkek',  'Türkiye', 1, 1),
('Zeynep',   'Çelik',     'zeynep@mail.com',      '$2b$12$userHashExample0000004', '2000-05-30', 'Kadın',  'Türkiye', 1, 1),
('Can',      'Arslan',    'can@mail.com',         '$2b$12$userHashExample0000005', '1997-09-12', 'Erkek',  'Türkiye', 1, 1),
('Elif',     'Şahin',     'elif@mail.com',        '$2b$12$userHashExample0000006', '1996-02-18', 'Kadın',  'Türkiye', 1, 1),
('Burak',    'Koç',       'burak@mail.com',       '$2b$12$userHashExample0000007', '1994-08-25', 'Erkek',  'Almanya', 1, 1),
('Selin',    'Aydın',     'selin@mail.com',       '$2b$12$userHashExample0000008', '1999-12-03', 'Kadın',  'İngiltere', 1, 1),
('Emre',     'Yıldız',    'emre@mail.com',        '$2b$12$userHashExample0000009', '1992-06-14', 'Erkek',  'Türkiye', 1, 1),
('Deniz',    'Güneş',     'deniz@mail.com',       '$2b$12$userHashExample0000010', '2001-04-07', 'Diğer',  'Türkiye', 1, 0);

-- ------------------------------------------------------------
-- KULLANICI TÜR (Her kullanıcıya 3 favori tür)
-- ------------------------------------------------------------
INSERT INTO KullaniciTur (kullanici_id, tur_id) VALUES
-- Ahmet: Aksiyon, Drama, Gerilim
(2, 1), (2, 3), (2, 9),
-- Ayşe: Romantik, Komedi, Drama
(3, 6), (3, 2), (3, 3),
-- Mehmet: Bilim Kurgu, Aksiyon, Korku
(4, 5), (4, 1), (4, 4),
-- Zeynep: Animasyon, Komedi, Romantik
(5, 8), (5, 2), (5, 6),
-- Can: Suç, Gerilim, Drama
(6, 10), (6, 9), (6, 3),
-- Elif: Belgesel, Drama, Romantik
(7, 7), (7, 3), (7, 6),
-- Burak: Aksiyon, Bilim Kurgu, Gerilim
(8, 1), (8, 5), (8, 9),
-- Selin: Komedi, Animasyon, Romantik
(9, 2), (9, 8), (9, 6),
-- Emre: Korku, Gerilim, Suç
(10, 4), (10, 9), (10, 10),
-- Deniz: Belgesel, Bilim Kurgu, Animasyon
(11, 7), (11, 5), (11, 8);

-- ------------------------------------------------------------
-- PROGRAM
-- ------------------------------------------------------------
INSERT INTO Program (program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan) VALUES
('Inception',          'Rüya içinde rüya kurgusu üzerine kurulu aksiyon filmi.',         'Film',  2010, 1,  148, 320, 9.2),
('Breaking Bad',       'Kimya öğretmeninin uyuşturucu dünyasına girişinin hikayesi.',     'Dizi',  2008, 62, 47,  510, 9.5),
('The Dark Knight',    'Batman\'ın Joker ile mücadelesini anlatan süper kahraman filmi.', 'Film',  2008, 1,  152, 280, 9.0),
('Stranger Things',    'Gizemli olayların yaşandığı kasabada geçen bilim kurgu dizisi.',  'Dizi',  2016, 34, 50,  430, 8.7),
('Interstellar',       'İnsanlığın geleceği için uzay yolculuğuna çıkan astronotlar.',    'Film',  2014, 1,  169, 260, 8.9),
('Money Heist',        'Darbeyi planlamak yerine soygun planı kuran dahiler.',             'Dizi',  2017, 41, 70,  390, 8.3),
('The Witcher',        'Canavarlarla savaşan bir savaşçının maceraları.',                  'Dizi',  2019, 16, 60,  310, 7.8),
('Parasite',           'Sınıf çatışmasını ele alan Kore yapımı gerilim filmi.',           'Film',  2019, 1,  132, 190, 8.6),
('Dark',               'Almanya\'da geçen zaman yolculuğu temalı gizem dizisi.',          'Dizi',  2017, 26, 52,  270, 8.8),
('Joker',              'Joker karakterinin kökenini anlatan psikolojik drama filmi.',      'Film',  2019, 1,  122, 240, 8.4),
('Squid Game',         'Hayatta kalmak için yarışan insanların gerilim dizisi.',           'Dizi',  2021, 9,  54,  580, 8.0),
('The Social Network', 'Facebook\'un kuruluş hikayesini anlatan biyografik film.',        'Film',  2010, 1,  120, 170, 7.9),
('Ozark',              'Aile ve suç dünyasının kesiştiği gerilim dizisi.',                 'Dizi',  2017, 44, 60,  290, 8.5),
('Dune',               'Çöl gezegeni üzerinde siyasi ve mistik mücadele.',                'Film',  2021, 1,  155, 210, 8.1),
('Peaky Blinders',     'İngiltere\'de faaliyet gösteren organize suç ailesinin hikayesi.','Dizi',  2013, 36, 58,  350, 8.9);

-- ------------------------------------------------------------
-- PROGRAM TÜR
-- ------------------------------------------------------------
INSERT INTO ProgramTur (program_id, tur_id) VALUES
-- Inception: Aksiyon, Bilim Kurgu, Gerilim
(1, 1), (1, 5), (1, 9),
-- Breaking Bad: Drama, Suç, Gerilim
(2, 3), (2, 10), (2, 9),
-- The Dark Knight: Aksiyon, Suç, Drama
(3, 1), (3, 10), (3, 3),
-- Stranger Things: Bilim Kurgu, Drama, Korku
(4, 5), (4, 3), (4, 4),
-- Interstellar: Bilim Kurgu, Drama
(5, 5), (5, 3),
-- Money Heist: Suç, Drama, Gerilim
(6, 10), (6, 3), (6, 9),
-- The Witcher: Aksiyon, Drama
(7, 1), (7, 3),
-- Parasite: Gerilim, Drama, Suç
(8, 9), (8, 3), (8, 10),
-- Dark: Bilim Kurgu, Drama, Gerilim
(9, 5), (9, 3), (9, 9),
-- Joker: Drama, Gerilim, Suç
(10, 3), (10, 9), (10, 10),
-- Squid Game: Drama, Gerilim, Aksiyon
(11, 3), (11, 9), (11, 1),
-- The Social Network: Drama
(12, 3),
-- Ozark: Suç, Drama, Gerilim
(13, 10), (13, 3), (13, 9),
-- Dune: Bilim Kurgu, Aksiyon, Drama
(14, 5), (14, 1), (14, 3),
-- Peaky Blinders: Suç, Drama, Gerilim
(15, 10), (15, 3), (15, 9);

-- ------------------------------------------------------------
-- BÖLÜM (Diziler için - her diziden ilk 3 bölüm örnek)
-- ------------------------------------------------------------
-- Breaking Bad (program_id=2)
INSERT INTO Bolum (program_id, bolum_no, bolum_adi, sure_dk) VALUES
(2, 1,  'Pilot',                   58),
(2, 2,  'Cat\'s in the Bag',       48),
(2, 3,  'And the Bag\'s in the River', 48),
-- Stranger Things (program_id=4)
(4, 1,  'The Vanishing of Will Byers', 47),
(4, 2,  'The Weirdo on Maple Street',  55),
(4, 3,  'Holly Jolly',                 51),
-- Money Heist (program_id=6)
(6, 1,  'Episodio 1',  70),
(6, 2,  'Episodio 2',  68),
(6, 3,  'Episodio 3',  66),
-- The Witcher (program_id=7)
(7, 1,  'The End\'s Beginning', 59),
(7, 2,  'Four Marks',           56),
(7, 3,  'Betrayer Moon',        62),
-- Dark (program_id=9)
(9, 1,  'Secrets',          52),
(9, 2,  'Lies',             53),
(9, 3,  'Past and Present',  50),
-- Squid Game (program_id=11)
(11, 1, 'Red Light, Green Light', 60),
(11, 2, 'Hell',                   63),
(11, 3, 'The Man with the Umbrella', 56),
-- Ozark (program_id=13)
(13, 1, 'Sugarwood',    60),
(13, 2, 'Blue Cat',     58),
(13, 3, 'Rock Bottom',  62),
-- Peaky Blinders (program_id=15)
(15, 1, 'Episode 1', 57),
(15, 2, 'Episode 2', 59),
(15, 3, 'Episode 3', 58);

-- ------------------------------------------------------------
-- FAVORİ
-- ------------------------------------------------------------
INSERT INTO Favori (kullanici_id, program_id) VALUES
(2, 1), (2, 3), (2, 11),
(3, 6), (3, 10), (3, 12),
(4, 1), (4, 5), (4, 9),
(5, 11), (5, 4), (5, 7),
(6, 2), (6, 13), (6, 15),
(7, 8), (7, 10), (7, 12),
(8, 1), (8, 14), (8, 3),
(9, 6), (9, 11), (9, 4),
(10, 2), (10, 9), (10, 8),
(11, 5), (11, 14);

-- ------------------------------------------------------------
-- KULLANICI PROGRAM (İzleme + Puan)
-- ------------------------------------------------------------
INSERT INTO KullaniciProgram (kullanici_id, program_id, puan, tamamlandi, son_bolum_no, son_izleme_dk, toplam_sure_dk, ilk_izleme_tarihi, son_izleme_tarihi) VALUES
(2,  1,  9, 1, 1,  148, 148, '2025-01-10 20:00:00', '2025-01-10 22:28:00'),
(2,  3,  9, 1, 1,  152, 152, '2025-01-15 19:00:00', '2025-01-15 21:32:00'),
(2,  11, 8, 1, 9,   54, 486, '2025-02-01 21:00:00', '2025-02-10 23:00:00'),
(3,  6,  8, 0, 3,   25, 215, '2025-03-05 20:00:00', '2025-04-01 21:00:00'),
(3,  10, 9, 1, 1,  122, 122, '2025-02-14 20:00:00', '2025-02-14 22:02:00'),
(4,  1,  8, 1, 1,  148, 148, '2025-01-20 21:00:00', '2025-01-20 23:28:00'),
(4,  5,  9, 1, 1,  169, 169, '2025-02-05 20:00:00', '2025-02-05 22:49:00'),
(4,  9,  9, 0, 2,   30, 112, '2025-03-10 21:00:00', '2025-04-05 22:00:00'),
(5,  4,  8, 0, 2,   20, 102, '2025-03-15 20:00:00', '2025-04-10 21:00:00'),
(5,  11, 7, 1, 9,   54, 486, '2025-01-05 20:00:00', '2025-01-15 23:00:00'),
(6,  2,  10,0, 3,   40, 153, '2025-02-20 21:00:00', '2025-04-01 22:00:00'),
(6,  13, 8, 0, 2,   15, 118, '2025-03-01 20:00:00', '2025-03-20 22:00:00'),
(7,  8,  9, 1, 1,  132, 132, '2025-02-10 20:00:00', '2025-02-10 22:12:00'),
(7,  10, 8, 1, 1,  122, 122, '2025-03-05 21:00:00', '2025-03-05 23:02:00'),
(8,  1,  9, 1, 1,  148, 148, '2025-01-25 20:00:00', '2025-01-25 22:28:00'),
(8,  14, 8, 1, 1,  155, 155, '2025-04-02 20:00:00', '2025-04-02 22:35:00'),
(9,  6,  7, 0, 2,   45, 113, '2025-03-20 21:00:00', '2025-04-15 22:00:00'),
(10, 2,  10,0, 3,   47, 153, '2025-02-15 20:00:00', '2025-03-30 23:00:00'),
(10, 9,  9, 0, 1,   30,  82, '2025-04-01 21:00:00', '2025-04-20 22:00:00'),
(11, 5,  8, 1, 1,  169, 169, '2025-01-30 20:00:00', '2025-01-30 22:49:00');

-- ------------------------------------------------------------
-- İZLEME LOG
-- ------------------------------------------------------------
INSERT INTO IzlemeLog (kullanici_id, program_id, bolum_no, izleme_tarihi, izlenen_dk, tamamlandi) VALUES
(2,  1,  1, '2025-01-10 20:00:00', 148, 1),
(2,  3,  1, '2025-01-15 19:00:00', 152, 1),
(2,  11, 1, '2025-02-01 21:00:00',  60, 1),
(2,  11, 2, '2025-02-02 21:00:00',  63, 1),
(2,  11, 9, '2025-02-10 21:00:00',  56, 1),
(3,  6,  1, '2025-03-05 20:00:00',  70, 1),
(3,  6,  2, '2025-03-12 20:00:00',  68, 1),
(3,  6,  3, '2025-04-01 20:00:00',  25, 0),
(3,  10, 1, '2025-02-14 20:00:00', 122, 1),
(4,  1,  1, '2025-01-20 21:00:00', 148, 1),
(4,  5,  1, '2025-02-05 20:00:00', 169, 1),
(4,  9,  1, '2025-03-10 21:00:00',  52, 1),
(4,  9,  2, '2025-04-05 21:00:00',  30, 0),
(5,  4,  1, '2025-03-15 20:00:00',  47, 1),
(5,  4,  2, '2025-04-10 20:00:00',  20, 0),
(5,  11, 1, '2025-01-05 20:00:00',  60, 1),
(5,  11, 9, '2025-01-15 21:00:00',  54, 1),
(6,  2,  1, '2025-02-20 21:00:00',  58, 1),
(6,  2,  2, '2025-03-01 21:00:00',  48, 1),
(6,  2,  3, '2025-04-01 21:00:00',  40, 0),
(6,  13, 1, '2025-03-01 20:00:00',  60, 1),
(6,  13, 2, '2025-03-20 20:00:00',  15, 0),
(7,  8,  1, '2025-02-10 20:00:00', 132, 1),
(7,  10, 1, '2025-03-05 21:00:00', 122, 1),
(8,  1,  1, '2025-01-25 20:00:00', 148, 1),
(8,  14, 1, '2025-04-02 20:00:00', 155, 1),
(9,  6,  1, '2025-03-20 21:00:00',  70, 1),
(9,  6,  2, '2025-04-15 21:00:00',  45, 0),
(10, 2,  1, '2025-02-15 20:00:00',  58, 1),
(10, 2,  2, '2025-03-01 20:00:00',  48, 1),
(10, 2,  3, '2025-03-30 20:00:00',  47, 1),
(10, 9,  1, '2025-04-01 21:00:00',  52, 1),
(10, 9,  2, '2025-04-20 21:00:00',  30, 0),
(11, 5,  1, '2025-01-30 20:00:00', 169, 1);

-- ------------------------------------------------------------
-- OTURUM LOG
-- ------------------------------------------------------------
INSERT INTO OturumLog (kullanici_id, giris_tarihi, cikis_tarihi, ip_adresi) VALUES
(2,  '2025-01-10 19:50:00', '2025-01-10 22:30:00', '192.168.1.10'),
(2,  '2025-01-15 18:55:00', '2025-01-15 21:35:00', '192.168.1.10'),
(3,  '2025-02-14 19:45:00', '2025-02-14 22:10:00', '192.168.1.11'),
(3,  '2025-03-05 19:55:00', '2025-03-05 22:00:00', '192.168.1.11'),
(4,  '2025-01-20 20:50:00', '2025-01-20 23:30:00', '10.0.0.5'),
(4,  '2025-02-05 19:45:00', '2025-02-05 22:55:00', '10.0.0.5'),
(5,  '2025-01-05 19:50:00', '2025-01-05 23:15:00', '10.0.0.6'),
(6,  '2025-02-20 20:45:00', '2025-02-20 23:00:00', '172.16.0.3'),
(7,  '2025-02-10 19:55:00', '2025-02-10 22:15:00', '172.16.0.4'),
(8,  '2025-01-25 19:50:00', '2025-01-25 22:35:00', '192.168.2.20'),
(9,  '2025-03-20 20:55:00', '2025-03-20 23:05:00', '192.168.2.21'),
(10, '2025-02-15 19:45:00', '2025-02-15 23:10:00', '192.168.3.30'),
(11, '2025-01-30 19:50:00', '2025-01-30 22:55:00', '192.168.3.31');
