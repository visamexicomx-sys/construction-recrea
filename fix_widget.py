#!/usr/bin/env python3
"""Fix WhatsApp widget and email button on all pages."""
import os, re, glob

ROOT = '/home/olek/recrea-bootstrap'

# Old widget JS patterns (both inline and in script blocks)
OLD_JS_INLINE = re.compile(
    r"<script>\(function\(\)\{var t=document\.getElementById\('waToggle'\).*?\}\);\}\)\(\);</script>",
    re.DOTALL
)

OLD_JS_BLOCK = re.compile(
    r"// WhatsApp Widget\n\(function\(\)\{\n\s*var toggle=document\.getElementById\('waToggle'\).*?\}\);\n\}\)\(\);",
    re.DOTALL
)

# New robust widget JS (inline version for pages that have it as separate script)
NEW_JS_INLINE = """<script>(function(){var t=document.getElementById('waToggle'),b=document.getElementById('waChatBox'),c=document.getElementById('waClose'),i=document.getElementById('waIcon');if(!t||!b)return;t.addEventListener('click',function(e){e.stopPropagation();var o=b.classList.toggle('wa-show');t.classList.toggle('wa-open',o);if(i)i.className=o?'bi bi-x-lg':'bi bi-whatsapp';});if(c)c.addEventListener('click',function(e){e.stopPropagation();b.classList.remove('wa-show');t.classList.remove('wa-open');if(i)i.className='bi bi-whatsapp';});document.addEventListener('click',function(e){if(!e.target.closest('#waWidget')){b.classList.remove('wa-show');t.classList.remove('wa-open');if(i)i.className='bi bi-whatsapp';}});})();</script>"""

# New widget JS for block version (inside existing script tag)
NEW_JS_BLOCK = """// WhatsApp Widget
(function(){
  var toggle=document.getElementById('waToggle'),
      box=document.getElementById('waChatBox'),
      close=document.getElementById('waClose'),
      icon=document.getElementById('waIcon');
  if(!toggle||!box)return;
  toggle.addEventListener('click',function(e){
    e.stopPropagation();
    var open=box.classList.toggle('wa-show');
    toggle.classList.toggle('wa-open',open);
    if(icon){icon.className=open?'bi bi-x-lg':'bi bi-whatsapp';}
  });
  if(close)close.addEventListener('click',function(e){
    e.stopPropagation();
    box.classList.remove('wa-show');
    toggle.classList.remove('wa-open');
    if(icon)icon.className='bi bi-whatsapp';
  });
  document.addEventListener('click',function(e){
    if(!e.target.closest('#waWidget')){
      box.classList.remove('wa-show');
      toggle.classList.remove('wa-open');
      if(icon)icon.className='bi bi-whatsapp';
    }
  });
})();"""

# Orphaned SVG pattern (old WhatsApp float icon remnant)
ORPHAN_SVG = re.compile(
    r'\n\s*<svg viewBox="0 0 24 24"><path d="M17\.472.*?</svg>\n</a>',
    re.DOTALL
)

count = 0
for pattern in ['index.html', 'en/index.html', 'de/index.html', 'ru/index.html', 'zh/index.html',
                 'blog/*.html', 'blog-es/*.html', 'blog-de/*.html', 'blog-ru/*.html', 'blog-zh/*.html',
                 'projects/*.html', 'noticias/*.html', 'partners/*.html']:
    for fpath in glob.glob(os.path.join(ROOT, pattern)):
        if fpath.endswith('.py'):
            continue
        with open(fpath, 'r') as f:
            content = f.read()

        if 'waToggle' not in content:
            continue

        original = content

        # Remove orphaned SVG
        content = ORPHAN_SVG.sub('', content)

        # Fix inline widget JS
        content = OLD_JS_INLINE.sub(NEW_JS_INLINE, content)

        # Fix block widget JS
        content = OLD_JS_BLOCK.sub(NEW_JS_BLOCK, content)

        if content != original:
            with open(fpath, 'w') as f:
                f.write(content)
            count += 1
            print(f"Fixed: {os.path.relpath(fpath, ROOT)}")

print(f"\nTotal fixed: {count}")
