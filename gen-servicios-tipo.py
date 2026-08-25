#!/usr/bin/env python3
"""The five type pages that carry the national head terms for the service clusters.

gen-servicios-ciudades.py builds the city layer and links up to these; without them
those links are broken and the head terms have nowhere to land. Volume (Semrush, MX):

    /puertas-de-madera/       puertas de madera          27100
    /cocinas-de-madera/       cocinas de madera           5400 · cocina integral de madera 2400
    /closets-a-medida/        closets de madera           2400 · closets a medida          210
    /remodelacion-de-banos/   remodelacion de banos       1300
    /albercas-infinity/       alberca infinity             720

These are the pages where the volume actually is: the city pages exist to catch
"carpinteria cancun" (320) and "cocinas integrales cancun" (210), but the national
terms are ten to a hundred times bigger. Each type page is the hub of its cluster and
links down to all nine cities.

Prices stay anchored to the same figures the city pages publish.
"""
import os, re, importlib.util

spec = importlib.util.spec_from_file_location(
    'svc', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen-servicios-ciudades.py'))
svc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(svc)
kw1 = svc.kw1
CITIES = svc.CITIES


def city_links(slug_tpl, label):
    return [('/' + slug_tpl % s + '/', '%s en %s' % (label, c['name'])) for s, c in CITIES.items()]


PAGES = {

'remodelacion-de-banos': dict(
 title='Remodelación de Baños: Precios 2026 y Proceso | Recrea',
 desc=('Remodelación de baños en la Riviera Maya: precios 2026 por nivel, '
       'impermeabilización, plomería y plazos reales. Presupuesto cerrado por partidas.'),
 h1='Remodelación de Baños: Precios 2026 y Cómo se Hace',
 lead=('Qué cuesta remodelar un baño en la Riviera Maya, qué incluye cada nivel de obra '
       'y cuáles son las tres partidas donde se decide si el baño dura o da problemas.'),
 head=('Nivel de remodelación', 'Qué incluye', 'Costo 2026'),
 rows=[('Solo cambio de acabados', 'Azulejo, grifería y muebles sin tocar instalación', '$22,000 – $55,000 MXN'),
       ('Medio baño / visitas', 'Renovación completa de superficie e instalación', '$28,000 – $60,000 MXN'),
       ('Baño básico (3–5 m²)', 'Azulejo, muebles de línea, grifería estándar', '$45,000 – $90,000 MXN'),
       ('Baño medio (4–6 m²)', 'Mueble a medida, cubierta, regadera de cristal', '$90,000 – $180,000 MXN'),
       ('Baño principal (6–10 m²)', 'Doble lavabo, nicho, cancel a medida, iluminación', '$180,000 – $320,000 MXN'),
       ('Baño premium / master', 'Chukum o piedra natural, tina exenta, domótica', '$320,000 – $650,000 MXN')],
 secs=[
  ('Cuánto cuesta remodelar un baño',
   'La horquilla es amplia porque "remodelar un baño" describe cuatro trabajos distintos. Cambiar solo acabados sobre '
   'una instalación sana arranca en $22,000 MXN. Un baño completo de tamaño normal, abriendo hasta la tubería y '
   'rehaciendo impermeabilización, se mueve entre $45,000 y $180,000 según nivel de material. Un baño principal grande '
   'con mueble a medida y cancelería de cristal entra en $180,000–$320,000. Y a partir de ahí está el terreno del baño '
   'premium, donde la piedra natural, la tina exenta y la domótica pueden llevar la partida por encima de $650,000. '
   'Estos rangos son de la Riviera Maya en 2026 e incluyen material, mano de obra e instalación.'),
  ('Las tres partidas que deciden el resultado',
   'La primera es la impermeabilización de la zona húmeda: membrana continua bajo el azulejo, subida al menos 20 cm en '
   'muro y sellada en el encuentro piso-muro y en la penetración del desagüe. Es lo que no se ve y lo primero que '
   'recorta un presupuesto barato; en losa de entrepiso, una regadera mal impermeabilizada aparece como mancha en el '
   'plafón de abajo entre seis meses y dos años después. La segunda es la instalación oculta: en obra de más de diez '
   'años lo normal es encontrar tubería picada, y renovar el acabado sin tocarla significa romper lo nuevo cuando '
   'llegue la fuga. La tercera es la ventilación: un baño interior sin extractor en clima húmedo tiene moho en la '
   'junta antes de dos temporadas.'),
  ('Qué mueve el presupuesto hacia arriba',
   'Cuatro decisiones explican casi toda la diferencia entre un baño medio y uno premium. Mover el desagüe de sitio, '
   'que obliga a tocar losa o a levantar el nivel de piso. Pasar de regadera a tina exenta, que suma peso, '
   'alimentación y desagüe nuevos. Cambiar a piedra natural, por el material y por el corte y el sellado. Y la '
   'cancelería de cristal templado a medida, que en un baño fuera de escuadra vale bastante más que un cancel de '
   'línea. Ninguna de las cuatro es un capricho; simplemente conviene decidirlas antes de comparar cotizaciones, '
   'porque son las que hacen que dos presupuestos del mismo baño no se parezcan.'),
  ('Materiales que aguantan en la costa',
   'Funcionan el porcelánico rectificado, la piedra natural sellada y el chukum en zona seca o en muro de regadera '
   'bien tratado. No funcionan el tablaroca estándar en zona húmeda, que hay que sustituir por tablacemento, ni el '
   'herraje de acero común, que se oxida a la vista en meses de humedad salina. La grifería conviene de cartucho '
   'cerámico: el agua de esta costa es dura e incrusta los aireadores baratos en una temporada. Y el chukum, que es lo '
   'que más se pide por estética, se resella cada cuatro a seis años y nunca va como piso de plato de ducha sin '
   'tratamiento antiderrapante.'),
  ('Plazos y permisos',
   'Un baño completo se entrega en tres a cinco semanas; un medio baño, en una a dos. El tramo que no se acelera es el '
   'curado del firme y la impermeabilización antes de azulejar. Para remodelación interior que no toca estructura ni '
   'fachada normalmente no hace falta licencia municipal, pero en condominio casi siempre se necesita el visto bueno '
   'de la administración, que fija horarios, ruta de escombro y afectación a vecinos. Ese trámite es el que marca el '
   'arranque real de la obra, y conviene resolverlo antes de comprar material.')],
 faq=[
  ('¿Cuánto cuesta remodelar un baño en 2026?',
   'De $22,000 MXN si solo se cambian acabados sobre instalación sana, a $45,000–$180,000 MXN un baño completo de '
   'tamaño normal, y $180,000–$320,000 un baño principal grande. El baño premium con piedra natural y tina exenta '
   'puede superar $650,000 MXN.'),
  ('¿Se puede remodelar un baño sin romper el piso?',
   'Sí, si la instalación está sana y no se mueve el desagüe: se cambian azulejo de muro, muebles y grifería sobre lo '
   'existente. Es el alcance más barato y el más rápido. Deja de tener sentido en cuanto hay humedad de fondo, porque '
   'la humedad no se resuelve por encima.'),
  ('¿Cuánto tarda la obra?',
   'Tres a cinco semanas un baño completo y una a dos un medio baño. Si es el único baño de la casa se trabaja por '
   'etapas para dejarlo utilizable, lo que suma entre cinco y diez días.'),
  ('¿Necesito permiso para remodelar un baño?',
   'Municipal, normalmente no, mientras no se toque estructura ni fachada. En condominio sí hace falta el visto bueno '
   'de la administración por horarios, escombro y afectación a vecinos.'),
  ('¿Qué garantía debería exigir?',
   'Garantía por escrito sobre impermeabilización e instalación hidrosanitaria, que es donde aparecen los problemas '
   'reales. Muebles y grifería van con la garantía de su fabricante. Exija también la prueba de escurrimiento hecha '
   'antes de la entrega.')],
 links=lambda: city_links('remodelacion-banos-%s', 'Remodelación de baños') +
               [('/remodelacion-riviera-maya/', 'Remodelación en la Riviera Maya'),
                ('/cocinas-de-madera/', 'Cocinas de madera')]),

'cocinas-de-madera': dict(
 title='Cocinas de Madera a Medida: Precios 2026 | Recrea',
 desc=('Cocinas de madera a medida en la Riviera Maya: tzalam, parota y chapa fina. '
       'Precios 2026 por metro lineal, qué madera aguanta y qué cubierta elegir.'),
 h1='Cocinas de Madera a Medida',
 lead=('Cocina integral de madera fabricada en taller propio: qué maderas aguantan la '
       'humedad de la costa, dónde conviene madera sólida y dónde no, y qué cuesta el metro lineal.'),
 head=('Tipo de cocina', 'Materiales', 'Costo 2026 por metro lineal'),
 rows=[('Melamina de línea', 'Melamina 16 mm, herraje estándar', '$3,000 – $5,500 MXN'),
       ('Melamina premium / MDF lacado', 'Canto ABS, herraje con cierre suave', '$5,500 – $9,000 MXN'),
       ('Chapa fina sobre MDF', 'Aspecto de madera con estabilidad de tablero', '$7,000 – $12,000 MXN'),
       ('Madera sólida (tzalam, parota)', 'Frentes y estructura en madera dura local', '$9,000 – $16,000 MXN'),
       ('Cubierta de cuarzo o granito', 'Suministro e instalación, por metro lineal', '$4,500 – $12,000 MXN'),
       ('Isla o península', 'Estructura, cubierta y conexiones, por pieza', '$45,000 – $160,000 MXN')],
 secs=[
  ('Madera sólida, chapa o melamina: qué conviene de verdad',
   'La cocina enteramente de madera sólida es la más cara y no siempre la mejor decisión en esta costa. La madera '
   'trabaja con la humedad ambiente: se mueve, y en un frente grande ese movimiento se ve. La solución que mejor '
   'resultado da es mixta — estructura en tablero estable y frentes en madera sólida o en chapa fina sobre MDF —, que '
   'conserva el aspecto y elimina el problema de estabilidad. La melamina premium con canto ABS es la opción sensata '
   'cuando el presupuesto manda y la casa está cerca del mar, porque no le afecta la humedad como a la madera.'),
  ('Tzalam, parota y las maderas que aguantan aquí',
   'El tzalam es la madera dura local de referencia: estable, resistente al insecto, de veta oscura. La parota tiene '
   'veta ancha y es la que se pide para barras e islas de aspecto rústico. La caoba funciona en interior fino. Lo que '
   'no funciona es el pino sin tratar en zona húmeda ni el aglomerado corriente en el mueble bajo de la tarja, que '
   'hincha por el canto en cuanto entra agua y ya no vuelve a su sitio. Toda madera lleva tratamiento contra termita, '
   'que aquí es subterránea y ataca por el contacto con piso o muro húmedo.'),
  ('Dónde poner la madera y dónde no',
   'La madera va bien en frentes de alacena, isla, barra y cabecera de cocina. Va mal como cubierta de trabajo húmeda '
   'y va mal en el mueble bajo de la tarja si no es tablero hidrófugo. La regla práctica: madera donde se ve, tablero '
   'estable donde se moja. En cubierta, el cuarzo es el estándar sensato porque no es poroso y no necesita sellado; el '
   'granito aguanta más calor pero hay que sellarlo; el concreto pulido da el aspecto que mucha gente busca y es el '
   'que más mantenimiento pide.'),
  ('Herrajes: la partida que decide los cinco años',
   'Entre una cocina de $5,500 y una de $9,000 el metro lineal la diferencia rara vez está en el diseño. Está en el '
   'espesor del tablero, el canto y el herraje: canto ABS pegado en lugar de canto de papel que se despega en un año, '
   'bisagra con cierre suave y corredera de extracción total sobre balín en lugar de corredera de rodillo. En casa a '
   'menos de un kilómetro del mar, además, herraje inoxidable: una bisagra común se traba en dos temporadas por el '
   'salitre. Son las partidas que un presupuesto barato recorta primero y las que se notan al quinto año.'),
  ('Plazos y por qué se mide sobre muro terminado',
   'De cuatro a ocho semanas entre levantamiento e instalación; la madera sólida y la cubierta de cuarzo con corte '
   'especial son los tramos largos. La medida se toma en sitio y sobre muro terminado, nunca sobre plano: un muro '
   'fuera de escuadra de dos centímetros arruina una cocina de catálogo, y absorber esa tolerancia dentro del mueble '
   'es justamente la diferencia entre una cocina a medida y una modular armada en sitio.')],
 faq=[
  ('¿Cuánto cuesta una cocina de madera?',
   'De $9,000 a $16,000 MXN por metro lineal en madera sólida tipo tzalam o parota, y de $7,000 a $12,000 en chapa '
   'fina sobre MDF, sin cubierta. La cubierta de cuarzo o granito suma $4,500 a $12,000 por metro lineal.'),
  ('¿La madera aguanta la humedad de la costa?',
   'La madera dura local tratada, sí, en frentes y zonas secas. Lo que no aguanta es la madera como cubierta de '
   'trabajo húmeda o como mueble bajo de tarja sin tablero hidrófugo. Por eso la mejor cocina de madera aquí es mixta: '
   'madera donde se ve, tablero estable donde se moja.'),
  ('¿Qué es mejor, madera sólida o chapa?',
   'Para la mayoría de las cocinas, chapa fina sobre MDF: mismo aspecto, mucha más estabilidad frente a la humedad y '
   'menor costo. La madera sólida tiene sentido en isla, barra y piezas donde el canto y el espesor se ven.'),
  ('¿Cuánto tarda una cocina a medida?',
   'De cuatro a ocho semanas desde el levantamiento, según material y carga de taller. La instalación en sitio toma de '
   'dos a cuatro días.'),
  ('¿Incluyen electrodomésticos?',
   'No. El precio es del mueble, la cubierta, los herrajes y la instalación, con los huecos y las conexiones previstos '
   'para los electrodomésticos que el cliente elija.')],
 links=lambda: city_links('cocinas-integrales-%s', 'Cocinas integrales') +
               [('/closets-a-medida/', 'Clósets a medida'), ('/puertas-de-madera/', 'Puertas de madera')]),

'closets-a-medida': dict(
 title='Clósets a Medida y de Madera: Precios 2026 | Recrea',
 desc=('Clósets a medida en la Riviera Maya: melamina, MDF lacado y madera. Precios '
       '2026 por metro lineal, herrajes que duran y qué sube el costo.'),
 h1='Clósets a Medida y Vestidores',
 lead=('Clósets y vestidores fabricados en taller propio sobre medida real del muro: '
       'qué cambia el precio por metro lineal y qué herrajes aguantan en la costa.'),
 head=('Tipo de clóset', 'Materiales', 'Costo 2026 por metro lineal'),
 rows=[('Clóset básico', 'Melamina 16 mm, canto ABS, entrepaños y tubo', '$2,500 – $3,800 MXN'),
       ('Clóset con cajonera', 'Corredera de extracción total, puertas abatibles', '$3,800 – $5,000 MXN'),
       ('Clóset con puertas corredizas', 'Riel superior, puertas de piso a techo', '$4,200 – $7,000 MXN'),
       ('Vestidor premium', 'MDF lacado o chapa, cierre suave, iluminación', '$5,000 – $11,000 MXN'),
       ('Clóset en madera sólida', 'Frentes en tzalam o parota', '$8,000 – $15,000 MXN'),
       ('Mueble complementario (zapatera, isla)', 'Según diseño, por pieza', '$8,000 – $45,000 MXN')],
 secs=[
  ('Qué cambia el precio por metro lineal',
   'Tres cosas, y ninguna es el diseño: fondo del mueble, número de cajones y tipo de puerta. Un clóset con puertas '
   'corredizas de piso a techo, cajonera interior con corredera de extracción total e iluminación cuesta el doble por '
   'metro lineal que el mismo clóset con puertas abatibles y entrepaños. Por eso dos cotizaciones del mismo espacio '
   'pueden diferir en un 100% sin que ninguna esté inflada. Conviene decidir cuántos cajones se quieren antes de pedir '
   'precios, porque es el concepto que más se esconde entre una cotización y otra.'),
  ('Herrajes y cantos: donde está la diferencia a cinco años',
   'El canto ABS pegado a máquina no se despega; el canto de papel se levanta en el primer año y desde ahí entra la '
   'humedad al tablero. La bisagra con cierre suave y la corredera de extracción total sobre balín son la diferencia '
   'entre un cajón que sigue corriendo bien a los cinco años y uno que se atora al segundo. En casa cercana al mar, '
   'todo el herraje va inoxidable, porque el salitre traba una bisagra común en dos temporadas. Estas tres partidas '
   'son las que decide un presupuesto barato recortar, y las únicas que el cliente nota con el uso.'),
  ('Melamina, MDF lacado o madera',
   'La melamina de 16 mm con canto ABS es la opción correcta para la mayoría de los clósets: estable frente a la '
   'humedad, económica y con acabados que hoy imitan bien la madera. El MDF lacado da frente liso y color a medida, y '
   'es lo que se usa en vestidor premium. La madera sólida en clóset tiene sentido en frentes vistos y en piezas de '
   'diseño; en interior de mueble no aporta nada y encarece mucho. En clóset dentro de zona húmeda o muro con historial '
   'de humedad, siempre tablero hidrófugo y mueble sobre zócalo ventilado, nunca apoyado directo en el piso.'),
  ('Medida real, no medida de plano',
   'El clóset se mide en sitio y sobre muro terminado. Los muros de esta región rara vez están a escuadra perfecta, y '
   'un desplome de dos centímetros en tres metros de largo se come cualquier mueble modular. El mueble a medida '
   'absorbe esa tolerancia en el despiece y se nivela sobre patas regulables; el modular la deja a la vista como una '
   'junta que se abre hacia arriba. Es la razón principal por la que un clóset a medida se ve distinto instalado, más '
   'allá del material.'),
  ('Plazos y coordinación con la obra',
   'De tres a seis semanas entre levantamiento y montaje. La carpintería es de los últimos oficios en entrar, después '
   'de piso y pintura, y por eso es la que más sufre cuando la obra viene retrasada. Si el clóset lleva iluminación '
   'interior, la salida eléctrica se deja prevista antes de cerrar muros: resolverla al final significa canaleta '
   'vista o romper acabado nuevo.')],
 faq=[
  ('¿Cuánto cuesta un clóset a medida?',
   'De $2,500 a $3,800 MXN por metro lineal en melamina básica con entrepaños y tubo, de $3,800 a $5,000 con cajonera, '
   'y de $5,000 a $11,000 en vestidor premium con cierre suave e iluminación.'),
  ('¿Conviene clóset de madera o de melamina?',
   'Para el interior del mueble, melamina o MDF: son más estables frente a la humedad de la costa y bastante más '
   'baratos. La madera sólida tiene sentido en los frentes vistos y en piezas de diseño.'),
  ('¿Puertas abatibles o corredizas?',
   'Corredizas cuando no hay espacio libre delante del clóset o el mueble es muy largo; abatibles cuando sí lo hay, '
   'porque dan acceso a todo el frente de una vez y cuestan menos. Las corredizas de piso a techo suben el precio por '
   'el riel y por el peso de la hoja.'),
  ('¿Cuánto tarda la fabricación?',
   'De tres a seis semanas desde el levantamiento en sitio, según material y carga de taller. El montaje toma de uno a '
   'tres días.'),
  ('¿Trabajan sobre proyecto de mi diseñador?',
   'Sí, con el despiece revisado en taller y con aviso por escrito de cualquier punto que en obra no vaya a funcionar '
   'antes de cortar: casi siempre tolerancia de muro o fondo de mueble.')],
 links=lambda: city_links('carpinteria-%s', 'Carpintería a medida') +
               [('/cocinas-de-madera/', 'Cocinas de madera'), ('/puertas-de-madera/', 'Puertas de madera')]),

'puertas-de-madera': dict(
 title='Puertas de Madera a Medida: Precios 2026 | Recrea',
 desc=('Puertas de madera a medida en la Riviera Maya: tambor, sólida, tzalam y parota. '
       'Precios 2026 por hoja, qué aguanta en exterior y qué mantenimiento pide.'),
 h1='Puertas de Madera a Medida',
 lead=('Puertas interiores y de entrada fabricadas en taller propio: qué tipo conviene '
       'en cada sitio de la casa, qué maderas aguantan el exterior y qué cuesta cada hoja.'),
 head=('Tipo de puerta', 'Construcción', 'Costo 2026 por hoja'),
 rows=[('Puerta interior de tambor', 'Bastidor con chapa, marco y herraje', '$4,500 – $9,000 MXN'),
       ('Puerta interior de MDF lacado', 'Tablero lacado a color, marco y herraje', '$6,500 – $13,000 MXN'),
       ('Puerta sólida de madera dura', 'Tzalam, parota o caoba, por hoja', '$12,000 – $45,000 MXN'),
       ('Puerta de entrada principal', 'Madera dura, herraje reforzado, alero recomendado', '$25,000 – $85,000 MXN'),
       ('Puerta de doble altura o doble hoja', 'Estructura reforzada, por conjunto', '$45,000 – $150,000 MXN'),
       ('Puerta corrediza tipo granero', 'Riel visto, hoja en madera o tablero', '$9,000 – $30,000 MXN')],
 secs=[
  ('Tambor, MDF o madera sólida: qué va en cada sitio',
   'La puerta interior de tambor — bastidor de madera con chapa en las dos caras — resuelve la mayoría de la casa a '
   'costo razonable y se comporta bien en interior climatizado. El MDF lacado da frente liso y color a medida, y es la '
   'opción de diseño en interior. La madera sólida tiene sentido en puerta de entrada, en puertas de doble altura y '
   'donde se busca aislamiento acústico real: una puerta de tambor no aísla ruido, por más gruesa que parezca. Poner '
   'madera sólida en todas las puertas interiores de una casa es una de las formas más caras de no notar la '
   'diferencia.'),
  ('Exterior: el alero no es opcional',
   'Una puerta de madera en exterior necesita protección. Sol directo más lluvia sobre una hoja sin resguardo abre la '
   'veta y levanta el acabado por bueno que sea, y ninguna garantía cubre eso. Con alero o volado que la proteja, la '
   'misma puerta dura años con resellado cada dos o tres. Si el diseño no admite alero, la decisión honesta es ir a '
   'otro material en esa posición y dejar la madera donde sí se puede mantener. Lo decimos antes de fabricar, porque '
   'es el reclamo más frecuente del oficio.'),
  ('Maderas y tratamiento contra termita',
   'El tzalam y la parota son las maderas duras locales que mejor se comportan: estables, resistentes al insecto y con '
   'veta que aguanta el sol filtrado. La caoba funciona en interior fino. Toda madera lleva tratamiento contra '
   'termita, que en esta región es subterránea y ataca por el contacto con piso o muro húmedo; por eso el marco no se '
   'apoya directo sobre firme sin barrera. En exterior se suma sellador con filtro UV, que se renueva cada dos o tres '
   'años. En este clima no existe la madera exterior de cero mantenimiento, y quien la promete está omitiendo algo.'),
  ('Herraje, marco y el error de comprar solo la hoja',
   'Una puerta es hoja, marco, bisagras y cerradura, y el conjunto se comporta como el más débil de los cuatro. La '
   'hoja sólida colgada de bisagras livianas se descuelga y roza en meses; el marco mal anclado transmite cualquier '
   'movimiento del muro. En puerta de entrada el herraje va reforzado y, cerca del mar, en inoxidable. Cotizamos '
   'siempre el conjunto completo instalado, porque comparar precios de hoja suelta contra conjunto instalado es la '
   'confusión más común al pedir presupuesto.'),
  ('Medida a medida: por qué casi nunca sirve la puerta de línea',
   'Los vanos de obra en esta región rara vez coinciden con las medidas comerciales, y forzar una puerta de línea '
   'significa recortar el vano o rellenar con marco sobredimensionado. La puerta a medida se fabrica al vano real, con '
   'la holgura correcta arriba y abajo para el movimiento del material con la humedad. En rehabilitación es todavía '
   'más claro: los vanos viejos casi nunca están a plomo.')],
 faq=[
  ('¿Cuánto cuesta una puerta de madera?',
   'De $4,500 a $9,000 MXN por hoja la puerta interior de tambor con marco y herraje, de $12,000 a $45,000 la puerta '
   'sólida de madera dura, y de $25,000 a $85,000 la puerta de entrada principal.'),
  ('¿Qué madera es mejor para puerta de exterior?',
   'Tzalam o parota tratadas, siempre bajo alero o volado que las proteja de sol directo y lluvia. Sin esa protección '
   'ninguna madera aguanta bien en esta costa, y es preferible cambiar de material en esa posición.'),
  ('¿Cada cuánto hay que darle mantenimiento?',
   'Resellado cada dos o tres años en exterior, y prácticamente ninguno en interior climatizado más allá de la '
   'limpieza. El mantenimiento se entrega por escrito con la puerta.'),
  ('¿La puerta de tambor aísla el ruido?',
   'No de forma significativa. Para aislamiento acústico real hace falta hoja sólida y un marco bien sellado. Es el '
   'motivo principal para poner madera sólida en una puerta interior.'),
  ('¿Fabrican también el marco y colocan?',
   'Sí, cotizamos el conjunto completo instalado: hoja, marco, bisagras y cerradura. Comparar hoja suelta contra '
   'conjunto instalado es lo que más distorsiona los presupuestos de puertas.')],
 links=lambda: city_links('carpinteria-%s', 'Carpintería a medida') +
               [('/closets-a-medida/', 'Clósets a medida'), ('/cocinas-de-madera/', 'Cocinas de madera')]),

'albercas-infinity': dict(
 title='Albercas Infinity: Precios 2026 y Cómo Funcionan | Recrea',
 desc=('Albercas infinity y desbordantes en la Riviera Maya: precios 2026, tanque de '
       'compensación, cuánto desnivel hace falta y qué cuesta operarlas.'),
 h1='Albercas Infinity: Precios, Sistema y Cuándo Conviene',
 lead=('Cómo funciona realmente una alberca infinity, cuánto desnivel necesita para que '
       'el efecto se lea, qué cuesta construirla y qué cuesta mantenerla encendida.'),
 head=('Tipo de alberca infinity', 'Ideal para', 'Precio 2026'),
 rows=[('Infinity de un lado (borde simple)', 'Lote con desnivel hacia vista o selva', '$22,000 – $34,000 USD'),
       ('Infinity de dos lados (en esquina)', 'Terrenos de esquina y vistas dobles', '$30,000 – $45,000 USD'),
       ('Perimetral desbordante (4 lados)', 'Efecto espejo completo, proyecto de diseño', '$38,000 – $62,000 USD'),
       ('Infinity en rooftop', 'Con refuerzo estructural de losa', '$34,000 – $75,000 USD'),
       ('Infinity comercial / hotel', 'Cumplimiento normativo de uso público', '$55,000 – $140,000 USD'),
       ('Tanque de compensación y equipo', 'Cárcamo, bomba de recuperación y control', '$4,500 – $14,000 USD')],
 secs=[
  ('Qué es y cómo funciona una alberca infinity',
   'Es una alberca cuyo nivel de agua coincide exactamente con el borde de uno o varios lados, de modo que el agua '
   'desborda de forma continua sobre un canal oculto y baja a un tanque de compensación, desde donde una bomba la '
   'devuelve al vaso. Lo que el ojo lee como agua sin borde es un sistema de recirculación permanente. De ahí salen '
   'las dos consecuencias prácticas: hay más equipo que en una alberca normal, y el borde tiene que estar nivelado con '
   'una tolerancia que no admite improvisación. Si un extremo queda unos milímetros más alto, el agua desborda solo '
   'por la mitad y el efecto se pierde.'),
  ('Cuánto desnivel hace falta de verdad',
   'Para que el efecto se lea conviene al menos medio metro de caída visual del otro lado del borde; con menos, el ojo '
   'no separa el agua del terreno y el sobrecosto no se justifica. Lo ideal está entre uno y tres metros, que es donde '
   'el espejo funciona y el canal se resuelve sin obra de contención mayor. Con más desnivel se puede, pero entra muro '
   'de contención y el presupuesto cambia de escala. En terreno plano sin vista, la misma inversión rinde mucho más en '
   'una alberca convencional más grande, con mejor acabado y con área exterior resuelta: lo decimos antes de cotizar '
   'porque es la conversación que evita el arrepentimiento caro.'),
  ('El tanque de compensación y el muro del borde libre',
   'El cárcamo tiene que absorber el volumen de desborde en operación más el desplazamiento de los bañistas al entrar. '
   'Corto de volumen, la bomba de recuperación succiona en vacío y se sacrifica; sobrado, se paga obra de más. Se '
   'calcula sobre la superficie del vaso y la longitud del borde libre. El otro punto es estructural: el muro del lado '
   'desbordante soporta el empuje del agua sin el contrapeso de terreno del otro lado, y en lote en pendiente apoya '
   'sobre relleno o roca cortada, así que se calcula aparte con armado propio. En rooftop el problema lo decide el '
   'cálculo de la losa: el agua pesa una tonelada por metro cúbico.'),
  ('Qué cuesta tenerla encendida',
   'Una infinity trae una bomba más que una alberca normal, y esa bomba trabaja siempre que el efecto esté encendido. '
   'Con bomba de velocidad variable y temporizador el consumo se controla; con bomba de una sola velocidad corriendo '
   'todo el día, la cuenta de luz sorprende. La superficie en movimiento evapora más, así que la reposición automática '
   'de agua es parte del sistema y no un extra. Sume entre $800 y $1,500 MXN al mes sobre el mantenimiento de una '
   'alberca convencional del mismo tamaño, más la limpieza del canal de rebose, que junta hoja y sedimento. Muchos '
   'propietarios operan el desborde por horas y el resto del tiempo la usan como alberca normal.'),
  ('Acabado: por qué el color oscuro y el borde importan tanto',
   'El borde de rebose es la pieza que más delata una obra mal hecha, porque cualquier desnivel se marca con el agua '
   'corriendo: se resuelve con pieza rectificada o con chukum bien aplicado y con la junta al mínimo. En acabado '
   'interior, el chukum en tono oscuro da el espejo más limpio y el mosaico veneciano oscuro es la alternativa '
   'reparable pieza por pieza. El acabado claro se ve bien de cerca y arruina el efecto espejo a distancia, que es '
   'justamente aquello por lo que se paga una infinity.')],
 faq=[
  ('¿Cuánto cuesta una alberca infinity?',
   'De $22,000 a $34,000 USD la infinity de un lado, de $30,000 a $45,000 la de dos lados y de $38,000 a $62,000 la '
   'perimetral desbordante. En rooftop, de $34,000 a $75,000 USD según el refuerzo estructural que pida la losa.'),
  ('¿Cuánto más cuesta que una alberca normal?',
   'Entre 40% y 80% más que una alberca convencional del mismo tamaño. La diferencia son el canal de rebose, el tanque '
   'de compensación, la bomba de recuperación y el muro del borde libre.'),
  ('¿Necesito desnivel para hacer una infinity?',
   'Sí: al menos medio metro de caída visual para que el efecto se lea, e idealmente entre uno y tres metros. En '
   'terreno plano sin vista no se justifica.'),
  ('¿Consume mucha más agua y electricidad?',
   'Más que una alberca cerrada. La superficie en movimiento evapora más y la bomba de recuperación trabaja mientras '
   'el efecto está encendido. Con bomba de velocidad variable, reposición automática y operación por horas, el '
   'sobrecosto se mantiene razonable.'),
  ('¿Cuánto tarda construirla?',
   'De diez a dieciséis semanas, entre tres y cuatro más que una alberca convencional. El tiempo extra es el cárcamo, '
   'la nivelación verificada del borde y la puesta a punto del control de nivel.')],
 links=lambda: city_links('albercas-infinity-%s', 'Albercas infinity') +
               [('/construccion-albercas/', 'Construcción de albercas'),
                ('/albercas-cancun/', 'Albercas en Cancún')]),
}


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src = open(kw1.TPL, encoding='utf-8').read()
    built = {}
    for slug, d in PAGES.items():
        page = dict(d)
        page['links'] = d['links']()
        page['table'] = d['head'] + (d['rows'],)
        os.makedirs(slug, exist_ok=True)
        html = kw1.build(slug, page, src)
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        body = re.sub(r'<[^>]+>', ' ', html[html.index('<h1>'):html.index('<footer')]).lower().split()
        built[slug] = set(tuple(body[j:j + 6]) for j in range(len(body) - 5))
        print('%-24s title %2d  desc %3d  words %d' % (slug + '/', len(page['title']), len(page['desc']), len(body)))
    ks = list(built)
    mx = max((len(built[a] & built[b]) / len(built[a] | built[b]), a, b)
             for i, a in enumerate(ks) for b in ks[i + 1:])
    print('max pairwise similarity: %.2f  (%s vs %s)' % mx)
