#!/usr/bin/env python3
"""Third luxury-zone batch (2026-08-09): Tankah, Punta Brava, Riviera Cancún.

Verified before writing:
  Bahía Tankah (Tulum) — low-density beachfront villas north of Tulum, reef-
    protected calm bay, Casa Cenote / Cenote Manatí next door.
  Punta Brava (Puerto Morelos) — beachfront + residential lots south of Puerto
    Morelos town, coral reef just offshore, wetlands; own municipality since 2016.
  Riviera Cancún — the golf corridor south of Cancún (Jack Nicklaus 18-hole course,
    resorts and residences). It straddles the Benito Juárez / Puerto Morelos
    boundary, so the page says we verify which municipality the lot falls in
    instead of claiming one — that is a real practical issue there.

Zones needing their own municipal rules or soil notes carry NORM/SOIL overrides
instead of inheriting the parent town's text.
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
z1 = load('gen-casas-zonas.py', 'z1')
ml = z1.ml

ZONE3 = {
 'tankah':         dict(parent='tulum',  f=1.22, perm='3–5'),
 'punta-brava':    dict(parent='cancun', f=1.32, perm='3–5'),
 'riviera-cancun': dict(parent='cancun', f=1.28, perm='3–5'),
}

NAMES = {
 'tankah': {'es': 'Bahía Tankah', 'en': 'Tankah Bay', 'ru': 'Баия-Танках', 'de': 'Bahía Tankah',
            'fr': 'Bahía Tankah', 'zh': 'Tankah 湾'},
 'punta-brava': {'es': 'Punta Brava, Puerto Morelos', 'en': 'Punta Brava, Puerto Morelos',
                 'ru': 'Пунта-Брава, Пуэрто-Морелос', 'de': 'Punta Brava, Puerto Morelos',
                 'fr': 'Punta Brava, Puerto Morelos', 'zh': 'Punta Brava（Puerto Morelos）'},
 'riviera-cancun': {'es': 'Riviera Cancún', 'en': 'Riviera Cancún', 'ru': 'Ривьера-Канкун',
                    'de': 'Riviera Cancún', 'fr': 'Riviera Cancún', 'zh': 'Riviera Cancún'},
}
AREAS = {
 'tankah': {'es': 'Bahía Tankah, Casa Cenote y la costa entre Akumal y Tulum',
            'en': 'Tankah Bay, Casa Cenote and the coast between Akumal and Tulum',
            'ru': 'Баия-Танках, Каса-Сеноте и побережье между Акумалем и Тулумом',
            'de': 'Bahía Tankah, Casa Cenote und der Küste zwischen Akumal und Tulum',
            'fr': 'Bahía Tankah, Casa Cenote et la côte entre Akumal et Tulum',
            'zh': 'Tankah 湾、Casa Cenote 及 Akumal 与图卢姆之间的海岸'},
 'punta-brava': {'es': 'Punta Brava y la costa al sur de Puerto Morelos',
            'en': 'Punta Brava and the coast south of Puerto Morelos',
            'ru': 'Пунта-Брава и побережье к югу от Пуэрто-Морелоса',
            'de': 'Punta Brava und der Küste südlich von Puerto Morelos',
            'fr': 'Punta Brava et la côte au sud de Puerto Morelos',
            'zh': 'Punta Brava 及 Puerto Morelos 以南海岸'},
 'riviera-cancun': {'es': 'el corredor de Riviera Cancún, entre Cancún y Puerto Morelos',
            'en': 'the Riviera Cancún corridor, between Cancún and Puerto Morelos',
            'ru': 'коридоре Ривьера-Канкун, между Канкуном и Пуэрто-Морелосом',
            'de': 'dem Korridor Riviera Cancún, zwischen Cancún und Puerto Morelos',
            'fr': 'le corridor de Riviera Cancún, entre Cancún et Puerto Morelos',
            'zh': '坎昆与 Puerto Morelos 之间的 Riviera Cancún 走廊'},
}

TEXT = {
'tankah': {
 'es': 'Bahía Tankah es una franja de villas frente al mar entre Akumal y Tulum, protegida por el arrecife: agua tranquila, densidad muy baja y lotes grandes, con Casa Cenote (Cenote Manatí) a unos pasos conectando el río subterráneo con el mar. Casi no hay infraestructura pública, así que la casa se diseña autónoma —pozo, cisterna, tratamiento y solar— y la logística de obra es más larga que en el centro de Tulum.',
 'en': 'Tankah Bay is a strip of beachfront villas between Akumal and Tulum, sheltered by the reef: calm water, very low density and large lots, with Casa Cenote (Cenote Manatí) a few steps away where the underground river meets the sea. Public infrastructure is almost absent, so the house is designed self-sufficient — well, cistern, treatment and solar — and construction logistics run longer than in central Tulum.',
 'ru': 'Баия-Танках — полоса вилл на первой линии между Акумалем и Тулумом, защищённая рифом: спокойная вода, очень низкая плотность и крупные участки, а рядом Каса-Сеноте (сенот Манати), где подземная река выходит к морю. Городских сетей практически нет, поэтому дом проектируется автономным — скважина, цистерна, очистные, солнечная станция, — а логистика стройки длиннее, чем в центре Тулума.',
 'de': 'Bahía Tankah ist ein Streifen von Strandvillen zwischen Akumal und Tulum, geschützt durch das Riff: ruhiges Wasser, sehr geringe Dichte und große Grundstücke, mit Casa Cenote (Cenote Manatí) wenige Schritte entfernt, wo der unterirdische Fluss das Meer trifft. Öffentliche Infrastruktur fehlt praktisch, das Haus wird autark geplant — Brunnen, Zisterne, Kläranlage und Solar — und die Baulogistik dauert länger als im Zentrum von Tulum.',
 'fr': 'Bahía Tankah est une bande de villas en bord de mer entre Akumal et Tulum, protégée par le récif : eau calme, densité très faible et grands terrains, avec Casa Cenote (Cenote Manatí) à quelques pas, là où la rivière souterraine rejoint la mer. L’infrastructure publique est quasi inexistante : la maison se conçoit autonome — puits, citerne, traitement et solaire — et la logistique de chantier est plus longue qu’au centre de Tulum.',
 'zh': 'Bahía Tankah 是 Akumal 与图卢姆之间的一段海滨别墅带，受珊瑚礁庇护：水面平静、密度极低、地块宽大，几步之遥即是 Casa Cenote（Manatí 天然井），地下河在此汇入大海。此处几乎没有市政基础设施，住宅按自给自足设计——水井、蓄水池、污水处理与太阳能——施工物流也比图卢姆市区更长。'},
'punta-brava': {
 'es': 'Punta Brava está al sur del pueblo de Puerto Morelos, a unos 20 minutos de Cancún: lotes residenciales y frente de playa con el arrecife a pocos metros de la orilla y humedales protegidos tierra adentro. Ese arrecife es la clave de la zona y también de la normativa: la obra se planea para no afectar el Parque Nacional Arrecife de Puerto Morelos, con drenaje resuelto por planta o biodigestor y control estricto de escurrimientos.',
 'en': 'Punta Brava sits south of Puerto Morelos town, about 20 minutes from Cancún: residential and beachfront lots with the reef only metres offshore and protected wetlands inland. That reef defines both the appeal and the rules: the build is planned so as not to affect the Puerto Morelos Reef National Park, with drainage solved by a treatment plant or biodigester and strict runoff control.',
 'ru': 'Пунта-Брава расположена к югу от посёлка Пуэрто-Морелос, примерно в 20 минутах от Канкуна: жилые и пляжные участки, риф в нескольких метрах от берега и охраняемые водно-болотные угодья вглубь материка. Именно риф определяет и ценность зоны, и правила: стройка планируется так, чтобы не затронуть Национальный парк «Риф Пуэрто-Морелос», канализация решается очистными или биодигестером, а сток контролируется строго.',
 'de': 'Punta Brava liegt südlich des Orts Puerto Morelos, etwa 20 Minuten von Cancún: Wohn- und Strandgrundstücke mit dem Riff nur wenige Meter vor der Küste und geschützten Feuchtgebieten im Hinterland. Dieses Riff bestimmt Reiz und Regeln zugleich: Gebaut wird so, dass der Nationalpark Riff von Puerto Morelos unberührt bleibt — Entwässerung über Kläranlage oder Biodigester und strenge Kontrolle des Oberflächenabflusses.',
 'fr': 'Punta Brava se situe au sud du village de Puerto Morelos, à environ 20 minutes de Cancún : des lots résidentiels et en front de plage, avec le récif à quelques mètres du rivage et des zones humides protégées à l’intérieur. Ce récif fait à la fois l’attrait et la règle : le chantier est planifié pour ne pas affecter le Parc National du Récif de Puerto Morelos, avec assainissement par station ou biodigesteur et contrôle strict des ruissellements.',
 'zh': 'Punta Brava 位于 Puerto Morelos 镇以南，距坎昆约20分钟车程：住宅与海滨地块，珊瑚礁距岸仅数米，内陆则是受保护的湿地。这片珊瑚礁既是该区的价值所在，也是规则来源：施工须确保不影响 Puerto Morelos 珊瑚礁国家公园，排水以处理设备或生物消化池解决，并严格控制地表径流。'},
'riviera-cancun': {
 'es': 'Riviera Cancún es el corredor de golf y resorts al sur de Cancún, con el campo de 18 hoyos diseñado por Jack Nicklaus como eje y residencias y condominios alrededor. Está a minutos del aeropuerto, lo que lo vuelve la zona más cómoda de la costa norte para quien viaja seguido. Ojo con un detalle práctico: el corredor cruza el límite entre Benito Juárez y Puerto Morelos, así que lo primero es confirmar en qué municipio cae su lote — de eso depende toda la ruta de permisos.',
 'en': 'Riviera Cancún is the golf and resort corridor south of Cancún, built around the 18-hole Jack Nicklaus course, with residences and condominiums alongside. It is minutes from the airport, which makes it the most convenient stretch of the north coast for owners who travel often. One practical detail matters: the corridor crosses the boundary between Benito Juárez and Puerto Morelos, so the first step is confirming which municipality your lot falls in — the entire permit route depends on it.',
 'ru': 'Ривьера-Канкун — гольф- и курортный коридор к югу от Канкуна, построенный вокруг 18-луночного поля Джека Никлауса, с резиденциями и кондоминиумами вдоль него. До аэропорта — минуты, поэтому это самый удобный участок северного побережья для тех, кто часто летает. Важная практическая деталь: коридор пересекает границу между Benito Juárez и Пуэрто-Морелосом, поэтому первым делом подтверждаем, в каком муниципалитете ваш участок — от этого зависит весь маршрут разрешений.',
 'de': 'Riviera Cancún ist der Golf- und Resortkorridor südlich von Cancún, angelegt um den 18-Loch-Platz von Jack Nicklaus, mit Residenzen und Eigentumswohnungen ringsum. Der Flughafen liegt Minuten entfernt, was den Abschnitt zur bequemsten Lage der Nordküste für Vielreisende macht. Ein praktisches Detail ist entscheidend: Der Korridor überschreitet die Grenze zwischen Benito Juárez und Puerto Morelos — zuerst wird geklärt, in welcher Gemeinde Ihr Grundstück liegt, davon hängt der gesamte Genehmigungsweg ab.',
 'fr': 'Riviera Cancún est le corridor de golf et de resorts au sud de Cancún, organisé autour du parcours 18 trous signé Jack Nicklaus, avec résidences et copropriétés alentour. L’aéroport est à quelques minutes, ce qui en fait le secteur le plus pratique de la côte nord pour qui voyage souvent. Un détail pratique compte : le corridor franchit la limite entre Benito Juárez et Puerto Morelos ; la première étape est donc de confirmer la commune dont dépend votre terrain — tout le parcours des permis en découle.',
 'zh': 'Riviera Cancún 是坎昆以南的高尔夫与度假走廊，以 Jack Nicklaus 设计的18洞球场为核心，沿线分布住宅与公寓。距机场仅数分钟，是北部海岸对常旅客最便利的一段。有一个务实细节需注意：该走廊横跨 Benito Juárez 与 Puerto Morelos 的行政边界，因此第一步是确认您的地块归属哪个市——整条许可路径都取决于此。'},
}

NORM_OVR = {
'punta-brava': {
 'es': 'Punta Brava está en el municipio de Puerto Morelos, independiente desde 2016 y con criterios propios más estrictos por el arrecife: ahí se tramitan uso de suelo y licencia de construcción con proyecto firmado por DRO. En lotes frente al mar entra la concesión ZOFEMAT, y la cercanía del Parque Nacional Arrecife de Puerto Morelos y de los humedales suele activar autorización ambiental, con condiciones sobre desmonte, escurrimientos y tratamiento de aguas.',
 'en': 'Punta Brava is in the municipality of Puerto Morelos, independent since 2016 and stricter than its neighbours because of the reef: land use and the building licence are processed there with drawings signed by a DRO. Beachfront lots require a ZOFEMAT concession, and the proximity of the Puerto Morelos Reef National Park and the wetlands usually triggers environmental authorisation with conditions on clearing, runoff and wastewater treatment.',
 'ru': 'Пунта-Брава относится к муниципалитету Пуэрто-Морелос, самостоятельному с 2016 года и более строгому, чем соседи, из-за рифа: там оформляются назначение земли и разрешение на строительство с проектом за подписью DRO. На участках у моря требуется концессия ZOFEMAT, а близость Национального парка «Риф Пуэрто-Морелос» и водно-болотных угодий обычно включает экологическое согласование с условиями по расчистке, стоку и очистке сточных вод.',
 'de': 'Punta Brava liegt in der Gemeinde Puerto Morelos, seit 2016 eigenständig und wegen des Riffs strenger als die Nachbargemeinden: Dort werden Nutzungsart und Baugenehmigung mit DRO-unterzeichneten Plänen bearbeitet. Strandgrundstücke benötigen eine ZOFEMAT-Konzession, und die Nähe zum Nationalpark Riff von Puerto Morelos sowie zu den Feuchtgebieten löst meist eine Umweltgenehmigung mit Auflagen zu Rodung, Abfluss und Abwasserbehandlung aus.',
 'fr': 'Punta Brava dépend de la commune de Puerto Morelos, indépendante depuis 2016 et plus stricte que ses voisines à cause du récif : usage du sol et permis de construire s’y traitent avec des plans signés par un DRO. Les lots en front de mer exigent une concession ZOFEMAT, et la proximité du Parc National du Récif de Puerto Morelos et des zones humides déclenche généralement une autorisation environnementale assortie de conditions sur le défrichement, le ruissellement et le traitement des eaux.',
 'zh': 'Punta Brava 隶属 Puerto Morelos 市，该市自2016年独立设市，并因珊瑚礁而比周边更为严格：土地用途与施工许可均在该市办理，图纸须由 DRO 签署。海滨地块需 ZOFEMAT 特许；毗邻 Puerto Morelos 珊瑚礁国家公园与湿地，通常还会触发环保许可，并对清林、径流与污水处理提出具体条件。'},
'riviera-cancun': {
 'es': 'El corredor de Riviera Cancún cruza el límite municipal entre Benito Juárez y Puerto Morelos, y ese es el primer punto a resolver: la licencia de construcción y el uso de suelo se tramitan en el municipio al que pertenece el predio, con proyecto firmado por DRO en ambos casos. En lotes frente al mar aplica concesión ZOFEMAT, en desarrollos con reglamento interno hay comité de diseño, y del lado de Puerto Morelos pesa además la protección del arrecife. Confirmamos la jurisdicción antes de mover un solo trámite.',
 'en': 'The Riviera Cancún corridor crosses the municipal boundary between Benito Juárez and Puerto Morelos, and that is the first thing to settle: land use and the building licence are filed in whichever municipality the lot belongs to, with DRO-signed drawings either way. Beachfront lots require a ZOFEMAT concession, developments with internal by-laws add a design committee, and on the Puerto Morelos side reef protection weighs in as well. We confirm the jurisdiction before starting a single filing.',
 'ru': 'Коридор Ривьера-Канкун пересекает муниципальную границу между Benito Juárez и Пуэрто-Морелосом, и это первое, что нужно закрыть: назначение земли и разрешение на строительство подаются в тот муниципалитет, которому принадлежит участок, — с проектом за подписью DRO в обоих случаях. На участках у моря нужна концессия ZOFEMAT, в застройках со своим регламентом добавляется комитет по дизайну, а со стороны Пуэрто-Морелоса ещё и защита рифа. Юрисдикцию подтверждаем до начала любых процедур.',
 'de': 'Der Korridor Riviera Cancún überschreitet die Gemeindegrenze zwischen Benito Juárez und Puerto Morelos — das ist zuerst zu klären: Nutzungsart und Baugenehmigung werden in der Gemeinde eingereicht, zu der das Grundstück gehört, in beiden Fällen mit DRO-unterzeichneten Plänen. Strandgrundstücke brauchen eine ZOFEMAT-Konzession, Anlagen mit eigener Satzung zusätzlich einen Gestaltungsbeirat, und auf der Seite von Puerto Morelos kommt der Riffschutz hinzu. Wir klären die Zuständigkeit, bevor ein einziger Antrag läuft.',
 'fr': 'Le corridor de Riviera Cancún franchit la limite communale entre Benito Juárez et Puerto Morelos, et c’est le premier point à trancher : usage du sol et permis de construire se déposent dans la commune dont relève le terrain, avec des plans signés par un DRO dans les deux cas. Les lots en front de mer exigent une concession ZOFEMAT, les développements dotés d’un règlement interne ajoutent un comité d’architecture, et côté Puerto Morelos s’ajoute la protection du récif. Nous confirmons la juridiction avant d’engager la moindre démarche.',
 'zh': 'Riviera Cancún 走廊横跨 Benito Juárez 与 Puerto Morelos 的市界，这是首先要厘清的问题：土地用途与施工许可须向地块所属的市政递交，两种情形下图纸均需 DRO 签署。海滨地块需 ZOFEMAT 特许；设有内部规约的开发区还需经设计委员会审核；位于 Puerto Morelos 一侧的还须考虑珊瑚礁保护。我们会在启动任何报批前先确认管辖归属。'},
}
SOIL_OVR = {
'punta-brava': {
 'es': 'Roca caliza con manto freático muy somero y humedales cercanos: el estudio de mecánica de suelos define la cimentación y, sobre todo, la cota de desplante para no comprometer el escurrimiento natural. Frente al mar, especificación marina completa —recubrimientos mayores, herrería tratada, cancelería anodizada, impermeabilización reforzada— porque el arrecife está a metros y la brisa salina es constante.',
 'en': 'Limestone with a very shallow water table and wetlands nearby: the soil study sets the foundation and, above all, the finished floor level so natural runoff is not compromised. On the beachfront, a full marine spec — greater cover, treated ironwork, anodised joinery, reinforced waterproofing — because the reef is metres away and salt breeze is constant.',
 'ru': 'Известняк с очень высоким уровнем грунтовых вод и водно-болотными угодьями рядом: геология определяет фундамент и, главное, отметку пола, чтобы не нарушить естественный сток. На первой линии — полная морская спецификация: увеличенный защитный слой, обработанный металл, анодированный алюминий, усиленная гидроизоляция, потому что риф в метрах, а солёный бриз постоянен.',
 'de': 'Kalkstein mit sehr hohem Grundwasserstand und nahen Feuchtgebieten: Das Bodengutachten bestimmt die Gründung und vor allem die Höhenlage des Erdgeschosses, damit der natürliche Abfluss nicht beeinträchtigt wird. Am Strand volle Meeresspezifikation — größere Deckung, behandelte Schlosserarbeiten, eloxierte Fenster, verstärkte Abdichtung — denn das Riff liegt wenige Meter entfernt und die Salzbrise ist konstant.',
 'fr': 'Calcaire avec nappe très affleurante et zones humides proches : l’étude de sol fixe les fondations et surtout le niveau du rez-de-chaussée pour ne pas compromettre le ruissellement naturel. En front de mer, spécification marine complète — enrobages renforcés, ferronnerie traitée, menuiseries anodisées, étanchéité renforcée — car le récif est à quelques mètres et la brise saline est permanente.',
 'zh': '石灰岩地层，地下水位极浅，且毗邻湿地：土力学勘察决定基础形式，更重要的是确定首层标高，以免影响自然径流。海滨地块采用完整的海洋环境标准——加大保护层、铁件防腐、阳极氧化门窗、加强防水——因为珊瑚礁近在数米之外，咸风常年不断。'},
'riviera-cancun': {
 'es': 'Caliza con zonas de relleno y nivel freático alto, típico del corredor entre Cancún y Puerto Morelos. El estudio de mecánica de suelos define cimentación y tratamiento de humedad; en predios cercanos a la playa o a los humedales se refuerza la impermeabilización y la protección anticorrosiva del acero, y se cuida la cota de desplante por escurrimientos.',
 'en': 'Limestone with fill areas and a high water table, typical of the corridor between Cancún and Puerto Morelos. The soil study sets the foundation and the damp-proofing strategy; on lots near the beach or the wetlands, waterproofing and rebar corrosion protection are reinforced, and the finished floor level is checked against runoff.',
 'ru': 'Известняк с участками насыпного грунта и высоким уровнем грунтовых вод — типично для коридора между Канкуном и Пуэрто-Морелосом. Геология определяет фундамент и схему защиты от влаги; на участках у пляжа или водно-болотных угодий усиливаются гидроизоляция и антикоррозийная защита арматуры, а отметка пола проверяется по стоку.',
 'de': 'Kalkstein mit Auffüllungen und hohem Grundwasserstand, typisch für den Korridor zwischen Cancún und Puerto Morelos. Das Bodengutachten legt Gründung und Feuchteschutz fest; bei Grundstücken nahe Strand oder Feuchtgebieten werden Abdichtung und Korrosionsschutz verstärkt und die Höhenlage des Erdgeschosses am Abfluss geprüft.',
 'fr': 'Calcaire avec zones de remblai et nappe haute, typique du corridor entre Cancún et Puerto Morelos. L’étude de sol fixe les fondations et le traitement de l’humidité ; sur les lots proches de la plage ou des zones humides, l’étanchéité et la protection anticorrosion des aciers sont renforcées, et le niveau du rez-de-chaussée est vérifié au regard du ruissellement.',
 'zh': '石灰岩夹回填区、地下水位偏高，是坎昆至 Puerto Morelos 走廊的典型地层。土力学勘察确定基础与防潮方案；靠近海滩或湿地的地块需加强防水与钢筋防腐，并结合径流复核首层标高。'},
}

FAQ3 = {
'tankah': {
 'es': [('¿Hay servicios públicos en Bahía Tankah?', 'Prácticamente no. Resolvemos agua con pozo y cisterna, drenaje con planta de tratamiento o biodigestor y energía con solar más respaldo. Se dimensiona en el anteproyecto, porque cambia el presupuesto.'),
        ('¿Qué permisos aplican en Tankah?', 'Licencia municipal de Tulum con DRO, autorización ambiental de SEMA en la mayoría de los predios y concesión ZOFEMAT frente a playa, con cuidado adicional por el arrecife y el sistema de cenotes.')],
 'en': [('Are there public utilities in Tankah Bay?', 'Practically none. We solve water with a well and cistern, drainage with a treatment plant or biodigester and power with solar plus backup. It is sized at concept stage because it moves the budget.'),
        ('Which permits apply in Tankah?', 'The Tulum municipal licence with a DRO, SEMA environmental authorisation on most lots and a ZOFEMAT concession on the beachfront, with extra care for the reef and the cenote system.')],
 'ru': [('Есть ли в Баия-Танках городские сети?', 'Практически нет. Воду решаем скважиной и цистерной, канализацию — очистными или биодигестером, электричество — солнечной станцией с резервом. Считаем на стадии эскиза, потому что это меняет бюджет.'),
        ('Какие разрешения нужны в Танкахе?', 'Муниципальная лицензия Тулума с DRO, экологическое разрешение SEMA на большинстве участков и концессия ZOFEMAT на первой линии, с повышенным вниманием к рифу и системе сенотов.')],
 'de': [('Gibt es öffentliche Versorgung in Bahía Tankah?', 'Praktisch keine. Wasser lösen wir über Brunnen und Zisterne, Abwasser über Kläranlage oder Biodigester, Strom über Solar mit Backup. Das wird im Entwurf dimensioniert, denn es verschiebt das Budget.'),
        ('Welche Genehmigungen gelten in Tankah?', 'Kommunale Lizenz von Tulum mit DRO, SEMA-Umweltgenehmigung auf den meisten Grundstücken und ZOFEMAT-Konzession am Strand — mit besonderer Sorgfalt für Riff und Cenotensystem.')],
 'fr': [('Y a-t-il des réseaux publics à Bahía Tankah ?', 'Quasiment aucun. Nous réglons l’eau par puits et citerne, l’assainissement par station ou biodigesteur et l’électricité par solaire avec secours. Tout cela se dimensionne dès l’avant-projet car cela pèse sur le budget.'),
        ('Quels permis s’appliquent à Tankah ?', 'Permis municipal de Tulum avec DRO, autorisation environnementale SEMA sur la plupart des lots et concession ZOFEMAT en front de plage, avec une vigilance accrue pour le récif et le système de cénotes.')],
 'zh': [('Tankah 湾有市政配套吗？', '基本没有。供水靠水井与蓄水池，排水靠污水处理设备或生物消化池，用电靠太阳能加备用电源。这些在方案阶段就要定型，因为会显著影响预算。'),
        ('Tankah 需要哪些许可？', '带 DRO 的图卢姆市政许可、多数地块所需的 SEMA 环保许可，以及海滨地块的 ZOFEMAT 特许；因珊瑚礁与天然井水系，审查更为审慎。')]},
'punta-brava': {
 'es': [('¿Qué municipio da la licencia en Punta Brava?', 'Puerto Morelos, municipio propio desde 2016. Ahí se tramitan uso de suelo y licencia con DRO; frente al mar se suma ZOFEMAT y, por el arrecife y los humedales, normalmente autorización ambiental.'),
        ('¿Qué cuidados exige el arrecife?', 'Drenaje con planta de tratamiento o biodigestor —nunca fosa simple—, control de escurrimientos durante la obra, manejo de residuos documentado y cota de desplante que respete el flujo natural del agua.')],
 'en': [('Which municipality issues the licence in Punta Brava?', 'Puerto Morelos, its own municipality since 2016. Land use and the licence with a DRO are processed there; beachfront adds ZOFEMAT and, because of the reef and wetlands, usually environmental authorisation.'),
        ('What does the reef require?', 'Drainage through a treatment plant or biodigester — never a simple septic pit — runoff control during construction, documented waste handling and a floor level that respects the natural water flow.')],
 'ru': [('Какой муниципалитет выдаёт лицензию в Пунта-Брава?', 'Пуэрто-Морелос, самостоятельный муниципалитет с 2016 года. Там оформляются назначение земли и лицензия с DRO; на берегу добавляется ZOFEMAT, а из-за рифа и водно-болотных угодий обычно и экологическое согласование.'),
        ('Что требует риф?', 'Канализацию через очистные или биодигестер — никогда простую выгребную яму, — контроль стока во время стройки, документированный вывоз отходов и отметку пола, уважающую естественный ход воды.')],
 'de': [('Welche Gemeinde erteilt die Lizenz in Punta Brava?', 'Puerto Morelos, seit 2016 eigene Gemeinde. Dort laufen Nutzungsart und Lizenz mit DRO; am Strand kommt ZOFEMAT hinzu und wegen Riff und Feuchtgebieten meist eine Umweltgenehmigung.'),
        ('Was verlangt das Riff?', 'Entwässerung über Kläranlage oder Biodigester — nie eine einfache Sickergrube —, Abflusskontrolle während des Baus, dokumentierte Abfallentsorgung und eine Höhenlage, die den natürlichen Wasserfluss respektiert.')],
 'fr': [('Quelle commune délivre le permis à Punta Brava ?', 'Puerto Morelos, commune à part entière depuis 2016. L’usage du sol et le permis avec DRO s’y traitent ; en front de mer s’ajoute la ZOFEMAT et, du fait du récif et des zones humides, généralement une autorisation environnementale.'),
        ('Qu’exige le récif ?', 'Un assainissement par station ou biodigesteur — jamais une simple fosse —, le contrôle des ruissellements pendant le chantier, une gestion documentée des déchets et un niveau de plancher respectant l’écoulement naturel.')],
 'zh': [('Punta Brava 由哪个市政发放许可？', 'Puerto Morelos 市，自2016年独立设市。土地用途与带 DRO 的许可均在该市办理；海滨地块另需 ZOFEMAT，且因珊瑚礁与湿地通常还需环保许可。'),
        ('珊瑚礁带来哪些要求？', '排水必须采用处理设备或生物消化池，绝不可用简易化粪坑；施工期间控制径流、废弃物处理需留痕，并按自然水流确定首层标高。')]},
'riviera-cancun': {
 'es': [('¿En qué municipio queda mi lote en Riviera Cancún?', 'Depende del punto exacto: el corredor cruza el límite entre Benito Juárez y Puerto Morelos. Lo verificamos con la constancia de uso de suelo antes de iniciar cualquier trámite, porque cambia autoridad, tiempos y requisitos.'),
        ('¿Cuánto cuesta construir en Riviera Cancún?', 'De $14,700 a $30,700 MXN por m² según acabados. La cercanía al aeropuerto abarata logística frente a Tulum, pero el estándar de la zona y la especificación marina suben el nivel respecto al promedio de Cancún.')],
 'en': [('Which municipality is my lot in at Riviera Cancún?', 'It depends on the exact spot: the corridor crosses the Benito Juárez / Puerto Morelos boundary. We verify it with the land-use certificate before starting any filing, because it changes the authority, the timeline and the requirements.'),
        ('How much does it cost to build in Riviera Cancún?', 'From $14,700 to $30,700 MXN per m² depending on finishes. Being close to the airport cuts logistics compared with Tulum, but the area’s standard and the marine spec push it above the Cancún average.')],
 'ru': [('В каком муниципалитете мой участок в Ривьера-Канкун?', 'Зависит от конкретной точки: коридор пересекает границу Benito Juárez и Пуэрто-Морелоса. Проверяем по справке о назначении земли до начала любых процедур, потому что меняются орган, сроки и требования.'),
        ('Сколько стоит стройка в Ривьера-Канкун?', 'От $14,700 до $30,700 MXN за м² в зависимости от отделки. Близость аэропорта удешевляет логистику по сравнению с Тулумом, но стандарт зоны и морская спецификация поднимают уровень относительно среднего по Канкуну.')],
 'de': [('In welcher Gemeinde liegt mein Grundstück in Riviera Cancún?', 'Das hängt vom genauen Punkt ab: Der Korridor überschreitet die Grenze zwischen Benito Juárez und Puerto Morelos. Wir prüfen es über die Nutzungsbescheinigung vor jedem Antrag, denn Behörde, Fristen und Anforderungen ändern sich.'),
        ('Was kostet Bauen in Riviera Cancún?', 'Von $14.700 bis $30.700 MXN pro m² je nach Ausbau. Die Flughafennähe verbilligt die Logistik gegenüber Tulum, doch Standard der Zone und Meeresspezifikation liegen über dem Durchschnitt von Cancún.')],
 'fr': [('Dans quelle commune se trouve mon terrain à Riviera Cancún ?', 'Cela dépend du point exact : le corridor franchit la limite entre Benito Juárez et Puerto Morelos. Nous le vérifions via le certificat d’usage du sol avant toute démarche, car cela change l’autorité, les délais et les exigences.'),
        ('Combien coûte la construction à Riviera Cancún ?', 'De 14 700 à 30 700 MXN le m² selon les finitions. La proximité de l’aéroport allège la logistique par rapport à Tulum, mais le standard du secteur et la spécification marine placent le niveau au-dessus de la moyenne de Cancún.')],
 'zh': [('我在 Riviera Cancún 的地块属于哪个市？', '取决于具体位置：该走廊横跨 Benito Juárez 与 Puerto Morelos 的边界。我们会在启动任何报批前，通过土地用途证明予以确认，因为主管机关、周期与要求都会随之改变。'),
        ('在 Riviera Cancún 建房要多少钱？', '按装修标准，每平方米 14,700 至 30,700 比索。邻近机场使物流成本低于图卢姆，但片区标准与海洋环境做法令其高于坎昆平均水平。')]},
}

LINKS3 = {
 'es': {'tankah': [('/construccion-de-casas-bahia-soliman/','Construcción de casas en Bahía Solimán'), ('/construccion-de-casas-tulum/','Construcción de casas en Tulum'), ('/construccion-de-casas-akumal/','Construcción de casas en Akumal'), ('/calculadora/','Calculadora de costos')],
        'punta-brava': [('/constructora-puerto-morelos/','Constructora en Puerto Morelos'), ('/permisos-de-construccion-puerto-morelos/','Permisos de construcción en Puerto Morelos'), ('/construccion-de-casas-cancun/','Construcción de casas en Cancún'), ('/calculadora/','Calculadora de costos')],
        'riviera-cancun': [('/construccion-de-casas-cancun/','Construcción de casas en Cancún'), ('/construccion-de-casas-puerto-cancun/','Construcción de casas en Puerto Cancún'), ('/constructora-puerto-morelos/','Constructora en Puerto Morelos'), ('/calculadora/','Calculadora de costos')]},
 'en': {'tankah': [('/house-construction-bahia-soliman/','House construction in Soliman Bay'), ('/house-construction-tulum/','House construction in Tulum'), ('/house-construction-akumal/','House construction in Akumal'), ('/calculator/','Cost calculator')],
        'punta-brava': [('/construction-company-puerto-morelos/','Construction company in Puerto Morelos'), ('/construction-permits-puerto-morelos/','Construction permits in Puerto Morelos'), ('/house-construction-cancun/','House construction in Cancún'), ('/calculator/','Cost calculator')],
        'riviera-cancun': [('/house-construction-cancun/','House construction in Cancún'), ('/house-construction-puerto-cancun/','House construction in Puerto Cancún'), ('/construction-company-puerto-morelos/','Construction company in Puerto Morelos'), ('/calculator/','Cost calculator')]},
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
    LINKS3[_lang] = {}
    for _z, _d in ZONE3.items():
        LINKS3[_lang][_z] = [
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
    _set_parent_urls(ZONE3)
    for z in ZONE3:
        z1.ZAREA[z] = AREAS[z]
        z1.ZTEXT[z] = TEXT[z]
        z1.ZFAQ[z] = FAQ3[z]
    for lang in LINKS3:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS3[lang])
    for z, d in ZONE3.items():
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
        for lang, txt in NORM_OVR.get(z, {}).items():
            ml.NORM[lang][z] = txt
        for lang, txt in SOIL_OVR.get(z, {}).items():
            ml.SOIL[lang][z] = txt
    ml.LOCS.extend(ZONE3)
    for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
        ch = ml.chrome(lang)
        for z in ZONE3:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-44s %6d bytes' % (out + '/', len(html)))
