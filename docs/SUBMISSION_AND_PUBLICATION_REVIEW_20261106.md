# SignalBench — pre-publication privacy and grant-submission review

**Date:** 2026-11-06  
**Repository:** `topassky3/signalbench`  
**Current visibility:** **PRIVATE**; publication **NOT AUTHORIZED** by this document.

## Scope of the preliminary audit

- Enumerated every tracked file in the default branch through the GitHub recursive tree: **15 regular files**; the tree was not truncated.
- Inspected the text of each tracked file for obvious token assignments, private-key PEM headers, local IP addresses, personal e-mail address literals, home-directory paths and non-HTTPS links. No matches were found in the file contents under these patterns.
- Reviewed 13 current-repository commit summary entries. **All 13 expose an e-mail address in git author metadata** (it is not a GitHub noreply address). They do not need to be reproduced in application materials.
- The existing `LICENSE` contains an individual's personal name in the MIT copyright notice. Confirm the desired public attribution before making any repository public.
- The `.gitignore` excludes `*.sigmf-data`, `*.sigmf-meta`, `resultados_locales/`, keys and common environment files.
- Source files and the prior technical summary are **not** a substitute for a professional security scan, review of all historical blobs/PRs, or a legal review.
- One outdated item in `VERIFICACION.md` referred to unrelated OTF funding and was corrected in this branch.

## Release decision

**Do not automatically change this repository to public.** If the applicant chooses to publish later, compare these two options:

**A. Publish existing repository:** simplest and preserves the full Git history. **Risk:** author's e-mail addresses in the 13 historical commits become visible, and the copyright name is public. Removing e-mails in recent files does not remove historical commit metadata.

**B. Create a separate, clean-history public mirror:** keep this repository private, export only audited source, aggregate CSV, non-identifying documentation, and synthetic demos into a new public repo with fresh commits made using a privacy-preserving GitHub noreply identity. Do not copy raw IQ, sidecars, acquisition logs, .git history, local absolute paths or personal files. Verify the public mirror independently before sharing its URL. This requires explicit authorization for any new repo/publication. The existing project's history and evidence would remain private.

## Submission does not require a public repo

Hacker Initiative states: *"Just the information requested on the online form. You will be contacted for additional supporting documents if needed."* There is no requirement to release a repo or upload a report before submitting.

Source: https://hackerinitiative.org/application-faq/

If the form asks for a *project website*, use a genuinely accessible URL controlled by the applicant, clearly distinguish it from a private GitHub repository, or describe the private status truthfully if the field permits. Do not provide a private GitHub link as if anonymous reviewers can view it.

## Private form fields and final compliance check

The current online form is in English. The preview includes required personal/organizational contact information, a physical mailing address, check payee/tax responsibility, Q17–Q23 technical sections, Q25 reporting commitment, Q26 anti-discrimination commitment, Q27 referral source, and optional comments.

Before submitting, the applicant must personally verify:

- Legal first and last names, own contact e-mail, street address (not P.O. Box), municipality, regional division, country, postal code, phone and alternative contact information.
- Whether applying as an individual or a legally registered organization; enter `N/A` only if truthful and accepted by the form (do **not** invent tax ID/EIN).
- Who can lawfully receive a USD check and handle taxes/compliance in Colombia.
- Other project-specific financing already received **or expected**, if any; name funders as requested and do not presume "none".
- Q18 description between 150 and 300 words, Q19 measurable goals, Q20 worldwide community benefit, Q21 amount, Q22 detailed budget/timeline and geography.
- Q23 selection maximum of **two** categories (proposed: Research Project and Software/Tool Development).
- Q25 reporting: interim report by **June 15, 2027** and final report by **November 15, 2027**, notifying significant changes within five business days; Q26 anti-discrimination.
- Eligibility to participate and ability to accept/report the grant; budget estimates remain preliminary until supplier verification.
- Form confirmation after submission; keep the confirmation email and edit link. **Do not claim submission until the form confirms.**

The 2026 form says it closes Monday, November 9, 2026 at 11:59 PM PST. The form, not this repository, is the authoritative source:
https://docs.google.com/forms/d/e/1FAIpQLSc_6C9WO9PEXS3r1BN_Qq5LOL9xtoEux0pC6xTmxUlpxlanxg/viewform

## Evidence handling

- Keep uncalibrated OTA raw recordings in local private storage unless a separate legality/privacy review authorizes release.
- Do not expose the user's Windows screenshot with OS account details as a public figure; prefer a freshly exported plot with no user-interface chrome.
- The repository contains measured *aggregate values* and reproducible analysis scripts; an external party cannot reproduce the real PSD without the original raw samples. Say so plainly.
