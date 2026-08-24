import requests
import base64
from pathlib import Path

# === НАСТРОЙКИ ===
SOURCES_PC = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_SS+All_RUS.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_SS_WEAK_DPI_RUS.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-SNI-RU-all.txt",
]

SOURCES_MOBILE = [
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-all.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-checked.txt",
    "https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-SNI-RU-all.txt",
]

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)
# === КОНЕЦ НАСТРОЕК ===

PROTOCOLS = ("vless://", "ss://", "vmess://", "trojan://", "hysteria2://")

def fetch_lines(url):
    try:
        print(f"Загружаю {url}...")
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        lines = []
        for line in r.text.splitlines():
            line = line.strip()
            if line and not line.startswith("#") and line.startswith(PROTOCOLS):
                lines.append(line)
        print(f"  Найдено {len(lines)} ссылок")
        return lines
    except Exception as e:
        print(f"  Ошибка: {e}")
        return []

def deduplicate(lines):
    seen = set()
    result = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            result.append(line)
    return result

def make_base64(links):
    content = "\n".join(links)
    return base64.b64encode(content.encode()).decode()

def main():
    # PC
    print("=== Сборка PC подписки ===")
    pc_links = []
    for url in SOURCES_PC:
        pc_links.extend(fetch_lines(url))
    pc_links = deduplicate(pc_links)
    print(f"Всего PC уникальных ссылок: {len(pc_links)}")
    pc_b64 = make_base64(pc_links)
    (OUTPUT_DIR / "pc.txt").write_text(pc_b64)

    # Mobile
    print("\n=== Сборка Mobile подписки ===")
    mobile_links = []
    for url in SOURCES_MOBILE:
        mobile_links.extend(fetch_lines(url))
    mobile_links = deduplicate(mobile_links)
    print(f"Всего Mobile уникальных ссылок: {len(mobile_links)}")
    mobile_b64 = make_base64(mobile_links)
    (OUTPUT_DIR / "mobile.txt").write_text(mobile_b64)

    print("\nГотово! Файлы output/pc.txt и output/mobile.txt обновлены.")

if __name__ == "__main__":
    main()
