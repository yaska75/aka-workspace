"""Build the team board page.
  python3 team-board/build.py <live index.html>   -> keeps the team's live tasks and chat (use this before publishing)
  python3 team-board/build.py                     -> uses fixtures/sample-state.json (for tests only, never publish)
Writes build/team-board.html and build/team-board.js (for `node --check`)."""
import os, re, json, sys
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
if len(sys.argv) > 1:
    live = open(sys.argv[1]).read()
    st = json.loads(re.search(r'<script type="application/json" id="todo-state">(.*?)</script>', live, re.S).group(1))
else:
    st = json.load(open(os.path.join(here, 'fixtures/sample-state.json')))
print('rev', st.get('rev'), [(p['name'], len(p['tasks'])) for p in st['people']])
t = open(os.path.join(here, 'team.html')).read().replace('__STATE__', json.dumps(st, ensure_ascii=False).replace('<', '\\u003c'))
os.makedirs(os.path.join(root, 'build'), exist_ok=True)
open(os.path.join(root, 'build/team-board.html'), 'w').write(t)
open(os.path.join(root, 'build/team-board.js'), 'w').write(re.search(r'<script id="app">(.*?)</script>', t, re.S).group(1))
print('wrote build/team-board.html')
