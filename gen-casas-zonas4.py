#!/usr/bin/env python3
"""Fourth luxury-zone batch (2026-08-09): Selvazama, Punta Maroma, Xpu-Há, Bahía Petempich.

Verified before writing:
  Selvazama (Tulum) — ~500-acre master plan off Avenida Cobá, fully urbanised
    (water, power, drainage, fibre, concrete roads, bike paths), macro lots and
    single/multi-family lots. Its selling point is exactly what La Veleta lacks.
  Punta Maroma (Solidaridad) — beachfront parcels on one of the best-known beaches
    in the world, on the reef; zoning is hotel/tourism with a 3-level / 15 m height
    limit and deliberately limited permits for ecological reasons.
  Xpu-Há (Solidaridad) — bay 20 min south of Playa del Carmen; private residential
    communities (Estrella de Mar, Arrecife) with full urban services.
  Bahía Petempich (Puerto Morelos) — beachfront residences facing the reef barrier
    inside the Puerto Morelos natural-park area; gated, high privacy.
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
z1 = load('gen-casas-zonas.py', 'z1')
ml = z1.ml

ZONE4 = {
 'selvazama':       dict(parent='tulum',            f=1.20, perm='3–5'),
 'punta-maroma':    dict(parent='playa-del-carmen', f=1.45, perm='3–5'),
 'xpu-ha':          dict(parent='playa-del-carmen', f=1.22, perm='2–4'),
 'bahia-petempich': dict(parent='cancun',           f=1.35, perm='3–5'),
}

NAMES = {
 'selvazama': {'es': 'Selvazama', 'en': 'Selvazama', 'ru': 'Сельвасама', 'de': 'Selvazama', 'fr': 'Selvazama', 'zh': 'Selvazama'},
 'punta-maroma': {'es': 'Punta Maroma', 'en': 'Punta Maroma', 'ru': 'Пунта-Марома', 'de': 'Punta Maroma', 'fr': 'Punta Maroma', 'zh': 'Punta Maroma'},
 'xpu-ha': {'es': 'Xpu-Há', 'en': 'Xpu-Há', 'ru': 'Шпу-Ха', 'de': 'Xpu-Há', 'fr': 'Xpu-Há', 'zh': 'Xpu-Há'},
 'bahia-petempich': {'es': 'Bahía Petempich', 'en': 'Petempich Bay', 'ru': 'Баия-Петемпич', 'de': 'Bahía Petempich', 'fr': 'Bahía Petempich', 'zh': 'Petempich 湾'},
}
AREAS = {
 'selvazama': {'es': 'Selvazama y su entorno sobre la avenida Cobá', 'en': 'Selvazama and its surroundings off Avenida Cobá',
   'ru': 'Сельвасаме и районе авеню Коба', 'de': 'Selvazama und der Umgebung an der Avenida Cobá',
   'fr': 'Selvazama et ses abords sur l’avenue Cobá', 'zh': 'Selvazama 及 Cobá 大道沿线一带'},
 'punta-maroma': {'es': 'Punta Maroma, Punta Bete y la costa al norte de Playa del Carmen',
   'en': 'Punta Maroma, Punta Bete and the coast north of Playa del Carmen',
   'ru': 'Пунта-Мароме, Пунта-Бете и побережье к северу от Плая-дель-Кармен',
   'de': 'Punta Maroma, Punta Bete und der Küste nördlich von Playa del Carmen',
   'fr': 'Punta Maroma, Punta Bete et la côte au nord de Playa del Carmen',
   'zh': 'Punta Maroma、Punta Bete 及普拉亚德尔卡门以北海岸'},
 'xpu-ha': {'es': 'Xpu-Há, sus fraccionamientos privados y la bahía', 'en': 'Xpu-Há, its private communities and the bay',
   'ru': 'Шпу-Ха, его частных секторах и бухте', 'de': 'Xpu-Há, seinen privaten Wohnanlagen und der Bucht',
   'fr': 'Xpu-Há, ses résidences privées et la baie', 'zh': 'Xpu-Há、其私人社区与海湾'},
 'bahia-petempich': {'es': 'Bahía Petempich y la costa al sur de Puerto Morelos', 'en': 'Petempich Bay and the coast south of Puerto Morelos',
   'ru': 'Баия-Петемпич и побережье к югу от Пуэрто-Морелоса', 'de': 'Bahía Petempich und der Küste südlich von Puerto Morelos',
   'fr': 'Bahía Petempich et la côte au sud de Puerto Morelos', 'zh': 'Petempich 湾及 Puerto Morelos 以南海岸'},
}

TEXT = {
'selvazama': {
 'es': 'Selvazama es el plan maestro más grande de Tulum: unas 200 hectáreas urbanizadas sobre la avenida Cobá, con agua, electricidad, drenaje y fibra óptica, calles de concreto y ciclovías, además de lotes unifamiliares, multifamiliares, de uso mixto y macrolotes. Es justo lo que no ofrece La Veleta: infraestructura terminada. Eso acorta la obra y quita las sorpresas de factibilidad, aunque el trámite ambiental de Tulum sigue aplicando.',
 'en': 'Selvazama is Tulum’s largest master plan: roughly 200 hectares of urbanised land off Avenida Cobá, with water, power, drainage and fibre, concrete roads and bike paths, plus single-family, multi-family, mixed-use and macro lots. It is exactly what La Veleta does not offer: finished infrastructure. That shortens the build and removes feasibility surprises, though Tulum’s environmental process still applies.',
 'ru': 'Сельвасама — крупнейший мастер-план Тулума: около 200 гектаров урбанизированной земли вдоль авеню Коба, с водой, электричеством, канализацией и оптикой, бетонными улицами и велодорожками, плюс участки под индивидуальные дома, многоквартирные и смешанные проекты и макролоты. Это ровно то, чего нет в Ла-Велете: готовая инфраструктура. Она сокращает стройку и снимает сюрпризы по подключениям, хотя экологическая процедура Тулума всё равно действует.',
 'de': 'Selvazama ist der größte Masterplan Tulums: rund 200 Hektar erschlossenes Land an der Avenida Cobá, mit Wasser, Strom, Kanalisation und Glasfaser, Betonstraßen und Radwegen sowie Grundstücken für Einfamilien-, Mehrfamilien- und Mischnutzung samt Makrolots. Genau das, was La Veleta nicht bietet: fertige Infrastruktur. Das verkürzt den Bau und nimmt Erschließungsüberraschungen — das Umweltverfahren von Tulum gilt dennoch.',
 'fr': 'Selvazama est le plus grand plan-masse de Tulum : environ 200 hectares urbanisés le long de l’avenue Cobá, avec eau, électricité, assainissement et fibre, voiries en béton et pistes cyclables, ainsi que des lots individuels, collectifs, mixtes et des macro-lots. C’est précisément ce que La Veleta n’offre pas : une infrastructure achevée. Cela raccourcit le chantier et supprime les surprises de faisabilité, même si la procédure environnementale de Tulum reste applicable.',
 'zh': 'Selvazama 是图卢姆规模最大的总体规划区：沿 Cobá 大道约200公顷已完成市政配套的土地，供水、供电、排水与光纤齐备，配混凝土道路与自行车道，并提供独栋、多户、混合用途地块及大宗地块。这正是 La Veleta 所缺乏的——成熟的基础设施，可缩短工期并消除接入方面的意外，不过图卢姆的环保流程依然适用。'},
'punta-maroma': {
 'es': 'Punta Maroma es el frente de mar más exclusivo al norte de Playa del Carmen, sobre una de las playas más reconocidas del mundo y frente al segundo arrecife más grande del planeta. La zonificación es turístico-hotelera con límite de 3 niveles o 15 metros de altura, y los permisos se otorgan de forma deliberadamente limitada para proteger el entorno. Aquí no se construye volumen: se construye una residencia o un proyecto boutique, con especificación marina completa y un expediente ambiental impecable.',
 'en': 'Punta Maroma is the most exclusive beachfront north of Playa del Carmen, on one of the best-known beaches in the world and facing the second largest reef on the planet. Zoning is hotel/tourism with a 3-level or 15-metre height cap, and permits are granted deliberately sparingly to protect the setting. You do not build volume here: you build one residence or a boutique project, with a full marine spec and a spotless environmental file.',
 'ru': 'Пунта-Марома — самая эксклюзивная первая линия к северу от Плая-дель-Кармен, на одном из самых известных пляжей мира и напротив второго по величине рифа планеты. Зонирование туристско-гостиничное с ограничением в 3 уровня или 15 метров высоты, а разрешения выдаются намеренно ограниченно ради защиты среды. Здесь не строят объёмом: здесь строят одну резиденцию или бутик-проект, с полной морской спецификацией и безупречным экологическим досье.',
 'de': 'Punta Maroma ist die exklusivste Strandlage nördlich von Playa del Carmen, an einem der bekanntesten Strände der Welt und gegenüber dem zweitgrößten Riff der Erde. Die Zonierung ist Hotel/Tourismus mit einer Höhenbegrenzung von 3 Ebenen bzw. 15 Metern, und Genehmigungen werden bewusst restriktiv erteilt, um die Umgebung zu schützen. Hier baut man kein Volumen, sondern eine Residenz oder ein Boutiqueprojekt — mit voller Meeresspezifikation und einer tadellosen Umweltakte.',
 'fr': 'Punta Maroma est le front de mer le plus exclusif au nord de Playa del Carmen, sur l’une des plages les plus réputées au monde et face au deuxième plus grand récif de la planète. Le zonage est hôtelier-touristique, avec une limite de 3 niveaux ou 15 mètres, et les permis sont délivrés de façon volontairement restreinte pour protéger le site. Ici on ne construit pas du volume : on construit une résidence ou un projet boutique, avec une spécification marine complète et un dossier environnemental irréprochable.',
 'zh': 'Punta Maroma 是普拉亚德尔卡门以北最为稀缺的海滨地段，坐落于世界知名海滩之上，正对全球第二大珊瑚礁。规划用途为旅游酒店类，限高3层或15米，且出于生态保护考虑，许可发放刻意从严。这里不做体量开发：只做一栋住宅或精品项目，配以完整的海洋环境做法与无可挑剔的环保申报材料。'},
'xpu-ha': {
 'es': 'Xpu-Há es una bahía a veinte minutos al sur de Playa del Carmen, con fraccionamientos privados como Estrella de Mar y Arrecife: lotes de 600 a 800 m², calles de concreto hidráulico, agua, luz, drenaje y áreas de conservación dentro del propio desarrollo. Es la opción de playa con servicios completos y precio más razonable que Tulum o Puerto Aventuras, en municipio Solidaridad, con los tiempos de permiso más cortos de la costa sur.',
 'en': 'Xpu-Há is a bay twenty minutes south of Playa del Carmen, with private communities such as Estrella de Mar and Arrecife: lots of 600 to 800 m², hydraulic concrete streets, water, power, drainage and conservation areas inside the development itself. It is the beach option with full services at a more reasonable price than Tulum or Puerto Aventuras, in the Solidaridad municipality, with the shortest permit timelines on the southern coast.',
 'ru': 'Шпу-Ха — бухта в двадцати минутах к югу от Плая-дель-Кармен, с частными секторами вроде Эстрелья-де-Мар и Аррecife: участки 600–800 м², улицы из гидравлического бетона, вода, свет, канализация и охраняемые зоны внутри самой застройки. Это вариант «пляж с полными коммуникациями» по более разумной цене, чем Тулум или Пуэрто-Авентурас, в муниципалитете Solidaridad, с самыми короткими сроками разрешений на южном побережье.',
 'de': 'Xpu-Há ist eine Bucht zwanzig Minuten südlich von Playa del Carmen, mit privaten Anlagen wie Estrella de Mar und Arrecife: Grundstücke von 600 bis 800 m², Straßen aus Hydraulikbeton, Wasser, Strom, Kanalisation und Schutzflächen innerhalb der Anlage. Die Strandoption mit voller Erschließung zu einem vernünftigeren Preis als Tulum oder Puerto Aventuras, in der Gemeinde Solidaridad, mit den kürzesten Genehmigungszeiten der Südküste.',
 'fr': 'Xpu-Há est une baie à vingt minutes au sud de Playa del Carmen, avec des résidences privées comme Estrella de Mar et Arrecife : des lots de 600 à 800 m², des voiries en béton hydraulique, l’eau, l’électricité, l’assainissement et des zones de conservation au sein même du développement. C’est l’option plage entièrement viabilisée à un prix plus raisonnable que Tulum ou Puerto Aventuras, en commune de Solidaridad, avec les délais de permis les plus courts de la côte sud.',
 'zh': 'Xpu-Há 是位于普拉亚德尔卡门以南二十分钟车程的海湾，拥有 Estrella de Mar、Arrecife 等私人社区：地块约600至800平方米，采用水硬性混凝土道路，供水、供电、排水齐备，开发区内另设保护绿地。这是配套齐全的海滨选择，价格较图卢姆或 Puerto Aventuras 更为合理，属 Solidaridad 市辖，许可周期为南部海岸最短。'},
'bahia-petempich': {
 'es': 'Bahía Petempich es la franja de residencias frente al mar al sur de Puerto Morelos, dentro del área natural protegida y de cara a la barrera arrecifal. Es la zona más discreta del corredor norte: pocos lotes, mucha privacidad, arena tranquila y una normativa que gira toda alrededor del arrecife —tratamiento de aguas obligatorio, control de escurrimientos y expediente ambiental cuidado desde el primer plano.',
 'en': 'Petempich Bay is the strip of beachfront residences south of Puerto Morelos, inside the protected natural area and facing the reef barrier. It is the most discreet stretch of the northern corridor: few lots, a lot of privacy, calm sand and a rulebook that revolves entirely around the reef — mandatory wastewater treatment, runoff control and an environmental file handled carefully from the first drawing.',
 'ru': 'Баия-Петемпич — полоса резиденций на первой линии к югу от Пуэрто-Морелоса, внутри охраняемой природной территории и напротив барьерного рифа. Это самый непубличный участок северного коридора: мало лотов, много приватности, спокойный песок и нормативка, целиком построенная вокруг рифа — обязательная очистка стоков, контроль поверхностного стока и экологическое досье, которое ведётся с первого чертежа.',
 'de': 'Bahía Petempich ist der Streifen von Strandresidenzen südlich von Puerto Morelos, innerhalb des Naturschutzgebiets und gegenüber dem Barriereriff. Es ist der diskreteste Abschnitt des Nordkorridors: wenige Grundstücke, viel Privatsphäre, ruhiger Sand und ein Regelwerk, das sich ganz um das Riff dreht — verpflichtende Abwasserbehandlung, Abflusskontrolle und eine Umweltakte, die ab der ersten Zeichnung sorgfältig geführt wird.',
 'fr': 'Bahía Petempich est la bande de résidences en bord de mer au sud de Puerto Morelos, à l’intérieur de l’aire naturelle protégée et face à la barrière de corail. C’est le secteur le plus discret du corridor nord : peu de lots, beaucoup d’intimité, un sable paisible et une réglementation entièrement centrée sur le récif — traitement des eaux obligatoire, contrôle des ruissellements et dossier environnemental soigné dès le premier plan.',
 'zh': 'Bahía Petempich 是 Puerto Morelos 以南的海滨住宅带，位于自然保护区之内、正对堡礁。它是北部走廊中最低调的一段：地块稀少、私密性强、沙滩宁静，而全部规则都围绕珊瑚礁展开——污水处理为强制项、需控制地表径流，环保申报材料从第一版图纸起就要认真准备。'},
}

NORM_OVR = {
'punta-maroma': {
 'es': 'Punta Maroma está en el municipio de Solidaridad, pero su zonificación es turístico-hotelera, no residencial común: el límite de altura es de 3 niveles o 15 metros y el uso de suelo debe verificarse lote por lote antes de comprar. A la licencia municipal con DRO se suman la concesión ZOFEMAT en frente de playa y la autorización ambiental, que aquí pesa más que en cualquier otro punto de la costa por el arrecife y la duna. Los permisos se otorgan de forma limitada: el proyecto se diseña para caber en la norma, no al revés.',
 'en': 'Punta Maroma is in the Solidaridad municipality, but its zoning is hotel/tourism rather than ordinary residential: the height cap is 3 levels or 15 metres and land use has to be checked lot by lot before you buy. On top of the municipal licence with a DRO come the ZOFEMAT concession on the beachfront and the environmental authorisation, which carries more weight here than anywhere else on the coast because of the reef and the dune. Permits are granted sparingly: the project is designed to fit the rules, not the other way round.',
 'ru': 'Пунта-Марома относится к муниципалитету Solidaridad, но зонирование здесь туристско-гостиничное, а не обычное жилое: ограничение по высоте — 3 уровня или 15 метров, и назначение земли нужно проверять по каждому лоту до покупки. К муниципальной лицензии с DRO добавляются концессия ZOFEMAT на первой линии и экологическое разрешение, которое здесь весит больше, чем где-либо на побережье, из-за рифа и дюны. Разрешения выдаются ограниченно: проект подгоняется под норму, а не наоборот.',
 'de': 'Punta Maroma liegt in der Gemeinde Solidaridad, ist aber als Hotel-/Tourismusgebiet ausgewiesen, nicht als gewöhnliches Wohngebiet: Die Höhenbegrenzung beträgt 3 Ebenen bzw. 15 Meter, und die Nutzungsart muss vor dem Kauf Grundstück für Grundstück geprüft werden. Zur kommunalen Lizenz mit DRO kommen die ZOFEMAT-Konzession am Strand und die Umweltgenehmigung, die hier wegen Riff und Düne schwerer wiegt als anderswo an der Küste. Genehmigungen werden restriktiv erteilt: Der Entwurf richtet sich nach der Norm, nicht umgekehrt.',
 'fr': 'Punta Maroma se trouve en commune de Solidaridad, mais son zonage est hôtelier-touristique et non résidentiel ordinaire : la limite de hauteur est de 3 niveaux ou 15 mètres et l’usage du sol doit être vérifié lot par lot avant l’achat. Au permis municipal avec DRO s’ajoutent la concession ZOFEMAT en front de plage et l’autorisation environnementale, qui pèse ici plus que partout ailleurs sur la côte du fait du récif et de la dune. Les permis sont délivrés avec parcimonie : le projet se conçoit pour entrer dans la norme, et non l’inverse.',
 'zh': 'Punta Maroma 属 Solidaridad 市辖，但其规划用途为旅游酒店类而非普通住宅：限高3层或15米，购地前须逐地块核实土地用途。除带 DRO 的市政许可外，海滨地块还需 ZOFEMAT 特许与环保许可；因珊瑚礁与沙丘的存在，此处的环保审查比海岸其他任何地段都更为关键。许可发放从严：方案须迁就法规，而非相反。'},
'bahia-petempich': {
 'es': 'Bahía Petempich pertenece al municipio de Puerto Morelos, independiente desde 2016, y está dentro del área de influencia del Parque Nacional Arrecife de Puerto Morelos. Ahí se tramitan uso de suelo y licencia de construcción con DRO; frente al mar aplica concesión ZOFEMAT y prácticamente siempre autorización ambiental, con condiciones sobre desmonte, escurrimientos, iluminación hacia la playa y tratamiento de aguas residuales. Es de las zonas donde el expediente ambiental define el calendario completo de la obra.',
 'en': 'Petempich Bay belongs to the municipality of Puerto Morelos, independent since 2016, and sits within the influence area of the Puerto Morelos Reef National Park. Land use and the building licence with a DRO are processed there; beachfront lots require a ZOFEMAT concession and, in practice, always an environmental authorisation, with conditions on clearing, runoff, beach-facing lighting and wastewater treatment. This is one of the areas where the environmental file sets the entire construction calendar.',
 'ru': 'Баия-Петемпич относится к муниципалитету Пуэрто-Морелос, самостоятельному с 2016 года, и находится в зоне влияния Национального парка «Риф Пуэрто-Морелос». Там оформляются назначение земли и разрешение на строительство с DRO; на первой линии нужна концессия ZOFEMAT и практически всегда экологическое разрешение — с условиями по расчистке, стоку, освещению в сторону пляжа и очистке сточных вод. Это одна из зон, где экологическое досье задаёт весь календарь стройки.',
 'de': 'Bahía Petempich gehört zur Gemeinde Puerto Morelos, seit 2016 eigenständig, und liegt im Einflussbereich des Nationalparks Riff von Puerto Morelos. Dort werden Nutzungsart und Baugenehmigung mit DRO bearbeitet; am Strand gelten die ZOFEMAT-Konzession und praktisch immer eine Umweltgenehmigung, mit Auflagen zu Rodung, Abfluss, strandseitiger Beleuchtung und Abwasserbehandlung. Hier bestimmt die Umweltakte den gesamten Bauzeitplan.',
 'fr': 'Bahía Petempich relève de la commune de Puerto Morelos, indépendante depuis 2016, et se situe dans la zone d’influence du Parc National du Récif de Puerto Morelos. L’usage du sol et le permis avec DRO s’y traitent ; en front de mer s’appliquent la concession ZOFEMAT et, en pratique, toujours une autorisation environnementale, assortie de conditions sur le défrichement, le ruissellement, l’éclairage vers la plage et le traitement des eaux usées. C’est une zone où le dossier environnemental commande tout le calendrier du chantier.',
 'zh': 'Bahía Petempich 隶属 Puerto Morelos 市（2016年独立设市），并位于 Puerto Morelos 珊瑚礁国家公园的影响范围内。土地用途与带 DRO 的施工许可在该市办理；海滨地块需 ZOFEMAT 特许，且实务中必然需要环保许可，并对清林、径流、朝向沙滩的照明与污水处理提出条件。在这一带，环保审批进度直接决定整个施工日程。'},
}
SOIL_OVR = {
'punta-maroma': {
 'es': 'Duna costera sobre roca caliza: la cota de desplante, el respeto a la vegetación de duna y el manejo del escurrimiento son tan importantes como la capacidad de carga. Especificación marina completa en toda la obra —recubrimientos mayores, acero protegido, cancelería anodizada, vidrio para huracanes e impermeabilización reforzada— porque la exposición aquí es directa, sin nada que frene el viento salino.',
 'en': 'Coastal dune over limestone: the finished floor level, respecting dune vegetation and managing runoff matter as much as bearing capacity. Full marine spec across the build — greater cover, protected rebar, anodised joinery, hurricane-rated glazing and reinforced waterproofing — because exposure here is direct, with nothing to break the salt wind.',
 'ru': 'Прибрежная дюна на известняке: отметка пола, сохранение дюнной растительности и управление стоком здесь важны не меньше несущей способности. Полная морская спецификация по всему объекту — увеличенный защитный слой, защищённая арматура, анодированный алюминий, ударопрочное остекление под ураганы и усиленная гидроизоляция, — потому что экспозиция прямая и солёный ветер ничем не задерживается.',
 'de': 'Küstendüne über Kalkstein: Höhenlage des Erdgeschosses, Erhalt der Dünenvegetation und Abflussmanagement sind hier so wichtig wie die Tragfähigkeit. Volle Meeresspezifikation im gesamten Bau — größere Deckung, geschützte Bewehrung, eloxierte Fenster, hurrikanfeste Verglasung und verstärkte Abdichtung — denn die Exposition ist direkt, nichts bremst den Salzwind.',
 'fr': 'Dune côtière sur calcaire : le niveau du plancher, le respect de la végétation dunaire et la gestion du ruissellement comptent autant que la portance. Spécification marine complète sur tout le chantier — enrobages renforcés, aciers protégés, menuiseries anodisées, vitrages anticycloniques et étanchéité renforcée — car l’exposition est directe, rien ne freine le vent salin.',
 'zh': '石灰岩之上的滨海沙丘：首层标高、沙丘植被保留与径流管理，其重要性不亚于地基承载力。全项目采用完整海洋环境标准——加大保护层、钢筋防护、阳极氧化门窗、抗飓风玻璃与加强防水——因为此处直面海风，没有任何屏障可以削弱盐雾侵蚀。'},
'bahia-petempich': {
 'es': 'Caliza costera con manto freático muy somero frente al arrecife. El estudio de mecánica de suelos define cimentación y cota de desplante, y el diseño se hace con recubrimientos y aditivos para ambiente marino. El drenaje se resuelve con planta de tratamiento o biodigestor —nunca fosa simple— porque cualquier descarga mal resuelta llega al arrecife.',
 'en': 'Coastal limestone with a very shallow water table facing the reef. The soil study sets the foundation and the finished floor level, and the structure is designed with marine-grade cover and admixtures. Drainage is solved with a treatment plant or biodigester — never a simple septic pit — because any badly resolved discharge reaches the reef.',
 'ru': 'Прибрежный известняк с очень высоким уровнем грунтовых вод напротив рифа. Геология определяет фундамент и отметку пола, а конструктив считается с защитным слоем и добавками под морскую среду. Канализация — очистные или биодигестер, никогда простая яма, потому что любой неправильный сброс доходит до рифа.',
 'de': 'Küstenkalkstein mit sehr hohem Grundwasserstand gegenüber dem Riff. Das Bodengutachten legt Gründung und Höhenlage fest, die Struktur wird mit meerwassertauglicher Deckung und Zusatzmitteln geplant. Die Entwässerung erfolgt über Kläranlage oder Biodigester — nie über eine einfache Sickergrube —, denn jede schlecht gelöste Einleitung erreicht das Riff.',
 'fr': 'Calcaire côtier avec nappe très affleurante face au récif. L’étude de sol fixe les fondations et le niveau du plancher, et la structure est calculée avec enrobages et adjuvants qualité marine. L’assainissement passe par station ou biodigesteur — jamais une simple fosse — car tout rejet mal traité atteint le récif.',
 'zh': '正对珊瑚礁的滨海石灰岩，地下水位极浅。土力学勘察确定基础形式与首层标高，结构按海洋环境标准配置保护层与外加剂。排水采用处理设备或生物消化池，绝不可用简易化粪坑，因为任何处理不当的排放都会流向珊瑚礁。'},
'xpu-ha': {
 'es': 'Roca caliza con cavidades y manto freático somero, típica de la costa: el estudio de mecánica de suelos define si la cimentación va con zapatas, losa o pilotes. Al estar cerca del mar se aplica protección anticorrosiva en acero y herrería, y en lotes de playa se refuerza la impermeabilización y se revisa la cota de desplante por escurrimientos.',
 'en': 'Limestone with cavities and a shallow water table, typical of the coast: the soil study decides between footings, a mat foundation or piles. Being close to the sea, rebar and ironwork get anti-corrosion protection, and on beach lots waterproofing is reinforced and the floor level checked against runoff.',
 'ru': 'Известняк с пустотами и высоким уровнем грунтовых вод — типично для побережья: геология определяет, будет ли фундамент на зап, плите или сваях. Из-за близости моря арматура и металл получают антикоррозийную защиту, а на пляжных участках усиливается гидроизоляция и проверяется отметка пола по стоку.',
 'de': 'Kalkstein mit Hohlräumen und hohem Grundwasserstand, typisch für die Küste: Das Bodengutachten entscheidet zwischen Streifenfundament, Bodenplatte oder Pfählen. Wegen der Meeresnähe erhalten Bewehrung und Schlosserarbeiten Korrosionsschutz; bei Strandgrundstücken wird die Abdichtung verstärkt und die Höhenlage am Abfluss geprüft.',
 'fr': 'Calcaire avec cavités et nappe peu profonde, typique de la côte : l’étude de sol tranche entre semelles, radier ou pieux. La proximité de la mer impose une protection anticorrosion des aciers et de la ferronnerie ; sur les lots de plage, l’étanchéité est renforcée et le niveau du plancher vérifié au regard du ruissellement.',
 'zh': '带溶洞的石灰岩、地下水位较浅，是海岸典型地层：土力学勘察据此确定采用条形基础、筏板还是桩基。因临近海边，钢筋与铁件均做防腐处理；海滩地块需加强防水，并结合径流复核首层标高。'},
}

FAQ4 = {
'selvazama': {
 'es': [('¿Qué ventaja tiene Selvazama frente a otras zonas de Tulum?', 'La urbanización terminada: agua, electricidad, drenaje, fibra óptica y calles de concreto ya construidas. Se ahorra el riesgo de factibilidad de servicios que sí existe en zonas en desarrollo como La Veleta.'),
        ('¿Sigue aplicando el trámite ambiental?', 'Sí. Selvazama está en el municipio de Tulum, así que la licencia municipal con DRO y, en la mayoría de los casos, la autorización ambiental estatal siguen siendo parte del calendario.')],
 'en': [('What is the advantage of Selvazama over other Tulum areas?', 'Finished urbanisation: water, power, drainage, fibre and concrete streets already built. It removes the utility feasibility risk that still exists in developing areas such as La Veleta.'),
        ('Does the environmental process still apply?', 'Yes. Selvazama is in the municipality of Tulum, so the municipal licence with a DRO and, in most cases, the state environmental authorisation remain part of the schedule.')],
 'ru': [('В чём преимущество Сельвасамы перед другими районами Тулума?', 'Готовая урбанизация: вода, электричество, канализация, оптика и бетонные улицы уже построены. Снимается риск по подключениям, который остаётся в развивающихся районах вроде Ла-Велеты.'),
        ('Экологическая процедура всё равно нужна?', 'Да. Сельвасама в муниципалитете Тулум, поэтому муниципальная лицензия с DRO и, в большинстве случаев, экологическое разрешение штата остаются частью календаря.')],
 'de': [('Welchen Vorteil bietet Selvazama gegenüber anderen Lagen in Tulum?', 'Die fertige Erschließung: Wasser, Strom, Kanalisation, Glasfaser und Betonstraßen sind bereits gebaut. Das nimmt das Erschließungsrisiko, das in wachsenden Vierteln wie La Veleta weiter besteht.'),
        ('Gilt das Umweltverfahren trotzdem?', 'Ja. Selvazama liegt in der Gemeinde Tulum, die kommunale Lizenz mit DRO und meist die staatliche Umweltgenehmigung bleiben Teil des Terminplans.')],
 'fr': [('Quel est l’avantage de Selvazama sur les autres secteurs de Tulum ?', 'La viabilisation achevée : eau, électricité, assainissement, fibre et voiries béton déjà réalisés. Cela supprime le risque de faisabilité des réseaux qui subsiste dans les secteurs en développement comme La Veleta.'),
        ('La procédure environnementale s’applique-t-elle encore ?', 'Oui. Selvazama est en commune de Tulum : le permis municipal avec DRO et, dans la plupart des cas, l’autorisation environnementale de l’État font toujours partie du calendrier.')],
 'zh': [('相比图卢姆其他片区，Selvazama 优势何在？', '在于市政配套已完成：供水、供电、排水、光纤与混凝土道路均已建成，可规避 La Veleta 等在建片区仍存在的接入可行性风险。'),
        ('环保流程还需要办吗？', '需要。Selvazama 属图卢姆市辖，带 DRO 的市政许可以及多数情形下的州级环保许可，仍是进度计划的一部分。')]},
'punta-maroma': {
 'es': [('¿Cuánta altura puedo construir en Punta Maroma?', 'La zonificación turístico-hotelera de la zona limita a 3 niveles o 15 metros. El uso de suelo se verifica lote por lote antes de comprar: no todos los predios admiten el mismo programa.'),
        ('¿Por qué los permisos tardan más aquí?', 'Porque el expediente ambiental es el eje: duna, vegetación costera y arrecife. Se resuelve con proyecto ajustado a la norma desde el inicio y trámite iniciado en paralelo al diseño, no después.')],
 'en': [('How tall can I build at Punta Maroma?', 'The area’s hotel/tourism zoning caps it at 3 levels or 15 metres. Land use is verified lot by lot before you buy: not every parcel allows the same programme.'),
        ('Why do permits take longer here?', 'Because the environmental file is the centrepiece: dune, coastal vegetation and reef. It is handled with a design that fits the rules from the start and a process launched in parallel with design, not after it.')],
 'ru': [('Какую высоту можно строить в Пунта-Мароме?', 'Туристско-гостиничное зонирование ограничивает 3 уровнями или 15 метрами. Назначение земли проверяем по каждому лоту до покупки: не все участки допускают одинаковую программу.'),
        ('Почему разрешения здесь дольше?', 'Потому что экологическое досье — стержень процесса: дюна, прибрежная растительность, риф. Решается проектом, изначально подогнанным под норму, и процедурой, запущенной параллельно проектированию, а не после.')],
 'de': [('Wie hoch darf ich in Punta Maroma bauen?', 'Die Hotel-/Tourismuszonierung begrenzt auf 3 Ebenen bzw. 15 Meter. Die Nutzungsart wird vor dem Kauf Grundstück für Grundstück geprüft — nicht jedes Grundstück lässt dasselbe Programm zu.'),
        ('Warum dauern die Genehmigungen hier länger?', 'Weil die Umweltakte im Zentrum steht: Düne, Küstenvegetation, Riff. Gelöst wird das mit einem von Anfang an normkonformen Entwurf und einem Verfahren, das parallel zur Planung startet — nicht danach.')],
 'fr': [('Quelle hauteur puis-je construire à Punta Maroma ?', 'Le zonage hôtelier-touristique limite à 3 niveaux ou 15 mètres. L’usage du sol se vérifie lot par lot avant l’achat : tous les terrains n’autorisent pas le même programme.'),
        ('Pourquoi les permis sont-ils plus longs ici ?', 'Parce que le dossier environnemental est central : dune, végétation côtière et récif. On le traite avec un projet conforme dès le départ et une procédure lancée en parallèle de la conception, pas après.')],
 'zh': [('在 Punta Maroma 可以建多高？', '该片区的旅游酒店类规划限制为3层或15米。购地前须逐地块核实土地用途：并非所有地块都允许相同的开发内容。'),
        ('为什么这里许可周期更长？', '因为环保申报是核心：沙丘、海岸植被与珊瑚礁。解决之道是方案从一开始就合规，并让报批与设计并行推进，而不是设计完再办。')]},
'xpu-ha': {
 'es': [('¿Xpu-Há ya cuenta con servicios?', 'Sí, en los fraccionamientos privados: agua, electricidad, drenaje y calles de concreto hidráulico dentro del desarrollo. Aun así verificamos factibilidad y situación legal del lote antes de que usted compre.'),
        ('¿Cuánto cuesta construir en Xpu-Há?', 'De $14,600 a $30,500 MXN por m² según acabados. Sale por debajo de Tulum y Puerto Aventuras manteniendo playa, servicios completos y tiempos de permiso de Solidaridad.')],
 'en': [('Does Xpu-Há already have utilities?', 'Yes, inside the private communities: water, power, drainage and hydraulic concrete streets within the development. We still verify feasibility and the legal status of the lot before you buy.'),
        ('How much does it cost to build in Xpu-Há?', 'From $14,600 to $30,500 MXN per m² depending on finishes. It lands below Tulum and Puerto Aventuras while keeping the beach, full services and Solidaridad permit timelines.')],
 'ru': [('В Шпу-Ха уже есть коммуникации?', 'Да, в частных секторах: вода, электричество, канализация и улицы из гидравлического бетона внутри застройки. Тем не менее до покупки проверяем факт подключения и юридический статус участка.'),
        ('Сколько стоит стройка в Шпу-Ха?', 'От $14,600 до $30,500 MXN за м² в зависимости от отделки. Дешевле Тулума и Пуэрто-Авентурас при сохранении пляжа, полных коммуникаций и сроков разрешений Solidaridad.')],
 'de': [('Gibt es in Xpu-Há bereits Versorgung?', 'Ja, innerhalb der privaten Anlagen: Wasser, Strom, Kanalisation und Straßen aus Hydraulikbeton. Wir prüfen dennoch Anschlussfähigkeit und Rechtslage des Grundstücks vor dem Kauf.'),
        ('Was kostet Bauen in Xpu-Há?', 'Von $14.600 bis $30.500 MXN pro m² je nach Ausbau. Günstiger als Tulum und Puerto Aventuras, bei Strandlage, voller Erschließung und den Genehmigungszeiten von Solidaridad.')],
 'fr': [('Xpu-Há dispose-t-il déjà des réseaux ?', 'Oui, dans les résidences privées : eau, électricité, assainissement et voiries en béton hydraulique au sein du développement. Nous vérifions tout de même la faisabilité et la situation juridique du terrain avant l’achat.'),
        ('Combien coûte la construction à Xpu-Há ?', 'De 14 600 à 30 500 MXN le m² selon les finitions. Cela reste sous Tulum et Puerto Aventuras tout en gardant la plage, des réseaux complets et les délais de permis de Solidaridad.')],
 'zh': [('Xpu-Há 已经有市政配套了吗？', '在私人社区内是的：开发区内配有供水、供电、排水与水硬性混凝土道路。即便如此，我们仍会在您购地前核实接入可行性与地块法律状态。'),
        ('在 Xpu-Há 建房要多少钱？', '按装修标准，每平方米 14,600 至 30,500 比索。低于图卢姆与 Puerto Aventuras，同时兼具海滩、完整配套与 Solidaridad 的许可周期。')]},
'bahia-petempich': {
 'es': [('¿Qué municipio y qué permisos aplican en Bahía Petempich?', 'Puerto Morelos, municipio propio desde 2016: uso de suelo y licencia con DRO ahí, ZOFEMAT en frente de playa y autorización ambiental prácticamente siempre, por el Parque Nacional Arrecife.'),
        ('¿Qué debo prever por estar frente al arrecife?', 'Planta de tratamiento o biodigestor, control de escurrimientos durante la obra, iluminación que no invada la playa y manejo documentado de residuos. Se planea desde el anteproyecto, no como parche final.')],
 'en': [('Which municipality and permits apply at Petempich Bay?', 'Puerto Morelos, its own municipality since 2016: land use and the licence with a DRO there, ZOFEMAT on the beachfront and, in practice, always an environmental authorisation because of the Reef National Park.'),
        ('What should I plan for facing the reef?', 'A treatment plant or biodigester, runoff control during construction, lighting that does not spill onto the beach and documented waste handling. It is planned at concept stage, not patched at the end.')],
 'ru': [('Какой муниципалитет и какие разрешения в Баия-Петемпич?', 'Пуэрто-Морелос, самостоятельный муниципалитет с 2016 года: назначение земли и лицензия с DRO там, ZOFEMAT на первой линии и практически всегда экологическое разрешение — из-за Национального парка «Риф».'),
        ('Что учесть, находясь напротив рифа?', 'Очистные или биодигестер, контроль стока во время стройки, освещение, не выходящее на пляж, и документированный вывоз отходов. Планируется на стадии эскиза, а не заплаткой в конце.')],
 'de': [('Welche Gemeinde und welche Genehmigungen gelten in Bahía Petempich?', 'Puerto Morelos, seit 2016 eigene Gemeinde: Nutzungsart und Lizenz mit DRO dort, ZOFEMAT am Strand und praktisch immer eine Umweltgenehmigung wegen des Riff-Nationalparks.'),
        ('Was ist gegenüber dem Riff einzuplanen?', 'Kläranlage oder Biodigester, Abflusskontrolle während des Baus, Beleuchtung, die nicht auf den Strand strahlt, und dokumentierte Abfallentsorgung. Das wird im Entwurf geplant, nicht am Ende nachgebessert.')],
 'fr': [('Quelle commune et quels permis à Bahía Petempich ?', 'Puerto Morelos, commune à part entière depuis 2016 : usage du sol et permis avec DRO sur place, ZOFEMAT en front de mer et, en pratique, toujours une autorisation environnementale du fait du Parc National du Récif.'),
        ('Que prévoir face au récif ?', 'Station de traitement ou biodigesteur, contrôle des ruissellements pendant le chantier, éclairage qui ne déborde pas sur la plage et gestion documentée des déchets. Cela se planifie dès l’avant-projet, pas en rattrapage.')],
 'zh': [('Bahía Petempich 涉及哪个市政与哪些许可？', 'Puerto Morelos 市（2016年独立设市）：土地用途与带 DRO 的许可在该市办理，海滨需 ZOFEMAT，且因珊瑚礁国家公园，实务中必然还需环保许可。'),
        ('正对珊瑚礁需要提前考虑什么？', '污水处理设备或生物消化池、施工期径流控制、不外溢至沙滩的照明方案，以及可追溯的废弃物处理。这些在方案阶段就要规划，而不是收尾时补救。')]},
}

LINKS4 = {
 'es': {'selvazama': [('/construccion-de-casas-aldea-zama/','Construcción de casas en Aldea Zamá'), ('/construccion-de-casas-tulum/','Construcción de casas en Tulum'), ('/constructora-tulum/','Constructora en Tulum'), ('/calculadora/','Calculadora de costos')],
        'punta-maroma': [('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/villas-de-lujo-playa-del-carmen/','Villas de lujo'), ('/construccion-de-casas-mayakoba/','Construcción de casas en Mayakoba'), ('/calculadora/','Calculadora de costos')],
        'xpu-ha': [('/construccion-de-casas-puerto-aventuras/','Construcción de casas en Puerto Aventuras'), ('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/constructora-puerto-aventuras/','Constructora en Puerto Aventuras'), ('/calculadora/','Calculadora de costos')],
        'bahia-petempich': [('/construccion-de-casas-punta-brava/','Construcción de casas en Punta Brava'), ('/constructora-puerto-morelos/','Constructora en Puerto Morelos'), ('/permisos-de-construccion-puerto-morelos/','Permisos en Puerto Morelos'), ('/calculadora/','Calculadora de costos')]},
 'en': {'selvazama': [('/house-construction-aldea-zama/','House construction in Aldea Zamá'), ('/house-construction-tulum/','House construction in Tulum'), ('/construction-company-tulum/','Construction company in Tulum'), ('/calculator/','Cost calculator')],
        'punta-maroma': [('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/luxury-villa-construction-playa-del-carmen/','Luxury villas'), ('/house-construction-mayakoba/','House construction in Mayakoba'), ('/calculator/','Cost calculator')],
        'xpu-ha': [('/house-construction-puerto-aventuras/','House construction in Puerto Aventuras'), ('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/construction-company-puerto-aventuras/','Construction company in Puerto Aventuras'), ('/calculator/','Cost calculator')],
        'bahia-petempich': [('/house-construction-punta-brava/','House construction in Punta Brava'), ('/construction-company-puerto-morelos/','Construction company in Puerto Morelos'), ('/construction-permits-puerto-morelos/','Permits in Puerto Morelos'), ('/calculator/','Cost calculator')]},
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
    LINKS4[_lang] = {}
    for _z, _d in ZONE4.items():
        LINKS4[_lang][_z] = [
            ('/%s-%s/' % (_pref, _d['parent']), '%s — %s' % (hub, ml.CITY[_lang][_d['parent']])),
            perm,
            ('/%s-riviera-maya/' % _pref, '%s — %s' % (hub, ml.CITY[_lang]['riviera-maya'])),
            (_calc, names[0]), (_blog, names[1])]


def _set_parent_urls(locs):
    P = {'es':'construccion-de-casas','en':'house-construction','ru':'stroitelstvo-domov','de':'hausbau','fr':'construction-de-maisons','zh':'zhuzhai-jianzao'}
    ml.OVR.setdefault('parent_url', {})
    for zk, d in locs.items():
        for l in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            ml.OVR['parent_url'].setdefault(zk, {})[l] = '/%s-%s/' % (P[l], d['parent'])


if __name__ == '__main__':
    _set_parent_urls(ZONE4)
    for z in ZONE4:
        z1.ZAREA[z] = AREAS[z]
        z1.ZTEXT[z] = TEXT[z]
        z1.ZFAQ[z] = FAQ4[z]
    for lang in LINKS4:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS4[lang])
    for z, d in ZONE4.items():
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
        for lang, txt in NORM_OVR.get(z, {}).items():
            ml.NORM[lang][z] = txt
        for lang, txt in SOIL_OVR.get(z, {}).items():
            ml.SOIL[lang][z] = txt
    ml.LOCS.extend(ZONE4)
    for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
        ch = ml.chrome(lang)
        for z in ZONE4:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-44s %6d bytes' % (out + '/', len(html)))
