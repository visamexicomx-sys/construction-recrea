#!/usr/bin/env python3
"""Fifth zone batch (2026-08-10): Región 15, Punta Bete, Punta Paraíso, Chan Chemuyil.

Chosen after checking the market rather than by filling the map:
  Región 15 (Tulum) — the fastest-growing part of Tulum, m² up >100% in 18 months,
    and the one place where the site already had a landing but no cluster page.
  Punta Bete / Xcalacoco (Solidaridad) — quiet beachfront 4 km north of Playa del
    Carmen, next to El Cielo, with the Azul Fives / Petit Lafitte hotel strip.
  Punta Paraíso / Paamul (Solidaridad) — gated coastal development 10 minutes south
    of Playa del Carmen with beach club, lakes and eco park.
  Chan Chemuyil (Tulum municipality) — 37 km from Playa del Carmen, 5 km from the
    Xcacel turtle sanctuary; the affordable alternative to expensive beachfront.

Chan Chemuyil takes Playa del Carmen's price band (it is cheaper than Akumal) but
Tulum's municipal rules, because that is the municipality it actually belongs to.
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

ZONE5 = {
 'region-15-tulum': dict(parent='tulum',            f=1.05, perm='3–5'),
 'punta-bete':      dict(parent='playa-del-carmen', f=1.35, perm='2–4'),
 'punta-paraiso':   dict(parent='playa-del-carmen', f=1.28, perm='2–4'),
 'chan-chemuyil':   dict(parent='playa-del-carmen', f=1.10, perm='3–5'),
}

NAMES = {
 'region-15-tulum': {'es': 'Región 15, Tulum', 'en': 'Región 15, Tulum', 'ru': 'Регионе 15, Тулум',
                     'de': 'Región 15, Tulum', 'fr': 'Región 15, Tulum', 'zh': '图卢姆15区'},
 'punta-bete': {'es': 'Punta Bete', 'en': 'Punta Bete', 'ru': 'Пунта-Бете', 'de': 'Punta Bete',
                'fr': 'Punta Bete', 'zh': 'Punta Bete'},
 'punta-paraiso': {'es': 'Punta Paraíso', 'en': 'Punta Paraíso', 'ru': 'Пунта-Параисо',
                   'de': 'Punta Paraíso', 'fr': 'Punta Paraíso', 'zh': 'Punta Paraíso'},
 'chan-chemuyil': {'es': 'Chan Chemuyil', 'en': 'Chan Chemuyil', 'ru': 'Чан-Чемуйиль',
                   'de': 'Chan Chemuyil', 'fr': 'Chan Chemuyil', 'zh': 'Chan Chemuyil'},
}
AREAS = {
 'region-15-tulum': {'es': 'Región 15 y el eje de la avenida Kukulkán', 'en': 'Región 15 and the Kukulkán avenue corridor',
   'ru': 'Регионе 15 и вдоль авеню Кукулькан', 'de': 'Región 15 und der Achse der Avenida Kukulkán',
   'fr': 'Región 15 et l’axe de l’avenue Kukulkán', 'zh': '15区及 Kukulkán 大道沿线'},
 'punta-bete': {'es': 'Punta Bete, Xcalacoco y la costa al norte de Playa del Carmen',
   'en': 'Punta Bete, Xcalacoco and the coast north of Playa del Carmen',
   'ru': 'Пунта-Бете, Шкалакоко и побережье к северу от Плая-дель-Кармен',
   'de': 'Punta Bete, Xcalacoco und der Küste nördlich von Playa del Carmen',
   'fr': 'Punta Bete, Xcalacoco et la côte au nord de Playa del Carmen',
   'zh': 'Punta Bete、Xcalacoco 及普拉亚德尔卡门以北海岸'},
 'punta-paraiso': {'es': 'Punta Paraíso, Paamul y la costa al sur de Playa del Carmen',
   'en': 'Punta Paraíso, Paamul and the coast south of Playa del Carmen',
   'ru': 'Пунта-Параисо, Паамуле и побережье к югу от Плая-дель-Кармен',
   'de': 'Punta Paraíso, Paamul und der Küste südlich von Playa del Carmen',
   'fr': 'Punta Paraíso, Paamul et la côte au sud de Playa del Carmen',
   'zh': 'Punta Paraíso、Paamul 及普拉亚德尔卡门以南海岸'},
 'chan-chemuyil': {'es': 'Chan Chemuyil, Chemuyil y la zona de Xcacel',
   'en': 'Chan Chemuyil, Chemuyil and the Xcacel area',
   'ru': 'Чан-Чемуйиле, Чемуйиле и районе Шкасель',
   'de': 'Chan Chemuyil, Chemuyil und der Gegend von Xcacel',
   'fr': 'Chan Chemuyil, Chemuyil et le secteur de Xcacel',
   'zh': 'Chan Chemuyil、Chemuyil 与 Xcacel 一带'},
}

TEXT = {
'region-15-tulum': {
 'es': 'Región 15 es la zona que más rápido crece en Tulum: el precio por m² se ha más que duplicado en año y medio y el eje de la avenida Kukulkán sigue empujando. A diez minutos de la playa y de la zona arqueológica, es hoy la mejor relación entre precio de entrada y plusvalía de la ciudad, con la contraparte habitual de una zona joven: hay que verificar servicios y situación legal calle por calle antes de comprar.',
 'en': 'Región 15 is the fastest-growing part of Tulum: the price per m² has more than doubled in a year and a half and the Kukulkán avenue corridor keeps pushing it. Ten minutes from the beach and the archaeological zone, it is currently the city’s best balance of entry price and appreciation — with the usual caveat of a young area: services and legal status have to be checked street by street before buying.',
 'ru': 'Регион 15 — самый быстрорастущий район Тулума: цена за м² выросла более чем вдвое за полтора года, и ось авеню Кукулькан продолжает тянуть её вверх. В десяти минутах от пляжа и археологической зоны это сегодня лучшее в городе соотношение цены входа и роста стоимости — с обычной оговоркой молодого района: коммуникации и юридический статус нужно проверять по каждой улице до покупки.',
 'de': 'Región 15 ist der am schnellsten wachsende Teil Tulums: Der m²-Preis hat sich in anderthalb Jahren mehr als verdoppelt, und die Achse der Avenida Kukulkán treibt weiter. Zehn Minuten von Strand und Ausgrabungsstätte entfernt ist es derzeit das beste Verhältnis von Einstiegspreis und Wertsteigerung der Stadt — mit dem üblichen Vorbehalt eines jungen Viertels: Versorgung und Rechtslage müssen vor dem Kauf Straße für Straße geprüft werden.',
 'fr': 'Región 15 est le secteur de Tulum qui croît le plus vite : le prix au m² a plus que doublé en un an et demi et l’axe de l’avenue Kukulkán continue de tirer. À dix minutes de la plage et du site archéologique, c’est aujourd’hui le meilleur rapport prix d’entrée / plus-value de la ville — avec la réserve habituelle d’un quartier jeune : réseaux et situation juridique se vérifient rue par rue avant l’achat.',
 'zh': '15区是图卢姆增长最快的片区：每平方米价格在一年半内翻了一倍以上，Kukulkán 大道沿线仍在持续拉动。距海滩与考古区仅十分钟，是目前全城入手价与增值潜力平衡得最好的区域——同时也带着新兴片区的老问题：购地前必须逐街核查市政配套与法律状态。'},
'punta-bete': {
 'es': 'Punta Bete y Xcalacoco son la costa tranquila a cuatro kilómetros al norte de Playa del Carmen: playa abierta, poca densidad y una franja hotelera pequeña, a minutos del centro pero sin su ruido. Es de los pocos puntos cercanos donde todavía se construye casa frente al mar; en predios de playa aplica concesión ZOFEMAT y el proyecto se hace con especificación marina completa.',
 'en': 'Punta Bete and Xcalacoco are the quiet coast four kilometres north of Playa del Carmen: open beach, low density and a small hotel strip, minutes from downtown but without its noise. It is one of the few nearby spots where a beachfront house is still being built; beach lots require a ZOFEMAT concession and the design carries a full marine spec.',
 'ru': 'Пунта-Бете и Шкалакоко — спокойное побережье в четырёх километрах к северу от Плая-дель-Кармен: открытый пляж, низкая плотность и небольшая отельная полоса, в минутах от центра, но без его шума. Одна из немногих ближних точек, где ещё строят дом на первой линии; на пляжных участках нужна концессия ZOFEMAT, а проект делается с полной морской спецификацией.',
 'de': 'Punta Bete und Xcalacoco sind die ruhige Küste vier Kilometer nördlich von Playa del Carmen: offener Strand, geringe Dichte und ein kleiner Hotelstreifen, Minuten vom Zentrum, aber ohne dessen Lärm. Einer der wenigen nahen Orte, an denen noch ein Strandhaus gebaut wird; Strandgrundstücke brauchen eine ZOFEMAT-Konzession, und geplant wird mit voller Meeresspezifikation.',
 'fr': 'Punta Bete et Xcalacoco forment la côte tranquille à quatre kilomètres au nord de Playa del Carmen : plage ouverte, faible densité et une petite bande hôtelière, à quelques minutes du centre mais sans son bruit. C’est l’un des rares endroits proches où l’on construit encore une maison en front de mer ; les lots de plage exigent une concession ZOFEMAT et le projet se fait en spécification marine complète.',
 'zh': 'Punta Bete 与 Xcalacoco 是普拉亚德尔卡门以北四公里的宁静海岸：海滩开阔、密度低、酒店带规模小，距市中心仅数分钟却没有喧嚣。这是附近少数仍可建造海滨住宅的地点之一；海滩地块需 ZOFEMAT 特许，设计须采用完整的海洋环境标准。'},
'punta-paraiso': {
 'es': 'Punta Paraíso, junto a Paamul, es un desarrollo cerrado sobre la costa a diez minutos al sur de Playa del Carmen, con club de playa, lagos y parque ecológico dentro del propio predio. El producto es la casa de baja densidad con acceso privado al mar; el reglamento del desarrollo define alturas, imagen y áreas verdes antes de que el expediente llegue al municipio.',
 'en': 'Punta Paraíso, next to Paamul, is a gated coastal development ten minutes south of Playa del Carmen, with a beach club, lakes and an eco park inside the estate itself. The product is a low-density house with private sea access; the development’s rules set heights, façade image and green areas before the file reaches the municipality.',
 'ru': 'Пунта-Параисо рядом с Паамулем — закрытая прибрежная застройка в десяти минутах к югу от Плая-дель-Кармен, с бич-клубом, озёрами и эко-парком на своей территории. Продукт — дом низкой плотности с приватным выходом к морю; регламент застройки задаёт высоты, облик и зелёные зоны ещё до того, как пакет уйдёт в муниципалитет.',
 'de': 'Punta Paraíso neben Paamul ist eine geschlossene Küstenanlage zehn Minuten südlich von Playa del Carmen, mit Beachclub, Seen und Ökopark auf dem eigenen Gelände. Das Produkt ist ein Haus geringer Dichte mit privatem Meerzugang; die Anlagensatzung legt Höhen, Fassadenbild und Grünflächen fest, bevor die Akte zur Gemeinde geht.',
 'fr': 'Punta Paraíso, voisin de Paamul, est un développement côtier fermé à dix minutes au sud de Playa del Carmen, avec beach club, lacs et parc écologique dans l’enceinte même. Le produit est la maison de faible densité avec accès privé à la mer ; le règlement du développement fixe hauteurs, image de façade et espaces verts avant que le dossier n’arrive en mairie.',
 'zh': 'Punta Paraíso 毗邻 Paamul，是普拉亚德尔卡门以南十分钟车程的封闭式滨海开发区，园区内自带海滩俱乐部、湖泊与生态公园。产品定位是低密度住宅并享有私人入海通道；社区规约在材料递交市政之前，就已确定高度、立面风貌与绿地要求。'},
'chan-chemuyil': {
 'es': 'Chan Chemuyil está a 37 km de Playa del Carmen y 13 de Tulum, a cinco kilómetros de Xcacel, santuario de tortuga marina. Es la alternativa razonable al frente de mar caro: terreno accesible, comunidad consolidada de expatriados y servicios urbanizados, a diez minutos de playas que no tienen cobro ni multitud. Municipio Tulum, así que la ruta ambiental es la de Tulum, no la de Solidaridad.',
 'en': 'Chan Chemuyil sits 37 km from Playa del Carmen and 13 from Tulum, five kilometres from Xcacel, a sea-turtle sanctuary. It is the sensible alternative to expensive beachfront: accessible land, an established expat community and urbanised services, ten minutes from beaches with no gate fee and no crowd. Tulum municipality, so the environmental route is Tulum’s, not Solidaridad’s.',
 'ru': 'Чан-Чемуйиль — в 37 км от Плая-дель-Кармен и 13 от Тулума, в пяти километрах от Шкаселя, заповедника морских черепах. Это разумная альтернатива дорогой первой линии: доступная земля, сложившееся сообщество экспатов и городские коммуникации, в десяти минутах от пляжей без платы за вход и без толп. Муниципалитет Тулум, поэтому экологический маршрут — тулумский, а не Solidaridad.',
 'de': 'Chan Chemuyil liegt 37 km von Playa del Carmen und 13 von Tulum entfernt, fünf Kilometer von Xcacel, einem Schildkrötenschutzgebiet. Die vernünftige Alternative zur teuren Strandlage: bezahlbares Land, eine etablierte Expat-Gemeinde und erschlossene Versorgung, zehn Minuten von Stränden ohne Eintritt und ohne Gedränge. Gemeinde Tulum — der Umweltweg ist also der von Tulum, nicht der von Solidaridad.',
 'fr': 'Chan Chemuyil se trouve à 37 km de Playa del Carmen et 13 de Tulum, à cinq kilomètres de Xcacel, sanctuaire de tortues marines. C’est l’alternative raisonnable au front de mer coûteux : foncier accessible, communauté d’expatriés établie et réseaux viabilisés, à dix minutes de plages sans péage ni foule. Commune de Tulum : le parcours environnemental est donc celui de Tulum, pas celui de Solidaridad.',
 'zh': 'Chan Chemuyil 距普拉亚德尔卡门37公里、距图卢姆13公里，距海龟保护区 Xcacel 仅五公里。它是昂贵海滨地段的务实替代：地价친民、外籍居民社区成熟、市政配套完善，距免门票且不拥挤的海滩仅十分钟。属图卢姆市辖，因此环保流程走图卢姆而非 Solidaridad。'},
}

# Chan Chemuyil borrows Playa del Carmen's price band but belongs to Tulum municipality
NORM_FROM = {'chan-chemuyil': 'tulum'}

FAQ = {
'region-15-tulum': {
 'es': [('¿Por qué construir en Región 15?', 'Precio de entrada más bajo que Aldea Zamá o La Veleta con la plusvalía más rápida de Tulum. A cambio hay que revisar antes agua, CFE, acceso y situación legal del predio: en zona joven cambia de manzana en manzana.'),
        ('¿Aplica SEMA en Región 15?', 'En la mayoría de los predios sí, además del uso de suelo y la licencia municipal de Tulum con DRO. Presupueste de 3 a 5 meses de permisos y arranque el trámite con el anteproyecto.')],
 'en': [('Why build in Región 15?', 'A lower entry price than Aldea Zamá or La Veleta with the fastest appreciation in Tulum. In exchange you must first check water, CFE, access and the lot’s legal status: in a young area it changes block by block.'),
        ('Does SEMA apply in Región 15?', 'On most lots yes, on top of land use and the Tulum municipal licence with a DRO. Budget 3 to 5 months of permits and start the process with the concept design.')],
 'ru': [('Почему строить в Регионе 15?', 'Цена входа ниже, чем в Альдеа-Зама или Ла-Велете, при самом быстром росте стоимости в Тулуме. Взамен нужно заранее проверить воду, CFE, подъезд и юридический статус участка: в молодом районе это меняется от квартала к кварталу.'),
        ('Действует ли SEMA в Регионе 15?', 'На большинстве участков да, вдобавок к назначению земли и муниципальной лицензии Тулума с DRO. Закладывайте 3–5 месяцев на разрешения и запускайте процедуру вместе с эскизом.')],
 'de': [('Warum in Región 15 bauen?', 'Niedrigerer Einstiegspreis als Aldea Zamá oder La Veleta bei der schnellsten Wertsteigerung Tulums. Dafür sind Wasser, CFE, Zufahrt und Rechtslage vorab zu prüfen: In einem jungen Viertel ändert sich das von Block zu Block.'),
        ('Gilt die SEMA in Región 15?', 'Auf den meisten Grundstücken ja, zusätzlich zu Nutzungsart und kommunaler Lizenz von Tulum mit DRO. Kalkulieren Sie 3 bis 5 Monate Genehmigungen und starten Sie mit dem Entwurf.')],
 'fr': [('Pourquoi construire en Región 15 ?', 'Un prix d’entrée plus bas qu’Aldea Zamá ou La Veleta avec la plus forte plus-value de Tulum. En contrepartie, il faut vérifier au préalable l’eau, la CFE, l’accès et la situation juridique : dans un quartier jeune, cela change d’un îlot à l’autre.'),
        ('La SEMA s’applique-t-elle en Región 15 ?', 'Sur la plupart des lots oui, en plus de l’usage du sol et du permis municipal de Tulum avec DRO. Comptez 3 à 5 mois de permis et lancez la procédure dès l’avant-projet.')],
 'zh': [('为什么选择在15区建房？', '入手价低于 Aldea Zamá 与 La Veleta，而增值速度是图卢姆最快的。代价是须提前核查供水、CFE 供电、道路接入与地块法律状态：新兴片区这些逐街区不同。'),
        ('15区需要办 SEMA 吗？', '多数地块需要，此外还需土地用途与带 DRO 的图卢姆市政许可。许可周期请预留3至5个月，并在方案阶段即启动。')]},
'punta-bete': {
 'es': [('¿Se puede construir frente al mar en Punta Bete?', 'Sí, en los predios que lo permiten: licencia municipal de Solidaridad con DRO, concesión ZOFEMAT en frente de playa y autorización ambiental por duna y vegetación costera. Verificamos el uso de suelo antes de que usted compre.'),
        ('¿Qué diferencia a Punta Bete de Playa del Carmen?', 'Densidad. Aquí hay playa abierta y pocos vecinos a cuatro kilómetros del centro; se gana silencio y frente de mar, se pierde el caminar a la Quinta Avenida.')],
 'en': [('Can you build beachfront at Punta Bete?', 'Yes, on the lots that allow it: Solidaridad municipal licence with a DRO, a ZOFEMAT concession on the beachfront and environmental authorisation for the dune and coastal vegetation. We verify land use before you buy.'),
        ('What sets Punta Bete apart from Playa del Carmen?', 'Density. Here you get open beach and few neighbours four kilometres from downtown; you gain quiet and beachfront, you lose walking to Quinta Avenida.')],
 'ru': [('Можно ли строить на первой линии в Пунта-Бете?', 'Да, на участках, где это допускается: муниципальная лицензия Solidaridad с DRO, концессия ZOFEMAT на берегу и экологическое разрешение из-за дюны и прибрежной растительности. Назначение земли проверяем до покупки.'),
        ('Чем Пунта-Бете отличается от Плая-дель-Кармен?', 'Плотностью. Здесь открытый пляж и мало соседей в четырёх километрах от центра: выигрываете тишину и первую линию, теряете пешую доступность Пятой авеню.')],
 'de': [('Kann man in Punta Bete am Strand bauen?', 'Ja, auf den Grundstücken, die es zulassen: kommunale Lizenz von Solidaridad mit DRO, ZOFEMAT-Konzession am Strand und Umweltgenehmigung wegen Düne und Küstenvegetation. Die Nutzungsart prüfen wir vor dem Kauf.'),
        ('Was unterscheidet Punta Bete von Playa del Carmen?', 'Die Dichte. Hier gibt es offenen Strand und wenige Nachbarn, vier Kilometer vom Zentrum: Man gewinnt Ruhe und Strandlage, verliert den Fußweg zur Quinta Avenida.')],
 'fr': [('Peut-on construire en front de mer à Punta Bete ?', 'Oui, sur les lots qui l’autorisent : permis municipal de Solidaridad avec DRO, concession ZOFEMAT en front de plage et autorisation environnementale pour la dune et la végétation côtière. Nous vérifions l’usage du sol avant l’achat.'),
        ('Qu’est-ce qui distingue Punta Bete de Playa del Carmen ?', 'La densité. Ici, plage ouverte et peu de voisins à quatre kilomètres du centre : on gagne le calme et le front de mer, on perd l’accès à pied à la Quinta Avenida.')],
 'zh': [('在 Punta Bete 可以建海滨住宅吗？', '可以，在允许的地块上：带 DRO 的 Solidaridad 市政许可、海滨 ZOFEMAT 特许，以及因沙丘与海岸植被而需的环保许可。我们会在您购地前核实土地用途。'),
        ('Punta Bete 与普拉亚德尔卡门有何不同？', '差别在密度。这里是开阔海滩、邻居稀少，距市中心四公里：换来的是安静与临海，失去的是步行前往第五大道的便利。')]},
'punta-paraiso': {
 'es': [('¿Qué reglas rigen en Punta Paraíso?', 'Las del desarrollo primero —volumetría, alturas, imagen y áreas verdes— y después la licencia municipal de Solidaridad con DRO. Presentamos ambos expedientes en paralelo para no perder semanas.'),
        ('¿Conviene para renta o para vivir?', 'El entorno cerrado con club de playa y baja densidad funciona muy bien para estancias largas y vivienda permanente; para renta diaria conviene revisar antes el reglamento interno del desarrollo.')],
 'en': [('What rules apply at Punta Paraíso?', 'The development’s first — massing, heights, façade image and green areas — then the Solidaridad municipal licence with a DRO. We file both in parallel so no weeks are lost.'),
        ('Better for rental or for living?', 'The gated setting with a beach club and low density works very well for long stays and permanent living; for daily rental, check the estate’s internal rules first.')],
 'ru': [('Какие правила действуют в Пунта-Параисо?', 'Сначала правила застройки — объём, высоты, облик и зелёные зоны, — затем муниципальная лицензия Solidaridad с DRO. Оба пакета подаём параллельно, чтобы не терять недели.'),
        ('Лучше под аренду или для жизни?', 'Закрытая среда с бич-клубом и низкой плотностью отлично работает для длительных заездов и постоянного проживания; для посуточной аренды сначала стоит проверить внутренний регламент.')],
 'de': [('Welche Regeln gelten in Punta Paraíso?', 'Zuerst die der Anlage — Baukörper, Höhen, Fassadenbild und Grünflächen —, dann die kommunale Lizenz von Solidaridad mit DRO. Wir reichen beides parallel ein, damit keine Wochen verloren gehen.'),
        ('Eher zur Vermietung oder zum Wohnen?', 'Das geschlossene Umfeld mit Beachclub und geringer Dichte eignet sich sehr gut für Langzeitaufenthalte und dauerhaftes Wohnen; für Kurzzeitvermietung zuerst die interne Satzung prüfen.')],
 'fr': [('Quelles règles s’appliquent à Punta Paraíso ?', 'Celles du développement d’abord — volumétrie, hauteurs, image de façade et espaces verts — puis le permis municipal de Solidaridad avec DRO. Nous déposons les deux en parallèle pour ne pas perdre de semaines.'),
        ('Plutôt pour louer ou pour habiter ?', 'Le cadre fermé avec beach club et faible densité convient très bien aux longs séjours et à la résidence permanente ; pour la location quotidienne, vérifiez d’abord le règlement intérieur.')],
 'zh': [('Punta Paraíso 适用哪些规则？', '先是社区规约——体量、高度、立面风貌与绿地，随后是带 DRO 的 Solidaridad 市政许可。两套材料并行报审，避免浪费数周时间。'),
        ('更适合出租还是自住？', '带海滩俱乐部的低密度封闭环境非常适合长住与长期居住；若打算按天出租，请先核查社区内部规约。')]},
'chan-chemuyil': {
 'es': [('¿Por qué Chan Chemuyil y no la playa cara?', 'Porque el terreno cuesta una fracción y las playas —Xcacel, Chemuyil— quedan a diez minutos. Se cambia el frente de mar por presupuesto de obra y por una comunidad ya hecha, con servicios urbanizados.'),
        ('¿Qué municipio y qué permisos aplican?', 'Municipio Tulum: uso de suelo y licencia con DRO ahí, y autorización ambiental de SEMA en la mayoría de los predios. La cercanía del santuario de tortuga de Xcacel exige cuidado con iluminación y descargas.')],
 'en': [('Why Chan Chemuyil instead of expensive beachfront?', 'Because land costs a fraction and the beaches — Xcacel, Chemuyil — are ten minutes away. You trade the beachfront for construction budget and for a community that already exists, with urbanised services.'),
        ('Which municipality and permits apply?', 'Tulum municipality: land use and the licence with a DRO there, plus SEMA environmental authorisation on most lots. Proximity to the Xcacel turtle sanctuary demands care with lighting and discharges.')],
 'ru': [('Почему Чан-Чемуйиль, а не дорогой берег?', 'Потому что земля стоит долю от берега, а пляжи — Шкасель, Чемуйиль — в десяти минутах. Первая линия меняется на бюджет стройки и на уже сложившееся сообщество с городскими коммуникациями.'),
        ('Какой муниципалитет и какие разрешения?', 'Муниципалитет Тулум: назначение земли и лицензия с DRO там, плюс экологическое разрешение SEMA на большинстве участков. Близость черепашьего заповедника Шкасель требует аккуратности с освещением и сбросами.')],
 'de': [('Warum Chan Chemuyil statt teurer Strandlage?', 'Weil das Grundstück einen Bruchteil kostet und die Strände — Xcacel, Chemuyil — zehn Minuten entfernt sind. Man tauscht die Strandlage gegen Baubudget und eine bereits bestehende Gemeinde mit erschlossener Versorgung.'),
        ('Welche Gemeinde und welche Genehmigungen gelten?', 'Gemeinde Tulum: Nutzungsart und Lizenz mit DRO dort, dazu SEMA-Umweltgenehmigung auf den meisten Grundstücken. Die Nähe zum Schildkrötenschutzgebiet Xcacel verlangt Sorgfalt bei Beleuchtung und Einleitungen.')],
 'fr': [('Pourquoi Chan Chemuyil plutôt que le front de mer cher ?', 'Parce que le terrain coûte une fraction et que les plages — Xcacel, Chemuyil — sont à dix minutes. On échange le front de mer contre du budget de chantier et une communauté déjà constituée, avec des réseaux viabilisés.'),
        ('Quelle commune et quels permis ?', 'Commune de Tulum : usage du sol et permis avec DRO sur place, plus l’autorisation environnementale de la SEMA sur la plupart des lots. La proximité du sanctuaire de tortues de Xcacel impose de la prudence sur l’éclairage et les rejets.')],
 'zh': [('为什么选 Chan Chemuyil 而不是昂贵海滨？', '因为地价只是海滨的一小部分，而 Xcacel、Chemuyil 等海滩仅十分钟车程。以放弃临海换取施工预算，以及一个配套完善、已然成型的社区。'),
        ('归属哪个市政、需要哪些许可？', '属图卢姆市：土地用途与带 DRO 的许可在该市办理，多数地块还需 SEMA 环保许可。毗邻 Xcacel 海龟保护区，因此在照明与排放方面须格外谨慎。')]},
}

LINKS = {
 'es': {'region-15-tulum': [('/constructora-region-15-tulum/', 'Constructora en Región 15'), ('/construccion-de-casas-tulum/', 'Construcción de casas en Tulum'), ('/construccion-de-casas-la-veleta/', 'Construcción de casas en La Veleta'), ('/calculadora/', 'Calculadora de costos')],
        'punta-bete': [('/construccion-de-casas-playa-del-carmen/', 'Construcción de casas en Playa del Carmen'), ('/construccion-de-casas-el-cielo-playa-del-carmen/', 'Construcción de casas en El Cielo'), ('/villas-de-lujo-playa-del-carmen/', 'Villas de lujo'), ('/calculadora/', 'Calculadora de costos')],
        'punta-paraiso': [('/construccion-de-casas-playa-del-carmen/', 'Construcción de casas en Playa del Carmen'), ('/construccion-de-casas-puerto-aventuras/', 'Construcción de casas en Puerto Aventuras'), ('/villas-de-lujo-playa-del-carmen/', 'Villas de lujo'), ('/calculadora/', 'Calculadora de costos')],
        'chan-chemuyil': [('/construccion-de-casas-akumal/', 'Construcción de casas en Akumal'), ('/construccion-de-casas-tulum/', 'Construcción de casas en Tulum'), ('/constructora-akumal/', 'Constructora en Akumal'), ('/calculadora/', 'Calculadora de costos')]},
 'en': {'region-15-tulum': [('/builder-region-15-tulum/', 'Builder in Región 15'), ('/house-construction-tulum/', 'House construction in Tulum'), ('/house-construction-la-veleta/', 'House construction in La Veleta'), ('/calculator/', 'Cost calculator')],
        'punta-bete': [('/house-construction-playa-del-carmen/', 'House construction in Playa del Carmen'), ('/house-construction-el-cielo-playa-del-carmen/', 'House construction in El Cielo'), ('/luxury-villa-construction-playa-del-carmen/', 'Luxury villas'), ('/calculator/', 'Cost calculator')],
        'punta-paraiso': [('/house-construction-playa-del-carmen/', 'House construction in Playa del Carmen'), ('/house-construction-puerto-aventuras/', 'House construction in Puerto Aventuras'), ('/luxury-villa-construction-playa-del-carmen/', 'Luxury villas'), ('/calculator/', 'Cost calculator')],
        'chan-chemuyil': [('/house-construction-akumal/', 'House construction in Akumal'), ('/house-construction-tulum/', 'House construction in Tulum'), ('/construction-company-akumal/', 'Construction company in Akumal'), ('/calculator/', 'Cost calculator')]},
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
    for _z, _d in ZONE5.items():
        LINKS[_lang][_z] = [('/%s-%s/' % (_pref, _d['parent']), '%s — %s' % (hub, ml.CITY[_lang][_d['parent']])),
                            perm, ('/%s-riviera-maya/' % _pref, '%s — %s' % (hub, ml.CITY[_lang]['riviera-maya'])),
                            (_calc, names[0]), (_blog, names[1])]


def _set_parent_urls(locs):
    P = {'es': 'construccion-de-casas', 'en': 'house-construction', 'ru': 'stroitelstvo-domov',
         'de': 'hausbau', 'fr': 'construction-de-maisons', 'zh': 'zhuzhai-jianzao'}
    ml.OVR.setdefault('parent_url', {})
    for zk, d in locs.items():
        for l in LANGS:
            ml.OVR['parent_url'].setdefault(zk, {})[l] = '/%s-%s/' % (P[l], d['parent'])


if __name__ == '__main__':
    _set_parent_urls(ZONE5)
    for z in ZONE5:
        z1.ZAREA[z] = AREAS[z]; z1.ZTEXT[z] = TEXT[z]; z1.ZFAQ[z] = FAQ[z]
    for lang in LINKS:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS[lang])
    for z, d in ZONE5.items():
        for lang in LANGS:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
        src = NORM_FROM.get(z)
        if src:
            for lang in LANGS:
                if lang == 'es':   # ES town rules live in the ES generator, not in ml.NORM
                    ml.NORM['es'][z] = z1.esg.CITIES[src]['norm']
                    ml.SOIL['es'][z] = z1.esg.CITIES[src]['soil']
                else:
                    ml.NORM[lang][z] = ml.NORM[lang][src]
                    ml.SOIL[lang][z] = ml.SOIL[lang][src]
    ml.LOCS.extend(ZONE5)
    for lang in LANGS:
        ch = ml.chrome(lang)
        for z in ZONE5:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-44s %6d bytes' % (out + '/', len(html)))
