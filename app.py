import pandas as pd
import re
import csv
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
CORS(app)

# --- 1. DEFINISI ENTITAS DAN KATA KUNCI (DARI SKRIP PERTAMA) ---
LOKASI_JAKARTA = [
    # Jakarta Pusat
    {'nama_jalan': 'sudirman', 'keywords': ['sudirman', 'jl jend sudirman', 'jendral sudirman', 'fx sudirman'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'thamrin', 'keywords': ['thamrin', 'mh thamrin', 'jl mh thamrin'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'bundaran hi', 'keywords': ['bundaran hi', 'bunderan hi', 'hotel indonesia', 'plaza gi'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'monas', 'keywords': ['monas', 'silang monas', 'monas timur', 'kawasan monas'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'patung kuda', 'keywords': ['patung kuda', 'bundaran patung kuda', 'monas barat daya'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'gbk', 'keywords': ['gbk', 'gelora bung karno', 'pintu 10 gbk', 'gbk senayan'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'senayan', 'keywords': ['senayan', 'bundaran senayan', 'senayan city', 'plaza senayan', 'lapangan tembak senayan'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'simpang lima senen', 'keywords': ['simpang lima senen', 'senen', 'stasiun senen', 'ps senen'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'cempaka putih', 'keywords': ['cempaka putih'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'salemba', 'keywords': ['salemba', 'salemba raya', 'tl carolus'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'tugu tani', 'keywords': ['tugu tani'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'gambir', 'keywords': ['gambir'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'kwitang', 'keywords': ['kwitang'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'harmoni', 'keywords': ['harmoni'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'kemayoran', 'keywords': ['kemayoran', 'jiexpo kemayoran'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'palmerah', 'keywords': ['palmerah'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'parman', 'keywords': ['parman', 's parman', 'jl s parman', 'letjend s parman'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'pejompongan', 'keywords': ['pejompongan', 'penjernihan'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'suryopranoto', 'keywords': ['suryopranoto', 'jl suryopranoto'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'gunung sahari', 'keywords': ['gunung sahari', 'jl gunung sahari'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'pintu besi', 'keywords': ['pintu besi'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'kramat raya', 'keywords': ['kramat raya', 'jl kramat raya'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'kramat bunder', 'keywords': ['kramat bunder', 'jl kramat bunder'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'letjen suprapto', 'keywords': ['letjen suprapto', 'jl letjen suprapto'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'asia afrika', 'keywords': ['asia afrika', 'jl asia afrika'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'gerbang pemuda', 'keywords': ['gerbang pemuda', 'jl gerbang pemuda'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'biak', 'keywords': ['biak', 'tl biak'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'dukuh atas', 'keywords': ['dukuh atas'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'tanah abang', 'keywords': ['tanah abang'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'sarinah', 'keywords': ['sarinah'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'kebon sirih', 'keywords': ['kebon sirih'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'wahidin', 'keywords': ['wahidin', 'jl dr wahidin'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'karet bivak', 'keywords': ['karet bivak'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'dpr/mpr', 'keywords': ['dpr ri', 'dpr/mpr ri', 'gedung dpr/mpr'], 'wilayah': 'jakarta pusat'},
    {'nama_jalan': 'lapangan banteng', 'keywords': ['lapangan banteng'], 'wilayah': 'jakarta pusat'},
    # Jakarta Selatan
    {'nama_jalan': 'gatot subroto', 'keywords': ['gatot subroto', 'gatsu', 'jl gatot subroto'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'kuningan', 'keywords': ['kuningan', 'gt kuningan', 'mall kuningan city', 'rasuna said', 'jl rasuna said', 'hr rasuna said'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'pancoran', 'keywords': ['pancoran'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'semanggi', 'keywords': ['semanggi', 'plaza semanggi', 'jembatan semanggi', 'gt semanggi', 'off ramp semanggi'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'tendean', 'keywords': ['tendean'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'fatmawati', 'keywords': ['fatmawati', 'on ramp fatmawati', 'mrt fatmawati'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'lebak bulus', 'keywords': ['lebak bulus'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'cilandak', 'keywords': ['cilandak', 'gt cilandak'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'pasar minggu', 'keywords': ['pasar minggu', 'ps minggu'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'kalibata', 'keywords': ['kalibata', 'tl kalibata'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'ragunan', 'keywords': ['ragunan', 'taman margasatwa ragunan'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'blok m', 'keywords': ['blok m'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'mt haryono', 'keywords': ['mt haryono', 'jl mt haryono'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'tb simatupang', 'keywords': ['tb simatupang', 'jl tb simatupang'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'pondok indah', 'keywords': ['pondok indah', 'pim', 'underpass pim'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'bintaro', 'keywords': ['bintaro', 'hankam bintaro'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'antasari', 'keywords': ['antasari', 'jlnt antasari'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'prapanca', 'keywords': ['prapanca raya'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'satrio', 'keywords': ['jl dr satrio', 'jl satrio', 'casablanca', 'jlnt casablanca'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'mampang', 'keywords': ['mampang', 'mampang prapatan'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'tebet', 'keywords': ['tebet', 'off ramp tebet'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'cipete', 'keywords': ['cipete', 'off ramp cipete'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'ampera', 'keywords': ['ampera', 'gt ampera'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'pakubuwono', 'keywords': ['pakubuwono'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'iskandarsyah', 'keywords': ['iskandarsyah raya'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'melawai', 'keywords': ['melawai'], 'wilayah': 'jakarta selatan'},
    {'nama_jalan': 'panglima polim', 'keywords': ['panglima polim'], 'wilayah': 'jakarta selatan'},
    # Jakarta Timur
    {'nama_jalan': 'cawang', 'keywords': ['cawang', 'cawang kompor', 'uki cawang', 'cawang interchange'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'ahmad yani', 'keywords': ['ahmad yani', 'jl ahmad yani'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'rawamangun', 'keywords': ['rawamangun', 'mega rawamangun'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'panjaitan', 'keywords': ['panjaitan', 'jl di panjaitan'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'matraman', 'keywords': ['matraman'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'jatinegara', 'keywords': ['jatinegara', 'kodim lama jatinegara'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'kampung rambutan', 'keywords': ['kampung rambutan', 'kp rambutan'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'pasar rebo', 'keywords': ['pasar rebo', 'ps rebo'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'tmii', 'keywords': ['tmii', 'taman mini', 'pintu 1 tmii'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'pgc', 'keywords': ['pgc', 'pgc cililitan'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'cililitan', 'keywords': ['cililitan'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'condet', 'keywords': ['condet'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'cakung', 'keywords': ['cakung', 'kolong cakung', 'pospol cakung'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'pulogadung', 'keywords': ['pulogadung', 'pulo gadung'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'bekasi raya', 'keywords': ['jl raya bekasi', 'bekasi raya'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'halim', 'keywords': ['halim', 'halim baru', 'halim lama'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'dewi sartika', 'keywords': ['dewi sartika', 'jl dewi sartika'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'bogor raya', 'keywords': ['bogor raya', 'jl raya bogor'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'arion', 'keywords': ['arion', 'lampu merah arion'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'pramuka', 'keywords': ['jl pramuka raya'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'bambu apus', 'keywords': ['bambu apus'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'cibubur', 'keywords': ['cibubur', 'cibubur junction'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'tamini square', 'keywords': ['tamini square', 'lampu merah garuda', 'tmi square'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'cijantung', 'keywords': ['cijantung'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'pinang ranti', 'keywords': ['pinang ranti'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'otista', 'keywords': ['otista raya'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'utan kayu', 'keywords': ['utan kayu'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'caglak', 'keywords': ['caglak', 'tl caglak'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'rindam', 'keywords': ['rindam'], 'wilayah': 'jakarta timur'},
    {'nama_jalan': 'kiwi', 'keywords': ['kiwi', 'tl kiwi'], 'wilayah': 'jakarta timur'},
    # Jakarta Barat
    {'nama_jalan': 'daan mogot', 'keywords': ['daan mogot', 'jl daan mogot', 'daanmogot baru'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'slipi', 'keywords': ['slipi', 'lampu merah slipi', 'tl slipi'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'tomang', 'keywords': ['tomang', 'underpass tomang'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'grogol', 'keywords': ['grogol', 'central park', 'rs darmais'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'cengkareng', 'keywords': ['cengkareng', 'tl cengkareng'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'kalideres', 'keywords': ['kalideres'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'pesing', 'keywords': ['pesing'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'kota', 'keywords': ['kota', 'stasiun kota', 'kota tua'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'asemka', 'keywords': ['asemka', 'tl asemka'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'jembatan lima', 'keywords': ['jembatan lima'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'jalan panjang', 'keywords': ['jl panjang', 'jalan panjang'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'puri kembangan', 'keywords': ['puri kembangan', 'ringroad puri'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'kedoya', 'keywords': ['kedoya'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'latumenten', 'keywords': ['latumenten'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'meruya', 'keywords': ['meruya', 'gt meruya'], 'wilayah': 'jakarta barat'},
    {'nama_jalan': 'roxy', 'keywords': ['roxy'], 'wilayah': 'jakarta barat'},
    # Jakarta Utara
    {'nama_jalan': 'priok', 'keywords': ['priok', 'tanjung priok', 'tj priok', 'pelabuhan tj priok'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'ancol', 'keywords': ['ancol', 'taman impian jaya ancol', 'bintang mas ancol'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'pluit', 'keywords': ['pluit', 'emporium pluit', 'gt pluit'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'kelapa gading', 'keywords': ['kelapa gading', 'moi', 'mall of indonesia'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'sunter', 'keywords': ['sunter'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'cilincing', 'keywords': ['cilincing', 'jl cakung cilincing'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'koja', 'keywords': ['koja', 'tl jaya koja'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'marunda', 'keywords': ['marunda'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'pademangan', 'keywords': ['pademangan'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'muara angke', 'keywords': ['muara angke'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'jembatan tiga', 'keywords': ['jembatan tiga'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'perintis', 'keywords': ['perintis', 'tl perintis'], 'wilayah': 'jakarta utara'},
    {'nama_jalan': 'kebon baru', 'keywords': ['kebon baru', 'tl kebon baru'], 'wilayah': 'jakarta utara'},
    # Ruas Tol
    {'nama_jalan': 'tol dalam kota', 'keywords': ['tol dalam kota', 'dalkot', 'ruas tol dalam kota'], 'wilayah': 'lintas wilayah'},
    {'nama_jalan': 'tol jakarta-cikampek', 'keywords': ['tol jakarta-cikampek', 'tol japek', 'ruas tol japek'], 'wilayah': 'lintas wilayah'},
    {'nama_jalan': 'tol jagorawi', 'keywords': ['tol jagorawi', 'ruas tol jagorawi'], 'wilayah': 'lintas wilayah'},
    {'nama_jalan': 'tol jakarta-tangerang', 'keywords': ['tol jakarta-tangerang', 'ruas tol jakarta-tangerang', 'tol janger'], 'wilayah': 'lintas wilayah'},
    {'nama_jalan': 'tol jorr', 'keywords': ['tol jorr', 'ruas tol jorr', 'jorr w2s'], 'wilayah': 'lintas wilayah'},
    {'nama_jalan': 'tol sedyatmo', 'keywords': ['tol sedyatmo', 'ruas tol sedyatmo', 'tol bandara'], 'wilayah': 'lintas wilayah'},
    {'nama_jalan': 'tol cawang-priok', 'keywords': ['tol cawang - tanjung priok', 'tol wiyoto wiyono'], 'wilayah': 'lintas wilayah'},
    {'nama_jalan': 'layang mbz', 'keywords': ['layang mbz'], 'wilayah': 'lintas wilayah'},
    {'nama_jalan': 'cikunir', 'keywords': ['cikunir', 'off ramp cikunir', 'gt cikunir', 'km 09+750'], 'wilayah': 'bekasi'},
    # Lainnya
    {'nama_jalan': 'bandara soetta', 'keywords': ['bandara soetta', 'bandara soekarno hatta'], 'wilayah': 'tangerang'},
    {'nama_jalan': 'bekasi', 'keywords': ['bekasi'], 'wilayah': 'bekasi'},
    {'nama_jalan': 'depok', 'keywords': ['depok'], 'wilayah': 'depok'},
    {'nama_jalan': 'tangerang', 'keywords': ['tangerang'], 'wilayah': 'tangerang'},
    {'nama_jalan': 'jatiasih', 'keywords': ['jatiasih'], 'wilayah': 'bekasi'},
]

ALL_LOC_KEYWORDS_REGEX = []
for loc in LOKASI_JAKARTA:
    for keyword in loc['keywords']:
        ALL_LOC_KEYWORDS_REGEX.append(keyword)
ALL_LOC_KEYWORDS_REGEX = sorted(list(set(ALL_LOC_KEYWORDS_REGEX)), key=len, reverse=True)

STATUS_KEYWORDS_REGEX = {
    'padat merayap': ['padat merayap'],
    'ramai cenderung padat': ['ramai cenderung padat'],
    'cukup padat': ['cukup padat', 'agak padat'],
    'padat': ['padat'],
    'tersendat': ['tersendat', 'terhambat', 'sedikit terhambat'],
    'ramai lancar': ['ramai lancar', 'ramai lancer'],
    'lancar': ['lancar'],
    'kondusif': ['kondusif'],
}

OBSTACLE_KEYWORDS_REGEX = {
    'proyek': ['proyek', 'pengerjaan', 'betonisasi jalan', 'pembetonan', 'perbaikan jalan', 'perbaikan', 'pengaspalan', 'pembangunan lrt', 'galian'],
    'kecelakaan': ['kecelakaan', 'laka lantas', 'gangguan ban', 'ban pecah'],
    'kendaraan gangguan': ['gangguan', 'mogok', 'kendala'],
    'demonstrasi': ['penyampaian pendapat', 'aksi masyarakat', 'aliansi mahasiswa'],
    'kegiatan': ['kegiatan', 'fun run', 'konser', 'pertandingan sepak bola', 'hbkb'],
    'balap liar': ['balap liar'],
    'banjir': ['banjir', 'genangan'],
    'rekayasa lalin': ['rekayasa lalu lintas', 'buka tutup', 'pengalihan arus', 'penutupan arus'],
    'antrian': ['antrian kendaraan', 'antrian'],
    'volume kendaraan': ['volume kendaraan'],
}

WEATHER_KEYWORDS_REGEX = {
    'hujan': ['hujan'],
    'gerimis': ['gerimis'],
    'berawan': ['berawan'],
    'cerah': ['cerah'],
}

BIDIRECTIONAL_KEYWORDS_REGEX = [
    'arah sebaliknya', 'kedua arah', 'dan sebaliknya', 'maupun arah sebaliknya',
    'arah berlawanan', 'maupun arah', 'arah ... maupun arah', 'dari ... menuju ... maupun'
]

# --- 2. FUNGSI-FUNGSI EKSTRAKSI (DARI SKRIP PERTAMA) ---
def find_keywords_regex(text, keyword_map):
    for canonical, variations in keyword_map.items():
        for var in variations:
            if var in text:
                return canonical
    return None

def ner_locations_regex(text, location_keywords):
    found_locations = []
    temp_text = " " + text + " "
    for loc in location_keywords:
        if f" {loc} " in temp_text:
            found_locations.append(loc)
            temp_text = temp_text.replace(f" {loc} ", " <LOC_FOUND> ", 1)
    found_locations.sort(key=lambda x: text.find(x))
    return list(dict.fromkeys(found_locations))

def determine_from_to_regex(text, locations):
    if len(locations) < 2:
        return []
    pairs = []

    maupun_match = re.search(r'di (.*?) arah (.*?) maupun arah (.*)', text)
    if maupun_match and len(locations) > 0:
        source = locations[0]
        for dest in locations[1:]:
            if dest in maupun_match.group(0):
                pairs.append((source, dest))
        if pairs: return pairs

    for i in range(len(locations) - 1):
        loc1_re = re.escape(locations[i])
        loc2_re = re.escape(locations[i+1])
        pattern = re.compile(f"{loc1_re}.*?(?:arah|menuju|ke|menuju arah){{1,2}}.*{loc2_re}")
        if pattern.search(text):
            pairs.append((locations[i], locations[i+1]))

    for i in range(len(locations) - 1):
        loc1_re = re.escape(locations[i])
        loc2_re = re.escape(locations[i+1])
        pattern = re.compile(f"dari {loc1_re} (?:menuju|ke) {loc2_re}")
        if pattern.search(text):
            pairs.append((locations[i], locations[i+1]))

    if not pairs and len(locations) >= 2:
        pairs.append((locations[0], locations[1]))

    return list(dict.fromkeys(pairs))

# --- 3. PROSES UTAMA (DARI SKRIP PERTAMA) ---
def process_traffic_data_regex(csv_filepath):
    all_extracted_data = []
    try:
        with open(csv_filepath, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_from_csv = row.get('date', '').strip()
                text_from_csv = row.get('text', '').strip()
                if not date_from_csv or not text_from_csv:
                    continue

                time_match = re.search(r'^(\d{2}[.:]\d{2})', text_from_csv)
                if not time_match:
                    continue

                time = time_match.group(1).replace('.', ':') + ":00"
                date = date_from_csv
                cleaned_text = re.sub(r'^\d{2}[.:]\d{2}\s*', '', text_from_csv).lower()

                status = find_keywords_regex(cleaned_text, STATUS_KEYWORDS_REGEX)
                obstacle = find_keywords_regex(cleaned_text, OBSTACLE_KEYWORDS_REGEX)
                weather = find_keywords_regex(cleaned_text, WEATHER_KEYWORDS_REGEX)
                locations_found = ner_locations_regex(cleaned_text, ALL_LOC_KEYWORDS_REGEX)
                from_to_pairs = determine_from_to_regex(cleaned_text, locations_found)
                
                if not from_to_pairs:
                    continue

                is_bidirectional = any(keyword in cleaned_text for keyword in BIDIRECTIONAL_KEYWORDS_REGEX)

                for from_loc, to_loc in from_to_pairs:
                    if not all([time, date, from_loc, to_loc, status]):
                        continue

                    data_entry = {
                        "time": time,
                        "date": date,
                        "from": from_loc.title(),
                        "to": to_loc.title(),
                        "status": status.title(),
                        "obstacle": obstacle.title() if obstacle else None,
                        "weather": weather.title() if weather else None
                    }
                    all_extracted_data.append(data_entry)

                    if is_bidirectional:
                        reversed_entry = data_entry.copy()
                        reversed_entry["from"] = to_loc.title()
                        reversed_entry["to"] = from_loc.title()
                        all_extracted_data.append(reversed_entry)
        return all_extracted_data
    except FileNotFoundError:
        return None # Akan ditangani di endpoint
    except Exception as e:
        print(f"Error processing with regex method: {e}")
        return []


# ==============================================================================
# LOGIC FOR /inner ENDPOINT (Token-Labeling Based Extraction)
# ==============================================================================
def custom_tokenizer(text):
    if not isinstance(text, str): return []
    urls = re.findall(r'https://t.co/\S+', text)
    text_no_urls = re.sub(r'https://t.co/\S+', '', text)
    tokens = [token for token in re.split(r'([,.()])?\s+', text_no_urls) if token]
    return tokens

def clean_location(loc_str):
    if not loc_str: return None
    loc_str = re.sub(r'^(di|dari|ke|menuju)\s+', '', loc_str.strip(), flags=re.IGNORECASE)
    loc_str = loc_str.strip(' ,.()')
    return loc_str if 'Jl.' in loc_str else loc_str.title()

TIME_PATTERN = re.compile(r'^\d{2}\.\d{2}$')
LOC_STARTERS = {'di', 'dari', 'depan', 'kawasan', 'on', 'exit'}
LOC_KEYWORDS = {
    'arteri', 'bundaran', 'csw', 'exit', 'gbk', 'gerbang', 'graha', 'gt', 'interchange',
    'jakbar', 'jakpus', 'jaksel', 'jaktim', 'jakut', 'jembatan', 'jl', 'jlnt', 'junction',
    'km', 'kolong', 'lampu', 'light', 'merah', 'monas', 'mrt', 'off', 'pasar', 'pgc',
    'pintu', 'pospol', 'ramp', 'ruas', 'semanggi', 'simpang', 'susun', 'terminal', 'tl',
    'tmii', 'tugu', 'tol', 'traffic', 'underpass', 'wisata'
}
STATUS_KEYWORDS = {'cukup', 'cenderung', 'lancar', 'mengalir', 'normal', 'padat', 'ramai'}
DIRECTION_KEYWORD = {'arah', 'mengarah', 'menuju'}
BIDIRECTIONAL_KEYWORDS = {'maupun', 'sebaliknya', 'dan'}
OBSTACLE_CAUSE_KEYWORDS = {'karena', 'imbas', 'dikarenakan'}
WEATHER = {'hujan','berawan','gerimis','cerah'}

def label_tokens(text):
    tokens = custom_tokenizer(text)
    labels = []
    is_location, is_status = False, False

    for i, tok in enumerate(tokens):
        lower_tok = tok.lower()
        if i == 0: is_location = is_status = False

        if tok.startswith('https://t.co/'):
            labels.append("O")
            is_location = is_status = False
        elif TIME_PATTERN.match(tok):
            labels.append("B-TIME")
            is_location = is_status = False
        elif lower_tok in BIDIRECTIONAL_KEYWORDS:
            labels.append("B-BIDIR")
            is_location = False
        elif lower_tok in DIRECTION_KEYWORD:
            labels.append("B-DIR")
            is_location = False
        elif lower_tok in OBSTACLE_CAUSE_KEYWORDS:
            labels.append("B-OBSTACLE-CAUSE")
            is_location = is_status = False
        elif lower_tok in LOC_STARTERS or any(kw in lower_tok for kw in LOC_KEYWORDS):
            labels.append("B-LOC" if not is_location else "I-LOC")
            is_location = True; is_status = False
        elif lower_tok in STATUS_KEYWORDS:
            labels.append("B-STATUS" if not is_status else "I-STATUS")
            is_status = True; is_location = False
        elif is_location:
            if lower_tok in ['terpantau', 'sedangkan', 'diimbau', 'dan', 'yang']:
                labels.append("O"); is_location = False
            else:
                labels.append("I-LOC")
        elif lower_tok in WEATHER:
            labels.append("B-WEATHER")
            is_location = is_status = False
        else:
            labels.append("O")
            is_location = is_status = False
    return tokens, labels

def extract_from_tagged(tokens, labels, date_from_csv, base_from=None):
    time, status, obstacle, weather = None, None, None, None
    locations, bidir_flags = [], []

    i = 0
    while i < len(tokens):
        tag = labels[i]
        if tag.startswith("B-"):
            chunk_tokens = []; chunk_type = tag[2:]
            j = i
            while j < len(tokens) and (labels[j] == f"B-{chunk_type}" or labels[j] == f"I-{chunk_type}"):
                chunk_tokens.append(tokens[j]); j += 1
            full_chunk = " ".join(chunk_tokens)
            if chunk_type == "TIME": time = full_chunk.replace('.', ':') + ":00"
            elif chunk_type == "STATUS": status = full_chunk
            elif chunk_type == "LOC": locations.append(clean_location(full_chunk))
            elif chunk_type == "BIDIR": bidir_flags.append(tokens[i].lower())
            elif chunk_type == "OBSTACLE-CAUSE":
                obs_tokens = [tokens[k] for k in range(j, len(tokens)) if tokens[k].lower() not in ['diimbau', 'agar']]
                if obs_tokens: obstacle = ' '.join(obs_tokens).strip(" .")
            elif chunk_type == "WEATHER": weather = full_chunk
            i = j
        else: i += 1

    results = []
    if base_from and not locations: return []
    if base_from and not any(re.search(r'di |dari ', loc, re.I) for loc in locations):
        locations.insert(0, base_from)

    if not time or not status or not locations: return []

    base_record = {'time': time, 'date': date_from_csv, 'from': None, 'to': None, 'status': status, 'obstacle': obstacle, 'weather': weather}

    if len(locations) == 1:
        results.append({**base_record, 'from': locations[0], 'to': None})
    elif 'maupun' in bidir_flags and len(locations) > 1:
        origin = locations[0]
        for dest in locations[1:]:
            results.append({**base_record, 'from': origin, 'to': dest})
    elif 'sebaliknya' in bidir_flags and len(locations) > 1:
        loc1, loc2 = locations[0], locations[1]
        results.append({**base_record, 'from': loc1, 'to': loc2})
        results.append({**base_record, 'from': loc2, 'to': loc1})
    elif len(locations) >= 2:
        results.append({**base_record, 'from': locations[0], 'to': locations[1]})

    return results

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "server is running", "endpoints": ["/inner", "/regex"]})

@app.route('/regex', methods=['GET'])
def get_regex_traffic_data():
    """Endpoint to get traffic data using the dictionary and rule-based method."""
    csv_file = 'lalu_lintas.csv'
    extracted_data = process_traffic_data_regex(csv_file)

    if extracted_data is None:
        return jsonify({"error": f"File '{csv_file}' tidak ditemukan."}), 404
    
    # Menghapus duplikat entri sebelum mengirim respons
    if extracted_data:
        unique_data = [dict(t) for t in {tuple(d.items()) for d in extracted_data}]
        return jsonify(unique_data)
    else:
        return jsonify([])


@app.route('/inner', methods=['GET'])
def get_all_traffic_data():
    """Endpoint to get traffic data using the token-labeling method."""
    try:
        df_input = pd.read_csv('lalu_lintas.csv')
    except FileNotFoundError:
        return jsonify({"error": "File 'lalu_lintas.csv' tidak ditemukan."}), 404
    except Exception as e:
        return jsonify({"error": f"Gagal membaca file CSV: {e}"}), 500

    all_extracted_data = []
    base_origin_for_sedangkan = None

    for index, row in df_input.iterrows():
        if not isinstance(row['text'], str): continue

        parts = re.split(r'\s+sedangkan\s+', row['text'], flags=re.IGNORECASE)

        for i, part in enumerate(parts):
            tokens, labels = label_tokens(part)
            contextual_origin = base_origin_for_sedangkan if i > 0 else None
            extracted_records = extract_from_tagged(tokens, labels, row['date'], contextual_origin)

            if extracted_records:
                all_extracted_data.extend(extracted_records)
                if i == 0 and extracted_records[0]['from']:
                    base_origin_for_sedangkan = extracted_records[0]['from']
        
        base_origin_for_sedangkan = None

    MANDATORY_KEYS = ['time', 'date', 'from', 'to', 'status']
    final_data = [
        rec for rec in all_extracted_data if all(rec.get(key) for key in MANDATORY_KEYS)
    ]

    return jsonify(final_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)