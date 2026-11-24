import re, unicodedata
CHO = ['K','K','N','T','T','R','M','P','P','S','S','','C','C','C','K','T','P','H']
JONG = ['','K','K','K','N','N','N','T','R','R','R','R','R','R','R','R','M','P','P','T','T','NG','T','T','K','T','P','T']
LET = dict(A='',B='P',C='S',D='T',E='',F='P',G='C',H='C',I='',J='C',K='K',L='R',M='M',N='N',O='',P='P',Q='K',R='R',S='S',T='T',U='',V='P',W='TPR',X='KS',Y='',Z='C')
V = set('AEIOUY')

def kor_key(s):  # 한글 -> 자음 골격
    s = unicodedata.normalize('NFKC', str(s))
    s = re.sub(r'제\s*(\d+)', r'\1', s); s = re.sub(r'호$', '', s.strip())  # 제2..호 -> 2
    out = []
    for ch in s:
        o = ord(ch) - 0xAC00
        if 0 <= o < 11172: out.append(CHO[o // 588] + JONG[o % 28])  # 초성+종성, 모음 버림
        elif ch.isdigit(): out.append(ch)
    return re.sub(r'(.)\1+', r'\1', ''.join(out))

def eng_word(w):
    if w.isdigit(): return w
    if len(w) <= 3 and not any(c in V for c in w):  # 약어 SJ -> 에스제이
        return ''.join(LET.get(c, '') for c in w)
    w = w.replace('PH','F').replace('CK','K').replace('QU','K').replace('SH','S').replace('TH','S').replace('X','KS')
    out = []
    for i, c in enumerate(w):
        nx = w[i+1] if i+1 < len(w) else ''; pv = w[i-1] if i > 0 else ''
        if c in V or c == 'W': continue
        if c == 'H' and pv and pv not in V and pv != 'C': continue
        if c == 'R' and pv in V and nx not in V: continue  # 무음 r: Morning -> 모닝
        if c == 'C': out.append('C' if nx == 'H' else ('S' if nx and nx in 'EIY' else 'K')); continue
        if c == 'H' and pv == 'C': continue
        if c == 'N' and nx == 'G': out.append('NG'); continue
        if c == 'G' and pv == 'N': continue
        out.append({'G':'K','J':'C','Z':'C','V':'P','F':'P','L':'R','D':'T','B':'P'}.get(c, c))
    return ''.join(out)

def eng_key(s):  # 영문 -> 자음 골격
    s = unicodedata.normalize('NFKC', str(s)).upper()
    s = re.sub(r'\bNO\.?\s*(?=\d)', '', s)  # No.2 -> 2
    return re.sub(r'(.)\1+', r'\1', ''.join(eng_word(t) for t in re.findall(r'[A-Z]+|\d+', s)))