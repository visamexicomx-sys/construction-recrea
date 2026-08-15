#!/usr/bin/env python3
"""Fourth English batch: the parts of the buyer journey still uncovered (2026-08-15).

Coverage audit first, keyword tool second — after three batches the remaining
value is in gaps, not in volume. Checked against every English page and blog post
on the site:

  closing / escrow / notario ...... nothing at all
  area comparison ................. one 665-word blog comparing two towns
  home insurance .................. only a construction-insurance post, which is
                                    a different product from homeowner cover
  utilities connection ............ buried inside a maintenance-costs post
  renting out legally ............. one 519-word casita post; nothing on SAT
                                    registration, IVA, or platform withholding

All five are questions a foreign buyer must answer before or immediately after
purchase, and all five are asked of us constantly. The tax and legal sections are
written as practical orientation with the limits stated plainly: rules change,
individual situations differ, and a Mexican contador signs off, not a builder.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'gsc', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-gsc-pages.py'))
gsc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gsc)

L_CONC = ('/concierge-construction-riviera-maya/', 'Concierge construction service')
L_LAND = ('/buying-land-in-mexico/', 'Buying land: due diligence')
L_FID = ('/fideicomiso-mexico-guide/', 'How a fideicomiso works')
L_INSP = ('/home-inspection-mexico/', 'Home inspection before buying')
L_MAINT = ('/villa-maintenance-riviera-maya/', 'Villa maintenance for absent owners')
L_FURN = ('/furnishing-a-vacation-rental-mexico/', 'Furnishing a vacation rental')
L_COST = ('/cost-to-build-a-house-in-mexico/', 'Cost to build a house in Mexico')
L_BUY = ('/build-or-buy-playa-del-carmen/', 'Build or buy?')

PAGES = {

'closing-process-buying-property-mexico': dict(lang='en',
  title='Closing on Property in Mexico: Process, Costs, Timeline',
  desc='How a property purchase actually closes in Mexico: offer, escrow, the notario, the fideicomiso permit, closing costs and how long each step really takes.',
  h1='The Closing Process When Buying Property in Mexico',
  lead='The Mexican closing is not the North American one with different paperwork. The notario is a public official rather than your advocate, escrow is optional rather than standard, and the timeline is set by documents you do not control.',
  secs=[
   ('Who the notario is, and who is not representing you',
    'A notario público in Mexico is a licensed public official who validates the transaction, verifies the title, calculates and withholds taxes, and registers the deed. That is a far larger role than a North American notary, and a fundamentally different one from a lawyer: the notario is not your advocate and does not negotiate on your behalf. If you want someone whose duty runs to you alone, retain your own attorney in addition. The buyer generally chooses the notario, which matters more than most buyers realise — use that choice rather than accepting the seller\'s by default.'),
   ('Offer, deposit and the promissory agreement',
    'A signed offer is followed by a promissory purchase agreement setting price, deadlines, penalties for either side and what happens if the trust permit is delayed. Read the default clauses carefully: this is where a deposit becomes non-refundable. Never send a deposit directly to a seller or an agent\'s personal account. Use escrow with a recognised provider, or the notario\'s account, and make the release conditions explicit in writing before any money moves.'),
   ('Due diligence, in parallel',
    'While the paperwork proceeds, verify: title at the public registry, certificate of no encumbrances, that the seller is the registered owner and any inheritance is resolved, no outstanding property tax, water bill or HOA arrears, that the construction matches what is registered, and land use if you plan to build or extend. On a resale, add a technical inspection. This period is short and the checks are cheap; skipping them is where expensive surprises originate.'),
   ('The trust permit and the closing itself',
    'In the coastal restricted zone, the fideicomiso requires a permit from the foreign affairs ministry and the trustee bank\'s acceptance. That step, more than anything the buyer does, sets the calendar. When it is in place, the notario prepares the deed, both parties sign, funds are released, taxes are withheld and paid, and the deed goes to the public registry. Registration itself takes additional weeks after you already hold the keys, which is normal.'),
   ('Costs and timeline',
    'Budget 5% to 8% of the purchase price in closing costs, more when a fideicomiso is being created. Below is how the calendar usually distributes. Cash purchases move faster; a Mexican mortgage adds appraisal and bank timelines on top.'),
   ('What goes wrong most often',
    'Deposits paid outside escrow. Promissory agreements signed without reading the default clauses. Assuming the trust permit is instant. Discovering unpermitted construction that is not in the registry, which becomes your problem when you resell. And using the seller\'s notario without question — legal, common, and not in your interest when something needs deciding.'),
  ],
  table=('Step', 'What happens', 'Typical duration',
   [('Offer and promissory agreement', 'Price, deadlines, penalties agreed', '1 – 2 weeks'),
    ('Escrow deposit', 'Funds held against written conditions', 'At signature'),
    ('Due diligence', 'Registry, encumbrances, debts, inspection', '2 – 4 weeks'),
    ('Fideicomiso permit and bank', 'Ministry permit, trustee acceptance', '4 – 10 weeks'),
    ('Closing at the notario', 'Deed signed, funds released, taxes withheld', '1 day'),
    ('Registration of the deed', 'Public registry entry', '4 – 12 weeks after closing')]),
  faq=[('How long does it take to close on property in Mexico?',
        'Typically two to four months for a coastal purchase requiring a fideicomiso, with the trust permit as the main variable. Outside the restricted zone and paying cash, it can be considerably faster.'),
       ('What are closing costs in Mexico?',
        'Usually 5% to 8% of the purchase price — acquisition tax, notary fees, registry and, in the restricted zone, setting up the trust. The buyer normally carries these; the seller carries capital gains withholding.'),
       ('Is escrow normal in Mexico?',
        'It is not automatic the way it is in the United States, but it is available and you should insist on it. Never send a deposit to a seller\'s or agent\'s personal account.'),
       ('Can I choose my own notario?',
        'Yes, and you should. The notario validates the transaction for the state, not for you, so the choice matters — and so does retaining your own attorney if you want advice that is on your side.'),
       ('Do I need to be in Mexico to close?',
        'Not necessarily. A power of attorney granted to someone you trust can allow closing in your absence, though it must be properly drafted and, if executed abroad, apostilled and translated.')],
  links=[L_FID, L_LAND, L_INSP, L_BUY]),

'where-to-build-riviera-maya-area-guide': dict(lang='en',
  title='Where to Build in the Riviera Maya: Area by Area',
  desc='An honest comparison of where to build on this coast: Playa del Carmen, Tulum, Puerto Aventuras, Akumal, Puerto Morelos, Cancun, Cozumel and Isla Mujeres.',
  h1='Where to Build in the Riviera Maya: An Area Guide',
  lead='We build in all of these places, so this is not a pitch for one of them. It is what each one is actually like to own in, and who each one suits.',
  secs=[
   ('Playa del Carmen and Puerto Aventuras',
    'Playa del Carmen is the practical middle of the coast: the deepest pool of trades and suppliers, hospitals, schools, an airport 45 minutes away, and the shortest construction timelines because everything is available locally. It is also the busiest, and the beachfront is largely built out. Puerto Aventuras, twenty minutes south, trades that energy for a gated marina community with a genuine year-round population — quieter, family-oriented, with internal rules that keep it that way and constrain what you can build.'),
   ('Tulum and Akumal',
    'Tulum has the strongest brand on the coast and the strictest permitting, which are related facts: the environmental file is a real barrier, and barriers protect what is already approved. It also has the most crowded condo supply and infrastructure that has lagged demand. Akumal, between the two, is quieter and more residential, with a protected bay and serious environmental scrutiny — good for a private villa, less so for someone who wants restaurants within walking distance.'),
   ('Puerto Morelos and Cancun',
    'Puerto Morelos keeps a fishing-village core with a national marine park offshore, twenty minutes from the airport, and remains the most understated option on the coast. Cancun is the largest market with the most infrastructure — hospitals, flights, services — and the widest range from hotel-zone condos to inland residential developments like Cumbres. If access and services matter more than seclusion, Cancun is objectively the practical choice, and it is the one people romanticise least.'),
   ('Cozumel and Isla Mujeres',
    'Both are islands, and that governs everything about building on them: material arrives by ferry or barge, costs roughly 15% more, and needs scheduling weeks ahead. In exchange you get a genuine island community, exceptional diving off Cozumel, and a pace the mainland lost years ago. Isla Mujeres also has a mainland portion — Costa Mujeres — which is a different proposition entirely: new hotel corridor, ordinary construction logistics.'),
   ('What actually decides it',
    'How often will you really be here, and will it be rented when you are not. Distance to the airport matters enormously if you visit for long weekends and not at all if you come for the season. Building costs vary only modestly across the mainland corridor; permit timelines vary a lot. And if rental income is part of the plan, competition varies far more than any of these factors — the same villa performs very differently in Tulum\'s crowded market than in Puerto Morelos.'),
  ],
  table=('Area', 'Suits', 'Build considerations',
   [('Playa del Carmen', 'Amenities, rental demand, convenience', 'Fastest supply chain, most trades'),
    ('Puerto Aventuras', 'Families, marina, gated quiet', 'Community rules govern design and hours'),
    ('Tulum', 'Brand, design-led villas', 'Strictest environmental permitting'),
    ('Akumal', 'Privacy, nature, private villas', 'High environmental scrutiny, thin local supply'),
    ('Puerto Morelos', 'Quiet, close to airport', 'Marine park shapes the environmental file'),
    ('Cancun', 'Services, flights, hospitals', 'Traffic-impact review, HOA rules'),
    ('Cozumel / Isla Mujeres', 'Island life, diving', 'Sea freight, roughly 15% cost premium')]),
  faq=[('Where is the best place to build on the Riviera Maya?',
        'It depends on how often you will be here and whether it will be rented. Playa del Carmen for convenience and rental demand, Puerto Aventuras or Akumal for quiet, Tulum for brand at the cost of permitting time, Puerto Morelos for proximity to the airport, Cancun for services.'),
       ('Is it much more expensive to build on Cozumel or Isla Mujeres?',
        'Around 15% more on the civil works, from sea freight, longer lead times and crew accommodation. We identify that separately in the budget rather than burying it in unit prices.'),
       ('Which area has the hardest permits?',
        'Tulum, followed by locations near protected areas such as Puerto Morelos and Akumal. The environmental component, not the municipal one, is what sets those timelines.'),
       ('Where is rental competition toughest?',
        'Small condo units in Tulum, where a lot of nearly identical supply chases the same guest. Private villas with real outdoor space compete in a much thinner market anywhere on the coast.')],
  links=[('/construccion-de-casas-riviera-maya/', 'Building houses across the region'),
         ('/tulum-investment-property-guide/', 'Is Tulum a good investment?'), L_LAND, L_CONC]),

'home-insurance-mexico-coastal': dict(lang='en',
  title='Home Insurance in Mexico: Hurricane and Coastal Cover',
  desc='Insuring a home on the Mexican Caribbean: what hurricane cover includes, the deductible that surprises owners, exclusions, and what insurers require.',
  h1='Home Insurance for a Coastal Property in Mexico',
  lead='Most disputes after a storm are not about whether the policy paid. They are about the deductible, the exclusions, and a valuation the owner never checked.',
  secs=[
   ('What a coastal policy usually contains',
    'Structure against named perils including hurricane and flood; contents; civil liability, which matters if you rent the property out; and often loss of rental income. Read how hurricane damage is defined: wind and rain entering through a breached opening is typically covered, while water rising from the ground — storm surge or flood — is frequently a separate item that must be added. That distinction is the single most common unpleasant surprise on this coast.'),
   ('The deductible nobody reads',
    'Hurricane deductibles are usually a percentage of the insured value rather than a fixed amount, and the percentage can be substantial. On a property insured for a few million pesos, that is a meaningful sum you carry yourself before the policy engages. It is the number to check first, before the premium, because it determines whether the policy responds to the loss you are actually worried about.'),
   ('What insurers want from the building',
    'Better construction earns better terms, and sometimes earns cover at all. Impact-rated glazing or shutters, a properly anchored roof, treated palapa thatch, documented compliance with permits, and evidence of maintenance all help. Unpermitted construction is a genuine problem: an addition that does not appear in the registry may simply not be covered, and nobody discovers that until they claim.'),
   ('Insuring during construction is a different policy',
    'A house being built is not covered by a homeowner policy. Construction all-risk cover, plus the contractor\'s civil liability and workers\' cover, is what protects that period — and it should be confirmed in the contract rather than assumed. Ask your builder for current certificates before work starts. We carry ours and expect to be asked.'),
   ('Practical steps that make a claim work',
    'Photograph the property annually and before hurricane season, and store the images off-site. Keep receipts for significant items and improvements. Confirm the insured value reflects reconstruction cost today, not the price you paid years ago. Know your broker\'s claim procedure before you need it. And after a storm, document damage before making even temporary repairs — necessary repairs are usually reimbursable, but only if the original state was recorded.'),
  ],
  table=('Element', 'What to check', 'Why it matters here',
   [('Hurricane deductible', 'Percentage of insured value', 'Often the largest number in the policy'),
    ('Flood and storm surge', 'Included or separate item', 'Frequently excluded by default'),
    ('Insured value', 'Reconstruction cost, not purchase price', 'Under-insurance reduces every payout'),
    ('Civil liability', 'Especially if renting to guests', 'Guest injury claims'),
    ('Loss of rental income', 'Period and conditions', 'Repairs can take months here'),
    ('Permitted construction', 'Registry matches what exists', 'Unpermitted work may not be covered')]),
  faq=[('Is hurricane damage covered by home insurance in Mexico?',
        'Wind damage and rain entering through a breach usually are. Flood and storm surge are often a separate item that must be added, and the hurricane deductible is normally a percentage of insured value rather than a fixed sum.'),
       ('Do I need insurance while my house is being built?',
        'Yes, and it is a different policy: construction all-risk, plus the contractor\'s civil liability and workers\' cover. Ask for current certificates before work starts.'),
       ('Does impact glazing reduce my premium?',
        'It can improve terms and, on some properties, availability of cover. Insurers respond to documented protection of openings, anchored roofs and evidence of maintenance.'),
       ('What if part of my house was built without a permit?',
        'It may not be covered, and you may not learn that until you claim. Regularising unpermitted work protects both the insurance position and the resale.')],
  links=[('/hurricane-proof-windows-and-doors/', 'Hurricane proof windows and doors'),
         L_MAINT, ('/blog/hurricane-season-preparation-checklist.html', 'Hurricane season checklist'), L_INSP]),

'utilities-for-a-new-home-mexico': dict(lang='en',
  title='Connecting Utilities for a New Home in Mexico',
  desc='Getting power, water, gas and internet to a new build in the Riviera Maya: what each connection requires, realistic timelines and costs.',
  h1='Connecting Utilities for a New Build',
  lead='The house is finished and there is no power. It happens more often than it should, and always for the same reason: connections were treated as the last step instead of an early one.',
  secs=[
   ('Electricity: start early, because it is the long one',
    'A permanent CFE connection requires the installation to be complete and compliant, with documentation and, above a certain load, its own transformer and the associated infrastructure — which is a project in itself, not a form. Rural or newly subdivided lots may have no nearby line at all, and extending one is the owner\'s cost, occasionally a large one. Establish availability and load capacity before buying the land, and file early. Construction runs on a temporary supply, which is normal, but a temporary supply is not a substitute for the permanent one.'),
   ('Water and drainage',
    'Where a municipal network exists, connection is straightforward and the house stores in a cistern regardless, because supply is not continuous everywhere. Where it does not, the property relies on a well or delivered water, both of which change the design. Drainage is the other half: in most of this region wastewater is treated on the property with a biodigester or a compact plant rather than infiltrated, and that decision belongs in the project from the first drawings because the authority reviews it.'),
   ('Gas',
    'Most homes use LP gas from a stationary tank on the property, sized to consumption and refilled by a supplier, with underground or surface distribution to the kitchen, heaters and any outdoor kitchen. Natural gas networks exist in parts of the region but are far from universal. Position the tank for delivery access and required clearances at design stage, not once the terrace is finished.'),
   ('Internet, which decides whether you can work here',
    'Fibre is available across most of the developed corridor and is genuinely good where it exists; coverage thins outside it, where fixed wireless or satellite fill the gap. If working remotely is part of the plan, verify the service at the specific address before buying — coverage maps are optimistic, and neighbours give better answers than providers. Run conduit and cabling through the house during construction, including the outdoor areas you will actually use.'),
   ('Costs and timelines',
    'Ranges for a residential property in the Riviera Maya. Electricity is the item that most often delays a handover, which is why we file for it while finishes are still in progress rather than afterwards.'),
  ],
  table=('Service', 'What it involves', 'Cost and timeline',
   [('CFE permanent connection', 'Compliant installation, documentation', '2 – 8 weeks after filing'),
    ('Transformer and infrastructure', 'Higher loads or distant lines', 'Per project, can be significant'),
    ('Water connection and cistern', 'Network connection plus storage', '$45,000 – $140,000 MXN'),
    ('Wastewater treatment', 'Biodigester or compact plant', '$25,000 – $600,000 MXN'),
    ('LP gas installation', 'Tank, distribution, safety', '$25,000 – $70,000 MXN'),
    ('Fibre internet', 'Where available at the address', '1 – 4 weeks')]),
  faq=[('How long does it take to get electricity connected in Mexico?',
        'Typically two to eight weeks after filing with a compliant installation. Where a transformer or line extension is needed, considerably longer — which is why availability should be checked before buying the land.'),
       ('Do I need a cistern if there is municipal water?',
        'Yes, in practice. Supply is not continuous or at constant pressure everywhere on this coast, so the house stores and pumps regardless of the connection.'),
       ('Is internet good enough to work remotely?',
        'Fibre across most of the developed corridor is genuinely good. Outside it, coverage thins. Verify at the specific address before buying, and run conduit during construction.'),
       ('What about gas?',
        'Most homes use LP gas from a stationary tank, sized to consumption. Position and clearances belong in the design, not in a decision made after the terrace is built.')],
  links=[('/water-supply-and-filtration-mexico/', 'Water supply and filtration'),
         ('/pozo-de-absorcion/', 'Wastewater in karst'),
         ('/instalacion-electrica-casa/', 'Electrical installation'), L_COST]),

'renting-out-your-property-in-mexico': dict(lang='en',
  title='Renting Out Your Property in Mexico: Rules and Tax',
  desc='What renting a home in Mexico actually involves: SAT registration and RFC, IVA and income tax, what platforms withhold, HOA and municipal rules, and running costs.',
  h1='Renting Out Your Property in Mexico',
  lead='Short-term rental here is entirely legal and entirely taxable. The owners who run into trouble are not the ones who pay tax — they are the ones who assumed a foreign platform handled everything for them.',
  secs=[
   ('You need to be registered, even as a non-resident',
    'Rental income from a Mexican property is taxable in Mexico regardless of where you live or where the guest paid. That means registering with the tax authority and obtaining an RFC, which also requires the paperwork behind it. Platforms operating in Mexico withhold tax on payouts, and the rate applied is generally better when you are registered than when you are not. Withholding is also not the end of the obligation: it is an advance against what you owe, not a substitute for filing.'),
   ('IVA, income tax and what a contador actually does',
    'Short-term lodging attracts value-added tax as well as income tax, and both have filing obligations that recur monthly rather than annually. Deductible expenses — maintenance, management fees, some depreciation, utilities attributable to the rental — change the outcome materially, and getting that right is the difference between an efficient structure and an expensive one. This is genuinely a job for a Mexican contador. We are builders; we will tell you the obligation exists and hand you to someone who signs off on it.'),
   ('HOA rules and municipal registration',
    'Before tax, check whether you are allowed to rent at all. Many condominiums and gated developments restrict or prohibit short-term rental, set minimum stays, or require guest registration — and those rules are enforced by the people you live among. Municipalities in Quintana Roo also apply a lodging tax on short-term stays, which platforms may or may not collect on your behalf depending on the arrangement in force.'),
   ('What it actually costs to operate',
    'The gap between gross bookings and what reaches you is larger than most projections show. Management takes a meaningful share of gross, cleaning is per stay, and platform fees, utilities under guest use — air conditioning runs continuously — pool and garden service, restocking, maintenance and taxes all come out before you do. Model with the table below rather than with a listing\'s projected yield.'),
   ('Building and furnishing for rental, not for yourself',
    'Rental properties fail on the boring things: hot water that runs out with a full house, air conditioning undersized for real occupancy, surfaces that cannot take rotation, not enough seating for the number the listing sleeps, and no storage for linens. If rental is the plan, that belongs in the design brief from the start — it is far cheaper than discovering it through reviews.'),
  ],
  table=('Cost', 'Typical share or amount', 'Note',
   [('Management', '15% – 30% of gross', 'Higher for full service'),
    ('Cleaning', 'Per stay', 'Often billed to the guest'),
    ('Platform fees', 'Varies by platform', 'Deducted before payout'),
    ('Utilities under guest use', 'Higher than owner use', 'Air conditioning runs constantly'),
    ('Pool, garden, maintenance', 'Monthly', 'Non-optional in this climate'),
    ('Taxes', 'Income tax plus IVA on lodging', 'Confirm with a contador')]),
  faq=[('Do I have to pay tax on rental income in Mexico?',
        'Yes. Rental income from a Mexican property is taxable in Mexico regardless of your residence or where the guest paid. Registration with the tax authority and an RFC are part of doing it properly.'),
       ('Does the booking platform handle my taxes?',
        'Platforms operating in Mexico withhold on payouts, and registered hosts generally face better rates than unregistered ones. Withholding is an advance, not a replacement for filing.'),
       ('Can my condo association stop me renting short-term?',
        'Frequently yes. Many condominiums and gated developments restrict or prohibit short-term rental or set minimum stays. Check before buying if rental income is part of your plan.'),
       ('What net return is realistic?',
        'That depends on segment, location and management, and any projection should be re-run with real running costs and the occupancy comparable listings actually achieve. Management alone takes 15% to 30% of gross before anything else.'),
       ('Do you handle the tax side?',
        'No — we are builders. We will tell you the obligations exist and refer you to a Mexican contador who signs off on them. Anyone in construction offering tax advice is outside their competence.')],
  links=[L_FURN, ('/tulum-investment-property-guide/', 'Is Tulum a good investment?'),
         ('/casita-guest-house-riviera-maya/', 'Casita and guest house'), L_MAINT]),
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
        print('%-44s T%2d D%3d words %4d%s' % (slug + '/', len(d['title']), len(d['desc']), len(body), flag))
    ks = list(texts)
    mx = max((len(texts[a] & texts[b]) / len(texts[a] | texts[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity: %.2f (%s vs %s)' % mx)
