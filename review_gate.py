
import json
from datetime import datetime
import uuid


def review_gate_v1(report, decision, reviewer_note=""):
    allowed_decisions = {"approve", "edit", "reject"}

    if decision not in allowed_decisions:
        raise ValueError(
            f"Invalid decision: {decision}. "
            f"Allowed decisions are: {sorted(allowed_decisions)}"
        )

    run_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()

    result = {
        "decision": decision,
        "reviewer_note": reviewer_note,
        "external_use_allowed": decision == "approve",
        "reviewed_at": timestamp
    }

    audit_entry = {
        "timestamp": timestamp,
        "run_id": run_id,
        "region": "all_flagged_regions",
        "decision": decision,
        "reviewer_note": reviewer_note
    }

    with open("audit_log.jsonl", "a") as f:
        f.write(json.dumps(audit_entry) + "\n")

    return result


if __name__ == "__main__":

    report = {"status": "draft"}

    # Start with a fresh audit log
    open("audit_log.jsonl", "w").close()

    review_gate_v1(
        report,
        "approve",
        "Approved for external use."
    )

    review_gate_v1(
        report,
        "edit",
        "Edit required before external use."
    )

    review_gate_v1(
        report,
        "reject",
        "Rejected pending further validation."
    )

    with open("audit_log.jsonl") as f:
        entries = [json.loads(line) for line in f if line.strip()]

    print("Audit entries:", len(entries))

    required_fields = {
        "timestamp",
        "run_id",
        "region",
        "decision",
        "reviewer_note"
    }

    print(
        "All entries contain required fields:",
        all(required_fields.issubset(entry.keys()) for entry in entries)
    )
