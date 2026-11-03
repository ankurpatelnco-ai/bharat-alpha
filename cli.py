"""
CLI Interface for Indian Market Research Engine.
Usage:
    python cli.py --scan                      # Run complete research scan & print report
    python cli.py --analyze LICI              # Deep-dive on a single stock (e.g., LIC, RELIANCE)
    python cli.py --compare LICI HDFCBANK     # Factor comparison between two stocks
    python cli.py --telegram                  # Output Telegram formatted report
    python cli.py --whatsapp                  # Output WhatsApp compact summary
    python cli.py --email                     # Save and display Email HTML report
    python cli.py --audit                     # Show performance tracker & win-rate stats
"""
import argparse
import os
import sys
import io
import warnings
import logging

os.environ["PYTHONUNBUFFERED"] = "1"
os.environ["PYTHONWARNINGS"] = "ignore"
warnings.simplefilter("ignore")
logging.getLogger("yfinance").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

# Fix Windows console Unicode output
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from core.engine import run_full_market_scan, analyze_single_stock, _LATEST_SCAN_CACHE
from core.report_generator import (
    generate_telegram_report,
    generate_whatsapp_report,
    generate_email_html_report,
    format_single_stock_analysis,
    format_stock_comparison,
    format_outcomes_summary,
    format_backtest_summary
)
from core.audit_tracker import get_performance_audit, get_detailed_outcomes_summary
from core.backtester import run_2yr_backtest

def main():
    parser = argparse.ArgumentParser(description="Indian Market Automated Research Engine")
    parser.add_argument("--scan", action="store_true", help="Execute daily morning research scan")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of stocks to scan (e.g. --limit 30)")
    parser.add_argument("--analyze", type=str, help="Deep dive analysis on stock symbol (e.g. --analyze LICI)")
    parser.add_argument("--compare", nargs=2, metavar=("SYM1", "SYM2"), help="Compare two stocks side-by-side")
    parser.add_argument("--telegram", action="store_true", help="Print Telegram-formatted report")
    parser.add_argument("--whatsapp", action="store_true", help="Print WhatsApp-formatted summary")
    parser.add_argument("--email", action="store_true", help="Generate and save HTML email report")
    parser.add_argument("--audit", action="store_true", help="Display recommendation performance tracking audit")
    parser.add_argument("--outcomes", action="store_true", help="Display daily & cumulative target achieved summary")
    parser.add_argument("--backtest", action="store_true", help="Run 2-year strategy backtest against Nifty 50")
    parser.add_argument("--backtest-refresh", action="store_true", help="Force fresh 2-year historical download")

    args = parser.parse_args()

    if args.analyze:
        print(f"\n[CLI] Analyzing Stock: {args.analyze}...")
        try:
            data = analyze_single_stock(args.analyze)
            card = format_single_stock_analysis(data)
            print(card)
        except Exception as e:
            print(f"[ERROR] Failed to analyze stock: {e}")
        return

    if args.compare:
        s1, s2 = args.compare
        print(f"\n[CLI] Comparing {s1} vs {s2}...")
        try:
            d1 = analyze_single_stock(s1)
            d2 = analyze_single_stock(s2)
            comp = format_stock_comparison(d1, d2)
            print(comp)
        except Exception as e:
            print(f"[ERROR] Comparison failed: {e}")
        return

    if args.audit:
        print("\n[CLI] Retrieving Recommendation Performance Audit from SQLite...")
        audit = get_performance_audit()
        print(f"Total Recommendations Tracked: {audit['total_recommendations']}")
        print(f"Win Rate: {audit['win_rate_pct']}% | Average Return: {audit['avg_return_pct']}%")
        print("\nRecent Tracked Recommendations:")
        print(f"{'Date':<12} | {'Symbol':<12} | {'Category':<14} | {'Entry':<8} | {'Current':<8} | {'Return':<8} | {'Status'}")
        print("-" * 75)
        for r in audit["records"]:
            sym = r.get('symbol', '')[:10]
            cat = r.get('category', '')[:14]
            ep = r.get('entry_price', 0.0)
            cp = r.get('current_price', ep)
            ret = r.get('return_pct', 0.0)
            st = r.get('status', 'OPEN')
            print(f"{r.get('date', ''):<12} | {sym:<12} | {cat:<14} | ₹{ep:<7} | ₹{cp:<7} | {ret:<7}% | {st}")
        return

    if args.outcomes:
        print("\n[CLI] Calculating Daily & Cumulative Target Achievement Outcomes...")
        outcomes = get_detailed_outcomes_summary()
        print(format_outcomes_summary(outcomes))
        return

    if args.backtest:
        print("\n[CLI] Running 2-Year Strategy Backtest Simulation against Nifty 50...")
        bt = run_2yr_backtest(force_refresh=args.backtest_refresh)
        print(format_backtest_summary(bt))
        return

    # Default or --scan
    scan_data = run_full_market_scan(max_stocks=args.limit)

    if args.telegram:
        print("\n" + generate_telegram_report(scan_data))
    elif args.whatsapp:
        print("\n" + generate_whatsapp_report(scan_data))
    elif args.email:
        html = generate_email_html_report(scan_data)
        out_file = Path("morning_report.html")
        out_file.write_text(html, encoding="utf-8")
        print(f"\n[CLI] Email HTML report written to {out_file.resolve()}")
    else:
        # Default prints Telegram report format for readability in terminal
        print("\n" + generate_telegram_report(scan_data))

if __name__ == "__main__":
    main()
