"""Verify archived review evidence without network access or executing upstream code."""

import hashlib
import json
from pathlib import Path


def main():
    review_root = Path(__file__).resolve().parent
    manifest = json.loads((review_root / "source_manifest.json").read_text())
    deeper_manifest = json.loads((review_root / "deeper_review_manifest.json").read_text())
    long_run_manifest = json.loads((review_root / "long_run_review_manifest.json").read_text())
    planning_manifest = json.loads((review_root / "planning_input_audit_manifest.json").read_text())
    snapshots = manifest["snapshots"] + deeper_manifest["snapshots"] + long_run_manifest["snapshots"] + planning_manifest["snapshots"]
    for source in snapshots:
        source_path = (review_root / source["local_path"]).resolve()
        if not source_path.is_relative_to(review_root):
            raise ValueError("Snapshot path leaves review directory")
        source_bytes = source_path.read_bytes()
        if len(source_bytes) != source["size_bytes"]:
            raise ValueError(f"Size mismatch: {source_path.name}")
        if hashlib.sha256(source_bytes).hexdigest() != source["sha256"]:
            raise ValueError(f"Hash mismatch: {source_path.name}")
        if source_path.suffix == ".pdf" and not source_bytes.startswith(b"%PDF"):
            raise ValueError(f"Not a PDF: {source_path.name}")
        for expected_text in source.get("expected_text", []):
            if expected_text not in source_bytes.decode("utf-8"):
                raise ValueError(f"Expected evidence missing: {source_path.name}: {expected_text}")

    repository_root = review_root.parent
    repository_inputs = long_run_manifest["repository_inputs"] + planning_manifest["repository_inputs"]
    primary_reference = planning_manifest["existing_primary_input"]
    linked_primary = next(source for source in long_run_manifest["repository_inputs"] if source["source_id"] == "L6")
    if primary_reference["repository_path"] != linked_primary["repository_path"]:
        raise ValueError("Planning audit primary-source reference changed")
    primary_page_record = {**primary_reference, "pdf_pages": linked_primary["pdf_pages"]}
    for source in repository_inputs:
        source_path = (repository_root / source["repository_path"]).resolve()
        if not source_path.is_relative_to(repository_root):
            raise ValueError("Input path leaves repository")
        source_bytes = source_path.read_bytes()
        if len(source_bytes) != source["size_bytes"]:
            raise ValueError(f"Size mismatch: {source_path.name}")
        if hashlib.sha256(source_bytes).hexdigest() != source["sha256"]:
            raise ValueError(f"Hash mismatch: {source_path.name}")
        if source["format"] == "pdf" and not source_bytes.startswith(b"%PDF"):
            raise ValueError(f"Not a PDF: {source_path.name}")

    for source in snapshots + repository_inputs + [primary_page_record]:
        if "inspected_pdf_pages" in source:
            reviewed_pages = source.get("inspected_pdf_pages", [])
            if not reviewed_pages or any(page < 1 or page > source["pdf_pages"] for page in reviewed_pages):
                raise ValueError(f"Invalid reviewed page range: {source['source_id']}")
            if not set(source.get("visually_checked_pdf_pages", [])).issubset(reviewed_pages):
                raise ValueError(f"Visual check outside reviewed pages: {source['source_id']}")

    notebook_path = review_root / manifest["notebook_audit"]["local_path"]
    notebook = json.loads(notebook_path.read_text())
    preprocessing = "".join(notebook["cells"][11]["source"])
    loss_definition = "".join(notebook["cells"][17]["source"])
    expected_fragments = [
        "np.random.shuffle(set_assignments)",
        "percent_train, percent_val, percent_test = .6, .2, .2",
        "feature_cols = ['Load', 'VRE', 'Hour', 'Day_of_Year', \"Hours_since_2018\"]",
        "scaler.fit(train_x)",
    ]
    for fragment in expected_fragments:
        if fragment not in preprocessing:
            raise ValueError(f"Notebook evidence changed: {fragment}")
    if "delta_load_tensor" not in loss_definition or "delta_vre_tensor" not in loss_definition:
        raise ValueError("Expected emissions-response loss inputs missing")

    print(f"PASS: {len(snapshots)} snapshot hashes and sizes; PDF signatures; notebook evidence.")
    print(f"PASS: {len(repository_inputs)} existing input hashes; text markers; reviewed-page bounds.")
    print("This checks evidence integrity, not MEF validity or forecast performance.")


if __name__ == "__main__":
    main()
