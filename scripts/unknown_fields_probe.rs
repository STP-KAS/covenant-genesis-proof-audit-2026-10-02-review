//! Review probe (not part of argent#66). Copy to crates/argent-genesis/tests/ in a
//! scratch checkout of 9592dd99 and run: cargo test -p argent-genesis --test unknown_fields_probe -- --nocapture
//! It plants annotations that a human might read as part of the proof and checks
//! whether `GenesisProofPackage::from_json` + `verify` accept them.
use argent_genesis::{ConsensusGenesisProof, GenesisProofPackage, IndexedGenesisOutput};
use kaspa_consensus_core::{
    Hash,
    tx::{ScriptPublicKey, TransactionOutpoint},
};
use serde_json::json;

fn package() -> GenesisProofPackage {
    let proof = ConsensusGenesisProof::compose(
        TransactionOutpoint::new(Hash::from_bytes([0x11; 32]), 7),
        vec![IndexedGenesisOutput::new(0, 1_000, ScriptPublicKey::new(0, vec![0x51].into()))],
    )
    .expect("compose");
    GenesisProofPackage::new(proof)
}

fn probe(label: &str, mutate: impl Fn(&mut serde_json::Value)) -> bool {
    let pkg = package();
    let id = match &pkg.proof {
        argent_genesis::GenesisProofLayer::Consensus(p) => p.claimed_covenant_id,
        _ => unreachable!(),
    };
    let mut v = serde_json::to_value(&pkg).unwrap();
    mutate(&mut v);
    let accepted = match GenesisProofPackage::from_json(&v.to_string()) {
        Ok(decoded) => decoded.verify(id).is_ok(),
        Err(_) => false,
    };
    println!("PROBE {label}: accepted_and_verified={accepted}");
    accepted
}

#[test]
fn unknown_field_probe() {
    let envelope = probe("envelope.audited", |v| v["audited"] = json!(true));
    let layer = probe("proof.audited (next to kind/value)", |v| v["proof"]["audited"] = json!(true));
    let inner = probe("proof.value.audited (ConsensusGenesisProof)", |v| v["proof"]["value"]["audited"] = json!(true));
    let output = probe("proof.value.outputs[0].source_url (IndexedGenesisOutput)", |v| {
        v["proof"]["value"]["outputs"][0]["source_url"] = json!("https://example.invalid/app.ag")
    });
    // Documented expectations from the audited repo's F2: envelope and layer reject; inner objects accept.
    assert!(!envelope && !layer, "envelope/layer should reject unknown fields");
    println!("RESULT inner_accepts={inner} output_accepts={output}");
}
