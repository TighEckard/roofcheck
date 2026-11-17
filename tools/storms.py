"""Daily storm check: NOAA Storm Prediction Center (SPC) preliminary hail and wind reports
-> storm events for cities that have a page on the site -> tools/storms.json.

Run:  python3 tools/storms.py            (checks yesterday, UTC)
      python3 tools/storms.py 2026-05-14 (checks a given convective day)
      python3 tools/storms.py --csv hail.csv wind.csv 2026-05-14  (offline test)
SPC reports are preliminary and unverified; pages say so and link the source.
"""
import csv, io, json, os, sys, datetime, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import citygen
from places import slug

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "storms.json")
SPC = "https://www.spc.noaa.gov/climo/reports/{d}_rpts_filtered_{k}.csv"
NEAR_KM = 20          # report must be within this distance of the city point
MIN_HAIL_IN = 1.0     # NWS severe hail threshold
MIN_WIND_MPH = 58     # NWS severe wind threshold

def fetch(day, kind):
    url = SPC.format(d=day.strftime("%y%m%d"), k=kind)
    req = urllib.request.Request(url, headers={"User-Agent": "bedrockroof-storm-check (static site build)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", "replace")

def parse(text, kind):
    out = []
    for row in csv.DictReader(io.StringIO(text)):
        try:
            lat, lon = float(row["Lat"]), float(row["Lon"])
        except (KeyError, TypeError, ValueError):
            continue
        rec = {"lat": lat, "lon": lon, "loc": (row.get("Location") or "").strip().title(), "county": (row.get("County") or "").strip().title(),
               "st": (row.get("State") or "").strip().upper(), "time": (row.get("Time") or "").strip()}
        if kind == "hail":
            try: rec["size"] = int(row["Size"]) / 100.0
            except (KeyError, ValueError): continue
            if rec["size"] < MIN_HAIL_IN: continue
        else:
            sp = (row.get("Speed") or "").strip()
            rec["mph"] = int(sp) if sp.isdigit() else None
            if rec["mph"] is not None and rec["mph"] < MIN_WIND_MPH: continue
        out.append(rec)
    return out

def events_for(day, hail, wind):
    cities = [r for r in citygen.load() if r["lat"]]
    ev = {}
    for kind, reps in (("hail", hail), ("wind", wind)):
        for p in reps:
            # each report counts for its single nearest city page, so one storm doesn't spawn look-alike pages for every suburb
            near = sorted((citygen.dist_km(c, p), i) for i, c in enumerate(cities) if c["st"] == p["st"])
            if not near or near[0][0] > NEAR_KM: continue
            c = cities[near[0][1]]
            if True:
                k = (c["n"], c["st"])
                e = ev.setdefault(k, {"date": day.isoformat(), "n": c["n"], "st": c["st"], "hail_max": 0, "hail_n": 0,
                                      "wind_max": 0, "wind_n": 0, "places": []})
                if kind == "hail":
                    e["hail_n"] += 1; e["hail_max"] = max(e["hail_max"], p["size"])
                else:
                    e["wind_n"] += 1; e["wind_max"] = max(e["wind_max"], p["mph"] or 0)
                place = f'{p["loc"]} ({p["county"]} County)' if p["county"] else p["loc"]
                if place and place not in e["places"] and len(e["places"]) < 6: e["places"].append(place)
    # only events worth a page: big hail, several hail reports, or very strong wind
    keep = [e for e in ev.values() if e["hail_max"] >= 1.25 or e["hail_n"] >= 3 or e["wind_max"] >= 70 or e["wind_n"] >= 4]
    return sorted(keep, key=lambda e: (-e["hail_max"], -e["wind_max"], e["n"]))

def event_slug(e):
    return f'{e["date"]}-{slug(e["n"])}-{e["st"].lower()}'

def load_events():
    return json.load(open(OUT)) if os.path.exists(OUT) else []

def save(new):
    old = load_events()
    have = {event_slug(e) for e in old}
    added = [e for e in new if event_slug(e) not in have]
    allev = sorted(old + added, key=lambda e: (e["date"], e["st"], e["n"]), reverse=True)
    json.dump(allev, open(OUT, "w"), indent=1)
    return added

def main(argv):
    if argv[:1] == ["--csv"]:
        hail_t, wind_t, day = open(argv[1]).read(), open(argv[2]).read(), datetime.date.fromisoformat(argv[3])
    else:
        day = datetime.date.fromisoformat(argv[0]) if argv else datetime.datetime.utcnow().date() - datetime.timedelta(days=1)
        hail_t, wind_t = fetch(day, "hail"), fetch(day, "wind")
    added = save(events_for(day, parse(hail_t, "hail"), parse(wind_t, "wind")))
    print(f"{day}: {len(added)} new storm events", *[event_slug(e) for e in added], sep="\n  ")

if __name__ == "__main__":
    main(sys.argv[1:])
