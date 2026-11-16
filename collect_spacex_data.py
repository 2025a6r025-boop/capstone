import requests
import pandas as pd
from pathlib import Path

URL = "https://api.spacexdata.com/v4/launches"

def main():
    records = requests.get(URL, timeout=45)
    records.raise_for_status()
    rows = []
    for x in records.json():
        core = (x.get("cores") or [{}])[0]
        rows.append({
            "flight_number": x.get("flight_number"),
            "name": x.get("name"),
            "date_utc": x.get("date_utc"),
            "year": str(x.get("date_utc", ""))[:4],
            "launchpad": x.get("launchpad"),
            "rocket": x.get("rocket"),
            "success": x.get("success"),
            "landing_attempt": core.get("landing_attempt"),
            "landing_success": core.get("landing_success"),
            "landing_type": core.get("landing_type"),
            "reused": core.get("reused"),
            "payload_ids": x.get("payloads") or []
        })
    out = Path(__file__).resolve().parents[1] / "data/raw/spacex_launches.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print("Saved", len(rows), "launches to", out)

if __name__ == "__main__":
    main()
