#!/usr/bin/env python3
"""Fourth depth pass, batch 1 of 3: the Spanish and English tail (2026-08-15).

18 pages at 1-4 impressions each. Small numbers individually; the point of doing
them is that they are the last thin Spanish and English pages on the site, and a
site where every indexable page says something substantial is a different asset
from one carrying a few hundred stubs.

Blocks are shorter than in the earlier passes because these pages are shorter
topics, not because the standard dropped: each one is specific, priced where
pricing helps, and written to answer the question the title promises.
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
'blog-es/administracion-propiedades-riviera-maya.html':
 sec('Qué debe incluir una administración seria',
     'Visita semanal con reporte fotográfico fechado, no un mensaje diciendo que todo está bien. Coordinación de '
     'alberca, jardín y limpieza. Revisión de drenajes de condensados y de azotea antes de lluvias. Atención de '
     'emergencias con un límite de gasto autorizado por escrito, para que una fuga se repare el mismo día y no cuando '
     'despierte otro huso horario. Y un reporte anual de estado con presupuesto de lo que la propiedad va a necesitar.')
 + sec('Lo que cuesta y cómo se cobra',
     'Se cobra por cuota mensual fija, por porcentaje de la renta cuando incluye gestión de huéspedes, o mixto. '
     'Desconfíe del modelo que cobra comisión sobre reparaciones: incentiva reparar de más. Pida que el proveedor '
     'muestre cotizaciones de terceros para trabajos mayores.')
 + tbl(['Servicio', 'Frecuencia', 'Costo 2026'],
       [['Revisión de propiedad con reporte', 'Semanal', '$1,500 – $3,500 MXN/mes'],
        ['Alberca', 'Semanal', '$1,500 – $4,000 MXN/mes'],
        ['Jardín', 'Semanal o quincenal', '$2,000 – $6,000 MXN/mes'],
        ['Gestión de renta vacacional', 'Por reserva', '15% – 30% del bruto']]),

'blog-es/casa-dos-pisos-riviera-maya.html':
 sec('Cuándo conviene dos plantas y cuándo no',
     'Conviene cuando el terreno es chico y quiere jardín o alberca, cuando busca vistas, o cuando el uso de suelo '
     'limita el COS pero permite altura. No conviene si planea envejecer en la casa sin prever elevador, si el terreno '
     'permite una planta cómoda, o si el presupuesto está justo: dos plantas suman escalera, estructura más exigente y '
     'una instalación hidráulica más larga.')
 + sec('Lo que encarece la segunda planta',
     'Losa de entrepiso con su armado, columnas y trabes dimensionadas para la carga, escalera —de $18,000 a $55,000 '
     'MXN según tipo—, subida de instalaciones, y con frecuencia una cimentación más robusta. En la práctica el metro '
     'cuadrado de planta alta cuesta parecido al de planta baja, pero el proyecto completo sube porque la estructura '
     'trabaja más.')
 + sec('El detalle que casi nadie prevé',
     'Dejar el cubo de un futuro elevador, usado mientras tanto como clóset o alacena. Cuesta poco durante la obra y '
     'evita romper losas después. En una casa de retiro es la diferencia entre quedarse en ella o mudarse.'),

'blog-es/casa-inteligente-automatizacion-riviera-maya.html':
 sec('Qué automatización sí vale la pena aquí',
     'Control de clima por zonas, que es donde está el gasto real; iluminación con escenas y atenuación; portón y '
     'acceso; riego automático sectorizado; cámaras y sensores de apertura; y detección de fuga de agua, que en una '
     'casa que pasa meses sola vale más que cualquier otra cosa de esta lista. Lo demás es comodidad, no ahorro.')
 + sec('Cableado ahora, dispositivos después',
     'Los dispositivos cambian cada pocos años; la canalización no. Deje cableado de red a los puntos clave, espacio en '
     'tablero, alimentación en accesos y previsión de sensores. Con eso puede actualizar tecnología sin volver a abrir '
     'muros, que es exactamente donde se va el presupuesto cuando se automatiza una casa ya terminada.')
 + sec('Internet, respaldo y realidad local',
     'Un sistema que depende de la nube deja de funcionar cuando cae el internet o la luz, y aquí ambas cosas pasan. '
     'Elija equipos que conserven control local, y prevea respaldo eléctrico para el enrutador y para los accesos.'),

'blog-es/casa-pequena-tulum-presupuesto.html':
 sec('Dónde se va el dinero en una casa chica',
     'En una casa de 60 a 90 m² el costo por metro cuadrado sube, no baja: baños y cocina —las partidas más caras por '
     'metro— pesan proporcionalmente más, y los costos fijos de obra, trámite y conexiones se reparten entre menos '
     'superficie. Eso sorprende a quien espera que menos metros signifiquen proporcionalmente menos dinero.')
 + sec('Cómo hacerla sentir grande sin construir más',
     'Techos altos, un solo espacio para estar-comer-cocinar, buena luz natural cruzada, y sobre todo exterior techado: '
     'una terraza bajo palapa o pérgola cuesta una fracción del interior y en este clima se usa todo el año. Esa es la '
     'jugada que más cambia la percepción de tamaño por peso.')
 + sec('Presupuesto realista', 'Obra terminada en Tulum, sin terreno, proyecto ni permisos.')
 + tbl(['Superficie', 'Nivel medio', 'Nivel premium'],
       [['60 m²', '$1,150,000 – $1,550,000 MXN', '$1,650,000 – $2,300,000 MXN'],
        ['90 m²', '$1,700,000 – $2,350,000 MXN', '$2,450,000 – $3,450,000 MXN']]),

'blog-es/casita-renta-ingresos-riviera-maya.html':
 sec('Primero la densidad, después el diseño',
     'La constancia de uso de suelo dice cuántas viviendas admite el predio, además de COS y CUS. Una casita como '
     'vivienda independiente con cocina propia no siempre está permitida, y dentro de un fraccionamiento el reglamento '
     'interno con frecuencia la prohíbe aunque el municipio la permita. Verificar ambas cosas antes de gastar en planos '
     'es lo que separa un proyecto viable de uno muerto.')
 + sec('Por qué el metro cuadrado sale más barato',
     'Lo caro de una casa son cocina, baños, instalaciones y obra exterior. La casita comparte predio, conexiones y a '
     'menudo alberca, así que el costo marginal de sumar 40 a 60 m² es mucho menor que construirlos aislados. Por eso '
     'suele ser la mejor ampliación por peso invertido.')
 + sec('La aritmética honesta de rentarla',
     'El retorno sobre el incremento suele ser mejor que sobre la casa principal. Lo que cuesta es privacidad y '
     'gestión: huéspedes en su terreno, limpiezas entre estancias, y el cumplimiento —acceso separado, seguridad, y el '
     'registro y la tributación que apliquen. Decídalo antes de construir, no después de la primera reserva.'),

'blog-es/diseno-casa-personalizada-playa-del-carmen.html':
 sec('Diseñar para este clima antes que para el catálogo',
     'Orientación que evite el sol poniente en las fachadas de estar, ventilación cruzada real, protección solar en '
     'vanos grandes, aleros generosos para lluvia intensa, y materiales que aguanten sal y humedad. Una casa que ignora '
     'esto se ve idéntica en el render y cuesta el doble de operar durante veinte años.')
 + sec('El programa antes que la planta',
     'Cuántas personas de verdad, con qué frecuencia, y qué pasa cuando llegan visitas. Si va a rentarse parte del año, '
     'eso cambia baños, accesos y almacenamiento desde el primer boceto. Definir el programa con honestidad evita el '
     'error más caro del diseño personalizado: metros que se pagan, se mantienen y no se usan.')
 + sec('Qué esperar del proceso',
     'Anteproyecto, proyecto arquitectónico, proyecto ejecutivo con estructural e instalaciones, y documentación para '
     'trámite firmada por DRO. De 6 a 10 semanas para casa unifamiliar, y entre 4% y 8% del costo de obra. Sin ejecutivo '
     'nadie puede cotizar por partidas ni controlar la obra.'),

'blog-es/diseno-iluminacion-riviera-maya.html':
 sec('Las capas, y por qué una sola no alcanza',
     'General para moverse, de trabajo donde se hace algo, de acento sobre texturas y vegetación, y decorativa cuando la '
     'luminaria se ve. Un proyecto que solo resuelve la general se siente plano y además consume más, porque compensa '
     'con potencia lo que debería resolver con posición.')
 + sec('Temperatura de color y exteriores en costa',
     'Cálida —2700 a 3000 K— en interiores y terrazas; neutra en cocina y trabajo; nunca mezcladas en un mismo espacio. '
     'En exterior costero la luminaria necesita grado de protección real y cuerpo resistente a corrosión: aquí no las '
     'mata la lluvia, las mata la sal que entra por las juntas.')
 + sec('Decidir el control antes de cablear',
     'Un atenuador bien puesto cambia más una sala que dos luminarias extra. Escenas por espacio, sensores en pasillos, '
     'y automatización de fachada y jardín por horario. Agregarlo después implica volver a abrir muros.'),

'blog-es/garajes-estacionamiento-riviera-maya.html':
 sec('Cochera techada, pérgola o descubierto',
     'El sol y la lluvia de esta región castigan pintura, plásticos y tapicería. Una cochera techada protege de verdad; '
     'una pérgola con enredadera es estética y no protege del agua; descubierto es la opción de menor costo y mayor '
     'desgaste. Si el auto es nuevo o va a quedarse meses solo, techarlo sale más barato que repintarlo.')
 + sec('Piso, pendiente y drenaje',
     'Concreto con acabado antiderrapante y pendiente hacia un punto de desagüe, nunca hacia la casa. Con lluvia '
     'intensa un piso plano se convierte en charco permanente y la humedad sube por el muro contiguo. Y si el acceso '
     'baja hacia la propiedad, hace falta rejilla y capacidad de desalojo reales.')
 + sec('Reglamento y número de cajones',
     'Muchos municipios exigen un mínimo de cajones por vivienda para otorgar licencia, y los fraccionamientos suelen '
     'sumar sus propias reglas sobre estacionamiento en vía interna. Se revisa antes del proyecto: resolverlo después '
     'puede costar superficie de jardín.'),

'blog-es/permisos-construccion-puerto-aventuras.html':
 sec('Dos reglamentos, no uno',
     'Puerto Aventuras pertenece a Solidaridad, así que aplican los trámites municipales de Playa del Carmen. Encima '
     'está el reglamento del fraccionamiento: comité que revisa el proyecto, retiros y alturas propios, horarios de '
     'obra, registro de personal y vehículos, depósito y plazo máximo. El comité suele revisar antes que el municipio, '
     'y su visto bueno condiciona todo lo demás.')
 + sec('Accesos sobre carretera federal',
     'Los predios con frente a la 307 requieren resolver acceso, carriles y maniobras con la autoridad correspondiente, '
     'no solo con el municipio. Es de los puntos que más retrasan un expediente cuando se plantea tarde.')
 + sec('Tiempos realistas', 'Suponiendo expediente completo; uno incompleto reinicia el reloj.')
 + tbl(['Etapa', 'Tiempo típico', 'Nota'],
       [['Aprobación del comité', '2 – 6 semanas', 'Antes del trámite municipal'],
        ['Constancia de uso de suelo', '1 – 3 semanas', 'Primero en el municipio'],
        ['Licencia con DRO', '3 – 10 semanas', 'Con registro vigente'],
        ['Terminación de obra', 'Al cierre', 'Necesaria para habitabilidad']]),

'blog-es/plusvalia-inmobiliaria-riviera-maya-2026.html':
 sec('Qué mueve la plusvalía aquí, y qué no',
     'La mueve la infraestructura real —accesos, aeropuerto, servicios, seguridad— y la escasez de producto '
     'diferenciado. No la mueve la promesa de un desarrollo futuro, ni la proyección de rentabilidad de un folleto. '
     'Cuando muchas unidades casi idénticas compiten por el mismo huésped, el ajuste no aparece primero como caída de '
     'precio sino como caída de ocupación.')
 + sec('Dónde el mercado está más delgado',
     'Villas privadas con superficie exterior real, privacidad y alberca compiten en un mercado mucho menos saturado '
     'que los condominios chicos vendidos por rendimiento. Son más difíciles de construir y de replicar en serie, y esa '
     'barrera es justamente lo que protege el valor de lo ya construido.')
 + sec('Cómo evaluar sin autoengaño',
     'Compare contra ocupación real de anuncios equivalentes, no contra la proyección del vendedor. Reste costos '
     'operativos completos: administración 15% a 30% del bruto, limpieza, electricidad con aire acondicionado, alberca, '
     'jardín, seguro y reserva de mantenimiento del 1% al 2% del valor al año.'),

'blog-es/reporte-mercado-construccion-t3-2026.html':
 sec('Cómo leemos el mercado',
     'Con cifras que efectivamente cotizamos y plazos que efectivamente tardaron, no con optimismo. Cuando un dato nos '
     'parece poco sólido lo decimos, en lugar de publicarlo como certeza. Un reporte de mercado hecho por quien vende '
     'el mercado vale poco; este lo escribe quien tiene que cumplir los presupuestos que publica.')
 + sec('Las variables que mueven un presupuesto de obra',
     'Acero y cemento, que arrastran estructura; mano de obra especializada, que compite con la construcción hotelera; '
     'y tiempos de trámite, que cuestan dinero aunque no aparezcan en ninguna partida. En esta región el trámite '
     'ambiental ha sido en los últimos años el factor que más ha movido calendarios.')
 + sec('Qué hacer con esta información',
     'Si va a construir, cierre especificación antes de colar la losa y pida material de entrega larga en cuanto se '
     'apruebe el proyecto. Si está comparando presupuestos, revise que ambos tengan las mismas partidas y cantidades '
     'antes de mirar el total.'),

'blog-es/seguridad-casa-riviera-maya.html':
 sec('Lo que de verdad reduce el riesgo',
     'Iluminación exterior bien distribuida, visibilidad desde la calle en lugar de muros ciegos que esconden, accesos '
     'sólidos con herrajes de calidad, y la impresión de que la casa está habitada: temporizadores, jardín cuidado, '
     'correspondencia recogida. Casi todo lo que funciona es diseño y rutina, no equipo.')
 + sec('Cámaras, sensores y quien responde',
     'Un sistema que graba pero no avisa a nadie sirve después del hecho. Lo útil es detección de apertura y movimiento '
     'con aviso a una persona que puede acudir —vecino, administrador, empresa— y respaldo eléctrico para que no se '
     'caiga con el primer apagón. Si la casa queda sola meses, eso no es opcional.')
 + sec('Cerraduras, ventanas y el punto débil real',
     'La mayoría de los accesos forzados ocurren por ventanas y puertas secundarias, no por la principal. Herrajes '
     'inoxidables que no se traben con la sal, cristal laminado donde importa, y protecciones diseñadas para no parecer '
     'reja son la combinación que funciona sin convertir la casa en una jaula.'),

'blog-es/seguros-garantias-construccion.html':
 sec('Tres coberturas distintas que suelen confundirse',
     'Todo riesgo de construcción, que cubre la obra mientras se ejecuta. Responsabilidad civil del constructor, que '
     'cubre daños a terceros. Y cobertura de trabajadores. Son tres cosas separadas y el contrato debería nombrarlas por '
     'separado, con certificados vigentes que usted pueda ver antes de que empiece la obra.')
 + sec('Garantía de vicios ocultos',
     'Debe estar por escrito: qué cubre, por cuánto tiempo y cómo se reporta. Una "garantía" sin plazo ni alcance no es '
     'una garantía. Y ningún constructor serio garantiza estructura ejecutada por otro sin haberla verificado, lo cual '
     'es relevante si está retomando una obra empezada.')
 + sec('Lo que hace que una reclamación funcione',
     'Fotografías fechadas del avance, resultados de pruebas de laboratorio, bitácora, y acta de entrega con lista de '
     'pendientes. Ese expediente es lo que sostiene una reclamación; sin él, la discusión es palabra contra palabra.'),

'blog-es/techos-impermeabilizacion-riviera-maya.html':
 sec('Por qué aquí la impermeabilización es estructural, no cosmética',
     'Lluvia intensa concentrada, sol directo que degrada membranas y humedad constante. Un sistema que en clima seco '
     'dura una década, aquí puede pedir mantenimiento en la mitad del tiempo. Y la filtración no solo mancha: el agua '
     'que llega al acero de la losa lo corroe, y esa reparación ya no es de pintura.')
 + sec('El detalle, no el producto',
     'La mayoría de las filtraciones aparecen en encuentros: pretiles, bajadas, salidas de tubería, base de domos y '
     'juntas constructivas. Ahí es donde se define si el sistema dura. Un producto premium mal rematado en un pretil '
     'gotea igual que uno barato bien ejecutado.')
 + sec('Mantenimiento y costos', 'Rangos por m² de azotea en la Riviera Maya, incluida preparación de superficie.')
 + tbl(['Sistema', 'Vida útil orientativa', 'Costo por m²'],
       [['Prefabricado asfáltico', '5 – 10 años', '$180 – $350 MXN'],
        ['Acrílico elastomérico', '3 – 7 años', '$120 – $250 MXN'],
        ['Poliuretano', '8 – 15 años', '$300 – $600 MXN'],
        ['Revisión anual antes de lluvias', 'Cada año', 'Mínima y evita lo caro']]),

# ---------------------------------------------------------------------- English
'blog/construction-permits-puerto-aventuras.html':
 sec('Two rulebooks, not one',
     'Puerto Aventuras sits in the municipality of Solidaridad, so the municipal process is the same as Playa del '
     'Carmen. On top of that runs the development\'s own regulation: a design committee, its own setbacks and heights, '
     'working hours, registration of crew and vehicles, a deposit and a maximum construction period. The committee '
     'usually reviews before the municipality does, and its approval conditions everything after it.')
 + sec('Access onto the federal highway',
     'Lots fronting Highway 307 must resolve access, deceleration and manoeuvring with the relevant authority, not only '
     'with the municipality. It is one of the items that most often delays a file when it is raised late.')
 + sec('Realistic timelines', 'Assuming a complete file; an incomplete one restarts the clock.')
 + tbl(['Stage', 'Typical time', 'Note'],
       [['Design committee approval', '2 – 6 weeks', 'Before the municipal process'],
        ['Land use certificate', '1 – 3 weeks', 'First at the municipality'],
        ['Licence with DRO', '3 – 10 weeks', 'Current registration required'],
        ['Completion certificate', 'At closing', 'Needed for occupancy']]),

'blog/cost-to-build-house-corasol.html':
 sec('What Corasol adds to the budget',
     'A master-planned community with design guidelines: the project passes an internal review before the municipality '
     'sees it, and materials, heights, setbacks and construction hours are constrained. Add access control, restricted '
     'working windows and a completion deadline with a deposit. None of that is a reason to avoid it — it is what keeps '
     'the setting intact — but it belongs in the budget and the schedule from the start.')
 + sec('What the per-square-metre figure leaves out',
     'Land, architectural and executive project at 4% to 8%, permits and DRO, soils study, connections, furniture, '
     'landscaping and the pool. Between the construction line and total outlay there is normally 25% to 40%.')
 + sec('Cost bands 2026', 'Per built square metre in Corasol, excluding land, fees and permits.')
 + tbl(['Level', 'What it means', 'Cost per m²'],
       [['Mid-range', 'Good finishes, small pool', '$19,000 – $26,000 MXN'],
        ['Premium', 'Imported materials, large pool', '$27,000 – $38,000 MXN'],
        ['Design-led villa', 'Bespoke joinery, feature materials', 'From $38,000 MXN']]),

'blog/land-prices-playa-del-carmen-tulum-2026.html':
 sec('Price per m² is not what tells you the lot is good',
     'Two lots at the same price can be worth very different amounts, for five reasons you cannot see by walking them: '
     'permitted land use and density, COS and CUS, height limit, whether any part touches a protected area or federal '
     'zone, and what is underneath. Cheap land you cannot build your project on is not cheap.')
 + sec('Ejido versus private title',
     'This distinction has cost foreign buyers more money in Quintana Roo than anything else. Ejido land is communal '
     'and cannot be freely transferred until properly regularised into private title, whatever document you are shown. '
     'Verify it at the public registry first, and treat a price far below market as a reason for more diligence.')
 + sec('What is worth spending before you buy',
     'A topographic survey, because deeded and actual area differ more often than buyers expect. A soils study, because '
     'in fractured limestone foundations change between neighbouring lots. The land-use certificate. And services '
     'feasibility, since extending a power line is the owner\'s cost.'),

'blog/real-estate-appreciation-riviera-maya-2026.html':
 sec('What drives appreciation here, and what does not',
     'Real infrastructure — access, the airport, services, security — and scarcity of differentiated product. Not the '
     'promise of a future development, and not a brochure\'s yield projection. When many near-identical units chase the '
     'same guest, the adjustment shows up first as falling occupancy and discounting rather than as falling prices.')
 + sec('Where the market is thinner',
     'Private villas with real outdoor space, privacy and a pool compete in a far less crowded market than small condos '
     'sold on yield. They are harder to build and harder to replicate at scale, and that barrier is what protects the '
     'value of what already exists.')
 + sec('How to assess it without fooling yourself',
     'Compare against the occupancy comparable listings actually achieve, not the seller\'s projection. Subtract the '
     'full operating cost: management at 15% to 30% of gross, cleaning, electricity with air conditioning running, pool, '
     'garden, insurance, and a maintenance reserve of 1% to 2% of value per year.'),
}


def insert(path, block):
    s = open(path, encoding='utf-8').read()
    s = re.sub(re.escape(OPEN) + r'.*?' + re.escape(CLOSE), '', s, flags=re.S)
    payload = OPEN + '\n' + block + CLOSE + '\n'
    m = (re.search(r'\n[ \t]*<h2[^>]*>\s*(Preguntas Frecuentes|Frequently Asked Questions|FAQ)', s)
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
    n = 0
    for path, block in B.items():
        if not os.path.exists(path):
            print('  missing:', path); continue
        before = wc(open(path, encoding='utf-8').read())
        after = wc(insert(path, block))
        n += 1
        print('%-58s %4d -> %4d' % (path, before, after))
    print('deepened:', n)
