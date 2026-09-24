---
name: research-sprint
description: Fast multi-front web research sprint on a technology, vendor, method or market question. Splits the question into independent fronts, runs research agents (tech-scout, market-data-researcher, quant-researcher) in parallel, cross-checks their claims, and writes an evidence-graded report plus tech-radar updates. Use when the user asks to research, compare, or find new tools/libraries/services.
argument-hint: "<question or topic>"
---

Run a research sprint on: $ARGUMENTS

1. **Frame the sprint.**
   - Write the decision the research must inform, the constraints (the product and data rights in `02`/`04`, team size, budget), and what would change the answer.
   - Split the question into 3–6 **independent fronts**, for example: runtime and language, engines and frameworks, data sources, managed services, new work from the last 12 months, and academic evidence.
2. **Fan out in parallel.** Use the Agent tool:
   - `tech-scout` for tools and libraries;
   - `market-data-researcher` for data, vendors and licensing;
   - `quant-researcher` for methods and papers.

   Each agent's brief includes:
   - its front;
   - "primary sources; registry versions and dates; licence vs data rights; benchmarks with methodology; URL + access date + H/M/L";
   - a note to return a table plus an unverified list.
3. **Cross-check.**
   - Take any claim the decision depends on and re-verify it on the primary page, or in read-only registry metadata (PyPI JSON, crates.io, GitHub releases). Check that the package author or homepage matches the vendor.
   - Installing or running third-party code, for example an import test or a benchmark, **needs user approval first**.
   - Where agents conflict, mark the item "conflicting".
4. **Write the report.** Save it as `docs/production-plan/research/<kebab-topic>.md`, with sections in this order:
   1. decision question;
   2. recommendation and tier;
   3. comparison table;
   4. what would change the answer;
   5. unverified items;
   6. sources.

   Update `research/tech-radar.md` using the rings Adopt, Trial, Assess, Hold.
5. **Propose an ADR** if the answer changes an existing decision. Don't accept it yourself; the user decides.

Budget: keep it quick. Prefer breadth first, then go deep only on the 2–3 finalists.
