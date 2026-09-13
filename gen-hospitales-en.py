#!/usr/bin/env python3
"""English counterparts of the hospital and clinic construction cluster.

Written for a different reader than the Spanish pages. The Spanish set addresses
someone who will run the process locally; these address a foreign practitioner,
a medical-tourism operator or an investor who has to decide whether a project is
viable before committing — so the emphasis is on what the regulator will and will
not accept, what cannot be delegated, how long it really takes and what it costs
in both currencies.

Each page is hreflang-paired with its Spanish counterpart. Cross-language overlap
is printed at the end to confirm these are counterparts, not translations.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'gsc', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-gsc-pages.py'))
gsc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gsc)

FX = 18.0
BASE = [('Consulting clinic fit-out', 'Civil work, installations, washable seamless finishes', 14000, 24000),
        ('Dental practice', 'Suction, compressed air, treated water, sealed surfaces', 20000, 38000),
        ('Clinic with procedure rooms and CSSD', 'Dirty-to-clean flow, sterilisation, ventilation', 25000, 45000),
        ('Day surgery with operating theatre', 'Clean area, medical gas outlets, recovery', 40000, 75000),
        ('Radiological shielding, per room', 'Design, installation and documentation', 150000, 500000),
        ('Medical gas pipeline system', 'Distribution, alarms, testing and certification', 300000, 1200000),
        ('Generator with automatic transfer', 'Small facility', 200000, 500000)]


def m(v):
    return '$' + format(int(round(v, -3)), ',d')


def usd(v):
    v = v / FX
    return '$' + (format(int(round(v, -2)), ',d') if v >= 1000 else format(int(round(v, -1)), ',d'))


def rows_for(f):
    out = []
    for label, note, lo, hi in BASE:
        per = ' / m²' if hi <= 75000 else ''
        out.append((label, note, '%s – %s MXN%s (%s – %s USD%s)'
                    % (m(lo * f), m(hi * f), per, usd(lo * f), usd(hi * f), per)))
    return out


SCOPE = [
 ('What we build, and what a specialist signs',
  'We do the civil work and the full fit-out: layout, partitions, seamless washable finishes, hydro-sanitary and '
  'electrical installations, air conditioning with whatever filtration each area requires, lighting, fixed joinery, '
  'stainless steel fixtures and the biohazard waste store. What we do not sign is the medical gas pipeline or the '
  'radiological shielding: those are executed and certified by an accredited specialist, and the contract should say '
  'so. We build around them and we program their testing into the schedule.'),
 ('The real scope of the construction contract',
  'Our contract covers construction: masonry, installations, climate control and filtration, continuous-surface '
  'finishes with coved skirting, doors with clear widths for a stretcher, hands-free taps, the RPBI waste room and '
  'the service provisions for medical equipment. The medical gas system, the shielding of any imaging room and the '
  'regulatory filing itself sit with certified specialists. Their test dates go into the programme from the start, '
  'not at the end.'),
 ('How a healthcare project splits',
  'A medical unit is built on three fronts running in parallel: civil work and installations — ours; the specialist '
  'packages of medical gas and radiological shielding; and the regulatory file that the operating licence rests on. '
  'Confusing them is the usual cause of delay. The clean area does not close before the gas pipeline is tested, and '
  'equipment does not go in before the shielding is verified. What we guarantee is that the construction side is not '
  'the part holding up the calendar.')]

PERMITS = [
 ('The regulator writes the room schedule, not the architect',
  'In a medical unit the schedule of accommodation is set by health regulation according to the services you intend '
  'to provide. A consulting room, a dental practice, a procedure unit, imaging and day surgery are different '
  'categories, each with its own minimum areas, circulation widths, separation of flows and installation '
  'requirements. That is why the first deliverable is not a drawing: it is the list of services, converted into a '
  'compliant room schedule with a regulatory consultant. Starting from a floor plan is what forces it to be redrawn.'),
 ('Licence, sanitary responsible and radiological registration',
  'Depending on the activity, the unit needs either a notice of operation or a health licence, with a designated '
  'sanitary responsible, and imaging adds registration plus a radiological safety report. The premises are assessed '
  'against those requirements, so an attractive unit with narrow circulation or no dirty-to-clean separation simply '
  'is not authorised. Bring the regulatory consultant in at concept stage — not once there are walls.'),
 ('Three layers of approval that run together',
  'Health: notice or licence, sanitary responsible, RPBI waste handling and, where applicable, radiological safety. '
  'Municipal: land use compatible with healthcare, construction licence, Director Responsable de Obra and official '
  'number. Civil Protection: exits, widths, emergency lighting, signage, extinguishers and an evacuation plan that '
  'works for patients who cannot leave unaided. All three start in the first month; leaving Civil Protection to the '
  'end is the single most common reason an opening date slips.')]

TECH = [
 ('Finishes and installations that actually pass inspection',
  'Continuous-surface flooring — heat-welded sheet vinyl or resin — with coved skirting; walls coated to '
  'resist disinfectants; sealed ceilings in critical areas; no open shelving in procedure rooms. A hands-free basin '
  'in every clinical area, doors with clear width for a stretcher and a wheelchair, and air conditioning with the '
  'filtration and pressure regime each area requires. Ordinary commercial specification does not comply and, more '
  'to the point, does not work clinically.'),
 ('Critical services and redundancy',
  'Protected circuits in wet and procedure areas, UPS for equipment that cannot drop mid-procedure, and a generator '
  'with automatic transfer in any unit that sedates patients: on this coast a wet-season outage is routine, not an '
  'exception. Two water sources — mains plus your own cistern — treatment for the local hardness so '
  'autoclaves and dental equipment survive, and independent extraction in sterilisation.'),
 ('Flows, circulation and clinical waste',
  'The plan is organised by flow: patient, staff, clean supply and dirty return, without crossing where regulation '
  'forbids it. Sterilisation is designed with separate dirty and clean zones and one-way movement. The temporary '
  'store for biohazard waste must be isolated, ventilated, impermeable, signed, and on a route that does not cross '
  'patient areas — and you need a licensed collection contractor before you open. It is a small room that, '
  'when it is missing from the plan, forces half the floor to be rebuilt.')]

OPER = [
 ('Building while the unit stays open',
  'Most clinic extensions and refurbishments happen without closing. We work in isolated zones behind sealed '
  'hoarding with dust control, define a construction route that never crosses patient circulation, and schedule '
  'noisy work in windows agreed with the medical director. Water and power shutdowns are planned in writing weeks '
  'ahead, because in a medical unit an unannounced interruption has clinical consequences, not just commercial ones.'),
 ('Realistic timelines',
  'A consulting clinic takes 10 to 16 weeks of construction. A dental practice with several surgeries, 12 to 20. A '
  'unit with procedure rooms and sterilisation, 4 to 7 months. Day surgery with a theatre, 6 to 12. On top of that '
  'sits the regulatory path, which is frequently longer than the build and therefore starts first. The other '
  'bottleneck is equipment: imaging, autoclaves and dental chairs have long lead times into Quintana Roo, and the '
  'room is built for the specific model.'),
 ('Medical equipment and supplier coordination',
  'The building is constructed around specific machines, not categories: every model carries its own requirements '
  'for space, weight, power, water, drainage and ventilation. That is why we ask for the signed equipment list '
  'before closing installations. We coordinate the medical gas contractor, the shielding specialist, the stainless '
  'fabricator and the equipment supplier, and hand over verified provisions so installation does not mean opening '
  'finished walls.')]

FAQ_COMMON = [
 ('Can the clinic stay open during the works?',
  'Almost always, zone by zone, behind sealed hoarding with dust control and a construction route separate from '
  'patient circulation. Noisy work and service shutdowns are scheduled in writing with the medical director.'),
 ('Do you obtain the health licence?',
  'We coordinate it, we do not sign it. The filing and the sanitary responsible belong to a regulatory consultant; '
  'we build against that room schedule and hand over premises in a condition to be inspected.'),
 ('Do you install medical gas and radiological shielding?',
  'We coordinate them and leave the provisions, but execution and certification are done by an accredited '
  'specialist. That is correct both technically and legally, and it is what the contract says.'),
 ('Do you work at a fixed price?',
  'Yes: fixed price with an itemised budget, payments against verified progress and retention until the snag list '
  'closes. In healthcare the scope has to be settled before starting, precisely because regulation defines the areas.')]

CITIES = {
'playa-del-carmen': dict(
  name='Playa del Carmen', muni='Solidaridad', factor=1.0,
  ctx=('Playa del Carmen holds the largest private outpatient market in the state after Cancún, and the one '
       'most oriented to foreign patients: dental and aesthetic clinics serving medical tourism in the centre and '
       'along 30th Avenue, specialist consulting rooms clustered around the private hospitals, and urgent care for a '
       'resident population growing faster than its health infrastructure. Almost every project here is converting a '
       'commercial unit to medical use — which is a change of activity, not a refurbishment.'),
  local=('In Solidaridad the first thing to verify is that the land use of that specific unit admits healthcare. It '
         'is the filter that stops more projects than any other, and it is resolved before signing the lease, not '
         'after. Civil Protection requirements for premises with patients are also heavier than for a shop of the '
         'same size.'),
  faq=[('Can I convert a commercial unit into a clinic in Playa del Carmen?',
        'It depends on the unit\'s land use and whether the structure allows compliant circulation widths, exits and '
        'ventilation. We check that before you sign the lease — the point at which you can still change unit '
        'at no cost.'),
       ('What does fitting out a consulting clinic cost here?',
        '$14,000 to $24,000 MXN per m² ($780–$1,335 USD) for consulting use, and $20,000 to $38,000 for a '
        'dental practice, where suction, compressed air and treated water raise the installation cost.'),
       ('Do you build clinics aimed at medical tourism?',
        'Yes, and it is a significant part of the work here. Those units have to satisfy sanitary inspection and '
        'at the same time carry a finish level that an international patient recognises — the two requirements '
        'are not in conflict, but they do have to be designed together.')]),

'cancun': dict(
  name='Cancún', muni='Benito Juárez', factor=0.98,
  ctx=('Cancún has the largest hospital infrastructure in Quintana Roo and the largest projects: consulting '
       'towers, extensions to private hospitals, imaging units and clinics serving visitors. It is also the only '
       'market in the state with local specialist suppliers, which shortens lead times on medical gas, stainless '
       'fabrication and equipment servicing — a genuine advantage when a project has a fixed opening date.'),
  local=('In Benito Juárez the constraint is urban: manoeuvring hours on high-traffic avenues, the parking '
         'ratio the activity triggers, and in the Hotel Zone working windows and noise limits. For extensions to '
         'hospitals in operation, the construction plan is negotiated with the medical director before it is '
         'negotiated with the municipality.'),
  faq=[('Do you extend hospitals that are still operating?',
        'Yes. Zone by zone, with sealed isolation, dust control and independent access, and service shutdowns agreed '
        'in writing with the medical director.'),
       ('What does a day-surgery unit cost in Cancún?',
        '$40,000 to $75,000 MXN per m² ($2,225–$4,170 USD) for construction and installations, with the '
        'medical gas pipeline and the shielding of any imaging room quoted separately.'),
       ('Are specialist suppliers available locally?',
        'Yes, and it is the real advantage of building here: medical gas, custom stainless and equipment servicing '
        'are resolved in the city rather than shipped from Mérida or Mexico City.')]),

'tulum': dict(
  name='Tulum', muni='Tulum', factor=1.07,
  ctx=('Tulum grew far faster than its health infrastructure. The resident and floating population already justifies '
       'urgent care, basic imaging and specialist clinics that until recently meant driving to Playa del Carmen, and '
       'the airport has sharpened that demand. It is the market with the most room for new units and, at the same '
       'time, the longest approval path in the corridor.'),
  local=('Tulum adds an environmental layer to everything else: on a vegetated lot the environmental file sets the '
         'whole calendar. It also turns something that is a detail elsewhere into a requirement here — the '
         'grid is less reliable, so a generator with automatic transfer stops being optional in any unit that '
         'sedates patients or depends on refrigeration.'),
  faq=[('Why does a clinic in Tulum take longer to open?',
        'Two calendars run together: the sanitary one, which exists everywhere, and the municipal environmental file, '
        'which on a vegetated lot can take months. Both start before construction does.'),
       ('Is a backup generator really necessary?',
        'In any unit that sedates patients or relies on refrigeration, in practice yes. Wet-season outages here are '
        'routine, and the backup is designed in from the start rather than added afterwards.'),
       ('How is clinic drainage handled here?',
        'Treatment before infiltration, sized to real occupancy, with clinical waste handled entirely separately '
        'from the sanitary drain. On karst ground that is examined closely.')]),

'puerto-aventuras': dict(
  name='Puerto Aventuras', muni='Solidaridad', factor=1.03,
  ctx=('Puerto Aventuras needs a very specific kind of unit: urgent care and general practice for a gated residential '
       'community with a large foreign and retired population, plus service to the marina and the hotels along the '
       'stretch. These are not hospitals. They are small, well-equipped clinics that resolve the immediate problem '
       'and refer anything complex to Playa del Carmen.'),
  local=('The municipal route is the same as Playa del Carmen, but the work happens inside a gated community: '
         'controlled access, restricted working hours, worker registration and normally the internal committee\'s '
         'approval. The programme is built around those windows from day one.'),
  faq=[('What kind of unit makes sense in Puerto Aventuras?',
        'General practice and minor urgent care, able to stabilise and refer. The population does not support a '
        'surgical unit, but it does support a well-resolved clinic with laboratory and plain radiography.'),
       ('Does the gated community complicate construction?',
        'It conditions it: controlled access, restricted hours, worker registration and an internal rulebook. Not a '
        'problem when it is programmed from the start; very much one when discovered mid-project.'),
       ('Do you also build consulting rooms inside hotels?',
        'Yes. A hotel consulting room has its own circulation and independent-access requirements, and those are '
        'better resolved at concept stage than at inspection.')]),

'puerto-morelos': dict(
  name='Puerto Morelos', muni='Puerto Morelos', factor=1.02,
  ctx=('Puerto Morelos sits between two hospital poles: Cancún twenty minutes north and Playa del Carmen to '
       'the south. That defines the product — consulting, dentistry and minor urgent care for residents, for '
       'the hotels along the corridor and for the diving community, with fast referral to the two larger cities when '
       'something bigger is needed.'),
  local=('It is a young municipality, separated from Benito Juárez in 2016, with relatively recent planning '
         'instruments: confirm land use and requirements case by case rather than assuming Cancún practice. '
         'The upside is an accessible administration, where a complete file moves quickly and an incomplete one '
         'stalls.'),
  faq=[('Is a clinic here viable with Cancún so close?',
        'Yes, for consulting, dentistry and minor urgent care. What does not work is competing in high specialty: '
        'the model that succeeds resolves the everyday and refers the complex.'),
       ('Is the approval process the same as Cancún?',
        'No. Puerto Morelos has issued its own licences since 2016 and its planning instruments are recent. The land '
        'use of the specific property is confirmed before designing.'),
       ('Do you build hyperbaric medicine units?',
        'The civil work and installations, yes; the chamber and its certification come from the manufacturer. The '
        'structural, electrical and ventilation provisions are designed for the specific model.')]),

'akumal': dict(
  name='Akumal', muni='Tulum', factor=1.08,
  ctx=('Akumal has small but sharply defined demand: immediate care for a dispersed residential community, for the '
       'hotels around the bay and for diving, which here is a daily activity rather than an occasional one. The '
       'viable model is a compact urgent-care and consulting unit, equipped to stabilise and transfer rather than to '
       'treat at length.'),
  local=('It belongs to the municipality of Tulum and inherits its environmental demands, with the added sensitivity '
         'of the bay and the cenote systems: waste handling and drainage are examined more closely than inland. The '
         'local trade base is thin, so the crew travels in from Playa del Carmen as a unit.'),
  faq=[('What kind of unit suits Akumal?',
        'A compact urgent-care and consulting clinic able to stabilise and coordinate transfer. The population does '
        'not support more, and the distance to Playa del Carmen makes transfer part of the model rather than a '
        'failure of it.'),
       ('How is clinical waste handled in a small community?',
        'With an isolated, ventilated temporary store inside the unit and a licensed collection contractor on a '
        'scheduled route. It is the item most often neglected in small units and the first one inspected.'),
       ('Is there a location premium?',
        'Around 8% over the equivalent build in Playa del Carmen, for crew and material transport. It is identified '
        'as its own line rather than diluted into unit rates.')]),

'cozumel': dict(
  name='Cozumel', muni='Cozumel', factor=1.16,
  ctx=('Cozumel has medical demand that does not resemble the mainland: diving every day of the year, a cruise port '
       'landing thousands of passengers in a shift, and a resident population that cannot depend on a ferry crossing '
       'for an emergency. That sustains immediate-care units, hyperbaric medicine and specialist consulting that a '
       'mainland town of the same size would not carry.'),
  local=('It is an island, and that governs the build before anything else: all material arrives by ferry or barge '
         'on its own calendar, with freight that shows in the budget. The municipality runs its own approvals. '
         'Deliveries are staged and critical items over-ordered, because a shortage cannot be fixed the same day as '
         'it can on the mainland.'),
  faq=[('How much does island logistics add?',
        'Around 15% over the equivalent mainland build, for sea freight, lead times and crew accommodation. We show '
        'it as its own line item.'),
       ('Do you build hyperbaric chambers?',
        'The civil work, electrical installation and ventilation, designed for the specific equipment. The chamber '
        'itself and its certification come from the manufacturer.'),
       ('How do you secure material supply?',
        'With staged shipments and on-site storage, carrying margin on critical finishes and fixings. Stopping the '
        'job costs more than the extra material.')]),

'isla-mujeres': dict(
  name='Isla Mujeres', muni='Isla Mujeres', factor=1.15,
  ctx=('The municipality contains two different situations under one authority: the island, where a medical unit has '
       'to handle urgent care for a high floating population with logistics by boat, and Costa Mujeres on the '
       'mainland, where new hotels have created demand for consulting rooms and guest medical support. The two '
       'builds have almost nothing in common.'),
  local=('On the island the constraint is access: narrow streets, limited manoeuvring and material arriving by boat. '
         'In Costa Mujeres it is a corridor build with normal machinery access. The municipal process is the same in '
         'both cases, but the construction plan and the budget are different documents.'),
  faq=[('Do you work both on the island and in Costa Mujeres?',
        'Both. The island requires marine logistics and constrained manoeuvring; Costa Mujeres is built with normal '
        'access, at essentially Cancún cost.'),
       ('What unit works on the island?',
        'Immediate care and consulting, sized for a high floating population in season. What matters is the ability '
        'to stabilise and coordinate transfer, not the number of consulting rooms.'),
       ('How does material reach the island?',
        'By boat, in staged shipments with material accumulated in advance. The transport is an identified budget '
        'line rather than a hidden loading.')]),
}

PILLAR = dict(
  name='the Riviera Maya', muni='Quintana Roo', factor=1.0,
  ctx=('We build and fit out medical units across the corridor: Cancún, Puerto Morelos, Playa del Carmen, '
       'Puerto Aventuras, Akumal, Tulum, Cozumel and Isla Mujeres — from a single consulting room or dental '
       'practice to units with procedure rooms, imaging and day surgery. It is the most regulated commercial work we '
       'do, because here the premises are part of the licence: the room schedule is agreed with the regulatory '
       'consultant before the first drawing.'),
  local=('Each municipality adds its own layer: urban impact and parking in Benito Juárez and Solidaridad, '
         'the environmental file and grid backup in Tulum, a young administration in Puerto Morelos, marine '
         'logistics in Cozumel and Isla Mujeres. The health and Civil Protection layers are common to all; the real '
         'calendar is set by the municipality and, on the islands, by freight.'),
  faq=[('Which cities do you work in?',
        'Cancún, Puerto Morelos, Playa del Carmen, Puerto Aventuras, Akumal, Tulum, Cozumel and Isla Mujeres. '
        'Outside that corridor we assess case by case: we would rather decline than stretch a crew.'),
       ('What kinds of medical units do you build?',
        'Consulting rooms, dental practices, consulting and procedure units, imaging, laboratory and day surgery, '
        'plus extensions and refurbishments of units already in operation.'),
       ('Where does a clinic project start?',
        'With the list of services you intend to provide. The compliant room schedule follows from it, and only then '
        'does drawing make sense. Starting with the floor plan is what forces it to be redrawn.')])

PAIRS = {}


def make(slug_city, d, order):
    city = d['name']
    i = order
    v, vp, vc, vo = i % 3, (i + 1) % 3, (i + 2) % 3, (i // 3) % 3
    secs = [
        ('Medical units in %s' % city, d['ctx']),
        SCOPE[v],
        PERMITS[vp],
        ('Construction costs in %s, 2026' % city,
         'Ranges for civil work, installations and medical-grade finishes, excluding medical equipment. The items '
         'that move the total most are filtered air conditioning, continuous-surface finishes and the special '
         'installations. Shielding and medical gas are quoted separately because a certified specialist executes '
         'them.'),
        TECH[vc],
        ('Local requirements: %s' % d['muni'], d['local']),
        OPER[vo],
    ]
    links = [('/hospital-clinic-construction-riviera-maya/', 'Clinics across the Riviera Maya')] if slug_city else []
    links += [('/commercial-hotel-construction-riviera-maya/', 'Commercial and hotel construction'),
              ('/construction-permits-licenses-riviera-maya/', 'Permits and licences'),
              ('/site-supervision-mexico/', 'Site supervision')]
    if not slug_city:
        links = [('/hospital-clinic-construction-%s/' % s, 'Clinics in %s' % c['name'])
                 for s, c in list(CITIES.items())[:3]] + links[1:]
    t_long = 'Hospital and Clinic Construction in %s | Recrea' % city
    t_short = 'Clinic Construction in %s | Recrea' % city
    return dict(
        title=t_long if len(t_long) <= 65 else t_short,
        desc=('Building and fitting out clinics and medical units in %s: the compliant room schedule, finishes '
              'and installations that pass inspection, and 2026 costs.' % city.replace('the ', '')),
        h1='Hospital and Clinic Construction in %s' % city,
        lead=('Civil work, installations and medical-grade finishes for healthcare units in %s, built against the '
              'room schedule that health regulation requires — not the other way round.' % city),
        secs=secs,
        table=('Scope', 'What it covers', 'Cost 2026') + (rows_for(d['factor']),),
        faq=d['faq'] + FAQ_COMMON, links=links)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    texts = {}
    items = [('', PILLAR)] + list(CITIES.items())
    for i, (slug_city, d) in enumerate(items):
        key = slug_city or 'riviera-maya'
        slug = 'hospital-clinic-construction-' + key
        es = 'construccion-hospitales-clinicas-' + key
        PAIRS[slug] = es
        page = make(slug_city, d, i)
        os.makedirs(slug, exist_ok=True)
        html = gsc.build(slug, page, 'en')
        alt = ('  <link rel="alternate" hreflang="en" href="https://construction-recrea.com/%s/">\n'
               '  <link rel="alternate" hreflang="es" href="https://construction-recrea.com/%s/">\n'
               '  <link rel="alternate" hreflang="x-default" href="https://construction-recrea.com/%s/">\n'
               % (slug, es, slug))
        html = html.replace('</head>', alt + '</head>', 1)
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        esf = os.path.join(es, 'index.html')
        if os.path.exists(esf):
            s = open(esf, encoding='utf-8').read()
            s = re.sub(r'\s*<link rel="alternate" hreflang="(en|es|x-default)"[^>]*>', '', s)
            s = s.replace('</head>', alt + '</head>', 1)
            open(esf, 'w', encoding='utf-8').write(s)
        body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
        texts[slug] = set(tuple(body[j:j + 6]) for j in range(len(body) - 5))
        print('%-48s T%2d D%3d words %4d  hreflang<->/%s/' % (slug + '/', len(page['title']), len(page['desc']), len(body), es))
    ks = list(texts)
    mx = max((len(texts[a] & texts[b]) / len(texts[a] | texts[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max EN pairwise similarity: %.2f  (%s vs %s)' % mx)
    worst = 0
    for en_slug, es_slug in PAIRS.items():
        s = open(os.path.join(es_slug, 'index.html'), encoding='utf-8').read()
        b = re.sub(r'<[^>]+>', ' ', s[s.index('<h1'):s.index('<footer')]).lower().split()
        sb = set(tuple(b[j:j + 6]) for j in range(len(b) - 5))
        worst = max(worst, len(texts[en_slug] & sb) / len(texts[en_slug] | sb))
    print('worst EN/ES pair overlap: %.3f' % worst)
