#!/usr/bin/env python3
"""Give the stub blog articles real content.

Measuring every blog for the first time showed the non-English ones carry
100-250 words of their own prose inside 300-560 words of repeated navigation:
76 articles across ES, DE, RU and ZH. The duplicate-pair counts those blogs were
showing (ES 286, ZH 188, DE 100, RU 74 above 0.55) are a symptom of that, not
the disease — stripping the shared blocks would have exposed the emptiness
rather than fixed it.

Every stub has the same skeleton: an H2 "Services" paragraph repeating the meta
description, an H2 "Costs" paragraph saying to contact us, and then the shared
furniture. This replaces exactly that span with sections written for the topic
in that language. Everything else on the page — cost table, process, FAQ, CTA,
links, the photograph — is left alone.
"""
import os, re, sys

SVC = {'es': 'Servicios', 'de': 'Leistungen', 'ru': 'Услуги', 'zh': '服务',
       'fr': 'Prestations', 'en': 'Services'}
END = '<div class="bg-dark text-white p-4 rounded my-4 text-center">'
COST = {'es': '<h2>Costos de Construcción por Zona', 'de': '<h2>Baukosten nach Standort',
        'ru': '<h2>Стоимость строительства по', 'zh': '<h2>各区域建设成本'}
FAQ_H = {'es': '<h2>Preguntas Frecuentes', 'de': '<h2>Häufige Fragen',
         'ru': '<h2>Частые вопросы', 'zh': '<h2>常见问题'}

# (lang, topic) -> [(h2, html), ...]
C = {}


def fill(lang, path, secs):
    h = open(path, encoding='utf-8').read()
    marker = '<h2>%s</h2>' % SVC[lang]
    body = ''.join('<h2>%s</h2>\n%s\n' % (t, b.strip()) for t, b in secs)
    if '<!--filled-->' in h:
        return None                       # already done
    if marker in h:
        # stub skeleton: the empty Services/Costs pair is replaced outright
        start = h.index(marker)
        end = h.index(END, start)
        out = h[:start] + '<!--filled-->' + body + h[end:]
    else:
        # article already has real headings but is thin: insert before the
        # shared cost table or the FAQ, whichever comes first
        anchors = [a for a in (COST[lang], FAQ_H[lang]) if a in h]
        if not anchors:
            return None
        cut = min(h.index(a) for a in anchors)
        out = h[:cut] + '<!--filled-->' + body + h[cut:]
    open(path, 'w', encoding='utf-8').write(out)
    words = len(re.findall(r'[^\s<>]+', re.sub(r'<[^>]+>', ' ', body)))
    chars = len([c for c in re.sub(r'<[^>]+>', ' ', body) if not c.isspace()])
    return words if lang != 'zh' else chars


# --- restaurant & bar construction --------------------------------------------
C[("es","blog-es/construccion-restaurantes-bares-riviera-maya.html")] = [
("Lo que decide si un local sirve para restaurante", """
<p>Tres cosas deciden la viabilidad antes de elegir un solo acabado, y las tres se resuelven <strong>antes de firmar el arrendamiento</strong>:</p>
<ul>
<li><strong>La ruta de extracción.</strong> Una cocina comercial necesita ducto con descarga a nivel de azotea y aire de reposición que lo equilibre. Si el edificio no tiene ruta, o el condominio no la autoriza, el concepto no cabe en ese local a ningún presupuesto. Es el motivo más frecuente por el que un proyecto se cae, y se verifica en una tarde.</li>
<li><strong>Grasas y drenaje.</strong> Trampa de grasa dimensionada para los comensales previstos, con acceso para mantenimiento, y capacidad de drenaje que la losa existente realmente admita. Abrir pendientes nuevas en una losa terminada es caro y a veces estructuralmente imposible.</li>
<li><strong>Aforo y salidas.</strong> Protección Civil calcula el aforo a partir del mobiliario, y ese número define anchos de salida, distancias de recorrido, iluminación de emergencia y plan de evacuación. Un acomodo más denso puede rebasar lo que las salidas existentes soportan: por eso el layout se acuerda contra el cálculo de aforo, no después.</li>
</ul>
"""),
("Licencias que corren en paralelo a la obra", """
<p>La licencia de funcionamiento para giro de alimentos, el permiso de alcohol donde aplica &mdash; con sus restricciones por ubicación &mdash; y los requisitos sanitarios que determinan acabados, ubicación de lavamanos y cadena de frío. En terraza frente al mar se suma la zona federal marítimo terrestre: antes de dibujar nada del lado de la playa hay que saber dónde termina la propiedad.</p>
<p>El trámite suele ser más largo que la obra, y por eso arranca primero. La fecha que importa no es cuándo termina la construcción, sino cuándo le permiten abrir.</p>
"""),
("Costos y tiempos reales 2026", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Alcance</th><th>MXN/m²</th><th>Tiempo de obra</th></tr></thead><tbody>
<tr><td>Cafetería o comida rápida: cocina, extracción, instalaciones</td><td>$18,000&ndash;$35,000</td><td>10&ndash;16 semanas</td></tr>
<tr><td>Restaurante completo con barra</td><td>$25,000&ndash;$55,000</td><td>12&ndash;20 semanas</td></tr>
<tr><td>Beach club o terraza de gran formato</td><td>$30,000&ndash;$60,000+</td><td>16&ndash;28 semanas</td></tr>
<tr><td>Campana con aire de reposición</td><td>$90,000&ndash;$320,000 por equipo</td><td>&mdash;</td></tr>
</tbody></table></div>
<p>Dos notas de programa. El equipo de cocina tiene plazos de entrega largos hacia Quintana Roo y el local se construye para modelos concretos, así que la lista de equipo se firma antes de cerrar instalaciones. Y en plaza o edificio con vecinos operando, el trabajo ruidoso va en ventanas acordadas: alarga el calendario y conserva la relación con el arrendador.</p>
"""),
]

C[("de","blog-de/restaurant-bar-bau-riviera-maya.html")] = [
("Was über die Machbarkeit eines Lokals entscheidet", """
<p>Drei Punkte entscheiden, ob ein Konzept in eine bestimmte Fläche passt &mdash; und alle drei gehören geklärt, <strong>bevor der Mietvertrag unterschrieben wird</strong>:</p>
<ul>
<li><strong>Der Abluftweg.</strong> Eine Gewerbeküche braucht einen Kanal mit Ausblas über Dach und eine Zuluft, die ihn ausgleicht. Hat das Gebäude keinen Weg, oder genehmigt ihn die Eigentümergemeinschaft nicht, passt das Konzept zu keinem Preis in diese Fläche. Das ist der häufigste K.-o.-Punkt und an einem Nachmittag prüfbar.</li>
<li><strong>Fett und Entwässerung.</strong> Fettabscheider nach geplanter Gästezahl, mit Wartungszugang, und eine Entwässerungsleistung, die die vorhandene Decke tatsächlich hergibt. Neue Gefälle in eine fertige Decke zu schneiden ist teuer und manchmal statisch ausgeschlossen.</li>
<li><strong>Personenzahl und Fluchtwege.</strong> Der Zivilschutz berechnet die Belegung aus der Bestuhlung, und diese Zahl bestimmt Fluchtwegbreiten, Wegstrecken, Sicherheitsbeleuchtung und Evakuierungsplan. Eine dichtere Bestuhlung kann das überschreiten, was die vorhandenen Ausgänge tragen &mdash; deshalb wird der Grundriss gegen die Belegungsrechnung abgestimmt, nicht danach.</li>
</ul>
"""),
("Genehmigungen laufen parallel zum Bau", """
<p>Die Betriebsgenehmigung für Gastronomie, die Alkoholkonzession mit ihren ortsabhängigen Einschränkungen und die hygienerechtlichen Vorgaben, die Oberflächen, Handwaschbecken und Kühlkette bestimmen. Bei einer Strandterrasse kommt die Bundesküstenzone hinzu: Bevor auf der Sandseite irgendetwas geplant wird, muss feststehen, wo das Grundstück endet.</p>
<p>Das Verfahren dauert häufig länger als der Bau und startet deshalb zuerst. Entscheidend ist nicht, wann der Ausbau fertig ist, sondern wann Sie öffnen dürfen.</p>
"""),
("Kosten und Bauzeiten 2026", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Umfang</th><th>MXN/m²</th><th>Bauzeit</th></tr></thead><tbody>
<tr><td>Café oder Schnellgastronomie: Küche, Abluft, Installationen</td><td>$18.000&ndash;$35.000</td><td>10&ndash;16 Wochen</td></tr>
<tr><td>Vollrestaurant mit Bar</td><td>$25.000&ndash;$55.000</td><td>12&ndash;20 Wochen</td></tr>
<tr><td>Beachclub oder große Terrasse</td><td>$30.000&ndash;$60.000+</td><td>16&ndash;28 Wochen</td></tr>
<tr><td>Abzugshaube mit Zuluft</td><td>$90.000&ndash;$320.000 je Anlage</td><td>&mdash;</td></tr>
</tbody></table></div>
<p>Zwei Terminhinweise: Küchentechnik hat lange Lieferzeiten nach Quintana Roo und die Räume werden für konkrete Modelle gebaut, also wird die Geräteliste vor Schließen der Installationen freigegeben. Und in einem Center oder Gebäude mit laufendem Betrieb liegen laute Arbeiten in abgestimmten Zeitfenstern &mdash; das verlängert den Plan und erhält das Verhältnis zum Vermieter.</p>
"""),
]

C[("ru","blog-ru/stroitelstvo-restoranov-barov-riviera-maya.html")] = [
("Что решает, подойдёт ли помещение под ресторан", """
<p>Три вещи определяют жизнеспособность ещё до выбора отделки, и все три решаются <strong>до подписания аренды</strong>:</p>
<ul>
<li><strong>Маршрут вытяжки.</strong> Профессиональной кухне нужен воздуховод с выбросом на уровне кровли и приточный воздух, который его компенсирует. Если в здании такого маршрута нет или кондоминиум его не разрешает, концепция не помещается в это помещение ни за какие деньги. Это самая частая причина срыва проекта, и проверяется она за один вечер.</li>
<li><strong>Жир и канализация.</strong> Жироуловитель по расчётному числу посадочных мест, с доступом для обслуживания, и пропускная способность стоков, которую реально даёт существующая плита. Нарезать новые уклоны в готовой плите дорого, а иногда невозможно конструктивно.</li>
<li><strong>Вместимость и эвакуация.</strong> Гражданская защита считает вместимость по расстановке мебели, и эта цифра задаёт ширину выходов, длину путей эвакуации, аварийное освещение и план эвакуации. Более плотная посадка может превысить то, что выдерживают существующие выходы, — поэтому планировка согласуется против расчёта вместимости, а не после него.</li>
</ul>
"""),
("Лицензии идут параллельно стройке", """
<p>Лицензия на деятельность для общепита, разрешение на алкоголь там, где оно применимо, со своими ограничениями по расположению, и санитарные требования, которые задают отделку, размещение раковин и холодовую цепь. На террасе у моря добавляется федеральная морская зона: прежде чем чертить что-либо со стороны пляжа, нужно знать, где заканчивается участок.</p>
<p>Оформление обычно дольше самой стройки и поэтому запускается первым. Значение имеет не дата окончания работ, а дата, когда вам разрешат открыться.</p>
"""),
("Реальные цены и сроки 2026", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Объём</th><th>MXN/м²</th><th>Срок работ</th></tr></thead><tbody>
<tr><td>Кофейня или быстрое питание: кухня, вытяжка, инженерия</td><td>$18,000&ndash;$35,000</td><td>10&ndash;16 недель</td></tr>
<tr><td>Полноценный ресторан с баром</td><td>$25,000&ndash;$55,000</td><td>12&ndash;20 недель</td></tr>
<tr><td>Пляжный клуб или большая терраса</td><td>$30,000&ndash;$60,000+</td><td>16&ndash;28 недель</td></tr>
<tr><td>Зонт с приточной компенсацией</td><td>$90,000&ndash;$320,000 за установку</td><td>&mdash;</td></tr>
</tbody></table></div>
<p>Два замечания по графику. У кухонного оборудования длинные сроки поставки в Кинтана-Роо, а помещение строится под конкретные модели, поэтому список оборудования подписывается до закрытия инженерии. И в торговом центре или здании с работающими соседями шумные работы идут в согласованные окна — это удлиняет календарь и сохраняет отношения с арендодателем.</p>
"""),
]

C[("zh","blog-zh/canting-jiudian-jianshe-riviera-maya.html")] = [
("决定一个铺面能否做餐厅的三件事", """
<p>在挑选任何饰面之前，有三件事决定项目是否可行，而且都应当在<strong>签租约之前</strong>弄清楚：</p>
<ul>
<li><strong>排烟路径。</strong>商用厨房需要一条通往屋面排放的风管，并配套补风保持平衡。如果楼体没有这条路径，或者业主委员会不允许，那么无论预算多少，这个业态都装不进这个铺面。这是项目最常见的致命点，而查清楚只需要一个下午。</li>
<li><strong>油脂与排水。</strong>按计划座位数确定的隔油池，并留出维护通道；排水能力必须是现有楼板真正能承受的。在已完成的楼板上重新开凿坡度既昂贵，有时在结构上也不可行。</li>
<li><strong>容纳人数与疏散。</strong>民防部门按座位布置计算容纳人数，这个数字决定疏散宽度、疏散距离、应急照明和疏散预案。更密集的座位可能超出现有出口的承载能力，因此平面布置要对着容纳人数计算来定，而不是事后再调。</li>
</ul>
"""),
("许可与施工并行推进", """
<p>餐饮业态的经营许可、适用情况下的酒类许可（各地限制不同），以及决定饰面、洗手盆位置与冷链配置的卫生要求。若是海边露台，还要加上联邦海域区：在沙滩一侧动笔之前，必须先确认产权到底止于何处。</p>
<p>手续通常比施工更耗时，因此要先启动。真正重要的日期不是装修完工的时间，而是获准开业的时间。</p>
"""),
("2026年真实造价与工期", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>范围</th><th>比索/平米</th><th>施工周期</th></tr></thead><tbody>
<tr><td>咖啡馆或快餐：厨房、排烟、机电</td><td>$18,000&ndash;$35,000</td><td>10&ndash;16 周</td></tr>
<tr><td>含吧台的完整餐厅</td><td>$25,000&ndash;$55,000</td><td>12&ndash;20 周</td></tr>
<tr><td>海滩俱乐部或大型露台</td><td>$30,000&ndash;$60,000+</td><td>16&ndash;28 周</td></tr>
<tr><td>带补风的抽油烟系统</td><td>每套 $90,000&ndash;$320,000</td><td>&mdash;</td></tr>
</tbody></table></div>
<p>两点工期提醒：厨房设备运抵金塔纳罗奥的交期很长，而房间是按具体型号建造的，因此设备清单要在机电封闭前定稿。在有营业邻居的商场或楼宇内，噪声作业安排在约定时段——这会拉长工期，但能保住与业主方的关系。</p>
"""),
]


# --- FF&E for rental properties -----------------------------------------------
C[("es","blog-es/muebles-ffe-propiedades-renta-riviera-maya.html")] = [
("Amueblar para renta no es amueblar una casa", """
<p>El mobiliario de una propiedad en renta trabaja mucho más duro que el de una casa: rotación semanal, huéspedes que no son dueños, sal, humedad y sol. Lo que decide el resultado no es el estilo sino tres criterios prácticos:</p>
<ul>
<li><strong>Telas de desempeño o piel</strong> en todo lo que se sienta. El algodón y el lino sin tratar se manchan con bronceador en la primera temporada.</li>
<li><strong>Estructuras de madera dura o aluminio con recubrimiento</strong> en exteriores. El ratán barato dura una temporada y se ve mal en la foto mucho antes de romperse.</li>
<li><strong>Piezas reemplazables y estandarizadas.</strong> Un modelo de silla, un modelo de lámpara, un color de pintura. Con refacciones en bodega, el administrador resuelve el mismo día en lugar de buscar un artículo descontinuado.</li>
</ul>
"""),
("Qué presupuestar y dónde no ahorrar", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Concepto</th><th>MXN</th></tr></thead><tbody>
<tr><td>Paquete FF&amp;E villa de 3 recámaras</td><td>$450,000&ndash;$1,200,000</td></tr>
<tr><td>Reposición anual (reserva recomendada)</td><td>3&ndash;5% del ingreso bruto</td></tr>
<tr><td>Colchones con protector, por recámara</td><td>$12,000&ndash;$35,000</td></tr>
<tr><td>Comedor exterior 6 personas, madera dura</td><td>$55,000&ndash;$120,000</td></tr>
</tbody></table></div>
<p>Lo que no conviene recortar: colchones, aire acondicionado y la iluminación de la terraza. Son las tres cosas que aparecen en las reseñas. Lo que sí se puede recortar sin costo en tarifa: electrodomésticos de alta gama que el huésped no usará, y decoración frágil que se rompe y se fotografía rota.</p>
"""),
]
C[("de","blog-de/moebel-ffe-mietobjekte-riviera-maya.html")] = [
("Für Vermietung möblieren ist etwas anderes", """
<p>Möbel in einem Mietobjekt arbeiten härter als in einem Privathaus: wöchentlicher Wechsel, Gäste ohne Eigentümerinteresse, Salz, Feuchte und Sonne. Über das Ergebnis entscheidet nicht der Stil, sondern drei praktische Kriterien:</p>
<ul>
<li><strong>Performance-Stoffe oder Leder</strong> überall dort, wo gesessen wird. Unbehandelte Baumwolle und Leinen sind nach der ersten Saison von Sonnencreme gezeichnet.</li>
<li><strong>Hartholz- oder beschichtete Aluminiumgestelle</strong> im Außenbereich. Billiges Rattan h&auml;lt eine Saison und sieht auf dem Foto lange vorher schlecht aus.</li>
<li><strong>Austauschbare, standardisierte Teile.</strong> Ein Stuhlmodell, ein Leuchtenmodell, eine Wandfarbe. Mit Ersatz im Lager l&ouml;st die Verwaltung ein Problem am selben Tag, statt ein abgek&uuml;ndigtes Teil zu suchen.</li>
</ul>
"""),
("Budget und wo nicht gespart wird", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Position</th><th>MXN</th></tr></thead><tbody>
<tr><td>FF&amp;E-Paket, Villa mit 3 Schlafzimmern</td><td>$450.000&ndash;$1.200.000</td></tr>
<tr><td>J&auml;hrlicher Ersatz (empfohlene R&uuml;cklage)</td><td>3&ndash;5% des Bruttoertrags</td></tr>
<tr><td>Matratzen mit Schoner, je Schlafzimmer</td><td>$12.000&ndash;$35.000</td></tr>
<tr><td>Au&szlig;enesstisch f&uuml;r 6, Hartholz</td><td>$55.000&ndash;$120.000</td></tr>
</tbody></table></div>
<p>Nicht sparen sollte man an Matratzen, Klimaanlage und Terrassenbeleuchtung &mdash; genau diese drei tauchen in Bewertungen auf. Sparen kann man dagegen ohne Ratenverlust bei hochwertigen Ger&auml;ten, die G&auml;ste nie benutzen, und bei zerbrechlicher Dekoration, die kaputtgeht und kaputt fotografiert wird.</p>
"""),
]
C[("ru","blog-ru/mebel-ffe-arendnaya-nedvizhimost-riviera-maya.html")] = [
("Обставлять под аренду — не то же самое, что под себя", """
<p>Мебель в арендной вилле работает намного жёстче, чем в частном доме: смена гостей каждую неделю, люди без чувства собственности, соль, влажность и солнце. Результат определяет не стиль, а три практических критерия:</p>
<ul>
<li><strong>Износостойкие ткани или кожа</strong> везде, где сидят. Необработанные хлопок и лён покрываются пятнами от солнцезащитного крема за первый же сезон.</li>
<li><strong>Каркасы из плотной древесины или алюминия с покрытием</strong> на улице. Дешёвый ротанг живёт один сезон, а на фотографиях выглядит плохо задолго до того, как сломается.</li>
<li><strong>Заменяемые и стандартизованные позиции.</strong> Одна модель стула, одна модель светильника, один цвет краски. С запасом на складе управляющий решает вопрос в тот же день, а не ищет снятую с производства позицию.</li>
</ul>
"""),
("Бюджет и статьи, на которых нельзя экономить", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Статья</th><th>MXN</th></tr></thead><tbody>
<tr><td>Комплект FF&amp;E для виллы с 3 спальнями</td><td>$450,000&ndash;$1,200,000</td></tr>
<tr><td>Ежегодная замена (рекомендуемый резерв)</td><td>3&ndash;5% валовой выручки</td></tr>
<tr><td>Матрасы с наматрасником, на спальню</td><td>$12,000&ndash;$35,000</td></tr>
<tr><td>Уличный обеденный комплект на 6 человек</td><td>$55,000&ndash;$120,000</td></tr>
</tbody></table></div>
<p>Экономить нельзя на матрасах, кондиционерах и освещении террасы — именно эти три пункта попадают в отзывы. Экономить можно без потери ставки на технике премиум-класса, которой гость не воспользуется, и на хрупком декоре, который ломается и в таком виде попадает на фото.</p>
"""),
]
C[("zh","blog-zh/jiaju-ffe-chuzu-fangchan-riviera-maya.html")] = [
("为出租配家具，和为自住配家具不是一回事", """
<p>出租物业里的家具比自住房辛苦得多：每周换客、住客没有主人心态，再加上盐分、潮气和日晒。决定成败的不是风格，而是三条实际标准：</p>
<ul>
<li><strong>耐用性面料或真皮</strong>，凡是坐的地方都用。未经处理的棉麻第一个季节就会被防晒霜留下污渍。</li>
<li><strong>硬木或带涂层铝制框架</strong>用于户外。廉价藤制品只能撑一季，而在拍照上更早就不好看。</li>
<li><strong>可替换、标准化的单品。</strong>一款椅子、一款灯具、一种墙漆颜色。库房里备着替换件，管家当天就能解决问题，而不是去找早已停产的型号。</li>
</ul>
"""),
("预算与不能省的地方", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>项目</th><th>比索</th></tr></thead><tbody>
<tr><td>三卧别墅 FF&amp;E 整套</td><td>$450,000&ndash;$1,200,000</td></tr>
<tr><td>年度更换（建议计提）</td><td>毛收入的 3&ndash;5%</td></tr>
<tr><td>床垫含保护垫，每间卧室</td><td>$12,000&ndash;$35,000</td></tr>
<tr><td>六人户外餐桌椅，硬木</td><td>$55,000&ndash;$120,000</td></tr>
</tbody></table></div>
<p>不能省的是床垫、空调和露台照明——评价里出现的正是这三项。可以省而不影响房价的，是住客根本不会用的高端家电，以及易碎的装饰品：它们会坏，而且会以损坏的样子被拍进照片。</p>
"""),
]

# --- green building materials ---------------------------------------------------
C[("es","blog-es/materiales-construccion-ecologicos-mexico.html")] = [
("Qué funciona de verdad en clima tropical", """
<p>Mucho de lo que se vende como construcción ecológica está pensado para climas secos y fracasa aquí. Lo que sí resiste 80% de humedad, sal y termitas:</p>
<ul>
<li><strong>Chukum y cales locales:</strong> acabado transpirable de origen regional, que envejece bien y no atrapa humedad detrás como una pintura plástica.</li>
<li><strong>Maderas duras regionales</strong> &mdash; tzalam, chechén, machiche &mdash; con resistencia natural a termitas, frente a maderas importadas que exigen tratamiento permanente.</li>
<li><strong>Piedra caliza de la zona:</strong> cero flete largo, comportamiento térmico conocido y disponibilidad real.</li>
<li><strong>Concreto con sustitución parcial de cemento:</strong> menos huella y, con mezclas más densas, mejor comportamiento frente a cloruros.</li>
</ul>
<p>Lo que no funciona: tablaroca en zonas húmedas, bambú sin tratamiento serio, y pinturas selladoras que impiden que el muro seque.</p>
"""),
("Lo que baja el consumo más que cualquier material", """
<p>En esta costa el aire acondicionado domina el recibo de CFE, así que la decisión ambiental con más impacto no es el material sino la orientación: eje largo este&ndash;oeste, sombra profunda sobre el vidrio poniente y ventilación cruzada. Después vienen el vidrio laminado con baja emisividad, el aislamiento en losa de azotea &mdash; casi siempre ausente y la mejora de confort más barata &mdash; y la captación de agua de lluvia, que con 1,200 mm anuales sobre 200 m² de techo es un volumen real.</p>
<p>Solar cierra la lista: si el consumo ya llegó a tarifa DAC, el retorno típico baja a tres a cinco años.</p>
"""),
]
C[("de","blog-de/oekologische-baumaterialien-mexiko.html")] = [
("Was im tropischen Klima wirklich funktioniert", """
<p>Vieles, was als &ouml;kologisches Bauen verkauft wird, ist f&uuml;r trockene Klimazonen gedacht und versagt hier. Was 80% Luftfeuchte, Salz und Termiten standh&auml;lt:</p>
<ul>
<li><strong>Chukum und lokale Kalkputze:</strong> diffusionsoffene, regional gewonnene Oberfl&auml;chen, die gut altern und keine Feuchte hinter sich einschlie&szlig;en wie ein Kunststoffanstrich.</li>
<li><strong>Regionale Harth&ouml;lzer</strong> &mdash; Tzalam, Chechén, Machiche &mdash; mit nat&uuml;rlicher Termitenresistenz, statt Importholz mit Dauerbehandlung.</li>
<li><strong>Kalkstein aus der Region:</strong> kein langer Transport, bekanntes thermisches Verhalten, reale Verf&uuml;gbarkeit.</li>
<li><strong>Beton mit teilweisem Zementersatz:</strong> geringerer Fu&szlig;abdruck und, bei dichteren Mischungen, besseres Verhalten gegen&uuml;ber Chloriden.</li>
</ul>
<p>Was nicht funktioniert: Trockenbau in Feuchtbereichen, unbehandelter Bambus und sperrende Anstriche, die das Austrocknen der Wand verhindern.</p>
"""),
("Was den Verbrauch stärker senkt als jedes Material", """
<p>An dieser K&uuml;ste dominiert die Klimaanlage die CFE-Rechnung. Die wirksamste &ouml;kologische Entscheidung ist deshalb kein Material, sondern die Ausrichtung: Langseite Ost&ndash;West, tiefe Verschattung der Westverglasung und Querl&uuml;ftung. Danach kommen Verbundglas mit niedrigem Emissionsgrad, D&auml;mmung der Dachdecke &mdash; fast immer nicht vorhanden und die g&uuml;nstigste Komfortverbesserung &uuml;berhaupt &mdash; und Regenwassernutzung, die bei 1.200 mm Jahresniederschlag auf 200 m² Dach ein reales Volumen ergibt.</p>
<p>Solar schlie&szlig;t die Liste ab: Liegt der Verbrauch bereits im DAC-Tarif, sinkt die Amortisation typischerweise auf drei bis f&uuml;nf Jahre.</p>
"""),
]
C[("ru","blog-ru/ekologichnye-stroitelnye-materialy-meksika.html")] = [
("Что действительно работает в тропиках", """
<p>Многое из того, что продаётся как экологичное строительство, придумано для сухого климата и здесь не выдерживает. Что реально держит 80% влажности, соль и термитов:</p>
<ul>
<li><strong>Чукум и местные известковые составы:</strong> паропроницаемая отделка регионального происхождения, которая хорошо стареет и не запирает влагу за собой, как пластиковая краска.</li>
<li><strong>Местные плотные породы</strong> — цалам, чечен, мачиче — с природной стойкостью к термитам, в отличие от импортной древесины, требующей постоянной обработки.</li>
<li><strong>Местный известняк:</strong> без дальней доставки, с понятным тепловым поведением и реальной доступностью.</li>
<li><strong>Бетон с частичной заменой цемента:</strong> меньше следа, а при более плотных смесях — лучше поведение под воздействием хлоридов.</li>
</ul>
<p>Что не работает: гипсокартон во влажных зонах, необработанный бамбук и запирающие краски, не дающие стене высыхать.</p>
"""),
("Что снижает потребление сильнее любого материала", """
<p>На этом побережье счёт CFE определяет кондиционирование, поэтому самое действенное экологическое решение — не материал, а ориентация: длинная ось восток—запад, глубокая тень над западным остеклением и сквозное проветривание. Дальше идут триплекс с низкоэмиссионным покрытием, утепление кровельной плиты — его почти никогда нет, а это самое дешёвое улучшение комфорта — и сбор дождевой воды: при 1200 мм осадков в год на 200 м² кровли это реальный объём.</p>
<p>Замыкают список солнечные панели: если потребление уже вышло на тариф DAC, окупаемость обычно падает до трёх-пяти лет.</p>
"""),
]
C[("zh","blog-zh/huanbao-jiancai-moxige.html")] = [
("在热带气候下真正管用的做法", """
<p>许多以"绿色建筑"名义推销的做法是为干燥气候设计的，在这里并不成立。能扛住80%湿度、盐分和白蚁的是这些：</p>
<ul>
<li><strong>Chukum 与本地石灰材料：</strong>本地取材的透气饰面，老化得体，不会像塑性涂料那样把潮气封在墙体里。</li>
<li><strong>本地硬木</strong>——tzalam、chechén、machiche——天然抗白蚁，优于需要长期维护处理的进口木材。</li>
<li><strong>本地石灰岩：</strong>没有长途运输，热工性能已知，供应真实可靠。</li>
<li><strong>部分替代水泥的混凝土：</strong>碳足迹更低，而且更密实的配比在抗氯离子方面表现更好。</li>
</ul>
<p>不管用的是：潮湿区域用石膏板、未经认真处理的竹材，以及阻碍墙体干燥的封闭型涂料。</p>
"""),
("比任何材料都更能降低能耗的事", """
<p>在这段海岸，空调主导电费账单，因此最有效的环保决定不是材料而是朝向：长轴东西向、西向玻璃做深遮阳、组织穿堂通风。其次是低辐射夹胶玻璃、屋面板保温——这一项几乎总是缺失，也是最便宜的舒适度提升——以及雨水收集：年降水1200毫米落在200平米屋面上是实打实的水量。</p>
<p>最后才是光伏：如果用电量已经进入 DAC 高耗电费率，回本期通常缩短到三到五年。</p>
"""),
]


# --- condo development ----------------------------------------------------------
C[("es","blog-es/desarrollo-condominios-riviera-maya.html")] = [
("Los tres números que definen el edificio", """
<p>Un edificio de condominios se diseña hacia atrás desde tres límites, y los tres se confirman antes de dibujar:</p>
<ul>
<li><strong>Estacionamiento.</strong> El cajón por unidad que exige el municipio y si caben a nivel o hay que ir a estructura. En la mayoría de los predios del corredor es el estacionamiento &mdash; no el CUS &mdash; lo que topa el número de unidades, y el cajón estructurado cambia la viabilidad del esquema completo.</li>
<li><strong>Densidad y CUS.</strong> La densidad limita unidades con independencia de la superficie construible. Dos predios con el mismo CUS pueden permitir distinto número de departamentos.</li>
<li><strong>Umbral de altura.</strong> A partir de cierta altura el edificio adquiere elevador, requisitos de evacuación más estrictos y otra solución estructural. Cruzar esa línea por un nivel puede costar más de lo que ese nivel produce.</li>
</ul>
"""),
("Mezcla de unidades, preventa y régimen", """
<p>La mezcla define el ingreso. En este corredor los departamentos de una y dos recámaras se absorben más rápido, mientras que un número reducido de unidades grandes con terraza sostiene el tope de precio. Una amenidad en azotea &mdash; alberca, terraza, área sombreada &mdash; sube el precio de todas las unidades y no solo del último piso; suele ser el mejor retorno por metro construido del edificio.</p>
<p>La preventa financia la obra en la mayoría de los desarrollos pequeños de la zona, y el comprador y su abogado van a pedir los permisos y el borrador del régimen de condominio: eso existe antes de salir a vender, no después. Y si la propuesta es renta vacacional, el reglamento debe permitirla de forma expresa, con un umbral de modificación lo bastante alto para que una asamblea posterior no la revierta.</p>
"""),
]
C[("de","blog-de/eigentumswohnung-bau-riviera-maya.html")] = [
("Die drei Zahlen, die das Gebäude bestimmen", """
<p>Ein Eigentumswohnungsbau wird von drei Grenzwerten her entworfen, und alle drei stehen vor dem ersten Strich fest:</p>
<ul>
<li><strong>Stellpl&auml;tze.</strong> Der Schl&uuml;ssel je Wohnung und die Frage, ob die Pl&auml;tze ebenerdig passen oder eine Parkkonstruktion n&ouml;tig wird. Auf den meisten Grundst&uuml;cken des Korridors begrenzt der Stellplatzschl&uuml;ssel &mdash; nicht der CUS &mdash; die Wohnungszahl, und ein Platz in der Konstruktion ver&auml;ndert die Wirtschaftlichkeit des ganzen Projekts.</li>
<li><strong>Dichte und CUS.</strong> Die Dichte begrenzt die Einheiten unabh&auml;ngig von der zul&auml;ssigen Geschossfl&auml;che. Zwei Grundst&uuml;cke mit gleichem CUS k&ouml;nnen unterschiedlich viele Wohnungen zulassen.</li>
<li><strong>H&ouml;hengrenze.</strong> Ab einer bestimmten H&ouml;he kommen Aufzug, sch&auml;rfere Rettungsweganforderungen und eine andere Tragwerksl&ouml;sung hinzu. Diese Linie um ein Geschoss zu &uuml;berschreiten kann mehr kosten, als das Geschoss einbringt.</li>
</ul>
"""),
("Wohnungsmix, Vorverkauf und Teilungserklärung", """
<p>Der Mix bestimmt den Ertrag. In diesem Korridor werden Ein- und Zweizimmerwohnungen am schnellsten absorbiert, w&auml;hrend wenige gro&szlig;e Einheiten mit Terrasse die Preisspitze tragen. Eine Dachnutzung &mdash; Pool, Terrasse, beschatteter Bereich &mdash; hebt den Preis aller Wohnungen und nicht nur des obersten Geschosses; sie ist meist die beste Rendite je gebautem Quadratmeter.</p>
<p>Der Vorverkauf finanziert in den meisten kleinen Projekten der Region den Bau, und K&auml;ufer und ihre Anw&auml;lte verlangen Genehmigungen und den Entwurf der Teilungserkl&auml;rung: beides existiert vor dem Vertriebsstart, nicht danach. Soll Kurzzeitvermietung Teil des Angebots sein, muss die Hausordnung sie ausdr&uuml;cklich erlauben &mdash; mit einer &Auml;nderungsh&uuml;rde, die hoch genug ist, damit eine sp&auml;tere Versammlung sie nicht kippt.</p>
"""),
]
C[("ru","blog-ru/stroitelstvo-kondominiumov-riviera-maya.html")] = [
("Три числа, которые определяют здание", """
<p>Кондоминиум проектируется от трёх ограничений, и все три выясняются до первой линии на чертеже:</p>
<ul>
<li><strong>Парковка.</strong> Норматив машиномест на квартиру и то, помещаются ли они на уровне земли или нужен паркинг в конструкции. На большинстве участков коридора именно парковка, а не CUS, ограничивает число квартир, а машиноместо в конструкции меняет экономику всей схемы.</li>
<li><strong>Плотность и CUS.</strong> Плотность ограничивает количество единиц независимо от разрешённой площади. Два участка с одинаковым CUS могут допускать разное число квартир.</li>
<li><strong>Порог высоты.</strong> Выше определённой отметки появляются лифт, более жёсткие требования к эвакуации и другое конструктивное решение. Перешагнуть эту черту на один этаж может стоить дороже, чем этот этаж принесёт.</li>
</ul>
"""),
("Состав квартир, предпродажи и режим", """
<p>Состав определяет выручку. В этом коридоре быстрее всего расходятся одно- и двухкомнатные, а верхнюю планку цены держит небольшое число крупных квартир с террасой. Кровельная амениция — бассейн, терраса, затенённая зона — поднимает цену всех квартир, а не только последнего этажа, и обычно даёт лучшую отдачу на построенный метр во всём здании.</p>
<p>Предпродажи финансируют стройку в большинстве небольших проектов региона, и покупатель с юристом попросят разрешения и проект режима кондоминиума: они существуют до выхода в продажу, а не после. Если продаётся именно арендная модель, регламент должен разрешать краткосрочную аренду прямо, с порогом изменения достаточно высоким, чтобы позднее собрание её не отменило.</p>
"""),
]
C[("zh","blog-zh/gongyukaifa-riviera-maya.html")] = [
("决定这栋楼的三个数字", """
<p>公寓楼是从三个限制倒推着设计的，而且三个都要在动笔之前确认：</p>
<ul>
<li><strong>停车位。</strong>市政规定的每户车位数，以及这些车位能否在地面解决，还是必须做结构式停车。走廊上的多数地块，真正限制户数的是停车位而非 CUS，而结构式车位会改变整个方案的可行性。</li>
<li><strong>密度与 CUS。</strong>密度独立于可建面积限制户数。CUS 相同的两块地，允许的户数可能完全不同。</li>
<li><strong>高度门槛。</strong>超过一定高度，楼栋就要配电梯、执行更严的疏散要求，并换一套结构方案。为了多一层而越过这条线，代价常常高于这一层带来的收益。</li>
</ul>
"""),
("户型配比、预售与产权制度", """
<p>户型配比决定收入。在这条走廊上，一居和两居去化最快，而少量带露台的大户型撑起价格上限。屋顶配套——泳池、露台、遮阴区——抬升的是所有户型的价格，而不只是顶层，通常是全楼每平米回报最高的投入。</p>
<p>本地多数小型开发靠预售为施工融资，买方及其律师会索要许可文件和公寓产权制度草案：这些要在开盘前就存在，而不是之后补。如果卖点本身就是短租收益，规约必须明确允许短租，并把修改门槛设得足够高，使日后的业主大会无法轻易推翻。</p>
"""),
]

# --- gated community ------------------------------------------------------------
C[("es","blog-es/construccion-fraccionamientos-riviera-maya.html")] = [
("La infraestructura que se construye antes de las casas", """
<p>En un fraccionamiento las casas son la parte visible y rara vez la difícil. Lo que decide si el proyecto funciona es la infraestructura común: se construye primero, se financia antes de vender una sola unidad y después se mantiene o se entrega bajo reglas que conviene escribir desde el inicio.</p>
<ul>
<li><strong>Agua y drenaje.</strong> Sin red municipal, planta de tratamiento dimensionada para la ocupación final &mdash; no para la primera etapa &mdash; con su campo de absorción y un régimen de mantenimiento documentado. Ajustarla al presupuesto de la etapa uno es el error que obliga a una segunda planta después.</li>
<li><strong>Electricidad.</strong> Distribución interior, capacidad de transformación para el número final de lotes y alumbrado. La extensión de CFE hasta el predio se cotiza antes de comprar la tierra: en un terreno sin servicio puede rebasar seis cifras y cambiar el modelo financiero completo.</li>
<li><strong>Vialidades, drenaje pluvial y caseta.</strong> Pavimento, manejo de escurrimientos en suelo kárstico que no puede descargar al vecino, control de acceso, barda y el acceso de servicio que mantiene las entregas fuera de la circulación de residentes.</li>
</ul>
"""),
("Régimen, cuota y etapas", """
<p>La capa legal corre en paralelo: el régimen que separa lotes privados de áreas comunes, los indivisos, el reglamento que decide si se permite renta vacacional y un fondo de reserva escrito desde el principio en lugar de dejarlo a una asamblea futura. Las amenidades &mdash; alberca, casa club, gimnasio, paisajismo &mdash; son lo que vende lotes y también lo que fija la cuota que pagará cada propietario: se diseñan contra una cuota que el mercado acepte, no contra el render.</p>
<p>Y las etapas importan: cada una debe funcionar de forma independiente, con acceso de obra de las siguientes separado de quienes ya viven ahí.</p>
"""),
]
C[("de","blog-de/wohnanlage-bau-riviera-maya.html")] = [
("Die Infrastruktur, die vor den Häusern entsteht", """
<p>In einer geschlossenen Wohnanlage sind die H&auml;user der sichtbare und selten der schwierige Teil. &Uuml;ber den Erfolg entscheidet die gemeinsame Infrastruktur: sie wird zuerst gebaut, vor dem Verkauf der ersten Einheit finanziert und danach nach Regeln unterhalten, die von Anfang an feststehen sollten.</p>
<ul>
<li><strong>Wasser und Abwasser.</strong> Ohne st&auml;dtisches Netz eine Kl&auml;ranlage f&uuml;r die Endbelegung &mdash; nicht f&uuml;r die erste Bauphase &mdash; samt Sickerfeld und dokumentiertem Wartungsregime. Sie auf das Budget der ersten Phase zu k&uuml;rzen ist der Fehler, der sp&auml;ter eine zweite Anlage erzwingt.</li>
<li><strong>Strom.</strong> Verteilung innerhalb der Anlage, Trafoleistung f&uuml;r die endg&uuml;ltige Parzellenzahl und Stra&szlig;enbeleuchtung. Die CFE-Erweiterung bis zum Grundst&uuml;ck wird vor dem Landkauf beziffert: auf unerschlossenem Gel&auml;nde kann sie sechsstellig werden und das gesamte Modell ver&auml;ndern.</li>
<li><strong>Stra&szlig;en, Regenwasser und Pf&ouml;rtnerhaus.</strong> Belag, Ableitung auf Karstboden, die nicht beim Nachbarn enden darf, Zugangskontrolle, Einfriedung und ein Lieferzugang, der Anlieferungen aus dem Bewohnerverkehr h&auml;lt.</li>
</ul>
"""),
("Teilungserklärung, Umlage und Bauabschnitte", """
<p>Die rechtliche Ebene l&auml;uft parallel: die Teilung in private Parzellen und Gemeinschaftseigentum, die Anteile, die Hausordnung mit der Frage der Kurzzeitvermietung und eine von Beginn an festgeschriebene Instandhaltungsr&uuml;cklage statt einer sp&auml;teren Versammlungsentscheidung. Die Annehmlichkeiten &mdash; Pool, Clubhaus, Fitness, Bepflanzung &mdash; verkaufen die Parzellen und bestimmen zugleich die Umlage, die jeder k&uuml;nftige Eigent&uuml;mer zahlt: sie werden gegen eine markttaugliche Umlage geplant, nicht gegen das Rendering.</p>
<p>Auch die Abschnitte z&auml;hlen: jeder muss eigenst&auml;ndig funktionieren, mit Baustellenzufahrt f&uuml;r sp&auml;tere Phasen getrennt von denen, die bereits dort wohnen.</p>
"""),
]
C[("ru","blog-ru/stroitelstvo-zakrytyh-poselkov-riviera-maya.html")] = [
("Инфраструктура, которая строится до домов", """
<p>В закрытом посёлке дома — видимая часть и редко самая сложная. Успех определяет общая инфраструктура: она строится первой, финансируется до продажи первой единицы и потом обслуживается по правилам, которые лучше написать с самого начала.</p>
<ul>
<li><strong>Вода и канализация.</strong> Без городской сети — очистные, рассчитанные на итоговую заселённость, а не на первую очередь, с полем фильтрации и документированным регламентом обслуживания. Подогнать их под бюджет первой очереди — ошибка, из-за которой позже придётся строить вторые.</li>
<li><strong>Электричество.</strong> Внутренняя распределительная сеть, трансформаторная мощность на итоговое число участков и уличное освещение. Расширение сети CFE до участка считается до покупки земли: на необеспеченном наделе оно может уйти за шестизначную сумму и переписать всю финансовую модель.</li>
<li><strong>Дороги, ливнёвка и КПП.</strong> Покрытие, отвод стоков на карсте, который нельзя сбрасывать соседу, контроль доступа, ограждение и служебный въезд, уводящий доставку с маршрута жителей.</li>
</ul>
"""),
("Режим, взнос и очереди", """
<p>Юридический слой идёт параллельно: режим, разделяющий частные участки и общее имущество, доли, регламент с решением по краткосрочной аренде и резервный фонд, прописанный сразу, а не оставленный будущему собранию. Инфраструктура досуга — бассейн, клубный дом, спортзал, озеленение — продаёт участки и одновременно задаёт взнос, который будет платить каждый владелец: её проектируют под взнос, приемлемый для рынка, а не под визуализацию.</p>
<p>Очереди тоже важны: каждая должна работать самостоятельно, а строительный доступ к следующим — быть отделён от тех, кто уже живёт.</p>
"""),
]
C[("zh","blog-zh/fengbi-shequ-jianshe-riviera-maya.html")] = [
("在房子之前先建的基础设施", """
<p>在封闭社区里，房子是看得见的部分，却很少是难的部分。决定项目成败的是公共基础设施：它最先施工，在卖出第一套之前就要出钱，之后还要按一套最好在开头就写清楚的规则来维护或移交。</p>
<ul>
<li><strong>给水与污水。</strong>没有市政管网时，污水处理站要按最终入住规模设计，而不是按一期，并配渗滤场和有据可查的维护制度。为迁就一期预算而缩小规模，正是日后不得不再建第二套的原因。</li>
<li><strong>供电。</strong>社区内部配电、按最终地块数确定的变压器容量，以及路灯。接到红线的 CFE 线路延伸要在买地之前询价：在未通电的地块上，它可能达到六位数，足以改写整个财务模型。</li>
<li><strong>道路、雨水与门岗。</strong>路面做法、喀斯特地面上不能排给邻地的雨水处理、门禁、围界，以及把送货与住户动线分开的服务入口。</li>
</ul>
"""),
("产权制度、物业费与分期", """
<p>法律层面同步推进：划分私有地块与共有部分的制度、份额比例、决定能否短租的规约，以及一开始就写入的维修储备金，而不是留给日后的业主大会。配套——泳池、会所、健身房、景观——既是卖地块的卖点，也决定了每位业主日后要交的物业费：它们要对着市场能接受的费率来设计，而不是对着效果图。</p>
<p>分期同样重要：每一期都必须能独立运转，后续各期的施工通道要与已入住的住户彻底分开。</p>
"""),
]


# --- terrain preparation & retaining walls --------------------------------------
C[("es","blog-es/preparacion-terreno-muros-contencion-riviera-maya.html")] = [
("Preparar terreno sobre roca caliza", """
<p>Aquí el movimiento de tierras no es mover tierra: es cortar roca. La caliza de la península se excava con martillo hidráulico o con corte, no con pala, y eso cambia rendimientos, tiempos y precio. Lo que define el costo de esta partida:</p>
<ul>
<li><strong>Profundidad de roca sana</strong> y si hay sascab &mdash; caliza blanda &mdash; o roca dura desde el primer metro.</li>
<li><strong>Cavidades.</strong> El karst es soluble: un sondeo puede dar excelente capacidad de carga y otro a dos metros encontrar un hueco relleno de material suelto. Por eso los sondeos se hacen sobre la huella real y no en el centro del lote.</li>
<li><strong>Retiro de material.</strong> La roca extraída pesa y su acarreo es una partida en sí misma; parte puede triturarse y reutilizarse en plataformas, lo que baja el costo si se planea antes.</li>
</ul>
"""),
("Muros de contención: cuándo y de qué", """
<p>En terreno con pendiente o desnivel entre predios, el muro no es decoración estructural sino la pieza que sostiene la plataforma. Tres soluciones habituales y cuándo usarlas:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Tipo</th><th>Cuándo</th><th>MXN/m²</th></tr></thead><tbody>
<tr><td>Mampostería de piedra local</td><td>Alturas bajas, buen drenaje, estética regional</td><td>$2,200&ndash;$4,500</td></tr>
<tr><td>Concreto armado en voladizo</td><td>Alturas medias y empujes definidos</td><td>$3,500&ndash;$7,000</td></tr>
<tr><td>Muro anclado o con contrafuertes</td><td>Alturas mayores o sobrecarga de edificación</td><td>Se diseña caso por caso</td></tr>
</tbody></table></div>
<p>El punto que más veces falla no es el muro sino el drenaje detrás de él: sin filtro y lloraderos, la presión del agua en temporada de lluvias empuja lo que el cálculo estructural no contempló. Un muro sin drenaje es un muro con fecha de caducidad.</p>
"""),
]
C[("ru","blog-ru/podgotovka-uchastka-podpornye-steny-riviera-maya.html")] = [
("Подготовка участка на известняке", """
<p>Здесь земляные работы — это не перемещение грунта, а резка камня. Известняк полуострова разрабатывают гидромолотом или пилой, а не лопатой, и это меняет выработку, сроки и цену. Что определяет стоимость этой статьи:</p>
<ul>
<li><strong>Глубина залегания прочной породы</strong> и наличие саскаба — мягкого известняка — против твёрдой породы с первого метра.</li>
<li><strong>Полости.</strong> Карст растворим: одна скважина даёт отличную несущую способность, а другая в двух метрах упирается в пустоту, заполненную рыхлым материалом. Поэтому скважины бурят по фактическому пятну застройки, а не в центре участка.</li>
<li><strong>Вывоз материала.</strong> Выбранная порода тяжёлая, и её вывоз — отдельная статья; часть можно дробить и использовать в основаниях площадок, что снижает затраты при заблаговременном планировании.</li>
</ul>
"""),
("Подпорные стены: когда и из чего", """
<p>На склоне или при перепаде между участками стена — не декоративный элемент, а конструкция, удерживающая площадку. Три обычных решения и когда их применять:</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Тип</th><th>Когда</th><th>MXN/м²</th></tr></thead><tbody>
<tr><td>Кладка из местного камня</td><td>Малые высоты, хороший дренаж, региональная эстетика</td><td>$2,200&ndash;$4,500</td></tr>
<tr><td>Железобетонная консольная</td><td>Средние высоты и понятные нагрузки</td><td>$3,500&ndash;$7,000</td></tr>
<tr><td>С анкерами или контрфорсами</td><td>Большие высоты или пригрузка от здания</td><td>Проектируется индивидуально</td></tr>
</tbody></table></div>
<p>Чаще всего подводит не сама стена, а дренаж за ней: без фильтрующего слоя и водовыпусков давление воды в сезон дождей создаёт нагрузку, которой не было в расчёте. Стена без дренажа — это стена со сроком годности.</p>
"""),
]
C[("zh","blog-zh/changdi-zhunbei-dangtuqiang-riviera-maya.html")] = [
("在石灰岩上做场地准备", """
<p>这里的土方不是搬土，而是破岩。半岛的石灰岩要用液压破碎锤或切割来开挖，不是靠铲子，这改变了功效、工期和价格。决定这一项造价的是：</p>
<ul>
<li><strong>完好岩层的埋深</strong>，以及是遇到 sascab（软质石灰岩）还是从第一米就是硬岩。</li>
<li><strong>溶洞。</strong>喀斯特会被溶蚀：一个钻孔显示承载力极佳，两米外的另一个却打进被松散物填充的空腔。因此钻孔要覆盖实际建筑轮廓，而不是打在地块中心。</li>
<li><strong>弃料外运。</strong>开挖出的岩石很重，外运本身就是一项费用；其中一部分可以破碎后用于场地垫层，若提前规划就能降低成本。</li>
</ul>
"""),
("挡土墙：何时做，用什么做", """
<p>在坡地或地块间存在高差时，挡土墙不是结构装饰，而是支撑整个平台的构件。三种常见做法及其适用条件：</p>
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>类型</th><th>适用</th><th>比索/平米</th></tr></thead><tbody>
<tr><td>本地石材砌体</td><td>高度较低、排水良好、追求地域风貌</td><td>$2,200&ndash;$4,500</td></tr>
<tr><td>钢筋混凝土悬臂式</td><td>中等高度、荷载明确</td><td>$3,500&ndash;$7,000</td></tr>
<tr><td>锚固式或带扶壁</td><td>高度较大或上部有建筑荷载</td><td>逐案设计</td></tr>
</tbody></table></div>
<p>最常出问题的不是墙体本身，而是墙后的排水：没有反滤层和泄水孔，雨季的水压会施加结构计算里并未考虑的推力。没有排水的挡土墙，是一道有保质期的墙。</p>
"""),
]

# --- interior design, tropical homes -------------------------------------------
C[("es","blog-es/diseno-interiores-casas-tropicales-riviera-maya.html")] = [
("Lo que el clima le hace a un interior", """
<p>Un interior que funciona en Ciudad de México falla aquí, y siempre por lo mismo: 80% de humedad, sal en el aire y sol directo. Las decisiones que marcan la diferencia:</p>
<ul>
<li><strong>Nada de tablaroca en zonas húmedas</strong> y nada de alfombra pegada a la losa. El moho no es una posibilidad, es una cuestión de tiempo.</li>
<li><strong>Textiles de desempeño o piel,</strong> y espuma de celda cerrada en exteriores. El algodón y el lino sin tratar son una decisión que se lamenta en la segunda temporada.</li>
<li><strong>Maderas duras regionales</strong> con contenido de humedad medido &mdash; 10 a 14% &mdash; antes de fabricar. Un tablón húmedo se convierte en una mesa que se alabea.</li>
<li><strong>Herrajes 316</strong> en todo lo cercano al exterior. El acero niquelado mancha la laca blanca en dos años.</li>
</ul>
"""),
("Luz, ventilación y una casa que se cierra meses", """
<p>El interiorismo aquí empieza antes de los muebles: profundidad de aleros, orientación del vidrio y ventilación cruzada determinan si la casa se siente fresca o si se vive con el aire encendido. La iluminación cálida a 2700&ndash;3000 K, en capas y con reguladores, hace más por el resultado que cualquier pieza de decoración.</p>
<p>Y si la casa se cierra entre visitas &mdash; lo normal en segunda residencia &mdash; el diseño cambia: carcasas ventiladas, zoclos con rejilla, nada de chapa de madera, y deshumidificador con humidistato en las habitaciones cerradas. Es la diferencia entre volver a una casa fresca y volver a una casa con olor.</p>
"""),
]
C[("de","blog-de/inneneinrichtung-tropische-haeuser-riviera-maya.html")] = [
("Was das Klima mit einem Interieur macht", """
<p>Eine Einrichtung, die in Mexiko-Stadt funktioniert, versagt hier &mdash; und immer aus denselben Gr&uuml;nden: 80% Luftfeuchte, Salz in der Luft und direkte Sonne. Die Entscheidungen, die den Unterschied machen:</p>
<ul>
<li><strong>Kein Trockenbau in Feuchtbereichen</strong> und kein verklebter Teppich auf der Bodenplatte. Schimmel ist keine M&ouml;glichkeit, sondern eine Frage der Zeit.</li>
<li><strong>Performance-Textilien oder Leder</strong> und geschlossenzelliger Schaum im Au&szlig;enbereich. Unbehandelte Baumwolle und Leinen bereut man in der zweiten Saison.</li>
<li><strong>Regionale Harth&ouml;lzer</strong> mit gemessener Holzfeuchte &mdash; 10 bis 14% &mdash; vor der Fertigung. Aus einer feuchten Bohle wird ein Tisch, der sich wirft.</li>
<li><strong>316er Beschl&auml;ge</strong> &uuml;berall nahe dem Au&szlig;enbereich. Vernickelter Stahl zeichnet wei&szlig;en Lack binnen zwei Jahren.</li>
</ul>
"""),
("Licht, Lüftung und ein Haus, das monatelang zu ist", """
<p>Innenarchitektur beginnt hier vor den M&ouml;beln: Dach&uuml;berstand, Ausrichtung der Verglasung und Querl&uuml;ftung entscheiden, ob sich das Haus k&uuml;hl anf&uuml;hlt oder ob man mit laufender Klimaanlage lebt. Warmes Licht bei 2700&ndash;3000 K, in Schichten und dimmbar, tr&auml;gt mehr zum Ergebnis bei als jedes Dekorationsst&uuml;ck.</p>
<p>Und wenn das Haus zwischen den Besuchen geschlossen bleibt &mdash; bei Zweitwohnsitzen die Regel &mdash; &auml;ndert sich der Entwurf: hinterl&uuml;ftete Korpusse, Sockel mit Gitter, kein Furnier und ein hygrostatgesteuerter Entfeuchter in geschlossenen R&auml;umen. Das ist der Unterschied zwischen einem frischen Haus und einem, das riecht.</p>
"""),
]
C[("ru","blog-ru/dizajn-interyera-tropicheskie-doma-riviera-maya.html")] = [
("Что климат делает с интерьером", """
<p>Интерьер, работающий в Мехико, здесь проваливается, и всегда по одним и тем же причинам: 80% влажности, соль в воздухе и прямое солнце. Решения, которые определяют результат:</p>
<ul>
<li><strong>Никакого гипсокартона во влажных зонах</strong> и никакого ковролина, приклеенного к плите. Плесень — не вероятность, а вопрос времени.</li>
<li><strong>Износостойкий текстиль или кожа,</strong> а на улице — пена с закрытыми ячейками. Необработанные хлопок и лён — решение, о котором жалеют во втором сезоне.</li>
<li><strong>Местные плотные породы</strong> с измеренной влажностью — 10–14% — до начала изготовления. Из сырой доски получается стол, который поведёт.</li>
<li><strong>Фурнитура 316</strong> везде рядом с улицей. Никелированная сталь оставляет пятна на белом лаке за два года.</li>
</ul>
"""),
("Свет, вентиляция и дом, закрытый месяцами", """
<p>Интерьер здесь начинается до мебели: глубина свесов, ориентация остекления и сквозное проветривание решают, будет ли в доме прохладно или придётся жить с включённым кондиционером. Тёплый свет 2700–3000 K, слоями и с диммерами, даёт результату больше, чем любой предмет декора.</p>
<p>А если дом закрывается между приездами — норма для второго жилья — проект меняется: вентилируемые корпуса мебели, цоколи с решёткой, никакого шпона и осушитель с гигростатом в закрытых комнатах. Это разница между возвращением в свежий дом и возвращением в дом с запахом.</p>
"""),
]


# --- accessibility / universal design -------------------------------------------
C[("es","blog-es/accesibilidad-diseno-universal-casas-mexico.html")] = [
("Lo que cuesta nada ahora y mucho después", """
<p>Casi todo el diseño accesible es gratis en proyecto y caro en obra terminada. La lista corta, en orden de importancia:</p>
<ul>
<li><strong>Un solo nivel,</strong> o planta baja completa con recámara y baño. Si hay segundo piso, escalera cómoda con descanso, no la más angosta que permita el reglamento.</li>
<li><strong>Umbrales a nivel</strong> en todas las puertas al exterior, con canaleta de drenaje y pendiente hacia afuera para que la lluvia no entre. Es la misma solución que exige el buen detalle constructivo, así que no cuesta más.</li>
<li><strong>Puertas de 90 cm</strong> y espacio de giro en baño y cocina. Nadie se ha arrepentido nunca de una puerta ancha.</li>
<li><strong>Refuerzo en muros de baño</strong> para barras de apoyo futuras, aunque hoy no se instalen. Un tablón detrás del acabado cuesta casi nada.</li>
</ul>
"""),
("Baño, pisos y luz", """
<p>El baño se diseña una vez y bien: regadera a nivel sin escalón con drenaje lineal, WC de altura confort, llave de palanca y suficiente piso libre para asistir a alguien. Los pisos, con resistencia real al deslizamiento en mojado &mdash; el porcelánico pulido junto a la alberca es un riesgo, no un acabado.</p>
<p>La iluminación importa más de lo que parece: luz generosa y pareja, sin transiciones oscuras entre estancias, y apagadores a altura alcanzable. En una casa pensada para envejecer en ella, esos detalles valen más que cualquier metro cuadrado extra.</p>
"""),
]
C[("de","blog-de/barrierefreiheit-universelles-design-mexiko.html")] = [
("Was heute nichts kostet und später viel", """
<p>Fast alles an barrierefreiem Entwurf ist in der Planung kostenlos und im fertigen Haus teuer. Die kurze Liste, nach Wichtigkeit:</p>
<ul>
<li><strong>Eine Ebene,</strong> oder ein vollst&auml;ndiges Erdgeschoss mit Schlafzimmer und Bad. Bei zwei Geschossen eine bequeme Treppe mit Podest, nicht die schmalste zul&auml;ssige.</li>
<li><strong>Schwellenlose &Uuml;berg&auml;nge</strong> an allen Au&szlig;ent&uuml;ren, mit Rinne und Gef&auml;lle nach au&szlig;en, damit der Regen drau&szlig;en bleibt. Das ist ohnehin das richtige Detail und kostet deshalb nicht mehr.</li>
<li><strong>90-cm-T&uuml;ren</strong> und Wendefl&auml;che in Bad und K&uuml;che. Eine breite T&uuml;r hat noch niemand bereut.</li>
<li><strong>Verst&auml;rkung in den Badw&auml;nden</strong> f&uuml;r sp&auml;tere Haltegriffe, auch wenn heute keine montiert werden. Eine Platte hinter dem Belag kostet fast nichts.</li>
</ul>
"""),
("Bad, Böden und Licht", """
<p>Das Bad wird einmal richtig geplant: bodengleiche Dusche mit Linienentw&auml;sserung, WC in Komforth&ouml;he, Hebelarmatur und genug freie Fl&auml;che, um jemandem zu helfen. B&ouml;den mit echter Rutschhemmung im nassen Zustand &mdash; poliertes Feinsteinzeug am Pool ist ein Risiko, kein Belag.</p>
<p>Beleuchtung z&auml;hlt mehr, als man denkt: gro&szlig;z&uuml;gig und gleichm&auml;&szlig;ig, ohne dunkle &Uuml;berg&auml;nge zwischen R&auml;umen, mit Schaltern in erreichbarer H&ouml;he. In einem Haus, in dem man alt werden will, sind diese Details mehr wert als jeder zus&auml;tzliche Quadratmeter.</p>
"""),
]
C[("zh","blog-zh/wuzhangai-tongyong-sheji-zhuzhai-moxige.html")] = [
("现在不花钱、以后很贵的那些事", """
<p>无障碍设计几乎全部在设计阶段免费，在房子建成后昂贵。按重要性排列的简表：</p>
<ul>
<li><strong>单层布局，</strong>或者首层就有完整的卧室和卫生间。若有二层，楼梯要舒适并带休息平台，而不是取规范允许的最窄尺寸。</li>
<li><strong>所有通往室外的门做无高差门槛，</strong>配排水沟并向外找坡，让雨水留在室外。这本来就是正确的构造做法，因此并不额外花钱。</li>
<li><strong>90厘米门洞</strong>以及卫生间和厨房的回转空间。没有人会后悔门开得宽。</li>
<li><strong>卫生间墙体预埋加固</strong>，为将来的扶手做准备，即便现在不装。饰面后面加一块衬板几乎不花钱。</li>
</ul>
"""),
("卫生间、地面与照明", """
<p>卫生间一次做对：无挡水的同层淋浴配线性地漏、舒适高度坐便器、手柄式龙头，以及足够搀扶他人的净空。地面要有在潮湿状态下的真实防滑性能——泳池边用抛光瓷砖是风险，不是饰面。</p>
<p>照明比想象中更重要：光照充足均匀，房间之间没有明暗骤变，开关设在可及高度。在一栋准备住到老的房子里，这些细节比多出来的任何一平米都值钱。</p>
"""),
]

# --- plumbing & water systems ---------------------------------------------------
C[("es","blog-es/plomeria-sistemas-agua-riviera-maya.html")] = [
("Cisterna, presión y tratamiento: el orden correcto", """
<p>El suministro municipal en el corredor es intermitente en varias zonas y el agua es dura y clorada. Por eso toda casa aquí lleva sistema propio, y dimensionarlo es decisión de ingeniería, no costumbre del albañil:</p>
<ul>
<li><strong>Cisterna:</strong> mínimo dos o tres días de consumo real; más en villa de renta con alberca y ocupación completa. La cisterna corta es la queja número uno que atendemos en casas terminadas.</li>
<li><strong>Sistema de presión:</strong> hidroneumático o bomba de velocidad variable dimensionada al número de muebles y a la simultaneidad real. Tres regaderas de lluvia al mismo tiempo se diseñan, no se descubren.</li>
<li><strong>Tren de tratamiento:</strong> sedimentos, suavizador por la dureza, carbón para cloro y sabor, y ósmosis en el punto de consumo. Protege boiler, regaderas y equipo de alberca.</li>
</ul>
"""),
("Agua caliente, recirculación y lo que se descuida", """
<p>Los calentadores instantáneos de gas LP son el estándar local y funcionan bien; el solar térmico se paga rápido en este clima. En recorridos largos conviene recirculación: sin ella, un baño lejano desperdicia treinta segundos de agua en cada uso.</p>
<p>Lo que más se descuida: dejar espacio y drenaje para el cuarto de tratamiento, prever el desagüe del retrolavado, y separar el agua pluvial del drenaje sanitario. Y en casa que se cierra meses, un corte de suministro con la bomba encendida es el escenario que arruina el equipo &mdash; se resuelve con protección de marcha en seco desde el primer día.</p>
"""),
]
C[("de","blog-de/sanitaer-wassersysteme-riviera-maya.html")] = [
("Zisterne, Druck und Aufbereitung in der richtigen Reihenfolge", """
<p>Die st&auml;dtische Versorgung im Korridor ist stellenweise unterbrochen, und das Wasser ist hart und gechlort. Deshalb hat hier jedes Haus eine eigene Anlage, und ihre Dimensionierung ist eine Ingenieurentscheidung, keine Gewohnheit:</p>
<ul>
<li><strong>Zisterne:</strong> mindestens zwei bis drei Tage realen Verbrauchs, mehr bei einer Mietvilla mit Pool und Vollbelegung. Die zu kleine Zisterne ist die h&auml;ufigste Beschwerde, die wir an fertigen H&auml;usern bearbeiten.</li>
<li><strong>Druckanlage:</strong> Hauswasserwerk oder drehzahlgeregelte Pumpe, ausgelegt auf die Zahl der Entnahmestellen und die tats&auml;chliche Gleichzeitigkeit. Drei Regenduschen gleichzeitig plant man, man entdeckt sie nicht.</li>
<li><strong>Aufbereitungsstrecke:</strong> Sediment, Enth&auml;rter wegen der H&auml;rte, Aktivkohle f&uuml;r Chlor und Geschmack, Umkehrosmose an der Entnahmestelle. Das sch&uuml;tzt Durchlauferhitzer, Armaturen und Pooltechnik.</li>
</ul>
"""),
("Warmwasser, Zirkulation und das Vergessene", """
<p>Gas-Durchlauferhitzer sind hier Standard und funktionieren gut; Solarthermie amortisiert sich in diesem Klima schnell. Bei langen Leitungswegen lohnt eine Zirkulation: ohne sie verschwendet ein entferntes Bad bei jeder Nutzung drei&szlig;ig Sekunden Wasser.</p>
<p>Am h&auml;ufigsten vergessen: Platz und Ablauf f&uuml;r den Technikraum, der Ablauf der R&uuml;cksp&uuml;lung und die Trennung von Regen- und Schmutzwasser. Und in einem Haus, das monatelang leer steht, ruiniert ein Versorgungsausfall bei laufender Pumpe die Technik &mdash; ein Trockenlaufschutz von Anfang an l&ouml;st das.</p>
"""),
]
C[("zh","blog-zh/guandao-gongshui-riviera-maya.html")] = [
("蓄水池、增压与水处理：正确的顺序", """
<p>走廊上部分区域的市政供水是间断的，而且水质硬、含氯。因此这里每栋房子都有自己的系统，其规模是工程计算的结果，而不是施工习惯：</p>
<ul>
<li><strong>蓄水池：</strong>至少按两到三天的实际用水量；带泳池且满员出租的别墅要更多。容量偏小是我们在已建成住宅中处理最多的投诉。</li>
<li><strong>增压系统：</strong>气压罐或变频泵，按用水点数量和真实同时使用率选型。三个花洒同时用，是设计出来的，不是事后发现的。</li>
<li><strong>处理流程：</strong>沉淀过滤、针对硬度的软化、除氯除味的活性炭，以及饮用点的反渗透。它保护的是热水器、花洒和泳池设备。</li>
</ul>
"""),
("热水、循环与最容易被忽略的部分", """
<p>燃气即热式热水器是本地标准做法，效果不错；在这样的气候下太阳能热水回本很快。管路较长时值得做热水循环：没有循环，远端卫生间每次使用都要白放三十秒的水。</p>
<p>最常被忽略的是：给设备间留出空间和排水、预留反冲洗排水口，以及把雨水与污水分开。另外，在长期空置的房子里，供水中断而水泵仍在运行是毁设备的场景——从一开始就装防干转保护即可解决。</p>
"""),
]


# --- construction timeline ------------------------------------------------------
C[("es","blog-es/cronograma-construccion-riviera-maya.html")] = [
("Cuánto tarda de verdad, por etapa", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Etapa</th><th>Duración</th></tr></thead><tbody>
<tr><td>Uso de suelo, alineamiento y licencia</td><td>2&ndash;12 semanas según municipio</td></tr>
<tr><td>Expediente ambiental (lote con vegetación)</td><td>3&ndash;9 meses &mdash; en Tulum, el extremo alto</td></tr>
<tr><td>Mecánica de suelos y proyecto ejecutivo</td><td>6&ndash;14 semanas, en paralelo</td></tr>
<tr><td>Cimentación y estructura</td><td>3&ndash;5 meses</td></tr>
<tr><td>Instalaciones y acabados</td><td>4&ndash;7 meses</td></tr>
<tr><td>Alberca, exteriores y entrega</td><td>1&ndash;2 meses</td></tr>
</tbody></table></div>
<p>Una casa de 150 m² toma de 7 a 10 meses de obra. Lo que más varía no es la obra sino lo anterior: el trámite. De la compra al primer día de obra pueden pasar de 2 a 14 meses según el municipio y la vegetación del lote.</p>
"""),
("Lo que realmente atrasa una obra aquí", """
<ul>
<li><strong>Empezar el expediente ambiental tarde.</strong> No requiere planos finales y condiciona el diseño: arranca en anteproyecto o se paga en meses.</li>
<li><strong>Decidir acabados a mitad de obra.</strong> Cada cambio tardío mueve pedidos con plazos largos hacia Quintana Roo.</li>
<li><strong>Temporada de lluvias.</strong> Junio a octubre afecta colados, impermeabilización y exteriores; se programa alrededor, no contra ella.</li>
<li><strong>Fraccionamientos con horarios restringidos.</strong> Playacar, Corasol, Puerto Aventuras: menos horas hábiles por día es menos avance por semana, desde el día uno.</li>
<li><strong>Conexión de CFE solicitada al final.</strong> Es la causa más común de una casa terminada que no puede entregarse.</li>
</ul>
"""),
]
C[("de","blog-de/bauzeitplan-riviera-maya.html")] = [
("Wie lange es wirklich dauert, nach Phasen", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Phase</th><th>Dauer</th></tr></thead><tbody>
<tr><td>Nutzung, Fluchtlinie und Baugenehmigung</td><td>2&ndash;12 Wochen je nach Gemeinde</td></tr>
<tr><td>Umweltakte (bewachsenes Grundst&uuml;ck)</td><td>3&ndash;9 Monate &mdash; in Tulum am oberen Rand</td></tr>
<tr><td>Bodengutachten und Ausf&uuml;hrungsplanung</td><td>6&ndash;14 Wochen, parallel</td></tr>
<tr><td>Gr&uuml;ndung und Rohbau</td><td>3&ndash;5 Monate</td></tr>
<tr><td>Installationen und Ausbau</td><td>4&ndash;7 Monate</td></tr>
<tr><td>Pool, Au&szlig;enanlagen und &Uuml;bergabe</td><td>1&ndash;2 Monate</td></tr>
</tbody></table></div>
<p>Ein 150-m²-Haus braucht 7 bis 10 Monate Bauzeit. Am st&auml;rksten schwankt nicht der Bau, sondern das davor: das Verfahren. Vom Kauf bis zum ersten Bautag k&ouml;nnen je nach Gemeinde und Bewuchs 2 bis 14 Monate vergehen.</p>
"""),
("Was einen Bau hier wirklich verzögert", """
<ul>
<li><strong>Die Umweltakte zu sp&auml;t beginnen.</strong> Sie braucht keine Endpl&auml;ne und beeinflusst den Entwurf: entweder sie startet im Vorentwurf, oder sie kostet Monate.</li>
<li><strong>Ausbauentscheidungen mitten im Bau.</strong> Jede sp&auml;te &Auml;nderung verschiebt Bestellungen mit langen Lieferzeiten nach Quintana Roo.</li>
<li><strong>Regenzeit.</strong> Juni bis Oktober betrifft Betonagen, Abdichtung und Au&szlig;enanlagen; man plant darum herum, nicht dagegen.</li>
<li><strong>Anlagen mit eingeschr&auml;nkten Arbeitszeiten.</strong> Playacar, Corasol, Puerto Aventuras: weniger Stunden pro Tag sind weniger Fortschritt pro Woche, von Tag eins an.</li>
<li><strong>Der CFE-Anschluss zuletzt beantragt.</strong> Die h&auml;ufigste Ursache f&uuml;r ein fertiges Haus, das nicht &uuml;bergeben werden kann.</li>
</ul>
"""),
]
C[("ru","blog-ru/grafik-stroitelstva-riviera-maya.html")] = [
("Сколько на самом деле занимает каждый этап", """
<div class="table-responsive"><table class="table table-bordered"><thead class="table-dark"><tr><th>Этап</th><th>Срок</th></tr></thead><tbody>
<tr><td>Назначение земли, выравнивание и лицензия</td><td>2–12 недель в зависимости от муниципалитета</td></tr>
<tr><td>Экологическое досье (участок с растительностью)</td><td>3–9 месяцев — в Тулуме верхняя граница</td></tr>
<tr><td>Геология и рабочий проект</td><td>6–14 недель, параллельно</td></tr>
<tr><td>Фундамент и каркас</td><td>3–5 месяцев</td></tr>
<tr><td>Инженерия и отделка</td><td>4–7 месяцев</td></tr>
<tr><td>Бассейн, благоустройство и сдача</td><td>1–2 месяца</td></tr>
</tbody></table></div>
<p>Дом 150 м² строится 7–10 месяцев. Сильнее всего колеблется не стройка, а то, что перед ней: оформление. От покупки до первого дня работ проходит от 2 до 14 месяцев в зависимости от муниципалитета и растительности на участке.</p>
"""),
("Что реально задерживает стройку здесь", """
<ul>
<li><strong>Поздний старт экологического досье.</strong> Оно не требует финальных чертежей и влияет на проект: либо запускается на стадии эскиза, либо оплачивается месяцами.</li>
<li><strong>Выбор отделки посреди стройки.</strong> Каждое позднее изменение сдвигает заказы с длинными сроками поставки в Кинтана-Роо.</li>
<li><strong>Сезон дождей.</strong> С июня по октябрь страдают бетонирование, гидроизоляция и наружные работы; график строят вокруг сезона, а не против него.</li>
<li><strong>Посёлки с ограниченными часами работ.</strong> Плаякар, Корасоль, Пуэрто-Авентурас: меньше рабочих часов в день — меньше выработки в неделю, с первого дня.</li>
<li><strong>Заявка на подключение CFE в последний момент.</strong> Самая частая причина, по которой готовый дом нельзя сдать.</li>
</ul>
"""),
]

# --- tax benefits ---------------------------------------------------------------
C[("es","blog-es/beneficios-fiscales-construccion-mexico.html")] = [
("Por qué las facturas importan más que el descuento", """
<p>La decisión fiscal más rentable en una obra no ocurre durante la obra sino al venderla. El impuesto sobre la ganancia se calcula contra el costo comprobado de adquisición y mejoras, y lo único que comprueba una mejora es una <strong>factura electrónica a nombre del propietario de registro</strong>. Un pago en efectivo sin factura no reduce nada: años después se convierte en ganancia gravable.</p>
<p>De ahí tres reglas prácticas: obtener RFC y definir la estructura de propiedad antes del primer pago fuerte; exigir factura de obra, honorarios y materiales relevantes; y conservar el expediente completo, incluidos permisos y planos, porque respaldan el gasto.</p>
"""),
("Estructura, IVA y lo que conviene preguntar al contador", """
<p>La forma de tenencia &mdash; persona física, fideicomiso o sociedad mexicana &mdash; cambia el tratamiento de la renta, la deducibilidad y el escenario de venta. Para una casa habitación la vía normal del extranjero es el fideicomiso; para una operación de renta como negocio, la sociedad suele encajar mejor, con contabilidad y declaraciones que conlleva.</p>
<p>El IVA también depende del uso: la enajenación de casa habitación tiene un tratamiento distinto al de un inmueble comercial, y la renta de corto plazo se comporta distinto a la de largo plazo. Nada de esto se decide leyendo un blog: se define con un contador mexicano antes de firmar, porque corregirlo después cuesta mucho más que consultarlo antes.</p>
"""),
]
C[("ru","blog-ru/nalogovye-lgoty-stroitelstvo-meksika.html")] = [
("Почему счета-фактуры важнее любой льготы", """
<p>Самое выгодное налоговое решение на стройке принимается не во время стройки, а при продаже. Налог на прирост считается от подтверждённой стоимости приобретения и улучшений, а подтверждает улучшение только <strong>электронная фактура на имя собственника по документам</strong>. Оплата наличными без фактуры не уменьшает ничего: через годы она превращается в облагаемую прибыль.</p>
<p>Отсюда три практических правила: получить RFC и определить структуру владения до первого крупного платежа; требовать фактуры на работы, гонорары и значимые материалы; и хранить весь комплект документов, включая разрешения и чертежи, — они подтверждают расходы.</p>
"""),
("Структура, НДС и что спросить у бухгалтера", """
<p>Форма владения — физическое лицо, фидеикомисо или мексиканская компания — меняет режим по аренде, вычетам и сценарий продажи. Для жилого дома обычный путь для иностранца — фидеикомисо; для арендного бизнеса чаще подходит компания, но вместе с бухгалтерией и отчётностью.</p>
<p>НДС тоже зависит от назначения: продажа жилого дома облагается иначе, чем коммерческого объекта, а краткосрочная аренда ведёт себя иначе, чем долгосрочная. Ничего из этого не решается по статье в блоге: это определяется с мексиканским бухгалтером до подписания, потому что исправлять потом заметно дороже, чем спросить заранее.</p>
"""),
]

# --- foundation types -----------------------------------------------------------
C[("es","blog-es/tipos-cimentacion-riviera-maya.html")] = [
("Qué cimentación pide el suelo de la costa", """
<p>La caliza de la península suele dar excelente capacidad de carga a poca profundidad &mdash; mejor de la que espera quien viene de suelos blandos &mdash; y a la vez esconde cavidades. Por eso la elección se hace con la mecánica de suelos en la mano, no por costumbre:</p>
<ul>
<li><strong>Zapatas aisladas:</strong> lo más común cuando hay roca sana a poca profundidad y cargas moderadas. Económicas y rápidas.</li>
<li><strong>Losa de cimentación:</strong> cuando el terreno es irregular, hay relleno o se quiere repartir la carga sobre zonas con capacidad variable.</li>
<li><strong>Zapatas corridas y contratrabes:</strong> para rigidizar frente a asentamientos diferenciales y puentear zonas débiles localizadas.</li>
<li><strong>Pilas o pilotes:</strong> cuando la roca sana está profunda o hay que atravesar material suelto.</li>
</ul>
"""),
("Cavidades, nivel freático y errores caros", """
<p>Encontrar un hueco no significa no construir: significa resolverlo. Se rellena y consolida, se puentea con trabe o losa rigidizada, o se recorre la huella unos metros. Todo eso es barato comparado con descubrirlo después del colado.</p>
<p>Cerca de la costa aparece el nivel freático: excavaciones, cisternas y vasos de alberca necesitan abatimiento y revisión de flotación. Y en toda la zona, el recubrimiento de concreto en elementos expuestos se aumenta por cloruros: es la diferencia entre una cimentación que dura décadas y una con acero corroído en quince años.</p>
"""),
]
C[("ru","blog-ru/tipy-fundamentov-riviera-maya.html")] = [
("Какой фундамент требует грунт побережья", """
<p>Известняк полуострова обычно даёт отличную несущую способность на малой глубине — лучше, чем ожидают приезжие из регионов со слабыми грунтами, — и одновременно скрывает полости. Поэтому выбор делается по результатам геологии, а не по привычке:</p>
<ul>
<li><strong>Отдельные столбчатые фундаменты:</strong> самый частый вариант при прочной породе близко к поверхности и умеренных нагрузках. Экономично и быстро.</li>
<li><strong>Фундаментная плита:</strong> при неровном основании, наличии насыпного грунта или когда нагрузку нужно распределить по зонам с разной несущей способностью.</li>
<li><strong>Ленточные фундаменты с обвязочными балками:</strong> для жёсткости против неравномерных осадок и перекрытия локальных слабых участков.</li>
<li><strong>Сваи или буронабивные опоры:</strong> когда прочная порода залегает глубоко или нужно пройти рыхлый слой.</li>
</ul>
"""),
("Полости, грунтовые воды и дорогие ошибки", """
<p>Найденная полость не означает отказ от стройки — она означает решение. Её заполняют и уплотняют, перекрывают балкой или усиленной плитой либо сдвигают пятно застройки на несколько метров. Всё это дёшево по сравнению с обнаружением уже после бетонирования.</p>
<p>Ближе к побережью появляется высокий уровень грунтовых вод: котлованы, цистерны и чаши бассейнов требуют водопонижения и проверки на всплытие. А по всей зоне защитный слой бетона на открытых элементах увеличивают из-за хлоридов: это разница между фундаментом на десятилетия и арматурой, проржавевшей за пятнадцать лет.</p>
"""),
]


# --- property management --------------------------------------------------------
C[("de","blog-de/hausverwaltung-riviera-maya.html")] = [
("Was eine Verwaltung an dieser Küste wirklich leisten muss", """
<p>Hausverwaltung hei&szlig;t hier nicht Schl&uuml;ssel&uuml;bergabe, sondern Schadensverh&uuml;tung. Die teuren Ausf&auml;lle an einem leerstehenden Haus sind immer dieselben: ein Pool, der kippt, ein Klimager&auml;t, das ausf&auml;llt, ein Leck, das niemand bemerkt, und Schimmel in geschlossenen R&auml;umen.</p>
<ul>
<li><strong>W&ouml;chentliche Kontrolle mit Protokoll und Fotos,</strong> nicht nur bei gemeldeten Problemen.</li>
<li><strong>Pool und Garten unter Vertrag,</strong> mit Fernüberwachung der Pumpe &mdash; der gr&uuml;ne Pool bei Anreise ist der klassische Schaden.</li>
<li><strong>Entfeuchtung und L&uuml;ftung</strong> w&auml;hrend der Abwesenheit, plus ein Dauerstromkreis f&uuml;r Sicherheit, Internet und Poolsteuerung.</li>
<li><strong>Wartungsplan f&uuml;r Technik:</strong> Klimaanlage, Wasseraufbereitung, Notstrom &mdash; alles mit Intervallen statt auf Zuruf.</li>
</ul>
"""),
("Kosten und was im Vertrag stehen sollte", """
<p>Verwaltungskosten bewegen sich &uuml;blicherweise bei 15&ndash;25% der Bruttoeinnahmen bei Vermietung oder als Pauschale bei reiner Objektbetreuung. Dazu kommen Betriebskosten &mdash; Strom, Wasser, Pool, Garten, Reinigung &mdash; die bei einem vermieteten Objekt 25&ndash;35% des Bruttoertrags ausmachen.</p>
<p>In den Vertrag geh&ouml;ren: Berichtsintervall und -form, Reaktionszeiten bei Notf&auml;llen, Freigabegrenzen f&uuml;r Reparaturen ohne R&uuml;ckfrage, Zugriff auf Schl&uuml;ssel und Codes, und eine klare Trennung zwischen Verwaltungsleistung und beauftragten Handwerkerkosten. Ohne diese Punkte entsteht genau die Grauzone, in der Eigent&uuml;mer aus der Ferne den &Uuml;berblick verlieren.</p>
"""),
]
C[("ru","blog-ru/upravlenie-nedvizhimostyu-riviera-maya.html")] = [
("Что управление недвижимостью реально должно делать здесь", """
<p>Управление здесь — это не передача ключей, а предотвращение ущерба. Дорогие поломки в пустующем доме всегда одни и те же: позеленевший бассейн, отказавший кондиционер, незамеченная протечка и плесень в закрытых комнатах.</p>
<ul>
<li><strong>Еженедельный осмотр с протоколом и фото,</strong> а не только по обращению.</li>
<li><strong>Бассейн и сад по договору,</strong> с удалённым контролем насоса — зелёный бассейн к приезду это классический случай.</li>
<li><strong>Осушение и проветривание</strong> на время отсутствия плюс отдельная всегда включённая линия на охрану, интернет и контроллер бассейна.</li>
<li><strong>График обслуживания оборудования:</strong> кондиционеры, водоподготовка, резервное питание — по интервалам, а не по факту поломки.</li>
</ul>
"""),
("Стоимость и что должно быть в договоре", """
<p>Вознаграждение управляющего обычно составляет 15–25% валовой выручки при аренде либо фиксированную плату при простом обслуживании объекта. Сверху идут эксплуатационные расходы — электричество, вода, бассейн, сад, уборка, — которые в арендном объекте забирают 25–35% валовой выручки.</p>
<p>В договоре должны быть: периодичность и форма отчётности, время реакции на аварию, лимит расходов на ремонт без согласования, порядок доступа к ключам и кодам и чёткое разделение вознаграждения управляющего и стоимости работ подрядчиков. Без этих пунктов возникает именно та серая зона, в которой удалённый собственник теряет контроль.</p>
"""),
]

# --- two-storey house -----------------------------------------------------------
C[("de","blog-de/zweistoeckiges-haus-riviera-maya.html")] = [
("Wann sich das zweite Geschoss lohnt", """
<p>Nach oben zu bauen ist hier kein Standard, sondern eine Antwort auf bestimmte Lagen: ein schmales Grundst&uuml;ck, auf dem der COS sonst keinen Garten und keinen Pool &uuml;brig l&auml;sst; teures Bauland, das vertikal effizienter genutzt wird; eine Aussicht, die es erst im Obergeschoss gibt; oder die Trennung von Schlafr&auml;umen und Terrassenl&auml;rm.</p>
<p>Dagegen spricht: ein breites Grundst&uuml;ck mit gro&szlig;z&uuml;gigem COS, ein Budget, in dem der Aufpreis den Pool frisst, und eine H&ouml;henbegrenzung, die das zweite Geschoss gedr&uuml;ckt aussehen l&auml;sst. Bei einem Haus zum Altwerden raten wir zu einem Geschoss plus Dachterrasse.</p>
"""),
("Aufpreis, Treppe und die häufigste Schadensursache", """
<p>Ein zweigeschossiges Haus kostet pro Quadratmeter rund <strong>10&ndash;20% mehr</strong> als ein eingeschossiges gleicher Fl&auml;che: Gr&uuml;ndung f&uuml;r doppelte Last, gr&ouml;&szlig;ere St&uuml;tzen und Unterz&uuml;ge, eine komplette Zwischendecke mit eigener Schalung, l&auml;ngere Leitungswege und 1,5 bis 3 Monate mehr Bauzeit. Die Treppe verbraucht dabei 8 bis 14 m² &uuml;ber beide Ebenen.</p>
<p>Der h&auml;ufigste Schaden ist Wasser durch die Zwischendecke &mdash; aus einem Bad im Obergeschoss oder von einer Terrasse &uuml;ber Wohnraum &mdash; das als Fleck in einer fertigen Decke auftaucht. Es ist ein Abdichtungs- und Detailfehler, teuer zu finden und vollst&auml;ndig vermeidbar, wenn Nassbereiche &uuml;bereinander liegen.</p>
"""),
]
C[("ru","blog-ru/dvuhetazhnyy-dom-riviera-maya.html")] = [
("Когда второй этаж оправдан", """
<p>Строить вверх здесь не стандарт, а ответ на конкретные ситуации: узкий участок, где при заданном COS иначе не останется ни сада, ни бассейна; дорогая земля, которую вертикаль использует эффективнее; вид, который появляется только со второго этажа; или отделение спален от шума террасы.</p>
<p>Против: широкий участок со щедрым COS, бюджет, в котором надбавка съедает бассейн, и ограничение высоты, из-за которого второй этаж выходит сдавленным. Для дома, в котором планируют стареть, мы советуем один этаж плюс эксплуатируемую кровлю.</p>
"""),
("Надбавка, лестница и самая частая поломка", """
<p>Двухэтажный дом стоит примерно на <strong>10–20% дороже за квадратный метр</strong>, чем одноэтажный той же площади: фундамент под двойную нагрузку, более крупные колонны и ригели, полноценное междуэтажное перекрытие со своей опалубкой, более длинные инженерные трассы и на 1,5–3 месяца больший срок. Лестница при этом съедает 8–14 м² на двух уровнях.</p>
<p>Самая частая проблема — вода через междуэтажное перекрытие, из санузла наверху или с террасы над жилой комнатой, проявляющаяся пятном на готовом потолке. Это ошибка гидроизоляции и узлов: дорого искать и полностью предотвратимо, если мокрые зоны расположены друг над другом.</p>
"""),
]

# --- home security --------------------------------------------------------------
C[("de","blog-de/sicherheitssysteme-riviera-maya.html")] = [
("Sicherheit für ein Haus, das oft leer steht", """
<p>Der realistische Bedrohungsfall an dieser K&uuml;ste ist nicht der Einbruch bei Anwesenheit, sondern das monatelang leere Zweitwohnhaus. Was dort tats&auml;chlich hilft:</p>
<ul>
<li><strong>Perimeter zuerst:</strong> Beleuchtung mit Bewegungsmeldern, klare Sichtachsen, ein Tor, das ohne Strom &ouml;ffnet, und eine Fu&szlig;g&auml;ngerpforte.</li>
<li><strong>Kameras an den Zug&auml;ngen,</strong> lokal <em>und</em> in der Cloud aufgezeichnet &mdash; eine nur lokale Aufzeichnung verschwindet mit dem Rekorder.</li>
<li><strong>Smart Lock mit zeitlich begrenzten Codes</strong> f&uuml;r Reinigung, Poolservice und G&auml;ste, mit Protokoll.</li>
<li><strong>Netz&uuml;berwachung:</strong> Wassermelder, Pumpen&uuml;berwachung und ein Stromausfall-Alarm. Die meisten Sch&auml;den an leeren H&auml;usern sind technischer, nicht krimineller Natur.</li>
</ul>
"""),
("Was die Installation an dieser Küste verlangt", """
<p>Marine Umgebung hei&szlig;t: geschirmte, gedichtete Geh&auml;use mit Tropfschlaufen, 316er Befestigungen und Kameras mit beschichteten Komponenten. Standardware aus dem Baumarkt rostet innerhalb von zwei Jahren durch, und der Ausfall ist fast immer Wasser im Geh&auml;use, nicht die Elektronik selbst.</p>
<p>Dazu geh&ouml;rt ein &Uuml;berspannungsschutz an der Hauptverteilung: In der Regenzeit sind Blitzereignisse und Netzst&ouml;rungen Routine, und eine Alarmanlage ohne Schutz ist genau das Ger&auml;t, das als Erstes stirbt. Eine USV f&uuml;r Router, Rekorder und Alarmzentrale h&auml;lt das System &uuml;ber den Ausfall hinweg &mdash; ohne sie ist die Anlage genau dann blind, wenn der Strom weg ist.</p>
"""),
]
C[("ru","blog-ru/sistemy-bezopasnosti-doma-riviera-maya.html")] = [
("Безопасность дома, который часто пустует", """
<p>Реальный сценарий на этом побережье — не взлом при хозяевах, а второй дом, пустующий месяцами. Что действительно работает:</p>
<ul>
<li><strong>Сначала периметр:</strong> освещение с датчиками движения, открытые линии обзора, ворота, открывающиеся без электричества, и калитка.</li>
<li><strong>Камеры на входах,</strong> с записью локально <em>и</em> в облако — только локальная запись исчезает вместе с регистратором.</li>
<li><strong>Умный замок с кодами на время</strong> для уборки, обслуживания бассейна и гостей, с журналом доступа.</li>
<li><strong>Инженерный мониторинг:</strong> датчики протечки, контроль насоса и оповещение об отключении электричества. Большинство убытков в пустом доме — технические, а не криминальные.</li>
</ul>
"""),
("Чего требует монтаж на этом побережье", """
<p>Морская среда означает: экранированные герметичные корпуса с водосборными петлями на вводах, крепёж 316 и камеры с защищёнными компонентами. Обычное оборудование из строительного магазина прогнивает за два года, и отказ почти всегда вызван водой в корпусе, а не самой электроникой.</p>
<p>Сюда же относится защита от перенапряжений на вводном щите: в сезон дождей грозовые события и броски в сети — рутина, а сигнализация без защиты именно тот прибор, который умирает первым. ИБП на роутер, регистратор и панель сигнализации удерживает систему во время отключения — без него она слепнет ровно тогда, когда пропадает свет.</p>
"""),
]

# --- luxury villa, Playacar -----------------------------------------------------
C[("de","blog-de/luxusvilla-bauen-playacar.html")] = [
("Playacar baut man fast immer auf einem bebauten Grundstück", """
<p>Playacar ist praktisch voll. Fast jedes Projekt ist deshalb Abriss und Neubau, eine gro&szlig;e Sanierung oder die Bebauung eines der wenigen freien Grundst&uuml;cke. Die Entscheidung zwischen den ersten beiden f&auml;llt nach einem Gutachten, nicht nach einer Besichtigung: H&auml;user dieses Alters tragen an dieser K&uuml;ste regelm&auml;&szlig;ig chloridinduzierte Bewehrungskorrosion an Deckenr&auml;ndern, Balkonen und St&uuml;tzen.</p>
<p>Faustregel: Erreicht die Instandsetzung 25&ndash;30% der Neubaukosten, ist Abriss die bessere Wahl. Dagegen spricht nur eines &mdash; und das ernsthaft: Die Grundst&uuml;cke sind nicht ersetzbar und der alte Baumbestand ist gesch&uuml;tzt und wertvoll.</p>
"""),
("Beirat, Bäume und Preisniveau", """
<p>Der Gestaltungsbeirat pr&uuml;ft H&ouml;he, Baumasse und Abst&auml;nde &uuml;ber das gemeindliche Ma&szlig; hinaus, Dachform, Fassade, Farbe, Einfriedungen und jede Baumf&auml;llung einzeln. Reichen Sie im Vorentwurf ein, mit Baumkataster, und planen Sie mindestens eine Pr&uuml;frunde plus Kaution ein &mdash; eine ungeplante Runde ist hier die h&auml;ufigste Verz&ouml;gerung.</p>
<p>Preislich liegt Playacar rund 25% &uuml;ber dem Basisniveau von Playa del Carmen: $21.000&ndash;$26.000 MXN/m² im Standard- bis Premiumausbau, $30.000&ndash;$42.000 im Luxussegment, und $42.000&ndash;$60.000+ direkt am Strand. Der Aufschlag ist reale Arbeit &mdash; enge Stra&szlig;en, registrierte Arbeiter, begrenzte Zeiten, Baumschutz, Marine-Spezifikation &mdash; und kein Adresszuschlag.</p>
"""),
]
C[("ru","blog-ru/stroitelstvo-villy-lyuks-playacar.html")] = [
("В Плаякаре почти всегда строят на застроенном участке", """
<p>Плаякар практически заполнен. Поэтому почти каждый проект — это снос и новое строительство, крупная реконструкция или застройка одного из немногих свободных участков. Выбор между первыми двумя делается по результатам обследования, а не после осмотра: дома этого возраста на этом побережье регулярно несут хлоридную коррозию арматуры на торцах плит, балконах и колоннах.</p>
<p>Ориентир простой: если ремонт достигает 25–30% стоимости нового дома, сносить выгоднее. Против этого есть только один довод, зато серьёзный — участки невоспроизводимы, а взрослые деревья охраняются и стоят денег.</p>
"""),
("Комитет, деревья и уровень цен", """
<p>Архитектурный комитет проверяет высоту, объём и отступы строже муниципальных норм, форму кровли, фасад, цвет, ограждения и каждое дерево к вырубке отдельно. Подавайте на стадии эскиза вместе с дендропланом и закладывайте минимум один круг рассмотрения плюс залог — незапланированный круг здесь самая частая задержка.</p>
<p>По цене Плаякар примерно на 25% выше базового уровня Плая-дель-Кармен: $21,000–$26,000 MXN/м² при отделке от стандартной до премиум, $30,000–$42,000 в люкс-сегменте и $42,000–$60,000+ на первой линии. Надбавка — это реальная работа: узкие улицы, регистрация рабочих, ограниченные часы, защита деревьев, морская спецификация, — а не наценка за адрес.</p>
"""),
]


if __name__ == '__main__':
    keys = sorted(C)
    if len(sys.argv) > 1:
        keys = [k for k in keys if k[0] in sys.argv[1:] or k[1] in sys.argv[1:]]
    for lang, path in keys:
        n = fill(lang, path, C[(lang, path)])
        if n is None:
            continue
        print('  %5d  %s' % (n, path))
