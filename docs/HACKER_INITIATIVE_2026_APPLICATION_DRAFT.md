# Hacker Initiative 2026 — SignalBench application draft (NOT SUBMITTED)

Prepared 2026-11-06; draft subject to applicant confirmation. Respond to the **actual online form in English**. This document deliberately omits address, tax identification, and banking information.

## Question 17 — Project Name

**SignalBench: Reproducible Open-Source SDR Measurement Toolkit**

## Question 18 — Brief Project Description (232 words; permitted 150–300)

SignalBench is an open-source, low-cost toolkit for inspecting software-defined radio (SDR) recordings and making measurement limitations visible. A radio capture is more than a waveform: its interpretation depends on correct sample-rate metadata, data integrity, receiver settings, and honest reporting of uncertainty. Beginners and independent hackers often lack a repeatable process for distinguishing a real signal feature from a processing or acquisition artifact.

Our working Python demonstrator generates documented synthetic cases, checks recording integrity with SHA-512, reads a focused subset of SigMF, and reports relative sample power, DC contribution, digital rail indicators, and spectral peak offsets. Six numerical tests initially passed. We subsequently acquired one real RTL-SDR recording and carried out a nine-capture gain sweep on an ARM64 computer at three manual gain settings. All ten automated software tests passed, and the nine physical recordings were transferred and verified against their recorded checksums. These results establish an acquisition and analysis workflow, not calibrated RF sensitivity or frequency accuracy.

We seek USD 5,000 for a 12-week project to develop controlled signal-reference experiments, assemble eight affordable replication kits, publish at least twelve carefully documented bench recordings, and support three independent replication attempts. The deliverables will include source code, executable tests, bilingual instructions, reproducible analysis notebooks or scripts, and clear explanations of what can and cannot be concluded from low-cost SDR measurements. SignalBench will help hackers and STEM learners develop practical signal-processing literacy using accessible hardware.

## Question 19 — Project Goals / Measurable Success

Over twelve weeks, SignalBench will (1) release a documented open-source Python toolkit and regression suite; (2) perform **three controlled bench experiments** with explicitly recorded references, gain/attenuation settings, and uncertainty/limits; (3) assemble **eight low-cost SDR replication kits** for compatible receivers and host setups; (4) publish **at least twelve shareable, non-sensitive bench recordings** with SigMF metadata, SHA-512, capture logs and scripted analysis; and (5) invite and document **three independent replication attempts**, including failed attempts and issues. Success will be assessed from reproducible test logs, checked hashes, data availability/permissions, transparent experimental limitations, and the completeness of outside reproduction reports. The project does not promise an accredited RF calibration or an inference of absolute physical RF power from digital power alone.

**Proposed timeline:**
- Weeks 1–2: finalize versioned processing code, metadata import, capture safety checks, and measurement protocol.
- Weeks 3–6: purchase/assemble kits and reference setup; conduct controlled amplitude, metadata, and gain/attenuation experiments.
- Weeks 7–10: record and check at least twelve bench datasets; publish reproducible analysis and clear instructions.
- Weeks 11–12: request three external replications, collect issue reports, and release a final technical summary.

## Question 20 — Community Benefit

SignalBench is designed for independent hardware hackers, radio experimenters, security researchers, STEM educators, and students who use low-cost SDR hardware. It makes common pitfalls in I/Q analysis directly inspectable: incorrect sampling metadata, DC contamination, digital clipping thresholds, uncertain gain effects, and the difference between numerical consistency and instrument calibration. The proposed open-source release will provide runnable code, synthetic controls, explicitly tagged real recordings, bilingual setup instructions, and inexpensive replication recipes. Its purpose is not to sell a proprietary instrument but to lower barriers to careful measurement and help the global hacking community discuss signal evidence with appropriate skepticism.

## Question 21 — Amount of Funding Requested

**USD 5,000 (requested).**

Other grants, sponsorships or expected project-specific contributions: **[APPLICANT MUST CONFIRM AND NAME ANY SOURCES; do not state “none” without confirmation].**

## Question 22 — Intended Use of Grant and Spending Timeline

**Preliminary allocation (estimates, not supplier quotes):**

| Direct project cost | Qty | Budget (USD) |
| --- | ---: | ---: |
| Eight compatible SDR replication kits: receivers, suitable antenna accessories and modest host/storage/power components | 8 | 1,600 |
| One controlled RF reference source appropriate to agreed test frequencies and levels | 1 | 1,250 |
| Two lower-cost reference/tone source modules for replicated test benches | 2 | 300 |
| Fixed attenuators, 50-ohm terminations, coax, adapters, filters and test protection | mixed | 650 |
| Evidence storage and removable media for datasets and distribution | mixed | 400 |
| Documented shipping, import duties, taxes and handling of eligible hardware | estimate | 800 |
| **TOTAL** | | **5,000** |

The above are **planning estimates only** and must be reconciled against dated vendor quotations, shipping destinations, import charges, receiver and host compatibility, and the grantee's legal/tax obligations before submission. Do not buy additional RTL-SDR Blog V4 receivers merely to match the existing unit: the V4 has reached end-of-line; assess currently supported hardware such as genuine V3 or V4L and cross-model comparability. The existing Orange Pi + RTL-SDR V4 equipment has already been used for the proof of concept and is **not** being charged retroactively.

Suggested spend phases: weeks 1–4 reference equipment and accessories; weeks 3–7 kits and storage; weeks 5–10 logistics as purchases are shipped and delivered; weeks 10–12 remaining eligible consumables and verification. Final quantities will be reduced or substituted if verified quotes exceed budget.

**Funding restrictions:** no salaries, staff training, tuition, website production, fundraising, commercial advertising or unrelated activities. The work is an open-source scientific/educational hardware and software measurement project.

**Geographic location:** Antioquia, Colombia, with a remote global replication community. Project code: `https://github.com/topassky3/signalbench` (**private while being reviewed; do not claim reviewers can access it yet**).

## Question 23 — Project Category (choose no more than two)

- **Research Project**
- **Software/Tool Development**

These best describe the work, although equipment will also be purchased; the official form permits a maximum of two selections.

## Personal fields and compliance gates (not filled in this file)

The form additionally requests legal name, physical street/mailing address (not a P.O. box), postal code, contact information, organization fields as applicable, website, relationship, check payee/tax compliance, and confirmation of reporting and anti-discrimination policies. These answers must use verified **private** applicant information, not assumptions; do not commit them to a public code repository.

Confirm ability to comply with reporting, including the official form's stated **June 15, 2027 interim** and **November 15, 2027 final** reporting deadlines and notices of material changes. Confirm ability to legally receive USD payments/checks in Colombia and state how fiscal compliance will be managed. Only the applicant should agree to legal commitments and submit.

## Verified official sources (2026-11-06)

- Grant cycle and deadline: https://hackerinitiative.org/
- Application guidance and exclusions: https://hackerinitiative.org/apply-now/
- FAQ: https://hackerinitiative.org/application-faq/
- Official application preview: https://hackerinitiative.org/wp-content/uploads/2026/09/The-Hacker-Initiative-Grant-Application-2026.pdf
- RTL-SDR Blog V4 EOL notice: https://www.rtl-sdr.com/rtl-sdr-blog-v4-end-of-line/

**Deadline:** Monday 9 November 2026, 11:59 PM PST, per form preview; aim to submit Sunday 8 November in Colombia. The actual application must be submitted using the official online form; a PDF or repository is supporting material, not the submission channel.
