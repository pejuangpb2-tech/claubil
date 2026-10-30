#!/usr/bin/env python3
"""Generate a video clip with Google Veo through the Gemini API.

Usage:
    python3 tools/veo.py prompts/shot1.txt assets/shot1.mp4

Reads the API key from GEMINI_API_KEY (or GOOGLE_API_KEY). Picks the newest Veo
model the key can use, submits the prompt, waits for the job and downloads the MP4.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

API = "https://generativelanguage.googleapis.com/v1beta"
PREFERRED = ["veo-3.1-generate-preview", "veo-3.0-generate-001", "veo-3.0-generate-preview", "veo-2.0-generate-001"]
NEGATIVE = "text, subtitles, captions, watermark, logo, distorted faces, extra fingers, deformed hands, cartoon, 3d render"


def call(method, url, key, body=None):
    req = urllib.request.Request(url, method=method, headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    data = json.dumps(body).encode() if body is not None else None
    try:
        with urllib.request.urlopen(req, data=data, timeout=120) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"{method} {url.split('?')[0]} failed: {e.code} {e.read().decode()[:600]}")


def pick_model(key):
    models, token = [], ""
    while True:
        page = call("GET", f"{API}/models?pageSize=200" + (f"&pageToken={token}" if token else ""), key)
        models += [m["name"].split("/")[-1] for m in page.get("models", []) if "predictLongRunning" in m.get("supportedGenerationMethods", [])]
        token = page.get("nextPageToken")
        if not token:
            break
    veo = [m for m in models if m.startswith("veo")]
    for name in PREFERRED:
        if name in veo:
            return name
    if not veo:
        sys.exit("This API key has no Veo model available.")
    return sorted(veo)[-1]


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    prompt_file, out = sys.argv[1], sys.argv[2]
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit("Set GEMINI_API_KEY in the environment first.")
    prompt = open(prompt_file).read().strip()
    model = os.environ.get("VEO_MODEL") or pick_model(key)
    print(f"model: {model}")
    params = {"aspectRatio": "16:9", "negativePrompt": NEGATIVE}
    if model.startswith("veo-3"):
        params["resolution"] = "1080p"
    op = call("POST", f"{API}/models/{model}:predictLongRunning", key, {"instances": [{"prompt": prompt}], "parameters": params})
    name = op["name"]
    print(f"operation: {name}")
    started = time.time()
    while not op.get("done"):
        time.sleep(10)
        op = call("GET", f"{API}/{name}", key)
        print(f"  waiting... {int(time.time() - started)}s", flush=True)
    if "error" in op:
        sys.exit(f"Veo error: {json.dumps(op['error'])}")
    samples = op["response"]["generateVideoResponse"].get("generatedSamples") or []
    if not samples:
        sys.exit(f"No video returned (possibly filtered): {json.dumps(op['response'])[:600]}")
    uri = samples[0]["video"]["uri"]
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    req = urllib.request.Request(uri, headers={"x-goog-api-key": key})
    with urllib.request.urlopen(req, timeout=300) as r, open(out, "wb") as f:
        f.write(r.read())
    print(f"saved {out}")


if __name__ == "__main__":
    main()
