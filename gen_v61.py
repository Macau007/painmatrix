import os, base64

TARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'README_CN.md')
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_v610.b64')

if os.path.exists(DATA):
    with open(DATA, 'r', encoding='ascii') as f:
        b64 = f.read()
    content = base64.b64decode(b64).decode('utf-8')
    with open(TARGET, 'w', encoding='utf-8') as out:
        out.write(content)
    print(f'Written {len(content)} chars to {TARGET}')
    os.remove(DATA)
    print('Cleaned up data file')
else:
    print(f'Data file not found: {DATA}')
