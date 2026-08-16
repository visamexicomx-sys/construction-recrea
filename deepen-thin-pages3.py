#!/usr/bin/env python3
"""Third depth pass: the 42 remaining thin pages with 5+ impressions (2026-08-15).

Six languages. Every block below is written in the language of the page it lands
on — authored, not machine-translated — and every one is specific to its page.

The tail beyond this batch (119 pages at 1-4 impressions each, ~330 impressions
in total) is handled in the fourth pass, because writing 119 more blocks at this
standard is a separate piece of work and doing it carelessly would undo the point
of doing it at all.
"""
import os, re

OPEN, CLOSE = '<div data-depth="2026-08">', '</div><!--/depth-->'


def sec(h, p):
    return '<h2 class="mt-4">%s</h2>\n<p>%s</p>\n' % (h, p)


def tbl(head, rows):
    return ('<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr>'
            + ''.join('<th>%s</th>' % h for h in head) + '</tr></thead><tbody>\n'
            + '\n'.join('<tr>' + ''.join('<td>%s</td>' % c for c in r) + '</tr>' for r in rows)
            + '\n</tbody></table></div>\n')


B = {

# ---------------------------------------------------------------------- Spanish
'blog-es/ventanas-puertas-clima-tropical.html':
 sec('La serie del perfil importa tanto como el cristal',
     'Una serie ligera con cristal templado se comporta muy distinto a una serie estructural con el mismo cristal: '
     'cambia la hermeticidad, el sellado y el comportamiento en vanos grandes con viento. En fachadas expuestas y en '
     'corredizas de gran formato, la serie es lo que evita que entre agua con lluvia y viento cruzado.')
 + sec('Cristal: control solar antes que cualquier otra cosa',
     'En esta latitud el cristal de control solar reduce la carga térmica que después paga el aire acondicionado todo el '
     'año, y es lo primero que conviene especificar en poniente y sur. Doble cristal cuando importa el ruido. Laminado '
     'cuando se busca resistencia a impacto y seguridad, que en costa expuesta es la única protección que funciona sin '
     'que alguien la cierre antes del huracán.')
 + sec('Donde se filtra no es el cristal, es el encuentro',
     'Casi todas las filtraciones por ventana vienen del perímetro: sellado deficiente contra el muro, ausencia de '
     'goterón, alféizar sin pendiente. Un producto excelente mal instalado gotea igual que uno malo, y la mancha aparece '
     'adentro tras la primera lluvia con viento.')
 + sec('Precios 2026', 'Por m² de vano instalado en la Riviera Maya.')
 + tbl(['Tipo', 'Uso recomendado', 'Costo por m²'],
       [['Serie ligera, cristal claro', 'Vanos pequeños protegidos', '$1,800 – $3,000 MXN'],
        ['Serie intermedia, templado', 'Estándar residencial', '$3,000 – $5,000 MXN'],
        ['Serie estructural, control solar', 'Vanos grandes, exposición alta', '$5,000 – $9,000 MXN'],
        ['Laminado de impacto', 'Costa expuesta', '$8,000 – $15,000 MXN']]),

'noticias/index.html':
 sec('Qué publicamos aquí',
     'Cambios normativos que afectan a quien construye en Quintana Roo: reglamentos municipales, criterios ambientales, '
     'trámites que cambian de dependencia o de requisitos. Movimientos de precios de materiales cuando son lo bastante '
     'grandes para mover un presupuesto. Y notas de obra propia cuando enseñan algo aplicable a otros proyectos.')
 + sec('Por qué esto le importa si está construyendo',
     'En esta región el marco cambia con cierta frecuencia, y los cambios rara vez se anuncian donde un propietario los '
     'vería. Un requisito ambiental nuevo, una vigencia de licencia distinta o una dependencia federal que cambia de '
     'nombre pueden mover el calendario de una obra en curso. Preferimos que se entere aquí y no cuando le devuelvan un '
     'expediente.')
 + sec('Cómo leemos el mercado',
     'Con cifras, no con optimismo: costos por m² que efectivamente cotizamos, plazos de trámite que efectivamente '
     'tardaron, y cuando algo se encareció, cuánto. Si un dato nos parece poco sólido, lo decimos en lugar de '
     'publicarlo como certeza.'),

'services/residencial.html':
 sec('Qué hace distinta a una casa en esta costa',
     'Caliza fracturada: la cimentación se diseña con estudio de suelos, no con un detalle estándar. Sal y humedad: '
     'herrajes inoxidables, maderas densas o aluminio en exteriores, y protección real en la instalación eléctrica. '
     'Lluvia intensa: la impermeabilización y el drenaje deciden si la casa es cómoda en el año tres. Karst: las aguas '
     'residuales se tratan en el predio, no se infiltran. Nada de eso es exótico; todo se omite cuando se construye con '
     'una plantilla pensada para otro clima.')
 + sec('Qué incluye el contrato y qué se cotiza aparte',
     'Incluye: estructura, envolvente, instalaciones, acabados, carpintería y exteriores según especificación. Aparte, y '
     'con frecuencia el propietario supone lo contrario: terreno, proyecto arquitectónico y ejecutivo (4% a 8%), '
     'permisos y DRO, estudio de suelos, conexiones, mobiliario, paisajismo y alberca. Lo listamos explícito para que no '
     'aparezca después como obra extra.')
 + sec('Plazos', 'De 7 a 11 meses de obra para una casa normal de 150 a 200 m², más 2 a 6 meses previos de proyecto y '
       'trámite —más en Tulum o cerca de áreas protegidas, donde el expediente ambiental marca el calendario.')
 + sec('Costos por nivel de acabado', 'Por m² construido en la Riviera Maya, sin terreno, proyecto ni permisos.')
 + tbl(['Nivel', 'Qué implica', 'Costo por m²'],
       [['Económico', 'Acabados básicos, sin alberca', '$12,000 – $16,000 MXN'],
        ['Medio', 'Buenos acabados, alberca chica', '$17,000 – $24,000 MXN'],
        ['Premium', 'Materiales importados, alberca grande', '$25,000 – $35,000 MXN'],
        ['Lujo', 'Diseño de autor', 'Desde $35,000 MXN']]),

'mapa-precios/index.html':
 sec('De dónde salen estas cifras',
     'Son nuestros costos de obra en el corredor, actualizados a 2026, por metro cuadrado construido y agrupados por '
     'ciudad y zona. No son precios de terreno ni de propiedad terminada: eso se mueve por razones que nada tienen que '
     'ver con lo que cuesta construir. Cuando una zona sale más cara aquí, es por factores constructivos reales.')
 + sec('Por qué una zona cuesta más que su vecina',
     'Isla: alrededor de 15% más por flete marítimo, tiempos de entrega y estancia de cuadrilla. Fraccionamiento: comité '
     'de diseño, horarios restringidos y control de acceso. Cerca de área protegida: exigencias ambientales que se ven '
     'en drenaje y tratamiento, no en acabados. Y caliza con cavidades o relleno: cimentación más cara, que depende del '
     'lote y no del código postal.')
 + sec('Cómo usar el mapa antes de comprar terreno',
     'Tome la banda de la zona, aplíquela a la superficie que quiere, y sume lo que nunca aparece en un precio por m²: '
     'proyecto 4% a 8%, permisos y DRO, estudio de suelos, conexiones, mobiliario y alberca. Ese total, y no la línea de '
     'obra, es lo que debe compararse contra el precio de una propiedad terminada en la misma zona.'),

'services/electrico.html':
 sec('Cómo se cablea de verdad una casa aquí',
     'Circuitos separados para iluminación, contactos generales, cocina, y uno dedicado por cada equipo de aire '
     'acondicionado, por bomba y por el equipo de alberca. No es lujo: es lo que evita que el interruptor bote en agosto '
     'con todo encendido. El calibre se elige por carga y por distancia, y las corridas largas a una bomba de jardín o a '
     'un portón se calculan en lugar de suponerse. Todo se prueba antes de tapar muros.')
 + sec('Tierra física, sobretensiones y costa',
     'La tierra física con su electrodo y su puenteo es lo que protege a las personas y a los equipos, y es la primera '
     'partida que desaparece de un presupuesto barato. Con tormentas eléctricas frecuentes, la protección contra '
     'sobretensiones en el tablero vale su costo modesto. Y cerca del mar, tableros y salidas de exterior con grado de '
     'protección real, porque la sal entra por donde el plástico barato ya no cierra.')
 + sec('Qué dejar preparado durante la obra',
     'Canalización y espacio en tablero para paneles solares, aunque lleguen después. Circuito para bomba de alberca y '
     'equipo de tratamiento. Alimentación para portón automático. Punto de carga de vehículo eléctrico. Y cableado de '
     'red donde vaya a trabajar, incluida la terraza. Todo cuesta una fracción con los muros abiertos.')
 + sec('Precios 2026', 'Vivienda en la Riviera Maya, material de marca y mano de obra. La acometida CFE se cotiza según '
       'carga y sitio.')
 + tbl(['Alcance', 'Aplicación', 'Costo 2026'],
       [['Instalación completa, obra nueva', 'Por m² construido', '$450 – $900 MXN/m²'],
        ['Por salida', 'Obra o remodelación', '$600 – $1,200 MXN'],
        ['Tablero con protecciones', 'Casa unifamiliar', '$12,000 – $35,000 MXN'],
        ['Tierra física', 'Varilla, conductor, registro', '$6,000 – $18,000 MXN']]),

'blog-es/precios-terrenos-playa-del-carmen-tulum-2026.html':
 sec('El precio por m² no es lo que decide si el terreno es bueno',
     'Dos lotes al mismo precio pueden tener valores muy distintos según cinco cosas que no se ven caminándolo: uso de '
     'suelo y densidad permitida, COS y CUS, altura máxima, si toca área protegida o zona federal, y qué hay debajo. Un '
     'terreno barato donde no cabe lo que quiere construir no es barato.')
 + sec('Ejidal contra propiedad privada',
     'Es la distinción que más dinero ha costado a compradores extranjeros en Quintana Roo. La tierra ejidal es comunal '
     'y no se transmite libremente hasta estar regularizada en propiedad privada, sin importar qué documento le muestren. '
     'Se verifica en el registro público antes que cualquier otra cosa, y un precio muy por debajo del mercado es motivo '
     'para revisar más, no menos.')
 + sec('Lo que conviene gastar antes de comprar',
     'Levantamiento topográfico: la superficie escriturada y la real difieren con más frecuencia de la que uno espera, y '
     'un desnivel que no se ve caminando puede significar relleno o muro de contención. Estudio de mecánica de suelos: '
     'en caliza fracturada la cimentación cambia entre lotes vecinos. Constancia de uso de suelo. Y factibilidad de '
     'servicios, porque extender una línea eléctrica corre por cuenta del propietario.'),

'blog-es/fosas-septicas-biodigestores-riviera-maya.html':
 sec('Por qué la fosa tradicional no es la respuesta aquí',
     'La península es caliza fracturada: lo que se infiltra llega rápido al acuífero, y el acuífero descarga en cenotes '
     'y en el mar sobre el arrecife. Por eso la autoridad ambiental condiciona o rechaza proyectos que descarguen sin '
     'tratamiento, y por eso una fosa séptica simple para aguas negras es, además de un problema legal, un problema para '
     'el agua que usa toda la zona.')
 + sec('Biodigestor o planta compacta',
     'Biodigestor autolimpiable para casa unifamiliar, dimensionado por número de usuarios y aportación diaria. Planta '
     'de tratamiento compacta cuando el aforo lo justifica: hotel pequeño, restaurante, varias viviendas. El efluente ya '
     'tratado puede reutilizarse en riego o infiltrarse según lo que autorice el permiso, que no es lo mismo que '
     'infiltrar sin tratar.')
 + sec('El mantenimiento es parte del permiso',
     'Purga de lodos periódica —según uso, cada 12 a 24 meses— y revisión anual. Sin eso el equipo deja de cumplir y la '
     'condición del permiso queda en falta. Si usted no vive aquí, eso va en un contrato de mantenimiento y no en su '
     'memoria.')
 + sec('Costos 2026', 'Instalado en la Riviera Maya.')
 + tbl(['Solución', 'Cuándo aplica', 'Costo'],
       [['Biodigestor autolimpiable', 'Casa, 5–10 usuarios', '$25,000 – $60,000 MXN'],
        ['Planta compacta', 'Hotel, restaurante, varias viviendas', '$180,000 – $600,000 MXN'],
        ['Trampa de grasas', 'Cocinas y servicio', '$8,000 – $25,000 MXN']]),

'blog-es/paneles-solares-casas-riviera-maya.html':
 sec('Aquí el ahorro se mide contra el aire acondicionado',
     'Las tarifas de CFE son escalonadas y cruzar al rango de alto consumo cambia el recibo de golpe. Una casa con aire '
     'acondicionado durante el verano y bomba de alberca vive justo en ese límite, y ahí es donde un sistema solar bien '
     'dimensionado cambia más la factura anual. Dimensionar contra el consumo real de doce meses, no contra la superficie '
     'de techo disponible.')
 + sec('Net metering, y qué hay que entender antes',
     'El excedente que inyecta a la red se compensa, no se paga como si vendiera energía, y el esquema tiene reglas y '
     'plazos. Sobredimensionar para generar mucho más de lo que consume rara vez conviene. Lo que sí conviene es cubrir '
     'bien el consumo propio y dejar previsto crecer después, que es más barato si la canalización y el espacio de '
     'tablero se dejaron en obra.')
 + sec('Lo que este clima le hace a un sistema solar',
     'Sal, humedad y polvo reducen el rendimiento si no se limpia; la temporada de huracanes exige anclaje calculado, no '
     'solo apoyado; y la orientación importa menos que la sombra, porque una palma que crece dos metros puede costarle '
     'un porcentaje notable de generación. La estructura y los herrajes deben ser inoxidables o de aluminio, no '
     'galvanizado corriente.'),

'blog-es/mudarse-a-playa-del-carmen-guia.html':
 sec('Rente antes de comprar, y rente en la temporada que menos le gusta',
     'Pase unos meses aquí antes de comprometer capital, y procure que alguno caiga en el calor húmedo de finales de '
     'verano y no solo en el invierno seco que todos visitan. Colonias que se sienten iguales en febrero se comportan '
     'muy distinto en septiembre: ruido, encharcamiento, mosquitos y si la calle es realmente donde quiere vivir todo el '
     'año.')
 + sec('La lista práctica que nadie le entrega',
     'Situación migratoria y qué le permite hacer. Cuenta bancaria mexicana, que normalmente exige residencia. RFC si va '
     'a tener ingresos por renta. Cobertura médica decidida antes de necesitarla. Número local, porque aquí todo pasa por '
     'WhatsApp. Y una visión realista del transporte: fuera del centro caminable, el coche es prácticamente necesario.')
 + sec('Lo que se subestima',
     'Cuánto castiga la humedad a las cosas y a los edificios. Cuánto cuesta operar aire acondicionado. Cuánto tarda '
     'cualquier trámite y cuánto mejora con los papeles preparados de antemano. Y cuánto cambia la vida diaria con '
     'español funcional, aunque en la zona turística todos hablen inglés.'),

'blog-es/construccion-villa-lujo-playacar.html':
 sec('Playacar tiene reglamento propio, y manda',
     'Comité de diseño que revisa el proyecto antes que el municipio, retiros y alturas más estrictos, paleta de '
     'materiales y colores, horarios de obra, control de acceso para personal y vehículos, y plazos máximos de '
     'construcción con depósito. Todo eso es exigible y cambia tanto el diseño como el costo. Se revisa antes de dibujar, '
     'no después de la aprobación municipal.')
 + sec('Qué distingue a una villa de lujo aquí de una casa grande',
     'No los metros: la especificación y las instalaciones. Cristalería estructural con control solar, carpintería a '
     'medida en maderas densas, herrajes inoxidables en todo el exterior, iluminación por capas con control de escenas, '
     'aire acondicionado dimensionado con carga real y silencioso, alberca con desbordante y equipo de mayor capacidad, '
     'y un back of house que no se ve: cuarto de máquinas, lavandería, almacenamiento y acceso de servicio.')
 + sec('Costos 2026', 'Por m² construido en Playacar, obra terminada, sin mobiliario ni paisajismo.')
 + tbl(['Nivel', 'Qué implica', 'Costo por m²'],
       [['Alto residencial', 'Buenos acabados nacionales', '$25,000 – $32,000 MXN'],
        ['Lujo', 'Especificación importada, carpintería a medida', '$32,000 – $48,000 MXN'],
        ['Villa de autor', 'Diseño singular, materiales especiales', 'Desde $48,000 MXN']]),

'blog-es/paisajismo-tropical-riviera-maya.html':
 sec('Especies que aguantan sal, sequía y lluvia intensa',
     'La península tiene seis meses secos y seis de lluvia concentrada, más salinidad en costa. Funciona lo nativo y lo '
     'adaptado: chit y otras palmas locales, uva de mar en primera línea, buganvilia, plumbago, crotos, agaves y '
     'suculentas donde pega el sol, y helechos y filodendros en sombra. Lo que falla es la paleta copiada de un proyecto '
     'de clima templado, que exige riego constante y muere en la primera seca.')
 + sec('Riego y suelo: lo que nadie ve',
     'Sobre caliza el sustrato suele ser delgado, así que casi todo jardín serio aquí implica aportar tierra y mejorar. '
     'El riego automático sectorizado es lo que evita replantar cada primavera, y regar de madrugada reduce mucho la '
     'evaporación. Un jardín sin riego programado en esta región no es de bajo mantenimiento: es de vida corta.')
 + sec('Huracanes y árboles junto a la casa',
     'Poda de formación desde jóvenes, distancia de plantación pensada para el tamaño adulto, y revisión anual de ramas '
     'sobre techo y sobre instalaciones. La mayoría de los daños de temporada en casas bien construidas los provoca '
     'vegetación mal ubicada, no el viento en sí.'),

'blog-es/casa-autosuficiente-fuera-de-red.html':
 sec('Fuera de red aquí significa tres sistemas, no uno',
     'Energía: solar con banco de baterías dimensionado para días nublados, y casi siempre un generador de respaldo, '
     'porque en temporada de lluvias hay semanas de baja generación. Agua: captación pluvial con almacenamiento '
     'suficiente para la temporada seca, o pozo donde el predio lo permita, más filtración. Aguas residuales: '
     'biodigestor o planta compacta, nunca infiltración sin tratar. Fallar en cualquiera de los tres convierte la casa '
     'en un problema, no en una independencia.')
 + sec('Dimensionar de verdad, con el aire acondicionado dentro',
     'El error habitual es calcular el consumo sin contar el aire acondicionado, que en este clima es la carga dominante. '
     'Una casa fuera de red cómoda aquí se diseña primero para necesitar menos: orientación, ventilación cruzada, '
     'aislamiento, protección solar en poniente y masa térmica. Después se dimensiona el sistema. Al revés sale carísimo.')
 + sec('Costos y lo que conviene esperar',
     'Un sistema solar con baterías para una casa que opera aire acondicionado varias horas al día es una inversión '
     'considerable, y el banco de baterías es la partida que se reemplaza con los años. Conviene planear el reemplazo '
     'desde el principio en lugar de descubrirlo en el año ocho.'),

'blog-es/cisternas-almacenamiento-agua.html':
 sec('Por qué aquí toda casa almacena',
     'La red municipal no es continua ni de presión constante en todas partes, así que la casa guarda: cisterna a nivel '
     'o enterrada, bomba que presuriza, y con frecuencia tanque hidroneumático o bomba de velocidad variable para que la '
     'presión no varíe con cada llave que se abre. Algunas propiedades suman tinaco alto como respaldo por gravedad.')
 + sec('Dimensionar el volumen',
     'Se calcula por número de habitantes, uso previsto y por cuántos días quiere autonomía si falla el suministro. Una '
     'casa familiar suele resolverse con varios miles de litros; una villa de renta con ocupación alta necesita bastante '
     'más, y si hay alberca, el llenado y reposición se contemplan aparte. Quedarse corto se nota en la primera semana '
     'de temporada alta.')
 + sec('Construcción y limpieza',
     'Impermeabilización interior adecuada, tapa hermética que impida entrada de insectos y luz, acceso real para '
     'limpieza, y ventilación. La limpieza al menos anual no es opcional: una cisterna sin mantenimiento cambia el sabor '
     'del agua y la calidad de todo lo que sale de la llave. Y si capta agua de lluvia, hace falta separador de primeras '
     'aguas antes de la entrada.'),

# ---------------------------------------------------------------------- English
'services/all-services.html':
 sec('How we work, in one page',
     'Fixed price against a line-item budget with quantities and unit prices, so the number you sign is the number you '
     'pay unless the scope changes. Payments tied to verifiable progress rather than calendar dates. Change orders priced '
     'and signed before execution. Weekly reports with dated photographs, which is how most of our clients work because '
     'they do not live in Mexico.')
 + sec('What we cover, and where we stop',
     'New residential construction, villas and small developments; full and partial renovation; commercial and hotel '
     'work; and the trades owners otherwise chase separately — electrical, plumbing, air conditioning, carpentry, '
     'metalwork, waterproofing, pools and finishes. Geographically: Cancun to Tulum, plus Cozumel and Isla Mujeres. '
     'Outside that corridor we decline, because a crew three hours from base is not supervised properly.')
 + sec('What to ask any builder before signing',
     'A line-item budget rather than one number. Current DRO registration for whoever signs the project. Certificates of '
     'civil liability and workers\' cover, in date. A project in progress to visit, which tells you more than a finished '
     'one. And the change-order procedure in writing, because that is where budgets lose control.'),

'services/permits.html':
 sec('The correct order of the file',
     'Land-use certificate first: if the lot does not permit what you want, no design fixes it and everything else is '
     'wasted. Then alignment and official number, services feasibility, the project signed by a DRO, and with those, the '
     'construction licence. In parallel where it applies, the environmental file — which is what actually sets the '
     'calendar in Tulum, Puerto Morelos and near protected areas.')
 + sec('Why files get returned',
     'Rarely because the authority is slow — because the file arrives incomplete. Drawings that do not match the '
     'land-use certificate, density or height beyond what is permitted, wastewater unresolved, DRO documentation arriving '
     'after everything else, or a declared area that does not match the survey. Each return restarts the clock, and it is '
     'the difference between three weeks and three months.')
 + sec('What we control and what we do not',
     'We assemble the file, engage the DRO, submit, follow up and answer requirements. We do not control resolution times '
     'or environmental criteria, and we tell you realistic ranges at the start rather than an optimistic date that '
     'becomes a construction problem three months later.'),

'blog/guest-house-casita-rental-income-riviera-maya.html':
 sec('Check density before you design anything',
     'The land-use certificate states how many dwellings the lot permits, along with ground coverage and floor area '
     'limits. A casita as a genuinely separate dwelling with its own kitchen may or may not be allowed, and inside a '
     'gated development the internal rules frequently prohibit a second dwelling regardless of what the municipality '
     'permits. Verify both before spending money on drawings — this is where casita projects die.')
 + sec('Why the cost per m² is lower',
     'The expensive parts of a house are kitchens, bathrooms, services and site work. A casita shares the site, the '
     'connections and often the pool, so the marginal cost of adding 40 to 60 m² is far lower than building the same '
     'area standalone. That is what makes it the best-value expansion on most lots.')
 + sec('The honest arithmetic of renting it',
     'The return on the increment is usually better than on the main house because the marginal build cost is low. What '
     'it costs you is privacy and management: guests on your lot, cleaning turnovers, and compliance — separate access, '
     'safety, and whatever registration and taxation apply locally. Decide whether you want that before building, not '
     'after the first booking.')
 + sec('Costs 2026', 'Built alongside an existing house that already has connections.')
 + tbl(['Size', 'What it gives you', 'Cost'],
       [['Studio, 35 – 45 m²', 'Sleeping area, bathroom, kitchenette', '$700,000 – $1,300,000 MXN'],
        ['One-bedroom, 55 – 70 m²', 'Separate bedroom, full kitchen', '$1,100,000 – $2,000,000 MXN'],
        ['Furnishing package', 'Rental-ready', '$120,000 – $300,000 MXN']]),

'construction-company-akumal/index.html':
 sec('Building in Akumal: what the authority looks at first',
     'Akumal sits in the municipality of Tulum, beside a bay of high environmental value and above cenote systems '
     'inland. Before the design, the authority looks at water: what happens to stormwater, how wastewater is treated, '
     'and how far all of it sits from a water body. A project that resolves this at concept stage moves; one that leaves '
     'it to the end is returned.')
 + sec('House to live in, or villa to rent',
     'They are not built the same way even at identical size. A rental villa needs more bathrooms, services sized for '
     'intensive use, finishes that survive guest rotation, a pool with higher-capacity equipment and provision for '
     'frequent maintenance. Decide before the executive project — changing it later means reopening services already '
     'buried.')
 + sec('Logistics here are thinner than in Playa or Tulum centre',
     'Akumal does not have the supplier depth of the larger towns. We bring our own crew and schedule materials in '
     'stages rather than relying on last-minute local purchases. That is the difference between a project that advances '
     'every week and one that stops for three days waiting for a truck nobody here has in stock.'),

'blog/construction-permits-akumal.html':
 sec('Akumal inherits Tulum\'s environmental rigour',
     'Same municipality, and the proximity to the bay and to cenote systems means the environmental component is '
     'examined more closely than in Tulum centre. Spill containment, separation of stormwater drainage and treatment of '
     'wastewater are the core of the file rather than an annex, and that file — not the municipal licence — is what sets '
     'the start date.')
 + sec('What has to be resolved before the design is fixed',
     'Land use and density for the lot. Whether any part of it touches a protected area or federal zone. Where '
     'wastewater will be treated and where treated effluent goes. How rainwater is captured and managed. And a soils '
     'study, because on this stretch cavities and old fill are common enough to change a foundation entirely.')
 + sec('Realistic timelines', 'Assuming a complete file. An incomplete one restarts the clock rather than pausing it.')
 + tbl(['Stage', 'Typical time', 'Note'],
       [['Land use certificate', '1 – 3 weeks', 'Before any design'],
        ['Environmental file', 'Months where required', 'Sets the whole calendar'],
        ['Construction licence with DRO', '3 – 10 weeks', 'After the rest of the package'],
        ['Start on site', 'Only with the licence', 'Starting without it is expensive']]),

'blog/retirement-home-construction-mexico.html':
 sec('Design for the person you will be in twenty years',
     'Single-level living, or at minimum a ground-floor bedroom and full bathroom. Doorways at 90 cm clear. A shower '
     'without a step, with space to turn. No isolated single steps anywhere, indoors or at the entrance. Corridors wide '
     'enough for a walker. And a lift shaft left as a closet if the house has two levels — building the shaft costs '
     'little now and retrofitting one means cutting slabs later.')
 + sec('What matters more than the layout: running costs and heat',
     'A retirement budget is fixed, and the electricity bill here is not. Orientation, cross ventilation, solar control '
     'glazing, insulation and correctly sized air conditioning decide whether the house costs a modest amount to keep '
     'comfortable or a punishing one. Solar panels change that arithmetic further. These are construction decisions, and '
     'they cannot be added afterwards for the same money.')
 + sec('Practical questions to settle before building',
     'Distance to a hospital you would actually use, and to an international airport for family visits. Whether the '
     'community has year-round residents or empties in low season. Health cover decided in advance. And who maintains '
     'the property if you travel for months — in this climate an unattended house degrades quickly.'),

'blog/cost-to-build-house-aldea-zama-tulum.html':
 sec('Aldea Zamá: what the location adds to the cost',
     'A master-planned area with design guidelines, so the project passes a review before the municipality sees it — '
     'materials, heights, setbacks and construction hours are constrained. Add Tulum\'s environmental rigour, karst '
     'ground where a cavity changes a foundation, and demand for skilled trades competing with hotel construction. None '
     'of that is a reason to avoid it; all of it belongs in the budget from the start.')
 + sec('What the price per m² leaves out',
     'Land, architectural and executive project at 4% to 8% of construction, permits and DRO, environmental file, soils '
     'study, connections, furniture, landscaping and the pool. Between the construction line and the total outlay there '
     'is usually 25% to 40%, and that gap is where first-time budgets break.')
 + sec('Cost bands 2026', 'Per built square metre in Aldea Zamá, excluding land, project fees and permits.')
 + tbl(['Level', 'What it means', 'Cost per m²'],
       [['Mid-range', 'Good finishes, small pool', '$19,000 – $26,000 MXN'],
        ['Premium', 'Imported materials, large pool', '$27,000 – $38,000 MXN'],
        ['Design-led villa', 'Bespoke joinery, feature materials', 'From $38,000 MXN']]),

'topographic-survey-plans-riviera-maya/index.html':
 sec('What the survey delivers',
     'The real dimensions of the polygon and its boundaries, contour lines and level differences, the position of '
     'existing structures, significant trees, wells and cenotes, plus references and coordinates. With that, the '
     'architect designs on the land that exists rather than on the one described in the deed — and in this region those '
     'two do not always agree.')
 + sec('Why it belongs before the purchase',
     'Deeded area and actual area differ more often than buyers expect, boundaries are sometimes encroached, and a level '
     'difference you cannot see while walking a lot can mean hundreds of cubic metres of fill or a full retaining wall. '
     'All of that changes what the land is worth paying for.')
 + sec('How it connects to the project and the permit',
     'The survey feeds the architectural project — founding levels, platforms, access — and the stormwater design, which '
     'matters more here than it appears. Several municipalities also require a topographic plan within the licence file, '
     'and one produced carelessly gets the file returned.'),

# ---------------------------------------------------------------------- French
'blog-fr/guide-construction-palapa.html':
 sec('Durée de vie réelle et ce qui la détermine',
     'Une couverture en huano bien posée tient généralement de 8 à 15 ans avant remplacement, et l\'écart est large à '
     'cause de ce qui l\'entoure. L\'ombre permanente et l\'humidité qui ne sèche jamais la raccourcissent nettement : '
     'une palapa sous les arbres se dégrade bien avant une palapa en plein soleil. La ventilation par-dessous prolonge '
     'sa vie, tout comme une pente prononcée et un recouvrement correct. La charpente en bois dur survit à plusieurs '
     'cycles de couverture, et c\'est pourquoi refaire le toit coûte une fraction du prix initial.')
 + sec('Traitement ignifuge, assurance et autorisations',
     'Le huano peut être traité avec un retardateur de flamme, et pour un bien locatif ou commercial c\'est en général '
     'obligatoire : de nombreux assureurs l\'exigent, certaines municipalités aussi. Appliqué pendant la construction, '
     'il coûte bien moins cher qu\'après. Vérifiez la hauteur et l\'implantation autorisées par votre municipalité ou '
     'votre lotissement, et prévenez votre assureur avant de construire, pas après un sinistre.')
 + sec('L\'entretien qui compte vraiment',
     'Contrôle annuel des ligatures et des appuis, nettoyage des noues encombrées de feuilles, élagage des branches qui '
     'maintiennent la toiture à l\'ombre en permanence, et réparation ponctuelle des zones abîmées avant que l\'eau '
     'n\'atteigne la charpente. Une palapa entretenue atteint le haut de sa fourchette de durée de vie ; une palapa '
     'négligée, le bas.')
 + sec('Coûts 2026', 'Par m² couvert dans la Riviera Maya, charpente en bois dur et couverture en huano.')
 + tbl(['Poste', 'Détail', 'Coût 2026 par m²'],
       [['Palapa neuve', 'Charpente bois dur et huano', '$4,000 – $9,000 MXN'],
        ['Charpente haut de gamme', 'Chicozapote, assemblages apparents', '$7,000 – $12,000 MXN'],
        ['Réfection de la couverture', 'Charpente conservée', '$1,500 – $3,500 MXN'],
        ['Traitement ignifuge', 'Appliqué en construction', '+$250 – $600 MXN']]),

'blog-fr/fenetres-portes-climat-tropical.html':
 sec('La série du profil compte autant que le vitrage',
     'Une série légère avec verre trempé se comporte très différemment d\'une série structurelle avec le même verre : '
     'l\'étanchéité, les joints et la tenue au vent sur les grandes baies changent complètement. Sur une façade exposée '
     'et pour des coulissants de grand format, c\'est la série qui empêche l\'eau d\'entrer lors d\'une pluie avec vent '
     'de travers.')
 + sec('Le verre : contrôle solaire avant tout',
     'Sous cette latitude, le verre à contrôle solaire réduit la charge thermique que la climatisation paierait toute '
     'l\'année ; c\'est le premier poste à spécifier sur les façades ouest et sud. Double vitrage lorsque le bruit '
     'compte. Verre feuilleté anti-impact en zone côtière exposée : c\'est la seule protection qui fonctionne sans que '
     'quelqu\'un doive la fermer avant l\'ouragan.')
 + sec('Ce qui fuit, ce n\'est pas le vitrage, c\'est la jonction',
     'La plupart des infiltrations par une fenêtre viennent du pourtour : calfeutrement insuffisant contre le mur, '
     'absence de larmier, appui sans pente. Un excellent produit mal posé fuit autant qu\'un mauvais, et la tache '
     'apparaît à l\'intérieur après la première pluie accompagnée de vent.')
 + sec('Prix 2026', 'Par m² de baie, posé, dans la Riviera Maya.')
 + tbl(['Type', 'Usage', 'Prix par m²'],
       [['Série légère, verre clair', 'Petites baies protégées', '$1,800 – $3,000 MXN'],
        ['Série intermédiaire, trempé', 'Standard résidentiel', '$3,000 – $5,000 MXN'],
        ['Série structurelle, contrôle solaire', 'Grandes baies exposées', '$5,000 – $9,000 MXN'],
        ['Feuilleté anti-impact', 'Côte exposée', '$8,000 – $15,000 MXN']]),

'services/prestations.html':
 sec('Comment nous travaillons',
     'Prix ferme sur un devis détaillé par poste, avec quantités et prix unitaires : le montant que vous signez est '
     'celui que vous payez, sauf changement de programme. Paiements liés à un avancement vérifiable et non à des dates. '
     'Avenants chiffrés et signés avant exécution. Rapport hebdomadaire avec photos datées, car la plupart de nos '
     'clients ne vivent pas au Mexique.')
 + sec('Ce que nous couvrons, et où nous nous arrêtons',
     'Construction neuve, villas et petits ensembles ; rénovation complète ou partielle ; travaux commerciaux et '
     'hôteliers ; et les corps d\'état que le propriétaire finit sinon par gérer séparément — électricité, plomberie, '
     'climatisation, menuiserie, ferronnerie, étanchéité, piscines et finitions. Géographiquement : de Cancún à Tulum, '
     'plus Cozumel et Isla Mujeres. Au-delà, nous déclinons.')
 + sec('Ce qu\'il faut demander à tout constructeur',
     'Un devis par poste et non un chiffre global. L\'enregistrement en cours de validité du DRO qui signera le projet. '
     'Les attestations de responsabilité civile et de couverture des ouvriers. Un chantier en cours à visiter, plus '
     'parlant qu\'une maison terminée. Et la procédure d\'avenants par écrit, car c\'est là que les budgets dérapent.'),

'blog-fr/construction-a-distance-mexique.html':
 sec('Les cinq moments qui ne se revoient pas',
     'Implantation et niveaux avant terrassement. Ferraillage des fondations avant coulage. Ferraillage de dalle, '
     'réseaux noyés et essais de pression avant coulage. Étanchéité avant recouvrement. Électricité et plomberie avant '
     'fermeture des cloisons. Chacun dure quelques heures et détermine la maison. Tout le reste peut être inspecté plus '
     'tard ; ceux-là, non, sans casser quelque chose.')
 + sec('Ce qu\'il faut exiger dans les comptes rendus',
     'Rapport écrit hebdomadaire avec photos datées de chaque étape avant fermeture, avancement comparé au planning, '
     'résultats des essais de laboratoire, liste d\'observations avec responsable et échéance, et registre des avenants. '
     'Des photos éparses envoyées par messagerie, sans date ni contexte, ne sont pas un compte rendu : c\'est une '
     'réassurance, et c\'est précisément ce qu\'un chantier en difficulté produit le plus.')
 + sec('Structurer les paiements pour se protéger',
     'Paiements adossés à des jalons vérifiables — fondations terminées, structure et dalles, réseaux fermés, finitions, '
     'réception — et non à des dates. L\'acompte s\'amortit proportionnellement sur chaque situation plutôt que de '
     'rester dû jusqu\'à la fin. Retenue de garantie jusqu\'à levée des réserves. Ce seul choix protège davantage un '
     'propriétaire absent que n\'importe quelle surveillance.'),

'calculateur/index.html':
 sec('Comment cette estimation est construite',
     'Le chiffre provient du coût au mètre carré construit selon le niveau de finition choisi, appliqué à la surface '
     'saisie. C\'est la base sur laquelle nous ouvrons une discussion avec un client, et elle suffit à savoir si le '
     'projet entre dans votre budget. Ce n\'est pas un devis : un devis suppose un projet, car les mêmes 200 m² peuvent '
     'varier de 30% selon la géométrie, les portées, le sol et la part d\'extérieur couvert.')
 + sec('Ce qui est inclus et ce qui ne l\'est pas',
     'Inclus : la construction de la maison au niveau choisi — structure, enveloppe, réseaux, finitions et extérieurs de '
     'base. Non inclus, et chacun bien réel : le terrain ; le projet architectural et d\'exécution, de 4% à 8% du coût '
     'des travaux ; permis, DRO et dossier environnemental le cas échéant ; l\'étude de sol ; les raccordements ; le '
     'mobilier ; le paysagisme ; et la piscine, à partir d\'environ 180 000 MXN pour un petit bassin.')
 + sec('Pourquoi votre chiffre réel peut s\'écarter',
     'À la hausse : cavités ou remblai dans le calcaire, géométrie complexe, grandes portées, finitions importées, accès '
     'difficile, logistique insulaire. À la baisse : volumétrie simple, plain-pied, bonnes finitions locales, et un '
     'programme figé avant le coulage de la dalle. Le poste qui fait le plus varier le total est la fondation, d\'où '
     'l\'étude de sol avant tout chiffrage ferme.'),

'blog-fr/construire-pres-cenote-riviera-maya.html':
 sec('La distance n\'est pas toute la question',
     'La première question de chacun porte sur le recul par rapport au cénote, et ce n\'est que le début. Ce que '
     'l\'autorité évalue, c\'est si quoi que ce soit venant de votre terrain peut atteindre l\'eau : ruissellement '
     'pluvial, eaux usées, déversements, sédiments de chantier. Une maison éloignée mais rejetant sans traitement est un '
     'dossier plus mauvais qu\'une maison plus proche qui traite et contient tout. On conçoit l\'eau avant la maison.')
 + sec('Ce qui est exigé en pratique',
     'Traitement des eaux usées sur la parcelle — biodigesteur ou station compacte, jamais d\'infiltration sans '
     'traitement. Eaux pluviales captées et conduites, pas dirigées vers le cénote. Rétention en cas de déversement là '
     'où circulent véhicules et engins. Contrôle des sédiments pendant le chantier, phase qui fait le plus de dégâts et '
     'reçoit le moins d\'attention. Et la documentation de tout cela dans le dossier environnemental.')
 + sec('Vivre à côté, honnêtement',
     'Un cénote sur ou à côté de votre terrain est un vrai atout et une vraie responsabilité. Il contraint où vous '
     'pouvez bâtir, ce que vous pouvez rejeter, comment éclairer la nuit et ce que vous pouvez planter. Ceux qui '
     'acceptent ces contraintes comme le prix du privilège s\'en sortent bien ; ceux qui cherchent le minimum '
     'réglementaire finissent souvent dans les statistiques de sanction.'),

'blog-fr/construction-piscine-riviera-maya.html':
 sec('Ce qui détermine réellement le prix',
     'Trois choses : le système constructif (béton armé projeté ou coulé, ou coque préfabriquée), l\'équipement (pompe, '
     'filtration, traitement, chauffage) et la finition (carrelage, enduit, pierre ou chukum). S\'y ajoute ce que '
     'personne ne chiffre au départ : l\'excavation dans la roche calcaire, l\'hydraulique, l\'éclairage, et le génie '
     'civil des plages et margelles.')
 + sec('Ce qui est inclus et ce qui ne l\'est pas',
     'Inclus : excavation, structure, étanchéité, hydraulique, filtration, finition intérieure et mise en service. '
     'Rarement inclus : chauffage ou pompe à chaleur, électrolyse au sel, éclairage architectural, couverture, cascades, '
     'terrasse et paysagisme. Demandez le détail par poste, exactement comme pour la maison.')
 + sec('L\'entretien, le coût qu\'on oublie',
     'Sous ce climat, une piscine consomme produits, électricité de pompage et heures de nettoyage toute l\'année : en '
     'pratique entre 1 500 et 4 000 MXN par mois pour une piscine familiale avec entretien confié, plus la '
     'consommation électrique. L\'électrolyse au sel réduit les produits mais exige plus de soin sur les équipements.')
 + sec('Prix 2026', 'Ouvrage terminé, hors paysagisme, dans la Riviera Maya.')
 + tbl(['Type', 'Dimensions typiques', 'Coût 2026'],
       [['Petit bassin', '3×2 à 4×2 m', '$180,000 – $350,000 MXN'],
        ['Piscine familiale', '6×3 à 8×4 m', '$380,000 – $750,000 MXN'],
        ['Débordement', '8×4 m avec miroir', '$700,000 – $1,300,000 MXN']]),

'blog-fr/piscines-riviera-maya-types-couts.html':
 sec('Béton projeté, béton coulé ou coque',
     'Le béton projeté permet toutes les formes et convient aux sols irréguliers, ce qui est fréquent sur calcaire '
     'fracturé. Le béton coulé donne des géométries simples et régulières à un coût maîtrisé. La coque préfabriquée est '
     'rapide, mais l\'économie est moindre qu\'on ne l\'imagine ici : il faut de toute façon excaver, préparer le fond, '
     'raccorder et traiter les abords, et en terrain rocheux l\'excavation reste le poste lourd.')
 + sec('Finitions et ce qu\'elles supportent',
     'Le carrelage résiste bien et se répare pièce par pièce. L\'enduit coûte moins cher et se rénove périodiquement. Le '
     'chukum donne l\'aspect régional recherché, avec sa propre exigence d\'exécution et d\'entretien. La pierre demande '
     'un traitement adapté au chlore ou au sel. Dans tous les cas, prévoyez une finition antidérapante sur les plages : '
     'sous les pluies d\'ici, une margelle polie est un accident en attente.')
 + sec('Équipement : où il vaut la peine de payer plus',
     'Une pompe à vitesse variable consomme nettement moins qu\'une pompe classique sur une année entière. Un système de '
     'filtration correctement dimensionné évite l\'eau trouble en pleine saison. Et l\'accès de maintenance au local '
     'technique, souvent négligé au dessin, fait la différence entre un entretien de routine et un chantier à chaque '
     'panne.'),

'blog-fr/cout-de-la-vie-pendant-construction-mexique.html':
 sec('Le poste qui surprend : l\'électricité',
     'Les tarifs de la CFE sont progressifs par tranches, et franchir la tranche haute change la facture brutalement, '
     'pas graduellement. Une maison climatisée pendant l\'été caribéen, avec une pompe de piscine, vit exactement à '
     'cette limite. C\'est la plus grande variable d\'un budget domestique ici, et celle que les décisions de chantier '
     'améliorent le plus : orientation, isolation, verre à contrôle solaire, équipements bien dimensionnés, solaire.')
 + sec('Se loger pendant les travaux',
     'La location saisonnière coûte beaucoup plus cher en haute saison qu\'en basse ; un bail de longue durée revient '
     'nettement moins cher si votre chantier dure sept à onze mois, ce qui est la norme. Beaucoup de nos clients '
     'préfèrent suivre le chantier à distance et venir aux étapes clés — c\'est souvent le calcul le plus rationnel.')
 + sec('Ce qu\'il faut prévoir mois par mois',
     'Logement, électricité et eau, transport (une voiture est quasi indispensable hors du centre), assurance santé, '
     'internet, et une réserve pour les allers-retours si vous ne restez pas sur place. Additionner ces postes sur la '
     'durée réelle du chantier change parfois la décision entre construire et acheter.'),

'constructeur-cancun/index.html':
 sec('Cancún n\'est pas un seul marché',
     'La zone hôtelière impose des créneaux d\'accès étroits, des règles de bruit strictes et souvent une interdiction '
     'de travaux en haute saison : le planning se construit autour de l\'immeuble, pas autour des corps d\'état. Puerto '
     'Cancún et les développements récents ont des comités de conception attentifs à tout ce qui se voit de l\'extérieur. '
     'Cumbres et l\'ouest concentrent la construction résidentielle neuve, avec la circulation et l\'accès comme '
     'contrainte principale.')
 + sec('Le règlement du lotissement prime souvent sur la municipalité',
     'Reculs plus importants, hauteur inférieure, matériaux et couleurs imposés, horaires de chantier, dépôt de garantie '
     'et délai maximal de construction. Tout cela vous est opposable indépendamment de ce qu\'autorise Benito Juárez, et '
     'se vérifie avant la conception plutôt qu\'après l\'accord municipal.')
 + sec('Coûts 2026', 'Par m² construit à Cancún, hors terrain, honoraires et permis.')
 + tbl(['Niveau', 'Ce que cela implique', 'Coût par m²'],
       [['Économique', 'Finitions de base, sans piscine', '$12,000 – $16,000 MXN'],
        ['Milieu de gamme', 'Bonnes finitions, petite piscine', '$17,000 – $24,000 MXN'],
        ['Premium', 'Matériaux importés, grande piscine', '$25,000 – $35,000 MXN']]),

# ---------------------------------------------------------------------- German
'services/dienstleistungen.html':
 sec('Wie wir arbeiten',
     'Festpreis auf Basis eines Leistungsverzeichnisses mit Mengen und Einheitspreisen: Was Sie unterschreiben, zahlen '
     'Sie — sofern sich der Umfang nicht ändert. Zahlungen an überprüfbaren Bautenstand gekoppelt, nicht an '
     'Kalenderdaten. Nachträge werden vor Ausführung bepreist und unterschrieben. Wöchentlicher Bericht mit datierten '
     'Fotos, weil die meisten unserer Kunden nicht in Mexiko leben.')
 + sec('Was wir übernehmen — und wo wir aufhören',
     'Neubau von Häusern und Villen, kleine Anlagen; Komplett- und Teilsanierung; Gewerbe- und Hotelbau; sowie die '
     'Gewerke, die Eigentümer sonst einzeln koordinieren müssen — Elektro, Sanitär, Klima, Schreinerei, Metallbau, '
     'Abdichtung, Pools und Ausbau. Geografisch: von Cancún bis Tulum, dazu Cozumel und Isla Mujeres. Darüber hinaus '
     'sagen wir ab.')
 + sec('Was Sie jedem Bauunternehmen abverlangen sollten',
     'Ein Leistungsverzeichnis statt einer Pauschalsumme. Die gültige Registrierung des DRO, der das Projekt '
     'unterschreibt. Nachweise über Haftpflicht- und Arbeiterversicherung. Eine laufende Baustelle zum Besichtigen — sie '
     'sagt mehr als ein fertiges Haus. Und das Nachtragsverfahren schriftlich, denn dort geraten Budgets außer Kontrolle.'),

'services/schreinerei.html':
 sec('Welche Hölzer dieses Klima überstehen',
     'Tzalam, Chechén und Chicozapote sind dichte regionale Harthölzer mit sehr gutem Verhalten im Freien. Kesseldruck'
     'imprägniertes Kiefernholz ist die günstige Option, brauchbar wenn die Imprägnierung wirklich eindringt und nicht '
     'nur oberflächlich aufgetragen wurde. Unbehandeltes Weichholz im Außenbereich bestraft dieses Klima innerhalb '
     'weniger Saisons — zwischen Feuchtigkeit und Termiten.')
 + sec('Küchen und Schränke, die Feuchtigkeit standhalten',
     'Der Korpus entscheidet über die Lebensdauer. Spanplatte quillt auf und erholt sich nicht; Marine-Sperrholz oder '
     'Massivholz schon. Beschläge aus Edelstahl oder hochwertig beschichtet, weil gewöhnliche Ware hier festgeht. Und '
     'Hinterlüftung: einen Schrank dicht an die Außenwand zu setzen ist der übliche Startpunkt für Schimmel in einer '
     'täglich geputzten Küche.')
 + sec('Preise 2026', 'Gefertigt und montiert in der Riviera Maya. Das Material bewegt den Preis stärker als die '
       'Komplexität.')
 + tbl(['Position', 'Material', 'Preis 2026'],
       [['Küche, laufender Meter', 'Marine-Sperrholz, gute Beschläge', '$8,000 – $18,000 MXN/m'],
        ['Schrank, laufender Meter', 'Marine-Sperrholz', '$6,000 – $13,000 MXN/m'],
        ['Innentür', 'Massiv oder furniert', '$6,000 – $16,000 MXN'],
        ['Deck aus Hartholz', 'Hinterlüftete Unterkonstruktion', '$2,500 – $4,200 MXN/m²']]),

'blog-de/casita-gaestehaus-mieteinnahmen-riviera-maya.html':
 sec('Zuerst die Dichte prüfen, dann entwerfen',
     'Die Nutzungsbescheinigung legt fest, wie viele Wohneinheiten das Grundstück zulässt, dazu Grundflächen- und '
     'Geschossflächenzahl. Eine Casita als eigenständige Wohnung mit eigener Küche ist nicht automatisch erlaubt, und '
     'innerhalb einer geschlossenen Wohnanlage untersagt die interne Ordnung eine zweite Einheit häufig unabhängig von '
     'der kommunalen Regelung. Beides klären, bevor Geld in Pläne fließt.')
 + sec('Warum der Quadratmeterpreis niedriger liegt',
     'Teuer an einem Haus sind Küche, Bäder, Haustechnik und Erschließung. Eine Casita teilt sich Grundstück, Anschlüsse '
     'und oft den Pool mit dem Haupthaus — die Grenzkosten für 40 bis 60 m² liegen daher deutlich unter denen eines '
     'freistehenden Baus gleicher Fläche. Das macht sie auf den meisten Grundstücken zur wirtschaftlichsten Erweiterung.')
 + sec('Vermieten: die ehrliche Rechnung',
     'Die Rendite auf den Zubau ist meist besser als auf das Haupthaus, weil die Grenzkosten niedrig sind. Der Preis '
     'dafür ist Privatsphäre und Verwaltung: Gäste auf Ihrem Grundstück, Reinigungswechsel, und die Pflichten — '
     'separater Zugang, Sicherheit, Registrierung und Besteuerung. Diese Entscheidung gehört vor den Bau, nicht nach der '
     'ersten Buchung.'),

'blog-de/pools-riviera-maya-kosten.html':
 sec('Was den Preis wirklich bestimmt',
     'Drei Dinge: die Bauweise (Spritzbeton oder Ortbeton, alternativ Fertigbecken), die Technik (Pumpe, Filter, '
     'Wasseraufbereitung, Heizung) und die Oberfläche (Fliese, Putz, Naturstein oder Chukum). Dazu kommt, was anfangs '
     'kaum jemand kalkuliert: Aushub im Kalkstein, Hydraulik, Beleuchtung sowie der Rohbau von Umgang und Beckenrand.')
 + sec('Was enthalten ist und was nicht',
     'Enthalten: Aushub, Struktur, Abdichtung, Hydraulik, Filtertechnik, Innenausbau und Inbetriebnahme. Selten '
     'enthalten: Heizung oder Wärmepumpe, Salzelektrolyse, Architekturbeleuchtung, Abdeckung, Wasserfälle, Deck und '
     'Bepflanzung. Verlangen Sie die Aufschlüsselung nach Positionen, genau wie beim Haus.')
 + sec('Unterhalt — der Posten, den man vergisst',
     'In diesem Klima verbraucht ein Pool ganzjährig Chemie, Pumpenstrom und Reinigungsstunden: praktisch 1.500 bis '
     '4.000 MXN monatlich für einen Familienpool mit Servicevertrag, plus Stromkosten. Salzelektrolyse reduziert die '
     'Chemie, verlangt aber mehr Sorgfalt bei der Technik.')
 + sec('Preise 2026', 'Fertiges Becken ohne Bepflanzung, Riviera Maya.')
 + tbl(['Typ', 'Typische Maße', 'Kosten 2026'],
       [['Kompaktbecken', '3×2 bis 4×2 m', '$180,000 – $350,000 MXN'],
        ['Familienpool', '6×3 bis 8×4 m', '$380,000 – $750,000 MXN'],
        ['Überlaufbecken', '8×4 m mit Spiegel', '$700,000 – $1,300,000 MXN']]),

'blog-de/baukosten-playa-del-carmen-2026.html':
 sec('Der Unterschied zwischen Baukosten und tatsächlicher Ausgabe',
     'Der Quadratmeterpreis deckt den Bau des Hauses. Nicht enthalten sind Grundstück, Architektur- und '
     'Ausführungsplanung (4% bis 8% der Bausumme), Baugenehmigung und DRO, Baugrundgutachten, Hausanschlüsse, '
     'Einrichtung, Außenanlagen und Pool. Zwischen Baukostenlinie und Gesamtausgabe liegen üblicherweise 25% bis 40% — '
     'genau dort scheitern Budgets von Erstbauherren.')
 + sec('Wie sich die Kosten verteilen',
     'Ungefähre Anteile für ein Haus mittlerer Ausstattung. Sie genügen, um ein unausgewogenes Angebot auf einen Blick '
     'zu erkennen, bevor man ins Detail geht.')
 + tbl(['Position', 'Anteil an der Bausumme', 'Hinweis'],
       [['Vorarbeiten und Gründung', '12% – 18%', 'Höher bei Hohlräumen im Kalkstein'],
        ['Rohbau', '25% – 32%', 'Beton, Stahl, Wände, Decken'],
        ['Haustechnik', '14% – 18%', 'Inklusive Zisterne und Pumpe'],
        ['Ausbau und Oberflächen', '22% – 30%', 'Die variabelste Position'],
        ['Schreinerei und Metallbau', '8% – 12%', 'Küche, Schränke, Fenster'],
        ['Außenanlagen', '4% – 8%', 'Wege, Garten, Übergabe']])
 + sec('Wo sich sparen lässt und wo nicht',
     'Sparen lässt sich mit einfacher Geometrie, Eingeschossigkeit, guten lokalen Materialien, einem kleineren aber gut '
     'ausgestatteten Pool und einer vor dem Deckenguss festgelegten Ausstattung. Nicht sparen sollte man bei '
     'Baugrundgutachten, Gründung, Abdichtung, verdeckter Haustechnik und Abwasserbehandlung — das verschiebt die '
     'Ausgabe nur und vervielfacht sie.'),

'blog-de/lebenshaltungskosten-bauen-mexiko.html':
 sec('Der Posten, der alle überrascht: Strom',
     'Die CFE-Tarife sind gestaffelt, und der Sprung in die hohe Verbrauchsstufe verändert die Rechnung sprunghaft, '
     'nicht allmählich. Ein Haus mit Klimaanlage im karibischen Sommer plus Poolpumpe bewegt sich genau an dieser '
     'Grenze. Es ist die größte Variable im Haushaltsbudget hier — und diejenige, die Bauentscheidungen am stärksten '
     'verbessern: Ausrichtung, Dämmung, Sonnenschutzglas, richtig dimensionierte Geräte, Photovoltaik.')
 + sec('Wohnen während der Bauzeit',
     'Ferienvermietung kostet in der Hochsaison ein Vielfaches der Nebensaison; ein längerfristiger Mietvertrag ist '
     'deutlich günstiger, wenn Ihr Bau sieben bis elf Monate dauert, was die Regel ist. Viele unserer Kunden verfolgen '
     'den Bau aus der Ferne und reisen zu den entscheidenden Etappen an — meist die wirtschaftlichere Rechnung.')
 + sec('Was Sie monatlich einplanen sollten',
     'Unterkunft, Strom und Wasser, Mobilität (außerhalb des fußläufigen Zentrums ist ein Auto praktisch nötig), '
     'Krankenversicherung, Internet und eine Reserve für Flüge, falls Sie nicht durchgehend hier sind. Diese Posten über '
     'die reale Bauzeit summiert verändern manchmal die Entscheidung zwischen Bauen und Kaufen.'),

# ---------------------------------------------------------------------- Russian
'stroitelnaya-kompaniya-cancun/index.html':
 sec('Канкун — это три разных рынка',
     'В отельной зоне узкие окна доступа, строгие нормы по шуму и частый запрет работ в высокий сезон: график строится '
     'вокруг здания, а не вокруг бригад. В Пуэрто-Канкуне и новых посёлках работают комитеты по дизайну, которым важно '
     'всё, что видно снаружи. В Кумбресе и на западе идёт основная новая застройка, и там ограничение — тяжёлый трафик '
     'и подъезд. Одни и те же чертежи дают три разных проекта.')
 + sec('Регламент посёлка обычно строже муниципального',
     'Большие отступы, меньшая высота, обязательная палитра материалов и цветов, часы работ, залог и максимальный срок '
     'строительства. Всё это обязательно к исполнению независимо от того, что разрешает Бенито-Хуарес, и читать это '
     'нужно до проектирования, а не после муниципального согласования.')
 + sec('Стоимость 2026', 'За м² построенной площади в Канкуне, без земли, проекта и разрешений.')
 + tbl(['Уровень', 'Что это значит', 'Стоимость за м²'],
       [['Эконом', 'Базовая отделка, без бассейна', '$12,000 – $16,000 MXN'],
        ['Средний', 'Хорошая отделка, небольшой бассейн', '$17,000 – $24,000 MXN'],
        ['Премиум', 'Импортные материалы, большой бассейн', '$25,000 – $35,000 MXN']]),

'blog-ru/stoimost-zhizni-stroitelstvo-meksika.html':
 sec('Статья, которая удивляет всех: электричество',
     'Тарифы CFE ступенчатые, и переход в верхнюю ступень меняет счёт скачком, а не постепенно. Дом с кондиционерами '
     'карибским летом плюс насос бассейна живёт ровно на этой границе. Это самая крупная переменная в бытовом бюджете '
     'здесь — и та, которую сильнее всего улучшают решения, принятые на стройке: ориентация, утепление, солнцезащитное '
     'стекло, правильно подобранная мощность, солнечные панели.')
 + sec('Где жить, пока идёт стройка',
     'Посуточная аренда в высокий сезон стоит кратно дороже, чем в низкий; долгосрочный договор заметно выгоднее, если '
     'стройка занимает от семи до одиннадцати месяцев — а это норма. Многие наши клиенты ведут стройку удалённо и '
     'прилетают на ключевые этапы; по деньгам это чаще всего самый рациональный вариант.')
 + sec('Что закладывать в месячный бюджет',
     'Жильё, электричество и вода, транспорт (за пределами пешеходного центра машина практически необходима), '
     'медицинская страховка, интернет и резерв на перелёты, если вы здесь не постоянно. Сумма этих статей за реальный '
     'срок стройки иногда меняет решение между «строить» и «купить готовое».'),

# ---------------------------------------------------------------------- Chinese
'blog-zh/airbnb-roi-jisuanqi-tulum-playa.html':
 sec('测算之前先算清真实运营成本',
     '房源总收入和最终到手的钱之间差距很大。管理通常占毛收入的 15% 至 30%，每次入住有保洁费用，'
     '平台佣金在打款前扣除，客人使用期间空调几乎全天运转，电费远高于自住，'
     '再加上泳池与花园维护、补充易耗品和这个气候下不可省略的维修准备金。任何不含这些的收益预测都不是保守，而是错的。')
 + sec('图卢姆的供给已经跑在需求前面',
     '以收益率为卖点销售的小户型公寓，是竞争最激烈的一类产品。当大量几乎一样的房源争夺同一批客人时，'
     '调整首先不体现在房价下跌，而是入住率下降、打折促销，以及管理费吞掉剩余利润。'
     '如果有人用收益率说服您购买，请务必问清楚：这个测算假设的入住率是多少，再去对比同类房源目前的真实表现。')
 + sec('装修与配置要按出租标准做，而不是按自住标准',
     '出租房失败往往败在不起眼的地方：满房时热水不够、空调按自住人数选型、表面材料经不起高频轮换、'
     '座位数少于房源标注的可住人数、没有布草储藏空间。如果计划出租，这些必须写进设计任务书，'
     '事后通过差评发现的代价要高得多。'),

'blog-zh/jianzhu-qijian-shenghuo-feiyong-moxige.html':
 sec('最容易被低估的一项：电费',
     'CFE 电价按阶梯计费，一旦跨入高用电档，账单是跳涨而不是渐涨。加勒比夏季持续开空调、'
     '再加上泳池水泵的住宅，正好处在这条边界上。这是本地家庭预算中波动最大的一项，'
     '也是最能靠施工阶段的决策改善的一项：朝向、保温、遮阳玻璃、空调选型是否合理、以及是否安装光伏。')
 + sec('施工期间住哪里',
     '旺季短租的价格是淡季的数倍；如果工期是七到十一个月（这属于常态），签长期租约要划算得多。'
     '我们不少客户选择远程跟进工程，只在关键节点飞过来——从成本上看，这往往是最理性的方案。')
 + sec('每月需要预留的开支',
     '住宿、水电、交通（在可步行的中心区之外，基本需要一辆车）、医疗保险、网络，'
     '以及若您不常驻本地还需预留往返机票。把这些费用按真实工期累加起来，'
     '有时会改变"自建"还是"买现房"的最终结论。'),

'blog-zh/jinkou-jiaju-cailiao-moxige.html':
 sec('进口之前先确认三件事',
     '第一，总到岸成本：货值之外还有海运、保险、关税、清关服务费和内陆运输，'
     '合计常常远超很多人的预期。第二，时间：定制家具和特定设备的交期加上清关的不确定性，'
     '是导致交房推迟最常见的原因之一。第三，售后：进口设备一旦损坏，本地能否维修、配件从哪里来，'
     '这个问题应该在下单前问清楚，而不是在保修期内才发现。')
 + sec('哪些值得进口，哪些不值得',
     '值得：本地确实买不到的特定设备、成套厨房系统、以及对整体设计至关重要的标志性单品。'
     '不值得：本地能买到同等品质的常规家具、以及任何笨重、易损、价值密度低的物件——'
     '运费会吃掉全部差价。石材和瓷砖通常在本地采购更划算，破损风险也低得多。')
 + sec('这个气候对进口家具的考验',
     '高湿度全年存在，沿海还有盐分。刨花板基材会膨胀且无法恢复，普通五金会锈蚀卡死，'
     '未经处理的软木在户外撑不了几季。进口之前请确认基材、五金材质和面料是否适合湿热海洋环境——'
     '这比品牌本身更能决定它能用多少年。'),
}


def insert(path, block):
    s = open(path, encoding='utf-8').read()
    s = re.sub(re.escape(OPEN) + r'.*?' + re.escape(CLOSE), '', s, flags=re.S)
    payload = OPEN + '\n' + block + CLOSE + '\n'
    m = (re.search(r'\n[ \t]*<h2[^>]*>\s*(Preguntas Frecuentes|Frequently Asked Questions|Häufige Fragen|'
                   r'Questions fréquentes|Часто задаваемые|常见问题|FAQ)', s)
         or re.search(r'\n[ \t]*<div class="cta-section', s)
         or re.search(r'\n[ \t]*<section data-cluster=', s))
    at = (s.rfind('\n', 0, m.start() + 1) + 1) if m else s.rfind('<footer')
    s = s[:at] + payload + s[at:]
    open(path, 'w', encoding='utf-8').write(s)
    return s


def wc(html):
    body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1'):html.index('<footer')])
    return len(re.sub(r'[一-鿿]', '', body).split()) + int(len(re.findall(r'[一-鿿]', body)) / 1.6)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    ok = 0
    for path, block in B.items():
        if not os.path.exists(path):
            print('  missing:', path); continue
        before = wc(open(path, encoding='utf-8').read())
        after = wc(insert(path, block))
        ok += 1
        print('%-56s %4d -> %4d' % (path, before, after))
    print('deepened:', ok)
