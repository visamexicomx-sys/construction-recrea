#!/usr/bin/env python3
"""Third English batch for foreign owners (checked 2026-08-14).

A note on keyword selection, because this batch rejected more than it accepted.
Semrush US shows huge volume on generic home-services queries — roof replacement
cost 22,200/mo, whole house water filtration 90,500, home generator installation
40,500, smart home installation 18,100. Those searchers are homeowners in Ohio.
Ranking for them would produce traffic that can never become a client, so the
batch skips all of them.

What it builds instead: topics where the searcher plausibly wants a builder on
this coast, and where the site has either nothing or something too thin to rank.

  outdoor-kitchen-riviera-maya    1,000/mo US + 320 MX, CPC $2.38 — only a blog
                                  post that splits the topic with palapas
  palapa-roof-construction          170/mo US + 20 MX, CPC $1.67 — blog is 469 words
  casita-guest-house-riviera-maya   170/mo US, KD 14 — blog is 519 words
  water-supply-and-filtration       Mexico-qualified slice of a 90,500/mo generic;
                                    the question every foreign owner asks first
  home-inspection-mexico            Mexico-qualified slice of 40,500/mo generic
  villa-maintenance-riviera-maya    almost no search volume, high conversion value:
                                    it is the recurring half of the concierge offer
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'gsc', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-gsc-pages.py'))
gsc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gsc)

L_CONC = ('/concierge-construction-riviera-maya/', 'Concierge construction service')
L_REMOTE = ('/remote-construction-management-mexico/', 'Managing a build from abroad')
L_TURNKEY = ('/turnkey-construction-for-foreigners-riviera-maya/', 'Turnkey construction for foreign owners')
L_LAND = ('/buying-land-in-mexico/', 'Buying land: due diligence')
L_COST = ('/cost-to-build-a-house-in-mexico/', 'Cost to build a house in Mexico')
L_FURN = ('/furnishing-a-vacation-rental-mexico/', 'Furnishing a vacation rental')
L_GC = ('/general-contractor-riviera-maya/', 'General contractor in the Riviera Maya')

PAGES = {

'outdoor-kitchen-riviera-maya': dict(lang='en',
  title='Outdoor Kitchen Cost and Design in the Riviera Maya',
  desc='Building an outdoor kitchen on the Caribbean coast: what survives salt and rain, layout that works, services to run first, and real costs per configuration in 2026.',
  h1='Outdoor Kitchen: Cost, Design and What Survives Here',
  lead='On this coast the outdoor kitchen gets used more than the indoor one. It also gets destroyed faster, because most of them are built with indoor materials.',
  secs=[
   ('Materials that last, and the ones that do not',
    'What fails: standard stainless of low grade, which pits and rusts within a couple of seasons near the sea; particleboard or MDF carcasses, which swell the first humid summer; ordinary hinges and drawer runners; and untreated softwood. What lasts: masonry or concrete carcasses finished in chukum, tile or stone; marine-grade or high-grade stainless appliances and doors; solid dense hardwood; powder-coated aluminium; and stone or concrete worktops. The price difference is real, and so is the difference between a kitchen that looks good in year five and one that is embarrassing in year two.'),
   ('Layout that actually works outdoors',
    'Put the grill downwind of the seating, not upwind of it. Give yourself worktop on both sides of the grill — the single most common regret. Keep the sink close to the grill rather than at the far end. Provide shade over the cook, not only over the guests; standing at a grill in direct afternoon sun is what makes an outdoor kitchen go unused. And plan storage that closes properly, because anything left open here collects humidity, insects and dust.'),
   ('Services to run before anything is built',
    'Gas line with a shut-off, water supply and a drain that goes somewhere legitimate, dedicated electrical circuits for refrigeration and outlets with proper outdoor-rated enclosures, and lighting on its own switch. All of it is cheap while the terrace is open and expensive once it is finished. If the outdoor kitchen is even a possibility, leave the services stubbed out during construction.'),
   ('Costs in 2026',
    'Ranges for a complete installation in the Riviera Maya, including masonry, finishes, services and mid-range appliances. Appliances are the swing factor: a high-end imported grill can cost more than the entire structure around it.'),
   ('Roof or no roof',
    'A palapa or pergola over the kitchen extends its life substantially — it keeps direct rain off the appliances and the cook out of the sun. It also changes the project: a solid roof over a cooking area needs ventilation planning, and a palapa over a grill needs correct clearances and a heat-resistant zone above it. Neither is complicated; both are frequently ignored.'),
  ],
  table=('Configuration', 'What it includes', 'Cost 2026',
   [('Compact grill station', 'Masonry base, worktop, grill', '$65,000 – $140,000 MXN'),
    ('Standard outdoor kitchen', 'Grill, sink, storage, worktop, services', '$150,000 – $350,000 MXN'),
    ('Full outdoor kitchen with bar', 'Adds refrigeration, bar seating, lighting', '$350,000 – $700,000 MXN'),
    ('Under palapa or pergola', 'Structure over the cooking area', 'Adds $80,000 – $250,000 MXN')]),
  faq=[('How much does an outdoor kitchen cost in the Riviera Maya?',
        'From $65,000 MXN for a compact grill station to $350,000–$700,000 MXN for a full outdoor kitchen with bar and refrigeration. Appliances are the biggest variable.'),
       ('What materials survive the salt air?',
        'Masonry or concrete carcasses finished in chukum, tile or stone; high-grade stainless; dense hardwoods; powder-coated aluminium. Anything with particleboard, low-grade stainless or ordinary hardware fails quickly here.'),
       ('Do I need a roof over it?',
        'Not required, but a palapa or pergola meaningfully extends the life of appliances and makes the kitchen usable in the afternoon. It needs correct clearances above a grill, which is often overlooked.'),
       ('Can it be added to an existing terrace?',
        'Yes, provided the terrace can take the load and the services can be routed. Running gas, water, drainage and dedicated circuits into a finished terrace is the part that drives the cost.')],
  links=[('/palapa-roof-construction/', 'Palapa roof construction'),
         ('/pergola-de-madera/', 'Pergolas in tropical climate'), L_CONC, L_COST]),

'palapa-roof-construction': dict(lang='en',
  title='Palapa Roof Construction: Cost, Lifespan, Permits',
  desc='How a real palapa is built: hardwood frame, huano palm thatch, what it costs per m² in 2026, how long the thatch lasts, fire treatment and maintenance.',
  h1='Palapa Roof Construction: Cost, Lifespan and Care',
  lead='The palapa is the one piece of regional architecture that outperforms anything imported: it is cooler than a solid roof, it survives hurricanes better than it looks, and it has been built here for centuries.',
  secs=[
   ('How a real palapa is built',
    'A frame of dense local hardwood — chicozapote, tzalam or chechén — with the palm thatch tied in overlapping layers from the eave upward. The steep pitch is not aesthetic: it is what sheds tropical rain fast enough that water never sits in the thatch. Good palapas are tied, not nailed through, so the structure flexes in wind instead of tearing. Everything about the form is a solution to this specific climate, arrived at long before anyone calculated it.'),
   ('Why it stays cool',
    'Thatch is a thick, ventilated, low-density layer: it absorbs solar radiation at the surface and lets the heat dissipate into moving air rather than radiating it down into the room. The high ceiling volume lets hot air rise well above the people below. In practice a palapa-covered terrace runs noticeably cooler than the same terrace under a concrete slab, with no energy cost at all.'),
   ('Lifespan and what really determines it',
    'Well-built huano thatch typically lasts around 8 to 15 years before it needs replacing, and the range is wide because of what sits around it. Shade and constant damp shorten it — a palapa under trees that never dries out fails much sooner than one in open sun. Ventilation underneath extends it. So does keeping the pitch steep and the layering correct. The frame, in dense hardwood, outlives several thatch cycles.'),
   ('Costs in 2026',
    'Ranges per m² of covered area in the Riviera Maya, including hardwood frame, thatch, fixings and installation. Re-thatching later costs far less than the original because the frame stays.'),
   ('Fire treatment, permits and insurance',
    'Thatch can be treated with a fire retardant, and for commercial or rental properties it usually should be — many insurers and some municipalities require it, and it is far cheaper applied during construction. Check whether your municipality or development has rules about palapa height and location, and if the property is insured, confirm with the insurer before building rather than after a claim.'),
  ],
  table=('Element', 'Detail', 'Cost 2026 per m²',
   [('Palapa, hardwood frame and huano thatch', 'Complete, new build', '$4,000 – $9,000 MXN'),
    ('Premium hardwood frame', 'Chicozapote, exposed joinery', '$7,000 – $12,000 MXN'),
    ('Re-thatching an existing palapa', 'Frame retained', '$1,500 – $3,500 MXN'),
    ('Fire-retardant treatment', 'Applied during construction', 'Adds $250 – $600 MXN')]),
  faq=[('How much does a palapa cost?',
        'Between $4,000 and $9,000 MXN per m² of covered area for a new palapa with a hardwood frame and huano thatch, and $7,000 to $12,000 MXN for premium framing with exposed joinery.'),
       ('How long does a palapa roof last?',
        'The thatch typically lasts 8 to 15 years depending on sun, ventilation and how well it was layered. The hardwood frame outlives several thatch cycles, which is why re-thatching costs a fraction of the original.'),
       ('Do palapas survive hurricanes?',
        'Better than people expect, when built correctly: the frame is anchored, the thatch is tied in layers rather than fixed rigidly, and wind passes through instead of lifting a sealed surface. Badly built ones lose thatch, which is repairable.'),
       ('Is a palapa a fire risk?',
        'Untreated thatch burns. Fire-retardant treatment is available, is far cheaper applied during construction, and is often required for commercial or rental properties and by insurers.'),
       ('Can I put a palapa over an outdoor kitchen?',
        'Yes, and it is a good combination, provided the design keeps correct clearance and a heat-resistant zone above the grill and allows smoke to escape.')],
  links=[('/outdoor-kitchen-riviera-maya/', 'Outdoor kitchens'),
         ('/blog-es/guia-construccion-palapas.html', 'Guía de palapas (ES)'),
         ('/pergola-de-madera/', 'Pergolas and hardwood'), L_GC]),

'casita-guest-house-riviera-maya': dict(lang='en',
  title='Casita Guest House: Cost, Rules and Rental Return',
  desc='Building a casita or guest house on your lot in the Riviera Maya: what density and land use allow, real construction costs in 2026, and whether renting it out pays.',
  h1='Casita and Guest House Construction',
  lead='A casita is the cheapest square metre you will ever add to a property — if the land use allows a second dwelling. That single check decides the whole project.',
  secs=[
   ('Check density before you design anything',
    'The municipal land-use certificate states how many dwellings are permitted on the lot, along with ground coverage and floor area limits. A casita as a genuinely separate dwelling with its own kitchen may or may not be allowed; a guest suite without a full kitchen is treated differently in many cases. Inside a gated development, the internal rules often prohibit a second dwelling regardless of what the municipality permits. Verify both before spending money on drawings — this is where casita projects die.'),
   ('Why the cost per m² is lower',
    'The expensive parts of a house are the kitchen, the bathrooms, the services and the site work. A casita shares the site, the connections and often the pool with the main house, so the marginal cost of adding 40 to 60 m² is much lower than building the same area as a standalone home. That is what makes it the best-value expansion on most lots — and why it is often the first thing we suggest to owners who think they need to sell and move.'),
   ('Sizing it to be genuinely useful',
    'Around 35 to 45 m² gives a studio that works: sleeping area, decent bathroom, kitchenette, and a covered outdoor space that makes it feel larger than it is. Around 55 to 70 m² gives a real one-bedroom. Below 30 m² it starts to feel like a hotel room, which limits both guest satisfaction and rental appeal. Give it its own entrance and some acoustic separation from the main house — privacy is the entire value proposition, for family and for guests alike.'),
   ('Costs in 2026',
    'Ranges for a casita built alongside an existing house in the Riviera Maya, including its own bathroom and kitchenette, sharing connections with the main property.'),
   ('Renting it out: the honest arithmetic',
    'A well-built casita in a good location can rent, and because the marginal construction cost is low, the return on that increment is usually better than on the main house. But it changes how you live: guests on your lot, cleaning turnovers, and management. It also has to comply — separate access, safety, and whatever registration and taxation apply to short-term rental in your municipality. Decide whether you want that before you build, not after the first booking.'),
  ],
  table=('Size', 'What it gives you', 'Cost 2026',
   [('Studio, 35 – 45 m²', 'Sleeping area, bathroom, kitchenette', '$700,000 – $1,300,000 MXN'),
    ('One-bedroom, 55 – 70 m²', 'Separate bedroom, full bathroom, kitchen', '$1,100,000 – $2,000,000 MXN'),
    ('Two-bedroom casita, 80 – 100 m²', 'Family or long-stay use', '$1,700,000 – $3,000,000 MXN'),
    ('Furnishing package', 'Rental-ready', '$120,000 – $300,000 MXN')]),
  faq=[('Can I build a casita on my lot in Mexico?',
        'It depends on the density permitted by the land-use certificate and, inside a gated development, on the internal rules. Both must be checked before design, because a second dwelling is not automatically allowed.'),
       ('How much does a casita cost to build?',
        'Roughly $700,000 to $1,300,000 MXN for a 35–45 m² studio and $1,100,000 to $2,000,000 MXN for a one-bedroom, when built alongside an existing house that already has connections.'),
       ('Is a casita a good rental investment?',
        'The return on the increment is usually better than on the main house because the marginal construction cost is low. What it costs you is privacy and management, which is a lifestyle decision more than a financial one.'),
       ('What size should it be?',
        '35 to 45 m² for a comfortable studio, 55 to 70 m² for a real one-bedroom. Below 30 m² it stops feeling like a home, which shows up in both guest reviews and family use.')],
  links=[L_FURN, ('/uso-de-suelo/', 'Land use, density, COS and CUS'),
         ('/tulum-investment-property-guide/', 'Is Tulum a good investment?'), L_CONC]),

'water-supply-and-filtration-mexico': dict(lang='en',
  title='Water in a Riviera Maya Home: Supply, Storage, Filtering',
  desc='How water works in a Caribbean-coast home: cistern and pump, pressure, whole-house filtration, drinking water, and what hard limestone water costs you.',
  h1='Water in Your Home: Supply, Storage and Filtration',
  lead='This is the first question almost every foreign owner asks, and the answer is more reassuring than the rumours: the plumbing here is fine. It is the hardness and the storage that need designing.',
  secs=[
   ('How water actually reaches a house here',
    'Municipal supply arrives at variable pressure and is not continuous everywhere, so houses store: a cistern at or below ground level, then a pump that pressurises the house, often with a hydropneumatic tank or a variable-speed pump to keep pressure steady. Some properties add a rooftop tank as gravity backup. This is why a house here has more waterworks than a house in North America — the storage is what turns an intermittent supply into a normal shower.'),
   ('Hard water, and what it costs you',
    'The aquifer runs through limestone, so the water is hard: high in dissolved calcium. Left untreated it scales up water heaters, shortens the life of taps and shower valves, spots glass and tile, stiffens laundry and blocks aerators. It is not a health issue; it is a maintenance and equipment issue, and it is entirely solvable with a softener sized for the house. Skipping it is a decision to replace fixtures and heaters years earlier than you should.'),
   ('A filtration setup that makes sense',
    'A workable layered approach: sediment filtration at the cistern outlet to protect the pump; a softener for the whole house to stop scale; carbon for taste and odour on the drinking line; and a point-of-use unit — reverse osmosis or equivalent — at the kitchen for drinking and cooking. That last stage is what lets you stop buying garrafones, which is both a cost and a logistics saving over a year.'),
   ('Costs in 2026',
    'Ranges for a residential property in the Riviera Maya, installed. The cistern is usually part of the construction budget; the treatment train is often added later, which costs more than including it during the build.'),
   ('Hot water and pool interaction',
    'Gas instant heaters are the norm and work well when sized correctly and protected from scale; solar thermal makes real sense in this climate and pays back quickly. Whichever you choose, hard water is its main enemy, which is another argument for softening upstream. If there is a pool, keep its top-up line and chemistry entirely separate from domestic treatment — connecting them is a mistake that shows up as ruined equipment.'),
  ],
  table=('Element', 'What it does', 'Cost 2026 installed',
   [('Cistern and pump', 'Storage plus house pressure', '$45,000 – $140,000 MXN'),
    ('Sediment filtration', 'Protects pump and fixtures', '$6,000 – $18,000 MXN'),
    ('Whole-house softener', 'Stops limestone scale', '$25,000 – $70,000 MXN'),
    ('Drinking water unit at kitchen', 'Replaces bottled water', '$8,000 – $25,000 MXN'),
    ('Solar water heating', 'Cuts gas consumption', '$30,000 – $90,000 MXN')]),
  faq=[('Can you drink the tap water in the Riviera Maya?',
        'Most residents do not drink it untreated, and use bottled water or a point-of-use unit. With proper filtration at the kitchen, drinking your own tap water is entirely practical and cheaper over a year than buying bottles.'),
       ('Why does a house here need a cistern and a pump?',
        'Because municipal supply is not continuous or at constant pressure everywhere. The cistern stores, the pump pressurises, and together they turn an intermittent supply into a normal shower.'),
       ('Do I need a water softener?',
        'On this coast, yes if you care about your equipment. Limestone-hard water scales water heaters, shortens the life of taps and valves, and spots glass and tile. A softener is cheaper than replacing them early.'),
       ('What does it cost to set up water properly?',
        'A cistern and pump run $45,000 to $140,000 MXN, and a full treatment train — sediment, softener, drinking unit — adds roughly $40,000 to $110,000 MXN. Including it during construction costs less than retrofitting.')],
  links=[('/captacion-de-agua-de-lluvia/', 'Rainwater harvesting'),
         ('/pozo-de-absorcion/', 'Wastewater in karst'),
         ('/plumbing-playa-del-carmen/', 'Plumbing services'), L_CONC]),

'home-inspection-mexico': dict(lang='en',
  title='Home Inspection in Mexico: What to Check Before Buying',
  desc='A technical inspection before buying property in the Riviera Maya: structure, waterproofing, electrical, plumbing, salt damage and what a report should cost you.',
  h1='Home Inspection Before Buying in the Riviera Maya',
  lead='Almost nobody commissions one here, which is exactly why it is worth doing. A few thousand pesos of inspection routinely finds problems that cost hundreds of thousands to fix.',
  secs=[
   ('Why it matters more on this coast',
    'Salt, humidity, intense rain and a construction boom that outpaced quality control. A house here can look immaculate and be five years from serious repair: waterproofing at the end of its life, reinforcement corroding where cover was too thin, an electrical installation with no proper earth, or a pool structure with a slow leak. None of that is visible on a viewing, and none of it is disclosed by a seller who may not know it either.'),
   ('What a proper inspection covers',
    'Structure: cracks and their type, deflection, signs of settlement, exposed or corroding reinforcement. Envelope: roof waterproofing condition and age, terraces, window and door sealing, evidence of past leaks. Services: electrical panel, circuits, earthing, water pressure, drainage falls, wastewater treatment and whether it is compliant. Pool: structure, equipment and leaks. Plus damp mapping, because damp is the region\'s most common and most misdiagnosed defect.'),
   ('What it costs and what it saves',
    'A technical inspection of a house or condo here costs a fraction of one month of the mortgage you are about to take on, and the findings either give you a repair budget or a negotiating position. The most common outcome is not walking away — it is adjusting the price or having the seller resolve specific items before closing.'),
   ('The paperwork inspection matters as much',
    'The physical condition is only half. Confirm the property is registered as it exists — unpermitted additions are common and become your problem at resale. Check for outstanding property tax, HOA arrears and utility debt, all of which follow the property. Confirm the seller\'s title and that any inheritance has been resolved. Your notario covers much of this, and you get to choose the notario.'),
   ('New construction and pre-sale',
    'A new build deserves an inspection too, at the right moment: before you accept handover, while the developer still has an incentive to fix things. For a pre-sale unit, the useful inspection points are during construction rather than at the end — the same principle that applies to a private build, where reinforcement and services must be seen before they are covered.'),
  ],
  table=('Area', 'What is checked', 'Why it matters here',
   [('Structure', 'Cracks, deflection, reinforcement cover', 'Salt corrodes under-covered steel'),
    ('Waterproofing', 'Roof, terraces, age and condition', 'The most common expensive defect'),
    ('Electrical', 'Panel, circuits, earthing, protection', 'Earthing is frequently absent'),
    ('Water and drainage', 'Pressure, falls, wastewater compliance', 'Non-compliant systems become your problem'),
    ('Pool and equipment', 'Structure, leaks, plant condition', 'Leaks hide in the ground'),
    ('Documents', 'Registration, permits, debts, HOA', 'Unpermitted works surface at resale')]),
  faq=[('Are home inspections normal in Mexico?',
        'They are far less common than in the United States or Canada, which is precisely why they are worth doing. Nothing prevents you from commissioning one, and sellers rarely object.'),
       ('What does a home inspection cost in the Riviera Maya?',
        'A fraction of what a single undetected defect costs. The usual outcome is not walking away from the purchase but adjusting the price or having specific items repaired before closing.'),
       ('What is the most common problem found?',
        'Waterproofing at or past the end of its life, followed by damp from filtration or condensation, and electrical installations without proper earthing.'),
       ('Should I inspect a brand-new property?',
        'Yes, before accepting handover, while the developer still has an incentive to correct things. For pre-sale units the valuable checks happen during construction, not at the end.')],
  links=[L_LAND, ('/humedad-en-paredes/', 'Damp: causes and remedies'),
         ('/grietas-en-muros/', 'Cracks: which ones matter'), L_CONC]),

'villa-maintenance-riviera-maya': dict(lang='en',
  title='Villa Maintenance in the Riviera Maya for Absent Owners',
  desc='What a home on this coast needs to stay in good condition: the maintenance calendar, hurricane-season preparation, costs, and how it works from abroad.',
  h1='Villa Maintenance for Owners Who Live Abroad',
  lead='This climate does not pause while you are away. A house left unattended for a season here does not simply gather dust — it degrades, and the repairs cost multiples of the maintenance that would have prevented them.',
  secs=[
   ('What this climate does to an empty house',
    'Humidity finds every closed, unventilated space and turns it into mould — closets, under sinks, behind furniture. Air conditioning left off for months lets that spread; left on unattended, a blocked condensate drain floods a ceiling. Pool chemistry collapses in days without service and algae can require draining. Salt corrodes hardware, hinges and outdoor fixtures continuously. Gardens grow at a rate northern owners consistently underestimate. Insects find any gap. None of this is dramatic in month one; all of it is expensive by month six.'),
   ('The maintenance calendar that actually matters',
    'Weekly: pool service, garden, and a walk-through with photographs. Monthly: run every tap and flush every toilet to keep traps sealed, check air conditioning condensate drains, test the pump. Quarterly: clean air conditioning filters and coils, check hardware and lubricate, inspect seals and silicone. Annually: roof waterproofing inspection before the rains, gutter and drain clearing, electrical check, servicing of pumps and heaters, and repainting on the schedule the exposure demands rather than when it looks bad.'),
   ('Hurricane season, specifically',
    'Before the season: trim trees away from the roof, confirm shutters or impact glazing work, clear all drains, photograph the property for insurance, and confirm the policy is current. Before a specific storm: secure or store outdoor furniture, lower the pool level, shut off gas, and protect openings. After: inspect the roof and drains before the next rain, not after the damage appears. An owner abroad needs someone with keys and authority to do all of this on short notice — that is the part that cannot be arranged remotely once a storm is named.'),
   ('Costs in 2026',
    'Typical monthly ranges for a private villa on this coast. Pool and garden are the recurring core; the rest scales with the size and exposure of the property.'),
   ('What we do for owners who are not here',
    'Scheduled maintenance with a written checklist and dated photographs after each visit, so you can see what was done rather than take it on trust. Emergency response with your pre-approved spending limit, so a leak is fixed on the day instead of waiting for a time zone to wake up. Pre-arrival preparation. And an annual condition report with a budget for what the property will need in the coming year, which is what turns maintenance from a series of surprises into a plan.'),
  ],
  table=('Service', 'Frequency', 'Cost 2026',
   [('Pool service', 'Weekly', '$1,500 – $4,000 MXN/month'),
    ('Garden and landscaping', 'Weekly or biweekly', '$2,000 – $6,000 MXN/month'),
    ('Property check with photo report', 'Weekly', '$1,500 – $3,500 MXN/month'),
    ('Air conditioning service', 'Quarterly', '$800 – $2,000 MXN per unit/visit'),
    ('Annual condition report and budget', 'Yearly', 'Per property'),
    ('Hurricane preparation', 'Seasonal', 'Per property')]),
  faq=[('What does villa maintenance cost in the Riviera Maya?',
        'Pool service runs $1,500 to $4,000 MXN a month and garden care $2,000 to $6,000, with a weekly property check adding $1,500 to $3,500. A full programme for a private villa typically lands in the middle of those combined ranges.'),
       ('What happens to a house left empty for six months here?',
        'Mould in unventilated spaces, pool chemistry collapse, corroded hardware, overgrown garden, and any small leak becoming a large one. The repairs cost several times what the maintenance would have.'),
       ('Should I leave the air conditioning running while away?',
        'Running it unattended risks a blocked condensate drain flooding a ceiling; leaving everything closed and off invites mould. The workable answer is controlled ventilation plus a scheduled visit that checks drains and runs the systems.'),
       ('Can you prepare the property for hurricane season?',
        'Yes: tree trimming, shutters or glazing checked, drains cleared, insurance documentation photographed, and storm-specific preparation when one is named. That last part requires someone here with keys and authority, agreed in advance.')],
  links=[L_CONC, ('/hurricane-proof-windows-and-doors/', 'Hurricane proof windows and doors'),
         L_FURN, ('/blog/hurricane-season-preparation-checklist.html', 'Hurricane season checklist')]),
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
        flag = '' if len(d['title']) <= 65 and len(d['desc']) <= 165 else '  <-- CHECK'
        print('%-38s T%2d D%3d words %4d%s' % (slug + '/', len(d['title']), len(d['desc']), len(body), flag))
    ks = list(texts)
    mx = max((len(texts[a] & texts[b]) / len(texts[a] | texts[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity: %.2f (%s vs %s)' % mx)
