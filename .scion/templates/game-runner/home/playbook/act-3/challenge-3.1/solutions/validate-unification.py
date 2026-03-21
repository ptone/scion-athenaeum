#!/usr/bin/env python3
"""
Validate the unified codex partial submission for Challenge 3.1.
Usage: python validate-unification.py <path-to-unified-codex.json>
"""

import json
import hashlib
import sys
import os

def compute_integrity_hash(fragments):
    """Compute SHA-256 hash of fragment contents concatenated in sequence order."""
    sorted_frags = sorted(fragments, key=lambda f: f["sequence_number"])
    hash_input = ""
    for frag in sorted_frags:
        hash_input += json.dumps(frag["content"], separators=(',', ':'), sort_keys=True)
    return "sha256:" + hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

def validate(filepath):
    errors = []
    warnings = []

    # Load submission
    try:
        with open(filepath) as f:
            data = json.load(f)
    except Exception as e:
        print(f"FAIL: Could not load JSON: {e}")
        return False

    # Check top-level structure
    if "codex_partial" not in data:
        errors.append("Missing top-level key 'codex_partial'")
        print(f"FAIL: {errors[-1]}")
        return False

    codex = data["codex_partial"]

    # Check fragment count
    if codex.get("fragments_unified") != 3:
        errors.append(f"Expected fragments_unified=3, got {codex.get('fragments_unified')}")

    if codex.get("fragments_remaining") != 2:
        errors.append(f"Expected fragments_remaining=2, got {codex.get('fragments_remaining')}")

    # Check fragments present
    fragments = codex.get("fragments", [])
    if len(fragments) != 3:
        errors.append(f"Expected 3 fragments, got {len(fragments)}")
    else:
        frag_ids = sorted([f.get("fragment_id") for f in fragments])
        if frag_ids != ["A", "B", "C"]:
            errors.append(f"Expected fragment IDs ['A', 'B', 'C'], got {frag_ids}")

        # Validate fragment data
        expected_domains = {"A": "history", "B": "geography", "C": "mathematics"}
        expected_record_counts = {"A": 5, "B": 5, "C": 5}
        for frag in fragments:
            fid = frag.get("fragment_id")
            domain = frag.get("content", {}).get("domain")
            if domain != expected_domains.get(fid):
                errors.append(f"Fragment {fid}: expected domain '{expected_domains.get(fid)}', got '{domain}'")
            records = frag.get("content", {}).get("records", [])
            if len(records) != expected_record_counts.get(fid, 0):
                errors.append(f"Fragment {fid}: expected {expected_record_counts.get(fid)} records, got {len(records)}")

    # Check cross-references
    expected_refs = {
        "ANCHOR-A-5e8d1f": {"fragment": "A", "record": "R001"},
        "ANCHOR-A-3f7b4c": {"fragment": "A", "record": "R003"},
        "ANCHOR-B-7f3a9d": {"fragment": "B", "record": "G001"},
        "ANCHOR-B-1a6e5d": {"fragment": "B", "record": "G003"},
        "ANCHOR-C-2d1e8b": {"fragment": "C", "record": "T001"},
        "ANCHOR-C-9b4c2e": {"fragment": "C", "record": "T003"}
    }
    cross_refs = codex.get("cross_references_resolved", {})
    for anchor_id, expected_val in expected_refs.items():
        if anchor_id not in cross_refs:
            errors.append(f"Missing cross-reference: {anchor_id}")
        elif cross_refs[anchor_id] != expected_val:
            errors.append(f"Cross-reference {anchor_id}: expected {expected_val}, got {cross_refs[anchor_id]}")

    # Check integrity hash
    if len(fragments) == 3:
        expected_hash = compute_integrity_hash(fragments)
        actual_hash = codex.get("integrity_hash", "")
        if actual_hash != expected_hash:
            errors.append(f"Integrity hash mismatch: expected {expected_hash}, got {actual_hash}")

    # Report
    if errors:
        print("FAIL: Unified codex validation failed.")
        for e in errors:
            print(f"  ERROR: {e}")
        return False
    else:
        print("PASS: Unified codex partial is valid.")
        print(f"  Fragments unified: {codex['fragments_unified']}")
        print(f"  Cross-references resolved: {len(cross_refs)}")
        print(f"  Integrity hash: {codex['integrity_hash']}")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Default path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, "unified-codex-partial.json")
        if not os.path.exists(filepath):
            print("Usage: python validate-unification.py <path-to-unified-codex.json>")
            sys.exit(1)
    else:
        filepath = sys.argv[1]

    success = validate(filepath)
    sys.exit(0 if success else 1)
