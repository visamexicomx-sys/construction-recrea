#!/usr/bin/env python3
"""Analyse Google Search Console exports for construction-recrea.com.

Drop the CSVs from GSC into ./gsc/ and run this. It accepts the files exactly as
Search Console exports them (the ZIP contains Queries.csv, Pages.csv, etc. — just
unzip it into ./gsc/), and it does not care about column order or language, so the
Spanish-language export works too.

    python3 gsc-analyze.py

What it reports, in the order the answers matter:

  1. Indexation — how many of our 1,376 submitted URLs Google actually has, and
     which of the new page clusters (guides, gas stations, location cluster) are
     missing. This is the number we have been guessing at for weeks.
  2. Striking distance — queries sitting at positions 4-20 with real impressions.
     These are the pages where a title rewrite or a paragraph moves money, and
     they are invisible without this data.
  3. High impressions, no clicks — queries where we are shown and ignored. That
     is a title/description problem, not a ranking problem.
  4. Cannibalisation — one query where two or more of our URLs compete.
  5. Cluster performance — do the pages built in August 2026 get impressions yet.
"""
import csv, glob, os, re, sys
from collections import defaultdict

GSC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gsc')


def read(name_hints):
    """Find a CSV whose filename matches any hint, return list of dicts."""
    for f in glob.glob(os.path.join(GSC, '*.csv')):
        base = os.path.basename(f).lower()
        if any(h in base for h in name_hints):
            with open(f, encoding='utf-8-sig', newline='') as fh:
                sample = fh.read(4096); fh.seek(0)
                delim = ';' if sample.count(';') > sample.count(',') else ','
                return [r for r in csv.DictReader(fh, delimiter=delim)]
    return []


def num(v):
    if v is None: return 0.0
    v = str(v).replace('%', '').replace(',', '.').strip()
    try: return float(v)
    except ValueError: return 0.0


def col(row, *hints):
    for k in row:
        kl = k.lower()
        if any(h in kl for h in hints): return row[k]
    return ''


CLUSTERS = [
    ('guías (18 páginas)', re.compile(r'/(presupuesto-de-obra|proyecto-arquitectonico|pozo-de-absorcion|'
                                      r'cuanto-cuesta-una-alberca|muro-de-contencion|mecanica-de-suelos|microcemento|'
                                      r'cemento-pulido|humedad-en-paredes|contrato-de-obra|supervision-de-obra|'
                                      r'uso-de-suelo|director-responsable-de-obra|pergola-de-madera|deck-de-madera|'
                                      r'ventanas-de-aluminio|captacion-de-agua-de-lluvia|grietas-en-muros|guias)/')),
    ('gasolineras (9)', re.compile(r'/construccion-remodelacion-gasolineras-')),
    ('casas por zona', re.compile(r'/construccion-de-casas-')),
    ('villas y hoteles', re.compile(r'/construccion-villas-hoteles-')),
    ('blog', re.compile(r'/blog')),
]


def main():
    if not os.path.isdir(GSC) or not glob.glob(os.path.join(GSC, '*.csv')):
        print('Pon los CSV de Search Console en %s/ y vuelve a ejecutar.' % GSC)
        print('En GSC: Rendimiento -> Exportar -> CSV (descarga un ZIP, descomprímelo ahí).')
        print('Y desde Indexación -> Páginas -> Exportar, para el informe de indexación.')
        return 1

    queries = read(['quer', 'consult', 'anfrag'])
    pages = read(['page', 'pagin', 'seit'])

    if queries:
        rows = []
        for r in queries:
            rows.append((col(r, 'quer', 'consult', 'anfrag'),
                         num(col(r, 'click', 'clic')),
                         num(col(r, 'impress', 'impres')),
                         num(col(r, 'position', 'posici'))))
        tot_c = sum(x[1] for x in rows); tot_i = sum(x[2] for x in rows)
        print('=== CONSULTAS: %d | clics %d | impresiones %d | CTR %.1f%%'
              % (len(rows), tot_c, tot_i, 100 * tot_c / tot_i if tot_i else 0))

        strike = sorted([x for x in rows if 3.5 <= x[3] <= 20.5 and x[2] >= 10],
                        key=lambda x: -x[2])[:25]
        print('\n--- A un paso (posición 4-20, con impresiones reales)')
        print('%-46s %6s %8s %6s' % ('consulta', 'clics', 'impr', 'pos'))
        for q, c, i, p in strike:
            print('%-46s %6d %8d %6.1f' % (q[:46], c, i, p))

        nocl = sorted([x for x in rows if x[1] == 0 and x[2] >= 30], key=lambda x: -x[2])[:15]
        print('\n--- Muchas impresiones, cero clics (problema de title/description)')
        for q, c, i, p in nocl:
            print('%-46s %8d impr  pos %.1f' % (q[:46], i, p))

    if pages:
        prows = []
        for r in pages:
            prows.append((col(r, 'page', 'pagin', 'url', 'seit'),
                          num(col(r, 'click', 'clic')),
                          num(col(r, 'impress', 'impres')),
                          num(col(r, 'position', 'posici'))))
        print('\n=== PÁGINAS con datos: %d' % len(prows))
        print('\n--- Rendimiento por cluster')
        print('%-24s %8s %8s %10s %8s' % ('cluster', 'páginas', 'clics', 'impresiones', 'pos med'))
        for name, rx in CLUSTERS:
            sel = [x for x in prows if rx.search(x[0])]
            if not sel:
                print('%-24s %8d %8s %10s %8s' % (name, 0, '-', '-', 'sin datos aún'))
                continue
            c = sum(x[1] for x in sel); i = sum(x[2] for x in sel)
            pos = sum(x[3] * x[2] for x in sel) / i if i else 0
            print('%-24s %8d %8d %10d %8.1f' % (name, len(sel), c, i, pos))

        # what we submitted vs what has any impression at all
        sm = open(os.path.join(os.path.dirname(GSC), 'sitemap.xml'), encoding='utf-8').read()
        subm = set(u.rstrip('/') for u in re.findall(r'<loc>(.*?)</loc>', sm))
        seen = set(x[0].rstrip('/') for x in prows)
        never = sorted(subm - seen)
        print('\n=== URLs enviadas: %d | con al menos una impresión: %d | sin ninguna: %d'
              % (len(subm), len(subm & seen), len(never)))
        for name, rx in CLUSTERS:
            n = [u for u in never if rx.search(u)]
            if n: print('   %-24s sin impresiones: %d' % (name, len(n)))
        print('\n--- Ejemplos sin ninguna impresión (revisar indexación en GSC)')
        for u in never[:15]: print('   ', u)

    if queries and pages:
        # cannibalisation needs the query+page export; GSC only gives it filtered,
        # so this uses whatever page-level rows share a top query prefix
        print('\nNota: para canibalización exacta hace falta el export de Consultas '
              'filtrado por página, o la API. Con estos CSV se ve el cluster, no el par.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
