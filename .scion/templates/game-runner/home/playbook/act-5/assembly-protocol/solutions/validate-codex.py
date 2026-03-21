#!/usr/bin/env python3
"""
Validate the complete Codex Machina submission for Challenge 5.1.
Usage: python validate-codex.py <path-to-complete-codex.json>
"""

import json
import hashlib
import sys
import os

def compute_integrity_hash(fragments):
    """Compute SHA-256 hash of all fragment contents concatenated in sequence order."""
    sorted_frags = sorted(fragments, key=lambda f: f["sequence_number"])
    hash_input = ""
    for frag in sorted_frags:
        hash_input += json.dumps(frag["content"], separators=(',', ':'), sort_keys=True)
    return "sha256:" + hashlib.sha256(hash_input.encode('utf-8')).hexdigest()

EXPECTED_FRAGMENTS = {
    "A": {
        "sequence_number": 1,
        "realm_origin": "Realm of Formats",
        "domain": "history",
        "record_count": 5,
        "first_record_id": "R001",
        "last_record_id": "R005"
    },
    "B": {
        "sequence_number": 2,
        "realm_origin": "Realm of APIs",
        "domain": "geography",
        "record_count": 5,
        "first_record_id": "G001",
        "last_record_id": "G005"
    },
    "C": {
        "sequence_number": 3,
        "realm_origin": "Realm of Patterns",
        "domain": "mathematics",
        "record_count": 5,
        "first_record_id": "T001",
        "last_record_id": "T005"
    },
    "D": {
        "sequence_number": 4,
        "realm_origin": "The Deep Archive",
        "domain": "arts",
        "record_count": 5,
        "first_record_id": "A001",
        "last_record_id": "A005"
    },
    "E": {
        "sequence_number": 5,
        "realm_origin": "The Deep Archive",
        "domain": "governance",
        "record_count": 5,
        "first_record_id": "L001",
        "last_record_id": "L005"
    }
}

EXPECTED_CROSS_REFS = {
    "ANCHOR-A-5e8d1f": {"fragment": "A", "record": "R001"},
    "ANCHOR-A-3f7b4c": {"fragment": "A", "record": "R003"},
    "ANCHOR-B-7f3a9d": {"fragment": "B", "record": "G001"},
    "ANCHOR-B-1a6e5d": {"fragment": "B", "record": "G003"},
    "ANCHOR-C-2d1e8b": {"fragment": "C", "record": "T001"},
    "ANCHOR-C-9b4c2e": {"fragment": "C", "record": "T003"}
}

def validate(filepath):
    errors = []

    # Load submission
    try:
        with open(filepath) as f:
            data = json.load(f)
    except Exception as e:
        print(f"FAIL: Could not load JSON: {e}")
        return False

    # Check top-level structure
    if "codex_machina" not in data:
        errors.append("Missing top-level key 'codex_machina'")
        print(f"FAIL: {errors[-1]}")
        return False

    codex = data["codex_machina"]

    # Check metadata
    if codex.get("title") != "The Complete Codex Machina":
        errors.append(f"Wrong title: {codex.get('title')}")
    if codex.get("fragments_count") != 5:
        errors.append(f"Expected fragments_count=5, got {codex.get('fragments_count')}")
    if codex.get("status") != "RESTORED":
        errors.append(f"Expected status='RESTORED', got {codex.get('status')}")

    # Check all 5 fragments
    fragments = codex.get("fragments", [])
    if len(fragments) != 5:
        errors.append(f"Expected 5 fragments, got {len(fragments)}")
    else:
        frag_ids = sorted([f.get("fragment_id") for f in fragments])
        if frag_ids != ["A", "B", "C", "D", "E"]:
            errors.append(f"Expected fragment IDs ['A','B','C','D','E'], got {frag_ids}")

        # Check correct order (sequence numbers)
        for i, frag in enumerate(fragments):
            if frag.get("sequence_number") != i + 1:
                errors.append(f"Fragment at index {i}: expected sequence_number={i+1}, got {frag.get('sequence_number')}")

        # Validate each fragment's data
        for frag in fragments:
            fid = frag.get("fragment_id")
            if fid not in EXPECTED_FRAGMENTS:
                errors.append(f"Unknown fragment_id: {fid}")
                continue
            expected = EXPECTED_FRAGMENTS[fid]

            if frag.get("sequence_number") != expected["sequence_number"]:
                errors.append(f"Fragment {fid}: wrong sequence_number")
            if frag.get("realm_origin") != expected["realm_origin"]:
                errors.append(f"Fragment {fid}: wrong realm_origin")

            content = frag.get("content", {})
            if content.get("domain") != expected["domain"]:
                errors.append(f"Fragment {fid}: expected domain '{expected['domain']}', got '{content.get('domain')}'")

            records = content.get("records", [])
            if len(records) != expected["record_count"]:
                errors.append(f"Fragment {fid}: expected {expected['record_count']} records, got {len(records)}")
            else:
                if records[0].get("id") != expected["first_record_id"]:
                    errors.append(f"Fragment {fid}: first record should be {expected['first_record_id']}")
                if records[-1].get("id") != expected["last_record_id"]:
                    errors.append(f"Fragment {fid}: last record should be {expected['last_record_id']}")

    # Check cross-references
    cross_refs = codex.get("cross_references", {})
    for anchor_id, expected_val in EXPECTED_CROSS_REFS.items():
        if anchor_id not in cross_refs:
            errors.append(f"Missing cross-reference: {anchor_id}")
        elif cross_refs[anchor_id] != expected_val:
            errors.append(f"Cross-reference {anchor_id}: expected {expected_val}, got {cross_refs[anchor_id]}")

    # Check integrity hash
    if len(fragments) == 5:
        expected_hash = compute_integrity_hash(fragments)
        actual_hash = codex.get("integrity_hash", "")
        if actual_hash != expected_hash:
            errors.append(f"Integrity hash mismatch: expected {expected_hash}, got {actual_hash}")

    # Report
    if errors:
        print("FAIL: Codex Machina validation failed.")
        for e in errors:
            print(f"  ERROR: {e}")
        return False
    else:
        print("PASS: The Codex Machina is fully restored.")
        print(f"  Title: {codex['title']}")
        print(f"  Fragments: {codex['fragments_count']}")
        print(f"  Cross-references: {len(cross_refs)}")
        print(f"  Integrity hash: {codex['integrity_hash']}")
        print(f"  Status: {codex['status']}")
        print()
        print("  The Athenaeum is whole once more.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, "complete-codex.json")
        if not os.path.exists(filepath):
            print("Usage: python validate-codex.py <path-to-complete-codex.json>")
            sys.exit(1)
    else:
        filepath = sys.argv[1]

    success = validate(filepath)
    sys.exit(0 if success else 1)
