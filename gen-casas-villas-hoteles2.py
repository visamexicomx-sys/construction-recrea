#!/usr/bin/env python3
"""Villa + boutique-hotel pages for Puerto Aventuras, Akumal and Puerto Morelos.

Second batch of the villa/hotel format (2026-08-09). Two notes:

- Puerto Aventuras and Akumal already have a house-construction town page, so their
  villa m² band is taken from it unchanged (f = 1.0) — no self-contradiction.
- Puerto Morelos has NO town page in this cluster, so its villa band is derived from
  Playa del Carmen at f = 1.0 (the factor the earlier city-cost cluster used for
  Puerto Morelos) and it links to /constructora-puerto-morelos/ instead. `town=None`
  keeps the linker from attaching it to the wrong town page.
"""
import importlib.util, os, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
vh1 = load('gen-casas-villas-hoteles.py', 'vh1')
il = vh1.il
z1 = vh1.z1
ml = vh1.ml

CITIES = {
 'vh-puerto-aventuras': dict(parent='puerto-aventuras', f=1.0, perm='2–4', town='puerto-aventuras'),
 'vh-akumal':           dict(parent='akumal',           f=1.0, perm='3–5', town='akumal'),
 'vh-puerto-morelos':   dict(parent='playa-del-carmen', f=1.0, perm='3–5', town=None),
}
BASE_SLUG = {'vh-puerto-aventuras': 'puerto-aventuras', 'vh-akumal': 'akumal', 'vh-puerto-morelos': 'puerto-morelos'}
SLUG_PREFIX = vh1.SLUG_PREFIX

NAMES = {
 'vh-puerto-aventuras': {'es': 'Puerto Aventuras', 'en': 'Puerto Aventuras', 'ru': 'Пуэрто-Авентурас',
                         'de': 'Puerto Aventuras', 'fr': 'Puerto Aventuras', 'zh': 'Puerto Aventuras'},
 'vh-akumal': {'es': 'Akumal', 'en': 'Akumal', 'ru': 'Акумале', 'de': 'Akumal', 'fr': 'Akumal', 'zh': 'Akumal'},
 'vh-puerto-morelos': {'es': 'Puerto Morelos', 'en': 'Puerto Morelos', 'ru': 'Пуэрто-Морелосе',
                       'de': 'Puerto Morelos', 'fr': 'Puerto Morelos', 'zh': 'Puerto Morelos'},
}
AREAS = {
 'vh-puerto-aventuras': {'es': 'la marina, Xcalacoco, Bahía Chemuyil y los fraccionamientos privados',
   'en': 'the marina, Xcalacoco, Bahía Chemuyil and the private phases',
   'ru': 'районе марины, Шкалакоко, Баия-Чемуйиль и частных секторах',
   'de': 'der Marina, Xcalacoco, Bahía Chemuyil und den privaten Abschnitten',
   'fr': 'la marina, Xcalacoco, Bahía Chemuyil et les tranches privées',
   'zh': '码头区、Xcalacoco、Bahía Chemuyil 与各私人区段'},
 'vh-akumal': {'es': 'Akumal Norte, Media Luna Bay, Jade Bay y Aventuras Akumal',
   'en': 'Akumal Norte, Media Luna Bay, Jade Bay and Aventuras Akumal',
   'ru': 'Акумаль-Норте, Медиа-Луна, Хейд-Бэй и Авентурас-Акумаль',
   'de': 'Akumal Norte, Media Luna Bay, Jade Bay und Aventuras Akumal',
   'fr': 'Akumal Norte, Media Luna Bay, Jade Bay et Aventuras Akumal',
   'zh': 'Akumal Norte、Media Luna Bay、Jade Bay 与 Aventuras Akumal'},
 'vh-puerto-morelos': {'es': 'el pueblo, la zona hotelera sur, Bahía Petempich y Punta Brava',
   'en': 'the town, the southern hotel strip, Bahía Petempich and Punta Brava',
   'ru': 'посёлке, южной отельной полосе, Баия-Петемпич и Пунта-Брава',
   'de': 'dem Ort, dem südlichen Hotelstreifen, Bahía Petempich und Punta Brava',
   'fr': 'le village, la bande hôtelière sud, Bahía Petempich et Punta Brava',
   'zh': '镇区、南部酒店带、Bahía Petempich 与 Punta Brava'},
}

# premium / standard / economy, USD per key
KEYS = {
 'vh-puerto-aventuras': ('$110,000 – $185,000', '$90,000 – $150,000', '$70,000 – $115,000'),
 'vh-akumal':           ('$120,000 – $195,000', '$95,000 – $160,000', '$75,000 – $120,000'),
 'vh-puerto-morelos':   ('$100,000 – $165,000', '$82,000 – $135,000', '$62,000 – $105,000'),
}

TEXT = {
'vh-puerto-aventuras': {
 'es': 'Puerto Aventuras es una comunidad cerrada con marina, golf y seguridad 24/7, y ese es exactamente su producto: villas de renta alta y hotelería pequeña o condo-hotel dentro del fraccionamiento. Aquí no se improvisa nada: el comité de diseño revisa alturas, fachadas y colores, y la administración controla accesos, horarios y proveedores en obra. A cambio, el huésped llega a un entorno cerrado con marina y playa, que es lo que sostiene la tarifa.',
 'en': 'Puerto Aventuras is a gated community with a marina, golf and 24/7 security, and that is exactly its product: high-yield rental villas and small hospitality or condo-hotel inside the estate. Nothing is improvised here: the design committee reviews heights, façades and colours, and the administration controls site access, hours and suppliers. In exchange, the guest arrives into a gated setting with marina and beach — which is what sustains the rate.',
 'ru': 'Пуэрто-Авентурас — закрытая община с мариной, гольфом и охраной 24/7, и это ровно её продукт: доходные виллы под аренду и небольшая гостиница или кондо-отель внутри посёлка. Здесь ничего не делается на ходу: комитет по дизайну проверяет высоты, фасады и цвета, а администрация контролирует доступ, часы работ и поставщиков. Взамен гость попадает в закрытую среду с мариной и пляжем — именно это держит тариф.',
 'de': 'Puerto Aventuras ist eine geschlossene Anlage mit Marina, Golf und 24/7-Sicherheit — und genau das ist ihr Produkt: renditestarke Mietvillen und kleine Hotellerie oder Condo-Hotel innerhalb der Anlage. Hier wird nichts improvisiert: Der Gestaltungsbeirat prüft Höhen, Fassaden und Farben, die Verwaltung steuert Zufahrt, Zeiten und Lieferanten. Dafür kommt der Gast in ein geschlossenes Umfeld mit Marina und Strand — das trägt die Rate.',
 'fr': 'Puerto Aventuras est une résidence fermée avec marina, golf et sécurité 24h/24, et c’est exactement son produit : villas locatives à fort rendement et petite hôtellerie ou condo-hôtel au sein de la résidence. Rien ne s’improvise ici : le comité d’architecture examine hauteurs, façades et couleurs, et l’administration contrôle accès, horaires et fournisseurs. En échange, le client arrive dans un cadre fermé avec marina et plage — c’est ce qui soutient le tarif.',
 'zh': 'Puerto Aventuras 是配有码头、高尔夫与24小时安保的封闭社区，而这正是它的产品定位：高收益出租别墅，以及社区内的小型酒店或产权式酒店。这里没有临场发挥的余地：设计委员会审核高度、立面与色彩，物业管理方管控出入、作业时段与进场供应商。作为回报，客人进入的是带码头与海滩的封闭环境——这正是房价的支撑。'},
'vh-akumal': {
 'es': 'Akumal es playa, arrecife y tortuga marina: villas frente al mar y hoteles pequeños de 8 a 15 llaves, con una demanda que paga por estar en la bahía y no por tener cien habitaciones. La contraparte es la normativa: municipio Tulum, SEMA en la mayoría de los predios, ZOFEMAT frente a playa y restricciones de iluminación y trabajos nocturnos en temporada de anidación. Se diseña con eso puesto en el programa, no como sorpresa.',
 'en': 'Akumal is beach, reef and sea turtles: beachfront villas and small hotels of 8 to 15 keys, with demand that pays to be on the bay rather than to have a hundred rooms. The flip side is the rulebook: Tulum municipality, SEMA on most lots, ZOFEMAT on the beachfront and restrictions on lighting and night work during nesting season. That goes into the brief from the start, not as a surprise.',
 'ru': 'Акумаль — это пляж, риф и морские черепахи: виллы на первой линии и небольшие отели на 8–15 номеров, где спрос платит за нахождение в бухте, а не за сто комнат. Обратная сторона — нормативка: муниципалитет Тулум, SEMA на большинстве участков, ZOFEMAT на берегу и ограничения по освещению и ночным работам в сезон гнездования. Это закладывается в задание сразу, а не всплывает по ходу.',
 'de': 'Akumal ist Strand, Riff und Meeresschildkröten: Strandvillen und kleine Hotels mit 8 bis 15 Zimmern, deren Nachfrage für die Lage an der Bucht zahlt und nicht für hundert Zimmer. Die Kehrseite ist das Regelwerk: Gemeinde Tulum, SEMA auf den meisten Grundstücken, ZOFEMAT am Strand sowie Auflagen zu Beleuchtung und Nachtarbeit in der Nistzeit. Das steht von Anfang an im Programm, nicht als Überraschung.',
 'fr': 'Akumal, c’est la plage, le récif et les tortues marines : villas en front de mer et petits hôtels de 8 à 15 clés, avec une demande qui paie pour être sur la baie et non pour cent chambres. La contrepartie, c’est la réglementation : commune de Tulum, SEMA sur la plupart des lots, ZOFEMAT en bord de plage et restrictions d’éclairage et de travaux nocturnes en saison de ponte. Cela entre dans le programme dès le départ, pas en cours de route.',
 'zh': 'Akumal 的核心是海滩、珊瑚礁与海龟：海滨别墅与8至15间客房的小型酒店，客群愿意为身处海湾而付费，而不是为上百间客房。另一面则是法规：属图卢姆市辖，多数地块需 SEMA 许可，海滨需 ZOFEMAT，产卵季对照明与夜间施工有限制。这些从任务书阶段就纳入考量，而不是中途才发现。'},
'vh-puerto-morelos': {
 'es': 'Puerto Morelos combina pueblo de pescadores, arrecife a pocos metros y una franja hotelera al sur, con precios de terreno todavía por debajo de Playa del Carmen y Tulum. Es el punto más razonable de la costa norte para una villa de renta o un hotel pequeño con concepto de buceo y naturaleza. Todo gira alrededor del Parque Nacional Arrecife: tratamiento de aguas obligatorio, control de escurrimientos y expediente ambiental cuidado.',
 'en': 'Puerto Morelos combines a fishing town, a reef a few metres offshore and a hotel strip to the south, with land prices still below Playa del Carmen and Tulum. It is the most reasonable point on the north coast for a rental villa or a small hotel built around diving and nature. Everything revolves around the Reef National Park: mandatory wastewater treatment, runoff control and a carefully handled environmental file.',
 'ru': 'Пуэрто-Морелос сочетает рыбацкий посёлок, риф в нескольких метрах от берега и отельную полосу южнее, при ценах на землю всё ещё ниже, чем в Плая-дель-Кармен и Тулуме. Это самая разумная точка северного побережья для виллы под аренду или небольшого отеля с концепцией дайвинга и природы. Всё вращается вокруг Национального парка «Риф»: обязательная очистка стоков, контроль поверхностного стока и аккуратное экологическое досье.',
 'de': 'Puerto Morelos verbindet Fischerort, ein Riff wenige Meter vor der Küste und einen Hotelstreifen im Süden — bei Grundstückspreisen, die noch unter Playa del Carmen und Tulum liegen. Der vernünftigste Punkt der Nordküste für eine Mietvilla oder ein kleines Hotel mit Tauch- und Naturkonzept. Alles dreht sich um den Riff-Nationalpark: verpflichtende Abwasserbehandlung, Abflusskontrolle und eine sorgfältig geführte Umweltakte.',
 'fr': 'Puerto Morelos associe village de pêcheurs, récif à quelques mètres du rivage et une bande hôtelière au sud, avec des prix du foncier encore inférieurs à Playa del Carmen et Tulum. C’est le point le plus raisonnable de la côte nord pour une villa locative ou un petit hôtel axé plongée et nature. Tout tourne autour du Parc National du Récif : traitement des eaux obligatoire, contrôle des ruissellements et dossier environnemental soigné.',
 'zh': 'Puerto Morelos 兼具渔村风貌、距岸仅数米的珊瑚礁与南侧的酒店带，而地价仍低于普拉亚德尔卡门与图卢姆。对于出租别墅或以潜水与自然为主题的小型酒店而言，这是北部海岸最务实的选择。一切都围绕珊瑚礁国家公园展开：污水处理为强制项，需控制地表径流，环保申报材料必须细致。'},
}

NORM = {
'vh-puerto-aventuras': {
 'es': 'La licencia se tramita en Solidaridad —uso de suelo conforme al PDU, proyecto firmado por DRO— pero el filtro real está adentro: la administración y el comité de diseño de Puerto Aventuras aprueban volumetría, fachada, colores y horarios de obra antes de que el expediente salga del fraccionamiento. Para operar como hotel o renta vacacional se suman uso de suelo con giro, licencia de funcionamiento, visto bueno de Protección Civil y registro turístico, además del reglamento interno de rentas.',
 'en': 'The licence is filed in Solidaridad — land use under the PDU, drawings signed by a DRO — but the real filter is inside: Puerto Aventuras’ administration and design committee approve massing, façade, colours and working hours before the file even leaves the estate. To operate as a hotel or vacation rental you add zoning for that use, the municipal operating licence, Civil Protection sign-off and tourism registration, plus the estate’s own rental by-laws.',
 'ru': 'Лицензия оформляется в Solidaridad — назначение земли по PDU, проект за подписью DRO, — но реальный фильтр внутри: администрация и комитет по дизайну Пуэрто-Авентурас утверждают объём, фасад, цвета и часы работ до того, как пакет уйдёт из посёлка. Для работы отелем или посуточной арендой добавляются назначение земли под этот профиль, лицензия на деятельность, заключение Гражданской защиты и туристическая регистрация, плюс внутренний регламент по аренде.',
 'de': 'Die Lizenz läuft über Solidaridad — Nutzungsart nach PDU, DRO-unterzeichnete Pläne —, der eigentliche Filter sitzt aber innen: Verwaltung und Gestaltungsbeirat von Puerto Aventuras genehmigen Baukörper, Fassade, Farben und Bauzeiten, bevor die Akte die Anlage verlässt. Für den Betrieb als Hotel oder Ferienvermietung kommen die entsprechende Nutzungsart, die Betriebslizenz, die Freigabe des Zivilschutzes und die Tourismusregistrierung hinzu — dazu die interne Vermietungssatzung.',
 'fr': 'Le permis se dépose à Solidaridad — usage du sol au titre du PDU, plans signés par un DRO — mais le vrai filtre est à l’intérieur : l’administration et le comité d’architecture de Puerto Aventuras valident volumétrie, façade, couleurs et horaires de chantier avant même que le dossier ne quitte la résidence. Pour exploiter en hôtel ou en location saisonnière s’ajoutent l’usage du sol correspondant, la licence d’exploitation, l’avis de la Protection Civile et l’enregistrement touristique, ainsi que le règlement interne de location.',
 'zh': '许可在 Solidaridad 市办理——依 PDU 取得土地用途、图纸由 DRO 签署——但真正的关卡在社区内部：Puerto Aventuras 的物业管理方与设计委员会须先批准体量、立面、色彩与施工时段，材料才会递出社区。若要作为酒店或度假出租经营，还需相应土地用途、经营许可、民防意见与旅游登记，以及社区内部的出租规约。'},
'vh-akumal': {
 'es': 'Akumal pertenece al municipio de Tulum: uso de suelo y licencia con DRO se tramitan ahí, y la mayoría de los predios requiere autorización ambiental de SEMA. Frente a playa entra la concesión ZOFEMAT, y por ser zona de anidación de tortuga hay condiciones de iluminación hacia el mar y de trabajos nocturnos entre mayo y octubre. Para hotel se añaden giro hotelero, licencia de funcionamiento, Protección Civil, capacidad eléctrica ante CFE y registro turístico; el drenaje se resuelve con planta o biodigestor, nunca con fosa.',
 'en': 'Akumal belongs to the municipality of Tulum: land use and the licence with a DRO are processed there, and most lots require SEMA environmental authorisation. Beachfront brings a ZOFEMAT concession, and being a turtle nesting area there are conditions on sea-facing lighting and night work between May and October. A hotel adds hotel-use zoning, the operating licence, Civil Protection, CFE capacity and tourism registration; drainage is solved with a plant or biodigester, never a septic pit.',
 'ru': 'Акумаль относится к муниципалитету Тулум: назначение земли и лицензия с DRO оформляются там, а большинству участков нужна экологическая авторизация SEMA. На первой линии добавляется концессия ZOFEMAT, а как зона гнездования черепах — условия по освещению в сторону моря и ночным работам с мая по октябрь. Для отеля добавляются гостиничный профиль, лицензия на деятельность, Гражданская защита, мощность в CFE и туристическая регистрация; канализация — очистные или биодигестер, никогда выгребная яма.',
 'de': 'Akumal gehört zur Gemeinde Tulum: Nutzungsart und Lizenz mit DRO laufen dort, und die meisten Grundstücke brauchen eine SEMA-Umweltgenehmigung. Am Strand kommt die ZOFEMAT-Konzession hinzu, und als Schildkröten-Nistgebiet gelten Auflagen für meerseitige Beleuchtung und Nachtarbeit zwischen Mai und Oktober. Für ein Hotel ergänzen sich Hotel-Nutzungsart, Betriebslizenz, Zivilschutz, CFE-Leistung und Tourismusregistrierung; die Entwässerung erfolgt über Anlage oder Biodigester, nie über eine Sickergrube.',
 'fr': 'Akumal relève de la commune de Tulum : usage du sol et permis avec DRO s’y traitent, et la plupart des lots exigent l’autorisation environnementale de la SEMA. En front de plage s’ajoute la concession ZOFEMAT et, zone de ponte oblige, des conditions sur l’éclairage côté mer et les travaux nocturnes de mai à octobre. Pour un hôtel s’ajoutent l’usage hôtelier, la licence d’exploitation, la Protection Civile, la puissance CFE et l’enregistrement touristique ; l’assainissement passe par station ou biodigesteur, jamais par une fosse.',
 'zh': 'Akumal 隶属图卢姆市：土地用途与带 DRO 的许可在该市办理，多数地块需 SEMA 环保许可。海滨地块需 ZOFEMAT 特许；作为海龟产卵区，5月至10月对朝海照明与夜间施工另有限制。酒店还需酒店类土地用途、经营许可、民防意见、CFE 用电容量与旅游登记；排水须采用处理设备或生物消化池，不得使用化粪坑。'},
'vh-puerto-morelos': {
 'es': 'Puerto Morelos es municipio propio desde 2016 y aplica criterios más estrictos que sus vecinos por el arrecife: ahí se tramitan uso de suelo y licencia de construcción con DRO. Frente al mar entra ZOFEMAT y, por la cercanía del Parque Nacional Arrecife y de los humedales, normalmente autorización ambiental con condiciones sobre desmonte, escurrimientos y aguas residuales. Para hotel se suman giro hotelero, licencia de funcionamiento, Protección Civil, capacidad eléctrica por aforo y registro turístico.',
 'en': 'Puerto Morelos has been its own municipality since 2016 and applies stricter criteria than its neighbours because of the reef: land use and the building licence with a DRO are processed there. Beachfront brings ZOFEMAT and, given the proximity of the Reef National Park and the wetlands, usually an environmental authorisation with conditions on clearing, runoff and wastewater. A hotel adds hotel-use zoning, the operating licence, Civil Protection, occupancy-based electrical capacity and tourism registration.',
 'ru': 'Пуэрто-Морелос — самостоятельный муниципалитет с 2016 года и применяет более строгие критерии, чем соседи, из-за рифа: там оформляются назначение земли и разрешение на строительство с DRO. На первой линии нужна ZOFEMAT, а из-за близости Национального парка «Риф» и водно-болотных угодий обычно и экологическое согласование с условиями по расчистке, стоку и сточным водам. Для отеля добавляются гостиничный профиль, лицензия на деятельность, Гражданская защита, мощность под вместимость и туристическая регистрация.',
 'de': 'Puerto Morelos ist seit 2016 eigene Gemeinde und wendet wegen des Riffs strengere Kriterien an als die Nachbarn: Nutzungsart und Baugenehmigung mit DRO laufen dort. Am Strand gilt ZOFEMAT, und wegen der Nähe zum Riff-Nationalpark und den Feuchtgebieten meist eine Umweltgenehmigung mit Auflagen zu Rodung, Abfluss und Abwasser. Für ein Hotel kommen Hotel-Nutzungsart, Betriebslizenz, Zivilschutz, belegungsabhängige Leistung und Tourismusregistrierung hinzu.',
 'fr': 'Puerto Morelos est commune à part entière depuis 2016 et applique des critères plus stricts que ses voisines à cause du récif : usage du sol et permis de construire avec DRO s’y traitent. En front de mer s’applique la ZOFEMAT et, vu la proximité du Parc National du Récif et des zones humides, généralement une autorisation environnementale assortie de conditions sur le défrichement, le ruissellement et les eaux usées. Pour un hôtel s’ajoutent l’usage hôtelier, la licence d’exploitation, la Protection Civile, la puissance selon capacité et l’enregistrement touristique.',
 'zh': 'Puerto Morelos 自2016年独立设市，并因珊瑚礁而采用比周边更严格的标准：土地用途与带 DRO 的施工许可在该市办理。海滨地块需 ZOFEMAT；鉴于紧邻珊瑚礁国家公园与湿地，通常还需环保许可，并对清林、径流与污水提出条件。酒店另需酒店类土地用途、经营许可、民防意见、按容量核定的用电容量与旅游登记。'},
}

FAQ = {
'vh-puerto-aventuras': {
 'es': [('¿Se puede operar renta vacacional u hotel dentro de Puerto Aventuras?', 'Sí, pero con doble regla: la licencia municipal de Solidaridad y el reglamento interno del fraccionamiento, que fija condiciones de renta, accesos y ruido. Lo revisamos antes de diseñar para que el proyecto encaje.'),
        ('¿Cuánto cuesta un hotel pequeño aquí?', 'De $70,000 a $185,000 USD por llave según nivel. En el fraccionamiento predominan formatos pequeños y condo-hotel, no volumen.')],
 'en': [('Can you run a vacation rental or hotel inside Puerto Aventuras?', 'Yes, but under two rulebooks: the Solidaridad municipal licence and the estate’s internal by-laws, which set rental conditions, access and noise. We check them before designing so the project fits.'),
        ('What does a small hotel cost here?', 'From $70,000 to $185,000 USD per key depending on level. The estate favours small formats and condo-hotel, not volume.')],
 'ru': [('Можно ли вести посуточную аренду или отель внутри Пуэрто-Авентурас?', 'Да, но по двум сводам правил: муниципальная лицензия Solidaridad и внутренний регламент посёлка, который задаёт условия аренды, доступ и шум. Проверяем их до проектирования, чтобы проект вписался.'),
        ('Сколько стоит небольшой отель здесь?', 'От $70,000 до $185,000 USD за номер в зависимости от уровня. В посёлке преобладают малые форматы и кондо-отель, а не объём.')],
 'de': [('Kann man in Puerto Aventuras Ferienvermietung oder Hotel betreiben?', 'Ja, aber nach zwei Regelwerken: kommunale Lizenz von Solidaridad und interne Satzung der Anlage, die Vermietung, Zufahrt und Lärm regelt. Wir prüfen sie vor dem Entwurf, damit das Projekt passt.'),
        ('Was kostet hier ein kleines Hotel?', 'Von $70.000 bis $185.000 USD pro Zimmer je nach Niveau. In der Anlage dominieren kleine Formate und Condo-Hotel, kein Volumen.')],
 'fr': [('Peut-on exploiter une location saisonnière ou un hôtel dans Puerto Aventuras ?', 'Oui, mais sous deux règlements : le permis municipal de Solidaridad et le règlement intérieur de la résidence, qui fixe conditions de location, accès et bruit. Nous les vérifions avant de concevoir pour que le projet s’y insère.'),
        ('Combien coûte un petit hôtel ici ?', 'De 70 000 à 185 000 USD par clé selon le niveau. La résidence privilégie les petits formats et le condo-hôtel, pas le volume.')],
 'zh': [('在 Puerto Aventuras 内可以做度假出租或酒店吗？', '可以，但要同时满足两套规则：Solidaridad 市政许可与社区内部规约（对出租条件、出入与噪音均有规定）。我们会在设计前先行核查，确保方案可落地。'),
        ('这里建小型酒店要多少钱？', '按档次每间客房 70,000 至 185,000 美元。社区内以小体量与产权式酒店为主，而非大规模开发。')]},
'vh-akumal': {
 'es': [('¿Qué tamaño de hotel funciona en Akumal?', 'De 8 a 15 llaves. La demanda paga por la bahía, el arrecife y la baja densidad; un formato grande choca con la normativa ambiental y con el propio producto.'),
        ('¿Las tortugas limitan la operación del hotel?', 'Sí, en temporada de anidación (mayo–octubre) hay condiciones de iluminación hacia la playa y de trabajos nocturnos. Se resuelve con proyecto de iluminación diseñado desde el inicio, no con parches.')],
 'en': [('What hotel size works in Akumal?', '8 to 15 keys. Demand pays for the bay, the reef and low density; a large format collides both with environmental rules and with the product itself.'),
        ('Do the turtles limit hotel operations?', 'Yes — during nesting season (May–October) there are conditions on beach-facing lighting and night work. It is solved with a lighting design done from the start, not with patches.')],
 'ru': [('Какой размер отеля работает в Акумале?', '8–15 номеров. Спрос платит за бухту, риф и низкую плотность; крупный формат конфликтует и с экологическими нормами, и с самим продуктом.'),
        ('Ограничивают ли черепахи работу отеля?', 'Да, в сезон гнездования (май–октябрь) действуют условия по освещению в сторону пляжа и ночным работам. Решается проектом освещения, заложенным с самого начала, а не заплатками.')],
 'de': [('Welche Hotelgröße funktioniert in Akumal?', '8 bis 15 Zimmer. Die Nachfrage zahlt für Bucht, Riff und geringe Dichte; ein großes Format kollidiert mit den Umweltauflagen und mit dem Produkt selbst.'),
        ('Schränken die Schildkröten den Hotelbetrieb ein?', 'Ja — in der Nistzeit (Mai–Oktober) gelten Auflagen für strandseitige Beleuchtung und Nachtarbeit. Gelöst wird das mit einem von Anfang an geplanten Lichtkonzept, nicht mit Nachbesserungen.')],
 'fr': [('Quelle taille d’hôtel fonctionne à Akumal ?', 'De 8 à 15 clés. La demande paie pour la baie, le récif et la faible densité ; un grand format se heurte à la réglementation environnementale comme au produit lui-même.'),
        ('Les tortues limitent-elles l’exploitation de l’hôtel ?', 'Oui : en saison de ponte (mai–octobre), l’éclairage côté plage et les travaux nocturnes sont encadrés. Cela se règle par un projet d’éclairage conçu dès le départ, pas par des rustines.')],
 'zh': [('在 Akumal 建多大规模的酒店合适？', '8至15间客房。客群为海湾、珊瑚礁与低密度买单；大体量既与环保法规冲突，也与产品本身相悖。'),
        ('海龟会限制酒店运营吗？', '会。产卵季（5月至10月）对朝向沙滩的照明与夜间作业有要求。解决办法是从设计之初就做好照明方案，而非事后修补。')]},
'vh-puerto-morelos': {
 'es': [('¿Por qué construir un hotel en Puerto Morelos y no en Cancún?', 'Por terreno más accesible, entorno de pueblo y arrecife a pocos metros: un concepto de buceo y naturaleza sostiene tarifa con menos llaves. La contraparte es la normativa ambiental, más estricta por el Parque Nacional.'),
        ('¿Qué exige el arrecife a un hotel?', 'Planta de tratamiento dimensionada al aforo, control de escurrimientos, manejo documentado de residuos y cuidado con la iluminación hacia la playa. Sin eso, el expediente no avanza.')],
 'en': [('Why build a hotel in Puerto Morelos rather than Cancún?', 'More accessible land, a village setting and a reef metres offshore: a diving-and-nature concept sustains the rate with fewer keys. The trade-off is stricter environmental rules because of the National Park.'),
        ('What does the reef require from a hotel?', 'A treatment plant sized to occupancy, runoff control, documented waste handling and care with beach-facing lighting. Without that the file does not move.')],
 'ru': [('Почему отель в Пуэрто-Морелосе, а не в Канкуне?', 'Более доступная земля, атмосфера посёлка и риф в нескольких метрах: концепция дайвинга и природы держит тариф при меньшем числе номеров. Обратная сторона — более строгие экологические нормы из-за Нацпарка.'),
        ('Что риф требует от отеля?', 'Очистные под вместимость, контроль стока, документированный вывоз отходов и аккуратность с освещением в сторону пляжа. Без этого пакет не двигается.')],
 'de': [('Warum ein Hotel in Puerto Morelos statt in Cancún?', 'Günstigeres Grundstück, Dorfatmosphäre und ein Riff wenige Meter vor der Küste: Ein Tauch- und Naturkonzept trägt die Rate mit weniger Zimmern. Die Kehrseite sind strengere Umweltauflagen wegen des Nationalparks.'),
        ('Was verlangt das Riff von einem Hotel?', 'Eine auf die Belegung ausgelegte Kläranlage, Abflusskontrolle, dokumentierte Abfallentsorgung und Sorgfalt bei strandseitiger Beleuchtung. Ohne das bewegt sich die Akte nicht.')],
 'fr': [('Pourquoi un hôtel à Puerto Morelos plutôt qu’à Cancún ?', 'Un foncier plus accessible, une ambiance de village et un récif à quelques mètres : un concept plongée et nature soutient le tarif avec moins de clés. La contrepartie, ce sont des règles environnementales plus strictes du fait du Parc National.'),
        ('Qu’exige le récif d’un hôtel ?', 'Une station de traitement dimensionnée à la capacité, le contrôle des ruissellements, une gestion documentée des déchets et de la prudence sur l’éclairage côté plage. Sans cela, le dossier n’avance pas.')],
 'zh': [('为什么选择在 Puerto Morelos 而不是坎昆建酒店？', '地价更友好、镇区氛围突出、珊瑚礁近在数米：以潜水与自然为主题的概念，可以用更少的客房维持房价。代价是因国家公园而更严格的环保要求。'),
        ('珊瑚礁对酒店提出哪些要求？', '按接待容量配置的污水处理设备、径流控制、可追溯的废弃物处理，以及谨慎处理朝向沙滩的照明。做不到这些，报批无法推进。')]},
}

LINKS = {
 'es': {'vh-puerto-aventuras': [('/construccion-de-casas-puerto-aventuras/','Construcción de casas en Puerto Aventuras'), ('/villas-de-lujo-puerto-aventuras/','Villas de lujo en Puerto Aventuras'), ('/construccion-comercial-hoteles-riviera-maya/','Construcción comercial y hoteles'), ('/calculadora/','Calculadora de costos')],
        'vh-akumal': [('/construccion-de-casas-akumal/','Construcción de casas en Akumal'), ('/villas-de-lujo-akumal/','Villas de lujo en Akumal'), ('/construccion-comercial-hoteles-riviera-maya/','Construcción comercial y hoteles'), ('/calculadora/','Calculadora de costos')],
        'vh-puerto-morelos': [('/constructora-puerto-morelos/','Constructora en Puerto Morelos'), ('/construccion-de-casas-punta-brava/','Construcción de casas en Punta Brava'), ('/construccion-de-casas-bahia-petempich/','Construcción de casas en Bahía Petempich'), ('/construccion-comercial-hoteles-riviera-maya/','Construcción comercial y hoteles')]},
 'en': {'vh-puerto-aventuras': [('/house-construction-puerto-aventuras/','House construction in Puerto Aventuras'), ('/luxury-villas-puerto-aventuras/','Luxury villas in Puerto Aventuras'), ('/commercial-hotel-construction-riviera-maya/','Commercial and hotel construction'), ('/calculator/','Cost calculator')],
        'vh-akumal': [('/house-construction-akumal/','House construction in Akumal'), ('/luxury-villas-akumal/','Luxury villas in Akumal'), ('/commercial-hotel-construction-riviera-maya/','Commercial and hotel construction'), ('/calculator/','Cost calculator')],
        'vh-puerto-morelos': [('/construction-company-puerto-morelos/','Construction company in Puerto Morelos'), ('/house-construction-punta-brava/','House construction in Punta Brava'), ('/house-construction-bahia-petempich/','House construction in Petempich Bay'), ('/commercial-hotel-construction-riviera-maya/','Commercial and hotel construction')]},
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
    for _z, _d in CITIES.items():
        town = _d['town'] or 'riviera-maya'
        LINKS[_lang][_z] = [('/%s-%s/' % (_pref, town), '%s — %s' % (hub, ml.CITY[_lang][town])),
                            perm, ('/%s-riviera-maya/' % _pref, '%s — %s' % (hub, ml.CITY[_lang]['riviera-maya'])),
                            (_calc, names[0]), (_blog, names[1])]


if __name__ == '__main__':
    for z in CITIES:
        z1.ZAREA[z] = AREAS[z]; z1.ZTEXT[z] = TEXT[z]; z1.ZFAQ[z] = FAQ[z]
    for lang in LINKS:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS[lang])
    for k in ['h1', 'title', 'desc', 'block', 'alert', 'h_cost', 'row', 'h_proc']:
        ml.OVR.setdefault(k, {})
    for z, d in CITIES.items():
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
            ml.OVR['block'].setdefault(z, {})
    # build the hospitality block with this batch's per-key figures
    def block(z, lang):
        b = il.BLOCK_STR[lang]; c = NAMES[z][lang]
        rows = '\n'.join('<tr><td>%s</td><td>%s USD</td><td>%s</td></tr>' % (r[0], k, r[1])
                         for r, k in zip(b['rows'], KEYS[z]))
        lis = '\n'.join('<li>%s</li>' % x for x in b['li'])
        return ('<h2 class="mt-4">%s</h2>\n<p>%s</p>\n'
                '<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark">'
                '<tr><th>%s</th><th>%s</th><th>%s</th></tr></thead><tbody>\n%s\n</tbody></table></div>\n'
                '<h3 class="mt-3">%s</h3>\n<ul>\n%s\n</ul>'
                % (b['h'].format(c=c), b['p'], b['th'][0], b['th'][1], b['th'][2], rows, b['h2'], lis))
    for z in CITIES:
        for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
            ml.OVR['block'][z][lang] = block(z, lang)
    ml.LOCS.extend(CITIES)
    for lang in ['es', 'en', 'ru', 'de', 'fr', 'zh']:
        ch = ml.chrome(lang)
        for z in CITIES:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-52s %6d bytes' % (out + '/', len(html)))
