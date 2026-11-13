import os
from pathlib import Path
from datetime import datetime, timedelta

ROOT = Path.home() / 'Downloads'
MIN_MB = 50
DAYS = 30

def human(n):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if n < 1024:
            return f'{n:.1f}{unit}'
        n /= 1024
    return f'{n:.1f}TB'

def suggest(root=ROOT):
    cutoff = datetime.now() - timedelta(days=DAYS)
    out = []
    for p in root.rglob('*'):
        try:
            if not p.is_file():
                continue
            st = p.stat()
            old = datetime.fromtimestamp(st.st_mtime) < cutoff
            large = st.st_size >= MIN_MB * 1024 * 1024
            if old or large:
                out.append((p, st.st_size, 'large' if large else 'stale'))
        except OSError:
            pass
    return sorted(out, key=lambda x: x[1], reverse=True)

def main():
    files = suggest()
    print(f'Purrge demo: scanning {ROOT}')
    for i, (p, size, why) in enumerate(files[:20], 1):
        print(f'{i:2}. {human(size):>8} [{why}] {p}')
    if not files:
        print('No candidates found.')
        return
    ans = input('Type YES to delete these 20 files: ')
    if ans.strip() != 'YES':
        print('Dry run only. Cancelled.')
        return
    freed = 0
    for p, size, _ in files[:20]:
        try:
            p.unlink()
            freed += size
            print('Removed', p)
        except OSError as e:
            print('Skip', p, e)
    print('Freed', human(freed))

if __name__ == '__main__':
    main()