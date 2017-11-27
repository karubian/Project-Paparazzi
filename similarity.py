import difflib as dl
import numpy
from math import sqrt, log

a = """Mazhar Alanson, bir dergi için objektif karşısına geçti.İlk gençlik yılları için, "Çok zor bir adamdım. Hatta kötü bir insan olduğumu bile söyleyebilirim" diyen Alanson, tasavvufla tanışınca değiştiğini anlattı: "İlerleyen yıllarda tasavvufla hepsi bitti. Çünkü ahlakın ne kadar önemli olduğunu anladım. Gönül kırmanın kötülüğünü fark ettim."""
b = "Gençliğinde çok zor bir adam olduğunu söyleyen Mazhar Alanson, ''Dahası kötü biriydim. 30'lu yaşlarda tasavvuf ile tanışınca değiştim. Kötülükler bitti. Çünkü ahlakın ne kadar önemli olduğunu anladım, kalp kırmanın kötülüğünü fark ettim'' dedi."


c = "Şarkıcı Dilan Çıtak, babası İbrahim Tatlıses'e babalık davası açtı. Ancak Çıtak'ın davayı kazanabilmesi için nüfustaki babası Cem Çıtak'a karşı nesebin reddi davası açması gerekiyor."
d = "asdjak"

e = """Cumhurbaşkanı ve AK Parti Genel Başkanı Recep Tayyip Erdoğan, partisinin TBMM Grup Toplantısı'nda yaptığı konuşmada "Yıllardır adeta yenilmez bir canavar gibi takdim edilen DEAŞ'ın, sahada sergilenen tüm kirli ayak oyunlarına rağmen aslında ne kadar kof bir yapı olduğunu dünyaya gösteren Türkiye olmuştur." dedi. Cumhurbaşkanı Erdoğan konuşmasında "Türkiye'yi NATO toplantılarındaki gibi terbiyesizliklerle, gizli-açık mesaj aracılığıyla tehdit edenlere, küçümseyenlere mesajımız şu: Tek millet, tek bayrak, tek vatan, tek devlet. Biz 80 milyonu tek millet olarak gördük. Onlar saldırdıkça biz saflarımızı daha da sıklaştırdık, ileriye doğru daha kararlı adımlar attık" ifadelerini kullandı."""
f = """AKP Genel Başkanı ve Cumhurbaşkanı Recep Tayyip Erdoğan, AKP Genişletilmiş İl Başkanları Toplantısı'na katıldı. AKP Genel Merkezi'nde düzenlenen toplantıda hitap eden Erdoğan, Myanmar'ın Arakan eyaletinin kuzeyindeki olaylara ilişkin açıklamalarda bulundu. Özellikle sosyal medyada yer alan bazı görüntülerle haberlerin Arakan'la ilgisi olmadığını belirten Cumhurbaşkanı Erdoğan, "Arakan, bizim için meçhul bir yer, hiçbir ilgimizin olmadığı bir coğrafya değildir. Arakan'daki sıkıntının uzun geçmişi olan karmaşık sebepleri bulunan farklı hesaplarla sürekli kaşınan meselelerden kaynaklandığını elbette biliyoruz. Medyada özellikle de sosyal medyada dolaşan görüntülerin, resimlerin, haberlerin pek çoğunun da Arakan ile ilgili yoktur. Bu resimlerin bir kısmı, bizdeki Gezi olayları ve bölücü örgütün çukur eylemleri dahil dünyadaki pek çok hadisede kullanılmıştır. Merkezi farklı yerde. Bölgeyle ilgili provokasyonlar, sadece medyayla sınırlı da değildir. Bir anda ortaya çıkan ve arkası karanlık silahlı örgütlerden yerel devlet güçlerinin hukukla insanlıkla bağdaşmayan davranışlarına kadar pek çok sorun birlikte yaşanıyor. Rohingya diasporasının da bu meselede zaman zaman farklı kaygılarla hareket ettiğini biliyoruz. Tüm bunlara rağmen orada milyonlarca insanın mağduriyetine yol açan gelişmelerin yaşandığı bir hakikattir. Bölgede Birleşmiş Milletler dahil neredeyse hiçbir uluslararası kuruluşun ve yardım örgütünün faaliyet göstermesine izin verilmemesi yaşanan hadiselerin vahametini ortaya koymaktadır" diye konuştu."""
g = """Cumhurbaşkanı Recep Tayyip Erdoğan, Almanya'nın bu günlerini iki ay öncesinden tahmin etmişti 24 Eylül'de yapılan genel seçimden iki gün sonra konuşan Cumhurbaşkanı Erdoğan, "Almanya'da seçim oldu. Bizde bir referandum oldu. Bu referandum sürecinde Türkiye'ye nasıl saldırdıklarını gördünüz. Şimdi kendi seçimlerinde bize saldırıyorlar. Seçimin bizimle ne alakası var? Almanya'da yaptığınız seçimde bizi niye kullanmaya çalışıyorsunuz. Ne oldu şimdi hükümet kuramayacaklar bak göreceksiniz. En az birkaç aylarını alır" açıklamasını yapmıştı."""



merve = """Uzun zamandır birlikte olduğu Murat Binici'yle ilişkisini noktayan Merve Özbey, ayrılık sonrası imaj yeniledi.Yeni imajıyla ilk kez Beyoğlu Jolly Joker'deki konserinde sevenlerinin karşısına çıkan şarkıcı, "Saçımın rengini açtık. Bunlar kadınsal hareketler" dedi.Hürriyet'in haberine göre; Özbey, ayrılıkla ilgili soruya ise "Evet evliliği hak eden bir ilişkiydi ama olmayınca olmuyor" diye yanıt verdi.Özbey, kıyafeti ve performansıyla büyük beğeni topladı.Merve Özbey'i dinlemeye gelenler arasında yakın arkadaşı İrem Derici de vardı. Derici, oturduğu yerden Özbey'in şarkılarına eşlik etti."""
mervegece = """Beyoğlu'nda bir mekanda sahne alan Merve Özbey, konseri öncesi ayrılık sorularını cevapladı. Özbey, “Evet evliliği hak eden bir ilişkiydi ama olmayınca olmuyor” diye yanıt verdi.Uzun zamandır birlikte olduğu Murat Binici’yle ilişkisini noktalayan Merve Özbey, ayrılık sonrası imaj yeniledi. Yeni imajıyla ilk kez Beyoğlu'nda bir mekandaki konserinde sevenlerinin karşısına çıkan şarkıcı, “Saçımın rengini açtık. Bunlar kadınsal hareketler” dedi. Özbey, ayrılıkla ilgili soruya ise “Evet evliliği hak eden bir ilişkiydi ama olmayınca olmuyor” diye yanıt verdi. Özbey, kıyafeti ve performansıyla büyük beğeni topladı. Merve Özbey'i dinlemeye gelenler arasında yakın arkadaşı İrem Derici de vardı. Derici, oturduğu yerden Özbey'in şarkılarına eşlik etti."""
sim = dl.get_close_matches

s = 0
wa = e.split()
wb = f.split()
for i in wa:
    a = sim(i, wb)
    if len(a)!= 0:
       # print(i)
       # print(a)
        s += 1

n = float(s) / float(len(wa))
print('%f%% similarity' % float(n * 100))


def cosine_sim(u,v):
    return numpy.dot(u,v) / (sqrt(numpy.dot(u,u)) * sqrt(numpy.dot(v,v)))

print(cosine_sim(a,b))