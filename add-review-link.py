#!/usr/bin/env python3
"""Add the Google Business Profile review links site-wide (2026-08-16).

The owner supplied the profile's CID: 15171494471908439484 (hex 0xd28bf9d715e7b5bc).

Two links are used, because they do different jobs:

  WRITE  a deep link that opens Google's write-a-review dialog directly. Asking a
         happy client to "search for us on Google and leave a review" loses most
         of them at the search step; a one-tap link is the difference between a
         handful of reviews and a steady flow.
  READ   the Maps profile itself, for visitors who want to check the reviews
         before contacting us. This one belongs next to the phone number, not
         hidden in a footer column.

Reviews are the single blocker I have flagged since the first Semrush pull:
on-page work is finished, the domain has 61 referring domains, and the local
pack — which decides "constructora playa del carmen" — runs on the profile, not
on the site. So this goes everywhere, in the language of each page.

Also adds the profile to the sameAs array of the GeneralContractor schema, which
is how Google associates this site with that listing.
"""
import os, re, glob, json

CID = '15171494471908439484'
HEX = '0xd28bf9d715e7b5bc'
READ = 'https://www.google.com/maps?cid=' + CID
WRITE = ('https://search.google.com/local/writereview?placeid=' if False else
         'https://www.google.com/search?q=Recrea+Construction+%26+Arquitectura'
         '&ludocid=' + CID + '#lrd=0x0:' + HEX + ',3,,,')

T = {
 'es': ('¿Trabajamos juntos? Deje su reseña en Google', 'Escribir una reseña', 'Ver reseñas en Google',
        'Su opinión ayuda a otros propietarios a decidir, y a nosotros a mejorar.'),
 'en': ('Worked with us? Leave a Google review', 'Write a review', 'Read our Google reviews',
        'Your review helps other owners decide, and helps us improve.'),
 'de': ('Haben wir für Sie gebaut? Hinterlassen Sie eine Google-Bewertung', 'Bewertung schreiben',
        'Google-Bewertungen ansehen', 'Ihre Bewertung hilft anderen Bauherren bei der Entscheidung.'),
 'fr': ('Nous avons travaillé ensemble ? Laissez un avis Google', 'Rédiger un avis', 'Voir les avis Google',
        'Votre avis aide d\'autres propriétaires à décider, et nous aide à progresser.'),
 'ru': ('Работали с нами? Оставьте отзыв в Google', 'Написать отзыв', 'Читать отзывы в Google',
        'Ваш отзыв помогает другим владельцам решиться, а нам — становиться лучше.'),
 'zh': ('与我们合作过？欢迎在 Google 留下评价', '撰写评价', '查看 Google 评价',
        '您的评价能帮助其他业主做决定，也帮助我们改进。'),
}

BLOCK = ('<section data-review="gbp" class="py-4" style="background:#f6f7f9;border-top:1px solid #e6e8eb">'
         '<div class="container text-center">'
         '<h2 class="h5 mb-2">%s</h2>'
         '<p class="mb-3 text-muted small">%s</p>'
         '<a href="%s" target="_blank" rel="noopener" class="btn btn-cta me-2 mb-2">'
         '<i class="bi bi-star-fill me-2"></i>%s</a>'
         '<a href="%s" target="_blank" rel="noopener" class="btn btn-outline-secondary mb-2">'
         '<i class="bi bi-google me-2"></i>%s</a>'
         '</div></section>\n')

FOOT = ('<p data-review="gbp-foot" class="mb-0 mt-2"><a href="%s" target="_blank" rel="noopener">%s</a> · '
        '<a href="%s" target="_blank" rel="noopener">%s</a></p>\n')


def lang_of(s):
    m = re.search(r'<html lang="([\w-]+)"', s)
    code = (m.group(1) if m else 'es').split('-')[0]
    return code if code in T else 'es'


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    files = glob.glob('**/*.html', recursive=True)
    blocks = foots = schema = 0
    for f in files:
        s = open(f, encoding='utf-8').read()
        if '<footer' not in s:
            continue
        lg = lang_of(s)
        head, ask, read_lbl, sub = T[lg]

        # 1) the call-to-action section, immediately before the footer
        s = re.sub(r'<section data-review="gbp">.*?</section>\n?', '', s, flags=re.S)
        s = re.sub(r'<section data-review="gbp"[^>]*>.*?</section>\n?', '', s, flags=re.S)
        blk = BLOCK % (head, sub, WRITE, ask, READ, read_lbl)
        i = s.rfind('<footer')
        s = s[:i] + blk + s[i:]
        blocks += 1

        # 2) a permanent pair of links inside the footer's first column
        s = re.sub(r'<p data-review="gbp-foot".*?</p>\n?', '', s, flags=re.S)
        m = re.search(r'(<footer.*?<div class="col-lg-4">.*?</p>)', s, re.S)
        if m:
            s = s[:m.end()] + '\n' + (FOOT % (WRITE, ask, READ, read_lbl)) + s[m.end():]
            foots += 1

        # 3) associate the site with the listing in structured data
        def add_sameas(mm):
            try:
                d = json.loads(mm.group(1))
            except Exception:
                return mm.group(0)
            if not isinstance(d, dict) or d.get('@type') not in (
                    'GeneralContractor', 'LocalBusiness', 'HomeAndConstructionBusiness', 'Organization'):
                return mm.group(0)
            same = d.get('sameAs') or []
            if isinstance(same, str):
                same = [same]
            if READ not in same:
                same.append(READ)
            d['sameAs'] = same
            return '<script type="application/ld+json">%s</script>' % json.dumps(d, ensure_ascii=False)

        before = s
        s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', add_sameas, s, flags=re.S)
        if s != before:
            schema += 1

        open(f, 'w', encoding='utf-8').write(s)

    print('review CTA blocks: %d | footer links: %d | schema sameAs: %d | files: %d'
          % (blocks, foots, schema, len(files)))
    print('WRITE:', WRITE)
    print('READ :', READ)


if __name__ == '__main__':
    main()
