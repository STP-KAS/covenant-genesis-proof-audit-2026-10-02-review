# Review of covenant-genesis-proof-audit-2026-10-02

> **Challenge context.** The STP-KAS audit repos are part of the challenge between the **bot side** (kaspa master challenge / kaspa master bot) and the **build side** (Grok Build / kaspa master prompt build). This repo is an **independent review** within that challenge. It checks the build-side audit [STP-KAS/covenant-genesis-proof-audit-2026-10-02](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02) against primary sources and reruns its tests. It does not speak for either side.

No comments, issues, PRs, reactions, tags, or releases were made on any repo, upstream or STP-KAS. The audited repo was not modified.

## Scope

| | |
| --- | --- |
| Audited repo | [STP-KAS/covenant-genesis-proof-audit-2026-10-02](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02), public |
| Audited commit | [`a97842da266517c3a5759d5d3375d773f39b5858`](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/commit/a97842da266517c3a5759d5d3375d773f39b5858) (2026-10-02 20:27 CEST, "Second pass…"), parent `fad7c0c1` |
| Files reviewed | `README.md`, `AUDIT.md` (F1–F12), `VECTORS.md` (V1–V6), `COVERAGE.md`, `INCONSISTENCIES.md` (I1–I7), `MASTER-DELTA.md`, `SECOND-PASS.md` (all 7) |
| Subject of that audit | [argent-lang/argent#66](https://github.com/argent-lang/argent/pull/66) at head [`9592dd99`](https://github.com/argent-lang/argent/commit/9592dd996d2503eb166335d6da92548de193877f), "Add layered covenant genesis proof APIs and CLI tooling" |
| Review date | 2026-10-02 (about 20:57 to 21:30 CEST) |

## Method

1. Read every file in the audited repo. Listed each substantive claim with its file and line.
2. Re-checked each claim against primary sources at pinned commits: argent `9592dd99`, rusty-kaspa `a41a333b` and tag v2.1.0, kips `e4ae2332` (KIP-20), kccs#26 `d51721ad` (KCC-23), silverscript `3ed97333` (v1.0.0), supertypo dotk-indexer `17ca993b` plus dotk-core, dotk-sdk, and dotk-sdk-tx, argent issue #57, the X post and reply (X API), and `STP-KAS/kaspa-master-file` (`main` `99ae9620`, `build/2026-10-02` `0c72511f`). GitHub was read only (`gh api`, `git clone`).
3. Reran the audit's runs on Linux with rustc/cargo 1.97.1, the same toolchain the audit used: V1, V2, V3.
4. Wrote an **independent** KIP-20 recompute in Python ([scripts/kip20_recompute.py](scripts/kip20_recompute.py)) for V4 (KCC-23 vector) and V5 (DOTK binding and byte checks).
5. Added probes the audit had not run: unknown JSON fields at the library level and through the CLI (R-01).
6. Full reproduction: [scripts/reproduce.sh](scripts/reproduce.sh). Outputs: [logs/](logs/).

## Findings

| ID | Severity | Audit claim / location | Result |
| --- | --- | --- | --- |
| [R-01](FINDINGS.md#r-01-medium-f2-understates-the-unknown-field-gap-annotations-are-also-accepted-inside-embedded-artifacts-and-still-accepted-with---source) | medium | F2, AUDIT.md L24-L34, SECOND-PASS L19 | F2 is confirmed by an actual probe, and it reaches further than the audit says. Unknown fields inside the embedded `Artifact` are also dropped, and `verify --require-argent --source` still exits 0 and prints "source correspondence matches". The audit's six-type fix is incomplete. |
| [R-02](FINDINGS.md#r-02-low-f6-cites-a-transaction-builder-helper-as-the-nodes-ordering-rule) | low | F6, AUDIT.md L72-L82 | The conclusion holds. The lead citation `populate_genesis_covenants` is a transaction-builder helper. Consensus enforcement is `CovenantsContext::from_tx` (validator L182). |
| [R-03](FINDINGS.md#r-03-low-f7-says-issue-57s-four-rules-are-otherwise-met-rule-2-is-deliberately-not-met-on-the-default-consensus-layer-path) | low | F7, AUDIT.md L90 | "Four rules otherwise met" is generous. #57 rule 2 (bind the program) is not met by consensus-layer packages, which plain `verify` accepts. |
| [R-04](FINDINGS.md#r-04-low-the-sil-files-are-not-public-rests-on-one-repo-a-wider-check-agrees) | low | AUDIT.md L178, F9 | "`.sil` not public" was checked in one repo only. This review checked all four public DOTK repos: still none. The ABI `source_path` names `sil/DotkGap.sil` and `sil/DotkDeed.sil`. |
| [R-05](FINDINGS.md#r-05-low-the-audited-repo-calls-itself-private-but-it-is-public) | low | README.md L3, SECOND-PASS L3 | The repo calls itself a "Private desk note", but GitHub visibility is PUBLIC. |
| [R-06](FINDINGS.md#r-06-low-hygiene-windows-paths-in-vectorsmd-do-not-follow-stps-cusersfermi-convention) | low | VECTORS.md L3, L39, L45 | Windows paths use a profile name other than `C:\Users\Fermi\...`. |
| [R-07](FINDINGS.md#r-07-info-the-audit-never-says-who-wrote-argent66) | info | README "Why" | The PR author (michaelsutton) is also the author of the framing post. The audit does not say so. |
| [R-08](FINDINGS.md#r-08-info-the-deed-template-hash-occurs-twice-in-the-gap-script) | info | VECTORS L100, SECOND-PASS L30 | The deed template hash occurs at 5604 **and** 5851, not only at 5604. |
| [R-09](FINDINGS.md#r-09-info-facts-that-depend-on-time-have-moved-since-the-audit) | info | MASTER-DELTA L7, COVERAGE L23 | The MASTER-DELTA edits are now applied on `build/2026-10-02` at `0c72511f`. The quote count is now 5. PR #66 is unchanged. |
| [R-10](FINDINGS.md#r-10-info-pin-the-kip-20-citation-and-the-posts-dotk-link) | info | COVERAGE L12 | KIP-20 was cited from a "saved copy". It is pinned here to `e4ae2332`, and the text matches. |

There are no critical or high findings. Every reproduced number matched exactly: 15, 430, 7, 10 tests; covenant ids `656c9d1c…9c48`, `c86366ce…394e`, `ee2128c0…21de`; 6342 / 3220 / 35 / 66 bytes; offset 5604. See the "Confirmed correct" table in [FINDINGS.md](FINDINGS.md#confirmed-correct-re-checked-by-this-review).

Could not verify: the Discord card (no access, and the audit did not reopen it), the X quote search, Sil-layer unknown fields, the V6 full workspace/clippy/fmt runs, and DOTK on-chain state (no node). Teammate agents were not contacted: this executor had no messaging tool, so the master-file branches were searched instead. Details are under "Could not be verified" in FINDINGS.md.

## Verdict

**The audit holds.** Its central claim is independently confirmed: argent#66's lowest layer calls rusty-kaspa's own `covenant_id`, whose byte layout is KIP-20 §3.2 (u64 little-endian lengths, BLAKE2b-256 keyed `CovenantID`). The same is true of its DOTK recompute, its test results, and its conclusions ("0 blockers, reviewable, not yet the finished deployment process", "not a consensus requirement", "KCC-23 is Draft"). The one substantive correction is that F2's should-fix (unknown JSON fields) is real and **wider** than written. It also covers embedded artifacts, and it survives the `--source` path, so the proposed six-type fix should be extended. The other items are citation precision, scope, labeling, and hygiene.

## Repo contents

- [FINDINGS.md](FINDINGS.md): every finding in full, the confirmed list, what could not be verified, and open questions
- [SOURCES.md](SOURCES.md): every source used, pinned
- [scripts/](scripts/): `kip20_recompute.py`, `unknown_fields_probe.rs`, `reproduce.sh`
- [logs/](logs/): V1, V2, V3, P1, P2, the R4/R5 recompute, a PR #66 snapshot, and the environment
