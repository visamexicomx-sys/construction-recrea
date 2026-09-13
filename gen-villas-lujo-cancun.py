#!/usr/bin/env python3
"""Build the city-level luxury-villa cluster for Cancún (6 languages).

Playa del Carmen had a city-level luxury-villa page in all six languages; Cancún
only had zone-level ones (Puerto Cancún, Zona Hotelera). This builds the missing
hub: one page per language that covers the premium areas of Cancún and links down
to the zone pages, rather than repeating them.

Chrome (head assets, top bar, nav, footer, review section) is lifted from the
corresponding Playa del Carmen page in the same language; the head meta, hreflang
cluster, schema and the whole main <section> are rewritten.
"""
import os, re, json

BASE = os.path.dirname(os.path.abspath(__file__))

DONOR = {
    "es": "villas-de-lujo-playa-del-carmen",
    "en": "luxury-villa-construction-playa-del-carmen",
    "de": "luxusvilla-bau-playa-del-carmen",
    "ru": "stroitelstvo-vill-playa-del-carmen",
    "fr": "construction-villa-luxe-playa-del-carmen",
    "zh": "haohua-bieshu-playa-del-carmen",
}
SLUG = {
    "es": "villas-de-lujo-cancun",
    "en": "luxury-villas-cancun",
    "de": "luxusvilla-bau-cancun",
    "ru": "stroitelstvo-vill-cancun",
    "fr": "construction-villa-luxe-cancun",
    "zh": "haohua-bieshu-cancun",
}
SITE = "https://construction-recrea.com/"
C = {}   # lang -> {"title","desc","keywords","body","faq":[(q,a)]}


def hreflang_block():
    out = ""
    for l in ["es", "en", "de", "ru", "fr", "zh"]:
        out += f'\n  <link rel="alternate" hreflang="{l}" href="{SITE}{SLUG[l]}/">'
    out += f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}{SLUG["en"]}/">'
    return out


def build(lang):
    c = C[lang]
    src = os.path.join(BASE, DONOR[lang], "index.html")
    h = open(src, encoding="utf-8").read()
    url = f"{SITE}{SLUG[lang]}/"

    # --- head meta
    h = re.sub(r"<title>.*?</title>", "<title>" + c["title"] + "</title>", h, count=1, flags=re.S)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        h = re.sub(r"(" + re.escape(attr) + r' content=")[^"]*(")',
                   lambda m: m.group(1) + c["desc"] + m.group(2), h, count=1)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        h = re.sub(r"(" + re.escape(attr) + r' content=")[^"]*(")',
                   lambda m: m.group(1) + c["title"] + m.group(2), h, count=1)
    h = re.sub(r'(name="keywords" content=")[^"]*(")',
               lambda m: m.group(1) + c["keywords"] + m.group(2), h, count=1)
    h = re.sub(r'(rel="canonical" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)
    h = re.sub(r'(property="og:url" content=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), h, count=1)

    # --- hreflang cluster replaced wholesale
    h = re.sub(r'(\n\s*<link rel="alternate" hreflang="[^"]+" href="[^"]+">)+', hreflang_block(), h, count=1)

    # --- schema: page url, Cancún coordinates, FAQ rebuilt from the visible questions
    h = h.replace(f'"url": "{SITE}{DONOR[lang]}/"', f'"url": "{url}"')
    h = re.sub(r'"geo": \{"@type": "GeoCoordinates", "latitude": [\d.\-]+, "longitude": [\d.\-]+\}',
               '"geo": {"@type": "GeoCoordinates", "latitude": 21.1619, "longitude": -86.8515}', h, count=1)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": re.sub(r"<[^>]+>", "", q).replace('"', "'"),
         "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a).replace('"', "'")}}
        for q, a in c["faq"]]}
    h = re.sub(r'<script type="application/ld\+json">\{"@context": "https://schema.org", "@type": "FAQPage".*?</script>',
               '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + "</script>",
               h, count=1, flags=re.S)

    # --- main content section
    start = h.index('<section class="py-5">')
    end = h.index("</section>", start) + len("</section>")
    h = h[:start] + c["body"] + h[end:]

    out_dir = os.path.join(BASE, SLUG[lang])
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(h)
    words = len(re.findall(r"[^\s<>]+", re.sub(r"<[^>]+>", " ", c["body"])))
    return words, SLUG[lang]


C["es"] = {
 "title": "Villas de Lujo en Cancún 2026 | Constructora | Recrea",
 "desc": "Construcción y remodelación de villas de lujo en Cancún: Puerto Cancún, Zona Hotelera, Isla Dorada y los fraccionamientos privados. Precios 2026 y permisos BJ.",
 "keywords": "villas de lujo cancun, constructora villas cancun, casas de lujo cancun, construir villa puerto cancun, villa zona hotelera cancun",
 "faq": [
  ("¿Cuánto cuesta construir una villa de lujo en Cancún?",
   "En 2026, de $25,000 a $45,000+ MXN/m² según acabados y zona. Una villa de 400 m² frente a marina o canal ronda los $12–18 millones MXN llave en mano. Contrato a precio fijo con presupuesto desglosado."),
  ("¿En qué zonas de Cancún construyen villas?",
   "Puerto Cancún (marina y golf TPC), Zona Hotelera e Isla Dorada (frente a canal y laguna), y los fraccionamientos privados del interior: Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres y Riviera Cancún."),
  ("¿Qué permisos se necesitan en Cancún?",
   "Uso de suelo, licencia de construcción y alineamiento del municipio de Benito Juárez, con Director Responsable de Obra. En Zona Hotelera e Isla Dorada se suman FONATUR y, frente a canal o mar, la zona federal marítimo terrestre (ZOFEMAT). Los fraccionamientos privados añaden su propio comité de diseño."),
  ("¿Cuánto tarda la obra?",
   "Una villa de lujo toma de 10 a 16 meses de obra, más 2–4 meses de proyecto y trámites. En fraccionamientos con horarios restringidos el plazo se va al extremo alto, y queda por escrito en el contrato."),
  ("¿Qué especificación exige el clima de Cancún?",
   "Inoxidable 316 en herrajes y barandales, aluminio anodizado o con recubrimiento marino, mayor recubrimiento de concreto en elementos expuestos y vidrio laminado o de impacto en fachadas expuestas. Es lo que separa una villa que envejece bien de una con manchas de óxido a los tres años."),
  ("¿Pueden construir a distancia si no vivo en México?",
   "Sí. Reportes semanales con foto y video, videollamadas de avance, pagos por avance verificado y gestión completa de permisos y notaría. Es como trabaja la mayoría de nuestros clientes extranjeros."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Villas de Lujo en Cancún</h1>
<p class="lead">Construimos y remodelamos <strong>villas de lujo en Cancún</strong> &mdash; de la marina de Puerto Cancún y los canales de Isla Dorada a los fraccionamientos privados del interior. Diseño, permisos, obra, alberca, domótica y mobiliario bajo un mismo techo. 18+ años y 196 proyectos en Quintana Roo.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Villa de lujo en Cancún 2026:</strong> $25,000&ndash;$45,000+ MXN/m² según zona y acabados. Gestionamos licencia de Benito Juárez, DRO y, donde aplica, FONATUR y ZOFEMAT.</div>

<h2>Dónde se Construyen Villas de Lujo en Cancún</h2>
<p>Cancún no es un solo mercado de lujo, sino cuatro, y cada uno se construye distinto:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Zona</th><th>Producto</th><th>Lo que cambia en obra</th></tr></thead><tbody>
<tr><td><a href="/villas-de-lujo-puerto-cancun/">Puerto Cancún</a></td><td>Villas frente a marina y campo de golf TPC</td><td>Reglamento del fraccionamiento, acceso controlado, ZOFEMAT en frente de marina</td></tr>
<tr><td><a href="/villas-de-lujo-zona-hotelera-cancun/">Zona Hotelera e Isla Dorada</a></td><td>Residencias frente a canal y laguna Nichupté</td><td>FONATUR, ZOFEMAT, especificación marina completa, acceso por la única vialidad</td></tr>
<tr><td><a href="/construccion-de-casas-lagos-del-sol-cancun/">Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres</a></td><td>Villas en fraccionamiento cerrado, lago o golf</td><td>Comité de diseño propio, sin zona federal, trámite BJ más directo</td></tr>
<tr><td><a href="/construccion-de-casas-riviera-cancun/">Riviera Cancún</a></td><td>Villas en corredor de golf hacia Puerto Morelos</td><td>El lote puede caer en Benito Juárez o en Puerto Morelos &mdash; se verifica primero</td></tr>
</tbody></table></div>

<h2 class="mt-4">Todo Para su Villa en Cancún</h2>
<div class="row g-3 my-2">
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-house-heart me-2" style="color:var(--accent)"></i>Villa Llave en Mano</h5><p class="small mb-0">De la mecánica de suelos a la entrega amueblada, con licencia de Benito Juárez y DRO incluidos.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-hammer me-2" style="color:var(--accent)"></i>Remodelación Integral</h5><p class="small mb-0">Villas y residencias de los noventa y dos miles: estructura, instalaciones, cocina, baños y fachada.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-water me-2" style="color:var(--accent)"></i>Albercas y Exteriores</h5><p class="small mb-0">Alberca desbordante, jacuzzi, roof garden y palapa, diseñados para vista a canal, laguna o golf.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-shield-check me-2" style="color:var(--accent)"></i>Especificación Marina</h5><p class="small mb-0">Inoxidable 316, aluminio anodizado y recubrimiento de concreto reforzado. Cancún es una isla de arena frente al mar.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-file-earmark-text me-2" style="color:var(--accent)"></i>Permisos y Comités</h5><p class="small mb-0">Licencia BJ, DRO, FONATUR y ZOFEMAT donde aplica, más la autorización del comité del fraccionamiento.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-lamp me-2" style="color:var(--accent)"></i>Interiorismo y Domótica</h5><p class="small mb-0">Cocina, carpintería a medida, iluminación, clima y seguridad integrados y listos para habitar o rentar.</p></div></div>
</div>

<h2 class="mt-4">Precios de Villas de Lujo en Cancún (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tipo</th><th>MXN/m²</th><th>USD/m²</th></tr></thead><tbody>
<tr><td>Remodelación integral de villa existente</td><td>$12,000&ndash;$20,000</td><td>$660&ndash;$1,100</td></tr>
<tr><td>Villa nueva premium en fraccionamiento interior</td><td>$22,000&ndash;$30,000</td><td>$1,220&ndash;$1,670</td></tr>
<tr><td>Villa nueva premium en Puerto Cancún</td><td>$25,000&ndash;$35,000</td><td>$1,380&ndash;$1,930</td></tr>
<tr><td>Ultra-lujo frente a canal, laguna o marina</td><td>$35,000&ndash;$45,000+</td><td>$1,930&ndash;$2,480+</td></tr>
</tbody></table></div>
<p class="text-muted small">Incluye estructura, instalaciones y acabados. Sin terreno, alberca de proyecto, jardinería madura ni mobiliario, que se cotizan aparte.</p>

<h2 class="mt-4">Lo que Debe Saber Antes de Construir en Cancún</h2>
<ul>
<li><strong>Municipio de Benito Juárez.</strong> Uso de suelo, licencia, alineamiento y Director Responsable de Obra. Para un lote residencial con servicios es de los trámites más predecibles del estado.</li>
<li><strong>Zona Hotelera e Isla Dorada.</strong> Ahí se suman FONATUR y la zona federal marítimo terrestre: confirme dónde termina realmente su propiedad y qué concesión existe antes de comprar.</li>
<li><strong>Comités de diseño.</strong> Puerto Cancún, Lagos del Sol, Villa Magna, Aqua y Residencial Cumbres revisan altura, materiales, color y bardas, y exigen trabajadores registrados, horarios y fianza. Presente en anteproyecto.</li>
<li><strong>Mecánica de suelos.</strong> El karst puede dar excelente capacidad de carga y una cavidad dos metros al lado; los sondeos se hacen sobre la huella real.</li>
<li><strong>Especificación marina, también tierra adentro.</strong> El aerosol salino llega varios kilómetros: herrajes y serpentines de condensadores duran mucho más en 316 y recubrimientos marinos.</li>
<li><strong>Vidrio.</strong> Laminado o con clasificación de impacto en fachadas expuestas: reduce la carga térmica que domina el recibo de CFE y mantiene la envolvente cerrada en temporada de huracanes.</li>
</ul>
<p>Guías útiles: <a href="/constructora-cancun/">Constructora en Cancún</a> · <a href="/permisos-de-construccion-cancun/">Permisos de construcción en Cancún</a> · <a href="/construccion-de-casas-cancun/">Construcción de casas en Cancún</a> · <a href="/construccion-villas-hoteles-cancun/">Villas y hoteles en Cancún</a> · <a href="/blog-es/cuanto-cuesta-construir-casa-cancun.html">¿Cuánto cuesta construir en Cancún?</a> · <a href="/villas-de-lujo-playa-del-carmen/">Villas de lujo en Playa del Carmen</a></p>

<h2 class="mt-4">Por Qué Elegir Recrea en Cancún</h2>
<ul>
<li><strong>196+ proyectos</strong> en Quintana Roo desde 2008, con obra propia en Cancún, Puerto Cancún y la Zona Hotelera.</li>
<li><strong>Contrato a precio fijo</strong> con presupuesto desglosado, pagos por avance verificado y retención hasta cerrar la lista de detalles.</li>
<li><strong>Todo en casa:</strong> arquitectura, estructura, instalaciones, carpintería, herrería, alberca e interiorismo &mdash; un solo responsable.</li>
<li><strong>Trámites completos:</strong> licencia BJ, DRO, FONATUR, ZOFEMAT y comité del fraccionamiento.</li>
<li><strong>Obra a distancia:</strong> reportes semanales con foto y video para propietarios en EE.UU., Canadá y Europa.</li>
<li><strong>Garantía por escrito</strong> de un año sobre la obra.</li>
</ul>

<h2 class="mt-4">Preguntas Frecuentes</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">¿Cuánto cuesta construir una villa de lujo en Cancún?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">En 2026, de $25,000 a $45,000+ MXN/m² según acabados y zona. Una villa de 400 m² frente a marina o canal ronda los $12&ndash;18 millones MXN llave en mano. Contrato a precio fijo con presupuesto desglosado.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">¿En qué zonas de Cancún construyen villas?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Puerto Cancún (marina y golf TPC), Zona Hotelera e Isla Dorada (frente a canal y laguna), y los fraccionamientos privados del interior: Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres y Riviera Cancún.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">¿Qué permisos se necesitan en Cancún?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Uso de suelo, licencia de construcción y alineamiento del municipio de Benito Juárez, con Director Responsable de Obra. En Zona Hotelera e Isla Dorada se suman FONATUR y, frente a canal o mar, la zona federal marítimo terrestre (ZOFEMAT). Los fraccionamientos privados añaden su propio comité de diseño.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">¿Cuánto tarda la obra?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Una villa de lujo toma de 10 a 16 meses de obra, más 2&ndash;4 meses de proyecto y trámites. En fraccionamientos con horarios restringidos el plazo se va al extremo alto, y queda por escrito en el contrato.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">¿Qué especificación exige el clima de Cancún?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Inoxidable 316 en herrajes y barandales, aluminio anodizado o con recubrimiento marino, mayor recubrimiento de concreto en elementos expuestos y vidrio laminado o de impacto en fachadas expuestas. Es lo que separa una villa que envejece bien de una con manchas de óxido a los tres años.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">¿Pueden construir a distancia si no vivo en México?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Sí. Reportes semanales con foto y video, videollamadas de avance, pagos por avance verificado y gestión completa de permisos y notaría. Es como trabaja la mayoría de nuestros clientes extranjeros.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">¿Listo para su villa en Cancún?</h3><p class="text-white-50 mb-4">196+ proyectos. Contrato a precio fijo. Cotización detallada en 48 horas.</p><a href="https://wa.me/529844525333?text=Hola!%20Quiero%20cotizar%20una%20villa%20de%20lujo%20en%20Canc%C3%BAn" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Cotizar por WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ Años</span><span class="trust-badge"><i class="bi bi-building"></i>196+ Proyectos</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Licencia y DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>Garantía 1 Año</span></div>
</div></div></div></section>""",
}

C["en"] = {
 "title": "Luxury Villas in Cancún 2026: Build &amp; Remodel | Recrea",
 "desc": "Luxury villa construction and remodeling in Cancún — Puerto Cancún, the Hotel Zone, Isla Dorada and the inland gated communities. 2026 prices and permit route.",
 "keywords": "luxury villas cancun, villa construction cancun, build villa puerto cancun, hotel zone cancun villa, luxury home builder cancun",
 "faq": [
  ("How much does a luxury villa cost to build in Cancún?",
   "In 2026, $25,000 to $45,000+ MXN/m² depending on the area and the finish level. A 400 m² villa on a canal or the marina lands around $12–18 million MXN turnkey. Fixed price with an itemised budget."),
  ("Which parts of Cancún do you build luxury villas in?",
   "Puerto Cancún (marina and TPC golf), the Hotel Zone and Isla Dorada (canal and lagoon frontage), and the inland gated communities: Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres and Riviera Cancún."),
  ("What permits are required in Cancún?",
   "Land use, construction licence and alignment from the municipality of Benito Juárez, with a Director Responsable de Obra. The Hotel Zone and Isla Dorada add FONATUR and, on canal or sea frontage, the federal maritime zone (ZOFEMAT). Gated communities add their own design committee."),
  ("How long does construction take?",
   "Ten to sixteen months on site for a luxury villa, plus two to four months of design and permits. In communities with restricted working hours the programme runs at the longer end, and the date goes into the contract."),
  ("What specification does the Cancún climate demand?",
   "316 stainless for fixings and railings, anodised or marine-grade coated aluminium, increased concrete cover on exposed elements, and laminated or impact-rated glazing on exposed elevations. That is what separates a villa that ages well from one with rust streaks by year three."),
  ("Can you build for me remotely from abroad?",
   "Yes. Weekly photo and video reports, progress video calls, payments against verified progress, and full handling of permits and notary. It is how most of our foreign clients build."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Luxury Villas in Cancún</h1>
<p class="lead">We build and remodel <strong>luxury villas in Canc&uacute;n</strong> &mdash; from the marina at Puerto Canc&uacute;n and the canals of Isla Dorada to the gated communities inland. Design, permits, construction, pool, home automation and furnishing under one contract. 18+ years and 196 projects in Quintana Roo.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Luxury villa in Canc&uacute;n, 2026:</strong> $25,000&ndash;$45,000+ MXN/m² depending on area and finish. We handle the Benito Ju&aacute;rez licence, the DRO and, where they apply, FONATUR and ZOFEMAT.</div>

<h2>Where Luxury Villas Get Built in Cancún</h2>
<p>Canc&uacute;n is not one luxury market but four, and each one builds differently:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Area</th><th>Product</th><th>What changes on site</th></tr></thead><tbody>
<tr><td><a href="/luxury-villas-puerto-cancun/">Puerto Canc&uacute;n</a></td><td>Villas facing the marina and the TPC golf course</td><td>Community rulebook, controlled access, ZOFEMAT on marina frontage</td></tr>
<tr><td><a href="/luxury-villas-hotel-zone-cancun/">Hotel Zone and Isla Dorada</a></td><td>Residences on the canals and the Nichupt&eacute; lagoon</td><td>FONATUR, ZOFEMAT, full marine specification, access along a single road</td></tr>
<tr><td><a href="/house-construction-lagos-del-sol-cancun/">Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres</a></td><td>Gated-community villas on lake or golf frontage</td><td>Each community's design committee, no federal zone, a more direct BJ permit route</td></tr>
<tr><td><a href="/house-construction-riviera-cancun/">Riviera Canc&uacute;n</a></td><td>Villas along the golf corridor toward Puerto Morelos</td><td>The lot may fall in Benito Ju&aacute;rez or in Puerto Morelos &mdash; that gets verified first</td></tr>
</tbody></table></div>

<h2 class="mt-4">Everything Your Cancún Villa Needs</h2>
<div class="row g-3 my-2">
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-house-heart me-2" style="color:var(--accent)"></i>Turnkey Villa</h5><p class="small mb-0">From the soil study to a furnished handover, with the Benito Ju&aacute;rez licence and DRO included.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-hammer me-2" style="color:var(--accent)"></i>Full Remodel</h5><p class="small mb-0">Nineties and 2000s villas taken back to structure: services, kitchen, bathrooms and facade.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-water me-2" style="color:var(--accent)"></i>Pools and Outdoor</h5><p class="small mb-0">Infinity pool, jacuzzi, roof terrace and palapa, designed around the canal, lagoon or golf view.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-shield-check me-2" style="color:var(--accent)"></i>Marine Specification</h5><p class="small mb-0">316 stainless, anodised aluminium and increased concrete cover. Canc&uacute;n is a sand bar facing open sea.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-file-earmark-text me-2" style="color:var(--accent)"></i>Permits and Committees</h5><p class="small mb-0">BJ licence, DRO, FONATUR and ZOFEMAT where they apply, plus the community's design approval.</p></div></div>
<div class="col-md-4"><div class="p-3 bg-light rounded h-100"><h5><i class="bi bi-lamp me-2" style="color:var(--accent)"></i>Interiors and Automation</h5><p class="small mb-0">Kitchen, bespoke joinery, lighting, climate and security integrated and ready to live in or rent.</p></div></div>
</div>

<h2 class="mt-4">Luxury Villa Prices in Cancún (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Scope</th><th>MXN/m²</th><th>USD/m²</th></tr></thead><tbody>
<tr><td>Full remodel of an existing villa</td><td>$12,000&ndash;$20,000</td><td>$660&ndash;$1,100</td></tr>
<tr><td>New premium villa, inland gated community</td><td>$22,000&ndash;$30,000</td><td>$1,220&ndash;$1,670</td></tr>
<tr><td>New premium villa, Puerto Canc&uacute;n</td><td>$25,000&ndash;$35,000</td><td>$1,380&ndash;$1,930</td></tr>
<tr><td>Ultra-luxury on canal, lagoon or marina frontage</td><td>$35,000&ndash;$45,000+</td><td>$1,930&ndash;$2,480+</td></tr>
</tbody></table></div>
<p class="text-muted small">Covers structure, installations and finishes. Land, a designed pool, mature landscaping and furniture are quoted separately.</p>

<h2 class="mt-4">What to Know Before Building in Cancún</h2>
<ul>
<li><strong>Municipality of Benito Ju&aacute;rez.</strong> Land use, licence, alignment and a Director Responsable de Obra. On a serviced residential lot it is one of the most predictable processes in the state.</li>
<li><strong>Hotel Zone and Isla Dorada.</strong> FONATUR and the federal maritime zone apply there &mdash; establish where your property actually ends and what concession exists before you buy.</li>
<li><strong>Design committees.</strong> Puerto Canc&uacute;n, Lagos del Sol, Villa Magna, Aqua and Residencial Cumbres review height, materials, colour and boundary walls, and require registered workers, restricted hours and a bond. Submit at concept stage.</li>
<li><strong>Soil study.</strong> The karst can give excellent bearing and a cavity two metres away; probes go across the actual footprint.</li>
<li><strong>Marine specification inland too.</strong> Salt aerosol reaches several kilometres &mdash; fixings and condenser coils last far longer in 316 and marine-grade coatings.</li>
<li><strong>Glazing.</strong> Laminated or impact-rated on exposed elevations: it cuts the cooling load that dominates the CFE bill and keeps the envelope closed in hurricane season.</li>
</ul>
<p>Useful guides: <a href="/construction-company-cancun/">Construction company in Canc&uacute;n</a> &middot; <a href="/construction-permits-cancun/">Construction permits in Canc&uacute;n</a> &middot; <a href="/house-construction-cancun/">House construction in Canc&uacute;n</a> &middot; <a href="/villa-hotel-construction-cancun/">Villas and hotels in Canc&uacute;n</a> &middot; <a href="/blog/cost-to-build-house-cancun.html">What it costs to build in Canc&uacute;n</a> &middot; <a href="/luxury-villa-construction-playa-del-carmen/">Luxury villas in Playa del Carmen</a></p>

<h2 class="mt-4">Why Build with Recrea in Cancún</h2>
<ul>
<li><strong>196+ projects</strong> across Quintana Roo since 2008, including work in Canc&uacute;n, Puerto Canc&uacute;n and the Hotel Zone.</li>
<li><strong>Fixed-price contract</strong> with an itemised budget, payments against verified progress and retention held until the snag list closes.</li>
<li><strong>Everything in house:</strong> architecture, structure, installations, carpentry, metalwork, pool and interiors &mdash; one party accountable.</li>
<li><strong>Full permit handling:</strong> BJ licence, DRO, FONATUR, ZOFEMAT and the community design committee.</li>
<li><strong>Remote construction:</strong> weekly photo and video reporting for owners in the US, Canada and Europe.</li>
<li><strong>One-year written warranty</strong> on the work.</li>
</ul>

<h2 class="mt-4">Frequently Asked Questions</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">How much does a luxury villa cost to build in Canc&uacute;n?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">In 2026, $25,000 to $45,000+ MXN/m² depending on the area and the finish level. A 400 m² villa on a canal or the marina lands around $12&ndash;18 million MXN turnkey. Fixed price with an itemised budget.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">Which parts of Canc&uacute;n do you build luxury villas in?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Puerto Canc&uacute;n (marina and TPC golf), the Hotel Zone and Isla Dorada (canal and lagoon frontage), and the inland gated communities: Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres and Riviera Canc&uacute;n.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">What permits are required in Canc&uacute;n?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Land use, construction licence and alignment from the municipality of Benito Ju&aacute;rez, with a Director Responsable de Obra. The Hotel Zone and Isla Dorada add FONATUR and, on canal or sea frontage, the federal maritime zone (ZOFEMAT). Gated communities add their own design committee.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">How long does construction take?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Ten to sixteen months on site for a luxury villa, plus two to four months of design and permits. In communities with restricted working hours the programme runs at the longer end, and the date goes into the contract.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">What specification does the Canc&uacute;n climate demand?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">316 stainless for fixings and railings, anodised or marine-grade coated aluminium, increased concrete cover on exposed elements, and laminated or impact-rated glazing on exposed elevations. That is what separates a villa that ages well from one with rust streaks by year three.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">Can you build for me remotely from abroad?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Yes. Weekly photo and video reports, progress video calls, payments against verified progress, and full handling of permits and notary. It is how most of our foreign clients build.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">Ready to build your Canc&uacute;n villa?</h3><p class="text-white-50 mb-4">196+ projects completed. Fixed-price contracts. Detailed quote within 48 hours.</p><a href="https://wa.me/529844525333?text=Hello!%20I%20want%20a%20quote%20for%20a%20luxury%20villa%20in%20Cancun" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Get a Quote on WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ Years</span><span class="trust-badge"><i class="bi bi-building"></i>196+ Projects</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Licensed &amp; DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>1-Year Warranty</span></div>
</div></div></div></section>""",
}

C["de"] = {
 "title": "Luxusvillen in Cancún 2026: Bau &amp; Sanierung | Recrea",
 "desc": "Luxusvillen in Cancún bauen und sanieren — Puerto Cancún, Hotelzone, Isla Dorada und die Wohnanlagen im Inland. Preise 2026, Genehmigungen und Marine-Spezifikation.",
 "keywords": "luxusvilla cancun, villa bauen cancun, hausbau puerto cancun, luxusimmobilie cancun, bauunternehmen villa cancun",
 "faq": [
  ("Was kostet eine Luxusvilla in Cancún?",
   "2026 zwischen $25,000 und $45,000+ MXN/m², je nach Lage und Ausbau. Eine 400-m²-Villa am Kanal oder an der Marina liegt schlüsselfertig bei rund $12–18 Mio. MXN. Festpreis mit Positionsbudget."),
  ("In welchen Lagen von Cancún bauen Sie Villen?",
   "Puerto Cancún (Marina und TPC-Golfplatz), Hotelzone und Isla Dorada (Kanal- und Lagunenlage) sowie die geschlossenen Wohnanlagen im Inland: Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres und Riviera Cancún."),
  ("Welche Genehmigungen braucht man in Cancún?",
   "Nutzungszertifikat, Baugenehmigung und Fluchtlinie der Gemeinde Benito Juárez mit einem Director Responsable de Obra. In Hotelzone und Isla Dorada kommen FONATUR und, bei Kanal- oder Meerfront, die Bundesküstenzone ZOFEMAT hinzu. Wohnanlagen haben zusätzlich einen eigenen Gestaltungsbeirat."),
  ("Wie lange dauert der Bau?",
   "Zehn bis sechzehn Monate Bauzeit für eine Luxusvilla, plus zwei bis vier Monate Planung und Genehmigungen. In Anlagen mit eingeschränkten Arbeitszeiten liegt der Termin am oberen Ende und steht im Vertrag."),
  ("Welche Spezifikation verlangt das Klima in Cancún?",
   "316er Edelstahl bei Befestigungen und Geländern, eloxiertes oder marinebeschichtetes Aluminium, größere Betondeckung an exponierten Bauteilen und Verbund- oder schlagfestes Glas an exponierten Fassaden. Das unterscheidet eine Villa, die gut altert, von einer mit Rostfahnen im dritten Jahr."),
  ("Können Sie aus dem Ausland für mich bauen?",
   "Ja. Wöchentliche Foto- und Videoberichte, Fortschritts-Videocalls, Zahlungen nach geprüftem Baufortschritt und die komplette Abwicklung von Genehmigungen und Notar. So bauen die meisten unserer ausländischen Kunden."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Luxusvillen in Canc&uacute;n</h1>
<p class="lead">Wir bauen und sanieren <strong>Luxusvillen in Canc&uacute;n</strong> &mdash; von der Marina in Puerto Canc&uacute;n und den Kan&auml;len von Isla Dorada bis zu den geschlossenen Wohnanlagen im Inland. Planung, Genehmigungen, Bau, Pool, Smart Home und Ausstattung aus einer Hand. 18+ Jahre, 196 Projekte in Quintana Roo.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Luxusvilla in Canc&uacute;n 2026:</strong> $25.000&ndash;$45.000+ MXN/m² je nach Lage und Ausbau. Wir &uuml;bernehmen Baugenehmigung in Benito Ju&aacute;rez, DRO und, wo einschl&auml;gig, FONATUR und ZOFEMAT.</div>

<h2>Wo in Cancún Luxusvillen entstehen</h2>
<p>Canc&uacute;n ist nicht ein Luxusmarkt, sondern vier &mdash; und jeder wird anders gebaut:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Lage</th><th>Produkt</th><th>Was sich auf der Baustelle ändert</th></tr></thead><tbody>
<tr><td>Puerto Canc&uacute;n</td><td>Villen an Marina und TPC-Golfplatz</td><td>Regelwerk der Anlage, kontrollierter Zugang, ZOFEMAT an der Marina</td></tr>
<tr><td>Hotelzone und Isla Dorada</td><td>Residenzen an Kan&auml;len und der Nichupt&eacute;-Lagune</td><td>FONATUR, ZOFEMAT, volle Marine-Spezifikation, Zufahrt &uuml;ber eine einzige Stra&szlig;e</td></tr>
<tr><td>Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres</td><td>Villen in geschlossenen Anlagen an See oder Golfplatz</td><td>Eigener Gestaltungsbeirat, keine Bundeszone, direkterer Weg bei BJ</td></tr>
<tr><td>Riviera Canc&uacute;n</td><td>Villen im Golfkorridor Richtung Puerto Morelos</td><td>Das Grundst&uuml;ck kann in Benito Ju&aacute;rez oder in Puerto Morelos liegen &mdash; das wird zuerst gepr&uuml;ft</td></tr>
</tbody></table></div>

<h2 class="mt-4">Preise für Luxusvillen in Cancún (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Umfang</th><th>MXN/m²</th><th>USD/m²</th></tr></thead><tbody>
<tr><td>Kernsanierung einer bestehenden Villa</td><td>$12.000&ndash;$20.000</td><td>$660&ndash;$1.100</td></tr>
<tr><td>Neubau Premium, Anlage im Inland</td><td>$22.000&ndash;$30.000</td><td>$1.220&ndash;$1.670</td></tr>
<tr><td>Neubau Premium, Puerto Canc&uacute;n</td><td>$25.000&ndash;$35.000</td><td>$1.380&ndash;$1.930</td></tr>
<tr><td>Ultra-Luxus an Kanal, Lagune oder Marina</td><td>$35.000&ndash;$45.000+</td><td>$1.930&ndash;$2.480+</td></tr>
</tbody></table></div>
<p class="text-muted small">Enth&auml;lt Rohbau, Installationen und Ausbau. Grundst&uuml;ck, geplanter Pool, ausgewachsene Bepflanzung und M&ouml;bel werden separat kalkuliert.</p>

<h2 class="mt-4">Was Sie vor dem Bau in Cancún wissen sollten</h2>
<ul>
<li><strong>Gemeinde Benito Ju&aacute;rez.</strong> Nutzung, Genehmigung, Fluchtlinie und Director Responsable de Obra. Auf einem erschlossenen Wohngrundst&uuml;ck einer der berechenbarsten Abl&auml;ufe im Bundesstaat.</li>
<li><strong>Hotelzone und Isla Dorada.</strong> Dort gelten FONATUR und die Bundesk&uuml;stenzone &mdash; kl&auml;ren Sie vor dem Kauf, wo Ihr Grundst&uuml;ck tats&auml;chlich endet und welche Konzession besteht.</li>
<li><strong>Gestaltungsbeir&auml;te.</strong> Puerto Canc&uacute;n, Lagos del Sol, Villa Magna, Aqua und Residencial Cumbres pr&uuml;fen H&ouml;he, Materialien, Farbe und Einfriedungen und verlangen registrierte Arbeiter, Arbeitszeiten und eine Kaution. In der Entwurfsphase einreichen.</li>
<li><strong>Bodengutachten.</strong> Der Karst kann hervorragende Tragf&auml;higkeit bieten und zwei Meter weiter einen Hohlraum; sondiert wird &uuml;ber der tats&auml;chlichen Grundfl&auml;che.</li>
<li><strong>Marine-Spezifikation auch im Inland.</strong> Salzaerosol reicht mehrere Kilometer &mdash; Befestigungen und Verfl&uuml;ssigerlamellen halten in 316 und Marine-Beschichtung deutlich l&auml;nger.</li>
<li><strong>Verglasung.</strong> Verbund- oder schlagfest an exponierten Fassaden: senkt die K&uuml;hllast, die die CFE-Rechnung dominiert, und h&auml;lt die Geb&auml;udeh&uuml;lle in der Hurrikansaison geschlossen.</li>
</ul>
<p>N&uuml;tzliche Seiten: <a href="/bauunternehmen-cancun/">Bauunternehmen in Canc&uacute;n</a> &middot; <a href="/hausbau-cancun/">Hausbau in Canc&uacute;n</a> &middot; <a href="/villen-hotelbau-cancun/">Villen- und Hotelbau in Canc&uacute;n</a> &middot; <a href="/blog-de/hausbau-kosten-cancun.html">Hausbau-Kosten in Canc&uacute;n</a> &middot; <a href="/luxusvilla-bau-playa-del-carmen/">Luxusvillen in Playa del Carmen</a></p>

<h2 class="mt-4">Warum Recrea in Cancún</h2>
<ul>
<li><strong>196+ Projekte</strong> in Quintana Roo seit 2008, darunter Canc&uacute;n, Puerto Canc&uacute;n und die Hotelzone.</li>
<li><strong>Festpreisvertrag</strong> mit Positionsbudget, Zahlungen nach gepr&uuml;ftem Fortschritt und Einbehalt bis zur Abnahme.</li>
<li><strong>Alles im Haus:</strong> Architektur, Statik, Installationen, Tischlerei, Metallbau, Pool und Innenausbau &mdash; ein Verantwortlicher.</li>
<li><strong>Komplette Genehmigungen:</strong> BJ-Lizenz, DRO, FONATUR, ZOFEMAT und Gestaltungsbeirat.</li>
<li><strong>Bauen aus der Ferne:</strong> w&ouml;chentliche Foto- und Videoberichte f&uuml;r Eigent&uuml;mer in Europa und Nordamerika.</li>
<li><strong>Ein Jahr schriftliche Gew&auml;hrleistung.</strong></li>
</ul>

<h2 class="mt-4">Häufige Fragen</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">Was kostet eine Luxusvilla in Canc&uacute;n?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">2026 zwischen $25.000 und $45.000+ MXN/m², je nach Lage und Ausbau. Eine 400-m²-Villa am Kanal oder an der Marina liegt schl&uuml;sselfertig bei rund $12&ndash;18 Mio. MXN. Festpreis mit Positionsbudget.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">In welchen Lagen von Canc&uacute;n bauen Sie Villen?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Puerto Canc&uacute;n (Marina und TPC-Golfplatz), Hotelzone und Isla Dorada (Kanal- und Lagunenlage) sowie die geschlossenen Wohnanlagen im Inland: Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres und Riviera Canc&uacute;n.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">Welche Genehmigungen braucht man in Canc&uacute;n?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Nutzungszertifikat, Baugenehmigung und Fluchtlinie der Gemeinde Benito Ju&aacute;rez mit einem Director Responsable de Obra. In Hotelzone und Isla Dorada kommen FONATUR und, bei Kanal- oder Meerfront, die Bundesk&uuml;stenzone ZOFEMAT hinzu. Wohnanlagen haben zus&auml;tzlich einen eigenen Gestaltungsbeirat.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">Wie lange dauert der Bau?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Zehn bis sechzehn Monate Bauzeit f&uuml;r eine Luxusvilla, plus zwei bis vier Monate Planung und Genehmigungen. In Anlagen mit eingeschr&auml;nkten Arbeitszeiten liegt der Termin am oberen Ende und steht im Vertrag.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">Welche Spezifikation verlangt das Klima?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">316er Edelstahl bei Befestigungen und Gel&auml;ndern, eloxiertes oder marinebeschichtetes Aluminium, gr&ouml;&szlig;ere Betondeckung an exponierten Bauteilen und Verbund- oder schlagfestes Glas an exponierten Fassaden.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">K&ouml;nnen Sie aus dem Ausland f&uuml;r mich bauen?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Ja. W&ouml;chentliche Foto- und Videoberichte, Fortschritts-Videocalls, Zahlungen nach gepr&uuml;ftem Baufortschritt und die komplette Abwicklung von Genehmigungen und Notar.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">Bereit f&uuml;r Ihre Villa in Canc&uacute;n?</h3><p class="text-white-50 mb-4">196+ Projekte. Festpreis. Detailliertes Angebot in 48 Stunden.</p><a href="https://wa.me/529844525333?text=Hallo!%20Angebot%20Luxusvilla%20Cancun" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Angebot per WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ Jahre</span><span class="trust-badge"><i class="bi bi-building"></i>196+ Projekte</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Lizenz &amp; DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>1 Jahr Garantie</span></div>
</div></div></div></section>""",
}

C["ru"] = {
 "title": "Виллы Люкс в Канкуне 2026: Строительство | Recrea",
 "desc": "Строительство и реконструкция вилл люкс в Канкуне: Пуэрто-Канкун, Зона Отелера, Исла-Дорада и закрытые посёлки. Цены 2026, разрешения и морская спецификация.",
 "keywords": "виллы люкс канкун, построить виллу канкун, строительство вилл пуэрто канкун, элитная недвижимость канкун, застройщик вилл канкун",
 "faq": [
  ("Сколько стоит построить виллу люкс в Канкуне?",
   "В 2026 году от $25,000 до $45,000+ MXN/м² в зависимости от района и отделки. Вилла 400 м² у канала или марины обходится примерно в $12–18 млн MXN под ключ. Фиксированная цена с постатейной сметой."),
  ("В каких районах Канкуна вы строите виллы?",
   "Пуэрто-Канкун (марина и поле для гольфа TPC), Зона Отелера и Исла-Дорада (каналы и лагуна), а также закрытые посёлки вглубь материка: Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres и Riviera Cancún."),
  ("Какие разрешения нужны в Канкуне?",
   "Назначение земли, лицензия на строительство и выравнивание в муниципалитете Бенито Хуарес, с Director Responsable de Obra. В Зона Отелера и на Исла-Дорада добавляются FONATUR и, при выходе к каналу или морю, федеральная морская зона ZOFEMAT. В закрытых посёлках есть собственный архитектурный комитет."),
  ("Сколько идёт стройка?",
   "Вилла люкс строится 10–16 месяцев, плюс 2–4 месяца на проект и разрешения. В посёлках с ограниченными часами работ срок уходит к верхней границе и фиксируется в договоре."),
  ("Какую спецификацию требует климат Канкуна?",
   "Нержавейка 316 в крепеже и ограждениях, анодированный или с морским покрытием алюминий, увеличенный защитный слой бетона на открытых элементах и триплекс либо ударостойкое остекление на открытых фасадах."),
  ("Можно ли строить дистанционно из другой страны?",
   "Да. Еженедельные отчёты с фото и видео, видеозвонки по ходу работ, оплата по проверенному факту и полное ведение разрешений и нотариата."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Виллы Люкс в Канкуне</h1>
<p class="lead">Строим и реконструируем <strong>виллы люкс в Канкуне</strong> &mdash; от марины Пуэрто-Канкуна и каналов Исла-Дорада до закрытых посёлков вглубь материка. Проект, разрешения, стройка, бассейн, автоматизация и меблировка по одному договору. 18+ лет и 196 проектов в Кинтана-Роо.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Вилла люкс в Канкуне, 2026:</strong> $25,000&ndash;$45,000+ MXN/м² в зависимости от района и отделки. Берём на себя лицензию Бенито Хуарес, DRO и, где применимо, FONATUR и ZOFEMAT.</div>

<h2>Где в Канкуне строят виллы люкс</h2>
<p>Канкун &mdash; это не один люксовый рынок, а четыре, и строятся они по-разному:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Район</th><th>Продукт</th><th>Что меняется на стройке</th></tr></thead><tbody>
<tr><td>Пуэрто-Канкун</td><td>Виллы у марины и поля для гольфа TPC</td><td>Регламент посёлка, контролируемый въезд, ZOFEMAT со стороны марины</td></tr>
<tr><td>Зона Отелера и Исла-Дорада</td><td>Резиденции у каналов и лагуны Ничупте</td><td>FONATUR, ZOFEMAT, полная морская спецификация, единственная подъездная дорога</td></tr>
<tr><td>Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres</td><td>Виллы в закрытых посёлках у озера или поля для гольфа</td><td>Собственный архитектурный комитет, без федеральной зоны, более прямой путь в BJ</td></tr>
<tr><td>Riviera Cancún</td><td>Виллы в гольф-коридоре в сторону Пуэрто-Морелоса</td><td>Участок может относиться к Бенито Хуарес или к Пуэрто-Морелосу &mdash; это проверяется первым делом</td></tr>
</tbody></table></div>

<h2 class="mt-4">Цены на виллы люкс в Канкуне (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Объём работ</th><th>MXN/м²</th><th>USD/м²</th></tr></thead><tbody>
<tr><td>Полная реконструкция существующей виллы</td><td>$12,000&ndash;$20,000</td><td>$660&ndash;$1,100</td></tr>
<tr><td>Новая вилла премиум, посёлок вглубь материка</td><td>$22,000&ndash;$30,000</td><td>$1,220&ndash;$1,670</td></tr>
<tr><td>Новая вилла премиум, Пуэрто-Канкун</td><td>$25,000&ndash;$35,000</td><td>$1,380&ndash;$1,930</td></tr>
<tr><td>Ультра-люкс у канала, лагуны или марины</td><td>$35,000&ndash;$45,000+</td><td>$1,930&ndash;$2,480+</td></tr>
</tbody></table></div>
<p class="text-muted small">Включает конструктив, инженерию и отделку. Земля, проектный бассейн, взрослое озеленение и мебель считаются отдельно.</p>

<h2 class="mt-4">Что нужно знать до начала стройки в Канкуне</h2>
<ul>
<li><strong>Муниципалитет Бенито Хуарес.</strong> Назначение земли, лицензия, выравнивание и Director Responsable de Obra. Для обеспеченного коммуникациями участка это одна из самых предсказуемых процедур в штате.</li>
<li><strong>Зона Отелера и Исла-Дорада.</strong> Там действуют FONATUR и федеральная морская зона: до покупки выясните, где реально заканчивается участок и какая концессия существует.</li>
<li><strong>Архитектурные комитеты.</strong> Пуэрто-Канкун, Lagos del Sol, Villa Magna, Aqua и Residencial Cumbres проверяют высоту, материалы, цвет и ограждения, требуют регистрации рабочих, соблюдения часов и залога. Подавайте на стадии эскиза.</li>
<li><strong>Геология.</strong> Карст может дать отличное основание и полость в двух метрах рядом; скважины делаются по фактическому пятну застройки.</li>
<li><strong>Морская спецификация и вглубь материка.</strong> Солевой аэрозоль доходит на несколько километров &mdash; крепёж и теплообменники служат заметно дольше в 316 и морских покрытиях.</li>
<li><strong>Остекление.</strong> Триплекс или ударостойкое на открытых фасадах: снижает тепловую нагрузку, определяющую счёт CFE, и сохраняет контур здания закрытым в сезон ураганов.</li>
</ul>
<p>Полезные страницы: <a href="/stroitelnaya-kompaniya-cancun/">Строительная компания в Канкуне</a> &middot; <a href="/stroitelstvo-domov-cancun/">Строительство домов в Канкуне</a> &middot; <a href="/stroitelstvo-vill-i-otelei-cancun/">Виллы и отели в Канкуне</a> &middot; <a href="/blog-ru/skolko-stoit-postroit-dom-cancun.html">Сколько стоит построить дом в Канкуне</a> &middot; <a href="/stroitelstvo-vill-playa-del-carmen/">Виллы люкс в Плая-дель-Кармен</a></p>

<h2 class="mt-4">Почему Recrea в Канкуне</h2>
<ul>
<li><strong>196+ проектов</strong> в Кинтана-Роо с 2008 года, включая Канкун, Пуэрто-Канкун и Зона Отелера.</li>
<li><strong>Договор с фиксированной ценой</strong> и постатейной сметой, оплата по проверенному факту, удержание до закрытия списка замечаний.</li>
<li><strong>Всё внутри компании:</strong> архитектура, конструктив, инженерия, столярка, металл, бассейн и интерьер &mdash; один ответственный.</li>
<li><strong>Разрешения под ключ:</strong> лицензия BJ, DRO, FONATUR, ZOFEMAT и комитет посёлка.</li>
<li><strong>Стройка дистанционно:</strong> еженедельные отчёты с фото и видео для владельцев из России, Европы и Северной Америки.</li>
<li><strong>Год письменной гарантии</strong> на работы.</li>
</ul>

<h2 class="mt-4">Частые вопросы</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">Сколько стоит построить виллу люкс в Канкуне?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">В 2026 году от $25,000 до $45,000+ MXN/м² в зависимости от района и отделки. Вилла 400 м² у канала или марины обходится примерно в $12&ndash;18 млн MXN под ключ.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">В каких районах Канкуна вы строите виллы?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Пуэрто-Канкун, Зона Отелера и Исла-Дорада, а также закрытые посёлки вглубь материка: Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres и Riviera Cancún.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">Какие разрешения нужны в Канкуне?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Назначение земли, лицензия и выравнивание в муниципалитете Бенито Хуарес с DRO. В Зона Отелера и на Исла-Дорада добавляются FONATUR и федеральная морская зона ZOFEMAT, а в закрытых посёлках &mdash; собственный архитектурный комитет.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">Сколько идёт стройка?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">10&ndash;16 месяцев, плюс 2&ndash;4 месяца на проект и разрешения. В посёлках с ограниченными часами срок уходит к верхней границе и фиксируется в договоре.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">Какую спецификацию требует климат?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Нержавейка 316, анодированный или с морским покрытием алюминий, увеличенный защитный слой бетона и триплекс либо ударостойкое остекление на открытых фасадах.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">Можно ли строить дистанционно?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Да. Еженедельные отчёты с фото и видео, видеозвонки, оплата по проверенному факту и полное ведение разрешений и нотариата.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">Готовы начать виллу в Канкуне?</h3><p class="text-white-50 mb-4">196+ проектов. Фиксированная цена. Детальная смета за 48 часов.</p><a href="https://wa.me/529844525333?text=Здравствуйте!%20Смета%20на%20виллу%20в%20Канкуне" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Запросить в WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ лет</span><span class="trust-badge"><i class="bi bi-building"></i>196+ проектов</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Лицензия и DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>Гарантия 1 год</span></div>
</div></div></div></section>""",
}

C["fr"] = {
 "title": "Villas de Luxe à Cancún 2026 : Construction | Recrea",
 "desc": "Construction et rénovation de villas de luxe à Cancún : Puerto Cancún, Zone Hôtelière, Isla Dorada et résidences fermées. Prix 2026, permis et spécification marine.",
 "keywords": "villas de luxe cancun, construction villa cancun, constructeur villa puerto cancun, immobilier luxe cancun, villa zone hoteliere cancun",
 "faq": [
  ("Combien coûte une villa de luxe à Cancún ?",
   "En 2026, de $25,000 à $45,000+ MXN/m² selon le secteur et la finition. Une villa de 400 m² sur canal ou marina revient à environ $12–18 millions MXN clé en main. Prix ferme avec budget détaillé."),
  ("Dans quels secteurs de Cancún construisez-vous des villas ?",
   "Puerto Cancún (marina et golf TPC), la Zone Hôtelière et Isla Dorada (front de canal et de lagune), ainsi que les résidences fermées à l'intérieur : Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres et Riviera Cancún."),
  ("Quels permis sont nécessaires à Cancún ?",
   "Usage du sol, permis de construire et alignement auprès de la municipalité de Benito Juárez, avec un Director Responsable de Obra. La Zone Hôtelière et Isla Dorada ajoutent FONATUR et, sur front de canal ou de mer, la zone fédérale maritime (ZOFEMAT). Les résidences fermées ont leur propre comité d'architecture."),
  ("Combien de temps dure le chantier ?",
   "Dix à seize mois de chantier pour une villa de luxe, plus deux à quatre mois de conception et de permis. Dans les résidences aux horaires restreints, le délai se situe en haut de la fourchette et figure au contrat."),
  ("Quelle spécification impose le climat de Cancún ?",
   "Inox 316 pour les fixations et garde-corps, aluminium anodisé ou à revêtement marin, enrobage de béton augmenté sur les éléments exposés, et vitrage feuilleté ou classé impact sur les façades exposées."),
  ("Pouvez-vous construire à distance depuis l'étranger ?",
   "Oui. Rapports hebdomadaires photo et vidéo, visioconférences d'avancement, paiements à l'avancement vérifié et gestion complète des permis et du notaire."),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>Villas de Luxe &agrave; Canc&uacute;n</h1>
<p class="lead">Nous construisons et r&eacute;novons des <strong>villas de luxe &agrave; Canc&uacute;n</strong> &mdash; de la marina de Puerto Canc&uacute;n et des canaux d'Isla Dorada aux r&eacute;sidences ferm&eacute;es de l'int&eacute;rieur. Conception, permis, chantier, piscine, domotique et ameublement sous un seul contrat. 18+ ans et 196 projets au Quintana Roo.</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>Villa de luxe &agrave; Canc&uacute;n, 2026 :</strong> $25,000&ndash;$45,000+ MXN/m² selon le secteur et la finition. Nous prenons en charge le permis de Benito Ju&aacute;rez, le DRO et, le cas &eacute;ch&eacute;ant, FONATUR et ZOFEMAT.</div>

<h2>Où se construisent les villas de luxe à Cancún</h2>
<p>Canc&uacute;n n'est pas un march&eacute; de luxe mais quatre, et chacun se construit diff&eacute;remment :</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Secteur</th><th>Produit</th><th>Ce qui change sur le chantier</th></tr></thead><tbody>
<tr><td>Puerto Canc&uacute;n</td><td>Villas face &agrave; la marina et au golf TPC</td><td>R&egrave;glement de la r&eacute;sidence, acc&egrave;s contr&ocirc;l&eacute;, ZOFEMAT c&ocirc;t&eacute; marina</td></tr>
<tr><td>Zone H&ocirc;teli&egrave;re et Isla Dorada</td><td>R&eacute;sidences sur les canaux et la lagune Nichupt&eacute;</td><td>FONATUR, ZOFEMAT, sp&eacute;cification marine int&eacute;grale, acc&egrave;s par une voie unique</td></tr>
<tr><td>Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres</td><td>Villas en r&eacute;sidence ferm&eacute;e, front de lac ou de golf</td><td>Comit&eacute; d'architecture propre, pas de zone f&eacute;d&eacute;rale, parcours BJ plus direct</td></tr>
<tr><td>Riviera Canc&uacute;n</td><td>Villas dans le corridor de golf vers Puerto Morelos</td><td>La parcelle peut relever de Benito Ju&aacute;rez ou de Puerto Morelos &mdash; cela se v&eacute;rifie d'abord</td></tr>
</tbody></table></div>

<h2 class="mt-4">Prix des villas de luxe à Cancún (2026)</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Prestation</th><th>MXN/m²</th><th>USD/m²</th></tr></thead><tbody>
<tr><td>R&eacute;novation lourde d'une villa existante</td><td>$12,000&ndash;$20,000</td><td>$660&ndash;$1,100</td></tr>
<tr><td>Villa neuve premium, r&eacute;sidence int&eacute;rieure</td><td>$22,000&ndash;$30,000</td><td>$1,220&ndash;$1,670</td></tr>
<tr><td>Villa neuve premium, Puerto Canc&uacute;n</td><td>$25,000&ndash;$35,000</td><td>$1,380&ndash;$1,930</td></tr>
<tr><td>Ultra-luxe sur canal, lagune ou marina</td><td>$35,000&ndash;$45,000+</td><td>$1,930&ndash;$2,480+</td></tr>
</tbody></table></div>
<p class="text-muted small">Comprend structure, installations et finitions. Terrain, piscine con&ccedil;ue, plantations matures et mobilier sont chiffr&eacute;s &agrave; part.</p>

<h2 class="mt-4">À savoir avant de construire à Cancún</h2>
<ul>
<li><strong>Municipalit&eacute; de Benito Ju&aacute;rez.</strong> Usage du sol, permis, alignement et Director Responsable de Obra. Sur une parcelle r&eacute;sidentielle viabilis&eacute;e, c'est l'un des parcours les plus pr&eacute;visibles de l'&Eacute;tat.</li>
<li><strong>Zone H&ocirc;teli&egrave;re et Isla Dorada.</strong> FONATUR et la zone f&eacute;d&eacute;rale maritime s'y appliquent &mdash; &eacute;tablissez avant l'achat o&ugrave; s'arr&ecirc;te r&eacute;ellement votre propri&eacute;t&eacute; et quelle concession existe.</li>
<li><strong>Comit&eacute;s d'architecture.</strong> Puerto Canc&uacute;n, Lagos del Sol, Villa Magna, Aqua et Residencial Cumbres examinent hauteur, mat&eacute;riaux, couleur et cl&ocirc;tures, et exigent ouvriers enregistr&eacute;s, horaires et caution. D&eacute;posez au stade avant-projet.</li>
<li><strong>&Eacute;tude de sol.</strong> Le karst peut offrir une excellente portance et une cavit&eacute; deux m&egrave;tres plus loin ; les sondages se font sur l'emprise r&eacute;elle.</li>
<li><strong>Sp&eacute;cification marine aussi &agrave; l'int&eacute;rieur.</strong> L'a&eacute;rosol salin porte sur plusieurs kilom&egrave;tres &mdash; fixations et batteries de climatisation durent bien plus longtemps en 316 et rev&ecirc;tements marins.</li>
<li><strong>Vitrage.</strong> Feuillet&eacute; ou class&eacute; impact sur les fa&ccedil;ades expos&eacute;es : il r&eacute;duit la charge de climatisation qui domine la facture CFE et maintient l'enveloppe close en saison cyclonique.</li>
</ul>
<p>Pages utiles : <a href="/constructeur-cancun/">Constructeur &agrave; Canc&uacute;n</a> &middot; <a href="/construction-de-maisons-cancun/">Construction de maisons &agrave; Canc&uacute;n</a> &middot; <a href="/construction-villas-hotels-cancun/">Villas et h&ocirc;tels &agrave; Canc&uacute;n</a> &middot; <a href="/blog-fr/cout-construire-maison-cancun.html">Co&ucirc;t de construction &agrave; Canc&uacute;n</a> &middot; <a href="/construction-villa-luxe-playa-del-carmen/">Villas de luxe &agrave; Playa del Carmen</a></p>

<h2 class="mt-4">Pourquoi Recrea à Cancún</h2>
<ul>
<li><strong>196+ projets</strong> au Quintana Roo depuis 2008, dont Canc&uacute;n, Puerto Canc&uacute;n et la Zone H&ocirc;teli&egrave;re.</li>
<li><strong>Contrat &agrave; prix ferme</strong> avec budget d&eacute;taill&eacute;, paiements &agrave; l'avancement v&eacute;rifi&eacute; et retenue jusqu'&agrave; lev&eacute;e des r&eacute;serves.</li>
<li><strong>Tout en interne :</strong> architecture, structure, installations, menuiserie, m&eacute;tallerie, piscine et int&eacute;rieurs &mdash; un seul responsable.</li>
<li><strong>Permis complets :</strong> licence BJ, DRO, FONATUR, ZOFEMAT et comit&eacute; de la r&eacute;sidence.</li>
<li><strong>Chantier &agrave; distance :</strong> rapports hebdomadaires photo et vid&eacute;o pour les propri&eacute;taires en Europe et en Am&eacute;rique du Nord.</li>
<li><strong>Garantie &eacute;crite d'un an</strong> sur les travaux.</li>
</ul>

<h2 class="mt-4">Questions fréquentes</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">Combien co&ucirc;te une villa de luxe &agrave; Canc&uacute;n ?</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">En 2026, de $25,000 &agrave; $45,000+ MXN/m² selon le secteur et la finition. Une villa de 400 m² sur canal ou marina revient &agrave; environ $12&ndash;18 millions MXN cl&eacute; en main.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">Dans quels secteurs construisez-vous ?</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Puerto Canc&uacute;n, la Zone H&ocirc;teli&egrave;re et Isla Dorada, ainsi que les r&eacute;sidences ferm&eacute;es de l'int&eacute;rieur : Lagos del Sol, Villa Magna, Aqua, Residencial Cumbres et Riviera Canc&uacute;n.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">Quels permis sont n&eacute;cessaires ?</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Usage du sol, permis et alignement aupr&egrave;s de Benito Ju&aacute;rez avec un DRO. La Zone H&ocirc;teli&egrave;re et Isla Dorada ajoutent FONATUR et la zone f&eacute;d&eacute;rale maritime ; les r&eacute;sidences ferm&eacute;es ont leur propre comit&eacute;.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">Combien de temps dure le chantier ?</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Dix &agrave; seize mois, plus deux &agrave; quatre mois de conception et de permis. Dans les r&eacute;sidences aux horaires restreints, le d&eacute;lai se situe en haut de la fourchette et figure au contrat.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">Quelle sp&eacute;cification impose le climat ?</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Inox 316, aluminium anodis&eacute; ou &agrave; rev&ecirc;tement marin, enrobage de b&eacute;ton augment&eacute; et vitrage feuillet&eacute; ou class&eacute; impact sur les fa&ccedil;ades expos&eacute;es.</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">Pouvez-vous construire &agrave; distance ?</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Oui. Rapports hebdomadaires photo et vid&eacute;o, visioconf&eacute;rences d'avancement, paiements &agrave; l'avancement v&eacute;rifi&eacute; et gestion compl&egrave;te des permis et du notaire.</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">Pr&ecirc;t pour votre villa &agrave; Canc&uacute;n ?</h3><p class="text-white-50 mb-4">196+ projets. Prix ferme. Devis d&eacute;taill&eacute; sous 48 heures.</p><a href="https://wa.me/529844525333?text=Bonjour!%20Devis%20villa%20de%20luxe%20Cancun" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Devis par WhatsApp</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18+ ans</span><span class="trust-badge"><i class="bi bi-building"></i>196+ projets</span><span class="trust-badge"><i class="bi bi-shield-check"></i>Licence &amp; DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>Garantie 1 an</span></div>
</div></div></div></section>""",
}

C["zh"] = {
 "title": "2026年坎昆豪华别墅建造与翻新 | Recrea",
 "desc": "坎昆豪华别墅的建造与翻新：Puerto Cancún、酒店区、Isla Dorada 及内陆封闭社区。2026年价格、许可流程与海洋级规格。",
 "keywords": "坎昆豪华别墅, 坎昆建别墅, Puerto Cancun 别墅, 坎昆酒店区住宅, 坎昆建筑公司",
 "faq": [
  ("在坎昆建一栋豪华别墅要多少钱？",
   "2026年为每平米 $25,000 至 $45,000+ 比索，取决于区域与装修标准。运河或码头旁的400平米别墅交钥匙约 $1,200 万–$1,800 万比索。固定总价，附分项预算。"),
  ("你们在坎昆的哪些区域建别墅？",
   "Puerto Cancún（码头与 TPC 高尔夫球场）、酒店区与 Isla Dorada（运河与潟湖景观），以及内陆封闭社区：Lagos del Sol、Villa Magna、Aqua、Residencial Cumbres 和 Riviera Cancún。"),
  ("在坎昆需要哪些许可？",
   "贝尼托华雷斯市政厅的土地用途、施工许可与红线，并需责任建筑师（DRO）。酒店区和 Isla Dorada 还涉及 FONATUR，临运河或海岸还涉及联邦海域区（ZOFEMAT）。封闭社区另设设计委员会。"),
  ("工期需要多久？",
   "豪华别墅施工10至16个月，另加2至4个月的设计与报批。在限制作业时段的社区，工期趋向上限，并写入合同。"),
  ("坎昆的气候要求什么规格？",
   "紧固件与栏杆采用316不锈钢、阳极氧化或海洋级涂层铝材、外露构件加大混凝土保护层，以及外露立面采用夹胶或抗冲击玻璃。"),
  ("我人在国外可以远程建造吗？",
   "可以。每周图文与视频报告、进度视频会议、按核验进度付款，并全程代办许可与公证。"),
 ],
 "body": """<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>坎昆豪华别墅</h1>
<p class="lead">我们在<strong>坎昆</strong>建造与翻新<strong>豪华别墅</strong> &mdash; 从 Puerto Cancún 的码头、Isla Dorada 的运河，到内陆的封闭社区。设计、许可、施工、泳池、智能家居与软装，全部在同一份合同内完成。18年以上经验，金塔纳罗奥州196个项目。</p>
<div class="alert" style="background:var(--accent);color:#000;border:none"><strong>2026年坎昆豪华别墅：</strong>每平米 $25,000&ndash;$45,000+ 比索，视区域与装修而定。我们办理贝尼托华雷斯施工许可、DRO，以及适用时的 FONATUR 与 ZOFEMAT。</div>

<h2>坎昆的豪华别墅建在哪里</h2>
<p>坎昆不是一个豪宅市场，而是四个，各自的施工方式不同：</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>区域</th><th>产品</th><th>施工上的差别</th></tr></thead><tbody>
<tr><td>Puerto Cancún</td><td>面向码头与 TPC 高尔夫球场的别墅</td><td>社区规约、门禁管控、码头一侧涉及 ZOFEMAT</td></tr>
<tr><td>酒店区与 Isla Dorada</td><td>面向运河与 Nichupté 潟湖的住宅</td><td>FONATUR、ZOFEMAT、全套海洋级规格，仅有一条进出道路</td></tr>
<tr><td>Lagos del Sol、Villa Magna、Aqua、Residencial Cumbres</td><td>湖景或球场景观的封闭社区别墅</td><td>各社区自有设计委员会，无联邦区问题，市政流程更直接</td></tr>
<tr><td>Riviera Cancún</td><td>通往普埃尔托莫雷洛斯的高尔夫走廊别墅</td><td>地块可能属于贝尼托华雷斯或普埃尔托莫雷洛斯 &mdash; 需先核实</td></tr>
</tbody></table></div>

<h2 class="mt-4">2026年坎昆豪华别墅价格</h2>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>范围</th><th>比索/平米</th><th>美元/平米</th></tr></thead><tbody>
<tr><td>既有别墅整体翻新</td><td>$12,000&ndash;$20,000</td><td>$660&ndash;$1,100</td></tr>
<tr><td>内陆封闭社区高端新建</td><td>$22,000&ndash;$30,000</td><td>$1,220&ndash;$1,670</td></tr>
<tr><td>Puerto Cancún 高端新建</td><td>$25,000&ndash;$35,000</td><td>$1,380&ndash;$1,930</td></tr>
<tr><td>运河、潟湖或码头旁的超豪华</td><td>$35,000&ndash;$45,000+</td><td>$1,930&ndash;$2,480+</td></tr>
</tbody></table></div>
<p class="text-muted small">含结构、机电与装修。土地、定制泳池、成熟园林与家具另行报价。</p>

<h2 class="mt-4">在坎昆开工前需要知道的事</h2>
<ul>
<li><strong>贝尼托华雷斯市政厅。</strong>土地用途、许可、红线与责任建筑师。对于已通管线的住宅地块，这是全州最可预期的流程之一。</li>
<li><strong>酒店区与 Isla Dorada。</strong>那里适用 FONATUR 与联邦海域区 &mdash; 购地前请确认产权到底止于何处、存在何种特许。</li>
<li><strong>设计委员会。</strong>Puerto Cancún、Lagos del Sol、Villa Magna、Aqua 与 Residencial Cumbres 审查高度、材料、色彩与围墙，并要求工人登记、限定作业时段与保证金。请在方案阶段提交。</li>
<li><strong>地质勘察。</strong>喀斯特可能给出极好的承载力，而两米外就是溶洞；钻孔覆盖实际建筑轮廓。</li>
<li><strong>内陆同样需要海洋级规格。</strong>盐雾可深入数公里 &mdash; 采用316不锈钢与海洋级涂层的紧固件和冷凝器盘管寿命明显更长。</li>
<li><strong>玻璃。</strong>外露立面采用夹胶或抗冲击玻璃：既降低主导电费的制冷负荷，也在飓风季保持建筑外壳完整。</li>
</ul>
<p>相关页面：<a href="/cancun-jianzhu-gongsi/">坎昆建筑公司</a> &middot; <a href="/zhuzhai-jianzao-cancun/">坎昆住宅建造</a> &middot; <a href="/bieshu-jiudian-jianzao-cancun/">坎昆别墅与酒店建设</a> &middot; <a href="/blog-zh/cancun-jianfang-chengben.html">坎昆建房成本</a> &middot; <a href="/haohua-bieshu-playa-del-carmen/">普拉亚德尔卡门豪华别墅</a></p>

<h2 class="mt-4">为什么选择 Recrea</h2>
<ul>
<li><strong>自2008年起196个以上项目</strong>，其中包括坎昆、Puerto Cancún 与酒店区。</li>
<li><strong>固定总价合同</strong>，附分项预算，按核验进度付款，缺陷清单关闭后释放质保金。</li>
<li><strong>全部自有团队：</strong>建筑、结构、机电、木作、金属、泳池与室内 &mdash; 单一责任方。</li>
<li><strong>许可全程代办：</strong>市政许可、DRO、FONATUR、ZOFEMAT 与社区设计委员会。</li>
<li><strong>远程建造：</strong>为身在海外的业主提供每周图文与视频报告。</li>
<li><strong>一年书面质保。</strong></li>
</ul>

<h2 class="mt-4">常见问题</h2>
<div class="accordion my-4" id="faqAcc">
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#f1">在坎昆建一栋豪华别墅要多少钱？</button></h3><div id="f1" class="accordion-collapse collapse show" data-bs-parent="#faqAcc"><div class="accordion-body">2026年为每平米 $25,000 至 $45,000+ 比索，取决于区域与装修标准。运河或码头旁的400平米别墅交钥匙约 $1,200 万&ndash;$1,800 万比索。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f2">你们在坎昆的哪些区域建别墅？</button></h3><div id="f2" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">Puerto Cancún、酒店区与 Isla Dorada，以及内陆封闭社区：Lagos del Sol、Villa Magna、Aqua、Residencial Cumbres 和 Riviera Cancún。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f3">在坎昆需要哪些许可？</button></h3><div id="f3" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">贝尼托华雷斯市政厅的土地用途、施工许可与红线，并需 DRO。酒店区和 Isla Dorada 还涉及 FONATUR 与联邦海域区，封闭社区另设设计委员会。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f4">工期需要多久？</button></h3><div id="f4" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">施工10至16个月，另加2至4个月的设计与报批。在限制作业时段的社区，工期趋向上限，并写入合同。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f5">坎昆的气候要求什么规格？</button></h3><div id="f5" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">316不锈钢、阳极氧化或海洋级涂层铝材、外露构件加大混凝土保护层，以及外露立面的夹胶或抗冲击玻璃。</div></div></div>
<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#f6">可以远程建造吗？</button></h3><div id="f6" class="accordion-collapse collapse" data-bs-parent="#faqAcc"><div class="accordion-body">可以。每周图文与视频报告、进度视频会议、按核验进度付款，并全程代办许可与公证。</div></div></div>
</div>

<div class="cta-section rounded p-5 text-center my-5"><h3 class="text-white mb-3">准备在坎昆开始您的别墅？</h3><p class="text-white-50 mb-4">196个以上项目。固定总价。48小时内出详细报价。</p><a href="https://wa.me/529844525333?text=您好！坎昆豪华别墅报价" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>WhatsApp 获取报价</a></div>
<div class="trust-badges"><span class="trust-badge"><i class="bi bi-award"></i>18年以上</span><span class="trust-badge"><i class="bi bi-building"></i>196+ 项目</span><span class="trust-badge"><i class="bi bi-shield-check"></i>执照与 DRO</span><span class="trust-badge"><i class="bi bi-patch-check"></i>一年质保</span></div>
</div></div></div></section>""",
}

if __name__ == "__main__":
    import sys
    for lang in (sys.argv[1:] or sorted(C)):
        if lang not in C:
            print(f"  ! no content for {lang}"); continue
        w, s = build(lang)
        print(f"  {w:5d} words  /{s}/")
