#!/usr/bin/env python3
"""Split per-page text into units <= max_pages.

Strategy: cut at the shallowest heading level inside an oversized span,
recursing into sub-spans; when no headings exist, chunk by pages with a
1-page overlap between consecutive chunks.

Usage: python3 split_document.py <pages.json> <headings.json> <outdir>
       [--max-pages 20] [--chunk-pages 10] [--overlap 1]
       python3 split_document.py --text <file.txt> <headings.json> <outdir>
pages.json:    ["page 1 text", ...]  OR  {"page_count": N, "pages": [...]}
               (the pdf skill's --text raw output is accepted directly)
--text:        any plain text; chunked internally into 250-line pseudo-pages
headings.json: [{"level": 1, "title": "X", "page": 3}, ...]  (1-based pages)
Writes: outdir/unit-0001.txt ... and outdir/index.json
        [{unit, path, start_page, end_page}]  (1-based, inclusive)
"""
import argparse, json, os

MAX_PAGES = 20
CHUNK_PAGES = 10
OVERLAP = 1


LINES_PER = 250  # pseudo-page size for --text mode


def split(pages, headings, outdir):
    n = len(pages)
    hs = sorted([h for h in headings if 1 <= h.get('page', 0) <= n],
                key=lambda h: h['page'])
    units = []

    def emit(s, e):
        units.append((s, e))

    def split_by_pages(s, e):
        pos = s
        while pos < e:
            end = min(pos + CHUNK_PAGES, e)
            if end >= e:
                emit(pos, e)
                return
            emit(pos, end)
            pos = end - OVERLAP

    def walk(s, e):  # pages s..e-1
        if e - s <= MAX_PAGES:
            emit(s, e)
            return
        inside = [h for h in hs if s < h['page'] < e]
        if not inside:
            split_by_pages(s, e)
            return
        min_level = min(h['level'] for h in inside)
        cuts = [h['page'] for h in inside if h['level'] == min_level]
        cur = s
        for c in cuts + [e]:
            if c > cur:
                walk(cur, c)
            cur = c

    walk(1, n + 1)

    os.makedirs(outdir, exist_ok=True)
    index = []
    for i, (s, e) in enumerate(units, 1):
        p = os.path.join(outdir, 'unit-%04d.txt' % i)
        with open(p, 'w', encoding='utf-8') as f:
            f.write('\f'.join(pages[s - 1:e - 1]))
        index.append({'unit': i, 'path': p, 'start_page': s, 'end_page': e - 1})
    with open(os.path.join(outdir, 'index.json'), 'w') as f:
        json.dump(index, f, indent=2)
    print('units=%d' % len(index))
    for it in index:
        print('  unit-%04d.txt pages %d-%d' % (it['unit'], it['start_page'], it['end_page']))


def main():
    global MAX_PAGES, CHUNK_PAGES, OVERLAP
    ap = argparse.ArgumentParser()
    ap.add_argument('pages_json', nargs='?')
    ap.add_argument('headings_json')
    ap.add_argument('outdir')
    ap.add_argument('--text', help='plain text file; chunked into pseudo-pages')
    ap.add_argument('--max-pages', type=int, default=MAX_PAGES)
    ap.add_argument('--chunk-pages', type=int, default=CHUNK_PAGES)
    ap.add_argument('--overlap', type=int, default=OVERLAP)
    a = ap.parse_args()
    MAX_PAGES, CHUNK_PAGES, OVERLAP = a.max_pages, a.chunk_pages, a.overlap
    if a.text:
        with open(a.text, encoding='utf-8') as f:
            lines = f.read().splitlines()
        pages = ['\n'.join(lines[i:i + LINES_PER])
                 for i in range(0, len(lines), LINES_PER)]
    else:
        if not a.pages_json:
            ap.error('pages_json or --text is required')
        with open(a.pages_json, encoding='utf-8') as f:
            pages = json.load(f)
        if isinstance(pages, dict):  # pdf skill --text raw output
            pages = pages.get('pages', [])
    with open(a.headings_json, encoding='utf-8') as f:
        headings = json.load(f)
    split(pages, headings, a.outdir)


if __name__ == '__main__':
    main()
