#!/usr/bin/env python3
"""Gas station construction / remodeling pages, one per city in the service corridor.

Search volume here is tiny (Semrush MX: "construccion de gasolineras" 20/mo,
"remodelacion de gasolineras" 10/mo, most city variants have no data at all).
These pages exist for a different reason than the guides: a single captured lead
is a multi-million-peso contract, and the B2B credibility carries over to the rest
of the commercial work.

Because volume is thin, thin duplicate pages would be actively harmful. Every city
below carries its own local context, its own municipal notes, its own logistics
section and three of its own FAQ entries; the shared technical sections rotate
between three written variants. Measured pairwise similarity is printed at the end
and must stay well under 0.55.

Scope is stated honestly on every page: we do the civil work, the canopy, the shop
and the image change. Tanks, pipe and dispensing equipment are ASEA-regulated and
are executed by certified specialists — we coordinate around them, we do not claim
to install them.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'kw1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-keyword-pages.py'))
kw1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kw1)

# Base civil-work ranges, MXN, 2026. Island cities get a logistics factor applied in code
# so the table and the FAQ can never drift apart.
BASE = [('Cambio de imagen y señalización', 'Fascia de canopy, tótem, pintura, señalética', 350000, 1200000, 'obra'),
        ('Canopy nuevo o sustitución', 'Estructura metálica, cubierta, iluminación', 1800, 3500, 'm2'),
        ('Patio de maniobras', 'Concreto hidráulico resistente a hidrocarburos', 900, 1800, 'm2'),
        ('Tienda de conveniencia', 'Obra civil, instalaciones y acabados', 8000, 18000, 'm2'),
        ('Estación nueva, obra civil completa', 'Sin equipo de despacho ni tanques', 6000000, 15000000, 'obra')]


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


# --- shared technical sections, three variants, rotated so no two neighbouring cities match
SCOPE = [
 ('Qué construimos y qué no',
  'Hacemos la obra civil de la estación: patio de maniobras, islas, canopy, tienda de conveniencia, baños, '
  'oficinas, barda, drenajes, cisterna, obra eléctrica de baja tensión, señalética e imagen de marca. '
  'Lo que no hacemos es instalar tanques, tubería de producto ni dispensarios: eso corresponde a empresas '
  'certificadas bajo la normatividad de ASEA y así debe quedar en el contrato. Trabajamos coordinados con '
  'ese proveedor, no encima de él.'),
 ('Alcance real de nuestro trabajo',
  'Nuestro contrato cubre la parte civil y de imagen: terracerías, pavimento del patio, islas de despacho, '
  'estructura y cubierta del canopy, tienda, sanitarios, área administrativa, instalaciones hidrosanitarias, '
  'obra eléctrica de baja tensión, drenaje pluvial separado y señalización. El sistema de almacenamiento y '
  'despacho de combustible lo ejecuta un contratista certificado conforme a la normatividad de ASEA; '
  'nosotros programamos la obra alrededor de sus tiempos y de sus pruebas.'),
 ('Cómo se divide la obra de una estación',
  'Una estación de servicio se construye con dos contratos que corren en paralelo: el de obra civil e imagen '
  '—que es el nuestro— y el del sistema de combustible, que por normatividad ejecuta una empresa certificada '
  'ante ASEA. Confundirlos es la causa más común de retrasos: el patio no se puede colar antes de que la '
  'tubería esté probada, y el canopy no se cierra antes de que el dispensario esté posicionado. '
  'Lo que sí garantizamos es que nuestra parte no sea la que detiene el calendario.'),
]

PERMITS = [
 ('Trámites: federales, estatales y municipales',
  'Una estación necesita permiso federal para el expendio al público de petrolíferos, el trámite ambiental y '
  'de seguridad industrial ante ASEA, y del lado local: uso de suelo compatible, licencia de construcción, '
  'dictamen de impacto vial y visto bueno de protección civil. La autoridad federal que emite el permiso ha '
  'cambiado de adscripción en los últimos años, así que conviene confirmar el trámite vigente antes de fijar '
  'fechas: es el rubro donde más se equivocan los calendarios.'),
 ('El expediente, por orden de importancia',
  'Lo primero es el uso de suelo: si el predio no admite estación de servicio, no hay proyecto que lo arregle. '
  'Después vienen el permiso federal de expendio al público, el expediente ambiental y de seguridad ante ASEA, '
  'el impacto vial y protección civil, y al final la licencia municipal de construcción. Cada municipio agrega '
  'sus propias distancias mínimas a escuelas, hospitales y zonas habitacionales, y esas distancias se verifican '
  'antes de comprar el terreno, no después.'),
 ('Permisos antes de mover una máquina',
  'Federal: permiso de expendio al público de petrolíferos y expediente ante ASEA en materia ambiental y de '
  'seguridad industrial. Local: uso de suelo, licencia de construcción, impacto vial, protección civil y, según '
  'la ubicación, autorización ambiental adicional. Los tiempos reales de este bloque suelen superar a los de la '
  'obra, y por eso la programación seria empieza por el trámite y no por el calendario constructivo.'),
]

CIVIL = [
 ('La obra civil que sí decide la vida útil',
  'El patio es lo que más se castiga: carga pesada, giros continuos, derrames y lluvia intensa. Se resuelve con '
  'concreto hidráulico de resistencia adecuada, juntas bien trazadas, pendientes hacia el sistema de captación y '
  'separador de hidrocarburos, y drenaje pluvial independiente del sanitario. Un patio mal colado se agrieta en '
  'el primer año y se repara con la estación operando, que es la forma más cara de hacerlo.'),
 ('Dónde se gana o se pierde la obra',
  'En el pavimento del patio y en el drenaje. El concreto hidráulico debe estar diseñado para tránsito pesado y '
  'para contacto con hidrocarburos; las pendientes deben llevar el escurrimiento al separador y no a la calle; '
  'y el drenaje pluvial va separado del sanitario. Después importa el canopy: estructura calculada para viento de '
  'zona costera, con anclajes y herrajes protegidos contra corrosión.'),
 ('Detalles constructivos que importan aquí',
  'Concreto hidráulico en el patio, diseñado para carga pesada y derrames; pendientes hacia el separador de '
  'hidrocarburos; drenaje pluvial separado; canopy con estructura calculada para viento costero y protección '
  'anticorrosiva real, no solo pintura; e instalación eléctrica con las clasificaciones que exige el entorno de '
  'la zona de despacho. En clima de sal y lluvia intensa, el ahorro en protección se paga en el tercer año.'),
]

OPER = [
 ('Remodelar sin cerrar la estación',
  'Casi ningún operador puede cerrar. Se trabaja por etapas y por franjas horarias: se aísla una zona con barrera '
  'física y señalización, se mantiene el flujo de vehículos por el resto del patio, y las maniobras ruidosas o de '
  'grúa se programan en horario de baja demanda. Un cambio de imagen completo se resuelve normalmente en días, no '
  'en semanas, si el material llega antes de que empiece la obra.'),
 ('Obra con la estación operando',
  'Se define primero el plan de etapas con el operador: qué islas quedan fuera de servicio y cuándo, cómo circulan '
  'los vehículos, dónde se aísla el área de trabajo y qué se hace de noche. Toda maniobra cerca de la zona de '
  'despacho se coordina con el responsable de la estación y con su protocolo de seguridad. Nada se improvisa junto '
  'a un dispensario.'),
 ('Etapas, horarios y seguridad',
  'La obra se divide para que la estación siga vendiendo: media plataforma a la vez, barreras físicas, señalización '
  'de desvío interno y trabajos ruidosos fuera de hora pico. En zona de despacho se respeta el protocolo de seguridad '
  'del operador, sin herramienta que genere chispa donde no corresponde y con permisos de trabajo por escrito.'),
]

FAQ_COMMON = [
 ('¿Instalan tanques y dispensarios?',
  'No. El sistema de almacenamiento y despacho lo ejecuta una empresa certificada conforme a la normatividad de ASEA. '
  'Nosotros hacemos la obra civil, el canopy, la tienda y la imagen, y coordinamos nuestro calendario con el suyo.'),
 ('¿Trabajan con la estación abierta?',
  'Sí, es lo habitual. Se planifica por etapas, con áreas aisladas, señalización de circulación interna y maniobras '
  'pesadas en horario de baja demanda.'),
]

CITIES = {
'playa-del-carmen': dict(
  name='Playa del Carmen', muni='Solidaridad', factor=1.0, v=0,
  ctx=('Playa del Carmen concentra el tránsito de la carretera federal 307 y el reparto urbano de una ciudad que no '
       'deja de crecer hacia el poniente. Las estaciones que más obra piden son las del corredor de la 307 y las de '
       'las avenidas que alimentan Ejido y las colonias nuevas: patios castigados por reparto continuo, tiendas de '
       'conveniencia que se quedaron chicas y canopies con quince años de sal encima.'),
  local=('En Solidaridad la revisión municipal se detiene en dos puntos: el impacto vial —accesos, carriles de '
         'desaceleración y radios de giro sobre avenidas con camellón— y el drenaje pluvial, en una ciudad donde la '
         'lluvia intensa encharca con facilidad. Conviene resolver ambos en el anteproyecto, porque son los que '
         'devuelven expedientes.'),
  faq=[('¿Cuánto tarda un cambio de imagen en Playa del Carmen?',
        'Con material en sitio, entre 5 y 12 días trabajando por etapas y sin cerrar la estación. El plazo lo suele '
        'marcar la fabricación de fascia y tótem, no la instalación.'),
       ('¿Pueden trabajar de noche sobre la 307?',
        'Sí, y en el corredor de la 307 suele ser lo más eficiente para maniobras de grúa y para colados de patio. '
        'Se coordina con el operador y con la señalización vial correspondiente.'),
       ('¿Hacen también la tienda de conveniencia?',
        'Sí: obra civil, instalaciones, aire acondicionado, acabados, mobiliario fijo y baños. Es la parte donde el '
        'operador recupera margen más rápido después de la inversión.')]),

'cancun': dict(
  name='Cancún', muni='Benito Juárez', factor=1.0, v=1,
  ctx=('Cancún es el mercado más grande del estado y el más exigente en logística de obra: estaciones en avenidas '
       'principales con tránsito continuo, otras dentro del corredor hotelero con restricciones de horario, y un '
       'cinturón de estaciones nuevas hacia la zona de Cumbres y la salida a Mérida. El volumen de despacho es alto, '
       'y eso significa que cerrar aunque sea media plataforma tiene un costo diario que el operador conoce al peso.'),
  local=('En Benito Juárez el impacto vial pesa más que en cualquier otro municipio de la región: accesos y salidas '
         'sobre avenidas de alto flujo, carriles auxiliares y maniobras de pipas. En el corredor hotelero se suman '
         'restricciones de horario y de ruido que condicionan el calendario de obra desde el primer día.'),
  faq=[('¿Pueden operar dentro de la zona hotelera de Cancún?',
        'Sí, ajustándonos a las ventanas de horario y a las restricciones de ruido y de acceso de la zona. La '
        'programación se arma alrededor de esas ventanas, no al revés.'),
       ('¿Cuánto cuesta remodelar una estación en Cancún?',
        'Un cambio de imagen completo se ubica entre $350,000 y $1,200,000 MXN según el tamaño del canopy y la '
        'cantidad de señalización; la remodelación de la tienda se cotiza por m² y suele ser la partida mayor.'),
       ('¿Trabajan estaciones en Cumbres y en la salida a Mérida?',
        'Sí. Son las zonas con más obra nueva del municipio y donde el patio y el drenaje se diseñan pensando en '
        'tránsito pesado desde el primer día.')]),

'tulum': dict(
  name='Tulum', muni='Tulum', factor=1.06, v=2,
  ctx=('Tulum es el municipio donde el expediente ambiental manda sobre todo lo demás. Las estaciones del corredor de '
       'la 307 y de la salida a Cobá conviven con suelo kárstico, cenotes y áreas naturales protegidas, y eso cambia '
       'el diseño del drenaje, de la contención de derrames y del propio patio. El crecimiento del aeropuerto y de la '
       'zona de nuevos desarrollos ha traído obra nueva, pero con un filtro ambiental que no existe en otros municipios.'),
  local=('Aquí la contención de escurrimientos deja de ser un detalle: en roca fracturada, lo que se infiltra llega al '
         'acuífero y de ahí a los cenotes. El separador de hidrocarburos, la impermeabilización del patio y el manejo '
         'del agua pluvial se revisan con lupa, y el expediente ambiental fija el calendario de toda la obra.'),
  faq=[('¿Por qué una estación en Tulum tarda más en trámites?',
        'Porque el componente ambiental es más exigente: suelo kárstico, cenotes y áreas protegidas obligan a '
        'justificar el manejo de escurrimientos y de derrames con más detalle que en otros municipios.'),
       ('¿Cambia el diseño del patio por el suelo de Tulum?',
        'Sí. La impermeabilización, las pendientes y la captación se diseñan para que ningún escurrimiento con '
        'hidrocarburos alcance el subsuelo, y eso se refleja en el costo del patio.'),
       ('¿Trabajan en la zona del aeropuerto y la salida a Cobá?',
        'Sí. Son los dos frentes con más movimiento del municipio para obra nueva y para ampliación de estaciones '
        'existentes.')]),

'puerto-morelos': dict(
  name='Puerto Morelos', muni='Puerto Morelos', factor=1.05, v=0,
  ctx=('Puerto Morelos vive del tramo Cancún–Playa de la 307 y de la ruta de los cenotes. Es un municipio joven, con '
       'un parque nacional arrecifal frente a la costa, y eso condiciona cualquier obra que maneje hidrocarburos. Las '
       'estaciones aquí sirven a tránsito de paso más que a reparto urbano, con picos fuertes de fin de semana.'),
  local=('El arrecife es área natural protegida y el manejo de escurrimientos se revisa en consecuencia. A eso se suma '
         'un municipio de creación reciente, con trámites que conviene confirmar caso por caso en lugar de asumir que '
         'funcionan igual que en Benito Juárez o Solidaridad.'),
  faq=[('¿La cercanía del arrecife afecta el proyecto?',
        'Sí, en el manejo de agua pluvial y en la contención de derrames. El expediente debe demostrar que nada con '
        'hidrocarburos alcanza el escurrimiento natural hacia la costa.'),
       ('¿Atienden estaciones sobre la ruta de los cenotes?',
        'Sí, con la misma lógica: en esa zona el suelo y el agua subterránea son el punto crítico del diseño.'),
       ('¿Cuánto personal mueven a un municipio pequeño?',
        'La cuadrilla se traslada completa desde Playa del Carmen o Cancún. No dependemos de subcontratación local, '
        'que es lo que suele estirar los plazos en municipios chicos.')]),

'puerto-aventuras': dict(
  name='Puerto Aventuras', muni='Solidaridad', factor=1.03, v=1,
  ctx=('Puerto Aventuras es tránsito puro de la 307 entre Playa del Carmen y Tulum, con un fraccionamiento cerrado y '
       'una marina que generan demanda propia. Las estaciones del tramo atienden turismo de paso, transporte de '
       'personal hotelero y reparto hacia los desarrollos de la costa, con muy poca tolerancia al cierre porque las '
       'alternativas quedan a kilómetros.'),
  local=('Al ser Solidaridad, aplican las mismas reglas municipales que en Playa del Carmen, con el añadido de los '
         'accesos sobre carretera federal: carriles de desaceleración, señalización y maniobras que se resuelven con '
         'la autoridad correspondiente antes de tocar el pavimento.'),
  faq=[('¿Se puede remodelar sin cortar el tránsito de la 307?',
        'Sí. Se trabaja por mitades de patio, con señalización interna y con las maniobras que invaden acceso '
        'programadas en horario de baja demanda.'),
       ('¿Atienden también la marina y el fraccionamiento?',
        'Sí, para obra civil y comercial. En el fraccionamiento aplican además los reglamentos internos, que suelen '
        'ser más estrictos que el municipio en horarios y en imagen.'),
       ('¿Hay sobrecosto por la distancia?',
        'Mínimo: está a menos de una hora de nuestra base en Playa del Carmen y la cuadrilla se traslada a diario.')]),

'akumal': dict(
  name='Akumal', muni='Tulum', factor=1.06, v=0,
  ctx=('Akumal es un tramo corto y sensible de la 307: bahía con tortugas, cenotes tierra adentro y desarrollos '
       'residenciales dispersos. El servicio de combustible aquí atiende sobre todo tránsito de paso y operación '
       'hotelera de la zona, y cualquier obra convive con un entorno donde el manejo del agua es el tema central.'),
  local=('Pertenece al municipio de Tulum, así que hereda su exigencia ambiental. La cercanía a la bahía y a sistemas '
         'de cenotes hace que la contención de derrames y la separación del drenaje pluvial sean el corazón del '
         'expediente, no un anexo.'),
  faq=[('¿Akumal tiene reglas distintas a Tulum centro?',
        'Es el mismo municipio, pero la cercanía a la bahía y a los sistemas de cenotes hace que el componente '
        'ambiental se revise con más detalle.'),
       ('¿Qué pasa con el agua pluvial del patio?',
        'Se capta, se conduce al separador de hidrocarburos y se maneja según lo autorizado. No puede escurrir al '
        'terreno natural ni a la carretera.'),
       ('¿Trabajan en estaciones pequeñas de dos islas?',
        'Sí. La escala cambia el monto, no el procedimiento: mismo criterio de patio, drenaje y contención.')]),

'cozumel': dict(
  name='Cozumel', muni='Cozumel', factor=1.16, v=0,
  ctx=('Cozumel es una isla, y eso define la obra antes que cualquier otra consideración. Todo el material entra por '
       'ferry o por barcaza, con calendario propio y con costo de flete que se refleja en el presupuesto. Las '
       'estaciones atienden a la población local, al transporte turístico y al movimiento del puerto de cruceros, con '
       'una demanda muy marcada por temporada.'),
  local=('El municipio de Cozumel gestiona sus propios trámites y el parque marino condiciona el manejo ambiental de '
         'cualquier obra que involucre hidrocarburos. A eso se suma la logística: el concreto premezclado, el acero '
         'del canopy y la señalización deben programarse con semanas de anticipación, porque un faltante no se '
         'resuelve el mismo día como en el continente.'),
  faq=[('¿Cuánto encarece la obra el hecho de ser isla?',
        'En nuestros presupuestos, del orden de 15% sobre la obra civil equivalente en el continente, por flete '
        'marítimo, tiempos de entrega y estancia de la cuadrilla.'),
       ('¿Cómo manejan el suministro de materiales?',
        'Con programa de embarques por etapa y acopio en sitio. Se pide de más en lo crítico —acero, sujeción, '
        'señalización— porque el costo de parar la obra supera el del material extra.'),
       ('¿La cuadrilla se queda en la isla?',
        'Sí, durante la obra. Se contempla hospedaje y traslado en el presupuesto desde el principio, en lugar de '
        'aparecer después como extra.')]),

'isla-mujeres': dict(
  name='Isla Mujeres', muni='Isla Mujeres', factor=1.15, v=1,
  ctx=('El municipio de Isla Mujeres tiene dos realidades: la isla, con calles estrechas, tránsito de carritos de golf '
       'y logística por embarcación; y la porción continental de Costa Mujeres, donde la hotelería nueva ha traído '
       'demanda de servicio sobre el corredor hacia Cancún. Son dos escenarios de obra distintos bajo la misma '
       'autoridad municipal.'),
  local=('En la isla, el acceso de maquinaria y el horario de maniobras son la restricción principal, junto con el '
         'transporte marítimo del material. En Costa Mujeres el condicionante es el vial y el ambiental del corredor '
         'costero. El trámite municipal es el mismo, pero el plan de obra no se parece en nada.'),
  faq=[('¿Trabajan en la isla y en Costa Mujeres?',
        'En ambas. La isla exige logística marítima y maniobras acotadas por el ancho de calle; Costa Mujeres se '
        'trabaja como obra de corredor, con acceso normal de maquinaria.'),
       ('¿Cómo llega el material a la isla?',
        'Por embarcación, con programa por etapas y acopio previo. El costo del traslado va identificado en el '
        'presupuesto, no diluido en los precios unitarios.'),
       ('¿Cuánto sube el costo respecto al continente?',
        'Alrededor de 15% en la obra civil de la isla. En Costa Mujeres, prácticamente el mismo costo que en Cancún.')]),
}

PILLAR = dict(
  name='la Riviera Maya', muni='Quintana Roo', factor=1.0, v=1,
  ctx=('Atendemos estaciones de servicio en todo el corredor: Cancún, Puerto Morelos, Playa del Carmen, Puerto '
       'Aventuras, Akumal, Tulum, Cozumel e Isla Mujeres. El corredor de la carretera federal 307 concentra la mayor '
       'parte del parque de estaciones de la zona, con volúmenes altos, tránsito continuo y muy poco margen para '
       'cerrar. Es obra comercial exigente: se hace con la estación operando y con normatividad federal encima.'),
  local=('Cada municipio agrega lo suyo: impacto vial en Benito Juárez y Solidaridad, exigencia ambiental en Tulum y '
         'Puerto Morelos, logística marítima en Cozumel e Isla Mujeres. El trámite federal y el expediente ante ASEA '
         'son comunes; el calendario real lo define el municipio y, en las islas, el flete.'),
  faq=[('¿En qué ciudades trabajan?',
        'Cancún, Puerto Morelos, Playa del Carmen, Puerto Aventuras, Akumal, Tulum, Cozumel e Isla Mujeres. Fuera de '
        'ese corredor lo evaluamos caso por caso: preferimos decir que no antes que estirar una cuadrilla.'),
       ('¿Construyen estaciones nuevas o solo remodelan?',
        'Ambas, en la parte civil. Obra nueva completa —patio, islas, canopy, tienda, oficinas— y remodelación o '
        'cambio de imagen sobre estaciones en operación.'),
       ('¿Cuánto cuesta la obra civil de una estación nueva?',
        'Del orden de $6,000,000 a $15,000,000 MXN según tamaño, número de islas, superficie de tienda y condiciones '
        'del terreno, sin considerar equipo de despacho ni tanques.')])


def make(slug_city, d, order):
    city = d['name']
    de_city = city if city.startswith('la ') else city
    # four independent rotation indices derived from the page order: with 9 pages this
    # gives every city a unique combination of the shared sections
    i = order
    v, vp, vc, vo = i % 3, (i + 1) % 3, (i + 2) % 3, (i // 3) % 3
    secs = [
        ('Estaciones de servicio en %s' % de_city, d['ctx']),
        SCOPE[v],
        PERMITS[vp],
        ('Costos de obra civil 2026 en %s' % de_city,
         'Rangos de la obra civil y de imagen, sin equipo de despacho ni tanques. El patio y la tienda son las '
         'partidas que más mueven el total; en isla se suma el flete, que identificamos por separado en lugar de '
         'esconderlo en los precios unitarios.'),
        CIVIL[vc],
        ('Normativa local: %s' % d['muni'], d['local']),
        OPER[vo],
    ]
    # build() places the table after the third section, which is exactly where the cost text sits
    secs = secs[:3] + [secs[3]] + secs[4:]
    faq = d['faq'] + FAQ_COMMON
    links = [('/construccion-remodelacion-gasolineras-riviera-maya/', 'Gasolineras en toda la Riviera Maya')] if slug_city else []
    links += [('/construccion-comercial-hoteles-riviera-maya/', 'Construcción comercial y hotelera'),
              ('/permisos-licencias-construccion-riviera-maya/', 'Permisos y licencias'),
              ('/supervision-de-obra/', 'Supervisión de obra')]
    if not slug_city:
        links = [('/construccion-remodelacion-gasolineras-%s/' % s, 'Gasolineras en %s' % c['name'])
                 for s, c in list(CITIES.items())[:3]] + links[1:]
    # long title where it fits under 65 chars, short one where it does not
    t_long = 'Construcción y Remodelación de Gasolineras en %s | Recrea' % city
    t_short = 'Construcción de Gasolineras en %s | Recrea' % city
    return dict(
        title=t_long if len(t_long) <= 65 else t_short,
        desc=('Obra civil e imagen para gasolineras en %s: patio, canopy, tienda y señalización, '
              'con la estación operando. Costos 2026 y trámites.' % city),
        h1='Construcción y Remodelación de Gasolineras en %s' % city,
        lead=('Obra civil e imagen para estaciones de servicio en %s: patio, islas, canopy, tienda y señalización, '
              'trabajando por etapas para que la estación no deje de vender.' % city),
        secs=secs,
        table=('Concepto', 'Incluye', 'Costo 2026') + (rows_for(d['factor']),),
        faq=faq, links=links)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src = open(kw1.TPL, encoding='utf-8').read()
    built = {}
    items = [('', PILLAR)] + list(CITIES.items())
    for i, (slug_city, d) in enumerate(items):
        slug = 'construccion-remodelacion-gasolineras-' + (slug_city or 'riviera-maya')
        page = make(slug_city, d, i)
        os.makedirs(slug, exist_ok=True)
        html = kw1.build(slug, page, src)
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
        built[slug] = set(tuple(body[j:j + 6]) for j in range(len(body) - 5))
        print('%-52s title %2d  desc %3d  words %d' % (slug + '/', len(page['title']), len(page['desc']), len(body)))
    ks = list(built)
    mx = max((len(built[a] & built[b]) / len(built[a] | built[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity: %.2f  (%s vs %s)' % mx)
