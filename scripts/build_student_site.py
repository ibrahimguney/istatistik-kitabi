"""Build the student portal using only the Python standard library.
Run: python scripts/build_student_site.py
Content and course levels follow main.tex and izlence-rotasi-combined.tex.
"""
from pathlib import Path
from html import escape as e
import re
import zipfile
import hashlib
import json
ROOT = Path(__file__).resolve().parents[1]
GH = 'https://github.com/ibrahimguney/istatistik-kitabi'
TITLES = ['İstatistiksel düşünme, veri ve araştırma','Grafiksel ve sayısal betimleme','Eksik veri ve veri kalitesi','Örnekleme yöntemleri ve yanlılık','Örnekleme dağılımları','Normal dağılım, standart puanlar ve MLT','Nokta tahmini','Güven aralıkları','Bootstrap ve rastgeleleştirme','Hipotez testleri, hata, güç ve etki','Tek, bağımsız ve eşleştirilmiş t testleri','ANOVA ve grup karşılaştırmaları','Kategorik veri ve ki-kare','Korelasyon','Basit doğrusal regresyon','Parametrik olmayan yöntemler','Ölçek puanlarının güvenirliği','Çoklu doğrusal regresyon','Bütünleştirici veri analizi laboratuvarı','Genel değerlendirme ve yöntem seçimi']
PACKAGES = [['b01','b02'],['b03'],['eksik-veri'],['b06'],['b04'],['b05'],['b07'],['b08'],['bootstrap'],['b09','b10'],['b10','b11'],['anova'],['b12'],['b13'],['b13'],['nonparametrik'],['guvenirlik'],['coklu-regresyon'],['laboratuvar'],['b14']]
# Portable archives include all inputs and instructions for the four new packages.
NEW_PACKAGES = ['eksik-veri','nonparametrik','guvenirlik','laboratuvar']
(ROOT/'downloads').mkdir(exist_ok=True)
for slug in NEW_PACKAGES:
    base=ROOT/'companion/bolumler'/slug
    files=sorted(p for p in base.rglob('*') if p.is_file() and p.name!='MANIFEST.sha256' and not p.name.startswith('sonuclar-') and '__pycache__' not in p.parts)
    (base/'MANIFEST.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.relative_to(base).as_posix()+'\n' for p in files))
    with zipfile.ZipFile(ROOT/'downloads'/f'{slug}.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in files+[base/'MANIFEST.sha256']:
            info=zipfile.ZipInfo(slug+'/'+p.relative_to(base).as_posix(),date_time=(2026,9,23,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,p.read_bytes())
GROUPS = ['Veri ve betimleme','Örnekleme ve tahmin','İstatistiksel çıkarım','İlişki ve modelleme','Genel değerlendirme']
SOURCES = re.findall(r'\\input\{(chapters/[^}]+)\}', (ROOT/'main.tex').read_text())
assert len(SOURCES)==len(TITLES)==20

def level(n,course):
    if n==19:return 'Uygulama'
    if n==20:return 'Tekrar'
    if n==9:return 'Destek'
    if course=='imo':return 'İleri okuma' if n==18 else 'Destek' if n in [12,16,17] else 'Temel'
    return 'Destek' if n in [13,18] else 'Temel'

def group(n):return 0 if n<=4 else 1 if n<=9 else 2 if n<=12 else 3 if n<=19 else 4

def shell(title,body,prefix=''):
    return f'''<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="İbrahim Güney'in birleşik istatistik kitabı: IMO301 ve PDR209 ders rotaları, bölüm uygulamaları ve veri dosyaları."><title>{e(title)} | İstatistik</title><link rel="stylesheet" href="{prefix}web/style.css"><script defer src="{prefix}web/app.js"></script></head><body><a class="skip" href="#icerik">İçeriğe geç</a><header><a class="brand" href="{prefix}index.html"><span class="mark">σ</span> İstatistik <span class="brand-sub">ÇALIŞMA ALANI</span></a><nav aria-label="Ana menü"><a href="{prefix}index.html#bolumler">Bölümler</a><a href="{prefix}index.html#baslangic">Nasıl çalışırım?</a><a href="{GH}">GitHub ↗</a></nav></header><main id="icerik">{body}</main><footer><span>İbrahim Güney · İstatistik</span><span>Veri Okuryazarlığından İstatistiksel Çıkarıma</span><a href="{GH}/blob/main/LICENSE.md">Kullanım koşulları</a></footer></body></html>'''

def ghlink(path,label):return f'<a class="resource" href="{GH}/blob/main/{path}">{e(label)} <span>↗</span></a>'

def filelink(path,label):
    assert (ROOT/path).is_file(),path
    return f'<a class="resource" download href="../../{path}">{e(label)} <span>↓</span></a>'

cards=[]
for n,title in enumerate(TITLES,1):
    p=ROOT/'bolumler'/f'b{n:02}'
    p.mkdir(parents=True,exist_ok=True)
    packages=PACKAGES[n-1]
    status='Veri ve uygulama dosyaları' if packages else 'Bölüm kaynağı ve okuma başlıkları'
    cards.append(f'''<a class="chapter" href="bolumler/b{n:02}/index.html" data-title="{e(title)}" data-group="{group(n)}" data-imo="{level(n,'imo')}" data-pdr="{level(n,'pdr')}"><div class="card-top"><span class="number">{n:02}</span><span class="level">{e(GROUPS[group(n)])}</span></div><h3>{e(title)}</h3><p>{status}</p><span class="open">Bölümü aç <span>↗</span></span></a>''')
    source=SOURCES[n-1]+'.tex'
    raw=(ROOT/source).read_text()
    sections=re.findall(r'\\section\*?\{([^{}]+)\}',raw)
    sections=[re.sub(r'\\[a-zA-Z]+\s*','',x).replace('$','') for x in sections]
    outline='<ul>'+''.join('<li>'+e(x)+'</li>' for x in sections)+'</ul>' if sections else ''
    content=f'''<a class="back" href="../../index.html#bolumler">← Bütün bölümler</a><section class="chapter-hero"><p class="eyebrow">BÖLÜM {n:02} / {e(GROUPS[group(n)])}</p><h1>{e(title)}</h1><div class="tags"><span>IMO301 · {level(n,'imo')}</span><span>PDR209 · {level(n,'pdr')}</span></div></section><div class="detail-grid"><article><section class="panel"><h2>Bu bölümde</h2>{outline}{ghlink(source,'Kitaptaki bölüm kaynağını aç (LaTeX)')}</section>'''
    if not packages:
        content+='<section class="panel"><h2>Okuma ve çalışma</h2><p>Bu bölüm için henüz bağımsız bir indirme paketi eşleştirilmedi. Kitaptaki anlatım, örnekler ve alıştırmalar bölüm kaynağında bulunuyor.</p><p>Okurken kullanılan değişkenleri, yöntemin varsayımlarını ve sonuçların nasıl raporlandığını not edin.</p></section>'
    for package in packages:
        base=f'companion/bolumler/{package}'
        example=base+'/ornek-01'
        content+=f'<section class="panel"><p class="eyebrow">UYGULAMA PAKETİ · {package.upper()}</p><h2>Veriden yoruma</h2><p class="note">'
        content+= f'Bu paket birleşik kitabın {n}. bölümündeki öğretim verilerini kullanır.' if package in ['eksik-veri','nonparametrik','guvenirlik','laboratuvar'] else f'Paket içindeki bölüm numaraları önceki kitap düzenine aittir. Bu sayfa birleşik kitabın {n}. bölümüne yönlendirir.'
        if n in [14,15]:content+=' Korelasyon ve basit regresyon aynı uygulama paketini paylaşır.'
        if package=='b10':content+=' Bu paket güç ve tek örneklem t testi çalışmalarında ortak kullanılır.'
        content+='</p>'
        if package in NEW_PACKAGES: content+=filelink(f'downloads/{package}.zip','Tüm paketi indir · ZIP')
        content+='<div class="resources">'
        for filename,label in [('veri.csv','Veri seti · CSV'),('esli.csv','Eşleştirilmiş farklar · CSV'),('uc-grup.csv','Üç grup verisi · CSV'),('guvenirlik.csv','Kitap kodu için veri · CSV'),('veri-sozlugu.csv','Değişken sözlüğü · CSV'),('beklenen-sonuclar.csv','Beklenen sonuçlar · CSV'),('cozum.py','Python kodu · .py'),('cozum.R','R kodu · .R'),('analiz.sps.txt','SPSS sözdizimi · .sps.txt')]:
            if (ROOT/example/filename).is_file():content+=filelink(example+'/'+filename,label)
        content+='</div><h3>1. Hazırlan ve çalıştır</h3><p>Veri, sözlük, beklenen sonuçlar ve seçtiğiniz yazılımın kodunu aynı klasöre kaydedin. Ek dosyalar ve gerekli paketler için önce çalıştırma rehberini okuyun. SPSS dosyasını kullanırken uzantısını <code>.sps</code> olarak değiştirin.</p>'
        if (ROOT/example/'README.md').exists():content+=ghlink(example+'/README.md','Örneğin verisi ve çalıştırma rehberi')
        content+=f'<a class="resource" href="{GH}/tree/main/{example}">Örneğin tüm dosyaları <span>↗</span></a>'
        if (ROOT/base/'alistirmalar.md').exists():content+='<h3>2. Kendin dene</h3>'+ghlink(base+'/alistirmalar.md','Alıştırmaları aç')
        content+='<details><summary>3. Çözüm ve sonuçlarla karşılaştır</summary>'
        for rel,label in [('ornek-01/cozum.md','Örneğin adım adım çözümü'),('cozumler.md','Alıştırmaların yanıtları'),('DOGRULAMA.md','Yazılımlara göre doğrulama kaydı')]:
            if (ROOT/base/rel).exists():content+=ghlink(base+'/'+rel,label)
        content+='</details><p class="small">Verinin kaynağı ve öğretim amaçlı olup olmadığı örnek rehberinde belirtilir. Kodun bulunması, her yazılımda çalıştırılarak doğrulandığı anlamına gelmez.</p></section>'
    content+='</article><aside><section class="panel"><p class="eyebrow">ÇALIŞMA AKIŞI</p><h2>Oku. Uygula. Yorumla.</h2><ol><li>Kitaptan konuyu oku.</li><li>Veriyi ve değişkenleri tanı.</li><li>Tercih ettiğin yazılımla uygula.</li><li>Sonucu bir cümleyle yorumla.</li><li>Alıştırmaları çözümden önce dene.</li></ol></section></aside></div><nav class="pagination" aria-label="Bölümler arası gezinme">'
    if n>1:content+=f'<a href="../b{n-1:02}/index.html">← {n-1:02} · {e(TITLES[n-2])}</a>'
    if n<20:content+=f'<a href="../b{n+1:02}/index.html">{n+1:02} · {e(TITLES[n])} →</a>'
    content+='</nav>'
    (p/'index.html').write_text(shell(title,content,'../../'))

body='''<section class="hero"><div><p class="eyebrow">İBRAHİM GÜNEY / BİRLEŞİK KİTAP</p><h1>Veriyi anla.<br>Kanıtla düşün.</h1><p class="lead">Veri okuryazarlığından istatistiksel çıkarıma.<br>İki ders, ortak bir kitap; bölüm bölüm uygulama.</p><a class="primary" href="#bolumler">Çalışmaya başla <span>↓</span></a></div><div class="hero-art" aria-hidden="true"><span class="art-label">ÖRNEKTEN EVRENE</span><svg viewBox="0 0 360 230"><g stroke="currentColor" opacity=".18"><path d="M20 180H340 M20 130H340 M20 80H340 M20 30H340 M80 20V200 M180 20V200 M280 20V200"/></g><path d="M20 180 C90 180 110 35 180 35 S270 180 340 180" fill="none" stroke="currentColor" stroke-width="3"/><path d="M110 155 Q145 35 180 35 Q215 35 250 155 L250 180 H110Z" fill="currentColor" opacity=".12"/><circle cx="180" cy="35" r="6" fill="currentColor"/><path d="M180 45V185" stroke="currentColor" stroke-dasharray="4 7"/></svg><div class="art-bottom"><span>20 bölüm</span><span>R · Python · SPSS</span></div></div></section>
<section class="intro" id="baslangic"><div><span class="step">01 / OKU</span><p>Kitabındaki bölümü seç.</p></div><div><span class="step">02 / UYGULA</span><p>Veriyi indir, kodu çalıştır.</p></div><div><span class="step">03 / YORUMLA</span><p>Alıştırmayla kendini dene.</p></div></section>
<section id="bolumler"><div class="section-heading"><div><p class="eyebrow">BÖLÜM REHBERİ</p><h2>Nereden devam edelim?</h2></div><p>Kitabın güncel 20 bölümlük sırasıyla.</p></div><div class="controls"><fieldset><legend>Ders rotası</legend><div class="route-buttons"><button type="button" data-course="all" aria-pressed="true">Bütün kitap</button><button type="button" data-course="imo" aria-pressed="false">IMO301</button><button type="button" data-course="pdr" aria-pressed="false">PDR209</button></div></fieldset><div><label for="search">Bölüm ara</label><input id="search" type="search" placeholder="Örn. güven aralıkları, ANOVA…"></div><div><label for="group">Konu alanı</label><select id="group"><option value="all">Tüm konular</option>'''+''.join(f'<option value="{i}">{g}</option>' for i,g in enumerate(GROUPS))+'''</select></div></div><p id="route-note" class="note">Bütün bölümler kitap sırasıyla gösteriliyor. Ders seçerek temel, destek ve ileri okuma etiketlerini görebilirsiniz.</p><p id="results" class="small" aria-live="polite">20 bölüm</p><div class="chapters">'''+''.join(cards)+'''</div><p id="empty" hidden>Bu aramayla eşleşen bölüm yok. Aramayı veya konu filtresini değiştirin.</p><noscript><p>Arama ve ders seçimi için JavaScript gerekir. Tüm bölüm bağlantıları aşağıdaki sırayla kullanılabilir.</p></noscript></section><section class="bottom-note"><h2>Kitap ve uygulamalar birlikte.</h2><p>Bu alan kitabın uygulama rehberidir. PDF yayımları ve kaynak dosyaları için proje deposunu kullanabilirsiniz.</p><div class="bottom-links"><a href="'''+GH+'''/releases">Yayımlar ↗</a><a href="'''+GH+'''">Kitap deposu ↗</a></div></section>'''
(ROOT/'index.html').write_text(shell('Çalışma alanı',body))
(ROOT/'.nojekyll').write_text('')
print('Built home page and 20 chapter pages.')
