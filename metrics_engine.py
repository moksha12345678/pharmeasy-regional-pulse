
import json


def compute_percentage_change_v1(current, previous):
    if previous == 0:
        return 0

    return round(((current - previous) / previous) * 100, 2)


def flag_significant_regions_v1(changes, threshold=8):
    return {
        region: change
        for region, change in changes.items()
        if abs(change) > threshold
    }


def save_state_v1(state, filename="metrics_state.json"):
    with open(filename, "w") as f:
        json.dump(state, f, indent=2)


def load_state_v1(filename="metrics_state.json"):
    with open(filename) as f:
        return json.load(f)


if __name__ == "__main__":

    april_may = {
        "Bengaluru": -15.02,
        "Guntur": 122.19,
        "Hyderabad": 16.29,
        "Karimnagar": 23.63,
        "Nellore": 6.50,
        "Tirupati": 66.87,
        "Vijayawada": 2.06,
        "Visakhapatnam": -62.46,
        "Warangal": -22.03
    }

    may_june = {
        "Bengaluru": -1.52,
        "Guntur": -28.11,
        "Hyderabad": 20.61,
        "Karimnagar": -44.00,
        "Nellore": 3.52,
        "Tirupati": -17.07,
        "Vijayawada": -12.02,
        "Visakhapatnam": 99.12,
        "Warangal": -14.84
    }

    flagged_april_may = flag_significant_regions_v1(april_may)
    flagged_may_june = flag_significant_regions_v1(may_june)

    print("April-May flagged:", sorted(flagged_april_may))
    print("May-June flagged:", sorted(flagged_may_june))

    unique_flagged = sorted(
        set(flagged_april_may) | set(flagged_may_june)
    )

    print("Unique flagged regions:", unique_flagged)
    print("Unique flagged count:", len(unique_flagged))
