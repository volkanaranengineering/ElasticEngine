"""Mekanik işleyişi açıklayan ölçekten bağımsız çizimler; kinematik çözüm değildir."""
import base64
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Arc, FancyArrowPatch

def olustur(out):
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11})
    def rect(ax,x,y,w,h,text,color='#dceee9',fs=11):
        ax.add_patch(Rectangle((x,y),w,h,facecolor=color,edgecolor='#315666',lw=1.5))
        ax.text(x+w/2,y+h/2,text,ha='center',va='center',fontsize=fs)
    def arr(ax,a,b,color='#187f77',lw=2.5):
        ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=17,color=color,lw=lw))
    def save(fig,name):
        fig.savefig(out/(name+'.png'),dpi=170,bbox_inches='tight')
        svg=out/(name+'.svg')
        fig.savefig(svg,bbox_inches='tight');plt.close(fig)
        svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')

    fig,ax=plt.subplots(figsize=(15,7));ax.set(xlim=(0,16),ylim=(0,8));ax.axis('off')
    ax.set_title('A — Tek hücrenin açılmış mekanik görünümü\nHalat kendi ekseni etrafında burulur; eksenel hareket ayrıca izlenir',fontsize=17,pad=20)
    rect(ax,.4,2.8,.65,2.2,'1\nSabit\nmesnet',fs=9)
    rect(ax,1.05,3.5,.5,.8,'2',color='#b8c7d0')
    x=np.linspace(1.55,7.4,500)
    for phase in [0,np.pi]:ax.plot(x,3.9+.22*np.sin((x-1.55)*7+phase),color='#167b72',lw=3)
    ax.text(4.3,4.65,'3  CNT halat / çok hücreli düzenekte tekrarlanan eleman',ha='center',fontsize=11)
    rect(ax,7.1,2.8,2.5,2.2,'',color='#e9eef1')
    rect(ax,7.4,3.5,.5,.8,'4',color='#b8c7d0')
    ax.plot([7.9,10.7],[3.9,3.9],color='#b47c28',lw=7)
    for xx in [8.1,9.0]:
        ax.add_patch(Rectangle((xx,3.5),.25,.8,facecolor='white',edgecolor='#315666',lw=2))
    ax.text(8.35,5.4,'5  Döner mil ve yataklar\n6  Eksenel hareketli kızak',ha='center')
    for yy in [2.4,2.6]:ax.plot([6.6,10],[yy,yy],color='#5d7481',lw=3)
    arr(ax,(7.3,2.05),(9.6,2.05),color='#2367a0');ax.text(8.45,1.5,'x: iki yönde ötelenme\nYön, ölçülen halat davranışına bağlıdır',ha='center',fontsize=10)
    ax.add_patch(Arc((8.65,3.9),.8,1.6,theta1=35,theta2=310,color='#b47c28',lw=2.5));arr(ax,(8.94,3.29),(9.04,3.48),color='#b47c28')
    ax.text(10.1,4.6,'φ: dönme',color='#996211')
    rect(ax,11,3.3,4.2,1.25,'DÖNEL İŞ ÇIKIŞI\nAnlık güç: T × dφ/dt',color='#f4e3c4')
    arr(ax,(9.6,2.9),(10.7,1.5),color='#2367a0')
    rect(ax,11,.8,4.2,1.25,'EKSENEL İŞ ÇIKIŞI\nAnlık güç: F × dx/dt',color='#dce9f5')
    ax.text(.5,.35,'1–2: yükü gövdeye taşır. 4–6: dönen ve kayan ucu taşır. Her iki hareket de bekleme sırasında kilitlenmelidir.',fontsize=11)
    save(fig,'hucre_mekanigi')

    fig,axs=plt.subplots(2,2,figsize=(14,8),layout='constrained')
    states=[('1. DOLDURMA','Dış tahrik halata iş verir.','Dönme + eksenel hareket denetlenir.','#dce9f5'),('2. BEKLETME','Her iki serbestlik derecesi kilitlidir.','Enerji halatın şekil değiştirmesinde kalır.','#f4e3c4'),('3. BOŞALTMA','Halat kontrollü olarak geri şekil değiştirir.','Toplayıcı, mekanik işi güç koluna aktarır.','#dceee9'),('4. KARTUŞ DEĞİŞİMİ','Eski kartuşun yükü azaltılır; yenisi artırılır.','Geçişte toplam kol gücü 10 kW hedeflenir.','#eadff0')]
    for i,(ax,(title,a,b,c)) in enumerate(zip(axs.flat,states)):
        ax.set(xlim=(0,10),ylim=(0,6));ax.axis('off');ax.set_title(title,fontsize=15,fontweight='bold')
        rect(ax,.4,2.2,3.0,1.5,'CNT kartuş\nElastik enerji',c)
        rect(ax,4,2.2,2.3,1.5,'Kilitler +\nkavrama','#e8edf0')
        rect(ax,7,2.2,2.6,1.5,'Tahrik /\nçıkış mili',c)
        if i==0:arr(ax,(7,2.95),(6.3,2.95));arr(ax,(4,2.95),(3.4,2.95))
        elif i==1:
            ax.text(5.15,4.3,'Dönme kilidi: TUT\nEksenel kilit: TUT',ha='center',fontsize=11)
        else:arr(ax,(3.4,2.95),(4,2.95));arr(ax,(6.3,2.95),(7,2.95))
        ax.text(5,1.3,a,ha='center',fontsize=12);ax.text(5,.6,b,ha='center',fontsize=11)
        if i!=1:ax.text(5,4.5,'Kilit çözülmeden önce yük aktarımı kurulur.',ha='center',fontsize=10)
    fig.suptitle('B — Bir kartuşun çalışma çevrimi\nOklar enerji akışını gösterir; fiziksel dönme yönünü göstermez.',fontsize=16)
    save(fig,'calisma_cevrimi')

    fig,ax=plt.subplots(figsize=(15,7));ax.set(xlim=(0,16),ylim=(0,8));ax.axis('off')
    ax.set_title('C — Enerji halattan mile nasıl ulaşır?',fontsize=18)
    rect(ax,.3,3.1,2.3,1.8,'CNT hücreleri\nElastik enerji')
    rect(ax,3.5,5.0,3.4,1.2,'Dönel yol\nMil + kavrama',color='#f4e3c4')
    rect(ax,3.5,1.7,3.4,1.2,'Eksenel yol\nKızak + doğrusal/dönel çevirici',color='#dce9f5',fs=10)
    arr(ax,(2.6,4.4),(3.5,5.6),color='#b47c28');arr(ax,(2.6,3.6),(3.5,2.3),color='#2367a0')
    rect(ax,8,3.1,3.0,1.8,'İş toplama birimi\nOran ve yük uyumu',color='#eadff0')
    arr(ax,(6.9,5.6),(8,4.5),color='#b47c28');arr(ax,(6.9,2.3),(8,3.5),color='#2367a0')
    rect(ax,12,3.1,3.6,1.8,'Güç kolu çıkışı\n10 kW · 1.000 dev/dak\n95,5 N·m',color='#dceee9')
    arr(ax,(11,4),(12,4))
    ax.text(9.5,6.5,'İki girişi doğrudan rijit bağlamak yeterli değildir.\nHızlar ve yer değiştirmeler uyumlu olmalıdır.',ha='center',fontsize=11)
    ax.text(8,.7,'Pçıkış ≤ T·φ̇ + F·ẋ; yatak, kavrama ve aktarım kayıpları düşülür.\nEksenel işi toplamazsak makaledeki toplam enerji değerini kullanamayız.',ha='center',fontsize=13)
    save(fig,'iki_is_yolu')

    fig,ax=plt.subplots(1,2,figsize=(14,5),layout='constrained')
    tt=np.linspace(-.2,.2,101);w=(tt+.2)/.4
    ax[0].plot(tt,10*(1-w),label='Eski kartuş');ax[0].plot(tt,10*w,label='Yeni kartuş');ax[0].plot(tt,np.full_like(tt,10),'--',label='Toplam hedef')
    ax[0].set(xlabel='Geçiş merkezine göre süre (s)',ylabel='Kol gücü (kW)',title='Örnek 0,4 s örtüşme komutu');ax[0].legend()
    for lane in range(10):
        for slot in range(20):ax[1].broken_barh([(slot*3,2.92)],(lane+.15,.7),facecolors=['#167b72' if slot%2==0 else '#8ac6be'])
    ax[1].set(xlim=(0,60),ylim=(0,10),xlabel='Süre (dakika)',ylabel='Güç kolu',yticks=np.arange(10)+.5,yticklabels=np.arange(1,11),title='10 kol × 20 kartuş × 3 dakika')
    for a in ax:a.grid(alpha=.2)
    fig.suptitle('D — Kartuş geçişi ve bir saatlik çalışma\nSoldaki eğriler önerilen komuttur; geçiş benzetimi veya doğrulanmış denetim sonucu değildir.',fontsize=14)
    save(fig,'gecis_zamanlamasi')
    def image(name):return '<img alt="'+name+'" src="data:image/png;base64,'+base64.b64encode((out/(name+'.png')).read_bytes()).decode()+'">'
    section='''<h2>3A. Önce tek bir halat hücresini düşünelim</h2><p>Bu düzenekte enerji bir makarada veya dönen ağır bir kütlede depolanmaz. Depolama elemanı CNT halatın kendisidir. Halatın bir ucu mesnete bağlıdır; diğer ucu hem dönebilir hem eksen boyunca hareket edebilir. Doldururken dış tahrik bu uca mekanik iş verir. Boşaltırken halat geri şekil değiştirir ve bu işi geri verir.</p>'''+image('hucre_mekanigi')+'''<p><b>Çizimdeki çift sarmal yalnızca burulmayı görünür kılar;</b> gerçek halatın iç yapısını, helis adımını veya makaledeki mikroskobik geometriyi temsil etmez. Döner mil kızakla birlikte ötelenir; çizimdeki iş çıkışları bu hareketi kabul edebilen bağlantılar gerektirir. Yataklar sürtünmeyi azaltır ama enerji üretmez. Mesnet bütün tepkileri taşır.</p>
<h2>3B. Dört çalışma durumu</h2>'''+image('calisma_cevrimi')+'''<table><tr><th>Durum</th><th>Kilitler</th><th>Kavrama / denetim</th><th>Enerji akışı</th></tr><tr><td>Doldurma</td><td>Yük tahrike alındıktan sonra çözülür</td><td>Tahrik bağlı; burulma ve uzama birlikte denetlenir</td><td>Dış kaynak → halat</td></tr><tr><td>Bekletme</td><td>Dönel ve eksenel hareket tutulur</td><td>Yük kilitlere aktarıldıktan sonra tahrik ayrılabilir</td><td>İdeal olarak akış yok; gevşeme kaybı vardır</td></tr><tr><td>Boşaltma</td><td>Çıkış yolu yükü aldıktan sonra çözülür</td><td>Aktarım oranı ve moment denetlenir</td><td>Halat → iş toplayıcı → mil</td></tr><tr><td>Geçiş</td><td>Eski kartuş kalan yükünde yeniden tutulur</td><td>Yeni kartuş eşleştirilir; yük örtüşmeli aktarılır</td><td>İki kartuş kısa süre birlikte çıkış verir</td></tr></table><p>“Kilidi aç, sonra bağla” sırası kullanılmaz: bu, halatın denetimsiz çözülmesine neden olabilir. Önce kuvvet ve momenti karşılayan yol kurulur; sonra kilit yükü azaltılır. Bu sıra bir işlev şartıdır; kilit ve kavramaların ayrıntılı tasarımı henüz yapılmamıştır.</p>
<h2>3C. Neden iki ayrı iş yolu var?</h2>'''+image('iki_is_yolu')+'''<p>Bir yayı yalnızca döndürerek boşaltmak ile hem döndürüp hem uzama/kısalma hareketini toplamak aynı değildir. Makalenin enerji hesabı <b>∫T dφ + ∫F dx</b> içerir. İki hareketin işaretleri, deneyde ölçülen kuvvet–moment–yer değiştirme eğrileriyle belirlenmelidir; eksenel hareket her durumda kendiliğinden aynı yönde yararlı güç üretir varsayılmamıştır.</p><p><b>Çözülmemiş mekanizma:</b> “iş toplama birimi” hazır bir dişli kutusu değildir. Doğrusal hareketi dönmeye çeviren örneğin bir bilyalı vida, ancak gerekli yük ve hareket yörüngesi belirlendikten sonra seçilebilir. Sabit vida adımı ile sabit dişli oranı kullanmak, halatın doğal hareketini engelleyebilir. Bu nedenle çizim bir güç akışı şemasıdır; tüm parçaları kinematik olarak kapanmış bir makine olarak sunulmaz.</p>
<h2>3D. Tek hücreden 100 kW sisteme</h2><p>Çok sayıda küçük hücre, ortak tutucular ve kolektörlerle bir kartuş oluşturur. Ancak çok sayıda hücrenin aynı açıda burulması için yönlendirme ve yük paylaşımı gerekir; sıradan bir makaranın çevresinden halat geçirmek bunu otomatik sağlamaz. Makalenin Şekil 6 önerisi sık paketlemeye yöneliktir; bizim sistemde tutucu, kılavuz ve aktarım kayıpları ayrıca çözülmelidir.</p><p>Bir kartuş <b>10 kW × 180 s = 1,8 MJ = 0,5 kWh</b> mil enerjisi sağlar. Yirmi kartuş art arda bir güç kolunda 10 kWh verir. On kol paralel çalışınca 100 kWh ve 100 kW elde edilir. Referans kartuşun başlangıç enerjisi 0,8036 kWh ve etkin halat kütlesi 5,623 kg'dır; fark kayıplar ve kalan enerjidir. Kartuş, tek bir kalın halat değildir.</p>'''+image('gecis_zamanlamasi')+'''<p>Değişken aktarım oranı enerjiyi çoğaltmaz. Halatın momenti azalırken hız/moment dönüşümünü değiştirir. Çıkış 1.000 dev/dak'ta tutulursa bir güç kolu yaklaşık 95,5 N·m sağlamalıdır. Giriş momenti ve hız aralığı bilinmediğinden gerekli en küçük/en büyük aktarım oranı henüz hesaplanamaz.</p><p>Soldaki 0,4 saniyelik örtüşme sadece açıklayıcı komut örneğidir. İdeal saatlik hesapta anahtarlama anlıktır; dolayısıyla bu şekil yeni bir dinamik çözüm değildir. Örtüşme başarısızlığında 0,2 saniyeyi karşılayan 20 kJ volan tamponu düşünülebilir; volan da doldurulmalı ve kayıpları enerji bütçesine eklenmelidir.</p>
<h2>3E. 3B yerleşim nasıl okunmalı?</h2><p>Yeşil kutu bir halat değil, birçok hücre içeren kartuşun dış sınırıdır. Her dört sütun ve beş katlı grup bir güç koludur. Sarı kutular kavrama ve aktarım birimlerinin yer tutucusudur. Koyu çubuklar toplama millerini anlatır; gerçek mil bağlantıları, dişli temasları ve yataklar çizilmiş değildir. Önceki 3B model yerleşimi gösterir; yukarıdaki A–D çizimleri çalışma ilkesini açıklar.</p><p><b>Doğrulanmış olan:</b> belirtilen varsayımlar altında enerji bilançosu ve boşaltma programının aritmetiği. <b>Doğrulanmamış olan:</b> verimli çift iş toplama, küçük hücrelerin ortak tahriki, gerçek kavrama geçişi, bütün makinenin kütlesi ve çevrim ömrü.</p>'''
    (out/'MEKANIK_CALISMA_REHBERI_TR.html').write_text('<!doctype html><html lang="tr"><meta charset="utf-8"><title>Mekanik çalışma rehberi</title><style>body{font:18px/1.65 Arial;color:#193b50;max-width:1150px;margin:40px auto;padding:25px}img{width:100%}h2{color:#167b72}table{border-collapse:collapse;font-size:15px}td,th{border:1px solid #ccd9df;padding:10px}</style><h1>Elastik batarya nasıl çalışır?</h1>'+section,encoding='utf-8')
    return section
