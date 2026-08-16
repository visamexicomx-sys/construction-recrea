#!/usr/bin/env python3
"""Second depth pass: every remaining thin page with 15+ impressions (2026-08-15).

Correction to the first pass: the word counter split on whitespace, which
undercounts Chinese by roughly four times — a page measured at 57 "words" holds
376 CJK characters, about 234 word-equivalents. The audit was re-run with a
language-aware count before this batch was chosen, and the Chinese pages moved
accordingly.

Selected: the 24 pages under ~620 word-equivalents that still earn 15 or more
impressions per quarter, after the first pass took the top 15. Together they
carry about 700 impressions.

Three kinds of page here, treated differently:

  Tools (/calculator, /calculadora, /price-map, /jisuanqi) — depth means
  explaining the method behind the number, which is also what makes the tool
  trustworthy rather than decorative.

  /team — this one is pure E-E-A-T. A construction company asking foreigners to
  wire six figures abroad should say who is responsible, not show three stock
  portraits.

  Everything else — page-specific substance, written for that page only.

Blocks carry data-depth so re-running replaces instead of duplicating, and each
is written in the language of the page it lands on.
"""
import os, re

OPEN, CLOSE = '<div data-depth="2026-08">', '</div><!--/depth-->'


def sec(h, p):
    return '<h2 class="mt-4">%s</h2>\n<p>%s</p>\n' % (h, p)


def table(head, rows):
    return ('<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr>'
            + ''.join('<th>%s</th>' % h for h in head) + '</tr></thead><tbody>\n'
            + '\n'.join('<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>' for r in rows)
            + '\n</tbody></table></div>\n')


BLOCKS = {

# ---------------------------------------------------------------- tools
'calculator/index.html':
 sec('How this estimate is built',
     'The figure comes from cost per built square metre at the finish level you choose, applied to the area you enter. '
     'That is the same basis we use to open a conversation with a client, and it is accurate enough to tell you whether '
     'a project fits your budget. It is not a quote. A quote requires a design, because the same 200 m² can differ by '
     '30% depending on geometry, spans, ground conditions and how much of the house is roofed outdoor space.')
 + sec('What the number includes and what it leaves out',
     'Included: construction of the house to the selected finish level — structure, envelope, services, finishes and '
     'basic external works. Not included, and each of them real: land; architectural and engineering project at roughly '
     '4% to 8% of construction; permits, DRO and the environmental file where it applies; the soils study; utility '
     'connections; furniture; landscaping; and the pool, which starts around $180,000 MXN for a plunge pool.')
 + sec('Why your real number may land above or below',
     'Above: cavities or poor fill found in the limestone, complex geometry, large spans, imported finishes, difficult '
     'access, island logistics. Below: simple rectangular geometry, single storey, good local finishes, and a '
     'specification fixed before the slab is poured. The single largest swing in either direction is the foundation, '
     'which is why we ask for a soils study before quoting anything firm.')
 + sec('What to do with the estimate',
     'Use it to decide whether to proceed, not to sign anything. When you are ready for a real number, we produce a '
     'line-item budget with quantities and unit prices against an actual design — the kind you can hand to another '
     'builder and compare line by line, which is the only comparison worth making.'),

'calculadora/index.html':
 sec('Cómo se construye esta estimación',
     'La cifra sale del costo por metro cuadrado construido según el nivel de acabado que elija, aplicado a la superficie '
     'que capture. Es la misma base con la que abrimos una conversación con un cliente y sirve para saber si el proyecto '
     'cabe en su presupuesto. No es una cotización. Una cotización necesita proyecto, porque los mismos 200 m² pueden '
     'variar 30% según geometría, claros, terreno y cuánta superficie es exterior techado.')
 + sec('Qué incluye y qué no',
     'Incluye: la obra de la casa al nivel elegido — estructura, envolvente, instalaciones, acabados y exteriores '
     'básicos. No incluye, y cada punto es real: terreno; proyecto arquitectónico y ejecutivo, del 4% al 8% de la obra; '
     'licencia, DRO y expediente ambiental cuando aplica; estudio de mecánica de suelos; conexiones de servicios; '
     'mobiliario; paisajismo; y la alberca, que arranca alrededor de $180,000 MXN en formato compacto.')
 + sec('Por qué su número real puede subir o bajar',
     'Sube con: cavidades o relleno en la caliza, geometría complicada, claros grandes, acabados importados, acceso '
     'difícil, logística de isla. Baja con: geometría simple, una sola planta, acabados nacionales de buena calidad y '
     'una especificación cerrada antes de colar la losa. Lo que más mueve el resultado en ambos sentidos es la '
     'cimentación, y por eso pedimos estudio de suelos antes de cotizar en firme.')
 + sec('Para qué usar esta estimación',
     'Para decidir si avanza, no para firmar. Cuando quiera un número real, entregamos presupuesto por partidas con '
     'cantidades y precios unitarios sobre un proyecto concreto: el tipo de documento que puede poner al lado del de '
     'otro constructor y comparar línea por línea, que es la única comparación que sirve.'),

'jisuanqi/index.html':
 sec('这个估算是怎么算出来的',
     '数字来自您所选装修级别的每建筑平方米造价，乘以您输入的面积。这与我们和客户开始沟通时使用的基准相同，'
     '足以判断项目是否符合您的预算。但它不是报价。报价需要设计图，因为同样的 200 平方米，'
     '会因几何形状、跨度、地基条件以及有顶室外空间的比例而相差 30%。')
 + sec('包含什么，不包含什么',
     '包含：所选级别的房屋施工——结构、围护、机电、装修和基础室外工程。不包含，且每一项都是真实支出：土地；'
     '建筑与施工图设计，约占工程造价的 4% 至 8%；许可证、DRO 以及适用时的环评文件；地质勘察；市政接入；'
     '家具；景观；以及泳池，紧凑型泳池约从 180,000 比索起。')
 + sec('您的实际数字为何可能更高或更低',
     '更高：石灰岩中的溶洞或回填土、复杂几何形状、大跨度、进口饰面、进场困难、岛屿物流。更低：简单的矩形体量、'
     '单层、优质国产饰面，以及在浇筑楼板前就锁定的材料规格。上下浮动最大的一项是基础，'
     '因此在给出正式报价前，我们会要求做地质勘察。')
 + sec('这个估算该怎么用',
     '用来判断是否推进，而不是用来签约。当您需要真实数字时，我们会基于具体设计出具分项预算，'
     '列明工程量与单价——这种文件可以拿去和另一家承包商逐条对比，而这是唯一有意义的比较方式。'),

'price-map/index.html':
 sec('Where these figures come from',
     'They are our own construction costs across the corridor, updated for 2026, expressed per built square metre and '
     'grouped by town and zone. They are not asking prices for land or property — those move for reasons that have '
     'nothing to do with what a house costs to build. Where a zone carries a premium here, it reflects real construction '
     'factors: access, logistics, development regulations, and ground conditions.')
 + sec('Why one zone costs more than its neighbour',
     'Island locations add roughly 15% for sea freight, lead times and crew accommodation. Gated developments add design '
     'review, restricted hours and access control. Areas near protected zones add environmental requirements that show up '
     'in drainage and wastewater rather than in finishes. And limestone with cavities or old fill adds foundation cost '
     'that has nothing to do with the postcode and everything to do with the specific lot.')
 + sec('How to use the map before you buy land',
     'Take the band for the zone, apply it to the area you want, then add the items that never appear in a per-square-'
     'metre figure: project fees at 4% to 8%, permits and DRO, the soils study, connections, furniture and the pool. '
     'That total, not the construction line, is what should be compared against the price of a finished property in the '
     'same zone.'),

'team/index.html':
 sec('Who is responsible for your project',
     'Every project has a named person accountable for it: a project lead who owns the schedule and the budget, a site '
     'supervisor who is physically present at the stages that get covered up, and a registered DRO who signs the file and '
     'answers to the municipality. You are told who they are before the contract is signed, not after something goes '
     'wrong. If you are wiring six figures to a country you do not live in, knowing which human being is accountable is '
     'not a nicety.')
 + sec('What we can show you',
     'Current DRO registration for the professional signing your project. Certificates of civil liability and workers\' '
     'cover, in date. Completed projects you can visit, and — more usefully — projects in progress, because a finished '
     'house tells you about photography and a live site tells you about the builder. References from owners who built '
     'remotely, which is the specific experience most of our clients are buying.')
 + sec('How we communicate during a project',
     'A single point of contact who answers in English or Spanish. Weekly written reports with dated photographs. Video '
     'calls at the stages that cannot be reviewed later. Written approval for every change order before it is executed. '
     'Nothing agreed verbally on site becomes an invoice. Across two languages and two time zones, the written record is '
     'the only version of events that survives, and it protects both sides.')
 + sec('196 projects, and what that number means',
     'It means we have made most of the mistakes available in this climate at somebody else\'s expense, and stopped '
     'making them. It also means we know which jobs to decline: sites outside our corridor, projects without a soils '
     'study, and owners who want a price that can only be met by leaving something important out.'),

# ---------------------------------------------------------------- service pages
'services/comercial.html':
 sec('En obra comercial manda la fecha de apertura',
     'Cada semana de retraso tiene un costo que el operador conoce al peso, así que el calendario es el presupuesto. '
     'Eso cambia la planeación: material de entrega larga pedido antes de demoler, oficios traslapados donde se puede '
     'hacer con seguridad, y la administración del centro comercial o el arrendador involucrados antes de que llegue la '
     'primera cuadrilla, no cuando la detienen en el andén de carga.')
 + sec('Qué construimos',
     'Locales y adecuaciones en plaza; oficinas y corporativos; restaurantes y cocinas con extracción, gas y trampas de '
     'grasa; consultorios y clínicas; bodegas ligeras; e imagen de marca dentro de centros comerciales. También '
     'remodelación integral de locales en operación, que es la mitad de lo que nos piden en Playa del Carmen y Cancún.')
 + sec('Oficinas: mandan las instalaciones, no los acabados',
     'Red y eléctrica dimensionadas para la densidad real de puestos, no para el plano; aire acondicionado calculado con '
     'carga de equipos y personas; iluminación pensada para pantallas; acústica entre salas y área abierta; y salidas que '
     'cumplan protección civil. Una oficina que se ve bien y suena mal se vuelve a remodelar en dos años.')
 + sec('Costos 2026', 'Rangos por m² terminado en la Riviera Maya. Las instalaciones especiales de cocina, clínica o '
       'laboratorio se cotizan aparte porque cambian el orden de magnitud.')
 + table(['Tipo', 'Alcance típico', 'Costo 2026 por m²'],
         [['Adecuación de local', 'Acabados, instalaciones, imagen', '$7,000 – $14,000 MXN'],
          ['Oficina corporativa', 'Divisiones, red, clima, acústica', '$10,000 – $20,000 MXN'],
          ['Restaurante o cocina', 'Instalaciones especiales, extracción', '$15,000 – $30,000 MXN'],
          ['Obra nueva comercial', 'Estructura, envolvente, instalaciones', '$14,000 – $26,000 MXN']]),

'services/servicios.html':
 sec('Cómo trabajamos, en una página',
     'Contrato a precio fijo por partidas, con cantidades y precios unitarios, para que el número que firma sea el '
     'número que paga salvo que cambie el alcance. Pagos ligados a avance verificable y no a fechas de calendario. '
     'Órdenes de cambio cotizadas y firmadas antes de ejecutarse. Reporte semanal con fotos fechadas, que es como '
     'trabajan la mayoría de nuestros clientes, porque no viven en México.')
 + sec('Qué cubrimos y hasta dónde llegamos',
     'Obra nueva residencial, villas y desarrollos pequeños; remodelación integral y por áreas; obra comercial y '
     'hotelera; y los oficios que normalmente el propietario termina persiguiendo por separado — eléctrica, plomería, '
     'aire acondicionado, carpintería, herrería, impermeabilización, albercas y acabados. Bajo un solo contrato hay un '
     'responsable; con cinco contratistas hay cinco versiones de por qué algo no avanzó.')
 + sec('Dónde trabajamos y dónde no',
     'El corredor de Cancún a Tulum, más Cozumel e Isla Mujeres. Fuera de ahí decimos que no. Una cuadrilla estirada a '
     'tres horas de la base no se supervisa igual, y en construcción la supervisión es la mitad del resultado. '
     'Preferimos rechazar una obra antes que entregarla mal.')
 + sec('Qué pedirnos antes de contratar',
     'Presupuesto por partidas, no un número global. El registro vigente del DRO que va a firmar. Certificados de '
     'responsabilidad civil y de cobertura de trabajadores. Una obra en proceso para visitar, que dice más que una '
     'terminada. Y el mecanismo de órdenes de cambio por escrito, que es donde se descontrolan los presupuestos.'),

'services/remodelacion.html':
 sec('Lo que casi toda remodelación destapa aquí',
     'Impermeabilización al final de su vida, instalación eléctrica sin tierra física, y humedad que se pintó encima en '
     'lugar de diagnosticarse. Una remodelación que solo toca superficies deja las tres cosas dentro y se ve impecable '
     'unos dieciocho meses. Nosotros levantamos primero y cotizamos las causas, lo que a veces hace que nuestro '
     'presupuesto parezca más caro que el de quien piensa pintar encima.')
 + sec('El orden correcto, y por qué importa',
     'Levantamiento y diagnóstico; demolición con protección de lo que se queda; correcciones estructurales y de '
     'impermeabilización; instalaciones renovadas con los muros abiertos; después acabados; después muebles y '
     'accesorios; y al final la lista de pendientes. Alterar ese orden para ver un resultado antes es la causa número '
     'uno de trabajo repetido.')
 + sec('Vivir en la casa, rentarla, o estar fuera',
     'Con la casa habitada: control de polvo, un baño y una cocina siempre funcionando, y horarios previsibles. Con '
     'propiedad en renta: obra comprimida en temporada baja y fecha de término dura. Con el propietario fuera del país: '
     'reporte semanal con fotos fechadas y aprobación por escrito de cada cambio, que es como trabajan la mayoría de '
     'nuestros clientes de remodelación.')
 + sec('Precios 2026', 'Rangos por m² de área intervenida. Cocinas y baños llevan el costo más alto por metro por las '
       'instalaciones que hay detrás.')
 + table(['Alcance', 'Incluye', 'Costo 2026 por m²'],
         [['Refrescamiento', 'Pintura, pisos, accesorios', '$4,000 – $8,000 MXN'],
          ['Cocina y baños', 'Carpintería, azulejo, plomería', '$9,000 – $18,000 MXN'],
          ['Remodelación integral', 'Instalaciones renovadas, acabados', '$12,000 – $22,000 MXN'],
          ['Cambio estructural', 'Claros, trabes, ingeniería', 'Por proyecto']]),

'construction-company-cancun/index.html':
 sec('Cancun is not one market',
     'The hotel zone runs on narrow access windows, strict noise rules and buildings that often prohibit work in high '
     'season — the schedule is built around the building, not the trade. Puerto Cancun and the newer developments have '
     'design committees that care about anything visible from outside. Cumbres and the western growth areas are where '
     'most new residential building happens, with heavy traffic and access as the constraint. The same drawings produce '
     'three different projects.')
 + sec('The development rulebook usually outranks the municipality',
     'Greater setbacks, lower heights, mandatory materials and colours, working hours, a damage deposit and a maximum '
     'construction period. All enforceable against you regardless of what Benito Juárez permits, and all worth reading '
     'before design rather than after municipal approval, when changing them costs fees and weeks.')
 + sec('What we do here',
     'New houses and villas, full renovations, condo remodels, and commercial fit-outs. Fixed price against a line-item '
     'budget, weekly dated photo reports, and written change orders — the way most of our clients work, because they are '
     'in the United States or Canada while we build.')
 + sec('Costs', 'Ranges per built square metre in Cancun for 2026, excluding land, project fees and permits.')
 + table(['Level', 'What it means', 'Cost per m², 2026'],
         [['Budget', 'Basic finishes, no pool', '$12,000 – $16,000 MXN'],
          ['Mid-range', 'Good finishes, small pool', '$17,000 – $24,000 MXN'],
          ['Premium', 'Imported materials, large pool', '$25,000 – $35,000 MXN']]),

# ---------------------------------------------------------------- blog, EN
'blog/cost-of-living-playa-del-carmen-2026.html':
 sec('The line that surprises everyone: electricity',
     'CFE tariffs are tiered, and crossing into the high-consumption bracket changes the bill dramatically rather than '
     'gradually. A house running air conditioning through a Caribbean summer, plus a pool pump, can move from a modest '
     'bill to a genuinely large one in a single billing period. This is the single biggest variable in a household budget '
     'here, and it is also the one most improved by decisions made during construction: orientation, insulation, solar '
     'control glazing, correctly sized units and solar panels.')
 + sec('What a house costs to keep, not to buy',
     'Beyond electricity: water, gas, internet, property tax, home insurance, pool service, garden, and a maintenance '
     'reserve that this climate makes non-optional. If the property is rented, add management and cleaning. Owners who '
     'budget only for the mortgage or the purchase are the ones surprised in year one.')
 + sec('Monthly ranges', 'For a private house with pool in Playa del Carmen, 2026. Ranges are wide because occupancy '
       'and air conditioning use drive most of the variation.')
 + table(['Item', 'Monthly range', 'Note'],
         [['Electricity', '$2,500 – $10,000 MXN', 'Tariff tiers punish heavy AC use'],
          ['Water', '$200 – $800 MXN', 'Low by North American standards'],
          ['Gas', '$500 – $1,500 MXN', 'LP tank, depends on hot water'],
          ['Internet', '$500 – $1,200 MXN', 'Fibre where available'],
          ['Pool service', '$1,500 – $4,000 MXN', 'Weekly'],
          ['Garden', '$2,000 – $6,000 MXN', 'Growth rate surprises newcomers']]),

'blog/moving-to-playa-del-carmen-guide.html':
 sec('Rent before you buy, and rent in the season you dislike',
     'Spend a few months here before committing capital, and make sure some of them fall in the humid heat of late '
     'summer rather than the pleasant dry winter everyone visits in. Neighbourhoods that feel identical on a February '
     'afternoon behave very differently in September — for noise, for flooding, for mosquitoes and for whether the '
     'street is actually where you want to live year-round.')
 + sec('The practical list nobody hands you',
     'Residency status and what it allows you to do. A Mexican bank account, which usually requires residency. An RFC if '
     'you will earn rental income. Health cover, private or public, decided before you need it. A local mobile number, '
     'because everything here runs on WhatsApp. And a realistic view of driving: a car is close to necessary outside the '
     'walkable centre.')
 + sec('Housing costs and the choice to build',
     'Renting first tells you which zone suits you, and that answer is worth more than the months of rent. When you do '
     'buy, the decision between buying finished and building comes down to time: building takes twelve to twenty-four '
     'months including land and permits, and buying takes weeks. What building gives back is a house specified for this '
     'climate rather than one built to a brochure.')
 + sec('What people underestimate',
     'How hard the humidity is on possessions and on buildings. How much air conditioning costs to run. How long any '
     'administrative process takes, and how much smoother it goes with the right paperwork prepared in advance. And how '
     'much easier life becomes with functional Spanish, even when everyone in the tourist zone speaks English.'),

'blog/building-near-cenote-riviera-maya.html':
 sec('Why the setback is not the whole question',
     'Distance to the cenote is the first thing anyone asks about, and it is only the beginning. What the authority '
     'actually assesses is whether anything from your property can reach the water: stormwater runoff, wastewater, spills '
     'and construction sediment. A house at a generous distance with untreated discharge is a worse proposal than a '
     'closer one that treats and contains everything. Design the water before you design the house.')
 + sec('What is required in practice',
     'Treatment of wastewater on the property — biodigester or compact plant, never infiltration of untreated effluent. '
     'Stormwater captured and managed rather than allowed to run toward the feature. Spill containment where vehicles or '
     'equipment operate. Sediment control during construction, which is the phase that does most of the damage and gets '
     'the least attention. And documentation of all of it in the environmental file.')
 + sec('Living next to one, honestly',
     'A cenote on or beside your lot is a genuine asset and a genuine responsibility. It constrains where you can build, '
     'what you can discharge, how you can light the property at night, and what you can plant. Owners who treat those '
     'constraints as the price of the privilege do well. Owners who look for the minimum that passes tend to end up in '
     'the enforcement statistics.'),

'blog/construction-permits-tulum.html':
 sec('The environmental file sets the calendar, not the municipality',
     'In Tulum the permit that decides when work starts is the environmental one. Karst ground, cenote systems and '
     'protected areas mean the file must justify stormwater handling, wastewater treatment and spill containment in '
     'detail. A complete file moves; an incomplete one is returned and the clock restarts rather than pausing. Serious '
     'programming here starts with the paperwork, not with the construction sequence.')
 + sec('What gets examined most closely',
     'Distance to cenotes and water bodies. Depth relative to the water table. Whether treatment precedes any '
     'infiltration. How rainwater on the lot is managed. Vegetation affected. And where the lot sits relative to a '
     'protected area, which brings that area\'s management programme and its own rules on density, height and lighting.')
 + sec('Mistakes that cost months',
     'Buying the land without verifying land use and environmental status. Commissioning the design before the land-use '
     'certificate exists. Proposing infiltration of untreated wastewater, which is refused. Filing DRO documentation '
     'after the rest of the package. And assuming that what was approved next door will be approved for you.')
 + sec('Realistic timelines', 'What we plan around in Tulum. These assume a complete file — an incomplete one restarts '
       'the clock.')
 + table(['Stage', 'Typical time', 'Note'],
         [['Land use certificate', '1 – 3 weeks', 'Before any design work'],
          ['Environmental file', 'Months', 'Sets the whole calendar'],
          ['Construction licence with DRO', '3 – 10 weeks', 'After the rest of the package'],
          ['Start on site', 'Only with the licence', 'Starting without it is expensive']]),

'blog/boutique-hotel-construction-tulum.html':
 sec('The permit stack is the project plan',
     'A boutique hotel in Tulum is a commercial project under environmental review, which means the federal file, not '
     'the municipal licence, determines when you break ground. Plan on months for that stage, and treat any schedule '
     'that does not name it as a schedule written by someone who has not built here. The building itself is the '
     'straightforward part.')
 + sec('What makes hotel construction different from a large house',
     'Wastewater at hotel volume needs a compact treatment plant, not a domestic biodigester. Electrical load requires '
     'its own transformer and CFE infrastructure. Water storage and pumping are sized for peak occupancy, not for a '
     'family. Fire safety, exits and civil protection sign-off apply. Back of house — laundry, storage, staff areas — '
     'is invisible to guests and to inexperienced budgets, and it is what makes the operation work.')
 + sec('Designing for the guest and the operator at once',
     'Guests notice water pressure, quiet air conditioning, blackout, and outdoor space that works in rain. Operators '
     'notice service routes that do not cross guest paths, surfaces that survive rotation, and equipment that can be '
     'maintained without closing a room. A design that pleases only the first of those two produces beautiful '
     'photography and an expensive operation.')
 + sec('Cost ranges 2026', 'Per m² of built area in Tulum, civil works and finishes, excluding FF&E and specialist '
       'kitchen equipment.')
 + table(['Segment', 'What it implies', 'Cost 2026 per m²'],
         [['Boutique, simple', 'Modest finishes, small key count', '$22,000 – $32,000 MXN'],
          ['Boutique, design-led', 'Bespoke joinery, feature materials', '$32,000 – $48,000 MXN'],
          ['High-end', 'Imported specification throughout', '$48,000 MXN and up']]),

'blog/bathroom-renovation-cost-playa-del-carmen.html':
 sec('Where a bathroom budget actually goes',
     'Not on the tiles. On what is behind them: waterproofing, falls to the drain, plumbing that may be forty years old, '
     'ventilation, and the electrical work around a wet area. A renovation that replaces surfaces over failing '
     'waterproofing looks excellent and leaks into the room below within two years — which on this coast, with this '
     'humidity, is the most common bathroom failure we are called to fix.')
 + sec('The things worth spending on here',
     'Waterproofing done properly, with upstands and laps rather than a coat of paint. Falls that actually drain, checked '
     'with water before tiling. Ventilation, mechanical if there is no window, because humidity here does not leave on '
     'its own. Stainless or quality-coated fittings, because ordinary chrome pits within a few years. And a shower valve '
     'you can service without breaking the wall.')
 + sec('Costs 2026', 'Ranges for a full bathroom renovation in Playa del Carmen, including demolition, waterproofing, '
       'services, tiling and fittings.')
 + table(['Scope', 'Includes', 'Cost 2026'],
         [['Cosmetic refresh', 'Fittings, paint, minor tiling', '$25,000 – $60,000 MXN'],
          ['Full renovation, standard', 'Demolition to finished, mid-range', '$80,000 – $160,000 MXN'],
          ['Full renovation, high spec', 'Bespoke joinery, feature stone', '$160,000 – $350,000 MXN'],
          ['Plumbing rerouting', 'Where risers or falls allow', 'Quoted separately']]),

# ---------------------------------------------------------------- blog, ES
'blog-es/construir-hotel-boutique-tulum.html':
 sec('El expediente es el plan de obra',
     'Un hotel boutique en Tulum es un proyecto comercial bajo revisión ambiental, así que lo que define cuándo se '
     'arranca no es la licencia municipal sino el expediente federal. Cuente meses para esa etapa, y desconfíe de '
     'cualquier calendario que no la mencione. El edificio, comparado con eso, es la parte sencilla.')
 + sec('En qué se diferencia de una casa grande',
     'Las aguas residuales a volumen hotelero piden planta compacta, no biodigestor doméstico. La carga eléctrica exige '
     'transformador propio e infraestructura CFE. El almacenamiento y bombeo de agua se dimensiona para ocupación pico. '
     'Aplican protección civil, salidas y seguridad contra incendio. Y el back of house — lavandería, almacén, áreas de '
     'personal — es invisible para el huésped y para los presupuestos sin experiencia, y es lo que hace operable el hotel.')
 + sec('Diseñar para el huésped y para el operador a la vez',
     'El huésped nota presión de agua, aire acondicionado silencioso, blackout y exteriores que funcionan con lluvia. '
     'El operador nota rutas de servicio que no cruzan las del huésped, superficies que aguantan rotación y equipo al que '
     'se le da mantenimiento sin cerrar una habitación. Un diseño que solo atiende lo primero produce fotos preciosas y '
     'una operación cara.')
 + sec('Rangos de costo 2026', 'Por m² construido en Tulum, obra civil y acabados, sin mobiliario ni equipo especializado '
       'de cocina.')
 + table(['Segmento', 'Qué implica', 'Costo 2026 por m²'],
         [['Boutique sencillo', 'Acabados moderados, pocas llaves', '$22,000 – $32,000 MXN'],
          ['Boutique de diseño', 'Carpintería a medida, materiales de autor', '$32,000 – $48,000 MXN'],
          ['Alta gama', 'Especificación importada', 'Desde $48,000 MXN']]),

'blog-es/costo-de-vida-playa-del-carmen-2026.html':
 sec('La partida que sorprende a todos: la luz',
     'Las tarifas de CFE son escalonadas, y cruzar al rango de alto consumo cambia el recibo de forma brusca, no gradual. '
     'Una casa con aire acondicionado durante el verano caribeño, más bomba de alberca, puede pasar de un recibo modesto '
     'a uno realmente alto en un solo periodo. Es la variable más grande del presupuesto doméstico aquí, y la que más se '
     'corrige con decisiones tomadas en obra: orientación, aislamiento, cristal de control solar, equipos bien '
     'dimensionados y paneles solares.')
 + sec('Lo que cuesta mantener una casa, no comprarla',
     'Además de la luz: agua, gas, internet, predial, seguro, mantenimiento de alberca, jardín y una reserva de '
     'mantenimiento que en este clima no es opcional. Si la propiedad se renta, sume administración y limpieza. Quien '
     'presupuesta solo la compra es quien se sorprende el primer año.')
 + sec('Rangos mensuales', 'Para una casa con alberca en Playa del Carmen, 2026. Los rangos son amplios porque la '
       'ocupación y el uso de aire acondicionado explican casi toda la variación.')
 + table(['Concepto', 'Rango mensual', 'Nota'],
         [['Electricidad', '$2,500 – $10,000 MXN', 'Las tarifas castigan el uso intensivo de A/A'],
          ['Agua', '$200 – $800 MXN', 'Baja para estándares del norte'],
          ['Gas', '$500 – $1,500 MXN', 'Tanque estacionario de LP'],
          ['Internet', '$500 – $1,200 MXN', 'Fibra donde hay cobertura'],
          ['Alberca', '$1,500 – $4,000 MXN', 'Servicio semanal'],
          ['Jardín', '$2,000 – $6,000 MXN', 'Crece más rápido de lo que espera']]),

'blog-es/construir-cerca-cenote-riviera-maya.html':
 sec('La distancia no es toda la pregunta',
     'Lo primero que todos preguntan es a qué distancia del cenote se puede construir, y eso es apenas el principio. Lo '
     'que evalúa la autoridad es si algo de su predio puede llegar al agua: escurrimiento pluvial, aguas residuales, '
     'derrames y sedimento de obra. Una casa lejos con descarga sin tratar es peor propuesta que una más cerca que trata '
     'y contiene todo. El agua se diseña antes que la casa.')
 + sec('Qué se exige en la práctica',
     'Tratamiento de aguas residuales en el predio — biodigestor o planta compacta, nunca infiltración sin tratar. Agua '
     'pluvial captada y conducida, no dirigida hacia el cenote. Contención de derrames donde operen vehículos o equipo. '
     'Control de sedimento durante la obra, que es la etapa que más daño hace y la que menos atención recibe. Y todo eso '
     'documentado en el expediente ambiental.')
 + sec('Vivir junto a uno, con honestidad',
     'Un cenote en su terreno o al lado es un activo real y una responsabilidad real. Condiciona dónde puede construir, '
     'qué puede descargar, cómo puede iluminar de noche y qué puede plantar. A quien acepta esas restricciones como el '
     'precio del privilegio le va bien; quien busca el mínimo que pase suele terminar en las estadísticas de sanción.'),

'blog-es/elevadores-accesibilidad-casas.html':
 sec('Cuándo conviene decidirlo: antes de colar',
     'Un elevador residencial cabe casi en cualquier casa si se previó el cubo desde el proyecto; agregarlo después '
     'implica romper losas, reforzar y perder superficie útil en dos niveles. Aun sin instalar el equipo, dejar el cubo '
     'previsto y usarlo como closet o alacena cuesta poco y convierte una obra futura en una instalación de una semana. '
     'Es la decisión más barata que casi nadie toma.')
 + sec('Tipos y qué exige cada uno',
     'Hidráulico: sencillo, no requiere cuarto de máquinas amplio, buena opción residencial. Eléctrico de tracción: más '
     'suave y eficiente para más niveles. Plataforma elevadora: recorrido corto, ideal para salvar desniveles de acceso, '
     'mucho más económica. Salvaescaleras: la solución de menor obra en una casa ya terminada. Todos necesitan '
     'alimentación eléctrica dedicada y mantenimiento periódico, y ese contrato es parte del costo real.')
 + sec('Accesibilidad más allá del elevador',
     'Puertas de 90 cm libres, un baño en planta baja con espacio de giro y regadera sin escalón, pasillos sin cambios '
     'de nivel, acceso a la casa sin peldaño aislado, y una recámara en planta baja convertible. Casi nada de eso cuesta '
     'más si se dibuja desde el inicio, y todo cuesta mucho si se resuelve después. En una casa pensada para el retiro '
     'es la diferencia entre envejecer en ella o mudarse.')
 + sec('Costos 2026', 'Rangos instalados en la Riviera Maya, sin obra civil del cubo.')
 + table(['Solución', 'Aplicación', 'Costo 2026'],
         [['Plataforma elevadora', 'Desniveles de acceso, recorrido corto', '$180,000 – $450,000 MXN'],
          ['Elevador hidráulico, 2 niveles', 'Residencial estándar', '$450,000 – $900,000 MXN'],
          ['Elevador de tracción, 3+ niveles', 'Mayor recorrido y confort', '$800,000 – $1,600,000 MXN'],
          ['Salvaescaleras', 'Casa terminada, obra mínima', '$90,000 – $250,000 MXN']]),

'blog-es/cocinas-exteriores-palapas-riviera-maya.html':
 sec('Qué materiales sobreviven al aire salino',
     'Fallan: el acero inoxidable de baja calidad, que se pica en un par de temporadas cerca del mar; los cuerpos de '
     'aglomerado o MDF, que se hinchan el primer verano húmedo; las bisagras y correderas corrientes; y la madera blanda '
     'sin tratar. Duran: cuerpos de mampostería o concreto acabados en chukum, azulejo o piedra; inoxidable de buena '
     'calidad; maderas duras densas; aluminio con pintura electrostática; y cubiertas de piedra o concreto.')
 + sec('Distribución que sí funciona al aire libre',
     'La parrilla a favor del viento respecto de la zona de estar, no en contra. Superficie de trabajo a ambos lados de '
     'la parrilla, que es el arrepentimiento más común. El fregadero cerca de la parrilla y no en el extremo opuesto. '
     'Sombra sobre quien cocina, no solo sobre los invitados. Y almacenamiento que cierre bien, porque aquí todo lo que '
     'queda abierto junta humedad, insectos y polvo.')
 + sec('Instalaciones que hay que dejar antes',
     'Línea de gas con válvula de corte, agua y un desagüe que vaya a donde debe ir, circuitos eléctricos dedicados para '
     'refrigeración, contactos con protección de intemperie, e iluminación en su propio apagador. Todo eso es barato con '
     'la terraza abierta y caro cuando ya está terminada.')
 + sec('Costos 2026', 'Instalación completa en la Riviera Maya, con mampostería, acabados, instalaciones y equipo de '
       'gama media. El equipo importado puede costar más que toda la obra que lo rodea.')
 + table(['Configuración', 'Qué incluye', 'Costo 2026'],
         [['Estación de parrilla', 'Base, cubierta, asador', '$65,000 – $140,000 MXN'],
          ['Cocina exterior estándar', 'Asador, tarja, guardado, instalaciones', '$150,000 – $350,000 MXN'],
          ['Cocina con barra', 'Suma refrigeración, barra, iluminación', '$350,000 – $700,000 MXN'],
          ['Bajo palapa o pérgola', 'Estructura sobre la zona de cocción', 'Suma $80,000 – $250,000 MXN']]),

'blog-es/pisos-acabados-clima-tropical.html':
 sec('Lo que este clima le hace a un piso',
     'Humedad alta todo el año, arena que actúa como abrasivo, sal en zona costera, y agua que entra desde la terraza '
     'con cada lluvia fuerte. Eso descarta materiales que en clima seco funcionan sin problema: maderas blandas sin '
     'tratar, laminados de baja calidad que se hinchan por los cantos, y cualquier acabado que dependa de un sellador '
     'que nadie va a renovar.')
 + sec('Qué funciona, por zona',
     'Porcelanato de baja absorción en casi toda la casa, y en terrazas con acabado antiderrapante. Chukum y concreto '
     'pulido cuando se busca continuidad, con juntas de control bien trazadas. Piedra local en exteriores, rugosa donde '
     'se pisa mojado. Maderas duras tropicales o composite en decks, siempre con rastreles ventilados. Y en baños, '
     'pendiente que realmente drene, verificada con agua antes de colocar el acabado.')
 + sec('El detalle que decide todo: la junta',
     'En pisos continuos, las juntas de control son lo que evita que la superficie elija dónde agrietarse. En '
     'porcelanato, la junta correcta absorbe el movimiento térmico de una terraza al sol. Y en el encuentro entre '
     'interior y exterior, el goterón y la pendiente son lo que impide que el agua entre con viento. Casi todas las '
     'quejas de piso en esta región son de junta o de pendiente, no de material.'),

'blog-es/aire-acondicionado-ventilacion-riviera-maya.html':
 sec('Dimensionar bien es lo que baja el recibo',
     'Un equipo sobredimensionado enfría rápido, se apaga, y deja el aire húmedo porque no alcanza a deshumidificar: '
     'la casa se siente fría y pegajosa, y el consumo sube por los arranques. Uno subdimensionado trabaja sin parar. El '
     'cálculo se hace con superficie, orientación, altura, cristal, aislamiento y ocupación real, no con una regla '
     'general por metro cuadrado. En esta región ese cálculo es la diferencia más grande en la factura anual.')
 + sec('Inverter, ductos y minisplit',
     'Los equipos inverter modulan en lugar de encender y apagar: consumen bastante menos y mantienen temperatura '
     'estable, y en un clima donde el aire trabaja casi todo el año se pagan solos. Minisplit por zona permite enfriar '
     'solo lo que se usa. El sistema por ductos da mejor resultado estético y uniforme, y exige diseño de retornos que '
     'con frecuencia se omite, dejando habitaciones que nunca enfrían.')
 + sec('Ventilación, humedad y el drenaje que inunda',
     'La ventilación cruzada bien resuelta reduce las horas de aire acondicionado. Los baños necesitan extracción real. '
     'Y el drenaje de condensados es el detalle que causa más daños en la región: si se tapa, el agua encuentra el '
     'plafón. Pendiente correcta, registro accesible y limpieza periódica son diez minutos de mantenimiento contra un '
     'techo manchado.')
 + sec('Costos 2026', 'Rangos instalados en la Riviera Maya, equipo y mano de obra.')
 + table(['Equipo', 'Aplicación', 'Costo 2026'],
         [['Minisplit inverter 1 tonelada', 'Recámara', '$14,000 – $28,000 MXN'],
          ['Minisplit inverter 2 toneladas', 'Sala o área abierta', '$22,000 – $45,000 MXN'],
          ['Sistema por ductos', 'Casa completa, por tonelada', '$35,000 – $70,000 MXN'],
          ['Mantenimiento', 'Por equipo, trimestral', '$800 – $2,000 MXN']]),

'blog-es/cuanto-cuesta-construir-casa-playa-del-carmen.html':
 sec('La diferencia entre el costo de obra y lo que realmente desembolsa',
     'El precio por metro cuadrado cubre la construcción de la casa. No cubre terreno, proyecto arquitectónico y '
     'ejecutivo (4% a 8% de la obra), licencia y DRO, estudio de mecánica de suelos, conexiones de servicios, mobiliario, '
     'paisajismo ni alberca. Entre el costo de obra y el desembolso total suele haber entre 25% y 40% de diferencia, y '
     'ahí es exactamente donde se rompen los presupuestos de quien construye por primera vez.')
 + sec('Cómo se reparte el costo',
     'Porcentajes aproximados para una casa de nivel medio. Sirven para detectar de un vistazo un presupuesto '
     'desequilibrado antes de leer el detalle.')
 + table(['Partida', '% del costo de obra', 'Nota'],
         [['Preliminares y cimentación', '12% – 18%', 'Sube con cavidades o relleno'],
          ['Estructura y albañilería', '25% – 32%', 'Concreto, acero, muros, losas'],
          ['Instalaciones', '14% – 18%', 'Incluye cisterna y bombeo'],
          ['Acabados', '22% – 30%', 'La partida que más varía por nivel'],
          ['Carpintería y herrería', '8% – 12%', 'Cocina, closets, cancelería'],
          ['Exteriores y limpieza', '4% – 8%', 'Andadores, jardín, entrega']])
 + sec('Dónde sí se puede ahorrar y dónde no',
     'Se puede: geometría simple, una sola planta, acabados nacionales de buena calidad, alberca más chica y bien '
     'equipada, y especificación cerrada antes de colar la losa. No se debe: estudio de suelos, cimentación, '
     'impermeabilización, instalaciones ocultas y tratamiento de aguas. Ahorrar ahí no evita el gasto, lo pospone y lo '
     'multiplica.'),

# ---------------------------------------------------------------- other languages
'blog-ru/palapa-stroitelstvo-gid.html':
 sec('Сколько на самом деле служит крыша из пальмы',
     'Хорошо уложенный уано служит обычно от 8 до 15 лет до замены, и разброс такой широкий из-за того, что вокруг. '
     'Постоянная тень и сырость, которая никогда не просыхает, сокращают срок заметно: палапа под деревьями выходит из '
     'строя раньше, чем такая же на открытом солнце. Вентиляция снизу срок продлевает, как и крутой скат с правильным '
     'нахлёстом. Каркас из твёрдой древесины переживает несколько циклов замены пальмы — поэтому перекрытие стоит '
     'вчетверо дешевле новой палапы.')
 + sec('Огнезащита, страховка и разрешения',
     'Пальму обрабатывают антипиреном, и для арендной или коммерческой недвижимости это обычно обязательно: страховые '
     'компании требуют, некоторые муниципалитеты тоже. Нанесённая на стройке обработка стоит существенно дешевле, чем '
     'потом. Уточните допустимую высоту и расположение в муниципалитете или во внутреннем регламенте посёлка, и '
     'предупредите страховщика до постройки, а не после страхового случая.')
 + sec('Обслуживание, которое действительно нужно',
     'Ежегодная проверка вязки и опорных узлов, очистка ендов от скопившихся листьев, обрезка веток, дающих постоянную '
     'тень на кровлю, и точечный ремонт повреждённых участков до того, как вода дойдёт до каркаса. Ухоженная палапа '
     'доживает до верхней границы срока, заброшенная — до нижней.')
 + sec('Стоимость в 2026 году', 'Диапазоны за м² покрытой площади на Ривьере-Майя, каркас из твёрдой древесины и '
       'кровля из уано.')
 + table(['Позиция', 'Детали', 'Стоимость 2026 за м²'],
         [['Новая палапа', 'Каркас из твёрдой древесины и уано', '$4,000 – $9,000 MXN'],
          ['Премиальный каркас', 'Чикосапоте, открытые соединения', '$7,000 – $12,000 MXN'],
          ['Перекрытие кровли', 'Каркас сохраняется', '$1,500 – $3,500 MXN'],
          ['Огнезащитная обработка', 'На этапе строительства', '+$250 – $600 MXN']]),

'blog-de/chukum-oberflaeche-leitfaden.html':
 sec('Warum Chukum in diesem Klima funktioniert',
     'Chukum ist ein Putz auf Basis des Harzes des gleichnamigen Baumes, seit Jahrhunderten auf der Halbinsel im '
     'Einsatz. Er ergibt eine fugenlose, warm getönte Oberfläche, die Wasser abweist und dennoch atmungsaktiv bleibt — '
     'genau die Kombination, die in einem Klima mit hoher Luftfeuchtigkeit und heftigem Regen zählt. Deshalb hält er '
     'sich dort, wo importierte Beschichtungen nach wenigen Jahren aufgeben.')
 + sec('Wo er sinnvoll ist und wo nicht',
     'Sehr gut: Innenwände, Bäder, Terrassen, Poolumrandungen und Fassaden. Im Pool selbst nur mit dem dafür '
     'vorgesehenen System und fachgerechter Ausführung. Nicht sinnvoll auf Untergründen, die arbeiten oder bereits '
     'gerissen sind, ohne diese vorher zu stabilisieren — der Riss kommt sonst an der Oberfläche zurück. Die '
     'Untergrundvorbereitung ist die halbe Arbeit und entscheidet über die Gewährleistung.')
 + sec('Pflege, ehrlich gesagt',
     'Chukum ist pflegeleicht, aber nicht wartungsfrei. Im Außenbereich und besonders in Küstennähe empfiehlt sich eine '
     'regelmäßige Auffrischung der Versiegelung, Reinigung mit pH-neutralen Mitteln und keine Säuren oder Scheuermittel. '
     'Farbliche Abweichungen zwischen Flächen gehören zum Material: Musterflächen vor Ausführung freigeben, nicht '
     'hinterher darüber diskutieren.')
 + sec('Preise 2026', 'Bandbreiten pro m² in der Riviera Maya, inklusive Untergrundvorbereitung und Versiegelung.')
 + table(['Anwendung', 'Vorbereitung', 'Preis 2026 pro m²'],
         [['Innenwände', 'Tragfähiger Putzgrund', '$650 – $1,100 MXN'],
          ['Bäder und Nassbereiche', 'Abdichtung, Systemaufbau', '$900 – $1,500 MXN'],
          ['Terrassen und Fassade', 'Außensystem, UV-Versiegelung', '$1,000 – $1,800 MXN'],
          ['Poolumrandung', 'Rutschhemmend ausgeführt', '$1,100 – $2,000 MXN']]),

'blog-de/hurrikan-saison-checkliste-mexiko.html':
 sec('Vor der Saison: was im Juni erledigt sein sollte',
     'Bäume zurückschneiden, die auf das Dach fallen könnten. Läden oder Schlagschutzverglasung prüfen und einmal '
     'komplett schließen, damit klar ist, dass sie funktionieren. Sämtliche Abläufe und Dachrinnen reinigen. Das '
     'Anwesen fotografieren und die Bilder außer Haus speichern — das ist Ihre Dokumentation gegenüber der Versicherung. '
     'Police auf Deckung für Sturmflut und auf die Höhe des Selbstbehalts prüfen, der bei Hurrikanschäden meist ein '
     'Prozentsatz der Versicherungssumme ist.')
 + sec('Wenn ein Sturm benannt ist',
     'Gartenmöbel, Sonnenschirme und alles Lose sichern oder einlagern. Poolwasserstand absenken, aber den Pool nicht '
     'leeren. Gas absperren. Öffnungen schützen. Wichtige Dokumente digital und wasserdicht sichern. Wer nicht im Land '
     'ist, braucht dafür jemanden vor Ort mit Schlüssel und Vollmacht — und diese Absprache muss vorher stehen, nicht '
     'wenn der Sturm bereits einen Namen hat.')
 + sec('Danach: die richtige Reihenfolge',
     'Zuerst dokumentieren, dann provisorisch reparieren. Notwendige Sofortmaßnahmen sind in der Regel erstattungsfähig, '
     'aber nur, wenn der Ausgangszustand festgehalten wurde. Dach und Abläufe vor dem nächsten Regen kontrollieren, '
     'nicht erst wenn Feuchtigkeit sichtbar wird. Und Schäden an Elektroinstallationen prüfen lassen, bevor wieder '
     'eingeschaltet wird.'),
}


def insert(path, block):
    s = open(path, encoding='utf-8').read()
    s = re.sub(re.escape(OPEN) + r'.*?' + re.escape(CLOSE), '', s, flags=re.S)
    payload = OPEN + '\n' + block + CLOSE + '\n'
    m = (re.search(r'\n[ \t]*<h2[^>]*>\s*(Preguntas Frecuentes|Frequently Asked Questions|Häufige Fragen|'
                   r'Часто задаваемые|常见问题|FAQ)', s)
         or re.search(r'\n[ \t]*<div class="cta-section', s)
         or re.search(r'\n[ \t]*<section data-cluster=', s))
    at = (s.rfind('\n', 0, m.start() + 1) + 1) if m else s.rfind('<footer')
    s = s[:at] + payload + s[at:]
    open(path, 'w', encoding='utf-8').write(s)
    return s


def wordcount(html):
    """Language-aware: CJK has no spaces, so whitespace splitting undercounts ~4x."""
    body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1'):html.index('<footer')])
    cjk = len(re.findall(r'[一-鿿]', body))
    latin = len(re.sub(r'[一-鿿]', '', body).split())
    return latin + int(cjk / 1.6)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for path, block in BLOCKS.items():
        if not os.path.exists(path):
            print('  missing:', path); continue
        before = wordcount(open(path, encoding='utf-8').read())
        after = wordcount(insert(path, block))
        print('%-52s %4d -> %4d' % (path, before, after))
