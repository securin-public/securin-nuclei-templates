#!/usr/bin/env python3
"""Sync Securin templates merged into projectdiscovery/nuclei-templates.

Finds every PR opened by the contributor accounts, copies each template file
the PR added (as it exists on upstream main today) into
templates/<YYYY>/<YYYY-MM-DD>/ keyed by merge date, then regenerates
data/contributions.json and README.md.

Usage:
    GH_TOKEN=$(gh auth token -u ArjunSecurin) python3 scripts/update.py
"""

import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml

UPSTREAM = "projectdiscovery/nuclei-templates"
CONTRIBUTORS = ["ArjunSecurin"]
AUTHOR_TAG = "securin"
TEMPLATE_EXT = (".yaml", ".yml")
SEVERITY_ORDER = ["critical", "high", "medium", "low", "info", "unknown"]

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"
DATA_FILE = ROOT / "data" / "contributions.json"
README = ROOT / "README.md"


def token():
    tok = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if tok:
        return tok
    try:
        return subprocess.check_output(
            ["gh", "auth", "token", "-u", CONTRIBUTORS[0]], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        sys.exit("No GitHub token: set GH_TOKEN or log in with `gh auth login`.")


TOKEN = token()


def api(path, params=None, raw=False):
    url = f"https://api.github.com/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(req) as resp:
        body = resp.read()
    return body.decode() if raw else json.loads(body)


def search_prs(author):
    prs, page = [], 1
    while True:
        res = api("search/issues", {
            "q": f"repo:{UPSTREAM} is:pr author:{author}",
            "per_page": 100, "page": page,
        })
        prs += res["items"]
        if len(prs) >= res["total_count"] or not res["items"]:
            return prs
        page += 1


def pr_files(number):
    files, page = [], 1
    while True:
        batch = api(f"repos/{UPSTREAM}/pulls/{number}/files", {"per_page": 100, "page": page})
        files += batch
        if len(batch) < 100:
            return files
        page += 1


def upstream_file(path):
    try:
        return api(f"repos/{UPSTREAM}/contents/{urllib.parse.quote(path)}", {"ref": "main"}, raw=True)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def collect():
    prs = {}
    for author in CONTRIBUTORS:
        for item in search_prs(author):
            prs[item["number"]] = item

    pr_records, templates = [], []
    for number in sorted(prs):
        item = prs[number]
        pr = api(f"repos/{UPSTREAM}/pulls/{number}")
        state = "merged" if pr["merged_at"] else pr["state"]
        pr_records.append({
            "number": number,
            "title": pr["title"],
            "state": state,
            "opened": pr["created_at"][:10],
            "closed": (pr["merged_at"] or pr["closed_at"] or "")[:10] or None,
            "url": pr["html_url"],
        })
        if state != "merged":
            continue

        for f in pr_files(number):
            path = f["filename"]
            if f["status"] != "added" or not path.endswith(TEMPLATE_EXT):
                continue
            content = upstream_file(path)
            if content is None:
                print(f"  skip {path}: no longer on upstream main", file=sys.stderr)
                continue
            info = (yaml.safe_load(content) or {}).get("info", {})
            author_field = str(info.get("author", ""))
            if AUTHOR_TAG not in author_field.lower():
                print(f"  skip {path}: author is '{author_field}'", file=sys.stderr)
                continue
            cls = info.get("classification") or {}
            meta = info.get("metadata") or {}
            templates.append({
                "id": Path(path).stem,
                "name": info.get("name", ""),
                "author": author_field,
                "severity": str(info.get("severity", "unknown")).lower(),
                "cvss": cls.get("cvss-score"),
                "cwe": cls.get("cwe-id"),
                "vendor": meta.get("vendor"),
                "product": meta.get("product"),
                "upstream_path": path,
                "pr": number,
                "submitted": pr["created_at"][:10],
                "merged": pr["merged_at"][:10],
                "_content": content,
            })

    templates.sort(key=lambda t: (t["merged"], t["id"]))
    return pr_records, templates


def write_templates(templates):
    if TEMPLATES_DIR.exists():
        shutil.rmtree(TEMPLATES_DIR)
    for t in templates:
        day = t["merged"]
        dest = TEMPLATES_DIR / day[:4] / day / Path(t["upstream_path"]).name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(t.pop("_content"))
        t["path"] = dest.relative_to(ROOT).as_posix()


def cve_year(template_id):
    parts = template_id.split("-")
    return parts[1] if len(parts) > 2 and parts[0].upper() == "CVE" else "non-CVE"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def render_readme(prs, templates, generated):
    states = Counter(p["state"] for p in prs)
    decided = states["merged"] + states["closed"]
    rate = f"{states['merged'] / decided:.0%}" if decided else "n/a"
    severities = Counter(t["severity"] for t in templates)
    years = Counter(cve_year(t["id"]) for t in templates)
    months = Counter(t["merged"][:7] for t in templates)

    parts = [
        "# Securin nuclei templates",
        "",
        f"Templates authored by Securin Labs and merged into "
        f"[`{UPSTREAM}`](https://github.com/{UPSTREAM}). Each file is an exact copy of the "
        "template on upstream `main`, stored under `templates/<year>/<merge-date>/`.",
        "",
        f"_Last updated: {generated}_",
        "",
        "## Summary",
        "",
        table(["Metric", "Count"], [
            ["Templates merged", len(templates)],
            ["PRs merged", states["merged"]],
            ["PRs open", states["open"]],
            ["PRs closed without merge", states["closed"]],
            ["Merge rate (merged / decided PRs)", rate],
        ]),
        "",
        "## By severity",
        "",
        table(["Severity", "Templates"],
              [[s, severities[s]] for s in SEVERITY_ORDER if severities[s]]),
        "",
        "## By CVE year",
        "",
        table(["CVE year", "Templates"], sorted(years.items())),
        "",
        "## By merge month",
        "",
        table(["Month", "Templates"], sorted(months.items())),
        "",
        "## Templates",
        "",
        table(
            ["Template", "Name", "Severity", "CVSS", "Merged", "PR"],
            [[f"[{t['id']}]({t['path']})", t["name"].replace("|", "\\|"), t["severity"],
              t["cvss"] if t["cvss"] is not None else "", t["merged"],
              f"[#{t['pr']}](https://github.com/{UPSTREAM}/pull/{t['pr']})"]
             for t in reversed(templates)],
        ),
    ]

    open_prs = [p for p in prs if p["state"] == "open"]
    if open_prs:
        parts += ["", "## Open PRs", "",
                  table(["PR", "Title", "Opened"],
                        [[f"[#{p['number']}]({p['url']})", p["title"].replace("|", "\\|"), p["opened"]]
                         for p in open_prs])]

    parts += ["", "## Updating", "",
              "```sh",
              "GH_TOKEN=$(gh auth token -u ArjunSecurin) python3 scripts/update.py",
              "```",
              "",
              "The script rebuilds `templates/`, `data/contributions.json` and this README "
              "from the GitHub API. Do not edit them by hand.", ""]
    return "\n".join(parts)


def main():
    prs, templates = collect()
    write_templates(templates)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(
        {"generated": generated, "upstream": UPSTREAM, "templates": templates, "pull_requests": prs},
        indent=2) + "\n")
    README.write_text(render_readme(prs, templates, generated))
    print(f"{len(templates)} templates, {len(prs)} PRs")


if __name__ == "__main__":
    main()
