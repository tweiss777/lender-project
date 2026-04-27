# DECISIONS.md

## Which Lender Requirements Were Prioritized

All five provided lender PDFs were ingested and modeled. The following criteria were implemented across the matching engine:

- **FICO score** minimum (per program/tier)
- **PayNet score** minimum (per program/tier)
- **Time in business** minimum (years)
- **Loan amount** range (min/max)
- **Loan term** range (min/max months)
- **Annual revenue** minimum
- **Equipment type** restrictions (blacklist)
- **Equipment age** maximum (years, derived from equipment model year)
- **State** restrictions (whitelist and blacklist)
- **Industry** restrictions (whitelist and blacklist)
- **Bankruptcy history** — both hard no-bankruptcy flags (Advantage+) and minimum years-since-discharge (Falcon: 15yr, Stearns: 7yr, Citizens: 5yr)
- **Judgments** — flagged as disqualifying where stated (Advantage+)
- **Tax liens** — flagged as disqualifying where stated (Advantage+)
- **US Citizenship** requirement (Citizens Bank, Advantage+)

Criteria that were deprioritized due to ambiguity or complexity:
- **Advance rates / LTV ratios** — lenders reference these but they vary by collateral type and would require an appraisal model to evaluate accurately
- **Personal guarantor net worth** — mentioned by some lenders but not consistently defined across PDFs
- **Collateral haircuts** — too lender-specific and collateral-dependent to normalize reliably in the time available

---

## Simplifications Made and Why

**Flat equipment type matching** — equipment type is matched as a string against a blacklist. A more robust implementation would use a taxonomy (e.g. NAICS equipment codes) to catch variations like "Semi-Truck" vs "Class 8 Truck". This was simplified to keep the matching engine readable and easy to extend.

**No discharge date for bankruptcy** — the engine flags bankruptcy as a disqualifier when a lender requires a minimum years-since-discharge, but it does not calculate the exact discharge date. This was left as a "manual review required" flag since collecting a precise discharge date would require additional UI and validation logic. In practice, a loan officer would verify this.

**Equipment age from model year only** — equipment age is derived from the equipment model year field. A more accurate implementation would account for first-use date or hours-of-use for used equipment, but model year is the most consistently available data point.

**Single guarantor** — the schema supports one personal guarantor per borrower. Multi-guarantor deals (e.g. partnerships) are common in equipment finance but were out of scope for this implementation.

**Seed data as source of truth for PDFs** — the five provided lender PDFs were manually parsed into seed data to ensure accuracy. The automated PDF parser (Claude API) is used for new lenders added after the fact. Running the PDFs through the parser would produce slightly different values depending on how Claude interprets ambiguous language in the guidelines.

**No PayNet score for new businesses** — some lenders accept alternative scoring for businesses without a PayNet history. This edge case was not modeled; the engine will flag PayNet as failing if no score is on file.

---

## What I Would Add With More Time

**More robust policy editing UI** — the current lender policy screen is read-only. A full CRUD editor for each policy field (including the join tables for industries, states, and equipment) would make it easier for a loan officer to update policies without touching the database directly.

**Webhook / async underwriting** — for large numbers of lenders, running all checks synchronously in a single request could become slow. The natural next step is to move `MatchingEngine.run()` into a background task (Hatchet or FastAPI's `BackgroundTasks`) and poll for results, which also enables retry logic per lender.

**PayNet score integration** — real-world underwriting pulls PayNet scores via API at application time. Integrating a PayNet data feed would remove the need to manually enter business credit scores.

**Advance rate / LTV calculation** — several lenders cap financing at a percentage of the equipment's appraised value. Modeling this would require an equipment valuation source (e.g. EquipmentWatch) and would significantly improve the accuracy of the fit score.

**Tier auto-selection** — for lenders with multiple tiers (Apex A/B/C, Stearns 1/2/3), the engine currently evaluates all tiers independently and returns all results. A smarter implementation would identify the best tier the borrower qualifies for and surface only that one, reducing noise in the results.

**Test coverage** — basic unit tests for the matching engine checks are the highest priority addition. Each `EvaluationCheck` subclass is pure logic with no database dependencies, making them straightforward to test with mocked `ApplicationContext` and `PolicyContext` objects.

**Document storage** — uploaded PDFs are currently parsed and discarded. Storing them alongside the lender record would allow re-parsing if the extraction prompt improves, and serves as an audit trail for where each policy came from.
