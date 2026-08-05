#!/bin/bash
cd /home/olek/recrea-bootstrap
/usr/bin/python3 generate-blogs.py
/usr/bin/python3 rebuild-blog-index.py
git add -A
git commit -m "daily blog: 5 new SEO articles $(date +%Y-%m-%d)"
git pull --rebase origin main
git push origin main
