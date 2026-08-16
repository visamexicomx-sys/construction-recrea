#!/usr/bin/env python3
"""English technical guides — fixing a defect as much as adding pages (2026-08-15).

An audit of internal links found English pages sending English readers to Spanish
guides: /mecanica-de-suelos/ from 3 English pages, /pozo-de-absorcion/ from 3,
/uso-de-suelo/ from 3, plus presupuesto, contrato and supervisión. Those links
were mine, added over the last few batches, and they are a real defect: a foreign
owner clicks "soils studies in limestone" and lands on a page in Spanish.

So this batch builds the English counterparts of the six guides English pages
actually needed, and repoints the links. They are written for a different reader
than the Spanish originals — the Spanish pages address someone who will manage
the process; these address an owner who has to know what to demand and how to
verify it was done. Written fresh rather than translated; cross-language overlap
is printed at the end.

Each pair is joined with hreflang so Google understands they are language
alternates rather than competitors.
"""
import os, re, json, importlib.util

spec = importlib.util.spec_from_file_location(
    'gsc', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-gsc-pages.py'))
gsc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gsc)

L_CONC = ('/concierge-construction-riviera-maya/', 'Concierge construction service')
L_REMOTE = ('/remote-construction-management-mexico/', 'Managing a build from abroad')
L_COST = ('/cost-to-build-a-house-in-mexico/', 'Cost to build a house in Mexico')
L_LAND = ('/buying-land-in-mexico/', 'Buying land: due diligence')
L_STALL = ('/finish-stalled-construction-project-mexico/', 'Taking over a stalled project')

# EN slug -> ES counterpart, for hreflang and for repointing English links
PAIRS = {
 'soil-study-mexico': 'mecanica-de-suelos',
 'wastewater-treatment-karst-mexico': 'pozo-de-absorcion',
 'land-use-cos-cus-mexico': 'uso-de-suelo',
 'construction-budget-mexico': 'presupuesto-de-obra',
 'construction-contract-mexico': 'contrato-de-obra',
 'site-supervision-mexico': 'supervision-de-obra',
}

PAGES = {

'soil-study-mexico': dict(lang='en',
  title='Soil Study Before Building in Mexico: What and Why',
  desc='Why a soils study is not optional on limestone: what it tests, what the report must tell your engineer, what it costs, and what happens to owners who skip it.',
  h1='Soil Study Before Building on Limestone',
  lead='This is the cheapest insurance available on this coast, and the most commonly skipped. Every expensive foundation story we have been called into begins with somebody deciding it was unnecessary.',
  secs=[
   ('What the ground here is actually like',
    'Fractured limestone, with sascab, fill and voids. Not the deep soft strata that dominate central Mexico — something less predictable in a different way. Two adjacent lots can need different foundations because one has a cavity at three metres and the other does not. The water table is shallow. Old fill from previous clearing is common and is frequently mistaken for natural ground. None of this is visible from the surface, and none of it is disclosed by a seller.'),
   ('What the study tests and what it delivers',
    'Borings and test pits, with additional exploration where voids are suspected. The report should give you: the stratigraphy, allowable bearing capacity, water table depth, a recommended foundation type with founding depth, and criteria for excavation and fill. That is what your structural engineer designs against. Without it they either guess and add cost as a safety margin, or guess and do not — and only one of those two errors is visible before you move in.'),
   ('What it costs',
    'Ranges for the Riviera Maya. Set against a foundation that has to be redesigned mid-excavation, or a structure that settles, the study is a rounding error — which is why it is worth insisting on even when the seller, the architect or the builder shrugs at it.'),
   ('When to commission it',
    'Ideally before you close on the land, or with the purchase conditional on the result. At minimum, before the design is finalised, because the foundation type affects both layout and budget. Commissioning it after the design is complete means either redesigning or accepting a more expensive foundation than the site needed. Commissioning it after excavation starts means finding out the expensive way.'),
   ('What to ask for as a foreign owner',
    'The report itself, not a summary — it should be a signed document with logs, not a paragraph in an email. The number and depth of borings, and where they were placed relative to your building footprint. Whether voids were specifically investigated. And confirmation that your structural engineer received it and designed to it, which is a separate question from whether it exists.'),
  ],
  table=('Scope', 'Applies to', 'Cost 2026',
   [('2 borings, single house', 'Lot up to 400 m²', '$18,000 – $32,000 MXN'),
    ('3–4 borings, large residence', 'Lot 400 – 1,500 m²', '$30,000 – $55,000 MXN'),
    ('Building or hotel study', 'Multiple storeys or basement', '$60,000 – $180,000 MXN'),
    ('Void investigation', 'Areas with known cavities', 'By extent')]),
  faq=[('Do I really need a soils study for one house?',
        'On fractured limestone, yes. The ground varies between neighbouring lots, and the two alternatives are paying for an over-engineered foundation or discovering a cavity with the structure already up.'),
       ('How much does a soils study cost in Mexico?',
        '$18,000 to $32,000 MXN for a single house on a lot up to 400 m², more for larger properties or where voids must be investigated.'),
       ('Can I use the neighbour\'s study?',
        'No. It is useful background, not a substitute. Limestone varies over short distances, and a void or old fill can sit in one lot and not the next.'),
       ('When should it be done?',
        'Before closing on the land if possible, or with the purchase conditional on it. At the latest, before the design is finalised — the foundation type changes both the layout and the budget.')],
  links=[L_LAND, L_COST, ('/mecanica-de-suelos/', 'Versión en español'), L_CONC]),

'wastewater-treatment-karst-mexico': dict(lang='en',
  title='Wastewater and Septic Systems in Karst: What Is Allowed',
  desc='Why soakaways for sewage are the wrong answer on the Yucatan peninsula, what authorities do authorise, and what biodigesters and compact plants cost.',
  h1='Wastewater on Limestone: What Is Actually Allowed',
  lead='The rock under this coast carries water to cenotes and to the reef within days. That single fact governs how every house here is allowed to deal with sewage.',
  secs=[
   ('Why a soakaway for sewage is not an option here',
    'The peninsula is fractured limestone. Water that infiltrates reaches the aquifer quickly, and the aquifer discharges into cenotes and offshore onto the reef. Infiltrating untreated wastewater contaminates the water the region drinks and swims in, which is why environmental authorities condition or reject projects that propose it — and why plenty of older houses here are quietly part of the problem. If a builder proposes a simple soakaway for black water, that alone tells you what kind of builder they are.'),
   ('What is authorised instead',
    'For a single house: a self-cleaning biodigester, sized by users and daily flow. For a hotel, a restaurant, several dwellings or anything with real volume: a compact treatment plant sized in cubic metres per day. Treated effluent may then be reused for irrigation or infiltrated according to what the permit authorises. Rainwater is a separate matter and can go to a properly sized soakaway, with a sediment trap and a grease separator where it collects runoff from paved areas.'),
   ('Costs',
    'Ranges for the Riviera Maya, installed. This belongs in the construction budget from the first drawings, not as an afterthought — it affects the site layout, the drainage design and the permit file.'),
   ('What the authority checks',
    'Distance to cenotes, water bodies and supply wells. Depth relative to the water table. Whether treatment precedes any infiltration. And evidence of maintenance. In or near a protected area — Puerto Morelos, Akumal, Tulum, Cozumel — this part of the file sets the schedule for the whole project, not just for the plumbing.'),
   ('Maintenance, which is where systems fail',
    'A biodigester needs periodic sludge purging — typically every 12 to 24 months depending on use — and an annual check. A compact plant needs more. Without that, the equipment stops performing, the permit condition is breached, and the neighbours notice before the authority does. If you are an absentee owner, put this in a maintenance contract rather than in your memory.'),
  ],
  table=('Solution', 'When it applies', 'Cost 2026',
   [('Biodigester, self-cleaning', 'Single house, 5 – 10 users', '$25,000 – $60,000 MXN'),
    ('Compact treatment plant', 'Hotel, restaurant, several dwellings', '$180,000 – $600,000 MXN'),
    ('Grease and solids trap', 'Kitchens and service areas', '$8,000 – $25,000 MXN'),
    ('Rainwater soakaway', 'Roof and paved runoff only', '$18,000 – $45,000 MXN')]),
  faq=[('Can I put in a septic tank or soakaway in Quintana Roo?',
        'Not as the solution for sewage. The karst carries whatever is infiltrated to the aquifer, then to cenotes and the reef. What is authorised is treatment first — a biodigester or compact plant — with any infiltration applying to treated effluent under the permit.'),
       ('What does a biodigester cost?',
        '$25,000 to $60,000 MXN installed for a house, plus a sludge register. Maintenance is periodic purging every 12 to 24 months and an annual check.'),
       ('Does this affect my construction permit?',
        'Yes. The wastewater solution is part of the submitted project, and near protected areas it is among the first things reviewed and the most common reason a file is returned.'),
       ('What about rainwater?',
        'Rainwater is different and can go to a properly sized soakaway, with sediment and grease separation where it collects runoff from paved areas.')],
  links=[('/water-supply-and-filtration-mexico/', 'Water supply and filtration'),
         ('/utilities-for-a-new-home-mexico/', 'Connecting utilities'),
         ('/pozo-de-absorcion/', 'Versión en español'), L_CONC]),

'land-use-cos-cus-mexico': dict(lang='en',
  title='Land Use, Density, COS and CUS in Mexico Explained',
  desc='What the land-use certificate controls: permitted use, density, ground coverage (COS), floor area ratio (CUS) and height — and how to check it before buying a lot.',
  h1='Land Use, Density, COS and CUS',
  lead='Five numbers on one municipal document decide what your lot is worth building on. Buyers routinely spend six figures before checking any of them.',
  secs=[
   ('What the certificate actually states',
    'The municipal urban development programme assigns each lot a use — residential, mixed, tourist, commercial, conservation — and with it the limits that govern your project: density in dwellings or rooms per hectare; COS, the proportion of the lot your building footprint may occupy; CUS, the total built area you may have across all floors; maximum height in storeys; and required setbacks. Those five numbers determine the viability of a project before any architect draws a line.'),
   ('COS and CUS, in plain terms',
    'COS limits footprint: a COS of 0.6 on a 500 m² lot allows 300 m² of ground coverage. CUS limits total construction: a CUS of 1.2 on the same lot allows 600 m² across all levels. Together with the height limit they define the actual envelope. A lot with a generous CUS and a low height limit is a different building from one with the reverse, even though the totals look similar on paper.'),
   ('How to obtain it, and when',
    'Request the land-use certificate from the municipal urban development office with the cadastral key and the lot details. Some municipalities publish cartographic viewers, useful as a preliminary reference, but the document issued by the authority is the one that governs and the one the permit file needs. Get it before you buy — or make the offer conditional on it — not after you have commissioned a design.'),
   ('The things that override it',
    'Inside a gated development, the internal regulations frequently impose stricter setbacks, lower heights, mandatory materials and colours, construction hours and completion deadlines. Those are enforceable against you regardless of what the municipality permits. Protected areas, the federal maritime zone and rights of way impose their own restrictions on top. Check all of them together, in the same week, before you commit.'),
   ('Costs and timelines',
    'These are the documents that precede any design work, with typical municipal figures for the region.'),
  ],
  table=('Document', 'What it gives you', 'Cost and time',
   [('Land use certificate', 'Use, density, COS, CUS, height', '$1,500 – $6,000 MXN · 1 – 3 weeks'),
    ('Alignment and official number', 'Boundaries and frontage', '$800 – $3,500 MXN · 1 – 2 weeks'),
    ('Services feasibility', 'Water, drainage, power availability', 'Per utility · 2 – 6 weeks'),
    ('Construction licence', 'Authorises the works, with DRO', 'By area · 3 – 10 weeks')]),
  faq=[('How do I find out the land use of a lot in Mexico?',
        'Request the land-use certificate from the municipal urban development office using the cadastral key. Online cartographic viewers are a useful preliminary reference but the issued document is what governs.'),
       ('What do COS and CUS mean?',
        'COS is the proportion of the lot the building footprint may occupy. CUS is the total built area permitted across all floors. Together with the height limit they define what you can actually build.'),
       ('Can land use be changed?',
        'Procedures exist but they are slow and uncertain, and depend on the urban development programme in force. Buying a lot on the assumption that use will change is taking a risk, not making a plan.'),
       ('Can the gated community rules be stricter than the municipality?',
        'Frequently, and they are enforceable: greater setbacks, lower heights, mandatory materials, working hours and completion deadlines. Review them alongside the land use, before design.')],
  links=[L_LAND, ('/closing-process-buying-property-mexico/', 'The closing process'),
         ('/uso-de-suelo/', 'Versión en español'), L_CONC]),

'construction-budget-mexico': dict(lang='en',
  title='Construction Budget in Mexico: How to Read a Real One',
  desc='What a line-item construction budget must contain, how cost distributes across trades, and how to compare two quotes without being fooled.',
  h1='How to Read a Construction Budget',
  lead='A serious budget is not a number. It is a list of items with quantities, unit prices and a defined scope — and the difference between that and a one-page quote is most of the risk you carry.',
  secs=[
   ('What a proper budget contains',
    'Preliminaries and setting out; excavation and foundations; structure; masonry and slabs; plumbing, electrical, gas and air conditioning; waterproofing; renders, floors and paint; joinery and metalwork; glazing; bathroom and kitchen fittings; cistern, pump and tank; final cleaning and testing. Each with a unit, a quantity, a unit price and a total. Plus overheads, supervision, profit and tax shown separately. If those last three are not separated, the document cannot be compared with anything.'),
   ('How the cost distributes',
    'Approximate shares for a mid-range house on this coast. They vary with design, but they are enough to spot an unbalanced budget at a glance — a finishes line at 12% or a foundation line at 4% is telling you something before you read the detail.'),
   ('Comparing two quotes without being fooled',
    'Compare line by line, never by total. Confirm both include the same items with the same quantities — the cheaper one has usually omitted three. Compare unit prices rather than totals. Ask what happens if steel or cement moves during the works. Confirm who pays permits, testing and final cleaning. And treat a lump-sum quote as what it is: a number that cannot be verified, from someone who would rather it were not.'),
   ('The omissions that reappear as extras',
    'Quantities given "as a lot" for work that is measured per square metre. Finishes described as "high quality" with no brand or model. Services with no gauge, diameter or capacity specified. Pool, landscaping or boundary wall mentioned in the description but absent from the totals. And the big one: a budget produced without an executive project, which is not a budget at all — nobody can quantify what has not been drawn.'),
   ('Fixed price or cost-plus',
    'Fixed price against a line-item budget puts the performance risk on the builder and gives you a number you can hold them to; it requires a complete design. Cost-plus only works if you are on site, supervising, and willing to absorb variation — which describes very few foreign owners. We work fixed-price by line item, and change orders are priced and signed before they are executed.'),
  ],
  table=('Section', 'Share of construction cost', 'Note',
   [('Preliminaries and foundations', '12% – 18%', 'Higher where limestone complicates excavation'),
    ('Structure and masonry', '25% – 32%', 'Concrete, steel, walls, slabs'),
    ('Services: plumbing, electrical, AC', '14% – 18%', 'Includes cistern and pumping'),
    ('Finishes', '22% – 30%', 'The section that varies most by level'),
    ('Joinery, metalwork, glazing', '8% – 12%', 'Kitchen, closets, doors, windows'),
    ('External works and cleaning', '4% – 8%', 'Paths, garden, handover')]),
  faq=[('What should a construction budget include?',
        'Every trade as a separate line with unit, quantity, unit price and total, plus overheads, supervision, profit and tax shown separately. Anything less cannot be compared or verified.'),
       ('Why do two quotes for the same house differ by 40%?',
        'Almost never the margin — the scope. One includes complete services, specified finishes and permits; the other omits them or describes them without quantifying. Compared line by line, the real gap is usually much smaller.'),
       ('Should I take fixed price or cost-plus?',
        'Fixed price against a line-item budget if you want predictability, and especially if you are not here to supervise. Cost-plus transfers the risk to the person least able to control it.'),
       ('Does the budget include the land?',
        'No. Construction budgets cover construction. Land, notary, taxes, furniture and often the pool are separate — confirm which in writing rather than assuming.')],
  links=[('/construction-contract-mexico/', 'The construction contract'),
         L_COST, ('/presupuesto-de-obra/', 'Versión en español'), L_REMOTE]),

'construction-contract-mexico': dict(lang='en',
  title='Construction Contract in Mexico: Clauses to Insist On',
  desc='What a construction contract must contain in Mexico: scope, milestone payments, change orders, penalties, warranty and termination clauses.',
  h1='The Construction Contract: Clauses to Insist On',
  lead='Most construction disputes are not technical. They are about scope and payments, and both are settled — or lost — in the contract, months before anyone argues.',
  secs=[
   ('Scope, defined by documents rather than adjectives',
    'The contract must attach the line-item budget, the drawings and the specifications, each identified by date and version. "A house of approximately 200 m² to a high standard" is not a scope; it is an invitation to a disagreement. Everything the owner assumes is included and is not written down will be an extra, and it will be an extra at a moment when you have no leverage.'),
   ('Payments tied to verified progress',
    'Payments should follow milestones that can be inspected — foundation complete, structure and slabs, services closed, finishes, handover — not calendar dates. Any advance should amortise proportionally across each payment rather than sitting outstanding until the end. Hold a retention until the punch list is cleared. For an owner abroad, this structure protects more than any amount of supervision does.'),
   ('Change orders, priced before execution',
    'Every change, whether you asked for it or the site forced it, must be documented before it is executed, with its cost and its effect on the schedule. Without that mechanism a project advances on verbal agreements and produces a final invoice nobody recognises. With it, the final number is explainable line by line — which is the entire point.'),
   ('Time, penalties and legitimate extensions',
    'Start date, completion date, and a defined list of what justifies an extension: extraordinary rain, owner-requested changes, authority delays outside the builder\'s control. Plus a delay penalty and its cap. A contract with no completion date is a contract that only protects one party, and it is not you.'),
   ('Warranty, insurance and termination',
    'A written warranty against hidden defects, with what it covers, for how long and how to report. Confirmation of the builder\'s civil liability and workers\' cover, with current certificates. And termination clauses with how the settlement is calculated — for work executed and verified, materials on site, and any penalty. Nobody signs a contract expecting to use that clause, which is exactly why it gets left out.'),
  ],
  table=('Item', 'Sound practice', 'Warning sign',
   [('Advance payment', 'Amortised across each payment', 'Large advance, never amortised'),
    ('Payments', 'Tied to verified progress', 'Fixed calendar dates, no inspection'),
    ('Changes', 'Priced and signed before execution', 'Verbal agreements on site'),
    ('Completion', 'Date plus defined extensions', 'No completion date at all'),
    ('Warranty', 'Written, scoped, time-limited', '"Guaranteed" with no terms'),
    ('Termination', 'Settlement method defined', 'Clause absent entirely')]),
  faq=[('What must a construction contract in Mexico include?',
        'Scope with the line-item budget and dated drawings attached, milestone-based payments, a written change-order procedure, completion date with defined extensions, delay penalty, warranty against hidden defects, insurance, and termination terms.'),
       ('Does the contract need a notary?',
        'Not for validity between the parties. What matters far more is that the annexes — budget, drawings, specifications — are identified and attached, because disputes are about scope, not about signatures.'),
       ('How much advance payment is normal?',
        'Enough to cover mobilisation and initial materials, amortised proportionally across each subsequent payment. The percentage matters less than whether it is amortised and backed by verified progress.'),
       ('What if the builder is late?',
        'The agreed penalty applies, except for extensions the contract defines as legitimate. That is why the extension list must be written down rather than argued about afterwards.')],
  links=[('/construction-budget-mexico/', 'How to read a construction budget'),
         ('/site-supervision-mexico/', 'Site supervision'),
         ('/contrato-de-obra/', 'Versión en español'), L_STALL]),

'site-supervision-mexico': dict(lang='en',
  title='Site Supervision in Mexico: What Gets Checked and When',
  desc='What construction supervision actually verifies, the moments that cannot be reviewed later, what the record should contain, and what independent supervision costs.',
  h1='Site Supervision: What Gets Checked, and When',
  lead='Supervision is not visiting the site. It is verifying specific things at specific moments — most of which last a few hours and then disappear under concrete.',
  secs=[
   ('The moments that cannot be revisited',
    'Setting out and levels before excavation. Foundation reinforcement before the pour. Slab reinforcement, embedded services and pressure testing before the pour. Waterproofing before it is covered. Electrical and plumbing runs before walls are closed. Everything else on a construction site can be inspected later; these five cannot, without breaking something. A supervision arrangement that does not guarantee attendance at these is decoration.'),
   ('What is actually verified',
    'That what is built matches the drawings and the specification. Bar size, spacing and cover in reinforcement. Concrete strength and slump, with sampling. Cable gauges, pipe diameters and equipment capacities. Levels, plumb and dimensions. Drainage falls. Hydraulic and electrical testing. And that materials delivered are the ones quoted, rather than an equivalent that costs the builder less.'),
   ('What the record must contain',
    'A site log with dates. Dated photographs of each stage before it is closed. Laboratory results. An observation list with a responsible party and a deadline against each item. And a change-order register. For an owner abroad, this file is the only real access you have to what happened — which is why loose photographs sent over a messaging app do not qualify.'),
   ('What it costs',
    'Independent supervision is charged as a percentage of construction cost or per scheduled visit. Where the builder is contracted fixed-price, their own supervision is part of the service; independent supervision is engaged separately, precisely so that the person checking is not the person being checked.'),
   ('Do you need independent supervision?',
    'Honest answer: not always. With a fixed-price contract, a line-item budget, milestone payments and disciplined weekly reporting, many owners do not. Where it earns its fee is on large projects, on complex sites, and where the owner is abroad and has nobody they trust attending the pours. We will tell you which of those applies to your project rather than selling you the service by default.'),
  ],
  table=('Stage', 'What must be verified', 'How it is evidenced',
   [('Setting out', 'Position, levels, setbacks', 'Photos plus survey reference'),
    ('Foundation reinforcement', 'Bar size, spacing, cover', 'Dated photos before pour'),
    ('Slab and services', 'Reinforcement, embedded runs, pressure test', 'Photos plus test records'),
    ('Waterproofing', 'Coverage, laps, upstands', 'Photos before covering'),
    ('Services in walls', 'Gauges, diameters, boxes', 'Photos before closing'),
    ('Handover', 'Punch list, as-builts, warranties', 'Signed handover record')]),
  faq=[('How much does independent site supervision cost?',
        'Typically 3% to 7% of construction cost for continuous supervision, or per scheduled visit where only the critical stages need attendance.'),
       ('Is it worth it if I already have a good builder?',
        'It depends on project size and whether you can be present. With a fixed-price contract and disciplined reporting many owners do without it. On a large build managed from abroad, it usually pays for itself.'),
       ('What should I receive during construction?',
        'A weekly written report with dated photographs of each stage before it is covered, progress against the schedule, laboratory results, and an observation list with owners and deadlines.'),
       ('Can I supervise from another country?',
        'Partly. You can require reports, photographs and test results, and approve changes in writing. What cannot be done remotely is verifying reinforcement before a pour — that needs someone you trust on site that day.')],
  links=[('/construction-contract-mexico/', 'The construction contract'), L_REMOTE,
         ('/supervision-de-obra/', 'Versión en español'), L_STALL]),
}


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    texts = {}
    for slug, d in PAGES.items():
        os.makedirs(slug, exist_ok=True)
        html = gsc.build(slug, d, 'en')
        # hreflang pairing with the Spanish counterpart
        es = PAIRS[slug]
        alt = ('  <link rel="alternate" hreflang="en" href="https://construction-recrea.com/%s/">\n'
               '  <link rel="alternate" hreflang="es" href="https://construction-recrea.com/%s/">\n'
               '  <link rel="alternate" hreflang="x-default" href="https://construction-recrea.com/%s/">\n'
               % (slug, es, slug))
        html = html.replace('</head>', alt + '</head>', 1)
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        # and the same pair declared on the Spanish page
        esf = os.path.join(es, 'index.html')
        if os.path.exists(esf):
            s = open(esf, encoding='utf-8').read()
            s = re.sub(r'\s*<link rel="alternate" hreflang="(en|es|x-default)"[^>]*>', '', s)
            s = s.replace('</head>', alt.replace('x-default" href="https://construction-recrea.com/%s/' % slug,
                                                 'x-default" href="https://construction-recrea.com/%s/' % es) + '</head>', 1)
            open(esf, 'w', encoding='utf-8').write(s)
        body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
        texts[slug] = set(tuple(body[i:i + 6]) for i in range(len(body) - 5))
        flag = '' if len(d['title']) <= 65 and len(d['desc']) <= 175 else '  <-- CHECK'
        print('%-38s T%2d D%3d words %4d  hreflang<->/%s/%s'
              % (slug + '/', len(d['title']), len(d['desc']), len(body), es, flag))

    # confirm these are not translations
    worst = 0
    for en_slug, es_slug in PAIRS.items():
        esf = os.path.join(es_slug, 'index.html')
        if not os.path.exists(esf):
            continue
        s = open(esf, encoding='utf-8').read()
        b = re.sub(r'<[^>]+>', ' ', s[s.index('<h1'):s.index('<footer')]).lower().split()
        sb = set(tuple(b[i:i + 6]) for i in range(len(b) - 5))
        worst = max(worst, len(texts[en_slug] & sb) / len(texts[en_slug] | sb))
    print('worst EN/ES pair overlap: %.3f' % worst)
    ks = list(texts)
    mx = max((len(texts[a] & texts[b]) / len(texts[a] | texts[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity within batch: %.2f (%s vs %s)' % mx)
