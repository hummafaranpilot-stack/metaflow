# Cloudflare Stream — Upload & Embed Guide

Complete workflow for uploading videos to Cloudflare Stream and embedding them on any landing page with tap-to-pause support.

---

## 1. Credentials

```
ACCOUNT_ID = "7a6e1fad95b03d6e23f9b3542f818c5e"
API_TOKEN  = "cfut_DQMelRTRem8pN6lU09AwrkEeio6rMnxKLHM0RGaj15f87980"
```

**Token permissions needed:** `Stream: Edit` on the account.

Create a new token at: https://dash.cloudflare.com/profile/api-tokens

---

## 2. Upload API

### Endpoint
```
POST https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream
```

### Headers
```
Authorization: Bearer {API_TOKEN}
```

### Body (multipart/form-data)
| Field  | Value                                          |
|--------|------------------------------------------------|
| `file` | Binary MP4 (up to 200MB; use TUS for larger)  |
| `meta` | JSON string, e.g. `{"name": "My Video Label"}` |

### Success response
```json
{
  "result": {
    "uid": "5c5603a73be349d22fde6362da84f990",
    "readyToStream": false,
    "playback": {
      "hls": "https://videodelivery.net/{uid}/manifest/video.m3u8",
      "dash": "https://videodelivery.net/{uid}/manifest/video.mpd"
    }
  },
  "success": true
}
```

Save the `uid` — that's what you embed.

---

## 3. Python upload script

Downloads from YouTube (or skip if you have MP4s locally) then uploads to Cloudflare Stream.

```python
import subprocess, requests, os, json, sys

ACCOUNT_ID = "7a6e1fad95b03d6e23f9b3542f818c5e"
API_TOKEN  = "cfut_DQMelRTRem8pN6lU09AwrkEeio6rMnxKLHM0RGaj15f87980"
SAVE_DIR   = r"C:\path\to\your\videos"

# Add one entry per video
VIDEOS = [
    {"id": "YOUTUBE_ID_HERE", "name": "video-slug", "label": "Display Name"},
    # ...
]

results = {}
for v in VIDEOS:
    mp4_path = os.path.join(SAVE_DIR, f"{v['name']}.mp4")

    # 1. Download from YouTube (skip if MP4 already exists)
    if not os.path.exists(mp4_path):
        subprocess.run([
            sys.executable, "-m", "yt_dlp",
            "--cookies-from-browser", "firefox",
            "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]",
            "--merge-output-format", "mp4",
            "-o", os.path.join(SAVE_DIR, f"{v['name']}.%(ext)s"),
            "--no-playlist",
            f"https://www.youtube.com/watch?v={v['id']}"
        ])

    # 2. Upload to Cloudflare Stream
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream"
    with open(mp4_path, "rb") as f:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {API_TOKEN}"},
            files={"file": (f"{v['name']}.mp4", f, "video/mp4")},
            data={"meta": json.dumps({"name": v["label"]})}
        )

    if resp.status_code in (200, 201):
        results[v["name"]] = resp.json()["result"]["uid"]
        print(f"OK {v['label']} -> {results[v['name']]}")
    else:
        print(f"ERROR {v['label']}: {resp.text[:200]}")

with open(os.path.join(SAVE_DIR, "cf_video_ids.json"), "w") as f:
    json.dump(results, f, indent=2)

print(json.dumps(results, indent=2))
```

**yt-dlp gotcha:** Chrome 127+ encrypts cookies with DPAPI and can't be extracted. Use `--cookies-from-browser firefox` (log into YouTube in Firefox first, then close Firefox before running).

---

## 4. Embedding options

### Option A: Iframe (desktop, mouse controls)
Simpler, but limited programmatic control.

```html
<iframe
  src="https://iframe.videodelivery.net/{UID}?autoplay=true&controls=true"
  allow="autoplay; encrypted-media; picture-in-picture; fullscreen"
  allowfullscreen
  style="width:100%;height:100%;border:none;">
</iframe>
```

### Option B: Native `<video>` with HLS (mobile, full JS control)
Use this when you need tap-to-pause, custom controls, or programmatic pause/play.

```html
<video
  src="https://videodelivery.net/{UID}/manifest/video.m3u8"
  controls
  playsinline
  style="width:100%;height:100%;object-fit:contain;background:#000;">
</video>
```

HLS works natively in Safari (iOS/macOS) and modern mobile Chrome/Firefox. For older desktop Chrome add `hls.js`.

---

## 5. Full facade pattern (poster → click to play → tap to pause)

This is the pattern used in `mobile.html`. Works on mobile with native tap-to-pause.

### HTML template (per video)
```html
<div class="mv-player" data-video-id="video-slug" data-cf-id="{UID}">
  <span class="mv-badge">LABEL</span>
  <img class="mv-poster" src="poster.webp" alt="">
  <div class="mv-play-overlay" onclick="ytFacadePlay(this)">
    <div class="mv-play-btn">
      <svg class="mv-play-icon" viewBox="0 0 24 24" fill="#fff"><polygon points="6,3 20,12 6,21"/></svg>
      <svg class="mv-pause-icon" viewBox="0 0 24 24" fill="#fff"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>
    </div>
  </div>
</div>
```

### CSS
```css
.mv-player { position: relative; width: 100%; aspect-ratio: 16/9; overflow: hidden; border-radius: 12px; background: #000; }
.mv-poster { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 1; }
.mv-badge  { position: absolute; top: 10px; right: 10px; background: #B22222; color: #fff; padding: 4px 10px; border-radius: 4px; font: 700 12px sans-serif; z-index: 3; }
.mv-play-overlay { position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; z-index: 4; cursor: pointer; }
.mv-play-btn { width: 64px; height: 64px; border-radius: 50%; background: rgba(255,255,255,0.15); backdrop-filter: blur(12px); border: 2px solid rgba(255,255,255,0.3); display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
.mv-play-btn svg { width: 24px; height: 24px; margin-left: 3px; }
.mv-play-overlay .mv-pause-icon { display: none; }
```

### JavaScript
```javascript
(function(){
    // Map your slugs to Cloudflare UIDs
    var CF = {
        'video-slug': '{UID_HERE}',
        // ...
    };

    // Preload (buffers HLS in background, hidden)
    function preload(player){
        if(player.dataset.cfPre) return;
        player.dataset.cfPre = '1';
        var cfId = CF[player.getAttribute('data-video-id')];
        if(!cfId) return;
        var v = document.createElement('video');
        v.src = 'https://videodelivery.net/' + cfId + '/manifest/video.m3u8';
        v.preload = 'auto';
        v.muted = true;
        v.setAttribute('playsinline','');
        v.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:100%;object-fit:contain;background:#000;visibility:hidden;pointer-events:none;';
        player.appendChild(v);
    }

    // Preload first video immediately, others when scrolled near
    var first = document.querySelector('.mv-player');
    if(first) preload(first);
    if(window.IntersectionObserver){
        var io = new IntersectionObserver(function(entries){
            entries.forEach(function(en){
                if(en.isIntersecting){ preload(en.target); io.unobserve(en.target); }
            });
        },{ rootMargin: '500px 0px' });
        document.querySelectorAll('.mv-player[data-cf-id]').forEach(function(p){
            if(p !== first) io.observe(p);
        });
    }

    // Click handler
    window.ytFacadePlay = function(overlay){
        var player = overlay.closest('.mv-player');
        var cfId = CF[player.getAttribute('data-video-id')];
        if(!cfId) return;

        // If already active — toggle play/pause
        var vid = player.querySelector('video[data-mv-active]');
        if(vid){
            if(vid.paused) vid.play();
            else vid.pause();
            return;
        }

        // First click — use preloaded video or create new one
        var video = player.querySelector('video');
        if(!video){
            video = document.createElement('video');
            video.src = 'https://videodelivery.net/' + cfId + '/manifest/video.m3u8';
            video.setAttribute('playsinline','');
            video.style.cssText = 'position:absolute;top:0;left:0;width:100%;height:100%;object-fit:contain;background:#000;';
            player.appendChild(video);
        }
        video.style.visibility = 'visible';
        video.style.pointerEvents = 'auto';
        video.setAttribute('controls','');
        video.setAttribute('data-mv-active','1');
        video.muted = false;
        video.play().catch(function(){ video.muted = true; video.play(); });

        var poster = player.querySelector('.mv-poster');
        if(poster) poster.style.display = 'none';

        // Remove overlay button, leave transparent tap zone above native controls
        var btn = overlay.querySelector('.mv-play-btn');
        if(btn) btn.parentNode.removeChild(btn);
        overlay.style.cssText = 'position:absolute;top:0;left:0;right:0;bottom:44px;z-index:4;cursor:pointer;background:transparent;';

        // Close button (X) — top-right
        var close = document.createElement('button');
        close.innerHTML = '&#x2715;';
        close.style.cssText = 'position:absolute;top:14px;right:14px;z-index:7;background:rgba(0,0,0,0.6);color:#fff;border:none;width:38px;height:38px;border-radius:8px;font-size:17px;cursor:pointer;display:flex;align-items:center;justify-content:center;';
        close.onclick = function(e){
            e.stopPropagation();
            video.pause();
            video.removeAttribute('data-mv-active');
            video.style.visibility = 'hidden';
            video.style.pointerEvents = 'none';
            video.removeAttribute('controls');
            video.muted = true;
            close.remove();
            if(poster) poster.style.display = '';
            overlay.style.cssText = '';
            overlay.innerHTML = '<div class="mv-play-btn"><svg class="mv-play-icon" viewBox="0 0 24 24" fill="#fff"><polygon points="6,3 20,12 6,21"/></svg><svg class="mv-pause-icon" viewBox="0 0 24 24" fill="#fff"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg></div>';
        };
        player.appendChild(close);
    };
})();
```

---

## 6. Checklist for adding videos to a new page

1. Upload the MP4s using the Python script → get back a JSON of `{slug: uid}`
2. Paste the HTML template for each video (set `data-video-id` to your slug)
3. Paste the CSS and JS blocks
4. Update the `CF` map in the JS with your slug → uid pairs
5. Add poster images (optional — for fast first paint)

---

## 7. Useful API calls

### List all videos
```
GET https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream
Authorization: Bearer {API_TOKEN}
```

### Get single video status
```
GET https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream/{UID}
```
Poll until `result.readyToStream === true` before embedding.

### Delete a video
```
DELETE https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/stream/{UID}
```

---

## 8. Current KetoWater video UIDs (reference)

```json
{
  "kw-hook":     "5c5603a73be349d22fde6362da84f990",
  "kw-fat":      "9b35659e9351467763e19c7fff20e7d0",
  "kw-bride":    "23cbe4e0992eab5539ff7fd612ed6249",
  "kw-linda":    "ff558f06164938f05db807e7d13f6edd",
  "kw-patricia": "b6b811754ce000b44892f28c880fbc2e",
  "kw-sean":     "38c685f1ba26383bc32342bf8f78bd4d",
  "kw-eat":      "690e26e54ea5e2b5682e6def78140067"
}
```
