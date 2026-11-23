"""Roof cost calculator + roof repair cost guide (added 2026-11-23).
Every dollar figure here is quoted from a named source (NerdWallet citing Angi; Angi's own repair survey).
The calculator only does arithmetic on those published ranges; the method is shown on the page."""

NW = '<a href="https://www.nerdwallet.com/home-ownership/home-improvement/learn/roof-replacement-cost" rel="nofollow noopener">NerdWallet</a>'
ANGI = '<a href="https://www.angi.com/articles/how-much-do-roof-repairs-cost.htm" rel="nofollow noopener">Angi</a>'

# ------------------------------------------------------------------ calculator
CALC_PATH = "/roof-cost-calculator/"
CALC_TITLE = "Roof Replacement Cost Calculator (Free, 2026) | Bedrock Roof"
CALC_H1 = "Roof replacement cost calculator"
CALC_DESC = "Free roof cost calculator: enter your home's size, roof pitch and material to see a ballpark price range for a new roof, based on published U.S. cost data."
CALC_BLURB = "Ballpark a new roof by size, pitch and material."

CALC_WIDGET = """<div class="card calc" id="calc" data-calc>
<h2>Estimate your new roof</h2><p class="lead">Takes 20 seconds. Nothing is sent until you ask for a quote.</p>
<div class="row"><div><label for="ksz">Home size (sq ft of living space)</label><input id="ksz" name="ksz" inputmode="numeric" maxlength="6" placeholder="2000" value="2000"></div>
<div><label for="kst">Stories</label><select id="kst"><option value="1" selected>1</option><option value="2">2</option><option value="3">3</option></select></div></div>
<label for="kpi">Roof pitch</label><select id="kpi">
<option value="1.054">Low (walkable, about 4/12)</option><option value="1.118" selected>Medium (typical, about 6/12)</option>
<option value="1.25" data-steep="1">Steep (hard to walk, about 9/12)</option><option value="1.414" data-steep="1">Very steep (12/12 or more)</option></select>
<label for="kmt">Roofing material</label><select id="kmt">
<option value="0,0" selected>Asphalt shingles</option><option value="4,10.8">Synthetic (composite) shingles</option>
<option value="5,13.8">Wood shingles or shakes</option><option value="5,14.8">Metal shingles or panels</option>
<option value="9,18.8">Clay or concrete tile</option><option value="9,28.8">Slate</option></select>
<label for="kar">Know your roof area? <span class="opt">(optional, in sq ft; overrides the size above)</span></label><input id="kar" inputmode="numeric" maxlength="6" placeholder="e.g. 2400">
<button class="btn full" type="button" data-calc-go>Show my estimate</button>
<div class="calc-out" aria-live="polite" hidden>
<p class="calc-range"><span data-lo></span> to <span data-hi></span></p>
<p class="calc-sub">Estimated roof area: <b data-area></b> sq ft (about <b data-sq></b> roofing squares)<span data-steepnote hidden>, including $1,000 to $3,000 for a steep roof</span>.</p>
<p class="calc-sub">This is a national ballpark, not a quote. Local labor, tear-off, decking repairs and permits can move it a lot.</p>
<a class="btn full" href="#quote" data-calc-cta>Get a real price from a local roofer (free)</a></div></div>"""

CALC_BODY = f"""<div class="callout quick"><b>Quick answer:</b> A new roof in the U.S. costs about <b>$9,500</b> on average, and most jobs fall between about <b>$5,800 and $46,000</b>, or roughly <b>$4 to $11 per square foot</b> of roof with typical materials. Use the calculator below to scale that to your home. <span class="src">Source: Angi data, as reported by {NW}.</span></div>
WIDGET
<h2>How the calculator works</h2>
<ol><li><b>Roof area.</b> We divide your living space by the number of stories to get the footprint, add 10% for overhangs, then multiply by a standard pitch factor (1.05 for a low 4/12 roof up to 1.41 for a 12/12 roof). If you enter your roof area, we use that instead.</li>
<li><b>Base price.</b> Roof area times <b>$4 to $11 per square foot</b>, the national installed range for a typical asphalt roof reported by NerdWallet from Angi data.</li>
<li><b>Material.</b> For other materials we add the difference between that material's cost per square foot and asphalt's ($1 to $1.20), using the same source: synthetic $5&ndash;$12, wood $6&ndash;$15, metal $6&ndash;$16, clay or concrete tile $10&ndash;$20, slate $10&ndash;$30 per square foot.</li>
<li><b>Steep roofs.</b> A steeply sloped roof can add about <b>$1,000 to $3,000</b>, per the same source.</li></ol>
<p>Results are rounded to the nearest $100. They don't include extended warranties (about $500 to $5,000), permit fees (often up to $500) or rotted decking, which a roofer can only price after an inspection.</p>
<h2>Typical cost by house size</h2>
<table><thead><tr><th>Roof area</th><th>Typical installed price</th></tr></thead><tbody>
<tr><td>1,000 sq ft</td><td>$4,000 to $11,000</td></tr><tr><td>1,500 sq ft</td><td>$6,000 to $16,500</td></tr>
<tr><td>2,000 sq ft</td><td>$8,000 to $22,000</td></tr><tr><td>2,500 sq ft</td><td>$10,000 to $27,500</td></tr>
<tr><td>3,000 sq ft</td><td>$12,000 to $33,000</td></tr></tbody></table>
<p class="src">Source: {NW}, typical materials.</p>
<h2>Why your real quote may differ</h2>
<ul><li><b>Local labor.</b> Labor is often more than half the bill and runs higher in expensive metros and right after big storms.</li>
<li><b>Tear-off.</b> Removing one or more old layers adds labor and disposal.</li>
<li><b>Decking.</b> Soft or rotted boards are replaced per sheet once the old roof is off. Ask for that price in writing.</li>
<li><b>Roof shape.</b> Valleys, dormers, chimneys and skylights add flashing work.</li>
<li><b>Insurance.</b> If hail or wind damaged the roof, your policy may cover part of it. See <a href="/insurance-roof-replacement/">does insurance cover roof replacement?</a></li></ul>
<h2>Commercial or flat roof?</h2><p>Commercial roofs are priced differently (membrane type, insulation, drains and rooftop units). See <a href="/commercial-roof-replacement-cost/">what drives commercial roof replacement cost</a> or ask for a free commercial inspection below.</p>"""

CALC_FAQ = [
 ("How accurate is a roof cost calculator?", "It gives a ballpark range based on national data. Your actual price depends on local labor, your roof's shape, how many layers need to come off and whether the decking needs repair. Only a written quote after an inspection is exact."),
 ("How do I measure my roof area?", "Roofers measure it for you during an inspection, often from satellite imagery. As a rough guide, roof area is your home's footprint plus overhangs, multiplied by a factor for the pitch: about 1.05 for a low roof and up to about 1.41 for a very steep one."),
 ("What is a roofing square?", "A square is 100 square feet of roof. A 2,000 sq ft roof is 20 squares. Quotes and material orders are usually priced by the square."),
 ("Why is my quote higher than the calculator?", "Common reasons are higher local labor rates, a steep or complex roof, extra layers to tear off, decking repairs, upgraded underlayment or an extended warranty. Ask the roofer to itemize the quote, or get a free second opinion."),
 ("Does homeowners insurance pay for a new roof?", "It may, if the roof was damaged by a covered event like hail or wind. Wear and tear from age usually isn't covered, and the final decision is your insurer's."),
]

# ------------------------------------------------------------------ repair cost guide (G2-style tuple)
G3 = [
("/roof-repair-cost/", "Roof Repair Cost: 2026 Prices by Repair Type | Bedrock Roof", "How much does roof repair cost?",
 "Typical U.S. roof repair costs by repair type and roof material, from small leaks and flashing to hail damage, plus when repair stops making sense.",
 "Typical national prices for common roof repairs, and how to tell a fair repair quote from a push to replace.",
 f"""<div class="callout quick"><b>Quick answer:</b> Most roof repairs in the U.S. cost between about <b>$393 and $1,934</b>, with an average of about <b>$1,155</b>. Small fixes like a vent boot or a patched hole can be a few hundred dollars, while hail damage or sagging can run into the thousands. A full replacement typically costs about $5,900 to $12,900 by comparison. <span class="src">Source: {ANGI} survey of more than 30,000 customers (2025 data).</span></div>
<h2>Cost by repair type</h2>
<table><thead><tr><th>Repair</th><th>Typical cost</th></tr></thead><tbody>
<tr><td>Vent repair</td><td>$75 to $250</td></tr><tr><td>Hole patching</td><td>$100 to $1,000</td></tr>
<tr><td>Flashing</td><td>$200 to $500</td></tr><tr><td>Ridge cap repair</td><td>$200 to $750</td></tr>
<tr><td>Skylight leak</td><td>$300 to $800</td></tr><tr><td>Roof leak</td><td>$360 to $1,550</td></tr>
<tr><td>Ice dam removal</td><td>$500 to $700</td></tr><tr><td>Roof truss</td><td>$500 to $5,000</td></tr>
<tr><td>Soffit and fascia</td><td>$600 to $6,000</td></tr><tr><td>Hail damage</td><td>$700 to $4,000</td></tr>
<tr><td>Sagging roof</td><td>$1,500 to $1,700</td></tr><tr><td>Eave repair</td><td>$1,500 to $1,700</td></tr></tbody></table>
<p class="src">Source: {ANGI}.</p>
<h2>Cost by size of the damaged area</h2>
<table><thead><tr><th>Area repaired</th><th>Typical cost</th></tr></thead><tbody>
<tr><td>100 sq ft</td><td>$350 to $1,200</td></tr><tr><td>200 sq ft</td><td>$700 to $2,400</td></tr>
<tr><td>500 sq ft</td><td>$1,750 to $6,000</td></tr><tr><td>1,000 sq ft</td><td>$3,500 to $12,000</td></tr></tbody></table>
<h2>Average repair cost by roof material</h2>
<table><thead><tr><th>Roof type</th><th>Average repair</th></tr></thead><tbody>
<tr><td>Flat, foam or single-ply</td><td>$400</td></tr><tr><td>Composite</td><td>$450</td></tr><tr><td>Wood shake</td><td>$750</td></tr>
<tr><td>Asphalt shingles</td><td>$975</td></tr><tr><td>Tile</td><td>$1,000</td></tr><tr><td>Metal</td><td>$1,700</td></tr><tr><td>Slate</td><td>$1,800</td></tr></tbody></table>
<p class="src">Source: {ANGI}.</p>
<h2>Other costs to expect</h2><ul><li><b>Inspection:</b> about $75 to $600 when it isn't free.</li><li><b>Emergency or after-hours call:</b> often an extra $100 to $300 or more.</li><li><b>Labor:</b> roughly $45 to $75 per hour.</li></ul>
<h2>Repair or replace?</h2><p>Repair usually makes sense when the damage is limited to one area and the roof has years of life left. Replacement starts to make sense when repairs are adding up, damage is spread across the roof, or the roof is near the end of its life. If one repair would cost a large share of a new roof, get a replacement quote too. See <a href="/roof-repair-or-replace/">repair or replace</a> and use our <a href="/roof-cost-calculator/">roof cost calculator</a> to compare.</p>
<h2>How to get a fair repair price</h2><ol><li>Ask for photos of the damage and a written scope before work starts.</li><li>Ask whether the price includes matching shingles and flashing, not just sealant.</li><li>If the damage came from a storm, ask the roofer to document it before you call your insurer. See <a href="/roof-insurance-claim/">filing a roof claim</a>.</li><li>Be careful with anyone who finds damage you can't see in the photos. See <a href="/roofing-scams/">roofing scams</a>.</li></ol>""",
 "Roof repair cost", "crew3",
 [("How much does it cost to fix a roof leak?", "Angi reports most roof leak repairs cost about $360 to $1,550, depending on the cause, how easy it is to reach and how much water damage there is underneath."),
  ("Is it worth repairing an old roof?", "If the damage is small and the rest of the roof is sound, a repair can buy years. If the roof is near the end of its expected life or problems keep coming back, putting the money toward a replacement is often better value."),
  ("Does insurance pay for roof repairs?", "It may if the damage came from a sudden covered event like hail, wind or a fallen tree, minus your deductible. Wear and tear and slow leaks from age usually aren't covered."),
  ("Can I get a free roof repair estimate?", "Many roofers inspect and quote repairs for free. You can request a free inspection from a local roofer on this page.")],
 "Prices by repair type, roof material and damage size.",
 ["/roof-cost-calculator/", "/roof-repair-or-replace/", "/roof-leak/", "/roof-replacement-cost/"]),
]
