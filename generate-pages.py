#!/usr/bin/env python3
import os, re

BASE = "/home/olek/recrea-bootstrap"
CONTENT = "/home/olek/recrea-site-upgrade"

def strip_comments(html):
    return re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL).strip()

def page_template(title, meta_desc, body, breadcrumb="", css_path="css/style.css", depth=0):
    prefix = "../" * depth
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{meta_desc}">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="{prefix}css/style.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
  <div class="container">
    <a class="navbar-brand fw-bold" href="{prefix}index.html">RECREA</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu"><span class="navbar-toggler-icon"></span></button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto align-items-center">
        <li class="nav-item"><a class="nav-link" href="{prefix}index.html#services">Services</a></li>
        <li class="nav-item"><a class="nav-link" href="{prefix}index.html#projects">Projects</a></li>
        <li class="nav-item"><a class="nav-link" href="{prefix}index.html#about">About</a></li>
        <li class="nav-item"><a class="nav-link" href="{prefix}blog/">Blog</a></li>
        <li class="nav-item"><a class="nav-link" href="{prefix}index.html#contact">Contact</a></li>
        <li class="nav-item ms-lg-3"><a class="btn btn-whatsapp" href="https://wa.me/529844525333"><i class="bi bi-whatsapp me-1"></i> WhatsApp</a></li>
      </ul>
    </div>
  </div>
</nav>

<div style="padding-top:80px"></div>

{breadcrumb}

<section class="py-5">
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-8">
{body}
      </div>
    </div>
  </div>
</section>

<section class="cta-section">
  <div class="container text-center">
    <h2 class="mb-3">Ready to Start Your Project?</h2>
    <p class="lead mb-4" style="color:rgba(255,255,255,.8)">Free consultation — call or WhatsApp</p>
    <a href="https://wa.me/529844525333" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>WhatsApp Us</a>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <div class="footer-bottom text-center">
      <p class="mb-0">&copy; 2008–2026 Recrea Construction. All rights reserved. | <a href="{prefix}index.html">Home</a></p>
    </div>
  </div>
</footer>

<a href="https://wa.me/529844525333" class="whatsapp-float" aria-label="WhatsApp">
  <svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.611.611l4.458-1.495A11.94 11.94 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.319 0-4.476-.724-6.252-1.957l-.436-.31-3.266 1.095 1.095-3.266-.31-.436A9.953 9.953 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg>
</a>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>'''

def breadcrumb_html(items, prefix=""):
    bc = '<nav class="container mt-3"><ol class="breadcrumb">'
    for i, (label, url) in enumerate(items):
        if i == len(items) - 1:
            bc += f'<li class="breadcrumb-item active">{label}</li>'
        else:
            bc += f'<li class="breadcrumb-item"><a href="{prefix}{url}">{label}</a></li>'
    bc += '</ol></nav>'
    return bc

# ============ BLOG POSTS (English) ============
os.makedirs(f"{BASE}/blog", exist_ok=True)

blog_posts = [
    ("cost-build-house-tulum.html", "How Much Does It Cost to Build a House in Tulum? (2026 Guide)",
     "Detailed breakdown of construction costs in Tulum, Mexico. Per square meter pricing from a local contractor.",
     f"{CONTENT}/blog-posts/01-cost-build-house-tulum.html"),
    ("construction-permits-playa-del-carmen.html", "Construction Permits in Playa del Carmen: Complete Guide (2026)",
     "How to get construction permits in Playa del Carmen. Requirements, costs, timeline, and documents needed.",
     f"{CONTENT}/blog-posts/02-construction-permits-playa-del-carmen.html"),
    ("choose-construction-company-riviera-maya.html", "How to Choose a Construction Company in Riviera Maya (2026)",
     "What to look for when hiring a contractor in Playa del Carmen, Tulum, or Cancún.",
     f"{CONTENT}/blog-posts/03-best-contractors-riviera-maya.html"),
    ("home-renovation-playa-del-carmen.html", "Home Renovation in Playa del Carmen: Costs, Ideas & Tips (2026)",
     "Planning a home renovation in Playa del Carmen? Cost per m², timeline, and what to know.",
     f"{CONTENT}/blog-posts/04-renovation-playa-del-carmen.html"),
    ("foreigners-build-house-mexico.html", "Can Foreigners Build a House in Mexico? Yes — Here's How",
     "Everything foreigners need to know about building property in Mexico. Fideicomiso, permits, costs.",
     f"{CONTENT}/blog-posts/05-buying-building-foreigner-mexico.html"),
    ("commercial-construction-cancun.html", "Commercial Construction in Cancún & Riviera Maya | Recrea",
     "Commercial construction services in Cancún, Playa del Carmen, and Tulum. Turnkey builds.",
     f"{CONTENT}/blog-posts/06-commercial-construction-cancun.html"),
    ("hurricane-proof-construction.html", "Hurricane-Proof Construction in the Riviera Maya | Recrea",
     "How to build a hurricane-resistant home in Cancún, Playa del Carmen, or Tulum.",
     f"{CONTENT}/blog-posts/07-hurricane-proof-construction-mexico.html"),
    ("airbnb-investment-tulum.html", "Building an Airbnb Investment Property in Tulum (2026 ROI Guide)",
     "Is building an Airbnb in Tulum worth it? Construction costs, rental income, ROI projections.",
     f"{CONTENT}/blog-posts/08-airbnb-investment-property-tulum.html"),
]

for fname, title, desc, src in blog_posts:
    with open(src) as f:
        body = strip_comments(f.read())
    bc = breadcrumb_html([("Home", "index.html"), ("Blog", "blog/"), (title[:40]+"...", "")], "../")
    html = page_template(title, desc, body, bc, depth=1)
    with open(f"{BASE}/blog/{fname}", "w") as f:
        f.write(html)
    print(f"  Blog: {fname}")

# Blog index
blog_index_body = '<h1 class="section-title">Construction Guides</h1>\n<p class="section-subtitle">Expert advice for building in the Riviera Maya</p>\n<div class="list-group">\n'
for fname, title, desc, _ in blog_posts:
    blog_index_body += f'<a href="{fname}" class="list-group-item list-group-item-action p-4 mb-3 rounded">\n<h5 class="fw-bold mb-1">{title}</h5>\n<p class="text-muted mb-0">{desc}</p>\n</a>\n'
blog_index_body += '</div>'
bc = breadcrumb_html([("Home", "index.html"), ("Blog", "")], "../")
html = page_template("Construction Blog | Recrea Construction", "Expert guides to building in the Riviera Maya.", blog_index_body, bc, depth=1)
with open(f"{BASE}/blog/index.html", "w") as f:
    f.write(html)
print("  Blog: index.html")

# ============ SPANISH BLOG POSTS ============
os.makedirs(f"{BASE}/blog-es", exist_ok=True)

blog_es = [
    ("costo-construir-casa-tulum.html", "¿Cuánto Cuesta Construir una Casa en Tulum? Guía 2026",
     "Desglose de costos de construcción en Tulum. Precios por metro cuadrado.",
     f"{CONTENT}/blog-posts-es/01-costo-construir-casa-tulum.html"),
    ("permisos-construccion-playa-del-carmen.html", "Permisos de Construcción en Playa del Carmen: Guía 2026",
     "Cómo obtener permisos de construcción en Playa del Carmen. Requisitos, costos, tiempos.",
     f"{CONTENT}/blog-posts-es/02-permisos-construccion-playa-del-carmen.html"),
    ("remodelacion-casa-playa-del-carmen.html", "Remodelación de Casa en Playa del Carmen: Costos e Ideas 2026",
     "Costos de remodelación en Playa del Carmen. Cocina, baño, remodelación completa.",
     f"{CONTENT}/blog-posts-es/03-remodelacion-playa-del-carmen.html"),
    ("construccion-comercial-cancun.html", "Construcción Comercial en Cancún y Riviera Maya | Recrea",
     "Construcción comercial en Cancún, Playa del Carmen y Tulum. Locales, restaurantes, oficinas.",
     f"{CONTENT}/blog-posts-es/04-construccion-comercial-cancun.html"),
]

for fname, title, desc, src in blog_es:
    with open(src) as f:
        body = strip_comments(f.read())
    bc = breadcrumb_html([("Inicio", "index.html"), ("Blog", "blog-es/"), (title[:40]+"...", "")], "../")
    html = page_template(title, desc, body, bc, depth=1)
    html = html.replace('lang="en"', 'lang="es"')
    with open(f"{BASE}/blog-es/{fname}", "w") as f:
        f.write(html)
    print(f"  Blog ES: {fname}")

# ============ SERVICE PAGES ============
os.makedirs(f"{BASE}/services", exist_ok=True)

svc_file = f"{CONTENT}/seo/11-service-page-content.html"
with open(svc_file) as f:
    svc_raw = f.read()

sections_data = [
    ("residential.html", "House & Villa Construction Playa del Carmen, Tulum | Recrea",
     "Custom home and villa construction in Playa del Carmen, Tulum, and Puerto Aventuras.",
     "House & Villa", "PAGE: House"),
    ("commercial.html", "Commercial Construction Cancún & Riviera Maya | Recrea",
     "Commercial construction for shops, restaurants, and offices in Cancún, Playa del Carmen, and Tulum.",
     "Commercial", "PAGE: Commercial"),
    ("renovation.html", "Home Renovation & Remodeling Playa del Carmen | Recrea",
     "Home renovation and remodeling in Playa del Carmen, Tulum, Puerto Aventuras.",
     "Renovation", "PAGE: Renovation"),
    ("electrical.html", "Electrical & LED Installation Riviera Maya | Recrea",
     "Electrical installation, LED lighting, and wiring for homes and businesses.",
     "Electrical", "PAGE: Electrical"),
    ("carpentry.html", "Custom Carpentry & Furniture Playa del Carmen | Recrea",
     "Custom wood furniture, cabinetry, and carpentry in Playa del Carmen.",
     "Carpentry", "PAGE: Carpentry"),
    ("metalwork.html", "Ironwork, Aluminum & Glass Installation Riviera Maya | Recrea",
     "Custom metalwork, aluminum windows, glass railings in Playa del Carmen, Cancún, Tulum.",
     "Ironwork", "PAGE: Ironwork"),
]

svc_sections = svc_raw.split("<!-- ============================================= -->")

for fname, title, desc, keyword, marker in sections_data:
    body = ""
    for s in svc_sections:
        if keyword in s and marker in s:
            body = strip_comments(s)
            break
    if not body:
        body = f"<h1>{title}</h1><p>Content coming soon.</p>"

    bc = breadcrumb_html([("Home", "index.html"), ("Services", ""), (title.split("|")[0].strip(), "")], "../")
    html = page_template(title, desc, body, bc, depth=1)
    with open(f"{BASE}/services/{fname}", "w") as f:
        f.write(html)
    print(f"  Service: {fname}")

print("\nAll pages generated!")
