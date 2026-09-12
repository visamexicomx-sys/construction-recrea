#!/usr/bin/env python3
"""Replace the boilerplate body of a template-generated blog article with
topic-specific content.

generate-blogs.py builds every article in a category from the same static body
(only the title and first keyword are interpolated), so its output measured at
0.99 6-gram similarity page-to-page. This script keeps the page chrome — nav,
breadcrumb, H1, quick-summary alert, inline quote form, "We Build Across",
related service/articles, CTA, why-Recrea — and rewrites everything in between
plus the FAQPage JSON-LD from the CONTENT table below.

Usage: python3 rewrite-generated-blogs.py [slug ...]   (no args = all in CONTENT)
"""
import os, re, sys, json

BASE = os.path.dirname(os.path.abspath(__file__))

# slug -> {"intro": [<p> text...], "sections": [(h2, html)...], "faq": [(q, a)...]}
CONTENT = {}

def _esc(s):
    return re.sub(r"<[^>]+>", "", s).replace('"', "'").strip()

def rewrite(slug):
    path = os.path.join(BASE, "blog", f"{slug}.html")
    html = open(path, encoding="utf-8").read()
    c = CONTENT[slug]

    # --- keep the inline quote form verbatim (slug-parameterised conversion block)
    m = re.search(r'<div class="inline-quote-form".*?\n    </div>\n', html, re.S)
    form = m.group(0) if m else ""

    # --- body region: end of the quick-summary alert -> "We Build Across" block
    start = html.index('<div class="alert" style="background:var(--accent)')
    start = html.index("</div>", start) + len("</div>")
    end = html.index('<div class="bg-light p-4 rounded my-4">')

    body = "\n\n"
    for p in c["intro"]:
        body += f"    <p>{p}</p>\n"
    for i, (h2, inner) in enumerate(c["sections"]):
        body += f"\n    <h2>{h2}</h2>\n{inner}\n"
        if i == 1 and form:                      # form after the second section
            body += "\n" + form
    if len(c["sections"]) < 2 and form:
        body += "\n" + form
    body += "\n    <h2>Frequently Asked Questions</h2>\n"
    body += '    <div class="accordion mb-4" id="faqAcc">\n'
    for i, (q, a) in enumerate(c["faq"], 1):
        shown = " show" if i == 1 else ""
        btn = "" if i == 1 else " collapsed"
        body += (f'      <div class="accordion-item">\n'
                 f'        <h3 class="accordion-header"><button class="accordion-button{btn}" type="button" '
                 f'data-bs-toggle="collapse" data-bs-target="#faq{i}">{q}</button></h3>\n'
                 f'        <div id="faq{i}" class="accordion-collapse collapse{shown}" data-bs-parent="#faqAcc">'
                 f'<div class="accordion-body">{a}</div></div>\n'
                 f'      </div>\n')
    body += "    </div>\n\n    "
    html = html[:start] + body + html[end:]

    # --- FAQPage JSON-LD in <head> must match the visible FAQ
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": _esc(q),
         "acceptedAnswer": {"@type": "Answer", "text": _esc(a)}} for q, a in c["faq"]]}
    html = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
                  '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>',
                  html, count=1, flags=re.S)

    # --- meta title/description/read time
    if c.get("title"):
        html = re.sub(r"<title>.*?</title>", "<title>" + c["title"] + "</title>", html, count=1, flags=re.S)
        for attr in ('property="og:title"', 'name="twitter:title"'):
            html = re.sub(r"(" + re.escape(attr) + r' content=")[^"]*(")',
                          lambda m: m.group(1) + c["title"] + m.group(2), html, count=1)
    if c.get("desc"):
        for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
            html = re.sub(r"(" + re.escape(attr) + r' content=")[^"]*(")',
                          lambda m: m.group(1) + c["desc"] + m.group(2), html, count=1)
    words = len(re.findall(r"[A-Za-z0-9']+", re.sub(r"<[^>]+>", " ", body)))
    html = re.sub(r"\d+ min read", f"{max(4, round(words / 220))} min read", html, count=1)

    open(path, "w", encoding="utf-8").write(html)
    return words


CONTENT["closet-wardrobe-construction-riviera-maya"] = {
 "title": "Custom Closets in the Riviera Maya: Humidity-Proof Build Guide",
 "desc": "Why factory melamine closets fail in Playa del Carmen and Tulum, what marine plywood and 316 hardware cost per linear metre, and how to spec a walk-in.",
 "intro": [
   "A closet is the single most humidity-sensitive piece of joinery in a Riviera Maya house. It is a sealed box against an exterior or party wall, it gets no air movement, and it holds fabric — which means that in a climate that averages 80% relative humidity, a closet built the way closets are built in Guadalajara or Texas will grow mould on the back panel within two rainy seasons. The failures we are called to replace are almost never design failures. They are material and ventilation failures.",
   "This guide covers what actually survives here: substrate choices and their real cost per linear metre, the hardware grade that does not bleed rust into a white lacquer door, the ventilation detail that costs nothing at build time, and what a full walk-in in Playa del Carmen, Tulum or Puerto Aventuras should cost you in 2026."
 ],
 "sections": [
  ("What Fails First, and Why",
   """    <p>Open a five-year-old closet in a coastal house and the damage follows a predictable order. The back panel goes first — it is usually 3 mm hardboard stapled to the carcass, sitting directly against block that wicks moisture from the slab. Then the bottom shelf swells at the front edge where melamine tape has lifted. Then the hinges: 304 stainless or nickel-plated steel spots and stains the door around the cup. Rails on drawers seize last.</p>
    <p>The cause is almost always the same three decisions, made to hit a price: particleboard instead of a moisture-stable substrate, a closed carcass with no air path, and hardware chosen on catalogue price rather than corrosion grade. None of the three is expensive to fix at build time. All three are expensive to fix after installation, because the carcass has to come out.</p>
    <ul>
      <li><strong>Particleboard (aglomerado):</strong> swells irreversibly at 16&ndash;18% moisture content. In an unventilated coastal closet it gets there.</li>
      <li><strong>MDF:</strong> better machining, worse water behaviour than plywood at edges and screw points. Acceptable for doors, not for the carcass bottom.</li>
      <li><strong>Marine or phenolic-glued plywood:</strong> the substrate that holds dimension here. More expensive per sheet, cheaper per decade.</li>
      <li><strong>Solid tropical hardwood:</strong> stable if properly dried, but it moves seasonally &mdash; fine for doors and face frames, wrong for a full carcass.</li>
    </ul>"""),
  ("Substrate and Hardware Costs Per Linear Metre &mdash; 2026",
   """    <p>Closet pricing in the Riviera Maya is quoted per linear metre of run (metro lineal), at a standard 2.40 m height and 60 cm depth. The numbers below are our own installed pricing for Playa del Carmen; add roughly 8&ndash;12% for Tulum and Puerto Aventuras on transport and site access, and 15&ndash;20% for island jobs.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Build spec</th><th>MXN / linear metre</th><th>USD / linear metre</th><th>Expected coastal life</th></tr></thead>
      <tbody>
        <tr><td>Melamine on particleboard, nickel hardware</td><td>$4,500&ndash;$7,000</td><td>$250&ndash;$390</td><td>3&ndash;6 years</td></tr>
        <tr><td>Melamine on moisture-resistant MDF, 304 hardware</td><td>$7,000&ndash;$11,000</td><td>$390&ndash;$610</td><td>7&ndash;12 years</td></tr>
        <tr><td>Marine plywood carcass, lacquered doors, 316 hardware</td><td>$11,000&ndash;$17,000</td><td>$610&ndash;$945</td><td>15&ndash;25 years</td></tr>
        <tr><td>Marine plywood + solid tzalam or parota fronts, soft-close</td><td>$16,000&ndash;$26,000</td><td>$890&ndash;$1,445</td><td>20&ndash;30 years</td></tr>
      </tbody>
    </table>
    </div>
    <p>A 3.5 m reach-in for a guest bedroom therefore lands between $38,000 and $60,000 MXN in the spec we recommend. A 12&ndash;16 linear metre primary walk-in with an island runs $175,000&ndash;$400,000 MXN depending on fronts and whether it carries integrated lighting and a dressing bench.</p>
    <div class="alert alert-warning"><i class="bi bi-exclamation-triangle me-2"></i><strong>The hardware line is where quotes lie.</strong> "Acero inoxidable" on a quote means nothing on its own. 304 stainless pits in salt air within a few kilometres of the beach; 316 (marine grade, with molybdenum) does not. The upgrade on a full walk-in is a few thousand pesos. The repaint after 304 bleeds rust into a white lacquer door is not.</div>"""),
  ("The Ventilation Detail That Costs Nothing",
   """    <p>Every closet we build gets an air path, and it is the cheapest durability decision in the whole job. Three details, none of which change the visible design:</p>
    <ol>
      <li><strong>Hold the carcass off the wall.</strong> A 12&ndash;15 mm batten behind the back panel creates a chimney gap so wall moisture never sits against the panel. On an exterior wall we also paint the block face with a cementitious waterproofer before the carcass goes in.</li>
      <li><strong>Vent top and bottom.</strong> A continuous 10 mm gap at the plinth plus a slotted or perforated panel in the top rail lets air convect. In a fully closed walk-in, a small extraction to the bathroom duct or a 4&ndash;6 W trickle fan on a humidistat does the same job.</li>
      <li><strong>Lift the base.</strong> Plinth feet, not a carcass sitting on the floor tile &mdash; so a leak, a mopped floor or a hurricane-driven water ingress does not wick into the bottom panel.</li>
    </ol>
    <p>In houses that are closed up for months between owner visits &mdash; the norm for second homes here &mdash; add a rechargeable dehumidifier or a low-wattage closet rod heater. Clients who do this stop reporting mildew on stored linen entirely.</p>"""),
  ("Specifying a Walk-In That Works in This Climate",
   """    <p>Layout rules that hold up locally, as opposed to the ones in imported design catalogues:</p>
    <ul>
      <li><strong>Open shelving over drawers for anything worn daily.</strong> Air moves; drawers do not. Keep drawers for items that leave the house rarely.</li>
      <li><strong>Slatted or cane-panel doors on a jungle-side wall.</strong> In Tulum and inland Puerto Morelos the humidity load is higher than at the beach because there is no breeze. A vented door face is a genuine functional upgrade, not a style choice.</li>
      <li><strong>Lacquer over open-pore finishes on the coast.</strong> A catalysed lacquer or 2K polyurethane closes the surface. Oiled and waxed finishes look beautiful for a season and then need annual attention.</li>
      <li><strong>No shoe storage on the floor of an exterior-wall closet.</strong> It is the coldest surface in the box and the first place condensation appears.</li>
      <li><strong>LED at 3000 K on the shelf front edge, driver outside the carcass.</strong> Drivers fail in heat; keep them accessible.</li>
    </ul>
    <p>We build closets in our own shop in Playa del Carmen, which matters for one practical reason: panels are cut, edged and assembled in a controlled space and then installed, instead of being cut on a dusty site in 32&deg;C heat. It also means a damaged door is remade in days rather than reordered from a catalogue supplier in Mexico City.</p>"""),
 ],
 "faq": [
  ("What does a custom closet cost per linear metre in Playa del Carmen?",
   "In our recommended coastal spec &mdash; marine plywood carcass, lacquered fronts, 316 stainless hardware &mdash; $11,000&ndash;$17,000 MXN per linear metre ($610&ndash;$945 USD) installed. Melamine on moisture-resistant MDF with 304 hardware runs $7,000&ndash;$11,000 and is a reasonable choice for interior walls in an air-conditioned house. Add 8&ndash;12% for Tulum and Puerto Aventuras, 15&ndash;20% for Cozumel and Isla Mujeres."),
  ("Is melamine a bad choice for closets on the Caribbean coast?",
   "Melamine as a <em>surface</em> is fine &mdash; it is stable and easy to clean. The problem is what is under it. Melamine bonded to particleboard swells permanently once it reaches 16&ndash;18% moisture content, which an unventilated closet against an exterior wall will do. Melamine on moisture-resistant MDF or on plywood behaves very differently. Always ask the carpenter what the substrate is, not what the finish is."),
  ("Why does the hardware in my closet have rust spots after two years?",
   "Almost certainly 304 stainless or nickel-plated steel. Within a few kilometres of the sea, chloride-laden air pits 304 and the corrosion bleeds into surrounding paint or lacquer. 316 stainless (marine grade) resists it. On hinges, rods, rails and handles the price difference across a whole walk-in is small; replacing stained doors is not."),
  ("Can you build closets for a house that sits empty for months?",
   "Yes, and the spec changes. Vented door faces, plinth feet, a back-panel air gap and a humidistat-controlled trickle fan or rechargeable dehumidifier inside the carcass. We also recommend leaving closet doors ajar during absences and avoiding leather and untreated cotton storage. This is the standard brief for second homes in Playacar, Puerto Aventuras and Aldea Zam&aacute;."),
  ("Do you make the closets yourselves or subcontract them?",
   "Our own carpentry shop in Playa del Carmen cuts, edges, assembles and finishes them, and our installers fit them. That is why we can hold the moisture and hardware spec &mdash; and why a damaged panel is remade in days. The same shop makes the kitchens, doors, pergolas and furniture, so joinery across the house matches in species and finish."),
 ],
}

CONTENT["pergola-palapa-construction-riviera-maya"] = {
 "title": "Palapa and Pergola Construction in the Riviera Maya",
 "desc": "What a huano palapa costs per m², how long the thatch lasts, the fire-retardant rule for hotels, and when a hardwood or aluminium pergola wins.",
 "intro": [
   "A palapa and a pergola solve the same problem &mdash; shade over an outdoor room &mdash; and almost nothing else about them is comparable. A palapa is a thatched roof of huano palm over a hardwood frame: it is the coolest structure you can build here, it is culturally native to the peninsula, and it is a consumable &mdash; the thatch has a service life, not a warranty. A pergola is a permanent frame, usually hardwood, aluminium or steel, that you specify once.",
   "Owners get this decision wrong in both directions: they build a palapa over a grill they use weekly and are surprised when smoke shortens the thatch life, or they put an aluminium pergola on a jungle lot in Tulum where a palapa would have read better and cost less. Below is what each actually costs, what maintenance each demands, and the permit and fire rules that apply when the structure is for a rental or a hotel."
 ],
 "sections": [
  ("Palapa: Real Costs and Real Service Life",
   """    <p>A palapa is priced by roof area, and the two variables that move the price most are pitch and thatch density. A steeper pitch sheds water faster and lasts materially longer; a denser weave costs more per m&sup2; and also lasts longer. Cheap palapas are cheap because they are shallow and thin, and they are the ones that leak in the third year.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Spec</th><th>MXN / m&sup2; of roof</th><th>USD / m&sup2;</th><th>Thatch service life</th></tr></thead>
      <tbody>
        <tr><td>Economy: low pitch, thin weave, rough poles</td><td>$1,400&ndash;$2,200</td><td>$78&ndash;$122</td><td>4&ndash;7 years</td></tr>
        <tr><td>Standard: 45&deg;+ pitch, dense weave, treated frame</td><td>$2,400&ndash;$3,800</td><td>$133&ndash;$211</td><td>8&ndash;12 years</td></tr>
        <tr><td>Premium: steep pitch, double-layer ridge, chiclero-grade weave</td><td>$4,000&ndash;$6,500</td><td>$222&ndash;$361</td><td>12&ndash;18 years</td></tr>
        <tr><td>Fire-retardant treated (hotel / rental compliance)</td><td>+$450&ndash;$900</td><td>+$25&ndash;$50</td><td>treatment re-applied per supplier cycle</td></tr>
      </tbody>
    </table>
    </div>
    <p>A 40 m&sup2; terrace palapa in the standard spec is therefore roughly $96,000&ndash;$152,000 MXN. Re-thatching later costs 45&ndash;65% of the original roof price, because the frame is reused. Budget for it the way you budget for exterior paint: a known cost on a known cycle, not a failure.</p>
    <div class="alert alert-warning"><i class="bi bi-exclamation-triangle me-2"></i><strong>Ask where the huano comes from and when it was cut.</strong> Palm harvested in the wrong moon phase or installed green is the single most common cause of a palapa that rots or gets eaten early. Established palapa crews on the peninsula are specific about this; opportunistic ones are not.</div>"""),
  ("Fire Rules, Insurance and Rentals",
   """    <p>If the structure shades a private terrace on a private house, the practical requirement is a municipal construction licence covering the works and, on the coast, confirmation you are not inside the federal maritime zone. If the property is a rental, a restaurant, or any part of a hotel, two more things apply and they are the ones people discover late:</p>
    <ul>
      <li><strong>Civil Protection (Protecci&oacute;n Civil) review.</strong> A thatched roof over a commercial occupancy is treated as a combustible roof assembly. Expect a requirement for fire-retardant treatment of the thatch, extinguisher placement, and clear egress under the structure.</li>
      <li><strong>Insurance wording.</strong> Several insurers writing property cover in Quintana Roo either exclude thatch entirely or require documented retardant treatment and a stated replacement cycle. Check the policy before you build, not after the claim.</li>
      <li><strong>Clearance from ignition sources.</strong> Open grills, pizza ovens and fire features under a palapa need a non-combustible hood and vertical clearance; otherwise plan the kitchen outside the thatch footprint.</li>
    </ul>
    <p>None of this rules out a palapa for a rental villa &mdash; a large share of the ones we build are on rental properties. It changes the specification and adds a documented maintenance obligation.</p>"""),
  ("When a Pergola Is the Better Structure",
   """    <p>Choose a pergola over a palapa when the structure needs to be maintenance-light, when it sits over a grill or outdoor kitchen, when it carries a retractable shade or solar panels, or when the architecture is contemporary and a thatch roof would fight it.</p>
    <div class="table-responsive">
    <table class="table table-bordered">
      <thead class="table-dark"><tr><th>Pergola type</th><th>MXN / m&sup2;</th><th>Maintenance</th><th>Best use</th></tr></thead>
      <tbody>
        <tr><td>Tropical hardwood (tzalam, chechen, parota)</td><td>$3,500&ndash;$7,000</td><td>Re-oil or re-seal every 12&ndash;24 months on the coast</td><td>Jungle and garden settings, Tulum aesthetic</td></tr>
        <tr><td>Powder-coated aluminium, fixed louvre</td><td>$5,500&ndash;$9,500</td><td>Wash only</td><td>Beachfront, rentals, owner absent for months</td></tr>
        <tr><td>Aluminium bioclimatic (motorised louvres)</td><td>$11,000&ndash;$20,000</td><td>Motor service; wash</td><td>Roof terraces, restaurants, premium villas</td></tr>
        <tr><td>Hot-dip galvanised steel with timber infill</td><td>$4,500&ndash;$8,500</td><td>Inspect coating at fixings</td><td>Long spans, structures carrying solar</td></tr>
      </tbody>
    </table>
    </div>
    <p>Two local specification notes. First, in salt air every fastener and bracket should be 316 stainless or hot-dip galvanised &mdash; a hardwood pergola bolted with plain steel fails at the connections long before the timber does. Second, anything on a roof terrace must be engineered for uplift and either designed to be struck down before a hurricane or anchored to the slab through the waterproofing with a detailed, sealed penetration. We design pergolas here for uplift first and appearance second; the order matters in June.</p>"""),
 ],
 "faq": [
  ("How much does a palapa cost per square metre in 2026?",
   "In the specification we recommend &mdash; 45&deg; or steeper pitch, dense weave, treated hardwood frame &mdash; $2,400&ndash;$3,800 MXN per m&sup2; of roof ($133&ndash;$211 USD). A 40 m&sup2; terrace palapa is roughly $96,000&ndash;$152,000 MXN. Economy palapas start near $1,400/m&sup2; but last 4&ndash;7 years instead of 8&ndash;12."),
  ("How long does palapa thatch last before it has to be replaced?",
   "Eight to twelve years for a well-pitched, densely woven huano roof; four to seven for a shallow, thin one; twelve to eighteen for a premium steep-pitch roof with a double-layer ridge. Re-thatching reuses the frame and costs 45&ndash;65% of the original roof price. Treat it as a scheduled cost, like exterior paint."),
  ("Do I need a permit for a palapa or pergola?",
   "For a private terrace structure, the municipal construction licence covering the works, plus confirmation that you are outside the federal maritime zone (ZOFEMAT) if you are beachfront. For a rental, restaurant or hotel, a Civil Protection review applies and usually brings a fire-retardant treatment requirement for thatch. We handle both as part of the build."),
  ("Palapa or pergola for a rental villa?",
   "A palapa if the look is the selling point and you accept a documented maintenance and retardant-treatment cycle. An aluminium pergola if the property is managed remotely and you want a structure that needs washing and nothing else. For a terrace with a built-in grill, pergola &mdash; open flame under thatch requires clearances that usually make the kitchen layout awkward."),
  ("Can a pergola carry solar panels or a retractable awning?",
   "Yes, but it has to be designed for it. Panels add dead load and, more importantly, a large uplift surface; a retractable awning adds a concentrated load at the cassette. Galvanised steel or a purpose-engineered aluminium system handles both. A decorative hardwood pergola sized for shade alone does not, and adding panels to one after the fact is how they end up in the pool after a storm."),
 ],
}

CONTENT["wood-deck-construction-riviera-maya"] = {
 "title": "Wood Decks in the Riviera Maya: Species, Costs and Pool Details",
 "desc": "Tropical hardwood vs composite decking on this coast: cost per m², joist and ventilation details that prevent rot, and what works at the pool edge.",
 "intro": [
   "A deck here has to survive three things at once that decks elsewhere rarely face together: standing humidity under the boards, UV at a latitude of 20&deg;N, and either chlorine splash or salt-system water at the pool edge. Add termites, which are endemic across the peninsula and will find untreated softwood framing within a season, and the material list narrows quickly.",
   "This is a practical specification guide: which species actually hold up, what composite does and does not solve, the substructure detail that decides whether a deck lasts eight years or twenty-five, and installed costs per m&sup2; in Playa del Carmen, Tulum and the surrounding corridor for 2026."
 ],
 "sections": [
  ("Species and Materials: What Survives",
   """    <p>Decking choice is a durability class decision before it is an aesthetic one. The species below are the ones we specify and the ones worth paying for locally.</p>
    <ul>
      <li><strong>Ip&eacute; (Brazilian walnut):</strong> the benchmark. Extremely dense, naturally rot and termite resistant, 25+ years on a coastal deck with periodic oiling. Most expensive, hardest to machine, needs pre-drilling.</li>
      <li><strong>Cumaru:</strong> close behind ip&eacute; at roughly 70&ndash;80% of the price; slightly more movement, excellent durability.</li>
      <li><strong>Tzalam:</strong> the regional choice &mdash; harvested on the peninsula, beautiful chocolate tone, good durability when kept ventilated. Our most-requested hardwood deck.</li>
      <li><strong>Chechen:</strong> hard and stable, striking colour variation. Handle the sap with care during fabrication.</li>
      <li><strong>Teak:</strong> superb stability and water behaviour; plantation teak locally is expensive and quality varies sharply by supplier.</li>
      <li><strong>Pressure-treated pine:</strong> acceptable for a hidden substructure only if the treatment is rated for ground contact, and never as a finished surface here.</li>
      <li><strong>WPC composite:</strong> solves splinters, annual oiling and termites. Does not solve heat &mdash; dark composite on a west-facing terrace gets too hot to walk on barefoot at 3 p.m. Choose light colours and capped boards with UV-stable pigment.</li>
    </ul>
    <p>Whatever the surface, the fasteners are 316 stainless and the substructure is either treated hardwood or hot-dip galvanised / aluminium joists. A hardwood deck on plain steel or untreated pine joists is a five-year deck with a twenty-year surface on top of it.</p>"""),
  ("Installed Cost Per Square Metre &mdash; 2026",
   """    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Deck build-up</th><th>MXN / m&sup2; installed</th><th>USD / m&sup2;</th><th>Coastal life</th></tr></thead>
      <tbody>
        <tr><td>Tzalam on treated hardwood joists, hidden clips</td><td>$3,200&ndash;$5,200</td><td>$178&ndash;$289</td><td>15&ndash;20 years</td></tr>
        <tr><td>Cumaru on aluminium substructure</td><td>$4,200&ndash;$6,800</td><td>$233&ndash;$378</td><td>20&ndash;25 years</td></tr>
        <tr><td>Ip&eacute; on aluminium substructure</td><td>$5,500&ndash;$9,000</td><td>$306&ndash;$500</td><td>25+ years</td></tr>
        <tr><td>Capped WPC composite on aluminium</td><td>$3,800&ndash;$6,500</td><td>$211&ndash;$361</td><td>20&ndash;25 years, low maintenance</td></tr>
        <tr><td>Elevated deck over sloping or rocky ground (add)</td><td>+$900&ndash;$2,500</td><td>+$50&ndash;$139</td><td>&mdash;</td></tr>
      </tbody>
    </table>
    </div>
    <p>A 45 m&sup2; pool deck in tzalam therefore runs roughly $144,000&ndash;$234,000 MXN installed. The elevated-structure premium is real on jungle lots in Tulum and on the limestone shelf north of Akumal, where levelling by excavation is more expensive than building a ventilated platform over the rock.</p>"""),
  ("The Substructure and Ventilation Detail",
   """    <p>Nearly every failed deck we are asked to replace failed from underneath. The board surface still looks serviceable while the joists and fixings have gone. Four details prevent it:</p>
    <ol>
      <li><strong>Air under the deck, always.</strong> Minimum 8&ndash;10 cm clear to grade or slab, with cross-ventilation at the perimeter. A deck sealed at its edges is a humidity trap, and on this coast that means rot and termites regardless of species.</li>
      <li><strong>Joist spacing 40&ndash;45 cm, not 60.</strong> Tropical hardwood boards are usually 19&ndash;21 mm here; the wider spacing common in imported details produces springy boards and cupping.</li>
      <li><strong>Gap the boards 5&ndash;7 mm.</strong> Rain here arrives fast and heavy. Tight boards pond water and trap debris, and the debris holds moisture against the surface.</li>
      <li><strong>Termite barrier at every ground contact.</strong> Concrete pads or galvanised shoes, never timber into soil, plus a soil treatment before the platform closes. The peninsula's subterranean termites will find any timber-to-ground path.</li>
    </ol>
    <p>At the pool edge two more rules apply: hardwood ends get sealed before installation, because end grain is where chlorinated or saline water enters; and the deck is set so splash drains away from the boards, not into the substructure. Salt-system pools are gentler on skin and harder on metal &mdash; there the 316 stainless fastener requirement is not optional.</p>"""),
 ],
 "faq": [
  ("What does a hardwood deck cost per square metre in the Riviera Maya?",
   "Tzalam on treated hardwood joists with hidden clips: $3,200&ndash;$5,200 MXN per m&sup2; installed ($178&ndash;$289 USD). Cumaru on an aluminium substructure: $4,200&ndash;$6,800. Ip&eacute;: $5,500&ndash;$9,000. Capped WPC composite sits between tzalam and cumaru at $3,800&ndash;$6,500 and needs far less maintenance. Elevated decks over rock or slope add $900&ndash;$2,500 per m&sup2;."),
  ("Which wood is best for a pool deck here &mdash; tzalam, ip&eacute; or teak?",
   "Ip&eacute; lasts longest and costs most. Tzalam is the best value locally: regionally harvested, handsome, and durable when the deck is properly ventilated and the board ends are sealed. Teak is excellent but local supply quality varies a lot by batch. Whichever you choose, the deciding factors are ventilation underneath, 316 stainless fixings and sealed end grain &mdash; not the species alone."),
  ("Is composite decking a good idea on the Caribbean coast?",
   "For a remotely managed or rental property, often yes: no annual oiling, no splinters, immune to termites. The trade-off is surface temperature &mdash; dark composite in full afternoon sun becomes uncomfortable barefoot. Specify light colours, capped boards with UV-stable pigment, and the same ventilated aluminium substructure you would use under hardwood."),
  ("How often does a hardwood deck need refinishing in this climate?",
   "If you want the original colour, oil it every 12&ndash;18 months; on a fully exposed beachfront deck, annually. If you accept the silver-grey patina that UV produces, you can skip the oil and just wash it &mdash; the durability of ip&eacute;, cumaru and tzalam comes from density, not from the finish. What you cannot skip is clearing debris from board gaps and checking fixings once a year."),
  ("Can you build a deck over rock or a steep jungle lot?",
   "Yes, and it is frequently cheaper than levelling. We build a ventilated platform on concrete pads or drilled anchors into the limestone, with galvanised or aluminium framing above grade. That approach also keeps the timber away from soil contact, which is the main termite path, and it disturbs far less of the lot &mdash; which matters where the environmental file limits site clearance."),
 ],
}

CONTENT["custom-kitchen-cabinets-playa-del-carmen"] = {
 "title": "Custom Kitchen Cabinets in Playa del Carmen: Specification Guide",
 "desc": "Carcass substrates, door finishes and hardware grades that survive coastal humidity, plus real 2026 cabinet pricing per linear metre in Playa del Carmen and Tulum.",
 "intro": [
   "A kitchen is the most expensive joinery in the house and the hardest working. It takes steam, splash, heat from an oven, and in this climate a permanent 75&ndash;85% ambient humidity load whenever the air conditioning is off &mdash; which in most houses here is most of the day. The difference between a kitchen that looks new at year twelve and one that has swollen door edges at year four is decided in the specification, before anyone chooses a colour.",
   "Below: what to use for the carcass, how each door finish behaves locally, why the hinge and drawer-runner grade matters more here than anywhere you have built before, and what a full kitchen costs per linear metre in Playa del Carmen in 2026."
 ],
 "sections": [
  ("Carcass, Doors and Countertops",
   """    <p><strong>Carcass.</strong> Marine or phenolic-glued plywood for anything under a sink, next to a dishwasher, or on an exterior wall; moisture-resistant MDF is acceptable elsewhere in an air-conditioned kitchen. Particleboard under a sink is the single most common failure we replace &mdash; one slow supply-line drip and the base is unrecoverable.</p>
    <p><strong>Doors.</strong> Four realistic options and how they behave on the coast:</p>
    <ul>
      <li><strong>Catalysed lacquer / 2K polyurethane on MDF:</strong> the best value for a clean contemporary look. Closed surface, repairable, holds colour. Avoid high-gloss on a sun-facing wall &mdash; it shows every distortion.</li>
      <li><strong>Thermofused laminate (TFL) and high-pressure laminate:</strong> extremely stable and forgiving in humidity. The honest workhorse; the giveaway is the edge detail, so specify laser-edged or 2 mm ABS, not thin tape.</li>
      <li><strong>Solid tropical hardwood fronts on a plywood carcass:</strong> beautiful and locally sourced (tzalam, parota, chechen). Expect seasonal movement of a millimetre or two across a wide rail &mdash; design the reveals to absorb it.</li>
      <li><strong>Veneer:</strong> gorgeous, and the least tolerant of a steam leak or a persistent damp spot. Only with a properly sealed carcass and good extraction.</li>
    </ul>
    <p><strong>Countertops.</strong> Local granite and quartzite are abundant and priced well. Engineered quartz performs superbly indoors but discolours under direct UV, so do not carry it out to an exposed terrace. Concrete and chukum finishes suit the regional aesthetic and need sealing on a schedule. For an outdoor kitchen, the surfaces that last are granite, porcelain slab and stainless.</p>"""),
  ("Cabinet Pricing Per Linear Metre &mdash; Playa del Carmen 2026",
   """    <p>Kitchens here are quoted per linear metre of run, counting upper and lower cabinets together, with countertops and appliances separate. These are our installed figures for Playa del Carmen; Tulum and Puerto Aventuras run 8&ndash;12% higher on access and logistics.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Specification</th><th>MXN / linear metre</th><th>USD / linear metre</th></tr></thead>
      <tbody>
        <tr><td>Laminate on moisture-resistant MDF, 304 hardware</td><td>$9,000&ndash;$14,000</td><td>$500&ndash;$780</td></tr>
        <tr><td>Lacquered MDF fronts, marine plywood wet-zone carcasses, 316 hardware</td><td>$14,000&ndash;$22,000</td><td>$780&ndash;$1,220</td></tr>
        <tr><td>Solid tzalam or parota fronts, plywood carcass, soft-close throughout</td><td>$20,000&ndash;$34,000</td><td>$1,110&ndash;$1,890</td></tr>
        <tr><td>Countertop: local granite / quartzite</td><td>$2,800&ndash;$6,500 per m&sup2;</td><td>$155&ndash;$361</td></tr>
        <tr><td>Countertop: engineered quartz or porcelain slab</td><td>$5,500&ndash;$12,000 per m&sup2;</td><td>$306&ndash;$667</td></tr>
      </tbody>
    </table>
    </div>
    <p>A typical 7-linear-metre kitchen with an island, in the middle specification, lands around $98,000&ndash;$154,000 MXN for cabinetry plus $25,000&ndash;$60,000 for stone. Appliances are usually the next largest line and are worth sourcing early &mdash; lead times on imported built-ins into Quintana Roo run long.</p>
    <div class="alert alert-warning"><i class="bi bi-exclamation-triangle me-2"></i><strong>Check the hinge and runner brand and grade in writing.</strong> Soft-close hardware from an unnamed supplier fails in two to three years of coastal use, and replacing it means removing every door. Named European hardware with a 316 or properly coated finish costs a fraction of the kitchen and outlives it.</div>"""),
  ("Layout and Services in a Coastal Kitchen",
   """    <p>Local specifics that change a kitchen plan here:</p>
    <ul>
      <li><strong>Extraction is a durability item, not a comfort item.</strong> A ducted hood that actually discharges outside removes the steam load that destroys cabinet interiors. Recirculating hoods keep the moisture in the room.</li>
      <li><strong>Plan for water treatment.</strong> Municipal supply across the corridor is hard and often chlorinated; most of our clients want a filter at the sink and a softener upstream. Leave the cabinet space and the plumbing for it at rough-in.</li>
      <li><strong>Toe-kick and plinth.</strong> Sealed plinths with removable panels so a leak dries and gets found. Cabinets sitting directly on tile wick water.</li>
      <li><strong>Voltage and appliance reality.</strong> Mexican residential supply is 127 V; large imported ranges, some ovens and many US dryers need a 220 V circuit run deliberately. Decide before the electrical rough-in, not at installation.</li>
      <li><strong>Second-home kitchens.</strong> If the house closes for months, specify vented plinth panels, leave a gap behind the base cabinets, and avoid veneer. It costs nothing and prevents the classic return-visit smell.</li>
    </ul>
    <p>We fabricate kitchens in our own shop in Playa del Carmen, which keeps the substrate and hardware specification under our control and means a damaged front is remade rather than reordered. It also lets us match the kitchen to the closets, doors and furniture in the same species and finish &mdash; the detail that makes a house read as one project.</p>"""),
 ],
 "faq": [
  ("What does a custom kitchen cost in Playa del Carmen?",
   "Cabinetry runs $14,000&ndash;$22,000 MXN per linear metre ($780&ndash;$1,220 USD) in the specification we recommend for this climate &mdash; lacquered fronts, marine plywood in the wet zones, 316 hardware. A 7-metre kitchen with an island is therefore roughly $98,000&ndash;$154,000 MXN for the cabinets, plus $25,000&ndash;$60,000 for granite or quartz. Laminate builds start near $9,000 per linear metre."),
  ("What is the best cabinet material for coastal humidity?",
   "Marine or phenolic-glued plywood for any carcass in a wet zone, moisture-resistant MDF elsewhere, and either catalysed lacquer or laminate on the doors. The substrate matters more than the finish: particleboard under a sink fails on the first slow drip, no matter how good the door looks."),
  ("Can I use engineered quartz on an outdoor kitchen counter?",
   "Not in direct sun. Engineered quartz discolours under sustained UV, and most manufacturers exclude exterior use from their warranty. For outdoor kitchens use granite, full-body porcelain slab or stainless steel. Indoors, quartz performs very well here."),
  ("Do you handle the appliances and the 220 V circuits?",
   "Yes. We coordinate appliance specification early because lead times into Quintana Roo are long, and our electricians run any 220 V circuits at rough-in &mdash; Mexican residential supply is 127 V, so an imported range or a large oven needs a dedicated circuit planned before the walls close."),
  ("How long does a custom kitchen take from measurement to installation?",
   "Typically four to seven weeks in our shop for fabrication and finishing, plus two to five days on site for installation, with the countertop templated after the cabinets are set and fitted about a week later. Solid hardwood fronts and specialty finishes sit at the longer end. We schedule it against the site programme so the kitchen is not sitting in a dusty house."),
 ],
}

CONTENT["tropical-hardwood-furniture-riviera-maya"] = {
 "title": "Tropical Hardwood Furniture: Parota, Tzalam and Chechen Guide",
 "desc": "How Yucatán hardwoods behave, what kiln-dried really means here, joinery that survives 80% humidity, and what commissioned pieces cost in 2026.",
 "intro": [
   "The peninsula produces some of the best furniture timber in the Americas, and it is available within a few hours of Playa del Carmen: parota with its wide live-edge slabs, tzalam with its chocolate figure, chechen with dramatic colour, machiche and huanacaxtle for heavier work. Commissioning furniture from a local shop costs less than importing something comparable, and the piece is made for this climate rather than shipped into it.",
   "The risk is the same as the opportunity: a slab bought wet and built immediately will move, crack and open its joints within a year, and by then the maker has moved on. This guide explains what to specify so that does not happen &mdash; drying and moisture content, joinery that accommodates movement, finishes that hold up to humidity and UV &mdash; and what commissioned pieces actually cost."
 ],
 "sections": [
  ("The Species, Honestly Compared",
   """    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Species</th><th>Character</th><th>Best for</th><th>Watch for</th></tr></thead>
      <tbody>
        <tr><td><strong>Parota</strong> (guanacaste)</td><td>Wide slabs, open grain, warm honey-brown, relatively light</td><td>Live-edge dining tables, benches, headboards</td><td>Wide boards move the most &mdash; drying and breadboard detailing are critical</td></tr>
        <tr><td><strong>Tzalam</strong> (Caribbean walnut)</td><td>Dense, chocolate with dark streaks, fine figure</td><td>Dining tables, cabinetry fronts, doors, decking</td><td>Colour deepens with UV; keep sets from one batch</td></tr>
        <tr><td><strong>Chechen</strong> (Caribbean rosewood)</td><td>Very hard, red-to-black variation</td><td>Table tops, accent pieces, flooring</td><td>The sap irritates skin &mdash; a fabrication issue, not an owner issue</td></tr>
        <tr><td><strong>Machiche</strong></td><td>Heavy, tight-grained, dark red-brown</td><td>Structural furniture, outdoor benches, stair treads</td><td>Hard on tooling; expect a longer build time</td></tr>
        <tr><td><strong>Huanacaxtle</strong></td><td>Figured, wide availability in slabs</td><td>Tables, consoles</td><td>Quality varies sharply by supplier and by log</td></tr>
      </tbody>
    </table>
    </div>
    <p>All of these are regionally harvested. Ask for documentation of legal origin &mdash; the reputable yards on the peninsula can produce it, and it is the single best filter on the supply chain.</p>"""),
  ("Drying, Moisture Content and Movement",
   """    <p>This is the part that decides whether a table survives. Timber reaches equilibrium with the air around it; in the Riviera Maya interior that equilibrium sits around 12&ndash;14% moisture content, and higher in a house without air conditioning. A slab that arrives at 20%+ will lose several percent after it becomes furniture, and it will do so by shrinking across the grain, which is how tops cup and how a mortise opens.</p>
    <ul>
      <li><strong>Ask for a moisture meter reading, in writing, before fabrication.</strong> Target 10&ndash;14% for interior furniture here. A maker who cannot tell you the number is not measuring it.</li>
      <li><strong>Air-dried plus a kiln cycle</strong> is the practical local standard: a year or more of air drying, then a kiln to finish and to kill insects. Kiln-only on a thick slab often leaves a wet core.</li>
      <li><strong>Design for movement.</strong> Breadboard ends with elongated fixing slots, tops attached with buttons or figure-8 fasteners rather than screwed rigid, and no wide panel trapped in a tight frame.</li>
      <li><strong>Never let the piece dry in place next to a window.</strong> Sun on one face and cool air on the other cups a top faster than anything else.</li>
    </ul>
    <p>Cracks in parota slabs are normal and are usually stabilised with bow ties or epoxy fills. Done deliberately, they are part of the character. Appearing a year after delivery, they mean the slab was wet.</p>"""),
  ("What Commissioned Pieces Cost &mdash; 2026",
   """    <div class="table-responsive">
    <table class="table table-bordered">
      <thead class="table-dark"><tr><th>Piece</th><th>MXN</th><th>USD</th></tr></thead>
      <tbody>
        <tr><td>Parota live-edge dining table, 2.4 m, steel base</td><td>$38,000&ndash;$75,000</td><td>$2,110&ndash;$4,170</td></tr>
        <tr><td>Tzalam dining table, 2.4 m, solid hardwood base</td><td>$45,000&ndash;$90,000</td><td>$2,500&ndash;$5,000</td></tr>
        <tr><td>King bed frame with headboard, tzalam or parota</td><td>$28,000&ndash;$60,000</td><td>$1,560&ndash;$3,330</td></tr>
        <tr><td>Console or sideboard, 1.8 m</td><td>$22,000&ndash;$48,000</td><td>$1,220&ndash;$2,670</td></tr>
        <tr><td>Outdoor dining set, machiche or teak, 6 seats</td><td>$55,000&ndash;$120,000</td><td>$3,060&ndash;$6,670</td></tr>
        <tr><td>Full villa FF&amp;E package, 3-bedroom rental</td><td>$450,000&ndash;$1,200,000</td><td>$25,000&ndash;$66,700</td></tr>
      </tbody>
    </table>
    </div>
    <p>Finish choice matters as much as species for how the piece ages. Indoors, a catalysed lacquer or hardwax oil both work; oil is repairable in place, lacquer is more resistant to spills. Outdoors under a palapa or pergola, use a UV-stabilised exterior oil and accept a re-oiling cycle of 12&ndash;24 months, or let the timber silver deliberately. Fully exposed to sun and rain, only the densest species (machiche, ip&eacute;, teak) are worth the money, with 316 stainless fixings throughout.</p>"""),
 ],
 "faq": [
  ("Which tropical hardwood is best for a dining table here?",
   "Parota for a wide live-edge slab look, tzalam for a denser, darker, finer-figured table that moves less. Both are regionally harvested and both work well indoors &mdash; the deciding factor is whether the slab was properly dried, not which species you picked. For a table that will sit in a bright room, tzalam holds its appearance better."),
  ("What moisture content should furniture timber have in the Riviera Maya?",
   "Ten to fourteen percent for interior pieces, which is where the wood will settle in a house here. Ask the maker for a meter reading before fabrication starts. A slab at 18&ndash;20%+ will shrink after it becomes a table, and that shrinkage is what cups tops and opens joints in the first year."),
  ("How much does a custom parota dining table cost?",
   "A 2.4 m live-edge parota table with a steel base runs $38,000&ndash;$75,000 MXN ($2,110&ndash;$4,170 USD) depending on slab quality, thickness and base design. The same table in tzalam with a solid hardwood base is $45,000&ndash;$90,000. Lead times are typically four to eight weeks if the timber is already dried."),
  ("Can tropical hardwood furniture live outdoors?",
   "Under a palapa or pergola, yes &mdash; machiche, teak and ip&eacute; with a UV-stabilised exterior oil and 316 stainless fixings, re-oiled every 12&ndash;24 months or left to silver. Fully exposed to sun and rain, only the densest species justify the cost, and no finish removes the maintenance entirely. Parota is an indoor timber."),
  ("Do you supply full furniture packages for rental villas?",
   "Yes &mdash; FF&amp;E packages for rental properties are a regular part of our work, typically $450,000&ndash;$1,200,000 MXN for a three-bedroom villa depending on specification. Built in the same shop as the kitchen, closets and doors, so species and finish match across the house, and specified for rental duty: durable finishes, replaceable components, no delicate veneers."),
 ],
}

CONTENT["electrical-installation-new-home-riviera-maya"] = {
 "title": "Electrical Installation for a New Home in the Riviera Maya",
 "desc": "NOM-001-SEDE compliance, CFE connection steps and real costs, 127 V vs 220 V planning, and the coastal details that keep a new installation working past year five.",
 "intro": [
   "Electrical work is where an imported mental model causes the most trouble on a build here. Mexican residential supply is 127 V single phase, the governing standard is NOM-001-SEDE, and the utility &mdash; CFE &mdash; has its own sequence and its own timing that has nothing to do with your contractor's programme. Get the connection application moving late and you will finish a house that cannot be energised.",
   "This is the practical version: what a compliant installation includes, how the CFE connection actually works and what it costs, where 220 V circuits have to be planned, and the coastal details &mdash; corrosion, lightning, and long absences &mdash; that decide whether the installation is still sound at year ten."
 ],
 "sections": [
  ("What a Compliant Installation Includes",
   """    <p>NOM-001-SEDE is the Mexican electrical installations standard, and a residential installation that satisfies it looks broadly like this. It is also what a Unidad de Verificaci&oacute;n checks when a verification is required.</p>
    <ul>
      <li><strong>Load calculation and circuit schedule</strong> before any conduit is run &mdash; sized for real appliance load, air conditioning per room, pool equipment and water pumps.</li>
      <li><strong>Dedicated circuits</strong> for each air conditioner, the pool pump, the water pump and pressure system, the kitchen counter outlets, and any 220 V appliance.</li>
      <li><strong>GFCI protection</strong> (interruptor de falla a tierra) on bathrooms, kitchen counters, exterior outlets and everything within reach of the pool.</li>
      <li><strong>A real grounding system</strong> &mdash; ground rod or rods into the limestone with a measured resistance, bonded to the panel, plus equipotential bonding of the pool structure, ladders and metalwork.</li>
      <li><strong>Conduit throughout</strong> &mdash; PVC conduit cast in slabs and walls, not cable buried directly in plaster. It is the standard here and it is what lets a circuit be repulled later instead of re-chased.</li>
      <li><strong>Panel sized with spare ways</strong> &mdash; leave 25&ndash;30% spare. Solar, an EV charger or a second air conditioner will happen.</li>
    </ul>
    <p>The grounding item is the one most often skimped. On limestone, achieving a low resistance can require multiple rods, a deeper rod, or chemical treatment of the electrode pit &mdash; and it is the protection that everything else depends on.</p>"""),
  ("The CFE Connection: Sequence, Cost, Timing",
   """    <p>The utility connection runs in parallel with construction and is the item most likely to delay handover. The sequence:</p>
    <ol>
      <li><strong>Temporary construction supply</strong> (or a generator) for the build itself.</li>
      <li><strong>Application for definitive service</strong> with the property documents, the address, and the load you are requesting. Requesting the right load matters: too low and you are back for an upgrade, too high and you may trigger a different tariff and metering arrangement.</li>
      <li><strong>Verification</strong> of the internal installation where required, by an approved Unidad de Verificaci&oacute;n, producing the certificate CFE expects.</li>
      <li><strong>Utility works</strong> &mdash; transformer, service drop or underground run, meter base. If the lot needs a new transformer or poles, this is where cost and time expand.</li>
      <li><strong>Meter installation and energisation.</strong></li>
    </ol>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Item</th><th>Typical cost (MXN)</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>Full house wiring, 200&ndash;250 m&sup2;, NOM compliant</td><td>$180,000&ndash;$380,000</td><td>Materials + labour; varies with circuit count and automation</td></tr>
        <tr><td>Panel, protections, grounding system</td><td>$25,000&ndash;$70,000</td><td>Higher where limestone forces multiple electrodes</td></tr>
        <tr><td>Verification (UVIE) and paperwork</td><td>$8,000&ndash;$25,000</td><td>Scope depends on load and municipality</td></tr>
        <tr><td>CFE connection in a serviced urban street</td><td>$10,000&ndash;$40,000</td><td>Weeks, if the file is complete</td></tr>
        <tr><td>Extension: new poles / transformer to an unserviced lot</td><td>$150,000&ndash;$900,000+</td><td>Months. Check this <em>before</em> buying land</td></tr>
      </tbody>
    </table>
    </div>
    <div class="alert alert-warning"><i class="bi bi-exclamation-triangle me-2"></i><strong>Verify the service before you buy the lot.</strong> Two identical lots one street apart can differ by six figures and six months in electrification. On jungle lots in Tulum and along the Ruta de los Cenotes, off-grid with solar and storage is sometimes cheaper and faster than an extension &mdash; but that has to be a decision, not a surprise.</div>"""),
  ("Coastal Details, 220 V, and Houses That Sit Empty",
   """    <p>Three local realities shape the specification beyond the standard:</p>
    <ul>
      <li><strong>Corrosion.</strong> Within sight of the sea, exterior enclosures, covers, fixings and luminaire bodies need to be marine-rated &mdash; stainless or properly rated polymer, gasketed, with drip loops. Standard outdoor fittings from a general supplier rust through in a couple of years, and the failure is usually water in an enclosure, not the fitting itself.</li>
      <li><strong>Lightning and surge.</strong> The peninsula has a high lightning density in the wet season, and CFE supply quality varies. Fit whole-house surge protection at the panel plus point-of-use protection for AV, computers and pool controls. It is a cheap insurance line against the most common appliance loss here.</li>
      <li><strong>220 V by design.</strong> Imported ranges, some ovens, US dryers and most EV chargers need 220 V. That is two legs of the 127 V service, planned at rough-in, with the right conductor size to the appliance location. Retrofitting it into a finished wall is disruptive and avoidable.</li>
      <li><strong>Absent-owner circuits.</strong> For a house closed for months: a small always-on circuit for security, a dehumidifier and the pool controller, separated from everything else so the rest of the house can be isolated. Add remote monitoring of the pool pump &mdash; the most expensive failure during an absence is a pump running dry or a pool going green.</li>
    </ul>
    <p>We do electrical in-house on every project, which means the load schedule is drawn against the architectural plans, the conduit goes in before the slab is poured rather than being chased in afterwards, and the CFE file starts early enough that energisation is not the thing holding up your handover.</p>"""),
 ],
 "faq": [
  ("How much does electrical installation cost for a new house in the Riviera Maya?",
   "For a 200&ndash;250 m&sup2; house, a NOM-001-SEDE compliant installation runs $180,000&ndash;$380,000 MXN including materials and labour, plus $25,000&ndash;$70,000 for the panel, protections and grounding. Verification and paperwork add $8,000&ndash;$25,000. A CFE connection on a serviced street is $10,000&ndash;$40,000; extending service to an unserviced lot can exceed $900,000."),
  ("How long does a CFE connection take?",
   "Weeks on a serviced urban street if the file is complete and the verification is in order. Months if CFE has to install poles or a transformer to reach the lot. The application should be started well before the house is finished &mdash; late applications are the most common reason a completed house cannot be energised on schedule."),
  ("Is the electricity 110 V or 220 V in Mexico?",
   "Residential supply is 127 V single phase. 220 V is available as two legs of that service and has to be planned at rough-in for the appliances that need it &mdash; imported ranges and ovens, US-spec dryers, EV chargers, some pool and well equipment. Decide before the walls close; retrofitting means opening finished surfaces."),
  ("What does grounding involve on limestone?",
   "One or more electrodes driven into the rock, with the resistance actually measured rather than assumed. Limestone can give poor readings, so achieving compliance sometimes needs multiple rods, a deeper electrode or treatment of the electrode pit, plus equipotential bonding of the pool shell, ladders, rails and metalwork. It is the protection all the others depend on and the one most often skipped."),
  ("What should I install if the house will be empty for months?",
   "Whole-house surge protection, a separated always-on circuit for security, a dehumidifier and the pool controller, marine-rated exterior fittings, and remote monitoring on the pool pump. The classic absent-owner losses here are an appliance killed by a surge and a pool pump that failed unnoticed &mdash; both are cheap to protect against at installation."),
 ],
}

CONTENT["solar-panel-installation-cost-playa-del-carmen"] = {
 "title": "Solar Panel Cost in Playa del Carmen: Net Metering Math 2026",
 "desc": "What a residential solar system really costs in Playa del Carmen, how CFE net metering and the DAC tariff change the payback, and hurricane mounting done properly.",
 "intro": [
   "Solar makes unusually good sense on this coast: roughly 5.5&ndash;6 peak sun hours a day year-round, an air-conditioning load that peaks exactly when the sun is strongest, and a utility tariff structure that punishes high consumption hard enough to make self-generation compelling. The complication is that the payback depends far more on which CFE tariff you are on than on the price of the panels.",
   "Below: system sizing against real consumption, installed 2026 costs in Playa del Carmen, how net metering (medici&oacute;n neta) actually settles, the DAC tariff trap that transforms the economics, and the mounting and corrosion detail that decides whether the array is still on the roof after a Category 3."
 ],
 "sections": [
  ("Sizing and Installed Cost &mdash; 2026",
   """    <p>Size the system to your consumption history, not to your roof. Pull twelve months of CFE bills, work in kWh per two-month billing period, and design for the annual total &mdash; a system that overproduces in a net-metering scheme mostly gives energy away.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>System</th><th>Typical monthly output</th><th>Installed cost (MXN)</th><th>Installed cost (USD)</th></tr></thead>
      <tbody>
        <tr><td>3 kWp (small house, no AC or minimal)</td><td>~380&ndash;450 kWh</td><td>$75,000&ndash;$110,000</td><td>$4,200&ndash;$6,100</td></tr>
        <tr><td>5 kWp (typical 2&ndash;3 bed with AC)</td><td>~620&ndash;750 kWh</td><td>$115,000&ndash;$165,000</td><td>$6,400&ndash;$9,200</td></tr>
        <tr><td>8 kWp (villa, pool, several AC units)</td><td>~1,000&ndash;1,200 kWh</td><td>$175,000&ndash;$250,000</td><td>$9,700&ndash;$13,900</td></tr>
        <tr><td>12 kWp (large villa or small rental complex)</td><td>~1,500&ndash;1,800 kWh</td><td>$250,000&ndash;$370,000</td><td>$13,900&ndash;$20,600</td></tr>
        <tr><td>Battery storage, per 10 kWh usable</td><td>&mdash;</td><td>$90,000&ndash;$180,000</td><td>$5,000&ndash;$10,000</td></tr>
      </tbody>
    </table>
    </div>
    <p>Prices assume quality tier-1 panels, a named-brand inverter with a real local warranty channel, and proper structural mounting. Systems quoted 30&ndash;40% below these numbers usually cut the mounting, the inverter brand, or the paperwork &mdash; and the mounting is the one that matters most here.</p>"""),
  ("Net Metering and the DAC Tariff",
   """    <p>CFE's <em>medici&oacute;n neta</em> scheme runs a bidirectional meter: energy you export is credited against energy you import, and the credit carries forward for up to twelve months. What you settle is the net. That makes solar a consumption-offset play rather than a sell-to-the-grid business, and it means the value of each kWh you produce equals the price of the kWh you would otherwise have bought.</p>
    <p>Which brings us to the tariff that determines everything. Residential tariff 1A/1B/1C is subsidised in blocks. Exceed the high-consumption threshold on a rolling basis and CFE reclassifies you as <strong>DAC</strong> (Doméstica de Alto Consumo) &mdash; the subsidy disappears and the per-kWh price rises steeply. In a house with several air conditioners and a pool pump, DAC is easy to reach.</p>
    <ul>
      <li><strong>On a subsidised residential tariff,</strong> simple payback on a well-sized system typically runs 5&ndash;8 years.</li>
      <li><strong>On DAC,</strong> the same system commonly pays back in 3&ndash;5 years, and getting consumption back under the threshold can also return you to the subsidised tariff.</li>
      <li><strong>On a commercial tariff</strong> (rental complex, small hotel, restaurant) payback is usually 4&ndash;6 years, with demand charges making inverter and load management design worth doing carefully.</li>
    </ul>
    <p>So the honest first question is not "how many panels" but "what tariff am I on and how close am I to DAC". Bring twelve months of bills to the conversation and the answer is arithmetic.</p>"""),
  ("Mounting, Corrosion and Hurricanes",
   """    <p>Every wet season tests the mounting, and roughly once a decade a major hurricane tests it properly. What we specify:</p>
    <ul>
      <li><strong>Engineered attachment into the structural slab</strong> &mdash; anchors set into concrete with the waterproofing detailed and sealed at each penetration, not ballasted frames sitting on a flat roof.</li>
      <li><strong>Anodised aluminium rails with 316 stainless fixings.</strong> Anything galvanised-only within a couple of kilometres of the beach will stain and then seize.</li>
      <li><strong>Uplift-rated layout:</strong> panels set back from roof edges and parapets where uplift pressure is highest, tilt kept modest, rails spanned to the manufacturer's high-wind table rather than the standard one.</li>
      <li><strong>Cable management out of the sun.</strong> UV-degraded DC cable insulation is a common five-year fault and a fire risk. Conduit or properly rated tray, with drip loops at every entry.</li>
      <li><strong>Inverter located in shade and ventilated.</strong> Heat is the main determinant of inverter lifetime; an inverter on a west-facing exterior wall in full sun will not reach its rated life.</li>
    </ul>
    <p>One planning note for new builds: decide about solar before the roof slab is poured. Conduit routes, inverter position, a dedicated panel way and the anchor positions all cost almost nothing at that stage, and each of them costs real money to retrofit. If you are not installing now but might later, at least leave the conduit and the panel space &mdash; we do this by default on the houses we build.</p>"""),
 ],
 "faq": [
  ("How much does a solar system cost in Playa del Carmen?",
   "A 5 kWp system suited to a typical two-to-three bedroom house with air conditioning runs $115,000&ndash;$165,000 MXN installed ($6,400&ndash;$9,200 USD). An 8 kWp villa system with a pool is $175,000&ndash;$250,000. Battery storage adds roughly $90,000&ndash;$180,000 per 10 kWh usable. Prices assume tier-1 panels, a named-brand inverter and engineered mounting."),
  ("What is the payback period on solar here?",
   "Five to eight years on a subsidised residential tariff, three to five years if your consumption has pushed you onto the DAC high-consumption tariff, and four to six years on a commercial tariff. The tariff matters far more than the equipment price, so start by reviewing twelve months of CFE bills."),
  ("How does net metering work with CFE?",
   "A bidirectional meter credits the energy you export against the energy you import, with credits carrying forward for up to twelve months, and you settle the net. It is a consumption-offset arrangement rather than a sell-to-the-grid one, so oversizing the system mostly donates energy. Size to your annual consumption."),
  ("Will solar panels survive a hurricane?",
   "Properly engineered ones generally do. That means anchors into the structural slab with sealed, detailed penetrations, anodised aluminium rails, 316 stainless fixings, panels set back from roof edges where uplift is highest, and rail spans taken from the manufacturer's high-wind tables. Ballasted frames sitting loose on a flat roof are the ones that leave."),
  ("Should I install solar during construction or later?",
   "Install later if you like, but do the preparation during construction: conduit routes, inverter position, a dedicated panel way and anchor positions. Those cost almost nothing before the slab is poured and a great deal afterwards. We leave new houses solar-ready by default."),
 ],
}

CONTENT["backup-generator-riviera-maya"] = {
 "title": "Backup Generators in the Riviera Maya: Sizing and Costs",
 "desc": "Generator vs battery backup for a coastal villa: sizing for AC and pool loads, installed costs, fuel logistics after a hurricane and transfer switch rules.",
 "intro": [
   "Power goes out here for three reasons: routine faults in the wet season, planned utility work, and hurricanes. The first two last hours. The third can last days or, in a bad year and an outlying area, longer &mdash; and that is the scenario that decides what you should install. A villa with a pool, a cistern pump, refrigeration and an owner arriving next week has a different backup problem than a house occupied full time.",
   "This guide covers sizing against real loads, what generators and battery systems cost installed in 2026, the transfer-switch and fuel-storage details that make the difference between a backup that works and one that sits idle, and how each option behaves in the week after a storm."
 ],
 "sections": [
  ("Sizing: Do the Load Arithmetic First",
   """    <p>Almost every oversized generator we are asked to replace was sized by house area. Size by load instead, and split the load into what you want during a short outage and what you want during a long one.</p>
    <div class="table-responsive">
    <table class="table table-bordered">
      <thead class="table-dark"><tr><th>Load</th><th>Running watts</th><th>Starting surge</th></tr></thead>
      <tbody>
        <tr><td>Mini-split AC, 1 ton (12,000 BTU), inverter type</td><td>900&ndash;1,200 W</td><td>Low (soft start)</td></tr>
        <tr><td>Mini-split AC, 1 ton, non-inverter</td><td>1,100&ndash;1,400 W</td><td>2&ndash;3&times;</td></tr>
        <tr><td>Pool pump, 1&ndash;1.5 HP</td><td>750&ndash;1,500 W</td><td>2&ndash;3&times;</td></tr>
        <tr><td>Cistern / pressure pump</td><td>500&ndash;1,100 W</td><td>2&ndash;3&times;</td></tr>
        <tr><td>Refrigeration, lighting, outlets, WiFi</td><td>600&ndash;1,200 W</td><td>Low</td></tr>
        <tr><td>Water heater, electric</td><td>1,500&ndash;4,500 W</td><td>Low</td></tr>
      </tbody>
    </table>
    </div>
    <p>A realistic essentials package for a three-bedroom villa &mdash; refrigeration, lights, outlets, water pump, internet, and two bedrooms of air conditioning &mdash; sits around 4&ndash;6 kW running. Whole-house with the pool and all AC running lands at 10&ndash;15 kW. Inverter-type mini-splits change this calculation substantially because they avoid the hard starting surge, which is why we specify them on any house with backup.</p>"""),
  ("What It Costs Installed &mdash; 2026",
   """    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Option</th><th>Installed (MXN)</th><th>Installed (USD)</th><th>Reality</th></tr></thead>
      <tbody>
        <tr><td>Portable 5&ndash;7 kW petrol + manual interlock</td><td>$35,000&ndash;$70,000</td><td>$1,950&ndash;$3,900</td><td>Cheap; you must be present to start and refuel it</td></tr>
        <tr><td>Standby 8&ndash;12 kW, automatic transfer switch, LP gas</td><td>$160,000&ndash;$320,000</td><td>$8,900&ndash;$17,800</td><td>The default for an occupied villa</td></tr>
        <tr><td>Standby 15&ndash;22 kW, ATS, LP gas, whole house incl. pool</td><td>$300,000&ndash;$550,000</td><td>$16,700&ndash;$30,600</td><td>Large villas, small hotels</td></tr>
        <tr><td>Battery backup, 10&ndash;20 kWh, with existing solar</td><td>$140,000&ndash;$330,000</td><td>$7,800&ndash;$18,300</td><td>Silent, no fuel; limited to the essentials circuit overnight</td></tr>
        <tr><td>Solar + battery + small standby generator</td><td>$400,000&ndash;$800,000</td><td>$22,200&ndash;$44,400</td><td>The genuine multi-day answer for remote lots</td></tr>
      </tbody>
    </table>
    </div>
    <p>Two lines people forget. First, the concrete pad, the enclosure, the gas run and the conduit are a real part of the cost &mdash; a generator delivered is not a generator installed. Second, annual service: oil, filters, coolant and a load test, roughly $6,000&ndash;$15,000 MXN a year. An unserviced standby generator fails precisely when you finally need it, and the failure is nearly always the battery or stale fuel.</p>"""),
  ("Fuel, Transfer Switches and the Week After a Storm",
   """    <p><strong>Fuel choice is decided by the aftermath, not the purchase price.</strong> LP gas is the pragmatic local answer: it stores indefinitely without degrading, a stationary tank can hold days of running, and refills are a local delivery. Diesel gives the best fuel economy for large sets but needs fuel treatment and polishing in this humidity, and petrol both degrades in months and becomes the scarcest commodity in the region after a hurricane &mdash; queues at stations are the defining memory of every serious storm here.</p>
    <ul>
      <li><strong>Automatic transfer switch, properly interlocked.</strong> It must make back-feeding the grid physically impossible &mdash; that is a lineman-safety issue and a code issue, not a preference. Manual interlocks are acceptable for a portable set if the interlock is a real mechanical one.</li>
      <li><strong>Size the tank for five to seven days,</strong> not for a night. Deliveries pause during and immediately after a storm.</li>
      <li><strong>Mount above expected flood level,</strong> on a raised pad, with the enclosure rated for salt air and the intake and exhaust detailed against driven rain.</li>
      <li><strong>Exercise it monthly</strong> under load. Most standby units do this automatically; check that the schedule is actually enabled.</li>
      <li><strong>Surge protection on both sides.</strong> The return of grid power after an outage is itself a common appliance-killing event.</li>
    </ul>
    <p>For houses that sit empty, we usually recommend a modest battery system on an essentials circuit &mdash; security, internet, the pool controller and a dehumidifier &mdash; rather than a large generator nobody is there to start. It rides out the routine outages silently, keeps the pool from turning, and needs no fuel logistics. For full-time occupancy, or a rental that has to keep guests comfortable, an LP standby unit with an automatic transfer switch is the specification that holds up.</p>"""),
 ],
 "faq": [
  ("What size generator do I need for a villa in the Riviera Maya?",
   "Size by load, not by house area. An essentials package for a three-bedroom villa &mdash; refrigeration, lights, outlets, water pump, internet and two bedrooms of air conditioning &mdash; needs about 4&ndash;6 kW running. Whole-house including the pool and all air conditioning is 10&ndash;15 kW. Inverter-type mini-splits reduce the requirement noticeably because they avoid a hard starting surge."),
  ("How much does a whole-house standby generator cost installed?",
   "An 8&ndash;12 kW LP standby unit with an automatic transfer switch runs $160,000&ndash;$320,000 MXN installed ($8,900&ndash;$17,800 USD). A 15&ndash;22 kW unit covering a large villa with pool is $300,000&ndash;$550,000. Budget $6,000&ndash;$15,000 MXN a year for service &mdash; unserviced standby units fail when you need them."),
  ("LP gas, diesel or petrol for a backup generator here?",
   "LP gas for most residential installations: it stores indefinitely, a stationary tank holds days of running, and refills are a local delivery. Diesel suits large sets but needs fuel treatment in this humidity. Avoid petrol for anything permanent &mdash; it degrades within months and it is the hardest fuel to obtain in the days after a hurricane."),
  ("Is a battery system better than a generator?",
   "For a house that sits empty, usually yes &mdash; a 10&ndash;20 kWh battery on an essentials circuit keeps security, internet, the pool controller and a dehumidifier running through routine outages with no fuel and no noise, for $140,000&ndash;$330,000 MXN installed. For multi-day outages with full occupancy, batteries alone are not enough; the robust answer is solar plus battery plus a small LP standby set."),
  ("Do I need a transfer switch, or can I just plug the generator in?",
   "You need a transfer switch &mdash; automatic for a standby unit, or a genuine mechanical interlock for a portable one. It has to make back-feeding the utility physically impossible, which is a lineman-safety requirement, not an optional refinement. Improvised connections through an outlet are the most dangerous thing people do with a generator."),
 ],
}

CONTENT["ev-charger-installation-riviera-maya"] = {
 "title": "EV Charger Installation in the Riviera Maya: What It Takes",
 "desc": "Level 2 charging on 127/220 V Mexican supply: load calculation, CFE implications, costs for villas and rentals, and charging for hotels.",
 "intro": [
   "EV charging in Quintana Roo has moved from curiosity to a routine request, driven by two things: rental guests arriving in EVs from Canc&uacute;n airport rentals, and owners who want a charger before they need one. The installation itself is simple electrical work. What is not simple is the supply &mdash; Mexican residential service is 127 V, a Level 2 charger wants 220 V at 32&ndash;48 A, and the existing service to many houses here has no spare capacity for it.",
   "This covers the load calculation that determines whether your service can take a charger at all, what installation costs in 2026, the difference between doing it during construction and retrofitting, and what hotels and rental complexes should install if they want the booking advantage without a service upgrade."
 ],
 "sections": [
  ("Load Calculation and Service Capacity",
   """    <p>Start with what the charger draws and what your service can spare. A 7.4 kW single-phase Level 2 charger at 220 V pulls about 32 A continuously for hours. That is a substantial, sustained load &mdash; comparable to running three or four air conditioners without a break.</p>
    <ul>
      <li><strong>Check the service rating and the existing calculated load</strong> against the panel. Many villas here were wired with little headroom once the air conditioning, pool and water pumps were counted.</li>
      <li><strong>If there is no headroom, the options are</strong> a service upgrade with CFE, a lower-power charger (16&ndash;20 A), or a load-management device that throttles the charger when the rest of the house is drawing heavily. The third is usually the cheapest and works well &mdash; overnight charging rarely competes with peak household load.</li>
      <li><strong>Mind the tariff.</strong> Regular EV charging adds enough consumption to push a household across CFE's high-consumption threshold and onto the DAC tariff, where per-kWh costs rise steeply. Pairing a charger with solar is not just green &mdash; on DAC it is what keeps the running cost sane.</li>
      <li><strong>Dedicated circuit, dedicated protection.</strong> A charger requires its own circuit with the correct conductor size for a continuous load and GFCI/RCD protection appropriate to the equipment. No shared circuits, no extension arrangements.</li>
    </ul>"""),
  ("Installation Costs &mdash; 2026",
   """    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Scenario</th><th>Cost (MXN)</th><th>Cost (USD)</th></tr></thead>
      <tbody>
        <tr><td>Level 2 charger (7.4 kW), short run, capacity available</td><td>$28,000&ndash;$55,000</td><td>$1,560&ndash;$3,060</td></tr>
        <tr><td>Same, with a 25&ndash;40 m run and trenching to a detached garage</td><td>$45,000&ndash;$95,000</td><td>$2,500&ndash;$5,280</td></tr>
        <tr><td>Add load-management device instead of a service upgrade</td><td>+$8,000&ndash;$20,000</td><td>+$440&ndash;$1,110</td></tr>
        <tr><td>CFE service upgrade where required</td><td>$40,000&ndash;$250,000+</td><td>$2,200&ndash;$13,900+</td></tr>
        <tr><td>Conduit and capacity provision during construction (new build)</td><td>$6,000&ndash;$18,000</td><td>$330&ndash;$1,000</td></tr>
        <tr><td>Rental / hotel: 4 bays with shared load management and billing</td><td>$250,000&ndash;$650,000</td><td>$13,900&ndash;$36,100</td></tr>
      </tbody>
    </table>
    </div>
    <p>Note the gap between the last two rows and everything above them. Running conduit and leaving a panel way while the walls are open costs almost nothing; chasing a 220 V circuit through finished walls, a tiled terrace and a garden to reach a carport is most of the retrofit price. On every house we build we leave the conduit and the panel capacity whether or not the owner wants a charger today.</p>"""),
  ("Coastal Siting and Hotel Charging",
   """    <p><strong>Where the unit goes matters here more than in a temperate climate.</strong> A charger on a salt-exposed wall needs a genuinely weather-rated enclosure, a gasketed cover and a drip loop at the cable entry; the failures we see are water ingress and corroded terminals, not electronics. Keep it out of direct afternoon sun &mdash; heat derates the unit and shortens its life &mdash; and above any plausible flood or storm-surge level. Cable management on a wall hook rather than the floor keeps the lead out of standing water.</p>
    <p><strong>For rentals,</strong> a single 7.4 kW charger with a simple access method is enough to appear in listing filters and to satisfy guests charging overnight. Choose a unit with a locally supported warranty channel and an app that does not require the owner's personal account to authorise a guest.</p>
    <p><strong>For hotels and condo complexes,</strong> the sensible pattern is several lower-power bays sharing a managed supply rather than a couple of high-power ones: four 7 kW bays with load management typically need a smaller supply than two 22 kW bays, cost less to install, and serve more guests overnight. Add per-session billing if the charging is not meant to be free, and put the whole installation on a circuit that can be isolated for storm preparation. We design these against the building's existing load profile, which is the only way to know whether the supply needs upgrading at all.</p>"""),
 ],
 "faq": [
  ("Can I install a Level 2 EV charger on Mexican residential power?",
   "Yes. A 7.4 kW Level 2 charger runs on 220 V, which is obtained from two legs of the 127 V residential service on a dedicated circuit. The question is whether your existing service has spare capacity once air conditioning, pool and water pumps are counted &mdash; often it does not, and then you either upgrade with CFE, fit a smaller charger, or add a load-management device."),
  ("How much does EV charger installation cost in the Riviera Maya?",
   "$28,000&ndash;$55,000 MXN ($1,560&ndash;$3,060 USD) for a 7.4 kW charger on a short run where capacity is available. A long run with trenching to a detached carport is $45,000&ndash;$95,000. A CFE service upgrade, if needed, adds $40,000&ndash;$250,000 or more. Provision during construction costs only $6,000&ndash;$18,000."),
  ("Will an EV charger push my CFE bill onto the DAC tariff?",
   "It can. Regular charging adds enough kWh to cross the high-consumption threshold, after which the residential subsidy is lost and the per-kWh price rises sharply. If you charge often, pair the charger with solar &mdash; the daytime generation offsets the charging and keeps consumption under the threshold."),
  ("Should I install a charger now or just prepare for one?",
   "Prepare at minimum. Conduit from the panel to the parking position plus a reserved panel way costs a fraction of a retrofit and takes the future installation from a chased-wall job to an afternoon. We do this by default on new builds, whether or not the owner currently drives an EV."),
  ("What should a hotel or condo complex install?",
   "Several lower-power bays sharing a managed supply, rather than two high-power ones: four 7 kW bays with load management usually need less service capacity, cost less to install and serve more overnight guests. Add per-session billing where charging is not complimentary, and keep the whole installation on a circuit that can be isolated during storm preparation."),
 ],
}

CONTENT["home-theater-installation-riviera-maya"] = {
 "title": "Home Theater Installation in the Riviera Maya: Humidity and Heat",
 "desc": "Designing a media room for 80% humidity and salt air: equipment protection, ventilation, acoustic treatment that does not mould, outdoor cinema, and 2026 costs.",
 "intro": [
   "A media room is one of the few parts of a tropical house where the climate fights the equipment directly. Projectors, AV receivers and amplifiers generate heat, dislike humidity, and sit in a sealed dark room. Speaker drivers use paper and foam that mould. Screens can grow spots. And every piece of it is exposed to the surge events that come with the grid here.",
   "None of this is a reason to skip a cinema room &mdash; we build them regularly, including in rental villas where a media room genuinely improves booking performance. It is a reason to design one for this climate: conditioned and ventilated, protected electrically, treated with materials that do not hold moisture, and specified so that a failure is a component swap rather than a rebuild."
 ],
 "sections": [
  ("Climate: the Three Things That Kill AV Here",
   """    <ul>
      <li><strong>Humidity.</strong> Sustained relative humidity above roughly 65% grows mould on speaker cones, foam surrounds, projector optics and screen surfaces, and corrodes board contacts. The fix is a room that is either conditioned continuously or dehumidified on a humidistat &mdash; not air conditioning that runs only when someone is watching a film.</li>
      <li><strong>Heat.</strong> Equipment racks in a closed cabinet reach temperatures that halve component life. Every rack we build is actively ventilated, with intake low, extraction high, and thermostatic fan control. A projector needs its own clear air path and a filter that is actually accessible for cleaning.</li>
      <li><strong>Surge.</strong> The peninsula's lightning season plus utility switching events make AV the most commonly destroyed equipment category in a coastal house. Whole-house protection at the panel plus a good rack-level conditioner is the minimum; for a serious system add an online UPS so the projector lamp and electronics shut down gracefully instead of being cut mid-cycle.</li>
    </ul>
    <p>One layout consequence: put the rack outside the room if you can &mdash; in a ventilated service closet with the cabling pre-run. It keeps heat and fan noise out of the room and makes service possible without moving furniture, and in a house that sits empty it can be isolated and kept dry on its own small circuit.</p>"""),
  ("Acoustic Treatment That Does Not Grow Mould",
   """    <p>The standard acoustic toolkit &mdash; open-cell foam, fabric-wrapped fibreglass, heavy carpet, upholstered seating &mdash; is a list of materials that hold moisture. Substitutions that work here:</p>
    <ul>
      <li><strong>Mineral wool instead of fibreglass batt</strong> inside panels, wrapped in a breathable acoustic fabric rather than a vinyl that traps damp behind it.</li>
      <li><strong>Slatted or perforated hardwood panels</strong> over a mineral wool cavity. They diffuse well, they suit the regional aesthetic, and they dry. Tzalam and chechen both work and we build them in our own shop.</li>
      <li><strong>Hard flooring with a removable rug,</strong> not fitted carpet. The rug can be lifted, cleaned and replaced; carpet glued to a slab in this climate is a long-term problem.</li>
      <li><strong>Leather or performance-fabric seating,</strong> not untreated cotton or linen upholstery, and set on legs so air moves underneath.</li>
      <li><strong>Solid-core doors with proper seals</strong> for isolation &mdash; which also helps keep the room's conditioned air where it belongs.</li>
    </ul>
    <p>Do the room geometry before the materials: a rectangular room with the seats out of the exact centre, speakers off the wall plane, and the first reflection points treated will outperform an untreated room with expensive electronics every time.</p>"""),
  ("Costs, and the Outdoor Cinema Alternative &mdash; 2026",
   """    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Scope</th><th>MXN</th><th>USD</th></tr></thead>
      <tbody>
        <tr><td>Media room pre-wire during construction (conduit, rack space, speaker runs)</td><td>$25,000&ndash;$70,000</td><td>$1,390&ndash;$3,890</td></tr>
        <tr><td>Living-room system: large TV, soundbar or 5.1, ventilated rack</td><td>$60,000&ndash;$180,000</td><td>$3,330&ndash;$10,000</td></tr>
        <tr><td>Dedicated cinema: projector, screen, 7.1, acoustic treatment, seating</td><td>$350,000&ndash;$900,000</td><td>$19,400&ndash;$50,000</td></tr>
        <tr><td>Premium cinema: 4K laser projector, immersive audio, custom joinery</td><td>$900,000&ndash;$2,500,000</td><td>$50,000&ndash;$139,000</td></tr>
        <tr><td>Outdoor cinema: exterior-rated projector or LED wall, weatherproof speakers</td><td>$120,000&ndash;$450,000</td><td>$6,670&ndash;$25,000</td></tr>
        <tr><td>Rack ventilation, surge protection and UPS (any of the above)</td><td>$20,000&ndash;$80,000</td><td>$1,110&ndash;$4,440</td></tr>
      </tbody>
    </table>
    </div>
    <p><strong>The outdoor option deserves a serious look.</strong> In a climate where the best hours are after sunset outdoors, a retractable screen under a palapa or pergola with weather-rated speakers often delivers more actual use than an indoor cinema &mdash; and it photographs extremely well for a rental listing. The equipment has to be genuinely exterior-rated (IP-rated speakers, a projector in a ventilated enclosure or an outdoor LED panel, marine-grade fixings) and it should be on a circuit that can be isolated before a storm.</p>
    <p>For new builds the decision that costs almost nothing now and a lot later is the pre-wire: conduit to the screen wall and speaker positions, a ventilated rack location, an HDMI-capable conduit path with a pull string, and a dedicated circuit. We run it on every house where a media room is even a possibility.</p>"""),
 ],
 "faq": [
  ("What does a home cinema cost in the Riviera Maya?",
   "A dedicated cinema room &mdash; projector, screen, 7.1 audio, acoustic treatment and seating &mdash; runs $350,000&ndash;$900,000 MXN ($19,400&ndash;$50,000 USD). A good living-room system is $60,000&ndash;$180,000. An outdoor cinema under a palapa is $120,000&ndash;$450,000. Pre-wiring during construction costs only $25,000&ndash;$70,000 and saves far more later."),
  ("How do I stop AV equipment from failing in the humidity?",
   "Keep the room conditioned or dehumidified continuously rather than only during use &mdash; sustained humidity above about 65% grows mould on speaker cones, foam surrounds and projector optics. Actively ventilate the equipment rack, ideally locating it outside the room in a service closet, and protect everything electrically with panel-level surge protection plus a rack conditioner or UPS."),
  ("What acoustic materials work in a tropical climate?",
   "Mineral wool inside panels rather than fibreglass batt, breathable acoustic fabric rather than vinyl, slatted or perforated hardwood panels over a mineral wool cavity, hard flooring with a removable rug instead of fitted carpet, and leather or performance-fabric seating on legs. Anything that holds moisture &mdash; open-cell foam, glued carpet, cotton upholstery &mdash; becomes a mould problem here."),
  ("Is an outdoor cinema practical on the coast?",
   "Very &mdash; it is often the better investment, because the pleasant hours here are after sunset outdoors, and it shows well in rental listings. It requires genuinely exterior-rated equipment: IP-rated speakers, a projector in a ventilated enclosure or an outdoor LED panel, marine-grade fixings, and a circuit that can be isolated before a storm."),
  ("Can you pre-wire a house for a cinema I will install later?",
   "Yes, and it is the single best-value decision. Conduit to the screen wall and speaker positions with pull strings, a ventilated rack location, a dedicated circuit and a clean HDMI path cost $25,000&ndash;$70,000 MXN during construction. Retrofitting the same routes through finished walls, tiled floors and a poured slab costs several times that and never looks as clean."),
 ],
}

CONTENT["stainless-steel-kitchen-riviera-maya"] = {
 "title": "Stainless Steel Kitchens in the Riviera Maya: 304 vs 316",
 "desc": "Why stainless suits outdoor kitchens on this coast, the grade that matters within sight of the sea, fabrication detail that shows years later, and costs.",
 "intro": [
   "Stainless steel is the only kitchen material that takes salt air, UV, tropical rain and commercial-grade use without a maintenance programme &mdash; which is why every serious outdoor kitchen and every restaurant kitchen here is built from it. It is also the material most often specified wrong, because the word &quot;stainless&quot; on a quote covers two alloys that behave completely differently a hundred metres from the beach.",
   "This guide covers the grade decision, how fabrication quality shows up years later, what outdoor and commercial stainless kitchens cost in 2026, and where stainless is the wrong answer and something else should be used instead."
 ],
 "sections": [
  ("304 vs 316: the Decision That Matters",
   """    <p>Both are austenitic stainless steels. The difference is molybdenum, which 316 has and 304 does not, and which is precisely what resists chloride attack &mdash; the mechanism by which sea air pits stainless.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Location</th><th>Recommended grade</th><th>Why</th></tr></thead>
      <tbody>
        <tr><td>Indoor kitchen, air conditioned</td><td>304</td><td>Ample; no chloride exposure of consequence</td></tr>
        <tr><td>Covered terrace, 1&ndash;5 km inland</td><td>304 body, 316 fixings and fasteners</td><td>Fasteners are the first thing to pit</td></tr>
        <tr><td>Beachfront or within ~1 km of the sea</td><td>316 throughout</td><td>Chloride-laden air and salt spray; 304 will pit and tea-stain</td></tr>
        <tr><td>Salt-system pool area</td><td>316 throughout</td><td>Saline splash and aerosol are aggressive</td></tr>
        <tr><td>Commercial kitchen, indoors</td><td>304, 1.2&ndash;1.5 mm on worktops</td><td>Hygiene and impact resistance drive the spec</td></tr>
      </tbody>
    </table>
    </div>
    <p>The surface finish also matters. A brushed No.4 finish hides use marks and is the practical choice for worktops; mirror finishes look spectacular and show every fingerprint and scratch. Bead-blasted and patterned finishes hide marks best but are harder to clean in a food environment.</p>
    <div class="alert alert-warning"><i class="bi bi-exclamation-triangle me-2"></i><strong>&quot;Tea staining&quot; is not rust and it is not a failure of the steel</strong> &mdash; it is a brown surface discolouration that appears on under-specified or contaminated stainless in marine air. It comes from using 304 where 316 belonged, from carbon-steel contamination during fabrication, or from never washing the surface. Specify the grade, insist on stainless-only tooling, and rinse exterior surfaces with fresh water periodically.</div>"""),
  ("Fabrication: Where Quality Actually Shows",
   """    <p>Two stainless kitchens can quote within 15% of each other and differ enormously in how they age. What separates them:</p>
    <ul>
      <li><strong>Passivation after welding.</strong> Welding destroys the passive chromium-oxide layer and leaves heat tint. Proper work pickles and passivates the welds; skipped, those welds are where corrosion starts.</li>
      <li><strong>No carbon-steel cross-contamination.</strong> Grinding discs, brushes and benches used on mild steel embed iron particles that rust in place and look like the stainless has failed. A shop that fabricates stainless properly keeps dedicated tooling.</li>
      <li><strong>Continuous welds, ground flush, on wet surfaces.</strong> Spot-welded seams and silicone-filled joints on a worktop trap water and food. That is a hygiene issue indoors and a corrosion initiation site outdoors.</li>
      <li><strong>Sheet thickness.</strong> 1.2&ndash;1.5 mm for worktops with proper sub-framing; thinner sheet drums, dents and telegraphs every fixing.</li>
      <li><strong>Radiused internal corners and integral coved splashbacks</strong> &mdash; the detail that makes a commercial kitchen cleanable and a residential one look built rather than assembled.</li>
      <li><strong>Drainage in exterior cabinetry.</strong> Outdoor stainless base units must drain and ventilate. A sealed exterior cabinet fills with condensation.</li>
    </ul>
    <p>We fabricate stainless in our own metal shop alongside the aluminium and ironwork, which is what makes grade control and passivation enforceable rather than a promise on a quote.</p>"""),
  ("Costs and When Not to Use Stainless &mdash; 2026",
   """    <div class="table-responsive">
    <table class="table table-bordered">
      <thead class="table-dark"><tr><th>Scope</th><th>MXN</th><th>USD</th></tr></thead>
      <tbody>
        <tr><td>Outdoor kitchen, 3 m, 304 body + 316 fixings, grill cut-out</td><td>$85,000&ndash;$160,000</td><td>$4,720&ndash;$8,890</td></tr>
        <tr><td>Outdoor kitchen, 3 m, full 316 (beachfront)</td><td>$130,000&ndash;$240,000</td><td>$7,220&ndash;$13,330</td></tr>
        <tr><td>Stainless worktop only, per linear metre, 1.5 mm</td><td>$6,500&ndash;$14,000</td><td>$360&ndash;$780</td></tr>
        <tr><td>Commercial kitchen fit-out, small restaurant (benches, sinks, shelving, hoods)</td><td>$350,000&ndash;$1,100,000</td><td>$19,400&ndash;$61,100</td></tr>
        <tr><td>Extraction hood with make-up air, restaurant</td><td>$90,000&ndash;$320,000</td><td>$5,000&ndash;$17,800</td></tr>
      </tbody>
    </table>
    </div>
    <p><strong>Where stainless is the wrong choice.</strong> On a fully sun-exposed worktop it becomes too hot to touch in the afternoon &mdash; pair it with a granite or porcelain landing area, or shade it. As a full wall of cabinet fronts in a residential kitchen it reads cold and shows every mark; combining a stainless worktop and appliance run with hardwood or lacquered fronts usually looks better and costs less. And for a restaurant front-of-house surface, porcelain slab or granite is often the more attractive, equally durable answer.</p>
    <p>For outdoor kitchens the combination we build most often is a 316 stainless carcass and worktop for everything structural and wet, with a granite or porcelain serving surface, hardwood or louvred aluminium door fronts for warmth, and a ventilated, drained base &mdash; all under a palapa or pergola so the equipment is shaded.</p>"""),
 ],
 "faq": [
  ("Should I use 304 or 316 stainless for an outdoor kitchen here?",
   "316 throughout if you are within about a kilometre of the sea or next to a salt-system pool. Further inland, a 304 body with 316 fixings and fasteners is a reasonable compromise, because fasteners pit first. Indoors, 304 is entirely adequate. The difference is molybdenum, which is what resists the chloride attack that causes pitting and tea staining."),
  ("What does a stainless outdoor kitchen cost?",
   "A 3 m outdoor kitchen with a grill cut-out runs $85,000&ndash;$160,000 MXN ($4,720&ndash;$8,890 USD) in 304 with 316 fixings, or $130,000&ndash;$240,000 in full 316 for a beachfront position. A stainless worktop alone is $6,500&ndash;$14,000 MXN per linear metre in 1.5 mm sheet."),
  ("Why is my stainless steel turning brown?",
   "That is tea staining &mdash; surface discolouration from chloride exposure on under-specified or contaminated stainless. The usual causes are 304 used where 316 was needed, iron particles embedded during fabrication by tooling also used on mild steel, or never rinsing the surface. It can often be cleaned and passivated, but the real fix is grade and fabrication discipline."),
  ("Do you build commercial restaurant kitchens?",
   "Yes &mdash; benches, sinks, shelving, extraction hoods and make-up air, fabricated in our own metal shop. A small restaurant fit-out typically runs $350,000&ndash;$1,100,000 MXN depending on scope, with extraction adding $90,000&ndash;$320,000. We coordinate it with the Civil Protection and health requirements that apply to the occupancy."),
  ("Is a fully stainless kitchen a good idea indoors?",
   "Rarely as the whole kitchen. A stainless worktop and appliance run is excellent; a full wall of stainless fronts reads cold, shows every fingerprint, and usually costs more than a better-looking mix. Most of our residential kitchens combine a stainless or stone worktop with lacquered or hardwood fronts."),
 ],
}

CONTENT["aluminum-windows-riviera-maya-guide"] = {
 "title": "Aluminium Windows in the Riviera Maya: Hurricane Ratings & Costs",
 "desc": "Thermal break, laminated vs tempered glass, impact ratings, anodised vs powder-coated frames and real 2026 window costs for coastal houses in Quintana Roo.",
 "intro": [
   "Windows are the most consequential single specification in a coastal house. They are the weakest point in the envelope during a hurricane, the largest heat gain in a climate where cooling is the dominant energy cost, and the component most likely to be quietly value-engineered down between quote and installation. A villa with excellent structure and cheap windows is a villa with an air-conditioning bill and a storm-season problem.",
   "This guide explains what the ratings actually mean, when laminated glass is required rather than preferred, how frame finishes behave in salt air, and what windows cost installed in 2026 across the corridor from Canc&uacute;n to Tulum."
 ],
 "sections": [
  ("Glass: Tempered, Laminated, Impact-Rated",
   """    <p>Three terms get used interchangeably in quotes here and they are not the same thing.</p>
    <ul>
      <li><strong>Tempered (templado):</strong> heat-treated so it breaks into small blunt granules. It is a safety requirement in many locations &mdash; doors, low glazing, glass near wet areas &mdash; but it offers no storm protection. Struck by debris, it shatters completely and the opening is lost.</li>
      <li><strong>Laminated:</strong> two or more glass plies bonded to a PVB or SentryGlas interlayer. Struck by debris it cracks but stays in the frame, which keeps the building envelope closed. It also cuts UV and improves acoustics noticeably.</li>
      <li><strong>Impact-rated assembly:</strong> a tested combination of laminated glass, frame and anchorage, certified to resist a missile impact followed by pressure cycling. The rating belongs to the whole assembly, not the glass alone &mdash; laminated glass in a weak frame with short anchors is not impact-rated.</li>
    </ul>
    <p>For most houses we build, the sensible pattern is laminated glass on all exposed elevations plus either impact-rated assemblies or shutters on the largest openings. That keeps the envelope intact in a storm, and it is worth noting that an intact envelope is what prevents the internal pressurisation that lifts roofs. On top of that, low-E coatings and a thermal break in the frame materially cut cooling load &mdash; in this climate the solar heat gain coefficient deserves as much attention as the U-value.</p>"""),
  ("Frames and Finishes in Salt Air",
   """    <p>Aluminium is the right frame material here &mdash; it does not rot, does not feed termites and carries large glass sizes &mdash; but the finish determines its life.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Finish</th><th>Coastal behaviour</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>Anodised (class 2, 20&ndash;25 &micro;m)</td><td>Excellent</td><td>The benchmark for beachfront; colour range limited</td></tr>
        <tr><td>Powder coat, marine-rated pretreatment</td><td>Very good</td><td>Any colour; demands proper chromate/chrome-free pretreatment</td></tr>
        <tr><td>Standard architectural powder coat</td><td>Chalks and blisters at edges within a few years on the beach</td><td>Fine 5+ km inland, not on the shore</td></tr>
        <tr><td>Mill finish / unfinished</td><td>Pits and whitens</td><td>Service and utility openings only</td></tr>
      </tbody>
    </table>
    </div>
    <p>Two details worth insisting on. First, <strong>stainless hardware and fasteners &mdash; 316 on the coast.</strong> Aluminium frames with plated-steel screws fail at the screws, and galvanic corrosion between dissimilar metals accelerates it. Second, <strong>thermal break</strong> on air-conditioned rooms: an unbroken aluminium frame conducts heat straight into the room and condenses on the interior face in the humid season, which is how mould appears on window reveals.</p>"""),
  ("Installed Costs and the Installation Itself &mdash; 2026",
   """    <div class="table-responsive">
    <table class="table table-bordered">
      <thead class="table-dark"><tr><th>Specification</th><th>MXN / m&sup2;</th><th>USD / m&sup2;</th></tr></thead>
      <tbody>
        <tr><td>Standard aluminium, 6 mm tempered, no thermal break</td><td>$2,600&ndash;$4,500</td><td>$145&ndash;$250</td></tr>
        <tr><td>Aluminium, laminated glass, marine powder coat</td><td>$4,800&ndash;$8,500</td><td>$267&ndash;$472</td></tr>
        <tr><td>Thermal-break aluminium, laminated low-E, anodised</td><td>$8,000&ndash;$14,000</td><td>$444&ndash;$778</td></tr>
        <tr><td>Impact-rated assembly, certified system</td><td>$12,000&ndash;$22,000</td><td>$667&ndash;$1,222</td></tr>
        <tr><td>Large sliding or lift-and-slide door systems</td><td>$14,000&ndash;$30,000</td><td>$778&ndash;$1,667</td></tr>
        <tr><td>Aluminium roller shutters (persianas) as an alternative</td><td>$3,500&ndash;$7,000</td><td>$194&ndash;$389</td></tr>
      </tbody>
    </table>
    </div>
    <p>On a 250 m&sup2; villa with generous glazing, the gap between the cheapest and the well-specified option is commonly $400,000&ndash;$900,000 MXN &mdash; which is exactly why this line gets cut when a budget tightens, and exactly the wrong place to cut it.</p>
    <p><strong>Installation decides whether any of it works.</strong> The anchorage has to go into structural concrete or block with the specified anchor type and spacing, not into plaster. The perimeter needs a proper sealant joint over a backer rod, with a drained and vented sill so wind-driven rain that gets past the outer seal escapes outward instead of running into the wall. And the opening must be square and the frame not distorted by shimming &mdash; a racked frame never seals again. We fabricate and install our own aluminium, which means the opening, the anchor and the sealant detail are one trade's responsibility rather than a dispute between two.</p>"""),
 ],
 "faq": [
  ("What do good hurricane-resistant windows cost in the Riviera Maya?",
   "Thermal-break aluminium with laminated low-E glass and an anodised finish runs $8,000&ndash;$14,000 MXN per m&sup2; installed ($444&ndash;$778 USD). Certified impact-rated assemblies are $12,000&ndash;$22,000 per m&sup2;. Standard aluminium with tempered glass starts around $2,600 but provides no storm protection. Roller shutters over ordinary glazing at $3,500&ndash;$7,000 per m&sup2; are a cost-effective middle path."),
  ("Is tempered glass enough for hurricane season?",
   "No. Tempered glass is a safety specification &mdash; it breaks into blunt granules rather than shards &mdash; but it offers no debris resistance, and when it fails the opening is completely lost. Laminated glass cracks and stays in the frame, keeping the envelope closed, which is what prevents the internal pressurisation that lifts roofs."),
  ("Anodised or powder-coated frames for a beachfront house?",
   "Anodised, class 2 at 20&ndash;25 microns, is the benchmark on the shoreline. A marine-rated powder coat with proper pretreatment is very good and gives you any colour. A standard architectural powder coat chalks and blisters at the edges within a few years in beachfront exposure, though it is perfectly fine several kilometres inland."),
  ("Do I need a thermal break in a tropical climate?",
   "Yes, on any air-conditioned room. An unbroken aluminium frame conducts heat directly inward and its interior face condenses in the humid season, which is where mould on window reveals comes from. Combined with a low-E coating, the thermal break is one of the cheapest reductions in cooling load available."),
  ("Can windows be retrofitted into an existing house?",
   "Yes, and it is common work for us in older villas and condos &mdash; but the value is in the installation, not just the unit. Retrofit requires opening back to structure for proper anchorage, a drained and vented sill, and a correct sealant joint. Slotting a better window into a bad opening reproduces the original leak with more expensive glass."),
 ],
}

CONTENT["iron-railing-balcony-riviera-maya"] = {
 "title": "Railings and Balconies in the Riviera Maya: Code and Corrosion",
 "desc": "Height and load requirements, why powder-coated iron fails on the coast, glass and cable options compared, and costs per linear metre.",
 "intro": [
   "A railing is a life-safety component that people shop for as decoration. It has to resist a horizontal load applied by a crowd leaning on it, it has to keep a child from passing through or climbing it, and on this coast it has to do both after a decade in salt air. Those three requirements, in that order, should drive the material choice &mdash; and they routinely do not.",
   "This guide covers the dimensional and load rules we build to, an honest comparison of iron, aluminium, stainless, glass and cable in a marine environment, and installed costs per linear metre for 2026."
 ],
 "sections": [
  ("Dimensions and Loads",
   """    <p>The figures below are the ones we design to in Quintana Roo; municipal reviews and hotel Civil Protection reviews are where they get checked in practice, and a design committee in a gated community may impose more.</p>
    <ul>
      <li><strong>Height:</strong> 90 cm minimum for residential guarding, and 1.05&ndash;1.10 m for terraces, roof terraces, commercial and hotel applications. Above roughly 10 m we go to 1.10 m as a matter of course.</li>
      <li><strong>Gap:</strong> no opening that passes a 10 cm sphere &mdash; the standard child-safety criterion. This is where decorative horizontal designs run into trouble.</li>
      <li><strong>No climbable geometry</strong> in a family or hotel setting: horizontal rails and wide bottom rails form a ladder. Vertical balusters, glass or tensioned cable at close spacing avoid it.</li>
      <li><strong>Horizontal load:</strong> design for a distributed load applied at the top rail, plus a point load. In practice the failure is never the rail &mdash; it is the anchorage.</li>
      <li><strong>Anchorage:</strong> into structural concrete with the specified embedment, or through-bolted with plates. Expansion anchors into a thin slab edge or into block are the most common defect we find on inspections.</li>
    </ul>
    <p>On a rental property, this is not merely a code question. A guest injury involving a non-compliant railing is the liability that insurers look at hardest.</p>"""),
  ("Material Comparison in Marine Air",
   """    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Material</th><th>Coastal performance</th><th>Maintenance</th><th>Best for</th></tr></thead>
      <tbody>
        <tr><td>Painted mild steel / wrought iron</td><td>Poor to fair</td><td>Rust treatment and repaint every 2&ndash;4 years</td><td>Inland only, or where the look is essential and upkeep accepted</td></tr>
        <tr><td>Hot-dip galvanised steel, then powder coated (duplex)</td><td>Good</td><td>Inspect coating at welds and fixings</td><td>Long spans, ornate work, structural balconies</td></tr>
        <tr><td>Powder-coated aluminium</td><td>Very good</td><td>Wash</td><td>The default residential choice on the coast</td></tr>
        <tr><td>316 stainless</td><td>Excellent</td><td>Rinse to avoid tea staining</td><td>Beachfront, pool surrounds, contemporary design</td></tr>
        <tr><td>Structural glass with stainless or aluminium fixings</td><td>Excellent</td><td>Clean glass; check gaskets</td><td>View-critical terraces</td></tr>
        <tr><td>Tensioned stainless cable</td><td>Very good in 316</td><td>Re-tension periodically</td><td>Contemporary look &mdash; watch the climbability rule</td></tr>
      </tbody>
    </table>
    </div>
    <p>The specific trap here is <strong>painted iron on a beachfront balcony</strong>. It looks right for a colonial or hacienda aesthetic, and within three years it is bleeding rust stains down a white facade. If the design demands iron, galvanise it first and then powder coat it &mdash; the duplex system, which roughly doubles or triples the life of either treatment alone &mdash; and use 316 stainless fasteners so the fixings do not become the weak point. Where that is not possible, aluminium detailed to look like ironwork is an honest substitute we build often.</p>"""),
  ("Costs Per Linear Metre and Glass Detailing &mdash; 2026",
   """    <div class="table-responsive">
    <table class="table table-bordered">
      <thead class="table-dark"><tr><th>Railing type</th><th>MXN / linear metre</th><th>USD / linear metre</th></tr></thead>
      <tbody>
        <tr><td>Painted steel, simple vertical balusters</td><td>$1,800&ndash;$3,500</td><td>$100&ndash;$194</td></tr>
        <tr><td>Galvanised + powder-coated steel</td><td>$3,200&ndash;$6,000</td><td>$178&ndash;$333</td></tr>
        <tr><td>Powder-coated aluminium</td><td>$3,000&ndash;$6,500</td><td>$167&ndash;$361</td></tr>
        <tr><td>316 stainless, tube and post</td><td>$6,500&ndash;$13,000</td><td>$361&ndash;$722</td></tr>
        <tr><td>Laminated glass with stainless standoffs or channel</td><td>$7,000&ndash;$16,000</td><td>$389&ndash;$889</td></tr>
        <tr><td>Frameless structural glass, minimal hardware</td><td>$12,000&ndash;$25,000</td><td>$667&ndash;$1,389</td></tr>
      </tbody>
    </table>
    </div>
    <p><strong>Glass railings on the coast, specified properly:</strong> laminated glass rather than monolithic tempered (so a break does not leave an open edge), a base channel or standoffs in 316, drainage designed into the channel so it does not become a salt-water trough, and a hand rail on top wherever the glass is the primary guard and a code review is likely. Frameless glass is the most maintenance-friendly view solution here &mdash; nothing corrodes, nothing needs painting &mdash; provided the fixings are the right alloy.</p>
    <p>We fabricate aluminium, steel and stainless railings in our own metal shop and install them ourselves, which keeps the anchorage detail with the same trade that made the railing. That matters, because on the coastal failures we are called to assess, the railing is usually still sound and the fixings are not.</p>"""),
 ],
 "faq": [
  ("How high does a balcony railing have to be?",
   "Ninety centimetres minimum for residential guarding, and 1.05&ndash;1.10 m for terraces, roof terraces and any commercial or hotel application. No opening may pass a 10 cm sphere, and the geometry must not be climbable &mdash; which rules out widely spaced horizontal rails in family and hotel settings."),
  ("What does a balcony railing cost per linear metre?",
   "Powder-coated aluminium runs $3,000&ndash;$6,500 MXN per linear metre ($167&ndash;$361 USD); galvanised and powder-coated steel $3,200&ndash;$6,000; 316 stainless $6,500&ndash;$13,000; laminated glass with stainless fixings $7,000&ndash;$16,000; frameless structural glass $12,000&ndash;$25,000. Painted mild steel is cheapest at $1,800&ndash;$3,500 and the shortest-lived on the coast."),
  ("Why does my wrought iron railing rust so fast?",
   "Because painted mild steel in chloride-laden air corrodes from any coating breach, and the coating always breaches at welds, edges and fixings first. If the design needs ironwork, galvanise it and then powder coat it &mdash; a duplex system &mdash; and use 316 stainless fasteners. Otherwise aluminium detailed to look like ironwork gives the same appearance without the rust streaks down the facade."),
  ("Are glass railings a good idea near the sea?",
   "Yes, and they are often the lowest-maintenance option, because glass does not corrode. Specify laminated rather than monolithic tempered glass, 316 stainless standoffs or a drained base channel so salt water cannot pool in it, and a top hand rail where the glass is the primary guard. The hardware alloy is what determines the life of the installation."),
  ("Can you replace railings on an existing condo or villa?",
   "Regularly &mdash; it is one of our most common renovation items on coastal properties, and we usually find the railing itself is sound while the anchorage has corroded. Replacement means opening back to structural concrete, repairing any spalled or carbonated concrete at the slab edge, and re-anchoring properly. Bolting a new railing to a deteriorated slab edge just resets the clock on the same failure."),
 ],
}

CONTENT["security-gates-riviera-maya"] = {
 "title": "Security Gates in the Riviera Maya: Automation, Power Cuts, Costs",
 "desc": "Automatic gate operators that survive salt air and outages, sliding vs swing vs cantilever for local lots, access control for rentals, and 2026 installed costs.",
 "intro": [
   "An automatic gate is the most-used moving part on a property and the one most exposed to everything this climate does: salt air on the hardware, heat in the controller, lightning on the low-voltage lines, and power cuts that leave a heavy gate closed with the owner outside it. Add rentals &mdash; where strangers need access on a schedule &mdash; and access control becomes as important as the gate.",
   "Below: choosing the gate type for the lot rather than the catalogue, what to demand of the operator and controller in a marine environment, how to handle outages properly, access options for rental and multi-unit properties, and 2026 installed costs."
 ],
 "sections": [
  ("Gate Type: Match It to the Lot",
   """    <ul>
      <li><strong>Sliding (single-leaf, track or cantilever):</strong> the default on narrow urban lots in Playa del Carmen and Canc&uacute;n where a swing leaf would sweep into the street or the driveway. Track sliders are cheaper; a ground track in this climate fills with sand and debris and needs sweeping. Cantilever slides avoid the track entirely and are the better buy on a sandy or unpaved approach.</li>
      <li><strong>Swing (double-leaf):</strong> the classic residential look, needs clear sweep space inside the property and a level approach. Wind load matters &mdash; a solid-panel swing leaf on an exposed beachfront lot is a sail, and either the leaf gets perforated or the operator gets oversized.</li>
      <li><strong>Barrier arm plus pedestrian gate:</strong> the right answer for a condo or hotel entrance with attendant traffic, far faster in operation and cheaper to maintain than a full vehicle gate cycling hundreds of times a day.</li>
      <li><strong>Pedestrian side gate:</strong> always specify one. It is the thing that saves you during an outage or an operator failure, and it lets deliveries and staff in without cycling the vehicle gate.</li>
    </ul>
    <p>Material follows the same logic as railings: powder-coated aluminium for low maintenance, galvanised-then-coated steel where the design is heavy or ornate, 316 stainless hardware in every case. Solid hardwood-clad leaves look superb and are heavier than clients expect &mdash; which changes the operator class and the post foundations, so decide the cladding before the structure is designed.</p>"""),
  ("Operators, Corrosion and Power Cuts",
   """    <p>The operator is where a gate installation either lasts or becomes an annual repair line.</p>
    <ul>
      <li><strong>Duty class matched to real cycles.</strong> A residential operator on a rental property with daily guest turnover is being used commercially. Specify the next class up; it is a small premium against a burned-out motor.</li>
      <li><strong>Enclosure and siting.</strong> The controller belongs in a sealed, gasketed enclosure, shaded, above flood level, with cable entries at the bottom and drip loops. Sun-baked controller boxes are the most common electronic failure here, and water entering a top-mounted gland is the second.</li>
      <li><strong>Surge protection on the mains and the low-voltage runs.</strong> A long buried loop or photocell cable is an excellent lightning antenna. Protect both ends.</li>
      <li><strong>Battery backup is not optional.</strong> Specify an operator with battery backup sized for at least 10&ndash;20 cycles, or a solar-assisted unit. The alternative is a manual release, which you should also insist on, and which means getting out of the car in the rain.</li>
      <li><strong>Safety devices, properly installed:</strong> photocells at two heights, obstruction sensing in the operator, and for a sliding gate a safety edge. On rental and commercial properties, treat these as mandatory &mdash; an automatic gate is a heavy powered machine that the public interacts with.</li>
      <li><strong>Corrosion on the moving parts.</strong> Stainless or sealed bearings, galvanised or stainless chain and rack, and a lubrication schedule. A gate that grinds is a gate whose operator is about to fail.</li>
    </ul>"""),
  ("Access Control and Costs &mdash; 2026",
   """    <p>For an owner-occupied house, remotes plus a keypad are enough. For a rental, a vacation property or a multi-unit building, the requirement is different: give access to a stranger for a defined window without handing over a physical credential and without the owner being present.</p>
    <ul>
      <li><strong>App or cloud-based controller</strong> with time-limited guest access and an event log &mdash; the standard for short-term rentals now, and worth confirming that it degrades gracefully when the internet drops.</li>
      <li><strong>GSM intercom</strong> that calls the owner's or manager's phone, which works when the property's internet does not.</li>
      <li><strong>Keypad with rotating codes</strong> as the simple, robust fallback. Choose a stainless or properly sealed unit; standard keypads corrode.</li>
      <li><strong>Camera at the gate</strong> on the same power and surge protection, positioned to read plates and faces, recording locally as well as to cloud.</li>
    </ul>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Scope</th><th>MXN</th><th>USD</th></tr></thead>
      <tbody>
        <tr><td>Sliding gate, aluminium, 4 m, residential operator, remotes</td><td>$55,000&ndash;$110,000</td><td>$3,060&ndash;$6,110</td></tr>
        <tr><td>Double swing gate, galvanised + coated steel, 4.5 m, operators</td><td>$70,000&ndash;$150,000</td><td>$3,890&ndash;$8,330</td></tr>
        <tr><td>Cantilever slider, 5&ndash;6 m, commercial-duty operator</td><td>$130,000&ndash;$280,000</td><td>$7,220&ndash;$15,560</td></tr>
        <tr><td>Hardwood-clad gate with steel frame (add)</td><td>+$35,000&ndash;$120,000</td><td>+$1,940&ndash;$6,670</td></tr>
        <tr><td>Access control: app controller, keypad, GSM intercom, camera</td><td>$25,000&ndash;$75,000</td><td>$1,390&ndash;$4,170</td></tr>
        <tr><td>Battery backup and surge protection package</td><td>$12,000&ndash;$35,000</td><td>$670&ndash;$1,940</td></tr>
      </tbody>
    </table>
    </div>
    <p>The post foundations and the electrical supply are part of the job, not extras: a heavy gate needs a properly sized reinforced foundation to each post, and the operator needs a dedicated protected circuit run to it. Retrofitting automation onto an existing gate is common work and usually straightforward &mdash; provided the gate itself is straight, the hinges or rollers are sound, and the posts can take the loads the operator will apply.</p>"""),
 ],
 "faq": [
  ("What does an automatic gate cost in the Riviera Maya?",
   "An aluminium sliding gate about 4 m wide with a residential operator and remotes runs $55,000&ndash;$110,000 MXN ($3,060&ndash;$6,110 USD). A double swing gate in galvanised and coated steel is $70,000&ndash;$150,000. A commercial-duty cantilever slider is $130,000&ndash;$280,000. Access control adds $25,000&ndash;$75,000 and a battery-backup plus surge package $12,000&ndash;$35,000."),
  ("What happens to an automatic gate during a power cut?",
   "With battery backup, it keeps working for at least 10&ndash;20 cycles &mdash; which is why we specify it as standard rather than as an option, given how often the grid drops here in the wet season. Always have a manual release as well, and always build a pedestrian side gate: it is what gets you onto the property when the operator itself fails."),
  ("Sliding or swing gate for a lot in Playa del Carmen?",
   "Sliding on a narrow urban lot, because a swing leaf sweeps into the street or eats the driveway. A cantilever slider is better than a track slider on sandy or unpaved approaches, since ground tracks fill with debris. Swing gates suit larger properties with clear internal sweep space, but a solid leaf on an exposed beachfront lot acts as a sail and needs either perforation or a larger operator."),
  ("How do I give rental guests access without handing over a remote?",
   "An app or cloud controller with time-limited guest codes and an event log, backed by a keypad for when the internet drops and a GSM intercom that calls the manager's phone over the mobile network. Add a gate camera positioned to read plates and faces, recording locally as well as to the cloud."),
  ("Can you automate my existing gate?",
   "Usually yes. The gate has to be straight and running freely, the hinges or rollers sound, and the posts capable of taking the loads the operator will apply &mdash; we check those first, because automating a sagging gate just breaks it faster. We also add the protected circuit, surge protection, safety photocells and battery backup as part of the conversion."),
 ],
}

CONTENT["steel-structure-construction-riviera-maya"] = {
 "title": "Steel Structures in the Riviera Maya: Corrosion and Costs",
 "desc": "When steel beats concrete on this coast, galvanising vs paint systems, hurricane and seismic design loads, and costs per m² for warehouses and mezzanines.",
 "intro": [
   "Concrete is the default structural material on the peninsula for good reasons: it is locally produced, the labour force is deeply skilled in it, and a reinforced concrete frame is inherently mass-resistant to hurricane loads. Steel earns its place where concrete struggles &mdash; long clear spans, fast programmes, industrial buildings, mezzanines inserted into existing structures, and roofs with large cantilevers.",
   "The catch is corrosion. Structural steel in a marine atmosphere is on a clock, and the only question is whether your protection system is specified for the exposure or for a drawing office three hundred kilometres inland. This guide covers where steel is the right choice, what protection system to specify by distance from the sea, how hurricane and seismic loads shape the design, and 2026 costs."
 ],
 "sections": [
  ("Where Steel Beats Concrete Here",
   """    <ul>
      <li><strong>Clear spans over about 12 m:</strong> warehouses, workshops, event halls, padel and sports covers. A steel portal frame or truss is lighter, faster and usually cheaper than the concrete equivalent at these spans.</li>
      <li><strong>Industrial buildings (naves industriales):</strong> the standard solution across the corridor, with insulated sandwich panel or metal deck roofing.</li>
      <li><strong>Mezzanines and additions inside existing buildings:</strong> steel goes in through an opening and gets bolted up, where concrete needs formwork, curing time and a way to bring wet concrete inside.</li>
      <li><strong>Long cantilevers and large openings</strong> in residential architecture &mdash; a floating roof plane over a terrace, a wide glazed corner.</li>
      <li><strong>Programme-driven projects:</strong> fabrication happens off-site while foundations are poured, which can take weeks out of a schedule.</li>
    </ul>
    <p>Where concrete stays better: everything below grade or in contact with soil, pool structures, anything with heavy acoustic or thermal mass requirements, and typical residential floor plates in the 5&ndash;8 m span range, where a concrete slab is simply cheaper here. Many of our projects are hybrids &mdash; concrete frame and slabs with steel where the span or the cantilever demands it.</p>"""),
  ("Corrosion Protection by Exposure",
   """    <p>Specify the protection system by distance from the coast and by whether the steel is exposed. This is the single most important decision in a steel project here, and it is where cheap tenders are cheap.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Exposure</th><th>System</th><th>Expected service before major maintenance</th></tr></thead>
      <tbody>
        <tr><td>Interior, dry, air conditioned</td><td>Primer + alkyd or epoxy topcoat</td><td>15&ndash;25 years</td></tr>
        <tr><td>Interior, unconditioned (warehouse), 5+ km inland</td><td>Zinc-rich primer + epoxy</td><td>12&ndash;20 years</td></tr>
        <tr><td>Exterior, 1&ndash;5 km from the sea</td><td>Hot-dip galvanised, or zinc-rich + epoxy + polyurethane (3-coat)</td><td>15&ndash;25 years</td></tr>
        <tr><td>Exterior, within ~1 km / beachfront</td><td>Hot-dip galvanised <em>plus</em> a duplex paint system</td><td>25&ndash;35 years</td></tr>
        <tr><td>Splash zone, pool structures, pier work</td><td>Duplex plus 316 stainless for fixings and exposed details</td><td>Inspect on a defined cycle</td></tr>
      </tbody>
    </table>
    </div>
    <p>Three details matter as much as the coating. <strong>Design out the traps:</strong> no upward-facing channels, no unsealed hollow sections, no crevices that hold water &mdash; drain and vent every closed member. <strong>Protect the connections:</strong> bolts, plates and welds are where corrosion starts, so galvanised or stainless fasteners and touch-up of site welds are mandatory, not tidy-up. <strong>Isolate dissimilar metals:</strong> aluminium cladding directly against galvanised steel with a wet interface corrodes galvanically; use isolating washers and tapes.</p>
    <div class="alert alert-warning"><i class="bi bi-exclamation-triangle me-2"></i><strong>Galvanising has to be designed in.</strong> Members must fit the galvaniser's bath, vent and drain holes have to be on the shop drawings, and post-galvanising site welds need a compatible repair system. Deciding to galvanise after fabrication rarely works out.</div>"""),
  ("Design Loads and Cost Per Square Metre &mdash; 2026",
   """    <p>Quintana Roo combines a high wind-load region with a modest but non-zero seismic requirement, and steel buildings are governed by wind. Two consequences dominate design: <strong>uplift</strong> on light roofs, which makes holding-down details and roof-sheet fixing patterns critical, and <strong>the envelope</strong> &mdash; a failed door or window pressurises the building and turns a cladding problem into a structural one. Large roller doors on industrial buildings are the usual weak point, and specifying a wind-rated door is much cheaper than replacing a roof.</p>
    <div class="table-responsive">
    <table class="table table-bordered">
      <thead class="table-dark"><tr><th>Structure</th><th>MXN / m&sup2;</th><th>USD / m&sup2;</th></tr></thead>
      <tbody>
        <tr><td>Steel portal-frame warehouse shell, 15&ndash;25 m span, metal roof</td><td>$4,500&ndash;$8,500</td><td>$250&ndash;$472</td></tr>
        <tr><td>Same with insulated sandwich panel roof and walls</td><td>$7,000&ndash;$13,000</td><td>$389&ndash;$722</td></tr>
        <tr><td>Steel mezzanine inside an existing building</td><td>$5,500&ndash;$11,000</td><td>$306&ndash;$611</td></tr>
        <tr><td>Architectural exposed steel in a residential project</td><td>$9,000&ndash;$20,000</td><td>$500&ndash;$1,110</td></tr>
        <tr><td>Duplex protection premium over standard paint</td><td>+8&ndash;18% of steel cost</td><td>&mdash;</td></tr>
      </tbody>
    </table>
    </div>
    <p>Foundations are separate and are not trivial: the limestone here often gives excellent bearing at shallow depth, which is good news, but uplift on a light steel building means the pad has to hold the frame down as well as up, and cavities in the karst have to be found before they are built over. That is a soil-study question, answered before the steel is ordered.</p>"""),
 ],
 "faq": [
  ("When is steel a better choice than concrete in the Riviera Maya?",
   "For clear spans beyond about 12 m &mdash; warehouses, workshops, event and sports covers &mdash; for mezzanines inserted into existing buildings, for long cantilevers in residential architecture, and where the programme matters, since steel is fabricated off-site while foundations are poured. Concrete remains better below grade, for pool structures, and for ordinary residential floor spans."),
  ("What corrosion protection does structural steel need on the coast?",
   "Within about a kilometre of the sea, hot-dip galvanising plus a duplex paint system. One to five kilometres inland, galvanising or a three-coat zinc-rich/epoxy/polyurethane system. Inside an unconditioned building well inland, zinc-rich primer plus epoxy. In every case the fasteners, plates and site welds need the same attention as the members &mdash; that is where corrosion starts."),
  ("How much does a steel warehouse cost per square metre?",
   "A portal-frame shell with a metal roof at 15&ndash;25 m span runs $4,500&ndash;$8,500 MXN per m&sup2; ($250&ndash;$472 USD). With insulated sandwich panel roof and walls it is $7,000&ndash;$13,000. Foundations are separate, and duplex corrosion protection adds 8&ndash;18% to the steel cost &mdash; which is the cheapest durability money you will spend on the coast."),
  ("How are hurricane loads handled in a steel building?",
   "Wind governs the design, and uplift governs the details: holding-down bolts and pad weights sized to resist the frame lifting, roof-sheet fixing patterns tightened at edges and corners, and a wind-rated roller door on industrial buildings. The envelope is structural here &mdash; a door that fails pressurises the building and can take the roof with it."),
  ("Do you design and build steel structures, or only erect them?",
   "Both. We handle the structural design and the corrosion specification, coordinate fabrication, and erect on site, including the foundation design once the soil study is in. Getting the protection system, the venting and drainage for galvanising, and the connection details onto the shop drawings before fabrication is the part that determines how the building ages."),
 ],
}

CONTENT["structural-engineering-riviera-maya"] = {
 "title": "Structural Engineering in the Riviera Maya: Wind and Karst",
 "desc": "How structures are designed for Quintana Roo: hurricane wind loads, limestone and cenote risk, concrete cover against chloride attack, and the DRO's role.",
 "intro": [
   "Structural engineering here is shaped by three local facts that override most imported design habits. The region sits in one of Mexico's highest wind-load zones. The ground is karst limestone, which can give excellent bearing at shallow depth and then open into a cavity two metres away. And the atmosphere carries chlorides that attack reinforcement through the concrete cover, which makes durability detailing a structural issue rather than a finishing one.",
   "This is what a competent structural design addresses in Quintana Roo, why the geotechnical study comes before the structural design rather than alongside it, how durability is specified, and where the Director Responsable de Obra fits into the legal chain of responsibility."
 ],
 "sections": [
  ("Wind Governs, Not Earthquakes",
   """    <p>Most of the peninsula is in a low seismic zone, and residential structures here are governed by wind. The design consequences are specific:</p>
    <ul>
      <li><strong>Uplift, not just lateral push.</strong> Light roofs, wide eaves, palapas, pergolas and canopies all want to lift. Continuous load paths from the roof plane down into the foundation &mdash; straps, dowels, ring beams, holding-down details &mdash; are the core of the design.</li>
      <li><strong>Edges and corners take the worst of it.</strong> Pressure coefficients are far higher at roof edges, corners and parapets than over the field of the roof, which is why fixing patterns tighten in those zones and why a uniform fixing schedule across a whole roof is a red flag.</li>
      <li><strong>The envelope is structural.</strong> If a window or a large door fails, the building pressurises internally and the roof is then being pushed from inside as well as lifted from outside. This is why laminated or impact-rated glazing on large openings is a structural decision.</li>
      <li><strong>Reinforced concrete frames with masonry infill,</strong> the regional norm, perform well under these loads &mdash; provided the confinement steel, the ring beam (cadena de cerramiento) and the column-to-beam connections are detailed and actually built as drawn.</li>
      <li><strong>Cantilevers and slender roof planes</strong> &mdash; the signature move in contemporary Tulum architecture &mdash; need explicit uplift and deflection analysis, not a rule of thumb.</li>
    </ul>"""),
  ("Karst Ground: the Geotechnical Study Comes First",
   """    <p>The limestone shelf that the corridor sits on is soluble, which means it is riddled with dissolution features: cenotes, caves, and cavities filled with soft sediment. Bearing capacity at shallow depth is often very good &mdash; better than clients from soft-soil regions expect &mdash; and then a probe two metres to one side finds a void.</p>
    <ul>
      <li><strong>A soil study (mec&aacute;nica de suelos) with borings or probes across the actual footprint</strong> is the prerequisite for any structural design here. A single borehole at the centre of the lot does not characterise karst.</li>
      <li><strong>Where cavities are found,</strong> the responses are localised: bridge them with a stiffened raft or grade beams, fill and grout, relocate footings, or in extreme cases move the building on the lot. All of these are cheap compared to discovering the void after the slab is poured.</li>
      <li><strong>Shallow water table near the coast</strong> affects excavations, cisterns, pool shells and any basement &mdash; buoyancy and dewatering become design items, and a pool shell can float if it is emptied at the wrong time.</li>
      <li><strong>Drainage into the aquifer is regulated.</strong> Absorption wells (pozos de absorci&oacute;n) and treatment requirements are part of the design, and in the Tulum and Puerto Morelos environmental files they are examined closely, because what goes into the karst reaches the reef.</li>
    </ul>
    <p>This is the single most common false economy we encounter: a client skips the $25,000&ndash;$60,000 MXN soil study to save time, and then pays several times that in foundation redesign, or builds over a cavity and pays vastly more.</p>"""),
  ("Durability, Concrete Cover, and Who Signs",
   """    <p><strong>Chloride attack is the long-term structural risk on this coast.</strong> Salt reaches the reinforcement through the concrete cover, depassivates the steel, and the corrosion product expands and spalls the concrete &mdash; the brown-stained, flaking slab edges and columns visible on older coastal buildings all over the Caribbean. Design against it:</p>
    <ul>
      <li><strong>Increase the cover</strong> on exposed elements &mdash; slab edges, columns, balconies, roof beams &mdash; relative to inland practice, and control it on site with spacers, because cover achieved is what matters, not cover drawn.</li>
      <li><strong>Lower water/cement ratio and denser mixes</strong> reduce permeability, which is the actual mechanism of protection. Specify strength <em>and</em> durability class.</li>
      <li><strong>Epoxy-coated or stainless reinforcement</strong> in genuinely aggressive positions: splash zones, beachfront balconies, pool structures.</li>
      <li><strong>Cure properly.</strong> In 32&deg;C heat with wind, concrete cured badly for the first week is permanently more permeable. This is free to do right and expensive to fix.</li>
      <li><strong>Detail for water to leave.</strong> Drips, throats, falls and no upward-facing traps &mdash; standing water on a balcony edge is a chloride pump.</li>
    </ul>
    <p><strong>Who is responsible.</strong> In Quintana Roo municipalities the construction licence requires a <em>Director Responsable de Obra</em> &mdash; a registered professional who signs for the project and the works and carries legal responsibility for compliance. The structural design sits under that signature, as do the plans submitted for the licence. When you engage us, the structural design, the DRO and the site execution are coordinated as one chain of responsibility instead of three parties pointing at each other &mdash; which matters a great deal if something is ever questioned.</p>"""),
 ],
 "faq": [
  ("What wind loads are houses designed for in Quintana Roo?",
   "The peninsula sits in one of Mexico's highest wind-load regions, and residential structures here are governed by wind rather than seismic loading. The practical implications are continuous load paths to resist uplift, tightened fixing patterns at roof edges and corners where pressures are highest, and glazing specified so the envelope stays closed &mdash; because internal pressurisation after a window failure is what takes roofs off."),
  ("Do I really need a soil study before designing the structure?",
   "Yes, and with probes across the actual building footprint, not a single hole in the middle of the lot. The ground here is karst limestone: bearing can be excellent at shallow depth and a cavity can sit two metres away. A study costs $25,000&ndash;$60,000 MXN; discovering a void after the slab is poured costs multiples of that."),
  ("What is a Director Responsable de Obra and do I need one?",
   "A registered professional who signs for the project and the works, and carries legal responsibility for compliance with the municipal regulations. The construction licence in Quintana Roo municipalities requires one. The structural design and the submitted plans sit under that signature, which is why the engineering, the DRO and the site execution should be coordinated rather than contracted separately."),
  ("Why do coastal buildings here get flaking, stained concrete?",
   "Chloride-induced reinforcement corrosion. Salt migrates through the concrete cover, the steel corrodes, and the expanding corrosion product spalls the concrete. The defences are greater cover on exposed elements, denser and less permeable concrete, proper curing, epoxy-coated or stainless rebar in splash zones, and detailing so water drains rather than standing on edges."),
  ("Can you engineer the long cantilevers and floating roofs in contemporary Tulum designs?",
   "Yes &mdash; they simply require explicit analysis rather than rules of thumb, because the governing case is uplift and deflection rather than downward load. Those elements also need the most careful durability detailing, since they are the most exposed parts of the building. We design them in-house alongside the architecture, which is how the aesthetic intent survives the engineering."),
 ],
}

CONTENT["mep-engineering-plans-riviera-maya"] = {
 "title": "MEP Plans in the Riviera Maya: Water, Power, AC, Wastewater",
 "desc": "What a complete MEP set contains for a Quintana Roo house: cistern and pressure systems, water treatment, AC sizing, CFE load, and karst-compliant wastewater.",
 "intro": [
   "MEP &mdash; mechanical, electrical and plumbing &mdash; is the half of a house that determines whether living in it is pleasant, and the half most often drawn thinly or not at all. Plenty of houses here are built from an architectural set plus improvisation on site, and they work, in the sense that water comes out of the taps. They also have undersized cisterns, air conditioning that cannot hold the house at 24&deg;C in August, no plan for the water hardness, and a drainage arrangement that the environmental authority would not have approved if it had been asked.",
   "This covers what a proper MEP set contains for a house on this coast, the four local systems that differ most from anywhere else &mdash; water storage and pressure, treatment, cooling, and wastewater into karst &mdash; and what the engineering costs relative to what it saves."
 ],
 "sections": [
  ("Water: Storage, Pressure and Treatment",
   """    <p>Municipal supply across the corridor is intermittent in places, pressure is variable, and the water is hard and chlorinated. Every house here therefore has a storage-and-pressure system, and the sizing is an engineering decision, not a builder's habit.</p>
    <ul>
      <li><strong>Cistern sizing:</strong> plan for at least two to three days of consumption &mdash; more for a rental villa with a pool and full occupancy, more again where supply is known to be intermittent. Undersized cisterns are the most common MEP complaint we are called about in finished houses.</li>
      <li><strong>Pressure system:</strong> a hydropneumatic set or a variable-speed pump sized to the fixture count and the simultaneity you actually expect. A villa with three rain showers running at once needs to be designed for that, not discovered.</li>
      <li><strong>Treatment train:</strong> sediment filtration, a softener for the hardness (which otherwise destroys water heaters, shower fittings and pool equipment), carbon for chlorine and taste, and a point-of-use RO at the kitchen for drinking. Leave the plant room space and the plumbing at rough-in.</li>
      <li><strong>Rainwater harvesting</strong> is genuinely worth designing in here &mdash; 1,200+ mm of annual rainfall on a roof area of 200 m&sup2; is a substantial volume, and it is soft water, which is a bonus for irrigation and the pool.</li>
      <li><strong>Hot water:</strong> LP gas instantaneous units are the local default and work well; solar thermal pays back fast in this climate; heat-pump water heaters suit larger houses. Whichever, plan recirculation on long runs so a distant bathroom does not waste thirty seconds of water.</li>
    </ul>"""),
  ("Cooling, Ventilation and Electrical Load",
   """    <p><strong>Air conditioning is the largest single energy load in a house here, so sizing errors are expensive twice.</strong> Oversized equipment short-cycles, never runs long enough to dehumidify, and leaves a house that is cold and clammy; undersized equipment runs continuously and still does not hold temperature in August. A room-by-room load calculation &mdash; accounting for glazing area and orientation, insulation, ceiling height, occupancy and the infiltration rate &mdash; is the deliverable, not a rule of thumb per square metre.</p>
    <ul>
      <li><strong>Inverter mini-splits per zone</strong> for most houses: efficient, quiet, and they dehumidify properly at part load. Ducted systems suit larger villas where the equipment can be hidden and serviced.</li>
      <li><strong>Dehumidification as a separate consideration.</strong> In shoulder seasons the house needs moisture removed more than heat. A standalone dehumidifier on a humidistat protects joinery, artwork and stored textiles &mdash; essential in a house that closes for months.</li>
      <li><strong>Ventilation.</strong> Bathroom and kitchen extraction ducted to outside, a make-up air path, and ceiling fans everywhere: in this climate, air movement raises the comfortable set point by two or three degrees, which is real money on the CFE bill.</li>
      <li><strong>Electrical load schedule</strong> built from the actual equipment list &mdash; every AC unit, pool pump, water pump, treatment plant, EV charger and 220 V appliance &mdash; sized with 25&ndash;30% spare panel capacity and matched to the CFE service being requested. Requesting the wrong load is one of the more tedious mistakes to unwind with the utility.</li>
    </ul>"""),
  ("Wastewater into Karst, and What the Engineering Costs",
   """    <p>This is the system where local regulation bites hardest. There is no continuous municipal sewer across much of the corridor, the ground is permeable karst, and what infiltrates reaches the aquifer and then the reef. Environmental files in Tulum and Puerto Morelos examine the wastewater solution closely, and rightly.</p>
    <ul>
      <li><strong>Where a municipal sewer exists</strong> (much of Playa del Carmen and Canc&uacute;n), connect to it &mdash; with the correct connection permit.</li>
      <li><strong>Where it does not,</strong> the compliant answer is treatment before infiltration: a package treatment plant or a biodigester sized to occupancy, followed by an absorption well or field, with sludge management planned. A bare septic pit discharging into the karst is the arrangement being actively enforced against.</li>
      <li><strong>Greywater separation</strong> lets you reuse for irrigation and reduces the treatment load &mdash; worth designing in on villas with gardens.</li>
      <li><strong>Pool backwash and equipment drainage</strong> need their own route; saline or chlorinated backwash into a planted absorption area kills the planting and is not an acceptable discharge.</li>
    </ul>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Item</th><th>MXN</th><th>Notes</th></tr></thead>
      <tbody>
        <tr><td>Full MEP engineering set, 200&ndash;300 m&sup2; house</td><td>$45,000&ndash;$120,000</td><td>Load calcs, schematics, layouts, schedules</td></tr>
        <tr><td>Cistern 10,000&ndash;15,000 L with pressure system</td><td>$60,000&ndash;$150,000</td><td>Sized to consumption, not to habit</td></tr>
        <tr><td>Water treatment train (filter, softener, carbon, RO)</td><td>$35,000&ndash;$95,000</td><td>Protects every fitting downstream</td></tr>
        <tr><td>Package treatment plant / biodigester + absorption well</td><td>$90,000&ndash;$350,000</td><td>Sized to occupancy; part of the environmental file</td></tr>
        <tr><td>AC: inverter mini-splits, 4&ndash;5 zones, installed</td><td>$120,000&ndash;$280,000</td><td>After a room-by-room load calculation</td></tr>
      </tbody>
    </table>
    </div>
    <p>Set the engineering fee against what it prevents: a cistern that has to be dug up and enlarged, an AC system that cannot hold the house and gets replaced in year three, a treatment solution retrofitted under pressure from an environmental review. We produce the MEP set in-house against the architectural plans, which is also why our conduit, sleeves and drainage runs are in the slab before it is poured rather than chased into it afterwards.</p>"""),
 ],
 "faq": [
  ("What does an MEP engineering set cost for a house here?",
   "$45,000&ndash;$120,000 MXN for a 200&ndash;300 m&sup2; house &mdash; load calculations, schematics, layouts and equipment schedules for mechanical, electrical and plumbing. It is a small fraction of the systems cost and it prevents the expensive category of error: undersized cisterns, mis-sized air conditioning, and wastewater solutions retrofitted under regulatory pressure."),
  ("How big should the cistern be?",
   "Size it to two to three days of actual consumption at minimum, and more for a rental villa with a pool and full occupancy or where supply is known to be intermittent. Undersized cisterns are the most frequent complaint we hear about finished houses here, and enlarging one after the terrace is built is genuinely disruptive."),
  ("Do I need water treatment in the Riviera Maya?",
   "In practice yes. The water is hard and chlorinated, and untreated it shortens the life of water heaters, shower fittings, appliances and pool equipment. The standard train is sediment filtration, a softener, carbon for chlorine and taste, and a point-of-use reverse osmosis unit at the kitchen for drinking &mdash; $35,000&ndash;$95,000 MXN installed, and it protects everything downstream of it."),
  ("What is the correct wastewater solution where there is no sewer?",
   "Treatment before infiltration: a package treatment plant or biodigester sized to the occupancy, discharging to an absorption well or field, with sludge management planned and pool backwash routed separately. A bare septic pit into karst is what environmental authorities are enforcing against, because what infiltrates reaches the aquifer and then the reef."),
  ("How should air conditioning be sized?",
   "From a room-by-room load calculation that accounts for glazing area and orientation, insulation, ceiling height, occupancy and infiltration &mdash; not a fixed number of BTU per square metre. Oversized units short-cycle and leave the house cold and humid because they never run long enough to dehumidify; undersized units run constantly and still lose in August."),
 ],
}

CONTENT["floor-plans-riviera-maya-homes"] = {
 "title": "Floor Plans for Riviera Maya Homes: What Works in This Climate",
 "desc": "Orientation, cross-ventilation, indoor-outdoor transitions and the service spaces imported plans forget — the plan decisions that make a tropical house work.",
 "intro": [
   "Most of the house plans that arrive with new clients here were drawn for a different climate. They put the main glazing west, they treat the terrace as a leftover strip, they omit the service spaces a house in Quintana Roo actually needs, and they assume a corridor-and-room logic that fights a place where you want to live with the doors open for eight months of the year.",
   "A good plan here does specific things: it orients against the sun and with the prevailing breeze, it gives the outdoor room as much design attention as the living room, it separates guest and owner zones, and it makes room for the equipment a tropical house runs on. This guide is the checklist we work through with clients before anything is drawn."
 ],
 "sections": [
  ("Orientation, Sun and the Prevailing Breeze",
   """    <p>Two environmental facts drive the plan. The prevailing wind on this coast comes predominantly from the east and southeast, and the sun is high and punishing, with the west elevation taking the worst heat of the day in the late afternoon.</p>
    <ul>
      <li><strong>Long axis roughly east&ndash;west,</strong> so the main rooms face north and south and the small, hard-to-shade elevations face east and west. This single decision reduces cooling load more than any equipment choice.</li>
      <li><strong>Minimise west glazing,</strong> or shade it properly with deep overhangs, louvres or planting. A big unshaded west window in Playa del Carmen is an afternoon heater you cannot turn off.</li>
      <li><strong>Open the plan to the east&ndash;southeast breeze</strong> and give it a path out &mdash; openings on opposite sides of each main space, and internal doors and transoms that let air cross rather than dead-ending in a corridor.</li>
      <li><strong>Deep overhangs and covered terraces</strong> as the default, not an add-on: they shade the wall, keep rain out of open doors, and create the space people actually use.</li>
      <li><strong>Stack the wet rooms and services</strong> on the hot west or north-facing service side, using them as a thermal buffer for the living spaces.</li>
    </ul>
    <p>On a jungle lot in Tulum or along the Ruta de los Cenotes, add one more: decide early which trees stay. The environmental file may limit clearance, and mature canopy is the best shading device available &mdash; a plan that works around three existing trees is usually cooler and always cheaper than one that removes them.</p>"""),
  ("Indoor&ndash;Outdoor Living and Room Sizing",
   """    <p>The characteristic mistake in imported plans is treating the terrace as circulation. Here it is the primary living space for most of the year, and it should be sized and equipped accordingly.</p>
    <ul>
      <li><strong>Make the covered terrace a room:</strong> 20&ndash;40 m&sup2; for a family house, deep enough (3.5 m+) that furniture and a table fit without being rained on, with a ceiling fan, lighting circuits and power.</li>
      <li><strong>Flush thresholds and wide sliding or lift-and-slide openings</strong> so the boundary genuinely disappears. Detail the drainage carefully &mdash; a flush threshold needs a channel drain and a slope away, or driven rain comes inside.</li>
      <li><strong>Outdoor kitchen and grill</strong> positioned downwind of seating and out from under any thatch.</li>
      <li><strong>Pool placement</strong> for sun at the hour you swim, with a shaded shallow end or a sun shelf, and with the equipment pad screened, accessible and not under a bedroom window.</li>
      <li><strong>Rooftop terrace,</strong> if the zoning allows the height &mdash; it is the highest-value square metre in a rental listing on this coast. Design the structure and waterproofing for it from the start, not as a later addition.</li>
      <li><strong>Ceiling height:</strong> 2.9&ndash;3.4 m in main spaces. Height buys comfort in the tropics and is cheap while the walls are going up.</li>
    </ul>
    <p>For guest and rental performance, separate the zones: a primary suite that can be closed off, guest bedrooms with their own bathrooms rather than sharing, and ideally a casita or lock-off unit &mdash; which lets an owner use the house while the rest is rented, and materially widens the rental market.</p>"""),
  ("The Service Spaces Imported Plans Forget",
   """    <p>Local houses include a set of spaces that plans drawn elsewhere routinely omit. Adding them later means losing a bathroom or a closet, so they belong on the first sketch.</p>
    <ul>
      <li><strong>Cistern and pump room,</strong> or a properly sized below-terrace cistern with an accessible hatch. This is not optional here &mdash; supply is intermittent.</li>
      <li><strong>Water treatment plant space</strong> for the filter, softener and carbon unit, with drainage and a little working room around it.</li>
      <li><strong>Utility / laundry area with drying space out of the rain.</strong> An outdoor line in the shade dries clothes faster than a dryer and costs nothing; nobody wants it across the front terrace.</li>
      <li><strong>Storage for hurricane preparation</strong> &mdash; somewhere to put shutters, outdoor furniture and the palapa-adjacent loose items on a day's notice. A garage or a dedicated storeroom that can take terrace furniture is worth a great deal twice a decade.</li>
      <li><strong>AC equipment positions</strong> planned for airflow and service access, not squeezed onto a light well where no technician can reach them.</li>
      <li><strong>Pool equipment pad,</strong> screened, ventilated and drained.</li>
      <li><strong>Staff and delivery access</strong> that does not cross the main terrace &mdash; a practical courtesy in a house with a gardener, pool service and cleaning.</li>
      <li><strong>Generous entrance transition</strong> &mdash; somewhere to take off sandy shoes and put wet towels, which in a beach house is a real room, not a detail.</li>
    </ul>
    <p>We design plans in-house against these constraints and then engineer them, which is why our drawings tend to look slightly less dramatic in a render and considerably better to live in. If you already have plans drawn abroad, we review them against this list and against the municipal land-use limits &mdash; setbacks, height, COS and CUS &mdash; before anything is submitted, because adjusting a plan is cheap and adjusting a foundation is not.</p>"""),
 ],
 "faq": [
  ("How should a house be oriented in the Riviera Maya?",
   "Long axis roughly east&ndash;west, so the main rooms face north and south while the small elevations take the harsh east and west sun. Open the plan to the prevailing east&ndash;southeast breeze with openings on opposite sides of each space so air crosses, and shade or minimise west glazing &mdash; unshaded west glass is the biggest avoidable cooling load in a house here."),
  ("How big should the covered terrace be?",
   "Treat it as a room, not circulation: 20&ndash;40 m&sup2; for a family house and at least 3.5 m deep so a table and furniture stay dry, with a ceiling fan, lighting and power. For eight months of the year it is where the household actually lives, and in a rental listing it is one of the strongest selling images."),
  ("What spaces do imported house plans usually leave out?",
   "The cistern and pump room, water treatment plant space, a laundry with covered drying, storage for hurricane preparation and terrace furniture, serviceable AC equipment positions, a screened pool equipment pad, and a generous entry transition for sandy shoes and wet towels. Adding them later costs a bathroom or a closet, so they belong on the first sketch."),
  ("Is a rooftop terrace worth it?",
   "Where the zoning height allows it, yes &mdash; it is typically the highest-value square metre on a rental property here. It has to be designed in from the start, though: the structure, the waterproofing build-up, the stair, the services and the shade structure all change if the roof is occupied rather than just a roof."),
  ("Can you review plans an architect abroad has already drawn?",
   "Yes, and it is worth doing before anything is submitted. We check them against the climate issues &mdash; orientation, cross-ventilation, west exposure, terrace depth &mdash; against the local service spaces they usually omit, and against the municipal land-use limits: setbacks, height, COS and CUS. Adjusting a plan is inexpensive; adjusting a poured foundation is not."),
 ],
}

CONTENT["construction-costs-puerto-aventuras"] = {
 "title": "Construction Costs in Puerto Aventuras: 2026 Price Breakdown",
 "desc": "Building in Puerto Aventuras: per-m² bands, the marina and gated-community factors, design committee rules, HOA fees and how it compares to PDC.",
 "intro": [
   "Puerto Aventuras is a gated marina community about 20 minutes south of Playa del Carmen, and building there is a genuinely different exercise from building in an open subdivision. The land is largely built out with canal-front and golf-adjacent lots, the community runs a design review committee with its own rules, access and working hours are controlled, and the marina and canal frontage bring salt-air and structural considerations that inland lots do not have.",
   "This is what building there actually costs in 2026, what the community's own requirements add to a project, and how the total compares with Playa del Carmen and Tulum for the same house."
 ],
 "sections": [
  ("Cost Per Square Metre &mdash; Puerto Aventuras 2026",
   """    <p>Puerto Aventuras runs roughly 8&ndash;12% above equivalent Playa del Carmen pricing. The premium is not the community being expensive for its own sake &mdash; it is access control, restricted working hours, longer material handling, and the marine-grade specification that canal and near-shore positions require.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Build level</th><th>MXN/m&sup2;</th><th>USD/m&sup2;</th><th>200 m&sup2; house</th></tr></thead>
      <tbody>
        <tr><td>Mid-range</td><td>$16,500&ndash;$21,000</td><td>$915&ndash;$1,165</td><td>$183,000&ndash;$233,000 USD</td></tr>
        <tr><td>Premium</td><td>$22,000&ndash;$28,000</td><td>$1,220&ndash;$1,555</td><td>$244,000&ndash;$311,000 USD</td></tr>
        <tr><td>Luxury (canal front, marine spec)</td><td>$28,000&ndash;$40,000+</td><td>$1,555&ndash;$2,220+</td><td>$311,000&ndash;$444,000+ USD</td></tr>
      </tbody>
    </table>
    </div>
    <p>Those figures cover structure, finishes, MEP and basic landscaping. Outside them, budget separately for: architectural and engineering fees, the municipal licence and community review, the pool, a cistern and treatment plant, air conditioning, furniture, and the boat dock or slip works if the lot is canal-front. Dock works in particular are their own project with their own permitting and can add substantially.</p>"""),
  ("What the Community and the Municipality Require",
   """    <p>Two approval layers apply, and they are sequential in practice.</p>
    <ul>
      <li><strong>Municipal licence (Solidaridad).</strong> Puerto Aventuras sits in the municipality of Solidaridad, so the construction licence, land-use verification, alignment and the Director Responsable de Obra requirement run through Solidaridad &mdash; the same process as Playa del Carmen.</li>
      <li><strong>Community design review.</strong> The development's own committee reviews the design against the community's rules: height, setbacks, roof and facade materials, colour palette, wall and fence treatments, and the visual consistency the community maintains. Submit before you finalise the architecture, not after.</li>
      <li><strong>Construction rules on site.</strong> Expect controlled site access and worker registration, restricted working hours and days, rules about deliveries and material storage on the lot, an obligation to keep the street clean, and in many cases a construction deposit or bond held against damage to community infrastructure.</li>
      <li><strong>HOA fees.</strong> The community maintenance fee is an ongoing ownership cost and is worth confirming for the specific lot &mdash; canal-front and marina-adjacent properties often carry more, and any dock or slip may be a separate charge.</li>
    </ul>
    <p>None of this is unusual for a gated community, and it is precisely why an approval-and-access plan belongs in the programme at the start. The delays we see in communities like this are almost always a design committee round-trip that nobody scheduled.</p>"""),
  ("Canal and Marina Positions: What Changes Technically",
   """    <p>A canal-front lot is the reason people buy in Puerto Aventuras, and it changes the specification:</p>
    <ul>
      <li><strong>Marine-grade everything on the exterior.</strong> 316 stainless fixings, anodised or marine-powder-coated aluminium, upgraded concrete cover on exposed elements. Salt aerosol off the canal is constant, not seasonal.</li>
      <li><strong>Retaining and edge structures</strong> at the water's edge, with their own design and approval requirements. Assess the condition of existing seawalls and canal edges before you buy &mdash; repairing one is a significant project.</li>
      <li><strong>High water table.</strong> Excavations, cisterns and pool shells all need dewatering and buoyancy consideration. An emptied pool near the water table can float if it is drained at the wrong time.</li>
      <li><strong>Dock or slip works</strong> are separately permitted, involve federal maritime considerations where applicable, and should be priced as their own line rather than assumed into the house budget.</li>
      <li><strong>Storm exposure.</strong> Water-adjacent lots take the full wind load and, in a serious event, surge. Laminated or impact-rated glazing on the water elevation is a specification we would not compromise on here.</li>
    </ul>
    <p><strong>How it compares:</strong> for the same house, Puerto Aventuras runs about 8&ndash;12% above Playa del Carmen, broadly level with or slightly below the Tulum beach-adjacent zones, and clearly below Playacar, Mayakoba and Corasol. What you get for the premium is a gated marina community with its own services and, for a certain buyer, the only canal-front product in the corridor &mdash; which is also why it holds rental demand from families and boaters rather than only the Tulum design crowd.</p>"""),
 ],
 "faq": [
  ("How much does it cost to build a house in Puerto Aventuras?",
   "Mid-range construction runs $16,500&ndash;$21,000 MXN per m&sup2; ($915&ndash;$1,165 USD), premium $22,000&ndash;$28,000, and luxury canal-front with full marine specification $28,000&ndash;$40,000+. A 200 m&sup2; house therefore falls between roughly $183,000 and $444,000 USD depending on level, excluding land, pool, furniture and dock works."),
  ("Why is building in Puerto Aventuras more expensive than Playa del Carmen?",
   "By about 8&ndash;12%, for four concrete reasons: controlled site access and worker registration, restricted working hours that lengthen the programme, longer material handling inside the community, and the marine-grade specification that canal and near-shore positions require. It is not a surcharge for the address &mdash; each item is a real cost line."),
  ("Do I need approval from the community as well as the municipality?",
   "Yes, and they are sequential. The construction licence and the Director Responsable de Obra requirement run through the municipality of Solidaridad, while the community's own design committee reviews height, setbacks, materials, colours and boundary treatments. Submit to the committee before finalising the architecture &mdash; an unscheduled review round-trip is the most common delay here."),
  ("What extra costs come with a canal-front lot?",
   "Marine-grade exterior specification throughout, dewatering and buoyancy design for excavations and the pool, assessment or repair of the existing seawall or canal edge, and dock or slip works which are separately permitted and priced. Impact-rated glazing on the water elevation is also strongly advisable given the exposure."),
  ("How does Puerto Aventuras compare with Tulum or Playacar for building costs?",
   "It sits about 8&ndash;12% above Playa del Carmen, broadly level with the Tulum beach-adjacent zones, and clearly below Playacar, Mayakoba and Corasol. The distinctive product is canal and marina frontage, which nothing else in the corridor offers, and which draws a family and boating rental market rather than the design-led Tulum one."),
 ],
}

CONTENT["building-in-akumal-guide"] = {
 "title": "Building in Akumal: Turtle Rules, ZOFEMAT and Real Costs",
 "desc": "Akumal construction: Tulum municipality permits, turtle-nesting lighting and night-work limits, ZOFEMAT beachfront rules and reef-safe drainage.",
 "intro": [
   "Akumal is the most environmentally regulated stretch of the corridor between Playa del Carmen and Tulum, and for good reason: the bay is a green turtle feeding and nesting area, the reef sits close inshore, and the whole area drains into the same karst aquifer that feeds it. Building there is entirely possible &mdash; we do it &mdash; but the rules are more specific than anywhere else on the coast, and they affect the construction calendar as well as the design.",
   "This guide covers which authority does what, the turtle-season restrictions that shape lighting and night work, the beachfront rules if your lot touches the federal zone, the drainage requirements the reef imposes, and what building in Akumal costs in 2026."
 ],
 "sections": [
  ("Which Authority Governs What",
   """    <p>Akumal sits in the municipality of <strong>Tulum</strong>, which surprises owners who assume Solidaridad because Playa del Carmen is closer. That single fact changes the permit route, the office you file in, and the environmental sensitivity of the review.</p>
    <ul>
      <li><strong>Municipality of Tulum</strong> &mdash; land use, construction licence, alignment, Director Responsable de Obra, occupancy. Tulum's review is more environmentally demanding than Solidaridad's and its timelines are typically longer; plan for that rather than around it.</li>
      <li><strong>State environmental authority (SEMA Quintana Roo)</strong> &mdash; environmental impact where the project triggers it, which on a coastal or vegetated lot in this area is common.</li>
      <li><strong>SEMARNAT / federal</strong> &mdash; where federal jurisdiction applies, including ZOFEMAT beachfront and protected-species matters.</li>
      <li><strong>CONAGUA</strong> &mdash; water-related authorisations, including anything touching the aquifer or discharge.</li>
      <li><strong>ZOFEMAT concession</strong> &mdash; if any part of the property is within the federal maritime-terrestrial zone, that strip is federal and use requires a concession. Never assume the fence line equals the property boundary on a beachfront lot here.</li>
    </ul>
    <p>The practical consequence: permits in Akumal take longer and require a more complete environmental submission than the equivalent project in Playa del Carmen. Budget the calendar accordingly and file early &mdash; this is not a process that can be compressed by pressure.</p>"""),
  ("Turtle Season: Lighting and Night Work",
   """    <p>Turtle nesting on this coast runs broadly from <strong>May to October</strong>, and it imposes obligations that are real, enforced, and worth respecting on their own merits. They affect both how you build and what you build.</p>
    <ul>
      <li><strong>Lighting.</strong> Beach-facing exterior lighting must not disorient nesting females or hatchlings: low mounting height, shielded and downward-directed fittings, long-wavelength amber or red sources rather than white, no lighting that is visible from the beach, and no uplighting of facades or palms on the seaward side. This is a design decision &mdash; retrofitting a lighting scheme is far more expensive than specifying it.</li>
      <li><strong>Night work and beach activity</strong> in the nesting season is restricted near the beach. Heavy work, floodlighting and any activity on the sand are the first things curtailed.</li>
      <li><strong>Programme consequence.</strong> Schedule the noisy, beach-adjacent phases outside the season where possible, and plan the interior fit-out for the restricted months. A project that ignores this loses weeks.</li>
      <li><strong>Rental operation, later.</strong> The same lighting rules apply to the finished house in operation. Guests leaving beachfront floodlights on is a compliance problem for the owner, so specify the lighting controls so compliance is the default setting rather than a request in a welcome book.</li>
    </ul>"""),
  ("Reef-Safe Drainage, Costs, and Buying Advice",
   """    <p><strong>Drainage is the technical heart of an Akumal project.</strong> There is no comprehensive sewer, the ground is permeable karst, and the bay is close. Treatment before infiltration is not a nicety &mdash; it is what the environmental file is built around. Expect to install a package treatment plant or biodigester sized to occupancy with an absorption well or field, keep pool backwash out of the planted areas, separate greywater where it helps, and document sludge management. Reef-safe practice also extends to what the household uses: mineral-based sunscreen policies and low-phosphate products are standard guidance in rental houses here.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Build level</th><th>MXN/m&sup2;</th><th>USD/m&sup2;</th><th>Note</th></tr></thead>
      <tbody>
        <tr><td>Mid-range</td><td>$17,000&ndash;$22,000</td><td>$945&ndash;$1,220</td><td>~12% above Playa del Carmen</td></tr>
        <tr><td>Premium</td><td>$23,000&ndash;$29,000</td><td>$1,275&ndash;$1,610</td><td>Jungle or second-row lots</td></tr>
        <tr><td>Luxury beachfront</td><td>$29,000&ndash;$42,000+</td><td>$1,610&ndash;$2,330+</td><td>Marine spec, ZOFEMAT, full environmental file</td></tr>
        <tr><td>Treatment plant + absorption well</td><td>$120,000&ndash;$380,000</td><td>&mdash;</td><td>Sized to occupancy; central to approval</td></tr>
        <tr><td>Environmental studies and permits</td><td>$80,000&ndash;$350,000</td><td>&mdash;</td><td>Scope depends on vegetation and proximity to shore</td></tr>
      </tbody>
    </table>
    </div>
    <p><strong>Before you buy a lot in Akumal,</strong> check four things: whether any part of it lies in the federal maritime zone and what concession exists; what the land-use classification permits in terms of density, height and COS/CUS; whether electricity and water service reach the lot or require an extension; and whether there is an existing environmental authorisation, because inheriting a clean file is worth real money. We do this review for clients before purchase, and it has talked people out of lots more than once &mdash; which is cheaper than talking them out of a building.</p>"""),
 ],
 "faq": [
  ("Which municipality issues permits for Akumal?",
   "Tulum, not Solidaridad &mdash; a frequent surprise, since Playa del Carmen is physically closer. That means the land use, construction licence, alignment and DRO requirements go through Tulum, whose environmental review is more demanding and whose timelines are typically longer than Solidaridad's."),
  ("What are the turtle-season rules and do they affect construction?",
   "Nesting season runs roughly May to October. Beach-facing lighting must be low, shielded, downward-directed and amber or red rather than white, with no facade or palm uplighting on the seaward side; night work and activity on the sand near the beach are restricted. Schedule noisy beach-adjacent phases outside the season and keep interior work for those months."),
  ("How much does it cost to build in Akumal?",
   "Mid-range runs $17,000&ndash;$22,000 MXN per m&sup2; ($945&ndash;$1,220 USD), roughly 12% above Playa del Carmen; premium $23,000&ndash;$29,000; luxury beachfront $29,000&ndash;$42,000+. Add $120,000&ndash;$380,000 for a treatment plant and absorption well, and $80,000&ndash;$350,000 for environmental studies and permits depending on vegetation and proximity to the shore."),
  ("What drainage solution is acceptable in Akumal?",
   "Treatment before infiltration: a package treatment plant or biodigester sized to occupancy, discharging to an absorption well or field, with pool backwash routed separately and sludge management documented. The karst carries anything infiltrated toward the aquifer and the bay, which is why the environmental file is built around this system."),
  ("What should I check before buying a lot in Akumal?",
   "Whether any part lies in the federal maritime zone and what concession exists; the land-use classification and its density, height and COS/CUS limits; whether electricity and water actually reach the lot or need an extension; and whether an environmental authorisation already exists for the property. We run that review before purchase &mdash; it is far cheaper than discovering a constraint after closing."),
 ],
}

CONTENT["puerto-morelos-construction-guide"] = {
 "title": "Building in Puerto Morelos: Reef Park Rules and 2026 Costs",
 "desc": "Puerto Morelos became its own municipality in 2016 — what that means for permits, reef park and wetland limits, Ruta de los Cenotes lots and costs.",
 "intro": [
   "Puerto Morelos is the quiet middle of the corridor: twenty minutes from Canc&uacute;n airport, a working fishing village at its centre, a national marine park directly offshore, mangrove and wetland behind the town, and the Ruta de los Cenotes running inland. It also became its own municipality in 2016, separating from Benito Ju&aacute;rez, which is the single most important administrative fact for anyone planning to build there.",
   "This guide covers what the young municipality means in practice for permits, the environmental constraints the reef park and the wetlands impose, how inland Ruta de los Cenotes lots differ from town and beachfront lots, and what construction costs in 2026."
 ],
 "sections": [
  ("A Municipality Since 2016 &mdash; What That Changes",
   """    <p>Until 2016 this area was administered from Canc&uacute;n as part of Benito Ju&aacute;rez. Puerto Morelos now issues its own licences and runs its own planning instruments, and that has three practical consequences.</p>
    <ul>
      <li><strong>File in Puerto Morelos, not Canc&uacute;n.</strong> Land use, construction licence, alignment, DRO registration and occupancy all go through the municipality's own offices. Advice based on Benito Ju&aacute;rez practice is out of date.</li>
      <li><strong>Younger planning instruments.</strong> The municipality has been developing and updating its urban development programme, so density, height and use limits for a specific lot should be verified currently rather than assumed from an older document or a neighbour's project.</li>
      <li><strong>A smaller administration</strong> can mean either a faster, more direct process than a big-city bureaucracy, or a slower one where a file needs something unusual. Either way, the route is direct: the officials reviewing your file are accessible, which makes a complete, well-prepared submission unusually valuable.</li>
    </ul>
    <p>State and federal layers are unchanged: SEMA for state environmental impact, SEMARNAT and federal jurisdiction where it applies, CONAGUA for water matters, and ZOFEMAT for anything inside the federal maritime zone on the beach side.</p>"""),
  ("Reef Park, Mangroves and the Aquifer",
   """    <p>Puerto Morelos has the most explicit environmental geography of the corridor: a national park protecting the reef offshore, protected mangrove and wetland behind the town, and the cenote-riddled karst inland. Each sets a hard constraint rather than a guideline.</p>
    <ul>
      <li><strong>Mangrove is protected.</strong> Clearing or filling it is not a permitting negotiation. Wetland-adjacent lots need the boundary of the protected vegetation established before a footprint is drawn &mdash; and some lots offered for sale have far less buildable area than the title area suggests.</li>
      <li><strong>Discharge quality is the reef's issue.</strong> Treatment before infiltration, correctly sized, with pool backwash handled separately. The national park's presence makes this the centre of any environmental review.</li>
      <li><strong>Cenote and sinkhole setbacks</strong> apply inland, along with restrictions on what may infiltrate near them. A cenote on or near a lot is an asset and a constraint at the same time.</li>
      <li><strong>Flood and storm surge.</strong> Low-lying land near the wetlands and the shore requires finished floor levels set with surge and flooding in mind &mdash; a decision made at design stage and impossible to fix later.</li>
      <li><strong>Vegetation survey early.</strong> On any treed lot, an inventory drives both the environmental submission and the design. It is also the cheapest way to find out whether the house you want fits the land you are buying.</li>
    </ul>"""),
  ("Town, Beachfront and Ruta de los Cenotes &mdash; Costs 2026",
   """    <p>The three sub-markets behave differently, and it shows in the numbers.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Location / level</th><th>MXN/m&sup2;</th><th>USD/m&sup2;</th></tr></thead>
      <tbody>
        <tr><td>Town and inland residential, mid-range</td><td>$15,000&ndash;$19,500</td><td>$835&ndash;$1,085</td></tr>
        <tr><td>Town and inland residential, premium</td><td>$20,000&ndash;$26,000</td><td>$1,110&ndash;$1,445</td></tr>
        <tr><td>Beachfront / near-shore, marine spec</td><td>$26,000&ndash;$38,000+</td><td>$1,445&ndash;$2,110+</td></tr>
        <tr><td>Ruta de los Cenotes, serviced lot</td><td>$14,000&ndash;$19,000</td><td>$780&ndash;$1,055</td></tr>
        <tr><td>Ruta de los Cenotes, off-grid (solar, well, treatment)</td><td>$17,000&ndash;$24,000</td><td>$945&ndash;$1,335</td></tr>
      </tbody>
    </table>
    </div>
    <p><strong>The Ruta de los Cenotes is the value play and the logistics challenge.</strong> Land is markedly cheaper than the coast, the setting is exceptional, and an eco-lodge or a private house there can be genuinely special &mdash; but many lots have no CFE service and no municipal water. Off-grid is often the faster and cheaper answer than an electricity extension, and it is a design decision from day one: solar with storage sized to real loads, a well with treatment, rainwater harvesting, and a treatment plant with careful setback from any cenote. Budget for the access road too; a kilometre of unpaved access changes every delivery on the project.</p>
    <p><strong>Town and beachfront</strong> behave like a smaller, calmer version of the rest of the corridor: serviced, straightforward to build in, and roughly level with Playa del Carmen pricing inland with a clear premium on the shore, where the marine specification and the federal-zone questions apply. For buyers, Puerto Morelos is the corridor's steadiest proposition &mdash; airport proximity without Canc&uacute;n's density, and a rental market driven by divers and families rather than nightlife.</p>"""),
 ],
 "faq": [
  ("Which municipality issues construction permits in Puerto Morelos?",
   "Puerto Morelos itself &mdash; it separated from Benito Ju&aacute;rez (Canc&uacute;n) in 2016 and now issues its own land use, construction licences, alignments and occupancy approvals. Any guidance based on Canc&uacute;n practice is out of date, and the municipality's planning instruments are relatively young, so verify a specific lot's density, height and use limits currently rather than assuming from an older document."),
  ("How much does it cost to build in Puerto Morelos?",
   "Town and inland residential runs $15,000&ndash;$19,500 MXN per m&sup2; mid-range ($835&ndash;$1,085 USD) and $20,000&ndash;$26,000 premium. Beachfront with marine specification is $26,000&ndash;$38,000+. On the Ruta de los Cenotes, a serviced lot is $14,000&ndash;$19,000 and an off-grid build $17,000&ndash;$24,000."),
  ("Can I build on a mangrove or wetland lot?",
   "Not in the protected vegetation itself &mdash; mangrove clearing or filling is not a permitting negotiation. The boundary of protected vegetation has to be established before a footprint is drawn, and some lots offered for sale have substantially less buildable area than their title area implies. Have this checked before purchase."),
  ("What does building on the Ruta de los Cenotes involve?",
   "Cheaper land and an exceptional setting, in exchange for infrastructure. Many lots have no CFE service or municipal water, so the realistic path is off-grid by design: solar with storage sized to real loads, a well with treatment, rainwater harvesting, and a treatment plant set back properly from any cenote. Budget for the access road as well &mdash; unpaved access affects every delivery."),
  ("Is the national reef park a problem for building here?",
   "Not a prohibition, but it is the lens the environmental review looks through. Because the karst carries anything infiltrated toward the aquifer and the reef, discharge quality and treatment sizing are the central technical questions in the file, along with vegetation and setbacks. Projects that address them properly get approved; projects that treat drainage as an afterthought stall."),
 ],
}

CONTENT["construction-bacalar-lagoon"] = {
 "title": "Building in Bacalar: Lagoon Rules, Logistics and Real Costs",
 "desc": "Building near the Lagoon of Seven Colours: stromatolite and shoreline protection, wastewater rules, supply-chain distance and honest 2026 cost bands.",
 "intro": [
   "Bacalar is the most beautiful place to build in Quintana Roo and the most easily damaged. The Lagoon of Seven Colours owes its colour to a shallow limestone bed and to living stromatolite formations along parts of the shoreline &mdash; ancient microbial structures that are destroyed by trampling, by sediment, and by nutrient loading from wastewater. The boom in lakeside development has already produced visible consequences, and the regulatory response has tightened accordingly.",
   "This guide is written for someone considering a house or a small boutique project there, and it is deliberately honest about two things people underestimate: what the environmental rules genuinely require, and what it costs to build three and a half hours from the corridor's supply chain."
 ],
 "sections": [
  ("The Lagoon Is the Constraint",
   """    <p>Every serious decision in a Bacalar project comes back to the water. The lagoon is fed by the same karst aquifer that sits under the site, so what infiltrates on your lot arrives in the lagoon &mdash; and unlike the open Caribbean, a closed lagoon has nowhere to dilute it.</p>
    <ul>
      <li><strong>Wastewater is the central issue, not a detail.</strong> Treatment before infiltration, properly sized and properly maintained, is the baseline expectation. Nutrient loading from inadequate systems is directly implicated in algal growth and the loss of water clarity, and it is where enforcement attention sits.</li>
      <li><strong>Stromatolites are protected living formations.</strong> Where they occur along the shoreline they cannot be walked on, built over, dredged or disturbed. Shoreline works near them face the highest level of scrutiny, and some lakeside structures elsewhere on the lagoon have been the subject of enforcement.</li>
      <li><strong>Shoreline and riparian setbacks apply,</strong> along with federal jurisdiction over the federal zone at the water's edge. A dock, a deck over the water or a swimming platform is a separate permitting question from the house, and not an assumed right of a lakefront lot.</li>
      <li><strong>Vegetation clearing is scrutinised,</strong> and sediment control during construction matters &mdash; runoff carrying disturbed soil into the lagoon is as damaging as effluent.</li>
      <li><strong>Municipality of Bacalar</strong> issues the licence, with SEMA and federal authorities involved depending on the project's proximity to the water and its scale.</li>
    </ul>
    <p>Anyone who tells you the lakefront rules are a formality is describing how things were, not how they are. A project designed around the lagoon &mdash; set back, properly treated, minimal shoreline intervention &mdash; is approvable. A project designed against it is a slow, expensive argument.</p>"""),
  ("Distance from the Supply Chain: the Real Cost Driver",
   """    <p>Bacalar sits roughly 3.5&ndash;4 hours south of Playa del Carmen and about 40 minutes from Chetumal. That distance is the second defining feature of a project there, and it shows up in four places:</p>
    <ul>
      <li><strong>Materials.</strong> Basic materials &mdash; block, cement, steel, aggregate &mdash; are available locally or from Chetumal. Specialist items, quality joinery hardware, imported fittings, stone and specified aluminium systems generally come from the Canc&uacute;n&ndash;Playa corridor, with freight and lead time attached.</li>
      <li><strong>Skilled trades.</strong> The local labour pool handles conventional construction competently. Specialist work &mdash; high-end joinery, chukum application to a premium standard, complex aluminium glazing, pool and treatment plant commissioning &mdash; typically means mobilising crews from the corridor, with accommodation and travel in the budget.</li>
      <li><strong>Supervision.</strong> A weekly site visit from Playa del Carmen is a full day. Projects here need either a resident site supervisor or a deliberately longer visit cycle with much better documentation &mdash; and remote-managed clients need a reporting discipline that does not depend on the owner dropping in.</li>
      <li><strong>Programme.</strong> Build in float. A missing component that is a two-hour errand in Playa del Carmen is a two-day problem in Bacalar.</li>
    </ul>
    <p>The offset is land price. Lakefront and near-lake land in Bacalar has historically been a fraction of the coastal equivalent, which is exactly why the boutique-hotel and eco-lodge interest exists. The arithmetic can be excellent &mdash; it just has to include the logistics rather than assume corridor conditions.</p>"""),
  ("Cost Bands and What Suits the Place &mdash; 2026",
   """    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Project</th><th>MXN/m&sup2;</th><th>USD/m&sup2;</th></tr></thead>
      <tbody>
        <tr><td>Conventional local-standard house</td><td>$11,000&ndash;$15,000</td><td>$610&ndash;$835</td></tr>
        <tr><td>Mid-range house, corridor-standard specification</td><td>$15,000&ndash;$21,000</td><td>$835&ndash;$1,165</td></tr>
        <tr><td>Premium / lakeside villa, specialist trades mobilised</td><td>$22,000&ndash;$32,000</td><td>$1,220&ndash;$1,780</td></tr>
        <tr><td>Boutique eco-lodge, per key (6&ndash;14 keys)</td><td>$900,000&ndash;$2,400,000 per key</td><td>$50,000&ndash;$133,000 per key</td></tr>
        <tr><td>Treatment plant sized for a small lodge</td><td>$350,000&ndash;$1,200,000</td><td>&mdash;</td></tr>
      </tbody>
    </table>
    </div>
    <p><strong>What suits Bacalar architecturally</strong> is also what suits it environmentally: low-rise buildings set back from the water, timber and local stone, palapa and pergola shade structures, cross-ventilated plans that reduce dependence on air conditioning, rainwater harvesting, solar with storage, and a wastewater solution over-specified rather than minimally compliant. Low density is not a compromise here &mdash; it is the product. The market coming to Bacalar is looking for quiet, dark skies and clear water, all three of which are destroyed by the sort of development that maximises keys per hectare.</p>
    <p>One honest caveat about builders, ourselves included: our base and our crews are in Playa del Carmen, and Bacalar is a mobilisation, not a local operation. For a project there we would price the travel, accommodation and resident supervision explicitly rather than bury them, and for a small conventional house you may well be better served by a competent Bacalar or Chetumal contractor. For a lakeside villa or a boutique lodge where the specification and the environmental file are the hard part, mobilising a corridor team is usually the right call &mdash; and either way, that is a conversation to have before you buy the lot.</p>"""),
 ],
 "faq": [
  ("Can you build on the lagoon shore in Bacalar?",
   "Set back from it, yes, with a properly engineered treatment system and minimal shoreline intervention. Building over the water, dredging, or disturbing stromatolite formations is not permittable &mdash; those formations are protected living structures, and shoreline works near them face the highest scrutiny. A dock or over-water deck is a separate permitting question from the house, not an automatic right of a lakefront lot."),
  ("How much does it cost to build in Bacalar?",
   "A conventional local-standard house runs $11,000&ndash;$15,000 MXN per m&sup2; ($610&ndash;$835 USD); a mid-range house built to corridor specification $15,000&ndash;$21,000; a premium lakeside villa with specialist trades mobilised from the coast $22,000&ndash;$32,000. A boutique eco-lodge typically works out at $900,000&ndash;$2,400,000 MXN per key."),
  ("Why is building in Bacalar sometimes more expensive than the coast?",
   "Because it is 3.5&ndash;4 hours from the corridor's supply chain. Basic materials are available locally, but specialist items, quality hardware and specified systems come from Canc&uacute;n or Playa del Carmen with freight and lead time, and specialist trades have to be mobilised with travel and accommodation. Land price usually more than offsets it &mdash; the arithmetic just has to include the logistics."),
  ("What wastewater system is required near the lagoon?",
   "Treatment before infiltration, sized generously and maintained &mdash; this is the central technical issue of any Bacalar project, because the karst carries whatever infiltrates into a closed lagoon that cannot dilute it. Nutrient loading from inadequate systems is directly implicated in the loss of water clarity, which is why it is also where enforcement attention concentrates."),
  ("Do you work in Bacalar?",
   "We are based in Playa del Carmen, so Bacalar is a mobilisation rather than a local operation, and we price the travel, accommodation and resident supervision explicitly rather than hiding them in the rate. For a straightforward conventional house, a good Bacalar or Chetumal contractor may serve you better. For a lakeside villa or boutique lodge where specification and the environmental file are the difficult part, mobilising a corridor team usually makes sense &mdash; and the decision is best made before you buy the land."),
 ],
}

CONTENT["isla-mujeres-construction-challenges"] = {
 "title": "Building on Isla Mujeres: Ferry Logistics, Salt and Water",
 "desc": "Island construction reality: barge and ferry material costs, no local aggregate, marine corrosion spec, water limits and the real logistics premium.",
 "intro": [
   "Isla Mujeres is eight kilometres long, half a kilometre wide at its widest, and everything that becomes a building there arrives by water. That single fact reorganises a construction project: procurement becomes a scheduling discipline, waste removal becomes a cost line, and a forgotten box of fixings becomes a lost day rather than a lost hour.",
   "Add the most aggressive salt exposure in the state &mdash; the island is surrounded by sea on all sides, with almost no position more than a couple of hundred metres from the water &mdash; plus finite utilities and a municipal administration of its own, and you have a build that rewards planning far more than it rewards speed. This guide covers the logistics, the corrosion specification, the utility constraints, and what the island premium actually is."
 ],
 "sections": [
  ("Logistics: Everything Arrives by Water",
   """    <p>Materials reach the island by cargo barge from Puerto Ju&aacute;rez or by the vehicle ferry, and the practical consequences dominate the programme:</p>
    <ul>
      <li><strong>Aggregate, block, cement and steel all ship in.</strong> There is no local quarry or aggregate source of consequence, so the base materials that are cheap on the mainland arrive with freight attached.</li>
      <li><strong>Barge scheduling, not just-in-time delivery.</strong> Deliveries are batched. That means accurate quantity take-offs, storage space on a small site, and protection of stored material from salt and rain &mdash; and it means a take-off error is expensive rather than annoying.</li>
      <li><strong>Concrete supply is the classic constraint.</strong> Either it is barged as ready-mix within a workable window, or it is batched on site from imported materials, which affects quality control and the pour strategy. Plan pours as events, with contingency.</li>
      <li><strong>Waste goes back off the island.</strong> Demolition and construction debris removal is a real, quotable cost that mainland projects barely notice.</li>
      <li><strong>Narrow streets and access.</strong> Much of the island cannot take a large truck or a concrete pump of any size. Golf carts and small vehicles are the local reality, and the last 50 metres of a delivery is sometimes manual.</li>
      <li><strong>Trades travel daily</strong> unless they are housed on the island, so the working day is shortened by the crossing at both ends, or accommodation goes in the budget.</li>
    </ul>
    <p>Net effect on cost: expect roughly <strong>25&ndash;40% above equivalent mainland Canc&uacute;n construction</strong>, concentrated in materials, logistics and time rather than in labour rates.</p>"""),
  ("Corrosion: the Most Aggressive Exposure in the State",
   """    <p>No part of Isla Mujeres is meaningfully sheltered from marine air, so the specification that is prudent on the mainland coast is mandatory here.</p>
    <ul>
      <li><strong>316 stainless for all exposed fixings, fasteners and hardware</strong> &mdash; railings, gates, window furniture, pergolas, light fittings, pool fixtures. 304 will pit and tea-stain.</li>
      <li><strong>Anodised aluminium or marine-grade powder coat</strong> for all glazing and exterior aluminium. Standard architectural powder coat does not last here.</li>
      <li><strong>Increased concrete cover and denser, less permeable mixes</strong> on every exposed element, with cover controlled on site by spacers and the pour cured properly. Chloride-induced spalling is the island's signature long-term defect.</li>
      <li><strong>Galvanised plus painted (duplex) protection for any structural steel,</strong> with connections and site welds treated rather than touched up.</li>
      <li><strong>Marine-rated electrical enclosures, gasketed, with drip loops,</strong> and AC condensers specified with coated coils &mdash; uncoated coils corrode and lose capacity within a few years.</li>
      <li><strong>Fresh-water rinse points</strong> designed into terraces and pool surrounds, because periodic rinsing is the cheapest maintenance regime available for stainless and glass.</li>
    </ul>
    <p>Build the maintenance cycle into the handover documentation: on this island, a building that is not rinsed and inspected annually ages roughly twice as fast as one that is.</p>"""),
  ("Water, Wastewater and the Permit Layer",
   """    <p><strong>Utilities are finite,</strong> and this shapes what a project can be. Potable water is supplied to the island, and capacity is not unlimited &mdash; which makes rainwater harvesting, low-flow fixtures, greywater reuse and, for hotel-scale projects, desalination or substantial storage genuine design questions rather than sustainability decoration. Wastewater must be treated properly: the island sits in a marine-park environment with the reef and Punta Sur protections nearby, and discharge quality is central to any environmental file. Electricity comes by submarine cable, so the load you request matters, and solar with storage is attractive both economically and as resilience.</p>
    <p><strong>Permits</strong> run through the municipality of Isla Mujeres &mdash; which, it is worth noting, also administers a stretch of the mainland including Playa Mujeres. State environmental review via SEMA applies, federal jurisdiction applies in the maritime zone and around protected areas, and hotel or commercial projects add Civil Protection and, in a national park context, additional federal consultation. Height and density limits on the island are deliberately restrained, so verify the specific lot's classification before designing anything &mdash; an island lot's realistic envelope is often smaller than a buyer assumes.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Project</th><th>MXN/m&sup2;</th><th>USD/m&sup2;</th></tr></thead>
      <tbody>
        <tr><td>Renovation of an existing house</td><td>$12,000&ndash;$22,000</td><td>$670&ndash;$1,220</td></tr>
        <tr><td>New house, mid-range, full marine spec</td><td>$22,000&ndash;$30,000</td><td>$1,220&ndash;$1,670</td></tr>
        <tr><td>Premium / seafront villa</td><td>$30,000&ndash;$45,000+</td><td>$1,670&ndash;$2,500+</td></tr>
        <tr><td>Small boutique hotel, per key</td><td>$1,300,000&ndash;$3,600,000 per key</td><td>$72,000&ndash;$200,000 per key</td></tr>
      </tbody>
    </table>
    </div>
    <p>Renovation is the island's most common work, and it is where the biggest surprises live: opening up a twenty-year-old house frequently reveals corroded reinforcement, failed waterproofing and electrical installations that have to be replaced rather than extended. Budget a contingency of 15&ndash;20% on any island renovation, and have the structure assessed before you commit to a scope.</p>"""),
 ],
 "faq": [
  ("How much more does it cost to build on Isla Mujeres?",
   "Roughly 25&ndash;40% above equivalent mainland Canc&uacute;n construction. The premium is in materials and logistics rather than labour: aggregate, block, cement and steel all arrive by barge or ferry, deliveries are batched rather than just-in-time, waste has to be shipped back off the island, and narrow streets often make the last stretch of a delivery manual."),
  ("What is the biggest technical challenge of island construction?",
   "Corrosion. Nowhere on the island is sheltered from marine air, so 316 stainless fixings, anodised or marine-grade coated aluminium, increased and well-controlled concrete cover, duplex-protected structural steel and coated AC coils are all mandatory rather than prudent. Chloride-induced concrete spalling is the island's signature long-term defect."),
  ("How is concrete handled on the island?",
   "Either barged as ready-mix within a workable window, or batched on site from imported materials. Both require pours to be planned as events with contingency, rather than ordered on the day. This is one of the main reasons island programmes need more float than mainland ones."),
  ("Are there limits on water and wastewater for a new project?",
   "Yes. Potable supply to the island is finite, which makes rainwater harvesting, low-flow fixtures and greywater reuse genuine design requirements &mdash; and for hotel-scale projects, storage or desalination. Wastewater must be properly treated, with discharge quality central to the environmental file given the marine park and nearby protected areas."),
  ("Is renovating an existing island house cheaper than building new?",
   "Usually, at $12,000&ndash;$22,000 MXN per m&sup2; against $22,000&ndash;$30,000 for a new mid-range house &mdash; but it carries more risk. Opening up an older island house regularly reveals corroded reinforcement, failed waterproofing and electrical work that must be replaced rather than extended. Have the structure assessed before fixing a scope, and carry a 15&ndash;20% contingency."),
 ],
}

CONTENT["airbnb-regulations-quintana-roo"] = {
 "title": "Airbnb Rules in Quintana Roo: Tax, Licences and Condo Bylaws",
 "desc": "The three layers governing short-term rentals here: federal tax withholding, the state lodging tax and municipal licences — plus the condo bylaw that stops owners.",
 "intro": [
   "Short-term rental in Quintana Roo is legal, normal and taxed, and the compliance picture has three layers that people tend to discover one at a time: federal tax, a state lodging tax, and municipal operating requirements. On top of those sits the rule that actually stops the largest number of owners &mdash; the condominium's own bylaws.",
   "This is an orientation to how those layers fit together, written from the perspective of someone building or buying to rent. Tax rates, registry requirements and municipal procedures do change, and they have changed more than once in recent years, so treat this as the map and confirm the current numbers with a Mexican accountant (contador) before you commit to a structure."
 ],
 "sections": [
  ("The Three Regulatory Layers",
   """    <ul>
      <li><strong>Federal &mdash; income tax and VAT.</strong> Rental income earned in Mexico is taxable in Mexico regardless of where the owner lives. Since the digital-platform rules came in, platforms such as Airbnb and Vrbo withhold income tax (ISR) and VAT (IVA) on Mexican-sourced bookings and remit them to SAT. Withholding is not the same as being fully compliant: whether you still need to register with SAT, issue invoices (facturas) and file returns depends on your residency status, your income level and how you hold the property. This is exactly the question to put to a contador.</li>
      <li><strong>State &mdash; lodging tax (impuesto al hospedaje).</strong> Quintana Roo levies a lodging tax on short-term accommodation, and it applies to private rentals, not just hotels. Platforms collect and remit it in many cases; direct bookings taken outside a platform generally do not have anyone collecting it for you, which is where owners fall out of compliance without realising.</li>
      <li><strong>Municipal &mdash; operating requirements.</strong> Municipalities in the state have moved toward treating short-term rental as a commercial lodging activity, which brings an operating licence (licencia de funcionamiento) or equivalent registration, Civil Protection requirements, and in some cases a property register. Requirements and enforcement differ by municipality and have been tightening, so check with the specific municipality &mdash; Solidaridad, Tulum, Benito Ju&aacute;rez, Puerto Morelos and Isla Mujeres each run their own process.</li>
    </ul>
    <p>None of this is unusually onerous by international standards. What causes problems is discovering the second and third layers after two years of operating on the first.</p>"""),
  ("The Rule That Stops Most Owners: Condo Bylaws",
   """    <p>Before any of the above matters, check the condominium regime. A building's own <em>reglamento</em> can prohibit short-term rental outright, impose a minimum stay of a month or more, cap the number of units that may be rented, require registration of guests with the administration, or charge the owner for guest use of amenities. These restrictions are private and enforceable, and they are entirely independent of whether the activity is legal under state and municipal rules.</p>
    <ul>
      <li><strong>Read the reglamento and the assembly minutes before purchase,</strong> not the listing description. Bylaws can also be amended by assembly after you buy &mdash; in buildings with a rising share of owner-occupiers, that happens.</li>
      <li><strong>Ask how many units currently rent short-term,</strong> and whether the administration is comfortable with it. A building running on rental income behaves very differently from a residential one with a few rentals in it.</li>
      <li><strong>Check the amenity and access arrangements.</strong> Some buildings restrict pool and gym access for short-stay guests, which changes what you can advertise.</li>
      <li><strong>Consider a standalone house instead.</strong> This is the single strongest structural argument for building a house or a villa rather than buying a condo for rental: nobody can vote your business model out of existence. It is one reason we see investors move from condo purchase to a custom build after their first experience of a bylaw amendment.</li>
    </ul>"""),
  ("Operating Well Inside the Rules",
   """    <p>Practical steps that keep a rental clean and defensible, and which also happen to improve the operation:</p>
    <ol>
      <li><strong>Get a contador before the first booking.</strong> Structure (individual vs company, resident vs non-resident), RFC registration, invoicing and filings are much cheaper to set up than to correct retroactively.</li>
      <li><strong>Keep platform withholding statements.</strong> They are your evidence of what has already been withheld and remitted, and they are what your accountant reconciles against.</li>
      <li><strong>Handle direct bookings deliberately.</strong> Direct bookings are more profitable and carry the taxes nobody is collecting for you. Decide how those are invoiced and remitted.</li>
      <li><strong>Get the municipal side in order.</strong> An operating licence, Civil Protection compliance &mdash; extinguishers, egress, pool safety, gas installation &mdash; and adequate liability insurance. These also matter after an incident, which is the moment they become expensive.</li>
      <li><strong>Build for the rules you will operate under.</strong> In Akumal that means turtle-compliant lighting as a default setting. In any coastal property it means a treatment plant sized for full occupancy rather than for a family. In a gated community it means confirming the HOA permits short-term rental at all.</li>
    </ol>
    <p>We build a large share of our projects for owners who intend to rent, and the compliance-relevant items &mdash; a treatment plant sized for occupancy rather than for two people, Civil Protection-ready gas and electrical work, pool safety, lighting that complies where nesting rules apply, and a lock-off unit so the owner can use part of the property while the rest earns &mdash; are all decisions made at design stage. Retrofitting them onto a finished house costs several times what including them costs, and until they are in place the property cannot legitimately operate at the occupancy its pro forma assumes.</p>"""),
 ],
 "faq": [
  ("Is Airbnb legal in Quintana Roo?",
   "Yes. Short-term rental is a legal, taxed activity here. Compliance involves three layers &mdash; federal income tax and VAT, the state lodging tax, and municipal operating requirements &mdash; plus, in a condominium, the building's own bylaws, which are private rules and can prohibit it regardless of what the law permits."),
  ("Does Airbnb withhold taxes for me in Mexico?",
   "Platforms withhold income tax and VAT on Mexican-sourced bookings and remit them to SAT under the digital-platform rules. That is not the same as being fully compliant: whether you also need to register with SAT, issue facturas and file returns depends on your residency, income level and ownership structure, and direct bookings taken outside a platform have nobody withholding on your behalf. Confirm your position with a Mexican accountant."),
  ("What is the lodging tax in Quintana Roo?",
   "The state levies a lodging tax (impuesto al hospedaje) on short-term accommodation, including private rentals rather than only hotels. Platforms collect and remit it on many bookings; direct bookings generally do not have anyone collecting it for you. The rate and the collection mechanism have changed over time, so verify the current figure with your contador."),
  ("Can my condo association stop me renting short-term?",
   "Yes &mdash; and this is what stops most owners. A condominium's bylaws can prohibit short-term rental, set minimum stays, cap the number of rented units, or restrict guest access to amenities, and they can be amended by assembly after you buy. Read the reglamento and recent assembly minutes before purchasing, and note that a standalone house removes this risk entirely."),
  ("What should I build differently if the property will be rented?",
   "A treatment plant sized for full occupancy rather than a couple, Civil Protection-ready gas and electrical installations, pool safety provisions, compliant lighting where turtle-nesting rules apply, durable finishes and replaceable components, and ideally a lock-off unit so you can use part of the property while the rest earns. All of these are design-stage decisions that cost a fraction of what they cost to retrofit."),
 ],
}

CONTENT["build-to-rent-riviera-maya"] = {
 "title": "Build-to-Rent in the Riviera Maya: Designing for Yield",
 "desc": "How a purpose-built rental villa differs from a private house: lock-off units, durability spec, occupancy-sized systems and the numbers that set the layout.",
 "intro": [
   "A house built to be lived in and a house built to be rented are different buildings, even at the same cost per square metre. The rental version earns more per square metre from bedrooms and outdoor space, it fails in different places because it is used harder by people who do not own it, it must be operable by a manager rather than an owner, and its systems have to carry full occupancy every night rather than two people most nights.",
   "This is a design guide for build-to-rent on this coast: what drives revenue, what drives cost over a ten-year hold, the layout decisions that matter most, and how to specify so the property is still earning at the top of its band in year eight."
 ],
 "sections": [
  ("What Actually Drives Rental Revenue Here",
   """    <p>Nightly rate and occupancy on this coast respond to a fairly predictable list, and it is not the list owners instinctively spend on.</p>
    <ul>
      <li><strong>Bedroom and bathroom count, en suite.</strong> Revenue scales with the number of couples or families that can share comfortably. Four bedrooms each with its own bathroom outperforms three bedrooms and a home office at almost every rate point.</li>
      <li><strong>The pool, and the pool's photograph.</strong> A private pool is close to non-negotiable for villa rental here, and its position relative to afternoon sun and to the main photograph is worth real money.</li>
      <li><strong>Covered outdoor living and a rooftop terrace.</strong> The two highest-value non-bedroom spaces. A deep shaded terrace with a dining table and a rooftop with a view convert browsers into bookings.</li>
      <li><strong>Air conditioning in every bedroom,</strong> working reliably. The most common serious complaint in reviews on this coast, and the one that most damages a listing's ranking.</li>
      <li><strong>A lock-off unit or casita.</strong> Lets the owner stay while the main house rents, allows two simultaneous bookings, and broadens the market to groups who want separation. Frequently the single best return on built area in a rental property.</li>
      <li><strong>Walkability or a genuine location story.</strong> Near the beach, near 5th Avenue, inside a gated community with amenities, or a jungle setting with real privacy &mdash; something a listing can say in one line.</li>
      <li><strong>Fast, reliable internet</strong> and a workable desk position. The remote-worker segment books longer stays, which is the most profitable kind of booking.</li>
    </ul>
    <p>Notice what is absent: expensive interior finishes above a competent standard, imported fittings, and bespoke joinery beyond the kitchen. Those raise cost without raising rate, and in a rental they wear visibly.</p>"""),
  ("Specify for Ten Years of Guests, Not for Yourself",
   """    <p>Rental use is harder than owner use in specific, predictable ways. Specify against them:</p>
    <ul>
      <li><strong>Floors:</strong> large-format porcelain or good local stone. Avoid soft natural stone that stains from sunscreen and wine, and avoid any timber floor in a beach house.</li>
      <li><strong>Walls:</strong> washable paint and generous use of tile in wet areas. Plan on repainting between seasons and make that cheap.</li>
      <li><strong>Joinery:</strong> laminate or lacquer over veneer, 316 hardware, and a design where a damaged door is replaceable from a standard size rather than a custom-made one-off.</li>
      <li><strong>Furniture:</strong> performance fabrics, leather, or slipcovers that can be laundered. Solid hardwood or powder-coated aluminium frames outdoors &mdash; never cheap rattan, which lasts one season.</li>
      <li><strong>Systems sized for full occupancy:</strong> cistern, hot water, pressure system and treatment plant designed for the maximum number of guests every night, not for the average. This is the most frequent undersize we are called in to correct.</li>
      <li><strong>Everything serviceable without entering a bedroom:</strong> AC condensers, pool equipment, water plant and the electrical panel accessible from outside or from a service area, so maintenance can happen during a stay.</li>
      <li><strong>Standardise.</strong> One tap model, one light fitting family, one paint colour, one AC brand. Spares in a cupboard mean a manager fixes a problem the same day instead of sourcing a discontinued part.</li>
      <li><strong>Remote monitoring:</strong> smart locks with time-limited codes, a pool pump monitor, a water-leak sensor, and cameras at entry points only. The failures that destroy a booking are a green pool and a failed AC unit, and both can be caught early.</li>
    </ul>"""),
  ("The Numbers That Shape the Plan",
   """    <p>Rough working figures we use with clients when sizing a build-to-rent project on this coast. They are starting points for a conversation, not a promise &mdash; actual performance depends on location, management quality and the property's photographs more than on any single design feature.</p>
    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Item</th><th>Typical range</th></tr></thead>
      <tbody>
        <tr><td>Construction, rental-grade specification</td><td>$18,000&ndash;$26,000 MXN/m&sup2;</td></tr>
        <tr><td>FF&amp;E (furniture, fittings, equipment), 3&ndash;4 bed villa</td><td>$450,000&ndash;$1,200,000 MXN</td></tr>
        <tr><td>Gross occupancy, well-managed villa</td><td>55&ndash;75% depending on location and rate strategy</td></tr>
        <tr><td>Management commission</td><td>15&ndash;25% of gross</td></tr>
        <tr><td>Operating costs (utilities, pool, garden, cleaning, maintenance, HOA)</td><td>25&ndash;35% of gross</td></tr>
        <tr><td>Platform fees and taxes</td><td>Varies &mdash; model with your contador</td></tr>
        <tr><td>Reserve for replacement of FF&amp;E</td><td>3&ndash;5% of gross annually</td></tr>
      </tbody>
    </table>
    </div>
    <p><strong>Two design conclusions follow from that table.</strong> First, because operating costs and commission consume a large share of gross, the cheapest reliable way to improve net yield is to reduce failure and maintenance &mdash; which is a specification decision made at build time, not an operational one. Second, because revenue scales with sleeping capacity and outdoor space, the plan should push area toward en-suite bedrooms, the pool terrace and a rooftop, and away from formal interior rooms that photograph well and earn nothing.</p>
    <p>We build to this brief regularly, and the most common change we make to a client's first sketch is converting an oversized living room and a study into a fourth en-suite bedroom and a deeper covered terrace. It costs the same to build and it moves the property into a higher rate band and a larger group market.</p>"""),
 ],
 "faq": [
  ("How is a build-to-rent villa different from a private house?",
   "Area is pushed toward en-suite bedrooms, the pool terrace and a rooftop rather than formal interior rooms; finishes are chosen for durability and replaceability rather than character; systems &mdash; cistern, hot water, pressure, treatment plant &mdash; are sized for full occupancy every night; everything is serviceable without entering a bedroom; and components are standardised so spares are on the shelf."),
  ("What is the single best return on built area for a rental property?",
   "Usually a lock-off unit or casita. It lets the owner stay while the main house rents, allows two simultaneous bookings, and appeals to groups who want separation. After that, an additional en-suite bedroom and a deeper covered terrace &mdash; both raise the rate band for the same construction cost as the rooms they replace."),
  ("What does it cost to build and furnish a rental villa here?",
   "Construction in a rental-grade specification runs $18,000&ndash;$26,000 MXN per m&sup2;, and FF&amp;E for a three-to-four bedroom villa is $450,000&ndash;$1,200,000 MXN. Budget a further 3&ndash;5% of gross revenue annually to replace furniture and equipment &mdash; rental use consumes it faster than owner use."),
  ("What fails most often in rental properties on this coast?",
   "Air conditioning and pool water quality &mdash; and both are the complaints that most damage a listing. Undersized cisterns and hot water systems come next, because they were specified for a family rather than for full occupancy. All three are specification decisions at build time rather than management problems afterwards."),
  ("What occupancy and operating costs should I model?",
   "For a well-managed villa, 55&ndash;75% gross occupancy depending on location and rate strategy, with management commission at 15&ndash;25% of gross and operating costs &mdash; utilities, pool, garden, cleaning, maintenance and any HOA fee &mdash; at 25&ndash;35%. Taxes and platform fees sit on top and should be modelled with a Mexican accountant, since the treatment depends on your structure."),
 ],
}

CONTENT["construction-financing-mexico-foreigners"] = {
 "title": "Construction Financing in Mexico for Foreigners: Real Options",
 "desc": "Why Mexican construction loans rarely work for foreign buyers, what actually funds builds here, and how milestone payments replace a construction loan.",
 "intro": [
   "The question arrives in almost every first conversation with a foreign client: can I get a construction mortgage in Mexico? The honest answer is that you usually can in theory and rarely should in practice. Mexican peso mortgage rates have historically run far above US and Canadian rates, cross-border underwriting for a non-resident without Mexican income is slow and document-heavy, and construction lending &mdash; as opposed to a mortgage on a finished property &mdash; is a thin product here even for residents.",
   "What actually funds the builds we deliver is a small set of arrangements, none of which is a Mexican construction loan. This is what they are, what each costs, and how the payment structure of the build itself works &mdash; because for most clients the milestone schedule is the financing."
 ],
 "sections": [
  ("Why the Mexican Construction Loan Is Rarely the Answer",
   """    <ul>
      <li><strong>Rate.</strong> Peso lending rates have historically been multiples of US and Canadian mortgage rates. A dollar-earning borrower paying peso rates on a peso loan is taking both an expensive rate and a currency position.</li>
      <li><strong>Underwriting.</strong> Mexican banks underwrite on Mexican income and Mexican credit history. Foreign income can sometimes be used, but the documentation burden is heavy, timelines are long, and approvals are unpredictable &mdash; which is poison for a construction programme with contractor commitments.</li>
      <li><strong>Construction lending specifically.</strong> Progressive draw-down against site progress is not a well-developed retail product here. Some cross-border lenders offer dollar-denominated loans to foreign buyers, generally for finished property rather than ground-up construction, and at rates above their home-market equivalents.</li>
      <li><strong>Fideicomiso and title.</strong> Within the restricted coastal zone, foreign buyers hold residential property through a bank trust (fideicomiso) or a Mexican company. That is well-established and lenders can work with it, but it adds a layer to any security arrangement and to the timeline.</li>
    </ul>
    <p>The practical result: foreigners building here almost always fund from capital or from borrowing raised outside Mexico, and the project's own payment schedule does the rest of the work.</p>"""),
  ("What Actually Funds Builds Here",
   """    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th>Source</th><th>Typical use</th><th>Reality</th></tr></thead>
      <tbody>
        <tr><td><strong>Cash / liquidated investments</strong></td><td>The majority of custom builds</td><td>Simplest; the milestone schedule spreads the outlay over 8&ndash;14 months</td></tr>
        <tr><td><strong>Home equity line or refinance in the home country</strong></td><td>Very common among US and Canadian clients</td><td>Home-market rates, home-market underwriting, funds arrive as cash here</td></tr>
        <tr><td><strong>Cross-border USD lender</strong></td><td>Purchase of finished property more often than construction</td><td>Rates above US equivalents; works with fideicomiso; slower closing</td></tr>
        <tr><td><strong>Developer or seller financing on the land</strong></td><td>Lot purchase, short terms</td><td>Widely available on lots; terms vary enormously &mdash; read them carefully</td></tr>
        <tr><td><strong>Private / hard-money lending in Mexico</strong></td><td>Bridge situations, short holds</td><td>Expensive; occasionally the right tool, never the default</td></tr>
        <tr><td><strong>Mexican bank mortgage</strong></td><td>Buyers with Mexican residency and income</td><td>Realistic for that profile; rarely competitive for a non-resident</td></tr>
      </tbody>
    </table>
    </div>
    <p>Two currency notes that matter more than clients expect. First, construction here is contracted in pesos, so a dollar-funded client carries FX exposure across an eight-to-fourteen-month build &mdash; movement in either direction is real money on a $300,000 project, and some clients choose to convert at milestones rather than all at once. Second, a contract denominated in dollars but executed in pesos hides that exposure inside the contractor's pricing, which usually costs more than managing it yourself.</p>"""),
  ("The Milestone Schedule Is the Financing",
   """    <p>A well-structured fixed-price contract spreads payment across the programme against verified progress. That structure is what lets a client build without a construction loan, and it is also the client's main protection.</p>
    <ol>
      <li><strong>Design and permits</strong> &mdash; drawn and paid as a defined stage, before any construction commitment.</li>
      <li><strong>Mobilisation and foundations</strong> &mdash; the first construction milestone.</li>
      <li><strong>Structure</strong> &mdash; columns, beams, slabs, typically in two or three tranches on a larger house.</li>
      <li><strong>Envelope and roof</strong> &mdash; walls closed, roof cast and waterproofed.</li>
      <li><strong>MEP rough-in</strong> &mdash; electrical, plumbing and AC in place before finishes.</li>
      <li><strong>Finishes</strong> &mdash; usually two milestones, as tiling and joinery progress.</li>
      <li><strong>Pool, landscaping, external works.</strong></li>
      <li><strong>Handover, snag list closed, retention released.</strong></li>
    </ol>
    <p>What to insist on in the contract: a <strong>fixed price with an itemised budget</strong> rather than a cost-plus arrangement with an unpriced scope; each payment tied to <strong>verified physical progress</strong>, not to a calendar date; a <strong>retention</strong> of five to ten percent released after the snag list is closed; <strong>change orders in writing with prices</strong> before work proceeds; and a clear statement of what is excluded &mdash; furniture, appliances, landscaping beyond a defined line, utility connection fees. A schedule where a large payment falls due before matching work exists on site is the structure to walk away from.</p>
    <p>We contract fixed price with milestone payments against progress, with weekly photo and video reporting, precisely because most of our clients are funding from abroad and are not on site. That reporting is not a courtesy &mdash; it is the evidence base for releasing each payment, and it is what makes remote-funded construction workable at all. Talk to a Mexican accountant about how the build is invoiced and how VAT applies to your structure before the first payment, because that is far easier to set up correctly than to correct afterwards.</p>"""),
 ],
 "faq": [
  ("Can a foreigner get a construction loan in Mexico?",
   "In theory sometimes, in practice rarely on competitive terms. Peso lending rates have historically run well above US and Canadian rates, banks underwrite on Mexican income and credit history, and progressive construction draw-down is a thin retail product here. Most foreign clients fund from capital or from borrowing raised in their home country."),
  ("What do most foreign clients actually use to fund a build?",
   "Cash or liquidated investments spread across the milestone schedule, or a home equity line or refinance in their own country at home-market rates. Cross-border USD lenders exist but mostly finance finished property rather than ground-up construction. Developer financing is common for the land itself, and private lending is occasionally useful as a bridge but never as a default."),
  ("How do construction payments work if I am not in Mexico?",
   "Through a fixed-price contract with payments tied to verified physical progress rather than calendar dates &mdash; design and permits, foundations, structure, envelope, MEP rough-in, finishes, external works, then handover with a retention released after the snag list closes. Weekly photo and video reporting provides the evidence for each release."),
  ("Should my contract be in pesos or dollars?",
   "Construction here is bought in pesos, so a peso contract is the honest one. A dollar-denominated contract executed in pesos simply moves the currency risk into the contractor's pricing, which usually costs you more than managing it yourself. If you are dollar-funded, consider converting at milestones rather than all at once across an 8&ndash;14 month build."),
  ("What should I insist on in a construction contract here?",
   "A fixed price with an itemised budget rather than open-ended cost-plus; payments against verified progress; a five to ten percent retention released after the snag list is closed; written, priced change orders before work proceeds; and an explicit exclusions list covering furniture, appliances, landscaping limits and utility connection fees. Never accept a schedule where a large payment falls due before matching work exists on site."),
 ],
}

CONTENT["pre-sale-vs-custom-build-riviera-maya"] = {
 "title": "Pre-Sale Condo vs Custom Build in the Riviera Maya: Honest Math",
 "desc": "Preventa condo or build your own villa? Capital timing, delivery risk, HOA and bylaw exposure, rental economics and exit liquidity compared side by side.",
 "intro": [
   "Two very different propositions compete for the same buyer here. A pre-sale (preventa) condo asks for a deposit and staged payments against a building that does not exist yet, promises a discount to finished value, and hands over a managed asset with amenities. A custom build asks you to buy land, commission a design, and manage a project &mdash; and hands over an asset nobody else controls.",
   "Both work. They fail differently, they suit different amounts of attention, and the usual comparison &mdash; price per square metre &mdash; is the least informative number available. Here is the comparison that matters, with the risks each side actually carries."
 ],
 "sections": [
  ("The Comparison That Matters",
   """    <div class="table-responsive">
    <table class="table table-bordered table-striped">
      <thead class="table-dark"><tr><th></th><th>Pre-sale condo</th><th>Custom build</th></tr></thead>
      <tbody>
        <tr><td><strong>Capital timing</strong></td><td>Deposit plus staged payments over the construction period; often the lowest entry cost</td><td>Land in full up front, then milestone payments over 8&ndash;14 months</td></tr>
        <tr><td><strong>Main risk</strong></td><td>Developer delivery &mdash; delay, specification changes, or non-completion</td><td>Budget and programme management; permit timelines</td></tr>
        <tr><td><strong>Control of the product</strong></td><td>None beyond finish selections</td><td>Total &mdash; layout, orientation, systems, specification</td></tr>
        <tr><td><strong>Ongoing charges</strong></td><td>HOA fee, which can rise and is outside your control</td><td>Your own maintenance only; HOA only if in a gated community</td></tr>
        <tr><td><strong>Rental restrictions</strong></td><td>Condo bylaws can limit or ban short-term rental, and can be amended by assembly</td><td>None imposed by others on a standalone house</td></tr>
        <tr><td><strong>Time to income</strong></td><td>At delivery, whenever the developer actually delivers</td><td>Predictable once permits are in hand; typically 10&ndash;16 months from start</td></tr>
        <tr><td><strong>Exit liquidity</strong></td><td>Easier &mdash; comparable units, a known product, a broader buyer pool</td><td>Slower &mdash; a unique house finds a narrower but sometimes better-paying buyer</td></tr>
        <tr><td><strong>Effort required</strong></td><td>Low</td><td>Moderate, or low with a turnkey builder handling design, permits and construction</td></tr>
      </tbody>
    </table>
    </div>"""),
  ("Where Pre-Sale Is the Right Choice &mdash; and How to De-Risk It",
   """    <p>Pre-sale genuinely suits several situations: a first purchase in Mexico where you do not yet know the market; a buyer who wants amenities &mdash; gym, concierge, roof pool &mdash; that a single house cannot justify; a buyer who wants to be entirely hands-off; and a buyer who wants a smaller entry ticket than land-plus-build requires. The discount to finished value is real, and in a rising market the staged payment structure is efficient.</p>
    <p>The risk is concentrated in one place: whether the developer delivers what was sold, on time. How to reduce it:</p>
    <ul>
      <li><strong>Check completed projects, not renders.</strong> Visit two or three buildings the developer has finished and speak to owners about delivery date, final specification and defect resolution.</li>
      <li><strong>Read the contract for what happens if they are late</strong> or if the specification changes. Many pre-sale contracts are strongly asymmetric &mdash; penalties for a buyer who is late with a payment, and little for a developer who is late with a building.</li>
      <li><strong>Verify the permits actually exist</strong> for the building being sold: land use, construction licence, environmental authorisation where required, and the condominium regime. Pre-sales launched before permits are in hand are where the worst outcomes occur.</li>
      <li><strong>Read the condominium regime and bylaws</strong> before signing, especially if rental income is part of your plan. This is the constraint people most often discover after closing.</li>
      <li><strong>Understand the HOA budget</strong> and how fees are set. Amenity-heavy buildings carry amenity-heavy fees, and fees rise.</li>
      <li><strong>Use a Mexican notary and an independent lawyer,</strong> not the developer's.</li>
    </ul>"""),
  ("Where a Custom Build Wins",
   """    <p>Build instead of buying pre-sale when any of these apply:</p>
    <ul>
      <li><strong>Rental income is central to the plan.</strong> A standalone house cannot have its business model voted away by an assembly, has no HOA fee taking a slice of gross, and can be designed for yield &mdash; en-suite bedrooms, a lock-off casita, a rooftop, a pool positioned for the photograph.</li>
      <li><strong>You want the house you actually want.</strong> Orientation against the sun and breeze, a terrace deep enough to use, ceiling height, a kitchen that suits how you cook, systems sized properly. None of these is available in a finished floor plate.</li>
      <li><strong>You value control of quality.</strong> You choose the substrate behind the melamine, the stainless grade, the glazing specification, the cistern size and the treatment plant. In a condo you inherit whatever hit the developer's budget.</li>
      <li><strong>You are buying for the long term.</strong> Over a ten-to-twenty-year hold, a well-built house with a treatment plant sized correctly and marine-grade fixings costs far less to own than a building whose common-element repairs arrive as special assessments.</li>
      <li><strong>The land has something a building cannot manufacture</strong> &mdash; a cenote, mature canopy, a canal frontage, genuine privacy.</li>
    </ul>
    <p><strong>Rough working numbers.</strong> A custom build is land plus construction: construction in a good rental-grade specification runs $18,000&ndash;$26,000 MXN/m&sup2; in the corridor, with land the variable that moves the total most &mdash; from modest inland lots to premium gated-community prices. Add design and engineering, permits, pool, furniture and contingency. Pre-sale pricing is quoted per m&sup2; of finished unit and looks lower than land-plus-build, but it includes a developer margin, buys you a share of common area you pay to maintain, and comes with the bylaw and HOA exposure above.</p>
    <p>The honest summary: pre-sale buys convenience and liquidity, and pays for it with control. A custom build buys control and yield, and pays for it with effort and a slower exit. If you want the second without the effort, that is exactly what a turnkey builder is for &mdash; we handle design, permits, construction and handover as one contract, which is the arrangement most of our foreign clients use precisely because they are not here to manage it themselves.</p>"""),
 ],
 "faq": [
  ("Is a pre-sale condo cheaper than building a house here?",
   "Per square metre of finished space it usually looks cheaper, and the entry ticket is certainly smaller. But that price includes a developer margin and a share of common areas you then pay to maintain through an HOA fee, and it comes with bylaw restrictions on rental. Land plus construction costs more up front and produces an asset nobody else controls."),
  ("What is the main risk of buying pre-sale in the Riviera Maya?",
   "Developer delivery &mdash; delay, changes to the specification, or non-completion. Reduce it by visiting completed projects and talking to their owners, verifying that the land use, construction licence, environmental authorisation and condominium regime actually exist for the building being sold, reading what the contract says about developer delay, and using your own lawyer rather than the developer's."),
  ("Which is better for rental income?",
   "A standalone house, in most cases. Condominium bylaws can restrict or prohibit short-term rental and can be amended by assembly after you buy, the HOA fee takes a slice of gross revenue, and you cannot design a finished unit for yield. A purpose-built villa can have en-suite bedrooms, a lock-off casita and a rooftop &mdash; the features that actually move nightly rate."),
  ("How long does a custom build take compared with waiting for a pre-sale?",
   "Ten to sixteen months from start on site, and predictable once the permits are in hand. A pre-sale delivers when the developer delivers, which may be on schedule or considerably later. The relevant comparison is not build time against zero, it is build time against the developer's actual track record on delivery dates."),
  ("Can I build without managing the project myself?",
   "Yes &mdash; that is what a turnkey contract is for. Design, engineering, permits, construction and handover under one fixed-price agreement, with milestone payments against verified progress and weekly photo and video reporting. Most of our foreign clients are not in Mexico during construction, and the reporting discipline is what makes that work."),
 ],
}

CONTENT["real-estate-investment-puerto-aventuras"] = {
 "title": "Investing in Puerto Aventuras: Who Rents There and Why",
 "desc": "The marina community's investment case: the family and boating rental market, HOA and dock costs, seasonality and how yields compare to Tulum.",
 "intro": [
   "Puerto Aventuras is the corridor's odd one out, and that is the whole investment thesis. It is a gated marina community with its own school, dolphin facility, golf, beach club and shops, twenty minutes south of Playa del Carmen &mdash; so it competes for a different guest and a different buyer than either the design-led Tulum market or the nightlife-driven Playa del Carmen one. Understanding who actually rents there is more useful than any headline yield figure.",
   "This looks at the demand profile, the ownership costs that are specific to a marina community, how the seasonality and the numbers compare with the alternatives, and what to check before buying &mdash; whether you buy a finished property or build."
 ],
 "sections": [
  ("Who Rents in Puerto Aventuras",
   """    <p>The guest mix here is distinctive and it shapes everything from unit sizing to review scores.</p>
    <ul>
      <li><strong>Families.</strong> Gated, walkable, calm, with a marina to look at and a beach club to use. Parents who would not book a Tulum jungle villa with a plunge pool and a toddler book here instead.</li>
      <li><strong>Multi-generational groups.</strong> Larger units and houses with several bedrooms and separated sleeping areas perform particularly well &mdash; grandparents plus parents plus children in one property.</li>
      <li><strong>Boaters and fishing guests.</strong> The marina is the only one of its kind in the immediate corridor. A property with or near a slip has a demand source nothing inland can replicate.</li>
      <li><strong>Divers and snorkellers.</strong> Cenote and reef access nearby, with the calm of a gated community at the end of the day.</li>
      <li><strong>Longer stays and snowbirds.</strong> A meaningful winter segment takes month-plus bookings &mdash; lower nightly rate, far lower turnover cost, and far kinder on the property.</li>
    </ul>
    <p>What this does <em>not</em> attract in volume: the young short-stay crowd chasing beach clubs and nightlife. That is a feature if you are optimising for wear, review quality and longer bookings, and a limitation if your pro forma assumes peak Tulum nightly rates.</p>"""),
  ("Ownership Costs Specific to a Marina Community",
   """    <p>The costs that catch investors out here are the community ones, and they need to be verified for the specific property rather than estimated.</p>
    <ul>
      <li><strong>HOA / maintenance fee.</strong> The community fee funds security, gates, common areas and services. Canal-front and marina-adjacent properties often carry more. Ask for the current fee, the budget behind it, and its history over the last five years &mdash; the trend matters more than the number.</li>
      <li><strong>Dock or slip charges,</strong> where applicable, are typically separate from the HOA fee, and a slip may be owned, leased or assigned &mdash; three quite different things legally and in resale.</li>
      <li><strong>Seawall and canal-edge maintenance</strong> on a canal-front property is an owner obligation that can become a significant repair. Assess the condition before purchase, not after.</li>
      <li><strong>Higher maintenance from salt exposure.</strong> Marine air on all exterior metalwork, AC condensers, gates and fixings. Properties specified with 316 stainless and marine-grade coatings cost less to own here by a wide margin, which is a real due-diligence question when buying an existing house.</li>
      <li><strong>Rental permissions.</strong> Confirm what the community and, in a condominium, the regime and bylaws actually permit for short-term rental, including minimum stays and guest access to amenities. This is the constraint most likely to break an investment plan, and it is checkable in an afternoon.</li>
      <li><strong>Property tax (predial) is modest by US and Canadian standards,</strong> and the lodging and income taxes on rental operation are the ones to model with a Mexican accountant.</li>
    </ul>"""),
  ("Seasonality, Comparison and What to Check",
   """    <p><strong>Seasonality</strong> follows the corridor: a strong high season from roughly December to April, a secondary summer peak from family travel, and a soft September&ndash;October during the heart of hurricane season, when many owners schedule maintenance and repainting. The family and snowbird mix here makes the shoulder seasons somewhat steadier than in markets dependent on short party-weekend stays &mdash; and the month-plus winter bookings smooth the calendar considerably.</p>
    <p><strong>How it compares.</strong> Tulum has historically shown the highest nightly rates and the most volatile occupancy, with a large and growing supply of design-led villas competing for the same guest. Playa del Carmen offers the deepest, most liquid market and the steadiest occupancy, at lower rates and with high competition. Puerto Aventuras sits in between: fewer competing properties, a differentiated product that nothing nearby replicates, moderate rates, good repeat-guest behaviour, and a narrower buyer pool at exit &mdash; which cuts both ways, since a well-specified canal-front house in a gated marina community has few genuine substitutes.</p>
    <p><strong>Before buying, check:</strong></p>
    <ol>
      <li>The current HOA fee, its five-year trend and the budget behind it.</li>
      <li>Whether short-term rental is permitted, at what minimum stay, and whether guests may use the amenities.</li>
      <li>The dock or slip status &mdash; owned, leased or assigned &mdash; and its cost.</li>
      <li>The condition of the seawall or canal edge, assessed by someone who will not be selling you the property.</li>
      <li>The exterior specification of an existing house: stainless grade, aluminium finish, condition of concrete at slab edges and balconies. Chloride damage is the expensive defect here and it is visible if you know where to look.</li>
      <li>What the design committee will permit if you intend to extend, remodel or rebuild.</li>
    </ol>
    <p>We work in Puerto Aventuras regularly on both new houses and renovations, and the pattern is consistent: the properties that perform are the ones whose exterior specification was right in the first place, and the ones that disappoint are usually fine houses with a decade of salt damage that was never budgeted for. If you are weighing a specific property, a pre-purchase condition assessment costs very little against the repair bill it either finds or rules out.</p>"""),
 ],
 "faq": [
  ("Who rents properties in Puerto Aventuras?",
   "Families, multi-generational groups, boaters and fishing guests, divers, and a meaningful winter segment taking month-plus stays. It does not draw the young short-stay nightlife crowd in volume &mdash; which means less wear, better reviews and longer bookings, but also that a pro forma built on peak Tulum nightly rates will not hold here."),
  ("What are the ownership costs in a marina community?",
   "The HOA maintenance fee covering security, gates and common areas &mdash; often higher for canal-front and marina-adjacent properties &mdash; plus separate dock or slip charges where applicable, seawall and canal-edge maintenance as an owner obligation, and higher exterior maintenance from salt exposure. Ask for the fee's five-year trend, not just the current figure."),
  ("How do returns compare with Tulum and Playa del Carmen?",
   "Tulum has historically shown the highest nightly rates with the most volatile occupancy and heavy new supply. Playa del Carmen is the deepest and most liquid market at lower rates. Puerto Aventuras sits between them: fewer competing properties, a differentiated product, moderate rates, strong repeat guests, and a narrower buyer pool at exit."),
  ("Can I rent my Puerto Aventuras property short-term?",
   "Usually, but confirm it specifically &mdash; the community's rules and, in a condominium, the regime and bylaws determine whether short-term rental is allowed, what minimum stay applies, and whether guests may use the amenities. It is the single most common reason an otherwise sound investment plan fails, and it takes an afternoon to verify."),
  ("What should I inspect before buying an existing house here?",
   "The exterior specification and its condition: stainless grade on fixings and railings, the aluminium finish on windows, and the state of the concrete at slab edges and balconies, where chloride damage shows first. Also the seawall or canal edge on a waterfront lot, the dock or slip status, and what the design committee will permit if you plan to remodel or extend."),
 ],
}

if __name__ == "__main__":
    slugs = sys.argv[1:] or sorted(CONTENT)
    for s in slugs:
        if s not in CONTENT:
            print(f"  ! no CONTENT for {s}"); continue
        print(f"  {rewrite(s):5d} unique words  blog/{s}.html")
