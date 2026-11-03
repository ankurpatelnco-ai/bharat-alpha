"""
FastAPI Web Server for Indian Market Research Engine & Opportunity Ranking Dashboard.
Includes session-based authentication, user access control, and live dashboard APIs.
"""
import sys
import io
import warnings
from pathlib import Path
from typing import Optional

# UTF-8 stdout on Windows
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=UserWarning)
warnings.filterwarnings("ignore")

from fastapi import FastAPI, Query, HTTPException, Request, Response, Depends
from fastapi.responses import HTMLResponse, PlainTextResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from core.engine import run_full_market_scan, analyze_single_stock, _LATEST_SCAN_CACHE
import core.engine as engine_module
from core.report_generator import (
    generate_telegram_report,
    generate_whatsapp_report,
    generate_email_html_report,
    format_single_stock_analysis,
    format_stock_comparison
)
from core.audit_tracker import get_performance_audit
from core.auth import (
    authenticate_user,
    register_user,
    create_session_token,
    verify_session_token,
    change_user_password,
    delete_user,
    list_users,
    toggle_registration,
    get_public_auth_config,
    get_all_users,
    SESSION_DURATION_SECS
)

app = FastAPI(title="Bharat Alpha Research Engine", version="1.0.0")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

class AuthCredentials(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: Optional[str] = "viewer"

class ToggleRegRequest(BaseModel):
    allow: bool

def require_auth(request: Request) -> str:
    token = request.cookies.get("bharat_auth_token")
    username = verify_session_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Authentication required. Please sign in.")
    return username

def get_or_run_scan():
    cached = engine_module.get_latest_scan_cache()
    if cached is not None:
        return cached
    # Fallback to fast initial scan
    engine_module._LATEST_SCAN_CACHE = run_full_market_scan(max_stocks=35)
    return engine_module._LATEST_SCAN_CACHE

# ----------------- AUTHENTICATION ROUTES -----------------

@app.get("/login", response_class=HTMLResponse)
async def serve_login(request: Request):
    token = request.cookies.get("bharat_auth_token")
    username = verify_session_token(token)
    if username:
        return RedirectResponse(url="/", status_code=303)
    login_file = TEMPLATES_DIR / "login.html"
    return HTMLResponse(content=login_file.read_text(encoding="utf-8"))

@app.get("/api/auth/config")
async def api_auth_config():
    return get_public_auth_config()

@app.post("/api/auth/login")
async def api_login(creds: AuthCredentials):
    user = authenticate_user(creds.username, creds.password)
    if not user:
        return JSONResponse(status_code=400, content={"success": False, "error": "Invalid username or password."})
    token = create_session_token(user["username"])
    res = JSONResponse(content={"success": True, "username": user["username"], "role": user["role"]})
    res.set_cookie(
        key="bharat_auth_token",
        value=token,
        max_age=SESSION_DURATION_SECS,
        httponly=True,
        samesite="lax",
        path="/"
    )
    return res

@app.post("/api/auth/register")
async def api_register(creds: AuthCredentials):
    success, msg = register_user(creds.username, creds.password)
    if not success:
        return JSONResponse(status_code=400, content={"success": False, "error": msg})
    return JSONResponse(content={"success": True, "message": msg})

@app.post("/api/auth/logout")
async def api_logout():
    res = JSONResponse(content={"success": True})
    res.delete_cookie(key="bharat_auth_token", path="/" )
    return res

@app.get("/api/auth/me")
async def api_me(request: Request):
    token = request.cookies.get("bharat_auth_token")
    username = verify_session_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    data = get_all_users()
    user_info = data.get("users", {}).get(username, {})
    return {
        "authenticated": True,
        "username": username,
        "role": user_info.get("role", "viewer")
    }

@app.post("/api/auth/change-password")
async def api_change_password(req: ChangePasswordRequest, user: str = Depends(require_auth)):
    auth_check = authenticate_user(user, req.current_password)
    if not auth_check:
        return JSONResponse(status_code=400, content={"success": False, "error": "Current password is incorrect."})
    success, msg = change_user_password(user, req.new_password)
    if not success:
        return JSONResponse(status_code=400, content={"success": False, "error": msg})
    return {"success": True, "message": msg}

@app.get("/api/auth/users")
async def api_get_users(user: str = Depends(require_auth)):
    data = get_all_users()
    users_dict = data.get("users", {})
    if users_dict.get(user, {}).get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin permissions required.")
    return {
        "allow_registration": data.get("allow_registration", False),
        "users": list_users()
    }

@app.post("/api/auth/users/create")
async def api_create_user_admin(req: CreateUserRequest, user: str = Depends(require_auth)):
    data = get_all_users()
    if data.get("users", {}).get(user, {}).get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin permissions required.")
    success, msg = register_user(req.username, req.password, is_admin_created=True, role=req.role or "viewer")
    if not success:
        return JSONResponse(status_code=400, content={"success": False, "error": msg})
    return {"success": True, "message": msg}

@app.delete("/api/auth/users/{username}")
async def api_delete_user(username: str, user: str = Depends(require_auth)):
    data = get_all_users()
    if data.get("users", {}).get(user, {}).get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin permissions required.")
    success, msg = delete_user(username)
    if not success:
        return JSONResponse(status_code=400, content={"success": False, "error": msg})
    return {"success": True, "message": msg}

@app.post("/api/auth/toggle-registration")
async def api_toggle_registration(req: ToggleRegRequest, user: str = Depends(require_auth)):
    data = get_all_users()
    if data.get("users", {}).get(user, {}).get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin permissions required.")
    state = toggle_registration(req.allow)
    return {"success": True, "allow_registration": state}

# ----------------- PROTECTED DASHBOARD ROUTES -----------------

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    token = request.cookies.get("bharat_auth_token")
    username = verify_session_token(token)
    if not username:
        return RedirectResponse(url="/login", status_code=303)
    index_file = TEMPLATES_DIR / "index.html"
    return HTMLResponse(content=index_file.read_text(encoding="utf-8"))

@app.get("/api/scan")
async def get_scan(_user: str = Depends(require_auth)):
    return get_or_run_scan()

@app.post("/api/scan/refresh")
async def refresh_scan(_user: str = Depends(require_auth)):
    data = run_full_market_scan(max_stocks=45)
    return data

@app.get("/api/analyze/{symbol}")
async def api_analyze(symbol: str, _user: str = Depends(require_auth)):
    try:
        result = analyze_single_stock(symbol)
        return result
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/compare")
async def api_compare(
    s1: str = Query(..., description="First Stock Symbol"),
    s2: str = Query(..., description="Second Stock Symbol"),
    _user: str = Depends(require_auth)
):
    try:
        d1 = analyze_single_stock(s1)
        d2 = analyze_single_stock(s2)
        return {
            "stock1": d1,
            "stock2": d2
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/reports/telegram", response_class=PlainTextResponse)
async def get_telegram_text(_user: str = Depends(require_auth)):
    scan_data = get_or_run_scan()
    return generate_telegram_report(scan_data)

@app.get("/api/reports/whatsapp", response_class=PlainTextResponse)
async def get_whatsapp_text(_user: str = Depends(require_auth)):
    scan_data = get_or_run_scan()
    return generate_whatsapp_report(scan_data)

@app.get("/api/reports/email", response_class=HTMLResponse)
async def get_email_preview(_user: str = Depends(require_auth)):
    scan_data = get_or_run_scan()
    return HTMLResponse(content=generate_email_html_report(scan_data))

@app.get("/api/audit")
async def get_audit(_user: str = Depends(require_auth)):
    return get_performance_audit()

@app.get("/api/outcomes")
async def get_outcomes(_user: str = Depends(require_auth)):
    from core.audit_tracker import get_detailed_outcomes_summary
    return get_detailed_outcomes_summary()

@app.get("/api/backtest")
async def get_backtest(_user: str = Depends(require_auth)):
    from core.backtester import run_2yr_backtest
    return run_2yr_backtest()

@app.post("/api/backtest/refresh")
async def refresh_backtest(_user: str = Depends(require_auth)):
    from core.backtester import run_2yr_backtest
    return run_2yr_backtest(force_refresh=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web_app:app", host="0.0.0.0", port=8000, reload=False)
