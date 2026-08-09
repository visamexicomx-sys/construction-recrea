#!/usr/bin/env python3
"""Island pages (2026-08-09): Isla Mujeres and Cozumel — villas AND boutique hotels.

These are not "another zone": both are their own municipality, everything arrives
by ferry, and each island sits inside a marine national park. So the pages get:
  - their own H1/title/description (villas + hotels, not just houses)
  - their own slug per language
  - their own permit and ground paragraphs
  - an extra hospitality block: cost per key, plus what a hotel needs on an island
    (operating licence, Protección Civil, treatment plant, water, power capacity)

Verified: Cozumel is reached only by ferry from Playa del Carmen (passengers) with
vehicle/cargo ferries, and its reefs are a national marine park and UNESCO biosphere
reserve; Isla Mujeres is served by the Puerto Juárez / Gran Puerto ferries from Cancún.
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
z1 = load('gen-casas-zonas.py', 'z1')
ml = z1.ml

ISLAS = {
 'isla-mujeres': dict(parent='cancun',           f=1.35, perm='3–5'),
 'cozumel':      dict(parent='playa-del-carmen', f=1.30, perm='3–5'),
}
SLUGS = {
 'es': {'isla-mujeres': 'construccion-villas-hoteles-isla-mujeres', 'cozumel': 'construccion-villas-hoteles-cozumel'},
 'en': {'isla-mujeres': 'villa-hotel-construction-isla-mujeres', 'cozumel': 'villa-hotel-construction-cozumel'},
 'ru': {'isla-mujeres': 'stroitelstvo-vill-i-otelei-isla-mujeres', 'cozumel': 'stroitelstvo-vill-i-otelei-cozumel'},
 'de': {'isla-mujeres': 'villen-hotelbau-isla-mujeres', 'cozumel': 'villen-hotelbau-cozumel'},
 'fr': {'isla-mujeres': 'construction-villas-hotels-isla-mujeres', 'cozumel': 'construction-villas-hotels-cozumel'},
 'zh': {'isla-mujeres': 'bieshu-jiudian-jianzao-isla-mujeres', 'cozumel': 'bieshu-jiudian-jianzao-cozumel'},
}
NAMES = {
 'isla-mujeres': {'es': 'Isla Mujeres', 'en': 'Isla Mujeres', 'ru': 'Исла-Мухерес', 'de': 'Isla Mujeres', 'fr': 'Isla Mujeres', 'zh': 'Isla Mujeres'},
 'cozumel': {'es': 'Cozumel', 'en': 'Cozumel', 'ru': 'Косумеле', 'de': 'Cozumel', 'fr': 'Cozumel', 'zh': 'Cozumel'},
}
AREAS = {
 'isla-mujeres': {'es': 'Isla Mujeres, Punta Sur, Sac Bajo y la zona norte', 'en': 'Isla Mujeres, Punta Sur, Sac Bajo and the north end',
   'ru': 'Исла-Мухерес, Пунта-Сур, Сак-Бахо и северной части острова', 'de': 'Isla Mujeres, Punta Sur, Sac Bajo und dem Nordteil',
   'fr': 'Isla Mujeres, Punta Sur, Sac Bajo et la pointe nord', 'zh': 'Isla Mujeres、Punta Sur、Sac Bajo 与岛北端'},
 'cozumel': {'es': 'San Miguel de Cozumel, la costa norte y la carretera costera sur', 'en': 'San Miguel de Cozumel, the north coast and the southern coastal road',
   'ru': 'Сан-Мигель-де-Косумель, северном побережье и южной береговой дороге', 'de': 'San Miguel de Cozumel, der Nordküste und der südlichen Küstenstraße',
   'fr': 'San Miguel de Cozumel, la côte nord et la route côtière sud', 'zh': 'San Miguel de Cozumel、北部海岸与南部海滨公路沿线'},
}

H1 = {
 'es': 'Construcción de Villas y Hoteles en {c}', 'en': 'Villa and Hotel Construction in {c}',
 'ru': 'Строительство вилл и отелей на {c}', 'de': 'Villen- und Hotelbau auf {c}',
 'fr': 'Construction de Villas et d’Hôtels à {c}', 'zh': '{c}别墅与酒店建造',
}
TITLE = {
 'es': 'Construcción de Villas y Hoteles en {c} | Llave en Mano | Recrea',
 'en': 'Villa and Hotel Construction in {c} | Turnkey | Recrea',
 'ru': 'Строительство вилл и отелей на {c} | Под ключ | Recrea',
 'de': 'Villen- und Hotelbau auf {c} | Schlüsselfertig | Recrea',
 'fr': 'Construction de Villas et d’Hôtels à {c} | Clé en Main | Recrea',
 'zh': '{c}别墅与酒店建造 | 整包交钥匙 | Recrea',
}
DESC = {
 'es': 'Construcción de villas y hoteles boutique en {c}: precio por m² y por llave 2026, logística de materiales por ferry, permisos municipales y ambientales. 18+ años, 196+ proyectos.',
 'en': 'Villa and boutique hotel construction in {c}: 2026 cost per m² and per key, ferry logistics for materials, municipal and environmental permits. 18+ years, 196+ projects.',
 'ru': 'Строительство вилл и бутик-отелей на {c}: цена за м² и за номер 2026, логистика материалов паромом, муниципальные и экологические разрешения. 18+ лет, 196+ проектов.',
 'de': 'Villen- und Boutiquehotelbau auf {c}: Preis pro m² und pro Zimmer 2026, Materiallogistik per Fähre, kommunale und Umweltgenehmigungen. 18+ Jahre, 196+ Projekte.',
 'fr': 'Construction de villas et d’hôtels boutique à {c} : prix au m² et par clé 2026, logistique des matériaux par ferry, permis municipaux et environnementaux. 18+ ans, 196+ projets.',
 'zh': '{c}别墅与精品酒店建造：2026年每平方米及每间客房造价、材料轮渡物流、市政与环保许可。18年以上经验，196+个项目。',
}

TEXT = {
'isla-mujeres': {
 'es': 'Isla Mujeres es municipio propio y todo llega por ferry desde Puerto Juárez y Gran Puerto: concreto, acero, cancelería, mobiliario. Esa logística es el factor de costo que no aparece en el continente —hay que programar entregas, almacenar en obra y trabajar con ventanas de traslado—, y por eso el m² sale entre 15% y 25% por encima de Cancún. A cambio, la isla concentra la demanda de villas de renta alta y hotelería boutique de la zona norte.',
 'en': 'Isla Mujeres is its own municipality and everything arrives by ferry from Puerto Juárez and Gran Puerto: concrete, steel, joinery, furniture. That logistics chain is the cost factor that does not exist on the mainland — deliveries have to be scheduled, materials stored on site and work planned around crossing windows — which is why the m² runs 15% to 25% above Cancún. In exchange, the island concentrates the north zone’s demand for high-yield rental villas and boutique hospitality.',
 'ru': 'Исла-Мухерес — самостоятельный муниципалитет, и всё приходит паромом из Пуэрто-Хуарес и Гран-Пуэрто: бетон, арматура, столярка, мебель. Именно эта логистика — фактор стоимости, которого нет на материке: поставки надо планировать, материалы хранить на площадке, а работы подгонять под окна переправы. Поэтому м² выходит на 15–25% дороже Канкуна. Взамен остров концентрирует спрос севера на доходные виллы под аренду и бутик-отели.',
 'de': 'Isla Mujeres ist eine eigene Gemeinde, und alles kommt per Fähre aus Puerto Juárez und Gran Puerto: Beton, Stahl, Fenster, Möbel. Diese Logistik ist der Kostenfaktor, den es auf dem Festland nicht gibt — Lieferungen müssen getaktet, Material auf der Baustelle gelagert und Arbeiten um die Überfahrtsfenster geplant werden. Deshalb liegt der m² 15 bis 25% über Cancún. Dafür bündelt die Insel die Nachfrage des Nordens nach renditestarken Mietvillen und Boutiquehotellerie.',
 'fr': 'Isla Mujeres est une commune à part entière et tout arrive par ferry depuis Puerto Juárez et Gran Puerto : béton, acier, menuiseries, mobilier. Cette logistique est le facteur de coût qui n’existe pas sur le continent — livraisons à cadencer, stockage sur site, travaux calés sur les fenêtres de traversée — d’où un m² de 15 à 25% au-dessus de Cancún. En contrepartie, l’île concentre la demande du nord en villas locatives à fort rendement et en hôtellerie boutique.',
 'zh': 'Isla Mujeres 是独立设市的岛屿，混凝土、钢材、门窗、家具等一切材料都需从 Puerto Juárez 与 Gran Puerto 经轮渡运入。这条物流链是大陆所没有的成本因素——需排定到货批次、在工地设置堆场，并按渡运时间窗组织施工，因此每平方米造价比坎昆高出15%至25%。作为回报，该岛集中了北部地区对高收益出租别墅与精品酒店的需求。'},
'cozumel': {
 'es': 'A Cozumel el material entra únicamente por ferry desde Playa del Carmen y por los ferris de carga y vehículos: no hay carretera. Eso obliga a comprar por lotes grandes, prever almacenaje y calendarizar cada entrega, y añade entre 15% y 25% al costo por m² frente al continente. La isla vive del buceo y del crucero, así que la demanda real está en villas de renta y hoteles boutique pequeños, no en desarrollos masivos.',
 'en': 'On Cozumel materials come in only by ferry from Playa del Carmen and by the vehicle and cargo ferries: there is no road. That forces bulk purchasing, on-site storage and a scheduled delivery calendar, and adds 15% to 25% to the cost per m² versus the mainland. The island lives on diving and cruise traffic, so the real demand is rental villas and small boutique hotels, not mass developments.',
 'ru': 'На Косумель материал заходит только паромом из Плая-дель-Кармен и грузовыми/автомобильными паромами: дороги нет. Это заставляет закупать крупными партиями, предусматривать склад на площадке и планировать каждую поставку, добавляя 15–25% к цене за м² по сравнению с материком. Остров живёт дайвингом и круизами, поэтому реальный спрос — виллы под аренду и небольшие бутик-отели, а не массовая застройка.',
 'de': 'Nach Cozumel gelangt Material ausschließlich per Fähre aus Playa del Carmen sowie über Fahrzeug- und Frachtfähren: Es gibt keine Straße. Das erzwingt Großeinkauf, Lagerung auf der Baustelle und einen getakteten Lieferkalender und schlägt mit 15 bis 25% auf den m²-Preis gegenüber dem Festland durch. Die Insel lebt vom Tauchen und von Kreuzfahrten, die reale Nachfrage sind daher Mietvillen und kleine Boutiquehotels, keine Massenprojekte.',
 'fr': 'À Cozumel, les matériaux n’arrivent que par ferry depuis Playa del Carmen et par les ferries de véhicules et de fret : il n’y a pas de route. Cela impose des achats par lots, du stockage sur site et un calendrier de livraisons cadencé, et ajoute 15 à 25% au coût du m² par rapport au continent. L’île vit de la plongée et des croisières : la demande réelle porte sur des villas locatives et de petits hôtels boutique, pas sur des opérations de masse.',
 'zh': '前往 Cozumel 的材料只能经由从普拉亚德尔卡门出发的轮渡以及车辆与货运渡轮运入：岛上没有公路与大陆相连。这要求按批量采购、在工地设置堆场并严格排定每一次到货，使每平方米造价较大陆高出15%至25%。该岛以潜水与邮轮为经济支柱，真正的需求是出租别墅与小型精品酒店，而非大规模开发。'},
}

NORM = {
'isla-mujeres': {
 'es': 'Isla Mujeres es municipio propio: ahí se tramitan la constancia de uso de suelo y la licencia de construcción, con proyecto firmado por DRO y respeto al PDU insular, que limita alturas y densidad. Frente al mar aplica concesión ZOFEMAT, y buena parte de la costa está dentro del Parque Nacional Costa Occidental de Isla Mujeres, Punta Cancún y Punta Nizuc, lo que activa autorización ambiental con condiciones sobre desmonte, descargas e iluminación. Para hotel se suman licencia de funcionamiento, visto bueno de Protección Civil y registro turístico.',
 'en': 'Isla Mujeres is its own municipality: the land-use certificate and the building licence are processed there, with drawings signed by a DRO and compliance with the island PDU, which caps height and density. Beachfront requires a ZOFEMAT concession, and much of the coast falls inside the Costa Occidental de Isla Mujeres, Punta Cancún y Punta Nizuc National Park, which triggers environmental authorisation with conditions on clearing, discharges and lighting. A hotel adds the operating licence, Civil Protection sign-off and tourism registration.',
 'ru': 'Исла-Мухерес — самостоятельный муниципалитет: там оформляются справка о назначении земли и разрешение на строительство, с проектом за подписью DRO и соблюдением островного PDU, который ограничивает высоту и плотность. На первой линии нужна концессия ZOFEMAT, а значительная часть побережья входит в Национальный парк «Коста-Оксиденталь-де-Исла-Мухерес, Пунта-Канкун и Пунта-Нисук», что включает экологическое согласование с условиями по расчистке, сбросам и освещению. Для отеля добавляются лицензия на деятельность, заключение Гражданской защиты и туристическая регистрация.',
 'de': 'Isla Mujeres ist eine eigene Gemeinde: Nutzungsbescheinigung und Baugenehmigung werden dort bearbeitet, mit DRO-unterzeichneten Plänen und nach dem Insel-PDU, der Höhe und Dichte begrenzt. Am Strand gilt die ZOFEMAT-Konzession, und große Teile der Küste liegen im Nationalpark Costa Occidental de Isla Mujeres, Punta Cancún y Punta Nizuc, was eine Umweltgenehmigung mit Auflagen zu Rodung, Einleitungen und Beleuchtung auslöst. Für ein Hotel kommen Betriebslizenz, Freigabe des Zivilschutzes und Tourismusregistrierung hinzu.',
 'fr': 'Isla Mujeres est une commune à part entière : le certificat d’usage du sol et le permis de construire s’y traitent, avec des plans signés par un DRO et le respect du PDU insulaire, qui limite hauteurs et densité. En front de mer s’applique la concession ZOFEMAT, et une grande partie du littoral relève du Parc National Costa Occidental de Isla Mujeres, Punta Cancún y Punta Nizuc, ce qui déclenche une autorisation environnementale assortie de conditions sur le défrichement, les rejets et l’éclairage. Pour un hôtel s’ajoutent la licence d’exploitation, l’avis de la Protection Civile et l’enregistrement touristique.',
 'zh': 'Isla Mujeres 为独立设市：土地用途证明与施工许可均在该市办理，图纸须由 DRO 签署，并须符合限制高度与密度的岛屿 PDU 规划。海滨地块需 ZOFEMAT 特许；海岸线相当一部分位于 Costa Occidental de Isla Mujeres、Punta Cancún 与 Punta Nizuc 国家公园范围内，因而须办理环保许可，并对清林、排放与照明作出限制。若为酒店，还需经营许可、民防（Protección Civil）意见与旅游登记。'},
'cozumel': {
 'es': 'Cozumel es municipio propio, con su propio PDU y su Dirección de Desarrollo Urbano: ahí van uso de suelo y licencia con DRO. El punto crítico es ambiental: los arrecifes son Parque Nacional Arrecifes de Cozumel y la isla forma parte de una reserva de biosfera reconocida por la UNESCO, así que los proyectos cercanos a la costa se revisan con lupa —hay antecedentes de licencias detenidas y litigadas por cercanía al arrecife—. Frente al mar aplica ZOFEMAT; para hotel, licencia de funcionamiento, Protección Civil y registro turístico.',
 'en': 'Cozumel is its own municipality, with its own PDU and urban development office: land use and the licence with a DRO go there. The critical part is environmental: the reefs are the Arrecifes de Cozumel National Park and the island forms part of a UNESCO-recognised biosphere reserve, so coastal projects are examined closely — there are precedents of licences held up and litigated over proximity to the reef. Beachfront requires ZOFEMAT; a hotel adds the operating licence, Civil Protection and tourism registration.',
 'ru': 'Косумель — самостоятельный муниципалитет со своим PDU и управлением городского развития: туда идут назначение земли и лицензия с DRO. Критичен экологический блок: рифы — Национальный парк «Аррecifes de Cozumel», а сам остров входит в биосферный резерват, признанный ЮНЕСКО, поэтому прибрежные проекты рассматривают под лупой — есть прецеденты приостановленных и оспоренных в суде лицензий из-за близости к рифу. На первой линии нужна ZOFEMAT; для отеля — лицензия на деятельность, Гражданская защита и туристическая регистрация.',
 'de': 'Cozumel ist eine eigene Gemeinde mit eigenem PDU und eigener Stadtentwicklungsbehörde: Dorthin gehen Nutzungsart und Lizenz mit DRO. Kritisch ist der Umweltteil: Die Riffe sind der Nationalpark Arrecifes de Cozumel, die Insel gehört zu einem von der UNESCO anerkannten Biosphärenreservat, küstennahe Projekte werden daher genau geprüft — es gibt Präzedenzfälle gestoppter und beklagter Lizenzen wegen Riffnähe. Am Strand gilt ZOFEMAT; für ein Hotel kommen Betriebslizenz, Zivilschutz und Tourismusregistrierung hinzu.',
 'fr': 'Cozumel est une commune à part entière, avec son propre PDU et sa direction du développement urbain : usage du sol et permis avec DRO s’y déposent. Le point critique est environnemental : les récifs constituent le Parc National Arrecifes de Cozumel et l’île fait partie d’une réserve de biosphère reconnue par l’UNESCO ; les projets côtiers sont donc examinés de près — il existe des précédents de permis bloqués et contestés en justice pour proximité du récif. En front de mer, ZOFEMAT s’applique ; pour un hôtel s’ajoutent licence d’exploitation, Protection Civile et enregistrement touristique.',
 'zh': 'Cozumel 为独立设市，拥有自己的 PDU 规划与城市发展局：土地用途与带 DRO 的许可均在此办理。关键在于环保：周边珊瑚礁为 Arrecifes de Cozumel 国家公园，全岛属于联合国教科文组织认定的生物圈保护区，因此临海项目审查极为严格——此前已有因过于靠近珊瑚礁而被暂停并诉诸法院的许可先例。海滨地块需 ZOFEMAT；酒店另需经营许可、民防意见与旅游登记。'},
}
SOIL = {
'isla-mujeres': {
 'es': 'Caliza costera de baja altura sobre el nivel del mar, con manto freático somero y exposición salina en las dos caras de la isla. El estudio de mecánica de suelos define cimentación y cota de desplante; el diseño va con especificación marina completa —recubrimientos mayores, acero protegido, cancelería anodizada, vidrio para huracanes— y el agua se resuelve con cisterna generosa, porque el abasto insular no perdona errores de dimensionamiento.',
 'en': 'Coastal limestone at low elevation above sea level, with a shallow water table and salt exposure on both sides of the island. The soil study sets the foundation and the finished floor level; the design carries a full marine spec — greater cover, protected rebar, anodised joinery, hurricane-rated glazing — and water is solved with a generous cistern, because island supply does not forgive sizing mistakes.',
 'ru': 'Прибрежный известняк с малой высотой над уровнем моря, высоким уровнем грунтовых вод и солевой нагрузкой с обеих сторон острова. Геология определяет фундамент и отметку пола; проект идёт с полной морской спецификацией — увеличенный защитный слой, защищённая арматура, анодированный алюминий, ударопрочное остекление, — а вода решается ёмкой цистерной, потому что островное снабжение не прощает ошибок в расчёте.',
 'de': 'Küstenkalkstein in geringer Höhe über dem Meeresspiegel, mit hohem Grundwasserstand und Salzbelastung auf beiden Inselseiten. Das Bodengutachten legt Gründung und Höhenlage fest; geplant wird mit voller Meeresspezifikation — größere Deckung, geschützte Bewehrung, eloxierte Fenster, hurrikanfeste Verglasung — und Wasser wird über eine großzügige Zisterne gelöst, denn die Inselversorgung verzeiht keine Dimensionierungsfehler.',
 'fr': 'Calcaire côtier de faible altitude, nappe affleurante et exposition saline sur les deux faces de l’île. L’étude de sol fixe les fondations et le niveau du plancher ; le projet est conçu en spécification marine complète — enrobages renforcés, aciers protégés, menuiseries anodisées, vitrages anticycloniques — et l’eau se règle par une citerne généreuse, car l’approvisionnement insulaire ne pardonne pas les erreurs de dimensionnement.',
 'zh': '岛上为海拔较低的滨海石灰岩，地下水位浅，且岛屿两侧均受盐雾侵蚀。土力学勘察确定基础与首层标高；设计采用完整海洋环境标准——加大保护层、钢筋防护、阳极氧化门窗、抗飓风玻璃——供水则以容量充裕的蓄水池解决，因为岛上供应不容许容量测算出错。'},
'cozumel': {
 'es': 'Caliza insular muy permeable: todo lo que se infiltra llega al acuífero y, en la costa, al arrecife. Por eso el estudio de mecánica de suelos va acompañado de una solución de aguas residuales seria —planta de tratamiento o biodigestor, nunca fosa simple— y de control de escurrimientos. Estructura y herrería con especificación marina, y previsión de respaldo eléctrico: en isla, un corte prolongado es un problema operativo, sobre todo en hotel.',
 'en': 'Highly permeable island limestone: whatever infiltrates reaches the aquifer and, on the coast, the reef. That is why the soil study comes with a serious wastewater solution — treatment plant or biodigester, never a simple septic pit — and runoff control. Structure and ironwork to marine spec, and power backup planned in: on an island a long outage is an operational problem, especially for a hotel.',
 'ru': 'Островной известняк очень водопроницаем: всё, что уходит в грунт, попадает в водоносный горизонт, а на побережье — к рифу. Поэтому к геологии добавляется серьёзное решение по стокам — очистные или биодигестер, никогда простая яма — и контроль поверхностного стока. Конструктив и металл по морской спецификации, плюс резервное электропитание: на острове長 длительное отключение — операционная проблема, особенно для отеля.',
 'de': 'Sehr durchlässiger Inselkalkstein: Was versickert, erreicht den Grundwasserleiter und an der Küste das Riff. Deshalb gehört zum Bodengutachten eine belastbare Abwasserlösung — Kläranlage oder Biodigester, nie eine einfache Sickergrube — und Abflusskontrolle. Struktur und Schlosserarbeiten in Meeresspezifikation, dazu eingeplante Notstromversorgung: Auf einer Insel ist ein längerer Ausfall ein Betriebsproblem, besonders im Hotel.',
 'fr': 'Calcaire insulaire très perméable : tout ce qui s’infiltre atteint l’aquifère et, sur la côte, le récif. L’étude de sol s’accompagne donc d’une solution d’assainissement sérieuse — station de traitement ou biodigesteur, jamais une simple fosse — et d’un contrôle des ruissellements. Structure et ferronnerie en spécification marine, et secours électrique prévu : sur une île, une coupure prolongée est un problème d’exploitation, surtout en hôtel.',
 'zh': '岛上石灰岩渗透性极强：一切下渗物都会进入含水层，在沿海则流向珊瑚礁。因此除土力学勘察外，还必须配套可靠的污水方案——处理设备或生物消化池，绝不可用简易化粪坑——并控制地表径流。结构与铁件按海洋环境标准设计，并预留备用电源：在岛上，长时间断电是运营问题，酒店尤甚。'},
}

# hospitality block inserted right after the villa cost table
KEYS = {'isla-mujeres': ('$110,000 – $190,000', '$95,000 – $150,000', '$75,000 – $115,000'),
        'cozumel':      ('$105,000 – $180,000', '$90,000 – $145,000', '$72,000 – $110,000')}
BLOCK_STR = {
 'es': dict(h='Cuánto Cuesta Construir un Hotel Boutique en {c}',
   p='Costo de obra por llave (habitación terminada, sin terreno ni operación), con la logística insular ya incluida. Un hotel boutique de 12 a 20 llaves es el formato que mejor funciona en la isla.',
   th=('Nivel', 'USD por llave', 'Qué incluye'),
   rows=[('Premium / diseño de autor', 'Habitaciones grandes, alberca, spa, restaurante y áreas comunes de autor'),
         ('Boutique estándar', 'Habitación completa, alberca, terraza, cocina y áreas comunes'),
         ('Económico / hostal-hotel', 'Habitación funcional, áreas comunes simples, sin restaurante propio')],
   h2='Lo que un hotel necesita además de la obra',
   li=['Licencia de funcionamiento municipal y visto bueno de Protección Civil',
       'Planta de tratamiento de aguas residuales dimensionada al aforo',
       'Abasto y almacenamiento de agua: cisterna, bombeo y, según el caso, desalinizadora',
       'Capacidad eléctrica contratada ante CFE más planta de emergencia',
       'Cocina, lavandería y áreas de servicio con normativa sanitaria',
       'Protección contra huracanes: cristalería, cierres y protocolo de temporada']),
 'en': dict(h='What a Boutique Hotel Costs to Build in {c}',
   p='Construction cost per key (finished room, excluding land and operations), with island logistics already included. A 12 to 20 key boutique hotel is the format that works best on the island.',
   th=('Level', 'USD per key', 'What it includes'),
   rows=[('Premium / signature design', 'Large rooms, pool, spa, restaurant and designer common areas'),
         ('Standard boutique', 'Complete room, pool, terrace, kitchen and common areas'),
         ('Economy / hostel-hotel', 'Functional room, simple common areas, no in-house restaurant')],
   h2='What a hotel needs beyond the build',
   li=['Municipal operating licence and Civil Protection sign-off',
       'Wastewater treatment plant sized to occupancy',
       'Water supply and storage: cistern, pumping and, where needed, a desalination unit',
       'Contracted electrical capacity with CFE plus a backup generator',
       'Kitchen, laundry and service areas to health regulations',
       'Hurricane protection: glazing, closures and a season protocol']),
 'ru': dict(h='Сколько стоит построить бутик-отель на {c}',
   p='Стоимость стройки за номер (готовый номер, без земли и операционных расходов), островная логистика уже учтена. Формат на 12–20 номеров работает на острове лучше всего.',
   th=('Уровень', 'USD за номер', 'Что входит'),
   rows=[('Премиум / авторский дизайн', 'Большие номера, бассейн, спа, ресторан и авторские общие зоны'),
         ('Стандартный бутик', 'Полноценный номер, бассейн, терраса, кухня и общие зоны'),
         ('Эконом / хостел-отель', 'Функциональный номер, простые общие зоны, без своего ресторана')],
   h2='Что нужно отелю помимо стройки',
   li=['Муниципальная лицензия на деятельность и заключение Гражданской защиты',
       'Очистные сооружения, рассчитанные на вместимость',
       'Водоснабжение и запас: цистерна, насосная, при необходимости опреснитель',
       'Заявленная мощность в CFE плюс резервный генератор',
       'Кухня, прачечная и служебные зоны по санитарным нормам',
       'Защита от ураганов: остекление, ставни и сезонный протокол']),
 'de': dict(h='Was ein Boutiquehotel auf {c} kostet',
   p='Baukosten pro Zimmer (fertiges Zimmer, ohne Grundstück und Betrieb), Insel-Logistik bereits enthalten. Ein Boutiquehotel mit 12 bis 20 Zimmern ist auf der Insel das tragfähigste Format.',
   th=('Niveau', 'USD pro Zimmer', 'Was enthalten ist'),
   rows=[('Premium / Autorendesign', 'Große Zimmer, Pool, Spa, Restaurant und gestaltete Gemeinschaftsbereiche'),
         ('Standard-Boutique', 'Komplettes Zimmer, Pool, Terrasse, Küche und Gemeinschaftsbereiche'),
         ('Economy / Hostel-Hotel', 'Funktionales Zimmer, einfache Gemeinschaftsbereiche, ohne eigenes Restaurant')],
   h2='Was ein Hotel über den Bau hinaus braucht',
   li=['Kommunale Betriebslizenz und Freigabe des Zivilschutzes',
       'Auf die Belegung ausgelegte Abwasserbehandlungsanlage',
       'Wasserversorgung und -speicherung: Zisterne, Pumpen und ggf. Entsalzungsanlage',
       'Bei der CFE kontrahierte Leistung plus Notstromaggregat',
       'Küche, Wäscherei und Servicebereiche nach Hygienevorschriften',
       'Hurrikanschutz: Verglasung, Verschlüsse und Saisonprotokoll']),
 'fr': dict(h='Combien coûte la construction d’un hôtel boutique à {c}',
   p='Coût de construction par clé (chambre livrée, hors terrain et exploitation), logistique insulaire déjà incluse. Un hôtel boutique de 12 à 20 clés est le format qui fonctionne le mieux sur l’île.',
   th=('Niveau', 'USD par clé', 'Ce que cela comprend'),
   rows=[('Premium / design d’auteur', 'Grandes chambres, piscine, spa, restaurant et parties communes signées'),
         ('Boutique standard', 'Chambre complète, piscine, terrasse, cuisine et parties communes'),
         ('Économique / hostel-hôtel', 'Chambre fonctionnelle, parties communes simples, sans restaurant propre')],
   h2='Ce dont un hôtel a besoin au-delà du chantier',
   li=['Licence d’exploitation municipale et avis de la Protection Civile',
       'Station de traitement des eaux usées dimensionnée à la capacité',
       'Alimentation et stockage d’eau : citerne, pompage et, si besoin, dessalinisateur',
       'Puissance électrique contractée auprès de la CFE et groupe de secours',
       'Cuisine, blanchisserie et locaux de service aux normes sanitaires',
       'Protection anticyclonique : vitrages, fermetures et protocole de saison']),
 'zh': dict(h='在{c}建一家精品酒店要多少钱',
   p='按每间客房计的建造成本（交付标准客房，不含土地与运营），已包含岛屿物流因素。12至20间客房的精品酒店是岛上最可行的规模。',
   th=('档次', '每间客房（美元）', '包含内容'),
   rows=[('高端 / 名家设计', '大面积客房、泳池、水疗、餐厅与设计感公共区域'),
         ('标准精品', '完整客房、泳池、露台、厨房与公共区域'),
         ('经济 / 旅舍型酒店', '功能型客房、简约公共区域，不含自营餐厅')],
   h2='除施工之外，酒店还需要什么',
   li=['市政经营许可与民防（Protección Civil）意见',
       '按接待容量配置的污水处理设备',
       '供水与储水：蓄水池、加压系统，必要时配海水淡化装置',
       '向 CFE 申请的用电容量及应急发电机',
       '符合卫生法规的厨房、洗衣房与后勤区域',
       '防飓风措施：玻璃、封闭构件与季节应对预案']),
}

FAQ = {
'isla-mujeres': {
 'es': [('¿Por qué construir en Isla Mujeres cuesta más?', 'Por la logística: cada camión de material cruza en ferry, hay que programar entregas y almacenar en obra. Eso suma entre 15% y 25% al costo por m² frente a Cancún, y es lo primero que dimensionamos en el presupuesto.'),
        ('¿Pueden construir un hotel boutique llave en mano?', 'Sí: proyecto, licencia municipal, Protección Civil, planta de tratamiento, capacidad eléctrica ante CFE, obra y FF&E. Entregamos el hotel listo para abrir, no solo el edificio.')],
 'en': [('Why does building on Isla Mujeres cost more?', 'Logistics: every truckload of material crosses by ferry, deliveries have to be scheduled and materials stored on site. That adds 15% to 25% to the cost per m² versus Cancún, and it is the first thing we size in the budget.'),
        ('Can you build a boutique hotel turnkey?', 'Yes: design, municipal licence, Civil Protection, treatment plant, CFE capacity, construction and FF&E. We hand over a hotel ready to open, not just a building.')],
 'ru': [('Почему стройка на Исла-Мухерес дороже?', 'Из-за логистики: каждый грузовик с материалом идёт паромом, поставки надо планировать, а материал хранить на площадке. Это добавляет 15–25% к цене за м² против Канкуна, и именно это мы считаем первым в смете.'),
        ('Можете построить бутик-отель под ключ?', 'Да: проект, муниципальная лицензия, Гражданская защита, очистные, мощность в CFE, стройка и FF&E. Сдаём отель, готовый к открытию, а не просто здание.')],
 'de': [('Warum kostet Bauen auf Isla Mujeres mehr?', 'Wegen der Logistik: Jede Materialladung fährt per Fähre, Lieferungen müssen getaktet und Material auf der Baustelle gelagert werden. Das schlägt mit 15 bis 25% auf den m²-Preis gegenüber Cancún durch und wird im Budget zuerst bemessen.'),
        ('Bauen Sie ein Boutiquehotel schlüsselfertig?', 'Ja: Planung, kommunale Lizenz, Zivilschutz, Kläranlage, CFE-Leistung, Bau und FF&E. Wir übergeben ein eröffnungsbereites Hotel, nicht nur ein Gebäude.')],
 'fr': [('Pourquoi construire à Isla Mujeres coûte-t-il plus cher ?', 'La logistique : chaque camion de matériaux traverse en ferry, les livraisons se cadencent et le matériel se stocke sur site. Cela ajoute 15 à 25% au coût du m² face à Cancún, et c’est le premier poste que nous dimensionnons.'),
        ('Pouvez-vous construire un hôtel boutique clé en main ?', 'Oui : conception, permis municipal, Protection Civile, station de traitement, puissance CFE, chantier et FF&E. Nous livrons un hôtel prêt à ouvrir, pas seulement un bâtiment.')],
 'zh': [('为什么在 Isla Mujeres 建造成本更高？', '因为物流：每一车材料都要经轮渡运送，到货需排期、现场需堆放。这使每平方米造价较坎昆高出15%至25%，也是我们编制预算时首先测算的部分。'),
        ('你们能整包交付精品酒店吗？', '可以：设计、市政许可、民防审批、污水处理设备、CFE 用电容量、施工与 FF&E 家具配套。我们交付的是可直接开业的酒店，而不仅是一栋建筑。')]},
'cozumel': {
 'es': [('¿Cómo llega el material a Cozumel?', 'Por ferry desde Playa del Carmen y por los ferris de carga y vehículos. Compramos por lotes grandes, prevemos almacenaje en obra y calendarizamos cada entrega: en isla, un material faltante detiene la obra una semana, no un día.'),
        ('¿Qué tan estricto es el tema ambiental en Cozumel?', 'Mucho: los arrecifes son parque nacional y la isla forma parte de una reserva de biosfera. Los proyectos costeros se revisan a fondo, así que el expediente ambiental y el tratamiento de aguas se diseñan desde el primer plano.')],
 'en': [('How do materials reach Cozumel?', 'By ferry from Playa del Carmen and by the vehicle and cargo ferries. We buy in bulk, plan on-site storage and schedule each delivery: on an island a missing material stops the site for a week, not a day.'),
        ('How strict is the environmental side on Cozumel?', 'Very: the reefs are a national park and the island is part of a biosphere reserve. Coastal projects are reviewed thoroughly, so the environmental file and the wastewater solution are designed from the first drawing.')],
 'ru': [('Как материал попадает на Косумель?', 'Паромом из Плая-дель-Кармен и грузовыми/автомобильными паромами. Закупаем крупными партиями, планируем склад на площадке и календарь поставок: на острове нехватка материала останавливает стройку на неделю, а не на день.'),
        ('Насколько строг экологический блок на Косумеле?', 'Очень: рифы — национальный парк, остров входит в биосферный резерват. Прибрежные проекты проверяют досконально, поэтому экологическое досье и решение по стокам проектируются с первого чертежа.')],
 'de': [('Wie kommt Material nach Cozumel?', 'Per Fähre aus Playa del Carmen sowie über Fahrzeug- und Frachtfähren. Wir kaufen in Chargen, planen Lagerung auf der Baustelle und takten jede Lieferung: Auf einer Insel stoppt fehlendes Material die Baustelle eine Woche, nicht einen Tag.'),
        ('Wie streng ist der Umweltteil auf Cozumel?', 'Sehr: Die Riffe sind Nationalpark, die Insel Teil eines Biosphärenreservats. Küstenprojekte werden gründlich geprüft, deshalb entstehen Umweltakte und Abwasserlösung ab der ersten Zeichnung.')],
 'fr': [('Comment les matériaux arrivent-ils à Cozumel ?', 'Par ferry depuis Playa del Carmen et par les ferries de véhicules et de fret. Nous achetons par lots, prévoyons le stockage sur site et cadençons chaque livraison : sur une île, un matériau manquant arrête le chantier une semaine, pas un jour.'),
        ('L’environnement est-il strict à Cozumel ?', 'Très : les récifs sont un parc national et l’île fait partie d’une réserve de biosphère. Les projets côtiers sont examinés en profondeur ; le dossier environnemental et l’assainissement se conçoivent dès le premier plan.')],
 'zh': [('材料如何运抵 Cozumel？', '经由普拉亚德尔卡门出发的轮渡以及车辆与货运渡轮。我们按批量采购、规划工地堆场并排定每次到货：在岛上，缺一种材料会让工地停一周而不是一天。'),
        ('Cozumel 的环保要求有多严？', '非常严：珊瑚礁为国家公园，全岛属生物圈保护区。临海项目会被深入审查，因此环保申报材料与污水方案从第一版图纸起就同步设计。')]},
}

LINKS = {
 'es': {'isla-mujeres': [('/construccion-de-casas-playa-mujeres/','Construcción de casas en Playa Mujeres'), ('/construccion-de-casas-cancun/','Construcción de casas en Cancún'), ('/construccion-comercial-hoteles-riviera-maya/','Construcción comercial y hoteles'), ('/calculadora/','Calculadora de costos')],
        'cozumel': [('/construccion-de-casas-playa-del-carmen/','Construcción de casas en Playa del Carmen'), ('/construccion-comercial-hoteles-riviera-maya/','Construcción comercial y hoteles'), ('/construccion-eco-lodge-retiro-tulum/','Eco-lodges y retiros'), ('/calculadora/','Calculadora de costos')]},
 'en': {'isla-mujeres': [('/house-construction-playa-mujeres/','House construction in Playa Mujeres'), ('/house-construction-cancun/','House construction in Cancún'), ('/commercial-hotel-construction-riviera-maya/','Commercial and hotel construction'), ('/calculator/','Cost calculator')],
        'cozumel': [('/house-construction-playa-del-carmen/','House construction in Playa del Carmen'), ('/commercial-hotel-construction-riviera-maya/','Commercial and hotel construction'), ('/eco-lodge-wellness-retreat-construction-tulum/','Eco-lodges and retreats'), ('/calculator/','Cost calculator')]},
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
    for _z, _d in ISLAS.items():
        LINKS[_lang][_z] = [('/%s-%s/' % (_pref, _d['parent']), '%s — %s' % (hub, ml.CITY[_lang][_d['parent']])),
                            perm, ('/%s-riviera-maya/' % _pref, '%s — %s' % (hub, ml.CITY[_lang]['riviera-maya'])),
                            (_calc, names[0]), (_blog, names[1])]


ALERT = {
 'es': '<strong>Precio de construcción en {c} (2026):</strong> villas {m2} MXN/m² ({usd} USD/m²) y hoteles boutique desde {key} USD por llave, según nivel de acabados y sin incluir el terreno.',
 'en': '<strong>Construction cost in {c} (2026):</strong> villas {m2} MXN/m² ({usd} USD/m²) and boutique hotels from {key} USD per key, depending on finish level and excluding land.',
 'ru': '<strong>Стоимость строительства на {c} (2026):</strong> виллы {m2} MXN/м² ({usd} USD/м²), бутик-отели от {key} USD за номер, в зависимости от уровня отделки и без учёта участка.',
 'de': '<strong>Baukosten auf {c} (2026):</strong> Villen {m2} MXN/m² ({usd} USD/m²) und Boutiquehotels ab {key} USD pro Zimmer, je nach Ausbaustandard und ohne Grundstück.',
 'fr': '<strong>Coût de construction à {c} (2026) :</strong> villas {m2} MXN/m² ({usd} USD/m²) et hôtels boutique à partir de {key} USD par clé, selon le niveau de finition et hors terrain.',
 'zh': '<strong>{c}建造造价（2026年）：</strong>别墅每平方米 {m2} 比索（{usd} 美元），精品酒店每间客房自 {key} 美元起，按装修标准浮动，不含土地。',
}
H_COST = {
 'es': 'Cuánto Cuesta Construir una Villa en {c}', 'en': 'What a Villa Costs to Build in {c}',
 'ru': 'Сколько стоит построить виллу на {c}', 'de': 'Was eine Villa auf {c} kostet',
 'fr': 'Combien coûte la construction d’une villa à {c}', 'zh': '在{c}建一栋别墅要多少钱',
}
H_PROC = {'es': 'Proceso de Obra Paso a Paso', 'en': 'Construction Process Step by Step',
 'ru': 'Процесс стройки по этапам', 'de': 'Bauablauf Schritt für Schritt',
 'fr': 'Déroulé du chantier étape par étape', 'zh': '施工流程分步说明'}
ROW = {'es': 'Villa {n} m²', 'en': '{n} m² villa', 'ru': 'Вилла {n} м²', 'de': 'Villa {n} m²',
       'fr': 'Villa {n} m²', 'zh': '{n} 平方米别墅'}

def block(z, lang):
    b = BLOCK_STR[lang]; c = NAMES[z][lang]
    rows = '\n'.join('<tr><td>%s</td><td>%s USD</td><td>%s</td></tr>' % (r[0], k, r[1])
                     for r, k in zip(b['rows'], KEYS[z]))
    lis = '\n'.join('<li>%s</li>' % x for x in b['li'])
    return ('<h2 class="mt-4">%s</h2>\n<p>%s</p>\n'
            '<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark">'
            '<tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>\n%s\n</tbody></table></div>\n'
            '<h3 class="mt-3">%s</h3>\n<ul>\n%s\n</ul>'
            % (b['h'].format(c=c), b['p'], b['th'][0], b['th'][1], b['th'][2], rows, b['h2'], lis))


if __name__ == '__main__':
    for z in ISLAS:
        z1.ZAREA[z] = AREAS[z]; z1.ZTEXT[z] = TEXT[z]; z1.ZFAQ[z] = FAQ[z]
    for lang in LINKS:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS[lang])
    for k in ['h1', 'title', 'desc', 'block', 'alert', 'h_cost', 'row', 'h_proc']:
        ml.OVR.setdefault(k, {})
    for z, d in ISLAS.items():
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            ml.SLUG[lang][z] = SLUGS[lang][z]
            ml.NORM[lang][z] = NORM[z][lang]
            ml.SOIL[lang][z] = SOIL[z][lang]
            c = NAMES[z][lang]
            ml.OVR['h1'].setdefault(z, {})[lang] = H1[lang].format(c=c)
            ml.OVR['title'].setdefault(z, {})[lang] = TITLE[lang].format(c=c)
            ml.OVR['desc'].setdefault(z, {})[lang] = DESC[lang].format(c=c)
            ml.OVR['block'].setdefault(z, {})[lang] = block(z, lang)
            nm = ml.NUM[z]
            ml.OVR['alert'].setdefault(z, {})[lang] = ALERT[lang].format(
                c=c, m2=nm['m2'], usd=nm['usd'], key=KEYS[z][2].split(' – ')[0])
            ml.OVR['h_cost'].setdefault(z, {})[lang] = H_COST[lang].format(c=c)
            ml.OVR['row'].setdefault(z, {})[lang] = ROW[lang]
            ml.OVR['h_proc'].setdefault(z, {})[lang] = H_PROC[lang]
    ml.LOCS.extend(ISLAS)
    for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
        ch = ml.chrome(lang)
        for z in ISLAS:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-46s %6d bytes' % (out + '/', len(html)))
