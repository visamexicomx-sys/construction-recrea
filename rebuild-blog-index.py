#!/usr/bin/env python3
"""Rebuild the article grid of every blog index (blog, blog-es, blog-de, blog-ru,
blog-fr, blog-zh) from the actual article files on disk.

Fixes the drift that accumulated from articles being appended by hand:
every article is listed exactly once, in the right category section, with
correct counts in the pills / section headers / hero stats, and uniform cards.
Idempotent: safe to re-run after adding new articles."""
import re, os, glob, html

DIRS = ['blog', 'blog-es', 'blog-de', 'blog-ru', 'blog-fr', 'blog-zh']

# ---------------------------------------------------------------- taxonomy ---
CATS = [
    ('news',       '#dc3545', 'bi-newspaper'),
    ('costs',      '#198754', 'bi-calculator'),
    ('permits',    '#fd7e14', 'bi-file-earmark-text'),
    ('foreigners', '#0d6efd', 'bi-globe'),
    ('build',      '#6f42c1', 'bi-tools'),
    ('home',       '#20c997', 'bi-house-heart'),
]

# slug keywords, all six languages pooled; checked in the order of CATS above.
# 'tok' matches a whole slug token by prefix, 'sub' matches anywhere in the slug.
KW2 = {
 'news': dict(tok='informe reporte rapport report obzor otchet bericht baumarktbericht baogao news '
                  'noticias actualites mercado market markt immobilienmarkt marche rynok shichang boom '
                  'bauboom bum fanrong trend tendencias plusvalia wertsteigerung appreciation rost zengzhi xinwen statistik',
              sub='tren-maya train-maya maya-train land-prices maya-zug maya-lieche poezd-maya plus-value precios-terrenos '
                  'prix-terrains grundstueckspreise ceny-na-zemlyu tudi-jiage fangdichan-shichang fangchan-zengzhi'),
 'costs': dict(tok='cost costo costos costs cout couts cuesta cuanto precio prix preis preise kosten baukosten '
                   'hausbau unterhaltskosten lebenshaltungskosten stoimost skolko cena byudzhet budget feiyong '
                   'zaojia chengben jianfang presupuesto roi inversion investment investicii investissement invest '
                   'airbnb touzi rentabilite rendite financiacion hypothek mortgage impuesto impuestos tax steuer '
                   'steuervorteile nalog nalogovye shuishou fiscal fiscaux lgoty kalkulyator calculadora calculateur '
                   'calculator rechner jisuanqi huibao',
               sub='metro-cuadrado metre-carre kvadratny-metr quadratmeter pingfangmi costo-de-vida cout-de-la-vie '
                   'stoimost-zhizni shenghuo-feiyong shenghuo-chengben jianzhu-chengben zhuangxiu-feiyong '
                   'weihu-feiyong fanxin-touzi'),
 'permits': dict(tok='permis permisos permit permits licencia licencias genehmigungen baugenehmigungen razresheniya '
                     'xukezheng xuke pdu zonificacion zonage zonierung zonirovanie zoning guihua legal notaria ley '
                     'leyes loi lois gesetz gesetze baugesetze zakon zakony ekologicheskie geldwaesche antilavado '
                     'ambientales umwelt huanjing fagui tramite gestoria cronograma delais planning grafik sroki '
                     'timeline zeitplan bauzeitplan shijianbiao seguros assurances versicherungen strahovanie baoxian '
                     'warranty elegir choisir vybrat waehlen senales signaux warnsignale krasnye guyong xinhao '
                     'udalennoe fernverwaltung yuancheng choose insurance environmental',
                 sub='construir-vs-comprar construire-ou-acheter bauen-oder-kaufen stroit-ili build-vs-buy '
                     'zijian-vs-goumai fan-xiqian ruhe-xuanze jianzhu-shijian a-distance red-flags anti-money remote-construction'),
 'foreigners': dict(tok='extranjeros extranjero foreigners auslaender auswandern inostrantsy waiguoren etrangers '
                        'fideicomiso fideikomiso xintuoqi visa expat mudarse demenager pereezd banjia umzug retiro '
                        'retraite ruhestandshaus pensii yanglao comprar acheter pokupka kupit grundstueck goumai '
                        'buying moving retirement',
                    sub='casa-retiro maison-retraite moxige-yanglao dom-dlya-pensii'),
 'home': dict(tok='diseno design dizajn dizayn sheji conception interior interyera interieur inneneinrichtung redai '
                  'paisaj paysager landshaftnyy landshaft landscap gartengestaltung yuanlin jardin smart inteligente '
                  'umnyj umnyy zhineng connectee domotique automatisierung avtomatizaciya zidonghua iluminacion '
                  'eclairage osveshchenie osveshcheniya beleuchtung zhaoming lighting muebles mobilier ameublement '
                  'mebel moebel furniture jiaju ffe cocina cocinas cuisine cuisines kuhnya kuhni letnie letnyaya '
                  'kueche kuechen aussenkuechen chufang kitchen huwai bano vannoj badezimmer yushi terraza terrasa '
                  'terrasse dachterrasse azotea rooftop lutai seguridad securite bezopasnost sicherheitssysteme '
                  'anquan security mantenimiento entretien soderzhaniya wartung hausverwaltung administracion '
                  'upravlenie wuye gestion pisos sols poly bodenbelaege dimiancailiao acabado acabados finitions '
                  'otdelka ventanas fenetres fenster okna menchuang puertas portes dveri alberca albercas piscina '
                  'piscinas piscine piscines bassejny bassejnov pool pools schwimmbadbau youyongchi yongchi palapa '
                  'palapas palapy maocao garaje garajes garages garagen garazhi chewei elevador elevadores ascenseurs '
                  'lifty aufzuege dianti accesibilidad accessibilite accessibility dostupnost barrierefreiheit '
                  'wuzhangai remodelacion renovation renovierung hausrenovierung remont fanxin zhuangxiu '
                  'flooring windows doors minimalist',
              sub='sistemy-bezopasnosti gestion-locative property-management upravlenie-nedvizhimostyu'),
}

L = {
 'blog': dict(lang='en', cats=dict(news='News & Market', costs='Costs & ROI',
        permits='Permits & Process', foreigners='For Foreigners',
        build='Building & Technical', home='Design & Living'),
        all='All', ph='Search guides…', noun='articles', more='Read guide',
        h1='Construction Guides', lead='Real numbers from 196+ projects in the Riviera Maya. Costs, permits, ROI and building in Mexico.',
        st=('Guides','Categories','Projects','Years'), nores=('No articles found','Try another search term'),
        showall='Show all', articles='articles'),
 'blog-es': dict(lang='es', cats=dict(news='Noticias y Mercado', costs='Costos y ROI',
        permits='Permisos y Procesos', foreigners='Para Extranjeros',
        build='Construcción y Técnica', home='Diseño y Hogar'),
        all='Todas', ph='Buscar guías…', noun='artículos', more='Leer guía',
        h1='Guías de Construcción', lead='Números reales de 196+ proyectos en la Riviera Maya. Costos, permisos, ROI y construcción en México.',
        st=('Guías','Categorías','Proyectos','Años'), nores=('No se encontraron artículos','Intenta con otro término de búsqueda'),
        showall='Ver todas', articles='artículos'),
 'blog-de': dict(lang='de', cats=dict(news='Nachrichten & Markt', costs='Kosten & ROI',
        permits='Genehmigungen & Ablauf', foreigners='Für Ausländer',
        build='Bau & Technik', home='Design & Wohnen'),
        all='Alle', ph='Leitfäden suchen…', noun='Artikel', more='Leitfaden lesen',
        h1='Bau-Leitfäden', lead='Echte Zahlen aus 196+ Projekten in der Riviera Maya. Kosten, Genehmigungen, ROI und Bauen in Mexiko.',
        st=('Leitfäden','Kategorien','Projekte','Jahre'), nores=('Keine Artikel gefunden','Versuchen Sie einen anderen Suchbegriff'),
        showall='Alle anzeigen', articles='Artikel'),
 'blog-ru': dict(lang='ru', cats=dict(news='Новости и рынок', costs='Стоимость и ROI',
        permits='Разрешения и процесс', foreigners='Для иностранцев',
        build='Стройка и техника', home='Дизайн и дом'),
        all='Все', ph='Поиск по гидам…', noun='статей', more='Читать',
        h1='Гиды по строительству', lead='Реальные цифры из 196+ проектов на Ривьере-Майя. Стоимость, разрешения, ROI и строительство в Мексике.',
        st=('Гидов','Категорий','Проектов','Лет'), nores=('Статьи не найдены','Попробуйте другой запрос'),
        showall='Показать все', articles='статей'),
 'blog-fr': dict(lang='fr', cats=dict(news='Actualités & marché', costs='Coûts & ROI',
        permits='Permis & démarches', foreigners='Pour les étrangers',
        build='Construction & technique', home='Design & maison'),
        all='Tous', ph='Rechercher un guide…', noun='articles', more='Lire le guide',
        h1='Guides de construction', lead='Chiffres réels de 196+ projets dans la Riviera Maya. Coûts, permis, ROI et construction au Mexique.',
        st=('Guides','Catégories','Projets','Ans'), nores=('Aucun article trouvé','Essayez un autre terme de recherche'),
        showall='Tout afficher', articles='articles'),
 'blog-zh': dict(lang='zh', cats=dict(news='新闻与市场', costs='造价与回报',
        permits='许可与流程', foreigners='外国买家',
        build='施工与技术', home='设计与生活'),
        all='全部', ph='搜索指南…', noun='篇', more='阅读指南',
        h1='建筑指南', lead='来自里维埃拉玛雅196+个项目的真实数据：造价、许可、投资回报与在墨西哥建房。',
        st=('指南','分类','项目','年经验'), nores=('未找到文章','请尝试其他关键词'),
        showall='显示全部', articles='篇'),
}

PER_SECTION = 12   # cards shown before "show all"

# ------------------------------------------------------------------- style ---
STYLE = """<style id="blogIndexStyle">
.blog-hero{background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);color:#fff;padding:52px 0 40px;position:relative;overflow:hidden}
.blog-hero:after{content:"";position:absolute;right:-80px;top:-80px;width:320px;height:320px;border-radius:50%;background:radial-gradient(circle,rgba(212,168,67,.18),transparent 70%)}
.blog-hero h1{font-size:2.1rem;font-weight:800;margin-bottom:10px}
.blog-hero .lead{color:rgba(255,255,255,.7);font-size:1rem;max-width:640px;margin-bottom:0}
.blog-stats{display:flex;gap:28px;margin-top:22px;flex-wrap:wrap}
.blog-stat strong{display:block;font-size:1.5rem;font-weight:800;color:#d4a843;line-height:1.1}
.blog-stat span{font-size:.78rem;color:rgba(255,255,255,.6)}
.search-box{position:relative;max-width:500px;margin:26px auto 0}
.search-box input{width:100%;padding:13px 20px 13px 46px;border:2px solid rgba(255,255,255,.15);background:rgba(255,255,255,.08);border-radius:50px;color:#fff;font-size:.95rem;transition:all .3s}
.search-box input::placeholder{color:rgba(255,255,255,.4)}
.search-box input:focus{outline:none;border-color:#d4a843;background:rgba(255,255,255,.12)}
.search-box i{position:absolute;left:18px;top:50%;transform:translateY(-50%);color:rgba(255,255,255,.4);font-size:1.05rem}
.search-box .search-count{position:absolute;right:18px;top:50%;transform:translateY(-50%);color:rgba(255,255,255,.4);font-size:.78rem}
.cat-pills{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;padding:18px 0}
.cat-pill{border:2px solid #dee2e6;background:#fff;border-radius:50px;padding:7px 16px;font-size:.83rem;font-weight:600;cursor:pointer;transition:all .25s;display:inline-flex;align-items:center;gap:6px;color:#495057;user-select:none}
.cat-pill:hover{transform:translateY(-1px);box-shadow:0 4px 12px rgba(0,0,0,.1)}
.cat-pill.active{background:#1a1a2e;color:#fff;border-color:transparent;box-shadow:0 4px 15px rgba(0,0,0,.15)}
.cat-pill .pill-count{background:rgba(0,0,0,.08);border-radius:50px;padding:1px 8px;font-size:.72rem;font-weight:700}
.cat-pill.active .pill-count{background:rgba(255,255,255,.25)}
.cat-section-header{display:flex;align-items:center;gap:12px;margin-bottom:18px;padding-bottom:10px;border-bottom:2px solid #f0f0f0}
.cat-section-header .cat-icon{width:38px;height:38px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1.15rem;flex:0 0 auto}
.cat-section-header h2{font-size:1.2rem;font-weight:700;margin:0;color:#1a1a2e}
.cat-section-header .cat-count{font-size:.8rem;color:#6c757d;margin-left:auto;white-space:nowrap}
/* uniform cards: the anchor must stretch, or cards in a row grow unevenly */
.article-item>a{display:block;height:100%}
.blog-card{background:#fff;border-radius:16px;border:1px solid #e9ecef;transition:transform .25s,box-shadow .25s,border-color .25s;overflow:hidden;height:100%;display:flex;flex-direction:column}
.blog-card:hover{transform:translateY(-4px);box-shadow:0 12px 30px rgba(0,0,0,.1);border-color:#d4a843}
.blog-card .card-body{padding:20px 20px 14px;flex:1;display:flex;flex-direction:column}
.blog-card .card-cat{font-size:.68rem;font-weight:700;padding:3px 11px;border-radius:50px;letter-spacing:.4px;text-transform:uppercase;display:inline-block;align-self:flex-start}
.blog-card .card-title{font-size:1rem;font-weight:700;line-height:1.35;margin:10px 0 7px;color:#1a1a2e;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;min-height:2.7em}
.blog-card:hover .card-title{color:#e8720c}
.blog-card .card-desc{font-size:.85rem;color:#6c757d;line-height:1.5;margin:0;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;min-height:3.8em}
.blog-card .card-footer-custom{padding:12px 20px;border-top:1px solid #f0f0f0;margin-top:auto}
.blog-card .read-more{font-size:.83rem;font-weight:600;color:#e8720c;display:inline-flex;align-items:center;gap:4px;transition:gap .2s}
.blog-card:hover .read-more{gap:9px}
.article-item.extra{display:none}
.cat-section.expanded .article-item.extra{display:block}
.show-all{display:block;margin:14px auto 0;border:2px solid #dee2e6;background:#fff;border-radius:50px;padding:8px 22px;font-size:.85rem;font-weight:600;color:#495057;cursor:pointer;transition:all .2s}
.show-all:hover{border-color:#d4a843;color:#1a1a2e}
.cat-section.expanded .show-all{display:none}
.no-results{text-align:center;padding:60px 20px;color:#6c757d}
.no-results i{font-size:3.4rem;margin-bottom:14px;display:block;color:#dee2e6}
.view-toggle{display:flex;gap:4px;background:#f0f0f0;border-radius:8px;padding:3px}
.view-toggle button{border:none;background:none;padding:6px 10px;border-radius:6px;color:#6c757d;cursor:pointer;transition:all .2s}
.view-toggle button.active{background:#fff;color:#1a1a2e;box-shadow:0 1px 3px rgba(0,0,0,.1)}
.list-view .blog-card .card-desc,.list-view .blog-card .card-footer-custom{display:none}
.list-view .blog-card .card-title{font-size:.93rem;min-height:0;-webkit-line-clamp:2}
.list-view .blog-card .card-body{padding:13px 16px}
.list-view .blog-card .card-cat{font-size:.62rem;padding:2px 8px}
@media(max-width:768px){.blog-hero{padding:34px 0 28px}.blog-hero h1{font-size:1.6rem}.blog-stats{gap:16px}.blog-stat strong{font-size:1.25rem}.cat-pills{gap:6px;padding:12px 0}.cat-pill{padding:6px 12px;font-size:.78rem}.blog-card .card-title{font-size:.95rem}}
</style>"""

SCRIPT = """<script id="blogIndexScript">
function filterCat(cat,btn){
  document.querySelectorAll('.cat-pill').forEach(function(p){p.classList.remove('active');p.style.background='';p.style.borderColor='';p.style.color=''});
  btn.classList.add('active');
  if(cat!=='all'){var c=btn.dataset.color;btn.style.background=c;btn.style.borderColor=c;btn.style.color='#fff'}
  document.querySelectorAll('.article-item').forEach(function(i){i.style.display=''});
  document.querySelectorAll('.cat-section').forEach(function(s){
    var on=(cat==='all'||s.dataset.cat===cat);
    s.style.display=on?'':'none';
    s.classList.toggle('expanded',on&&cat!=='all');
  });
  document.getElementById('searchInput').value='';
  document.getElementById('noResults').style.display='none';
  updateCount();
}
function searchArticles(){
  var q=document.getElementById('searchInput').value.toLowerCase().trim();
  document.querySelectorAll('.cat-pill').forEach(function(p){p.classList.remove('active');p.style.background='';p.style.borderColor='';p.style.color=''});
  var ap=document.querySelector('.cat-pill[data-cat="all"]');if(ap)ap.classList.add('active');
  var shown=0;
  document.querySelectorAll('.article-item').forEach(function(item){
    var hit=!q||item.dataset.title.indexOf(q)>-1||item.dataset.desc.indexOf(q)>-1;
    item.style.display=hit?'':'none';
    if(hit)shown++;
  });
  document.querySelectorAll('.cat-section').forEach(function(s){
    s.classList.toggle('expanded',!!q);
    var v=0;s.querySelectorAll('.article-item').forEach(function(i){if(i.style.display!=='none')v++});
    s.style.display=(q&&!v)?'none':'';
  });
  document.getElementById('noResults').style.display=(q&&!shown)?'block':'none';
  setCount(shown);
}
function setCount(n){var e=document.getElementById('searchCount');if(e)e.textContent=n+' __NOUN__'}
function updateCount(){
  var n=0;document.querySelectorAll('.cat-section').forEach(function(s){
    if(s.style.display!=='none')n+=s.querySelectorAll('.article-item').length});
  setCount(n);
}
function showAll(btn){btn.closest('.cat-section').classList.add('expanded')}
function toggleView(mode,btn){
  var c=document.getElementById('articlesGrid');
  document.querySelectorAll('.view-toggle button').forEach(function(b){b.classList.remove('active')});
  btn.classList.add('active');
  c.classList.toggle('list-view',mode==='list');
}
document.addEventListener('DOMContentLoaded',updateCount);
</script>"""


def rgba(hexcol, a='.08'):
    r, g, b = int(hexcol[1:3], 16), int(hexcol[3:5], 16), int(hexcol[5:7], 16)
    return 'rgba(%d,%d,%d,%s)' % (r, g, b, a)


def clean(t):
    t = re.sub(r'\s+', ' ', html.unescape(t or '')).strip()
    return t


def shorten(t, n):
    if len(t) <= n:
        return t
    cut = t[:n]
    sp = cut.rfind(' ')
    if sp > n * 0.6:
        cut = cut[:sp]
    return cut.rstrip(' ,;.—-') + '…'


def read_article(path):
    with open(path, encoding='utf-8') as f:
        head = f.read(6000)
    m = re.search(r'<title>(.*?)</title>', head, re.S)
    title = clean(m.group(1)) if m else ''
    m = re.search(r'<meta\s+name="description"\s+content="(.*?)"', head, re.S)
    desc = clean(m.group(1)) if m else ''
    for sep in [' | ', ' — Recrea', ' - Recrea']:
        if sep in title:
            title = title.split(sep)[0].strip()
    return title, desc


def classify(slug):
    toks = slug.split('-')
    for key, _c, _i in CATS:
        rules = KW2.get(key)
        if not rules:
            continue
        if any(sub in slug for sub in rules['sub'].split()):
            return key
        kws = rules['tok'].split()
        if any(t.startswith(kw) for t in toks for kw in kws):
            return key
    return 'build'


def build(d):
    cfg = L[d]
    files = sorted(p for p in glob.glob(os.path.join(d, '*.html'))
                   if os.path.basename(p) != 'index.html')
    items = {k: [] for k, _c, _i in CATS}
    for p in files:
        slug = os.path.basename(p)[:-5]
        title, desc = read_article(p)
        if not title:
            continue
        items[classify(slug)].append((slug, title, desc))
    for k in items:
        items[k].sort(key=lambda x: x[1].lower())

    total = sum(len(v) for v in items.values())
    used = [(k, c, i) for k, c, i in CATS if items[k]]

    # ---- hero + toolbar
    st = cfg['st']
    out = ['<section class="blog-hero">',
           '<div class="container position-relative" style="z-index:1">',
           '<div class="row align-items-center">',
           '<div class="col-lg-7">',
           '<h1><i class="bi bi-journal-richtext me-2"></i>%s</h1>' % cfg['h1'],
           '<p class="lead">%s</p>' % cfg['lead'],
           '<div class="blog-stats">',
           '<div class="blog-stat"><strong>%d</strong><span>%s</span></div>' % (total, st[0]),
           '<div class="blog-stat"><strong>%d</strong><span>%s</span></div>' % (len(used), st[1]),
           '<div class="blog-stat"><strong>196+</strong><span>%s</span></div>' % st[2],
           '<div class="blog-stat"><strong>18+</strong><span>%s</span></div>' % st[3],
           '</div></div>',
           '<div class="col-lg-5"><div class="search-box">',
           '<i class="bi bi-search"></i>',
           '<input type="text" id="searchInput" placeholder="%s" oninput="searchArticles()">' % cfg['ph'],
           '<span class="search-count" id="searchCount">%d %s</span>' % (total, cfg['noun']),
           '</div></div></div></div></section>']

    out.append('<div class="container"><div class="d-flex align-items-center justify-content-between flex-wrap gap-2 py-3">')
    out.append('<div class="flex-grow-1"><div class="cat-pills" id="catPills">')
    out.append('<button class="cat-pill active" data-cat="all" onclick="filterCat(\'all\',this)">'
               '<i class="bi bi-grid-3x3-gap me-1"></i>%s<span class="pill-count">%d</span></button>'
               % (cfg['all'], total))
    for k, col, ic in used:
        out.append('<button class="cat-pill" data-cat="cat-%s" data-color="%s" onclick="filterCat(\'cat-%s\',this)">'
                   '<i class="bi %s me-1"></i>%s<span class="pill-count">%d</span></button>'
                   % (k, col, k, ic, cfg['cats'][k], len(items[k])))
    out.append('</div></div>')
    out.append('<div class="view-toggle d-none d-md-flex">'
               '<button class="active" onclick="toggleView(\'grid\',this)" title="Grid"><i class="bi bi-grid-3x3-gap"></i></button>'
               '<button onclick="toggleView(\'list\',this)" title="List"><i class="bi bi-list-ul"></i></button></div>')
    out.append('</div></div>')

    # ---- sections
    out.append('<section class="py-4"><div class="container" id="articlesGrid">')
    out.append('<div id="noResults" style="display:none" class="no-results"><i class="bi bi-search"></i>'
               '<h4>%s</h4><p>%s</p></div>' % cfg['nores'])
    for k, col, ic in used:
        lst = items[k]
        out.append('<div class="cat-section" data-cat="cat-%s">' % k)
        out.append('<div class="cat-section-header"><div class="cat-icon" style="background:%s;color:%s">'
                   '<i class="bi %s"></i></div><h2>%s</h2><span class="cat-count">%d %s</span></div>'
                   % (rgba(col), col, ic, cfg['cats'][k], len(lst), cfg['articles']))
        out.append('<div class="row g-3">')
        for n, (slug, title, desc) in enumerate(lst):
            extra = ' extra' if n >= PER_SECTION else ''
            t = html.escape(shorten(title, 72))
            dsc = html.escape(shorten(desc, 118))
            out.append('<div class="col-md-6 col-lg-4 article-item%s" data-cat="cat-%s" data-title="%s" data-desc="%s">'
                       % (extra, k, html.escape(title.lower(), quote=True), html.escape(desc.lower(), quote=True)))
            out.append('<a href="%s.html" class="text-decoration-none"><div class="blog-card"><div class="card-body">'
                       '<span class="card-cat" style="background:%s;color:%s">%s</span>'
                       '<h3 class="card-title">%s</h3><p class="card-desc">%s</p></div>'
                       '<div class="card-footer-custom"><span class="read-more">%s <i class="bi bi-arrow-right"></i></span>'
                       '</div></div></a></div>'
                       % (slug, rgba(col), col, cfg['cats'][k], t, dsc, cfg['more']))
        out.append('</div>')
        if len(lst) > PER_SECTION:
            out.append('<button class="show-all" onclick="showAll(this)">%s (%d) <i class="bi bi-chevron-down"></i></button>'
                       % (cfg['showall'], len(lst)))
        out.append('</div>')
    out.append('</div></section>')
    return '\n'.join(out), total, {k: len(items[k]) for k, _c, _i in CATS}


def patch(d):
    path = os.path.join(d, 'index.html')
    s = open(path, encoding='utf-8').read()
    grid, total, counts = build(d)

    # 1. style: drop our previous block, insert fresh one right before </head>
    s = re.sub(r'<style id="blogIndexStyle">.*?</style>\s*', '', s, flags=re.S)
    s = s.replace('</head>', STYLE + '\n</head>', 1)

    # 2. replace everything from the hero to the end of the articles grid
    if 'id="articlesGrid"' in s:
        start = s.index('<section class="blog-hero">')
        end = s.index('</div></section>', s.index('id="articlesGrid"')) + len('</div></section>')
    else:  # blog-fr: older layout — swap the whole listing section, keep its CTA tail
        start = s.index('<section class="py-5"><div class="container">')
        end = s.index('<div class="text-center mt-5">', start)
        grid += '\n<section class="py-4"><div class="container">'
    s = s[:start] + grid + s[end:]

    # 3. script: replace old inline filter script, add ours before </body>
    s = re.sub(r'<script id="blogIndexScript">.*?</script>\s*', '', s, flags=re.S)
    s = re.sub(r'<script>\s*function filterCat.*?</script>\s*', '', s, flags=re.S)
    s = s.replace('</body>', SCRIPT.replace('__NOUN__', L[d]['noun']) + '\n</body>', 1)

    open(path, 'w', encoding='utf-8').write(s)
    print('%-8s %3d articles  %s' % (d, total, ' '.join('%s=%d' % (k, v) for k, v in counts.items() if v)))


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for d in DIRS:
        patch(d)
