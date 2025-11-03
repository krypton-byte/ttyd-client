<div align="center">

# 🖥️ TTYD Client
<img src="assets/icon.png" alt="TTYD Client Icon" width="120" height="120" />

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey.svg)](https://github.com/krypton-byte/ttyd-client)

**A cross-platform terminal client for TTYD WebSocket connections**

[English](#english) | [Indonesia](#indonesia) | [中文](#中文)

</div>

---

## English

### 📖 Overview

TTYD Client is a powerful, cross-platform terminal client that enables seamless connections to [ttyd](https://github.com/tsl0922/ttyd) servers via WebSocket. It provides a native terminal experience with full support for escape sequences, special keys, and terminal multiplexers like tmux/byobu.

### ✨ Features

- 🌍 **Cross-Platform Support**: Works seamlessly on Linux, macOS, and Windows
- 🔐 **Secure Authentication**: Supports basic authentication with token-based access
- ⌨️ **Full Keyboard Support**: Captures all escape sequences including arrow keys, function keys, and control characters
- 🎨 **Terminal Query Filtering**: Automatically filters device control sequences to prevent unwanted responses
- 📺 **Terminal Multiplexer Compatible**: Works perfectly with tmux, screen, and byobu
- 🔄 **Auto-Resize**: Automatically adjusts terminal size on window resize (Unix/Linux/macOS)
- 🚀 **High Performance**: Efficient input/output handling with minimal latency

### 📦 Installation

#### From Source

```bash
git clone https://github.com/krypton-byte/ttyd-client.git
cd ttyd-client
pip install -r requirements.txt
```

#### Requirements

- Python 3.7+
- websocket-client
- requests

### 🚀 Usage

#### Basic Connection

```bash
ttyd-client http://localhost:7681
```

#### With Authentication

```bash
ttyd-client https://example.com:7681 --credential "username:password"
```

#### Disable SSL Verification

```bash
ttyd-client https://example.com:7681 --no-verify
```

#### Execute Command on Connect

```bash
ttyd-client http://localhost:7681 --cmd "ls -la"
```

#### Pass Arguments to Remote Shell

```bash
ttyd-client http://localhost:7681 --args bash --login
```

### 🛠️ Command Line Options

| Option | Description |
|--------|-------------|
| `url` | TTYD server URL (required) |
| `--credential` | Authentication in format "username:password" |
| `--no-verify` | Disable SSL certificate verification |
| `--cmd` | Command to execute on connection |
| `--args` | Arguments to pass to remote shell |

### 🏗️ Architecture

```
ttyd_cli/
├── __init__.py          # Package initialization
├── __main__.py          # CLI entry point
├── auth.py              # Authentication handler
├── client.py            # Main WebSocket client
├── exceptions.py        # Custom exceptions
├── utils.py             # Utility functions
└── platforms/           # Platform-specific implementations
    ├── __init__.py
    ├── base.py          # Base input handler
    ├── unix.py          # Unix/Linux/macOS handler
    └── windows.py       # Windows handler
```

### 🔧 Advanced Features

#### Terminal Query Filtering

The client automatically filters terminal device control sequences such as:
- Color queries (OSC 10, 11, 12, 4)
- Device attribute queries (CSI > c, CSI ? c)
- Cursor position reports
- DCS/APC sequences

This prevents terminal responses from being interpreted as keyboard input.

#### Platform-Specific Input Handling

- **Unix/Linux/macOS**: Uses `termios` and `tty` for raw mode terminal control
- **Windows**: Uses `msvcrt` with special key mapping to ANSI sequences

### 📝 Examples

#### Connect to Local TTYD Server

```bash
# Start ttyd server
ttyd -p 7681 bash

# Connect with client
ttyd-client --url http://localhost:7681
```

#### Secure Connection with SSL

```bash
ttyd-client --url https://secure-server.com:443 --credential "admin:secret"
```

#### Use with Byobu/Tmux

```bash
ttyd-client --url http://localhost:7681 --cmd byobu
```

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Indonesia

### 📖 Gambaran Umum

TTYD Client adalah klien terminal lintas platform yang kuat, memungkinkan koneksi yang mulus ke server [ttyd](https://github.com/tsl0922/ttyd) melalui WebSocket. Ini menyediakan pengalaman terminal native dengan dukungan penuh untuk escape sequences, tombol khusus, dan terminal multiplexer seperti tmux/byobu.

### ✨ Fitur

- 🌍 **Dukungan Lintas Platform**: Berfungsi dengan baik di Linux, macOS, dan Windows
- 🔐 **Autentikasi Aman**: Mendukung autentikasi dasar dengan akses berbasis token
- ⌨️ **Dukungan Keyboard Penuh**: Menangkap semua escape sequences termasuk tombol panah, function keys, dan karakter kontrol
- 🎨 **Filtering Query Terminal**: Secara otomatis memfilter device control sequences untuk mencegah respons yang tidak diinginkan
- 📺 **Kompatibel dengan Terminal Multiplexer**: Bekerja sempurna dengan tmux, screen, dan byobu
- 🔄 **Auto-Resize**: Secara otomatis menyesuaikan ukuran terminal saat window di-resize (Unix/Linux/macOS)
- 🚀 **Performa Tinggi**: Penanganan input/output yang efisien dengan latensi minimal

### 📦 Instalasi

#### Dari Source

```bash
git clone https://github.com/krypton-byte/ttyd-client.git
cd ttyd-client
pip install -r requirements.txt
```

#### Persyaratan

- Python 3.7+
- websocket-client
- requests

### 🚀 Penggunaan

#### Koneksi Dasar

```bash
ttyd-client --url http://localhost:7681
```

#### Dengan Autentikasi

```bash
ttyd-client --url https://example.com:7681 --credential "username:password"
```

#### Nonaktifkan Verifikasi SSL

```bash
ttyd-client --url https://example.com:7681 --no-verify
```

#### Jalankan Perintah Saat Koneksi

```bash
ttyd-client --url http://localhost:7681 --cmd "ls -la"
```

#### Kirim Argumen ke Remote Shell

```bash
ttyd-client --url http://localhost:7681 --args bash --login
```

### 🛠️ Opsi Command Line

| Opsi | Deskripsi |
|------|-----------|
| `url` | URL server TTYD (wajib) |
| `--credential` | Autentikasi dengan format "username:password" |
| `--no-verify` | Nonaktifkan verifikasi sertifikat SSL |
| `--cmd` | Perintah yang dijalankan saat koneksi |
| `--args` | Argumen untuk dikirim ke remote shell |

### 🏗️ Arsitektur

```
ttyd_cli/
├── __init__.py          # Inisialisasi package
├── __main__.py          # Entry point CLI
├── auth.py              # Handler autentikasi
├── client.py            # WebSocket client utama
├── exceptions.py        # Exception kustom
├── utils.py             # Fungsi utilitas
└── platforms/           # Implementasi spesifik platform
    ├── __init__.py
    ├── base.py          # Base input handler
    ├── unix.py          # Handler Unix/Linux/macOS
    └── windows.py       # Handler Windows
```

### 🔧 Fitur Lanjutan

#### Filtering Query Terminal

Klien secara otomatis memfilter device control sequences terminal seperti:
- Query warna (OSC 10, 11, 12, 4)
- Query atribut perangkat (CSI > c, CSI ? c)
- Laporan posisi kursor
- Sequences DCS/APC

Ini mencegah respons terminal ditafsirkan sebagai input keyboard.

#### Penanganan Input Spesifik Platform

- **Unix/Linux/macOS**: Menggunakan `termios` dan `tty` untuk kontrol terminal mode raw
- **Windows**: Menggunakan `msvcrt` dengan pemetaan tombol khusus ke sequences ANSI

### 📝 Contoh

#### Koneksi ke Server TTYD Lokal

```bash
# Jalankan ttyd server
ttyd -p 7681 bash

# Koneksi dengan client
ttyd-client --url http://localhost:7681
```

#### Koneksi Aman dengan SSL

```bash
ttyd-client --url https://secure-server.com:443 --credential "admin:secret"
```

#### Gunakan dengan Byobu/Tmux

```bash
ttyd-client --url http://localhost:7681 --cmd byobu
```

### 🤝 Kontribusi

Kontribusi sangat diterima! Silakan kirimkan Pull Request.

### 📄 Lisensi

Proyek ini dilisensikan di bawah MIT License - lihat file [LICENSE](LICENSE) untuk detail.

---

## 中文

### 📖 概述

TTYD Client 是一个强大的跨平台终端客户端，可通过 WebSocket 无缝连接到 [ttyd](https://github.com/tsl0922/ttyd) 服务器。它提供原生终端体验，完全支持转义序列、特殊键和终端复用器（如 tmux/byobu）。

### ✨ 特性

- 🌍 **跨平台支持**：在 Linux、macOS 和 Windows 上无缝运行
- 🔐 **安全认证**：支持基于令牌访问的基本身份验证
- ⌨️ **完整键盘支持**：捕获所有转义序列，包括方向键、功能键和控制字符
- 🎨 **终端查询过滤**：自动过滤设备控制序列以防止不需要的响应
- 📺 **终端复用器兼容**：与 tmux、screen 和 byobu 完美配合
- 🔄 **自动调整大小**：窗口调整大小时自动调整终端大小（Unix/Linux/macOS）
- 🚀 **高性能**：高效的输入/输出处理，延迟最小

### 📦 安装

#### 从源码安装

```bash
git clone https://github.com/krypton-byte/ttyd-client.git
cd ttyd-client
pip install -r requirements.txt
```

#### 要求

- Python 3.7+
- websocket-client
- requests

### 🚀 使用方法

#### 基本连接

```bash
ttyd-client --url http://localhost:7681
```

#### 使用身份验证

```bash
ttyd-client --url https://example.com:7681 --credential "username:password"
```

#### 禁用 SSL 验证

```bash
ttyd-client --url https://example.com:7681 --no-verify
```

#### 连接时执行命令

```bash
ttyd-client --url http://localhost:7681 --cmd "ls -la"
```

#### 向远程 Shell 传递参数

```bash
ttyd-client --url http://localhost:7681 --args bash --login
```

### 🛠️ 命令行选项

| 选项 | 描述 |
|------|------|
| `url` | TTYD 服务器 URL（必需）|
| `--credential` | 格式为 "username:password" 的身份验证 |
| `--no-verify` | 禁用 SSL 证书验证 |
| `--cmd` | 连接时执行的命令 |
| `--args` | 传递给远程 shell 的参数 |

### 🏗️ 架构

```
ttyd_cli/
├── __init__.py          # 包初始化
├── __main__.py          # CLI 入口点
├── auth.py              # 身份验证处理器
├── client.py            # 主 WebSocket 客户端
├── exceptions.py        # 自定义异常
├── utils.py             # 实用函数
└── platforms/           # 平台特定实现
    ├── __init__.py
    ├── base.py          # 基础输入处理器
    ├── unix.py          # Unix/Linux/macOS 处理器
    └── windows.py       # Windows 处理器
```

### 🔧 高级功能

#### 终端查询过滤

客户端自动过滤终端设备控制序列，例如：
- 颜色查询（OSC 10、11、12、4）
- 设备属性查询（CSI > c、CSI ? c）
- 光标位置报告
- DCS/APC 序列

这可以防止终端响应被解释为键盘输入。

#### 平台特定输入处理

- **Unix/Linux/macOS**：使用 `termios` 和 `tty` 进行原始模式终端控制
- **Windows**：使用 `msvcrt`，将特殊键映射到 ANSI 序列

### 📝 示例

#### 连接到本地 TTYD 服务器

```bash
# 启动 ttyd 服务器
ttyd -p 7681 bash

# 使用客户端连接
ttyd-client --url http://localhost:7681
```

#### 使用 SSL 的安全连接

```bash
ttyd-client --url https://secure-server.com:443 --credential "admin:secret"
```

#### 与 Byobu/Tmux 一起使用

```bash
ttyd-client --url http://localhost:7681 --cmd byobu
```

### 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

### 📄 许可证

该项目根据 MIT 许可证授权 - 有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

---

<div align="center">

### 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=krypton-byte/ttyd-client&type=Date)](https://star-history.com/#krypton-byte/ttyd-client&Date)

**Made with ❤️ by [krypton-byte](https://github.com/krypton-byte)**

</div>
