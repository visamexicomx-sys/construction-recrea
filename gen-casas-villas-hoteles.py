#!/usr/bin/env python3
"""Villa + boutique-hotel pages for the three mainland cities (2026-08-09).

Same structure as the island pages (own slug, own H1, villa cost table + a second
table in USD per key, hotel requirements block), for Playa del Carmen, Tulum and
Cancún.

Deliberate choice: the villa m² band is IDENTICAL to the city's house-construction
page (villas sit in the upper half of that band) so the site never contradicts its
own published numbers. What differentiates these pages is the hospitality half:
per-key costs, hotel licensing and the villa/hotel market angle per city.

They also stay clear of /construccion-comercial-hoteles-riviera-maya/ (regional,
commercial + hotels broadly) — these are city-level villa + boutique hotel pages
and cross-link to it.
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
il = load('gen-casas-islas.py', 'il')
z1 = il.z1
ml = il.ml

CITIES = {
 'vh-playa-del-carmen': dict(parent='playa-del-carmen', f=1.0, perm='2–4'),
 'vh-tulum':            dict(parent='tulum',            f=1.0, perm='3–5'),
 'vh-cancun':           dict(parent='cancun',           f=1.0, perm='2–4'),
}
BASE_SLUG = {'vh-playa-del-carmen': 'playa-del-carmen', 'vh-tulum': 'tulum', 'vh-cancun': 'cancun'}
SLUG_PREFIX = {'es': 'construccion-villas-hoteles', 'en': 'villa-hotel-construction',
               'ru': 'stroitelstvo-vill-i-otelei', 'de': 'villen-hotelbau',
               'fr': 'construction-villas-hotels', 'zh': 'bieshu-jiudian-jianzao'}

NAMES = {
 'vh-playa-del-carmen': {'es': 'Playa del Carmen', 'en': 'Playa del Carmen', 'ru': 'Плая-дель-Кармен',
                         'de': 'Playa del Carmen', 'fr': 'Playa del Carmen', 'zh': '普拉亚德尔卡门'},
 'vh-tulum': {'es': 'Tulum', 'en': 'Tulum', 'ru': 'Тулуме', 'de': 'Tulum', 'fr': 'Tulum', 'zh': '图卢姆'},
 'vh-cancun': {'es': 'Cancún', 'en': 'Cancún', 'ru': 'Канкуне', 'de': 'Cancún', 'fr': 'Cancún', 'zh': '坎昆'},
}
AREAS = {
 'vh-playa-del-carmen': {'es': 'Playacar, Corasol, Mayakoba, Zazil-Ha y el centro', 'en': 'Playacar, Corasol, Mayakoba, Zazil-Ha and downtown',
   'ru': 'Плаякаре, Корасоле, Майякобе, Сасиль-Ха и центре', 'de': 'Playacar, Corasol, Mayakoba, Zazil-Ha und dem Zentrum',
   'fr': 'Playacar, Corasol, Mayakoba, Zazil-Ha et le centre', 'zh': 'Playacar、Corasol、Mayakoba、Zazil-Ha 与市中心'},
 'vh-tulum': {'es': 'Aldea Zamá, La Veleta, la zona hotelera y Región 15', 'en': 'Aldea Zamá, La Veleta, the hotel zone and Región 15',
   'ru': 'Альдеа-Зама, Ла-Велете, отельной зоне и Регионе 15', 'de': 'Aldea Zamá, La Veleta, der Hotelzone und Región 15',
   'fr': 'Aldea Zamá, La Veleta, la zone hôtelière et Región 15', 'zh': 'Aldea Zamá、La Veleta、酒店区与15区'},
 'vh-cancun': {'es': 'Puerto Cancún, la Zona Hotelera, Supermanzanas y Costa Mujeres', 'en': 'Puerto Cancún, the Hotel Zone, the Supermanzanas and Costa Mujeres',
   'ru': 'Пуэрто-Канкуне, Отельной зоне, Супермансанас и Коста-Мухерес', 'de': 'Puerto Cancún, der Hotelzone, den Supermanzanas und Costa Mujeres',
   'fr': 'Puerto Cancún, la Zone Hôtelière, les Supermanzanas et Costa Mujeres', 'zh': 'Puerto Cancún、酒店区、Supermanzanas 与 Costa Mujeres'},
}

# premium / standard / economy, USD per key
KEYS = {
 'vh-playa-del-carmen': ('$105,000 – $175,000', '$85,000 – $140,000', '$65,000 – $105,000'),
 'vh-tulum':            ('$120,000 – $200,000', '$95,000 – $155,000', '$70,000 – $115,000'),
 'vh-cancun':           ('$100,000 – $170,000', '$80,000 – $135,000', '$62,000 – $100,000'),
}

TEXT = {
'vh-playa-del-carmen': {
 'es': 'Playa del Carmen es el mercado más equilibrado de la región para las dos cosas: villas en Playacar, Corasol o Mayakoba y hotelería boutique de 10 a 25 llaves cerca de la Quinta Avenida y el centro. Los proveedores y la mano de obra están aquí, no a dos horas, y eso se nota en el plazo y en el costo por llave. La villa se diseña para renta alta o vivienda permanente; el hotel, para operar con equipo pequeño y ocupación estable todo el año.',
 'en': 'Playa del Carmen is the most balanced market in the region for both: villas in Playacar, Corasol or Mayakoba and 10 to 25 key boutique hospitality near Quinta Avenida and downtown. Suppliers and trades are here, not two hours away, and that shows in both the schedule and the cost per key. The villa is designed for high-yield rental or permanent living; the hotel, to run with a small team and steady year-round occupancy.',
 'ru': 'Плая-дель-Кармен — самый сбалансированный рынок региона сразу для двух задач: виллы в Плаякаре, Корасоле или Майякобе и бутик-отели на 10–25 номеров рядом с Пятой авеню и центром. Поставщики и бригады здесь, а не в двух часах езды, и это видно и в сроке, и в цене за номер. Вилла проектируется под высокую аренду или постоянное проживание, отель — под работу небольшой командой и ровную загрузку весь год.',
 'de': 'Playa del Carmen ist der ausgewogenste Markt der Region für beides: Villen in Playacar, Corasol oder Mayakoba und Boutiquehotellerie mit 10 bis 25 Zimmern nahe der Quinta Avenida und dem Zentrum. Lieferanten und Gewerke sind hier, nicht zwei Stunden entfernt — das zeigt sich in Terminplan und Kosten pro Zimmer. Die Villa wird für hohe Mietrendite oder dauerhaftes Wohnen geplant, das Hotel für den Betrieb mit kleinem Team und stabiler Ganzjahresauslastung.',
 'fr': 'Playa del Carmen est le marché le plus équilibré de la région pour les deux : des villas à Playacar, Corasol ou Mayakoba et une hôtellerie boutique de 10 à 25 clés près de la Quinta Avenida et du centre. Les fournisseurs et les corps de métier sont ici, pas à deux heures de route, et cela se voit sur les délais comme sur le coût par clé. La villa se conçoit pour la location à fort rendement ou la résidence permanente ; l’hôtel, pour tourner avec une petite équipe et un taux d’occupation stable toute l’année.',
 'zh': '普拉亚德尔卡门是本区域同时适合这两类项目的最均衡市场：Playacar、Corasol 或 Mayakoba 的别墅，以及第五大道与市中心附近10至25间客房的精品酒店。供应商与工班就在本地，而非两小时车程之外，这直接体现在工期与每间客房造价上。别墅按高收益出租或长期自住设计，酒店则按小团队运营、全年稳定入住率设计。'},
'vh-tulum': {
 'es': 'Tulum es el mercado de mayor rendimiento en renta y también el más exigente: villas eco-chic en Aldea Zamá o La Veleta y hoteles boutique pequeños, de 8 a 20 llaves, donde el concepto pesa tanto como la obra. Aquí manda el calendario ambiental: con SEMA de por medio, el proyecto se diseña ya conforme a la norma y el trámite arranca en paralelo. El estándar de acabados —chukum, madera dura, diseño bioclimático— es parte del producto, no un extra.',
 'en': 'Tulum is the highest-yield rental market and also the most demanding: eco-chic villas in Aldea Zamá or La Veleta and small boutique hotels of 8 to 20 keys, where the concept weighs as much as the construction. The environmental calendar rules here: with SEMA involved, the design is drawn compliant from the start and the process runs in parallel. The finish standard — chukum, hardwood, bioclimatic design — is part of the product, not an extra.',
 'ru': 'Тулум — рынок с самой высокой доходностью аренды и самый требовательный: эко-шик виллы в Альдеа-Зама или Ла-Велете и небольшие бутик-отели на 8–20 номеров, где концепция весит не меньше стройки. Здесь командует экологический календарь: с участием SEMA проект сразу рисуется под норму, а процедура идёт параллельно. Стандарт отделки — чукум, твёрдая древесина, биоклиматика — это часть продукта, а не опция.',
 'de': 'Tulum ist der renditestärkste Mietmarkt und zugleich der anspruchsvollste: Eco-Chic-Villen in Aldea Zamá oder La Veleta und kleine Boutiquehotels mit 8 bis 20 Zimmern, bei denen das Konzept so viel wiegt wie der Bau. Hier bestimmt der Umweltkalender: Mit der SEMA im Spiel wird von Anfang an normkonform geplant und das Verfahren läuft parallel. Der Ausbaustandard — Chukum, Hartholz, bioklimatisches Design — ist Teil des Produkts, kein Extra.',
 'fr': 'Tulum est le marché locatif au meilleur rendement et le plus exigeant : villas éco-chic à Aldea Zamá ou La Veleta et petits hôtels boutique de 8 à 20 clés, où le concept pèse autant que le chantier. Ici, c’est le calendrier environnemental qui commande : avec la SEMA dans la boucle, le projet est conçu conforme dès le départ et la procédure avance en parallèle. Le standard de finition — chukum, bois dur, conception bioclimatique — fait partie du produit, pas des options.',
 'zh': '图卢姆是租金回报最高、同时也最考验执行力的市场：Aldea Zamá 或 La Veleta 的生态时尚风别墅，以及8至20间客房的小型精品酒店——在这里，概念的分量不亚于施工。主导节奏的是环保时间表：涉及 SEMA 时，方案从一开始就按合规绘制，报批与设计并行。chukum 灰泥、硬木与生态气候设计等装修标准是产品的一部分，而非额外选项。'},
'vh-cancun': {
 'es': 'Cancún juega en dos tableros: villas y residencias en Puerto Cancún, la Zona Hotelera y Costa Mujeres, y hotelería de ciudad —negocios, aeropuerto, estancias cortas— que opera todo el año sin depender de la temporada de playa. Es el mejor costo por llave de la región por cercanía de proveedores, y el punto donde más pesa revisar la jurisdicción y el uso de suelo antes de comprar: FONATUR y ZOFEMAT cambian por completo el expediente.',
 'en': 'Cancún plays on two boards: villas and residences in Puerto Cancún, the Hotel Zone and Costa Mujeres, and city hospitality — business, airport, short stays — that runs all year without depending on the beach season. It is the region’s best cost per key thanks to supplier proximity, and the place where checking jurisdiction and land use before buying matters most: FONATUR and ZOFEMAT change the whole file.',
 'ru': 'Канкун играет на двух полях: виллы и резиденции в Пуэрто-Канкуне, Отельной зоне и Коста-Мухерес — и городская гостиница под бизнес, аэропорт и короткие заезды, которая работает круглый год и не зависит от пляжного сезона. Здесь лучшая в регионе цена за номер благодаря близости поставщиков и одновременно место, где важнее всего до покупки проверить юрисдикцию и назначение земли: FONATUR и ZOFEMAT полностью меняют пакет документов.',
 'de': 'Cancún spielt auf zwei Feldern: Villen und Residenzen in Puerto Cancún, der Hotelzone und Costa Mujeres — und Stadthotellerie für Geschäftsreise, Flughafen und Kurzaufenthalte, die ganzjährig läuft und nicht von der Strandsaison abhängt. Dank Lieferantennähe der beste Preis pro Zimmer der Region, und zugleich der Ort, an dem die Prüfung von Zuständigkeit und Nutzungsart vor dem Kauf am wichtigsten ist: FONATUR und ZOFEMAT ändern die gesamte Akte.',
 'fr': 'Cancún joue sur deux tableaux : villas et résidences à Puerto Cancún, en Zone Hôtelière et à Costa Mujeres, et une hôtellerie urbaine — affaires, aéroport, courts séjours — qui tourne toute l’année sans dépendre de la saison balnéaire. C’est le meilleur coût par clé de la région grâce à la proximité des fournisseurs, et l’endroit où vérifier la juridiction et l’usage du sol avant d’acheter compte le plus : FONATUR et ZOFEMAT changent tout le dossier.',
 'zh': '坎昆有两条主线：Puerto Cancún、酒店区与 Costa Mujeres 的别墅与住宅，以及面向商务、机场与短住的城市酒店——全年运营，不依赖海滩旺季。得益于供应商就近，这里是全区每间客房造价最优的市场；同时也是购地前最需要核实管辖与土地用途的地方：FONATUR 与 ZOFEMAT 会彻底改变申报材料构成。'},
}

NORM = {
'vh-playa-del-carmen': {
 'es': 'Para una villa el camino es el habitual en Solidaridad: constancia de uso de suelo conforme al PDU, licencia de construcción con proyecto firmado por DRO y trámite ambiental si el predio colinda con manglar, duna o cenote. Para un hotel se suma otra capa: uso de suelo con giro hotelero, licencia de funcionamiento municipal, visto bueno de Protección Civil, proyecto eléctrico ante CFE acorde al aforo y registro turístico. Iniciamos ambos expedientes en paralelo al proyecto ejecutivo.',
 'en': 'For a villa the route is the usual one in Solidaridad: land-use certificate under the PDU, building licence with DRO-signed drawings and an environmental process if the lot borders mangrove, dune or a cenote. A hotel adds another layer: hotel-use land use, municipal operating licence, Civil Protection sign-off, a CFE electrical project sized to occupancy and tourism registration. We start both files in parallel with the construction documents.',
 'ru': 'Для виллы путь обычный для Solidaridad: справка о назначении земли по PDU, разрешение на строительство с проектом за подписью DRO и экологическая процедура, если участок граничит с мангром, дюной или сенотом. Для отеля добавляется ещё слой: назначение земли под гостиничный профиль, муниципальная лицензия на деятельность, заключение Гражданской защиты, электропроект в CFE под вместимость и туристическая регистрация. Оба пакета запускаем параллельно рабочему проекту.',
 'de': 'Für eine Villa ist der Weg der übliche in Solidaridad: Nutzungsbescheinigung nach PDU, Baugenehmigung mit DRO-unterzeichneten Plänen und Umweltverfahren, wenn das Grundstück an Mangroven, Düne oder Cenote grenzt. Ein Hotel bringt eine weitere Ebene: Nutzungsart Hotel, kommunale Betriebslizenz, Freigabe des Zivilschutzes, ein auf die Belegung ausgelegtes CFE-Elektroprojekt und Tourismusregistrierung. Wir starten beide Akten parallel zur Ausführungsplanung.',
 'fr': 'Pour une villa, le parcours est celui de Solidaridad : certificat d’usage du sol au titre du PDU, permis de construire avec plans signés par un DRO et procédure environnementale si le terrain jouxte mangrove, dune ou cénote. Un hôtel ajoute une couche : usage du sol à vocation hôtelière, licence d’exploitation municipale, avis de la Protection Civile, projet électrique CFE dimensionné à la capacité et enregistrement touristique. Nous lançons les deux dossiers en parallèle du projet d’exécution.',
 'zh': '别墅走 Solidaridad 的常规流程：依 PDU 取得土地用途证明、提交由 DRO 签署的图纸办理施工许可；若地块毗邻红树林、沙丘或天然井，还需环保流程。酒店则多一层：需取得酒店类土地用途、市政经营许可、民防（Protección Civil）意见、按接待容量向 CFE 报批的电气方案，以及旅游登记。两套材料我们与施工图并行推进。'},
'vh-tulum': {
 'es': 'En Tulum el eje es ambiental: la mayoría de los proyectos requiere autorización de la SEMA (con MIA cuando hay desmonte o cercanía a cenotes o manglar), además de uso de suelo y licencia municipal con DRO. Para hotel se añaden giro hotelero en el uso de suelo, licencia de funcionamiento, Protección Civil, capacidad eléctrica ante CFE y registro turístico; si hay club de playa o restaurante abierto al público, más requisitos sanitarios y de aforo. Presupueste de 3 a 5 meses de permisos y arranque el trámite con el anteproyecto.',
 'en': 'In Tulum the environmental axis leads: most projects need SEMA authorisation (with an MIA where there is clearing or proximity to cenotes or mangrove), on top of land use and the municipal licence with a DRO. A hotel adds hotel-use zoning, the operating licence, Civil Protection, CFE capacity and tourism registration; if there is a beach club or a restaurant open to the public, health and occupancy requirements too. Budget 3 to 5 months of permits and start the process with the concept design.',
 'ru': 'В Тулуме ось — экология: большинству проектов нужна авторизация SEMA (с MIA при расчистке или близости сенота либо мангров), плюс назначение земли и муниципальная лицензия с DRO. Для отеля добавляются гостиничный профиль в назначении земли, лицензия на деятельность, Гражданская защита, мощность в CFE и туристическая регистрация; при пляжном клубе или ресторане для публики — санитарные требования и нормы вместимости. Закладывайте 3–5 месяцев на разрешения и запускайте процедуру уже с эскизом.',
 'de': 'In Tulum führt die Umweltachse: Die meisten Projekte brauchen eine SEMA-Genehmigung (mit MIA bei Rodung oder Nähe zu Cenoten und Mangroven), dazu Nutzungsart und kommunale Lizenz mit DRO. Ein Hotel ergänzt Hotel-Nutzungsart, Betriebslizenz, Zivilschutz, CFE-Leistung und Tourismusregistrierung; bei Beachclub oder öffentlichem Restaurant zusätzlich Hygiene- und Belegungsauflagen. Kalkulieren Sie 3 bis 5 Monate Genehmigungen und starten Sie das Verfahren bereits mit dem Entwurf.',
 'fr': 'À Tulum, l’axe environnemental commande : la plupart des projets exigent l’autorisation de la SEMA (avec MIA en cas de défrichement ou de proximité de cénotes ou de mangrove), en plus de l’usage du sol et du permis municipal avec DRO. Un hôtel ajoute l’usage hôtelier, la licence d’exploitation, la Protection Civile, la puissance CFE et l’enregistrement touristique ; avec un beach club ou un restaurant ouvert au public, s’ajoutent les exigences sanitaires et de capacité. Comptez 3 à 5 mois de permis et lancez la procédure dès l’avant-projet.',
 'zh': '在图卢姆，环保是主线：多数项目需 SEMA 许可（涉及清林或临近天然井、红树林时须做 MIA），此外还需土地用途与带 DRO 的市政许可。酒店另需将土地用途调整为酒店类，并办理经营许可、民防意见、CFE 用电容量与旅游登记；若设有海滩俱乐部或对外营业餐厅，还须满足卫生与容纳人数要求。许可周期请预留3至5个月，并在方案阶段即启动报批。'},
'vh-cancun': {
 'es': 'En Benito Juárez la licencia de construcción se tramita ante Desarrollo Urbano con proyecto avalado por DRO. En Puerto Cancún y la Zona Hotelera se añade el visto bueno de FONATUR y, frente al mar, la concesión ZOFEMAT; en fraccionamientos con reglamento, comité de diseño. Para hotel entran uso de suelo con giro hotelero, licencia de funcionamiento, Protección Civil, proyecto eléctrico ante CFE por aforo y registro turístico. Lo primero, siempre: confirmar municipio y uso de suelo del predio antes de comprar.',
 'en': 'In Benito Juárez the building licence goes through Urban Development with a DRO-endorsed project. Puerto Cancún and the Hotel Zone add FONATUR sign-off and, on the beachfront, a ZOFEMAT concession; gated developments add a design committee. A hotel brings hotel-use zoning, the operating licence, Civil Protection, a CFE electrical project sized to occupancy and tourism registration. First step, always: confirm the municipality and the land use of the lot before buying.',
 'ru': 'В Benito Juárez разрешение выдаёт управление городского развития по проекту с подписью DRO. В Пуэрто-Канкуне и Отельной зоне добавляется согласование FONATUR, на первой линии — концессия ZOFEMAT; в закрытых посёлках — комитет по дизайну. Для отеля появляются гостиничный профиль назначения земли, лицензия на деятельность, Гражданская защита, электропроект в CFE под вместимость и туристическая регистрация. Первым делом всегда: подтвердить муниципалитет и назначение земли участка до покупки.',
 'de': 'In Benito Juárez läuft die Baugenehmigung über die Stadtentwicklung mit DRO-geprüftem Projekt. Puerto Cancún und die Hotelzone ergänzen die FONATUR-Freigabe und am Strand die ZOFEMAT-Konzession; in Anlagen mit Satzung kommt ein Gestaltungsbeirat dazu. Für ein Hotel kommen Hotel-Nutzungsart, Betriebslizenz, Zivilschutz, ein auf die Belegung ausgelegtes CFE-Elektroprojekt und Tourismusregistrierung hinzu. Zuerst immer: Gemeinde und Nutzungsart des Grundstücks vor dem Kauf klären.',
 'fr': 'À Benito Juárez, le permis passe par le développement urbain avec un projet validé par un DRO. Puerto Cancún et la Zone Hôtelière ajoutent l’accord FONATUR et, en front de mer, la concession ZOFEMAT ; les résidences réglementées ajoutent un comité d’architecture. Un hôtel implique l’usage hôtelier, la licence d’exploitation, la Protection Civile, un projet électrique CFE dimensionné à la capacité et l’enregistrement touristique. Première étape, toujours : confirmer la commune et l’usage du sol du terrain avant l’achat.',
 'zh': '在 Benito Juárez，施工许可由城市发展局审批，项目须经 DRO 背书。Puerto Cancún 与酒店区还需 FONATUR 批准，海滨地块需 ZOFEMAT 特许；设有规约的封闭社区另需设计委员会审核。酒店则需酒店类土地用途、经营许可、民防意见、按容量向 CFE 报批的电气方案与旅游登记。第一步始终是：购地前确认地块所属市政与土地用途。'},
}

FAQ = {
'vh-playa-del-carmen': {
 'es': [('¿Cuánto cuesta construir un hotel boutique en Playa del Carmen?', 'De $65,000 a $175,000 USD por llave según el nivel: económico, boutique estándar o premium con restaurante y spa. Un hotel de 15 llaves estándar ronda $1.3–$2.1 millones USD de obra, sin terreno.'),
        ('¿Construyen villa y hotel con el mismo equipo?', 'Sí, y con el mismo contrato a precio fijo. La diferencia está en el expediente: el hotel suma giro hotelero, licencia de funcionamiento, Protección Civil y capacidad eléctrica por aforo, que gestionamos nosotros.')],
 'en': [('How much does a boutique hotel cost to build in Playa del Carmen?', 'From $65,000 to $175,000 USD per key depending on level: economy, standard boutique or premium with restaurant and spa. A 15-key standard hotel runs $1.3–$2.1 million USD of construction, land excluded.'),
        ('Do you build villas and hotels with the same team?', 'Yes, and under the same fixed-price contract. The difference is the paperwork: a hotel adds hotel-use zoning, operating licence, Civil Protection and occupancy-based electrical capacity, which we handle.')],
 'ru': [('Сколько стоит построить бутик-отель в Плая-дель-Кармен?', 'От $65,000 до $175,000 USD за номер в зависимости от уровня: эконом, стандартный бутик или премиум с рестораном и спа. Отель на 15 номеров в стандарте — примерно $1.3–$2.1 млн USD стройки, без участка.'),
        ('Виллу и отель строит одна команда?', 'Да, и по одному договору с фиксированной ценой. Разница в документах: у отеля добавляются гостиничный профиль, лицензия на деятельность, Гражданская защита и мощность под вместимость — это ведём мы.')],
 'de': [('Was kostet ein Boutiquehotel in Playa del Carmen?', 'Von $65.000 bis $175.000 USD pro Zimmer je nach Niveau: Economy, Standard-Boutique oder Premium mit Restaurant und Spa. Ein Standardhotel mit 15 Zimmern liegt bei $1,3–$2,1 Mio. USD Bauleistung, ohne Grundstück.'),
        ('Bauen Sie Villa und Hotel mit demselben Team?', 'Ja, und unter demselben Festpreisvertrag. Der Unterschied liegt in den Unterlagen: Beim Hotel kommen Hotel-Nutzungsart, Betriebslizenz, Zivilschutz und belegungsabhängige Leistung hinzu — das übernehmen wir.')],
 'fr': [('Combien coûte un hôtel boutique à Playa del Carmen ?', 'De 65 000 à 175 000 USD par clé selon le niveau : économique, boutique standard ou premium avec restaurant et spa. Un hôtel standard de 15 clés représente 1,3 à 2,1 M USD de travaux, hors terrain.'),
        ('Villa et hôtel, est-ce la même équipe ?', 'Oui, et le même contrat à prix fixe. La différence est administrative : l’hôtel ajoute l’usage hôtelier, la licence d’exploitation, la Protection Civile et la puissance selon capacité — nous nous en chargeons.')],
 'zh': [('在普拉亚德尔卡门建一家精品酒店要多少钱？', '按档次每间客房 65,000 至 175,000 美元：经济型、标准精品或含餐厅与水疗的高端型。15间客房的标准酒店，工程造价约130万至210万美元，不含土地。'),
        ('别墅与酒店是同一个团队施工吗？', '是，且适用同一份固定总价合同。差别在报批：酒店需增加酒店类土地用途、经营许可、民防意见与按容量核定的用电容量，这些由我们负责办理。')]},
'vh-tulum': {
 'es': [('¿Cuánto cuesta un hotel boutique en Tulum?', 'De $70,000 a $200,000 USD por llave. Tulum es el más caro de la costa por normativa ambiental, logística y estándar de acabados, y también el de mayor tarifa por noche.'),
        ('¿Qué tanto retrasa la SEMA un proyecto hotelero?', 'De 3 a 5 meses si el expediente entra bien armado. Por eso diseñamos conforme a la norma desde el anteproyecto y arrancamos el trámite en paralelo, no cuando el proyecto ya está cerrado.')],
 'en': [('How much does a boutique hotel cost in Tulum?', 'From $70,000 to $200,000 USD per key. Tulum is the most expensive on the coast because of environmental rules, logistics and the finish standard — and it also commands the highest nightly rate.'),
        ('How much does SEMA delay a hotel project?', '3 to 5 months if the file goes in properly prepared. That is why we design to the rules from the concept stage and start the process in parallel, not once the design is closed.')],
 'ru': [('Сколько стоит бутик-отель в Тулуме?', 'От $70,000 до $200,000 USD за номер. Тулум — самый дорогой на побережье из-за экологических норм, логистики и стандарта отделки, и одновременно с самым высоким тарифом за ночь.'),
        ('Насколько SEMA задерживает отельный проект?', 'На 3–5 месяцев, если пакет подан грамотно. Поэтому мы проектируем под норму уже на эскизе и запускаем процедуру параллельно, а не когда проект закрыт.')],
 'de': [('Was kostet ein Boutiquehotel in Tulum?', 'Von $70.000 bis $200.000 USD pro Zimmer. Tulum ist wegen Umweltauflagen, Logistik und Ausbaustandard das teuerste an der Küste — und erzielt zugleich die höchsten Zimmerraten.'),
        ('Wie stark verzögert die SEMA ein Hotelprojekt?', 'Um 3 bis 5 Monate, wenn die Akte sauber eingereicht wird. Deshalb planen wir ab dem Entwurf normkonform und starten das Verfahren parallel, nicht erst nach Planungsabschluss.')],
 'fr': [('Combien coûte un hôtel boutique à Tulum ?', 'De 70 000 à 200 000 USD par clé. Tulum est le plus cher de la côte du fait de la réglementation environnementale, de la logistique et du standard de finition — et affiche aussi les meilleurs tarifs par nuit.'),
        ('Dans quelle mesure la SEMA retarde-t-elle un projet hôtelier ?', 'De 3 à 5 mois si le dossier est bien préparé. C’est pourquoi nous concevons conforme dès l’avant-projet et lançons la procédure en parallèle, et non une fois le projet figé.')],
 'zh': [('在图卢姆建精品酒店要多少钱？', '每间客房 70,000 至 200,000 美元。受环保法规、物流与装修标准影响，图卢姆是海岸线上造价最高的市场，同时房价也最高。'),
        ('SEMA 会让酒店项目延后多久？', '材料准备充分的情况下为3至5个月。因此我们从方案阶段就按法规设计，并让报批与设计并行，而不是等方案定稿后再办。')]},
'vh-cancun': {
 'es': [('¿Cuánto cuesta construir un hotel en Cancún?', 'De $62,000 a $170,000 USD por llave según nivel. Es el mejor costo por llave de la región porque los proveedores están a minutos de la obra.'),
        ('¿Conviene hotel de ciudad o de playa en Cancún?', 'El de ciudad —Supermanzanas, corredor del aeropuerto— opera todo el año con menos estacionalidad y menos inversión por llave. El de playa cobra más por noche pero suma FONATUR, ZOFEMAT y especificación marina completa.')],
 'en': [('How much does a hotel cost to build in Cancún?', 'From $62,000 to $170,000 USD per key depending on level. It is the region’s best cost per key because suppliers are minutes from site.'),
        ('City hotel or beach hotel in Cancún?', 'The city one — Supermanzanas, airport corridor — runs all year with less seasonality and lower investment per key. The beach one charges more per night but adds FONATUR, ZOFEMAT and a full marine spec.')],
 'ru': [('Сколько стоит построить отель в Канкуне?', 'От $62,000 до $170,000 USD за номер в зависимости от уровня. Это лучшая цена за номер в регионе, потому что поставщики в минутах от площадки.'),
        ('Что выгоднее в Канкуне — городской отель или пляжный?', 'Городской (Супермансанас, коридор аэропорта) работает круглый год с меньшей сезонностью и меньшими вложениями на номер. Пляжный берёт больше за ночь, но добавляет FONATUR, ZOFEMAT и полную морскую спецификацию.')],
 'de': [('Was kostet ein Hotel in Cancún?', 'Von $62.000 bis $170.000 USD pro Zimmer je nach Niveau. Der beste Preis pro Zimmer der Region, weil Lieferanten Minuten von der Baustelle entfernt sind.'),
        ('Stadthotel oder Strandhotel in Cancún?', 'Das Stadthotel — Supermanzanas, Flughafenkorridor — läuft ganzjährig mit weniger Saisonalität und geringerer Investition pro Zimmer. Das Strandhotel erzielt höhere Raten, bringt aber FONATUR, ZOFEMAT und volle Meeresspezifikation mit.')],
 'fr': [('Combien coûte la construction d’un hôtel à Cancún ?', 'De 62 000 à 170 000 USD par clé selon le niveau. C’est le meilleur coût par clé de la région, les fournisseurs étant à quelques minutes du chantier.'),
        ('Hôtel de ville ou de plage à Cancún ?', 'Celui de ville — Supermanzanas, corridor de l’aéroport — tourne toute l’année avec moins de saisonnalité et un investissement par clé plus faible. Celui de plage se vend plus cher la nuit mais ajoute FONATUR, ZOFEMAT et une spécification marine complète.')],
 'zh': [('在坎昆建一家酒店要多少钱？', '按档次每间客房 62,000 至 170,000 美元。由于供应商距工地仅数分钟，这里是全区每间客房造价最优的市场。'),
        ('在坎昆做城市酒店还是海滨酒店？', '城市酒店（Supermanzanas、机场走廊）全年运营、季节性更弱、每间客房投入更低；海滨酒店房价更高，但需增加 FONATUR、ZOFEMAT 与完整海洋环境做法。')]},
}

LINKS = {
 'es': {'vh-playa-del-carmen': [('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/villas-de-lujo-playa-del-carmen/','Villas de lujo'), ('/construccion-comercial-hoteles-riviera-maya/','Construcción comercial y hoteles'), ('/calculadora/','Calculadora de costos')],
        'vh-tulum': [('/construccion-de-casas-tulum/','Construcción de casas en Tulum'), ('/construccion-eco-lodge-retiro-tulum/','Eco-lodges y retiros en Tulum'), ('/construccion-comercial-hoteles-riviera-maya/','Construcción comercial y hoteles'), ('/calculadora/','Calculadora de costos')],
        'vh-cancun': [('/construccion-de-casas-cancun/','Construcción de casas en Cancún'), ('/constructora-cancun/','Constructora en Cancún'), ('/construccion-comercial-hoteles-riviera-maya/','Construcción comercial y hoteles'), ('/calculadora/','Calculadora de costos')]},
 'en': {'vh-playa-del-carmen': [('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/luxury-villa-construction-playa-del-carmen/','Luxury villas'), ('/commercial-hotel-construction-riviera-maya/','Commercial and hotel construction'), ('/calculator/','Cost calculator')],
        'vh-tulum': [('/house-construction-tulum/','House construction in Tulum'), ('/eco-lodge-wellness-retreat-construction-tulum/','Eco-lodges and retreats in Tulum'), ('/commercial-hotel-construction-riviera-maya/','Commercial and hotel construction'), ('/calculator/','Cost calculator')],
        'vh-cancun': [('/house-construction-cancun/','House construction in Cancún'), ('/construction-company-cancun/','Construction company in Cancún'), ('/commercial-hotel-construction-riviera-maya/','Commercial and hotel construction'), ('/calculator/','Cost calculator')]},
}
for _lang, _pref, _calc, _blog in [('ru', 'stroitelstvo-domov', '/kalkulyator/', '/blog-ru/'),
                                   ('de', 'hausbau', '/kostenrechner/', '/blog-de/'),
                                   ('fr', 'construction-de-maisons', '/calculateur/', '/blog-fr/'),
                                   ('zh', 'zhuzhai-jianzao', '/jisuanqi/', '/blog-zh/')]:
    hub = {'ru': 'Строительство домов', 'de': 'Hausbau', 'fr': 'Construction de maisons', 'zh': '住宅建造'}[_lang]
    perm = {'ru': ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'),
            'de': ('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen, Lizenzen und DRO'),
            'fr': ('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'),
            'zh': ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO')}[_lang]
    names = {'ru': ('Калькулятор стоимости', 'Гиды по строительству'), 'de': ('Kostenrechner', 'Bau-Leitfäden'),
             'fr': ('Calculateur de coûts', 'Guides de construction'), 'zh': ('造价计算器', '建筑指南')}[_lang]
    LINKS[_lang] = {}
    for _z, _d in CITIES.items():
        LINKS[_lang][_z] = [('/%s-%s/' % (_pref, _d['parent']), '%s — %s' % (hub, ml.CITY[_lang][_d['parent']])),
                            perm, ('/%s-riviera-maya/' % _pref, '%s — %s' % (hub, ml.CITY[_lang]['riviera-maya'])),
                            (_calc, names[0]), (_blog, names[1])]


def block(z, lang):
    b = il.BLOCK_STR[lang]; c = NAMES[z][lang]
    rows = '\n'.join('<tr><td>%s</td><td>%s USD</td><td>%s</td></tr>' % (r[0], k, r[1])
                     for r, k in zip(b['rows'], KEYS[z]))
    lis = '\n'.join('<li>%s</li>' % x for x in b['li'])
    return ('<h2 class="mt-4">%s</h2>\n<p>%s</p>\n'
            '<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark">'
            '<tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>\n%s\n</tbody></table></div>\n'
            '<h3 class="mt-3">%s</h3>\n<ul>\n%s\n</ul>'
            % (b['h'].format(c=c), b['p'], b['th'][0], b['th'][1], b['th'][2], rows, b['h2'], lis))


if __name__ == '__main__':
    for z in CITIES:
        z1.ZAREA[z] = AREAS[z]; z1.ZTEXT[z] = TEXT[z]; z1.ZFAQ[z] = FAQ[z]
    for lang in LINKS:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS[lang])
    for k in ['h1', 'title', 'desc', 'block', 'alert', 'h_cost', 'row', 'h_proc']:
        ml.OVR.setdefault(k, {})
    for z, d in CITIES.items():
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            ml.SLUG[lang][z] = '%s-%s' % (SLUG_PREFIX[lang], BASE_SLUG[z])
            ml.NORM[lang][z] = NORM[z][lang]
            c = NAMES[z][lang]
            nm = ml.NUM[z]
            ml.OVR['h1'].setdefault(z, {})[lang] = il.H1[lang].format(c=c)
            ml.OVR['title'].setdefault(z, {})[lang] = il.TITLE[lang].format(c=c)
            ml.OVR['desc'].setdefault(z, {})[lang] = il.DESC[lang].format(c=c)
            ml.OVR['alert'].setdefault(z, {})[lang] = il.ALERT[lang].format(
                c=c, m2=nm['m2'], usd=nm['usd'], key=KEYS[z][2].split(' – ')[0])
            ml.OVR['h_cost'].setdefault(z, {})[lang] = il.H_COST[lang].format(c=c)
            ml.OVR['row'].setdefault(z, {})[lang] = il.ROW[lang]
            ml.OVR['h_proc'].setdefault(z, {})[lang] = il.H_PROC[lang]
            ml.OVR['block'].setdefault(z, {})[lang] = block(z, lang)
    ml.LOCS.extend(CITIES)
    for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
        ch = ml.chrome(lang)
        for z in CITIES:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-50s %6d bytes' % (out + '/', len(html)))
