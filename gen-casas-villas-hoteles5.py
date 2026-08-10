#!/usr/bin/env python3
"""Villa + hospitality pages for the remaining 12 zones (2026-08-09), 6 languages.

Design decision that keeps this batch honest instead of padded: the municipal rules
for each zone are ALREADY written per language on its house-construction page, so
this generator reuses that text verbatim and appends the hotel layer — which really
is the same municipal checklist everywhere (hotel land use, operating licence, Civil
Protection, CFE capacity by occupancy, tourism registration). What is written fresh
per zone is the part that actually differs: whether hospitality is viable there at
all, in what format, and the per-key band.
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
vh4 = load('gen-casas-villas-hoteles4.py', 'vh4')
vh3 = vh4.vh3; il = vh4.il; z1 = vh4.z1; ml = vh4.ml
SLUG_PREFIX = vh4.SLUG_PREFIX
ROWS = vh4.ROWS
LANGS = ['es', 'en', 'ru', 'de', 'fr', 'zh']

# zone key -> price parent + factor (identical to the zone's house page) + per-key band
Z = {
 'ciudad-mayakoba':         ('playa-del-carmen', 1.30, '2–4', ('$140,000 – $230,000', '$110,000 – $175,000', '$88,000 – $135,000')),
 'el-cielo-playa-del-carmen': ('playa-del-carmen', 1.15, '2–4', ('$110,000 – $185,000', '$88,000 – $140,000', '$68,000 – $108,000')),
 'selvamar-playa-del-carmen': ('playa-del-carmen', 1.18, '2–4', ('$115,000 – $190,000', '$90,000 – $145,000', '$70,000 – $112,000')),
 'punta-maroma':            ('playa-del-carmen', 1.45, '3–5', ('$200,000 – $330,000', '$155,000 – $240,000', '$120,000 – $180,000')),
 'xpu-ha':                  ('playa-del-carmen', 1.22, '2–4', ('$120,000 – $200,000', '$95,000 – $155,000', '$74,000 – $118,000')),
 'bahia-soliman':           ('tulum',            1.25, '3–5', ('$130,000 – $215,000', '$105,000 – $165,000', '$80,000 – $125,000')),
 'tankah':                  ('tulum',            1.22, '3–5', ('$128,000 – $210,000', '$102,000 – $160,000', '$78,000 – $122,000')),
 'selvazama':               ('tulum',            1.20, '3–5', ('$125,000 – $205,000', '$100,000 – $158,000', '$76,000 – $120,000')),
 'punta-brava':             ('cancun',           1.32, '3–5', ('$140,000 – $235,000', '$110,000 – $175,000', '$85,000 – $135,000')),
 'riviera-cancun':          ('cancun',           1.28, '3–5', ('$135,000 – $225,000', '$105,000 – $170,000', '$82,000 – $130,000')),
 'bahia-petempich':         ('cancun',           1.35, '3–5', ('$145,000 – $240,000', '$112,000 – $180,000', '$88,000 – $138,000')),
 'playa-mujeres':           ('cancun',           1.35, '3–5', ('$160,000 – $270,000', '$125,000 – $195,000', '$95,000 – $150,000')),
}
ZONES = {'vh-' + k: dict(parent=v[0], f=v[1], perm=v[2], zone=k) for k, v in Z.items()}
KEYS = {'vh-' + k: v[3] for k, v in Z.items()}
BASE_SLUG = {'vh-' + k: k for k in Z}

# names and sub-areas come from the batches that already built these zones
SRC = [load('gen-casas-zonas.py', 'zz1'), load('gen-casas-zonas2.py', 'zz2'),
       load('gen-casas-zonas3.py', 'zz3'), load('gen-casas-zonas4.py', 'zz4')]
NAMES, AREAS = {}, {}
for k in Z:
    for m in SRC:
        if hasattr(m, 'NAMES') and k in getattr(m, 'NAMES'):
            NAMES['vh-' + k] = m.NAMES[k]; AREAS['vh-' + k] = m.AREAS[k]; break
        if hasattr(m, 'ZNAME') and k in getattr(m, 'ZONE', {}):
            NAMES['vh-' + k] = {l: m.ZNAME[l][k] for l in LANGS}
            AREAS['vh-' + k] = {l: m.ZAREA[k][l] for l in LANGS}; break

# the hotel layer is the same municipal checklist everywhere; the municipality-specific
# rules are inherited from the zone's own page and this is appended to them
HOTEL_LAYER = {
 'es': ' <strong>Para hospedaje se suma otra capa:</strong> constancia de uso de suelo con giro hotelero —no todos los predios lo admiten y es lo primero que verificamos—, licencia de funcionamiento, visto bueno de Protección Civil, proyecto eléctrico ante CFE acorde al aforo y registro turístico. Si hay restaurante abierto al público, se añaden requisitos sanitarios y de aforo.',
 'en': ' <strong>Lodging adds another layer:</strong> a land-use certificate with hotel designation — not every lot allows it, and it is the first thing we verify — the operating licence, Civil Protection sign-off, a CFE electrical project sized to occupancy and tourism registration. A restaurant open to the public adds health and capacity requirements.',
 'ru': ' <strong>Для размещения добавляется ещё слой:</strong> справка о назначении земли с гостиничным профилем — его допускают не все участки, и это первое, что мы проверяем, — лицензия на деятельность, заключение Гражданской защиты, электропроект в CFE под вместимость и туристическая регистрация. Если есть ресторан для публики, добавляются санитарные требования и нормы вместимости.',
 'de': ' <strong>Für Beherbergung kommt eine weitere Ebene hinzu:</strong> Nutzungsbescheinigung mit Hotelwidmung — nicht jedes Grundstück lässt sie zu, und sie wird als Erstes geprüft —, Betriebslizenz, Freigabe des Zivilschutzes, ein auf die Belegung ausgelegtes CFE-Elektroprojekt und Tourismusregistrierung. Ein öffentlich zugängliches Restaurant ergänzt Hygiene- und Kapazitätsauflagen.',
 'fr': ' <strong>L’hébergement ajoute une couche :</strong> certificat d’usage du sol à vocation hôtelière — tous les lots ne l’admettent pas, et c’est la première chose que nous vérifions —, licence d’exploitation, avis de la Protection Civile, projet électrique CFE dimensionné à la capacité et enregistrement touristique. Un restaurant ouvert au public ajoute des exigences sanitaires et de capacité.',
 'zh': ' <strong>做住宿业态还需多一层手续：</strong>载明酒店用途的土地用途证明——并非所有地块都允许，这也是我们首先核实的事项——以及经营许可、民防意见、按接待容量向 CFE 报批的电气方案与旅游登记。若设有对外营业的餐厅，还需满足卫生与容纳人数要求。',
}
# one generic hospitality FAQ per language, plus one zone-specific FAQ written below
GENERIC_FAQ = {
 'es': ('¿Qué se necesita para operar hospedaje aquí?', 'Lo primero es que el uso de suelo del predio admita giro hotelero: sin eso no hay proyecto, y por eso lo verificamos antes de que usted compre. Después vienen licencia de funcionamiento, Protección Civil, capacidad eléctrica ante CFE por aforo, tratamiento de aguas dimensionado y registro turístico. Los gestionamos junto con la obra.'),
 'en': ('What does it take to operate lodging here?', 'First, the lot’s land use has to allow hotel operation: without it there is no project, which is why we verify it before you buy. Then come the operating licence, Civil Protection, CFE capacity by occupancy, properly sized wastewater treatment and tourism registration. We handle them alongside the build.'),
 'ru': ('Что нужно, чтобы вести здесь размещение?', 'Прежде всего назначение земли участка должно допускать гостиничный профиль: без этого проекта нет, поэтому проверяем до покупки. Дальше — лицензия на деятельность, Гражданская защита, мощность в CFE под вместимость, очистные нужного размера и туристическая регистрация. Ведём их параллельно со стройкой.'),
 'de': ('Was braucht man, um hier Beherbergung zu betreiben?', 'Zuerst muss die Nutzungsart des Grundstücks Hotelbetrieb zulassen: Ohne sie gibt es kein Projekt, deshalb prüfen wir sie vor dem Kauf. Danach folgen Betriebslizenz, Zivilschutz, CFE-Leistung nach Belegung, richtig dimensionierte Abwasserbehandlung und Tourismusregistrierung. Wir erledigen das parallel zum Bau.'),
 'fr': ('Que faut-il pour exploiter de l’hébergement ici ?', 'D’abord, l’usage du sol du terrain doit autoriser l’exploitation hôtelière : sans cela, il n’y a pas de projet, d’où notre vérification avant l’achat. Viennent ensuite la licence d’exploitation, la Protection Civile, la puissance CFE selon capacité, un assainissement correctement dimensionné et l’enregistrement touristique. Nous les menons avec le chantier.'),
 'zh': ('在这里做住宿经营需要什么？', '首先，地块的土地用途必须允许酒店经营：没有它就没有项目，因此我们会在您购地前核实。随后是经营许可、民防意见、按容量核定的 CFE 用电容量、按规模配置的污水处理设备与旅游登记。这些我们与施工同步办理。'),
}

# per zone: villa/hotel positioning + whether hospitality is viable and in what format
TEXT = {
'ciudad-mayakoba': {
 'es': 'Ciudad Mayakoba ofrece lotes residenciales y country club dentro de un plan maestro que fija estándar de diseño y áreas verdes. La villa es el producto natural; para hospedaje, el formato viable es residencias con servicio o boutique pequeño en los predios donde el máster plan y el uso de suelo lo permiten.',
 'en': 'Ciudad Mayakoba offers residential lots and a country club inside a master plan that sets the design standard and green areas. The villa is the natural product; for lodging, the viable format is serviced residences or a small boutique on the lots where the master plan and land use allow it.',
 'ru': 'Сьюдад-Майякоба предлагает жилые участки и кантри-клуб внутри мастер-плана, который задаёт стандарт дизайна и зелёные зоны. Вилла — естественный продукт; для размещения рабочий формат — резиденции с сервисом или небольшой бутик на участках, где это допускают мастер-план и назначение земли.',
 'de': 'Ciudad Mayakoba bietet Wohngrundstücke und einen Country Club innerhalb eines Masterplans, der Gestaltungsstandard und Grünflächen vorgibt. Die Villa ist das natürliche Produkt; für Beherbergung sind Serviced Residences oder ein kleines Boutique auf Grundstücken machbar, wo Masterplan und Nutzungsart es zulassen.',
 'fr': 'Ciudad Mayakoba propose des lots résidentiels et un country club au sein d’un plan-masse qui fixe le standard architectural et les espaces verts. La villa est le produit naturel ; pour l’hébergement, le format viable est la résidence avec services ou un petit boutique sur les lots où le plan-masse et l’usage du sol l’autorisent.',
 'zh': 'Ciudad Mayakoba 在统一总体规划下提供住宅地块与乡村俱乐部，并规定了设计标准与绿地要求。别墅是天然的产品形态；就住宿业态而言，在总体规划与土地用途允许的地块上，可行形态是带服务的住宅或小型精品酒店。'},
'el-cielo-playa-del-carmen': {
 'es': 'El Cielo es la entrada más accesible al segmento cerrado de Playa del Carmen, con lotes para casa a la medida y ambiente familiar. Aquí la villa de renta larga funciona mejor que la rotación diaria, y el hospedaje solo es posible donde el uso de suelo lo admite: el reglamento del residencial está pensado para vivir, no para operar hotel.',
 'en': 'El Cielo is the most accessible entry into Playa del Carmen’s gated segment, with custom-home lots and a family atmosphere. Here a long-stay rental villa works better than daily turnover, and lodging is only possible where land use allows it: the community’s rules are written for living, not for running a hotel.',
 'ru': 'Эль-Сьело — самый доступный вход в закрытый сегмент Плая-дель-Кармен: участки под индивидуальный дом и семейная атмосфера. Здесь вилла под длительную аренду работает лучше ежедневной ротации, а размещение возможно только там, где допускает назначение земли: регламент посёлка написан под жизнь, а не под работу отеля.',
 'de': 'El Cielo ist der günstigste Einstieg ins geschlossene Segment von Playa del Carmen, mit Grundstücken für individuelle Häuser und familiärem Umfeld. Hier funktioniert die Langzeit-Mietvilla besser als täglicher Wechsel, und Beherbergung ist nur möglich, wo die Nutzungsart es zulässt: Die Satzung ist fürs Wohnen geschrieben, nicht für den Hotelbetrieb.',
 'fr': 'El Cielo est l’entrée la plus accessible au segment fermé de Playa del Carmen, avec des lots pour maisons sur mesure et une ambiance familiale. Ici, la villa en location longue fonctionne mieux que la rotation quotidienne, et l’hébergement n’est possible que là où l’usage du sol l’admet : le règlement de la résidence est écrit pour habiter, pas pour exploiter un hôtel.',
 'zh': 'El Cielo 是进入普拉亚德尔卡门封闭社区市场门槛最低的选择，提供可自建住宅的地块，氛围宜居适合家庭。这里长租别墅比按天周转更合适；住宿业态仅在土地用途允许之处可行：社区规约是为居住而设，并非为酒店运营。'},
'selvamar-playa-del-carmen': {
 'es': 'Selvamar es baja densidad y selva conservada a diez minutos del centro: el producto es la villa integrada al entorno, con estancias largas y clientes que buscan silencio. Para hospedaje, el formato compatible es muy pequeño y solo donde el uso de suelo lo permita; el porcentaje de vegetación conservada condiciona todo el programa.',
 'en': 'Selvamar is low density and preserved jungle ten minutes from downtown: the product is a villa integrated into its setting, for long stays and guests who want quiet. For lodging, the compatible format is very small and only where land use allows it; the preserved-vegetation ratio conditions the whole brief.',
 'ru': 'Сельвамар — низкая плотность и сохранённая сельва в десяти минутах от центра: продукт здесь — вилла, встроенная в среду, под длительные заезды и клиентов, ищущих тишину. Для размещения совместимый формат очень небольшой и только там, где допускает назначение земли; доля сохраняемой растительности задаёт всю программу.',
 'de': 'Selvamar ist geringe Dichte und erhaltener Dschungel zehn Minuten vom Zentrum: Das Produkt ist eine in die Umgebung integrierte Villa für Langzeitaufenthalte und Gäste, die Ruhe suchen. Für Beherbergung ist nur ein sehr kleines Format kompatibel und nur, wo die Nutzungsart es zulässt; der Anteil erhaltener Vegetation bestimmt das gesamte Programm.',
 'fr': 'Selvamar, c’est la faible densité et la jungle préservée à dix minutes du centre : le produit, c’est la villa intégrée à son cadre, pour des séjours longs et des clients en quête de calme. Pour l’hébergement, le format compatible est très petit et seulement là où l’usage du sol l’autorise ; le taux de végétation conservée conditionne tout le programme.',
 'zh': 'Selvamar 密度低、丛林保留完好，距市中心仅十分钟：其产品是融入环境的别墅，面向长住客与追求安静的客群。就住宿业态而言，可兼容的规模很小，且仅限土地用途允许之处；植被保留比例决定了整个设计任务书。'},
'punta-maroma': {
 'es': 'Punta Maroma es el frente de mar más exclusivo al norte de Playa del Carmen, con zonificación turístico-hotelera y límite de 3 niveles o 15 metros. Aquí el producto es una residencia excepcional o un proyecto boutique muy contenido: los permisos se otorgan de forma limitada y el proyecto se diseña para caber en la norma.',
 'en': 'Punta Maroma is the most exclusive beachfront north of Playa del Carmen, with hotel/tourism zoning and a 3-level or 15-metre cap. The product here is an exceptional residence or a very contained boutique project: permits are granted sparingly and the design is made to fit the rules.',
 'ru': 'Пунта-Марома — самая эксклюзивная первая линия к северу от Плая-дель-Кармен, с туристско-гостиничным зонированием и лимитом в 3 уровня или 15 метров. Продукт здесь — исключительная резиденция или очень сдержанный бутик-проект: разрешения выдаются ограниченно, и проект подгоняется под норму.',
 'de': 'Punta Maroma ist die exklusivste Strandlage nördlich von Playa del Carmen, mit Hotel-/Tourismuszonierung und einer Grenze von 3 Ebenen bzw. 15 Metern. Das Produkt ist hier eine außergewöhnliche Residenz oder ein sehr zurückhaltendes Boutiqueprojekt: Genehmigungen werden restriktiv erteilt, der Entwurf richtet sich nach der Norm.',
 'fr': 'Punta Maroma est le front de mer le plus exclusif au nord de Playa del Carmen, avec un zonage hôtelier-touristique et une limite de 3 niveaux ou 15 mètres. Le produit y est une résidence d’exception ou un projet boutique très contenu : les permis sont délivrés avec parcimonie et le projet se conçoit pour entrer dans la norme.',
 'zh': 'Punta Maroma 是普拉亚德尔卡门以北最稀缺的海滨地段，规划用途为旅游酒店类，限高3层或15米。此处的产品是一栋卓越住宅或规模极为克制的精品项目：许可发放从严，方案须迁就法规。'},
'xpu-ha': {
 'es': 'Xpu-Há tiene playa y fraccionamientos privados con servicios completos a veinte minutos de Playa del Carmen. Es de las pocas zonas donde una villa de renta o un boutique pequeño salen a costo razonable sin renunciar a infraestructura, siempre que el uso de suelo del lote admita el giro que usted quiere operar.',
 'en': 'Xpu-Há has beach and private communities with full services twenty minutes from Playa del Carmen. It is one of the few areas where a rental villa or a small boutique comes out at a reasonable cost without giving up infrastructure — provided the lot’s land use allows the operation you want to run.',
 'ru': 'В Шпу-Ха есть пляж и частные секторы с полными коммуникациями в двадцати минутах от Плая-дель-Кармен. Это одна из немногих зон, где вилла под аренду или небольшой бутик выходят по разумной цене без потери инфраструктуры — при условии, что назначение земли участка допускает нужный вам профиль.',
 'de': 'Xpu-Há hat Strand und private Wohnanlagen mit voller Erschließung, zwanzig Minuten von Playa del Carmen. Eine der wenigen Lagen, in denen eine Mietvilla oder ein kleines Boutique zu vernünftigen Kosten entsteht, ohne auf Infrastruktur zu verzichten — sofern die Nutzungsart des Grundstücks den gewünschten Betrieb zulässt.',
 'fr': 'Xpu-Há offre la plage et des résidences privées entièrement viabilisées à vingt minutes de Playa del Carmen. C’est l’un des rares secteurs où une villa locative ou un petit boutique revient à un coût raisonnable sans renoncer aux réseaux — à condition que l’usage du sol du lot autorise l’exploitation visée.',
 'zh': 'Xpu-Há 拥有海滩与配套齐全的私人社区，距普拉亚德尔卡门二十分钟车程。这是少数几个既能保有完整市政配套、又能以合理造价建成出租别墅或小型精品酒店的片区——前提是地块土地用途允许您计划的经营业态。'},
'bahia-soliman': {
 'es': 'Bahía Solimán es baja densidad frente al mar, con lotes grandes y casi nada de infraestructura pública. El producto natural es la villa de renta de alto ticket; para hospedaje, un formato muy pequeño y autónomo —pozo, cisterna, planta de tratamiento y solar— que se dimensiona desde el anteproyecto.',
 'en': 'Soliman Bay is low-density beachfront with large lots and almost no public infrastructure. The natural product is a high-ticket rental villa; for lodging, a very small self-sufficient format — well, cistern, treatment plant and solar — sized from the concept stage.',
 'ru': 'Баия-Солиман — низкая плотность на первой линии, крупные участки и почти полное отсутствие городских сетей. Естественный продукт — вилла под аренду с высоким чеком; для размещения — очень небольшой автономный формат: скважина, цистерна, очистные и солнечная станция, рассчитанные на стадии эскиза.',
 'de': 'Bahía Solimán ist Strandlage geringer Dichte mit großen Grundstücken und kaum öffentlicher Infrastruktur. Das natürliche Produkt ist eine hochpreisige Mietvilla; für Beherbergung ein sehr kleines, autarkes Format — Brunnen, Zisterne, Kläranlage und Solar — ab dem Entwurf dimensioniert.',
 'fr': 'Bahía Solimán, c’est du front de mer en faible densité, de grands terrains et quasi aucune infrastructure publique. Le produit naturel est la villa locative haut de gamme ; pour l’hébergement, un format très petit et autonome — puits, citerne, station de traitement et solaire — dimensionné dès l’avant-projet.',
 'zh': 'Bahía Solimán 是低密度的海滨地带，地块宽大，几乎没有市政基础设施。天然的产品形态是高客单价的出租别墅；若做住宿业态，则宜采用极小规模的自给方案——水井、蓄水池、污水处理设备与太阳能，并在方案阶段完成选型。'},
'tankah': {
 'es': 'Tankah es la bahía protegida por el arrecife entre Akumal y Tulum: villas frente al mar, densidad mínima y Casa Cenote a un paso. Para hospedaje funciona lo muy pequeño y bien resuelto en autonomía; la logística es más larga que en el centro de Tulum y eso se refleja en el costo por llave.',
 'en': 'Tankah is the reef-sheltered bay between Akumal and Tulum: beachfront villas, minimal density and Casa Cenote a step away. For lodging, what works is very small and properly self-sufficient; logistics run longer than in central Tulum and that shows in the cost per key.',
 'ru': 'Танках — защищённая рифом бухта между Акумалем и Тулумом: виллы у моря, минимальная плотность и Каса-Сеноте в двух шагах. Для размещения работает очень небольшой формат с хорошо решённой автономностью; логистика длиннее, чем в центре Тулума, и это видно в цене за номер.',
 'de': 'Tankah ist die riffgeschützte Bucht zwischen Akumal und Tulum: Strandvillen, minimale Dichte und Casa Cenote in Schrittweite. Für Beherbergung funktioniert nur sehr Kleines mit gut gelöster Autarkie; die Logistik dauert länger als im Zentrum von Tulum, was sich in den Kosten pro Zimmer zeigt.',
 'fr': 'Tankah, c’est la baie protégée par le récif entre Akumal et Tulum : villas en bord de mer, densité minimale et Casa Cenote à deux pas. Pour l’hébergement, ce qui marche est très petit et bien autonome ; la logistique est plus longue qu’au centre de Tulum, ce qui se voit sur le coût par clé.',
 'zh': 'Tankah 是 Akumal 与图卢姆之间受珊瑚礁庇护的海湾：海滨别墅、密度极低，Casa Cenote 近在咫尺。住宿业态适合极小规模且自给方案完善的项目；物流周期长于图卢姆市区，这一点会体现在每间客房造价上。'},
'selvazama': {
 'es': 'Selvazama es el plan maestro urbanizado de Tulum: agua, drenaje, electricidad y fibra ya construidos, con lotes unifamiliares, multifamiliares y de uso mixto. Es de los pocos puntos de Tulum donde un proyecto de hospedaje arranca sin riesgo de factibilidad de servicios; queda resolver el uso de suelo con giro y la ruta de SEMA.',
 'en': 'Selvazama is Tulum’s urbanised master plan: water, drainage, power and fibre already built, with single-family, multi-family and mixed-use lots. One of the few places in Tulum where a lodging project starts without utility feasibility risk; what remains is hotel land use and the SEMA route.',
 'ru': 'Сельвасама — урбанизированный мастер-план Тулума: вода, канализация, электричество и оптика уже построены, участки под индивидуальные дома, многоквартирные и смешанные проекты. Одна из немногих точек Тулума, где проект размещения стартует без риска по подключениям; остаётся решить назначение земли под профиль и маршрут SEMA.',
 'de': 'Selvazama ist der erschlossene Masterplan Tulums: Wasser, Kanalisation, Strom und Glasfaser bereits gebaut, mit Grundstücken für Einfamilien-, Mehrfamilien- und Mischnutzung. Einer der wenigen Orte in Tulum, an dem ein Beherbergungsprojekt ohne Erschließungsrisiko startet; zu klären bleiben Hotel-Nutzungsart und der SEMA-Weg.',
 'fr': 'Selvazama est le plan-masse viabilisé de Tulum : eau, assainissement, électricité et fibre déjà réalisés, avec des lots individuels, collectifs et mixtes. L’un des rares points de Tulum où un projet d’hébergement démarre sans risque de faisabilité des réseaux ; restent l’usage hôtelier et le parcours SEMA.',
 'zh': 'Selvazama 是图卢姆已完成市政配套的总体规划区：供水、排水、供电与光纤均已建成，并提供独栋、多户与混合用途地块。这是图卢姆少数可以在没有接入可行性风险的前提下启动住宿类项目的地方；剩下要解决的是酒店类土地用途与 SEMA 流程。'},
'punta-brava': {
 'es': 'Punta Brava tiene arrecife a pocos metros y humedales protegidos tierra adentro, al sur de Puerto Morelos. El producto es la villa frente al mar o un hospedaje pequeño con concepto de naturaleza; todo se diseña para no afectar el Parque Nacional Arrecife, con tratamiento de aguas y control de escurrimientos desde el primer plano.',
 'en': 'Punta Brava has the reef metres offshore and protected wetlands inland, south of Puerto Morelos. The product is a beachfront villa or small nature-led lodging; everything is designed not to affect the Reef National Park, with wastewater treatment and runoff control from the first drawing.',
 'ru': 'У Пунта-Брава риф в нескольких метрах от берега и охраняемые водно-болотные угодья вглубь материка, к югу от Пуэрто-Морелоса. Продукт — вилла на первой линии или небольшое размещение с природной концепцией; всё проектируется так, чтобы не затронуть Нацпарк «Риф», с очисткой стоков и контролем поверхностного стока с первого чертежа.',
 'de': 'Punta Brava hat das Riff wenige Meter vor der Küste und geschützte Feuchtgebiete im Hinterland, südlich von Puerto Morelos. Das Produkt ist eine Strandvilla oder eine kleine naturnahe Beherbergung; alles wird so geplant, dass der Riff-Nationalpark unberührt bleibt — mit Abwasserbehandlung und Abflusskontrolle ab der ersten Zeichnung.',
 'fr': 'Punta Brava a le récif à quelques mètres et des zones humides protégées à l’intérieur, au sud de Puerto Morelos. Le produit est une villa en front de mer ou un petit hébergement axé nature ; tout est conçu pour ne pas affecter le Parc National du Récif, avec traitement des eaux et contrôle des ruissellements dès le premier plan.',
 'zh': 'Punta Brava 位于 Puerto Morelos 以南，珊瑚礁距岸仅数米，内陆分布受保护湿地。产品形态是海滨别墅或以自然为主题的小型住宿；所有设计都以不影响珊瑚礁国家公园为前提，自第一版图纸起即纳入污水处理与径流控制。'},
'riviera-cancun': {
 'es': 'El corredor de Riviera Cancún tiene golf, resorts y residencias a minutos del aeropuerto, lo que lo vuelve cómodo para operar y para llegar. Antes de cualquier cosa hay que confirmar en qué municipio cae el predio —el corredor cruza el límite entre Benito Juárez y Puerto Morelos—, porque de eso depende toda la ruta de permisos, también la del hotel.',
 'en': 'The Riviera Cancún corridor has golf, resorts and residences minutes from the airport, which makes it convenient both to operate and to reach. Before anything else you have to confirm which municipality the lot falls in — the corridor crosses the Benito Juárez / Puerto Morelos boundary — because the whole permit route depends on it, the hotel one included.',
 'ru': 'Коридор Ривьера-Канкун — гольф, резорты и резиденции в минутах от аэропорта, что удобно и для управления, и для приезда. Прежде всего нужно подтвердить, в каком муниципалитете участок: коридор пересекает границу Benito Juárez и Пуэрто-Морелоса, а от этого зависит весь маршрут разрешений, в том числе гостиничных.',
 'de': 'Der Korridor Riviera Cancún bietet Golf, Resorts und Residenzen wenige Minuten vom Flughafen — bequem im Betrieb wie in der Anreise. Zuerst ist zu klären, in welcher Gemeinde das Grundstück liegt: Der Korridor überschreitet die Grenze zwischen Benito Juárez und Puerto Morelos, und davon hängt der gesamte Genehmigungsweg ab, auch der für das Hotel.',
 'fr': 'Le corridor de Riviera Cancún réunit golf, resorts et résidences à quelques minutes de l’aéroport, pratique à exploiter comme à rejoindre. Avant tout, il faut confirmer la commune dont relève le terrain — le corridor franchit la limite entre Benito Juárez et Puerto Morelos — car tout le parcours des permis en dépend, celui de l’hôtel compris.',
 'zh': 'Riviera Cancún 走廊拥有高尔夫、度假村与住宅，距机场仅数分钟，无论运营还是抵达都很便利。首要之事是确认地块归属哪个市——该走廊横跨 Benito Juárez 与 Puerto Morelos 的边界——因为整条许可路径（包括酒店许可）都取决于此。'},
'bahia-petempich': {
 'es': 'Bahía Petempich es frente de mar discreto y de pocos lotes dentro del área de influencia del Parque Nacional Arrecife. La villa de alto ticket es el producto claro; para hospedaje, formatos pequeños donde el uso de suelo lo admita, con tratamiento de aguas obligatorio y expediente ambiental cuidado desde el inicio.',
 'en': 'Petempich Bay is discreet beachfront with few lots, inside the influence area of the Reef National Park. A high-ticket villa is the clear product; for lodging, small formats where land use allows them, with mandatory wastewater treatment and a carefully handled environmental file from the start.',
 'ru': 'Баия-Петемпич — непубличная первая линия с небольшим числом лотов, в зоне влияния Нацпарка «Риф». Вилла с высоким чеком — очевидный продукт; для размещения — малые форматы там, где допускает назначение земли, с обязательной очисткой стоков и аккуратным экологическим досье с самого начала.',
 'de': 'Bahía Petempich ist diskrete Strandlage mit wenigen Grundstücken, im Einflussbereich des Riff-Nationalparks. Die hochpreisige Villa ist das klare Produkt; für Beherbergung kleine Formate, wo die Nutzungsart es zulässt — mit verpflichtender Abwasserbehandlung und von Beginn an sorgfältig geführter Umweltakte.',
 'fr': 'Bahía Petempich, c’est un front de mer discret avec peu de lots, dans la zone d’influence du Parc National du Récif. La villa haut de gamme est le produit évident ; pour l’hébergement, de petits formats là où l’usage du sol l’admet, avec traitement des eaux obligatoire et dossier environnemental soigné dès le départ.',
 'zh': 'Bahía Petempich 是地块稀少、氛围低调的海滨地带，位于珊瑚礁国家公园影响范围内。高客单价别墅是明确的产品方向；住宿业态则宜采用小规模形态，且仅限土地用途允许之处，并须强制配置污水处理、自始认真准备环保材料。'},
'playa-mujeres': {
 'es': 'Playa Mujeres reúne golf de firma, marina, playa virgen y residencias de marca al norte de Cancún, en el municipio de Isla Mujeres. Es el entorno donde el producto de marca —residencias con servicio, condo-hotel, boutique de alto nivel— tiene mercado real, siempre con el visto bueno de FONATUR y el comité de diseño del desarrollo.',
 'en': 'Playa Mujeres brings together a signature golf course, a marina, unspoilt beach and branded residences north of Cancún, in the municipality of Isla Mujeres. It is the setting where the branded product — serviced residences, condo-hotel, high-end boutique — has a real market, always with FONATUR sign-off and the development’s design committee.',
 'ru': 'Плая-Мухерес объединяет авторское поле для гольфа, марину, нетронутый пляж и брендовые резиденции к северу от Канкуна, в муниципалитете Isla Mujeres. Это среда, где брендовый продукт — резиденции с сервисом, кондо-отель, бутик высокого уровня — имеет реальный рынок, всегда с согласованием FONATUR и комитетом по дизайну застройки.',
 'de': 'Playa Mujeres vereint Signature-Golf, Marina, unverbauten Strand und Markenresidenzen nördlich von Cancún, in der Gemeinde Isla Mujeres. Hier hat das Markenprodukt — Serviced Residences, Condo-Hotel, High-End-Boutique — einen realen Markt, stets mit FONATUR-Freigabe und dem Gestaltungsbeirat der Anlage.',
 'fr': 'Playa Mujeres réunit golf signature, marina, plage préservée et résidences de marque au nord de Cancún, dans la commune d’Isla Mujeres. C’est le cadre où le produit de marque — résidences avec services, condo-hôtel, boutique haut de gamme — trouve un vrai marché, toujours avec l’accord FONATUR et le comité d’architecture du développement.',
 'zh': 'Playa Mujeres 位于坎昆以北、隶属 Isla Mujeres 市，汇聚名家高尔夫球场、码头、未开发海滩与品牌住宅。在这里，品牌化产品——带服务的住宅、产权式酒店、高端精品酒店——拥有真实市场，但始终需要 FONATUR 批准与开发区设计委员会审核。'},
}

# one zone-specific hospitality FAQ per zone (the second FAQ is the generic one above)
FAQ1 = {
'ciudad-mayakoba': {'es': ('¿Puedo operar hospedaje en Ciudad Mayakoba?', 'Solo donde el máster plan y el uso de suelo lo permitan; el formato viable es residencias con servicio o boutique pequeño. Lo confirmamos con la constancia de uso de suelo antes de diseñar.'),
 'en': ('Can I operate lodging in Ciudad Mayakoba?', 'Only where the master plan and land use allow it; the viable format is serviced residences or a small boutique. We confirm it with the land-use certificate before designing.'),
 'ru': ('Можно ли вести размещение в Сьюдад-Майякобе?', 'Только там, где допускают мастер-план и назначение земли; рабочий формат — резиденции с сервисом или небольшой бутик. Подтверждаем справкой о назначении земли до проектирования.'),
 'de': ('Kann ich in Ciudad Mayakoba Beherbergung betreiben?', 'Nur wo Masterplan und Nutzungsart es zulassen; machbar sind Serviced Residences oder ein kleines Boutique. Wir prüfen es vor dem Entwurf mit der Nutzungsbescheinigung.'),
 'fr': ('Puis-je exploiter de l’hébergement à Ciudad Mayakoba ?', 'Uniquement là où le plan-masse et l’usage du sol l’autorisent ; le format viable est la résidence avec services ou un petit boutique. Nous le confirmons via le certificat d’usage du sol avant de concevoir.'),
 'zh': ('我可以在 Ciudad Mayakoba 做住宿经营吗？', '仅限总体规划与土地用途允许之处；可行形态为带服务的住宅或小型精品酒店。我们会在设计前以土地用途证明予以确认。')},
'el-cielo-playa-del-carmen': {'es': ('¿Conviene El Cielo para renta?', 'Para estancia larga, sí: entorno familiar, amenidades y seguridad. Para rotación diaria hay que revisar antes el reglamento del residencial y el uso de suelo, porque la comunidad está pensada para vivir.'),
 'en': ('Is El Cielo good for rental?', 'For long stays, yes: family setting, amenities and security. For daily turnover you must first check the community rules and the land use, because the community is designed for living.'),
 'ru': ('Подходит ли Эль-Сьело под аренду?', 'Под длительные заезды — да: семейная среда, инфраструктура и охрана. Для ежедневной ротации сначала нужно проверить регламент посёлка и назначение земли, потому что община рассчитана на проживание.'),
 'de': ('Eignet sich El Cielo für Vermietung?', 'Für Langzeitaufenthalte ja: familiäres Umfeld, Ausstattung und Sicherheit. Für täglichen Wechsel müssen zuerst Anlagensatzung und Nutzungsart geprüft werden, denn die Anlage ist fürs Wohnen ausgelegt.'),
 'fr': ('El Cielo convient-il à la location ?', 'Pour les longs séjours, oui : cadre familial, équipements et sécurité. Pour la rotation quotidienne, il faut d’abord vérifier le règlement de la résidence et l’usage du sol, car la communauté est pensée pour habiter.'),
 'zh': ('El Cielo 适合做出租吗？', '长租适合：氛围宜居、配套完善、有安保。若要按天周转，需先核查社区规约与土地用途，因为该社区是按居住定位设计的。')},
'selvamar-playa-del-carmen': {'es': ('¿Se puede hacer hospedaje en Selvamar?', 'Solo formatos muy pequeños y donde el uso de suelo lo admita. El porcentaje de vegetación conservada y la baja densidad condicionan el programa desde el inicio.'),
 'en': ('Can you do lodging in Selvamar?', 'Only very small formats and where land use allows it. The preserved-vegetation ratio and the low density shape the brief from the start.'),
 'ru': ('Можно ли размещение в Сельвамаре?', 'Только очень небольшие форматы и там, где допускает назначение земли. Доля сохраняемой растительности и низкая плотность задают программу с самого начала.'),
 'de': ('Ist Beherbergung in Selvamar möglich?', 'Nur sehr kleine Formate und dort, wo die Nutzungsart es zulässt. Vegetationsanteil und geringe Dichte prägen das Programm von Anfang an.'),
 'fr': ('Peut-on faire de l’hébergement à Selvamar ?', 'Uniquement de très petits formats et là où l’usage du sol l’admet. Le taux de végétation conservée et la faible densité conditionnent le programme dès le départ.'),
 'zh': ('Selvamar 可以做住宿业态吗？', '仅限极小规模，且需土地用途允许。植被保留比例与低密度从一开始就限定了设计任务书。')},
'punta-maroma': {'es': ('¿Qué se puede construir en Punta Maroma?', 'Zonificación turístico-hotelera con límite de 3 niveles o 15 metros, y permisos otorgados de forma limitada. El uso de suelo se verifica lote por lote antes de comprar: no todos admiten el mismo programa.'),
 'en': ('What can be built at Punta Maroma?', 'Hotel/tourism zoning with a 3-level or 15-metre cap, and permits granted sparingly. Land use is checked lot by lot before buying: not all of them allow the same programme.'),
 'ru': ('Что можно построить в Пунта-Мароме?', 'Туристско-гостиничное зонирование с лимитом 3 уровня или 15 метров и ограниченная выдача разрешений. Назначение земли проверяется по каждому лоту до покупки: не все допускают одинаковую программу.'),
 'de': ('Was lässt sich in Punta Maroma bauen?', 'Hotel-/Tourismuszonierung mit 3 Ebenen bzw. 15 Metern Grenze und restriktiv erteilten Genehmigungen. Die Nutzungsart wird vor dem Kauf Grundstück für Grundstück geprüft — nicht alle lassen dasselbe Programm zu.'),
 'fr': ('Que peut-on construire à Punta Maroma ?', 'Zonage hôtelier-touristique avec une limite de 3 niveaux ou 15 mètres et des permis délivrés avec parcimonie. L’usage du sol se vérifie lot par lot avant l’achat : tous n’autorisent pas le même programme.'),
 'zh': ('在 Punta Maroma 能建什么？', '规划用途为旅游酒店类，限高3层或15米，且许可发放从严。购地前须逐地块核实土地用途：并非所有地块都允许相同的开发内容。')},
'xpu-ha': {'es': ('¿Xpu-Há sirve para un boutique pequeño?', 'Sí, donde el uso de suelo lo admita: hay servicios completos dentro de los fraccionamientos y el costo por llave es de los más razonables de la costa sur.'),
 'en': ('Does Xpu-Há work for a small boutique?', 'Yes, where land use allows it: the private communities have full services and the cost per key is among the most reasonable on the southern coast.'),
 'ru': ('Подходит ли Шпу-Ха под небольшой бутик?', 'Да, где допускает назначение земли: внутри секторов есть полные коммуникации, а цена за номер — одна из самых разумных на южном побережье.'),
 'de': ('Eignet sich Xpu-Há für ein kleines Boutique?', 'Ja, wo die Nutzungsart es zulässt: In den Anlagen liegt volle Erschließung vor, und die Kosten pro Zimmer gehören zu den vernünftigsten der Südküste.'),
 'fr': ('Xpu-Há convient-il à un petit boutique ?', 'Oui, là où l’usage du sol l’admet : les résidences privées sont entièrement viabilisées et le coût par clé est parmi les plus raisonnables de la côte sud.'),
 'zh': ('Xpu-Há 适合做小型精品酒店吗？', '在土地用途允许之处可行：私人社区内配套齐全，且每间客房造价在南部海岸属较为合理的水平。')},
'bahia-soliman': {'es': ('¿Qué formato de hospedaje aguanta Bahía Solimán?', 'Muy pequeño y autónomo. Sin red pública, cada llave suma pozo, cisterna, tratamiento y respaldo eléctrico: eso define el tamaño viable, no el gusto del inversionista.'),
 'en': ('What lodging format does Soliman Bay support?', 'Very small and self-sufficient. With no public network, every key adds well, cistern, treatment and power backup — that defines the viable size, not the investor’s preference.'),
 'ru': ('Какой формат размещения выдержит Баия-Солиман?', 'Очень небольшой и автономный. Без городских сетей каждый номер добавляет скважину, цистерну, очистные и резервное питание — именно это определяет посильный размер, а не желание инвестора.'),
 'de': ('Welches Beherbergungsformat trägt Bahía Solimán?', 'Sehr klein und autark. Ohne öffentliches Netz bringt jedes Zimmer Brunnen, Zisterne, Aufbereitung und Notstrom mit — das bestimmt die machbare Größe, nicht der Wunsch des Investors.'),
 'fr': ('Quel format d’hébergement Bahía Solimán supporte-t-il ?', 'Très petit et autonome. Sans réseau public, chaque clé ajoute puits, citerne, traitement et secours électrique : c’est cela qui définit la taille viable, pas la préférence de l’investisseur.'),
 'zh': ('Bahía Solimán 能承载什么规模的住宿项目？', '极小规模且自给自足。没有市政管网，每增加一间客房都意味着水井、蓄水池、处理设备与备用电源的追加——决定可行规模的是这些，而非投资人的偏好。')},
'tankah': {'es': ('¿Se puede operar hospedaje en Tankah?', 'En formatos muy pequeños y donde el uso de suelo lo permita, con SEMA resuelta y ZOFEMAT si el predio es de playa. La autonomía de servicios se dimensiona antes de definir el número de llaves.'),
 'en': ('Can you operate lodging in Tankah?', 'In very small formats and where land use allows it, with SEMA resolved and ZOFEMAT if the lot is on the beach. Utility autonomy is sized before the key count is set.'),
 'ru': ('Можно ли вести размещение в Танкахе?', 'В очень небольших форматах и там, где допускает назначение земли, с закрытой SEMA и ZOFEMAT, если участок пляжный. Автономность считается до того, как определяется число номеров.'),
 'de': ('Kann man in Tankah Beherbergung betreiben?', 'In sehr kleinen Formaten und dort, wo die Nutzungsart es zulässt, mit geklärter SEMA und ZOFEMAT bei Strandlage. Die Autarkie wird dimensioniert, bevor die Zimmerzahl feststeht.'),
 'fr': ('Peut-on exploiter de l’hébergement à Tankah ?', 'Dans de très petits formats et là où l’usage du sol l’autorise, avec la SEMA réglée et la ZOFEMAT si le terrain est en bord de plage. L’autonomie se dimensionne avant de fixer le nombre de clés.'),
 'zh': ('在 Tankah 可以做住宿经营吗？', '可在极小规模、且土地用途允许的前提下进行，需先完成 SEMA；若属海滩地块还需 ZOFEMAT。客房数量应在完成自给系统选型之后再确定。')},
'selvazama': {'es': ('¿Por qué Selvazama para un proyecto de hospedaje?', 'Porque la urbanización ya está: agua, drenaje, CFE y fibra construidas. Se elimina el riesgo de factibilidad que sí existe en zonas en desarrollo; queda el uso de suelo con giro y la ruta de SEMA.'),
 'en': ('Why Selvazama for a lodging project?', 'Because the urbanisation is already there: water, drainage, CFE and fibre built. It removes the feasibility risk that developing areas still carry; what remains is hotel land use and the SEMA route.'),
 'ru': ('Почему Сельвасама для проекта размещения?', 'Потому что урбанизация уже есть: вода, канализация, CFE и оптика построены. Снимается риск подключений, который остаётся в развивающихся районах; остаются назначение земли под профиль и маршрут SEMA.'),
 'de': ('Warum Selvazama für ein Beherbergungsprojekt?', 'Weil die Erschließung bereits steht: Wasser, Kanalisation, CFE und Glasfaser gebaut. Das nimmt das Erschließungsrisiko wachsender Viertel; es bleiben Hotel-Nutzungsart und SEMA-Weg.'),
 'fr': ('Pourquoi Selvazama pour un projet d’hébergement ?', 'Parce que la viabilisation est faite : eau, assainissement, CFE et fibre réalisés. Cela supprime le risque de faisabilité des secteurs en développement ; restent l’usage hôtelier et le parcours SEMA.'),
 'zh': ('为什么在 Selvazama 做住宿项目？', '因为市政配套已经到位：供水、排水、CFE 供电与光纤均已建成，可消除在建片区仍存在的接入风险；剩下的是酒店类土地用途与 SEMA 流程。')},
'punta-brava': {'es': ('¿Qué exige el arrecife a un proyecto de hospedaje aquí?', 'Planta de tratamiento o biodigestor dimensionado al aforo, control de escurrimientos durante la obra, manejo documentado de residuos y cuidado con la iluminación. Sin eso el expediente ambiental no avanza.'),
 'en': ('What does the reef require from a lodging project here?', 'A treatment plant or biodigester sized to occupancy, runoff control during construction, documented waste handling and care with lighting. Without that the environmental file does not move.'),
 'ru': ('Что риф требует от проекта размещения здесь?', 'Очистные или биодигестер под вместимость, контроль стока во время стройки, документированный вывоз отходов и аккуратность с освещением. Без этого экологическое досье не двигается.'),
 'de': ('Was verlangt das Riff hier von einem Beherbergungsprojekt?', 'Eine auf die Belegung ausgelegte Kläranlage oder einen Biodigester, Abflusskontrolle während des Baus, dokumentierte Abfallentsorgung und Sorgfalt bei der Beleuchtung. Ohne das bewegt sich die Umweltakte nicht.'),
 'fr': ('Qu’exige le récif d’un projet d’hébergement ici ?', 'Une station de traitement ou un biodigesteur dimensionné à la capacité, le contrôle des ruissellements pendant le chantier, une gestion documentée des déchets et de la prudence sur l’éclairage. Sans cela, le dossier environnemental n’avance pas.'),
 'zh': ('珊瑚礁对这里的住宿项目有哪些要求？', '按接待容量配置的污水处理设备或生物消化池、施工期径流控制、可追溯的废弃物处理，以及谨慎的照明设计。做不到这些，环保审批无法推进。')},
'riviera-cancun': {'es': ('¿Qué reviso primero para un hotel en Riviera Cancún?', 'El municipio: el corredor cruza el límite entre Benito Juárez y Puerto Morelos y cambia autoridad, tiempos y requisitos. Lo confirmamos con la constancia de uso de suelo antes de mover cualquier trámite.'),
 'en': ('What do I check first for a hotel in Riviera Cancún?', 'The municipality: the corridor crosses the Benito Juárez / Puerto Morelos boundary and that changes the authority, the timeline and the requirements. We confirm it with the land-use certificate before starting any process.'),
 'ru': ('Что проверить первым для отеля в Ривьера-Канкун?', 'Муниципалитет: коридор пересекает границу Benito Juárez и Пуэрто-Морелоса, а это меняет орган, сроки и требования. Подтверждаем справкой о назначении земли до начала любых процедур.'),
 'de': ('Was prüfe ich zuerst für ein Hotel in Riviera Cancún?', 'Die Gemeinde: Der Korridor überschreitet die Grenze zwischen Benito Juárez und Puerto Morelos, was Behörde, Fristen und Anforderungen ändert. Wir klären das über die Nutzungsbescheinigung, bevor ein Verfahren startet.'),
 'fr': ('Que vérifier en premier pour un hôtel à Riviera Cancún ?', 'La commune : le corridor franchit la limite entre Benito Juárez et Puerto Morelos, ce qui change l’autorité, les délais et les exigences. Nous le confirmons via le certificat d’usage du sol avant toute démarche.'),
 'zh': ('在 Riviera Cancún 做酒店，首先要核查什么？', '所属市政：该走廊横跨 Benito Juárez 与 Puerto Morelos 的边界，主管机关、周期与要求都会随之改变。我们会在启动任何报批前，通过土地用途证明予以确认。')},
'bahia-petempich': {'es': ('¿Es viable un hotel pequeño en Bahía Petempich?', 'Donde el uso de suelo lo admita, sí, en formato reducido. La zona tiene pocos lotes y el expediente ambiental por el Parque Nacional Arrecife marca el calendario completo.'),
 'en': ('Is a small hotel viable in Petempich Bay?', 'Where land use allows it, yes, in a reduced format. The area has few lots and the environmental file for the Reef National Park sets the whole calendar.'),
 'ru': ('Возможен ли небольшой отель в Баия-Петемпич?', 'Там, где допускает назначение земли, — да, в уменьшенном формате. Лотов мало, а экологическое досье из-за Нацпарка «Риф» задаёт весь календарь.'),
 'de': ('Ist ein kleines Hotel in Bahía Petempich machbar?', 'Wo die Nutzungsart es zulässt, ja — in reduziertem Format. Es gibt wenige Grundstücke, und die Umweltakte wegen des Riff-Nationalparks bestimmt den gesamten Zeitplan.'),
 'fr': ('Un petit hôtel est-il viable à Bahía Petempich ?', 'Là où l’usage du sol l’admet, oui, en format réduit. Le secteur compte peu de lots et le dossier environnemental lié au Parc National du Récif fixe tout le calendrier.'),
 'zh': ('在 Bahía Petempich 做小型酒店可行吗？', '在土地用途允许之处可行，但规模须小。该片区地块稀少，且因珊瑚礁国家公园而产生的环保申报决定了整体进度。')},
'playa-mujeres': {'es': ('¿Qué producto de hospedaje funciona en Playa Mujeres?', 'El de marca: residencias con servicio, condo-hotel o boutique de alto nivel. Todo pasa por el visto bueno de FONATUR, el comité de diseño y la licencia del municipio de Isla Mujeres.'),
 'en': ('What lodging product works in Playa Mujeres?', 'The branded one: serviced residences, condo-hotel or a high-end boutique. Everything goes through FONATUR sign-off, the design committee and the Isla Mujeres municipal licence.'),
 'ru': ('Какой продукт размещения работает в Плая-Мухерес?', 'Брендовый: резиденции с сервисом, кондо-отель или бутик высокого уровня. Всё проходит согласование FONATUR, комитет по дизайну и лицензию муниципалитета Isla Mujeres.'),
 'de': ('Welches Beherbergungsprodukt funktioniert in Playa Mujeres?', 'Das markengebundene: Serviced Residences, Condo-Hotel oder ein High-End-Boutique. Alles läuft über FONATUR-Freigabe, den Gestaltungsbeirat und die Lizenz der Gemeinde Isla Mujeres.'),
 'fr': ('Quel produit d’hébergement fonctionne à Playa Mujeres ?', 'Le produit de marque : résidences avec services, condo-hôtel ou boutique haut de gamme. Tout passe par l’accord FONATUR, le comité d’architecture et le permis de la commune d’Isla Mujeres.'),
 'zh': ('在 Playa Mujeres，哪类住宿产品可行？', '品牌化产品：带服务的住宅、产权式酒店或高端精品酒店。所有项目都需经 FONATUR 批准、设计委员会审核，并取得 Isla Mujeres 市政许可。')},
}


# appended 2026-08-09: 'how this differs from the neighbour' — the pairs that stayed
# above 0.55 similarity after the boilerplate was removed
DIFFER = {'tankah': {'es': ' Frente a Bahía Solimán, Tankah es más cerrada y más tranquila: el arrecife deja el agua casi sin oleaje, los lotes son algo menores y Casa Cenote está al lado, con agua dulce mezclándose con el mar. Es el argumento de venta que Solimán no tiene y el que sostiene la tarifa por noche.', 'en': ' Compared with Soliman Bay, Tankah is more enclosed and calmer: the reef leaves the water almost without swell, lots are somewhat smaller and Casa Cenote sits right there, fresh water meeting the sea. That is the selling point Soliman does not have, and what holds the nightly rate.', 'ru': ' В отличие от Баия-Солиман, Танках более закрытая и тихая: риф оставляет воду почти без волн, участки чуть меньше, а рядом Каса-Сеноте, где пресная вода смешивается с морской. Это аргумент, которого у Солимана нет, и именно он держит тариф за ночь.', 'de': ' Im Vergleich zu Bahía Solimán ist Tankah geschlossener und ruhiger: Das Riff nimmt dem Wasser fast jeden Wellengang, die Grundstücke sind etwas kleiner und Casa Cenote liegt direkt daneben, wo Süßwasser auf das Meer trifft. Das ist das Verkaufsargument, das Solimán nicht hat — und was die Übernachtungsrate trägt.', 'fr': ' Face à Bahía Solimán, Tankah est plus fermée et plus calme : le récif laisse une eau presque sans houle, les terrains sont un peu plus petits et Casa Cenote est juste à côté, l’eau douce rejoignant la mer. C’est l’argument que Solimán n’a pas, et celui qui soutient le tarif à la nuitée.', 'zh': ' 与 Bahía Solimán 相比，Tankah 更封闭也更安静：珊瑚礁让海面几乎没有涌浪，地块略小，而 Casa Cenote 就在旁边，淡水在此汇入大海。这是 Solimán 所不具备的卖点，也是支撑每晚房价的关键。'}, 'bahia-soliman': {'es': ' A diferencia de Tankah, Solimán ofrece lotes más grandes y una bahía más abierta: más privacidad y frente de playa por propiedad, a cambio de más camino hasta Tulum y de resolver la autonomía a mayor escala. Es la opción de quien quiere una sola casa grande, no varias pequeñas.', 'en': ' Unlike Tankah, Soliman offers larger lots and a more open bay: more privacy and beachfront per property, in exchange for a longer drive to Tulum and self-sufficiency solved at a bigger scale. It is the choice for one large house, not several small ones.', 'ru': ' В отличие от Танкаха, Солиман — это более крупные участки и более открытая бухта: больше приватности и береговой линии на объект, но дальше ехать до Тулума и автономность нужно решать в большем масштабе. Вариант для одного большого дома, а не нескольких маленьких.', 'de': ' Anders als Tankah bietet Solimán größere Grundstücke und eine offenere Bucht: mehr Privatsphäre und Strandfront pro Objekt, dafür längere Fahrt nach Tulum und Autarkie in größerem Maßstab. Die Wahl für ein großes Haus, nicht für mehrere kleine.', 'fr': ' Contrairement à Tankah, Solimán propose de plus grands terrains et une baie plus ouverte : davantage d’intimité et de front de mer par propriété, en échange d’un trajet plus long vers Tulum et d’une autonomie à plus grande échelle. C’est le choix d’une seule grande maison, pas de plusieurs petites.', 'zh': ' 与 Tankah 不同，Solimán 的地块更大、海湾更开阔：单个物业拥有更强的私密性与更长的海岸线，代价是前往图卢姆的车程更长，且自给系统需按更大规模配置。它适合建一栋大宅，而非若干小屋。'}, 'selvazama': {'es': ' A diferencia de Tankah o Solimán, aquí no hay playa ni ZOFEMAT: es suelo urbanizado con servicios conectados. Se cambia el frente de mar por un arranque de obra sin pozo, sin planta propia y sin depender de un camino de terracería, y por la posibilidad de uso mixto dentro del mismo plan maestro.', 'en': ' Unlike Tankah or Soliman, there is no beach and no ZOFEMAT here: it is urbanised land with connected services. You trade the beachfront for a build that starts without a well, without its own plant and without depending on a dirt road — plus the option of mixed use inside the same master plan.', 'ru': ' В отличие от Танкаха или Солимана, здесь нет пляжа и нет ZOFEMAT: это урбанизированная земля с подключёнными коммуникациями. Первая линия меняется на старт стройки без скважины, без своих очистных и без зависимости от грунтовой дороги — плюс возможность смешанного использования внутри мастер-плана.', 'de': ' Anders als Tankah oder Solimán gibt es hier weder Strand noch ZOFEMAT: erschlossenes Land mit angeschlossener Versorgung. Man tauscht die Strandlage gegen einen Baustart ohne Brunnen, ohne eigene Anlage und ohne Abhängigkeit von einer Schotterpiste — dazu die Option der Mischnutzung im selben Masterplan.', 'fr': ' Contrairement à Tankah ou Solimán, il n’y a ici ni plage ni ZOFEMAT : c’est du foncier viabilisé avec les réseaux raccordés. On échange le front de mer contre un chantier qui démarre sans puits, sans station propre et sans dépendre d’une piste — avec en prime la possibilité d’usage mixte dans le même plan-masse.', 'zh': ' 与 Tankah 或 Solimán 不同，这里既无海滩也不涉及 ZOFEMAT：这是市政配套已接入的城市化土地。以放弃海景为代价，换来的是无需水井、无需自建处理设备、也不依赖土路即可开工，并且可在同一总体规划内做混合用途。'}, 'el-cielo-playa-del-carmen': {'es': ' Frente a Selvamar, El Cielo es más comunidad y menos selva: andadores, ciclovías, áreas deportivas y vida de barrio, con la playa de Xcalacoco a pocos minutos. Selvamar cambia todo eso por densidad más baja y vegetación conservada; El Cielo por amenidades y movimiento.', 'en': ' Compared with Selvamar, El Cielo is more community and less jungle: walking and cycling paths, sports areas and neighbourhood life, with Xcalacoco beach minutes away. Selvamar trades all that for lower density and preserved vegetation; El Cielo trades it for amenities and activity.', 'ru': ' По сравнению с Сельвамаром Эль-Сьело — это больше сообщество и меньше сельвы: дорожки, велодорожки, спортивные зоны и жизнь района, а пляж Шкалакоко в нескольких минутах. Сельвамар меняет это на более низкую плотность и сохранённую растительность; Эль-Сьело — на инфраструктуру и движение.', 'de': ' Im Vergleich zu Selvamar ist El Cielo mehr Gemeinschaft und weniger Dschungel: Fuß- und Radwege, Sportflächen und Nachbarschaftsleben, der Strand von Xcalacoco wenige Minuten entfernt. Selvamar tauscht das gegen geringere Dichte und erhaltene Vegetation; El Cielo gegen Ausstattung und Betrieb.', 'fr': ' Face à Selvamar, El Cielo est davantage communauté que jungle : allées, pistes cyclables, espaces sportifs et vie de quartier, avec la plage de Xcalacoco à quelques minutes. Selvamar échange tout cela contre une densité plus faible et une végétation préservée ; El Cielo, contre des équipements et de l’animation.', 'zh': ' 与 Selvamar 相比，El Cielo 更偏社区氛围而非丛林：步道、自行车道、运动场地与浓厚的邻里生活，Xcalacoco 海滩仅数分钟车程。Selvamar 以更低密度与保留植被取胜；El Cielo 则胜在配套与活力。'}, 'selvamar-playa-del-carmen': {'es': ' Frente a El Cielo, Selvamar apuesta por lo contrario: manzanas rodeadas de selva conservada, densidad baja y silencio, sin playa propia ni tanta amenidad. Si el proyecto vive de la naturaleza y del sonido de la selva, es aquí; si vive de la vida de comunidad, es El Cielo.', 'en': ' Compared with El Cielo, Selvamar bets the other way: blocks surrounded by preserved jungle, low density and quiet, with no beach of its own and fewer amenities. If the project lives off nature and the sound of the jungle, it belongs here; if it lives off community life, it belongs in El Cielo.', 'ru': ' В отличие от Эль-Сьело, Сельвамар ставит на обратное: кварталы в сохранённой сельве, низкая плотность и тишина, без своего пляжа и без обилия инфраструктуры. Если проект живёт природой и звуком джунглей — это сюда; если жизнью сообщества — в Эль-Сьело.', 'de': ' Gegenüber El Cielo setzt Selvamar auf das Gegenteil: Blöcke inmitten erhaltenen Dschungels, geringe Dichte und Ruhe, ohne eigenen Strand und mit weniger Ausstattung. Lebt das Projekt von Natur und Dschungelgeräuschen, gehört es hierher; lebt es vom Gemeinschaftsleben, nach El Cielo.', 'fr': ' Face à El Cielo, Selvamar mise sur l’inverse : des îlots entourés de jungle préservée, une faible densité et le calme, sans plage propre ni autant d’équipements. Si le projet vit de la nature et du bruit de la jungle, c’est ici ; s’il vit de la vie de communauté, c’est El Cielo.', 'zh': ' 与 El Cielo 相反，Selvamar 走的是另一条路：街区被保留的丛林环抱，密度低、环境安静，没有自有海滩，配套也更少。若项目依托自然与丛林声景，就选这里；若依托社区生活，则选 El Cielo。'}, 'ciudad-mayakoba': {'es': ' Conviene no confundirlo con dos vecinos: Mayakoba es el complejo de resorts y residencias privadas, y Corasol es la comunidad de golf con beach club propio. Ciudad Mayakoba es plan maestro urbano —lotes unifamiliares, multifamiliares y uso mixto alrededor de un country club—, y por eso admite programas que en los otros dos no caben.', 'en': ' It should not be confused with two neighbours: Mayakoba is the resort and private residence complex, and Corasol is the golf community with its own beach club. Ciudad Mayakoba is an urban master plan — single-family, multi-family and mixed-use lots around a country club — which is why it allows programmes the other two cannot host.', 'ru': ' Важно не путать с двумя соседями: Майякоба — комплекс курортов и частных резиденций, Корасоль — гольф-комьюнити со своим бич-клубом. Сьюдад-Майякоба — городской мастер-план с участками под индивидуальные дома, многоквартирные и смешанные проекты вокруг кантри-клуба, поэтому здесь возможны программы, которые в тех двух не помещаются.', 'de': ' Nicht zu verwechseln mit zwei Nachbarn: Mayakoba ist die Resort- und Privatresidenz-Anlage, Corasol die Golf-Community mit eigenem Beachclub. Ciudad Mayakoba ist ein urbaner Masterplan — Einfamilien-, Mehrfamilien- und Mischnutzungsgrundstücke rund um einen Country Club — und lässt deshalb Programme zu, die in den beiden anderen keinen Platz haben.', 'fr': ' À ne pas confondre avec deux voisins : Mayakoba est le complexe de resorts et de résidences privées, et Corasol la communauté de golf avec son propre beach club. Ciudad Mayakoba est un plan-masse urbain — lots individuels, collectifs et mixtes autour d’un country club — d’où des programmes que les deux autres ne peuvent accueillir.', 'zh': ' 需与两个近邻区分开：Mayakoba 是度假村与私人住宅综合体，Corasol 是拥有自有海滩俱乐部的高尔夫社区。Ciudad Mayakoba 则是城市总体规划区——围绕乡村俱乐部布置独栋、多户与混合用途地块——因此可容纳前两者无法承载的开发内容。'}}
for _k, _d in DIFFER.items():
    for _l, _t in _d.items():
        TEXT[_k][_l] = TEXT[_k][_l] + _t


def register_base_zone(k):
    """Register the underlying zone so ml.NORM/ml.SOIL for it exist in this process
    (the source generators only do that inside their __main__)."""
    for m in SRC:
        zd = getattr(m, 'ZONE', None) or getattr(m, 'ZONE2', None) or getattr(m, 'ZONE3', None) or getattr(m, 'ZONE4', None)
        if not zd or k not in zd:
            continue
        d = zd[k]
        if hasattr(m, 'ZNAME'):                      # gen-casas-zonas.py layout
            for l in LANGS:
                z1.ZNAME.setdefault(l, {})[k] = m.ZNAME[l][k]
            z1.ZAREA[k] = m.ZAREA[k]; z1.ZTEXT[k] = m.ZTEXT[k]; z1.ZFAQ[k] = m.ZFAQ[k]
            for l in LANGS:
                z1.ZLINKS.setdefault(l, {})[k] = m.ZLINKS[l][k]
        else:                                        # batches 2/3/4 layout
            for l in LANGS:
                z1.ZNAME.setdefault(l, {})[k] = m.NAMES[k][l]
            z1.ZAREA[k] = m.AREAS[k]; z1.ZTEXT[k] = m.TEXT[k]
            fq = getattr(m, 'FAQ2', None) or getattr(m, 'FAQ3', None) or getattr(m, 'FAQ4', None)
            z1.ZFAQ[k] = fq[k]
            lk = getattr(m, 'LINKS2', None) or getattr(m, 'LINKS3', None) or getattr(m, 'LINKS4', None)
            for l in LANGS:
                z1.ZLINKS.setdefault(l, {})[k] = lk[l][k]
        z1.register(k, d)
        for name in ('ZNORM_OVERRIDE', 'NORM_OVR'):
            ovr = getattr(m, name, {})
            if k in ovr:
                for l, txt in ovr[k].items():
                    ml.NORM[l][k] = txt
        for l, txt in getattr(m, 'SOIL_OVR', {}).get(k, {}).items():
            ml.SOIL[l][k] = txt
        return True
    raise SystemExit('zone not found in any source generator: ' + k)


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
    for k in Z:
        register_base_zone(k)
    for k, zk in [(k, 'vh-' + k) for k in Z]:
        z1.ZAREA[zk] = AREAS[zk]
        z1.ZTEXT[zk] = TEXT[k]
        z1.ZFAQ[zk] = {l: [FAQ1[k][l], GENERIC_FAQ[l]] for l in LANGS}
    for lang in LANGS:
        z1.ZLINKS.setdefault(lang, {})
    pref = {'es': 'construccion-de-casas', 'en': 'house-construction', 'ru': 'stroitelstvo-domov',
            'de': 'hausbau', 'fr': 'construction-de-maisons', 'zh': 'zhuzhai-jianzao'}
    TOWN = {'playa-del-carmen': {'es':'Playa del Carmen','en':'Playa del Carmen','ru':'Плая-дель-Кармен','de':'Playa del Carmen','fr':'Playa del Carmen','zh':'普拉亚德尔卡门'},
            'tulum': {'es':'Tulum','en':'Tulum','ru':'Тулум','de':'Tulum','fr':'Tulum','zh':'图卢姆'},
            'cancun': {'es':'Cancún','en':'Cancún','ru':'Канкун','de':'Cancún','fr':'Cancún','zh':'坎昆'}}
    hub = {'es': 'Construcción de casas', 'en': 'House construction', 'ru': 'Строительство домов',
           'de': 'Hausbau', 'fr': 'Construction de maisons', 'zh': '住宅建造'}
    permlink = {'es': ('/permisos-licencias-construccion-riviera-maya/', 'Permisos, licencias y DRO'),
                'en': ('/construction-permits-licenses-riviera-maya/', 'Permits, licences and DRO'),
                'ru': ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'),
                'de': ('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen, Lizenzen und DRO'),
                'fr': ('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'),
                'zh': ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO')}
    hotels = {'es': ('/construccion-comercial-hoteles-riviera-maya/', 'Construcción comercial y hoteles'),
              'en': ('/commercial-hotel-construction-riviera-maya/', 'Commercial and hotel construction'),
              'ru': ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения и лицензии'),
              'de': ('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen und Lizenzen'),
              'fr': ('/permis-et-licences-construction-riviera-maya/', 'Permis et licences'),
              'zh': ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可')}
    calc = {'es': ('/calculadora/', 'Calculadora de costos'), 'en': ('/calculator/', 'Cost calculator'),
            'ru': ('/kalkulyator/', 'Калькулятор стоимости'), 'de': ('/kostenrechner/', 'Kostenrechner'),
            'fr': ('/calculateur/', 'Calculateur de coûts'), 'zh': ('/jisuanqi/', '造价计算器')}
    for zk, d in ZONES.items():
        for lang in LANGS:
            z1.ZLINKS[lang][zk] = [
                ('/%s-%s/' % (pref[lang], d['zone']), '%s — %s' % (hub[lang], NAMES[zk][lang])),
                ('/%s-%s/' % (pref[lang], d['parent']), '%s — %s' % (hub[lang], TOWN[d['parent']][lang])),
                permlink[lang], hotels[lang], calc[lang]]
    for k in ['h1', 'title', 'desc', 'block', 'alert', 'h_cost', 'row', 'h_proc']:
        ml.OVR.setdefault(k, {})
    for zk, d in ZONES.items():
        for lang in LANGS:
            z1.ZNAME.setdefault(lang, {})[zk] = NAMES[zk][lang]
        z1.register(zk, d)
        for lang in LANGS:
            ml.SLUG[lang][zk] = '%s-%s' % (SLUG_PREFIX[lang], BASE_SLUG[zk])
            # inherit the zone's own municipal rules and append the hotel layer
            ml.NORM[lang][zk] = ml.NORM[lang][d['zone']] + HOTEL_LAYER[lang]
            ml.SOIL[lang][zk] = ml.SOIL[lang][d['zone']]
            c = NAMES[zk][lang]; nm = ml.NUM[zk]
            ml.OVR['h1'].setdefault(zk, {})[lang] = il.H1[lang].format(c=c)
            ml.OVR['title'].setdefault(zk, {})[lang] = il.TITLE[lang].format(c=c)
            ml.OVR['desc'].setdefault(zk, {})[lang] = il.DESC[lang].format(c=c)
            ml.OVR['alert'].setdefault(zk, {})[lang] = il.ALERT[lang].format(
                c=c, m2=nm['m2'], usd=nm['usd'], key=KEYS[zk][2].split(' – ')[0])
            ml.OVR['h_cost'].setdefault(zk, {})[lang] = il.H_COST[lang].format(c=c)
            ml.OVR['row'].setdefault(zk, {})[lang] = il.ROW[lang]
            ml.OVR['h_proc'].setdefault(zk, {})[lang] = il.H_PROC[lang]
            ml.OVR['block'].setdefault(zk, {})[lang] = block(zk, lang)
    ml.LOCS.extend(ZONES)
    for lang in LANGS:
        ch = ml.chrome(lang)
        for zk in ZONES:
            out = ml.SLUG[lang][zk]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, zk, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
    print('generated %d pages' % (len(ZONES) * len(LANGS)))
