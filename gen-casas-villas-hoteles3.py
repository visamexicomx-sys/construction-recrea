#!/usr/bin/env python3
"""Villa + hospitality pages for four gated communities (2026-08-09):
Tulum Country Club, Playacar, Mayakoba and Corasol.

Different from the city villa/hotel pages in one honest respect: inside a gated
master plan you cannot simply decide to build a hotel. Hotel use has to be allowed
by BOTH the master plan and the municipal land use; in purely residential phases it
is not, and the workable formats are branded residences or condo-hotel where the
developer permits them. Every page says that up front instead of selling a hotel
that cannot be licensed.

The villa m² band equals the community's existing house-construction page (same
factor), so the site stays consistent with itself. The per-key tiers are relabelled
for this segment — "economy / hostel" makes no sense in Mayakoba.
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
vh1 = load('gen-casas-villas-hoteles.py', 'vh1')
z1 = vh1.z1
il = vh1.il
ml = vh1.ml
SLUG_PREFIX = vh1.SLUG_PREFIX

# reuse each community's own factor so the villa band matches its house page
ZONES = {
 'vh-playacar':           dict(parent='playa-del-carmen', f=1.25, perm='2–4', zone='playacar'),
 'vh-mayakoba':           dict(parent='playa-del-carmen', f=1.42, perm='3–5', zone='mayakoba'),
 'vh-corasol':            dict(parent='playa-del-carmen', f=1.30, perm='2–4', zone='corasol'),
 'vh-tulum-country-club': dict(parent='tulum',            f=1.13, perm='3–5', zone='tulum-country-club'),
}
BASE_SLUG = {k: d['zone'] for k, d in ZONES.items()}

NAMES = {
 'vh-playacar': {'es': 'Playacar', 'en': 'Playacar', 'ru': 'Плаякаре', 'de': 'Playacar', 'fr': 'Playacar', 'zh': 'Playacar'},
 'vh-mayakoba': {'es': 'Mayakoba', 'en': 'Mayakoba', 'ru': 'Майякобе', 'de': 'Mayakoba', 'fr': 'Mayakoba', 'zh': 'Mayakoba'},
 'vh-corasol': {'es': 'Corasol', 'en': 'Corasol', 'ru': 'Корасоле', 'de': 'Corasol', 'fr': 'Corasol', 'zh': 'Corasol'},
 'vh-tulum-country-club': {'es': 'Tulum Country Club', 'en': 'Tulum Country Club', 'ru': 'Tulum Country Club',
                           'de': 'Tulum Country Club', 'fr': 'Tulum Country Club', 'zh': 'Tulum Country Club'},
}
AREAS = {
 'vh-playacar': {'es': 'Playacar Fase I y Fase II', 'en': 'Playacar Phase I and Phase II', 'ru': 'Плаякар Фаза I и Фаза II',
   'de': 'Playacar Phase I und Phase II', 'fr': 'Playacar Phase I et Phase II', 'zh': 'Playacar 一期与二期'},
 'vh-mayakoba': {'es': 'Mayakoba y sus residencias privadas', 'en': 'Mayakoba and its private residences',
   'ru': 'Майякобе и её частных резиденциях', 'de': 'Mayakoba und seinen privaten Residenzen',
   'fr': 'Mayakoba et ses résidences privées', 'zh': 'Mayakoba 及其私人住宅区'},
 'vh-corasol': {'es': 'Corasol y sus secciones de golf', 'en': 'Corasol and its golf sections',
   'ru': 'Корасоле и его гольф-секциях', 'de': 'Corasol und seinen Golfabschnitten',
   'fr': 'Corasol et ses sections de golf', 'zh': 'Corasol 及其高尔夫区段'},
 'vh-tulum-country-club': {'es': 'Tulum Country Club y las zonas de golf de Tulum', 'en': 'Tulum Country Club and Tulum’s golf areas',
   'ru': 'Tulum Country Club и гольф-районах Тулума', 'de': 'Tulum Country Club und den Golfgebieten von Tulum',
   'fr': 'Tulum Country Club et les secteurs de golf de Tulum', 'zh': 'Tulum Country Club 及图卢姆高尔夫片区'},
}

# branded / boutique premium / entry boutique, USD per key
KEYS = {
 'vh-playacar':           ('$170,000 – $270,000', '$130,000 – $200,000', '$100,000 – $150,000'),
 'vh-mayakoba':           ('$200,000 – $320,000', '$150,000 – $230,000', '$120,000 – $175,000'),
 'vh-corasol':            ('$160,000 – $260,000', '$125,000 – $195,000', '$95,000 – $145,000'),
 'vh-tulum-country-club': ('$150,000 – $240,000', '$115,000 – $180,000', '$90,000 – $140,000'),
}
# tier labels for the gated-community segment
ROWS = {
 'es': [('Residencias de marca / resort', 'Estándar de hotelería internacional: spa, restaurante, áreas comunes y servicio de resort'),
        ('Boutique premium', 'Habitación amplia, alberca, terraza y áreas comunes de diseño'),
        ('Boutique de entrada', 'Habitación completa con acabados de la comunidad, áreas comunes simples')],
 'en': [('Branded residences / resort', 'International hospitality standard: spa, restaurant, common areas and resort service'),
        ('Premium boutique', 'Generous room, pool, terrace and designed common areas'),
        ('Entry boutique', 'Complete room with the community’s finish standard, simple common areas')],
 'ru': [('Брендовые резиденции / резорт', 'Международный гостиничный стандарт: спа, ресторан, общие зоны и сервис резорта'),
        ('Премиальный бутик', 'Просторный номер, бассейн, терраса и общие зоны с дизайном'),
        ('Бутик начального уровня', 'Полноценный номер в стандарте отделки посёлка, простые общие зоны')],
 'de': [('Branded Residences / Resort', 'Internationaler Hotelstandard: Spa, Restaurant, Gemeinschaftsbereiche und Resort-Service'),
        ('Premium-Boutique', 'Großzügiges Zimmer, Pool, Terrasse und gestaltete Gemeinschaftsbereiche'),
        ('Einstiegs-Boutique', 'Komplettes Zimmer im Ausbaustandard der Anlage, einfache Gemeinschaftsbereiche')],
 'fr': [('Résidences de marque / resort', 'Standard hôtelier international : spa, restaurant, parties communes et service resort'),
        ('Boutique premium', 'Chambre généreuse, piscine, terrasse et parties communes dessinées'),
        ('Boutique d’entrée', 'Chambre complète au standard de finition de la résidence, parties communes simples')],
 'zh': [('品牌住宅 / 度假村', '国际酒店标准：水疗、餐厅、公共区域与度假村式服务'),
        ('高端精品', '宽敞客房、泳池、露台与经设计的公共区域'),
        ('入门精品', '按社区装修标准交付的完整客房，公共区域从简')],
}

TEXT = {
'vh-playacar': {
 'es': 'Playacar combina lo que casi ningún fraccionamiento tiene: golf, playa privada, vigilancia y una zona hotelera consolidada en la Fase I. Para villa, el producto es claro y el reglamento de diseño manda. Para hotelería, la clave es el uso de suelo: la Fase I admite giro hotelero en predios específicos, mientras que las secciones residenciales no. Lo verificamos lote por lote antes de que usted compre, porque de eso depende que el proyecto exista.',
 'en': 'Playacar combines what almost no gated estate has: golf, private beach, security and an established hotel strip in Phase I. For a villa the product is clear and the design code rules. For hospitality the key is land use: Phase I allows hotel use on specific lots, while the residential sections do not. We verify it lot by lot before you buy, because that is what decides whether the project can exist at all.',
 'ru': 'Плаякар сочетает то, чего почти нет ни у одного посёлка: гольф, приватный пляж, охрана и сложившаяся отельная зона в Фазе I. Для виллы продукт понятен, и правит регламент дизайна. Для гостиницы ключ — назначение земли: Фаза I допускает гостиничный профиль на конкретных участках, жилые секции — нет. Проверяем по каждому лоту до покупки, потому что от этого зависит, состоится ли проект вообще.',
 'de': 'Playacar vereint, was kaum eine Anlage hat: Golf, Privatstrand, Bewachung und einen etablierten Hotelstreifen in Phase I. Für eine Villa ist das Produkt klar und die Gestaltungssatzung bestimmend. Für Hotellerie entscheidet die Nutzungsart: Phase I lässt Hotelnutzung auf bestimmten Grundstücken zu, die Wohnabschnitte nicht. Wir prüfen das vor dem Kauf Grundstück für Grundstück — davon hängt ab, ob das Projekt überhaupt möglich ist.',
 'fr': 'Playacar réunit ce que presque aucune résidence n’offre : golf, plage privée, sécurité et une zone hôtelière établie en Phase I. Pour une villa, le produit est clair et le règlement architectural commande. Pour l’hôtellerie, la clé est l’usage du sol : la Phase I autorise l’usage hôtelier sur des lots précis, les sections résidentielles non. Nous le vérifions lot par lot avant l’achat, car c’est ce qui décide si le projet peut exister.',
 'zh': 'Playacar 兼具几乎没有其他社区能同时提供的条件：高尔夫、私人海滩、安保，以及一期已成熟的酒店带。就别墅而言，产品定位清晰，由设计规约主导；就酒店而言，关键在土地用途：一期的特定地块允许酒店用途，而住宅区段不允许。我们会在您购地前逐地块核实——这决定了项目能否成立。'},
'vh-mayakoba': {
 'es': 'Mayakoba es hotelería de clase mundial y residencias privadas en el mismo complejo, con campo de golf PGA y un control de obra que no se parece a nada más en la costa. Aquí la villa se construye al estándar del resort, y cualquier proyecto de hospedaje pasa por el comité de diseño, las reglas ambientales de lagunas y manglar y la coordinación de accesos, horarios y proveedores. Es el segmento más alto de la región y el que menos tolera improvisación.',
 'en': 'Mayakoba is world-class hospitality and private residences inside the same complex, with a PGA golf course and construction control unlike anywhere else on the coast. Here the villa is built to resort standard, and any lodging project goes through the design committee, the lagoon and mangrove environmental rules and coordinated access, hours and suppliers. It is the region’s highest segment and the one that tolerates improvisation least.',
 'ru': 'Майякоба — это гостиничный бизнес мирового уровня и частные резиденции в одном комплексе, с полем PGA и контролем стройки, которого нет больше нигде на побережье. Вилла здесь строится в стандарте резорта, а любой проект размещения проходит комитет по дизайну, экологические правила лагун и мангров и согласование доступа, часов и поставщиков. Это самый верхний сегмент региона и наименее терпимый к импровизации.',
 'de': 'Mayakoba ist Weltklasse-Hotellerie und private Residenzen im selben Komplex, mit PGA-Golfplatz und einer Baukontrolle, die es sonst nirgends an der Küste gibt. Die Villa wird hier im Resort-Standard gebaut, und jedes Beherbergungsprojekt durchläuft den Gestaltungsbeirat, die Umweltregeln für Lagunen und Mangroven sowie die Abstimmung von Zufahrt, Zeiten und Lieferanten. Das höchste Segment der Region — und das am wenigsten improvisationsfreundliche.',
 'fr': 'Mayakoba, c’est une hôtellerie de classe mondiale et des résidences privées dans le même complexe, avec un golf PGA et un contrôle de chantier sans équivalent sur la côte. La villa s’y construit au standard du resort, et tout projet d’hébergement passe par le comité d’architecture, les règles environnementales des lagunes et de la mangrove et la coordination des accès, horaires et fournisseurs. C’est le segment le plus haut de la région et le moins tolérant à l’improvisation.',
 'zh': 'Mayakoba 在同一综合体内汇聚了世界级酒店与私人住宅，拥有 PGA 高尔夫球场，以及海岸线上独一无二的施工管控体系。别墅按度假村标准建造；任何住宿类项目都须经设计委员会审核，遵守泻湖与红树林的环保规定，并统一协调出入、作业时段与供应商。这是全区最高端、也最容不得临场发挥的板块。'},
'vh-corasol': {
 'es': 'Corasol es la comunidad de golf de Playa del Carmen, con lotes amplios, beach club y lineamientos de diseño del desarrollo. La villa aquí se piensa para vivir todo el año o para renta de estancia larga, más que para rotación diaria. Para hospedaje, el uso de suelo y el reglamento del desarrollo definen qué es posible: donde se permite, el formato natural es boutique pequeño o residencias con servicio. Nuestra oficina está en Corasol, así que la supervisión es diaria.',
 'en': 'Corasol is Playa del Carmen’s golf community, with generous lots, a beach club and developer design guidelines. The villa here is conceived for year-round living or long-stay rental rather than daily turnover. For lodging, land use and the development’s rules define what is possible: where it is allowed, the natural format is a small boutique or serviced residences. Our office is in Corasol, so supervision is daily.',
 'ru': 'Корасоль — гольф-комьюнити Плая-дель-Кармен: просторные участки, бич-клуб и дизайн-регламент застройщика. Вилла здесь проектируется под круглогодичную жизнь или长 длительную аренду, а не под ежедневную ротацию. Для размещения возможности задают назначение земли и регламент застройки: где разрешено, естественный формат — небольшой бутик или резиденции с сервисом. Наш офис в Корасоле, поэтому надзор ежедневный.',
 'de': 'Corasol ist die Golf-Community von Playa del Carmen: großzügige Grundstücke, Beachclub und Gestaltungsrichtlinien des Entwicklers. Die Villa wird hier für ganzjähriges Wohnen oder Langzeitvermietung gedacht, nicht für täglichen Wechsel. Für Beherbergung bestimmen Nutzungsart und Anlagensatzung, was möglich ist: wo erlaubt, ist das natürliche Format ein kleines Boutiquehotel oder Serviced Residences. Unser Büro liegt in Corasol, die Überwachung erfolgt täglich.',
 'fr': 'Corasol est la communauté de golf de Playa del Carmen : grands terrains, beach club et lignes directrices architecturales du promoteur. La villa s’y conçoit pour vivre à l’année ou pour la location longue durée, plutôt que pour la rotation quotidienne. Pour l’hébergement, l’usage du sol et le règlement du développement définissent le possible : là où c’est autorisé, le format naturel est un petit boutique ou des résidences avec services. Notre bureau est à Corasol : la supervision est quotidienne.',
 'zh': 'Corasol 是普拉亚德尔卡门的高尔夫社区：地块宽阔、设有海滩俱乐部，并有开发商制定的设计导则。此处的别墅更适合按全年居住或长租设计，而非按天周转。就住宿业态而言，可行性由土地用途与社区规约决定：在允许的位置，自然的形态是小型精品酒店或带服务的住宅。我们的办公室就在 Corasol，因此监理为每日到场。'},
'vh-tulum-country-club': {
 'es': 'Tulum Country Club es golf y selva dentro del municipio de Tulum: lotes grandes, lineamientos del desarrollo y un estándar de acabados alto. La villa es el producto principal; para hospedaje, además del reglamento interno hay que resolver el uso de suelo y la ruta ambiental de Tulum, que es la más larga de la costa. Diseñamos el proyecto ya conforme a la norma y arrancamos SEMA en paralelo, porque aquí el calendario de permisos define la fecha de apertura.',
 'en': 'Tulum Country Club is golf and jungle inside the municipality of Tulum: large lots, developer guidelines and a high finish standard. The villa is the main product; for lodging, on top of the internal rules you have to solve land use and Tulum’s environmental route, the longest on the coast. We design compliant from the start and open the SEMA process in parallel, because here the permit calendar sets the opening date.',
 'ru': 'Tulum Country Club — это гольф и сельва внутри муниципалитета Тулум: крупные участки, регламент застройки и высокий стандарт отделки. Вилла — основной продукт; для размещения, помимо внутреннего регламента, нужно решить назначение земли и экологический маршрут Тулума, самый长 длинный на побережье. Проектируем сразу под норму и запускаем SEMA параллельно, потому что здесь календарь разрешений определяет дату открытия.',
 'de': 'Tulum Country Club ist Golf und Dschungel in der Gemeinde Tulum: große Grundstücke, Entwicklerrichtlinien und ein hoher Ausbaustandard. Die Villa ist das Hauptprodukt; für Beherbergung müssen neben der internen Satzung die Nutzungsart und Tulums Umweltweg gelöst werden — der längste der Küste. Wir planen von Anfang an normkonform und starten die SEMA parallel, denn hier bestimmt der Genehmigungskalender das Eröffnungsdatum.',
 'fr': 'Tulum Country Club, c’est le golf et la jungle dans la commune de Tulum : grands terrains, lignes directrices du promoteur et standard de finition élevé. La villa est le produit principal ; pour l’hébergement, au-delà du règlement interne, il faut régler l’usage du sol et le parcours environnemental de Tulum, le plus long de la côte. Nous concevons conforme dès le départ et ouvrons la procédure SEMA en parallèle, car ici le calendrier des permis fixe la date d’ouverture.',
 'zh': 'Tulum Country Club 是位于图卢姆市辖内的高尔夫与雨林社区：地块宽大、设有开发导则、装修标准较高。别墅是主力产品；若做住宿业态，除社区内部规约外，还须解决土地用途与图卢姆的环保路径——这是海岸线上最漫长的一条。我们从一开始就按法规设计，并同步启动 SEMA 报批，因为在这里，许可进度决定开业日期。'},
}

NORM = {
'vh-playacar': {
 'es': 'Doble vía, siempre: comité de diseño de Playacar (alturas, retiros, cubiertas, colores, materiales) y licencia municipal de Solidaridad con DRO. Para hospedaje, lo primero es la constancia de uso de suelo: solo algunos predios admiten giro hotelero, y sin eso no hay proyecto. Después vienen licencia de funcionamiento, visto bueno de Protección Civil, proyecto eléctrico ante CFE por aforo y registro turístico. Frente al mar, además, concesión ZOFEMAT.',
 'en': 'Two tracks, always: the Playacar design committee (heights, setbacks, roofs, colours, materials) and the Solidaridad municipal licence with a DRO. For lodging the first step is the land-use certificate: only some lots allow hotel use, and without it there is no project. Then come the operating licence, Civil Protection sign-off, a CFE electrical project sized to occupancy and tourism registration. Beachfront adds a ZOFEMAT concession.',
 'ru': 'Всегда два трека: комитет по дизайну Плаякара (высоты, отступы, кровли, цвета, материалы) и муниципальная лицензия Solidaridad с DRO. Для размещения первое — справка о назначении земли: гостиничный профиль допускают лишь некоторые участки, без этого проекта нет. Дальше — лицензия на деятельность, заключение Гражданской защиты, электропроект в CFE под вместимость и туристическая регистрация. На первой линии — ещё и концессия ZOFEMAT.',
 'de': 'Immer zweigleisig: Gestaltungsbeirat von Playacar (Höhen, Abstände, Dächer, Farben, Materialien) und kommunale Lizenz von Solidaridad mit DRO. Für Beherbergung steht zuerst die Nutzungsbescheinigung: Nur manche Grundstücke lassen Hotelnutzung zu — ohne sie gibt es kein Projekt. Danach Betriebslizenz, Freigabe des Zivilschutzes, CFE-Elektroprojekt nach Belegung und Tourismusregistrierung. Am Strand zusätzlich die ZOFEMAT-Konzession.',
 'fr': 'Toujours deux voies : le comité d’architecture de Playacar (hauteurs, reculs, toitures, couleurs, matériaux) et le permis municipal de Solidaridad avec DRO. Pour l’hébergement, la première étape est le certificat d’usage du sol : seuls certains lots admettent l’usage hôtelier, sans quoi il n’y a pas de projet. Viennent ensuite la licence d’exploitation, l’avis de la Protection Civile, le projet électrique CFE selon capacité et l’enregistrement touristique. En front de mer, la concession ZOFEMAT s’ajoute.',
 'zh': '始终是两条线并行：Playacar 设计委员会（高度、退线、屋面、色彩、材料）与带 DRO 的 Solidaridad 市政许可。做住宿业态的第一步是土地用途证明：仅部分地块允许酒店用途，没有它就没有项目。其后依次是经营许可、民防意见、按容量向 CFE 报批的电气方案与旅游登记。海滨地块另需 ZOFEMAT 特许。'},
'vh-mayakoba': {
 'es': 'Además de la licencia municipal de Solidaridad con DRO, en Mayakoba manda el comité de diseño del complejo y el control ambiental por las lagunas y el manglar: desmonte, escurrimientos, manejo de residuos y horarios están reglamentados, y los accesos y proveedores se autorizan. Cualquier proyecto de hospedaje requiere que el uso de suelo y el máster plan lo permitan; donde se permite, el formato suele ser residencias de marca o condo-hotel, con licencia de funcionamiento, Protección Civil y registro turístico.',
 'en': 'On top of the Solidaridad municipal licence with a DRO, Mayakoba is governed by the complex’s design committee and environmental control for the lagoons and mangrove: clearing, runoff, waste handling and hours are regulated, and access and suppliers are authorised. Any lodging project requires that land use and the master plan allow it; where they do, the usual format is branded residences or condo-hotel, with operating licence, Civil Protection and tourism registration.',
 'ru': 'Помимо муниципальной лицензии Solidaridad с DRO, в Майякобе правят комитет по дизайну комплекса и экологический контроль из-за лагун и мангров: расчистка, сток, обращение с отходами и часы работ регламентированы, доступ и поставщики согласуются. Любой проект размещения требует, чтобы это допускали назначение земли и мастер-план; где допускают, формат обычно — брендовые резиденции или кондо-отель, с лицензией на деятельность, Гражданской защитой и туристической регистрацией.',
 'de': 'Neben der kommunalen Lizenz von Solidaridad mit DRO bestimmen in Mayakoba der Gestaltungsbeirat des Komplexes und die Umweltkontrolle für Lagunen und Mangroven: Rodung, Abfluss, Abfallentsorgung und Zeiten sind geregelt, Zufahrt und Lieferanten werden freigegeben. Jedes Beherbergungsprojekt setzt voraus, dass Nutzungsart und Masterplan es zulassen; wo ja, ist das übliche Format Branded Residences oder Condo-Hotel, mit Betriebslizenz, Zivilschutz und Tourismusregistrierung.',
 'fr': 'Outre le permis municipal de Solidaridad avec DRO, Mayakoba est régi par le comité d’architecture du complexe et le contrôle environnemental des lagunes et de la mangrove : défrichement, ruissellement, gestion des déchets et horaires sont encadrés, accès et fournisseurs autorisés. Tout projet d’hébergement suppose que l’usage du sol et le plan-masse l’autorisent ; le cas échéant, le format habituel est la résidence de marque ou le condo-hôtel, avec licence d’exploitation, Protection Civile et enregistrement touristique.',
 'zh': '除带 DRO 的 Solidaridad 市政许可外，Mayakoba 还由综合体设计委员会与针对泻湖、红树林的环境管控主导：清林、径流、废弃物处理与作业时段均有规定，出入与供应商需经批准。任何住宿类项目都须以土地用途与总体规划允许为前提；在允许的情形下，常见形态为品牌住宅或产权式酒店，并需经营许可、民防意见与旅游登记。'},
'vh-corasol': {
 'es': 'Licencia municipal de Solidaridad con DRO y lineamientos de diseño del desarrollo (volumetría, materiales, alturas, áreas verdes), que se presentan en paralelo. Para hospedaje, la pregunta previa es si el uso de suelo del lote y el reglamento del desarrollo lo permiten; donde sí, se suman licencia de funcionamiento, Protección Civil, capacidad eléctrica por aforo y registro turístico. Coordinamos accesos y horarios con la administración desde el arranque de obra.',
 'en': 'Solidaridad municipal licence with a DRO plus the development’s design guidelines (massing, materials, heights, green areas), filed in parallel. For lodging, the prior question is whether the lot’s land use and the development’s rules allow it; where they do, add the operating licence, Civil Protection, occupancy-based electrical capacity and tourism registration. We coordinate access and working hours with the estate management from day one on site.',
 'ru': 'Муниципальная лицензия Solidaridad с DRO плюс дизайн-регламент застройки (объём, материалы, высоты, зелёные зоны) — подаются параллельно. Для размещения предварительный вопрос: допускают ли это назначение земли участка и регламент застройки; где допускают, добавляются лицензия на деятельность, Гражданская защита, мощность под вместимость и туристическая регистрация. Доступ и часы работ согласуем с администрацией с первого дня стройки.',
 'de': 'Kommunale Lizenz von Solidaridad mit DRO plus die Gestaltungsrichtlinien der Anlage (Baukörper, Materialien, Höhen, Grünflächen), parallel eingereicht. Für Beherbergung lautet die Vorfrage, ob Nutzungsart des Grundstücks und Anlagensatzung es zulassen; wenn ja, kommen Betriebslizenz, Zivilschutz, belegungsabhängige Leistung und Tourismusregistrierung hinzu. Zufahrt und Bauzeiten stimmen wir ab dem ersten Tag mit der Verwaltung ab.',
 'fr': 'Permis municipal de Solidaridad avec DRO et lignes directrices architecturales du développement (volumétrie, matériaux, hauteurs, espaces verts), déposés en parallèle. Pour l’hébergement, la question préalable est de savoir si l’usage du sol du lot et le règlement du développement l’autorisent ; le cas échéant, s’ajoutent la licence d’exploitation, la Protection Civile, la puissance selon capacité et l’enregistrement touristique. Nous coordonnons accès et horaires avec l’administration dès l’ouverture du chantier.',
 'zh': '带 DRO 的 Solidaridad 市政许可，加上开发商设计导则（体量、材料、高度、绿地），两者并行报审。就住宿业态而言，前置问题是地块土地用途与社区规约是否允许；若允许，还需经营许可、民防意见、按容量核定的用电容量与旅游登记。自进场首日起，我们即与物业管理方协调出入与作业时段。'},
'vh-tulum-country-club': {
 'es': 'Tres frentes: comité de diseño del desarrollo, licencia municipal de Tulum con DRO y autorización ambiental de SEMA, que aplica en la mayoría de los predios. Para hospedaje se suma el uso de suelo con giro y, después, licencia de funcionamiento, Protección Civil, capacidad eléctrica ante CFE y registro turístico. Con SEMA de por medio, presupueste de 3 a 5 meses de permisos y arranque el trámite junto con el anteproyecto, no al final.',
 'en': 'Three fronts: the development’s design committee, the Tulum municipal licence with a DRO and SEMA environmental authorisation, which applies on most lots. Lodging adds hotel-use zoning and then the operating licence, Civil Protection, CFE capacity and tourism registration. With SEMA involved, budget 3 to 5 months of permits and start the process alongside the concept design, not at the end.',
 'ru': 'Три фронта: комитет по дизайну застройки, муниципальная лицензия Тулума с DRO и экологическая авторизация SEMA, которая действует на большинстве участков. Для размещения добавляется назначение земли под профиль, а затем лицензия на деятельность, Гражданская защита, мощность в CFE и туристическая регистрация. С участием SEMA закладывайте 3–5 месяцев на разрешения и запускайте процедуру вместе с эскизом, а не в конце.',
 'de': 'Drei Fronten: Gestaltungsbeirat der Anlage, kommunale Lizenz von Tulum mit DRO und SEMA-Umweltgenehmigung, die für die meisten Grundstücke gilt. Beherbergung ergänzt die Hotel-Nutzungsart und danach Betriebslizenz, Zivilschutz, CFE-Leistung und Tourismusregistrierung. Mit der SEMA im Spiel: 3 bis 5 Monate Genehmigungen einplanen und das Verfahren mit dem Entwurf starten, nicht am Ende.',
 'fr': 'Trois fronts : le comité d’architecture du développement, le permis municipal de Tulum avec DRO et l’autorisation environnementale de la SEMA, applicable sur la plupart des lots. L’hébergement ajoute l’usage hôtelier puis la licence d’exploitation, la Protection Civile, la puissance CFE et l’enregistrement touristique. Avec la SEMA, comptez 3 à 5 mois de permis et lancez la procédure avec l’avant-projet, pas à la fin.',
 'zh': '三条战线：社区设计委员会、带 DRO 的图卢姆市政许可，以及多数地块适用的 SEMA 环保许可。住宿业态还需先取得酒店类土地用途，随后办理经营许可、民防意见、CFE 用电容量与旅游登记。涉及 SEMA 时，请预留3至5个月许可周期，并在方案阶段同步启动，而非收尾时才办。'},
}

FAQ = {
'vh-playacar': {
 'es': [('¿Se puede construir un hotel en Playacar?', 'Solo en predios cuyo uso de suelo admita giro hotelero, concentrados en la Fase I. En las secciones residenciales no. Revisamos la constancia de uso de suelo antes de que usted compre: es lo que decide si el proyecto existe.'),
        ('¿Cuánto cuesta por llave aquí?', 'De $100,000 a $270,000 USD por llave. El estándar del fraccionamiento y su reglamento de fachadas colocan el piso más alto que en el resto de Playa del Carmen.')],
 'en': [('Can you build a hotel in Playacar?', 'Only on lots whose land use allows hotel operation, concentrated in Phase I. Not in the residential sections. We check the land-use certificate before you buy — it decides whether the project exists at all.'),
        ('What is the cost per key here?', 'From $100,000 to $270,000 USD per key. The estate standard and its façade rules set a higher floor than the rest of Playa del Carmen.')],
 'ru': [('Можно ли построить отель в Плаякаре?', 'Только на участках, где назначение земли допускает гостиничный профиль, — они сосредоточены в Фазе I. В жилых секциях нельзя. Проверяем справку о назначении земли до покупки: именно это решает, состоится ли проект.'),
        ('Сколько стоит здесь номер?', 'От $100,000 до $270,000 USD за номер. Стандарт посёлка и регламент по фасадам задают более высокий порог, чем в остальной Плая-дель-Кармен.')],
 'de': [('Kann man in Playacar ein Hotel bauen?', 'Nur auf Grundstücken, deren Nutzungsart Hotelbetrieb zulässt — konzentriert in Phase I. In den Wohnabschnitten nicht. Wir prüfen die Nutzungsbescheinigung vor dem Kauf: Sie entscheidet, ob das Projekt überhaupt existiert.'),
        ('Wie hoch sind die Kosten pro Zimmer?', 'Von $100.000 bis $270.000 USD pro Zimmer. Anlagenstandard und Fassadensatzung setzen ein höheres Niveau als im übrigen Playa del Carmen.')],
 'fr': [('Peut-on construire un hôtel à Playacar ?', 'Uniquement sur des lots dont l’usage du sol autorise l’exploitation hôtelière, concentrés en Phase I. Pas dans les sections résidentielles. Nous vérifions le certificat d’usage du sol avant l’achat : c’est lui qui décide si le projet existe.'),
        ('Quel coût par clé ici ?', 'De 100 000 à 270 000 USD par clé. Le standard de la résidence et son règlement de façades placent le plancher plus haut que dans le reste de Playa del Carmen.')],
 'zh': [('在 Playacar 可以建酒店吗？', '仅限土地用途允许酒店经营的地块，主要集中在一期；住宅区段不可。我们会在您购地前核查土地用途证明——它决定项目是否成立。'),
        ('这里每间客房造价是多少？', '每间客房 100,000 至 270,000 美元。社区标准与立面规约使其起点高于普拉亚德尔卡门其他片区。')]},
'vh-mayakoba': {
 'es': [('¿Qué formato de hospedaje es viable en Mayakoba?', 'Donde el máster plan y el uso de suelo lo permiten, residencias de marca o condo-hotel; no hotelería independiente en secciones residenciales. Confirmamos la factibilidad antes de diseñar.'),
        ('¿Por qué el costo por llave es el más alto de la costa?', 'Estándar de acabados de resort, logística de obra regulada (accesos, horarios, proveedores autorizados) y requisitos ambientales por lagunas y manglar. De $120,000 a $320,000 USD por llave.')],
 'en': [('What lodging format is viable in Mayakoba?', 'Where the master plan and land use allow it, branded residences or condo-hotel; not standalone hospitality in residential sections. We confirm feasibility before designing.'),
        ('Why is the cost per key the highest on the coast?', 'Resort finish standard, regulated site logistics (access, hours, approved suppliers) and environmental requirements for the lagoons and mangrove. From $120,000 to $320,000 USD per key.')],
 'ru': [('Какой формат размещения возможен в Майякобе?', 'Там, где допускают мастер-план и назначение земли, — брендовые резиденции или кондо-отель; самостоятельная гостиница в жилых секциях — нет. Подтверждаем возможность до проектирования.'),
        ('Почему цена за номер самая высокая на побережье?', 'Стандарт отделки резорта, регламентированная логистика стройки (доступ, часы, допущенные поставщики) и экологические требования из-за лагун и мангров. От $120,000 до $320,000 USD за номер.')],
 'de': [('Welches Beherbergungsformat ist in Mayakoba machbar?', 'Wo Masterplan und Nutzungsart es zulassen: Branded Residences oder Condo-Hotel; keine eigenständige Hotellerie in Wohnabschnitten. Wir klären die Machbarkeit vor dem Entwurf.'),
        ('Warum sind die Kosten pro Zimmer die höchsten der Küste?', 'Resort-Ausbaustandard, regulierte Baulogistik (Zufahrt, Zeiten, zugelassene Lieferanten) und Umweltauflagen wegen Lagunen und Mangroven. Von $120.000 bis $320.000 USD pro Zimmer.')],
 'fr': [('Quel format d’hébergement est viable à Mayakoba ?', 'Là où le plan-masse et l’usage du sol l’autorisent : résidences de marque ou condo-hôtel ; pas d’hôtellerie indépendante dans les sections résidentielles. Nous confirmons la faisabilité avant de concevoir.'),
        ('Pourquoi le coût par clé y est-il le plus élevé de la côte ?', 'Standard de finition resort, logistique de chantier encadrée (accès, horaires, fournisseurs agréés) et exigences environnementales liées aux lagunes et à la mangrove. De 120 000 à 320 000 USD par clé.')],
 'zh': [('在 Mayakoba，哪种住宿形态可行？', '在总体规划与土地用途允许之处：品牌住宅或产权式酒店；住宅区段内不可做独立酒店。我们会在设计前先确认可行性。'),
        ('为什么这里每间客房造价为海岸之最？', '度假村级装修标准、受规范约束的施工物流（出入、时段、指定供应商），以及因泻湖与红树林而生的环保要求。每间客房 120,000 至 320,000 美元。')]},
'vh-corasol': {
 'es': [('¿Villa para vivir o para rentar en Corasol?', 'El entorno favorece vivienda permanente y estancias largas: lotes amplios, golf y beach club. Para renta diaria conviene revisar el reglamento del desarrollo antes de diseñar.'),
        ('¿Recrea supervisa la obra a diario?', 'Sí, nuestra oficina está en Corasol. Eso significa presencia diaria en obra y trato directo con la administración para accesos, horarios y revisión de proyecto.')],
 'en': [('Villa to live in or to rent in Corasol?', 'The setting favours permanent living and long stays: generous lots, golf and a beach club. For daily rental, check the development’s rules before designing.'),
        ('Does Recrea supervise the site daily?', 'Yes — our office is in Corasol. That means daily presence on site and direct dealings with the estate management on access, hours and project review.')],
 'ru': [('Вилла в Корасоле — жить или сдавать?', 'Среда располагает к постоянному проживанию и длительным заездам: просторные участки, гольф и бич-клуб. Для посуточной аренды стоит проверить регламент застройки до проектирования.'),
        ('Recrea контролирует стройку ежедневно?', 'Да, наш офис в Корасоле. Это ежедневное присутствие на площадке и прямое взаимодействие с администрацией по доступу, часам и согласованию проекта.')],
 'de': [('Villa zum Wohnen oder zum Vermieten in Corasol?', 'Das Umfeld begünstigt dauerhaftes Wohnen und Langzeitaufenthalte: große Grundstücke, Golf und Beachclub. Für Kurzzeitvermietung sollte die Anlagensatzung vor dem Entwurf geprüft werden.'),
        ('Überwacht Recrea die Baustelle täglich?', 'Ja — unser Büro liegt in Corasol. Das bedeutet tägliche Präsenz und direkte Abstimmung mit der Verwaltung zu Zufahrt, Zeiten und Projektprüfung.')],
 'fr': [('Villa pour habiter ou pour louer à Corasol ?', 'Le cadre favorise la résidence permanente et les longs séjours : grands terrains, golf et beach club. Pour la location quotidienne, vérifiez le règlement du développement avant de concevoir.'),
        ('Recrea supervise-t-il le chantier quotidiennement ?', 'Oui — notre bureau est à Corasol. Cela signifie une présence quotidienne et un lien direct avec l’administration pour les accès, horaires et la revue de projet.')],
 'zh': [('在 Corasol，别墅适合自住还是出租？', '这里的环境更适合长期居住与长住客：地块宽阔、配有高尔夫与海滩俱乐部。若打算做按天出租，请在设计前先核查社区规约。'),
        ('Recrea 是否每日到场监理？', '是。我们的办公室就在 Corasol，可做到每日到场，并就出入、时段与方案审核与物业管理方直接沟通。')]},
'vh-tulum-country-club': {
 'es': [('¿Se puede operar hospedaje en Tulum Country Club?', 'Depende del uso de suelo del lote y del reglamento del desarrollo. Donde se permite, el formato razonable es boutique pequeño o residencias con servicio; lo confirmamos antes de diseñar.'),
        ('¿Cuánto retrasa SEMA un proyecto aquí?', 'De 3 a 5 meses con expediente bien armado. Por eso diseñamos conforme a la norma desde el anteproyecto y arrancamos el trámite en paralelo: la fecha de apertura la fija el permiso, no la obra.')],
 'en': [('Can you operate lodging at Tulum Country Club?', 'It depends on the lot’s land use and the development’s rules. Where allowed, the sensible format is a small boutique or serviced residences; we confirm it before designing.'),
        ('How much does SEMA delay a project here?', '3 to 5 months with a properly prepared file. That is why we design to the rules from the concept stage and start the process in parallel: the opening date is set by the permit, not by the build.')],
 'ru': [('Можно ли вести размещение в Tulum Country Club?', 'Зависит от назначения земли участка и регламента застройки. Где разрешено, разумный формат — небольшой бутик или резиденции с сервисом; подтверждаем до проектирования.'),
        ('Насколько SEMA задерживает проект здесь?', 'На 3–5 месяцев при грамотно собранном пакете. Поэтому проектируем под норму уже на эскизе и запускаем процедуру параллельно: дату открытия задаёт разрешение, а не стройка.')],
 'de': [('Kann man im Tulum Country Club Beherbergung betreiben?', 'Das hängt von der Nutzungsart des Grundstücks und der Anlagensatzung ab. Wo erlaubt, ist ein kleines Boutiquehotel oder Serviced Residences sinnvoll; wir klären das vor dem Entwurf.'),
        ('Wie stark verzögert die SEMA hier ein Projekt?', 'Um 3 bis 5 Monate bei sauber vorbereiteter Akte. Deshalb planen wir ab dem Entwurf normkonform und starten parallel: Das Eröffnungsdatum bestimmt die Genehmigung, nicht der Bau.')],
 'fr': [('Peut-on exploiter de l’hébergement à Tulum Country Club ?', 'Cela dépend de l’usage du sol du lot et du règlement du développement. Là où c’est permis, le format raisonnable est un petit boutique ou des résidences avec services ; nous le confirmons avant de concevoir.'),
        ('Dans quelle mesure la SEMA retarde-t-elle un projet ici ?', 'De 3 à 5 mois avec un dossier bien préparé. D’où une conception conforme dès l’avant-projet et une procédure lancée en parallèle : c’est le permis qui fixe la date d’ouverture, pas le chantier.')],
 'zh': [('在 Tulum Country Club 可以做住宿经营吗？', '取决于地块的土地用途与社区规约。在允许的情形下，合理形态是小型精品酒店或带服务的住宅；我们会在设计前予以确认。'),
        ('SEMA 在这里会让项目延后多久？', '材料准备充分时为3至5个月。因此我们从方案阶段即按法规设计并同步报批：决定开业日期的是许可，而不是施工。')]},
}

LINKS = {
 'es': {z: [('/construccion-de-casas-%s/' % d['zone'], 'Construcción de casas en %s' % NAMES[z]['es']),
            ('/construccion-de-casas-%s/' % d['parent'], 'Construcción de casas en la ciudad'),
            ('/construccion-comercial-hoteles-riviera-maya/', 'Construcción comercial y hoteles'),
            ('/calculadora/', 'Calculadora de costos')] for z, d in ZONES.items()},
 'en': {z: [('/house-construction-%s/' % d['zone'], 'House construction in %s' % NAMES[z]['en']),
            ('/house-construction-%s/' % d['parent'], 'House construction in the city'),
            ('/commercial-hotel-construction-riviera-maya/', 'Commercial and hotel construction'),
            ('/calculator/', 'Cost calculator')] for z, d in ZONES.items()},
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
    for _z, _d in ZONES.items():
        LINKS[_lang][_z] = [('/%s-%s/' % (_pref, _d['zone']), '%s — %s' % (hub, NAMES[_z][_lang])),
                            perm, ('/%s-%s/' % (_pref, _d['parent']), '%s — %s' % (hub, ml.CITY[_lang][_d['parent']])),
                            (_calc, names[0]), (_blog, names[1])]


def block(z, lang):
    b = il.BLOCK_STR[lang]; c = NAMES[z][lang]
    rows = '\n'.join('<tr><td>%s</td><td>%s USD</td><td>%s</td></tr>' % (r[0], k, r[1])
                     for r, k in zip(ROWS[lang], KEYS[z]))
    lis = '\n'.join('<li>%s</li>' % x for x in b['li'])
    return ('<h2 class="mt-4">%s</h2>\n<p>%s</p>\n'
            '<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark">'
            '<tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>\n%s\n</tbody></table></div>\n'
            '<h3 class="mt-3">%s</h3>\n<ul>\n%s\n</ul>'
            % (b['h'].format(c=c), b['p'], b['th'][0], b['th'][1], b['th'][2], rows, b['h2'], lis))


if __name__ == '__main__':
    for z in ZONES:
        z1.ZAREA[z] = AREAS[z]; z1.ZTEXT[z] = TEXT[z]; z1.ZFAQ[z] = FAQ[z]
    for lang in LINKS:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS[lang])
    for k in ['h1', 'title', 'desc', 'block', 'alert', 'h_cost', 'row', 'h_proc']:
        ml.OVR.setdefault(k, {})
    for z, d in ZONES.items():
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            ml.SLUG[lang][z] = '%s-%s' % (SLUG_PREFIX[lang], BASE_SLUG[z])
            ml.NORM[lang][z] = NORM[z][lang]
            c = NAMES[z][lang]; nm = ml.NUM[z]
            ml.OVR['h1'].setdefault(z, {})[lang] = il.H1[lang].format(c=c)
            ml.OVR['title'].setdefault(z, {})[lang] = il.TITLE[lang].format(c=c)
            ml.OVR['desc'].setdefault(z, {})[lang] = il.DESC[lang].format(c=c)
            ml.OVR['alert'].setdefault(z, {})[lang] = il.ALERT[lang].format(
                c=c, m2=nm['m2'], usd=nm['usd'], key=KEYS[z][2].split(' – ')[0])
            ml.OVR['h_cost'].setdefault(z, {})[lang] = il.H_COST[lang].format(c=c)
            ml.OVR['row'].setdefault(z, {})[lang] = il.ROW[lang]
            ml.OVR['h_proc'].setdefault(z, {})[lang] = il.H_PROC[lang]
            ml.OVR['block'].setdefault(z, {})[lang] = block(z, lang)
    ml.LOCS.extend(ZONES)
    for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
        ch = ml.chrome(lang)
        for z in ZONES:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-54s %6d bytes' % (out + '/', len(html)))
