"""
BHARAT ALPHA: 1-Click Dashboard Launcher
Checks if the server is running, launches the web interface, and opens your browser.
"""
import socket
import webbrowser
import time
import sys
from pathlib import Path

# Fix Windows console Unicode output
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

PORT = 8000
URL = f"http://127.0.0.1:{PORT}"

def get_lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def is_port_in_use(port: int) -> bool:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.8)
            return s.connect_ex(("127.0.0.1", port)) == 0
    except Exception:
        return False

def main():
    lan_ip = get_lan_ip()
    lan_url = f"http://{lan_ip}:{PORT}"

    print("\n=======================================================")
    print(" 🚀 BHARAT ALPHA: AI Market Research & Opportunity Engine")
    print("=======================================================")
    print(f"  • Local PC:     {URL}")
    print(f"  • LAN / Wi-Fi:  {lan_url}  (Mobile / Other PC)")
    print("=======================================================\n")

    if is_port_in_use(PORT):
        print(f"[OK] Dashboard server is already active!")
        print(f"[OK] Opening browser...")
        webbrowser.open(URL)
        time.sleep(1.5)
        return

    print(f"[1/2] Opening browser at {URL}...")
    webbrowser.open(URL)

    print(f"[2/2] Starting server on 0.0.0.0:{PORT} (Accessible on LAN)...")
    print(f"      Access from phone/tablet: {lan_url}")
    print("      (Keep this window open while using the dashboard)\n")

    import uvicorn
    from web_app import app
    uvicorn.run(app, host="0.0.0.0", port=PORT, log_level="info")

if __name__ == "__main__":
    main()

