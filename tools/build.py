#!/usr/bin/env python3
"""Builds the static Bedrock Roof site into the repo root.
Run: python3 tools/build.py   (set PREVIEW=0 to drop the noindex tag at launch)
"""
import json, os, html
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from places import CLIMATES, STATES, CITIES, slug
from local import STATE_LICENSE, CITY_LOCAL

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://bedrockroof.com"
BRAND = "Bedrock Roof"
EMAIL = "hello@bedrockroof.com"
PREVIEW = os.environ.get("PREVIEW", "1") == "1"
BASE = os.environ.get("BASE", "")  # "/roofcheck" for the github.io preview, "" on bedrockroof.com
PHONE = os.environ.get("PHONE", "")  # e.g. "+13055550123" once the Twilio number exists
UPDATED = "2026-11-15"

def img(id_, w, h=None, q=60):
    s = f"https://images.unsplash.com/photo-{id_}?fm=webp&fit=crop&q={q}&w={w}"
    return s + (f"&h={h}" if h else "")

def pic(id_, alt, w=900, ratio=0.75, cls="", lazy=True, sizes="(min-width:900px) 33vw, 100vw"):
    ws = [480, 720, w] if w > 720 else [480, w]
    srcset = ", ".join(f"{img(id_, x, int(x*ratio))} {x}w" for x in ws)
    return (f'<img class="{cls}" src="{img(id_, w, int(w*ratio))}" srcset="{srcset}" sizes="{sizes}" '
            f'width="{w}" height="{int(w*ratio)}" alt="{html.escape(alt)}"'
            + (' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"') + '>')

P = {  # Unsplash photos (Unsplash License: free for commercial use, no attribution required)
 "hero": "1755114203680-d39d95efa82c",
 "crew1": "1635424709961-f3a150459ad4", "crew2": "1635424824849-1b09bdcc55b1",
 "crew3": "1635424709845-3a85ad5e1f5e", "shingles": "1643225523483-e2c434191bba",
 "tearoff": "1633759593085-1eaeb724fc88", "metal": "1780445392484-5fb7d5610708",
 "home1": "1792454005492-cb3b09be9d02", "home2": "1789683037479-44602dbee028",
 "home3": "1761013320045-d29e4f10bcbc", "home4": "1773427657182-4776c4f5b363",
 "home5": "1584738766473-61c083514bf4", "roofsky": "1563993356056-b23a9cd265ad",
 "couple": "1758691031787-90867cb6fb2c", "kitchen": "1556909115-3f381036bcb3",
}

LOGO = ('<svg width="30" height="30" viewBox="0 0 32 32" aria-hidden="true"><rect width="32" height="32" rx="7" fill="#12294a"/>'
        '<path d="M5 17.5 16 8l11 9.5" fill="none" stroke="#e8a33d" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M9 16v8h14v-8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linejoin="round"/></svg>')

NAV = [("/how-it-works/", "How it works"), ("/guides/", "Guides"),
       ("/choosing-a-roofer/", "Choosing a roofer"), ("/roofers/", "Find a roofer"), ("/faq/", "FAQ")]

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "url": SITE + "/",
       "logo": SITE + "/assets/logo.svg", "email": EMAIL, **({"telephone": PHONE} if PHONE else {}),
       "description": "Bedrock Roof is a free referral service that connects U.S. homeowners with independent local roofing contractors for inspections and quotes. Bedrock Roof does not perform roofing work."}

def fmt_phone(p):
    d = p[-10:]
    return f"({d[:3]}) {d[3:6]}-{d[6:]}"

def phone_link(cls="tel"):
    return f'<a class="{cls}" href="tel:{PHONE}">Call {fmt_phone(PHONE)}</a>' if PHONE else ""

def page(path, title, desc, body, schema=None, crumbs=None, og_img=P["hero"]):
    url = SITE + path
    graph = [ORG, {"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": BRAND, "publisher": {"@id": SITE + "/#org"}}]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate([("Home", "/")] + crumbs)]})
    graph += schema or []
    nav = "".join(f'<a href="{u}"{" aria-current=page" if u == path else ""}>{n}</a>' for u, n in NAV)
    robots = '<meta name="robots" content="noindex,nofollow">' if PREVIEW else '<meta name="robots" content="index,follow,max-image-preview:large">'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
{robots}
<link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{img(og_img, 1200, 630)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
<link rel="preconnect" href="https://images.unsplash.com" crossorigin>
<link rel="stylesheet" href="/assets/site.css?v=1">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, separators=(",", ":"))}</script>
</head><body>
<header class="top"><div class="wrap bar"><a class="logo" href="/">{LOGO}<span>Bedrock<b>Roof</b></span></a>
<nav class="nav" aria-label="Main">{nav}</nav>{phone_link()}<a class="btn sm" href="/get-quotes/">Get a free quote</a></div></header>
<main>{body}</main>
<footer class="foot"><div class="wrap fgrid">
<div><a class="logo" href="/">{LOGO}<span>Bedrock<b>Roof</b></span></a>
<p>A free referral service that connects homeowners across the U.S. with independent local roofing contractors.</p>
<p class="disc"><b>Bedrock Roof is not a roofing contractor</b> and does not perform, guarantee or warranty any roofing work. Contractors are independent businesses and may pay us for introductions. Always check a contractor's license, insurance and references before you sign anything.</p></div>
<div><h4>Homeowners</h4><a href="/get-quotes/">Get a free quote</a><a href="/how-it-works/">How it works</a><a href="/roofers/">Find a roofer by state</a><a href="/faq/">FAQ</a></div>
<div><h4>Guides</h4><a href="/roof-replacement-cost/">Roof replacement cost</a><a href="/choosing-a-roofer/">How to choose a roofer</a><a href="/storm-damage/">After storm damage</a><a href="/hail-damage-roof/">Hail damage</a><a href="/roof-leak/">Roof leaks</a><a href="/insurance-roof-replacement/">Insurance and roofs</a><a href="/guides/">All guides</a></div>
<div><h4>Company</h4><a href="/about/">About us</a><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
</div><div class="wrap legal">&copy; 2026 {BRAND}. Photos from <a href="https://unsplash.com" rel="nofollow">Unsplash</a>, shown for illustration.</div></footer>
<script src="/assets/site.js?v=1" defer></script>
</body></html>
"""

FORM = """<form class="qform" novalidate data-form>
<h2>{h}</h2><p class="lead">Free and no obligation. A local roofer will call or text you to set up a time.</p>
<fieldset class="need"><legend>What do you need?</legend>
<label><input type="radio" name="need" value="replacement" checked><span>New roof</span></label>
<label><input type="radio" name="need" value="repair"><span>Repair or leak</span></label>
<label><input type="radio" name="need" value="storm"><span>Storm damage</span></label>
<label><input type="radio" name="need" value="inspection"><span>Inspection</span></label></fieldset>
<div class="row"><div><label for="{p}n">Full name</label><input id="{p}n" name="n" required maxlength="40" autocomplete="name" placeholder="Jane Smith"></div>
<div><label for="{p}a">ZIP code</label><input id="{p}a" name="a" required inputmode="numeric" maxlength="5" autocomplete="postal-code" placeholder="12345"></div></div>
<label for="{p}p">Mobile phone</label><input id="{p}p" name="p" required type="tel" inputmode="tel" maxlength="20" autocomplete="tel" placeholder="(555) 555-5555">
<label for="{p}m">Anything the roofer should know? <span class="opt">(optional)</span></label><input id="{p}m" name="m" maxlength="45" autocomplete="off" placeholder="e.g. leak in the kitchen, roof is 20 years old">
<p class="err" role="alert" hidden></p>
<button class="btn full" type="submit">Get my free quote</button>
<p class="fine">By tapping &ldquo;Get my free quote&rdquo; you agree that Bedrock Roof may share your request with an independent roofing contractor serving your ZIP code, and that Bedrock Roof and that contractor may call or text you at the number you entered about your roof, including by automated means. Consent is not a condition of any purchase. Msg &amp; data rates may apply. Reply STOP to opt out. See our <a href="/privacy/">privacy policy</a>.</p>
</form>
<div class="okbox" hidden><h2>Thanks, we got your request.</h2><p>A local roofer should reach out soon, usually by call or text. If we can't find a roofer serving your area, we'll let you know.</p><p><a href="/choosing-a-roofer/">While you wait: 7 questions to ask any roofer &rarr;</a></p></div>"""

def form(h="Get a free roof quote", p="q"):
    return '<div class="card" id="quote">' + FORM.format(h=h, p=p) + '</div>'

def cta(t="Ready for a quote?", s="Tell us about your roof and a local roofer will reach out. Free, no obligation."):
    return f'<section class="cta"><div class="wrap"><h2>{t}</h2><p>{s}</p><a class="btn lg" href="/get-quotes/">Get a free quote</a></div></section>'

def faq_block(items, h="Frequently asked questions"):
    out = "".join(f'<details><summary>{q}</summary><div>{a}</div></details>' for q, a in items)
    return f'<section class="faq wrap narrow"><h2>{h}</h2>{out}</section>'

def faq_schema(items):
    import re
    strip = lambda s: re.sub(r"<[^>]+>", "", s)
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": strip(q), "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in items]}

def article(path, title, h1, desc, intro, body, crumb, photo, faq=None):
    sch = [{"@type": "Article", "headline": h1, "description": desc, "datePublished": UPDATED, "dateModified": UPDATED,
            "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": SITE + path,
            "image": img(photo, 1200, 630)}]
    if faq: sch.append(faq_schema(faq))
    b = f"""<section class="phero"><div class="wrap narrow"><p class="kick">Homeowner guide</p><h1>{h1}</h1><p class="sub">{intro}</p><p class="meta">Updated November 15, 2026 &middot; By the {BRAND} team</p></div></section>
<div class="wrap narrow prose"><figure class="lead-img">{pic(photo, h1, 1200, 0.5, lazy=False, sizes="(min-width:760px) 720px, 100vw")}</figure>{body}</div>
{faq_block(faq) if faq else ''}{cta()}"""
    return page(path, title, desc, b, sch, [(crumb, path)], og_img=photo)

# ------------------------------------------------------------------ pages
HOME_FAQ = [
 ("Is Bedrock Roof free for homeowners?", "Yes. You never pay Bedrock Roof anything. Roofing contractors may pay us for introductions, which is how we keep the service free for you."),
 ("Is Bedrock Roof a roofing company?", "No. We are a referral service. We don't install or repair roofs. We connect you with an independent local roofing contractor, and any work is between you and that contractor."),
 ("How many roofers will contact me?", "We try to match each request with one local roofer instead of sending your number to a long list of companies. You can always get more quotes on your own, and we recommend at least two or three for a full replacement."),
 ("Do I have to hire the roofer?", "No. The inspection and quote are free and there's no obligation to hire anyone."),
 ("Which areas do you serve?", "Homeowners anywhere in the United States can send a request. If we can't find a roofer serving your ZIP code, we'll tell you."),
 ("Can a roofer help with an insurance claim?", "Many roofers will document storm damage with photos and a written estimate you can give your insurer. Whether a claim is covered is up to your insurance company, and nobody can promise approval."),
]

home = f"""
<section class="hero">{pic(P['hero'], 'Suburban house with a newly replaced asphalt shingle roof', 1600, 0.5625, 'bg', lazy=False, sizes='100vw')}
<div class="wrap hgrid"><div class="hcopy"><p class="kick light">Free roof quotes, anywhere in the U.S.</p>
<h1 data-city>Need a new roof? Get a free quote from a local roofer.</h1>
<p class="sub">Tell us what's going on with your roof. We'll connect you with an independent roofing contractor near you for a free inspection and a written quote.</p>
<ul class="ticks"><li>Free for homeowners</li><li>No obligation to hire</li><li>One local roofer, not a flood of calls</li></ul></div>
{form()}</div></section>

<section class="band"><div class="wrap three">
<div><h3>Replacement</h3><p>Old, curling or missing shingles? Get a written quote for a full tear-off and new roof.</p></div>
<div><h3>Repairs and leaks</h3><p>Water stains on the ceiling or a drip in the attic? Get a roofer out before it spreads.</p></div>
<div><h3>Storm damage</h3><p>Hail or wind damage? A roofer can inspect and document it for your insurance claim.</p></div></div></section>

<section class="how wrap"><p class="kick">How it works</p><h2>Three simple steps</h2><div class="steps">
<div class="step">{pic(P['home1'], 'Two-story suburban home', 720, 0.66)}<b>1</b><h3>Tell us about your roof</h3><p>Pick what you need and enter your name, phone and ZIP code.</p></div>
<div class="step">{pic(P['crew2'], 'Roofer working on a shingle roof', 720, 0.66)}<b>2</b><h3>A local roofer reaches out</h3><p>An independent contractor serving your area calls or texts to book a free inspection.</p></div>
<div class="step">{pic(P['couple'], 'Homeowners relaxing at home', 720, 0.66)}<b>3</b><h3>Get a written quote</h3><p>Compare it, ask questions and decide on your own time. No pressure, no obligation.</p></div>
</div><p class="center"><a href="/how-it-works/">More about how it works &rarr;</a></p></section>

<section class="split wrap"><div class="stext"><p class="kick">Why homeowners use Bedrock Roof</p><h2>Straight answers, no runaround</h2>
<p>Finding a roofer usually means calling around, waiting on callbacks and getting pushed for a quick signature. We keep it simple: one request, one local roofer, and honest guides so you know what a fair quote looks like.</p>
<div class="feat"><div><h4>Honest about how we work</h4><p>We're a referral service, not a contractor, and we say so on every page. Roofers may pay us for introductions. You never do.</p></div>
<div><h4>Your number isn't blasted out</h4><p>We aim to share your request with one roofer serving your ZIP code, not a dozen.</p></div>
<div><h4>Know what to check</h4><p>Our free guides show you how to verify a license and insurance, read a quote and spot red flags.</p></div></div></div>
<div class="mosaic">{pic(P['crew1'], 'Two roofers installing shingles', 720, 0.75)}{pic(P['home2'], 'House with a brown metal roof', 720, 0.75)}{pic(P['shingles'], 'Roofer carrying a bundle of shingles', 720, 0.75)}{pic(P['home4'], 'Brick house with a new roof', 720, 0.75)}</div></section>

<section class="guides wrap"><p class="kick">Free homeowner guides</p><h2>Know before you hire</h2><div class="gcards">
<a class="gcard" href="/roof-replacement-cost/">{pic(P['tearoff'], 'Old shingles being removed', 720, 0.6)}<h3>How much does a new roof cost?</h3><p>National price ranges, what drives the cost and how to compare quotes.</p></a>
<a class="gcard" href="/choosing-a-roofer/">{pic(P['crew3'], 'Roofing crew on a residential roof', 720, 0.6)}<h3>How to choose a roofer</h3><p>Check the license, insurance and warranty, and the red flags to avoid.</p></a>
<a class="gcard" href="/storm-damage/">{pic(P['roofsky'], 'Roof against a blue sky', 720, 0.6)}<h3>What to do after storm damage</h3><p>Safety, photos, insurance and how to avoid storm chasers.</p></a>
</div></section>
{faq_block(HOME_FAQ)}
{cta()}"""

how = f"""<section class="phero"><div class="wrap narrow"><p class="kick">How it works</p><h1>How Bedrock Roof works</h1><p class="sub">A free, simple way to get a roofer out to look at your roof. Here's exactly what happens, and how we're paid.</p></div></section>
<div class="wrap narrow prose">
<h2>1. You send a request</h2><p>Choose what you need (new roof, repair, storm damage or inspection) and enter your name, mobile number and ZIP code. A short note helps the roofer come prepared.</p>
<h2>2. We match you with a local roofer</h2><p>We pass your request to an independent roofing contractor that serves your ZIP code. We aim to send each request to one roofer so your phone doesn't ring off the hook. If we can't find anyone in your area, we'll let you know.</p>
<h2>3. The roofer contacts you</h2><p>The roofer calls or texts to set up a free inspection. They'll look at the roof, answer your questions and give you a written quote.</p>
<h2>4. You decide</h2><p>There's no obligation. Compare the quote with others, check the contractor's license and insurance (<a href="/choosing-a-roofer/">here's how</a>) and hire only if it's right for you. Any contract is between you and the roofer.</p>
<figure>{pic(P['home3'], 'Farmhouse with a wrap-around porch', 1200, 0.5, sizes='(min-width:760px) 720px, 100vw')}</figure>
<h2>How we make money</h2><p>Bedrock Roof is free for homeowners. Roofing contractors may pay us a fee for introductions to homeowners who asked to be contacted. That fee never gets added to your bill by us, and it doesn't change your right to say no.</p>
<h2>What we are not</h2><p>We are not a roofing contractor and we don't perform, inspect, guarantee or warranty roofing work. We don't handle insurance claims and can't promise any claim will be approved. Roofers are independent businesses, so always verify a roofer's license and insurance yourself before signing.</p>
</div>{cta()}"""

cost_faq = [
 ("What's the average cost to replace a roof?", "Angi's figures, as reported by NerdWallet, put the national average around $9,500, with most jobs between about $5,800 and $46,000 depending on size, material and location."),
 ("How much does a roof cost per square foot?", "About $4 to $11 per square foot for a typical replacement, according to Angi data cited by NerdWallet. Premium materials like slate and clay tile cost more."),
 ("Why are my quotes so different?", "Quotes vary with the materials, how many layers come off, whether decking needs replacing, ventilation and flashing work, the warranty offered, and the contractor's overhead. Ask each roofer to itemize so you compare the same scope."),
]
cost = article("/roof-replacement-cost/", "Roof Replacement Cost: 2026 Homeowner Guide | Bedrock Roof", "How much does a roof replacement cost?",
 "Typical U.S. roof replacement costs, what drives the price, and how to compare quotes fairly.",
 "Here are typical national price ranges, the factors that move the number up or down, and how to compare quotes so you're not overpaying.",
 """<div class="callout"><b>Quick answer:</b> A full roof replacement in the U.S. averages about <b>$9,500</b>, and most jobs fall between about <b>$5,800 and $46,000</b>. That works out to roughly <b>$4 to $11 per square foot</b>. <span class="src">Source: Angi data, as reported by <a href="https://www.nerdwallet.com/article/mortgage/roof-replacement-cost" rel="nofollow noopener">NerdWallet</a>.</span></div>
<p>These are national ballpark figures. Your price depends on your roof and your market, and the only way to know for sure is a written quote after an inspection.</p>
<h2>What drives the cost</h2>
<ul><li><b>Roof size.</b> Roofers price by the "square" (100 sq ft of roof). Your roof area is usually larger than your home's floor area.</li>
<li><b>Material.</b> Asphalt shingles are the most affordable. Metal, wood shakes, clay or concrete tile and slate cost more but can last longer.</li>
<li><b>Pitch and complexity.</b> Steep roofs, multiple levels, chimneys, skylights and valleys take more labor. NerdWallet notes steep pitches can add roughly $1,000 to $3,000.</li>
<li><b>Tear-off and repairs.</b> Removing old layers and replacing rotted decking adds cost. Ask how decking repairs are priced before you sign.</li>
<li><b>Labor and location.</b> Labor is often more than half the bill and is higher in high-cost areas and after big storms.</li>
<li><b>Permits and warranty.</b> Many areas require a permit. Extended manufacturer warranties are optional extras.</li></ul>
<h2>Common roofing materials</h2>
<table><thead><tr><th>Material</th><th>Cost</th><th>Good to know</th></tr></thead><tbody>
<tr><td>Asphalt shingle</td><td>$</td><td>Most common in the U.S. and the most budget-friendly.</td></tr>
<tr><td>Metal</td><td>$$</td><td>Long-lasting and sheds snow and rain well. Costs more up front.</td></tr>
<tr><td>Wood shake</td><td>$$</td><td>Natural look. Needs more upkeep and may face fire-code limits.</td></tr>
<tr><td>Clay or concrete tile</td><td>$$$</td><td>Popular in warm climates. Heavy, so the structure must support it.</td></tr>
<tr><td>Slate</td><td>$$$$</td><td>Premium and very long-lived. Needs a specialist installer.</td></tr></tbody></table>
<h2>How to compare quotes</h2>
<ol><li>Get at least two or three written quotes for a full replacement.</li>
<li>Make sure each one covers the same scope: tear-off, underlayment, flashing, vents, drip edge, cleanup and disposal.</li>
<li>Ask how decking replacement is priced (per sheet is common).</li>
<li>Compare warranties: the manufacturer's warranty on materials and the contractor's warranty on workmanship.</li>
<li>Be wary of a quote far below the others. It may leave things out.</li></ol>
<h2>Can insurance pay for it?</h2><p>Homeowners insurance may cover damage from a sudden event like hail or wind, but usually not wear and tear from age. Coverage depends on your policy and your insurer's decision. A roofer can document damage, but no one can promise approval. See <a href="/storm-damage/">what to do after storm damage</a>.</p>""",
 "Roof replacement cost", P["tearoff"], cost_faq)

choose_faq = [
 ("How do I check a roofer's license?", "Search your state's contractor licensing board website using the company's name or license number. Licensing rules vary by state, and in some states roofers are licensed by the city or county instead."),
 ("Should I pay a deposit up front?", "A reasonable deposit for materials is common, but be cautious with anyone who wants most or all of the money before work starts, or wants cash only. Check whether your state limits deposits."),
 ("How many quotes should I get?", "For a full replacement, two or three written quotes covering the same scope is a good rule of thumb."),
]
choose = article("/choosing-a-roofer/", "How to Choose a Roofer: Checklist and Red Flags | Bedrock Roof", "How to choose a roofer you can trust",
 "A homeowner checklist for hiring a roofing contractor: license, insurance, written estimates, warranties and red flags.",
 "A roof is one of the biggest repairs most homeowners ever pay for. Use this checklist before you sign with anyone, including any roofer you meet through us.",
 """<h2>Before you hire: the checklist</h2>
<ol><li><b>Check the license.</b> Look the company up on your state contractor licensing board, or your city or county if your state doesn't license roofers. Make sure the name matches the contract.</li>
<li><b>Ask for proof of insurance.</b> Ask for certificates of general liability and workers' compensation insurance, and call the insurer to confirm they're current.</li>
<li><b>Look for a local address and track record.</b> A real business address, reviews on independent sites and references from recent jobs near you.</li>
<li><b>Get it in writing.</b> A detailed written estimate with materials, scope, cleanup, timeline, permit and payment schedule.</li>
<li><b>Understand the warranty.</b> Ask about both the manufacturer's material warranty and the contractor's workmanship warranty, and get both in writing.</li>
<li><b>Confirm the permit.</b> Ask who pulls the permit. In most places it should be the contractor.</li>
<li><b>Pay sensibly.</b> Avoid paying most of the cost up front or in cash. Pay by check or card so there's a record.</li></ol>
<h2>Red flags</h2>
<ul><li>Knocking on doors right after a storm and pressing you to sign that day.</li>
<li>Offering to "cover" or waive your insurance deductible. That can be insurance fraud in many states.</li>
<li>No license number, no written estimate, or a contract with blanks in it.</li>
<li>Asking you to sign over insurance benefits before you understand what you're agreeing to.</li>
<li>A price far below every other quote.</li></ul>
<h2>7 questions to ask any roofer</h2>
<ol><li>What's your license number, and can I see your insurance certificates?</li><li>Will you pull the permit?</li><li>Who will be on the roof: your crew or subcontractors?</li><li>What exactly does the quote include, and how is rotted decking priced?</li><li>What warranties do I get, and who backs them?</li><li>How long will the job take and how do you protect my yard and gutters?</li><li>Can I talk to two customers whose roofs you did this year?</li></ol>
<p>Roofers we connect you with are independent businesses. We encourage you to run every one through this checklist.</p>""",
 "Choosing a roofer", P["crew3"], choose_faq)

storm_faq = [
 ("Will insurance cover storm damage to my roof?", "It may, if your policy covers the type of damage (for example wind or hail) and the damage came from a covered event rather than age or wear. Your insurer decides. Read your policy and talk to your agent."),
 ("How soon should I file a claim?", "Report damage to your insurer promptly. Many policies set deadlines for reporting, so check yours."),
 ("Should I sign with the first roofer who knocks?", "Take your time. Get a written estimate, check the license and insurance, and get more than one opinion before signing."),
]
storm = article("/storm-damage/", "Roof Storm Damage: What to Do Next | Bedrock Roof", "What to do after storm damage to your roof",
 "Step-by-step guide for homeowners after hail, wind or hurricane damage: safety, photos, temporary repairs, insurance and avoiding storm chasers.",
 "Hail, high wind or a hurricane can damage a roof in minutes. Here's what to do in the hours and days after, in the right order.",
 """<h2>1. Stay safe</h2><p>Don't climb on a wet or damaged roof. Watch for downed power lines, and if water is coming through a ceiling near lights or outlets, turn off power to that area if it's safe to do so.</p>
<h2>2. Document everything</h2><p>Take dated photos and video of the roof from the ground, damaged shingles in the yard, gutters, siding, windows and any leaks or stains inside. Keep receipts for anything you spend.</p>
<h2>3. Prevent more damage</h2><p>Your policy may require you to take reasonable steps to prevent further damage, like a tarp over a hole. Put buckets under drips and move belongings. Keep receipts for temporary repairs.</p>
<h2>4. Call your insurance company</h2><p>Report the damage and ask about your deductible (some policies have separate wind or hurricane deductibles), what's covered and the next steps. An adjuster may inspect.</p>
<h2>5. Get a roofer's inspection</h2><p>A roofer can inspect, document damage with photos and give you a written estimate to share with your insurer. Only your insurance company can decide whether a claim is approved.</p>
<h2>6. Watch out for storm chasers</h2><p>After big storms, out-of-town crews often go door to door. Check the license and local address, never pay large sums up front, and don't sign anything under pressure. See our <a href="/choosing-a-roofer/">roofer checklist</a>.</p>""",
 "Storm damage", P["roofsky"], storm_faq)

rr_faq = [
 ("How long does a roof last?", "It depends on material, climate, ventilation and installation. Asphalt shingle roofs commonly last a couple of decades, while metal, tile and slate can last much longer."),
 ("Can I put new shingles over old ones?", "Some areas allow one layer over another, but many roofers recommend a full tear-off so they can inspect the decking. Local codes may limit layers."),
]
rr = article("/roof-repair-or-replace/", "Roof Repair or Replacement? How to Decide | Bedrock Roof", "Should you repair or replace your roof?",
 "Signs your roof can be repaired versus signs it's time for a full replacement.",
 "Not every leak means you need a new roof. Here's how roofers usually think about repair versus replacement.",
 """<h2>A repair may be enough when</h2><ul><li>The damage is limited to a small area, like a few missing shingles or a flashing leak around a chimney or vent.</li><li>The roof is relatively young and otherwise in good shape.</li><li>The decking underneath is solid.</li></ul>
<h2>Replacement makes more sense when</h2><ul><li>The roof is near the end of its expected life.</li><li>Shingles are curling, cracking or losing granules across large areas.</li><li>There are multiple leaks, sagging, or soft spots in the decking.</li><li>Repairs keep adding up year after year.</li><li>Your insurer is asking questions about the roof's age or condition.</li></ul>
<h2>Get an honest opinion</h2><p>Ask the roofer to show you photos of what they found and explain why they recommend repair or replacement. For a big decision, a second opinion is always reasonable.</p>""",
 "Repair or replace", P["home5"], rr_faq)


# ------------------------------------------------------------------ more guides
leak_faq = [
 ("Can I put a tarp on my roof myself?", "Only if it's safe. Wet and steep roofs are dangerous. Many roofers offer emergency tarping, and your insurer may expect reasonable steps to prevent more damage."),
 ("Will homeowners insurance pay for a roof leak?", "It depends on the cause. Sudden damage, like a tree limb or wind, is often covered, while leaks from age or wear usually aren't. Your policy and insurer decide."),
]
leak = article("/roof-leak/", "Roof Leaking? What to Do Right Now | Bedrock Roof", "Roof leaking? What to do right now",
 "Step-by-step help for a leaking roof: limit the damage, find the source, and get it repaired properly.",
 "A drip from the ceiling is stressful. Here's how to limit the damage today and get the leak fixed for good.",
 """<h2>Right now: limit the damage</h2><ol><li>Move furniture and electronics out of the way and put a bucket under the drip.</li><li>If a ceiling stain is bulging, water may be pooling above it. Carefully poke a small hole in the center to let it drain into a bucket, which can keep the ceiling from collapsing.</li><li>If water is near light fixtures or outlets, turn off power to that area at the breaker if you can do so safely.</li><li>Take photos and video of the leak and any damage.</li></ol>
<h2>Common causes of roof leaks</h2><ul><li><b>Flashing</b> around chimneys, vents, skylights and walls that has cracked, rusted or pulled away.</li><li><b>Missing or damaged shingles</b> after wind or hail.</li><li><b>Pipe boots</b> (the rubber seals around plumbing vents) that have cracked with age.</li><li><b>Ice dams</b> in cold climates that push water under shingles.</li><li><b>Clogged gutters</b> that back water up under the roof edge.</li><li><b>An aging roof</b> where the shingles and underlayment have simply worn out.</li></ul>
<h2>Get it inspected</h2><p>Water often travels along rafters before it drips, so the leak on your ceiling may be several feet from the hole in the roof. A roofer can trace it and tell you whether a repair will do or whether the roof is near the end of its life. See <a href="/roof-repair-or-replace/">repair or replace?</a></p>""",
 "Roof leak", P["home5"], leak_faq)

hail_faq = [
 ("Can hail damage a roof without causing a leak?", "Yes. Hail can bruise shingles and knock off the protective granules, which shortens the roof's life and can lead to leaks later."),
 ("How long do I have to file a hail claim?", "It depends on your policy and state. Many policies set a deadline for reporting damage, so check yours and report promptly."),
 ("What are impact-resistant shingles?", "Shingles tested to resist hail impacts, often labeled Class 4. They cost more, but some insurers in hail-prone states offer premium discounts for them."),
]
hail = article("/hail-damage-roof/", "Hail Damage on Your Roof: Signs and Next Steps | Bedrock Roof", "How to tell if hail damaged your roof",
 "How to spot hail damage on a roof, what to do after a hailstorm, and how insurance claims usually work.",
 "Hail damage is easy to miss from the ground. Here are the signs to look for after a storm and what to do next.",
 """<h2>Signs to look for from the ground</h2><ul><li>Dents in gutters, downspouts, vents and air-conditioning units.</li><li>Granules from shingles collecting in gutters or at the bottom of downspouts.</li><li>Damaged siding, window screens or outdoor furniture.</li><li>Shingle pieces in the yard.</li></ul>
<h2>What hail does to shingles</h2><p>Hail can leave dark spots where granules were knocked off, soft "bruises" that feel like a bruised apple, and cracks or punctures. Damage that looks minor can still shorten a roof's life. Please don't climb on the roof yourself. A roofer can inspect safely and photograph what they find.</p>
<h2>After a hailstorm</h2><ol><li>Photograph damage you can see from the ground, along with the hail itself if you can, with dates.</li><li>Get a roofer's inspection and written findings.</li><li>Report the damage to your insurer and ask about your deductible. Some states and policies have separate wind and hail deductibles.</li><li>Be careful with storm chasers knocking on doors. Check the license and local address of anyone you hire. See <a href="/choosing-a-roofer/">how to choose a roofer</a>.</li></ol>""",
 "Hail damage", P["roofsky"], hail_faq)

ins_faq = [
 ("Will insurance replace an old roof?", "Usually only if a covered event, like a storm, damaged it. Normal wear and tear from age generally isn't covered. Some policies pay less on older roofs, so read yours."),
 ("What's the difference between replacement cost and actual cash value?", "Replacement cost coverage pays to replace the roof with similar materials, minus your deductible. Actual cash value subtracts depreciation for the roof's age, so it pays less."),
 ("Should a roofer handle my insurance claim?", "A roofer can document damage and give you an estimate, but your claim is between you and your insurer. Be careful about signing anything that hands over your insurance benefits before you understand it, and never agree to have your deductible waived."),
]
ins = article("/insurance-roof-replacement/", "Does Homeowners Insurance Cover Roof Replacement? | Bedrock Roof", "Does homeowners insurance cover roof replacement?",
 "When homeowners insurance usually pays for roof damage, when it doesn't, and how the claim process works.",
 "Insurance can pay for a new roof in some cases, but not all. Here's how it usually works, in plain English.",
 """<p class="note"><i>This is general information, not insurance or legal advice. Your policy and your insurer decide what's covered.</i></p>
<h2>What's usually covered</h2><p>Most standard homeowners policies cover sudden, accidental damage from covered events, such as wind, hail, fire or a falling tree. If a storm damages your roof, your policy may pay to repair or replace it, minus your deductible.</p>
<h2>What usually isn't</h2><ul><li>Wear and tear from age.</li><li>Damage from lack of maintenance, like long-term leaks that weren't fixed.</li><li>Problems from poor installation.</li><li>Events your policy excludes, such as flood (which needs separate flood insurance).</li></ul>
<h2>Things that affect your payout</h2><ul><li><b>Your deductible.</b> Some policies, especially in coastal and hail-prone states, have separate percentage deductibles for wind, hail or hurricanes.</li><li><b>Replacement cost or actual cash value.</b> Actual cash value pays less because it subtracts depreciation for the roof's age.</li><li><b>Roof age.</b> Some insurers limit coverage on older roofs or ask about roof age before renewing a policy.</li></ul>
<h2>How a roof claim usually works</h2><ol><li>Document the damage with dated photos.</li><li>Report it to your insurer promptly.</li><li>An adjuster inspects the roof.</li><li>Get a roofer's written estimate so you can compare it with the adjuster's.</li><li>If you disagree with the decision, ask your insurer how to dispute it.</li></ol>
<p>See also: <a href="/storm-damage/">what to do after storm damage</a> and <a href="/hail-damage-roof/">hail damage</a>.</p>""",
 "Insurance and roofs", P["home4"], ins_faq)

signs_faq = [
 ("Is a roof inspection worth it if I don't see a leak?", "Often yes, especially after a big storm or if the roof is getting older. Small problems are cheaper to fix before they become leaks."),
 ("Are black streaks on my roof a problem?", "They're usually algae. It's mostly cosmetic, though it can be cleaned, and algae-resistant shingles prevent it."),
]
signs = article("/signs-you-need-a-new-roof/", "9 Signs You Need a New Roof | Bedrock Roof", "9 signs you might need a new roof",
 "Warning signs that your roof may need repair or replacement, from curling shingles to a sagging roof line.",
 "Roofs rarely fail all at once. These are the signs roofers look for when deciding whether it's time for a new one.",
 """<ol><li><b>Age.</b> If your roof is approaching the typical lifespan for its material, it's worth an inspection. See <a href="/how-long-does-a-roof-last/">how long roofs last</a>.</li>
<li><b>Curling or cupping shingles.</b> Edges that turn up or centers that sink are signs of wear or poor ventilation.</li>
<li><b>Cracked or missing shingles</b>, especially across several areas of the roof.</li>
<li><b>Granules in the gutters.</b> Shingles shed granules as they age, and heavy loss means less protection.</li>
<li><b>Daylight in the attic</b> or water stains on rafters and decking.</li>
<li><b>Ceiling stains or leaks</b> inside the home.</li>
<li><b>A sagging roof line</b>, which can mean water damage or structural problems and should be checked soon.</li>
<li><b>Damaged flashing</b> around chimneys, vents and skylights.</li>
<li><b>Rising energy bills</b> together with an old roof can point to ventilation or insulation problems.</li></ol>
<p>One sign alone doesn't always mean you need a whole new roof. A good roofer will explain what they see and whether a repair is enough.</p>""",
 "Signs you need a new roof", P["tearoff"], signs_faq)

life_faq = [
 ("What makes a roof wear out faster?", "Intense sun and heat, poor attic ventilation, storms, trees rubbing or dropping debris, and poor installation all shorten a roof's life."),
 ("Does a warranty tell me how long my roof will last?", "Not exactly. Manufacturer warranties cover material defects and often have conditions. Ask your roofer to explain what's covered and for how long."),
]
life = article("/how-long-does-a-roof-last/", "How Long Does a Roof Last? Lifespan by Material | Bedrock Roof", "How long does a roof last?",
 "Typical lifespans for asphalt shingle, metal, tile, slate and wood roofs, and what shortens them.",
 "Every roof wears out eventually. Here's roughly how long common roofing materials last and what affects their lifespan.",
 """<p>These are general ranges. Climate, installation quality, ventilation and maintenance can move the real number a lot in either direction.</p>
<table><thead><tr><th>Material</th><th>Typical lifespan</th></tr></thead><tbody>
<tr><td>Asphalt shingles</td><td>Roughly 15 to 30 years, with architectural shingles at the longer end</td></tr>
<tr><td>Metal</td><td>Often 40 years or more</td></tr>
<tr><td>Wood shakes</td><td>Roughly 20 to 40 years with upkeep</td></tr>
<tr><td>Clay or concrete tile</td><td>50 years or more for the tiles, though the underlayment may need replacing sooner</td></tr>
<tr><td>Slate</td><td>Often 75 years or more</td></tr>
<tr><td>Flat roofs (TPO, EPDM, modified bitumen)</td><td>Roughly 15 to 30 years depending on the system</td></tr></tbody></table>
<h2>What shortens a roof's life</h2><ul><li>Hot, sunny climates and strong UV.</li><li>Hail, wind and storms.</li><li>Poor attic ventilation that traps heat and moisture.</li><li>Overhanging trees, clogged gutters and moss.</li><li>Poor installation.</li></ul>
<h2>How to make it last</h2><ul><li>Keep gutters clean and trim back branches.</li><li>Have the roof checked after major storms.</li><li>Fix small problems like loose flashing or cracked pipe boots early.</li><li>Make sure the attic is properly ventilated and insulated.</li></ul>""",
 "Roof lifespan", P["home2"], life_faq)

GUIDES = [("/roof-replacement-cost/", "How much does a roof replacement cost?", "National price ranges and how to compare quotes."),
 ("/choosing-a-roofer/", "How to choose a roofer you can trust", "License, insurance, warranties and red flags."),
 ("/storm-damage/", "What to do after storm damage", "Safety, photos, insurance and storm chasers."),
 ("/hail-damage-roof/", "How to tell if hail damaged your roof", "Signs to look for and what to do next."),
 ("/roof-leak/", "Roof leaking? What to do right now", "Limit the damage and find the cause."),
 ("/insurance-roof-replacement/", "Does insurance cover roof replacement?", "What's usually covered and how claims work."),
 ("/signs-you-need-a-new-roof/", "9 signs you might need a new roof", "What roofers look for."),
 ("/how-long-does-a-roof-last/", "How long does a roof last?", "Lifespan by material."),
 ("/roof-repair-or-replace/", "Should you repair or replace your roof?", "How to decide.")]
guides_idx = f"""<section class="phero"><div class="wrap narrow"><p class="kick">Guides</p><h1>Homeowner roofing guides</h1><p class="sub">Plain-English answers to the questions homeowners ask before hiring a roofer.</p></div></section>
<div class="wrap narrow states">""" + "".join(f'<div class="srow"><h3><a href="{u}">{t}</a></h3><p>{d}</p></div>' for u, t, d in GUIDES) + "</div>" + cta()

faq_all = HOME_FAQ + [
 ("What happens after I submit the form?", "We pass your request to an independent roofer serving your ZIP code, who will call or text you to set up a free inspection."),
 ("Is the inspection really free?", "Roofers in our referrals offer free inspections and quotes for homeowners who request them. If a roofer ever asks to charge you for an inspection, you're free to say no."),
 ("Do you check roofers' licenses and insurance?", "Roofers are independent businesses and we don't guarantee their work. Always verify the license with your state or local licensing board and ask for current insurance certificates before you sign. Our <a href='/choosing-a-roofer/'>checklist</a> shows you how."),
 ("Will you sell my information?", "We share your request only with the roofer we match you with so they can contact you about your roof. We don't sell your information to marketing lists. See our <a href='/privacy/'>privacy policy</a>."),
 ("How do I stop calls or texts?", "Reply STOP to any text, tell the caller you're no longer interested, or email " + EMAIL + "."),
]
faq = f"""<section class="phero"><div class="wrap narrow"><p class="kick">FAQ</p><h1>Questions homeowners ask</h1><p class="sub">Straight answers about how Bedrock Roof works.</p></div></section>
{faq_block(faq_all, "All questions")}{cta()}"""

about = f"""<section class="phero"><div class="wrap narrow"><p class="kick">About us</p><h1>About Bedrock Roof</h1><p class="sub">We help homeowners take the first step on a roof project: getting a qualified local roofer to come take a look.</p></div></section>
<div class="wrap narrow prose"><figure>{pic(P['kitchen'], 'Homeowners at home in the kitchen', 1200, 0.5, sizes='(min-width:760px) 720px, 100vw')}</figure>
<p>Bedrock Roof is a free referral service for homeowners across the United States. You tell us what's going on with your roof, and we connect you with an independent roofing contractor serving your area for a free inspection and quote.</p>
<h2>What we believe</h2><p>Hiring a roofer shouldn't mean dozens of sales calls or pressure to sign on the spot. We keep the process simple, we're clear about how we're paid, and we publish plain-English guides so you can make your own decision.</p>
<h2>How we're paid</h2><p>Roofing contractors may pay us for introductions to homeowners who asked to be contacted. Homeowners never pay us.</p>
<h2>What we don't do</h2><p>We're not a roofing contractor. We don't perform, guarantee or warranty roofing work, and we don't decide insurance claims. Every roofer is an independent business, so please verify the license and insurance of any contractor before hiring.</p>
<h2>Contact</h2><p>Email us at <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>Are you a roofer?</h2><p>If you're a licensed, insured roofing contractor and want homeowner requests in your area, email <a href="mailto:{EMAIL}">{EMAIL}</a>.</p></div>{cta()}"""

quotes = f"""<section class="phero short"><div class="wrap narrow"><h1>Get a free roof quote</h1><p class="sub">Free for homeowners and no obligation. Takes about a minute.</p></div></section>
<div class="wrap qwrap">{form('Tell us about your roof', 'g')}
<aside class="side"><h3>What happens next</h3><ol><li>We match your request with an independent roofer serving your ZIP code.</li><li>The roofer calls or texts you to book a free inspection.</li><li>You get a written quote and decide on your own time.</li></ol>
<p class="small">Bedrock Roof is a referral service, not a roofing contractor. <a href="/how-it-works/">How it works</a>.</p>{pic(P['crew1'], 'Roofers installing shingles', 720, 0.66)}</aside></div>"""

privacy = f"""<section class="phero short"><div class="wrap narrow"><h1>Privacy policy</h1><p class="sub">Last updated November 15, 2026</p></div></section>
<div class="wrap narrow prose">
<p>This policy explains what information Bedrock Roof ("we") collects on bedrockroof.com and how we use it.</p>
<h2>Information you give us</h2><p>When you request a quote we collect your name, mobile phone number, ZIP code, the type of help you need and any note you add.</p>
<h2>Information collected automatically</h2><p>We use our own cookieless analytics to understand how the site is used: pages viewed, how you arrived (for example a search engine or a link), device and browser type, approximate city and region based on your IP address, scroll depth and clicks, and whether a form was started or sent. We don't store your IP address with these records. We honor Do Not Track and Global Privacy Control signals by turning this analytics off. The site uses a third-party service (ipwho.is) to estimate your city from your IP address.</p>
<h2>How we use and share it</h2><ul><li>To pass your request to an independent roofing contractor serving your area so they can contact you about your roof. Contractors may pay us for these introductions.</li><li>To contact you about your request by call or text, with your consent.</li><li>To run, secure and improve the site.</li><li>When required by law.</li></ul>
<p>We don't sell your information to data brokers or marketing lists. Once a contractor receives your request, their use of it is governed by their own privacy practices.</p>
<h2>Calls and texts</h2><p>You can opt out of texts by replying STOP, and you can ask us or the contractor to stop calling at any time.</p>
<h2>Your choices</h2><p>To ask what we hold about you, or to have it corrected or deleted, email <a href="mailto:{EMAIL}">{EMAIL}</a>. Depending on your state, you may have additional rights.</p>
<h2>Data storage and security</h2><p>Requests are stored with a cloud database provider and kept only as long as needed for the purposes above. No system is perfectly secure, but we take reasonable steps to protect your information.</p>
<h2>Children</h2><p>This site is for adults and isn't directed to children under 13.</p>
<h2>Changes</h2><p>We may update this policy and will change the date above when we do.</p></div>"""

terms = f"""<section class="phero short"><div class="wrap narrow"><h1>Terms of use</h1><p class="sub">Last updated November 15, 2026</p></div></section>
<div class="wrap narrow prose">
<p>By using bedrockroof.com you agree to these terms.</p>
<h2>What we provide</h2><p>Bedrock Roof is a free referral service that connects homeowners with independent roofing contractors. We are not a roofing contractor, we don't perform roofing work, and we are not a party to any agreement between you and a contractor.</p>
<h2>No endorsement or guarantee</h2><p>Contractors are independent businesses. We don't guarantee, warranty or endorse their work, pricing, licensing, insurance or conduct. You are responsible for checking a contractor's license, insurance and references before hiring.</p>
<h2>Information on this site</h2><p>Our guides are general information, not professional, legal or insurance advice. Prices are national estimates from the sources cited and can differ in your area.</p>
<h2>Insurance claims</h2><p>We don't handle or decide insurance claims and can't promise any claim will be covered.</p>
<h2>Limitation of liability</h2><p>To the fullest extent allowed by law, Bedrock Roof isn't liable for any loss arising from your use of the site or from work performed by any contractor.</p>
<h2>Contact</h2><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>"""

notfound = """<section class="phero"><div class="wrap narrow"><h1>Page not found</h1><p class="sub">That page doesn't exist. <a href="/">Go to the home page</a> or <a href="/get-quotes/">get a free quote</a>.</p></div></section>"""

SVC = {"@type": "Service", "name": "Free roofing contractor referrals", "serviceType": "Roofing contractor referral",
       "provider": {"@id": SITE + "/#org"}, "areaServed": {"@type": "Country", "name": "United States"},
       "audience": {"@type": "Audience", "audienceType": "Homeowners"},
       "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Free for homeowners"}}

PAGES = [
 ("/", page("/", "Free Roof Quotes from Local Roofers | Bedrock Roof",
   "Need a new roof, a repair or storm damage checked? Get a free, no-obligation inspection and quote from an independent local roofer anywhere in the U.S.", home, [SVC, faq_schema(HOME_FAQ)]), "1.0"),
 ("/get-quotes/", page("/get-quotes/", "Get a Free Roof Quote | Bedrock Roof", "Request a free roof inspection and written quote from an independent local roofer. Free for homeowners, no obligation.", quotes, [SVC], [("Get a free quote", "/get-quotes/")]), "0.9"),
 ("/how-it-works/", page("/how-it-works/", "How Bedrock Roof Works | Free Roofer Referrals", "How Bedrock Roof connects homeowners with independent local roofers for free inspections and quotes, and how we're paid.", how, None, [("How it works", "/how-it-works/")]), "0.8"),
 ("/roof-replacement-cost/", cost, "0.8"),
 ("/choosing-a-roofer/", choose, "0.8"),
 ("/storm-damage/", storm, "0.8"),
 ("/roof-repair-or-replace/", rr, "0.7"),
 ("/roof-leak/", leak, "0.8"), ("/hail-damage-roof/", hail, "0.8"), ("/insurance-roof-replacement/", ins, "0.8"),
 ("/signs-you-need-a-new-roof/", signs, "0.7"), ("/how-long-does-a-roof-last/", life, "0.7"),
 ("/guides/", page("/guides/", "Homeowner Roofing Guides | Bedrock Roof", "Free, plain-English roofing guides for homeowners: costs, hiring a roofer, storm and hail damage, leaks and insurance.", guides_idx, None, [("Guides", "/guides/")]), "0.7"),
 ("/faq/", page("/faq/", "Roofing FAQ | Bedrock Roof", "Answers to common homeowner questions about Bedrock Roof, free roof quotes and hiring a roofer.", faq, [faq_schema(faq_all)], [("FAQ", "/faq/")]), "0.7"),
 ("/about/", page("/about/", "About Bedrock Roof", "Bedrock Roof is a free referral service connecting U.S. homeowners with independent local roofing contractors.", about, None, [("About", "/about/")]), "0.5"),
 ("/privacy/", page("/privacy/", "Privacy Policy | Bedrock Roof", "How Bedrock Roof collects, uses and shares information.", privacy, None, [("Privacy policy", "/privacy/")]), "0.2"),
 ("/terms/", page("/terms/", "Terms of Use | Bedrock Roof", "Terms of use for bedrockroof.com.", terms, None, [("Terms of use", "/terms/")]), "0.2"),
]


# ------------------------------------------------------------------ locations
def city_path(c, st): return f"/roofers/{slug(c)}-{st.lower()}/"
def state_path(st): return f"/roofers/{slug(STATES[st][0])}/"

def city_guides(clim):
    first = {"hail": "/hail-damage-roof/", "hurricane": "/storm-damage/", "snow": "/roof-leak/"}.get(clim, "/signs-you-need-a-new-roof/")
    urls = [first] + [u for u in ["/roof-replacement-cost/", "/choosing-a-roofer/", "/insurance-roof-replacement/"] if u != first]
    t = {u: t for u, t, _ in GUIDES}
    return "".join(f'<a href="{u}">{t[u]}</a>' for u in urls)

def city_page(c, st, clim):
    sname = STATES[st][0]; cl = CLIMATES[clim]; path = city_path(c, st)
    risks = "".join(f"<li>{r[0].upper()+r[1:]}.</li>" for r in cl["risks"])
    others = [x for x in CITIES if x[1] == st and x[0] != c]
    near = "".join(f'<a href="{city_path(o[0], o[1])}">{o[0]}</a>' for o in others)
    fq = [
     (f"Do roofers need a license in {sname}?", STATE_LICENSE[st]),
     (f"How do I find a good roofer in {c}?", f"Get two or three written quotes, check each contractor's license or registration, ask for proof of liability and workers' comp insurance, and read the warranty terms. Our <a href='/choosing-a-roofer/'>roofer checklist</a> walks you through it."),
     (f"How much does a new roof cost in {c}?", f"It depends on the size, pitch and material of your roof and on local labor costs. Nationally, Angi data reported by NerdWallet puts the average around $9,500, with most jobs between about $5,800 and $46,000. A written quote after an inspection is the only way to know your price in {c}."),
     (f"Is the roof inspection free?", "Yes. Requests through Bedrock Roof are for a free inspection and quote, with no obligation to hire."),
     (f"Do I need a permit to replace my roof in {c}?", f"Most U.S. cities require a building permit for a full roof replacement. Ask your roofer to pull the permit with the {c} or county building department and show it to you."),
    ]
    body = f"""<section class="phero city">{pic(P[cl['photo']], f'Home in the {c} area', 1600, 0.45, 'bg', lazy=False, sizes='100vw')}<div class="wrap hgrid"><div class="hcopy">
<p class="kick light"><a href="{state_path(st)}">{sname}</a> &rsaquo; {c}</p><h1>Roofers near {c}, {st}</h1>
<p class="sub">Get a free roof inspection and written quote from an independent roofing contractor serving {c}. Free for homeowners, no obligation.</p></div>
{form(f'Free roof quote in {c}', 'c')}</div></section>
<div class="wrap narrow prose">
<h2>Roofing in {c}: what to know</h2><p>{CITY_LOCAL[c]}</p><p>More broadly, {c} is in the {cl['label']}. The most common causes of roof damage in this kind of climate are:</p><ul>{risks}</ul>
<h2>Popular roof types around {c}</h2><p>{cl['materials']}</p>
<div class="callout"><b>Local tip:</b> {cl['tip']}</div>
<h2>Checking a roofer's license in {sname}</h2><p>{STATE_LICENSE[st]}</p>
<h2>Before you hire a roofer in {c}</h2><ol><li>Verify the license or registration as described above, and make sure the name matches the contract.</li><li>Ask for current certificates of liability and workers' compensation insurance.</li><li>Get a written, itemized quote and compare at least two.</li><li>Make sure the roofer pulls the permit with the local building department.</li><li>Get the material and workmanship warranties in writing.</li></ol>
<p>Bedrock Roof is a referral service, not a roofing contractor. We connect {c} homeowners with independent local roofers, who may pay us for the introduction. Read <a href="/how-it-works/">how it works</a>.</p>
<h2>Helpful guides</h2><p class="links">{city_guides(clim)}</p>
{f'<h2>Other {sname} cities</h2><p class="links">{near}</p>' if near else ''}</div>
{faq_block(fq, f'{c} roofing questions')}{cta(f'Get a free roof quote in {c}')}"""
    sch = [dict(SVC, name=f"Free roofer referrals in {c}, {st}", areaServed={"@type": "City", "name": f"{c}, {sname}"}), faq_schema(fq)]
    return path, page(path, f"Roofers Near {c}, {st}: Free Roof Inspection & Quote | {BRAND}",
        f"Looking for roofers near {c}, {sname}? Get a free roof inspection and written quote from an independent local roofing contractor. Free, no obligation.",
        body, sch, [(sname, state_path(st)), (c, path)], og_img=P[cl['photo']])

def state_page(st):
    sname, clim = STATES[st]; cl = CLIMATES[clim]; path = state_path(st)
    cities = [x for x in CITIES if x[1] == st]
    links = "".join(f'<a class="chip" href="{city_path(c, s)}">Roofers near {c}</a>' for c, s, _ in cities)
    risks = "".join(f"<li>{r[0].upper()+r[1:]}.</li>" for r in cl["risks"])
    body = f"""<section class="phero"><div class="wrap narrow"><p class="kick"><a href="/roofers/">All states</a> &rsaquo; {sname}</p><h1>Roofers in {sname}</h1>
<p class="sub">Free roof inspections and quotes from independent roofing contractors across {sname}. Pick your city or <a href="/get-quotes/">send a request</a> from anywhere in the state.</p></div></section>
<div class="wrap narrow prose"><h2>{sname} cities</h2><p class="chips">{links}</p>
<p>Don't see your city? Homeowners anywhere in {sname} can <a href="/get-quotes/">request a free quote</a>. If we can't find a roofer serving your ZIP code, we'll let you know.</p>
<h2>Roofing in {sname}</h2><p>Much of {sname} falls in the {cl['label']}. Common roof problems include:</p><ul>{risks}</ul><p>{cl['materials']}</p>
<div class="callout"><b>Tip:</b> {cl['tip']}</div>
<h2>Checking a roofer's license in {sname}</h2><p>{STATE_LICENSE[st]}</p><p>Ask every contractor for their license or registration number and check it before you sign. Our <a href="/choosing-a-roofer/">roofer checklist</a> covers the rest.</p></div>{cta()}"""
    return path, page(path, f"Roofers in {sname}: Free Roof Quotes by City | {BRAND}",
        f"Find roofers in {sname}. Get a free roof inspection and quote from an independent local roofing contractor in your city.",
        body, [dict(SVC, name=f"Free roofer referrals in {sname}", areaServed={"@type": "State", "name": sname})], [(sname, path)])

def hub_page():
    rows = "".join(f'<div class="srow"><h3><a href="{state_path(st)}">{STATES[st][0]}</a></h3><p>' + " &middot; ".join(f'<a href="{city_path(c, s)}">{c}</a>' for c, s, _ in CITIES if s == st) + '</p></div>' for st in sorted(STATES, key=lambda k: STATES[k][0]))
    body = f"""<section class="phero"><div class="wrap narrow"><p class="kick">Find a roofer</p><h1>Roofers near you, by state and city</h1><p class="sub">Homeowners anywhere in the U.S. can <a href="/get-quotes/">request a free quote</a>. Or start with your state below.</p></div></section>
<div class="wrap narrow states">{rows}</div>{cta()}"""
    return "/roofers/", page("/roofers/", f"Find Roofers Near You by State and City | {BRAND}", "Find local roofers by state and city and get a free roof inspection and quote.", body, None, [("Find a roofer", "/roofers/")])

LOC = [hub_page()] + [state_page(st) for st in STATES] + [city_page(c, st, cl or STATES[st][1]) for c, st, cl in CITIES]

def llms():
    g = "\n".join(f"- [{t}]({SITE}{u}): {d}" for u, t, d in GUIDES)
    st = "\n".join(f"- [Roofers in {STATES[s][0]}]({SITE}{state_path(s)})" for s in sorted(STATES, key=lambda k: STATES[k][0]))
    return f"""# {BRAND}

> {BRAND} is a free referral service that connects homeowners anywhere in the United States with independent local roofing contractors for a free roof inspection and written quote. It is free for homeowners; contractors may pay for introductions. {BRAND} is not a roofing contractor and does not perform or warranty roofing work.

Homeowners can request a free quote at {SITE}/get-quotes/ for roof replacement, roof repair or leaks, storm damage, or a roof inspection.

## Guides
{g}

## Find a roofer by state
- [All states and cities]({SITE}/roofers/)
{st}

## Contact
{EMAIL}
"""

def rebase(doc):
    return doc.replace('href="/', f'href="{BASE}/').replace('src="/', f'src="{BASE}/') if BASE else doc

def main():
    for path, doc in LOC:
        PAGES.append((path, doc, "0.6" if path.count("/") > 3 or "-" in path.split("/")[2] else "0.7"))
    for path, doc, _ in PAGES:
        d = os.path.join(ROOT, path.strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(rebase(doc))
    open(os.path.join(ROOT, "404.html"), "w").write(rebase(page("/404.html", "Page not found | Bedrock Roof", "Page not found.", notfound)))
    sm = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{UPDATED}</lastmod><priority>{pr}</priority></url>" for p, _, pr in PAGES)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Applebot"]
    rb = "User-agent: *\nDisallow: /\n" if PREVIEW else "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n"
    open(os.path.join(ROOT, "llms.txt"), "w").write(llms())
    open(os.path.join(ROOT, "robots.txt"), "w").write(rb)
    print("built", len(PAGES) + 1, "pages; preview mode" if PREVIEW else "; launch mode")

if __name__ == "__main__":
    main()
