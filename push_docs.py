#!/usr/bin/env python3
"""GitHub API push for PainMatrix README documentation update."""
import os, json, base64, urllib.request, urllib.parse

REPO = "Macau007/painmatrix"
TOKEN = "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"
BRANCH = "master"

def api(method, path, data=None):
    url = f"https://api.github.com/{path}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "PainMatrix-Push/1.0"
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def get_file(path):
    try:
        return api("GET", f"repos/{REPO}/contents/{path}?ref={BRANCH}")
    except Exception:
        return None

def push_file(path, content, sha=None):
    data = {
        "message": f"docs: rewrite README with deep feature analysis",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": BRANCH
    }
    if sha:
        data["sha"] = sha
    return api("PUT", f"repos/{REPO}/contents/{path}", data)

files = [
    ("README.md", open("README.md", "r", encoding="utf-8").read()),
    ("README_CN.md", open("README_CN.md", "r", encoding="utf-8").read()),
    ("docs/README_EN.md", open("docs/README_EN.md", "r", encoding="utf-8").read()),
    ("docs/README_CN.md", open("docs/README_CN.md", "r", encoding="utf-8").read()),
]

for path, content in files:
    existing = get_file(path)
    sha = existing["sha"] if existing else None
    result = push_file(path, content, sha)
    print(f"✓ {path}" if result.get("commit") else f"✗ {path}: {result}")

print("\nDone!")
