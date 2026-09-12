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

Z[("es","cancun")] = {
 "title": "Cuánto Cuesta Construir una Casa en Cancún 2026",
 "desc": "Construir en Cancún cuesta menos que en el resto del corredor. Rangos por m² 2026, de dónde viene ese descuento y dónde deja de ser una ganga.",
 "lead": "Construir una casa familiar de 150 m&sup2; en <strong>Canc&uacute;n</strong> cuesta aproximadamente <strong>$2.48M&ndash;$3M MXN ($138k&ndash;$167k USD)</strong> llave en mano en 2026 &mdash; la cifra m&aacute;s baja del corredor y alrededor de 4% por debajo de Playa del Carmen con el mismo acabado. Aqu&iacute; explicamos de d&oacute;nde sale ese descuento y d&oacute;nde deja de serlo.",
 "sections": [
  ("Por qué Cancún cotiza por debajo del resto del corredor",
   """<p>Canc&uacute;n es el &uacute;nico punto del corredor donde la escala juega a favor de quien construye una casa: la mayor bolsa de mano de obra de la regi&oacute;n, la mayor concentraci&oacute;n de proveedores y talleres, y suficientes constructoras compitiendo como para que el precio se ponga realmente a prueba. Todo lo que est&aacute; al sur de Puerto Morelos trae alguna parte del trabajo desde aqu&iacute;.</p>
<ul>
<li><strong>Materiales en origen.</strong> Block, cemento, acero, agregados, aluminio, loseta y muebles de ba&ntilde;o se compran localmente sin flete del corredor &mdash; en una casa de 150 m&sup2; eso solo vale varios puntos porcentuales.</li>
<li><strong>Oficios sin movilizaci&oacute;n.</strong> El trabajo especializado que a Tulum o Akumal hay que programarlo y trasladarlo, aqu&iacute; es una llamada local.</li>
<li><strong>Lotes residenciales tierra adentro.</strong> La mayor parte de la vivienda en Canc&uacute;n se construye en fraccionamientos cerrados interiores: sin zona federal mar&iacute;timo terrestre, sin concesi&oacute;n ZOFEMAT, sin calendario de anidaci&oacute;n de tortuga y con un expediente ambiental m&aacute;s ligero que un lote costero equivalente.</li>
</ul>
<p>Los permisos se tramitan en el municipio de <strong>Benito Ju&aacute;rez</strong> &mdash; uso de suelo, licencia de construcci&oacute;n, alineamiento y Director Responsable de Obra &mdash; y para un lote residencial urbanizado es de los procesos m&aacute;s predecibles del estado.</p>"""),
  ("Costo llave en mano por tamaño de casa",
   """<p>Rangos con acabado est&aacute;ndar para Canc&uacute;n &mdash; estructura, instalaciones y acabados; sin terreno, alberca ni mobiliario:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tama&ntilde;o</th><th>Llave en mano (MXN)</th><th>Llave en mano (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.65M&ndash;$2M</td><td>$92k&ndash;$111k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.48M&ndash;$3M</td><td>$138k&ndash;$167k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.30M&ndash;$4M</td><td>$183k&ndash;$222k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.13M&ndash;$5M</td><td>$229k&ndash;$278k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referencia: $16,500&ndash;$20,000 MXN/m&sup2; acabado est&aacute;ndar. USD/MXN &asymp; 18. Sin terreno, alberca ni mobiliario.</p>
<p>Esos rangos aplican al Canc&uacute;n residencial interior. Un lote en la Zona Hotelera, en Isla Dorada o con frente al mar o a la laguna es otro edificio: especificaci&oacute;n marina completa, preguntas de zona federal y un nivel de acabado que el sitio exige. Ah&iacute; el rango realista es $26,000&ndash;$40,000 MXN/m&sup2;.</p>"""),
  ("Dónde el ahorro se convierte en riesgo",
   """<p>Un mercado grande y competido produce precios bajos y una enorme variaci&oacute;n de calidad. En Canc&uacute;n el problema no es la obra cara: es la barata.</p>
<ul>
<li><strong>Cotizaciones por debajo de $14,000 MXN/m&sup2;</strong> est&aacute;n recortando algo estructural &mdash; normalmente densidad de armado, calidad del concreto o la instalaci&oacute;n el&eacute;ctrica. En una zona de vientos altos, el acero no es el lugar para ahorrar.</li>
<li><strong>Sin mec&aacute;nica de suelos.</strong> El karst puede dar excelente capacidad de carga somera y una cavidad dos metros al lado. El estudio sobre la huella real cuesta $25,000&ndash;$60,000 y es la reducci&oacute;n de riesgo m&aacute;s barata del proyecto.</li>
<li><strong>Reglas del fraccionamiento.</strong> Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua o Palmaris operan comit&eacute;s de dise&ntilde;o con sus propios l&iacute;mites de altura, remetimientos, materiales y colores, adem&aacute;s de registro de trabajadores, horarios restringidos y fianza de obra. Pres&eacute;ntelo en etapa de anteproyecto.</li>
<li><strong>Tr&aacute;fico y ventanas de entrega.</strong> Canc&uacute;n es el &uacute;nico lugar del corredor donde el tr&aacute;fico urbano es un tema de programa: las entregas a fraccionamientos interiores requieren horario, y los reglamentos de horario lo complican m&aacute;s.</li>
<li><strong>La sal tambi&eacute;n llega tierra adentro.</strong> Incluso a varios kil&oacute;metros del mar, herrajes, barandales y serpentines de condensadores duran mucho m&aacute;s en acero inoxidable 316 y recubrimientos de grado marino.</li>
</ul>
<p>Una casa de 150 m&sup2; toma unos <strong>7&ndash;10 meses</strong> desde la licencia hasta la entrega, y la profundidad de proveedores de Canc&uacute;n reduce las esperas de material que alargan obras m&aacute;s al sur. Exija contrato a precio fijo con presupuesto desglosado y pagos por avance verificado: en un mercado de este tama&ntilde;o, ese documento es lo que separa a los buenos constructores de los baratos.</p>"""),
 ],
 "faq": [
  ("¿Cuánto cuesta construir una casa en Cancún en 2026?",
   "Alrededor de $2.48M&ndash;$3M MXN ($138k&ndash;$167k USD) llave en mano para una casa de 150 m&sup2; con acabado est&aacute;ndar en lote residencial interior, sin terreno, alberca ni mobiliario &mdash; unos $16,500&ndash;$20,000 MXN/m&sup2;."),
  ("¿Por qué Cancún es más barato que Playa del Carmen o Tulum?",
   "Por escala: la mayor bolsa de mano de obra del corredor, la mayor densidad de proveedores y talleres, y suficiente competencia entre constructoras para que el precio se pruebe. Adem&aacute;s, la vivienda se construye en lotes interiores, lo que evita la zona federal mar&iacute;timo terrestre, las reglas de anidaci&oacute;n de tortuga y el expediente ambiental m&aacute;s pesado de un lote costero."),
  ("¿Ese precio aplica en la Zona Hotelera?",
   "No. Zona Hotelera, Isla Dorada o cualquier frente de mar o laguna implica especificaci&oacute;n marina completa, preguntas de zona federal y mayor nivel de acabado: presupuestar $26,000&ndash;$40,000 MXN/m&sup2; en lugar del rango interior."),
  ("¿Cuál es el precio más bajo razonable de un constructor en Cancún?",
   "Tome como se&ntilde;al de alerta cualquier cifra por debajo de unos $14,000 MXN/m&sup2;. A ese precio se est&aacute; reduciendo algo estructural &mdash; densidad de armado, calidad del concreto o la instalaci&oacute;n el&eacute;ctrica &mdash; y en una zona de vientos altos esos son los ahorros equivocados."),
  ("¿Los fraccionamientos cerrados encarecen la obra?",
   "S&iacute;. Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua y Palmaris tienen comit&eacute;s de dise&ntilde;o con l&iacute;mites propios de altura, remetimientos, materiales y color, adem&aacute;s de registro de trabajadores, horarios restringidos y fianza. Presupueste el ciclo de revisi&oacute;n en el programa, no solo las cuotas."),
 ],
}

Z[("es","puerto-aventuras")] = {
 "title": "Cuánto Cuesta Construir una Casa en Puerto Aventuras 2026",
 "desc": "Costos llave en mano en Puerto Aventuras más las partidas de la comunidad marina que casi nadie presupuesta: cuota HOA, muelle, muro de canal y comité.",
 "lead": "Una casa de 150 m&sup2; en <strong>Puerto Aventuras</strong> cuesta aproximadamente <strong>$2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD)</strong> llave en mano en 2026, cerca de 8% por encima de Playa del Carmen. La obra es la parte predecible; las partidas de abajo son donde se descuadran los presupuestos en una comunidad marina.",
 "sections": [
  ("Costo llave en mano por tamaño de casa",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tama&ntilde;o</th><th>Llave en mano (MXN)</th><th>Llave en mano (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.85M&ndash;$2.25M</td><td>$103k&ndash;$125k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.77M&ndash;$3.38M</td><td>$154k&ndash;$188k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.70M&ndash;$4.50M</td><td>$206k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.63M&ndash;$5.63M</td><td>$257k&ndash;$313k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referencia: $18,500&ndash;$22,500 MXN/m&sup2; acabado est&aacute;ndar. USD/MXN &asymp; 18. Sin terreno, alberca ni mobiliario.</p>
<p>El 8% sobre Playa del Carmen son cuatro cosas concretas, no un recargo por la direcci&oacute;n: acceso controlado con registro de trabajadores, horarios restringidos que alargan el programa, mayor manejo de material dentro de la comunidad y la especificaci&oacute;n de grado marino que exigen las posiciones sobre canal o cerca del mar. Cada una es una partida real.</p>"""),
  ("Las partidas que se olvidan",
   """<p>Quedan fuera del costo de obra y son las que sorprenden a quien compra por primera vez en la comunidad:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Concepto</th><th>Qué confirmar</th></tr></thead><tbody>
<tr><td><strong>Cuota de mantenimiento (HOA)</strong></td><td>La cifra vigente para ese lote, el presupuesto que la respalda y su tendencia de cinco a&ntilde;os. Los lotes sobre canal y cerca de la marina suelen pagar m&aacute;s.</td></tr>
<tr><td><strong>Muelle o amarre</strong></td><td>Si es propio, arrendado o asignado &mdash; tres figuras distintas legalmente y en reventa &mdash; y cu&aacute;nto cuesta al a&ntilde;o. Las obras de muelle se permisan aparte de la casa.</td></tr>
<tr><td><strong>Muro de canal</strong></td><td>Su estado, revisado por alguien que no le est&aacute; vendiendo la propiedad. Repararlo es un proyecto en s&iacute; mismo.</td></tr>
<tr><td><strong>Comit&eacute; de dise&ntilde;o</strong></td><td>Presentaci&oacute;n, ciclo de revisi&oacute;n y fianza de obra: presupueste $60,000&ndash;$250,000 MXN y al menos una ronda de revisi&oacute;n en el programa.</td></tr>
<tr><td><strong>Especificaci&oacute;n marina</strong></td><td>Herrajes 316, aluminio anodizado o con recubrimiento marino, mayor recubrimiento de concreto. Suma a la obra y ahorra mucho m&aacute;s en una d&eacute;cada.</td></tr>
</tbody></table></div>
<p>Los permisos se tramitan en el municipio de <strong>Solidaridad</strong> &mdash; la misma ruta que Playa del Carmen &mdash; con la revisi&oacute;n arquitect&oacute;nica de la comunidad por delante en la pr&aacute;ctica.</p>"""),
  ("Frente a canal: qué cambia técnicamente",
   """<p>El lote sobre canal es la raz&oacute;n para comprar aqu&iacute;, y cambia la ingenier&iacute;a:</p>
<ul>
<li><strong>Nivel fre&aacute;tico alto.</strong> Excavaciones, cisterna y vaso de alberca requieren abatimiento y revisi&oacute;n de flotaci&oacute;n &mdash; una alberca vaciada en el momento equivocado puede flotar.</li>
<li><strong>Aerosol salino constante</strong> desde el agua, no exposici&oacute;n estacional. Aqu&iacute; el inoxidable 316 deja de ser preferencia.</li>
<li><strong>Exposici&oacute;n a tormenta.</strong> Los lotes junto al agua reciben viento completo y, en un evento serio, marea de tormenta. El vidrio laminado o con clasificaci&oacute;n de impacto en la fachada al agua es la especificaci&oacute;n que no negociamos.</li>
<li><strong>Estructuras de borde</strong> en la l&iacute;nea de agua tienen dise&ntilde;o y autorizaci&oacute;n propios.</li>
</ul>
<p>La obra de una casa de 150 m&sup2; toma unos <strong>7&ndash;10 meses</strong> desde la licencia, y los horarios restringidos dentro de la comunidad empujan el programa al extremo largo. Contrate a precio fijo con presupuesto desglosado y pagos por avance verificado: donde el acceso es controlado y las horas limitadas, un esquema abierto es donde el calendario se desdibuja.</p>"""),
 ],
 "faq": [
  ("¿Cuánto cuesta construir una casa en Puerto Aventuras?",
   "Alrededor de $2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD) llave en mano para 150 m&sup2; con acabado est&aacute;ndar, sin terreno, alberca ni mobiliario &mdash; unos $18,500&ndash;$22,500 MXN/m&sup2;, cerca de 8% arriba de Playa del Carmen."),
  ("¿Por qué es más caro que Playa del Carmen?",
   "Por cuatro razones concretas: acceso controlado con registro de trabajadores, horarios restringidos que alargan el programa, mayor manejo de material dentro de la comunidad y la especificaci&oacute;n de grado marino que exigen los lotes sobre canal o cercanos al mar."),
  ("¿Qué costos quedan fuera del presupuesto de obra?",
   "La cuota de mantenimiento del lote, el cargo de muelle o amarre si aplica, la reparaci&oacute;n del muro de canal si est&aacute; deteriorado, y la presentaci&oacute;n al comit&eacute; con su fianza, alrededor de $60,000&ndash;$250,000 MXN. Las obras de muelle se permisan por separado."),
  ("¿Necesito aprobación de la comunidad además del municipio?",
   "S&iacute;, y en la pr&aacute;ctica la comunidad va primero. La licencia y el DRO se tramitan en Solidaridad, mientras el comit&eacute; arquitect&oacute;nico revisa altura, remetimientos, materiales, colores y bardas. Presente en anteproyecto: una ronda de revisi&oacute;n no prevista es el retraso m&aacute;s com&uacute;n aqu&iacute;."),
  ("¿Qué cambia en un lote con frente a canal?",
   "Abatimiento y revisi&oacute;n de flotaci&oacute;n para excavaciones y alberca, especificaci&oacute;n marina completa porque el aerosol salino es constante, vidrio laminado o de impacto en la fachada al agua por la exposici&oacute;n a tormenta, y autorizaci&oacute;n aparte para cualquier obra en la l&iacute;nea de agua."),
 ],
}

Z[("es","akumal")] = {
 "title": "Cuánto Cuesta Construir una Casa en Akumal 2026",
 "desc": "Costos de obra en Akumal 2026 y por qué el expediente ambiental — no los muros — define el total. Tortugas, planta de tratamiento, transporte y calendario.",
 "lead": "Una casa de 150 m&sup2; en <strong>Akumal</strong> cuesta aproximadamente <strong>$2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD)</strong> llave en mano en 2026. Pero en un lote de Akumal la construcci&oacute;n es la mitad predecible del presupuesto: el expediente ambiental, la planta de tratamiento y el calendario de permisos son lo que separa dos proyectos aparentemente iguales.",
 "sections": [
  ("Costo llave en mano por tamaño de casa",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tama&ntilde;o</th><th>Llave en mano (MXN)</th><th>Llave en mano (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.90M&ndash;$2.35M</td><td>$106k&ndash;$131k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.85M&ndash;$3.52M</td><td>$158k&ndash;$196k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.80M&ndash;$4.70M</td><td>$211k&ndash;$261k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.75M&ndash;$5.88M</td><td>$264k&ndash;$326k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referencia: $19,000&ndash;$23,500 MXN/m&sup2; acabado est&aacute;ndar. USD/MXN &asymp; 18. Sin terreno, alberca ni mobiliario.</p>
<p>Es cerca de 12% arriba de Playa del Carmen, y ese sobreprecio es transporte de todo el material por el corredor, especificaci&oacute;n de grado marino por la exposici&oacute;n salina, y una base local de oficios m&aacute;s peque&ntilde;a que obliga a movilizar cuadrillas.</p>"""),
  ("Las partidas que solo existen en Akumal",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Partida</th><th>MXN</th><th>Por qué</th></tr></thead><tbody>
<tr><td>Estudios y autorizaci&oacute;n ambiental</td><td>$80,000&ndash;$350,000</td><td>El alcance lo fija la vegetaci&oacute;n y la distancia a la costa, no el tama&ntilde;o de la casa</td></tr>
<tr><td>Planta de tratamiento + pozo de absorci&oacute;n</td><td>$120,000&ndash;$380,000</td><td>No hay drenaje municipal: tratar antes de infiltrar es el centro del expediente</td></tr>
<tr><td>Iluminaci&oacute;n compatible con anidaci&oacute;n</td><td>$30,000&ndash;$120,000</td><td>Baja, apantallada, &aacute;mbar o roja en fachadas hacia la playa</td></tr>
<tr><td>Levantamiento ZOFEMAT y revisi&oacute;n de concesi&oacute;n</td><td>$20,000&ndash;$80,000</td><td>Solo en lotes que tocan la zona federal mar&iacute;timo terrestre</td></tr>
<tr><td>Mec&aacute;nica de suelos sobre la huella</td><td>$25,000&ndash;$60,000</td><td>Karst: una cavidad puede estar a dos metros de una buena capacidad de carga</td></tr>
</tbody></table></div>
<p>Cuatro de esas cinco partidas escalan con el <em>lote</em>, no con la casa. Por eso una casa compacta en Akumal sale m&aacute;s cara por metro cuadrado que una grande, y por eso el ahorro m&aacute;s barato disponible es elegir un lote con autorizaci&oacute;n ambiental vigente y servicios ya en el l&iacute;mite del predio.</p>"""),
  ("El calendario de permisos y lo que cuesta esperar",
   """<p>Akumal pertenece al municipio de <strong>Tulum</strong>, no a Solidaridad &mdash; sorprende a muchos propietarios porque Playa del Carmen queda m&aacute;s cerca. La revisi&oacute;n de Tulum es la m&aacute;s exigente del corredor en materia ambiental, y la consecuencia pr&aacute;ctica es calendario:</p>
<ul>
<li><strong>Expediente ambiental:</strong> 4&ndash;9 meses en un lote con vegetaci&oacute;n o cercano a la costa.</li>
<li><strong>Revisi&oacute;n de licencia con expediente completo:</strong> 4&ndash;12 semanas.</li>
<li><strong>Total realista desde la compra hasta iniciar obra:</strong> 6&ndash;14 meses.</li>
</ul>
<p>Esos meses son un costo real: terreno cargado y capital comprometido sin producir. Tambi&eacute;n son la raz&oacute;n por la que un lote con autorizaci&oacute;n vigente se vende con premio &mdash; y normalmente lo vale.</p>
<p>Un dato de programaci&oacute;n propio de esta costa: la anidaci&oacute;n de tortuga corre aproximadamente de <strong>mayo a octubre</strong>, con restricciones a trabajo pesado, iluminaci&oacute;n intensa y actividad en la arena cerca de la playa. Programe las fases exteriores ruidosas fuera de esa ventana y los acabados interiores dentro de ella.</p>
<p>La obra toma unos <strong>7&ndash;10 meses</strong> para 150 m&sup2;. Contrate a precio fijo con presupuesto desglosado, y aseg&uacute;rese de que las condicionantes ambientales &mdash; supervivencia de reforestaci&oacute;n, bit&aacute;cora de la planta, cumplimiento de iluminaci&oacute;n &mdash; queden asignadas a alguien despu&eacute;s de la entrega, porque siguen vigentes toda la vida del inmueble.</p>"""),
 ],
 "faq": [
  ("¿Cuánto cuesta construir una casa en Akumal en 2026?",
   "Alrededor de $2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD) llave en mano para 150 m&sup2; con acabado est&aacute;ndar &mdash; unos $19,000&ndash;$23,500 MXN/m&sup2;, cerca de 12% arriba de Playa del Carmen. Terreno, alberca, mobiliario y las partidas ambientales van aparte."),
  ("¿Qué costos adicionales tiene un lote en Akumal?",
   "Estudios y autorizaci&oacute;n ambiental $80,000&ndash;$350,000, planta de tratamiento con pozo de absorci&oacute;n $120,000&ndash;$380,000, iluminaci&oacute;n compatible con anidaci&oacute;n $30,000&ndash;$120,000, levantamiento ZOFEMAT en lotes federales $20,000&ndash;$80,000 y mec&aacute;nica de suelos $25,000&ndash;$60,000. Casi todas escalan con el lote, no con la casa."),
  ("¿Qué municipio otorga los permisos en Akumal?",
   "Tulum, no Solidaridad, aunque Playa del Carmen quede m&aacute;s cerca. Su revisi&oacute;n ambiental es la m&aacute;s exigente del corredor, por lo que conviene planear entre 6 y 14 meses desde la compra hasta iniciar obra."),
  ("¿Las reglas de anidación afectan el programa de obra?",
   "S&iacute;. La temporada corre aproximadamente de mayo a octubre y restringe trabajo pesado, iluminaci&oacute;n intensa y actividad en la arena cerca de la playa. Programe las fases exteriores fuera de la temporada y los interiores dentro. Las reglas de iluminaci&oacute;n tambi&eacute;n aplican a la casa terminada."),
  ("¿Una casa más pequeña sale más barata por m² en Akumal?",
   "No, sale m&aacute;s cara por metro. El expediente ambiental, la mec&aacute;nica de suelos, la planta de tratamiento y la conexi&oacute;n de servicios cuestan casi lo mismo para 80 m&sup2; que para 200 m&sup2;, as&iacute; que en una casa compacta esas partidas fijas pesan mucho m&aacute;s."),
 ],
}

Z[("es","puerto-morelos")] = {
 "title": "Cuánto Cuesta Construir una Casa en Puerto Morelos 2026",
 "desc": "Puerto Morelos construye a precio de Playa del Carmen con terreno más barato. Rangos 2026, la descarga frente al parque de arrecife y la Ruta de los Cenotes.",
 "lead": "Una casa de 150 m&sup2; en <strong>Puerto Morelos</strong> cuesta aproximadamente <strong>$2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD)</strong> llave en mano en 2026 &mdash; pr&aacute;cticamente al nivel de Playa del Carmen en obra, sobre terreno por lo general m&aacute;s barato. Esa combinaci&oacute;n es lo que lo convierte en la opci&oacute;n de valor discreta del corredor.",
 "sections": [
  ("Costo llave en mano y los tres submercados",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tama&ntilde;o</th><th>Llave en mano (MXN)</th><th>Llave en mano (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.70M&ndash;$2.10M</td><td>$94k&ndash;$117k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.55M&ndash;$3.15M</td><td>$142k&ndash;$175k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.40M&ndash;$4.20M</td><td>$189k&ndash;$233k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.25M&ndash;$5.25M</td><td>$236k&ndash;$292k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referencia: $17,000&ndash;$21,000 MXN/m&sup2; acabado est&aacute;ndar. USD/MXN &asymp; 18. Sin terreno, alberca ni mobiliario.</p>
<p>Esos rangos cubren el pueblo y los lotes residenciales interiores. Los otros dos submercados se comportan distinto:</p>
<ul>
<li><strong>Frente al mar y cercano a costa:</strong> $26,000&ndash;$38,000+ MXN/m&sup2; con especificaci&oacute;n marina, preguntas de zona federal y expediente ambiental m&aacute;s pesado.</li>
<li><strong>Ruta de los Cenotes:</strong> $14,000&ndash;$19,000 en lote con servicios, o $17,000&ndash;$24,000 construyendo fuera de red &mdash; terreno m&aacute;s barato, m&aacute;s infraestructura.</li>
</ul>"""),
  ("Municipio propio desde 2016",
   """<p>Puerto Morelos se separ&oacute; de Benito Ju&aacute;rez en 2016 y hoy emite su propio uso de suelo, licencias, alineamientos y ocupaci&oacute;n. Tres consecuencias pr&aacute;cticas:</p>
<ul>
<li><strong>Se tramita aqu&iacute;, no en Canc&uacute;n.</strong> La orientaci&oacute;n basada en la pr&aacute;ctica de Benito Ju&aacute;rez est&aacute; desactualizada, igual que la experiencia de un vecino anterior a 2016.</li>
<li><strong>Verifique los n&uacute;meros del lote hoy.</strong> Los instrumentos de planeaci&oacute;n del municipio son relativamente recientes y se han actualizado: confirme densidad, altura y uso permitido para el predio exacto en lugar de asumirlos de un documento viejo.</li>
<li><strong>Una administraci&oacute;n peque&ntilde;a es una administraci&oacute;n directa.</strong> Quien revisa su expediente es accesible, lo que vuelve muy valioso presentar un expediente completo &mdash; y muy lento presentar uno incompleto.</li>
</ul>
<p>La revisi&oacute;n ambiental estatal (SEMA), la jurisdicci&oacute;n federal cuando aplica, CONAGUA en materia de agua y ZOFEMAT del lado de playa siguen aplicando igual que en el resto del corredor.</p>"""),
  ("Lo que el arrecife y los humedales agregan a la especificación",
   """<p>Puerto Morelos tiene la geograf&iacute;a ambiental m&aacute;s expl&iacute;cita del corredor: parque nacional de arrecife frente a la costa, manglar y humedal protegidos detr&aacute;s del pueblo, y karst con cenotes tierra adentro. Cada uno es una partida, no un lema.</p>
<ul>
<li><strong>La calidad de la descarga es el centro del expediente.</strong> Tratamiento antes de infiltrar, correctamente dimensionado, con el retrolavado de alberca por ruta separada &mdash; $90,000&ndash;$350,000 MXN seg&uacute;n ocupaci&oacute;n. Lo que se infiltra aqu&iacute; llega al acu&iacute;fero y de ah&iacute; al arrecife.</li>
<li><strong>El manglar no se negocia.</strong> En lotes junto al humedal hay que establecer el l&iacute;mite de vegetaci&oacute;n protegida antes de dibujar la huella &mdash; y algunos predios en venta tienen mucho menos &aacute;rea construible que la superficie escriturada. Rev&iacute;selo antes de comprar.</li>
<li><strong>Restricciones por cenotes</strong> tierra adentro, con limitaciones sobre qu&eacute; puede infiltrarse cerca.</li>
<li><strong>El nivel de piso terminado</strong> en terrenos bajos junto al humedal o la costa debe fijarse considerando inundaci&oacute;n y marea de tormenta. Es decisi&oacute;n de proyecto y no se corrige despu&eacute;s.</li>
<li><strong>En la Ruta de los Cenotes,</strong> presupueste el camino de acceso ($40,000&ndash;$300,000) y la extensi&oacute;n de CFE &mdash; cot&iacute;cela antes de comprar, va de $150,000 a m&aacute;s de $900,000 &mdash; o un sistema fuera de red con solar, almacenamiento, pozo tratado y captaci&oacute;n pluvial.</li>
</ul>
<p>La obra de 150 m&sup2; toma unos <strong>7&ndash;10 meses</strong> desde la licencia hasta la entrega.</p>"""),
 ],
 "faq": [
  ("¿Cuánto cuesta construir una casa en Puerto Morelos?",
   "Alrededor de $2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD) llave en mano para 150 m&sup2; en lote del pueblo o interior &mdash; unos $17,000&ndash;$21,000 MXN/m&sup2;, pr&aacute;cticamente al nivel de Playa del Carmen. Frente al mar sube a $26,000&ndash;$38,000+ y la Ruta de los Cenotes va de $14,000 a $24,000 seg&uacute;n servicios."),
  ("¿Qué municipio emite los permisos en Puerto Morelos?",
   "El propio Puerto Morelos: se separ&oacute; de Benito Ju&aacute;rez (Canc&uacute;n) en 2016. Cualquier orientaci&oacute;n basada en la pr&aacute;ctica de Canc&uacute;n est&aacute; desactualizada, y como los instrumentos de planeaci&oacute;n son recientes conviene verificar densidad, altura y uso del predio exacto."),
  ("¿Puedo construir en un lote junto al manglar?",
   "No dentro de la vegetaci&oacute;n protegida, y el l&iacute;mite debe establecerse antes de dibujar la huella. Algunos lotes en venta tienen bastante menos &aacute;rea construible que la superficie de escrituras, as&iacute; que conviene verificarlo antes de comprar."),
  ("¿Qué implica el parque nacional de arrecife para mi obra?",
   "Que la calidad de la descarga es la pregunta t&eacute;cnica central del expediente. Tratamiento antes de infiltrar dimensionado a la ocupaci&oacute;n, con retrolavado de alberca por ruta separada, cuesta $90,000&ndash;$350,000 MXN y se revisa con detalle porque el karst lleva lo infiltrado al acu&iacute;fero y al arrecife."),
  ("¿Construir en la Ruta de los Cenotes es más barato?",
   "El terreno s&iacute;, y la obra ronda $14,000&ndash;$19,000 MXN/m&sup2; en lote con servicios. Pero muchos predios no tienen CFE ni agua municipal: presupueste la extensi&oacute;n &mdash; cot&iacute;cela antes de comprar, va de $150,000 a m&aacute;s de $900,000 &mdash; o un sistema fuera de red, m&aacute;s $40,000&ndash;$300,000 de camino de acceso."),
 ],
}

Z[("es","playacar")] = {
 "title": "Cuánto Cuesta Construir una Casa en Playacar 2026",
 "desc": "Playacar está prácticamente lleno: la mayoría de proyectos son remodelación o demolición. Rangos 2026, costo de demolición, comité de diseño y Fase I vs Fase II.",
 "lead": "Una casa de 150 m&sup2; en <strong>Playacar</strong> cuesta aproximadamente <strong>$3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD)</strong> llave en mano en 2026, cerca de 25% arriba de Playa del Carmen base. Pero Playacar est&aacute; pr&aacute;cticamente construido, as&iacute; que la pregunta real no es cu&aacute;nto cuesta una casa nueva &mdash; es si conviene remodelar la que est&aacute; en el lote o tirarla.",
 "sections": [
  ("Remodelar o demoler: la aritmética",
   """<p>Casi todo proyecto en Playacar es una reconstrucci&oacute;n, una remodelaci&oacute;n mayor o una obra en uno de los pocos lotes que quedan. La decisi&oacute;n entre las dos primeras debe tomarse tras un dictamen, no tras una visita, porque las casas de esa edad en esta costa cargan un defecto predecible: corrosi&oacute;n del acero de refuerzo por cloruros en bordes de losa, balcones, columnas y pretiles.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Concepto</th><th>MXN</th></tr></thead><tbody>
<tr><td>Dictamen estructural con calas en zonas representativas</td><td>$40,000&ndash;$150,000</td></tr>
<tr><td>Demolici&oacute;n y retiro de escombro, casa tipo</td><td>$180,000&ndash;$600,000</td></tr>
<tr><td>Programa de reparaci&oacute;n de concreto, si se conserva</td><td>Se cotiza tras el dictamen &mdash; puede superar la demolici&oacute;n</td></tr>
<tr><td>Remodelaci&oacute;n integral, especificaci&oacute;n premium</td><td>$14,000&ndash;$26,000 MXN/m&sup2;</td></tr>
<tr><td>Obra nueva, premium</td><td>$24,000&ndash;$30,000 MXN/m&sup2;</td></tr>
<tr><td>Obra nueva, lujo</td><td>$30,000&ndash;$42,000 MXN/m&sup2;</td></tr>
</tbody></table></div>
<p>El umbral honesto: cuando la reparaci&oacute;n estructural se acerca a 25&ndash;30% del costo de reconstruir, est&aacute; pagando precio de obra nueva por la altura libre, la orientaci&oacute;n y la planta de un edificio viejo. En Playacar hay contraargumento real, eso s&iacute;: los lotes no se reponen, el arbolado maduro est&aacute; protegido y vale, y una casa de los noventa bien construida y con buenas alturas en Fase II puede merecer conservarse.</p>"""),
  ("Costo llave en mano por tamaño de casa",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tama&ntilde;o</th><th>Llave en mano (MXN)</th><th>Llave en mano (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.10M&ndash;$2.60M</td><td>$117k&ndash;$144k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.15M&ndash;$3.90M</td><td>$175k&ndash;$217k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.20M&ndash;$5.20M</td><td>$233k&ndash;$289k</td></tr>
<tr><td>250 m&sup2;</td><td>$5.25M&ndash;$6.50M</td><td>$292k&ndash;$361k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referencia: $21,000&ndash;$26,000 MXN/m&sup2; acabado est&aacute;ndar a premium. USD/MXN &asymp; 18. Sin terreno, alberca ni mobiliario.</p>
<p>Ese 25% sobre Playa del Carmen base es acceso restringido por calles angostas, trabajadores registrados y horarios limitados, el proceso del comit&eacute; de dise&ntilde;o, protecci&oacute;n de arbolado, especificaci&oacute;n de grado marino y el nivel de acabado que el mercado local espera. En un lote de Playacar frente al mar, agregue la zona federal mar&iacute;timo terrestre y vidrio de impacto en la fachada al mar: ah&iacute; el rango es $42,000&ndash;$60,000+ MXN/m&sup2;.</p>"""),
  ("El comité, los árboles y Fase I vs Fase II",
   """<p><strong>La revisi&oacute;n arquitect&oacute;nica es real</strong> y es donde se atrasan los programas en Playacar. Espere revisi&oacute;n de altura, volumetr&iacute;a y remetimientos m&aacute;s estrictos que los municipales, forma y materiales de cubierta, tratamiento de fachada y paleta de color, bardas y cercas, y sobre todo retiro de arbolado &mdash; el dosel maduro es parte de lo que la comunidad protege y cada &aacute;rbol se justifica. Presente en anteproyecto con el inventario de arbolado en mano, y contemple al menos un ciclo de revisi&oacute;n m&aacute;s la fianza de obra.</p>
<p><strong>Fase I y Fase II son lugares distintos.</strong> Fase I est&aacute; m&aacute;s cerca del pueblo y del ferry: m&aacute;s densa, lotes m&aacute;s chicos, caminabilidad real a la Quinta Avenida y acceso de obra por calles angostas que encarece. Fase II es mayor y m&aacute;s tranquila alrededor del campo de golf, con lotes grandes, vegetaci&oacute;n madura y espacio para una villa importante &mdash; y el frente de golf trae su propia pregunta de cristaler&iacute;a, porque las pelotas desviadas son un riesgo cotizable en ventanas y domos.</p>
<p>Los permisos se tramitan en <strong>Solidaridad</strong>, la misma ruta que el resto de Playa del Carmen, con la revisi&oacute;n de la comunidad por delante en la pr&aacute;ctica. La obra toma unos <strong>7&ndash;10 meses</strong> para 150 m&sup2;, m&aacute;s la demolici&oacute;n cuando aplica.</p>"""),
 ],
 "faq": [
  ("¿Cuánto cuesta construir en Playacar?",
   "Alrededor de $3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD) llave en mano para 150 m&sup2; &mdash; unos $21,000&ndash;$26,000 MXN/m&sup2;, cerca de 25% arriba de Playa del Carmen base. Especificaci&oacute;n de lujo va de $30,000 a $42,000 y los lotes frente al mar de $42,000 a $60,000+."),
  ("¿Conviene remodelar la casa existente o demolerla?",
   "Primero un dictamen con calas en zonas representativas, $40,000&ndash;$150,000 MXN, porque las casas de esa edad suelen traer corrosi&oacute;n del refuerzo por cloruros. Cuando la reparaci&oacute;n estructural se acerca a 25&ndash;30% del costo de reconstruir, normalmente conviene demoler: retiro y escombro cuestan $180,000&ndash;$600,000."),
  ("¿Qué revisa el comité de diseño de Playacar?",
   "Altura, volumetr&iacute;a y remetimientos m&aacute;s estrictos que los municipales, forma y materiales de cubierta, fachada y color, bardas y cercas, y el retiro de arbolado, que debe justificarse &aacute;rbol por &aacute;rbol. Tambi&eacute;n fija reglas de obra: trabajadores registrados, horarios, entregas, almacenaje y fianza."),
  ("¿Qué diferencia hay entre Fase I y Fase II para construir?",
   "Fase I tiene lotes m&aacute;s chicos y densos con acceso de obra por calles angostas que encarece, y caminabilidad real a la Quinta Avenida. Fase II tiene lotes grandes junto al golf, vegetaci&oacute;n madura y espacio para una villa &mdash; y el frente de golf vuelve la especificaci&oacute;n de ventanas y domos un tema pr&aacute;ctico."),
  ("¿Por qué Playacar cuesta 25% más que el resto de Playa del Carmen?",
   "Acceso restringido por calles angostas, trabajadores registrados y horarios limitados, el proceso del comit&eacute;, protecci&oacute;n de arbolado durante la obra, especificaci&oacute;n de grado marino y el nivel de acabado que espera el mercado local. Cada punto es una partida real, no un recargo por la direcci&oacute;n."),
 ],
}

Z[("es","mayakoba")] = {
 "title": "Cuánto Cuesta Construir una Casa en Mayakoba 2026",
 "desc": "Mayakoba es el lugar más caro para construir en la Riviera Maya. Rangos por m² 2026, qué incluye realmente la especificación de nivel resort y por qué.",
 "lead": "Una casa de 150 m&sup2; en <strong>Mayakoba</strong> cuesta aproximadamente <strong>$3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD)</strong> llave en mano en 2026 &mdash; el rango m&aacute;s alto del corredor, cerca de 42% arriba de Playa del Carmen base. Aunque casi nada se construye en ese extremo bajo: lo que realmente se levanta aqu&iacute; est&aacute; muy por encima, y esta p&aacute;gina explica por qu&eacute;.",
 "sections": [
  ("Costo llave en mano y la cifra realista",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tama&ntilde;o</th><th>Llave en mano (MXN)</th><th>Llave en mano (USD)</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.60M&ndash;$4.50M</td><td>$200k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$6M&ndash;$7.50M</td><td>$333k&ndash;$417k</td></tr>
<tr><td>350 m&sup2;</td><td>$8.40M&ndash;$10.50M</td><td>$467k&ndash;$583k</td></tr>
<tr><td>500 m&sup2;</td><td>$12M&ndash;$15M</td><td>$667k&ndash;$833k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referencia: $24,000&ndash;$30,000 MXN/m&sup2; acabado est&aacute;ndar a premium. USD/MXN &asymp; 18. Sin terreno, alberca ni mobiliario.</p>
<p>Esas cifras son el rango de entrada. Las casas que efectivamente se construyen dentro del plan maestro son de 300&ndash;600 m&sup2; con especificaci&oacute;n de autor, lo que lleva los n&uacute;meros reales a <strong>$35,000&ndash;$55,000 MXN/m&sup2;</strong> contando dise&ntilde;o arquitect&oacute;nico, herrajes y acabados importados, automatizaci&oacute;n completa, alberca de proyecto y jardiner&iacute;a madura. Presupuestar una villa de Mayakoba desde los $24,000 es presupuestar una casa que no pasar&iacute;a la revisi&oacute;n de dise&ntilde;o.</p>"""),
  ("Qué compra realmente ese sobreprecio",
   """<ul>
<li><strong>Control de dise&ntilde;o.</strong> Un plan maestro construido alrededor de la operaci&oacute;n hotelera revisa arquitectura, materiales, color, paisaje e iluminaci&oacute;n con el est&aacute;ndar de los hoteles vecinos. Las presentaciones son detalladas, los ciclos de revisi&oacute;n existen y abaratar la fachada no es una opci&oacute;n disponible.</li>
<li><strong>Expectativa de acabado.</strong> Los comparables son residencias de marca. Carpinter&iacute;a, piedra, cristaler&iacute;a y herrajes se especifican contra eso, y la mano de obra para instalarlos con precisi&oacute;n cuesta m&aacute;s que los materiales.</li>
<li><strong>Disciplina de obra.</strong> Se construye dentro de un entorno de resort en operaci&oacute;n: acceso controlado, trabajadores registrados, horarios restringidos, tapiales apantallados, l&iacute;mites de ruido, obligaciones de limpieza y fianza. Cada punto son horas de programa.</li>
<li><strong>Entorno ambiental.</strong> El plan maestro se organiza alrededor de lagunas, canales y manglar. Vegetaci&oacute;n conservada, restricciones, drenaje y descarga se gestionan a nivel comunidad adem&aacute;s de las autoridades &mdash; y el paisaje que no puede retirar es parte de lo que paga.</li>
<li><strong>Especificaci&oacute;n marina y de humedad</strong> completa: inoxidable 316, aluminio anodizado o con recubrimiento marino, recubrimiento generoso de concreto, carpinter&iacute;a ventilada.</li>
<li><strong>Escasez.</strong> Pocos lotes residenciales y cada proyecto es a la medida: no hay repetici&oacute;n entre la cual repartir el costo de dise&ntilde;o y direcci&oacute;n.</li>
</ul>"""),
  ("Programa, permisos y qué más presupuestar",
   """<p>Los permisos se tramitan en el municipio de <strong>Solidaridad</strong> &mdash; uso de suelo, licencia, alineamiento y DRO &mdash; con la revisi&oacute;n arquitect&oacute;nica de la comunidad por delante y, por el entorno, una revisi&oacute;n ambiental que toma en serio la laguna y el manglar. Presente a la comunidad en anteproyecto: terminar un dise&ntilde;o y despu&eacute;s mandarlo a revisi&oacute;n es como los proyectos de Mayakoba pierden un trimestre.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Además de la obra</th><th>MXN</th></tr></thead><tbody>
<tr><td>Dise&ntilde;o e ingenier&iacute;a de autor a este nivel</td><td>10&ndash;15% de la obra</td></tr>
<tr><td>Presentaci&oacute;n a la comunidad, revisiones y fianza</td><td>$150,000&ndash;$600,000</td></tr>
<tr><td>Alberca de proyecto con equipo</td><td>$900,000&ndash;$3,500,000</td></tr>
<tr><td>Jardiner&iacute;a madura y riego</td><td>$400,000&ndash;$2,000,000</td></tr>
<tr><td>Mobiliario y equipamiento de una villa de esta clase</td><td>$1,500,000&ndash;$6,000,000</td></tr>
<tr><td>Cuota de comunidad</td><td>Recurrente &mdash; verificar por lote</td></tr>
</tbody></table></div>
<p>La obra toma unos <strong>10&ndash;16 meses</strong> para una villa de esta especificaci&oacute;n, m&aacute;s que la norma del corredor: horarios restringidos, ciclos de revisi&oacute;n y precisi&oacute;n de acabado consumen tiempo que un lote suburbano no consume. Contrate a precio fijo con presupuesto desglosado y pagos por avance verificado.</p>"""),
 ],
 "faq": [
  ("¿Cuánto cuesta construir una casa en Mayakoba?",
   "El rango de entrada es $24,000&ndash;$30,000 MXN/m&sup2;, es decir $3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD) para 150 m&sup2;. En la pr&aacute;ctica se construyen casas de 300&ndash;600 m&sup2; a $35,000&ndash;$55,000 MXN/m&sup2; contando dise&ntilde;o de autor, acabados importados, automatizaci&oacute;n, alberca y jardiner&iacute;a madura."),
  ("¿Por qué Mayakoba es lo más caro del corredor?",
   "Control de dise&ntilde;o con est&aacute;ndar de resort, expectativa de acabado comparada con residencias de marca, disciplina de obra dentro de un entorno de lujo en operaci&oacute;n, gesti&oacute;n ambiental alrededor de lagunas y manglar, especificaci&oacute;n marina completa y escasez de lotes sin repetici&oacute;n entre la cual repartir costos."),
  ("¿Qué debo presupuestar además de la obra?",
   "Dise&ntilde;o e ingenier&iacute;a 10&ndash;15% de la obra, presentaci&oacute;n y fianza $150,000&ndash;$600,000, alberca de proyecto $900,000&ndash;$3,500,000, jardiner&iacute;a madura $400,000&ndash;$2,000,000, mobiliario y equipamiento $1,500,000&ndash;$6,000,000, y la cuota recurrente de comunidad."),
  ("¿Cuánto tarda una villa en Mayakoba?",
   "Unos 10&ndash;16 meses para una villa de esta especificaci&oacute;n, m&aacute;s que la norma del corredor. Horarios restringidos, ciclos de revisi&oacute;n de la comunidad y la precisi&oacute;n que exige el nivel de acabado consumen tiempo adicional."),
  ("¿Quién aprueba el diseño?",
   "El municipio de Solidaridad para uso de suelo, licencia, alineamiento y DRO, y la revisi&oacute;n arquitect&oacute;nica de la comunidad, que en la pr&aacute;ctica va primero y examina arquitectura, materiales, color, paisaje e iluminaci&oacute;n. Presente en anteproyecto."),
 ],
}

Z[("es","corasol")] = {
 "title": "Cuánto Cuesta Construir una Casa en Corasol 2026",
 "desc": "Costos de obra en Corasol 2026 y qué implica construir dentro de un plan maestro en desarrollo: infraestructura por etapas, comité, frente de golf y accesos.",
 "lead": "Una casa de 150 m&sup2; en <strong>Corasol</strong> cuesta aproximadamente <strong>$3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD)</strong> llave en mano en 2026, cerca de 30% arriba de Playa del Carmen base. Corasol es adem&aacute;s donde est&aacute; nuestra oficina, as&iacute; que esta p&aacute;gina se escribe a pocos minutos a pie del tema.",
 "sections": [
  ("Costo llave en mano por tamaño de casa",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tama&ntilde;o</th><th>Llave en mano (MXN)</th><th>Llave en mano (USD)</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.30M&ndash;$4.12M</td><td>$183k&ndash;$229k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.40M&ndash;$5.50M</td><td>$244k&ndash;$306k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.60M&ndash;$8.25M</td><td>$367k&ndash;$458k</td></tr>
<tr><td>450 m&sup2;</td><td>$9.90M&ndash;$12.38M</td><td>$550k&ndash;$688k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referencia: $22,000&ndash;$27,500 MXN/m&sup2; acabado est&aacute;ndar a premium. USD/MXN &asymp; 18. Sin terreno, alberca ni mobiliario.</p>
<p>La mayor parte de lo que se construye aqu&iacute; supera los 150 m&sup2;: los lotes y el mercado empujan hacia villas de 250&ndash;450 m&sup2; con alberca, roof garden y jardiner&iacute;a de proyecto. Presupueste el paquete completo y no solo el precio por metro: en una villa de 300 m&sup2;, alberca, jardiner&iacute;a, mobiliario y honorarios suman com&uacute;nmente 35&ndash;50% sobre la cifra de obra.</p>"""),
  ("Construir dentro de una comunidad que todavía se construye",
   """<p>Esta es la diferencia pr&aacute;ctica entre Corasol y una direcci&oacute;n consolidada como Playacar. El plan maestro sigue desarroll&aacute;ndose, y eso corta por los dos lados:</p>
<ul>
<li><strong>La infraestructura llega por etapas.</strong> Confirme para su lote qu&eacute; hay realmente en el l&iacute;mite del predio hoy &mdash; capacidad el&eacute;ctrica, agua, drenaje, superficie de calle &mdash; y qu&eacute; est&aacute; programado en lugar de prometido. La distancia entre "la comunidad tendr&aacute;" y "el lote tiene" es donde se mueven los presupuestos.</li>
<li><strong>Tendr&aacute; vecinos en obra.</strong> Otras casas y obras de comunidad estar&aacute;n en marcha durante a&ntilde;os: ruido y tr&aacute;fico durante su propia ocupaci&oacute;n, y accesos compartidos durante su construcci&oacute;n.</li>
<li><strong>La revisi&oacute;n de dise&ntilde;o est&aacute; activa y en evoluci&oacute;n.</strong> El comit&eacute; examina altura, volumetr&iacute;a, materiales, color, bardas y paisaje con la intenci&oacute;n de proteger una imagen coherente en una comunidad que a&uacute;n no termina. Presente en anteproyecto.</li>
<li><strong>Reglas de acceso y obra.</strong> Trabajadores registrados, entrada controlada, horarios de entrega definidos, l&iacute;mites de almacenaje en el lote, limpieza de calle y fianza. Presupueste $80,000&ndash;$300,000 MXN entre presentaci&oacute;n, fianza y gesti&oacute;n de accesos.</li>
<li><strong>El frente de golf</strong> en los lotes correspondientes trae la pregunta de cristaler&iacute;a y domos &mdash; las pelotas desviadas son un riesgo real y cotizable &mdash; adem&aacute;s de la interfaz de riego y drenaje con el campo.</li>
</ul>"""),
  ("Condiciones de sitio, permisos y programa",
   """<p>Corasol pertenece al municipio de <strong>Solidaridad</strong>, as&iacute; que la ruta de permisos es la conocida: certificado de uso de suelo, alineamiento, licencia de construcci&oacute;n y Director Responsable de Obra, con la revisi&oacute;n arquitect&oacute;nica de la comunidad por delante en la pr&aacute;ctica. Los requisitos ambientales aplican al lote como en el resto de la costa, y el karst exige mec&aacute;nica de suelos con sondeos sobre la huella real: buena capacidad de carga somera y una cavidad dos metros al lado son ambas normales aqu&iacute;.</p>
<ul>
<li><strong>La especificaci&oacute;n marina sigue aplicando.</strong> Corasol est&aacute; lo bastante cerca del mar para que inoxidable 316, aluminio anodizado o con recubrimiento marino y recubrimiento generoso de concreto sean lo correcto, no una mejora opcional.</li>
<li><strong>Dise&ntilde;e la azotea como terraza desde el inicio</strong> si la altura lo permite. En lotes con vista al campo o hacia el mar es el metro cuadrado m&aacute;s valioso de la casa, y adaptarla despu&eacute;s cuesta varias veces lo que incluirla.</li>
<li><strong>Planee bien el cuarto de m&aacute;quinas:</strong> cisterna, hidroneum&aacute;tico, tratamiento de agua por la dureza local, equipo de alberca y posiciones de aire acondicionado, todo accesible para servicio.</li>
</ul>
<p>La obra toma unos <strong>8&ndash;12 meses</strong> para una villa de 250&ndash;300 m&sup2;, y m&aacute;s si la revisi&oacute;n de dise&ntilde;o pasa de un ciclo. Contrate a precio fijo con presupuesto desglosado y pagos por avance verificado &mdash; y si compra el lote ahora para construir despu&eacute;s, obtenga por escrito la situaci&oacute;n de servicios en el l&iacute;mite del predio antes de cerrar.</p>"""),
 ],
 "faq": [
  ("¿Cuánto cuesta construir una casa en Corasol?",
   "Alrededor de $3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD) llave en mano para 150 m&sup2; &mdash; unos $22,000&ndash;$27,500 MXN/m&sup2;, cerca de 30% arriba de Playa del Carmen base. La mayor&iacute;a de las casas aqu&iacute; son de 250&ndash;450 m&sup2;, donde alberca, jardiner&iacute;a, mobiliario y honorarios suman 35&ndash;50% adicional."),
  ("¿Qué debo revisar antes de comprar un lote en Corasol?",
   "Qu&eacute; infraestructura est&aacute; realmente en el l&iacute;mite del lote hoy &mdash; capacidad el&eacute;ctrica, agua, drenaje, superficie de calle &mdash; frente a lo que est&aacute; programado. En un plan maestro en desarrollo, esa diferencia es donde se mueven los presupuestos."),
  ("¿El comité de diseño agrega costo y tiempo?",
   "S&iacute; a ambos. Presupueste $80,000&ndash;$300,000 MXN entre presentaci&oacute;n, fianza de obra y gesti&oacute;n de accesos, y contemple al menos un ciclo de revisi&oacute;n en el programa, adem&aacute;s de trabajadores registrados, entrada controlada, horarios y limpieza de calle."),
  ("¿Qué cambia con frente al campo de golf?",
   "La especificaci&oacute;n de ventanas y domos, porque las pelotas desviadas son un riesgo real y cotizable, adem&aacute;s de la interfaz de riego y drenaje con el campo. Conviene resolverlo en proyecto y no reemplazando cristales despu&eacute;s."),
  ("¿Cuánto tarda una villa en Corasol?",
   "Unos 8&ndash;12 meses para 250&ndash;300 m&sup2; desde la licencia hasta la entrega, y m&aacute;s si la revisi&oacute;n de dise&ntilde;o pasa de un ciclo. Los horarios restringidos y el acceso controlado empujan el programa al extremo largo."),
 ],
}

Z[("es","aldea-zama")] = {
 "title": "Cuánto Cuesta Construir una Casa en Aldea Zamá 2026",
 "desc": "Costos en Aldea Zamá 2026 más la partida que nadie presupuesta: el calendario de permisos de Tulum. Altura, confiabilidad eléctrica y el plan maestro urbanizado.",
 "lead": "Una casa de 150 m&sup2; en <strong>Aldea Zam&aacute;</strong> cuesta aproximadamente <strong>$3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD)</strong> llave en mano en 2026, cerca de 20% arriba de Playa del Carmen base. La cifra de obra es directa. La que casi nadie presupuesta en Tulum es el tiempo.",
 "sections": [
  ("Costo llave en mano por tamaño de casa",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tama&ntilde;o</th><th>Llave en mano (MXN)</th><th>Llave en mano (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.05M&ndash;$2.50M</td><td>$114k&ndash;$139k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.08M&ndash;$3.75M</td><td>$171k&ndash;$208k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.10M&ndash;$5M</td><td>$228k&ndash;$278k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.15M&ndash;$7.50M</td><td>$342k&ndash;$417k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referencia: $20,500&ndash;$25,000 MXN/m&sup2; acabado est&aacute;ndar a premium. USD/MXN &asymp; 18. Sin terreno, alberca ni mobiliario.</p>
<p>Aldea Zam&aacute; cotiza por encima de las Regiones de Tulum y de La Veleta por una raz&oacute;n simple: es un plan maestro urbanizado, con servicios instalados, accesos pavimentados y car&aacute;cter definido, a distancia caminable o de bicicleta de la carretera de playa. Se paga infraestructura que ya existe en vez de infraestructura que hay que construir.</p>"""),
  ("Lo que realmente cuesta el calendario de permisos",
   """<p>La revisi&oacute;n de Tulum es la m&aacute;s exigente del corredor en materia ambiental, y en un lote con vegetaci&oacute;n el expediente es la ruta cr&iacute;tica. Duraciones realistas desde la compra hasta iniciar obra:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Etapa</th><th>Duración</th></tr></thead><tbody>
<tr><td>Certificado de uso de suelo y alineamiento</td><td>2&ndash;8 semanas</td></tr>
<tr><td>Mec&aacute;nica de suelos (en paralelo)</td><td>2&ndash;5 semanas</td></tr>
<tr><td>Expediente ambiental</td><td>3&ndash;8 meses seg&uacute;n vegetaci&oacute;n</td></tr>
<tr><td>Proyecto t&eacute;cnico (en paralelo)</td><td>6&ndash;14 semanas</td></tr>
<tr><td>Revisi&oacute;n de licencia con expediente completo</td><td>4&ndash;12 semanas</td></tr>
<tr><td><strong>Total antes de iniciar obra</strong></td><td><strong>5&ndash;12 meses</strong></td></tr>
</tbody></table></div>
<p>Esos meses son una partida real: terreno cargado y capital comprometido sin producir. Dos formas de acortarlos. Primero, arranque el expediente ambiental y la mec&aacute;nica de suelos con la arquitectura todav&iacute;a en anteproyecto &mdash; ninguno requiere planos finales y ambos condicionan el dise&ntilde;o. Segundo, al comparar lotes, valore mucho una autorizaci&oacute;n ambiental vigente: puede valer seis meses y una cifra de seis d&iacute;gitos.</p>"""),
  ("Altura, energía y qué se construye aquí",
   """<ul>
<li><strong>Los l&iacute;mites de altura son restringidos</strong> y se aplican. Las reglas de Tulum son deliberadamente m&aacute;s estrictas que las de Playa del Carmen, as&iacute; que verifique el l&iacute;mite exacto de su lote antes de dise&ntilde;ar una azotea &mdash; en muchos predios el roof garden es la diferencia entre un buen proyecto y uno comprometido, y depende de ese solo n&uacute;mero.</li>
<li><strong>La confiabilidad el&eacute;ctrica es menor que en Playa del Carmen.</strong> Presupueste protecci&oacute;n contra sobretensiones para toda la casa como est&aacute;ndar y, en propiedad de renta, un sistema de bater&iacute;as para lo esencial &mdash; internet, controlador de alberca, algo de iluminaci&oacute;n y un ventilador &mdash; por $140,000&ndash;$330,000 MXN. El solar tiene mucho sentido aqu&iacute;, sobre todo cuando bomba de alberca y varios equipos de aire llevan el consumo a la tarifa DAC.</li>
<li><strong>El mercado est&aacute; dominado por condominios,</strong> que es justamente el argumento para construir casa. Una casa independiente no puede perder su permiso de renta corta por acuerdo de asamblea, no paga cuota de mantenimiento sobre el ingreso bruto y puede dise&ntilde;arse para rendimiento: rec&aacute;maras con ba&ntilde;o propio, casita lock-off, roof garden y alberca colocada para la fotograf&iacute;a.</li>
</ul>
<p>T&eacute;cnicamente aplican los temas habituales de Tulum: tratamiento antes de infiltrar dimensionado a la ocupaci&oacute;n ($90,000&ndash;$250,000 MXN), tratamiento de agua por la dureza local, detalles contra termita y humedad, y mec&aacute;nica de suelos porque el karst aqu&iacute; est&aacute; lleno de cenotes. La obra toma unos <strong>7&ndash;11 meses</strong> para 150&ndash;200 m&sup2;.</p>"""),
 ],
 "faq": [
  ("¿Cuánto cuesta construir una casa en Aldea Zamá?",
   "Alrededor de $3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD) llave en mano para 150 m&sup2; con acabado est&aacute;ndar a premium &mdash; unos $20,500&ndash;$25,000 MXN/m&sup2;, cerca de 20% arriba de Playa del Carmen base."),
  ("¿Por qué cuesta más que las Regiones de Tulum?",
   "Porque la infraestructura ya existe: es un plan maestro urbanizado con servicios instalados, accesos pavimentados y car&aacute;cter definido cerca de la carretera de playa. En un lote de Regi&oacute;n m&aacute;s barato se paga despu&eacute;s construir los servicios, el acceso y el entorno."),
  ("¿Cuánto tardo en poder iniciar obra en Tulum?",
   "De cinco a doce meses desde la compra: 2&ndash;8 semanas de uso de suelo y alineamiento, 3&ndash;8 meses de expediente ambiental en lote con vegetaci&oacute;n, y 4&ndash;12 semanas de revisi&oacute;n de licencia. Arranque el expediente y la mec&aacute;nica de suelos con la arquitectura a&uacute;n en anteproyecto."),
  ("¿Puedo construir roof garden en Aldea Zamá?",
   "Depende del l&iacute;mite de altura de su lote, y en Tulum esos l&iacute;mites son deliberadamente restringidos y se aplican. Verif&iacute;quelo antes de dise&ntilde;ar: en muchos predios la azotea utilizable es la diferencia entre un proyecto fuerte y uno comprometido."),
  ("¿Qué hago con los cortes de energía en Tulum?",
   "Protecci&oacute;n contra sobretensiones para toda la casa como est&aacute;ndar y, en propiedad de renta, bater&iacute;as para lo esencial &mdash; internet, controlador de alberca, iluminaci&oacute;n y ventilador &mdash; por $140,000&ndash;$330,000 MXN. El solar tambi&eacute;n se paga r&aacute;pido, sobre todo si el consumo ya lleg&oacute; a tarifa DAC."),
 ],
}

Z[("es","playa-del-carmen")] = {
 "title": "Costo de Construir una Casa en Playa del Carmen: Por Etapas",
 "desc": "El precio de referencia del corredor. Presupuesto por etapas de una casa de 150 m², qué incluye y qué no el precio por m², extras y cómo no perder el control.",
 "lead": "Una casa familiar bien construida de 150 m&sup2; en <strong>Playa del Carmen</strong> cuesta aproximadamente <strong>$2.6M&ndash;$3.2M MXN ($145,000&ndash;$178,000 USD)</strong> llave en mano en 2026. Esta es la cifra contra la que se compara todo el corredor, as&iacute; que conviene entenderla por etapas y no como un solo n&uacute;mero.",
 "sections": [
  ("Presupuesto por etapas (casa estándar de 150 m²)",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Etapa</th><th>% del presupuesto</th><th>Costo aprox. (MXN)</th><th>Incluye</th></tr></thead><tbody>
<tr><td>Permisos, DRO y estudios</td><td>5%</td><td>$130,000&ndash;$160,000</td><td>Licencia, DRO, mec&aacute;nica de suelos, topograf&iacute;a</td></tr>
<tr><td>Cimentaci&oacute;n y estructura</td><td>30%</td><td>$780,000&ndash;$960,000</td><td>Losa, columnas, trabes, entrepisos</td></tr>
<tr><td>Muros y cubierta</td><td>18%</td><td>$470,000&ndash;$580,000</td><td>Block, castillos, losa de azotea</td></tr>
<tr><td>Instalaciones</td><td>15%</td><td>$390,000&ndash;$480,000</td><td>El&eacute;ctrica, hidr&aacute;ulica, sanitaria</td></tr>
<tr><td>Acabados</td><td>25%</td><td>$650,000&ndash;$800,000</td><td>Pisos, pintura, chukum, carpinter&iacute;a</td></tr>
<tr><td>Limpieza y entrega</td><td>7%</td><td>$180,000&ndash;$220,000</td><td>Detalles finales, entrega</td></tr>
</tbody></table></div>
<p class="text-muted small">Total llave en mano &asymp; $2.6M&ndash;$3.2M MXN. Sin terreno, alberca ni mobiliario.</p>
<p>Dos lecturas de esa tabla. La estructura es casi un tercio del presupuesto y es la &uacute;nica etapa donde ahorrar es genuinamente peligroso en una zona de vientos altos. Y los acabados, con 25%, son donde vive realmente su especificaci&oacute;n: la misma obra negra con distintos acabados mueve el total un 20% sin cambiar un solo plano.</p>"""),
  ("Qué incluye y qué no el precio por m²",
   """<p>El rango de $17,000&ndash;$21,000 MXN/m&sup2; que produce esos totales cubre estructura, instalaciones y acabados est&aacute;ndar. Lo siguiente queda fuera y explica la mayor&iacute;a de las sorpresas de presupuesto:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Concepto</th><th>MXN</th></tr></thead><tbody>
<tr><td>Terreno</td><td>Aparte, y la mayor variable en Playa del Carmen</td></tr>
<tr><td>Alberca de 4&times;8 m con equipo</td><td>$450,000&ndash;$1,200,000</td></tr>
<tr><td>Habilitaci&oacute;n de roof garden (estructura ya prevista)</td><td>$3,500&ndash;$9,000 por m&sup2;</td></tr>
<tr><td>Tren de tratamiento de agua (filtro, suavizador, carb&oacute;n, &oacute;smosis)</td><td>$35,000&ndash;$95,000</td></tr>
<tr><td>Aire acondicionado, 4&ndash;5 zonas inverter</td><td>$120,000&ndash;$280,000</td></tr>
<tr><td>Solar, 5&ndash;8 kWp</td><td>$115,000&ndash;$250,000</td></tr>
<tr><td>Jardiner&iacute;a y riego</td><td>$500&ndash;$2,000 por m&sup2;</td></tr>
<tr><td>Mobiliario y electrodom&eacute;sticos</td><td>$450,000&ndash;$1,200,000 en casa familiar</td></tr>
</tbody></table></div>
<p>Dise&ntilde;o, ingenier&iacute;a, estudios y permisos suman normalmente 8&ndash;14% del costo de obra en una casa a la medida &mdash; en parte ya reflejado en la tabla anterior, y no es partida para comprimir: cada error que evita cuesta m&aacute;s que el paquete completo.</p>"""),
  ("Por qué es la referencia del corredor y cómo sostener el presupuesto",
   """<p>Playa del Carmen cotiza por debajo de las zonas cerradas y premium por razones estructurales, no de calidad: base amplia de proveedores, competencia real entre constructoras, lotes urbanos con servicios, una ruta de permisos directa en el municipio de <strong>Solidaridad</strong> y ausencia de zona federal mar&iacute;timo terrestre en la gran mayor&iacute;a de los predios. Todo lo dem&aacute;s del corredor es un m&uacute;ltiplo de esta cifra: Puerto Morelos al mismo nivel, Puerto Aventuras cerca de 8% arriba, Akumal 12%, Aldea Zam&aacute; 20%, Playacar 25%, Corasol 30% y Mayakoba 42%.</p>
<p>Cuatro h&aacute;bitos que mantienen el presupuesto donde empez&oacute;:</p>
<ul>
<li><strong>Precio fijo con presupuesto desglosado,</strong> no un precio por m&sup2; de apret&oacute;n de manos. Una tarifa &uacute;nica multiplicada por metros no es un presupuesto: es una invitaci&oacute;n a renegociar.</li>
<li><strong>Pagos contra avance f&iacute;sico verificado,</strong> no contra fechas, con 5&ndash;10% de retenci&oacute;n liberada al cerrar la lista de detalles.</li>
<li><strong>&Oacute;rdenes de cambio por escrito y cotizadas antes de ejecutarlas.</strong> Los cambios verbales son la ruta m&aacute;s com&uacute;n de un precio firme a uno abierto.</li>
<li><strong>Lista expl&iacute;cita de exclusiones</strong> &mdash; mobiliario, electrodom&eacute;sticos, jardiner&iacute;a m&aacute;s all&aacute; de cierto l&iacute;mite, derechos de conexi&oacute;n &mdash; acordada en la firma, para que las sorpresas ocurran en papel y no en obra.</li>
</ul>
<p>Una casa de 150 m&sup2; toma unos <strong>7&ndash;10 meses</strong> desde la licencia hasta la entrega, m&aacute;s dos a cuatro meses de tr&aacute;mites previos. Use la <a href="/calculadora/">calculadora de costos</a> para una estimaci&oacute;n r&aacute;pida con su tama&ntilde;o y nivel de acabado.</p>"""),
 ],
 "faq": [
  ("¿Cuánto cuesta construir una casa en Playa del Carmen en 2026?",
   "Alrededor de $2.6M&ndash;$3.2M MXN ($145,000&ndash;$178,000 USD) llave en mano para una casa de 150 m&sup2; con acabado est&aacute;ndar &mdash; unos $17,000&ndash;$21,000 MXN/m&sup2;, sin terreno, alberca ni mobiliario."),
  ("¿Qué no incluye el precio por metro cuadrado?",
   "Terreno, alberca ($450,000&ndash;$1,200,000), habilitaci&oacute;n de roof garden, tratamiento de agua, aire acondicionado, solar, jardiner&iacute;a y mobiliario. De ah&iacute; vienen casi todas las sorpresas de presupuesto, as&iacute; que convi&eacute;rtalas en partidas propias desde el inicio."),
  ("¿Qué etapa cuesta más?",
   "Cimentaci&oacute;n y estructura, con cerca de 30% del presupuesto, seguidas de acabados con 25%. La estructura es tambi&eacute;n donde ahorrar resulta peligroso en zona de vientos altos, mientras que los acabados pueden mover el total un 20% sin cambiar un plano."),
  ("¿Cómo se compara con las demás zonas?",
   "Es la referencia. Puerto Morelos est&aacute; al mismo nivel, Puerto Aventuras cerca de 8% arriba, Akumal 12%, Aldea Zam&aacute; 20%, Playacar 25%, Corasol 30% y Mayakoba 42% &mdash; y esas diferencias vienen de accesos restringidos, comit&eacute;s de dise&ntilde;o, especificaci&oacute;n marina y requisitos ambientales, no de calidad de obra."),
  ("¿Cómo evito que el presupuesto se desborde?",
   "Precio fijo con presupuesto desglosado en lugar de una tarifa por m&sup2;, pagos contra avance f&iacute;sico verificado con 5&ndash;10% de retenci&oacute;n, &oacute;rdenes de cambio por escrito y cotizadas antes de ejecutarse, y una lista expl&iacute;cita de exclusiones acordada en la firma."),
 ],
}

Z[("de","cancun")] = {
 "title": "Hausbau-Kosten in Cancún 2026: Warum Es Günstiger Ist",
 "desc": "In Cancún baut man günstiger als im übrigen Korridor. Die m²-Spannen für 2026, woher der Abschlag kommt und wo er zum Risiko wird.",
 "lead": "Ein 150-m&sup2;-Familienhaus in <strong>Canc&uacute;n</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$2.48M&ndash;$3M MXN ($138k&ndash;$167k USD)</strong> &mdash; der niedrigste Wert im Korridor und etwa 4% unter Playa del Carmen bei gleicher Ausstattung. Hier steht, woher dieser Abschlag kommt und wo er aufh&ouml;rt, ein Schn&auml;ppchen zu sein.",
 "sections": [
  ("Warum Cancún unter dem Rest des Korridors liegt",
   """<p>Canc&uacute;n ist der einzige Ort im Korridor, an dem die Gr&ouml;&szlig;e des Marktes dem Bauherrn n&uuml;tzt: der gr&ouml;&szlig;te Arbeitskr&auml;ftepool der Region, die h&ouml;chste Dichte an Lieferanten und Werkst&auml;tten und genug konkurrierende Bauunternehmen, dass Preise tats&auml;chlich gepr&uuml;ft werden. Alles s&uuml;dlich von Puerto Morelos holt einen Teil der Arbeit von hier.</p>
<ul>
<li><strong>Material an der Quelle.</strong> Block, Zement, Stahl, Zuschl&auml;ge, Aluminium, Fliesen und Sanit&auml;robjekte werden lokal gekauft, ohne Fracht durch den Korridor &mdash; bei einem 150-m&sup2;-Haus sind das allein mehrere Prozent.</li>
<li><strong>Gewerke ohne Anreise.</strong> Spezialarbeiten, die nach Tulum oder Akumal terminiert und transportiert werden m&uuml;ssen, sind hier ein Ortsgespr&auml;ch.</li>
<li><strong>Grundst&uuml;cke im Landesinneren.</strong> Der Hausbau in Canc&uacute;n findet gr&ouml;&szlig;tenteils in geschlossenen Wohnanlagen im Inland statt: keine Bundesk&uuml;stenzone, keine ZOFEMAT-Konzession, kein Schildkr&ouml;ten-Kalender und eine leichtere Umweltakte als ein vergleichbares K&uuml;stengrundst&uuml;ck.</li>
</ul>
<p>Genehmigt wird in der Gemeinde <strong>Benito Ju&aacute;rez</strong> &mdash; Nutzungszertifikat, Baugenehmigung, Fluchtlinie und ein Director Responsable de Obra &mdash; und bei einem erschlossenen Wohngrundst&uuml;ck ist das einer der berechenbarsten Abl&auml;ufe im Bundesstaat.</p>"""),
  ("Schlüsselfertige Kosten nach Hausgröße",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Hausgr&ouml;&szlig;e</th><th>Schl&uuml;sselfertig (MXN)</th><th>Schl&uuml;sselfertig (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.65M&ndash;$2M</td><td>$92k&ndash;$111k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.48M&ndash;$3M</td><td>$138k&ndash;$167k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.30M&ndash;$4M</td><td>$183k&ndash;$222k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.13M&ndash;$5M</td><td>$229k&ndash;$278k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referenz: $16,500&ndash;$20,000 MXN/m&sup2; Standardausbau. USD/MXN &asymp; 18. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<p>Diese Spannen gelten f&uuml;r das Wohn-Canc&uacute;n im Inland. Ein Grundst&uuml;ck in der Zona Hotelera, auf Isla Dorada oder mit Meer- oder Lagunenfront ist ein anderes Geb&auml;ude: durchgehend Marine-Spezifikation, Fragen der Bundeszone und ein Ausbauniveau, das der Ort verlangt. Dort sind $26,000&ndash;$40,000 MXN/m&sup2; realistisch.</p>"""),
  ("Wo die Ersparnis zum Risiko wird",
   """<p>Ein gro&szlig;er, umk&auml;mpfter Markt erzeugt niedrige Preise und enorme Qualit&auml;tsunterschiede. Das Problem in Canc&uacute;n ist nicht der teure Bau, sondern der billige.</p>
<ul>
<li><strong>Angebote unter etwa $14,000 MXN/m&sup2;</strong> sparen an etwas Strukturellem &mdash; meist Bewehrungsdichte, Betonqualit&auml;t oder Elektroinstallation. In einer Starkwindregion ist der Bewehrungsstahl der falsche Posten.</li>
<li><strong>Kein Bodengutachten.</strong> Der Karst kann hervorragende Tragf&auml;higkeit bieten und zwei Meter weiter einen Hohlraum. Sondierungen &uuml;ber der tats&auml;chlichen Grundfl&auml;che kosten $25,000&ndash;$60,000 und sind die g&uuml;nstigste Risikominderung im Projekt.</li>
<li><strong>Regeln der Wohnanlage.</strong> Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua und Palmaris betreiben Gestaltungsbeir&auml;te mit eigenen Vorgaben zu H&ouml;he, Abst&auml;nden, Materialien und Farben, dazu Arbeiterregistrierung, eingeschr&auml;nkte Arbeitszeiten und eine Baukaution. Reichen Sie in der Entwurfsphase ein.</li>
<li><strong>Verkehr und Lieferfenster.</strong> Canc&uacute;n ist der einzige Ort im Korridor, an dem St&auml;dteverkehr ein Terminthema ist: Lieferungen in Wohnanlagen im Inland brauchen Zeitfenster, und Zeitbeschr&auml;nkungen versch&auml;rfen das.</li>
<li><strong>Salz erreicht auch das Inland.</strong> Selbst mehrere Kilometer vom Meer halten Befestigungen, Gel&auml;nder und Verfl&uuml;ssigerlamellen in 316er Edelstahl und Marine-Beschichtung deutlich l&auml;nger.</li>
</ul>
<p>Ein 150-m&sup2;-Haus dauert etwa <strong>7&ndash;10 Monate</strong> von der Genehmigung bis zur &Uuml;bergabe, und die Lieferantendichte verhindert einen Teil der Materialwartezeiten, die Projekte weiter s&uuml;dlich verl&auml;ngern. Bestehen Sie auf einem Festpreisvertrag mit Positionsbudget und Zahlungen nach gepr&uuml;ftem Baufortschritt.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Cancún 2026?",
   "Etwa $2.48M&ndash;$3M MXN ($138k&ndash;$167k USD) schl&uuml;sselfertig f&uuml;r 150 m&sup2; mit Standardausbau auf einem Wohngrundst&uuml;ck im Inland, ohne Grundst&uuml;ck, Pool und M&ouml;bel &mdash; rund $16,500&ndash;$20,000 MXN/m&sup2;."),
  ("Warum ist Cancún günstiger als Playa del Carmen oder Tulum?",
   "Wegen der Marktgr&ouml;&szlig;e: der gr&ouml;&szlig;te Arbeitskr&auml;ftepool des Korridors, die h&ouml;chste Lieferantendichte und echter Wettbewerb unter Bauunternehmen. Zudem wird &uuml;berwiegend im Inland gebaut, was Bundesk&uuml;stenzone, Schildkr&ouml;tenregeln und die schwerere Umweltakte eines K&uuml;stengrundst&uuml;cks vermeidet."),
  ("Gilt dieser Preis auch in der Zona Hotelera?",
   "Nein. Zona Hotelera, Isla Dorada oder jede Meer- und Lagunenfront bedeutet durchgehende Marine-Spezifikation, Fragen der Bundeszone und ein h&ouml;heres Ausbauniveau &mdash; kalkulieren Sie dort $26,000&ndash;$40,000 MXN/m&sup2;."),
  ("Wie niedrig darf ein Angebot in Cancún sein?",
   "Betrachten Sie alles unter etwa $14,000 MXN/m&sup2; als Warnsignal. Zu diesem Preis wird an etwas Strukturellem gespart &mdash; Bewehrungsdichte, Betonqualit&auml;t oder Elektroinstallation &mdash; und das sind in einer Starkwindregion die falschen Einsparungen."),
  ("Verteuern geschlossene Wohnanlagen den Bau?",
   "Ja. Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua und Palmaris haben eigene Gestaltungsbeir&auml;te mit Vorgaben zu H&ouml;he, Abst&auml;nden, Materialien und Farbe, dazu Arbeiterregistrierung, eingeschr&auml;nkte Arbeitszeiten und eine Kaution. Planen Sie den Pr&uuml;fzyklus ein, nicht nur die Geb&uuml;hren."),
 ],
}

Z[("de","puerto-aventuras")] = {
 "title": "Hausbau-Kosten in Puerto Aventuras 2026: Das Ganze Budget",
 "desc": "Schlüsselfertige Baukosten in Puerto Aventuras plus die Posten der Marina-Gemeinde, die Käufer übersehen: HOA, Liegeplatz, Ufermauer, Gestaltungsbeirat.",
 "lead": "Ein 150-m&sup2;-Haus in <strong>Puerto Aventuras</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD)</strong>, etwa 8% &uuml;ber Playa del Carmen. Der Bau ist der berechenbare Teil; die Posten darunter sind, wo Budgets in einer Marina-Gemeinde kippen.",
 "sections": [
  ("Schlüsselfertige Kosten nach Hausgröße",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Hausgr&ouml;&szlig;e</th><th>Schl&uuml;sselfertig (MXN)</th><th>Schl&uuml;sselfertig (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.85M&ndash;$2.25M</td><td>$103k&ndash;$125k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.77M&ndash;$3.38M</td><td>$154k&ndash;$188k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.70M&ndash;$4.50M</td><td>$206k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.63M&ndash;$5.63M</td><td>$257k&ndash;$313k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referenz: $18,500&ndash;$22,500 MXN/m&sup2; Standardausbau. USD/MXN &asymp; 18. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<p>Die 8% gegen&uuml;ber Playa del Carmen sind vier konkrete Dinge und kein Zuschlag f&uuml;r die Adresse: kontrollierter Baustellenzugang mit Arbeiterregistrierung, eingeschr&auml;nkte Arbeitszeiten, l&auml;ngere Materialwege innerhalb der Anlage und die Marine-Spezifikation, die Kanal- und k&uuml;stennahe Lagen verlangen.</p>"""),
  ("Die Posten, die vergessen werden",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Posten</th><th>Was zu klären ist</th></tr></thead><tbody>
<tr><td><strong>HOA-Geb&uuml;hr</strong></td><td>Der aktuelle Betrag f&uuml;r genau dieses Grundst&uuml;ck, das zugrunde liegende Budget und die F&uuml;nfjahresentwicklung. Kanal- und marinanahe Lagen zahlen oft mehr.</td></tr>
<tr><td><strong>Liegeplatz</strong></td><td>Ob im Eigentum, gepachtet oder zugewiesen &mdash; rechtlich und beim Wiederverkauf drei verschiedene Dinge &mdash; und die j&auml;hrlichen Kosten. Steganlagen werden getrennt vom Haus genehmigt.</td></tr>
<tr><td><strong>Ufer- bzw. Kanalmauer</strong></td><td>Zustand, gepr&uuml;ft von jemandem, der Ihnen die Immobilie nicht verkauft. Eine Sanierung ist ein eigenes Projekt.</td></tr>
<tr><td><strong>Gestaltungsbeirat</strong></td><td>Einreichung, Pr&uuml;fzyklus und Baukaution: $60,000&ndash;$250,000 MXN und mindestens eine Pr&uuml;frunde im Terminplan.</td></tr>
<tr><td><strong>Marine-Spezifikation</strong></td><td>316er Befestigungen, eloxiertes oder marinebeschichtetes Aluminium, gr&ouml;&szlig;ere Betondeckung. Verteuert den Bau und spart &uuml;ber ein Jahrzehnt ein Vielfaches.</td></tr>
</tbody></table></div>
<p>Genehmigt wird in der Gemeinde <strong>Solidaridad</strong> &mdash; derselbe Weg wie in Playa del Carmen &mdash; wobei die Architekturpr&uuml;fung der Gemeinschaft in der Praxis davor liegt.</p>"""),
  ("Kanallage: was sich technisch ändert",
   """<ul>
<li><strong>Hoher Grundwasserstand.</strong> Aush&uuml;be, Zisterne und Poolbecken brauchen Wasserhaltung und Auftriebsnachweis &mdash; ein zum falschen Zeitpunkt entleerter Pool kann aufschwimmen.</li>
<li><strong>St&auml;ndiges Salzaerosol</strong> vom Wasser, keine saisonale Belastung. Hier ist 316er Edelstahl keine Vorliebe mehr.</li>
<li><strong>Sturmexposition.</strong> Wassernahe Grundst&uuml;cke nehmen die volle Windlast und bei einem schweren Ereignis auch Sturmflut. Verbund- oder schlagfestes Glas zur Wasserseite ist die Spezifikation, bei der wir nicht nachgeben.</li>
<li><strong>Uferbauwerke</strong> an der Wasserlinie haben eigene Planungs- und Genehmigungsanforderungen.</li>
</ul>
<p>Ein 150-m&sup2;-Haus dauert etwa <strong>7&ndash;10 Monate</strong> ab Genehmigung, und die eingeschr&auml;nkten Arbeitszeiten schieben den Terminplan ans obere Ende. Vertraglich Festpreis mit Positionsbudget und Zahlungen nach gepr&uuml;ftem Fortschritt.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Puerto Aventuras?",
   "Etwa $2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD) schl&uuml;sselfertig f&uuml;r 150 m&sup2; mit Standardausbau, ohne Grundst&uuml;ck, Pool und M&ouml;bel &mdash; rund $18,500&ndash;$22,500 MXN/m&sup2;, etwa 8% &uuml;ber Playa del Carmen."),
  ("Warum ist es teurer als Playa del Carmen?",
   "Vier konkrete Gr&uuml;nde: kontrollierter Zugang mit Arbeiterregistrierung, eingeschr&auml;nkte Arbeitszeiten, l&auml;ngere Materialwege in der Anlage und die Marine-Spezifikation f&uuml;r Kanal- und k&uuml;stennahe Lagen."),
  ("Welche Kosten liegen außerhalb des Baubudgets?",
   "Die HOA-Geb&uuml;hr f&uuml;r das konkrete Grundst&uuml;ck, eine etwaige Liegeplatzgeb&uuml;hr, die Sanierung der Ufermauer bei schlechtem Zustand sowie Einreichung und Kaution beim Gestaltungsbeirat mit rund $60,000&ndash;$250,000 MXN. Steganlagen werden separat genehmigt."),
  ("Brauche ich neben der Gemeinde auch die Zustimmung der Anlage?",
   "Ja, und praktisch kommt die Anlage zuerst. Baugenehmigung und DRO laufen &uuml;ber Solidaridad, w&auml;hrend der Architekturbeirat H&ouml;he, Abst&auml;nde, Materialien, Farben und Einfriedungen pr&uuml;ft. Reichen Sie in der Entwurfsphase ein."),
  ("Was ändert sich bei einem Kanalgrundstück?",
   "Wasserhaltung und Auftriebsnachweis f&uuml;r Aush&uuml;be und Pool, durchgehende Marine-Spezifikation wegen des st&auml;ndigen Salzaerosols, schlagfestes Glas zur Wasserseite wegen der Sturmexposition und eine separate Genehmigung f&uuml;r Bauwerke an der Wasserlinie."),
 ],
}

Z[("de","akumal")] = {
 "title": "Hausbau-Kosten in Akumal 2026: Die Umweltakte Entscheidet",
 "desc": "Baukosten in Akumal 2026 und warum die Umwelt- und Genehmigungsakte — nicht die Mauern — die Endsumme bestimmt. Schildkröten, Kläranlage, Transport.",
 "lead": "Ein 150-m&sup2;-Haus in <strong>Akumal</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD)</strong>. Auf einem Akumal-Grundst&uuml;ck ist der Bau jedoch die berechenbare H&auml;lfte: Umweltakte, Kl&auml;ranlage und Genehmigungskalender trennen zwei scheinbar gleiche Projekte.",
 "sections": [
  ("Schlüsselfertige Kosten nach Hausgröße",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Hausgr&ouml;&szlig;e</th><th>Schl&uuml;sselfertig (MXN)</th><th>Schl&uuml;sselfertig (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.90M&ndash;$2.35M</td><td>$106k&ndash;$131k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.85M&ndash;$3.52M</td><td>$158k&ndash;$196k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.80M&ndash;$4.70M</td><td>$211k&ndash;$261k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.75M&ndash;$5.88M</td><td>$264k&ndash;$326k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referenz: $19,000&ndash;$23,500 MXN/m&sup2; Standardausbau. USD/MXN &asymp; 18. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<p>Das sind etwa 12% &uuml;ber Playa del Carmen: Transport jedes Materials den Korridor hinunter, Marine-Spezifikation wegen der Salzbelastung und eine kleinere lokale Gewerkebasis, die Anfahrten n&ouml;tig macht.</p>"""),
  ("Posten, die es nur in Akumal gibt",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Posten</th><th>MXN</th><th>Warum</th></tr></thead><tbody>
<tr><td>Umweltgutachten und Genehmigung</td><td>$80,000&ndash;$350,000</td><td>Umfang bestimmt die Vegetation und die K&uuml;stenn&auml;he, nicht die Hausgr&ouml;&szlig;e</td></tr>
<tr><td>Kl&auml;ranlage + Sickerbrunnen</td><td>$120,000&ndash;$380,000</td><td>Keine Kanalisation; Reinigung vor Versickerung ist der Kern der Akte</td></tr>
<tr><td>Schildkr&ouml;tenkonforme Beleuchtung</td><td>$30,000&ndash;$120,000</td><td>Niedrig, abgeschirmt, bernstein- oder rotfarben zur Strandseite</td></tr>
<tr><td>ZOFEMAT-Vermessung und Konzessionspr&uuml;fung</td><td>$20,000&ndash;$80,000</td><td>Nur bei Grundst&uuml;cken in der Bundesk&uuml;stenzone</td></tr>
<tr><td>Bodengutachten &uuml;ber der Grundfl&auml;che</td><td>$25,000&ndash;$60,000</td><td>Karst: ein Hohlraum kann zwei Meter neben guter Tragf&auml;higkeit liegen</td></tr>
</tbody></table></div>
<p>Vier dieser f&uuml;nf Posten skalieren mit dem <em>Grundst&uuml;ck</em>, nicht mit dem Haus. Deshalb ist ein kompaktes Haus in Akumal pro Quadratmeter teurer als ein gro&szlig;es &mdash; und deshalb ist ein Grundst&uuml;ck mit bestehender Umweltgenehmigung und Anschl&uuml;ssen an der Grenze die g&uuml;nstigste Ersparnis, die es hier gibt.</p>"""),
  ("Der Genehmigungskalender und was Warten kostet",
   """<p>Akumal geh&ouml;rt zur Gemeinde <strong>Tulum</strong>, nicht zu Solidaridad &mdash; das &uuml;berrascht viele, weil Playa del Carmen n&auml;her liegt. Tulums Pr&uuml;fung ist die umweltrechtlich anspruchsvollste im Korridor, und die Folge ist Zeit:</p>
<ul>
<li><strong>Umweltakte:</strong> 4&ndash;9 Monate bei bewachsenem oder k&uuml;stennahem Grundst&uuml;ck.</li>
<li><strong>Genehmigungspr&uuml;fung bei vollst&auml;ndiger Akte:</strong> 4&ndash;12 Wochen.</li>
<li><strong>Realistisch vom Kauf bis zum Baubeginn:</strong> 6&ndash;14 Monate.</li>
</ul>
<p>Diese Monate sind ein realer Kostenblock: gebundenes Grundst&uuml;ck und gebundenes Kapital ohne Ertrag. Sie sind auch der Grund, warum ein Grundst&uuml;ck mit sauberer bestehender Genehmigung einen Aufpreis hat &mdash; meist zu Recht.</p>
<p>Ein Terminpunkt speziell f&uuml;r diesen K&uuml;stenabschnitt: Die Schildkr&ouml;tensaison l&auml;uft etwa von <strong>Mai bis Oktober</strong> und beschr&auml;nkt schwere Arbeiten, starke Beleuchtung und Aktivit&auml;t am Strand. Legen Sie laute Au&szlig;enphasen au&szlig;erhalb dieses Fensters und den Innenausbau hinein.</p>
<p>Die Bauzeit betr&auml;gt etwa <strong>7&ndash;10 Monate</strong> f&uuml;r 150 m&sup2;. Festpreisvertrag mit Positionsbudget &mdash; und die Umweltauflagen (Anwuchskontrolle, Betriebsbuch der Kl&auml;ranlage, Beleuchtung) geh&ouml;ren nach der &Uuml;bergabe in jemandes Verantwortung, denn sie gelten lebenslang.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Akumal 2026?",
   "Etwa $2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD) schl&uuml;sselfertig f&uuml;r 150 m&sup2; mit Standardausbau &mdash; rund $19,000&ndash;$23,500 MXN/m&sup2;, etwa 12% &uuml;ber Playa del Carmen. Grundst&uuml;ck, Pool, M&ouml;bel und die Umweltposten kommen hinzu."),
  ("Welche Zusatzkosten hat ein Grundstück in Akumal?",
   "Umweltgutachten und Genehmigung $80,000&ndash;$350,000, Kl&auml;ranlage mit Sickerbrunnen $120,000&ndash;$380,000, schildkr&ouml;tenkonforme Beleuchtung $30,000&ndash;$120,000, ZOFEMAT-Vermessung $20,000&ndash;$80,000 und Bodengutachten $25,000&ndash;$60,000. Die meisten skalieren mit dem Grundst&uuml;ck, nicht mit dem Haus."),
  ("Welche Gemeinde erteilt die Genehmigung für Akumal?",
   "Tulum, nicht Solidaridad, obwohl Playa del Carmen n&auml;her liegt. Die Umweltpr&uuml;fung dort ist die anspruchsvollste im Korridor, weshalb 6&ndash;14 Monate vom Kauf bis zum Baubeginn realistisch sind."),
  ("Beeinflussen die Schildkrötenregeln den Bauablauf?",
   "Ja. Die Saison l&auml;uft etwa von Mai bis Oktober und beschr&auml;nkt schwere Arbeiten, starke Beleuchtung und Aktivit&auml;t am Strand. Laute Au&szlig;enphasen geh&ouml;ren au&szlig;erhalb der Saison, der Innenausbau hinein. Die Beleuchtungsregeln gelten auch f&uuml;r das fertige Haus."),
  ("Ist ein kleineres Haus pro m² günstiger?",
   "Nein, teurer. Umweltakte, Bodengutachten, Kl&auml;ranlage und Hausanschluss kosten f&uuml;r 80 m&sup2; fast dasselbe wie f&uuml;r 200 m&sup2;, sodass diese Fixposten bei einem kompakten Haus einen viel gr&ouml;&szlig;eren Anteil ausmachen."),
 ],
}

Z[("de","puerto-morelos")] = {
 "title": "Hausbau-Kosten in Puerto Morelos 2026: Das Beste Verhältnis",
 "desc": "Puerto Morelos baut zu Playa-del-Carmen-Preisen auf günstigerem Land. Die Spannen 2026, die Einleitungsvorgaben am Riffpark und die Ruta de los Cenotes.",
 "lead": "Ein 150-m&sup2;-Haus in <strong>Puerto Morelos</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD)</strong> &mdash; beim Bau praktisch auf dem Niveau von Playa del Carmen, auf meist g&uuml;nstigerem Grund. Diese Kombination macht den Ort zum stillen Preis-Leistungs-Sieger des Korridors.",
 "sections": [
  ("Kosten nach Hausgröße und die drei Teilmärkte",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Hausgr&ouml;&szlig;e</th><th>Schl&uuml;sselfertig (MXN)</th><th>Schl&uuml;sselfertig (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.70M&ndash;$2.10M</td><td>$94k&ndash;$117k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.55M&ndash;$3.15M</td><td>$142k&ndash;$175k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.40M&ndash;$4.20M</td><td>$189k&ndash;$233k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.25M&ndash;$5.25M</td><td>$236k&ndash;$292k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referenz: $17,000&ndash;$21,000 MXN/m&sup2; Standardausbau. USD/MXN &asymp; 18. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<ul>
<li><strong>Strandnah:</strong> $26,000&ndash;$38,000+ MXN/m&sup2; mit Marine-Spezifikation und schwererer Umweltakte.</li>
<li><strong>Ruta de los Cenotes:</strong> $14,000&ndash;$19,000 auf erschlossenem Grundst&uuml;ck, $17,000&ndash;$24,000 netzunabh&auml;ngig &mdash; billigeres Land, mehr Infrastruktur.</li>
</ul>"""),
  ("Eigene Gemeinde seit 2016",
   """<p>Puerto Morelos hat sich 2016 von Benito Ju&aacute;rez getrennt und erteilt heute eigene Nutzungszertifikate, Baugenehmigungen, Fluchtlinien und Abnahmen. Drei praktische Folgen:</p>
<ul>
<li><strong>Eingereicht wird hier, nicht in Canc&uacute;n.</strong> Ratschl&auml;ge nach Benito-Ju&aacute;rez-Praxis sind &uuml;berholt &mdash; ebenso die Erfahrung eines Nachbarn von vor 2016.</li>
<li><strong>Pr&uuml;fen Sie die Kennzahlen aktuell.</strong> Die Planungsinstrumente der Gemeinde sind noch jung und wurden fortgeschrieben: Dichte, H&ouml;he und zul&auml;ssige Nutzung f&uuml;r genau dieses Grundst&uuml;ck best&auml;tigen lassen.</li>
<li><strong>Eine kleine Verwaltung ist eine direkte.</strong> Die pr&uuml;fende Stelle ist erreichbar, was eine vollst&auml;ndige Einreichung besonders wertvoll und eine unvollst&auml;ndige besonders langsam macht.</li>
</ul>
<p>Landesumweltpr&uuml;fung (SEMA), Bundeszust&auml;ndigkeit wo einschl&auml;gig, CONAGUA f&uuml;r Wasser und ZOFEMAT strandseitig gelten unver&auml;ndert.</p>"""),
  ("Was Riff und Feuchtgebiete zur Spezifikation beitragen",
   """<ul>
<li><strong>Die Einleitqualit&auml;t ist der Kern der Akte.</strong> Reinigung vor Versickerung, richtig dimensioniert, mit separat gef&uuml;hrtem Poolr&uuml;cksp&uuml;lwasser &mdash; $90,000&ndash;$350,000 MXN je nach Belegung. Was hier versickert, erreicht den Aquifer und dann das Riff.</li>
<li><strong>Mangroven sind nicht verhandelbar.</strong> Bei feuchtgebietsnahen Grundst&uuml;cken muss die Grenze der gesch&uuml;tzten Vegetation vor dem ersten Grundriss feststehen &mdash; manche angebotenen Grundst&uuml;cke haben deutlich weniger bebaubare Fl&auml;che als die Grundbuchfl&auml;che vermuten l&auml;sst.</li>
<li><strong>Cenote-Abst&auml;nde</strong> gelten im Inland, mit Auflagen dazu, was in ihrer N&auml;he versickern darf.</li>
<li><strong>Die H&ouml;he des Erdgeschossniveaus</strong> in tief liegendem Gel&auml;nde ist eine Entwurfsentscheidung gegen Hochwasser und Sturmflut &mdash; sp&auml;ter nicht korrigierbar.</li>
<li><strong>An der Ruta de los Cenotes</strong> kalkulieren Sie die Zufahrt ($40,000&ndash;$300,000) und entweder eine CFE-Erweiterung &mdash; vor dem Kauf anfragen, $150,000 bis &uuml;ber $900,000 &mdash; oder ein geplantes Inselsystem mit Solar, Speicher, aufbereitetem Brunnen und Regenwasser.</li>
</ul>
<p>Die Bauzeit betr&auml;gt etwa <strong>7&ndash;10 Monate</strong> f&uuml;r 150 m&sup2;.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Puerto Morelos?",
   "Etwa $2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD) schl&uuml;sselfertig f&uuml;r 150 m&sup2; im Ort oder im Inland &mdash; rund $17,000&ndash;$21,000 MXN/m&sup2;, praktisch auf dem Niveau von Playa del Carmen. Strandnah $26,000&ndash;$38,000+, Ruta de los Cenotes $14,000&ndash;$24,000 je nach Erschlie&szlig;ung."),
  ("Welche Gemeinde genehmigt in Puerto Morelos?",
   "Puerto Morelos selbst &mdash; die Trennung von Benito Ju&aacute;rez (Canc&uacute;n) erfolgte 2016. Auskunft nach Canc&uacute;n-Praxis ist &uuml;berholt, und da die Planungsinstrumente jung sind, sollten Dichte, H&ouml;he und zul&auml;ssige Nutzung aktuell gepr&uuml;ft werden."),
  ("Darf ich neben Mangroven bauen?",
   "Nicht in der gesch&uuml;tzten Vegetation, und deren Grenze muss vor dem Grundriss feststehen. Manche angebotenen Grundst&uuml;cke haben erheblich weniger bebaubare Fl&auml;che als die Grundbuchfl&auml;che &mdash; das geh&ouml;rt vor den Kauf gepr&uuml;ft."),
  ("Was bedeutet der Riff-Nationalpark für meinen Bau?",
   "Dass die Einleitqualit&auml;t die zentrale technische Frage der Umweltakte ist. Reinigung vor Versickerung, auf die Belegung dimensioniert, mit separat gef&uuml;hrtem Poolr&uuml;cksp&uuml;lwasser, kostet $90,000&ndash;$350,000 MXN und wird genau gepr&uuml;ft."),
  ("Ist die Ruta de los Cenotes günstiger?",
   "Das Land ja, und der Bau liegt bei $14,000&ndash;$19,000 MXN/m&sup2; auf erschlossenem Grundst&uuml;ck. Viele Parzellen haben aber weder CFE noch Wasser: kalkulieren Sie die Netzerweiterung &mdash; vor dem Kauf anfragen, $150,000 bis &uuml;ber $900,000 &mdash; oder ein Inselsystem, plus $40,000&ndash;$300,000 Zufahrt."),
 ],
}

Z[("de","playacar")] = {
 "title": "Hausbau-Kosten in Playacar 2026: Abriss Oder Sanierung",
 "desc": "Playacar ist bebaut — die meisten Projekte sind Sanierung oder Neubau nach Abriss. Spannen 2026, Abrisskosten, Gestaltungsbeirat, Phase I gegen Phase II.",
 "lead": "Ein 150-m&sup2;-Haus in <strong>Playacar</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD)</strong>, etwa 25% &uuml;ber dem Basisniveau von Playa del Carmen. Playacar ist jedoch praktisch bebaut &mdash; die eigentliche Frage lautet daher nicht, was ein Neubau kostet, sondern ob das Bestandshaus saniert oder abgerissen wird.",
 "sections": [
  ("Sanieren oder abreißen: die Rechnung",
   """<p>Fast jedes Projekt in Playacar ist ein Neubau nach Abriss, eine gro&szlig;e Sanierung oder eine Bebauung eines der wenigen verbliebenen Grundst&uuml;cke. Die Entscheidung zwischen den ersten beiden geh&ouml;rt hinter ein Gutachten, nicht hinter eine Besichtigung: H&auml;user dieses Alters an dieser K&uuml;ste tragen einen vorhersehbaren Schaden &mdash; chloridinduzierte Bewehrungskorrosion an Deckenr&auml;ndern, Balkonen, St&uuml;tzen und Attiken.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Position</th><th>MXN</th></tr></thead><tbody>
<tr><td>Zustandsgutachten mit &Ouml;ffnungen an repr&auml;sentativen Stellen</td><td>$40,000&ndash;$150,000</td></tr>
<tr><td>Abriss und Schuttentsorgung, typisches Haus</td><td>$180,000&ndash;$600,000</td></tr>
<tr><td>Betoninstandsetzungsprogramm bei Erhalt</td><td>Nach Gutachten &mdash; kann den Abriss &uuml;bersteigen</td></tr>
<tr><td>Kernsanierung, Premium-Ausbau</td><td>$14,000&ndash;$26,000 MXN/m&sup2;</td></tr>
<tr><td>Neubau, Premium</td><td>$24,000&ndash;$30,000 MXN/m&sup2;</td></tr>
<tr><td>Neubau, Luxus</td><td>$30,000&ndash;$42,000 MXN/m&sup2;</td></tr>
</tbody></table></div>
<p>Die ehrliche Schwelle: Sobald die Instandsetzung etwa 25&ndash;30% der Neubaukosten erreicht, zahlen Sie Neubaupreise f&uuml;r Raumh&ouml;hen, Ausrichtung und Grundriss eines alten Geb&auml;udes. In Playacar gibt es allerdings ein echtes Gegenargument: Die Grundst&uuml;cke sind nicht ersetzbar, alter Baumbestand ist gesch&uuml;tzt und wertvoll, und ein solides Haus der Neunziger mit gro&szlig;z&uuml;giger H&ouml;he in Phase II kann erhaltenswert sein.</p>"""),
  ("Schlüsselfertige Kosten nach Hausgröße",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Hausgr&ouml;&szlig;e</th><th>Schl&uuml;sselfertig (MXN)</th><th>Schl&uuml;sselfertig (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.10M&ndash;$2.60M</td><td>$117k&ndash;$144k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.15M&ndash;$3.90M</td><td>$175k&ndash;$217k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.20M&ndash;$5.20M</td><td>$233k&ndash;$289k</td></tr>
<tr><td>250 m&sup2;</td><td>$5.25M&ndash;$6.50M</td><td>$292k&ndash;$361k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referenz: $21,000&ndash;$26,000 MXN/m&sup2; Standard- bis Premium-Ausbau. USD/MXN &asymp; 18. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<p>Die 25% &uuml;ber dem Basisniveau sind eingeschr&auml;nkter Zugang &uuml;ber enge Stra&szlig;en, registrierte Arbeiter und begrenzte Arbeitszeiten, das Verfahren des Gestaltungsbeirats, Baumschutz, Marine-Spezifikation und das erwartete Ausbauniveau. Bei einem Strandgrundst&uuml;ck in Playacar kommen Bundesk&uuml;stenzone und schlagfestes Glas zur Meerseite hinzu: dort $42,000&ndash;$60,000+ MXN/m&sup2;.</p>"""),
  ("Beirat, Bäume und Phase I gegen Phase II",
   """<p><strong>Die Architekturpr&uuml;fung ist real</strong> und dort verlieren Playacar-Terminpl&auml;ne Zeit. Erwartet werden Pr&uuml;fungen von H&ouml;he, Baumasse und Abst&auml;nden &uuml;ber das gemeindliche Ma&szlig; hinaus, Dachform und Materialien, Fassade und Farbe, Mauern und Z&auml;une und vor allem Baumf&auml;llungen &mdash; jeder Baum muss begr&uuml;ndet werden. Reichen Sie in der Entwurfsphase mit Baumkataster ein und planen Sie mindestens eine Pr&uuml;frunde plus Kaution ein.</p>
<p><strong>Phase I und Phase II sind verschiedene Orte.</strong> Phase I liegt n&auml;her am Ort und an der F&auml;hre: dichter, kleinere Grundst&uuml;cke, echte Fu&szlig;l&auml;ufigkeit zur Quinta Avenida und Baustellenzufahrt &uuml;ber enge Stra&szlig;en, was verteuert. Phase II ist gr&ouml;&szlig;er und ruhiger am Golfplatz, mit gro&szlig;en Grundst&uuml;cken, altem Bewuchs und Platz f&uuml;r eine gr&ouml;&szlig;ere Villa &mdash; und Golflage macht Verglasung und Oberlichter zu einem kalkulierbaren Thema.</p>
<p>Genehmigt wird in <strong>Solidaridad</strong>, der Bau dauert etwa <strong>7&ndash;10 Monate</strong> f&uuml;r 150 m&sup2;, zuz&uuml;glich Abriss.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Playacar?",
   "Etwa $3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD) schl&uuml;sselfertig f&uuml;r 150 m&sup2; &mdash; rund $21,000&ndash;$26,000 MXN/m&sup2;, etwa 25% &uuml;ber dem Basisniveau von Playa del Carmen. Luxusausbau $30,000&ndash;$42,000, Strandgrundst&uuml;cke $42,000&ndash;$60,000+."),
  ("Sanieren oder abreißen?",
   "Zuerst ein Gutachten mit &Ouml;ffnungen an repr&auml;sentativen Stellen f&uuml;r $40,000&ndash;$150,000 MXN, denn H&auml;user dieses Alters tragen h&auml;ufig chloridinduzierte Bewehrungskorrosion. Erreicht die Instandsetzung 25&ndash;30% der Neubaukosten, ist Abriss meist die bessere Entscheidung; Abbruch und Entsorgung kosten $180,000&ndash;$600,000."),
  ("Was prüft der Gestaltungsbeirat in Playacar?",
   "H&ouml;he, Baumasse und Abst&auml;nde &uuml;ber das gemeindliche Ma&szlig; hinaus, Dachform und Materialien, Fassade und Farbe, Mauern und Z&auml;une sowie jede Baumf&auml;llung. Dazu kommen Bauregeln: registrierte Arbeiter, Arbeitszeiten, Lieferungen, Lagerung und eine Kaution."),
  ("Was unterscheidet Phase I von Phase II beim Bauen?",
   "Phase I hat kleinere, dichtere Grundst&uuml;cke mit verteuernder Baustellenzufahrt &uuml;ber enge Stra&szlig;en und echte Fu&szlig;l&auml;ufigkeit zur Quinta Avenida. Phase II bietet gro&szlig;e Grundst&uuml;cke am Golfplatz mit altem Bewuchs &mdash; und Golflage macht Verglasung und Oberlichter zum praktischen Thema."),
  ("Warum kostet Playacar 25% mehr?",
   "Eingeschr&auml;nkter Zugang &uuml;ber enge Stra&szlig;en, registrierte Arbeiter und begrenzte Arbeitszeiten, das Beiratsverfahren, Baumschutz w&auml;hrend der Bauzeit, Marine-Spezifikation und das erwartete Ausbauniveau &mdash; jeweils reale Positionen, kein Adresszuschlag."),
 ],
}

Z[("de","mayakoba")] = {
 "title": "Hausbau-Kosten in Mayakoba 2026: Die Obergrenze",
 "desc": "Mayakoba ist der teuerste Bauort der Riviera Maya. Die m²-Spannen 2026, was die Resort-Spezifikation tatsächlich umfasst und warum.",
 "lead": "Ein 150-m&sup2;-Haus in <strong>Mayakoba</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD)</strong> &mdash; die h&ouml;chste Spanne im Korridor, etwa 42% &uuml;ber dem Basisniveau von Playa del Carmen. Am unteren Rand wird hier allerdings kaum gebaut, und diese Seite erkl&auml;rt, warum.",
 "sections": [
  ("Kosten nach Hausgröße und die realistische Zahl",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Hausgr&ouml;&szlig;e</th><th>Schl&uuml;sselfertig (MXN)</th><th>Schl&uuml;sselfertig (USD)</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.60M&ndash;$4.50M</td><td>$200k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$6M&ndash;$7.50M</td><td>$333k&ndash;$417k</td></tr>
<tr><td>350 m&sup2;</td><td>$8.40M&ndash;$10.50M</td><td>$467k&ndash;$583k</td></tr>
<tr><td>500 m&sup2;</td><td>$12M&ndash;$15M</td><td>$667k&ndash;$833k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referenz: $24,000&ndash;$30,000 MXN/m&sup2; Standard- bis Premium-Ausbau. USD/MXN &asymp; 18. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<p>Das ist die Einstiegsspanne. Tats&auml;chlich entstehen im Masterplan H&auml;user von 300&ndash;600 m&sup2; in Autorenqualit&auml;t, was reale Werte von <strong>$35,000&ndash;$55,000 MXN/m&sup2;</strong> bedeutet, sobald Architektenleistung, importierte Ausstattung, Vollautomation, geplanter Pool und ausgewachsene Bepflanzung eingerechnet sind. Wer eine Mayakoba-Villa mit $24,000 kalkuliert, kalkuliert ein Haus, das die Gestaltungspr&uuml;fung nicht best&uuml;nde.</p>"""),
  ("Was der Aufpreis tatsächlich kauft",
   """<ul>
<li><strong>Gestaltungskontrolle.</strong> Ein um den Resortbetrieb herum entwickelter Masterplan pr&uuml;ft Architektur, Materialien, Farbe, Freianlagen und Beleuchtung am Ma&szlig;stab der benachbarten Hotels. Einreichungen sind detailliert, Pr&uuml;fzyklen real, und die Fassade zu verbilligen steht nicht zur Wahl.</li>
<li><strong>Ausbauerwartung.</strong> Die Vergleichsobjekte sind Branded Residences. Tischlerarbeiten, Naturstein, Verglasung und Beschl&auml;ge werden danach spezifiziert &mdash; und die pr&auml;zise Montage kostet mehr als das Material.</li>
<li><strong>Baustellendisziplin.</strong> Gebaut wird in einer laufenden Luxusumgebung: kontrollierter Zugang, registrierte Arbeiter, begrenzte Zeiten, abgeschirmte Bauz&auml;une, L&auml;rmgrenzen, Reinigungspflichten und Kaution. Jeder Punkt kostet Bauzeit.</li>
<li><strong>Naturraum.</strong> Der Masterplan ist um Lagunen, Kan&auml;le und Mangroven organisiert. Erhaltene Vegetation, Abst&auml;nde, Entw&auml;sserung und Einleitung werden zus&auml;tzlich auf Gemeinschaftsebene gesteuert.</li>
<li><strong>Marine- und Feuchtespezifikation</strong> durchgehend: 316er Edelstahl, eloxiertes oder marinebeschichtetes Aluminium, gro&szlig;z&uuml;gige Betondeckung, hinterl&uuml;ftete Einbauten.</li>
<li><strong>Knappheit.</strong> Wenige Wohngrundst&uuml;cke, jedes Projekt ein Einzelst&uuml;ck &mdash; keine Wiederholung, auf die sich Planungs- und Bauleitungskosten verteilen lie&szlig;en.</li>
</ul>"""),
  ("Ablauf, Genehmigungen und was zusätzlich zu budgetieren ist",
   """<p>Genehmigt wird in der Gemeinde <strong>Solidaridad</strong>, mit der Architekturpr&uuml;fung der Gemeinschaft davor und einer Umweltpr&uuml;fung, die Lagune und Mangrove ernst nimmt. Reichen Sie in der Entwurfsphase ein: einen Entwurf fertigzustellen und erst dann zur Pr&uuml;fung zu geben, kostet hier ein Quartal.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Zusätzlich zum Bau</th><th>MXN</th></tr></thead><tbody>
<tr><td>Architekten- und Ingenieurleistungen auf diesem Niveau</td><td>10&ndash;15% der Bausumme</td></tr>
<tr><td>Einreichung, Pr&uuml;fzyklen, Baukaution</td><td>$150,000&ndash;$600,000</td></tr>
<tr><td>Geplanter Pool mit Technik</td><td>$900,000&ndash;$3,500,000</td></tr>
<tr><td>Ausgewachsene Bepflanzung und Bew&auml;sserung</td><td>$400,000&ndash;$2,000,000</td></tr>
<tr><td>Ausstattung einer Villa dieser Klasse</td><td>$1,500,000&ndash;$6,000,000</td></tr>
<tr><td>Gemeinschaftsgeb&uuml;hr</td><td>Laufend &mdash; je Grundst&uuml;ck pr&uuml;fen</td></tr>
</tbody></table></div>
<p>Die Bauzeit betr&auml;gt etwa <strong>10&ndash;16 Monate</strong> &mdash; l&auml;nger als im Korridor &uuml;blich, weil begrenzte Arbeitszeiten, Pr&uuml;fzyklen und Ausf&uuml;hrungspr&auml;zision Zeit kosten.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Mayakoba?",
   "Die Einstiegsspanne liegt bei $24,000&ndash;$30,000 MXN/m&sup2;, also $3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD) f&uuml;r 150 m&sup2;. Real entstehen H&auml;user von 300&ndash;600 m&sup2; zu $35,000&ndash;$55,000 MXN/m&sup2; inklusive Architektenleistung, importierter Ausstattung, Automation, Pool und Bepflanzung."),
  ("Warum ist Mayakoba der teuerste Bauort im Korridor?",
   "Gestaltungskontrolle nach Resortma&szlig;stab, eine an Branded Residences orientierte Ausbauerwartung, Baustellendisziplin in laufender Luxusumgebung, Umweltmanagement um Lagunen und Mangroven, durchgehende Marine-Spezifikation und Knappheit ohne Wiederholungseffekte."),
  ("Was muss ich zusätzlich zur Bausumme einplanen?",
   "Planung und Ingenieurleistungen mit 10&ndash;15% der Bausumme, Einreichung und Kaution $150,000&ndash;$600,000, geplanter Pool $900,000&ndash;$3,500,000, ausgewachsene Bepflanzung $400,000&ndash;$2,000,000, Ausstattung $1,500,000&ndash;$6,000,000 sowie die laufende Gemeinschaftsgeb&uuml;hr."),
  ("Wie lange dauert eine Villa in Mayakoba?",
   "Etwa 10&ndash;16 Monate f&uuml;r eine Villa dieser Spezifikation, l&auml;nger als im Korridor &uuml;blich. Begrenzte Arbeitszeiten, Pr&uuml;fzyklen der Gemeinschaft und die geforderte Ausf&uuml;hrungspr&auml;zision kosten zus&auml;tzliche Zeit."),
  ("Wer genehmigt den Entwurf?",
   "Die Gemeinde Solidaridad f&uuml;r Nutzung, Genehmigung, Fluchtlinie und DRO sowie die Architekturpr&uuml;fung der Gemeinschaft, die praktisch zuerst kommt und Architektur, Materialien, Farbe, Freianlagen und Beleuchtung pr&uuml;ft."),
 ],
}

Z[("de","corasol")] = {
 "title": "Hausbau-Kosten in Corasol 2026: Bauen Im Laufenden Masterplan",
 "desc": "Baukosten in Corasol 2026 und was Bauen in einem noch entstehenden Masterplan bedeutet: Infrastruktur in Etappen, Gestaltungsbeirat, Golflage, Zufahrtsregeln.",
 "lead": "Ein 150-m&sup2;-Haus in <strong>Corasol</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD)</strong>, etwa 30% &uuml;ber dem Basisniveau von Playa del Carmen. In Corasol steht auch unser B&uuml;ro &mdash; diese Seite entsteht also wenige Gehminuten vom Thema entfernt.",
 "sections": [
  ("Schlüsselfertige Kosten nach Hausgröße",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Hausgr&ouml;&szlig;e</th><th>Schl&uuml;sselfertig (MXN)</th><th>Schl&uuml;sselfertig (USD)</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.30M&ndash;$4.12M</td><td>$183k&ndash;$229k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.40M&ndash;$5.50M</td><td>$244k&ndash;$306k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.60M&ndash;$8.25M</td><td>$367k&ndash;$458k</td></tr>
<tr><td>450 m&sup2;</td><td>$9.90M&ndash;$12.38M</td><td>$550k&ndash;$688k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referenz: $22,000&ndash;$27,500 MXN/m&sup2; Standard- bis Premium-Ausbau. USD/MXN &asymp; 18. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<p>Das meiste hier ist gr&ouml;&szlig;er als 150 m&sup2;: Grundst&uuml;cke und Markt dr&auml;ngen zu Villen von 250&ndash;450 m&sup2; mit Pool, Dachterrasse und geplanter Bepflanzung. Kalkulieren Sie das Gesamtpaket &mdash; bei 300 m&sup2; summieren sich Pool, Freianlagen, M&ouml;blierung und Honorare h&auml;ufig auf 35&ndash;50% oberhalb der reinen Bausumme.</p>"""),
  ("Bauen in einer Gemeinschaft, die selbst noch entsteht",
   """<ul>
<li><strong>Die Infrastruktur kommt in Etappen.</strong> Lassen Sie sich f&uuml;r Ihr Grundst&uuml;ck best&auml;tigen, was heute tats&auml;chlich an der Grenze liegt &mdash; elektrische Leistung, Wasser, Kanal, Stra&szlig;enbelag &mdash; und was lediglich geplant ist. Zwischen "die Anlage wird haben" und "das Grundst&uuml;ck hat" liegt das Budgetrisiko.</li>
<li><strong>Sie werden Baustellen als Nachbarn haben.</strong> Weitere H&auml;user und Gemeinschaftsarbeiten laufen &uuml;ber Jahre: L&auml;rm und Verkehr w&auml;hrend Ihrer Nutzung, geteilte Zufahrten w&auml;hrend Ihres Baus.</li>
<li><strong>Die Gestaltungspr&uuml;fung ist aktiv und entwickelt sich.</strong> Der Beirat pr&uuml;ft H&ouml;he, Baumasse, Materialien, Farbe, Einfriedungen und Freianlagen, um ein stimmiges Bild in einer unfertigen Anlage zu sichern. Reichen Sie in der Entwurfsphase ein.</li>
<li><strong>Zufahrts- und Bauregeln.</strong> Registrierte Arbeiter, kontrollierte Einfahrt, feste Lieferzeiten, Lagergrenzen auf dem Grundst&uuml;ck, Stra&szlig;enreinigung und Kaution. Kalkulieren Sie $80,000&ndash;$300,000 MXN f&uuml;r Einreichung, Kaution und Zufahrtsmanagement.</li>
<li><strong>Golflage</strong> bringt die Frage von Verglasung und Oberlichtern &mdash; verirrte B&auml;lle sind ein reales, kalkulierbares Risiko &mdash; dazu die Schnittstelle von Bew&auml;sserung und Entw&auml;sserung zum Platz.</li>
</ul>"""),
  ("Baugrund, Genehmigungen und Ablauf",
   """<p>Corasol liegt in der Gemeinde <strong>Solidaridad</strong>: Nutzungszertifikat, Fluchtlinie, Baugenehmigung und Director Responsable de Obra, mit der Architekturpr&uuml;fung der Gemeinschaft praktisch davor. Umweltanforderungen gelten wie an der &uuml;brigen K&uuml;ste, und der Karst verlangt ein Bodengutachten mit Sondierungen &uuml;ber der tats&auml;chlichen Grundfl&auml;che &mdash; gute Tragf&auml;higkeit und ein Hohlraum zwei Meter daneben sind hier beide normal.</p>
<ul>
<li><strong>Die Marine-Spezifikation gilt weiterhin.</strong> Corasol liegt nah genug am Meer, dass 316er Edelstahl, eloxiertes oder marinebeschichtetes Aluminium und gro&szlig;z&uuml;gige Betondeckung richtig und nicht optional sind.</li>
<li><strong>Planen Sie das Dach von Anfang an als Terrasse,</strong> wenn die H&ouml;he es zul&auml;sst. Bei Grundst&uuml;cken mit Blick auf Platz oder Meer ist es der wertvollste Quadratmeter des Hauses; nachtr&auml;glich kostet es ein Vielfaches.</li>
<li><strong>Technikfl&auml;chen richtig einplanen:</strong> Zisterne, Druckanlage, Wasseraufbereitung wegen der H&auml;rte, Pooltechnik und Positionen der Klimager&auml;te &mdash; alles wartungszug&auml;nglich.</li>
</ul>
<p>Die Bauzeit betr&auml;gt etwa <strong>8&ndash;12 Monate</strong> f&uuml;r eine Villa von 250&ndash;300 m&sup2; und mehr, wenn die Gestaltungspr&uuml;fung &uuml;ber einen Zyklus hinausgeht. Wenn Sie das Grundst&uuml;ck jetzt kaufen und sp&auml;ter bauen: Lassen Sie sich den Erschlie&szlig;ungsstand an der Grundst&uuml;cksgrenze vor dem Notartermin schriftlich geben.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Corasol?",
   "Etwa $3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD) schl&uuml;sselfertig f&uuml;r 150 m&sup2; &mdash; rund $22,000&ndash;$27,500 MXN/m&sup2;, etwa 30% &uuml;ber dem Basisniveau von Playa del Carmen. Die meisten H&auml;user hier haben 250&ndash;450 m&sup2;, wo Pool, Freianlagen, M&ouml;blierung und Honorare 35&ndash;50% hinzukommen."),
  ("Was sollte ich vor dem Grundstückskauf in Corasol prüfen?",
   "Welche Infrastruktur heute tats&auml;chlich an der Grundst&uuml;cksgrenze liegt &mdash; elektrische Leistung, Wasser, Kanal, Stra&szlig;enbelag &mdash; im Vergleich zum Geplanten. In einem noch entstehenden Masterplan liegt genau dort das Budgetrisiko."),
  ("Kostet der Gestaltungsbeirat Zeit und Geld?",
   "Beides. Kalkulieren Sie $80,000&ndash;$300,000 MXN f&uuml;r Einreichung, Baukaution und Zufahrtsmanagement und mindestens einen Pr&uuml;fzyklus im Terminplan, dazu registrierte Arbeiter, kontrollierte Einfahrt, Lieferzeiten und Stra&szlig;enreinigung."),
  ("Was ändert die Golflage?",
   "Die Spezifikation von Verglasung und Oberlichtern, weil verirrte B&auml;lle ein reales und kalkulierbares Risiko sind, dazu die Schnittstelle von Bew&auml;sserung und Entw&auml;sserung zum Platz. Das geh&ouml;rt in die Planung, nicht in einen sp&auml;teren Glastausch."),
  ("Wie lange dauert eine Villa in Corasol?",
   "Etwa 8&ndash;12 Monate f&uuml;r 250&ndash;300 m&sup2; von der Genehmigung bis zur &Uuml;bergabe, l&auml;nger bei mehr als einem Pr&uuml;fzyklus. Begrenzte Arbeitszeiten und kontrollierter Zugang schieben den Plan ans obere Ende."),
 ],
}

Z[("de","aldea-zama")] = {
 "title": "Hausbau-Kosten in Aldea Zamá 2026: Der Kalender Kostet",
 "desc": "Baukosten in Aldea Zamá 2026 plus der Posten, den niemand einplant: Tulums Genehmigungskalender. Höhenbegrenzung, Stromversorgung, erschlossener Masterplan.",
 "lead": "Ein 150-m&sup2;-Haus in <strong>Aldea Zam&aacute;</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD)</strong>, etwa 20% &uuml;ber dem Basisniveau von Playa del Carmen. Die Bausumme ist unkompliziert. Was in Tulum selten budgetiert wird, ist Zeit.",
 "sections": [
  ("Schlüsselfertige Kosten nach Hausgröße",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Hausgr&ouml;&szlig;e</th><th>Schl&uuml;sselfertig (MXN)</th><th>Schl&uuml;sselfertig (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.05M&ndash;$2.50M</td><td>$114k&ndash;$139k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.08M&ndash;$3.75M</td><td>$171k&ndash;$208k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.10M&ndash;$5M</td><td>$228k&ndash;$278k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.15M&ndash;$7.50M</td><td>$342k&ndash;$417k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referenz: $20,500&ndash;$25,000 MXN/m&sup2; Standard- bis Premium-Ausbau. USD/MXN &asymp; 18. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<p>Aldea Zam&aacute; liegt aus einem einfachen Grund &uuml;ber den Tulum-Regionen und La Veleta: Es ist ein erschlossener Masterplan mit Leitungen im Boden, asphaltierten Zufahrten und definiertem Charakter in Geh- oder Radn&auml;he zur Strandstra&szlig;e. Sie bezahlen vorhandene Infrastruktur statt Infrastruktur, die Sie selbst herstellen m&uuml;ssen.</p>"""),
  ("Was der Genehmigungskalender wirklich kostet",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Schritt</th><th>Dauer</th></tr></thead><tbody>
<tr><td>Nutzungszertifikat und Fluchtlinie</td><td>2&ndash;8 Wochen</td></tr>
<tr><td>Bodengutachten (parallel)</td><td>2&ndash;5 Wochen</td></tr>
<tr><td>Umweltakte</td><td>3&ndash;8 Monate je nach Bewuchs</td></tr>
<tr><td>Technische Planung (parallel)</td><td>6&ndash;14 Wochen</td></tr>
<tr><td>Genehmigungspr&uuml;fung bei vollst&auml;ndiger Akte</td><td>4&ndash;12 Wochen</td></tr>
<tr><td><strong>Gesamt bis zum Baubeginn</strong></td><td><strong>5&ndash;12 Monate</strong></td></tr>
</tbody></table></div>
<p>Diese Monate sind ein realer Posten: gebundenes Grundst&uuml;ck, gebundenes Kapital, kein Ertrag. Zwei Wege, sie zu verk&uuml;rzen. Erstens: Umweltakte und Bodengutachten starten, solange die Architektur noch im Entwurf ist &mdash; beides braucht keine Endpl&auml;ne und beeinflusst den Entwurf ohnehin. Zweitens: Beim Grundst&uuml;cksvergleich eine bestehende Umweltgenehmigung hoch gewichten; sie kann sechs Monate und einen sechsstelligen Betrag wert sein.</p>"""),
  ("Höhe, Strom und was hier gebaut wird",
   """<ul>
<li><strong>Die H&ouml;henbegrenzungen sind streng</strong> und werden durchgesetzt. Tulums Regeln sind bewusst enger als die von Playa del Carmen &mdash; pr&uuml;fen Sie das genaue Ma&szlig; f&uuml;r Ihr Grundst&uuml;ck, bevor Sie eine Dachterrasse planen. Bei vielen Grundst&uuml;cken h&auml;ngt an dieser einen Zahl, ob das Projekt &uuml;berzeugt.</li>
<li><strong>Die Stromversorgung ist unzuverl&auml;ssiger als in Playa del Carmen.</strong> Kalkulieren Sie einen &Uuml;berspannungsschutz f&uuml;r das ganze Haus als Standard und bei Mietobjekten ein Batteriesystem f&uuml;r das N&ouml;tigste &mdash; Internet, Poolsteuerung, etwas Licht und einen Ventilator &mdash; f&uuml;r $140,000&ndash;$330,000 MXN. Solar rechnet sich hier besonders, sobald Poolpumpe und mehrere Klimager&auml;te den Verbrauch in den DAC-Tarif treiben.</li>
<li><strong>Der Markt ist eigentumswohnungsdominiert,</strong> was genau das Argument f&uuml;r ein Haus ist. Einem freistehenden Haus kann keine Eigent&uuml;merversammlung die Kurzzeitvermietung entziehen, es zahlt keine Gemeinschaftsgeb&uuml;hr auf den Bruttoertrag und l&auml;sst sich auf Rendite planen: Schlafzimmer mit eigenem Bad, Lock-off-Casita, Dachterrasse, Pool in der richtigen Blickachse.</li>
</ul>
<p>Technisch gelten die &uuml;blichen Tulum-Punkte: Reinigung vor Versickerung nach Belegung ($90,000&ndash;$250,000 MXN), Wasseraufbereitung wegen der H&auml;rte, Termiten- und Feuchtedetails sowie ein Bodengutachten, weil der Karst hier cenotenreich ist. Die Bauzeit betr&auml;gt etwa <strong>7&ndash;11 Monate</strong> f&uuml;r 150&ndash;200 m&sup2;.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Aldea Zamá?",
   "Etwa $3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD) schl&uuml;sselfertig f&uuml;r 150 m&sup2; im Standard- bis Premium-Ausbau &mdash; rund $20,500&ndash;$25,000 MXN/m&sup2;, etwa 20% &uuml;ber dem Basisniveau von Playa del Carmen."),
  ("Warum ist es teurer als die Tulum-Regionen?",
   "Weil die Infrastruktur vorhanden ist: ein erschlossener Masterplan mit Leitungen im Boden, asphaltierten Zufahrten und definiertem Charakter nahe der Strandstra&szlig;e. Bei einem g&uuml;nstigeren Regi&oacute;n-Grundst&uuml;ck bezahlen Sie Erschlie&szlig;ung, Zufahrt und Umfeld sp&auml;ter selbst."),
  ("Wie lange dauert es bis zum Baubeginn in Tulum?",
   "Realistisch f&uuml;nf bis zw&ouml;lf Monate ab Kauf: 2&ndash;8 Wochen Nutzungszertifikat und Fluchtlinie, 3&ndash;8 Monate Umweltakte bei bewachsenem Grundst&uuml;ck und 4&ndash;12 Wochen Genehmigungspr&uuml;fung. Starten Sie Umweltakte und Bodengutachten bereits in der Entwurfsphase."),
  ("Ist eine Dachterrasse in Aldea Zamá möglich?",
   "Das h&auml;ngt an der H&ouml;henbegrenzung des konkreten Grundst&uuml;cks, und Tulums Grenzen sind bewusst eng und werden durchgesetzt. Pr&uuml;fen Sie das Ma&szlig; vor dem Entwurf &mdash; bei vielen Grundst&uuml;cken entscheidet es &uuml;ber die Qualit&auml;t des Projekts."),
  ("Was tun gegen Stromausfälle in Tulum?",
   "&Uuml;berspannungsschutz f&uuml;r das ganze Haus als Standard und bei Mietobjekten ein Batteriesystem f&uuml;r Internet, Poolsteuerung, Licht und Ventilator f&uuml;r $140,000&ndash;$330,000 MXN. Solar amortisiert sich hier ebenfalls schnell, besonders im DAC-Tarif."),
 ],
}

Z[("de","playa-del-carmen")] = {
 "title": "Hausbau-Kosten in Playa del Carmen 2026: Phase für Phase",
 "desc": "Der Referenzpreis des Korridors. Phasenbudget für ein 150-m²-Haus, was der m²-Preis enthält und was nicht, Zusatzposten und Budgetdisziplin.",
 "lead": "Ein solide gebautes 150-m&sup2;-Familienhaus in <strong>Playa del Carmen</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$2.6M&ndash;$3.2M MXN ($145.000&ndash;$178.000 USD)</strong>. An dieser Zahl misst sich der gesamte Korridor &mdash; deshalb lohnt es, sie phasenweise zu verstehen statt als eine einzige Summe.",
 "sections": [
  ("Phasenbudget (Standardhaus, 150 m²)",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Phase</th><th>% des Budgets</th><th>Kosten (MXN)</th><th>Umfang</th></tr></thead><tbody>
<tr><td>Genehmigungen, DRO, Gutachten</td><td>5%</td><td>$130.000&ndash;$160.000</td><td>Baugenehmigung, DRO, Boden, Vermessung</td></tr>
<tr><td>Gr&uuml;ndung und Rohbau</td><td>30%</td><td>$780.000&ndash;$960.000</td><td>Bodenplatte, St&uuml;tzen, Unterz&uuml;ge, Decken</td></tr>
<tr><td>W&auml;nde und Dach</td><td>18%</td><td>$470.000&ndash;$580.000</td><td>Mauerwerk, Ringanker, Dachdecke</td></tr>
<tr><td>Installationen</td><td>15%</td><td>$390.000&ndash;$480.000</td><td>Elektro, Sanit&auml;r, Abwasser</td></tr>
<tr><td>Ausbau</td><td>25%</td><td>$650.000&ndash;$800.000</td><td>B&ouml;den, Anstrich, Chukum, Tischlerei</td></tr>
<tr><td>Endreinigung und &Uuml;bergabe</td><td>7%</td><td>$180.000&ndash;$220.000</td><td>Restarbeiten, &Uuml;bergabe</td></tr>
</tbody></table></div>
<p class="text-muted small">Gesamt schl&uuml;sselfertig &asymp; $2.6M&ndash;$3.2M MXN. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<p>Zwei Lesarten: Der Rohbau ist fast ein Drittel des Budgets und die einzige Phase, in der Sparen in einer Starkwindregion wirklich gef&auml;hrlich ist. Und der Ausbau mit 25% ist dort, wo Ihre Spezifikation tats&auml;chlich stattfindet &mdash; derselbe Rohbau mit anderem Ausbau verschiebt die Summe um 20%, ohne dass sich ein Plan &auml;ndert.</p>"""),
  ("Was der m²-Preis enthält und was nicht",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Position</th><th>MXN</th></tr></thead><tbody>
<tr><td>Grundst&uuml;ck</td><td>Separat, und die gr&ouml;&szlig;te Variable in Playa del Carmen</td></tr>
<tr><td>Pool 4&times;8 m mit Technik</td><td>$450.000&ndash;$1.200.000</td></tr>
<tr><td>Dachterrassenausbau (Statik vorgesehen)</td><td>$3.500&ndash;$9.000 pro m&sup2;</td></tr>
<tr><td>Wasseraufbereitung (Filter, Enth&auml;rter, Aktivkohle, Osmose)</td><td>$35.000&ndash;$95.000</td></tr>
<tr><td>Klimaanlage, 4&ndash;5 Inverter-Zonen</td><td>$120.000&ndash;$280.000</td></tr>
<tr><td>Solar, 5&ndash;8 kWp</td><td>$115.000&ndash;$250.000</td></tr>
<tr><td>Freianlagen und Bew&auml;sserung</td><td>$500&ndash;$2.000 pro m&sup2;</td></tr>
<tr><td>M&ouml;bel und Ger&auml;te</td><td>$450.000&ndash;$1.200.000 f&uuml;r ein Familienhaus</td></tr>
</tbody></table></div>
<p>Planung, Ingenieurleistungen, Gutachten und Genehmigungen liegen bei einem individuellen Haus zusammen typischerweise bei 8&ndash;14% der Bausumme &mdash; teils bereits in der Phasentabelle enthalten und keine Position zum K&uuml;rzen, denn jeder dadurch vermiedene Fehler kostet mehr als das ganze Paket.</p>"""),
  ("Warum das die Referenz ist und wie das Budget hält",
   """<p>Playa del Carmen liegt unter den geschlossenen und Premium-Lagen aus strukturellen Gr&uuml;nden, nicht aus Qualit&auml;tsgr&uuml;nden: breite Lieferantenbasis, echter Wettbewerb, erschlossene st&auml;dtische Grundst&uuml;cke, ein direkter Genehmigungsweg in der Gemeinde <strong>Solidaridad</strong> und bei den allermeisten Grundst&uuml;cken keine Bundesk&uuml;stenzone. Alles &Uuml;brige im Korridor ist ein Vielfaches davon: Puerto Morelos etwa gleichauf, Puerto Aventuras rund 8% dar&uuml;ber, Akumal 12%, Aldea Zam&aacute; 20%, Playacar 25%, Corasol 30%, Mayakoba 42%.</p>
<ul>
<li><strong>Festpreis mit Positionsbudget,</strong> kein m&sup2;-Preis per Handschlag. Ein Einheitspreis mal Quadratmeter ist kein Budget, sondern eine Einladung zum Nachverhandeln.</li>
<li><strong>Zahlungen nach gepr&uuml;ftem Baufortschritt,</strong> nicht nach Kalenderdaten, mit 5&ndash;10% Einbehalt bis zum Abschluss der M&auml;ngelliste.</li>
<li><strong>Nachtr&auml;ge schriftlich und bepreist,</strong> bevor gearbeitet wird. M&uuml;ndliche &Auml;nderungen sind der h&auml;ufigste Weg vom Festpreis zum offenen Preis.</li>
<li><strong>Ausdr&uuml;ckliche Ausschlussliste</strong> &mdash; M&ouml;bel, Ger&auml;te, Freianlagen jenseits einer definierten Grenze, Anschlussgeb&uuml;hren &mdash; bei Vertragsschluss vereinbart.</li>
</ul>
<p>Ein 150-m&sup2;-Haus dauert etwa <strong>7&ndash;10 Monate</strong> ab Genehmigung, zuz&uuml;glich zwei bis vier Monate Vorlauf. F&uuml;r eine schnelle Sch&auml;tzung nutzen Sie den <a href="/kostenrechner/">Kostenrechner</a>.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Playa del Carmen 2026?",
   "Etwa $2.6M&ndash;$3.2M MXN ($145.000&ndash;$178.000 USD) schl&uuml;sselfertig f&uuml;r 150 m&sup2; mit Standardausbau &mdash; rund $17.000&ndash;$21.000 MXN/m&sup2;, ohne Grundst&uuml;ck, Pool und M&ouml;bel."),
  ("Was ist im m²-Preis nicht enthalten?",
   "Grundst&uuml;ck, Pool ($450.000&ndash;$1.200.000), Dachterrassenausbau, Wasseraufbereitung, Klimaanlage, Solar, Freianlagen und M&ouml;blierung. Daraus entstehen die meisten Budget&uuml;berraschungen &mdash; also von Anfang an als eigene Positionen kalkulieren."),
  ("Welche Phase kostet am meisten?",
   "Gr&uuml;ndung und Rohbau mit etwa 30%, gefolgt vom Ausbau mit 25%. Der Rohbau ist zugleich die Phase, in der Sparen in einer Starkwindregion gef&auml;hrlich ist, w&auml;hrend der Ausbau die Summe um 20% verschieben kann, ohne dass sich ein Plan &auml;ndert."),
  ("Wie verhält sich Playa del Carmen zu den anderen Lagen?",
   "Es ist die Referenz. Puerto Morelos liegt etwa gleichauf, Puerto Aventuras rund 8% dar&uuml;ber, Akumal 12%, Aldea Zam&aacute; 20%, Playacar 25%, Corasol 30% und Mayakoba 42% &mdash; die Unterschiede stammen aus Zugangsbeschr&auml;nkungen, Gestaltungsbeir&auml;ten, Marine-Spezifikation und Umweltauflagen."),
  ("Wie verhindere ich, dass das Budget davonläuft?",
   "Festpreis mit Positionsbudget statt m&sup2;-Pauschale, Zahlungen nach gepr&uuml;ftem Baufortschritt mit 5&ndash;10% Einbehalt, schriftliche und bepreiste Nachtr&auml;ge vor Ausf&uuml;hrung und eine ausdr&uuml;ckliche Ausschlussliste bei Vertragsschluss."),
 ],
}

Z[("de","tulum")] = {
 "title": "Hausbau-Kosten in Tulum 2026: Grundstück Entscheidet",
 "desc": "Baukosten in Tulum 2026 und warum das Grundstück — Erschließung, Bewuchs, Umweltakte — mehr über die Endsumme entscheidet als das Haus selbst.",
 "lead": "Ein 150-m&sup2;-Haus in <strong>Tulum</strong> kostet 2026 schl&uuml;sselfertig rund <strong>$2.85M&ndash;$3.60M MXN ($158k&ndash;$200k USD)</strong>. Die Spanne der Endsummen ist hier jedoch gr&ouml;&szlig;er als irgendwo sonst im Korridor &mdash; und der Grund daf&uuml;r ist fast nie das Haus, sondern das Grundst&uuml;ck.",
 "sections": [
  ("Kosten nach Hausgröße und Lage",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Hausgr&ouml;&szlig;e</th><th>Schl&uuml;sselfertig (MXN)</th><th>Schl&uuml;sselfertig (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.90M&ndash;$2.40M</td><td>$106k&ndash;$133k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.85M&ndash;$3.60M</td><td>$158k&ndash;$200k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.80M&ndash;$4.80M</td><td>$211k&ndash;$267k</td></tr>
<tr><td>300 m&sup2;</td><td>$5.70M&ndash;$7.20M</td><td>$317k&ndash;$400k</td></tr>
</tbody></table></div>
<p class="text-muted small">Referenz: $19.000&ndash;$24.000 MXN/m&sup2; Standard- bis Premium-Ausbau. USD/MXN &asymp; 18. Ohne Grundst&uuml;ck, Pool und M&ouml;bel.</p>
<p>Innerhalb Tulums spreizen sich die Lagen deutlich: die Regionen und La Veleta am unteren Rand, Aldea Zam&aacute; und der Tulum Country Club dar&uuml;ber, die Strandstra&szlig;e mit Marine-Spezifikation und schwerer Umweltakte weit dar&uuml;ber.</p>"""),
  ("Warum das Grundstück die Endsumme bestimmt",
   """<p>Vier Positionen, die mit dem Grundst&uuml;ck und nicht mit der Hausgr&ouml;&szlig;e skalieren:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Position</th><th>MXN</th></tr></thead><tbody>
<tr><td>Umweltakte je nach Bewuchs</td><td>$80.000&ndash;$300.000</td></tr>
<tr><td>Kl&auml;ranlage bzw. Biodigestor mit Sickerfeld</td><td>$90.000&ndash;$250.000</td></tr>
<tr><td>CFE-Anschluss an erschlossener Stra&szlig;e</td><td>$10.000&ndash;$40.000</td></tr>
<tr><td>CFE-Erweiterung zu unerschlossenem Grundst&uuml;ck</td><td>$150.000&ndash;&uuml;ber $900.000</td></tr>
<tr><td>Inselversorgung statt Netzanschluss (Solar, Speicher, Brunnen)</td><td>$250.000&ndash;$800.000</td></tr>
<tr><td>Zufahrt und Erschlie&szlig;ung im Dschungelgel&auml;nde</td><td>$40.000&ndash;$300.000</td></tr>
</tbody></table></div>
<p>Deshalb ist die wichtigste Entscheidung in Tulum die Grundst&uuml;cksauswahl und nicht die Ausstattungsliste. Lassen Sie die CFE-Erweiterung <em>vor</em> dem Kauf beziffern: Diese eine Zahl entscheidet dar&uuml;ber, ob Netzanschluss oder eine geplante Inselversorgung der g&uuml;nstigere und schnellere Weg ist.</p>"""),
  ("Genehmigungskalender, Strom und Ausführung",
   """<p>Tulums Pr&uuml;fung ist die umweltrechtlich anspruchsvollste im Korridor. Realistisch vergehen <strong>6&ndash;14 Monate</strong> vom Kauf bis zum Baubeginn: Nutzungszertifikat und Fluchtlinie 2&ndash;8 Wochen, Umweltakte 4&ndash;9 Monate bei bewachsenem Grundst&uuml;ck, technische Planung parallel, Genehmigungspr&uuml;fung 4&ndash;12 Wochen. Starten Sie Umweltakte und Bodengutachten in der Entwurfsphase &mdash; beides braucht keine Endpl&auml;ne und beeinflusst den Entwurf ohnehin.</p>
<ul>
<li><strong>H&ouml;henbegrenzungen sind streng</strong> und werden durchgesetzt &mdash; pr&uuml;fen Sie das Ma&szlig; f&uuml;r Ihr Grundst&uuml;ck, bevor Sie eine Dachterrasse planen.</li>
<li><strong>Die Stromversorgung ist unzuverl&auml;ssiger</strong> als weiter n&ouml;rdlich: &Uuml;berspannungsschutz als Standard, bei Mietobjekten ein Batteriesystem f&uuml;r Internet, Poolsteuerung und Grundbeleuchtung, $140.000&ndash;$330.000 MXN.</li>
<li><strong>Cenoten und Karst</strong> verlangen Bodengutachten mit Sondierungen und Abst&auml;nde f&uuml;r Versickerung. Was hier versickert, erreicht den Aquifer und das Riff.</li>
<li><strong>Termiten und Feuchte:</strong> kein Holz-Erdkontakt, Bodenbehandlung vor der Platte, hinterl&uuml;ftete Einbauten, Entfeuchtung in geschlossenen R&auml;umen.</li>
</ul>
<p>Die reine Bauzeit betr&auml;gt etwa <strong>7&ndash;11 Monate</strong> f&uuml;r 150&ndash;200 m&sup2;. Festpreisvertrag mit Positionsbudget und Zahlungen nach gepr&uuml;ftem Fortschritt &mdash; und den Genehmigungskalender von Anfang an in die Planung nehmen, statt ihn zu entdecken.</p>"""),
 ],
 "faq": [
  ("Was kostet ein Hausbau in Tulum 2026?",
   "Etwa $2.85M&ndash;$3.60M MXN ($158k&ndash;$200k USD) schl&uuml;sselfertig f&uuml;r 150 m&sup2; &mdash; rund $19.000&ndash;$24.000 MXN/m&sup2;. Innerhalb Tulums liegen die Regionen und La Veleta am unteren Rand, Aldea Zam&aacute; dar&uuml;ber und die Strandstra&szlig;e deutlich dar&uuml;ber."),
  ("Warum schwanken die Endsummen in Tulum so stark?",
   "Weil vier gro&szlig;e Positionen mit dem Grundst&uuml;ck skalieren und nicht mit dem Haus: Umweltakte $80.000&ndash;$300.000, Kl&auml;ranlage $90.000&ndash;$250.000, Stromanschluss zwischen $10.000 und &uuml;ber $900.000, und Zufahrt im Dschungelgel&auml;nde $40.000&ndash;$300.000."),
  ("Netzanschluss oder Inselversorgung?",
   "Lassen Sie die CFE-Erweiterung vor dem Kauf beziffern. Liegt sie im hohen sechsstelligen Bereich, ist eine geplante Inselversorgung mit Solar, Speicher, aufbereitetem Brunnen und Regenwasser f&uuml;r $250.000&ndash;$800.000 oft g&uuml;nstiger und schneller."),
  ("Wie lange dauert es bis zum Baubeginn?",
   "Realistisch 6&ndash;14 Monate ab Kauf, haupts&auml;chlich wegen der Umweltakte, die bei bewachsenem Grundst&uuml;ck 4&ndash;9 Monate braucht. Umweltakte und Bodengutachten sollten starten, solange die Architektur noch im Entwurf ist."),
  ("Welche technischen Punkte sind in Tulum besonders wichtig?",
   "Reinigung vor Versickerung mit korrekten Abst&auml;nden zu Cenoten, Bodengutachten wegen des Karsts, &Uuml;berspannungsschutz und gegebenenfalls Batteriepuffer wegen der Netzqualit&auml;t, sowie konsequente Termiten- und Feuchtedetails ohne Holz-Erdkontakt."),
 ],
}

Z[("ru","cancun")] = {
 "title": "Сколько Стоит Построить Дом в Канкуне 2026: Почему Дешевле",
 "desc": "Строительство в Канкуне дешевле, чем в остальном коридоре. Диапазоны за м² на 2026 год, откуда берётся скидка и где она превращается в риск.",
 "lead": "Семейный дом 150 м&sup2; в <strong>Канкуне</strong> обойдётся примерно в <strong>$2.48M&ndash;$3M MXN ($138k&ndash;$167k USD)</strong> под ключ в 2026 году &mdash; самая низкая цифра в коридоре, примерно на 4% ниже Плая-дель-Кармен при той же отделке. Ниже объясняем, откуда эта скидка и где она перестаёт быть выгодой.",
 "sections": [
  ("Почему Канкун дешевле остального побережья",
   """<p>Канкун &mdash; единственное место на побережье, где масштаб рынка работает на застройщика частного дома: самый большой пул рабочей силы, наибольшая концентрация поставщиков и цехов и достаточное число конкурирующих подрядчиков, чтобы цена действительно проверялась. Всё, что южнее Пуэрто-Морелоса, часть работ везёт отсюда.</p>
<ul>
<li><strong>Материалы по месту.</strong> Блок, цемент, арматура, инертные, алюминий, плитка и сантехника покупаются локально без доставки по коридору &mdash; на доме 150 м&sup2; это уже несколько процентов.</li>
<li><strong>Бригады без командировок.</strong> Специализированные работы, которые в Тулум или Акумаль нужно планировать и везти, здесь решаются местным звонком.</li>
<li><strong>Участки вглубь материка.</strong> Основная частная застройка Канкуна идёт в закрытых посёлках внутри города: нет федеральной морской зоны, нет концессии ZOFEMAT, нет календаря гнездования черепах и заметно легче экологическое досье, чем на прибрежном участке того же размера.</li>
</ul>
<p>Разрешения оформляются в муниципалитете <strong>Бенито Хуарес</strong> &mdash; назначение земли, лицензия на строительство, выравнивание и Director Responsable de Obra &mdash; и для обеспеченного коммуникациями участка это одна из самых предсказуемых процедур в штате.</p>"""),
  ("Стоимость под ключ по площади дома",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Площадь</th><th>Под ключ (MXN)</th><th>Под ключ (USD)</th></tr></thead><tbody>
<tr><td>100 м&sup2;</td><td>$1.65M&ndash;$2M</td><td>$92k&ndash;$111k</td></tr>
<tr><td>150 м&sup2;</td><td>$2.48M&ndash;$3M</td><td>$138k&ndash;$167k</td></tr>
<tr><td>200 м&sup2;</td><td>$3.30M&ndash;$4M</td><td>$183k&ndash;$222k</td></tr>
<tr><td>250 м&sup2;</td><td>$4.13M&ndash;$5M</td><td>$229k&ndash;$278k</td></tr>
</tbody></table></div>
<p class="text-muted small">Ориентир: $16,500&ndash;$20,000 MXN/м&sup2; стандартная отделка. USD/MXN &asymp; 18. Без земли, бассейна и мебели.</p>
<p>Эти диапазоны относятся к жилому Канкуну вглубь материка. Участок в Зона Отелера, на Исла-Дорада или с выходом к морю либо лагуне &mdash; это другое здание: морская спецификация целиком, вопросы федеральной зоны и уровень отделки, которого требует место. Там реалистично $26,000&ndash;$40,000 MXN/м&sup2;.</p>"""),
  ("Где экономия превращается в риск",
   """<p>Большой конкурентный рынок даёт низкие цены и огромный разброс качества. Проблема Канкуна &mdash; не дорогая стройка, а дешёвая.</p>
<ul>
<li><strong>Предложения ниже примерно $14,000 MXN/м&sup2;</strong> режут что-то конструктивное &mdash; обычно плотность армирования, качество бетона или электрику. В зоне сильных ветров арматура &mdash; неподходящая статья для экономии.</li>
<li><strong>Без геологии.</strong> Карст может дать отличную несущую способность и полость в двух метрах рядом. Изыскания по пятну застройки стоят $25,000&ndash;$60,000 и это самое дешёвое снижение риска в проекте.</li>
<li><strong>Правила посёлка.</strong> Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua и Palmaris работают с архитектурными комитетами: собственные ограничения по высоте, отступам, материалам и цвету, регистрация рабочих, ограниченные часы и залог. Подавайте на стадии эскиза.</li>
<li><strong>Трафик и окна поставок.</strong> Канкун &mdash; единственное место на побережье, где городской трафик становится вопросом графика: поставки во внутренние посёлки требуют времени, а ограничения по часам это усложняют.</li>
<li><strong>Соль доходит и вглубь.</strong> Даже в нескольких километрах от моря крепёж, ограждения и теплообменники кондиционеров служат заметно дольше в нержавейке 316 и морских покрытиях.</li>
</ul>
<p>Дом 150 м&sup2; занимает примерно <strong>7&ndash;10 месяцев</strong> от лицензии до сдачи, и глубина рынка поставщиков снимает часть материальных простоев, которые растягивают проекты южнее. Требуйте договор с фиксированной ценой, постатейной сметой и оплатой по проверенному факту.</p>"""),
 ],
 "faq": [
  ("Сколько стоит построить дом в Канкуне в 2026 году?",
   "Около $2.48M&ndash;$3M MXN ($138k&ndash;$167k USD) под ключ за 150 м&sup2; со стандартной отделкой на внутреннем жилом участке, без земли, бассейна и мебели &mdash; примерно $16,500&ndash;$20,000 MXN/м&sup2;."),
  ("Почему Канкун дешевле Плая-дель-Кармен или Тулума?",
   "Из-за масштаба: крупнейший пул рабочей силы на побережье, наибольшая плотность поставщиков и цехов и реальная конкуренция подрядчиков. Плюс застройка идёт на внутренних участках, что снимает федеральную морскую зону, правила гнездования черепах и более тяжёлое экологическое досье прибрежного участка."),
  ("Эта цена действует в Зона Отелера?",
   "Нет. Зона Отелера, Исла-Дорада и любой выход к морю или лагуне означают полную морскую спецификацию, вопросы федеральной зоны и более высокий уровень отделки &mdash; закладывайте $26,000&ndash;$40,000 MXN/м&sup2;."),
  ("Насколько низкой может быть адекватная смета в Канкуне?",
   "Считайте тревожным сигналом всё, что ниже примерно $14,000 MXN/м&sup2;. На этой цене сокращают что-то конструктивное &mdash; армирование, качество бетона или электрику &mdash; а в зоне сильных ветров это неверная экономия."),
  ("Закрытые посёлки удорожают стройку?",
   "Да. Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua и Palmaris имеют архитектурные комитеты с собственными нормами по высоте, отступам, материалам и цвету, плюс регистрацию рабочих, ограниченные часы и залог. Закладывайте цикл согласования в график, а не только взносы."),
 ],
}

Z[("ru","puerto-aventuras")] = {
 "title": "Сколько Стоит Построить Дом в Пуэрто-Авентурас 2026",
 "desc": "Стоимость под ключ в Пуэрто-Авентурас плюс статьи марины, которые забывают: взнос HOA, причал, состояние набережной стены и архитектурный комитет.",
 "lead": "Дом 150 м&sup2; в <strong>Пуэрто-Авентурас</strong> обойдётся примерно в <strong>$2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD)</strong> под ключ в 2026 году &mdash; около 8% выше Плая-дель-Кармен. Стройка здесь предсказуема; расходятся бюджеты на статьях ниже.",
 "sections": [
  ("Стоимость под ключ по площади дома",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Площадь</th><th>Под ключ (MXN)</th><th>Под ключ (USD)</th></tr></thead><tbody>
<tr><td>100 м&sup2;</td><td>$1.85M&ndash;$2.25M</td><td>$103k&ndash;$125k</td></tr>
<tr><td>150 м&sup2;</td><td>$2.77M&ndash;$3.38M</td><td>$154k&ndash;$188k</td></tr>
<tr><td>200 м&sup2;</td><td>$3.70M&ndash;$4.50M</td><td>$206k&ndash;$250k</td></tr>
<tr><td>250 м&sup2;</td><td>$4.63M&ndash;$5.63M</td><td>$257k&ndash;$313k</td></tr>
</tbody></table></div>
<p class="text-muted small">Ориентир: $18,500&ndash;$22,500 MXN/м&sup2; стандартная отделка. USD/MXN &asymp; 18. Без земли, бассейна и мебели.</p>
<p>Эти 8% сверх Плая-дель-Кармен &mdash; четыре конкретные вещи, а не наценка за адрес: контролируемый въезд с регистрацией рабочих, ограниченные часы работ, более длинная логистика материалов внутри посёлка и морская спецификация, которой требуют участки у канала и у моря.</p>"""),
  ("Статьи, о которых забывают",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Статья</th><th>Что выяснить</th></tr></thead><tbody>
<tr><td><strong>Взнос HOA</strong></td><td>Текущая сумма именно по этому участку, бюджет за ней и динамика за пять лет. Участки у канала и у марины часто платят больше.</td></tr>
<tr><td><strong>Причал или место стоянки</strong></td><td>В собственности, в аренде или закреплён &mdash; юридически и при перепродаже это три разные вещи &mdash; и сколько стоит в год. Причальные работы разрешаются отдельно от дома.</td></tr>
<tr><td><strong>Набережная стена канала</strong></td><td>Состояние, оценённое тем, кто не продаёт вам объект. Её ремонт &mdash; отдельный проект.</td></tr>
<tr><td><strong>Архитектурный комитет</strong></td><td>Подача, цикл рассмотрения и залог: $60,000&ndash;$250,000 MXN и минимум один круг согласования в графике.</td></tr>
<tr><td><strong>Морская спецификация</strong></td><td>Крепёж 316, анодированный или с морским покрытием алюминий, увеличенный защитный слой бетона. Дороже на стройке и многократно дешевле за десятилетие.</td></tr>
</tbody></table></div>
<p>Разрешения идут через муниципалитет <strong>Солидаридад</strong> &mdash; тот же путь, что и Плая-дель-Кармен &mdash; при этом архитектурное согласование посёлка на практике стоит раньше.</p>"""),
  ("Участок у канала: что меняется технически",
   """<ul>
<li><strong>Высокий уровень грунтовых вод.</strong> Котлованы, цистерна и чаша бассейна требуют водопонижения и проверки на всплытие &mdash; опорожнённый в неподходящий момент бассейн может всплыть.</li>
<li><strong>Постоянный солевой аэрозоль</strong> с воды, а не сезонная нагрузка. Здесь нержавейка 316 перестаёт быть предпочтением.</li>
<li><strong>Штормовая экспозиция.</strong> Участки у воды получают полную ветровую нагрузку и, при серьёзном событии, нагонную волну. Триплекс или ударостойкое остекление на фасаде к воде &mdash; спецификация, по которой мы не уступаем.</li>
<li><strong>Береговые сооружения</strong> на урезе воды имеют собственные требования к проекту и согласованию.</li>
</ul>
<p>Дом 150 м&sup2; строится примерно <strong>7&ndash;10 месяцев</strong> от лицензии, а ограниченные часы работ сдвигают график к верхней границе. Договор с фиксированной ценой, постатейной сметой и оплатой по проверенному факту.</p>"""),
 ],
 "faq": [
  ("Сколько стоит построить дом в Пуэрто-Авентурас?",
   "Около $2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD) под ключ за 150 м&sup2; со стандартной отделкой, без земли, бассейна и мебели &mdash; примерно $18,500&ndash;$22,500 MXN/м&sup2;, около 8% выше Плая-дель-Кармен."),
  ("Почему дороже, чем в Плая-дель-Кармен?",
   "Четыре конкретные причины: контролируемый въезд с регистрацией рабочих, ограниченные часы работ, более длинная логистика материалов внутри посёлка и морская спецификация для участков у канала и у моря."),
  ("Какие расходы вне сметы стройки?",
   "Взнос HOA по конкретному участку, плата за причал, ремонт набережной стены при её износе и подача в комитет с залогом &mdash; примерно $60,000&ndash;$250,000 MXN. Причальные работы разрешаются отдельно от дома."),
  ("Нужно ли согласование посёлка помимо муниципалитета?",
   "Да, и на практике посёлок идёт первым. Лицензия и DRO оформляются в Солидаридад, а архитектурный комитет проверяет высоту, отступы, материалы, цвета и ограждения. Подавайте на стадии эскиза: непредусмотренный круг согласования &mdash; самая частая задержка здесь."),
  ("Что меняется на участке у канала?",
   "Водопонижение и проверка на всплытие для котлованов и бассейна, полная морская спецификация из-за постоянного солевого аэрозоля, ударостойкое остекление на фасаде к воде из-за штормовой экспозиции и отдельное согласование любых сооружений на урезе воды."),
 ],
}

Z[("ru","akumal")] = {
 "title": "Сколько Стоит Построить Дом в Акумале 2026",
 "desc": "Стоимость стройки в Акумале 2026 и почему итог определяет экологическое досье, а не стены. Черепахи, очистные, транспорт и календарь разрешений.",
 "lead": "Дом 150 м&sup2; в <strong>Акумале</strong> стоит примерно <strong>$2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD)</strong> под ключ в 2026 году. Но на участке в Акумале стройка &mdash; предсказуемая половина бюджета: экологическое досье, очистные и календарь разрешений разводят два внешне одинаковых проекта.",
 "sections": [
  ("Стоимость под ключ по площади дома",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Площадь</th><th>Под ключ (MXN)</th><th>Под ключ (USD)</th></tr></thead><tbody>
<tr><td>100 м&sup2;</td><td>$1.90M&ndash;$2.35M</td><td>$106k&ndash;$131k</td></tr>
<tr><td>150 м&sup2;</td><td>$2.85M&ndash;$3.52M</td><td>$158k&ndash;$196k</td></tr>
<tr><td>200 м&sup2;</td><td>$3.80M&ndash;$4.70M</td><td>$211k&ndash;$261k</td></tr>
<tr><td>250 м&sup2;</td><td>$4.75M&ndash;$5.88M</td><td>$264k&ndash;$326k</td></tr>
</tbody></table></div>
<p class="text-muted small">Ориентир: $19,000&ndash;$23,500 MXN/м&sup2; стандартная отделка. USD/MXN &asymp; 18. Без земли, бассейна и мебели.</p>
<p>Это примерно на 12% выше Плая-дель-Кармен: доставка каждого материала по коридору, морская спецификация из-за солевой нагрузки и меньшая местная база подрядчиков, из-за чего часть бригад приезжает.</p>"""),
  ("Статьи, которые есть только в Акумале",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Статья</th><th>MXN</th><th>Почему</th></tr></thead><tbody>
<tr><td>Экологические изыскания и разрешение</td><td>$80,000&ndash;$350,000</td><td>Объём задаёт растительность и близость к берегу, а не площадь дома</td></tr>
<tr><td>Очистные + поглощающий колодец</td><td>$120,000&ndash;$380,000</td><td>Канализации нет; очистка перед инфильтрацией &mdash; ядро досье</td></tr>
<tr><td>Освещение, совместимое с гнездованием</td><td>$30,000&ndash;$120,000</td><td>Низкое, экранированное, янтарное или красное на фасадах к пляжу</td></tr>
<tr><td>Съёмка ZOFEMAT и проверка концессии</td><td>$20,000&ndash;$80,000</td><td>Только на участках в федеральной морской зоне</td></tr>
<tr><td>Геология по пятну застройки</td><td>$25,000&ndash;$60,000</td><td>Карст: полость может быть в двух метрах от хорошего основания</td></tr>
</tbody></table></div>
<p>Четыре из пяти статей масштабируются с <em>участком</em>, а не с домом. Поэтому компактный дом в Акумале дороже за метр, чем большой, и поэтому самая дешёвая экономия здесь &mdash; выбрать участок с действующим экологическим разрешением и коммуникациями на границе.</p>"""),
  ("Календарь разрешений и цена ожидания",
   """<p>Акумаль относится к муниципалитету <strong>Тулум</strong>, а не к Солидаридад &mdash; это удивляет владельцев, ведь Плая-дель-Кармен ближе. Экологическая экспертиза Тулума самая требовательная на побережье, и следствие &mdash; календарь:</p>
<ul>
<li><strong>Экологическое досье:</strong> 4&ndash;9 месяцев на участке с растительностью или у берега.</li>
<li><strong>Рассмотрение лицензии при полном комплекте:</strong> 4&ndash;12 недель.</li>
<li><strong>Реалистично от покупки до начала работ:</strong> 6&ndash;14 месяцев.</li>
</ul>
<p>Эти месяцы &mdash; реальная статья: земля и капитал заморожены без дохода. Поэтому участок с действующим разрешением продаётся с премией &mdash; и обычно она оправдана.</p>
<p>Отдельный пункт графика для этого участка побережья: гнездование черепах идёт примерно с <strong>мая по октябрь</strong>, с ограничениями на тяжёлые работы, яркий свет и активность на песке. Шумные наружные этапы планируйте вне этого окна, а отделку &mdash; внутри него.</p>
<p>Сама стройка занимает около <strong>7&ndash;10 месяцев</strong> для 150 м&sup2;. Фиксированная цена с постатейной сметой, а экологические условия &mdash; приживаемость посадок, журнал очистных, соблюдение освещения &mdash; должны быть закреплены за кем-то и после сдачи: они действуют весь срок жизни объекта.</p>"""),
 ],
 "faq": [
  ("Сколько стоит построить дом в Акумале в 2026 году?",
   "Около $2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD) под ключ за 150 м&sup2; со стандартной отделкой &mdash; примерно $19,000&ndash;$23,500 MXN/м&sup2;, на 12% выше Плая-дель-Кармен. Земля, бассейн, мебель и экологические статьи считаются отдельно."),
  ("Какие дополнительные расходы у участка в Акумале?",
   "Экологические изыскания и разрешение $80,000&ndash;$350,000, очистные с поглощающим колодцем $120,000&ndash;$380,000, освещение по правилам гнездования $30,000&ndash;$120,000, съёмка ZOFEMAT $20,000&ndash;$80,000 и геология $25,000&ndash;$60,000. Большинство зависит от участка, а не от дома."),
  ("Какой муниципалитет выдаёт разрешения в Акумале?",
   "Тулум, а не Солидаридад, хотя Плая-дель-Кармен ближе. Его экологическая экспертиза самая требовательная на побережье, поэтому реалистично планировать 6&ndash;14 месяцев от покупки до начала работ."),
  ("Правила гнездования влияют на график?",
   "Да. Сезон идёт примерно с мая по октябрь и ограничивает тяжёлые работы, яркое освещение и активность на песке у пляжа. Шумные наружные этапы &mdash; вне сезона, отделка &mdash; внутри. Правила освещения действуют и для готового дома."),
  ("Маленький дом дешевле за метр в Акумале?",
   "Нет, дороже за метр. Экологическое досье, геология, очистные и подключение стоят почти одинаково для 80 м&sup2; и для 200 м&sup2;, поэтому на компактном доме эти фиксированные статьи весят гораздо больше."),
 ],
}

Z[("ru","puerto-morelos")] = {
 "title": "Сколько Стоит Построить Дом в Пуэрто-Морелосе 2026",
 "desc": "Пуэрто-Морелос строит по ценам Плая-дель-Кармен на более дешёвой земле. Диапазоны 2026, требования к сбросу у рифового парка и Рута-де-лос-Сеноте.",
 "lead": "Дом 150 м&sup2; в <strong>Пуэрто-Морелосе</strong> стоит примерно <strong>$2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD)</strong> под ключ в 2026 году &mdash; по стройке фактически на уровне Плая-дель-Кармен, но на в целом более дешёвой земле. Это сочетание и делает его тихим выбором по соотношению цены и качества.",
 "sections": [
  ("Стоимость под ключ и три субрынка",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Площадь</th><th>Под ключ (MXN)</th><th>Под ключ (USD)</th></tr></thead><tbody>
<tr><td>100 м&sup2;</td><td>$1.70M&ndash;$2.10M</td><td>$94k&ndash;$117k</td></tr>
<tr><td>150 м&sup2;</td><td>$2.55M&ndash;$3.15M</td><td>$142k&ndash;$175k</td></tr>
<tr><td>200 м&sup2;</td><td>$3.40M&ndash;$4.20M</td><td>$189k&ndash;$233k</td></tr>
<tr><td>250 м&sup2;</td><td>$4.25M&ndash;$5.25M</td><td>$236k&ndash;$292k</td></tr>
</tbody></table></div>
<p class="text-muted small">Ориентир: $17,000&ndash;$21,000 MXN/м&sup2; стандартная отделка. USD/MXN &asymp; 18. Без земли, бассейна и мебели.</p>
<ul>
<li><strong>У моря:</strong> $26,000&ndash;$38,000+ MXN/м&sup2; с морской спецификацией и более тяжёлым экологическим досье.</li>
<li><strong>Рута-де-лос-Сеноте:</strong> $14,000&ndash;$19,000 на участке с коммуникациями и $17,000&ndash;$24,000 при автономном варианте &mdash; дешевле земля, больше инфраструктуры.</li>
</ul>"""),
  ("Собственный муниципалитет с 2016 года",
   """<p>Пуэрто-Морелос отделился от Бенито Хуарес в 2016 году и теперь сам выдаёт назначение земли, лицензии, выравнивания и акты ввода. Три практических следствия:</p>
<ul>
<li><strong>Подаём здесь, а не в Канкуне.</strong> Советы по практике Бенито Хуарес устарели, как и опыт соседа, строившего до 2016 года.</li>
<li><strong>Проверяйте параметры участка на сегодня.</strong> Градостроительные документы муниципалитета относительно новые и обновлялись: подтверждайте плотность, высоту и разрешённое использование именно по вашему участку.</li>
<li><strong>Маленькая администрация &mdash; прямая администрация.</strong> Те, кто рассматривает досье, доступны, поэтому полный комплект здесь особенно ценен, а неполный &mdash; особенно медленен.</li>
</ul>
<p>Экспертиза штата (SEMA), федеральная юрисдикция там, где она применима, CONAGUA по воде и ZOFEMAT со стороны пляжа действуют как и на остальном побережье.</p>"""),
  ("Что риф и водно-болотные угодья добавляют к спецификации",
   """<ul>
<li><strong>Качество сброса &mdash; ядро досье.</strong> Очистка перед инфильтрацией, корректно рассчитанная, с отдельным отводом промывной воды бассейна &mdash; $90,000&ndash;$350,000 MXN в зависимости от наполняемости. То, что инфильтруется здесь, доходит до водоносного горизонта, а затем до рифа.</li>
<li><strong>Мангры не обсуждаются.</strong> На участках у водно-болотных угодий границу охраняемой растительности нужно установить до первого плана &mdash; у части продаваемых участков застраиваемая площадь значительно меньше площади по документам.</li>
<li><strong>Отступы от сенотов</strong> действуют вглубь материка, с ограничениями на то, что может инфильтроваться рядом.</li>
<li><strong>Отметка чистого пола</strong> на низких участках у болот или берега задаётся с учётом затопления и нагонной волны. Это решение стадии проекта, позже не исправляется.</li>
<li><strong>На Рута-де-лос-Сеноте</strong> закладывайте подъездную дорогу ($40,000&ndash;$300,000) и либо расширение сети CFE &mdash; запросите цену до покупки, от $150,000 до более $900,000 &mdash; либо спроектированную автономию: солнечные панели, накопитель, скважина с водоподготовкой и сбор дождевой воды.</li>
</ul>
<p>Строительство 150 м&sup2; занимает около <strong>7&ndash;10 месяцев</strong>.</p>"""),
 ],
 "faq": [
  ("Сколько стоит построить дом в Пуэрто-Морелосе?",
   "Около $2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD) под ключ за 150 м&sup2; в посёлке или вглубь материка &mdash; примерно $17,000&ndash;$21,000 MXN/м&sup2;, фактически на уровне Плая-дель-Кармен. У моря $26,000&ndash;$38,000+, на Рута-де-лос-Сеноте $14,000&ndash;$24,000 в зависимости от коммуникаций."),
  ("Какой муниципалитет выдаёт разрешения?",
   "Сам Пуэрто-Морелос: он отделился от Бенито Хуарес (Канкун) в 2016 году. Рекомендации по канкунской практике устарели, а поскольку градостроительные документы новые, плотность, высоту и использование стоит проверять актуально."),
  ("Можно ли строить рядом с манграми?",
   "Не в самой охраняемой растительности, и её границу нужно установить до разработки плана. У части продаваемых участков застраиваемая площадь заметно меньше документальной, поэтому проверяйте это до покупки."),
  ("Что означает рифовый национальный парк для стройки?",
   "Что качество сброса становится центральным техническим вопросом досье. Очистка перед инфильтрацией по фактической наполняемости, с отдельным отводом промывной воды бассейна, стоит $90,000&ndash;$350,000 MXN и проверяется внимательно."),
  ("Дешевле ли строить на Рута-де-лос-Сеноте?",
   "Земля &mdash; да, стройка около $14,000&ndash;$19,000 MXN/м&sup2; на участке с коммуникациями. Но у многих участков нет ни CFE, ни воды: закладывайте расширение сети &mdash; цену запрашивайте до покупки, от $150,000 до более $900,000 &mdash; либо автономную систему, плюс $40,000&ndash;$300,000 на подъезд."),
 ],
}

Z[("ru","playacar")] = {
 "title": "Сколько Стоит Построить Дом в Плаякаре 2026",
 "desc": "Плаякар застроен — большинство проектов это реконструкция или снос под новый дом. Диапазоны 2026, стоимость сноса, архитектурный комитет, Фаза I и II.",
 "lead": "Дом 150 м&sup2; в <strong>Плаякаре</strong> стоит примерно <strong>$3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD)</strong> под ключ в 2026 году, около 25% выше базового уровня Плая-дель-Кармен. Но Плаякар практически застроен, поэтому реальный вопрос не в цене нового дома, а в том, реконструировать существующий или снести его.",
 "sections": [
  ("Реконструкция или снос: арифметика",
   """<p>Почти каждый проект в Плаякаре &mdash; это новый дом после сноса, крупная реконструкция или застройка одного из немногих оставшихся участков. Выбор между первыми двумя делается после обследования, а не после осмотра: дома этого возраста на этом побережье несут предсказуемый дефект &mdash; хлоридную коррозию арматуры на торцах плит, балконах, колоннах и парапетах.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Позиция</th><th>MXN</th></tr></thead><tbody>
<tr><td>Обследование со вскрытиями в характерных местах</td><td>$40,000&ndash;$150,000</td></tr>
<tr><td>Снос и вывоз, типовой дом</td><td>$180,000&ndash;$600,000</td></tr>
<tr><td>Программа ремонта бетона при сохранении</td><td>По итогам обследования &mdash; может превысить снос</td></tr>
<tr><td>Полная реконструкция, премиум-отделка</td><td>$14,000&ndash;$26,000 MXN/м&sup2;</td></tr>
<tr><td>Новое строительство, премиум</td><td>$24,000&ndash;$30,000 MXN/м&sup2;</td></tr>
<tr><td>Новое строительство, люкс</td><td>$30,000&ndash;$42,000 MXN/м&sup2;</td></tr>
</tbody></table></div>
<p>Честный порог: как только ремонт конструкций приближается к 25&ndash;30% стоимости нового дома, вы платите цену новостройки за высоты потолков, ориентацию и планировку старого здания. В Плаякаре есть и контраргумент: участки не воспроизводятся, взрослые деревья охраняются и стоят денег, а крепкий дом девяностых с хорошими высотами во Фазе II может быть достоин сохранения.</p>"""),
  ("Стоимость под ключ по площади дома",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Площадь</th><th>Под ключ (MXN)</th><th>Под ключ (USD)</th></tr></thead><tbody>
<tr><td>100 м&sup2;</td><td>$2.10M&ndash;$2.60M</td><td>$117k&ndash;$144k</td></tr>
<tr><td>150 м&sup2;</td><td>$3.15M&ndash;$3.90M</td><td>$175k&ndash;$217k</td></tr>
<tr><td>200 м&sup2;</td><td>$4.20M&ndash;$5.20M</td><td>$233k&ndash;$289k</td></tr>
<tr><td>250 м&sup2;</td><td>$5.25M&ndash;$6.50M</td><td>$292k&ndash;$361k</td></tr>
</tbody></table></div>
<p class="text-muted small">Ориентир: $21,000&ndash;$26,000 MXN/м&sup2; от стандартной до премиум-отделки. USD/MXN &asymp; 18. Без земли, бассейна и мебели.</p>
<p>Эти 25% над базовым уровнем &mdash; ограниченный доступ по узким улицам, регистрация рабочих и лимит часов, процедура архитектурного комитета, защита деревьев, морская спецификация и уровень отделки, которого ждёт местный рынок. На пляжном участке Плаякара добавляются федеральная морская зона и ударостойкое остекление к морю: там $42,000&ndash;$60,000+ MXN/м&sup2;.</p>"""),
  ("Комитет, деревья и Фаза I против Фазы II",
   """<p><strong>Архитектурное согласование здесь реально</strong> и именно на нём теряются графики. Ожидайте проверки высоты, объёма и отступов строже муниципальных, формы и материалов кровли, обработки фасада и палитры, оград и заборов и, главное, вырубки деревьев &mdash; взрослый полог часть того, что посёлок защищает, и каждое дерево обосновывается. Подавайте на стадии эскиза вместе с дендропланом и закладывайте хотя бы один круг рассмотрения плюс залог.</p>
<p><strong>Фаза I и Фаза II &mdash; разные места.</strong> Фаза I ближе к городу и парому: плотнее, участки меньше, реальная пешая доступность Пятой авеню и въезд для стройки по узким улицам, что удорожает. Фаза II крупнее и спокойнее вокруг поля для гольфа, с большими участками, взрослой растительностью и местом под серьёзную виллу &mdash; а соседство с полем делает остекление и зенитные фонари практическим вопросом.</p>
<p>Разрешения оформляются в <strong>Солидаридад</strong>, стройка занимает около <strong>7&ndash;10 месяцев</strong> для 150 м&sup2; плюс снос, если он нужен.</p>"""),
 ],
 "faq": [
  ("Сколько стоит строительство в Плаякаре?",
   "Около $3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD) под ключ за 150 м&sup2; &mdash; примерно $21,000&ndash;$26,000 MXN/м&sup2;, на 25% выше базового уровня Плая-дель-Кармен. Люкс-отделка $30,000&ndash;$42,000, пляжные участки $42,000&ndash;$60,000+."),
  ("Реконструировать существующий дом или снести?",
   "Сначала обследование со вскрытиями за $40,000&ndash;$150,000 MXN: дома этого возраста часто несут хлоридную коррозию арматуры. Когда ремонт конструкций приближается к 25&ndash;30% стоимости нового дома, снос обычно правильнее; снос и вывоз стоят $180,000&ndash;$600,000."),
  ("Что проверяет архитектурный комитет Плаякара?",
   "Высоту, объём и отступы строже муниципальных, форму и материалы кровли, фасад и цвет, ограды и заборы, а также вырубку каждого дерева, которая обосновывается отдельно. Он же задаёт правила стройки: регистрацию рабочих, часы, поставки, хранение и залог."),
  ("Чем Фаза I отличается от Фазы II при строительстве?",
   "Во Фазе I участки меньше и плотнее, а въезд по узким улицам удорожает работы, зато есть реальная пешая доступность Пятой авеню. Во Фазе II крупные участки у поля для гольфа со взрослой растительностью &mdash; и соседство с полем делает остекление практическим вопросом."),
  ("Почему Плаякар дороже остального Плая-дель-Кармен на 25%?",
   "Ограниченный доступ по узким улицам, регистрация рабочих и лимит часов, процедура комитета, защита деревьев во время стройки, морская спецификация и ожидаемый уровень отделки. Каждый пункт &mdash; реальная статья, а не наценка за адрес."),
 ],
}

Z[("ru","mayakoba")] = {
 "title": "Сколько Стоит Построить Дом в Майякобе 2026",
 "desc": "Майякоба — самое дорогое место для стройки на Ривьере Майя. Диапазоны за м² 2026, что на самом деле включает спецификация уровня резорта и почему.",
 "lead": "Дом 150 м&sup2; в <strong>Майякобе</strong> стоит примерно <strong>$3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD)</strong> под ключ в 2026 году &mdash; самый высокий диапазон на побережье, около 42% выше базового уровня Плая-дель-Кармен. Впрочем, по нижней границе здесь почти не строят, и эта страница объясняет почему.",
 "sections": [
  ("Стоимость по площади и реалистичная цифра",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Площадь</th><th>Под ключ (MXN)</th><th>Под ключ (USD)</th></tr></thead><tbody>
<tr><td>150 м&sup2;</td><td>$3.60M&ndash;$4.50M</td><td>$200k&ndash;$250k</td></tr>
<tr><td>250 м&sup2;</td><td>$6M&ndash;$7.50M</td><td>$333k&ndash;$417k</td></tr>
<tr><td>350 м&sup2;</td><td>$8.40M&ndash;$10.50M</td><td>$467k&ndash;$583k</td></tr>
<tr><td>500 м&sup2;</td><td>$12M&ndash;$15M</td><td>$667k&ndash;$833k</td></tr>
</tbody></table></div>
<p class="text-muted small">Ориентир: $24,000&ndash;$30,000 MXN/м&sup2; от стандартной до премиум-отделки. USD/MXN &asymp; 18. Без земли, бассейна и мебели.</p>
<p>Это входной диапазон. Реально в мастер-плане строят дома 300&ndash;600 м&sup2; авторского уровня, что даёт фактические <strong>$35,000&ndash;$55,000 MXN/м&sup2;</strong> с учётом архитектурного проекта, импортной фурнитуры, полной автоматизации, проектного бассейна и взрослого озеленения. Кто считает виллу в Майякобе от $24,000, считает дом, который не пройдёт архитектурное согласование.</p>"""),
  ("Что на самом деле покупает надбавка",
   """<ul>
<li><strong>Контроль архитектуры.</strong> Мастер-план, выстроенный вокруг работы отелей, проверяет архитектуру, материалы, цвет, ландшафт и освещение по стандарту соседних резортов. Подачи подробные, циклы рассмотрения реальные, а удешевить фасад попросту нельзя.</li>
<li><strong>Ожидания по отделке.</strong> Сопоставимые объекты &mdash; брендированные резиденции. Столярка, камень, остекление и фурнитура закладываются под этот уровень, а точный монтаж стоит дороже самих материалов.</li>
<li><strong>Дисциплина стройплощадки.</strong> Работа идёт внутри действующей люксовой среды: контролируемый доступ, регистрация рабочих, ограниченные часы, закрытые ограждения, лимиты шума, обязательства по уборке и залог. Каждый пункт &mdash; часы графика.</li>
<li><strong>Природная среда.</strong> Мастер-план организован вокруг лагун, каналов и мангров. Сохранённая растительность, отступы, дренаж и сброс регулируются ещё и на уровне сообщества.</li>
<li><strong>Морская и влажностная спецификация</strong> целиком: нержавейка 316, анодированный или с морским покрытием алюминий, увеличенный защитный слой бетона, вентилируемая столярка.</li>
<li><strong>Дефицит.</strong> Мало жилых участков, каждый проект штучный &mdash; нет повторяемости, на которую можно разложить проектирование и управление.</li>
</ul>"""),
  ("График, разрешения и что ещё заложить",
   """<p>Разрешения идут через муниципалитет <strong>Солидаридад</strong>, при этом архитектурное согласование сообщества стоит раньше, а экологическая экспертиза серьёзно относится к лагуне и манграм. Подавайте в сообщество на стадии эскиза: довести проект до конца и только потом отправить его на согласование &mdash; это потеря квартала.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Помимо стройки</th><th>MXN</th></tr></thead><tbody>
<tr><td>Авторское проектирование и инженерия этого уровня</td><td>10&ndash;15% от стройки</td></tr>
<tr><td>Подача в сообщество, циклы рассмотрения, залог</td><td>$150,000&ndash;$600,000</td></tr>
<tr><td>Проектный бассейн с оборудованием</td><td>$900,000&ndash;$3,500,000</td></tr>
<tr><td>Взрослое озеленение и полив</td><td>$400,000&ndash;$2,000,000</td></tr>
<tr><td>Меблировка виллы этого класса</td><td>$1,500,000&ndash;$6,000,000</td></tr>
<tr><td>Взнос сообщества</td><td>Регулярный &mdash; уточнять по участку</td></tr>
</tbody></table></div>
<p>Стройка занимает около <strong>10&ndash;16 месяцев</strong> для виллы такой спецификации &mdash; дольше нормы побережья, потому что ограниченные часы, циклы согласования и точность отделки требуют времени.</p>"""),
 ],
 "faq": [
  ("Сколько стоит построить дом в Майякобе?",
   "Входной диапазон $24,000&ndash;$30,000 MXN/м&sup2;, то есть $3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD) за 150 м&sup2;. Фактически строят дома 300&ndash;600 м&sup2; по $35,000&ndash;$55,000 MXN/м&sup2; с учётом авторского проекта, импортной отделки, автоматизации, бассейна и взрослого озеленения."),
  ("Почему Майякоба самое дорогое место на побережье?",
   "Контроль архитектуры по стандарту резорта, ожидания отделки на уровне брендированных резиденций, дисциплина стройки внутри действующей люксовой среды, управление природной средой вокруг лагун и мангров, полная морская спецификация и дефицит участков без эффекта повторяемости."),
  ("Что ещё заложить помимо стоимости стройки?",
   "Проектирование и инженерию 10&ndash;15% от стройки, подачу и залог $150,000&ndash;$600,000, проектный бассейн $900,000&ndash;$3,500,000, взрослое озеленение $400,000&ndash;$2,000,000, меблировку $1,500,000&ndash;$6,000,000 и регулярный взнос сообщества."),
  ("Сколько строится вилла в Майякобе?",
   "Около 10&ndash;16 месяцев для виллы такой спецификации, дольше нормы побережья. Ограниченные часы работ, циклы согласования сообщества и требуемая точность отделки забирают дополнительное время."),
  ("Кто утверждает проект?",
   "Муниципалитет Солидаридад по назначению земли, лицензии, выравниванию и DRO, и архитектурное согласование сообщества, которое на практике идёт первым и проверяет архитектуру, материалы, цвет, ландшафт и освещение."),
 ],
}

Z[("ru","corasol")] = {
 "title": "Сколько Стоит Построить Дом в Корасоле 2026",
 "desc": "Стоимость стройки в Корасоле 2026 и что значит строить внутри развивающегося мастер-плана: инфраструктура очередями, комитет, поле для гольфа, доступ.",
 "lead": "Дом 150 м&sup2; в <strong>Корасоле</strong> стоит примерно <strong>$3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD)</strong> под ключ в 2026 году, около 30% выше базового уровня Плая-дель-Кармен. В Корасоле находится и наш офис, так что эта страница пишется в нескольких минутах ходьбы от темы.",
 "sections": [
  ("Стоимость под ключ по площади дома",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Площадь</th><th>Под ключ (MXN)</th><th>Под ключ (USD)</th></tr></thead><tbody>
<tr><td>150 м&sup2;</td><td>$3.30M&ndash;$4.12M</td><td>$183k&ndash;$229k</td></tr>
<tr><td>200 м&sup2;</td><td>$4.40M&ndash;$5.50M</td><td>$244k&ndash;$306k</td></tr>
<tr><td>300 м&sup2;</td><td>$6.60M&ndash;$8.25M</td><td>$367k&ndash;$458k</td></tr>
<tr><td>450 м&sup2;</td><td>$9.90M&ndash;$12.38M</td><td>$550k&ndash;$688k</td></tr>
</tbody></table></div>
<p class="text-muted small">Ориентир: $22,000&ndash;$27,500 MXN/м&sup2; от стандартной до премиум-отделки. USD/MXN &asymp; 18. Без земли, бассейна и мебели.</p>
<p>Большинство домов здесь крупнее 150 м&sup2;: участки и рынок тянут к виллам 250&ndash;450 м&sup2; с бассейном, эксплуатируемой кровлей и проектным садом. Считайте пакет целиком &mdash; на вилле 300 м&sup2; бассейн, озеленение, мебель и гонорары обычно добавляют 35&ndash;50% сверх стоимости стройки.</p>"""),
  ("Строительство в посёлке, который сам ещё строится",
   """<ul>
<li><strong>Инфраструктура приходит очередями.</strong> Уточните по вашему участку, что реально проложено на границе сегодня &mdash; электрическая мощность, вода, канализация, покрытие улицы &mdash; и что лишь запланировано. Разрыв между «в посёлке будет» и «на участке есть» и есть бюджетный риск.</li>
<li><strong>Соседи будут строиться.</strong> Другие дома и работы сообщества идут годами: шум и трафик во время вашего проживания и общие проезды во время вашей стройки.</li>
<li><strong>Архитектурное согласование активно и развивается.</strong> Комитет проверяет высоту, объём, материалы, цвет, ограждения и ландшафт, чтобы сохранить целостный облик в незавершённом посёлке. Подавайте на стадии эскиза.</li>
<li><strong>Правила доступа и стройки.</strong> Регистрация рабочих, контролируемый въезд, фиксированные часы поставок, лимиты хранения на участке, уборка улицы и залог. Закладывайте $80,000&ndash;$300,000 MXN на подачу, залог и организацию доступа.</li>
<li><strong>Соседство с полем для гольфа</strong> ставит вопрос остекления и зенитных фонарей &mdash; залетающие мячи реальный и просчитываемый риск &mdash; плюс стык полива и дренажа с полем.</li>
</ul>"""),
  ("Условия площадки, разрешения и график",
   """<p>Корасоль относится к муниципалитету <strong>Солидаридад</strong>: сертификат использования земли, выравнивание, лицензия и Director Responsable de Obra, при этом архитектурное согласование сообщества на практике идёт первым. Экологические требования действуют как и на остальном побережье, а карст требует геологии со скважинами по фактическому пятну застройки &mdash; хорошее основание и полость в двух метрах здесь одинаково нормальны.</p>
<ul>
<li><strong>Морская спецификация действует.</strong> Корасоль достаточно близко к морю, чтобы нержавейка 316, анодированный или с морским покрытием алюминий и увеличенный защитный слой бетона были правильным решением, а не опцией.</li>
<li><strong>Проектируйте кровлю как террасу сразу,</strong> если высота позволяет. На участках с видом на поле или море это самый ценный метр дома, а переделка обходится в разы дороже.</li>
<li><strong>Продумайте технические помещения:</strong> цистерна, станция давления, водоподготовка под местную жёсткость, оборудование бассейна и места кондиционеров &mdash; всё с доступом для обслуживания.</li>
</ul>
<p>Стройка занимает около <strong>8&ndash;12 месяцев</strong> для виллы 250&ndash;300 м&sup2; и дольше, если согласование идёт больше одного круга. Если покупаете участок сейчас, а строите позже, получите письменное подтверждение состояния коммуникаций на границе участка до сделки.</p>"""),
 ],
 "faq": [
  ("Сколько стоит построить дом в Корасоле?",
   "Около $3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD) под ключ за 150 м&sup2; &mdash; примерно $22,000&ndash;$27,500 MXN/м&sup2;, на 30% выше базового уровня Плая-дель-Кармен. Большинство домов здесь 250&ndash;450 м&sup2;, где бассейн, озеленение, мебель и гонорары добавляют 35&ndash;50%."),
  ("Что проверить перед покупкой участка в Корасоле?",
   "Какая инфраструктура реально проложена на границе участка сегодня &mdash; электрическая мощность, вода, канализация, покрытие улицы &mdash; против того, что лишь запланировано. В развивающемся мастер-плане именно здесь и прячется бюджетный риск."),
  ("Комитет добавляет стоимость и время?",
   "И то, и другое. Закладывайте $80,000&ndash;$300,000 MXN на подачу, залог и организацию доступа и минимум один круг рассмотрения в графике, плюс регистрацию рабочих, контролируемый въезд, часы поставок и уборку улицы."),
  ("Что меняет соседство с полем для гольфа?",
   "Спецификацию остекления и зенитных фонарей, поскольку залетающие мячи &mdash; реальный и просчитываемый риск, а также стык полива и дренажа с полем. Это решается в проекте, а не заменой стёкол потом."),
  ("Сколько строится вилла в Корасоле?",
   "Около 8&ndash;12 месяцев для 250&ndash;300 м&sup2; от лицензии до сдачи и дольше, если согласование идёт больше одного круга. Ограниченные часы и контролируемый доступ смещают график к верхней границе."),
 ],
}

Z[("ru","aldea-zama")] = {
 "title": "Сколько Стоит Построить Дом в Альдеа-Зама 2026",
 "desc": "Стоимость в Альдеа-Зама 2026 плюс статья, которую не закладывают: календарь разрешений Тулума. Ограничения высоты, надёжность электросети, мастер-план.",
 "lead": "Дом 150 м&sup2; в <strong>Альдеа-Зама</strong> стоит примерно <strong>$3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD)</strong> под ключ в 2026 году, около 20% выше базового уровня Плая-дель-Кармен. Цифра стройки простая. В Тулуме не закладывают другое &mdash; время.",
 "sections": [
  ("Стоимость под ключ по площади дома",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Площадь</th><th>Под ключ (MXN)</th><th>Под ключ (USD)</th></tr></thead><tbody>
<tr><td>100 м&sup2;</td><td>$2.05M&ndash;$2.50M</td><td>$114k&ndash;$139k</td></tr>
<tr><td>150 м&sup2;</td><td>$3.08M&ndash;$3.75M</td><td>$171k&ndash;$208k</td></tr>
<tr><td>200 м&sup2;</td><td>$4.10M&ndash;$5M</td><td>$228k&ndash;$278k</td></tr>
<tr><td>300 м&sup2;</td><td>$6.15M&ndash;$7.50M</td><td>$342k&ndash;$417k</td></tr>
</tbody></table></div>
<p class="text-muted small">Ориентир: $20,500&ndash;$25,000 MXN/м&sup2; от стандартной до премиум-отделки. USD/MXN &asymp; 18. Без земли, бассейна и мебели.</p>
<p>Альдеа-Зама дороже регионов Тулума и Ла-Велеты по простой причине: это урбанизированный мастер-план с коммуникациями в земле, асфальтированными проездами и сложившимся характером в пешей или велосипедной доступности от пляжной дороги. Вы платите за существующую инфраструктуру, а не за ту, которую предстоит построить.</p>"""),
  ("Во что реально обходится календарь разрешений",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Этап</th><th>Срок</th></tr></thead><tbody>
<tr><td>Сертификат использования земли и выравнивание</td><td>2&ndash;8 недель</td></tr>
<tr><td>Геология (параллельно)</td><td>2&ndash;5 недель</td></tr>
<tr><td>Экологическое досье</td><td>3&ndash;8 месяцев в зависимости от растительности</td></tr>
<tr><td>Технический проект (параллельно)</td><td>6&ndash;14 недель</td></tr>
<tr><td>Рассмотрение лицензии при полном комплекте</td><td>4&ndash;12 недель</td></tr>
<tr><td><strong>Итого до начала работ</strong></td><td><strong>5&ndash;12 месяцев</strong></td></tr>
</tbody></table></div>
<p>Эти месяцы &mdash; реальная статья: земля и капитал заморожены. Сократить их можно двумя способами. Первый: запускать экологическое досье и геологию, пока архитектура ещё в эскизе &mdash; ни то, ни другое не требует финальных чертежей, и оба всё равно влияют на проект. Второй: при сравнении участков высоко ценить действующее экологическое разрешение &mdash; оно может стоить полугода и шестизначной суммы.</p>"""),
  ("Высота, электроснабжение и что здесь строят",
   """<ul>
<li><strong>Ограничения высоты строгие</strong> и соблюдаются. Правила Тулума намеренно жёстче, чем в Плая-дель-Кармен, поэтому уточните точный лимит по вашему участку до проектирования кровли &mdash; на многих участках именно эта цифра решает, получится ли сильный проект.</li>
<li><strong>Электроснабжение менее надёжно,</strong> чем в Плая-дель-Кармен. Закладывайте защиту от перенапряжений на весь дом как стандарт, а для арендной недвижимости &mdash; аккумуляторную систему на базовые нужды (интернет, контроллер бассейна, часть освещения и вентилятор) за $140,000&ndash;$330,000 MXN. Солнечные панели здесь особенно оправданы, когда насос бассейна и несколько кондиционеров выводят потребление на тариф DAC.</li>
<li><strong>Рынок здесь кондоминиумный,</strong> что и есть аргумент в пользу дома. У отдельного дома нельзя собранием отнять право краткосрочной аренды, он не платит взнос с валовой выручки и проектируется под доходность: спальни с собственными санузлами, casita с отдельным входом, эксплуатируемая кровля и бассейн в нужном ракурсе.</li>
</ul>
<p>Технически действуют обычные для Тулума пункты: очистка перед инфильтрацией по фактической наполняемости ($90,000&ndash;$250,000 MXN), водоподготовка под жёсткость, решения против термитов и влаги и геология, потому что карст здесь изобилует сенотами. Стройка занимает около <strong>7&ndash;11 месяцев</strong> для 150&ndash;200 м&sup2;.</p>"""),
 ],
 "faq": [
  ("Сколько стоит построить дом в Альдеа-Зама?",
   "Около $3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD) под ключ за 150 м&sup2; от стандартной до премиум-отделки &mdash; примерно $20,500&ndash;$25,000 MXN/м&sup2;, на 20% выше базового уровня Плая-дель-Кармен."),
  ("Почему дороже, чем в регионах Тулума?",
   "Потому что инфраструктура уже есть: урбанизированный мастер-план с коммуникациями в земле, асфальтированными проездами и сложившимся характером рядом с пляжной дорогой. На более дешёвом участке в регионе вы оплачиваете коммуникации, подъезд и среду позже сами."),
  ("Сколько ждать до начала строительства в Тулуме?",
   "Реалистично от пяти до двенадцати месяцев с момента покупки: 2&ndash;8 недель на использование земли и выравнивание, 3&ndash;8 месяцев на экологическое досье при растительности и 4&ndash;12 недель на лицензию. Запускайте досье и геологию, пока архитектура в эскизе."),
  ("Можно ли сделать эксплуатируемую кровлю в Альдеа-Зама?",
   "Зависит от лимита высоты по конкретному участку, а в Тулуме эти лимиты намеренно жёсткие и соблюдаются. Проверьте цифру до проектирования: на многих участках именно она отделяет сильный проект от компромиссного."),
  ("Что делать с отключениями электричества в Тулуме?",
   "Защита от перенапряжений на весь дом как стандарт и, для арендной недвижимости, аккумуляторы на интернет, контроллер бассейна, освещение и вентилятор за $140,000&ndash;$330,000 MXN. Солнечные панели тоже быстро окупаются, особенно на тарифе DAC."),
 ],
}

Z[("ru","playa-del-carmen")] = {
 "title": "Сколько Стоит Построить Дом в Плая-дель-Кармен 2026",
 "desc": "Эталонная цена побережья. Бюджет по этапам для дома 150 м², что входит и не входит в цену за м², дополнительные статьи и как удержать смету.",
 "lead": "Добротный семейный дом 150 м&sup2; в <strong>Плая-дель-Кармен</strong> стоит примерно <strong>$2.6M&ndash;$3.2M MXN ($145,000&ndash;$178,000 USD)</strong> под ключ в 2026 году. С этой цифрой сравнивают всё побережье, поэтому её стоит понимать по этапам, а не как одно число.",
 "sections": [
  ("Бюджет по этапам (стандартный дом 150 м²)",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Этап</th><th>% бюджета</th><th>Стоимость (MXN)</th><th>Состав</th></tr></thead><tbody>
<tr><td>Разрешения, DRO, изыскания</td><td>5%</td><td>$130,000&ndash;$160,000</td><td>Лицензия, DRO, геология, топография</td></tr>
<tr><td>Фундамент и каркас</td><td>30%</td><td>$780,000&ndash;$960,000</td><td>Плита, колонны, ригели, перекрытия</td></tr>
<tr><td>Стены и кровля</td><td>18%</td><td>$470,000&ndash;$580,000</td><td>Блок, обвязки, плита кровли</td></tr>
<tr><td>Инженерия</td><td>15%</td><td>$390,000&ndash;$480,000</td><td>Электрика, водоснабжение, канализация</td></tr>
<tr><td>Отделка</td><td>25%</td><td>$650,000&ndash;$800,000</td><td>Полы, покраска, чукум, столярка</td></tr>
<tr><td>Уборка и сдача</td><td>7%</td><td>$180,000&ndash;$220,000</td><td>Доделки, передача объекта</td></tr>
</tbody></table></div>
<p class="text-muted small">Итого под ключ &asymp; $2.6M&ndash;$3.2M MXN. Без земли, бассейна и мебели.</p>
<p>Два вывода из таблицы. Каркас &mdash; почти треть бюджета и единственный этап, где экономия в зоне сильных ветров по-настоящему опасна. А отделка с её 25% &mdash; это то, где реально живёт ваша спецификация: та же коробка с другой отделкой сдвигает итог на 20% без единого изменения в чертежах.</p>"""),
  ("Что входит и что не входит в цену за м²",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Статья</th><th>MXN</th></tr></thead><tbody>
<tr><td>Земля</td><td>Отдельно, и это самая большая переменная в Плая-дель-Кармен</td></tr>
<tr><td>Бассейн 4&times;8 м с оборудованием</td><td>$450,000&ndash;$1,200,000</td></tr>
<tr><td>Обустройство эксплуатируемой кровли (если заложена в конструкции)</td><td>$3,500&ndash;$9,000 за м&sup2;</td></tr>
<tr><td>Водоподготовка (фильтр, умягчитель, уголь, осмос)</td><td>$35,000&ndash;$95,000</td></tr>
<tr><td>Кондиционирование, 4&ndash;5 инверторных зон</td><td>$120,000&ndash;$280,000</td></tr>
<tr><td>Солнечные панели, 5&ndash;8 кВт</td><td>$115,000&ndash;$250,000</td></tr>
<tr><td>Озеленение и полив</td><td>$500&ndash;$2,000 за м&sup2;</td></tr>
<tr><td>Мебель и техника</td><td>$450,000&ndash;$1,200,000 для семейного дома</td></tr>
</tbody></table></div>
<p>Проектирование, инженерия, изыскания и разрешения вместе обычно составляют 8&ndash;14% от стоимости стройки на индивидуальном доме &mdash; частично это уже отражено в таблице этапов. Сокращать эту статью не стоит: каждая предотвращённая ею ошибка дороже всего пакета.</p>"""),
  ("Почему это эталон побережья и как удержать смету",
   """<p>Плая-дель-Кармен дешевле закрытых и премиальных зон по структурным, а не качественным причинам: широкая база поставщиков, реальная конкуренция подрядчиков, городские участки с коммуникациями, прямой путь разрешений через муниципалитет <strong>Солидаридад</strong> и отсутствие федеральной морской зоны на подавляющем большинстве участков. Всё остальное на побережье &mdash; множитель к этой цифре: Пуэрто-Морелос примерно вровень, Пуэрто-Авентурас около +8%, Акумаль +12%, Альдеа-Зама +20%, Плаякар +25%, Корасоль +30%, Майякоба +42%.</p>
<ul>
<li><strong>Фиксированная цена с постатейной сметой,</strong> а не цена за м&sup2; на словах. Единая ставка, умноженная на метры, &mdash; это не смета, а приглашение к пересмотру.</li>
<li><strong>Оплата по проверенному факту работ,</strong> а не по датам, с удержанием 5&ndash;10% до закрытия списка замечаний.</li>
<li><strong>Изменения &mdash; письменно и с ценой</strong> до начала работ. Устные договорённости &mdash; самый частый путь от твёрдой цены к открытой.</li>
<li><strong>Явный список исключений</strong> &mdash; мебель, техника, озеленение сверх границы, плата за подключения &mdash; согласованный при подписании.</li>
</ul>
<p>Дом 150 м&sup2; строится около <strong>7&ndash;10 месяцев</strong> от лицензии, плюс два-четыре месяца на предшествующие процедуры. Для быстрой оценки воспользуйтесь <a href="/kalkulyator/">калькулятором стоимости</a>.</p>"""),
 ],
 "faq": [
  ("Сколько стоит построить дом в Плая-дель-Кармен в 2026 году?",
   "Около $2.6M&ndash;$3.2M MXN ($145,000&ndash;$178,000 USD) под ключ за 150 м&sup2; со стандартной отделкой &mdash; примерно $17,000&ndash;$21,000 MXN/м&sup2;, без земли, бассейна и мебели."),
  ("Что не входит в цену за квадратный метр?",
   "Земля, бассейн ($450,000&ndash;$1,200,000), обустройство кровли-террасы, водоподготовка, кондиционирование, солнечные панели, озеленение и мебель. Именно отсюда берутся почти все бюджетные сюрпризы, поэтому считайте их отдельными статьями с самого начала."),
  ("Какой этап самый дорогой?",
   "Фундамент и каркас &mdash; около 30% бюджета, затем отделка с 25%. Каркас при этом единственный этап, где экономия в зоне сильных ветров опасна, а отделка способна сдвинуть итог на 20% без изменения чертежей."),
  ("Как Плая-дель-Кармен соотносится с другими зонами?",
   "Это эталон. Пуэрто-Морелос примерно вровень, Пуэрто-Авентурас +8%, Акумаль +12%, Альдеа-Зама +20%, Плаякар +25%, Корасоль +30%, Майякоба +42% &mdash; разница идёт от ограничений доступа, архитектурных комитетов, морской спецификации и экологических требований, а не от качества работ."),
  ("Как не дать смете расползтись?",
   "Фиксированная цена с постатейной сметой вместо ставки за м&sup2;, оплата по проверенному факту с удержанием 5&ndash;10%, письменные и оценённые изменения до начала работ и явный список исключений, согласованный при подписании."),
 ],
}

Z[("ru","tulum")] = {
 "title": "Сколько Стоит Построить Дом в Тулуме 2026: Решает Участок",
 "desc": "Стоимость стройки в Тулуме 2026 и почему итог определяет участок — коммуникации, растительность, экологическое досье — а не сам дом.",
 "lead": "Дом 150 м&sup2; в <strong>Тулуме</strong> стоит примерно <strong>$2.85M&ndash;$3.60M MXN ($158k&ndash;$200k USD)</strong> под ключ в 2026 году. Но разброс итоговых сумм здесь больше, чем где-либо на побережье &mdash; и причина почти никогда не в доме, а в участке.",
 "sections": [
  ("Стоимость по площади и по локации",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Площадь</th><th>Под ключ (MXN)</th><th>Под ключ (USD)</th></tr></thead><tbody>
<tr><td>100 м&sup2;</td><td>$1.90M&ndash;$2.40M</td><td>$106k&ndash;$133k</td></tr>
<tr><td>150 м&sup2;</td><td>$2.85M&ndash;$3.60M</td><td>$158k&ndash;$200k</td></tr>
<tr><td>200 м&sup2;</td><td>$3.80M&ndash;$4.80M</td><td>$211k&ndash;$267k</td></tr>
<tr><td>300 м&sup2;</td><td>$5.70M&ndash;$7.20M</td><td>$317k&ndash;$400k</td></tr>
</tbody></table></div>
<p class="text-muted small">Ориентир: $19,000&ndash;$24,000 MXN/м&sup2; от стандартной до премиум-отделки. USD/MXN &asymp; 18. Без земли, бассейна и мебели.</p>
<p>Внутри Тулума локации сильно расходятся: регионы и Ла-Велета по нижней границе, Альдеа-Зама и Tulum Country Club выше, пляжная дорога с морской спецификацией и тяжёлым экологическим досье &mdash; значительно выше.</p>"""),
  ("Почему итог определяет участок",
   """<p>Четыре статьи масштабируются с участком, а не с площадью дома:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Статья</th><th>MXN</th></tr></thead><tbody>
<tr><td>Экологическое досье в зависимости от растительности</td><td>$80,000&ndash;$300,000</td></tr>
<tr><td>Очистные или биодигестер с полем фильтрации</td><td>$90,000&ndash;$250,000</td></tr>
<tr><td>Подключение CFE на улице с сетями</td><td>$10,000&ndash;$40,000</td></tr>
<tr><td>Расширение сети CFE до участка без коммуникаций</td><td>$150,000&ndash;свыше $900,000</td></tr>
<tr><td>Автономия вместо подключения (солнце, накопитель, скважина)</td><td>$250,000&ndash;$800,000</td></tr>
<tr><td>Подъезд и освоение в джунглях</td><td>$40,000&ndash;$300,000</td></tr>
</tbody></table></div>
<p>Поэтому главное решение в Тулуме &mdash; выбор участка, а не список отделки. Запросите цену расширения сети CFE <em>до</em> покупки: именно эта цифра определяет, что дешевле и быстрее &mdash; подключение или спроектированная автономия.</p>"""),
  ("Календарь разрешений, электричество и исполнение",
   """<p>Экологическая экспертиза Тулума самая требовательная на побережье. Реалистично от покупки до начала работ проходит <strong>6&ndash;14 месяцев</strong>: сертификат использования земли и выравнивание 2&ndash;8 недель, экологическое досье 4&ndash;9 месяцев на участке с растительностью, технический проект параллельно, рассмотрение лицензии 4&ndash;12 недель. Запускайте досье и геологию на стадии эскиза &mdash; финальные чертежи для них не нужны, а на проект они влияют.</p>
<ul>
<li><strong>Ограничения высоты строгие</strong> и соблюдаются &mdash; проверьте лимит по участку до проектирования кровли-террасы.</li>
<li><strong>Сеть менее надёжна,</strong> чем севернее: защита от перенапряжений как стандарт, для аренды &mdash; аккумуляторы на интернет, контроллер бассейна и базовое освещение, $140,000&ndash;$330,000 MXN.</li>
<li><strong>Сеноты и карст</strong> требуют геологии со скважинами и отступов для инфильтрации. То, что уходит в грунт, доходит до водоносного горизонта и рифа.</li>
<li><strong>Термиты и влага:</strong> никакого контакта дерева с грунтом, обработка основания до плиты, вентилируемая столярка, осушение в закрытых помещениях.</li>
</ul>
<p>Сама стройка занимает около <strong>7&ndash;11 месяцев</strong> для 150&ndash;200 м&sup2;. Фиксированная цена с постатейной сметой и оплата по проверенному факту &mdash; и календарь разрешений в плане с самого начала, а не как открытие.</p>"""),
 ],
 "faq": [
  ("Сколько стоит построить дом в Тулуме в 2026 году?",
   "Около $2.85M&ndash;$3.60M MXN ($158k&ndash;$200k USD) под ключ за 150 м&sup2; &mdash; примерно $19,000&ndash;$24,000 MXN/м&sup2;. Внутри Тулума регионы и Ла-Велета по нижней границе, Альдеа-Зама выше, пляжная дорога значительно выше."),
  ("Почему итоговые суммы в Тулуме так различаются?",
   "Потому что четыре крупные статьи зависят от участка, а не от дома: экологическое досье $80,000&ndash;$300,000, очистные $90,000&ndash;$250,000, электроснабжение от $10,000 до более $900,000 и подъезд в джунглях $40,000&ndash;$300,000."),
  ("Подключение к сети или автономия?",
   "Запросите цену расширения сети CFE до покупки. Если она в верхнем шестизначном диапазоне, спроектированная автономия с солнечными панелями, накопителем, скважиной с водоподготовкой и сбором дождевой воды за $250,000&ndash;$800,000 часто дешевле и быстрее."),
  ("Сколько ждать до начала работ?",
   "Реалистично 6&ndash;14 месяцев с момента покупки, в основном из-за экологического досье, которое на участке с растительностью занимает 4&ndash;9 месяцев. Досье и геологию стоит запускать, пока архитектура ещё в эскизе."),
  ("Какие технические моменты в Тулуме важнее всего?",
   "Очистка перед инфильтрацией с корректными отступами от сенотов, геология из-за карста, защита от перенапряжений и при необходимости аккумуляторы из-за качества сети, а также последовательная защита от термитов и влаги без контакта дерева с грунтом."),
 ],
}

Z[("fr","cancun")] = {
 "title": "Coût de Construction d'une Maison à Cancún 2026",
 "desc": "Construire à Cancún coûte moins cher que partout ailleurs sur le corridor. Fourchettes au m² 2026, d'où vient la remise et où elle devient un risque.",
 "lead": "Une maison familiale de 150 m&sup2; &agrave; <strong>Canc&uacute;n</strong> co&ucirc;te environ <strong>$2.48M&ndash;$3M MXN ($138k&ndash;$167k USD)</strong> cl&eacute; en main en 2026 &mdash; le chiffre le plus bas du corridor, environ 4% sous Playa del Carmen &agrave; prestation &eacute;gale. Voici d'o&ugrave; vient cette remise et o&ugrave; elle cesse d'&ecirc;tre une bonne affaire.",
 "sections": [
  ("Pourquoi Cancún se situe sous le reste du corridor",
   """<p>Canc&uacute;n est le seul endroit du corridor o&ugrave; l'&eacute;chelle du march&eacute; profite &agrave; celui qui construit une maison : le plus grand vivier de main-d'&oelig;uvre de la r&eacute;gion, la plus forte densit&eacute; de fournisseurs et d'ateliers, et assez d'entreprises en concurrence pour que les prix soient r&eacute;ellement &eacute;prouv&eacute;s. Tout ce qui se trouve au sud de Puerto Morelos fait venir une partie du travail d'ici.</p>
<ul>
<li><strong>Mat&eacute;riaux &agrave; la source.</strong> Blocs, ciment, acier, granulats, aluminium, carrelage et sanitaires s'ach&egrave;tent sur place sans transport le long du corridor &mdash; sur une maison de 150 m&sup2;, cela repr&eacute;sente d&eacute;j&agrave; plusieurs points.</li>
<li><strong>Corps de m&eacute;tier sans d&eacute;placement.</strong> Les travaux sp&eacute;cialis&eacute;s qu'il faut planifier et acheminer vers Tulum ou Akumal se r&egrave;glent ici par un appel local.</li>
<li><strong>Terrains &agrave; l'int&eacute;rieur des terres.</strong> L'essentiel de la construction r&eacute;sidentielle se fait dans des lotissements ferm&eacute;s int&eacute;rieurs : pas de zone f&eacute;d&eacute;rale maritime, pas de concession ZOFEMAT, pas de calendrier de nidification des tortues et un dossier environnemental plus l&eacute;ger qu'un terrain c&ocirc;tier &eacute;quivalent.</li>
</ul>
<p>Les autorisations passent par la municipalit&eacute; de <strong>Benito Ju&aacute;rez</strong> &mdash; usage du sol, permis de construire, alignement et Director Responsable de Obra &mdash; et sur un terrain viabilis&eacute;, c'est l'un des parcours les plus pr&eacute;visibles de l'&Eacute;tat.</p>"""),
  ("Coût clé en main par taille de maison",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Surface</th><th>Cl&eacute; en main (MXN)</th><th>Cl&eacute; en main (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.65M&ndash;$2M</td><td>$92k&ndash;$111k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.48M&ndash;$3M</td><td>$138k&ndash;$167k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.30M&ndash;$4M</td><td>$183k&ndash;$222k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.13M&ndash;$5M</td><td>$229k&ndash;$278k</td></tr>
</tbody></table></div>
<p class="text-muted small">R&eacute;f&eacute;rence : $16,500&ndash;$20,000 MXN/m&sup2; finition standard. USD/MXN &asymp; 18. Hors terrain, piscine et mobilier.</p>
<p>Ces fourchettes valent pour le Canc&uacute;n r&eacute;sidentiel int&eacute;rieur. Un terrain dans la Zona Hotelera, &agrave; Isla Dorada ou en front de mer ou de lagune est un autre b&acirc;timent : sp&eacute;cification marine int&eacute;grale, questions de zone f&eacute;d&eacute;rale et niveau de finition exig&eacute; par le lieu. On y compte plut&ocirc;t $26,000&ndash;$40,000 MXN/m&sup2;.</p>"""),
  ("Où l'économie devient un risque",
   """<p>Un march&eacute; vaste et concurrentiel produit des prix bas et une &eacute;norme dispersion de qualit&eacute;. &Agrave; Canc&uacute;n, le probl&egrave;me n'est pas le chantier cher, c'est le chantier bon march&eacute;.</p>
<ul>
<li><strong>Les offres sous environ $14,000 MXN/m&sup2;</strong> rognent sur du structurel &mdash; g&eacute;n&eacute;ralement densit&eacute; d'armatures, qualit&eacute; du b&eacute;ton ou installation &eacute;lectrique. En zone de vents forts, l'acier n'est pas le bon poste d'&eacute;conomie.</li>
<li><strong>Sans &eacute;tude de sol.</strong> Le karst peut offrir une excellente portance et une cavit&eacute; deux m&egrave;tres plus loin. Des sondages sur l'emprise r&eacute;elle co&ucirc;tent $25,000&ndash;$60,000 : la r&eacute;duction de risque la moins ch&egrave;re du projet.</li>
<li><strong>R&egrave;gles du lotissement.</strong> Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua et Palmaris ont des comit&eacute;s d'architecture avec leurs propres limites de hauteur, de retraits, de mat&eacute;riaux et de couleurs, plus enregistrement des ouvriers, horaires restreints et caution. D&eacute;posez au stade avant-projet.</li>
<li><strong>Trafic et cr&eacute;neaux de livraison.</strong> Canc&uacute;n est le seul endroit du corridor o&ugrave; la circulation urbaine devient un sujet de planning.</li>
<li><strong>Le sel atteint aussi l'int&eacute;rieur.</strong> M&ecirc;me &agrave; plusieurs kilom&egrave;tres de la mer, fixations, garde-corps et batteries de climatisation durent nettement plus longtemps en inox 316 et rev&ecirc;tements marins.</li>
</ul>
<p>Une maison de 150 m&sup2; demande environ <strong>7&ndash;10 mois</strong> du permis &agrave; la remise, et la profondeur du march&eacute; local &eacute;vite une partie des attentes de mat&eacute;riaux qui allongent les chantiers plus au sud. Exigez un contrat &agrave; prix ferme, avec budget d&eacute;taill&eacute; et paiements &agrave; l'avancement v&eacute;rifi&eacute;.</p>"""),
 ],
 "faq": [
  ("Combien coûte la construction d'une maison à Cancún en 2026 ?",
   "Environ $2.48M&ndash;$3M MXN ($138k&ndash;$167k USD) cl&eacute; en main pour 150 m&sup2; en finition standard sur un terrain r&eacute;sidentiel int&eacute;rieur, hors terrain, piscine et mobilier &mdash; soit $16,500&ndash;$20,000 MXN/m&sup2;."),
  ("Pourquoi Cancún est-il moins cher que Playa del Carmen ou Tulum ?",
   "Par l'&eacute;chelle : le plus grand vivier de main-d'&oelig;uvre du corridor, la plus forte densit&eacute; de fournisseurs et une vraie concurrence entre entreprises. De plus on construit &agrave; l'int&eacute;rieur des terres, ce qui &eacute;vite la zone f&eacute;d&eacute;rale maritime, les r&egrave;gles de nidification et le dossier environnemental plus lourd d'un terrain c&ocirc;tier."),
  ("Ce prix s'applique-t-il dans la Zona Hotelera ?",
   "Non. Zona Hotelera, Isla Dorada ou tout front de mer ou de lagune impliquent une sp&eacute;cification marine int&eacute;grale, des questions de zone f&eacute;d&eacute;rale et un niveau de finition sup&eacute;rieur &mdash; comptez $26,000&ndash;$40,000 MXN/m&sup2;."),
  ("Jusqu'où un devis peut-il descendre à Cancún ?",
   "Consid&eacute;rez comme un signal d'alerte tout ce qui est sous environ $14,000 MXN/m&sup2;. &Agrave; ce prix on r&eacute;duit du structurel &mdash; armatures, qualit&eacute; du b&eacute;ton ou &eacute;lectricit&eacute; &mdash; et en zone de vents forts ce sont les mauvaises &eacute;conomies."),
  ("Les lotissements fermés augmentent-ils le coût ?",
   "Oui. Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua et Palmaris ont leurs propres comit&eacute;s d'architecture avec limites de hauteur, retraits, mat&eacute;riaux et couleurs, plus enregistrement des ouvriers, horaires restreints et caution. Int&eacute;grez le cycle d'examen au planning, pas seulement les frais."),
 ],
}

Z[("fr","puerto-aventuras")] = {
 "title": "Coût de Construction d'une Maison à Puerto Aventuras 2026",
 "desc": "Coûts clé en main à Puerto Aventuras plus les postes de la marina que les acheteurs oublient : charges HOA, ponton, mur de canal et comité d'architecture.",
 "lead": "Une maison de 150 m&sup2; &agrave; <strong>Puerto Aventuras</strong> co&ucirc;te environ <strong>$2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD)</strong> cl&eacute; en main en 2026, soit environ 8% au-dessus de Playa del Carmen. Le chantier est la partie pr&eacute;visible ; ce sont les postes ci-dessous qui font d&eacute;railler les budgets dans une communaut&eacute; de marina.",
 "sections": [
  ("Coût clé en main par taille de maison",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Surface</th><th>Cl&eacute; en main (MXN)</th><th>Cl&eacute; en main (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.85M&ndash;$2.25M</td><td>$103k&ndash;$125k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.77M&ndash;$3.38M</td><td>$154k&ndash;$188k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.70M&ndash;$4.50M</td><td>$206k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.63M&ndash;$5.63M</td><td>$257k&ndash;$313k</td></tr>
</tbody></table></div>
<p class="text-muted small">R&eacute;f&eacute;rence : $18,500&ndash;$22,500 MXN/m&sup2; finition standard. USD/MXN &asymp; 18. Hors terrain, piscine et mobilier.</p>
<p>Ces 8% au-dessus de Playa del Carmen recouvrent quatre choses concr&egrave;tes, et non un suppl&eacute;ment d'adresse : acc&egrave;s contr&ocirc;l&eacute; avec enregistrement des ouvriers, horaires restreints qui allongent le planning, manutention plus longue &agrave; l'int&eacute;rieur de la communaut&eacute; et sp&eacute;cification marine exig&eacute;e par les positions sur canal ou proches du littoral.</p>"""),
  ("Les postes que l'on oublie",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Poste</th><th>Ce qu'il faut vérifier</th></tr></thead><tbody>
<tr><td><strong>Charges HOA</strong></td><td>Le montant actuel pour ce terrain pr&eacute;cis, le budget qui le justifie et son &eacute;volution sur cinq ans. Les lots sur canal et pr&egrave;s de la marina paient souvent davantage.</td></tr>
<tr><td><strong>Ponton ou place d'amarrage</strong></td><td>En propri&eacute;t&eacute;, en location ou attribu&eacute; &mdash; trois choses diff&eacute;rentes juridiquement et &agrave; la revente &mdash; et le co&ucirc;t annuel. Les travaux de ponton s'autorisent s&eacute;par&eacute;ment de la maison.</td></tr>
<tr><td><strong>Mur de canal</strong></td><td>Son &eacute;tat, &eacute;valu&eacute; par quelqu'un qui ne vous vend pas le bien. Sa reprise est un projet &agrave; part enti&egrave;re.</td></tr>
<tr><td><strong>Comit&eacute; d'architecture</strong></td><td>D&eacute;p&ocirc;t, cycle d'examen et caution : $60,000&ndash;$250,000 MXN et au moins un tour d'examen au planning.</td></tr>
<tr><td><strong>Sp&eacute;cification marine</strong></td><td>Fixations 316, aluminium anodis&eacute; ou &agrave; rev&ecirc;tement marin, enrobage de b&eacute;ton augment&eacute;. Plus cher au chantier, bien moins cher sur une d&eacute;cennie.</td></tr>
</tbody></table></div>
<p>Les autorisations passent par la municipalit&eacute; de <strong>Solidaridad</strong> &mdash; le m&ecirc;me parcours que Playa del Carmen &mdash; l'examen architectural de la communaut&eacute; venant en pratique avant.</p>"""),
  ("Front de canal : ce qui change techniquement",
   """<ul>
<li><strong>Nappe phr&eacute;atique haute.</strong> Fouilles, citerne et bassin de piscine demandent rabattement et v&eacute;rification &agrave; la pouss&eacute;e &mdash; une piscine vid&eacute;e au mauvais moment peut remonter.</li>
<li><strong>A&eacute;rosol salin permanent</strong> venu de l'eau, et non une exposition saisonni&egrave;re. L'inox 316 cesse ici d'&ecirc;tre une pr&eacute;f&eacute;rence.</li>
<li><strong>Exposition aux temp&ecirc;tes.</strong> Les terrains au bord de l'eau prennent la charge de vent compl&egrave;te et, lors d'un &eacute;v&eacute;nement s&eacute;rieux, la submersion. Le vitrage feuillet&eacute; ou class&eacute; impact c&ocirc;t&eacute; eau est la sp&eacute;cification sur laquelle nous ne c&eacute;dons pas.</li>
<li><strong>Ouvrages de berge</strong> en limite d'eau : conception et autorisation propres.</li>
</ul>
<p>Une maison de 150 m&sup2; demande environ <strong>7&ndash;10 mois</strong> &agrave; partir du permis, et les horaires restreints poussent le planning vers le haut de la fourchette. Contrat &agrave; prix ferme, budget d&eacute;taill&eacute;, paiements &agrave; l'avancement v&eacute;rifi&eacute;.</p>"""),
 ],
 "faq": [
  ("Combien coûte une maison à Puerto Aventuras ?",
   "Environ $2.77M&ndash;$3.38M MXN ($154k&ndash;$188k USD) cl&eacute; en main pour 150 m&sup2; en finition standard, hors terrain, piscine et mobilier &mdash; soit $18,500&ndash;$22,500 MXN/m&sup2;, environ 8% au-dessus de Playa del Carmen."),
  ("Pourquoi est-ce plus cher qu'à Playa del Carmen ?",
   "Quatre raisons concr&egrave;tes : acc&egrave;s contr&ocirc;l&eacute; avec enregistrement des ouvriers, horaires restreints qui allongent le planning, manutention plus longue dans la communaut&eacute; et sp&eacute;cification marine pour les lots sur canal ou proches du littoral."),
  ("Quels coûts sortent du budget de construction ?",
   "Les charges HOA du terrain, l'&eacute;ventuelle redevance de ponton, la reprise du mur de canal s'il est fatigu&eacute;, et le d&eacute;p&ocirc;t au comit&eacute; avec sa caution, environ $60,000&ndash;$250,000 MXN. Les travaux de ponton s'autorisent s&eacute;par&eacute;ment."),
  ("Faut-il l'accord de la communauté en plus de la municipalité ?",
   "Oui, et en pratique la communaut&eacute; passe d'abord. Le permis et le DRO rel&egrave;vent de Solidaridad, tandis que le comit&eacute; examine hauteur, retraits, mat&eacute;riaux, couleurs et cl&ocirc;tures. D&eacute;posez au stade avant-projet : un tour d'examen impr&eacute;vu est le retard le plus courant ici."),
  ("Qu'est-ce qui change sur un terrain en front de canal ?",
   "Rabattement de nappe et v&eacute;rification &agrave; la pouss&eacute;e pour les fouilles et la piscine, sp&eacute;cification marine int&eacute;grale &agrave; cause de l'a&eacute;rosol salin permanent, vitrage class&eacute; impact c&ocirc;t&eacute; eau, et autorisation distincte pour tout ouvrage en limite d'eau."),
 ],
}

Z[("fr","akumal")] = {
 "title": "Coût de Construction d'une Maison à Akumal 2026",
 "desc": "Coûts de construction à Akumal 2026 et pourquoi c'est le dossier environnemental — pas les murs — qui décide du total. Tortues, station d'épuration, transport.",
 "lead": "Une maison de 150 m&sup2; &agrave; <strong>Akumal</strong> co&ucirc;te environ <strong>$2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD)</strong> cl&eacute; en main en 2026. Mais sur un terrain d'Akumal, le chantier est la moiti&eacute; pr&eacute;visible du budget : ce sont le dossier environnemental, la station d'&eacute;puration et le calendrier des autorisations qui s&eacute;parent deux projets apparemment identiques.",
 "sections": [
  ("Coût clé en main par taille de maison",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Surface</th><th>Cl&eacute; en main (MXN)</th><th>Cl&eacute; en main (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.90M&ndash;$2.35M</td><td>$106k&ndash;$131k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.85M&ndash;$3.52M</td><td>$158k&ndash;$196k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.80M&ndash;$4.70M</td><td>$211k&ndash;$261k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.75M&ndash;$5.88M</td><td>$264k&ndash;$326k</td></tr>
</tbody></table></div>
<p class="text-muted small">R&eacute;f&eacute;rence : $19,000&ndash;$23,500 MXN/m&sup2; finition standard. USD/MXN &asymp; 18. Hors terrain, piscine et mobilier.</p>
<p>Soit environ 12% au-dessus de Playa del Carmen : transport de chaque mat&eacute;riau le long du corridor, sp&eacute;cification marine pour l'exposition saline et une base locale de corps de m&eacute;tier plus r&eacute;duite qui impose des d&eacute;placements.</p>"""),
  ("Les postes qui n'existent qu'à Akumal",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Poste</th><th>MXN</th><th>Pourquoi</th></tr></thead><tbody>
<tr><td>&Eacute;tudes et autorisation environnementale</td><td>$80,000&ndash;$350,000</td><td>L'ampleur d&eacute;pend de la v&eacute;g&eacute;tation et de la proximit&eacute; du rivage, pas de la taille de la maison</td></tr>
<tr><td>Station d'&eacute;puration + puits d'absorption</td><td>$120,000&ndash;$380,000</td><td>Pas de r&eacute;seau ; traiter avant d'infiltrer est le c&oelig;ur du dossier</td></tr>
<tr><td>&Eacute;clairage compatible nidification</td><td>$30,000&ndash;$120,000</td><td>Bas, capot&eacute;, ambre ou rouge sur les fa&ccedil;ades c&ocirc;t&eacute; plage</td></tr>
<tr><td>Lev&eacute; ZOFEMAT et examen de concession</td><td>$20,000&ndash;$80,000</td><td>Uniquement pour les lots touchant la zone f&eacute;d&eacute;rale maritime</td></tr>
<tr><td>&Eacute;tude de sol sur l'emprise</td><td>$25,000&ndash;$60,000</td><td>Karst : une cavit&eacute; peut se trouver &agrave; deux m&egrave;tres d'un bon appui</td></tr>
</tbody></table></div>
<p>Quatre de ces cinq postes varient avec le <em>terrain</em>, pas avec la maison. C'est pourquoi une maison compacte &agrave; Akumal co&ucirc;te plus cher au m&egrave;tre qu'une grande, et pourquoi la meilleure &eacute;conomie disponible ici consiste &agrave; choisir un terrain disposant d&eacute;j&agrave; d'une autorisation environnementale et des r&eacute;seaux en limite.</p>"""),
  ("Le calendrier des autorisations et le coût de l'attente",
   """<p>Akumal rel&egrave;ve de la municipalit&eacute; de <strong>Tulum</strong>, et non de Solidaridad &mdash; ce qui surprend, Playa del Carmen &eacute;tant plus proche. L'examen environnemental de Tulum est le plus exigeant du corridor, et la cons&eacute;quence pratique est le calendrier :</p>
<ul>
<li><strong>Dossier environnemental :</strong> 4&ndash;9 mois sur un terrain v&eacute;g&eacute;talis&eacute; ou proche du rivage.</li>
<li><strong>Instruction du permis avec dossier complet :</strong> 4&ndash;12 semaines.</li>
<li><strong>Total r&eacute;aliste de l'achat au d&eacute;marrage :</strong> 6&ndash;14 mois.</li>
</ul>
<p>Ces mois sont un co&ucirc;t r&eacute;el : terrain port&eacute; et capital immobilis&eacute; sans rendement. C'est aussi pourquoi un terrain avec autorisation en cours de validit&eacute; se vend avec une prime &mdash; g&eacute;n&eacute;ralement m&eacute;rit&eacute;e.</p>
<p>Un point de planning propre &agrave; ce littoral : la nidification des tortues court environ de <strong>mai &agrave; octobre</strong>, avec restrictions sur les travaux lourds, l'&eacute;clairage puissant et l'activit&eacute; sur le sable. Placez les phases ext&eacute;rieures bruyantes hors de cette fen&ecirc;tre et les finitions int&eacute;rieures dedans.</p>
<p>Le chantier lui-m&ecirc;me dure environ <strong>7&ndash;10 mois</strong> pour 150 m&sup2;. Contrat &agrave; prix ferme avec budget d&eacute;taill&eacute; &mdash; et les conditions environnementales (reprise des plantations, carnet de la station, conformit&eacute; de l'&eacute;clairage) doivent &ecirc;tre confi&eacute;es &agrave; quelqu'un apr&egrave;s la remise, car elles courent sur toute la vie du bien.</p>"""),
 ],
 "faq": [
  ("Combien coûte une maison à Akumal en 2026 ?",
   "Environ $2.85M&ndash;$3.52M MXN ($158k&ndash;$196k USD) cl&eacute; en main pour 150 m&sup2; en finition standard &mdash; soit $19,000&ndash;$23,500 MXN/m&sup2;, environ 12% au-dessus de Playa del Carmen. Terrain, piscine, mobilier et postes environnementaux en sus."),
  ("Quels surcoûts porte un terrain à Akumal ?",
   "&Eacute;tudes et autorisation environnementale $80,000&ndash;$350,000, station d'&eacute;puration avec puits d'absorption $120,000&ndash;$380,000, &eacute;clairage compatible nidification $30,000&ndash;$120,000, lev&eacute; ZOFEMAT $20,000&ndash;$80,000 et &eacute;tude de sol $25,000&ndash;$60,000. La plupart d&eacute;pendent du terrain, pas de la maison."),
  ("Quelle municipalité délivre les permis à Akumal ?",
   "Tulum, et non Solidaridad, bien que Playa del Carmen soit plus proche. Son examen environnemental est le plus exigeant du corridor : pr&eacute;voyez 6&ndash;14 mois de l'achat au d&eacute;marrage du chantier."),
  ("Les règles de nidification affectent-elles le planning ?",
   "Oui. La saison court environ de mai &agrave; octobre et restreint travaux lourds, &eacute;clairage puissant et activit&eacute; sur le sable pr&egrave;s de la plage. Placez les phases ext&eacute;rieures hors saison et l'int&eacute;rieur dedans. Les r&egrave;gles d'&eacute;clairage valent aussi pour la maison termin&eacute;e."),
  ("Une maison plus petite coûte-t-elle moins cher au m² à Akumal ?",
   "Non, elle co&ucirc;te plus cher au m&egrave;tre. Dossier environnemental, &eacute;tude de sol, station d'&eacute;puration et raccordement co&ucirc;tent presque autant pour 80 m&sup2; que pour 200 m&sup2;, donc ces postes fixes p&egrave;sent bien davantage sur une maison compacte."),
 ],
}

Z[("fr","puerto-morelos")] = {
 "title": "Coût de Construction d'une Maison à Puerto Morelos 2026",
 "desc": "Puerto Morelos construit aux prix de Playa del Carmen sur un foncier moins cher. Fourchettes 2026, rejets face au parc du récif et Ruta de los Cenotes.",
 "lead": "Une maison de 150 m&sup2; &agrave; <strong>Puerto Morelos</strong> co&ucirc;te environ <strong>$2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD)</strong> cl&eacute; en main en 2026 &mdash; pratiquement au niveau de Playa del Carmen c&ocirc;t&eacute; chantier, sur un foncier g&eacute;n&eacute;ralement moins cher. C'est cette combinaison qui en fait le bon rapport qualit&eacute;-prix discret du corridor.",
 "sections": [
  ("Coût clé en main et les trois sous-marchés",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Surface</th><th>Cl&eacute; en main (MXN)</th><th>Cl&eacute; en main (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.70M&ndash;$2.10M</td><td>$94k&ndash;$117k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.55M&ndash;$3.15M</td><td>$142k&ndash;$175k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.40M&ndash;$4.20M</td><td>$189k&ndash;$233k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.25M&ndash;$5.25M</td><td>$236k&ndash;$292k</td></tr>
</tbody></table></div>
<p class="text-muted small">R&eacute;f&eacute;rence : $17,000&ndash;$21,000 MXN/m&sup2; finition standard. USD/MXN &asymp; 18. Hors terrain, piscine et mobilier.</p>
<ul>
<li><strong>Bord de mer :</strong> $26,000&ndash;$38,000+ MXN/m&sup2; avec sp&eacute;cification marine et dossier environnemental plus lourd.</li>
<li><strong>Ruta de los Cenotes :</strong> $14,000&ndash;$19,000 sur terrain viabilis&eacute;, $17,000&ndash;$24,000 en autonomie &mdash; foncier moins cher, davantage d'infrastructure.</li>
</ul>"""),
  ("Municipalité à part entière depuis 2016",
   """<p>Puerto Morelos s'est s&eacute;par&eacute;e de Benito Ju&aacute;rez en 2016 et d&eacute;livre d&eacute;sormais ses propres usages du sol, permis, alignements et r&eacute;ceptions. Trois cons&eacute;quences pratiques :</p>
<ul>
<li><strong>On d&eacute;pose ici, pas &agrave; Canc&uacute;n.</strong> Les conseils fond&eacute;s sur la pratique de Benito Ju&aacute;rez sont p&eacute;rim&eacute;s, tout comme l'exp&eacute;rience d'un voisin ant&eacute;rieure &agrave; 2016.</li>
<li><strong>V&eacute;rifiez les chiffres du terrain aujourd'hui.</strong> Les documents d'urbanisme de la commune sont r&eacute;cents et ont &eacute;t&eacute; actualis&eacute;s : faites confirmer densit&eacute;, hauteur et usage autoris&eacute; pour votre parcelle.</li>
<li><strong>Une petite administration est une administration directe.</strong> Les agents qui instruisent sont accessibles, ce qui rend un dossier complet particuli&egrave;rement efficace et un dossier incomplet particuli&egrave;rement lent.</li>
</ul>
<p>L'examen environnemental de l'&Eacute;tat (SEMA), la comp&eacute;tence f&eacute;d&eacute;rale le cas &eacute;ch&eacute;ant, CONAGUA pour l'eau et ZOFEMAT c&ocirc;t&eacute; plage s'appliquent comme ailleurs.</p>"""),
  ("Ce que le récif et les zones humides ajoutent à la spécification",
   """<ul>
<li><strong>La qualit&eacute; du rejet est le c&oelig;ur du dossier.</strong> Traitement avant infiltration, correctement dimensionn&eacute;, avec les eaux de lavage de piscine &eacute;vacu&eacute;es s&eacute;par&eacute;ment &mdash; $90,000&ndash;$350,000 MXN selon l'occupation. Ce qui s'infiltre ici atteint l'aquif&egrave;re puis le r&eacute;cif.</li>
<li><strong>La mangrove ne se n&eacute;gocie pas.</strong> Sur un terrain riverain, la limite de la v&eacute;g&eacute;tation prot&eacute;g&eacute;e doit &ecirc;tre &eacute;tablie avant tout plan &mdash; certains lots offerts &agrave; la vente ont une surface constructible bien inf&eacute;rieure &agrave; leur surface cadastrale.</li>
<li><strong>Les reculs autour des cenotes</strong> s'appliquent &agrave; l'int&eacute;rieur des terres, avec des restrictions sur ce qui peut s'infiltrer &agrave; proximit&eacute;.</li>
<li><strong>Le niveau du plancher fini</strong> sur terrain bas pr&egrave;s des zones humides ou du rivage se fixe en tenant compte des inondations et de la submersion. D&eacute;cision de conception, non rattrapable ensuite.</li>
<li><strong>Sur la Ruta de los Cenotes,</strong> budg&eacute;tez la voie d'acc&egrave;s ($40,000&ndash;$300,000) et soit une extension CFE &mdash; &agrave; chiffrer avant l'achat, de $150,000 &agrave; plus de $900,000 &mdash; soit une autonomie con&ccedil;ue avec solaire, stockage, puits trait&eacute; et r&eacute;cup&eacute;ration d'eau de pluie.</li>
</ul>
<p>Le chantier d'une maison de 150 m&sup2; dure environ <strong>7&ndash;10 mois</strong>.</p>"""),
 ],
 "faq": [
  ("Combien coûte une maison à Puerto Morelos ?",
   "Environ $2.55M&ndash;$3.15M MXN ($142k&ndash;$175k USD) cl&eacute; en main pour 150 m&sup2; au village ou &agrave; l'int&eacute;rieur &mdash; soit $17,000&ndash;$21,000 MXN/m&sup2;, pratiquement au niveau de Playa del Carmen. Bord de mer $26,000&ndash;$38,000+, Ruta de los Cenotes $14,000&ndash;$24,000 selon les r&eacute;seaux."),
  ("Quelle municipalité délivre les permis ?",
   "Puerto Morelos elle-m&ecirc;me : s&eacute;paration de Benito Ju&aacute;rez (Canc&uacute;n) en 2016. Toute information fond&eacute;e sur la pratique de Canc&uacute;n est p&eacute;rim&eacute;e, et comme les documents d'urbanisme sont r&eacute;cents, densit&eacute;, hauteur et usage doivent &ecirc;tre v&eacute;rifi&eacute;s &agrave; jour."),
  ("Peut-on construire près de la mangrove ?",
   "Pas dans la v&eacute;g&eacute;tation prot&eacute;g&eacute;e, et sa limite doit &ecirc;tre &eacute;tablie avant tout plan. Certains lots &agrave; vendre ont une surface constructible nettement inf&eacute;rieure &agrave; la surface cadastrale : &agrave; v&eacute;rifier avant l'achat."),
  ("Qu'implique le parc national du récif pour mon chantier ?",
   "Que la qualit&eacute; du rejet devient la question technique centrale du dossier. Le traitement avant infiltration dimensionn&eacute; &agrave; l'occupation, avec les eaux de lavage de piscine s&eacute;par&eacute;es, co&ucirc;te $90,000&ndash;$350,000 MXN et fait l'objet d'un examen attentif."),
  ("Construire sur la Ruta de los Cenotes est-il moins cher ?",
   "Le foncier oui, et le chantier tourne autour de $14,000&ndash;$19,000 MXN/m&sup2; sur terrain viabilis&eacute;. Mais beaucoup de parcelles n'ont ni CFE ni eau : pr&eacute;voyez l'extension &mdash; &agrave; chiffrer avant l'achat, de $150,000 &agrave; plus de $900,000 &mdash; ou une autonomie con&ccedil;ue, plus $40,000&ndash;$300,000 d'acc&egrave;s."),
 ],
}

Z[("fr","playacar")] = {
 "title": "Coût de Construction d'une Maison à Playacar 2026",
 "desc": "Playacar est bâti : la plupart des projets sont rénovation ou démolition-reconstruction. Fourchettes 2026, coût de démolition, comité, Phase I et Phase II.",
 "lead": "Une maison de 150 m&sup2; &agrave; <strong>Playacar</strong> co&ucirc;te environ <strong>$3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD)</strong> cl&eacute; en main en 2026, soit environ 25% au-dessus du niveau de base de Playa del Carmen. Mais Playacar est pratiquement b&acirc;ti : la vraie question n'est pas le prix d'une maison neuve, c'est de savoir si l'on r&eacute;nove l'existante ou si on la d&eacute;molit.",
 "sections": [
  ("Rénover ou démolir : l'arithmétique",
   """<p>Presque tous les projets &agrave; Playacar sont une reconstruction apr&egrave;s d&eacute;molition, une grosse r&eacute;novation ou la construction sur l'un des rares terrains restants. Le choix entre les deux premiers se fait apr&egrave;s diagnostic, pas apr&egrave;s visite : les maisons de cet &acirc;ge sur ce littoral portent un d&eacute;faut pr&eacute;visible &mdash; corrosion des armatures par les chlorures en rives de dalle, balcons, poteaux et acrot&egrave;res.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Poste</th><th>MXN</th></tr></thead><tbody>
<tr><td>Diagnostic avec sondages destructifs cibl&eacute;s</td><td>$40,000&ndash;$150,000</td></tr>
<tr><td>D&eacute;molition et &eacute;vacuation, maison type</td><td>$180,000&ndash;$600,000</td></tr>
<tr><td>Programme de r&eacute;paration du b&eacute;ton si conservation</td><td>Chiffr&eacute; apr&egrave;s diagnostic &mdash; peut d&eacute;passer la d&eacute;molition</td></tr>
<tr><td>R&eacute;novation lourde, finition premium</td><td>$14,000&ndash;$26,000 MXN/m&sup2;</td></tr>
<tr><td>Neuf, premium</td><td>$24,000&ndash;$30,000 MXN/m&sup2;</td></tr>
<tr><td>Neuf, luxe</td><td>$30,000&ndash;$42,000 MXN/m&sup2;</td></tr>
</tbody></table></div>
<p>Le seuil honn&ecirc;te : d&egrave;s que la r&eacute;paration structurelle approche 25&ndash;30% du co&ucirc;t d'une reconstruction, vous payez le prix du neuf pour les hauteurs, l'orientation et le plan d'un b&acirc;timent ancien. &Agrave; Playacar il existe toutefois un vrai contre-argument : les terrains ne se remplacent pas, les arbres adultes sont prot&eacute;g&eacute;s et pr&eacute;cieux, et une maison solide des ann&eacute;es 1990 avec de belles hauteurs en Phase II peut m&eacute;riter d'&ecirc;tre conserv&eacute;e.</p>"""),
  ("Coût clé en main par taille de maison",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Surface</th><th>Cl&eacute; en main (MXN)</th><th>Cl&eacute; en main (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.10M&ndash;$2.60M</td><td>$117k&ndash;$144k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.15M&ndash;$3.90M</td><td>$175k&ndash;$217k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.20M&ndash;$5.20M</td><td>$233k&ndash;$289k</td></tr>
<tr><td>250 m&sup2;</td><td>$5.25M&ndash;$6.50M</td><td>$292k&ndash;$361k</td></tr>
</tbody></table></div>
<p class="text-muted small">R&eacute;f&eacute;rence : $21,000&ndash;$26,000 MXN/m&sup2; finition standard &agrave; premium. USD/MXN &asymp; 18. Hors terrain, piscine et mobilier.</p>
<p>Ces 25% correspondent &agrave; l'acc&egrave;s restreint par des rues &eacute;troites, aux ouvriers enregistr&eacute;s et aux horaires limit&eacute;s, &agrave; la proc&eacute;dure du comit&eacute;, &agrave; la protection des arbres, &agrave; la sp&eacute;cification marine et au niveau de finition attendu localement. Sur un terrain de Playacar en bord de mer, ajoutez la zone f&eacute;d&eacute;rale maritime et le vitrage class&eacute; impact c&ocirc;t&eacute; mer : $42,000&ndash;$60,000+ MXN/m&sup2;.</p>"""),
  ("Comité, arbres et Phase I contre Phase II",
   """<p><strong>L'examen architectural est r&eacute;el</strong> et c'est l&agrave; que les plannings de Playacar se d&eacute;calent. Attendez-vous &agrave; un examen de la hauteur, du volume et des retraits au-del&agrave; des minima municipaux, de la forme et des mat&eacute;riaux de toiture, du traitement de fa&ccedil;ade et de la palette, des murs et cl&ocirc;tures, et surtout de l'abattage d'arbres &mdash; chaque arbre doit &ecirc;tre justifi&eacute;. D&eacute;posez au stade avant-projet avec l'inventaire des arbres, et pr&eacute;voyez au moins un tour d'examen plus la caution.</p>
<p><strong>Phase I et Phase II sont deux lieux distincts.</strong> La Phase I est plus proche du centre et du ferry : plus dense, parcelles plus petites, v&eacute;ritable marche &agrave; pied jusqu'&agrave; la Quinta Avenida et acc&egrave;s chantier par rues &eacute;troites, ce qui rench&eacute;rit. La Phase II est plus vaste et calme autour du golf, avec de grandes parcelles, une v&eacute;g&eacute;tation mature et la place pour une villa importante &mdash; et la proximit&eacute; du parcours fait du vitrage et des verri&egrave;res un sujet concret.</p>
<p>Les autorisations passent par <strong>Solidaridad</strong> ; le chantier dure environ <strong>7&ndash;10 mois</strong> pour 150 m&sup2;, d&eacute;molition en sus le cas &eacute;ch&eacute;ant.</p>"""),
 ],
 "faq": [
  ("Combien coûte la construction à Playacar ?",
   "Environ $3.15M&ndash;$3.90M MXN ($175k&ndash;$217k USD) cl&eacute; en main pour 150 m&sup2; &mdash; soit $21,000&ndash;$26,000 MXN/m&sup2;, environ 25% au-dessus du niveau de base de Playa del Carmen. Finition luxe $30,000&ndash;$42,000, terrains en bord de mer $42,000&ndash;$60,000+."),
  ("Faut-il rénover la maison existante ou la démolir ?",
   "D'abord un diagnostic avec sondages cibl&eacute;s, $40,000&ndash;$150,000 MXN, car les maisons de cet &acirc;ge portent souvent une corrosion des armatures par chlorures. D&egrave;s que la r&eacute;paration approche 25&ndash;30% du co&ucirc;t du neuf, la d&eacute;molition est g&eacute;n&eacute;ralement pr&eacute;f&eacute;rable ; d&eacute;molition et &eacute;vacuation co&ucirc;tent $180,000&ndash;$600,000."),
  ("Que contrôle le comité d'architecture de Playacar ?",
   "Hauteur, volume et retraits au-del&agrave; des minima municipaux, forme et mat&eacute;riaux de toiture, fa&ccedil;ade et couleur, murs et cl&ocirc;tures, et l'abattage de chaque arbre, qui doit &ecirc;tre justifi&eacute;. Il fixe aussi les r&egrave;gles de chantier : ouvriers enregistr&eacute;s, horaires, livraisons, stockage et caution."),
  ("Quelle différence entre Phase I et Phase II pour construire ?",
   "La Phase I a des parcelles plus petites et denses avec un acc&egrave;s chantier par rues &eacute;troites qui rench&eacute;rit, et une vraie proximit&eacute; pi&eacute;tonne de la Quinta Avenida. La Phase II offre de grandes parcelles au bord du golf avec v&eacute;g&eacute;tation mature &mdash; et la proximit&eacute; du parcours rend le vitrage concret."),
  ("Pourquoi Playacar coûte-t-il 25% de plus ?",
   "Acc&egrave;s restreint par rues &eacute;troites, ouvriers enregistr&eacute;s et horaires limit&eacute;s, proc&eacute;dure du comit&eacute;, protection des arbres pendant les travaux, sp&eacute;cification marine et niveau de finition attendu &mdash; autant de postes r&eacute;els, pas un suppl&eacute;ment d'adresse."),
 ],
}

Z[("fr","mayakoba")] = {
 "title": "Coût de Construction d'une Maison à Mayakoba 2026",
 "desc": "Mayakoba est l'endroit le plus cher où construire sur la Riviera Maya. Fourchettes au m² 2026, ce que recouvre réellement la spécification niveau resort.",
 "lead": "Une maison de 150 m&sup2; &agrave; <strong>Mayakoba</strong> co&ucirc;te environ <strong>$3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD)</strong> cl&eacute; en main en 2026 &mdash; la fourchette la plus haute du corridor, environ 42% au-dessus du niveau de base de Playa del Carmen. On n'y construit pourtant presque rien &agrave; ce bas de fourchette, et cette page explique pourquoi.",
 "sections": [
  ("Coût par surface et le chiffre réaliste",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Surface</th><th>Cl&eacute; en main (MXN)</th><th>Cl&eacute; en main (USD)</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.60M&ndash;$4.50M</td><td>$200k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$6M&ndash;$7.50M</td><td>$333k&ndash;$417k</td></tr>
<tr><td>350 m&sup2;</td><td>$8.40M&ndash;$10.50M</td><td>$467k&ndash;$583k</td></tr>
<tr><td>500 m&sup2;</td><td>$12M&ndash;$15M</td><td>$667k&ndash;$833k</td></tr>
</tbody></table></div>
<p class="text-muted small">R&eacute;f&eacute;rence : $24,000&ndash;$30,000 MXN/m&sup2; finition standard &agrave; premium. USD/MXN &asymp; 18. Hors terrain, piscine et mobilier.</p>
<p>C'est la fourchette d'entr&eacute;e. Les maisons r&eacute;ellement construites dans le plan directeur font 300&ndash;600 m&sup2; en niveau d'auteur, ce qui place les chiffres r&eacute;els &agrave; <strong>$35,000&ndash;$55,000 MXN/m&sup2;</strong> une fois compt&eacute;s conception architecturale, &eacute;quipements import&eacute;s, domotique compl&egrave;te, piscine con&ccedil;ue et plantations matures. Budg&eacute;ter une villa de Mayakoba &agrave; partir de $24,000, c'est budg&eacute;ter une maison qui ne passerait pas l'examen architectural.</p>"""),
  ("Ce que la prime achète réellement",
   """<ul>
<li><strong>Contr&ocirc;le de la conception.</strong> Un plan directeur construit autour de l'exploitation h&ocirc;teli&egrave;re examine architecture, mat&eacute;riaux, couleur, paysage et &eacute;clairage au standard des h&ocirc;tels voisins. Les d&eacute;p&ocirc;ts sont d&eacute;taill&eacute;s, les cycles d'examen r&eacute;els, et &eacute;conomiser sur la fa&ccedil;ade n'est pas une option.</li>
<li><strong>Attente de finition.</strong> Les comparables sont des r&eacute;sidences de marque. Menuiserie, pierre, vitrage et quincaillerie se sp&eacute;cifient en cons&eacute;quence, et la pose pr&eacute;cise co&ucirc;te plus cher que les mat&eacute;riaux.</li>
<li><strong>Discipline de chantier.</strong> On construit dans un environnement de luxe en exploitation : acc&egrave;s contr&ocirc;l&eacute;, ouvriers enregistr&eacute;s, horaires restreints, palissades occultantes, limites de bruit, obligations de propret&eacute; et caution. Chaque point co&ucirc;te des heures de planning.</li>
<li><strong>Cadre naturel.</strong> Le plan directeur s'organise autour de lagunes, canaux et mangroves. V&eacute;g&eacute;tation conserv&eacute;e, reculs, drainage et rejets sont g&eacute;r&eacute;s aussi au niveau de la communaut&eacute;.</li>
<li><strong>Sp&eacute;cification marine et hygrom&eacute;trique</strong> int&eacute;grale : inox 316, aluminium anodis&eacute; ou &agrave; rev&ecirc;tement marin, enrobage g&eacute;n&eacute;reux, menuiseries ventil&eacute;es.</li>
<li><strong>Raret&eacute;.</strong> Peu de terrains r&eacute;sidentiels et chaque projet est unique : aucune r&eacute;p&eacute;tition pour amortir conception et direction de travaux.</li>
</ul>"""),
  ("Planning, autorisations et postes supplémentaires",
   """<p>Les autorisations passent par la municipalit&eacute; de <strong>Solidaridad</strong>, l'examen architectural de la communaut&eacute; venant avant, et l'examen environnemental prenant au s&eacute;rieux lagune et mangrove. D&eacute;posez aupr&egrave;s de la communaut&eacute; au stade avant-projet : finir un projet puis l'envoyer &agrave; l'examen co&ucirc;te ici un trimestre.</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>En plus du chantier</th><th>MXN</th></tr></thead><tbody>
<tr><td>Conception et ing&eacute;nierie d'auteur &agrave; ce niveau</td><td>10&ndash;15% du chantier</td></tr>
<tr><td>D&eacute;p&ocirc;t communautaire, cycles d'examen, caution</td><td>$150,000&ndash;$600,000</td></tr>
<tr><td>Piscine con&ccedil;ue avec &eacute;quipements</td><td>$900,000&ndash;$3,500,000</td></tr>
<tr><td>Plantations matures et arrosage</td><td>$400,000&ndash;$2,000,000</td></tr>
<tr><td>Ameublement d'une villa de cette classe</td><td>$1,500,000&ndash;$6,000,000</td></tr>
<tr><td>Charges de communaut&eacute;</td><td>R&eacute;currentes &mdash; &agrave; v&eacute;rifier par lot</td></tr>
</tbody></table></div>
<p>Le chantier dure environ <strong>10&ndash;16 mois</strong> pour une villa de cette sp&eacute;cification &mdash; plus que la norme du corridor, car horaires restreints, cycles d'examen et pr&eacute;cision d'ex&eacute;cution prennent du temps.</p>"""),
 ],
 "faq": [
  ("Combien coûte une maison à Mayakoba ?",
   "La fourchette d'entr&eacute;e est de $24,000&ndash;$30,000 MXN/m&sup2;, soit $3.60M&ndash;$4.50M MXN ($200k&ndash;$250k USD) pour 150 m&sup2;. En pratique on y construit des maisons de 300&ndash;600 m&sup2; &agrave; $35,000&ndash;$55,000 MXN/m&sup2; avec conception d'auteur, &eacute;quipements import&eacute;s, domotique, piscine et plantations matures."),
  ("Pourquoi Mayakoba est-il le plus cher du corridor ?",
   "Contr&ocirc;le de conception au standard resort, attente de finition align&eacute;e sur des r&eacute;sidences de marque, discipline de chantier en environnement de luxe en exploitation, gestion environnementale autour des lagunes et mangroves, sp&eacute;cification marine int&eacute;grale et raret&eacute; sans effet de r&eacute;p&eacute;tition."),
  ("Que budgéter en plus du chantier ?",
   "Conception et ing&eacute;nierie &agrave; 10&ndash;15% du chantier, d&eacute;p&ocirc;t et caution $150,000&ndash;$600,000, piscine con&ccedil;ue $900,000&ndash;$3,500,000, plantations matures $400,000&ndash;$2,000,000, ameublement $1,500,000&ndash;$6,000,000 et les charges r&eacute;currentes de communaut&eacute;."),
  ("Combien de temps pour une villa à Mayakoba ?",
   "Environ 10&ndash;16 mois pour une villa de cette sp&eacute;cification, plus que la norme du corridor. Horaires restreints, cycles d'examen de la communaut&eacute; et pr&eacute;cision d'ex&eacute;cution consomment du temps suppl&eacute;mentaire."),
  ("Qui approuve le projet ?",
   "La municipalit&eacute; de Solidaridad pour usage du sol, permis, alignement et DRO, et l'examen architectural de la communaut&eacute;, qui vient en pratique d'abord et porte sur architecture, mat&eacute;riaux, couleur, paysage et &eacute;clairage."),
 ],
}

Z[("fr","corasol")] = {
 "title": "Coût de Construction d'une Maison à Corasol 2026",
 "desc": "Coûts à Corasol 2026 et ce qu'implique bâtir dans un plan directeur en cours : viabilisation par tranches, comité, front de golf et règles d'accès.",
 "lead": "Une maison de 150 m&sup2; &agrave; <strong>Corasol</strong> co&ucirc;te environ <strong>$3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD)</strong> cl&eacute; en main en 2026, soit environ 30% au-dessus du niveau de base de Playa del Carmen. C'est aussi &agrave; Corasol que se trouve notre bureau : cette page s'&eacute;crit &agrave; quelques minutes &agrave; pied du sujet.",
 "sections": [
  ("Coût clé en main par taille de maison",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Surface</th><th>Cl&eacute; en main (MXN)</th><th>Cl&eacute; en main (USD)</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.30M&ndash;$4.12M</td><td>$183k&ndash;$229k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.40M&ndash;$5.50M</td><td>$244k&ndash;$306k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.60M&ndash;$8.25M</td><td>$367k&ndash;$458k</td></tr>
<tr><td>450 m&sup2;</td><td>$9.90M&ndash;$12.38M</td><td>$550k&ndash;$688k</td></tr>
</tbody></table></div>
<p class="text-muted small">R&eacute;f&eacute;rence : $22,000&ndash;$27,500 MXN/m&sup2; finition standard &agrave; premium. USD/MXN &asymp; 18. Hors terrain, piscine et mobilier.</p>
<p>L'essentiel de ce qui se construit ici d&eacute;passe 150 m&sup2; : les parcelles et le march&eacute; poussent vers des villas de 250&ndash;450 m&sup2; avec piscine, toit-terrasse et jardin dessin&eacute;. Budg&eacute;tez l'ensemble et pas seulement le prix au m&egrave;tre : sur une villa de 300 m&sup2;, piscine, plantations, mobilier et honoraires ajoutent couramment 35&ndash;50% au chiffre du chantier.</p>"""),
  ("Bâtir dans une communauté qui se construit encore",
   """<ul>
<li><strong>La viabilisation arrive par tranches.</strong> Faites confirmer, pour votre parcelle, ce qui est r&eacute;ellement en limite aujourd'hui &mdash; puissance &eacute;lectrique, eau, assainissement, rev&ecirc;tement de voirie &mdash; et ce qui n'est que programm&eacute;. L'&eacute;cart entre &laquo; la communaut&eacute; aura &raquo; et &laquo; la parcelle a &raquo; est l&agrave; o&ugrave; les budgets bougent.</li>
<li><strong>Vous aurez des chantiers voisins.</strong> D'autres maisons et des travaux communs se poursuivront des ann&eacute;es : bruit et circulation pendant votre occupation, acc&egrave;s partag&eacute;s pendant votre chantier.</li>
<li><strong>L'examen architectural est actif et &eacute;volutif.</strong> Le comit&eacute; contr&ocirc;le hauteur, volume, mat&eacute;riaux, couleur, cl&ocirc;tures et paysage afin de pr&eacute;server une image coh&eacute;rente dans un ensemble inachev&eacute;. D&eacute;posez au stade avant-projet.</li>
<li><strong>R&egrave;gles d'acc&egrave;s et de chantier.</strong> Ouvriers enregistr&eacute;s, entr&eacute;e contr&ocirc;l&eacute;e, cr&eacute;neaux de livraison, limites de stockage sur la parcelle, nettoyage de voirie et caution. Comptez $80,000&ndash;$300,000 MXN pour d&eacute;p&ocirc;t, caution et gestion des acc&egrave;s.</li>
<li><strong>Le front de golf</strong> pose la question du vitrage et des verri&egrave;res &mdash; les balles &eacute;gar&eacute;es sont un risque r&eacute;el et chiffrable &mdash; ainsi que l'interface arrosage-drainage avec le parcours.</li>
</ul>"""),
  ("Conditions de site, autorisations et planning",
   """<p>Corasol rel&egrave;ve de la municipalit&eacute; de <strong>Solidaridad</strong> : certificat d'usage du sol, alignement, permis de construire et Director Responsable de Obra, l'examen architectural de la communaut&eacute; venant en pratique d'abord. Les exigences environnementales s'appliquent comme ailleurs sur cette c&ocirc;te, et le karst impose une &eacute;tude de sol avec sondages sur l'emprise r&eacute;elle &mdash; bonne portance et cavit&eacute; &agrave; deux m&egrave;tres sont ici &eacute;galement normales.</p>
<ul>
<li><strong>La sp&eacute;cification marine reste de mise.</strong> Corasol est assez proche de la mer pour que l'inox 316, l'aluminium anodis&eacute; ou &agrave; rev&ecirc;tement marin et un enrobage g&eacute;n&eacute;reux soient le bon choix, non une option.</li>
<li><strong>Concevez la toiture en terrasse d&egrave;s le d&eacute;part</strong> si la hauteur le permet. Sur les parcelles avec vue sur le parcours ou vers la mer, c'est le m&egrave;tre carr&eacute; le plus pr&eacute;cieux de la maison.</li>
<li><strong>Pr&eacute;voyez les locaux techniques :</strong> citerne, surpresseur, traitement de l'eau pour la duret&eacute; locale, &eacute;quipements de piscine et emplacements de climatisation, tous accessibles pour la maintenance.</li>
</ul>
<p>Le chantier dure environ <strong>8&ndash;12 mois</strong> pour une villa de 250&ndash;300 m&sup2;, davantage si l'examen d&eacute;passe un cycle. Si vous achetez la parcelle maintenant pour b&acirc;tir plus tard, faites confirmer par &eacute;crit l'&eacute;tat des r&eacute;seaux en limite avant la signature.</p>"""),
 ],
 "faq": [
  ("Combien coûte une maison à Corasol ?",
   "Environ $3.30M&ndash;$4.12M MXN ($183k&ndash;$229k USD) cl&eacute; en main pour 150 m&sup2; &mdash; soit $22,000&ndash;$27,500 MXN/m&sup2;, environ 30% au-dessus du niveau de base de Playa del Carmen. La plupart des maisons y font 250&ndash;450 m&sup2;, o&ugrave; piscine, plantations, mobilier et honoraires ajoutent 35&ndash;50%."),
  ("Que vérifier avant d'acheter une parcelle à Corasol ?",
   "Quels r&eacute;seaux sont r&eacute;ellement en limite de parcelle aujourd'hui &mdash; puissance &eacute;lectrique, eau, assainissement, voirie &mdash; par rapport &agrave; ce qui n'est que programm&eacute;. Dans un plan directeur en cours, c'est pr&eacute;cis&eacute;ment l&agrave; que se joue le budget."),
  ("Le comité d'architecture coûte-t-il du temps et de l'argent ?",
   "Les deux. Comptez $80,000&ndash;$300,000 MXN pour le d&eacute;p&ocirc;t, la caution et la gestion des acc&egrave;s, et au moins un cycle d'examen au planning, en plus des ouvriers enregistr&eacute;s, de l'entr&eacute;e contr&ocirc;l&eacute;e, des cr&eacute;neaux de livraison et du nettoyage de voirie."),
  ("Qu'est-ce que change le front de golf ?",
   "La sp&eacute;cification du vitrage et des verri&egrave;res, les balles &eacute;gar&eacute;es &eacute;tant un risque r&eacute;el et chiffrable, ainsi que l'interface arrosage-drainage avec le parcours. Cela se r&egrave;gle en conception, pas par un remplacement de vitrage ensuite."),
  ("Combien de temps pour une villa à Corasol ?",
   "Environ 8&ndash;12 mois pour 250&ndash;300 m&sup2; du permis &agrave; la remise, davantage si l'examen architectural d&eacute;passe un cycle. Horaires restreints et acc&egrave;s contr&ocirc;l&eacute; poussent le planning vers le haut."),
 ],
}

Z[("fr","aldea-zama")] = {
 "title": "Coût de Construction d'une Maison à Aldea Zamá 2026",
 "desc": "Coûts à Aldea Zamá 2026 plus le poste que personne ne budgète : le calendrier des autorisations de Tulum. Hauteur, fiabilité électrique, plan viabilisé.",
 "lead": "Une maison de 150 m&sup2; &agrave; <strong>Aldea Zam&aacute;</strong> co&ucirc;te environ <strong>$3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD)</strong> cl&eacute; en main en 2026, soit environ 20% au-dessus du niveau de base de Playa del Carmen. Le chiffre du chantier est simple. Ce que l'on oublie de budg&eacute;ter &agrave; Tulum, c'est le temps.",
 "sections": [
  ("Coût clé en main par taille de maison",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Surface</th><th>Cl&eacute; en main (MXN)</th><th>Cl&eacute; en main (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.05M&ndash;$2.50M</td><td>$114k&ndash;$139k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.08M&ndash;$3.75M</td><td>$171k&ndash;$208k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.10M&ndash;$5M</td><td>$228k&ndash;$278k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.15M&ndash;$7.50M</td><td>$342k&ndash;$417k</td></tr>
</tbody></table></div>
<p class="text-muted small">R&eacute;f&eacute;rence : $20,500&ndash;$25,000 MXN/m&sup2; finition standard &agrave; premium. USD/MXN &asymp; 18. Hors terrain, piscine et mobilier.</p>
<p>Aldea Zam&aacute; se situe au-dessus des Regiones de Tulum et de La Veleta pour une raison simple : c'est un plan directeur viabilis&eacute;, r&eacute;seaux enterr&eacute;s, voiries rev&ecirc;tues et caract&egrave;re &eacute;tabli, &agrave; distance de marche ou de v&eacute;lo de la route de plage. Vous payez une infrastructure qui existe plut&ocirc;t qu'une infrastructure &agrave; construire.</p>"""),
  ("Ce que coûte réellement le calendrier des autorisations",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Étape</th><th>Durée</th></tr></thead><tbody>
<tr><td>Certificat d'usage du sol et alignement</td><td>2&ndash;8 semaines</td></tr>
<tr><td>&Eacute;tude de sol (en parall&egrave;le)</td><td>2&ndash;5 semaines</td></tr>
<tr><td>Dossier environnemental</td><td>3&ndash;8 mois selon la v&eacute;g&eacute;tation</td></tr>
<tr><td>Projet technique (en parall&egrave;le)</td><td>6&ndash;14 semaines</td></tr>
<tr><td>Instruction du permis avec dossier complet</td><td>4&ndash;12 semaines</td></tr>
<tr><td><strong>Total avant le démarrage</strong></td><td><strong>5&ndash;12 mois</strong></td></tr>
</tbody></table></div>
<p>Ces mois sont un poste r&eacute;el : terrain port&eacute;, capital immobilis&eacute;, aucun rendement. Deux fa&ccedil;ons de les r&eacute;duire. D'abord, lancer le dossier environnemental et l'&eacute;tude de sol alors que l'architecture est encore en avant-projet &mdash; aucun des deux n'exige de plans d&eacute;finitifs et tous deux orientent la conception. Ensuite, en comparant des parcelles, valoriser fortement une autorisation environnementale existante : elle peut valoir six mois et un montant &agrave; six chiffres.</p>"""),
  ("Hauteur, électricité et ce qui se construit ici",
   """<ul>
<li><strong>Les limites de hauteur sont strictes</strong> et appliqu&eacute;es. Les r&egrave;gles de Tulum sont d&eacute;lib&eacute;r&eacute;ment plus serr&eacute;es qu'&agrave; Playa del Carmen : v&eacute;rifiez la valeur exacte pour votre parcelle avant de dessiner un toit-terrasse &mdash; sur beaucoup de terrains, tout tient &agrave; ce seul chiffre.</li>
<li><strong>Le r&eacute;seau &eacute;lectrique est moins fiable</strong> qu'&agrave; Playa del Carmen. Pr&eacute;voyez une protection contre les surtensions pour toute la maison en standard et, en locatif, un syst&egrave;me de batteries pour l'essentiel &mdash; internet, r&eacute;gulation de piscine, un peu d'&eacute;clairage et un ventilateur &mdash; pour $140,000&ndash;$330,000 MXN. Le solaire est particuli&egrave;rement pertinent d&egrave;s que pompe de piscine et plusieurs climatiseurs font basculer la consommation sur le tarif DAC.</li>
<li><strong>Le march&eacute; est domin&eacute; par les copropri&eacute;t&eacute;s,</strong> ce qui est pr&eacute;cis&eacute;ment l'argument en faveur d'une maison. Une maison individuelle ne peut pas se voir retirer la location courte dur&eacute;e par une assembl&eacute;e, ne paie pas de charges sur le brut et se con&ccedil;oit pour le rendement : chambres avec salle de bain, casita ind&eacute;pendante, toit-terrasse, piscine plac&eacute;e pour la photo.</li>
</ul>
<p>Techniquement, les points habituels de Tulum s'appliquent : traitement avant infiltration dimensionn&eacute; &agrave; l'occupation ($90,000&ndash;$250,000 MXN), traitement de l'eau pour la duret&eacute;, d&eacute;tails contre termites et humidit&eacute;, et &eacute;tude de sol car le karst y est riche en cenotes. Le chantier dure environ <strong>7&ndash;11 mois</strong> pour 150&ndash;200 m&sup2;.</p>"""),
 ],
 "faq": [
  ("Combien coûte une maison à Aldea Zamá ?",
   "Environ $3.08M&ndash;$3.75M MXN ($171k&ndash;$208k USD) cl&eacute; en main pour 150 m&sup2; en finition standard &agrave; premium &mdash; soit $20,500&ndash;$25,000 MXN/m&sup2;, environ 20% au-dessus du niveau de base de Playa del Carmen."),
  ("Pourquoi est-ce plus cher que les Regiones de Tulum ?",
   "Parce que l'infrastructure existe d&eacute;j&agrave; : plan directeur viabilis&eacute;, r&eacute;seaux enterr&eacute;s, voiries rev&ecirc;tues et caract&egrave;re &eacute;tabli pr&egrave;s de la route de plage. Sur une parcelle de Regi&oacute;n moins ch&egrave;re, vous payez ensuite vous-m&ecirc;me les r&eacute;seaux, l'acc&egrave;s et l'environnement."),
  ("Combien de temps avant de démarrer le chantier à Tulum ?",
   "De cinq &agrave; douze mois apr&egrave;s l'achat : 2&ndash;8 semaines pour l'usage du sol et l'alignement, 3&ndash;8 mois de dossier environnemental sur terrain v&eacute;g&eacute;talis&eacute;, et 4&ndash;12 semaines d'instruction du permis. Lancez dossier et &eacute;tude de sol d&egrave;s l'avant-projet."),
  ("Un toit-terrasse est-il possible à Aldea Zamá ?",
   "Cela d&eacute;pend de la limite de hauteur de votre parcelle, et &agrave; Tulum ces limites sont volontairement serr&eacute;es et appliqu&eacute;es. V&eacute;rifiez la valeur avant de concevoir : sur beaucoup de terrains, c'est ce qui s&eacute;pare un bon projet d'un projet compromis."),
  ("Que faire face aux coupures de courant à Tulum ?",
   "Protection contre les surtensions pour toute la maison en standard et, en locatif, des batteries pour internet, r&eacute;gulation de piscine, &eacute;clairage et ventilateur, pour $140,000&ndash;$330,000 MXN. Le solaire s'amortit &eacute;galement vite, surtout en tarif DAC."),
 ],
}

Z[("fr","playa-del-carmen")] = {
 "title": "Coût de Construction d'une Maison à Playa del Carmen 2026",
 "desc": "Le prix de référence du corridor. Budget par phases pour 150 m², ce que le prix au m² inclut ou non, postes annexes et comment tenir le budget.",
 "lead": "Une maison familiale bien construite de 150 m&sup2; &agrave; <strong>Playa del Carmen</strong> co&ucirc;te environ <strong>$2.6M&ndash;$3.2M MXN ($145 000&ndash;$178 000 USD)</strong> cl&eacute; en main en 2026. C'est le chiffre auquel se compare tout le corridor : mieux vaut le comprendre par phases que comme un total unique.",
 "sections": [
  ("Budget par phases (maison standard de 150 m²)",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Phase</th><th>% du budget</th><th>Co&ucirc;t (MXN)</th><th>Contenu</th></tr></thead><tbody>
<tr><td>Autorisations, DRO et &eacute;tudes</td><td>5%</td><td>$130 000&ndash;$160 000</td><td>Permis, DRO, &eacute;tude de sol, topographie</td></tr>
<tr><td>Fondations et structure</td><td>30%</td><td>$780 000&ndash;$960 000</td><td>Dalle, poteaux, poutres, planchers</td></tr>
<tr><td>Murs et toiture</td><td>18%</td><td>$470 000&ndash;$580 000</td><td>Blocs, cha&icirc;nages, dalle de toiture</td></tr>
<tr><td>Installations</td><td>15%</td><td>$390 000&ndash;$480 000</td><td>&Eacute;lectricit&eacute;, plomberie, assainissement</td></tr>
<tr><td>Finitions</td><td>25%</td><td>$650 000&ndash;$800 000</td><td>Sols, peinture, chukum, menuiserie</td></tr>
<tr><td>Nettoyage et remise</td><td>7%</td><td>$180 000&ndash;$220 000</td><td>Finitions de d&eacute;tail, livraison</td></tr>
</tbody></table></div>
<p class="text-muted small">Total cl&eacute; en main &asymp; $2.6M&ndash;$3.2M MXN. Hors terrain, piscine et mobilier.</p>
<p>Deux lectures. La structure repr&eacute;sente pr&egrave;s d'un tiers du budget et c'est la seule phase o&ugrave; &eacute;conomiser est r&eacute;ellement dangereux en zone de vents forts. Et les finitions, &agrave; 25%, sont l&agrave; o&ugrave; vit votre sp&eacute;cification : le m&ecirc;me gros &oelig;uvre avec d'autres finitions d&eacute;place le total de 20% sans changer un plan.</p>"""),
  ("Ce que le prix au m² inclut et n'inclut pas",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Poste</th><th>MXN</th></tr></thead><tbody>
<tr><td>Terrain</td><td>&Agrave; part, et la plus grande variable &agrave; Playa del Carmen</td></tr>
<tr><td>Piscine 4&times;8 m avec &eacute;quipements</td><td>$450 000&ndash;$1 200 000</td></tr>
<tr><td>Am&eacute;nagement du toit-terrasse (structure pr&eacute;vue)</td><td>$3 500&ndash;$9 000 par m&sup2;</td></tr>
<tr><td>Traitement de l'eau (filtre, adoucisseur, charbon, osmose)</td><td>$35 000&ndash;$95 000</td></tr>
<tr><td>Climatisation, 4&ndash;5 zones inverter</td><td>$120 000&ndash;$280 000</td></tr>
<tr><td>Solaire, 5&ndash;8 kWc</td><td>$115 000&ndash;$250 000</td></tr>
<tr><td>Plantations et arrosage</td><td>$500&ndash;$2 000 par m&sup2;</td></tr>
<tr><td>Mobilier et &eacute;lectrom&eacute;nager</td><td>$450 000&ndash;$1 200 000 pour une maison familiale</td></tr>
</tbody></table></div>
<p>Conception, ing&eacute;nierie, &eacute;tudes et autorisations repr&eacute;sentent ensemble 8&ndash;14% du co&ucirc;t de construction sur une maison sur mesure &mdash; en partie d&eacute;j&agrave; refl&eacute;t&eacute;s dans le tableau ci-dessus, et ce n'est pas un poste &agrave; comprimer : chaque erreur qu'il &eacute;vite co&ucirc;te plus cher que l'ensemble.</p>"""),
  ("Pourquoi c'est la référence et comment tenir le budget",
   """<p>Playa del Carmen se situe sous les zones ferm&eacute;es et premium pour des raisons structurelles, non de qualit&eacute; : base de fournisseurs large, concurrence r&eacute;elle, parcelles urbaines viabilis&eacute;es, parcours d'autorisation direct aupr&egrave;s de la municipalit&eacute; de <strong>Solidaridad</strong> et absence de zone f&eacute;d&eacute;rale maritime sur la grande majorit&eacute; des terrains. Tout le reste du corridor est un multiple de ce chiffre : Puerto Morelos &agrave; parit&eacute;, Puerto Aventuras environ +8%, Akumal +12%, Aldea Zam&aacute; +20%, Playacar +25%, Corasol +30%, Mayakoba +42%.</p>
<ul>
<li><strong>Prix ferme avec budget d&eacute;taill&eacute;,</strong> et non un prix au m&egrave;tre convenu de vive voix. Un taux unique multipli&eacute; par des m&egrave;tres n'est pas un budget, c'est une invitation &agrave; ren&eacute;gocier.</li>
<li><strong>Paiements &agrave; l'avancement physique v&eacute;rifi&eacute;,</strong> non &agrave; des dates, avec 5&ndash;10% de retenue lib&eacute;r&eacute;e apr&egrave;s lev&eacute;e des r&eacute;serves.</li>
<li><strong>Avenants &eacute;crits et chiffr&eacute;s</strong> avant ex&eacute;cution. Les modifications verbales sont le chemin le plus court du prix ferme au prix ouvert.</li>
<li><strong>Liste d'exclusions explicite</strong> &mdash; mobilier, &eacute;lectrom&eacute;nager, plantations au-del&agrave; d'une limite, frais de raccordement &mdash; convenue &agrave; la signature.</li>
</ul>
<p>Une maison de 150 m&sup2; demande environ <strong>7&ndash;10 mois</strong> &agrave; partir du permis, plus deux &agrave; quatre mois de proc&eacute;dures pr&eacute;alables. Pour une estimation rapide, utilisez le <a href="/calculateur/">calculateur de co&ucirc;ts</a>.</p>"""),
 ],
 "faq": [
  ("Combien coûte une maison à Playa del Carmen en 2026 ?",
   "Environ $2.6M&ndash;$3.2M MXN ($145 000&ndash;$178 000 USD) cl&eacute; en main pour 150 m&sup2; en finition standard &mdash; soit $17 000&ndash;$21 000 MXN/m&sup2;, hors terrain, piscine et mobilier."),
  ("Qu'est-ce qui n'est pas inclus dans le prix au mètre carré ?",
   "Le terrain, la piscine ($450 000&ndash;$1 200 000), l'am&eacute;nagement du toit-terrasse, le traitement de l'eau, la climatisation, le solaire, les plantations et le mobilier. C'est de l&agrave; que viennent presque toutes les surprises : traitez-les comme des postes &agrave; part d&egrave;s le d&eacute;but."),
  ("Quelle phase coûte le plus cher ?",
   "Fondations et structure, environ 30% du budget, puis les finitions &agrave; 25%. La structure est aussi la phase o&ugrave; &eacute;conomiser est dangereux en zone de vents forts, tandis que les finitions peuvent d&eacute;placer le total de 20% sans changer un plan."),
  ("Comment Playa del Carmen se compare-t-il aux autres zones ?",
   "C'est la r&eacute;f&eacute;rence. Puerto Morelos est &agrave; parit&eacute;, Puerto Aventuras +8%, Akumal +12%, Aldea Zam&aacute; +20%, Playacar +25%, Corasol +30% et Mayakoba +42% &mdash; ces &eacute;carts viennent des acc&egrave;s restreints, des comit&eacute;s d'architecture, de la sp&eacute;cification marine et des exigences environnementales."),
  ("Comment éviter la dérive du budget ?",
   "Prix ferme avec budget d&eacute;taill&eacute; plut&ocirc;t qu'un taux au m&egrave;tre, paiements &agrave; l'avancement v&eacute;rifi&eacute; avec 5&ndash;10% de retenue, avenants &eacute;crits et chiffr&eacute;s avant ex&eacute;cution, et liste d'exclusions explicite convenue &agrave; la signature."),
 ],
}

Z[("fr","tulum")] = {
 "title": "Coût de Construction d'une Maison à Tulum 2026 : Le Terrain",
 "desc": "Coûts de construction à Tulum 2026 et pourquoi c'est le terrain — réseaux, végétation, dossier environnemental — qui décide du total, pas la maison.",
 "lead": "Une maison de 150 m&sup2; &agrave; <strong>Tulum</strong> co&ucirc;te environ <strong>$2.85M&ndash;$3.60M MXN ($158k&ndash;$200k USD)</strong> cl&eacute; en main en 2026. Mais la dispersion des totaux y est plus large que partout ailleurs sur le corridor &mdash; et la raison n'est presque jamais la maison, c'est le terrain.",
 "sections": [
  ("Coût par surface et par emplacement",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Surface</th><th>Cl&eacute; en main (MXN)</th><th>Cl&eacute; en main (USD)</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.90M&ndash;$2.40M</td><td>$106k&ndash;$133k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.85M&ndash;$3.60M</td><td>$158k&ndash;$200k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.80M&ndash;$4.80M</td><td>$211k&ndash;$267k</td></tr>
<tr><td>300 m&sup2;</td><td>$5.70M&ndash;$7.20M</td><td>$317k&ndash;$400k</td></tr>
</tbody></table></div>
<p class="text-muted small">R&eacute;f&eacute;rence : $19,000&ndash;$24,000 MXN/m&sup2; finition standard &agrave; premium. USD/MXN &asymp; 18. Hors terrain, piscine et mobilier.</p>
<p>&Agrave; l'int&eacute;rieur de Tulum, les secteurs divergent nettement : les Regiones et La Veleta en bas de fourchette, Aldea Zam&aacute; et le Tulum Country Club au-dessus, la route de plage avec sp&eacute;cification marine et dossier environnemental lourd bien au-dessus.</p>"""),
  ("Pourquoi le terrain décide du total",
   """<p>Quatre postes varient avec le terrain et non avec la surface de la maison :</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Poste</th><th>MXN</th></tr></thead><tbody>
<tr><td>Dossier environnemental selon la v&eacute;g&eacute;tation</td><td>$80,000&ndash;$300,000</td></tr>
<tr><td>Station d'&eacute;puration ou biodigesteur avec &eacute;pandage</td><td>$90,000&ndash;$250,000</td></tr>
<tr><td>Raccordement CFE en rue viabilis&eacute;e</td><td>$10,000&ndash;$40,000</td></tr>
<tr><td>Extension CFE vers un terrain non viabilis&eacute;</td><td>$150,000&ndash;plus de $900,000</td></tr>
<tr><td>Autonomie au lieu du raccordement (solaire, stockage, puits)</td><td>$250,000&ndash;$800,000</td></tr>
<tr><td>Acc&egrave;s et d&eacute;frichement en terrain de jungle</td><td>$40,000&ndash;$300,000</td></tr>
</tbody></table></div>
<p>La d&eacute;cision la plus importante &agrave; Tulum est donc le choix du terrain, pas la liste des finitions. Faites chiffrer l'extension CFE <em>avant</em> l'achat : ce seul chiffre d&eacute;termine si le raccordement ou une autonomie con&ccedil;ue est la voie la moins ch&egrave;re et la plus rapide.</p>"""),
  ("Calendrier, électricité et exécution",
   """<p>L'examen environnemental de Tulum est le plus exigeant du corridor. De l'achat au d&eacute;marrage, comptez r&eacute;alistement <strong>6&ndash;14 mois</strong> : certificat d'usage du sol et alignement 2&ndash;8 semaines, dossier environnemental 4&ndash;9 mois sur terrain v&eacute;g&eacute;talis&eacute;, projet technique en parall&egrave;le, instruction du permis 4&ndash;12 semaines. Lancez dossier et &eacute;tude de sol d&egrave;s l'avant-projet.</p>
<ul>
<li><strong>Les limites de hauteur sont strictes</strong> et appliqu&eacute;es &mdash; v&eacute;rifiez la valeur de votre parcelle avant de dessiner un toit-terrasse.</li>
<li><strong>Le r&eacute;seau est moins fiable</strong> que plus au nord : protection contre les surtensions en standard et, en locatif, batteries pour internet, r&eacute;gulation de piscine et &eacute;clairage de base, $140,000&ndash;$330,000 MXN.</li>
<li><strong>Cenotes et karst</strong> imposent &eacute;tude de sol avec sondages et reculs d'infiltration. Ce qui s'infiltre ici atteint l'aquif&egrave;re puis le r&eacute;cif.</li>
<li><strong>Termites et humidit&eacute; :</strong> aucun contact bois-sol, traitement du terrain avant dalle, menuiseries ventil&eacute;es, d&eacute;shumidification des pi&egrave;ces ferm&eacute;es.</li>
</ul>
<p>Le chantier lui-m&ecirc;me dure environ <strong>7&ndash;11 mois</strong> pour 150&ndash;200 m&sup2;. Prix ferme, budget d&eacute;taill&eacute;, paiements &agrave; l'avancement v&eacute;rifi&eacute; &mdash; et le calendrier des autorisations int&eacute;gr&eacute; au plan d&egrave;s le d&eacute;part.</p>"""),
 ],
 "faq": [
  ("Combien coûte une maison à Tulum en 2026 ?",
   "Environ $2.85M&ndash;$3.60M MXN ($158k&ndash;$200k USD) cl&eacute; en main pour 150 m&sup2; &mdash; soit $19,000&ndash;$24,000 MXN/m&sup2;. Les Regiones et La Veleta sont en bas de fourchette, Aldea Zam&aacute; au-dessus, la route de plage bien au-dessus."),
  ("Pourquoi les totaux varient-ils autant à Tulum ?",
   "Parce que quatre postes importants d&eacute;pendent du terrain et non de la maison : dossier environnemental $80,000&ndash;$300,000, station d'&eacute;puration $90,000&ndash;$250,000, &eacute;lectricit&eacute; de $10,000 &agrave; plus de $900,000, et acc&egrave;s en jungle $40,000&ndash;$300,000."),
  ("Raccordement ou autonomie ?",
   "Faites chiffrer l'extension CFE avant l'achat. Si elle se situe dans le haut des six chiffres, une autonomie con&ccedil;ue avec solaire, stockage, puits trait&eacute; et r&eacute;cup&eacute;ration d'eau de pluie &agrave; $250,000&ndash;$800,000 est souvent moins ch&egrave;re et plus rapide."),
  ("Combien de temps avant de démarrer ?",
   "R&eacute;alistement 6&ndash;14 mois apr&egrave;s l'achat, principalement &agrave; cause du dossier environnemental qui demande 4&ndash;9 mois sur terrain v&eacute;g&eacute;talis&eacute;. Dossier et &eacute;tude de sol doivent d&eacute;marrer pendant l'avant-projet."),
  ("Quels points techniques comptent le plus à Tulum ?",
   "Traitement avant infiltration avec reculs corrects vis-&agrave;-vis des cenotes, &eacute;tude de sol &agrave; cause du karst, protection contre les surtensions et &eacute;ventuellement batteries vu la qualit&eacute; du r&eacute;seau, et un traitement rigoureux des termites et de l'humidit&eacute; sans contact bois-sol."),
 ],
}

Z[("zh","cancun")] = {
 "title": "2026年坎昆建房成本：为什么这里最便宜",
 "desc": "坎昆是整个走廊建房最便宜的地方。2026年每平米价格区间、便宜的原因，以及便宜在什么情况下会变成风险。",
 "lead": "2026年在<strong>坎昆</strong>建一栋150平米的家庭住宅，交钥匙约需 <strong>$2.48M&ndash;$3M 比索（$138k&ndash;$167k 美元）</strong> &mdash; 这是整个走廊最低的数字，同等装修标准下比普拉亚德尔卡门低约4%。本页说明这个折扣从何而来，以及它在什么时候不再划算。",
 "sections": [
  ("为什么坎昆比走廊其他地方便宜",
   """<p>坎昆是走廊上唯一一个市场规模对建房者有利的地方：全区最大的建筑劳动力池、最密集的材料供应商与加工厂，以及足够多相互竞争的施工企业，价格因此真正受到检验。普埃尔托莫雷洛斯以南的一切，都要从这里调一部分资源。</p>
<ul>
<li><strong>材料就地采购。</strong>砌块、水泥、钢筋、骨料、铝材、瓷砖和卫浴都在本地购买，不承担走廊运费 &mdash; 仅此一项在150平米住宅上就值几个百分点。</li>
<li><strong>工种无需调动。</strong>去图卢姆或阿库马尔需要排期并长途运送的专业工程，在这里只是一个本地电话。</li>
<li><strong>内陆住宅地块。</strong>坎昆的住宅建设主要发生在内陆封闭社区：没有联邦海域区、没有 ZOFEMAT 特许、没有海龟产卵季日程，环评文件也比同等面积的海边地块轻得多。</li>
</ul>
<p>许可在 <strong>贝尼托华雷斯</strong> 市政厅办理 &mdash; 土地用途、施工许可、红线和责任建筑师（DRO）&mdash; 对于已通市政管网的住宅地块，这是全州最可预期的流程之一。</p>"""),
  ("按住宅面积的交钥匙造价",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>住宅面积</th><th>交钥匙（比索）</th><th>交钥匙（美元）</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.65M&ndash;$2M</td><td>$92k&ndash;$111k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.48M&ndash;$3M</td><td>$138k&ndash;$167k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.30M&ndash;$4M</td><td>$183k&ndash;$222k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.13M&ndash;$5M</td><td>$229k&ndash;$278k</td></tr>
</tbody></table></div>
<p class="text-muted small">参考：标准装修 $16,500&ndash;$20,000 比索/平米。美元/比索 &asymp; 18。不含土地、泳池和家具。</p>
<p>以上区间适用于内陆住宅区。酒店区、金岛（Isla Dorada）或任何面海、面潟湖的地块则是另一种建筑：全套海洋级规格、联邦区权属问题，以及地段本身要求的装修水准。那里的合理区间是 $26,000&ndash;$40,000 比索/平米。</p>"""),
  ("便宜在哪里会变成风险",
   """<p>庞大而竞争激烈的市场会带来低价，也会带来巨大的质量落差。坎昆的问题从来不是贵，而是便宜。</p>
<ul>
<li><strong>低于约 $14,000 比索/平米的报价</strong>一定在结构上做了削减 &mdash; 通常是配筋密度、混凝土标号或电气工程。在强风区，钢筋不是省钱的地方。</li>
<li><strong>没有地质勘察。</strong>喀斯特地层可能给出极好的承载力，而两米之外就是溶洞。覆盖实际建筑轮廓的钻孔勘察花费 $25,000&ndash;$60,000，是整个项目中最便宜的风险控制。</li>
<li><strong>社区规约。</strong>Residencial Cumbres、Lagos del Sol、Villa Magna、Aqua、Palmaris 都设有设计委员会，对高度、退线、材料和色彩另有规定，并要求工人登记、限制施工时段、缴纳施工保证金。请在方案阶段提交。</li>
<li><strong>交通与送货时段。</strong>坎昆是走廊上唯一需要把城市交通计入工期的地方，内陆社区的送货必须安排时间窗口。</li>
<li><strong>盐分同样深入内陆。</strong>即使离海数公里，紧固件、栏杆和空调冷凝器盘管采用 316 不锈钢与海洋级涂层也会明显更耐久。</li>
</ul>
<p>150平米住宅从许可到交付约需 <strong>7&ndash;10 个月</strong>，而坎昆的供应链深度可以避免不少在南边常见的等料停工。务必签订带分项预算的固定总价合同，并按经核验的实际进度付款。</p>"""),
 ],
 "faq": [
  ("2026年在坎昆建房要多少钱？",
   "内陆住宅地块上，150平米标准装修交钥匙约 $2.48M&ndash;$3M 比索（$138k&ndash;$167k 美元），不含土地、泳池和家具 &mdash; 折合约 $16,500&ndash;$20,000 比索/平米。"),
  ("为什么坎昆比普拉亚德尔卡门或图卢姆便宜？",
   "因为规模：全走廊最大的劳动力池、最密集的供应商与加工厂，以及施工企业之间的真实竞争。加上住宅建设多在内陆地块，避开了联邦海域区、海龟产卵规定和海边地块更重的环评文件。"),
  ("这个价格适用于酒店区吗？",
   "不适用。酒店区、金岛或任何面海、面潟湖的地块都意味着全套海洋级规格、联邦区权属问题和更高的装修标准 &mdash; 请按 $26,000&ndash;$40,000 比索/平米预算。"),
  ("坎昆的报价最低可以到多少？",
   "把低于约 $14,000 比索/平米的报价当作警示信号。在这个价位上一定削减了结构部分 &mdash; 配筋密度、混凝土标号或电气 &mdash; 而在强风区，这些正是不该省的地方。"),
  ("封闭社区会增加成本吗？",
   "会。Residencial Cumbres、Lagos del Sol、Villa Magna、Aqua 和 Palmaris 都有自己的设计委员会，对高度、退线、材料和颜色另有限制，还要求工人登记、限制施工时段并缴纳保证金。预算里要留出审查周期，而不只是费用。"),
 ],
}

Z[("zh","puerto-aventuras")] = {
 "title": "2026年普埃尔托阿文图拉斯建房成本：完整预算",
 "desc": "普埃尔托阿文图拉斯的交钥匙造价，以及买家常忽略的码头社区支出：HOA费用、泊位、运河护岸和设计委员会。",
 "lead": "2026年在<strong>普埃尔托阿文图拉斯</strong>建一栋150平米住宅，交钥匙约需 <strong>$2.77M&ndash;$3.38M 比索（$154k&ndash;$188k 美元）</strong>，比普拉亚德尔卡门高约8%。施工本身是可预期的部分；真正让码头社区预算失控的，是下面这些项目。",
 "sections": [
  ("按住宅面积的交钥匙造价",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>住宅面积</th><th>交钥匙（比索）</th><th>交钥匙（美元）</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.85M&ndash;$2.25M</td><td>$103k&ndash;$125k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.77M&ndash;$3.38M</td><td>$154k&ndash;$188k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.70M&ndash;$4.50M</td><td>$206k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.63M&ndash;$5.63M</td><td>$257k&ndash;$313k</td></tr>
</tbody></table></div>
<p class="text-muted small">参考：标准装修 $18,500&ndash;$22,500 比索/平米。美元/比索 &asymp; 18。不含土地、泳池和家具。</p>
<p>比普拉亚德尔卡门高出的这8%，对应四件具体的事，而不是地址溢价：门禁管控与工人登记、限制施工时段而拉长工期、社区内部更长的材料搬运距离，以及运河与近海位置所要求的海洋级规格。</p>"""),
  ("被忽略的支出项",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>项目</th><th>需要核实什么</th></tr></thead><tbody>
<tr><td><strong>HOA 维护费</strong></td><td>该地块当前的具体金额、背后的预算，以及过去五年的变化趋势。运河边和靠近码头的地块通常更高。</td></tr>
<tr><td><strong>码头泊位</strong></td><td>属于产权、租赁还是分配使用 &mdash; 在法律上和转售时是三件不同的事 &mdash; 以及年度费用。码头工程与住宅分开报批。</td></tr>
<tr><td><strong>运河护岸</strong></td><td>由不向您出售该房产的人评估其状况。修复护岸本身就是一个独立工程。</td></tr>
<tr><td><strong>设计委员会</strong></td><td>提交、审查周期与施工保证金：预留 $60,000&ndash;$250,000 比索，工期中至少留出一轮审查。</td></tr>
<tr><td><strong>海洋级规格</strong></td><td>316 紧固件、阳极氧化或海洋级涂层铝材、加大混凝土保护层。施工时更贵，十年维度上省得更多。</td></tr>
</tbody></table></div>
<p>许可通过 <strong>索利达里达德</strong> 市政厅办理 &mdash; 与普拉亚德尔卡门同一路径 &mdash; 实务上社区的建筑审查排在前面。</p>"""),
  ("运河地块：技术上有什么不同",
   """<ul>
<li><strong>地下水位高。</strong>基坑、蓄水池和泳池池体都需要降水与抗浮验算 &mdash; 在错误的时间排空泳池，池体可能上浮。</li>
<li><strong>持续的盐雾</strong>来自水面，而非季节性暴露。在这里 316 不锈钢不再是偏好问题。</li>
<li><strong>风暴暴露。</strong>临水地块承受完整风荷载，遇到强烈事件还有风暴潮。面水立面采用夹胶或抗冲击玻璃，是我们不让步的一项规格。</li>
<li><strong>水际构筑物</strong>有独立的设计与审批要求。</li>
</ul>
<p>150平米住宅自许可起约需 <strong>7&ndash;10 个月</strong>，社区内的施工时段限制会把工期推向上限。签订带分项预算的固定总价合同，并按经核验进度付款。</p>"""),
 ],
 "faq": [
  ("在普埃尔托阿文图拉斯建房要多少钱？",
   "150平米标准装修交钥匙约 $2.77M&ndash;$3.38M 比索（$154k&ndash;$188k 美元），不含土地、泳池和家具 &mdash; 折合约 $18,500&ndash;$22,500 比索/平米，比普拉亚德尔卡门高约8%。"),
  ("为什么比普拉亚德尔卡门贵？",
   "四个具体原因：门禁管控与工人登记、限制施工时段拉长工期、社区内部更长的材料搬运，以及运河和近海地块所需的海洋级规格。"),
  ("哪些费用不在施工预算里？",
   "该地块的 HOA 维护费、码头泊位费（如适用）、护岸老化时的修复费用，以及设计委员会的提交与保证金，约 $60,000&ndash;$250,000 比索。码头工程与住宅分开报批。"),
  ("除了市政许可，还需要社区批准吗？",
   "需要，而且实务上社区在前。施工许可和 DRO 在索利达里达德办理，社区建筑委员会则审查高度、退线、材料、色彩和围墙。请在方案阶段提交 &mdash; 计划外的审查轮次是这里最常见的延误。"),
  ("运河地块有什么不同？",
   "基坑和泳池需要降水与抗浮设计、因持续盐雾需全套海洋级规格、面水立面需抗冲击玻璃以应对风暴暴露，任何水际构筑物还需单独审批。"),
 ],
}

Z[("zh","akumal")] = {
 "title": "2026年阿库马尔建房成本：环评文件决定总价",
 "desc": "2026年阿库马尔建房造价，以及为什么决定总价的是环评与许可文件而不是墙体。海龟规定、污水处理站、运输与审批日程。",
 "lead": "2026年在<strong>阿库马尔</strong>建一栋150平米住宅，交钥匙约需 <strong>$2.85M&ndash;$3.52M 比索（$158k&ndash;$196k 美元）</strong>。但在阿库马尔的地块上，施工是预算中可预期的那一半：真正把两个看似相同的项目拉开差距的，是环评文件、污水处理站和审批日程。",
 "sections": [
  ("按住宅面积的交钥匙造价",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>住宅面积</th><th>交钥匙（比索）</th><th>交钥匙（美元）</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.90M&ndash;$2.35M</td><td>$106k&ndash;$131k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.85M&ndash;$3.52M</td><td>$158k&ndash;$196k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.80M&ndash;$4.70M</td><td>$211k&ndash;$261k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.75M&ndash;$5.88M</td><td>$264k&ndash;$326k</td></tr>
</tbody></table></div>
<p class="text-muted small">参考：标准装修 $19,000&ndash;$23,500 比索/平米。美元/比索 &asymp; 18。不含土地、泳池和家具。</p>
<p>这大约比普拉亚德尔卡门高12%，来源是所有材料沿走廊的运输、应对盐蚀的海洋级规格，以及本地工种基础较薄、部分班组需要外调。</p>"""),
  ("只有阿库马尔才有的预算项",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>项目</th><th>比索</th><th>原因</th></tr></thead><tbody>
<tr><td>环境研究与批复</td><td>$80,000&ndash;$350,000</td><td>范围由植被和离岸距离决定，与住宅面积无关</td></tr>
<tr><td>污水处理站 + 渗井</td><td>$120,000&ndash;$380,000</td><td>没有市政污水管网；先处理后渗透是文件的核心</td></tr>
<tr><td>符合海龟规定的照明</td><td>$30,000&ndash;$120,000</td><td>低位、带遮罩、朝海立面用琥珀或红色光源</td></tr>
<tr><td>ZOFEMAT 测绘与特许核查</td><td>$20,000&ndash;$80,000</td><td>仅适用于触及联邦海域区的地块</td></tr>
<tr><td>建筑轮廓范围的地质勘察</td><td>$25,000&ndash;$60,000</td><td>喀斯特：良好持力层两米外可能就是溶洞</td></tr>
</tbody></table></div>
<p>五项中有四项随<em>地块</em>变化，而不随住宅面积变化。这正是阿库马尔的小房子单方造价高于大房子的原因，也是这里最省钱的做法为何是挑一块已有环评批复、管线已到红线的地。</p>"""),
  ("审批日程与等待的代价",
   """<p>阿库马尔属于 <strong>图卢姆</strong> 市，而不是索利达里达德 &mdash; 很多业主会意外，因为普拉亚德尔卡门更近。图卢姆的环境审查是整个走廊最严格的，其实际后果就是时间：</p>
<ul>
<li><strong>环评文件：</strong>植被覆盖或近岸地块需 4&ndash;9 个月。</li>
<li><strong>文件齐全后的许可审查：</strong>4&ndash;12 周。</li>
<li><strong>从购地到动工的现实总时长：</strong>6&ndash;14 个月。</li>
</ul>
<p>这些月份是实实在在的成本：土地被占用、资金被冻结却不产生收益。这也是为什么带有效环评批复的地块能卖出溢价 &mdash; 而且通常物有所值。</p>
<p>这一段海岸还有一个专属的排程要点：海龟产卵季大致从 <strong>5月到10月</strong>，期间限制重型作业、强光照明和沙滩上的活动。请把嘈杂的室外阶段安排在这个窗口之外，把室内装修放在窗口之内。</p>
<p>施工本身150平米约需 <strong>7&ndash;10 个月</strong>。采用带分项预算的固定总价合同，并确保交付之后的环保条件 &mdash; 补种成活率、处理站运行台账、照明合规 &mdash; 有人负责，因为它们在建筑的整个生命周期内持续有效。</p>"""),
 ],
 "faq": [
  ("2026年在阿库马尔建房要多少钱？",
   "150平米标准装修交钥匙约 $2.85M&ndash;$3.52M 比索（$158k&ndash;$196k 美元）&mdash; 折合约 $19,000&ndash;$23,500 比索/平米，比普拉亚德尔卡门高约12%。土地、泳池、家具和环保相关项目另计。"),
  ("阿库马尔的地块有哪些额外费用？",
   "环境研究与批复 $80,000&ndash;$350,000、污水处理站与渗井 $120,000&ndash;$380,000、符合海龟规定的照明 $30,000&ndash;$120,000、联邦区地块的 ZOFEMAT 测绘 $20,000&ndash;$80,000，以及地质勘察 $25,000&ndash;$60,000。其中多数取决于地块而非房屋。"),
  ("阿库马尔的许可由哪个市政厅发放？",
   "图卢姆，而不是索利达里达德，尽管普拉亚德尔卡门在地理上更近。图卢姆的环境审查是走廊中最严格的，因此从购地到动工请按 6&ndash;14 个月规划。"),
  ("海龟规定会影响施工进度吗？",
   "会。产卵季大致从5月到10月，限制重型作业、强光照明和靠近海滩的沙上活动。嘈杂的室外阶段安排在季节之外，室内工程放在季节之内。照明规定对建成后的房屋同样有效。"),
  ("在阿库马尔，小房子单方更便宜吗？",
   "不，单方更贵。环评文件、地质勘察、污水处理站和管线接入对80平米和200平米的花费几乎相同，因此在小房子上这些固定项目占比大得多。"),
 ],
}

Z[("zh","puerto-morelos")] = {
 "title": "2026年普埃尔托莫雷洛斯建房成本：性价比之选",
 "desc": "普埃尔托莫雷洛斯以普拉亚德尔卡门的造价、更便宜的地价建房。2026年区间、珊瑚礁公园对排放的要求，以及天坑之路地块。",
 "lead": "2026年在<strong>普埃尔托莫雷洛斯</strong>建一栋150平米住宅，交钥匙约需 <strong>$2.55M&ndash;$3.15M 比索（$142k&ndash;$175k 美元）</strong> &mdash; 施工造价基本与普拉亚德尔卡门持平，而地价通常更低。正是这个组合，使它成为走廊上低调的性价比之选。",
 "sections": [
  ("交钥匙造价与三个细分市场",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>住宅面积</th><th>交钥匙（比索）</th><th>交钥匙（美元）</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.70M&ndash;$2.10M</td><td>$94k&ndash;$117k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.55M&ndash;$3.15M</td><td>$142k&ndash;$175k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.40M&ndash;$4.20M</td><td>$189k&ndash;$233k</td></tr>
<tr><td>250 m&sup2;</td><td>$4.25M&ndash;$5.25M</td><td>$236k&ndash;$292k</td></tr>
</tbody></table></div>
<p class="text-muted small">参考：标准装修 $17,000&ndash;$21,000 比索/平米。美元/比索 &asymp; 18。不含土地、泳池和家具。</p>
<ul>
<li><strong>海边与近岸：</strong>$26,000&ndash;$38,000+ 比索/平米，需海洋级规格与更重的环评文件。</li>
<li><strong>天坑之路（Ruta de los Cenotes）：</strong>已通管线地块 $14,000&ndash;$19,000，离网建设 $17,000&ndash;$24,000 &mdash; 地价更低，但基础设施更多。</li>
</ul>"""),
  ("2016年起自成一个市",
   """<p>普埃尔托莫雷洛斯于2016年从贝尼托华雷斯分出，如今自行发放土地用途、施工许可、红线和竣工验收。三个实际影响：</p>
<ul>
<li><strong>在这里报批，而不是坎昆。</strong>基于贝尼托华雷斯做法的建议已经过时，2016年以前邻居的经验同样过时。</li>
<li><strong>按当前口径核实地块参数。</strong>该市的规划文件相对年轻且经过修订：请就具体地块确认密度、高度和允许用途，而不是沿用旧文件。</li>
<li><strong>小机构意味着直接沟通。</strong>审批人员可以接触到，因此一份完整的报批材料格外有效，而一份不完整的会格外拖沓。</li>
</ul>
<p>州级环评（SEMA）、适用时的联邦管辖、涉水事务的 CONAGUA，以及海滩一侧的 ZOFEMAT，与走廊其他地方一致。</p>"""),
  ("珊瑚礁与湿地给规格增加了什么",
   """<ul>
<li><strong>排放水质是文件的核心。</strong>先处理后渗透，规模匹配实际入住人数，泳池反冲洗水单独排放 &mdash; 视入住规模 $90,000&ndash;$350,000 比索。这里渗入地下的水会到达含水层，再到达珊瑚礁。</li>
<li><strong>红树林没有商量余地。</strong>湿地相邻地块必须在画出建筑轮廓之前确定受保护植被的边界 &mdash; 部分在售地块的可建面积远小于产权面积。</li>
<li><strong>天坑退距</strong>适用于内陆，并对附近可渗透的内容加以限制。</li>
<li><strong>室内地坪标高</strong>在湿地或海岸附近的低洼地块，要按洪水与风暴潮设定。这是设计阶段的决定，事后无法更正。</li>
<li><strong>在天坑之路，</strong>请预留进场道路（$40,000&ndash;$300,000），并在 CFE 线路延伸（购地前先询价，$150,000 至超过 $900,000）与包含光伏、储能、处理后水井和雨水收集的离网系统之间做出选择。</li>
</ul>
<p>150平米住宅的施工期约为 <strong>7&ndash;10 个月</strong>。</p>"""),
 ],
 "faq": [
  ("在普埃尔托莫雷洛斯建房要多少钱？",
   "镇上或内陆地块，150平米交钥匙约 $2.55M&ndash;$3.15M 比索（$142k&ndash;$175k 美元）&mdash; 折合约 $17,000&ndash;$21,000 比索/平米，基本与普拉亚德尔卡门持平。海边为 $26,000&ndash;$38,000+，天坑之路视管线情况为 $14,000&ndash;$24,000。"),
  ("哪个市政厅发放许可？",
   "普埃尔托莫雷洛斯自己：它于2016年从贝尼托华雷斯（坎昆）分出。任何基于坎昆做法的说法都已过时，而且由于规划文件较新，密度、高度和用途都应按当前口径核实。"),
  ("可以在红树林旁边建房吗？",
   "不能在受保护植被范围内，且其边界必须在画出建筑轮廓之前确定。部分在售地块的可建面积明显小于产权面积，应在购地前核实。"),
  ("珊瑚礁国家公园对我的工程意味着什么？",
   "意味着排放水质成为环评文件的核心技术问题。按实际入住规模设计的处理系统、泳池反冲洗水单独排放，费用 $90,000&ndash;$350,000 比索，并会被仔细审查。"),
  ("在天坑之路建房更便宜吗？",
   "地价更便宜，已通管线地块的施工约 $14,000&ndash;$19,000 比索/平米。但许多地块既无 CFE 也无市政供水：请预留线路延伸费用（购地前询价，$150,000 至超过 $900,000）或离网系统，另加 $40,000&ndash;$300,000 的进场道路。"),
 ],
}

Z[("zh","playacar")] = {
 "title": "2026年普拉亚卡尔建房成本：拆建还是翻新",
 "desc": "普拉亚卡尔已基本建满，多数项目是翻新或拆除重建。2026年价格区间、拆除费用、设计委员会，以及一期与二期的差别。",
 "lead": "2026年在<strong>普拉亚卡尔</strong>建一栋150平米住宅，交钥匙约需 <strong>$3.15M&ndash;$3.90M 比索（$175k&ndash;$217k 美元）</strong>，比普拉亚德尔卡门基准高约25%。但普拉亚卡尔实际上已经建满，真正的问题不是新房造价，而是把地块上的旧房翻新还是拆掉。",
 "sections": [
  ("翻新还是拆除：算一笔账",
   """<p>普拉亚卡尔几乎每个项目都是拆除重建、大规模翻新，或在少数剩余地块上新建。前两者之间的选择应当在结构检测之后做出，而不是看过房子就决定：这个年代的房子在这段海岸带有一个可预期的缺陷 &mdash; 板边、阳台、柱和女儿墙的氯离子引起的钢筋锈蚀。</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>项目</th><th>比索</th></tr></thead><tbody>
<tr><td>含代表性部位开凿的结构检测</td><td>$40,000&ndash;$150,000</td></tr>
<tr><td>拆除与清运，典型住宅</td><td>$180,000&ndash;$600,000</td></tr>
<tr><td>保留时的混凝土修复方案</td><td>检测后报价 &mdash; 可能超过拆除费用</td></tr>
<tr><td>整体翻新，高端装修</td><td>$14,000&ndash;$26,000 比索/平米</td></tr>
<tr><td>新建，高端</td><td>$24,000&ndash;$30,000 比索/平米</td></tr>
<tr><td>新建，豪华</td><td>$30,000&ndash;$42,000 比索/平米</td></tr>
</tbody></table></div>
<p>诚实的临界点：当结构修复接近重建造价的 25&ndash;30% 时，您是在用新建的钱买一栋旧建筑的层高、朝向和平面。不过在普拉亚卡尔确有相反的理由 &mdash; 地块不可复制，成熟树木受保护且有价值，二期一栋层高慷慨、结构扎实的九十年代住宅，往往值得保留。</p>"""),
  ("按住宅面积的交钥匙造价",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>住宅面积</th><th>交钥匙（比索）</th><th>交钥匙（美元）</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.10M&ndash;$2.60M</td><td>$117k&ndash;$144k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.15M&ndash;$3.90M</td><td>$175k&ndash;$217k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.20M&ndash;$5.20M</td><td>$233k&ndash;$289k</td></tr>
<tr><td>250 m&sup2;</td><td>$5.25M&ndash;$6.50M</td><td>$292k&ndash;$361k</td></tr>
</tbody></table></div>
<p class="text-muted small">参考：标准至高端装修 $21,000&ndash;$26,000 比索/平米。美元/比索 &asymp; 18。不含土地、泳池和家具。</p>
<p>高出基准的这25%，来自狭窄街道带来的通行限制、工人登记与作业时段限制、设计委员会流程、树木保护、海洋级规格，以及当地市场预期的装修水准。若是普拉亚卡尔的海边地块，还要加上联邦海域区问题和朝海立面的抗冲击玻璃：那里是 $42,000&ndash;$60,000+ 比索/平米。</p>"""),
  ("委员会、树木与一期二期之别",
   """<p><strong>建筑审查是实打实的</strong>，普拉亚卡尔的工期也多半在这里被拖延。预计会审查：超出市政最低要求的高度、体量与退线，屋面形式与材料，立面处理与色彩，围墙与栅栏，尤其是树木砍伐 &mdash; 成熟树冠是社区所保护的内容之一，每一棵都要论证。请在方案阶段连同树木清查一并提交，并在工期中留出至少一轮审查以及保证金。</p>
<p><strong>一期和二期是两个不同的地方。</strong>一期更靠近市区和渡口：密度更高、地块更小，步行到第五大道确实可行，施工通行需经狭窄街道因而更贵。二期更大也更安静，围绕高尔夫球场展开，地块宽裕、植被成熟，有条件建造较大的别墅 &mdash; 而球场临界会让玻璃和天窗的选型成为一个现实问题。</p>
<p>许可在 <strong>索利达里达德</strong> 办理；150平米的施工期约 <strong>7&ndash;10 个月</strong>，如需拆除另计。</p>"""),
 ],
 "faq": [
  ("在普拉亚卡尔建房要多少钱？",
   "150平米交钥匙约 $3.15M&ndash;$3.90M 比索（$175k&ndash;$217k 美元）&mdash; 折合约 $21,000&ndash;$26,000 比索/平米，比普拉亚德尔卡门基准高约25%。豪华装修 $30,000&ndash;$42,000，海边地块 $42,000&ndash;$60,000+。"),
  ("应该翻新旧房还是拆掉重建？",
   "先做含代表性部位开凿的结构检测，$40,000&ndash;$150,000 比索，因为这个年代的房子常有氯离子引起的钢筋锈蚀。当结构修复接近重建造价的 25&ndash;30% 时，通常拆除更合理；拆除与清运费用为 $180,000&ndash;$600,000。"),
  ("普拉亚卡尔的设计委员会审查什么？",
   "超出市政最低要求的高度、体量与退线，屋面形式与材料，立面与色彩，围墙与栅栏，以及需要逐棵论证的树木砍伐。它同时规定施工规则：工人登记、作业时段、送货、材料堆放和保证金。"),
  ("一期和二期在施工上有何不同？",
   "一期地块更小更密，施工通行经狭窄街道因而更贵，但步行到第五大道确实可行。二期是高尔夫球场旁的大地块，植被成熟 &mdash; 球场临界让玻璃与天窗选型成为现实问题。"),
  ("为什么普拉亚卡尔比其他区域贵25%？",
   "狭窄街道的通行限制、工人登记与作业时段限制、委员会流程、施工期间的树木保护、海洋级规格，以及当地市场预期的装修水准 &mdash; 每一项都是真实成本，而非地址溢价。"),
 ],
}

Z[("zh","mayakoba")] = {
 "title": "2026年玛雅科巴建房成本：走廊的价格上限",
 "desc": "玛雅科巴是里维埃拉玛雅最贵的建房地点。2026年每平米区间、度假村级规格到底包含什么，以及为什么是这个价。",
 "lead": "2026年在<strong>玛雅科巴</strong>建一栋150平米住宅，交钥匙约需 <strong>$3.60M&ndash;$4.50M 比索（$200k&ndash;$250k 美元）</strong> &mdash; 整个走廊最高的区间，比普拉亚德尔卡门基准高约42%。不过这里几乎没有人按区间下限建房，本页说明原因。",
 "sections": [
  ("按面积的造价与现实数字",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>住宅面积</th><th>交钥匙（比索）</th><th>交钥匙（美元）</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.60M&ndash;$4.50M</td><td>$200k&ndash;$250k</td></tr>
<tr><td>250 m&sup2;</td><td>$6M&ndash;$7.50M</td><td>$333k&ndash;$417k</td></tr>
<tr><td>350 m&sup2;</td><td>$8.40M&ndash;$10.50M</td><td>$467k&ndash;$583k</td></tr>
<tr><td>500 m&sup2;</td><td>$12M&ndash;$15M</td><td>$667k&ndash;$833k</td></tr>
</tbody></table></div>
<p class="text-muted small">参考：标准至高端装修 $24,000&ndash;$30,000 比索/平米。美元/比索 &asymp; 18。不含土地、泳池和家具。</p>
<p>以上是入门区间。总体规划区内真正建成的房子多为 300&ndash;600 平米的作者级作品，计入建筑师主导的设计、进口五金洁具、全屋自动化、定制泳池和成熟园林后，实际数字落在 <strong>$35,000&ndash;$55,000 比索/平米</strong>。用 $24,000 去预算一栋玛雅科巴别墅，等于在预算一栋通不过设计审查的房子。</p>"""),
  ("这笔溢价究竟买到什么",
   """<ul>
<li><strong>设计管控。</strong>一个围绕度假村运营构建的总体规划，会以相邻酒店的标准审查建筑、材料、色彩、景观与照明。提交要求详尽，审查周期真实存在，而在立面上做减法根本不是可选项。</li>
<li><strong>装修预期。</strong>这里的对标物是品牌住宅。木作、石材、玻璃与五金按此标准选型，而精准安装的人工成本高于材料本身。</li>
<li><strong>现场纪律。</strong>施工发生在一个正在运营的奢华环境中：门禁管控、工人登记、时段限制、遮挡围挡、噪音限值、清洁义务和保证金。每一项都消耗工期。</li>
<li><strong>自然环境。</strong>总体规划围绕潟湖、水道与红树林组织。保留植被、退距、排水和排放除受主管部门约束外，还在社区层面统一管理。</li>
<li><strong>海洋与防潮规格</strong>全屋贯彻：316 不锈钢、阳极氧化或海洋级涂层铝材、加大保护层、通风柜体。</li>
<li><strong>稀缺性。</strong>住宅地块很少，每个项目都是孤例 &mdash; 没有可摊薄设计与管理成本的重复量。</li>
</ul>"""),
  ("工期、许可与另需预算的项目",
   """<p>许可通过 <strong>索利达里达德</strong> 市政厅办理，社区建筑审查排在其前，而环境审查会认真对待潟湖与红树林。请在方案阶段就向社区提交：先把设计做完再送审，在这里等于损失一个季度。</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>施工之外</th><th>比索</th></tr></thead><tbody>
<tr><td>此级别的建筑师主导设计与工程</td><td>施工造价的 10&ndash;15%</td></tr>
<tr><td>社区提交、审查周期与施工保证金</td><td>$150,000&ndash;$600,000</td></tr>
<tr><td>定制泳池含设备</td><td>$900,000&ndash;$3,500,000</td></tr>
<tr><td>成熟园林与灌溉</td><td>$400,000&ndash;$2,000,000</td></tr>
<tr><td>此级别别墅的家具与设备</td><td>$1,500,000&ndash;$6,000,000</td></tr>
<tr><td>社区费用</td><td>持续性 &mdash; 按地块核实</td></tr>
</tbody></table></div>
<p>此规格别墅的施工期约 <strong>10&ndash;16 个月</strong>，长于走廊常态 &mdash; 时段限制、审查周期和装修精度都需要时间。</p>"""),
 ],
 "faq": [
  ("在玛雅科巴建房要多少钱？",
   "入门区间为 $24,000&ndash;$30,000 比索/平米，即150平米约 $3.60M&ndash;$4.50M 比索（$200k&ndash;$250k 美元）。实际建成的多为 300&ndash;600 平米、$35,000&ndash;$55,000 比索/平米的项目，含作者级设计、进口装修、自动化、泳池与成熟园林。"),
  ("为什么玛雅科巴是走廊最贵的？",
   "度假村标准的设计管控、对标品牌住宅的装修预期、在运营中的奢华环境内施工的纪律成本、围绕潟湖与红树林的环境管理、全屋海洋级规格，以及没有重复量可摊薄成本的稀缺性。"),
  ("除了施工还要预算什么？",
   "设计与工程为施工造价的 10&ndash;15%、社区提交与保证金 $150,000&ndash;$600,000、定制泳池 $900,000&ndash;$3,500,000、成熟园林 $400,000&ndash;$2,000,000、家具设备 $1,500,000&ndash;$6,000,000，以及持续性的社区费用。"),
  ("玛雅科巴的别墅要建多久？",
   "此规格约 10&ndash;16 个月，长于走廊常态。作业时段限制、社区审查周期和所要求的装修精度都会额外占用时间。"),
  ("谁来批准设计？",
   "索利达里达德市政厅负责土地用途、许可、红线和 DRO；社区建筑审查在实务上排在前面，审查建筑、材料、色彩、景观与照明。"),
 ],
}

Z[("zh","corasol")] = {
 "title": "2026年科拉索尔建房成本：在建设中的总体规划里施工",
 "desc": "2026年科拉索尔建房造价，以及在一个仍在开发的总体规划社区内施工意味着什么：分期市政配套、设计委员会、高尔夫临界与通行规则。",
 "lead": "2026年在<strong>科拉索尔</strong>建一栋150平米住宅，交钥匙约需 <strong>$3.30M&ndash;$4.12M 比索（$183k&ndash;$229k 美元）</strong>，比普拉亚德尔卡门基准高约30%。我们的办公室也在科拉索尔，这篇内容是在距离主题步行几分钟的地方写成的。",
 "sections": [
  ("按住宅面积的交钥匙造价",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>住宅面积</th><th>交钥匙（比索）</th><th>交钥匙（美元）</th></tr></thead><tbody>
<tr><td>150 m&sup2;</td><td>$3.30M&ndash;$4.12M</td><td>$183k&ndash;$229k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.40M&ndash;$5.50M</td><td>$244k&ndash;$306k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.60M&ndash;$8.25M</td><td>$367k&ndash;$458k</td></tr>
<tr><td>450 m&sup2;</td><td>$9.90M&ndash;$12.38M</td><td>$550k&ndash;$688k</td></tr>
</tbody></table></div>
<p class="text-muted small">参考：标准至高端装修 $22,000&ndash;$27,500 比索/平米。美元/比索 &asymp; 18。不含土地、泳池和家具。</p>
<p>这里建成的多数超过150平米：地块条件和市场都推向 250&ndash;450 平米、带泳池、屋顶露台和成品园林的别墅。请按整包预算而不只看单方价：在一栋300平米别墅上，泳池、园林、家具和设计费通常还要在施工造价之上再加 35&ndash;50%。</p>"""),
  ("在一个自身仍在建设的社区里施工",
   """<ul>
<li><strong>市政配套分期到位。</strong>请就您的地块确认今天红线处实际具备什么 &mdash; 电力容量、供水、排水、路面 &mdash; 以及哪些只是规划中的。"社区将会有"和"地块现在有"之间的差距，正是预算波动之处。</li>
<li><strong>邻居也在施工。</strong>其他住宅和社区工程会持续数年：您入住期间有噪音和运输车流，您施工期间则要共用通道。</li>
<li><strong>设计审查活跃且在演进。</strong>委员会审查高度、体量、材料、色彩、围墙和景观，目的是在一个尚未完工的社区中维持统一的面貌。请在方案阶段提交。</li>
<li><strong>通行与施工规则。</strong>工人登记、门禁进入、固定送货时段、地块堆放限制、道路清洁义务和保证金。提交、保证金与通行管理合计预留 $80,000&ndash;$300,000 比索。</li>
<li><strong>高尔夫临界</strong>带来玻璃与天窗的选型问题 &mdash; 失控球是真实且可量化的风险 &mdash; 以及与球场的灌溉排水衔接。</li>
</ul>"""),
  ("场地条件、许可与工期",
   """<p>科拉索尔属于 <strong>索利达里达德</strong> 市：土地用途证明、红线、施工许可和责任建筑师（DRO），社区建筑审查实务上排在前面。环境要求与这段海岸其他地方一致，喀斯特地层要求覆盖实际建筑轮廓的钻孔勘察 &mdash; 良好承载力与两米外的溶洞在这里同样正常。</p>
<ul>
<li><strong>海洋级规格依然适用。</strong>科拉索尔离海足够近，316 不锈钢、阳极氧化或海洋级涂层铝材和加大的混凝土保护层是正确做法，而非可选升级。</li>
<li><strong>如果高度允许，从一开始就把屋面设计成露台。</strong>在能看到球场或海景的地块上，那是全屋最有价值的一平米，事后改造要多花数倍。</li>
<li><strong>认真规划设备空间：</strong>蓄水池、增压系统、针对本地水质硬度的水处理、泳池设备与空调机位，全部要留出检修通道。</li>
</ul>
<p>250&ndash;300 平米别墅的施工期约 <strong>8&ndash;12 个月</strong>，若设计审查超过一轮还会更久。如果现在买地、以后再建，请在成交前取得红线处配套状况的书面确认。</p>"""),
 ],
 "faq": [
  ("在科拉索尔建房要多少钱？",
   "150平米交钥匙约 $3.30M&ndash;$4.12M 比索（$183k&ndash;$229k 美元）&mdash; 折合约 $22,000&ndash;$27,500 比索/平米，比普拉亚德尔卡门基准高约30%。这里多数住宅为 250&ndash;450 平米，泳池、园林、家具与设计费还要再加 35&ndash;50%。"),
  ("在科拉索尔买地前应该核实什么？",
   "该地块红线处今天实际具备哪些配套 &mdash; 电力容量、供水、排水、路面 &mdash; 与仅在规划中的部分之间的差别。在仍在建设的总体规划社区里，预算风险恰恰藏在这个差距里。"),
  ("设计委员会会增加成本和时间吗？",
   "两者都会。提交、施工保证金与通行管理预留 $80,000&ndash;$300,000 比索，工期中至少留出一轮审查，此外还有工人登记、门禁、送货时段和道路清洁。"),
  ("高尔夫临界会改变什么？",
   "玻璃与天窗的选型，因为失控球是真实且可量化的风险；还有与球场的灌溉排水衔接。这些应在设计阶段解决，而不是事后更换玻璃。"),
  ("科拉索尔的别墅要建多久？",
   "250&ndash;300 平米从许可到交付约 8&ndash;12 个月，设计审查超过一轮则更久。作业时段限制和门禁管控会把工期推向上限。"),
 ],
}

Z[("zh","aldea-zama")] = {
 "title": "2026年阿尔迪亚萨马建房成本：日历也是成本",
 "desc": "2026年阿尔迪亚萨马造价，以及几乎没人预算的一项：图卢姆的审批日程。高度限制、供电可靠性和已完成市政配套的总体规划。",
 "lead": "2026年在<strong>阿尔迪亚萨马</strong>建一栋150平米住宅，交钥匙约需 <strong>$3.08M&ndash;$3.75M 比索（$171k&ndash;$208k 美元）</strong>，比普拉亚德尔卡门基准高约20%。施工数字本身很直接。在图卢姆很少有人预算的，是时间。",
 "sections": [
  ("按住宅面积的交钥匙造价",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>住宅面积</th><th>交钥匙（比索）</th><th>交钥匙（美元）</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$2.05M&ndash;$2.50M</td><td>$114k&ndash;$139k</td></tr>
<tr><td>150 m&sup2;</td><td>$3.08M&ndash;$3.75M</td><td>$171k&ndash;$208k</td></tr>
<tr><td>200 m&sup2;</td><td>$4.10M&ndash;$5M</td><td>$228k&ndash;$278k</td></tr>
<tr><td>300 m&sup2;</td><td>$6.15M&ndash;$7.50M</td><td>$342k&ndash;$417k</td></tr>
</tbody></table></div>
<p class="text-muted small">参考：标准至高端装修 $20,500&ndash;$25,000 比索/平米。美元/比索 &asymp; 18。不含土地、泳池和家具。</p>
<p>阿尔迪亚萨马高于图卢姆各 Regi&oacute;n 和拉维莱塔，原因很简单：这是一个已完成市政配套的总体规划区，管线入地、道路铺装、风貌确定，且步行或骑行即可到达海滨路。您买的是已经存在的基础设施，而不是还需要自己建设的基础设施。</p>"""),
  ("审批日程真正的代价",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>阶段</th><th>时长</th></tr></thead><tbody>
<tr><td>土地用途证明与红线</td><td>2&ndash;8 周</td></tr>
<tr><td>地质勘察（并行）</td><td>2&ndash;5 周</td></tr>
<tr><td>环评文件</td><td>视植被 3&ndash;8 个月</td></tr>
<tr><td>技术图纸（并行）</td><td>6&ndash;14 周</td></tr>
<tr><td>文件齐全后的许可审查</td><td>4&ndash;12 周</td></tr>
<tr><td><strong>动工前总计</strong></td><td><strong>5&ndash;12 个月</strong></td></tr>
</tbody></table></div>
<p>这些月份是实实在在的成本：土地被占用、资金被冻结、没有任何收益。缩短它的办法有两个。其一，在建筑方案仍处于草图阶段就启动环评和地质勘察 &mdash; 二者都不需要最终图纸，而且本来就会反过来约束设计。其二，比较地块时高度重视已有的环评批复：它可能价值半年时间和一笔六位数金额。</p>"""),
  ("高度、供电与这里建什么",
   """<ul>
<li><strong>高度限制严格</strong>且会被执行。图卢姆的规定刻意比普拉亚德尔卡门更紧，因此在设计屋顶露台之前请核实您地块的具体数值 &mdash; 在许多地块上，一个项目出彩与否就取决于这一个数字。</li>
<li><strong>供电可靠性不如普拉亚德尔卡门。</strong>请把全屋浪涌保护列为标配；出租型物业还应配置覆盖基本用电的储能系统 &mdash; 网络、泳池控制器、部分照明和一台风扇 &mdash; 费用 $140,000&ndash;$330,000 比索。当泳池泵和多台空调把用电推到 DAC 高耗电费率时，光伏在这里尤其划算。</li>
<li><strong>市场以公寓为主，</strong>而这恰恰是建独栋的理由。独栋住宅的短租权不会被业主大会投票取消，不必从租金毛收入中缴纳社区费，并且可以为收益而设计：每间卧室带独立卫浴、可独立出租的 casita、屋顶露台，以及为照片取景而布置的泳池。</li>
</ul>
<p>技术上图卢姆的常规要点同样适用：按入住规模设计的先处理后渗透系统（$90,000&ndash;$250,000 比索）、针对水质硬度的水处理、白蚁与防潮构造，以及因喀斯特天坑密布而必需的地质勘察。150&ndash;200 平米的施工期约 <strong>7&ndash;11 个月</strong>。</p>"""),
 ],
 "faq": [
  ("在阿尔迪亚萨马建房要多少钱？",
   "150平米标准至高端装修交钥匙约 $3.08M&ndash;$3.75M 比索（$171k&ndash;$208k 美元）&mdash; 折合约 $20,500&ndash;$25,000 比索/平米，比普拉亚德尔卡门基准高约20%。"),
  ("为什么比图卢姆的 Región 地块贵？",
   "因为基础设施已经存在：管线入地、道路铺装、风貌确定的总体规划区，且靠近海滨路。在更便宜的 Regi&oacute;n 地块上，配套、进场道路和环境是您日后自己出钱建设的。"),
  ("在图卢姆多久才能动工？",
   "从购地起现实为五到十二个月：土地用途与红线 2&ndash;8 周，植被地块的环评 3&ndash;8 个月，许可审查 4&ndash;12 周。请在建筑方案仍是草图时就启动环评和地质勘察。"),
  ("阿尔迪亚萨马可以做屋顶露台吗？",
   "取决于您地块的高度限制，而图卢姆的限制刻意严格且会被执行。请在设计前核实这个数值：在许多地块上，它决定了方案是出彩还是妥协。"),
  ("图卢姆停电怎么办？",
   "全屋浪涌保护作为标配；出租物业另配覆盖网络、泳池控制器、照明和风扇的储能系统，$140,000&ndash;$330,000 比索。光伏回本也快，尤其是在 DAC 费率下。"),
 ],
}

Z[("zh","playa-del-carmen")] = {
 "title": "2026年普拉亚德尔卡门建房成本：分阶段预算",
 "desc": "整个走廊的基准价格。150平米住宅的分阶段预算、单方价包含与不包含的内容、附加项目，以及如何守住预算。",
 "lead": "2026年在<strong>普拉亚德尔卡门</strong>建一栋扎实的150平米家庭住宅，交钥匙约需 <strong>$2.6M&ndash;$3.2M 比索（$145,000&ndash;$178,000 美元）</strong>。整个走廊的价格都以这个数字为参照，因此值得按阶段拆开理解，而不是当成一个总数。",
 "sections": [
  ("分阶段预算（150平米标准住宅）",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>阶段</th><th>占比</th><th>费用（比索）</th><th>内容</th></tr></thead><tbody>
<tr><td>许可、DRO 与勘察</td><td>5%</td><td>$130,000&ndash;$160,000</td><td>施工许可、DRO、地质勘察、测绘</td></tr>
<tr><td>基础与结构</td><td>30%</td><td>$780,000&ndash;$960,000</td><td>底板、柱、梁、楼板</td></tr>
<tr><td>墙体与屋面</td><td>18%</td><td>$470,000&ndash;$580,000</td><td>砌块、构造柱、屋面板</td></tr>
<tr><td>机电安装</td><td>15%</td><td>$390,000&ndash;$480,000</td><td>电气、给水、排水</td></tr>
<tr><td>装修</td><td>25%</td><td>$650,000&ndash;$800,000</td><td>地面、涂装、chukum、木作</td></tr>
<tr><td>清理与交付</td><td>7%</td><td>$180,000&ndash;$220,000</td><td>收尾细节、交房</td></tr>
</tbody></table></div>
<p class="text-muted small">交钥匙合计 &asymp; $2.6M&ndash;$3.2M 比索。不含土地、泳池和家具。</p>
<p>从这张表可以读出两点。结构接近预算的三分之一，也是在强风区唯一一个省钱真正危险的阶段。而占25%的装修，才是您的规格真正落地的地方 &mdash; 同一套主体结构换一套装修，总价可以相差20%，而图纸一张都不用改。</p>"""),
  ("单方价包含与不包含什么",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>项目</th><th>比索</th></tr></thead><tbody>
<tr><td>土地</td><td>单独计算，也是普拉亚德尔卡门最大的变量</td></tr>
<tr><td>4&times;8 米泳池含设备</td><td>$450,000&ndash;$1,200,000</td></tr>
<tr><td>屋顶露台做法（结构已预留）</td><td>每平米 $3,500&ndash;$9,000</td></tr>
<tr><td>水处理（过滤、软化、活性炭、反渗透）</td><td>$35,000&ndash;$95,000</td></tr>
<tr><td>空调，4&ndash;5 个变频分区</td><td>$120,000&ndash;$280,000</td></tr>
<tr><td>光伏，5&ndash;8 kWp</td><td>$115,000&ndash;$250,000</td></tr>
<tr><td>园林与灌溉</td><td>每平米 $500&ndash;$2,000</td></tr>
<tr><td>家具与电器</td><td>家庭住宅 $450,000&ndash;$1,200,000</td></tr>
</tbody></table></div>
<p>在定制住宅上，设计、工程、勘察与许可合计通常占施工造价的 8&ndash;14% &mdash; 上表中已部分体现。这一项不宜压缩：它所避免的每一个错误，代价都高于整个服务包。</p>"""),
  ("为什么这是走廊的基准，以及如何守住预算",
   """<p>普拉亚德尔卡门低于封闭社区和高端片区，原因是结构性的而非质量性的：供应商基础深厚、施工企业真实竞争、城市地块已通管线、通过 <strong>索利达里达德</strong> 市政厅的审批路径直接，且绝大多数地块不涉及联邦海域区。走廊上其他一切都是这个数字的倍数：普埃尔托莫雷洛斯基本持平，普埃尔托阿文图拉斯约 +8%，阿库马尔 +12%，阿尔迪亚萨马 +20%，普拉亚卡尔 +25%，科拉索尔 +30%，玛雅科巴 +42%。</p>
<ul>
<li><strong>带分项预算的固定总价，</strong>而不是口头约定的单方价。一个单价乘以面积不是预算，而是重新议价的邀请。</li>
<li><strong>按经核验的实际进度付款，</strong>而不是按日期，并保留 5&ndash;10% 质保金，待缺陷清单关闭后释放。</li>
<li><strong>变更须书面并标价</strong>后再施工。口头变更是从固定价滑向开口价最常见的路径。</li>
<li><strong>明确的除外清单</strong> &mdash; 家具、电器、超出界限的园林、管线接入费 &mdash; 在签约时就约定好。</li>
</ul>
<p>150平米住宅自许可起约需 <strong>7&ndash;10 个月</strong>，之前还有两到四个月的手续期。可使用<a href="/jisuanqi/">造价计算器</a>快速估算。</p>"""),
 ],
 "faq": [
  ("2026年在普拉亚德尔卡门建房要多少钱？",
   "150平米标准装修交钥匙约 $2.6M&ndash;$3.2M 比索（$145,000&ndash;$178,000 美元）&mdash; 折合约 $17,000&ndash;$21,000 比索/平米，不含土地、泳池和家具。"),
  ("单方价里不包含什么？",
   "土地、泳池（$450,000&ndash;$1,200,000）、屋顶露台做法、水处理、空调、光伏、园林和家具。预算意外几乎都出自这里，因此从一开始就把它们列为独立项目。"),
  ("哪个阶段最贵？",
   "基础与结构约占30%，其次是占25%的装修。结构同时也是在强风区省钱危险的阶段，而装修可以在不改图纸的情况下让总价浮动20%。"),
  ("普拉亚德尔卡门与其他片区相比如何？",
   "它是基准。普埃尔托莫雷洛斯基本持平，普埃尔托阿文图拉斯 +8%，阿库马尔 +12%，阿尔迪亚萨马 +20%，普拉亚卡尔 +25%，科拉索尔 +30%，玛雅科巴 +42% &mdash; 差异来自通行限制、设计委员会、海洋级规格和环保要求，而不是施工质量。"),
  ("怎样避免预算失控？",
   "用带分项预算的固定总价代替单方包干、按经核验进度付款并保留 5&ndash;10% 质保金、变更先书面标价再施工，以及在签约时约定明确的除外清单。"),
 ],
}

Z[("zh","tulum")] = {
 "title": "2026年图卢姆建房成本：决定总价的是地块",
 "desc": "2026年图卢姆建房造价，以及为什么决定总价的是地块——管线、植被、环评文件——而不是房子本身。",
 "lead": "2026年在<strong>图卢姆</strong>建一栋150平米住宅，交钥匙约需 <strong>$2.85M&ndash;$3.60M 比索（$158k&ndash;$200k 美元）</strong>。但这里最终总价的离散度高于走廊任何地方 &mdash; 原因几乎从来不是房子，而是地块。",
 "sections": [
  ("按面积与地段的造价",
   """<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>住宅面积</th><th>交钥匙（比索）</th><th>交钥匙（美元）</th></tr></thead><tbody>
<tr><td>100 m&sup2;</td><td>$1.90M&ndash;$2.40M</td><td>$106k&ndash;$133k</td></tr>
<tr><td>150 m&sup2;</td><td>$2.85M&ndash;$3.60M</td><td>$158k&ndash;$200k</td></tr>
<tr><td>200 m&sup2;</td><td>$3.80M&ndash;$4.80M</td><td>$211k&ndash;$267k</td></tr>
<tr><td>300 m&sup2;</td><td>$5.70M&ndash;$7.20M</td><td>$317k&ndash;$400k</td></tr>
</tbody></table></div>
<p class="text-muted small">参考：标准至高端装修 $19,000&ndash;$24,000 比索/平米。美元/比索 &asymp; 18。不含土地、泳池和家具。</p>
<p>图卢姆内部的地段差异明显：各 Regi&oacute;n 和拉维莱塔位于区间下沿，阿尔迪亚萨马和 Tulum Country Club 更高，海滨路一带因海洋级规格与更重的环评文件而远高于此。</p>"""),
  ("为什么地块决定总价",
   """<p>有四项支出随地块而非住宅面积变化：</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>项目</th><th>比索</th></tr></thead><tbody>
<tr><td>环评文件（视植被）</td><td>$80,000&ndash;$300,000</td></tr>
<tr><td>污水处理站或生物消化器加渗滤场</td><td>$90,000&ndash;$250,000</td></tr>
<tr><td>已通管线街道的 CFE 接入</td><td>$10,000&ndash;$40,000</td></tr>
<tr><td>向未通电地块延伸 CFE 线路</td><td>$150,000&ndash;超过 $900,000</td></tr>
<tr><td>以离网系统替代接入（光伏、储能、水井）</td><td>$250,000&ndash;$800,000</td></tr>
<tr><td>丛林地块的进场道路与场地清理</td><td>$40,000&ndash;$300,000</td></tr>
</tbody></table></div>
<p>因此图卢姆最关键的决定是选地，而不是选装修清单。请在购地<em>之前</em>询价 CFE 线路延伸：这一个数字就能决定接入电网还是设计一套离网系统更便宜、更快。</p>"""),
  ("审批日程、供电与施工要点",
   """<p>图卢姆的环境审查是走廊中最严格的。从购地到动工现实需要 <strong>6&ndash;14 个月</strong>：土地用途证明与红线 2&ndash;8 周，植被地块的环评 4&ndash;9 个月，技术图纸并行推进，许可审查 4&ndash;12 周。请在方案阶段就启动环评和地质勘察 &mdash; 两者都不需要最终图纸，却都会影响设计。</p>
<ul>
<li><strong>高度限制严格</strong>且会被执行 &mdash; 设计屋顶露台前请核实您地块的数值。</li>
<li><strong>电网不如北面稳定：</strong>浪涌保护列为标配，出租物业另配覆盖网络、泳池控制器和基本照明的储能系统，$140,000&ndash;$330,000 比索。</li>
<li><strong>天坑与喀斯特</strong>要求钻孔勘察与渗透退距。这里渗入地下的水会到达含水层，再到达珊瑚礁。</li>
<li><strong>白蚁与潮气：</strong>杜绝木材与土壤接触、浇底板前做土壤处理、柜体通风、封闭房间除湿。</li>
</ul>
<p>纯施工期150&ndash;200平米约 <strong>7&ndash;11 个月</strong>。采用带分项预算的固定总价并按经核验进度付款 &mdash; 同时把审批日程从一开始就写进计划，而不是事后才发现。</p>"""),
 ],
 "faq": [
  ("2026年在图卢姆建房要多少钱？",
   "150平米交钥匙约 $2.85M&ndash;$3.60M 比索（$158k&ndash;$200k 美元）&mdash; 折合约 $19,000&ndash;$24,000 比索/平米。各 Regi&oacute;n 和拉维莱塔位于下沿，阿尔迪亚萨马更高，海滨路远高于此。"),
  ("为什么图卢姆的总价差别这么大？",
   "因为有四项大额支出取决于地块而非房子：环评文件 $80,000&ndash;$300,000、污水处理 $90,000&ndash;$250,000、供电从 $10,000 到超过 $900,000，以及丛林地块的进场道路 $40,000&ndash;$300,000。"),
  ("接入电网还是离网？",
   "请在购地前询价 CFE 线路延伸。如果报价落在六位数高段，那么包含光伏、储能、处理后水井和雨水收集、造价 $250,000&ndash;$800,000 的离网系统往往更便宜也更快。"),
  ("多久才能动工？",
   "从购地起现实为 6&ndash;14 个月，主要受环评文件影响，植被地块需要 4&ndash;9 个月。环评和地质勘察应在建筑方案仍是草图时就启动。"),
  ("图卢姆最重要的技术要点有哪些？",
   "先处理后渗透并保持对天坑的正确退距、因喀斯特而必需的地质勘察、因电网质量而需要的浪涌保护与必要时的储能，以及杜绝木材接触土壤的白蚁与防潮构造。"),
 ],
}

if __name__ == "__main__":
    keys = ([tuple(a.split(":", 1)) for a in sys.argv[1:]] or sorted(Z))
    for lang, zone in keys:
        if (lang, zone) not in Z:
            print(f"  ! no content for {lang}:{zone}"); continue
        w, rel = rewrite(lang, zone)
        print(f"  {w:5d} body words  {rel}")
