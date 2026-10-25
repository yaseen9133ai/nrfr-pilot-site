"""Check that site/ works offline and holds only what the page needs (CLAUDE.md rule 8).

  loads     every reference that the browser loads (src, srcset, poster, data,
            <link href>, inline style and style.css url() and @import) is a
            relative path inside site/ that exists; an external one = fail.
            Plain <a href> links to other sites are not loaded; they are listed.
  links     every <a href> to a local file (the links to the full-size
            images) points to a file inside site/ that exists.
  scripts   no <script>, <iframe>, <object> or <embed> element at all.
  files     site/ holds only index.html and assets/; every file in assets/ is
            used by the page (style.css, the images) or is manifest.csv.
  manifest  every image is listed in site/assets/manifest.csv, and its SHA-256
            and size equal the file.
  images    every <img> has width and height attributes equal to the pixel
            size in the PNG header (layout only; they are not page text).

Reads only. Exit 0 = pass, 1 = a problem, 2 = setup error.
Python standard library only.
"""

import csv
import hashlib
import io
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

SITE = Path(__file__).resolve().parent.parent
ROOT = SITE / 'site'
LOADED_ATTRS = {'src', 'srcset', 'poster', 'data'}
BANNED = {'script', 'iframe', 'object', 'embed', 'frame', 'applet'}


def external(ref):
    """True for anything fetched from a network; an inline data: URI is not fetched."""
    parts = urlsplit(ref.strip())
    if parts.scheme == 'data':
        return False
    return bool(parts.scheme or parts.netloc or ref.strip().startswith('//'))


class Refs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.loaded, self.links, self.banned, self.styles, self.imgs, self.local = [], [], [], [], [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        line = self.getpos()[0]
        if tag in BANNED:
            self.banned.append((tag, line))
        for k, v in a.items():
            if v is None:
                continue
            if k in LOADED_ATTRS:
                for ref in ([x.strip().split(' ')[0] for x in v.split(',')] if k == 'srcset' else [v]):
                    self.loaded.append((f'<{tag} {k}>', ref, line))
            if k == 'style':
                self.styles.append((v, line))
            if k.startswith('on'):
                self.banned.append((f'{tag} {k}', line))
        if tag == 'img':
            self.imgs.append((a.get('src') or '', a.get('width'), a.get('height'), line))
        if tag == 'link' and a.get('href'):
            self.loaded.append((f'<link rel={a.get("rel")}>', a['href'], line))
        if tag == 'a' and a.get('href') and external(a['href']):
            self.links.append((a['href'], line))
        elif tag == 'a' and a.get('href') and not a['href'].startswith('#'):
            self.local.append((a['href'], line))
        if tag in ('use', 'image') and (a.get('href') or a.get('xlink:href')):
            ref = a.get('href') or a.get('xlink:href')
            if not ref.startswith('#'):
                self.loaded.append((f'<{tag} href>', ref, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def css_refs(text):
    refs = [m.group(2) for m in re.finditer(r'url\(\s*([\'"]?)(.*?)\1\s*\)', text)]
    refs += [m.group(2) for m in re.finditer(r'@import\s+([\'"])(.*?)\1', text)]
    return refs


def main():
    index = ROOT / 'index.html'
    if not index.is_file():
        print('ERROR: site/index.html not found.')
        return 2
    problems, used = [], set()
    r = Refs()
    r.feed(index.read_text(encoding='utf-8'))
    for tag, line in r.banned:
        problems.append(f'index.html line {line}: {tag} (no scripts, frames, embeds or event handlers)')
    refs = [(w, ref, f'index.html line {line}') for w, ref, line in r.loaded]
    refs += [('style attribute', ref, f'index.html line {line}') for v, line in r.styles for ref in css_refs(v)]
    for css in sorted(ROOT.rglob('*.css')):
        refs += [('css', ref, str(css.relative_to(SITE))) for ref in css_refs(css.read_text(encoding='utf-8'))]
        if re.search(r'@font-face', css.read_text(encoding='utf-8')):
            problems.append(f'{css.relative_to(SITE)}: @font-face (no web fonts)')
    for what, ref, where in refs:
        if external(ref):
            problems.append(f'{where}: {what} loads an external URL: {ref}')
            continue
        if ref.strip().startswith('data:'):
            continue
        target = (index.parent / ref.split('#')[0].split('?')[0]).resolve()
        if ROOT.resolve() not in target.parents or not target.is_file():
            problems.append(f'{where}: {what} points to a missing file or outside site/: {ref}')
        else:
            used.add(target)
    for href, line in r.local:
        target = (index.parent / href.split('#')[0].split('?')[0]).resolve()
        if ROOT.resolve() not in target.parents or not target.is_file():
            problems.append(f'index.html line {line}: link to a missing file or outside site/: {href}')
    # files
    for f in sorted(ROOT.rglob('*')):
        if f.is_dir():
            continue
        rel = f.relative_to(ROOT)
        if rel.parts[0] not in ('index.html', 'assets'):
            problems.append(f'site/{rel}: not part of the page (site/ holds index.html and assets/ only)')
        elif rel.parts[0] == 'assets' and f.resolve() not in used and f.name != 'manifest.csv':
            problems.append(f'site/{rel}: not used by the page')
    # manifest
    man = ROOT / 'assets' / 'manifest.csv'
    listed = {}
    if man.is_file():
        for row in csv.DictReader(io.StringIO(man.read_text(encoding='utf-8'))):
            listed[row['asset']] = row
    for img in sorted((ROOT / 'assets').glob('*.png')):
        row = listed.pop(img.name, None)
        blob = img.read_bytes()
        if row is None:
            problems.append(f'site/assets/{img.name}: not in manifest.csv')
        elif row['sha256'] != hashlib.sha256(blob).hexdigest() or int(row['bytes']) != len(blob):
            problems.append(f'site/assets/{img.name}: SHA-256 or size differs from manifest.csv')
    for name in listed:
        problems.append(f'manifest.csv: {name} listed but not in site/assets/')
    for src, w, h, line in r.imgs:
        f = ROOT / src
        if f.suffix != '.png' or not f.is_file():
            continue
        head = f.read_bytes()[:24]
        if head[:8] != b'\x89PNG\r\n\x1a\n' or head[12:16] != b'IHDR':
            problems.append(f'index.html line {line}: {src} is not a PNG file')
            continue
        size = (str(int.from_bytes(head[16:20], 'big')), str(int.from_bytes(head[20:24], 'big')))
        if (w, h) != size:
            problems.append(f'index.html line {line}: {src} width/height {w}x{h} != file {size[0]}x{size[1]}')
    print(f'Images: {len(r.imgs)}, each with its width and height checked against the file.')
    print(f'Loaded references: {len(refs)} (all must be local files in site/). '
          f'Links to local files: {len(r.local)}. Links to other sites (not loaded): {len(r.links)}.')
    for href, line in r.links:
        print(f'  link, line {line}: {href}')
    for p in problems:
        print(f'FAIL: {p}')
    print('Result: ' + ('PASS' if not problems else 'FAIL'))
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
