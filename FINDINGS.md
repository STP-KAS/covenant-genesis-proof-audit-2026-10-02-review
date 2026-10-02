# Findings: review of covenant-genesis-proof-audit-2026-10-02

Audited repo: [STP-KAS/covenant-genesis-proof-audit-2026-10-02](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02) at [`a97842da266517c3a5759d5d3375d773f39b5858`](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/commit/a97842da266517c3a5759d5d3375d773f39b5858). Its subject: [argent-lang/argent#66](https://github.com/argent-lang/argent/pull/66) at head [`9592dd996d2503eb166335d6da92548de193877f`](https://github.com/argent-lang/argent/commit/9592dd996d2503eb166335d6da92548de193877f).

Review date: 2026-10-02, about 20:57 to 21:30 CEST. All times are CEST (UTC+2) unless a source carries its own zone.

Short names used below: `AUD` = the audited repo at `a97842da`. `ARG` = argent at `9592dd99`. `RK` = rusty-kaspa at `a41a333b08848f41bf737b72592e463a6011b8ac`.

Severity describes how much the audit's text needs to change. It does not rate argent#66. "Confirmed" means this review checked it again on its own, against the primary source or by running it.

---

## R-01 (medium): F2 understates the unknown-field gap. Annotations are also accepted inside embedded artifacts, and still accepted with `--source`

- **Claim:** [AUD AUDIT.md L24-L34](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/AUDIT.md#L24-L34). Six proof structs lack `deny_unknown_fields`. The proposed fix is to "set `deny_unknown_fields` on those six types, and add one JSON test" (L32). [SECOND-PASS.md L19](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/SECOND-PASS.md#L19) says it was "Not run as an extra serde probe".
- **What is right:** The six structs named do lack the attribute: [preimage.rs L20-L49](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-genesis/src/preimage.rs#L20-L49), [sil.rs L35-L36, L85-L86](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-genesis/src/sil.rs#L35-L36), and [ag.rs L101-L102, L151-L152](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-genesis/src/ag.rs#L101-L102). The envelope, the layer enum, `ArgentGenesisPackage`, and both bootstraps do have it ([package.rs L19-L21, L101-L103, L131-L133](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-genesis/src/package.rs#L19-L21)).
- **What is missing:**
  1. The audit never ran a probe. This review did, and the gap is real. `GenesisProofPackage::from_json` followed by `verify` accepts `proof.value.audited` and `proof.value.outputs[0].source_url`. It rejects the same field on the envelope and next to `kind`/`value` ([logs/P1-unknown-fields-probe.log](logs/P1-unknown-fields-probe.log), probe source in [scripts/unknown_fields_probe.rs](scripts/unknown_fields_probe.rs)).
  2. The same gap exists in a type the audit does not list: the embedded `argent_artifact::Artifact` ([argent-artifact/src/lib.rs L30-L31](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-artifact/src/lib.rs#L30-L31)). That file contains no `deny_unknown_fields` at all. The artifact id check (`verify_id`, [L181-L190](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-artifact/src/lib.rs#L171-L190), called through `check_artifact_consistency` in [argent-runtime/src/lib.rs L1723-L1728](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-runtime/src/lib.rs#L1723-L1728)) hashes the parsed struct, so the dropped field never reaches the hash. CLI run: planting `"audit_status": "verified"` in `proof.value.primary` and running `argentc genesis verify ... --require-argent --source app.ag` exits 0. It prints "source correspondence matches the primary app and dependency artifact IDs" ([logs/P2-cli-annotated-package.log](logs/P2-cli-annotated-package.log)).
  3. As a result, the audit's six-type fix would leave the strongest-looking verify path (`--source`) still accepting a raw-JSON "verified" annotation.
- **Why it matters:** The audit's own reasoning (AUDIT.md L28) is that a person or explorer reading the raw file can mistake an annotation for part of the check. That risk is greatest on the `--source` path, because its stdout reads like an endorsement.
- **Agreement:** The audit is right that this is not a blocker. The covenant id does not cover JSON text, and no mutation here changes what is verified.
- **Recommendation:** Change F2 to cover the `Artifact` tree, or to require that explorers render only a typed re-serialization (`to_json` of the parsed package) and never the published bytes. Replace "Not run as an extra serde probe" with these results. The silverscript-abi types inside the Sil layer were not probed here (see U-03).

## R-02 (low): F6 cites a transaction-builder helper as the node's ordering rule

- **Claim:** [AUD AUDIT.md L72-L82](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/AUDIT.md#L72-L82), titled "Node order matches the proof's strict indices", leads with `Transaction::populate_genesis_covenants` (`is_sorted` then `seen_outs`). [COVERAGE.md L16](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/COVERAGE.md#L16) does the same.
- **What is wrong:** `populate_genesis_covenants` ([RK consensus/core/src/tx.rs L335-L371](https://github.com/kaspanet/rusty-kaspa/blob/a41a333b08848f41bf737b72592e463a6011b8ac/consensus/core/src/tx.rs#L335-L371)) fills in covenant bindings while a transaction is being built. The wasm client exposes it too ([consensus/client/src/transaction.rs L300, L500](https://github.com/kaspanet/rusty-kaspa/blob/a41a333b08848f41bf737b72592e463a6011b8ac/consensus/client/src/transaction.rs#L300)). It is not where consensus validates a block transaction. Consensus enforcement is `CovenantsContext::from_tx`, called from [tx_validation_in_utxo_context.rs L182](https://github.com/kaspanet/rusty-kaspa/blob/a41a333b08848f41bf737b72592e463a6011b8ac/consensus/src/processes/transaction_validator/tx_validation_in_utxo_context.rs#L182). It builds each genesis group by `enumerate()` over the outputs, so indices are increasing by construction, then recomputes and compares the id ([covenants.rs L113-L160](https://github.com/kaspanet/rusty-kaspa/blob/a41a333b08848f41bf737b72592e463a6011b8ac/crypto/txscript/src/covenants.rs#L113-L160)).
- **Effect:** The conclusion (holds) stands. The audit also names `covenants.rs` in its "How you checked" line. Only the citation that leads the finding is wrong.
- **Recommendation:** Lead F6 with `CovenantsContext::from_tx` and the validator call site. Present `populate_genesis_covenants` as the builder-side mirror that the proof's unit test uses ([preimage.rs L144-L160](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-genesis/src/preimage.rs#L144-L160)).

## R-03 (low): F7 says issue #57's four rules are "otherwise met". Rule 2 is deliberately not met on the default consensus-layer path

- **Claim:** [AUD AUDIT.md L90](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/AUDIT.md#L84-L94): "The four rules are otherwise met at the layer where they apply."
- **Evidence:** [argent#57](https://github.com/argent-lang/argent/issues/57) rule 2 ("Bind the program, not just the preimage") warns that without a template or artifact binding "a lookalike lineage passes every structural check". Plain `argentc genesis verify` with no `--require-argent` accepts a consensus-layer package and prints "covenant ID matches" ([src/cli/genesis.rs L121-L151](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/src/cli/genesis.rs#L121-L151)). That layer carries no template or artifact id ([preimage.rs L41-L49](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-genesis/src/preimage.rs#L41-L49)). The CLI does print its scope ("checked: genesis output scripts, values, indices, and authorizing outpoint"), and the audit's explorer section says to name the layer. That reduces the risk but does not remove it.
- **Recommendation:** Say rule 2 is met for the Sil and Argent layers and is out of scope by design for the consensus layer. Keep the explorer guidance to "say which layer ran". Severity stays a nit for argent#66.

## R-04 (low): "The `.sil` files are not public" rests on one repo. A wider check agrees

- **Claim:** [AUD AUDIT.md L178](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/AUDIT.md#L178): "The `.sil` files are not public at tip `17ca993bec66`." F9 and COVERAGE only list `supertypo/dotk-indexer`.
- **Evidence:** The audit is right that dotk-indexer [`17ca993b`](https://github.com/supertypo/dotk-indexer/tree/17ca993bec669fe2e8cc0be2b708bfbe0137ba46) has no `.sil` or `.ag` (recursive tree, 134 entries, not truncated). This review also checked the other public DOTK repos: [dotk-core `5a0e6ae1`](https://github.com/supertypo/dotk-core/tree/5a0e6ae101622e9f7769a02a557c8cea386555ea), [dotk-sdk `c9194976`](https://github.com/supertypo/dotk-sdk/tree/c919497661ea999d267fd06cbc30014872a31776), and [dotk-sdk-tx `d9d9a595`](https://github.com/supertypo/dotk-sdk-tx/tree/d9d9a59535bb0897f777afed040afab9f2730e52). None has a `.sil` file. GitHub code search for `DotkGap` found only dotk-sdk generated TypeScript. The manifest's ABI names the missing files: `gapAbi.contracts.DotkGap.source_path = "sil/DotkGap.sil"` and `deedAbi.contracts.DotkDeed.source_path = "sil/DotkDeed.sil"` (compiler_version `0.1.0`).
- **Recommendation:** Write it as "not in any public supertypo DOTK repo as of these tips". Add the `source_path` detail, which is the manifest's own pointer to source that is not yet published.

## R-05 (low): The audited repo calls itself private, but it is public

- **Claim:** [AUD README.md L3](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/README.md#L3): "Private desk note for stp". [SECOND-PASS.md L3](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/SECOND-PASS.md#L3): "after the private repo's first push". The commit message of `fad7c0c1` says "Record the private covenant genesis proof audit".
- **Evidence:** The GitHub API reports `"visibility": "PUBLIC"` for the repo (created 2026-10-02T18:23:46Z, which is 20:23 CEST).
- **Recommendation:** Either make the wording match the visibility, or decide which was intended. stp has since asked for these challenge repos to be public, so the wording is what should change. Nothing sensitive was found apart from R-06.

## R-06 (low, hygiene): Windows paths in VECTORS.md do not follow stp's `C:\Users\Fermi\...` convention

- **Where:** [AUD VECTORS.md L3, L39, L45](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/VECTORS.md#L3). The clone path, the `--out` path, and the printed `wrote` path all use a Windows profile directory with a different user name. That name is not repeated here.
- **Why it matters:** stp's rule is that Windows local paths must read `C:\Users\Fermi\...`. In a public repo this also exposes a local user name.
- **Recommendation:** Rewrite those three lines to `C:\Users\Fermi\...` in a normal follow-up commit, without rewriting history.

## R-07 (info): The audit never says who wrote argent#66

- **Evidence:** The GitHub API gives `user.login = michaelsutton`, and every commit's author is Michael Sutton (head commit at 2026-10-02 16:38:38 +03:00, which is 15:38 CEST). The X post that the audit treats as the framing source ([2106033659698450492](https://x.com/michaelsuttonil/status/2106033659698450492), 14:48:47Z, which is 16:48 CEST) is by the same person and links the pull.
- **Why it matters:** The post and the PR are one source, not two. The audit's README "Why" section reads as if the post asked for tooling and the pull answered it independently. Nothing in the audit is wrong because of this.
- **Recommendation:** Add one line: "PR author: michaelsutton (also the author of the post)".

## R-08 (info): The deed template hash occurs twice in the gap script

- **Claim:** [AUD VECTORS.md L100](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/VECTORS.md#L100) and SECOND-PASS L30 say "at offset 5604".
- **Evidence:** It occurs at offsets **5604 and 5851** in the 6342-byte redeem script ([logs/R4-R5-kip20-recompute.log](logs/R4-R5-kip20-recompute.log)). 5604 is the first occurrence, so the statement is not false, only incomplete.
- **Recommendation:** Say "first occurs at 5604 (2 occurrences)". As the audit says, this is a byte find and not a deed audit.

## R-09 (info): Facts that depend on time have moved since the audit

- MASTER-DELTA [L7](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/MASTER-DELTA.md#L7) says `build/2026-10-02` was at `9f5d3ca`. It is now at [`0c72511f`](https://github.com/STP-KAS/kaspa-master-file/commit/0c72511fdc1a809fe177e0f267ee89eeea8fb230) (2026-10-02 20:26:13 +02:00, "Record the covenant-id byte layout and the DOTK binding recompute."). That commit contains main `99ae9620` and applies the Argent-cell, DOTK-cell, do-not-weld, and master.json edits that MASTER-DELTA proposed. They are on the build branch only, not on `main`, which matches MASTER-DELTA's instruction.
- COVERAGE L23 gives the post's quote count as 4. The X API now returns 5 (likes 334, reposts 123, replies 14 when this review read it). Expected drift, not an error.
- argent#66 itself has not moved: still open, `draft: false`, head `9592dd99`, `updated_at` 2026-10-02T13:47:33Z (15:47 CEST), 0 reviews, 0 comments, 0 review comments, no assignees or requested reviewers ([logs/pr66-snapshot.json](logs/pr66-snapshot.json)).
- **Recommendation:** Mark MASTER-DELTA as applied on `build/2026-10-02` at `0c72511f`.

## R-10 (info): Pin the KIP-20 citation and the post's DOTK link

- COVERAGE [L12](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/blob/a97842da266517c3a5759d5d3375d773f39b5858/COVERAGE.md#L12) cites `kips/blob/master/kip-0020.md (saved copy)` without a commit. This review read [kips `e4ae2332`](https://github.com/kaspanet/kips/blob/e4ae2332117b5cb68bd6188e065ef885b6d17939/kip-0020.md) ("Mark kips 16,17,20,21 as active (#45)", 2026-07-15). Sections 3.1, 3.2, and 4.3 say what the audit quotes, Status Active.
- The post links `dotk-indexer/blob/main/genesis/mainnet.json` (not pinned). The audit pinned `17ca993bec66`. That is still the tip and still blob `99a76792…`, so the audit's pin and the post's link point at the same bytes today.

---

## Confirmed correct (re-checked by this review)

| Audit claim | Where | How confirmed |
| --- | --- | --- |
| PR #66 open, draft false, not merged, mergeable true / blocked, 12 commits, 22 files, +3231/−97, 0 reviews/comments, no assignees/reviewers/labels, base `b312deda` = argent master tip | README, AUDIT header, F12, SECOND-PASS | `gh api` (read-only), [logs/pr66-snapshot.json](logs/pr66-snapshot.json); `git log`/`git diff --stat b312deda..9592dd99` |
| Head date 2026-10-02T13:38:38Z, "remove the impl process from the guide", 102 deletions in the guide only | AUDIT header, F3 | `git show --stat 9592dd99` |
| F1: proof calls `kaspa_consensus_core::hashing::covenant_id::covenant_id`, rejecting empty and non-increasing lists first | AUDIT F1 | [preimage.rs L94-L118](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-genesis/src/preimage.rs#L94-L118) |
| Pin `a41a333b`. `covenant_id.rs` blob `48d8bcc2…` is the same blob at v2.1.0 (`01b532e8`, lightweight tag) | F1, MASTER-DELTA | `git rev-parse` + contents API at both refs. [covenant_id.rs](https://github.com/kaspanet/rusty-kaspa/blob/a41a333b08848f41bf737b72592e463a6011b8ac/consensus/core/src/hashing/covenant_id.rs) |
| `write_len` = `(len as u64).to_le_bytes()`, `write_var_bytes` = len + bytes | F1, I1 | [hashing/mod.rs L50-L52, L86-L88](https://github.com/kaspanet/rusty-kaspa/blob/a41a333b08848f41bf737b72592e463a6011b8ac/consensus/core/src/hashing/mod.rs#L50-L88) |
| `CovenantID` = BLAKE2b, hash length 32, `.key(b"CovenantID")`, same macro as `TransactionID` | F1, I1 | [hashers.rs L22-L32, L88-L113](https://github.com/kaspanet/rusty-kaspa/blob/a41a333b08848f41bf737b72592e463a6011b8ac/crypto/hashes/src/hashers.rs#L88-L113) |
| `Hash` display/FromStr hex-encode without reversing | F1 | [crypto/hashes/src/lib.rs L142-L166](https://github.com/kaspanet/rusty-kaspa/blob/a41a333b08848f41bf737b72592e463a6011b8ac/crypto/hashes/src/lib.rs#L142-L166) |
| KIP-20 §3.1/§3.2 layout and §4.3 grouped validation, strictly increasing indices, Status Active, cites `covenant_id.rs` | F1, F6, I1 | [kip-0020.md @ e4ae2332](https://github.com/kaspanet/kips/blob/e4ae2332117b5cb68bd6188e065ef885b6d17939/kip-0020.md) |
| F6 conclusion (proof order = consensus order) | F6 | see R-02 for the correct citation |
| F3: `docs/followups.md` L157-L164 still says "Implement the layered composition and verification plan…" and this PR wrote that sentence (commit `ea1817c`) | F3, I4 | [followups.md L157-L164](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/docs/followups.md#L157-L164); guide L269-L271, L422-L423 say source package / Sil comparison remain separate |
| F4: compose prints `covenant ID: …` unlabeled | F4 | [src/cli/genesis.rs L112](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/src/cli/genesis.rs#L112) |
| F5: Sil layer materialises redeem script via `materialize_redeem_script` (prefix + encoded state + suffix), then P2SH | F5 | [argent-runtime/src/script.rs](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-runtime/src/script.rs). Tests named in F5 passed here |
| F8: claim checked before external id; consistent replacement claim fails original id | F8 | [package/tests.rs L50-L79](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-genesis/src/package/tests.rs#L50-L79), tests passed |
| `--source` compares artifact ids; ids are verified against content (`verify_id`) on bundle construction; `computed_id_hex` clears `id`, `root`, `modules` under domain `argent/artifact/v1` | F7, "must be fixed" #2 | [argent-artifact/src/lib.rs L132-L190](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/crates/argent-artifact/src/lib.rs#L132-L190); [cli L158-L177](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/src/cli/genesis.rs#L158-L177) |
| I6: `emitter.rs` spawn preimage (version-0, 35-byte P2SH, declaration order), not in the #66 diff | I6, F12 | [emitter.rs L765-L840](https://github.com/argent-lang/argent/blob/9592dd996d2503eb166335d6da92548de193877f/src/compiler/codegen/emitter.rs#L765-L840); `git diff --stat b312deda..HEAD -- src/compiler` is empty |
| F7: issue #57 open, 2026-09-02, 0 comments, four rules; only other "genesis proof" issue; Discussions → HTTP 410 | F7, F12, COVERAGE | `gh api` |
| F10: kccs#26 "Add KCC-23: MJ (Metadata JSON)", head `d51721ad`, open, not merged; `Status: Draft`; §3.3 "launch proof" = both transactions | F10, I7 | [kcc-0023.md @ d51721ad](https://github.com/kaspanet/kccs/blob/d51721ad0ac5fa43679d24dc77aeef4e48da8d0a/kcc-0023.md) |
| V4: KCC-23 vector id `c86366ce…394e` from the KIP-20 layout; reversed txid/digest do not match | VECTORS V4 | independent Python, [logs/R4-R5-kip20-recompute.log](logs/R4-R5-kip20-recompute.log) |
| V5 / F9: DOTK mainnet.json blob `99a76792…` (64711 B), v6, one output (0, 100000000, v0, 35-B SPK) → `ee2128c0…21de`; SPK = `aa20‖BLAKE2b-256(redeem)‖87`; redeem 6342 B = `DotkGap` bytecode; state span {1,66} = state; deed bytecode 3220 B ≠ redeem; `gapTemplateHash` = ABI template hash | VECTORS V5, F9, MASTER-DELTA | same script and log |
| F11: commit `0c70d461` "extract genesis proofs into argent-genesis"; silverscript `3ed97333` = tag v1.0.0, `silverc` at `silverscript-lang/src/bin/silverc.rs`, same rusty-kaspa pin `a41a333b` | F11, COVERAGE | `git log`, `gh api` |
| Post text: "every stateful covenant…", "the goal is a verifiable link from a covenant id back to the source code…", "kudos to @supertypo_kas…", "(not sure if the sil contracts themselves are public yet)"; reply 2106047257867079683 "They will be very soon!" | README, I3, F9 | X API (`get_posts_by_ids`) |
| V1: `argent-genesis` lib 15 passed | VECTORS V1 | reproduced on Linux, [logs/V1-argent-genesis-lib.log](logs/V1-argent-genesis-lib.log) |
| V2: compiler lib 430 passed (7 `genesis_proof`), `tests/genesis_cli.rs` 10 passed | VECTORS V2 | reproduced, [logs/V2-lib-and-genesis_cli.log](logs/V2-lib-and-genesis_cli.log) |
| V3: fixture compose → `656c9d1c…9c48`; verify with `--require-argent --source` exit 0; zero id exit 1 naming both ids | VECTORS V3 | reproduced on Linux with the identical id (cross-platform deterministic), [logs/V3-cli-compose-verify.log](logs/V3-cli-compose-verify.log) |
| Blockers 0; "not a consensus requirement"; KCC-23 not called a standard | README, SECOND-PASS | agree, see sources above |

## Could not be verified

- **U-01. The Discord card** ("Genesis proof tooling [DRAFT]", "wip", "kind of ready"), used in I2, F10, and F12. The audit itself says it was supplied and not reopened. This review had no Discord access either. Treat it as hearsay.
- **U-02. The X quote search** (COVERAGE L23: three named quotes). Not re-run. The audit does not use them as evidence.
- **U-03. Unknown-field behaviour of `silverscript_abi` types inside a Sil-layer package.** Not probed. The Argent-layer and consensus-layer probes are in R-01.
- **U-04. V6 items** (full `cargo test --workspace`, doctests, fmt, clippy, `check.sh --regen-examples`) and the author's "543 tests" figure. Neither the audit nor this review ran them.
- **U-05. On-chain facts for DOTK** (that outpoint `e077087a…:0` exists and was spent, that the registry UTXO carries `ee2128c0…`). No node RPC was used by the audit or by this review. The match is between the manifest and KIP-20 arithmetic only.
- **U-06. Teammate notes.** The task asked this review to ask "kaspa master challenge" and "kaspa master bot" for notes. This executor had no agent-messaging tool, so they were not contacted. As a substitute, every branch of `STP-KAS/kaspa-master-file` was searched for `argent#66`, "genesis proof", or this repo name. Matches were only on `main`, `build/2026-10-02`, `build/api-tn10-2026-10-02`, and `build/kcc-last-call-2026-10-02`. No `challenge/*` branch mentions them.

## Open questions

1. Should argent#66 rely on `deny_unknown_fields` everywhere, or should it declare that only the typed re-serialization is authoritative? The second is easier to keep correct across the `Artifact` and silverscript-abi trees (R-01).
2. Should `argentc genesis verify` require an explicit `--layer consensus` (or warn) before accepting a consensus-only package, given #57 rule 2 (R-03)?
3. Was the audited repo meant to be private (R-05)? stp's current instruction says the challenge repos are public.
