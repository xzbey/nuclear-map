from pathlib import Path
import pandas as pd #pip install pandas
import json

path = 'USSR-ntests2'
country = ['USA', "USSR", "UK", "FR", "PRC", "OTH"]

db_dir = Path(__file__).parent.parent / 'db' / 'csv'

df = pd.read_csv(db_dir / (path + '.csv'), sep=';')
df['site'] = df['site'].str.replace("'", "")
#print(df)

site_usa = {
    'AK': 'Amichitka Island, Alaska',
    'BK':'Bikini Atoll, Trust Territory of the Pacific Islands (now Marshall Islands)',
    'EN':'Enwetak Atoll, Trust Territory of the Pacific Islands (now Marshall Islands)',
    'JO':'Johnston Island',
    'LI-CH':'Christmas Island, Line Islands (now Kiritimati), Pacific Ocean',
    'NARF':'Nellis Air Force Range, Nevada',
    'NAFR':'Nellis Air Force Range, Nevada',
    'NM-A':'Alamagordo area, New Mexico',
    'NM':'New Mexico',
    'NV-FF':'Nevada Test Site, Nevada, USA, Frenchman Flat',
    'NV-PM':'Nevada Test Site, Nevada, USA, Pahute Mesa',
    'NV-RM':'Nevada Test Site, Nevada, USA, Rainier Mesa',
    'NV-YF':'Nevada Test Site, Nevada, USA, Yucca Flat',
    'NV-15':'Nevada Test Site, Nevada, USA, Area 15',
    'NV-16':'Nevada Test Site, Nevada, USA, Area 16',
    'NV-18':'Nevada Test Site, Nevada, USA, Area 18',
    'NV-30':'Nevada Test Site, Nevada, USA, Area 30',
    'NTS-FF':'Nevada Test Site, Nevada, USA, Frenchman Flat',
    'NTS-PM':'Nevada Test Site, Nevada, USA, Pahute Mesa',
    'NTS-RM':'Nevada Test Site, Nevada, USA, Rainier Mesa',
    'NTS-YF':'Nevada Test Site, Nevada, USA, Yucca Flat',
    'NTS-15':'Nevada Test Site, Nevada, USA, Area 15',
    'NTS-16':'Nevada Test Site, Nevada, USA, Area 16',
    'NTS-18':'Nevada Test Site, Nevada, USA, Area 18',
    'NTS-30':'Nevada Test Site, Nevada, USA, Area 30',
    '-CO':'Colorado',
    '-JP':'Japan (two combat uses)',
    '-LA':'Los Alamos National Laboratory, New Mexico',
    '-MS':'Mississippi',
    '-NM':'New Mexico (outside test ranges)',
    '-NV':'Nevada (outside test ranges)',
    '-PAC':'Pacific Ocean',
    '-SATL':'South Atlantic Ocean',
    '-SATL  -':'South Atlantic Ocean'
}
site_ussr = {
    'MTR':'Missile Testing Range',
    'NZ':'Novaya Zemlya',
    'NZ-CB':'Novaya Zemlya, Chernaya Bay',
    'NZ-CB?':'Novaya Zemlya, Chernaya Bay',
    'NZ-MB':'Novaya Zemlya, Mityushikha Bay',
    'NZ-MB?':'Novaya Zemlya, Mityushikha Bay',
    'NZ-NS':'Novaya Zemlya, Northern Site (Matochkin Shar)',
    'NZ-SS':'Novaya Zemlya, Southern Site (Belushya)',
    'STS':'Semipalatinsk',
    'STS-B':'Semipalatinsk, Balapan',
    'STS-D':'Semipalatinsk, Degelen',
    'STS-GZ':'Semipalatinsk, Ground Zero (Technical Area Sh)',
    'STS-SU':'Semipalatinsk, Sary-Uzen',
    'STS-T':'Semipalatinsk, Telkem',
    '-KZ':'Kazakhstan',
    '-KZ-BA':'Kazakhstan, Bolshoy Azgir area',
    '-KZ-KA':'Kazakhstan, Karachaganakskoye oil field',
    '-KZ-MA':'Kazakhstan, Mangyshlak oblast',
    '-RU':'Russia',
    '-RU-A':'Russia, Arkhangelsk area',
    '-RU-AS':'Russia, Astrakhan gas deposit',
    '-RU-BK':'Russia, Bashkir',
    '-RU-K':'Russia, Krasnoyarsk area',
    '-RU-M':'Russia, Murmansk',
    '-RU-O':'Russia, Orenberg area',
    '-RU-P':'Russia, Perm area',
    '-RU-T':'Russia, Tuymen area',
    '-RU-YK':'Russia, Yakutia',
    '-TU':'Turkmenistan',
    '-UK':'Ukraine',
    '-UZ':'Uzbekistan',
}
site_uk = {
    'LI-CH':'Christmas Island (now Kiritimati)',
    'LI-MI':'Malden Island',
    'MB':'Monte Bello Islands, Western Australia, Australia',
    'NTS-PM':'Nevada Test Site, Nevada, United States, Pahute Mesa',
    'NTS-YF':'Nevada Test Site, Nevada, United States, Yucca Flat',
    'SAU-EF':'South Australia, Emu Field',
    'SAU-MR':'South Australia, Maralinga range',
    'SAU-NA':'South Australia, Maralinga, Naya site',
    'SAU-WE':'South Australia, Maralinga, Wewak site',
}
site_fr = {
    'AL-IE':'French Algeria, In Ecker (CSEM)',
    'AL-R':'French Algeria, Reggane Proving Ground (CEMO)',
    'PFA-FR':'Pacific Test Site (CEP), Fangataufa, Fregate zone',
    'PFA-L':'Pacific Test Site (CEP), Fangataufa, lagoon',
    'PFA-L2':'Pacific Test Site (CEP), Fangataufa, lagoon, area 2',
    'PFA-R1':'Pacific Test Site (CEP), Fangataufa, rim, area 1 (southern rim)',
    'PMU-L':'Pacific Test Site (CEP), Mururoa, lagoon (areas 5, 6, 7)',
    'PMU-CO':'Pacific Test Site (CEP), Mururoa, Colette zone',
    'PMU-DE':'Pacific Test Site (CEP), Mururoa, Denise zone',
    'PMU-DI':'Pacific Test Site (CEP), Mururoa, Dindon zone',
    'PMU-R':'Pacific Test Site (CEP), Mururoa, rim (areas 1, 2, 3, 4)',
    'PMU-R34':'Pacific Test Site (CEP), Mururoa, rim, areas 3 and 4 (islands of Zoe and Yvonne)',
}
site_prc = {
    'LN':'Lop Nor',
    'LN-A':'Lop Nor, area "A"',
    'LN-B':'Lop Nor, area "B"',
    'LN-C':'Lop Nor, area "C"',
    'LN-D':'Lop Nor, area "D"',
}
site_oth = {
    'CHA':'Chagai Hills, Pakistan',
    'POK':'Pokoran, India',
    '-SATL':'South Atlantic Ocean',
}

type_usa = {
    'A-AD':'atmospheric, airdrop',
    'A-B':'atmospheric, balloon',
    'A-R':'atmospheric, rocket or missile',
    'AH-R':'atmospheric, high altitude (between 30 km and 80 km), rocket or missile',
    'AS-T':'atmospheric, surface ,tower',
    'AW-BG':'atmospheric, water surface, barge',
    'AX-R':'space (altitude over 80 km), rocket or missile',
    'CR':'cratering burst (shallow subsurface)',
    'UG-S':'underground, shaft',
    'UG-T':'underground, tunnel',
    'UG-TC':'underground, cavity in tunnel',
    'UW':'underwater',
}
type_ussr = {
    'A':'atmospheric',
    'A-AD':'atmospheric, airdrop',
    'A-CM':'atmospheric, cruise missile',
    'A-R':'atmospheric, rocket or missile',
    'AH-R':'atmospheric, high altitude (between 30 km and 80 km), rocket',
    'AS-AD':'atmospheric, surface, airdrop',
    'AS-R':'atmospheric, surface, rocket or missile',
    'AS-T':'atmospheric, surface, tower',
    'AW-AS':'atmospheric, water surface, anti-submarine weapon or torpedo',
    'AW-CM':'atmospheric, water surface, cruise missile',
    'AX-R':'space (altitude over 80 km), rocket',
    'UG-CS':'underground, cavity, shaft',
    'UG-M':'underground, mine',
    'UG-S':'underground, shaft',
    'UG-T':'underground, tunnel',
    'UW-AS':'underwater, antisubmarine weapon or torpedo',
    'UW-B':'underwater, barge',
}
type_uk = {
    'A-AD':'atmospheric, airdrop',
    'A-B':'atmospheric, balloon',
    'AS-T':'atmospheric, surface, tower',
    'AW-BG':'atmospheric, water surface, barge',
    'UG-S':'underground, shaft',
}
type_fr = {
    'A-AD':'atmospheric, airdrop',
    'A-B':'atmospheric, balloon',
    'AS-T':'atmospheric, surface, tower',
    'AW-B':'atmospheric, water surface, balloon',
    'AW-BG':'atmospheric, water surface, barge',
    'UG-S':'underground, shaft',
    'UG-T':'underground, tunnel',
}
type_prc = {
    'A-AD':'atmospheric, airdrop',
    'A-R':'atmospheric, rocket or missile',
    'AS-T':'atmospheric, surface, tower',
    'UG':'underground',
    'UG-S':'underground, shaft',
    'UG-S?':'underground, shaft?',
    'UG-T':'underground, tunnel',
    'UG-T?':'underground, tunnel?',
}
type_oth = {
    'A':'atmospheric',
    'UG':'underground',
    'UG-S':'underground, shaft',
    'UG-T':'underground, tunnel',
}

purpose_usa = {
    'C':'combat use, strategic warfare',
    'PR':'peaceful research',
    'SE':'safety experiment',
    'ST':'safety/transport experiment',
    'VU':'Vela uniform test',
    'WE':'weapons effects',
    'WR':'nuclear weapons related',
    'WR?':'nuclear weapons related?',
}
purpose_ussr = {
    'FS':'fundamental science',
    'I':'industrial applications',
    'I-CV':'industrial applications, cavity excavation',
    'I-EM':'industrial applications, earth-moving',
    'I-FE':'industrial applications, extinguishing of oil/gas well fire',
    'I-OS':'industrial applications, oil stimulation',
    'I-SS':'industrial applications, seismic sounding',
    'JV':'joint verification',
    'ME':'military exercise',
    'PR':'research for peaceful applications',
    'SE':'safety experiment',
    'ST':'storage/transportation experiment',
    'VU':'Vela uniform',
    'WE':'weapons effects',
    'WR':'nuclear weapons related',
}

if "USA" in path:
    site = site_usa
    type_ = type_usa
    purpose = purpose_usa
elif "USSR" in path:
    site = site_ussr
    type_ = type_ussr
    purpose = purpose_ussr
elif "UK" in path:
    site = site_uk
    type_ = type_uk
    purpose = purpose_usa
elif "FR" in path:
    site = site_fr
    type_ = type_fr
    purpose = purpose_usa
elif "PRC" in path:
    site = site_prc
    type_ = type_prc
    purpose = purpose_usa
else:
    site = site_oth
    type_ = type_oth
    purpose = purpose_usa

df['site'] = df['site'].map(site).fillna(df['site'])
df['type'] = df['type'].map(type_).fillna(df['type'])
df['purpose'] = df['purpose'].map(purpose).fillna(df['purpose'])
df = df.fillna('Unknown')

features = []
for _, row in df.iterrows():
    #print(type(row['lat']))
    feature = {
        "type": "Feature",
        "properties": {
            "id": row['id'],
            "series": row['series'],
            "shot": row['shot'],
            "date": f"{row['day']}.{row['mon']}.{row['year']}",
            "year": row['year'],
            "time": row['time'],
            "site": row['site'],
            "type": row['type'],
            "purpose": row['purpose'],
            "yield": f"min: {row['yield_min']}, max: {row['yield_max']}",
            "crater": row['crater'],
            "warhead": row['warhead'],
            "sponsor": row['sponsor'],
            "impact": 'test',
            "country": path[:path.find('-')]
        },
        "geometry": {
            "type": "Point",
            "coordinates": [row['lon'], float(row['lat'].split()[-1]) if type(row['lat'])==str else row['lat']]
        }
    }
    features.append(feature)

geojson = {
    "type": "FeatureCollection",
    "features": features
}

out_dir = Path(__file__).parent.parent / 'db' / 'geojson'
out_dir.mkdir(exist_ok=True)

with open(out_dir / (path + '.geojson'), 'w') as f:
    json.dump(geojson, f, indent=2, ensure_ascii=False)

print('Готово, записей ' + str(len(features)))