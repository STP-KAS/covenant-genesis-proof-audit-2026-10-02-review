# Sources

All read on 2026-10-02 between about 20:57 and 21:30 CEST. GitHub was read through `gh api` and `git clone`/`fetch` only. Nothing was written to any repo except this one.

## Audited repo
- STP-KAS/covenant-genesis-proof-audit-2026-10-02 @ [`a97842da266517c3a5759d5d3375d773f39b5858`](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/tree/a97842da266517c3a5759d5d3375d773f39b5858) (parent [`fad7c0c1`](https://github.com/STP-KAS/covenant-genesis-proof-audit-2026-10-02/commit/fad7c0c13d01de514bb88a55950d76a502167006)). `gh repo view`: visibility PUBLIC, created 2026-10-02T18:23:46Z.

## argent
- PR [argent-lang/argent#66](https://github.com/argent-lang/argent/pull/66): API `repos/argent-lang/argent/pulls/66`, `/pulls/66/reviews`, `/pulls/66/comments`, `/issues/66/comments` ([logs/pr66-snapshot.json](logs/pr66-snapshot.json))
- Head [`9592dd996d2503eb166335d6da92548de193877f`](https://github.com/argent-lang/argent/tree/9592dd996d2503eb166335d6da92548de193877f), base / master [`b312deda6fe10f6493c8d49eb748e3f61860458a`](https://github.com/argent-lang/argent/commit/b312deda6fe10f6493c8d49eb748e3f61860458a)
- Files at head: `crates/argent-genesis/src/{preimage,sil,ag,package,lib}.rs`, `package/tests.rs`, `crates/argent-runtime/src/{lib,script}.rs`, `crates/argent-artifact/src/lib.rs`, `src/cli/genesis.rs`, `src/compiler/codegen/emitter.rs`, `docs/followups.md`, `docs/genesis-proof-tooling.md`, `Cargo.toml`
- Commits [`0c70d461`](https://github.com/argent-lang/argent/commit/0c70d461ab70f05bb0367c3e13b3bfc85f0e6ba4), [`554f221c`](https://github.com/argent-lang/argent/commit/554f221c34b701bf0ad93112e920faee93ae7a90), `ea1817c` (first commit, wrote the followups sentence)
- Issue [argent#57](https://github.com/argent-lang/argent/issues/57). Issue search `repo:argent-lang/argent "genesis proof"` and `genesis`. `repos/argent-lang/argent/discussions` returns HTTP 410, `has_discussions: false`

## Kaspa upstream
- rusty-kaspa [`a41a333b08848f41bf737b72592e463a6011b8ac`](https://github.com/kaspanet/rusty-kaspa/tree/a41a333b08848f41bf737b72592e463a6011b8ac): `consensus/core/src/hashing/covenant_id.rs` (blob `48d8bcc23de775464cf6e7b51db7055508792bea`), `consensus/core/src/hashing/mod.rs`, `crypto/hashes/src/{hashers,lib}.rs`, `consensus/core/src/tx.rs`, `crypto/txscript/src/covenants.rs`, `consensus/src/processes/transaction_validator/tx_validation_in_utxo_context.rs`, `consensus/client/src/transaction.rs`
- rusty-kaspa tag v2.1.0, which points to commit [`01b532e8b553523216471682649693af92f0fd16`](https://github.com/kaspanet/rusty-kaspa/tree/01b532e8b553523216471682649693af92f0fd16). Same `covenant_id.rs` blob
- KIPs [`e4ae2332117b5cb68bd6188e065ef885b6d17939`](https://github.com/kaspanet/kips/blob/e4ae2332117b5cb68bd6188e065ef885b6d17939/kip-0020.md) `kip-0020.md` (Status Active, §3.1, §3.2, §4.3, Reference Implementation)
- KCCs PR [kaspanet/kccs#26](https://github.com/kaspanet/kccs/pull/26) (open, not merged), `kcc-0023.md` @ [`d51721ad0ac5fa43679d24dc77aeef4e48da8d0a`](https://github.com/kaspanet/kccs/blob/d51721ad0ac5fa43679d24dc77aeef4e48da8d0a/kcc-0023.md) (Status Draft, §3.3, §6 vector)
- silverscript [`3ed973335b59269293564805cc2c58a14595ec03`](https://github.com/kaspanet/silverscript/tree/3ed973335b59269293564805cc2c58a14595ec03) = tag v1.0.0 = master tip: `Cargo.toml` (rusty-kaspa pin), `silverscript-lang/src/bin/silverc.rs`

## DOTK (supertypo)
- dotk-indexer [`17ca993bec669fe2e8cc0be2b708bfbe0137ba46`](https://github.com/supertypo/dotk-indexer/tree/17ca993bec669fe2e8cc0be2b708bfbe0137ba46) (tip, 2026-10-02T09:45:15Z): recursive tree (134 entries, not truncated), [`genesis/mainnet.json`](https://github.com/supertypo/dotk-indexer/blob/17ca993bec669fe2e8cc0be2b708bfbe0137ba46/genesis/mainnet.json) blob `99a7679242ebf3816d0e656f67488ad7e36999a9`, 64711 bytes
- dotk-core [`5a0e6ae1`](https://github.com/supertypo/dotk-core/tree/5a0e6ae101622e9f7769a02a557c8cea386555ea), dotk-sdk [`c9194976`](https://github.com/supertypo/dotk-sdk/tree/c919497661ea999d267fd06cbc30014872a31776), dotk-sdk-tx [`d9d9a595`](https://github.com/supertypo/dotk-sdk-tx/tree/d9d9a59535bb0897f777afed040afab9f2730e52): recursive trees, none truncated
- GitHub code search `DotkGap`. `users/supertypo/repos`

## X
- Post [2106033659698450492](https://x.com/michaelsuttonil/status/2106033659698450492) (michaelsuttonil, 2026-10-02T14:48:47Z) and reply [2106047257867079683](https://x.com/supertypo_kas/status/2106047257867079683) (supertypo_kas, 15:42:49Z), read through the X API `get_posts_by_ids` (note_tweet text, expanded URLs, public metrics)

## STP-KAS master file
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file): `main` [`99ae9620`](https://github.com/STP-KAS/kaspa-master-file/commit/99ae9620dd580ff0630cd720f83a0e78de616f4e), `build/2026-10-02` [`0c72511f`](https://github.com/STP-KAS/kaspa-master-file/commit/0c72511fdc1a809fe177e0f267ee89eeea8fb230). All remote branches searched for `argent#66` / genesis proof

## Local runs (box: Linux, rustc/cargo 1.97.1, Python 3.13.5)
- [logs/V1-argent-genesis-lib.log](logs/V1-argent-genesis-lib.log), [logs/V2-lib-and-genesis_cli.log](logs/V2-lib-and-genesis_cli.log), [logs/V3-cli-compose-verify.log](logs/V3-cli-compose-verify.log), [logs/P1-unknown-fields-probe.log](logs/P1-unknown-fields-probe.log), [logs/P2-cli-annotated-package.log](logs/P2-cli-annotated-package.log), [logs/R4-R5-kip20-recompute.log](logs/R4-R5-kip20-recompute.log), [logs/environment.txt](logs/environment.txt)

## Not used
- Discord, Telegram, any Kaspa node or RPC, teammate agents (no messaging tool available to this executor)
