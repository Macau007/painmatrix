# -*- coding: utf-8 -*-
import os
TARGET = os.path.join(r'D:\PainMatrix', 'docs', 'README_CN.md')
# Read from the data file
DATA = os.path.join(r'D:\PainMatrix', '_doc_data.b64')
import base64
with open(DATA, 'r') as f:
    b64data = f.read()
content = base64.b64decode(b64data).decode('utf-8')
with open(TARGET, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'Written {len(content)} chars to {TARGET}')
os.remove(DATA)
print('Cleaned up data file')
