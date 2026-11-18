#!/usr/bin/env python3
"""Builds the static Bedrock Roof site into the repo root.
Run: python3 tools/build.py   (set PREVIEW=0 to drop the noindex tag at launch)
"""
import json, os, html
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from places import CLIMATES, STATES, CITIES, slug
from local import STATE_LICENSE, CITY_LOCAL
import citygen

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://bedrockroof.com"
BRAND = "Bedrock Roof"
EMAIL = "hello@bedrockroof.com"
PREVIEW = os.environ.get("PREVIEW", "1") == "1"
BASE = os.environ.get("BASE", "")  # "/roofcheck" for the github.io preview, "" on bedrockroof.com
PHONE = os.environ.get("PHONE", "")  # e.g. "+13055550123" once the Twilio number exists
UPDATED = "2026-11-18"
INDEXNOW_KEY = "6a9a6bc3df0969e92c11df1a8493d526"  # public key for IndexNow (Bing, Yandex, etc.); the matching file is served at /<key>.txt

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
       ("/commercial-roofing/", "Commercial"), ("/roofers/", "Find a roofer"), ("/faq/", "FAQ")]

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "alternateName": ["Bedrock Roofing", "BedrockRoof", "bedrockroof.com"], "url": SITE + "/",
       "sameAs": ["https://www.facebook.com/profile.php?id=61596870171615"],
       "areaServed": {"@type": "Country", "name": "United States"},
       "logo": SITE + "/assets/logo.svg", "email": EMAIL, **({"telephone": PHONE} if PHONE else {}),
       "description": "Bedrock Roof is a free referral service that connects U.S. homeowners with independent local roofing contractors for inspections and quotes. Bedrock Roof does not perform roofing work."}

def fmt_phone(p):
    d = p[-10:]
    return f"({d[:3]}) {d[3:6]}-{d[6:]}"

def phone_link(cls="tel"):
    return f'<a class="{cls}" href="tel:{PHONE}">Call {fmt_phone(PHONE)}</a>' if PHONE else ""

import hashlib
JS_V = hashlib.md5(open(os.path.join(ROOT, "assets", "site.js"), "rb").read()).hexdigest()[:8]
CSS_V = hashlib.md5(open(os.path.join(ROOT, "assets", "site.css"), "rb").read()).hexdigest()[:8]

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
<link rel="preconnect" href="https://images.unsplash.com">
<link rel="stylesheet" href="/assets/site.css?v={CSS_V}">
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
<div><h4>Guides</h4><a href="/roof-replacement-cost/">Roof replacement cost</a><a href="/choosing-a-roofer/">How to choose a roofer</a><a href="/storm-damage/">After storm damage</a><a href="/hail-damage-roof/">Hail damage</a><a href="/roof-leak/">Roof leaks</a><a href="/roof-insurance-claim/">Filing a roof claim</a><a href="/roofing-scams/">Roofing scams</a><a href="/roofing-materials/">Roofing materials</a><a href="/guides/">All guides</a></div>
<div><h4>Company</h4><a href="/about/">About us</a><a href="/editorial-policy/">Editorial policy</a><a href="/privacy/">Privacy policy</a><a href="/terms/">Terms of use</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
</div><div class="wrap legal">&copy; 2026 {BRAND}. Photos from <a href="https://unsplash.com" rel="nofollow">Unsplash</a>, shown for illustration.</div></footer>
<script src="/assets/site.js?v={JS_V}" defer></script>
</body></html>
"""

FORM = """<form class="qform" novalidate data-form>
<h2>{h}</h2><p class="lead">Free and no obligation. A local roofer will call or text you to set up a time. Homes and commercial buildings.</p>
<fieldset class="need prop"><legend>Property type</legend>
<label><input type="radio" name="prop" value="home" checked><span>Home</span></label>
<label><input type="radio" name="prop" value="commercial"><span>Commercial</span></label>
<label><input type="radio" name="prop" value="multifamily"><span>Apts / HOA</span></label></fieldset>
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

import datetime as _dt0
def article(path, title, h1, desc, intro, body, crumb, photo, faq=None):
    sch = [{"@type": "Article", "headline": h1, "description": desc, "datePublished": UPDATED, "dateModified": UPDATED,
            "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": SITE + path,
            "image": img(photo, 1200, 630)}]
    if faq: sch.append(faq_schema(faq))
    b = f"""<section class="phero"><div class="wrap narrow"><p class="kick">{"Commercial roofing" if path.startswith("/commercial") or path == "/flat-roof-types/" else "Homeowner guide"}</p><h1>{h1}</h1><p class="sub">{intro}</p><p class="meta">Updated {_dt0.date.fromisoformat(UPDATED).strftime("%B %-d, %Y")} &middot; By the {BRAND} team</p></div></section>
<div class="wrap narrow prose"><figure class="lead-img">{pic(photo, h1, 1200, 0.5, lazy=False, sizes="(min-width:760px) 720px, 100vw")}</figure>{body}</div>
<div class="wrap narrow prose"><h2>Related guides</h2><p class="links">RELATED</p></div>
{faq_block(faq) if faq else ''}{cta()}"""
    return page(path, title, desc, b, sch, [(crumb, path)], og_img=photo)

# ------------------------------------------------------------------ pages
HOME_FAQ = [
 ("Is Bedrock Roof free for homeowners?", "Yes. You never pay Bedrock Roof anything. Roofing contractors may pay us for introductions, which is how we keep the service free for you."),
 ("Is Bedrock Roof a roofing company?", "No. We are a referral service. We don't install or repair roofs. We connect you with an independent local roofing contractor, and any work is between you and that contractor."),
 ("How many roofers will contact me?", "We try to match each request with one local roofer instead of sending your number to a long list of companies. You can always get more quotes on your own, and we recommend at least two or three for a full replacement."),
 ("Do I have to hire the roofer?", "No. The inspection and quote are free and there's no obligation to hire anyone."),
 ("Do you help with commercial roofs?", "Yes. Owners and managers of commercial buildings, apartments, condos and HOAs can request a free inspection and quote from an independent commercial roofer. See our <a href=\"/commercial-roofing/\">commercial roofing guide</a>."),
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
<div><h3>Storm damage</h3><p>Hail or wind damage? A roofer can inspect and document it for your insurance claim.</p></div></div>
<div class="wrap"><p class="center"><b>Own or manage a commercial building, apartments or an HOA?</b> We connect you with commercial roofers too. <a href="/commercial-roofing/">Commercial roofing &rarr;</a></p></div></section>

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

# ------------------------------------------------------------------ in-depth guides (Nov 2026)
scam_faq = [
 ("What is a storm chaser roofer?", "A storm chaser is a roofing crew, often from out of state, that follows major hail and wind storms and goes door to door looking for insurance-paid jobs. Some are legitimate, but many are hard to reach once the job is done, which matters when a warranty or leak problem comes up."),
 ("Can a roofer pay or waive my insurance deductible?", "No. Your deductible is your share of the claim. Offering to cover or waive it is a form of insurance fraud, and several states, including Texas and Florida, specifically prohibit contractors from offering it."),
 ("Should I sign a contract with a roofer on the day of the inspection?", "You don't have to, and it's usually better not to. Get at least two written quotes, check the contractor's license and insurance, and read any contract or insurance agreement before signing."),
 ("How much should a roofing deposit be?", "It varies by company and by state, and some states cap deposits on home improvement contracts. Be cautious of anyone who wants a large share of the price in cash before materials arrive, and pay by a traceable method."),
]
scams = article("/roofing-scams/", "Roofing Scams and Red Flags: How to Avoid a Storm Chaser | Bedrock Roof", "Roofing scams and red flags: how to protect yourself",
 "The most common roofing scams after storms, the red flags to watch for, and how to check a roofer before you sign anything.",
 "Most roofers are honest, but storms bring out a few who aren't. These are the scams homeowners run into most, and how to avoid them.",
 """<div class="callout quick"><b>Quick answer:</b> The biggest roofing red flags are a roofer who knocks on your door right after a storm, pushes you to sign the same day, offers to pay or waive your insurance deductible, wants a large cash payment up front, or can't show a license (where your state requires one) and proof of insurance. Check any roofer before you sign, and never let anyone pressure you into a decision on the spot.</div>
<h2>The most common roofing scams</h2>
<h3>1. The door-knock after a storm</h3><p>After hail or high winds, crews go door to door offering free inspections. Some are reputable local companies, but some are out-of-town crews that will be gone when the warranty matters. Ask for a local address and look the company up before you let anyone on your roof.</p>
<h3>2. "We'll cover your deductible"</h3><p>An offer to pay, rebate or waive your deductible sounds generous, but it means the roofer is either inflating the claim or cutting corners on the work. It's a form of insurance fraud, and states including Texas and Florida specifically prohibit it.</p>
<h3>3. Damage that wasn't there before</h3><p>Dishonest inspectors have been caught creating "hail hits" or tearing shingles to make damage look worse. If someone goes up on your roof, ask for clear, dated photos, and consider getting a second opinion before filing a claim.</p>
<h3>4. The contingency agreement that's really a contract</h3><p>Some roofers ask you to sign a form "so we can talk to your insurance company." Read it carefully. Some of these forms commit you to hiring that roofer if the claim is approved. Several states regulate these agreements and give you a short window to cancel, so ask what you're signing and get a copy.</p>
<h3>5. Large cash deposits</h3><p>Paying most of the job in cash before work starts leaves you with little leverage if the crew never shows up. Pay by check or card, keep receipts, and tie payments to progress, like delivery of materials and completion.</p>
<h3>6. The too-good-to-be-true price</h3><p>A bid far below the others can mean skipped underlayment, reused flashing, no permit or uninsured workers. Compare <a href="/roof-replacement-cost/">itemized quotes</a> line by line so you know what each one includes.</p>
<h2>Red flags checklist</h2><ul><li>Pressure to sign today, or "this price is only good right now".</li><li>No physical local address, or a phone number that goes straight to voicemail.</li><li>Can't or won't show a license (where required) and current certificates of liability and workers' comp insurance.</li><li>Offers to handle your claim "for free" in exchange for a signature.</li><li>Asks you to sign a blank or incomplete contract.</li><li>Won't pull a building permit, or asks you to pull it yourself.</li><li>Only accepts cash.</li></ul>
<h2>How to check a roofer in 10 minutes</h2><ol><li>Look up the license or registration on your state or city website. Our <a href="/roofers/">state pages</a> explain each state's rules.</li><li>Ask for certificates of insurance and call the insurer to confirm they're current.</li><li>Search the company name with words like "complaint" or "scam", and check your state attorney general's site.</li><li>Ask for two or three local references from the past year.</li><li>Get the warranty, the scope of work and the payment schedule in writing.</li></ol>
<h2>If you think you've been scammed</h2><p>Stop payment if you can, keep every document and photo, and report it to your state attorney general's consumer protection office and your insurer. The Federal Trade Commission also takes reports at <a href="https://reportfraud.ftc.gov/" rel="nofollow noopener">ReportFraud.ftc.gov</a>.</p>
<p>For the full hiring checklist, see <a href="/choosing-a-roofer/">how to choose a roofer you can trust</a>.</p>""",
 "Roofing scams", P["roofsky"], scam_faq)

mat_faq = [
 ("What is the most common roofing material in the U.S.?", "Asphalt shingles. They cover most American homes because they're affordable, widely available and easy to repair."),
 ("Is a metal roof worth the extra cost?", "It can be if you plan to stay in the home a long time. Metal usually costs more up front but often lasts two to three times as long as asphalt shingles and handles wind, snow and wildfire embers well."),
 ("What roof lasts the longest?", "Natural slate and clay tile can last a century or more when installed and maintained well. Their weight and cost limit where they're used."),
 ("Can I put a new roof over my old shingles?", "Some codes allow one extra layer of asphalt shingles over an existing layer, but many roofers recommend a full tear-off so they can inspect and repair the decking. Your local building code and the shingle manufacturer's warranty terms decide what's allowed."),
]
mats_rows = [
 ("Asphalt shingles", "15 to 30 years", "$", "Most homes; easy to repair; architectural shingles last longer than 3-tab"),
 ("Impact-resistant (Class 4) shingles", "20 to 30 years", "$$", "Hail-prone areas; some insurers offer discounts"),
 ("Standing-seam metal", "40 to 70 years", "$$$", "Wind, snow, wildfire areas; long lifespan"),
 ("Metal shingles or panels (exposed fastener)", "30 to 50 years", "$$", "Budget metal; fasteners need periodic checks"),
 ("Concrete tile", "50 years or more", "$$$", "Hot, sunny and hurricane areas; heavy"),
 ("Clay tile", "50 to 100 years", "$$$$", "Spanish and Mediterranean styles; very heavy"),
 ("Natural slate", "75 to 100+ years", "$$$$", "Historic homes; needs specialist roofers"),
 ("Wood shakes", "20 to 40 years", "$$$", "Look of natural wood; not ideal in wildfire areas unless treated"),
 ("Flat-roof membranes (TPE, EPDM, modified bitumen)", "15 to 30 years", "$$", "Low-slope and flat roofs"),
]
mats_table = "<table class=\"snap\"><thead><tr><th>Material</th><th>Typical lifespan</th><th>Relative cost</th><th>Best for</th></tr></thead><tbody>" + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in mats_rows) + "</tbody></table>"
materials = article("/roofing-materials/", "Roofing Materials Compared: Asphalt vs Metal vs Tile vs Slate | Bedrock Roof", "Roofing materials compared: asphalt, metal, tile and slate",
 "Compare roofing materials side by side: typical lifespan, relative cost and which climates each one suits best.",
 "The right roof depends on your climate, budget, home style and how long you plan to stay. Here's how the main options compare.",
 f"""<div class="callout quick"><b>Quick answer:</b> Asphalt shingles are the cheapest and most common choice and typically last 15 to 30 years. Metal costs more but often lasts 40 to 70 years and handles wind, snow and embers well. Concrete and clay tile suit hot, sunny and hurricane-prone areas and can last 50 years or more. Slate lasts the longest but is the most expensive and heaviest.</div>
<h2>Side-by-side comparison</h2>{mats_table}
<p class="small">Lifespans are typical ranges and depend heavily on installation quality, ventilation, climate and maintenance. Relative cost compares installed price for a typical home, from $ (lowest) to $$$$ (highest).</p>
<h2>How climate changes the choice</h2><ul>
<li><b>Hail country</b> (Texas to the Dakotas and the Front Range): impact-resistant shingles or metal. See <a href="/hail-damage-roof/">hail damage</a>.</li>
<li><b>Hurricane coasts</b>: high-wind-rated shingles, tile or standing-seam metal installed to local wind codes, plus a sealed roof deck.</li>
<li><b>Snow and ice</b>: any good material, plus an ice-and-water barrier at the eaves and proper attic ventilation to prevent ice dams.</li>
<li><b>Desert heat</b>: tile or reflective "cool roof" materials to cut heat gain.</li>
<li><b>Wildfire areas</b>: Class A fire-rated roofing, such as asphalt, metal or tile, with ember-resistant vents.</li>
<li><b>Wet Pacific Northwest</b>: moss-resistant shingles or metal, with careful flashing.</li></ul>
<p>Our <a href="/roofers/">city pages</a> list the main roof risks and common material choices for each city.</p>
<h2>Questions to ask about any material</h2><ol><li>What wind and impact ratings does this product have, and what does my local code require?</li><li>What does the manufacturer's warranty cover, and does it require a certified installer?</li><li>What underlayment, flashing and ventilation are included in the quote?</li><li>Can my roof structure carry the weight? (Important for tile and slate.)</li><li>Are there HOA or historic-district rules on color or material?</li></ol>
<p>Material is only part of the cost. See <a href="/roof-replacement-cost/">roof replacement cost</a> and <a href="/how-long-does-a-roof-last/">how long a roof lasts</a>.</p>""",
 "Roofing materials", P["metal"], mat_faq)

claim_faq = [
 ("Should I call my insurer or a roofer first?", "For obvious damage, report it to your insurer promptly, since policies set deadlines. Many homeowners also have a roofer inspect first so they know whether damage is worth a claim, especially when it might be close to the deductible."),
 ("What is the difference between ACV and RCV?", "Actual cash value (ACV) pays what the roof was worth at the time of the loss, after depreciation. Replacement cost value (RCV) pays to replace it with a similar new roof, often in two payments: the depreciated amount first and the rest after the work is done."),
 ("What if I disagree with the adjuster?", "Ask for the estimate in writing, send your roofer's estimate and photos, and ask for a re-inspection. Many policies include an appraisal clause for disputes over the amount, and you can contact your state's department of insurance."),
 ("Will a roof claim raise my premium?", "It can. Insurers price policies using claim history and local risk. A weather claim affecting a whole area is generally treated differently from a one-off claim, but rules vary by state and insurer."),
]
claim = article("/roof-insurance-claim/", "How to File a Roof Insurance Claim, Step by Step | Bedrock Roof", "How to file a roof insurance claim, step by step",
 "A step-by-step guide to filing a homeowners insurance claim for roof damage: documenting damage, the adjuster visit, ACV vs RCV and what to do if you disagree.",
 "A roof claim goes more smoothly when you know the steps and keep good records. Here's the process from storm to final payment.",
 """<p class="note"><i>This is general information, not insurance or legal advice. Your policy and your insurer decide what's covered.</i></p>
<div class="callout quick"><b>Quick answer:</b> To file a roof claim, document the damage with dated photos, prevent further damage with a tarp if it's safe, read your policy's deductible and deadlines, report the claim promptly, meet the insurance adjuster with your own roofer if possible, and compare the insurer's estimate to a written roofer's estimate before approving work.</div>
<h2>Step 1: Make sure it's safe, then document everything</h2><p>Stay off a wet or damaged roof. From the ground, photograph missing shingles, dented gutters and vents, debris and interior water stains. Note the date of the storm. Local news or weather service reports of hail or high winds that day are useful to keep.</p>
<h2>Step 2: Prevent more damage</h2><p>Most policies expect you to take reasonable steps to stop further damage, like tarping an opening or catching drips. Keep receipts. Your insurer may reimburse reasonable temporary repairs.</p>
<h2>Step 3: Read your policy</h2><ul><li><b>Deductible:</b> Is it a flat amount or a percentage of your home's insured value? Many hurricane and wind-hail deductibles are percentages.</li><li><b>Roof payment terms:</b> Does the policy pay replacement cost (RCV) or actual cash value (ACV) for the roof? Some policies use a payment schedule based on roof age.</li><li><b>Deadlines:</b> Note how long you have to report damage and to complete repairs.</li></ul>
<h2>Step 4: Get a professional inspection</h2><p>A roofer can tell you whether the damage is storm-related and whether repairs are likely to exceed your deductible. Get the findings in writing with photos. Be wary of anyone who pressures you to sign a contract before your claim is decided. See <a href="/roofing-scams/">roofing scams and red flags</a>.</p>
<h2>Step 5: File the claim</h2><p>Report it by phone, app or website. Give the date of loss, describe the damage and share photos. Write down your claim number and the adjuster's name.</p>
<h2>Step 6: The adjuster's inspection</h2><p>The insurer sends an adjuster to inspect the roof. It often helps to have your roofer there to point out damage. Ask for a copy of the adjuster's estimate.</p>
<h2>Step 7: Compare estimates and resolve differences</h2><p>Compare the insurer's estimate line by line with your roofer's. Missing items often include drip edge, starter shingles, ice-and-water barrier, permits and code-required upgrades. If something is missing, send documentation and ask for a supplement or re-inspection. If you still disagree, check your policy's appraisal clause or contact your state's department of insurance.</p>
<h2>Step 8: Get the work done and collect the rest</h2><p>With replacement-cost coverage, insurers often pay the depreciated amount first and release the rest (the "recoverable depreciation") after you send proof the work is complete. Keep the final invoice, permit and photos.</p>
<h2>Mistakes to avoid</h2><ul><li>Waiting months to report damage.</li><li>Signing over your claim rights without reading what you signed.</li><li>Accepting an offer to waive your deductible, which is fraud.</li><li>Paying a large deposit before the claim is approved.</li></ul>
<p>Related: <a href="/insurance-roof-replacement/">does insurance cover roof replacement?</a> and <a href="/storm-damage/">what to do after storm damage</a>.</p>""",
 "Roof insurance claim", P["home4"], claim_faq)

ir_faq = [
 ("What does Class 4 mean on shingles?", "Class 4 is the highest rating in the UL 2218 impact test, in which steel balls are dropped on the shingle. A Class 4 shingle showed no cracking when hit by the largest ball, about 2 inches across."),
 ("Do impact-resistant shingles lower insurance premiums?", "Often, in hail-prone states. Many insurers offer a discount for Class 4 roofs, and the size varies widely. Ask your agent before you choose a shingle, and keep the product paperwork."),
 ("Are impact-resistant shingles hail-proof?", "No. They resist damage much better than standard shingles, but very large hail can still damage them."),
]
impact = article("/impact-resistant-shingles/", "Are Impact-Resistant (Class 4) Shingles Worth It? | Bedrock Roof", "Are impact-resistant (Class 4) shingles worth it?",
 "What Class 4 impact-resistant shingles are, how much more they cost, whether they lower insurance premiums, and who they make sense for.",
 "If you live where hail is common, Class 4 shingles are worth a close look. Here's what they are and how to decide.",
 """<div class="callout quick"><b>Quick answer:</b> Impact-resistant shingles carry a Class 4 rating under the UL 2218 test, the highest impact rating for roofing. They usually cost more than standard architectural shingles, but in hail-prone states many insurers offer premium discounts that can offset part of the extra cost over time. They make the most sense in hail country, such as Texas, Oklahoma, Kansas, Nebraska, Colorado and the Dakotas.</div>
<h2>What "Class 4" means</h2><p>Under UL 2218, steel balls of increasing size are dropped onto the roofing. Class 4 is the top rating: the product showed no cracks after impacts from a ball about 2 inches in diameter. Many Class 4 asphalt shingles use a rubberized (SBS-modified) asphalt that's more flexible than standard shingles. Metal roofing can also earn a Class 4 rating, although it may still dent.</p>
<h2>Pros</h2><ul><li>Fewer hail claims and less chance of a full replacement after a moderate hailstorm.</li><li>Possible insurance discounts in hail-prone states.</li><li>Many carry stronger wind ratings too.</li></ul>
<h2>Cons</h2><ul><li>Higher up-front cost than standard shingles.</li><li>Not hail-proof. Very large hail can still damage them.</li><li>Discounts vary by insurer and aren't guaranteed.</li></ul>
<h2>How to decide</h2><ol><li>Check how often hail hits your area. Our <a href="/roofers/">city pages</a> flag hail where it's a main roof risk.</li><li>Ask your insurance agent what discount, if any, applies to a Class 4 roof and what proof they need.</li><li>Get quotes for both standard and Class 4 shingles so you can compare the real price difference.</li><li>Keep the product label or invoice showing the UL 2218 Class 4 rating.</li></ol>
<p>Related: <a href="/hail-damage-roof/">how to tell if hail damaged your roof</a> and <a href="/roofing-materials/">roofing materials compared</a>.</p>""",
 "Impact-resistant shingles", P["shingles"], ir_faq)

editorial = f"""<section class="phero"><div class="wrap narrow"><p class="kick">Trust</p><h1>Editorial policy</h1><p class="sub">How we write and check the guides and city pages on Bedrock Roof.</p></div></section>
<div class="wrap narrow prose">
<h2>Who writes our content</h2><p>Bedrock Roof's guides and city pages are written and edited by the Bedrock Roof team. We are a referral service, not a roofing contractor, so our guides explain how roofing, hiring and insurance usually work. They are not a substitute for an in-person inspection or for professional insurance or legal advice.</p>
<h2>How we research</h2><ul><li><b>Costs</b> come from published sources, which we name and link, such as Angi data reported by NerdWallet. We don't invent prices or averages.</li><li><b>Licensing rules</b> come from state licensing agencies. Rules change, so every page tells you to check the license with your state or city before hiring.</li><li><b>City facts</b>: population comes from GeoNames, climate type from the K&ouml;ppen-Geiger classification, and county from U.S. Census boundaries. Local notes on storms and conditions are written by hand from public records and news coverage of major events.</li><li><b>Insurance</b>: we explain common policy terms. Your policy and insurer decide what's covered.</li></ul>
<h2>What we won't publish</h2><ul><li>Made-up reviews, testimonials, project photos or job counts.</li><li>Claims that any roofer is licensed, insured or "certified" unless the homeowner can verify it.</li><li>Promises about insurance approval.</li></ul>
<h2>How we make money</h2><p>Homeowners never pay us. Roofing contractors may pay us for introductions to homeowners who asked to be contacted. That doesn't change what our guides say. We recommend getting more than one quote and checking every contractor, including any we introduce you to.</p>
<h2>Corrections</h2><p>If something on this site is wrong or out of date, email <a href="mailto:{EMAIL}">{EMAIL}</a>. We review every report and update the page and its date when we make a change.</p>
<p class="small">Last reviewed {UPDATED}.</p></div>{cta()}"""

# ------------------------------------------------------------------ commercial roofing
com_faq = [
 ("Does Bedrock Roof help with commercial roofs?", "Yes. Owners and managers of commercial buildings, apartment and condo buildings, HOAs, churches, warehouses and retail properties can request a free inspection and quote from an independent commercial roofing contractor."),
 ("What types of commercial roofs are there?", "Most commercial buildings have low-slope or flat roofs covered with a single-ply membrane (TPO, EPDM or PVC), modified bitumen or built-up roofing. Metal roofs are common on warehouses and newer buildings. Roof coatings can extend the life of many of these systems."),
 ("How often should a commercial roof be inspected?", "Many roofing manufacturers and industry groups recommend an inspection at least twice a year, typically in spring and fall, and after any major storm. Regular inspections are often a condition of keeping a manufacturer's warranty in force."),
 ("Can a commercial roof be restored instead of replaced?", "Often, if the existing roof is still mostly dry and sound. A roofer can check for trapped moisture, for example with core samples or an infrared or moisture survey, and tell you whether a coating or restoration system is an option."),
 ("Do commercial roofers need a different license?", "It depends on the state. Some states license commercial roofing separately from residential work, or require a general contractor license for commercial jobs. Our state pages explain each state's rules."),
]
commercial = article("/commercial-roofing/", "Commercial Roofing: Free Inspections and Quotes | Bedrock Roof", "Commercial roofing: free inspections and quotes",
 "Free commercial roof inspections and quotes for property managers, HOAs and building owners: flat roofs, TPO, EPDM, PVC, metal and roof coatings.",
 "For property managers, HOAs, landlords and business owners. Tell us about the building and we'll connect you with an independent commercial roofer.",
 """<div class="callout quick"><b>Quick answer:</b> Bedrock Roof connects owners and managers of commercial buildings, apartment and condo buildings, HOAs and churches with independent commercial roofing contractors for a free inspection and quote. Most commercial roofs are low-slope systems (TPO, EPDM, PVC, modified bitumen or built-up roofing) or metal, and many can be repaired or restored with a coating instead of fully replaced.</div>
<h2>Who we help</h2><ul><li><b>Property managers</b> handling one building or a portfolio.</li><li><b>HOAs and condo associations</b> planning repairs or a reserve-funded replacement.</li><li><b>Apartment and multifamily owners</b>.</li><li><b>Business owners</b>: retail, restaurants, offices, medical buildings.</li><li><b>Warehouses and industrial buildings</b>, often with metal or large single-ply roofs.</li><li><b>Churches, schools and nonprofits</b>.</li></ul>
<h2>Common commercial roof types</h2>
<ul><li><b>TPO</b>: a white single-ply membrane, widely used on new low-slope roofs. It reflects sunlight and has heat-welded seams.</li><li><b>EPDM</b>: a black synthetic rubber membrane with a long track record, common in colder climates.</li><li><b>PVC</b>: a single-ply membrane with heat-welded seams that resists chemicals and grease, which is why it's used on restaurants.</li><li><b>Modified bitumen</b>: asphalt-based sheets applied in layers, common on smaller flat roofs.</li><li><b>Built-up roofing (BUR)</b>: the traditional "tar and gravel" roof made of alternating layers of bitumen and felt.</li><li><b>Metal</b>: standing-seam or through-fastened panels, common on warehouses and pre-engineered buildings.</li><li><b>Roof coatings</b>: silicone, acrylic or polyurethane coatings applied over a sound existing roof to seal it and reflect heat.</li></ul>
<p>See <a href="/flat-roof-types/">flat roof types compared</a> and <a href="/commercial-roof-coatings/">commercial roof coatings</a> for details.</p>
<h2>What a commercial inspection usually covers</h2><ol><li>The membrane or roof surface, seams and penetrations (HVAC curbs, pipes, vents).</li><li>Drainage: drains, scuppers, gutters and any areas where water ponds.</li><li>Flashing at walls, parapets and edges.</li><li>Signs of trapped moisture in the insulation, sometimes checked with core cuts or an infrared or moisture survey.</li><li>Rooftop equipment and foot-traffic damage.</li><li>The age and warranty status of the roof.</li></ol>
<h2>Before you hire a commercial roofer</h2><ul><li>Check the contractor's state license or registration for commercial work. Rules differ by state; see our <a href="/roofers/">state pages</a>.</li><li>Ask for certificates of general liability and workers' comp insurance, and to be named as an additional insured if your lease or lender requires it.</li><li>Ask whether the contractor is certified by the membrane manufacturer, which is often required for a manufacturer's system warranty.</li><li>Get a written scope that lists the roof system, insulation, flashing details, warranty terms and how tenants and operations will be protected during the work.</li><li>Ask for references from similar buildings.</li></ul>
<h2>Maintenance matters more on flat roofs</h2><p>Flat and low-slope roofs don't shed water as quickly as steep roofs, so small problems like a clogged drain or an open seam turn into leaks faster. A twice-yearly inspection and prompt repairs are usually the cheapest way to make a commercial roof last. See our <a href="/commercial-roof-maintenance/">commercial roof maintenance checklist</a>.</p>""",
 "Commercial roofing", P["metal"], com_faq)

flat_faq = [
 ("Which is better, TPO or EPDM?", "Neither is best everywhere. TPO is white and reflective with heat-welded seams, which suits hot climates and cooling-heavy buildings. EPDM is a durable rubber membrane with a long track record, popular in colder climates. Installation quality and the details at seams and edges matter as much as the membrane."),
 ("How long does a flat roof last?", "Single-ply and modified bitumen roofs commonly last about 15 to 30 years, depending on the product, thickness, installation, climate and maintenance."),
 ("Is ponding water on a flat roof a problem?", "Water that stands for more than about 48 hours after rain is generally a sign of a drainage or structural issue. It speeds up wear, can void some warranties and adds weight, so it's worth having a roofer look at it."),
]
flat_rows = [
 ("TPO", "White, reflective; heat-welded seams", "Hot climates; most new low-slope roofs", "15 to 30 years"),
 ("EPDM", "Black (or white) rubber; glued or taped seams", "Cold climates; long track record", "20 to 30+ years"),
 ("PVC", "Heat-welded; resists grease and chemicals", "Restaurants, chemical exposure", "20 to 30 years"),
 ("Modified bitumen", "Asphalt sheets in layers", "Small flat roofs, foot traffic", "15 to 25 years"),
 ("Built-up roof (BUR)", "Layers of bitumen and felt, often with gravel", "Older commercial buildings", "20 to 30 years"),
 ("Coating over existing roof", "Silicone, acrylic or polyurethane", "Extending a sound existing roof", "10 to 20 years, can be renewed"),
]
flat_table = "<table class=\"snap\"><thead><tr><th>System</th><th>What it is</th><th>Often used for</th><th>Typical lifespan</th></tr></thead><tbody>" + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in flat_rows) + "</tbody></table>"
flat = article("/flat-roof-types/", "Flat Roof Types Compared: TPO vs EPDM vs PVC vs Modified Bitumen | Bedrock Roof", "Flat roof types compared: TPO, EPDM, PVC and more",
 "Compare flat and low-slope roofing systems for homes and commercial buildings: TPO, EPDM, PVC, modified bitumen, built-up roofing and coatings.",
 "Flat and low-slope roofs need different materials than shingled roofs. Here's how the main systems compare.",
 f"""<div class="callout quick"><b>Quick answer:</b> The most common flat-roof systems are TPO (white, reflective, heat-welded seams), EPDM (durable rubber, popular in cold climates), PVC (heat-welded and grease-resistant, common on restaurants), modified bitumen and built-up roofing. Most last about 15 to 30 years. Installation quality, drainage and seam details matter as much as the material.</div>
<h2>Side-by-side comparison</h2>{flat_table}
<p class="small">Lifespans are typical ranges and depend on membrane thickness, installation, climate, drainage and maintenance.</p>
<h2>What matters besides the membrane</h2><ul><li><b>Drainage.</b> Tapered insulation, drains and scuppers keep water from ponding.</li><li><b>Insulation.</b> Replacing a roof is often the time to bring insulation up to the current energy code, which may be required.</li><li><b>Attachment.</b> Membranes can be mechanically fastened, fully adhered or ballasted. Wind zone and building type drive the choice.</li><li><b>Edges and flashing.</b> Most flat-roof leaks start at seams, edges, walls and penetrations, not in the middle of the membrane.</li><li><b>Warranty.</b> Manufacturer warranties vary from material-only to full system coverage and often require a certified installer and regular maintenance.</li></ul>
<h2>Homes with flat roofs</h2><p>Rowhouses, mid-century modern homes and additions often have flat or low-slope sections. The same materials apply, and shingles should never be used on a roof that's too flat for them.</p>
<p>Related: <a href="/commercial-roofing/">commercial roofing</a> and <a href="/commercial-roof-coatings/">roof coatings</a>.</p>""",
 "Flat roof types", P["metal"], flat_faq)

coat_faq = [
 ("Can you put a coating on a leaking roof?", "Coatings aren't a fix for an active leak or a wet roof. Leaks need to be repaired and wet insulation replaced first. A coating then goes over a sound, dry roof."),
 ("Silicone or acrylic coating?", "Silicone holds up well to ponding water and UV. Acrylic is usually less expensive and very reflective but is generally not recommended where water ponds. The existing roof type and local climate decide which is a better fit."),
 ("Does a roof coating qualify as a new roof?", "Usually not. It's a restoration that extends the life of the existing roof. Some coating systems come with their own manufacturer warranty, and the terms vary."),
]
coat = article("/commercial-roof-coatings/", "Commercial Roof Coatings: Restore or Replace? | Bedrock Roof", "Commercial roof coatings: restore or replace?",
 "When a silicone, acrylic or polyurethane roof coating makes sense, when it doesn't, and how to compare restoration with full roof replacement.",
 "A coating can add years to a commercial roof for less than a replacement, but only if the roof underneath is in good shape.",
 """<div class="callout quick"><b>Quick answer:</b> A roof coating (silicone, acrylic or polyurethane) can extend the life of a commercial roof that is still mostly dry and sound, usually for less than a full replacement and with less disruption. It's not a fix for a roof with widespread wet insulation, failing seams everywhere or structural problems. A roofer should check for trapped moisture before recommending one.</div>
<h2>When a coating can make sense</h2><ul><li>The roof is aging but still watertight, with only isolated problems that can be repaired first.</li><li>A moisture survey or core cuts show the insulation is mostly dry.</li><li>You want a reflective surface to cut cooling loads.</li><li>You want to delay a full tear-off for budget or tenant reasons.</li></ul>
<h2>When replacement is the better call</h2><ul><li>Large areas of wet insulation.</li><li>Widespread seam failure, blistering or shrinkage.</li><li>Deck damage or structural sagging.</li><li>The roof already has the maximum number of layers allowed by code.</li></ul>
<h2>Main coating types</h2><ul><li><b>Silicone</b>: handles ponding water and UV well. Recoating later usually requires silicone again.</li><li><b>Acrylic</b>: water-based, reflective and usually less expensive. Best where water drains well.</li><li><b>Polyurethane and SPF</b>: tough coatings, and spray polyurethane foam can add insulation and fix low spots.</li></ul>
<h2>Questions to ask</h2><ol><li>How did you check the roof for trapped moisture?</li><li>What repairs will be made before coating, including seams, flashing and drains?</li><li>What coating thickness will be applied, and how will you verify it?</li><li>What warranty comes with the system, and what maintenance does it require?</li></ol>
<p>Related: <a href="/flat-roof-types/">flat roof types compared</a> and <a href="/commercial-roof-maintenance/">commercial roof maintenance checklist</a>.</p>""",
 "Roof coatings", P["metal"], coat_faq)

maint_faq = [
 ("Who is responsible for the roof in a commercial lease?", "It depends on the lease. Many leases make the landlord responsible for the roof structure and replacement, and some assign routine maintenance to the tenant. Check the lease before scheduling work."),
 ("How should an HOA plan for roof replacement?", "Many associations use a reserve study to estimate when roofs will need replacing and how much to set aside. Regular inspections help keep that estimate accurate and catch problems early."),
]
maint = article("/commercial-roof-maintenance/", "Commercial Roof Maintenance Checklist for Property Managers and HOAs | Bedrock Roof", "Commercial roof maintenance checklist",
 "A practical roof maintenance checklist for property managers, HOAs and building owners: what to inspect, how often, and what to document.",
 "Most commercial roof leaks start small. A simple routine catches them early and helps protect your warranty.",
 """<div class="callout quick"><b>Quick answer:</b> Have a commercial roof inspected at least twice a year, typically in spring and fall, and after major storms. Keep drains and gutters clear, limit rooftop foot traffic, fix small seam and flashing problems quickly, and keep a log with photos. Many manufacturer warranties require documented maintenance.</div>
<h2>Twice-a-year checklist</h2><ul><li>Clear drains, scuppers, gutters and downspouts of debris.</li><li>Look for ponding water that stays more than about two days after rain.</li><li>Check seams, edges and flashing at walls, curbs and penetrations.</li><li>Look for blisters, cracks, punctures, shrinkage or loose fasteners.</li><li>Check sealant at pitch pans, pipes and rooftop equipment.</li><li>Inspect walkway pads around HVAC units and service areas.</li><li>Look for interior signs: ceiling stains, wet insulation, musty smells.</li></ul>
<h2>After a storm</h2><ul><li>Check for blown-off edge metal, debris, punctures from hail or branches, and damaged rooftop units.</li><li>Photograph damage with dates before any cleanup.</li><li>Report damage to your insurer promptly. See <a href="/roof-insurance-claim/">filing a roof insurance claim</a>.</li></ul>
<h2>Keep a roof file</h2><p>Keep the installation date, contractor, roof system and warranty, plus every inspection report, repair invoice and photo. It makes warranty claims, insurance claims and budgeting much easier.</p>
<h2>For HOAs and multifamily</h2><p>Coordinate access with residents, plan work around weather and occupancy, and keep your reserve study up to date with current roof conditions.</p>
<p>Related: <a href="/commercial-roofing/">commercial roofing</a>, <a href="/flat-roof-types/">flat roof types</a> and <a href="/commercial-roof-coatings/">roof coatings</a>.</p>""",
 "Commercial roof maintenance", P["metal"], maint_faq)

GUIDES = [("/roof-replacement-cost/", "How much does a roof replacement cost?", "National price ranges and how to compare quotes."),
 ("/choosing-a-roofer/", "How to choose a roofer you can trust", "License, insurance, warranties and red flags."),
 ("/storm-damage/", "What to do after storm damage", "Safety, photos, insurance and storm chasers."),
 ("/hail-damage-roof/", "How to tell if hail damaged your roof", "Signs to look for and what to do next."),
 ("/roof-leak/", "Roof leaking? What to do right now", "Limit the damage and find the cause."),
 ("/insurance-roof-replacement/", "Does insurance cover roof replacement?", "What's usually covered and how claims work."),
 ("/signs-you-need-a-new-roof/", "9 signs you might need a new roof", "What roofers look for."),
 ("/how-long-does-a-roof-last/", "How long does a roof last?", "Lifespan by material."),
 ("/roof-repair-or-replace/", "Should you repair or replace your roof?", "How to decide."),
 ("/roof-insurance-claim/", "How to file a roof insurance claim, step by step", "Documenting damage, the adjuster visit, ACV vs RCV and disputes."),
 ("/roofing-scams/", "Roofing scams and red flags", "Storm chasers, deductible offers and how to check a roofer."),
 ("/roofing-materials/", "Roofing materials compared", "Asphalt, metal, tile and slate: lifespan, cost and best climates."),
 ("/impact-resistant-shingles/", "Are Class 4 impact-resistant shingles worth it?", "Hail ratings, insurance discounts and who should buy them."),
 ("/commercial-roofing/", "Commercial roofing: free inspections and quotes", "For property managers, HOAs and building owners."),
 ("/flat-roof-types/", "Flat roof types compared", "TPO, EPDM, PVC, modified bitumen and built-up roofs."),
 ("/commercial-roof-coatings/", "Commercial roof coatings: restore or replace?", "When silicone, acrylic or polyurethane coatings make sense."),
 ("/commercial-roof-maintenance/", "Commercial roof maintenance checklist", "What property managers and HOAs should inspect, and how often.")]
from guides2 import G2
G2_PAGES = []
for _p, _t, _h, _d, _i, _b, _c, _ph, _fq, _blurb, _rel in G2:
    G2_PAGES.append((_p, article(_p, _t, _h, _d, _i, _b, _c, P[_ph], _fq)))
    GUIDES.append((_p, _h[0].upper() + _h[1:], _blurb))
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
<h2>How we write our guides</h2><p>Our guides are written in plain English, cite their sources, and never include made-up reviews or jobs. Read our <a href="/editorial-policy/">editorial policy</a>.</p>
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
       "audience": [{"@type": "Audience", "audienceType": "Homeowners"}, {"@type": "BusinessAudience", "audienceType": "Commercial property owners, property managers and HOAs"}],
       "category": ["Residential roofing", "Commercial roofing"],
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
 ("/commercial-roofing/", commercial, "0.9"), ("/flat-roof-types/", flat, "0.7"), ("/commercial-roof-coatings/", coat, "0.7"), ("/commercial-roof-maintenance/", maint, "0.7"),
 ("/roof-insurance-claim/", claim, "0.8"), ("/roofing-scams/", scams, "0.8"), ("/roofing-materials/", materials, "0.8"), ("/impact-resistant-shingles/", impact, "0.7"),
 *[(u, d, "0.7") for u, d in G2_PAGES],
 ("/editorial-policy/", page("/editorial-policy/", "Editorial Policy | Bedrock Roof", "How Bedrock Roof researches, writes, checks and corrects its roofing guides and city pages.", editorial, None, [("Editorial policy", "/editorial-policy/")]), "0.4"),
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
    first = {"hail": "/impact-resistant-shingles/", "hurricane": "/storm-damage/", "snow": "/roof-leak/"}.get(clim, "/signs-you-need-a-new-roof/")
    second = "/hail-damage-roof/" if clim == "hail" else "/roofing-materials/"
    urls = [first, second] + [u for u in ["/roof-replacement-cost/", "/roofing-scams/", "/roof-insurance-claim/"] if u not in (first, second)]
    t = {u: t for u, t, _ in GUIDES}
    return "".join(f'<a href="{u}">{t[u]}</a>' for u in urls)

RECS = citygen.load()
PAGE_KEYS = {(slug(r["n"]), r["st"]) for r in RECS}

def city_page(r):
    c, st, clim = r["n"], r["st"], r["clim"]
    sname = STATES[st][0]; cl = CLIMATES[clim]; path = city_path(c, st)
    rl = citygen.risks(r, [x[0].upper() + x[1:] for x in cl["risks"]])
    short = [citygen.RISK_SHORT[f] for f in r["flags"]][:3] or [x.split(" that ")[0].lower() for x in rl[:3]]
    risk_phrase = citygen.join(short)
    risks = "".join(f"<li>{x}.</li>" for x in rl)
    mats = citygen.materials(r, cl["materials"])
    near = [(n, s2, mi) for n, s2, mi in r["nearby"] if (slug(n), s2) in PAGE_KEYS]
    near_html = "".join(f'<a href="{city_path(n, s2)}">{n}</a> <span class="mi">({mi} mi)</span>' for n, s2, mi in near)
    more = [x for x in RECS if x["st"] == st and x is not r and (x["n"], x["st"]) not in {(n, s2) for n, s2, _ in near}][:10]
    more_html = "".join(f'<a href="{city_path(x["n"], st)}">{x["n"]}</a>' for x in more)
    rows = []
    cty = citygen.county(r)
    if cty: rows.append(("County", cty))
    if r["pop"]: rows.append(("Population", f"About {citygen.fmt_pop(r['pop'])}"))
    if r["kg"] in citygen.KOPPEN: rows.append(("Climate", citygen.KOPPEN[r["kg"]].split(",")[0].capitalize() + f" (K&ouml;ppen {r['kg']})"))
    if r["coast_km"] is not None and r.get("ocean") and r["coast_km"] <= 80:
        rows.append(("Nearest coast", f"About {max(1, citygen.km_mi(r['coast_km']))} miles to the {citygen.OCEAN[r['ocean']]}"))
    elif r["lat"]: rows.append(("Nearest coast", "Well inland"))
    rows.append(("Main roof risks", "RISKROW"))
    rows.append(("Roofer licensing", f"<a href=\"#license\">See {sname} rules</a>"))
    rows = [(k, v if v != "RISKROW" else risk_phrase[0].upper() + risk_phrase[1:]) for k, v in rows]
    table = "<table class=\"snap\"><tbody>" + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows) + "</tbody></table>"
    weather_a = f"Around {c}, the most common causes of roof damage are " + "; ".join(x[0].lower() + x[1:] for x in rl[:3]) + "."
    when_a = citygen.season(r)
    lic1 = STATE_LICENSE[st].split(". ")[0].rstrip(".") + "."
    mshort = [citygen.MAT_SHORT[f] for f in r["flags"] if f in citygen.MAT_SHORT][:2]
    quick = (f"The main roof risks in {c} are {risk_phrase}"
             + (f", so roofers here often suggest {', as well as '.join(mshort)}." if mshort else ".")
             + f" {lic1} Compare at least two written quotes before you hire.")
    fq = [
     (f"How much does a new roof cost in {c}?", f"Nationally, Angi data reported by NerdWallet puts the average near $9,500, with most jobs between about $5,800 and $46,000. Your price in {c} depends on size, pitch, material and local labor, so get a written quote."),
     (f"Will insurance pay for roof damage in {c}?", citygen.insurance(r, c)),
     (f"Do I need a permit to replace my roof in {c}?", f"Usually, yes. Your roofer should pull it with the {c} building department{f' or {cty}' if cty else ''} and show it to you before work starts."),
    ]
    body = f"""<section class="phero city">{pic(P[cl['photo']], f'Home in the {c} area', 1600, 0.45, 'bg', lazy=False, sizes='100vw')}<div class="wrap hgrid"><div class="hcopy">
<p class="kick light"><a href="{state_path(st)}">{sname}</a> &rsaquo; {c}</p><h1>Roofers near {c}, {st}</h1>
<p class="sub">Get a free roof inspection and written quote from an independent roofing contractor serving {c}, for homes and commercial buildings. Free, no obligation.</p></div>
{form(f'Free roof quote in {c}', 'c')}</div></section>
<div class="wrap narrow prose">
<div class="callout quick"><b>Quick answer:</b> {quick}</div>
{recent_storms_html(c, st)}
<h2>Roofing in {c}: what to know</h2><p>{r['local']}</p>
<h3>{c} roofing snapshot</h3>{table}
<h2>What wears out roofs around {c}</h2><ul>{risks}</ul>
<h2>Best roofing materials for {c}</h2><p>{mats}</p>
<h2>Best time to replace a roof in {c}</h2><p>{when_a}</p>
<div class="callout"><b>Local tip:</b> {cl['tip']}</div>
<h2 id="license">Checking a roofer's license in {sname}</h2><p>{STATE_LICENSE[st]} Our <a href="/choosing-a-roofer/">roofer checklist</a> covers the rest.</p>
<h2>Commercial roofing in {c}</h2><p>Own or manage a commercial building, apartments or an HOA in {c}? We also connect property owners and managers with independent commercial roofers for flat and low-slope roofs (TPO, EPDM, PVC, modified bitumen), metal roofs and roof coatings. Choose "Commercial" or "Apts / HOA" on the form, or read our <a href="/commercial-roofing/">commercial roofing guide</a>.</p>
<p class="small">Bedrock Roof is a free referral service, not a roofing contractor. Roofers may pay us for introductions. <a href="/how-it-works/">How it works</a>.</p>
<h2>Helpful guides</h2><p class="links">{city_guides(clim)}</p>
{f'<h2>Roofers in nearby cities</h2><p class="links">{near_html}</p>' if near_html else ''}
{f'<h2>More {sname} cities</h2><p class="links">{more_html}</p>' if more_html else ''}
<p class="small">Sources: GeoNames (population), K&ouml;ppen-Geiger (climate), U.S. Census (county). Updated {UPDATED}.</p></div>
{faq_block(fq, f'{c} roofing questions')}{cta(f'Get a free roof quote in {c}')}"""
    city = {"@type": "City", "name": f"{c}, {sname}", "containedInPlace": {"@type": "State", "name": sname}}
    if r["lat"]: city["geo"] = {"@type": "GeoCoordinates", "latitude": round(r["lat"], 4), "longitude": round(r["lon"], 4)}
    sch = [dict(SVC, name=f"Free roofer referrals in {c}, {st}", areaServed=city), faq_schema(fq)]
    return path, page(path, f"Roofers Near {c}, {st}: Free Roof Inspection & Quote | {BRAND}",
        f"Free roof inspection and quote from an independent roofer near {c}, {st}. Main local roof risk: {short[0]}. Plus {st} license rules and FAQs.",
        body, sch, [(sname, state_path(st)), (c, path)], og_img=P[cl['photo']])

def state_page(st):
    sname, clim = STATES[st]; cl = CLIMATES[clim]; path = state_path(st)
    cities = [x for x in RECS if x["st"] == st]
    cities.sort(key=lambda x: -x["pop"])
    links = "".join(f'<a class="chip" href="{city_path(x["n"], st)}">Roofers near {x["n"]}</a>' for x in cities)
    from collections import Counter
    fc = Counter(f for x in cities for f in x["flags"])
    top = [f for f, _ in fc.most_common(4)]
    rl = [citygen.RISK_TEXT[f] for f in top] or [x[0].upper() + x[1:] for x in cl["risks"]]
    risks = "".join(f"<li>{x}.</li>" for x in rl)
    city_block = (f'<h2>{sname} cities</h2><p class="chips">{links}</p>' if links else "")
    body = f"""<section class="phero"><div class="wrap narrow"><p class="kick"><a href="/roofers/">All states</a> &rsaquo; {sname}</p><h1>Roofers in {sname}</h1>
<p class="sub">Free roof inspections and quotes from independent roofing contractors across {sname}. {"Pick your city or " if links else ""}<a href="/get-quotes/">send a request</a> from anywhere in the state.</p></div></section>
<div class="wrap narrow prose">{city_block}
<p>Don't see your city? Homeowners anywhere in {sname} can <a href="/get-quotes/">request a free quote</a>. If we can't find a roofer serving your ZIP code, we'll let you know.</p>
<h2>Common roof problems in {sname}</h2><ul>{risks}</ul><p>{cl['materials']}</p>
<div class="callout"><b>Tip:</b> {cl['tip']}</div>
<h2>Checking a roofer's license in {sname}</h2><p>{STATE_LICENSE[st]}</p><p>Ask every contractor for their license or registration number and check it before you sign. Our <a href="/choosing-a-roofer/">roofer checklist</a> covers the rest.</p></div>{cta()}"""
    return path, page(path, f"Roofers in {sname}: Free Roof Quotes by City | {BRAND}",
        f"Find roofers in {sname}. Get a free roof inspection and quote from an independent local roofing contractor in your city.",
        body, [dict(SVC, name=f"Free roofer referrals in {sname}", areaServed={"@type": "State", "name": sname})], [(sname, path)])

def hub_page():
    rows = "".join(f'<div class="srow"><h3><a href="{state_path(st)}">{STATES[st][0]}</a></h3><p>' + " &middot; ".join(f'<a href="{city_path(x["n"], st)}">{x["n"]}</a>' for x in sorted([x for x in RECS if x["st"] == st], key=lambda x: -x["pop"])) + '</p></div>' for st in sorted(STATES, key=lambda k: STATES[k][0]))
    body = f"""<section class="phero"><div class="wrap narrow"><p class="kick">Find a roofer</p><h1>Roofers near you, by state and city</h1><p class="sub">Homeowners anywhere in the U.S. can <a href="/get-quotes/">request a free quote</a>. Or start with your state below.</p></div></section>
<div class="wrap narrow states">{rows}</div>{cta()}"""
    return "/roofers/", page("/roofers/", f"Find Roofers Near You by State and City | {BRAND}", "Find local roofers by state and city and get a free roof inspection and quote.", body, None, [("Find a roofer", "/roofers/")])

# ------------------------------------------------------------------ storm pages (from tools/storms.json, made by tools/storms.py)
import datetime as _dt
STORMS = json.load(open(os.path.join(ROOT, "tools", "storms.json"))) if os.path.exists(os.path.join(ROOT, "tools", "storms.json")) else []
STORM_SRC = "https://www.spc.noaa.gov/climo/reports/"

def hail_name(x):
    for lim, name in [(4.0, "softball size"), (3.0, "teacup size"), (2.75, "baseball size"), (2.5, "tennis ball size"), (2.0, "hen egg size"),
                      (1.75, "golf ball size"), (1.5, "ping pong ball size"), (1.25, "half dollar size"), (1.0, "quarter size")]:
        if x >= lim: return name
    return "smaller than a quarter"

def hail_effect(x):
    if x >= 2.0: return "Hail this large often causes widespread roof damage, including cracked and punctured shingles, broken tiles, dented metal and damaged skylights, vents and gutters."
    if x >= 1.5: return "Hail this size commonly bruises and cracks asphalt shingles and dents gutters, vents and metal flashing, even on newer roofs."
    if x >= 1.0: return "Hail around an inch can damage asphalt shingles, especially older ones, by knocking off granules and bruising the mat. The damage often isn't visible from the ground."
    return "Smaller hail rarely damages a roof on its own, but it's worth a look if it fell with high winds."

def nice_date(d):
    x = _dt.date.fromisoformat(d)
    return x.strftime("%B ") + str(x.day) + x.strftime(", %Y")

def storm_path(e): return f"/storms/{e['date']}-{slug(e['n'])}-{e['st'].lower()}/"

def storm_kind(e):
    if e["hail_max"] and e["wind_n"]: return "Hail and damaging winds"
    return "Hail" if e["hail_max"] else "Damaging winds"

def storm_page(e):
    c, st = e["n"], e["st"]; sname = STATES[st][0]; d = nice_date(e["date"]); path = storm_path(e)
    kind = storm_kind(e)
    facts = []
    if e["hail_max"]:
        facts.append(f"{e['hail_n']} preliminary hail report{'s' if e['hail_n'] != 1 else ''} within about 12 miles of {c}, with hail up to <b>{e['hail_max']:.2f} inches</b> ({hail_name(e['hail_max'])})")
    if e["wind_n"]:
        w = f", with gusts up to <b>{e['wind_max']} mph</b>" if e["wind_max"] else ""
        facts.append(f"{e['wind_n']} report{'s' if e['wind_n'] != 1 else ''} of damaging wind{w}")
    fact = " and ".join(facts)
    effect = hail_effect(e["hail_max"]) if e["hail_max"] else "Damaging winds can lift and tear off shingles, peel back flashing and drop trees and limbs onto roofs."
    places = "".join(f"<li>{html.escape(p)}</li>" for p in e["places"])
    rec = next((r for r in RECS if r["n"] == c and r["st"] == st), None)
    city_link = f'<a href="{city_path(c, st)}">Roofers near {c}, {st}</a>' if rec else f'<a href="{state_path(st)}">Roofers in {sname}</a>'
    body = f"""<section class="phero"><div class="wrap narrow"><p class="kick"><a href="/storms/">Storm reports</a> &rsaquo; {sname}</p>
<h1>{kind} near {c}, {st} on {d}: what to do about your roof</h1>
<p class="sub">Severe weather was reported around {c}. Here's what was reported, what it can do to a roof, and the steps to take now.</p><p class="meta">Published {d} &middot; Source: NOAA Storm Prediction Center</p></div></section>
<div class="wrap narrow prose">
<div class="callout quick"><b>Quick answer:</b> NOAA's Storm Prediction Center logged {fact} on the storm day of {d}. {effect} Check your roof from the ground, photograph any damage, and have a roofer inspect it before your insurer's deadline for reporting damage.</div>
<h2>What was reported</h2><p>Reports came from these locations near {c}:</p><ul>{places}</ul>
<p class="small">These are preliminary reports from trained spotters, emergency managers and the public, collected by the <a href="{STORM_SRC}" rel="nofollow noopener">NOAA Storm Prediction Center</a>. They can be revised, and storm damage can vary a lot from street to street.</p>
<h2>Signs your roof may be damaged</h2><ul><li>Dents in gutters, downspouts, vents, mailboxes or air-conditioning units.</li><li>Shingle granules collecting at downspouts.</li><li>Missing, cracked or lifted shingles, or pieces in the yard.</li><li>New water stains on ceilings or in the attic.</li></ul>
<p>Hail damage to shingles is often invisible from the ground. See <a href="/hail-damage-roof/">how to tell if hail damaged your roof</a>.</p>
<h2>What to do now</h2><ol><li>Stay off the roof. Watch for downed lines and limbs.</li><li>Take dated photos of damage, including dented metal and any leaks.</li><li>Cover openings or catch drips to prevent more damage, and keep receipts.</li><li>Check your policy's deductible and deadlines, and report damage promptly. See <a href="/roof-insurance-claim/">how to file a roof claim</a>.</li><li>Get a roofer to inspect and document the damage in writing.</li></ol>
<div class="callout"><b>Watch out for storm chasers.</b> After storms, out-of-town crews often go door to door. Don't sign anything on the spot, and never accept an offer to pay or waive your deductible. See <a href="/roofing-scams/">roofing scams and red flags</a>.</div>
<h2>Get a free inspection in {c}</h2><p>Bedrock Roof can connect you with an independent local roofer for a free inspection and written quote, for homes and commercial buildings. More about local roof risks and licensing: {city_link}.</p></div>
<div class="wrap narrow">{form(f'Free storm damage inspection in {c}', 's')}</div>{cta()}"""
    sch = [{"@type": "Article", "headline": f"{kind} near {c}, {st} on {d}", "datePublished": e["date"], "dateModified": e["date"],
            "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": SITE + path,
            "about": {"@type": "City", "name": f"{c}, {sname}"}}]
    title = f"{kind} in {c}, {st} ({_dt.date.fromisoformat(e['date']).strftime('%b')} {_dt.date.fromisoformat(e['date']).day}, {e['date'][:4]}): Roof Damage Checklist | {BRAND}"
    desc = f"{kind} reported near {c}, {sname} on {d}" + (f", hail up to {e['hail_max']:.2f} in." if e["hail_max"] else ".") + " What it can do to your roof, what to do now and how to get a free inspection."
    return path, page(path, title, desc, body, sch, [("Storm reports", "/storms/"), (f"{c} {d}", path)], og_img=P["roofsky"])

def storms_index():
    rows = "".join(f'<div class="srow"><h3><a href="{storm_path(e)}">{storm_kind(e)} near {e["n"]}, {e["st"]}</a></h3><p>{nice_date(e["date"])}'
                   + (f' &middot; hail up to {e["hail_max"]:.2f} in.' if e["hail_max"] else "") + (f' &middot; wind gusts to {e["wind_max"]} mph' if e["wind_max"] else "") + "</p></div>" for e in STORMS[:300])
    empty = "<p>No recent severe hail or wind reports near the cities we cover. Check back after the next storm.</p>"
    body = f"""<section class="phero"><div class="wrap narrow"><p class="kick">Storm reports</p><h1>Recent hail and wind storms by city</h1>
<p class="sub">Severe hail and wind reports near U.S. cities, from NOAA's Storm Prediction Center, with what to do about your roof.</p></div></section>
<div class="wrap narrow states">{rows or empty}<p class="small">Source: preliminary storm reports from the <a href="{STORM_SRC}" rel="nofollow noopener">NOAA Storm Prediction Center</a>. Updated daily.</p></div>{cta()}"""
    return "/storms/", page("/storms/", f"Recent Hail and Wind Storms by City | {BRAND}", "Recent severe hail and wind reports near U.S. cities, with roof damage checklists and free inspections.", body, None, [("Storm reports", "/storms/")])

def recent_storms_html(c, st, days=120):
    today = _dt.date.today()
    ev = [e for e in STORMS if e["n"] == c and e["st"] == st and (today - _dt.date.fromisoformat(e["date"])).days <= days]
    if not ev: return ""
    items = "".join(f'<li><a href="{storm_path(e)}">{storm_kind(e)} on {nice_date(e["date"])}</a>' + (f' (hail up to {e["hail_max"]:.2f} in.)' if e["hail_max"] else "") + "</li>" for e in ev[:5])
    return f'<div class="callout"><b>Recent severe weather near {c}:</b><ul>{items}</ul></div>'

LOC = [hub_page()] + [state_page(st) for st in STATES] + [city_page(r) for r in RECS] + ([storms_index()] if STORMS else []) + [storm_page(e) for e in STORMS]

def llms():
    g = "\n".join(f"- [{t}]({SITE}{u}): {d}" for u, t, d in GUIDES)
    st = "\n".join(f"- [Roofers in {STATES[s][0]}]({SITE}{state_path(s)})" for s in sorted(STATES, key=lambda k: STATES[k][0]))
    return f"""# {BRAND}

> {BRAND} is a free referral service that connects homeowners and commercial property owners, property managers and HOAs anywhere in the United States with independent local roofing contractors for a free roof inspection and written quote. It is free for homeowners; contractors may pay for introductions. {BRAND} is not a roofing contractor and does not perform or warranty roofing work.

Homeowners can request a free quote at {SITE}/get-quotes/ for roof replacement, roof repair or leaks, storm damage, or a roof inspection.

## Guides
{g}

## Find a roofer by state
- [All states and cities]({SITE}/roofers/)
{st}

## City pages
Each city page (for example {SITE}/roofers/houston-tx/) gives a short quick answer, the city's main roof risks, recommended roofing materials, the best time of year for roof work, the state's roofer licensing rules, and local notes. Sources: GeoNames (population), Koppen-Geiger (climate), U.S. Census (county).

## About this site
- [How it works]({SITE}/how-it-works/)
- [Editorial policy]({SITE}/editorial-policy/): how pages are researched and corrected; no made-up reviews or jobs.
- [Full text of the guides]({SITE}/llms-full.txt)

## Contact
{EMAIL}
"""

def to_text(doc):
    """Main content of a page as plain Markdown-ish text, for llms-full.txt."""
    import re, html as H
    m = re.search(r"<main[^>]*>(.*)</main>", doc, re.S)
    t = m.group(1) if m else doc
    t = re.sub(r"<(script|style|form|figure|nav)[^>]*>.*?</\1>", " ", t, flags=re.S)
    t = re.sub(r'<div class="ok".*?</div>', " ", t, flags=re.S)
    t = re.sub(r"<h1[^>]*>(.*?)</h1>", r"\n# \1\n", t, flags=re.S)
    t = re.sub(r"<h2[^>]*>(.*?)</h2>", r"\n## \1\n", t, flags=re.S)
    t = re.sub(r"<h3[^>]*>(.*?)</h3>", r"\n### \1\n", t, flags=re.S)
    t = re.sub(r"<summary[^>]*>(.*?)</summary>", r"\n### \1\n", t, flags=re.S)
    t = re.sub(r"<li[^>]*>", "\n- ", t)
    t = re.sub(r"</(p|div|tr|ul|ol|table)>", "\n", t)
    t = re.sub(r"</t[dh]>", " | ", t)
    t = H.unescape(re.sub(r"<[^>]+>", "", t))
    t = re.sub(r"[ \t]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n\n", t).strip()

def llms_full():
    want = ["/how-it-works/"] + [u for u, _, _ in GUIDES] + ["/faq/", "/editorial-policy/"]
    docs = {p: d for p, d, _ in PAGES}
    parts = [f"# {BRAND}: full text of guides\n\nSource: {SITE}. Free for homeowners; {BRAND} is a referral service, not a roofing contractor. Updated {UPDATED}."]
    for u in want:
        if u in docs: parts.append(f"---\nURL: {SITE}{u}\n\n" + to_text(fill_related(u, docs[u])))
    return "\n\n".join(parts) + "\n"

def rebase(doc):
    return doc.replace('href="/', f'href="{BASE}/').replace('src="/', f'src="{BASE}/') if BASE else doc

RELATED = {
 "/commercial-roofing/": ["/flat-roof-types/", "/commercial-roof-coatings/", "/commercial-roof-maintenance/", "/roof-insurance-claim/"],
 "/flat-roof-types/": ["/commercial-roofing/", "/commercial-roof-coatings/", "/roofing-materials/", "/commercial-roof-maintenance/"],
 "/commercial-roof-coatings/": ["/flat-roof-types/", "/commercial-roof-maintenance/", "/commercial-roofing/", "/roof-repair-or-replace/"],
 "/commercial-roof-maintenance/": ["/commercial-roofing/", "/commercial-roof-coatings/", "/roof-insurance-claim/", "/roofing-scams/"],
 "/roof-replacement-cost/": ["/roofing-materials/", "/choosing-a-roofer/", "/roof-repair-or-replace/", "/insurance-roof-replacement/"],
 "/choosing-a-roofer/": ["/roofing-scams/", "/roof-replacement-cost/", "/roofing-materials/", "/how-long-does-a-roof-last/"],
 "/storm-damage/": ["/roof-insurance-claim/", "/hail-damage-roof/", "/roofing-scams/", "/roof-leak/"],
 "/hail-damage-roof/": ["/impact-resistant-shingles/", "/roof-insurance-claim/", "/storm-damage/", "/roofing-scams/"],
 "/roof-leak/": ["/roof-repair-or-replace/", "/storm-damage/", "/signs-you-need-a-new-roof/", "/roof-insurance-claim/"],
 "/insurance-roof-replacement/": ["/roof-insurance-claim/", "/storm-damage/", "/hail-damage-roof/", "/roofing-scams/"],
 "/signs-you-need-a-new-roof/": ["/how-long-does-a-roof-last/", "/roof-repair-or-replace/", "/roof-replacement-cost/", "/roofing-materials/"],
 "/how-long-does-a-roof-last/": ["/roofing-materials/", "/signs-you-need-a-new-roof/", "/roof-replacement-cost/", "/impact-resistant-shingles/"],
 "/roof-repair-or-replace/": ["/signs-you-need-a-new-roof/", "/roof-replacement-cost/", "/roof-leak/", "/choosing-a-roofer/"],
 "/roof-insurance-claim/": ["/insurance-roof-replacement/", "/storm-damage/", "/roofing-scams/", "/hail-damage-roof/"],
 "/roofing-scams/": ["/choosing-a-roofer/", "/roof-insurance-claim/", "/storm-damage/", "/roof-replacement-cost/"],
 "/roofing-materials/": ["/how-long-does-a-roof-last/", "/impact-resistant-shingles/", "/roof-replacement-cost/", "/choosing-a-roofer/"],
 "/impact-resistant-shingles/": ["/hail-damage-roof/", "/roofing-materials/", "/roof-insurance-claim/", "/roof-replacement-cost/"],
}

RELATED.update({g[0]: g[10] for g in G2})
RELATED["/choosing-a-roofer/"] = ["/roofing-scams/", "/roof-warranty/", "/roof-replacement-permit/", "/roof-replacement-cost/"]
RELATED["/roofing-materials/"] = ["/metal-roof-vs-shingles/", "/how-long-does-a-roof-last/", "/impact-resistant-shingles/", "/roof-replacement-cost/"]
RELATED["/signs-you-need-a-new-roof/"] = ["/roof-inspection/", "/how-long-does-a-roof-last/", "/roof-repair-or-replace/", "/best-time-to-replace-roof/"]
RELATED["/roof-replacement-cost/"] = ["/roofing-materials/", "/metal-roof-vs-shingles/", "/roof-replacement-process/", "/insurance-roof-replacement/"]

def fill_related(path, doc):
    if "RELATED" not in doc: return doc
    t = {u: x for u, x, _ in GUIDES}
    return doc.replace("RELATED", "".join(f'<a href="{u}">{t[u]}</a>' for u in RELATED.get(path, [])))

def main():
    for path, doc in LOC:
        PAGES.append((path, doc, "0.6" if path.count("/") > 3 or "-" in path.split("/")[2] else "0.7"))
    for path, doc, _ in PAGES:
        doc = fill_related(path, doc)
        d = os.path.join(ROOT, path.strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(rebase(doc))
    open(os.path.join(ROOT, "404.html"), "w").write(rebase(page("/404.html", "Page not found | Bedrock Roof", "Page not found.", notfound)))
    sm = "".join(f"<url><loc>{SITE}{p}</loc><lastmod>{UPDATED}</lastmod><priority>{pr}</priority></url>" for p, _, pr in PAGES)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
    bots = ["Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "GPTBot", "PerplexityBot", "ClaudeBot", "Claude-SearchBot", "Google-Extended", "Applebot"]
    rb = "User-agent: *\nDisallow: /\n" if PREVIEW else "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"User-agent: *\nAllow: /\nDisallow: /tools/\n\nSitemap: {SITE}/sitemap.xml\n"
    open(os.path.join(ROOT, "llms.txt"), "w").write(llms())
    open(os.path.join(ROOT, "llms-full.txt"), "w").write(llms_full())
    open(os.path.join(ROOT, INDEXNOW_KEY + ".txt"), "w").write(INDEXNOW_KEY)
    # Google Search Console ownership file; keep it or verification is lost
    open(os.path.join(ROOT, "google1dfcdf84782c73c9.html"), "w").write("google-site-verification: google1dfcdf84782c73c9.html")
    open(os.path.join(ROOT, "robots.txt"), "w").write(rb)
    print("built", len(PAGES) + 1, "pages; preview mode" if PREVIEW else "; launch mode")

if __name__ == "__main__":
    main()
