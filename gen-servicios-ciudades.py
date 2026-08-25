#!/usr/bin/env python3
"""Four service clusters across the nine corridor cities, plus their type pages.

Chosen from Semrush (MX) volume, not from the shape of the existing grid:

    puertas de madera        27100      remodelacion de casas      1900
    cocinas integrales       27100      remodelacion de banos      1300
    pergolas de madera        8100      alberca infinity            720
    cocinas de madera         5400      remodelacion de cocinas     590
    closets de madera         2400      carpinteria cancun          320
    cocina integral de madera 2400      carpinteria pdc             260
    deck de madera            2400      cocinas integrales cancun   210

"remodelacion de lujo" and "remodelacion integral" return nothing; the demand is
in plain "remodelación de baños / cocinas", so the premium positioning lives in the
copy and not in the URL. Baños was the largest uncovered head term on the site.

Clusters:
    banos        /remodelacion-banos-<city>/       + /remodelacion-de-banos/
    cocinas      /cocinas-integrales-<city>/       + /cocinas-de-madera/
    carpinteria  /carpinteria-<city>/              + /closets-a-medida/, /puertas-de-madera/
    infinity     /albercas-infinity-<city>/        + /albercas-infinity/

Prices are anchored to what the site already publishes so no two layers contradict:
carpentry at $3,000 MXN/ml for kitchens and $2,500 MXN/ml for closets from
/carpinteria-y-herreria-playa-del-carmen/, kitchen remodels $80,000–$700,000 MXN from
/remodelacion-cocina-playa-del-carmen/, whole-house remodel $4,500–$18,000 MXN/m² from
/remodelacion-casas-cancun/, and the pool ranges from /construccion-albercas/. Bathroom
figures are derived from the whole-house m² anchor and stated as such on the page.

Every city carries its own zones, its own technical quirk and its own FAQ entry in
every cluster; shared sections rotate between three written variants. Pairwise
similarity is printed per cluster and must stay well under 0.55.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'kw1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-keyword-pages.py'))
kw1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kw1)


def mxn(v):
    return '$' + format(int(round(v, -3)), ',d') + ' MXN'


def usd(v):
    return '$' + format(int(round(v, -2)), ',d')


CITIES = {
'cancun': dict(name='Cancún', muni='Benito Juárez', factor=1.00,
  zones='Supermanzanas, Residencial Cumbres, Lagos del Sol, Villa Magna, Puerto Cancún y la Zona Hotelera',
  quirk='el salitre de la Zona Hotelera, que obliga a herrajes inoxidables en todo lo que quede expuesto'),
'playa-del-carmen': dict(name='Playa del Carmen', muni='Solidaridad', factor=1.00,
  zones='Playacar, Centro, Ejidal, Corasol, Selvamar y el corredor de la 30',
  quirk='el trámite municipal más ágil de la región, de dos a cuatro semanas con expediente completo'),
'tulum': dict(name='Tulum', muni='Tulum', factor=1.06,
  zones='Aldea Zamá, La Veleta, Región 15, Región 8 y Tulum Country Club',
  quirk='el expediente ambiental, que en este municipio condiciona el calendario de toda la obra'),
'puerto-morelos': dict(name='Puerto Morelos', muni='Puerto Morelos', factor=1.05,
  zones='el pueblo, la zona de villas frente al mar y el corredor de la Ruta de los Cenotes',
  quirk='el parque nacional del arrecife, que hace del manejo de residuos y descargas un punto revisable'),
'puerto-aventuras': dict(name='Puerto Aventuras', muni='Solidaridad', factor=1.03,
  zones='las villas de canal, la marina y las secciones residenciales del fraccionamiento',
  quirk='el reglamento interno del desarrollo, que fija horarios de obra y ruta de acceso antes que el municipio'),
'akumal': dict(name='Akumal', muni='Tulum', factor=1.06,
  zones='Akumal Norte, Akumal Pueblo, Aventuras Akumal, Media Luna Bay y Jade Bay',
  quirk='la bahía de anidación de tortuga, que regula la iluminación exterior de todo el conjunto'),
'cozumel': dict(name='Cozumel', muni='Cozumel', factor=1.16,
  zones='San Miguel, la zona norte de hoteles y la costa oriente',
  quirk='la logística insular: todo el material cruza en ferry y el flete se cotiza como partida aparte'),
'isla-mujeres': dict(name='Isla Mujeres', muni='Isla Mujeres', factor=1.15,
  zones='el centro de la isla, la zona de Playa Norte y la porción continental de Costa Mujeres',
  quirk='el ancho de calle en la isla, que limita el tamaño de pieza que se puede meter armada'),
'bacalar': dict(name='Bacalar', muni='Bacalar', factor=1.15,
  zones='el pueblo, la ribera de la laguna y el corredor hacia la carretera federal',
  quirk='la distancia al corredor Cancún–Playa, que pesa en el flete más que en el resto de la costa'),
}


# ---------------------------------------------------------------- baños ----
BANOS = dict(
 slug='remodelacion-banos-%s',
 title='Remodelación de Baños en %s: Precios 2026 | Recrea',
 desc=('Remodelación de baños en %s: precios 2026 por nivel, impermeabilización, '
       'plomería, cancelería y plazos reales. Presupuesto cerrado.'),
 h1='Remodelación de Baños en %s',
 lead=('Remodelamos baños en %s de principio a fin: demolición, plomería, '
       'impermeabilización, azulejo, mueble a medida y cancelería, con presupuesto cerrado por partidas.'),
 head=('Nivel de remodelación', 'Qué incluye', 'Costo 2026'),
 rows=[('Baño básico (3–5 m²)', 'Azulejo, muebles de línea, grifería estándar', 45000, 90000),
       ('Baño medio (4–6 m²)', 'Mueble a medida, cubierta, regadera de cristal', 90000, 180000),
       ('Baño principal (6–10 m²)', 'Doble lavabo, nicho, cancel a medida, iluminación', 180000, 320000),
       ('Baño premium / master', 'Chukum o piedra natural, tina exenta, domótica', 320000, 650000),
       ('Medio baño / visitas', 'Renovación completa de superficie e instalación', 28000, 60000),
       ('Solo cambio de acabados', 'Azulejo, grifería y muebles sin tocar instalación', 22000, 55000)],
 scope=[
  ('Qué incluye una remodelación de baño llave en mano',
   'Demolición y retiro de escombro, revisión y cambio de la tubería hidráulica y sanitaria que quede a la vista, '
   'impermeabilización de la zona húmeda, plafón e instalación eléctrica, azulejo o recubrimiento, mueble de lavabo, '
   'cubierta, grifería, cancelería de cristal y la limpieza final con todo probado. Fuera del precio quedan la tina '
   'exenta, la domótica y el calentador si hay que sustituirlo, que se cotizan por separado.'),
  ('Alcance: de la demolición a la entrega probada',
   'El trabajo empieza por abrir y ver: en casa de más de diez años la tubería vieja y el registro de la losa deciden '
   'el alcance real, no el catálogo de azulejo. Después van impermeabilización, instalación nueva, recubrimientos, '
   'muebles y cancelería. Entregamos con prueba de escurrimiento hecha y con las llaves probadas una por una, que es '
   'lo que evita la llamada a los tres meses.'),
  ('Baño completo, medio baño o solo acabados',
   'Tres alcances distintos y tres presupuestos distintos. Completo: se abre hasta la instalación y se rehace todo, '
   'que es lo único que resuelve una humedad de fondo. Medio baño de visitas: superficie e instalación en un espacio '
   'chico, la obra más rápida de la casa. Solo acabados: se conservan tubería y salidas y se cambian azulejo, muebles '
   'y grifería — sale entre 35% y 50% de un baño completo y tiene sentido cuando la instalación está sana.')],
 tech=[
  ('Impermeabilización: donde se decide si el baño dura',
   'Es la partida que menos se ve y la que más reclamaciones evita. La zona húmeda lleva membrana continua bajo el '
   'azulejo, con el desarrollo subido en muro al menos 20 cm y sellado en el encuentro piso-muro y en la penetración '
   'del desagüe. En losa de entrepiso, una regadera mal impermeabilizada aparece como mancha en el plafón del piso de '
   'abajo entre seis meses y dos años después. Es también el motivo por el que un presupuesto muy barato suele serlo: '
   'la membrana es lo primero que se recorta.'),
  ('Plomería vieja, presión y agua dura',
   'En obra de más de diez años lo normal es encontrar tubería galvanizada picada o PVC con uniones cansadas: si se '
   'renueva el acabado sin cambiar la instalación, la fuga llega después y hay que romper lo nuevo. La presión es el '
   'otro punto: las regaderas de lluvia grandes necesitan caudal y presión reales, y sin bomba o sin hidroneumático '
   'quedan en un chorro decepcionante. Y el agua de esta costa es dura: incrusta grifería y aireadores, así que '
   'conviene grifería de cartucho cerámico y no la más barata del anaquel.'),
  ('Ventilación, humedad y qué materiales aguantan aquí',
   'Un baño interior sin ventilación mecánica en clima húmedo desarrolla moho en la junta y sobre el plafón en menos '
   'de dos temporadas: el extractor no es opcional, es parte de la obra. En materiales, funcionan porcelánico '
   'rectificado, piedra natural sellada y chukum en zona seca; no funcionan el tablaroca estándar en zona húmeda, '
   'que hay que sustituir por tablacemento, ni el herraje de acero común, que se oxida a la vista en meses.')],
 extra=[
  ('Plazos reales y cómo vivir la obra',
   'Un baño completo se entrega en tres a cinco semanas y un medio baño en una a dos. El tramo que no se puede '
   'acelerar es el curado del firme y la impermeabilización antes de azulejar. Si es el único baño de la casa, se '
   'planea por etapas para dejarlo utilizable la mayor parte del tiempo, y en departamento habitado se acuerda antes '
   'la ruta de escombro y el horario permitido por la administración.'),
  ('Qué mueve el presupuesto hacia arriba',
   'Mover el desagüe de lugar, que obliga a tocar losa o a levantar el nivel de piso. Pasar de regadera a tina exenta, '
   'que suma peso, alimentación y desagüe nuevos. Cambiar a piedra natural, por costo de material y por el corte y el '
   'sellado. Y la cancelería a medida en cristal templado, que en un baño irregular vale bastante más que un cancel '
   'de línea. Estos cuatro conceptos explican casi toda la diferencia entre un baño medio y uno premium.'),
  ('Presupuesto cerrado y garantía',
   'Trabajamos con presupuesto cerrado por partidas y calendario de pagos ligado a avance verificable. Los dos '
   'conceptos que se manejan como variable declarada son el estado de la instalación oculta y el de la losa, porque '
   'dependen de lo que aparezca al demoler. La garantía cubre impermeabilización e instalación; los muebles y la '
   'grifería van con la garantía del fabricante.')],
 faq_city={
  'cancun': ('¿Cuánto cuesta remodelar un baño en Cancún?',
     'Un baño básico de 3 a 5 m² va de $45,000 a $90,000 MXN, y un baño principal completo de $180,000 a $320,000 MXN. '
     'En departamento de Zona Hotelera o Puerto Cancún hay que sumar la maniobra de escombro y el horario restringido '
     'que fija la administración, que alarga el plazo más de lo que sube el costo.'),
  'playa-del-carmen': ('¿Cuánto tarda remodelar un baño en Playa del Carmen?',
     'De tres a cinco semanas un baño completo y de una a dos un medio baño. Al ser nuestra base, el suministro de '
     'material y el taller están a minutos de obra, y eso es lo que hace que el plazo se cumpla: en Playa el retraso '
     'típico no es de mano de obra, es de material que no llegó.'),
  'tulum': ('¿Se puede hacer un baño con acabado chukum en Tulum?',
     'Sí, y es lo más pedido aquí. El chukum va en zona seca y en muro de regadera bien sellado, nunca como piso de '
     'plato de ducha sin tratamiento antiderrapante. Se resella cada cuatro a seis años. En baño de villa de renta '
     'solemos combinarlo con porcelánico en el piso por el tránsito.'),
  'puerto-morelos': ('¿Qué se hace con el escombro de una remodelación en Puerto Morelos?',
     'Se retira a sitio autorizado y se documenta. En este municipio el manejo de residuos de obra sí se revisa por la '
     'condición del parque nacional del arrecife, y dejar escombro en predio o en la vía es el tipo de detalle que '
     'genera una observación. Va incluido en nuestro presupuesto como partida propia.'),
  'puerto-aventuras': ('¿Qué permisos pide el fraccionamiento en Puerto Aventuras?',
     'Para remodelación interior no hay licencia municipal, pero sí aprobación de la administración del desarrollo: '
     'horario de obra, ruta de acceso, control de personal y en varios casos depósito de garantía. Es el trámite que '
     'marca el arranque real, y lo gestionamos nosotros antes de mover material.'),
  'akumal': ('¿Trabajan en villas de renta ocupadas en Akumal?',
     'Sí, y se planea por ventanas entre reservas. Un baño completo necesita de tres a cinco semanas continuas, así '
     'que lo normal es programarlo en temporada baja. Si la villa tiene varios baños, se atacan por turnos para que la '
     'casa siga rentando durante la obra.'),
  'cozumel': ('¿Cuánto encarece la remodelación de baño en Cozumel?',
     'Alrededor de 16% frente al continente, y casi todo es flete: material y muebles cruzan en ferry. Por eso '
     'cotizamos el traslado como partida aparte en lugar de repartirlo en los precios unitarios, y compramos el '
     'material del baño completo en un solo envío en vez de por viajes sueltos.'),
  'isla-mujeres': ('¿Cabe un mueble de baño a medida por las calles de Isla Mujeres?',
     'Depende de la pieza. En la isla el ancho de calle limita lo que se puede meter armado, así que los muebles '
     'grandes y la cancelería se despiezan en taller y se ensamblan en sitio. En Costa Mujeres, del lado continental, '
     'no hay esa restricción y se trabaja como obra normal de corredor.'),
  'bacalar': ('¿Cuánto cuesta remodelar un baño en Bacalar?',
     'De $51,000 a $103,000 MXN el baño básico, con el factor de distancia ya aplicado. Bacalar está fuera del '
     'corredor Cancún–Playa y el flete pesa más que en el resto de la costa, así que conviene agrupar la compra de '
     'material de todos los baños de la casa en un solo envío.')},
 faq_common=[
  ('¿Necesito permiso municipal para remodelar un baño?',
   'Para remodelación interior que no toca estructura ni fachada, normalmente no. Sí lo necesita cuando se modifica '
   'estructura, se abre en muro de carga o cambia el uso de un espacio. En condominio, en cambio, casi siempre hace '
   'falta el visto bueno de la administración, que revisa horarios, ruta de escombro y afectación a vecinos.'),
  ('¿Puedo quedarme en la casa durante la obra?',
   'Sí en casa con más de un baño. Se aísla la zona, se define ruta de escombro y se protege el resto de la vivienda. '
   'Si es el único baño, se trabaja por etapas para dejarlo utilizable la mayor parte del tiempo, lo que alarga el '
   'plazo entre cinco y diez días.'),
  ('¿El precio incluye muebles y grifería?',
   'Sí, dentro del rango cotizado y con la marca y el modelo especificados en el presupuesto. Si el cliente prefiere '
   'una línea distinta, se ajusta la partida. Lo que se cotiza aparte es la tina exenta, la domótica y el calentador '
   'nuevo cuando hay que sustituirlo.'),
  ('¿Qué garantía dan?',
   'Garantía por escrito sobre impermeabilización e instalación hidrosanitaria, que es donde se juegan los problemas '
   'reales. Muebles, grifería y cancelería van con la garantía de su fabricante. La entrega incluye prueba de '
   'escurrimiento y revisión de cada salida.')],
 links=[('/remodelacion-de-banos/', 'Remodelación de baños: precios y proceso'),
        ('/remodelacion-riviera-maya/', 'Remodelación en la Riviera Maya'),
        ('/cocinas-integrales-cancun/', 'Cocinas integrales'),
        ('/carpinteria-cancun/', 'Carpintería a medida'),
        ('/supervision-de-obra/', 'Supervisión de obra')],
 unit='mxn')


# -------------------------------------------------------------- cocinas ----
COCINAS = dict(
 slug='cocinas-integrales-%s',
 title='Cocinas Integrales en %s: Precios 2026 | Recrea',
 desc=('Cocinas integrales a medida en %s: precios 2026 por metro lineal, materiales '
       'que aguantan el clima, cubiertas y plazos. Taller propio.'),
 h1='Cocinas Integrales a Medida en %s',
 lead=('Diseñamos y fabricamos cocinas integrales a medida en %s con taller propio: '
       'gabinetes, cubierta, herrajes e instalación, sin intermediarios.'),
 head=('Tipo de cocina', 'Materiales', 'Costo 2026 por metro lineal'),
 rows=[('Melamina de línea', 'Melamina 16 mm, herraje estándar, cubierta laminada', 3000, 5500),
       ('Melamina premium / MDF lacado', 'Canto ABS, herraje con cierre suave', 5500, 9000),
       ('Madera sólida o enchapada', 'Tzalam, parota o chapa fina sobre MDF', 9000, 16000),
       ('Cubierta de cuarzo o granito', 'Suministro e instalación, por metro lineal', 4500, 12000),
       ('Isla o península', 'Estructura, cubierta y conexiones, por pieza', 45000, 160000),
       ('Cocina completa llave en mano', 'Proyecto, fabricación, instalación y arranque', 95000, 700000)],
 scope=[
  ('Qué entra en una cocina integral a medida',
   'Levantamiento en sitio y proyecto de despiece, fabricación en taller propio, herrajes, cubierta, instalación, '
   'ajuste de puertas y cajones, y la conexión de tarja y campana. Fuera del precio quedan los electrodomésticos, el '
   'trabajo eléctrico e hidráulico si hay que mover salidas, y el recubrimiento del muro entre cubierta y alacena. '
   'Todo eso se cotiza por partida para que se vea qué es mueble y qué es obra.'),
  ('Del levantamiento a la instalación',
   'La medida se toma en sitio y sobre muro terminado, nunca sobre plano, porque un muro fuera de escuadra de dos '
   'centímetros arruina una cocina de catálogo. Con la medida real se hace el despiece, se fabrica en taller y se '
   'instala nivelando sobre patas regulables. La diferencia entre una cocina a medida y una modular armada en sitio '
   'está justo ahí: en la tolerancia que absorbe el mueble en lugar de dejarla a la vista.'),
  ('Cocina nueva, cambio de frentes o solo cubierta',
   'Tres trabajos distintos. Cocina nueva completa: proyecto, fabricación e instalación desde cero. Cambio de frentes '
   'y herrajes conservando los cajones: renueva por completo el aspecto por una fracción del costo, y solo funciona '
   'si la estructura está sana y a escuadra. Cambio de cubierta solamente: retiro, plantilla, corte y colocación, con '
   'el detalle del sellado en el encuentro con la tarja, que es donde entra el agua que hincha un mueble.')],
 tech=[
  ('Humedad, sal y por qué aquí no sirve cualquier tablero',
   'El enemigo de una cocina en esta costa no es el uso, es la humedad ambiente sostenida más la sal en la franja '
   'costera. El aglomerado corriente hincha por el canto en cuanto entra agua y ya no vuelve. Trabajamos melamina de '
   '16 mm con canto ABS pegado — no el canto de papel que se despega en un año — y en zona de tarja usamos tablero '
   'hidrófugo. Los herrajes van con recubrimiento anticorrosión, y en casa a menos de un kilómetro del mar, '
   'directamente en inoxidable: una bisagra común se traba en dos temporadas.'),
  ('Cubiertas: cuarzo, granito, concreto o madera',
   'El cuarzo es el estándar sensato para cocina de uso diario: no poroso, no necesita sellado y resiste manchas. El '
   'granito aguanta más calor directo pero es poroso y hay que sellarlo. El concreto pulido da el aspecto que mucha '
   'gente busca aquí y es el que más mantenimiento pide, porque se mancha con ácido y con aceite. La madera funciona '
   'de barra o de isla decorativa, no de zona de trabajo húmeda. La elección cambia el presupuesto por metro lineal '
   'más que casi cualquier otra decisión de la cocina.'),
  ('Distribución, ventilación y el error más caro',
   'La distribución se resuelve antes que el estilo: triángulo de trabajo entre tarja, cocción y refrigerador, y '
   'circulación libre de al menos noventa centímetros frente a los muebles. El error que más cuesta corregir es '
   'colocar la campana sin salida real al exterior; una campana de recirculación en clima húmedo deja la grasa en el '
   'ambiente y con ella el problema de mantenimiento de toda la cocina. Si no hay ducto posible, eso condiciona dónde '
   'puede ir la cocción, y conviene saberlo antes de fabricar.')],
 extra=[
  ('Precios por metro lineal y qué significa eso',
   'Cotizar por metro lineal es la forma honesta de comparar: es el largo de mueble bajo con su cubierta y su alacena '
   'correspondiente. Una cocina de seis metros lineales en melamina premium entra en un rango muy distinto a la misma '
   'cocina en madera sólida, y la diferencia está en el tablero y en el herraje, no en el diseño. Las islas se cotizan '
   'por pieza porque llevan estructura y conexiones propias.'),
  ('Plazos: por qué una cocina a medida no es inmediata',
   'De cuatro a ocho semanas entre el levantamiento y la instalación, según el material y la carga del taller. La '
   'fabricación en madera sólida y la cubierta de cuarzo con corte especial son los dos tramos largos. La instalación '
   'en sí toma de dos a cuatro días. En obra nueva conviene tomar la medida cuando el muro ya está terminado y no '
   'antes, aunque eso obligue a esperar.'),
  ('Taller propio: qué cambia en la práctica',
   'Fabricamos nosotros, así que la corrección de una pieza mal cortada se resuelve en días y no en semanas de ir y '
   'venir con un proveedor. También significa que el precio no lleva el margen del intermediario y que se puede '
   'ajustar el proyecto a un mueble raro, una columna en medio o un techo inclinado, que es exactamente lo que la '
   'cocina modular de catálogo no resuelve.')],
 faq_city={
  'cancun': ('¿Cuánto cuesta una cocina integral en Cancún?',
     'De $3,000 a $5,500 MXN por metro lineal en melamina de línea y de $9,000 a $16,000 en madera sólida o enchapada, '
     'sin cubierta. Una cocina completa llave en mano va de $95,000 a $700,000 MXN según tamaño y materiales. En la '
     'Zona Hotelera especificamos herraje inoxidable por el salitre.'),
  'playa-del-carmen': ('¿Dónde está el taller que fabrica la cocina?',
     'En Playa del Carmen, que es nuestra base. Eso permite que el cliente vea el mueble antes de instalarlo y que '
     'cualquier ajuste se resuelva el mismo día. Para obra en Playa la instalación se programa sin flete adicional.'),
  'tulum': ('¿Hacen cocinas de madera con estética de Tulum?',
     'Sí: tzalam o parota con acabado natural, frentes sin tirador y combinación con concreto pulido o chukum en la '
     'zona de barra. Es lo que más se pide en villa de renta. En cocina de uso diario recomendamos cubierta de cuarzo '
     'y dejar la madera en isla o barra, porque la humedad de trabajo continuo la castiga.'),
  'puerto-morelos': ('¿Trabajan cocinas para casa de renta en Puerto Morelos?',
     'Sí, y se especifican distinto: herraje reforzado, frentes que no marcan huella y cubierta de cuarzo, porque la '
     'rotación de huéspedes es dura con los muebles. Sale algo más caro al inicio y evita la reposición de frentes a '
     'los dos años.'),
  'puerto-aventuras': ('¿Cómo se instala una cocina dentro del fraccionamiento?',
     'Con la ventana de horario y la ruta de acceso aprobadas por la administración antes de mover material. La cocina '
     'llega despiezada del taller y se arma en sitio, lo que reduce el tiempo de maniobra dentro del desarrollo a dos '
     'o tres días.'),
  'akumal': ('¿Qué cocina conviene en villa de renta en Akumal?',
     'Melamina premium o MDF lacado con herraje de cierre suave y cubierta de cuarzo. Aguanta la rotación, se limpia '
     'fácil y no sufre con la humedad salina de la bahía. La madera sólida queda mejor en isla o barra que en el '
     'frente de trabajo.'),
  'cozumel': ('¿Cómo llega una cocina a medida a Cozumel?',
     'Fabricada y despiezada en taller, embalada por módulos y cruzada en ferry en un solo envío. El flete se cotiza '
     'como partida aparte y ronda el 16% sobre el continente. Fabricar allá pieza por pieza saldría más caro que '
     'traerla completa.'),
  'isla-mujeres': ('¿Se puede instalar una isla grande en la isla?',
     'Sí, despiezada. El límite en Isla Mujeres es el ancho de calle para meter la pieza armada, no la técnica: la '
     'isla llega en módulos y se ensambla y nivela en sitio. En Costa Mujeres no hay esa restricción.'),
  'bacalar': ('¿Cuánto cuesta una cocina integral en Bacalar?',
     'De $3,500 a $6,300 MXN por metro lineal en melamina de línea, con el factor de distancia aplicado. Conviene '
     'cerrar el proyecto completo de una vez para que la cocina viaje en un solo envío desde el taller.')},
 faq_common=[
  ('¿Cotizan por metro lineal o por cocina completa?',
   'Las dos formas. El metro lineal sirve para comparar materiales entre sí; la cocina completa llave en mano es lo '
   'que se firma, con el despiece, los herrajes y la cubierta especificados por marca y modelo en el presupuesto.'),
  ('¿Incluyen los electrodomésticos?',
   'No. El precio es del mueble, la cubierta, los herrajes y la instalación. Dejamos previstas las medidas, los huecos '
   'y las conexiones de los electrodomésticos que el cliente elija, y si se quiere, los suministramos como partida '
   'aparte al costo más manejo.'),
  ('¿Cuánto dura una cocina a medida en este clima?',
   'De diez a quince años el cuerpo del mueble si el tablero y el canto son los correctos, y bastante más la cubierta '
   'de cuarzo. Lo que se degrada primero es el herraje en casa cercana al mar, y es también lo más barato de '
   'reemplazar.'),
  ('¿Pueden trabajar sobre un diseño de mi arquitecto?',
   'Sí. Fabricamos sobre proyecto de terceros con el despiece revisado en taller, y señalamos por escrito cualquier '
   'punto que en obra no vaya a funcionar antes de cortar, que suele ser tolerancia de muro o fondo de mueble.')],
 links=[('/cocinas-de-madera/', 'Cocinas de madera a medida'),
        ('/carpinteria-cancun/', 'Carpintería a medida'),
        ('/closets-a-medida/', 'Clósets a medida'),
        ('/remodelacion-cocina-playa-del-carmen/', 'Remodelación de cocina'),
        ('/remodelacion-banos-cancun/', 'Remodelación de baños')],
 unit='ml')


# ---------------------------------------------------------- carpintería ----
CARPINTERIA = dict(
 slug='carpinteria-%s',
 title='Carpintería a Medida en %s: Precios 2026 | Recrea',
 desc=('Carpintería a medida en %s: clósets, puertas, cocinas y muebles en taller '
       'propio. Precios 2026 por metro lineal y maderas que aguantan.'),
 h1='Carpintería a Medida en %s',
 lead=('Clósets, puertas, cocinas, muebles y carpintería de obra a medida en %s, '
       'fabricados en taller propio con maderas y tableros elegidos para el clima de la costa.'),
 head=('Trabajo de carpintería', 'Materiales', 'Costo 2026'),
 rows=[('Clóset a medida', 'Melamina 16 mm, canto ABS, herraje estándar', 2500, 5000),
       ('Clóset vestidor premium', 'MDF lacado o chapa, cierre suave, iluminación', 5000, 11000),
       ('Puerta interior de tambor', 'Bastidor con chapa, marco y herraje', 4500, 9000),
       ('Puerta sólida de madera dura', 'Tzalam, parota o caoba, por hoja', 12000, 45000),
       ('Cocina integral', 'Por metro lineal, sin cubierta', 3000, 16000),
       ('Mueble a medida (TV, baño, barra)', 'Según diseño y material, por pieza', 8000, 60000)],
 scope=[
  ('Qué fabricamos en taller propio',
   'Clósets y vestidores, puertas interiores y de entrada, cocinas integrales, muebles de baño, libreros, barras, '
   'cabeceras y carpintería de obra como plafones y lambrines de madera. Todo sobre medida tomada en sitio, no sobre '
   'catálogo. El taller propio es lo que permite resolver el mueble raro: la columna en medio del clóset, el techo '
   'inclinado, el hueco de veintitrés centímetros que ningún modular cubre.'),
  ('Cómo trabajamos una pieza a medida',
   'Levantamiento en sitio sobre muro terminado, proyecto de despiece con la tolerancia real del espacio, fabricación '
   'en taller, y montaje con nivelación sobre patas o tacos regulables. Entregamos con puertas y cajones ajustados, no '
   'solo colgados: en carpintería el ajuste final es la mitad del trabajo y es lo primero que se nota cuando se '
   'omite.'),
  ('Obra nueva, reposición o solo frentes',
   'En obra nueva la carpintería entra al final y se mide cuando ya hay muro, piso y plafón terminados. En reposición '
   'se retira lo viejo y se aprovecha el hueco, revisando antes plomo y escuadra del muro. Y en cambio de frentes, se '
   'conserva la estructura interior sana y se renuevan puertas, cajones y herrajes: renueva el aspecto completo por '
   'una fracción del costo de un mueble nuevo.')],
 tech=[
  ('Qué madera aguanta en la costa y cuál no',
   'El tzalam y la parota son las maderas duras locales que mejor se comportan: estables, resistentes al insecto y con '
   'veta que aguanta el sol filtrado. La caoba funciona en interior fino. Lo que no funciona es el pino sin tratar '
   'para nada expuesto a humedad, ni el aglomerado corriente en zona húmeda. Toda madera exterior lleva tratamiento '
   'contra termita y sellador con filtro UV, y se renueva el acabado cada dos o tres años: en este clima no existe la '
   'madera exterior de cero mantenimiento, y quien la promete está omitiendo algo.'),
  ('Tableros, cantos y herrajes: donde está la diferencia real',
   'Entre un clóset de $2,500 y uno de $5,000 el metro lineal la diferencia no suele estar en el diseño sino en tres '
   'cosas: espesor de tablero, tipo de canto y calidad de herraje. Canto ABS pegado en lugar de canto de papel, '
   'bisagra con cierre suave y corredera de extracción total sobre balín en lugar de la corredera de rodillo. Son las '
   'tres partidas que deciden si el mueble sigue cerrando bien a los cinco años, y las tres primeras que recorta un '
   'presupuesto barato.'),
  ('Humedad, termita y el mantenimiento que sí hace falta',
   'La humedad relativa alta hincha el tablero por el canto y la termita subterránea ataca la madera en contacto con '
   'piso o muro húmedo. Por eso el mueble no se apoya directo en el piso sino sobre patas o zócalo ventilado, y la '
   'madera exterior lleva tratamiento y se resella. En casa cercana al mar el herraje va en inoxidable, porque el '
   'salitre traba una bisagra común en dos temporadas.')],
 extra=[
  ('Clósets: lo que cambia el precio por metro lineal',
   'Fondo del mueble, número de cajones y tipo de puerta. Un clóset con puertas corredizas de piso a techo, cajonera '
   'interior con corredera de extracción total e iluminación cuesta el doble por metro lineal que el mismo clóset con '
   'puertas abatibles y entrepaños. Conviene decidir cuántos cajones se quieren antes de comparar presupuestos, '
   'porque es el concepto que más se esconde entre una cotización y otra.'),
  ('Puertas: de tambor a madera sólida',
   'La puerta interior de tambor con chapa cubre la mayoría de la casa a costo razonable y se comporta bien en '
   'interior climatizado. La madera sólida tiene sentido en puerta de entrada, en puertas de doble altura y donde se '
   'busca aislamiento acústico real. En exterior, la puerta sólida necesita alero o protección: sol directo más lluvia '
   'sobre una hoja sin resguardo abre la veta por más buen acabado que lleve.'),
  ('Plazos y coordinación con el resto de la obra',
   'De tres a seis semanas entre levantamiento y montaje, según pieza y material. La carpintería es de los últimos '
   'oficios en entrar, y por eso es la que más sufre cuando la obra viene retrasada. Medimos sobre muro terminado y '
   'coordinamos el montaje después de piso y pintura, con la instalación eléctrica de iluminación de mueble ya '
   'prevista, no improvisada al final.')],
 faq_city={
  'cancun': ('¿Cuánto cuesta un clóset a medida en Cancún?',
     'De $2,500 a $5,000 MXN por metro lineal en melamina con herraje estándar, y de $5,000 a $11,000 en vestidor '
     'premium con cierre suave e iluminación. En casa cercana al mar especificamos herraje inoxidable, que sube algo '
     'el costo y evita que las bisagras se traben.'),
  'playa-del-carmen': ('¿Puedo ver el mueble antes de que lo instalen?',
     'Sí. El taller está en Playa del Carmen y el cliente puede revisar la pieza fabricada antes del montaje. Es la '
     'ventaja práctica de fabricar en casa: una corrección se resuelve en días.'),
  'tulum': ('¿Trabajan tzalam y parota en Tulum?',
     'Sí, son las dos maderas que más pedimos aquí, con acabado natural y sellador con filtro UV. En exterior siempre '
     'con tratamiento contra termita y bajo alero. Sin protección de lluvia y sol directo, ninguna madera dura aguanta '
     'sin abrir veta.'),
  'puerto-morelos': ('¿Hacen carpintería para cabañas y hoteles boutique en Puerto Morelos?',
     'Sí: muebles de habitación, cabeceras, clósets de servicio y carpintería de obra por lotes. En proyecto hotelero '
     'la ventaja del taller propio es la repetición idéntica de pieza y el poder reponer una unidad dañada meses '
     'después con el mismo despiece.'),
  'puerto-aventuras': ('¿Cómo entra la carpintería al fraccionamiento?',
     'Con la ventana de horario y la ruta aprobadas por la administración. Las piezas llegan despiezadas y se '
     'ensamblan en sitio, lo que reduce a dos o tres días la maniobra dentro del desarrollo y molesta menos a los '
     'vecinos.'),
  'akumal': ('¿Qué carpintería aguanta en villa frente a la bahía en Akumal?',
     'Tablero hidrófugo y herraje inoxidable, sin excepción: la carga salina de la bahía es alta. En madera expuesta, '
     'tzalam bajo alero con resellado cada dos o tres años. El mueble no se apoya directo en piso, va sobre zócalo '
     'ventilado.'),
  'cozumel': ('¿Fabrican en Cozumel o cruzan la carpintería?',
     'Se fabrica en el taller del continente y cruza despiezada en ferry en un solo envío, con el flete cotizado '
     'aparte, alrededor de 16%. Es más barato y más rápido que montar producción en la isla para un proyecto.'),
  'isla-mujeres': ('¿Cabe un clóset armado por las calles de Isla Mujeres?',
     'Armado, muchas veces no. Por eso todo va despiezado por módulos y se ensambla en sitio: el ancho de calle es el '
     'límite real de la isla, no la técnica. En Costa Mujeres se trabaja como obra normal de corredor.'),
  'bacalar': ('¿Cuánto cuesta la carpintería en Bacalar?',
     'De $2,900 a $5,800 MXN por metro lineal en clóset de melamina, con el factor de distancia aplicado. Conviene '
     'cerrar toda la carpintería de la casa en un proyecto para que viaje en un solo envío desde el taller.')},
 faq_common=[
  ('¿Trabajan con proyecto de arquitecto o diseñador?',
   'Sí. Fabricamos sobre proyecto de terceros, con el despiece revisado en taller y con aviso por escrito de cualquier '
   'punto que en obra no vaya a funcionar antes de cortar: normalmente tolerancia de muro, fondo de mueble o '
   'interferencia con instalación.'),
  ('¿Qué garantía tiene la carpintería?',
   'Garantía por escrito sobre fabricación y montaje. Los herrajes van con la garantía de su fabricante. No cubre el '
   'deterioro de madera exterior sin el resellado de mantenimiento, que se entrega por escrito con el mueble.'),
  ('¿Cuánto tardan en fabricar?',
   'De tres a seis semanas desde el levantamiento, según pieza, material y carga de taller. La madera sólida es el '
   'tramo largo; la melamina y el MDF son más rápidos. El montaje en sitio toma de uno a cuatro días.'),
  ('¿Hacen solo el mueble o también la obra alrededor?',
   'Las dos cosas. Somos constructora con taller propio, así que podemos entregar solo la carpintería o el espacio '
   'completo con instalación eléctrica, iluminación de mueble, recubrimientos y pintura ya resueltos.')],
 links=[('/carpinteria-y-herreria-playa-del-carmen/', 'Carpintería y herrería en Playa del Carmen'),
        ('/closets-a-medida/', 'Clósets a medida'),
        ('/puertas-de-madera/', 'Puertas de madera'),
        ('/cocinas-de-madera/', 'Cocinas de madera'),
        ('/deck-de-madera/', 'Deck de madera'),
        ('/pergola-de-madera/', 'Pérgola de madera')],
 unit='mxn')


# ------------------------------------------------------- albercas infinity -
INFINITY = dict(
 slug='albercas-infinity-%s',
 title='Albercas Infinity en %s: Precios 2026 | Recrea',
 desc=('Albercas infinity y desbordantes en %s: precios 2026, tanque de compensación, '
       'nivel de espejo y el desnivel que realmente hace falta.'),
 h1='Albercas Infinity y Desbordantes en %s',
 lead=('Construimos albercas infinity y desbordantes en %s: cálculo del canal y del '
       'tanque de compensación, borde nivelado al milímetro y contrato a precio fijo.'),
 head=('Tipo de alberca infinity', 'Ideal para', 'Precio 2026'),
 rows=[('Infinity de un lado (borde simple)', 'Lote con desnivel hacia vista o selva', 22000, 34000),
       ('Infinity de dos lados (en esquina)', 'Terrenos de esquina y vistas dobles', 30000, 45000),
       ('Perimetral desbordante (4 lados)', 'Efecto espejo completo, proyecto de diseño', 38000, 62000),
       ('Infinity en rooftop', 'Con refuerzo estructural de losa', 34000, 75000),
       ('Infinity comercial / hotel', 'Cumplimiento normativo de uso público', 55000, 140000),
       ('Tanque de compensación y equipo', 'Cárcamo, bomba de recuperación y control', 4500, 14000)],
 scope=[
  ('Qué es realmente una alberca infinity',
   'Una alberca cuyo nivel de agua coincide exactamente con el borde de un lado, de modo que el agua desborda de forma '
   'continua sobre un canal oculto y de ahí baja a un tanque de compensación, desde donde una bomba la devuelve al '
   'vaso. Lo que el ojo lee como agua sin borde es en realidad un sistema de recirculación permanente. Eso significa '
   'dos cosas prácticas: hay más equipo que en una alberca normal, y el borde tiene que estar nivelado con una '
   'tolerancia que no admite improvisación en obra.'),
  ('Alcance: vaso, canal, cárcamo y nivelación',
   'El trabajo son cuatro piezas: el vaso de concreto armado, el canal de rebose corrido a lo largo del borde libre, '
   'el tanque de compensación dimensionado al volumen de desborde, y la bomba de recuperación con su control de nivel. '
   'La partida crítica no es ninguna de las cuatro, es la nivelación del borde: si un extremo queda unos milímetros '
   'más alto, el agua desborda solo por la mitad y el efecto se pierde. Se verifica con nivel láser antes de colar y '
   'se corrige entonces, no después.'),
  ('Cuándo tiene sentido y cuándo no',
   'Tiene sentido con desnivel real aprovechable — lote en pendiente, vista a laguna, selva o mar, azotea con vacío al '
   'frente — y en propiedad de renta donde la foto sostiene la tarifa por noche. No tiene sentido en terreno plano sin '
   'vista, donde se paga el sistema completo para mirar una barda. Ahí la misma inversión rinde mucho más en una '
   'alberca convencional más grande, con mejor acabado y con área exterior resuelta. Lo decimos antes de cotizar '
   'porque es la conversación que evita el arrepentimiento caro.')],
 tech=[
  ('El tanque de compensación: la pieza que nadie ve y todo lo decide',
   'El cárcamo tiene que absorber el volumen de desborde en operación más el desplazamiento de los bañistas al entrar. '
   'Corto de volumen, la bomba de recuperación succiona en vacío y se sacrifica; sobrado, se paga obra de más. Se '
   'calcula sobre la superficie del vaso y la longitud del borde libre, no a ojo. Lleva además control de nivel '
   'automático y reposición de agua, porque en esta costa la evaporación en temporada seca es alta y una infinity '
   'pierde nivel más rápido que una alberca cerrada.'),
  ('Consumo, evaporación y lo que cuesta operarla',
   'Una infinity trae una bomba más que una alberca normal y esa bomba trabaja siempre que el efecto esté encendido. '
   'Con bomba de velocidad variable y un temporizador razonable, el consumo se controla; con bomba de una sola '
   'velocidad corriendo todo el día, la cuenta de luz sorprende. La superficie en movimiento evapora más, así que la '
   'reposición automática de agua no es un lujo sino parte del sistema. Muchos propietarios operan el desborde por '
   'horas — mañana y tarde — y el resto del tiempo como alberca normal.'),
  ('Estructura: por qué el borde libre es un problema de ingeniería',
   'El muro del lado desbordante trabaja distinto al resto del vaso: soporta el empuje del agua sin el contrapeso de '
   'terreno del otro lado, y en lote en pendiente además apoya sobre relleno o sobre roca cortada. Ese muro se calcula '
   'aparte, con su armado propio y a veces con dado de cimentación corrido. En rooftop el problema cambia de sitio y '
   'lo decide el cálculo de la losa: el agua pesa una tonelada por metro cúbico, y esa carga se verifica con el '
   'ingeniero estructural antes de dibujar nada.')],
 extra=[
  ('Cuánto desnivel hace falta de verdad',
   'Para que el efecto se lea bien conviene al menos medio metro de caída visual del otro lado del borde; con menos, '
   'el ojo no separa el agua del terreno y el sobrecosto no se justifica. Lo ideal es entre uno y tres metros, que es '
   'donde el espejo funciona y el canal todavía se resuelve sin obra de contención mayor. Con más desnivel se puede, '
   'pero entra muro de contención y el presupuesto cambia de escala.'),
  ('Acabado y borde: donde se ve el oficio',
   'El borde de rebose es la pieza que más delata una obra mal hecha, porque cualquier desnivel se marca con el agua '
   'corriendo. Se resuelve con pieza de borde rectificada o con chukum bien aplicado, y con la junta al mínimo. En '
   'acabado interior, el chukum en tono oscuro da el espejo más limpio y el mosaico veneciano oscuro es la alternativa '
   'reparable por piezas. El acabado claro se ve bonito de cerca y arruina el efecto espejo a distancia.'),
  ('Mantenimiento propio de una infinity',
   'Además del mantenimiento normal, hay que limpiar el canal de rebose, que junta hoja y sedimento, y revisar el '
   'control de nivel del cárcamo. La bomba de recuperación es una pieza más que se desgasta. Súmele entre $800 y '
   '$1,500 MXN al mes sobre el costo de una alberca convencional del mismo tamaño. En temporada de huracanes no se '
   'vacía: se baja el nivel parcialmente y se protege el equipo.')],
 faq_city={
  'cancun': ('¿Dónde funciona una alberca infinity en Cancún?',
     'En Puerto Cancún y en la Zona Hotelera con vista a laguna o mar, y en rooftop de condominio, que es donde más '
     'nos la piden. En terreno plano de supermanzana rara vez se justifica. En rooftop lo primero es el dictamen '
     'estructural de la losa, antes de cualquier proyecto.'),
  'playa-del-carmen': ('¿Cuánto cuesta una alberca infinity en Playa del Carmen?',
     'De $22,000 a $34,000 USD la infinity de un lado y de $38,000 a $62,000 la perimetral desbordante. En Corasol y '
     'Selvamar hay desnivel aprovechable; en Centro y Ejidal, en lote plano, casi siempre recomendamos alberca '
     'convencional con mejor acabado por el mismo dinero.'),
  'tulum': ('¿Se puede hacer infinity con acabado chukum en Tulum?',
     'Sí, y es la combinación más pedida aquí: chukum en tono oscuro da el espejo más limpio. El punto a resolver '
     'antes es el ambiental, porque el agua de retrolavado y de vaciado en Tulum se documenta, y una infinity mueve '
     'más agua que una alberca cerrada.'),
  'puerto-morelos': ('¿Conviene una infinity frente al arrecife en Puerto Morelos?',
     'Conviene por la vista, y hay que resolver el manejo de descargas con disposición controlada por la condición del '
     'parque nacional. En los predios de la Ruta de los Cenotes el desnivel suele ser escaso, así que ahí revisamos '
     'primero si el efecto se va a leer.'),
  'puerto-aventuras': ('¿Funciona una desbordante hacia el canal en Puerto Aventuras?',
     'Es de los mejores escenarios: hay desnivel hacia el agua y la vista sostiene el efecto. Se suma la aprobación de '
     'la administración del desarrollo y, por el ambiente salino de la marina, herrajes y luminarias en inoxidable 316 '
     'o material no ferroso.'),
  'akumal': ('¿Cuánto cuesta una infinity con vista a la bahía en Akumal?',
     'De $23,300 a $36,000 USD la de un lado, con el factor de traslado incluido. La iluminación es el punto '
     'particular de Akumal: por la anidación de tortuga va cálida, baja y dirigida hacia abajo, y eso se resuelve en '
     'el proyecto eléctrico, no comprando luminarias al final.'),
  'cozumel': ('¿Se puede construir una infinity en Cozumel?',
     'Sí, sobre todo en la costa oriente y en la zona norte, donde hay desnivel y vista. El costo sube alrededor de '
     '16% por el cruce de material en ferry, que cotizamos como partida aparte. El equipo se pide completo en un solo '
     'envío para no encadenar viajes.'),
  'isla-mujeres': ('¿Hay desnivel para una infinity en Isla Mujeres?',
     'En la zona alta de la isla y en varios predios con vista al Caribe, sí. En el centro plano no se justifica. La '
     'restricción práctica es la maniobra: equipo y material entran por calles estrechas, así que la logística se '
     'planea antes de firmar el proyecto.'),
  'bacalar': ('¿Se puede hacer una infinity hacia la laguna de Bacalar?',
     'La vista es inmejorable y el punto que decide es el manejo de descargas cerca de la ribera, que ahí se revisa de '
     'verdad por los estromatolitos. Se resuelve con disposición controlada y, en varios predios, alejando el vaso del '
     'borde aunque cueste algo de vista.')},
 faq_common=[
  ('¿Cuánto más cuesta una infinity que una alberca normal?',
   'Entre 40% y 80% más que una alberca convencional del mismo tamaño. La diferencia son el canal de rebose, el tanque '
   'de compensación, la bomba de recuperación y el muro del borde libre, que se calcula aparte.'),
  ('¿Necesito desnivel para hacer una infinity?',
   'Necesita al menos medio metro de caída visual del otro lado del borde para que el efecto se lea; lo ideal es entre '
   'uno y tres metros. En terreno plano sin vista, la misma inversión rinde mucho más en una alberca convencional más '
   'grande y mejor acabada.'),
  ('¿Cuánto tarda construir una alberca infinity?',
   'De diez a dieciséis semanas, entre tres y cuatro más que una alberca convencional. Lo que agrega tiempo es el '
   'cárcamo, la nivelación verificada del borde y la puesta a punto del control de nivel.'),
  ('¿Consume mucha más agua y luz?',
   'Más que una alberca cerrada, sí: la superficie en movimiento evapora más y la bomba de recuperación trabaja '
   'mientras el efecto está encendido. Con bomba de velocidad variable, reposición automática y operación por horas, '
   'el sobrecosto de operación se mantiene razonable.')],
 links=[('/albercas-infinity/', 'Albercas infinity: precios y sistema'),
        ('/construccion-albercas/', 'Construcción de albercas en la Riviera Maya'),
        ('/albercas-de-lujo-playa-del-carmen/', 'Albercas de lujo'),
        ('/cuanto-cuesta-una-alberca/', 'Cuánto cuesta una alberca'),
        ('/muro-de-contencion/', 'Muro de contención')],
 unit='usd')


CLUSTERS = {'banos': BANOS, 'cocinas': COCINAS, 'carpinteria': CARPINTERIA, 'infinity': INFINITY}


def price(lo, hi, factor, unit):
    if unit == 'usd':
        return '%s – %s USD' % (usd(lo * factor), usd(hi * factor))
    if unit == 'ml':
        return '%s – %s / ml' % (mxn(lo * factor), mxn(hi * factor))
    return '%s – %s' % (mxn(lo * factor), mxn(hi * factor))


# Rotated like the cluster sections. With nine cities and only three variants per
# section, a plain i%3 hands cities three apart an identical page; the offsets below
# give every city a different combination of the five rotating blocks.
INTRO = [
 'Trabajamos en %s — %s — y el proyecto se ajusta a lo que la plaza impone: %s. Somos constructora con equipo propio, '
 'no intermediarios que subcontratan la obra y desaparecen cuando hay que responder.',
 'En %s cubrimos %s. La condición que marca el trabajo aquí es %s, y por eso el presupuesto se arma sobre el sitio '
 'concreto y no sobre un precio de catálogo. Ejecutamos con personal propio y un solo responsable de obra.',
 'Damos servicio en %s: %s. Antes de cotizar visitamos el sitio, porque en esta plaza pesa %s, y ese detalle cambia '
 'materiales y plazo más de lo que la gente espera. Equipo propio, sin cadena de subcontratistas.']

PRICE_NOTE = [
 'Rangos para trabajo terminado y entregado, con mano de obra, material e instalación incluidos. En las plazas fuera '
 'del corredor Cancún–Playa el flete va identificado como partida propia en lugar de repartido a escondidas en los '
 'precios unitarios, para que se pueda comparar contra cualquier otra cotización de la región.',
 'Los rangos de abajo son de obra terminada y probada, no de suministro suelto. Incluyen material, mano de obra e '
 'instalación. Lo que se cotiza por separado se dice por su nombre en el presupuesto; el flete a plazas alejadas es '
 'una partida visible y no un recargo escondido en el precio unitario.',
 'Precios de 2026 para el trabajo entregado y funcionando. Cada partida lleva marca y modelo especificados, que es lo '
 'que permite comparar dos presupuestos de verdad en lugar de comparar totales. En las plazas insulares y en Bacalar '
 'el traslado se factura aparte y a la vista.']

PROCESS = [
 'Visita y levantamiento en sitio sin costo, presupuesto cerrado por partidas con marcas y modelos especificados, '
 'calendario de pagos ligado a avance verificable y un solo responsable de obra de principio a fin. En %s coordinamos '
 'además los permisos o vistos buenos que el proyecto requiera antes de mover material.',
 'Primero vamos al sitio y medimos; después entregamos un presupuesto cerrado por partidas, con el calendario de pagos '
 'atado a avance que el cliente puede verificar. Durante la obra hay un único responsable y un reporte de avance. En '
 '%s gestionamos nosotros los vistos buenos previos que correspondan.',
 'El proceso es siempre el mismo: levantamiento en sitio, proyecto, presupuesto cerrado por partidas y contrato con '
 'calendario ligado a avance. Nada arranca sin que el alcance esté escrito. En %s resolvemos antes los permisos o la '
 'autorización de la administración que el trabajo necesite.']


def make(cl, slug_city, city, order):
    n, zones, quirk = city['name'], city['zones'], city['quirk']
    i = order
    v, vt, ve = i % 3, (i // 3) % 3, (i + i // 3) % 3
    vi, vp, vc = (i + 2) % 3, (i * 2 + i // 3) % 3, (i + 1) % 3
    secs = [('%s en %s' % (cl['h1'].split(' en ')[0], n), INTRO[vi] % (n, zones, quirk)),
            cl['scope'][v],
            cl['tech'][vt],
            ('Precios 2026 en %s' % n, PRICE_NOTE[vp]),
            cl['extra'][ve],
            ('Cómo trabajamos en %s' % n, PROCESS[vc] % n)]
    faq = [cl['faq_city'][slug_city]] + cl['faq_common']
    sibs = list(CITIES.items())
    sibs = [sibs[(order + k) % len(sibs)] for k in (1, 2, 3)]
    links = [(('/' + cl['slug'] % s + '/'), '%s en %s' % (cl['h1'].split(' en ')[0], c['name']))
             for s, c in sibs] + cl['links']
    t = cl['title'] % n
    return dict(title=t if len(t) <= 65 else cl['title'].replace(': Precios 2026', '') % n,
                desc=cl['desc'] % n, h1=cl['h1'] % n, lead=cl['lead'] % n, secs=secs,
                table=cl['head'] + ([(a, b, price(lo, hi, city['factor'], cl['unit']))
                                     for a, b, lo, hi in cl['rows']],),
                faq=faq, links=links)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src = open(kw1.TPL, encoding='utf-8').read()
    for cname, cl in CLUSTERS.items():
        built = {}
        for i, (slug_city, city) in enumerate(CITIES.items()):
            slug = cl['slug'] % slug_city
            page = make(cl, slug_city, city, i)
            os.makedirs(slug, exist_ok=True)
            html = kw1.build(slug, page, src)
            open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
            body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
            built[slug] = set(tuple(body[j:j + 6]) for j in range(len(body) - 5))
        ks = list(built)
        mx = max((len(built[a] & built[b]) / len(built[a] | built[b]), a, b)
                 for i, a in enumerate(ks) for b in ks[i + 1:])
        words = sum(len(re.sub(r'<[^>]+>', ' ', open(k + '/index.html', encoding='utf-8').read()).split())
                    for k in ks) // len(ks)
        print('%-14s %d pages  ~%d words  max similarity %.2f  (%s vs %s)'
              % (cname, len(ks), words, mx[0], mx[1], mx[2]))
