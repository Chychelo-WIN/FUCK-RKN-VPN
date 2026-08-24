<!-- Language Switcher -->
<div align="center">
  <a href="README-ru.md"><img src="https://img.shields.io/badge/Русский-README--ru.md-blue?style=for-the-badge&logo=googletranslate&logoColor=white" alt="Russian"></a>
  <a href="README-en.md"><img src="https://img.shields.io/badge/English-README--en.md-red?style=for-the-badge&logo=googletranslate&logoColor=white" alt="English"></a>
</div>

<br>

<div align="center">
  <img src="https://i.imgur.com/OrVp5Rx.jpeg" alt="Star Sky" width="600"/>
  <h1>🌟 FUCK-RKN-VPN 🌟</h1>
  <p><strong>Bypass censorship together 🚀</strong></p>
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNTljeGk4d3lzZnU3Mm1peDBienFpbmEyb3JmaDB5N21tMW9oczIwdyZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/8p1WPEOeDWFCksfe18/giphy.gif" width="150" alt="NyaCat"/>
</div>

---

# <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2RkeXZzdDl1Y3g4dW1xcjFxc2xsMHVsZ2RiY243OHJodjd0cHQ1NSZlcD12MV9zdGlja2Vyc19zZWFyY2gmY3Q9cw/qXp82ZL3eZbbTUrLyy/giphy.gif" width="45"> Free VPN configs working in Russia

**FUCK‑RKN‑VPN** – my own subscription based on free servers from the repository [igareck/vpn‑configs‑for‑russia](https://github.com/igareck/vpn-configs-for-russia).  

All configs are public, auto‑updated, and automatically tested for usability.  
**Subscriptions are refreshed every hour** – you always have the latest list of working servers without junk.

---

## 📦 Subscriptions

### ⚫ Blacklist (standard internet)
| Version | File | RAW Link |
|---------|------|----------|
| **Mobile** (Top‑150, mix of protocols) | `BLACK_VLESS_RUS_mobile.txt` | [Download](https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS_mobile.txt) |
| **PC** (full VLESS) | `BLACK_VLESS_RUS.txt` | [Download](https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/BLACK_VLESS_RUS.txt) |

### ⚪ Whitelist (strict CIDR restrictions)
| Version | File | RAW Link |
|---------|------|----------|
| **Mobile** (Top‑150 CIDR) | `Vless-Reality-White-Lists-Rus-Mobile.txt` | [Download](https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/Vless-Reality-White-Lists-Rus-Mobile.txt) |
| **PC** (full CIDR list) | `WHITE-CIDR-RU-all.txt` | [Download](https://raw.githubusercontent.com/igareck/vpn-configs-for-russia/main/WHITE-CIDR-RU-all.txt) |

> All configs are taken from the original repository and are regularly tested.  
> Subscriptions update automatically **every hour** – just enable auto‑update in your client.

---

## 🔒 Important Security Note

A recent article on **Habr** revealed a critical vulnerability in mobile clients based on xray/sing‑box: an unauthenticated local SOCKS5 proxy can be exploited by Russian apps to leak your real IP.

**Happ client** – the developer removed the HandlerService on Android and added inbound authentication (username/password) on all platforms.  
**This makes Happ secure if you set a login and password in the settings.**

Recommended secure clients (with local proxy auth):
- ✅ **Karing**, **Throne**, **v2rayNG**, **v2rayTun**, **Happ** – safe (requires login/password setup).
- ❌ **Streisand**, **NekoBox**, **V2Box** – not yet updated, use with caution.

**Practical advice:** if you have Russian apps on your device (banks, government services, Yandex, etc.), use a separate Android profile or a dedicated device for better isolation.

---

## 🧩 Client Setup Instructions

General steps for all clients:
1. Copy the RAW link of the desired subscription (from the table above).
2. In your client, add a new subscription (usually "Add Profile" → "Subscription").
3. Paste the link, set a name, and set update interval to **1 hour**.
4. Refresh the subscription and run a "real delay" test (not TCP/ICMP Ping).
5. Pick the server with the lowest latency and connect.

### Quick Client Guides

#### 📱 Android
- **v2rayNG** – "+" → "Subscription" → paste URL → refresh → test latency → connect. Set local proxy login/password in settings.
- **NekoBox** – "+" → "Subscription" → paste URL → save → refresh → test latency → connect.
- **Hiddify** – "+" → "Add subscription" → paste URL → add → refresh → test latency → connect. Enable inbound auth in settings.
- **V2box** – "+" → "Subscription" → enter URL → save → refresh → test latency → connect.
- **Happ** – "+" → "Subscription" → paste URL → refresh → test latency → connect. Set inbound login/password in settings.

#### 🍎 iOS
- **Shadowrocket** – "+" → "Subscribe" → paste URL → Done → refresh → Test Latency → select server → enable VPN.
- **V2box** – similar via "Subscribe".
- **Happ** – similar to Android.

#### 💻 Windows / Linux / MacOS
- **v2rayN** – "Subscription Group" → "Subscription Group Settings" → add URL → refresh → test latency → select server → enable "TUN Mode". In routing, choose "RUv1‑All except RF".
- **Nekoray** – "Settings" → "Groups" → "New Group" → "Subscription" → paste URL → refresh → test latency → connect.
- **Hiddify (Desktop)** – "+" → "Add subscription" → paste URL → add → refresh → test latency → connect.

> Always use the "real delay" test to pick a truly working server.

---

## 📌 Useful Links

- **Original server repository:** [github.com/igareck/vpn-configs-for-russia](https://github.com/igareck/vpn-configs-for-russia)
- **Public DoH servers** (to encrypt DNS):
  - Cloudflare: `https://dns.cloudflare.com/dns-query`
  - Google: `https://dns.google/dns-query`
  - AdGuard: `https://dns.adguard-dns.com/dns-query`
  - Quad9: `https://dns.quad9.net/dns-query`
- **Privacy‑focused browsers:** [Librewolf](https://librewolf.net/), [Ungoogled Chromium](https://github.com/ungoogled-software), [Cromite](https://github.com/uazo/cromite)
- **Habr vulnerability article:** [link](https://habr.com/ru/articles/1020080/) (archive mirror available)

---

## ⚠️ Disclaimer

> *The author is not the owner or provider of the VPN configs. This is an independent informational review and test results. The material is intended solely for citizens of countries where such information is legal. Use VPN only for lawful purposes (e.g., privacy protection). Usage is at your own risk. The author does not encourage illegal use.*
