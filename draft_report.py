
import json


def draft_report_v1(flagged_regions, metrics):
    report = []

    for region in sorted(flagged_regions):
        m = metrics[region]

        report.append({
            "region": region,
            "context": (
                f"{region} was flagged because its sales movement crossed "
                "the 8% significance threshold."
            ),
            "evidence": {
                "april_sales": m["april_sales"],
                "may_sales": m["may_sales"],
                "june_sales": m["june_sales"],
                "april_may_change": m["april_may_change"],
                "may_june_change": m["may_june_change"]
            },
            "insight": (
                f"{region} showed a material month-over-month sales movement "
                "across the reviewed period."
            ),
            "implication": (
                "Review the regional movement and validate the underlying "
                "business context before taking further action."
            )
        })

    return report


if __name__ == "__main__":

    flagged_regions = [
        "Bengaluru",
        "Guntur",
        "Hyderabad",
        "Karimnagar",
        "Tirupati",
        "Vijayawada",
        "Visakhapatnam",
        "Warangal"
    ]

    metrics = {
        "Guntur": {
            "april_sales": 62442.27,
            "may_sales": 138738.93,
            "june_sales": 99745.18,
            "april_may_change": 122.19,
            "may_june_change": -28.11
        }
    }

    report = draft_report_v1(flagged_regions, {
        region: metrics.get(region, {
            "april_sales": 0,
            "may_sales": 0,
            "june_sales": 0,
            "april_may_change": 0,
            "may_june_change": 0
        })
        for region in flagged_regions
    })

    print("CII blocks generated:", len(report))
    print("Report generated successfully")

    with open("draft_report.json", "w") as f:
        json.dump(report, f, indent=2)
