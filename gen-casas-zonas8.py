#!/usr/bin/env python3
"""Eighth zone batch (2026-08-11): Tulum's remaining premium submarkets.

Verified before writing: Holistika is the wellness-led community priced above
Regiones 11, 12 and 15 and La Veleta; Región 8 is among the closest inland areas to
the beaches and already holds luxury homes, with infrastructure still developing;
Región 12 sits below Holistika on price; Tulum Centro is the most accessible and one
of the priciest per m² in sale terms.

Not built: Luum Zamá — it is a micro-zone inside Aldea Zamá, which already has its
own page; a separate page would duplicate it.
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

ZONE8 = {
 'holistika-tulum':  dict(parent='tulum', f=1.25, perm='3–5'),
 'region-8-tulum':   dict(parent='tulum', f=1.15, perm='3–5'),
 'region-12-tulum':  dict(parent='tulum', f=1.02, perm='3–5'),
 'tulum-centro':     dict(parent='tulum', f=1.10, perm='2–4'),
}

NAMES = {
 'holistika-tulum': {'es': 'Holistika, Tulum', 'en': 'Holistika, Tulum', 'ru': 'Холистика, Тулум',
   'de': 'Holistika, Tulum', 'fr': 'Holistika, Tulum', 'zh': '图卢姆 Holistika'},
 'region-8-tulum': {'es': 'Región 8, Tulum', 'en': 'Región 8, Tulum', 'ru': 'Регионе 8, Тулум',
   'de': 'Región 8, Tulum', 'fr': 'Región 8, Tulum', 'zh': '图卢姆8区'},
 'region-12-tulum': {'es': 'Región 12, Tulum', 'en': 'Región 12, Tulum', 'ru': 'Регионе 12, Тулум',
   'de': 'Región 12, Tulum', 'fr': 'Región 12, Tulum', 'zh': '图卢姆12区'},
 'tulum-centro': {'es': 'Tulum Centro', 'en': 'Tulum Centro', 'ru': 'центре Тулума',
   'de': 'Tulum Centro', 'fr': 'Tulum Centro', 'zh': '图卢姆市中心'},
}
AREAS = {
 'holistika-tulum': {'es': 'Holistika y su entorno de selva', 'en': 'Holistika and its jungle setting',
   'ru': 'Холистике и окружающей сельве', 'de': 'Holistika und seinem Dschungelumfeld',
   'fr': 'Holistika et son cadre de jungle', 'zh': 'Holistika 及其丛林环境'},
 'region-8-tulum': {'es': 'Región 8 y su acceso a las playas', 'en': 'Región 8 and its access to the beaches',
   'ru': 'Регионе 8 и его выходе к пляжам', 'de': 'Región 8 und seinem Zugang zu den Stränden',
   'fr': 'Región 8 et son accès aux plages', 'zh': '8区及其通往海滩的路径'},
 'region-12-tulum': {'es': 'Región 12 y las manzanas vecinas', 'en': 'Región 12 and the neighbouring blocks',
   'ru': 'Регионе 12 и соседних кварталах', 'de': 'Región 12 und den angrenzenden Blöcken',
   'fr': 'Región 12 et les îlots voisins', 'zh': '12区及相邻街区'},
 'tulum-centro': {'es': 'Tulum centro y la avenida Tulum', 'en': 'downtown Tulum and Avenida Tulum',
   'ru': 'центре Тулума и на авеню Тулум', 'de': 'dem Zentrum von Tulum und der Avenida Tulum',
   'fr': 'le centre de Tulum et l’avenue Tulum', 'zh': '图卢姆市中心与 Tulum 大道'},
}

TEXT = {
'holistika-tulum': {
 'es': 'Holistika es la comunidad de bienestar de Tulum: selva conservada, baja densidad y un lenguaje de diseño que la zona da por hecho —materiales naturales, ventilación cruzada, integración con el entorno—. Está por encima en precio de las Regiones 11, 12 y 15 y de La Veleta, y esa prima se paga por concepto, no por metros. El proyecto se diseña alrededor de los árboles y del ruido que no quiere oírse.',
 'en': 'Holistika is Tulum’s wellness community: preserved jungle, low density and a design language the area takes for granted — natural materials, cross ventilation, integration with the surroundings. It prices above Regiones 11, 12 and 15 and La Veleta, and that premium is paid for the concept, not for square metres. The project is designed around the trees and around the noise you do not want to hear.',
 'ru': 'Холистика — велнес-сообщество Тулума: сохранённая сельва, низкая плотность и язык дизайна, который здесь считается нормой — природные материалы, сквозная вентиляция, встроенность в среду. По цене она выше Регионов 11, 12 и 15 и Ла-Велеты, и эта премия платится за концепцию, а не за метры. Проект строится вокруг деревьев и вокруг шума, которого не хочется слышать.',
 'de': 'Holistika ist Tulums Wellness-Community: erhaltener Dschungel, geringe Dichte und eine Entwurfssprache, die hier vorausgesetzt wird — natürliche Materialien, Querlüftung, Einbindung in die Umgebung. Preislich liegt sie über den Regionen 11, 12 und 15 und über La Veleta; dieser Aufschlag wird für das Konzept gezahlt, nicht für Quadratmeter. Geplant wird um die Bäume herum — und um den Lärm, den man nicht hören will.',
 'fr': 'Holistika est la communauté bien-être de Tulum : jungle préservée, faible densité et un langage architectural que le secteur tient pour acquis — matériaux naturels, ventilation traversante, intégration au site. Elle se situe au-dessus des Regiones 11, 12 et 15 et de La Veleta en prix, et cette prime se paie pour le concept, pas pour les mètres carrés. Le projet se conçoit autour des arbres et du bruit que l’on ne veut pas entendre.',
 'zh': 'Holistika 是图卢姆的康养社区：丛林得到保留、密度低，并有一套该片区默认的设计语汇——天然材料、穿堂通风、与环境融合。其价格高于11区、12区、15区与 La Veleta，这份溢价买的是理念而非面积。方案要围绕树木布置，也要围绕“不想听见的噪音”来布置。'},
'region-8-tulum': {
 'es': 'Región 8 es de las zonas interiores más cercanas a las playas de Tulum y ya concentra casas de nivel alto. La contraparte honesta es la infraestructura: todavía en desarrollo, y cambia de una calle a otra. Antes de comprar verificamos agua, CFE, acceso pavimentado y situación legal del predio; ese chequeo decide el costo real de la obra más que el diseño.',
 'en': 'Región 8 is among the inland areas closest to Tulum’s beaches and already concentrates high-end houses. The honest counterweight is infrastructure: still developing, and it changes from one street to the next. Before buying we verify water, CFE, paved access and the lot’s legal status; that check decides the real cost of the build more than the design does.',
 'ru': 'Регион 8 — одна из внутренних зон, ближайших к пляжам Тулума, и там уже стоят дома высокого уровня. Честная обратная сторона — инфраструктура: она ещё формируется и меняется от улицы к улице. До покупки проверяем воду, CFE, асфальтированный подъезд и юридический статус участка; именно эта проверка определяет реальную стоимость стройки сильнее, чем проект.',
 'de': 'Región 8 gehört zu den strandnächsten Binnenlagen Tulums und versammelt bereits hochwertige Häuser. Das ehrliche Gegengewicht ist die Infrastruktur: noch im Aufbau und von Straße zu Straße verschieden. Vor dem Kauf prüfen wir Wasser, CFE, befestigte Zufahrt und Rechtslage; diese Prüfung bestimmt die realen Baukosten stärker als der Entwurf.',
 'fr': 'Región 8 fait partie des secteurs intérieurs les plus proches des plages de Tulum et rassemble déjà des maisons haut de gamme. Le contrepoids honnête, c’est l’infrastructure : encore en développement, et variable d’une rue à l’autre. Avant l’achat, nous vérifions l’eau, la CFE, l’accès goudronné et la situation juridique ; cette vérification pèse plus sur le coût réel que la conception.',
 'zh': '8区是图卢姆距海滩最近的内陆片区之一，已聚集了一批高端住宅。诚实的另一面是基础设施：仍在建设中，且逐街不同。购地前我们会核查供水、CFE 供电、硬化道路接入与地块法律状态；这项核查对实际造价的影响，往往大于设计本身。'},
'region-12-tulum': {
 'es': 'Región 12 es el punto medio de Tulum: más barata que Holistika y que las zonas de playa, con acceso razonable al centro y a la carretera. Funciona bien para primera casa o para renta a residentes, y es donde el presupuesto rinde más por m² construido. La condición sigue siendo la misma del resto de la ciudad: verificar servicios calle por calle y resolver la ruta de SEMA antes de arrancar.',
 'en': 'Región 12 is Tulum’s middle ground: cheaper than Holistika and the beach areas, with reasonable access to downtown and the highway. It works well for a first house or a rental to residents, and it is where the budget stretches furthest per built m². The condition is the same as everywhere else in town: verify services street by street and settle the SEMA route before starting.',
 'ru': 'Регион 12 — середина Тулума: дешевле Холистики и пляжных зон, с разумным доступом к центру и трассе. Хорошо работает для первого дома или аренды резидентам, и именно здесь бюджет даёт больше построенных м². Условие то же, что и по всему городу: проверить коммуникации по улицам и закрыть маршрут SEMA до старта.',
 'de': 'Región 12 ist Tulums Mittelfeld: günstiger als Holistika und die Strandlagen, mit vernünftiger Anbindung an Zentrum und Landstraße. Gut für das erste Haus oder die Vermietung an Residenten — hier reicht das Budget pro gebautem m² am weitesten. Die Bedingung ist dieselbe wie überall in der Stadt: Versorgung Straße für Straße prüfen und den SEMA-Weg vor Baubeginn klären.',
 'fr': 'Región 12 est le juste milieu de Tulum : moins chère qu’Holistika et que les secteurs de plage, avec un accès raisonnable au centre et à la route. Elle convient pour une première maison ou une location à des résidents, et c’est là que le budget rend le plus au m² construit. La condition reste celle de toute la ville : vérifier les réseaux rue par rue et régler le parcours SEMA avant de démarrer.',
 'zh': '12区是图卢姆的中间地带：价格低于 Holistika 与海滩片区，前往市中心与公路都还算便利。适合作为首套自住房或面向常住客的出租房，也是预算在“每建成平方米”上最划算的片区。前提与全城一致：逐街核查市政配套，并在开工前走完 SEMA 流程。'},
'tulum-centro': {
 'es': 'Tulum centro es la zona con servicios ya instalados y el acceso más rápido a todo: por eso el m² de venta es de los más altos de la ciudad y por eso el trámite suele ser más corto que en las regiones jóvenes. Aquí el producto rara vez es una villa aislada: son casas urbanas, edificios pequeños y proyectos de uso mixto, con las reglas de densidad, altura y estacionamiento del centro pesando sobre el diseño.',
 'en': 'Downtown Tulum is the area with services already installed and the fastest access to everything: that is why sale prices per m² are among the city’s highest and why the permit route is usually shorter than in the young regions. The product here is rarely an isolated villa: it is townhouses, small buildings and mixed-use projects, with downtown density, height and parking rules bearing on the design.',
 'ru': 'Центр Тулума — зона с уже подведёнными сетями и самым быстрым доступом ко всему: поэтому цена продажи за м² здесь одна из самых высоких в городе, а процедура обычно короче, чем в молодых регионах. Продукт здесь редко бывает отдельной виллой: это городские дома, небольшие здания и проекты смешанного назначения, а на дизайн давят правила плотности, высоты и парковок.',
 'de': 'Das Zentrum von Tulum ist der Bereich mit vorhandener Versorgung und dem schnellsten Zugang zu allem: Deshalb zählen die Verkaufspreise pro m² zu den höchsten der Stadt und der Genehmigungsweg ist meist kürzer als in den jungen Regionen. Das Produkt ist hier selten die freistehende Villa: es sind Stadthäuser, kleine Gebäude und Mischnutzungsprojekte — mit Dichte-, Höhen- und Stellplatzregeln, die den Entwurf prägen.',
 'fr': 'Le centre de Tulum est le secteur déjà viabilisé et le plus accessible : d’où des prix de vente au m² parmi les plus élevés de la ville et un parcours de permis généralement plus court que dans les regiones jeunes. Le produit y est rarement une villa isolée : ce sont des maisons de ville, de petits immeubles et des projets mixtes, avec les règles de densité, de hauteur et de stationnement qui pèsent sur la conception.',
 'zh': '图卢姆市中心市政配套已就位、通达性最好：因此其每平方米售价位居全城前列，报批周期通常也短于新兴片区。这里的产品很少是独栋别墅，而多为联排住宅、小体量建筑与混合用途项目；市中心的密度、限高与停车位规定会直接影响方案。'},
}

FAQ = {
'holistika-tulum': {
 'es': [('¿Por qué Holistika cuesta más que Región 12 o La Veleta?', 'Por concepto y densidad: selva conservada, pocos lotes y un estándar de diseño e integración que el mercado ya espera aquí. No se paga por metros, se paga por entorno.'),
        ('¿Se puede hacer un retiro o proyecto de bienestar?', 'Depende del uso de suelo del predio. Donde se permite, el formato natural es pequeño —cabañas o villas con áreas comunes— y con SEMA resuelta antes de operar, no después.')],
 'en': [('Why does Holistika cost more than Región 12 or La Veleta?', 'Concept and density: preserved jungle, few lots and a design and integration standard the market already expects here. You do not pay for square metres, you pay for the setting.'),
        ('Can I build a retreat or wellness project?', 'It depends on the lot’s land use. Where allowed, the natural format is small — cabins or villas with shared areas — with SEMA settled before operating, not after.')],
 'ru': [('Почему Холистика дороже Региона 12 или Ла-Велеты?', 'Из-за концепции и плотности: сохранённая сельва, мало участков и стандарт дизайна и встроенности, который рынок здесь уже ожидает. Платят не за метры, а за среду.'),
        ('Можно ли сделать ретрит или велнес-проект?', 'Зависит от назначения земли участка. Где разрешено, естественный формат небольшой — домики или виллы с общими зонами — и с закрытой SEMA до начала работы, а не после.')],
 'de': [('Warum kostet Holistika mehr als Región 12 oder La Veleta?', 'Konzept und Dichte: erhaltener Dschungel, wenige Grundstücke und ein Gestaltungs- und Einbindungsstandard, den der Markt hier erwartet. Man zahlt nicht für Quadratmeter, sondern für das Umfeld.'),
        ('Kann ich ein Retreat- oder Wellnessprojekt bauen?', 'Das hängt von der Nutzungsart ab. Wo erlaubt, ist das natürliche Format klein — Cabañas oder Villen mit Gemeinschaftsflächen — mit geklärter SEMA vor dem Betrieb, nicht danach.')],
 'fr': [('Pourquoi Holistika coûte-t-il plus que Región 12 ou La Veleta ?', 'Le concept et la densité : jungle préservée, peu de lots et un standard de conception et d’intégration que le marché attend ici. On ne paie pas des mètres carrés, on paie un cadre.'),
        ('Peut-on faire une retraite ou un projet bien-être ?', 'Cela dépend de l’usage du sol. Là où c’est permis, le format naturel est petit — cabañas ou villas avec espaces communs — avec la SEMA réglée avant l’exploitation, pas après.')],
 'zh': [('为什么 Holistika 比12区或 La Veleta 更贵？', '在于理念与密度：丛林得以保留、地块稀少，且市场对此地的设计与融入环境已有既定期待。买的不是面积，而是环境。'),
        ('可以做静修或康养项目吗？', '取决于地块土地用途。在允许之处，合适的形态偏小——带公共区域的木屋或别墅——且须在开始运营前完成 SEMA，而非事后补办。')]},
'region-8-tulum': {
 'es': [('¿Qué reviso antes de comprar en Región 8?', 'Agua, CFE, acceso pavimentado, uso de suelo y situación legal del predio, calle por calle. La zona está cerca de la playa pero su infraestructura sigue en desarrollo, y eso mueve el presupuesto real.'),
        ('¿Ya hay casas de nivel alto en Región 8?', 'Sí, la zona concentra propiedades de gama alta por su cercanía a las playas. Eso sostiene el valor, pero no sustituye la verificación de servicios en su calle concreta.')],
 'en': [('What should I check before buying in Región 8?', 'Water, CFE, paved access, land use and the lot’s legal status, street by street. The area is close to the beach but its infrastructure is still developing, and that moves the real budget.'),
        ('Are there already high-end houses in Región 8?', 'Yes, the area concentrates upmarket properties thanks to its proximity to the beaches. That sustains value, but it does not replace checking services on your specific street.')],
 'ru': [('Что проверить до покупки в Регионе 8?', 'Воду, CFE, асфальтированный подъезд, назначение земли и юридический статус участка — по каждой улице. Зона близко к пляжу, но инфраструктура ещё формируется, и это двигает реальный бюджет.'),
        ('Есть ли уже дома высокого уровня в Регионе 8?', 'Да, зона концентрирует премиальные объекты благодаря близости к пляжам. Это держит стоимость, но не отменяет проверку коммуникаций именно на вашей улице.')],
 'de': [('Was prüfe ich vor dem Kauf in Región 8?', 'Wasser, CFE, befestigte Zufahrt, Nutzungsart und Rechtslage — Straße für Straße. Die Lage ist strandnah, aber die Infrastruktur entsteht noch, und das verschiebt das reale Budget.'),
        ('Gibt es in Región 8 bereits hochwertige Häuser?', 'Ja, das Gebiet bündelt gehobene Objekte wegen der Strandnähe. Das trägt den Wert, ersetzt aber nicht die Prüfung der Versorgung in Ihrer konkreten Straße.')],
 'fr': [('Que vérifier avant d’acheter en Región 8 ?', 'L’eau, la CFE, l’accès goudronné, l’usage du sol et la situation juridique, rue par rue. Le secteur est proche de la plage mais son infrastructure se construit encore, ce qui déplace le budget réel.'),
        ('Y a-t-il déjà des maisons haut de gamme en Región 8 ?', 'Oui, le secteur concentre des biens haut de gamme grâce à la proximité des plages. Cela soutient la valeur, mais ne remplace pas la vérification des réseaux dans votre rue.')],
 'zh': [('在8区购地前要核查什么？', '逐街核查供水、CFE 供电、硬化道路接入、土地用途与地块法律状态。该片区靠近海滩，但配套仍在建设，这会直接改变实际预算。'),
        ('8区已经有高端住宅了吗？', '有。凭借靠近海滩的区位，该片区聚集了不少高端物业。这支撑了资产价值，但仍不能替代对您所在街道配套情况的核查。')]},
'region-12-tulum': {
 'es': [('¿Región 12 conviene para primera casa?', 'Sí: es de los mejores rendimientos por m² construido en Tulum, con acceso razonable al centro. El ahorro está en el terreno, no en bajar el estándar de obra.'),
        ('¿Aplica SEMA aquí también?', 'En la mayoría de los predios sí, junto con uso de suelo y licencia municipal con DRO. Presupueste de 3 a 5 meses de permisos y arranque el trámite con el anteproyecto.')],
 'en': [('Is Región 12 good for a first house?', 'Yes: it delivers some of the best value per built m² in Tulum, with reasonable access to downtown. The saving is in the land, not in lowering the build standard.'),
        ('Does SEMA apply here too?', 'On most lots yes, along with land use and the municipal licence with a DRO. Budget 3 to 5 months of permits and start the process with the concept design.')],
 'ru': [('Подходит ли Регион 12 для первого дома?', 'Да: одна из лучших отдач на построенный м² в Тулуме при разумном доступе к центру. Экономия — в земле, а не в снижении стандарта стройки.'),
        ('SEMA действует и здесь?', 'На большинстве участков да, вместе с назначением земли и муниципальной лицензией с DRO. Закладывайте 3–5 месяцев на разрешения и запускайте процедуру с эскизом.')],
 'de': [('Eignet sich Región 12 für das erste Haus?', 'Ja: eines der besten Verhältnisse pro gebautem m² in Tulum, bei vernünftiger Anbindung ans Zentrum. Gespart wird am Grundstück, nicht am Baustandard.'),
        ('Gilt die SEMA auch hier?', 'Auf den meisten Grundstücken ja, dazu Nutzungsart und kommunale Lizenz mit DRO. Kalkulieren Sie 3 bis 5 Monate Genehmigungen und starten Sie mit dem Entwurf.')],
 'fr': [('Región 12 convient-il pour une première maison ?', 'Oui : c’est l’un des meilleurs rendements au m² construit de Tulum, avec un accès raisonnable au centre. L’économie est sur le terrain, pas sur le standard de construction.'),
        ('La SEMA s’applique-t-elle aussi ici ?', 'Sur la plupart des lots oui, avec l’usage du sol et le permis municipal avec DRO. Comptez 3 à 5 mois de permis et lancez la procédure dès l’avant-projet.')],
 'zh': [('12区适合作为首套自住房吗？', '适合：在图卢姆，它的“每建成平方米性价比”名列前茅，前往市中心也较为便利。省的是地价，而不是施工标准。'),
        ('这里也需要办 SEMA 吗？', '多数地块需要，此外还需土地用途与带 DRO 的市政许可。许可周期请预留3至5个月，并在方案阶段即启动。')]},
'tulum-centro': {
 'es': [('¿Se puede construir una villa en Tulum centro?', 'Se puede, pero rara vez es lo que conviene: los lotes son urbanos y las reglas de densidad, altura y estacionamiento empujan hacia casa urbana, edificio pequeño o uso mixto.'),
        ('¿El trámite es más rápido en el centro?', 'Suele serlo, porque los servicios ya están instalados y no hay que demostrar factibilidad desde cero. El uso de suelo y la licencia municipal con DRO siguen siendo obligatorios.')],
 'en': [('Can you build a villa in downtown Tulum?', 'You can, but it is rarely the right move: the lots are urban and density, height and parking rules push towards a townhouse, a small building or mixed use.'),
        ('Is the permit process faster downtown?', 'Usually yes, because services are already installed and feasibility does not have to be proven from scratch. Land use and the municipal licence with a DRO are still mandatory.')],
 'ru': [('Можно ли построить виллу в центре Тулума?', 'Можно, но редко это разумно: участки городские, а правила плотности, высоты и парковок толкают к городскому дому, небольшому зданию или смешанному использованию.'),
        ('Процедура в центре быстрее?', 'Обычно да, потому что сети уже подведены и не нужно доказывать возможность подключения с нуля. Назначение земли и муниципальная лицензия с DRO всё равно обязательны.')],
 'de': [('Kann man im Zentrum von Tulum eine Villa bauen?', 'Man kann, aber es ist selten sinnvoll: Die Grundstücke sind städtisch, und Dichte-, Höhen- und Stellplatzregeln drängen zu Stadthaus, kleinem Gebäude oder Mischnutzung.'),
        ('Geht das Verfahren im Zentrum schneller?', 'Meist ja, weil die Versorgung vorhanden ist und die Machbarkeit nicht von Grund auf nachgewiesen werden muss. Nutzungsart und kommunale Lizenz mit DRO bleiben Pflicht.')],
 'fr': [('Peut-on construire une villa au centre de Tulum ?', 'On peut, mais c’est rarement pertinent : les lots sont urbains et les règles de densité, hauteur et stationnement orientent vers la maison de ville, le petit immeuble ou le mixte.'),
        ('La procédure est-elle plus rapide au centre ?', 'En général oui, car les réseaux sont là et la faisabilité n’est pas à démontrer de zéro. L’usage du sol et le permis municipal avec DRO restent obligatoires.')],
 'zh': [('能在图卢姆市中心建独栋别墅吗？', '可以，但通常并不划算：地块属城市用地，密度、限高与停车位规定更适合联排住宅、小体量建筑或混合用途。'),
        ('市中心的报批更快吗？', '通常更快，因为市政配套已就位，无需从零证明接入可行性。但土地用途与带 DRO 的市政许可仍是必办项。')]},
}

LINKS = {}
_HUB = {'es': ('construccion-de-casas', 'Construcción de casas', '/calculadora/', 'Calculadora de costos', '/blog-es/', 'Guías de construcción'),
        'en': ('house-construction', 'House construction', '/calculator/', 'Cost calculator', '/blog/', 'Construction guides'),
        'ru': ('stroitelstvo-domov', 'Строительство домов', '/kalkulyator/', 'Калькулятор стоимости', '/blog-ru/', 'Гиды по строительству'),
        'de': ('hausbau', 'Hausbau', '/kostenrechner/', 'Kostenrechner', '/blog-de/', 'Bau-Leitfäden'),
        'fr': ('construction-de-maisons', 'Construction de maisons', '/calculateur/', 'Calculateur de coûts', '/blog-fr/', 'Guides de construction'),
        'zh': ('zhuzhai-jianzao', '住宅建造', '/jisuanqi/', '造价计算器', '/blog-zh/', '建筑指南')}
_PERM = {'es': ('/permisos-de-construccion-tulum-ciudad/', 'Permisos de construcción en Tulum'),
         'en': ('/construction-permits-tulum-city/', 'Construction permits in Tulum'),
         'ru': ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'),
         'de': ('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen, Lizenzen und DRO'),
         'fr': ('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'),
         'zh': ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO')}
for _l, (_p, _hub, _c, _cn, _b, _bn) in _HUB.items():
    LINKS[_l] = {}
    for _z in ZONE8:
        LINKS[_l][_z] = [('/%s-tulum/' % _p, '%s — Tulum' % _hub), _PERM[_l],
                         ('/%s-la-veleta/' % _p, _hub), (_c, _cn), (_b, _bn)]


def _set_parent_urls(locs):
    P = {'es': 'construccion-de-casas', 'en': 'house-construction', 'ru': 'stroitelstvo-domov',
         'de': 'hausbau', 'fr': 'construction-de-maisons', 'zh': 'zhuzhai-jianzao'}
    ml.OVR.setdefault('parent_url', {})
    for zk, d in locs.items():
        for l in LANGS:
            ml.OVR['parent_url'].setdefault(zk, {})[l] = '/%s-%s/' % (P[l], d['parent'])


if __name__ == '__main__':
    _set_parent_urls(ZONE8)
    for z in ZONE8:
        z1.ZAREA[z] = AREAS[z]; z1.ZTEXT[z] = TEXT[z]; z1.ZFAQ[z] = FAQ[z]
    for lang in LINKS:
        z1.ZLINKS.setdefault(lang, {}).update(LINKS[lang])
    for z, d in ZONE8.items():
        for lang in LANGS:
            z1.ZNAME.setdefault(lang, {})[z] = NAMES[z][lang]
        z1.register(z, d)
    ml.LOCS.extend(ZONE8)
    for lang in LANGS:
        ch = ml.chrome(lang)
        for z in ZONE8:
            out = ml.SLUG[lang][z]
            os.makedirs(out, exist_ok=True)
            html = ml.build(lang, z, ch)
            open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(html)
            print('%-46s %6d bytes' % (out + '/', len(html)))
