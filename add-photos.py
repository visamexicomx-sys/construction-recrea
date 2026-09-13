#!/usr/bin/env python3
"""Place the photographs we already have onto pages that have none.

870 indexable pages carried no image at all — 57% of the site — on a site selling
work that is judged visually. There are only ~27 distinct photographs in img/, so
this is deliberately not "one image everywhere": each page family is matched to
the photographs that actually show that kind of work, and candidates rotate by
page order so neighbouring pages in a cluster never show the same one.

Phase A (this pass): the 150 commercial landing pages, where a photograph does
the most work. Blog articles are a separate pass.

When real project photography arrives, only PHOTOS and RULES need editing — the
placement, alt text and markup stay.
"""
import os, re, sys, glob

# name -> (width, height)  — webp is served, jpg exists as the source
PHOTOS = {
 'villa-pool-tropical': (1200, 1600), 'hurricane-shutters-pool': (1170, 640),
 'rooftop-terrace-pergola': (563, 703), 'service-carpentry': (1523, 1003),
 'service-renovation': (1600, 915), 'commercial-interior-fitout': (1280, 720),
 'commercial-building-aerial': (1280, 720), 'construction-excavator-aerial': (1280, 720),
 'commercial-corner-construction': (1600, 900), 'commercial-pemex-construction': (1280, 960),
 'gomart-finished-exterior': (1280, 960), 'project-gomart': (1270, 722),
 'commercial-glass-entrance': (1204, 1600), 'villa-luxury-night': (1080, 1339),
 'service-residential': (960, 547), 'commercial-foundation-cemex': (1280, 720),
 'playa-del-carmen-aerial': (1280, 720), 'service-commercial': (1280, 720),
 'service-electrical': (1600, 1050), 'service-metalwork': (1200, 788),
 'development-complex-aerial': (952, 624), 'concrete-slab-pouring': (1280, 720),
 'metalwork-modern-door': (736, 1094), 'project-renovation': (1600, 915),
}

# subject -> alt text per language (describes the photograph, not the page)
ALT = {
 'pool': {'es': 'Alberca de obra nueva con acabado tropical construida por Recrea en la Riviera Maya',
          'en': 'Newly built pool with tropical finish by Recrea in the Riviera Maya',
          'de': 'Neu gebauter Pool mit tropischer Ausführung von Recrea an der Riviera Maya',
          'ru': 'Новый бассейн с тропической отделкой, построенный Recrea на Ривьере Майя',
          'fr': 'Piscine neuve à finition tropicale réalisée par Recrea dans la Riviera Maya',
          'zh': 'Recrea 在里维埃拉玛雅建造的热带风格新建泳池'},
 'carpentry': {'es': 'Carpintería a medida en madera tropical fabricada en el taller de Recrea',
               'en': 'Custom tropical hardwood joinery made in the Recrea workshop',
               'de': 'Maßgefertigte Tischlerarbeit aus Tropenholz aus der Recrea-Werkstatt',
               'ru': 'Столярные изделия из тропического дерева, изготовленные в цеху Recrea',
               'fr': 'Menuiserie sur mesure en bois tropical fabriquée dans l’atelier Recrea',
               'zh': 'Recrea 自有工厂制作的热带硬木定制木作'},
 'renovation': {'es': 'Remodelación integral de interiores terminada por Recrea Construcción',
                'en': 'Completed full interior renovation by Recrea Construction',
                'de': 'Abgeschlossene Kernsanierung von Innenräumen durch Recrea',
                'ru': 'Завершённая комплексная реконструкция интерьера от Recrea',
                'fr': 'Rénovation intérieure complète achevée par Recrea',
                'zh': 'Recrea 完成的室内整体翻新工程'},
 'warehouse': {'es': 'Obra de nave industrial en la Riviera Maya ejecutada por Recrea',
               'en': 'Industrial warehouse build in the Riviera Maya by Recrea',
               'de': 'Industriehallenbau an der Riviera Maya von Recrea',
               'ru': 'Строительство промышленного склада на Ривьере Майя силами Recrea',
               'fr': 'Chantier de bâtiment industriel dans la Riviera Maya par Recrea',
               'zh': 'Recrea 在里维埃拉玛雅承建的工业厂房工程'},
 'fuel': {'es': 'Obra civil de estación de servicio ejecutada por Recrea Construcción',
          'en': 'Service station civil works delivered by Recrea Construction',
          'de': 'Tiefbau einer Tankstelle ausgeführt von Recrea',
          'ru': 'Общестроительные работы АЗС, выполненные Recrea',
          'fr': 'Travaux de génie civil de station-service réalisés par Recrea',
          'zh': 'Recrea 完成的加油站土建工程'},
 'clinic': {'es': 'Interior comercial con acabados lavables terminado por Recrea',
            'en': 'Commercial interior with washable finishes completed by Recrea',
            'de': 'Gewerbeinnenausbau mit abwaschbaren Oberflächen von Recrea',
            'ru': 'Коммерческий интерьер с моющимися покрытиями, выполненный Recrea',
            'fr': 'Intérieur commercial à finitions lavables réalisé par Recrea',
            'zh': 'Recrea 完成的可清洗饰面商业室内空间'},
 'villa': {'es': 'Villa de lujo terminada por Recrea Construcción en la Riviera Maya',
           'en': 'Luxury villa completed by Recrea Construction in the Riviera Maya',
           'de': 'Von Recrea fertiggestellte Luxusvilla an der Riviera Maya',
           'ru': 'Вилла люкс, построенная Recrea на Ривьере Майя',
           'fr': 'Villa de luxe achevée par Recrea dans la Riviera Maya',
           'zh': 'Recrea 在里维埃拉玛雅建成的豪华别墅'},
 'permits': {'es': 'Cimentación en obra con licencia de construcción vigente, proyecto de Recrea',
             'en': 'Permitted foundation works on a Recrea construction site',
             'de': 'Genehmigte Fundamentarbeiten auf einer Recrea-Baustelle',
             'ru': 'Устройство фундамента на объекте Recrea с действующим разрешением',
             'fr': 'Travaux de fondation autorisés sur un chantier Recrea',
             'zh': 'Recrea 工地上已取得许可的基础施工'},
 'commercial': {'es': 'Obra comercial terminada por Recrea en la Riviera Maya',
                'en': 'Completed commercial build by Recrea in the Riviera Maya',
                'de': 'Fertiggestellter Gewerbebau von Recrea an der Riviera Maya',
                'ru': 'Завершённый коммерческий объект Recrea на Ривьере Майя',
                'fr': 'Chantier commercial achevé par Recrea dans la Riviera Maya',
                'zh': 'Recrea 在里维埃拉玛雅完成的商业工程'},
 'electrical': {'es': 'Instalación eléctrica ejecutada por el equipo propio de Recrea',
                'en': 'Electrical installation carried out by Recrea’s in-house team',
                'de': 'Elektroinstallation durch das eigene Team von Recrea',
                'ru': 'Электромонтаж, выполненный собственной бригадой Recrea',
                'fr': 'Installation électrique réalisée par l’équipe interne de Recrea',
                'zh': 'Recrea 自有团队完成的电气安装'},
 'metalwork': {'es': 'Herrería y cancelería de aluminio fabricada por Recrea',
               'en': 'Metalwork and aluminium glazing fabricated by Recrea',
               'de': 'Metallbau und Aluminiumverglasung von Recrea',
               'ru': 'Металлоконструкции и алюминиевое остекление производства Recrea',
               'fr': 'Métallerie et menuiserie aluminium fabriquées par Recrea',
               'zh': 'Recrea 自制的金属工程与铝合金门窗'},
 'hotel': {'es': 'Desarrollo hotelero en construcción en la Riviera Maya',
           'en': 'Hotel development under construction in the Riviera Maya',
           'de': 'Hotelentwicklung im Bau an der Riviera Maya',
           'ru': 'Гостиничный комплекс в стадии строительства на Ривьере Майя',
           'fr': 'Développement hôtelier en construction dans la Riviera Maya',
           'zh': '里维埃拉玛雅在建的酒店开发项目'},
 'plans': {'es': 'Movimiento de tierras al inicio de obra en un proyecto de Recrea',
           'en': 'Earthworks at the start of a Recrea project',
           'de': 'Erdarbeiten zu Beginn eines Recrea-Projekts',
           'ru': 'Земляные работы в начале проекта Recrea',
           'fr': 'Terrassement au démarrage d’un projet Recrea',
           'zh': 'Recrea 项目开工阶段的土方作业'},
}

# (slug pattern, subject, rotating photo candidates)
RULES = [
 (r'^albercas', 'pool', ['villa-pool-tropical', 'hurricane-shutters-pool', 'rooftop-terrace-pergola']),
 (r'^(carpinteria|cocinas-integrales|closets|puertas-de-madera|cocinas-de-madera)', 'carpentry',
  ['service-carpentry', 'metalwork-modern-door']),
 (r'^(remodelacion|home-renovation)', 'renovation', ['service-renovation', 'commercial-interior-fitout', 'project-renovation']),
 (r'^construccion-naves-industriales', 'warehouse',
  ['commercial-building-aerial', 'construction-excavator-aerial', 'commercial-corner-construction']),
 (r'^construccion-remodelacion-gasolineras', 'fuel',
  ['commercial-pemex-construction', 'gomart-finished-exterior', 'project-gomart']),
 (r'^(construccion-hospitales-clinicas|hospital-clinic-construction)', 'clinic',
  ['commercial-interior-fitout', 'commercial-glass-entrance']),
 (r'^(villa-de-inversion-airbnb|airbnb-investment-villa)', 'villa',
  ['villa-luxury-night', 'villa-pool-tropical', 'service-residential']),
 (r'^(permisos-de-construccion|construction-permits)', 'permits',
  ['commercial-foundation-cemex', 'concrete-slab-pouring', 'playa-del-carmen-aerial']),
]

SERVICES = {
 'residential': ('villa', ['service-residential']), 'residencial': ('villa', ['service-residential']),
 'wohnungsbau': ('villa', ['service-residential']), 'zhilishchnoe-stroitelstvo': ('villa', ['service-residential']),
 'zhuzhai-jianshe': ('villa', ['service-residential']),
 'commercial': ('commercial', ['service-commercial']), 'comercial': ('commercial', ['service-commercial']),
 'gewerbebau': ('commercial', ['service-commercial']), 'kommercheskoe-stroitelstvo': ('commercial', ['service-commercial']),
 'shangye-jianshe': ('commercial', ['service-commercial']),
 'renovation': ('renovation', ['service-renovation']), 'remodelacion': ('renovation', ['service-renovation']),
 'renovierung': ('renovation', ['service-renovation']), 'remont': ('renovation', ['service-renovation']),
 'fanxin-zhuangxiu': ('renovation', ['service-renovation']),
 'carpentry': ('carpentry', ['service-carpentry']), 'carpinteria': ('carpentry', ['service-carpentry']),
 'schreinerei': ('carpentry', ['service-carpentry']), 'stolarnye-raboty': ('carpentry', ['service-carpentry']),
 'mugong-jiaju': ('carpentry', ['service-carpentry']),
 'electrical': ('electrical', ['service-electrical']), 'electrico': ('electrical', ['service-electrical']),
 'elektroinstallation': ('electrical', ['service-electrical']), 'elektromontazh': ('electrical', ['service-electrical']),
 'dianqi-anzhuang': ('electrical', ['service-electrical']),
 'metalwork': ('metalwork', ['service-metalwork']), 'herreria': ('metalwork', ['service-metalwork']),
 'metallbau': ('metalwork', ['service-metalwork']), 'metalloizdeliya': ('metalwork', ['service-metalwork']),
 'jinshu-gongcheng': ('metalwork', ['service-metalwork']),
 'hotels': ('hotel', ['development-complex-aerial']), 'hoteles': ('hotel', ['development-complex-aerial']),
 'hotelbau': ('hotel', ['development-complex-aerial']), 'oteli': ('hotel', ['development-complex-aerial']),
 'jiudian-jianshe': ('hotel', ['development-complex-aerial']),
 'permits': ('permits', ['commercial-foundation-cemex']), 'permisos': ('permits', ['commercial-foundation-cemex']),
 'genehmigungen': ('permits', ['commercial-foundation-cemex']), 'razresheniya': ('permits', ['commercial-foundation-cemex']),
 'xukezheng': ('permits', ['commercial-foundation-cemex']),
 'plans': ('plans', ['construction-excavator-aerial']), 'planos': ('plans', ['construction-excavator-aerial']),
 'architekturplaene': ('plans', ['construction-excavator-aerial']), 'plany': ('plans', ['construction-excavator-aerial']),
 'jianzhu-tupian': ('plans', ['construction-excavator-aerial']),
 'all-services': ('commercial', ['playa-del-carmen-aerial']), 'servicios': ('commercial', ['playa-del-carmen-aerial']),
 'dienstleistungen': ('commercial', ['playa-del-carmen-aerial']), 'uslugi': ('commercial', ['playa-del-carmen-aerial']),
 'fuwu': ('commercial', ['playa-del-carmen-aerial']), 'prestations': ('commercial', ['playa-del-carmen-aerial']),
}

CAPTION = {'es': 'Proyecto de Recrea Construcción', 'en': 'A Recrea Construction project',
           'de': 'Ein Projekt von Recrea Construction', 'ru': 'Проект Recrea Construcción',
           'fr': 'Un projet de Recrea Construction', 'zh': 'Recrea Construcción 项目'}


def figure(photo, subject, lang, depth):
    w, h = PHOTOS[photo]
    prefix = '../' * depth if depth else ''
    alt = ALT[subject].get(lang, ALT[subject]['en'])
    cap = CAPTION.get(lang, CAPTION['en'])
    return ('\n<figure class="my-4" data-photo="auto">\n'
            '<img loading="lazy" decoding="async" src="%simg/%s.webp" width="%d" height="%d" '
            'alt="%s" class="img-fluid rounded" style="max-width:100%%;height:auto">\n'
            '<figcaption class="text-muted small mt-2">%s</figcaption>\n</figure>\n'
            % (prefix, photo, w, h, alt, cap))


def target(path):
    """returns (subject, candidates) or None"""
    slug = path.split('/')[0]
    if slug == 'services':
        key = os.path.basename(path)[:-5]
        return SERVICES.get(key)
    for pat, subj, cands in RULES:
        if re.match(pat, slug):
            return subj, cands
    return None



# ---------------------------------------------------------------- Phase B: blog
ALT['market'] = {'es': 'Vista aérea del corredor de la Riviera Maya donde construye Recrea',
                 'en': 'Aerial view of the Riviera Maya corridor where Recrea builds',
                 'de': 'Luftbild des Riviera-Maya-Korridors, in dem Recrea baut',
                 'ru': 'Вид с воздуха на коридор Ривьеры Майя, где работает Recrea',
                 'fr': 'Vue aérienne du corridor de la Riviera Maya où Recrea construit',
                 'zh': 'Recrea 施工所在的里维埃拉玛雅走廊航拍'}
ALT['structure'] = {'es': 'Colado de losa en obra supervisado por el equipo de Recrea',
                    'en': 'Slab pour on site, supervised by the Recrea team',
                    'de': 'Deckenbetonage auf der Baustelle, überwacht vom Recrea-Team',
                    'ru': 'Заливка плиты на объекте под контролем команды Recrea',
                    'fr': 'Coulage de dalle sur chantier, supervisé par l’équipe Recrea',
                    'zh': 'Recrea 团队监督下的现场楼板浇筑'}

BLOG_RULES = [
 ('pool', ['villa-pool-tropical', 'hurricane-shutters-pool', 'rooftop-terrace-pergola'],
  ['pool', 'jacuzzi', 'infinity', 'alberca']),
 ('carpentry', ['service-carpentry', 'metalwork-modern-door'],
  ['carpentry', 'closet', 'wardrobe', 'cabinet', 'hardwood', 'furniture', 'kitchen', 'deck', 'pergola', 'palapa']),
 ('metalwork', ['service-metalwork', 'metalwork-modern-door'],
  ['window', 'railing', 'balcon', 'gate', 'steel', 'aluminum', 'stainless', 'ironwork', 'hurricane-proof', 'shutter']),
 ('electrical', ['service-electrical'],
  ['electrical', 'solar', 'generator', 'ev-charger', 'home-theater', 'lighting', 'utilities']),
 ('renovation', ['service-renovation', 'project-renovation', 'commercial-interior-fitout'],
  ['renovation', 'remodel', 'refurbish', 'outdoor-living']),
 ('warehouse', ['commercial-building-aerial', 'commercial-corner-construction'],
  ['warehouse', 'industrial']),
 ('clinic', ['commercial-interior-fitout', 'commercial-glass-entrance'],
  ['clinic', 'medical', 'hospital']),
 ('commercial', ['service-commercial', 'gomart-finished-exterior', 'commercial-corner-construction',
                 'commercial-glass-entrance', 'project-gomart'],
  ['commercial', 'retail', 'office', 'plaza', 'store', 'restaurant', 'coworking', 'gym', 'school', 'shop']),
 ('hotel', ['development-complex-aerial'],
  ['hotel', 'hostel', 'resort', 'glamping', 'lodge']),
 ('permits', ['commercial-foundation-cemex', 'concrete-slab-pouring'],
  ['permit', 'licen', 'land-use', 'environmental', 'regime', 'zoning', 'fideicomiso', 'closing-process']),
 ('plans', ['construction-excavator-aerial'],
  ['plans', 'rendering', 'structural', 'mep', 'floor-plan', 'soil', 'survey', 'topograph', 'design', 'engineering']),
 ('villa', ['villa-luxury-night', 'service-residential', 'villa-pool-tropical', 'residential-block-construction'],
  ['villa', 'luxury', 'penthouse', 'house', 'home', 'beachfront', 'jungle', 'minimalist', 'story', 'family',
   'retirement', 'casita', 'condo', 'apartment']),
 ('market', ['playa-del-carmen-aerial', 'development-complex-aerial'],
  ['cost', 'price', 'market', 'investment', 'invest', 'financ', 'roi', 'rent', 'airbnb', 'buy', 'guide',
   'areas', 'living', 'timeline', 'contract', 'budget']),
 ('structure', ['concrete-slab-pouring', 'commercial-foundation-cemex'],
  ['concrete', 'foundation', 'slab', 'cistern', 'waterproof', 'cenote', 'chukum', 'material']),
]

PHOTOS.setdefault('residential-block-construction', (720, 1280))
ALT.setdefault('structure', ALT['structure'])


def blog_subject(slug):
    for subj, cands, keys in BLOG_RULES:
        if any(k in slug for k in keys):
            return subj, cands
    return None


def phase_b():
    import urllib.parse
    en = sorted(f for f in glob.glob('blog/*.html') if os.path.basename(f) != 'index.html')
    order = 0
    placed = 0
    used = {}
    for f in en:
        slug = os.path.basename(f)[:-5]
        t = blog_subject(slug)
        if not t:
            continue
        subj, cands = t
        photo = cands[order % len(cands)]
        order += 1
        h = open(f, encoding='utf-8').read()
        # the whole hreflang cluster shares the topic, so it shares the photograph
        cluster = [f]
        for u in re.findall(r'<link rel="alternate" hreflang="(?!x-default)[a-z]{2}" href="([^"]+)"', h):
            rel = urllib.parse.urlparse(u).path.lstrip('/')
            if rel.endswith('.html') and os.path.exists(rel):
                cluster.append(rel)
        for p in dict.fromkeys(cluster):
            s2 = open(p, encoding='utf-8').read()
            if 'Redirecting...' in s2 or re.search(r'<img[\s>]', s2) or 'data-photo="auto"' in s2:
                continue
            m = re.search(r'<html[^>]*lang="([a-z]{2})"', s2)
            lang = m.group(1) if m else 'en'
            lead = re.search(r'<p class="lead">.*?</p>', s2, re.S)
            anchor = lead.end() if lead else None
            if anchor is None:
                m2 = re.search(r'<h1[^>]*>.*?</h1>\s*(?:<p[^>]*>.*?</p>\s*)?', s2, re.S)
                if not m2:
                    continue
                anchor = m2.end()
            fig = figure(photo, subj, lang, p.count('/'))
            open(p, 'w', encoding='utf-8').write(s2[:anchor] + fig + s2[anchor:])
            used[photo] = used.get(photo, 0) + 1
            placed += 1
    print('blog figures placed:', placed, 'across', len(used), 'photos')
    for k, v in sorted(used.items(), key=lambda x: -x[1]):
        print('  %-34s %3d' % (k, v))



# ------------------------------------------- Phase C: everything still imageless
# Keywords in all six languages, matched against the page's own slug. Most
# specific subject first; anything that still matches nothing is left alone
# rather than given a filler photograph.
MULTI = [
 ('pool', ['villa-pool-tropical', 'hurricane-shutters-pool', 'rooftop-terrace-pergola'],
  ['pool', 'alberca', 'piscin', 'бассейн', 'yongchi', 'jacuzzi']),
 ('garden', ['rooftop-terrace-pergola', 'villa-pool-tropical'],
  ['jardin', 'garden', 'garten', 'сад', 'landscap', 'paysag', 'terraza', 'terrace', 'terrasse', 'террас',
   'dachterrasse', 'roof-garden', 'wuding', 'jardim', 'paisaj', 'landshaft', 'redai-yuanlin', 'letnyaya-kuhnya']),
 ('carpentry', ['service-carpentry', 'metalwork-modern-door'],
  ['carpint', 'carpentry', 'menuiser', 'tischler', 'schreiner', 'столяр', 'mugong', 'cocina', 'kitchen',
   'küche', 'kuche', 'кухн', 'chufang', 'closet', 'wardrobe', 'schrank', 'deck', 'pergola', 'palapa',
   'madera', 'holz', 'bois', 'muebl', 'furniture', 'möbel', 'mobel', 'мебел']),
 ('metalwork', ['service-metalwork', 'metalwork-modern-door'],
  ['herrer', 'metal', 'ventana', 'window', 'fenster', 'fenetre', 'окн', 'chuang', 'baranda', 'railing',
   'geländer', 'gelaender', 'перил', 'porton', 'gate', 'tor-', 'ворот', 'acero', 'steel', 'stahl', 'сталь',
   'aluminio', 'aluminium', 'алюмин', 'persiana', 'shutter', 'huracan', 'hurricane', 'hurrikan', 'ураган']),
 ('electrical', ['service-electrical'],
  ['electr', 'elektr', 'электр', 'dianqi', 'solar', 'generador', 'generator', 'генератор', 'iluminacion',
   'lighting', 'beleuchtung', 'eclairage', 'освещен', 'zhaoming', 'domotica', 'smart', 'intelligent',
   'умны', 'automatis', 'automatiz', 'avtomatiz', 'ev-charger', 'ladestation', 'solnechnye', 'osveshchenie', 'umnyj', 'umnyy']),
 ('water', ['concrete-slab-pouring', 'commercial-foundation-cemex'],
  ['cisterna', 'cistern', 'zisterne', 'цистерн', 'septic', 'fosa', 'klaeranlage', 'klaranlage', 'септик',
   'desal', 'entsalz', 'dessal', 'sanitar', 'plomer', 'plumbing', 'water', 'agua', 'wasser', 'вод', 'eau', 'shui', 'septik', 'septiki', 'vodoprovod', 'opresneniya']),
 ('structure', ['concrete-slab-pouring', 'commercial-foundation-cemex', 'construction-excavator-aerial'],
  ['concreto', 'concrete', 'beton', 'бетон', 'cimenta', 'foundation', 'fundament', 'фундамент', 'losa',
   'slab', 'decke', 'плит', 'impermeabiliz', 'waterproof', 'abdicht', 'гидроизол', 'muro', 'mauer',
   'стен', 'terreno', 'gelaende', 'gelände', 'retaining', 'stuetzmauer', 'grieta', 'humedad', 'bodenbelag', 'microcemento', 'cemento', 'domo', 'riego', 'pozo', 'utilities', 'inspection',
   'piso', 'floor', 'pol-', 'topograf', 'topograph', 'suelo', 'soil', 'vermessung', 'cehui', 'proyecto-arquitectonico', 'bodenbelaeg', 'poly-otdelka', 'dimiancailiao', 'podgotovka-uchastka', 'podpornye', 'preparation-terrain', 'soutenement', 'changdi-zhunbei', 'dangtuqiang', 'barda']),
 ('garage', ['residential-block-construction', 'commercial-corner-construction'],
  ['garaje', 'garage', 'garagen', 'гараж', 'parking', 'estacionamiento', 'stellplatz', 'chewei', 'garazhi', 'parkovk']),
 ('renovation', ['service-renovation', 'project-renovation', 'commercial-interior-fitout'],
  ['remodel', 'renovation', 'renovier', 'ремонт', 'fanxin', 'reform', 'renovat']),
 ('clinic', ['commercial-interior-fitout', 'commercial-glass-entrance'],
  ['clinic', 'clinica', 'klinik', 'клиник', 'medic', 'hospital', 'yiliao']),
 ('hotel', ['development-complex-aerial'],
  ['hotel', 'hostel', 'resort', 'glamping', 'lodge', 'jiudian']),
 ('commercial', ['service-commercial', 'gomart-finished-exterior', 'commercial-corner-construction',
                 'commercial-glass-entrance'],
  ['comercial', 'commercial', 'gewerbe', 'коммерч', 'shangye', 'naves', 'bodegas', 'tienda', 'store', 'retail', 'laden',
   'oficina', 'office', 'büro', 'buro', 'офис', 'restaurant', 'coworking', 'gym', 'escuela', 'school']),
 ('permits', ['commercial-foundation-cemex', 'concrete-slab-pouring'],
  ['permis', 'licenc', 'licens', 'lizenz', 'genehmigung', 'разрешен', 'xukezheng', 'uso-de-suelo',
   'land-use', 'nutzung', 'ambiental', 'environmental', 'umwelt', 'эколог', 'fideicomiso', 'notari',
   'impuesto', 'tax', 'steuer', 'налог', 'dro', 'tramite', 'gestoria', 'razresheniya', 'jianzhu-xuke', 'zhizhao']),
 ('interior', ['commercial-interior-fitout', 'service-renovation'],
  ['interior', 'innenarchitekt', 'интерьер', 'decorac', 'shinei', 'ffe', 'amueblad', 'furnish']),
 ('market', ['playa-del-carmen-aerial', 'development-complex-aerial'],
  ['costo', 'cost', 'kosten', 'cout', 'стоимост', 'chengben', 'precio', 'price', 'preis', 'prix', 'цен',
   'mercado', 'market', 'markt', 'marche', 'рынок', 'inversion', 'investment', 'investit', 'инвест',
   'renta', 'rent', 'miete', 'аренд', 'airbnb', 'wertsteigerung', 'valor', 'seguro', 'insurance',
   'versicherung', 'страхов', 'administracion', 'management', 'verwaltung', 'управлен', 'guia', 'guide',
   'leitfaden', 'гид', 'checklist', 'garantia', 'garantie', 'fiscal', 'fiscaux', 'beneficios', 'nalogovye', 'plusvalia', 'plus-value', 'appreciation', 'zengzhi', 'rost-stoimosti', 'boom', 'obzor-rynka', 'train-maya', 'blanchiment', 'baoxian', 'strahovanie', 'constructora', 'construction-company', 'empresas-de-construccion', 'supervision', 'contrato', 'contract', 'presupuesto', 'budget', 'concierge', 'extranjeros', 'foreigners', 'financ', 'stalled', 'abandonada', 'closing-process', 'buying-land', 'turnkey', 'gestion-locative', 'upravlenie-nedvizhimostyu', 'wuye-guanli', 'bauunternehmen', 'choisir-entreprise', 'ruhe-xuanze', 'a-distance', 'durable', 'bezopasnost', 'jufeng', 'challenges', 'pre-sale', 'lagoon']),
 ('villa', ['villa-luxury-night', 'service-residential', 'villa-pool-tropical',
            'residential-block-construction'],
  ['villa', 'casa', 'house', 'haus', 'дом', 'zhuzhai', 'maison', 'penthouse', 'lujo', 'luxury', 'luxus',
   'люкс', 'luxe', 'playa', 'beach', 'strand', 'пляж', 'jungla', 'jungle', 'dschungel', 'джунгл',
   'minimalista', 'minimalist', 'accesibilidad', 'accessibility', 'barrierefrei', 'доступн', 'elevador',
   'elevator', 'aufzug', 'лифт', 'casita', 'condo', 'apartment', 'wohnung', 'квартир', 'residencial',
   'residential', 'ampliacion', 'clima', 'aire', 'air-conditioning', 'klimaanlage', 'lueftung', 'кондицион', 'kondicionirovanie', 'kongtiao', 'okna-dveri', 'vill-', 'bieshu', 'prefab', 'modular']),
]

SKIP = ('index.html', 'noticias', 'news', 'nachrichten', 'novosti', 'xinwen', 'actualites')


def phase_c():
    order = 0
    placed = 0
    used = {}
    files = sorted(glob.glob('blog*/*.html')) + sorted(glob.glob('*/index.html')) + ['index.html']
    for f in files:
        base = os.path.basename(f)
        slug = (f.split('/')[0] if base == 'index.html' else base[:-5]).lower()
        if base == 'index.html' and f == 'index.html':
            continue
        if any(k in f.lower() for k in SKIP) and base == 'index.html' and f.count('/') == 1:
            pass
        if base == 'index.html' and f.split('/')[0] in ('blog', 'blog-es', 'blog-de', 'blog-ru', 'blog-fr', 'blog-zh'):
            continue
        if base == 'index.html' and not os.path.exists(f):
            continue
        if any(k in slug for k in SKIP[1:]):
            continue
        h = open(f, encoding='utf-8', errors='ignore').read()
        if 'Redirecting...' in h or re.search(r'<img[\s>]', h) or 'data-photo="auto"' in h:
            continue
        hit = None
        for subj, cands, keys in MULTI:
            if any(k in slug for k in keys):
                hit = (subj, cands); break
        if not hit:
            continue
        subj, cands = hit
        photo = cands[order % len(cands)]
        order += 1
        m = re.search(r'<html[^>]*lang="([a-z]{2})"', h)
        lang = m.group(1) if m else 'es'
        lead = re.search(r'<p class="lead">.*?</p>', h, re.S)
        if lead:
            anchor = lead.end()
        else:
            m2 = re.search(r'<h1[^>]*>.*?</h1>\s*(?:<p[^>]*>.*?</p>\s*)?', h, re.S)
            if not m2:
                continue
            anchor = m2.end()
        fig = figure(photo, subj, lang, f.count('/'))
        open(f, 'w', encoding='utf-8').write(h[:anchor] + fig + h[anchor:])
        used[photo] = used.get(photo, 0) + 1
        placed += 1
    print('phase C figures placed:', placed, 'across', len(used), 'photos')


ALT.setdefault('garden', ALT['pool'])
ALT.setdefault('water', ALT['structure'])
ALT.setdefault('garage', ALT['villa'])
ALT.setdefault('interior', ALT['renovation'])


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(glob.glob('*/index.html')) + sorted(glob.glob('services/*.html'))
    done = collections = 0
    used = {}
    order = 0
    for f in files:
        h = open(f, encoding='utf-8').read()
        if 'Redirecting...' in h or re.search(r'<img[\s>]', h) or 'data-photo="auto"' in h:
            continue
        t = target(f)
        if not t:
            continue
        subj, cands = t
        m = re.search(r'<html[^>]*lang="([a-z]{2})"', h)
        lang = m.group(1) if m else 'es'
        photo = cands[order % len(cands)]
        order += 1
        depth = f.count('/')
        fig = figure(photo, subj, lang, depth)
        lead = re.search(r'<p class="lead">.*?</p>', h, re.S)
        if not lead:
            continue
        h = h[:lead.end()] + fig + h[lead.end():]
        open(f, 'w', encoding='utf-8').write(h)
        used[photo] = used.get(photo, 0) + 1
        done += 1
    print('figures placed:', done)
    for k, v in sorted(used.items(), key=lambda x: -x[1]):
        print('  %-32s %3d' % (k, v))
    if 'blog' in sys.argv:
        phase_b()
    if 'rest' in sys.argv:
        phase_c()
