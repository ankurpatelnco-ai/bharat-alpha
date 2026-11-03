"""
BHARAT ALPHA: 1-Click Worldwide Public Live Launcher (Cloudflare Tunnel)
Connects your local dashboard securely to Cloudflare's global edge network.
Generates a 100% Free, secure HTTPS link accessible worldwide on any phone, tablet, or PC,
protected by the Bharat Alpha Login Terminal.
"""
import sys
import re
import time
import socket
import subprocess
import webbrowser
from pathlib import Path

# UTF-8 Console output on Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
BIN_DIR = BASE_DIR / "bin"
CLOUDFLARED_EXE = BIN_DIR / "cloudflared.exe"
PORT = 8000

def is_port_in_use(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.8)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False

def copy_to_clipboard(text: str):
    try:
        process = subprocess.Popen('clip', stdin=subprocess.PIPE, shell=True)
        process.communicate(text.encode('utf-8'))
    except Exception:
        pass

def main():
    print("\n" + "=" * 76)
    print(" 🚀 BHARAT ALPHA: 1-CLICK WORLDWIDE LIVE BROADCASTER")
    print("=" * 76)
    print(" Starting secure worldwide tunnel to make your dashboard accessible")
    print(" to everyone on the internet after logging in...\n")

    # 1. Ensure local server is active
    server_process = None
    if not is_port_in_use(PORT):
        print(f"[*] Starting background research server on port {PORT}...")
        python_exe = sys.executable
        server_process = subprocess.Popen(
            [python_exe, "-m", "uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", str(PORT)],
            cwd=str(BASE_DIR),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2.5)

    if not CLOUDFLARED_EXE.exists():
        print(f"[!] cloudflared.exe not found at {CLOUDFLARED_EXE}")
        print("    Please run: .venv\\Scripts\\python.exe -c \"import urllib.request; urllib.request.urlretrieve('https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe', 'bin/cloudflared.exe')\"")
        return

    # 2. Launch Cloudflare Tunnel
    print("[*] Connecting to Cloudflare global network edge...")
    cf_proc = subprocess.Popen(
        [str(CLOUDFLARED_EXE), "tunnel", "--url", f"http://127.0.0.1:{PORT}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

    public_url = None
    start_time = time.time()

    # Read output to capture public URL
    while time.time() - start_time < 30:
        line = cf_proc.stderr.readline()
        if not line:
            time.sleep(0.1)
            continue
        match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
        if match:
            public_url = match.group(0)
            break

    if not public_url:
        print("[!] Could not retrieve public tunnel URL. Check your internet connection.")
        cf_proc.terminate()
        return

    # 3. Display glowing info card
    copy_to_clipboard(public_url)
    
    print("\n" + "╔" + "═" * 74 + "╗")
    print("║  🌍 BHARAT ALPHA IS NOW LIVE WORLDWIDE ON THE PUBLIC INTERNET!           ║")
    print("╠" + "═" * 74 + "╣")
    print(f"║  👉 PUBLIC LINK:  {public_url:<54} ║")
    print("║  (Copied to your clipboard automatically!)                              ║")
    print("╠" + "═" * 74 + "╣")
    print("║  🔒 ACCESS PROTECTION (Login Required to Enter):                         ║")
    print("║     • Master Admin:  admin  /  admin123                                  ║")
    print("║     • New Visitors:  Can click 'Create Account' to register their own    ║")
    print("║                      personal username & password directly on the site.  ║")
    print("╠" + "═" * 74 + "╣")
    print("║  📱 WORKS ON: iPhones, Android phones, iPads, MacBooks & any computer!   ║")
    print("║  ⚠️  NOTE: Keep this window open while you want the live link active.    ║")
    print("╚" + "═" * 74 + "╝\n")

    # Open browser to public URL
    print("[*] Opening your live public terminal in Chrome/browser...")
    webbrowser.open(public_url)

    try:
        # Keep process alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[*] Stopping Cloudflare Tunnel and shutting down public live link...")
        cf_proc.terminate()
        if server_process:
            server_process.terminate()
        print("[OK] Public link disconnected successfully.")

if __name__ == "__main__":
    main()

