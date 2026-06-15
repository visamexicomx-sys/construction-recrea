<?php
if (php_sapi_name() !== 'cli' && (!isset($_GET['key']) || $_GET['key'] !== 'recrea2026news')) {
    http_response_code(403);
    die('Forbidden');
}

set_time_limit(120);
ini_set('memory_limit', '128M');

$base = dirname(__FILE__);
$out_dir = $base . '/noticias';
if (!is_dir($out_dir)) mkdir($out_dir, 0755, true);

$categories = [
    'construccion' => [
        'name' => 'Construcción',
        'icon' => 'bi-building',
        'color' => '#e8720c',
        'queries' => [
            'construcción Quintana Roo',
            'construcción Playa del Carmen Tulum',
            'construction Riviera Maya Mexico'
        ]
    ],
    'inmobiliario' => [
        'name' => 'Inmobiliario',
        'icon' => 'bi-house-door',
        'color' => '#198754',
        'queries' => [
            'bienes raíces Riviera Maya',
            'real estate Cancun Playa del Carmen',
            'inmobiliario Quintana Roo'
        ]
    ],
    'turismo' => [
        'name' => 'Turismo & Inversión',
        'icon' => 'bi-globe-americas',
        'color' => '#0d6efd',
        'queries' => [
            'turismo Riviera Maya inversión',
            'tourism investment Cancun Tulum',
            'desarrollo turístico Quintana Roo'
        ]
    ],
    'sostenibilidad' => [
        'name' => 'Sostenibilidad',
        'icon' => 'bi-leaf',
        'color' => '#20c997',
        'queries' => [
            'construcción sostenible México',
            'sustainable building Mexico Caribbean',
            'energía renovable Quintana Roo'
        ]
    ],
    'infraestructura' => [
        'name' => 'Infraestructura',
        'icon' => 'bi-signpost-2',
        'color' => '#6f42c1',
        'queries' => [
            'infraestructura Quintana Roo',
            'Tren Maya desarrollo',
            'infraestructura Cancún Playa del Carmen'
        ]
    ]
];

function fetch_rss($query, $max = 8) {
    $url = 'https://news.google.com/rss/search?q=' . urlencode($query) . '&hl=es-419&gl=MX&ceid=MX:es-419';
    $ctx = stream_context_create([
        'http' => [
            'timeout' => 15,
            'user_agent' => 'Mozilla/5.0 (compatible; RecreaBot/1.0)'
        ]
    ]);
    $xml = @file_get_contents($url, false, $ctx);
    if (!$xml) return [];

    libxml_use_internal_errors(true);
    $feed = @simplexml_load_string($xml);
    if (!$feed || !isset($feed->channel->item)) return [];

    $items = [];
    $cutoff = strtotime('-48 hours');
    foreach ($feed->channel->item as $item) {
        $pub = strtotime((string)$item->pubDate);
        if ($pub < $cutoff) continue;
        $title = strip_tags((string)$item->title);
        $source = '';
        if (preg_match('/\s*-\s*([^-]+)$/', $title, $m)) {
            $source = trim($m[1]);
            $title = trim(preg_replace('/\s*-\s*[^-]+$/', '', $title));
        }
        $items[] = [
            'title' => $title,
            'link' => (string)$item->link,
            'source' => $source,
            'date' => $pub,
            'date_fmt' => date('d M Y, H:i', $pub)
        ];
        if (count($items) >= $max) break;
    }
    return $items;
}

$all_news = [];
$cat_counts = [];

foreach ($categories as $key => $cat) {
    $cat_items = [];
    $seen = [];
    foreach ($cat['queries'] as $q) {
        $items = fetch_rss($q, 5);
        foreach ($items as $item) {
            $hash = md5($item['title']);
            if (isset($seen[$hash])) continue;
            $seen[$hash] = true;
            $item['category'] = $key;
            $cat_items[] = $item;
        }
    }
    usort($cat_items, function($a, $b) { return $b['date'] - $a['date']; });
    $cat_items = array_slice($cat_items, 0, 8);
    $cat_counts[$key] = count($cat_items);
    $all_news = array_merge($all_news, $cat_items);
}

$total = count($all_news);
$updated = date('d/m/Y H:i', time());
$updated_iso = date('c');

$news_html = '';
foreach ($categories as $key => $cat) {
    $items = array_filter($all_news, function($n) use ($key) { return $n['category'] === $key; });
    if (empty($items)) continue;

    $news_html .= '<div class="news-group" data-category="' . $key . '">';
    $news_html .= '<h3 class="category-title mt-5 mb-3"><i class="bi ' . $cat['icon'] . ' me-2"></i>' . $cat['name'] . ' <span class="badge rounded-pill" style="background:' . $cat['color'] . '">' . count($items) . '</span></h3>';
    $news_html .= '<div class="row g-3">';
    foreach ($items as $item) {
        $news_html .= '
        <div class="col-md-6">
          <div class="news-card h-100">
            <div class="news-card-body">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <span class="news-badge" style="background:' . $cat['color'] . '15;color:' . $cat['color'] . '">' . $cat['name'] . '</span>
                <small class="text-muted">' . $item['date_fmt'] . '</small>
              </div>
              <h5 class="news-title"><a href="' . htmlspecialchars($item['link']) . '" target="_blank" rel="noopener">' . htmlspecialchars($item['title']) . '</a></h5>
              ' . ($item['source'] ? '<p class="news-source mb-0"><i class="bi bi-newspaper me-1"></i>' . htmlspecialchars($item['source']) . '</p>' : '') . '
            </div>
          </div>
        </div>';
    }
    $news_html .= '</div></div>';
}

$filter_buttons = '<button class="filter-btn active" data-filter="all">Todas <span class="count">' . $total . '</span></button>';
foreach ($categories as $key => $cat) {
    if (($cat_counts[$key] ?? 0) === 0) continue;
    $filter_buttons .= '<button class="filter-btn" data-filter="' . $key . '" style="--cat-color:' . $cat['color'] . '"><i class="bi ' . $cat['icon'] . '"></i> ' . $cat['name'] . ' <span class="count">' . $cat_counts[$key] . '</span></button>';
}

$html = '<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Noticias del Sector | Recrea Construction — Construcción & Inmobiliario Riviera Maya</title>
  <meta name="description" content="Últimas noticias de construcción, inmobiliario, turismo e infraestructura en la Riviera Maya. Actualizado diariamente.">
  <meta name="robots" content="index, follow">
  <link rel="canonical" href="https://construction-recrea.com/noticias/">
  <meta property="og:title" content="Noticias del Sector — Recrea Construction">
  <meta property="og:description" content="Noticias diarias de construcción, inmobiliario e inversión en la Riviera Maya.">
  <meta property="og:url" content="https://construction-recrea.com/noticias/">
  <meta property="og:type" content="website">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
  <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link href="../css/style.css" rel="stylesheet">
  <link rel="icon" href="../favicon.ico" sizes="32x32">
  <style>
    .news-hero{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 50%,#0f3460 100%);padding:80px 0 50px;margin-top:56px}
    .news-hero h1{font-size:2.5rem;font-weight:800;color:#fff}
    .news-hero .lead{color:rgba(255,255,255,.7);font-size:1.1rem}
    .news-stats{display:flex;gap:24px;margin-top:20px}
    .news-stat{color:rgba(255,255,255,.9);font-size:.9rem}
    .news-stat strong{color:#e8720c;font-size:1.3rem;display:block}
    .filter-bar{background:#fff;border-radius:12px;padding:16px 20px;box-shadow:0 2px 12px rgba(0,0,0,.08);margin-top:-30px;position:relative;z-index:10;display:flex;flex-wrap:wrap;gap:8px;align-items:center}
    .filter-btn{border:1.5px solid #dee2e6;background:#fff;border-radius:8px;padding:8px 16px;font-size:.85rem;font-weight:600;cursor:pointer;transition:all .2s;font-family:Inter,sans-serif;display:inline-flex;align-items:center;gap:6px}
    .filter-btn:hover{border-color:#e8720c;color:#e8720c}
    .filter-btn.active{background:#e8720c;color:#fff;border-color:#e8720c}
    .filter-btn .count{background:rgba(0,0,0,.1);border-radius:12px;padding:1px 8px;font-size:.75rem}
    .filter-btn.active .count{background:rgba(255,255,255,.25)}
    .category-title{font-size:1.3rem;font-weight:700;color:#1a1a2e;display:flex;align-items:center}
    .category-title .badge{font-size:.7rem;font-weight:600;margin-left:8px}
    .news-card{background:#fff;border:1px solid #e9ecef;border-radius:12px;transition:all .25s;overflow:hidden}
    .news-card:hover{box-shadow:0 8px 25px rgba(0,0,0,.1);transform:translateY(-2px);border-color:#e8720c}
    .news-card-body{padding:20px}
    .news-badge{font-size:.7rem;font-weight:600;padding:4px 10px;border-radius:6px;letter-spacing:.3px;text-transform:uppercase}
    .news-title{font-size:.95rem;font-weight:600;line-height:1.4;margin-bottom:8px}
    .news-title a{color:#1a1a2e;text-decoration:none}
    .news-title a:hover{color:#e8720c}
    .news-source{font-size:.8rem;color:#6c757d}
    .empty-state{text-align:center;padding:60px 20px;color:#6c757d}
    .empty-state i{font-size:3rem;margin-bottom:16px;display:block}
    .update-badge{background:rgba(232,114,12,.1);color:#e8720c;font-size:.8rem;padding:6px 14px;border-radius:20px;font-weight:500}
    @media(max-width:768px){
      .news-hero h1{font-size:1.8rem}
      .filter-bar{padding:12px;gap:6px}
      .filter-btn{padding:6px 12px;font-size:.8rem}
      .news-stats{gap:16px}
    }
  </style>
</head>
<body>

<nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" id="mainNav">
  <div class="container">
    <a class="navbar-brand fw-bold" href="/">RECREA</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navMenu"><span class="navbar-toggler-icon"></span></button>
    <div class="collapse navbar-collapse" id="navMenu">
      <ul class="navbar-nav ms-auto align-items-center">
        <li class="nav-item"><a class="nav-link" href="/#services">Servicios</a></li>
        <li class="nav-item"><a class="nav-link" href="/#projects">Proyectos</a></li>
        <li class="nav-item"><a class="nav-link" href="/#about">Nosotros</a></li>
        <li class="nav-item"><a class="nav-link active" href="/noticias/">Noticias</a></li>
        <li class="nav-item"><a class="nav-link" href="/partners/">Partners</a></li>
        <li class="nav-item"><a class="nav-link" href="/#faq">FAQ</a></li>
        <li class="nav-item"><a class="nav-link" href="/#contact">Contacto</a></li>
        <li class="nav-item dropdown ms-lg-2">
          <a class="nav-link dropdown-toggle" href="#" data-bs-toggle="dropdown">ES</a>
          <ul class="dropdown-menu dropdown-menu-end">
            <li><a class="dropdown-item active" href="/">Español</a></li>
            <li><a class="dropdown-item" href="/en/">English</a></li>
            <li><a class="dropdown-item" href="/de/">Deutsch</a></li>
            <li><a class="dropdown-item" href="/ru/">Русский</a></li>
            <li><a class="dropdown-item" href="/zh/">中文</a></li>
          </ul>
        </li>
        <li class="nav-item ms-lg-2"><a class="btn btn-whatsapp" href="https://wa.me/529844525333"><i class="bi bi-whatsapp me-1"></i> WhatsApp</a></li>
      </ul>
    </div>
  </div>
</nav>

<section class="news-hero">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-8">
        <h1><i class="bi bi-newspaper me-2"></i>Noticias del Sector</h1>
        <p class="lead">Construcción, inmobiliario e inversión en la Riviera Maya — actualizado diariamente</p>
        <div class="news-stats">
          <div class="news-stat"><strong>' . $total . '</strong>noticias hoy</div>
          <div class="news-stat"><strong>' . count(array_filter($cat_counts)) . '</strong>categorías</div>
          <div class="news-stat"><strong>24/7</strong>monitoreo</div>
        </div>
      </div>
      <div class="col-lg-4 text-lg-end mt-3 mt-lg-0">
        <span class="update-badge"><i class="bi bi-clock me-1"></i>Actualizado: ' . $updated . '</span>
      </div>
    </div>
  </div>
</section>

<div class="container">
  <div class="filter-bar">
    ' . $filter_buttons . '
  </div>
</div>

<section class="py-4">
  <div class="container">
    ' . ($total > 0 ? $news_html : '<div class="empty-state"><i class="bi bi-inbox"></i><h4>Sin noticias recientes</h4><p>No se encontraron noticias en las últimas 48 horas. Vuelve más tarde.</p></div>') . '
  </div>
</section>

<section class="py-5">
  <div class="container">
    <div class="cta-section rounded p-5 text-center">
      <h3 class="text-white mb-3">¿Planeas Construir en la Riviera Maya?</h3>
      <p class="text-white-50 mb-4">18+ años de experiencia, 196+ proyectos. Respondemos en menos de 2 horas.</p>
      <a href="https://wa.me/529844525333?text=Hola%2C%20vi%20las%20noticias%20en%20su%20sitio%20y%20tengo%20una%20consulta." class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>Consulta Gratuita</a>
    </div>
  </div>
</section>

<footer class="footer"><div class="container"><div class="footer-bottom text-center"><p class="mb-0">&copy; 2008–2026 Recrea Construction. Todos los derechos reservados. | <a href="/">Inicio</a> · <a href="/noticias/">Noticias</a> · <a href="/blog/">Blog</a></p></div></div></footer>
<a href="https://wa.me/529844525333" class="whatsapp-float" aria-label="WhatsApp"><svg viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/><path d="M12 0C5.373 0 0 5.373 0 12c0 2.625.846 5.059 2.284 7.034L.789 23.492a.5.5 0 00.611.611l4.458-1.495A11.94 11.94 0 0012 24c6.627 0 12-5.373 12-12S18.627 0 12 0zm0 22c-2.319 0-4.476-.724-6.252-1.957l-.436-.31-3.266 1.095 1.095-3.266-.31-.436A9.953 9.953 0 012 12C2 6.477 6.477 2 12 2s10 4.477 10 10-4.477 10-10 10z"/></svg></a>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>
window.addEventListener("scroll",function(){document.getElementById("mainNav").classList.toggle("scrolled",window.scrollY>50)});
document.querySelectorAll(".filter-btn").forEach(function(btn){
  btn.addEventListener("click",function(){
    document.querySelectorAll(".filter-btn").forEach(function(b){b.classList.remove("active")});
    this.classList.add("active");
    var f=this.getAttribute("data-filter");
    document.querySelectorAll(".news-group").forEach(function(g){
      g.style.display=(f==="all"||g.getAttribute("data-category")===f)?"block":"none";
    });
  });
});
var c=document.getElementById("navMenu");if(c){document.querySelectorAll("#navMenu .nav-link:not(.dropdown-toggle)").forEach(function(l){l.addEventListener("click",function(){var b=bootstrap.Collapse.getInstance(c);if(b)b.hide()})})};
</script>
</body>
</html>';

file_put_contents($out_dir . '/index.html', $html);

if (php_sapi_name() !== 'cli') {
    header('Content-Type: text/plain');
}
echo "OK | {$total} noticias | " . count(array_filter($cat_counts)) . " categorías | {$updated}\n";
foreach ($categories as $key => $cat) {
    echo "  {$cat['name']}: " . ($cat_counts[$key] ?? 0) . "\n";
}
