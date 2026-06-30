#!/bin/bash
cd /home/olek/recrea-bootstrap
/usr/bin/python3 generate-blogs.py
git add -A
git commit -m "daily blog: 5 new SEO articles $(date +%Y-%m-%d)"
git push origin main
