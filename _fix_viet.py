import os
import sys

files_and_fixes = [
    (
        r'c:\Users\admin\Downloads\ML\Lab01_3B1B\drivex\scenes\part03\p03_s03_smart_intersection.py',
        'PIBubble(pi,  "Tại sao nhiều sensor vậy?\nKhông phải overkill à?", position=UR)',
        'PIBubble(pi,  "Why so many sensors?\nIsn\'t that overkill?", position=UR)'
    ),
    (
        r'c:\Users\admin\Downloads\ML\Lab01_3B1B\drivex\scenes\part02\p02_s03_evolution.py',
        'PIBubble(pi, "E2E đã giải quyết\nmọi thứ chưa?", position=UR)',
        'PIBubble(pi, "Has E2E solved\neverything yet?", position=UR)'
    ),
]

for fpath, old, new in files_and_fixes:
    with open(fpath, encoding='utf-8') as f:
        content = f.read()
    if old in content:
        content = content.replace(old, new)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {os.path.basename(fpath)}')
    else:
        print(f'NOT FOUND in: {os.path.basename(fpath)}')
