import os,base64
T=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'docs', 'README_CN.md')
D=os.path.join(os.path.dirname(os.path.abspath(__file__)), '_v610.b64')
with open(D, 'r', encoding='ascii') as f: b=f.read()
c=base64.b64decode(b).decode('utf-8')
with open(T, 'w', encoding='utf-8') as o: o.write(c)
print(f'Written {len(c)} chars to {T}')
os.remove(D)