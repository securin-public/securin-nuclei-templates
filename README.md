# Securin nuclei templates

Templates authored by Securin Labs and merged into [`projectdiscovery/nuclei-templates`](https://github.com/projectdiscovery/nuclei-templates). Each file is an exact copy of the template on upstream `main`, stored under `templates/<year>/<merge-date>/`.

_Last updated: 2026-10-27 08:17 UTC_

## Summary

| Metric | Count |
|---|---|
| Templates merged | 6 |
| PRs merged | 5 |
| PRs open | 4 |
| PRs closed without merge | 13 |
| Merge rate (merged / decided PRs) | 28% |

## By severity

| Severity | Templates |
|---|---|
| critical | 4 |
| high | 2 |

## By CVE year

| CVE year | Templates |
|---|---|
| 2010 | 2 |
| 2017 | 1 |
| 2019 | 1 |
| 2020 | 1 |
| 2026 | 1 |

## By merge month

| Month | Templates |
|---|---|
| 2026-08 | 3 |
| 2026-10 | 3 |

## Templates

| Template | Name | Severity | CVSS | Merged | PR |
|---|---|---|---|---|---|
| [CVE-2010-1428](templates/2026/2026-10-25/CVE-2010-1428.yaml) | Red Hat JBoss - Web/JMX Console Access | high | 7.5 | 2026-10-25 | [#17340](https://github.com/projectdiscovery/nuclei-templates/pull/17340) |
| [CVE-2026-85714](templates/2026/2026-10-22/CVE-2026-85714.yaml) | Stirling PDF <= 2.13.1 - H2 Database Import Remote Code Execution | critical | 9.1 | 2026-10-22 | [#17383](https://github.com/projectdiscovery/nuclei-templates/pull/17383) |
| [CVE-2010-0738](templates/2026/2026-10-15/CVE-2010-0738.yaml) | JBoss JMX/Web Console - Authentication Bypass via HTTP Verb Tampering | critical | 9.8 | 2026-10-15 | [#17330](https://github.com/projectdiscovery/nuclei-templates/pull/17330) |
| [CVE-2020-10221](templates/2026/2026-08-25/CVE-2020-10221.yaml) | rConfig <= 3.9.4 - Authenticated OS Command Injection | high | 8.8 | 2026-08-25 | [#16567](https://github.com/projectdiscovery/nuclei-templates/pull/16567) |
| [CVE-2019-11043](templates/2026/2026-08-25/CVE-2019-11043.yaml) | PHP-FPM Path Info Buffer Underflow - Remote Code Execution | critical | 9.8 | 2026-08-25 | [#16567](https://github.com/projectdiscovery/nuclei-templates/pull/16567) |
| [CVE-2017-7504](templates/2026/2026-08-25/CVE-2017-7504.yaml) | JBossMQ HTTP Invocation Layer (HTTPServerILServlet) - Unauthenticated Java Deserialization | critical | 9.8 | 2026-08-25 | [#16567](https://github.com/projectdiscovery/nuclei-templates/pull/16567) |

## Open PRs

| PR | Title | Opened |
|---|---|---|
| [#17587](https://github.com/projectdiscovery/nuclei-templates/pull/17587) | Add CVE-2023-54335 - eXtplorer <= 2.1.14 - Authentication Bypass | 2026-10-27 |
| [#17588](https://github.com/projectdiscovery/nuclei-templates/pull/17588) | Add CVE-2023-31719 - FUXA < 1.2.4 - Unauthenticated SQL Injection | 2026-10-27 |
| [#17589](https://github.com/projectdiscovery/nuclei-templates/pull/17589) | Add CVE-2026-24898 - OpenEMR < 8.0.0 - MedEx Callback Unauthenticated Token Disclosure | 2026-10-27 |
| [#17590](https://github.com/projectdiscovery/nuclei-templates/pull/17590) | Add CVE-2025-50201 - WeGIA < 3.4.2 - Unauthenticated OS Command Injection | 2026-10-27 |

## Updating

```sh
GH_TOKEN=$(gh auth token -u ArjunSecurin) python3 scripts/update.py
```

The script rebuilds `templates/`, `data/contributions.json` and this README from the GitHub API. Do not edit them by hand.
