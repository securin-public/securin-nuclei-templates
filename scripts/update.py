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
WEBSITE = "https://www.securin.io"


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


SEVERITY_BADGE = {"critical": "critical-8B0000", "high": "high-E05D44",
                  "medium": "medium-DFB317", "low": "low-4C9A2A", "info": "info-5B8DEF",
                  "unknown": "unknown-9F9F9F"}


def badge(label, message, color, link=None):
    q = lambda v: urllib.parse.quote(str(v).replace("-", "--"), safe="")
    img = f"https://img.shields.io/badge/{q(label)}-{q(message)}-{color}?style=flat-square"
    tag = f'<img alt="{label}" src="{img}">'
    return f'<a href="{link}">{tag}</a>' if link else tag


def sev_badge(sev):
    name, color = SEVERITY_BADGE.get(sev, SEVERITY_BADGE["unknown"]).rsplit("-", 1)
    return f"![{name}](https://img.shields.io/badge/-{name}-{color}?style=flat-square)"


def render_readme(prs, templates, generated):
    states = Counter(p["state"] for p in prs)
    severities = Counter(t["severity"] for t in templates)
    years = Counter(cve_year(t["id"]) for t in templates)

    parts = [
        '<p align="center">',
        f'  <a href="{WEBSITE}">',
        "    <picture>",
        '      <source media="(prefers-color-scheme: dark)" srcset="assets/securin-logo-dark.png">',
        '      <img alt="Securin" src="assets/securin-logo-light.png" width="320">',
        "    </picture>",
        "  </a>",
        "</p>",
        "",
        '<h1 align="center">Securin Nuclei Templates</h1>',
        "",
        '<p align="center">',
        "  Lab-validated <a href=\"https://github.com/projectdiscovery/nuclei\">Nuclei</a> "
        "detection templates authored by <a href=\"" + WEBSITE + "\">Securin</a> "
        "and merged into the official ProjectDiscovery template library.",
        "</p>",
        "",
        '<p align="center">',
        "  " + " ".join([
            badge("templates merged", len(templates), "7F30FF", f"#templates"),
            badge("critical", severities["critical"], "8B0000"),
            badge("in review", states["open"], "9C66FF", "#in-review"),
            badge("upstream", "nuclei-templates", "181717", f"https://github.com/{UPSTREAM}"),
            badge("website", "securin.io", "7F30FF", WEBSITE),
        ]),
        "</p>",
        "",
        "---",
        "",
        "## About",
        "",
        f"[Securin]({WEBSITE}) researches exploitable vulnerabilities and contributes "
        f"detections back to the community through [`{UPSTREAM}`](https://github.com/{UPSTREAM}). "
        "Every template in this repository has been reviewed and accepted by the ProjectDiscovery "
        "maintainers, and favours active proof of exploitability (command output, retrieved file "
        "content, unauthenticated access to protected resources) over version banners.",
        "",
        "This repository is a curated record of those contributions. Each file is an exact copy "
        "of the template as it exists on upstream `main`, so it stays in step with maintainer "
        "edits and metadata refreshes.",
        "",
        "## Highlights",
        "",
        table(["Metric", "Value"], [
            ["Templates merged upstream", f"**{len(templates)}**"],
            ["Critical / High severity",
             f"{severities['critical']} / {severities['high']}"],
            ["CVE years covered",
             f"{min(y for y in years if y != 'non-CVE')}–{max(y for y in years if y != 'non-CVE')}"
             if any(y != "non-CVE" for y in years) else "n/a"],
            ["Pull requests in review", states["open"]],
        ]),
        "",
        "## Templates",
        "",
        table(
            ["CVE", "Title", "Severity", "CVSS", "Merged", "Upstream PR"],
            [[f"[**{t['id']}**]({t['path']})", t["name"].replace("|", "\\|"),
              sev_badge(t["severity"]),
              t["cvss"] if t["cvss"] is not None else "–", t["merged"],
              f"[#{t['pr']}](https://github.com/{UPSTREAM}/pull/{t['pr']})"]
             for t in reversed(templates)],
        ),
    ]

    open_prs = [p for p in prs if p["state"] == "open"]
    if open_prs:
        parts += ["", "## In review", "",
                  "Submitted upstream and awaiting maintainer review.", "",
                  table(["Pull request", "Title", "Submitted"],
                        [[f"[#{p['number']}]({p['url']})",
                          p["title"].removeprefix("Add ").replace("|", "\\|"), p["opened"]]
                         for p in open_prs])]

    parts += [
        "",
        "## Usage",
        "",
        "Install [Nuclei](https://github.com/projectdiscovery/nuclei) and run any template "
        "against a target you are **authorized** to test:",
        "",
        "```sh",
        "# single template",
        "nuclei -u https://target.example -t templates/2026/2026-10-28/CVE-2026-24898.yaml",
        "",
        "# every Securin template",
        "nuclei -l targets.txt -t templates/",
        "```",
        "",
        "The same templates ship with the official library, so `nuclei -update-templates` "
        "followed by `nuclei -id <CVE-ID>` works as well.",
        "",
        "## Repository layout",
        "",
        "```",
        "templates/<year>/<merge-date>/<CVE-ID>.yaml   exact copies from upstream main",
        "data/contributions.json                       machine-readable index",
        "scripts/update.py                             regenerates templates, data and this README",
        "```",
        "",
        "## Responsible use",
        "",
        "These templates are provided for defensive security, vulnerability management and "
        "authorized testing only. Do not scan systems without explicit permission from their owner.",
        "",
        "## License",
        "",
        "Templates are distributed under the [MIT License](LICENSE), as published in "
        f"[`{UPSTREAM}`](https://github.com/{UPSTREAM}).",
        "",
        "---",
        "",
        f'<p align="center"><sub>Maintained by <a href="{WEBSITE}">Securin</a> · '
        f"Last synced {generated}</sub></p>",
        "",
    ]
    return "\n".join(parts)


def main():
    prs, templates = collect()
    write_templates(templates)
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(
        {"generated": generated, "upstream": UPSTREAM, "templates": templates,
         "pull_requests": [p for p in prs if p["state"] in ("merged", "open")]},
        indent=2) + "\n")
    README.write_text(render_readme(prs, templates, generated))
    print(f"{len(templates)} templates, {len(prs)} PRs")


if __name__ == "__main__":
    main()
