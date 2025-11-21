import sys
p = r'd:\\parking_qr\\app\\web.py'
with open(p,'r',encoding='utf-8') as f:
    for i,l in enumerate(f,1):
        print(f'{i:03}: {l.rstrip()}')
