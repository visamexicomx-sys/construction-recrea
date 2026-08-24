#!/usr/bin/env python3
"""Naves industriales / bodegas: one page per city of the service corridor.

The pillar (/naves-industriales-bodegas-riviera-maya/) already ranks the head term.
This adds the city layer, following the same rules as gen-gasolineras.py: every city
carries its own industrial context, its own municipal notes and three of its own FAQ
entries, and the shared technical sections rotate between three written variants so
that no two pages read alike. Pairwise similarity is printed at the end and must stay
well under 0.55.

Costs are anchored to the pillar page ($6,500–$16,000 MXN/m² by nave type) so the two
layers can never contradict each other; island cities get a logistics factor applied
in code.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'kw1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-keyword-pages.py'))
kw1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kw1)

# Base ranges, MXN 2026, same anchors as the pillar page.
BASE = [('Bodega básica (obra gris + acero)', 'Estructura, cubierta, piso, obra civil', 6500, 9000, 'm2'),
        ('Nave industrial estándar', 'Con oficinas, andenes e instalaciones', 9000, 12000, 'm2'),
        ('Centro logístico / nave premium', 'Alta especificación, refrigerado, gran claro', 12000, 16000, 'm2'),
        ('Piso industrial de alta resistencia', 'Concreto reforzado, pulido o epóxico', 900, 2200, 'm2'),
        ('Patio de maniobras y andenes', 'Pavimento para tráiler, rampas, muelles', 1200, 2500, 'm2'),
        ('Subestación e instalación eléctrica', 'Media tensión, tablero, iluminación de nave', 450000, 2500000, 'obra')]


def money(v):
    return '$' + format(int(round(v, -3)), ',d') + ' MXN'


def rows_for(factor):
    out = []
    for label, note, lo, hi, kind in BASE:
        lo2, hi2 = lo * factor, hi * factor
        val = '%s – %s' % (money(lo2), money(hi2)) if kind == 'obra' else \
              '%s – %s / m²' % (money(lo2), money(hi2))
        out.append((label, note, val))
    return out


# --- shared sections, three variants each, rotated by page order
SCOPE = [
 ('Qué entregamos en una nave llave en mano',
  'El paquete completo: proyecto ejecutivo y cálculo estructural, gestión del uso de suelo y de la licencia, '
  'cimentación, estructura metálica de gran claro, cubierta y fachada, piso industrial, andenes y patio de maniobras, '
  'oficinas y mezzanine, instalaciones hidrosanitarias, eléctricas y contra incendio, y la entrega con planos as-built. '
  'Un solo contrato a precio fijo y un solo responsable de obra, que es la diferencia práctica frente a contratar la '
  'estructura por un lado y la obra civil por otro.'),
 ('Alcance de obra: de la cimentación a la entrega',
  'Trabajamos el proyecto completo: estudio de mecánica de suelos, cimentación diseñada para la carga real de racks y '
  'montacargas, estructura de acero, envolvente, losa industrial, muelles de carga, área administrativa, servicios y '
  'sistemas. Si el cliente ya trae proyecto o fabricante de estructura, entramos solo por la obra civil y la '
  'coordinación; si no, lo desarrollamos nosotros. Lo que no hacemos es entregar una nave sin planos as-built ni sin '
  'los trámites cerrados.'),
 ('Nave nueva, ampliación o adecuación',
  'Tres escenarios distintos y tres presupuestos distintos. Nave nueva: terreno, cimentación, estructura y envolvente '
  'desde cero. Ampliación: nuevo módulo empatado a la estructura existente, con el detalle de junta constructiva y de '
  'continuidad de piso, que es donde suele fallar la obra barata. Adecuación de nave rentada: piso, andenes, oficinas, '
  'iluminación, red contra incendio y divisiones para la operación específica del inquilino. En los tres casos el '
  'contrato es a precio fijo por partidas.'),
]

PERMITS = [
 ('Uso de suelo industrial: el filtro que decide todo',
  'Antes de hablar de costo por m², hay que confirmar que el predio admite uso industrial o de bodega según el programa '
  'de desarrollo urbano vigente, y con qué COS, CUS y altura máxima. Después vienen licencia de construcción, DRO, '
  'visto bueno de Protección Civil, el trámite ambiental cuando aplica y la solicitud de carga a CFE. Comprar terreno '
  'antes de verificar el uso de suelo es el error más caro que vemos en obra industrial, y no tiene arreglo de diseño.'),
 ('Permisos, en el orden en que se tramitan',
  'Constancia de uso de suelo compatible; licencia de construcción con proyecto firmado por el Director Responsable de '
  'Obra; dictamen de Protección Civil, que en nave industrial revisa salidas, señalización y sistema contra incendio; '
  'trámite ambiental si el predio o el giro lo exigen; y en paralelo la gestión con CFE, porque la conexión de media '
  'tensión tiene tiempos propios que no dependen del municipio. Ese último punto es el que más retrasa entregas.'),
 ('El expediente de una nave y sus tiempos reales',
  'Uso de suelo, licencia municipal, DRO, Protección Civil, factibilidad de agua y drenaje y factibilidad eléctrica. En '
  'la práctica, el bloque de trámites corre entre 6 y 16 semanas según el municipio y el giro, y la conexión eléctrica '
  'de alta demanda puede ir más allá. Por eso el trámite arranca en paralelo con el proyecto ejecutivo y no cuando la '
  'estructura ya está en el patio del fabricante: la nave terminada sin energía es una inversión parada.'),
]

TECH = [
 ('Cimentación sobre suelo kárstico y piso industrial',
  'El subsuelo de la península es roca caliza con cavidades, rellenos y zonas blandas que cambian en pocos metros. Sin '
  'mecánica de suelos, la cimentación se diseña a ciegas y el resultado se ve en el piso: asentamientos diferenciales, '
  'juntas abiertas y losas fisuradas bajo el paso del montacargas. El piso industrial se calcula por carga puntual de '
  'rack y por tránsito, con espesor, refuerzo, trazo de juntas y acabado definidos antes de colar, no improvisados el '
  'día del colado.'),
 ('Estructura de acero de gran claro y envolvente',
  'La nave se resuelve con marcos rígidos o armaduras de acero que libran claros de 20 a 40 m sin columnas intermedias, '
  'lo que se traduce directamente en área útil y en libertad para acomodar racks y pasillos. En zona costera manda el '
  'diseño por viento: la estructura y sus anclajes se calculan para velocidades de huracán, y la protección '
  'anticorrosiva —galvanizado o esquema de recubrimiento real— es lo que decide si la nave llega a los treinta años o '
  'empieza a picarse al quinto.'),
 ('Detalles que definen la vida útil de la nave',
  'Cuatro puntos concentran los problemas: la cimentación, que debe partir de un estudio de suelos y no de un supuesto; '
  'el piso, calculado por carga de rack y tránsito de montacargas; la cubierta, con pendiente, sellos y bajantes '
  'dimensionados para lluvia tropical intensa; y la protección contra corrosión del acero en ambiente de sal. A eso se '
  'suma el aislamiento térmico de cubierta, que en este clima paga su costo en consumo eléctrico y en condiciones de '
  'trabajo dentro de la nave.'),
]

OPER = [
 ('Plazos y forma de contratación',
  'Una bodega de 800 a 1,200 m² se construye en 5 a 8 meses desde la firma, incluyendo trámites; una nave de 3,000 m² '
  'con oficinas y andenes se va a 9–14 meses. El tiempo de fabricación y montaje de la estructura corre en paralelo con '
  'la cimentación, y ahí se recupera calendario. Contratamos a precio fijo por partidas, con calendario de obra y pagos '
  'ligados a avance verificado, no a fechas del calendario.'),
 ('Cómo se controla el costo en obra industrial',
  'El presupuesto se entrega desglosado por partidas —cimentación, estructura, envolvente, piso, instalaciones, '
  'obra exterior— para que el cliente vea dónde está cada peso y pueda ajustar especificación sin renegociar todo el '
  'contrato. El acero es la partida más volátil: se cotiza y se cierra con el fabricante al inicio, no a mitad de obra. '
  'Los cambios de alcance se documentan por escrito con su costo antes de ejecutarse.'),
 ('Obra con la operación en marcha',
  'En ampliaciones y adecuaciones la empresa casi nunca puede parar. Se trabaja por zonas, con separación física entre '
  'la obra y la operación, accesos y rutas de maniobra diferenciados para que los tráileres del cliente y los de obra '
  'no compitan por el mismo patio, y las maniobras de montaje o los colados grandes programados en fin de semana o en '
  'turno nocturno. El plan de etapas se acuerda con el responsable de la planta antes de firmar el calendario.'),
]

FAQ_COMMON = [
 ('¿Construyen llave en mano o solo la obra civil?',
  'Ambas modalidades. Llave en mano es lo habitual —proyecto, permisos, estructura, obra civil e instalaciones bajo un '
  'solo contrato a precio fijo—, pero si el cliente ya tiene proyecto o fabricante de estructura entramos solo por la '
  'parte que le falta y coordinamos al resto.'),
 ('¿Qué se necesita para cotizar una nave?',
  'Ubicación del terreno, superficie aproximada de construcción y tipo de operación (almacén, distribución, taller, '
  'refrigerado, renta). Con eso entregamos un rango por partidas; para precio cerrado hacen falta mecánica de suelos y '
  'proyecto ejecutivo.'),
]

CITIES = {
'playa-del-carmen': dict(
  name='Playa del Carmen', muni='Solidaridad', factor=1.0, v=0,
  ctx=('Playa del Carmen concentra la logística intermedia del corredor: bodegas de abasto para hotelería y '
       'restaurantes, almacenes de materiales de construcción que alimentan la obra de Tulum y Puerto Aventuras, y '
       'naves de distribución de última milla para una ciudad que sigue creciendo hacia el poniente. La demanda de '
       'bodega en renta se mantiene alta porque el suelo con uso industrial es escaso y está concentrado sobre la 307 '
       'y las salidas de la ciudad.'),
  local=('En Solidaridad los dos puntos que devuelven expedientes son el uso de suelo —muchos predios que se venden '
         'como industriales no lo son— y el impacto vial: accesos para tráiler sobre avenidas con camellón, radios de '
         'giro y carriles de desaceleración. El drenaje pluvial del patio también se revisa, porque la lluvia intensa '
         'encharca con facilidad en toda la zona.'),
  faq=[('¿Cuánto cuesta construir una bodega en Playa del Carmen?',
        'En 2026, desde $6,500 MXN/m² una bodega básica en estructura de acero y hasta $12,000 MXN/m² una nave con '
        'oficinas, andenes e instalaciones completas. El piso industrial y el patio de maniobras se cotizan aparte '
        'porque dependen de la carga real de operación.'),
       ('¿Dónde hay uso de suelo industrial en Playa del Carmen?',
        'Está concentrado en los corredores sobre la carretera federal y en las salidas de la ciudad. Antes de cerrar '
        'la compra de un terreno revisamos la constancia de uso de suelo y el COS, CUS y altura permitidos: es una '
        'verificación de días y evita perder la inversión completa.'),
       ('¿Conviene construir para rentar?',
        'Es el caso más frecuente que nos llega. La bodega en renta se coloca bien cuando tiene altura libre útil, '
        'piso resistente y acceso para tráiler; sin esos tres, se renta a precio de patio techado.')]),

'cancun': dict(
  name='Cancún', muni='Benito Juárez', factor=1.0, v=1,
  ctx=('Cancún es el mercado industrial real del estado: la zona sobre la salida a Mérida y el entorno del aeropuerto '
       'concentran el abasto de todo el corredor, desde alimentos y bebidas hasta materiales, mobiliario y logística de '
       'cruceros. Aquí se construyen las naves más grandes de la región, con andenes para tráiler, cámaras frías y '
       'cargas eléctricas que obligan a subestación propia desde el proyecto.'),
  local=('En Benito Juárez el impacto vial pesa más que en ningún otro municipio: accesos y salidas de tráiler sobre '
         'avenidas de alto flujo, carriles auxiliares y maniobras que deben resolverse dentro del predio. Protección '
         'Civil revisa con detalle el sistema contra incendio en naves de almacenamiento, y la factibilidad eléctrica '
         'de alta demanda conviene arrancarla el mismo mes que la licencia.'),
  faq=[('¿Cuánto tarda construir una nave industrial en Cancún?',
        'Una bodega de 1,000 m², entre 5 y 8 meses con trámites incluidos. Una nave de 3,000 m² con oficinas, andenes '
        'y subestación, de 9 a 14 meses. El cuello de botella suele ser la conexión eléctrica, no la obra.'),
       ('¿Construyen naves con cámara fría o refrigeración?',
        'Sí, en la parte de obra civil, envolvente aislada, piso y preparaciones eléctricas y mecánicas. El equipo de '
        'refrigeración lo instala el proveedor especializado y nosotros programamos la obra alrededor de sus tiempos.'),
       ('¿Se puede ampliar una nave existente sin parar la operación?',
        'Sí, es lo normal en la zona industrial. Se trabaja por zonas con separación física, accesos diferenciados '
        'para los tráileres de obra y maniobras de montaje en fin de semana o turno nocturno.')]),

'tulum': dict(
  name='Tulum', muni='Tulum', factor=1.06, v=2,
  ctx=('Tulum pasó de no tener casi bodega a necesitarla con urgencia: la operación hotelera, el abasto de alimentos, '
       'los almacenes de materiales para la obra en curso y el movimiento generado por el aeropuerto crearon una '
       'demanda que el inventario existente no cubre. La contrapartida es que el suelo con uso industrial es limitado y '
       'el filtro ambiental es el más estricto de la región.'),
  local=('Aquí el expediente ambiental manda sobre el calendario. Suelo kárstico, cenotes y áreas protegidas obligan a '
         'justificar el manejo de escurrimientos del patio y de la cubierta, la disposición de aguas residuales y el '
         'desplante sobre roca fracturada. Un patio de maniobras de varios miles de m² es superficie impermeable, y así '
         'se revisa: con su drenaje pluvial diseñado, no como un anexo del proyecto.'),
  faq=[('¿Por qué una nave en Tulum tarda más en trámites?',
        'Porque al bloque municipal se suma el componente ambiental. La superficie impermeable del patio, el manejo de '
        'escurrimientos y la disposición de aguas residuales se revisan con más detalle que en otros municipios, y eso '
        'suele agregar semanas antes de arrancar obra.'),
       ('¿El suelo kárstico encarece la cimentación?',
        'Puede hacerlo, y por eso la mecánica de suelos no es opcional. En roca sana la cimentación es económica; si '
        'aparecen cavidades o rellenos, el sobrecosto de tratarlas es una fracción de lo que cuesta reparar un piso '
        'industrial asentado.'),
       ('¿Hay demanda de bodega en renta en Tulum?',
        'La hay, sobre todo de superficies medianas para abasto hotelero y de materiales. El inventario formal es '
        'escaso: buena parte de lo que se ofrece son patios techados sin piso ni acceso para tráiler.')]),

'puerto-morelos': dict(
  name='Puerto Morelos', muni='Puerto Morelos', factor=1.05, v=0,
  ctx=('Puerto Morelos está en el punto medio del corredor y a minutos del aeropuerto de Cancún, que es exactamente lo '
       'que busca un centro de distribución que sirva a las dos ciudades. Todavía hay terreno disponible a precio '
       'razonable sobre la federal y hacia la ruta de los cenotes, y eso lo convierte en la alternativa lógica cuando '
       'el suelo industrial de Cancún o Playa se vuelve prohibitivo.'),
  local=('Es un municipio de creación reciente, con trámites que conviene confirmar caso por caso en lugar de asumir '
         'que funcionan igual que en Benito Juárez. El parque nacional arrecifal y la zona de cenotes condicionan el '
         'manejo de agua pluvial y de aguas residuales de cualquier nave, y el acceso desde la carretera federal se '
         'resuelve con la autoridad correspondiente antes de proyectar el patio.'),
  faq=[('¿Conviene ubicar un centro de distribución en Puerto Morelos?',
        'Para servir a Cancún y Playa al mismo tiempo, es la ubicación con mejor equilibrio entre precio de terreno y '
        'tiempo de recorrido, con el aeropuerto a corta distancia. Lo que hay que verificar antes es el uso de suelo '
        'del predio y la factibilidad eléctrica y de agua.'),
       ('¿Afecta la cercanía del arrecife o de los cenotes?',
        'Sí, en el manejo del agua. La cubierta y el patio generan escurrimiento que debe captarse y conducirse según '
        'lo autorizado, y las aguas residuales requieren solución propia cuando no hay red disponible.'),
       ('¿Trabajan sobre la ruta de los cenotes?',
        'Sí. Ahí el punto crítico es la factibilidad de servicios: muchos predios no tienen red eléctrica ni de agua a '
        'pie de terreno, y esa acometida forma parte del presupuesto desde el principio.')]),

'puerto-aventuras': dict(
  name='Puerto Aventuras', muni='Solidaridad', factor=1.03, v=1,
  ctx=('En Puerto Aventuras la demanda no es de gran logística sino de bodega de operación: almacenes de abasto y '
       'mantenimiento para hoteles y condominios, talleres, resguardo de equipo náutico de la marina y espacio de '
       'materiales para la obra residencial del tramo entre Playa del Carmen y Tulum. Son naves de escala media, con '
       'acceso desde la federal y patio suficiente para camión de reparto.'),
  local=('Pertenece a Solidaridad, así que aplican las mismas reglas municipales que en Playa del Carmen, con el '
         'añadido de los accesos sobre carretera federal: carriles de desaceleración, señalización y maniobras que se '
         'autorizan antes de tocar el pavimento. Dentro del fraccionamiento se suman los reglamentos internos, más '
         'estrictos que el municipio en imagen y en horarios de obra.'),
  faq=[('¿Qué tamaño de bodega tiene sentido aquí?',
        'La mayoría de los proyectos que atendemos van de 300 a 1,200 m²: abasto hotelero, mantenimiento, taller o '
        'resguardo. Para superficies mayores, el terreno y el acceso suelen resolverse mejor en Playa del Carmen o '
        'Puerto Morelos.'),
       ('¿Hay sobrecosto por la distancia?',
        'Mínimo. Está a menos de una hora de nuestra base en Playa del Carmen y la cuadrilla se traslada a diario, sin '
        'hospedaje ni estancia cargados al presupuesto.'),
       ('¿Se puede construir dentro del fraccionamiento?',
        'Para obra de servicio y almacén asociada a la operación, sí, cumpliendo el reglamento interno además del '
        'municipal. La restricción real suele ser el uso permitido, no la obra.')]),

'akumal': dict(
  name='Akumal', muni='Tulum', factor=1.06, v=0,
  ctx=('Akumal es un tramo corto y sensible de la 307, con desarrollos residenciales y hoteleros dispersos que '
       'necesitan almacén cercano: bodegas de mantenimiento, resguardo de equipo, talleres y espacio de materiales para '
       'la obra de la zona. No es mercado de gran nave logística, y presentarlo como tal sería engañar: aquí se '
       'construyen bodegas medianas bien resueltas.'),
  local=('Pertenece al municipio de Tulum y hereda su exigencia ambiental. La cercanía a la bahía y a sistemas de '
         'cenotes hace que el manejo de escurrimientos del patio y de la cubierta, junto con la disposición de aguas '
         'residuales, sean el corazón del expediente. La superficie impermeable se justifica con su drenaje, no se '
         'declara y ya.'),
  faq=[('¿Se puede construir una bodega en Akumal?',
        'Sí, en predios con uso de suelo compatible y con el expediente ambiental resuelto. La escala típica es de '
        'bodega de operación y taller, no de centro logístico.'),
       ('¿Qué pasa con el agua de la cubierta y del patio?',
        'Se capta y se maneja según lo autorizado. En roca fracturada, lo que se infiltra sin control llega al '
        'acuífero, y ese es el punto que revisa la autoridad.'),
       ('¿Aplican las mismas reglas que en Tulum centro?',
        'Es el mismo municipio, pero la cercanía a la bahía y a los cenotes hace que el componente ambiental se revise '
        'con más detalle y con más tiempo.')]),

'cozumel': dict(
  name='Cozumel', muni='Cozumel', factor=1.16, v=0,
  ctx=('Cozumel es una isla y eso define la obra antes que cualquier otra consideración. La demanda de bodega viene del '
       'abasto de la población, de la hotelería y del movimiento del puerto de cruceros, con almacenes que trabajan '
       'contra el calendario de los barcos. Todo el material de construcción entra por ferry o barcaza, con costo de '
       'flete que aparece identificado en el presupuesto en lugar de diluirse en los precios unitarios.'),
  local=('El municipio gestiona sus propios trámites y el parque marino condiciona el manejo ambiental de la obra. La '
         'logística es el otro condicionante: estructura metálica, concreto premezclado y cubierta deben programarse '
         'con semanas de anticipación, porque un faltante no se resuelve el mismo día como en el continente. La '
         'cuadrilla se queda en la isla durante la obra.'),
  faq=[('¿Cuánto encarece la obra el hecho de ser isla?',
        'En nuestros presupuestos, del orden de 15% sobre la obra equivalente en el continente, por flete marítimo, '
        'tiempos de entrega y estancia de la cuadrilla. Va identificado como partida, no escondido en el m².'),
       ('¿Cómo llega la estructura de acero a la isla?',
        'Por barcaza, con programa de embarques por etapa y acopio en sitio. Se pide de más en lo crítico —sujeción, '
        'tornillería, lámina— porque parar la obra cuesta más que el material extra.'),
       ('¿Qué tipo de nave se construye en Cozumel?',
        'Bodega de abasto y distribución local, almacén para hotelería y taller. La escala la marca el mercado insular: '
        'superficies medianas, bien resueltas en piso, cubierta y acceso.')]),

'isla-mujeres': dict(
  name='Isla Mujeres', muni='Isla Mujeres', factor=1.15, v=1,
  ctx=('El municipio tiene dos realidades industriales distintas. En la isla, bodegas pequeñas de abasto y taller, con '
       'calles estrechas, maniobras acotadas y material que llega por embarcación. En la porción continental de Costa '
       'Mujeres, la hotelería nueva ha traído demanda real de almacén de abasto y de mantenimiento, con acceso normal '
       'de maquinaria y terreno disponible sobre el corredor hacia Cancún.'),
  local=('El trámite municipal es el mismo en las dos zonas, pero el plan de obra no se parece en nada: en la isla '
         'mandan el ancho de calle, el horario de maniobras y el transporte marítimo; en Costa Mujeres, el acceso vial '
         'y el condicionante ambiental del corredor costero. Conviene definir cuál de las dos es el sitio antes de '
         'estimar cualquier plazo.'),
  faq=[('¿Trabajan en la isla y en Costa Mujeres?',
        'En ambas. La isla exige logística marítima y maniobras acotadas por el ancho de calle; Costa Mujeres se '
        'trabaja como obra de corredor, con acceso normal de maquinaria y montaje.'),
       ('¿Cuánto sube el costo respecto al continente?',
        'Alrededor de 15% en la obra dentro de la isla. En Costa Mujeres, prácticamente el mismo costo que en Cancún.'),
       ('¿Se puede montar estructura de acero en la isla?',
        'Sí, con la estructura despiezada para el traslado y el montaje programado por tramos. El límite lo pone el '
        'acceso al predio, no la técnica.')]),
}


def make(slug_city, d, order):
    city = d['name']
    i = order
    v, vp, vc, vo = i % 3, (i + 1) % 3, (i + 2) % 3, (i // 3) % 3
    secs = [
        ('Naves industriales y bodegas en %s' % city, d['ctx']),
        SCOPE[v],
        PERMITS[vp],
        ('Costos de construcción 2026 en %s' % city,
         'Rangos por m² de construcción para nave nueva, más las partidas que más mueven el total: piso industrial, '
         'patio de maniobras y acometida eléctrica. No incluyen terreno, racks ni equipo de proceso. En isla se suma '
         'el flete, que identificamos por separado en lugar de esconderlo en los precios unitarios.'),
        TECH[vc],
        ('Normativa local: %s' % d['muni'], d['local']),
        OPER[vo],
    ]
    faq = d['faq'] + FAQ_COMMON
    # three sibling cities, rotated by order so the cluster links in a ring instead of
    # every page pointing at the same two neighbours
    sibs = list(CITIES.items())
    sibs = [sibs[(order + k) % len(sibs)] for k in (1, 2, 3)]
    links = [('/naves-industriales-bodegas-riviera-maya/', 'Naves y bodegas en toda la Riviera Maya')]
    links += [('/construccion-naves-industriales-bodegas-%s/' % s, 'Naves y bodegas en %s' % c['name'])
              for s, c in sibs]
    links += [('/construccion-comercial-oficinas/', 'Construcción comercial y oficinas'),
              ('/permisos-licencias-construccion-riviera-maya/', 'Permisos y licencias'),
              ('/cimentacion-y-losas-playa-del-carmen/', 'Cimentación y losas'),
              ('/supervision-de-obra/', 'Supervisión de obra')]
    t_long = 'Construcción de Naves Industriales y Bodegas en %s | Recrea' % city
    t_short = 'Naves Industriales y Bodegas en %s | Recrea' % city
    return dict(
        title=t_long if len(t_long) <= 65 else t_short,
        desc=('Construcción de naves industriales y bodegas en %s: estructura de acero, piso industrial, '
              'andenes y permisos. Costos 2026 y plazos reales.' % city),
        h1='Construcción de Naves Industriales y Bodegas en %s' % city,
        lead=('Naves industriales, bodegas y centros de distribución llave en mano en %s: estructura de acero de gran '
              'claro, piso industrial, andenes de carga, oficinas y permisos, con contrato a precio fijo.' % city),
        secs=secs,
        table=('Concepto', 'Incluye', 'Costo 2026') + (rows_for(d['factor']),),
        faq=faq, links=links)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src = open(kw1.TPL, encoding='utf-8').read()
    built = {}
    for i, (slug_city, d) in enumerate(CITIES.items()):
        slug = 'construccion-naves-industriales-bodegas-' + slug_city
        page = make(slug_city, d, i)
        os.makedirs(slug, exist_ok=True)
        html = kw1.build(slug, page, src)
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
        built[slug] = set(tuple(body[j:j + 6]) for j in range(len(body) - 5))
        print('%-56s title %2d  desc %3d  words %d' % (slug + '/', len(page['title']), len(page['desc']), len(body)))
    ks = list(built)
    mx = max((len(built[a] & built[b]) / len(built[a] | built[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity: %.2f  (%s vs %s)' % mx)
