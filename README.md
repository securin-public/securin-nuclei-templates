# Securin nuclei templates

Templates authored by Securin Labs and merged into [`projectdiscovery/nuclei-templates`](https://github.com/projectdiscovery/nuclei-templates). Each file is an exact copy of the template on upstream `main`, stored under `templates/<year>/<merge-date>/`.

_Last updated: 2026-10-23 01:58 UTC_

## Summary

| Metric | Count |
|---|---|
| Templates merged | 5 |
| PRs merged | 4 |
| PRs open | 1 |
| PRs closed without merge | 13 |
| Merge rate (merged / decided PRs) | 24% |

## By severity

| Severity | Templates |
|---|---|
| critical | 4 |
| high | 1 |

## By CVE year

| CVE year | Templates |
|---|---|
| 2010 | 1 |
| 2017 | 1 |
| 2019 | 1 |
| 2020 | 1 |
| 2026 | 1 |

## By merge month

| Month | Templates |
|---|---|
| 2026-08 | 3 |
| 2026-10 | 2 |

## Templates

| Template | Name | Severity | CVSS | Merged | PR |
|---|---|---|---|---|---|
| [CVE-2026-85714](templates/2026/2026-10-22/CVE-2026-85714.yaml) | Stirling PDF <= 2.13.1 - H2 Database Import Remote Code Execution | critical | 9.1 | 2026-10-22 | [#17383](https://github.com/projectdiscovery/nuclei-templates/pull/17383) |
| [CVE-2010-0738](templates/2026/2026-10-15/CVE-2010-0738.yaml) | JBoss JMX/Web Console - Authentication Bypass via HTTP Verb Tampering | critical | 9.8 | 2026-10-15 | [#17330](https://github.com/projectdiscovery/nuclei-templates/pull/17330) |
| [CVE-2020-10221](templates/2026/2026-08-25/CVE-2020-10221.yaml) | rConfig <= 3.9.4 - Authenticated OS Command Injection | high | 8.8 | 2026-08-25 | [#16567](https://github.com/projectdiscovery/nuclei-templates/pull/16567) |
| [CVE-2019-11043](templates/2026/2026-08-25/CVE-2019-11043.yaml) | PHP-FPM Path Info Buffer Underflow - Remote Code Execution | critical | 9.8 | 2026-08-25 | [#16567](https://github.com/projectdiscovery/nuclei-templates/pull/16567) |
| [CVE-2017-7504](templates/2026/2026-08-25/CVE-2017-7504.yaml) | JBossMQ HTTP Invocation Layer (HTTPServerILServlet) - Unauthenticated Java Deserialization | critical | 9.8 | 2026-08-25 | [#16567](https://github.com/projectdiscovery/nuclei-templates/pull/16567) |

## Open PRs

| PR | Title | Opened |
|---|---|---|
| [#17340](https://github.com/projectdiscovery/nuclei-templates/pull/17340) | Add CVE-2010-1428 (Red Hat JBoss unauthenticated Web/JMX console access) | 2026-09-29 |

## Updating

```sh
GH_TOKEN=$(gh auth token -u ArjunSecurin) python3 scripts/update.py
```

The script rebuilds `templates/`, `data/contributions.json` and this README from the GitHub API. Do not edit them by hand.
