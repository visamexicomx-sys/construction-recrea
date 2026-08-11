#!/usr/bin/env python3
"""Holbox guide, 6 languages — deliberately NOT a "we build here" page.

Everything in it was verified before writing: Holbox belongs to the municipality of
Lázaro Cárdenas and sits inside the Yum Balam Flora and Fauna Protection Area
(federal decree of 6 June 1994); the height cap inside the reserve is 12 m and the
municipality has ordered a top floor demolished for exceeding it; SEMARNAT denied
the Biocentro Isla Grande project (49 stilt units over 331+ ha) on density and
preservation-zone grounds, applying the 20-year forestry ban that followed the
August 2025 fire; in October 2025 authorities flagged 25+ illegal developments
inside protected areas including Yum Balam; the Yalahau aquifer is contaminated
through missing sewerage and poor wastewater management.

The article says plainly that we build on the mainland and do not sell new-build
villas on Holbox. It exists to answer the question honestly, not to take a deposit.

Published as a blog article in each language so rebuild-blog-index.py picks it up
and files it under permits automatically.
"""
import os, re, json

BASE = 'https://construction-recrea.com'
TPL = {
 'es': ('blog-es', 'permisos-construccion-playa-del-carmen.html', 'holbox-permisos-construccion-que-se-puede.html'),
 'en': ('blog', 'construction-permits-playa-del-carmen.html', 'holbox-construction-permits-what-you-can-build.html'),
 'ru': ('blog-ru', 'razresheniya-na-stroitelstvo-playa-del-carmen.html', 'holbox-razresheniya-na-stroitelstvo.html'),
 'de': ('blog-de', 'baugenehmigungen-playa-del-carmen.html', 'holbox-baugenehmigungen-was-erlaubt-ist.html'),
 'fr': ('blog-fr', 'permis-construction-playa-del-carmen.html', 'holbox-permis-construction-ce-qui-est-autorise.html'),
 'zh': ('blog-zh', 'playa-del-carmen-jianzhu-xukezheng.html', 'holbox-jianzhu-xukezheng-zhinan.html'),
}
BLOG_HOME = {'es': '../blog-es/', 'en': '../blog/', 'ru': '../blog-ru/', 'de': '../blog-de/',
             'fr': '../blog-fr/', 'zh': '../blog-zh/'}
HOME_LABEL = {'es': 'Inicio', 'en': 'Home', 'ru': 'Главная', 'de': 'Startseite', 'fr': 'Accueil', 'zh': '首页'}
BLOG_LABEL = {'es': 'Blog', 'en': 'Blog', 'ru': 'Блог', 'de': 'Blog', 'fr': 'Blog', 'zh': '博客'}

T = {
'es': dict(
 title='Construir en Holbox: qué permite la ley y qué no (2026)',
 desc='Holbox está dentro del área protegida Yum Balam: altura máxima 12 m, autorización federal además de la municipal y precedentes de proyectos negados. Qué se puede construir y qué no.',
 h1='Construir en Holbox: qué permite la ley y qué no',
 lead='Holbox se vende como el próximo Tulum. Legalmente no lo es, y conviene entender por qué antes de comprar un terreno. Esta guía resume lo que la normativa permite hoy, con los precedentes de 2025 y 2026 sobre la mesa.',
 secs=[('Dos autoridades, no una',
   'Holbox pertenece al municipio de Lázaro Cárdenas, pero la isla completa está dentro del Área de Protección de Flora y Fauna Yum Balam, decretada por el gobierno federal el 6 de junio de 1994. Eso significa que la licencia municipal no basta: cualquier obra relevante necesita además autorización ambiental federal. Un proyecto puede cumplir con el municipio y aun así no construirse nunca.'),
  ('Altura, densidad y zonas',
   'Dentro de la reserva la altura máxima permitida es de 12 metros, y no es letra muerta: personal del municipio de Lázaro Cárdenas ha ordenado demoler el último nivel de una construcción por exceder ese límite. La densidad y la zonificación del área protegida pesan igual: hay polígonos de preservación donde simplemente no se autoriza desarrollo, independientemente de lo que diga el vendedor del terreno.'),
  ('Los precedentes de 2025 y 2026',
   'SEMARNAT negó el permiso al proyecto Biocentro Isla Grande —49 casas sobre pilotes en más de 331 hectáreas— por no cumplir con la densidad y por ubicarse en zona de preservación del área natural protegida. En la negativa pesó además la veda forestal de 20 años derivada del incendio de agosto de 2025. Y en octubre de 2025 las autoridades ambientales identificaron más de 25 desarrollos irregulares dentro de áreas naturales protegidas, Yum Balam entre ellas.'),
  ('El problema de fondo: agua y drenaje',
   'La razón por la que todo se endureció no es estética. En el acuífero de Yalahau se han detectado niveles altos de contaminación por falta de infraestructura, crecimiento turístico descontrolado y mal manejo de aguas residuales. Mientras eso no se resuelva, la autoridad tiene un argumento sólido para negar cualquier proyecto que sume carga sin resolver su propio tratamiento.'),
  ('Logística: no hay coches y todo llega en ferry',
   'A Holbox se llega en ferry desde Chiquilá y en la isla no circulan automóviles. Todo el material —cemento, acero, cancelería, mobiliario— cruza en embarcación y se mueve en carritos. La excavación en suelo arenoso se hace a mano, con pico y pala, para el desplante de zapatas, pilotes o columnas que levantan la casa del terreno. Cada una de esas condiciones se traduce en tiempo y en costo por m² muy por encima del continente.'),
  ('Qué sí se puede hacer hoy',
   'Obra menor y remodelación de construcciones existentes en el polígono urbano con servicios ya instalados; sustitución o mejora de plantas de tratamiento; adecuaciones que no aumenten densidad ni altura. Todo con licencia municipal y, según el caso, con autorización ambiental. Es un terreno de trabajo real, pero acotado: no es lo mismo que levantar una villa nueva frente a la playa.'),
  ('Antes de comprar un terreno en Holbox',
   'Pida y verifique cinco cosas: la constancia de uso de suelo vigente, la ubicación exacta del predio respecto a los polígonos del área natural protegida, si existe autorización ambiental previa y con qué condicionantes, la situación legal del título y la factibilidad real de agua y tratamiento. Si el vendedor no puede mostrar los dos primeros documentos, no hay proyecto que valga la pena diseñar.')],
 stance_h='Nuestra postura, con toda claridad',
 stance='Recrea construye en el corredor de la Riviera Maya —Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal, Puerto Morelos—, no en Holbox. No vendemos villas nuevas en la isla porque, en la mayoría de los predios que se ofrecen hoy, ese permiso no se obtiene. Escribimos esta guía porque nos preguntan por Holbox cada mes y la respuesta honesta ahorra dinero. Si después de leerla su proyecto se muda al continente, ahí sí podemos construirlo con precio fijo.',
 faq=[('¿Se puede construir una casa nueva en Holbox?',
       'Depende del predio. La isla está dentro del área protegida Yum Balam y hay polígonos de preservación donde no se autoriza desarrollo. Además de la licencia municipal de Lázaro Cárdenas se requiere autorización ambiental federal, y hay precedentes recientes de negativas.'),
      ('¿Cuál es la altura máxima permitida en Holbox?',
       'Dentro de la reserva son 12 metros. El municipio ha ordenado demoler niveles construidos por encima de ese límite, así que no es un criterio negociable en obra.'),
      ('¿Por qué negaron proyectos hoteleros recientemente?',
       'El caso más citado es Biocentro Isla Grande: 49 casas sobre pilotes en más de 331 hectáreas, negado por densidad y por ubicarse en zona de preservación, con la veda forestal de 20 años posterior al incendio de agosto de 2025 como agravante.'),
      ('¿Ustedes construyen en Holbox?',
       'No. Trabajamos en el corredor de la Riviera Maya. Si su proyecto termina en Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal o Puerto Morelos, lo construimos con contrato a precio fijo.')],
 cta='Si su proyecto es en la Riviera Maya, cotícelo',
 links=[('/construccion-de-casas-riviera-maya/', 'Construcción de casas en la Riviera Maya'),
        ('/permisos-licencias-construccion-riviera-maya/', 'Permisos, licencias y DRO'),
        ('/construccion-de-casas-tulum/', 'Construcción de casas en Tulum')]),

'en': dict(
 title='Building on Holbox: what the law allows and what it does not (2026)',
 desc='Holbox sits inside the Yum Balam protected area: 12 m height cap, federal authorisation on top of the municipal licence and recent project denials. What can and cannot be built.',
 h1='Building on Holbox: what the law allows and what it does not',
 lead='Holbox is sold as the next Tulum. Legally it is not, and it is worth understanding why before buying land. This guide sets out what the rules allow today, with the 2025 and 2026 precedents on the table.',
 secs=[('Two authorities, not one',
   'Holbox belongs to the municipality of Lázaro Cárdenas, but the whole island lies inside the Yum Balam Flora and Fauna Protection Area, decreed by the federal government on 6 June 1994. A municipal licence is therefore not enough: any meaningful work also needs federal environmental authorisation. A project can satisfy the municipality and still never be built.'),
  ('Height, density and zoning',
   'Inside the reserve the maximum permitted height is 12 metres, and it is enforced: staff from the municipality of Lázaro Cárdenas have ordered the top floor of a building demolished for exceeding it. Density and the protected area’s zoning weigh just as much: there are preservation polygons where development is simply not authorised, whatever the land seller says.'),
  ('The 2025 and 2026 precedents',
   'SEMARNAT denied the permit for the Biocentro Isla Grande project — 49 stilt houses across more than 331 hectares — for failing density rules and for sitting in a preservation zone of the protected area. The denial also applied the 20-year forestry ban that followed the August 2025 fire. And in October 2025 environmental authorities identified more than 25 irregular developments inside protected natural areas, Yum Balam among them.'),
  ('The real problem: water and sewerage',
   'The reason everything tightened is not aesthetic. High contamination levels have been found in the Yalahau aquifer because of missing infrastructure, uncontrolled tourism growth and poor wastewater management. Until that is fixed, the authority has a solid argument to deny any project that adds load without solving its own treatment.'),
  ('Logistics: no cars, everything arrives by ferry',
   'Holbox is reached by ferry from Chiquilá and no cars circulate on the island. Every material — cement, steel, joinery, furniture — crosses by boat and moves on carts. Excavation in the sandy soil is done by hand, with pick and shovel, for the footings, piles or columns that lift the house off the ground. Each of those conditions turns into time and into a cost per m² well above the mainland.'),
  ('What can actually be done today',
   'Minor works and renovation of existing buildings inside the urban footprint where services already exist; replacing or upgrading treatment plants; adjustments that add neither density nor height. All of it with a municipal licence and, depending on the case, environmental authorisation. It is real work, but bounded — it is not the same as putting up a new beachfront villa.'),
  ('Before you buy land on Holbox',
   'Ask for and verify five things: the current land-use certificate, the lot’s exact position relative to the protected area polygons, whether a prior environmental authorisation exists and under what conditions, the legal status of the title, and real feasibility of water and treatment. If the seller cannot produce the first two documents, there is no project worth designing.')],
 stance_h='Our position, stated plainly',
 stance='Recrea builds in the Riviera Maya corridor — Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal, Puerto Morelos — not on Holbox. We do not sell new-build villas on the island because, on most of the lots offered today, that permit is not obtainable. We wrote this guide because we are asked about Holbox every month and the honest answer saves money. If after reading it your project moves to the mainland, that we can build, at a fixed price.',
 faq=[('Can you build a new house on Holbox?',
       'It depends on the lot. The island is inside the Yum Balam protected area and there are preservation polygons where development is not authorised. On top of the Lázaro Cárdenas municipal licence, federal environmental authorisation is required, and there are recent precedents of denials.'),
      ('What is the maximum building height on Holbox?',
       '12 metres inside the reserve. The municipality has ordered floors built above that limit demolished, so it is not negotiable on site.'),
      ('Why were hotel projects denied recently?',
       'The most cited case is Biocentro Isla Grande: 49 stilt houses across more than 331 hectares, denied on density grounds and for sitting in a preservation zone, with the 20-year forestry ban following the August 2025 fire as an aggravating factor.'),
      ('Do you build on Holbox?',
       'No. We work in the Riviera Maya corridor. If your project ends up in Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal or Puerto Morelos, we build it under a fixed-price contract.')],
 cta='If your project is in the Riviera Maya, get a quote',
 links=[('/house-construction-riviera-maya/', 'House construction in the Riviera Maya'),
        ('/construction-permits-licenses-riviera-maya/', 'Permits, licences and DRO'),
        ('/house-construction-tulum/', 'House construction in Tulum')]),

'ru': dict(
 title='Строительство на Холбоше: что закон разрешает, а что нет (2026)',
 desc='Холбош внутри охраняемой территории Yum Balam: лимит высоты 12 м, федеральное согласование сверх муниципального и свежие отказы по проектам. Что можно строить, а что нельзя.',
 h1='Строительство на Холбоше: что закон разрешает, а что нет',
 lead='Холбош продают как «следующий Тулум». Юридически это не так, и разобраться стоит до покупки участка. Гид собирает то, что нормы разрешают сегодня, с прецедентами 2025 и 2026 годов на столе.',
 secs=[('Две инстанции, а не одна',
   'Холбош относится к муниципалитету Ласаро-Карденас, но весь остров находится внутри Зоны охраны флоры и фауны Yum Balam, учреждённой федеральным правительством 6 июня 1994 года. Значит, муниципальной лицензии недостаточно: любой значимый объект требует ещё и федерального экологического разрешения. Проект может устроить муниципалитет и всё равно никогда не быть построен.'),
  ('Высота, плотность и зоны',
   'Внутри резервата максимальная разрешённая высота — 12 метров, и это не формальность: сотрудники муниципалитета Ласаро-Карденас предписывали снести верхний уровень постройки за превышение лимита. Плотность и зонирование охраняемой территории весят не меньше: есть полигоны сохранения, где застройка просто не согласуется, что бы ни говорил продавец участка.'),
  ('Прецеденты 2025 и 2026 годов',
   'SEMARNAT отказала в разрешении проекту Biocentro Isla Grande — 49 домов на сваях более чем на 331 гектаре — за несоответствие плотности и за расположение в зоне сохранения охраняемой территории. В отказе учли и 20-летний запрет на лесопользование, введённый после пожара августа 2025 года. А в октябре 2025 экологические власти выявили более 25 нелегальных застроек внутри охраняемых природных территорий, включая Yum Balam.'),
  ('Корень проблемы: вода и канализация',
   'Ужесточение произошло не из-за эстетики. В водоносном горизонте Yalahau зафиксирован высокий уровень загрязнения из-за отсутствия инфраструктуры, неконтролируемого роста туризма и плохого обращения со сточными водами. Пока это не решено, у власти есть весомый аргумент отказать любому проекту, который добавляет нагрузку, не решая собственную очистку.'),
  ('Логистика: машин нет, всё идёт паромом',
   'На Холбош попадают паромом из Чикилы, автомобили по острову не ездят. Весь материал — цемент, арматура, окна, мебель — переправляется судном и развозится тележками. Выемка в песчаном грунте делается вручную, киркой и лопатой, под подошвы, сваи или колонны, поднимающие дом над землёй. Каждое из этих условий превращается во время и в цену за м², заметно выше материковой.'),
  ('Что реально можно делать сегодня',
   'Мелкие работы и реконструкция существующих построек в городской черте с уже подведёнными сетями; замена или модернизация очистных; изменения, которые не увеличивают ни плотность, ни высоту. Всё — с муниципальной лицензией и, по ситуации, с экологическим согласованием. Это реальный фронт работ, но ограниченный: это не то же самое, что поставить новую виллу у моря.'),
  ('Перед покупкой участка на Холбоше',
   'Запросите и проверьте пять вещей: действующую справку о назначении земли, точное положение участка относительно полигонов охраняемой территории, наличие предыдущего экологического разрешения и его условия, юридическую чистоту титула и реальную возможность подключения воды и очистки. Если продавец не может показать первые два документа, проектировать нечего.')],
 stance_h='Наша позиция, без обиняков',
 stance='Recrea строит в коридоре Ривьеры-Майя — Плая-дель-Кармен, Тулум, Канкун, Пуэрто-Авентурас, Акумаль, Пуэрто-Морелос, — а не на Холбоше. Мы не продаём новые виллы на острове, потому что на большинстве предлагаемых сегодня участков такое разрешение не получить. Этот гид написан потому, что про Холбош спрашивают каждый месяц, а честный ответ экономит деньги. Если после прочтения ваш проект переедет на материк — его мы построим по фиксированной цене.',
 faq=[('Можно ли построить новый дом на Холбоше?',
       'Зависит от участка. Остров внутри охраняемой территории Yum Balam, и есть полигоны сохранения, где застройка не согласуется. Кроме муниципальной лицензии Ласаро-Карденас нужно федеральное экологическое разрешение, и есть свежие прецеденты отказов.'),
      ('Какая максимальная высота застройки на Холбоше?',
       '12 метров внутри резервата. Муниципалитет предписывал сносить уровни, построенные выше лимита, так что на площадке это не обсуждается.'),
      ('Почему недавно отказали отельным проектам?',
       'Самый цитируемый случай — Biocentro Isla Grande: 49 домов на сваях более чем на 331 гектаре, отказ по плотности и из-за расположения в зоне сохранения, с 20-летним запретом на лесопользование после пожара августа 2025 года как отягчающим фактором.'),
      ('Вы строите на Холбоше?',
       'Нет. Мы работаем в коридоре Ривьеры-Майя. Если проект окажется в Плая-дель-Кармен, Тулуме, Канкуне, Пуэрто-Авентурас, Акумале или Пуэрто-Морелосе — построим по договору с фиксированной ценой.')],
 cta='Если ваш проект на Ривьере-Майя — посчитаем',
 links=[('/stroitelstvo-domov-riviera-maya/', 'Строительство домов на Ривьере-Майя'),
        ('/razresheniya-i-licenzii-riviera-maya/', 'Разрешения, лицензии и DRO'),
        ('/stroitelstvo-domov-tulum/', 'Строительство домов в Тулуме')]),

'de': dict(
 title='Bauen auf Holbox: was das Gesetz erlaubt und was nicht (2026)',
 desc='Holbox liegt im Schutzgebiet Yum Balam: 12 m Höhengrenze, föderale Genehmigung zusätzlich zur kommunalen und aktuelle Projektablehnungen. Was gebaut werden darf und was nicht.',
 h1='Bauen auf Holbox: was das Gesetz erlaubt und was nicht',
 lead='Holbox wird als das nächste Tulum verkauft. Rechtlich ist es das nicht, und man sollte verstehen warum, bevor man ein Grundstück kauft. Dieser Leitfaden fasst zusammen, was die Vorschriften heute zulassen — mit den Präzedenzfällen von 2025 und 2026 auf dem Tisch.',
 secs=[('Zwei Behörden, nicht eine',
   'Holbox gehört zur Gemeinde Lázaro Cárdenas, doch die gesamte Insel liegt im Schutzgebiet für Flora und Fauna Yum Balam, das die Bundesregierung am 6. Juni 1994 dekretierte. Eine kommunale Lizenz genügt also nicht: Jedes relevante Vorhaben braucht zusätzlich eine föderale Umweltgenehmigung. Ein Projekt kann die Gemeinde zufriedenstellen und trotzdem nie gebaut werden.'),
  ('Höhe, Dichte und Zonierung',
   'Innerhalb des Reservats beträgt die zulässige Höhe 12 Meter — und das wird durchgesetzt: Mitarbeiter der Gemeinde Lázaro Cárdenas haben den Abriss des obersten Geschosses eines Gebäudes angeordnet, weil es die Grenze überschritt. Dichte und Zonierung des Schutzgebiets wiegen ebenso schwer: Es gibt Erhaltungspolygone, in denen Entwicklung schlicht nicht genehmigt wird, was auch immer der Grundstücksverkäufer sagt.'),
  ('Die Präzedenzfälle 2025 und 2026',
   'SEMARNAT lehnte die Genehmigung für das Projekt Biocentro Isla Grande ab — 49 Pfahlhäuser auf mehr als 331 Hektar — wegen Verstoßes gegen die Dichtevorgaben und wegen der Lage in einer Erhaltungszone des Schutzgebiets. In die Ablehnung floss zudem das 20-jährige Rodungsverbot nach dem Brand vom August 2025 ein. Und im Oktober 2025 identifizierten Umweltbehörden mehr als 25 irreguläre Entwicklungen innerhalb geschützter Naturgebiete, darunter Yum Balam.'),
  ('Das eigentliche Problem: Wasser und Abwasser',
   'Der Grund für die Verschärfung ist nicht ästhetisch. Im Yalahau-Grundwasserleiter wurden hohe Verschmutzungswerte festgestellt — durch fehlende Infrastruktur, unkontrolliertes Tourismuswachstum und schlechtes Abwassermanagement. Solange das nicht gelöst ist, hat die Behörde ein starkes Argument, jedes Projekt abzulehnen, das Last hinzufügt, ohne seine eigene Aufbereitung zu lösen.'),
  ('Logistik: keine Autos, alles kommt per Fähre',
   'Holbox erreicht man per Fähre aus Chiquilá, auf der Insel fahren keine Autos. Jedes Material — Zement, Stahl, Fenster, Möbel — überquert per Boot und wird auf Karren bewegt. Der Aushub im Sandboden erfolgt von Hand, mit Spitzhacke und Schaufel, für Fundamente, Pfähle oder Stützen, die das Haus vom Boden abheben. Jede dieser Bedingungen wird zu Zeit und zu einem m²-Preis deutlich über dem Festland.'),
  ('Was heute tatsächlich möglich ist',
   'Kleinere Arbeiten und Sanierung bestehender Gebäude im Siedlungsbereich mit vorhandener Versorgung; Ersatz oder Ertüchtigung von Kläranlagen; Anpassungen, die weder Dichte noch Höhe erhöhen. Alles mit kommunaler Lizenz und je nach Fall mit Umweltgenehmigung. Das ist echte Arbeit, aber begrenzt — nicht dasselbe wie eine neue Strandvilla zu errichten.'),
  ('Bevor Sie auf Holbox ein Grundstück kaufen',
   'Verlangen und prüfen Sie fünf Dinge: die gültige Nutzungsbescheinigung, die genaue Lage des Grundstücks zu den Polygonen des Schutzgebiets, ob eine frühere Umweltgenehmigung existiert und unter welchen Auflagen, die Rechtslage des Titels und die reale Machbarkeit von Wasser und Aufbereitung. Kann der Verkäufer die ersten beiden Dokumente nicht vorlegen, lohnt sich kein Entwurf.')],
 stance_h='Unsere Position, klar gesagt',
 stance='Recrea baut im Korridor der Riviera Maya — Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal, Puerto Morelos — nicht auf Holbox. Wir verkaufen keine Neubauvillen auf der Insel, weil diese Genehmigung auf den meisten heute angebotenen Grundstücken nicht zu bekommen ist. Wir haben diesen Leitfaden geschrieben, weil wir jeden Monat nach Holbox gefragt werden und die ehrliche Antwort Geld spart. Zieht Ihr Projekt danach aufs Festland, bauen wir es zum Festpreis.',
 faq=[('Kann man auf Holbox ein neues Haus bauen?',
       'Das hängt vom Grundstück ab. Die Insel liegt im Schutzgebiet Yum Balam, und es gibt Erhaltungspolygone, in denen keine Entwicklung genehmigt wird. Zusätzlich zur kommunalen Lizenz von Lázaro Cárdenas ist eine föderale Umweltgenehmigung erforderlich, und es gibt aktuelle Ablehnungen.'),
      ('Wie hoch darf auf Holbox gebaut werden?',
       '12 Meter innerhalb des Reservats. Die Gemeinde hat den Abriss von Geschossen oberhalb dieser Grenze angeordnet — auf der Baustelle ist das nicht verhandelbar.'),
      ('Warum wurden zuletzt Hotelprojekte abgelehnt?',
       'Der meistzitierte Fall ist Biocentro Isla Grande: 49 Pfahlhäuser auf mehr als 331 Hektar, abgelehnt wegen Dichte und Lage in einer Erhaltungszone, verschärft durch das 20-jährige Rodungsverbot nach dem Brand vom August 2025.'),
      ('Bauen Sie auf Holbox?',
       'Nein. Wir arbeiten im Korridor der Riviera Maya. Landet Ihr Projekt in Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal oder Puerto Morelos, bauen wir es mit Festpreisvertrag.')],
 cta='Liegt Ihr Projekt in der Riviera Maya, holen Sie ein Angebot',
 links=[('/hausbau-riviera-maya/', 'Hausbau in der Riviera Maya'),
        ('/baugenehmigungen-lizenzen-riviera-maya/', 'Genehmigungen, Lizenzen und DRO'),
        ('/hausbau-tulum/', 'Hausbau in Tulum')]),

'fr': dict(
 title='Construire à Holbox : ce que la loi autorise et ce qu’elle interdit (2026)',
 desc='Holbox est dans l’aire protégée Yum Balam : hauteur limitée à 12 m, autorisation fédérale en plus du permis municipal et refus de projets récents. Ce qui peut se construire, et ce qui ne peut pas.',
 h1='Construire à Holbox : ce que la loi autorise et ce qu’elle interdit',
 lead='Holbox se vend comme le prochain Tulum. Juridiquement, ce n’en est pas un, et mieux vaut comprendre pourquoi avant d’acheter un terrain. Ce guide résume ce que la réglementation permet aujourd’hui, avec les précédents de 2025 et 2026 sur la table.',
 secs=[('Deux autorités, pas une',
   'Holbox relève de la commune de Lázaro Cárdenas, mais toute l’île se situe dans l’Aire de Protection de la Flore et de la Faune Yum Balam, décrétée par le gouvernement fédéral le 6 juin 1994. Le permis municipal ne suffit donc pas : tout chantier significatif exige en plus une autorisation environnementale fédérale. Un projet peut satisfaire la commune et ne jamais voir le jour.'),
  ('Hauteur, densité et zonage',
   'Dans la réserve, la hauteur maximale autorisée est de 12 mètres, et la règle est appliquée : des agents de la commune de Lázaro Cárdenas ont ordonné la démolition du dernier niveau d’une construction qui la dépassait. La densité et le zonage de l’aire protégée pèsent tout autant : il existe des polygones de préservation où aucun développement n’est autorisé, quoi qu’en dise le vendeur du terrain.'),
  ('Les précédents de 2025 et 2026',
   'La SEMARNAT a refusé le permis au projet Biocentro Isla Grande — 49 maisons sur pilotis sur plus de 331 hectares — pour non-respect de la densité et pour implantation en zone de préservation de l’aire protégée. Le refus s’appuyait aussi sur l’interdiction forestière de 20 ans consécutive à l’incendie d’août 2025. Et en octobre 2025, les autorités environnementales ont identifié plus de 25 développements irréguliers dans des aires naturelles protégées, dont Yum Balam.'),
  ('Le vrai problème : l’eau et l’assainissement',
   'Le durcissement n’est pas esthétique. Des niveaux élevés de contamination ont été relevés dans l’aquifère de Yalahau, faute d’infrastructures, du fait d’une croissance touristique incontrôlée et d’une mauvaise gestion des eaux usées. Tant que cela n’est pas réglé, l’autorité dispose d’un argument solide pour refuser tout projet qui ajoute de la charge sans traiter ses propres effluents.'),
  ('Logistique : pas de voitures, tout arrive par ferry',
   'On accède à Holbox par ferry depuis Chiquilá et aucune voiture ne circule sur l’île. Tout le matériel — ciment, acier, menuiseries, mobilier — traverse en bateau et se déplace en chariots. L’excavation dans le sol sableux se fait à la main, à la pioche et à la pelle, pour les semelles, pieux ou poteaux qui soulèvent la maison. Chacune de ces conditions se traduit en temps et en coût au m² bien supérieur au continent.'),
  ('Ce qu’il est réellement possible de faire',
   'Travaux mineurs et rénovation de bâtiments existants dans le périmètre urbain déjà desservi ; remplacement ou amélioration des stations de traitement ; adaptations qui n’augmentent ni densité ni hauteur. Le tout avec permis municipal et, selon les cas, autorisation environnementale. C’est du travail réel, mais borné — ce n’est pas construire une villa neuve en front de mer.'),
  ('Avant d’acheter un terrain à Holbox',
   'Demandez et vérifiez cinq choses : le certificat d’usage du sol en vigueur, la position exacte du terrain par rapport aux polygones de l’aire protégée, l’existence d’une autorisation environnementale antérieure et ses conditions, la situation juridique du titre et la faisabilité réelle de l’eau et du traitement. Si le vendeur ne peut pas produire les deux premiers documents, aucun projet ne mérite d’être dessiné.')],
 stance_h='Notre position, dite clairement',
 stance='Recrea construit dans le corridor de la Riviera Maya — Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal, Puerto Morelos — pas à Holbox. Nous ne vendons pas de villas neuves sur l’île car, sur la plupart des terrains proposés aujourd’hui, ce permis ne s’obtient pas. Nous avons écrit ce guide parce qu’on nous interroge sur Holbox chaque mois et que la réponse honnête fait économiser de l’argent. Si votre projet migre ensuite vers le continent, celui-là, nous le construisons à prix fixe.',
 faq=[('Peut-on construire une maison neuve à Holbox ?',
       'Cela dépend du terrain. L’île est dans l’aire protégée Yum Balam et certains polygones de préservation n’autorisent aucun développement. Outre le permis municipal de Lázaro Cárdenas, une autorisation environnementale fédérale est requise, et des refus récents existent.'),
      ('Quelle est la hauteur maximale à Holbox ?',
       '12 mètres dans la réserve. La commune a ordonné la démolition de niveaux construits au-dessus de cette limite : ce n’est pas négociable sur le chantier.'),
      ('Pourquoi des projets hôteliers ont-ils été refusés récemment ?',
       'Le cas le plus cité est Biocentro Isla Grande : 49 maisons sur pilotis sur plus de 331 hectares, refusé pour densité et pour implantation en zone de préservation, avec l’interdiction forestière de 20 ans postérieure à l’incendie d’août 2025 comme facteur aggravant.'),
      ('Construisez-vous à Holbox ?',
       'Non. Nous travaillons dans le corridor de la Riviera Maya. Si votre projet aboutit à Playa del Carmen, Tulum, Cancún, Puerto Aventuras, Akumal ou Puerto Morelos, nous le construisons à prix fixe.')],
 cta='Si votre projet est dans la Riviera Maya, demandez un devis',
 links=[('/construction-de-maisons-riviera-maya/', 'Construction de maisons dans la Riviera Maya'),
        ('/permis-et-licences-construction-riviera-maya/', 'Permis, licences et DRO'),
        ('/construction-de-maisons-tulum/', 'Construction de maisons à Tulum')]),

'zh': dict(
 title='在 Holbox 建房：法律允许什么、禁止什么（2026）',
 desc='Holbox 位于 Yum Balam 保护区内：限高12米，除市政许可外还需联邦环保批准，并有近期项目被否的先例。哪些能建、哪些不能建。',
 h1='在 Holbox 建房：法律允许什么、禁止什么',
 lead='Holbox 常被当作“下一个图卢姆”来推销。从法律上看并非如此，购地之前值得先弄清原因。本指南梳理现行法规允许的范围，并摆出2025与2026年的实际先例。',
 secs=[('两个主管机关，而非一个',
   'Holbox 隶属 Lázaro Cárdenas 市，但整座岛屿都位于联邦政府于1994年6月6日设立的 Yum Balam 动植物保护区之内。因此仅有市政许可并不够：任何有实质规模的工程还需联邦环保许可。一个项目可能满足了市政要求，却依然永远无法开工。'),
  ('高度、密度与分区',
   '保护区内允许的最大建筑高度为12米，并且确实执行：Lázaro Cárdenas 市工作人员曾因超高而责令拆除某建筑的顶层。保护区的密度与分区同样关键：存在完全不批准开发的保育多边形区域，无论卖地方如何宣称。'),
  ('2025与2026年的先例',
   'SEMARNAT 否决了 Biocentro Isla Grande 项目的许可——在331公顷以上土地上建设49栋高脚屋——理由是不符合密度要求且位于保护区的保育区内。否决同时援引了2025年8月火灾之后实施的20年林业禁令。此外，2025年10月环保部门在多个自然保护区（含 Yum Balam）内查出超过25处违规开发。'),
  ('真正的症结：供水与排污',
   '监管收紧并非出于审美考量。由于基础设施缺失、旅游无序增长与污水处理不当，Yalahau 含水层已检出较高污染水平。在这一问题解决之前，主管部门有充分理由否决任何新增负荷却未解决自身处理能力的项目。'),
  ('物流：岛上无汽车，一切靠轮渡',
   '前往 Holbox 需从 Chiquilá 乘轮渡，岛上不通行汽车。水泥、钢材、门窗、家具等所有材料都要经船运抵，再以小车转运。砂质土层的开挖以人工镐锹完成，用于设置将房屋抬离地面的基脚、桩或柱。每一项条件都会转化为工期与远高于大陆的每平方米造价。'),
  ('今天真正可以做的事',
   '在已有市政配套的建成区内，对既有建筑进行小型工程与翻新；更换或升级污水处理设备；不增加密度与高度的调整。以上均需市政许可，并视情况需要环保批准。这是真实存在的工作范围，但边界清晰——与在海边新建一栋别墅完全不是一回事。'),
  ('在 Holbox 购地之前',
   '请索取并核实五项：现行土地用途证明、地块相对保护区多边形的精确位置、是否已有环保许可及其附加条件、产权的法律状态，以及供水与污水处理的实际可行性。如果卖方拿不出前两份文件，就没有值得设计的项目。')],
 stance_h='我们的立场，直说',
 stance='Recrea 在里维埃拉玛雅走廊施工——普拉亚德尔卡门、图卢姆、坎昆、Puerto Aventuras、Akumal、Puerto Morelos——不在 Holbox。我们不在岛上销售新建别墅，因为目前挂牌的多数地块根本拿不到相应许可。撰写本指南，是因为每个月都有人问起 Holbox，而诚实的答案能替人省钱。若读完之后您的项目转到大陆，那样的项目我们可以按固定总价承建。',
 faq=[('在 Holbox 可以新建住宅吗？',
       '取决于具体地块。全岛位于 Yum Balam 保护区内，部分保育多边形区域完全不批准开发。除 Lázaro Cárdenas 市政许可外，还需联邦环保许可，且近期已有被否先例。'),
      ('Holbox 的建筑限高是多少？',
       '保护区内为12米。市政曾责令拆除超出该限值的楼层，因此在现场没有商量余地。'),
      ('为什么近期有酒店项目被否？',
       '最常被引用的是 Biocentro Isla Grande：在331公顷以上土地上建49栋高脚屋，因密度不符且位于保育区而被否，2025年8月火灾后实施的20年林业禁令是加重因素。'),
      ('你们在 Holbox 施工吗？',
       '不。我们的业务范围是里维埃拉玛雅走廊。若您的项目落在普拉亚德尔卡门、图卢姆、坎昆、Puerto Aventuras、Akumal 或 Puerto Morelos，我们可按固定总价合同承建。')],
 cta='如果您的项目在里维埃拉玛雅，欢迎索取报价',
 links=[('/zhuzhai-jianzao-riviera-maya/', '里维埃拉玛雅住宅建造'),
        ('/jianzhu-xuke-yu-zhizhao-riviera-maya/', '建筑许可与DRO'),
        ('/zhuzhai-jianzao-tulum/', '图卢姆住宅建造')]),
}


def build(lang):
    folder, tpl_name, out_name = TPL[lang]
    src = open(os.path.join(folder, tpl_name), encoding='utf-8').read()
    t = T[lang]
    url = '%s/%s/%s' % (BASE, folder, out_name)

    head_end = src.index('</head>')
    head = src[:head_end]
    body_rest = src[head_end:]

    # keep only the asset links from the template head, drop its meta/schema
    assets = '\n'.join(l for l in head.split('\n')
                       if ('cdn.jsdelivr' in l or 'fonts.g' in l or 'style.min.css' in l
                           or 'favicon' in l or 'apple-touch' in l or 'webmanifest' in l))
    alts = '\n  '.join('<link rel="alternate" hreflang="%s" href="%s/%s/%s">'
                       % (c, BASE, TPL[c][0], TPL[c][2]) for c in ['es', 'en', 'de', 'ru', 'zh', 'fr'])
    alts += '\n  <link rel="alternate" hreflang="x-default" href="%s/%s/%s">' % (BASE, TPL['en'][0], TPL['en'][2])
    art = {"@context": "https://schema.org", "@type": "Article", "headline": t['title'],
           "description": t['desc'], "inLanguage": lang, "datePublished": "2026-08-10",
           "author": {"@type": "Organization", "name": "Recrea Construction", "url": BASE},
           "publisher": {"@type": "Organization", "name": "Recrea Construction"},
           "mainEntityOfPage": url}
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
           {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t['faq']]}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": HOME_LABEL[lang], "item": BASE + "/"},
          {"@type": "ListItem", "position": 2, "name": BLOG_LABEL[lang], "item": '%s/%s/' % (BASE, folder)},
          {"@type": "ListItem", "position": 3, "name": t['title']}]}

    new_head = ('<!DOCTYPE html>\n<html lang="%s">\n<head>\n'
                '  <meta name="google-site-verification" content="0WwXyAoY4jeA2xgFFFB06a9HqEfzR7LnyLYVBrFTU0A" />\n'
                '  <meta charset="UTF-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
                '  <title>%s</title>\n  <meta name="description" content="%s">\n%s\n'
                '  <script type="application/ld+json">%s</script>\n'
                '  <script type="application/ld+json">%s</script>\n'
                '  <script type="application/ld+json">%s</script>\n'
                '  <link rel="canonical" href="%s">\n  %s\n'
                '  <meta property="og:type" content="article">\n'
                '  <meta property="og:title" content="%s">\n'
                '  <meta property="og:description" content="%s">\n'
                '  <meta property="og:url" content="%s">\n'
                '  <meta property="og:image" content="%s/img/og-wallpaper.png">\n'
                '  <meta name="twitter:card" content="summary_large_image">\n'
                % (lang, t['title'], t['desc'], assets,
                   json.dumps(art, ensure_ascii=False), json.dumps(faq, ensure_ascii=False),
                   json.dumps(bc, ensure_ascii=False), url, alts, t['title'], t['desc'], url, BASE))

    secs = '\n'.join('<h2 class="mt-4">%s</h2>\n<p>%s</p>' % (h, p) for h, p in t['secs'])
    faq_html = '\n'.join(
        '<div class="accordion-item"><h3 class="accordion-header"><button class="accordion-button%s" type="button" '
        'data-bs-toggle="collapse" data-bs-target="#hbfaq%d">%s</button></h3>'
        '<div id="hbfaq%d" class="accordion-collapse collapse%s" data-bs-parent="#hbFaq">'
        '<div class="accordion-body">%s</div></div></div>'
        % ('' if i == 0 else ' collapsed', i, q, i, ' show' if i == 0 else '', a)
        for i, (q, a) in enumerate(t['faq']))
    links = ' · '.join('<a href="%s">%s</a>' % l for l in t['links'])

    article = ('''<nav class="container mt-3"><ol class="breadcrumb"><li class="breadcrumb-item"><a href="/">%s</a></li>'''
               '''<li class="breadcrumb-item"><a href="%s">%s</a></li>'''
               '''<li class="breadcrumb-item active">%s</li></ol></nav>
<section class="py-5"><div class="container"><div class="row justify-content-center"><div class="col-lg-8">
<h1>%s</h1>
<p class="lead">%s</p>
%s
<h2 class="mt-4">%s</h2>
<div class="alert" style="background:#f8f9fa;border-left:4px solid #c8a96e">%s</div>
<p>%s</p>
<h2 class="mt-5">%s</h2>
<div class="accordion my-4" id="hbFaq">
%s
</div>
<div class="cta-section rounded p-5 text-center my-5">
<h3 class="text-white mb-3">%s</h3>
<a href="https://wa.me/529844525333" target="_blank" rel="noopener" class="btn btn-cta btn-lg"><i class="bi bi-whatsapp me-2"></i>WhatsApp</a>
</div>
</div></div></div></section>
''' % (HOME_LABEL[lang], BLOG_HOME[lang], BLOG_LABEL[lang], t['title'],
       t['h1'], t['lead'], secs, t['stance_h'], t['stance'], links, 'FAQ', faq_html, t['cta']))

    # chrome from the template: everything from <body> to <footer, and the footer onwards
    body_start = body_rest.index('<body')
    chrome_top = body_rest[body_start:body_rest.index('<div style="padding-top:116px"></div>') + len('<div style="padding-top:116px"></div>')]
    chrome_bottom = body_rest[body_rest.index('<footer'):]
    return new_head + '</head>\n' + chrome_top + '\n' + article + chrome_bottom


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for lang in TPL:
        folder, _, out_name = TPL[lang]
        html = build(lang)
        open(os.path.join(folder, out_name), 'w', encoding='utf-8').write(html)
        print('%-16s %-56s %6d bytes' % (lang, folder + '/' + out_name, len(html)))
