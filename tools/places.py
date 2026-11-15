"""Cities and states for location pages. Start small; add cities only with real regional content.
Climate profiles are general regional roofing considerations, not claims about specific roofers."""

CLIMATES = {
 "hurricane": {
  "label": "hurricane and high-wind coast",
  "risks": ["hurricane and tropical-storm winds that lift and tear shingles", "wind-driven rain that gets under flashing", "heat and humidity that age shingles and underlayment faster"],
  "materials": "Many homeowners here choose high-wind-rated architectural shingles, concrete or clay tile, or standing-seam metal. Ask roofers about wind ratings, secondary water barriers and how the roof deck is fastened.",
  "tip": "After a named storm, report damage to your insurer quickly and be careful with out-of-town crews going door to door. Some insurers here ask about a roof's age before renewing a policy, so keep your installation paperwork.",
  "photo": "home2"},
 "hail": {
  "label": "hail and severe-storm belt",
  "risks": ["hail that bruises and cracks shingles, sometimes without an obvious leak", "spring and summer thunderstorms with strong straight-line winds", "big temperature swings that stress roofing materials"],
  "materials": "Impact-resistant (often called Class 4) shingles and metal roofing are popular here. Some insurers offer premium discounts for impact-rated roofs, so ask your agent.",
  "tip": "Hail damage isn't always visible from the ground. If a storm hit your neighborhood, a roofer's inspection with photos can show what's there before you call your insurer.",
  "photo": "roofsky"},
 "snow": {
  "label": "snow and freeze-thaw country",
  "risks": ["ice dams that push water under shingles at the eaves", "heavy snow loads on older or low-slope roofs", "freeze-thaw cycles that crack flashing and sealants"],
  "materials": "Asphalt shingles with an ice-and-water barrier along the eaves are the norm, and metal roofs shed snow well. Good attic insulation and ventilation matter as much as the shingles.",
  "tip": "Many roofers here book up in late summer and fall, so get quotes early if you want the work done before winter.",
  "photo": "home4"},
 "desert": {
  "label": "desert heat and sun",
  "risks": ["intense UV and heat that dry out and crack shingles and underlayment", "monsoon storms with sudden wind and heavy rain", "flat and low-slope roofs that need regular coating"],
  "materials": "Concrete and clay tile, reflective 'cool roof' coatings, foam roofs on flat sections and light-colored shingles are common choices. On tile roofs, the underlayment beneath often wears out before the tiles do.",
  "tip": "Ask whether a tile roof needs a full replacement or an underlayment 'lift and relay', which reuses good tiles.",
  "photo": "home3"},
 "wildfire": {
  "label": "dry, fire-prone West",
  "risks": ["wildfire embers that can ignite roofs and gutters", "long dry seasons followed by heavy winter rain", "sun and heat that age roofing materials"],
  "materials": "Class A fire-rated roofing such as tile, metal or rated asphalt shingles is common, and some areas require it. Ember-resistant vents and clean gutters help too.",
  "tip": "Ask roofers about local fire-rating requirements and whether your area needs a permit for a reroof (most do).",
  "photo": "home5"},
 "rain": {
  "label": "rainy Pacific Northwest",
  "risks": ["long wet seasons that find every weak spot in flashing", "moss and algae that lift shingles and hold moisture", "windstorms that drop branches on roofs"],
  "materials": "Architectural asphalt shingles and metal are common. Moss-resistant shingles, good ventilation and well-sealed flashing around chimneys and skylights matter here.",
  "tip": "Dry summer months are the busiest season for roofers, so book inspections early.",
  "photo": "home1"},
 "humid": {
  "label": "hot, humid Southeast",
  "risks": ["summer thunderstorms and the occasional tropical system", "humidity that feeds algae streaks and attic moisture", "heat that shortens the life of shingles"],
  "materials": "Algae-resistant architectural shingles are the most common choice, with metal roofs growing in popularity. Proper attic ventilation helps shingles last longer in the heat.",
  "tip": "Black streaks are usually algae, not damage, but curling, missing or granule-shedding shingles are worth an inspection.",
  "photo": "home1"},
}

STATES = {
 "FL": ("Florida", "hurricane"), "TX": ("Texas", "hail"), "GA": ("Georgia", "humid"), "NC": ("North Carolina", "humid"),
 "AZ": ("Arizona", "desert"), "CO": ("Colorado", "hail"), "OK": ("Oklahoma", "hail"), "TN": ("Tennessee", "humid"),
 "IL": ("Illinois", "snow"), "OH": ("Ohio", "snow"), "MI": ("Michigan", "snow"), "PA": ("Pennsylvania", "snow"),
 "NY": ("New York", "snow"), "CA": ("California", "wildfire"), "WA": ("Washington", "rain"), "NV": ("Nevada", "desert"),
 "SC": ("South Carolina", "humid"), "LA": ("Louisiana", "hurricane"), "MN": ("Minnesota", "snow"), "MO": ("Missouri", "hail"),
}

# (city, state, climate override or None)
CITIES = [
 ("Miami", "FL", None), ("Tampa", "FL", None), ("Orlando", "FL", None), ("Jacksonville", "FL", None), ("Fort Lauderdale", "FL", None),
 ("Houston", "TX", "hurricane"), ("Dallas", "TX", None), ("San Antonio", "TX", None), ("Austin", "TX", None), ("Fort Worth", "TX", None),
 ("Atlanta", "GA", None), ("Charlotte", "NC", None), ("Raleigh", "NC", None), ("Phoenix", "AZ", None), ("Tucson", "AZ", None),
 ("Denver", "CO", None), ("Colorado Springs", "CO", None), ("Oklahoma City", "OK", None), ("Tulsa", "OK", None), ("Nashville", "TN", None),
 ("Chicago", "IL", None), ("Columbus", "OH", None), ("Cleveland", "OH", None), ("Detroit", "MI", None), ("Philadelphia", "PA", None),
 ("Pittsburgh", "PA", None), ("Buffalo", "NY", None), ("Los Angeles", "CA", None), ("San Diego", "CA", None), ("Sacramento", "CA", None),
 ("Seattle", "WA", None), ("Las Vegas", "NV", None), ("Charleston", "SC", "hurricane"), ("New Orleans", "LA", None), ("Minneapolis", "MN", None),
 ("Kansas City", "MO", None), ("St. Louis", "MO", None),
]

def slug(s):
    import re
    return re.sub(r"[^a-z0-9]+", "-", s.lower().replace(".", "")).strip("-")
