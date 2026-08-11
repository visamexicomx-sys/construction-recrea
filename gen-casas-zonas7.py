#!/usr/bin/env python3
"""Seventh zone batch (2026-08-11): the premium gaps in Playa del Carmen and Puerto Morelos.

Verified before writing: Zazil-Ha / Coco Beach is among the three most expensive
areas of Playa del Carmen (alongside Playacar Phase II and Xcalacoco, both already
covered); Playa Magna is a consolidated gated residential area with strong rental
demand; Playa del Secreto is the exclusive beachfront enclave between Puerto Morelos
and Playa del Carmen; the Ruta de los Cenotes is the inland jungle corridor of Puerto
Morelos where land is cheap and there are no networks at all.

The two Puerto Morelos zones carry their own municipal text — Puerto Morelos has been
its own municipality since 2016 and the reef national park drives its rules — and they
are deliberately written to contrast with each other: beachfront ZOFEMAT versus inland
aquifer protection.
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
z1 = load('gen-casas-zonas.py', 'z1')
ml = z1.ml
LANGS = ['es', 'en', 'ru', 'de', 'fr', 'zh']

ZONE7 = {
 'zazil-ha-coco-beach': dict(parent='playa-del-carmen', f=1.35, perm='2–4'),
 'playa-magna':         dict(parent='playa-del-carmen', f=1.22, perm='2–4'),
 'playa-del-secreto':   dict(parent='playa-del-carmen', f=1.35, perm='3–5'),
 'ruta-de-los-cenotes': dict(parent='playa-del-carmen', f=1.05, perm='3–5'),
}

NAMES = {
 'zazil-ha-coco-beach': {'es': 'Zazil-Ha y Coco Beach', 'en': 'Zazil-Ha and Coco Beach',
   'ru': 'Сасиль-Ха и Коко-Бич', 'de': 'Zazil-Ha und Coco Beach',
   'fr': 'Zazil-Ha et Coco Beach', 'zh': 'Zazil-Ha 与 Coco Beach'},
 'playa-magna': {'es': 'Playa Magna', 'en': 'Playa Magna', 'ru': 'Плая-Магна',
   'de': 'Playa Magna', 'fr': 'Playa Magna', 'zh': 'Playa Magna'},
 'playa-del-secreto': {'es': 'Playa del Secreto', 'en': 'Playa del Secreto', 'ru': 'Плая-дель-Секрето',
   'de': 'Playa del Secreto', 'fr': 'Playa del Secreto', 'zh': 'Playa del Secreto'},
 'ruta-de-los-cenotes': {'es': 'la Ruta de los Cenotes', 'en': 'the Ruta de los Cenotes',
   'ru': 'Руте сенотов', 'de': 'der Ruta de los Cenotes', 'fr': 'la Ruta de los Cenotes', 'zh': '天然井之路（Ruta de los Cenotes）'},
}
AREAS = {
 'zazil-ha-coco-beach': {'es': 'Zazil-Ha, Coco Beach y el frente de playa al norte del centro',
   'en': 'Zazil-Ha, Coco Beach and the beachfront north of downtown',
   'ru': 'Сасиль-Ха, Коко-Бич и первой линии к северу от центра',
   'de': 'Zazil-Ha, Coco Beach und der Strandlage nördlich des Zentrums',
   'fr': 'Zazil-Ha, Coco Beach et le front de mer au nord du centre',
   'zh': 'Zazil-Ha、Coco Beach 与市中心以北的海滨地带'},
 'playa-magna': {'es': 'Playa Magna y sus secciones residenciales', 'en': 'Playa Magna and its residential sections',
   'ru': 'Плая-Магне и её жилых секциях', 'de': 'Playa Magna und seinen Wohnabschnitten',
   'fr': 'Playa Magna et ses sections résidentielles', 'zh': 'Playa Magna 及其住宅区段'},
 'playa-del-secreto': {'es': 'Playa del Secreto y la costa entre Puerto Morelos y Playa del Carmen',
   'en': 'Playa del Secreto and the coast between Puerto Morelos and Playa del Carmen',
   'ru': 'Плая-дель-Секрето и побережье между Пуэрто-Морелосом и Плая-дель-Кармен',
   'de': 'Playa del Secreto und der Küste zwischen Puerto Morelos und Playa del Carmen',
   'fr': 'Playa del Secreto et la côte entre Puerto Morelos et Playa del Carmen',
   'zh': 'Playa del Secreto 及 Puerto Morelos 与普拉亚德尔卡门之间的海岸'},
 'ruta-de-los-cenotes': {'es': 'la Ruta de los Cenotes y la selva de Puerto Morelos',
   'en': 'the Ruta de los Cenotes and the Puerto Morelos jungle',
   'ru': 'Руте сенотов и сельве Пуэрто-Морелоса',
   'de': 'der Ruta de los Cenotes und dem Dschungel von Puerto Morelos',
   'fr': 'la Ruta de los Cenotes et la jungle de Puerto Morelos',
   'zh': '天然井之路与 Puerto Morelos 丛林地带'},
}

TEXT = {
'zazil-ha-coco-beach': {
 'es': 'Zazil-Ha y Coco Beach forman el frente de playa al norte del centro y están, junto con Playacar Fase II y Xcalacoco, entre las direcciones más caras de Playa del Carmen. Aquí se paga por caminar a la playa y seguir a diez minutos de la Quinta Avenida. Es zona urbana consolidada: quedan pocos lotes y mucha obra es sustitución o remodelación integral, con predios de playa que suman concesión ZOFEMAT y especificación marina completa.',
 'en': 'Zazil-Ha and Coco Beach make up the beachfront north of downtown and rank, alongside Playacar Phase II and Xcalacoco, among the most expensive addresses in Playa del Carmen. What you pay for here is walking to the beach and still being ten minutes from Quinta Avenida. It is a consolidated urban area: few lots remain and much of the work is replacement or full renovation, with beach lots adding a ZOFEMAT concession and a full marine spec.',
 'ru': 'Сасиль-Ха и Коко-Бич — первая линия к северу от центра и, вместе с Playacar Fase II и Шкалакоко, одни из самых дорогих адресов Плая-дель-Кармен. Здесь платят за возможность дойти до пляжа пешком и при этом быть в десяти минутах от Пятой авеню. Район сложившийся: свободных участков мало, значительная часть работ — замена дома или капитальная реконструкция, а пляжные участки добавляют концессию ZOFEMAT и полную морскую спецификацию.',
 'de': 'Zazil-Ha und Coco Beach bilden die Strandlage nördlich des Zentrums und zählen, neben Playacar Phase II und Xcalacoco, zu den teuersten Adressen von Playa del Carmen. Bezahlt wird hier der Fußweg zum Strand bei zehn Minuten Entfernung zur Quinta Avenida. Es ist ein etabliertes Stadtgebiet: wenige freie Grundstücke, viel Ersatzneubau und Komplettsanierung; Strandgrundstücke bringen ZOFEMAT-Konzession und volle Meeresspezifikation mit.',
 'fr': 'Zazil-Ha et Coco Beach forment le front de mer au nord du centre et figurent, avec Playacar Phase II et Xcalacoco, parmi les adresses les plus chères de Playa del Carmen. Ce que l’on paie ici, c’est d’aller à la plage à pied tout en restant à dix minutes de la Quinta Avenida. Le secteur est constitué : peu de terrains libres, beaucoup de démolition-reconstruction et de rénovation intégrale ; les lots de plage ajoutent la concession ZOFEMAT et une spécification marine complète.',
 'zh': 'Zazil-Ha 与 Coco Beach 构成市中心以北的海滨地带，与 Playacar 二期、Xcalacoco 同属普拉亚德尔卡门最昂贵的地址。人们在此支付的是“步行可达海滩、同时距第五大道仅十分钟”。该片区已高度成熟：空置地块不多，大量工作是原房重建或整体翻新；海滩地块还需 ZOFEMAT 特许并采用完整的海洋环境标准。'},
'playa-magna': {
 'es': 'Playa Magna es residencial cerrado consolidado en Playa del Carmen, con demanda de renta larga estable y precio más razonable que el frente de playa. El producto natural es la casa para vivir todo el año o para rentar a residentes, no para rotación diaria. El reglamento del residencial define fachada, alturas y áreas verdes, y la licencia municipal de Solidaridad con DRO va en paralelo.',
 'en': 'Playa Magna is a consolidated gated residential area in Playa del Carmen, with steady long-term rental demand and a more reasonable price than the beachfront. The natural product is a house to live in year-round or to rent to residents, not for daily turnover. The community rules set façade, heights and green areas, and the Solidaridad municipal licence with a DRO runs in parallel.',
 'ru': 'Плая-Магна — сложившийся закрытый жилой район Плая-дель-Кармен, со стабильным спросом на длительную аренду и более разумной ценой, чем первая линия. Естественный продукт — дом для круглогодичной жизни или аренды резидентам, а не для посуточной ротации. Регламент посёлка задаёт фасад, высоты и зелёные зоны, а муниципальная лицензия Solidaridad с DRO идёт параллельно.',
 'de': 'Playa Magna ist ein etabliertes geschlossenes Wohngebiet in Playa del Carmen, mit stabiler Langzeitmietnachfrage und günstigerem Preis als die Strandlage. Das natürliche Produkt ist ein Haus zum ganzjährigen Wohnen oder zur Vermietung an Residenten, nicht für täglichen Wechsel. Die Anlagensatzung regelt Fassade, Höhen und Grünflächen, die kommunale Lizenz von Solidaridad mit DRO läuft parallel.',
 'fr': 'Playa Magna est une résidence fermée constituée de Playa del Carmen, avec une demande locative longue durée stable et un prix plus raisonnable que le front de mer. Le produit naturel est la maison pour vivre à l’année ou louer à des résidents, pas pour la rotation quotidienne. Le règlement fixe façade, hauteurs et espaces verts ; le permis municipal de Solidaridad avec DRO avance en parallèle.',
 'zh': 'Playa Magna 是普拉亚德尔卡门一处成熟的封闭住宅区，长租需求稳定，价格较海滨地带更为合理。其天然产品是供全年居住或出租给常住客的住宅，而非按天周转。社区规约规定立面、高度与绿地，带 DRO 的 Solidaridad 市政许可同步推进。'},
'playa-del-secreto': {
 'es': 'Playa del Secreto es el enclave discreto de casas frente al mar entre Puerto Morelos y Playa del Carmen: pocos lotes, playa amplia y muy poca densidad. Es de las direcciones más privadas del corredor, y por eso la obra se planea con acceso controlado, horarios acordados y especificación marina completa. Municipio Puerto Morelos, con el arrecife marcando la pauta ambiental.',
 'en': 'Playa del Secreto is the discreet beachfront enclave between Puerto Morelos and Playa del Carmen: few lots, a wide beach and very low density. It is one of the most private addresses on the corridor, so the build is planned with controlled access, agreed hours and a full marine spec. Puerto Morelos municipality, with the reef setting the environmental pace.',
 'ru': 'Плая-дель-Секрето — непубличный анклав домов на первой линии между Пуэрто-Морелосом и Плая-дель-Кармен: мало участков, широкий пляж и очень низкая плотность. Один из самых приватных адресов коридора, поэтому стройка планируется с контролируемым доступом, согласованными часами и полной морской спецификацией. Муниципалитет Пуэрто-Морелос, а экологический ритм задаёт риф.',
 'de': 'Playa del Secreto ist die diskrete Strandhaus-Enklave zwischen Puerto Morelos und Playa del Carmen: wenige Grundstücke, breiter Strand und sehr geringe Dichte. Eine der privatesten Adressen des Korridors — der Bau wird mit kontrollierter Zufahrt, abgestimmten Zeiten und voller Meeresspezifikation geplant. Gemeinde Puerto Morelos, den ökologischen Takt gibt das Riff vor.',
 'fr': 'Playa del Secreto est l’enclave discrète de maisons en front de mer entre Puerto Morelos et Playa del Carmen : peu de lots, une plage large et une densité très faible. C’est l’une des adresses les plus privées du corridor : le chantier se planifie avec accès contrôlé, horaires convenus et spécification marine complète. Commune de Puerto Morelos, le récif donnant le tempo environnemental.',
 'zh': 'Playa del Secreto 是 Puerto Morelos 与普拉亚德尔卡门之间低调的海滨住宅聚落：地块稀少、沙滩宽阔、密度极低。作为走廊上最私密的地址之一，施工须按受控出入、约定时段与完整海洋环境标准来安排。属 Puerto Morelos 市辖，环保节奏由珊瑚礁决定。'},
'ruta-de-los-cenotes': {
 'es': 'La Ruta de los Cenotes es el corredor de selva tierra adentro de Puerto Morelos: terreno mucho más barato que la costa, cenotes en el propio predio y cero infraestructura de red. Ese es el trato: se ahorra en tierra y se invierte en autonomía —pozo, cisterna, planta de tratamiento y solar con respaldo—. Y hay una responsabilidad concreta: los cenotes alimentan el acuífero que llega al arrecife, así que el manejo de aguas residuales no admite atajos.',
 'en': 'The Ruta de los Cenotes is Puerto Morelos’ inland jungle corridor: land far cheaper than the coast, cenotes on the lot itself and zero network infrastructure. That is the trade: you save on land and invest in self-sufficiency — well, cistern, treatment plant and solar with backup. And there is a concrete responsibility: the cenotes feed the aquifer that reaches the reef, so wastewater handling allows no shortcuts.',
 'ru': 'Рута сенотов — вглубь материка от Пуэрто-Морелоса, коридор сельвы: земля намного дешевле побережья, сеноты прямо на участке и полное отсутствие сетей. Такова сделка: экономите на земле и вкладываетесь в автономность — скважина, цистерна, очистные и солнечная станция с резервом. И есть конкретная ответственность: сеноты питают водоносный горизонт, который доходит до рифа, поэтому в обращении со стоками срезать углы нельзя.',
 'de': 'Die Ruta de los Cenotes ist der Dschungelkorridor im Hinterland von Puerto Morelos: Land weit günstiger als an der Küste, Cenoten auf dem Grundstück selbst und null Netzinfrastruktur. Das ist der Handel: Man spart am Boden und investiert in Autarkie — Brunnen, Zisterne, Kläranlage und Solar mit Backup. Und es gibt eine konkrete Verantwortung: Die Cenoten speisen den Grundwasserleiter, der bis zum Riff reicht — beim Abwasser sind Abkürzungen ausgeschlossen.',
 'fr': 'La Ruta de los Cenotes est le corridor de jungle à l’intérieur des terres de Puerto Morelos : un foncier bien moins cher que la côte, des cénotes sur le terrain même et zéro réseau. C’est le marché : on économise sur la terre et on investit dans l’autonomie — puits, citerne, station de traitement et solaire avec secours. Et il y a une responsabilité concrète : les cénotes alimentent l’aquifère qui rejoint le récif ; l’assainissement n’autorise aucun raccourci.',
 'zh': '天然井之路是 Puerto Morelos 内陆的丛林走廊：地价远低于海岸，地块内往往就有天然井，且完全没有市政管网。这就是取舍：省下的是地价，投入的是自给系统——水井、蓄水池、污水处理设备与带备用的太阳能。同时也伴随明确的责任：天然井补给的含水层最终通向珊瑚礁，污水处理绝不能走捷径。'},
}

NORM = {
'playa-del-secreto': {
 'es': 'Playa del Secreto está en el municipio de Puerto Morelos, independiente desde 2016: ahí se tramitan uso de suelo y licencia de construcción con DRO. Al ser frente de mar entra la concesión ZOFEMAT y, por la cercanía del Parque Nacional Arrecife de Puerto Morelos, autorización ambiental con condiciones sobre desmonte, escurrimientos, iluminación hacia la playa y tratamiento de aguas. La baja densidad de la zona es parte de la norma, no una casualidad del mercado.',
 'en': 'Playa del Secreto is in the municipality of Puerto Morelos, independent since 2016: land use and the building licence with a DRO are processed there. Being beachfront brings a ZOFEMAT concession and, given the proximity of the Puerto Morelos Reef National Park, environmental authorisation with conditions on clearing, runoff, beach-facing lighting and wastewater treatment. The area’s low density is part of the rules, not a market accident.',
 'ru': 'Плая-дель-Секрето относится к муниципалитету Пуэрто-Морелос, самостоятельному с 2016 года: там оформляются назначение земли и разрешение на строительство с DRO. Первая линия добавляет концессию ZOFEMAT, а близость Национального парка «Риф Пуэрто-Морелос» — экологическое разрешение с условиями по расчистке, стоку, освещению в сторону пляжа и очистке стоков. Низкая плотность здесь — часть нормы, а не случайность рынка.',
 'de': 'Playa del Secreto liegt in der Gemeinde Puerto Morelos, seit 2016 eigenständig: Dort werden Nutzungsart und Baugenehmigung mit DRO bearbeitet. Die Strandlage bringt die ZOFEMAT-Konzession und wegen der Nähe zum Riff-Nationalpark Puerto Morelos eine Umweltgenehmigung mit Auflagen zu Rodung, Abfluss, strandseitiger Beleuchtung und Abwasserbehandlung. Die geringe Dichte ist Teil der Norm, kein Marktzufall.',
 'fr': 'Playa del Secreto est dans la commune de Puerto Morelos, indépendante depuis 2016 : usage du sol et permis de construire avec DRO s’y traitent. Le front de mer implique la concession ZOFEMAT et, vu la proximité du Parc National du Récif de Puerto Morelos, une autorisation environnementale assortie de conditions sur le défrichement, le ruissellement, l’éclairage côté plage et le traitement des eaux. La faible densité relève de la règle, pas du hasard du marché.',
 'zh': 'Playa del Secreto 隶属 Puerto Morelos 市（2016年独立设市）：土地用途与带 DRO 的施工许可均在该市办理。海滨属性带来 ZOFEMAT 特许；因毗邻 Puerto Morelos 珊瑚礁国家公园，还需环保许可，并对清林、径流、朝向沙滩的照明与污水处理提出条件。该片区的低密度是法规使然，而非市场偶然。'},
'ruta-de-los-cenotes': {
 'es': 'Municipio Puerto Morelos: uso de suelo y licencia con DRO ahí. Aquí no hay ZOFEMAT porque no hay playa, pero sí un filtro ambiental serio: cualquier predio con cenote o con escurrimiento hacia el sistema kárstico exige autorización con condiciones sobre desmonte, descargas y distancia de construcción respecto al cuerpo de agua. La factibilidad de servicios se resuelve por cuenta propia y se documenta: pozo, tratamiento y energía.',
 'en': 'Puerto Morelos municipality: land use and the licence with a DRO go there. There is no ZOFEMAT here because there is no beach, but there is a serious environmental filter: any lot with a cenote or drainage into the karst system requires authorisation with conditions on clearing, discharges and setback from the water body. Utility feasibility is solved privately and documented: well, treatment and power.',
 'ru': 'Муниципалитет Пуэрто-Морелос: назначение земли и лицензия с DRO там. ZOFEMAT здесь нет, потому что нет пляжа, но есть серьёзный экологический фильтр: любой участок с сенотом или стоком в карстовую систему требует согласования с условиями по расчистке, сбросам и отступу застройки от водного объекта. Возможность подключения решается своими силами и документируется: скважина, очистные, энергия.',
 'de': 'Gemeinde Puerto Morelos: Nutzungsart und Lizenz mit DRO laufen dort. ZOFEMAT gibt es hier nicht, weil es keinen Strand gibt, dafür einen ernsthaften Umweltfilter: Jedes Grundstück mit Cenote oder Abfluss in das Karstsystem erfordert eine Genehmigung mit Auflagen zu Rodung, Einleitungen und Abstand der Bebauung zum Gewässer. Die Versorgung wird in Eigenregie gelöst und dokumentiert: Brunnen, Aufbereitung, Energie.',
 'fr': 'Commune de Puerto Morelos : usage du sol et permis avec DRO s’y traitent. Pas de ZOFEMAT ici puisqu’il n’y a pas de plage, mais un filtre environnemental sérieux : tout terrain avec cénote ou écoulement vers le système karstique exige une autorisation assortie de conditions sur le défrichement, les rejets et le recul de la construction par rapport au plan d’eau. La faisabilité des réseaux se règle en propre et se documente : puits, traitement, énergie.',
 'zh': '属 Puerto Morelos 市辖：土地用途与带 DRO 的许可在该市办理。此处没有海滩，因而无需 ZOFEMAT，但环保门槛依然很高：凡地块内有天然井或径流汇入喀斯特水系的，均须取得许可，并对清林、排放及建筑退让水体的距离作出规定。市政配套需自行解决并留存记录：水井、污水处理与供电。'},
}

FAQ = {
'zazil-ha-coco-beach': {
 'es': [('¿Quedan terrenos en Zazil-Ha o Coco Beach?', 'Pocos y caros. Gran parte del trabajo aquí es sustitución de casa existente o remodelación integral, con la ventaja de servicios instalados y la restricción de obra en zona urbana consolidada.'),
        ('¿Qué exige un predio frente al mar?', 'Concesión ZOFEMAT, autorización ambiental por duna y vegetación costera, y especificación marina completa: recubrimientos mayores, acero protegido, cancelería anodizada e impermeabilización reforzada.')],
 'en': [('Are there lots left in Zazil-Ha or Coco Beach?', 'Few and expensive. Much of the work here is replacing an existing house or a full renovation, with the advantage of services in place and the constraint of building in a consolidated urban area.'),
        ('What does a beachfront lot require?', 'A ZOFEMAT concession, environmental authorisation for the dune and coastal vegetation, and a full marine spec: greater cover, protected rebar, anodised joinery and reinforced waterproofing.')],
 'ru': [('Остались ли участки в Сасиль-Ха или Коко-Бич?', 'Мало и дорого. Значительная часть работы здесь — замена существующего дома или капитальная реконструкция, с плюсом готовых сетей и ограничением стройки в сложившемся городском районе.'),
        ('Что требует участок на первой линии?', 'Концессию ZOFEMAT, экологическое разрешение из-за дюны и прибрежной растительности и полную морскую спецификацию: увеличенный защитный слой, защищённую арматуру, анодированный алюминий и усиленную гидроизоляцию.')],
 'de': [('Gibt es noch Grundstücke in Zazil-Ha oder Coco Beach?', 'Wenige und teure. Ein großer Teil der Arbeit ist Ersatz eines Bestandshauses oder Komplettsanierung — mit vorhandener Versorgung und der Einschränkung, im etablierten Stadtgebiet zu bauen.'),
        ('Was verlangt ein Strandgrundstück?', 'ZOFEMAT-Konzession, Umweltgenehmigung wegen Düne und Küstenvegetation sowie volle Meeresspezifikation: größere Deckung, geschützte Bewehrung, eloxierte Fenster und verstärkte Abdichtung.')],
 'fr': [('Reste-t-il des terrains à Zazil-Ha ou Coco Beach ?', 'Peu, et chers. L’essentiel du travail y est le remplacement d’une maison existante ou une rénovation intégrale, avec l’avantage des réseaux en place et la contrainte du tissu urbain constitué.'),
        ('Qu’exige un lot en front de mer ?', 'Une concession ZOFEMAT, une autorisation environnementale pour la dune et la végétation côtière, et une spécification marine complète : enrobages renforcés, aciers protégés, menuiseries anodisées et étanchéité renforcée.')],
 'zh': [('Zazil-Ha 或 Coco Beach 还有地块吗？', '很少且价格昂贵。这里的工作大多是原房重建或整体翻新，优势是市政配套齐备，限制是在成熟城区内施工。'),
        ('海滨地块有哪些要求？', 'ZOFEMAT 特许、因沙丘与海岸植被而需的环保许可，以及完整的海洋环境标准：加大保护层、钢筋防护、阳极氧化门窗与加强防水。')]},
'playa-magna': {
 'es': [('¿Playa Magna sirve para renta?', 'Para renta larga a residentes, sí: la demanda es estable y el entorno cerrado ayuda. Para rotación diaria conviene revisar antes el reglamento del residencial, porque la comunidad está pensada para vivir.'),
        ('¿Qué permisos aplican?', 'Reglamento del residencial —fachada, alturas, áreas verdes— y licencia municipal de Solidaridad con proyecto firmado por DRO. Los presentamos en paralelo para no perder semanas.')],
 'en': [('Does Playa Magna work for rental?', 'For long-term rental to residents, yes: demand is steady and the gated setting helps. For daily turnover, check the community rules first, because it is designed for living.'),
        ('Which permits apply?', 'The community rules — façade, heights, green areas — and the Solidaridad municipal licence with DRO-signed drawings. We file both in parallel so no weeks are lost.')],
 'ru': [('Подходит ли Плая-Магна под аренду?', 'Под длительную аренду резидентам — да: спрос стабильный, закрытая среда помогает. Для посуточной ротации сначала проверьте регламент посёлка: он рассчитан на проживание.'),
        ('Какие разрешения нужны?', 'Регламент посёлка — фасад, высоты, зелёные зоны — и муниципальная лицензия Solidaridad с проектом за подписью DRO. Подаём параллельно, чтобы не терять недели.')],
 'de': [('Eignet sich Playa Magna zur Vermietung?', 'Für Langzeitvermietung an Residenten ja: stabile Nachfrage, das geschlossene Umfeld hilft. Für täglichen Wechsel zuerst die Anlagensatzung prüfen — sie ist fürs Wohnen ausgelegt.'),
        ('Welche Genehmigungen gelten?', 'Die Anlagensatzung — Fassade, Höhen, Grünflächen — und die kommunale Lizenz von Solidaridad mit DRO-unterzeichneten Plänen. Wir reichen beides parallel ein.')],
 'fr': [('Playa Magna convient-il à la location ?', 'Pour la location longue durée à des résidents, oui : la demande est stable et le cadre fermé aide. Pour la rotation quotidienne, vérifiez d’abord le règlement : la résidence est pensée pour habiter.'),
        ('Quels permis s’appliquent ?', 'Le règlement de la résidence — façade, hauteurs, espaces verts — et le permis municipal de Solidaridad avec plans signés par un DRO. Nous déposons les deux en parallèle.')],
 'zh': [('Playa Magna 适合出租吗？', '面向常住客的长租适合：需求稳定，封闭环境是加分项。若打算按天周转，请先核查社区规约——该社区按居住定位设计。'),
        ('需要哪些许可？', '社区规约（立面、高度、绿地）与带 DRO 签署图纸的 Solidaridad 市政许可。两者并行报审，避免浪费数周。')]},
'playa-del-secreto': {
 'es': [('¿Por qué Playa del Secreto y no Playa del Carmen?', 'Por privacidad y densidad: playa amplia, pocos vecinos y una zona que la norma mantiene baja en construcción. Se pierde la caminata al centro; se gana una casa que no comparte playa con un hotel.'),
        ('¿Qué municipio y qué permisos?', 'Puerto Morelos, independiente desde 2016: uso de suelo y licencia con DRO ahí, concesión ZOFEMAT por ser frente de mar y autorización ambiental por el Parque Nacional Arrecife.')],
 'en': [('Why Playa del Secreto rather than Playa del Carmen?', 'Privacy and density: a wide beach, few neighbours and an area the rules keep low-rise. You lose the walk downtown; you gain a house that does not share its beach with a hotel.'),
        ('Which municipality and permits?', 'Puerto Morelos, independent since 2016: land use and the licence with a DRO there, a ZOFEMAT concession for being beachfront and environmental authorisation because of the Reef National Park.')],
 'ru': [('Почему Плая-дель-Секрето, а не Плая-дель-Кармен?', 'Приватность и плотность: широкий пляж, мало соседей и зона, которую норма держит малоэтажной. Теряете пешую доступность центра, выигрываете дом, который не делит пляж с отелем.'),
        ('Какой муниципалитет и какие разрешения?', 'Пуэрто-Морелос, самостоятельный с 2016 года: назначение земли и лицензия с DRO там, концессия ZOFEMAT как для первой линии и экологическое разрешение из-за Нацпарка «Риф».')],
 'de': [('Warum Playa del Secreto statt Playa del Carmen?', 'Privatsphäre und Dichte: breiter Strand, wenige Nachbarn und ein Gebiet, das die Norm niedrig hält. Man verliert den Fußweg ins Zentrum und gewinnt ein Haus, das seinen Strand nicht mit einem Hotel teilt.'),
        ('Welche Gemeinde und welche Genehmigungen?', 'Puerto Morelos, seit 2016 eigenständig: Nutzungsart und Lizenz mit DRO dort, ZOFEMAT-Konzession wegen der Strandlage und Umweltgenehmigung wegen des Riff-Nationalparks.')],
 'fr': [('Pourquoi Playa del Secreto plutôt que Playa del Carmen ?', 'L’intimité et la densité : plage large, peu de voisins et un secteur que la règle maintient bas. On perd l’accès à pied au centre ; on gagne une maison qui ne partage pas sa plage avec un hôtel.'),
        ('Quelle commune et quels permis ?', 'Puerto Morelos, indépendante depuis 2016 : usage du sol et permis avec DRO sur place, concession ZOFEMAT en front de mer et autorisation environnementale du fait du Parc National du Récif.')],
 'zh': [('为什么选 Playa del Secreto 而不是普拉亚德尔卡门？', '为了私密性与低密度：沙滩宽阔、邻居稀少，且法规将该片区维持在低层开发。代价是无法步行到市中心，换来的是一栋不与酒店共用沙滩的住宅。'),
        ('归属哪个市政、需要哪些许可？', 'Puerto Morelos 市（2016年独立设市）：土地用途与带 DRO 的许可在该市办理；因属海滨需 ZOFEMAT 特许，并因珊瑚礁国家公园而需环保许可。')]},
'ruta-de-los-cenotes': {
 'es': [('¿Cuánto se ahorra comprando en la Ruta de los Cenotes?', 'Mucho en terreno y poco en obra: al no haber red hay que resolver pozo, cisterna, tratamiento y energía. El ahorro real depende de cuánta autonomía necesite el proyecto, y eso se dimensiona en el anteproyecto.'),
        ('¿Puedo construir si el predio tiene un cenote?', 'Con autorización y condiciones: distancia de construcción al cuerpo de agua, control de descargas y de escurrimientos. El cenote alimenta el acuífero que llega al arrecife; el proyecto se diseña alrededor de él, no encima.')],
 'en': [('How much do you save buying on the Ruta de los Cenotes?', 'A lot on land and little on construction: with no network you must solve well, cistern, treatment and power. The real saving depends on how much autonomy the project needs, and that is sized at concept stage.'),
        ('Can I build if the lot has a cenote?', 'With authorisation and conditions: setback from the water body, control of discharges and runoff. The cenote feeds the aquifer that reaches the reef; the project is designed around it, not on top of it.')],
 'ru': [('Сколько экономишь, покупая на Руте сенотов?', 'Много на земле и мало на стройке: сетей нет, поэтому нужны скважина, цистерна, очистные и энергия. Реальная экономия зависит от требуемой автономности, а она считается на стадии эскиза.'),
        ('Можно ли строить, если на участке сенот?', 'С разрешением и условиями: отступ застройки от водного объекта, контроль сбросов и стока. Сенот питает водоносный горизонт, доходящий до рифа; проект строится вокруг него, а не поверх.')],
 'de': [('Wie viel spart man auf der Ruta de los Cenotes?', 'Viel beim Grundstück und wenig beim Bau: Ohne Netz sind Brunnen, Zisterne, Aufbereitung und Energie zu lösen. Die reale Ersparnis hängt davon ab, wie viel Autarkie das Projekt braucht — das wird im Entwurf dimensioniert.'),
        ('Darf ich bauen, wenn das Grundstück eine Cenote hat?', 'Mit Genehmigung und Auflagen: Abstand der Bebauung zum Gewässer, Kontrolle von Einleitungen und Abfluss. Die Cenote speist den Grundwasserleiter bis zum Riff; geplant wird um sie herum, nicht darüber.')],
 'fr': [('Combien économise-t-on sur la Ruta de los Cenotes ?', 'Beaucoup sur le terrain et peu sur le chantier : sans réseau, il faut régler puits, citerne, traitement et énergie. L’économie réelle dépend du degré d’autonomie nécessaire, dimensionné dès l’avant-projet.'),
        ('Puis-je construire si le terrain a un cénote ?', 'Avec autorisation et conditions : recul de la construction par rapport au plan d’eau, contrôle des rejets et des ruissellements. Le cénote alimente l’aquifère qui rejoint le récif ; le projet se conçoit autour, pas au-dessus.')],
 'zh': [('在天然井之路购地能省多少？', '省在地价，不省在施工：没有管网，就必须解决水井、蓄水池、污水处理与供电。实际节省取决于项目所需的自给程度，这在方案阶段完成测算。'),
        ('地块内有天然井还能建吗？', '可以，但需取得许可并满足条件：建筑退让水体的距离、排放与径流控制。天然井补给的含水层最终通向珊瑚礁；方案要围绕它布置，而不是压在它上面。')]},
}

LINKS = {}
_HUB = {'es': ('construccion-de-casas', 'Construcción de casas', '/calculadora/', 'Calculadora de costos', '/blog-es/', 'Guías de construcción'),
        'en': ('house-construction', 'House construction', '/calculator/', 'Cost calculator', '/blog/', 'Construction guides'),
        'ru': ('stroitelstvo-domov', 'Строительство домов', '/kalkulyator/', 'Калькулятор стоимости', '/blog-ru/', 'Гиды по строительству'),
        'de': ('hausbau', 'Hausbau', '/kostenrechner/', 'Kostenrechner', '/blog-de/', 'Bau-Leitfäden'),
        'fr': ('construction-de-maisons', 'Construction de maisons', '/calculateur/', 'Calculateur de coûts', '/blog-fr/', 'Guides de construction'),
        'zh': ('zhuzhai-jianzao', '住宅建造', '/jisuanqi/', '造价计算器', '/blog-zh/', '建筑指南')}
_PERM = {'es': ('/permisos-de-construccion-puerto-morelos/', 'Permisos de construcción en Puerto Morelos'),
         'en': ('/construction-permits-puerto-morelos/', 'Construction permits in Puerto Morelos'),
         'ru': ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'),
         'de': ('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen, Lizenzen und DRO'),
         'fr': ('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'),
         'zh': ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO')}
_PERM_PDC = {'es': ('/permisos-de-construccion-playa-del-carmen/', 'Permisos de construcción en Playa del Carmen'),
             'en': ('/construction-permits-playa-del-carmen/', 'Construction permits in Playa del Carmen')}
for _l, (_p, _hub, _c, _cn, _b, _bn) in _HUB.items():
    LINKS[_l] = {}
    for _z in ZONE7:
        pm = _z in ('playa-del-secreto', 'ruta-de-los-cenotes')
        perm = _PERM[_l] if pm else _PERM_PDC.get(_l, _PERM[_l])
        sib = 'punta-brava' if pm else 'el-cielo-playa-del-carmen'
        LINKS[_l][_z] = [('/%s-playa-del-carmen/' % _p, '%s — Playa del Carmen' % _hub), perm,
                         ('/%s-%s/' % (_p, sib), _hub), (_c, _cn), (_b, _bn)]


def _set_parent_urls(locs):
    P = {'es': 'construccion-de-casas', 'en': 'house-construction', 'ru': 'stroitelstvo-domov',
         'de': 'hausbau', 'fr': 'construction-de-maisons', 'zh': 'zhuzhai-jianzao'}
    ml.OVR.setdefault('parent_url', {})
    for zk, d in locs.items():
        for l in LANGS:
            ml.OVR['parent_url'].setdefault(zk, {})[l] = '/%s-%s/' % (P[l], d['parent'])


if __name__ == '__main__':
    _set_parent_urls(ZONE7)
    for z in ZONE7:
        z1.ZAREA[z] = AREAS[z]; z1.ZTEXT[z] = TEXT[z]; z1.ZFAQ[z] = FAQ[z]
    for lang in LINKS:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS[lang])
    for z, d in ZONE7.items():
        for lang in LANGS:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
        for lang, txt in NORM.get(z, {}).items():
            ml.NORM[lang][z] = txt
    ml.LOCS.extend(ZONE7)
    for lang in LANGS:
        ch = ml.chrome(lang)
        for z in ZONE7:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-48s %6d bytes' % (out + '/', len(html)))
