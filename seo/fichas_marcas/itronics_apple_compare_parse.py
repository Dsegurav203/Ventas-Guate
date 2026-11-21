import sys,json,re
from bs4 import BeautifulSoup
soup=BeautifulSoup(open(sys.argv[1],encoding='utf8').read(),'lxml')
from collections import OrderedDict
groups=OrderedDict()
for c in soup.select('div.cell-item'):
    p=c.parent
    groups.setdefault(id(p),(p,[]))[1].append(c)
sizes={}
for k,(p,cs) in groups.items(): sizes[len(cs)]=sizes.get(len(cs),0)+1
print(sizes)
# show a few parent contexts
out=[]
for k,(p,cs) in groups.items():
    # find nearest preceding heading/label
    lab=p.find_previous(lambda t: t.name in ('h3','h4','h5','h6') or (t.get('class') and any('title' in x or 'label' in x or 'name' in x for x in t.get('class'))))
    out.append({'label': lab.get_text(' ',strip=True)[:80] if lab else None,'n':len(cs),'vals':[re.sub(r'\s+',' ',c.get_text(' ',strip=True)) for c in cs]})
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(out))
