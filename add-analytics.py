#!/usr/bin/env python3
"""Insert the GA4 tag into every HTML page that lacks it. Safe to run repeatedly.
Runs after the daily blog and news generators so new pages are tagged too."""
import os, sys
GA_ID = "G-XXXXXXXXXX"  # set to the real GA4 measurement ID
ROOT = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) > 1:
    GA_ID = sys.argv[1]
if not GA_ID.startswith("G-") or "XXXX" in GA_ID:
    print("analytics: no GA4 ID set, skipping"); sys.exit(0)
TAG = ('<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>\n'
       '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}'
       "gtag('js',new Date());gtag('config','%s');</script>\n"
       '<script src="/js/track.js" defer></script>\n') % (GA_ID, GA_ID)
n = 0
for d, dirs, files in os.walk(ROOT):
    dirs[:] = [x for x in dirs if not x.startswith('.')]
    for f in files:
        if not f.endswith('.html'): continue
        p = os.path.join(d, f)
        s = open(p, encoding='utf-8', errors='surrogateescape').read()
        if 'googletagmanager.com/gtag/js' in s or '</head>' not in s: continue
        s = s.replace('</head>', TAG + '</head>', 1)
        open(p, 'w', encoding='utf-8', errors='surrogateescape').write(s); n += 1
print("analytics: tagged", n, "pages")
