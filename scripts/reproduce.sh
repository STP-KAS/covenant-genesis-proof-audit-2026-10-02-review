#!/usr/bin/env bash
# Reproduce this review's runs on Linux. Needs git, python3, rustup (Rust 1.97.1).
# Runs nothing against a node and pushes nothing anywhere.
set -euo pipefail
WORK=${WORK:-$PWD/work}; mkdir -p "$WORK"; cd "$WORK"
HERE=$(cd "$(dirname "$0")" && pwd)
ARGENT_HEAD=9592dd996d2503eb166335d6da92548de193877f
DOTK_TIP=17ca993bec669fe2e8cc0be2b708bfbe0137ba46
ID=656c9d1c4d30b77b2418ed4ad1421315eef55fcf852393bc09183b95983a9c48

# R4/R5: independent KIP-20 recompute (KCC-23 vector + DOTK mainnet binding)
curl -sfL "https://raw.githubusercontent.com/supertypo/dotk-indexer/$DOTK_TIP/genesis/mainnet.json" -o dotk-mainnet.json
python3 "$HERE/kip20_recompute.py" dotk-mainnet.json

# V1-V3: argent#66 head
[ -d argent ] || git clone -q https://github.com/argent-lang/argent argent
cd argent && git fetch -q origin pull/66/head && git checkout -q "$ARGENT_HEAD"
rustup toolchain install 1.97.1 --profile minimal >/dev/null
cargo +1.97.1 test -p argent-genesis --lib -- --test-threads=8
cargo +1.97.1 test --test genesis_cli --lib -- --test-threads=8
T=$(mktemp -d)
cargo +1.97.1 run -q -- genesis compose tests/fixtures/emit/capsule_route_context/app.ag \
  --bootstrap tests/fixtures/genesis_cli/expanded.json --out "$T/p.json"
cargo +1.97.1 run -q -- genesis verify "$T/p.json" --covenant-id $ID --require-argent \
  --source tests/fixtures/emit/capsule_route_context/app.ag
cargo +1.97.1 run -q -- genesis verify "$T/p.json" --covenant-id $(printf '0%.0s' {1..64}) --require-argent || echo "zero id rejected (expected)"

# P2: annotations inside the package survive verify (F2 scope)
python3 - "$T" <<'PY'
import json, sys
t = sys.argv[1]; p = json.load(open(f"{t}/p.json"))
p["proof"]["value"]["proof"]["outputs"][0]["audited_by"] = "example auditor"
p["proof"]["value"]["primary"]["audit_status"] = "verified"
json.dump(p, open(f"{t}/annotated.json", "w"))
PY
cargo +1.97.1 run -q -- genesis verify "$T/annotated.json" --covenant-id $ID --require-argent \
  --source tests/fixtures/emit/capsule_route_context/app.ag

# P1: library-level probe in a throwaway copy of the test file (not committed to argent)
cp "$HERE/unknown_fields_probe.rs" crates/argent-genesis/tests/ 2>/dev/null || { mkdir -p crates/argent-genesis/tests; cp "$HERE/unknown_fields_probe.rs" crates/argent-genesis/tests/; }
cargo +1.97.1 test -p argent-genesis --test unknown_fields_probe -- --nocapture
rm crates/argent-genesis/tests/unknown_fields_probe.rs
