#!/usr/bin/env python3
"""Internal links into the albercas city cluster.

gen-albercas-ciudades.py builds the seven city pages and rings them together, but a
page nothing links to is a page Google discovers from the sitemap and then declines
to index — which is exactly the state 274 URLs on this site are already in. So the
cluster gets its inbound links from the pages that already have standing:

  1. the pillar /construccion-albercas/ — each city card heading becomes the link
     to that city's page, which is the most contextual anchor available;
  2. /cuanto-cuesta-una-alberca/ and /albercas-de-lujo-playa-del-carmen/, which both
     already rank on pool queries, get a city row;
  3. every /construccion-de-casas-<city>/ page links to the pool page for the same
     city, since a house build and a pool are the same buyer.

Idempotent: run it twice and nothing changes.
"""
import os, re

CITIES = [('cancun', 'Cancún'), ('playa-del-carmen', 'Playa del Carmen'), ('tulum', 'Tulum'),
          ('puerto-morelos', 'Puerto Morelos'), ('puerto-aventuras', 'Puerto Aventuras'),
          ('akumal', 'Akumal'), ('bacalar', 'Bacalar')]

MARK = 'data-cluster="albercas"'
ROW = ('<section %s class="py-4 bg-light"><div class="container">'
       '<h2 class="h5 mb-3">Albercas por ciudad</h2><p class="mb-0">%s</p></div></section>\n'
       % (MARK, ' · '.join('<a href="/albercas-%s/">Albercas en %s</a>' % c for c in CITIES)))


def insert_before_footer(path, block):
    """Add a block just above the footer, once."""
    src = open(path, encoding='utf-8').read()
    if MARK in src:
        return False
    i = src.rfind('<footer')
    if i < 0:
        print('  no footer in %s' % path)
        return False
    open(path, 'w', encoding='utf-8').write(src[:i] + block + src[i:])
    return True


def link_pillar():
    """Turn the city card headings on the pillar into links to the city pages."""
    path = 'construccion-albercas/index.html'
    src = open(path, encoding='utf-8').read()
    out, n = src, 0
    for slug, name in CITIES:
        # the Akumal card is headed "Akumal y Puerto Morelos"; link the first name only
        pat = r'(<h3 class="h5 fw-bold">(?:<i[^>]*></i>)?)(%s)(?=<| y )' % re.escape(name)
        def sub(m):
            return '%s<a href="/albercas-%s/">%s</a>' % (m.group(1), slug, m.group(2))
        out, k = re.subn(pat, sub, out, count=1)
        n += k
    if '/albercas-cancun/' in src:
        return 0
    open(path, 'w', encoding='utf-8').write(out)
    return n


def link_house_pages():
    """/construccion-de-casas-<city>/ -> /albercas-<city>/ for the matching city."""
    done = 0
    for slug, name in CITIES:
        src_page = 'construccion-de-casas-%s/index.html' % slug
        if not os.path.exists(src_page):
            print('  no house page for %s' % slug)
            continue
        block = ('<section %s class="py-4 bg-light"><div class="container">'
                 '<h2 class="h5 mb-3">¿El proyecto lleva alberca?</h2><p class="mb-0">'
                 'Vea precios 2026, acabados y permisos en '
                 '<a href="/albercas-%s/">construcción de albercas en %s</a>.'
                 '</p></div></section>\n' % (MARK, slug, name))
        if insert_before_footer(src_page, block):
            done += 1
    return done


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print('pillar city headings linked:', link_pillar())
    for p in ('cuanto-cuesta-una-alberca/index.html',
              'albercas-de-lujo-playa-del-carmen/index.html',
              'construccion-albercas/index.html'):
        if os.path.exists(p):
            print('%-46s city row: %s' % (p, insert_before_footer(p, ROW)))
    print('house pages linked:', link_house_pages())
