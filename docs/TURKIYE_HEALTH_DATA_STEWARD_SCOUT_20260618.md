# Türkiye Health Data Steward Scout

Date: 2026 06 18

Status: public route scout for health data quality and AI readiness, not an application.

Purpose: turn the health data quality lane into a concrete route owner review surface for Türkiye health AI safety work.

This is not an official Ministry of Health document, not a TÜSEB document, not a proposal, not an application, not a partner claim, and not an endorsement claim.

## Source signals

### THDSS001: Sağlık Bilgi Sistemleri Genel Müdürlüğü public site

Official source: https://sbsgm.saglik.gov.tr

Checked fact: The public site lists Büyük Veri Sistemleri ve Veri Yönetimi Koordinatörlüğü among the General Directorate coordination surfaces.

Field read: A health data quality scout should route through data management and governance surfaces before any AI assurance claim is made.

### THDSS002: Yapay Zekâ ve Yenilikçi Teknolojiler Daire Başkanlığı

Official source: https://sbsgm.saglik.gov.tr/TR-104172/yapay-zeka-ve-yenilikci-teknolojiler-daire-baskanligi.html

Checked fact: The page lists duties that include identifying processes and problems that can be improved with AI, producing or procuring AI solutions, tracking AI technology developments, working with universities, institutes, and health organizations, ensuring interoperability of projects, and preparing education materials.

Field read: A useful public scout should connect data quality, interoperability, AI readiness, and education without claiming official access.

### THDSS003: Kayıt ve Tescil Birimi public site

Official source: https://kayittescil.saglik.gov.tr/

Checked fact: The public site lists registered software surfaces and announcements for health information management systems and related software categories.

Field read: Health AI readiness depends on registered software, data flow, provenance, and auditability before model claims.

### THDSS004: TÜSEB public site

Official source: https://www.tuseb.gov.tr/

Checked fact: The public site lists Türkiye Sağlık Veri Araştırmaları ve Yapay Zeka Uygulamaları Enstitüsü among TÜSEB institutes.

Field read: Health data research and AI application surfaces are relevant to a future data quality review packet, but this scout does not claim TÜSEB review or partnership.

## Steward questions

### Question 1: data source ownership

Review question: Who owns or stewards the data source used by the health AI project?

Reason: A model report is not reviewable if the data source and stewardship path are unclear.

### Question 2: data permission and public boundary

Review question: What can be shared publicly, and what must stay private or institutional?

Reason: Public artifacts should not expose patient level data, private operational data, or unclear permission states.

### Question 3: schema and coding provenance

Review question: Which coding system, schema, registry, or software source produced the data fields?

Reason: Medical AI errors often begin with unstable labels, inconsistent fields, and untracked coding changes.

### Question 4: missingness and drift

Review question: Which variables are missing, delayed, changed over time, or not comparable across institutions?

Reason: Missingness and drift can make public model claims look stronger than the actual evidence.

### Question 5: label audit

Review question: Who checked labels, how disagreements were handled, and when a label should remain uncertain?

Reason: Health AI safety needs label uncertainty language before any benchmark, report, or public claim.

### Question 6: AI readiness gate

Review question: Does the data have enough provenance, permission, completeness, and review trail to support an AI readiness claim?

Reason: Data availability is not the same as AI readiness.

### Question 7: public claim hygiene

Review question: Does the public wording avoid validation, deployment, endorsement, ranking, and official role claims?

Reason: Data quality work should make future field action safer without inflating authority.

## Route owner candidates

These are route surfaces, not confirmed partners.

1. Sağlık Bilgi Sistemleri Genel Müdürlüğü data management and big data surfaces.
2. Sağlık Bilgi Sistemleri Genel Müdürlüğü AI and innovative technology surfaces.
3. Kayıt ve Tescil Birimi software registration and health information system surfaces.
4. TÜSEB Türkiye Sağlık Veri Araştırmaları ve Yapay Zeka Uygulamaları Enstitüsü as a research aligned surface.
5. University health informatics and digital medicine boards already tracked in this repository.

## Decision states

1. Route unknown: do not send a data packet yet.
2. Route identified: send only a non patient data review surface.
3. Steward review requested: wait for explicit route owner response.
4. Data quality review possible: prepare a scoped worksheet with no patient data.
5. Blocked: any patient data, clinical validation, official role, partner, payment, or terms path appears without verified clearance.

## Boundary

1. No Ministry of Health endorsement claim.
2. No TÜSEB endorsement claim.
3. No official role claim.
4. No route access claim.
5. No partner claim.
6. No application claim.
7. No proposal claim.
8. No patient data included.
9. No private operational data included.
10. No diagnosis or treatment advice.
11. No clinical deployment claim.
12. No clinical validation claim.
13. No model ranking.
14. No score certification.
15. No payment.
16. No terms acceptance.

## Field action

Publish this as a public data steward scout. Use it to decide whether the next public action should be a non patient data data quality worksheet, a route owner fit note, or a source checked public claim hygiene card.

No email, public social post, application, proposal, official route, partner claim, payment, terms acceptance, patient data, clinical deployment, clinical validation, or official endorsement is made by this scout.

## Runnable check

```bash
make turkiye_health_data_steward_scout
```
