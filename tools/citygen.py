"""Builds per-city records from real data so each city page has its own facts.

Data: tools/cities.json, made from GeoNames (CC BY 4.0) via the all-the-cities package
(name, state, population, coordinates), plus the Koppen-Geiger climate class for the
coordinates (kgcpy, Beck et al.) and the distance to open ocean (global-land-mask).
Hand-written local notes in local.py take priority over generated text.
"""
import json, math, os
from places import CITIES as HAND, STATES, slug
from local import CITY_LOCAL

HERE = os.path.dirname(os.path.abspath(__file__))
MIN_POP = int(os.environ.get("MIN_POP", "100000"))

KOPPEN = {
 "Af": "tropical rainforest climate, hot and wet all year",
 "Am": "tropical monsoon climate, hot all year with a long rainy season",
 "Aw": "tropical savanna climate, hot all year with a distinct wet and dry season",
 "BWh": "hot desert climate, with very hot summers and little rain",
 "BWk": "cold desert climate, dry with cold winters",
 "BSh": "hot semi-arid climate, with hot summers and limited rain",
 "BSk": "semi-arid climate, with dry air, strong sun and limited rain",
 "Csa": "dry-summer (Mediterranean-type) climate, with hot, dry summers and most of its rain in the cooler months",
 "Csb": "dry-summer climate, with warm, dry summers and cool, wet winters",
 "Cfa": "humid subtropical climate, with hot, humid summers and cooler winters",
 "Cfb": "oceanic climate, mild and damp for much of the year",
 "Dfa": "hot-summer humid continental climate, with hot summers and cold, snowy winters",
 "Dfb": "warm-summer humid continental climate, with warm summers and long, cold, snowy winters",
 "Dfc": "subarctic climate, with short summers and long, very cold winters",
 "Dsa": "dry-summer continental climate, with hot, dry summers and cold winters",
 "Dsb": "dry-summer continental climate, with warm, dry summers and cold, snowy winters",
 "Dwa": "continental climate with hot summers and cold, dry winters",
 "Dwb": "continental climate with warm summers and cold, dry winters",
 "As": "tropical savanna climate, warm all year with a drier summer",
 "Dsc": "subarctic climate, with cool summers and long, cold winters",
 "Dwc": "subarctic climate, with cool summers and long, cold winters",
 "Cwa": "humid subtropical climate, with hot, wet summers and mild, dry winters",
 "Cfc": "subpolar oceanic climate, cool and damp much of the year",
 "ET": "tundra climate, cold most of the year",
}
OCEAN = {"Gulf": "Gulf of Mexico", "Atlantic": "Atlantic Ocean", "Pacific": "Pacific Ocean"}
HURRICANE_ST = {"TX", "LA", "MS", "AL", "FL", "GA", "SC", "NC", "VA"}
HAIL_ST = {"TX", "OK", "KS", "NE", "CO", "SD", "ND", "MN", "IA", "MO", "WY"}
WEST_ST = {"CA", "OR", "WA", "NV", "AZ", "NM", "CO", "UT", "ID", "MT"}

RISK_TEXT = {
 "hurricane": "Hurricane and tropical-storm winds that lift shingles and drive rain under flashing",
 "noreaster": "Nor'easters and the occasional tropical storm bringing wind-driven rain",
 "salt": "Salt air near the water that corrodes metal flashing, fasteners and vents",
 "hail": "Hailstorms that bruise and crack shingles, sometimes without an obvious leak",
 "snow": "Snow loads and ice dams that push meltwater under shingles at the eaves",
 "heat": "Intense sun and heat that dry out and crack shingles and underlayment",
 "wildfire": "Wildfire embers in dry seasons that can ignite roofs and gutters",
 "rain": "Long wet seasons, moss and algae that hold moisture against the roof",
 "humid": "Summer thunderstorms and humidity that speed up shingle aging and algae streaks",
}
MATERIAL_TEXT = {
 "hurricane": "high-wind-rated shingles, tile or standing-seam metal with a sealed roof deck",
 "noreaster": "well-sealed flashing and wind-rated architectural shingles",
 "salt": "corrosion-resistant flashing and fasteners",
 "hail": "impact-resistant (often Class 4) shingles or metal, which some insurers discount",
 "snow": "an ice-and-water barrier along the eaves plus good attic insulation and ventilation",
 "heat": "tile, light-colored or reflective 'cool roof' materials, and coatings on flat sections",
 "wildfire": "Class A fire-rated roofing and ember-resistant vents",
 "rain": "moss-resistant shingles or metal, with careful flashing around chimneys and skylights",
 "humid": "algae-resistant architectural shingles and good attic ventilation",
}
PRIMARY = ["hurricane", "hail", "snow", "heat", "wildfire", "rain", "humid", "noreaster"]
CLIMATE_KEY = {"hurricane": "hurricane", "hail": "hail", "snow": "snow", "heat": "desert", "wildfire": "wildfire",
               "rain": "rain", "humid": "humid", "noreaster": "snow"}

# GeoNames entries that are neighborhoods, duplicates or data errors rather than cities
EXCLUDE = {("Ironville", "KY"), ("Meads", "KY"), ("Lexington-Fayette", "KY"), ("Maryvale", "AZ"), ("Deer Valley", "AZ"),
 ("Tempe Junction", "AZ"), ("Alhambra", "AZ"), ("East Chattanooga", "TN"), ("East Hampton", "VA"), ("Metairie Terrace", "LA"),
 ("North Stamford", "CT"), ("North Peoria", "IL"), ("East Independence", "MO"), ("Valencia", "CA"), ("Jamaica", "NY"),
 ("East Flatbush", "NY"), ("Washington Heights", "NY"), ("Astoria", "NY"), ("Borough Park", "NY"), ("Sheepshead Bay", "NY"),
 ("East Harlem", "NY"), ("Elmhurst", "NY"), ("Bushwick", "NY"), ("Gravesend", "NY"), ("Corona", "NY"), ("Flushing", "NY"),
 ("Bensonhurst", "NY"), ("Bedford-Stuyvesant", "NY"), ("Canarsie", "NY"), ("Harlem", "NY"), ("Kings Bridge", "NY")}
BOROUGHS = {"Brooklyn", "Queens", "Manhattan", "The Bronx", "Staten Island"}

def km_mi(km): return round(km * 0.621371)

def dist_km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a["lat"], a["lon"], b["lat"], b["lon"]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371 * math.asin(math.sqrt(h))

def flags_for(c):
    kg, st, ck, oc = c["kg"] or "", c["st"], c["coast_km"], c.get("ocean")
    if kg == "Ocean": kg = "Af" if st == "HI" else ""
    f = []
    if st in HURRICANE_ST and oc in ("Gulf", "Atlantic") and ck is not None and ck <= 160: f.append("hurricane")
    if st not in HURRICANE_ST and oc == "Atlantic" and ck is not None and ck <= 60 and c["lat"] >= 37: f.append("noreaster")
    if ck is not None and ck <= 12: f.append("salt")
    if st in HAIL_ST: f.append("hail")
    if (kg.startswith("Cs") and c["lat"] >= 40 and st in ("ID", "UT", "NV", "MT", "WY", "CO")): f.append("snow")
    elif kg.startswith("D") or (kg in ("BSk", "BWk", "Csb", "Cfb", "Dsb") and c["lat"] >= 39 and st not in ("CA", "OR", "WA")) : f.append("snow")
    if kg.startswith("BW") or kg == "BSh" or (kg == "BSk" and c["lat"] < 37): f.append("heat")
    if st in WEST_ST and (kg.startswith("Cs") or kg.startswith("B")): f.append("wildfire")
    if st in ("WA", "OR") and kg in ("Csb", "Cfb"): f.append("rain")
    if kg in ("Cfa", "Am", "Aw", "Af") and "hurricane" not in f: f.append("humid")
    if not f: f.append("humid" if kg.startswith("C") else "snow")
    return f

def fmt_pop(p):
    if p >= 1_000_000: return f"{p/1_000_000:.1f} million".replace(".0 ", " ")
    return f"{int(round(p, -3)):,}"

ORD = {1: "largest", 2: "second-largest", 3: "third-largest", 4: "fourth-largest", 5: "fifth-largest",
       6: "sixth-largest", 7: "seventh-largest", 8: "eighth-largest", 9: "ninth-largest", 10: "10th-largest"}

def load():
    data = [c for c in json.load(open(os.path.join(HERE, "cities.json"))) if (c["n"], c["st"]) not in EXCLUDE]
    data.sort(key=lambda c: -c["pop"])
    by_slug = {}
    for c in data:
        by_slug.setdefault((slug(c["n"]), c["st"]), c)
    hand_alias = {"St. Louis": "St. Louis", "St. Paul": "Saint Paul"}
    chosen = []
    seen = set()
    for name, st, override in HAND:
        rec = by_slug.get((slug(name), st)) or by_slug.get((slug(hand_alias.get(name, name)), st))
        if rec: seen.add((slug(rec["n"]), st))
        rec = dict(rec) if rec else {"n": name, "st": st, "pop": 0, "lat": 0, "lon": 0, "kg": "", "coast_km": None, "ocean": None}
        rec["n"] = name; rec["override"] = override
        seen.add((slug(name), st)); chosen.append(rec)
    for c in data:
        if c["pop"] < MIN_POP or c["st"] not in STATES: continue
        k = (slug(c["n"]), c["st"])
        if k in seen: continue
        seen.add(k); r = dict(c); r["override"] = None; chosen.append(r)
    # state ranks among all known places
    rank = {}
    for st in STATES:
        lst = [c for c in data if c["st"] == st and c["n"] not in BOROUGHS]
        for i, c in enumerate(lst): rank[(slug(c["n"]), st)] = i + 1
    big = [c for c in data if c["pop"] >= 500_000]
    pages = {(slug(r["n"]), r["st"]) for r in chosen}
    out = []
    for r in chosen:
        f = flags_for(r) if r["kg"] else []
        if r["override"]:
            ck = r["override"]
        else:
            pk = next((p for p in PRIMARY if p in f), None)
            ck = CLIMATE_KEY[pk] if pk else STATES[r["st"]][1]
        r["flags"] = f; r["clim"] = ck
        r["rank"] = rank.get((slug(r["n"]), r["st"]))
        # nearest big city (metro anchor) and nearby pages
        if r["lat"]:
            anchors = sorted(((dist_km(r, b), b) for b in big if slug(b["n"]) != slug(r["n"])), key=lambda x: x[0])
            r["metro"] = (anchors[0][1]["n"], km_mi(anchors[0][0])) if anchors and anchors[0][0] <= 60 and anchors[0][1]["pop"] > r["pop"] else None
            near = sorted(((dist_km(r, o), o) for o in chosen if o is not r and o["lat"]), key=lambda x: x[0])
            r["nearby"] = [(o["n"], o["st"], km_mi(dkm)) for dkm, o in near[:6] if dkm <= 120]
        else:
            r["metro"] = None; r["nearby"] = []
        r["local"] = CITY_LOCAL.get(r["n"]) or generated_local(r)
        out.append(r)
    return out

def generated_local(r):
    n, sname = r["n"], STATES[r["st"]][0]
    parts = []
    rk = r.get("rank")
    size = f"the {ORD[rk]} city in {sname}" if rk and rk <= 10 else f"one of {sname}'s larger cities"
    lead = f"{n} is {size}, with roughly {fmt_pop(r['pop'])} residents"
    if n in BOROUGHS and r["st"] == "NY": lead = f"{n} is one of New York City's five boroughs, with roughly {fmt_pop(r['pop'])} residents"
    if r["st"] == "DC": lead = f"Washington, D.C. is the nation's capital, with roughly {fmt_pop(r['pop'])} residents"
    if r.get("metro") and n not in BOROUGHS and r["st"] != "DC": lead += f", about {r['metro'][1]} miles from {r['metro'][0]}"
    parts.append(lead + ".")
    if r["kg"] in KOPPEN: parts.append(f"It has a {KOPPEN[r['kg']]}.")
    ck, oc = r["coast_km"], r.get("ocean")
    if ck is not None and ck <= 8 and oc: parts.append(f"It sits right by the {OCEAN[oc]}, so salt air and coastal storms are part of the picture for roofs here.")
    elif ck is not None and ck <= 80 and oc: parts.append(f"It's about {km_mi(ck)} miles from the {OCEAN[oc]}.")
    else: parts.append("It's well inland, so the main roof threats come from inland weather rather than the ocean.")
    return " ".join(parts)

def risks(r, fallback):
    return [RISK_TEXT[f] for f in r["flags"]] or fallback

def materials(r, fallback):
    m = [MATERIAL_TEXT[f] for f in r["flags"] if f in MATERIAL_TEXT]
    if not m: return fallback
    if len(m) == 1: return f"Around {r['n']}, roofers often recommend {m[0]}."
    return f"Around {r['n']}, roofers often recommend " + ", ".join(m[:-1]) + f", and {m[-1]}."
