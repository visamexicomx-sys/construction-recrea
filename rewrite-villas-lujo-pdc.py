#!/usr/bin/env python3
"""Upgrade the six Playa del Carmen city-level luxury-villa pages to the same hub
standard as the Cancún cluster built alongside them.

They already existed in all six languages but were uneven — 135 words in Chinese,
622 in German — and none of them mapped the distinct luxury sub-markets around
Playa del Carmen or linked down to the zone pages. Chrome, hreflang and schema
identity are left untouched; the head title/description, the FAQPage JSON-LD and
the whole main <section> are rewritten.
"""
import os, re, sys, json

BASE = os.path.dirname(os.path.abspath(__file__))
DIRS = {
    "es": "villas-de-lujo-playa-del-carmen",
    "en": "luxury-villa-construction-playa-del-carmen",
    "de": "luxusvilla-bau-playa-del-carmen",
    "ru": "stroitelstvo-vill-playa-del-carmen",
    "fr": "construction-villa-luxe-playa-del-carmen",
    "zh": "haohua-bieshu-playa-del-carmen",
}
P = {}   # lang -> {"title","desc","keywords","body","faq":[(q,a)]}


def rewrite(lang):
    c = P[lang]
    path = os.path.join(BASE, DIRS[lang], "index.html")
    h = open(path, encoding="utf-8").read()

    h = re.sub(r"<title>.*?</title>", "<title>" + c["title"] + "</title>", h, count=1, flags=re.S)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        h = re.sub(r"(" + re.escape(attr) + r' content=")[^"]*(")',
                   lambda m: m.group(1) + c["title"] + m.group(2), h, count=1)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        h = re.sub(r"(" + re.escape(attr) + r' content=")[^"]*(")',
                   lambda m: m.group(1) + c["desc"] + m.group(2), h, count=1)
    if c.get("keywords"):
        h = re.sub(r'(name="keywords" content=")[^"]*(")',
                   lambda m: m.group(1) + c["keywords"] + m.group(2), h, count=1)

    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": re.sub(r"<[^>]+>", "", q).replace('"', "'"),
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a).replace('"', "'")}}
        for q, a in c["faq"]]}
    h = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
               '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
               h, count=1, flags=re.S)

    start = h.index('<section class="py-5">')
    end = h.index("</section>", start) + len("</section>")
    h = h[:start] + c["body"] + h[end:]

    open(path, "w", encoding="utf-8").write(h)
    return len(re.findall(r"[^\s<>]+", re.sub(r"<[^>]+>", " ", c["body"]))), DIRS[lang]


P["es"] = {
 "title": "Villas de Lujo en Playa del Carmen 2026 | Recrea",
 "desc": "Construcción y remodelación de villas de lujo en Playa del Carmen: Playacar, Corasol, Mayakoba, Zazil-Ha y las privadas del norte. Precios 2026 y permisos.",
 "keywords": "villas de lujo playa del carmen, constructora villas playacar, casas de lujo corasol, villa llave en mano riviera maya, construir villa playa del carmen",
 "faq": [
  ("¿Cuánto cuesta construir una villa de lujo en Playa del Carmen?",
   "En 2026, de $24,000 a $45,000+ MXN/m² según la zona y los acabados. Una villa de 400 m² en Playacar o Corasol ronda los $10–16 millones MXN llave en mano; en Mayakoba sube bastante más. Contrato a precio fijo con presupuesto desglosado."),
  ("¿En qué zonas de Playa del Carmen construyen villas de lujo?",
   "Playacar Fase I y II, Corasol, Mayakoba, Zazil-Ha y Coco Beach, las privadas El Cielo, Selvamar y Playa Magna, y la franja costera al norte: Playa del Secreto y Punta Bete–Xcalacoco."),
  ("¿Qué permisos se necesitan?",
   "Uso de suelo, licencia de construcción y alineamiento del municipio de Solidaridad, con Director Responsable de Obra. En lotes con vegetación o cerca de cenotes se suma el expediente ambiental estatal, y frente al mar la zona federal marítimo terrestre. Los fraccionamientos añaden su comité de diseño."),
  ("¿Cuánto tarda la obra?",
   "Una villa de lujo toma de 10 a 16 meses de obra, más 2–4 meses de proyecto y trámites. En Playacar, Corasol y Mayakoba los horarios restringidos y los ciclos de revisión llevan el plazo al extremo alto."),
  ("¿Playacar, Corasol o Mayakoba?",
   "Playacar por caminabilidad real a la Quinta Avenida y arbolado maduro, con la contra de calles angostas y lotes prácticamente agotados. Corasol por lotes grandes y golf en un plan maestro aún en desarrollo. Mayakoba por el estándar de resort — y por el precio más alto del corredor."),
  ("¿Pueden construir a distancia?",
   "Sí. Reportes semanales con foto y video, videollamadas de avance, pagos por avance verificado y gestión completa de permisos y notaría. Así trabaja la mayoría de nuestros clientes extranjeros."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Villas de Lujo en Playa del Carmen</h1>
<p class="lead">Construimos y remodelamos <strong>villas de lujo en Playa del Carmen</strong> &mdash; de Playacar y Corasol a Mayakoba, Zazil-Ha y la franja costera al norte. Diseño, permisos, obra, alberca, domótica y mobiliario bajo un mismo techo. 18+ años y 196 proyectos, con oficina en Corasol.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Villa de lujo en Playa del Carmen 2026:</strong> $24,000&ndash;$45,000+ MXN/m² según zona y acabados. Gestionamos licencia de Solidaridad, DRO, expediente ambiental y comité del fraccionamiento.</div>

<h2>Dónde se Construyen Villas de Lujo en Playa del Carmen</h2>
<p>El lujo en Playa del Carmen no es una sola zona, sino varias, y cada una se construye distinto:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Zona</th><th>Producto</th><th>Lo que cambia en obra</th></tr></thead><tbody>
<tr><td><a href="/villas-de-lujo-playacar/">Playacar Fase I y II</a></td><td>Villas en golf y cerca de playa, mayoría por demolición o remodelación</td><td>Comité de diseño estricto, protección de arbolado, calles angostas, +25% sobre la base</td></tr>
<tr><td><a href="/villas-de-lujo-corasol/">Corasol</a></td><td>Villas grandes en golf, lotes de 250&ndash;450 m² construidos</td><td>Plan maestro en desarrollo: confirmar servicios en el límite del lote, +30%</td></tr>
<tr><td><a href="/villas-de-lujo-mayakoba/">Mayakoba</a></td><td>Residencias de estándar resort junto a lagunas y manglar</td><td>Control de diseño al nivel de los hoteles vecinos, +42% &mdash; lo más caro del corredor</td></tr>
<tr><td><a href="/construccion-de-casas-zazil-ha-coco-beach/">Zazil-Ha y Coco Beach</a></td><td>Villas cerca del mar al norte del centro</td><td>Especificación marina completa, zona federal en los lotes frente al mar</td></tr>
<tr><td><a href="/construccion-de-casas-el-cielo-playa-del-carmen/">El Cielo</a>, <a href="/construccion-de-casas-selvamar-playa-del-carmen/">Selvamar</a> y <a href="/construccion-de-casas-playa-magna/">Playa Magna</a></td><td>Privadas consolidadas con servicios y seguridad</td><td>Reglamento del fraccionamiento, trámite de Solidaridad directo, sin zona federal</td></tr>
<tr><td><a href="/construccion-de-casas-playa-del-secreto/">Playa del Secreto</a> y <a href="/construccion-de-casas-punta-bete/">Punta Bete</a></td><td>Villas frente al mar en la franja norte</td><td>ZOFEMAT, duna protegida, expediente ambiental y anidación de tortuga</td></tr>
</tbody></table></div>

<h2 class="mt-4">Todo Para su Villa</h2>
<div class="row g-3 my-2">
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-house-heart me-2" style="color:var(--accent)"></i>Villa Llave en Mano</h5><p class="small mb-0">De la mecánica de suelos a la entrega amueblada, con licencia de Solidaridad y DRO incluidos.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-hammer me-2" style="color:var(--accent)"></i>Demolición y Reconstrucción</h5><p class="small mb-0">En Playacar la mayoría de proyectos son remodelación o demolición: primero dictamen estructural, después la decisión.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-water me-2" style="color:var(--accent)"></i>Albercas y Exteriores</h5><p class="small mb-0">Alberca desbordante, chukum, roof garden y palapa, pensadas para la vista al golf, al mar o a la selva.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-tree me-2" style="color:var(--accent)"></i>Arbolado y Ambiental</h5><p class="small mb-0">Inventario de arbolado, expediente ambiental y diseño que conserva los árboles que dan sombra y valor.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-file-earmark-text me-2" style="color:var(--accent)"></i>Permisos y Comités</h5><p class="small mb-0">Licencia de Solidaridad, DRO, SEMA y ZOFEMAT donde aplica, más la autorización del fraccionamiento.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-lamp me-2" style="color:var(--accent)"></i>Interiorismo y Domótica</h5><p class="small mb-0">Cocina, carpintería a medida, iluminación, clima y seguridad, listos para habitar o para renta.</p></div></div>
</div>

<h2 class="mt-4">Precios de Villas de Lujo en Playa del Carmen (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Zona / tipo</th><th>MXN/m²</th><th>USD/m²</th></tr></thead><tbody>
<tr><td>Remodelación integral de villa existente</td><td>$14,000&ndash;$26,000</td><td>$780&ndash;$1,445</td></tr>
<tr><td>Villa nueva premium (privadas consolidadas)</td><td>$24,000&ndash;$30,000</td><td>$1,335&ndash;$1,670</td></tr>
<tr><td>Playacar / Corasol</td><td>$26,000&ndash;$38,000</td><td>$1,445&ndash;$2,110</td></tr>
<tr><td>Mayakoba y frente al mar</td><td>$35,000&ndash;$55,000+</td><td>$1,945&ndash;$3,055+</td></tr>
</tbody></table></div>
<p class="text-muted small">Incluye estructura, instalaciones y acabados. Sin terreno, alberca de proyecto, jardinería madura ni mobiliario, que se cotizan aparte. Base de referencia de Playa del Carmen: $17,000&ndash;$21,000 MXN/m² en obra estándar.</p>

<h2 class="mt-4">Lo que Debe Saber Antes de Construir</h2>
<ul>
<li><strong>Municipio de Solidaridad.</strong> Uso de suelo, licencia, alineamiento y DRO. Verifique COS, CUS, altura y remetimientos del lote antes de encargar el proyecto: son esos números los que definen si cabe la villa que imagina.</li>
<li><strong>Comités de diseño.</strong> Playacar, Corasol y Mayakoba revisan altura, volumetría, materiales, color, bardas y retiro de arbolado, con trabajadores registrados, horarios y fianza. Presente en anteproyecto: una ronda de revisión no prevista es el retraso más común.</li>
<li><strong>Arbolado maduro.</strong> En Playacar y Corasol está protegido y vale dinero: cada retiro se justifica, y un proyecto que trama entre los árboles se aprueba antes y produce una casa más fresca.</li>
<li><strong>Mecánica de suelos.</strong> Karst: excelente capacidad de carga y una cavidad dos metros al lado. Los sondeos se hacen sobre la huella real.</li>
<li><strong>Especificación marina.</strong> Inoxidable 316, aluminio anodizado o con recubrimiento marino y mayor recubrimiento de concreto en elementos expuestos &mdash; obligatorio cerca del mar y recomendable en toda la ciudad.</li>
<li><strong>Azotea como terraza desde el proyecto.</strong> Donde la altura lo permite es el metro cuadrado más valioso de la casa; adaptarla después cuesta varias veces más.</li>
</ul>
<p>Guías útiles: <a href="/constructora-riviera-maya/">Constructora en la Riviera Maya</a> &middot; <a href="/permisos-de-construccion-playa-del-carmen/">Permisos en Playa del Carmen</a> &middot; <a href="/construccion-de-casas-playa-del-carmen/">Construcción de casas</a> &middot; <a href="/cuanto-cuesta-construir-casa-playa-del-carmen/">¿Cuánto cuesta construir?</a> &middot; <a href="/villas-de-lujo-cancun/">Villas de lujo en Cancún</a> &middot; <a href="/villas-de-lujo-puerto-aventuras/">Villas de lujo en Puerto Aventuras</a></p>

<h2 class="mt-4">Por Qué Elegir Recrea</h2>
<ul>
<li><strong>196+ proyectos</strong> desde 2008, con oficina en Corasol y obra propia en Playacar, Corasol y la franja costera.</li>
<li><strong>Contrato a precio fijo</strong> con presupuesto desglosado, pagos por avance verificado y retención hasta cerrar la lista de detalles.</li>
<li><strong>Todo en casa:</strong> arquitectura, estructura, instalaciones, carpintería, herrería, alberca e interiorismo.</li>
<li><strong>Trámites completos:</strong> Solidaridad, DRO, SEMA, ZOFEMAT y comité del fraccionamiento.</li>
<li><strong>Obra a distancia</strong> con reportes semanales en foto y video.</li>
<li><strong>Garantía por escrito</strong> de un año sobre la obra.</li>
</ul>

<h2 class="mt-4">Preguntas Frecuentes</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">¿Cuánto cuesta construir una villa de lujo en Playa del Carmen?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">En 2026, de $24,000 a $45,000+ MXN/m² según la zona y los acabados. Una villa de 400 m² en Playacar o Corasol ronda los $10&ndash;16 millones MXN llave en mano; en Mayakoba sube bastante más.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">¿En qué zonas construyen villas de lujo?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar Fase I y II, Corasol, Mayakoba, Zazil-Ha y Coco Beach, las privadas El Cielo, Selvamar y Playa Magna, y la franja costera al norte: Playa del Secreto y Punta Bete&ndash;Xcalacoco.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">¿Qué permisos se necesitan?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Uso de suelo, licencia y alineamiento de Solidaridad con DRO. En lotes con vegetación o cerca de cenotes se suma el expediente ambiental estatal, y frente al mar la zona federal marítimo terrestre. Los fraccionamientos añaden su comité de diseño.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">¿Cuánto tarda la obra?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">De 10 a 16 meses de obra, más 2&ndash;4 meses de proyecto y trámites. En Playacar, Corasol y Mayakoba los horarios restringidos y los ciclos de revisión llevan el plazo al extremo alto.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">¿Playacar, Corasol o Mayakoba?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar por caminabilidad real a la Quinta Avenida y arbolado maduro, con calles angostas y lotes casi agotados. Corasol por lotes grandes y golf en un plan maestro aún en desarrollo. Mayakoba por el estándar de resort &mdash; y por el precio más alto del corredor.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">¿Pueden construir a distancia?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Sí. Reportes semanales con foto y video, videollamadas de avance, pagos por avance verificado y gestión completa de permisos y notaría.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">¿Listo para su villa en Playa del Carmen?</h3><p class="text-white-50 mb-4">196+ proyectos. Contrato a precio fijo. Cotización detallada en 48 horas.</p><a href="https://wa.me/529844525333?text=Hola!%20Quiero%20cotizar%20una%20villa%20de%20lujo%20en%20Playa%20del%20Carmen" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Cotizar por WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ Años</span><span class="trust-badge"><i class="bi bi-building"></i>196+ Proyectos</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Licencia y DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>Garantía 1 Año</span></div>
</div></div></div></section>""",
}

P["en"] = {
 "title": "Luxury Villas in Playa del Carmen 2026: Build &amp; Remodel",
 "desc": "Luxury villa construction and remodeling in Playa del Carmen — Playacar, Corasol, Mayakoba, Zazil-Ha and the beachfront strip north. 2026 prices and permits.",
 "keywords": "luxury villas playa del carmen, villa construction playacar, luxury home corasol, build villa riviera maya, mayakoba villa builder",
 "faq": [
  ("How much does a luxury villa cost in Playa del Carmen?",
   "In 2026, $24,000 to $45,000+ MXN/m² depending on the area and the finish. A 400 m² villa in Playacar or Corasol lands around $10–16 million MXN turnkey; Mayakoba runs considerably higher. Fixed price with an itemised budget."),
  ("Which areas do you build luxury villas in?",
   "Playacar Phase I and II, Corasol, Mayakoba, Zazil-Ha and Coco Beach, the established gated communities El Cielo, Selvamar and Playa Magna, and the beachfront strip north: Playa del Secreto and Punta Bete–Xcalacoco."),
  ("What permits are required?",
   "Land use, construction licence and alignment from the municipality of Solidaridad, with a Director Responsable de Obra. Vegetated or cenote-adjacent lots add the state environmental file, and beachfront adds the federal maritime zone. Gated communities add their own design committee."),
  ("How long does construction take?",
   "Ten to sixteen months on site, plus two to four months of design and permits. In Playacar, Corasol and Mayakoba the restricted working hours and committee review cycles push the programme to the longer end."),
  ("Playacar, Corasol or Mayakoba?",
   "Playacar for genuine walkability to Fifth Avenue and mature canopy, against narrow streets and almost no remaining lots. Corasol for large lots and golf frontage in a master plan still being built. Mayakoba for resort-grade design control — and the highest price in the corridor."),
  ("Can you build for me remotely?",
   "Yes. Weekly photo and video reports, progress video calls, payments against verified progress and full handling of permits and notary. It is how most of our foreign clients build."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Luxury Villas in Playa del Carmen</h1>
<p class="lead">We build and remodel <strong>luxury villas in Playa del Carmen</strong> &mdash; from Playacar and Corasol to Mayakoba, Zazil-Ha and the beachfront strip to the north. Design, permits, construction, pool, home automation and furnishing under one contract. 18+ years, 196 projects, and our own office in Corasol.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Luxury villa in Playa del Carmen, 2026:</strong> $24,000&ndash;$45,000+ MXN/m² depending on area and finish. We handle the Solidaridad licence, the DRO, the environmental file and the community design committee.</div>

<h2>Where Luxury Villas Get Built in Playa del Carmen</h2>
<p>Luxury here is not one address but several, and each builds differently:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Area</th><th>Product</th><th>What changes on site</th></tr></thead><tbody>
<tr><td><a href="/luxury-villas-playacar/">Playacar Phase I &amp; II</a></td><td>Golf and near-beach villas, mostly teardown or remodel</td><td>Strict design committee, tree protection, narrow streets, ~25% over baseline</td></tr>
<tr><td><a href="/luxury-villas-corasol/">Corasol</a></td><td>Large golf-frontage villas, typically 250&ndash;450 m² built</td><td>Master plan still developing: confirm services at the lot boundary, ~30% over</td></tr>
<tr><td><a href="/luxury-villas-mayakoba/">Mayakoba</a></td><td>Resort-standard residences beside lagoons and mangrove</td><td>Design control benchmarked on the neighbouring hotels, ~42% &mdash; the corridor's ceiling</td></tr>
<tr><td><a href="/house-construction-zazil-ha-coco-beach/">Zazil-Ha and Coco Beach</a></td><td>Villas close to the sea north of the centre</td><td>Full marine specification; federal zone on beachfront lots</td></tr>
<tr><td><a href="/house-construction-el-cielo-playa-del-carmen/">El Cielo</a> and <a href="/house-construction-selvamar-playa-del-carmen/">Selvamar</a></td><td>Established gated communities with services and security</td><td>Community rulebook, direct Solidaridad route, no federal zone</td></tr>
<tr><td><a href="/house-construction-playa-del-secreto/">Playa del Secreto</a> and Punta Bete</td><td>Beachfront villas on the northern strip</td><td>ZOFEMAT, protected dune, environmental file and turtle-nesting rules</td></tr>
</tbody></table></div>

<h2 class="mt-4">Everything Your Villa Needs</h2>
<div class="row g-3 my-2">
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-house-heart me-2" style="color:var(--accent)"></i>Turnkey Villa</h5><p class="small mb-0">From the soil study to a furnished handover, with the Solidaridad licence and DRO included.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-hammer me-2" style="color:var(--accent)"></i>Teardown and Rebuild</h5><p class="small mb-0">Most Playacar projects are remodel or rebuild &mdash; structural survey first, decision second.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-water me-2" style="color:var(--accent)"></i>Pools and Outdoor</h5><p class="small mb-0">Infinity pool, chukum finishes, roof terrace and palapa, designed around the golf, sea or jungle view.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-tree me-2" style="color:var(--accent)"></i>Trees and Environmental</h5><p class="small mb-0">Tree survey, environmental file and a design that keeps the canopy that gives shade and value.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-file-earmark-text me-2" style="color:var(--accent)"></i>Permits and Committees</h5><p class="small mb-0">Solidaridad licence, DRO, SEMA and ZOFEMAT where they apply, plus the community approval.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-lamp me-2" style="color:var(--accent)"></i>Interiors and Automation</h5><p class="small mb-0">Kitchen, bespoke joinery, lighting, climate and security, ready to live in or to rent.</p></div></div>
</div>

<h2 class="mt-4">Luxury Villa Prices in Playa del Carmen (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Area / scope</th><th>MXN/m²</th><th>USD/m²</th></tr></thead><tbody>
<tr><td>Full remodel of an existing villa</td><td>$14,000&ndash;$26,000</td><td>$780&ndash;$1,445</td></tr>
<tr><td>New premium villa, established gated community</td><td>$24,000&ndash;$30,000</td><td>$1,335&ndash;$1,670</td></tr>
<tr><td>Playacar / Corasol</td><td>$26,000&ndash;$38,000</td><td>$1,445&ndash;$2,110</td></tr>
<tr><td>Mayakoba and beachfront</td><td>$35,000&ndash;$55,000+</td><td>$1,945&ndash;$3,055+</td></tr>
</tbody></table></div>
<p class="text-muted small">Covers structure, installations and finishes. Land, a designed pool, mature landscaping and furniture are quoted separately. Playa del Carmen's standard-build baseline for reference: $17,000&ndash;$21,000 MXN/m².</p>

<h2 class="mt-4">What to Know Before You Build</h2>
<ul>
<li><strong>Municipality of Solidaridad.</strong> Land use, licence, alignment and DRO. Check the lot's COS, CUS, height limit and setbacks before commissioning a design &mdash; those numbers decide whether the villa you have in mind fits at all.</li>
<li><strong>Design committees.</strong> Playacar, Corasol and Mayakoba review height, massing, materials, colour, boundary walls and tree removal, with registered workers, restricted hours and a bond. Submit at concept stage; an unscheduled review round is the most common delay.</li>
<li><strong>Mature canopy.</strong> In Playacar and Corasol it is protected and valuable: every removal is justified, and a design threaded between the trees is approved faster and produces a cooler house.</li>
<li><strong>Soil study.</strong> Karst gives excellent bearing and a cavity two metres away. Probes go across the actual footprint.</li>
<li><strong>Marine specification.</strong> 316 stainless, anodised or marine-coated aluminium and increased concrete cover on exposed elements &mdash; mandatory near the sea, sensible across the city.</li>
<li><strong>Design the roof as a terrace from the start</strong> where the height limit allows. It is the highest-value square metre in the house, and retrofitting it costs several times as much.</li>
</ul>
<p>Useful guides: <a href="/general-contractor-riviera-maya/">General contractor in the Riviera Maya</a> &middot; <a href="/construction-permits-playa-del-carmen/">Permits in Playa del Carmen</a> &middot; <a href="/house-construction-playa-del-carmen/">House construction</a> &middot; <a href="/blog/cost-to-build-house-playa-del-carmen.html">What it costs to build</a> &middot; <a href="/luxury-villas-cancun/">Luxury villas in Canc&uacute;n</a> &middot; <a href="/luxury-villas-puerto-aventuras/">Luxury villas in Puerto Aventuras</a></p>

<h2 class="mt-4">Why Build with Recrea</h2>
<ul>
<li><strong>196+ projects</strong> since 2008, with our office in Corasol and our own work in Playacar, Corasol and along the coastal strip.</li>
<li><strong>Fixed-price contract</strong> with an itemised budget, payments against verified progress and retention until the snag list closes.</li>
<li><strong>Everything in house:</strong> architecture, structure, installations, carpentry, metalwork, pool and interiors.</li>
<li><strong>Full permit handling:</strong> Solidaridad, DRO, SEMA, ZOFEMAT and the community committee.</li>
<li><strong>Remote construction</strong> with weekly photo and video reporting.</li>
<li><strong>One-year written warranty</strong> on the work.</li>
</ul>

<h2 class="mt-4">Frequently Asked Questions</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">How much does a luxury villa cost in Playa del Carmen?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">In 2026, $24,000 to $45,000+ MXN/m² depending on the area and the finish. A 400 m² villa in Playacar or Corasol lands around $10&ndash;16 million MXN turnkey; Mayakoba runs considerably higher.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">Which areas do you build luxury villas in?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar Phase I and II, Corasol, Mayakoba, Zazil-Ha and Coco Beach, the established gated communities El Cielo, Selvamar and Playa Magna, and the beachfront strip north: Playa del Secreto and Punta Bete&ndash;Xcalacoco.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">What permits are required?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Land use, construction licence and alignment from Solidaridad with a DRO. Vegetated or cenote-adjacent lots add the state environmental file, and beachfront adds the federal maritime zone. Gated communities add their own design committee.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">How long does construction take?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Ten to sixteen months on site, plus two to four months of design and permits. In Playacar, Corasol and Mayakoba the restricted hours and committee review cycles push the programme to the longer end.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">Playacar, Corasol or Mayakoba?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar for genuine walkability to Fifth Avenue and mature canopy, against narrow streets and almost no remaining lots. Corasol for large lots and golf frontage in a master plan still being built. Mayakoba for resort-grade design control &mdash; and the highest price in the corridor.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">Can you build for me remotely?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Yes. Weekly photo and video reports, progress video calls, payments against verified progress and full handling of permits and notary.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">Ready to build your villa in Playa del Carmen?</h3><p class="text-white-50 mb-4">196+ projects completed. Fixed-price contracts. Detailed quote within 48 hours.</p><a href="https://wa.me/529844525333?text=Hello!%20I%20want%20a%20quote%20for%20a%20luxury%20villa%20in%20Playa%20del%20Carmen" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Get a Quote on WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ Years</span><span class="trust-badge"><i class="bi bi-building"></i>196+ Projects</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Licensed &amp; DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>1-Year Warranty</span></div>
</div></div></div></section>""",
}

P["de"] = {
 "title": "Luxusvillen in Playa del Carmen 2026: Bau &amp; Sanierung",
 "desc": "Luxusvillen in Playa del Carmen bauen und sanieren — Playacar, Corasol, Mayakoba, Zazil-Ha und der Küstenstreifen im Norden. Preise 2026 und Genehmigungen.",
 "keywords": "luxusvilla playa del carmen, villa bauen playacar, luxushaus corasol, villa mayakoba bauen, bauunternehmen villa riviera maya",
 "faq": [
  ("Was kostet eine Luxusvilla in Playa del Carmen?",
   "2026 zwischen $24,000 und $45,000+ MXN/m², je nach Lage und Ausbau. Eine 400-m²-Villa in Playacar oder Corasol liegt schlüsselfertig bei rund $10–16 Mio. MXN; Mayakoba deutlich darüber. Festpreis mit Positionsbudget."),
  ("In welchen Lagen bauen Sie Luxusvillen?",
   "Playacar Phase I und II, Corasol, Mayakoba, Zazil-Ha und Coco Beach, die etablierten Wohnanlagen El Cielo, Selvamar und Playa Magna sowie der Küstenstreifen im Norden: Playa del Secreto und Punta Bete–Xcalacoco."),
  ("Welche Genehmigungen sind nötig?",
   "Nutzungszertifikat, Baugenehmigung und Fluchtlinie der Gemeinde Solidaridad mit einem Director Responsable de Obra. Bewachsene oder cenotennahe Grundstücke brauchen zusätzlich die Umweltakte, Strandlagen die Bundesküstenzone. Wohnanlagen haben einen eigenen Gestaltungsbeirat."),
  ("Wie lange dauert der Bau?",
   "Zehn bis sechzehn Monate Bauzeit, plus zwei bis vier Monate Planung und Genehmigungen. In Playacar, Corasol und Mayakoba schieben eingeschränkte Arbeitszeiten und Prüfzyklen den Termin ans obere Ende."),
  ("Playacar, Corasol oder Mayakoba?",
   "Playacar wegen echter Fußläufigkeit zur Quinta Avenida und altem Baumbestand, dafür enge Straßen und kaum freie Grundstücke. Corasol wegen großer Grundstücke am Golfplatz in einem noch entstehenden Masterplan. Mayakoba wegen Resort-Standard — und zum höchsten Preis im Korridor."),
  ("Können Sie aus der Ferne für mich bauen?",
   "Ja. Wöchentliche Foto- und Videoberichte, Fortschritts-Videocalls, Zahlungen nach geprüftem Baufortschritt und die komplette Abwicklung von Genehmigungen und Notar."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Luxusvillen in Playa del Carmen</h1>
<p class="lead">Wir bauen und sanieren <strong>Luxusvillen in Playa del Carmen</strong> &mdash; von Playacar und Corasol bis Mayakoba, Zazil-Ha und den K&uuml;stenstreifen im Norden. Planung, Genehmigungen, Bau, Pool, Smart Home und Ausstattung aus einer Hand. 18+ Jahre, 196 Projekte, eigenes B&uuml;ro in Corasol.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Luxusvilla in Playa del Carmen 2026:</strong> $24.000&ndash;$45.000+ MXN/m² je nach Lage und Ausbau. Wir &uuml;bernehmen die Genehmigung in Solidaridad, den DRO, die Umweltakte und den Gestaltungsbeirat der Anlage.</div>

<h2>Wo in Playa del Carmen Luxusvillen entstehen</h2>
<p>Luxus ist hier keine einzelne Adresse, sondern mehrere &mdash; und jede baut sich anders:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Lage</th><th>Produkt</th><th>Was sich auf der Baustelle ändert</th></tr></thead><tbody>
<tr><td>Playacar Phase I und II</td><td>Villen am Golfplatz und nahe Strand, meist Abriss oder Sanierung</td><td>Strenger Gestaltungsbeirat, Baumschutz, enge Stra&szlig;en, rund 25% &uuml;ber Basis</td></tr>
<tr><td>Corasol</td><td>Gro&szlig;e Villen am Golfplatz, meist 250&ndash;450 m² Wohnfl&auml;che</td><td>Masterplan noch im Bau: Erschlie&szlig;ung an der Grundst&uuml;cksgrenze pr&uuml;fen, rund 30% &uuml;ber Basis</td></tr>
<tr><td>Mayakoba</td><td>Residenzen auf Resort-Niveau an Lagunen und Mangroven</td><td>Gestaltungskontrolle am Ma&szlig;stab der Nachbarhotels, rund 42% &mdash; die Obergrenze im Korridor</td></tr>
<tr><td>Zazil-Ha und Coco Beach</td><td>Villen in Meern&auml;he n&ouml;rdlich des Zentrums</td><td>Volle Marine-Spezifikation; Bundeszone bei Strandgrundst&uuml;cken</td></tr>
<tr><td>El Cielo, Selvamar, Playa Magna</td><td>Etablierte geschlossene Anlagen mit Infrastruktur und Sicherheit</td><td>Regelwerk der Anlage, direkter Weg &uuml;ber Solidaridad, keine Bundeszone</td></tr>
<tr><td>Playa del Secreto und Punta Bete</td><td>Strandvillen am n&ouml;rdlichen Abschnitt</td><td>ZOFEMAT, gesch&uuml;tzte D&uuml;ne, Umweltakte und Schildkr&ouml;tenregeln</td></tr>
</tbody></table></div>

<h2 class="mt-4">Preise für Luxusvillen (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Lage / Umfang</th><th>MXN/m²</th><th>USD/m²</th></tr></thead><tbody>
<tr><td>Kernsanierung einer bestehenden Villa</td><td>$14.000&ndash;$26.000</td><td>$780&ndash;$1.445</td></tr>
<tr><td>Neubau Premium, etablierte Anlage</td><td>$24.000&ndash;$30.000</td><td>$1.335&ndash;$1.670</td></tr>
<tr><td>Playacar / Corasol</td><td>$26.000&ndash;$38.000</td><td>$1.445&ndash;$2.110</td></tr>
<tr><td>Mayakoba und Strandlage</td><td>$35.000&ndash;$55.000+</td><td>$1.945&ndash;$3.055+</td></tr>
</tbody></table></div>
<p class="text-muted small">Enth&auml;lt Rohbau, Installationen und Ausbau. Grundst&uuml;ck, geplanter Pool, ausgewachsene Bepflanzung und M&ouml;bel werden separat kalkuliert. Referenz f&uuml;r Standardbau in Playa del Carmen: $17.000&ndash;$21.000 MXN/m².</p>

<h2 class="mt-4">Was Sie vor dem Bau wissen sollten</h2>
<ul>
<li><strong>Gemeinde Solidaridad.</strong> Nutzung, Genehmigung, Fluchtlinie und DRO. Pr&uuml;fen Sie COS, CUS, H&ouml;henbegrenzung und Abst&auml;nde des Grundst&uuml;cks, bevor Sie planen lassen &mdash; diese Zahlen entscheiden, ob die gew&uuml;nschte Villa &uuml;berhaupt hineinpasst.</li>
<li><strong>Gestaltungsbeir&auml;te.</strong> Playacar, Corasol und Mayakoba pr&uuml;fen H&ouml;he, Baumasse, Materialien, Farbe, Einfriedungen und Baumf&auml;llungen, mit registrierten Arbeitern, Arbeitszeiten und Kaution. In der Entwurfsphase einreichen.</li>
<li><strong>Alter Baumbestand.</strong> In Playacar und Corasol gesch&uuml;tzt und wertvoll: jede F&auml;llung wird begr&uuml;ndet, und ein Entwurf zwischen den B&auml;umen wird schneller genehmigt und ergibt ein k&uuml;hleres Haus.</li>
<li><strong>Bodengutachten.</strong> Karst bietet hervorragende Tragf&auml;higkeit und zwei Meter weiter einen Hohlraum; sondiert wird &uuml;ber der tats&auml;chlichen Grundfl&auml;che.</li>
<li><strong>Marine-Spezifikation.</strong> 316er Edelstahl, eloxiertes oder marinebeschichtetes Aluminium und gr&ouml;&szlig;ere Betondeckung an exponierten Bauteilen.</li>
<li><strong>Dach von Anfang an als Terrasse planen,</strong> wo die H&ouml;he es zul&auml;sst &mdash; der wertvollste Quadratmeter des Hauses.</li>
</ul>
<p>N&uuml;tzliche Seiten: <a href="/bauunternehmen-tulum/">Bauunternehmen an der Riviera Maya</a> &middot; <a href="/hausbau-playa-del-carmen/">Hausbau in Playa del Carmen</a> &middot; <a href="/blog-de/hausbau-kosten-playa-del-carmen.html">Hausbau-Kosten</a> &middot; <a href="/luxusvilla-bau-cancun/">Luxusvillen in Canc&uacute;n</a></p>

<h2 class="mt-4">Warum Recrea</h2>
<ul>
<li><strong>196+ Projekte</strong> seit 2008, mit B&uuml;ro in Corasol und eigener Bauleitung in Playacar, Corasol und am K&uuml;stenstreifen.</li>
<li><strong>Festpreisvertrag</strong> mit Positionsbudget, Zahlungen nach gepr&uuml;ftem Fortschritt und Einbehalt bis zur Abnahme.</li>
<li><strong>Alles im Haus:</strong> Architektur, Statik, Installationen, Tischlerei, Metallbau, Pool und Innenausbau.</li>
<li><strong>Komplette Genehmigungen:</strong> Solidaridad, DRO, SEMA, ZOFEMAT und Gestaltungsbeirat.</li>
<li><strong>Bauen aus der Ferne</strong> mit w&ouml;chentlichen Foto- und Videoberichten.</li>
<li><strong>Ein Jahr schriftliche Gew&auml;hrleistung.</strong></li>
</ul>

<h2 class="mt-4">Häufige Fragen</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">Was kostet eine Luxusvilla in Playa del Carmen?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">2026 zwischen $24.000 und $45.000+ MXN/m², je nach Lage und Ausbau. Eine 400-m²-Villa in Playacar oder Corasol liegt schl&uuml;sselfertig bei rund $10&ndash;16 Mio. MXN; Mayakoba deutlich dar&uuml;ber.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">In welchen Lagen bauen Sie?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar Phase I und II, Corasol, Mayakoba, Zazil-Ha und Coco Beach, die Anlagen El Cielo, Selvamar und Playa Magna sowie Playa del Secreto und Punta Bete&ndash;Xcalacoco im Norden.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">Welche Genehmigungen sind n&ouml;tig?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Nutzung, Genehmigung und Fluchtlinie der Gemeinde Solidaridad mit DRO. Bewachsene oder cenotennahe Grundst&uuml;cke brauchen die Umweltakte, Strandlagen die Bundesk&uuml;stenzone, Anlagen zus&auml;tzlich ihren Gestaltungsbeirat.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">Wie lange dauert der Bau?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Zehn bis sechzehn Monate, plus zwei bis vier Monate Planung und Genehmigungen. In Playacar, Corasol und Mayakoba liegt der Termin am oberen Ende.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">Playacar, Corasol oder Mayakoba?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar wegen Fu&szlig;l&auml;ufigkeit und altem Baumbestand, dafür enge Stra&szlig;en und kaum freie Grundst&uuml;cke. Corasol wegen gro&szlig;er Grundst&uuml;cke am Golfplatz. Mayakoba wegen Resort-Standard &mdash; und zum h&ouml;chsten Preis im Korridor.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">K&ouml;nnen Sie aus der Ferne bauen?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Ja. W&ouml;chentliche Foto- und Videoberichte, Fortschritts-Videocalls, Zahlungen nach gepr&uuml;ftem Fortschritt und komplette Abwicklung von Genehmigungen und Notar.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">Bereit f&uuml;r Ihre Villa in Playa del Carmen?</h3><p class="text-white-50 mb-4">196+ Projekte. Festpreis. Detailliertes Angebot in 48 Stunden.</p><a href="https://wa.me/529844525333?text=Hallo!%20Angebot%20Luxusvilla%20Playa%20del%20Carmen" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Angebot per WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ Jahre</span><span class="trust-badge"><i class="bi bi-building"></i>196+ Projekte</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Lizenz &amp; DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>1 Jahr Garantie</span></div>
</div></div></div></section>""",
}

P["ru"] = {
 "title": "Виллы Люкс в Плая-дель-Кармен 2026 | Строительство",
 "desc": "Строительство и реконструкция вилл люкс в Плая-дель-Кармен: Плаякар, Корасоль, Майякоба, Сасиль-Ха и побережье к северу. Цены 2026 и разрешения.",
 "keywords": "виллы люкс плая дель кармен, построить виллу плаякар, элитный дом корасоль, вилла майякоба, строительство вилл ривьера майя",
 "faq": [
  ("Сколько стоит вилла люкс в Плая-дель-Кармен?",
   "В 2026 году от $24,000 до $45,000+ MXN/м² в зависимости от района и отделки. Вилла 400 м² в Плаякаре или Корасоле — примерно $10–16 млн MXN под ключ; в Майякобе заметно выше. Фиксированная цена с постатейной сметой."),
  ("В каких районах вы строите виллы люкс?",
   "Плаякар Фаза I и II, Корасоль, Майякоба, Сасиль-Ха и Коко-Бич, закрытые посёлки El Cielo, Selvamar и Playa Magna, а также побережье к северу: Playa del Secreto и Punta Bete–Xcalacoco."),
  ("Какие разрешения нужны?",
   "Назначение земли, лицензия и выравнивание муниципалитета Солидаридад с Director Responsable de Obra. На участках с растительностью или рядом с сенотами добавляется экологическое досье, на первой линии — федеральная морская зона. В посёлках действует свой архитектурный комитет."),
  ("Сколько идёт стройка?",
   "10–16 месяцев работ плюс 2–4 месяца на проект и разрешения. В Плаякаре, Корасоле и Майякобе ограниченные часы работ и циклы согласования сдвигают срок к верхней границе."),
  ("Плаякар, Корасоль или Майякоба?",
   "Плаякар — реальная пешая доступность Пятой авеню и взрослые деревья, но узкие улицы и почти не осталось участков. Корасоль — крупные участки у гольфа в развивающемся мастер-плане. Майякоба — стандарт резорта и самая высокая цена на побережье."),
  ("Можно ли строить дистанционно?",
   "Да. Еженедельные отчёты с фото и видео, видеозвонки по ходу работ, оплата по проверенному факту и полное ведение разрешений и нотариата."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Виллы Люкс в Плая-дель-Кармен</h1>
<p class="lead">Строим и реконструируем <strong>виллы люкс в Плая-дель-Кармен</strong> &mdash; от Плаякара и Корасоля до Майякобы, Сасиль-Ха и побережья к северу. Проект, разрешения, стройка, бассейн, автоматизация и меблировка по одному договору. 18+ лет, 196 проектов, собственный офис в Корасоле.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Вилла люкс в Плая-дель-Кармен, 2026:</strong> $24,000&ndash;$45,000+ MXN/м² в зависимости от района и отделки. Берём на себя лицензию Солидаридад, DRO, экологическое досье и согласование в посёлке.</div>

<h2>Где строят виллы люкс в Плая-дель-Кармен</h2>
<p>Люкс здесь &mdash; это не один адрес, а несколько, и строятся они по-разному:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Район</th><th>Продукт</th><th>Что меняется на стройке</th></tr></thead><tbody>
<tr><td>Плаякар, Фаза I и II</td><td>Виллы у гольфа и рядом с пляжем, чаще снос или реконструкция</td><td>Строгий комитет, защита деревьев, узкие улицы, около +25% к базе</td></tr>
<tr><td>Корасоль</td><td>Крупные виллы у поля для гольфа, обычно 250&ndash;450 м²</td><td>Мастер-план ещё строится: проверять коммуникации на границе участка, около +30%</td></tr>
<tr><td>Майякоба</td><td>Резиденции уровня резорта у лагун и мангров</td><td>Контроль архитектуры по стандарту соседних отелей, около +42% &mdash; максимум побережья</td></tr>
<tr><td>Сасиль-Ха и Коко-Бич</td><td>Виллы рядом с морем к северу от центра</td><td>Полная морская спецификация; федеральная зона на участках первой линии</td></tr>
<tr><td>El Cielo, Selvamar, Playa Magna</td><td>Сложившиеся закрытые посёлки с инфраструктурой и охраной</td><td>Регламент посёлка, прямой путь через Солидаридад, без федеральной зоны</td></tr>
<tr><td>Playa del Secreto и Punta Bete</td><td>Виллы первой линии на северном участке</td><td>ZOFEMAT, охраняемая дюна, экологическое досье и правила гнездования черепах</td></tr>
</tbody></table></div>

<h2 class="mt-4">Цены на виллы люкс (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Район / объём</th><th>MXN/м²</th><th>USD/м²</th></tr></thead><tbody>
<tr><td>Полная реконструкция существующей виллы</td><td>$14,000&ndash;$26,000</td><td>$780&ndash;$1,445</td></tr>
<tr><td>Новая вилла премиум в сложившемся посёлке</td><td>$24,000&ndash;$30,000</td><td>$1,335&ndash;$1,670</td></tr>
<tr><td>Плаякар / Корасоль</td><td>$26,000&ndash;$38,000</td><td>$1,445&ndash;$2,110</td></tr>
<tr><td>Майякоба и первая линия</td><td>$35,000&ndash;$55,000+</td><td>$1,945&ndash;$3,055+</td></tr>
</tbody></table></div>
<p class="text-muted small">Включает конструктив, инженерию и отделку. Земля, проектный бассейн, взрослое озеленение и мебель считаются отдельно. Базовый ориентир по Плая-дель-Кармен: $17,000&ndash;$21,000 MXN/м² в стандартной отделке.</p>

<h2 class="mt-4">Что нужно знать до начала</h2>
<ul>
<li><strong>Муниципалитет Солидаридад.</strong> Назначение земли, лицензия, выравнивание и DRO. Проверьте COS, CUS, ограничение высоты и отступы участка до заказа проекта &mdash; именно эти цифры решают, поместится ли задуманная вилла.</li>
<li><strong>Архитектурные комитеты.</strong> Плаякар, Корасоль и Майякоба проверяют высоту, объём, материалы, цвет, ограждения и вырубку деревьев, требуют регистрации рабочих, соблюдения часов и залога. Подавайте на стадии эскиза.</li>
<li><strong>Взрослые деревья.</strong> В Плаякаре и Корасоле они охраняются и стоят денег: каждая вырубка обосновывается, а проект, вписанный между деревьями, согласуется быстрее и даёт более прохладный дом.</li>
<li><strong>Геология.</strong> Карст даёт отличное основание и полость в двух метрах рядом; скважины делают по фактическому пятну застройки.</li>
<li><strong>Морская спецификация.</strong> Нержавейка 316, анодированный или с морским покрытием алюминий и увеличенный защитный слой бетона на открытых элементах.</li>
<li><strong>Кровля как терраса с самого проекта,</strong> где позволяет высота &mdash; самый ценный метр дома.</li>
</ul>
<p>Полезные страницы: <a href="/stroitelnaya-kompaniya-cancun/">Строительная компания</a> &middot; <a href="/stroitelstvo-domov-playa-del-carmen/">Строительство домов в Плая-дель-Кармен</a> &middot; <a href="/blog-ru/skolko-stoit-postroit-dom-playa-del-carmen.html">Сколько стоит построить дом</a> &middot; <a href="/stroitelstvo-vill-cancun/">Виллы люкс в Канкуне</a></p>

<h2 class="mt-4">Почему Recrea</h2>
<ul>
<li><strong>196+ проектов</strong> с 2008 года, офис в Корасоле, собственные объекты в Плаякаре, Корасоле и на побережье.</li>
<li><strong>Договор с фиксированной ценой</strong> и постатейной сметой, оплата по проверенному факту, удержание до закрытия замечаний.</li>
<li><strong>Всё внутри компании:</strong> архитектура, конструктив, инженерия, столярка, металл, бассейн и интерьер.</li>
<li><strong>Разрешения под ключ:</strong> Солидаридад, DRO, SEMA, ZOFEMAT и комитет посёлка.</li>
<li><strong>Стройка дистанционно</strong> с еженедельными отчётами в фото и видео.</li>
<li><strong>Год письменной гарантии</strong> на работы.</li>
</ul>

<h2 class="mt-4">Частые вопросы</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">Сколько стоит вилла люкс в Плая-дель-Кармен?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">В 2026 году от $24,000 до $45,000+ MXN/м² в зависимости от района и отделки. Вилла 400 м² в Плаякаре или Корасоле &mdash; примерно $10&ndash;16 млн MXN под ключ; в Майякобе заметно выше.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">В каких районах вы строите?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Плаякар Фаза I и II, Корасоль, Майякоба, Сасиль-Ха и Коко-Бич, посёлки El Cielo, Selvamar и Playa Magna, а также Playa del Secreto и Punta Bete&ndash;Xcalacoco к северу.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">Какие разрешения нужны?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Назначение земли, лицензия и выравнивание Солидаридад с DRO. На участках с растительностью или рядом с сенотами добавляется экологическое досье, на первой линии &mdash; федеральная морская зона, в посёлках &mdash; свой комитет.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">Сколько идёт стройка?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">10&ndash;16 месяцев плюс 2&ndash;4 месяца на проект и разрешения. В Плаякаре, Корасоле и Майякобе срок уходит к верхней границе.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">Плаякар, Корасоль или Майякоба?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Плаякар &mdash; пешая доступность и взрослые деревья, но узкие улицы и почти нет участков. Корасоль &mdash; крупные участки у гольфа. Майякоба &mdash; стандарт резорта и самая высокая цена на побережье.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">Можно ли строить дистанционно?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Да. Еженедельные отчёты с фото и видео, видеозвонки, оплата по проверенному факту и полное ведение разрешений и нотариата.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">Готовы начать виллу в Плая-дель-Кармен?</h3><p class="text-white-50 mb-4">196+ проектов. Фиксированная цена. Детальная смета за 48 часов.</p><a href="https://wa.me/529844525333?text=Здравствуйте!%20Смета%20на%20виллу%20в%20Плая-дель-Кармен" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Запросить в WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ лет</span><span class="trust-badge"><i class="bi bi-building"></i>196+ проектов</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Лицензия и DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>Гарантия 1 год</span></div>
</div></div></div></section>""",
}

P["fr"] = {
 "title": "Villas de Luxe à Playa del Carmen 2026 | Recrea",
 "desc": "Construction et rénovation de villas de luxe à Playa del Carmen : Playacar, Corasol, Mayakoba, Zazil-Ha et la côte au nord. Prix 2026 et permis.",
 "keywords": "villas de luxe playa del carmen, construction villa playacar, maison de luxe corasol, villa mayakoba, constructeur villa riviera maya",
 "faq": [
  ("Combien coûte une villa de luxe à Playa del Carmen ?",
   "En 2026, de $24,000 à $45,000+ MXN/m² selon le secteur et la finition. Une villa de 400 m² à Playacar ou Corasol revient à environ $10–16 millions MXN clé en main ; Mayakoba est nettement au-dessus. Prix ferme avec budget détaillé."),
  ("Dans quels secteurs construisez-vous des villas de luxe ?",
   "Playacar Phase I et II, Corasol, Mayakoba, Zazil-Ha et Coco Beach, les résidences établies El Cielo, Selvamar et Playa Magna, et la bande côtière au nord : Playa del Secreto et Punta Bete–Xcalacoco."),
  ("Quels permis sont nécessaires ?",
   "Usage du sol, permis de construire et alignement de la municipalité de Solidaridad, avec un Director Responsable de Obra. Les parcelles boisées ou proches d'un cenote ajoutent le dossier environnemental, le front de mer la zone fédérale maritime. Les résidences ont leur propre comité."),
  ("Combien de temps dure le chantier ?",
   "Dix à seize mois de chantier, plus deux à quatre mois de conception et de permis. À Playacar, Corasol et Mayakoba, les horaires restreints et les cycles d'examen placent le délai en haut de la fourchette."),
  ("Playacar, Corasol ou Mayakoba ?",
   "Playacar pour la marche à pied jusqu'à la Quinta Avenida et les arbres matures, mais rues étroites et presque plus de terrains. Corasol pour de grandes parcelles au bord du golf dans un plan directeur en cours. Mayakoba pour le standard resort — et le prix le plus élevé du corridor."),
  ("Pouvez-vous construire à distance ?",
   "Oui. Rapports hebdomadaires photo et vidéo, visioconférences d'avancement, paiements à l'avancement vérifié et gestion complète des permis et du notaire."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Villas de Luxe &agrave; Playa del Carmen</h1>
<p class="lead">Nous construisons et r&eacute;novons des <strong>villas de luxe &agrave; Playa del Carmen</strong> &mdash; de Playacar et Corasol &agrave; Mayakoba, Zazil-Ha et la bande c&ocirc;ti&egrave;re au nord. Conception, permis, chantier, piscine, domotique et ameublement sous un seul contrat. 18+ ans, 196 projets, bureau &agrave; Corasol.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Villa de luxe &agrave; Playa del Carmen, 2026 :</strong> $24,000&ndash;$45,000+ MXN/m² selon le secteur et la finition. Nous prenons en charge le permis de Solidaridad, le DRO, le dossier environnemental et le comit&eacute; de la r&eacute;sidence.</div>

<h2>Où se construisent les villas de luxe</h2>
<p>Le luxe ici n'est pas une adresse mais plusieurs, et chacune se construit diff&eacute;remment :</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Secteur</th><th>Produit</th><th>Ce qui change sur le chantier</th></tr></thead><tbody>
<tr><td>Playacar Phase I et II</td><td>Villas au golf et pr&egrave;s de la plage, surtout d&eacute;molition ou r&eacute;novation</td><td>Comit&eacute; strict, protection des arbres, rues &eacute;troites, environ +25% sur la base</td></tr>
<tr><td>Corasol</td><td>Grandes villas au bord du golf, 250&ndash;450 m² construits</td><td>Plan directeur en cours : v&eacute;rifier les r&eacute;seaux en limite, environ +30%</td></tr>
<tr><td>Mayakoba</td><td>R&eacute;sidences de standard resort, lagunes et mangrove</td><td>Contr&ocirc;le de conception au niveau des h&ocirc;tels voisins, environ +42% &mdash; le plafond du corridor</td></tr>
<tr><td>Zazil-Ha et Coco Beach</td><td>Villas proches de la mer au nord du centre</td><td>Sp&eacute;cification marine int&eacute;grale ; zone f&eacute;d&eacute;rale sur les parcelles en front de mer</td></tr>
<tr><td>El Cielo, Selvamar, Playa Magna</td><td>R&eacute;sidences ferm&eacute;es &eacute;tablies, services et s&eacute;curit&eacute;</td><td>R&egrave;glement de la r&eacute;sidence, parcours Solidaridad direct, pas de zone f&eacute;d&eacute;rale</td></tr>
<tr><td>Playa del Secreto et Punta Bete</td><td>Villas en front de mer sur la bande nord</td><td>ZOFEMAT, dune prot&eacute;g&eacute;e, dossier environnemental et r&egrave;gles de nidification</td></tr>
</tbody></table></div>

<h2 class="mt-4">Prix des villas de luxe (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Secteur / prestation</th><th>MXN/m²</th><th>USD/m²</th></tr></thead><tbody>
<tr><td>R&eacute;novation lourde d'une villa existante</td><td>$14,000&ndash;$26,000</td><td>$780&ndash;$1,445</td></tr>
<tr><td>Villa neuve premium, r&eacute;sidence &eacute;tablie</td><td>$24,000&ndash;$30,000</td><td>$1,335&ndash;$1,670</td></tr>
<tr><td>Playacar / Corasol</td><td>$26,000&ndash;$38,000</td><td>$1,445&ndash;$2,110</td></tr>
<tr><td>Mayakoba et front de mer</td><td>$35,000&ndash;$55,000+</td><td>$1,945&ndash;$3,055+</td></tr>
</tbody></table></div>
<p class="text-muted small">Comprend structure, installations et finitions. Terrain, piscine con&ccedil;ue, plantations matures et mobilier chiffr&eacute;s &agrave; part. R&eacute;f&eacute;rence en construction standard &agrave; Playa del Carmen : $17,000&ndash;$21,000 MXN/m².</p>

<h2 class="mt-4">À savoir avant de construire</h2>
<ul>
<li><strong>Municipalit&eacute; de Solidaridad.</strong> Usage du sol, permis, alignement et DRO. V&eacute;rifiez COS, CUS, hauteur et retraits de la parcelle avant de commander un projet &mdash; ce sont ces chiffres qui d&eacute;cident si la villa envisag&eacute;e tient.</li>
<li><strong>Comit&eacute;s d'architecture.</strong> Playacar, Corasol et Mayakoba examinent hauteur, volume, mat&eacute;riaux, couleur, cl&ocirc;tures et abattage d'arbres, avec ouvriers enregistr&eacute;s, horaires et caution. D&eacute;posez au stade avant-projet.</li>
<li><strong>Arbres matures.</strong> &Agrave; Playacar et Corasol ils sont prot&eacute;g&eacute;s et pr&eacute;cieux : chaque abattage se justifie, et un projet dessin&eacute; entre les arbres passe plus vite et donne une maison plus fra&icirc;che.</li>
<li><strong>&Eacute;tude de sol.</strong> Le karst offre une excellente portance et une cavit&eacute; deux m&egrave;tres plus loin ; les sondages couvrent l'emprise r&eacute;elle.</li>
<li><strong>Sp&eacute;cification marine.</strong> Inox 316, aluminium anodis&eacute; ou &agrave; rev&ecirc;tement marin et enrobage de b&eacute;ton augment&eacute; sur les &eacute;l&eacute;ments expos&eacute;s.</li>
<li><strong>Toit-terrasse d&egrave;s la conception</strong> l&agrave; o&ugrave; la hauteur l'autorise &mdash; le m&egrave;tre carr&eacute; le plus pr&eacute;cieux de la maison.</li>
</ul>
<p>Pages utiles : <a href="/constructeur-cancun/">Constructeur dans la Riviera Maya</a> &middot; <a href="/construction-de-maisons-playa-del-carmen/">Construction de maisons</a> &middot; <a href="/blog-fr/cout-construire-maison-playa-del-carmen.html">Co&ucirc;t de construction</a> &middot; <a href="/construction-villa-luxe-cancun/">Villas de luxe &agrave; Canc&uacute;n</a></p>

<h2 class="mt-4">Pourquoi Recrea</h2>
<ul>
<li><strong>196+ projets</strong> depuis 2008, bureau &agrave; Corasol et chantiers propres &agrave; Playacar, Corasol et sur la bande c&ocirc;ti&egrave;re.</li>
<li><strong>Contrat &agrave; prix ferme</strong> avec budget d&eacute;taill&eacute;, paiements &agrave; l'avancement v&eacute;rifi&eacute; et retenue jusqu'&agrave; lev&eacute;e des r&eacute;serves.</li>
<li><strong>Tout en interne :</strong> architecture, structure, installations, menuiserie, m&eacute;tallerie, piscine et int&eacute;rieurs.</li>
<li><strong>Permis complets :</strong> Solidaridad, DRO, SEMA, ZOFEMAT et comit&eacute; de la r&eacute;sidence.</li>
<li><strong>Chantier &agrave; distance</strong> avec rapports hebdomadaires photo et vid&eacute;o.</li>
<li><strong>Garantie &eacute;crite d'un an</strong> sur les travaux.</li>
</ul>

<h2 class="mt-4">Questions fréquentes</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">Combien co&ucirc;te une villa de luxe &agrave; Playa del Carmen ?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">En 2026, de $24,000 &agrave; $45,000+ MXN/m² selon le secteur et la finition. Une villa de 400 m² &agrave; Playacar ou Corasol revient &agrave; environ $10&ndash;16 millions MXN cl&eacute; en main ; Mayakoba est nettement au-dessus.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">Dans quels secteurs construisez-vous ?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar Phase I et II, Corasol, Mayakoba, Zazil-Ha et Coco Beach, les r&eacute;sidences El Cielo, Selvamar et Playa Magna, et la bande c&ocirc;ti&egrave;re au nord.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">Quels permis sont n&eacute;cessaires ?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Usage du sol, permis et alignement de Solidaridad avec un DRO. Les parcelles bois&eacute;es ou proches d'un cenote ajoutent le dossier environnemental, le front de mer la zone f&eacute;d&eacute;rale maritime, et les r&eacute;sidences leur propre comit&eacute;.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">Combien de temps dure le chantier ?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Dix &agrave; seize mois, plus deux &agrave; quatre mois de conception et de permis. &Agrave; Playacar, Corasol et Mayakoba le d&eacute;lai se situe en haut de la fourchette.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">Playacar, Corasol ou Mayakoba ?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar pour la marche &agrave; pied et les arbres matures, mais rues &eacute;troites et peu de terrains. Corasol pour de grandes parcelles au golf. Mayakoba pour le standard resort &mdash; et le prix le plus &eacute;lev&eacute; du corridor.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">Pouvez-vous construire &agrave; distance ?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Oui. Rapports hebdomadaires photo et vid&eacute;o, visioconf&eacute;rences, paiements &agrave; l'avancement v&eacute;rifi&eacute; et gestion compl&egrave;te des permis et du notaire.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">Pr&ecirc;t pour votre villa &agrave; Playa del Carmen ?</h3><p class="text-white-50 mb-4">196+ projets. Prix ferme. Devis d&eacute;taill&eacute; sous 48 heures.</p><a href="https://wa.me/529844525333?text=Bonjour!%20Devis%20villa%20de%20luxe%20Playa%20del%20Carmen" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Devis par WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ ans</span><span class="trust-badge"><i class="bi bi-building"></i>196+ projets</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Licence &amp; DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>Garantie 1 an</span></div>
</div></div></div></section>""",
}

P["zh"] = {
 "title": "2026年普拉亚德尔卡门豪华别墅建造与翻新 | Recrea",
 "desc": "普拉亚德尔卡门豪华别墅的建造与翻新：Playacar、Corasol、Mayakoba、Zazil-Ha 及北部海岸带。2026年价格、许可流程与设计委员会。",
 "keywords": "普拉亚德尔卡门豪华别墅, Playacar 别墅, Corasol 豪宅, Mayakoba 别墅建造, 里维埃拉玛雅别墅",
 "faq": [
  ("在普拉亚德尔卡门建一栋豪华别墅要多少钱？",
   "2026年为每平米 $24,000 至 $45,000+ 比索，取决于区域与装修。Playacar 或 Corasol 的400平米别墅交钥匙约 $1,000 万–$1,600 万比索；Mayakoba 明显更高。固定总价，附分项预算。"),
  ("你们在哪些区域建豪华别墅？",
   "Playacar 一期与二期、Corasol、Mayakoba、Zazil-Ha 与 Coco Beach，成熟封闭社区 El Cielo、Selvamar、Playa Magna，以及北部海岸带的 Playa del Secreto 与 Punta Bete–Xcalacoco。"),
  ("需要哪些许可？",
   "索利达里达德市政厅的土地用途、施工许可与红线，并需责任建筑师（DRO）。有植被或靠近天坑的地块还需州环评文件，海边地块涉及联邦海域区，封闭社区另设设计委员会。"),
  ("工期需要多久？",
   "施工10至16个月，另加2至4个月的设计与报批。在 Playacar、Corasol 和 Mayakoba，作业时段限制与审查周期会把工期推向上限。"),
  ("Playacar、Corasol 还是 Mayakoba？",
   "Playacar 胜在步行可达第五大道与成熟树冠，代价是街道狭窄、几乎没有空地。Corasol 胜在仍在开发的总体规划中的大面积高尔夫地块。Mayakoba 胜在度假村级标准 —— 也是走廊内最高的价格。"),
  ("可以远程建造吗？",
   "可以。每周图文与视频报告、进度视频会议、按核验进度付款，并全程代办许可与公证。"),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>普拉亚德尔卡门豪华别墅</h1>
<p class="lead">我们在<strong>普拉亚德尔卡门</strong>建造与翻新<strong>豪华别墅</strong> &mdash; 从 Playacar、Corasol 到 Mayakoba、Zazil-Ha 以及北部海岸带。设计、许可、施工、泳池、智能家居与软装，全部在同一份合同内完成。18年以上经验，196个项目，办公室设在 Corasol。</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>2026年普拉亚德尔卡门豪华别墅：</strong>每平米 $24,000&ndash;$45,000+ 比索，视区域与装修而定。我们办理索利达里达德施工许可、DRO、环评文件与社区设计委员会审批。</div>

<h2>豪华别墅建在哪里</h2>
<p>这里的豪宅不是一个地址，而是若干个，而且各自的施工方式不同：</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>区域</th><th>产品</th><th>施工上的差别</th></tr></thead><tbody>
<tr><td>Playacar 一期与二期</td><td>高尔夫与近海别墅，多为拆建或翻新</td><td>严格的设计委员会、树木保护、街道狭窄，约比基准高25%</td></tr>
<tr><td>Corasol</td><td>高尔夫旁大型别墅，建筑面积通常250&ndash;450平米</td><td>总体规划仍在建设：需确认红线处配套，约高30%</td></tr>
<tr><td>Mayakoba</td><td>潟湖与红树林旁的度假村级住宅</td><td>按邻近酒店标准的设计管控，约高42% &mdash; 走廊价格上限</td></tr>
<tr><td>Zazil-Ha 与 Coco Beach</td><td>市中心以北的近海别墅</td><td>全套海洋级规格；海边地块涉及联邦区</td></tr>
<tr><td>El Cielo、Selvamar、Playa Magna</td><td>配套与安保成熟的封闭社区</td><td>社区规约、市政流程直接、无联邦区问题</td></tr>
<tr><td>Playa del Secreto 与 Punta Bete</td><td>北段海滨别墅</td><td>ZOFEMAT、受保护沙丘、环评文件与海龟产卵规定</td></tr>
</tbody></table></div>

<h2 class="mt-4">2026年豪华别墅价格</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>区域 / 范围</th><th>比索/平米</th><th>美元/平米</th></tr></thead><tbody>
<tr><td>既有别墅整体翻新</td><td>$14,000&ndash;$26,000</td><td>$780&ndash;$1,445</td></tr>
<tr><td>成熟封闭社区高端新建</td><td>$24,000&ndash;$30,000</td><td>$1,335&ndash;$1,670</td></tr>
<tr><td>Playacar / Corasol</td><td>$26,000&ndash;$38,000</td><td>$1,445&ndash;$2,110</td></tr>
<tr><td>Mayakoba 与海滨</td><td>$35,000&ndash;$55,000+</td><td>$1,945&ndash;$3,055+</td></tr>
</tbody></table></div>
<p class="text-muted small">含结构、机电与装修。土地、定制泳池、成熟园林与家具另行报价。普拉亚德尔卡门标准建造参考价：$17,000&ndash;$21,000 比索/平米。</p>

<h2 class="mt-4">开工前需要知道的事</h2>
<ul>
<li><strong>索利达里达德市政厅。</strong>土地用途、许可、红线与 DRO。委托设计前请先核实地块的 COS、CUS、限高与退线 &mdash; 这几个数字决定您设想的别墅是否放得下。</li>
<li><strong>设计委员会。</strong>Playacar、Corasol 与 Mayakoba 审查高度、体量、材料、色彩、围墙与树木砍伐，并要求工人登记、限定时段与保证金。请在方案阶段提交。</li>
<li><strong>成熟树木。</strong>在 Playacar 与 Corasol 受保护且有价值：每棵砍伐都需论证，而在树间布局的方案审批更快，房子也更凉爽。</li>
<li><strong>地质勘察。</strong>喀斯特可能给出极好的承载力，两米外却是溶洞；钻孔覆盖实际建筑轮廓。</li>
<li><strong>海洋级规格。</strong>316不锈钢、阳极氧化或海洋级涂层铝材，外露构件加大混凝土保护层。</li>
<li><strong>屋面从方案阶段就按露台设计</strong>（在限高允许时）&mdash; 那是全屋最有价值的一平米。</li>
</ul>
<p>相关页面：<a href="/cancun-jianzhu-gongsi/">建筑公司</a> &middot; <a href="/zhuzhai-jianzao-playa-del-carmen/">普拉亚德尔卡门住宅建造</a> &middot; <a href="/blog-zh/playa-del-carmen-jianfang-chengben.html">建房成本</a> &middot; <a href="/haohua-bieshu-cancun/">坎昆豪华别墅</a></p>

<h2 class="mt-4">为什么选择 Recrea</h2>
<ul>
<li><strong>自2008年起196个以上项目</strong>，办公室位于 Corasol，在 Playacar、Corasol 与海岸带均有自有工程。</li>
<li><strong>固定总价合同</strong>，附分项预算，按核验进度付款，缺陷清单关闭后释放质保金。</li>
<li><strong>全部自有团队：</strong>建筑、结构、机电、木作、金属、泳池与室内。</li>
<li><strong>许可全程代办：</strong>市政许可、DRO、SEMA、ZOFEMAT 与社区委员会。</li>
<li><strong>远程建造：</strong>每周图文与视频报告。</li>
<li><strong>一年书面质保。</strong></li>
</ul>

<h2 class="mt-4">常见问题</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">在普拉亚德尔卡门建一栋豪华别墅要多少钱？</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">2026年为每平米 $24,000 至 $45,000+ 比索。Playacar 或 Corasol 的400平米别墅交钥匙约 $1,000 万&ndash;$1,600 万比索；Mayakoba 明显更高。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">你们在哪些区域建别墅？</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar 一期与二期、Corasol、Mayakoba、Zazil-Ha 与 Coco Beach，成熟社区 El Cielo、Selvamar、Playa Magna，以及北部的 Playa del Secreto 与 Punta Bete。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">需要哪些许可？</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">索利达里达德的土地用途、许可与红线，并需 DRO。有植被或近天坑的地块需环评文件，海边涉及联邦海域区，封闭社区另设设计委员会。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">工期需要多久？</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">施工10至16个月，另加2至4个月的设计与报批。在 Playacar、Corasol 和 Mayakoba 工期趋向上限。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">Playacar、Corasol 还是 Mayakoba？</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Playacar 胜在步行可达第五大道与成熟树冠；Corasol 胜在大面积高尔夫地块；Mayakoba 胜在度假村级标准，也是最高价格。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">可以远程建造吗？</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">可以。每周图文与视频报告、进度视频会议、按核验进度付款，并全程代办许可与公证。</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">准备在普拉亚德尔卡门开始您的别墅？</h3><p class="text-white-50 mb-4">196个以上项目。固定总价。48小时内出详细报价。</p><a href="https://wa.me/529844525333?text=您好！普拉亚德尔卡门豪华别墅报价" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>WhatsApp 获取报价</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18年以上</span><span class="trust-badge"><i class="bi bi-building"></i>196+ 项目</span><span class="trust-badge"><i class="bi bi-shield-check"></i>执照与 DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>一年质保</span></div>
</div></div></div></section>""",
}

if __name__ == "__main__":
    for lang in (sys.argv[1:] or sorted(P)):
        if lang not in P:
            print(f"  ! no content for {lang}"); continue
        w, d = rewrite(lang)
        print(f"  {w:5d} words  /{d}/")
