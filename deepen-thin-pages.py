#!/usr/bin/env python3
"""Add depth to the thin pages that already earn impressions (2026-08-15).

Selected by joining a word count of every indexable page against the Search
Console pages export, then sorting by impressions. 672 pages are under 600 words;
these are the ones where thinness is measurably costing something:

  /blog-es/costo-construir-casa-tulum.html    456 w  386 impr  pos 4.8
  /blog-es/permisos-construccion-cancun.html  513 w  385 impr  pos 4.9
  /services/electrical.html                   386 w  318 impr  pos 16.0
  /services/permisos.html                     497 w  298 impr  pos 7.8
  /services/metalwork.html                    410 w  242 impr  pos 15.5
  /blog-es/guia-construccion-palapas.html     477 w  228 impr  pos 6.3
  /services/residential.html                  587 w  165 impr  pos 11.2
  /blog/palapa-construction-guide...html      469 w  139 impr  pos  6.7
  /services/renovation.html                   410 w  134 impr  pos 18.0
  /blog-es/permisos-construccion-tulum.html   505 w   89 impr  pos  5.1
  /blog/construction-permits-cancun.html      447 w   73 impr  pos  6.6
  /services/carpinteria.html                  493 w   62 impr  pos 10.4
  /services/carpentry.html                    435 w   51 impr  pos 10.0
  /services/commercial.html                   411 w   46 impr  pos 14.6
  /services/herreria.html                     472 w   44 impr  pos  7.2

Two different opportunities in that list. Pages at position 4-7 with 200-400
impressions need depth to convert an existing top-ten placing into a top-three
one. Pages at position 15-18 with 240-320 impressions are being shown a lot and
ranked badly — that is the classic signature of a page Google finds relevant and
insufficient.

Content is appended before the FAQ or the closing CTA, whichever comes first, so
it reads as part of the article rather than as a bolt-on. Every block is written
for that specific page; none of it is filler, and no block is reused.
"""
import os, re

# marker so re-running replaces rather than duplicates
OPEN, CLOSE = '<div data-depth="2026-08">', '</div><!--/depth-->'


def sec(h, p):
    return '<h2 class="mt-4">%s</h2>\n<p>%s</p>\n' % (h, p)


def table(head, rows):
    return ('<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr>'
            + ''.join('<th>%s</th>' % h for h in head) + '</tr></thead><tbody>\n'
            + '\n'.join('<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>' for r in rows)
            + '\n</tbody></table></div>\n')


BLOCKS = {

'services/electrical.html':
 sec('How a house here is actually wired',
     'Separate circuits for lighting, general outlets, kitchen, and one dedicated circuit per air-conditioning unit, '
     'per pump and for the pool equipment. That is not gold-plating: it is what stops the breaker tripping in August '
     'with everything running. Conductor gauge follows the load and the run length, and long runs to a garden pump or '
     'a gate motor need sizing rather than guessing. Everything is tested before walls are closed, because after that '
     'a correction means breaking finishes.')
 + sec('Earthing, surge protection and the coast',
     'A proper earth electrode and bonding is what protects people and equipment, and it is the first line to disappear '
     'from a cheap quote. In a region with frequent electrical storms, surge protection at the panel is worth its modest '
     'cost for anything sensitive. Near the sea, panels, outdoor sockets and fittings need real ingress protection, '
     'because salt gets into anything that no longer seals and corrosion starts at the terminals.')
 + sec('What to leave prepared during construction',
     'Conduit and panel space for solar, even if the panels come later. A circuit for the pool pump and for water '
     'treatment. Supply for an automatic gate. An EV charging point. Network cabling to the places you will actually '
     'work, including the terrace. All of it costs a fraction while walls are open and is disruptive afterwards.')
 + sec('Prices and what drives them', 'Ranges for the Riviera Maya in 2026, with recognised-brand material and labour. '
       'The CFE connection and its paperwork are quoted separately because they depend on the load and the site.')
 + table(['Scope', 'Applies to', 'Cost 2026'],
         [['Complete installation, new build', 'Per m² built', '$450 – $900 MXN/m²'],
          ['Per outlet, switch or fitting', 'New work or remodel', '$600 – $1,200 MXN'],
          ['Main panel with protections', 'Single house', '$12,000 – $35,000 MXN'],
          ['Earthing system', 'Rod, conductor, inspection box', '$6,000 – $18,000 MXN'],
          ['Surge protection', 'Panel-mounted', '$4,000 – $14,000 MXN']]),

'services/metalwork.html':
 sec('What corrodes first, and why it is never the steel you see',
     'On this coast failure starts at the joints and fixings: an ordinary galvanised bolt in a stainless assembly, a weld '
     'that was never cleaned of flux, or a coating applied over mill scale. Salt finds those points, and rust travels '
     'outward from them while the visible surface still looks intact. That is why specification matters more than the '
     'metal itself, and why two railings that look identical behave very differently in year four.')
 + sec('Coatings that survive here',
     'Hot-dip galvanising then electrostatic powder coating is the durable combination for structural and exterior work. '
     'Marine-grade stainless is right for beachfront railings, pool-adjacent fittings and anything within reach of spray. '
     'Powder-coated aluminium suits lighter items where weight and corrosion both matter. Ordinary paint over untreated '
     'steel is a two-season solution sold at a one-season price.')
 + sec('What we fabricate',
     'Railings and balustrades, gates and automatic gate structures, security bars designed not to look like security '
     'bars, pergola and canopy structures, staircases and treads, window grilles, and structural steel for openings and '
     'mezzanines. Fabrication happens in the workshop, with fitting on site, so the noisy work does not happen in an '
     'occupied house.')
 + sec('Prices', 'Ranges for the Riviera Maya, fabricated and installed. Design complexity and finish drive the range '
       'far more than the weight of metal does.')
 + table(['Item', 'Specification', 'Cost 2026'],
         [['Railing, powder-coated steel', 'Galvanised then coated', '$1,800 – $3,500 MXN/m'],
          ['Railing, marine stainless', 'Beachfront exposure', '$4,500 – $9,000 MXN/m'],
          ['Sliding gate structure', 'Up to 4 m, without motor', '$25,000 – $60,000 MXN'],
          ['Window grilles', 'Per opening, designed', '$3,500 – $9,000 MXN'],
          ['Structural steel', 'Openings, mezzanines', 'By project']]),

'services/renovation.html':
 sec('What a renovation here actually involves',
     'Almost every renovation on this coast uncovers the same three things: waterproofing at the end of its life, '
     'electrical work without a proper earth, and damp that was painted over rather than diagnosed. A renovation that '
     'only addresses surfaces leaves all three in place and looks excellent for about eighteen months. We survey first '
     'and price the causes, which sometimes makes our quote look higher than one that intends to paint over them.')
 + sec('Sequence, and why it matters',
     'Survey and diagnosis; demolition with protection of what stays; structural and waterproofing corrections; services '
     'renewed while walls are open; then finishes; then fittings; then the punch list. Reordering that sequence to get a '
     'visible result sooner is the most common cause of work being done twice. Where the property is occupied or rented, '
     'we phase it so one area stays usable.')
 + sec('Living in it, renting it, or away for it',
     'Occupied renovations need dust control, a working bathroom and kitchen at all times, and predictable working hours. '
     'Rental properties need the work compressed into the low season with a hard finish date. Absentee owners get weekly '
     'dated photo reports and written approval for every change, which is how most of our renovation clients work.')
 + sec('Prices', 'Ranges per m² of intervened area in the Riviera Maya, 2026. Kitchens and bathrooms carry the highest '
       'cost per square metre because of the services behind them.')
 + table(['Scope', 'Includes', 'Cost 2026 per m²'],
         [['Cosmetic refresh', 'Paint, floors, fittings', '$4,000 – $8,000 MXN'],
          ['Kitchen and bathrooms', 'Cabinetry, tiling, plumbing', '$9,000 – $18,000 MXN'],
          ['Full interior renovation', 'Services renewed, all finishes', '$12,000 – $22,000 MXN'],
          ['Structural or layout change', 'Openings, beams, engineering', 'By project']]),

'services/residential.html':
 sec('How a house on this coast differs from one anywhere else',
     'Fractured limestone means the foundation is designed from a soils study rather than from a standard detail. Salt '
     'and humidity mean stainless fixings, dense hardwoods or aluminium outdoors, and real ingress protection on '
     'electrical work. Intense rain means waterproofing detail and drainage decide whether the house is comfortable in '
     'year three. Karst means wastewater is treated on the property rather than infiltrated. None of that is exotic; all '
     'of it is skipped by builders working from a template designed for somewhere else.')
 + sec('What is included and what is quoted separately',
     'Included in a construction contract: structure, envelope, services, finishes, joinery and external works to the '
     'agreed specification. Quoted separately, and often assumed by owners to be included: land, architectural and '
     'engineering project at roughly 4% to 8% of construction, permits and DRO, the soils study, utility connections, '
     'furniture, landscaping and the pool. We list them explicitly rather than letting them surface as extras.')
 + sec('Timeline',
     'Seven to eleven months of construction for a normal 150 to 200 m² house, plus two to six months beforehand for '
     'design and permits — longer in Tulum or near protected areas, where the environmental file sets the calendar. '
     'From decision to keys, including buying land, plan on twelve to twenty-four months.')
 + sec('Cost by finish level', 'Ranges per built square metre for turnkey construction in the Riviera Maya, 2026, '
       'excluding land, project fees and permits.')
 + table(['Level', 'What it means', 'Cost per m², 2026'],
         [['Budget', 'Basic finishes, no pool', '$12,000 – $16,000 MXN'],
          ['Mid-range', 'Good finishes, small pool', '$17,000 – $24,000 MXN'],
          ['Premium', 'Imported materials, large pool', '$25,000 – $35,000 MXN'],
          ['Luxury', 'Architect-designed throughout', '$35,000 MXN and up']]),

'services/commercial.html':
 sec('Commercial work runs on the opening date',
     'On a commercial project the schedule is the budget: every week past the opening date costs the operator revenue '
     'they can quantify precisely. That changes how the job is planned — long-lead items ordered before demolition, '
     'trades sequenced to overlap where they safely can, and the landlord or mall administration engaged before the '
     'first crew arrives rather than after they are turned away at the loading bay.')
 + sec('What we build',
     'Retail units and plaza fit-outs; offices and corporate space; restaurants and kitchens with their extraction, gas '
     'and grease-trap requirements; clinics and consulting rooms; light warehousing; and brand image work inside shopping '
     'centres. Also full remodels of premises that stay open, which is half of what we are asked for in Playa del Carmen '
     'and Cancun.')
 + sec('Offices: services decide the result, not finishes',
     'Network and electrical capacity sized for real desk density rather than for the drawing; air conditioning calculated '
     'with equipment and occupancy load; lighting designed for screens; acoustic separation between meeting rooms and open '
     'plan; and exits that satisfy civil protection. An office that looks excellent and sounds terrible gets renovated '
     'again within two years.')
 + sec('Costs', 'Ranges per m² of finished area in the Riviera Maya, 2026. Specialist installations — commercial kitchen, '
       'clinic, laboratory — are quoted separately because they change the order of magnitude.')
 + table(['Type', 'Typical scope', 'Cost 2026 per m²'],
         [['Retail fit-out', 'Finishes, services, brand image', '$7,000 – $14,000 MXN'],
          ['Corporate office', 'Partitions, network, HVAC, acoustics', '$10,000 – $20,000 MXN'],
          ['Restaurant or kitchen', 'Specialist services, extraction', '$15,000 – $30,000 MXN'],
          ['New commercial build', 'Structure, envelope, services', '$14,000 – $26,000 MXN']]),

'services/carpentry.html':
 sec('Which timbers survive this climate, and where',
     'Tzalam, chechén and chicozapote are dense regional hardwoods that behave well outdoors and age with character. '
     'Autoclave-treated pine is the economical option and acceptable when the treatment genuinely penetrates rather than '
     'coating the surface. Untreated pine outdoors is a mistake this climate punishes within a couple of seasons, between '
     'humidity and termites. Indoors the constraint relaxes, but stable, properly dried material still matters in a place '
     'where relative humidity sits high all year.')
 + sec('Kitchens and closets that survive humidity',
     'The carcass decides the lifespan. Particleboard swells and never recovers; marine-grade ply or solid material does '
     'not. Hinges and runners should be stainless or high-quality coated, because ordinary hardware seizes here. Allow '
     'ventilation behind and beneath units, and avoid sealing a cabinet tightly against an external wall, which is how '
     'mould starts in a kitchen that is cleaned every day.')
 + sec('What we make',
     'Kitchens, closets and dressing rooms, interior and entrance doors, stair treads and handrails, built-in furniture, '
     'pergolas, decks, ceilings and beams, and palapa structures in regional hardwood. Fabricated in the workshop and '
     'fitted on site, with finishing done under controlled conditions rather than in a dusty house.')
 + sec('Prices', 'Ranges for the Riviera Maya in 2026, made and installed. Material choice moves these more than '
       'complexity does.')
 + table(['Item', 'Material', 'Cost 2026'],
         [['Kitchen, linear metre', 'Marine ply, quality hardware', '$8,000 – $18,000 MXN/m'],
          ['Closet, linear metre', 'Marine ply, sliding or hinged', '$6,000 – $13,000 MXN/m'],
          ['Interior door', 'Solid or engineered', '$6,000 – $16,000 MXN'],
          ['Deck, tropical hardwood', 'Ventilated substructure', '$2,500 – $4,200 MXN/m²'],
          ['Pergola, tzalam', 'Stainless fixings', '$3,500 – $7,000 MXN/m²']]),

'services/carpinteria.html':
 sec('Qué maderas aguantan aquí y dónde ponerlas',
     'Tzalam, chechén y chicozapote son maderas duras de la región con muy buen comportamiento a la intemperie. El pino '
     'tratado en autoclave es la opción económica, aceptable cuando el tratamiento realmente penetra y no es un baño '
     'superficial. El pino sin tratar en exterior es el error que este clima castiga en un par de temporadas, entre '
     'humedad y termita. En interiores la exigencia baja, pero la madera debe venir bien seca y estable: aquí la humedad '
     'relativa es alta todo el año.')
 + sec('Cocinas y closets que resisten la humedad',
     'El cuerpo del mueble decide su vida útil. El aglomerado se hincha y no se recupera; la triplay marina o el macizo '
     'no. Bisagras y correderas de acero inoxidable o de buen recubrimiento, porque la herrajería corriente se traba. '
     'Y ventilación detrás y debajo del mueble: sellar un gabinete contra un muro exterior es como empieza el moho en una '
     'cocina que se limpia todos los días.')
 + sec('Qué fabricamos',
     'Cocinas integrales, closets y vestidores, puertas interiores y principales, escalones y pasamanos, muebles a medida, '
     'pérgolas, decks, plafones y vigas, y estructuras de palapa en madera dura regional. Se fabrica en taller y se instala '
     'en obra, con el acabado hecho en condiciones controladas y no en una casa llena de polvo.')
 + sec('Precios', 'Rangos en la Riviera Maya para 2026, fabricado e instalado. La elección de material mueve más el '
       'precio que la complejidad del diseño.')
 + table(['Concepto', 'Material', 'Costo 2026'],
         [['Cocina, metro lineal', 'Triplay marina, herrajes de calidad', '$8,000 – $18,000 MXN/m'],
          ['Closet, metro lineal', 'Triplay marina, corredizo o abatible', '$6,000 – $13,000 MXN/m'],
          ['Puerta interior', 'Sólida o de ingeniería', '$6,000 – $16,000 MXN'],
          ['Deck de madera dura', 'Rastreles ventilados', '$2,500 – $4,200 MXN/m²'],
          ['Pérgola de tzalam', 'Herraje inoxidable', '$3,500 – $7,000 MXN/m²']]),

'services/herreria.html':
 sec('Qué se corroe primero, y nunca es el acero que se ve',
     'En esta costa la falla empieza en las uniones y en la tornillería: un tornillo galvanizado corriente en un conjunto '
     'inoxidable, una soldadura que nunca se limpió, o una pintura aplicada sobre calamina. La sal encuentra esos puntos y '
     'el óxido avanza desde ahí mientras la superficie visible todavía se ve bien. Por eso la especificación importa más '
     'que el metal, y por eso dos barandales idénticos se comportan distinto al cuarto año.')
 + sec('Acabados que sí duran',
     'Galvanizado por inmersión y después pintura electrostática es la combinación durable para exterior y estructura. '
     'Acero inoxidable marino para barandales frente al mar, herrajes junto a la alberca y todo lo que reciba salpicadura. '
     'Aluminio con pintura electrostática donde importan peso y corrosión. Pintura común sobre acero sin preparar es una '
     'solución de dos temporadas vendida al precio de una.')
 + sec('Qué fabricamos',
     'Barandales y balaustradas, portones y estructuras para portón automático, protecciones que no parezcan rejas, '
     'estructuras de pérgola y cubiertas, escaleras y peldaños, herrería de ventana y acero estructural para claros y '
     'entrepisos. Se fabrica en taller y se monta en obra, para que el trabajo ruidoso no ocurra dentro de una casa habitada.')
 + sec('Precios', 'Rangos en la Riviera Maya, fabricado e instalado. El diseño y el acabado mueven el precio mucho más '
       'que los kilos de metal.')
 + table(['Concepto', 'Especificación', 'Costo 2026'],
         [['Barandal de acero con pintura electrostática', 'Galvanizado y recubierto', '$1,800 – $3,500 MXN/m'],
          ['Barandal de inoxidable marino', 'Frente al mar', '$4,500 – $9,000 MXN/m'],
          ['Estructura de portón corredizo', 'Hasta 4 m, sin motor', '$25,000 – $60,000 MXN'],
          ['Protecciones de ventana', 'Por vano, diseñadas', '$3,500 – $9,000 MXN'],
          ['Acero estructural', 'Claros, entrepisos', 'Por proyecto']]),

'services/permisos.html':
 sec('El orden correcto del expediente',
     'Primero la constancia de uso de suelo: si el predio no admite lo que quiere construir, no hay proyecto que lo '
     'arregle y todo lo demás sobra. Después alineamiento y número oficial, factibilidad de servicios, el proyecto '
     'firmado por DRO, y con eso la licencia de construcción. En paralelo, cuando aplica, el expediente ambiental, que '
     'es el que realmente marca el calendario en Tulum, Puerto Morelos y zonas cercanas a áreas protegidas.')
 + sec('Por qué se devuelven los expedientes',
     'Casi nunca porque la autoridad se demore: porque el expediente llega incompleto. Planos que no corresponden a la '
     'constancia de uso de suelo, densidad o altura fuera de lo permitido, manejo de aguas sin resolver, documentación '
     'del DRO que llega después del resto, o superficie declarada que no coincide con el levantamiento. Cada devolución '
     'reinicia tiempos, y es la diferencia entre tres semanas y tres meses.')
 + sec('Qué hacemos nosotros y qué depende de la autoridad',
     'Nosotros integramos el expediente, gestionamos DRO, presentamos y damos seguimiento, y respondemos requerimientos. '
     'Lo que no controlamos son los tiempos de resolución ni el criterio ambiental. Se lo decimos con plazos realistas '
     'desde el principio, porque una fecha optimista al inicio se convierte en un problema de obra tres meses después.')
 + sec('Trámites y tiempos', 'Órdenes de magnitud en la región para obra residencial. Varían por municipio y por '
       'superficie.')
 + table(['Trámite', 'Para qué sirve', 'Costo y tiempo'],
         [['Constancia de uso de suelo', 'Uso, densidad, COS, CUS, altura', '$1,500 – $6,000 MXN · 1–3 semanas'],
          ['Alineamiento y número oficial', 'Límites y frente del predio', '$800 – $3,500 MXN · 1–2 semanas'],
          ['Licencia de construcción con DRO', 'Autoriza la obra', 'Según superficie · 3–10 semanas'],
          ['Expediente ambiental', 'Cuando aplica', 'Por proyecto · meses'],
          ['Terminación de obra', 'Cierre del expediente', 'Según municipio']]),

'blog-es/costo-construir-casa-tulum.html':
 sec('Por qué Tulum cuesta distinto al resto del corredor',
     'Dos razones concretas. La primera es el trámite: el componente ambiental es el más exigente de la región y puede '
     'mover el arranque de obra varios meses, y el tiempo también cuesta. La segunda es el suelo y el agua: en zonas con '
     'sistemas de cenotes, el manejo de aguas residuales y pluviales se resuelve con tratamiento y contención, no con '
     'infiltración, y eso es una partida real. A eso se suma que la mano de obra especializada compite con la construcción '
     'hotelera de la zona.')
 + sec('Lo que casi nadie incluye en su presupuesto inicial',
     'Terreno, proyecto arquitectónico y ejecutivo (del 4% al 8% de la obra), estudio de mecánica de suelos, licencia y '
     'DRO, expediente ambiental cuando aplica, conexiones de servicios, tratamiento de aguas, alberca, mobiliario y '
     'paisajismo. La diferencia entre el costo de obra por m² y el desembolso total suele estar entre el 25% y el 40%, '
     'y es exactamente donde se rompen los presupuestos de primera vez.')
 + sec('Cómo se reparte el costo',
     'Porcentajes aproximados para una casa de nivel medio en Tulum. Sirven para detectar un presupuesto desequilibrado '
     'antes de leer el detalle: unos acabados al 12% o una cimentación al 4% le están diciendo algo.')
 + table(['Partida', '% del costo de obra', 'Nota'],
         [['Preliminares y cimentación', '12% – 18%', 'Sube con cavidades o relleno'],
          ['Estructura y albañilería', '25% – 32%', 'Concreto, acero, muros, losas'],
          ['Instalaciones', '14% – 18%', 'Incluye tratamiento de aguas'],
          ['Acabados', '22% – 30%', 'La partida que más varía'],
          ['Carpintería y herrería', '8% – 12%', 'Cocina, closets, cancelería'],
          ['Exteriores y limpieza', '4% – 8%', 'Andadores, jardín, entrega']])
 + sec('Cómo bajar el costo sin arruinar la casa',
     'Se puede: geometría simple en lugar de volúmenes complicados, acabados nacionales de buena calidad en lugar de '
     'importados, alberca más chica y bien equipada en lugar de grande y básica, y decidir toda la especificación antes '
     'de colar la losa. Lo que no se debe tocar: estudio de suelos, cimentación, impermeabilización, instalaciones '
     'ocultas y tratamiento de aguas. Ahorrar ahí es diferir un gasto mayor, no evitarlo.'),

'blog-es/permisos-construccion-cancun.html':
 sec('Impacto vial: lo que más se subestima en Benito Juárez',
     'En Cancún el dictamen de impacto vial pesa más que en cualquier otro municipio de la región. Accesos y salidas '
     'sobre avenidas de alto flujo, carriles auxiliares, radios de giro y maniobras de vehículos pesados se revisan con '
     'detalle, y un proyecto que resuelve la arquitectura pero ignora el vial se devuelve. Conviene plantearlo en el '
     'anteproyecto, cuando mover un acceso todavía es un trazo y no una obra.')
 + sec('El reglamento del fraccionamiento suele mandar más que el municipio',
     'Retiros mayores, altura menor, paleta de materiales y colores obligatoria, horarios de obra, depósito de garantía '
     'y plazo máximo de construcción. Todo eso es exigible contra usted independientemente de lo que permita el '
     'municipio, y se revisa junto con la constancia de uso de suelo. Rediseñar después de la aprobación municipal cuesta '
     'honorarios y semanas.')
 + sec('Documentos que integran el expediente',
     'Constancia de uso de suelo, alineamiento y número oficial, proyecto arquitectónico y estructural firmado por DRO '
     'con registro vigente, memorias de cálculo, factibilidad de servicios, y según el caso impacto vial, visto bueno de '
     'protección civil y autorización ambiental. Falta uno y el expediente espera completo, no avanza en partes.')
 + sec('Tiempos y costos', 'Órdenes de magnitud para obra residencial en Benito Juárez. La superficie y el tipo de '
       'zona mueven ambos.')
 + table(['Trámite', 'Tiempo típico', 'Nota'],
         [['Constancia de uso de suelo', '1 – 3 semanas', 'Primero de todo'],
          ['Alineamiento y número oficial', '1 – 2 semanas', 'Define frente y límites'],
          ['Dictamen de impacto vial', '2 – 6 semanas', 'Según ubicación y giro'],
          ['Licencia de construcción', '3 – 10 semanas', 'Con DRO vigente'],
          ['Terminación de obra', 'Al cierre', 'Necesaria para habitabilidad']]),

'blog-es/permisos-construccion-tulum.html':
 sec('El expediente ambiental manda sobre el calendario',
     'En Tulum el trámite que decide cuándo arranca la obra no es el municipal: es el ambiental. Suelo kárstico, cenotes '
     'y áreas naturales protegidas obligan a justificar con detalle el manejo de escurrimientos, el tratamiento de aguas '
     'residuales y la contención de cualquier derrame. Un expediente bien armado avanza; uno incompleto se devuelve y '
     'reinicia tiempos. Por eso la programación seria empieza por el trámite y no por la obra.')
 + sec('Qué revisa la autoridad con más detalle aquí',
     'Distancia a cenotes y cuerpos de agua, profundidad respecto al manto freático, si hay tratamiento antes de '
     'cualquier infiltración, manejo del agua pluvial del predio, y afectación de vegetación. En predios dentro o '
     'colindantes con área protegida se suma el programa de manejo de esa área, con sus propias reglas de densidad, '
     'altura e iluminación.')
 + sec('Errores que cuestan meses',
     'Comprar el terreno sin verificar uso de suelo ni situación ambiental. Encargar el proyecto antes de tener la '
     'constancia. Proponer infiltración de aguas residuales sin tratamiento, que se rechaza. Presentar documentación del '
     'DRO después del resto del expediente. Y asumir que lo que se autorizó en un predio vecino se autorizará en el suyo.')
 + sec('Tiempos realistas', 'Rangos con los que planificamos en Tulum. Suponen expediente completo: uno incompleto '
       'reinicia el reloj en lugar de pausarlo.')
 + table(['Etapa', 'Tiempo típico', 'Nota'],
         [['Constancia de uso de suelo', '1 – 3 semanas', 'Antes de diseñar'],
          ['Expediente ambiental', 'Meses', 'Marca el calendario completo'],
          ['Licencia de construcción con DRO', '3 – 10 semanas', 'Tras el resto del expediente'],
          ['Inicio de obra', 'Solo con licencia', 'Arrancar sin ella es caro']]),

'blog-es/guia-construccion-palapas.html':
 sec('Cuánto dura de verdad y de qué depende',
     'El huano bien colocado suele durar entre 8 y 15 años antes de requerir recambio, y el rango es amplio por lo que '
     'la rodea. La sombra permanente y la humedad que nunca seca la acortan mucho: una palapa bajo árboles falla antes '
     'que una a sol abierto. La ventilación por debajo la alarga. También la pendiente pronunciada y el traslape '
     'correcto. El armazón de madera dura sobrevive a varios ciclos de palma, y por eso re-enpalapar cuesta una fracción.')
 + sec('Tratamiento contra fuego, seguro y reglamento',
     'La palma se puede tratar con retardante de fuego, y en propiedades comerciales o de renta normalmente debe hacerse: '
     'muchas aseguradoras lo exigen y algunos municipios también. Aplicado durante la construcción cuesta mucho menos que '
     'después. Confirme además la altura y ubicación permitidas por su municipio o fraccionamiento, y avise a su '
     'aseguradora antes de construir, no después de un siniestro.')
 + sec('Mantenimiento que sí importa',
     'Revisión anual del amarre y de los apoyos, limpieza de hojas acumuladas en los valles, poda de ramas que dan sombra '
     'permanente sobre la cubierta, y reposición puntual de zonas dañadas antes de que el agua entre al armazón. Una '
     'palapa atendida llega al extremo alto de su vida útil; una abandonada, al bajo.')
 + sec('Costos 2026', 'Rangos por m² cubierto en la Riviera Maya, con armazón de madera dura y cubierta de huano.')
 + table(['Concepto', 'Detalle', 'Costo 2026 por m²'],
         [['Palapa nueva', 'Armazón de madera dura y huano', '$4,000 – $9,000 MXN'],
          ['Armazón premium', 'Chicozapote, ensambles a la vista', '$7,000 – $12,000 MXN'],
          ['Re-enpalapado', 'Se conserva el armazón', '$1,500 – $3,500 MXN'],
          ['Retardante de fuego', 'Aplicado en construcción', 'Suma $250 – $600 MXN']]),

'blog/palapa-construction-guide-riviera-maya.html':
 sec('How long thatch really lasts, and what decides it',
     'Well-laid huano typically lasts 8 to 15 years before it needs replacing, and the spread is that wide because of '
     'what surrounds it. Permanent shade and damp that never dries shorten it considerably — a palapa under trees fails '
     'sooner than one in open sun. Ventilation underneath extends it, as does a steep pitch and correct layering. The '
     'hardwood frame outlives several thatch cycles, which is why re-thatching costs a fraction of the original build.')
 + sec('Fire treatment, insurance and permits',
     'Thatch can be treated with a fire retardant, and for rental or commercial properties it usually must be: many '
     'insurers require it and some municipalities do too. Applied during construction it costs far less than afterwards. '
     'Confirm permitted height and placement with your municipality or gated development, and tell your insurer before '
     'building rather than after a claim.')
 + sec('Maintenance that actually matters',
     'An annual check of the ties and the bearing points, clearing accumulated leaves from the valleys, trimming branches '
     'that keep the roof permanently shaded, and patching damaged areas before water reaches the frame. A maintained '
     'palapa reaches the top of its life range; a neglected one reaches the bottom.')
 + sec('Costs in 2026', 'Ranges per m² of covered area in the Riviera Maya, with a hardwood frame and huano thatch.')
 + table(['Item', 'Detail', 'Cost 2026 per m²'],
         [['New palapa', 'Hardwood frame and huano thatch', '$4,000 – $9,000 MXN'],
          ['Premium frame', 'Chicozapote, exposed joinery', '$7,000 – $12,000 MXN'],
          ['Re-thatching', 'Frame retained', '$1,500 – $3,500 MXN'],
          ['Fire-retardant treatment', 'Applied during construction', 'Adds $250 – $600 MXN']]),

'blog/construction-permits-cancun.html':
 sec('Traffic impact is the step foreign owners never expect',
     'In Benito Juárez the traffic-impact opinion carries more weight than in any other municipality on this coast. '
     'Access and exit onto high-flow avenues, auxiliary lanes, turning radii and heavy-vehicle movements are reviewed in '
     'detail, and a project that solves the architecture while ignoring the traffic gets returned. Raise it at concept '
     'stage, while moving an entrance is still a line on a drawing.')
 + sec('The gated-community rulebook usually outranks the municipality',
     'Greater setbacks, lower heights, mandatory materials and colours, working hours, a damage deposit and a maximum '
     'construction period. All of it is enforceable against you regardless of what the municipality allows, and it should '
     'be reviewed alongside the land-use certificate. Redesigning after municipal approval costs fees and weeks.')
 + sec('What the file must contain',
     'Land-use certificate; alignment and official number; architectural and structural project signed by a DRO with '
     'current registration; calculation reports; services feasibility; and depending on the case, traffic impact, civil '
     'protection sign-off and environmental authorisation. Missing one item does not slow the file down — it stops it.')
 + sec('Timelines', 'Orders of magnitude for residential work in Benito Juárez. Area and zone move both cost and time.')
 + table(['Step', 'Typical time', 'Note'],
         [['Land use certificate', '1 – 3 weeks', 'Before anything else'],
          ['Alignment and official number', '1 – 2 weeks', 'Defines frontage and limits'],
          ['Traffic impact opinion', '2 – 6 weeks', 'By location and use'],
          ['Construction licence', '3 – 10 weeks', 'With a current DRO'],
          ['Completion certificate', 'At closing', 'Needed for occupancy']]),
}


def insert(path, block):
    s = open(path, encoding='utf-8').read()
    s = re.sub(re.escape(OPEN) + r'.*?' + re.escape(CLOSE), '', s, flags=re.S)
    payload = OPEN + '\n' + block + CLOSE + '\n'
    # place before the FAQ heading, else before the CTA, else before the footer
    m = (re.search(r'\n[ \t]*<h2[^>]*>\s*(Preguntas Frecuentes|Frequently Asked Questions|FAQ)', s)
         or re.search(r'\n[ \t]*<div class="cta-section', s)
         or re.search(r'\n[ \t]*<section data-cluster=', s))
    at = (s.rfind('\n', 0, m.start() + 1) + 1) if m else s.rfind('<footer')
    s = s[:at] + payload + s[at:]
    open(path, 'w', encoding='utf-8').write(s)
    w = len(re.sub(r'<[^>]+>', ' ', s[s.index('<h1'):s.index('<footer')]).split())
    return w


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for path, block in BLOCKS.items():
        if not os.path.exists(path):
            print('  missing:', path); continue
        before = len(re.sub(r'<[^>]+>', ' ', (lambda t: t[t.index('<h1'):t.index('<footer')])(
            open(path, encoding='utf-8').read())).split())
        after = insert(path, block)
        print('%-48s %4d -> %4d words' % (path, before, after))
