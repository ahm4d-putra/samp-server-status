# 🎮 SA-MP Server Status Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.3+-blue.svg)](https://discordpy.readthedocs.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Discord bot untuk mengecek status server **San Andreas Multiplayer (SA-MP)** secara real-time menggunakan slash commands.

![Preview](https://i.imgur.com/c3QH7Jj.png)

---

## ✨ Fitur

- 🔍 **`/ip`** — Cek status server (hostname, players, max players, gamemode, map)
- 👥 **`/players`** — Lihat daftar player online dengan score
- ⚡ **Real-time Query** — Direct query ke server SA-MP via UDP
- 🎨 **Discord Embed UI** — Tampilan rapi dan informatif
- 🔒 **Error Handling** — Pesan error jelas saat server offline

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/username/samp-server-status.git
cd samp-server-status
---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/username/samp-server-status.git
cd samp-server-status
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Konfigurasi Token

```
cp config.py.example config.py
# Edit config.py dengan token bot Discord kamu
```

### 4. Jalankan Bot

```
python bot.py
```

---

## 📋 Prerequisites

- Python 3.8 atau lebih baru
- Discord Bot Token ([Buat di sini](https://discord.com/developers/applications))
- Server SA-MP yang mendukung query (bukan passworded atau query-disabled)

---

## 🤖 Setup Discord Bot

1. Buka [Discord Developer Portal](https://discord.com/developers/applications)
2. Klik **"New Application"** → Beri nama → **Create**
3. Pergi ke **Bot** → **Add Bot** → **Yes, do it!**
4. Copy **Token** (simpan di `config.py`)
5. Enable **MESSAGE CONTENT INTENT** (Privileged Gateway Intents)
6. Pergi ke **OAuth2** → **URL Generator**
   - **SCOPES**: `bot`, `applications.commands`
   - **BOT PERMISSIONS**: `Send Messages`, `Embed Links`, `Use Slash Commands`
7. Copy URL dan invite ke server Discord kamu

---

## 📝 Commands

| Command | Parameter | Deskripsi |
|---------|-----------|-----------|
| `/ip` | `server_ip:port` | Cek status server SA-MP |
| `/players` | `server_ip:port` | Lihat daftar player online |
| `/ping` | — | Cek latency bot |

### Contoh Penggunaan

```
/ip 51.79.168.190:7777
```

**Output:**
- 🎮 Server Name
- 🌐 IP Address
- 👥 Players (online/max)
- 📊 Game Mode
- 🗺️ Map
- 🔐 Password Status

```
/players 51.79.168.190:7777
```

**Output:**
- List player dengan score (sorted by highest)
- Total player online
- Server hostname

---

## 📁 Struktur Project

```
samp-server-status/
├── bot.py              # Main bot file
├── config.py           # Token dan konfigurasi (ignored)
├── config.py.example   # Template konfigurasi
├── requirements.txt    # Dependencies
├── .gitignore         # Git ignore rules
└── README.md          # Dokumentasi ini
```

---

## ⚠️ Troubleshooting

### Slash command tidak muncul

- Tunggu 1-60 menit untuk global sync
- Atau gunakan guild sync (edit `MY_GUILD_ID` di `bot.py`)
- Pastikan bot di-invite dengan scope `applications.commands`

### Server tidak terdeteksi

- Cek format IP: `ip:port` (contoh: `127.0.0.1:7777`)
- Pastikan server online dan query enabled
- Beberapa server memblokir query dari luar

### `/players` error tapi `/ip` jalan

- Server tersebut disable query player detail
- Ini settingan server owner, bukan bug bot

---

## 🛠️ Tech Stack

- [Python](https://python.org) — Core language
- [discord.py](https://discordpy.readthedocs.io) — Discord API wrapper
- [SA-MP Query Protocol](https://wiki.sa-mp.com/wiki/Query) — UDP server query

---

## 🤝 Contributing

Pull request welcome! Untuk major changes, please open issue dulu.

1. Fork repository
2. Buat branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push ke branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

[MIT](LICENSE) © 2024

---

## 🙏 Credits

- [SA-MP](https://sa-mp.com) — San Andreas Multiplayer
- [discord.py](https://github.com/Rapptz/discord.py) — Awesome Discord library

---

> ⭐ Star repo ini kalau bermanfaat!
```


