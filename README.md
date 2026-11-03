# BHARAT ALPHA: Indian Market Automated Research Engine

An institutional-grade research and opportunity ranking engine for the Indian stock universe (Nifty 50, Nifty 500, BSE).

## Key Capabilities
- **Pre-Market Macro Analysis**: Live tracking of Nifty 50, Sensex, Brent Crude, India VIX, US 10Y Yield, Dollar Index, and USD/INR.
- **500+ Universe Ingestion**: Ingests 1-year OHLCV and computes RSI, MACD, EMAs (20/50/200), Volume Breakout, Support/Resistance, and Relative Strength vs Nifty.
- **Fundamental & Valuation Modeling**: P/E vs 5-year average, P/B, Debt/Equity, ROE, ROCE, Free Cash Flow, and Institutional Holding.
- **The LIC "Bottom + Quality Opportunity Scanner"**: Detects stocks with deep drawdowns near major support and distinguishes genuine value from value traps (🟢 ACCUMULATE / 🟡 WATCH / 🔴 AVOID).
- **5 Specialized Portfolios**:
  1. 🚀 Short-Term (1-30 days)
  2. 📈 Swing (2-12 weeks)
  3. 🏦 Long-Term (1-5 years)
  4. 💎 Deep Value
  5. 🔄 Turnaround
  6. ⚠️ Top 10 Stocks to AVOID
- **Multi-Channel Morning Reports**:
  - **Telegram**: Full research markdown with macro, breadth, and setups.
  - **WhatsApp**: Compact, actionable summary.
  - **Email**: Responsive HTML report with cards and badges.
- **Interactive Deep Dive & Compare**:
  - Analyze any stock (`/analyze LICI`, `/analyze RELIANCE`)
  - Compare two stocks side-by-side (`/compare LICI HDFCBANK`)
- **Recommendation Performance Audit**:
  - Immutable SQLite ledger (`data/research_audit.db`) tracking 1D, 1W, 1M, 3M, 1Y forward returns and hit rates vs Nifty benchmark.

---

## Quickstart

### 1. Launch the Web Dashboard
```bash
.venv\Scripts\python run.py --web
```
Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser to view the interactive real-time dashboard.

### 2. Run Daily Scan in Terminal
```bash
.venv\Scripts\python cli.py --scan
```

### 3. Analyze Any Stock on Demand
```bash
.venv\Scripts\python cli.py --analyze LICI
.venv\Scripts\python cli.py --analyze RELIANCE
```

### 4. Compare Two Stocks Side-by-Side
```bash
.venv\Scripts\python cli.py --compare LICI HDFCBANK
```

### 5. Check Target Outcomes & Achievement Ledger (Hit / Miss Summary)
```bash
.venv\Scripts\python cli.py --outcomes
```
Displays whether Target 1, Target 2, or Stop Loss was achieved for every recommendation, holding duration, and system win-rate.

### 6. Run 2-Year Strategy Backtest Simulation (vs Nifty 50)
```bash
.venv\Scripts\python cli.py --backtest
# Or force a fresh download:
.venv\Scripts\python cli.py --backtest --backtest-refresh
```
Simulates 500 trading days testing Momentum Breakouts and LIC Bottom-Hunting reversals, outputting 2Y Strategy Return, Benchmark Return, Alpha, Win Rate %, Profit Factor, Max Drawdown, and Trade Ledger.

### 7. Run Automated Morning Scheduler (8:30-9:00 AM IST)
```bash
.venv\Scripts\python scheduler.py
# Or trigger immediately:
.venv\Scripts\python scheduler.py --now
```
