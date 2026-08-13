#!/usr/bin/env python3
"""Pages for keyword gaps found in Semrush (MX database), 2026-08-12.

Picked by volume + difficulty + relevance, and each one verified as NOT already
targeted anywhere on the site (checked title and body coverage first):

  pozo de absorción        2,900/mo  KD 16  CPC $0.74  — zero mentions on the site
  presupuesto de obra      1,000/mo  KD 17  (+ "ejemplo" 390, "cómo hacer" 320)
  cuánto cuesta una alberca  320/mo  KD 24  (+ "hacer una alberca" 720)
  proyecto arquitectónico    880/mo  KD 13  — mentioned in passing, never targeted

Spanish only on purpose: these are Mexican-market informational queries with
commercial pull; the English equivalents are different searches with different
demand, so they are not machine-translated here.

The absorption-well page is written the honest way for this region: in karst with
cenotes and a reef aquifer, an absorption well is often exactly what you must NOT
build, and the page says so before it says anything else.
"""
import os, re, json

BASE = 'https://construction-recrea.com'
TPL = 'cimentacion-y-losas-playa-del-carmen/index.html'   # chrome donor (ES landing)

PAGES = {
'presupuesto-de-obra': dict(
  title='Presupuesto de Obra: Cómo se Hace y Qué Incluye | Recrea',
  desc='Cómo se hace un presupuesto de obra por partidas: qué debe incluir, ejemplo de una casa de 150 m² y cómo comparar dos presupuestos sin equivocarse.',
  h1='Presupuesto de Obra: Cómo se Hace y Qué Debe Incluir',
  lead='Un presupuesto de obra serio no es un número: es una lista de partidas con cantidades, precios unitarios y alcance. Así se arma, así se lee, y así se detecta el que está incompleto a propósito.',
  secs=[
   ('Qué es un presupuesto de obra por partidas',
    'Es el desglose del costo de una construcción en conceptos medibles: preliminares, cimentación, estructura, albañilería, instalaciones, acabados, exteriores y limpieza. Cada partida lleva unidad (m², m³, pieza, lote), cantidad, precio unitario e importe. Sin cantidades y precios unitarios no es un presupuesto: es una cotización global, y una cotización global es imposible de comparar y muy fácil de ajustar a la mitad de la obra.'),
   ('Qué debe incluir siempre',
    'Preliminares y trazo; excavación y cimentación; estructura de concreto; muros y losas; instalación hidrosanitaria, eléctrica y de gas; impermeabilización; aplanados, pisos y pintura; carpintería y herrería; cancelería; muebles de baño y cocina; cisterna, bombeo y tinaco; limpieza final y pruebas. Además: indirectos, supervisión, utilidad y el IVA claramente indicados. Si el documento no separa costo directo, indirectos y utilidad, no permite comparar nada.'),
   ('Ejemplo: estructura de un presupuesto de casa de 150 m²',
    'Con el rango de obra de la Riviera Maya en 2026, una casa de 150 m² de nivel medio se reparte aproximadamente así. Los porcentajes varían con el diseño, pero sirven para detectar un presupuesto desequilibrado a simple vista.'),
   ('Errores que inflan el costo (o lo esconden)',
    'Cantidades “por lote” en partidas que se miden por m². Acabados descritos como “de primera calidad” sin marca ni modelo. Instalaciones sin especificar calibre, diámetro ni capacidad. Alberca, paisajismo o barda incluidas en la descripción pero no en el importe. Y el clásico: presupuesto sin proyecto ejecutivo, que siempre termina en obra extra, porque nadie puede cuantificar lo que todavía no está dibujado.'),
   ('Cómo comparar dos presupuestos sin equivocarse',
    'Póngalos lado a lado por partida, no por total. Revise que ambos incluyan las mismas partidas y las mismas cantidades; casi siempre el más barato es el que omitió tres. Compare precios unitarios, no importes. Pregunte qué pasa si cambia el precio del acero o del cemento durante la obra. Y confirme quién paga los trámites, las pruebas y la limpieza: son partidas reales que a menudo desaparecen del papel.'),
  ],
  table=('Partida','% del costo de obra','Notas',
   [('Preliminares y cimentación','12–18%','Depende de la mecánica de suelos: en roca caliza puede subir'),
    ('Estructura y albañilería','25–32%','Concreto, acero, muros, losas'),
    ('Instalaciones (hidro, eléctrica, A/A)','14–18%','Incluye cisterna, bombeo y preparaciones'),
    ('Acabados','22–30%','La partida que más varía por nivel: económico a premium'),
    ('Carpintería, herrería y cancelería','8–12%','Cocina, closets, puertas, ventanas'),
    ('Exteriores y limpieza','4–8%','Andadores, jardín, entrega')]),
  faq=[('¿Cuánto cuesta hacer un presupuesto de obra?','Cuando ya existe proyecto ejecutivo, el presupuesto por partidas forma parte del servicio y no se cobra aparte. Sin proyecto, cualquier número es una estimación por m², útil para decidir si el proyecto cabe en su bolsillo, pero no para contratar.'),
       ('¿Presupuesto cerrado o por administración?','Cerrado por partidas si quiere previsibilidad: el riesgo de rendimiento lo asume el constructor. Por administración solo tiene sentido si usted va a supervisar de cerca y aceptar la variación. Nosotros trabajamos a precio fijo por partidas.'),
       ('¿Por qué dos presupuestos de la misma casa difieren 40%?','Casi nunca por el margen: por el alcance. Uno incluye instalaciones completas, acabados especificados y trámites; el otro los deja fuera o los describe sin cuantificar. Comparados partida por partida, la diferencia real suele ser mucho menor.'),
       ('¿El presupuesto incluye el terreno?','No. El presupuesto de obra cubre la construcción. Terreno, escrituras, notario e impuestos van aparte, igual que el mobiliario.')],
  links=[('/construccion-de-casas-riviera-maya/','Construcción de casas en la Riviera Maya'),
         ('/calculadora/','Calculadora de costos'),
         ('/topografia-y-planos-riviera-maya/','Topografía y proyecto ejecutivo'),
         ('/permisos-licencias-construccion-riviera-maya/','Permisos, licencias y DRO')]),

'pozo-de-absorcion': dict(
  title='Pozo de Absorción: Cuándo Sí, Cuándo No y Qué Usar | Recrea',
  desc='Pozo de absorción en suelo kárstico: cuándo está permitido, por qué en la Riviera Maya casi nunca lo está, medidas, costos y qué alternativas sí se autorizan.',
  h1='Pozo de Absorción: Cuándo Sí, Cuándo No y Qué Usar en su Lugar',
  lead='En buena parte de la Riviera Maya el pozo de absorción es justo lo que no debe construirse. Antes de dimensionar uno conviene saber por qué, y qué solución sí pasa el filtro ambiental.',
  secs=[
   ('Qué es y para qué se usa',
    'Un pozo de absorción es una excavación que infiltra en el subsuelo el agua que recibe. Para agua de lluvia captada en azoteas y patios es una solución común y aceptada en muchos municipios. El problema empieza cuando se usa para aguas residuales, que es como todavía se resuelven muchas casas viejas del sureste.'),
   ('Por qué en suelo kárstico casi nunca es la respuesta',
    'La península de Yucatán es roca caliza fracturada: el agua que se infiltra llega rápido al acuífero, y el acuífero descarga en cenotes y en el mar, sobre el arrecife. Infiltrar aguas residuales sin tratar es contaminar el agua que después bebe y usa la zona. Por eso las autoridades ambientales de la región condicionan o rechazan proyectos que descargan sin tratamiento, y por eso conviene diseñar el drenaje antes de comprar el terreno, no después.'),
   ('Qué se autoriza en su lugar',
    'Para aguas residuales: biodigestor autolimpiable en casas unifamiliares, o planta de tratamiento compacta cuando el aforo lo justifica —hotel pequeño, varias viviendas, restaurante—. El efluente ya tratado puede reutilizarse en riego o infiltrarse según lo que autorice el permiso. Para agua pluvial: pozo de absorción bien dimensionado, con trampa de sólidos y separador de grasas si recibe escurrimiento de patios.'),
   ('Medidas y criterios de dimensionamiento',
    'Un pozo pluvial se dimensiona con el área de captación, la intensidad de lluvia de diseño y la capacidad de infiltración del suelo. En la práctica regional se manejan diámetros de 1.00 a 1.50 m y profundidades que dependen del nivel del manto freático: nunca se busca alcanzarlo, sino quedarse por encima con margen. Los biodigestores se eligen por número de usuarios y aportación diaria; las plantas compactas, por metros cúbicos por día.'),
   ('Lo que revisa la autoridad',
    'Distancia a cenotes, cuerpos de agua y pozos de abasto; profundidad respecto al manto freático; tratamiento previo a cualquier infiltración; y evidencia de mantenimiento. En zonas dentro o cerca de áreas naturales protegidas —Puerto Morelos, Akumal, Tulum— el expediente ambiental es el que fija el calendario de toda la obra, no la construcción.'),
  ],
  table=('Solución','Cuándo aplica','Rango de costo 2026',
   [('Pozo de absorción pluvial','Agua de lluvia de azotea y patios','$18,000 – $45,000 MXN'),
    ('Biodigestor autolimpiable','Casa unifamiliar, 5–10 usuarios','$25,000 – $60,000 MXN'),
    ('Planta de tratamiento compacta','Hotel pequeño, varias viviendas, restaurante','$180,000 – $600,000 MXN'),
    ('Trampa de grasas y sólidos','Cocinas y áreas de servicio','$8,000 – $25,000 MXN')]),
  faq=[('¿Puedo hacer un pozo de absorción para aguas negras en Quintana Roo?','En general no es la vía correcta: el suelo kárstico conduce lo infiltrado al acuífero y de ahí a cenotes y al mar. Lo que se autoriza es tratamiento previo —biodigestor o planta compacta— y, en su caso, infiltración del efluente tratado según el permiso.'),
       ('¿Qué medidas tiene un pozo de absorción pluvial?','Se calcula, no se copia: depende del área de captación, la lluvia de diseño y la infiltración del terreno. En la región es común entre 1.00 y 1.50 m de diámetro, con profundidad limitada por el nivel del manto freático.'),
       ('¿Cuánto cuesta un biodigestor y cada cuánto se mantiene?','De $25,000 a $60,000 MXN instalado para una casa, más registro de lodos. El mantenimiento es una purga periódica —según uso, cada 12 a 24 meses— y revisión anual; sin eso el equipo deja de cumplir y el permiso queda en falta.'),
       ('¿Esto afecta el permiso de construcción?','Sí. La solución de aguas forma parte del proyecto que se presenta. En municipios con área natural protegida cerca, es de las primeras cosas que revisan y de las que más retrasan un expediente mal armado.')],
  links=[('/plomeria-instalaciones-hidraulicas-playa-del-carmen/','Plomería e instalaciones hidráulicas'),
         ('/construccion-de-casas-riviera-maya/','Construcción de casas en la Riviera Maya'),
         ('/permisos-licencias-construccion-riviera-maya/','Permisos, licencias y DRO'),
         ('/construccion-de-casas-ruta-de-los-cenotes/','Construir en la Ruta de los Cenotes')]),

'cuanto-cuesta-una-alberca': dict(
  title='Cuánto Cuesta una Alberca en 2026: Precios Reales | Recrea',
  desc='Cuánto cuesta hacer una alberca en la Riviera Maya en 2026: precio por tamaño y tipo, qué incluye, equipo, acabados, y cuánto cuesta mantenerla al mes.',
  h1='Cuánto Cuesta Hacer una Alberca (Precios 2026)',
  lead='El precio de una alberca no depende del largo por ancho, sino de la estructura, el equipo y el acabado. Estos son los rangos reales con los que trabajamos en la Riviera Maya y lo que cambia cada número.',
  secs=[
   ('Qué determina el precio',
    'Tres cosas: el sistema constructivo (concreto armado proyectado o colado, o prefabricada), el equipo (bomba, filtro, sistema de sanitización, calefacción) y el acabado (azulejo, pasta, piedra o chukum). A eso se suma lo que casi nadie cotiza al inicio: excavación en roca, instalación hidráulica, iluminación, y la obra civil de andadores y bordes.'),
   ('Precios por tamaño y tipo',
    'Rangos de obra terminada, sin paisajismo, para la Riviera Maya en 2026. La excavación en roca caliza es la variable que más mueve el extremo bajo.'),
   ('Qué incluye y qué no',
    'Incluye: excavación, estructura, impermeabilización, instalación hidráulica, equipo de filtrado, acabado interior y puesta en marcha. No suele incluir: calentador o bomba de calor, sistema de sal, iluminación arquitectónica, cubierta, cascadas o fuentes, deck y paisajismo. Conviene pedir el desglose por partidas, igual que en la casa.'),
   ('Mantenimiento: el costo que se olvida',
    'Una alberca residencial en clima tropical consume producto químico, energía de bombeo y horas de limpieza todo el año. En la práctica, entre $1,500 y $4,000 MXN al mes para una alberca familiar con mantenimiento contratado, más el consumo eléctrico. El sistema de sal reduce químicos pero exige más cuidado del equipo por la salinidad.'),
   ('Permisos y detalles que sí importan',
    'Dentro de un fraccionamiento, el comité de diseño suele revisar ubicación, retiros y desagüe. El vaciado no puede descargarse a la calle ni al terreno del vecino: se prevé un punto de descarga. Y si la alberca es parte de una casa nueva, entra en el proyecto y en la licencia de construcción, no como obra aparte.'),
  ],
  table=('Tipo de alberca','Medida típica','Costo de obra 2026',
   [('Alberca compacta / plunge pool','3×2 a 4×2 m','$180,000 – $350,000 MXN'),
    ('Alberca familiar','6×3 a 8×4 m','$380,000 – $750,000 MXN'),
    ('Alberca con desbordante','8×4 m con espejo','$700,000 – $1,300,000 MXN'),
    ('Alberca de villa / diseño','10×5 m y mayores','$1,200,000 MXN en adelante')]),
  faq=[('¿Cuánto cuesta hacer una alberca de 8x4?','Entre $380,000 y $750,000 MXN de obra terminada según estructura, equipo y acabado. Con desbordante o acabado en chukum el rango sube; con acabado en pasta y equipo básico baja.'),
       ('¿Cuánto tarda construir una alberca?','De 4 a 8 semanas para una alberca familiar, si la excavación no encuentra roca dura ni cavidades. Cuando la alberca es parte de una casa nueva, se integra al calendario de obra y no suma tiempo al final.'),
       ('¿Sale más barata una alberca prefabricada?','En equipo y tiempo sí; en obra civil no tanto, porque igual hay excavación, base, instalación y bordes. En terreno rocoso la diferencia se reduce bastante.'),
       ('¿Cuánto cuesta mantener una alberca al mes?','Entre $1,500 y $4,000 MXN de servicio y químicos para una alberca familiar, más electricidad. La cifra depende del uso, de si está a la sombra y del sistema de sanitización.')],
  links=[('/albercas-de-lujo-playa-del-carmen/','Albercas de lujo en Playa del Carmen'),
         ('/construccion-albercas/','Construcción de albercas'),
         ('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'),
         ('/calculadora/','Calculadora de costos')]),

'proyecto-arquitectonico': dict(
  title='Proyecto Arquitectónico: Qué Incluye y Cuánto Cuesta | Recrea',
  desc='Qué incluye un proyecto arquitectónico y ejecutivo: fases, planos, memorias, entregables y precios 2026 en la Riviera Maya. Qué pasa si construye sin él.',
  h1='Proyecto Arquitectónico: Qué Incluye, Fases y Precio',
  lead='El proyecto no es “los planos”. Es el documento con el que se pide la licencia, se cotiza la obra por partidas y se controla al constructor. Sin él, todo presupuesto es una estimación y toda obra extra es discutible.',
  secs=[
   ('Las fases, en orden',
    'Programa y análisis del terreno; anteproyecto (distribución, volumetría, imagen); proyecto arquitectónico (plantas, cortes, fachadas, detalles); proyecto ejecutivo (estructural, hidrosanitario, eléctrico, especiales); y documentación para trámite, firmada por DRO. Saltarse el ejecutivo es la causa más común de sobrecostos: lo que no está dibujado se resuelve en obra, y en obra siempre es más caro.'),
   ('Qué entregables debe recibir',
    'Planos arquitectónicos acotados; memoria y planos estructurales; isométricos y diagramas de instalaciones; cuadro de acabados; carpintería y herrería detalladas; y el juego firmado para licencia. En digital editable y en PDF. Si al final del proyecto usted no tiene un juego con el que otro constructor podría cotizar, no le entregaron un proyecto ejecutivo.'),
   ('Cuánto cuesta',
    'En la Riviera Maya, el proyecto completo suele ubicarse entre el 4% y el 8% del costo de obra, según complejidad y nivel de detalle. Cuando la misma empresa diseña y construye, ese porcentaje suele integrarse al contrato. Cobrar barato el proyecto y caro la obra extra es un modelo de negocio; conviene saber cuál está contratando.'),
   ('Proyecto y permiso: cómo se conectan',
    'La licencia municipal se solicita con el proyecto firmado por un DRO registrado. En municipios con requisito ambiental —Tulum, Puerto Morelos, zonas costeras— el proyecto también alimenta el expediente de la autoridad ambiental. Un proyecto bien armado acorta el trámite; uno incompleto lo devuelve una y otra vez.'),
   ('Diseñar para este clima, no para el catálogo',
    'Orientación y ventilación cruzada, protección solar en fachadas poniente, cubiertas y detalles pensados para lluvia intensa, materiales que resisten salinidad, y previsión de cisterna, bombeo y tratamiento. Un plano bonito que ignora esto se convierte en una casa cara de operar.'),
  ],
  table=('Fase','Qué entrega','% del costo de obra',
   [('Anteproyecto','Distribución, volumetría, presupuesto preliminar','0.5–1%'),
    ('Proyecto arquitectónico','Plantas, cortes, fachadas, detalles','1.5–3%'),
    ('Proyecto ejecutivo','Estructural, instalaciones, cuadro de acabados','2–4%'),
    ('Documentación y DRO','Juego firmado para licencia','Según municipio')]),
  faq=[('¿Puedo construir sin proyecto ejecutivo?','Legalmente necesita proyecto firmado por DRO para la licencia. En la práctica, además, sin ejecutivo nadie puede cotizar por partidas ni controlar la obra: cada decisión no dibujada se toma en el sitio y se cobra como extra.'),
       ('¿Cuánto cuesta un proyecto arquitectónico completo?','Entre 4% y 8% del costo de obra según complejidad. Para una casa de 150 m² de nivel medio en la Riviera Maya eso significa un rango orientativo de $120,000 a $300,000 MXN, integrable al contrato si diseñamos y construimos.'),
       ('¿Puedo llevar mis propios planos?','Sí. Los revisamos, verificamos que cumplan la normativa municipal y el reglamento del fraccionamiento, completamos lo que falte para el ejecutivo y cotizamos la obra por partidas.'),
       ('¿Cuánto tarda?','De 6 a 10 semanas para casa unifamiliar, desde el anteproyecto hasta el juego firmado. El trámite de licencia corre en paralelo cuando el expediente lo permite.')],
  links=[('/topografia-y-planos-riviera-maya/','Topografía y planos'),
         ('/arquitectos-playa-del-carmen/','Arquitectos en Playa del Carmen'),
         ('/permisos-licencias-construccion-riviera-maya/','Permisos, licencias y DRO'),
         ('/construccion-de-casas-riviera-maya/','Construcción de casas en la Riviera Maya')]),
}


def build(slug, d, src):
    url = '%s/%s/' % (BASE, slug)
    head_end = src.index('</head>')
    assets = '\n'.join(l for l in src[:head_end].split('\n')
                       if ('cdn.jsdelivr' in l or 'fonts.g' in l or 'style.min.css' in l
                           or 'favicon' in l or 'apple-touch' in l or 'webmanifest' in l))
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d['faq']]}
    art = {"@context": "https://schema.org", "@type": "Article", "headline": d['h1'],
           "description": d['desc'], "inLanguage": "es", "datePublished": "2026-08-12",
           "author": {"@type": "Organization", "name": "Recrea Construcción", "url": BASE},
           "publisher": {"@type": "Organization", "name": "Recrea Construcción"},
           "mainEntityOfPage": url}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Inicio", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": d['h1']}]}
    head = ('<!DOCTYPE html>\n<html lang="es">\n<head>\n'
            '  <meta name="google-site-verification" content="0WwXyAoY4jeA2xgFFFB06a9HqEfzR7LnyLYVBrFTU0A" />\n'
            '  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '  <title>%s</title>\n  <meta name="description" content="%s">\n%s\n'
            '  <script type="application/ld+json">%s</script>\n'
            '  <script type="application/ld+json">%s</script>\n'
            '  <script type="application/ld+json">%s</script>\n'
            '  <link rel="canonical" href="%s">\n'
            '  <meta property="og:type" content="article">\n  <meta property="og:title" content="%s">\n'
            '  <meta property="og:description" content="%s">\n  <meta property="og:url" content="%s">\n'
            '  <meta property="og:image" content="%s/img/og-wallpaper.png">\n'
            '  <meta property="og:locale" content="es_MX">\n'
            '  <meta name="twitter:card" content="summary_large_image">\n</head>\n'
            % (d['title'], d['desc'], assets, json.dumps(art, ensure_ascii=False),
               json.dumps(faq, ensure_ascii=False), json.dumps(bc, ensure_ascii=False),
               url, d['title'], d['desc'], url, BASE))
    body_rest = src[head_end:]
    top = body_rest[body_rest.index('<body'):body_rest.index('<div style="padding-top:116px"></div>') + len('<div style="padding-top:116px"></div>')]
    bottom = body_rest[body_rest.index('<footer'):]

    th, th2, th3, rows = d['table']
    table = ('<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark">'
             '<tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>\n%s\n</tbody></table></div>'
             % (th, th2, th3, '\n'.join('<tr><td>%s</td><td>%s</td><td>%s</td></tr>' % r for r in rows)))
    secs = ''
    for i, (h, p) in enumerate(d['secs']):
        secs += '<h2 class="mt-4">%s</h2>\n<p>%s</p>\n' % (h, p)
        if i == 2:      # the table belongs right after the third section
            secs += table + '\n'
    faq_html = '\n'.join(
        '<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button%s" type="button" '
        'data-bs-toggle="collapse" data-bs-target="#kf%d">%s</button></h3>'
        '<div id="kf%d" class="accordion-collapse collapse%s" data-bs-parent="#kwFaq">'
        '<div class="accordion-body">%s</div></div></div>'
        % ('' if i == 0 else ' collapsed', i, q, i, ' show' if i == 0 else '', a)
        for i, (q, a) in enumerate(d['faq']))
    links = ' · '.join('<a href="%s">%s</a>' % l for l in d['links'])

    article = ('<nav class="container mt-3"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="/">Inicio</a></li>'
               '<li class="breadcrumb-item active">%s</li></ol></nav>\n'
               '<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-8">\n'
               '<h1>%s</h1>\n<p class="lead">%s</p>\n%s\n'
               '<p>Guías útiles: %s</p>\n'
               '<h2 class="mt-5">Preguntas Frecuentes</h2>\n<div class="accordion my-4" id="kwFaq">\n%s\n</div>\n'
               '<div class="cta-section rounded p-5 text-center my-5">\n'
               '<h3 class="text-white mb-3">¿Quiere un presupuesto por partidas para su proyecto?</h3>\n'
               '<p class="text-white-50 mb-4">196+ proyectos terminados. Contrato a precio fijo. Respuesta en 2 minutos.</p>\n'
               '<a href="https://wa.me/529844525333" target="_blank" rel="noopener" class="btn btn-cta btn-lg">'
               '<i class="bi bi-whatsapp me-2"></i>Cotizar por WhatsApp</a>\n</div>\n'
               '</div></div></div></section>\n' % (d['h1'], d['h1'], d['lead'], secs, links, faq_html))
    return head + top + '\n' + article + bottom


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    src = open(TPL, encoding='utf-8').read()
    for slug, d in PAGES.items():
        os.makedirs(slug, exist_ok=True)
        html = build(slug, d, src)
        open(os.path.join(slug, 'index.html'), 'w', encoding='utf-8').write(html)
        print('%-28s %6d bytes  title %d  desc %d' % (slug + '/', len(html), len(d['title']), len(d['desc'])))
