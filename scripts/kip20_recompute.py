#!/usr/bin/env python3
"""Independent KIP-20 section 3.2 covenant-id recompute (no Argent / rusty-kaspa code).

covenant_id(O, auth_outputs) = BLAKE2b-256 keyed "CovenantID" over
  O.tx_id (32 raw bytes, no reversal) || le_u32(O.index) || le_u64(n)
  || for each (idx, out): le_u32(idx) || le_u64(value) || le_u16(version)
                          || le_u64(len(script)) || script

Usage: python3 kip20_recompute.py path/to/dotk-mainnet.json
"""
import hashlib, json, struct, sys

def covenant_id(txid_hex, out_index, outputs):
    h = hashlib.blake2b(digest_size=32, key=b"CovenantID")
    h.update(bytes.fromhex(txid_hex))
    h.update(struct.pack("<I", out_index))
    h.update(struct.pack("<Q", len(outputs)))
    for idx, value, version, script in outputs:
        h.update(struct.pack("<I", idx)); h.update(struct.pack("<Q", value))
        h.update(struct.pack("<H", version)); h.update(struct.pack("<Q", len(script))); h.update(script)
    return h.hexdigest()

def rev(x): return bytes.fromhex(x)[::-1].hex()

def report(name, got, expected):
    print(f"{name}: computed {got}\n{' '*len(name)}  expected {expected}  -> {'MATCH' if got == expected else 'MISMATCH'}")
    return got == expected

ok = True
# V4: KCC-23 conformance vector (kaspanet/kccs@d51721ad, kcc-0023.md section 6)
prep = "206a0c31dbe45384b86de451a177fd7c8e986d278f2a86724d941937443113ef"
exp4 = "c86366cec738e9a1578b2d871ee493dcaabfd79156810f13f3b62429859e394e"
ok &= report("KCC-23 vector", covenant_id(prep, 0, [(0, 90_000_000, 0, b"\x51")]), exp4)
print("  reversed txid:", covenant_id(rev(prep), 0, [(0, 90_000_000, 0, b"\x51")]) == exp4,
      "| reversed digest:", rev(covenant_id(prep, 0, [(0, 90_000_000, 0, b"\x51")])) == exp4)

if len(sys.argv) > 1:
    raw = open(sys.argv[1], "rb").read()
    d = json.loads(raw)
    print("manifest bytes:", len(raw), "version:", d["version"], "network:", d["network"])
    g = d["genesisBinding"]; op = g["authorizingOutpoint"]; outs = g["authorizedOutputs"]
    print("authorizedOutputs:", len(outs), "| keys:", sorted(outs[0].keys()), "| outputIndex:", g.get("outputIndex"))
    tup = [(o["index"], o["value"], o["scriptVersion"], bytes.fromhex(o["scriptPublicKey"])) for o in outs]
    cid = covenant_id(op["transactionId"], op["index"], tup)
    ok &= report("DOTK registry", cid, d["registryCovenantId"])
    print("  reversed txid matches:", covenant_id(rev(op["transactionId"]), op["index"], tup) == d["registryCovenantId"],
          "| reversed digest matches:", rev(cid) == d["registryCovenantId"])
    o = outs[0]; spk = bytes.fromhex(o["scriptPublicKey"]); rs = bytes.fromhex(o["redeemScript"])
    print("output0: index", o["index"], "value", o["value"], "scriptVersion", o["scriptVersion"], "spk len", len(spk), "redeem len", len(rs))
    p2sh = b"\xaa\x20" + hashlib.blake2b(rs, digest_size=32).digest() + b"\x87"
    print("spk == aa20||blake2b256(redeem)||87 (unkeyed):", spk == p2sh)
    def find_bytecode(abi, name):
        c = abi["contracts"][name] if "contracts" in abi else None
        return c
    gap = d["gapAbi"]; deed = d["deedAbi"]
    print("gapAbi keys:", sorted(gap.keys())[:12])
    print("gapAbi.contracts:", list(gap.get("contracts", {}).keys()), "| deedAbi.contracts:", list(deed.get("contracts", {}).keys()))
    def bc(abi):
        out = {}
        for n, c in abi.get("contracts", {}).items():
            comp = c.get("compiled", {})
            b = comp.get("bytecode")
            if b is not None:
                out[n] = bytes(b) if isinstance(b, list) else bytes.fromhex(b)
        return out
    gb = bc(gap); db = bc(deed)
    for n, b in gb.items(): print(f"gap contract {n}: bytecode len {len(b)}; equals redeemScript: {b == rs}")
    for n, b in db.items(): print(f"deed contract {n}: bytecode len {len(b)}; equals redeemScript: {b == rs}")
    for k in ("stateSpan", "state"):
        if k in o: print(k, "=", o[k] if k == "stateSpan" else (o[k][:16] + "... len " + str(len(bytes.fromhex(o[k])))))
    if "stateSpan" in o and "state" in o:
        sp = o["stateSpan"]; st = bytes.fromhex(o["state"])
        print("redeem[offset:offset+len] == state:", rs[sp["offset"]:sp["offset"] + sp["len"]] == st)
    dth = bytes.fromhex(d["deedTemplateHash"])
    print("deedTemplateHash offset in redeemScript:", rs.find(dth), "| occurrences:", rs.count(dth))
    gth = bytes.fromhex(d["gapTemplateHash"])
    for n, c in gap.get("contracts", {}).items():
        th = c.get("compiled", {}).get("template_hash") or c.get("template_hash")
        if th is not None:
            thb = bytes(th) if isinstance(th, list) else bytes.fromhex(th)
            print(f"gapTemplateHash == gapAbi.{n} template_hash: {thb == gth}")
print("ALL CORE MATCHES:", bool(ok))
sys.exit(0 if ok else 1)
