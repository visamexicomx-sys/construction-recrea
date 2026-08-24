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
import csv, glob, io, os, re, sys
from collections import defaultdict

GSC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gsc')


def decode(path):
    """GSC exports are UTF-16 in some locales and UTF-8 in others.

    Order matters: almost any byte string decodes as UTF-16 without raising,
    it just comes out as CJK mojibake, so decide by BOM (or by the NUL bytes
    that unmarked UTF-16 leaves behind) instead of by trial and error.
    """
    raw = open(path, 'rb').read()
    if raw[:2] in (b'\xff\xfe', b'\xfe\xff') or b'\x00' in raw[:200]:
        order = ('utf-16', 'utf-8-sig', 'cp1251')
    else:
        order = ('utf-8-sig', 'cp1251', 'cp1252', 'latin-1')
    for enc in order:
        try:
            t = raw.decode(enc)
        except (UnicodeDecodeError, UnicodeError):
            continue
        if '\x00' in t:
            continue
        return t
    return raw.decode('utf-8', 'replace')


def rows_of(path):
    t = decode(path)
    head = t.splitlines()[0] if t else ''
    delim = ';' if head.count(';') > head.count(',') else ','
    return list(csv.reader(io.StringIO(t), delimiter=delim))


def read(name_hints):
    """Find the CSV whose *first column header* matches any hint.

    The filename is unreliable: Search Console names the files in the account
    language, and the ZIP mangles non-ASCII names on some systems. The header
    row is the only dependable signal, so match on that. Returns rows already
    normalised to fixed keys, since the column names are localised too (and the
    Russian export even spells "Kлики" with a Latin K).
    """
    for f in sorted(glob.glob(os.path.join(GSC, '*.csv'))):
        rows = rows_of(f)
        if len(rows) < 2:
            continue
        first = rows[0][0].lower().strip()
        if not any(h in first for h in name_hints):
            continue
        out = []
        for r in rows[1:]:
            if not r or not r[0]:
                continue
            r = r + [''] * (5 - len(r))
            out.append({'dim': r[0], 'clicks': r[1], 'impressions': r[2],
                        'ctr': r[3], 'position': r[4]})
        return out
    return []


def num(v):
    if v is None: return 0.0
    v = str(v).replace('%', '').replace(',', '.').replace(' ', '').replace(' ', '').strip()
    try: return float(v)
    except ValueError: return 0.0


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

    queries = read(['quer', 'consult', 'anfrag', 'запрос'])
    pages = read(['page', 'pagin', 'seit', 'страниц'])
    index = read(['reason', 'motivo', 'grund', 'причина'])

    if queries:
        rows = []
        for r in queries:
            rows.append((r['dim'], num(r['clicks']), num(r['impressions']),
                         num(r['position'])))
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
            prows.append((r['dim'], num(r['clicks']), num(r['impressions']),
                          num(r['position'])))
        pc = sum(x[1] for x in prows); pi = sum(x[2] for x in prows)
        won = [x for x in prows if x[1] > 0]
        print('\n=== PÁGINAS con datos: %d | clics %d | impresiones %d | CTR %.1f%%'
              % (len(prows), pc, pi, 100 * pc / pi if pi else 0))
        print('    con al menos un clic: %d  |  con impresiones pero 0 clics: %d'
              % (len(won), len(prows) - len(won)))
        top = sorted(prows, key=lambda x: -x[1])[:10]
        share = 100 * sum(x[1] for x in top) / pc if pc else 0
        print('    las 10 mejores páginas concentran el %.0f%% de los clics' % share)
        print('\n--- Top 15 páginas')
        for u, c, i, p in sorted(prows, key=lambda x: -x[1])[:15]:
            print('   %5d clics %7d impr  pos %4.1f  %s'
                  % (c, i, p, u.replace('https://construction-recrea.com', '')[:58]))
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

    if index:
        # Indexación -> Páginas -> Exportar. Columnas: motivo, origen, validación, páginas.
        print('\n=== INDEXACIÓN: por qué Google deja páginas fuera')
        for r in index:
            n = num(r['ctr']) or num(r['position']) or num(r['impressions'])
            print('   %-52s %5d páginas' % (r['dim'][:52], n))

    if queries and pages:
        # cannibalisation needs the query+page export; GSC only gives it filtered,
        # so this uses whatever page-level rows share a top query prefix
        print('\nNota: para canibalización exacta hace falta el export de Consultas '
              'filtrado por página, o la API. Con estos CSV se ve el cluster, no el par.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
