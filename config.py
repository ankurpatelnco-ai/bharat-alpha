"""
Configuration for Indian Market Research Engine & Opportunity Ranking System
Covers Nifty 50, Nifty 500, Sector Indices, Global Macro Assets, and Scoring Weights.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "research_audit.db"

# Macro and Benchmark Tickers
MACRO_TICKERS = {
    "NIFTY_50": "^NSEI",
    "SENSEX": "^BSESN",
    "BANK_NIFTY": "^NSEBANK",
    "INDIA_VIX": "^INDIAVIX",
    "BRENT_CRUDE": "BZ=F",
    "GOLD": "GC=F",
    "USD_INR": "USDINR=X",
    "US_10Y_YIELD": "^TNX",
    "DOLLAR_INDEX": "DX-Y.NYB",
    "SP500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW": "^DJI",
    "NIKKEI": "^N225",
    "HANG_SENG": "^HSI"
}

# Sector Indices
SECTOR_TICKERS = {
    "NIFTY_BANK": "^NSEBANK",
    "NIFTY_IT": "^CNXIT",
    "NIFTY_AUTO": "^CNXAUTO",
    "NIFTY_PHARMA": "^CNXPHAR",
    "NIFTY_FMCG": "^CNXFMCG",
    "NIFTY_METAL": "^CNXMETAL",
    "NIFTY_ENERGY": "^CNXENERGY",
    "NIFTY_REALTY": "^CNXREALTY",
    "NIFTY_INFRA": "^CNXINFRA"
}

# Representative Indian Stock Universe covering Large, Mid, Small Cap and key turnaround/bottom plays
# Includes Nifty 50, Nifty Next 50, PSU Giants (like LIC, SBI, Coal India, BHEL), Growth, and Value stocks
SCAN_UNIVERSE = [
    # Top Large Caps & Nifty 50
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "BHARTIARTL.NS", "ICICIBANK.NS", 
    "INFY.NS", "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "LICI.NS", 
    "LT.NS", "BAJFINANCE.NS", "MARUTI.NS", "HCLTECH.NS", "SUNPHARMA.NS", 
    "AXISBANK.NS", "TITAN.NS", "ULTRACEMCO.NS", "KOTAKBANK.NS", "TATAPOWER.NS", 
    "ONGC.NS", "NTPC.NS", "POWERGRID.NS", "ADANIENT.NS", "ADANIPORTS.NS", 
    "COALINDIA.NS", "BAJAJFINSV.NS", "JSWSTEEL.NS", "TATASTEEL.NS", "M&M.NS", 
    "NESTLEIND.NS", "SIEMENS.NS", "GRASIM.NS", "TECHM.NS", "WIPRO.NS", 
    "HDFCLIFE.NS", "SBILIFE.NS", "BPCL.NS", "BRITANNIA.NS", "EICHERMOT.NS", 
    "CIPLA.NS", "DRREDDY.NS", "DIVISLAB.NS", "HEROMOTOCO.NS", "HINDALCO.NS", 
    "APOLLOHOSP.NS", "BAJAJ-AUTO.NS", "ASIANPAINT.NS", "INDUSINDBK.NS", "BEL.NS", 
    
    # Nifty Next 50 & High-Momentum / Growth
    "HAL.NS", "VBL.NS", "TRENT.NS", "VEDL.NS", "JIOFIN.NS", 
    "CHOLAFIN.NS", "DLF.NS", "PFC.NS", "RECLTD.NS", "IRFC.NS", 
    "POLYCAB.NS", "ABB.NS", "MOTHERSON.NS", "BOSCHLTD.NS", "SHRIRAMFIN.NS", 
    "CANBK.NS", "BANKBARODA.NS", "PNB.NS", "INDIANB.NS", "UNIONBANK.NS", 
    "BHEL.NS", "SAIL.NS", "NMDC.NS", "OIL.NS", "GAIL.NS", 
    "TVSMOTOR.NS", "ASHOKLEY.NS", "BHARATFORG.NS", "CUMMINSIND.NS", "SUZLON.NS", 
    
    # Key Value, Turnaround & Bottom-Watch Stocks (Like LIC, Chemicals, IT & PSU turnaround plays)
    "UPL.NS", "TATACHEM.NS", "DEEPAKNTR.NS", "AARTIIND.NS", "ATUL.NS", 
    "SRF.NS", "NAVINFLUOR.NS", "PIIND.NS", "COROMANDEL.NS", "GNFC.NS", 
    "IRCTC.NS", "RVNL.NS", "MAZDOCK.NS", "COCHINSHIP.NS", "CONCOR.NS", 
    "KPITTECH.NS", "PERSISTENT.NS", "COFORGE.NS", "LTTS.NS", "MPHASIS.NS", 
    "OFSS.NS", "TATAELXSI.NS", "SONACOMS.NS", "DIXON.NS", "KAYNES.NS", 
    "IDEA.NS", "YESBANK.NS", "IDFCFIRSTB.NS", "BANDHANBNK.NS", "FEDERALBNK.NS", 
    "LICHSGFIN.NS", "MANAPPURAM.NS", "MUTHOOTFIN.NS", "HUDCO.NS", "ABCAPITAL.NS", 
    "PAYTM.NS", "NYKAA.NS", "POLICYBZR.NS", "DELHIVERY.NS", "PAGEIND.NS"
]

# Scoring Weights
SHORT_TERM_WEIGHTS = {
    "momentum": 0.20,
    "technical_setup": 0.20,
    "volume": 0.15,
    "relative_strength": 0.10,
    "news_catalyst": 0.15,
    "market_sector_trend": 0.10,
    "risk_reward": 0.10
}

LONG_TERM_WEIGHTS = {
    "business_quality": 0.20,
    "earnings_growth": 0.20,
    "roce_roe": 0.10,
    "balance_sheet": 0.10,
    "valuation": 0.15,
    "competitive_advantage": 0.10,
    "management_quality": 0.05,
    "industry_outlook": 0.10
}

# Bottom + Quality Opportunity Scanner Thresholds (LIC Example Model)
BOTTOM_SCANNER_CONFIG = {
    "min_drawdown_pct": 18.0,          # At least 18% below 52-week or all-time high
    "support_proximity_pct": 8.0,       # Within 8% of major 52W or historical support
    "max_debt_to_equity": 2.5,          # Financial health barrier (higher for banks/NBFCs handled separately)
    "min_roe_pct": 6.0,                 # Non-negative, respectable equity return
    "pe_discount_vs_peer_threshold": 0.85 # Discounted relative to peers / historical
}

# Alert / Dispatch Channels Defaults
NOTIFICATIONS_CONFIG = {
    "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN", ""),
    "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID", ""),
    "whatsapp_api_url": os.getenv("WHATSAPP_API_URL", ""),
    "email_recipient": os.getenv("EMAIL_RECIPIENT", "user@example.com"),
    "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port": int(os.getenv("SMTP_PORT", "587")),
    "smtp_user": os.getenv("SMTP_USER", ""),
    "smtp_password": os.getenv("SMTP_PASSWORD", "")
}
