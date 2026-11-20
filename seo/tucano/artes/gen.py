import base64, sys, json, os
S=sys.argv[1]
def b64(p): return "data:image/jpeg;base64,"+base64.b64encode(open(f"{S}/img/{p}","rb").read()).decode()
def png(p): return "data:image/png;base64,"+base64.b64encode(open(f"{S}/img/{p}","rb").read()).decode()
P={k:b64(v) for k,v in {"modo":"D_1.jpg","rosa":"B_1.jpg","shop":"C_1.jpg","morado":"A_1.jpg","alunno":"E_1.jpg","isotta":"isotta16.jpg"}.items()}
LOGO=png("raw5")
CSS="""
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Inter Display','Inter',sans-serif;background:#0B1A2C;color:#fff;overflow:hidden}
.k{letter-spacing:.32em;font-weight:600;color:#9FB3C8;text-transform:uppercase}
.brand{font-weight:900;letter-spacing:.04em}
.big{font-weight:900;color:#FFC845;line-height:.82;letter-spacing:-.04em}
.sub{color:#E6EDF5;font-weight:500;line-height:1.3}
.cta{display:inline-block;background:#FFC845;color:#0B1A2C;font-weight:800;border-radius:999px}
.fine{color:#8CA0B6;font-weight:500}
.card{background:#fff;border-radius:28px;display:flex;align-items:center;justify-content:center;overflow:hidden;box-shadow:0 30px 60px rgba(0,0,0,.35)}
.card img{width:100%;height:100%;object-fit:contain}
.logo{background:#fff;border-radius:14px;display:inline-flex;align-items:center;justify-content:center}
.logo img{display:block}
.glow{position:absolute;border-radius:50%;background:radial-gradient(circle,#1E3A5F 0%,rgba(11,26,44,0) 70%)}
"""
def textblock(s, align="left", cta=True):
    # s = escala
    return f"""
<div style="text-align:{align}">
 <div class="k" style="font-size:{18*s}px;margin-bottom:{18*s}px">Especial de marca</div>
 <div class="brand" style="font-size:{64*s}px;margin-bottom:{6*s}px">TUCANO</div>
 <div class="big" style="font-size:{230*s}px">50<span style="font-size:{120*s}px">%</span></div>
 <div class="brand" style="font-size:{44*s}px;margin:{10*s}px 0 {22*s}px;color:#fff">de descuento</div>
 <div class="sub" style="font-size:{26*s}px;max-width:{620*s}px;{'margin:0 auto;' if align=='center' else ''}">Mochilas, maletines, fundas y accesorios originales. Diseño italiano.</div>
 {f'<div class="cta" style="font-size:{26*s}px;padding:{18*s}px {44*s}px;margin-top:{34*s}px">Comprar ahora</div>' if cta else ''}
 <div class="fine" style="font-size:{17*s}px;margin-top:{24*s}px">Válido en ventasguate.gt hasta el 31 de diciembre de 2026 o hasta agotar existencias.</div>
</div>"""
def logo(s): return f'<div class="logo" style="padding:{10*s}px {18*s}px"><img src="{LOGO}" style="height:{44*s}px"></div>'
def foot(s): return f'<div class="fine" style="font-size:{19*s}px;color:#C9D6E3">Envío a toda Guatemala · Pago contra entrega · 1 año de garantía</div>'

LAYOUTS={}
# 1 Hero desktop 1920x720
LAYOUTS["hero-desktop-1920x720"]=(1920,720,f"""
<div class="glow" style="width:1100px;height:1100px;left:-300px;top:-200px"></div>
<div style="position:absolute;left:110px;top:70px">{logo(0.9)}</div>
<div style="position:absolute;left:110px;top:160px">{textblock(0.78)}</div>
<div class="card" style="position:absolute;left:880px;top:70px;width:470px;height:580px;transform:rotate(-3deg)"><img src="{P['modo']}"></div>
<div class="card" style="position:absolute;left:1390px;top:60px;width:420px;height:290px"><img src="{P['rosa']}"></div>
<div class="card" style="position:absolute;left:1390px;top:375px;width:420px;height:290px"><img src="{P['shop']}"></div>
<div style="position:absolute;right:46px;top:30px;width:170px;height:170px;border-radius:50%;background:#FFC845;color:#0B1A2C;display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(10deg);box-shadow:0 20px 40px rgba(0,0,0,.35)"><div style="font-weight:900;font-size:58px;line-height:1">-50%</div><div style="font-weight:700;font-size:17px;letter-spacing:.1em">TODA LA MARCA</div></div>
""")
# 2 Hero móvil 900x1200
LAYOUTS["hero-movil-900x1200"]=(900,1200,f"""
<div class="glow" style="width:1000px;height:1000px;left:-50px;top:-300px"></div>
<div style="position:absolute;left:0;right:0;top:50px;text-align:center">{logo(0.85)}</div>
<div style="position:absolute;left:60px;right:60px;top:150px">{textblock(0.66,'center',cta=False)}</div>
<div class="card" style="position:absolute;left:70px;top:570px;width:360px;height:440px;transform:rotate(-3deg)"><img src="{P['modo']}"></div>
<div class="card" style="position:absolute;left:460px;top:560px;width:370px;height:215px"><img src="{P['rosa']}"></div>
<div class="card" style="position:absolute;left:460px;top:795px;width:370px;height:215px"><img src="{P['shop']}"></div>
<div style="position:absolute;left:0;right:0;bottom:60px;text-align:center"><div class="cta" style="font-size:28px;padding:20px 60px">Comprar ahora</div><div style="margin-top:18px">{foot(0.85)}</div></div>
""")
# 3 Banner colección 1920x500
LAYOUTS["banner-coleccion-1920x500"]=(1920,500,f"""
<div class="glow" style="width:900px;height:900px;left:-200px;top:-250px"></div>
<div style="position:absolute;left:110px;top:95px">
 <div class="k" style="font-size:16px;margin-bottom:12px">Especial de marca · hasta el 31 de diciembre</div>
 <div style="display:flex;align-items:flex-end;gap:28px"><div class="brand" style="font-size:96px;line-height:.9">TUCANO</div><div class="big" style="font-size:170px">50%</div></div>
 <div class="sub" style="font-size:26px;margin-top:14px">de descuento en mochilas, maletines, fundas y accesorios originales.</div>
 <div class="fine" style="font-size:16px;margin-top:18px">Válido en ventasguate.gt o hasta agotar existencias.</div>
</div>
<div class="card" style="position:absolute;left:1120px;top:60px;width:240px;height:380px"><img src="{P['modo']}"></div>
<div class="card" style="position:absolute;left:1385px;top:60px;width:240px;height:380px"><img src="{P['isotta']}"></div>
<div class="card" style="position:absolute;left:1650px;top:60px;width:220px;height:380px"><img src="{P['alunno']}"></div>
""")
# 4 Post 1080x1080
LAYOUTS["post-1080x1080"]=(1080,1080,f"""
<div class="glow" style="width:1100px;height:1100px;left:-400px;top:-300px"></div>
<div style="position:absolute;left:70px;top:70px">{logo(0.8)}</div>
<div style="position:absolute;left:70px;top:160px">
 <div class="k" style="font-size:17px;margin-bottom:12px">Especial de marca</div>
 <div class="brand" style="font-size:62px">TUCANO</div>
 <div class="big" style="font-size:190px">50%</div>
 <div class="brand" style="font-size:42px;margin-top:8px">de descuento</div>
</div>
<div class="card" style="position:absolute;left:600px;top:110px;width:410px;height:540px;transform:rotate(3deg)"><img src="{P['modo']}"></div>
<div class="card" style="position:absolute;left:70px;top:700px;width:300px;height:230px"><img src="{P['rosa']}"></div>
<div class="card" style="position:absolute;left:390px;top:700px;width:300px;height:230px"><img src="{P['shop']}"></div>
<div class="card" style="position:absolute;left:710px;top:700px;width:300px;height:230px"><img src="{P['morado']}"></div>
<div style="position:absolute;left:70px;right:70px;bottom:52px;display:flex;justify-content:space-between;align-items:center">{foot(0.9)}<div class="fine" style="font-size:18px;color:#FFC845;font-weight:700">ventasguate.gt</div></div>
""")
# 5 Story 1080x1920
LAYOUTS["story-1080x1920"]=(1080,1920,f"""
<div class="glow" style="width:1400px;height:1400px;left:-200px;top:-400px"></div>
<div style="position:absolute;left:0;right:0;top:150px;text-align:center">{logo(1)}</div>
<div style="position:absolute;left:60px;right:60px;top:290px">{textblock(0.98,'center',cta=False)}</div>
<div class="card" style="position:absolute;left:90px;top:1060px;width:470px;height:540px;transform:rotate(-3deg)"><img src="{P['modo']}"></div>
<div class="card" style="position:absolute;left:590px;top:1050px;width:400px;height:260px"><img src="{P['rosa']}"></div>
<div class="card" style="position:absolute;left:590px;top:1335px;width:400px;height:260px"><img src="{P['shop']}"></div>
<div style="position:absolute;left:0;right:0;bottom:150px;text-align:center"><div class="cta" style="font-size:36px;padding:24px 70px">Compra en ventasguate.gt</div><div style="margin-top:26px">{foot(1)}</div></div>
""")


os.makedirs(f"{S}/html",exist_ok=True)
jobs=[]
for name,(w,h,body) in LAYOUTS.items():
    open(f"{S}/html/{name}.html","w").write(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body style='width:{w}px;height:{h}px;position:relative'>{body}</body></html>")
    jobs.append([name,w,h])
json.dump(jobs,open(f"{S}/html/jobs.json","w"))
