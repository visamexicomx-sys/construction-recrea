#!/usr/bin/env python3
"""English cluster for foreign buyers, built around the concierge / turnkey positioning.

Why English and why now: the Search Console export shows the United States alone at
4,084 impressions and 42 clicks last quarter (CTR 1.03%, avg position 8.47) — the
audience is already finding this site, and the pages they land on are not written for
them. "contractor near me" 119 impressions at position 4.6 with zero clicks;
"how much does it cost to build a house in mexico" at positions 1.0-3.5.

Semrush US volumes for the money terms:
  fideicomiso              3,600/mo  KD 16  CPC $2.28
  buying land in mexico      590/mo  KD 16  CPC $0.78
  moving to mexico from usa  320/mo  KD 17  CPC $1.63
  playa del carmen r/e     1,600/mo  KD 14

The concierge and remote-management pages carry little search volume on their own.
They exist because they are the offer: a foreign owner who lands on the fideicomiso
or land-buying page needs to see that someone can run the whole thing for them.

Deliberately not duplicated: /turnkey-construction-for-foreigners-riviera-maya/
already covers the build process for foreign owners (867 words). These pages cover
what comes before it (ownership structure, land) and what wraps around it (concierge
scope, remote supervision, build-versus-buy).
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'gsc', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-gsc-pages.py'))
gsc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gsc)

L_TURNKEY = ('/turnkey-construction-for-foreigners-riviera-maya/', 'Turnkey construction for foreign owners')
L_GC = ('/general-contractor-riviera-maya/', 'General contractor in the Riviera Maya')
L_COST = ('/cost-to-build-a-house-in-mexico/', 'Cost to build a house in Mexico')
L_PERM = ('/hotel-resort-construction-permits-quintana-roo/', 'Permits in Quintana Roo')
L_ENV = ('/environmental-permits-cancun-development/', 'Environmental permits')
L_SOIL = ('/mecanica-de-suelos/', 'Soils studies in limestone')

PAGES = {

'fideicomiso-mexico-guide': dict(lang='en',
  title='Fideicomiso in Mexico: How It Works, Cost, Renewal',
  desc='What a fideicomiso is, why the coastal restricted zone requires one, what it costs to set up and maintain, how it renews, and when a corporation is better.',
  h1='Fideicomiso: How Foreigners Own Coastal Property in Mexico',
  lead='A fideicomiso is not a lease and it is not a loophole. It is a bank trust that has been the standard way foreigners hold coastal property in Mexico for decades — and understanding it removes most of the fear people arrive with.',
  secs=[
   ('Why it exists at all',
    'The Mexican constitution restricts direct foreign ownership of land within roughly 50 kilometres of the coastline and 100 kilometres of the borders. Every beach town on this coast sits inside that restricted zone. Rather than closing the market, Mexico created the fideicomiso: a Mexican bank holds legal title as trustee, and you, the beneficiary, hold every practical right — to occupy, renovate, rent, sell, and pass the property to your heirs. The bank cannot sell, encumber or use the property. It follows your instructions.'),
   ('What it costs, honestly',
    'There is a one-time setup — the permit from the foreign affairs ministry, the bank\'s acceptance fee, and the notary work — and then an annual trustee fee for as long as you hold it. Figures vary by bank and by property value, so treat the table below as the planning range rather than a quote, and ask for the fee schedule in writing before choosing a trustee bank. Banks differ more than people expect.'),
   ('Term, renewal and inheritance',
    'The trust runs for 50 years and is renewable, and renewal is an administrative step rather than a negotiation. Your named substitute beneficiaries inherit the beneficial rights directly through the trust, which is one of the underrated advantages: it avoids the Mexican probate process that would otherwise apply. Name them when the trust is created and review the names after any change in your family.'),
   ('Fideicomiso or Mexican corporation',
    'A corporation makes sense when you are buying several properties, running a genuine business, or acquiring land for development. It has no annual trustee fee, but it does have accounting, monthly filings and a tax obligation whether or not it earns. For a single home or villa, the fideicomiso is almost always simpler and cheaper over time. Anyone advising you to form a corporation to hold one house should be able to explain the ongoing compliance cost, and often cannot.'),
   ('Where people get hurt',
    'Buying ejido land, which is communal and cannot be freely transferred until it has been properly regularised — this is the single most common way foreigners lose money in this region. Skipping the title search and the certificate of no encumbrances. Paying deposits outside of escrow or notary channels. Believing a seller who says the restricted zone does not apply to a particular lot. And using the seller\'s notary without question: the notario is a public official, but you may choose which one, and you should.'),
  ],
  table=('Item', 'What it is', 'Typical planning range',
   [('Setup: permit, bank acceptance, notary', 'One-time, at closing', '$1,500 – $3,000 USD'),
    ('Annual trustee fee', 'Paid to the bank each year', '$500 – $900 USD'),
    ('Acquisition tax and closing costs', 'ISAI, notary, registry', '5% – 8% of price'),
    ('Trust term', 'Renewable', '50 years'),
    ('Mexican corporation alternative', 'Setup plus ongoing accounting', 'Setup, then monthly filings')]),
  faq=[('Do I really own the property with a fideicomiso?',
        'You hold all beneficial rights: use it, renovate it, rent it, sell it, and leave it to your heirs. The bank holds legal title as trustee and acts on your instruction. It cannot sell or encumber the property, and it is not a landlord.'),
       ('How much does a fideicomiso cost per year?',
        'Plan on roughly $500 to $900 USD a year in trustee fees, plus a one-time setup at closing of about $1,500 to $3,000 USD. Fees vary between banks, so ask for the schedule in writing before you choose one.'),
       ('What happens after 50 years?',
        'The trust is renewed for another term. It is an administrative renewal, not a re-negotiation, and it can be done by you or by your heirs.'),
       ('Can I build a house on property held in a fideicomiso?',
        'Yes. Construction permits attach to the property and the project, not to the ownership structure. You commission the build the same way any owner would, and the DRO files with the municipality.'),
       ('Is a fideicomiso safe?',
        'It has been the standard structure for foreign coastal ownership in Mexico for decades and is used by hundreds of thousands of owners. The risk in a Mexican property purchase is almost never the trust — it is the title, the land classification and the paperwork behind them.')],
  links=[('/buying-land-in-mexico/', 'Buying land in Mexico: due diligence'),
         L_TURNKEY, L_COST,
         ('/concierge-construction-riviera-maya/', 'Concierge construction service')]),

'buying-land-in-mexico': dict(lang='en',
  title='Buying Land in Mexico: Due Diligence Checklist 2026',
  desc='What to verify before buying land in the Riviera Maya: title, ejido status, land use, topography, soils and closing costs, in the order that matters.',
  h1='Buying Land in Mexico: What to Verify Before You Sign',
  lead='Most bad land purchases on this coast were avoidable for a few thousand dollars of checks. Here is the order we run them in, and what each one is protecting you from.',
  secs=[
   ('Start with what kind of land it is',
    'Private property (propiedad privada) can be sold freely. Ejido land is communal, and until it has been formally regularised into private title it cannot be transferred to you no matter what document you are shown. This distinction has cost more foreign buyers more money in Quintana Roo than every other risk combined. Verify it at the public registry before anything else, and treat an unusually cheap beachfront or jungle lot as a reason for more diligence, not less.'),
   ('Title, encumbrances and who is actually selling',
    'Pull the property record and the certificate of no encumbrances. Confirm the seller is the registered owner, or holds a valid power of attorney. Check for liens, mortgages, unpaid property tax and any pending litigation. Confirm there is no unresolved inheritance among heirs — a common and slow-moving problem. Your notario does much of this, and you get to choose the notario rather than accepting the seller\'s.'),
   ('What you are allowed to build there',
    'Land use, density, ground coverage (COS), floor area ratio (CUS) and maximum height come from the municipal urban development programme, and they decide whether your plan fits before any architect draws anything. Check whether the lot touches a protected area, the federal maritime zone, a right of way or a cenote system. And if it is inside a gated development, get the internal regulations: they are usually stricter than the municipality.'),
   ('The physical checks',
    'A topographic survey tells you the real dimensions, the real boundaries and how the land falls — deeded area and actual area differ more often than buyers expect. A soils study tells you what is underneath: in fractured limestone, cavities and poorly compacted fill are the most expensive surprise in this region, and finding one after the structure is up is the worst possible timing. Confirm access, and confirm that power and water can actually be brought in and at what cost.'),
   ('Closing costs and taxes',
    'Budget 5% to 8% of the purchase price for acquisition tax, notary, registry and, in the restricted zone, setting up the fideicomiso. Property tax (predial) in this region is low by North American standards. When you eventually sell, capital gains tax applies, with exemptions that depend on residency and on the property having been your home — worth understanding at purchase rather than at sale.'),
  ],
  table=('Check', 'What it protects you from', 'Typical cost',
   [('Registry search and no-encumbrance certificate', 'Liens, disputed ownership', 'Included in notary work'),
    ('Ejido / private status verification', 'The most expensive mistake here', 'Included in notary work'),
    ('Land use certificate', 'Buying land you cannot build on', '$1,500 – $6,000 MXN'),
    ('Topographic survey', 'Wrong area, encroached boundaries', '$8,000 – $30,000 MXN'),
    ('Soils study', 'Cavities, fill, foundation surprises', '$18,000 – $55,000 MXN'),
    ('Closing costs', '—', '5% – 8% of price')]),
  faq=[('Can foreigners buy land in Mexico?',
        'Yes. Within about 50 km of the coast the purchase is held through a bank trust (fideicomiso) or a Mexican corporation. Outside that restricted zone, foreigners may hold title directly.'),
       ('What is ejido land and why does it matter?',
        'It is communal land. Until it has been formally regularised into private title it cannot be legally transferred to a foreign buyer. Buying it on a handshake or a private contract is the most common way people lose money on this coast.'),
       ('How much are closing costs in Mexico?',
        'Typically 5% to 8% of the purchase price, covering acquisition tax, notary fees, registry and — in the restricted zone — the setup of the fideicomiso.'),
       ('Should I get a soils study before buying?',
        'On this coast, yes, or at least make the offer conditional on one. Limestone varies between neighbouring lots, and the foundation is where an unexamined lot turns expensive.'),
       ('Can I choose my own notario?',
        'Yes, and you should. The notario is a public official who validates the transaction, but the buyer is entitled to select which one handles the closing.')],
  links=[('/fideicomiso-mexico-guide/', 'How a fideicomiso works'),
         L_SOIL, ('/estudio-topografico/', 'Topographic surveys'),
         ('/concierge-construction-riviera-maya/', 'Concierge construction service')]),

'concierge-construction-riviera-maya': dict(lang='en',
  title='Concierge Construction in the Riviera Maya | Recrea',
  desc='A concierge builder for owners abroad: land vetting, design, permits, construction, furnishing and rental setup under one point of contact.',
  h1='Concierge Construction: One Point of Contact, Start to Finish',
  lead='Most foreign owners do not want a contractor. They want one person who answers the phone, knows every moving part of their project, and hands them the keys to a finished, furnished house.',
  secs=[
   ('What concierge actually means here',
    'It means we take responsibility for the whole chain rather than one link of it: vetting the land before you buy, coordinating the notary and the trust, design and engineering, the permit file and the DRO, construction under a fixed-price contract, furnishing and equipping the house, connecting utilities, and setting it up for rental if that is the plan. You get one contact, one schedule and one budget, instead of six specialists blaming each other across two time zones.'),
   ('The scope, stage by stage',
    'Before purchase: land use, title status, topography, soils, and an honest opinion on whether the plot suits what you want. Design: architecture and engineering, with the specification adapted to salt, humidity and hurricane season rather than copied from a temperate-climate catalogue. Permits: the municipal file, the DRO, and the environmental file where it applies. Construction: fixed price against a line-item budget. Handover: furnishing, appliances, linens, staff introductions, rental listing setup and a maintenance plan.'),
   ('How it works when you live abroad',
    'Weekly photo reports with dates. Payments tied to verifiable milestones rather than the calendar. Video calls at the moments that cannot be reviewed later — reinforcement before a pour, services before they are closed up. Written approval for every change order, priced before it is executed. Documents in English. And someone in your time zone\'s working hours, because a project you cannot ask questions about is a project you are not really in control of.'),
   ('What it costs',
    'Construction is quoted the normal way: fixed price against a line-item budget. The concierge layer — the coordination, the vetting, the procurement and the setup — is quoted as a defined scope, not as a vague percentage on top of everything. The table shows how a full turnkey engagement is typically structured. What we do not do is hide a management margin inside inflated unit prices, which is the standard way this service is sold badly.'),
   ('Who this is not for',
    'If you live here, enjoy managing trades and want to buy your own materials, you do not need a concierge builder and we will say so. This service exists for owners who are 3,000 kilometres away, who value their time more than the last five percent of margin, and who would rather have one accountable party than a cheaper invoice with nobody standing behind it.'),
  ],
  table=('Stage', 'What we handle', 'How it is priced',
   [('Pre-purchase vetting', 'Land use, title, topography, soils', 'Fixed fee per lot'),
    ('Design and engineering', 'Architecture, structure, services', '4% – 8% of construction'),
    ('Permits and DRO', 'Municipal file, environmental where needed', 'Quoted per project'),
    ('Construction', 'Full build, fixed price', 'Line-item budget'),
    ('Furnishing and setup', 'Furniture, appliances, rental readiness', 'Quoted per scope'),
    ('Ongoing care', 'Maintenance, staff, oversight', 'Monthly')]),
  faq=[('What does a concierge builder do that a contractor does not?',
        'A contractor builds what the drawings say. We also vet the land before you buy it, run the design and the permit file, furnish the house, connect the services and set it up for rental — under one contact and one schedule.'),
       ('Can you help me before I have bought the land?',
        'That is the best moment to involve us. Land use, density, topography and soils decide what your plot is actually worth building on, and those checks cost a fraction of what a bad lot costs.'),
       ('Do you furnish the house as well?',
        'Yes — furniture, appliances, kitchen equipment and the details that make a house rentable from day one, quoted as a defined scope rather than an open budget.'),
       ('How do I know I am not being overcharged from abroad?',
        'Fixed price against a line-item budget with quantities and unit prices, payments tied to verified milestones, and every change order priced and signed before it is executed. You can hand that budget to another builder and compare it line by line.'),
       ('Which areas do you cover?',
        'Cancun, Puerto Morelos, Playa del Carmen, Puerto Aventuras, Akumal, Tulum, Cozumel and Isla Mujeres.')],
  links=[L_TURNKEY, ('/remote-construction-management-mexico/', 'Managing a build from abroad'),
         ('/buying-land-in-mexico/', 'Buying land: due diligence'), L_GC]),

'remote-construction-management-mexico': dict(lang='en',
  title='Managing a Construction Project in Mexico From Abroad',
  desc='How to run a build in Mexico from abroad: what to verify and when, what reports to demand, how to structure payments, and the moments you cannot review later.',
  h1='Managing a Build in Mexico From Abroad',
  lead='You can absolutely build here without living here. What decides the outcome is not how often you visit — it is whether the right things get verified at the five moments that cannot be revisited.',
  secs=[
   ('The moments that cannot be reviewed later',
    'Setting out and levels before excavation. Reinforcement in the foundation before the pour. Slab reinforcement, embedded services and pressure tests before the pour. Waterproofing before it is covered. Electrical and plumbing runs before walls are closed. Each of these lasts hours and determines the house. Everything else can be inspected afterwards; these cannot, without breaking something. If you take one thing from this page, make it this list.'),
   ('What to demand in the reporting',
    'Weekly written report with dated photographs of each stage before it is closed up, progress measured against the schedule, laboratory results for concrete, an observation log with owner and deadline, and a running record of change orders. Loose photos over a messaging app with no dates and no context are not a report — they are reassurance, and reassurance is exactly what a project in trouble produces most of.'),
   ('Structure payments so they protect you',
    'Tie payments to verifiable milestones, not calendar dates: foundation complete, structure and slabs, services closed, finishes, handover. Amortise any advance across each payment rather than leaving it outstanding to the end. Withhold a retention until the punch list is cleared. This one structural choice does more to protect a remote owner than any amount of supervision.'),
   ('Who represents you on site',
    'Three workable models. The builder\'s own supervision, adequate when the contract is fixed-price and the reporting is disciplined. An independent supervisor paid by you, typically 3% to 7% of construction cost, which buys a second set of eyes with no stake in the build. Or a trusted individual — an architect friend, a property manager — attending the critical pours. What does not work is nobody, on the assumption that photographs are the same thing as verification.'),
   ('Time zones, language and the paper trail',
    'Agree who answers, in what language and within what hours, before the contract is signed. Insist every instruction and approval goes through email or another written channel, even when a call already settled it. On a project running twelve to eighteen months across two languages and two time zones, the written trail is not bureaucracy — it is the only version of events that survives.'),
  ],
  table=('Stage', 'What must be verified', 'How',
   [('Setting out', 'Position, levels, setbacks', 'Photos plus survey reference'),
    ('Foundation reinforcement', 'Bar size, spacing, cover', 'Dated photos before pour'),
    ('Slab and services', 'Reinforcement, embedded runs, pressure test', 'Photos plus test records'),
    ('Waterproofing', 'Coverage, laps, upstands', 'Photos before covering'),
    ('Services in walls', 'Cable gauge, pipe runs, boxes', 'Photos before closing'),
    ('Handover', 'Punch list, as-builts, warranties', 'Signed handover record')]),
  faq=[('Can I build a house in Mexico without being there?',
        'Yes, and many owners do. It requires a fixed-price contract with a line-item budget, milestone-based payments, weekly dated photo reports and someone verifying the five stages that get covered up.'),
       ('Do I need an independent supervisor?',
        'It depends on your risk tolerance and the size of the project. With a fixed-price contract and disciplined reporting, many owners do not. On a large build, from abroad, an independent supervisor at 3% to 7% pays for itself.'),
       ('How often should I get updates?',
        'Weekly, in writing, with dated photos and progress against the schedule — plus a video call at each of the critical stages before anything is covered.'),
       ('What if something is built wrong?',
        'That is what the observation log and the retention are for: the defect is recorded with a responsible party and a deadline, and the final payment is not released until the list is cleared.')],
  links=[('/concierge-construction-riviera-maya/', 'Concierge construction service'),
         ('/supervision-de-obra/', 'Site supervision explained'),
         ('/contrato-de-obra/', 'What the construction contract must say'), L_TURNKEY]),

'build-or-buy-playa-del-carmen': dict(lang='en',
  title='Build or Buy in Playa del Carmen? A Straight Comparison',
  desc='Building versus buying a home in Playa del Carmen and Tulum: real cost per m², timelines, what you control, and which one suits your situation.',
  h1='Build or Buy in Playa del Carmen: An Honest Comparison',
  lead='We build houses, so read this with that in mind — and then notice how often the answer below is "buy". Both routes work here. They suit different people.',
  secs=[
   ('The cost comparison, without the sales pitch',
    'Building typically costs less per finished square metre than buying comparable finished property in the same area, and the gap widens at the higher end, where developer margin and furnishing packages are largest. But building adds costs that a purchase does not: land, design, permits, connections, and your own time across twelve to twenty-four months. When people say building is cheaper, they are usually comparing construction cost against a finished sale price, which is not the same comparison.'),
   ('Time, and what it is worth to you',
    'Buying can close in weeks. Building means land purchase, then permits, then seven to eleven months of construction for a normal house — realistically a year to two from decision to keys. If you need to be living or renting within a season, that decides it. If you are planning two years ahead, the calendar stops being an argument.'),
   ('What you get by building',
    'Specification suited to this climate rather than to a brochure: real waterproofing, stainless fixings, proper electrical capacity for air conditioning, treated wastewater, orientation that keeps the house cool. A layout built around how you actually live. And no inherited defects — which matters here, where a five-year-old house built badly for the salt and the rain shows it clearly.'),
   ('What you get by buying',
    'Certainty and speed. You see the finished thing, you know the number, you move in. In a strong development you also get amenities and rental infrastructure that would be impractical to replicate alone. The risk moves from execution risk — will this be built well and on budget — to inspection risk: is what I am looking at actually sound. A proper technical inspection before purchase is cheap and almost nobody does it.'),
   ('Which one suits you',
    'Buy if you need it soon, if you want a known number, or if you cannot give the project attention. Build if you have a year or two, want the house to be right for this climate, want control over the specification, or already own land. And if you are buying to rent, run both numbers against realistic occupancy rather than the optimistic figure in the listing — it changes the answer more often than the construction cost does.'),
  ],
  table=('Factor', 'Building', 'Buying',
   [('Time to keys', '12 – 24 months', 'Weeks'),
    ('Cost control', 'Fixed price, line-item budget', 'Known price, unknown defects'),
    ('Specification', 'Chosen for this climate', 'Whatever was built'),
    ('Effort required', 'Meaningful, even with a concierge builder', 'Low'),
    ('Main risk', 'Execution and schedule', 'Hidden condition'),
    ('Best for', 'Owners with time and a plot', 'Owners who need it now')]),
  faq=[('Is it cheaper to build or buy in Playa del Carmen?',
        'Building usually costs less per finished square metre, but you must add land, design, permits, connections and a year or more of your time. Against a finished, furnished property, the gap is narrower than most people assume.'),
       ('How long does it take to build a house here?',
        'Seven to eleven months of construction for a normal 150 to 200 m² house, plus permits beforehand. From decision to keys, plan on twelve to twenty-four months including the land purchase.'),
       ('Should I buy land first?',
        'Only after checking land use, density, topography and soils. A cheap lot you cannot build what you want on is not cheap. We run those checks before purchase precisely because they change the decision.'),
       ('What about buying to rent out?',
        'Run both options against realistic occupancy and real running costs — maintenance, pool, electricity with air conditioning, management fees — rather than the listing\'s projection. That comparison decides it more often than the construction cost does.')],
  links=[L_COST, ('/buying-land-in-mexico/', 'Buying land: due diligence'),
         ('/fideicomiso-mexico-guide/', 'How a fideicomiso works'),
         ('/concierge-construction-riviera-maya/', 'Concierge construction service')]),
}


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    texts = {}
    for slug, d in PAGES.items():
        os.makedirs(slug, exist_ok=True)
        html = gsc.build(slug, d, 'en')
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
        texts[slug] = set(tuple(body[i:i + 6]) for i in range(len(body) - 5))
        flag = '' if len(d['title']) <= 65 and len(d['desc']) <= 175 else '  <-- CHECK'
        print('%-42s T%2d D%3d words %4d%s' % (slug + '/', len(d['title']), len(d['desc']), len(body), flag))
    ks = list(texts)
    mx = max((len(texts[a] & texts[b]) / len(texts[a] | texts[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity: %.2f (%s vs %s)' % mx)
