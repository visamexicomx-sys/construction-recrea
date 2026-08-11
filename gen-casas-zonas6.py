#!/usr/bin/env python3
"""Sixth zone batch (2026-08-11): Cancún's gated residential communities.

Everything covered for Cancún so far was tourist-facing (Puerto Cancún, Hotel Zone,
Playa Mujeres, Riviera Cancún). This batch covers where people actually live:
Residencial Cumbres and Aqua on Avenida Huayacán, Lagos del Sol, Villa Magna and
Palmaris — all in Benito Juárez, all inland, so no FONATUR and no ZOFEMAT; the real
gate is the estate's own design committee plus the municipal licence with a DRO.
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

ZONE6 = {
 'residencial-cumbres-cancun': dict(parent='cancun', f=1.15, perm='2–4'),
 'aqua-cancun':                dict(parent='cancun', f=1.32, perm='2–4'),
 'lagos-del-sol-cancun':       dict(parent='cancun', f=1.28, perm='2–4'),
 'villa-magna-cancun':         dict(parent='cancun', f=1.30, perm='2–4'),
 'palmaris-cancun':            dict(parent='cancun', f=1.20, perm='2–4'),
 'zona-hotelera-tulum':        dict(parent='tulum',  f=1.40, perm='3–5'),
 'isla-dorada-cancun':         dict(parent='cancun', f=1.35, perm='3–5'),
}

NAMES = {
 'residencial-cumbres-cancun': {'es': 'Residencial Cumbres, Cancún', 'en': 'Residencial Cumbres, Cancún',
   'ru': 'Резиденсиаль Кумбрес, Канкун', 'de': 'Residencial Cumbres, Cancún',
   'fr': 'Residencial Cumbres, Cancún', 'zh': '坎昆 Residencial Cumbres'},
 'aqua-cancun': {'es': 'Aqua, Cancún', 'en': 'Aqua, Cancún', 'ru': 'Аква, Канкун',
   'de': 'Aqua, Cancún', 'fr': 'Aqua, Cancún', 'zh': '坎昆 Aqua'},
 'lagos-del-sol-cancun': {'es': 'Lagos del Sol, Cancún', 'en': 'Lagos del Sol, Cancún',
   'ru': 'Лагос-дель-Соль, Канкун', 'de': 'Lagos del Sol, Cancún',
   'fr': 'Lagos del Sol, Cancún', 'zh': '坎昆 Lagos del Sol'},
 'villa-magna-cancun': {'es': 'Villa Magna, Cancún', 'en': 'Villa Magna, Cancún',
   'ru': 'Вилья-Магна, Канкун', 'de': 'Villa Magna, Cancún',
   'fr': 'Villa Magna, Cancún', 'zh': '坎昆 Villa Magna'},
 'palmaris-cancun': {'es': 'Palmaris, Cancún', 'en': 'Palmaris, Cancún', 'ru': 'Пальмарис, Канкун',
   'de': 'Palmaris, Cancún', 'fr': 'Palmaris, Cancún', 'zh': '坎昆 Palmaris'},
 'zona-hotelera-tulum': {'es': 'la Zona Hotelera de Tulum', 'en': 'the Tulum Hotel Zone', 'ru': 'Отельной зоне Тулума', 'de': 'der Hotelzone von Tulum', 'fr': 'la Zone Hôtelière de Tulum', 'zh': '图卢姆酒店区'},
 'isla-dorada-cancun': {'es': 'Isla Dorada, Cancún', 'en': 'Isla Dorada, Cancún', 'ru': 'Исла-Дорада, Канкун', 'de': 'Isla Dorada, Cancún', 'fr': 'Isla Dorada, Cancún', 'zh': '坎昆 Isla Dorada'},
}
AREAS = {
 'residencial-cumbres-cancun': {'es': 'Residencial Cumbres y el corredor de la avenida Huayacán',
   'en': 'Residencial Cumbres and the Avenida Huayacán corridor',
   'ru': 'Резиденсиаль Кумбрес и коридоре авеню Уаякан',
   'de': 'Residencial Cumbres und dem Korridor der Avenida Huayacán',
   'fr': 'Residencial Cumbres et le corridor de l’avenue Huayacán',
   'zh': 'Residencial Cumbres 及 Huayacán 大道沿线'},
 'aqua-cancun': {'es': 'Aqua y el corredor de la avenida Huayacán', 'en': 'Aqua and the Avenida Huayacán corridor',
   'ru': 'Акве и коридоре авеню Уаякан', 'de': 'Aqua und dem Korridor der Avenida Huayacán',
   'fr': 'Aqua et le corridor de l’avenue Huayacán', 'zh': 'Aqua 及 Huayacán 大道沿线'},
 'lagos-del-sol-cancun': {'es': 'Lagos del Sol y sus secciones alrededor de los lagos',
   'en': 'Lagos del Sol and its sections around the lakes',
   'ru': 'Лагос-дель-Соль и его секциях вокруг озёр',
   'de': 'Lagos del Sol und seinen Abschnitten rund um die Seen',
   'fr': 'Lagos del Sol et ses sections autour des lacs', 'zh': 'Lagos del Sol 及其环湖区段'},
 'villa-magna-cancun': {'es': 'Villa Magna y las zonas residenciales consolidadas de Cancún',
   'en': 'Villa Magna and Cancún’s consolidated residential areas',
   'ru': 'Вилья-Магне и сложившихся жилых районах Канкуна',
   'de': 'Villa Magna und den etablierten Wohngebieten von Cancún',
   'fr': 'Villa Magna et les quartiers résidentiels établis de Cancún',
   'zh': 'Villa Magna 及坎昆成熟住宅区'},
 'palmaris-cancun': {'es': 'Palmaris y el corredor de la avenida Huayacán',
   'en': 'Palmaris and the Avenida Huayacán corridor',
   'ru': 'Пальмарисе и коридоре авеню Уаякан',
   'de': 'Palmaris und dem Korridor der Avenida Huayacán',
   'fr': 'Palmaris et le corridor de l’avenue Huayacán',
   'zh': 'Palmaris 及 Huayacán 大道沿线'},
 'zona-hotelera-tulum': {'es': 'la carretera Tulum–Boca Paila y la franja costera', 'en': 'the Tulum–Boca Paila road and the coastal strip', 'ru': 'дороге Тулум–Бока-Паила и прибрежной полосе', 'de': 'der Straße Tulum–Boca Paila und dem Küstenstreifen', 'fr': 'la route Tulum–Boca Paila et la bande côtière', 'zh': '图卢姆–Boca Paila 公路与海岸带'},
 'isla-dorada-cancun': {'es': 'Isla Dorada y los canales de la Zona Hotelera', 'en': 'Isla Dorada and the Hotel Zone canals', 'ru': 'Исла-Дорада и каналах Отельной зоны', 'de': 'Isla Dorada und den Kanälen der Hotelzone', 'fr': 'Isla Dorada et les canaux de la Zone Hôtelière', 'zh': 'Isla Dorada 与酒店区水道一带'},
}

TEXT = {
'residencial-cumbres-cancun': {
 'es': 'Cumbres es el desarrollo privado más extenso del corredor de Huayacán: varias etapas, acabados de nivel alto y arquitectura moderna, con la entrada más accesible al segmento cerrado de Cancún. La contraparte es el reglamento: cada etapa tiene su comité y sus reglas de fachada, altura y horarios de obra, y la administración controla accesos y proveedores. Se construye rápido si el expediente entra bien armado; se atasca si se improvisa.',
 'en': 'Cumbres is the largest gated development on the Huayacán corridor: several phases, high-level finishes and modern architecture, with the most accessible entry into Cancún’s gated segment. The trade-off is the rulebook: each phase has its own committee and rules on façade, height and working hours, and the administration controls access and suppliers. It builds fast when the file goes in properly prepared, and stalls when it is improvised.',
 'ru': 'Кумбрес — самая крупная закрытая застройка коридора Уаякан: несколько очередей, отделка высокого уровня и современная архитектура, при самом доступном входе в закрытый сегмент Канкуна. Обратная сторона — регламент: у каждой очереди свой комитет и свои правила по фасаду, высоте и часам работ, а администрация контролирует доступ и поставщиков. Строится быстро, если пакет собран грамотно, и встаёт, если импровизировать.',
 'de': 'Cumbres ist die größte geschlossene Anlage am Huayacán-Korridor: mehrere Bauabschnitte, hochwertiger Ausbau und moderne Architektur, mit dem günstigsten Einstieg ins geschlossene Segment von Cancún. Die Kehrseite ist das Reglement: Jeder Abschnitt hat einen eigenen Beirat und Regeln zu Fassade, Höhe und Bauzeiten, die Verwaltung steuert Zufahrt und Lieferanten. Es baut sich schnell, wenn die Akte sauber ist — und stockt, wenn improvisiert wird.',
 'fr': 'Cumbres est la plus vaste résidence fermée du corridor de Huayacán : plusieurs tranches, finitions haut de gamme et architecture contemporaine, avec l’entrée la plus accessible au segment fermé de Cancún. La contrepartie, c’est le règlement : chaque tranche a son comité et ses règles de façade, hauteur et horaires de chantier, et l’administration contrôle accès et fournisseurs. Le chantier avance vite si le dossier est bien monté, et se bloque s’il est improvisé.',
 'zh': 'Cumbres 是 Huayacán 走廊上规模最大的封闭社区：分多期开发、装修标准较高、建筑风格现代，同时也是进入坎昆封闭社区市场门槛最低的选择。代价是规约：每一期都有自己的委员会，对立面、高度与施工时段各有规定，物业管理方还管控出入与供应商。材料齐备时推进很快，临场发挥则必然受阻。'},
'aqua-cancun': {
 'es': 'Aqua es de los residenciales con mayor prestigio y valor por m² de Cancún, sobre Huayacán y cerca del sistema lagunar. Esa cercanía manda en la obra: manto freático somero, impermeabilización reforzada y protección anticorrosiva del acero como estándar, no como extra. El comité de diseño es estricto con volumetría y materiales, así que el proyecto se dibuja conforme al reglamento desde el anteproyecto.',
 'en': 'Aqua is among Cancún’s highest-prestige residential estates by value per m², on Huayacán and close to the lagoon system. That proximity drives the build: a shallow water table, reinforced waterproofing and anti-corrosion protection of the rebar as standard, not as an extra. The design committee is strict on massing and materials, so the project is drawn to the rulebook from the concept stage.',
 'ru': 'Аква — один из самых престижных резиденсиалей Канкуна по цене за м², на Уаякане и рядом с лагунной системой. Эта близость и командует стройкой: высокий уровень грунтовых вод, усиленная гидроизоляция и антикоррозийная защита арматуры как стандарт, а не опция. Комитет по дизайну строг к объёму и материалам, поэтому проект рисуется под регламент уже на эскизе.',
 'de': 'Aqua gehört zu den prestigeträchtigsten Wohnanlagen Cancúns nach Wert pro m², an der Huayacán und nahe dem Lagunensystem. Diese Nähe bestimmt den Bau: hoher Grundwasserstand, verstärkte Abdichtung und Korrosionsschutz der Bewehrung als Standard, nicht als Extra. Der Gestaltungsbeirat ist streng bei Baukörper und Materialien — geplant wird ab dem Entwurf regelkonform.',
 'fr': 'Aqua figure parmi les résidences les plus prestigieuses de Cancún en valeur au m², sur Huayacán et près du système lagunaire. Cette proximité commande le chantier : nappe affleurante, étanchéité renforcée et protection anticorrosion des aciers en standard, pas en option. Le comité d’architecture est strict sur la volumétrie et les matériaux : le projet se dessine selon le règlement dès l’avant-projet.',
 'zh': 'Aqua 是坎昆每平方米价值最高、最具声望的住宅区之一，位于 Huayacán 大道、紧邻泻湖水系。这一区位直接决定施工做法：地下水位浅，加强防水与钢筋防腐属于标准配置而非额外选项。设计委员会对体量与材料要求严格，因此方案从概念阶段就按规约绘制。'},
'lagos-del-sol-cancun': {
 'es': 'Lagos del Sol es el residencial de mayor crecimiento y plusvalía de Cancún: lotes amplios alrededor de lagos, casas de dos y tres niveles con alberca y jardín, y un entorno pensado para vivir todo el año. En predios frente al agua la cota de desplante y el manejo de escurrimientos pesan tanto como la capacidad de carga, y el reglamento del desarrollo revisa alturas y fachadas antes del municipio.',
 'en': 'Lagos del Sol is Cancún’s fastest-growing and best-appreciating estate: generous lots around lakes, two- and three-storey houses with pool and garden, and an environment built for year-round living. On waterfront lots the finished floor level and runoff management matter as much as bearing capacity, and the development’s rules review heights and façades before the municipality does.',
 'ru': 'Лагос-дель-Соль — резиденсиаль с самым быстрым ростом и лучшей динамикой стоимости в Канкуне: просторные участки вокруг озёр, дома в два-три уровня с бассейном и садом, среда для круглогодичной жизни. На участках у воды отметка пола и управление стоком весят не меньше несущей способности, а регламент застройки проверяет высоты и фасады до муниципалитета.',
 'de': 'Lagos del Sol ist die am schnellsten wachsende und wertstärkste Anlage Cancúns: großzügige Grundstücke rund um Seen, zwei- und dreigeschossige Häuser mit Pool und Garten, ein Umfeld für ganzjähriges Wohnen. Bei Wassergrundstücken wiegen Höhenlage und Abflussmanagement so schwer wie die Tragfähigkeit, und die Anlagensatzung prüft Höhen und Fassaden vor der Gemeinde.',
 'fr': 'Lagos del Sol est la résidence à la plus forte croissance et à la meilleure plus-value de Cancún : grands terrains autour des lacs, maisons de deux et trois niveaux avec piscine et jardin, un cadre pensé pour vivre à l’année. Sur les lots au bord de l’eau, le niveau du plancher et la gestion des ruissellements comptent autant que la portance, et le règlement examine hauteurs et façades avant la mairie.',
 'zh': 'Lagos del Sol 是坎昆增长最快、增值表现最好的住宅区：环湖地块宽阔，多为带泳池与花园的二至三层住宅，整体环境适合全年居住。临水地块的首层标高与径流管理，其重要性不亚于地基承载力；社区规约会先于市政审核高度与立面。'},
'villa-magna-cancun': {
 'es': 'Villa Magna es de las zonas residenciales más exclusivas y consolidadas de Cancún: seguridad, tranquilidad y plusvalía sostenida. Consolidada significa también que quedan pocos lotes libres, así que aquí buena parte del trabajo es remodelación integral, ampliación o sustitución de casa existente, con la ventaja de servicios ya instalados y la restricción de convivir con vecinos durante la obra.',
 'en': 'Villa Magna is one of Cancún’s most exclusive and established residential areas: security, quiet and sustained appreciation. Established also means few free lots remain, so much of the work here is full renovation, extension or replacement of an existing house — with the advantage of services already in place and the constraint of building alongside neighbours.',
 'ru': 'Вилья-Магна — один из самых эксклюзивных и сложившихся жилых районов Канкуна: безопасность, тишина и устойчивый рост стоимости. «Сложившийся» означает и то, что свободных участков почти не осталось: значительная часть работы здесь — капитальная реконструкция, расширение или замена существующего дома, с плюсом готовых сетей и с ограничением работать рядом с соседями.',
 'de': 'Villa Magna gehört zu den exklusivsten und etabliertesten Wohngegenden Cancúns: Sicherheit, Ruhe und anhaltende Wertsteigerung. Etabliert heißt auch: kaum freie Grundstücke. Ein großer Teil der Arbeit ist hier Komplettsanierung, Anbau oder Ersatz eines Bestandshauses — mit dem Vorteil vorhandener Versorgung und der Einschränkung, neben Nachbarn zu bauen.',
 'fr': 'Villa Magna est l’un des quartiers résidentiels les plus exclusifs et les plus établis de Cancún : sécurité, tranquillité et plus-value durable. Établi signifie aussi qu’il reste peu de terrains libres : l’essentiel du travail y est la rénovation intégrale, l’extension ou le remplacement d’une maison existante — avec l’avantage des réseaux en place et la contrainte de bâtir au milieu des voisins.',
 'zh': 'Villa Magna 是坎昆最高端也最成熟的住宅区之一：安保完善、环境安静、增值稳定。成熟同时意味着空置地块所剩无几，因此这里的工作多为整体翻新、扩建或原房重建——优势是市政配套已就位，限制则是须在邻里之间施工。'},
'palmaris-cancun': {
 'es': 'Palmaris forma parte del corredor residencial más importante de Cancún, sobre Huayacán, con perfil familiar y precio más equilibrado que Aqua o Villa Magna. Es el punto razonable para casa propia con amenidades y seguridad sin pagar la prima de las zonas más exclusivas; el reglamento del residencial y la licencia municipal de Benito Juárez marcan el calendario, no la obra.',
 'en': 'Palmaris is part of Cancún’s most important residential corridor on Huayacán, family-oriented and more balanced in price than Aqua or Villa Magna. It is the sensible point for a home with amenities and security without paying the premium of the most exclusive estates; the community rules and the Benito Juárez municipal licence set the calendar, not the construction itself.',
 'ru': 'Пальмарис входит в главный жилой коридор Канкуна на Уаякане: семейный профиль и более сбалансированная цена, чем в Акве или Вилья-Магне. Разумная точка для собственного дома с инфраструктурой и охраной без премии самых эксклюзивных районов; календарь задают регламент посёлка и муниципальная лицензия Benito Juárez, а не сама стройка.',
 'de': 'Palmaris gehört zum wichtigsten Wohnkorridor Cancúns an der Huayacán: familiär geprägt und preislich ausgewogener als Aqua oder Villa Magna. Der vernünftige Punkt für ein eigenes Haus mit Ausstattung und Sicherheit, ohne den Aufschlag der exklusivsten Lagen; den Terminplan bestimmen Anlagensatzung und die kommunale Lizenz von Benito Juárez, nicht der Bau selbst.',
 'fr': 'Palmaris fait partie du principal corridor résidentiel de Cancún, sur Huayacán : profil familial et prix plus équilibré qu’Aqua ou Villa Magna. C’est le point raisonnable pour une maison avec équipements et sécurité sans payer la prime des quartiers les plus exclusifs ; ce sont le règlement de la résidence et le permis municipal de Benito Juárez qui fixent le calendrier, pas le chantier.',
 'zh': 'Palmaris 位于坎昆最重要的住宅走廊 Huayacán 大道沿线，定位偏家庭，价格较 Aqua 或 Villa Magna 更均衡。若想拥有配套与安保俱全的自住房，又不愿支付顶级片区的溢价，这里是务实之选；决定进度的是社区规约与 Benito Juárez 市政许可，而非施工本身。'},
 'zona-hotelera-tulum': {'es': 'La zona hotelera de Tulum es la franja entre la carretera Boca Paila y el mar: la dirección más cara del municipio y la más regulada. Aquí se cruzan tres cosas a la vez —zona federal marítimo terrestre, autorización ambiental de la SEMA y una infraestructura que históricamente no ha sido de red, con generación propia, pozo y tratamiento— y ninguna de las tres se resuelve sobre la marcha. El producto realista es pequeño, bien resuelto en autonomía y con el expediente ambiental impecable.', 'en': 'Tulum’s hotel zone is the strip between the Boca Paila road and the sea: the most expensive address in the municipality and the most regulated. Three things overlap here — the federal maritime-terrestrial zone, SEMA environmental authorisation and infrastructure that has historically not been grid-based, with own generation, well and treatment — and none of the three gets solved on the fly. The realistic product is small, properly self-sufficient and backed by a spotless environmental file.', 'ru': 'Отельная зона Тулума — полоса между дорогой Бока-Паила и морем: самый дорогой адрес муниципалитета и самый зарегулированный. Здесь сходятся сразу три вещи — федеральная морская зона, экологическое разрешение SEMA и инфраструктура, которой исторически не было в виде сетей: своя генерация, скважина и очистные. Ни одна из трёх не решается по ходу. Реалистичный продукт — небольшой, с продуманной автономностью и безупречным экологическим досье.', 'de': 'Tulums Hotelzone ist der Streifen zwischen der Straße Boca Paila und dem Meer: die teuerste Adresse der Gemeinde und die am stärksten regulierte. Drei Dinge überlagern sich hier — die föderale Meereszone, die SEMA-Umweltgenehmigung und eine Infrastruktur, die historisch nicht netzgebunden war, mit eigener Erzeugung, Brunnen und Aufbereitung — und keines davon lässt sich nebenbei lösen. Das realistische Produkt ist klein, sauber autark und mit tadelloser Umweltakte.', 'fr': 'La zone hôtelière de Tulum est la bande entre la route Boca Paila et la mer : l’adresse la plus chère de la commune et la plus réglementée. Trois choses s’y croisent — la zone fédérale maritime terrestre, l’autorisation environnementale de la SEMA et une infrastructure historiquement hors réseau, avec production propre, puits et traitement — et aucune ne se règle en cours de route. Le produit réaliste est petit, bien autonome et adossé à un dossier environnemental irréprochable.', 'zh': '图卢姆酒店区是 Boca Paila 公路与海之间的狭长地带：全市最贵的地址，也是监管最严的区域。这里同时叠加三件事——联邦海陆区、SEMA 环保许可，以及历史上并非市政管网供应的基础设施（自备发电、水井与污水处理），三者都无法边做边解决。现实可行的产品规模不大，自给系统完善，并配有无可挑剔的环保申报材料。'},
 'isla-dorada-cancun': {'es': 'Isla Dorada es la excepción residencial dentro de la Zona Hotelera de Cancún: lotes privados sobre canales, con acceso al agua y vecinos, no hoteles. Suelo FONATUR y licencia de Benito Juárez con DRO, más concesión ZOFEMAT si el predio da a la laguna o al canal. Manto freático alto y ambiente salino: la especificación marina y la impermeabilización reforzada no son opcionales, y los accesos de obra se acuerdan por el tráfico de la zona.', 'en': 'Isla Dorada is the residential exception inside Cancún’s Hotel Zone: private lots on the canals, with water access and neighbours rather than hotels. FONATUR land and the Benito Juárez licence with a DRO, plus a ZOFEMAT concession where the lot faces the lagoon or the canal. High water table and salt exposure: the marine spec and reinforced waterproofing are not optional, and site access is agreed around the zone’s traffic.', 'ru': 'Исла-Дорада — жилое исключение внутри Отельной зоны Канкуна: частные участки на каналах, с выходом к воде и соседями, а не отелями. Земля FONATUR и лицензия Benito Juárez с DRO, плюс концессия ZOFEMAT, если участок выходит на лагуну или канал. Высокий уровень грунтовых вод и солёная среда: морская спецификация и усиленная гидроизоляция не опция, а доступ на площадку согласуется с учётом трафика зоны.', 'de': 'Isla Dorada ist die Wohn-Ausnahme innerhalb der Hotelzone von Cancún: private Grundstücke an den Kanälen, mit Wasserzugang und Nachbarn statt Hotels. FONATUR-Land und die Lizenz von Benito Juárez mit DRO, dazu eine ZOFEMAT-Konzession, wenn das Grundstück an Lagune oder Kanal grenzt. Hoher Grundwasserstand und Salzbelastung: Meeresspezifikation und verstärkte Abdichtung sind nicht optional, und die Baustellenzufahrt wird wegen des Verkehrs abgestimmt.', 'fr': 'Isla Dorada est l’exception résidentielle au sein de la Zone Hôtelière de Cancún : des lots privés sur les canaux, avec accès à l’eau et des voisins plutôt que des hôtels. Terrain FONATUR et permis de Benito Juárez avec DRO, plus une concession ZOFEMAT si le lot donne sur la lagune ou le canal. Nappe haute et exposition saline : spécification marine et étanchéité renforcée ne sont pas optionnelles, et les accès de chantier se négocient selon le trafic de la zone.', 'zh': 'Isla Dorada 是坎昆酒店区内的住宅例外：临水道的私人地块，邻居是住户而非酒店。土地属 FONATUR，需办理带 DRO 的 Benito Juárez 许可；若地块面向泻湖或水道，还需 ZOFEMAT 特许。地下水位高、盐蚀明显：海洋环境标准与加强防水并非可选项，施工进出也需结合该区域交通状况协商确定。'},
}

FAQ = {
'residencial-cumbres-cancun': {
 'es': [('¿Qué exige el fraccionamiento para construir en Cumbres?', 'Aprobación del comité de la etapa correspondiente —fachada, altura, materiales— y después la licencia municipal de Benito Juárez con DRO. Además se coordinan accesos, horarios y proveedores con la administración.'),
        ('¿Cuánto cuesta construir en Cumbres?', 'De $13,200 a $27,600 MXN por m² según acabados. Es la entrada más accesible al segmento cerrado de Cancún sin renunciar a amenidades ni seguridad.')],
 'en': [('What does the estate require to build in Cumbres?', 'Approval from the relevant phase committee — façade, height, materials — and then the Benito Juárez municipal licence with a DRO. Access, working hours and suppliers are also coordinated with the administration.'),
        ('What does it cost to build in Cumbres?', 'From $13,200 to $27,600 MXN per m² depending on finishes. It is the most accessible entry into Cancún’s gated segment without giving up amenities or security.')],
 'ru': [('Что требует посёлок для стройки в Кумбресе?', 'Одобрение комитета соответствующей очереди — фасад, высота, материалы, — затем муниципальная лицензия Benito Juárez с DRO. Доступ, часы работ и поставщиков согласуем с администрацией.'),
        ('Сколько стоит стройка в Кумбресе?', 'От $13,200 до $27,600 MXN за м² в зависимости от отделки. Самый доступный вход в закрытый сегмент Канкуна без потери инфраструктуры и охраны.')],
 'de': [('Was verlangt die Anlage zum Bauen in Cumbres?', 'Freigabe des Beirats des jeweiligen Abschnitts — Fassade, Höhe, Materialien — und danach die kommunale Lizenz von Benito Juárez mit DRO. Zufahrt, Bauzeiten und Lieferanten werden mit der Verwaltung abgestimmt.'),
        ('Was kostet Bauen in Cumbres?', 'Von $13.200 bis $27.600 MXN pro m² je nach Ausbau. Der günstigste Einstieg ins geschlossene Segment von Cancún, ohne auf Ausstattung und Sicherheit zu verzichten.')],
 'fr': [('Qu’exige la résidence pour construire à Cumbres ?', 'L’accord du comité de la tranche concernée — façade, hauteur, matériaux — puis le permis municipal de Benito Juárez avec DRO. Accès, horaires et fournisseurs se coordonnent avec l’administration.'),
        ('Combien coûte la construction à Cumbres ?', 'De 13 200 à 27 600 MXN le m² selon les finitions. C’est l’entrée la plus accessible au segment fermé de Cancún, sans renoncer aux équipements ni à la sécurité.')],
 'zh': [('在 Cumbres 施工，社区有哪些要求？', '先取得相应分期委员会对立面、高度与材料的批准，再办理带 DRO 的 Benito Juárez 市政许可；出入、作业时段与供应商也需与物业协调。'),
        ('在 Cumbres 建房要多少钱？', '按装修标准，每平方米 13,200 至 27,600 比索。这是进入坎昆封闭社区市场门槛最低的选择，且不牺牲配套与安保。')]},
'aqua-cancun': {
 'es': [('¿Qué cuidados exige estar cerca del sistema lagunar?', 'Manto freático somero: la mecánica de suelos define cimentación y cota de desplante, y el proyecto lleva impermeabilización reforzada y protección anticorrosiva del acero desde el diseño.'),
        ('¿Es estricto el comité de diseño de Aqua?', 'Sí, en volumetría, materiales y fachada. Presentamos el proyecto al comité en paralelo al trámite municipal para no perder semanas en observaciones.')],
 'en': [('What does being near the lagoon system require?', 'A shallow water table: soil mechanics set the foundation and the finished floor level, and the design carries reinforced waterproofing and anti-corrosion protection of the rebar from the start.'),
        ('Is Aqua’s design committee strict?', 'Yes, on massing, materials and façade. We present the project to the committee in parallel with the municipal process so no weeks are lost to comments.')],
 'ru': [('Что требует близость лагунной системы?', 'Высокий уровень грунтовых вод: геология определяет фундамент и отметку пола, а проект изначально несёт усиленную гидроизоляцию и антикоррозийную защиту арматуры.'),
        ('Строг ли комитет по дизайну в Акве?', 'Да — по объёму, материалам и фасаду. Подаём проект в комитет параллельно с муниципальной процедурой, чтобы не терять недели на замечания.')],
 'de': [('Was verlangt die Nähe zum Lagunensystem?', 'Hoher Grundwasserstand: Die Bodenmechanik bestimmt Gründung und Höhenlage, und der Entwurf enthält von Anfang an verstärkte Abdichtung und Korrosionsschutz der Bewehrung.'),
        ('Ist der Gestaltungsbeirat von Aqua streng?', 'Ja — bei Baukörper, Materialien und Fassade. Wir legen das Projekt dem Beirat parallel zum kommunalen Verfahren vor, damit keine Wochen durch Auflagen verloren gehen.')],
 'fr': [('Qu’impose la proximité du système lagunaire ?', 'Une nappe affleurante : l’étude de sol fixe les fondations et le niveau du plancher, et le projet intègre dès la conception étanchéité renforcée et protection anticorrosion des aciers.'),
        ('Le comité d’architecture d’Aqua est-il strict ?', 'Oui, sur la volumétrie, les matériaux et la façade. Nous présentons le projet au comité en parallèle de la procédure municipale pour ne pas perdre de semaines en observations.')],
 'zh': [('紧邻泻湖水系需要注意什么？', '地下水位浅：土力学勘察决定基础与首层标高，方案自设计之初即包含加强防水与钢筋防腐处理。'),
        ('Aqua 的设计委员会严格吗？', '严格，尤其在体量、材料与立面方面。我们会在市政报批的同时向委员会报审，避免因补正意见而拖延数周。')]},
'lagos-del-sol-cancun': {
 'es': [('¿Qué cambia construir frente a un lago?', 'La cota de desplante y el manejo de escurrimientos se vuelven decisivos, junto con la impermeabilización. La mecánica de suelos define cimentación y nivel de piso terminado antes de dibujar la casa.'),
        ('¿Por qué Lagos del Sol tiene tanta plusvalía?', 'Lotes amplios, entorno de lagos y una comunidad orientada a vivir todo el año, no a la renta corta. Eso sostiene el valor y también el estándar de acabados que se espera aquí.')],
 'en': [('What changes when building by a lake?', 'The finished floor level and runoff management become decisive, alongside waterproofing. Soil mechanics set the foundation and the floor level before the house is drawn.'),
        ('Why does Lagos del Sol appreciate so strongly?', 'Generous lots, a lake setting and a community oriented to year-round living rather than short-term rental. That sustains value — and the finish standard expected here.')],
 'ru': [('Что меняет стройка у озера?', 'Решающими становятся отметка пола и управление стоком вместе с гидроизоляцией. Геология определяет фундамент и уровень чистого пола ещё до того, как дом нарисован.'),
        ('Почему в Лагос-дель-Соль такой рост стоимости?', 'Просторные участки, озёрная среда и сообщество, ориентированное на круглогодичную жизнь, а не на посуточную аренду. Это держит и стоимость, и ожидаемый здесь стандарт отделки.')],
 'de': [('Was ändert sich beim Bauen am See?', 'Höhenlage und Abflussmanagement werden entscheidend, zusammen mit der Abdichtung. Die Bodenmechanik legt Gründung und Fertigfußbodenhöhe fest, bevor das Haus gezeichnet wird.'),
        ('Warum steigt Lagos del Sol so stark im Wert?', 'Großzügige Grundstücke, Seenlage und eine Gemeinschaft, die auf ganzjähriges Wohnen statt Kurzzeitvermietung ausgerichtet ist. Das trägt den Wert — und den hier erwarteten Ausbaustandard.')],
 'fr': [('Qu’est-ce qui change en construisant au bord d’un lac ?', 'Le niveau du plancher et la gestion des ruissellements deviennent décisifs, avec l’étanchéité. L’étude de sol fixe fondations et niveau fini avant même de dessiner la maison.'),
        ('Pourquoi Lagos del Sol prend-il autant de valeur ?', 'De grands terrains, un cadre lacustre et une communauté tournée vers la résidence à l’année plutôt que la location courte. Cela soutient la valeur — et le standard de finition attendu.')],
 'zh': [('临湖建房有何不同？', '首层标高与径流管理成为关键，防水同样重要。土力学勘察会在绘制方案之前，先行确定基础形式与建筑完成面标高。'),
        ('Lagos del Sol 为何增值明显？', '地块宽阔、环湖环境，且社区面向全年居住而非短租。这既支撑了资产价值，也决定了此处的装修标准预期。')]},
'villa-magna-cancun': {
 'es': [('¿Quedan terrenos libres en Villa Magna?', 'Pocos. Por eso aquí buena parte del trabajo es remodelación integral, ampliación o sustitución de una casa existente, con servicios ya instalados y trámite municipal de Benito Juárez con DRO.'),
        ('¿Qué complica una obra en zona consolidada?', 'Los vecinos: accesos, ruido, horarios y limpieza se coordinan con la administración. Lo planeamos desde el inicio para que la obra no se convierta en un conflicto de convivencia.')],
 'en': [('Are there free lots left in Villa Magna?', 'Few. That is why much of the work here is full renovation, extension or replacement of an existing house, with services already in place and the Benito Juárez municipal process with a DRO.'),
        ('What makes a site difficult in an established area?', 'The neighbours: access, noise, hours and cleanliness are coordinated with the administration. We plan for it from day one so the build does not turn into a dispute.')],
 'ru': [('Остались ли свободные участки в Вилья-Магне?', 'Мало. Поэтому значительная часть работы здесь — капитальная реконструкция, расширение или замена существующего дома, при готовых сетях и муниципальной процедуре Benito Juárez с DRO.'),
        ('Что усложняет стройку в сложившемся районе?', 'Соседи: доступ, шум, часы работ и уборка согласуются с администрацией. Планируем это с первого дня, чтобы стройка не превратилась в конфликт.')],
 'de': [('Gibt es in Villa Magna noch freie Grundstücke?', 'Wenige. Deshalb ist hier ein großer Teil der Arbeit Komplettsanierung, Anbau oder Ersatz eines Bestandshauses — bei vorhandener Versorgung und kommunalem Verfahren in Benito Juárez mit DRO.'),
        ('Was erschwert eine Baustelle im etablierten Viertel?', 'Die Nachbarn: Zufahrt, Lärm, Zeiten und Sauberkeit werden mit der Verwaltung abgestimmt. Wir planen das ab dem ersten Tag, damit der Bau kein Konflikt wird.')],
 'fr': [('Reste-t-il des terrains libres à Villa Magna ?', 'Peu. C’est pourquoi l’essentiel du travail y est rénovation intégrale, extension ou remplacement d’une maison existante, avec réseaux en place et procédure municipale de Benito Juárez avec DRO.'),
        ('Qu’est-ce qui complique un chantier en quartier établi ?', 'Les voisins : accès, bruit, horaires et propreté se coordonnent avec l’administration. Nous l’anticipons dès le premier jour pour que le chantier ne devienne pas un conflit.')],
 'zh': [('Villa Magna 还有空地吗？', '很少。因此这里的工作多为整体翻新、扩建或原房重建，市政配套已就位，仍需办理带 DRO 的 Benito Juárez 市政手续。'),
        ('在成熟片区施工难在哪里？', '难在邻里关系：出入、噪音、作业时段与场地清洁都需与物业协调。我们从第一天就纳入计划，避免施工演变成纠纷。')]},
'palmaris-cancun': {
 'es': [('¿Por qué Palmaris y no Aqua o Villa Magna?', 'Por precio. Palmaris ofrece amenidades, seguridad y el mismo corredor de Huayacán con un costo por m² menor; se paga menos prima de exclusividad y se conserva la calidad de vida.'),
        ('¿Qué permisos aplican?', 'Reglamento del residencial primero y licencia municipal de Benito Juárez con proyecto firmado por DRO después. Los presentamos en paralelo y coordinamos accesos con la administración.')],
 'en': [('Why Palmaris rather than Aqua or Villa Magna?', 'Price. Palmaris offers amenities, security and the same Huayacán corridor at a lower cost per m²; you pay less of an exclusivity premium and keep the quality of life.'),
        ('Which permits apply?', 'The community rules first and then the Benito Juárez municipal licence with DRO-signed drawings. We file them in parallel and coordinate access with the administration.')],
 'ru': [('Почему Пальмарис, а не Аква или Вилья-Магна?', 'Из-за цены. Пальмарис даёт инфраструктуру, охрану и тот же коридор Уаякан при меньшей цене за м²: платите меньшую премию за эксклюзивность, сохраняя качество жизни.'),
        ('Какие разрешения нужны?', 'Сначала регламент посёлка, затем муниципальная лицензия Benito Juárez с проектом за подписью DRO. Подаём параллельно и согласуем доступ с администрацией.')],
 'de': [('Warum Palmaris statt Aqua oder Villa Magna?', 'Der Preis. Palmaris bietet Ausstattung, Sicherheit und denselben Huayacán-Korridor bei geringeren m²-Kosten; man zahlt weniger Exklusivitätsaufschlag und behält die Lebensqualität.'),
        ('Welche Genehmigungen gelten?', 'Zuerst die Anlagensatzung, danach die kommunale Lizenz von Benito Juárez mit DRO-unterzeichneten Plänen. Wir reichen parallel ein und stimmen die Zufahrt mit der Verwaltung ab.')],
 'fr': [('Pourquoi Palmaris plutôt qu’Aqua ou Villa Magna ?', 'Le prix. Palmaris offre équipements, sécurité et le même corridor de Huayacán à un coût au m² inférieur : on paie moins de prime d’exclusivité tout en conservant la qualité de vie.'),
        ('Quels permis s’appliquent ?', 'Le règlement de la résidence d’abord, puis le permis municipal de Benito Juárez avec plans signés par un DRO. Nous déposons en parallèle et coordonnons les accès avec l’administration.')],
 'zh': [('为什么选 Palmaris 而不是 Aqua 或 Villa Magna？', '因为价格。Palmaris 同样位于 Huayacán 走廊，配套与安保齐备，但每平方米造价更低：少付一份稀缺性溢价，生活品质不打折。'),
        ('需要哪些许可？', '先满足社区规约，再办理带 DRO 签署图纸的 Benito Juárez 市政许可。两者并行报审，出入事宜与物业协调。')]},
 'zona-hotelera-tulum': {'es': [('¿Qué permisos necesito en la zona hotelera de Tulum?', 'Licencia municipal de Tulum con DRO, autorización ambiental de la SEMA en prácticamente todos los predios y concesión ZOFEMAT en la franja federal frente al mar. El expediente ambiental define el calendario completo, no la obra.'), ('¿Hay servicios de red en la franja costera?', 'Históricamente no: se resuelve con generación propia o solar con respaldo, pozo y cisterna, y planta de tratamiento. Todo eso se dimensiona en el anteproyecto porque cambia el presupuesto y el tamaño viable del proyecto.')], 'en': [('What permits do I need in Tulum’s hotel zone?', 'The Tulum municipal licence with a DRO, SEMA environmental authorisation on practically every lot and a ZOFEMAT concession on the federal strip facing the sea. The environmental file sets the whole calendar, not the construction.'), ('Is there grid service on the coastal strip?', 'Historically not: it is solved with own generation or solar plus backup, a well and cistern, and a treatment plant. All of it is sized at concept stage because it changes the budget and the viable size of the project.')], 'ru': [('Какие разрешения нужны в отельной зоне Тулума?', 'Муниципальная лицензия Тулума с DRO, экологическое разрешение SEMA практически на всех участках и концессия ZOFEMAT в федеральной полосе у моря. Календарь задаёт экологическое досье, а не стройка.'), ('Есть ли сети на прибрежной полосе?', 'Исторически нет: решается своей генерацией или солнечной станцией с резервом, скважиной с цистерной и очистными. Всё это считается на стадии эскиза, потому что меняет и бюджет, и посильный размер проекта.')], 'de': [('Welche Genehmigungen brauche ich in Tulums Hotelzone?', 'Kommunale Lizenz von Tulum mit DRO, SEMA-Umweltgenehmigung auf praktisch jedem Grundstück und eine ZOFEMAT-Konzession im föderalen Streifen am Meer. Den gesamten Zeitplan bestimmt die Umweltakte, nicht der Bau.'), ('Gibt es Netzversorgung am Küstenstreifen?', 'Historisch nicht: gelöst wird das mit eigener Erzeugung oder Solar plus Backup, Brunnen und Zisterne sowie Kläranlage. Alles wird im Entwurf dimensioniert, denn es verändert Budget und machbare Projektgröße.')], 'fr': [('Quels permis faut-il en zone hôtelière de Tulum ?', 'Le permis municipal de Tulum avec DRO, l’autorisation environnementale de la SEMA sur pratiquement tous les lots et une concession ZOFEMAT sur la bande fédérale face à la mer. C’est le dossier environnemental qui fixe tout le calendrier, pas le chantier.'), ('Y a-t-il des réseaux sur la bande côtière ?', 'Historiquement non : on règle cela par production propre ou solaire avec secours, puits et citerne, et station de traitement. Tout se dimensionne dès l’avant-projet car cela change le budget et la taille viable du projet.')], 'zh': [('在图卢姆酒店区需要哪些许可？', '带 DRO 的图卢姆市政许可、几乎所有地块都需的 SEMA 环保许可，以及临海联邦地带的 ZOFEMAT 特许。决定整体进度的是环保申报，而非施工本身。'), ('海岸带有市政管网吗？', '历史上没有：需通过自备发电或太阳能加备用电源、水井与蓄水池，以及污水处理设备来解决。这些都在方案阶段完成选型，因为会同时改变预算与项目的可行规模。')]},
 'isla-dorada-cancun': {'es': [('¿Se puede construir casa en Isla Dorada?', 'Sí: es zona residencial dentro de la Zona Hotelera. Suelo FONATUR con licencia de Benito Juárez y DRO, más concesión ZOFEMAT si el predio da a laguna o canal.'), ('¿Qué exige estar sobre canal?', 'Manto freático alto y ambiente salino: mecánica de suelos para definir cimentación y cota de desplante, impermeabilización reforzada, acero protegido y cancelería anodizada.')], 'en': [('Can you build a house on Isla Dorada?', 'Yes: it is a residential area inside the Hotel Zone. FONATUR land with the Benito Juárez licence and a DRO, plus a ZOFEMAT concession where the lot faces the lagoon or a canal.'), ('What does a canal-front lot require?', 'High water table and salt exposure: soil mechanics to set the foundation and finished floor level, reinforced waterproofing, protected rebar and anodised joinery.')], 'ru': [('Можно ли построить дом на Исла-Дорада?', 'Да: это жилая зона внутри Отельной зоны. Земля FONATUR, лицензия Benito Juárez и DRO, плюс концессия ZOFEMAT, если участок выходит на лагуну или канал.'), ('Что требует участок на канале?', 'Высокий уровень грунтовых вод и солёная среда: геология для фундамента и отметки пола, усиленная гидроизоляция, защищённая арматура и анодированный алюминий.')], 'de': [('Kann man auf Isla Dorada ein Haus bauen?', 'Ja: Es ist Wohngebiet innerhalb der Hotelzone. FONATUR-Land mit Lizenz von Benito Juárez und DRO, dazu ZOFEMAT-Konzession bei Lage an Lagune oder Kanal.'), ('Was verlangt ein Grundstück am Kanal?', 'Hoher Grundwasserstand und Salzbelastung: Bodenmechanik für Gründung und Höhenlage, verstärkte Abdichtung, geschützte Bewehrung und eloxierte Fenster.')], 'fr': [('Peut-on construire une maison à Isla Dorada ?', 'Oui : c’est une zone résidentielle au sein de la Zone Hôtelière. Terrain FONATUR avec permis de Benito Juárez et DRO, plus concession ZOFEMAT si le lot donne sur la lagune ou un canal.'), ('Qu’exige un lot sur canal ?', 'Nappe haute et exposition saline : étude de sol pour les fondations et le niveau du plancher, étanchéité renforcée, aciers protégés et menuiseries anodisées.')], 'zh': [('在 Isla Dorada 可以建独栋住宅吗？', '可以：它是酒店区内的住宅片区。土地属 FONATUR，需带 DRO 的 Benito Juárez 许可；若面向泻湖或水道，另需 ZOFEMAT 特许。'), ('临水道地块有哪些要求？', '地下水位高、盐蚀强：需土力学勘察确定基础与首层标高，并采用加强防水、钢筋防护与阳极氧化门窗。')]},
}

LINKS = {}
_HUB = {'es': ('construccion-de-casas', 'Construcción de casas', '/calculadora/', 'Calculadora de costos', '/blog-es/', 'Guías de construcción'),
        'en': ('house-construction', 'House construction', '/calculator/', 'Cost calculator', '/blog/', 'Construction guides'),
        'ru': ('stroitelstvo-domov', 'Строительство домов', '/kalkulyator/', 'Калькулятор стоимости', '/blog-ru/', 'Гиды по строительству'),
        'de': ('hausbau', 'Hausbau', '/kostenrechner/', 'Kostenrechner', '/blog-de/', 'Bau-Leitfäden'),
        'fr': ('construction-de-maisons', 'Construction de maisons', '/calculateur/', 'Calculateur de coûts', '/blog-fr/', 'Guides de construction'),
        'zh': ('zhuzhai-jianzao', '住宅建造', '/jisuanqi/', '造价计算器', '/blog-zh/', '建筑指南')}
_PERM = {'es': ('/permisos-de-construccion-cancun/', 'Permisos de construcción en Cancún'),
         'en': ('/construction-permits-cancun/', 'Construction permits in Cancún'),
         'ru': ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'),
         'de': ('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen, Lizenzen und DRO'),
         'fr': ('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'),
         'zh': ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO')}
for _l, (_p, _hub, _c, _cn, _b, _bn) in _HUB.items():
    LINKS[_l] = {}
    for _z, _d in ZONE6.items():
        _town = _d['parent']
        _sib = 'zona-hotelera-cancun' if _town == 'cancun' else 'aldea-zama'
        LINKS[_l][_z] = [('/%s-%s/' % (_p, _town), '%s — %s' % (_hub, _town.replace('-', ' ').title())),
                         _PERM[_l], ('/%s-%s/' % (_p, _sib), _hub),
                         (_c, _cn), (_b, _bn)]


def _set_parent_urls(locs):
    P = {'es': 'construccion-de-casas', 'en': 'house-construction', 'ru': 'stroitelstvo-domov',
         'de': 'hausbau', 'fr': 'construction-de-maisons', 'zh': 'zhuzhai-jianzao'}
    ml.OVR.setdefault('parent_url', {})
    for zk, d in locs.items():
        for l in LANGS:
            ml.OVR['parent_url'].setdefault(zk, {})[l] = '/%s-%s/' % (P[l], d['parent'])


if __name__ == '__main__':
    _set_parent_urls(ZONE6)
    for z in ZONE6:
        z1.ZAREA[z] = AREAS[z]; z1.ZTEXT[z] = TEXT[z]; z1.ZFAQ[z] = FAQ[z]
    for lang in LINKS:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS[lang])
    for z, d in ZONE6.items():
        for lang in LANGS:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
    ml.LOCS.extend(ZONE6)
    for lang in LANGS:
        ch = ml.chrome(lang)
        for z in ZONE6:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-50s %6d bytes' % (out + '/', len(html)))
