#!/usr/bin/env python3
"""Generates the ES "construcción de casas en {ciudad}" cluster.

Gap found 2026-08-06: the site had ZERO pages targeting the service phrase
"construcción de casas" (only "constructora/empresas de construcción").
Angle = obra nueva paso a paso (process + price per m² + timeline), which does
not cannibalise the company pages ("constructora [ciudad]") or the cost guides
("cuánto cuesta construir una casa en [ciudad]" = informational)."""
import os, json

BASE = 'https://construction-recrea.com'
WA = 'https://wa.me/529844525333'

CITIES = {
 'playa-del-carmen': dict(
   city='Playa del Carmen', muni='Solidaridad', pre='en',
   zones='Playacar, Corasol, Zazil-Ha, Ejido, Villas del Mar, Selvamar y Mayakoba',
   m2='$12,000 – $25,000', usd='$650 – $1,380',
   sizes=[('Casa 100 m² (2 recámaras)','$1.6M – $2.5M','$88,000 – $138,000'),
          ('Casa 150 m² (3 rec. + alberca)','$2.7M – $4.5M','$150,000 – $250,000'),
          ('Casa 200 m² (3–4 recámaras)','$3.5M – $6M','$194,000 – $330,000'),
          ('Villa 300 m² de lujo','$7.5M – $13.5M','$415,000 – $750,000')],
   norm='En Solidaridad el trámite arranca con la constancia de uso de suelo y el PDU vigente: define cuántos niveles y qué COS/CUS puede construir en su lote. La licencia de construcción exige proyecto firmado por un DRO registrado en el municipio, memoria estructural y planos de instalaciones. Si el terreno colinda con manglar, duna o un cenote, se suma la autorización ambiental estatal.',
   soil='El subsuelo es roca caliza (karst): buena capacidad de carga, pero con cavidades y cenotes ocultos. Por eso arrancamos con estudio de mecánica de suelos — define si la cimentación va con zapatas corridas, losa de cimentación o pilotes, y evita el sobrecosto clásico de descubrir una oquedad ya con la obra empezada.',
   extra='Playa del Carmen es el mercado más equilibrado de la Riviera Maya: terreno más accesible que Tulum, mano de obra y proveedores locales establecidos, y la mejor relación costo/plusvalía para casa propia o para rentar.',
   links=[('/cuanto-cuesta-construir-casa-playa-del-carmen/','¿Cuánto cuesta construir una casa?'),
          ('/permisos-de-construccion-playa-del-carmen/','Permisos de construcción en Playa del Carmen'),
          ('/','Constructora en Playa del Carmen'),
          ('/villas-de-lujo-playa-del-carmen/','Villas de lujo'),
          ('/cimentacion-y-losas-playa-del-carmen/','Cimentación y losas'),
          ('/calculadora/','Calculadora de costos'),
          ('/blog-es/costos-construccion-playa-del-carmen-2026.html','Costos de construcción 2026'),
          ('/blog-es/mejores-zonas-construir-playa-del-carmen.html','Mejores zonas para construir')],
   faq=[('¿Cuánto cuesta la construcción de una casa en Playa del Carmen?',
         'De $12,000 a $25,000 MXN por m² según el nivel de acabados. Una casa de 150 m² con alberca cuesta entre $2.7 y $4.5 millones MXN ($150,000–$250,000 USD), sin incluir el terreno.'),
        ('¿Cuánto tarda construir una casa?',
         '8 a 14 meses de obra, más 2 a 4 meses de proyecto y permisos. Del primer contacto a la entrega de llaves: 12 a 18 meses para una casa de 150–200 m².'),
        ('¿Trabajan con precio fijo?',
         'Sí. Después del proyecto ejecutivo entregamos presupuesto cerrado por partidas y contrato a precio fijo con calendario de pagos por avance de obra. Lo que cambia el precio son los cambios que usted pida durante la obra.'),
        ('¿Ustedes consiguen los permisos?',
         'Sí. Gestionamos uso de suelo, licencia de construcción en Solidaridad, DRO, alta de CFE y agua, y el trámite ambiental si el terreno lo requiere. Usted no hace filas.'),
        ('¿Pueden construir si vivo en otro país?',
         'Es la mitad de nuestros clientes. Contrato bilingüe a precio fijo, pagos por avance y reporte semanal con fotos y video del avance real de su casa.'),
        ('¿Incluyen el diseño arquitectónico?',
         'Sí. Proyecto arquitectónico, estructural e instalaciones, todo en casa. Si ya trae planos, los revisamos y cotizamos la obra directamente.')],
   testi=[('"Construyeron nuestra casa de 180 m² en Zazil-Ha con precio fijo. Cero sobrecostos y entrega en el mes prometido."','Propietaria, Playa del Carmen'),
          ('"Vivimos en Canadá y seguimos toda la obra por video semanal. Llegamos a la casa terminada tal cual los planos."','Cliente extranjero, Playacar')]),

 'cancun': dict(
   city='Cancún', muni='Benito Juárez', pre='en',
   zones='Supermanzanas, Residencial Cumbres, Puerto Cancún, Zona Hotelera y Alfredo V. Bonfil',
   m2='$11,500 – $24,000', usd='$630 – $1,330',
   sizes=[('Casa 100 m² (2 recámaras)','$1.5M – $2.4M','$83,000 – $132,000'),
          ('Casa 150 m² (3 rec. + alberca)','$2.5M – $4.3M','$140,000 – $238,000'),
          ('Casa 200 m² (3–4 recámaras)','$3.3M – $5.7M','$183,000 – $315,000'),
          ('Residencia 300 m² de lujo','$7M – $12.9M','$390,000 – $715,000')],
   norm='En Benito Juárez la licencia de construcción se tramita ante la Dirección de Desarrollo Urbano con proyecto avalado por DRO. En Puerto Cancún y la Zona Hotelera se añade el visto bueno de FONATUR y, en lotes frente al mar, la concesión ZOFEMAT. En fraccionamientos con reglamento interno (Cumbres, Aqua, Lagos) hay además comité de diseño con restricciones de altura, fachada y horarios de obra.',
   soil='Suelo calizo con zonas de relleno y nivel freático alto cerca de la laguna Nichupté. El estudio de mecánica de suelos define el tipo de cimentación y el tratamiento contra humedad; en lotes cercanos a la laguna es obligatorio prever impermeabilización reforzada y protección anticorrosiva del acero.',
   extra='Cancún ofrece el terreno urbano más económico de la zona norte y proveedores a 20 minutos de obra, lo que abarata logística frente a Tulum. Es el mejor costo por m² construido de la Riviera Maya para casa propia.',
   links=[('/blog-es/cuanto-cuesta-construir-casa-cancun.html','¿Cuánto cuesta construir una casa en Cancún?'),
          ('/permisos-de-construccion-cancun/','Permisos de construcción en Cancún'),
          ('/constructora-cancun/','Constructora en Cancún'),
          ('/villas-de-lujo-puerto-cancun/','Villas de lujo en Puerto Cancún'),
          ('/remodelacion-casas-cancun/','Remodelación de casas en Cancún'),
          ('/calculadora/','Calculadora de costos'),
          ('/blog-es/permisos-construccion-cancun.html','Guía de permisos en Cancún'),
          ('/empresas-de-construccion-cancun/','Empresas de construcción en Cancún')],
   faq=[('¿Cuánto cuesta la construcción de una casa en Cancún?',
         'Entre $11,500 y $24,000 MXN por m² según acabados. Una casa de 150 m² con alberca ronda $2.5–$4.3 millones MXN ($140,000–$238,000 USD), sin terreno.'),
        ('¿Construir en Cancún sale más barato que en Playa del Carmen?',
         'Sí, entre 3% y 5% menos en obra: proveedores más cercanos, más mano de obra disponible y terreno urbano más accesible fuera de Puerto Cancún y la Zona Hotelera.'),
        ('¿Cuánto tarda la obra?',
         '8 a 14 meses de construcción más 2 a 4 meses de proyecto y licencia municipal en Benito Juárez.'),
        ('¿Construyen dentro de fraccionamientos con reglamento?',
         'Sí. Presentamos el proyecto al comité de diseño, respetamos horarios y accesos de obra y coordinamos con la administración del residencial.'),
        ('¿Gestionan los permisos en Benito Juárez?',
         'Sí: uso de suelo, licencia de construcción, DRO, CFE y agua. En Puerto Cancún y Zona Hotelera tramitamos también FONATUR y, si aplica, ZOFEMAT.'),
        ('¿Trabajan con precio fijo?',
         'Sí, contrato a precio fijo por partidas tras el proyecto ejecutivo, con pagos por avance de obra verificado.')],
   testi=[('"Construimos nuestra casa en Cumbres con ellos. Manejaron el comité del fraccionamiento y todos los permisos sin que nosotros moviéramos un dedo."','Propietario, Cancún'),
          ('"Presupuesto cerrado y avance semanal documentado. La obra terminó dentro del rango prometido."','Cliente, Puerto Cancún')]),

 'tulum': dict(
   city='Tulum', muni='Tulum', pre='en',
   zones='Aldea Zamá, La Veleta, Región 15, Holistika y la zona de Tulum centro',
   m2='$13,000 – $27,000', usd='$720 – $1,500',
   sizes=[('Casa 100 m² (2 recámaras)','$1.7M – $2.7M','$94,000 – $150,000'),
          ('Casa 150 m² (3 rec. + alberca)','$2.9M – $4.9M','$160,000 – $270,000'),
          ('Casa 200 m² (3–4 recámaras)','$3.8M – $6.5M','$210,000 – $360,000'),
          ('Villa 300 m² de lujo','$8.1M – $14.6M','$450,000 – $810,000')],
   norm='Tulum es el municipio más estricto de la Riviera Maya. Además de uso de suelo y licencia municipal con DRO, la mayoría de los proyectos requiere autorización ambiental de la SEMA (y MIA cuando hay desmonte o cercanía a cenotes o manglar). El PDU limita densidad y altura por zona, y la obra debe respetar el porcentaje de área verde permeable. Los tiempos de permiso son más largos: presupueste 3 a 5 meses.',
   soil='Roca caliza fracturada con cenotes y cavernas frecuentes, sobre todo en Región 15 y La Veleta. El estudio geofísico previo no es opcional: encontrar una caverna bajo el desplante ya iniciada la cimentación puede costar cientos de miles de pesos y semanas de retraso.',
   extra='Tulum es el m² más caro de la región por logística, normativa ambiental y demanda de acabados premium (chukum, madera dura, diseño bioclimático), pero también el mayor rendimiento en renta vacacional.',
   links=[('/blog-es/costo-construir-casa-tulum.html','¿Cuánto cuesta construir una casa en Tulum?'),
          ('/permisos-de-construccion-tulum-ciudad/','Permisos de construcción en Tulum'),
          ('/constructora-tulum/','Constructora en Tulum'),
          ('/villas-de-lujo-aldea-zama-tulum/','Villas de lujo en Aldea Zamá'),
          ('/villas-de-lujo-la-veleta-tulum/','Villas de lujo en La Veleta'),
          ('/construccion-eco-lodge-retiro-tulum/','Eco-lodges y retiros'),
          ('/blog-es/construccion-sustentable-tulum.html','Construcción sustentable en Tulum'),
          ('/blog-es/construir-cerca-cenote-riviera-maya.html','Construir cerca de un cenote')],
   faq=[('¿Cuánto cuesta la construcción de una casa en Tulum?',
         'De $13,000 a $27,000 MXN por m². Una casa de 150 m² con alberca cuesta entre $2.9 y $4.9 millones MXN ($160,000–$270,000 USD), sin terreno.'),
        ('¿Por qué construir en Tulum cuesta más?',
         'Normativa ambiental (SEMA/MIA), logística más larga desde proveedores, terreno con cenotes y cavernas, y un estándar de acabados más alto que en el resto de la Riviera Maya.'),
        ('¿Cuánto tardan los permisos en Tulum?',
         'De 3 a 5 meses cuando interviene la SEMA. Por eso arrancamos el trámite en paralelo al proyecto ejecutivo para no perder tiempo.'),
        ('¿Se puede construir en Región 15?',
         'Sí, es la zona de mejor precio de entrada en Tulum. Requiere revisar la situación legal del predio y el uso de suelo antes de comprar: lo verificamos antes de que usted firme.'),
        ('¿Manejan diseño bioclimático y chukum?',
         'Sí. Ventilación cruzada, orientación solar, cisterna y captación pluvial, acabados en chukum y madera dura tratada — el estándar que pide el mercado de Tulum.'),
        ('¿Puedo rentar la casa en Airbnb?',
         'Sí, y la diseñamos para eso: distribución para huéspedes, alberca, mobiliario FF&E y trámite de licencia de funcionamiento si opera como renta vacacional.')],
   testi=[('"Nos llevaron el trámite de SEMA completo en Aldea Zamá. Sin ese acompañamiento no habríamos podido construir."','Propietario, Aldea Zamá'),
          ('"Villa de 200 m² en La Veleta terminada para renta. Ocupación alta desde el primer año."','Inversionista, Tulum')]),

 'puerto-aventuras': dict(
   city='Puerto Aventuras', muni='Solidaridad', pre='en',
   zones='la zona de la marina, Xcalacoco, Bahía Chemuyil y los fraccionamientos privados de Puerto Aventuras',
   m2='$13,000 – $27,000', usd='$720 – $1,500',
   sizes=[('Casa 100 m² (2 recámaras)','$1.7M – $2.7M','$94,000 – $150,000'),
          ('Casa 150 m² (3 rec. + alberca)','$2.9M – $4.9M','$160,000 – $270,000'),
          ('Casa 200 m² (3–4 recámaras)','$3.8M – $6.5M','$210,000 – $360,000'),
          ('Villa 300 m² de lujo','$8.1M – $14.6M','$450,000 – $810,000')],
   norm='Puerto Aventuras pertenece a Solidaridad, así que el uso de suelo, la licencia de construcción y el DRO se tramitan en Playa del Carmen. La diferencia real está adentro: al ser una comunidad privada, el proyecto pasa además por la administración y el comité de diseño del fraccionamiento, con reglas de altura, fachada, colores, horarios de obra y acceso de camiones. Trabajamos con esos reglamentos desde hace años y presentamos el expediente completo para no perder semanas en observaciones.',
   soil='Roca caliza con manto freático cercano y ambiente altamente salino por la proximidad al mar y a la marina. Además del estudio de mecánica de suelos, aquí es obligatorio prever recubrimientos mayores en el acero de refuerzo, herrería tratada y cancelería de aluminio anodizado: en Puerto Aventuras la corrosión, no la estructura, es lo que arruina casas mal construidas. En lotes frente al mar aplica concesión ZOFEMAT.',
   extra='Puerto Aventuras es una comunidad cerrada con marina, golf y seguridad 24/7, muy demandada por extranjeros y por renta vacacional: la casa se construye pensando en huéspedes y en mantenimiento bajo cuando usted no está.',
   links=[('/constructora-puerto-aventuras/','Constructora en Puerto Aventuras'),
          ('/permisos-de-construccion-puerto-aventuras/','Permisos de construcción en Puerto Aventuras'),
          ('/villas-de-lujo-puerto-aventuras/','Villas de lujo en Puerto Aventuras'),
          ('/remodelacion-condominios-puerto-aventuras/','Remodelación de condominios'),
          ('/villa-de-inversion-airbnb-puerto-aventuras/','Villa de inversión Airbnb'),
          ('/calculadora/','Calculadora de costos'),
          ('/blog-es/permisos-construccion-puerto-aventuras.html','Guía de permisos'),
          ('/construccion-de-casas-riviera-maya/','Construcción de casas en la Riviera Maya')],
   faq=[('¿Cuánto cuesta la construcción de una casa en Puerto Aventuras?',
         'De $13,000 a $27,000 MXN por m² según acabados. Una casa de 150 m² con alberca cuesta entre $2.9 y $4.9 millones MXN ($160,000–$270,000 USD), sin el terreno.'),
        ('¿Cómo funciona el permiso dentro del fraccionamiento?',
         'Doble vía: licencia municipal en Solidaridad (uso de suelo, DRO, licencia de construcción) y aprobación del comité de diseño de Puerto Aventuras. Presentamos ambos expedientes y coordinamos accesos y horarios con la administración.'),
        ('¿Cuánto tarda la obra?',
         '8 a 14 meses de construcción más 2 a 4 meses de proyecto y permisos, incluyendo el trámite ante el comité del fraccionamiento.'),
        ('¿Qué cuidados extra exige estar junto al mar y la marina?',
         'Recubrimientos mayores en acero, herrería con tratamiento anticorrosivo, cancelería de aluminio anodizado, impermeabilización reforzada y equipos de A/A aptos para ambiente salino. Va incluido en nuestro estándar constructivo.'),
        ('¿Se puede rentar la casa en Airbnb?',
         'Sí, es uno de los mercados de renta más consolidados de la Riviera Maya. Diseñamos distribución para huéspedes, alberca y mobiliario FF&E, y coordinamos con el reglamento del fraccionamiento.'),
        ('¿Trabajan con precio fijo?',
         'Sí, contrato a precio fijo por partidas después del proyecto ejecutivo, con pagos por avance verificado y reporte semanal con fotos y video.')],
   testi=[]),

 'akumal': dict(
   city='Akumal', muni='Tulum', pre='en',
   zones='Akumal Norte, Akumal Pueblo, Aventuras Akumal, Media Luna Bay y Jade Bay',
   m2='$13,500 – $28,000', usd='$750 – $1,550',
   sizes=[('Casa 100 m² (2 recámaras)','$1.8M – $2.8M','$100,000 – $155,000'),
          ('Casa 150 m² (3 rec. + alberca)','$3.0M – $5.0M','$166,000 – $277,000'),
          ('Casa 200 m² (3–4 recámaras)','$3.9M – $6.7M','$216,000 – $370,000'),
          ('Villa 300 m² de lujo','$8.4M – $15.1M','$465,000 – $835,000')],
   norm='Akumal pertenece al municipio de Tulum, no a Solidaridad: eso cambia todo el trámite. Además del uso de suelo y la licencia municipal con DRO, la mayoría de los predios requiere autorización ambiental de la SEMA, y los lotes frente al mar suman concesión ZOFEMAT. Akumal es zona de anidación de tortuga marina, así que hay restricciones de iluminación hacia la playa y de trabajos nocturnos en temporada de anidación (mayo–octubre). Presupueste de 3 a 5 meses de permisos.',
   soil='Caliza fracturada con cavernas y cenotes, manto freático somero y ambiente salino intenso frente al arrecife. Aquí el estudio geofísico previo evita el peor sobrecosto de la zona, y el diseño estructural se hace con recubrimientos y aditivos para ambiente marino. El drenaje debe resolverse con biodigestor o planta compacta: descargar mal en Akumal es un riesgo legal y ambiental serio por la cercanía del arrecife.',
   extra='Akumal es el mercado más eco-sensible y más premium por m² de la costa norte: obra pequeña, logística más larga y estándar de acabados alto (chukum, madera dura, diseño bioclimático), con altísima demanda de renta vacacional frente a la bahía.',
   links=[('/constructora-akumal/','Constructora en Akumal'),
          ('/permisos-de-construccion-akumal/','Permisos de construcción en Akumal'),
          ('/villas-de-lujo-akumal/','Villas de lujo en Akumal'),
          ('/villa-de-inversion-airbnb-akumal/','Villa de inversión Airbnb en Akumal'),
          ('/blog-es/cuanto-cuesta-construir-casa-akumal.html','¿Cuánto cuesta construir en Akumal?'),
          ('/calculadora/','Calculadora de costos'),
          ('/blog-es/permisos-construccion-akumal.html','Guía de permisos'),
          ('/construccion-de-casas-riviera-maya/','Construcción de casas en la Riviera Maya')],
   faq=[('¿Cuánto cuesta la construcción de una casa en Akumal?',
         'De $13,500 a $28,000 MXN por m². Una casa de 150 m² con alberca cuesta entre $3.0 y $5.0 millones MXN ($166,000–$277,000 USD), sin el terreno.'),
        ('¿Por qué Akumal es más caro que Playa del Carmen?',
         'Trámite ambiental de SEMA, logística más larga hasta proveedores, protección de tortuga y arrecife, y estándar de acabados más alto. La diferencia de obra ronda el 10–12%.'),
        ('¿Qué permisos necesito en Akumal?',
         'Uso de suelo y licencia municipal de Tulum con DRO, autorización ambiental de SEMA en la mayoría de los predios y concesión ZOFEMAT si el lote es frente al mar. Nosotros gestionamos los tres.'),
        ('¿Hay restricciones por la tortuga marina?',
         'Sí. En temporada de anidación (mayo–octubre) se restringe la iluminación dirigida a la playa y los trabajos nocturnos en lotes costeros. El proyecto de iluminación se diseña desde el inicio para cumplir sin sacrificar la casa.'),
        ('¿Cómo se resuelve el drenaje?',
         'Con biodigestor o planta de tratamiento compacta, nunca con fosa simple: la cercanía del arrecife y del manto freático lo exige, y es lo que revisa la autoridad ambiental.'),
        ('¿Puedo construir si vivo fuera de México?',
         'Sí: contrato bilingüe a precio fijo, pagos por avance, reporte semanal con fotos y video, y coordinación con su notario y fideicomiso.')],
   testi=[]),

 'riviera-maya': dict(
   city='la Riviera Maya', muni='Solidaridad, Tulum, Benito Juárez y Puerto Morelos', pre='en',
   zones='Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal y Puerto Morelos',
   m2='$11,500 – $27,000', usd='$630 – $1,500',
   sizes=[('Casa 100 m² (2 recámaras)','$1.5M – $2.7M','$83,000 – $150,000'),
          ('Casa 150 m² (3 rec. + alberca)','$2.5M – $4.9M','$140,000 – $270,000'),
          ('Casa 200 m² (3–4 recámaras)','$3.3M – $6.5M','$183,000 – $360,000'),
          ('Villa 300 m² de lujo','$7M – $14.6M','$390,000 – $810,000')],
   norm='Cada municipio tiene reglas distintas y esa es la primera fuente de retrasos. Solidaridad (Playa del Carmen) resuelve por PDU y DRO municipal; Benito Juárez (Cancún) suma FONATUR en Puerto Cancún y Zona Hotelera; Tulum exige autorización ambiental de la SEMA en la mayoría de los predios; Puerto Morelos, municipio desde 2016, aplica criterios propios por su cercanía al arrecife. Trabajamos en los cuatro y arrancamos el trámite que corresponde a su terreno.',
   soil='Toda la costa se asienta sobre roca caliza con cenotes, cavernas y nivel freático somero. El estudio de mecánica de suelos —y estudio geofísico donde hay riesgo de caverna— define la cimentación y es la mejor inversión del proyecto: evita el sobrecosto más caro de la región.',
   extra='Construimos en todo el corredor, de Puerto Morelos a Tulum, con un solo equipo, un solo contrato y un solo responsable de obra. La diferencia de costo entre extremos del corredor llega al 15% por logística y normativa.',
   links=[('/constructora-riviera-maya/','Constructora en la Riviera Maya'),
          ('/construccion-de-casas-puerto-aventuras/','Construcción de casas en Puerto Aventuras'),
          ('/construccion-de-casas-akumal/','Construcción de casas en Akumal'),
          ('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'),
          ('/construccion-de-casas-cancun/','Construcción de casas en Cancún'),
          ('/construccion-de-casas-tulum/','Construcción de casas en Tulum'),
          ('/permisos-licencias-construccion-riviera-maya/','Permisos, licencias y DRO'),
          ('/calculadora/','Calculadora de costos'),
          ('/mapa-precios/','Mapa de precios por zona'),
          ('/construccion-para-extranjeros-riviera-maya/','Construcción para extranjeros')],
   faq=[('¿Cuánto cuesta la construcción de una casa en la Riviera Maya?',
         'De $11,500 a $27,000 MXN por m² según ciudad y acabados: Cancún es lo más económico, Tulum lo más caro. Una casa de 150 m² con alberca va de $2.5 a $4.9 millones MXN.'),
        ('¿En qué ciudades construyen?',
         'Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal y Puerto Morelos — todo el corredor, con oficina en Corasol, Playa del Carmen.'),
        ('¿Dónde conviene construir?',
         'Cancún y Puerto Morelos por costo; Playa del Carmen por equilibrio entre precio y plusvalía; Tulum por rendimiento en renta vacacional. Le damos números antes de que compre el terreno.'),
        ('¿Revisan el terreno antes de comprarlo?',
         'Sí. Uso de suelo, situación legal, riesgo de cenote o caverna y factibilidad de servicios. Es la revisión más barata que hará en todo el proyecto.'),
        ('¿Cuánto tarda una casa llave en mano?',
         '8 a 14 meses de obra más 2 a 5 meses de proyecto y permisos, según el municipio.'),
        ('¿Trabajan con clientes que viven fuera de México?',
         'Sí, es la mitad de nuestra cartera: contrato bilingüe a precio fijo, pagos por avance, reporte semanal en foto y video, y coordinación con su notario y fideicomiso.')],
   testi=[('"Un solo contrato para terreno, proyecto, permisos y obra. Nos ahorró coordinar cinco proveedores desde otro país."','Cliente, Riviera Maya'),
          ('"Comparamos tres constructoras. Fueron los únicos que nos dieron presupuesto por partidas y lo respetaron."','Propietario, Puerto Aventuras')]),
}

STEPS = [
 ('Revisión del terreno', 'Uso de suelo, situación legal, servicios y riesgo de cenote o caverna. Antes de que usted compre, si aún no lo hizo.', '1–2 semanas'),
 ('Anteproyecto y presupuesto', 'Distribución, volumetría y presupuesto preliminar por m². Aquí se decide el alcance real según su presupuesto.', '2–3 semanas'),
 ('Proyecto ejecutivo', 'Planos arquitectónicos, estructurales, eléctricos e hidrosanitarios firmados por DRO, más presupuesto cerrado por partidas.', '4–6 semanas'),
 ('Permisos y licencias', 'Uso de suelo, licencia de construcción, DRO, alta de CFE y agua y trámite ambiental si aplica.', '4–20 semanas'),
 ('Cimentación', 'Mecánica de suelos, excavación en roca, zapatas o losa de cimentación y preparación de instalaciones bajo losa.', '3–5 semanas'),
 ('Obra gris', 'Estructura, muros, losas y azoteas. Es la etapa que define la calidad estructural frente a huracanes y salinidad.', '10–16 semanas'),
 ('Instalaciones y acabados', 'Eléctrico, hidrosanitario, aire acondicionado, aplanados, pisos, carpintería, herrería, alberca y chukum.', '12–20 semanas'),
 ('Entrega llave en mano', 'Limpieza, pruebas de instalaciones, manual de la casa, planos as-built y garantía por escrito de 1 año.', '1–2 semanas'),
]

INCLUYE = ['Proyecto arquitectónico, estructural e instalaciones', 'DRO y licencia de construcción municipal',
 'Cimentación y estructura de concreto armado', 'Instalación eléctrica, hidrosanitaria y de aire acondicionado',
 'Aplanados, pisos, pintura y carpintería de closets y cocina', 'Herrería, cancelería y protección anticorrosiva',
 'Cisterna, tinaco y equipo hidroneumático', 'Limpieza final, pruebas y garantía escrita de 1 año']
NO_INCLUYE = ['El terreno y los gastos notariales', 'Mobiliario y decoración (los cotizamos aparte como FF&E)',
 'Alberca, paisajismo y palapa si no se contratan en el paquete', 'Paneles solares, generador o domótica (opcionales)',
 'Cambios que usted solicite con la obra ya iniciada']

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def build(slug, d):
    city, url = d['city'], BASE + '/construccion-de-casas-' + slug + '/'
    City = city[3:] if city.startswith('la ') else city
    h1 = 'Construcción de Casas en ' + City
    title = h1 + ' | Obra Nueva Llave en Mano | Recrea'
    desc = ('Construcción de casas en %s: obra nueva llave en mano con precio fijo. '
            'Precios por m² 2026, proceso paso a paso, permisos y tiempos. 18+ años, 196+ proyectos.' % City)
    kw = ('construccion de casas %s, construccion de casas en %s, construir casa %s, '
          'obra nueva %s, casas llave en mano %s' % (City.lower(), City.lower(), City.lower(), City.lower(), City.lower()))

    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[
        {"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in d['faq']]}
    lb = {"@context":"https://schema.org","@type":"GeneralContractor","name":"Recrea Construcción",
        "url":url,"image":BASE+"/img/og-wallpaper.png","telephone":"+52-984-452-5333",
        "email":"constructionrecrea@gmail.com","priceRange":"$$",
        "address":{"@type":"PostalAddress","streetAddress":"Corasol","addressLocality":"Playa del Carmen",
                   "addressRegion":"Quintana Roo","postalCode":"77710","addressCountry":"MX"},
        "geo":{"@type":"GeoCoordinates","latitude":20.6296,"longitude":-87.0739},
        "areaServed":[{"@type":"City","name":z.strip()} for z in d['zones'].replace(' y ',', ').split(',')][:6],
        "makesOffer":{"@type":"Offer","itemOffered":{"@type":"Service","name":"Construcción de casas en "+City,
            "serviceType":"Obra nueva residencial llave en mano"}},
        "sameAs":["https://www.facebook.com/recrea.arquitectura","https://www.instagram.com/recrea_arquitectura"],
        "foundingDate":"2008","knowsLanguage":["es","en"]}
    alts = '\n  '.join('<link rel="alternate" hreflang="%s" href="%s/%s-%s/">' % (c, BASE, pfx, slug)
                       for c, pfx in [('es','construccion-de-casas'),('en','house-construction'),
                                      ('de','hausbau'),('ru','stroitelstvo-domov'),
                                      ('zh','zhuzhai-jianzao'),('fr','construction-de-maisons')])
    alts += '\n  <link rel="alternate" hreflang="x-default" href="%s/house-construction-%s/">' % (BASE, slug)
    bc = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Inicio","item":BASE+"/"},
        {"@type":"ListItem","position":2,"name":h1}]}

    steps = '\n'.join(
      '<div class="col-md-6"><div class="p-3 bg-light rounded h-100"><h5 class="mb-1">'
      '<span style="color:var(--accent)">%d.</span> %s</h5>'
      '<p class="small mb-1">%s</p><p class="small text-muted mb-0"><i class="bi bi-clock me-1"></i>%s</p></div></div>'
      % (i+1, s[0], s[1], s[2]) for i, s in enumerate(STEPS))
    sizes = '\n'.join('<tr><td>%s</td><td>%s MXN</td><td>%s USD</td></tr>' % t for t in d['sizes'])
    links = ' · '.join('<a href="%s">%s</a>' % l for l in d['links'])
    inc = '\n'.join('<li>%s</li>' % x for x in INCLUYE)
    ninc = '\n'.join('<li>%s</li>' % x for x in NO_INCLUYE)
    faq_html = '\n'.join(
      '<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button%s" type="button" '
      'data-bs-toggle="collapse" data-bs-target="#faq%d">%s</button></h3>'
      '<div id="faq%d" class="accordion-collapse collapse%s" data-bs-parent="#faqAcc"><div class="accordion-body">%s</div></div></div>'
      % ('' if i == 0 else ' collapsed', i, esc(q), i, ' show' if i == 0 else '', esc(a))
      for i, (q, a) in enumerate(d['faq']))
    testi = '\n'.join(
      '<div class="col-md-6"><div class="p-3 bg-light rounded h-100"><p class="mb-2">%s</p>'
      '<p class="small text-muted mb-0"><strong>%s</strong></p></div></div>' % t for t in d['testi'])
    testi_block = ('<h2 class="mt-4">Lo Que Dicen Nuestros Clientes</h2>\n<div class="row g-3 my-2">\n'
                   + testi + '\n</div>') if d['testi'] else ''

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta name="google-site-verification" content="0WwXyAoY4jeA2xgFFFB06a9HqEfzR7LnyLYVBrFTU0A" />
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{kw}">
  <link rel="preload" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" as="style">
  <link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="../css/style.min.css?v=7" rel="stylesheet">
  <script type="application/ld+json">{json.dumps(lb, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script>
  <link rel="canonical" href="{url}">
  {alts}
  <link rel="icon" href="../favicon.svg" type="image/svg+xml">
  <link rel="icon" href="../favicon.ico" sizes="32x32">
  <link rel="apple-touch-icon" href="../apple-touch-icon.png">
  <link rel="manifest" href="../site.webmanifest">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{BASE}/img/og-wallpaper.png">
  <meta property="og:url" content="{url}">
  <meta property="og:locale" content="es_MX">
  <meta property="og:site_name" content="Recrea Construction">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{BASE}/img/og-wallpaper.png">
</head>
<body class="has-top-bar">
<div class="top-cta-bar"><span>Cotización Gratis — Respondemos en 2 min</span><a href="{WA}?text=Hola!%20Quiero%20cotizar%20la%20construcci%C3%B3n%20de%20una%20casa" target="_blank" rel="noopener"><i class="bi bi-whatsapp me-1"></i>Cotizar</a></div>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
  <div class="container">
    <a class="navbar-brand fw-bold" href="/">RECREA</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu"><span class="navbar-toggler-icon"></span></button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto align-items-center">
        <li class="nav-item"><a class="nav-link" href="/services/servicios.html">Servicios</a></li>
        <li class="nav-item"><a class="nav-link" href="/#projects">Proyectos</a></li>
        <li class="nav-item"><a class="nav-link" href="/#about">Nosotros</a></li>
        <li class="nav-item"><a class="nav-link" href="/blog-es/">Blog</a></li>
        <li class="nav-item"><a class="nav-link" href="/noticias/">Noticias</a></li>
        <li class="nav-item"><a class="nav-link" href="/certificaciones/">Certificaciones</a></li>
        <li class="nav-item"><a class="nav-link" href="/#contact">Contacto</a></li>
      </ul>
    </div>
  </div>
</nav>
<div style="padding-top:116px"></div>
<nav class="container mt-3"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="/">Inicio</a></li><li class="breadcrumb-item active">{h1}</li></ol></nav>
<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>{h1}</h1>
<p class="lead">Obra nueva llave en mano en {city}: proyecto, permisos, cimentación, obra gris y acabados con un solo responsable y contrato a precio fijo.</p>
<p>Recrea construye casas en {d['zones']} desde 2008 — 196+ proyectos terminados en la Riviera Maya. Somos <a href="/">constructora en Playa del Carmen</a> con equipo propio de arquitectura, eléctrico, carpintería y herrería, así que su casa no depende de subcontratistas que aparecen y desaparecen.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Precio de la construcción de casas en {City} (2026):</strong> {d['m2']} MXN/m² ({d['usd']} USD/m²) según nivel de acabados, sin incluir el terreno.</div>

<h2 class="mt-4">Cuánto Cuesta la Construcción de una Casa en {City}</h2>
<p>Presupuestos reales de obra terminada, sin terreno ni mobiliario. El rango depende del nivel de acabados: económico, medio o premium (chukum, madera dura, cocina de autor, alberca desbordante).</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tipo de casa</th><th>Costo de obra</th><th>Equivalente</th></tr></thead><tbody>
{sizes}
</tbody></table></div>
<p>¿Quiere el número exacto para su terreno y sus m²? Use la <a href="/calculadora/">calculadora de costos</a> o pídanos un presupuesto por partidas.</p>

<h2 class="mt-4">Proceso de Construcción de Casas Paso a Paso</h2>
<p>Así trabajamos cada obra nueva, con los tiempos que manejamos en {City}:</p>
<div class="row g-3 my-2">
{steps}
</div>
<p class="mt-2"><strong>Total:</strong> de 8 a 14 meses de obra, más 2 a 5 meses de proyecto y permisos según el municipio.</p>

<h2 class="mt-4">Qué Incluye y Qué No Incluye el Precio por m²</h2>
<div class="row g-3 my-2">
<div class="col-md-6"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-check-circle me-2" style="color:#198754"></i>Incluido</h5><ul class="mb-0 small">
{inc}
</ul></div></div>
<div class="col-md-6"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-x-circle me-2" style="color:#dc3545"></i>No incluido</h5><ul class="mb-0 small">
{ninc}
</ul></div></div>
</div>

<h2 class="mt-4">Permisos y Normativa para Construir en {City}</h2>
<p>{d['norm']}</p>
<h3 class="mt-3">El terreno: lo que decide su cimentación</h3>
<p>{d['soil']}</p>
<p>{d['extra']}</p>
<p>Guías útiles: {links}</p>

<h2 class="mt-4">Por Qué Elegir Recrea para Construir su Casa</h2>
<ul>
<li><strong>196+ proyectos terminados</strong> en la Riviera Maya desde 2008</li>
<li><strong>Contrato a precio fijo</strong> por partidas — sin sobrecostos sorpresa</li>
<li><strong>Todo en una sola empresa</strong> — arquitectura, permisos, obra, eléctrico, carpintería, herrería</li>
<li><strong>DRO y arquitectos licenciados</strong> — obra 100% legal y trabajadores con IMSS</li>
<li><strong>Reportes semanales</strong> con fotos y video, ideal si usted no vive en México</li>
<li><strong>Garantía por escrito de 1 año</strong> sobre estructura e instalaciones</li>
</ul>

<h2 class="mt-5">Proyectos Reales</h2>
<div class="row g-3 my-2">
<div class="col-md-6"><img loading="lazy" src="../img/villa-pool-tropical.jpg" class="img-fluid rounded" alt="Casa con alberca construida por Recrea en {City}" style="width:100%;height:260px;object-fit:cover"></div>
<div class="col-md-6"><img loading="lazy" src="../img/residential-block-construction.jpg" class="img-fluid rounded" alt="Obra nueva residencial terminada por Recrea en {City}" style="width:100%;height:260px;object-fit:cover"></div>
</div>

{testi_block}

<div class="row g-3 my-4">
<div class="col-md-6"><a href="{WA}?text=Hola!%20Quiero%20cotizar%20la%20construcci%C3%B3n%20de%20una%20casa%20en%20{City.replace(' ', '%20')}" target="_blank" rel="noopener" class="btn btn-success btn-lg w-100"><i class="bi bi-whatsapp me-2"></i>WhatsApp — 2 min</a></div>
<div class="col-md-6"><a href="tel:+529844525333" class="btn btn-outline-dark btn-lg w-100"><i class="bi bi-telephone me-2"></i>Llamar: 984 452 5333</a></div>
</div>

<h3 class="mt-4">O envíenos los datos de su proyecto</h3>
<form class="contact-form my-3" action="https://formsubmit.co/constructionrecrea@gmail.com" method="POST">
  <input type="hidden" name="_subject" value="[Construcción de casas {City}] Nueva solicitud">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_next" value="{url}">
  <input type="hidden" name="_autoresponse" value="Gracias por contactarnos. Te responderemos en menos de 24 horas. — Equipo Recrea Construction | +52 984 452 5333">
  <input type="text" name="_honey" style="display:none">
  <div class="row g-3">
    <div class="col-md-6"><input type="text" class="form-control" name="name" placeholder="Nombre" required></div>
    <div class="col-md-6"><input type="tel" class="form-control" name="phone" placeholder="Teléfono / WhatsApp" required></div>
    <div class="col-12"><textarea class="form-control" name="message" rows="3" placeholder="Metros cuadrados, zona del terreno y presupuesto aproximado..."></textarea></div>
    <div class="col-12 text-center"><button type="submit" class="btn btn-cta btn-lg"><i class="bi bi-send me-2"></i>Enviar Solicitud</button></div>
  </div>
</form>

<h2 class="mt-5">Preguntas Frecuentes</h2>
<div class="accordion my-4" id="faqAcc">
{faq_html}
</div>

<div class="cta-section rounded p-5 text-center my-5">
  <h3 class="text-white mb-3">Presupuesto gratis para su casa en {City}</h3>
  <p class="text-white-50 mb-4">196+ proyectos terminados. Contrato a precio fijo. Respuesta en 2 minutos.</p>
  <a href="{WA}?text=Hola!%20Quiero%20un%20presupuesto%20para%20construir%20una%20casa" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Cotizar por WhatsApp</a>
</div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-patch-check"></i>Garantía 1 año por escrito</span><span class="trust-badge"><i class="bi bi-award"></i>18+ Años</span><span class="trust-badge"><i class="bi bi-building"></i>196+ Proyectos</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Licencia y DRO</span><span class="trust-badge"><i class="bi bi-file-earmark-check"></i>Asegurados</span></div>
</div></div></div></section>
<footer class="footer"><div class="container"><div class="row g-4"><div class="col-lg-4"><h5>Recrea Construcción</h5><p>Constructora integral en Playa del Carmen. Casas, villas, obra comercial y remodelación en la Riviera Maya desde 2008.</p><a href="{WA}" target="_blank" rel="noopener" class="btn btn-success btn-sm"><i class="bi bi-whatsapp me-1"></i>WhatsApp 984 452 5333</a></div><div class="col-6 col-lg-2"><h5>Construcción de casas</h5><ul class="list-unstyled"><li><a href="/construccion-de-casas-playa-del-carmen/">Playa del Carmen</a></li><li><a href="/construccion-de-casas-cancun/">Cancún</a></li><li><a href="/construccion-de-casas-tulum/">Tulum</a></li><li><a href="/construccion-de-casas-riviera-maya/">Riviera Maya</a></li><li><a href="/villas-de-lujo-playa-del-carmen/">Villas de Lujo</a></li><li><a href="/remodelacion-casas-playa-del-carmen/">Remodelación</a></li><li><a href="/services/servicios.html">Todos los servicios</a></li></ul></div><div class="col-6 col-lg-2"><h5>Ciudades</h5><ul class="list-unstyled"><li><a href="/">Playa del Carmen</a></li><li><a href="/constructora-tulum/">Tulum</a></li><li><a href="/constructora-cancun/">Cancún</a></li><li><a href="/constructora-puerto-aventuras/">Puerto Aventuras</a></li><li><a href="/constructora-akumal/">Akumal</a></li><li><a href="/constructora-puerto-morelos/">Puerto Morelos</a></li><li><a href="/constructora-riviera-maya/">Riviera Maya</a></li></ul></div><div class="col-6 col-lg-2"><h5>Guías</h5><ul class="list-unstyled"><li><a href="/cuanto-cuesta-construir-casa-playa-del-carmen/">¿Cuánto cuesta construir?</a></li><li><a href="/calculadora/">Calculadora de costos</a></li><li><a href="/mapa-precios/">Mapa de precios</a></li><li><a href="/blog-es/">Blog</a></li></ul></div><div class="col-6 col-lg-2"><h5>Empresa</h5><ul class="list-unstyled"><li><a href="/empresas-de-construccion-playa-del-carmen/">Constructora PDC</a></li><li><a href="/certificaciones/">Certificaciones</a></li><li><a href="/#contact">Contacto</a></li></ul></div></div><hr class="mt-4 mb-3" style="border-color:rgba(255,255,255,.15)"><div class="footer-bottom text-center"><p class="mb-0">&copy; 2008–2026 Recrea Construcción. · <a href="/">Inicio</a> · <a href="/blog-es/">Blog</a> · <a href="/services/servicios.html">Servicios</a></p></div></div></footer>
<a href="mailto:constructionrecrea@gmail.com" class="email-float" aria-label="Email"><i class="bi bi-envelope-fill"></i></a>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>window.addEventListener('scroll',function(){{document.getElementById('mainNav').classList.toggle('scrolled',window.scrollY>50)}});</script>
<div class="wa-widget" id="waWidget"><div class="wa-chat-box" id="waChatBox"><div class="wa-chat-header"><div class="wa-avatar"><i class="bi bi-headset"></i></div><div><div class="wa-chat-name">Recrea</div><div class="wa-chat-status"><span class="wa-online-dot"></span> Online</div></div><button class="wa-close" id="waClose" aria-label="Close"><i class="bi bi-x-lg"></i></button></div><div class="wa-chat-body"><div class="wa-message"><span>¡Hola! ¿En qué podemos ayudarle?</span></div></div><div class="wa-quick-btns"><a href="{WA}?text=Hola!%20Cotización" target="_blank" rel="noopener" class="wa-quick-btn wa-quick-btn-main"><i class="bi bi-whatsapp me-1"></i>Cotizar</a></div></div><button class="whatsapp-float" id="waToggle" aria-label="WhatsApp"><i class="bi bi-whatsapp" id="waIcon"></i></button></div>
<script>(function(){{var t=document.getElementById('waToggle'),b=document.getElementById('waChatBox'),c=document.getElementById('waClose'),i=document.getElementById('waIcon');if(!t||!b)return;var open=false;t.addEventListener('click',function(e){{e.preventDefault();e.stopPropagation();open=!open;b.classList.toggle('open',open);if(i)i.className=open?'bi bi-x-lg':'bi bi-whatsapp';}});if(c)c.addEventListener('click',function(e){{e.stopPropagation();open=false;b.classList.remove('open');if(i)i.className='bi bi-whatsapp';}});document.addEventListener('click',function(e){{if(open&&!e.target.closest('#waWidget')){{open=false;b.classList.remove('open');if(i)i.className='bi bi-whatsapp';}}}});}})();</script>
</body></html>"""


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for slug, d in CITIES.items():
        dirname = 'construccion-de-casas-' + slug
        os.makedirs(dirname, exist_ok=True)
        html = build(slug, d)
        open(os.path.join(dirname, 'index.html'), 'w', encoding='utf-8').write(html)
        print('%-42s %6d bytes' % (dirname + '/', len(html)))
