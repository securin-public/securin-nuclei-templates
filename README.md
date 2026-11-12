<p align="center">
  <a href="https://www.securin.io">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/securin-logo-dark.png">
      <img alt="Securin" src="assets/securin-logo-light.png" width="320">
    </picture>
  </a>
</p>

<h1 align="center">Securin Nuclei Templates</h1>

<p align="center">
  Lab-validated <a href="https://github.com/projectdiscovery/nuclei">Nuclei</a> detection templates authored by <a href="https://www.securin.io">Securin</a> and merged into the official ProjectDiscovery template library.
</p>

<p align="center">
  <a href="#templates"><img alt="templates merged" src="https://img.shields.io/badge/templates%20merged-9-7F30FF?style=flat-square"></a> <img alt="critical" src="https://img.shields.io/badge/critical-7-8B0000?style=flat-square"> <a href="#in-review"><img alt="in review" src="https://img.shields.io/badge/in%20review-3-9C66FF?style=flat-square"></a> <a href="https://github.com/projectdiscovery/nuclei-templates"><img alt="upstream" src="https://img.shields.io/badge/upstream-nuclei--templates-181717?style=flat-square"></a> <a href="https://www.securin.io"><img alt="website" src="https://img.shields.io/badge/website-securin.io-7F30FF?style=flat-square"></a>
</p>

---

## About

[Securin](https://www.securin.io) researches exploitable vulnerabilities and contributes detections back to the community through [`projectdiscovery/nuclei-templates`](https://github.com/projectdiscovery/nuclei-templates). Every template in this repository has been reviewed and accepted by the ProjectDiscovery maintainers, and favours active proof of exploitability (command output, retrieved file content, unauthenticated access to protected resources) over version banners.

This repository is a curated record of those contributions. Each file is an exact copy of the template as it exists on upstream `main`, so it stays in step with maintainer edits and metadata refreshes.

## Highlights

| Metric | Value |
|---|---|
| Templates merged upstream | **9** |
| Critical / High severity | 7 / 2 |
| CVE years covered | 2010–2026 |
| Pull requests in review | 3 |

## Templates

| CVE | Title | Severity | CVSS | Merged | Upstream PR |
|---|---|---|---|---|---|
| [**CVE-2023-54335**](templates/2026/2026-10-29/CVE-2023-54335.yaml) | eXtplorer <= 2.1.14 - Authentication Bypass | ![critical](https://img.shields.io/badge/-critical-8B0000?style=flat-square) | 9.8 | 2026-10-29 | [#17587](https://github.com/projectdiscovery/nuclei-templates/pull/17587) |
| [**CVE-2023-31719**](templates/2026/2026-10-29/CVE-2023-31719.yaml) | FUXA <= 1.1.12 - Unauthenticated SQL Injection | ![critical](https://img.shields.io/badge/-critical-8B0000?style=flat-square) | 9.8 | 2026-10-29 | [#17588](https://github.com/projectdiscovery/nuclei-templates/pull/17588) |
| [**CVE-2026-24898**](templates/2026/2026-10-28/CVE-2026-24898.yaml) | OpenEMR < 8.0.0 - MedEx Callback Unauthenticated Token Disclosure | ![critical](https://img.shields.io/badge/-critical-8B0000?style=flat-square) | 10 | 2026-10-28 | [#17589](https://github.com/projectdiscovery/nuclei-templates/pull/17589) |
| [**CVE-2010-1428**](templates/2026/2026-10-25/CVE-2010-1428.yaml) | Red Hat JBoss - Web/JMX Console Access | ![high](https://img.shields.io/badge/-high-E05D44?style=flat-square) | 7.5 | 2026-10-25 | [#17340](https://github.com/projectdiscovery/nuclei-templates/pull/17340) |
| [**CVE-2026-85714**](templates/2026/2026-10-22/CVE-2026-85714.yaml) | Stirling PDF <= 2.13.1 - H2 Database Import Remote Code Execution | ![critical](https://img.shields.io/badge/-critical-8B0000?style=flat-square) | 9.1 | 2026-10-22 | [#17383](https://github.com/projectdiscovery/nuclei-templates/pull/17383) |
| [**CVE-2010-0738**](templates/2026/2026-10-15/CVE-2010-0738.yaml) | JBoss JMX/Web Console - Authentication Bypass via HTTP Verb Tampering | ![critical](https://img.shields.io/badge/-critical-8B0000?style=flat-square) | 9.8 | 2026-10-15 | [#17330](https://github.com/projectdiscovery/nuclei-templates/pull/17330) |
| [**CVE-2020-10221**](templates/2026/2026-08-25/CVE-2020-10221.yaml) | rConfig <= 3.9.4 - Authenticated OS Command Injection | ![high](https://img.shields.io/badge/-high-E05D44?style=flat-square) | 8.8 | 2026-08-25 | [#16567](https://github.com/projectdiscovery/nuclei-templates/pull/16567) |
| [**CVE-2019-11043**](templates/2026/2026-08-25/CVE-2019-11043.yaml) | PHP-FPM Path Info Buffer Underflow - Remote Code Execution | ![critical](https://img.shields.io/badge/-critical-8B0000?style=flat-square) | 9.8 | 2026-08-25 | [#16567](https://github.com/projectdiscovery/nuclei-templates/pull/16567) |
| [**CVE-2017-7504**](templates/2026/2026-08-25/CVE-2017-7504.yaml) | JBossMQ HTTP Invocation Layer (HTTPServerILServlet) - Unauthenticated Java Deserialization | ![critical](https://img.shields.io/badge/-critical-8B0000?style=flat-square) | 9.8 | 2026-08-25 | [#16567](https://github.com/projectdiscovery/nuclei-templates/pull/16567) |

## In review

Submitted upstream and awaiting maintainer review.

| Pull request | Title | Submitted |
|---|---|---|
| [#17590](https://github.com/projectdiscovery/nuclei-templates/pull/17590) | CVE-2025-50201 - WeGIA < 3.4.2 - Unauthenticated OS Command Injection | 2026-10-27 |
| [#17607](https://github.com/projectdiscovery/nuclei-templates/pull/17607) | CVE-2019-1003005 - Jenkins Script Security Plugin <=1.50 - Sandbox Bypass via AST Transforms | 2026-10-30 |
| [#17782](https://github.com/projectdiscovery/nuclei-templates/pull/17782) | CVE-2026-48356 - Adobe Commerce/Magento <= 2.4.8-p5 - Unauthenticated Arbitrary File Upload | 2026-11-12 |

## Usage

Install [Nuclei](https://github.com/projectdiscovery/nuclei) and run any template against a target you are **authorized** to test:

```sh
# single template
nuclei -u https://target.example -t templates/2026/2026-10-28/CVE-2026-24898.yaml

# every Securin template
nuclei -l targets.txt -t templates/
```

The same templates ship with the official library, so `nuclei -update-templates` followed by `nuclei -id <CVE-ID>` works as well.

## Repository layout

```
templates/<year>/<merge-date>/<CVE-ID>.yaml   exact copies from upstream main
data/contributions.json                       machine-readable index
scripts/update.py                             regenerates templates, data and this README
```

## Responsible use

These templates are provided for defensive security, vulnerability management and authorized testing only. Do not scan systems without explicit permission from their owner.

## License

Templates are distributed under the [MIT License](LICENSE), as published in [`projectdiscovery/nuclei-templates`](https://github.com/projectdiscovery/nuclei-templates).

---

<p align="center"><sub>Maintained by <a href="https://www.securin.io">Securin</a> · Last synced 2026-11-12 05:27 UTC</sub></p>
