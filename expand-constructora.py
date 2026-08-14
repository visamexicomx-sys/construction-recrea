#!/usr/bin/env python3
"""Expand the thin /constructora-*/ pages, driven by the Search Console export of 2026-08-13.

What the data said:

  /empresas-de-construccion-playa-del-carmen/  204 impr, 12 clicks, pos 5.34, 1,091 words
  /constructora-cancun/                        104 impr,  0 clicks, pos 8.96,   590 words
  /constructora-tulum/                          95 impr,  0 clicks, pos 14.07,  647 words
  /constructora-riviera-maya/                   19 impr,  0 clicks, pos 10.63,  775 words
  /constructora-akumal/                         14 impr,  0 clicks, pos 6.79,   586 words
  /constructora-puerto-aventuras/               11 impr,  0 clicks, pos 12.73,  534 words

The one page that earns clicks is also the only deep one. The rest sit at 534-775
words and convert nothing. Queries "constructora en tulum" (70 impr, pos 19.5) and
"constructoras en tulum" (59 impr, pos 18.2) confirm the demand exists and we are
on page two for it.

So: three new sections of genuinely city-specific substance per page, inserted
before "Por Qué Elegir Recrea", plus two extra FAQ entries. No filler, no repeated
boilerplate between cities - each block below is written for that city only.
"""
import os, re, sys

SECTIONS = {
'constructora-tulum': [
 ('Cuánto tarda una obra en Tulum, con trámites incluidos',
  'El calendario real de Tulum no lo marca la construcción: lo marca el expediente. Entre uso de suelo, licencia '
  'municipal y el componente ambiental, un proyecto residencial normal ocupa varias semanas antes de que llegue la '
  'primera máquina, y en predios cercanos a cenotes o dentro de zonas con protección el plazo se alarga. La obra en '
  'sí, para una casa de 150 a 200 m², corre entre 7 y 11 meses. Cuando alguien promete licencia en dos semanas, '
  'normalmente está describiendo un trámite que después se cae.'),
 ('El suelo de Tulum y lo que le hace al presupuesto',
  'Roca caliza fracturada, cavidades y manto freático somero. Esas tres palabras explican por qué dos terrenos '
  'vecinos pueden tener cimentaciones de costo muy distinto. Un estudio de mecánica de suelos aquí no es papeleo: '
  'es lo que evita descubrir una oquedad con la estructura ya montada. Y el manejo de aguas —biodigestor o planta '
  'compacta, nunca infiltración sin tratar— entra en el proyecto desde el primer plano, porque es de lo primero '
  'que revisa la autoridad.'),
 ('Qué preguntar a cualquier constructora en Tulum',
  'Pida el registro del DRO que va a firmar y verifique que esté vigente en el municipio. Pida el presupuesto por '
  'partidas con cantidades y precios unitarios, no un número global. Pregunte quién paga los trámites y qué pasa si '
  'el expediente ambiental se alarga. Pida ver una obra en proceso, no solo fotos terminadas. Y confirme por escrito '
  'el mecanismo de órdenes de cambio: en Tulum, donde el trámite puede mover el calendario, ese es el punto donde '
  'los presupuestos se descontrolan.'),
],
'constructora-cancun': [
 ('Construir en Cancún: zona hotelera, Cumbres y la salida a Mérida',
  'Cancún no es un solo mercado. En la zona hotelera y Puerto Cancún manda la normativa del desarrollo y el horario '
  'de maniobras; en Cumbres y las zonas nuevas del poniente manda el tránsito pesado y el acceso; y en las colonias '
  'consolidadas el reto suele ser construir entre medianeras con vecinos a un metro. Cada uno cambia el plan de obra, '
  'la logística de material y hasta la hora a la que se puede colar.'),
 ('Reglamento del fraccionamiento contra reglamento municipal',
  'En Cancún, la restricción que detiene un proyecto rara vez es la municipal: es la del fraccionamiento. Retiros '
  'mayores, altura menor, paleta de materiales obligatoria, horarios de obra, depósito de garantía y plazos máximos '
  'de construcción. Se revisan antes de diseñar, porque rediseñar después de la aprobación municipal cuesta '
  'honorarios y semanas. Nosotros pedimos el reglamento interno junto con la constancia de uso de suelo, siempre.'),
 ('Qué distingue a una constructora seria en Cancún',
  'Que le entregue presupuesto por partidas con precios unitarios; que el DRO exista y visite la obra; que tenga '
  'seguro de responsabilidad civil vigente; que le muestre una obra en proceso; y que ponga por escrito el '
  'procedimiento de cambios. En un mercado del tamaño de Cancún hay de todo, y la diferencia entre una empresa '
  'formal y un contratista improvisado no se ve en el precio inicial: se ve en el mes seis.'),
],
'constructora-puerto-aventuras': [
 ('Obra dentro de un fraccionamiento cerrado',
  'Puerto Aventuras funciona con reglamento propio: acceso controlado, registro de personal y vehículos, horarios de '
  'obra acotados, control de ruido y de escombro, y comité que revisa el proyecto antes que el municipio. Eso no es '
  'un obstáculo si se planifica —de hecho protege el valor de su propiedad—, pero obliga a una logística distinta: '
  'entregas programadas, cuadrilla registrada y una obra limpia todos los días, no solo el día de la visita.'),
 ('Marina, humedad y salinidad: lo que cambia en la especificación',
  'Cerca de la marina y del mar, la sal se lleva primero los herrajes, después la carpintería exterior y al final la '
  'instalación eléctrica mal protegida. Aquí se especifica herraje inoxidable en lugar de galvanizado corriente, '
  'maderas duras o composite en exteriores, aluminio con acabado anodizado de calidad y protección real en tableros '
  'y luminarias. Cuesta más en la lista de materiales y cuesta mucho menos en el año cinco.'),
 ('Presupuesto: qué debe traer y qué suele faltar',
  'Un presupuesto correcto para Puerto Aventuras incluye el costo de cumplir el reglamento del fraccionamiento: '
  'horarios reducidos, limpieza continua, protección de áreas comunes y, en su caso, depósito. También el manejo de '
  'aguas y la conexión de servicios según lo que autorice el desarrollo. Cuando esas partidas no aparecen, no es que '
  'sean gratis: es que van a aparecer después, en forma de obra extra.'),
],
'constructora-akumal': [
 ('Construir junto a la bahía: lo que la autoridad revisa primero',
  'Akumal está en el municipio de Tulum y convive con una bahía de valor ambiental alto y con sistemas de cenotes '
  'tierra adentro. Antes que el diseño, la autoridad mira el manejo del agua: qué pasa con el escurrimiento pluvial, '
  'cómo se tratan las aguas residuales y a qué distancia queda todo eso de un cuerpo de agua. Un proyecto que resuelve '
  'esto desde el anteproyecto avanza; uno que lo deja para el final se devuelve.'),
 ('Casa de playa o villa de renta: dos presupuestos distintos',
  'Una casa para vivir y una villa para renta vacacional no se construyen igual, aunque midan lo mismo. La villa exige '
  'más baños, instalaciones sobredimensionadas para uso intensivo, acabados que resistan rotación de huéspedes, alberca '
  'con equipo de mayor capacidad y previsión de mantenimiento frecuente. Vale la pena decidirlo antes del proyecto '
  'ejecutivo: cambiarlo después es rehacer instalaciones ya ahogadas.'),
 ('Distancia, cuadrilla y por qué eso importa en Akumal',
  'Akumal no tiene la infraestructura de proveedores de Playa del Carmen o Tulum centro. Traemos cuadrilla propia y '
  'programamos el material por etapas en lugar de depender de compras locales de última hora. Es la diferencia entre '
  'una obra que avanza todas las semanas y una que se detiene tres días porque faltó un camión de material que aquí '
  'nadie tiene en existencia.'),
],
'constructora-puerto-morelos': [
 ('Un municipio joven con un parque nacional enfrente',
  'Puerto Morelos se volvió municipio hace poco y su arrecife es área natural protegida. Ambas cosas se notan en el '
  'trámite: conviene confirmar cada requisito caso por caso en lugar de asumir que funciona igual que en Benito Juárez, '
  'y el manejo de escurrimientos y de aguas residuales se revisa con criterio ambiental. Quien ya trabajó aquí lo sabe; '
  'quien llega de otro municipio suele perder semanas descubriéndolo.'),
 ('La ruta de los cenotes: construir sobre agua subterránea',
  'Tierra adentro, la ruta de los cenotes es de los entornos más delicados de la región. El agua subterránea corre a '
  'poca profundidad y cualquier infiltración sin tratar llega directo al sistema. Aquí el proyecto de instalaciones pesa '
  'tanto como el arquitectónico: tratamiento de aguas, contención, manejo pluvial y una cimentación diseñada con '
  'estudio de suelos y no por analogía con el terreno de al lado.'),
 ('Qué esperar de una obra en Puerto Morelos',
  'Plazos de trámite que dependen del componente ambiental; una obra que avanza bien porque estamos a media hora de '
  'Cancún y a cuarenta minutos de Playa del Carmen; y una especificación pensada para primera línea de costa cuando el '
  'predio lo está. Presupuesto por partidas, precio fijo y reporte fotográfico semanal, que es como trabajamos también '
  'con clientes que no viven en México.'),
],
'constructora-riviera-maya': [
 ('Dónde trabajamos y por qué no vamos más lejos',
  'Cubrimos el corredor de Cancún a Tulum, más Cozumel e Isla Mujeres: Puerto Morelos, Playa del Carmen, Puerto '
  'Aventuras, Akumal y las zonas intermedias. Fuera de ese corredor decimos que no. Una cuadrilla estirada a tres horas '
  'de la base no supervisa igual, y en construcción la supervisión es la mitad del resultado. Preferimos rechazar una '
  'obra antes que entregarla mal.'),
 ('Lo que comparte toda la Riviera Maya y lo que cambia por municipio',
  'Comparten el suelo —caliza fracturada, cavidades, manto freático somero—, el clima —sal, humedad, lluvia intensa, '
  'temporada de huracanes— y la necesidad de tratar aguas en lugar de infiltrarlas. Cambian los trámites: impacto vial '
  'y reglamentos de fraccionamiento en Cancún y Playa del Carmen; expediente ambiental exigente en Tulum, Akumal y '
  'Puerto Morelos; logística marítima y costos de flete en Cozumel e Isla Mujeres.'),
 ('Cómo trabajamos con clientes que viven fuera de México',
  'Buena parte de nuestros clientes están en Estados Unidos, Canadá o Europa y ven la obra por reporte. Lo que hace que '
  'funcione: contrato a precio fijo por partidas, calendario ligado a hitos verificables, reporte semanal con fotos '
  'fechadas, videollamada en los momentos críticos —armados antes de colar, instalaciones antes de tapar— y aprobación '
  'por escrito de cada cambio. Nada de acuerdos verbales en sitio.'),
],
}

FAQ = {
'constructora-tulum': [
 ('¿Cuánto cuesta construir en Tulum por metro cuadrado?',
  'En 2026 el rango de obra en Tulum va aproximadamente de $18,000 a $32,000 MXN por m² según nivel de acabado, y sube '
  'en villas de diseño. La cimentación puede mover ese número más que los acabados si el terreno tiene cavidades.'),
 ('¿Cuánto tarda el permiso de construcción en Tulum?',
  'Varias semanas, y depende del componente ambiental más que del municipal. Los predios cerca de cenotes o dentro de '
  'zonas con protección requieren un expediente más completo y ese expediente fija el calendario de toda la obra.')],
'constructora-cancun': [
 ('¿Cuánto cuesta construir una casa en Cancún?',
  'El rango de obra en 2026 va aproximadamente de $17,000 a $30,000 MXN por m² según acabados, más terreno, proyecto y '
  'trámites. En zonas con reglamento de fraccionamiento estricto conviene presupuestar también el costo de cumplirlo.'),
 ('¿Trabajan dentro de fraccionamientos con comité de diseño?',
  'Sí, es habitual en Cancún. Presentamos el proyecto al comité, ajustamos lo que pidan antes de tramitar la licencia '
  'municipal y cumplimos horarios, accesos y control de ruido durante toda la obra.')],
'constructora-puerto-aventuras': [
 ('¿Pueden construir dentro del fraccionamiento de Puerto Aventuras?',
  'Sí. Registramos personal y vehículos, respetamos horarios y control de ruido, mantenemos la obra limpia y '
  'presentamos el proyecto al comité antes de iniciar. Es un requisito del desarrollo y forma parte de nuestro plan de obra.'),
 ('¿Qué cambia por estar cerca del mar y de la marina?',
  'La especificación: herraje inoxidable, maderas duras o composite en exteriores, aluminio anodizado de calidad y '
  'protección real en instalación eléctrica. Cuesta más en materiales y evita reponer todo en pocos años.')],
'constructora-akumal': [
 ('¿Se puede construir cerca de la bahía de Akumal?',
  'Depende del predio y de lo que autorice la autoridad ambiental, que aquí revisa con detalle el manejo de aguas y las '
  'distancias a cuerpos de agua. Es lo primero que verificamos, antes de dibujar cualquier plano.'),
 ('¿Construyen villas para renta vacacional en Akumal?',
  'Sí, y se diseñan distinto a una casa para habitar: más baños, instalaciones para uso intensivo, acabados que aguanten '
  'rotación y alberca con equipo de mayor capacidad. Conviene decidirlo antes del proyecto ejecutivo.')],
'constructora-puerto-morelos': [
 ('¿El arrecife afecta los permisos en Puerto Morelos?',
  'Afecta el manejo ambiental del proyecto: escurrimientos, tratamiento de aguas y contención se revisan con criterio de '
  'área natural protegida. No impide construir; obliga a resolverlo bien desde el proyecto.'),
 ('¿Trabajan en la ruta de los cenotes?',
  'Sí, con proyecto de instalaciones y estudio de suelos específicos para esa zona. Es el entorno donde menos sentido '
  'tiene copiar la solución del terreno vecino.')],
'constructora-riviera-maya': [
 ('¿En qué ciudades de la Riviera Maya trabajan?',
  'Cancún, Puerto Morelos, Playa del Carmen, Puerto Aventuras, Akumal, Tulum, Cozumel e Isla Mujeres. Fuera de ese '
  'corredor evaluamos caso por caso, y normalmente decimos que no.'),
 ('¿Pueden gestionar la obra si vivo en otro país?',
  'Sí, es como trabajamos con buena parte de nuestros clientes: precio fijo por partidas, reporte semanal con fotos '
  'fechadas, videollamada en los hitos críticos y aprobación por escrito de cualquier cambio.')],
}


def insert(slug):
    f = os.path.join(slug, 'index.html')
    s = open(f, encoding='utf-8').read()
    if 'data-expanded="gsc"' in s:
        s = re.sub(r'<div data-expanded="gsc">.*?</div><!--/gsc-->', '', s, flags=re.S)

    body = ''.join('<h2 class="mt-4">%s</h2>\n<p>%s</p>\n' % (h, p) for h, p in SECTIONS[slug])
    block = '<div data-expanded="gsc">\n%s</div><!--/gsc-->\n' % body

    # insert before the "Por Qué Elegir Recrea" heading, which every one of these pages has
    m = re.search(r'<h2[^>]*>\s*Por Qu[eé] Elegir', s)
    if not m:
        m = re.search(r'<h2[^>]*>\s*Proyectos Reales', s)
    if not m:
        print('  %s: no anchor heading found, skipped' % slug); return 0
    # climb to the start of the enclosing tag line so we do not land inside a heading
    at = s.rfind('\n', 0, m.start()) + 1
    s = s[:at] + block + s[at:]

    # two more FAQ entries, in the same accordion markup the page already uses
    add = FAQ[slug]
    last = s.rfind('</div></div></div>', 0, s.rfind('</div>\n'))
    acc = re.search(r'id="(faq[^"]*|accordion[^"]*)"', s)
    parent = acc.group(1) if acc else ''
    items = ''
    n0 = s.count('accordion-item')
    for i, (q, a) in enumerate(add):
        idx = n0 + i + 1
        items += ('<div class="accordion-item"><h3 class="accordion-header">'
                  '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" '
                  'data-bs-target="#gscq%d">%s</button></h3>'
                  '<div id="gscq%d" class="accordion-collapse collapse"%s>'
                  '<div class="accordion-body">%s</div></div></div>\n'
                  % (idx, q, idx, (' data-bs-parent="#%s"' % parent) if parent else '', a))
    mfaq = list(re.finditer(r'</div></div></div>', s))
    if mfaq and items:
        pos = None
        for mm in mfaq:
            if 'accordion' in s[max(0, mm.start() - 3000):mm.start()]:
                pos = mm.end()
        if pos:
            s = s[:pos] + '\n' + items + s[pos:]
    open(f, 'w', encoding='utf-8').write(s)
    words = len(re.sub(r'<[^>]+>', ' ', s[s.index('<h1'):s.index('<footer')]).split())
    return words


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for slug in SECTIONS:
        if not os.path.isdir(slug):
            print('  missing:', slug); continue
        print('%-34s -> %d words' % (slug, insert(slug)))
