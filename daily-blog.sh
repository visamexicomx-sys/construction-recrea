#!/bin/bash
cd /home/olek/recrea-bootstrap || exit 1

# Start from a clean, up-to-date tree (a GitHub Action also commits to main)
git stash push -u -m "daily-blog-autostash" >/dev/null 2>&1
git pull --rebase origin main || { echo "pull failed, aborting"; exit 1; }

/usr/bin/python3 generate-blogs.py
/usr/bin/python3 rebuild-blog-index.py

git add -A
git diff --staged --quiet && { echo "nothing new"; exit 0; }
git commit -m "daily blog: new SEO articles $(date +%Y-%m-%d)"

for i in 1 2 3; do
  git push origin main && exit 0
  echo "push rejected, re-syncing (attempt $i)"
  git pull --rebase origin main || exit 1
done
echo "push failed after 3 attempts"; exit 1
