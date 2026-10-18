#!/usr/bin/env python3
"""Fetch the economic data the homepage shows, and write it to _data/live.yml.

Runs on GitHub Actions every weekday morning. Uses only the Python standard
library, so there is nothing to install and nothing to break.

Sources, both free and neither needing an API key:
  - Frankfurter (European Central Bank reference rates) for exchange rates
  - The World Bank for India's annual indicators

If a source is unreachable the script keeps whatever is already in
_data/live.yml rather than wiping the page. A site that shows slightly old
numbers is fine; a site that shows an error is not.
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_data", "live.yml")

TIMEOUT = 25
WINDOW_DAYS = 90      # how much history to fetch
SPARK_W, SPARK_H = 150, 34


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "beautifuleconomics.in/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8"))


def sparkline(values):
    """Turn a list of numbers into an SVG path, scaled to fit the box."""
    if len(values) < 2:
        return ""
    lo, hi = min(values), max(values)
    span = (hi - lo) or 1.0
    step = SPARK_W / (len(values) - 1)
    pts = []
    for i, v in enumerate(values):
        x = i * step
        # invert y: SVG grows downward, and leave 3px padding top and bottom
        y = SPARK_H - 3 - ((v - lo) / span) * (SPARK_H - 6)
        pts.append(f"{x:.1f},{y:.1f}")
    return "M" + " L".join(pts)


def fetch_rates():
    """Rupees per unit of each currency, with history."""
    end = date.today()
    start = end - timedelta(days=WINDOW_DAYS)
    url = (f"https://api.frankfurter.dev/v1/{start.isoformat()}..{end.isoformat()}"
           f"?base=USD&symbols=INR,EUR,GBP,JPY")
    data = get_json(url)
    rates = data.get("rates") or {}
    if not rates:
        raise ValueError("no rates returned")

    days = sorted(rates.keys())

    # Frankfurter quotes everything per 1 USD. Rupees per euro is therefore
    # INR-per-USD divided by EUR-per-USD, and so on for each currency.
    series = {"USD": [], "EUR": [], "GBP": [], "JPY": []}
    kept_days = []
    for d in days:
        row = rates[d]
        inr = row.get("INR")
        if not inr:
            continue
        kept_days.append(d)
        series["USD"].append(inr)
        for code in ("EUR", "GBP"):
            per_usd = row.get(code)
            series[code].append(inr / per_usd if per_usd else None)
        jpy = row.get("JPY")
        # Per 100 yen reads better than per 1 yen.
        series["JPY"].append((inr / jpy) * 100 if jpy else None)

    out = []
    labels = {
        "USD": ("US dollar", "$1"),
        "EUR": ("Euro", "&euro;1"),
        "GBP": ("Pound sterling", "&pound;1"),
        "JPY": ("Japanese yen", "&yen;100"),
    }
    for code in ("USD", "EUR", "GBP", "JPY"):
        vals = [v for v in series[code] if v is not None]
        if len(vals) < 2:
            continue
        latest = vals[-1]
        month_ago = vals[-22] if len(vals) >= 22 else vals[0]
        change = ((latest - month_ago) / month_ago) * 100 if month_ago else 0.0
        name, unit = labels[code]
        out.append({
            "code": code,
            "name": name,
            "unit": unit,
            "value": round(latest, 2),
            "change": round(change, 2),
            "low": round(min(vals), 2),
            "high": round(max(vals), 2),
            "path": sparkline(vals),
        })
    return {"as_of": kept_days[-1], "points": len(kept_days), "rates": out}


def fetch_indicator(code, label, unit, note):
    url = (f"https://api.worldbank.org/v2/country/IND/indicator/{code}"
           f"?format=json&per_page=4&mrnev=1")
    data = get_json(url)
    if not isinstance(data, list) or len(data) < 2 or not data[1]:
        raise ValueError("unexpected World Bank shape for " + code)
    row = data[1][0]
    if row.get("value") is None:
        raise ValueError("null value for " + code)
    return {
        "label": label,
        "value": round(float(row["value"]), 2),
        "unit": unit,
        "year": row.get("date"),
        "note": note,
    }


def read_existing():
    """Keep the previous file as a fallback if a source is down."""
    if not os.path.exists(OUT):
        return None
    try:
        import re
        text = open(OUT, encoding="utf-8").read()
        m = re.search(r"^# json:(.*)$", text, re.M)
        return json.loads(m.group(1)) if m else None
    except Exception:
        return None


def yaml_escape(s):
    return str(s).replace("\\", "\\\\").replace('"', '\\"')


def write(payload):
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    lines = [
        "# Written automatically by scripts/fetch_live_data.py.",
        "# Do not edit by hand — the next scheduled run overwrites it.",
        "# json:" + json.dumps(payload, separators=(",", ":")),
        "",
        f'as_of: "{yaml_escape(payload["as_of"])}"',
        f'generated: "{yaml_escape(payload["generated"])}"',
        f'headline: "{yaml_escape(payload["headline"])}"',
        "rates:",
    ]
    for r in payload["rates"]:
        lines += [
            f'  - code: "{r["code"]}"',
            f'    name: "{yaml_escape(r["name"])}"',
            f'    unit: "{yaml_escape(r["unit"])}"',
            f'    value: {r["value"]}',
            f'    change: {r["change"]}',
            f'    low: {r["low"]}',
            f'    high: {r["high"]}',
            f'    path: "{r["path"]}"',
        ]
    lines.append("indicators:")
    for i in payload["indicators"]:
        lines += [
            f'  - label: "{yaml_escape(i["label"])}"',
            f'    value: {i["value"]}',
            f'    unit: "{yaml_escape(i["unit"])}"',
            f'    year: "{yaml_escape(i["year"])}"',
            f'    note: "{yaml_escape(i["note"])}"',
        ]
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def headline_for(usd):
    """One plain sentence about the month, written from the numbers."""
    if not usd:
        return "Exchange rates update each weekday morning."
    ch = usd["change"]
    size = abs(ch)
    if size < 0.25:
        return (f"The rupee has barely moved against the dollar this month — "
                f"{usd['value']} to the dollar, within a quarter of a percent of where it was.")
    direction = "weaker" if ch > 0 else "stronger"
    strength = "a little" if size < 1 else ("noticeably" if size < 3 else "sharply")
    return (f"The rupee is {strength} {direction} against the dollar than a month ago, "
            f"at {usd['value']} to the dollar — a move of {size:.1f}%.")


def main():
    previous = read_existing()
    problems = []

    try:
        fx = fetch_rates()
    except Exception as e:
        problems.append(f"exchange rates: {e}")
        fx = None

    indicators = []
    wanted = [
        ("FP.CPI.TOTL.ZG", "Consumer price inflation", "%", "Annual average, India"),
        ("NY.GDP.MKTP.KD.ZG", "GDP growth", "%", "Annual, constant prices"),
        ("SL.UEM.TOTL.ZS", "Unemployment", "%", "Modelled ILO estimate"),
    ]
    for code, label, unit, note in wanted:
        try:
            indicators.append(fetch_indicator(code, label, unit, note))
        except Exception as e:
            problems.append(f"{label}: {e}")

    if fx is None and not indicators:
        print("ERROR: every source failed:", "; ".join(problems), file=sys.stderr)
        if previous:
            print("Keeping the existing _data/live.yml untouched.", file=sys.stderr)
            return 0          # don't fail the build; yesterday's numbers still show
        return 1

    if fx is None and previous:
        fx = {"as_of": previous.get("as_of", ""), "rates": previous.get("rates", [])}
        problems.append("reused previous exchange rates")

    if not indicators and previous:
        indicators = previous.get("indicators", [])

    usd = next((r for r in (fx or {}).get("rates", []) if r["code"] == "USD"), None)
    payload = {
        "as_of": (fx or {}).get("as_of", ""),
        "generated": date.today().isoformat(),
        "headline": headline_for(usd),
        "rates": (fx or {}).get("rates", []),
        "indicators": indicators,
    }
    write(payload)

    print(f"Wrote {OUT}")
    print(f"  as of {payload['as_of']}, {len(payload['rates'])} rates, "
          f"{len(payload['indicators'])} indicators")
    print(f"  {payload['headline']}")
    if problems:
        print("  notes: " + "; ".join(problems))
    return 0


if __name__ == "__main__":
    sys.exit(main())
