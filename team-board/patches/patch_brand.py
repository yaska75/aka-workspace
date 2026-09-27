p='team.html'; s=open(p).read()
L=open('logo_light.txt').read(); D=open('logo_dark.txt').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:70]); s=s.replace(a,b)
FONT_OLD='family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700&family=Instrument+Sans'
FONT_NEW='family=Outfit:wght@500;600;700&family=Instrument+Sans'
rep(FONT_OLD,FONT_NEW,2)
s=s.replace('"Bricolage Grotesque"','"Outfit"')
rep('<title>a.k.a. Media team to-do</title>','<title>a.k.a. Media team board</title>',2)
light=':root{--paper:#F4F4F2;--surface:#FFFFFF;--ink:#141417;--muted:#5E5E66;--line:#E2E2DF;--accent:#EB1843;--accent-ink:#FFFFFF;--strike:#B0102C;--soft:#ECECE9;--p0:#EB1843;--p1:#141417;--p2:#6B4FC8;--p3:#1F6FB5;--p4:#2E7D46;--p5:#C2410C;--p6:#8A6A12;}'
dk='--paper:#0E0E11;--surface:#18181C;--ink:#EDEDF0;--muted:#9A9AA3;--line:#2C2C33;--accent:#FF4D6D;--accent-ink:#17080B;--strike:#FF8A9C;--soft:#232329;--p0:#FF4D6D;--p1:#E6E6EA;--p2:#A48CF0;--p3:#6FB0EE;--p4:#66C987;--p5:#F59E5B;--p6:#D9B44A;'
import re
s=re.sub(r':root\{--paper:#EEF3F4;[^}]*\}',light,s,count=1)
s=re.sub(r'(@media \(prefers-color-scheme: dark\)\{:root:not\(\[data-theme="light"\]\)\{)--paper:#0E1922;[^}]*\}',lambda m:m.group(1)+dk+'}',s,count=1)
s=re.sub(r':root\[data-theme="dark"\]\{--paper:#0E1922;[^}]*\}',':root[data-theme="dark"]{'+dk+'}',s,count=1)
assert '#0E1922' not in s and '#EEF3F4' not in s
# brand CSS
rep('.place{margin:0;color:var(--muted);font-size:15px}',
'''.place{margin:0;color:var(--muted);font-size:15px}
.brand{display:flex;align-items:center;gap:16px;min-width:0}
.logo{display:block;width:118px;aspect-ratio:450/215;flex:none;background:url(LOGO_L) left center/contain no-repeat}
.brand .sub{display:flex;flex-direction:column;gap:2px;padding-left:16px;border-left:2px solid var(--accent)}
.brand .sub b{font-family:"Outfit","Instrument Sans",system-ui,sans-serif;font-weight:600;font-size:13px;letter-spacing:.32em;text-transform:uppercase;color:var(--ink)}
.brand .sub span{font-size:14px;color:var(--muted)}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]) .logo{background-image:url(LOGO_D)}}
:root[data-theme="dark"] .logo{background-image:url(LOGO_D)}
@media (max-width:520px){.logo{width:92px}.brand{gap:12px}.brand .sub{padding-left:12px}}'''.replace('LOGO_L',L).replace('LOGO_D',D))
rep('''      '<div class="topline"><p class="place">a.k.a. Media, all offices</p>' +''',
'''      '<div class="topline"><div class="brand"><span class="logo" role="img" aria-label="a.k.a. Media"></span><div class="sub"><b>Team board</b><span>All offices</span></div></div>' +''')
rep("return cs.getPropertyValue(k).trim() || '#0B7B77'; }).concat(['#F2B233']);","return cs.getPropertyValue(k).trim() || '#EB1843'; }).concat(['#EB1843','#F2B233']);")
open(p,'w').write(s); print('ok',len(s))
