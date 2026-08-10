#!/usr/bin/env python3
"""Second batch of luxury-zone pages (2026-08-07), 6 languages each.

Researched, existing communities that the site had no page for:
  Ciudad Mayakoba / Mayakoba Country Club (Solidaridad) — master plan + Sergio
    García golf course, distinct from the Mayakoba resort residences we cover
  El Cielo Residencial (Solidaridad) — custom-home lots by Xcalacoco beach
  Selvamar (Solidaridad) — gated jungle eco-community north of downtown PDC
  Playa Mujeres (Isla Mujeres municipality) — golf + marina + beachfront, a
    DIFFERENT permitting authority than Cancún, so it carries its own norm text
  Bahía Soliman (Tulum) — low-density exclusive beachfront villas north of Tulum

Not built on purpose: Grand Coral is the former name of Corasol (already covered).
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
z1 = load('gen-casas-zonas.py', 'z1')
ml = z1.ml

ZONE2 = {
 'ciudad-mayakoba':         dict(parent='playa-del-carmen', f=1.30, perm='2–4'),
 'el-cielo-playa-del-carmen': dict(parent='playa-del-carmen', f=1.15, perm='2–4'),
 'selvamar-playa-del-carmen': dict(parent='playa-del-carmen', f=1.18, perm='2–4'),
 'playa-mujeres':           dict(parent='cancun',           f=1.35, perm='3–5'),
 'bahia-soliman':           dict(parent='tulum',            f=1.25, perm='3–5'),
}

NAMES = {
 'ciudad-mayakoba': {'es': 'Ciudad Mayakoba', 'en': 'Ciudad Mayakoba', 'ru': 'Сьюдад-Майякоба',
                     'de': 'Ciudad Mayakoba', 'fr': 'Ciudad Mayakoba', 'zh': 'Ciudad Mayakoba'},
 'el-cielo-playa-del-carmen': {'es': 'El Cielo, Playa del Carmen', 'en': 'El Cielo, Playa del Carmen',
                     'ru': 'Эль-Сьело, Плая-дель-Кармен', 'de': 'El Cielo, Playa del Carmen',
                     'fr': 'El Cielo, Playa del Carmen', 'zh': 'El Cielo（普拉亚德尔卡门）'},
 'selvamar-playa-del-carmen': {'es': 'Selvamar, Playa del Carmen', 'en': 'Selvamar, Playa del Carmen',
                     'ru': 'Сельвамар, Плая-дель-Кармен', 'de': 'Selvamar, Playa del Carmen',
                     'fr': 'Selvamar, Playa del Carmen', 'zh': 'Selvamar（普拉亚德尔卡门）'},
 'playa-mujeres': {'es': 'Playa Mujeres', 'en': 'Playa Mujeres', 'ru': 'Плая-Мухерес',
                   'de': 'Playa Mujeres', 'fr': 'Playa Mujeres', 'zh': 'Playa Mujeres'},
 'bahia-soliman': {'es': 'Bahía Solimán', 'en': 'Soliman Bay', 'ru': 'Баия-Солиман',
                   'de': 'Bahía Solimán', 'fr': 'Bahía Solimán', 'zh': 'Bahía Solimán（索利曼湾）'},
}
AREAS = {
 'ciudad-mayakoba': {'es': 'Ciudad Mayakoba y las secciones del country club', 'en': 'Ciudad Mayakoba and its country-club sections',
   'ru': 'Сьюдад-Майякобе и секциях кантри-клуба', 'de': 'Ciudad Mayakoba und den Country-Club-Abschnitten',
   'fr': 'Ciudad Mayakoba et ses sections country club', 'zh': 'Ciudad Mayakoba 及其乡村俱乐部区段'},
 'el-cielo-playa-del-carmen': {'es': 'El Cielo Residencial y la zona de Xcalacoco', 'en': 'El Cielo Residencial and the Xcalacoco area',
   'ru': 'Эль-Сьело Ресиденсиаль и районе Шкалакоко', 'de': 'El Cielo Residencial und der Gegend von Xcalacoco',
   'fr': 'El Cielo Residencial et le secteur de Xcalacoco', 'zh': 'El Cielo Residencial 与 Xcalacoco 一带'},
 'selvamar-playa-del-carmen': {'es': 'Selvamar y sus secciones residenciales', 'en': 'Selvamar and its residential sections',
   'ru': 'Сельвамаре и его жилых секциях', 'de': 'Selvamar und seinen Wohnabschnitten',
   'fr': 'Selvamar et ses sections résidentielles', 'zh': 'Selvamar 及其住宅区段'},
 'playa-mujeres': {'es': 'Playa Mujeres y Costa Mujeres', 'en': 'Playa Mujeres and Costa Mujeres',
   'ru': 'Плая-Мухерес и Коста-Мухерес', 'de': 'Playa Mujeres und Costa Mujeres',
   'fr': 'Playa Mujeres et Costa Mujeres', 'zh': 'Playa Mujeres 与 Costa Mujeres'},
 'bahia-soliman': {'es': 'Bahía Solimán, Tankah y la costa al norte de Tulum', 'en': 'Soliman Bay, Tankah and the coast north of Tulum',
   'ru': 'Баия-Солиман, Танках и побережье к северу от Тулума', 'de': 'Bahía Solimán, Tankah und der Küste nördlich von Tulum',
   'fr': 'Bahía Solimán, Tankah et la côte au nord de Tulum', 'zh': 'Bahía Solimán、Tankah 及图卢姆以北海岸'},
}

TEXT = {
'ciudad-mayakoba': {
 'es': 'Ciudad Mayakoba es el plan maestro urbano junto a Mayakoba: lotes residenciales, country club y un campo de golf firmado por Sergio García, con lineamientos de diseño y áreas verdes protegidas dentro del propio desarrollo. Se construye con reglamento del máster plan más licencia municipal de Solidaridad, y el estándar de acabados que pide la zona la coloca claramente arriba del promedio de Playa del Carmen.',
 'en': 'Ciudad Mayakoba is the urban master plan next to Mayakoba: residential lots, a country club and a golf course signed by Sergio García, with design guidelines and protected green areas inside the development itself. You build under the master-plan code plus the Solidaridad municipal licence, and the finish standard the area expects puts it clearly above the Playa del Carmen average.',
 'ru': 'Сьюдад-Майякоба — городской мастер-план рядом с Майякобой: жилые участки, кантри-клуб и поле для гольфа авторства Серхио Гарсии, с дизайн-регламентом и защищёнными зелёными зонами внутри самой застройки. Строят по регламенту мастер-плана плюс муниципальная лицензия Solidaridad, а ожидаемый уровень отделки ставит зону заметно выше среднего по Плая-дель-Кармен.',
 'de': 'Ciudad Mayakoba ist der städtische Masterplan neben Mayakoba: Wohngrundstücke, Country Club und ein von Sergio García gezeichneter Golfplatz, mit Gestaltungsrichtlinien und geschützten Grünflächen innerhalb der Anlage. Gebaut wird nach dem Masterplan-Reglement plus kommunaler Lizenz von Solidaridad; der erwartete Ausbaustandard liegt deutlich über dem Durchschnitt von Playa del Carmen.',
 'fr': 'Ciudad Mayakoba est le plan-masse urbain voisin de Mayakoba : terrains résidentiels, country club et un parcours de golf signé Sergio García, avec des lignes directrices architecturales et des espaces verts protégés au sein même du développement. On construit selon le règlement du plan-masse et le permis municipal de Solidaridad ; le standard de finition attendu place la zone nettement au-dessus de la moyenne de Playa del Carmen.',
 'zh': 'Ciudad Mayakoba 是紧邻 Mayakoba 的城市总体规划区：住宅地块、乡村俱乐部，以及由 Sergio García 设计的高尔夫球场，开发区内设有设计导则与受保护绿地。施工须同时满足总体规划规约与 Solidaridad 市政许可，而该片区所要求的装修标准明显高于普拉亚德尔卡门平均水平。'},
'el-cielo-playa-del-carmen': {
 'es': 'El Cielo Residencial es una comunidad cerrada entre la carretera federal y la playa de Xcalacoco, con lotes para casa a la medida, andadores, ciclovías y ambiente familiar, y con dos campos de golf PGA a pocos minutos. Es la puerta de entrada más accesible al segmento premium de Playa del Carmen: reglamento de construcción del residencial, licencia municipal de Solidaridad y obra sin la logística restringida de un resort.',
 'en': 'El Cielo Residencial is a gated community between the federal highway and Xcalacoco beach, with lots for custom homes, walking and cycling paths and a family atmosphere, and two PGA golf courses minutes away. It is the most accessible entry into Playa del Carmen’s premium segment: the community’s building code, the Solidaridad municipal licence and a build without the restricted logistics of a resort.',
 'ru': 'Эль-Сьело Ресиденсиаль — закрытая община между федеральной трассой и пляжем Шкалакоко: участки под дом по индивидуальному проекту, пешеходные и велодорожки, семейная атмосфера, два поля PGA в нескольких минутах. Это самый доступный вход в премиум-сегмент Плая-дель-Кармен: регламент застройки посёлка, муниципальная лицензия Solidaridad и стройка без жёсткой логистики курорта.',
 'de': 'El Cielo Residencial ist eine geschlossene Anlage zwischen Bundesstraße und dem Strand von Xcalacoco, mit Grundstücken für individuelle Häuser, Fuß- und Radwegen, familiärem Umfeld und zwei PGA-Golfplätzen in wenigen Minuten. Es ist der günstigste Einstieg ins Premiumsegment von Playa del Carmen: Bausatzung der Anlage, kommunale Lizenz von Solidaridad und ein Bau ohne die eingeschränkte Resort-Logistik.',
 'fr': 'El Cielo Residencial est une résidence fermée entre la route fédérale et la plage de Xcalacoco, avec des terrains pour maisons sur mesure, des allées piétonnes et cyclables, une ambiance familiale et deux parcours de golf PGA à quelques minutes. C’est l’entrée la plus accessible au segment premium de Playa del Carmen : règlement de construction de la résidence, permis municipal de Solidaridad et chantier sans la logistique contrainte d’un resort.',
 'zh': 'El Cielo Residencial 是位于联邦公路与 Xcalacoco 海滩之间的封闭社区，提供可自建住宅的地块，配有步道与自行车道，氛围宜居适合家庭，数分钟车程内有两座 PGA 高尔夫球场。它是进入普拉亚德尔卡门高端市场门槛最友好的选择：遵循社区建筑规约与 Solidaridad 市政许可，且无需应对度假村式的受限物流。'},
'selvamar-playa-del-carmen': {
 'es': 'Selvamar es la comunidad cerrada más verde de Playa del Carmen: manzanas rodeadas de selva conservada, andadores, áreas deportivas y una densidad baja pensada para vivir todo el año. Construir aquí exige respetar el porcentaje de vegetación del residencial y coordinar el desmonte mínimo autorizado; a cambio, se obtiene una casa integrada a la selva a diez minutos del centro.',
 'en': 'Selvamar is the greenest gated community in Playa del Carmen: blocks surrounded by preserved jungle, walking paths, sports areas and a low density designed for year-round living. Building here means respecting the community’s vegetation ratio and coordinating the minimum authorised clearing; in exchange you get a house integrated into the jungle ten minutes from downtown.',
 'ru': 'Сельвамар — самая «зелёная» закрытая община Плая-дель-Кармен: кварталы в сохранённой сельве, пешеходные дорожки, спортивные зоны и низкая плотность для круглогодичной жизни. Стройка требует соблюдать долю растительности по регламенту посёлка и согласовать минимальную разрешённую расчистку; взамен вы получаете дом, встроенный в джунгли, в десяти минутах от центра.',
 'de': 'Selvamar ist die grünste geschlossene Anlage von Playa del Carmen: Blöcke inmitten erhaltenen Dschungels, Fußwege, Sportbereiche und eine geringe Dichte für ganzjähriges Wohnen. Bauen heißt hier, den Vegetationsanteil der Anlage einzuhalten und die minimal genehmigte Rodung abzustimmen; dafür entsteht ein Haus, das zehn Minuten vom Zentrum in den Dschungel eingebettet ist.',
 'fr': 'Selvamar est la résidence fermée la plus verte de Playa del Carmen : des îlots entourés de jungle préservée, des allées, des espaces sportifs et une faible densité pensée pour vivre à l’année. Construire ici impose de respecter le taux de végétation de la résidence et de coordonner le défrichement minimal autorisé ; en échange, la maison s’intègre à la jungle à dix minutes du centre.',
 'zh': 'Selvamar 是普拉亚德尔卡门绿化最好的封闭社区：街区被保留的丛林环抱，配有步道与运动场地，密度低，适合全年居住。在此施工需遵守社区的植被保留比例，并就最低限度的清林作业进行报批；换来的是一栋融入丛林、距市中心仅十分钟的住宅。'},
'playa-mujeres': {
 'es': 'Playa Mujeres es el extremo premium al norte de Cancún: campo de golf de firma, marina, playa virgen y residencias de marca. Pertenece al municipio de Isla Mujeres, no a Benito Juárez, así que la licencia se tramita ahí; en predios FONATUR se suma su visto bueno y frente al mar la concesión ZOFEMAT. Sumado al comité de diseño del desarrollo, es la zona con el estándar constructivo más alto de la zona norte.',
 'en': 'Playa Mujeres is the premium end north of Cancún: a signature golf course, a marina, unspoilt beach and branded residences. It belongs to the municipality of Isla Mujeres, not Benito Juárez, so the licence is filed there; FONATUR sign-off is added on their land and a ZOFEMAT concession on beachfront lots. With the development’s design committee on top, it is the highest construction standard in the northern zone.',
 'ru': 'Плая-Мухерес — премиальный край к северу от Канкуна: авторское поле для гольфа, марина, нетронутый пляж и брендовые резиденции. Территория относится к муниципалитету Isla Mujeres, а не Benito Juárez, поэтому лицензия оформляется там; на землях FONATUR добавляется их согласование, а на первой линии — концессия ZOFEMAT. Вместе с комитетом по дизайну застройки это самый высокий строительный стандарт севера региона.',
 'de': 'Playa Mujeres ist das Premiumende nördlich von Cancún: Signature-Golfplatz, Marina, unverbauter Strand und Markenresidenzen. Es gehört zur Gemeinde Isla Mujeres, nicht zu Benito Juárez, die Lizenz läuft also dort; auf FONATUR-Land kommt deren Freigabe hinzu, am Strand die ZOFEMAT-Konzession. Zusammen mit dem Gestaltungsbeirat der Anlage gilt hier der höchste Baustandard des Nordens.',
 'fr': 'Playa Mujeres est l’extrémité premium au nord de Cancún : golf signature, marina, plage préservée et résidences de marque. La zone dépend de la commune d’Isla Mujeres, et non de Benito Juárez : le permis s’y dépose ; sur terrain FONATUR s’ajoute leur accord, et en front de mer la concession ZOFEMAT. Avec le comité d’architecture du développement, c’est le standard de construction le plus élevé du nord.',
 'zh': 'Playa Mujeres 是坎昆以北的高端尽头：名家设计高尔夫球场、码头、未开发海滩与品牌住宅。该区隶属 Isla Mujeres 市而非 Benito Juárez，许可须在该市办理；位于 FONATUR 土地的还需其批准，海滨地块另需 ZOFEMAT 特许。再加上开发区设计委员会的审核，这里的施工标准为北部之最。'},
'bahia-soliman': {
 'es': 'Bahía Solimán es el enclave de villas frente al mar entre Akumal y Tulum: baja densidad, lotes grandes, arrecife protegido y casi nada de infraestructura pública, así que muchos proyectos se resuelven con pozo, cisterna, planta de tratamiento y solar. Municipio Tulum, con SEMA en la mayoría de los predios y ZOFEMAT en frente de playa; la logística de obra es más larga y eso se ve en el costo por m².',
 'en': 'Soliman Bay is the beachfront villa enclave between Akumal and Tulum: low density, large lots, a protected reef and almost no public infrastructure, so many projects are solved with a well, cistern, treatment plant and solar. Tulum municipality, with SEMA on most lots and ZOFEMAT on the beachfront; construction logistics run longer and that shows in the cost per m².',
 'ru': 'Баия-Солиман — анклав вилл на первой линии между Акумалем и Тулумом: низкая плотность, большие участки, охраняемый риф и почти полное отсутствие городской инфраструктуры, поэтому многие проекты решаются скважиной, цистерной, очистными и солнечной генерацией. Муниципалитет Тулум, SEMA на большинстве участков и ZOFEMAT на берегу; логистика стройки длиннее, и это видно в цене за м².',
 'de': 'Bahía Solimán ist die Strandvillen-Enklave zwischen Akumal und Tulum: geringe Dichte, große Grundstücke, geschütztes Riff und kaum öffentliche Infrastruktur — viele Projekte werden mit Brunnen, Zisterne, Kläranlage und Solar gelöst. Gemeinde Tulum, SEMA auf den meisten Grundstücken und ZOFEMAT am Strand; die Baulogistik dauert länger, was sich im m²-Preis zeigt.',
 'fr': 'Bahía Solimán est l’enclave de villas en bord de mer entre Akumal et Tulum : faible densité, grands terrains, récif protégé et quasi aucune infrastructure publique — beaucoup de projets se règlent avec puits, citerne, station de traitement et solaire. Commune de Tulum, SEMA sur la plupart des lots et ZOFEMAT en front de mer ; la logistique de chantier est plus longue, ce qui se voit au coût du m².',
 'zh': 'Bahía Solimán 是位于 Akumal 与图卢姆之间的海滨别墅聚落：密度低、地块大、珊瑚礁受保护，且几乎没有市政基础设施，因此许多项目依靠水井、蓄水池、污水处理设备与太阳能自给。属图卢姆市辖，多数地块需 SEMA 许可，海滨地块需 ZOFEMAT；施工物流周期更长，这一点会反映在每平方米造价上。'},
}

FAQ2 = {
'ciudad-mayakoba': {
 'es': [('¿Es lo mismo Ciudad Mayakoba que Mayakoba?', 'No. Mayakoba es el complejo de resorts y residencias privadas; Ciudad Mayakoba es el plan maestro urbano vecino, con lotes residenciales, country club y campo de golf propio. Construimos en ambos, pero el trámite y el reglamento son distintos.'),
        ('¿Qué se necesita para construir en Ciudad Mayakoba?', 'Aprobación del reglamento del máster plan (volumetría, materiales, áreas verdes) y licencia municipal de Solidaridad con DRO. Presentamos ambos expedientes en paralelo.')],
 'en': [('Is Ciudad Mayakoba the same as Mayakoba?', 'No. Mayakoba is the resort and private residence complex; Ciudad Mayakoba is the neighbouring urban master plan with residential lots, a country club and its own golf course. We build in both, but the code and the process differ.'),
        ('What is needed to build in Ciudad Mayakoba?', 'Approval under the master-plan code (massing, materials, green areas) and the Solidaridad municipal licence with a DRO. We file both in parallel.')],
 'ru': [('Сьюдад-Майякоба и Майякоба — это одно и то же?', 'Нет. Майякоба — комплекс курортов и частных резиденций; Сьюдад-Майякоба — соседний городской мастер-план с жилыми участками, кантри-клубом и собственным полем для гольфа. Строим и там, и там, но регламент и процедура разные.'),
        ('Что нужно для стройки в Сьюдад-Майякобе?', 'Согласование по регламенту мастер-плана (объём, материалы, зелёные зоны) и муниципальная лицензия Solidaridad с DRO. Ведём оба пакета параллельно.')],
 'de': [('Ist Ciudad Mayakoba dasselbe wie Mayakoba?', 'Nein. Mayakoba ist die Resort- und Privatresidenz-Anlage; Ciudad Mayakoba ist der benachbarte urbane Masterplan mit Wohngrundstücken, Country Club und eigenem Golfplatz. Wir bauen in beiden, Reglement und Verfahren unterscheiden sich aber.'),
        ('Was braucht man zum Bauen in Ciudad Mayakoba?', 'Freigabe nach dem Masterplan-Reglement (Baukörper, Materialien, Grünflächen) und die kommunale Lizenz von Solidaridad mit DRO. Wir reichen beides parallel ein.')],
 'fr': [('Ciudad Mayakoba, est-ce la même chose que Mayakoba ?', 'Non. Mayakoba est le complexe de resorts et de résidences privées ; Ciudad Mayakoba est le plan-masse urbain voisin, avec terrains résidentiels, country club et son propre golf. Nous construisons dans les deux, mais le règlement et la procédure diffèrent.'),
        ('Que faut-il pour construire à Ciudad Mayakoba ?', 'L’accord au titre du règlement du plan-masse (volumétrie, matériaux, espaces verts) et le permis municipal de Solidaridad avec DRO. Nous déposons les deux en parallèle.')],
 'zh': [('Ciudad Mayakoba 和 Mayakoba 是同一个地方吗？', '不是。Mayakoba 是度假村与私人住宅综合体；Ciudad Mayakoba 是与之相邻的城市总体规划区，拥有住宅地块、乡村俱乐部及自有高尔夫球场。两地我们都承建，但规约与流程不同。'),
        ('在 Ciudad Mayakoba 建房需要什么？', '总体规划规约的审批（体量、材料、绿地）以及带 DRO 的 Solidaridad 市政许可。两套材料我们并行报审。')]},
'el-cielo-playa-del-carmen': {
 'es': [('¿Cuánto cuesta construir en El Cielo?', 'De $13,800 a $28,700 MXN por m² según acabados. Es de las entradas más accesibles al segmento cerrado de Playa del Carmen sin renunciar a amenidades ni seguridad.'),
        ('¿El residencial tiene reglamento de construcción?', 'Sí: alturas, retiros, imagen de fachada, horarios de obra y manejo de material. Presentamos el proyecto al residencial y en paralelo tramitamos la licencia municipal con DRO.')],
 'en': [('How much does it cost to build in El Cielo?', 'From $13,800 to $28,700 MXN per m² depending on finishes. It is one of the most accessible entries into Playa del Carmen’s gated segment without giving up amenities or security.'),
        ('Does the community have a building code?', 'Yes: heights, setbacks, façade image, working hours and material handling. We present the project to the community and file the municipal licence with a DRO in parallel.')],
 'ru': [('Сколько стоит стройка в Эль-Сьело?', 'От $13,800 до $28,700 MXN за м² в зависимости от отделки. Один из самых доступных входов в закрытый сегмент Плая-дель-Кармен без потери инфраструктуры и охраны.'),
        ('Есть ли у посёлка строительный регламент?', 'Да: высоты, отступы, облик фасада, часы работ и обращение с материалами. Подаём проект в посёлок и параллельно оформляем муниципальную лицензию с DRO.')],
 'de': [('Was kostet Bauen in El Cielo?', 'Von $13.800 bis $28.700 MXN pro m² je nach Ausbau. Einer der günstigsten Einstiege ins geschlossene Segment von Playa del Carmen, ohne auf Ausstattung und Sicherheit zu verzichten.'),
        ('Hat die Anlage eine Bausatzung?', 'Ja: Höhen, Abstände, Fassadenbild, Bauzeiten und Materialhandling. Wir legen das Projekt der Anlage vor und beantragen parallel die kommunale Lizenz mit DRO.')],
 'fr': [('Combien coûte la construction à El Cielo ?', 'De 13 800 à 28 700 MXN le m² selon les finitions. C’est l’une des entrées les plus accessibles au segment fermé de Playa del Carmen, sans renoncer aux équipements ni à la sécurité.'),
        ('La résidence a-t-elle un règlement de construction ?', 'Oui : hauteurs, reculs, image de façade, horaires de chantier et gestion des matériaux. Nous présentons le projet à la résidence et déposons en parallèle le permis municipal avec DRO.')],
 'zh': [('在 El Cielo 建房要多少钱？', '按装修标准，每平方米 13,800 至 28,700 比索。这是进入普拉亚德尔卡门封闭社区市场门槛较低的选择之一，同时不牺牲配套与安保。'),
        ('社区是否有建筑规约？', '有：高度、退线、立面风貌、施工时段与材料进出管理。我们向社区报审方案，同时并行办理带 DRO 的市政许可。')]},
'selvamar-playa-del-carmen': {
 'es': [('¿Puedo desmontar el lote en Selvamar?', 'Solo lo autorizado. El residencial fija un porcentaje mínimo de vegetación conservada y el desmonte se gestiona con la autoridad correspondiente; diseñamos la casa alrededor de los árboles que deben quedarse.'),
        ('¿Qué tipo de casa funciona mejor aquí?', 'Volumen compacto, ventilación cruzada, orientación para sombra y acabados de bajo mantenimiento. La selva alrededor es una ventaja de confort si el diseño la aprovecha, y un problema de humedad si no.')],
 'en': [('Can I clear the lot in Selvamar?', 'Only what is authorised. The community sets a minimum ratio of preserved vegetation and clearing is processed with the relevant authority; we design the house around the trees that have to stay.'),
        ('What kind of house works best here?', 'A compact volume, cross ventilation, orientation for shade and low-maintenance finishes. The surrounding jungle is a comfort advantage if the design uses it — and a damp problem if it does not.')],
 'ru': [('Можно ли расчистить участок в Сельвамаре?', 'Только в разрешённом объёме. Посёлок задаёт минимальную долю сохраняемой растительности, а расчистка согласуется с профильным органом; мы проектируем дом вокруг деревьев, которые должны остаться.'),
        ('Какой дом здесь работает лучше?', 'Компактный объём, сквозная вентиляция, ориентация под тень и отделка с низким обслуживанием. Окружающая сельва — плюс к комфорту, если проект её использует, и источник сырости, если нет.')],
 'de': [('Darf ich das Grundstück in Selvamar roden?', 'Nur im genehmigten Umfang. Die Anlage schreibt einen Mindestanteil erhaltener Vegetation vor, die Rodung wird mit der zuständigen Behörde abgestimmt; wir planen das Haus um die Bäume herum, die bleiben müssen.'),
        ('Welches Haus funktioniert hier am besten?', 'Kompakter Baukörper, Querlüftung, Ausrichtung nach Schatten und wartungsarme Oberflächen. Der Dschungel ringsum ist ein Komfortvorteil, wenn der Entwurf ihn nutzt — und ein Feuchteproblem, wenn nicht.')],
 'fr': [('Puis-je défricher le terrain à Selvamar ?', 'Uniquement ce qui est autorisé. La résidence impose un pourcentage minimal de végétation conservée et le défrichement se traite avec l’autorité compétente ; nous concevons la maison autour des arbres qui doivent rester.'),
        ('Quel type de maison fonctionne le mieux ici ?', 'Un volume compact, une ventilation traversante, une orientation pour l’ombre et des finitions à faible entretien. La jungle alentour est un atout de confort si le projet l’exploite, et un problème d’humidité sinon.')],
 'zh': [('在 Selvamar 可以清林吗？', '只能在批准范围内。社区规定了最低植被保留比例，清林须向主管部门报批；我们会围绕必须保留的树木来布置住宅。'),
        ('这里适合建什么样的房子？', '体量紧凑、穿堂通风、朝向利于遮阴、饰面易维护。周边丛林若被设计善加利用是舒适度加分项，反之则会带来潮湿问题。')]},
'playa-mujeres': {
 'es': [('¿Qué municipio otorga la licencia en Playa Mujeres?', 'Isla Mujeres, no Cancún. El expediente se presenta ahí con DRO, y se suman el visto bueno de FONATUR en sus predios y la concesión ZOFEMAT si el lote es frente al mar.'),
        ('¿Cuánto cuesta construir en Playa Mujeres?', 'De $15,500 a $32,400 MXN por m². El estándar de la zona, la especificación anticorrosiva frente al mar y la logística de acceso explican el nivel de precio.')],
 'en': [('Which municipality issues the licence in Playa Mujeres?', 'Isla Mujeres, not Cancún. The file is submitted there with a DRO, plus FONATUR sign-off on their land and a ZOFEMAT concession if the lot is beachfront.'),
        ('How much does it cost to build in Playa Mujeres?', 'From $15,500 to $32,400 MXN per m². The area’s standard, the beachfront anti-corrosion spec and access logistics explain the price level.')],
 'ru': [('Какой муниципалитет выдаёт лицензию в Плая-Мухерес?', 'Isla Mujeres, а не Канкун. Пакет подаётся туда, с DRO; добавляются согласование FONATUR на его землях и концессия ZOFEMAT, если участок на первой линии.'),
        ('Сколько стоит стройка в Плая-Мухерес?', 'От $15,500 до $32,400 MXN за м². Уровень цен объясняют стандарт зоны, антикоррозийная спецификация у моря и логистика доступа.')],
 'de': [('Welche Gemeinde erteilt die Lizenz in Playa Mujeres?', 'Isla Mujeres, nicht Cancún. Der Antrag wird dort mit DRO eingereicht, dazu die FONATUR-Freigabe auf deren Land und eine ZOFEMAT-Konzession bei Strandlage.'),
        ('Was kostet Bauen in Playa Mujeres?', 'Von $15.500 bis $32.400 MXN pro m². Der Standard der Zone, die Korrosionsschutzspezifikation am Meer und die Zufahrtslogistik erklären das Preisniveau.')],
 'fr': [('Quelle commune délivre le permis à Playa Mujeres ?', 'Isla Mujeres, et non Cancún. Le dossier y est déposé avec un DRO, auquel s’ajoutent l’accord FONATUR sur ses terrains et la concession ZOFEMAT en front de mer.'),
        ('Combien coûte la construction à Playa Mujeres ?', 'De 15 500 à 32 400 MXN le m². Le standard du secteur, la spécification anticorrosion en bord de mer et la logistique d’accès expliquent ce niveau de prix.')],
 'zh': [('Playa Mujeres 由哪个市政发放许可？', '是 Isla Mujeres 市，而非坎昆。材料在该市报审并需 DRO 签署；位于 FONATUR 土地的还需其批准，海滨地块需 ZOFEMAT 特许。'),
        ('在 Playa Mujeres 建房要多少钱？', '每平方米 15,500 至 32,400 比索。片区标准、海滨防腐做法与进出物流共同决定了这一价格水平。')]},
'bahia-soliman': {
 'es': [('¿Hay servicios públicos en Bahía Solimán?', 'Muy limitados. La mayoría de las casas resuelve agua con pozo y cisterna, drenaje con planta de tratamiento o biodigestor y energía con solar más respaldo. Lo dimensionamos desde el anteproyecto, no al final.'),
        ('¿Qué permisos aplican frente a la bahía?', 'Licencia municipal de Tulum con DRO, autorización ambiental de SEMA en la mayoría de los predios y concesión ZOFEMAT en frente de playa, con cuidado extra por el arrecife protegido.')],
 'en': [('Are there public utilities in Soliman Bay?', 'Very limited. Most houses solve water with a well and cistern, drainage with a treatment plant or biodigester, and power with solar plus backup. We size all of that at concept stage, not at the end.'),
        ('Which permits apply on the bay?', 'The Tulum municipal licence with a DRO, SEMA environmental authorisation on most lots and a ZOFEMAT concession on the beachfront, with extra care because of the protected reef.')],
 'ru': [('Есть ли в Баия-Солиман городские коммуникации?', 'Очень ограниченно. Большинство домов решает воду скважиной и цистерной, канализацию — очистными или биодигестером, электричество — солнечной станцией с резервом. Мы считаем это на стадии эскиза, а не в конце.'),
        ('Какие разрешения нужны у бухты?', 'Муниципальная лицензия Тулума с DRO, экологическое разрешение SEMA на большинстве участков и концессия ZOFEMAT на берегу, с повышенным вниманием к охраняемому рифу.')],
 'de': [('Gibt es öffentliche Versorgung in Bahía Solimán?', 'Sehr eingeschränkt. Die meisten Häuser lösen Wasser über Brunnen und Zisterne, Abwasser über Kläranlage oder Biodigester und Strom über Solar mit Backup. Wir dimensionieren das im Entwurf, nicht am Ende.'),
        ('Welche Genehmigungen gelten an der Bucht?', 'Kommunale Lizenz von Tulum mit DRO, SEMA-Umweltgenehmigung auf den meisten Grundstücken und ZOFEMAT-Konzession am Strand — mit besonderer Sorgfalt wegen des geschützten Riffs.')],
 'fr': [('Y a-t-il des réseaux publics à Bahía Solimán ?', 'Très peu. La plupart des maisons règlent l’eau par puits et citerne, l’assainissement par station de traitement ou biodigesteur, et l’électricité par solaire avec secours. Nous dimensionnons tout cela dès l’avant-projet.'),
        ('Quels permis s’appliquent sur la baie ?', 'Le permis municipal de Tulum avec DRO, l’autorisation environnementale SEMA sur la plupart des lots et la concession ZOFEMAT en front de plage, avec une vigilance accrue liée au récif protégé.')],
 'zh': [('Bahía Solimán 有市政配套吗？', '非常有限。多数住宅通过水井与蓄水池解决供水、以污水处理设备或生物消化池解决排水、以太阳能加备用电源解决用电。这些我们在方案阶段就完成选型，而非收尾时才考虑。'),
        ('海湾一带需要哪些许可？', '带 DRO 的图卢姆市政许可、多数地块所需的 SEMA 环保许可，以及海滨地块的 ZOFEMAT 特许；因珊瑚礁受保护，审查也更为严格。')]},
}

# Playa Mujeres sits in a different municipality than its price parent (Cancún)
ZNORM_OVERRIDE = {
 'playa-mujeres': {
 'es': 'Playa Mujeres está en el municipio de Isla Mujeres, en su porción continental al norte de Cancún: ahí se tramitan la constancia de uso de suelo y la licencia de construcción, con proyecto firmado por DRO. En predios de origen FONATUR se suma su visto bueno con revisión de imagen urbana y densidad, y en lotes frente al mar la concesión ZOFEMAT. A eso se añade el comité de diseño del desarrollo, que revisa alturas, materiales y fachadas antes de que el expediente entre al municipio.',
 'en': 'Playa Mujeres sits in the municipality of Isla Mujeres, on its mainland strip north of Cancún: that is where the land-use certificate and the building licence are processed, with drawings signed by a DRO. On FONATUR-origin land their sign-off is added, with urban-image and density review, and beachfront lots require a ZOFEMAT concession. On top of that the development’s design committee reviews heights, materials and façades before the file reaches the municipality.',
 'ru': 'Плая-Мухерес относится к муниципалитету Isla Mujeres — его континентальной части к северу от Канкуна: именно там оформляются справка о назначении земли и разрешение на строительство с проектом за подписью DRO. На землях происхождения FONATUR добавляется их согласование с проверкой городского облика и плотности, а на участках у моря — концессия ZOFEMAT. Сверх этого комитет по дизайну застройки проверяет высоты, материалы и фасады до подачи в муниципалитет.',
 'de': 'Playa Mujeres liegt in der Gemeinde Isla Mujeres, auf deren Festlandstreifen nördlich von Cancún: Dort werden Nutzungsbescheinigung und Baugenehmigung mit DRO-unterzeichneten Plänen bearbeitet. Auf Flächen mit FONATUR-Ursprung kommt deren Freigabe samt Prüfung von Stadtbild und Dichte hinzu, bei Strandgrundstücken die ZOFEMAT-Konzession. Zusätzlich prüft der Gestaltungsbeirat der Anlage Höhen, Materialien und Fassaden, bevor der Antrag zur Gemeinde geht.',
 'fr': 'Playa Mujeres se trouve dans la commune d’Isla Mujeres, sur sa partie continentale au nord de Cancún : c’est là que se traitent le certificat d’usage du sol et le permis de construire, avec des plans signés par un DRO. Sur les terrains d’origine FONATUR s’ajoute leur accord, avec examen de l’image urbaine et de la densité, et les lots en front de mer exigent une concession ZOFEMAT. S’y ajoute le comité d’architecture du développement, qui examine hauteurs, matériaux et façades avant le dépôt en mairie.',
 'zh': 'Playa Mujeres 位于 Isla Mujeres 市在坎昆以北的大陆部分：土地用途证明与施工许可均在该市办理，图纸须由 DRO 签署。属 FONATUR 来源的地块还需其批准，并审查城市风貌与容积密度；海滨地块需 ZOFEMAT 特许。此外，开发区设计委员会会在材料递交市政之前，先行审核高度、材料与立面。'},
}

LINKS2 = {
 'es': {'ciudad-mayakoba': [('/construccion-de-casas-mayakoba/','Construcción de casas en Mayakoba'), ('/villas-de-lujo-mayakoba/','Villas de lujo en Mayakoba'), ('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/calculadora/','Calculadora de costos')],
        'el-cielo-playa-del-carmen': [('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/villas-de-lujo-playa-del-carmen/','Villas de lujo en Playa del Carmen'), ('/permisos-de-construccion-playa-del-carmen/','Permisos de construcción'), ('/calculadora/','Calculadora de costos')],
        'selvamar-playa-del-carmen': [('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/permisos-de-construccion-playa-del-carmen/','Permisos de construcción'), ('/blog-es/construccion-sustentable-tulum.html','Construcción sustentable'), ('/calculadora/','Calculadora de costos')],
        'playa-mujeres': [('/construccion-de-casas-cancun/','Construcción de casas en Cancún'), ('/villas-de-lujo-zona-hotelera-cancun/','Villas de lujo en la Zona Hotelera'), ('/construccion-de-casas-puerto-cancun/','Construcción de casas en Puerto Cancún'), ('/calculadora/','Calculadora de costos')],
        'bahia-soliman': [('/construccion-de-casas-akumal/','Construcción de casas en Akumal'), ('/construccion-de-casas-tulum/','Construcción de casas en Tulum'), ('/villas-de-lujo-akumal/','Villas de lujo en Akumal'), ('/calculadora/','Calculadora de costos')]},
 'en': {'ciudad-mayakoba': [('/house-construction-mayakoba/','House construction in Mayakoba'), ('/luxury-villas-mayakoba/','Luxury villas in Mayakoba'), ('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/calculator/','Cost calculator')],
        'el-cielo-playa-del-carmen': [('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/luxury-villa-construction-playa-del-carmen/','Luxury villas in Playa del Carmen'), ('/construction-permits-playa-del-carmen/','Construction permits'), ('/calculator/','Cost calculator')],
        'selvamar-playa-del-carmen': [('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/construction-permits-playa-del-carmen/','Construction permits'), ('/prefab-modular-homes-riviera-maya/','Prefab and modular homes'), ('/calculator/','Cost calculator')],
        'playa-mujeres': [('/house-construction-cancun/','House construction in Cancún'), ('/luxury-villas-hotel-zone-cancun/','Luxury villas in the Hotel Zone'), ('/house-construction-puerto-cancun/','House construction in Puerto Cancún'), ('/calculator/','Cost calculator')],
        'bahia-soliman': [('/house-construction-akumal/','House construction in Akumal'), ('/house-construction-tulum/','House construction in Tulum'), ('/luxury-villas-akumal/','Luxury villas in Akumal'), ('/calculator/','Cost calculator')]},
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
    calcname = {'ru': 'Калькулятор стоимости', 'de': 'Kostenrechner', 'fr': 'Calculateur de coûts', 'zh': '造价计算器'}[_lang]
    blogname = {'ru': 'Гиды по строительству', 'de': 'Bau-Leitfäden', 'fr': 'Guides de construction', 'zh': '建筑指南'}[_lang]
    LINKS2[_lang] = {}
    for _z, _d in ZONE2.items():
        LINKS2[_lang][_z] = [
            ('/%s-%s/' % (_pref, _d['parent']), '%s — %s' % (hub, ml.CITY[_lang][_d['parent']])),
            perm,
            ('/%s-riviera-maya/' % _pref, '%s — %s' % (hub, ml.CITY[_lang]['riviera-maya'])),
            (_calc, calcname), (_blog, blogname)]


def _set_parent_urls(locs):
    P = {'es':'construccion-de-casas','en':'house-construction','ru':'stroitelstvo-domov','de':'hausbau','fr':'construction-de-maisons','zh':'zhuzhai-jianzao'}
    ml.OVR.setdefault('parent_url', {})
    for zk, d in locs.items():
        for l in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            ml.OVR['parent_url'].setdefault(zk, {})[l] = '/%s-%s/' % (P[l], d['parent'])


# appended 2026-08-09: distinguish the house page from Corasol and the Mayakoba resort
_CM = {'es': ' Conviene no confundirlo con dos vecinos: Mayakoba es el complejo de resorts y residencias privadas, y Corasol es la comunidad de golf con beach club propio. Ciudad Mayakoba es plan maestro urbano —lotes unifamiliares, multifamiliares y uso mixto alrededor de un country club—, y por eso admite programas que en los otros dos no caben.', 'en': ' It should not be confused with two neighbours: Mayakoba is the resort and private residence complex, and Corasol is the golf community with its own beach club. Ciudad Mayakoba is an urban master plan — single-family, multi-family and mixed-use lots around a country club — which is why it allows programmes the other two cannot host.', 'ru': ' Важно не путать с двумя соседями: Майякоба — комплекс курортов и частных резиденций, Корасоль — гольф-комьюнити со своим бич-клубом. Сьюдад-Майякоба — городской мастер-план с участками под индивидуальные дома, многоквартирные и смешанные проекты вокруг кантри-клуба, поэтому здесь возможны программы, которые в тех двух не помещаются.', 'de': ' Nicht zu verwechseln mit zwei Nachbarn: Mayakoba ist die Resort- und Privatresidenz-Anlage, Corasol die Golf-Community mit eigenem Beachclub. Ciudad Mayakoba ist ein urbaner Masterplan — Einfamilien-, Mehrfamilien- und Mischnutzungsgrundstücke rund um einen Country Club — und lässt deshalb Programme zu, die in den beiden anderen keinen Platz haben.', 'fr': ' À ne pas confondre avec deux voisins : Mayakoba est le complexe de resorts et de résidences privées, et Corasol la communauté de golf avec son propre beach club. Ciudad Mayakoba est un plan-masse urbain — lots individuels, collectifs et mixtes autour d’un country club — d’où des programmes que les deux autres ne peuvent accueillir.', 'zh': ' 需与两个近邻区分开：Mayakoba 是度假村与私人住宅综合体，Corasol 是拥有自有海滩俱乐部的高尔夫社区。Ciudad Mayakoba 则是城市总体规划区——围绕乡村俱乐部布置独栋、多户与混合用途地块——因此可容纳前两者无法承载的开发内容。'}
for _l, _x in _CM.items():
    TEXT['ciudad-mayakoba'][_l] = TEXT['ciudad-mayakoba'][_l] + _x

if __name__ == '__main__':
    _set_parent_urls(ZONE2)
    # z1.register reads these module-level dicts
    for z in ZONE2:
        z1.ZAREA[z] = AREAS[z]
        z1.ZTEXT[z] = TEXT[z]
        z1.ZFAQ[z] = FAQ2[z]
    for lang in LINKS2:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS2[lang])
    for z, d in ZONE2.items():
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
        if z in ZNORM_OVERRIDE:
            for lang, txt in ZNORM_OVERRIDE[z].items():
                ml.NORM[lang][z] = txt
    ml.LOCS.extend(ZONE2)
    for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
        ch = ml.chrome(lang)
        for z in ZONE2:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-48s %6d bytes' % (out + '/', len(html)))
