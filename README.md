🚀 Kişisel Dijital Asistan (Personal Digital Assistant)
Bu proje, günlük yaşamın karmaşasını yönetmek, bütçe takibi yapmak, görevleri organize etmek ve medya tüketimini kayıt altına almak için geliştirilmiş, Python ve CustomTkinter tabanlı, hepsi bir arada bir masaüstü uygulamasıdır.

🌟 Temel Özellikler
Uygulamanız, dört ana modülden oluşan dinamik ve verimli bir arayüze sahiptir:

💰 Bütçe Yönetimi
Gelir/Gider Takibi: Günlük harcamalarınızı kategorize ederek takip edin.

Dinamik Kategori: Uygulama içerisinden anlık olarak yeni bütçe kategorileri (örn: Ulaşım, Okul, Staj) ekleyin.

Özet Görünüm: Gelir, Gider ve Kalan bütçenizi tek bir ekranda yan yana analiz edin.

📓 Ajanda ve Görev Yönetimi
Günlük Notlar: Günlük tutma özelliği ile o günün notlarını kaydedin.

Görev Takibi: Görevlerinizi ekleyin, "Tamamla" butonuyla işaretleyin veya "Sil" butonuyla listenizden kaldırın.

Tarih Bazlı Kayıt: Takvim ile senkronize çalışan, seçtiğiniz tarihe göre veri getiren sistem.

📅 Akıllı Takvim
Görsel Planlayıcı: calendar kütüphanesi ile aylık bazda günleri kare kutucuklar halinde görüntüleyin.

Navigasyon: Aylar arası geçiş yapın.

Etkinlik Entegrasyonu: Ajanda'ya eklediğiniz görevler, takvim kutucuklarında otomatik olarak belirir.

Dinamik Ekleme: Takvim üzerinden belirli bir güne etkinlik adı girerek hızlıca kayıt oluşturun.

🎬 Medya Takibi
İzleme Listeleri: Dizi ve filmlerinizi "İzlenecekler", "İzleniyor" ve "Bitti" kategorilerine ayırın.

Durum Yönetimi: İzlemeye başladığınız veya bitirdiğiniz yapımları butonlarla listeler arası taşıyın.

🛠 Kullanılan Teknolojiler
Dil: Python

Arayüz: CustomTkinter (Modern, karanlık tema desteği)

Veri Depolama: JSON (Yerel dosya tabanlı veritabanı)

Kütüphaneler: datetime, calendar, os, json

⚙️ Kurulum ve Çalıştırma
Projeyi yerel bilgisayarınızda çalıştırmak için şu adımları izleyin:

Python'ın yüklü olduğundan emin olun.

Gerekli kütüphaneyi yükleyin:

Bash
pip install customtkinter
Depoyu klonlayın veya dosyaları indirin:

Bash
git clone [repo-adresin]
Uygulamayı çalıştırın:

Bash
python main.py
📂 Veri Saklama
Uygulama, verilerinizi otomatik olarak proje klasöründe şu isimlerdeki JSON dosyalarında saklar:

butce.json: Finansal verileriniz.

Yillik_Ajanda.json: Günlük notlar ve görevler.

Medya_Listesi.json: Medya takip listeleriniz.

Geliştirici: Gökçen Kayra Ünver
