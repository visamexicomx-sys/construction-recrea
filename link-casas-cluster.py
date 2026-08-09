#!/usr/bin/env python3
"""Re-injects the intra-cluster links that the page generators do not emit.

The generators rewrite whole pages, so anything injected afterwards is lost on the
next run. This script is idempotent and rebuilds it from the generator data:
  - every town page lists its premium zones (and the island pages)
  - every zone page links back to its parent town's zone list

Run it after any of gen-construccion-casas*.py / gen-casas-*.py.
"""
import importlib.util, os, re, sys

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); sys.modules[name] = m
    spec.loader.exec_module(m); return m

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
z1 = load('gen-casas-zonas.py', 'z1')
z2 = load('gen-casas-zonas2.py', 'z2')
z3 = load('gen-casas-zonas3.py', 'z3')
z4 = load('gen-casas-zonas4.py', 'z4')
il = load('gen-casas-islas.py', 'il')

LANGS = ['es', 'en', 'ru', 'de', 'fr', 'zh']
PREFIX = {'es': 'construccion-de-casas', 'en': 'house-construction', 'ru': 'stroitelstvo-domov',
          'de': 'hausbau', 'fr': 'construction-de-maisons', 'zh': 'zhuzhai-jianzao'}
LEAD_ZONES = {'es': 'Zonas premium: ', 'en': 'Premium zones: ', 'ru': 'Премиальные зоны: ',
              'de': 'Premium-Lagen: ', 'fr': 'Zones premium : ', 'zh': '高端片区：'}
LEAD_ISLES = {'es': 'Islas: ', 'en': 'Islands: ', 'ru': 'Острова: ',
              'de': 'Inseln: ', 'fr': 'Îles : ', 'zh': '岛屿：'}
BACK = {'es': 'Ver todas las zonas de %s', 'en': 'See every zone in %s', 'ru': 'Все зоны: %s',
        'de': 'Alle Lagen in %s', 'fr': 'Toutes les zones de %s', 'zh': '查看%s的全部片区'}
# town name in a neutral form per language (H1 wording differs too much to parse)
TOWN_NAME = {
 'playa-del-carmen': {'es': 'Playa del Carmen', 'en': 'Playa del Carmen', 'ru': 'Плая-дель-Кармен',
                      'de': 'Playa del Carmen', 'fr': 'Playa del Carmen', 'zh': '普拉亚德尔卡门'},
 'cancun': {'es': 'Cancún', 'en': 'Cancún', 'ru': 'Канкун', 'de': 'Cancún', 'fr': 'Cancún', 'zh': '坎昆'},
 'tulum': {'es': 'Tulum', 'en': 'Tulum', 'ru': 'Тулум', 'de': 'Tulum', 'fr': 'Tulum', 'zh': '图卢姆'},
}

# zone key -> (parent town, {lang: display name}, {lang: full slug})
ZONES = {}
for mod, zdict, names in [(z1, z1.ZONE, z1.ZNAME), (z2, z2.ZONE2, None), (z3, z3.ZONE3, None), (z4, z4.ZONE4, None)]:
    for z, d in zdict.items():
        nm = {l: (names[l][z] if names else mod.NAMES[z][l]) for l in LANGS}
        ZONES[z] = (d['parent'], nm, {l: '%s-%s' % (PREFIX[l], z) for l in LANGS})
ISLES = {z: (d['parent'], {l: il.NAMES[z][l] for l in LANGS}, {l: il.SLUGS[l][z] for l in LANGS})
         for z, d in il.ISLAS.items()}

# short label for the island links (they are villa+hotel pages, not house pages)
ISLE_LABEL = {'es': 'Villas y hoteles en %s', 'en': 'Villas and hotels in %s', 'ru': 'Виллы и отели — %s',
              'de': 'Villen und Hotels auf %s', 'fr': 'Villas et hôtels à %s', 'zh': '%s别墅与酒店'}

MARK_ZONES = 'data-cluster="zones"'
MARK_BACK = 'data-cluster="back"'


def strip_marked(html, mark):
    return re.sub(r'<p %s>.*?</p>\n?' % mark, '', html, flags=re.S)


def insert_after_table(html, para):
    """Insert right before the H2 that follows the cost table."""
    t = html.find('</table>')
    pos = html.find('<h2 class="mt-4">', t if t > -1 else 0)
    if pos == -1:
        return None
    return html[:pos] + para + html[pos:]


def run():
    changed = 0
    # 1. town pages -> their zones and islands
    by_parent = {}
    for z, (parent, nm, slug) in ZONES.items():
        by_parent.setdefault(parent, []).append((z, nm, slug, False))
    for z, (parent, nm, slug) in ISLES.items():
        by_parent.setdefault(parent, []).append((z, nm, slug, True))

    for lang in LANGS:
        for parent, items in by_parent.items():
            f = '%s-%s/index.html' % (PREFIX[lang], parent)
            if not os.path.isfile(f):
                print('missing town page', f); continue
            s = strip_marked(open(f, encoding='utf-8').read(), MARK_ZONES)
            zones = [(nm[lang], slug[lang]) for z, nm, slug, isle in items if not isle]
            isles = [(ISLE_LABEL[lang] % nm[lang], slug[lang]) for z, nm, slug, isle in items if isle]
            para = ''
            if zones:
                para += '<p %s>%s%s</p>\n' % (MARK_ZONES, LEAD_ZONES[lang],
                        ' · '.join('<a href="/%s/">%s</a>' % (sl, n) for n, sl in zones))
            if isles:
                para += '<p %s>%s%s</p>\n' % (MARK_ZONES, LEAD_ISLES[lang],
                        ' · '.join('<a href="/%s/">%s</a>' % (sl, n) for n, sl in isles))
            out = insert_after_table(s, para)
            if out is None:
                print('no anchor in', f); continue
            open(f, 'w', encoding='utf-8').write(out); changed += 1

    # 2. zone/island pages -> back link to the parent town
    TOWN = {}
    for lang in LANGS:
        TOWN[lang] = {}
    for z, (parent, nm, slug) in list(ZONES.items()) + list(ISLES.items()):
        for lang in LANGS:
            f = '%s/index.html' % slug[lang]
            if not os.path.isfile(f):
                print('missing zone page', f); continue
            s = strip_marked(open(f, encoding='utf-8').read(), MARK_BACK)
            town_slug = '%s-%s' % (PREFIX[lang], parent)
            town_name = TOWN_NAME[parent][lang]
            para = '<p %s><a href="/%s/">%s</a></p>\n' % (MARK_BACK, town_slug, BACK[lang] % town_name)
            out = insert_after_table(s, para)
            if out is None:
                print('no anchor in', f); continue
            open(f, 'w', encoding='utf-8').write(out); changed += 1
    print('pages updated:', changed)


if __name__ == '__main__':
    run()
