"""
Automated Morning Schedule Engine (8:30 - 9:00 AM IST).
Runs pre-market analysis on every trading day (Monday - Friday),
generates the 3 multi-channel report formats, archives them locally in reports/,
and dispatches to Telegram, WhatsApp Webhook, and SMTP Email if configured.
"""
import sys
import io
import time
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from pathlib import Path
import requests

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from config import NOTIFICATIONS_CONFIG
from core.engine import run_full_market_scan
from core.report_generator import (
    generate_telegram_report,
    generate_whatsapp_report,
    generate_email_html_report
)

REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

def dispatch_telegram(message_text: str):
    """Sends full research markdown to Telegram channel or bot chat."""
    token = NOTIFICATIONS_CONFIG.get("telegram_bot_token")
    chat_id = NOTIFICATIONS_CONFIG.get("telegram_chat_id")
    if not token or not chat_id:
        print("[NOTIFY] Telegram credentials not configured in environment. Saved locally.")
        return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message_text,
            "parse_mode": "Markdown"
        }
        r = requests.post(url, json=payload, timeout=10)
        if r.status_code == 200:
            print("[NOTIFY] Successfully delivered Telegram report.")
            return True
        else:
            print(f"[NOTIFY] Telegram delivery failed: {r.text}")
    except Exception as e:
        print(f"[NOTIFY] Telegram exception: {e}")
    return False


def dispatch_email(html_content: str, subject: str = "Indian Market Morning Intelligence Report"):
    """Dispatches HTML report via SMTP."""
    smtp_user = NOTIFICATIONS_CONFIG.get("smtp_user")
    smtp_pass = NOTIFICATIONS_CONFIG.get("smtp_password")
    recipient = NOTIFICATIONS_CONFIG.get("email_recipient")
    smtp_server = NOTIFICATIONS_CONFIG.get("smtp_server")
    smtp_port = NOTIFICATIONS_CONFIG.get("smtp_port")

    if not smtp_user or not smtp_pass:
        print("[NOTIFY] SMTP credentials not set. Email saved locally.")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = smtp_user
        msg["To"] = recipient
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, recipient, msg.as_string())
        print(f"[NOTIFY] Successfully emailed report to {recipient}.")
        return True
    except Exception as e:
        print(f"[NOTIFY] Email sending failed: {e}")
    return False


def execute_morning_cycle():
    """Executes the daily morning research run and archives all reports."""
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"\n=======================================================")
    print(f"⏰ [SCHEDULER] Triggering Daily Morning Scan: {today} at {datetime.now().strftime('%H:%M:%S')}")
    print(f"=======================================================")

    # 1. Run Market Scan
    scan_data = run_full_market_scan()

    # 2. Evaluate Target Achievements and Hit Status on Historical Picks
    try:
        from core.audit_tracker import update_target_outcomes
        from core.data_fetcher import fetch_price_history_batch
        from config import SCAN_UNIVERSE
        histories = fetch_price_history_batch(SCAN_UNIVERSE[:35], period="1mo")
        update_target_outcomes(histories)
    except Exception as e:
        print(f"[SCHEDULER] Note on target outcomes evaluation: {e}")

    # 3. Generate Reports
    tg_text = generate_telegram_report(scan_data)
    wa_text = generate_whatsapp_report(scan_data)
    email_html = generate_email_html_report(scan_data)

    # 3. Archive Locally
    tg_file = REPORTS_DIR / f"telegram_report_{today}.txt"
    wa_file = REPORTS_DIR / f"whatsapp_summary_{today}.txt"
    email_file = REPORTS_DIR / f"email_report_{today}.html"

    tg_file.write_text(tg_text, encoding="utf-8")
    wa_file.write_text(wa_text, encoding="utf-8")
    email_file.write_text(email_html, encoding="utf-8")

    print(f"[SCHEDULER] Reports archived:")
    print(f"  • {tg_file}")
    print(f"  • {wa_file}")
    print(f"  • {email_file}")

    # 4. Dispatch Notifications
    dispatch_telegram(tg_text)
    dispatch_email(email_html, subject=f"🇮🇳 Bharat Alpha Daily Report - {today}")
    print(f"[SCHEDULER] Daily Morning Cycle Complete!")


def run_scheduler_loop(target_time: str = "08:45"):
    """
    Continuous loop that triggers at target_time (08:45 AM IST) Monday through Friday.
    """
    print(f"[SCHEDULER] Daily market scheduler active. Scheduled for {target_time} IST every trading day.")
    last_run_date = ""

    while True:
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        current_hm = now.strftime("%H:%M")
        weekday = now.weekday()  # 0 is Monday, 4 is Friday

        # Only on trading days Monday(0) - Friday(4)
        if weekday < 5 and current_hm == target_time and current_date != last_run_date:
            try:
                execute_morning_cycle()
                last_run_date = current_date
            except Exception as e:
                print(f"[SCHEDULER ERROR] Cycle failed: {e}")

        time.sleep(30)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Automated Indian Market Schedule Dispatcher")
    parser.add_argument("--now", action="store_true", help="Execute morning cycle immediately and exit")
    parser.add_argument("--loop-only", action="store_true", help="Wait for scheduled time without running immediate cycle")
    parser.add_argument("--time", type=str, default="08:45", help="Target daily run time HH:MM (default 08:45)")
    args = parser.parse_args()

    if args.loop_only:
        run_scheduler_loop(target_time=args.time)
    elif args.now:
        print("[SCHEDULER] Running immediate market scan cycle...", flush=True)
        execute_morning_cycle()
    else:
        print("[SCHEDULER] Running market scan cycle now before entering schedule loop...", flush=True)
        execute_morning_cycle()
        print(f"[SCHEDULER] Cycle complete. Monitoring schedule for daily {args.time} AM IST run (Press Ctrl+C to stop)...", flush=True)
        run_scheduler_loop(target_time=args.time)
