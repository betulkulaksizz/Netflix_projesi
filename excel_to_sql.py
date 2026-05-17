import pandas as pd
from pathlib import Path

INPUT_XLSX = Path("Netflix DB (1).xlsx")
OUTPUT_SQL = Path("full_data.sql")


def _clean_text(value) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().replace("'", "''")


def _duration_from_row(row) -> int:
    if len(row) > 3 and not pd.isna(row[3]):
        try:
            return int(float(row[3]))
        except (TypeError, ValueError):
            return 0
    return 0


df = pd.read_excel(INPUT_XLSX, header=None)

sql_lines = [
    "USE netflix_platform;\n\n",
    "SET FOREIGN_KEY_CHECKS = 0;\n",
    "TRUNCATE TABLE ProgramTur;\n",
    "TRUNCATE TABLE Favori;\n",
    "TRUNCATE TABLE KullaniciProgram;\n",
    "TRUNCATE TABLE IzlemeLog;\n",
    "TRUNCATE TABLE Program;\n",
    "SET FOREIGN_KEY_CHECKS = 1;\n\n",
]

for _, row in df.iterrows():
    program_adi = _clean_text(row[0])
    turler = _clean_text(row[1])
    program_tipi = str(row[2]).strip() if len(row) > 2 and not pd.isna(row[2]) else "Film"
    bolum_uzunluk_dk = _duration_from_row(row)

    if program_tipi not in ["Film", "Dizi"]:
        program_tipi = "Film"

    sql_lines.append(f"""
INSERT INTO Program 
(program_adi, aciklama, program_tipi, yayin_yili, bolum_sayisi, bolum_uzunluk_dk, toplam_izlenme, ortalama_puan)
VALUES
('{program_adi}', '{turler}', '{program_tipi}', 2024, 1, {bolum_uzunluk_dk}, 0, 0.0);
""")

    tur_listesi = [t.strip() for t in turler.split(",") if t.strip()]

    for tur in tur_listesi:
        tur = tur.replace("'", "''")

        sql_lines.append(f"""
INSERT IGNORE INTO Tur (tur_adi)
VALUES ('{tur}');
""")

        sql_lines.append(f"""
INSERT IGNORE INTO ProgramTur (program_id, tur_id)
SELECT p.program_id, t.tur_id
FROM Program p
JOIN Tur t
WHERE p.program_adi = '{program_adi}'
AND t.tur_adi = '{tur}';
""")

with OUTPUT_SQL.open("w", encoding="utf-8") as f:
    f.writelines(sql_lines)

print("full_data.sql oluşturuldu.")
print(f"Toplam {len(df)} içerik eklenecek.")
