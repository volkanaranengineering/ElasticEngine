"""Türkçe rapor, şemalar ve imalata esas olmayan 3B yerleşim üretir."""
from pathlib import Path
import os,json,csv,base64,html
root=Path(__file__).resolve().parents[1];out=root/'results/turkce_sunum';out.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(out/'mplconfig')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import FreeCAD as App, Part
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
summary=json.loads((root/'results/cnt_pulley_concept/summary.json').read_text())
with (root/'results/cnt_pulley_concept/reference.csv').open() as f: rows=list(csv.DictReader(f))
d={k:np.array([float(r[k]) for r in rows]) for k in rows[0]};t=d['time_s']
fig,axs=plt.subplots(2,2,figsize=(13,8),layout='constrained')
axs[0,0].plot(t/60,np.where(t<3600,100,0),color='#147d79');axs[0,0].set(xlabel='Süre (dakika)',ylabel='Mil gücü (kW)',ylim=(0,115),title='Öngörülen çıkış: 100 kW, 60 dakika')
for k,label in [('stored_J','Kalan elastik enerji'),('delivered_J','Mile aktarılan enerji'),('conversion_loss_J','Dönüşüm kaybı'),('relaxation_loss_J','Gevşeme kaybı')]:axs[0,1].plot(t/60,d[k]/3.6e6,label=label)
axs[0,1].legend(fontsize=8);axs[0,1].set(xlabel='Süre (dakika)',ylabel='Enerji (kWh)',title='Referans durum: enerji bilançosu')
lam=-np.log(.95)/3600;E0=summary[1]['initial_kWh']*3.6e6/200
for j in [0,9,19]:
    elapsed=np.clip(t-j*180,0,180);after=np.maximum(t-(j+1)*180,0)
    en=E0*np.exp(-lam*t)-10000/(.72675*lam)*(-np.expm1(-lam*elapsed))*np.exp(-lam*after)
    axs[1,0].plot(t/60,en/3.6e6,label=f'{j+1}. kartuş')
axs[1,0].set(xlabel='Süre (dakika)',ylabel='Kartuş enerjisi (kWh)',title='Her güç kolunda sıralı boşaltma');axs[1,0].legend(fontsize=8)
vals=[r['active_mass_kg'] for r in summary]
axs[1,1].bar(['İyimser','Referans','Düşük dönüşüm'],vals,color=['#73bcb1','#147d79','#b47a43'])
for i,v in enumerate(vals):axs[1,1].text(i,v+60,f'{v:,.0f} kg'.replace(',','.'),ha='center')
axs[1,1].set(ylabel='Etkin halat kütlesi (kg)',ylim=(0,4300),title='Ölçekleme ve verim varsayımlarının etkisi')
for a in axs.flat:a.grid(alpha=.18)
fig.suptitle('Karbon nanotüp elastik batarya — analitik zaman alanı sonuçları\nGüç komutu verilmiştir; geçiş dinamiği ve denetleyici doğrulanmamıştır',fontsize=14)
fig.savefig(out/'hesaplama_sonuclari.png',dpi=160);plt.close(fig)

# The drawing coordinates are deliberately arbitrary; the CAD is a layout study only.
doc=App.newDocument('KavramsalYerlesim');boxes=[]
def box(name,label,x,y,z,l,w,h,color):
    o=doc.addObject('PartDesign::Feature',name);o.Label=label
    o.Shape=Part.makeBox(l*100,w*100,h*100,App.Vector(x*100,y*100,z*100))
    o.addProperty('App::PropertyString','Aciklama');o.Aciklama='Temsili geometri; ölçüler ve dayanım doğrulanmamıştır.'
    boxes.append((x,y,z,l,w,h,color));return o
for lane in range(10):
    bx=(lane%5)*6;by=(lane//5)*6
    box(f'Taban{lane}',f'{lane+1}. güç kolu — taban',bx-.15,by-.15,0,5.5,2.6,.15,'#8b98a2')
    for row in range(5):
        for col in range(4):
            n=row*4+col+1
            box(f'K{lane}_{n}',f'Kol {lane+1} / Kartuş {n} — 0,5 kWh çıkış',bx+col*1.3,by,.4+row*.8,1.1,2,.6,'#58aaa3')
    box(f'Aktarim{lane}',f'{lane+1}. kol — kavrama ve değişken oranlı aktarım',bx+1.7,by+2.7,.3,1.8,1,.8,'#d7a34b')
    box(f'Baglanti{lane}',f'{lane+1}. kol — mekanik bağlantı',bx+2.4,by+3.7,.5,.3,1.2,.3,'#718492')
for row in range(2):box(f'Mil{row}',f'{row+1}. sıra — temsili toplama mili',0,row*6+4.7,.5,29,.25,.25,'#394c60')
box('Cikis','Ortak çıkış ve tampon bağlantısı',29,4,.3,2,3,1.1,'#d7a34b')
doc.recompute();doc.saveAs(str(out/'kavramsal_yerlesim.FCStd'))
Part.export(doc.Objects,str(out/'kavramsal_yerlesim.step'))
assert len([o for o in doc.Objects if o.Name.startswith('K') and o.Name[1:2].isdigit()])==200
fig=plt.figure(figsize=(14,7));ax=fig.add_subplot(111,projection='3d')
for x,y,z,l,w,h,c in boxes:
    v=np.array([[x,y,z],[x+l,y,z],[x+l,y+w,z],[x,y+w,z],[x,y,z+h],[x+l,y,z+h],[x+l,y+w,z+h],[x,y+w,z+h]])
    faces=[[v[i] for i in ids] for ids in [[0,1,2,3],[4,5,6,7],[0,1,5,4],[1,2,6,5],[2,3,7,6],[3,0,4,7]]]
    ax.add_collection3d(Poly3DCollection(faces,facecolors=c,edgecolors='#344f5c',linewidths=.25,alpha=.95))
ax.set(xlim=(-1,32),ylim=(-1,12),zlim=(0,5));ax.set_box_aspect((33,13,5));ax.view_init(elev=28,azim=-62);ax.set_axis_off()
fig.suptitle('Kavramsal 3B yerleşim: 10 güç kolu × 20 kartuş\nYeşil: kartuşlar | Sarı: güç aktarımı | Koyu: toplama milleri',fontsize=15)
fig.text(.5,.06,'Ölçeksiz yerleşim çalışmasıdır. Gerçek hacim, boyut, kütle ve mekanik bağlantılar doğrulanmamıştır.',ha='center',fontsize=11)
fig.savefig(out/'kavramsal_3b.png',dpi=160,bbox_inches='tight');plt.close(fig)

def svgbase(title,body,height=540):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}"><rect width="1200" height="{height}" fill="#f5f9fb"/><defs><marker id="ok" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L0,6 L8,3 z" fill="#287f78"/></marker></defs><style>text{{font-family:Arial;fill:#193b50}}.k{{fill:#dfefeb;stroke:#287f78;stroke-width:2}}.a{{stroke:#287f78;stroke-width:3;fill:none;marker-end:url(#ok)}}.r{{fill:#f5e8cb;stroke:#ba8732;stroke-width:2}}</style><text x="30" y="38" font-size="25">{title}</text>{body}</svg>'''
system=svgbase('Sistem şeması — 100 kWh kullanılabilir enerji / 100 kW mil gücü','''
<rect class="k" x="30" y="85" width="260" height="135" rx="8"/><text x="45" y="115" font-size="20">200 enerji kartuşu</text><text x="45" y="148" font-size="17">Her kartuş: 0,5 kWh çıkış</text><text x="45" y="177" font-size="17">5,62 kg etkin halat / referans</text><text x="45" y="205" font-size="17">Mekanik kilitleme ve ayırma</text>
<path class="a" d="M290 155 H335"/><rect class="k" x="340" y="85" width="260" height="135" rx="8"/><text x="355" y="115" font-size="20">10 bağımsız güç kolu</text><text x="355" y="148" font-size="17">Her kolda 20 sıralı kartuş</text><text x="355" y="177" font-size="17">10 kW / 180 saniye / kartuş</text><text x="355" y="205" font-size="17">Kavrama + değişken aktarım</text>
<path class="a" d="M600 155 H645"/><rect class="k" x="650" y="85" width="260" height="135" rx="8"/><text x="665" y="115" font-size="20">Ortak çıkış mili</text><text x="665" y="148" font-size="17">1.000 dev/dak</text><text x="665" y="177" font-size="17">955 N·m toplam döndürme momenti</text><text x="665" y="205" font-size="17">Ters yönde mekanik doldurma</text><path class="a" d="M910 155 H950"/><text x="965" y="150" font-size="24">100 kW</text><text x="965" y="180" font-size="19">60 dakika</text>
<path class="a" d="M780 220 V275"/><rect class="r" x="650" y="285" width="430" height="80" rx="8"/><text x="670" y="316" font-size="19">İsteğe bağlı volan tamponu: 20 kJ</text><text x="670" y="346" font-size="17">0,2 saniyelik geçiş boşluğunu karşılar</text>
<rect class="r" x="30" y="285" width="520" height="80" rx="8"/><text x="50" y="315" font-size="19">Algılayıcılar ve denetleyici</text><text x="50" y="345" font-size="17">Devir, moment, burulma, uzama, sıcaklık → kavrama / oran</text>
<text x="30" y="425" font-size="18">Yüksek verimli toplama mekanizması tasarım hedefidir; makalede doğrulanmış bir büyük sistem değildir.</text><text x="30" y="462" font-size="17">Çıkış gücü analitik modelde verilidir. Gerçek geçişler, volan kayıpları ve denetim dinamiği modele dahil değildir.</text>
''')
cell=svgbase('Kartuş içi çalışma ilkesi — burulma ve eksenel işin birlikte toplanması','''
<rect class="k" x="35" y="85" width="190" height="205" rx="8"/><text x="50" y="118" font-size="20">Sabit mesnet</text><text x="50" y="150" font-size="16">Ortak tutucular</text><text x="50" y="180" font-size="16">Kısa halat hücreleri</text><text x="50" y="210" font-size="16">Yüzey koruması</text><text x="50" y="240" font-size="16">Kilit ve ayırıcı</text>
<path d="M225 130 H390 Q420 130 420 160 Q420 190 390 190 H270 Q240 190 240 220 Q240 250 270 250 H455" fill="none" stroke="#287f78" stroke-width="6"/>
<circle cx="390" cy="160" r="22" fill="#f5e8cb" stroke="#ba8732"/><circle cx="270" cy="220" r="22" fill="#f5e8cb" stroke="#ba8732"/>
<text x="240" y="325" font-size="16">Temsili makara / kılavuz yolu</text><text x="240" y="350" font-size="15">Halat eğilmesi ve sürtünme çözülmelidir</text>
<rect class="k" x="470" y="85" width="270" height="205" rx="8"/><text x="485" y="118" font-size="20">Hareketli toplayıcı</text><text x="485" y="150" font-size="17">Dönme: T dφ</text><text x="485" y="182" font-size="17">Eksenel ötelenme: F dx</text><text x="485" y="215" font-size="17">İki hareket için yataklama</text><text x="485" y="250" font-size="16">Eşlenik yer değiştirme ölçümü</text>
<path class="a" d="M740 135 H800"/><path class="a" d="M740 235 H800"/><rect class="r" x="815" y="85" width="345" height="205" rx="8"/><text x="830" y="118" font-size="20">Mekanik iş toplama</text><text x="830" y="150" font-size="17">Dönel yol → kavrama</text><text x="830" y="185" font-size="17">Doğrusal yol → dönel dönüştürücü</text><text x="830" y="220" font-size="17">Oran uyarlama → kol çıkışı</text><text x="830" y="255" font-size="16">Sabit vida adımı henüz seçilemez</text>
<text x="35" y="415" font-size="18">Makaralı yerleşim makalenin Şekil 6 önerisinden esinlenmiştir; bu çift hareketli toplayıcı bizim önerimizdir.</text><text x="35" y="450" font-size="17">Bu çizim kinematik olarak doğrulanmış bir mekanizma veya üretim resmi değildir.</text>
''',500)
(out/'sistem_semasi.svg').write_text(system,encoding='utf-8');(out/'kartus_semasi.svg').write_text(cell,encoding='utf-8')
def img(name):return '<img src="data:image/png;base64,'+base64.b64encode((out/name).read_bytes()).decode()+'">'
def trnum(v,digits=2):return f'{v:,.{digits}f}'.replace(',','X').replace('.',',').replace('X','.')
table=''.join('<tr><td>'+label+'</td>'+''.join('<td>'+trnum(r[key],digits)+'</td>' for r in summary)+'</tr>' for label,key,digits in [('Etkin halat kütlesi (kg)','active_mass_kg',1),('Kartuş başına etkin halat (kg)','active_mass_per_cartridge_kg',2),('Başlangıç enerjisi (kWh)','initial_kWh',2),('Çıkış enerjisi (kWh)','delivered_kWh',2),('Dönüşüm kaybı (kWh)','conversion_loss_kWh',2),('Gevşeme kaybı (kWh)','relaxation_loss_kWh',2),('Kalan enerji (kWh)','residual_kWh',2),('%50 etkin kütle varsayımıyla toplam (kg)','total_mass_if_half_active_kg',1),('Bu varsayımla özgül çıkış enerjisi (Wh/kg)','delivered_Wh_kg_if_half_active',2)])
report='''<!doctype html><html lang="tr"><meta charset="utf-8"><title>Karbon nanotüp elastik batarya — Türkçe teknik sonuç raporu</title><style>body{font:17px/1.65 Arial,sans-serif;color:#193447;background:#edf3f6;margin:0}main{max-width:1150px;margin:auto;background:white;padding:45px}h1{font-size:36px;line-height:1.2}h2{margin-top:42px;color:#126d69}h3{color:#24546c}table{border-collapse:collapse;width:100%;font-size:15px}th,td{padding:10px;border-bottom:1px solid #d8e2e7;text-align:right}th:first-child,td:first-child{text-align:left}th{background:#e0efeb}img,svg{width:100%;height:auto}.note{padding:18px;background:#fff1d9;border-left:5px solid #c18c38}.lead{font-size:21px}a{color:#087b80}code{background:#edf3f6}small{color:#526676}@media print{body{background:white}main{padding:0}h2{break-after:avoid}table,img,svg{break-inside:avoid}}</style><main>
<p>TEKNİK KAVRAM RAPORU · 25 EKİM 2026</p><h1>Karbon nanotüp elastik batarya<br>100 kWh enerji · 100 kW mekanik güç</h1>
<p class="lead">Kısa halat hücreleri, makaralı düzenek ve sıralı boşaltılan kartuşlarla bir saat süreli mekanik güç üretimi.</p>
<p class="note"><b>Sonuç:</b> Referans hesap 1.124,6 kg etkin halat gerektirir. Etkin halat toplam kütlenin yarısı olabilirse sistem kütle bütçesi 2.249,3 kg olur. İkinci değer donanım hesabı değil, sınanacak bir tasarım hedefidir. Makale ölçeğinden bu sisteme geçiş henüz doğrulanmamıştır.</p>
<h2>1. Tasarım görevi ve temel değerler</h2><table><tr><th>Büyüklük</th><th>Referans değer</th></tr><tr><td>Kullanılabilir mil enerjisi</td><td>100 kWh = 360 MJ</td></tr><tr><td>Sürekli çıkış gücü / süre</td><td>100 kW / 60 dakika</td></tr><tr><td>Mil devri / toplam döndürme momenti</td><td>1.000 dev/dak / 955 N·m</td></tr><tr><td>Güç kolu / kartuş sayısı</td><td>10 kol / 200 kartuş</td></tr><tr><td>Bir kartuşun çıkışı</td><td>10 kW × 180 saniye = 0,5 kWh</td></tr><tr><td>Başlangıç elastik enerji birikimi</td><td>160,73 kWh</td></tr><tr><td>Ortalama dönüşüm ve gevşeme ısısı</td><td>42,17 kW</td></tr></table>
<h2>2. Kaynak ile tasarım varsayımlarının ayrılması</h2><p>Temel kaynak, Utsumi ve arkadaşlarının 2024 tarihli çalışmasıdır [1]. Termoplastik poliüretanla değiştirilmiş tek duvarlı karbon nanotüp halatlarda 2,1 MJ/kg özgül enerji bildirilir. İş hesabı hem burulmayı hem eksenel hareketi içerir. Şekil 6, makaralı ve dikiş benzeri sık yerleşimi önerir. Küçük numunelerden büyük sisteme geçiş deneysel olarak gösterilmiş değildir.</p>
<p>Yaklaşık %90 şekil değiştirme enerjisi geri kazanımı ile disk deneyindeki %22 enerji dönüşümü farklı ölçümlerdir. Bunlar aynı verim kabul edilmemiştir. Buradaki kartuş gruplaması, çift hareketli toplayıcı, güç kolları ve ortak mil, kaynaktan hareketle geliştirilmiş mühendislik önerileridir.</p>
<h2>3. Sistem ve kartuş şemaları</h2>'''+system+'''<p>Her güç kolu yirmi kartuşu sırayla devreye alır. Kartuşun dönel ve eksenel işi ortak aktarım yoluna bağlanır. Değişken aktarım oranı, azalan elastik yük altında çıkış devrini korumayı amaçlar. Kilit, bekleyen kartuşu tutar; kavrama, güç aktarımını seçer.</p>'''+cell+'''
<p>Şemalar işlevleri açıklar; yatak ölçüsü, makara çapı, tutucu dayanımı ve aktarım oranı için yeterli kuvvet–yer değiştirme ve moment–açı verisi yoktur. Bu nedenle şemalardan üretime geçilemez.</p>
<h2>4. Kavramsal üç boyutlu yerleşim</h2>'''+img('kavramsal_3b.png')+'''<p>İki sırada beşer güç kolu; her kolda dört sütun ve beş seviyede yirmi kartuş gösterilmiştir. Yeşil hacimler enerji kartuşlarını, sarı hacimler güç aktarım birimlerini temsil eder. Ortak miller ve bağlantılar yalnızca yer tutucudur.</p><p class="note"><b>3B modelin sınırı:</b> CAD dosyası gerçek katı geometriler içerir; koordinatlar görselleştirme amacıyla seçilmiştir. Hacimsel enerji yoğunluğu, bakım boşlukları, aktarım kinematiği, gerçek boyutlar ve gerilme hesabı doğrulanmamıştır. Ölçüler kütle hesabında kullanılmamalıdır.</p>
<h2>5. Hesaplama modeli ve varsayımlar</h2><p>Her kartuşun enerji dengesi, etkin olduğunda <b>dE/dt = −λE − P/η</b>, beklerken <b>dE/dt = −λE</b> biçimindedir. Burada P = 10 kW, η boşaltma dönüşüm verimi ve λ = −ln(r)/3.600 bağıntısındaki r bir saatlik yüksüz enerji tutma oranıdır. Son kartuş, boşaltma sonunda yüksüz durumda kalacak enerjisinin %10'unu koruyacak şekilde boyutlandırılır.</p>
<p>Bir kartuşun başlangıç enerjisi: <b>E₀ = [P/(ηλ)] [exp(λΔt)−1] exp[λ(n−1)Δt] / (1−b)</b>; Δt = 180 s, n = 20 ve b = 0,10. Etkin malzeme kütlesi <b>m = 200E₀/e</b> ile bulunur.</p>
<table><tr><th>Varsayım</th><th>İyimser</th><th>Referans</th><th>Düşük dönüşüm</th></tr><tr><td>Etkin yükleme enerjisi (Wh/kg)</td><td>583,33</td><td>142,92</td><td>142,92</td></tr><tr><td>Boşaltma dönüşüm verimi</td><td>%82,935</td><td>%72,675</td><td>%22</td></tr><tr><td>Bir saat yüksüz enerji tutma</td><td>%99</td><td>%95</td><td>%95</td></tr></table>
<p>Referansta 583,33 Wh/kg değeri, ölçek büyütme için 0,5 ve çalışma burulması için 0,7² katsayılarıyla azaltılmıştır. Karesel burulma bağıntısı yaklaşımıdır; yorulma emniyeti kanıtı değildir. Referans dönüşüm çarpımı 0,90 × 0,85 × 0,95'tir: halat geri kazanımı, iş toplama ve son aktarım. %22 durumu yalnızca düşük yararlı dönüşüm duyarlılığıdır; ayrıca %90 ile çarpılmamıştır.</p>
<h2>6. Hesaplanan zaman alanı sonuçları</h2>'''+img('hesaplama_sonuclari.png')+'''<table><tr><th>Sonuç</th><th>İyimser</th><th>Referans</th><th>Düşük dönüşüm</th></tr>'''+table+'''</table>
<p>Referans enerji bilançosu: <b>160,73 = 100,00 + 37,60 + 4,57 + 18,56 kWh</b>. Sırasıyla mil çıkışı, dönüşüm kaybı, gevşeme kaybı ve kalan enerji gösterilmiştir. 100 kW güç grafiği modelin verilen komutudur; kararlı bir gerçek denetleyicinin deneysel sonucu değildir.</p>
<p>Bu çalışma kapalı biçimli çözümün bir saniyelik adımlarla değerlendirilmesidir; yeni bir çok cisimli dinamik veya sonlu elemanlar çözümü değildir. Bağımsız sayısal gevşeme integrali ile enerji hesabı arasındaki fark bütün durumlarda 0,03 J'den küçüktür. Bu kontrol denklemlerin uygulanmasını doğrular, malzeme varsayımlarını doğrulamaz.</p>
<h2>7. Geçiş tamponu ve ısıl yönetim</h2><p>0,2 saniyelik güç kesintisini köprülemek için 20 kJ kullanılabilir tampon gerekir. Örnek bir volanın 6.000'den 5.400 dev/dak'a inmesi halinde gerekli atalet momenti yaklaşık 0,533 kg·m² olur. 0,25 m yarıçaplı ideal ince halka karşılığı 8,53 kg'dır; bu değer yatak, muhafaza, bağlantı ve güvenli rotor hesabını içermez. Volanın toplam enerjisi yaklaşık 105 kJ'dır. Geçiş ve tampon kayıpları ana hesaba eklenmemiştir.</p>
<p>Referanstaki yaklaşık 42,17 kW ısı uzaklaştırma gereksinimi, yalnızca enerji taşıyıcı kütlesine odaklanmanın yetersizliğini gösterir. Soğutma sistemi boyutlandırılmadan toplam kütle hedefi doğrulanamaz.</p>
<h2>8. Önceki hidrolik tasarımla karşılaştırma</h2><table><tr><th>Yaklaşım</th><th>100 kWh için hesaplanan malzeme</th><th>Kritik sınır</th></tr><tr><td>Karbon çekme demeti + hidrolik</td><td>45,04 ton lif + 17,93 ton çalışma yağı</td><td>Silindirler ve taşıyıcılar hariç</td></tr><tr><td>Bu CNT burulma kavramı / referans</td><td>1,125 ton etkin halat</td><td>Ölçek büyütme ve toplayıcı doğrulanmamış</td></tr><tr><td>Bu kavram / %50 etkin kütle hedefi</td><td>2,249 ton toplam kütle bütçesi</td><td>Hesaplanmış donanım kütlesi değildir</td></tr></table><p>Tablo aynı mekanik çıkış hedefini kullanır ancak malzeme olgunlukları eşit değildir. CNT sonucunu kanıtlanmış bir hafiflik üstünlüğü olarak yorumlamak doğru olmaz.</p>
<h2>9. Doğrulama gerektiren başlıklar</h2><ol><li>Kısa numunede eksenel ve burulma işinin birlikte geri kazanılması.</li><li>Çok hücreli makara düzeneğinde sürtünme, kayma ve eşitsiz yük paylaşımı.</li><li>Tutucu ve yataklarla birlikte gerçek kullanılabilir Wh/kg ölçümü.</li><li>Moment–açı–uzama eğrilerinden aktarım oranı ve denetim bant genişliğinin bulunması.</li><li>Bekleme süresi, nem, sıcaklık ve çevrim sayısına bağlı kapasite değişimi.</li><li>0,5 kWh / 10 kW kartuşun ardından tam güç kolu deneyi.</li></ol><p>Bu adımlar tamamlanmadan 100 kWh tesisin gerçek boyutu, maliyeti veya toplam kütlesi verilemez.</p>
<h2>10. Kaynakça</h2><ol><li>Utsumi ve diğerleri (2024), <i>Giant nanomechanical energy storage capacity in twisted single-walled carbon nanotube ropes</i>. <a href="https://doi.org/10.1038/s41565-024-01645-x">Nature Nanotechnology, DOI: 10.1038/s41565-024-01645-x</a>. Temel deney ve Şekil 6.</li><li>Hill, Havel ve Livermore (2009), <i>Modeling mechanical energy storage in springs based on carbon nanotubes</i>. <a href="https://doi.org/10.1088/0957-4484/20/25/255704">Nanotechnology, DOI: 10.1088/0957-4484/20/25/255704</a>. Yay mimarilerinin modellenmesi.</li><li>Hill ve diğerleri (2009), <i>Storing elastic energy in carbon nanotubes</i>. <a href="https://doi.org/10.1088/0960-1317/19/9/094015">Journal of Micromechanics and Microengineering</a>. Küçük ölçekli yay deneyleri.</li><li>Fthenakis ve diğerleri (2013), <i>Limits of mechanical energy storage and structural changes in twisted carbon nanotube ropes</i>. <a href="https://doi.org/10.1103/PhysRevB.88.245402">Physical Review B</a>. Bağlaşık şekil değiştirme ve tersinmezlik.</li><li>Zhan ve diğerleri (2020), <i>High density mechanical energy storage with carbon nanothread bundle</i>. <a href="https://doi.org/10.1038/s41467-020-15807-7">Nature Communications</a>. Demet ölçeği ve alternatif karbon nanoiplik yaklaşımı.</li></ol>
<h2>11. Teslim dosyaları</h2><p>Bu HTML raporu şekilleri içinde taşır ve tek başına açılabilir. Ayrı dosyalar: <code>hesaplama_sonuclari.png</code>, <code>sistem_semasi.svg</code>, <code>kartus_semasi.svg</code>, <code>kavramsal_3b.png</code>, <code>kavramsal_yerlesim.FCStd</code> ve <code>kavramsal_yerlesim.step</code>. Önceki hesaplama verileri <code>results/cnt_pulley_concept</code> klasöründedir.</p><p>Yeniden üretim: mevcut Python ile <code>scripts/cnt_pulley_concept.py</code>, ardından <code>scripts/turkce_sonuc_sunumu.py</code>. Yeni yazılım yüklenmemiştir.</p></main></html>'''
from mekanik_aciklama_tr import olustur
report=report.replace('<h2>4. Kavramsal üç boyutlu yerleşim</h2>',olustur(out)+'<h2>4. Kavramsal üç boyutlu yerleşim</h2>')
(out/'TEKNIK_SONUC_RAPORU_TR.html').write_text(report,encoding='utf-8')
print('Tamamlandı:',out)
print('CAD katı sayısı:',len(doc.Objects),'Kartuş sayısı: 200')
