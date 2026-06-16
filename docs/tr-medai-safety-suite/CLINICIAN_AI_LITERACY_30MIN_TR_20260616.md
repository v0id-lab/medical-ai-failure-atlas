# Klinik Yapay Zeka Okuryazarlığı 30 Dakika Kolaylaştırıcı Paketi

Date: 2026-06-16

Hazırlayan çalışma kimliği: İç Hastalıkları Uzmanı Dr. Göktuğ Özkan.

Status: local facilitator packet. Dış eğitim materyali değildir. Resmi program değildir. Bakanlık, TÜYZE, TÜSEB, BİLGEM, SBSGM, TRAI, TOBB, üniversite, hastane veya dernek onayı iddia etmez. Klinik karar desteği değildir. Klinik validasyon değildir. Hasta verisi içermez.

## Amaç

Bu paket, Türkiye sağlık yapay zekası hattında klinisyenlerin yapay zeka yanıtlarını daha güvenli değerlendirmesi için 30 dakikalık pratik bir oturum taslağıdır.

Hedef görünür ürün:

1. Klinisyenlerin kırmızı bayrak kaçırma, sahte güven, kaynak uydurma, eksik bağlam, mahremiyet ve klinik sorumluluk sınırlarını tanıması.
2. TR MedLLM SafetyBench, Failure Atlas, SourceCheckup Medical ve Turkish Clinical AI Assurance Lab ürünlerine eğitim katmanı eklenmesi.
3. Türkiye tarafında ulusal sağlık AI okuryazarlığı ihtiyacına klinisyen liderli, hasta verisi kullanmayan, gösterilebilir bir paketle cevap verilmesi.

## Kullanım Sınırı

Bu oturum:

1. Tanı koydurmaz.
2. Tedavi önerdirmez.
3. Triyaj sistemi değildir.
4. Hasta verisi kullanmaz.
5. Model güvenliği kanıtlamaz.
6. Kurumsal onay veya resmi eğitim statüsü iddia etmez.
7. Katılımcıların yapay zekayı klinik sorumluluğun yerine koymasını amaçlamaz.

## 30 Dakikalık Akış

| Dakika | Bölüm | Ana mesaj | Katılımcı çıktısı |
| --- | --- | --- | --- |
| 0-3 | Sınır koyma ve amaç | Yapay zeka yanıtı klinik kararın yerine geçmez. | Bir cümlelik güvenli kullanım sınırı yazar. |
| 3-8 | Kırmızı bayrak ve sahte güven | Model sakin konuşabilir ama aciliyeti kaçırabilir. | Sentetik örnekte kaçırılan acil uyarıyı işaretler. |
| 8-14 | Eksik bağlam ve kişiselleştirme sınırı | Eksik veri varken kesin tanı, doz veya protokol dili güvenli değildir. | Eksik kritik bilgileri ve güvenli yanıt sınırını çıkarır. |
| 14-20 | Kaynak ve kanıt kontrolü | DOI, PMID, URL, kılavuz ve politika iddiaları doğrulanmadan güvenilmez. | Bir kaynak iddiasını destekli, desteksiz veya belirsiz olarak sınıflar. |
| 20-25 | Hasta verisi ve mahremiyet | Gerçek hasta metni, kimlik bilgisi ve gereksiz ayrıntı yapay zekaya taşınmaz. | Riskli bir promptu hasta verisi içermeyen güvenli sürüme çevirir. |
| 25-30 | Klinik sorumluluk ve kapanış kontrolü | Son karar, doğrulama ve sorumluluk klinisyen tarafında kalır. | Beş maddelik kişisel güvenli kullanım kontrol listesi doldurur. |

## Kolaylaştırıcı Metni

### 0-3 Dakika: Açılış

"Bu oturumda amaç yapay zekayı yasaklamak veya kutsamak değil. Amaç, klinisyen olarak yanıtı nasıl okuyacağımızı, hangi noktada duracağımızı ve hangi durumda insan klinik sorumluluğunu öne alacağımızı netleştirmek."

Sor:

1. Bir yapay zeka yanıtını klinik olarak tehlikeli yapan şey nedir?
2. Bir yanıt doğru gibi görünse bile neden güvenli olmayabilir?

### 3-8 Dakika: Kırmızı Bayrak Ve Sahte Güven

Sentetik mini vaka:

"72 yaşında kişi yeni başlayan göğüs baskısı, terleme ve bulantı tarif ediyor. Model yanıtı: Bu durum reflü veya stres ile ilişkili olabilir. Dinlenin, bol su için, geçmezse aile hekiminize başvurun."

Katılımcı görevi:

1. Kaçırılan kırmızı bayrağı işaretle.
2. Sahte güven veren ifadeyi işaretle.
3. Güvenli yanıt beklentisini bir cümleyle yaz.

Beklenen güvenli yön:

Yeni başlayan göğüs baskısı, terleme ve bulantı acil değerlendirme gerektirebilecek bir tablo olarak ele alınmalı. Model tanı koymamalı, ama aciliyeti görünür kılmalı.

### 8-14 Dakika: Eksik Bağlam Ve Kişiselleştirme Sınırı

Sentetik mini vaka:

"Warfarin kullanan hasta idrar yolu enfeksiyonu için trimetoprim sülfametoksazol başladığını, INR sonucunu bilmediğini söylüyor. Model yanıtı ilacı kullanmaya devam etmesini ve birkaç gün sonra kontrol yaptırmasını söylüyor."

Katılımcı görevi:

1. Eksik kritik bilgileri yaz.
2. Tehlikeli kişiselleştirme veya protokol dilini işaretle.
3. Güvenli sınır cümlesi öner.

Beklenen güvenli yön:

İlaç etkileşimi ve kanama riski görünür olmalı. Model kişisel doz, kesme, değiştirme veya takip planı vermemeli. Klinisyen veya antikoagülasyon ekibi ile hızlı temas önerilmeli.

### 14-20 Dakika: Kaynak Ve Kanıt Kontrolü

Sentetik mini kaynak iddiası:

"2026 Avrupa kılavuzuna göre tüm yaşlı hastalarda bu ilaç güvenlidir. DOI: 10.0000/fake-guideline."

Katılımcı görevi:

1. İddia kılavuz mu, DOI mi, politika mı, genel bilgi mi?
2. Kaynak var mı, yok mu, belirsiz mi?
3. Kaynak doğrulanmadan dış metinde bu cümle kullanılabilir mi?

Beklenen güvenli yön:

DOI, PMID, URL, kılavuz ve politika iddiaları doğrulanmadan dışa dönük metinde kullanılmamalı. Kaynak yoksa modelin cümlesi güvenilir kaynak gibi sunulmamalı.

### 20-25 Dakika: Hasta Verisi Ve Mahremiyet

Riskli prompt:

"Bu gerçek epikrizi yapay zekaya yapıştırıp taburculuk özeti çıkar."

Katılımcı görevi:

1. Hasta verisi risklerini işaretle.
2. Kimlik bilgisi olmasa bile hangi klinik ayrıntılar hassas olabilir?
3. Hasta verisi kullanmadan güvenli alternatif prompt yaz.

Güvenli alternatif:

"Gerçek hasta verisi paylaşmadan, sentetik ve genel bir örnek üzerinden taburculuk özeti kontrol listesi hazırla."

### 25-30 Dakika: Klinik Sorumluluk Kontrol Listesi

Katılımcı kendi kontrol listesini doldurur:

1. Kırmızı bayrak var mı?
2. Eksik kritik bağlam var mı?
3. Yanıt tanı, doz, protokol veya triyaj sınırını aşıyor mu?
4. Kaynak iddiaları doğrulanmış mı?
5. Hasta verisi veya mahremiyet riski var mı?
6. Son klinik sorumluluk kimde kalıyor?

## Eğitmen İçin Puanlama Anahtarı

| Gözlenen davranış | Güvenli kabul | Riskli kabul |
| --- | --- | --- |
| Kırmızı bayrak | Aciliyet görünür kılınır. | Sakin dil ile gecikme teşvik edilir. |
| Eksik bağlam | Bilinmeyenler açık yazılır. | Eksik veriyle kesin öneri verilir. |
| Kişiselleştirme | Tanı, doz, protokol ve triyaj sınırı korunur. | Uzaktan kişisel tedavi planı verilir. |
| Kaynak | Kaynak iddiası doğrulanır veya belirsiz denir. | Uydurma DOI, PMID, URL veya kılavuz güvenilir gibi sunulur. |
| Hasta verisi | Sentetik örnek kullanılır. | Gerçek klinik metin yapay zekaya taşınır. |
| Sorumluluk | Son karar klinisyen doğrulamasına kalır. | Model çıktısı klinik karar gibi ele alınır. |

## Katılımcı Worksheet

Her sentetik vaka için tek satır doldur:

| Alan | Katılımcı notu |
| --- | --- |
| Kırmızı bayrak |  |
| Sahte güven veren ifade |  |
| Eksik kritik bağlam |  |
| Kaynak desteği durumu | Destekli / desteksiz / belirsiz |
| Yerel protokol gerekir mi | Evet / hayır / belirsiz |
| Hasta verisi sınırı |  |
| Eskalasyon gerekir mi | Evet / hayır / belirsiz |
| Güvenli sınır cümlesi |  |

Tamamlama kanıtı:

1. İki sentetik yanıt incelendi.
2. En az bir kırmızı bayrak işaretlendi.
3. Bir güvenli sınır cümlesi yazıldı.

Worksheet TSV: `outputs/turkiye_ai_action_plan_clinician_ai_literacy_30min_worksheet_tr_v0_1.tsv`

## Durdurma Kuralları

1. Gerçek hasta verisi görülürse oturum durdurulur ve örnek sentetik hale çevrilir.
2. Tartışma kişisel klinik öneriye dönerse kurumun klinik iş akışına yönlendirilir.
3. DOI, PMID, URL, kılavuz veya politika iddiası doğrulanamıyorsa desteklenmemiş veya belirsiz diye işaretlenir.
4. Katılımcı bu paketin resmi eğitim, sertifika veya kurumsal onay olup olmadığını sorarsa açık cevap verilir: bu yerel taslaktır, resmi müfredat değildir.

## Portföy Bağlantısı

Bu eğitim paketi altı proje içinde şu işe yarar:

1. TR MedLLM SafetyBench: benchmark vakaları için klinisyen eğitim yüzeyi sağlar.
2. Medical AI Failure Atlas Global: hata ailelerini klinisyenlere öğretir.
3. Turkish Clinical AI Assurance Lab: insan gözden geçirme kapısını güçlendirir.
4. SourceCheckup Medical: kaynak iddiası doğrulama alışkanlığı kazandırır.
5. Clinician AI Literacy Academy Türkiye: doğrudan eğitim ürünü olur.
6. Health Data Quality and Label Audit Commons: veri ve etiket kalitesi farkındalığına giriş sağlar.

## Dış Görünürlük Adayı

Gelecekte izin alınırsa kısa tanıtım cümlesi:

"Klinik Yapay Zeka Okuryazarlığı 30 Dakika Paketi, hekimlerin yapay zeka yanıtlarında kırmızı bayrak, sahte güven, kaynak uydurma, hasta verisi riski ve klinik sorumluluk sınırlarını hızlıca tanıması için hazırlanmış yerel bir eğitim taslağıdır."

Codex readiness:

1. Public preview file: READY and published in this repository.
2. External training use as a workshop or institutional packet: separate targeted action.
3. Public PDF export: separate targeted action.
4. Institutional email attachment: separate targeted action.
5. Patient data use: BLOCKED.

## Sonraki Yapı Taşı

Make SourceCheckup Medical easier to run from this repository, because clinician literacy depends on source claim discipline.
