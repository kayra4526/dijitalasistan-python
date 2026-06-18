# 🚀 Kişisel Dijital Asistan (Personal Digital Assistant)

*Bu proje; günlük yaşamı organize etmek, harcamaları milimetrik takip etmek, görevleri planlamak ve alışkanlıkları yönetmek için sıfırdan geliştirilmiş **Python tabanlı, modern arayüzlü bir masaüstü asistan uygulamasıdır.*** Modern ve şık bir UI/UX deneyimi sunmak için **`customtkinter`** kütüphanesi kullanılarak özel olarak tasarlanmıştır.

---

## 🌟 Temel Modüller ve Özellikler

Uygulama, tüm verileri yerel `.json` dosyalarında *güvenli ve hafif* bir şekilde saklayan, birbiriyle senkronize çalışan gelişmiş modüllerden oluşur:

* **🏠 Ana Ekran (Dashboard) & Asenkron Pomodoro:** Bütçe, Ajanda ve F1 sekmelerindeki veriler JSON altyapısından anlık olarak çekilip 4'lü matris formatında özetlenir (Data Aggregation). Ayrıca GUI'yi kitlemeden arka planda çalışan (`app.after` metoduyla) 25 dakikalık Pomodoro sayacı entegre edilmiştir.
* **📅 Akıllı Ajanda (Daily Planner):** Günlük (Journal), İleri Tarihli Notlar (Notes) ve Görevler (Tasks) tek bir arayüzde, ancak birbirinden tamamen izole edilmiş veri yapılarıyla (Separation of Concerns) birleştirilmiştir. İndeksleme algoritması ile spesifik notların silinmesi ve görevlerin tamamlandı (✅) olarak işaretlenmesi sağlanır.
* **💰 Dinamik Bütçe (Budget Tracker):** Gelir-gider takibi yapmanızı sağlar. Girilen harcamalar arka planda bir sözlük (Dictionary) mimarisiyle anlık olarak gruplandırılır ve kategori bazlı toplam harcamalar detaylı bir analitik döküm olarak listelenir.
* **🫧 Otomatik Cilt Bakım Çizelgesi (Skincare Tracker):** Zaman bazlı otomasyonla (Python `isocalendar`) çalışan haftalık rutin modülüdür. Her Pazartesi günü (yeni haftaya girildiğinde) bir önceki haftanın onay kutuları (checkbox states) otomatik olarak sıfırlanarak temiz bir çizelge sunulur.
* **🏎️ F1 Yarış Merkezi (Time-sensitive UI):** Gömülü yarış takvimi ile hafta sonu seans saatlerini listeler. Sistem güncel tarihi okuyarak; geçmiş yarışları arayüzde otomatik olarak soluk/gri tona çevirir ve yaklaşan yarışları önceliklendirir.
* **📅 Takvim (Visual Calendar):** Seçtiğiniz aydaki günleri *profesyonel bir Excel ızgarası nizamında* gösteren dinamik takvim. Ajandaya eklediğiniz görevler, takvim üzerinde ilgili günün kutucuğunda otomatik olarak belirir.
* **🎯 Habit Tracker (Aylık Matris):** Aylık alışkanlıklarınızı dikey bir matris üzerinde takip edebileceğiniz sistem. Günler yukarıdan aşağıya sıralanır ve tek tıkla alışkanlık tamamlanabilir. *Ekranı taşırmayan, modern kaydırma (scroll) desteğine sahiptir.*
* **🎬 Medya (Media Tracker):** *İzlenecek, izleniyor* ve *bitti* durumlarındaki dizileri/filmleri pratik bir şekilde takip etmenizi sağlayan liste yöneticisi.

---

## 🛠️ Kullanılan Teknolojiler

* **Dil:** `Python 3.x`
* **Arayüz (GUI):** `CustomTkinter` *(Karanlık tema ve modern UI desteği)*
* **Veritabanı:** Yerel JSON Dosyaları (`json` modülü)
* **Zaman Yönetimi:** `datetime`, `calendar`

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları sırasıyla terminalinize uygulayın:

1. Gerekli kütüphaneyi yükleyin (Eğer yüklü değilse):
`pip install customtkinter`

2. Uygulamayı başlatın:
`python kisisel_asistan.py`

---

## 📂 Veri Yapısı (JSON Dosyaları)
Uygulama, çalıştığı dizinde verileri kaybetmemek için kendi otonom veritabanlarını oluşturur. Verilerinizi yedeklemek isterseniz sadece bu dosyaları kopyalamanız yeterlidir:
* `butce.json`
* `Yillik_Ajanda.json`
* `Medya_Listesi.json`
* `aliskanlik.json`
* `cilt_bakimi.json`
* `f1_takvim.json`

Geliştirmeye ve yeni modüller eklemeye açıktır. 🚀

**Gökçen Kayra Ünver**
