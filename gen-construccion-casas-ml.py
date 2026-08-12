#!/usr/bin/env python3
"""EN/RU/DE/FR/ZH twins of the ES "construcción de casas en [ciudad]" cluster.

Same obra-nueva angle (price per m² 2026 + 8-step process + what's in/out +
municipal rules + FAQ), one page per language per location, wired into a
6-language hreflang cluster with the ES pages.

Page chrome (top bar, nav, footer, WhatsApp widget) is lifted from an existing
page of the same language so the new pages match the rest of that language's
site; only the language dropdown is rebuilt to point at this cluster.
"""
import os, re, json

BASE = 'https://construction-recrea.com'
WA = 'https://wa.me/529844525333'
# Optional per-location overrides filled in by the zone generators:
#   OVR['h1'|'title'|'desc'|'block'][loc][lang] = str
OVR = {}

# Locations that keep the full body. Everything else (zones and zone villa/hotel
# pages) renders compact: the 8-step process, the included/excluded lists and the
# "why us" bullets live on the parent town page and are linked, not repeated. That
# boilerplate was ~40% of every zone page and carried zero differentiation.
FULL = {'playa-del-carmen', 'cancun', 'tulum', 'puerto-aventuras', 'akumal', 'riviera-maya',
        'isla-mujeres', 'cozumel',
        'vh-playa-del-carmen', 'vh-tulum', 'vh-cancun',
        'vh-puerto-aventuras', 'vh-akumal', 'vh-puerto-morelos'}

# {lang: (process line, includes line, why line)} — the compact replacements
COMPACT_TXT = {
 'es': ('El proceso de obra es el mismo que aplicamos en toda la Riviera Maya: revisión de terreno, anteproyecto, proyecto ejecutivo, permisos, cimentación, obra gris, instalaciones y acabados, y entrega llave en mano. <a href="%s">Vea el proceso completo con tiempos por etapa</a>.',
        'El desglose de <a href="%s">qué incluye y qué no incluye el precio por m²</a> es común a todos nuestros proyectos.',
        'Contrato a precio fijo por partidas, DRO y arquitectos licenciados, trabajadores con IMSS, reportes semanales con foto y video y garantía escrita de un año.'),
 'en': ('The construction process is the same one we run across the Riviera Maya: lot review, concept design, construction documents, permits, foundation, shell, services and finishes, then turnkey handover. <a href="%s">See the full process with per-stage timings</a>.',
        'The breakdown of <a href="%s">what the price per m² includes and excludes</a> is common to all our projects.',
        'Fixed-price contract by line item, licensed DRO and architects, workers registered with IMSS, weekly photo and video reports and a written one-year warranty.'),
 'ru': ('Процесс стройки тот же, что и по всей Ривьере-Майя: проверка участка, эскиз, рабочий проект, разрешения, фундамент, коробка, инженерия и отделка, сдача под ключ. <a href="%s">Посмотреть полный процесс со сроками по этапам</a>.',
        'Разбор того, <a href="%s">что входит и что не входит в цену за м²</a>, одинаков для всех наших проектов.',
        'Договор с фиксированной ценой по статьям, лицензированный DRO и архитекторы, рабочие с IMSS, еженедельные отчёты с фото и видео и письменная гарантия на год.'),
 'de': ('Der Bauablauf ist derselbe wie in der gesamten Riviera Maya: Grundstücksprüfung, Entwurf, Ausführungsplanung, Genehmigungen, Fundament, Rohbau, Installation und Ausbau, schlüsselfertige Übergabe. <a href="%s">Den vollständigen Ablauf mit Zeiten je Phase ansehen</a>.',
        'Die Aufstellung, <a href="%s">was der m²-Preis enthält und was nicht</a>, gilt für alle unsere Projekte.',
        'Festpreisvertrag nach Positionen, lizenzierter DRO und Architekten, bei IMSS angemeldete Arbeiter, wöchentliche Foto- und Videoberichte und ein Jahr schriftliche Garantie.'),
 'fr': ('Le déroulé du chantier est celui que nous appliquons dans toute la Riviera Maya : analyse du terrain, avant-projet, projet d’exécution, permis, fondations, gros œuvre, lots techniques et finitions, puis livraison clé en main. <a href="%s">Voir le déroulé complet avec les délais par étape</a>.',
        'Le détail de <a href="%s">ce que le prix au m² comprend et ne comprend pas</a> est commun à tous nos projets.',
        'Contrat à prix fixe par poste, DRO et architectes agréés, ouvriers déclarés à l’IMSS, rapports hebdomadaires photo et vidéo et garantie écrite d’un an.'),
 'zh': ('施工流程与我们在里维埃拉玛雅各地一致：地块核查、方案设计、施工图、许可办理、基础、主体、机电与装修，最后交钥匙移交。<a href="%s">查看含各阶段工期的完整流程</a>。',
        '<a href="%s">每平方米价格包含与不包含的内容</a>，对我们所有项目均适用。',
        '分项固定总价合同、持照DRO与建筑师、依法参保IMSS的工人、每周照片与视频报告，以及一年书面质保。'),
}

LOCS = ['playa-del-carmen', 'cancun', 'tulum', 'puerto-aventuras', 'akumal', 'riviera-maya']

# ---------------------------------------------------------------- numbers ---
NUM = {
 'playa-del-carmen': dict(m2='$12,000 – $25,000', usd='$650 – $1,380', perm='2–4',
   sizes=[('100', '$1.6M – $2.5M', '$88,000 – $138,000'), ('150', '$2.7M – $4.5M', '$150,000 – $250,000'),
          ('200', '$3.5M – $6M', '$194,000 – $330,000'), ('300', '$7.5M – $13.5M', '$415,000 – $750,000')]),
 'cancun': dict(m2='$11,500 – $24,000', usd='$630 – $1,330', perm='2–4',
   sizes=[('100', '$1.5M – $2.4M', '$83,000 – $132,000'), ('150', '$2.5M – $4.3M', '$140,000 – $238,000'),
          ('200', '$3.3M – $5.7M', '$183,000 – $315,000'), ('300', '$7M – $12.9M', '$390,000 – $715,000')]),
 'tulum': dict(m2='$13,000 – $27,000', usd='$720 – $1,500', perm='3–5',
   sizes=[('100', '$1.7M – $2.7M', '$94,000 – $150,000'), ('150', '$2.9M – $4.9M', '$160,000 – $270,000'),
          ('200', '$3.8M – $6.5M', '$210,000 – $360,000'), ('300', '$8.1M – $14.6M', '$450,000 – $810,000')]),
 'puerto-aventuras': dict(m2='$13,000 – $27,000', usd='$720 – $1,500', perm='2–4',
   sizes=[('100', '$1.7M – $2.7M', '$94,000 – $150,000'), ('150', '$2.9M – $4.9M', '$160,000 – $270,000'),
          ('200', '$3.8M – $6.5M', '$210,000 – $360,000'), ('300', '$8.1M – $14.6M', '$450,000 – $810,000')]),
 'akumal': dict(m2='$13,500 – $28,000', usd='$750 – $1,550', perm='3–5',
   sizes=[('100', '$1.8M – $2.8M', '$100,000 – $155,000'), ('150', '$3.0M – $5.0M', '$166,000 – $277,000'),
          ('200', '$3.9M – $6.7M', '$216,000 – $370,000'), ('300', '$8.4M – $15.1M', '$465,000 – $835,000')]),
 'riviera-maya': dict(m2='$11,500 – $27,000', usd='$630 – $1,500', perm='2–5',
   sizes=[('100', '$1.5M – $2.7M', '$83,000 – $150,000'), ('150', '$2.5M – $4.9M', '$140,000 – $270,000'),
          ('200', '$3.3M – $6.5M', '$183,000 – $360,000'), ('300', '$7M – $14.6M', '$390,000 – $810,000')]),
}

SLUG = {
 'es': {l: 'construccion-de-casas-' + l for l in LOCS},
 'en': {l: 'house-construction-' + l for l in LOCS},
 'ru': {l: 'stroitelstvo-domov-' + l for l in LOCS},
 'de': {l: 'hausbau-' + l for l in LOCS},
 'fr': {l: 'construction-de-maisons-' + l for l in LOCS},
 'zh': {l: 'zhuzhai-jianzao-' + l for l in LOCS},
}
REF = {'en': 'construction-company-cancun', 'ru': 'stroitelnaya-kompaniya-cancun',
       'de': 'bauunternehmen-cancun', 'fr': 'constructeur-cancun', 'zh': 'cancun-jianzhu-gongsi'}
LANGNAME = [('es', 'Español'), ('en', 'English'), ('de', 'Deutsch'), ('ru', 'Русский'), ('zh', '中文'), ('fr', 'Français')]

# --------------------------------------------------------------- language ---
# {city} {m2} {usd} {p150} {perm} {muni} are substituted per location.
L = {
'en': dict(locale='en_US',
  h1='House Construction in {city}',
  title='House Construction in {city} | Recrea',
  desc='Turnkey house construction in {city}: 2026 cost per m², the process step by step, permits and real timelines. Fixed-price contract, 196+ projects.',
  kw='house construction {lcity}, build a house {lcity}, new home construction {lcity}, turnkey house {lcity}, home builder {lcity}',
  lead='Turnkey new builds in {city}: design, permits, foundation, structure and finishes under one contract, one site manager and one fixed price.',
  intro='Recrea has been building houses in {zones} since 2008 — 196+ completed projects across the Riviera Maya. Our architecture, electrical, carpentry and ironwork crews are in-house, so your build does not depend on subcontractors who appear and vanish.',
  alert='<strong>House construction cost in {city} (2026):</strong> {m2} MXN/m² ({usd} USD/m²) depending on finish level, land not included.',
  h_cost='How Much House Construction Costs in {city}',
  cost_p='Real budgets for a completed build, excluding land and furniture. The range depends on the finish level: economy, mid or premium (chukum, hardwood, designer kitchen, infinity pool).',
  th=('House size', 'Construction cost', 'Equivalent'), row='{n} m² house',
  cost_after='Want the exact number for your lot and square metres? Use the <a href="/calculator/">cost calculator</a> or ask us for an itemised quote.',
  h_proc='House Construction Process Step by Step', proc_p='This is how we run every new build, with the timings we actually see in {city}:',
  proc_total='<strong>Total:</strong> 8 to 14 months of construction plus {perm} months of design and permits.',
  h_inc='What the Price per m² Includes — and What It Does Not', inc_t='Included', ninc_t='Not included',
  h_norm='Permits and Building Rules in {city}', h_soil='The lot: what decides your foundation',
  guides='Useful guides: ', h_why='Why Build With Recrea',
  why=['<strong>196+ completed projects</strong> in the Riviera Maya since 2008',
       '<strong>Fixed-price contract</strong> broken down by line item — no surprise overruns',
       '<strong>One company for everything</strong> — architecture, permits, construction, electrical, carpentry, ironwork',
       '<strong>Licensed DRO and architects</strong> — fully legal build, workers registered with IMSS',
       '<strong>Weekly photo and video reports</strong> — built for owners who live abroad',
       '<strong>Written 1-year warranty</strong> on structure and installations'],
  h_proj='Real Projects', h_cta='Free quote for your house in {city}',
  cta_p='196+ completed projects. Fixed-price contracts. We reply in 2 minutes.',
  wa='WhatsApp — 2 min', call='Call: 984 452 5333', form_h='Or send us your project details',
  f_name='Name', f_phone='Phone / WhatsApp', f_msg='Square metres, area of the lot and approximate budget...',
  f_send='Send request', h_faq='Frequently Asked Questions', cta_btn='Get a quote on WhatsApp',
  badges=['Written 1-year warranty', '18+ years', '196+ projects', 'Licensed & DRO', 'Insured'],
  steps=[('Lot review', 'Land use, legal status, utilities and cenote or cavern risk. Before you buy, if you have not bought yet.', '1–2 weeks'),
   ('Concept and budget', 'Layout, massing and a preliminary cost per m². This is where the real scope is set against your budget.', '2–3 weeks'),
   ('Construction documents', 'Architectural, structural, electrical and plumbing drawings signed by a DRO, plus a closed itemised budget.', '4–6 weeks'),
   ('Permits and licences', 'Land use, building licence, DRO, CFE and water hook-ups, environmental permit where required.', '4–20 weeks'),
   ('Foundation', 'Soil mechanics, rock excavation, footings or mat foundation and under-slab services.', '3–5 weeks'),
   ('Shell and structure', 'Structure, walls, slabs and roofs — the stage that decides how the house holds up against hurricanes and salt air.', '10–16 weeks'),
   ('Services and finishes', 'Electrical, plumbing, air conditioning, plaster, floors, carpentry, ironwork, pool and chukum.', '12–20 weeks'),
   ('Turnkey handover', 'Cleaning, systems testing, house manual, as-built drawings and a written 1-year warranty.', '1–2 weeks')],
  inc=['Architectural, structural and MEP design', 'DRO and municipal building licence',
   'Foundation and reinforced concrete structure', 'Electrical, plumbing and air-conditioning installation',
   'Plaster, floors, paint, closet and kitchen carpentry', 'Ironwork, aluminium joinery and anti-corrosion protection',
   'Cistern, water tank and pressure system', 'Final cleaning, testing and written 1-year warranty'],
  ninc=['The land and notary costs', 'Furniture and décor (quoted separately as FF&E)',
   'Pool, landscaping and palapa if not contracted in the package', 'Solar panels, generator or home automation (optional)',
   'Changes you request once construction has started'],
  faq=[('How much does house construction cost in {city}?',
        'From {m2} MXN per m² depending on finish level. A 150 m² house with a pool runs {p150} MXN, land not included.'),
       ('How long does it take to build a house?',
        '8 to 14 months of construction plus {perm} months for design and permits. From first meeting to handover: 12 to 18 months for a 150–200 m² house.'),
       ('Do you work on a fixed price?',
        'Yes. After the construction documents we issue a closed itemised budget and a fixed-price contract with payments tied to verified progress. Only changes you request move the price.'),
       ('Can you build if I live abroad?',
        'Half our clients do. Bilingual fixed-price contract, milestone payments and a weekly photo and video report of real progress on your house.')]),

'ru': dict(locale='ru_RU',
  h1='Строительство домов в {city}',
  title='Строительство домов в {city} | Recrea',
  desc='Дом под ключ в {city}: стоимость за м² 2026, процесс по этапам, разрешения и реальные сроки. Договор с фиксированной ценой, 196+ проектов.',
  kw='строительство домов {lcity}, построить дом {lcity}, дом под ключ {lcity}, строительство дома Мексика',
  lead='Дом под ключ в {city}: проект, разрешения, фундамент, коробка и отделка — один договор, один прораб и фиксированная цена.',
  intro='Recrea строит дома в районах {zones} с 2008 года — 196+ завершённых проектов на Ривьере-Майя. Архитектура, электрика, столярка и металл — свои бригады, поэтому стройка не зависит от подрядчиков, которые появляются и исчезают.',
  alert='<strong>Стоимость строительства дома в {city} (2026):</strong> {m2} MXN/м² ({usd} USD/м²) в зависимости от уровня отделки, без учёта участка.',
  h_cost='Сколько стоит строительство дома в {city}',
  cost_p='Реальные сметы готовой стройки без участка и мебели. Разброс задаёт уровень отделки: эконом, средний или премиум (чукум, твёрдая древесина, авторская кухня, переливной бассейн).',
  th=('Площадь дома', 'Стоимость стройки', 'Эквивалент'), row='Дом {n} м²',
  cost_after='Нужна точная цифра под ваш участок и метраж? Посчитайте в <a href="/kalkulyator/">калькуляторе стоимости</a> или запросите смету по статьям.',
  h_proc='Процесс строительства дома по этапам', proc_p='Так мы ведём каждую стройку, со сроками, которые реально получаются в {city}:',
  proc_total='<strong>Итого:</strong> 8–14 месяцев стройки плюс {perm} месяца на проект и разрешения.',
  h_inc='Что входит в цену за м², а что нет', inc_t='Входит', ninc_t='Не входит',
  h_norm='Разрешения и нормы строительства в {city}', h_soil='Участок: от чего зависит фундамент',
  guides='Полезные материалы: ', h_why='Почему Recrea',
  why=['<strong>196+ завершённых проектов</strong> на Ривьере-Майя с 2008 года',
       '<strong>Договор с фиксированной ценой</strong> по статьям — без внезапных доплат',
       '<strong>Всё в одной компании</strong> — архитектура, разрешения, стройка, электрика, столярка, металл',
       '<strong>Лицензированный DRO и архитекторы</strong> — стройка полностью легальна, рабочие оформлены в IMSS',
       '<strong>Еженедельные отчёты</strong> с фото и видео — если вы живёте не в Мексике',
       '<strong>Письменная гарантия 1 год</strong> на конструктив и инженерию'],
  h_proj='Реальные проекты', h_cta='Бесплатная смета на дом в {city}',
  cta_p='196+ завершённых проектов. Фиксированная цена в договоре. Отвечаем за 2 минуты.',
  wa='WhatsApp — 2 мин', call='Позвонить: 984 452 5333', form_h='Или пришлите детали проекта',
  f_name='Имя', f_phone='Телефон / WhatsApp', f_msg='Метраж, район участка и примерный бюджет...',
  f_send='Отправить заявку', h_faq='Частые вопросы', cta_btn='Запросить смету в WhatsApp',
  badges=['Гарантия 1 год письменно', '18+ лет', '196+ проектов', 'Лицензия и DRO', 'Застрахованы'],
  steps=[('Проверка участка', 'Назначение земли, юридическая чистота, коммуникации и риск сенота или каверны. До покупки, если вы ещё не купили.', '1–2 недели'),
   ('Эскиз и бюджет', 'Планировка, объём и предварительная цена за м². Здесь определяется реальный объём под ваш бюджет.', '2–3 недели'),
   ('Рабочий проект', 'Архитектура, конструктив, электрика и водоснабжение с подписью DRO плюс закрытая смета по статьям.', '4–6 недель'),
   ('Разрешения и лицензии', 'Назначение земли, разрешение на строительство, DRO, подключение CFE и воды, экологическое согласование при необходимости.', '4–20 недель'),
   ('Фундамент', 'Геология, выемка в скале, ленточный фундамент или монолитная плита, инженерия под плитой.', '3–5 недель'),
   ('Коробка', 'Каркас, стены, перекрытия и кровля — этап, который определяет стойкость дома к ураганам и солёному воздуху.', '10–16 недель'),
   ('Инженерия и отделка', 'Электрика, водопровод, кондиционирование, штукатурка, полы, столярка, металл, бассейн и чукум.', '12–20 недель'),
   ('Сдача под ключ', 'Уборка, проверка систем, инструкция по дому, исполнительная документация и письменная гарантия 1 год.', '1–2 недели')],
  inc=['Архитектурный, конструктивный и инженерный проект', 'DRO и муниципальное разрешение на строительство',
   'Фундамент и железобетонный каркас', 'Электрика, водоснабжение и кондиционирование',
   'Штукатурка, полы, покраска, столярка шкафов и кухни', 'Металл, алюминиевые окна и антикоррозийная защита',
   'Цистерна, бак и насосная станция', 'Финальная уборка, испытания и письменная гарантия 1 год'],
  ninc=['Участок и нотариальные расходы', 'Мебель и декор (считаем отдельно как FF&E)',
   'Бассейн, ландшафт и палапа, если не входят в пакет', 'Солнечные панели, генератор, «умный дом» (опции)',
   'Изменения, которые вы вносите уже в ходе стройки'],
  faq=[('Сколько стоит строительство дома в {city}?',
        'От {m2} MXN за м² в зависимости от уровня отделки. Дом 150 м² с бассейном — {p150} MXN, без участка.'),
       ('Сколько времени занимает стройка?',
        '8–14 месяцев строительства плюс {perm} месяца на проект и разрешения. От первой встречи до ключей — 12–18 месяцев для дома 150–200 м².'),
       ('Вы работаете по фиксированной цене?',
        'Да. После рабочего проекта выдаём закрытую смету по статьям и договор с фиксированной ценой, оплата по фактическому этапу. Цену меняют только ваши изменения в ходе стройки.'),
       ('Можно строить, если я живу не в Мексике?',
        'Половина наших клиентов так и делает. Двуязычный договор с фиксированной ценой, оплата по этапам и еженедельный отчёт с фото и видео реального хода стройки.')]),

'de': dict(locale='de_DE',
  h1='Hausbau in {city}',
  title='Hausbau in {city} | Recrea',
  desc='Schlüsselfertiger Hausbau in {city}: Kosten pro m² 2026, Ablauf Schritt für Schritt, Genehmigungen und Bauzeiten. Festpreis, 196+ Projekte.',
  kw='hausbau {lcity}, haus bauen {lcity}, neubau {lcity}, schlüsselfertig bauen {lcity}, hausbau mexiko',
  lead='Schlüsselfertiger Neubau in {city}: Planung, Genehmigungen, Fundament, Rohbau und Ausbau in einem Vertrag, mit einem Bauleiter und einem Festpreis.',
  intro='Recrea baut seit 2008 Häuser in {zones} — 196+ abgeschlossene Projekte in der Riviera Maya. Architektur, Elektrik, Schreinerei und Schlosserei sind eigene Gewerke, Ihr Bau hängt also nicht an Subunternehmern, die kommen und verschwinden.',
  alert='<strong>Hausbaukosten in {city} (2026):</strong> {m2} MXN/m² ({usd} USD/m²) je nach Ausbaustandard, ohne Grundstück.',
  h_cost='Was der Hausbau in {city} kostet',
  cost_p='Reale Budgets für den fertigen Bau, ohne Grundstück und Möblierung. Die Spanne ergibt sich aus dem Ausbaustandard: einfach, mittel oder Premium (Chukum, Hartholz, Designerküche, Infinity-Pool).',
  th=('Hausgröße', 'Baukosten', 'Entspricht'), row='Haus {n} m²',
  cost_after='Sie wollen die genaue Zahl für Ihr Grundstück? Nutzen Sie den <a href="/kostenrechner/">Kostenrechner</a> oder fordern Sie ein Angebot nach Positionen an.',
  h_proc='Hausbau Schritt für Schritt', proc_p='So führen wir jeden Neubau, mit den Zeiten, die in {city} realistisch sind:',
  proc_total='<strong>Gesamt:</strong> 8 bis 14 Monate Bauzeit plus {perm} Monate für Planung und Genehmigungen.',
  h_inc='Was im m²-Preis enthalten ist — und was nicht', inc_t='Enthalten', ninc_t='Nicht enthalten',
  h_norm='Genehmigungen und Bauvorschriften in {city}', h_soil='Das Grundstück: was Ihr Fundament bestimmt',
  guides='Nützliche Leitfäden: ', h_why='Warum mit Recrea bauen',
  why=['<strong>196+ abgeschlossene Projekte</strong> in der Riviera Maya seit 2008',
       '<strong>Festpreisvertrag</strong> nach Positionen — keine bösen Überraschungen',
       '<strong>Alles aus einer Hand</strong> — Architektur, Genehmigungen, Bau, Elektrik, Schreinerei, Schlosserei',
       '<strong>Lizenzierter DRO und Architekten</strong> — 100% legaler Bau, Arbeiter bei IMSS angemeldet',
       '<strong>Wöchentliche Foto- und Videoberichte</strong> — ideal, wenn Sie nicht in Mexiko leben',
       '<strong>Schriftliche Garantie von 1 Jahr</strong> auf Struktur und Installationen'],
  h_proj='Echte Projekte', h_cta='Kostenloses Angebot für Ihr Haus in {city}',
  cta_p='196+ abgeschlossene Projekte. Festpreisverträge. Antwort in 2 Minuten.',
  wa='WhatsApp — 2 Min', call='Anrufen: 984 452 5333', form_h='Oder senden Sie uns Ihre Projektdaten',
  f_name='Name', f_phone='Telefon / WhatsApp', f_msg='Quadratmeter, Lage des Grundstücks und ungefähres Budget...',
  f_send='Anfrage senden', h_faq='Häufige Fragen', cta_btn='Angebot über WhatsApp',
  badges=['1 Jahr schriftliche Garantie', '18+ Jahre', '196+ Projekte', 'Lizenz & DRO', 'Versichert'],
  steps=[('Grundstücksprüfung', 'Nutzungsart, Rechtslage, Versorgung und Risiko von Cenote oder Höhle. Vor dem Kauf, falls noch nicht gekauft.', '1–2 Wochen'),
   ('Entwurf und Budget', 'Grundriss, Baukörper und vorläufiger m²-Preis. Hier wird der reale Umfang zu Ihrem Budget festgelegt.', '2–3 Wochen'),
   ('Ausführungsplanung', 'Architektur-, Statik-, Elektro- und Sanitärpläne mit DRO-Unterschrift plus geschlossenes Angebot nach Positionen.', '4–6 Wochen'),
   ('Genehmigungen', 'Nutzungsart, Baugenehmigung, DRO, CFE- und Wasseranschluss, Umweltgenehmigung falls nötig.', '4–20 Wochen'),
   ('Fundament', 'Bodengutachten, Aushub im Fels, Streifenfundament oder Bodenplatte, Leitungen unter der Platte.', '3–5 Wochen'),
   ('Rohbau', 'Struktur, Wände, Decken und Dächer — die Phase, die über Hurrikan- und Salzluftfestigkeit entscheidet.', '10–16 Wochen'),
   ('Installation und Ausbau', 'Elektrik, Sanitär, Klimaanlage, Putz, Böden, Schreinerei, Schlosserei, Pool und Chukum.', '12–20 Wochen'),
   ('Schlüsselfertige Übergabe', 'Reinigung, Prüfung der Installationen, Hausbuch, Bestandspläne und 1 Jahr schriftliche Garantie.', '1–2 Wochen')],
  inc=['Architektur-, Statik- und Haustechnikplanung', 'DRO und kommunale Baugenehmigung',
   'Fundament und Stahlbetonstruktur', 'Elektro-, Sanitär- und Klimainstallation',
   'Putz, Böden, Anstrich, Schrank- und Küchenschreinerei', 'Schlosserei, Aluminiumfenster und Korrosionsschutz',
   'Zisterne, Wassertank und Druckanlage', 'Endreinigung, Prüfungen und 1 Jahr schriftliche Garantie'],
  ninc=['Grundstück und Notarkosten', 'Möbel und Dekoration (separat als FF&E)',
   'Pool, Garten und Palapa, wenn nicht im Paket', 'Solaranlage, Generator oder Smart Home (optional)',
   'Änderungen, die Sie nach Baubeginn wünschen'],
  faq=[('Was kostet der Hausbau in {city}?',
        'Ab {m2} MXN pro m² je nach Ausbaustandard. Ein Haus mit 150 m² und Pool liegt bei {p150} MXN, ohne Grundstück.'),
       ('Wie lange dauert der Hausbau?',
        '8 bis 14 Monate Bauzeit plus {perm} Monate für Planung und Genehmigungen. Vom Erstgespräch bis zur Übergabe: 12 bis 18 Monate für 150–200 m².'),
       ('Arbeiten Sie zum Festpreis?',
        'Ja. Nach der Ausführungsplanung erhalten Sie ein geschlossenes Angebot nach Positionen und einen Festpreisvertrag mit Zahlungen nach geprüftem Baufortschritt.'),
       ('Können Sie bauen, wenn ich im Ausland lebe?',
        'Die Hälfte unserer Kunden lebt im Ausland. Zweisprachiger Festpreisvertrag, Zahlungen nach Baufortschritt und wöchentlicher Bericht mit Fotos und Video.')]),

'fr': dict(locale='fr_FR',
  h1='Construction de Maisons à {city}',
  title='Construction de Maisons à {city} | Recrea',
  desc='Maison clé en main à {city} : coût au m² 2026, processus étape par étape, permis et délais réels. Contrat à prix fixe, 196+ projets.',
  kw='construction de maisons {lcity}, construire une maison {lcity}, maison clé en main {lcity}, constructeur maison mexique',
  lead='Construction neuve clé en main à {city} : conception, permis, fondations, gros œuvre et finitions dans un seul contrat, avec un seul responsable et un prix fixe.',
  intro='Recrea construit des maisons à {zones} depuis 2008 — 196+ projets livrés dans la Riviera Maya. Architecture, électricité, menuiserie et ferronnerie sont nos propres équipes : votre chantier ne dépend pas de sous-traitants qui apparaissent et disparaissent.',
  alert='<strong>Coût de la construction de maisons à {city} (2026) :</strong> {m2} MXN/m² ({usd} USD/m²) selon le niveau de finition, terrain non compris.',
  h_cost='Combien coûte la construction d’une maison à {city}',
  cost_p='Budgets réels pour une maison livrée, hors terrain et mobilier. La fourchette dépend du niveau de finition : économique, intermédiaire ou premium (chukum, bois dur, cuisine sur mesure, piscine à débordement).',
  th=('Taille de la maison', 'Coût de construction', 'Équivalent'), row='Maison {n} m²',
  cost_after='Vous voulez le chiffre exact pour votre terrain ? Utilisez le <a href="/calculateur/">calculateur de coûts</a> ou demandez un devis détaillé par poste.',
  h_proc='Processus de construction étape par étape', proc_p='Voici comment nous menons chaque chantier neuf, avec les délais réels à {city} :',
  proc_total='<strong>Total :</strong> 8 à 14 mois de chantier plus {perm} mois d’études et de permis.',
  h_inc='Ce que le prix au m² comprend — et ne comprend pas', inc_t='Compris', ninc_t='Non compris',
  h_norm='Permis et règles de construction à {city}', h_soil='Le terrain : ce qui décide vos fondations',
  guides='Guides utiles : ', h_why='Pourquoi construire avec Recrea',
  why=['<strong>196+ projets livrés</strong> dans la Riviera Maya depuis 2008',
       '<strong>Contrat à prix fixe</strong> détaillé par poste — sans dépassements surprises',
       '<strong>Tout dans une seule entreprise</strong> — architecture, permis, chantier, électricité, menuiserie, ferronnerie',
       '<strong>DRO et architectes agréés</strong> — chantier 100% légal, ouvriers déclarés à l’IMSS',
       '<strong>Rapports hebdomadaires</strong> photos et vidéo — pensé pour les propriétaires à l’étranger',
       '<strong>Garantie écrite d’un an</strong> sur la structure et les installations'],
  h_proj='Projets réels', h_cta='Devis gratuit pour votre maison à {city}',
  cta_p='196+ projets livrés. Contrats à prix fixe. Réponse en 2 minutes.',
  wa='WhatsApp — 2 min', call='Appeler : 984 452 5333', form_h='Ou envoyez-nous les détails de votre projet',
  f_name='Nom', f_phone='Téléphone / WhatsApp', f_msg='Surface, secteur du terrain et budget approximatif...',
  f_send='Envoyer la demande', h_faq='Questions fréquentes', cta_btn='Demander un devis sur WhatsApp',
  badges=['Garantie écrite 1 an', '18+ ans', '196+ projets', 'Licence & DRO', 'Assurés'],
  steps=[('Analyse du terrain', 'Usage du sol, situation juridique, réseaux et risque de cénote ou de cavité. Avant l’achat, si ce n’est pas encore fait.', '1–2 semaines'),
   ('Avant-projet et budget', 'Distribution, volumétrie et coût préliminaire au m². C’est ici que le programme réel est calé sur votre budget.', '2–3 semaines'),
   ('Projet d’exécution', 'Plans architecturaux, structure, électricité et plomberie signés par un DRO, plus un devis fermé par poste.', '4–6 semaines'),
   ('Permis et licences', 'Usage du sol, permis de construire, DRO, raccordements CFE et eau, autorisation environnementale si nécessaire.', '4–20 semaines'),
   ('Fondations', 'Étude de sol, excavation dans la roche, semelles ou radier, réseaux sous dalle.', '3–5 semaines'),
   ('Gros œuvre', 'Structure, murs, dalles et toitures — l’étape qui décide de la tenue aux cyclones et à l’air salin.', '10–16 semaines'),
   ('Lots techniques et finitions', 'Électricité, plomberie, climatisation, enduits, sols, menuiserie, ferronnerie, piscine et chukum.', '12–20 semaines'),
   ('Livraison clé en main', 'Nettoyage, essais des installations, carnet de la maison, plans de récolement et garantie écrite d’un an.', '1–2 semaines')],
  inc=['Conception architecturale, structure et fluides', 'DRO et permis de construire municipal',
   'Fondations et structure en béton armé', 'Installation électrique, plomberie et climatisation',
   'Enduits, sols, peinture, menuiserie de placards et cuisine', 'Ferronnerie, menuiserie aluminium et protection anticorrosion',
   'Citerne, réservoir et surpresseur', 'Nettoyage final, essais et garantie écrite d’un an'],
  ninc=['Le terrain et les frais de notaire', 'Mobilier et décoration (chiffrés à part en FF&E)',
   'Piscine, paysagisme et palapa s’ils ne sont pas au contrat', 'Panneaux solaires, groupe électrogène ou domotique (options)',
   'Les modifications demandées une fois le chantier lancé'],
  faq=[('Combien coûte la construction d’une maison à {city} ?',
        'À partir de {m2} MXN le m² selon le niveau de finition. Une maison de 150 m² avec piscine revient à {p150} MXN, hors terrain.'),
       ('Combien de temps dure la construction ?',
        '8 à 14 mois de chantier plus {perm} mois d’études et de permis. Du premier rendez-vous à la remise des clés : 12 à 18 mois pour 150–200 m².'),
       ('Travaillez-vous à prix fixe ?',
        'Oui. Après le projet d’exécution, nous remettons un devis fermé par poste et un contrat à prix fixe avec paiements selon l’avancement vérifié.'),
       ('Pouvez-vous construire si je vis à l’étranger ?',
        'C’est le cas de la moitié de nos clients : contrat bilingue à prix fixe, paiements par étapes et rapport hebdomadaire en photos et vidéo.')]),

'zh': dict(locale='zh_CN',
  h1='{city}住宅建造',
  title='{city}住宅建造 | Recrea',
  desc='{city}交钥匙住宅建造：2026年每平方米造价、分阶段流程、许可与真实工期。固定总价合同，196+个项目。',
  kw='{lcity}建房, {lcity}住宅建造, 墨西哥建房, 交钥匙别墅 {lcity}',
  lead='{city}交钥匙新建住宅：设计、许可、基础、主体与装修由一份合同、一位工程负责人和一个固定总价完成。',
  intro='Recrea 自2008年起在{zones}建造住宅，在里维埃拉玛雅完成196+个项目。建筑设计、电气、木作与铁艺均为自有团队，工程不依赖来去不定的分包商。',
  alert='<strong>{city}住宅建造造价（2026年）：</strong>每平方米 {m2} 比索（{usd} 美元），按装修标准浮动，不含土地。',
  h_cost='{city}建一栋房子要多少钱',
  cost_p='以下是交付标准的真实预算，不含土地与家具。区间取决于装修档次：经济型、中档或高端（chukum 灰泥、硬木、定制厨房、无边泳池）。',
  th=('房屋面积', '建造造价', '折合'), row='{n} 平方米住宅',
  cost_after='想知道您地块的准确数字？使用<a href="/jisuanqi/">造价计算器</a>，或向我们索取分项报价。',
  h_proc='住宅建造流程分步说明', proc_p='我们每个新建项目都按此推进，工期为{city}的真实数据：',
  proc_total='<strong>合计：</strong>施工8至14个月，另加设计与许可{perm}个月。',
  h_inc='每平方米价格包含什么、不包含什么', inc_t='包含', ninc_t='不包含',
  h_norm='{city}的建筑许可与法规', h_soil='地块：决定基础形式的关键',
  guides='实用指南：', h_why='为什么选择 Recrea',
  why=['自2008年起在里维埃拉玛雅<strong>完成196+个项目</strong>',
       '<strong>分项固定总价合同</strong>——不会出现意外超支',
       '<strong>一家公司全包</strong>——建筑设计、许可、施工、电气、木作、铁艺',
       '<strong>持照DRO与建筑师</strong>——工程完全合法，工人依法参保IMSS',
       '<strong>每周照片与视频报告</strong>——专为不在墨西哥的业主设计',
       '<strong>结构与设备一年书面质保</strong>'],
  h_proj='真实项目', h_cta='为您在{city}的住宅免费报价',
  cta_p='196+个已完成项目。固定总价合同。2分钟内回复。',
  wa='WhatsApp — 2分钟', call='致电：984 452 5333', form_h='或发送您的项目信息',
  f_name='姓名', f_phone='电话 / WhatsApp', f_msg='面积、地块位置与大致预算...',
  f_send='提交需求', h_faq='常见问题', cta_btn='通过WhatsApp获取报价',
  badges=['一年书面质保', '18年以上', '196+个项目', '执照与DRO', '已投保'],
  steps=[('地块核查', '土地用途、法律状态、市政接入以及天然井或溶洞风险。若尚未购地，购买前完成。', '1–2周'),
   ('方案与预算', '平面布局、体量与初步每平方米造价。在此阶段把实际规模与您的预算对齐。', '2–3周'),
   ('施工图设计', '建筑、结构、电气与给排水图纸，由DRO签署，并附分项封闭预算。', '4–6周'),
   ('许可与执照', '土地用途、施工许可、DRO、CFE供电与供水接入，必要时办理环保许可。', '4–20周'),
   ('基础工程', '土力学勘察、岩层开挖、条形基础或筏板基础，以及板下管线。', '3–5周'),
   ('主体结构', '结构、墙体、楼板与屋面——决定抗飓风与抗盐蚀性能的阶段。', '10–16周'),
   ('机电与装修', '电气、给排水、空调、抹灰、地面、木作、铁艺、泳池与chukum饰面。', '12–20周'),
   ('交钥匙移交', '清洁、系统调试、房屋手册、竣工图与一年书面质保。', '1–2周')],
  inc=['建筑、结构与机电设计', 'DRO与市政施工许可', '基础与钢筋混凝土结构', '电气、给排水与空调安装',
   '抹灰、地面、涂装、衣柜与厨房木作', '铁艺、铝合金门窗与防腐处理', '蓄水池、水箱与加压系统', '最终清洁、调试与一年书面质保'],
  ninc=['土地与公证费用', '家具与软装（按FF&E单独报价）', '未列入合同的泳池、景观与palapa',
   '太阳能、发电机或智能家居（可选）', '开工后由您提出的变更'],
  faq=[('在{city}建一栋房子要多少钱？',
        '按装修标准，每平方米 {m2} 比索起。150平方米带泳池的住宅约 {p150} 比索，不含土地。'),
       ('建造周期多长？',
        '施工8至14个月，另加设计与许可{perm}个月。从首次沟通到交房，150–200平方米住宅约12至18个月。'),
       ('是否按固定总价施工？',
        '是。施工图完成后提供分项封闭预算与固定总价合同，按核验进度付款。只有您提出的变更会影响价格。'),
       ('我人在国外，可以建房吗？',
        '我们一半客户如此：双语固定总价合同、按进度付款，以及每周施工照片和视频报告。')]),
}

# ---------------------------------------------- per-language, per-location ---
CITY = {
 'en': {'puerto-aventuras': 'Puerto Aventuras', 'akumal': 'Akumal', 'playa-del-carmen': 'Playa del Carmen', 'cancun': 'Cancún', 'tulum': 'Tulum', 'riviera-maya': 'the Riviera Maya'},
 'ru': {'puerto-aventuras': 'Пуэрто-Авентурас', 'akumal': 'Акумале', 'playa-del-carmen': 'Плая-дель-Кармен', 'cancun': 'Канкуне', 'tulum': 'Тулуме', 'riviera-maya': 'Ривьере-Майя'},
 'de': {'puerto-aventuras': 'Puerto Aventuras', 'akumal': 'Akumal', 'playa-del-carmen': 'Playa del Carmen', 'cancun': 'Cancún', 'tulum': 'Tulum', 'riviera-maya': 'der Riviera Maya'},
 'fr': {'puerto-aventuras': 'Puerto Aventuras', 'akumal': 'Akumal', 'playa-del-carmen': 'Playa del Carmen', 'cancun': 'Cancún', 'tulum': 'Tulum', 'riviera-maya': 'la Riviera Maya'},
 'zh': {'puerto-aventuras': 'Puerto Aventuras', 'akumal': 'Akumal', 'playa-del-carmen': '普拉亚德尔卡门', 'cancun': '坎昆', 'tulum': '图卢姆', 'riviera-maya': '里维埃拉玛雅'},
}
ZONES = {
 'en': {'puerto-aventuras': 'the marina district, Xcalacoco, Bahía Chemuyil and the private phases of Puerto Aventuras', 'akumal': 'Akumal Norte, Akumal Pueblo, Aventuras Akumal, Media Luna Bay and Jade Bay', 'playa-del-carmen': 'Playacar, Corasol, Zazil-Ha, Selvamar and Mayakoba',
        'cancun': 'the Supermanzanas, Residencial Cumbres, Puerto Cancún and the Hotel Zone',
        'tulum': 'Aldea Zamá, La Veleta, Región 15 and central Tulum',
        'riviera-maya': 'Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal and Puerto Morelos'},
 'ru': {'puerto-aventuras': 'районе марины, Шкалакоко, Баия-Чемуйиль и частных секторах Пуэрто-Авентурас', 'akumal': 'Акумаль-Норте, Акумаль-Пуэбло, Авентурас-Акумаль, Медиа-Луна и Хейд-Бэй', 'playa-del-carmen': 'Плаякар, Корасоль, Сасиль-Ха, Сельвамар и Майякоба',
        'cancun': 'Супермансанас, Резиденсиаль Кумбрес, Пуэрто-Канкун и Отельная зона',
        'tulum': 'Альдеа-Зама, Ла-Велета, Регион 15 и центр Тулума',
        'riviera-maya': 'Плая-дель-Кармен, Тулум, Канкун, Пуэрто-Авентурас, Акумаль и Пуэрто-Морелос'},
 'de': {'puerto-aventuras': 'dem Marina-Viertel, Xcalacoco, Bahía Chemuyil und den privaten Abschnitten von Puerto Aventuras', 'akumal': 'Akumal Norte, Akumal Pueblo, Aventuras Akumal, Media Luna Bay und Jade Bay', 'playa-del-carmen': 'Playacar, Corasol, Zazil-Ha, Selvamar und Mayakoba',
        'cancun': 'den Supermanzanas, Residencial Cumbres, Puerto Cancún und der Hotelzone',
        'tulum': 'Aldea Zamá, La Veleta, Región 15 und dem Zentrum von Tulum',
        'riviera-maya': 'Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal und Puerto Morelos'},
 'fr': {'puerto-aventuras': 'le quartier de la marina, Xcalacoco, Bahía Chemuyil et les tranches privées de Puerto Aventuras', 'akumal': 'Akumal Norte, Akumal Pueblo, Aventuras Akumal, Media Luna Bay et Jade Bay', 'playa-del-carmen': 'Playacar, Corasol, Zazil-Ha, Selvamar et Mayakoba',
        'cancun': 'les Supermanzanas, Residencial Cumbres, Puerto Cancún et la Zone Hôtelière',
        'tulum': 'Aldea Zamá, La Veleta, Región 15 et le centre de Tulum',
        'riviera-maya': 'Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal et Puerto Morelos'},
 'zh': {'puerto-aventuras': '码头区、Xcalacoco、Bahía Chemuyil 与 Puerto Aventuras 的各私人区段', 'akumal': 'Akumal Norte、Akumal Pueblo、Aventuras Akumal、Media Luna Bay 与 Jade Bay', 'playa-del-carmen': 'Playacar、Corasol、Zazil-Ha、Selvamar 与 Mayakoba',
        'cancun': 'Supermanzanas、Residencial Cumbres、Puerto Cancún 与酒店区',
        'tulum': 'Aldea Zamá、La Veleta、15区与图卢姆市中心',
        'riviera-maya': '普拉亚德尔卡门、图卢姆、坎昆、Puerto Aventuras、Akumal 与 Puerto Morelos'},
}
NORM = {
 'en': {'puerto-aventuras': "Puerto Aventuras belongs to Solidaridad, so land use, the building licence and the DRO are processed in Playa del Carmen. The real difference is inside the gate: as a private community, the project also goes through the estate's administration and design committee, with rules on height, façade, colours, working hours and truck access. We have worked with those by-laws for years and file the full package so you do not lose weeks to review comments.",
        'akumal': 'Akumal belongs to the municipality of Tulum, not Solidaridad — that changes the whole process. On top of land use and the municipal licence with a DRO, most lots need environmental authorisation from SEMA, and beachfront lots add a ZOFEMAT concession. Akumal is a sea-turtle nesting area, so there are restrictions on lighting facing the beach and on night work during nesting season (May–October). Budget 3 to 5 months for permits.',
        'playa-del-carmen': 'In Solidaridad the process starts with the land-use certificate and the current PDU: it sets how many storeys and what building density your lot allows. The building licence requires drawings signed by a DRO registered with the municipality, a structural report and services plans. If the lot borders mangrove, dune or a cenote, a state environmental permit is added.',
        'cancun': 'In Benito Juárez the building licence goes through the Urban Development office with a DRO-endorsed project. Puerto Cancún and the Hotel Zone add FONATUR sign-off and, on beachfront lots, a ZOFEMAT concession. Gated communities such as Cumbres, Aqua and Lagos also run a design committee with height, façade and working-hours rules.',
        'tulum': 'Tulum is the strictest municipality on the coast. On top of land use and the municipal licence with a DRO, most projects need environmental authorisation from SEMA (and an MIA where there is land clearing or proximity to cenotes or mangrove). The PDU caps density and height by zone and requires a minimum permeable green area. Budget 3 to 5 months for permits.',
        'riviera-maya': 'Every municipality has different rules and that is the first source of delays. Solidaridad (Playa del Carmen) works through the PDU and a municipal DRO; Benito Juárez (Cancún) adds FONATUR in Puerto Cancún and the Hotel Zone; Tulum requires SEMA environmental authorisation on most lots; Puerto Morelos, its own municipality since 2016, applies stricter criteria because of the reef. We build in all four and start the right process for your lot.'},
 'ru': {'puerto-aventuras': 'Пуэрто-Авентурас относится к муниципалитету Solidaridad, поэтому назначение земли, разрешение на строительство и DRO оформляются в Плая-дель-Кармен. Разница — внутри посёлка: это закрытая частная община, и проект дополнительно проходит администрацию и комитет по дизайну, с правилами по высоте, фасаду, цветам, времени работ и заезду техники. Мы работаем с этими регламентами много лет и подаём полный пакет, чтобы не терять недели на замечания.',
        'akumal': 'Акумаль относится к муниципалитету Тулум, а не Solidaridad — и это меняет всю процедуру. Помимо назначения земли и муниципальной лицензии с DRO, большинству участков нужно экологическое разрешение SEMA, а на первой линии — концессия ZOFEMAT. Акумаль — зона гнездования морских черепах, поэтому действуют ограничения на освещение в сторону пляжа и на ночные работы в сезон гнездования (май–октябрь). Закладывайте 3–5 месяцев на разрешения.',
        'playa-del-carmen': 'В муниципалитете Solidaridad всё начинается со справки о назначении земли и действующего PDU: он задаёт этажность и плотность застройки для вашего участка. Разрешение на строительство требует проекта с подписью DRO, зарегистрированного в муниципалитете, расчёта конструкций и планов инженерии. Если участок граничит с мангровыми зарослями, дюной или сенотом, добавляется экологическое согласование штата.',
        'cancun': 'В Benito Juárez разрешение выдаёт управление городского развития по проекту с подписью DRO. В Puerto Cancún и Отельной зоне добавляется согласование FONATUR, а на первой линии — концессия ZOFEMAT. В закрытых посёлках (Cumbres, Aqua, Lagos) действует комитет по дизайну с ограничениями по высоте, фасаду и времени работ.',
        'tulum': 'Тулум — самый строгий муниципалитет побережья. Кроме назначения земли и муниципальной лицензии с DRO, большинству проектов нужно экологическое разрешение SEMA (и MIA при расчистке участка или близости сенота либо мангров). PDU ограничивает плотность и высоту по зонам и требует минимальную долю зелёной проницаемой площади. Закладывайте на разрешения 3–5 месяцев.',
        'riviera-maya': 'В каждом муниципалитете свои правила — и это первая причина задержек. Solidaridad (Плая-дель-Кармен) работает через PDU и муниципального DRO; Benito Juárez (Канкун) добавляет FONATUR в Puerto Cancún и Отельной зоне; Тулум требует экологическое разрешение SEMA почти на всех участках; Пуэрто-Морелос, отдельный муниципалитет с 2016 года, применяет более жёсткие критерии из-за рифа. Мы работаем во всех четырёх и запускаем нужную процедуру под ваш участок.'},
 'de': {'puerto-aventuras': 'Puerto Aventuras gehört zur Gemeinde Solidaridad, Nutzungsart, Baugenehmigung und DRO laufen also über Playa del Carmen. Der Unterschied liegt hinter dem Tor: Als private Wohnanlage prüft zusätzlich die Verwaltung und der Gestaltungsbeirat das Projekt — mit Vorgaben zu Höhe, Fassade, Farben, Bauzeiten und Lkw-Zufahrt. Wir arbeiten seit Jahren mit diesen Satzungen und reichen die vollständige Unterlage ein, damit keine Wochen durch Nachforderungen verloren gehen.',
        'akumal': 'Akumal gehört zur Gemeinde Tulum, nicht zu Solidaridad — das ändert das gesamte Verfahren. Neben Nutzungsart und kommunaler Lizenz mit DRO benötigen die meisten Grundstücke eine Umweltgenehmigung der SEMA, Strandgrundstücke zusätzlich eine ZOFEMAT-Konzession. Akumal ist Nistgebiet für Meeresschildkröten: In der Nistzeit (Mai–Oktober) gelten Einschränkungen für strandseitige Beleuchtung und Nachtarbeiten. Kalkulieren Sie 3 bis 5 Monate für Genehmigungen.',
        'playa-del-carmen': 'In Solidaridad beginnt alles mit der Nutzungsbescheinigung und dem geltenden PDU: Er legt Geschosszahl und Bebauungsdichte für Ihr Grundstück fest. Die Baugenehmigung verlangt Pläne mit Unterschrift eines bei der Gemeinde registrierten DRO, einen Statiknachweis und Installationspläne. Grenzt das Grundstück an Mangroven, Düne oder eine Cenote, kommt eine staatliche Umweltgenehmigung hinzu.',
        'cancun': 'In Benito Juárez läuft die Baugenehmigung über die Stadtentwicklungsbehörde mit DRO-geprüftem Projekt. In Puerto Cancún und der Hotelzone kommt die FONATUR-Freigabe dazu, bei Strandgrundstücken die ZOFEMAT-Konzession. In Wohnanlagen wie Cumbres, Aqua oder Lagos entscheidet zusätzlich ein Gestaltungsbeirat über Höhe, Fassade und Bauzeiten.',
        'tulum': 'Tulum ist die strengste Gemeinde der Küste. Neben Nutzungsart und kommunaler Lizenz mit DRO braucht die Mehrzahl der Projekte eine Umweltgenehmigung der SEMA (und eine MIA bei Rodung oder Nähe zu Cenoten und Mangroven). Der PDU begrenzt Dichte und Höhe je Zone und schreibt einen Mindestanteil versickerungsfähiger Grünfläche vor. Kalkulieren Sie 3 bis 5 Monate für Genehmigungen.',
        'riviera-maya': 'Jede Gemeinde hat eigene Regeln — die häufigste Verzögerungsursache. Solidaridad (Playa del Carmen) über PDU und kommunalen DRO; Benito Juárez (Cancún) zusätzlich FONATUR in Puerto Cancún und der Hotelzone; Tulum verlangt bei den meisten Grundstücken die SEMA-Umweltgenehmigung; Puerto Morelos, seit 2016 eigene Gemeinde, ist wegen des Riffs strenger. Wir bauen in allen vieren und starten das passende Verfahren für Ihr Grundstück.'},
 'fr': {'puerto-aventuras': 'Puerto Aventuras dépend de la commune de Solidaridad : usage du sol, permis de construire et DRO se traitent donc à Playa del Carmen. La vraie différence est à l’intérieur : en résidence privée, le projet passe aussi devant l’administration et le comité d’architecture, avec des règles de hauteur, façade, couleurs, horaires de chantier et accès des camions. Nous travaillons avec ces règlements depuis des années et déposons un dossier complet pour ne pas perdre des semaines en observations.',
        'akumal': 'Akumal dépend de la commune de Tulum, et non de Solidaridad — cela change toute la procédure. Outre l’usage du sol et le permis municipal avec DRO, la plupart des terrains exigent une autorisation environnementale de la SEMA, et les lots en front de mer une concession ZOFEMAT. Akumal est une zone de ponte des tortues marines : en saison (mai–octobre), l’éclairage vers la plage et les travaux de nuit sont restreints. Comptez 3 à 5 mois de permis.',
        'playa-del-carmen': 'À Solidaridad, tout commence par le certificat d’usage du sol et le PDU en vigueur : il fixe le nombre de niveaux et la densité constructible de votre terrain. Le permis exige des plans signés par un DRO enregistré à la mairie, une note de structure et les plans des réseaux. Si le terrain jouxte la mangrove, la dune ou un cénote, s’ajoute l’autorisation environnementale de l’État.',
        'cancun': 'À Benito Juárez, le permis passe par la direction du développement urbain avec un projet validé par un DRO. Puerto Cancún et la Zone Hôtelière ajoutent l’accord FONATUR et, en front de mer, la concession ZOFEMAT. Dans les résidences fermées (Cumbres, Aqua, Lagos), un comité d’architecture impose hauteurs, façades et horaires de chantier.',
        'tulum': 'Tulum est la commune la plus stricte de la côte. Outre l’usage du sol et le permis municipal avec DRO, la majorité des projets exige une autorisation environnementale de la SEMA (et une MIA en cas de défrichement ou de proximité d’un cénote ou de la mangrove). Le PDU limite densité et hauteur par zone et impose un pourcentage d’espace vert perméable. Comptez 3 à 5 mois de permis.',
        'riviera-maya': 'Chaque commune a ses règles, et c’est la première source de retards. Solidaridad (Playa del Carmen) fonctionne par le PDU et un DRO municipal ; Benito Juárez (Cancún) ajoute FONATUR à Puerto Cancún et en Zone Hôtelière ; Tulum exige l’autorisation environnementale SEMA sur la plupart des terrains ; Puerto Morelos, commune à part depuis 2016, applique des critères plus stricts à cause du récif. Nous construisons dans les quatre et lançons la procédure adaptée à votre terrain.'},
 'zh': {'puerto-aventuras': 'Puerto Aventuras 隶属 Solidaridad 市，因此土地用途、施工许可与 DRO 均在普拉亚德尔卡门办理。真正的差别在社区内部：作为封闭式私人社区，方案还须经物业管理处与设计委员会审批，对高度、立面、色彩、施工时段和货车进出均有规定。我们长期按这些规约作业，一次性提交完整材料，避免因补件耽误数周。',
        'akumal': 'Akumal 隶属图卢姆市而非 Solidaridad，整个流程因此不同。除土地用途和带 DRO 的市政许可外，多数地块还需 SEMA 环保许可，海滨地块另需 ZOFEMAT 特许。Akumal 是海龟产卵区，产卵季（5月至10月）对朝向沙滩的灯光和夜间施工有限制。许可周期请预留3至5个月。',
        'playa-del-carmen': '在 Solidaridad 市，流程从土地用途证明和现行 PDU 规划开始：它决定您的地块可建层数与建筑密度。施工许可需要由在该市注册的 DRO 签署的图纸、结构计算书与管线图。若地块毗邻红树林、沙丘或天然井（cenote），还需州级环保许可。',
        'cancun': '在 Benito Juárez 市，施工许可由城市发展局审批，项目须由 DRO 背书。Puerto Cancún 与酒店区还需 FONATUR 批准，海滨地块需 ZOFEMAT 特许。Cumbres、Aqua、Lagos 等封闭社区另设设计委员会，对高度、立面与施工时段有明确限制。',
        'tulum': '图卢姆是海岸线上最严格的市镇。除土地用途和带 DRO 的市政许可外，多数项目还需 SEMA 环保许可（涉及清林或临近天然井、红树林时须做 MIA）。PDU 按分区限制密度与高度，并要求保留最低比例的可渗透绿地。许可周期请预留3至5个月。',
        'riviera-maya': '各市镇规则不同，这是延误的首要原因。Solidaridad（普拉亚德尔卡门）走 PDU 与市政 DRO；Benito Juárez（坎昆）在 Puerto Cancún 与酒店区增加 FONATUR；图卢姆多数地块需 SEMA 环保许可；Puerto Morelos 自2016年独立设市，因珊瑚礁保护要求更严。四个市镇我们都在施工，会按您的地块启动对应流程。'},
}
SOIL = {
 'en': {'puerto-aventuras': 'Limestone with a shallow water table and a highly saline environment from the sea and the marina. Beyond the soil study, greater rebar cover, treated ironwork and anodised aluminium joinery are mandatory here: in Puerto Aventuras it is corrosion, not the structure, that ruins badly built houses. Beachfront lots require a ZOFEMAT concession.',
        'akumal': 'Fractured limestone with caverns and cenotes, a shallow water table and heavy salt exposure facing the reef. A geophysical survey up front avoids the worst overrun in the area, and the structure is designed with marine-grade cover and admixtures. Drainage must be solved with a biodigester or a compact treatment plant — discharging badly in Akumal is a serious legal and environmental risk because of the reef.',
        'playa-del-carmen': 'The ground is limestone karst: good bearing capacity, but with hidden cavities and cenotes. That is why we start with a soil-mechanics study — it decides between strip footings, a mat foundation or piles, and prevents the classic overrun of discovering a void once the build is underway.',
        'cancun': 'Limestone with fill areas and a high water table near the Nichupté lagoon. The soil study sets the foundation type and the damp-proofing strategy; on lots near the lagoon, reinforced waterproofing and anti-corrosion protection of the rebar are mandatory.',
        'tulum': 'Fractured limestone with frequent cenotes and caverns, especially in Región 15 and La Veleta. A geophysical survey is not optional here: finding a cavern under the footprint after the foundation has started costs weeks of delay and hundreds of thousands of pesos.',
        'riviera-maya': 'The whole coast sits on limestone with cenotes, caverns and a shallow water table. A soil-mechanics study — plus a geophysical survey where cavern risk exists — decides the foundation and is the best money you will spend on the project.'},
 'ru': {'puerto-aventuras': 'Известняк с высоким уровнем грунтовых вод и агрессивно солёной средой из-за близости моря и марины. Кроме геологии, здесь обязательны увеличенный защитный слой арматуры, металл с антикоррозийной обработкой и анодированный алюминий: в Пуэрто-Авентурас дома убивает не конструктив, а коррозия. На первой линии нужна концессия ZOFEMAT.',
        'akumal': 'Трещиноватый известняк с пещерами и сенотами, высокий уровень грунтовых вод и сильное солевое воздействие напротив рифа. Геофизика до начала работ снимает самый дорогой риск района, а конструктив считается под морскую среду. Канализация — только биодигестер или компактные очистные: неправильный сброс в Акумале это серьёзный юридический и экологический риск из-за рифа.',
        'playa-del-carmen': 'Основание — известняковый карст: несущая способность хорошая, но с пустотами и скрытыми сенотами. Поэтому мы начинаем с геологии — она определяет, будет ли фундамент ленточным, монолитной плитой или на сваях, и снимает классический риск обнаружить каверну уже в ходе стройки.',
        'cancun': 'Известняк с участками насыпного грунта и высоким уровнем грунтовых вод у лагуны Ничупте. Геология определяет тип фундамента и схему гидроизоляции; рядом с лагуной обязательны усиленная гидроизоляция и антикоррозийная защита арматуры.',
        'tulum': 'Трещиноватый известняк с частыми сенотами и пещерами, особенно в Регионе 15 и Ла-Велете. Геофизика здесь не опция: обнаружить пещеру под пятном застройки после начала фундамента — это недели простоя и сотни тысяч песо.',
        'riviera-maya': 'Всё побережье стоит на известняке с сенотами, пещерами и высоким уровнем грунтовых вод. Геология — а там, где есть риск каверн, и геофизика — определяет фундамент и остаётся самой выгодной тратой в проекте.'},
 'de': {'puerto-aventuras': 'Kalkstein mit hohem Grundwasserstand und stark salzhaltiger Umgebung durch Meer und Marina. Neben dem Bodengutachten sind hier größere Betondeckung der Bewehrung, behandelte Schlosserarbeiten und eloxierte Aluminiumfenster Pflicht: In Puerto Aventuras zerstört nicht die Statik, sondern die Korrosion schlecht gebaute Häuser. Strandgrundstücke brauchen eine ZOFEMAT-Konzession.',
        'akumal': 'Zerklüfteter Kalkstein mit Höhlen und Cenoten, hoher Grundwasserstand und starke Salzbelastung gegenüber dem Riff. Eine vorgezogene Geophysik verhindert den teuersten Mehrkostenfall der Region; die Struktur wird mit meerwassertauglicher Deckung und Zusatzmitteln geplant. Die Entwässerung erfolgt über Biodigester oder Kompaktkläranlage — falsche Einleitung ist in Akumal wegen des Riffs ein ernstes rechtliches und ökologisches Risiko.',
        'playa-del-carmen': 'Der Untergrund ist Kalkstein-Karst: gute Tragfähigkeit, aber mit Hohlräumen und verborgenen Cenoten. Deshalb beginnen wir mit einem Bodengutachten — es entscheidet zwischen Streifenfundament, Bodenplatte oder Pfählen und verhindert den klassischen Mehrkostenfall, einen Hohlraum erst während des Baus zu entdecken.',
        'cancun': 'Kalkstein mit Auffüllungen und hohem Grundwasserstand nahe der Nichupté-Lagune. Das Bodengutachten legt Fundamenttyp und Feuchteschutz fest; nahe der Lagune sind verstärkte Abdichtung und Korrosionsschutz der Bewehrung Pflicht.',
        'tulum': 'Zerklüfteter Kalkstein mit häufigen Cenoten und Höhlen, vor allem in Región 15 und La Veleta. Eine geophysikalische Voruntersuchung ist hier keine Option: eine Höhle unter der Gründung zu finden, wenn das Fundament schon läuft, kostet Wochen und Hunderttausende Pesos.',
        'riviera-maya': 'Die gesamte Küste liegt auf Kalkstein mit Cenoten, Höhlen und hohem Grundwasser. Das Bodengutachten — bei Höhlenrisiko plus Geophysik — bestimmt die Gründung und ist die beste Investition im ganzen Projekt.'},
 'fr': {'puerto-aventuras': 'Calcaire avec nappe affleurante et environnement très salin, à cause de la mer et de la marina. Au-delà de l’étude de sol, l’enrobage renforcé des aciers, la ferronnerie traitée et les menuiseries aluminium anodisé sont ici obligatoires : à Puerto Aventuras, ce n’est pas la structure mais la corrosion qui ruine les maisons mal construites. Les lots en front de mer exigent une concession ZOFEMAT.',
        'akumal': 'Calcaire fracturé avec cavernes et cénotes, nappe affleurante et forte exposition saline face au récif. Une étude géophysique préalable évite le pire surcoût de la zone, et la structure est calculée en qualité marine. L’assainissement passe par biodigesteur ou micro-station : un rejet mal conçu à Akumal est un risque juridique et environnemental sérieux à cause du récif.',
        'playa-del-carmen': 'Le sous-sol est un karst calcaire : bonne portance, mais avec des cavités et des cénotes cachés. D’où l’étude de sol dès le départ — elle décide entre semelles filantes, radier ou pieux, et évite le surcoût classique de découvrir un vide une fois le chantier lancé.',
        'cancun': 'Calcaire avec zones de remblai et nappe haute près de la lagune Nichupté. L’étude de sol fixe le type de fondation et le traitement de l’humidité ; près de la lagune, étanchéité renforcée et protection anticorrosion des aciers sont obligatoires.',
        'tulum': 'Calcaire fracturé avec cénotes et cavernes fréquents, surtout en Región 15 et à La Veleta. L’étude géophysique n’est pas optionnelle : découvrir une caverne sous l’emprise une fois les fondations commencées coûte des semaines et des centaines de milliers de pesos.',
        'riviera-maya': 'Toute la côte repose sur du calcaire avec cénotes, cavernes et nappe affleurante. L’étude de sol — complétée d’une géophysique en cas de risque de caverne — décide les fondations et reste le meilleur investissement du projet.'},
 'zh': {'puerto-aventuras': '石灰岩地层，地下水位浅，且因临海与码头而盐分极高。除土力学勘察外，此地必须加大钢筋保护层、铁件做防腐处理、采用阳极氧化铝门窗：在 Puerto Aventuras，毁掉劣质房屋的不是结构而是腐蚀。海滨地块需办理 ZOFEMAT 特许。',
        'akumal': '破碎石灰岩，分布溶洞与天然井，地下水位浅，正对珊瑚礁、盐蚀严重。开工前的地球物理勘探可规避本区最大的超支风险，结构按海洋环境标准设计保护层与外加剂。排水必须采用生物消化池或一体化处理设备——在 Akumal 违规排放，因珊瑚礁而构成严重的法律与环境风险。',
        'playa-del-carmen': '地层为石灰岩喀斯特：承载力良好，但存在空洞和隐蔽的天然井。因此我们先做土力学勘察，据此确定采用条形基础、筏板基础还是桩基，避免开工后才发现溶洞的典型超支。',
        'cancun': '石灰岩夹回填区，靠近 Nichupté 泻湖处地下水位高。勘察决定基础形式与防潮方案；靠近泻湖的地块必须加强防水并对钢筋做防腐处理。',
        'tulum': '破碎石灰岩，天然井与溶洞频发，15区和 La Veleta 尤为明显。此处的地球物理勘探不是可选项：基础开工后才发现溶洞，将造成数周延误和数十万比索损失。',
        'riviera-maya': '整条海岸线均坐落于石灰岩之上，分布天然井、溶洞且地下水位较浅。土力学勘察（有溶洞风险时加做地球物理勘探）决定基础形式，是整个项目最划算的投入。'},
}
EXTRA = {
 'en': {'puerto-aventuras': 'Puerto Aventuras is a gated community with a marina, golf and 24/7 security, in strong demand from foreign owners and vacation rentals: the house is built for guests and for low maintenance while you are away.',
        'akumal': 'Akumal is the most eco-sensitive and the most premium market per m² on the north coast: small-scale builds, longer logistics and a high finish standard (chukum, hardwood, bioclimatic design), with very strong rental demand on the bay.',
        'playa-del-carmen': 'Playa del Carmen is the most balanced market on the coast: land cheaper than Tulum, established local trades and suppliers, and the best cost-to-appreciation ratio whether you build to live or to rent.',
        'cancun': 'Cancún has the most affordable urban land in the north and suppliers 20 minutes from site, which cuts logistics compared with Tulum. It is the lowest cost per built m² on the Riviera Maya.',
        'tulum': 'Tulum is the most expensive m² in the region — logistics, environmental rules and a premium finish standard (chukum, hardwood, bioclimatic design) — and also the strongest vacation-rental yield.',
        'riviera-maya': 'We build along the whole corridor, from Puerto Morelos to Tulum, with one team, one contract and one site manager. The cost gap between the ends of the corridor reaches 15% through logistics and regulation.'},
 'ru': {'puerto-aventuras': 'Пуэрто-Авентурас — закрытая община с мариной, гольфом и охраной 24/7, очень востребованная у иностранцев и в посуточной аренде: дом проектируется под гостей и под низкое обслуживание, когда вас нет.',
        'akumal': 'Акумаль — самый экочувствительный и самый премиальный по цене за м² рынок северного побережья: небольшие объёмы стройки, длинная логистика и высокий стандарт отделки (чукум, твёрдая древесина, биоклиматика) при очень высоком спросе на аренду у бухты.',
        'playa-del-carmen': 'Плая-дель-Кармен — самый сбалансированный рынок побережья: земля дешевле, чем в Тулуме, устоявшиеся местные бригады и поставщики, лучшее соотношение затрат и роста стоимости — и для жизни, и под аренду.',
        'cancun': 'В Канкуне самая доступная городская земля на севере и поставщики в 20 минутах от площадки, что удешевляет логистику по сравнению с Тулумом. Это самая низкая стоимость построенного м² на Ривьере-Майя.',
        'tulum': 'Тулум — самый дорогой м² в регионе: логистика, экологические нормы и премиальный стандарт отделки (чукум, твёрдая древесина, биоклиматика). Одновременно это лучшая доходность в посуточной аренде.',
        'riviera-maya': 'Мы строим по всему коридору — от Пуэрто-Морелоса до Тулума — одной командой, по одному договору и с одним ответственным за объект. Разница в стоимости между концами коридора доходит до 15% из-за логистики и норм.'},
 'de': {'puerto-aventuras': 'Puerto Aventuras ist eine geschlossene Wohnanlage mit Marina, Golf und 24/7-Sicherheit, stark nachgefragt von ausländischen Eigentümern und für Ferienvermietung: Das Haus wird für Gäste und für geringen Unterhalt in Ihrer Abwesenheit geplant.',
        'akumal': 'Akumal ist der ökologisch sensibelste und pro m² teuerste Markt der Nordküste: kleinteiliges Bauen, längere Logistik und ein hoher Ausbaustandard (Chukum, Hartholz, bioklimatisches Design) bei sehr hoher Mietnachfrage an der Bucht.',
        'playa-del-carmen': 'Playa del Carmen ist der ausgewogenste Markt der Küste: günstigeres Land als Tulum, etablierte Handwerker und Lieferanten vor Ort und das beste Verhältnis von Kosten zu Wertsteigerung — ob zum Wohnen oder Vermieten.',
        'cancun': 'Cancún bietet das günstigste Stadtgrundstück im Norden und Lieferanten 20 Minuten von der Baustelle, was die Logistik gegenüber Tulum verbilligt. Der niedrigste Preis pro gebautem m² in der Riviera Maya.',
        'tulum': 'Tulum hat den teuersten m² der Region — Logistik, Umweltauflagen und ein Premium-Ausbaustandard (Chukum, Hartholz, bioklimatisches Design) — dafür die höchste Rendite bei Ferienvermietung.',
        'riviera-maya': 'Wir bauen im gesamten Korridor von Puerto Morelos bis Tulum: ein Team, ein Vertrag, ein Bauleiter. Der Kostenunterschied zwischen den Enden des Korridors erreicht 15% durch Logistik und Vorschriften.'},
 'fr': {'puerto-aventuras': 'Puerto Aventuras est une résidence fermée avec marina, golf et sécurité 24h/24, très demandée par les propriétaires étrangers et la location saisonnière : la maison est conçue pour les hôtes et pour un entretien minimal en votre absence.',
        'akumal': 'Akumal est le marché le plus éco-sensible et le plus premium au m² de la côte nord : chantiers de petite taille, logistique plus longue et standard de finition élevé (chukum, bois dur, conception bioclimatique), avec une très forte demande locative sur la baie.',
        'playa-del-carmen': 'Playa del Carmen est le marché le plus équilibré de la côte : terrain moins cher qu’à Tulum, artisans et fournisseurs locaux établis, et le meilleur rapport coût/plus-value, pour y vivre comme pour louer.',
        'cancun': 'Cancún offre le foncier urbain le plus abordable du nord et des fournisseurs à 20 minutes du chantier, ce qui allège la logistique face à Tulum. C’est le coût au m² construit le plus bas de la Riviera Maya.',
        'tulum': 'Tulum affiche le m² le plus cher de la région — logistique, contraintes environnementales et standard de finition premium (chukum, bois dur, conception bioclimatique) — mais aussi le meilleur rendement locatif saisonnier.',
        'riviera-maya': 'Nous construisons sur tout le corridor, de Puerto Morelos à Tulum, avec une seule équipe, un seul contrat et un seul responsable de chantier. L’écart de coût entre les extrémités atteint 15% selon la logistique et la réglementation.'},
 'zh': {'puerto-aventuras': 'Puerto Aventuras 是配有码头、高尔夫与24小时安保的封闭社区，深受外籍业主与度假出租市场青睐：房屋按接待房客和业主不在时低维护的思路设计。',
        'akumal': 'Akumal 是北部海岸生态最敏感、每平方米最高端的市场：施工体量小、物流路线长、装修标准高（chukum、硬木、生态气候设计），海湾一带出租需求极强。',
        'playa-del-carmen': '普拉亚德尔卡门是海岸线上最均衡的市场：土地比图卢姆便宜，本地工班与供应商成熟，自住或出租的性价比与增值潜力都最好。',
        'cancun': '坎昆拥有北部最实惠的城市用地，供应商距工地仅20分钟，物流成本明显低于图卢姆，是里维埃拉玛雅每平方米建造成本最低的城市。',
        'tulum': '图卢姆是全区每平方米造价最高的市场——物流、环保法规与高端装修标准（chukum、硬木、生态气候设计）共同推高成本，但短租回报也最高。',
        'riviera-maya': '我们在从 Puerto Morelos 到图卢姆的整条走廊施工：一个团队、一份合同、一位现场负责人。因物流与法规差异，走廊两端的造价差异可达15%。'},
}
# 2 extra location-specific FAQ per language/location
FAQX = {
 'en': {'puerto-aventuras': [('How do permits work inside the gated community?', 'Two tracks: the municipal licence in Solidaridad (land use, DRO, building licence) and approval from the Puerto Aventuras design committee. We file both and coordinate access and working hours with the administration.'), ('What extra protection does being next to the sea and the marina require?', 'Greater rebar cover, anti-corrosion treated ironwork, anodised aluminium joinery, reinforced waterproofing and marine-rated A/C equipment. It is part of our standard build spec here.')],
        'akumal': [('Why is Akumal more expensive than Playa del Carmen?', 'SEMA environmental processing, longer logistics from suppliers, turtle and reef protection, and a higher finish standard. The construction gap is around 10–12%.'), ('Are there sea-turtle restrictions?', 'Yes. During nesting season (May–October) lighting aimed at the beach and night work on coastal lots are restricted. We design the lighting scheme from day one to comply without compromising the house.')],
        'playa-del-carmen': [('Do you handle the permits?', 'Yes: land use, the Solidaridad building licence, DRO, CFE and water hook-ups, plus the environmental permit if the lot needs one.'),
        ('Is the architectural design included?', 'Yes — architectural, structural and MEP design in-house. If you already have drawings we review them and quote the build directly.')],
        'cancun': [('Is building in Cancún cheaper than in Playa del Carmen?', 'Yes, 3% to 5% cheaper on construction: closer suppliers, more available labour and more affordable urban land outside Puerto Cancún and the Hotel Zone.'),
        ('Do you build inside gated communities with design rules?', 'Yes. We present the project to the design committee and coordinate access, working hours and deliveries with the HOA.')],
        'tulum': [('Why does building in Tulum cost more?', 'Environmental regulation (SEMA/MIA), longer logistics from suppliers, lots with cenotes and caverns, and a higher finish standard than the rest of the coast.'),
        ('Can I rent the house on Airbnb?', 'Yes, and we design for it: guest-friendly layout, pool, FF&E package and the operating licence if it runs as a vacation rental.')],
        'riviera-maya': [('Which town should I build in?', 'Cancún and Puerto Morelos for cost, Playa del Carmen for the balance of price and appreciation, Tulum for rental yield. We give you the numbers before you buy the lot.'),
        ('Do you check the lot before I buy it?', 'Yes: land use, legal status, cenote or cavern risk and utility feasibility. It is the cheapest check you will run on the whole project.')]},
 'ru': {'puerto-aventuras': [('Как устроены разрешения внутри закрытого посёлка?', 'Два трека: муниципальная лицензия в Solidaridad (назначение земли, DRO, разрешение на строительство) и одобрение комитета по дизайну Пуэрто-Авентурас. Мы подаём оба пакета и согласуем доступ и часы работ с администрацией.'), ('Что дополнительно требуется рядом с морем и мариной?', 'Увеличенный защитный слой арматуры, антикоррозийная обработка металла, анодированный алюминий, усиленная гидроизоляция и кондиционеры в морском исполнении. У нас это входит в стандарт стройки.')],
        'akumal': [('Почему в Акумале дороже, чем в Плая-дель-Кармен?', 'Экологическое согласование SEMA, длинная логистика от поставщиков, защита черепах и рифа, более высокий стандарт отделки. Разница по стройке — около 10–12%.'), ('Есть ли ограничения из-за морских черепах?', 'Да. В сезон гнездования (май–октябрь) ограничено освещение в сторону пляжа и ночные работы на прибрежных участках. Схему освещения проектируем сразу так, чтобы соответствовать нормам без ущерба для дома.')],
        'playa-del-carmen': [('Разрешения оформляете вы?', 'Да: назначение земли, разрешение на строительство в Solidaridad, DRO, подключение CFE и воды, а также экологическое согласование, если участок этого требует.'),
        ('Проект входит в стоимость?', 'Да — архитектура, конструктив и инженерия делаются у нас. Если у вас уже есть проект, мы его проверяем и считаем сразу стройку.')],
        'cancun': [('Строить в Канкуне дешевле, чем в Плая-дель-Кармен?', 'Да, на 3–5% по стройке: ближе поставщики, больше доступных бригад и дешевле городская земля за пределами Puerto Cancún и Отельной зоны.'),
        ('Строите в закрытых посёлках с регламентом?', 'Да. Подаём проект в комитет по дизайну и согласуем с администрацией доступ, часы работ и поставки.')],
        'tulum': [('Почему в Тулуме дороже?', 'Экологические нормы (SEMA/MIA), более длинная логистика от поставщиков, участки с сенотами и пещерами и более высокий стандарт отделки, чем на остальном побережье.'),
        ('Можно ли сдавать дом на Airbnb?', 'Да, и мы сразу это закладываем: планировка под гостей, бассейн, комплект мебели FF&E и лицензия на деятельность, если дом работает как посуточная аренда.')],
        'riviera-maya': [('Где выгоднее строить?', 'Канкун и Пуэрто-Морелос — по цене; Плая-дель-Кармен — по балансу стоимости и роста цены; Тулум — по доходности аренды. Цифры даём до покупки участка.'),
        ('Проверяете участок до покупки?', 'Да: назначение земли, юридическая чистота, риск сенота или каверны и возможность подключения. Самая дешёвая проверка во всём проекте.')]},
 'de': {'puerto-aventuras': [('Wie laufen die Genehmigungen in der geschlossenen Anlage?', 'Zweigleisig: kommunale Lizenz in Solidaridad (Nutzungsart, DRO, Baugenehmigung) und Freigabe durch den Gestaltungsbeirat von Puerto Aventuras. Wir reichen beides ein und stimmen Zufahrt und Bauzeiten mit der Verwaltung ab.'), ('Was verlangt die Lage an Meer und Marina zusätzlich?', 'Größere Betondeckung, korrosionsgeschützte Schlosserarbeiten, eloxiertes Aluminium, verstärkte Abdichtung und seeluftgeeignete Klimageräte. Das gehört hier zu unserem Baustandard.')],
        'akumal': [('Warum ist Akumal teurer als Playa del Carmen?', 'SEMA-Umweltverfahren, längere Logistik, Schildkröten- und Riffschutz sowie ein höherer Ausbaustandard. Der Bauunterschied liegt bei etwa 10–12%.'), ('Gibt es Auflagen wegen der Meeresschildkröten?', 'Ja. In der Nistzeit (Mai–Oktober) sind strandseitige Beleuchtung und Nachtarbeiten auf Küstengrundstücken eingeschränkt. Das Lichtkonzept planen wir von Anfang an regelkonform.')],
        'playa-del-carmen': [('Übernehmen Sie die Genehmigungen?', 'Ja: Nutzungsart, Baugenehmigung in Solidaridad, DRO, CFE- und Wasseranschluss sowie die Umweltgenehmigung, falls das Grundstück sie braucht.'),
        ('Ist die Planung enthalten?', 'Ja — Architektur, Statik und Haustechnik im Haus. Wenn Sie bereits Pläne haben, prüfen wir sie und kalkulieren direkt den Bau.')],
        'cancun': [('Ist Bauen in Cancún günstiger als in Playa del Carmen?', 'Ja, 3 bis 5% günstiger: nähere Lieferanten, mehr verfügbare Arbeitskräfte und günstigeres Stadtgrundstück außerhalb von Puerto Cancún und der Hotelzone.'),
        ('Bauen Sie in Wohnanlagen mit Gestaltungsbeirat?', 'Ja. Wir legen das Projekt dem Beirat vor und stimmen Zufahrt, Bauzeiten und Lieferungen mit der Verwaltung ab.')],
        'tulum': [('Warum ist Bauen in Tulum teurer?', 'Umweltauflagen (SEMA/MIA), längere Logistik, Grundstücke mit Cenoten und Höhlen sowie ein höherer Ausbaustandard als an der übrigen Küste.'),
        ('Kann ich das Haus über Airbnb vermieten?', 'Ja, und wir planen es dafür: gästetaugliche Aufteilung, Pool, FF&E-Paket und die Betriebslizenz, wenn es als Ferienvermietung läuft.')],
        'riviera-maya': [('Wo sollte ich bauen?', 'Cancún und Puerto Morelos nach Kosten, Playa del Carmen nach Preis-Wertsteigerungs-Verhältnis, Tulum nach Mietrendite. Die Zahlen bekommen Sie vor dem Grundstückskauf.'),
        ('Prüfen Sie das Grundstück vor dem Kauf?', 'Ja: Nutzungsart, Rechtslage, Cenoten- und Höhlenrisiko sowie Versorgungssicherheit. Die günstigste Prüfung im ganzen Projekt.')]},
 'fr': {'puerto-aventuras': [('Comment fonctionnent les permis dans la résidence fermée ?', 'Deux voies : le permis municipal à Solidaridad (usage du sol, DRO, permis de construire) et l’accord du comité d’architecture de Puerto Aventuras. Nous déposons les deux et coordonnons accès et horaires avec l’administration.'), ('Qu’exige la proximité de la mer et de la marina ?', 'Enrobage renforcé des aciers, ferronnerie traitée anticorrosion, menuiseries aluminium anodisé, étanchéité renforcée et climatisation qualifiée bord de mer. C’est inclus dans notre standard ici.')],
        'akumal': [('Pourquoi Akumal coûte-t-il plus cher que Playa del Carmen ?', 'Procédure environnementale SEMA, logistique plus longue, protection des tortues et du récif, et standard de finition supérieur. L’écart de chantier tourne autour de 10–12%.'), ('Y a-t-il des contraintes liées aux tortues marines ?', 'Oui. En saison de ponte (mai–octobre), l’éclairage vers la plage et les travaux de nuit sont restreints sur les lots côtiers. Nous concevons l’éclairage dès le départ pour être conformes.')],
        'playa-del-carmen': [('Gérez-vous les permis ?', 'Oui : usage du sol, permis de construire à Solidaridad, DRO, raccordements CFE et eau, ainsi que l’autorisation environnementale si le terrain l’exige.'),
        ('La conception est-elle incluse ?', 'Oui — architecture, structure et fluides en interne. Si vous avez déjà des plans, nous les vérifions et chiffrons directement le chantier.')],
        'cancun': [('Construire à Cancún coûte-t-il moins cher qu’à Playa del Carmen ?', 'Oui, 3 à 5% de moins sur le chantier : fournisseurs plus proches, main-d’œuvre plus disponible et foncier urbain plus accessible hors Puerto Cancún et Zone Hôtelière.'),
        ('Construisez-vous en résidence fermée avec règlement ?', 'Oui. Nous présentons le projet au comité d’architecture et coordonnons accès, horaires et livraisons avec l’administration.')],
        'tulum': [('Pourquoi construire à Tulum coûte-t-il plus cher ?', 'Réglementation environnementale (SEMA/MIA), logistique plus longue, terrains avec cénotes et cavernes, et un standard de finition supérieur au reste de la côte.'),
        ('Puis-je louer la maison sur Airbnb ?', 'Oui, et nous la concevons pour cela : distribution adaptée aux hôtes, piscine, pack FF&E et licence d’exploitation si elle fonctionne en location saisonnière.')],
        'riviera-maya': [('Où vaut-il mieux construire ?', 'Cancún et Puerto Morelos pour le coût, Playa del Carmen pour l’équilibre prix/plus-value, Tulum pour le rendement locatif. Nous donnons les chiffres avant l’achat du terrain.'),
        ('Vérifiez-vous le terrain avant l’achat ?', 'Oui : usage du sol, situation juridique, risque de cénote ou de cavité et faisabilité des réseaux. La vérification la moins chère de tout le projet.')]},
 'zh': {'puerto-aventuras': [('封闭社区内的许可如何办理？', '两条线并行：Solidaridad 市政许可（土地用途、DRO、施工许可）与 Puerto Aventuras 设计委员会审批。两套材料我们都负责报审，并与物业协调出入与施工时段。'), ('紧邻大海与码头需要哪些额外防护？', '加大钢筋保护层、铁件防腐处理、阳极氧化铝门窗、加强防水以及适用于海边环境的空调设备。这些均包含在我们本地的施工标准中。')],
        'akumal': [('为什么 Akumal 比普拉亚德尔卡门贵？', 'SEMA 环保审批、供应链距离更远、海龟与珊瑚礁保护要求，以及更高的装修标准。施工造价差约为10%至12%。'), ('海龟保护有哪些限制？', '有。产卵季（5月至10月）沿海地块朝向沙滩的照明与夜间施工受限。我们从设计之初就规划照明方案，在合规的同时不牺牲居住品质。')],
        'playa-del-carmen': [('许可由你们办理吗？', '是。土地用途、Solidaridad 市施工许可、DRO、CFE 供电与供水接入，若地块需要还包括环保许可。'),
        ('设计包含在内吗？', '包含——建筑、结构与机电设计均由我们内部完成。如果您已有图纸，我们审核后直接报价施工。')],
        'cancun': [('在坎昆建房比普拉亚德尔卡门便宜吗？', '是的，施工成本低3%至5%：供应商更近、工人更充足，且 Puerto Cancún 与酒店区之外的城市用地更便宜。'),
        ('封闭社区有规约，你们能施工吗？', '可以。我们向设计委员会报审方案，并与物业协调出入、施工时段与材料进场。')],
        'tulum': [('为什么图卢姆造价更高？', '环保法规（SEMA/MIA）、供应链距离更远、地块存在天然井与溶洞，以及高于海岸其他地区的装修标准。'),
        ('房子可以做 Airbnb 出租吗？', '可以，我们按此设计：适合房客的动线、泳池、FF&E 家具包，以及作为度假租赁运营所需的经营许可。')],
        'riviera-maya': [('在哪个城市建房更合适？', '论成本选坎昆与 Puerto Morelos；论价格与增值平衡选普拉亚德尔卡门；论租金回报选图卢姆。买地之前我们就给您具体数字。'),
        ('买地前你们会核查地块吗？', '会：土地用途、法律状态、天然井或溶洞风险以及市政接入可行性。这是整个项目中最便宜的一道核查。')]},
}
LINKS = {
 'en': {'puerto-aventuras': [('/construction-company-puerto-aventuras/', 'Construction company in Puerto Aventuras'), ('/construction-permits-puerto-aventuras/', 'Construction permits in Puerto Aventuras'), ('/luxury-villas-puerto-aventuras/', 'Luxury villas in Puerto Aventuras'), ('/condo-renovation-puerto-aventuras/', 'Condo renovation'), ('/calculator/', 'Cost calculator'), ('/house-construction-riviera-maya/', 'House construction in the Riviera Maya')],
        'akumal': [('/construction-company-akumal/', 'Construction company in Akumal'), ('/construction-permits-akumal/', 'Construction permits in Akumal'), ('/luxury-villas-akumal/', 'Luxury villas in Akumal'), ('/airbnb-investment-villa-construction-akumal/', 'Airbnb investment villa in Akumal'), ('/calculator/', 'Cost calculator'), ('/house-construction-riviera-maya/', 'House construction in the Riviera Maya')],
        'playa-del-carmen': [('/cost-to-build-house-playa-del-carmen/', 'How much does it cost to build a house?'), ('/construction-permits-playa-del-carmen/', 'Construction permits in Playa del Carmen'), ('/construction-companies-playa-del-carmen/', 'Construction companies in Playa del Carmen'), ('/luxury-villa-construction-playa-del-carmen/', 'Luxury villas'), ('/calculator/', 'Cost calculator'), ('/blog/', 'Construction guides')],
        'cancun': [('/construction-company-cancun/', 'Construction company in Cancún'), ('/construction-permits-cancun/', 'Construction permits in Cancún'), ('/luxury-villas-puerto-cancun/', 'Luxury villas in Puerto Cancún'), ('/home-renovation-cancun/', 'Home renovation in Cancún'), ('/calculator/', 'Cost calculator'), ('/blog/', 'Construction guides')],
        'tulum': [('/construction-company-tulum/', 'Construction company in Tulum'), ('/construction-permits-tulum-city/', 'Construction permits in Tulum'), ('/luxury-villas-aldea-zama-tulum/', 'Luxury villas in Aldea Zamá'), ('/eco-lodge-wellness-retreat-construction-tulum/', 'Eco-lodges and retreats'), ('/calculator/', 'Cost calculator'), ('/blog/', 'Construction guides')],
        'riviera-maya': [('/house-construction-puerto-aventuras/', 'House construction in Puerto Aventuras'), ('/house-construction-akumal/', 'House construction in Akumal'), ('/construction-company-riviera-maya/', 'Construction company in the Riviera Maya'), ('/house-construction-playa-del-carmen/', 'House construction in Playa del Carmen'), ('/house-construction-cancun/', 'House construction in Cancún'), ('/house-construction-tulum/', 'House construction in Tulum'), ('/construction-permits-licenses-riviera-maya/', 'Permits, licences and DRO'), ('/turnkey-construction-for-foreigners-riviera-maya/', 'Turnkey construction for foreigners')]},
 'ru': {'puerto-aventuras': [('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'), ('/stroitelstvo-vill-playa-del-carmen/', 'Строительство вилл'), ('/kalkulyator/', 'Калькулятор стоимости'), ('/stroitelstvo-domov-riviera-maya/', 'Строительство домов на Ривьере-Майя'), ('/blog-ru/', 'Гиды по строительству')],
        'akumal': [('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'), ('/blog-ru/skolko-stoit-postroit-dom-akumal.html', 'Сколько стоит построить дом в Акумале'), ('/kalkulyator/', 'Калькулятор стоимости'), ('/stroitelstvo-domov-riviera-maya/', 'Строительство домов на Ривьере-Майя'), ('/blog-ru/', 'Гиды по строительству')],
        'playa-del-carmen': [('/skolko-stoit-postroit-dom-playa-del-carmen/', 'Сколько стоит построить дом'), ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'), ('/stroitelstvo-vill-playa-del-carmen/', 'Строительство вилл'), ('/remont-domov-playa-del-carmen/', 'Ремонт домов'), ('/kalkulyator/', 'Калькулятор стоимости'), ('/blog-ru/', 'Гиды по строительству')],
        'cancun': [('/stroitelnaya-kompaniya-cancun/', 'Строительная компания в Канкуне'), ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения и лицензии'), ('/blog-ru/razresheniya-na-stroitelstvo-cancun.html', 'Разрешения на строительство в Канкуне'), ('/kalkulyator/', 'Калькулятор стоимости'), ('/blog-ru/', 'Гиды по строительству')],
        'tulum': [('/stroitelnaya-kompaniya-tulum/', 'Строительная компания в Тулуме'), ('/blog-ru/razresheniya-na-stroitelstvo-tulum.html', 'Разрешения на строительство в Тулуме'), ('/blog-ru/ekologichnoe-stroitelstvo-tulum.html', 'Экологичное строительство'), ('/kalkulyator/', 'Калькулятор стоимости'), ('/blog-ru/', 'Гиды по строительству')],
        'riviera-maya': [('/stroitelstvo-domov-puerto-aventuras/', 'Строительство домов в Пуэрто-Авентурас'), ('/stroitelstvo-domov-akumal/', 'Строительство домов в Акумале'), ('/stroitelstvo-domov-playa-del-carmen/', 'Строительство домов в Плая-дель-Кармен'), ('/stroitelstvo-domov-cancun/', 'Строительство домов в Канкуне'), ('/stroitelstvo-domov-tulum/', 'Строительство домов в Тулуме'), ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'), ('/kalkulyator/', 'Калькулятор стоимости'), ('/blog-ru/', 'Гиды по строительству')]},
 'de': {'puerto-aventuras': [('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen, Lizenzen und DRO'), ('/luxusvilla-bau-playa-del-carmen/', 'Luxusvillen'), ('/kostenrechner/', 'Kostenrechner'), ('/hausbau-riviera-maya/', 'Hausbau in der Riviera Maya'), ('/blog-de/', 'Bau-Leitfäden')],
        'akumal': [('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen, Lizenzen und DRO'), ('/blog-de/hausbau-kosten-akumal.html', 'Hausbaukosten in Akumal'), ('/kostenrechner/', 'Kostenrechner'), ('/hausbau-riviera-maya/', 'Hausbau in der Riviera Maya'), ('/blog-de/', 'Bau-Leitfäden')],
        'playa-del-carmen': [('/hausbau-kosten-playa-del-carmen/', 'Was kostet ein Hausbau?'), ('/baugenehmigungen-lizenzen-riviera-maya/', 'Baugenehmigungen, Lizenzen und DRO'), ('/luxusvilla-bau-playa-del-carmen/', 'Luxusvillen'), ('/hausrenovierung-playa-del-carmen/', 'Hausrenovierung'), ('/kostenrechner/', 'Kostenrechner'), ('/blog-de/', 'Bau-Leitfäden')],
        'cancun': [('/bauunternehmen-cancun/', 'Bauunternehmen in Cancún'), ('/blog-de/baugenehmigungen-cancun.html', 'Baugenehmigungen in Cancún'), ('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen und DRO'), ('/kostenrechner/', 'Kostenrechner'), ('/blog-de/', 'Bau-Leitfäden')],
        'tulum': [('/bauunternehmen-tulum/', 'Bauunternehmen in Tulum'), ('/blog-de/baugenehmigungen-tulum.html', 'Baugenehmigungen in Tulum'), ('/blog-de/nachhaltiges-bauen-tulum.html', 'Nachhaltiges Bauen'), ('/kostenrechner/', 'Kostenrechner'), ('/blog-de/', 'Bau-Leitfäden')],
        'riviera-maya': [('/hausbau-puerto-aventuras/', 'Hausbau in Puerto Aventuras'), ('/hausbau-akumal/', 'Hausbau in Akumal'), ('/hausbau-playa-del-carmen/', 'Hausbau in Playa del Carmen'), ('/hausbau-cancun/', 'Hausbau in Cancún'), ('/hausbau-tulum/', 'Hausbau in Tulum'), ('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen, Lizenzen und DRO'), ('/kostenrechner/', 'Kostenrechner'), ('/blog-de/', 'Bau-Leitfäden')]},
 'fr': {'puerto-aventuras': [('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'), ('/construction-villa-luxe-playa-del-carmen/', 'Villas de luxe'), ('/calculateur/', 'Calculateur de coûts'), ('/construction-de-maisons-riviera-maya/', 'Construction de maisons dans la Riviera Maya'), ('/blog-fr/', 'Guides de construction')],
        'akumal': [('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'), ('/blog-fr/cout-construire-maison-akumal.html', 'Coût pour construire à Akumal'), ('/calculateur/', 'Calculateur de coûts'), ('/construction-de-maisons-riviera-maya/', 'Construction de maisons dans la Riviera Maya'), ('/blog-fr/', 'Guides de construction')],
        'playa-del-carmen': [('/prix-construction-maison-playa-del-carmen/', 'Prix de construction d’une maison'), ('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'), ('/construction-villa-luxe-playa-del-carmen/', 'Villas de luxe'), ('/renovation-maison-playa-del-carmen/', 'Rénovation de maison'), ('/calculateur/', 'Calculateur de coûts'), ('/blog-fr/', 'Guides de construction')],
        'cancun': [('/constructeur-cancun/', 'Constructeur à Cancún'), ('/blog-fr/permis-construction-cancun.html', 'Permis de construire à Cancún'), ('/permis-et-licences-construction-riviera-maya/', 'Permis et DRO'), ('/calculateur/', 'Calculateur de coûts'), ('/blog-fr/', 'Guides de construction')],
        'tulum': [('/constructeur-tulum/', 'Constructeur à Tulum'), ('/blog-fr/permis-construction-tulum.html', 'Permis de construire à Tulum'), ('/blog-fr/construction-durable-tulum.html', 'Construction durable'), ('/calculateur/', 'Calculateur de coûts'), ('/blog-fr/', 'Guides de construction')],
        'riviera-maya': [('/construction-de-maisons-puerto-aventuras/', 'Construction de maisons à Puerto Aventuras'), ('/construction-de-maisons-akumal/', 'Construction de maisons à Akumal'), ('/construction-de-maisons-playa-del-carmen/', 'Construction de maisons à Playa del Carmen'), ('/construction-de-maisons-cancun/', 'Construction de maisons à Cancún'), ('/construction-de-maisons-tulum/', 'Construction de maisons à Tulum'), ('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'), ('/calculateur/', 'Calculateur de coûts'), ('/blog-fr/', 'Guides de construction')]},
 'zh': {'puerto-aventuras': [('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO'), ('/haohua-bieshu-playa-del-carmen/', '豪华别墅'), ('/jisuanqi/', '造价计算器'), ('/zhuzhai-jianzao-riviera-maya/', '里维埃拉玛雅住宅建造'), ('/blog-zh/', '建筑指南')],
        'akumal': [('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO'), ('/blog-zh/akumal-jianfang-chengben.html', 'Akumal 建房成本'), ('/jisuanqi/', '造价计算器'), ('/zhuzhai-jianzao-riviera-maya/', '里维埃拉玛雅住宅建造'), ('/blog-zh/', '建筑指南')],
        'playa-del-carmen': [('/playa-del-carmen-jianfang-chengben/', '建房成本是多少'), ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO'), ('/haohua-bieshu-playa-del-carmen/', '豪华别墅'), ('/fangwu-fanxin-playa-del-carmen/', '房屋翻新'), ('/jisuanqi/', '造价计算器'), ('/blog-zh/', '建筑指南')],
        'cancun': [('/cancun-jianzhu-gongsi/', '坎昆建筑公司'), ('/blog-zh/cancun-jianzhu-xukezheng.html', '坎昆施工许可'), ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '许可与DRO'), ('/jisuanqi/', '造价计算器'), ('/blog-zh/', '建筑指南')],
        'tulum': [('/tulum-jianzhu-gongsi/', '图卢姆建筑公司'), ('/blog-zh/tulum-jianzhu-xukezheng.html', '图卢姆施工许可'), ('/blog-zh/tulum-kechixu-jianzhu.html', '可持续建筑'), ('/jisuanqi/', '造价计算器'), ('/blog-zh/', '建筑指南')],
        'riviera-maya': [('/zhuzhai-jianzao-puerto-aventuras/', 'Puerto Aventuras 住宅建造'), ('/zhuzhai-jianzao-akumal/', 'Akumal 住宅建造'), ('/zhuzhai-jianzao-playa-del-carmen/', '普拉亚德尔卡门住宅建造'), ('/zhuzhai-jianzao-cancun/', '坎昆住宅建造'), ('/zhuzhai-jianzao-tulum/', '图卢姆住宅建造'), ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO'), ('/jisuanqi/', '造价计算器'), ('/blog-zh/', '建筑指南')]},
}


def chrome(lang):
    """Pull top bar, nav, footer and WhatsApp widget from a reference page."""
    s = open(os.path.join(REF[lang], 'index.html'), encoding='utf-8').read()
    g = lambda p: re.search(p, s, re.S).group(0)
    nav = g(r'<nav class="navbar.*?</nav>')
    nav = re.sub(r'<li class="nav-item dropdown.*?</ul>\s*</li>', '{DROPDOWN}', nav, flags=re.S)
    return dict(top=g(r'<div class="top-cta-bar">.*?</div>'), nav=nav,
                footer=g(r'<footer class="footer">.*?</footer>'),
                wa=g(r'<div class="wa-widget".*?</script>'))


def dropdown(lang, loc):
    items = ''
    for code, name in LANGNAME:
        cls, href = (' active', '#') if code == lang else ('', BASE + '/' + SLUG[code][loc] + '/')
        items += '<li><a class="dropdown-item%s" href="%s">%s</a></li>' % (cls, href, name)
    return ('<li class="nav-item dropdown ms-lg-2"><a class="nav-link dropdown-toggle" href="#" '
            'data-bs-toggle="dropdown">%s</a><ul class="dropdown-menu dropdown-menu-end">%s</ul></li>'
            % (lang.upper(), items))


def build(lang, loc, ch):
    t, n = L[lang], NUM[loc]
    city = CITY[lang][loc]
    lcity = re.sub(r'^(the|der|la|le) ', '', city)
    p150 = n['sizes'][1][1]
    F = dict(city=city, lcity=lcity.lower(), m2=n['m2'], usd=n['usd'], p150=p150,
             perm=n['perm'], zones=ZONES[lang][loc])
    f = lambda s: s.format(**F)
    url = BASE + '/' + SLUG[lang][loc] + '/'
    h1 = OVR.get('h1', {}).get(loc, {}).get(lang) or f(t['h1'])
    title = OVR.get('title', {}).get(loc, {}).get(lang) or f(t['title'])
    desc = OVR.get('desc', {}).get(loc, {}).get(lang) or f(t['desc'])
    extra_block = OVR.get('block', {}).get(loc, {}).get(lang, '')
    alert_txt = OVR.get('alert', {}).get(loc, {}).get(lang) or f(t['alert'])
    h_cost_txt = OVR.get('h_cost', {}).get(loc, {}).get(lang) or f(t['h_cost'])
    row_lbl = OVR.get('row', {}).get(loc, {}).get(lang) or t['row']
    h_proc_txt = OVR.get('h_proc', {}).get(loc, {}).get(lang) or t['h_proc']
    compact = loc not in FULL
    parent_url = OVR.get('parent_url', {}).get(loc, {}).get(lang, '/')

    # compact pages drop the four generic FAQ (they were on 49 of 54 pages per language)
    faq = ([] if loc not in FULL else [(f(q), f(a)) for q, a in t['faq']]) + FAQX[lang][loc]
    faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    lb = {"@context": "https://schema.org", "@type": "GeneralContractor", "name": "Recrea Construcción",
          "url": url, "image": BASE + "/img/og-wallpaper.png", "telephone": "+52-984-452-5333",
          "email": "constructionrecrea@gmail.com", "priceRange": "$$",
          "address": {"@type": "PostalAddress", "streetAddress": "Corasol", "addressLocality": "Playa del Carmen",
                      "addressRegion": "Quintana Roo", "postalCode": "77710", "addressCountry": "MX"},
          "geo": {"@type": "GeoCoordinates", "latitude": 20.6296, "longitude": -87.0739},
          "areaServed": [{"@type": "City", "name": lcity}],
          "makesOffer": {"@type": "Offer", "itemOffered": {"@type": "Service", "name": h1,
                         "serviceType": "Turnkey residential construction"}},
          "sameAs": ["https://www.facebook.com/recrea.arquitectura", "https://www.instagram.com/recrea_arquitectura"],
          "foundingDate": "2008", "knowsLanguage": ["es", "en"]}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
          {"@type": "ListItem", "position": 2, "name": h1}]}
    alts = '\n  '.join('<link rel="alternate" hreflang="%s" href="%s/%s/">' % (c, BASE, SLUG[c][loc])
                       for c, _ in LANGNAME)
    alts += '\n  <link rel="alternate" hreflang="x-default" href="%s/%s/">' % (BASE, SLUG['en'][loc])

    steps = '\n'.join(
      '<div class="col-md-6"><div class="p-3 bg-light rounded h-100"><h5 class="mb-1">'
      '<span style="color:var(--accent)">%d.</span> %s</h5><p class="small mb-1">%s</p>'
      '<p class="small text-muted mb-0"><i class="bi bi-clock me-1"></i>%s</p></div></div>'
      % (i + 1, s[0], s[1], s[2]) for i, s in enumerate(t['steps']))
    rows = '\n'.join('<tr><td>%s</td><td>%s MXN</td><td>%s USD</td></tr>'
                     % (row_lbl.format(n=sz[0]), sz[1], sz[2]) for sz in n['sizes'])
    faq_html = '\n'.join(
      '<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button%s" type="button" '
      'data-bs-toggle="collapse" data-bs-target="#faq%d">%s</button></h3>'
      '<div id="faq%d" class="accordion-collapse collapse%s" data-bs-parent="#faqAcc">'
      '<div class="accordion-body">%s</div></div></div>'
      % ('' if i == 0 else ' collapsed', i, q, i, ' show' if i == 0 else '', a)
      for i, (q, a) in enumerate(faq))
    links = ' · '.join('<a href="%s">%s</a>' % l for l in LINKS[lang][loc])
    badges = ''.join('<span class="trust-badge"><i class="bi bi-patch-check"></i>%s</span>' % b for b in t['badges'])
    if compact:
        cp, ci, cw = COMPACT_TXT[lang]
        process_block = ('<h2 class="mt-4">%s</h2>\n<p>%s</p>\n<p>%s</p>\n'
                         % (h_proc_txt, cp % parent_url, ci % parent_url))
        why_block = '<h2 class="mt-4">%s</h2>\n<p>%s</p>\n' % (t['h_why'], cw)
    else:
        process_block = ('<h2 class="mt-4">%s</h2>\n<p>%s</p>\n<div class="row g-3 my-2">\n%s\n</div>\n'
                         '<p class="mt-2">%s</p>\n\n'
                         '<h2 class="mt-4">%s</h2>\n<div class="row g-3 my-2">\n'
                         '<div class="col-md-6"><div class="p-3 bg-light rounded h-100"><h5>'
                         '<i class="bi bi-check-circle me-2" style="color:#198754"></i>%s</h5><ul class="mb-0 small">\n%s\n'
                         '</ul></div></div>\n'
                         '<div class="col-md-6"><div class="p-3 bg-light rounded h-100"><h5>'
                         '<i class="bi bi-x-circle me-2" style="color:#dc3545"></i>%s</h5><ul class="mb-0 small">\n%s\n'
                         '</ul></div></div>\n</div>\n'
                         % (h_proc_txt, f(t['proc_p']), steps, f(t['proc_total']), t['h_inc'],
                            t['inc_t'], chr(10).join('<li>%s</li>' % x for x in t['inc']),
                            t['ninc_t'], chr(10).join('<li>%s</li>' % x for x in t['ninc'])))
        why_block = ('<h2 class="mt-4">%s</h2>\n<ul>\n%s\n</ul>\n'
                     % (t['h_why'], chr(10).join('<li>%s</li>' % x for x in t['why'])))
    nav = ch['nav'].replace('{DROPDOWN}', dropdown(lang, loc))

    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
  <meta name="google-site-verification" content="0WwXyAoY4jeA2xgFFFB06a9HqEfzR7LnyLYVBrFTU0A" />
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{f(t['kw'])}">
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
  <meta property="og:locale" content="{t['locale']}">
  <meta property="og:site_name" content="Recrea Construction">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{BASE}/img/og-wallpaper.png">
</head>
<body class="has-top-bar">
{ch['top']}
{nav}
<div style="padding-top:116px"></div>
<nav class="container mt-3"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="/">Recrea</a></li><li class="breadcrumb-item active">{h1}</li></ol></nav>
<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-9">
<h1>{h1}</h1>
<p class="lead">{f(t['lead'])}</p>
<p>{f(t['intro'])}</p>
<div class="alert" style="background:var(--accent);color:#000;border:none">{alert_txt}</div>

<h2 class="mt-4">{h_cost_txt}</h2>
<p>{t['cost_p']}</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>{t['th'][0]}</th><th>{t['th'][1]}</th><th>{t['th'][2]}</th></tr></thead><tbody>
{rows}
</tbody></table></div>
<p>{t['cost_after']}</p>
{extra_block}

{process_block}

<h2 class="mt-4">{f(t['h_norm'])}</h2>
<p>{NORM[lang][loc]}</p>
<h3 class="mt-3">{t['h_soil']}</h3>
<p>{SOIL[lang][loc]}</p>
<p>{EXTRA[lang][loc]}</p>
<p>{t['guides']}{links}</p>

{why_block}

<h2 class="mt-5">{t['h_proj']}</h2>
<div class="row g-3 my-2">
<div class="col-md-6"><img loading="lazy" src="../img/villa-pool-tropical.jpg" class="img-fluid rounded" alt="{h1} — Recrea" style="width:100%;height:260px;object-fit:cover"></div>
<div class="col-md-6"><img loading="lazy" src="../img/residential-block-construction.jpg" class="img-fluid rounded" alt="{h1} — Recrea" style="width:100%;height:260px;object-fit:cover"></div>
</div>

<div class="row g-3 my-4">
<div class="col-md-6"><a href="{WA}" target="_blank" rel="noopener" class="btn btn-success btn-lg w-100"><i class="bi bi-whatsapp me-2"></i>{t['wa']}</a></div>
<div class="col-md-6"><a href="tel:+529844525333" class="btn btn-outline-dark btn-lg w-100"><i class="bi bi-telephone me-2"></i>{t['call']}</a></div>
</div>

<h3 class="mt-4">{t['form_h']}</h3>
<form class="contact-form my-3" action="https://formsubmit.co/constructionrecrea@gmail.com" method="POST">
  <input type="hidden" name="_subject" value="[{SLUG[lang][loc]}] New request">
  <input type="hidden" name="_captcha" value="false">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_next" value="{url}">
  <input type="text" name="_honey" style="display:none">
  <div class="row g-3">
    <div class="col-md-6"><input type="text" class="form-control" name="name" placeholder="{t['f_name']}" required></div>
    <div class="col-md-6"><input type="tel" class="form-control" name="phone" placeholder="{t['f_phone']}" required></div>
    <div class="col-12"><textarea class="form-control" name="message" rows="3" placeholder="{t['f_msg']}"></textarea></div>
    <div class="col-12 text-center"><button type="submit" class="btn btn-cta btn-lg"><i class="bi bi-send me-2"></i>{t['f_send']}</button></div>
  </div>
</form>

<h2 class="mt-5">{t['h_faq']}</h2>
<div class="accordion my-4" id="faqAcc">
{faq_html}
</div>

<div class="cta-section rounded p-5 text-center my-5">
  <h3 class="text-white mb-3">{f(t['h_cta'])}</h3>
  <p class="text-white-50 mb-4">{t['cta_p']}</p>
  <a href="{WA}" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>{t['cta_btn']}</a>
</div>
<div class="trust-badges">{badges}</div>
</div></div></div></section>
{ch['footer']}
<a href="mailto:constructionrecrea@gmail.com" class="email-float" aria-label="Email"><i class="bi bi-envelope-fill"></i></a>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
<script>window.addEventListener('scroll',function(){{document.getElementById('mainNav').classList.toggle('scrolled',window.scrollY>50)}});</script>
{ch['wa']}
</body></html>"""


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for lang in ['en', 'ru', 'de', 'fr', 'zh']:
        ch = chrome(lang)
        for loc in LOCS:
            d = SLUG[lang][loc]
            os.makedirs(d, exist_ok=True)
            html = build(lang, loc, ch)
            open(os.path.join(d, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-42s %6d bytes' % (d + '/', len(html)))
