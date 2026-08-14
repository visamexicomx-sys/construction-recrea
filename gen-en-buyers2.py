#!/usr/bin/env python3
"""Second English batch for foreign owners (Semrush US, checked 2026-08-14).

  how long does it take to build a house  6,600/mo  KD 14  CPC $3.11   GAP
  hurricane proof windows                 1,300/mo  KD 37  CPC $7.74   GAP
  condo remodel                             210/mo  KD 27  CPC $8.38   only Puerto Aventuras existed
  tulum real estate investment              110/mo  KD 14              GAP
  furnishing a vacation rental               50/mo  KD 16  CPC $1.22   GAP

Deliberately not built: a "hurricane proof house" page. That query is already
served by /blog/hurricane-proof-construction.html (1,049 words), so the batch
takes the glazing sub-topic instead, where the CPC is $7.74 and nothing on the
site competes. Two condo pages are added for Playa del Carmen and Cancun, since
only Puerto Aventuras had one and the phrase foreign owners use is "remodel".

The Tulum investment page is written to be useful rather than promotional: it
says plainly where the market has oversupplied and what that means for a build
decision. A page that only says yes is worth nothing to someone deciding.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'gsc', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-gsc-pages.py'))
gsc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gsc)

L_CONC = ('/concierge-construction-riviera-maya/', 'Concierge construction service')
L_COST = ('/cost-to-build-a-house-in-mexico/', 'Cost to build a house in Mexico')
L_REMOTE = ('/remote-construction-management-mexico/', 'Managing a build from abroad')
L_TURNKEY = ('/turnkey-construction-for-foreigners-riviera-maya/', 'Turnkey construction for foreign owners')
L_LAND = ('/buying-land-in-mexico/', 'Buying land: due diligence')
L_GC = ('/general-contractor-riviera-maya/', 'General contractor in the Riviera Maya')
L_FID = ('/fideicomiso-mexico-guide/', 'How a fideicomiso works')

PAGES = {

'how-long-to-build-a-house-in-mexico': dict(lang='en',
  title='How Long Does It Take to Build a House in Mexico?',
  desc='A realistic build timeline in the Riviera Maya: permits, foundation, structure, services and finishes, stage by stage, plus what actually causes delays here.',
  h1='How Long Does It Take to Build a House in Mexico?',
  lead='Seven to eleven months of construction for a normal house — and another two to six months before that, for the things people forget to count.',
  secs=[
   ('The honest answer, in two parts',
    'Construction of a 150 to 200 m² house on this coast runs seven to eleven months once you have a permit in hand. But the clock most owners care about starts earlier: land checks, design, engineering and the permit file add two to six months before a machine touches the site, and longer where a federal environmental file applies. From decision to keys, plan on twelve to twenty-four months including the land purchase. Anyone quoting you six months from scratch is either excluding permits or planning to build without one.'),
   ('Stage by stage',
    'The table below is how a normal residential project actually distributes. Stages overlap — services begin while structure finishes, finishes begin while services are tested — so the total is shorter than the sum. What does not overlap is the permit: nothing legitimate starts before it.'),
   ('What genuinely causes delays here',
    'The environmental file, in Tulum and near protected areas, which can move a start date by months. Foundations, when the soils study finds cavities or poor fill in the limestone — or when there was no soils study and the discovery happens mid-excavation. Rain, in the September–October peak, which mostly affects earthworks and pours. Imported finishes and fixtures with long lead times, which is the single most common self-inflicted delay. And change orders: every design change made after the structure is up costs more days than it looks like it should.'),
   ('What does not cause delays, despite the reputation',
    'Labour availability, on a properly staffed project. Materials, for anything sourced locally. And the municipality, when the file is complete — most permit "delays" here are files being returned for missing documents rather than authorities sitting on them. That distinction matters, because the first is something your builder controls and the second is not.'),
   ('How to protect the schedule',
    'Get the soils study before the design is finished. Order long-lead items — windows, kitchen, specialist fixtures — the moment the design is approved rather than when they are needed. Fix the specification before pouring the slab. Tie payments to milestones so the schedule has a financial consequence. And ask for the schedule as a document with dates and dependencies, not as a sentence in a proposal.'),
  ],
  table=('Stage', 'What happens', 'Typical duration',
   [('Land checks and design', 'Survey, soils, architecture, engineering', '6 – 12 weeks'),
    ('Permits and DRO', 'Municipal file; longer with environmental', '3 – 10 weeks'),
    ('Site work and foundation', 'Clearing, excavation in rock, footings', '4 – 8 weeks'),
    ('Structure and slabs', 'Columns, beams, roof slabs', '8 – 14 weeks'),
    ('Services and enclosure', 'Electrical, plumbing, AC, walls, waterproofing', '6 – 12 weeks'),
    ('Finishes and handover', 'Floors, joinery, fixtures, punch list', '10 – 16 weeks')]),
  faq=[('How long does it take to build a house in Mexico?',
        'Seven to eleven months of construction for a normal 150 to 200 m² house, plus two to six months beforehand for design and permits. From decision to keys, twelve to twenty-four months including buying the land.'),
       ('Can a house be built faster than that?',
        'Somewhat, with a simple design, locally sourced finishes and no changes after the slab is poured. What cannot be compressed is the permit and the curing of structural concrete, and compressing finishes is where quality quietly disappears.'),
       ('Does the rainy season stop construction?',
        'It slows earthworks and pours in the September and October peak but rarely stops a project. Structure and interior work continue. A schedule that ignores the season entirely was not built by someone who works here.'),
       ('What is the most common cause of delay?',
        'Long-lead imported items ordered late, and design changes made after the structure is up. Both are within the owner\'s control, which is why we push specification decisions as early as they can honestly be made.')],
  links=[L_COST, L_REMOTE, L_TURNKEY, ('/mecanica-de-suelos/', 'Soils studies in limestone')]),

'hurricane-proof-windows-and-doors': dict(lang='en',
  title='Hurricane Proof Windows and Doors in the Riviera Maya',
  desc='Impact glazing, shutters and storm panels for Caribbean homes: what actually protects a house, what the ratings mean and costs per m² in 2026.',
  h1='Hurricane Proof Windows and Doors',
  lead='In a hurricane the house is usually lost through an opening, not through a wall. Once a window fails, the pressure inside does the rest — which is why glazing is the part worth spending on.',
  secs=[
   ('Why openings decide the outcome',
    'Wind alone rarely destroys a well-built concrete house on this coast. What destroys it is a breached opening: once wind enters, internal pressure lifts the roof and pushes walls outward from the inside. Debris is what breaches the opening — not the wind speed itself, but a roof tile or a branch arriving at 200 km/h. Protecting openings is therefore the highest-return safety spend in a coastal house, and it is also the part most often value-engineered out of a budget.'),
   ('The three real options',
    'Laminated impact glazing: two glass panes bonded to an interpolymer layer, so the glass may crack but the opening stays sealed. It is permanent, needs nothing done before a storm, and is the only option that works when you are not in the country. Roll-down or accordion shutters: strong and reusable, but someone has to close them. Removable storm panels: the cheapest, and useless if nobody is there to install them. For an absentee owner, that last point decides the choice more than the price does.'),
   ('What the ratings actually mean',
    'Impact-rated systems are tested by firing a projectile at the assembly and then cycling it through thousands of pressure reversals. What passes is the whole assembly — glass, frame, anchors — not the glass alone, which is why installing impact glass in an ordinary frame with ordinary anchors buys much less than the invoice suggests. Ask for the test documentation of the complete system, and confirm the anchoring detail matches what is on the drawings.'),
   ('Costs in 2026',
    'Ranges per square metre of opening, installed, for the Riviera Maya. The frame series matters as much as the glass: a heavy structural series with impact glass behaves very differently from a light series with the same pane.'),
   ('Salt, and what fails first',
    'Near the sea the failure sequence is predictable: hardware first, then tracks, then the seals. Ordinary galvanised hardware on a beachfront window can seize within a few years, and a shutter that will not close is not protection. Specify stainless hardware, quality anodised or electrostatic finishes, and wash the frames and tracks with fresh water as routine maintenance. It is fifteen minutes a few times a year against replacing an entire system.'),
  ],
  table=('Protection', 'How it behaves', 'Cost per m² of opening, 2026',
   [('Standard tempered glazing', 'No debris protection', '$3,000 – $5,000 MXN'),
    ('Laminated impact glazing', 'Stays sealed when struck; nothing to close', '$8,000 – $15,000 MXN'),
    ('Roll-down shutters', 'Strong, reusable, must be closed', '$4,500 – $9,000 MXN'),
    ('Accordion shutters', 'Lower cost, manual operation', '$3,000 – $6,000 MXN'),
    ('Removable storm panels', 'Cheapest, needs someone on site', '$1,200 – $2,800 MXN')]),
  faq=[('Are hurricane proof windows worth it in the Riviera Maya?',
        'On the coast, and especially if the house sits empty part of the year, yes. Impact glazing is the only option that protects a house with nobody in it, and openings are how coastal houses are actually lost.'),
       ('How much do impact windows cost?',
        'Roughly $8,000 to $15,000 MXN per square metre of opening installed, against $3,000 to $5,000 for standard tempered glazing. Shutters sit in between and require someone to close them.'),
       ('Do shutters protect as well as impact glass?',
        'A good shutter system protects well — when it is closed. For an owner who is abroad during hurricane season, that condition is the whole problem, which is why we usually specify impact glazing on rental and second-home projects.'),
       ('Does taping windows do anything?',
        'No. Tape does not hold glass against impact or pressure and has never been shown to help. It is a habit, not a protection measure.'),
       ('What maintenance do they need near the sea?',
        'Fresh-water washing of frames and tracks, lubrication of moving hardware and an annual check of anchors and seals. Salt attacks hardware first, and a shutter that will not close is worth nothing.')],
  links=[('/ventanas-de-aluminio/', 'Aluminium windows: series and glass'),
         ('/blog/hurricane-proof-construction.html', 'Hurricane-proof construction'),
         L_CONC, L_GC]),

'condo-remodel-playa-del-carmen': dict(lang='en',
  title='Condo Remodel in Playa del Carmen: Cost and Rules',
  desc='Remodelling a condo in Playa del Carmen: what the HOA controls, real costs per m² in 2026, timelines, and how the work runs while you are abroad.',
  h1='Condo Remodel in Playa del Carmen',
  lead='A condo remodel is not a small house remodel. The building has rules, neighbours have patience limits, and half the job is logistics through a single elevator.',
  secs=[
   ('What the building decides before you do',
    'Most condominiums in Playa del Carmen require the administration to approve plans before work starts, restrict working hours and days, prohibit work in high season, control access for crews and materials, require a damage deposit, and limit how long the job may take. Some prohibit touching anything that affects the facade or common areas outright. All of this is knowable in a single conversation with the administrator, and it changes both the design and the price — so it happens first, not after demolition.'),
   ('What you can and cannot change',
    'Interiors, finishes, kitchens, bathrooms and non-structural partitions: usually yes. Plumbing risers, structural elements, facade openings, balcony enclosures and anything shared: usually no, or only with formal approval and an engineer\'s sign-off. Moving a bathroom in a building without accessible risers is the single most expensive idea in condo remodelling, and it is discovered late far too often.'),
   ('Costs in 2026',
    'Ranges per square metre of intervened area, for Playa del Carmen. Condo work carries a premium over house work for a simple reason: everything arrives and leaves through one elevator, on the building\'s schedule.'),
   ('Logistics: the part that decides the schedule',
    'Protection of common areas and elevator, debris removal in the permitted window, material deliveries booked with the administration, and crews on the building\'s hours rather than the trade\'s. On a good project this is planned before the first hammer; on a bad one it becomes a series of arguments with the administrator that stop work for days at a time.'),
   ('Doing it while you are not here',
    'Most of our condo clients are abroad, so the work runs the same way our builds do: fixed price against a line-item budget, weekly dated photo reports, payments tied to verified stages, and written approval for changes. We deal with the administration, the neighbours and the deposit. You approve finishes from a list rather than from a shop counter.'),
  ],
  table=('Scope', 'What it includes', 'Cost per m², 2026',
   [('Cosmetic refresh', 'Paint, floors, fixtures, minor joinery', '$4,000 – $8,000 MXN'),
    ('Kitchen and bathrooms', 'Cabinetry, tiling, plumbing fixtures', '$9,000 – $18,000 MXN'),
    ('Full interior remodel', 'Everything except structure and risers', '$12,000 – $22,000 MXN'),
    ('Rental-ready package', 'Remodel plus furnishing and equipping', 'Quoted per unit')]),
  faq=[('How much does it cost to remodel a condo in Playa del Carmen?',
        'From $4,000 to $8,000 MXN per m² for a cosmetic refresh, and $12,000 to $22,000 MXN per m² for a full interior remodel. Kitchens and bathrooms carry the highest cost per square metre.'),
       ('Do I need HOA approval?',
        'Almost always. Most buildings require approved plans, restrict working hours and days, control elevator and access, and hold a damage deposit. We confirm the rules before quoting, because they change the price and the schedule.'),
       ('Can I move the bathroom or kitchen?',
        'Only where the building\'s plumbing risers allow it, which frequently they do not. It is the first thing we check, because it is the difference between a straightforward remodel and an expensive one.'),
       ('How long does a condo remodel take?',
        'Four to ten weeks for a typical unit, depending on scope, on the building\'s permitted working hours and on whether work is prohibited during high season.'),
       ('Can you do it while I am out of the country?',
        'Yes, and most of our condo clients are. Fixed price, weekly dated photo reports, milestone payments, and we handle the administration and the neighbours.')],
  links=[('/condo-renovation-puerto-aventuras/', 'Condo renovation in Puerto Aventuras'),
         ('/condo-remodel-cancun/', 'Condo remodel in Cancun'), L_CONC, L_REMOTE]),

'condo-remodel-cancun': dict(lang='en',
  title='Condo Remodel in Cancun: Cost, HOA Rules, Timeline',
  desc='Remodelling a condo in Cancun: hotel-zone access rules, HOA approval, salt-air specification and costs per m² in 2026 for owners abroad.',
  h1='Condo Remodel in Cancun',
  lead='In Cancun the building rules and the location decide the job. A unit in the hotel zone and one in Puerto Cancun are two different projects with the same drawings.',
  secs=[
   ('Hotel zone, Puerto Cancun and the city',
    'In the hotel zone, access windows are narrow, noise rules are strict, and buildings frequently prohibit work during high season altogether — the schedule is built around the building, not the trade. In Puerto Cancun and the newer developments, design committees care about anything visible from outside and about protecting common areas. In the city, restrictions relax and the constraint becomes ordinary logistics. The same remodel can differ substantially in price between them, and the reason is access, not materials.'),
   ('Salt air changes the specification',
    'Oceanfront units eat hardware. Standard hinges, tracks, shower fittings and light fixtures corrode within a few years in a unit with the balcony doors open to the sea. The fix is unglamorous and effective: stainless hardware, quality anodised aluminium, marine-grade fixtures in exposed areas, and sealed electrical fittings on terraces. It costs more in the schedule of materials and much less than doing the job twice.'),
   ('Costs in 2026',
    'Ranges per square metre of intervened area in Cancun. The hotel zone sits at the upper end of each band, and the reason is almost entirely logistics and restricted working windows.'),
   ('What the building will and will not allow',
    'Interiors and finishes are normally fine. Plumbing risers, structure, facade openings and balcony enclosures normally are not, or need formal approval with engineering. Ask the administration for the rules in writing before design, including the deposit, the permitted hours and whether there is a high-season blackout. It is a short conversation that prevents the expensive kind of surprise.'),
   ('Rental-ready remodels',
    'If the unit is going into short-term rental, the remodel is designed differently: surfaces that survive rotation, hardware that tolerates heavy use, storage for linens and equipment, air conditioning sized for real occupancy, and a furnishing package that photographs well. We quote that as a defined scope so the numbers stay comparable rather than open-ended.'),
  ],
  table=('Scope', 'What it includes', 'Cost per m², 2026',
   [('Cosmetic refresh', 'Paint, floors, fixtures', '$4,500 – $8,500 MXN'),
    ('Kitchen and bathrooms', 'Cabinetry, tiling, fixtures', '$9,500 – $19,000 MXN'),
    ('Full interior remodel', 'Everything except structure and risers', '$13,000 – $24,000 MXN'),
    ('Oceanfront specification uplift', 'Stainless and marine-grade throughout', 'Adds 8% – 15%')]),
  faq=[('How much does a condo remodel cost in Cancun?',
        'From $4,500 to $8,500 MXN per m² for a refresh and $13,000 to $24,000 MXN per m² for a full interior remodel. Hotel-zone units sit at the top of each range because of restricted access and working hours.'),
       ('Can I remodel during high season?',
        'Many buildings prohibit it, particularly in the hotel zone. We confirm the building\'s calendar before scheduling, because a blackout period discovered mid-project is the worst kind of delay.'),
       ('What changes in an oceanfront unit?',
        'The hardware specification. Stainless fittings, quality anodised aluminium and marine-grade fixtures in exposed areas — otherwise corrosion starts within a few years and the job gets repeated.'),
       ('Do you handle the HOA paperwork?',
        'Yes: approval of plans, deposit, access and delivery scheduling, and compliance with working hours. It is part of the service, not an extra.')],
  links=[('/condo-remodel-playa-del-carmen/', 'Condo remodel in Playa del Carmen'),
         ('/apartment-condo-building-construction-riviera-maya/', 'Apartment and condo construction'),
         L_CONC, L_REMOTE]),

'furnishing-a-vacation-rental-mexico': dict(lang='en',
  title='Furnishing a Vacation Rental in Mexico: Cost and Kit',
  desc='What it costs to furnish a rental villa or condo in the Riviera Maya, what guests actually notice, and what breaks first in this climate.',
  h1='Furnishing a Vacation Rental in Mexico',
  lead='Furnishing decides your reviews far more than construction quality does. Guests never see the waterproofing; they absolutely notice the mattress, the water pressure and whether the air conditioning is quiet.',
  secs=[
   ('Budget by unit type',
    'A furnishing package covers furniture, mattresses and linens, kitchen equipment, appliances, televisions, outdoor furniture, decoration and the operational kit that guests never think about — spare linens, tools, cleaning equipment. The ranges below are what we see work in this market. Under-furnishing to save money is the most reliable way to lose a season of reviews, and reviews are the entire economics of a short-term rental.'),
   ('What guests actually notice',
    'Mattress quality. Water pressure and hot water that does not run out. Air conditioning that cools the bedrooms and is quiet enough to sleep through. Enough seating for the number of people the listing sleeps. Blackout curtains. A kitchen with real knives, enough plates and a decent coffee setup. Fast internet. Almost none of that is design — it is specification, and it is where owners who furnish remotely by catalogue tend to get it wrong.'),
   ('What fails first in this climate',
    'Cheap upholstery near the sea, which absorbs humidity and smells within a season. Particleboard furniture, which swells. Chrome hardware, which pits. Outdoor cushions without marine fabric. Standard electronics on unprotected circuits, during a storm season with real voltage events. The correct answers are solid or marine-grade materials, treated hardwoods or aluminium outdoors, stainless hardware, and surge protection — none of them exotic, all of them routinely skipped.'),
   ('Procurement timing',
    'This is the stage that most often delays a handover, because it is the one owners start last. Locally available furniture arrives in weeks; imported pieces, custom joinery and specific appliances take considerably longer, and customs is not always predictable. Start procurement when the finishes are chosen, not when the house is clean — otherwise the building is finished and the property sits empty waiting for sofas.'),
   ('Getting it rental-ready, not just furnished',
    'Beyond furniture: linens in the right multiples, a full equipment inventory, safety items, guest documentation, professional photography, listing setup and a maintenance plan. That last one matters more than owners expect — in this climate, a rental property without scheduled maintenance degrades visibly within a year, and the reviews follow.'),
  ],
  table=('Unit', 'Furnishing standard', 'Package cost, 2026',
   [('1-bedroom condo', 'Solid mid-range, rental-durable', '$180,000 – $350,000 MXN'),
    ('2-bedroom condo', 'Solid mid-range, rental-durable', '$280,000 – $550,000 MXN'),
    ('3-bedroom villa with pool', 'Upper-mid, outdoor furniture included', '$550,000 – $1,100,000 MXN'),
    ('Luxury villa', 'Designer, custom joinery', '$1,200,000 MXN and up')]),
  faq=[('How much does it cost to furnish a vacation rental in Mexico?',
        'Roughly $180,000 to $550,000 MXN for a one- or two-bedroom condo and $550,000 to $1,100,000 MXN for a three-bedroom villa with pool, including furniture, appliances, linens and the operational kit.'),
       ('How long does furnishing take?',
        'Weeks for locally available pieces; considerably longer for imported furniture, custom joinery and specific appliances. Procurement should start when finishes are selected, not when construction ends.'),
       ('What should I not economise on?',
        'Mattresses, air conditioning, water heating and outdoor furniture. Those four generate most of the complaints in reviews, and reviews are what the property earns from.'),
       ('Do you furnish as well as build?',
        'Yes, as a defined scope with a line-item budget: furniture, appliances, kitchen equipment, linens, decoration and the rental-readiness kit. It is part of the concierge service.')],
  links=[L_CONC, ('/blog/airbnb-roi-calculator-tulum-playa.html', 'Airbnb ROI in Tulum and Playa'),
         ('/tulum-investment-property-guide/', 'Is Tulum a good investment?'), L_TURNKEY]),

'tulum-investment-property-guide': dict(lang='en',
  title='Is Tulum a Good Investment in 2026? An Honest View',
  desc='Tulum property investment in 2026: what the airport changed, where supply has run ahead of demand, and the running costs projections leave out.',
  h1='Is Tulum a Good Investment? An Honest View for 2026',
  lead='We build in Tulum, so we have an obvious interest in you saying yes. Read the parts below where we tell you to be careful with that in mind — they are the ones worth your attention.',
  secs=[
   ('What actually changed',
    'The airport changed access, and access changes markets. More direct arrivals mean a longer season and a broader guest base than Tulum had when everything came through Cancun. That is real. What followed it was a construction wave, and a lot of it was condo product aimed at exactly the same short-term rental buyer, marketed with occupancy and rate projections that were written to sell units rather than to describe the market.'),
   ('Where supply has run ahead',
    'Small condo units in dense developments, sold on projected rental yield, are the most crowded segment. When many identical units compete for the same guest, the adjustment does not show up as falling prices first — it shows up as falling occupancy, discounting, and management fees eating what is left. If you are being sold a unit on a yield projection, ask what occupancy assumption it uses and compare that with what comparable listings actually achieve now.'),
   ('Where the market is thinner',
    'Larger private villas with real outdoor space, privacy and a pool are a different product with different competition. They are harder to build, harder to replicate at scale, and they serve guests who are not choosing between forty identical listings. That is the segment we build most in Tulum, which is a bias you should weigh — but it is also why the supply picture there looks different from the condo picture.'),
   ('The running costs nobody quotes',
    'Property tax is low. Everything else is not: electricity with air conditioning through a Caribbean summer, pool service, garden, insurance, HOA fees where they apply, management at a meaningful share of gross, cleaning between stays, and maintenance that this climate makes non-optional. A yield projection that omits these is not conservative — it is wrong. Model them before you commit, using the ranges below.'),
   ('Build or buy, specifically in Tulum',
    'Buying pre-sale is faster and puts you in the crowded segment, with the developer\'s specification and the developer\'s margin. Building takes twelve to twenty-four months, needs land that clears the environmental and land-use checks, and gives you a property that is not identical to forty others. Tulum\'s permit process is the strictest in the region, which is a genuine barrier — and barriers to entry are what protect the value of what is already built.'),
  ],
  table=('Annual cost', 'What drives it', 'Typical range',
   [('Electricity', 'Air conditioning, pool pump', '$35,000 – $120,000 MXN'),
    ('Pool and garden service', 'Weekly maintenance', '$30,000 – $90,000 MXN'),
    ('Property tax (predial)', 'Low by North American standards', 'Modest'),
    ('Rental management', 'Share of gross revenue', '15% – 30% of gross'),
    ('Maintenance reserve', 'Salt, humidity, rain', '1% – 2% of value/year')]),
  faq=[('Is Tulum still a good investment in 2026?',
        'It depends entirely on the segment. Small condo units sold on yield projections are competing with a lot of identical supply. Larger private villas face far less direct competition. Ask what occupancy any projection assumes and check it against comparable listings.'),
       ('Is it better to build or buy a pre-sale in Tulum?',
        'Buying is faster and puts you in the most crowded segment. Building takes twelve to twenty-four months and gives you a property that is not one of forty identical listings. Tulum\'s permit process is strict, which is a barrier — and also protection for what is already built.'),
       ('What returns are realistic?',
        'We will not publish a number, because any honest one depends on segment, location, management and the year. What we will say is that every projection should be re-run with real running costs and the occupancy comparable listings actually achieve, not the listing\'s assumption.'),
       ('What are the real running costs?',
        'Electricity with air conditioning, pool and garden service, insurance, HOA where applicable, management at 15% to 30% of gross, cleaning and a maintenance reserve of 1% to 2% of value per year in this climate.')],
  links=[('/construccion-de-casas-tulum/', 'Building houses in Tulum'),
         ('/furnishing-a-vacation-rental-mexico/', 'Furnishing a vacation rental'),
         ('/build-or-buy-playa-del-carmen/', 'Build or buy?'), L_LAND]),
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
        print('%-40s T%2d D%3d words %4d%s' % (slug + '/', len(d['title']), len(d['desc']), len(body), flag))
    ks = list(texts)
    mx = max((len(texts[a] & texts[b]) / len(texts[a] | texts[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity: %.2f (%s vs %s)' % mx)
