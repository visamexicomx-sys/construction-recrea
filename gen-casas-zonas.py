#!/usr/bin/env python3
"""Luxury-zone pages of the house-construction cluster, in all 6 languages.

Extends gen-construccion-casas-ml.py with premium communities instead of towns:
Playacar, Mayakoba, Corasol (Solidaridad), Aldea Zamá, La Veleta, Tulum Country
Club (Tulum) and Puerto Cancún, Zona Hotelera (Benito Juárez).

Municipal rules and soil come from the parent town (same authority), the zone
paragraph + zone FAQ + price tier are what make each page its own: design
committee, HOA, golf/beachfront specifics and the premium m² band.

Angle stays "obra nueva paso a paso" so these do not collide with the existing
villas-de-lujo-[zone] / luxury-villas-[zone] product pages.
"""
import importlib.util, os, re, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
ml = load('gen-construccion-casas-ml.py', 'ml')
esg = load('gen-construccion-casas.py', 'esg')

MXN_USD = 18.1
# zone -> parent town, price factor vs parent, permit months
ZONE = {
 'playacar':             dict(parent='playa-del-carmen', f=1.25, perm='2–4'),
 'mayakoba':             dict(parent='playa-del-carmen', f=1.42, perm='3–5'),
 'corasol':              dict(parent='playa-del-carmen', f=1.30, perm='2–4'),
 'aldea-zama':           dict(parent='tulum',            f=1.20, perm='3–5'),
 'la-veleta':            dict(parent='tulum',            f=1.10, perm='3–5'),
 'tulum-country-club':   dict(parent='tulum',            f=1.13, perm='3–5'),
 'puerto-cancun':        dict(parent='cancun',           f=1.25, perm='3–5'),
 'zona-hotelera-cancun': dict(parent='cancun',           f=1.30, perm='3–5'),
}

ZNAME = {
 'es': {'playacar': 'Playacar', 'mayakoba': 'Mayakoba', 'corasol': 'Corasol', 'aldea-zama': 'Aldea Zamá',
        'la-veleta': 'La Veleta', 'tulum-country-club': 'Tulum Country Club', 'puerto-cancun': 'Puerto Cancún',
        'zona-hotelera-cancun': 'la Zona Hotelera de Cancún'},
 'en': {'playacar': 'Playacar', 'mayakoba': 'Mayakoba', 'corasol': 'Corasol', 'aldea-zama': 'Aldea Zamá',
        'la-veleta': 'La Veleta', 'tulum-country-club': 'Tulum Country Club', 'puerto-cancun': 'Puerto Cancún',
        'zona-hotelera-cancun': 'the Cancún Hotel Zone'},
 'ru': {'playacar': 'Плаякаре', 'mayakoba': 'Майякобе', 'corasol': 'Корасоле', 'aldea-zama': 'Альдеа-Зама',
        'la-veleta': 'Ла-Велете', 'tulum-country-club': 'Tulum Country Club', 'puerto-cancun': 'Пуэрто-Канкун',
        'zona-hotelera-cancun': 'Отельной зоне Канкуна'},
 'de': {'playacar': 'Playacar', 'mayakoba': 'Mayakoba', 'corasol': 'Corasol', 'aldea-zama': 'Aldea Zamá',
        'la-veleta': 'La Veleta', 'tulum-country-club': 'Tulum Country Club', 'puerto-cancun': 'Puerto Cancún',
        'zona-hotelera-cancun': 'der Hotelzone von Cancún'},
 'fr': {'playacar': 'Playacar', 'mayakoba': 'Mayakoba', 'corasol': 'Corasol', 'aldea-zama': 'Aldea Zamá',
        'la-veleta': 'La Veleta', 'tulum-country-club': 'Tulum Country Club', 'puerto-cancun': 'Puerto Cancún',
        'zona-hotelera-cancun': 'la Zone Hôtelière de Cancún'},
 'zh': {'playacar': 'Playacar', 'mayakoba': 'Mayakoba', 'corasol': 'Corasol', 'aldea-zama': 'Aldea Zamá',
        'la-veleta': 'La Veleta', 'tulum-country-club': 'Tulum Country Club', 'puerto-cancun': 'Puerto Cancún',
        'zona-hotelera-cancun': '坎昆酒店区'},
}
# sub-areas used in the intro sentence
ZAREA = {
 'playacar': {'es': 'Playacar Fase I y Fase II', 'en': 'Playacar Phase I and Phase II', 'ru': 'Плаякар Фаза I и Фаза II',
              'de': 'Playacar Phase I und Phase II', 'fr': 'Playacar Phase I et Phase II', 'zh': 'Playacar 一期与二期'},
 'mayakoba': {'es': 'las residencias privadas de Mayakoba y su entorno de lagunas', 'en': 'the private residences of Mayakoba and its lagoon setting',
              'ru': 'частных резиденциях Майякобы и лагунной зоне', 'de': 'den privaten Residenzen von Mayakoba und der Lagunenlandschaft',
              'fr': 'les résidences privées de Mayakoba et son cadre lagunaire', 'zh': 'Mayakoba 私人住宅区及其泻湖环境'},
 'corasol': {'es': 'Corasol y sus secciones residenciales de golf', 'en': 'Corasol and its residential golf sections',
             'ru': 'Корасоле и его гольф-секциях', 'de': 'Corasol und seinen Golf-Wohnabschnitten',
             'fr': 'Corasol et ses sections résidentielles de golf', 'zh': 'Corasol 及其高尔夫住宅区'},
 'aldea-zama': {'es': 'Aldea Zamá y sus secciones residenciales', 'en': 'Aldea Zamá and its residential sections',
                'ru': 'Альдеа-Зама и её жилых секциях', 'de': 'Aldea Zamá und seinen Wohnabschnitten',
                'fr': 'Aldea Zamá et ses sections résidentielles', 'zh': 'Aldea Zamá 及其住宅区段'},
 'la-veleta': {'es': 'La Veleta y sus manzanas en desarrollo', 'en': 'La Veleta and its developing blocks',
               'ru': 'Ла-Велете и её застраивающихся кварталах', 'de': 'La Veleta und seinen wachsenden Blöcken',
               'fr': 'La Veleta et ses îlots en développement', 'zh': 'La Veleta 及其在建街区'},
 'tulum-country-club': {'es': 'Tulum Country Club y las zonas residenciales de golf de Tulum', 'en': 'Tulum Country Club and Tulum’s golf residential areas',
                        'ru': 'Tulum Country Club и гольф-районах Тулума', 'de': 'Tulum Country Club und den Golf-Wohngebieten von Tulum',
                        'fr': 'Tulum Country Club et les quartiers résidentiels de golf de Tulum', 'zh': 'Tulum Country Club 及图卢姆高尔夫住宅区'},
 'puerto-cancun': {'es': 'Puerto Cancún, su marina y sus fraccionamientos privados', 'en': 'Puerto Cancún, its marina and private phases',
                   'ru': 'Пуэрто-Канкуне, его марине и частных секторах', 'de': 'Puerto Cancún, seiner Marina und den privaten Abschnitten',
                   'fr': 'Puerto Cancún, sa marina et ses tranches privées', 'zh': 'Puerto Cancún、其码头与各私人区段'},
 'zona-hotelera-cancun': {'es': 'la Zona Hotelera, Isla Dorada y Punta Nizuc', 'en': 'the Hotel Zone, Isla Dorada and Punta Nizuc',
                          'ru': 'Отельной зоне, Исла-Дорада и Пунта-Нисук', 'de': 'der Hotelzone, Isla Dorada und Punta Nizuc',
                          'fr': 'la Zone Hôtelière, Isla Dorada et Punta Nizuc', 'zh': '酒店区、Isla Dorada 与 Punta Nizuc'},
}

# zone paragraph (replaces the town "extra" paragraph)
ZTEXT = {
'playacar': {
 'es': 'Playacar es un fraccionamiento cerrado con campo de golf, playa privada y vigilancia, y uno de los reglamentos de diseño más estrictos de la Riviera Maya: alturas, retiros, cubiertas y hasta la paleta de colores se aprueban en comité antes de que el municipio reciba nada. Quedan pocos lotes, casi todos de reposición, por eso aquí el proyecto se calcula al centímetro. En lotes frente al mar aplica además concesión ZOFEMAT.',
 'en': 'Playacar is a gated community with a golf course, private beach and security, and one of the strictest design codes on the Riviera Maya: heights, setbacks, roof types and even the colour palette are approved by committee before the municipality sees anything. Very few lots remain, almost all resales, so the design is worked out to the centimetre. Beachfront lots also require a ZOFEMAT concession.',
 'ru': 'Плаякар — закрытый посёлок с полем для гольфа, приватным пляжем и охраной и один из самых строгих регламентов застройки на Ривьере-Майя: высоты, отступы, тип кровли и даже палитра цветов утверждаются комитетом до того, как документы уйдут в муниципалитет. Свободных участков почти не осталось, в основном перепродажа, поэтому проект считается до сантиметра. На первой линии дополнительно нужна концессия ZOFEMAT.',
 'de': 'Playacar ist eine geschlossene Anlage mit Golfplatz, Privatstrand und Bewachung — und mit einer der strengsten Gestaltungssatzungen der Riviera Maya: Höhen, Abstände, Dachformen und sogar die Farbpalette genehmigt der Beirat, bevor die Gemeinde überhaupt etwas sieht. Es sind kaum noch Grundstücke frei, fast nur Wiederverkäufe, deshalb wird hier zentimetergenau geplant. Strandgrundstücke brauchen zusätzlich eine ZOFEMAT-Konzession.',
 'fr': 'Playacar est une résidence fermée avec golf, plage privée et sécurité, dotée d’un des règlements architecturaux les plus stricts de la Riviera Maya : hauteurs, reculs, types de toiture et jusqu’à la palette de couleurs passent en comité avant même la mairie. Il reste très peu de terrains, presque tous en revente, d’où un projet calé au centimètre. Les lots en front de mer exigent en plus une concession ZOFEMAT.',
 'zh': 'Playacar 是配有高尔夫球场、私人海滩与安保的封闭社区，也是里维埃拉玛雅设计规约最严格的社区之一：高度、退线、屋面形式乃至色彩方案都须先经委员会批准，之后才递交市政。可售地块所剩无几，多为二手转售，因此方案必须精确到厘米。海滨地块另需 ZOFEMAT 特许。'},
'mayakoba': {
 'es': 'Mayakoba es el escalón más alto de precio por m² de la costa: residencias privadas dentro de un complejo de resorts y campo de golf PGA, con comité de diseño propio y control ambiental serio por las lagunas y el manglar. La logística de obra está regulada —accesos, horarios, proveedores autorizados, manejo de residuos— y eso se refleja tanto en el estándar de acabados como en el costo por m².',
 'en': 'Mayakoba is the top price tier per m² on the coast: private residences inside a resort and PGA golf complex, with its own design committee and serious environmental control because of the lagoons and mangrove. Construction logistics are regulated — access, working hours, approved suppliers, waste handling — and that shows both in the finish standard and in the cost per m².',
 'ru': 'Майякоба — верхняя ценовая планка по стоимости м² на побережье: частные резиденции внутри курортного комплекса с полем PGA, собственный комитет по дизайну и серьёзный экологический контроль из-за лагун и мангров. Логистика стройки регламентирована — доступ, часы работ, допущенные поставщики, вывоз отходов — и это отражается и на стандарте отделки, и на цене за м².',
 'de': 'Mayakoba ist die höchste Preisstufe pro m² an der Küste: private Residenzen innerhalb einer Resort- und PGA-Golfanlage, mit eigenem Gestaltungsbeirat und strengem Umweltcontrolling wegen Lagunen und Mangroven. Die Baulogistik ist reguliert — Zufahrt, Arbeitszeiten, zugelassene Lieferanten, Abfallentsorgung — und das zeigt sich im Ausbaustandard wie im m²-Preis.',
 'fr': 'Mayakoba représente le haut de gamme absolu au m² sur la côte : des résidences privées au sein d’un complexe de resorts et d’un golf PGA, avec son propre comité d’architecture et un contrôle environnemental sérieux à cause des lagunes et de la mangrove. La logistique de chantier est encadrée — accès, horaires, fournisseurs agréés, gestion des déchets — ce qui se retrouve dans le standard de finition comme dans le coût au m².',
 'zh': 'Mayakoba 是海岸线上每平方米价格最高的一档：位于度假村与 PGA 高尔夫球场之内的私人住宅，设有自己的设计委员会，并因泻湖与红树林而实行严格的环境管控。施工物流受统一规范——进出通道、作业时段、指定供应商、废弃物处理——这既体现在装修标准上，也体现在每平方米造价上。'},
'corasol': {
 'es': 'Corasol es la comunidad de golf de Playa del Carmen: lotes amplios, lineamientos de diseño del desarrollo y un entorno pensado para casa habitación permanente más que para renta corta. Nuestra oficina está en Corasol, así que la supervisión aquí es diaria y la coordinación con la administración del desarrollo es directa.',
 'en': 'Corasol is Playa del Carmen’s golf community: generous lots, developer design guidelines and an environment built for permanent living rather than short-term rental. Our office is in Corasol, so supervision here is daily and coordination with the estate management is direct.',
 'ru': 'Корасоль — гольф-комьюнити Плая-дель-Кармен: просторные участки, дизайн-регламент застройщика и среда, рассчитанная скорее на постоянное проживание, чем на посуточную аренду. Наш офис находится в Корасоле, поэтому надзор здесь ежедневный, а согласование с администрацией — напрямую.',
 'de': 'Corasol ist die Golf-Community von Playa del Carmen: großzügige Grundstücke, Gestaltungsrichtlinien des Entwicklers und ein Umfeld, das eher auf dauerhaftes Wohnen als auf Kurzzeitvermietung ausgelegt ist. Unser Büro liegt in Corasol, die Bauüberwachung erfolgt hier täglich und die Abstimmung mit der Verwaltung direkt.',
 'fr': 'Corasol est la communauté de golf de Playa del Carmen : grands terrains, lignes directrices architecturales du promoteur et un cadre pensé pour la résidence permanente plus que pour la location courte. Notre bureau se trouve à Corasol : la supervision y est quotidienne et la coordination avec l’administration se fait en direct.',
 'zh': 'Corasol 是普拉亚德尔卡门的高尔夫社区：地块宽阔，开发商设有设计导则，整体环境更适合长期居住而非短租。我们的办公室就在 Corasol，因此这里的现场监理是每日进行，与社区管理方的协调也是直接对接。'},
'aldea-zama': {
 'es': 'Aldea Zamá es la zona premium urbanizada de Tulum: servicios subterráneos, calles terminadas y la mayor demanda de renta vacacional de la ciudad. El estilo dominante es eco-chic —chukum, madera dura, ventilación cruzada— y el trámite ambiental de SEMA es prácticamente obligatorio, así que el calendario de permisos manda sobre el de obra.',
 'en': 'Aldea Zamá is Tulum’s urbanised premium zone: underground services, finished streets and the city’s strongest vacation-rental demand. The dominant style is eco-chic — chukum, hardwood, cross ventilation — and SEMA environmental processing is effectively mandatory, so the permit calendar drives the construction calendar.',
 'ru': 'Альдеа-Зама — премиальный урбанизированный район Тулума: подземные коммуникации, готовые улицы и самый высокий в городе спрос на посуточную аренду. Доминирует эко-шик — чукум, твёрдая древесина, сквозная вентиляция, — а экологическая процедура SEMA практически обязательна, поэтому календарь разрешений задаёт календарь стройки.',
 'de': 'Aldea Zamá ist die erschlossene Premiumzone von Tulum: unterirdische Versorgung, fertige Straßen und die höchste Nachfrage nach Ferienvermietung der Stadt. Der prägende Stil ist Eco-Chic — Chukum, Hartholz, Querlüftung — und das SEMA-Umweltverfahren ist faktisch Pflicht, weshalb der Genehmigungskalender den Bauzeitplan bestimmt.',
 'fr': 'Aldea Zamá est la zone premium urbanisée de Tulum : réseaux enterrés, rues finies et la plus forte demande de location saisonnière de la ville. Le style dominant est éco-chic — chukum, bois dur, ventilation traversante — et la procédure environnementale SEMA est de fait obligatoire : c’est le calendrier des permis qui commande celui du chantier.',
 'zh': 'Aldea Zamá 是图卢姆已完成市政配套的高端片区：管线入地、道路成熟，度假出租需求全城最高。主流风格为生态时尚风——chukum 灰泥、硬木、穿堂通风——SEMA 环保流程几乎是必办项，因此许可进度决定施工进度。'},
'la-veleta': {
 'es': 'La Veleta es la zona de mayor crecimiento de Tulum y el mejor precio de entrada entre las zonas premium, con la contrapartida de que los servicios varían calle por calle: antes de comprar verificamos agua, CFE, acceso y situación legal del predio. La SEMA sigue aplicando en la mayoría de los lotes y la rentabilidad de renta corta aquí es de las más altas de la ciudad.',
 'en': 'La Veleta is Tulum’s fastest-growing area and the best entry price among the premium zones, with the trade-off that services vary street by street: before you buy we verify water, CFE, access and the legal status of the lot. SEMA still applies on most lots, and short-term rental returns here are among the highest in town.',
 'ru': 'Ла-Велета — самый быстрорастущий район Тулума и лучшая цена входа среди премиальных зон, но с оговоркой: коммуникации отличаются от улицы к улице, поэтому до покупки мы проверяем воду, CFE, подъезд и юридический статус участка. SEMA действует на большинстве лотов, а доходность посуточной аренды здесь одна из самых высоких в городе.',
 'de': 'La Veleta ist das am schnellsten wachsende Viertel Tulums und der günstigste Einstieg unter den Premiumlagen — mit dem Haken, dass die Versorgung von Straße zu Straße variiert: Vor dem Kauf prüfen wir Wasser, CFE, Zufahrt und Rechtslage des Grundstücks. SEMA gilt auf den meisten Grundstücken, und die Rendite aus Kurzzeitvermietung gehört hier zu den höchsten der Stadt.',
 'fr': 'La Veleta est le secteur à la croissance la plus rapide de Tulum et le meilleur prix d’entrée parmi les zones premium, avec pour contrepartie des réseaux qui varient d’une rue à l’autre : avant l’achat, nous vérifions l’eau, la CFE, l’accès et la situation juridique du terrain. La SEMA s’applique sur la plupart des lots et le rendement locatif court terme y est parmi les meilleurs de la ville.',
 'zh': 'La Veleta 是图卢姆增长最快的片区，也是高端区域中入手价格最友好的一处，代价是市政配套逐街不同：购地前我们会核查供水、CFE 供电、道路接入与地块法律状态。多数地块仍需 SEMA 审批，而此处短租回报率位居全城前列。'},
'tulum-country-club': {
 'es': 'Tulum Country Club es una comunidad residencial de golf dentro del municipio de Tulum: lotes grandes, lineamientos de diseño del desarrollo y un estándar de acabados alto, con la selva como telón de fondo. Al ser municipio Tulum, la ruta de permisos incluye SEMA además de la licencia municipal con DRO, y el comité del desarrollo revisa el proyecto antes de que entre a trámite.',
 'en': 'Tulum Country Club is a residential golf community inside the municipality of Tulum: large lots, developer design guidelines and a high finish standard, with the jungle as the backdrop. Because it is Tulum, the permit route includes SEMA on top of the municipal licence with a DRO, and the development’s committee reviews the project before it is filed.',
 'ru': 'Tulum Country Club — жилое гольф-сообщество в муниципалитете Тулум: крупные участки, дизайн-регламент застройщика и высокий стандарт отделки на фоне сельвы. Поскольку это Тулум, маршрут разрешений включает SEMA в дополнение к муниципальной лицензии с DRO, а комитет застройки проверяет проект до подачи в муниципалитет.',
 'de': 'Tulum Country Club ist eine Golf-Wohnanlage in der Gemeinde Tulum: große Grundstücke, Gestaltungsrichtlinien des Entwicklers und ein hoher Ausbaustandard vor der Kulisse des Dschungels. Da es Tulum ist, umfasst der Genehmigungsweg neben der kommunalen Lizenz mit DRO auch die SEMA, und der Beirat der Anlage prüft das Projekt vor der Einreichung.',
 'fr': 'Tulum Country Club est une communauté résidentielle de golf située dans la commune de Tulum : grands terrains, lignes directrices architecturales du promoteur et standard de finition élevé, avec la jungle en toile de fond. Commune de Tulum oblige, le parcours des permis inclut la SEMA en plus du permis municipal avec DRO, et le comité du développement examine le projet avant dépôt.',
 'zh': 'Tulum Country Club 是位于图卢姆市辖内的高尔夫住宅社区：地块宽大、开发商设有设计导则、装修标准较高，以雨林为背景。由于属图卢姆市，许可路径在带 DRO 的市政许可之外还包括 SEMA，且社区委员会会在报批前先行审核方案。'},
'puerto-cancun': {
 'es': 'Puerto Cancún es la zona residencial premium de Cancún: marina, campo de golf y fraccionamientos cerrados a minutos del centro y del aeropuerto. Al estar en suelo FONATUR, el proyecto pasa por su visto bueno además de la licencia de Benito Juárez, y los lotes frente al canal o al mar suman concesión ZOFEMAT y diseño anticorrosivo reforzado.',
 'en': 'Puerto Cancún is Cancún’s premium residential zone: marina, golf course and gated phases minutes from downtown and the airport. Because it sits on FONATUR land, the project needs their sign-off on top of the Benito Juárez licence, and lots facing the canal or the sea add a ZOFEMAT concession and a reinforced anti-corrosion spec.',
 'ru': 'Пуэрто-Канкун — премиальный жилой район Канкуна: марина, поле для гольфа и закрытые секторы в нескольких минутах от центра и аэропорта. Земля относится к FONATUR, поэтому проект проходит их согласование в дополнение к лицензии Benito Juárez, а участки у канала или моря требуют концессии ZOFEMAT и усиленной антикоррозийной схемы.',
 'de': 'Puerto Cancún ist die Premium-Wohnlage von Cancún: Marina, Golfplatz und geschlossene Abschnitte, Minuten von Zentrum und Flughafen. Da es auf FONATUR-Land liegt, ist deren Freigabe zusätzlich zur Lizenz von Benito Juárez nötig; Grundstücke am Kanal oder Meer benötigen eine ZOFEMAT-Konzession und eine verstärkte Korrosionsschutzplanung.',
 'fr': 'Puerto Cancún est la zone résidentielle premium de Cancún : marina, golf et tranches fermées à quelques minutes du centre et de l’aéroport. Terrain FONATUR oblige, le projet passe par leur accord en plus du permis de Benito Juárez, et les lots donnant sur le canal ou la mer ajoutent une concession ZOFEMAT et un traitement anticorrosion renforcé.',
 'zh': 'Puerto Cancún 是坎昆的高端住宅区：码头、高尔夫球场与封闭式区段，距市中心和机场仅数分钟车程。由于地处 FONATUR 土地，方案在 Benito Juárez 市政许可之外还需其批准；面向运河或海面的地块另需 ZOFEMAT 特许，并采用加强的防腐设计。'},
'zona-hotelera-cancun': {
 'es': 'La Zona Hotelera es el frente de mar más regulado del Caribe mexicano: suelo FONATUR, concesión ZOFEMAT en playa y ventanas de acceso y horario para obra por el tráfico turístico. Aquí construimos residencias y penthouses frente al mar con especificación marina completa —recubrimientos mayores, herrería tratada, cancelería anodizada, impermeabilización reforzada— porque la salinidad es la más agresiva de la región.',
 'en': 'The Hotel Zone is the most regulated beachfront in the Mexican Caribbean: FONATUR land, a ZOFEMAT concession on the beach and restricted access and working-hour windows because of tourist traffic. We build beachfront residences and penthouses here to a full marine spec — greater rebar cover, treated ironwork, anodised joinery, reinforced waterproofing — because salt exposure is the harshest in the region.',
 'ru': 'Отельная зона — самая зарегулированная первая линия мексиканского Карибского побережья: земля FONATUR, концессия ZOFEMAT на пляже и жёсткие окна доступа и часов работ из-за туристического трафика. Здесь мы строим резиденции и пентхаусы у моря по полной морской спецификации — увеличенный защитный слой, обработанный металл, анодированный алюминий, усиленная гидроизоляция, — потому что солевая агрессия тут самая сильная в регионе.',
 'de': 'Die Hotelzone ist die am stärksten regulierte Strandlage der mexikanischen Karibik: FONATUR-Land, ZOFEMAT-Konzession am Strand sowie beschränkte Zufahrts- und Arbeitszeitfenster wegen des Touristenverkehrs. Wir bauen hier Strandresidenzen und Penthouses in voller Meeresspezifikation — größere Betondeckung, behandelte Schlosserarbeiten, eloxierte Fenster, verstärkte Abdichtung — weil die Salzbelastung hier am aggressivsten ist.',
 'fr': 'La Zone Hôtelière est le front de mer le plus réglementé des Caraïbes mexicaines : terrain FONATUR, concession ZOFEMAT sur la plage et fenêtres d’accès et d’horaires restreintes à cause du trafic touristique. Nous y construisons résidences et penthouses en front de mer avec une spécification marine complète — enrobage renforcé, ferronnerie traitée, menuiseries anodisées, étanchéité renforcée — car la salinité y est la plus agressive de la région.',
 'zh': '酒店区是墨西哥加勒比海岸监管最严的海滨地段：FONATUR 土地、沙滩需 ZOFEMAT 特许，并因旅游车流而对进出通道与作业时段设有限制窗口。我们在此按完整的海洋环境标准建造海滨住宅与顶层公寓——加大保护层、铁件防腐、阳极氧化门窗、加强防水——因为这里的盐蚀强度为全区之最。'},
}

# two zone-specific FAQ per zone per language
ZFAQ = {
'playacar': {
 'es': [('¿Cómo se aprueba un proyecto en Playacar?', 'Primero el comité de diseño del fraccionamiento (alturas, retiros, cubiertas, colores, materiales) y después la licencia municipal de Solidaridad con DRO. Presentamos ambos expedientes y negociamos las observaciones del comité.'),
        ('¿Cuánto cuesta construir en Playacar?', 'De $15,000 a $31,300 MXN por m². El nivel de acabados que pide el fraccionamiento y su reglamento de fachadas es lo que sube el costo frente al resto de Playa del Carmen.')],
 'en': [('How does a project get approved in Playacar?', 'First the estate’s design committee (heights, setbacks, roofs, colours, materials), then the Solidaridad municipal licence with a DRO. We file both and negotiate the committee’s comments.'),
        ('How much does it cost to build in Playacar?', 'From $15,000 to $31,300 MXN per m². The finish standard the community expects and its façade rules are what raise the cost over the rest of Playa del Carmen.')],
 'ru': [('Как утверждается проект в Плаякаре?', 'Сначала комитет по дизайну посёлка (высоты, отступы, кровли, цвета, материалы), затем муниципальная лицензия Solidaridad с DRO. Мы подаём оба пакета и отрабатываем замечания комитета.'),
        ('Сколько стоит стройка в Плаякаре?', 'От $15,000 до $31,300 MXN за м². Дороже, чем в остальной Плая-дель-Кармен, из-за стандарта отделки и регламента по фасадам.')],
 'de': [('Wie wird ein Projekt in Playacar genehmigt?', 'Zuerst der Gestaltungsbeirat der Anlage (Höhen, Abstände, Dächer, Farben, Materialien), dann die kommunale Lizenz von Solidaridad mit DRO. Wir reichen beides ein und arbeiten die Auflagen des Beirats ab.'),
        ('Was kostet Bauen in Playacar?', 'Zwischen $15.000 und $31.300 MXN pro m². Der erwartete Ausbaustandard und die Fassadensatzung treiben den Preis gegenüber dem übrigen Playa del Carmen.')],
 'fr': [('Comment un projet est-il approuvé à Playacar ?', 'D’abord le comité d’architecture de la résidence (hauteurs, reculs, toitures, couleurs, matériaux), puis le permis municipal de Solidaridad avec DRO. Nous déposons les deux et traitons les observations du comité.'),
        ('Combien coûte la construction à Playacar ?', 'De 15 000 à 31 300 MXN le m². Le standard de finition attendu et le règlement de façades expliquent l’écart avec le reste de Playa del Carmen.')],
 'zh': [('在 Playacar 项目如何获批？', '先经社区设计委员会审批（高度、退线、屋面、色彩、材料），再办理带 DRO 的 Solidaridad 市政许可。两套材料均由我们报审，并负责回应委员会意见。'),
        ('在 Playacar 建房要多少钱？', '每平方米 15,000 至 31,300 比索。社区要求的装修标准与立面规约，是造价高于普拉亚德尔卡门其他片区的主要原因。')]},
'mayakoba': {
 'es': [('¿Qué hace distinta la obra en Mayakoba?', 'El control: comité de diseño propio, reglas ambientales por lagunas y manglar, accesos y horarios regulados y manejo de residuos documentado. La obra se planea alrededor de esas reglas desde el primer día.'),
        ('¿Cuál es el rango de precio en Mayakoba?', 'De $17,000 a $35,500 MXN por m², el escalón más alto de la Riviera Maya, por estándar de acabados, logística controlada y requisitos ambientales.')],
 'en': [('What makes building in Mayakoba different?', 'The control: its own design committee, environmental rules for the lagoons and mangrove, regulated access and hours, and documented waste handling. The build is planned around those rules from day one.'),
        ('What is the price range in Mayakoba?', 'From $17,000 to $35,500 MXN per m² — the top tier on the Riviera Maya, driven by finish standard, controlled logistics and environmental requirements.')],
 'ru': [('Чем стройка в Майякобе отличается?', 'Контролем: собственный комитет по дизайну, экологические правила из-за лагун и мангров, регламентированные доступ и часы работ, документированный вывоз отходов. Стройка планируется вокруг этих правил с первого дня.'),
        ('Какой диапазон цен в Майякобе?', 'От $17,000 до $35,500 MXN за м² — верхняя планка Ривьеры-Майя: стандарт отделки, контролируемая логистика и экологические требования.')],
 'de': [('Was ist beim Bauen in Mayakoba anders?', 'Die Kontrolle: eigener Gestaltungsbeirat, Umweltauflagen wegen Lagunen und Mangroven, geregelte Zufahrt und Arbeitszeiten sowie dokumentierte Abfallentsorgung. Der Bau wird von Tag eins um diese Regeln herum geplant.'),
        ('Wie hoch ist die Preisspanne in Mayakoba?', 'Von $17.000 bis $35.500 MXN pro m² — die höchste Stufe der Riviera Maya, bedingt durch Ausbaustandard, kontrollierte Logistik und Umweltauflagen.')],
 'fr': [('Qu’est-ce qui change à Mayakoba ?', 'Le contrôle : comité d’architecture propre, règles environnementales liées aux lagunes et à la mangrove, accès et horaires encadrés, gestion des déchets documentée. Le chantier est planifié autour de ces règles dès le premier jour.'),
        ('Quelle est la fourchette de prix à Mayakoba ?', 'De 17 000 à 35 500 MXN le m² — le haut du marché de la Riviera Maya, du fait du standard de finition, de la logistique encadrée et des exigences environnementales.')],
 'zh': [('在 Mayakoba 施工有何不同？', '在于管控：独立设计委员会、因泻湖与红树林而生的环保规定、受控的出入与作业时段，以及需留痕的废弃物处理。项目从第一天起就围绕这些规则排布。'),
        ('Mayakoba 的价格区间是多少？', '每平方米 17,000 至 35,500 比索，为里维埃拉玛雅最高一档，源于装修标准、受控物流与环保要求。')]},
'corasol': {
 'es': [('¿Recrea tiene presencia en Corasol?', 'Sí, nuestra oficina está en Corasol. Eso significa supervisión diaria de obra y trato directo con la administración del desarrollo para accesos, horarios y revisión de proyecto.'),
        ('¿Qué exige el desarrollo para construir?', 'Lineamientos de diseño del desarrollador (volumetría, materiales, alturas y áreas verdes) más la licencia municipal de Solidaridad con DRO. Los presentamos en paralelo para no perder tiempo.')],
 'en': [('Does Recrea have a presence in Corasol?', 'Yes — our office is in Corasol. That means daily site supervision and direct dealings with the estate management on access, working hours and project review.'),
        ('What does the development require to build?', 'The developer’s design guidelines (massing, materials, heights, green areas) plus the Solidaridad municipal licence with a DRO. We run both in parallel to save time.')],
 'ru': [('У Recrea есть присутствие в Корасоле?', 'Да, наш офис находится в Корасоле. Это ежедневный надзор на площадке и прямое взаимодействие с администрацией по доступу, часам работ и согласованию проекта.'),
        ('Что требует застройка для стройки?', 'Дизайн-регламент застройщика (объём, материалы, высоты, зелёные зоны) плюс муниципальная лицензия Solidaridad с DRO. Ведём оба трека параллельно.')],
 'de': [('Ist Recrea in Corasol präsent?', 'Ja, unser Büro liegt in Corasol. Das bedeutet tägliche Bauüberwachung und direkte Abstimmung mit der Verwaltung zu Zufahrt, Arbeitszeiten und Projektprüfung.'),
        ('Was verlangt die Anlage zum Bauen?', 'Die Gestaltungsrichtlinien des Entwicklers (Baukörper, Materialien, Höhen, Grünflächen) plus die kommunale Lizenz von Solidaridad mit DRO. Wir betreiben beides parallel.')],
 'fr': [('Recrea est-il présent à Corasol ?', 'Oui, notre bureau est à Corasol. Cela signifie une supervision quotidienne du chantier et un lien direct avec l’administration pour les accès, horaires et la revue de projet.'),
        ('Qu’exige le développement pour construire ?', 'Les lignes directrices architecturales du promoteur (volumétrie, matériaux, hauteurs, espaces verts) et le permis municipal de Solidaridad avec DRO. Nous menons les deux en parallèle.')],
 'zh': [('Recrea 在 Corasol 有据点吗？', '有，我们的办公室就设在 Corasol。这意味着每日现场监理，并可就出入、施工时段与方案审核与社区管理方直接对接。'),
        ('社区对施工有哪些要求？', '开发商设计导则（体量、材料、高度、绿地）加上带 DRO 的 Solidaridad 市政许可。两条线我们并行推进以节省时间。')]},
'aldea-zama': {
 'es': [('¿Cuánto tardan los permisos en Aldea Zamá?', 'De 3 a 5 meses, porque casi siempre interviene la SEMA además de la licencia municipal de Tulum. Iniciamos el trámite en paralelo al proyecto ejecutivo para no perder temporada.'),
        ('¿Conviene construir para renta vacacional?', 'Es la zona con mayor demanda de renta corta en Tulum. Diseñamos distribución para huéspedes, alberca, mobiliario FF&E y prevemos la licencia de funcionamiento desde el proyecto.')],
 'en': [('How long do permits take in Aldea Zamá?', '3 to 5 months, because SEMA is almost always involved on top of the Tulum municipal licence. We start the process in parallel with the construction documents so you do not lose a season.'),
        ('Is it worth building for vacation rental?', 'It is the strongest short-term rental zone in Tulum. We design guest-oriented layouts, a pool and an FF&E package, and plan for the operating licence from the design stage.')],
 'ru': [('Сколько идут разрешения в Альдеа-Зама?', '3–5 месяцев: почти всегда подключается SEMA в дополнение к муниципальной лицензии Тулума. Запускаем процедуру параллельно с рабочим проектом, чтобы не потерять сезон.'),
        ('Есть ли смысл строить под аренду?', 'Это зона с самым высоким спросом на посуточную аренду в Тулуме. Планировка под гостей, бассейн, комплект мебели FF&E и лицензия на деятельность закладываются ещё на этапе проекта.')],
 'de': [('Wie lange dauern Genehmigungen in Aldea Zamá?', '3 bis 5 Monate, da neben der kommunalen Lizenz von Tulum fast immer die SEMA beteiligt ist. Wir starten das Verfahren parallel zur Ausführungsplanung, damit keine Saison verloren geht.'),
        ('Lohnt sich der Bau für Ferienvermietung?', 'Es ist die nachfragestärkste Kurzzeitmietzone Tulums. Wir planen gästetaugliche Grundrisse, Pool und FF&E-Paket und berücksichtigen die Betriebslizenz bereits im Entwurf.')],
 'fr': [('Combien de temps prennent les permis à Aldea Zamá ?', '3 à 5 mois, car la SEMA intervient presque toujours en plus du permis municipal de Tulum. Nous lançons la procédure en parallèle du projet d’exécution pour ne pas perdre une saison.'),
        ('Faut-il construire pour la location saisonnière ?', 'C’est la zone la plus demandée de Tulum en location courte. Nous concevons une distribution adaptée aux hôtes, une piscine et un pack FF&E, et anticipons la licence d’exploitation dès la conception.')],
 'zh': [('Aldea Zamá 的许可需要多久？', '3至5个月，因为除图卢姆市政许可外几乎都会涉及 SEMA。我们会在施工图阶段同步启动报批，避免错过旺季。'),
        ('适合建来做度假出租吗？', '这是图卢姆短租需求最旺的片区。我们按接待房客的动线设计，配置泳池与 FF&E 家具包，并在设计阶段即预留经营许可事项。')]},
'la-veleta': {
 'es': [('¿Qué reviso antes de comprar en La Veleta?', 'Agua, CFE, acceso pavimentado, uso de suelo y situación legal del predio: en La Veleta varían calle por calle. Hacemos esa revisión antes de que usted firme.'),
        ('¿Por qué es más barato que Aldea Zamá?', 'Porque la urbanización aún está en proceso. El costo de obra es 8–10% menor y el terreno bastante más accesible, con el mismo requisito ambiental de SEMA.')],
 'en': [('What should I check before buying in La Veleta?', 'Water, CFE, paved access, land use and the legal status of the lot — in La Veleta these vary street by street. We run that check before you sign.'),
        ('Why is it cheaper than Aldea Zamá?', 'Because urbanisation is still in progress. Construction runs 8–10% lower and land is considerably more accessible, with the same SEMA environmental requirement.')],
 'ru': [('Что проверить до покупки в Ла-Велете?', 'Воду, CFE, асфальтированный подъезд, назначение земли и юридический статус участка — в Ла-Велете всё отличается от улицы к улице. Проверяем до подписания.'),
        ('Почему дешевле, чем Альдеа-Зама?', 'Потому что урбанизация ещё идёт. Стройка на 8–10% дешевле, земля заметно доступнее, при том же требовании SEMA.')],
 'de': [('Was prüfe ich vor dem Kauf in La Veleta?', 'Wasser, CFE, befestigte Zufahrt, Nutzungsart und Rechtslage des Grundstücks — in La Veleta variiert das von Straße zu Straße. Wir prüfen das vor Ihrer Unterschrift.'),
        ('Warum ist es günstiger als Aldea Zamá?', 'Weil die Erschließung noch läuft. Die Bauleistung liegt 8–10% niedriger und das Grundstück ist deutlich zugänglicher — bei gleicher SEMA-Auflage.')],
 'fr': [('Que vérifier avant d’acheter à La Veleta ?', 'L’eau, la CFE, l’accès goudronné, l’usage du sol et la situation juridique du terrain : à La Veleta, cela varie d’une rue à l’autre. Nous faisons cette vérification avant votre signature.'),
        ('Pourquoi est-ce moins cher qu’Aldea Zamá ?', 'Parce que l’urbanisation est encore en cours. Le chantier revient 8 à 10% moins cher et le foncier est nettement plus accessible, avec la même exigence SEMA.')],
 'zh': [('在 La Veleta 购地前应核查什么？', '供水、CFE 供电、硬化道路接入、土地用途与地块法律状态——在 La Veleta 这些逐街不同。我们会在您签约前完成核查。'),
        ('为什么比 Aldea Zamá 便宜？', '因为市政配套仍在推进中。施工造价低8%至10%，地价明显更友好，但 SEMA 环保要求相同。')]},
'tulum-country-club': {
 'es': [('¿Qué permisos necesito en Tulum Country Club?', 'Aprobación del comité de diseño del desarrollo, licencia municipal de Tulum con DRO y, en la mayoría de los predios, autorización ambiental de SEMA. Gestionamos las tres vías.'),
        ('¿Cuánto cuesta construir en Tulum Country Club?', 'De $14,700 a $30,500 MXN por m² según acabados. El lote grande y el estándar del desarrollo empujan hacia la parte alta del rango.')],
 'en': [('What permits do I need at Tulum Country Club?', 'Approval from the development’s design committee, the Tulum municipal licence with a DRO and, on most lots, SEMA environmental authorisation. We handle all three tracks.'),
        ('How much does it cost to build at Tulum Country Club?', 'From $14,700 to $30,500 MXN per m² depending on finishes. Large lots and the community’s standard push projects toward the upper half of that range.')],
 'ru': [('Какие разрешения нужны в Tulum Country Club?', 'Одобрение комитета по дизайну застройки, муниципальная лицензия Тулума с DRO и, на большинстве участков, экологическое разрешение SEMA. Ведём все три трека.'),
        ('Сколько стоит стройка в Tulum Country Club?', 'От $14,700 до $30,500 MXN за м² в зависимости от отделки. Крупный участок и стандарт застройки тянут проект в верхнюю половину диапазона.')],
 'de': [('Welche Genehmigungen brauche ich im Tulum Country Club?', 'Freigabe durch den Gestaltungsbeirat der Anlage, die kommunale Lizenz von Tulum mit DRO und auf den meisten Grundstücken die SEMA-Umweltgenehmigung. Wir übernehmen alle drei Wege.'),
        ('Was kostet Bauen im Tulum Country Club?', 'Von $14.700 bis $30.500 MXN pro m² je nach Ausbau. Große Grundstücke und der Standard der Anlage verschieben Projekte in die obere Hälfte der Spanne.')],
 'fr': [('Quels permis faut-il à Tulum Country Club ?', 'L’accord du comité d’architecture du développement, le permis municipal de Tulum avec DRO et, sur la plupart des lots, l’autorisation environnementale de la SEMA. Nous gérons les trois.'),
        ('Combien coûte la construction à Tulum Country Club ?', 'De 14 700 à 30 500 MXN le m² selon les finitions. La taille des terrains et le standard du développement tirent les projets vers le haut de la fourchette.')],
 'zh': [('在 Tulum Country Club 需要哪些许可？', '社区设计委员会批准、带 DRO 的图卢姆市政许可，以及多数地块所需的 SEMA 环保许可。三条线均由我们办理。'),
        ('在 Tulum Country Club 建房要多少钱？', '按装修标准，每平方米 14,700 至 30,500 比索。地块面积大与社区标准高，会把项目推向区间上半段。')]},
'puerto-cancun': {
 'es': [('¿Qué cambia por ser suelo FONATUR?', 'Se suma el visto bueno de FONATUR a la licencia de Benito Juárez, con revisión de imagen urbana y densidad. En lotes frente al canal o al mar entra además la concesión ZOFEMAT.'),
        ('¿Qué exige la cercanía a la marina?', 'Especificación anticorrosiva completa: mayor recubrimiento de acero, herrería tratada, cancelería anodizada, impermeabilización reforzada y equipos de A/A aptos para ambiente salino.')],
 'en': [('What changes because it is FONATUR land?', 'FONATUR sign-off is added to the Benito Juárez licence, with urban-image and density review. Lots facing the canal or the sea also require a ZOFEMAT concession.'),
        ('What does being next to the marina require?', 'A full anti-corrosion spec: greater rebar cover, treated ironwork, anodised joinery, reinforced waterproofing and marine-rated A/C equipment.')],
 'ru': [('Что меняет земля FONATUR?', 'К лицензии Benito Juárez добавляется согласование FONATUR с проверкой городского облика и плотности. Участки у канала или моря требуют ещё и концессии ZOFEMAT.'),
        ('Что требует близость марины?', 'Полную антикоррозийную спецификацию: увеличенный защитный слой арматуры, обработанный металл, анодированный алюминий, усиленную гидроизоляцию и кондиционеры в морском исполнении.')],
 'de': [('Was ändert FONATUR-Land?', 'Zur Lizenz von Benito Juárez kommt die FONATUR-Freigabe mit Prüfung von Stadtbild und Dichte. Grundstücke am Kanal oder Meer benötigen zusätzlich eine ZOFEMAT-Konzession.'),
        ('Was verlangt die Nähe zur Marina?', 'Eine vollständige Korrosionsschutzspezifikation: größere Betondeckung, behandelte Schlosserarbeiten, eloxierte Fenster, verstärkte Abdichtung und seeluftgeeignete Klimatechnik.')],
 'fr': [('Qu’est-ce qui change avec un terrain FONATUR ?', 'L’accord FONATUR s’ajoute au permis de Benito Juárez, avec examen de l’image urbaine et de la densité. Les lots sur le canal ou la mer exigent en plus une concession ZOFEMAT.'),
        ('Qu’impose la proximité de la marina ?', 'Une spécification anticorrosion complète : enrobage renforcé des aciers, ferronnerie traitée, menuiseries anodisées, étanchéité renforcée et climatisation qualifiée bord de mer.')],
 'zh': [('地处 FONATUR 土地有何不同？', '在 Benito Juárez 市政许可之外需增加 FONATUR 批准，并审查城市风貌与容积密度。面向运河或海面的地块另需 ZOFEMAT 特许。'),
        ('紧邻码头需要哪些配置？', '完整的防腐做法：加大钢筋保护层、铁件防腐处理、阳极氧化门窗、加强防水，以及适用于海边环境的空调设备。')]},
'zona-hotelera-cancun': {
 'es': [('¿Se puede construir casa en la Zona Hotelera?', 'Sí, en los lotes residenciales existentes: suelo FONATUR, licencia de Benito Juárez con DRO y concesión ZOFEMAT si el predio es de playa. Las ventanas de acceso y horario de obra se negocian por el tráfico turístico.'),
        ('¿Qué especificación se usa frente al mar?', 'Especificación marina completa: recubrimientos mayores, acero e instalaciones protegidas, cancelería anodizada, vidrio de seguridad para huracanes e impermeabilización reforzada en azoteas y terrazas.')],
 'en': [('Can you build a house in the Hotel Zone?', 'Yes, on the existing residential lots: FONATUR land, a Benito Juárez licence with a DRO and a ZOFEMAT concession if the lot is on the beach. Access and working-hour windows are negotiated around tourist traffic.'),
        ('What spec is used on the beachfront?', 'A full marine spec: greater cover, protected rebar and services, anodised joinery, hurricane-rated glazing and reinforced waterproofing on roofs and terraces.')],
 'ru': [('Можно ли построить дом в Отельной зоне?', 'Да, на существующих жилых участках: земля FONATUR, лицензия Benito Juárez с DRO и концессия ZOFEMAT, если участок пляжный. Окна доступа и часы работ согласуются с учётом туристического трафика.'),
        ('Какая спецификация нужна на первой линии?', 'Полная морская: увеличенные защитные слои, защищённая арматура и инженерия, анодированный алюминий, ударопрочное остекление под ураганы и усиленная гидроизоляция кровель и террас.')],
 'de': [('Kann man in der Hotelzone ein Haus bauen?', 'Ja, auf den bestehenden Wohngrundstücken: FONATUR-Land, Lizenz von Benito Juárez mit DRO und ZOFEMAT-Konzession bei Strandlage. Zufahrts- und Arbeitszeitfenster werden wegen des Touristenverkehrs abgestimmt.'),
        ('Welche Spezifikation gilt am Strand?', 'Volle Meeresspezifikation: größere Deckung, geschützte Bewehrung und Installationen, eloxierte Fenster, hurrikanfeste Verglasung und verstärkte Abdichtung auf Dächern und Terrassen.')],
 'fr': [('Peut-on construire une maison en Zone Hôtelière ?', 'Oui, sur les lots résidentiels existants : terrain FONATUR, permis de Benito Juárez avec DRO et concession ZOFEMAT si le lot est en bord de plage. Les fenêtres d’accès et d’horaires se négocient selon le trafic touristique.'),
        ('Quelle spécification en front de mer ?', 'Spécification marine complète : enrobages renforcés, aciers et réseaux protégés, menuiseries anodisées, vitrages anticycloniques et étanchéité renforcée en toitures et terrasses.')],
 'zh': [('可以在酒店区建独栋住宅吗？', '可以，在既有的住宅地块上：FONATUR 土地、带 DRO 的 Benito Juárez 市政许可，若属海滩地块还需 ZOFEMAT 特许。进出通道与作业时段需结合旅游车流协商确定。'),
        ('海滨地块采用什么标准？', '完整的海洋环境标准：加大保护层、钢筋与管线做防护、阳极氧化门窗、抗飓风安全玻璃，以及屋面与露台的加强防水。')]},
}

ZLINKS = {
 'es': {'playacar': [('/villas-de-lujo-playacar/','Villas de lujo en Playacar'), ('/permisos-de-construccion-playacar/','Permisos de construcción en Playacar'), ('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/calculadora/','Calculadora de costos')],
        'mayakoba': [('/villas-de-lujo-mayakoba/','Villas de lujo en Mayakoba'), ('/permisos-de-construccion-mayakoba/','Permisos de construcción en Mayakoba'), ('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/calculadora/','Calculadora de costos')],
        'corasol': [('/villas-de-lujo-corasol/','Villas de lujo en Corasol'), ('/permisos-de-construccion-corasol/','Permisos de construcción en Corasol'), ('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/calculadora/','Calculadora de costos')],
        'aldea-zama': [('/villas-de-lujo-aldea-zama-tulum/','Villas de lujo en Aldea Zamá'), ('/permisos-de-construccion-aldea-zama/','Permisos de construcción en Aldea Zamá'), ('/construccion-de-casas-tulum/','Construcción de casas en Tulum'), ('/calculadora/','Calculadora de costos')],
        'la-veleta': [('/villas-de-lujo-la-veleta-tulum/','Villas de lujo en La Veleta'), ('/permisos-de-construccion-la-veleta/','Permisos de construcción en La Veleta'), ('/construccion-de-casas-tulum/','Construcción de casas en Tulum'), ('/calculadora/','Calculadora de costos')],
        'tulum-country-club': [('/constructora-region-15-tulum/','Constructora en Región 15'), ('/permisos-de-construccion-tulum-ciudad/','Permisos de construcción en Tulum'), ('/construccion-de-casas-tulum/','Construcción de casas en Tulum'), ('/calculadora/','Calculadora de costos')],
        'puerto-cancun': [('/villas-de-lujo-puerto-cancun/','Villas de lujo en Puerto Cancún'), ('/permisos-de-construccion-puerto-cancun/','Permisos de construcción en Puerto Cancún'), ('/construccion-de-casas-cancun/','Construcción de casas en Cancún'), ('/calculadora/','Calculadora de costos')],
        'zona-hotelera-cancun': [('/villas-de-lujo-zona-hotelera-cancun/','Villas de lujo en la Zona Hotelera'), ('/permisos-de-construccion-zona-hotelera-cancun/','Permisos de construcción en la Zona Hotelera'), ('/construccion-de-casas-cancun/','Construcción de casas en Cancún'), ('/calculadora/','Calculadora de costos')]},
 'en': {'playacar': [('/luxury-villas-playacar/','Luxury villas in Playacar'), ('/construction-permits-playacar/','Construction permits in Playacar'), ('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/calculator/','Cost calculator')],
        'mayakoba': [('/luxury-villas-mayakoba/','Luxury villas in Mayakoba'), ('/construction-permits-mayakoba/','Construction permits in Mayakoba'), ('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/calculator/','Cost calculator')],
        'corasol': [('/luxury-villas-corasol/','Luxury villas in Corasol'), ('/construction-permits-corasol/','Construction permits in Corasol'), ('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/calculator/','Cost calculator')],
        'aldea-zama': [('/luxury-villas-aldea-zama-tulum/','Luxury villas in Aldea Zamá'), ('/construction-permits-aldea-zama/','Construction permits in Aldea Zamá'), ('/house-construction-tulum/','House construction in Tulum'), ('/calculator/','Cost calculator')],
        'la-veleta': [('/luxury-villas-la-veleta-tulum/','Luxury villas in La Veleta'), ('/construction-permits-la-veleta/','Construction permits in La Veleta'), ('/house-construction-tulum/','House construction in Tulum'), ('/calculator/','Cost calculator')],
        'tulum-country-club': [('/builder-region-15-tulum/','Builder in Región 15'), ('/construction-permits-tulum-city/','Construction permits in Tulum'), ('/house-construction-tulum/','House construction in Tulum'), ('/calculator/','Cost calculator')],
        'puerto-cancun': [('/luxury-villas-puerto-cancun/','Luxury villas in Puerto Cancún'), ('/construction-permits-puerto-cancun/','Construction permits in Puerto Cancún'), ('/house-construction-cancun/','House construction in Cancún'), ('/calculator/','Cost calculator')],
        'zona-hotelera-cancun': [('/luxury-villas-hotel-zone-cancun/','Luxury villas in the Hotel Zone'), ('/construction-permits-cancun-hotel-zone/','Construction permits in the Hotel Zone'), ('/house-construction-cancun/','House construction in Cancún'), ('/calculator/','Cost calculator')]},
}
for _lang, _hub, _calc, _blog in [('ru', '/stroitelstvo-domov-%s/', '/kalkulyator/', '/blog-ru/'),
                                  ('de', '/hausbau-%s/', '/kostenrechner/', '/blog-de/'),
                                  ('fr', '/construction-de-maisons-%s/', '/calculateur/', '/blog-fr/'),
                                  ('zh', '/zhuzhai-jianzao-%s/', '/jisuanqi/', '/blog-zh/')]:
    ZLINKS[_lang] = {}
    for _z, _d in ZONE.items():
        hub_label = {'ru': 'Строительство домов', 'de': 'Hausbau', 'fr': 'Construction de maisons', 'zh': '住宅建造'}[_lang]
        parent_name = ml.CITY[_lang][_d['parent']]
        ZLINKS[_lang][_z] = [
            (_hub % _d['parent'], '%s — %s' % (hub_label, parent_name)),
            ({'ru': '/razresheniya-i-licenzii-riviera-maya/', 'de': '/baugenehmigungen-lizenzen-riviera-maya/',
              'fr': '/permis-et-licences-construction-riviera-maya/', 'zh': '/jianzhu-xuke-yu-zhizhao-riviera-maya/'}[_lang],
             {'ru': 'Разрешения, лицензии и DRO', 'de': 'Genehmigungen, Lizenzen und DRO',
              'fr': 'Permis, licences et DRO', 'zh': '建筑许可与DRO'}[_lang]),
            (_hub % 'riviera-maya', '%s — %s' % (hub_label, ml.CITY[_lang]['riviera-maya'])),
            (_calc, {'ru': 'Калькулятор стоимости', 'de': 'Kostenrechner', 'fr': 'Calculateur de coûts', 'zh': '造价计算器'}[_lang]),
            (_blog, {'ru': 'Гиды по строительству', 'de': 'Bau-Leitfäden', 'fr': 'Guides de construction', 'zh': '建筑指南'}[_lang]),
        ]

# --------------------------------------------------------------- ES strings ---
ml.REF['es'] = 'constructora-cancun'
ml.L['es'] = dict(locale='es_MX',
  h1='Construcción de Casas en {city}',
  title='Construcción de Casas en {city} | Obra Nueva Llave en Mano | Recrea',
  desc='Construcción de casas en {city}: obra nueva llave en mano con precio fijo. Precio por m² 2026, proceso paso a paso, permisos y tiempos. 18+ años, 196+ proyectos.',
  kw='construccion de casas {lcity}, construir casa {lcity}, obra nueva {lcity}, casas llave en mano {lcity}',
  lead='Obra nueva llave en mano en {city}: proyecto, permisos, cimentación, obra gris y acabados con un solo responsable y contrato a precio fijo.',
  intro='Recrea construye casas en {zones} desde 2008 — 196+ proyectos terminados en la Riviera Maya. Arquitectura, eléctrico, carpintería y herrería son equipos propios, así que su obra no depende de subcontratistas que aparecen y desaparecen.',
  alert='<strong>Precio de la construcción de casas en {city} (2026):</strong> {m2} MXN/m² ({usd} USD/m²) según nivel de acabados, sin incluir el terreno.',
  h_cost='Cuánto Cuesta la Construcción de una Casa en {city}',
  cost_p='Presupuestos reales de obra terminada, sin terreno ni mobiliario. El rango depende del nivel de acabados: económico, medio o premium (chukum, madera dura, cocina de autor, alberca desbordante).',
  th=('Tipo de casa', 'Costo de obra', 'Equivalente'), row='Casa {n} m²',
  cost_after='¿Quiere el número exacto para su terreno y sus m²? Use la <a href="/calculadora/">calculadora de costos</a> o pídanos un presupuesto por partidas.',
  h_proc='Proceso de Construcción de Casas Paso a Paso', proc_p='Así trabajamos cada obra nueva, con los tiempos que manejamos en {city}:',
  proc_total='<strong>Total:</strong> de 8 a 14 meses de obra, más {perm} meses de proyecto y permisos.',
  h_inc='Qué Incluye y Qué No Incluye el Precio por m²', inc_t='Incluido', ninc_t='No incluido',
  h_norm='Permisos y Normativa para Construir en {city}', h_soil='El terreno: lo que decide su cimentación',
  guides='Guías útiles: ', h_why='Por Qué Elegir Recrea para Construir su Casa',
  why=['<strong>196+ proyectos terminados</strong> en la Riviera Maya desde 2008',
       '<strong>Contrato a precio fijo</strong> por partidas — sin sobrecostos sorpresa',
       '<strong>Todo en una sola empresa</strong> — arquitectura, permisos, obra, eléctrico, carpintería, herrería',
       '<strong>DRO y arquitectos licenciados</strong> — obra 100% legal y trabajadores con IMSS',
       '<strong>Reportes semanales</strong> con fotos y video, ideal si usted no vive en México',
       '<strong>Garantía por escrito de 1 año</strong> sobre estructura e instalaciones'],
  h_proj='Proyectos Reales', h_cta='Presupuesto gratis para su casa en {city}',
  cta_p='196+ proyectos terminados. Contrato a precio fijo. Respuesta en 2 minutos.',
  wa='WhatsApp — 2 min', call='Llamar: 984 452 5333', form_h='O envíenos los datos de su proyecto',
  f_name='Nombre', f_phone='Teléfono / WhatsApp', f_msg='Metros cuadrados, zona del terreno y presupuesto aproximado...',
  f_send='Enviar Solicitud', h_faq='Preguntas Frecuentes', cta_btn='Cotizar por WhatsApp',
  badges=['Garantía 1 año por escrito', '18+ Años', '196+ Proyectos', 'Licencia y DRO', 'Asegurados'],
  steps=esg.STEPS, inc=esg.INCLUYE, ninc=esg.NO_INCLUYE,
  faq=[('¿Cuánto cuesta la construcción de una casa en {city}?',
        'De {m2} MXN por m² según el nivel de acabados. Una casa de 150 m² con alberca cuesta {p150} MXN, sin incluir el terreno.'),
       ('¿Cuánto tarda construir una casa?',
        '8 a 14 meses de obra, más {perm} meses de proyecto y permisos. Del primer contacto a la entrega de llaves: 12 a 18 meses para una casa de 150–200 m².'),
       ('¿Trabajan con precio fijo?',
        'Sí. Después del proyecto ejecutivo entregamos presupuesto cerrado por partidas y contrato a precio fijo con pagos por avance verificado. Solo los cambios que usted pida mueven el precio.'),
       ('¿Pueden construir si vivo en otro país?',
        'Es la mitad de nuestros clientes: contrato bilingüe a precio fijo, pagos por avance y reporte semanal con fotos y video del avance real de su casa.')])


def scale_money(text, f):
    """Scale every $number in a range string by f, keeping the format."""
    def one(m):
        raw = m.group(1)
        if raw.endswith('M'):
            return '$%.1fM' % (float(raw[:-1].replace(',', '')) * f)
        return '$%s' % format(int(round(float(raw.replace(',', '')) * f, -2)), ',d')
    return re.sub(r'\$([\d.,]+M?)', one, text)


def usd_from(mxn_text):
    def one(m):
        raw = m.group(1)
        if raw.endswith('M'):
            v = float(raw[:-1]) * 1e6 / MXN_USD
            return '$%s' % format(int(round(v, -3)), ',d')
        return '$%s' % format(int(round(float(raw.replace(',', '')) / MXN_USD, -1)), ',d')
    return re.sub(r'\$([\d.,]+M?)', one, mxn_text)


def register(zone, d):
    parent, f = d['parent'], d['f']
    pn = ml.NUM[parent]
    m2 = scale_money(pn['m2'], f)
    ml.NUM[zone] = dict(m2=m2, usd=usd_from(m2), perm=d['perm'],
                        sizes=[(sz[0], scale_money(sz[1], f), usd_from(scale_money(sz[1], f))) for sz in pn['sizes']])
    for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
        for D in (ml.CITY, ml.ZONES, ml.NORM, ml.SOIL, ml.EXTRA, ml.FAQX, ml.LINKS):
            D.setdefault(lang, {})
        ml.SLUG[lang][zone] = {'es': 'construccion-de-casas-', 'en': 'house-construction-', 'ru': 'stroitelstvo-domov-',
                               'de': 'hausbau-', 'fr': 'construction-de-maisons-', 'zh': 'zhuzhai-jianzao-'}[lang] + zone
        ml.CITY[lang][zone] = ZNAME[lang][zone]
        ml.ZONES[lang][zone] = ZAREA[zone][lang]
        if lang == 'es':
            ml.NORM['es'][zone] = esg.CITIES[parent]['norm']
            ml.SOIL['es'][zone] = esg.CITIES[parent]['soil']
        else:
            ml.NORM[lang][zone] = ml.NORM[lang][parent]
            ml.SOIL[lang][zone] = ml.SOIL[lang][parent]
        ml.EXTRA[lang][zone] = ZTEXT[zone][lang]
        ml.FAQX[lang][zone] = ZFAQ[zone][lang]
        ml.LINKS[lang][zone] = ZLINKS[lang][zone]


if __name__ == '__main__':
    for z, d in ZONE.items():
        register(z, d)
    ml.LOCS.extend(ZONE)
    for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
        ch = ml.chrome(lang)
        for z in ZONE:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-46s %6d bytes' % (out + '/', len(html)))
