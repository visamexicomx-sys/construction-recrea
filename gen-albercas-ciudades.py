#!/usr/bin/env python3
"""Albercas: one page per city, on the axis that actually has search demand.

Why this cluster and not another city grid. Semrush, MX database, monthly volume:

    albercas cancun                     1300     constructoras en cancun      480
    alberca infinity                     720     constructoras en tulum        30
    construccion de albercas             590     constructoras en pdc          20
    piscinas cancun                      390     constructora en tulum         10
    cuanto cuesta una alberca            320     constructora puerto morelos    0
    albercas playa del carmen            210     construccion tulum             0
    piscinas playa del carmen            210     remodelacion cancun            0
    albercas tulum                       170

The 466 "constructora / construccion de casas + ciudad" pages already on the site
cover, all languages and all neighbourhoods added together, roughly 600 searches a
month. Pools alone are about 4,300, and before this script the site had a regional
pillar (/construccion-albercas/) and a luxury page for Playa del Carmen, but not one
page aimed at "albercas cancun" — the single biggest keyword on the map.

Prices are anchored to the pillar so the two layers cannot contradict each other:
plunge $6,500–$11,000 USD, estándar 4×8 $14,000–$22,000, grande 5×10 $22,000–$33,000,
infinity $22,000–$45,000, rooftop $28,000–$67,000. Cities away from the Cancún–Playa
corridor carry a logistics factor applied in code rather than a different price list.

Shared sections rotate between three written variants and every city carries its own
context, its own municipal note and three of its own FAQ entries; pairwise similarity
is printed at the end and must stay well under 0.55.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'kw1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-keyword-pages.py'))
kw1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kw1)

# USD, 2026, identical anchors to /construccion-albercas/.
BASE = [('Plunge pool 2×4 m', 'Lotes chicos, rooftops, Airbnb', 6500, 11000),
        ('Estándar de concreto 4×8 m', 'Residencial — la más solicitada', 14000, 22000),
        ('Grande 5×10 m', 'Villas y familias grandes', 22000, 33000),
        ('Infinity / desbordante', 'Lotes con desnivel o vista', 22000, 45000),
        ('Rooftop con refuerzo estructural', 'Condominios y hoteles boutique', 28000, 67000),
        ('Comercial / hotelera', 'Con cumplimiento normativo completo', 50000, 120000)]


def money(v):
    return '$' + format(int(round(v, -2)), ',d')


def rows_for(factor):
    return [(label, note, '%s – %s USD' % (money(lo * factor), money(hi * factor)))
            for label, note, lo, hi in BASE]


# --- shared sections, three variants each, rotated by page order -------------
SCOPE = [
 ('Qué incluye una alberca llave en mano',
  'El precio de arriba no es el casco solo. Incluye trazo y excavación, plantilla, armado y colado del vaso, '
  'instalación hidráulica de succión y retorno, cuarto de máquinas con bomba y filtro, acabado interior, borde y '
  'chapoteadero si lleva, arranque y entrega con la química del agua estabilizada. Fuera del precio quedan iluminación '
  'escénica, calentador, sistema de sal, cascadas y el deck perimetral, que se cotizan por separado porque no todos '
  'los proyectos los llevan.'),
 ('Alcance: del trazo al arranque del equipo',
  'Trabajamos la alberca completa: replanteo sobre terreno, excavación en roca caliza, vaso de concreto armado, '
  'tuberías con prueba de presión antes de tapar, cuarto de máquinas, acabado, boquillas y arranque. Si el cliente ya '
  'trae proyecto de arquitectura, entramos solo por la obra; si no, lo resolvemos nosotros con el ingeniero '
  'estructural. Lo que no entregamos es una alberca sin prueba hidrostática documentada.'),
 ('Alberca nueva, remodelación o cambio de acabado',
  'Tres trabajos distintos y tres presupuestos distintos. Nueva: excavación, vaso, instalación y acabado desde cero. '
  'Remodelación: se conserva el vaso si el concreto está sano, y se cambian acabado, boquillas, tubería y equipo — '
  'suele costar entre 35% y 60% de una alberca nueva. Cambio de acabado solamente: retiro del mosaico o del aplanado '
  'viejo, reparación de grietas y aplicación nueva. Antes de cotizar cualquiera de las dos últimas revisamos el vaso, '
  'porque una fuga estructural cambia por completo el alcance.')]

TECH = [
 ('Roca caliza, manto freático y salitre',
  'Tres condiciones que definen la ingeniería en esta costa. La roca caliza obliga a excavar con martillo o rompedora '
  'y encarece el movimiento de tierra respecto a un suelo blando, pero a cambio da un apoyo excelente al vaso. El '
  'manto freático está alto cerca de la costa: si el nivel sube por encima del fondo, el vaso vacío puede flotar, y '
  'por eso se instala válvula hidrostática y se define un procedimiento de vaciado. El salitre ataca herrajes, '
  'luminarias y equipos: todo lo metálico expuesto va en acero inoxidable 316 o en material no ferroso.'),
 ('Por qué una alberca aquí no se construye como en el altiplano',
  'El vaso lleva armado y espesor calculados para el empuje del terreno rocoso, no la receta estándar. La tubería se '
  'prueba a presión antes de tapar porque abrir un piso de chukum o de piedra para buscar una fuga cuesta más que la '
  'tubería completa. El equipo se especifica para agua dura: la caliza deja incrustación, y una bomba mal elegida se '
  'sacrifica en dos temporadas. Y el cuarto de máquinas se ubica y se ventila pensando en huracán, no solo en estética.'),
 ('Filtración, calidad de agua y consumo eléctrico',
  'El sistema decide el costo de vivir con la alberca. Filtro de arena con bomba de velocidad variable es el estándar '
  'sensato: baja el consumo eléctrico de forma notoria frente a una bomba de una sola velocidad, que es lo que casi '
  'siempre viene en las cotizaciones baratas. La clorinación salina evita el manejo de cloro y trata mejor el agua, '
  'pero exige que todo el herraje sea inoxidable o no ferroso. En agua dura conviene además controlar la dureza desde '
  'el arranque, porque la incrustación en el acabado no se quita después sin dañarlo.')]

FINISH = [
 ('Acabados: chukum, mosaico y agregado expuesto',
  'El chukum es la resina de árbol maya aplicada sobre aplanado: impermeable, sin junta, en tonos tierra que dan el '
  'agua verde-turquesa característico de la zona; $800–$1,500 MXN/m² y requiere aplicador con oficio, porque el color '
  'depende de la mano. El mosaico veneciano es el clásico durable, reparable pieza por pieza, con la junta como único '
  'punto de mantenimiento. El agregado expuesto tipo pebble da textura antiderrapante y aguanta muy bien el tránsito '
  'de una casa de renta. Los tres funcionan aquí; el que no funciona es la pintura epóxica, que en este clima no pasa '
  'de dos temporadas.'),
 ('Qué acabado elegir según el uso de la casa',
  'Casa habitada todo el año: mosaico o pebble, porque se reparan por zonas sin vaciar la alberca entera. Casa de '
  'renta vacacional: pebble por lo antiderrapante y por cómo esconde el desgaste entre huéspedes. Proyecto de diseño '
  'con estética de la zona: chukum, que es lo que la mayoría de la gente busca cuando pide "una alberca como las de '
  'Tulum". Casa cerrada varios meses al año: cualquiera de los tres, pero con el sistema de filtración y un timer '
  'bien dimensionados, que es lo que realmente decide en qué estado la encuentra al volver.'),
 ('El costo real del acabado no es el precio por metro',
  'Entre chukum y mosaico la diferencia en el presupuesto inicial suele ser menor de lo que la gente espera; la '
  'diferencia real aparece a los cinco años. El chukum se resella cada 4–6 años y el trabajo es de superficie '
  'completa. El mosaico no se resella, pero la junta se degrada y se repone por tramos. El pebble es el más estable '
  'de los tres y el más caro de retirar si algún día se quiere cambiar de estilo. Conviene decidir con el ciclo de '
  'mantenimiento a la vista y no solo con la foto de referencia.')]

OPER = [
 ('Mantenimiento: lo que nadie cotiza por adelantado',
  'Una alberca residencial de 4×8 m cuesta entre $1,500 y $3,500 MXN al mes en producto químico, electricidad y '
  'servicio, según si está en uso continuo o cerrada por temporadas. Súmele el resellado del acabado según el '
  'material y el cambio de arena del filtro cada 4–6 años. En casa de renta el número sube porque la carga de '
  'bañistas es otra y la frecuencia de servicio pasa a semanal o dos veces por semana.'),
 ('Vivir con la alberca todo el año',
  'La temporada de lluvias diluye la química y mete materia orgánica: hay que subir la frecuencia de revisión entre '
  'junio y octubre. En temporada de huracanes la alberca no se vacía — el vaso vacío es justo el que corre riesgo por '
  'flotación y por presión del terreno saturado —; se baja el nivel parcialmente, se protege el equipo y se '
  'sobreclorina. Y si la casa se cierra por meses, el timer y una visita quincenal cuestan mucho menos que recuperar '
  'un agua perdida.'),
 ('Garantía y qué cubre en realidad',
  'Damos garantía estructural del vaso y garantía sobre la instalación hidráulica; los equipos van con la garantía del '
  'fabricante, que es la que responde por bomba, filtro y calentador. Lo que ninguna garantía cubre es el acabado '
  'maltratado por química mal llevada: agua fuera de rango ataca el chukum y la junta del mosaico, y es el motivo más '
  'frecuente de un acabado arruinado antes de tiempo. Por eso entregamos con la química estabilizada y con la rutina '
  'por escrito.')]

FAQ_COMMON = [
 ('¿Cuánto tarda la construcción de una alberca?',
  'Entre 6 y 12 semanas para una alberca residencial, contadas desde la excavación hasta el arranque del equipo. La '
  'excavación en roca y el curado del concreto son los tramos que no se pueden acelerar; el acabado y el equipo sí '
  'admiten traslape con el resto de la obra.'),
 ('¿Se puede construir la alberca después de la casa?',
  'Sí, y es muy común. Encarece el acceso de maquinaria y obliga a proteger acabados ya terminados, así que sale entre '
  '10% y 20% por encima de haberla hecho junto con la obra. Si la casa ya está proyectada, conviene al menos dejar '
  'preparadas la tubería y la acometida eléctrica.'),
 ('¿El precio incluye el deck y la iluminación?',
  'No. El rango cotizado es la alberca terminada y funcionando: vaso, instalación, cuarto de máquinas, acabado y '
  'arranque. Deck perimetral, iluminación escénica, calentador, sistema de sal y cascadas se cotizan aparte porque no '
  'todos los proyectos los llevan.'),
 ('¿Trabajan con contrato a precio fijo?',
  'Sí, por partidas y con calendario de pagos ligado a avance verificable. Los dos conceptos que se manejan como '
  'variable declarada son la excavación en roca dura y cualquier hallazgo de manto freático alto, porque dependen de '
  'lo que aparezca al abrir.')]


CITIES = {
'cancun': dict(
  name='Cancún', muni='Benito Juárez', factor=1.0, v=0,
  ctx=('Cancún concentra tres mercados de alberca que no se parecen entre sí. En las residenciales del norte y del '
       'corredor a Puerto Juárez — Residencial Cumbres, Lagos del Sol, Villa Magna, Aqua — domina la alberca familiar '
       'de concreto con deck y área de asador. En la Zona Hotelera y en Puerto Cancún manda el proyecto de condominio: '
       'rooftop con refuerzo estructural, alberca de borde infinito hacia la laguna y cumplimiento normativo de alberca '
       'de uso público. Y en la franja de renta vacacional crece el plunge pool en lote chico, que es la inversión que '
       'más rápido se paga en tarifa por noche.'),
  local=('Benito Juárez pide licencia de construcción para la alberca cuando forma parte de obra nueva o cuando implica '
         'estructura, y en condominio se suma el visto bueno del régimen. Si la alberca es de uso público o compartido '
         '— hotel, club, amenidad de torre — entra además el cumplimiento sanitario, con registro de parámetros, '
         'recirculación mínima y las protecciones antiatrapamiento en succión. En Zona Hotelera hay que contar con el '
         'condicionante de zona federal y con el manto freático alto tan cerca del mar.'),
  faq=[('¿Cuánto cuesta una alberca en Cancún?',
        'Una alberca residencial estándar de 4×8 m con equipo y acabado terminado va de $14,000 a $22,000 USD. Un '
        'plunge pool de 2×4 m para lote chico o rooftop arranca en $6,500 USD, y una infinity de vista sube a un rango '
        'de $22,000 a $45,000 USD según desnivel y estructura.'),
       ('¿Construyen albercas en condominio y Zona Hotelera?',
        'Sí. Es obra distinta a la de casa: hay que verificar la capacidad de la losa con el ingeniero estructural, '
        'coordinar maniobras y horarios con la administración, y en amenidad compartida cumplir la normativa de alberca '
        'de uso público, incluidas las protecciones antiatrapamiento.'),
       ('¿El manto freático es problema en la Zona Hotelera?',
        'Es la condición que más hay que respetar. Con el nivel freático alto el vaso vacío puede flotar, así que se '
        'instala válvula hidrostática y se define por escrito el procedimiento de vaciado. No es un impedimento, pero '
        'sí una parte del diseño que no se puede omitir.')]),

'playa-del-carmen': dict(
  name='Playa del Carmen', muni='Solidaridad', factor=1.0, v=1,
  ctx=('Es nuestra base de operación, y donde más albercas hemos entregado: Playacar, Centro, Ejidal, Corasol, '
       'Selvamar y los desarrollos sobre la 30. El proyecto típico aquí es la alberca de patio con terraza integrada '
       'en casa residencial, y el segundo más frecuente es el rooftop con plunge pool en departamento de inversión, '
       'donde la alberca es literalmente lo que sostiene la tarifa por noche. En Playacar el condicionante suele ser '
       'el reglamento del fraccionamiento; en Centro y Ejidal, el tamaño del lote.'),
  local=('Solidaridad es de los municipios más ágiles de la región para el trámite de alberca dentro de obra nueva: '
         'dos a cuatro semanas cuando el expediente va completo. En Playacar se suma la revisión del fraccionamiento, '
         'que regula alturas, retiros y a veces hasta el color del acabado exterior. En obra de departamento en '
         'condominio, el visto bueno del régimen y el dictamen estructural de la losa son previos a cualquier '
         'excavación o refuerzo.'),
  faq=[('¿Cuánto cuesta una alberca en Playa del Carmen?',
        'La estándar de concreto de 4×8 m va de $14,000 a $22,000 USD terminada y funcionando. El plunge pool de '
        'rooftop, que es lo más pedido en departamento de inversión, arranca en $6,500 USD sin contar el refuerzo '
        'estructural, que se cotiza aparte según lo que diga el cálculo de la losa.'),
       ('¿Hacen albercas de lujo y desbordantes?',
        'Sí — es una línea propia. Desbordantes, de cristal, con spa integrado y con acabado premium. El detalle de '
        'ese trabajo está en nuestra página de albercas de lujo en Playa del Carmen.'),
       ('¿Cuánto tarda el permiso en Solidaridad?',
        'De dos a cuatro semanas con el expediente completo, y es el trámite más rápido de la región. Se alarga cuando '
        'falta el uso de suelo actualizado o cuando el predio tiene alguna observación previa sin resolver.')]),

'tulum': dict(
  name='Tulum', muni='Tulum', factor=1.05, v=2,
  ctx=('Tulum es la capital del acabado chukum y de la alberca de forma orgánica: entrada tipo playa, borde de piedra '
       'natural, integración con la selva y muy poca geometría dura. La demanda se reparte entre la villa de renta en '
       'Aldea Zamá, La Veleta y Región 15, y el proyecto de hotel boutique con alberca de uso público. La diferencia '
       'técnica frente a Playa o Cancún no está en el vaso, está en el trámite: aquí el componente ambiental es real y '
       'condiciona el calendario de toda la obra, no solo el de la alberca.'),
  local=('En Tulum el expediente ambiental es obligatorio y la cercanía a cenote o a cavidad subterránea cambia el '
         'proyecto: hay que documentar el manejo de agua de retrolavado y de vaciado, y el vertido a suelo sin control '
         'es justo lo que detiene una obra. Se suman uso de suelo, licencia municipal y DRO. Nuestra recomendación es '
         'siempre resolver el ambiental antes de excavar, porque rehacer una alberca ya colada por una observación '
         'ambiental no tiene arreglo barato.'),
  faq=[('¿Cuánto cuesta una alberca en Tulum?',
        'Entre $14,700 y $23,100 USD la estándar de 4×8 m, con el factor de logística de la zona ya aplicado. El '
        'acabado chukum, que es lo que casi todo el mundo pide aquí, va de $800 a $1,500 MXN/m² y está incluido en ese '
        'rango cuando se cotiza como alberca terminada.'),
       ('¿Necesito permiso ambiental para una alberca en Tulum?',
        'En la práctica sí, y más si el predio está cerca de cenote o de cavidad. Lo que se revisa es el manejo del '
        'agua de retrolavado y de vaciado, no la alberca en sí. Gestionamos el expediente como parte del proyecto.'),
       ('¿El chukum aguanta en alberca de renta?',
        'Aguanta bien si la química del agua se mantiene en rango y se resella cada 4–6 años. Lo que lo arruina antes '
        'de tiempo es el agua fuera de parámetros entre huéspedes, no el uso. En rotación muy alta solemos recomendar '
        'pebble por lo antiderrapante.')]),

'puerto-morelos': dict(
  name='Puerto Morelos', muni='Puerto Morelos', factor=1.05, v=0,
  ctx=('Puerto Morelos trabaja en dos frentes: el pueblo y la zona de villas frente al mar, donde la alberca es de casa '
       'residencial o de renta con vista, y el corredor de la Ruta de los Cenotes hacia el poniente, donde los predios '
       'son grandes y el proyecto tiende a alberca de mayor tamaño con área exterior completa. Es también el municipio '
       'donde el componente ambiental pesa más de toda la costa, por el parque nacional del arrecife.'),
  local=('El Parque Nacional Arrecife de Puerto Morelos condiciona la franja costera y obliga a un cuidado explícito en '
         'el manejo de descargas: agua de retrolavado, vaciado y químicos no pueden ir a suelo sin control. Sobre la '
         'Ruta de los Cenotes el condicionante es la cavidad subterránea. En los dos casos el expediente ambiental se '
         'resuelve antes de excavar, junto con uso de suelo y licencia municipal.'),
  faq=[('¿Se puede construir alberca cerca del arrecife?',
        'Sí, con el manejo de descargas documentado. Lo que la autoridad revisa es a dónde va el agua de retrolavado y '
        'de vaciado, y ese punto se resuelve en el proyecto con un sistema de disposición controlada, no improvisando '
        'al final de la obra.'),
       ('¿Cuánto cuesta una alberca en Puerto Morelos?',
        'La estándar de 4×8 m va de $14,700 a $23,100 USD, con el factor de traslado ya incluido. En los predios '
        'grandes de la Ruta de los Cenotes el proyecto suele irse al rango de 5×10 m, entre $23,100 y $34,700 USD.'),
       ('¿Trabajan sobre la Ruta de los Cenotes?',
        'Sí. El punto técnico ahí es la cavidad subterránea: antes de definir la posición del vaso conviene un '
        'reconocimiento del predio, porque una cavidad bajo la excavación cambia la cimentación de la alberca.')]),

'puerto-aventuras': dict(
  name='Puerto Aventuras', muni='Solidaridad', factor=1.05, v=1,
  ctx=('Puerto Aventuras es un desarrollo cerrado con marina, y eso define el trabajo: casi todas las albercas son de '
       'casa o villa dentro del fraccionamiento, con reglamento interno que revisa proyecto, horarios de obra y acceso '
       'de material antes de que empiece nada. Muchas de las casas dan a los canales de la marina, y ahí el nivel '
       'freático y la cercanía del agua salada mandan sobre el diseño del vaso y sobre la especificación de todo el '
       'herraje.'),
  local=('El trámite municipal es el de Solidaridad, pero el filtro real es la administración del desarrollo: '
         'aprobación de proyecto, ventana de horarios, ruta de acceso para material y maquinaria, y depósito de '
         'garantía en varios casos. Conviene meter el proyecto a revisión interna en paralelo con el trámite '
         'municipal, porque son dos tiempos independientes y el del fraccionamiento suele ser el que manda.'),
  faq=[('¿Cómo funciona el permiso dentro de Puerto Aventuras?',
        'Van dos vías en paralelo: la licencia municipal de Solidaridad y la aprobación de la administración del '
        'desarrollo, que revisa proyecto, horarios y acceso. Gestionamos las dos, y en la práctica la interna es la '
        'que fija el arranque real de obra.'),
       ('¿La cercanía a la marina afecta la alberca?',
        'Sí, en dos puntos. El nivel freático alto obliga a válvula hidrostática y a un procedimiento de vaciado, y el '
        'ambiente salino obliga a herrajes y luminarias en inoxidable 316 o material no ferroso. Con eso resuelto, la '
        'alberca se comporta igual que tierra adentro.'),
       ('¿Cuánto cuesta una alberca en Puerto Aventuras?',
        'Entre $14,700 y $23,100 USD la estándar de 4×8 m. En las villas de canal es frecuente el rango de 5×10 m con '
        'borde desbordante hacia el agua, que va de $23,100 a $47,300 USD según el desnivel disponible.')]),

'akumal': dict(
  name='Akumal', muni='Tulum', factor=1.10, v=2,
  ctx=('Akumal es mercado de villa de renta de gama alta — Akumal Norte, Aventuras Akumal, Media Luna Bay, Jade Bay — '
       'donde la alberca no es un extra sino el argumento de venta de la propiedad. El proyecto típico es alberca de '
       '5×10 m o desbordante con vista a la bahía, con deck amplio y área de sombra. La bahía es zona de anidación de '
       'tortuga, lo que condiciona la iluminación exterior del conjunto y, con ella, el diseño de la luz de la alberca.'),
  local=('Akumal pertenece al municipio de Tulum, así que aplica el mismo expediente ambiental, con el agravante de la '
         'franja costera y de la protección de la bahía. La iluminación exterior está sujeta a criterios por la '
         'anidación de tortuga: luz cálida, baja y dirigida hacia abajo. Es un detalle que hay que resolver en el '
         'proyecto de la alberca, no en la compra de luminarias al final.'),
  faq=[('¿Cuánto cuesta una alberca en Akumal?',
        'La estándar de 4×8 m va de $15,400 a $24,200 USD con el factor de traslado incluido. Lo más pedido aquí es la '
        'desbordante con vista a la bahía, en un rango de $24,200 a $49,500 USD según desnivel y estructura.'),
       ('¿Hay restricción de iluminación por la tortuga?',
        'Sí, en la franja cercana a la bahía: luz cálida, montada baja y dirigida hacia abajo, sin haces hacia la '
        'playa. Se resuelve en el proyecto eléctrico de la alberca y del jardín, y no encarece de forma significativa '
        'si se define desde el principio.'),
       ('¿Conviene alberca desbordante en villa de renta?',
        'En Akumal sí, porque es lo que sostiene la tarifa por noche frente a la competencia. Técnicamente exige '
        'desnivel aprovechable y un tanque de compensación bien dimensionado; sin desnivel real, una desbordante '
        'forzada da problemas de nivel y de consumo.')]),

'bacalar': dict(
  name='Bacalar', muni='Bacalar', factor=1.15, v=0,
  ctx=('Bacalar juega con reglas propias. La laguna de los siete colores debe su color a estromatolitos vivos, y por '
       'eso el manejo de cualquier descarga cerca de la orilla está bajo vigilancia real, no nominal. La demanda es de '
       'cabaña y hotel boutique más que de casa residencial, y el proyecto que mejor funciona es la alberca chica o '
       'mediana bien integrada al terreno, con disposición de agua controlada y lejos del borde de la laguna.'),
  local=('El municipio y la autoridad ambiental revisan con lupa la descarga de agua de retrolavado y de vaciado en '
         'predios cercanos a la laguna: es el punto que detiene proyectos. La distancia al borde, el sistema de '
         'disposición y el tipo de químico en uso forman parte del expediente. Recomendamos clorinación salina o '
         'sistemas de bajo residuo, y en varios predios la solución correcta es alejar el vaso de la orilla aunque '
         'cueste vista.'),
  faq=[('¿Se puede construir alberca frente a la laguna de Bacalar?',
        'Depende de la distancia al borde y del manejo de descargas, que es lo que realmente se revisa. Los '
        'estromatolitos son organismos vivos y el vertido de agua tratada químicamente cerca de la orilla es el punto '
        'que detiene un proyecto. Se resuelve con disposición controlada y, a veces, alejando el vaso.'),
       ('¿Cuánto cuesta una alberca en Bacalar?',
        'Entre $16,100 y $25,300 USD la estándar de 4×8 m, con el factor de distancia y traslado ya aplicado. Bacalar '
        'está fuera del corredor Cancún–Playa y el flete de material pesa más en el total que en el resto de la costa.'),
       ('¿Qué sistema de tratamiento recomiendan en Bacalar?',
        'Clorinación salina o sistemas de bajo residuo, con disposición controlada del retrolavado. No es solo criterio '
        'ambiental: es lo que hace que el expediente pase sin observaciones y lo que evita un problema con la '
        'autoridad después de entregada la obra.')]),
}


def make(slug_city, d, order):
    city = d['name']
    v, vt, vf, vo = d['v'], (order + 1) % 3, (order + 2) % 3, order % 3
    secs = [
        ('Construcción de albercas en %s' % city, d['ctx']),
        SCOPE[v],
        TECH[vt],
        ('Precios de alberca 2026 en %s' % city,
         'Rangos en dólares para alberca terminada y funcionando: vaso, instalación hidráulica, cuarto de máquinas, '
         'acabado y arranque del equipo. No incluyen deck perimetral, iluminación escénica, calentador ni cascadas, '
         'que se cotizan por separado. En las plazas fuera del corredor Cancún–Playa el flete de material va '
         'identificado como partida propia en lugar de repartido a escondidas en los precios unitarios.'),
        FINISH[vf],
        ('Trámites y normativa: %s' % d['muni'], d['local']),
        OPER[vo],
    ]
    faq = d['faq'] + FAQ_COMMON
    sibs = list(CITIES.items())
    sibs = [sibs[(order + k) % len(sibs)] for k in (1, 2, 3)]
    links = [('/construccion-albercas/', 'Construcción de albercas en la Riviera Maya')]
    links += [('/albercas-%s/' % s, 'Albercas en %s' % c['name']) for s, c in sibs]
    links += [('/cuanto-cuesta-una-alberca/', 'Cuánto cuesta una alberca'),
              ('/albercas-de-lujo-playa-del-carmen/', 'Albercas de lujo'),
              ('/permisos-licencias-construccion-riviera-maya/', 'Permisos y licencias'),
              ('/supervision-de-obra/', 'Supervisión de obra')]
    t_long = 'Albercas en %s: Precios 2026 y Construcción | Recrea' % city
    t_short = 'Albercas en %s | Precios 2026 | Recrea' % city
    return dict(
        title=t_long if len(t_long) <= 65 else t_short,
        desc=('Construcción de albercas en %s: precios 2026 en dólares por tipo y tamaño, acabados chukum, '
              'mosaico y pebble, permisos y mantenimiento real.' % city),
        h1='Construcción de Albercas en %s' % city,
        lead=('Albercas de concreto, infinity, chukum y rooftop en %s, llave en mano: excavación, vaso, cuarto de '
              'máquinas, acabado y arranque con contrato a precio fijo.' % city),
        secs=secs,
        table=('Tipo de alberca', 'Ideal para', 'Precio 2026') + (rows_for(d['factor']),),
        faq=faq, links=links)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src = open(kw1.TPL, encoding='utf-8').read()
    built = {}
    for i, (slug_city, d) in enumerate(CITIES.items()):
        slug = 'albercas-' + slug_city
        page = make(slug_city, d, i)
        os.makedirs(slug, exist_ok=True)
        html = kw1.build(slug, page, src)
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
        built[slug] = set(tuple(body[j:j + 6]) for j in range(len(body) - 5))
        print('%-34s title %2d  desc %3d  words %d' % (slug + '/', len(page['title']), len(page['desc']), len(body)))
    ks = list(built)
    mx = max((len(built[a] & built[b]) / len(built[a] | built[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity: %.2f  (%s vs %s)' % mx)
