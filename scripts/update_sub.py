import requests
import base64
import socket
import re
from urllib.parse import urlparse, unquote
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

SOURCES = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-SNI-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS_mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_VLESS_RUS.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_SS_WEAK_DPI_RUS.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/refs/heads/main/BLACK_SS%2BAll_RUS.txt",
    "https://raw.githubusercontent.com/ninjastrikers/Nexus-nodes/main/configs/all.txt",
    "https://raw.githubusercontent.com/barry-far/V2ray-Configs/main/All_Configs_Sub.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/mohammadaz2/v2rayConfigsForYou/main/configs.txt",
    "https://raw.githubusercontent.com/miladtahanian/Config-Collector/main/mixed_iran.txt",
    "https://raw.githubusercontent.com/r3zarahimi/tg-v2ray-configs-every2h/main/Config_jo.txt",
    "https://raw.githubusercontent.com/MahanKenway/Freedom-V2Ray/main/configs/mix_sub.txt",
    "https://raw.githubusercontent.com/wlunlocker/vpn-configs/main/whitelist_all.txt",
    "https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/refs/heads/main/configs/proxy_configs.txt"
]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

FLAG_REGEX = re.compile(r'[\U0001F1E6-\U0001F1FF]{2}')

UDP_PROTOCOLS = ('hysteria2://', 'hy2://', 'tuic://')

TCP_PROTOCOLS = ('vless://', 'vmess://', 'ss://', 'trojan://')

COUNTRY_MAP = {
    "россия": "Russia", "russia": "Russia", "рф": "Russia", "russian": "Russia",
    "украина": "Ukraine", "ukraine": "Ukraine", "ua": "Ukraine",
    "беларусь": "Belarus", "belarus": "Belarus", "by": "Belarus",
    "казахстан": "Kazakhstan", "kazakhstan": "Kazakhstan", "kz": "Kazakhstan",
    "узбекистан": "Uzbekistan", "uzbekistan": "Uzbekistan",
    "грузия": "Georgia", "georgia": "Georgia",
    "армения": "Armenia", "armenia": "Armenia",
    "азербайджан": "Azerbaijan", "azerbaijan": "Azerbaijan",
    "молдова": "Moldova", "moldova": "Moldova",
    "эстония": "Estonia", "estonia": "Estonia", "ee": "Estonia",
    "латвия": "Latvia", "latvia": "Latvia", "lv": "Latvia",
    "литва": "Lithuania", "lithuania": "Lithuania", "lt": "Lithuania",
    "германия": "Germany", "germany": "Germany", "de": "Germany", "фрг": "Germany",
    "финляндия": "Finland", "finland": "Finland", "fi": "Finland",
    "нидерланды": "Netherlands", "netherlands": "Netherlands", "голландия": "Netherlands", "nl": "Netherlands",
    "франция": "France", "france": "France", "fr": "France",
    "великобритания": "UK", "uk": "UK", "united kingdom": "UK", "англия": "UK", "gb": "UK",
    "швеция": "Sweden", "sweden": "Sweden", "se": "Sweden",
    "норвегия": "Norway", "norway": "Norway", "no": "Norway",
    "польша": "Poland", "poland": "Poland", "pl": "Poland",
    "италия": "Italy", "italy": "Italy", "it": "Italy",
    "испания": "Spain", "spain": "Spain", "es": "Spain",
    "португалия": "Portugal", "portugal": "Portugal", "pt": "Portugal",
    "швейцария": "Switzerland", "switzerland": "Switzerland", "ch": "Switzerland",
    "австрия": "Austria", "austria": "Austria", "at": "Austria",
    "бельгия": "Belgium", "belgium": "Belgium", "be": "Belgium",
    "дания": "Denmark", "denmark": "Denmark", "dk": "Denmark",
    "чехия": "Czechia", "czechia": "Czechia", "cz": "Czechia",
    "румыния": "Romania", "romania": "Romania", "ro": "Romania",
    "болгария": "Bulgaria", "bulgaria": "Bulgaria", "bg": "Bulgaria",
    "греция": "Greece", "greece": "Greece", "gr": "Greece",
    "венгрия": "Hungary", "hungary": "Hungary", "hu": "Hungary",
    "ирландия": "Ireland", "ireland": "Ireland", "ie": "Ireland",
    "исландия": "Iceland", "iceland": "Iceland", "is": "Iceland",
    "сербия": "Serbia", "serbia": "Serbia", "rs": "Serbia",
    "хорватия": "Croatia", "croatia": "Croatia", "hr": "Croatia",
    "словения": "Slovenia", "slovenia": "Slovenia", "si": "Slovenia",
    "словакия": "Slovakia", "slovakia": "Slovakia", "sk": "Slovakia",
    "албания": "Albania", "albania": "Albania", "al": "Albania",
    "кипр": "Cyprus", "cyprus": "Cyprus", "cy": "Cyprus",
    "мальта": "Malta", "malta": "Malta", "mt": "Malta",
    "люксембург": "Luxembourg", "luxembourg": "Luxembourg", "lu": "Luxembourg",
    "сша": "USA", "usa": "USA", "united states": "USA", "america": "USA", "us": "USA",
    "канада": "Canada", "canada": "Canada", "ca": "Canada",
    "бразилия": "Brazil", "brazil": "Brazil", "br": "Brazil",
    "мексика": "Mexico", "mexico": "Mexico", "mx": "Mexico",
    "аргентина": "Argentina", "argentina": "Argentina", "ar": "Argentina",
    "чили": "Chile", "chile": "Chile", "cl": "Chile",
    "колумбия": "Colombia", "colombia": "Colombia", "co": "Colombia",
    "перу": "Peru", "peru": "Peru", "pe": "Peru",
    "турция": "Turkey", "turkey": "Turkey", "tr": "Turkey",
    "япония": "Japan", "japan": "Japan", "jp": "Japan",
    "корея": "South Korea", "south korea": "South Korea", "korea": "South Korea", "kr": "South Korea",
    "китай": "China", "china": "China", "cn": "China",
    "индия": "India", "india": "India", "in": "India",
    "вьетнам": "Vietnam", "vietnam": "Vietnam", "vn": "Vietnam",
    "таиланд": "Thailand", "thailand": "Thailand", "th": "Thailand",
    "индонезия": "Indonesia", "indonesia": "Indonesia", "id": "Indonesia",
    "малайзия": "Malaysia", "malaysia": "Malaysia", "my": "Malaysia",
    "сингапур": "Singapore", "singapore": "Singapore", "sg": "Singapore",
    "филиппины": "Philippines", "philippines": "Philippines", "ph": "Philippines",
    "израиль": "Israel", "israel": "Israel", "il": "Israel",
    "оаэ": "UAE", "uae": "UAE", "emirates": "UAE", "ae": "UAE",
    "саудовская аравия": "Saudi Arabia", "saudi arabia": "Saudi Arabia", "sa": "Saudi Arabia",
    "египет": "Egypt", "egypt": "Egypt", "eg": "Egypt",
    "юар": "South Africa", "south africa": "South Africa", "za": "South Africa",
    "австралия": "Australia", "australia": "Australia", "au": "Australia",
    "новая зеландия": "New Zealand", "new zealand": "New Zealand", "nz": "New Zealand",
}

COUNTRY_FLAGS = {
    "Russia": "🇷🇺", "Ukraine": "🇺🇦", "Belarus": "🇧🇾", "Kazakhstan": "🇰🇿",
    "Uzbekistan": "🇺🇿", "Georgia": "🇬🇪", "Armenia": "🇦🇲", "Azerbaijan": "🇦🇿",
    "Moldova": "🇲🇩", "Estonia": "🇪🇪", "Latvia": "🇱🇻", "Lithuania": "🇱🇹",
    "Germany": "🇩🇪", "Finland": "🇫🇮", "Netherlands": "🇳🇱", "France": "🇫🇷",
    "UK": "🇬🇧", "Sweden": "🇸🇪", "Norway": "🇳🇴", "Poland": "🇵🇱",
    "Italy": "🇮🇹", "Spain": "🇪🇸", "Portugal": "🇵🇹", "Switzerland": "🇨🇭",
    "Austria": "🇦🇹", "Belgium": "🇧🇪", "Denmark": "🇩🇰", "Czechia": "🇨🇿",
    "Romania": "🇷🇴", "Bulgaria": "🇧🇬", "Greece": "🇬🇷", "Hungary": "🇭🇺",
    "Ireland": "🇮🇪", "Iceland": "🇮🇸", "Serbia": "🇷🇸", "Croatia": "🇭🇷",
    "Slovenia": "🇸🇮", "Slovakia": "🇸🇰", "Albania": "🇦🇱", "Cyprus": "🇨🇾",
    "Malta": "🇲🇹", "Luxembourg": "🇱🇺", "USA": "🇺🇸", "Canada": "🇨🇦",
    "Brazil": "🇧🇷", "Mexico": "🇲🇽", "Argentina": "🇦🇷", "Chile": "🇨🇱",
    "Colombia": "🇨🇴", "Peru": "🇵🇪", "Turkey": "🇹🇷", "Japan": "🇯🇵",
    "South Korea": "🇰🇷", "China": "🇨🇳", "India": "🇮🇳", "Vietnam": "🇻🇳",
    "Thailand": "🇹🇭", "Indonesia": "🇮🇩", "Malaysia": "🇲🇾", "Singapore": "🇸🇬",
    "Philippines": "🇵🇭", "Israel": "🇮🇱", "UAE": "🇦🇪", "Saudi Arabia": "🇸🇦",
    "Egypt": "🇪🇬", "South Africa": "🇿🇦", "Australia": "🇦🇺", "New Zealand": "🇳🇿"
}

def fetch_links(url):
    try:
        resp = requests.get(url, timeout=15)
        resp.raise_for_status()
        text = resp.text.strip()
        try:
            decoded = base64.b64decode(text).decode('utf-8', errors='ignore')
            if any(decoded.startswith(p) for p in ['vless://', 'vmess://', 'ss://', 'trojan://', 'hysteria2://', 'hy2://', 'tuic://']):
                return decoded
        except Exception:
            pass
        return text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def extract_uris(text):
    uris = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if any(line.startswith(p) for p in TCP_PROTOCOLS + UDP_PROTOCOLS):
            uris.append(line)
    return uris

def is_alive(uri):
    if uri.startswith(UDP_PROTOCOLS):
        return True
    try:
        parsed = urlparse(uri)
        host = parsed.hostname
        port = parsed.port
        if not host or not port:
            return False
        with socket.create_connection((host, int(port)), timeout=7.0):
            return True
    except Exception:
        return False

def get_display_name(uri):
    if '#' in uri:
        raw_name = unquote(uri.split('#', 1)[1]).strip()
        
        flag = ""
        flag_match = FLAG_REGEX.search(raw_name)
        if flag_match:
            flag = flag_match.group(0)
            raw_name_clean = FLAG_REGEX.sub('', raw_name).strip()
        else:
            raw_name_clean = raw_name
            
        name_lower = raw_name_clean.lower()
        
        for key, country_name in COUNTRY_MAP.items():
            if key in name_lower:
                correct_flag = COUNTRY_FLAGS.get(country_name, flag)
                return f"{correct_flag} {country_name}".strip()
                
        clean_name = re.sub(r'[^\w\s-]', '', raw_name_clean).strip()
        return f"{flag} {clean_name}".strip() if clean_name else "Server"
    return "Server"

def process_uris(uris, source_name):
    print(f"Checking {len(uris)} servers from {source_name}...")
    alive_uris = []
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        future_to_uri = {executor.submit(is_alive, uri): uri for uri in uris}
        for future in as_completed(future_to_uri):
            uri = future_to_uri[future]
            if future.result():
                alive_uris.append(uri)
                
    print(f"Found {len(alive_uris)} alive servers from {source_name}.")
    return alive_uris

def main():
    all_uris = []
    
    for url in SOURCES:
        source_name = url.split('/')[-1]
        text = fetch_links(url)
        if not text:
            continue
        uris = extract_uris(text)
        uris = list(set(uris))
        if not uris:
            continue
        alive = process_uris(uris, source_name)
        all_uris.extend(alive)
        
    all_uris = list(dict.fromkeys(all_uris))
    print(f"Total unique alive servers: {len(all_uris)}")
    
    all_uris.sort(key=get_display_name)
    
    renamed = []
    name_counters = {}
    
    for uri in all_uris:
        display_name = get_display_name(uri)
        name_counters[display_name] = name_counters.get(display_name, 0) + 1
        num = name_counters[display_name]
        
        new_name = f"{display_name} #{num}"
        
        if '#' in uri:
            base, _ = uri.rsplit('#', 1)
            renamed.append(f"{base}#{new_name}")
        else:
            renamed.append(f"{uri}#{new_name}")
    
    instruction = "vless://00000000-0000-0000-0000-000000000000@127.0.0.1:1#⚠️_IF_PING_DOES_NOT_SHOW,_JUST_CONNECT!"
    renamed.insert(0, instruction)
    
    headers = [
        "#profile-title: FUCK-RKN-VPN",
        "#profile-update-interval: 6"
    ]
    
    combined_text = "\n".join(headers + renamed)
    b64_encoded = base64.b64encode(combined_text.encode('utf-8')).decode('utf-8')
    
    output_file = OUTPUT_DIR / "FUCK-RKN-VPN.txt"
    output_file.write_text(b64_encoded)
    print(f"Successfully saved {len(renamed)-1} servers to {output_file}")

if __name__ == "__main__":
    main()
