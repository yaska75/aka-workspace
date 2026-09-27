"""Build the Command Centre page: src.html + logos -> build/command-centre.html"""
import os, re
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
s = open(os.path.join(here, 'src.html')).read()
s = s.replace('LOGO_L', open(os.path.join(root, 'assets/logo_light.txt')).read().strip())
s = s.replace('LOGO_D', open(os.path.join(root, 'assets/logo_dark.txt')).read().strip())
os.makedirs(os.path.join(root, 'build'), exist_ok=True)
out = os.path.join(root, 'build/command-centre.html'); open(out, 'w').write(s)
i = s.rfind('<script>'); open(os.path.join(root, 'build/command-centre.js'), 'w').write(s[i+8:s.rfind('</script>')])
print('wrote', out)
