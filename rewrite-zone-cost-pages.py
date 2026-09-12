#!/usr/bin/env python3
"""Rewrite the cost-to-build-house-{zone} cluster with zone-specific content.

These 58 pages (9-10 zones x 6 languages) were built from one template with the
zone name and a price band swapped in: within each language they measured
0.66-0.79 six-gram similarity page to page, on 420-660 words. This script keeps
the page chrome - head, nav, breadcrumb, H1, the data-cluster related-service
line, the CTA blocks, see-also, trust badges, hreflang - and replaces the lead,
the whole body, the FAQ and the FAQPage JSON-LD from the Z table below.

Usage: python3 rewrite-zone-cost-pages.py [lang:zone ...]   (no args = all in Z)
"""
import os, re, sys, json

BASE = os.path.dirname(os.path.abspath(__file__))

# (lang, zone) -> {"file":..., "title":..., "desc":..., "lead":..., "sections":[(h2,html)], "faq":[(q,a)]}
Z = {}

FILES = {
    "en": ("blog", "cost-to-build-house-%s.html"),
    "es": ("blog-es", "cuanto-cuesta-construir-casa-%s.html"),
    "ru": ("blog-ru", "skolko-stoit-postroit-dom-%s.html"),
    "de": ("blog-de", "hausbau-kosten-%s.html"),
    "fr": ("blog-fr", "cout-construire-maison-%s.html"),
    "zh": ("blog-zh", "%s-jianfang-chengben.html"),
}

def _plain(s):
    return re.sub(r"<[^>]+>", "", s).replace('"', "'").strip()

def rewrite(lang, zone):
    c = Z[(lang, zone)]
    d, pat = FILES[lang]
    path = os.path.join(BASE, d, c.get("file", pat % zone))
    html = open(path, encoding="utf-8").read()

    # ---- body region: after the lead (and the related-service line) to the dark CTA
    m_lead = re.search(r'<p class="lead">.*?</p>', html, re.S)
    if not m_lead:
        raise SystemExit(f"no lead in {path}")
    html = html[:m_lead.start()] + f'<p class="lead">{c["lead"]}</p>' + html[m_lead.end():]
    m_lead = re.search(r'<p class="lead">.*?</p>', html, re.S)

    start = m_lead.end()
    m_rel = re.compile(r'\s*<p data-cluster="blog">.*?</p>', re.S).match(html, start)
    if m_rel:
        start = m_rel.end()
    end = html.index('<div class="bg-dark text-white p-4 rounded my-4 text-center">')

    body = "\n"
    for h2, inner in c["sections"]:
        body += f"<h2>{h2}</h2>\n{inner}\n"
    html = html[:start] + body + html[end:]

    # ---- FAQ accordion (heading text stays in the page's own language)
    def faq_html():
        out = '<div class="accordion my-4" id="faqxAcc">\n'
        for i, (q, a) in enumerate(c["faq"]):
            out += (f'<div class="accordion-item"><h3 class="accordion-header">'
                    f'<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" '
                    f'data-bs-target="#faqx{i}">{q}</button></h3>\n'
                    f'<div id="faqx{i}" class="accordion-collapse collapse" data-bs-parent="#faqxAcc">'
                    f'<div class="accordion-body">{a}</div></div></div>\n')
        return out + "</div>\n"
    html = re.sub(r'<div class="accordion my-4" id="faqxAcc">.*?\n</div>\n', faq_html(), html, count=1, flags=re.S)

    # ---- FAQPage JSON-LD rebuilt from the visible questions
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": _plain(q),
         "acceptedAnswer": {"@type": "Answer", "text": _plain(a)}} for q, a in c["faq"]]}
    html = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
                  '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>',
                  html, count=1, flags=re.S)

    # ---- meta
    t, ds = c["title"], c["desc"]
    html = re.sub(r"<title>.*?</title>", "<title>" + t + "</title>", html, count=1, flags=re.S)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        html = re.sub(r"(" + re.escape(attr) + r' content=")[^"]*(")', lambda m: m.group(1) + t + m.group(2), html, count=1)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        html = re.sub(r"(" + re.escape(attr) + r' content=")[^"]*(")', lambda m: m.group(1) + ds + m.group(2), html, count=1)
    # BlogPosting schema description kept in step with the meta description
    html = re.sub(r'("@type": "BlogPosting", "headline": "[^"]*", "description": ")[^"]*(")',
                  lambda m: m.group(1) + _plain(ds) + m.group(2), html, count=1)

    open(path, "w", encoding="utf-8").write(html)
    words = len(re.findall(r"[^\s<>]+", re.sub(r"<[^>]+>", " ", body)))
    return words, os.path.relpath(path, BASE)


Z[("en","cancun")] = {
 "title": "Cost to Build a House in Cancún 2026: Why It Is Cheaper",
 "desc": "Building in Cancún costs less than anywhere else in the corridor. The 2026 per-m² bands, what the discount comes from, and where the savings turn into risk.",
 "lead": "A 150 m&sup2; family home in <strong>Canc&uacute;n</strong> costs roughly <strong>$2.48M&ndash;$3M MXN ($138k&ndash;$167k USD)</strong> turnkey in 2026 &mdash; the lowest figure in the corridor, and about 4% below Playa del Carmen for the same specification. This page explains where that discount comes from and where it stops being a bargain.",
 "sections": [
  ("Why Cancún prices below the rest of the corridor",
   """<p>Canc&uacute;n is the only place in the corridor where scale works in a homebuilder's favour. It has the region's largest construction labour pool, the deepest concentration of material suppliers and fabricators, and enough competing contractors that pricing is genuinely tested. Everywhere south of Puerto Morelos, some part of the job is being brought in from here.</p>
<p>Three specific effects on a budget:</p>
<ul>
<li><strong>Materials at source.</strong> Block, cement, steel, aggregate, aluminium, tile and sanitaryware are bought locally with no corridor freight attached &mdash; on a 150 m&sup2; house that alone is worth several percent.</li>
<li><strong>Trades available without mobilisation.</strong> Specialist work that has to be scheduled and travelled to Tulum or Akumal is a local phone call here.</li>
<li><strong>Inland residential lots.</strong> Most house building in Canc&uacute;n happens in gated inland communities rather than on the shoreline, which means no federal maritime zone, no ZOFEMAT concession question, no turtle-nesting calendar and a lighter environmental file than a coastal lot of the same size.</li>
</ul>
<p>Permits run through the municipality of <strong>Benito Ju&aacute;rez</strong> &mdash; land use, construction licence, alignment and a Director Responsable de Obra &mdash; and for a straightforward residential lot in a serviced subdivision it is among the more predictable processes in the state.</p>"""),
  ("Turnkey cost by home size",
   """<p>Standard-finish turnkey ranges for Canc&uacute;n &mdash; structure, installations and finishes, with land, pool and furniture excluded:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Home size</th><th>Turnkey (MXN)</th><th>Turnkey (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.65M&ndash;$2M</td><td>$92k&ndash;$111k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.48M&ndash;$3M</td><td>$138k&ndash;$167k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.30M&ndash;$4M</td><td>$183k&ndash;$222k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.13M&ndash;$5M</td><td>$229k&ndash;$278k</td></tr>
</tbody></table></div>
<p class="text-muted small">Reference: $16,500&ndash;$20,000 MXN/m&sup2; standard finish. USD/MXN &asymp; 18. Excludes land, pool and furniture.</p>
<p>Those bands apply to inland residential Canc&uacute;n. A lot in the Hotel Zone, on Isla Dorada or anywhere with sea or lagoon frontage is a different building: marine-grade specification throughout, federal-zone questions, and a finish level the location demands. Expect $26,000&ndash;$40,000 MXN/m&sup2; there, not $18,000.</p>"""),
  ("Where the saving turns into risk",
   """<p>A large, competitive market produces low prices and wide quality variance. The failure mode in Canc&uacute;n is not an expensive build, it is a cheap one.</p>
<ul>
<li><strong>Quotes below roughly $14,000 MXN/m&sup2;</strong> are cutting something structural &mdash; usually rebar density, concrete quality or the electrical installation. In a high wind-load region, rebar is the wrong place to economise.</li>
<li><strong>No soil study.</strong> The karst here can give excellent shallow bearing and a cavity two metres away. A study across the footprint costs $25,000&ndash;$60,000 and is the cheapest risk reduction in the project.</li>
<li><strong>Gated community rules.</strong> Communities such as Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua and Palmaris run design committees with their own height, setback, material and colour limits, plus registered-worker access, restricted hours and a construction bond. Submit at concept stage; an unscheduled review cycle is the usual delay.</li>
<li><strong>Traffic and delivery windows.</strong> Canc&uacute;n is the one place in the corridor where city traffic is a programme item &mdash; deliveries into inland subdivisions need timing, and restricted-hour communities compound it.</li>
<li><strong>Salt still reaches inland.</strong> Even several kilometres from the sea, exterior fixings, railings and condenser coils last far longer in 316 stainless and marine-grade coatings than in standard specification.</li>
</ul>
<p>A 150 m&sup2; house takes about <strong>7&ndash;10 months</strong> here from licence to handover, and Canc&uacute;n's supplier depth means fewer of the material-waiting delays that stretch programmes further south. Insist on a fixed-price written contract with a line-item budget and milestone payments against verified progress &mdash; in a market this large, that document is what separates the good contractors from the cheap ones.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build a house in Cancún in 2026?",
   "About $2.48M&ndash;$3M MXN ($138k&ndash;$167k USD) turnkey for a 150 m&sup2; standard-finish home on an inland residential lot, excluding land, pool and furniture &mdash; roughly $16,500&ndash;$20,000 MXN/m&sup2;."),
  ("Why is Cancún cheaper than Playa del Carmen or Tulum?",
   "Scale. It has the corridor's largest labour pool, the densest concentration of suppliers and fabricators, and enough competing contractors to keep pricing honest &mdash; and most house building happens on inland lots, which avoids the federal maritime zone, turtle-nesting rules and the heavier environmental file a coastal lot carries."),
  ("Does that price apply in the Hotel Zone?",
   "No. Hotel Zone, Isla Dorada and any sea or lagoon frontage means marine-grade specification throughout, federal-zone questions and a higher expected finish level &mdash; budget $26,000&ndash;$40,000 MXN/m&sup2; rather than the inland band."),
  ("What is the cheapest a Cancún builder should quote?",
   "Treat anything below roughly $14,000 MXN/m&sup2; as a warning. At that price something structural is being reduced &mdash; typically rebar density, concrete quality or the electrical installation &mdash; and in a high wind-load region those are the wrong savings."),
  ("Do gated communities in Cancún add cost?",
   "Yes. Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua and Palmaris all run design committees with their own limits on height, setbacks, materials and colour, plus worker registration, restricted working hours and a construction bond. Budget for the review cycle in the programme, not just the fees."),
 ],
}

Z[("en","puerto-aventuras")] = {
 "title": "Cost to Build a House in Puerto Aventuras 2026: Full Budget",
 "desc": "Turnkey build costs for Puerto Aventuras plus the marina-community lines buyers miss: HOA, dock or slip, seawall condition and the design committee.",
 "lead": "A 150 m&sup2; home in <strong>Puerto Aventuras</strong> costs roughly <strong>$2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD)</strong> turnkey in 2026 &mdash; about 8% above Playa del Carmen. The build is the predictable part; the lines below it are where marina-community budgets go wrong.",
 "sections": [
  ("Turnkey cost by home size",
   """<p>Standard-finish turnkey ranges for Puerto Aventuras &mdash; structure, installations and finishes; land, pool and furniture excluded:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Home size</th><th>Turnkey (MXN)</th><th>Turnkey (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.85M&ndash;$2.25M</td><td>$103k&ndash;$125k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.77M&ndash;$3.38M</td><td>$154k&ndash;$188k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.70M&ndash;$4.50M</td><td>$206k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.63M&ndash;$5.63M</td><td>$257k&ndash;$313k</td></tr>
</tbody></table></div>
<p class="text-muted small">Reference: $18,500&ndash;$22,500 MXN/m&sup2; standard finish. USD/MXN &asymp; 18. Excludes land, pool and furniture.</p>
<p>The 8% premium over Playa del Carmen is four specific things, not an address surcharge: controlled site access with worker registration, restricted working hours that lengthen the programme, longer material handling inside the community, and the marine-grade specification that canal and near-shore positions require. Each is a real line in the estimate.</p>"""),
  ("The lines buyers forget",
   """<p>These sit outside the build cost and regularly surprise first-time buyers in the community:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Item</th><th>What to establish</th></tr></thead><tbody>
<tr><td><strong>HOA / maintenance fee</strong></td><td>The current figure for that specific lot, the budget behind it and its five-year trend. Canal-front and marina-adjacent lots often carry more.</td></tr>
<tr><td><strong>Dock or slip</strong></td><td>Whether it is owned, leased or assigned &mdash; three different things legally and at resale &mdash; and what it costs annually. Dock works are separately permitted from the house.</td></tr>
<tr><td><strong>Seawall / canal edge</strong></td><td>Condition, assessed by someone who is not selling you the property. Repairing one is its own project.</td></tr>
<tr><td><strong>Design committee</strong></td><td>Submission, review cycle and any construction bond. Budget $60,000&ndash;$250,000 MXN and at least one review round in the programme.</td></tr>
<tr><td><strong>Marine specification</strong></td><td>316 stainless fixings, anodised or marine-coated aluminium, increased concrete cover. Adds to the build and saves far more over a decade.</td></tr>
</tbody></table></div>
<p>Permits themselves run through the municipality of <strong>Solidaridad</strong> &mdash; the same route as Playa del Carmen &mdash; with the community's own architectural review sitting in front of it in practice. For the community process in detail, see our <a href="/blog/construction-costs-puerto-aventuras.html">Puerto Aventuras construction guide</a>.</p>"""),
  ("Canal-front: what changes technically",
   """<p>A canal lot is why people buy here, and it changes the engineering:</p>
<ul>
<li><strong>High water table.</strong> Excavations, cisterns and the pool shell need dewatering and buoyancy consideration &mdash; an emptied pool can float if it is drained at the wrong moment.</li>
<li><strong>Constant salt aerosol</strong> off the water, not seasonal exposure. This is where 316 stainless stops being a preference.</li>
<li><strong>Storm exposure.</strong> Water-adjacent lots take the full wind load and, in a serious event, surge. Laminated or impact-rated glazing on the water elevation is the one specification we would not compromise here.</li>
<li><strong>Edge structures</strong> at the water line have their own design and approval requirements.</li>
</ul>
<p>A 150 m&sup2; house takes about <strong>7&ndash;10 months</strong> from licence to handover, and restricted working hours inside the community mean the programme runs at the longer end rather than the shorter. Contract on a fixed price with a line-item budget and milestone payments tied to verified progress; in a community where access is controlled and hours are limited, an open-ended arrangement is where the schedule quietly drifts.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build a house in Puerto Aventuras?",
   "About $2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD) turnkey for a 150 m&sup2; standard-finish home, excluding land, pool and furniture &mdash; roughly $18,500&ndash;$22,500 MXN/m&sup2;, or about 8% above Playa del Carmen."),
  ("Why is it more expensive than Playa del Carmen?",
   "Four concrete reasons: controlled site access with worker registration, restricted working hours that lengthen the programme, longer material handling inside the community, and the marine-grade specification canal and near-shore lots require. It is not a surcharge for the address."),
  ("What costs are outside the build budget?",
   "The HOA maintenance fee for that specific lot, any dock or slip charge, seawall or canal-edge repair if the existing structure is tired, and the design committee submission and bond at roughly $60,000&ndash;$250,000 MXN. Dock works are separately permitted from the house."),
  ("Do I need approval from the community as well as the municipality?",
   "Yes, and in practice the community comes first. The construction licence and DRO requirement run through Solidaridad, while the community's architectural committee reviews height, setbacks, materials, colours and boundary treatment. Submit at concept stage &mdash; an unscheduled review round is the most common delay here."),
  ("What changes on a canal-front lot?",
   "Dewatering and buoyancy design for excavations and the pool, marine-grade specification throughout because the salt aerosol is constant, impact-rated glazing on the water elevation given the storm exposure, and separate approval for any works at the water's edge."),
 ],
}

Z[("en","akumal")] = {
 "title": "Cost to Build a House in Akumal 2026: Permits Are the Variable",
 "desc": "Akumal build costs for 2026, and why the environmental and permit file — not the walls — is what decides your total. Turtle rules, treatment plant, transport.",
 "lead": "A 150 m&sup2; home in <strong>Akumal</strong> costs roughly <strong>$2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD)</strong> turnkey in 2026. But on an Akumal lot the construction is the predictable half of the budget: the environmental file, the treatment plant and the permit calendar are what actually separate two apparently similar projects.",
 "sections": [
  ("Turnkey cost by home size",
   """<p>Standard-finish turnkey ranges for Akumal &mdash; structure, installations and finishes; land, pool, furniture and the site-specific items below excluded:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Home size</th><th>Turnkey (MXN)</th><th>Turnkey (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.90M&ndash;$2.35M</td><td>$106k&ndash;$131k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.85M&ndash;$3.52M</td><td>$158k&ndash;$196k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.80M&ndash;$4.70M</td><td>$211k&ndash;$261k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.75M&ndash;$5.88M</td><td>$264k&ndash;$326k</td></tr>
</tbody></table></div>
<p class="text-muted small">Reference: $19,000&ndash;$23,500 MXN/m&sup2; standard finish. USD/MXN &asymp; 18. Excludes land, pool and furniture.</p>
<p>That is about 12% above Playa del Carmen, and the premium is transport of every material down the corridor, marine-grade specification for salt exposure, and a smaller local trade base that means some crews travel.</p>"""),
  ("The budget lines that only exist in Akumal",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Line</th><th>MXN</th><th>Why</th></tr></thead><tbody>
<tr><td>Environmental studies and authorisation</td><td>$80,000&ndash;$350,000</td><td>Scope set by vegetation and distance to the shore, not by house size</td></tr>
<tr><td>Treatment plant + absorption well</td><td>$120,000&ndash;$380,000</td><td>No sewer; treatment before infiltration is the centre of the file</td></tr>
<tr><td>Turtle-compliant lighting scheme</td><td>$30,000&ndash;$120,000</td><td>Shielded, low, amber or red on beach-facing elevations</td></tr>
<tr><td>ZOFEMAT survey and concession review</td><td>$20,000&ndash;$80,000</td><td>Only on lots touching the federal maritime zone</td></tr>
<tr><td>Soil study across the footprint</td><td>$25,000&ndash;$60,000</td><td>Karst; a cavity can sit two metres from good bearing</td></tr>
</tbody></table></div>
<p>Note that four of those five scale with the <em>lot</em>, not with the house. That is why a compact Akumal house costs more per square metre than a large one, and why the cheapest saving available on an Akumal project is choosing a lot with an existing environmental authorisation and utilities already at the boundary.</p>"""),
  ("Permit calendar, and what it costs to wait",
   """<p>Akumal sits in the municipality of <strong>Tulum</strong> &mdash; not Solidaridad, which surprises owners because Playa del Carmen is closer. Tulum's review is the most environmentally demanding in the corridor, and the practical consequence is calendar:</p>
<ul>
<li><strong>Environmental file:</strong> 4&ndash;9 months for a house on a vegetated or near-shore lot.</li>
<li><strong>Licence review once the file is complete:</strong> 4&ndash;12 weeks.</li>
<li><strong>Realistic total from purchase to breaking ground:</strong> 6&ndash;14 months.</li>
</ul>
<p>Those months are a real cost: carrying the land, and in most cases holding a construction budget that is not yet earning. They are also the reason a lot with a clean existing authorisation trades at a premium and is usually worth it.</p>
<p>One scheduling item specific to this stretch of coast: turtle nesting runs roughly <strong>May to October</strong>, and beach-adjacent heavy work, floodlighting and activity on the sand are restricted during it. Plan the noisy exterior phases outside that window and the interior fit-out inside it &mdash; a programme that ignores the season loses weeks to it.</p>
<p>Construction itself takes about <strong>7&ndash;10 months</strong> for a 150 m&sup2; house. Contract fixed-price with a line-item budget, and make sure the environmental conditions &mdash; replanting survival, treatment plant records, lighting compliance &mdash; are written into someone's responsibility for after handover, because they continue for the life of the property. For the full permitting picture see our <a href="/blog/building-in-akumal-guide.html">Akumal building guide</a>.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build a house in Akumal in 2026?",
   "About $2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD) turnkey for a 150 m&sup2; standard-finish home &mdash; roughly $19,000&ndash;$23,500 MXN/m&sup2;, some 12% above Playa del Carmen. Land, pool, furniture and the site-specific permit and treatment lines are separate."),
  ("What extra costs does an Akumal lot carry?",
   "Environmental studies and authorisation at $80,000&ndash;$350,000, a treatment plant with absorption well at $120,000&ndash;$380,000, a turtle-compliant lighting scheme at $30,000&ndash;$120,000, a ZOFEMAT survey on federal-zone lots at $20,000&ndash;$80,000, and the soil study at $25,000&ndash;$60,000. Most of those scale with the lot, not the house."),
  ("Which municipality issues the permits for Akumal?",
   "Tulum, not Solidaridad &mdash; a frequent surprise given Playa del Carmen is physically closer. Tulum's environmental review is the most demanding in the corridor, so plan 6&ndash;14 months realistically from purchase to breaking ground."),
  ("Do turtle-nesting rules affect the construction schedule?",
   "Yes. Nesting runs roughly May to October, and beach-adjacent heavy work, floodlighting and activity on the sand are restricted during it. Schedule noisy exterior phases outside the season and interior work inside it. The lighting rules also apply to the finished house in operation."),
  ("Is a smaller house cheaper per square metre in Akumal?",
   "No, it is more expensive per m&sup2;. The environmental file, the soil study, the treatment plant and the utility connection cost roughly the same for 80 m&sup2; as for 200 m&sup2;, so on a compact house those fixed lines are a much larger share of the total."),
 ],
}

Z[("en","puerto-morelos")] = {
 "title": "Cost to Build a House in Puerto Morelos 2026: Best Value",
 "desc": "Puerto Morelos builds at Playa del Carmen prices on cheaper land. The 2026 bands, the reef-park discharge spec, and the Ruta de los Cenotes off-grid option.",
 "lead": "A 150 m&sup2; home in <strong>Puerto Morelos</strong> costs roughly <strong>$2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD)</strong> turnkey in 2026 &mdash; essentially level with Playa del Carmen on construction, on land that is generally cheaper. That combination is why this is the corridor's quiet value play.",
 "sections": [
  ("Turnkey cost by home size, and the three sub-markets",
   """<p>Standard-finish turnkey ranges &mdash; structure, installations and finishes; land, pool and furniture excluded:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Home size</th><th>Turnkey (MXN)</th><th>Turnkey (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.70M&ndash;$2.10M</td><td>$94k&ndash;$117k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.55M&ndash;$3.15M</td><td>$142k&ndash;$175k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.40M&ndash;$4.20M</td><td>$189k&ndash;$233k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.25M&ndash;$5.25M</td><td>$236k&ndash;$292k</td></tr>
</tbody></table></div>
<p class="text-muted small">Reference: $17,000&ndash;$21,000 MXN/m&sup2; standard finish. USD/MXN &asymp; 18. Excludes land, pool and furniture.</p>
<p>Those bands cover town and inland residential lots. The two other sub-markets behave differently:</p>
<ul>
<li><strong>Beachfront and near-shore:</strong> $26,000&ndash;$38,000+ MXN/m&sup2; with marine specification, federal-zone questions and a heavier environmental file.</li>
<li><strong>Ruta de los Cenotes:</strong> $14,000&ndash;$19,000 on a serviced lot, or $17,000&ndash;$24,000 built off-grid &mdash; cheaper land, more infrastructure.</li>
</ul>"""),
  ("Its own municipality since 2016",
   """<p>Puerto Morelos separated from Benito Ju&aacute;rez in 2016 and now issues its own land use, construction licences, alignments and occupancy approvals. Three practical consequences for a budget and a programme:</p>
<ul>
<li><strong>File here, not in Canc&uacute;n.</strong> Guidance based on Benito Ju&aacute;rez practice is out of date, and so is a neighbour's experience from before 2016.</li>
<li><strong>Verify the lot's numbers currently.</strong> The municipality's planning instruments are relatively young and have been updated, so confirm density, height and permitted use for the exact lot rather than assuming from an older document.</li>
<li><strong>A small administration is a direct one.</strong> The officials reviewing your file are accessible, which makes a complete, well-prepared submission unusually valuable &mdash; and makes an incomplete one unusually slow.</li>
</ul>
<p>State environmental review (SEMA), federal jurisdiction where it applies, CONAGUA for water and ZOFEMAT on the beach side all sit on top as elsewhere.</p>"""),
  ("What the reef and the wetlands add to the spec",
   """<p>Puerto Morelos has the corridor's most explicit environmental geography: a national park protecting the reef offshore, protected mangrove and wetland behind the town, and cenote-riddled karst inland. Each is a budget item rather than a slogan.</p>
<ul>
<li><strong>Discharge quality is the file's centre.</strong> Treatment before infiltration, properly sized, with pool backwash routed separately &mdash; $90,000&ndash;$350,000 MXN depending on occupancy. What infiltrates here reaches the aquifer and then the reef, and the review examines it closely.</li>
<li><strong>Mangrove is not negotiable.</strong> On a wetland-adjacent lot the protected vegetation boundary has to be established before a footprint is drawn &mdash; and some lots for sale have far less buildable area than their title area suggests. Have this checked before purchase.</li>
<li><strong>Cenote setbacks</strong> apply inland, with restrictions on what may infiltrate nearby.</li>
<li><strong>Finished floor level</strong> on low-lying land near the wetlands or the shore has to be set with flooding and surge in mind. It is a design-stage decision and cannot be corrected later.</li>
<li><strong>On the Ruta de los Cenotes,</strong> budget the access road ($40,000&ndash;$300,000) and either a CFE extension (quote it before you buy &mdash; $150,000 to well over $900,000) or a designed off-grid system with solar, storage, a treated well and rainwater harvesting.</li>
</ul>
<p>A 150 m&sup2; house takes about <strong>7&ndash;10 months</strong> from licence to handover. For the full permitting and site picture, see our <a href="/blog/puerto-morelos-construction-guide.html">Puerto Morelos construction guide</a>.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build a house in Puerto Morelos?",
   "About $2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD) turnkey for a 150 m&sup2; standard-finish home on a town or inland lot &mdash; roughly $17,000&ndash;$21,000 MXN/m&sup2;, essentially level with Playa del Carmen. Beachfront runs $26,000&ndash;$38,000+ and Ruta de los Cenotes lots $14,000&ndash;$24,000 depending on services."),
  ("Which municipality issues permits in Puerto Morelos?",
   "Puerto Morelos itself &mdash; it separated from Benito Ju&aacute;rez (Canc&uacute;n) in 2016. Any guidance based on Canc&uacute;n practice is out of date, and because the planning instruments are relatively young, the density, height and permitted use should be verified currently for the exact lot."),
  ("Can I build on a lot next to the mangroves?",
   "Not in the protected vegetation itself, and the boundary has to be established before a footprint is drawn. Some lots offered for sale have substantially less buildable area than their title area implies, so have this verified before purchase rather than after."),
  ("What does the reef national park mean for my build?",
   "It makes discharge quality the central technical question in the environmental file. Treatment before infiltration sized to occupancy, with pool backwash routed separately, costs $90,000&ndash;$350,000 MXN &mdash; and because the karst carries whatever infiltrates toward the aquifer and the reef, it is examined closely."),
  ("Is building on the Ruta de los Cenotes cheaper?",
   "The land is, and construction runs $14,000&ndash;$19,000 MXN/m&sup2; on a serviced lot. But many parcels have no CFE service or municipal water, so budget either a line extension &mdash; quote it before buying, it ranges from $150,000 to over $900,000 &mdash; or a designed off-grid system, plus $40,000&ndash;$300,000 for access road works."),
 ],
}

Z[("en","playacar")] = {
 "title": "Cost to Build a House in Playacar 2026: Teardown Economics",
 "desc": "Playacar is built out, so most projects are rebuild or remodel. 2026 per-m² bands, demolition and survey costs, the design committee, and Phase I vs Phase II.",
 "lead": "A 150 m&sup2; home in <strong>Playacar</strong> costs roughly <strong>$3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD)</strong> turnkey in 2026, about 25% above baseline Playa del Carmen. But Playacar is effectively built out, so the real question for most buyers is not what a new house costs &mdash; it is whether to remodel the one on the lot or take it down.",
 "sections": [
  ("Remodel or rebuild: the arithmetic",
   """<p>Almost every Playacar project is a rebuild, a substantial remodel, or construction on one of the few remaining lots. The decision between the first two should be made after a survey, not from a walk-through, because houses of this age on this coast carry a predictable defect: chloride-induced reinforcement corrosion at slab edges, balconies, columns and parapets.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Item</th><th>MXN</th></tr></thead><tbody>
<tr><td>Condition survey with opening-up of representative areas</td><td>$40,000&ndash;$150,000</td></tr>
<tr><td>Demolition and debris removal, typical house</td><td>$180,000&ndash;$600,000</td></tr>
<tr><td>Structural concrete repair programme, if retaining</td><td>Priced after survey &mdash; can exceed demolition</td></tr>
<tr><td>Full remodel, premium specification</td><td>$14,000&ndash;$26,000 MXN/m&sup2;</td></tr>
<tr><td>New build, premium</td><td>$24,000&ndash;$30,000 MXN/m&sup2;</td></tr>
<tr><td>New build, luxury</td><td>$30,000&ndash;$42,000 MXN/m&sup2;</td></tr>
</tbody></table></div>
<p>The honest threshold: once structural repair approaches roughly 25&ndash;30% of a rebuild's cost, you are paying new-build money for an old building's ceiling heights, orientation and plan. In Playacar the counter-argument is real though &mdash; the lots are not replaceable, mature canopy is protected and valuable, and a sound 1990s house with generous ceilings in Phase II may be worth keeping.</p>"""),
  ("Turnkey cost by home size",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Home size</th><th>Turnkey (MXN)</th><th>Turnkey (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.10M&ndash;$2.60M</td><td>$117k&ndash;$144k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.15M&ndash;$3.90M</td><td>$175k&ndash;$217k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.20M&ndash;$5.20M</td><td>$233k&ndash;$289k</td></tr>
<tr><td>250 m&sup2;</td><td>$5.25M&ndash;$6.50M</td><td>$292k&ndash;$361k</td></tr>
</tbody></table></div>
<p class="text-muted small">Reference: $21,000&ndash;$26,000 MXN/m&sup2; standard-to-premium finish. USD/MXN &asymp; 18. Excludes land, pool and furniture.</p>
<p>The 25% premium over baseline Playa del Carmen is restricted access along narrow streets, registered workers and limited working hours, the design committee process, tree protection, marine-grade specification and the finish level the market there expects. On a beachfront Playacar lot, add the federal maritime zone question and impact-rated glazing on the sea elevation, and expect $42,000&ndash;$60,000+ MXN/m&sup2;.</p>"""),
  ("The committee, the trees, and Phase I vs Phase II",
   """<p><strong>The architectural review is real</strong> and it is where Playacar programmes slip. Expect scrutiny of height, massing and setbacks beyond the municipal minimums, roof form and materials, facade treatment and colour, boundary walls and fences, and above all tree removal &mdash; mature canopy is part of what the community protects and every removal has to be justified. Submit at concept stage with the tree survey in hand, and budget at least one review cycle in the programme plus a construction bond.</p>
<p><strong>Phase I and Phase II are different places.</strong> Phase I sits closer to town and the ferry: denser, smaller lots, real walkability to 5th Avenue, and narrow-street construction access that adds cost. Phase II is larger and quieter around the golf course, with bigger lots, mature vegetation and more space for a substantial villa &mdash; and golf frontage brings its own glazing question, because errant golf balls are a specification issue for windows and skylights.</p>
<p>Permits run through the municipality of <strong>Solidaridad</strong>, the same route as the rest of Playa del Carmen, with the community's review sitting first in practice. Construction takes about <strong>7&ndash;10 months</strong> for a 150 m&sup2; house, plus demolition where applicable. For the community process in detail, see our <a href="/blog/luxury-villa-construction-playacar.html">Playacar villa construction guide</a>.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build in Playacar?",
   "About $3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD) turnkey for a 150 m&sup2; home &mdash; roughly $21,000&ndash;$26,000 MXN/m&sup2;, some 25% above baseline Playa del Carmen. Luxury specification runs $30,000&ndash;$42,000 and beachfront lots $42,000&ndash;$60,000+."),
  ("Should I remodel the existing house or tear it down?",
   "Survey first, with opening-up of representative areas at $40,000&ndash;$150,000 MXN, because houses of this age here commonly carry chloride-induced reinforcement corrosion. Once structural repair approaches 25&ndash;30% of a rebuild's cost, rebuilding is usually the better decision &mdash; demolition and debris removal runs $180,000&ndash;$600,000."),
  ("What does the Playacar design committee control?",
   "Height, massing and setbacks beyond municipal minimums, roof form and materials, facade treatment and colour, boundary walls and fences, and tree removal &mdash; every tree has to be justified. It also sets construction rules: registered workers, restricted hours, delivery and storage limits, and usually a bond."),
  ("What is the difference between Phase I and Phase II for building?",
   "Phase I has smaller, denser lots with narrow-street construction access that adds cost, and real walkability to 5th Avenue. Phase II has larger lots around the golf course with mature vegetation and room for a substantial villa &mdash; and golf frontage makes window and skylight specification a practical issue."),
  ("Why is Playacar 25% above the rest of Playa del Carmen?",
   "Restricted access along narrow streets, registered workers and limited working hours, the design committee process, tree protection during construction, marine-grade specification, and the finish level the local market expects. Each is a real line in the estimate rather than a premium for the address."),
 ],
}

Z[("en","mayakoba")] = {
 "title": "Cost to Build a House in Mayakoba 2026: The Corridor's Ceiling",
 "desc": "Mayakoba is the most expensive place to build in the Riviera Maya. The 2026 per-m² bands, what the resort-grade specification actually includes, and why.",
 "lead": "A 150 m&sup2; home in <strong>Mayakoba</strong> costs roughly <strong>$3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD)</strong> turnkey in 2026 &mdash; the highest band in the corridor, around 42% above baseline Playa del Carmen. Very little is built at that lower end, though: what is actually constructed here sits well above it, and this page explains why.",
 "sections": [
  ("Turnkey cost by home size, and the realistic number",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Home size</th><th>Turnkey (MXN)</th><th>Turnkey (USD)</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.60M&ndash;$4.50M</td><td>$200k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$6M&ndash;$7.50M</td><td>$333k&ndash;$417k</td></tr>
<tr><td>350 m&sup2;</td><td>$8.40M&ndash;$10.50M</td><td>$467k&ndash;$583k</td></tr>
<tr><td>500 m&sup2;</td><td>$12M&ndash;$15M</td><td>$667k&ndash;$833k</td></tr>
</tbody></table></div>
<p class="text-muted small">Reference: $24,000&ndash;$30,000 MXN/m&sup2; standard-to-premium finish. USD/MXN &asymp; 18. Excludes land, pool and furniture.</p>
<p>Those figures are the entry band. Houses actually built inside the Mayakoba master plan are typically 300&ndash;600 m&sup2; at signature specification, which puts real-world numbers in the <strong>$35,000&ndash;$55,000 MXN/m&sup2;</strong> range once architect-led design, imported fittings, full automation, a designed pool and mature landscaping are counted. Anyone budgeting a Mayakoba villa from the $24,000 figure is budgeting a house that would not pass the design review.</p>"""),
  ("What the premium is actually buying",
   """<p>The 42% gap over baseline Playa del Carmen is not one thing. Broken down:</p>
<ul>
<li><strong>Design control.</strong> A master plan built around resort operations reviews architecture, materials, colour, landscape and lighting to a standard set by the hotels next door. Submissions are detailed, review cycles are real, and value-engineering the facade is not available to you.</li>
<li><strong>Finish expectation.</strong> The comparables here are branded residences. Joinery, stone, glazing and fittings are specified against that, and the labour to install them precisely costs more than the materials.</li>
<li><strong>Site discipline.</strong> Construction happens inside a live luxury resort environment: controlled access, registered workers, restricted hours, screened hoardings, noise limits, cleaning obligations and a bond. Every one of those is hours on the programme.</li>
<li><strong>Environmental setting.</strong> The master plan is built around lagoons, canals and mangrove. Retained vegetation, setbacks, drainage and discharge are managed at the community level as well as by the authorities, and the landscape you cannot remove is part of what you are paying for.</li>
<li><strong>Marine and humidity specification</strong> throughout &mdash; 316 stainless, anodised or marine-coated aluminium, generous concrete cover, ventilated joinery &mdash; because the water is close on more than one side.</li>
<li><strong>Scarcity.</strong> Few residential lots, and each project is effectively bespoke. There is no repetition to spread design and management cost across.</li>
</ul>"""),
  ("Programme, permits and what else to budget",
   """<p>Permits run through the municipality of <strong>Solidaridad</strong> &mdash; land use, construction licence, alignment and a Director Responsable de Obra &mdash; with the community's own architectural review in front of it and, given the setting, environmental review that takes the lagoon and mangrove seriously. Plan the community submission at concept stage: a design produced in full and then sent for review is how Mayakoba projects lose a quarter.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Beyond the build</th><th>MXN</th></tr></thead><tbody>
<tr><td>Architect-led design and engineering at this level</td><td>10&ndash;15% of construction</td></tr>
<tr><td>Community submission, review cycles and construction bond</td><td>$150,000&ndash;$600,000</td></tr>
<tr><td>Designed pool with plant</td><td>$900,000&ndash;$3,500,000</td></tr>
<tr><td>Mature landscaping and irrigation</td><td>$400,000&ndash;$2,000,000</td></tr>
<tr><td>FF&amp;E for a villa of this class</td><td>$1,500,000&ndash;$6,000,000</td></tr>
<tr><td>HOA / community fee</td><td>Ongoing &mdash; verify per lot</td></tr>
</tbody></table></div>
<p>Construction runs about <strong>10&ndash;16 months</strong> for a villa at this specification &mdash; longer than the corridor norm, because restricted hours, review cycles and finish precision all take time that a suburban site does not. Contract fixed price with a line-item budget and milestone payments against verified progress, and treat the design review as a partner in the first meeting rather than an obstacle at the end.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build a house in Mayakoba?",
   "The entry band is $24,000&ndash;$30,000 MXN/m&sup2;, so about $3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD) for 150 m&sup2;. Realistically, houses actually built inside the master plan are 300&ndash;600 m&sup2; at $35,000&ndash;$55,000 MXN/m&sup2; once architect-led design, imported fittings, automation, pool and mature landscaping are counted."),
  ("Why is Mayakoba the most expensive place to build in the corridor?",
   "Design control set against resort standards, a finish expectation benchmarked on branded residences, construction discipline inside a live luxury environment with restricted hours and registered access, environmental management around the lagoons and mangrove, full marine specification, and scarcity &mdash; few lots and no repetition to spread design cost across."),
  ("What should I budget beyond the construction cost?",
   "Architect-led design and engineering at 10&ndash;15% of construction, community submission and bond at $150,000&ndash;$600,000, a designed pool at $900,000&ndash;$3,500,000, mature landscaping at $400,000&ndash;$2,000,000, FF&amp;E at $1,500,000&ndash;$6,000,000, and the ongoing community fee."),
  ("How long does a Mayakoba villa take to build?",
   "About 10&ndash;16 months for a villa at this specification, longer than the corridor norm. Restricted working hours, community review cycles and the precision the finish level demands all consume time that a suburban site does not."),
  ("Who approves the design?",
   "Both the municipality of Solidaridad, for land use, licence, alignment and the DRO, and the community's own architectural review, which in practice comes first and examines architecture, materials, colour, landscape and lighting. Submit at concept stage &mdash; finishing a design and then sending it for review is how projects here lose months."),
 ],
}

Z[("en","corasol")] = {
 "title": "Cost to Build a House in Corasol 2026: Inside a Live Master Plan",
 "desc": "Corasol build costs for 2026 and what building inside a developing master plan means: phased infrastructure, design review, golf frontage and access rules.",
 "lead": "A 150 m&sup2; home in <strong>Corasol</strong> costs roughly <strong>$3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD)</strong> turnkey in 2026, about 30% above baseline Playa del Carmen. Corasol is also where our own office sits, so this page is written from a fairly short walk away.",
 "sections": [
  ("Turnkey cost by home size",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Home size</th><th>Turnkey (MXN)</th><th>Turnkey (USD)</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.30M&ndash;$4.12M</td><td>$183k&ndash;$229k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.40M&ndash;$5.50M</td><td>$244k&ndash;$306k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.60M&ndash;$8.25M</td><td>$367k&ndash;$458k</td></tr>
<tr><td>450 m&sup2;</td><td>$9.90M&ndash;$12.38M</td><td>$550k&ndash;$688k</td></tr>
</tbody></table></div>
<p class="text-muted small">Reference: $22,000&ndash;$27,500 MXN/m&sup2; standard-to-premium finish. USD/MXN &asymp; 18. Excludes land, pool and furniture.</p>
<p>Most of what is built here is larger than 150 m&sup2; &mdash; the lots and the market push toward 250&ndash;450 m&sup2; villas with a pool, a roof terrace and a designed garden. Budget the whole package rather than the per-m&sup2; number alone: on a 300 m&sup2; villa, the pool, landscaping, furniture and design fees together commonly add 35&ndash;50% on top of the construction figure.</p>"""),
  ("Building inside a community that is still being built",
   """<p>This is the practical difference between Corasol and an established address like Playacar. The master plan is still developing, which cuts both ways for a homeowner:</p>
<ul>
<li><strong>Infrastructure arrives in phases.</strong> Confirm for your specific lot what is actually in the ground at the boundary today &mdash; electricity capacity, water, drainage, road surface &mdash; and what is programmed rather than promised. The gap between "the community will have" and "the lot has" is where budgets move.</li>
<li><strong>You will have construction neighbours.</strong> Other houses and community works will be under way around you for years. That means noise and traffic during your own occupancy, and it also means shared access constraints during your build.</li>
<li><strong>Design review is active and evolving.</strong> Expect the committee to examine height, massing, materials, colour, boundary treatment and landscape, with the intention of protecting a coherent look across a community that is not finished yet. Submit at concept stage.</li>
<li><strong>Access and site rules.</strong> Registered workers, controlled entry, defined delivery hours, material storage limits on the lot, street cleaning obligations and a construction bond. Budget $80,000&ndash;$300,000 MXN for submission, bond and access management.</li>
<li><strong>Golf frontage</strong> on the relevant lots brings a glazing and skylight specification question &mdash; errant balls are a real and quotable risk &mdash; plus an irrigation and drainage interface with the course.</li>
</ul>"""),
  ("Site conditions, permits and programme",
   """<p>Corasol sits in the municipality of <strong>Solidaridad</strong>, so the permit route is the familiar one: land-use certificate, alignment, construction licence and a Director Responsable de Obra, with the community's architectural review sitting in front of it in practice. Environmental requirements apply to the lot as elsewhere on this coast, and the karst underneath demands a soil study with probes across the actual footprint &mdash; good shallow bearing and a cavity two metres away are both normal here.</p>
<p>Three specification notes for this particular community:</p>
<ul>
<li><strong>Marine specification still applies.</strong> Corasol is close enough to the sea that 316 stainless fixings, anodised or marine-coated aluminium and generous concrete cover on exposed elements are the right call, not an upgrade.</li>
<li><strong>Design the roof as a terrace from the start</strong> if the height limit allows it. On lots with a view over the golf course or toward the sea it is the highest-value square metre in the house, and retrofitting a usable roof costs several times what including it does.</li>
<li><strong>Plan the plant properly:</strong> cistern, pressure system, water treatment for the local hardness, pool equipment and AC positions, all accessible for service. In a villa of this class those are not afterthoughts.</li>
</ul>
<p>Construction takes about <strong>8&ndash;12 months</strong> for a 250&ndash;300 m&sup2; villa, and rather longer if the design review runs more than one cycle. Contract fixed-price with a line-item budget and milestone payments against verified progress &mdash; and if you are buying the lot now and building later, get the utilities position at the boundary confirmed in writing before you close.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build a house in Corasol?",
   "About $3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD) turnkey for 150 m&sup2; &mdash; roughly $22,000&ndash;$27,500 MXN/m&sup2;, some 30% above baseline Playa del Carmen. Most houses here are 250&ndash;450 m&sup2;, where pool, landscaping, furniture and design fees typically add 35&ndash;50% on top of the construction figure."),
  ("What should I check before buying a lot in Corasol?",
   "What infrastructure is actually in the ground at that lot's boundary today &mdash; electricity capacity, water, drainage, road surface &mdash; versus what is programmed. In a master plan still being built, the gap between what the community will have and what the lot has is where budgets move."),
  ("Does the design committee add cost and time?",
   "Yes on both. Budget $80,000&ndash;$300,000 MXN for submission, construction bond and access management, and plan at least one review cycle into the programme. Registered workers, controlled entry, delivery hours, storage limits and street-cleaning obligations all sit alongside it."),
  ("What does golf frontage change?",
   "Window and skylight specification, because errant golf balls are a real and quotable risk, plus an irrigation and drainage interface with the course. It is worth resolving at design stage rather than replacing glazing afterwards."),
  ("How long does a Corasol villa take to build?",
   "About 8&ndash;12 months for a 250&ndash;300 m&sup2; villa from licence to handover, and longer if the design review runs to more than one cycle. Restricted working hours and controlled access inside the community push the programme toward the longer end."),
 ],
}

Z[("en","aldea-zama-tulum")] = {
 "title": "Cost to Build a House in Aldea Zamá 2026: The Calendar Is Cost",
 "desc": "Aldea Zamá build costs for 2026 plus the item nobody budgets: Tulum's permit timeline. Height limits, power reliability and what the urbanised master plan gives you.",
 "lead": "A 150 m&sup2; home in <strong>Aldea Zam&aacute;</strong> costs roughly <strong>$3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD)</strong> turnkey in 2026, about 20% above baseline Playa del Carmen. The construction number is straightforward. The number people fail to budget in Tulum is time.",
 "sections": [
  ("Turnkey cost by home size",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Home size</th><th>Turnkey (MXN)</th><th>Turnkey (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.05M&ndash;$2.50M</td><td>$114k&ndash;$139k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.08M&ndash;$3.75M</td><td>$171k&ndash;$208k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.10M&ndash;$5M</td><td>$228k&ndash;$278k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.15M&ndash;$7.50M</td><td>$342k&ndash;$417k</td></tr>
</tbody></table></div>
<p class="text-muted small">Reference: $20,500&ndash;$25,000 MXN/m&sup2; standard-to-premium finish. USD/MXN &asymp; 18. Excludes land, pool and furniture.</p>
<p>Aldea Zam&aacute; prices above the Tulum Regiones and La Veleta for a straightforward reason: it is an urbanised master plan with services in the ground, paved access and a defined character, in walking or short-cycling distance of the beach road. You are paying for infrastructure that exists rather than infrastructure you have to build.</p>"""),
  ("What the permit calendar actually costs",
   """<p>Tulum's review is the most environmentally demanding in the corridor, and on a lot with vegetation the file is the critical path. Realistic durations, from purchase to breaking ground:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Stage</th><th>Duration</th></tr></thead><tbody>
<tr><td>Land-use certificate and alignment</td><td>2&ndash;8 weeks</td></tr>
<tr><td>Soil study (in parallel)</td><td>2&ndash;5 weeks</td></tr>
<tr><td>Environmental file</td><td>3&ndash;8 months, depending on vegetation</td></tr>
<tr><td>Technical project (in parallel)</td><td>6&ndash;14 weeks</td></tr>
<tr><td>Licence review with a complete file</td><td>4&ndash;12 weeks</td></tr>
<tr><td><strong>Total before construction starts</strong></td><td><strong>5&ndash;12 months</strong></td></tr>
</tbody></table></div>
<p>Those months are a real line: land carried, capital committed, nothing earning. Two ways to shorten them. First, start the environmental file and the soil study while the architecture is still in concept &mdash; neither needs final drawings, and both constrain the design anyway. Second, when comparing lots, weight an existing environmental authorisation heavily: it can be worth six months and a six-figure sum.</p>"""),
  ("Height, power and what gets built here",
   """<p>Three Aldea Zam&aacute; specifics that shape the brief:</p>
<ul>
<li><strong>Height limits are restrained</strong> and enforced. Tulum's rules are deliberately tighter than Playa del Carmen's, so verify the exact limit for your lot before designing a rooftop &mdash; on many lots the roof terrace is the difference between a good project and a compromised one, and it depends on that single number.</li>
<li><strong>Power reliability is worse than Playa del Carmen's.</strong> Budget whole-house surge protection as standard, and for a rental property a battery system covering essentials &mdash; internet, pool controller, some lighting and a fan &mdash; at $140,000&ndash;$330,000 MXN. Solar makes unusually good sense here too, particularly once a pool pump and several air conditioners push consumption onto the high-consumption CFE tariff.</li>
<li><strong>The market is condo-dominant,</strong> which is precisely the argument for building a house. A standalone house cannot have its short-term rental permission voted away by an assembly, carries no HOA fee taking a slice of gross, and can be designed for yield &mdash; en-suite bedrooms, a lock-off casita, a rooftop, a pool positioned for the photograph.</li>
</ul>
<p>Technically, the usual Tulum items apply: treatment before infiltration sized to occupancy ($90,000&ndash;$250,000 MXN), water treatment for the local hardness, termite and humidity detailing, and a soil study because the karst here is cenote-riddled. Construction runs about <strong>7&ndash;11 months</strong> for a 150&ndash;200 m&sup2; house. Contract on a fixed price with a line-item budget, and put the permit calendar in the plan rather than discovering it.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build a house in Aldea Zamá?",
   "About $3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD) turnkey for a 150 m&sup2; standard-to-premium home &mdash; roughly $20,500&ndash;$25,000 MXN/m&sup2;, some 20% above baseline Playa del Carmen. Land, pool and furniture are separate."),
  ("Why does Aldea Zamá cost more than the Tulum Regiones?",
   "Because the infrastructure exists. It is an urbanised master plan with services in the ground, paved access and a defined character within reach of the beach road &mdash; so you are not paying to build the utilities, the access and the setting yourself, which is what a cheaper Regi&oacute;n lot actually involves."),
  ("How long before I can start construction in Tulum?",
   "Five to twelve months from purchase, realistically: two to eight weeks for the land-use certificate and alignment, three to eight months for the environmental file on a vegetated lot, and four to twelve weeks for the licence once the file is complete. Start the environmental file and soil study while the architecture is still in concept."),
  ("Can I build a rooftop terrace in Aldea Zamá?",
   "It depends on the height limit for your specific lot, and Tulum's limits are deliberately restrained and enforced. Verify the number before designing, because on many lots the roof terrace is the difference between a strong project and a compromised one."),
  ("What should I do about Tulum's power cuts?",
   "Whole-house surge protection as standard, and for a rental property a battery system covering essentials &mdash; internet, pool controller, lighting and a fan &mdash; at $140,000&ndash;$330,000 MXN. Solar also pays back quickly here, especially once a pool pump and several air conditioners push consumption onto the high-consumption CFE tariff."),
 ],
}

Z[("en","playa-del-carmen")] = {
 "title": "Cost to Build a House in Playa del Carmen 2026: Phase by Phase",
 "desc": "The corridor's benchmark price. Phase-by-phase budget for a 150 m² house, what the per-m² number includes and excludes, add-ons, and how to keep it under control.",
 "lead": "A well-built 150 m&sup2; family home in <strong>Playa del Carmen</strong> costs roughly <strong>$2.6M&ndash;$3.2M MXN ($145,000&ndash;$178,000 USD)</strong> turnkey in 2026. This is the number every other zone in the corridor is priced against, so it is worth understanding phase by phase rather than as a single figure.",
 "sections": [
  ("Phase-by-phase budget (150 m² standard home)",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Phase</th><th>% of budget</th><th>Approx. cost (MXN)</th><th>Notes</th></tr></thead><tbody>
<tr><td>Permits, DRO &amp; studies</td><td>5%</td><td>$130,000&ndash;$160,000</td><td>Licence, DRO, soil study, topography</td></tr>
<tr><td>Foundation &amp; structure</td><td>30%</td><td>$780,000&ndash;$960,000</td><td>Slab, columns, beams, slabs</td></tr>
<tr><td>Walls &amp; roof</td><td>18%</td><td>$470,000&ndash;$580,000</td><td>Block, castillos, roof slab</td></tr>
<tr><td>Installations</td><td>15%</td><td>$390,000&ndash;$480,000</td><td>Electrical, plumbing, sanitary</td></tr>
<tr><td>Finishes</td><td>25%</td><td>$650,000&ndash;$800,000</td><td>Floors, paint, chukum, carpentry</td></tr>
<tr><td>Cleanup &amp; delivery</td><td>7%</td><td>$180,000&ndash;$220,000</td><td>Final details, handover</td></tr>
</tbody></table></div>
<p class="text-muted small">Total turnkey &asymp; $2.6M&ndash;$3.2M MXN. Excludes land, pool and furniture.</p>
<p>Two things to read from that table. The structure is nearly a third of the budget and is the one phase where saving money is genuinely dangerous in a high wind-load region. And finishes at a quarter are where your specification actually lives &mdash; the same shell with different finishes can swing the total by 20% without a single drawing changing.</p>"""),
  ("What the per-m² figure does and does not include",
   """<p>The $17,000&ndash;$21,000 MXN/m&sup2; band that produces those totals covers structure, installations and standard finishes. These sit outside it and account for most budget surprises:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Item</th><th>MXN</th></tr></thead><tbody>
<tr><td>Land</td><td>Separate, and the largest variable in Playa del Carmen</td></tr>
<tr><td>Pool, 4&times;8 m with plant</td><td>$450,000&ndash;$1,200,000</td></tr>
<tr><td>Rooftop terrace build-out (structure allowed for at design)</td><td>$3,500&ndash;$9,000 per m&sup2;</td></tr>
<tr><td>Water treatment train (filter, softener, carbon, RO)</td><td>$35,000&ndash;$95,000</td></tr>
<tr><td>Air conditioning, 4&ndash;5 inverter zones</td><td>$120,000&ndash;$280,000</td></tr>
<tr><td>Solar, 5&ndash;8 kWp</td><td>$115,000&ndash;$250,000</td></tr>
<tr><td>Landscaping and irrigation</td><td>$500&ndash;$2,000 per m&sup2;</td></tr>
<tr><td>Furniture and appliances</td><td>$450,000&ndash;$1,200,000 for a family house</td></tr>
</tbody></table></div>
<p>Design, engineering, studies and permits together typically run 8&ndash;14% of construction on a custom house here &mdash; already partly reflected in the phase table above, and not a line to compress, since the errors it prevents each cost more than the whole package.</p>"""),
  ("Why this is the corridor's benchmark, and how to hold the budget",
   """<p>Playa del Carmen prices lower than the gated and premium zones for structural reasons rather than quality ones: a deep supplier base, real contractor competition, serviced urban lots, a straightforward permit route through the municipality of <strong>Solidaridad</strong>, and no federal maritime zone question on the great majority of lots. Everything else in the corridor is a multiple of this number &mdash; Puerto Morelos about level, Puerto Aventuras roughly 8% above, Akumal 12%, Aldea Zam&aacute; 20%, Playacar 25%, Corasol 30%, Mayakoba 42%.</p>
<p>Four habits that keep a Playa del Carmen budget where it started:</p>
<ul>
<li><strong>Fixed price with a line-item budget,</strong> not a per-m&sup2; handshake. A single rate applied to a number of square metres is not a budget; it is an invitation to renegotiate.</li>
<li><strong>Payments against verified physical progress,</strong> not calendar dates, with 5&ndash;10% retention released after the snag list closes.</li>
<li><strong>Written, priced change orders before work proceeds.</strong> Verbal changes are the most common route from a firm price to an open one.</li>
<li><strong>An explicit exclusions list</strong> &mdash; furniture, appliances, landscaping beyond a defined line, utility connection fees &mdash; agreed at signature so the surprises happen on paper rather than on site.</li>
</ul>
<p>A 150 m&sup2; house takes about <strong>7&ndash;10 months</strong> from licence to handover, with the permit route typically adding two to four months before that. Use the <a href="/calculator/">cost calculator</a> for a quick estimate against your own size and finish level.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build a house in Playa del Carmen in 2026?",
   "About $2.6M&ndash;$3.2M MXN ($145,000&ndash;$178,000 USD) turnkey for a 150 m&sup2; standard-finish home &mdash; roughly $17,000&ndash;$21,000 MXN/m&sup2;, excluding land, pool and furniture."),
  ("What is not included in the per-m² price?",
   "Land, the pool ($450,000&ndash;$1,200,000), a rooftop terrace build-out, water treatment, air conditioning, solar, landscaping and furniture. Those are where most budget surprises come from, so price them as their own lines from the start rather than as extras."),
  ("Which phase costs the most?",
   "Foundation and structure at about 30% of the budget, followed by finishes at 25%. The structure is also where saving money is genuinely dangerous in a high wind-load region, while finishes are where specification choices can swing the total by 20% without changing a drawing."),
  ("How does Playa del Carmen compare with the other zones?",
   "It is the benchmark. Puerto Morelos runs about level, Puerto Aventuras roughly 8% above, Akumal 12%, Aldea Zam&aacute; 20%, Playacar 25%, Corasol 30% and Mayakoba 42% &mdash; the differences coming from access restrictions, design committees, marine specification and environmental requirements rather than from build quality."),
  ("How do I stop the budget from drifting?",
   "A fixed price with a line-item budget rather than a per-m&sup2; rate, payments tied to verified physical progress with 5&ndash;10% retention released after the snag list closes, written and priced change orders before work proceeds, and an explicit exclusions list agreed at signature."),
 ],
}

if __name__ == "__main__":
    keys = ([tuple(a.split(":", 1)) for a in sys.argv[1:]] or sorted(Z))
    for lang, zone in keys:
        if (lang, zone) not in Z:
            print(f"  ! no content for {lang}:{zone}"); continue
        w, rel = rewrite(lang, zone)
        print(f"  {w:5d} body words  {rel}")
