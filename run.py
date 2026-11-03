"""
BHARAT ALPHA: Master Launch Script.
Commands:
    python run.py                   # Run market scan & display morning report in terminal
    python run.py --web             # Launch the Interactive Web Dashboard on http://127.0.0.1:8000
    python run.py --scan            # Run market scan & display morning report in terminal
    python run.py --analyze LICI    # Deep dive on a single stock
    python run.py --compare LICI HDFCBANK # Side-by-side comparison
    python run.py --backtest        # Run 2-year strategy backtest against Nifty 50
    python run.py --outcomes        # View daily & cumulative target hit rate outcomes
    python run.py --audit           # View performance tracker audit
    python run.py --schedule        # Run automated trading day morning engine (08:45 AM)
"""
import sys
import io
import os
import argparse
import subprocess

# Ensure unbuffered output and quiet warnings
os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["PYTHONWARNINGS"] = "ignore"

# Fix Windows console Unicode output
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="BHARAT ALPHA: Indian Market Research Engine")
    parser.add_argument("--web", action="store_true", help="Start the Web Dashboard UI on port 8000")
    parser.add_argument("--scan", action="store_true", help="Run full market scan now")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of stocks to scan")
    parser.add_argument("--analyze", type=str, help="Analyze stock symbol (e.g. --analyze LICI)")
    parser.add_argument("--compare", nargs=2, metavar=("S1", "S2"), help="Compare two stocks")
    parser.add_argument("--backtest", action="store_true", help="Run 2-year strategy backtest")
    parser.add_argument("--outcomes", action="store_true", help="Show target achievement outcomes")
    parser.add_argument("--audit", action="store_true", help="Show performance tracking audit")
    parser.add_argument("--schedule", action="store_true", help="Run automated 08:45 AM scheduler")
    parser.add_argument("--port", type=int, default=8000, help="Web dashboard port (default 8000)")

    args = parser.parse_args()

    python_bin = sys.executable

    if args.web:
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            lan_ip = s.getsockname()[0]
            s.close()
        except Exception:
            lan_ip = "127.0.0.1"

        print(f"\n=======================================================")
        print(f"🚀 BHARAT ALPHA Web Dashboard Active:")
        print(f"   • Local:      http://127.0.0.1:{args.port}")
        print(f"   • LAN/Wi-Fi:  http://{lan_ip}:{args.port}")
        print(f"=======================================================\n", flush=True)
        subprocess.run([python_bin, "-u", "-m", "uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", str(args.port)])
    elif args.schedule:
        subprocess.run([python_bin, "-u", "scheduler.py"])
    elif args.analyze:
        subprocess.run([python_bin, "-u", "cli.py", "--analyze", args.analyze])
    elif args.compare:
        subprocess.run([python_bin, "-u", "cli.py", "--compare", args.compare[0], args.compare[1]])
    elif args.backtest:
        subprocess.run([python_bin, "-u", "cli.py", "--backtest"])
    elif args.outcomes:
        subprocess.run([python_bin, "-u", "cli.py", "--outcomes"])
    elif args.audit:
        subprocess.run([python_bin, "-u", "cli.py", "--audit"])
    else:
        # Default run scan
        cmd = [python_bin, "-u", "cli.py", "--scan"]
        if args.limit:
            cmd.extend(["--limit", str(args.limit)])
        subprocess.run(cmd)

if __name__ == "__main__":
    main()
