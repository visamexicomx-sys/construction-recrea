#!/usr/bin/env python3
"""Third batch of keyword-gap pages (Semrush MX, checked 2026-08-14).

Search Console gaps are exhausted — every query that already earns impressions
without a page of its own now has one. So this batch goes back to Semrush, with
seeds in areas the site had never touched. Each was verified as having no page
targeting it in a title before being written. Monthly volume, MX:

  roof garden           18,100  KD 37     escaleras de concreto  4,400  KD 28
  casas de madera       18,100  KD 45     jacuzzi exterior       3,600  KD 24
  muro verde             2,900  KD 24     barda perimetral       2,400  KD 19
  porton automatico      1,900  KD 25     instalacion electrica  1,300  KD 28
  domo de policarbonato    880  KD 30     iluminacion arq.         720  KD 15
  riego automatico         590  KD 29     estudio topografico      480  KD  9

The wooden-house page is written the honest way: in this climate, with termites
and 80% humidity, a timber house is usually the wrong answer, and the page says
so before it quotes a price. We would rather lose that job than build it badly.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'kw1', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-keyword-pages.py'))
kw1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kw1)

L_OBRA = ('/construccion-de-casas-riviera-maya/', 'Construcción de casas en la Riviera Maya')
L_PDC = ('/construccion-de-casas-playa-del-carmen/', 'Construcción de casas en Playa del Carmen')
L_REM = ('/remodelacion-casas-playa-del-carmen/', 'Remodelación de casas')
L_CARP = ('/carpinteria-y-herreria-playa-del-carmen/', 'Carpintería y herrería')
L_IMP = ('/impermeabilizacion-techos-playa-del-carmen/', 'Impermeabilización de techos')
L_PRES = ('/presupuesto-de-obra/', 'Presupuesto de obra por partidas')
L_PROY = ('/proyecto-arquitectonico/', 'Proyecto arquitectónico')
L_CIM = ('/cimentacion-y-losas-playa-del-carmen/', 'Cimentación y losas')
L_TOPO = ('/topografia-y-planos-riviera-maya/', 'Topografía y planos')
L_GUI = ('/guias/', 'Todas las guías técnicas')

PAGES = {

'roof-garden': dict(
  title='Roof Garden: Costo por m², Estructura y Cuidados | Recrea',
  desc='Roof garden en clima tropical: cuánto pesa, qué refuerzo y qué impermeabilización necesita, precio por m² en 2026 y mantenimiento real en la Riviera Maya.',
  h1='Roof Garden: Cuánto Cuesta y Qué Exige la Losa',
  lead='Un roof garden no es jardinería sobre una azotea: es carga permanente, agua retenida y una impermeabilización que ya no se puede revisar fácilmente. Se decide en la estructura.',
  secs=[
   ('Extensivo o intensivo: dos proyectos distintos',
    'Extensivo: sustrato delgado, vegetación baja de bajo mantenimiento, poco peso, transitable solo para servicio. Intensivo: sustrato profundo, arbustos y hasta árboles pequeños, área de estar, riego y mucho más peso. El primero se puede plantear sobre muchas losas existentes; el segundo casi siempre exige que la estructura se haya diseñado para ello desde el principio.'),
   ('El peso, que es donde se decide todo',
    'El sustrato saturado de agua pesa mucho más que seco, y en la Riviera Maya la lluvia llega concentrada. Un sistema extensivo típico ronda los 100 a 180 kg/m² saturado; uno intensivo puede superar los 400 kg/m². Antes de cotizar plantas hay que saber para cuánta carga viva se calculó la losa, y si no consta, revisarlo con un estructurista. Es la parte que nadie quiere pagar y la única que no se puede omitir.'),
   ('Las capas, en orden',
    'Impermeabilización de alto desempeño; barrera antirraíz; capa drenante con retención; geotextil filtrante; sustrato ligero; vegetación. Más el drenaje pluvial con registros accesibles y el riego. Saltarse la barrera antirraíz es garantizar que en dos o tres años las raíces encuentren la impermeabilización, y esa reparación implica levantar el jardín completo.'),
   ('Costos 2026',
    'Rangos por m² de azotea intervenida, incluyendo impermeabilización, capas de sistema, sustrato y plantación. El refuerzo estructural, cuando hace falta, se cotiza aparte.'),
   ('Qué mantenimiento pide de verdad',
    'Riego —automático, si quiere que sobreviva a marzo y abril—, poda, reposición de plantas, limpieza de drenajes antes de la temporada de lluvias y revisión anual de registros. Un roof garden abandonado seis meses en este clima no se ve descuidado: se muere y deja el sustrato como una carga muerta empapada sobre su losa.'),
  ],
  table=('Sistema','Peso saturado aproximado','Costo 2026 por m²',
   [('Extensivo, vegetación baja','100 – 180 kg/m²','$1,200 – $2,500 MXN'),
    ('Semi-intensivo, arbustos','200 – 350 kg/m²','$2,200 – $3,800 MXN'),
    ('Intensivo con área de estar','350 kg/m² en adelante','$3,500 – $6,500 MXN'),
    ('Refuerzo estructural, si aplica','Según proyecto','Por proyecto')]),
  faq=[('¿Cuánto cuesta un roof garden por metro cuadrado?','De $1,200 a $2,500 MXN por m² en sistema extensivo y de $3,500 a $6,500 MXN por m² en intensivo con área de estar, incluyendo impermeabilización y plantación.'),
       ('¿Aguanta mi losa un roof garden?','Depende de la carga viva para la que se calculó. Un sistema extensivo cabe en muchas losas residenciales; uno intensivo casi siempre requiere revisión estructural y, con frecuencia, refuerzo.'),
       ('¿No se filtra el agua a la casa?','No, si el sistema está bien ejecutado: impermeabilización de alto desempeño, barrera antirraíz y drenaje con registros accesibles. Las filtraciones aparecen cuando se ahorra en alguna de esas tres.'),
       ('¿Cuánto mantenimiento necesita?','Riego constante, poda, limpieza de drenajes antes de lluvias y revisión anual. Con riego automático el trabajo baja mucho; sin riego, en la temporada seca no sobrevive.')],
  links=[L_IMP, ('/riego-automatico/','Riego automático'), ('/muro-verde/','Muro verde'), L_CIM]),

'muro-verde': dict(
  title='Muro Verde: Precio por m², Natural o Artificial | Recrea',
  desc='Muro verde natural o artificial en la Riviera Maya: precio por m² en 2026, sistema de riego, qué plantas aguantan el clima y cuánto mantenimiento pide cada opción.',
  h1='Muro Verde: Precio por m² y Qué Sistema Elegir',
  lead='Un muro verde natural es un jardín vertical con riego: espectacular y exigente. Uno artificial es decoración: constante y sin vida. Conviene saber cuál está comprando.',
  secs=[
   ('Natural: qué lleva por dentro',
    'Estructura separada del muro para que este ventile, membrana impermeable, sistema modular o de fieltro que sostiene el sustrato, plantas seleccionadas por exposición, y riego por goteo con temporizador y, en instalaciones serias, recirculación y nutrición. Sin riego automático, un muro verde natural en este clima dura una temporada seca. Con él, es de los elementos que más carácter dan a un patio o a un lobby.'),
   ('Artificial: cuándo tiene sentido',
    'En interiores sin luz, en muros donde no hay forma de llevar agua, en zonas de rotación alta como una recepción o un local comercial, y cuando el cliente quiere el efecto sin el compromiso. El follaje sintético de calidad con protección UV aguanta bien en sombra; a sol directo pleno, todos pierden color con los años, unos más rápido que otros.'),
   ('Qué plantas funcionan en este clima',
    'Especies que toleran calor, humedad alta y salinidad si el proyecto está cerca del mar: helechos en las zonas sombreadas, filodendros y potos para volumen, bromelias y suculentas donde pega el sol, y plantas nativas que ya viven en la península. Copiar la paleta de un proyecto de clima templado es la forma más rápida de reponer el muro completo el primer año.'),
   ('Costos 2026',
    'Rangos por m² de muro instalado, incluyendo estructura, sistema y plantación o follaje. El riego automático y la iluminación se cotizan aparte cuando se piden.'),
   ('Mantenimiento honesto',
    'El natural pide revisión de riego, nutrición periódica, poda y reposición de plantas que no prosperan: en la práctica, visita mensual. El artificial pide lavado con agua y revisión de sujeciones. Si nadie va a encargarse del mantenimiento, el artificial no es una derrota: es la decisión correcta.'),
  ],
  table=('Tipo','Qué incluye','Costo 2026 por m²',
   [('Muro verde artificial','Estructura, follaje sintético con protección UV','$900 – $1,800 MXN'),
    ('Natural, sistema modular','Estructura, módulos, sustrato, plantas','$2,500 – $4,500 MXN'),
    ('Natural con riego y nutrición','Sistema completo automatizado','$3,500 – $6,000 MXN'),
    ('Mantenimiento mensual, natural','Riego, poda, reposición','$150 – $350 MXN/m²/mes')]),
  faq=[('¿Cuánto cuesta un muro verde?','De $900 a $1,800 MXN por m² el artificial y de $2,500 a $6,000 MXN por m² el natural según sistema, riego y nutrición.'),
       ('¿Cuánto dura un muro verde natural?','Años, si tiene riego automático y mantenimiento mensual. Sin riego, en la temporada seca de la Riviera Maya no llega a los seis meses.'),
       ('¿Daña el muro de la casa?','No, cuando se instala sobre estructura separada con membrana impermeable y cámara de ventilación. El daño aparece cuando el sistema se fija directo al aplanado y la humedad no tiene salida.'),
       ('¿Sirve en interiores?','El natural sí, con luz suficiente o iluminación de apoyo y con drenaje previsto. Cuando no hay ninguna de las dos, el artificial es la opción sensata.')],
  links=[('/roof-garden/','Roof garden'), ('/riego-automatico/','Riego automático'), ('/iluminacion-arquitectonica/','Iluminación arquitectónica'), L_REM]),

'barda-perimetral': dict(
  title='Barda Perimetral: Costo por Metro Lineal 2026 | Recrea',
  desc='Barda perimetral en la Riviera Maya: costo por metro lineal en 2026, block o concreto, cimentación en roca, altura permitida y errores que la agrietan.',
  h1='Barda Perimetral: Costo por Metro Lineal',
  lead='La barda parece la parte simple de la obra y es donde más se improvisa: sin cimentación adecuada ni castillos a distancia correcta, se agrieta en la primera temporada.',
  secs=[
   ('Cómo se construye una barda que no se agrieta',
    'Cimentación corrida o zapata aislada según el terreno, castillos a distancia calculada —no cada que se acuerdan—, dala de cerramiento arriba, refuerzo en esquinas y cambios de nivel, y juntas constructivas en tramos largos. En roca caliza el desplante suele ser más fácil que en relleno; en relleno mal compactado, la barda se mueve y ninguna reparación cosmética lo arregla.'),
   ('Materiales y acabados',
    'Block hueco de concreto es el estándar por costo y velocidad. Block de concreto aparente cuando se busca un acabado limpio sin aplanar. Muro de piedra o chapa de piedra donde importa la imagen. Y concreto armado en tramos que también contienen tierra, que ya no es barda sino muro de contención y se calcula distinto. Encima: aplanado y pintura, o acabado en chukum donde se quiere la estética regional.'),
   ('Altura, reglamento y vecinos',
    'La altura máxima la fija el municipio y, dentro de un fraccionamiento, el reglamento interno, que suele ser más estricto y a veces prohíbe bardas macizas en el frente. En colindancia conviene acordar por escrito con el vecino quién construye, dónde queda el eje y quién paga: es la fuente número uno de conflictos que terminan deteniendo una obra.'),
   ('Costos 2026',
    'Rangos por metro lineal de barda terminada, altura estándar de 2.40 m, con cimentación, castillos, dala y acabado.'),
   ('Cuándo la barda deja de ser barda',
    'En cuanto retiene tierra de un lado, cambia de categoría: el empuje horizontal de tierra saturada es de otro orden y exige cálculo, drenaje y armado propios. Muchos muros agrietados de la región son bardas que terminaron conteniendo un relleno para el que nunca fueron diseñadas.'),
  ],
  table=('Tipo de barda','Acabado','Costo 2026 por metro lineal',
   [('Block, aplanada y pintada','2.40 m de altura','$1,400 – $2,400 MXN'),
    ('Block aparente','Sin aplanar, junta cuidada','$1,200 – $2,000 MXN'),
    ('Con chapa de piedra o chukum','Acabado de imagen','$2,600 – $4,500 MXN'),
    ('Barda baja con reja de herrería','Muro 0.80 m + reja','$2,500 – $4,800 MXN')]),
  faq=[('¿Cuánto cuesta una barda perimetral por metro?','De $1,200 a $2,400 MXN por metro lineal en block a 2.40 m de altura, y de $2,600 a $4,800 MXN con acabados de imagen o reja de herrería.'),
       ('¿Qué altura puede tener?','La que permita el municipio y, dentro de un fraccionamiento, su reglamento interno, que suele limitar más y a veces prohíbe bardas macizas al frente. Conviene confirmarlo antes de cotizar.'),
       ('¿Necesita cimentación?','Sí, siempre. La barda sin cimentación adecuada es la que se agrieta y se inclina, sobre todo cuando se construye sobre relleno reciente sin compactar.'),
       ('¿Puede sostener tierra en un desnivel?','No, no como barda. Si retiene tierra necesita diseño de muro de contención, con cálculo, armado y drenaje propios.')],
  links=[('/muro-de-contencion/','Muro de contención'), ('/porton-automatico/','Portón automático'), L_CARP, L_PRES]),

'porton-automatico': dict(
  title='Portón Automático: Precio, Tipos y Instalación | Recrea',
  desc='Portón automático en la Riviera Maya: precio en 2026 según tipo y tamaño, motor adecuado, respaldo ante apagones y qué falla primero con la salinidad.',
  h1='Portón Automático: Precio e Instalación',
  lead='El portón se compra dos veces: la primera por el precio, la segunda cuando el motor barato se rinde ante el peso, los apagones o la sal. Aquí lo que importa es la selección.',
  secs=[
   ('Corredizo, batiente o levadizo',
    'Corredizo: el más común cuando hay espacio lateral, tolera bien el peso y el uso frecuente. Batiente de dos hojas: elegante y adecuado en accesos amplios, exige espacio de barrido y buen herraje. Levadizo o basculante: para cocheras con poco fondo. La elección la marca el terreno y el flujo, no el catálogo: un portón mal elegido se nota todos los días.'),
   ('El motor: la pieza que decide la vida útil',
    'Se dimensiona por peso de la hoja y ciclos diarios previstos, con margen. Un motor al límite trabaja caliente y muere joven, sobre todo en un acceso con muchas entradas al día. En zona costera conviene además protección del tablero contra humedad y sal, y evitar herrajes galvanizados corrientes donde debería ir inoxidable.'),
   ('Apagones, seguridad y control',
    'En la región los cortes de energía son parte de la vida, así que el respaldo por batería o la liberación manual accesible no son un extra: son el detalle que evita quedarse encerrado. Sume fotocelda de seguridad —obligatoria si hay niños o mascotas—, tope de fuerza, luz intermitente, y control por remoto, teclado o aplicación según prefiera.'),
   ('Costos 2026',
    'Rangos de portón instalado, incluyendo hoja de herrería, motor, herraje y automatización básica. Los acabados especiales y la iluminación se cotizan aparte.'),
   ('Mantenimiento en clima costero',
    'Lubricación de guías y bisagras, revisión de fotoceldas y tope de fuerza, ajuste de tensión, y sobre todo lavado con agua dulce de herrajes cerca del mar. Es media hora dos veces al año contra un motor forzado que se reemplaza completo.'),
  ],
  table=('Tipo','Aplicación','Costo 2026 instalado',
   [('Corredizo, hasta 4 m','Acceso residencial estándar','$35,000 – $70,000 MXN'),
    ('Corredizo grande o de alto uso','Más de 4 m o acceso común','$70,000 – $130,000 MXN'),
    ('Batiente de dos hojas','Acceso amplio, imagen','$40,000 – $95,000 MXN'),
    ('Automatización sobre portón existente','Motor, herraje, seguridad','$18,000 – $45,000 MXN')]),
  faq=[('¿Cuánto cuesta un portón automático?','De $35,000 a $130,000 MXN instalado según tipo, tamaño y motor. Automatizar un portón que ya existe cuesta entre $18,000 y $45,000 MXN.'),
       ('¿Qué pasa si se va la luz?','Con respaldo de batería sigue operando un número de ciclos; sin respaldo, se abre con la liberación manual. En esta región conviene siempre uno de los dos, y de preferencia los dos.'),
       ('¿Se puede automatizar un portón que ya tengo?','Sí, si la hoja está en buen estado, corre sin fricción y el peso corresponde al motor. Si la estructura está vencida, automatizarla solo acelera su final.'),
       ('¿Qué mantenimiento necesita cerca del mar?','Lavado con agua dulce de guías y herrajes, lubricación y revisión de seguridad dos veces al año. La sal ataca primero el herraje y después el motor.')],
  links=[('/barda-perimetral/','Barda perimetral'), L_CARP, ('/instalacion-electrica-casa/','Instalación eléctrica'), L_REM]),

'escaleras-de-concreto': dict(
  title='Escaleras de Concreto: Tipos, Medidas y Costo 2026 | Recrea',
  desc='Escaleras de concreto: tipos, medidas correctas de huella y peralte, armado, acabados y costo en 2026 en la Riviera Maya. Recta, en L, caracol o volada.',
  h1='Escaleras de Concreto: Medidas, Tipos y Costo',
  lead='Una escalera mal proporcionada se siente incómoda toda la vida de la casa y no se corrige después. Las medidas correctas cuestan lo mismo que las incorrectas.',
  secs=[
   ('Las medidas que hacen cómoda una escalera',
    'La regla práctica: dos peraltes más una huella entre 60 y 64 cm. En vivienda funcionan bien peraltes de 17 a 18 cm con huellas de 28 a 30 cm. Ancho mínimo cómodo de 90 cm, mejor 1.00 m o más. Todos los escalones iguales —una diferencia de un centímetro en el último se siente como un tropiezo—, y descanso cuando se superan los diez o doce peraltes seguidos.'),
   ('Tipos y qué implica cada uno',
    'Recta: la más económica y la que menos espacio desperdicia si hay largo disponible. En L o en U con descanso: la solución habitual cuando el hueco es compacto. Caracol: ocupa poco y es incómoda para subir muebles, mejor como acceso secundario. Volada o en voladizo: espectacular, y la más exigente en cálculo y en ejecución, porque cada escalón trabaja empotrado.'),
   ('Armado, cimbra y colado',
    'La escalera es un elemento estructural: lleva armado calculado, no acero repartido a ojo. Importan el anclaje al muro o a la trabe, el recubrimiento del acero, la cimbra bien apuntalada y un colado continuo para evitar juntas frías en el arranque. Las escaleras que vibran o se fisuran suelen tener el problema en el arranque o en el descanso, no en la mitad del tramo.'),
   ('Costos 2026',
    'Rangos de escalera terminada en obra, sin acabado de piso ni barandal, para vivienda de un nivel a otro.'),
   ('Acabados y barandal',
    'Concreto pulido, chukum, porcelanato, madera o piedra. En exteriores conviene acabado no resbaloso: en temporada de lluvias una escalera pulida al aire libre es un accidente esperando. El barandal se cotiza aparte —herrería, cristal templado o cable tensado— y en casas con niños la separación entre elementos importa más que el diseño.'),
  ],
  table=('Tipo de escalera','Consideración','Costo 2026 de obra',
   [('Recta, un nivel','Lo más económico','$18,000 – $38,000 MXN'),
    ('En L o U con descanso','Hueco compacto','$28,000 – $55,000 MXN'),
    ('Caracol de concreto','Espacio reducido','$45,000 – $95,000 MXN'),
    ('Volada / en voladizo','Cálculo y ejecución exigentes','$70,000 – $160,000 MXN')]),
  faq=[('¿Cuánto cuesta una escalera de concreto?','De $18,000 a $55,000 MXN una escalera recta o en L de un nivel a otro, y de $45,000 a $160,000 MXN en caracol o volada. Acabado de piso y barandal van aparte.'),
       ('¿Cuál es la medida correcta de huella y peralte?','En vivienda, peralte de 17 a 18 cm y huella de 28 a 30 cm, verificando que dos peraltes más una huella queden entre 60 y 64 cm. Todos los escalones deben ser idénticos.'),
       ('¿Se puede hacer una escalera volada en cualquier casa?','No. Requiere que el muro o la trabe de apoyo estén diseñados para recibir el empotramiento, así que se define en el proyecto estructural, no cuando la obra ya va avanzada.'),
       ('¿Qué acabado conviene en exteriores?','Uno antiderrapante. Con la lluvia intensa de la región, una escalera exterior pulida se vuelve peligrosa; el acabado texturizado o la piedra rugosa resuelven el problema.')],
  links=[L_CIM, ('/microcemento/','Microcemento'), ('/cemento-pulido/','Cemento pulido'), L_PROY]),

'jacuzzi-exterior': dict(
  title='Jacuzzi Exterior: Precio, Obra o Prefabricado | Recrea',
  desc='Jacuzzi exterior en la Riviera Maya: precio en 2026, obra civil contra prefabricado, requisitos eléctricos e hidráulicos, base estructural y mantenimiento real.',
  h1='Jacuzzi Exterior: Precio y Qué Necesita para Instalarse',
  lead='El jacuzzi es la partida donde más se subestima la preparación: base estructural, alimentación eléctrica dedicada y desagüe. El equipo suele ser lo fácil.',
  secs=[
   ('Prefabricado o construido en obra',
    'Prefabricado: llega listo, se instala en días, es la opción sensata cuando ya hay terraza y se quiere resolver rápido. En obra: se integra al diseño, permite cualquier forma, acabado en chukum, piedra o azulejo y desbordante hacia la alberca, pero implica estructura, impermeabilización y equipo instalados en sitio, con plazos de semanas.'),
   ('Lo que hay que preparar antes',
    'Base capaz de soportar el peso lleno más los usuarios —un jacuzzi familiar lleno pesa varias toneladas, y una terraza cualquiera no está calculada para eso—; alimentación eléctrica dedicada con su protección; desagüe previsto para el vaciado, que no puede ir a la calle ni al terreno del vecino; y acceso de servicio al equipo. Resolverlo después de instalado siempre cuesta más.'),
   ('Costos 2026',
    'Rangos instalados en la Riviera Maya, incluyendo equipo y conexiones. La obra civil de terraza o refuerzo estructural se cotiza aparte cuando hace falta.'),
   ('Calentamiento en clima cálido',
    'Aquí el problema rara vez es calentar el agua: es que en verano el jacuzzi al sol se pone tibio y deja de ser un jacuzzi. Por eso la sombra, la ubicación y, en instalaciones de nivel, un sistema que también enfríe cambian más la experiencia que la potencia del calentador. En invierno, con noches frescas, la bomba de calor sí se agradece.'),
   ('Mantenimiento y consumo',
    'Control químico semanal, limpieza de filtros, revisión de bomba y calentador, y vaciado periódico. El consumo eléctrico depende sobre todo del calentador y de si el equipo trabaja con cubierta térmica; sin cubierta, en exterior, el gasto se dispara y el agua se ensucia mucho más rápido.'),
  ],
  table=('Opción','Alcance','Costo 2026 instalado',
   [('Jacuzzi prefabricado, 4–6 plazas','Equipo, conexión, puesta en marcha','$95,000 – $250,000 MXN'),
    ('Prefabricado premium con cubierta','Mayor equipamiento y aislamiento','$250,000 – $450,000 MXN'),
    ('Construido en obra','Estructura, acabado, equipo','$180,000 – $420,000 MXN'),
    ('Integrado a alberca con desbordante','Obra y equipo compartidos','Desde $350,000 MXN')]),
  faq=[('¿Cuánto cuesta un jacuzzi exterior?','De $95,000 a $250,000 MXN un prefabricado de 4 a 6 plazas instalado, y de $180,000 a $420,000 MXN uno construido en obra con acabado a elegir.'),
       ('¿Puedo poner un jacuzzi en mi terraza?','Solo si la losa está calculada para el peso lleno, que en un modelo familiar son varias toneladas. Es lo primero que revisamos, antes de hablar de modelos.'),
       ('¿Cuánto consume de electricidad?','Depende del calentador y del aislamiento. Con cubierta térmica el consumo es razonable; sin cubierta, en exterior, sube mucho y el agua se ensucia más rápido.'),
       ('¿Se puede integrar a la alberca?','Sí, compartiendo obra civil y parte del equipo, con desbordante hacia el vaso principal. Conviene decidirlo antes de construir la alberca, no después.')],
  links=[('/cuanto-cuesta-una-alberca/','Cuánto cuesta una alberca'), ('/albercas-de-lujo-playa-del-carmen/','Albercas de lujo'), ('/deck-de-madera/','Deck de madera'), ('/instalacion-electrica-casa/','Instalación eléctrica')]),

'instalacion-electrica-casa': dict(
  title='Instalación Eléctrica de una Casa: Costo y Norma | Recrea',
  desc='Instalación eléctrica de una casa en la Riviera Maya: costo por m² y por salida en 2026, calibres, tablero, tierra física y qué exige el clima costero.',
  h1='Instalación Eléctrica de una Casa: Costo y Criterios',
  lead='La instalación eléctrica se paga una vez y se sufre veinte años. Aquí, con aire acondicionado todo el año y tormentas eléctricas, el sobredimensionar sale barato.',
  secs=[
   ('Qué incluye una instalación completa',
    'Acometida y medidor; tablero principal con interruptores termomagnéticos y protección diferencial; tierra física; circuitos separados para iluminación, contactos, aire acondicionado, bomba, alberca y cocina; canalización, cableado, salidas, apagadores y placas; y pruebas antes de tapar. Todo eso se define en el proyecto eléctrico, no se improvisa en obra con lo que haya en la camioneta.'),
   ('Calibres y circuitos: donde se ahorra mal',
    'Cada circuito lleva el calibre que corresponde a su carga y a su distancia. El error clásico es alimentar aires acondicionados o una bomba desde circuitos de contactos, o repartir toda la planta alta en dos circuitos. Se nota cuando el interruptor bota en agosto con todos los equipos encendidos, y para entonces el cable ya está dentro del muro.'),
   ('Costos 2026',
    'Rangos para vivienda en la Riviera Maya, con material de marca reconocida y mano de obra. La acometida y el trámite ante CFE se cotizan según el caso.'),
   ('Tierra física, tormentas y salinidad',
    'La tierra física no es opcional: es lo que protege a las personas y a los equipos, y es la primera partida que desaparece de un presupuesto barato. En una región con tormentas eléctricas frecuentes conviene además protección contra sobretensiones para los equipos sensibles. Y cerca del mar, tableros y salidas de exterior con grado de protección adecuado, porque la sal entra donde el plástico barato ya no cierra.'),
   ('Lo que conviene prever desde el proyecto',
    'Circuito para bomba de alberca y para equipo de tratamiento de agua; preparación para paneles solares aunque se instalen después; alimentación para portón automático; puntos de carga de vehículo eléctrico; y cableado de red donde vaya a haber trabajo o cámaras. Todo eso vale una fracción si se deja preparado antes de tapar muros.'),
  ],
  table=('Alcance','Aplicación','Costo 2026',
   [('Instalación completa, obra nueva','Por m² construido','$450 – $900 MXN/m²'),
    ('Por salida (contacto, apagador, luminaria)','Obra o remodelación','$600 – $1,200 MXN'),
    ('Tablero principal con protecciones','Casa unifamiliar','$12,000 – $35,000 MXN'),
    ('Tierra física','Varilla, conductor, registro','$6,000 – $18,000 MXN')]),
  faq=[('¿Cuánto cuesta la instalación eléctrica de una casa?','De $450 a $900 MXN por m² construido en obra nueva, o de $600 a $1,200 MXN por salida en remodelación. El tablero y la tierra física se identifican por separado.'),
       ('¿Cuántos circuitos necesita una casa?','Los que resulten de las cargas reales: iluminación y contactos por zona, y circuitos independientes para cada aire acondicionado, bomba, alberca y cocina. Es lo que evita que el interruptor bote en el mes más caluroso.'),
       ('¿Es obligatoria la tierra física?','Es lo que protege a las personas y a los equipos, y forma parte de una instalación correcta. Es también la partida que desaparece primero en los presupuestos más baratos.'),
       ('¿Puedo dejar preparado para paneles solares?','Sí, y conviene: dejar canalización, espacio en tablero y ruta de conductores durante la obra cuesta una fracción de hacerlo después.')],
  links=[('/paneles-solares-riviera-maya/','Paneles solares'), ('/iluminacion-arquitectonica/','Iluminación arquitectónica'), ('/porton-automatico/','Portón automático'), L_OBRA]),

'iluminacion-arquitectonica': dict(
  title='Iluminación Arquitectónica: Diseño y Costo por m² | Recrea',
  desc='Iluminación arquitectónica en casas y hoteles de la Riviera Maya: capas de luz, temperatura de color, IP para exteriores, control y costo por m² en 2026.',
  h1='Iluminación Arquitectónica: Cómo se Diseña y Cuánto Cuesta',
  lead='La diferencia entre una casa bonita de día y una casa bonita de noche son unos cuantos miles de pesos bien colocados. Y casi nunca es cuestión de poner más luz.',
  secs=[
   ('Las capas de luz',
    'General: la que permite moverse, y la que suele estar sobredimensionada. De trabajo: la que enfoca donde se hace algo, en cocina, baño y escritorio. De acento: la que da carácter, sobre texturas, plantas, obra de arte o el propio muro. Y decorativa: la luminaria que se ve. Un proyecto que solo resuelve la general se siente plano; uno que trabaja las cuatro capas se siente diseñado, con menos vatios instalados.'),
   ('Temperatura de color y reproducción cromática',
    'En clima tropical la luz cálida —alrededor de 2700 a 3000 K— funciona mejor en interiores y en terrazas, y la neutra queda para cocina y áreas de trabajo. Mezclar temperaturas en un mismo espacio es el error más visible y el más común. Y para que la madera, el chukum y la piedra se vean como son, conviene una reproducción cromática alta; con luminarias baratas todo tira a gris.'),
   ('Exteriores: IP, sal y mantenimiento',
    'Una luminaria de exterior en la costa necesita grado de protección adecuado contra agua y polvo, cuerpo resistente a la corrosión y sellos que aguanten la humedad permanente. Aquí lo que mata las luminarias baratas no es la lluvia: es la sal que entra por las juntas y se come el disipador. Sumar drivers accesibles para mantenimiento evita romper piso o muro cuando falle uno.'),
   ('Costos 2026',
    'Rangos por m² de área intervenida, incluyendo luminarias de calidad media-alta, canalización, cableado y control básico. El proyecto de iluminación para casas de nivel se cotiza aparte.'),
   ('Control: de un apagador a escenas',
    'Un atenuador bien puesto cambia más la percepción de una sala que dos luminarias adicionales. A partir de ahí: escenas por espacio, control por aplicación, sensores en pasillos y baños, y automatización de fachada y jardín por horario. Conviene decidirlo antes de cablear, porque agregar control después implica volver a abrir.'),
  ],
  table=('Alcance','Qué incluye','Costo 2026',
   [('Iluminación interior residencial','Luminarias, canalización, instalación','$600 – $1,400 MXN/m²'),
    ('Iluminación de acento y arquitectónica','Capas, atenuación, luminaria especial','$1,200 – $2,500 MXN/m²'),
    ('Exteriores y jardín','Luminarias con protección adecuada','$900 – $2,000 MXN/m²'),
    ('Proyecto de iluminación','Cálculo, selección, planos','Por proyecto')]),
  faq=[('¿Cuánto cuesta la iluminación arquitectónica?','De $600 a $1,400 MXN por m² en interior residencial y de $1,200 a $2,500 MXN por m² cuando se trabajan capas de acento con atenuación y luminaria especial.'),
       ('¿Qué temperatura de color conviene?','Cálida, alrededor de 2700 a 3000 K, en interiores y terrazas; neutra en cocina y áreas de trabajo. Lo importante es no mezclar temperaturas en un mismo espacio.'),
       ('¿Qué luminarias aguantan cerca del mar?','Las que tienen grado de protección adecuado, cuerpo resistente a la corrosión y sellos de calidad. La sal entra por las juntas y destruye primero el disipador de las luminarias baratas.'),
       ('¿Se puede agregar control después?','Se puede, pero implica volver a abrir muros o techos. Dejar previsto el control durante la obra cuesta mucho menos que agregarlo con la casa terminada.')],
  links=[('/instalacion-electrica-casa/','Instalación eléctrica'), ('/muro-verde/','Muro verde'), ('/roof-garden/','Roof garden'), L_REM]),

'domo-de-policarbonato': dict(
  title='Domo de Policarbonato: Precio por m² y Tipos | Recrea',
  desc='Domo de policarbonato en la Riviera Maya: precio por m² en 2026, tipos de lámina, control solar, resistencia a granizo y viento, y cómo evitar filtraciones.',
  h1='Domo de Policarbonato: Precio por m² y Qué Considerar',
  lead='El domo resuelve luz natural donde no hay ventanas. Mal elegido, convierte un patio en un horno; mal instalado, gotea justo por los tornillos.',
  secs=[
   ('Tipos de lámina y para qué sirve cada uno',
    'Alveolar o celular: liviana, aislante, económica, la más usada en patios de servicio y cubiertas de paso. Compacta: transparente como el cristal y muy resistente al impacto, para donde importa la vista. Ondulada: económica para cubiertas grandes. El espesor y el número de paredes definen aislamiento y resistencia; en cubiertas amplias también definen la separación máxima entre apoyos.'),
   ('Calor: la decisión que más se equivoca',
    'Un domo transparente sobre un patio orientado al sol de mediodía crea un invernadero. En este clima conviene lámina con control solar u opalina, o bien sombra parcial, y siempre ventilación en la parte alta para que el aire caliente salga. Un domo bien resuelto ilumina sin calentar; uno mal resuelto obliga a poner aire acondicionado en un espacio que no lo necesitaba.'),
   ('Estructura, viento y granizo',
    'La estructura se calcula para viento de zona costera, con anclajes y tornillería adecuados, no solo para sostener el peso. El policarbonato de calidad resiste bien el impacto, pero el punto débil suele ser la fijación: tornillo sin arandela de neopreno, perforación al límite del borde o sin espacio para dilatación. La lámina se dilata con el calor, y si no tiene holgura, se deforma o rompe por el punto fijo.'),
   ('Costos 2026',
    'Rangos por m² de domo instalado, incluyendo estructura metálica, lámina, perfilería, sellos y tornillería.'),
   ('Filtraciones: siempre por las juntas',
    'Las filtraciones no vienen de la lámina: vienen de perfiles mal sellados, tornillos sin arandela, encuentro con el muro sin goterón y pendiente insuficiente. Con pendiente adecuada, perfil de unión correcto y sellado en el perímetro, un domo se mantiene seco años. Sin eso, el primer aguacero con viento lo demuestra.'),
  ],
  table=('Tipo de domo','Aplicación','Costo 2026 por m²',
   [('Alveolar 6 mm','Patios de servicio, cubiertas ligeras','$1,300 – $2,200 MXN'),
    ('Alveolar 10–16 mm','Mayor aislamiento y claros amplios','$1,900 – $3,200 MXN'),
    ('Compacto transparente','Donde importa la transparencia','$2,600 – $4,500 MXN'),
    ('Con control solar','Reduce ganancia de calor','Suma $300 – $800 MXN')]),
  faq=[('¿Cuánto cuesta un domo de policarbonato por m²?','De $1,300 a $3,200 MXN por m² instalado en lámina alveolar según espesor, y de $2,600 a $4,500 MXN en policarbonato compacto transparente.'),
       ('¿Calienta mucho un domo?','El transparente sí, sobre todo a mediodía. Con lámina de control solar u opalina y ventilación en la parte alta, el espacio se ilumina sin convertirse en invernadero.'),
       ('¿Resiste huracanes?','Depende sobre todo de la estructura y de la fijación, no de la lámina. Se calcula para viento de zona costera y se ancla en consecuencia; ese es el punto que falla en las instalaciones baratas.'),
       ('¿Por qué gotea un domo?','Casi siempre por las juntas: tornillos sin arandela de neopreno, perfil de unión mal colocado, falta de goterón contra el muro o pendiente insuficiente.')],
  links=[L_IMP, ('/pergola-de-madera/','Pérgola de madera'), ('/ventanas-de-aluminio/','Ventanas de aluminio'), L_CARP]),

'riego-automatico': dict(
  title='Riego Automático: Costo por m² y Diseño 2026 | Recrea',
  desc='Sistema de riego automático para jardín en la Riviera Maya: aspersión o goteo, sectorización, programador, costo por m² en 2026 y consumo real de agua.',
  h1='Riego Automático: Cómo se Diseña y Cuánto Cuesta',
  lead='En un clima con seis meses secos y seis de lluvia intensa, el riego automático no es lujo: es lo que evita replantar el jardín cada primavera.',
  secs=[
   ('Aspersión, goteo o los dos',
    'Aspersión para césped y superficies amplias. Goteo para arriates, setos, palmeras y macetas, donde entrega el agua a la raíz y desperdicia mucho menos. En la práctica un jardín bien resuelto usa ambos, en sectores separados, porque el césped y una palma no piden ni la misma cantidad ni la misma frecuencia.'),
   ('Sectorización: el corazón del sistema',
    'El sistema se divide en sectores por tipo de planta, exposición al sol y presión disponible. Cada sector riega su tiempo, en su horario. Regar todo el jardín a la vez es lo que produce zonas encharcadas junto a zonas secas, y es el error más común en instalaciones improvisadas. La presión y el caudal disponibles determinan cuántos aspersores pueden trabajar juntos: por eso se calcula antes de comprar.'),
   ('Costos 2026',
    'Rangos por m² de jardín, incluyendo tubería, emisores, válvulas, programador e instalación. La bomba y la cisterna, cuando hacen falta, se cotizan aparte.'),
   ('Agua: de dónde sale y cuánto cuesta',
    'De la red, de pozo cuando el predio lo permite, o de captación de lluvia, que en esta región cubre bien buena parte del riego si hay almacenamiento suficiente. Regar de madrugada reduce la evaporación de forma notable; regar a mediodía es tirar una parte del agua al aire y quemar hoja con las gotas. Un programador barato bien configurado ahorra más agua que un sistema caro mal programado.'),
   ('Mantenimiento',
    'Revisión de aspersores desalineados o tapados, limpieza de filtros en goteo, ajuste estacional de tiempos —no se riega igual en abril que en septiembre— y purga antes y después de la temporada de lluvias. Es una revisión cada pocos meses; sin ella el sistema sigue funcionando pero deja de regar donde se necesita.'),
  ],
  table=('Sistema','Aplicación','Costo 2026 por m² de jardín',
   [('Goteo en arriates y setos','Jardinería, palmeras, macetas','$180 – $350 MXN'),
    ('Aspersión para césped','Superficies amplias','$250 – $450 MXN'),
    ('Sistema mixto sectorizado','Jardín completo','$300 – $550 MXN'),
    ('Programador y automatización','Control por sectores y horarios','$6,000 – $25,000 MXN')]),
  faq=[('¿Cuánto cuesta un sistema de riego automático?','De $180 a $550 MXN por m² de jardín según sistema, más el programador. Un jardín residencial de 200 m² suele ubicarse entre $60,000 y $130,000 MXN instalado.'),
       ('¿Goteo o aspersión?','Goteo para arriates, setos y palmeras; aspersión para césped. Un jardín completo normalmente usa ambos, en sectores independientes.'),
       ('¿A qué hora conviene regar?','De madrugada. Se pierde mucha menos agua por evaporación y la hoja no se quema, cosa que sí ocurre regando al sol de mediodía.'),
       ('¿Se puede regar con agua de lluvia?','Sí, y es de los mejores usos para el agua captada. Con almacenamiento suficiente cubre buena parte del riego anual en esta región.')],
  links=[('/captacion-de-agua-de-lluvia/','Captación de agua de lluvia'), ('/roof-garden/','Roof garden'), ('/muro-verde/','Muro verde'), L_OBRA]),

'estudio-topografico': dict(
  title='Estudio Topográfico: Qué Incluye y Precio 2026 | Recrea',
  desc='Estudio topográfico de un terreno en la Riviera Maya: qué entrega, levantamiento y niveles, deslinde, precio en 2026 y por qué se hace antes de comprar.',
  h1='Estudio Topográfico: Qué Entrega y Cuánto Cuesta',
  lead='El plano topográfico es el primer documento honesto sobre un terreno: dice cuánto mide de verdad, cómo cae y qué hay dentro. Cuesta poco y evita compras caras.',
  secs=[
   ('Qué entrega el levantamiento',
    'Plano con las medidas reales del polígono y sus colindancias; curvas de nivel y desniveles; ubicación de construcciones, árboles significativos, pozos, cenotes y servicios existentes; referencias y coordenadas. Con eso el arquitecto proyecta sobre el terreno que existe y no sobre el que dice la escritura, que en la región no siempre coinciden.'),
   ('Por qué se hace antes de comprar',
    'Porque la superficie escriturada y la real difieren con más frecuencia de la que uno esperaría, porque las colindancias a veces están invadidas, y porque un desnivel que no se ve caminando puede significar cientos de metros cúbicos de relleno o un muro de contención completo. Todo eso cambia el precio que tiene sentido pagar por el terreno.'),
   ('Costos 2026',
    'Rangos en la Riviera Maya según superficie y dificultad de acceso. Un terreno con vegetación densa exige limpieza de brechas y sube el costo.'),
   ('Topografía y proyecto: cómo se conectan',
    'El levantamiento alimenta el proyecto arquitectónico —niveles de desplante, plataformas, accesos— y el diseño de drenaje pluvial, que en esta región importa más de lo que parece. También sirve para el trámite: varios municipios piden plano topográfico dentro del expediente de licencia, y uno hecho a la ligera se devuelve.'),
   ('Deslinde, mojoneras y vecinos',
    'Cuando hay duda sobre los límites, el deslinde con colocación de mojoneras deja constancia física de dónde termina su terreno. Es incómodo de plantear y mucho menos incómodo que descubrir, con la cimentación colada, que dos metros de barda están del lado del vecino.'),
  ],
  table=('Alcance','Aplica a','Costo 2026',
   [('Levantamiento, terreno urbano','Hasta 500 m²','$8,000 – $16,000 MXN'),
    ('Levantamiento con curvas de nivel','500 – 2,000 m²','$14,000 – $30,000 MXN'),
    ('Terreno grande o con vegetación densa','Más de 2,000 m²','Según superficie y acceso'),
    ('Deslinde con mojoneras','Definición física de límites','$10,000 – $35,000 MXN')]),
  faq=[('¿Cuánto cuesta un estudio topográfico?','De $8,000 a $16,000 MXN para un terreno urbano de hasta 500 m², y de $14,000 a $30,000 MXN cuando se levantan curvas de nivel en predios de mayor superficie.'),
       ('¿Cuánto tarda?','Entre 2 y 7 días entre campo y entrega del plano, según superficie, vegetación y acceso.'),
       ('¿Sirve el plano de la escritura?','Como referencia legal sí, como base de proyecto no siempre: la superficie real y las colindancias difieren con frecuencia de lo escriturado, y el proyecto se dibuja sobre el terreno que existe.'),
       ('¿Es necesario para el permiso de construcción?','Varios municipios lo piden dentro del expediente, y en cualquier caso el proyecto ejecutivo lo necesita para definir niveles, plataformas y drenaje.')],
  links=[L_TOPO, ('/mecanica-de-suelos/','Mecánica de suelos'), ('/uso-de-suelo/','Uso de suelo'), L_PROY]),

'casas-de-madera': dict(
  title='Casas de Madera en Clima Tropical: Cuándo Sí | Recrea',
  desc='Casas de madera en la Riviera Maya: por qué la termita y el 80% de humedad complican la madera estructural, qué sistemas sí funcionan y qué cuesta cada opción.',
  h1='Casas de Madera en Clima Tropical: Cuándo Funciona y Cuándo No',
  lead='Vamos a decirlo antes del precio: en la Riviera Maya, una casa de madera estructural rara vez es la decisión correcta. Aquí están las razones y las alternativas que sí aguantan.',
  secs=[
   ('Los tres enemigos: termita, humedad y huracán',
    'La termita subterránea es endémica en la península y ataca la madera en contacto con el suelo o con humedad. La humedad relativa alta durante casi todo el año mantiene la madera trabajando, dilatando y contrayendo, y favorece hongos. Y la temporada de huracanes exige anclajes y arriostramiento que una construcción de madera ligera debe resolver con mucho más cuidado que una de concreto. Ninguno es insalvable; todos cuestan dinero y mantenimiento permanente.'),
   ('Dónde la madera sí es la respuesta',
    'En cubiertas y palapas con maderas duras locales —chicozapote, tzalam, chechén—, que llevan siglos funcionando aquí. En pérgolas, decks, celosías y carpintería exterior con la especie y el herraje correctos. En interiores, sin restricción. Y en estructuras elevadas sobre plataforma de concreto, con la madera lejos del suelo, ventilada y tratada. La madera no es el problema: el problema es la madera mal ubicada.'),
   ('Qué cuesta cada opción',
    'Rangos por m² construido en la Riviera Maya. Las opciones de madera incluyen tratamiento y herrajes adecuados al clima; sin ellos el precio baja y la vida útil también.'),
   ('Si aun así quiere una casa de madera',
    'Entonces hágala bien: plataforma de concreto que separe toda la madera del suelo, especies duras o madera tratada en autoclave con penetración real, herrajes inoxidables, aleros generosos para proteger los paramentos de la lluvia, ventilación cruzada bajo el piso y en cubierta, barrera antitermita en el perímetro y un programa de mantenimiento anual que nadie se salte. Con eso, funciona. Sin eso, dura pocos años.'),
   ('Lo que solemos recomendar',
    'Estructura de concreto o mampostería para lo que sostiene la casa, y madera para lo que se ve y se toca: cubiertas, pérgolas, celosías, decks, carpintería. Se obtiene el carácter que la gente busca en la madera sin apostar la estructura de la casa contra la termita. Es la combinación que construimos aquí todos los días.'),
  ],
  table=('Sistema','Consideración en este clima','Costo 2026 por m²',
   [('Concreto y mampostería','Estándar regional, mínimo mantenimiento','$17,000 – $30,000 MXN'),
    ('Estructura mixta con madera vista','Carácter sin apostar la estructura','$20,000 – $35,000 MXN'),
    ('Madera estructural bien resuelta','Plataforma, especies duras, mantenimiento','$18,000 – $32,000 MXN'),
    ('Palapa o cubierta de madera dura','Tradición regional, muy durable','$4,000 – $9,000 MXN')]),
  faq=[('¿Se puede construir una casa de madera en la Riviera Maya?','Se puede, con plataforma de concreto que separe la madera del suelo, especies duras o tratamiento en autoclave, herrajes inoxidables, aleros amplios, ventilación y mantenimiento anual. Sin todo eso, la termita y la humedad la castigan rápido.'),
       ('¿Sale más barata que una de concreto?','No necesariamente. Bien resuelta para este clima, con maderas adecuadas y herrajes inoxidables, se ubica en el mismo rango que una casa de concreto, y exige mantenimiento que la de concreto no pide.'),
       ('¿Qué maderas aguantan aquí?','Chicozapote, tzalam y chechén son las de mejor comportamiento a la intemperie en la región. El pino sin tratar es la peor elección posible en exterior.'),
       ('¿Y una palapa?','Es otra historia: la palapa de madera dura con cubierta de huano es tradición regional y funciona muy bien, con su propio mantenimiento. Ahí la madera está en su terreno.')],
  links=[('/pergola-de-madera/','Pérgola de madera'), ('/deck-de-madera/','Deck de madera'), ('/blog-es/guia-construccion-palapas.html','Construcción de palapas'), L_OBRA]),
}

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src = open(kw1.TPL, encoding='utf-8').read()
    texts = {}
    for slug, d in PAGES.items():
        os.makedirs(slug, exist_ok=True)
        html = kw1.build(slug, d, src)
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
        texts[slug] = set(tuple(body[i:i + 6]) for i in range(len(body) - 5))
        flag = '' if len(d['title']) <= 65 and len(d['desc']) <= 165 else '  <-- CHECK'
        print('%-28s T%2d D%3d words %4d%s' % (slug + '/', len(d['title']), len(d['desc']), len(body), flag))
    ks = list(texts)
    mx = max((len(texts[a] & texts[b]) / len(texts[a] | texts[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity: %.2f (%s vs %s)' % mx)
