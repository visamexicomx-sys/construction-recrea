#!/usr/bin/env python3
"""Rewrite title/description on the pages that rank but do not get clicked.

Picked from the GSC export of 13/08/2026 (gsc-analyze.py). Two groups:

  1. English blog — 4,097 impressions, 33 clicks, 0.8% CTR at an average
     position of 7. The Spanish twin of the same article gets 2.3%, so the
     ranking is fine and the snippet is the problem. In every case the number
     the reader is searching for was already in the body and missing from the
     title: the cost page ranked at 5.8 with "$650-$1,400/m²" in the title
     while the body said "a 150 m² house with pool: $150,000-$250,000 USD".

  2. Striking-distance pages — queries at positions 4-20 with real impressions
     and zero clicks ("licencia de construcción playa del carmen", 42 impr at
     position 5.7; "constructora en tulum", 70 impr at 18.2 against a page
     titled as a how-to-choose guide when the query is commercial).

Every figure used below is copied from the body of the page it goes on;
nothing here is invented. Run, then commit and ping IndexNow.

    python3 rewrite-titles.py [--dry-run]
"""
import html
import re
import sys

# path -> (title, description)
REWRITES = {
    # --- English blog: the number goes in the title -----------------------
    'blog/construction-costs-playa-del-carmen-2026.html': (
        'Cost to Build a House in Playa del Carmen 2026: $150k-$250k',
        'A 150 m² house with pool costs $150,000-$250,000 USD to build in Playa '
        'del Carmen in 2026. Full price table by build level, plus land and permits.',
    ),
    'blog/construction-permits-playa-del-carmen.html': (
        'Construction Permits Playa del Carmen: 4-10 Weeks, Real Costs',
        'A construction licence in Playa del Carmen takes 4-10 weeks. Land use, '
        'licence, environmental file and DRO: cost per step and what sends a file back.',
    ),
    'blog/swimming-pools-riviera-maya-cost.html': (
        'Pool Cost in Riviera Maya 2026 + What It Adds to Your Rental',
        'What a pool costs in Playa del Carmen and Tulum in 2026 by size and type, '
        'and the $20,000-$30,000 USD it adds to value, $30-$60 to nightly rates.',
    ),
    'blog/home-renovation-playa-del-carmen.html': (
        'Home Renovation in Playa del Carmen: 2026 Costs by Scope',
        'Renovation costs in Playa del Carmen 2026: price per m² by scope, pools at '
        '$250k-$500k MXN, the finishes that fail in tropical heat, where budgets break.',
    ),
    'blog/airbnb-roi-calculator-tulum-playa.html': (
        'Airbnb ROI Tulum & Playa 2026: $25k-$45k Net per Year',
        'A 2-bed with pool nets $25,000-$45,000 USD a year in Tulum. Nightly rates, '
        'occupancy and costs for 2026, and why building lifts ROI from 7-9% to 12-18%.',
    ),
    'blog/palapa-construction-guide-riviera-maya.html': (
        'Palapa Cost 2026: $80,000-$160,000 MXN for a 4x5 m Palapa',
        'A 4x5 m dining palapa costs $80,000-$160,000 MXN and lasts 15-25 years with '
        're-thatching every 5-8. Costs by size, huano vs zacate, permits, fire safety.',
    ),
    'blog/cost-build-house-tulum.html': (
        'How Much Does It Cost to Build a House in Tulum? (2026 Guide)',
        'Building in Tulum costs $12,000-$25,000 MXN/m² ($650-$1,400 USD) in 2026. '
        'Breakdown by finish level, plus land, permits and timeline from a local builder.',
    ),
    'blog/quintana-roo-environmental-construction-laws-2026.html': (
        'Quintana Roo Environmental Construction Laws 2026 Explained',
        'Quintana Roo tightened its environmental rules: projects without SEMA '
        'authorisation now face injunctions and work stoppages. What you file, and when.',
    ),
    'blog/airbnb-investment-tulum.html': (
        'Airbnb in Tulum 2026: $270k In, ~13% ROI, 7.5-Year Payback',
        'Real numbers on building an Airbnb in Tulum: ~$270,000 USD invested, ~$35,000 '
        'net income a year, ~13% cash-on-cash ROI and a 7.5-year payback.',
    ),
    'blog/build-vs-buy-riviera-maya.html': (
        'Build vs Buy in Riviera Maya: Building Saves 25-40%',
        'Building a 150 m² house in the Riviera Maya costs 25-40% less than buying the '
        'same spec, but takes 12-18 months instead of 60 days. Side-by-side comparison.',
    ),
    'blog/tulum-real-estate-market-2026.html': (
        'Tulum Real Estate 2026: 252 Projects, Demand Down 40%',
        'Tulum has 252 active construction projects and a 40% demand slowdown. Condo '
        'prices are flat to -10% while luxury villas and eco-builds still appreciate.',
    ),
    'en/index.html': (
        'Construction Company in Playa del Carmen & Tulum | Recrea',
        'Licensed builder in Playa del Carmen, Tulum and Cancún. Houses, villas and '
        'commercial builds for foreign owners: 18+ years, 196 projects, fixed price.',
    ),

    # --- Striking distance: intent match ---------------------------------
    # "licencia de construcción playa del carmen": 42 impr, pos 5.7, 0 clicks.
    # The page ranked on "permisos" and never said "licencia" in the title.
    'blog-es/permisos-construccion-playa-del-carmen.html': (
        'Permisos y Licencia de Construcción en Playa del Carmen 2026',
        'Cómo sacar la licencia de construcción en Playa del Carmen: uso de suelo, '
        'expediente ambiental y DRO, con costos reales, tiempos por paso y qué la frena.',
    ),
    # "constructora en tulum" 70 impr pos 19.5 + "constructoras en tulum" 59 impr
    # pos 18.2, both 0 clicks, against a commercial page titled as a guide.
    'constructora-tulum/index.html': (
        'Constructora en Tulum | Recrea Construcción — 18 Años de Obra',
        'Constructora en Tulum con 196 proyectos: casas, villas y hoteles boutique en '
        'Aldea Zamá, Región 15 y La Veleta. Permiso SEMA gestionado. Cotización gratis.',
    ),
    # "палапа": 35 impr, pos 7.7, 0 clicks. Price belongs in the title.
    'blog-ru/palapa-stroitelstvo-gid.html': (
        'Строительство палапы 2026: от 40 000 MXN, служит 15–25 лет',
        'Палапа 4×5 м под столовую — 80 000–160 000 MXN, срок службы 15–25 лет при '
        'смене кровли раз в 5–8 лет. Цены по размерам, уано или сакате, разрешения.',
    ),
}

# <title>, and the og:/twitter: pairs that mirror it. The og:/twitter: tags are
# optional — the older blog templates only carry og:, and Twitter falls back to
# it — so only a missing <title> or description is worth a warning.
PATTERNS = (
    ('title', True, r'(<title>)(.*?)(</title>)'),
    ('desc', True, r'(<meta name="description" content=")(.*?)(")'),
    ('title', False, r'(<meta property="og:title" content=")(.*?)(")'),
    ('desc', False, r'(<meta property="og:description" content=")(.*?)(")'),
    ('title', False, r'(<meta name="twitter:title" content=")(.*?)(")'),
    ('desc', False, r'(<meta name="twitter:description" content=")(.*?)(")'),
)


def main():
    dry = '--dry-run' in sys.argv
    changed = 0
    for path, (title, desc) in REWRITES.items():
        try:
            src = open(path, encoding='utf-8').read()
        except FileNotFoundError:
            print('MISSING %s' % path)
            continue
        new = src
        for kind, required, pat in PATTERNS:
            value = html.escape(title if kind == 'title' else desc, quote=True)
            new, n = re.subn(pat, lambda m: m.group(1) + value + m.group(3),
                             new, count=1, flags=re.S)
            if not n and required:
                print('  WARNING no %s tag in %s' % (kind, path))
        if new == src:
            continue
        print('%-58s  title %2d ch | desc %3d ch' % (path, len(title), len(desc)))
        if not dry:
            open(path, 'w', encoding='utf-8').write(new)
        changed += 1
    print('\n%d pages %s' % (changed, 'to change' if dry else 'rewritten'))
    over = [(p, len(t)) for p, (t, _) in REWRITES.items() if len(t) > 62]
    over += [(p, len(d)) for p, (_, d) in REWRITES.items() if len(d) > 162]
    for p, n in over:
        print('  WARNING too long (%d): %s' % (n, p))
    return 0


if __name__ == '__main__':
    sys.exit(main())
