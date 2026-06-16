# 🚀 Kişisel Dijital Asistan (Personal Digital Assistant)

*Bu proje; günlük yaşamı organize etmek, harcamaları milimetrik takip etmek, görevleri planlamak ve alışkanlıkları yönetmek için sıfırdan geliştirilmiş **Python tabanlı, modern arayüzlü bir masaüstü asistan uygulamasıdır.*** Modern ve şık bir UI/UX deneyimi sunmak için **`customtkinter`** kütüphanesi kullanılarak özel olarak tasarlanmıştır.

---

## 🌟 Temel Modüller ve Özellikler

Uygulama, **5 temel sekmeden** oluşur ve tüm veriler yerel `.json` dosyalarında *güvenli ve hafif* bir şekilde saklanır.

* **💰 Bütçe (Budget Tracker):** Gelir-gider takibi yapmanızı sağlar. Harcamalarınızı kategorize edebilir ve güncel bakiye özetinizi *anlık* olarak görebilirsiniz.
* **📓 Ajanda (Daily Planner):** Günlük notlar alabileceğiniz ve yapılacaklar listesi (To-Do) oluşturabileceğiniz modüldür. Görevleri tamamlandı olarak (✅) işaretleyebilir veya listeden silebilirsiniz (🗑️).
* **📅 Takvim (Visual Calendar):** Seçtiğiniz aydaki günleri *profesyonel bir Excel ızgarası nizamında* gösteren dinamik takvim. Ajandaya eklediğiniz görevler, takvim üzerinde ilgili günün kutucuğunda otomatik olarak belirir.
* **🎬 Medya (Media Tracker):** *İzlenecek, izleniyor* ve *bitti* durumlarındaki dizileri/filmleri pratik bir şekilde takip etmenizi sağlayan liste yöneticisi.
* **🎯 Habit Tracker (Aylık Matris):** Aylık alışkanlıklarınızı (spor, su içme, kodlama vb.) dikey bir matris üzerinde takip edebileceğiniz sistem. Günler yukarıdan aşağıya sıralanır ve tek tıkla o günkü alışkanlığınızı tamamlayabilirsiniz. *Ekranı taşırmayan, modern kaydırma (scroll) desteğine sahiptir.*

---

## 🛠️ Kullanılan Teknolojiler

* **Dil:** `Python 3.x`
* **Arayüz (GUI):** `CustomTkinter` *(Karanlık tema ve modern UI desteği)*
* **Veritabanı:** Yerel JSON Dosyaları (`json` modülü)
* **Zaman Yönetimi:** `datetime`, `calendar`

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla terminalinize yapıştırın:

Gerekli kütüphaneyi yükleyin (Eğer yüklü değilse):
pip install customtkinter

python kisisel_asistan.py




📂 Veri Yapısı (JSON Dosyaları)
Uygulama çalıştığı dizinde verileri kaybetmemek için 4 adet JSON dosyası oluşturur. Verilerinizi yedeklemek isterseniz sadece bu dosyaları kopyalamanız yeterlidir:

butce.json

Yillik_Ajanda.json

Medya_Listesi.json

aliskanlik.json


Geliştirmeye ve yeni modüller eklemeye açıktır. 🚀




Gökçen Kayra Ünver
