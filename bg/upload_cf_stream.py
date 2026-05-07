"""Upload MetaFlow video clips to Cloudflare Stream and save UIDs."""
import requests, os, json, sys, time

ACCOUNT_ID = "7a6e1fad95b03d6e23f9b3542f818c5e"
API_TOKEN  = "cfut_DQMelRTRem8pN6lU09AwrkEeio6rMnxKLHM0RGaj15f87980"
CLIPS_DIR  = r"D:\TrustedNutraProducts\VSL Downloader\MetaFlow\Clips"

VIDEOS = [
    {"slot": 1, "slug": "mf-hook",       "label": "MetaFlow Hook - ER Drama",        "file": r"hooks_educational\V2_H1_ER_drama.mp4"},
    {"slot": 2, "slug": "mf-stats",      "label": "MetaFlow Stats - Complications",  "file": r"hooks_educational\V2_E3_complications_stats.mp4"},
    {"slot": 3, "slug": "mf-hotel",      "label": "MetaFlow Education - Hotel",      "file": r"hooks_educational\V3_H3_hotel_analogy.mp4"},
    {"slot": 4, "slug": "mf-alan",       "label": "MetaFlow Story - Alan",           "file": r"testimonials\V2_T6_alan.mp4"},
    {"slot": 5, "slug": "mf-jessica",    "label": "MetaFlow Testimonial - Jessica",  "file": r"testimonials\V2_T1_jessica.mp4"},
    {"slot": 6, "slug": "mf-william",    "label": "MetaFlow Testimonial - William",  "file": r"testimonials\V2_T2_william.mp4"},
    {"slot": 7, "slug": "mf-donna",      "label": "MetaFlow Testimonial - Donna",    "file": r"testimonials\V2_T3_donna.mp4"},
    {"slot": 8, "slug": "mf-aspiration", "label": "MetaFlow Aspiration",             "file": r"hooks_educational\V3_H1_aspiration.mp4"},
    {"slot": 9, "slug": "mf-warning",    "label": "MetaFlow Warning - Insulin Damage", "file": r"hooks_educational\V3_H4_high_insulin_damage.mp4"},
    {"slot": 10, "slug": "mf-patty",     "label": "MetaFlow Final - Patty",          "file": r"testimonials\V2_T5_patty.mp4"},
]

results = {}
url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream"

for v in VIDEOS:
    mp4_path = os.path.join(CLIPS_DIR, v["file"])
    if not os.path.exists(mp4_path):
        print(f"[Slot {v['slot']}] MISSING: {v['file']}", flush=True)
        continue

    size_mb = os.path.getsize(mp4_path) / (1024 * 1024)
    print(f"[Slot {v['slot']}] Uploading {v['slug']} ({size_mb:.1f} MB)...", flush=True)
    t0 = time.time()
    with open(mp4_path, "rb") as f:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            files={"file": (os.path.basename(mp4_path), f, "video/mp4")},
            data={"meta": json.dumps({"name": v["label"]})},
            timeout=600,
        )
    dt = time.time() - t0

    if resp.status_code in (200, 201):
        uid = resp.json()["result"]["uid"]
        results[v["slug"]] = {"uid": uid, "label": v["label"], "slot": v["slot"]}
        print(f"  -> UID {uid} ({dt:.1f}s)", flush=True)
    else:
        print(f"  ERROR ({resp.status_code}): {resp.text[:300]}", flush=True)
        results[v["slug"]] = {"error": resp.text[:300], "label": v["label"], "slot": v["slot"]}

out_path = r"D:\TrustedNutraProducts\MetaFlow\bg\cf_video_ids.json"
with open(out_path, "w") as f:
    json.dump(results, f, indent=2)

print("\n=== ALL DONE ===", flush=True)
print(f"Saved to: {out_path}", flush=True)
print(json.dumps(results, indent=2), flush=True)
