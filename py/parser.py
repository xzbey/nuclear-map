from bs4 import BeautifulSoup #pip install beautifulsoup4
import requests #pip install requests
import csv

url = "https://johnstonsarchive.net/nuclear/tests/OTH-ntests1.html"
html = requests.get(url).text
soup = BeautifulSoup(html, "html.parser")
pre = soup.find("pre").get_text()

col_usa = [
    ("id",           0,  7),
    ("series",       7,  23),
    ("shot",        23,  43),
    ("year",        46,  52),
    ("mon",         52,  57),
    ("day",         57,  62),
    ("time",        62,  76),
    ("site",        76,  84),
    ("lat",         84,  94),
    ("lon",         94,  104),
    ("hob",        120,  127),
    ("gzalt",      127,  134),
    ("type",       134,  146),
    ("purpose",    146,  148),
    ("yield_min",  148,  156),
    ("yield_max",  156,  162),
    ("yield_kt",   172,  178),
    ("crater",     187,  191),
    ("warhead",    204,  214),
    ("sponsor",    214,  218)
]

col_ussr = [
    ("id",           0,  7),
    ("series",       7,  23),
    ("shot",        23,  43),
    ("year",        48,  52),
    ("mon",         52,  57),
    ("day",         57,  62),
    ("time",        62,  76),
    ("site",        76,  84),
    ("lat",         84,  94),
    ("lon",         94,  106),
    ("hob",        122,  129),
    ("gzalt",      129,  136),
    ("type",       141,  146),
    ("purpose",    146,  152),
    ("yield_min",  152,  158),
    ("yield_max",  158,  165),
    ("yield_kt",   175,  180),
    ("crater",     187,  191),
    ("warhead",    203,  214),
    ("sponsor",    214,  219)
]

col_uk = [
    ("id",           0,  7),
    ("series",       7,  23),
    ("shot",        23,  46),
    ("year",        46,  52),
    ("mon",         52,  57),
    ("day",         57,  62),
    ("time",        62,  76),
    ("site",        76,  83),
    ("lat",         83,  94),
    ("lon",         94,  106),
    ("hob",        120,  129),
    ("gzalt",      129,  136),
    ("type",       139,  146),
    ("purpose",    146,  152),
    ("yield_min",  152,  158),
    ("yield_max",  158,  165),
    ("yield_kt",   174,  180),
    ("crater",     187,  191),
    ("warhead",    203,  217),
    ("sponsor",    214,  219)
]

col_fr = [
    ("id",           0,  7),
    ("series",       7,  23),
    ("shot",        23,  43),
    ("year",        46,  52),
    ("mon",         52,  57),
    ("day",         57,  62),
    ("time",        62,  76),
    ("site",        76,  84),
    ("lat",         84,  95),
    ("lon",         95,  107),
    ("hob",        120,  130),
    ("gzalt",      130,  137),
    ("type",       140,  147),
    ("purpose",    147,  153),
    ("yield_min",  153,  159),
    ("yield_max",  159,  165),
    ("yield_kt",   174,  182),
    ("crater",     187,  191),
    ("warhead",    203,  217),
    ("sponsor",    214,  219)
]

col_prc = [
    ("id",           0,  7),
    ("series",       7,  23),
    ("shot",        23,  46),
    ("year",        46,  52),
    ("mon",         52,  57),
    ("day",         57,  62),
    ("time",        62,  76),
    ("site",        76,  84),
    ("lat",         84,  95),
    ("lon",         95,  107),
    ("hob",        120,  130),
    ("gzalt",      130,  137),
    ("type",       139,  147),
    ("purpose",    147,  153),
    ("yield_min",  153,  159),
    ("yield_max",  159,  165),
    ("yield_kt",   174,  181),
    ("crater",     187,  191),
    ("warhead",    203,  217),
    ("sponsor",    214,  219)
]

col_oth = [
    ("id",           0,  7),
    ("series",       7,  23),
    ("shot",        23,  45),
    ("year",        47,  52),
    ("mon",         52,  57),
    ("day",         57,  62),
    ("time",        62,  76),
    ("site",        76,  84),
    ("lat",         84,  95),
    ("lon",         95,  107),
    ("hob",        123,  130),
    ("gzalt",      130,  137),
    ("type",       139,  147),
    ("purpose",    147,  153),
    ("yield_min",  153,  159),
    ("yield_max",  159,  165),
    ("yield_kt",   174,  181),
    ("crater",     187,  191),
    ("warhead",    203,  217),
    ("sponsor",    214,  219)
]

col = col_oth
results = []
for line in pre.splitlines():
    if not line.strip():
        continue

    row = {}
    for name, start, end in col:
        row[name] = line[start:end].strip()

    results.append(row)

results = results[2:]
if url == "https://johnstonsarchive.net/nuclear/tests/OTH-ntests1.html": #комменты про другие страны в other
    del results[0]
    del results[6]
    del results[13]
    del results[14]

fieldnames = [item[0] for item in col]
colspecs = [(item[0], item[1]) for item in col]
print("successful parse")

numeric_fields = {"yield_min", "yield_max", "yield_kt", "crater", "hob", "gzalt"}
for row in results:
    if 'site' in row:
        row['site'] = "'" + row['site']
    for field in numeric_fields:
        if field in row and row[field]:
            row[field] = row[field].replace(".", ",")

with open("OTH-ntests1.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames,
        delimiter=";",
        quoting=csv.QUOTE_MINIMAL,
        quotechar='"'
    )
    writer.writeheader()
    writer.writerows(results)

print("successful upload in csv")
'''for x in results:
    print(x)'''

print("end")