#!/usr/bin/env python3
"""Villa + hospitality pages for Aldea Zamá, La Veleta, Puerto Cancún and the
Cancún Hotel Zone (2026-08-09), 6 languages each.

Same honest frame as the gated-community batch: hotel use has to be allowed by the
land use (and, inside a master plan, by the master plan too). The Hotel Zone page
goes further and says what is actually buildable there today — the strip is built
out and held by large operators, so realistic projects are reconversion, penthouses
and small boutique on the few remaining lots, not a new 300-key resort.

Villa m² bands equal each zone's existing house-construction page (same factors:
Aldea Zamá 1.20, La Veleta 1.10, Puerto Cancún 1.25, Zona Hotelera 1.30).
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
vh3 = load('gen-casas-villas-hoteles3.py', 'vh3')
vh1 = vh3.vh1; il = vh3.il; z1 = vh3.z1; ml = vh3.ml
SLUG_PREFIX = vh1.SLUG_PREFIX
ROWS = vh3.ROWS

ZONES = {
 'vh-aldea-zama':           dict(parent='tulum',  f=1.20, perm='3–5', zone='aldea-zama'),
 'vh-la-veleta':            dict(parent='tulum',  f=1.10, perm='3–5', zone='la-veleta'),
 'vh-puerto-cancun':        dict(parent='cancun', f=1.25, perm='3–5', zone='puerto-cancun'),
 'vh-zona-hotelera-cancun': dict(parent='cancun', f=1.30, perm='3–5', zone='zona-hotelera-cancun'),
}
BASE_SLUG = {k: d['zone'] for k, d in ZONES.items()}

NAMES = {
 'vh-aldea-zama': {'es': 'Aldea Zamá', 'en': 'Aldea Zamá', 'ru': 'Альдеа-Зама', 'de': 'Aldea Zamá', 'fr': 'Aldea Zamá', 'zh': 'Aldea Zamá'},
 'vh-la-veleta': {'es': 'La Veleta', 'en': 'La Veleta', 'ru': 'Ла-Велете', 'de': 'La Veleta', 'fr': 'La Veleta', 'zh': 'La Veleta'},
 'vh-puerto-cancun': {'es': 'Puerto Cancún', 'en': 'Puerto Cancún', 'ru': 'Пуэрто-Канкуне', 'de': 'Puerto Cancún', 'fr': 'Puerto Cancún', 'zh': 'Puerto Cancún'},
 'vh-zona-hotelera-cancun': {'es': 'la Zona Hotelera de Cancún', 'en': 'the Cancún Hotel Zone', 'ru': 'Отельной зоне Канкуна',
                             'de': 'der Hotelzone von Cancún', 'fr': 'la Zone Hôtelière de Cancún', 'zh': '坎昆酒店区'},
}
AREAS = {
 'vh-aldea-zama': {'es': 'Aldea Zamá y sus secciones residenciales', 'en': 'Aldea Zamá and its residential sections',
   'ru': 'Альдеа-Зама и её жилых секциях', 'de': 'Aldea Zamá und seinen Wohnabschnitten',
   'fr': 'Aldea Zamá et ses sections résidentielles', 'zh': 'Aldea Zamá 及其住宅区段'},
 'vh-la-veleta': {'es': 'La Veleta y sus manzanas en desarrollo', 'en': 'La Veleta and its developing blocks',
   'ru': 'Ла-Велете и её застраивающихся кварталах', 'de': 'La Veleta und seinen wachsenden Blöcken',
   'fr': 'La Veleta et ses îlots en développement', 'zh': 'La Veleta 及其在建街区'},
 'vh-puerto-cancun': {'es': 'Puerto Cancún, su marina y sus fraccionamientos privados', 'en': 'Puerto Cancún, its marina and private phases',
   'ru': 'Пуэрто-Канкуне, его марине и частных секторах', 'de': 'Puerto Cancún, seiner Marina und den privaten Abschnitten',
   'fr': 'Puerto Cancún, sa marina et ses tranches privées', 'zh': 'Puerto Cancún、其码头与各私人区段'},
 'vh-zona-hotelera-cancun': {'es': 'la Zona Hotelera, Isla Dorada y Punta Nizuc', 'en': 'the Hotel Zone, Isla Dorada and Punta Nizuc',
   'ru': 'Отельной зоне, Исла-Дорада и Пунта-Нисук', 'de': 'der Hotelzone, Isla Dorada und Punta Nizuc',
   'fr': 'la Zone Hôtelière, Isla Dorada et Punta Nizuc', 'zh': '酒店区、Isla Dorada 与 Punta Nizuc'},
}
# branded / premium boutique / entry boutique, USD per key
KEYS = {
 'vh-aldea-zama':           ('$140,000 – $230,000', '$110,000 – $175,000', '$85,000 – $135,000'),
 'vh-la-veleta':            ('$120,000 – $200,000', '$95,000 – $150,000', '$72,000 – $115,000'),
 'vh-puerto-cancun':        ('$150,000 – $250,000', '$115,000 – $185,000', '$90,000 – $140,000'),
 'vh-zona-hotelera-cancun': ('$170,000 – $290,000', '$130,000 – $210,000', '$100,000 – $160,000'),
}

TEXT = {
'vh-aldea-zama': {
 'es': 'Aldea Zamá es la zona de Tulum donde la renta corta ya está consolidada: servicios subterráneos, calles terminadas y demanda todo el año. Por eso funciona igual de bien la villa de renta que el hotel boutique de 8 a 20 llaves con concepto eco-chic. La condición es la de siempre en Tulum: uso de suelo que admita el giro y ruta ambiental de SEMA resuelta antes de abrir, no después.',
 'en': 'Aldea Zamá is the part of Tulum where short-term rental is already consolidated: underground services, finished streets and year-round demand. That is why a rental villa works as well as an 8 to 20 key eco-chic boutique hotel. The condition is the usual one in Tulum: land use that allows the operation and the SEMA route resolved before opening, not after.',
 'ru': 'Альдеа-Зама — район Тулума, где посуточная аренда уже сложилась: подземные коммуникации, готовые улицы и спрос круглый год. Поэтому одинаково хорошо работают и вилла под аренду, и бутик-отель на 8–20 номеров в эко-шик концепции. Условие обычное для Тулума: назначение земли, допускающее профиль, и маршрут SEMA, закрытый до открытия, а не после.',
 'de': 'Aldea Zamá ist der Teil Tulums, in dem die Kurzzeitvermietung bereits etabliert ist: unterirdische Versorgung, fertige Straßen und ganzjährige Nachfrage. Deshalb funktioniert die Mietvilla ebenso gut wie ein Eco-Chic-Boutiquehotel mit 8 bis 20 Zimmern. Die Bedingung ist die übliche in Tulum: eine Nutzungsart, die den Betrieb zulässt, und der SEMA-Weg vor der Eröffnung geklärt, nicht danach.',
 'fr': 'Aldea Zamá est le secteur de Tulum où la location courte est déjà installée : réseaux enterrés, rues finies et demande toute l’année. C’est pourquoi la villa locative fonctionne aussi bien qu’un hôtel boutique éco-chic de 8 à 20 clés. La condition est la même qu’ailleurs à Tulum : un usage du sol qui autorise l’exploitation et le parcours SEMA réglé avant l’ouverture, pas après.',
 'zh': 'Aldea Zamá 是图卢姆短租业态最成熟的片区：管线入地、道路完善、全年有需求。因此出租别墅与8至20间客房的生态时尚风精品酒店同样可行。前提与图卢姆其他地方一致：土地用途须允许该经营业态，且 SEMA 流程要在开业前走完，而不是开业后补。'},
'vh-la-veleta': {
 'es': 'La Veleta es la entrada más accesible al mercado de Tulum: terreno más barato y crecimiento rápido, con la contrapartida de que los servicios varían calle por calle. Para villa de renta o boutique pequeño es la mejor relación inversión/tarifa de la ciudad, siempre que la revisión previa sea seria: agua, CFE, acceso pavimentado, uso de suelo y situación legal del predio antes de comprar.',
 'en': 'La Veleta is the most accessible entry into the Tulum market: cheaper land and fast growth, with the trade-off that services vary street by street. For a rental villa or a small boutique it is the city’s best investment-to-rate ratio — provided the pre-purchase check is serious: water, CFE, paved access, land use and the lot’s legal status.',
 'ru': 'Ла-Велета — самый доступный вход на рынок Тулума: земля дешевле, рост быстрый, но коммуникации отличаются от улицы к улице. Для виллы под аренду или небольшого бутика это лучшее соотношение вложений и тарифа в городе — при условии серьёзной проверки до покупки: вода, CFE, асфальтированный подъезд, назначение земли и юридический статус участка.',
 'de': 'La Veleta ist der günstigste Einstieg in den Markt von Tulum: billigeres Land und schnelles Wachstum, dafür variiert die Versorgung von Straße zu Straße. Für eine Mietvilla oder ein kleines Boutiquehotel das beste Verhältnis von Investition zu Rate — vorausgesetzt, die Vorprüfung ist ernsthaft: Wasser, CFE, befestigte Zufahrt, Nutzungsart und Rechtslage des Grundstücks.',
 'fr': 'La Veleta est l’entrée la plus accessible au marché de Tulum : foncier moins cher et croissance rapide, avec pour contrepartie des réseaux qui varient d’une rue à l’autre. Pour une villa locative ou un petit boutique, c’est le meilleur rapport investissement/tarif de la ville — à condition que la vérification préalable soit sérieuse : eau, CFE, accès goudronné, usage du sol et situation juridique du terrain.',
 'zh': 'La Veleta 是进入图卢姆市场门槛最低的选择：地价更低、增长迅速，代价是市政配套逐街不同。就出租别墅或小型精品酒店而言，这里的投入与房价之比全城最优——前提是购前核查要做扎实：供水、CFE 供电、硬化道路接入、土地用途与地块法律状态。'},
'vh-puerto-cancun': {
 'es': 'Puerto Cancún combina marina, campo de golf y fraccionamientos cerrados a minutos del aeropuerto: para villa es el producto residencial más sólido de Cancún, y para hospedaje funciona el formato de residencias con servicio o condo-hotel donde el uso de suelo lo permite. Todo pasa por dos filtros: FONATUR, por el origen del suelo, y el reglamento del desarrollo. Frente al canal o al mar se suma ZOFEMAT y especificación anticorrosiva completa.',
 'en': 'Puerto Cancún combines a marina, a golf course and gated phases minutes from the airport: for a villa it is Cancún’s most solid residential product, and for lodging the working format is serviced residences or condo-hotel where land use allows it. Everything passes two filters: FONATUR, because of the land’s origin, and the development’s own rules. Facing the canal or the sea adds ZOFEMAT and a full anti-corrosion spec.',
 'ru': 'Пуэрто-Канкун сочетает марину, поле для гольфа и закрытые секторы в минутах от аэропорта: для виллы это самый устойчивый жилой продукт Канкуна, а для размещения работает формат резиденций с сервисом или кондо-отеля там, где допускает назначение земли. Всё проходит два фильтра: FONATUR — из-за происхождения земли — и регламент застройки. У канала или моря добавляются ZOFEMAT и полная антикоррозийная спецификация.',
 'de': 'Puerto Cancún verbindet Marina, Golfplatz und geschlossene Abschnitte, Minuten vom Flughafen: Für eine Villa das solideste Wohnprodukt Cancúns, für Beherbergung funktionieren Serviced Residences oder Condo-Hotel, wo die Nutzungsart es zulässt. Alles läuft durch zwei Filter: FONATUR wegen der Herkunft des Bodens und die Satzung der Anlage. Am Kanal oder Meer kommen ZOFEMAT und volle Korrosionsschutzspezifikation hinzu.',
 'fr': 'Puerto Cancún associe marina, golf et tranches fermées à quelques minutes de l’aéroport : pour une villa, c’est le produit résidentiel le plus solide de Cancún ; pour l’hébergement, le format qui fonctionne est la résidence avec services ou le condo-hôtel là où l’usage du sol l’autorise. Tout passe par deux filtres : FONATUR, du fait de l’origine du foncier, et le règlement du développement. Sur le canal ou la mer s’ajoutent la ZOFEMAT et une spécification anticorrosion complète.',
 'zh': 'Puerto Cancún 兼具码头、高尔夫球场与距机场数分钟的封闭区段：作为别墅产品，它是坎昆最稳健的选择；作为住宿业态，在土地用途允许之处，可行形态是带服务的住宅或产权式酒店。所有项目都要过两道关：因土地来源而需的 FONATUR，以及开发区自身规约。面向运河或海面的地块另需 ZOFEMAT 与完整防腐做法。'},
'vh-zona-hotelera-cancun': {
 'es': 'Aquí conviene decir lo que casi nadie dice: la Zona Hotelera está prácticamente construida y el suelo disponible es escaso y caro, en manos de grandes operadores. Lo que sí se hace todos los días —y es donde entramos— es reconversión y remodelación integral de propiedades existentes, penthouses y residencias frente al mar, y proyectos boutique en los pocos predios que quedan. Suelo FONATUR, ZOFEMAT en playa y ventanas de acceso y horario por el tráfico turístico.',
 'en': 'Here it is worth saying what few people say: the Hotel Zone is essentially built out, and the land still available is scarce, expensive and held by large operators. What does happen every day — and where we come in — is reconversion and full renovation of existing properties, beachfront penthouses and residences, and boutique projects on the few remaining lots. FONATUR land, ZOFEMAT on the beach and restricted access and working-hour windows because of tourist traffic.',
 'ru': 'Здесь стоит сказать то, чего обычно не говорят: Отельная зона практически застроена, свободная земля редка, дорога и находится у крупных операторов. Что действительно происходит каждый день — и где работаем мы — это реконверсия и капитальная реконструкция существующих объектов, пентхаусы и резиденции у моря, а также бутик-проекты на немногих оставшихся участках. Земля FONATUR, ZOFEMAT на пляже и окна доступа и часов работ из-за туристического трафика.',
 'de': 'Hier gehört gesagt, was kaum jemand sagt: Die Hotelzone ist im Wesentlichen bebaut, verfügbares Land ist knapp, teuer und in der Hand großer Betreiber. Was täglich stattfindet — und wo wir ansetzen — ist Umnutzung und Komplettsanierung bestehender Objekte, Penthouses und Strandresidenzen sowie Boutiqueprojekte auf den wenigen verbliebenen Grundstücken. FONATUR-Land, ZOFEMAT am Strand und beschränkte Zufahrts- und Arbeitszeitfenster wegen des Touristenverkehrs.',
 'fr': 'Il faut ici dire ce que peu de gens disent : la Zone Hôtelière est pour l’essentiel construite, et le foncier encore disponible est rare, cher et détenu par de grands opérateurs. Ce qui se fait tous les jours — et c’est là que nous intervenons — c’est la reconversion et la rénovation intégrale de biens existants, des penthouses et résidences en front de mer, et des projets boutique sur les rares lots restants. Terrain FONATUR, ZOFEMAT sur la plage et fenêtres d’accès et d’horaires restreintes du fait du trafic touristique.',
 'zh': '这里有必要说一句少有人讲的实话：酒店区基本已建成，可供开发的土地稀少、昂贵，且多掌握在大型运营商手中。真正每天都在发生、也是我们切入的领域，是既有物业的功能改造与整体翻新、海滨顶层公寓与住宅，以及在少数剩余地块上的精品项目。土地属 FONATUR，沙滩需 ZOFEMAT，并因旅游车流而对进出与作业时段设有限制窗口。'},
}

NORM = {
'vh-aldea-zama': {
 'es': 'Uso de suelo y licencia municipal de Tulum con DRO, más autorización ambiental de SEMA, que aplica en la práctica totalidad de la zona. Para hospedaje, primero la constancia de uso de suelo con giro; después licencia de funcionamiento, visto bueno de Protección Civil, capacidad eléctrica ante CFE por aforo y registro turístico. Con SEMA de por medio, de 3 a 5 meses de permisos: el trámite arranca con el anteproyecto.',
 'en': 'Land use and the Tulum municipal licence with a DRO, plus SEMA environmental authorisation, which applies across practically the whole area. For lodging: first the land-use certificate with the right use; then the operating licence, Civil Protection sign-off, CFE capacity by occupancy and tourism registration. With SEMA involved, 3 to 5 months of permits — the process starts with the concept design.',
 'ru': 'Назначение земли и муниципальная лицензия Тулума с DRO, плюс экологическая авторизация SEMA, действующая практически по всей зоне. Для размещения сначала справка о назначении земли с нужным профилем, затем лицензия на деятельность, заключение Гражданской защиты, мощность в CFE под вместимость и туристическая регистрация. С SEMA — 3–5 месяцев на разрешения: процедура стартует вместе с эскизом.',
 'de': 'Nutzungsart und kommunale Lizenz von Tulum mit DRO, dazu die SEMA-Umweltgenehmigung, die praktisch im gesamten Gebiet gilt. Für Beherbergung zuerst die Nutzungsbescheinigung mit passender Nutzung, danach Betriebslizenz, Freigabe des Zivilschutzes, CFE-Leistung nach Belegung und Tourismusregistrierung. Mit der SEMA 3 bis 5 Monate Genehmigungen — das Verfahren startet mit dem Entwurf.',
 'fr': 'Usage du sol et permis municipal de Tulum avec DRO, plus l’autorisation environnementale de la SEMA, applicable sur la quasi-totalité du secteur. Pour l’hébergement : d’abord le certificat d’usage du sol avec la vocation adéquate ; puis licence d’exploitation, avis de la Protection Civile, puissance CFE selon capacité et enregistrement touristique. Avec la SEMA, 3 à 5 mois de permis — la procédure démarre dès l’avant-projet.',
 'zh': '土地用途与带 DRO 的图卢姆市政许可，另加几乎覆盖全片区的 SEMA 环保许可。做住宿业态：先取得载明相应用途的土地用途证明，再办经营许可、民防意见、按容量核定的 CFE 用电容量与旅游登记。涉及 SEMA 时许可周期为3至5个月——报批自方案阶段即启动。'},
'vh-la-veleta': {
 'es': 'Además de uso de suelo, licencia de Tulum con DRO y autorización de SEMA en la mayoría de los predios, en La Veleta hay un paso previo que no es opcional: verificar factibilidad real de agua, drenaje y CFE en esa calle, más la situación legal del terreno. Para hospedaje se suman giro en el uso de suelo, licencia de funcionamiento, Protección Civil, capacidad eléctrica y registro turístico.',
 'en': 'Beyond land use, the Tulum licence with a DRO and SEMA authorisation on most lots, La Veleta has a prior step that is not optional: verifying real feasibility of water, drainage and CFE on that particular street, plus the lot’s legal status. Lodging adds the right use in the land-use certificate, the operating licence, Civil Protection, electrical capacity and tourism registration.',
 'ru': 'Помимо назначения земли, лицензии Тулума с DRO и авторизации SEMA на большинстве участков, в Ла-Велете есть обязательный предварительный шаг: проверить реальную возможность подключения воды, канализации и CFE именно на этой улице, а также юридический статус участка. Для размещения добавляются профиль в назначении земли, лицензия на деятельность, Гражданская защита, мощность и туристическая регистрация.',
 'de': 'Neben Nutzungsart, Lizenz von Tulum mit DRO und SEMA-Genehmigung auf den meisten Grundstücken gibt es in La Veleta einen Vorabschritt, der nicht optional ist: die tatsächliche Machbarkeit von Wasser, Kanalisation und CFE in genau dieser Straße prüfen, dazu die Rechtslage des Grundstücks. Für Beherbergung kommen die passende Nutzung, Betriebslizenz, Zivilschutz, Leistung und Tourismusregistrierung hinzu.',
 'fr': 'Outre l’usage du sol, le permis de Tulum avec DRO et l’autorisation SEMA sur la plupart des lots, La Veleta impose une étape préalable non optionnelle : vérifier la faisabilité réelle de l’eau, de l’assainissement et de la CFE dans cette rue précise, ainsi que la situation juridique du terrain. Pour l’hébergement s’ajoutent la vocation adéquate, la licence d’exploitation, la Protection Civile, la puissance et l’enregistrement touristique.',
 'zh': '除土地用途、带 DRO 的图卢姆许可以及多数地块所需的 SEMA 许可外，La Veleta 还有一个不可省略的前置步骤：核实该条街道上供水、排水与 CFE 的实际接入可行性，以及地块的法律状态。做住宿业态还需在土地用途中载明相应业态，并办理经营许可、民防意见、用电容量与旅游登记。'},
'vh-puerto-cancun': {
 'es': 'Licencia de construcción en Benito Juárez con proyecto avalado por DRO, visto bueno de FONATUR por el origen del suelo y, en lotes frente al canal o al mar, concesión ZOFEMAT. A eso se suma el reglamento del desarrollo, con su comité de diseño. Para hospedaje: uso de suelo con giro —solo en predios que lo admitan—, licencia de funcionamiento, Protección Civil, capacidad eléctrica por aforo y registro turístico.',
 'en': 'Building licence in Benito Juárez with a DRO-endorsed project, FONATUR sign-off because of the land’s origin and, on canal- or sea-facing lots, a ZOFEMAT concession. On top of that, the development’s rules and its design committee. For lodging: land use with the right designation — only on lots that allow it — the operating licence, Civil Protection, occupancy-based electrical capacity and tourism registration.',
 'ru': 'Разрешение на строительство в Benito Juárez с проектом за подписью DRO, согласование FONATUR из-за происхождения земли и, на участках у канала или моря, концессия ZOFEMAT. Плюс регламент застройки с комитетом по дизайну. Для размещения: назначение земли с нужным профилем — только на участках, где он допускается, — лицензия на деятельность, Гражданская защита, мощность под вместимость и туристическая регистрация.',
 'de': 'Baugenehmigung in Benito Juárez mit DRO-geprüftem Projekt, FONATUR-Freigabe wegen der Herkunft des Bodens und bei Kanal- oder Meergrundstücken eine ZOFEMAT-Konzession. Dazu die Satzung der Anlage mit ihrem Gestaltungsbeirat. Für Beherbergung: Nutzungsart mit passender Widmung — nur auf Grundstücken, die sie zulassen —, Betriebslizenz, Zivilschutz, belegungsabhängige Leistung und Tourismusregistrierung.',
 'fr': 'Permis de construire à Benito Juárez avec projet validé par un DRO, accord FONATUR du fait de l’origine du foncier et, sur les lots donnant sur le canal ou la mer, concession ZOFEMAT. S’y ajoutent le règlement du développement et son comité d’architecture. Pour l’hébergement : usage du sol avec la vocation adéquate — uniquement sur les lots qui l’admettent —, licence d’exploitation, Protection Civile, puissance selon capacité et enregistrement touristique.',
 'zh': '在 Benito Juárez 办理施工许可，项目须由 DRO 背书；因土地来源需 FONATUR 批准；面向运河或海面的地块需 ZOFEMAT 特许。此外还有开发区规约及其设计委员会。做住宿业态：需取得载明相应业态的土地用途（仅限允许的地块），并办理经营许可、民防意见、按容量核定的用电容量与旅游登记。'},
'vh-zona-hotelera-cancun': {
 'es': 'Suelo FONATUR con revisión de imagen urbana y densidad, licencia de Benito Juárez con DRO y concesión ZOFEMAT en predios de playa. En reconversión y remodelación de propiedades existentes se suman el reglamento del condominio u operador, las ventanas de acceso y horario de obra por el tráfico turístico y, si el destino es hospedaje, licencia de funcionamiento, Protección Civil, capacidad eléctrica por aforo y registro turístico.',
 'en': 'FONATUR land with urban-image and density review, the Benito Juárez licence with a DRO and a ZOFEMAT concession on beach lots. For reconversion and renovation of existing properties, add the condominium or operator by-laws, the access and working-hour windows imposed by tourist traffic and, if the use is lodging, the operating licence, Civil Protection, occupancy-based electrical capacity and tourism registration.',
 'ru': 'Земля FONATUR с проверкой городского облика и плотности, лицензия Benito Juárez с DRO и концессия ZOFEMAT на пляжных участках. При реконверсии и реконструкции существующих объектов добавляются регламент кондоминиума или оператора, окна доступа и часов работ из-за туристического трафика и — если назначение гостиничное — лицензия на деятельность, Гражданская защита, мощность под вместимость и туристическая регистрация.',
 'de': 'FONATUR-Land mit Prüfung von Stadtbild und Dichte, Lizenz von Benito Juárez mit DRO und ZOFEMAT-Konzession bei Strandgrundstücken. Bei Umnutzung und Sanierung bestehender Objekte kommen die Satzung der Eigentümergemeinschaft oder des Betreibers, die vom Touristenverkehr bestimmten Zufahrts- und Arbeitszeitfenster und — bei Beherbergungsnutzung — Betriebslizenz, Zivilschutz, belegungsabhängige Leistung und Tourismusregistrierung hinzu.',
 'fr': 'Terrain FONATUR avec examen de l’image urbaine et de la densité, permis de Benito Juárez avec DRO et concession ZOFEMAT sur les lots de plage. En reconversion et rénovation de biens existants s’ajoutent le règlement de copropriété ou de l’exploitant, les fenêtres d’accès et d’horaires imposées par le trafic touristique et, si la destination est l’hébergement, licence d’exploitation, Protection Civile, puissance selon capacité et enregistrement touristique.',
 'zh': '土地属 FONATUR，需审查城市风貌与容积密度；在 Benito Juárez 办理带 DRO 的许可；沙滩地块需 ZOFEMAT 特许。既有物业的功能改造与翻新，还须遵守业主委员会或运营商规约、因旅游车流而设的进出与作业时段窗口；若用于住宿经营，另需经营许可、民防意见、按容量核定的用电容量与旅游登记。'},
}

FAQ = {
'vh-aldea-zama': {
 'es': [('¿Villa de renta u hotel boutique en Aldea Zamá?', 'Ambos funcionan: la zona tiene la demanda de renta corta más consolidada de Tulum. La villa exige menos estructura operativa; el boutique de 8 a 20 llaves rinde más por m² si hay equipo para operarlo.'),
        ('¿Cuánto cuesta por llave aquí?', 'De $85,000 a $230,000 USD según nivel, con estándar eco-chic (chukum, madera dura, diseño bioclimático) que la zona da por hecho.')],
 'en': [('Rental villa or boutique hotel in Aldea Zamá?', 'Both work: the area has Tulum’s most consolidated short-term rental demand. The villa needs less operating structure; an 8 to 20 key boutique returns more per m² if you have a team to run it.'),
        ('What is the cost per key here?', 'From $85,000 to $230,000 USD depending on level, with the eco-chic standard (chukum, hardwood, bioclimatic design) the area takes for granted.')],
 'ru': [('Вилла под аренду или бутик-отель в Альдеа-Зама?', 'Работает и то, и другое: здесь самый сложившийся спрос на посуточную аренду в Тулуме. Вилла требует меньше операционной структуры; бутик на 8–20 номеров даёт больше с м², если есть команда для управления.'),
        ('Сколько стоит здесь номер?', 'От $85,000 до $230,000 USD в зависимости от уровня, при эко-шик стандарте (чукум, твёрдая древесина, биоклиматика), который зона считает нормой.')],
 'de': [('Mietvilla oder Boutiquehotel in Aldea Zamá?', 'Beides funktioniert: Das Gebiet hat die etablierteste Kurzzeitmietnachfrage Tulums. Die Villa braucht weniger Betriebsstruktur; ein Boutique mit 8 bis 20 Zimmern bringt mehr pro m², wenn ein Team es führt.'),
        ('Wie hoch sind die Kosten pro Zimmer?', 'Von $85.000 bis $230.000 USD je nach Niveau, beim Eco-Chic-Standard (Chukum, Hartholz, bioklimatisches Design), den die Zone voraussetzt.')],
 'fr': [('Villa locative ou hôtel boutique à Aldea Zamá ?', 'Les deux fonctionnent : le secteur a la demande locative courte la plus établie de Tulum. La villa demande moins de structure d’exploitation ; un boutique de 8 à 20 clés rend davantage au m² si une équipe le fait tourner.'),
        ('Quel coût par clé ici ?', 'De 85 000 à 230 000 USD selon le niveau, avec le standard éco-chic (chukum, bois dur, conception bioclimatique) que le secteur tient pour acquis.')],
 'zh': [('在 Aldea Zamá 该做出租别墅还是精品酒店？', '两者都可行：该片区拥有图卢姆最成熟的短租需求。别墅所需运营架构更轻；8至20间客房的精品酒店单位面积回报更高，前提是有团队运营。'),
        ('这里每间客房造价是多少？', '按档次 85,000 至 230,000 美元，且需满足该片区默认的生态时尚标准（chukum、硬木、生态气候设计）。')]},
'vh-la-veleta': {
 'es': [('¿Qué reviso antes de comprar en La Veleta para un proyecto de renta?', 'Factibilidad de agua, drenaje y CFE en esa calle concreta, acceso pavimentado, uso de suelo y situación legal. En La Veleta cambia de manzana en manzana, y de eso depende el costo real.'),
        ('¿Cuánto cuesta por llave?', 'De $72,000 a $200,000 USD. Es la entrada más accesible de Tulum manteniendo tarifa de zona premium.')],
 'en': [('What should I check before buying in La Veleta for a rental project?', 'Feasibility of water, drainage and CFE on that specific street, paved access, land use and legal status. In La Veleta it changes block by block, and the real cost depends on it.'),
        ('What is the cost per key?', 'From $72,000 to $200,000 USD. It is Tulum’s most accessible entry while still commanding premium-zone rates.')],
 'ru': [('Что проверить до покупки в Ла-Велете под проект аренды?', 'Возможность подключения воды, канализации и CFE именно на этой улице, асфальтированный подъезд, назначение земли и юридический статус. В Ла-Велете это меняется от квартала к кварталу, и от этого зависит реальная стоимость.'),
        ('Сколько стоит номер?', 'От $72,000 до $200,000 USD. Самый доступный вход в Тулуме при тарифе премиальной зоны.')],
 'de': [('Was prüfe ich vor dem Kauf in La Veleta für ein Vermietungsprojekt?', 'Machbarkeit von Wasser, Kanalisation und CFE in genau dieser Straße, befestigte Zufahrt, Nutzungsart und Rechtslage. In La Veleta ändert sich das von Block zu Block — davon hängen die realen Kosten ab.'),
        ('Wie hoch sind die Kosten pro Zimmer?', 'Von $72.000 bis $200.000 USD. Der günstigste Einstieg in Tulum bei Raten einer Premiumlage.')],
 'fr': [('Que vérifier avant d’acheter à La Veleta pour un projet locatif ?', 'La faisabilité de l’eau, de l’assainissement et de la CFE dans cette rue précise, l’accès goudronné, l’usage du sol et la situation juridique. À La Veleta, cela change d’un îlot à l’autre, et le coût réel en dépend.'),
        ('Quel coût par clé ?', 'De 72 000 à 200 000 USD. L’entrée la plus accessible de Tulum tout en conservant des tarifs de zone premium.')],
 'zh': [('在 La Veleta 做出租项目，购地前要核查什么？', '该条街道上供水、排水与 CFE 的接入可行性、硬化道路接入、土地用途与法律状态。在 La Veleta 这些逐街区不同，实际造价也随之变化。'),
        ('每间客房造价是多少？', '72,000 至 200,000 美元。这是图卢姆门槛最低的入手方式，同时仍可获得高端片区的房价水平。')]},
'vh-puerto-cancun': {
 'es': [('¿Se puede operar hospedaje en Puerto Cancún?', 'Solo donde el uso de suelo y el reglamento del desarrollo lo permitan; el formato viable suele ser residencias con servicio o condo-hotel. Lo confirmamos con la constancia de uso de suelo antes de diseñar.'),
        ('¿Qué cambia por ser suelo FONATUR?', 'Se suma su visto bueno a la licencia de Benito Juárez, con revisión de imagen urbana y densidad, y frente al canal o al mar entra la concesión ZOFEMAT.')],
 'en': [('Can you operate lodging in Puerto Cancún?', 'Only where land use and the development’s rules allow it; the viable format is usually serviced residences or condo-hotel. We confirm it with the land-use certificate before designing.'),
        ('What changes because it is FONATUR land?', 'Their sign-off is added to the Benito Juárez licence, with urban-image and density review, and canal- or sea-facing lots require a ZOFEMAT concession.')],
 'ru': [('Можно ли вести размещение в Пуэрто-Канкуне?', 'Только там, где допускают назначение земли и регламент застройки; рабочий формат обычно — резиденции с сервисом или кондо-отель. Подтверждаем справкой о назначении земли до проектирования.'),
        ('Что меняет земля FONATUR?', 'К лицензии Benito Juárez добавляется их согласование с проверкой городского облика и плотности, а у канала или моря — концессия ZOFEMAT.')],
 'de': [('Kann man in Puerto Cancún Beherbergung betreiben?', 'Nur wo Nutzungsart und Anlagensatzung es zulassen; das machbare Format sind meist Serviced Residences oder Condo-Hotel. Wir prüfen das vor dem Entwurf mit der Nutzungsbescheinigung.'),
        ('Was ändert FONATUR-Land?', 'Deren Freigabe kommt zur Lizenz von Benito Juárez hinzu, mit Prüfung von Stadtbild und Dichte; an Kanal oder Meer zusätzlich die ZOFEMAT-Konzession.')],
 'fr': [('Peut-on exploiter de l’hébergement à Puerto Cancún ?', 'Uniquement là où l’usage du sol et le règlement du développement l’autorisent ; le format viable est en général la résidence avec services ou le condo-hôtel. Nous le confirmons via le certificat d’usage du sol avant de concevoir.'),
        ('Qu’est-ce qui change avec un terrain FONATUR ?', 'Leur accord s’ajoute au permis de Benito Juárez, avec examen de l’image urbaine et de la densité ; sur le canal ou la mer, la concession ZOFEMAT s’applique.')],
 'zh': [('在 Puerto Cancún 可以做住宿经营吗？', '仅限土地用途与开发区规约允许之处；可行形态通常是带服务的住宅或产权式酒店。我们会在设计前以土地用途证明予以确认。'),
        ('地处 FONATUR 土地有何不同？', '在 Benito Juárez 许可之外需增加其批准，并审查城市风貌与容积密度；面向运河或海面的地块还需 ZOFEMAT 特许。')]},
'vh-zona-hotelera-cancun': {
 'es': [('¿Todavía se puede construir un hotel nuevo en la Zona Hotelera?', 'Muy poco: el suelo disponible es escaso, caro y en manos de grandes operadores. Lo realista hoy es reconversión y remodelación integral, penthouses y residencias frente al mar, o boutique en los pocos predios que quedan.'),
        ('¿Qué complica una obra aquí?', 'Los accesos y horarios: se trabaja con ventanas acordadas por el tráfico turístico y el condominio u operador. Eso, más la especificación marina completa, es lo que mueve el costo por llave.')],
 'en': [('Can you still build a new hotel in the Hotel Zone?', 'Barely: available land is scarce, expensive and held by large operators. What is realistic today is reconversion and full renovation, beachfront penthouses and residences, or a boutique on one of the few remaining lots.'),
        ('What makes a site here difficult?', 'Access and hours: you work within windows agreed around tourist traffic and the condominium or operator. That, plus the full marine spec, is what moves the cost per key.')],
 'ru': [('Можно ли ещё построить новый отель в Отельной зоне?', 'Почти нет: свободная земля редка, дорога и у крупных операторов. Реалистично сегодня — реконверсия и капитальная реконструкция, пентхаусы и резиденции у моря или бутик на одном из немногих оставшихся участков.'),
        ('Что усложняет стройку здесь?', 'Доступ и часы работ: работаем в окнах, согласованных с учётом туристического трафика и кондоминиума или оператора. Это плюс полная морская спецификация и двигает цену за номер.')],
 'de': [('Kann man in der Hotelzone noch ein neues Hotel bauen?', 'Kaum: Verfügbares Land ist knapp, teuer und in der Hand großer Betreiber. Realistisch sind heute Umnutzung und Komplettsanierung, Strand-Penthouses und -Residenzen oder ein Boutique auf einem der wenigen verbliebenen Grundstücke.'),
        ('Was macht eine Baustelle hier schwierig?', 'Zufahrt und Zeiten: Gearbeitet wird in Fenstern, die mit Blick auf Touristenverkehr und Eigentümergemeinschaft bzw. Betreiber abgestimmt sind. Das und die volle Meeresspezifikation treiben die Kosten pro Zimmer.')],
 'fr': [('Peut-on encore construire un hôtel neuf en Zone Hôtelière ?', 'À peine : le foncier disponible est rare, cher et détenu par de grands opérateurs. Ce qui est réaliste aujourd’hui, c’est la reconversion et la rénovation intégrale, les penthouses et résidences en front de mer, ou un boutique sur l’un des rares lots restants.'),
        ('Qu’est-ce qui complique un chantier ici ?', 'Les accès et les horaires : on travaille dans des fenêtres convenues selon le trafic touristique et la copropriété ou l’exploitant. Cela, avec la spécification marine complète, fait bouger le coût par clé.')],
 'zh': [('酒店区还能新建酒店吗？', '空间很小：可用地块稀少、价格高昂，且多由大型运营商持有。目前更现实的是功能改造与整体翻新、海滨顶层公寓与住宅，或在少数剩余地块上做精品项目。'),
        ('在这里施工难在哪里？', '难在进出与时段：必须在结合旅游车流、业主委员会或运营商协商确定的时间窗内作业。这一点加上完整的海洋环境做法，正是每间客房造价的主要变量。')]},
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


def _set_parent_urls(locs):
    P = {'es':'construccion-de-casas','en':'house-construction','ru':'stroitelstvo-domov','de':'hausbau','fr':'construction-de-maisons','zh':'zhuzhai-jianzao'}
    ml.OVR.setdefault('parent_url', {})
    for zk, d in locs.items():
        for l in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            ml.OVR['parent_url'].setdefault(zk, {})[l] = '/%s-%s/' % (P[l], d['parent'])


if __name__ == '__main__':
    _set_parent_urls(ZONES)
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
            print('%-56s %6d bytes' % (out + '/', len(html)))
