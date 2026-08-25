#!/usr/bin/env python3
"""Inbound links into the four new service clusters.

The clusters link among themselves and to their type pages, but a cluster that only
links to itself is invisible: Google reaches it from the sitemap, finds nothing
pointing at it from a page with standing, and files it under "discovered, not
indexed" — which is where 274 URLs on this site already are.

So each cluster gets links from the pages that already rank or already hold weight:

  baños        <- /remodelacion-riviera-maya/, /remodelacion-casas-<city>/
  cocinas      <- /remodelacion-cocina-playa-del-carmen/, /carpinteria-y-herreria-*/
  carpintería  <- /carpinteria-y-herreria-*/, /deck-de-madera/, /pergola-de-madera/,
                  /casas-de-madera/
  infinity     <- /construccion-albercas/, /albercas-<city>/, /albercas-de-lujo-*/

Idempotent: run it twice and nothing changes.
"""
import os, glob

MARK = 'data-cluster="servicios"'

CITIES = ['cancun', 'playa-del-carmen', 'tulum', 'puerto-morelos', 'puerto-aventuras',
          'akumal', 'cozumel', 'isla-mujeres', 'bacalar']
NAMES = {'cancun': 'Cancún', 'playa-del-carmen': 'Playa del Carmen', 'tulum': 'Tulum',
         'puerto-morelos': 'Puerto Morelos', 'puerto-aventuras': 'Puerto Aventuras',
         'akumal': 'Akumal', 'cozumel': 'Cozumel', 'isla-mujeres': 'Isla Mujeres',
         'bacalar': 'Bacalar'}


def row(heading, pairs):
    return ('<section %s class="py-4 bg-light"><div class="container"><h2 class="h5 mb-3">%s</h2>'
            '<p class="mb-0">%s</p></div></section>\n'
            % (MARK, heading, ' · '.join('<a href="%s">%s</a>' % p for p in pairs)))


def insert(path, block, mark):
    """Add the block above the footer unless this page already carries it.

    The guard is the block's own first href, not the shared data-cluster marker: a
    page can legitimately take two different cluster rows (the carpentry page wants
    both the kitchens row and the carpentry row), so keying on the marker would let
    the first block block the second.
    """
    if not os.path.exists(path):
        return False
    src = open(path, encoding='utf-8').read()
    if mark in src:
        return False
    i = src.rfind('<footer')
    if i < 0:
        return False
    open(path, 'w', encoding='utf-8').write(src[:i] + block + src[i:])
    return True


BANOS = row('Remodelación de baños por ciudad',
            [('/remodelacion-de-banos/', 'Precios y proceso')] +
            [('/remodelacion-banos-%s/' % c, NAMES[c]) for c in CITIES])
COCINAS = row('Cocinas integrales por ciudad',
              [('/cocinas-de-madera/', 'Cocinas de madera')] +
              [('/cocinas-integrales-%s/' % c, NAMES[c]) for c in CITIES])
CARP = row('Carpintería a medida por ciudad',
           [('/closets-a-medida/', 'Clósets a medida'), ('/puertas-de-madera/', 'Puertas de madera')] +
           [('/carpinteria-%s/' % c, NAMES[c]) for c in CITIES])
INFI = row('Albercas infinity por ciudad',
           [('/albercas-infinity/', 'Precios y sistema')] +
           [('/albercas-infinity-%s/' % c, NAMES[c]) for c in CITIES])


TARGETS = [
    (BANOS, ['remodelacion-riviera-maya/index.html'] +
            ['remodelacion-casas-%s/index.html' % c for c in CITIES] +
            ['remodelacion-condominios-puerto-aventuras/index.html']),
    (COCINAS, ['remodelacion-cocina-playa-del-carmen/index.html',
               'carpinteria-y-herreria-playa-del-carmen/index.html']),
    (CARP, ['carpinteria-y-herreria-playa-del-carmen/index.html',
            'deck-de-madera/index.html', 'pergola-de-madera/index.html',
            'casas-de-madera/index.html']),
    (INFI, ['construccion-albercas/index.html', 'albercas-de-lujo-playa-del-carmen/index.html',
            'cuanto-cuesta-una-alberca/index.html'] +
           ['albercas-%s/index.html' % c for c in CITIES]),
]


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for block, paths in TARGETS:
        head = block.split('<h2 class="h5 mb-3">')[1].split('</h2>')[0]
        # a page may take more than one block, so key the guard on the first link
        n = sum(1 for p in paths if insert(p, block, mark=block.split('href="')[1].split('"')[0]))
        print('%-38s %d pages linked' % (head, n))
