<div align="center">

<img src="assets/header.svg" alt="Gabriel Castillo — Backend and Integration Engineer. Stickers: systems that talk (banks, invoicing, CRMs), bugs traced to the root, busywork turned into internal tools, bank messages translated from SWIFT to ISO 20022." width="100%"/>

<br/>

[![Portfolio](https://img.shields.io/badge/Portfolio-gabo8191.github.io-0D0D0D?style=for-the-badge&labelColor=FFD93D)](https://gabo8191.github.io/portfolio/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-gabodev8191-0D0D0D?style=for-the-badge&labelColor=FF6FB5)](https://linkedin.com/in/gabodev8191)
[![Email](https://img.shields.io/badge/Email-gabo8191@gmail.com-0D0D0D?style=for-the-badge&labelColor=FFFDF5)](mailto:gabo8191@gmail.com)

</div>

<h2><img src="assets/section-about.svg" alt="01 / About — What I do" width="100%"/></h2>

I build backend systems and integrations and diagnose production incidents. I have over three years of remote experience with APIs, SQL, queues, financial messaging, electronic invoicing and internal tools using Python/Django, NestJS, Laravel and Java.

I like the difficult part of a system: following a record, message or transaction through SQL, logs and code until the failure is clear, then turning the finding into a fix the team can maintain.

| System integrations | Production support | Internal tools |
|---|---|---|
| SWIFT MT and ISO 20022 messaging, electronic invoicing connectors and data workflows between systems. | L2/L3 incidents traced through SQL, logs and code, with a written root cause. | Estimation tools, inventory platforms, reports, queued exports and admin panels. |

> Kubernetes, Terraform and observability are areas I practice in personal projects; I do not present them as employer-operated production infrastructure.

<h2><img src="assets/section-stack.svg" alt="02 / Stack — Tools I use" width="100%"/></h2>

<img src="assets/stack.svg" alt="Languages: Python, TypeScript, PHP, Java, SQL. Backend: Django, DRF, Celery, NestJS, Laravel, Filament, Apache Camel, REST, OpenAPI. Data: PostgreSQL, MySQL, Oracle PL/SQL, Redis, pandas, Excel, Power BI, Tableau. Operations: L2/L3 diagnosis, Sentry, Docker, Portainer, GitHub Actions, Linux." width="100%"/>

<h2><img src="assets/section-open-source.svg" alt="03 / Open source — Built in the open" width="100%"/></h2>

<table>
<tr>
<td width="50%" valign="top">

### [TomoReader](https://github.com/gabo8191/TomoReader)

Desktop comic and manga reader (**CBR/CBZ**) built with **Rust + Tauri 2** and React. Eye-friendly reading themes, reading-progress tracking and a SQLite-backed library.

`Rust` `Tauri` `React` `TypeScript` `SQLite`

[![Repo](https://img.shields.io/badge/View_repo-→-0D0D0D?style=flat-square&labelColor=FFD93D)](https://github.com/gabo8191/TomoReader)

</td>
<td width="50%" valign="top">

### [AutoTranslate-Anki](https://github.com/gabo8191/AutoTranslate-Anki)

**Anki** add-on that fills note translations for a whole deck in one click. Built in **Python**, no API key required, with configurable language pairs and field mapping.

`Python` `Anki` `Add-on`

[![Repo](https://img.shields.io/badge/View_repo-→-0D0D0D?style=flat-square&labelColor=FF6FB5)](https://github.com/gabo8191/AutoTranslate-Anki)

</td>
</tr>
</table>

<h2><img src="assets/section-live.svg" alt="04 / Live — Live projects" width="100%"/></h2>

<table>
<tr>
<td width="50%" valign="top">

### [Cadáver Exquisito](https://cadaver-exquisito-six.vercel.app/)

Serverless multiplayer web app for collective storytelling. A group builds a story in turns with **no backend**: the host's browser runs the authoritative engine over **WebRTC** (PeerJS), and all state persists locally in **IndexedDB**. Nobody sees what others wrote until the final reveal.

`TypeScript` `React` `Vite` `WebRTC` `IndexedDB`

[![Live demo](https://img.shields.io/badge/Live_demo-→-0D0D0D?style=flat-square&labelColor=FFD93D)](https://cadaver-exquisito-six.vercel.app/)

</td>
<td width="50%" valign="top">

### [NeuroSess](https://neurosess.netlify.app/)

Recording and transcription app for neuropsychology sessions, where the audio never leaves the consulting room. A static **Next.js** frontend talks over loopback to a **local Python engine** (FastAPI + **faster-whisper**, shipped as a **PyInstaller** binary for Windows and Linux), the only piece that runs inference and writes to disk.

`TypeScript` `Next.js` `Python` `FastAPI` `faster-whisper` `IndexedDB`

[![Live demo](https://img.shields.io/badge/Live_demo-→-0D0D0D?style=flat-square&labelColor=FF6FB5)](https://neurosess.netlify.app/)
[![Engine](https://img.shields.io/badge/Local_engine-→-0D0D0D?style=flat-square&labelColor=FFFDF5)](https://github.com/gabo8191/neurosess-engine)

</td>
</tr>
</table>

<h2><img src="assets/section-experience.svg" alt="05 / Experience — Where I worked" width="100%"/></h2>

<details open>
<summary><b>Keyrus Colombia</b> · BI and Data Analytics Intern · <code>Jul. 2026 – Present</code></summary>

<br/>

- Designed and built an internal **Django** application that analyzes files and estimates effort for the team.
- Built its REST API with **DRF**, background processing with Celery and Redis and PostgreSQL persistence, with automated tests in GitHub Actions.
- Prepared and validated data with **SQL and Python** for dashboard analysis.

`Python` `Django` `DRF` `Celery` `Redis` `PostgreSQL` `SQL`

</details>

<details>
<summary><b>TotalDev SAS</b> · Freelance Full Stack Developer · <code>Feb. 2025 – Mar. 2026</code></summary>

<br/>

- Added SWIFT MT support to an interbank gateway in **Java/Apache Camel**: MT103 and MT202 validation and automated ISO 20022 conversion.
- Developed the core modules of an electoral inventory platform in **Laravel and React**: bulk imports with row-level validation, regional permissions, Excel reports and queued PDF generation.
- Built a QR-scanning **PWA** for the operators of an industrial plant and its Laravel/Filament backend, with approvals, PDF delivery notes and monthly inventory reports.

`Java` `Apache Camel` `SWIFT` `ISO 20022` `Laravel` `Filament` `React` `PWA`

</details>

<details>
<summary><b>PARQ</b> · Full Stack Developer · <code>Nov. 2024 – Jul. 2025</code></summary>

<br/>

- Extended the **SATCOM, Siigo and Alegra** electronic invoicing connectors in a Laravel middleware with queued resend of failed invoices and per-request tracing.
- Maintained the **NestJS and PostgreSQL** services of a parking platform in Colombia, Mexico and the UK: country-specific rates, queued bulk membership creation and consistent timezones in reports.
- Built the corporate **Next.js** site with SSR, i18n and SEO and documented the APIs with OpenAPI.

`NestJS` `TypeORM` `PostgreSQL` `Laravel` `Next.js` `OpenAPI`

</details>

<details>
<summary><b>SEREMPRE</b> · Backend Developer · <code>Jan. 2023 – Nov. 2024</code></summary>

<br/>

- Diagnosed **L2/L3 production incidents** by tracing each failure through SQL, code review and Sentry, and documented its root cause.
- Built **Laravel APIs** for a benefits platform in more than five Latin American countries, with queues for validated payment uploads, duplicate cleanup and notifications.
- Wrote queries, **PL/SQL** procedures and Excel exports for other teams, and containerized legacy systems with Docker/DDEV.

`Laravel` `MySQL` `Oracle PL/SQL` `Sentry` `Docker` `Redis`

</details>

<h2><img src="assets/section-education.svg" alt="06 / Education — Studies and languages" width="100%"/></h2>

| | |
|---|---|
| **Systems and Computer Engineering** | UPTC, Tunja · Expected 2026 |
| **Information Systems Analysis and Development** (technologist) | SENA · 2022 |
| **Languages** | Spanish (native) · English (B2) |

<div align="center">

<br/>

<img src="assets/footer.svg" alt="Let's talk systems." width="100%"/>

<br/><br/>

[![Portfolio](https://img.shields.io/badge/Portfolio-gabo8191.github.io-0D0D0D?style=for-the-badge&labelColor=FFD93D)](https://gabo8191.github.io/portfolio/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-gabodev8191-0D0D0D?style=for-the-badge&labelColor=FF6FB5)](https://linkedin.com/in/gabodev8191)
[![Email](https://img.shields.io/badge/Email-gabo8191@gmail.com-0D0D0D?style=for-the-badge&labelColor=FFFDF5)](mailto:gabo8191@gmail.com)

![Profile views](https://komarev.com/ghpvc/?username=gabo8191&label=Profile%20views&color=0D0D0D&style=for-the-badge)

<sub>Tunja, Colombia · Remote · Spanish and English</sub>

</div>
