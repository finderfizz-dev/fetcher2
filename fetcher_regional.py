from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import time
import random
import threading
import os
import sys
from datetime import datetime, timezone
from collections import defaultdict

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

app = Flask(__name__)
CORS(app)

# ===============================
# Configuration
# ===============================
API_SECRET = "ATulI0I0QJVbKiZsJSkvweMTTib2O50m93TqIj9Hv4Qu4mVNVAATWwmiKjQsyuJ6"

# Central API configuration
CENTRAL_API_URL = "https://fizzfinder.store/fetcher/submit"
REGION_ID = os.getenv("REGION_ID", f"region-{random.randint(1000, 9999)}")

COOKIES = [
    os.getenv("ROBLOX_COOKIE_1"),
    os.getenv("ROBLOX_COOKIE_2"),
    os.getenv("ROBLOX_COOKIE_3"),
    os.getenv("ROBLOX_COOKIE_4"),
    os.getenv("ROBLOX_COOKIE_5"),
    os.getenv("ROBLOX_COOKIE_6"),
    os.getenv("ROBLOX_COOKIE_7"),
    os.getenv("ROBLOX_COOKIE_8"),
    os.getenv("ROBLOX_COOKIE_9"),
    os.getenv("ROBLOX_COOKIE_10"),
    os.getenv("ROBLOX_COOKIE_11"),
    os.getenv("ROBLOX_COOKIE_12"),
    os.getenv("ROBLOX_COOKIE_13"),
    os.getenv("ROBLOX_COOKIE_14"),
    os.getenv("ROBLOX_COOKIE_15"),
    os.getenv("ROBLOX_COOKIE_16"),
    os.getenv("ROBLOX_COOKIE_17"),
    os.getenv("ROBLOX_COOKIE_18"),
    os.getenv("ROBLOX_COOKIE_19"),
    os.getenv("ROBLOX_COOKIE_20"),
    os.getenv("ROBLOX_COOKIE_21"),
    os.getenv("ROBLOX_COOKIE_22"),
    os.getenv("ROBLOX_COOKIE_23"),
    os.getenv("ROBLOX_COOKIE_24"),
    os.getenv("ROBLOX_COOKIE_25"),
    os.getenv("ROBLOX_COOKIE_26"),
    os.getenv("ROBLOX_COOKIE_27"),
    os.getenv("ROBLOX_COOKIE_28"),
    os.getenv("ROBLOX_COOKIE_29"),
    os.getenv("ROBLOX_COOKIE_30"),
    os.getenv("ROBLOX_COOKIE_31"),
    os.getenv("ROBLOX_COOKIE_32"),
    os.getenv("ROBLOX_COOKIE_33"),
    os.getenv("ROBLOX_COOKIE_34"),
    os.getenv("ROBLOX_COOKIE_35"),
    os.getenv("ROBLOX_COOKIE_36"),
    os.getenv("ROBLOX_COOKIE_37"),
    os.getenv("ROBLOX_COOKIE_38"),
    os.getenv("ROBLOX_COOKIE_39"),
    os.getenv("ROBLOX_COOKIE_40"),
    os.getenv("ROBLOX_COOKIE_41"),
    os.getenv("ROBLOX_COOKIE_42"),
    os.getenv("ROBLOX_COOKIE_43"),
    os.getenv("ROBLOX_COOKIE_44"),
    os.getenv("ROBLOX_COOKIE_45"),
    os.getenv("ROBLOX_COOKIE_46"),
    os.getenv("ROBLOX_COOKIE_47"),
    os.getenv("ROBLOX_COOKIE_48"),
    os.getenv("ROBLOX_COOKIE_49"),
    os.getenv("ROBLOX_COOKIE_50"),
    os.getenv("ROBLOX_COOKIE_51"),
    os.getenv("ROBLOX_COOKIE_52"),
    os.getenv("ROBLOX_COOKIE_53"),
    os.getenv("ROBLOX_COOKIE_54"),
    os.getenv("ROBLOX_COOKIE_55"),
    os.getenv("ROBLOX_COOKIE_56"),
    os.getenv("ROBLOX_COOKIE_57"),
    os.getenv("ROBLOX_COOKIE_58"),
    os.getenv("ROBLOX_COOKIE_59"),
    os.getenv("ROBLOX_COOKIE_60"),
    os.getenv("ROBLOX_COOKIE_61"),
    os.getenv("ROBLOX_COOKIE_62"),
    os.getenv("ROBLOX_COOKIE_63"),
    os.getenv("ROBLOX_COOKIE_64"),
    os.getenv("ROBLOX_COOKIE_65"),
    os.getenv("ROBLOX_COOKIE_66"),
    os.getenv("ROBLOX_COOKIE_67"),
    os.getenv("ROBLOX_COOKIE_68"),
    os.getenv("ROBLOX_COOKIE_69"),
    os.getenv("ROBLOX_COOKIE_70"),
    os.getenv("ROBLOX_COOKIE_71"),
    os.getenv("ROBLOX_COOKIE_72"),
    os.getenv("ROBLOX_COOKIE_73"),
    os.getenv("ROBLOX_COOKIE_74"),
    os.getenv("ROBLOX_COOKIE_75"),
    os.getenv("ROBLOX_COOKIE_76"),
    os.getenv("ROBLOX_COOKIE_77"),
    os.getenv("ROBLOX_COOKIE_78"),
    os.getenv("ROBLOX_COOKIE_79"),
    os.getenv("ROBLOX_COOKIE_80"),
    os.getenv("ROBLOX_COOKIE_81"),
    os.getenv("ROBLOX_COOKIE_82"),
    os.getenv("ROBLOX_COOKIE_83"),
    os.getenv("ROBLOX_COOKIE_84"),
    os.getenv("ROBLOX_COOKIE_85"),
    os.getenv("ROBLOX_COOKIE_86"),
    os.getenv("ROBLOX_COOKIE_87"),
    os.getenv("ROBLOX_COOKIE_88"),
    os.getenv("ROBLOX_COOKIE_89"),
    os.getenv("ROBLOX_COOKIE_90"),
    os.getenv("ROBLOX_COOKIE_91"),
    os.getenv("ROBLOX_COOKIE_92"),
    os.getenv("ROBLOX_COOKIE_93"),
    os.getenv("ROBLOX_COOKIE_94"),
    os.getenv("ROBLOX_COOKIE_95"),
    os.getenv("ROBLOX_COOKIE_96"),
    os.getenv("ROBLOX_COOKIE_97"),
    os.getenv("ROBLOX_COOKIE_98"),
    os.getenv("ROBLOX_COOKIE_99"),
    os.getenv("ROBLOX_COOKIE_100")
]

COOKIES = [c for c in COOKIES if c]
if len(COOKIES) == 0:
    raise RuntimeError("❌ ERROR: No ROBLOX_COOKIE_* environment variables set!")

PLACE_ID = "109983668079237"

# ⚡ PERFORMANCE TUNING - SAFE FASTER SETTINGS
FETCH_INTERVAL = 6.0  # From 7.0 → 14% faster (safe)
REQUEST_TIMEOUT = 7  # From 8 → slightly faster
COOKIE_DELAY_MIN = 0.30  # From 0.38 → 21% faster
COOKIE_DELAY_MAX = 1.00  # From 1.14 → 12% faster
BATCH_DELAY_MIN = 0.60  # From 0.76 → 21% faster
BATCH_DELAY_MAX = 1.20  # From 1.52 → 21% faster
SUBMISSION_RETRY_DELAY = 1.5  # From 2.0 → 25% faster

# ===============================
# Global State
# ===============================
all_job_ids = []
job_lock = threading.Lock()
cookie_stats = {"total_fetches": 0, "rate_limits": 0, "last_fetch": None, "submissions": 0, "submission_errors": 0}
fetcher_ready = False

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
})

# ===============================
# Helper Functions
# ===============================
def check_secret():
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False
    token = auth_header.split(" ", 1)[1].strip()
    return token == API_SECRET.strip()

def fetch_jobs_with_cookie(cookie_index):
    cookie = COOKIES[cookie_index]
    url = f"https://games.roblox.com/v1/games/{PLACE_ID}/servers/Public"
    params = {"sortOrder": "Desc", "limit": 100}
    headers = {"Cookie": f".ROBLOSECURITY={cookie}"}
    
    try:
        time.sleep(random.uniform(COOKIE_DELAY_MIN, COOKIE_DELAY_MAX))
        resp = session.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
        
        if resp.status_code == 200:
            data = resp.json()
            jobs = [{"id": s.get("id"), "playing": s.get("playing", 0), 
                    "maxPlayers": s.get("maxPlayers", 0)} 
                   for s in data.get("data", [])]
            cookie_stats["total_fetches"] += 1
            return jobs
        elif resp.status_code == 429:
            cookie_stats["rate_limits"] += 1
            return []
        else:
            return []
    except:
        return []

def submit_to_central_api(jobs):
    """Submit collected jobs to central API"""
    try:
        payload = {
            "region_id": REGION_ID,
            "jobs": jobs
        }
        headers = {
            "Authorization": f"Bearer {API_SECRET}",
            "Content-Type": "application/json"
        }
        
        resp = requests.post(CENTRAL_API_URL, json=payload, headers=headers, timeout=10)
        
        if resp.status_code == 200:
            cookie_stats["submissions"] += 1
            result = resp.json()
            return True, result.get("total_pool", 0)
        else:
            cookie_stats["submission_errors"] += 1
            print(f"❌ Central API error: {resp.status_code}", flush=True)
            return False, 0
    except Exception as e:
        cookie_stats["submission_errors"] += 1
        print(f"❌ Submission failed: {e}", flush=True)
        return False, 0

def fetch_all_cookies():
    global all_job_ids, fetcher_ready
    
    new_jobs = []
    for i in range(len(COOKIES)):
        jobs = fetch_jobs_with_cookie(i)
        new_jobs.extend(jobs)
        time.sleep(random.uniform(BATCH_DELAY_MIN, BATCH_DELAY_MAX))
    
    unique_jobs = {}
    for job in new_jobs:
        if job["id"] not in unique_jobs:
            unique_jobs[job["id"]] = job
    
    jobs_list = list(unique_jobs.values())
    
    # Submit to central API
    success, total_pool = submit_to_central_api(jobs_list)
    
    with job_lock:
        all_job_ids = jobs_list
        random.shuffle(all_job_ids)
        fetcher_ready = True
        cookie_stats["last_fetch"] = datetime.now(timezone.utc)
    
    current_time = datetime.now(timezone.utc).strftime("%H:%M:%S")
    status = "✅" if success else "❌"
    print(f"[{current_time}] {status} Fetched {len(all_job_ids)} servers | Central pool: {total_pool} | Submissions: {cookie_stats['submissions']} | Errors: {cookie_stats['submission_errors']}", flush=True)

def background_fetcher():
    while True:
        try:
            fetch_all_cookies()
            time.sleep(FETCH_INTERVAL)
        except Exception as e:
            print(f"❌ Fetcher error: {e}", flush=True)
            time.sleep(SUBMISSION_RETRY_DELAY)

# ===============================
# API Endpoints (for local debugging)
# ===============================
@app.route("/health", methods=["GET"])
def health():
    with job_lock:
        return jsonify({
            "status": "online",
            "region_id": REGION_ID,
            "cookies": len(COOKIES),
            "ready": fetcher_ready,
            "servers_cached": len(all_job_ids),
            "stats": cookie_stats
        }), 200

@app.route("/stats", methods=["GET"])
def stats():
    """Get fetcher statistics"""
    return jsonify({
        "status": "ok",
        "region_id": REGION_ID,
        "cookies": len(COOKIES),
        "stats": cookie_stats,
        "servers_cached": len(all_job_ids),
        "fetch_interval": FETCH_INTERVAL
    }), 200

# ===============================
# Startup
# ===============================
def init_app():
    print(f"🚀 Regional Fetcher [{REGION_ID}] starting", flush=True)
    print(f"🔧 Config: {len(COOKIES)} cookies | Interval: {FETCH_INTERVAL}s", flush=True)
    print(f"🌐 Central API: {CENTRAL_API_URL}", flush=True)
    fetcher_thread = threading.Thread(target=background_fetcher, daemon=True)
    fetcher_thread.start()
    fetch_all_cookies()

init_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
