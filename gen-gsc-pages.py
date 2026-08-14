#!/usr/bin/env python3
"""Pages built from measured Search Console demand, not from keyword-tool guesses.

Source: GSC export 2026-08-13, last 3 months. Every page below targets a cluster of
queries that already produce impressions for this site but has no page of its own,
so Google is currently answering them with whatever page it can find. Impressions
are per quarter.

  EN  hotel / resort permits in Quintana Roo ......... 152 impr, pos 10-18
      (hotel construction permit quintana roo 38, construction permit quintana roo
       hotel resort 23, hotel construction environmental permit cancun 16,
       construction permits riviera maya legal 19, licencia de construccion quintana
       roo foreigners 20, municipal land use certificate quintana roo 14,
       environmental permits cancun development 12, benito juarez municipality
       construction permit 11, environmental permits cancun 9)
  EN  cost to build a house in Mexico ................. 45 impr, pos 1.0-3.5
  EN  contractor / trades near me .................... 185 impr, pos 4.6-7.2
  ES  construcción comercial y de oficinas ............ 55 impr, pos 14.6-30.5
  DE  Baurecht in Mexiko ............................... 39 impr, pos 14.0

Note on the low positions in the permit cluster: we are on page two for queries
worth a hotel contract. That is the highest-value gap the export exposed.
"""
import os, re, json

BASE = 'https://construction-recrea.com'
DONOR = {'en': 'construction-company-playa-del-carmen/index.html',
         'es': 'cimentacion-y-losas-playa-del-carmen/index.html',
         'de': 'de/index.html'}

UI = {
 'en': dict(home='Home', faq='Frequently Asked Questions', guides='Related pages',
            cta_h='Planning a project on this coast?',
            cta_p='196+ completed projects. Fixed-price contracts. Reply in 2 minutes.',
            cta_b='Ask on WhatsApp', wa='Hello! I would like a free quote'),
 'es': dict(home='Inicio', faq='Preguntas Frecuentes', guides='Páginas relacionadas',
            cta_h='¿Quiere un presupuesto por partidas?',
            cta_p='196+ proyectos terminados. Contrato a precio fijo. Respuesta en 2 minutos.',
            cta_b='Cotizar por WhatsApp', wa='¡Hola! Quiero una cotización gratis'),
 'de': dict(home='Startseite', faq='Häufige Fragen', guides='Verwandte Seiten',
            cta_h='Planen Sie ein Bauprojekt an dieser Küste?',
            cta_p='196+ abgeschlossene Projekte. Festpreisvertrag. Antwort in 2 Minuten.',
            cta_b='Auf WhatsApp fragen', wa='Hallo! Ich möchte ein kostenloses Angebot'),
}
LOCALE = {'en': 'en_US', 'es': 'es_MX', 'de': 'de_DE'}


def chrome(lang):
    """head assets, body-top (top bar + nav) and footer, lifted from a real page."""
    s = open(DONOR[lang], encoding='utf-8').read()
    he = s.index('</head>')
    assets = '\n'.join(l for l in s[:he].split('\n')
                       if any(x in l for x in ('cdn.jsdelivr', 'fonts.g', 'style.min.css',
                                               'favicon', 'apple-touch', 'webmanifest')))
    body_start = s.index('<body')
    # everything up to the end of the fixed navbar, plus the spacer div when present
    nav_end = s.index('</nav>', body_start) + len('</nav>')
    tail = s[nav_end:nav_end + 200]
    m = re.match(r'\s*<div style="padding-top:\d+px"></div>', tail)
    top = s[body_start:nav_end + (m.end() if m else 0)]
    if not m:
        top += '\n<div style="padding-top:116px"></div>'
    footer = s[s.index('<footer'):]
    return assets, top, footer


def build(slug, d, lang):
    assets, top, footer = chrome(lang)
    ui = UI[lang]
    url = '%s/%s/' % (BASE, slug)
    art = {"@context": "https://schema.org", "@type": "Article", "headline": d['h1'],
           "description": d['desc'], "inLanguage": lang, "datePublished": "2026-08-13",
           "author": {"@type": "Organization", "name": "Recrea Construcción", "url": BASE},
           "publisher": {"@type": "Organization", "name": "Recrea Construcción"},
           "mainEntityOfPage": url}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in d['faq']]}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": ui['home'], "item": BASE + '/'},
        {"@type": "ListItem", "position": 2, "name": d['h1']}]}
    head = ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n  <meta charset="UTF-8">\n'
            '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '  <title>%s</title>\n  <meta name="description" content="%s">\n%s\n'
            '  <script type="application/ld+json">%s</script>\n'
            '  <script type="application/ld+json">%s</script>\n'
            '  <script type="application/ld+json">%s</script>\n'
            '  <link rel="canonical" href="%s">\n'
            '  <meta property="og:type" content="article">\n  <meta property="og:title" content="%s">\n'
            '  <meta property="og:description" content="%s">\n  <meta property="og:url" content="%s">\n'
            '  <meta property="og:image" content="%s/img/og-wallpaper.png">\n'
            '  <meta property="og:locale" content="%s">\n'
            '  <meta name="twitter:card" content="summary_large_image">\n</head>\n'
            % (lang, d['title'], d['desc'], assets, json.dumps(art, ensure_ascii=False),
               json.dumps(faq, ensure_ascii=False), json.dumps(bc, ensure_ascii=False),
               url, d['title'], d['desc'], url, BASE, LOCALE[lang]))

    th1, th2, th3, rows = d['table']
    table = ('<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark">'
             '<tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>\n%s\n</tbody></table></div>\n'
             % (th1, th2, th3, '\n'.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % r for r in rows)))
    secs = ''
    for i, (h, p) in enumerate(d['secs']):
        secs += '<h2 class="mt-4">%s</h2>\n<p>%s</p>\n' % (h, p)
        if i == d.get('table_after', 2):
            secs += table
    faq_html = '\n'.join(
        '<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button%s" '
        'type="button" data-bs-toggle="collapse" data-bs-target="#gf%d">%s</button></h3>'
        '<div id="gf%d" class="accordion-collapse collapse%s" data-bs-parent="#gscFaq">'
        '<div class="accordion-body">%s</div></div></div>'
        % ('' if i == 0 else ' collapsed', i, q, i, ' show' if i == 0 else '', a)
        for i, (q, a) in enumerate(d['faq']))
    links = ' · '.join('<a href="%s">%s</a>' % l for l in d['links'])

    article = ('<nav class="container mt-3"><ol class="breadcrumb"><li class="breadcrumb-item">'
               '<a href="/">%s</a></li><li class="breadcrumb-item active">%s</li></ol></nav>\n'
               '<section class="py-5"><div class="container"><div class="row justify-content-center">'
               '<div class="col-lg-8">\n<h1>%s</h1>\n<p class="lead">%s</p>\n%s\n'
               '<p>%s: %s</p>\n'
               '<h2 class="mt-5">%s</h2>\n<div class="accordion my-4" id="gscFaq">\n%s\n</div>\n'
               '<div class="cta-section rounded p-5 text-center my-5">\n'
               '<h3 class="text-white mb-3">%s</h3>\n<p class="text-white-50 mb-4">%s</p>\n'
               '<a href="https://wa.me/529844525333?text=%s" target="_blank" rel="noopener" '
               'class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>%s</a>\n</div>\n'
               '</div></div></div></section>\n'
               % (ui['home'], d['h1'], d['h1'], d['lead'], secs, ui['guides'], links, ui['faq'],
                  faq_html, ui['cta_h'], ui['cta_p'],
                  ui['wa'].replace(' ', '%20'), ui['cta_b']))
    return head + top + '\n' + article + footer


PAGES = {

# ---------------------------------------------------------------- EN, hotel permits
'hotel-resort-construction-permits-quintana-roo': dict(lang='en',
  title='Hotel & Resort Construction Permits in Quintana Roo (2026)',
  desc='Every permit a hotel or resort needs in Quintana Roo: environmental authorisation, ZOFEMAT, municipal licence and DRO, with realistic timelines and what stalls a file.',
  h1='Hotel and Resort Construction Permits in Quintana Roo',
  lead='The building is rarely what delays a resort on this coast. The environmental file is. Here is the full permit stack, in the order it actually has to be solved.',
  secs=[
   ('The three layers, and which one controls your calendar',
    'Federal: environmental authorisation through SEMARNAT, plus the change-of-land-use file when vegetation is affected, and CONAGUA for anything touching water or federal zone. State: environmental impact for projects below the federal threshold, plus civil protection. Municipal: land use, construction licence, road-impact opinion and DRO signature. The federal environmental layer is the one that sets the calendar for a hotel — months, not weeks — and it is the one that cannot be accelerated by paying more attention to the municipal file.'),
   ('The coastal specifics nobody warns foreign developers about',
    'If the project touches the beach, the federal maritime-terrestrial zone (ZOFEMAT) requires its own concession, and it is not part of your property title no matter what the seller said. If it sits near a reef or a protected area — Puerto Morelos, Akumal, Tulum, Cozumel — the environmental file is reviewed against the management programme of that protected area. If it sits over karst with cenotes, wastewater treatment and stormwater handling become the centre of the file rather than an annex.'),
   ('Realistic timelines',
    'These are the ranges we plan around for hotel and resort projects on this coast. They assume a complete file; an incomplete one restarts the clock rather than pausing it.'),
   ('What actually stalls a file',
    'Incomplete environmental technical studies. A land-use certificate that does not support the density or the height being requested. Wastewater solutions that propose infiltration in karst without treatment. Missing ZOFEMAT concession on beachfront. And DRO documentation that arrives after the rest of the file, which in several municipalities means the whole package waits. In our experience the difference between a nine-month and an eighteen-month permit process is almost entirely file quality, not luck.'),
   ('Buying land: verify before you sign, not after',
    'Confirm land use, density, COS, CUS and height against the municipal urban development programme. Confirm whether any part of the lot falls in a protected area, federal zone or right of way. Confirm access and services capacity. And commission a soils study: in fractured limestone, a cavity found after the structure is up is the most expensive discovery in this region. All of it costs a fraction of one month of a stalled project.'),
  ],
  table=('Permit', 'Authority', 'Typical timeline',
   [('Environmental authorisation (MIA)', 'SEMARNAT (federal)', '4 – 10 months'),
    ('Change of land use (forestry)', 'SEMARNAT (federal)', '3 – 8 months, when applicable'),
    ('Water / federal zone concession', 'CONAGUA', '2 – 6 months'),
    ('ZOFEMAT concession', 'Federal maritime zone', '3 – 9 months, beachfront only'),
    ('Land use certificate', 'Municipality', '1 – 4 weeks'),
    ('Construction licence + DRO', 'Municipality', '3 – 10 weeks')]),
  faq=[('How long do hotel construction permits take in Quintana Roo?',
        'Plan on roughly 9 to 18 months from first filing to construction licence for a resort project that needs federal environmental authorisation. Projects below the federal threshold, or on already-impacted land, can be considerably faster.'),
       ('Do I need a federal environmental permit for a hotel in Cancun?',
        'For most hotel and resort projects, yes — the scale and the sector place them under federal environmental review, and coastal or protected-area locations make it certain. Smaller projects on already-urbanised land may fall under state review instead.'),
       ('Can a foreigner obtain construction permits in Quintana Roo?',
        'Yes. Permits attach to the property and the project, not to your nationality. Within the restricted coastal zone, foreign buyers typically hold property through a bank trust (fideicomiso) or a Mexican company, and permits are filed by the owner or by the DRO on their behalf.'),
       ('What is a DRO and do I need one?',
        'The Director Responsable de Obra is the licensed professional registered with the municipality who signs the project and answers to the authority for code compliance. No licence is issued without one, and a signature from a DRO who never visits the site provides no real protection.'),
       ('What does ZOFEMAT mean for a beachfront hotel?',
        'The federal maritime-terrestrial zone is the strip measured from the high-tide line. It is federal property, it is never included in your title, and using it requires a concession with its own process and annual payment.')],
  links=[('/environmental-permits-cancun-development/', 'Environmental permits for development in Cancun'),
         ('/construction-permits-cancun/', 'Construction permits in Cancun'),
         ('/construccion-comercial-hoteles-riviera-maya/', 'Hotel and commercial construction'),
         ('/uso-de-suelo/', 'Land use, COS and CUS')]),

# ---------------------------------------------------------------- EN, environmental
'environmental-permits-cancun-development': dict(lang='en',
  title='Environmental Permits for Development in Cancun (2026)',
  desc='Environmental permits for development in Cancun and the Riviera Maya: MIA, land-use change, CONAGUA and protected areas, with real timelines and costs.',
  h1='Environmental Permits for Development in Cancun',
  lead='On this coast the environmental file is the project. Get it right and everything else is scheduling; get it wrong and no amount of construction expertise recovers the year you lose.',
  secs=[
   ('Which authority reviews your project',
    'SEMARNAT handles federal environmental impact — the MIA — for projects whose sector, scale or location places them under federal jurisdiction, which covers most tourism development, coastal work and anything affecting forest land. The state environmental authority reviews smaller projects. CONAGUA governs water: extraction, discharge and federal water zones. ASEA regulates anything involving hydrocarbons, which is why service stations follow a separate track. Protected areas add the management programme of that specific area on top.'),
   ('MIA: what it is and which modality applies',
    'The environmental impact statement describes the project, its setting, the impacts it will cause and the measures that will prevent, reduce or compensate them. There is a simplified modality for smaller or lower-impact projects and a regional modality for larger developments or those with cumulative effects. Choosing the wrong modality is not a shortcut — it is a rejected file and a restarted clock.'),
   ('Costs and timelines you can plan around',
    'Figures below cover the technical studies and filing for projects in this region. They exclude compensation measures, which vary enormously with what the site actually holds.'),
   ('Karst, cenotes and why wastewater dominates the file',
    'The Yucatan peninsula is fractured limestone. Water that infiltrates reaches the aquifer quickly, and the aquifer discharges into cenotes and onto the reef. That single fact governs the environmental review here: any proposal that infiltrates untreated wastewater is dead on arrival, and stormwater handling, spill containment and treatment capacity get more scrutiny than the architecture. Solve them at concept stage, not after the design is fixed.'),
   ('Protected areas along this coast',
    'Puerto Morelos reef, Tulum, Cozumel, Isla Contoy, Sian Ka\'an and the cenote corridors all carry their own management programmes with their own restrictions on density, height, vegetation removal and lighting. A lot inside or adjacent to one of them is not unbuildable, but it is a different project with a different timeline, and the price you paid for the land does not change that.'),
  ],
  table=('Item', 'Scope', 'Typical cost and time',
   [('MIA, simplified modality', 'Smaller or lower-impact projects', '$180,000 – $600,000 MXN · 3 – 6 months'),
    ('MIA, regional modality', 'Large or cumulative-impact developments', '$600,000 – $2,500,000 MXN · 6 – 12 months'),
    ('Land-use change study', 'When forest vegetation is removed', '$150,000 – $700,000 MXN · 3 – 8 months'),
    ('CONAGUA water permits', 'Extraction, discharge, federal zone', 'Per project · 2 – 6 months'),
    ('Environmental supervision during works', 'Compliance with imposed conditions', 'Monthly, for the duration of works')]),
  faq=[('Do I need a MIA for a house in Cancun?',
        'A single house on an already-urbanised lot inside the city usually does not require a federal MIA, though it still needs municipal permits and, near protected areas or water bodies, may need state environmental review. Developments, hotels and coastal work generally do.'),
       ('How much does an environmental permit cost in Cancun?',
        'The technical studies and filing for a simplified MIA typically run $180,000 to $600,000 MXN, and a regional MIA for a large development considerably more. Compensation measures imposed by the resolution are separate and can exceed the study cost.'),
       ('What happens if I build without environmental authorisation?',
        'PROFEPA can suspend the works, impose fines and require restoration. Beyond the penalty, an unauthorised structure is a defect that surfaces at the worst moment — when you refinance, sell or try to obtain an operating licence.'),
       ('Can the permit be obtained after starting construction?',
        'Regularisation exists but it is slower, more expensive and gives the authority leverage over a project you have already spent money on. Filing first is always cheaper than explaining later.')],
  links=[('/hotel-resort-construction-permits-quintana-roo/', 'Hotel and resort permits in Quintana Roo'),
         ('/construction-permits-cancun/', 'Construction permits in Cancun'),
         ('/pozo-de-absorcion/', 'Wastewater and absorption wells in karst'),
         ('/uso-de-suelo/', 'Land use, COS and CUS')]),

# ---------------------------------------------------------------- EN, cost to build
'cost-to-build-a-house-in-mexico': dict(lang='en',
  title='Cost to Build a House in Mexico 2026: Real Numbers',
  desc='What it costs to build a house in Mexico in 2026, per m² on the Caribbean coast: what the price includes, what it never includes, and where budgets break.',
  h1='Cost to Build a House in Mexico (2026)',
  lead='Numbers from a builder on the Caribbean coast, not a national average. This is what a house actually costs here, what the quoted price leaves out, and how the total is really composed.',
  secs=[
   ('Cost per m² by finish level',
    'Construction cost on the Riviera Maya is quoted per built square metre and moves mainly with the finish level, then with the ground and the access. These are 2026 ranges for turnkey construction, excluding land, furniture and the project fees listed further down.'),
   ('What the price per m² does not include',
    'Land. Architectural and engineering project, typically 4% to 8% of construction cost. Permits, DRO and the environmental file where it applies. Soils study. Connections to power and water. Furniture and appliances. Landscaping. And the pool, unless the quote says otherwise — a pool is a separate contract in most budgets, from roughly $180,000 MXN for a plunge pool upward.'),
   ('A realistic total for a 150 m² house',
    'Mid-range construction at the middle of the range gives roughly $3,300,000 MXN for the house itself. Add project and permits at around 8% to 12%, a soils study, connections, and a modest pool, and a realistic all-in figure lands well above the construction line item. The gap between those two numbers is where most first-time budgets fail.'),
   ('What is different about building on this coast',
    'Fractured limestone means foundations vary lot by lot and a soils study is not optional. Salt and humidity mean stainless fixings, treated or dense hardwoods outdoors, quality anodised aluminium and real protection on electrical work. Intense rain means drainage and waterproofing detailing decide whether the house is comfortable in year three. And in karst, wastewater is treated rather than infiltrated, which is a line item and a permit rather than a pipe.'),
   ('How to compare two quotes without being fooled',
    'Compare line by line, never by total. Confirm both include the same items with the same quantities. Check unit prices instead of totals. Confirm who pays permits, tests and final cleaning. Ask what happens if steel or cement prices move mid-project. The cheaper quote is almost always the one that left three line items out, and those line items reappear as change orders.'),
  ],
  table=('Finish level', 'What it means', 'Cost per m², 2026',
   [('Budget', 'Basic finishes, no pool', '$12,000 – $16,000 MXN'),
    ('Mid-range', 'Good finishes, small pool', '$17,000 – $24,000 MXN'),
    ('Premium', 'Imported materials, large pool', '$25,000 – $35,000 MXN'),
    ('Luxury', 'Architect-designed, bespoke throughout', '$35,000 MXN and up')]),
  faq=[('How much does it cost to build a house in Mexico?',
        'On the Riviera Maya in 2026, roughly $12,000 to $35,000 MXN per built square metre depending on finish level, excluding land, project fees and permits. A 150 m² mid-range house is therefore around $2.5M to $3.6M MXN of construction alone.'),
       ('Is it cheaper to build than to buy in Mexico?',
        'Building usually costs less per square metre than buying finished property in the same area, and you control the specification. What building costs you instead is time and involvement: land purchase, permits and construction realistically span 12 to 24 months.'),
       ('Can a foreigner build a house in Mexico?',
        'Yes. Within the restricted zone near the coast, foreign buyers typically hold the land through a bank trust (fideicomiso) or a Mexican company. Construction permits are issued on the property regardless of the owner\'s nationality.'),
       ('How long does it take to build a house here?',
        'Seven to eleven months of construction for a normal 150 to 200 m² house once permits are in hand. Permits themselves take weeks to months depending on the municipality and whether an environmental file is required.'),
       ('What is the biggest hidden cost?',
        'Foundations. In fractured limestone the ground varies between neighbouring lots, and a cavity or poorly compacted fill discovered after work starts is the single most expensive surprise in this region. A soils study before design is the cheapest insurance available.')],
  links=[('/general-contractor-riviera-maya/', 'General contractor on the Riviera Maya'),
         ('/blog/construction-costs-playa-del-carmen-2026.html', 'Construction costs in Playa del Carmen'),
         ('/mecanica-de-suelos/', 'Soils studies in limestone'),
         ('/presupuesto-de-obra/', 'How a proper line-item budget is built')]),

# ---------------------------------------------------------------- EN, contractor
'general-contractor-riviera-maya': dict(lang='en',
  title='General Contractor in Riviera Maya: English-Speaking Team',
  desc='English-speaking general contractor for the Riviera Maya: new builds, renovations and all trades in Playa del Carmen, Tulum, Cancun and Puerto Aventuras.',
  h1='General Contractor in the Riviera Maya',
  lead='One contractor, one contract, one person answering the phone in English. That is usually what people are looking for when they search for a contractor here — and what is hardest to find.',
  secs=[
   ('What we take on',
    'New houses and villas; full renovations and remodels; commercial fit-outs and hotel work; and the trades that most owners end up chasing separately — electrical, plumbing, air conditioning, carpentry, metalwork, waterproofing, pools and finishes. Taking them under one contract is the difference between a project with a single responsible party and a project where every trade blames the previous one.'),
   ('Where we work',
    'The corridor from Cancun to Tulum, plus Cozumel and Isla Mujeres: Puerto Morelos, Playa del Carmen, Puerto Aventuras, Akumal and the zones between them. Outside that corridor we decline. A crew stretched three hours from base is not supervised properly, and in construction supervision is half the outcome.'),
   ('Working with owners who live abroad',
    'Most of our clients are in the United States, Canada or Europe and follow the project by report. What makes that work: fixed-price contract with a line-item budget, payments tied to verifiable milestones rather than dates, weekly photo reports with dates, video calls at the critical moments — reinforcement before pouring, services before they are closed up — and written approval for every change. No verbal agreements on site.'),
   ('How we price',
    'Fixed price against a line-item budget, so the number you sign is the number you pay unless you change the scope. Change orders are priced and signed before they are executed, which is the mechanism that keeps a final invoice explainable line by line. We do not work on an open cost-plus basis, because it moves all the risk to the person least able to supervise it.'),
   ('Licensing, permits and who is responsible',
    'Permits are filed with a DRO registered with the municipality, who signs the project and answers to the authority. We handle the paperwork chain — land use, licence, environmental file where it applies, connections — and tell you honestly which parts depend on the authority\'s pace rather than ours.'),
  ],
  table=('Service', 'Typical scope', 'How it is contracted',
   [('New construction', 'House, villa, small development', 'Fixed price, line-item budget'),
    ('Renovation', 'Full remodel or single area', 'Fixed price after site survey'),
    ('Commercial and hotel', 'Fit-out, expansion, rebranding', 'By stages, operating premises'),
    ('Individual trades', 'Electrical, plumbing, AC, carpentry', 'Per job or as part of a build')]),
  faq=[('Do you speak English?',
        'Yes. Contract, budget, reports and day-to-day communication are all available in English, and that is how most of our clients work with us.'),
       ('Can you manage a project while I am out of the country?',
        'Yes, and most of our projects run that way: weekly dated photo reports, milestone-based payments, video calls before anything gets covered up, and written approval for every change order.'),
       ('Do you handle permits as well as construction?',
        'Yes, including the DRO and the paperwork chain. Where a federal environmental file applies, we tell you the realistic timeline for it up front rather than after you have committed.'),
       ('How do I know the quote is complete?',
        'Ask for it line by line, with quantities and unit prices. A one-number quote cannot be compared with anything, and it is the format that allows scope to quietly disappear.'),
       ('Which areas do you cover?',
        'Cancun, Puerto Morelos, Playa del Carmen, Puerto Aventuras, Akumal, Tulum, Cozumel and Isla Mujeres.')],
  links=[('/cost-to-build-a-house-in-mexico/', 'What it costs to build here'),
         ('/construction-company-playa-del-carmen/', 'Construction company in Playa del Carmen'),
         ('/hotel-resort-construction-permits-quintana-roo/', 'Hotel and resort permits'),
         ('/services/renovation.html', 'Renovation services')]),

# ---------------------------------------------------------------- ES, comercial
'construccion-comercial-oficinas': dict(lang='es',
  title='Construcción Comercial y de Oficinas en Riviera Maya',
  desc='Construcción comercial y de oficinas en Cancún, Playa del Carmen y Tulum: locales, corporativos y restaurantes. Costos 2026 y obra con el negocio abierto.',
  h1='Construcción Comercial y de Oficinas',
  lead='Obra comercial es otra disciplina: manda la fecha de apertura, y cada semana de retraso tiene un costo que el cliente conoce al peso.',
  secs=[
   ('Qué construimos',
    'Locales comerciales y plazas; oficinas y corporativos; restaurantes y cocinas, con sus instalaciones especiales de extracción, gas y trampas de grasa; consultorios y clínicas; naves ligeras y bodegas; y adecuaciones de marca dentro de centros comerciales. También remodelación integral de locales en operación, que es la mitad de lo que nos piden en Playa del Carmen y Cancún.'),
   ('Lo que hace distinta a la obra de oficinas',
    'El acabado importa menos que las instalaciones. Estructura de red y eléctrica dimensionada para densidad real de puestos, no para el plano bonito; aire acondicionado calculado con la carga térmica de equipos y personas; iluminación diseñada para pantallas; acústica entre salas de junta y área abierta; y accesos y salidas que cumplan protección civil. Una oficina que se ve bien y suena mal es una oficina que se remodela otra vez a los dos años.'),
   ('Costos 2026',
    'Rangos por m² de obra terminada en la Riviera Maya. La instalación especial —cocina, clínica, laboratorio— se cotiza aparte porque cambia el orden de magnitud.'),
   ('Obra con el negocio abierto',
    'Se planifica por etapas y por horarios: se aísla el área con barrera y señalización, los trabajos ruidosos van fuera de horario de atención, y en centros comerciales se respeta la ventana de maniobras y el reglamento del administrador. Un local puede remodelarse por mitades sin cerrar, siempre que el material esté en sitio antes de empezar. Lo que arruina estos calendarios no es la obra: es esperar material a mitad de etapa.'),
   ('Trámites y protección civil',
    'Uso de suelo compatible con el giro, licencia de construcción o de adecuación, visto bueno de protección civil, y en restaurantes además los requisitos sanitarios y de manejo de grasas. En centros comerciales se suma la aprobación del administrador, que suele exigir planos, seguros y horarios antes de dejar entrar a la primera cuadrilla.'),
  ],
  table=('Tipo de obra', 'Alcance típico', 'Costo 2026 por m²',
   [('Adecuación de local', 'Acabados, instalaciones, imagen', '$7,000 – $14,000 MXN'),
    ('Oficina corporativa', 'Divisiones, red, clima, acústica', '$10,000 – $20,000 MXN'),
    ('Restaurante o cocina', 'Instalaciones especiales, extracción', '$15,000 – $30,000 MXN'),
    ('Obra nueva comercial', 'Estructura, envolvente, instalaciones', '$14,000 – $26,000 MXN')]),
  faq=[('¿Cuánto cuesta construir un local comercial?',
        'De $14,000 a $26,000 MXN por m² en obra nueva, y de $7,000 a $14,000 MXN por m² en adecuación de un local existente. Las instalaciones especiales de cocina o clínica se cotizan por separado.'),
       ('¿Pueden trabajar sin cerrar el negocio?',
        'Sí, es lo habitual en remodelación comercial. Se divide en etapas, se aísla el área intervenida y los trabajos ruidosos se programan fuera del horario de atención.'),
       ('¿Cuánto tarda la adecuación de una oficina?',
        'Entre 6 y 14 semanas para una oficina de tamaño medio, según instalaciones y tiempos de entrega de mobiliario y cancelería. En centro comercial hay que sumar el trámite con la administración.'),
       ('¿Gestionan los permisos del local?',
        'Sí: uso de suelo según el giro, licencia de construcción o adecuación y protección civil, además de la aprobación del administrador cuando el local está dentro de una plaza.')],
  links=[('/construccion-comercial-hoteles-riviera-maya/', 'Construcción comercial y hotelera'),
         ('/construccion-remodelacion-gasolineras-riviera-maya/', 'Gasolineras'),
         ('/presupuesto-de-obra/', 'Presupuesto por partidas'),
         ('/permisos-licencias-construccion-riviera-maya/', 'Permisos y licencias')]),

# ---------------------------------------------------------------- DE, Baurecht
'de/baurecht-mexiko': dict(lang='de',
  title='Baurecht in Mexiko: Genehmigungen und Eigentum 2026',
  desc='Baurecht in Mexiko für deutsche Bauherren: Grundstückskauf über Fideicomiso, Baugenehmigungen, DRO, Umweltauflagen und Bauvertrag an der Riviera Maya.',
  h1='Baurecht in Mexiko: Was deutsche Bauherren wissen müssen',
  lead='Mexikanisches Baurecht ist nicht kompliziert, aber es funktioniert anders als das deutsche. Die teuren Fehler entstehen fast immer vor dem ersten Spatenstich.',
  secs=[
   ('Eigentum in der Küstenzone: Fideicomiso oder Gesellschaft',
    'Innerhalb von 50 Kilometern zur Küste können Ausländer Grundstücke nicht direkt auf den eigenen Namen erwerben. Üblich sind zwei Wege: der Fideicomiso, ein Bankstreuhandvertrag mit einer mexikanischen Bank, bei dem Sie sämtliche Nutzungs-, Vermietungs- und Verkaufsrechte behalten; oder eine mexikanische Gesellschaft, die vor allem bei mehreren Objekten oder gewerblicher Nutzung sinnvoll ist. Beides ist rechtssicher und seit Jahrzehnten etabliert — was zählt, ist die saubere Prüfung des Titels vor dem Kauf.'),
   ('Die Genehmigungskette',
    'Zuerst die Nutzungsbescheinigung: Sie legt fest, was auf dem Grundstück überhaupt gebaut werden darf — Nutzungsart, Dichte, Grundflächen- und Geschossflächenzahl, maximale Höhe. Danach die Baugenehmigung der Gemeinde, eingereicht mit einem vom DRO unterzeichneten Projekt. Je nach Lage kommen Umweltverfahren, Wasserbehörde und Zivilschutz hinzu. Wer das Projekt vor der Nutzungsbescheinigung zeichnen lässt, zahlt die Umplanung zweimal.'),
   ('Kosten und Fristen',
    'Richtwerte für ein Einfamilienhaus an der Riviera Maya. Die Umweltprüfung betrifft nicht jedes Vorhaben, bestimmt aber den Zeitplan, sobald sie greift.'),
   ('Der DRO: eine Rolle ohne deutsche Entsprechung',
    'Der Director Responsable de Obra ist der bei der Gemeinde registrierte Architekt oder Ingenieur, der das Projekt unterschreibt und gegenüber der Behörde für die Einhaltung der Bauvorschriften haftet. Ohne seine Unterschrift gibt es keine Genehmigung. Eine geliehene Unterschrift von jemandem, der die Baustelle nie betritt, ist billiger und schützt Sie im Ernstfall nicht — lassen Sie sich die gültige Registrierung zeigen.'),
   ('Der Bauvertrag: worauf es wirklich ankommt',
    'Festpreis mit Leistungsverzeichnis nach Positionen, mit Mengen und Einheitspreisen, statt einer Pauschalsumme. Zahlungen an überprüfbare Bautenstände gekoppelt, nicht an Kalenderdaten. Schriftliche Nachtragsregelung, bevor eine Änderung ausgeführt wird. Vertragsstrafe bei Verzug und Gewährleistung für verdeckte Mängel. Wer aus Deutschland baut, sollte zusätzlich wöchentliche Fotoberichte mit Datum und eine Freigabe per E-Mail für jede Änderung vereinbaren.'),
  ],
  table=('Schritt', 'Behörde oder Stelle', 'Richtwert Kosten und Dauer',
   [('Fideicomiso einrichten', 'Mexikanische Bank', 'Einrichtung plus Jahresgebühr · 4 – 10 Wochen'),
    ('Nutzungsbescheinigung', 'Gemeinde', '$1,500 – $6,000 MXN · 1 – 3 Wochen'),
    ('Baugenehmigung mit DRO', 'Gemeinde', 'Nach Fläche · 3 – 10 Wochen'),
    ('Umweltverfahren', 'Bundes- oder Landesbehörde', 'Nur bei bestimmten Vorhaben · Monate'),
    ('Anschlüsse Strom und Wasser', 'CFE, Wasserversorger', 'Nach Projekt · 2 – 8 Wochen')]),
  faq=[('Dürfen Deutsche in Mexiko ein Grundstück kaufen?',
        'Ja. In der Küstenzone innerhalb von 50 Kilometern zum Meer erfolgt der Erwerb über einen Fideicomiso bei einer mexikanischen Bank oder über eine mexikanische Gesellschaft. Sie behalten dabei alle Rechte an Nutzung, Vermietung und Verkauf.'),
       ('Wie lange dauert eine Baugenehmigung in Mexiko?',
        'Für ein Einfamilienhaus meist drei bis zehn Wochen ab vollständiger Einreichung, abhängig von der Gemeinde. Kommt ein Umweltverfahren hinzu, bestimmt dieses den Zeitplan und dauert Monate.'),
       ('Was kostet der Bau eines Hauses an der Riviera Maya?',
        'Je nach Ausstattung etwa $12,000 bis $35,000 MXN pro gebautem Quadratmeter, ohne Grundstück, Planung und Genehmigungen. Planung und Genehmigungen liegen zusammen üblicherweise bei acht bis zwölf Prozent der Bausumme.'),
       ('Brauche ich einen Anwalt?',
        'Für Titelprüfung und Fideicomiso ja — dieser Teil gehört in juristische Hände. Für Genehmigungen und Bauausführung übernimmt das der DRO gemeinsam mit dem Bauunternehmen.'),
       ('Kann ich aus Deutschland bauen lassen?',
        'Ja, so arbeiten viele unserer Kunden. Entscheidend sind Festpreis nach Positionen, Zahlungen nach überprüfbarem Bautenstand, wöchentliche Fotoberichte mit Datum und schriftliche Freigabe jeder Änderung.')],
  links=[('/de/', 'Bauunternehmen an der Riviera Maya'),
         ('/hausbau-playa-del-carmen/', 'Hausbau in Playa del Carmen'),
         ('/bauunternehmen-tulum/', 'Bauunternehmen in Tulum'),
         ('/bauunternehmen-cancun/', 'Bauunternehmen in Cancún')]),
}


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for slug, d in PAGES.items():
        os.makedirs(slug, exist_ok=True)
        html = build(slug, d, d['lang'])
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        words = len(re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).split())
        flag = '' if len(d['title']) <= 65 and len(d['desc']) <= 175 else '  <-- CHECK'
        print('%-48s %s  T%2d D%3d  words %4d%s'
              % (slug + '/', d['lang'], len(d['title']), len(d['desc']), words, flag))
