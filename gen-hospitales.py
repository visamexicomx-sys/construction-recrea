#!/usr/bin/env python3
"""Hospital and clinic construction pages, one per city in the service corridor.

A new vertical: until now the only healthcare content on the site was a single
English blog article. Healthcare fit-out is the most regulated commercial work we
do — the operating licence depends on the premises themselves — so the pages are
written around that: the room schedule comes from the regulator, not from the
architect, and the build follows.

Scope is stated honestly on every page. We do the civil work, the installations,
the finishes and the coordination of the specialist packages. Medical gas systems,
radiological shielding and the regulatory filing itself are executed and signed by
certified specialists; we build around them and program their tests, we do not
claim to certify them.

Figures are kept in step with blog/medical-clinic-construction-playa-del-carmen.html.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'kw1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-keyword-pages.py'))
kw1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kw1)

BASE = [('Consultorio y clínica de consulta', 'Obra civil, instalaciones, acabados lavables', 14000, 24000, 'm2'),
        ('Clínica dental', 'Succión, aire comprimido, agua tratada, acabados sin juntas', 20000, 38000, 'm2'),
        ('Clínica con área de procedimientos y CEYE', 'Circulación sucio-limpio, esterilización', 25000, 45000, 'm2'),
        ('Cirugía ambulatoria con quirófano', 'Área blanca, gases medicinales, recuperación', 40000, 75000, 'm2'),
        ('Blindaje radiológico', 'Por sala: diseño, colocación y memoria', 150000, 500000, 'obra'),
        ('Red de gases medicinales', 'Tendido, alarmas, pruebas y certificación', 300000, 1200000, 'obra'),
        ('Planta de emergencia con transferencia automática', 'Clínica pequeña', 200000, 500000, 'obra')]


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


SCOPE = [
 ('Qué construimos y qué firma un tercero',
  'Hacemos la obra civil y la instalación completa de la unidad: distribución, muros, acabados lavables sin juntas, '
  'instalación hidrosanitaria y eléctrica, aire acondicionado con la filtración que pida cada área, iluminación, '
  'carpintería fija, mobiliario de acero inoxidable y el almacén de residuos peligrosos biológico-infecciosos. '
  'Lo que no firmamos es la red de gases medicinales ni el blindaje radiológico: los ejecuta y certifica un '
  'especialista acreditado, y así debe quedar en el contrato. Nosotros programamos la obra alrededor de sus pruebas.'),
 ('Alcance real del contrato de obra',
  'Nuestro contrato cubre la parte constructiva: albañilería, instalaciones, climatización y filtración, acabados '
  'de superficie continua con zoclo sanitario, puertas de paso libre, lavabos de accionamiento no manual, cuarto '
  'de RPBI y las preparaciones para el equipo médico. La red de gases medicinales, el blindaje de las salas de '
  'rayos X y el trámite sanitario los lleva un especialista certificado; el programa de obra se arma con sus '
  'tiempos de prueba dentro, no después.'),
 ('Cómo se divide una obra de salud',
  'Una unidad médica se construye con tres frentes que corren en paralelo: la obra civil e instalaciones —que es la '
  'nuestra—, los paquetes especializados de gases medicinales y blindaje radiológico, y el expediente regulatorio '
  'que sostiene la licencia sanitaria. Confundirlos es el origen habitual de los retrasos: el área blanca no se '
  'cierra antes de que la red de gases esté probada, y el equipo no entra antes de que el blindaje esté verificado. '
  'Lo que garantizamos es que la parte civil no sea la que detiene el calendario.')]

PERMITS = [
 ('El expediente sanitario define el proyecto, no al revés',
  'En una unidad médica el programa de áreas no lo decide el arquitecto: lo fija la normatividad sanitaria según los '
  'servicios que se van a prestar. Consultorio, clínica dental, unidad de procedimientos, imagenología y cirugía '
  'ambulatoria son categorías distintas, con superficies mínimas, anchos de circulación, separación de flujos y '
  'requisitos de instalaciones propios. Por eso el primer entregable no es un plano: es el listado de servicios, '
  'convertido en programa de áreas con un asesor regulatorio.'),
 ('Licencia sanitaria, aviso de funcionamiento y responsable',
  'Según el giro, la unidad requiere aviso de funcionamiento o licencia sanitaria, con responsable sanitario '
  'designado, y en imagenología además el registro y la memoria de seguridad radiológica. El inmueble se revisa '
  'contra esos requisitos, de modo que un local bonito pero con circulaciones estrechas o sin separación sucio-limpio '
  'simplemente no se autoriza. Conviene traer al asesor regulatorio desde el anteproyecto, no cuando ya hay muros.'),
 ('Tres capas de trámite que conviven',
  'Sanitaria: aviso o licencia, responsable sanitario, manejo de RPBI y, en su caso, seguridad radiológica. '
  'Municipal: uso de suelo compatible con el giro salud, licencia de construcción, DRO y número oficial. '
  'Protección Civil: salidas, anchos, iluminación de emergencia, señalización, extintores y un plan que funcione '
  'con pacientes que no pueden evacuar por su cuenta. Las tres se atienden en paralelo desde el primer mes; '
  'dejar Protección Civil para el final es lo que más veces retrasa una apertura.')]

TECH = [
 ('Acabados e instalaciones que sí pasan verificación',
  'Piso de superficie continua —vinílico en rollo termosellado o resina— con zoclo sanitario redondeado; muros con '
  'recubrimiento lavable y resistente a desinfectantes; plafón sellado en áreas críticas; sin repisas abiertas en '
  'salas de procedimientos. Lavabo con llave de accionamiento no manual en cada área clínica, puertas con paso libre '
  'suficiente para camilla y silla de ruedas, y climatización con la filtración y el régimen de presión que exija el '
  'área. El acabado comercial común no cumple y, más importante, no funciona clínicamente.'),
 ('Instalaciones críticas y redundancia',
  'Circuitos protegidos en zonas húmedas y en áreas de procedimientos, UPS para el equipo que no puede caer a media '
  'intervención y planta de emergencia con transferencia automática en toda unidad que seda pacientes: en esta región '
  'el corte de luz en temporada de lluvias es rutina, no excepción. Dos fuentes de agua —red y cisterna propia—, '
  'tratamiento por la dureza local para autoclaves y equipo dental, y extracción independiente en esterilización.'),
 ('Flujos, circulaciones y RPBI',
  'El plano se organiza por flujos: paciente, personal, material limpio y material sucio, sin que se crucen donde la '
  'norma no lo permite. La esterilización se diseña con zonas sucia y limpia separadas y paso en un solo sentido. '
  'El almacén temporal de residuos peligrosos biológico-infecciosos va aislado, ventilado, con superficies '
  'impermeables, señalizado y con ruta de salida que no cruce áreas de pacientes; además necesita empresa recolectora '
  'contratada antes de abrir. Es un cuarto pequeño que, cuando falta en el plano, obliga a rehacer media planta.')]

OPER = [
 ('Construir con la unidad operando',
  'La mayoría de las ampliaciones y remodelaciones de clínicas se hacen sin cerrar. Se trabaja por zonas aisladas con '
  'tapial hermético y control de polvo, se define ruta de obra que no cruce circulación de pacientes, y los trabajos '
  'ruidosos se programan en ventanas acordadas con la dirección médica. Los cortes de agua y energía se planean por '
  'escrito con semanas de anticipación, porque en una unidad médica una interrupción no avisada tiene consecuencias '
  'clínicas, no solo comerciales.'),
 ('Tiempos reales de una obra de salud',
  'Un consultorio o clínica de consulta toma de 10 a 16 semanas de obra. Una clínica dental con varias unidades, de '
  '12 a 20. Una unidad con área de procedimientos y esterilización, de 4 a 7 meses. Cirugía ambulatoria con '
  'quirófano, de 6 a 12. A eso se suma el trámite regulatorio, que con frecuencia es más largo que la obra y por eso '
  'arranca primero. El otro cuello de botella son los equipos: imagenología, autoclaves y unidades dentales tienen '
  'plazos de entrega largos y el cuarto se construye para el modelo específico.'),
 ('Equipo médico y coordinación de proveedores',
  'El inmueble se construye alrededor de equipos concretos, no de categorías: cada modelo trae su propia ficha de '
  'requerimientos de espacio, peso, alimentación eléctrica, agua, drenaje y ventilación. Por eso pedimos la lista de '
  'equipo firmada antes de cerrar instalaciones. Coordinamos al proveedor de gases medicinales, al de blindaje, al '
  'de mobiliario de acero inoxidable y al de equipo, y dejamos las preparaciones terminadas y verificadas para que '
  'la instalación del equipo no abra muros ya acabados.')]

FAQ_COMMON = [
 ('¿Se puede remodelar la clínica sin cerrarla?',
  'Casi siempre sí, por zonas, con tapial hermético, control de polvo y ruta de obra separada de la circulación de '
  'pacientes. Los trabajos ruidosos y los cortes de servicio se programan con la dirección médica por escrito.'),
 ('¿Ustedes tramitan la licencia sanitaria?',
  'La coordinamos, no la firmamos. El trámite y el responsable sanitario corresponden a un asesor regulatorio; '
  'nosotros construimos contra ese programa de áreas y entregamos el inmueble en condiciones de ser verificado.'),
 ('¿Instalan gases medicinales y blindaje radiológico?',
  'Los coordinamos y dejamos las preparaciones, pero la ejecución y la certificación las hace un especialista '
  'acreditado. Es lo correcto técnica y legalmente, y así queda en el contrato.'),
 ('¿Trabajan a precio fijo?',
  'Sí: contrato a precio fijo con presupuesto por partidas, pagos contra avance verificado y retención hasta cerrar '
  'la lista de detalles. En obra de salud el alcance debe estar cerrado antes de empezar, precisamente porque las '
  'áreas las define la norma.')]

CITIES = {
'playa-del-carmen': dict(
  name='Playa del Carmen', muni='Solidaridad', factor=1.0,
  ctx=('Playa del Carmen concentra el mercado privado de consulta más grande del estado después de Cancún: clínicas '
       'dentales y de estética orientadas a turismo médico en el centro y sobre la 30 Avenida, consultorios de '
       'especialidad alrededor de los hospitales privados, y unidades de urgencias que atienden a una población '
       'residente que crece más rápido que su infraestructura de salud. Casi toda la obra aquí es adecuación de '
       'local comercial a uso médico, que es un cambio de giro, no una remodelación.'),
  local=('En Solidaridad conviene verificar desde el principio que el uso de suelo admita el giro salud en ese local '
         'concreto: es el filtro que más proyectos detiene, y se resuelve antes de firmar el arrendamiento, no '
         'después. Sumado a eso, el trámite de Protección Civil para un giro con pacientes es más exigente que el de '
         'un comercio del mismo tamaño.'),
  faq=[('¿Puedo convertir un local comercial en clínica en Playa del Carmen?',
        'Depende del uso de suelo del local y de si la estructura permite anchos de circulación, salidas y '
        'ventilación acordes al giro. Lo revisamos antes de que firme el arrendamiento: es el momento en que '
        'todavía se puede cambiar de local sin costo.'),
       ('¿Cuánto cuesta acondicionar un consultorio en el centro?',
        'Entre $14,000 y $24,000 MXN/m² para consulta, y de $20,000 a $38,000 para una clínica dental por la '
        'instalación de succión, aire comprimido y agua tratada.'),
       ('¿Atienden clínicas de turismo médico?',
        'Sí, y es una parte importante del trabajo aquí. Son unidades donde el acabado comunica tanto como la '
        'norma: hay que cumplir verificación sanitaria y, al mismo tiempo, sostener una imagen de nivel '
        'internacional.')]),

'cancun': dict(
  name='Cancún', muni='Benito Juárez', factor=0.98,
  ctx=('Cancún tiene la mayor infraestructura hospitalaria de Quintana Roo y es donde aparecen los proyectos de mayor '
       'escala: torres de consultorios, ampliaciones de hospitales privados, unidades de imagenología y clínicas de '
       'atención a turismo. Es también el único mercado del estado con proveedores especializados locales, lo que '
       'acorta tiempos en gases medicinales, mobiliario de acero inoxidable y servicio de equipo médico.'),
  local=('En Benito Juárez el condicionante de obra es urbano: horarios de maniobra en avenidas de alto flujo, '
         'estacionamiento exigido por el giro y, en la zona hotelera, ventanas de trabajo y límites de ruido. Para '
         'ampliaciones sobre hospitales en operación, el plan de obra se negocia con la dirección médica antes que '
         'con el municipio.'),
  faq=[('¿Hacen ampliaciones de hospitales en operación?',
        'Sí. Se trabaja por zonas con aislamiento hermético, control de polvo y accesos independientes, con los '
        'cortes de servicio programados por escrito con la dirección médica.'),
       ('¿Cuánto cuesta una unidad de cirugía ambulatoria en Cancún?',
        'De $40,000 a $75,000 MXN/m² de obra e instalaciones, más la red de gases medicinales y el blindaje de las '
        'salas que lo requieran, que se cotizan por separado.'),
       ('¿Hay proveedores especializados en la ciudad?',
        'Sí, y es la ventaja real de construir aquí: gases medicinales, acero inoxidable a medida y servicio de '
        'equipo se resuelven localmente, sin traer todo desde Mérida o la Ciudad de México.')]),

'tulum': dict(
  name='Tulum', muni='Tulum', factor=1.07,
  ctx=('Tulum creció mucho más rápido que su infraestructura de salud: la población residente y flotante ya justifica '
       'unidades de urgencias, imagenología básica y clínicas de especialidad que hasta hace poco obligaban a '
       'trasladarse a Playa del Carmen. La apertura del aeropuerto acentuó esa demanda. Es el mercado con más espacio '
       'para unidades nuevas y, a la vez, el de trámite más largo.'),
  local=('El municipio de Tulum suma el componente ambiental a todo lo demás: en lote con vegetación, el expediente '
         'ambiental fija el calendario completo. A eso se añade lo que en otras ciudades es un detalle y aquí no lo '
         'es: la red eléctrica es menos confiable, de modo que la planta de emergencia con transferencia automática '
         'deja de ser opcional en cualquier unidad que sede pacientes o dependa de refrigeración.'),
  faq=[('¿Por qué una clínica en Tulum tarda más en abrir?',
        'Porque se suman dos calendarios: el sanitario, que existe en todas las ciudades, y el ambiental del '
        'municipio, que en lote con vegetación puede tomar meses. Ambos arrancan antes que la obra.'),
       ('¿Es obligatoria la planta de emergencia?',
        'En una unidad que seda pacientes o que depende de refrigeración, en la práctica sí. En Tulum el corte de '
        'energía en temporada de lluvias es rutina y el respaldo se diseña desde el principio, no se agrega después.'),
       ('¿Cómo se maneja el drenaje de una clínica aquí?',
        'Con tratamiento antes de infiltrar, dimensionado a la ocupación real, y con el manejo de RPBI '
        'completamente separado del drenaje sanitario. En suelo kárstico eso se revisa con detalle.')]),

'puerto-aventuras': dict(
  name='Puerto Aventuras', muni='Solidaridad', factor=1.03,
  ctx=('Puerto Aventuras demanda un tipo de unidad muy específico: atención de urgencias y consulta general para una '
       'comunidad residencial cerrada con población extranjera y de retiro, además de servicio a la marina y a la '
       'hotelería del tramo. No son hospitales: son clínicas pequeñas, bien equipadas, que resuelven lo inmediato y '
       'derivan lo complejo a Playa del Carmen.'),
  local=('Al pertenecer a Solidaridad, el trámite municipal es el mismo que en Playa del Carmen, pero la obra se '
         'ejecuta dentro de un fraccionamiento con acceso controlado, horarios de trabajo restringidos, registro de '
         'personal y, normalmente, aprobación del comité interno. El plan de obra se arma alrededor de esas ventanas '
         'desde el primer día.'),
  faq=[('¿Qué tipo de unidad tiene sentido en Puerto Aventuras?',
        'Consulta general y urgencias menores, con capacidad de estabilizar y derivar. El volumen de población no '
        'sostiene una unidad quirúrgica, pero sí una clínica bien resuelta con laboratorio y rayos X simple.'),
       ('¿La comunidad cerrada complica la obra?',
        'La condiciona: acceso controlado, horarios acotados, registro de trabajadores y reglamento interno. No es '
        'un problema si se programa desde el inicio; sí lo es si se descubre a mitad de obra.'),
       ('¿Atienden también consultorios dentro de hoteles?',
        'Sí. El consultorio de hotel tiene requisitos propios de circulación y de acceso independiente que conviene '
        'resolver en el anteproyecto.')]),

'puerto-morelos': dict(
  name='Puerto Morelos', muni='Puerto Morelos', factor=1.02,
  ctx=('Puerto Morelos vive entre dos polos hospitalarios: Cancún a veinte minutos al norte y Playa del Carmen al '
       'sur. Eso define el producto: clínicas de consulta, odontología y urgencias menores para residentes, para la '
       'hotelería del corredor y para el turismo de buceo, con derivación rápida a las dos ciudades grandes cuando '
       'hace falta algo mayor.'),
  local=('Es un municipio joven —se separó de Benito Juárez en 2016— con instrumentos de planeación relativamente '
         'recientes: conviene confirmar uso de suelo y requisitos caso por caso en lugar de asumir la práctica de '
         'Cancún. La ventaja es una administración accesible, donde un expediente completo avanza rápido y uno '
         'incompleto se atora.'),
  faq=[('¿Conviene una clínica aquí teniendo Cancún cerca?',
        'Sí, para consulta, odontología y urgencias menores. Lo que no tiene sentido es intentar competir en alta '
        'especialidad: el modelo que funciona es resolver lo cotidiano y derivar lo complejo.'),
       ('¿El trámite es igual que en Cancún?',
        'No. Puerto Morelos emite sus propias licencias desde 2016 y sus instrumentos de planeación son recientes. '
        'Se confirma el uso de suelo del predio concreto antes de proyectar.'),
       ('¿Atienden unidades de medicina hiperbárica?',
        'La obra civil y las instalaciones sí; la cámara y su certificación las provee el fabricante. La preparación '
        'estructural, eléctrica y de ventilación se diseña para el modelo específico.')]),

'akumal': dict(
  name='Akumal', muni='Tulum', factor=1.08,
  ctx=('Akumal tiene una demanda pequeña pero muy definida: atención inmediata para una comunidad residencial '
       'dispersa, para la hotelería de la bahía y para el buceo, que aquí es actividad cotidiana. El modelo viable es '
       'la unidad compacta de urgencias y consulta, resuelta para estabilizar y trasladar, no para tratamiento '
       'prolongado.'),
  local=('Pertenece al municipio de Tulum y hereda su exigencia ambiental, con la sensibilidad añadida de la bahía y '
         'de los sistemas de cenotes: el manejo de residuos y el drenaje se revisan con más detalle que tierra '
         'adentro. La base local de oficios es reducida, así que la cuadrilla se traslada completa desde Playa del '
         'Carmen.'),
  faq=[('¿Qué unidad tiene sentido en Akumal?',
        'Una clínica compacta de urgencias y consulta, con capacidad de estabilizar y coordinar traslado. La '
        'población no sostiene una unidad mayor y la distancia a Playa del Carmen hace que el traslado sea parte '
        'del modelo, no una falla.'),
       ('¿Cómo se maneja el RPBI en una comunidad pequeña?',
        'Con almacén temporal aislado y ventilado dentro de la unidad y empresa recolectora contratada con ruta '
        'programada. Es el punto que más se descuida en unidades pequeñas y el primero que se verifica.'),
       ('¿Hay sobrecosto por la ubicación?',
        'Del orden de 8% sobre la obra equivalente en Playa del Carmen, por traslado de cuadrilla y de material. Va '
        'identificado en el presupuesto, no diluido en los precios unitarios.')]),

'cozumel': dict(
  name='Cozumel', muni='Cozumel', factor=1.16,
  ctx=('Cozumel tiene una demanda médica que no se parece a la del continente: buceo todos los días del año, un '
       'puerto de cruceros que descarga miles de pasajeros por jornada y una población residente que no puede '
       'depender de un traslado en ferry para una urgencia. Eso sostiene unidades de atención inmediata, medicina '
       'hiperbárica y consulta de especialidad que en una ciudad del mismo tamaño en el continente no existirían.'),
  local=('Es isla, y eso manda sobre la obra: todo el material entra por ferry o barcaza, con calendario propio y '
         'flete que se refleja en el presupuesto. El municipio gestiona sus propios trámites. El acopio se programa '
         'por etapas y se pide de más en lo crítico, porque un faltante no se resuelve el mismo día como en el '
         'continente.'),
  faq=[('¿Cuánto encarece la obra el hecho de ser isla?',
        'Alrededor de 15% sobre la obra equivalente en el continente, por flete marítimo, tiempos de entrega y '
        'estancia de la cuadrilla. Lo identificamos como partida propia.'),
       ('¿Construyen cámaras hiperbáricas?',
        'La obra civil, la instalación eléctrica y la ventilación sí, diseñadas para el equipo concreto. La cámara '
        'y su certificación corresponden al fabricante.'),
       ('¿Cómo aseguran el suministro de material?',
        'Con programa de embarques por etapa y acopio en sitio, con margen en acabados críticos y sujeción. Parar '
        'la obra cuesta más que el material extra.')]),

'isla-mujeres': dict(
  name='Isla Mujeres', muni='Isla Mujeres', factor=1.15,
  ctx=('El municipio tiene dos escenarios distintos bajo la misma autoridad: la isla, donde la unidad médica debe '
       'resolver urgencias con población flotante alta y logística por embarcación, y Costa Mujeres en el continente, '
       'donde la hotelería nueva ha traído demanda de consultorios y de servicio médico de apoyo al huésped. La '
       'obra no se parece en nada de un lado al otro.'),
  local=('En la isla el condicionante es el acceso: calles estrechas, maniobras acotadas y material que llega por '
         'embarcación. En Costa Mujeres se construye como obra de corredor, con acceso normal de maquinaria. El '
         'trámite municipal es el mismo en ambos casos, pero el plan de obra y el presupuesto son documentos '
         'distintos.'),
  faq=[('¿Trabajan en la isla y en Costa Mujeres?',
        'En las dos. La isla exige logística marítima y maniobras acotadas; Costa Mujeres se trabaja con acceso '
        'normal, a costo prácticamente igual al de Cancún.'),
       ('¿Qué unidad funciona en la isla?',
        'Atención inmediata y consulta, dimensionada para población flotante alta en temporada. Lo determinante es '
        'la capacidad de estabilizar y coordinar traslado, no el número de consultorios.'),
       ('¿Cómo llega el material a la isla?',
        'Por embarcación, con programa por etapas y acopio previo. El traslado va como partida identificada en el '
        'presupuesto.')]),
}

PILLAR = dict(
  name='la Riviera Maya', muni='Quintana Roo', factor=1.0,
  ctx=('Construimos y adecuamos unidades médicas en todo el corredor: Cancún, Puerto Morelos, Playa del Carmen, '
       'Puerto Aventuras, Akumal, Tulum, Cozumel e Isla Mujeres. Van desde el consultorio y la clínica dental hasta '
       'unidades con área de procedimientos, imagenología y cirugía ambulatoria. Es la obra comercial más regulada '
       'que hacemos: aquí el inmueble es parte de la licencia, y por eso el programa de áreas se define con el '
       'asesor regulatorio antes del primer plano.'),
  local=('Cada municipio agrega lo suyo: impacto urbano y estacionamiento en Benito Juárez y Solidaridad, expediente '
         'ambiental y respaldo eléctrico en Tulum, municipio joven en Puerto Morelos, logística marítima en Cozumel e '
         'Isla Mujeres. La capa sanitaria y la de Protección Civil son comunes a todos; el calendario real lo fija el '
         'municipio y, en las islas, el flete.'),
  faq=[('¿En qué ciudades trabajan?',
        'Cancún, Puerto Morelos, Playa del Carmen, Puerto Aventuras, Akumal, Tulum, Cozumel e Isla Mujeres. Fuera '
        'de ese corredor lo evaluamos caso por caso: preferimos decir que no antes que estirar una cuadrilla.'),
       ('¿Qué tipo de unidades médicas construyen?',
        'Consultorios, clínicas dentales, unidades de consulta y procedimientos, imagenología, laboratorio y '
        'cirugía ambulatoria, además de ampliaciones y remodelaciones de unidades en operación.'),
       ('¿Por dónde se empieza un proyecto de clínica?',
        'Por el listado de servicios que se van a prestar. De ahí sale el programa de áreas normativo y solo '
        'entonces tiene sentido dibujar. Empezar por el plano es lo que obliga a rehacerlo.')])


def make(slug_city, d, order):
    city = d['name']
    i = order
    v, vp, vc, vo = i % 3, (i + 1) % 3, (i + 2) % 3, (i // 3) % 3
    secs = [
        ('Unidades médicas en %s' % city, d['ctx']),
        SCOPE[v],
        PERMITS[vp],
        ('Costos de obra 2026 en %s' % city,
         'Rangos de obra civil, instalaciones y acabados para uso médico, sin equipo médico. Las partidas que más '
         'mueven el total son la climatización con filtración, los acabados de superficie continua y las '
         'instalaciones especiales; el blindaje y los gases medicinales se cotizan por separado porque los ejecuta '
         'un especialista certificado.'),
        TECH[vc],
        ('Normativa local: %s' % d['muni'], d['local']),
        OPER[vo],
    ]
    faq = d['faq'] + FAQ_COMMON
    links = [('/construccion-hospitales-clinicas-riviera-maya/', 'Hospitales y clínicas en toda la Riviera Maya')] if slug_city else []
    links += [('/construccion-comercial-oficinas/', 'Construcción comercial y de oficinas'),
              ('/permisos-licencias-construccion-riviera-maya/', 'Permisos y licencias'),
              ('/supervision-de-obra/', 'Supervisión de obra')]
    if not slug_city:
        links = [('/construccion-hospitales-clinicas-%s/' % s, 'Clínicas en %s' % c['name'])
                 for s, c in list(CITIES.items())[:3]] + links[1:]
    t_long = 'Construcción de Hospitales y Clínicas en %s | Recrea' % city
    t_short = 'Construcción de Clínicas en %s | Recrea' % city
    return dict(
        title=t_long if len(t_long) <= 65 else t_short,
        desc=('Construcción y adecuación de clínicas y unidades médicas en %s: programa de áreas '
              'normativo, acabados e instalaciones que pasan verificación.' % city),
        h1='Construcción de Hospitales y Clínicas en %s' % city,
        lead=('Obra civil, instalaciones y acabados para unidades médicas en %s, construidos contra el programa de '
              'áreas que exige la normatividad sanitaria — no al revés.' % city),
        secs=secs,
        table=('Concepto', 'Incluye', 'Costo 2026') + (rows_for(d['factor']),),
        faq=faq, links=links)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src = open(kw1.TPL, encoding='utf-8').read()
    built = {}
    items = [('', PILLAR)] + list(CITIES.items())
    for i, (slug_city, d) in enumerate(items):
        slug = 'construccion-hospitales-clinicas-' + (slug_city or 'riviera-maya')
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
