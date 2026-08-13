#!/usr/bin/env python3
"""Second batch of keyword-gap pages (Semrush MX, checked 2026-08-13).

Every keyword below was verified as having no page targeting it in a title
before being written. Volumes are monthly, MX database:

  microcemento          14,800  KD 22      pergola de madera      8,100  KD 31
  muro de contencion     8,100  KD 22      mecanica de suelos     3,600  KD 16
  uso de suelo           3,600  KD 26      cemento pulido         2,900  KD 26
  deck de madera         2,400  KD 24      humedad en paredes     1,900  KD 22
  contrato de obra         880  KD 24      supervision de obra      880  KD 30
  ventanas de aluminio     720  KD 26      captacion agua lluvia    590  KD 36
  director resp. de obra   390  KD 24      grietas en muros         260  KD 10

Reuses build() from gen-keyword-pages.py so both batches stay identical in
markup, schema and chrome.
"""
import os, importlib.util

spec = importlib.util.spec_from_file_location(
    'kw1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-keyword-pages.py'))
kw1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kw1)

L_OBRA = ('/construccion-de-casas-riviera-maya/', 'Construcción de casas en la Riviera Maya')
L_PERM = ('/permisos-licencias-construccion-riviera-maya/', 'Permisos, licencias y DRO')
L_PRES = ('/presupuesto-de-obra/', 'Presupuesto de obra por partidas')
L_PROY = ('/proyecto-arquitectonico/', 'Proyecto arquitectónico')
L_TOPO = ('/topografia-y-planos-riviera-maya/', 'Topografía y planos')
L_CIM = ('/cimentacion-y-losas-playa-del-carmen/', 'Cimentación y losas')
L_REM = ('/remodelacion-casas-playa-del-carmen/', 'Remodelación de casas')
L_IMP = ('/impermeabilizacion-techos-playa-del-carmen/', 'Impermeabilización de techos')
L_CARP = ('/carpinteria-y-herreria-playa-del-carmen/', 'Carpintería y herrería')
L_PDC = ('/construccion-de-casas-playa-del-carmen/', 'Construcción de casas en Playa del Carmen')

PAGES = {

'muro-de-contencion': dict(
  title='Muro de Contención: Tipos, Cálculo y Precio 2026 | Recrea',
  desc='Muro de contención en la Riviera Maya: tipos, cuándo se necesita, cómo se calcula, drenaje, precios por m² en 2026 y los errores que provocan que fallen.',
  h1='Muro de Contención: Tipos, Cálculo y Precio por m²',
  lead='Un muro de contención no falla por el muro: falla por el agua que no pudo salir. Esto es lo que sostiene un talud de verdad, cuánto cuesta y cuándo hace falta.',
  secs=[
   ('Cuándo se necesita realmente',
    'Cuando el terreno tiene desnivel y hay que ganar plataforma; cuando la casa queda debajo de un talud; cuando una excavación deja una cara vertical junto a la colindancia; o cuando el relleno de nivelación necesita quedar confinado. En la Riviera Maya el caso más común no es la montaña: es el terreno relleno sobre roca, donde el desnivel de un metro y medio parece inofensivo y termina empujando una barda que nunca se calculó para eso.'),
   ('Tipos y para qué sirve cada uno',
    'Gravedad en mampostería: resuelve alturas bajas con material local, económico y sencillo. Concreto armado en voladizo: es el estándar para alturas medias y el que se calcula con empuje de tierras y momento de volteo. Gaviones: flexibles, drenan solos, buenos en taludes y en obra donde importa el aspecto natural. Muro anclado o pilotes: solo cuando la altura o la cercanía a la colindancia lo obliga, y siempre con proyecto estructural firmado.'),
   ('Lo que decide el precio',
    'Altura, tipo de muro, calidad del relleno y acceso de maquinaria. La excavación en roca caliza sube el costo del desplante; el acero y el concreto mandan en el resto. Estos son los rangos de obra terminada en la región para 2026, incluyendo cimentación del muro y drenaje.'),
   ('El drenaje: la parte que casi nadie cotiza',
    'Un muro sin drenaje acumula presión hidrostática detrás y termina agrietado o volteado. Lo que debe existir: filtro de grava, geotextil que evite que el filtro se colmate, tubo perforado al pie y lloraderos a lo largo del paramento. Cuesta una fracción del muro y es la diferencia entre veinte años y dos temporadas de lluvia.'),
   ('Errores que se ven en obra',
    'Muro de block macizo usado como contención sin refuerzo ni cálculo. Relleno con material arcilloso que retiene agua y aumenta el empuje. Compactación en capas gruesas y sin control. Colar contra el talud sin cimbra ni recubrimiento suficiente, con el acero expuesto a la humedad. Y construir el muro antes de que exista el estudio de mecánica de suelos, es decir, sin saber contra qué se está trabajando.'),
  ],
  table=('Tipo de muro','Altura habitual','Costo 2026 por m² de paramento',
   [('Mampostería de gravedad','hasta 2.0 m','$2,500 – $4,500 MXN'),
    ('Concreto armado en voladizo','2.0 – 4.0 m','$3,500 – $6,500 MXN'),
    ('Gaviones','1.5 – 4.0 m','$1,800 – $3,200 MXN'),
    ('Muro anclado o con pilotes','más de 4.0 m o colindancia','Según proyecto estructural')]),
  faq=[('¿Cuánto cuesta un muro de contención de 2 metros?','Entre $3,500 y $6,500 MXN por m² de paramento en concreto armado, es decir, del orden de $7,000 a $13,000 MXN por metro lineal de muro de 2 m, con cimentación y drenaje incluidos. En mampostería de gravedad el costo baja, pero la altura útil también.'),
       ('¿Necesito cálculo estructural?','Sí, salvo muros muy bajos de jardinería. A partir de aproximadamente 1.5 m, y siempre que haya construcción arriba o abajo del talud, el muro se calcula con empuje de tierras y sobrecarga, y el plano va firmado.'),
       ('¿Por qué se agrietan los muros de contención?','Casi siempre por drenaje ausente o tapado, por relleno inadecuado, o por acero mal dimensionado en el arranque. La grieta suele aparecer en la base del paramento y crece con cada temporada de lluvias.'),
       ('¿Se puede usar la barda como muro de contención?','No, si no fue calculada para eso. Una barda resiste su propio peso y viento; un muro de contención resiste empuje horizontal de tierra saturada, que es un orden de magnitud distinto.')],
  links=[L_CIM, ('/mecanica-de-suelos/','Estudio de mecánica de suelos'), L_PROY, L_OBRA]),

'mecanica-de-suelos': dict(
  title='Mecánica de Suelos: Qué Es, Precio y Por Qué Importa | Recrea',
  desc='Estudio de mecánica de suelos en la Riviera Maya: qué incluye, cómo se hace en roca caliza, precios 2026, cuándo es obligatorio y qué pasa si construye sin él.',
  h1='Mecánica de Suelos: Qué Incluye y Cuánto Cuesta',
  lead='En roca caliza fracturada, con cavidades y manto freático somero, el estudio de suelos no es un trámite: es lo que evita cimentar sobre un hueco.',
  secs=[
   ('Qué es y qué entrega',
    'Es el estudio que determina cómo se comporta el terreno bajo la carga de su construcción. Entrega: descripción estratigráfica, capacidad de carga admisible, nivel del manto freático, recomendación del tipo de cimentación con profundidad de desplante, y criterios para excavación y relleno. Con eso el estructurista calcula; sin eso, adivina y se cubre encareciendo la cimentación.'),
   ('Cómo se hace en el suelo de la península',
    'Aquí no hay estratos blandos profundos como en el centro del país: hay caliza, sascab, rellenos y cavidades. Se combinan sondeos de penetración, pozos a cielo abierto y, cuando hay sospecha de oquedades, exploración adicional. Lo que se busca no es solo la resistencia: es detectar cavernas, zonas de relleno mal compactado y qué tan cerca queda el agua.'),
   ('Precios 2026 en la Riviera Maya',
    'Depende del número y profundidad de sondeos, y de la superficie por explorar. Estos son los rangos habituales para proyectos de la región.'),
   ('Cuándo es obligatorio',
    'Para licencia de construcción en varios municipios de Quintana Roo se solicita en obras a partir de cierta superficie o número de niveles, y el DRO lo exige para firmar. En la práctica conviene siempre: incluso una casa de una planta cambia de cimentación —y de costo— según lo que aparezca a dos metros de profundidad.'),
   ('Qué pasa si se construye sin él',
    'Dos escenarios, ambos caros. El primero: se sobredimensiona la cimentación por seguridad y se paga de más desde el día uno. El segundo: aparece una cavidad o un relleno bajo una zapata y hay que resolver en obra, con la estructura ya arriba. El estudio cuesta una fracción de cualquiera de los dos.'),
  ],
  table=('Alcance del estudio','Aplica a','Costo 2026',
   [('2 sondeos, casa unifamiliar','Terreno hasta 400 m²','$18,000 – $32,000 MXN'),
    ('3–4 sondeos, residencia grande','Terreno 400 – 1,500 m²','$30,000 – $55,000 MXN'),
    ('Estudio para edificio o hotel','Varios niveles o sótano','$60,000 – $180,000 MXN'),
    ('Exploración por cavidades','Zonas con antecedentes de oquedades','Según extensión')]),
  faq=[('¿Cuánto cuesta un estudio de mecánica de suelos para una casa?','Entre $18,000 y $32,000 MXN para una casa unifamiliar en terreno de hasta 400 m², con dos sondeos. La cifra sube con la profundidad, el número de puntos y la dificultad de acceso.'),
       ('¿Cuánto tarda?','Entre 5 y 15 días hábiles entre trabajo de campo, laboratorio e informe firmado. Conviene pedirlo apenas se cierra la compra del terreno, porque su resultado afecta al proyecto y al presupuesto.'),
       ('¿Sirve el estudio del terreno de al lado?','No. En caliza la variabilidad es alta a pocos metros: una cavidad o un relleno antiguo pueden estar en un lote y no en el contiguo. Sirve como antecedente, no como sustituto.'),
       ('¿Detecta cenotes o cavernas?','Los sondeos detectan oquedades en los puntos explorados y dan indicios de otras. Cuando el antecedente de la zona lo justifica, se amplía la exploración antes de definir la cimentación.')],
  links=[L_CIM, ('/muro-de-contencion/','Muros de contención'), L_TOPO, L_PERM]),

'microcemento': dict(
  title='Microcemento: Precio por m², Ventajas y Cuidados | Recrea',
  desc='Microcemento en la Riviera Maya: precio por m² en 2026, dónde se aplica, cómo se compara con el cemento pulido y qué cuidados exige el clima tropical.',
  h1='Microcemento: Precio por m² y Dónde Conviene',
  lead='Acabado continuo, sin juntas, de 2 a 3 mm sobre casi cualquier superficie. Bien aplicado y bien sellado dura años; mal sellado en clima costero, mucho menos.',
  secs=[
   ('Qué es exactamente',
    'Un recubrimiento a base de cemento, polímeros y áridos finos que se aplica en capas delgadas sobre firme, loseta existente, muro o incluso mueble. No es un piso estructural: es una piel continua de unos 2 a 3 mm, que se pigmenta y se sella. De ahí vienen sus dos virtudes: no tiene juntas y no obliga a demoler el piso anterior.'),
   ('Dónde funciona y dónde no',
    'Funciona muy bien en interiores, baños, escaleras, muros de sala y barras de cocina. Funciona en exteriores solo con sistema y sellador específicos para intemperie, y aun así requiere mantenimiento. Donde no conviene: dentro de la alberca, en superficies con movimiento estructural sin tratar, y sobre firmes agrietados que no se hayan estabilizado antes, porque la grieta reaparece en la superficie.'),
   ('Precio por m² en 2026',
    'Incluye preparación de superficie, capas de microcemento, pigmento y sellador. El estado del sustrato es lo que más mueve la cifra.'),
   ('Microcemento o cemento pulido',
    'No son el mismo material. El cemento pulido es la losa o el firme de concreto acabado y pulido en obra: es el propio piso, tiene espesor estructural y suele llevar juntas de control. El microcemento es un recubrimiento delgado que va encima de algo que ya existe. Para remodelar sin demoler, microcemento. Para obra nueva donde la losa será el piso, cemento pulido.'),
   ('Cuidados en clima tropical',
    'Sol, salinidad y humedad castigan cualquier sellador. En zonas costeras conviene sellador de alta resistencia UV, resellado periódico —del orden de cada 2 a 4 años según exposición—, limpieza con pH neutro y nada de ácidos ni abrasivos. Y en baños, aplicación impecable en encuentros y desagües: el punto débil nunca es el centro del piso.'),
  ],
  table=('Aplicación','Preparación necesaria','Precio 2026 por m²',
   [('Piso interior sobre firme sano','Limpieza y primario','$700 – $1,100 MXN'),
    ('Sobre loseta o piso existente','Nivelación y puente de adherencia','$900 – $1,400 MXN'),
    ('Muros y barras','Aplanado sano','$650 – $1,000 MXN'),
    ('Exterior o zona húmeda','Sistema y sellador de intemperie','$1,100 – $1,800 MXN')]),
  faq=[('¿Cuánto cuesta el microcemento por metro cuadrado?','Entre $700 y $1,400 MXN por m² instalado en interiores, según el estado del sustrato. En exterior o zonas húmedas, con sistema de intemperie, el rango sube hasta cerca de $1,800 MXN.'),
       ('¿Se puede aplicar sobre azulejo existente?','Sí, y es uno de sus usos más frecuentes en remodelación. Requiere que la loseta esté bien adherida, limpieza profunda, tratamiento de juntas y puente de adherencia. Si hay piezas sueltas, se reponen antes.'),
       ('¿Se agrieta?','El microcemento copia lo que hace su sustrato. Si el firme se mueve o ya tenía grietas activas sin tratar, aparecerán. Por eso la preparación es la mitad del trabajo y la garantía real depende de ella.'),
       ('¿Cuánto dura?','Con sellado correcto y resellado periódico, muchos años en interior. En exterior costero la vida útil del sellador es más corta y el mantenimiento deja de ser opcional.')],
  links=[('/cemento-pulido/','Cemento pulido'), L_REM, ('/blog-es/pisos-acabados-clima-tropical.html','Pisos y acabados en clima tropical'), L_PDC]),

'cemento-pulido': dict(
  title='Cemento Pulido: Precio, Acabados y Juntas | Recrea',
  desc='Piso de cemento pulido: precio por m² en 2026, cómo se ejecuta, juntas de control, sellado y en qué se diferencia del microcemento. Riviera Maya.',
  h1='Cemento Pulido: Precio por m² y Cómo se Ejecuta Bien',
  lead='El piso más noble y el más fácil de arruinar. Todo se decide en el colado y en las juntas, no en el sellador que se pone al final.',
  secs=[
   ('Qué es y cómo se ejecuta',
    'Es un firme o losa de concreto que se acaba en fresco con llana mecánica hasta obtener una superficie cerrada y uniforme, y después se sella. Se ejecuta en una sola jornada por paño: si el pulido se hace tarde, la superficie queda abierta; si se hace temprano, se levanta lechada y aparecen manchas. No es un acabado que se pueda corregir al día siguiente.'),
   ('Juntas: dónde y por qué',
    'El concreto se contrae al fraguar, y si no se le dice dónde agrietarse, elige solo. Las juntas de control se cortan a tiempo, con profundidad de aproximadamente un cuarto del espesor, formando paños regulares y respetando cambios de geometría, columnas y vanos. Un piso pulido sin juntas se ve espectacular el primer mes y agrietado al tercero.'),
   ('Precio por m² en 2026',
    'Los rangos incluyen firme, acabado pulido y sellado. Los endurecedores superficiales y los colorantes se cotizan aparte cuando se piden.'),
   ('Acabados y color',
    'Del gris natural al pulido espejo, con endurecedor superficial o con pigmento integrado. En obra real el color nunca sale idéntico de un paño a otro: la variación es parte del material y conviene aceptarla desde el principio en lugar de descubrirla al final. Muestras aprobadas en sitio antes del colado, siempre.'),
   ('Mantenimiento honesto',
    'Sellado inicial, resellado periódico y limpieza sin ácidos. El cemento pulido resiste tráfico intenso mucho mejor que un recubrimiento delgado, pero es poroso: los derrames de aceite, vino o cítricos manchan si el sellador está vencido. En cocinas y terrazas conviene sellador de mayor resistencia.'),
  ],
  table=('Alcance','Incluye','Precio 2026 por m²',
   [('Firme pulido básico','Firme, pulido, sellado','$450 – $700 MXN'),
    ('Con endurecedor superficial','Mayor resistencia y cierre','$650 – $950 MXN'),
    ('Pigmentado o pulido fino','Color integrado, acabado cerrado','$850 – $1,300 MXN'),
    ('Sobre losa existente (rectificado)','Desbaste, resane, pulido','$500 – $900 MXN')]),
  faq=[('¿Cuánto cuesta un piso de cemento pulido?','De $450 a $1,300 MXN por m² según acabado. El firme pulido básico está en el extremo bajo; el pigmentado o de pulido fino, en el alto.'),
       ('¿Cuál es la diferencia con el microcemento?','El cemento pulido es el piso mismo, con espesor estructural y juntas de control. El microcemento es un recubrimiento de 2 a 3 mm sobre algo existente, sin juntas. Para obra nueva, pulido; para remodelar sin demoler, microcemento.'),
       ('¿Se puede pulir un piso que ya está colado?','Sí, mediante rectificado: desbaste mecánico, resane y pulido. Funciona si la losa está sana y nivelada; si tiene grietas activas o desniveles fuertes, no es el camino.'),
       ('¿Es resbaloso?','Pulido y mojado, sí. En terrazas, baños y bordes de alberca se especifica un acabado menos cerrado o un sellador antiderrapante, que es lo correcto en clima de lluvia intensa.')],
  links=[('/microcemento/','Microcemento'), ('/blog-es/pisos-acabados-clima-tropical.html','Pisos y acabados en clima tropical'), L_CIM, L_OBRA]),

'humedad-en-paredes': dict(
  title='Humedad en Paredes: Causas y Solución Real | Recrea',
  desc='Humedad en paredes en clima tropical: cómo distinguir filtración, capilaridad y condensación, qué solución aplica a cada una y cuánto cuesta repararla.',
  h1='Humedad en Paredes: Cómo Identificar la Causa y Resolverla',
  lead='Pintar encima nunca ha resuelto una humedad. Primero hay que saber de dónde viene el agua: son tres orígenes distintos y tres reparaciones distintas.',
  secs=[
   ('Los tres orígenes, y cómo distinguirlos',
    'Filtración: entra agua desde afuera —azotea, fachada, tubería rota— y la mancha crece después de llover o de usar una instalación. Capilaridad: el muro absorbe humedad del suelo y la mancha aparece en la parte baja, con una franja horizontal y salitre. Condensación: el vapor del aire condensa sobre superficies frías; se ve en esquinas, detrás de muebles y en cuartos con aire acondicionado, con moho negro y sin origen externo. Identificar mal el origen es la razón número uno de reparaciones que fracasan.'),
   ('Por qué aquí es peor',
    'Humedad relativa alta casi todo el año, lluvia intensa concentrada, salinidad en la costa y muros que trabajan con temperatura de un lado y aire acondicionado del otro. En la Riviera Maya un detalle constructivo que en clima seco perdona, aquí se manifiesta en la primera temporada.'),
   ('La solución que aplica a cada caso',
    'Filtración: reparar el origen —impermeabilización de azotea, sellado de encuentros y ventanas, o la tubería— y solo después resanar. Capilaridad: barrera química inyectada en la base del muro o barrera física, retirar el aplanado contaminado con sales y reponer con mortero adecuado. Condensación: ventilación, aislamiento y corrección de puentes térmicos; ningún impermeabilizante resuelve una condensación.'),
   ('Costos de reparación 2026',
    'Rangos de la región, considerando diagnóstico, reparación del origen y reposición del acabado.'),
   ('Lo que no funciona',
    'Pintura impermeabilizante sobre humedad activa: sella el vapor adentro y salta a los meses. Impermeabilizar por dentro una filtración que viene de afuera: mueve el problema, no lo quita. Y resanar antes de que el muro esté seco, que garantiza repetir el trabajo completo.'),
  ],
  table=('Origen','Reparación típica','Costo 2026',
   [('Filtración de azotea','Impermeabilización + resane','$180 – $450 MXN/m² de azotea'),
    ('Filtración en fachada o ventanas','Sellado, resane, pintura','$250 – $600 MXN/m² afectado'),
    ('Capilaridad','Barrera química + aplanado nuevo','$800 – $1,800 MXN/m lineal'),
    ('Condensación','Ventilación y aislamiento','Según diagnóstico')]),
  faq=[('¿Cómo sé si es filtración o humedad de capilaridad?','Por dónde aparece y cuándo. La capilaridad se queda en la parte baja del muro, con una franja bastante horizontal y polvo blanco de sales, y está presente todo el año. La filtración aparece o empeora después de la lluvia y suele venir de arriba o de un punto concreto.'),
       ('¿Sirve la pintura impermeabilizante?','Como protección preventiva sobre una superficie sana, sí. Sobre una humedad activa, no: atrapa el vapor y termina desprendiéndose, además de ocultar el avance del problema.'),
       ('¿Cuánto tarda en secar un muro después de reparar?','De 2 a 6 semanas según espesor, ventilación y época del año. Resanar antes de tiempo es lo que hace que la mancha vuelva y parezca que la reparación no funcionó.'),
       ('¿El moho negro es peligroso?','Conviene tratarlo pronto: además del daño al acabado, afecta la calidad del aire interior. Se elimina la colonia, se corrige la causa —casi siempre condensación o filtración— y recién entonces se repinta.')],
  links=[L_IMP, L_REM, ('/blog-es/pisos-acabados-clima-tropical.html','Pisos y acabados en clima tropical'), L_PDC]),

'contrato-de-obra': dict(
  title='Contrato de Obra: Qué Debe Incluir y Cómo Blindarlo | Recrea',
  desc='Contrato de obra en México: cláusulas indispensables, anticipos, calendario de pagos, penalizaciones, garantías y los puntos donde se pierden las obras.',
  h1='Contrato de Obra: Cláusulas que Debe Exigir',
  lead='La mayoría de los conflictos de obra no son técnicos: son de alcance y de pagos. Un contrato bien armado los resuelve antes de que ocurran.',
  secs=[
   ('Las modalidades y qué implica cada una',
    'Precio alzado —a precio fijo por un alcance definido— traslada el riesgo de rendimiento al constructor y da previsibilidad al cliente; exige proyecto ejecutivo completo. Precios unitarios: se pactan precios por concepto y se paga lo ejecutado; sirve cuando hay cantidades inciertas. Administración: el cliente paga costo más honorario y asume el riesgo; solo funciona con supervisión propia y mucha confianza. Nosotros trabajamos a precio fijo por partidas.'),
   ('Cláusulas que no pueden faltar',
    'Alcance con el catálogo de partidas y planos anexos, identificados por fecha y versión. Monto, forma de pago y calendario ligado a avance verificable, no a fechas sueltas. Plazo con inicio, fin y causas justificadas de prórroga. Procedimiento de cambios: nada se ejecuta sin orden de cambio firmada con precio y tiempo. Penalización por atraso y su tope. Garantía de vicios ocultos. Responsabilidad por seguridad y seguro. Y las causales de rescisión con su liquidación.'),
   ('Anticipos y calendario de pagos',
    'Un anticipo razonable cubre movilización y compra inicial de material; se amortiza proporcionalmente en cada estimación en lugar de quedar suelto hasta el final. Los pagos siguientes se ligan a hitos comprobables: cimentación terminada, estructura y losas, instalaciones ocultas cerradas, acabados, entrega. Pagar por calendario sin verificar avance es lo que financia obras ajenas con su dinero.'),
   ('Órdenes de cambio: donde se descontrolan los presupuestos',
    'Todo cambio pedido por el cliente o derivado de un imprevisto debe documentarse antes de ejecutarse, con su costo y su efecto en el plazo. Sin ese mecanismo, la obra avanza a base de acuerdos verbales y al final aparece una cuenta que nadie reconoce. Con él, el precio final es explicable línea por línea.'),
   ('Garantías y entrega',
    'La entrega se hace con acta, lista de pendientes y plazo para resolverlos, más manuales, planos as-built y garantías de equipos. La garantía de vicios ocultos cubre defectos que aparecen después; conviene que el contrato diga qué cubre, por cuánto tiempo y cómo se reporta.'),
  ],
  table=('Concepto','Práctica sana','Señal de alerta',
   [('Anticipo','Amortizable en cada estimación','Anticipo alto sin amortización'),
    ('Pagos','Ligados a avance verificado','Fechas fijas sin revisión de obra'),
    ('Cambios','Orden firmada antes de ejecutar','Acuerdos verbales en sitio'),
    ('Plazo','Fechas y prórrogas definidas','Contrato sin fecha de término'),
    ('Garantía','Vicios ocultos por escrito','“Garantía” sin plazo ni alcance')]),
  faq=[('¿Cuánto anticipo es normal en una obra?','Un anticipo que cubra movilización y compra inicial, amortizado proporcionalmente en cada estimación. Lo importante no es solo el porcentaje: es que se descuente en cada pago y que esté respaldado por avance real.'),
       ('¿El contrato necesita notario?','No es requisito para su validez entre las partes. Lo que sí conviene es que esté firmado con anexos identificados —catálogo de partidas, planos, especificaciones— porque el conflicto casi siempre es sobre el alcance, no sobre la firma.'),
       ('¿Qué pasa si la obra se atrasa?','Aplica la penalización pactada, salvo causas justificadas previstas en el contrato: lluvias extraordinarias, cambios pedidos por el cliente, retrasos de trámites ajenos al constructor. Por eso el contrato debe definir qué cuenta como prórroga válida.'),
       ('¿Puedo cancelar un contrato de obra?','Sí, conforme a las causales de rescisión pactadas. La liquidación cubre lo ejecutado y verificado, materiales en sitio y, en su caso, la penalización acordada. Un contrato sin cláusula de rescisión es un contrato que solo conviene a una parte.')],
  links=[L_PRES, ('/supervision-de-obra/','Supervisión de obra'), L_PERM, L_OBRA]),

'supervision-de-obra': dict(
  title='Supervisión de Obra: Qué Revisa y Cuánto Cuesta | Recrea',
  desc='Supervisión de obra: qué revisa un supervisor, en qué momentos, qué documenta y cuánto cuesta en 2026. Especialmente útil si usted no vive en México.',
  h1='Supervisión de Obra: Qué Revisa y Cuánto Cuesta',
  lead='Supervisar no es visitar la obra: es verificar en el momento exacto lo que después queda tapado. Casi todo lo que falla se decide en cinco o seis momentos concretos.',
  secs=[
   ('Los puntos de no retorno',
    'Trazo y niveles antes de excavar. Armado de cimentación antes del colado. Armado de losa, instalaciones ahogadas y pruebas de presión antes de colar. Impermeabilización antes de cubrirla. Instalación eléctrica antes de tapar muros. Cada uno de estos momentos dura horas y condiciona la casa entera; verificarlos después implica romper.'),
   ('Qué se revisa exactamente',
    'Que lo construido corresponda al proyecto y a las especificaciones; calibre y diámetro de instalaciones; separación, diámetro y recubrimiento del acero; resistencia y revenimiento del concreto con muestreo; niveles y plomos; pendientes de desagüe; pruebas hidráulicas y eléctricas; y que los materiales entregados sean los cotizados y no un equivalente más barato.'),
   ('Qué debe documentar',
    'Bitácora con fechas, fotografías fechadas de cada etapa antes de cerrarla, resultados de pruebas de laboratorio, lista de observaciones con responsable y plazo, y control de las órdenes de cambio. Si usted vive fuera de México, este expediente es su único acceso real a lo que ocurre en el terreno.'),
   ('Cuánto cuesta',
    'La supervisión independiente se cobra como porcentaje del costo de obra o como visita programada. Cuando la misma empresa construye, la supervisión interna forma parte del servicio; la externa se contrata aparte precisamente para que sean partes distintas.'),
   ('Supervisión a distancia',
    'Buena parte de nuestros clientes están en Estados Unidos, Canadá o Europa. Lo que hace que funcione: reporte semanal con fotos y avance contra calendario, videollamada en los hitos, aprobación por escrito de cada cambio, y acceso a las pruebas de laboratorio. Lo que no funciona: fotos sueltas por mensajería sin fecha ni contexto.'),
  ],
  table=('Modalidad','Alcance','Costo 2026',
   [('Supervisión interna del constructor','Incluida en el contrato de obra','Parte del servicio'),
    ('Supervisión externa por porcentaje','Presencia continua y bitácora','3% – 7% del costo de obra'),
    ('Visitas programadas en hitos','5 a 8 visitas con reporte','$4,500 – $9,000 MXN por visita'),
    ('Reporte semanal a distancia','Fotos fechadas, avance, pruebas','Según duración de obra')]),
  faq=[('¿Cuánto cuesta supervisar una obra?','Entre 3% y 7% del costo de obra en supervisión externa continua, o por visita programada cuando solo se requieren los hitos críticos. La cifra depende de la duración y de la distancia a la obra.'),
       ('¿Vale la pena si ya contraté un constructor serio?','Depende de su tolerancia al riesgo y de si puede estar presente. Con contrato a precio fijo, partidas claras y reportes fotográficos, muchos clientes no contratan supervisión externa. Si usted está fuera del país y la obra es grande, el costo se justifica solo.'),
       ('¿Puedo supervisar yo mismo desde el extranjero?','Parcialmente. Puede exigir reportes, fotos fechadas y pruebas de laboratorio, y aprobar cambios por escrito. Lo que no puede hacer a distancia es verificar un armado antes del colado; eso requiere alguien de su confianza en sitio ese día.'),
       ('¿Qué documentos debo pedir al final?','Planos as-built, manuales y garantías de equipos, resultados de pruebas, acta de entrega con lista de pendientes y el cierre de cada orden de cambio.')],
  links=[('/contrato-de-obra/','Contrato de obra'), L_PRES, L_PERM, L_OBRA]),

'uso-de-suelo': dict(
  title='Uso de Suelo: Qué Es y Cómo Consultarlo en QRoo | Recrea',
  desc='Uso de suelo en Quintana Roo: qué es la constancia, cómo se consulta antes de comprar un terreno, qué limita —densidad, altura, COS y CUS— y cuánto cuesta.',
  h1='Uso de Suelo: Qué Es y Cómo Verificarlo Antes de Comprar',
  lead='El uso de suelo define qué puede construir en ese terreno, cuánto y de qué altura. Se consulta antes de firmar la compra, no después de encargar los planos.',
  secs=[
   ('Qué define y con qué palabras',
    'El programa de desarrollo urbano de cada municipio asigna a cada predio un uso —habitacional, mixto, turístico, comercial, conservación— y con él una serie de límites: densidad (viviendas o cuartos por hectárea), COS (cuánto del terreno puede ocupar el desplante), CUS (cuánta superficie total puede construir), altura máxima en niveles, y restricciones frontales y laterales. Esos cinco números deciden la rentabilidad de un proyecto antes que cualquier diseño.'),
   ('Cómo se consulta',
    'Se solicita la constancia de uso de suelo o el dictamen correspondiente en la dirección de desarrollo urbano del municipio, con los datos del predio: clave catastral, superficie y ubicación. Existen también consultas cartográficas en línea según el municipio, útiles como referencia previa, pero el documento que sirve para proyectar y para tramitar es el que emite la autoridad.'),
   ('Qué revisar antes de comprar',
    'Que el uso permita lo que usted quiere hacer —una renta vacacional no siempre cabe en un uso estrictamente habitacional—; la densidad, si piensa en más de una unidad; COS y CUS contra el programa arquitectónico; la altura; si el predio toca área natural protegida, zona federal marítimo terrestre o derecho de vía; y si existen restricciones adicionales del fraccionamiento, que suelen ser más estrictas que el municipio.'),
   ('Costos y tiempos habituales',
    'Varían por municipio y por superficie del predio. Estos son los órdenes de magnitud con los que trabajamos en la región.'),
   ('Los errores caros',
    'Comprar por el precio del metro cuadrado sin ver el uso. Suponer que porque el vecino construyó tres niveles usted también puede. Ignorar el reglamento del fraccionamiento. Y encargar el proyecto antes de tener la constancia: rediseñar por densidad o altura cuesta tiempo y honorarios que se pudieron evitar con un trámite de días.'),
  ],
  table=('Trámite','Para qué sirve','Costo y tiempo aproximados',
   [('Constancia de uso de suelo','Confirma uso, densidad, COS, CUS y altura','$1,500 – $6,000 MXN · 5–15 días'),
    ('Constancia de alineamiento y número oficial','Define límites y frente del predio','$800 – $3,500 MXN · 5–10 días'),
    ('Factibilidad de servicios','Agua, drenaje y energía disponibles','Según organismo · 2–6 semanas'),
    ('Licencia de construcción','Autoriza la obra, con proyecto y DRO','Según superficie · 3–10 semanas')]),
  faq=[('¿Cómo saber el uso de suelo de un terreno?','Solicitando la constancia de uso de suelo en la dirección de desarrollo urbano del municipio con la clave catastral del predio. Las consultas cartográficas en línea sirven como referencia previa, pero el documento oficial es el que vale para proyectar y tramitar.'),
       ('¿Se puede cambiar el uso de suelo?','Existen procedimientos de cambio o de dictamen específico, pero no son rápidos ni seguros y dependen del programa de desarrollo urbano vigente. Comprar un terreno apostando a un cambio de uso es tomar un riesgo, no hacer un plan.'),
       ('¿Qué son COS y CUS?','COS es el coeficiente de ocupación del suelo: qué proporción del terreno puede ocupar el desplante de la construcción. CUS es el coeficiente de utilización: cuánta superficie total puede construir sumando niveles. Juntos limitan el tamaño real del proyecto.'),
       ('¿El reglamento del fraccionamiento puede ser más estricto que el municipio?','Sí, y con frecuencia lo es: retiros mayores, altura menor, materiales y colores obligatorios, tiempos de obra y horarios. Se revisa junto con el uso de suelo, antes de diseñar.')],
  links=[L_PERM, ('/gestoria-tramites-construccion-riviera-maya/','Gestoría de trámites'), L_PROY, L_OBRA]),

'director-responsable-de-obra': dict(
  title='Director Responsable de Obra (DRO): Qué Hace y Costo | Recrea',
  desc='Director Responsable de Obra en Quintana Roo: qué firma, qué responsabilidad asume, cuándo es obligatorio y cuánto cobra en 2026.',
  h1='Director Responsable de Obra (DRO): Qué Hace y Cuánto Cuesta',
  lead='El DRO es quien responde ante el municipio por que la obra cumpla el reglamento. Sin su firma no hay licencia, y con una firma prestada no hay respaldo real.',
  secs=[
   ('Qué es y qué asume',
    'Es el profesional —arquitecto o ingeniero— registrado ante el municipio que avala que el proyecto y la ejecución cumplen el reglamento de construcción. Firma la solicitud de licencia y el proyecto, asume responsabilidad ante la autoridad y debe estar enterado de lo que se construye. Su registro es personal y se renueva; el municipio puede sancionarlo, lo cual es exactamente lo que le da valor a su firma.'),
   ('Cuándo es obligatorio',
    'Para obtener licencia de construcción en los municipios de Quintana Roo, en obra nueva y en ampliaciones a partir de las superficies que fija cada reglamento. También se requiere para regularizar construcciones existentes y, según el caso, para demoliciones. Remodelaciones menores sin afectar estructura suelen tramitarse con requisitos más simples, pero conviene confirmarlo por municipio.'),
   ('Qué debe pedirle',
    'Copia de su registro vigente ante el municipio; que revise el proyecto antes de firmarlo, no solo que lo firme; que esté disponible durante la obra para las visitas y para responder requerimientos; y que quede claro por escrito qué incluye su honorario —trámite, visitas, terminación de obra— y qué no.'),
   ('Honorarios 2026',
    'Varían por superficie, complejidad y municipio. Estos son los rangos habituales en la Riviera Maya para obra residencial.'),
   ('La firma prestada',
    'Existe la práctica de conseguir una firma sin que el profesional pise la obra. Es más barata y deja al propietario sin respaldo: ante un requerimiento, una sanción o un problema estructural, nadie responde y la irregularidad se convierte en un obstáculo el día de vender. Cuando el constructor gestiona el DRO, conviene igualmente saber quién es y ver su registro.'),
  ],
  table=('Tipo de obra','Alcance del DRO','Honorario 2026',
   [('Casa unifamiliar hasta 200 m²','Firma de proyecto, trámite y visitas','$25,000 – $60,000 MXN'),
    ('Residencia 200 – 500 m²','Incluye seguimiento y terminación','$50,000 – $120,000 MXN'),
    ('Edificio o desarrollo','Según niveles y superficie','Por proyecto'),
    ('Regularización de obra existente','Levantamiento, dictamen y trámite','Según estado de la construcción')]),
  faq=[('¿Cuánto cobra un DRO?','Para una casa unifamiliar en la Riviera Maya, del orden de $25,000 a $60,000 MXN según superficie y municipio, incluyendo firma del proyecto, trámite y visitas. En residencias grandes el honorario escala con la superficie.'),
       ('¿El constructor incluye el DRO?','En nuestros contratos el trámite y el DRO se cotizan de forma explícita, dentro o fuera del precio de obra según el caso, pero siempre identificados. Si un presupuesto no dice quién paga el DRO, esa partida aparecerá después.'),
       ('¿Puedo construir sin DRO?','No para obtener licencia. Construir sin licencia expone a suspensión de obra, multas y a un problema de regularización que reaparece al vender o al escriturar.'),
       ('¿El DRO supervisa la obra?','Responde ante la autoridad por el cumplimiento del reglamento y realiza visitas, pero eso no equivale a supervisión técnica continua ni a control de calidad de acabados. Son funciones distintas.')],
  links=[L_PERM, ('/uso-de-suelo/','Uso de suelo y constancias'), ('/supervision-de-obra/','Supervisión de obra'), L_OBRA]),

'pergola-de-madera': dict(
  title='Pérgola de Madera: Precio, Maderas y Duración | Recrea',
  desc='Pérgola de madera en clima tropical: qué maderas resisten, precio por m² en 2026, cimentación, cubiertas y mantenimiento real en la Riviera Maya.',
  h1='Pérgola de Madera: Precio por m² y Qué Madera Aguanta',
  lead='En la Riviera Maya la pérgola no la mata el sol: la matan la humedad, la termita y el anclaje mal resuelto. La madera correcta cambia todo.',
  secs=[
   ('Qué maderas funcionan aquí',
    'Tzalam y chechén: duras, densas, de excelente comportamiento a la intemperie y estéticamente asociadas a la región. Chicozapote: durísima y muy resistente, tradicional en estructuras y palapas. Pino tratado en autoclave: la opción económica, aceptable si el tratamiento es real y penetrante, no un baño superficial. Lo que no funciona: madera de pino sin tratar, que en clima húmedo con termita dura poco y falla justo en los apoyos.'),
   ('Anclaje y cimentación: donde fallan',
    'La madera nunca debe apoyarse directamente sobre el piso ni quedar ahogada en concreto: se ancla con placa metálica galvanizada o de acero inoxidable, separada del piso para que el agua escurra y la pieza ventile. En zona costera el herraje galvanizado corriente se oxida rápido; el inoxidable cuesta más y es la diferencia entre revisar el anclaje o rehacerlo.'),
   ('Precios 2026 por m² cubierto',
    'Estructura, herrajes, tratamiento y acabado incluidos. La cubierta y la iluminación se cotizan aparte cuando se piden.'),
   ('Cubiertas: qué se pone encima',
    'Listones de la misma madera para sombra parcial; huano o palma para la estética regional, con mantenimiento propio; policarbonato o lámina traslúcida cuando se busca protección de lluvia; tela tensada o toldo retráctil cuando se quiere flexibilidad. La elección cambia la estructura: una cubierta sólida obliga a calcular carga de viento en serio, especialmente en temporada de huracanes.'),
   ('Mantenimiento honesto',
    'Limpieza y reaplicación de aceite o sellador cada 12 a 24 meses según exposición al sol y a la sal; revisión anual de herrajes y de los puntos de apoyo; y tratamiento preventivo contra termita. Una pérgola de madera dura que se mantiene supera fácilmente la década; sin mantenimiento, se ve castigada en dos o tres temporadas.'),
  ],
  table=('Material','Características','Precio 2026 por m² cubierto',
   [('Pino tratado en autoclave','Económico, requiere más mantenimiento','$2,200 – $3,800 MXN'),
    ('Tzalam o chechén','Dura, estable, estética regional','$3,500 – $7,000 MXN'),
    ('Chicozapote','Máxima durabilidad, disponibilidad limitada','$5,000 – $9,000 MXN'),
    ('Madera + cubierta sólida','Policarbonato o lámina, con cálculo de viento','Suma $900 – $2,500 MXN')]),
  faq=[('¿Cuánto cuesta una pérgola de madera?','Entre $2,200 y $7,000 MXN por m² cubierto según la madera, más la cubierta si se agrega. Una pérgola de 4×4 m en tzalam se ubica aproximadamente entre $56,000 y $112,000 MXN de estructura terminada.'),
       ('¿Qué madera aguanta más en la costa?','Chicozapote y tzalam son las más resistentes de la región. Con herraje inoxidable y anclaje separado del piso, el conjunto aguanta el clima; el punto débil casi nunca es la madera sino la unión.'),
       ('¿Aguanta un huracán?','Depende del cálculo y de la cubierta. Una pérgola abierta con listones ofrece poca superficie al viento; una cubierta sólida se convierte en una vela y exige anclaje y estructura diseñados para ello. Es una decisión de proyecto, no de carpintería.'),
       ('¿Cada cuánto hay que darle mantenimiento?','Reaplicación de aceite o sellador cada 12 a 24 meses según exposición, más revisión anual de herrajes y tratamiento antitermita. En primera línea de playa, en el extremo corto del rango.')],
  links=[('/deck-de-madera/','Deck de madera'), L_CARP, ('/blog-es/guia-construccion-palapas.html','Construcción de palapas'), L_PDC]),

'deck-de-madera': dict(
  title='Deck de Madera: Precio por m², Materiales y Cuidado | Recrea',
  desc='Deck de madera en la Riviera Maya: precio por m² en 2026, madera dura contra WPC, estructura, ventilación y mantenimiento real junto a alberca y mar.',
  h1='Deck de Madera: Precio por m² y Qué Material Elegir',
  lead='Junto a una alberca o frente al mar, el deck vive en el peor escenario posible: agua, sal, sol y humedad por debajo. Se resuelve en la estructura, no en la duela.',
  secs=[
   ('Madera dura o composite (WPC)',
    'Madera dura tropical —tzalam, chechén, ipé— da el mejor aspecto y envejece con carácter, pero exige aceite periódico y acepta que el color cambie. El WPC o composite resiste mejor humedad y termita, no necesita aceite y mantiene el color, aunque calienta más al sol directo y se ve como lo que es. Para alberca, ambos funcionan; la decisión suele ser cuánto mantenimiento está dispuesto a hacer.'),
   ('La estructura es lo que dura',
    'Rastreles separados y ventilados, nunca apoyados directamente sobre losa sin ventilación; pendiente para desagüe; herrajes inoxidables junto al mar; y separación entre duelas para que el agua pase y la madera se mueva. Un deck bien ventilado por debajo dura el doble que el mismo material mal apoyado, y esa diferencia no se ve en la foto ni en la cotización barata.'),
   ('Precios 2026 por m²',
    'Estructura, fijación y acabado incluidos. La preparación del sustrato se cotiza aparte cuando hay que nivelar o impermeabilizar.'),
   ('Deck junto a alberca',
    'El agua clorada o salina cae todos los días. Ahí conviene madera muy densa o WPC, fijación inoxidable, ligera pendiente hacia el desagüe y sellador adecuado. El borde de la alberca merece atención propia: es donde se pisa mojado y donde el material se degrada primero.'),
   ('Mantenimiento y vida útil',
    'Madera dura: limpieza y aceite cada 12 a 18 meses; si se deja envejecer sin aceite, adquiere tono plateado sin perder integridad, pero conviene revisar fijaciones. WPC: lavado, sin aceite. En ambos casos, revisión anual de la estructura por debajo, que es donde empieza cualquier problema serio.'),
  ],
  table=('Material','Mantenimiento','Precio 2026 por m² instalado',
   [('Pino tratado','Aceite anual, vida media','$1,400 – $2,200 MXN'),
    ('Tzalam o chechén','Aceite cada 12–18 meses','$2,500 – $4,200 MXN'),
    ('Ipé u otra madera premium','Aceite periódico, muy durable','$3,800 – $6,000 MXN'),
    ('WPC / composite','Solo lavado','$1,900 – $3,400 MXN')]),
  faq=[('¿Cuánto cuesta un deck de madera por m²?','De $1,400 a $6,000 MXN por m² instalado según material, con la madera dura tropical entre $2,500 y $4,200 y el composite entre $1,900 y $3,400.'),
       ('¿Qué es mejor junto a la alberca, madera o WPC?','Ambos funcionan si la estructura ventila y la fijación es inoxidable. WPC si prefiere no dar mantenimiento; madera dura si prefiere el aspecto y acepta aceitarla. El WPC oscuro calienta más al sol de mediodía.'),
       ('¿Cuánto dura un deck aquí?','Con material adecuado, estructura ventilada y mantenimiento, del orden de 10 a 20 años en madera dura. Mal ventilado por debajo, el mismo material puede empezar a fallar en 3 o 4 años.'),
       ('¿Se puede poner deck sobre una losa existente?','Sí, con rastreles que dejen cámara de aire y con la impermeabilización de la losa revisada antes. Colocar duela directamente sobre la losa es la forma más rápida de arruinar tanto el deck como la impermeabilización.')],
  links=[('/pergola-de-madera/','Pérgola de madera'), ('/albercas-de-lujo-playa-del-carmen/','Albercas'), L_CARP, L_PDC]),

'ventanas-de-aluminio': dict(
  title='Ventanas de Aluminio: Precio por m² y Qué Serie Elegir | Recrea',
  desc='Ventanas de aluminio en la Riviera Maya: precio por m² en 2026, series, cristal templado y control solar, hermeticidad y resistencia a huracán y salinidad.',
  h1='Ventanas de Aluminio: Precio por m² y Qué Serie Elegir',
  lead='La ventana define cuánto calor entra, cuánto ruido pasa y qué tan tranquilo se duerme en temporada de huracanes. Es de las peores partidas para ahorrar.',
  secs=[
   ('Series y para qué sirve cada una',
    'Serie ligera: económica, adecuada para vanos pequeños en interiores protegidos, poca hermeticidad. Serie intermedia: el estándar residencial razonable, con mejor sellado y perfiles más robustos. Serie estructural o pesada: para vanos grandes, corredizas de gran formato y zonas expuestas al viento; es la que permite las fachadas abiertas que se buscan aquí. La serie manda tanto como el cristal.'),
   ('El cristal es la mitad de la decisión',
    'Templado por seguridad, obligado en puertas y paños bajos. Control solar para reducir la carga térmica que después paga el aire acondicionado. Doble cristal cuando importa el ruido o la eficiencia. Laminado cuando se busca resistencia a impacto y seguridad. En una casa orientada al poniente, el cristal correcto ahorra más al año que casi cualquier otro ajuste de fachada.'),
   ('Precios 2026 por m² de vano',
    'Instalación incluida. Los herrajes de alta gama, las mallas y las persianas se cotizan aparte.'),
   ('Salinidad y huracanes',
    'Frente al mar, los herrajes comunes se corroen y las guías se traban en pocos años: conviene acabado anodizado o pintura electrostática de calidad, herraje inoxidable y mantenimiento de guías. Para temporada de huracanes, las opciones reales son cristal laminado de impacto, persianas o paneles de protección; una ventana corriente con cinta adhesiva no protege nada.'),
   ('Instalación: el detalle que filtra',
    'La mayoría de las filtraciones por ventana no vienen del cristal sino del encuentro con el muro: sellado perimetral deficiente, ausencia de goterón y falta de pendiente en el alféizar. Un buen producto mal instalado gotea igual que uno malo, y la mancha aparece en el interior después de la primera lluvia con viento.'),
  ],
  table=('Tipo','Uso recomendado','Precio 2026 por m² instalado',
   [('Serie ligera, cristal claro','Vanos pequeños, interiores','$1,800 – $3,000 MXN'),
    ('Serie intermedia, templado','Estándar residencial','$3,000 – $5,000 MXN'),
    ('Serie estructural, control solar','Vanos grandes, exposición alta','$5,000 – $9,000 MXN'),
    ('Cristal laminado de impacto','Zonas costeras expuestas','$8,000 – $15,000 MXN')]),
  faq=[('¿Cuánto cuesta una ventana de aluminio por m²?','De $1,800 a $9,000 MXN por m² instalado según serie y cristal, y hasta cerca de $15,000 con cristal laminado de impacto para zona costera expuesta.'),
       ('¿Vale la pena el cristal de control solar?','En esta latitud, sí, sobre todo en fachadas poniente y sur. Reduce la carga térmica y por tanto el consumo del aire acondicionado durante todo el año, que es el gasto operativo dominante de una casa aquí.'),
       ('¿Aluminio o PVC?','El aluminio con serie adecuada y acabado anticorrosivo domina el mercado local por disponibilidad, servicio y comportamiento en vanos grandes. El PVC aísla mejor térmicamente pero tiene menos oferta y servicio en la región.'),
       ('¿Qué mantenimiento necesitan frente al mar?','Lavado con agua dulce de perfiles y guías, revisión y lubricación de herrajes, y verificación anual del sellado perimetral. Sin eso, la corrosión se lleva primero los herrajes y luego el funcionamiento.')],
  links=[('/blog-es/ventanas-puertas-clima-tropical.html','Ventanas y puertas en clima tropical'), ('/aire-acondicionado-playa-del-carmen/','Aire acondicionado'), L_CARP, L_PDC]),

'captacion-de-agua-de-lluvia': dict(
  title='Captación de Agua de Lluvia: Sistema y Costo 2026 | Recrea',
  desc='Sistema de captación de agua de lluvia para casa en la Riviera Maya: cuánta agua se puede captar, componentes, filtración, costos 2026 y mantenimiento.',
  h1='Captación de Agua de Lluvia: Cómo se Diseña y Cuánto Cuesta',
  lead='Aquí llueve mucho y concentrado. Un sistema bien dimensionado cubre buena parte del consumo no potable del año; uno improvisado se llena de sedimento en dos meses.',
  secs=[
   ('Cuánta agua se puede captar realmente',
    'La regla práctica: superficie de captación en m² × precipitación anual en milímetros × un coeficiente de pérdida de aproximadamente 0.8 da los litros al año. Con la precipitación de la Riviera Maya, una azotea de 100 m² puede rendir del orden de 80,000 a 110,000 litros anuales. El límite no suele ser la lluvia: es el volumen de almacenamiento que decida construir y la estacionalidad, porque casi todo cae en unos pocos meses.'),
   ('Los componentes que no pueden faltar',
    'Superficie de captación limpia; canaletas y bajadas dimensionadas para lluvia intensa; separador de primeras aguas, que descarta el arrastre inicial de polvo y hojas; filtro de sedimentos; cisterna o aljibe con acceso para limpieza; bombeo; y, si el agua se destinará a usos que lo requieran, tratamiento adicional. Saltarse el separador de primeras aguas es la causa más común de agua turbia y cisterna sucia.'),
   ('Costos 2026',
    'Depende sobre todo del almacenamiento, que es la partida dominante. Estos son los rangos de sistemas residenciales en la región.'),
   ('Para qué se usa el agua captada',
    'Riego, lavado, sanitarios y alberca son los usos naturales, y ya representan una parte importante del consumo doméstico. Para consumo humano se requiere tratamiento y control, y conviene evaluarlo con honestidad en lugar de venderlo como automático. En una casa con jardín y alberca, cubrir el uso no potable ya cambia la factura.'),
   ('Mantenimiento',
    'Limpieza de canaletas antes de la temporada de lluvias; purga del separador de primeras aguas; cambio o lavado de filtros; y limpieza de cisterna al menos una vez al año. Es un sistema simple, pero deja de funcionar sin estas rutinas y la calidad del agua cae rápido.'),
  ],
  table=('Sistema','Almacenamiento','Costo 2026',
   [('Básico para riego','Tanque 2,500 – 5,000 L','$25,000 – $55,000 MXN'),
    ('Residencial con filtración','Cisterna 10,000 L','$60,000 – $120,000 MXN'),
    ('Integrado a la casa','Cisterna 20,000 L + bombeo','$120,000 – $250,000 MXN'),
    ('Con tratamiento avanzado','Según uso previsto','Por proyecto')]),
  faq=[('¿Cuánta agua de lluvia puedo captar en una casa?','Con una azotea de 100 m² y la precipitación de la Riviera Maya, del orden de 80,000 a 110,000 litros al año. Cuánta puede aprovechar depende del volumen de cisterna, porque la lluvia se concentra en pocos meses.'),
       ('¿Se puede beber?','No sin tratamiento. Para riego, lavado, sanitarios y alberca es directamente aprovechable con filtración adecuada; para consumo humano se requiere tratamiento específico y control periódico de calidad.'),
       ('¿Cuánto cuesta un sistema de captación?','De $25,000 MXN para un sistema básico de riego a $250,000 MXN para uno integrado a la casa con cisterna grande y bombeo. La cisterna es la partida que domina el costo.'),
       ('¿Conviene combinarlo con la cisterna de la casa?','Sí, y es lo más eficiente cuando se prevé desde el proyecto: una cisterna bien dimensionada, con entrada separada para lluvia y su filtración, evita duplicar obra civil.')],
  links=[('/pozo-de-absorcion/','Pozo de absorción y tratamiento'), ('/paneles-solares-riviera-maya/','Paneles solares'), L_OBRA, L_PROY]),

'grietas-en-muros': dict(
  title='Grietas en Muros: Cuáles Son Peligrosas y Cómo Reparar | Recrea',
  desc='Grietas en muros: cómo distinguir una fisura superficial de una grieta estructural, qué las causa en la Riviera Maya, cómo se reparan y cuánto cuesta.',
  h1='Grietas en Muros: Cuáles Preocupan y Cómo se Reparan',
  lead='No todas las grietas importan, pero algunas son un aviso. La diferencia se lee en la dirección, el ancho y en si sigue creciendo.',
  secs=[
   ('Cómo leer una grieta',
    'Fisuras finas, superficiales y ramificadas en el aplanado suelen ser retracción del mortero: molestas, no graves. Preocupan las diagonales que arrancan en esquinas de puertas y ventanas, las que atraviesan el muro de lado a lado, las que superan aproximadamente 3 mm de ancho, las horizontales continuas en la base y cualquiera que siga creciendo mes a mes o que aparezca acompañada de desnivel en pisos y puertas que dejan de cerrar.'),
   ('Causas frecuentes en esta región',
    'Asentamiento diferencial de la cimentación, muchas veces por relleno mal compactado o por una cavidad en la caliza. Movimiento térmico en muros largos sin junta constructiva. Falta de castillo o dala donde correspondía. Sobrecarga no prevista. Y humedad prolongada que degrada el mortero. Cada causa tiene una reparación distinta y ninguna se resuelve con resane.'),
   ('Cómo se repara según el caso',
    'Fisura de retracción: apertura en V, resane con mortero adecuado, malla si es extensa y repintado. Grieta activa: primero se detiene la causa —refuerzo de cimentación, junta constructiva, drenaje— y solo después se repara. Grieta estructural: dictamen, proyecto de refuerzo y ejecución; puede implicar recimentación, encamisado o costillas de refuerzo. Los testigos de yeso o los medidores permiten confirmar en semanas si la grieta sigue viva.'),
   ('Costos orientativos 2026',
    'La reparación cosmética es barata; lo que cuesta es corregir la causa cuando es estructural.'),
   ('Cuándo llamar de inmediato',
    'Grietas que crecen visiblemente en semanas, aberturas mayores a un centímetro, muros desplomados, pisos que se desnivelan, puertas y ventanas que dejan de cerrar, o grietas nuevas tras una excavación vecina. En esos casos el resane no solo es inútil: oculta la evidencia justo cuando hace falta verla.'),
  ],
  table=('Tipo de grieta','Gravedad','Reparación y costo 2026',
   [('Fisura de retracción en aplanado','Baja','Resane y pintura · $150 – $400 MXN/m'),
    ('Grieta en encuentro de materiales','Media','Malla, resane, junta · $300 – $700 MXN/m'),
    ('Grieta diagonal en esquinas de vanos','Alta','Dictamen previo · según causa'),
    ('Grieta estructural o desplome','Muy alta','Proyecto de refuerzo · por proyecto')]),
  faq=[('¿Cuándo una grieta es peligrosa?','Cuando es diagonal desde esquinas de puertas o ventanas, atraviesa el muro, supera unos 3 mm, o sigue creciendo. También cuando viene acompañada de pisos desnivelados o puertas que dejan de cerrar.'),
       ('¿Cómo sé si la grieta sigue activa?','Con testigos: se coloca una marca de yeso o un medidor sobre la grieta y se observa durante algunas semanas. Si el testigo se rompe o la medida cambia, la grieta está viva y resanar sería perder el trabajo.'),
       ('¿Cuánto cuesta reparar una grieta?','De $150 a $700 MXN por metro lineal cuando es superficial. Si es estructural, el costo lo determina la corrección de la causa —cimentación, refuerzo, drenaje— y no la grieta en sí.'),
       ('¿Puedo solo taparla con resanador?','Solo si es una fisura de retracción inactiva. En una grieta activa el resane se vuelve a abrir en semanas y, peor, oculta la evolución del problema.')],
  links=[('/mecanica-de-suelos/','Mecánica de suelos'), ('/humedad-en-paredes/','Humedad en paredes'), L_REM, L_CIM]),
}

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src = open(kw1.TPL, encoding='utf-8').read()
    for slug, d in PAGES.items():
        os.makedirs(slug, exist_ok=True)
        html = kw1.build(slug, d, src)
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        flag = '' if len(d['title']) <= 65 and len(d['desc']) <= 165 else '   <-- CHECK'
        print('%-30s title %2d  desc %3d%s' % (slug + '/', len(d['title']), len(d['desc']), flag))
