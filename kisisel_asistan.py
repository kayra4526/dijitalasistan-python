import customtkinter as ctk
import json
import os
import datetime
import calendar
import urllib.request
import threading

# --- 1. DOSYA AYARLARI ---
BUTCE_DOSYASI = "butce.json"
AJANDA_DOSYASI = "Yillik_Ajanda.json"
MEDYA_DOSYASI = "Medya_Listesi.json"
ALISKANLIK_DOSYASI = "aliskanlik.json" 
CILT_DOSYASI = "cilt_bakimi.json"
F1_DOSYASI = "f1_takvim.json"



def veri_yukle(dosya_adi, varsayilan):
    if os.path.exists(dosya_adi):
        try:
            with open(dosya_adi, "r", encoding="utf-8") as dosya: return json.load(dosya)
        except: return varsayilan
    return varsayilan

def veri_kaydet(dosya_adi, veri):
    with open(dosya_adi, "w", encoding="utf-8") as dosya:
        json.dump(veri, dosya, indent=4, ensure_ascii=False)

# Verileri yükle
butce_verisi = veri_yukle(BUTCE_DOSYASI, {"gelir": 0.0, "kategoriler": ["Genel", "Market", "Fatura", "Eğlence"], "harcamalar": []})
ajanda_verisi = veri_yukle(AJANDA_DOSYASI, {})
medya_verisi = veri_yukle(MEDYA_DOSYASI, {"izlenecekler": [], "izleniyor": [], "bitti": []})
aliskanlik_verisi = veri_yukle(ALISKANLIK_DOSYASI, {"aliskanliklar": [], "tarihler": {}}) 
varsayilan_cilt = {
    "son_hafta": datetime.date.today().isocalendar()[1], # Yılın kaçıncı haftası
    "rutin": {
        "Pazartesi": ["☀️ Sabah: Jumiso HA Toner, CreamCo, Güneş Kremi", "🌙 Akşam: Fiddy Metodu (Salisilik + Kil + Yağ Bazlı Temizleyici)"],
        "Salı": ["☀️ Sabah: Jumiso HA Toner, CreamCo, Güneş Kremi", "🌙 Akşam: Çift Aşama Temizlik + C Vitamini / Glikolik Asit"],
        "Çarşamba": ["☀️ Sabah: Jumiso HA Toner, CreamCo, Güneş Kremi", "🌙 Akşam: Çift Aşama Temizlik + Bariyer Onarım / Leke Aydınlatma"],
        "Perşembe": ["☀️ Sabah: Jumiso HA Toner, CreamCo, Güneş Kremi", "🌙 Akşam: Çift Aşama Temizlik + C Vitamini / Glikolik Asit"],
        "Cuma": ["☀️ Sabah: Jumiso HA Toner, CreamCo, Güneş Kremi", "🌙 Akşam: Çift Aşama Temizlik + Bariyer Onarım"],
        "Cumartesi": ["☀️ Sabah: Jumiso HA Toner, CreamCo, Güneş Kremi", "🌙 Akşam: Fiddy Metodu (Derin Gözenek Temizliği)"],
        "Pazar": ["☀️ Sabah: Sadece Su, CreamCo, Güneş Kremi", "🌙 Akşam: Çift Aşama Temizlik + Sadece Nemlendirici (Cildi Dinlendirme)"]
    },
    "durum": {} # Atılan tikler burada tutulacak
}
cilt_verisi = veri_yukle(CILT_DOSYASI, varsayilan_cilt)


varsayilan_f1 = [
    {"isim": "🇪🇸 İspanya Grand Prix", "tarih": "2026-06-14", "cuma": "14:30 Antrenman 1\n18:00 Antrenman 2", "cumartesi": "13:30 Antrenman 3\n17:00 Sıralama", "pazar": "16:00 Büyük Yarış"},
    {"isim": "🇦🇹 Avusturya Grand Prix", "tarih": "2026-06-28", "cuma": "13:30 Antrenman 1\n17:00 Sprint Sıralama", "cumartesi": "13:00 Sprint Yarışı\n17:00 Sıralama", "pazar": "16:00 Büyük Yarış"},
    {"isim": "🇬🇧 Britanya Grand Prix", "tarih": "2026-07-05", "cuma": "14:30 Antrenman 1\n18:00 Antrenman 2", "cumartesi": "13:30 Antrenman 3\n17:00 Sıralama", "pazar": "17:00 Büyük Yarış"},
    {"isim": "🇧🇪 Belçika Grand Prix", "tarih": "2026-07-19", "cuma": "14:30 Antrenman 1\n18:00 Antrenman 2", "cumartesi": "13:30 Antrenman 3\n17:00 Sıralama", "pazar": "16:00 Büyük Yarış"},
    {"isim": "🇭🇺 Macaristan Grand Prix", "tarih": "2026-07-26", "cuma": "14:30 Antrenman 1\n18:00 Antrenman 2", "cumartesi": "13:30 Antrenman 3\n17:00 Sıralama", "pazar": "16:00 Büyük Yarış"},
    {"isim": "🇳🇱 Hollanda Grand Prix", "tarih": "2026-08-23", "cuma": "13:30 Antrenman 1\n17:00 Sprint Sıralama", "cumartesi": "13:00 Sprint Yarışı\n16:00 Sıralama", "pazar": "16:00 Büyük Yarış"},
    {"isim": "🇮🇹 İtalya Grand Prix", "tarih": "2026-09-06", "cuma": "14:30 Antrenman 1\n18:00 Antrenman 2", "cumartesi": "13:30 Antrenman 3\n17:00 Sıralama", "pazar": "16:00 Büyük Yarış"},
    {"isim": "🇦🇿 Azerbaycan Grand Prix", "tarih": "2026-09-27", "cuma": "10:30 Antrenman 1\n14:00 Antrenman 2", "cumartesi": "10:30 Antrenman 3\n14:00 Sıralama", "pazar": "14:00 Büyük Yarış"}
]
f1_verisi = veri_yukle(F1_DOSYASI, varsayilan_f1)



# --- 2. ARAYÜZ KURULUMU ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x800") 
app.title("🚀 Kişisel Dijital Asistan v8.0 - Tam Çalışan Sürüm")

sekmeler = ctk.CTkTabview(app)
sekmeler.pack(padx=20, pady=20, fill="both", expand=True)

sekme_ana = sekmeler.add("🏠 Ana Ekran")
sekme_butce = sekmeler.add("💰 Bütçe")
sekme_ajanda = sekmeler.add("📓 Ajanda")
sekme_takvim = sekmeler.add("📅 Takvim")
sekme_medya = sekmeler.add("🎬 Medya")
sekme_aliskanlik = sekmeler.add("🎯 Habit Tracker")
sekme_cilt = sekmeler.add("🫧 Skincare")
sekme_f1 = sekmeler.add("🏎️ F1 Hub")


# ==========================================
# --- 🏠 ANA EKRAN (DASHBOARD) ---
# ==========================================
def dashboard_guncelle():
    # 1. Bütçe Durumu
    toplam_harcama = sum(h["tutar"] for h in butce_verisi.get("harcamalar", []))
    kalan = butce_verisi.get("gelir", 0) - toplam_harcama
    dash_butce_lbl.configure(text=f"Kalan Bakiye:\n{kalan:.2f} TL", text_color="lightgreen" if kalan >= 0 else "red")

    # 2. Ajanda Durumu (Bugün)
    bugun = datetime.date.today().strftime("%d-%m-%Y")
    bekleyen_gorev = 0
    if bugun in ajanda_verisi:
        bekleyen_gorev = len([g for g in ajanda_verisi[bugun].get("gorevler", []) if not g["tamamlandi"]])
    dash_ajanda_lbl.configure(text=f"Bugünün Ajandası:\n{bekleyen_gorev} Bekleyen Görev")

    # 3. F1 Durumu (Sıradaki Yarış)
    bugun_tarih = datetime.date.today().strftime("%Y-%m-%d")
    siradaki_yaris = "Veri Yok"
    for yaris in f1_verisi:
        if yaris["tarih"] >= bugun_tarih:
            siradaki_yaris = f"{yaris['isim']}\n{yaris['tarih']}"
            break
    dash_f1_lbl.configure(text=f"Sıradaki F1 Yarışı:\n{siradaki_yaris}")

# Dashboard Arayüz Tasarımı (4'lü Kutu Matrisi)
ctk.CTkLabel(sekme_ana, text="👋 Hoş Geldin! İşte Bugünün Özeti", font=("Arial", 20, "bold")).pack(pady=20)

kutu_frame = ctk.CTkFrame(sekme_ana, fg_color="transparent")
kutu_frame.pack(pady=10)

# Kutu 1: Bütçe
kutu_butce = ctk.CTkFrame(kutu_frame, width=200, height=120, fg_color="#222")
kutu_butce.pack_propagate(False); kutu_butce.grid(row=0, column=0, padx=10, pady=10)
ctk.CTkLabel(kutu_butce, text="💵 BÜTÇE", font=("Arial", 14, "bold"), text_color="gold").pack(pady=10)
dash_butce_lbl = ctk.CTkLabel(kutu_butce, text="-", font=("Arial", 16, "bold"))
dash_butce_lbl.pack(pady=5)

# Kutu 2: Ajanda
kutu_ajanda = ctk.CTkFrame(kutu_frame, width=200, height=120, fg_color="#222")
kutu_ajanda.pack_propagate(False); kutu_ajanda.grid(row=0, column=1, padx=10, pady=10)
ctk.CTkLabel(kutu_ajanda, text="📅 AJANDA", font=("Arial", 14, "bold"), text_color="cyan").pack(pady=10)
dash_ajanda_lbl = ctk.CTkLabel(kutu_ajanda, text="-", font=("Arial", 14))
dash_ajanda_lbl.pack(pady=5)

# Kutu 3: F1
kutu_f1 = ctk.CTkFrame(kutu_frame, width=420, height=150, fg_color="#222")
kutu_f1.pack_propagate(False); kutu_f1.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
ctk.CTkLabel(kutu_f1, text="🏎️ FORMULA 1", font=("Arial", 14, "bold"), text_color="red").pack(pady=10)
dash_f1_lbl = ctk.CTkLabel(kutu_f1, text="-", font=("Arial", 14))
dash_f1_lbl.pack(pady=5)

ctk.CTkButton(sekme_ana, text="🔄 Ekranı Yenile", command=dashboard_guncelle, width=150).pack(pady=20)

# Uygulama açıldığında ilk verileri çekmesi için
app.after(100, dashboard_guncelle)



# --- 🍅 POMODORO SAYACI (AJANDA İÇİ) ---
pomodoro_saniye = 25 * 60
pomodoro_calisiyor = False

def pomodoro_guncelle():
    global pomodoro_saniye, pomodoro_calisiyor
    if pomodoro_calisiyor and pomodoro_saniye > 0:
        pomodoro_saniye -= 1
        dak = pomodoro_saniye // 60
        san = pomodoro_saniye % 60
        pomodoro_lbl.configure(text=f"{dak:02d}:{san:02d}")
        app.after(1000, pomodoro_guncelle)
    elif pomodoro_saniye == 0:
        pomodoro_calisiyor = False
        pomodoro_lbl.configure(text="00:00", text_color="red")
        pomodoro_btn.configure(text="▶️ Başla")

def pomodoro_basla_dur():
    global pomodoro_calisiyor
    if pomodoro_calisiyor:
        pomodoro_calisiyor = False
        pomodoro_btn.configure(text="▶️ Başla", fg_color="#1f538d")
    else:
        if pomodoro_saniye == 0: return # Süre bittiyse başlamasın
        pomodoro_calisiyor = True
        pomodoro_btn.configure(text="⏸️ Duraklat", fg_color="orange")
        pomodoro_guncelle()

def pomodoro_sifirla():
    global pomodoro_saniye, pomodoro_calisiyor
    pomodoro_calisiyor = False
    pomodoro_saniye = 25 * 60
    pomodoro_lbl.configure(text="25:00", text_color="cyan")
    pomodoro_btn.configure(text="▶️ Başla", fg_color="#1f538d")

# Pomodoro Arayüzü (Ajanda sekmesinin en üstünde dursun)
pomo_frame = ctk.CTkFrame(sekme_ana, fg_color="#2b2b2b", corner_radius=10)
pomo_frame.pack(pady=(5, 10), padx=20, fill="x")

ctk.CTkLabel(pomo_frame, text="🍅 Odaklanma Modu:", font=("Arial", 14, "bold")).pack(side="left", padx=15)
pomodoro_lbl = ctk.CTkLabel(pomo_frame, text="25:00", font=("Courier", 24, "bold"), text_color="cyan")
pomodoro_lbl.pack(side="left", padx=20)

pomodoro_btn = ctk.CTkButton(pomo_frame, text="▶️ Başla", command=pomodoro_basla_dur, width=80)
pomodoro_btn.pack(side="left", padx=5)
ctk.CTkButton(pomo_frame, text="🔄 Sıfırla", command=pomodoro_sifirla, width=80, fg_color="#555").pack(side="left", padx=5)


# ==========================================
# --- BÜTÇE (GRUPLANDIRILMIŞ DETAYLI LİSTE) ---
# ==========================================
def butce_ekrani_guncelle():
    # 1. Özet Kısmını Hesapla
    toplam_harcama = sum(h["tutar"] for h in butce_verisi["harcamalar"])
    kalan = butce_verisi["gelir"] - toplam_harcama
    ozet_metni = f"💵 Gelir: {butce_verisi['gelir']:.2f} TL\n💸 Gider: {toplam_harcama:.2f} TL\n------------------------\n📈 Kalan: {kalan:.2f} TL"
    butce_ozet_label.configure(text=ozet_metni, text_color="red" if kalan < 0 else "white")

    # 2. Detaylı Harcama Listesini Güncelle
    butce_detay_textbox.configure(state="normal")
    butce_detay_textbox.delete("1.0", "end")
    
    if not butce_verisi["harcamalar"]:
        butce_detay_textbox.insert("end", "ℹ️ Henüz harcama eklenmedi. Cüzdan güvende!")
    else:
        # Harcamaları kategorilerine göre sözlük (dictionary) içinde grupluyoruz
        gruplar = {}
        for h in butce_verisi["harcamalar"]:
            kat = h["kategori"]
            if kat not in gruplar:
                gruplar[kat] = []
            gruplar[kat].append(h)
            
        # Gruplanmış verileri ekrana şık bir şekilde yazdırıyoruz
        detay_metni = ""
        for kat, harcamalar in gruplar.items():
            kategori_toplam = sum(h["tutar"] for h in harcamalar)
            detay_metni += f"📂 {kat.upper()} (Kategori Toplamı: {kategori_toplam:.2f} TL)\n"
            
            for h in harcamalar:
                detay_metni += f"   - {h['aciklama']}: {h['tutar']:.2f} TL\n"
            detay_metni += "\n" # Kategoriler arası boşluk
            
        butce_detay_textbox.insert("end", detay_metni)
        
    butce_detay_textbox.configure(state="disabled")

def yeni_kategori_ekle():
    yeni = kat_entry.get()
    if yeni and yeni not in butce_verisi["kategoriler"]:
        butce_verisi["kategoriler"].append(yeni)
        veri_kaydet(BUTCE_DOSYASI, butce_verisi)
        kategori_secim.configure(values=butce_verisi["kategoriler"])
        kat_entry.delete(0, 'end')

def gelir_ekle():
    try:
        butce_verisi["gelir"] = float(gelir_entry.get())
        veri_kaydet(BUTCE_DOSYASI, butce_verisi)
        butce_ekrani_guncelle()
    except: pass

def harcama_ekle():
    try:
        tutar = float(tutar_entry.get())
        aciklama = aciklama_entry.get()
        if not aciklama: return
        butce_verisi["harcamalar"].append({"kategori": kategori_secim.get(), "aciklama": aciklama, "tutar": tutar})
        veri_kaydet(BUTCE_DOSYASI, butce_verisi)
        butce_ekrani_guncelle()
        
        # Ekledikten sonra kutuları temizle ki arka arkaya hızlıca eklenebilsin
        tutar_entry.delete(0, 'end')
        aciklama_entry.delete(0, 'end')
    except: pass

# --- ARAYÜZ (UI) ELEMANLARI ---
butce_ozet_label = ctk.CTkLabel(sekme_butce, text="", font=("Courier", 16, "bold"), justify="left")
butce_ozet_label.pack(pady=10)

kat_frame = ctk.CTkFrame(sekme_butce)
kat_frame.pack(pady=5)
kat_entry = ctk.CTkEntry(kat_frame, placeholder_text="Yeni Kategori Adı")
kat_entry.pack(side="left", padx=5)
ctk.CTkButton(kat_frame, text="+", command=yeni_kategori_ekle, width=30).pack(side="left", padx=5)

gelir_entry = ctk.CTkEntry(sekme_butce, placeholder_text="Yeni Gelir Miktarı")
gelir_entry.pack(pady=5)
ctk.CTkButton(sekme_butce, text="Gelir Güncelle", command=gelir_ekle, fg_color="green", hover_color="darkgreen").pack(pady=5)

kategori_secim = ctk.CTkOptionMenu(sekme_butce, values=butce_verisi["kategoriler"])
kategori_secim.pack(pady=10)

aciklama_entry = ctk.CTkEntry(sekme_butce, placeholder_text="Açıklama (Örn: Kahve, Market)")
aciklama_entry.pack(pady=5)
tutar_entry = ctk.CTkEntry(sekme_butce, placeholder_text="Tutar (TL)")
tutar_entry.pack(pady=5)

ctk.CTkButton(sekme_butce, text="Harcama Ekle", command=harcama_ekle, fg_color="red", hover_color="darkred").pack(pady=10)

# Yeni Eklenen: Harcama Detay Kutusu
butce_detay_textbox = ctk.CTkTextbox(sekme_butce, height=200, width=500, font=("Arial", 13))
butce_detay_textbox.pack(pady=10)

# İlk açılışta verileri ekrana bas
butce_ekrani_guncelle()

# ==========================================
# --- AJANDA (GÖREV+NOT+GÜNLÜK TAM KONTROL) ---
# ==========================================
def ajanda_ekrani_guncelle():
    tarih = tarih_entry.get()
    ajanda_textbox.configure(state="normal")
    ajanda_textbox.delete("1.0", "end")
    
    if tarih in ajanda_verisi:
        veri = ajanda_verisi[tarih]
        icerik = f"📅 {tarih}\n" + "="*35 + "\n\n"
        
        # 1. GÜNLÜK
        icerik += "✍️ GÜNLÜK:\n" + veri.get("gunluk", "Henüz günlük girişi yok.") + "\n\n"
        
        # 2. NOTLAR (Artık Numaralı!)
        icerik += "📌 NOTLAR:\n"
        if veri.get("notlar"):
            for i, not_metni in enumerate(veri["notlar"], 1):
                icerik += f"  {i}. {not_metni}\n"
        else:
            icerik += "  Kayıt yok.\n"
        icerik += "\n"
        
        # 3. GÖREVLER
        icerik += "📝 GÖREVLER:\n"
        if veri.get("gorevler"):
            for i, gorev in enumerate(veri["gorevler"], 1):
                durum = "✅" if gorev["tamamlandi"] else "⬜"
                icerik += f"  {i}. {durum} {gorev['tanim']}\n"
        else:
            icerik += "  Kayıt yok.\n"
            
        ajanda_textbox.insert("end", icerik)
    else:
        ajanda_textbox.insert("end", f"ℹ️ {tarih} için henüz kayıt yok.")
        
    ajanda_textbox.configure(state="disabled")

def veri_ekle():
    tarih = tarih_entry.get()
    metin = girdi_entry.get()
    tur = tur_secim.get()
    if not metin: return
    
    if tarih not in ajanda_verisi: 
        ajanda_verisi[tarih] = {"gunluk": "", "notlar": [], "gorevler": []}
        
    if "notlar" not in ajanda_verisi[tarih]: ajanda_verisi[tarih]["notlar"] = []
    if "gorevler" not in ajanda_verisi[tarih]: ajanda_verisi[tarih]["gorevler"] = []
    if "gunluk" not in ajanda_verisi[tarih]: ajanda_verisi[tarih]["gunluk"] = ""
    
    if tur == "Not":
        ajanda_verisi[tarih]["notlar"].append(metin)
    elif tur == "Günlük":
        ajanda_verisi[tarih]["gunluk"] = metin
    elif tur == "Görev":
        ajanda_verisi[tarih]["gorevler"].append({"tanim": metin, "tamamlandi": False})
        
    veri_kaydet(AJANDA_DOSYASI, ajanda_verisi)
    ajanda_ekrani_guncelle()
    girdi_entry.delete(0, 'end')

def gorev_tamamla():
    # Tamamlama işlemi sadece Görevler için geçerlidir
    tarih = tarih_entry.get()
    try:
        no = int(islem_entry.get()) - 1
        if tarih in ajanda_verisi and 0 <= no < len(ajanda_verisi[tarih].get("gorevler", [])):
            ajanda_verisi[tarih]["gorevler"][no]["tamamlandi"] = True
            veri_kaydet(AJANDA_DOSYASI, ajanda_verisi)
            ajanda_ekrani_guncelle()
            islem_entry.delete(0, 'end')
    except ValueError:
        pass

def veri_sil():
    tarih = tarih_entry.get()
    hedef_tur = islem_secim.get() # Neyi sileceğiz? (Görev, Not, Günlük)
    
    if tarih not in ajanda_verisi: return

    # Günlük silinecekse numaraya gerek yok, direkt temizle
    if hedef_tur == "Günlük":
        ajanda_verisi[tarih]["gunluk"] = ""
    else:
        # Not veya Görev silinecekse numaraya bak
        try:
            no = int(islem_entry.get()) - 1
            if hedef_tur == "Görev" and 0 <= no < len(ajanda_verisi[tarih].get("gorevler", [])):
                ajanda_verisi[tarih]["gorevler"].pop(no)
            elif hedef_tur == "Not" and 0 <= no < len(ajanda_verisi[tarih].get("notlar", [])):
                ajanda_verisi[tarih]["notlar"].pop(no)
        except ValueError:
            pass # Numara girilmediyse hata verme
            
    veri_kaydet(AJANDA_DOSYASI, ajanda_verisi)
    ajanda_ekrani_guncelle()
    islem_entry.delete(0, 'end')

# --- ARAYÜZ ---
ctk.CTkLabel(sekme_ajanda, text="Tarih (GG-AA-YYYY):").pack(pady=(10, 0))
tarih_entry = ctk.CTkEntry(sekme_ajanda); tarih_entry.insert(0, datetime.date.today().strftime("%d-%m-%Y")); tarih_entry.pack()
ctk.CTkButton(sekme_ajanda, text="Tarihi Getir", command=ajanda_ekrani_guncelle).pack(pady=5)

ajanda_textbox = ctk.CTkTextbox(sekme_ajanda, height=300, width=500)
ajanda_textbox.pack(pady=10)

# 1. Ortak Giriş Alanı (Ekleme)
girdi_frame = ctk.CTkFrame(sekme_ajanda); girdi_frame.pack(pady=5)
girdi_entry = ctk.CTkEntry(girdi_frame, width=220, placeholder_text="Metni buraya yaz...")
girdi_entry.pack(side="left", padx=5)

tur_secim = ctk.CTkOptionMenu(girdi_frame, values=["Görev", "Not", "Günlük"], width=90)
tur_secim.pack(side="left", padx=5)

ctk.CTkButton(girdi_frame, text="Ekle/Kaydet", command=veri_ekle, width=70).pack(side="left", padx=5)

# 2. Akıllı İşlem Alanı (Silme ve Tamamlama)
islem_frame = ctk.CTkFrame(sekme_ajanda); islem_frame.pack(pady=10)

ctk.CTkLabel(islem_frame, text="Hedef:").pack(side="left", padx=(5, 2))
islem_secim = ctk.CTkOptionMenu(islem_frame, values=["Görev", "Not", "Günlük"], width=80)
islem_secim.pack(side="left", padx=2)

ctk.CTkLabel(islem_frame, text="No:").pack(side="left", padx=(10, 2))
islem_entry = ctk.CTkEntry(islem_frame, width=40, placeholder_text="No")
islem_entry.pack(side="left", padx=2)

ctk.CTkButton(islem_frame, text="✅ Görevi Tamamla", command=gorev_tamamla, width=120, fg_color="green", hover_color="darkgreen").pack(side="left", padx=10)
ctk.CTkButton(islem_frame, text="🗑️ Sil", command=veri_sil, width=60, fg_color="red", hover_color="darkred").pack(side="left", padx=5)

ajanda_ekrani_guncelle()
# ==========================================
# --- YENİ TAKVİM (Kutucuklu & Etkinlikli) ---
# ==========================================
curr_year, curr_month = datetime.date.today().year, datetime.date.today().month




def takvim_ciz():
    for widget in cal_frame.winfo_children(): widget.destroy()
    ctk.CTkLabel(cal_frame, text=f"{calendar.month_name[curr_month]} {curr_year}", font=("Arial", 20, "bold")).pack()
    
    grid = ctk.CTkFrame(cal_frame, fg_color="transparent")
    grid.pack(pady=10)
    
    # --- YENİ: GÜN İSİMLERİ BAŞLIKLARI ---
    gun_isimleri = ["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"]
    for i, isim in enumerate(gun_isimleri):
        # Gün isimleri için küçük, sade birer etiket oluşturuyoruz
        lbl = ctk.CTkLabel(grid, text=isim, font=("Arial", 11, "bold"), text_color="#aaa")
        # row=0 değerini gün isimlerine ayırdık
        lbl.grid(row=0, column=i, pady=(0, 5))
    
    ilkgun, gun_sayisi = calendar.monthrange(curr_year, curr_month)
    gun_sayaci = 1
    
    # Gün isimleri row=0'da olduğu için, takvim kutularını row+1 (yani 1'den 6'ya) olarak başlatıyoruz
    for r in range(6): 
        for c in range(7):
            if (r == 0 and c < ilkgun) or gun_sayaci > gun_sayisi:
                # BOŞ GÜNLER (Transparan)
                box = ctk.CTkFrame(grid, width=80, height=80, fg_color="transparent")
                box.pack_propagate(False) 
                box.grid(row=r+1, column=c, padx=2, pady=2) # r+1 yaptık
            else:
                # DOLU GÜNLER
                box = ctk.CTkFrame(grid, width=80, height=80, border_width=2, border_color="#555", fg_color="#333")
                box.pack_propagate(False) 
                box.grid(row=r+1, column=c, padx=2, pady=2) # r+1 yaptık
                
                # Gün sayısı
                ctk.CTkLabel(box, text=str(gun_sayaci), font=("Arial", 12, "bold")).pack(anchor="nw", padx=5)
                
                # Etkinlik kontrolü
                tarih_key = f"{gun_sayaci:02d}-{curr_month:02d}-{curr_year}"
                if tarih_key in ajanda_verisi and ajanda_verisi[tarih_key]["gorevler"]:
                    ctk.CTkLabel(box, text=ajanda_verisi[tarih_key]["gorevler"][0]["tanim"], font=("Arial", 15), text_color="#AED6F1", wraplength=70).pack(anchor="sw", padx=2)
                
                gun_sayaci += 1




def ay_degis(delta):
    global curr_month, curr_year
    curr_month += delta
    if curr_month > 12: curr_month = 1; curr_year += 1
    if curr_month < 1: curr_month = 12; curr_year -= 1
    takvim_ciz()

def etkinlik_ekle():
    try:
        # Seçilen günü, takvimde o an açık olan dinamik ay (curr_month) ve yıla (curr_year) bağlıyoruz
        tarih = f"{int(gun_entry.get()):02d}-{curr_month:02d}-{curr_year}"
        if tarih not in ajanda_verisi: ajanda_verisi[tarih] = {"gunluk": "", "gorevler": []}
        ajanda_verisi[tarih]["gorevler"].append({"tanim": event_entry.get(), "tamamlandi": False})
        veri_kaydet(AJANDA_DOSYASI, ajanda_verisi)
        takvim_ciz()
        
        # Ekledikten sonra kutuları temizlesin (opsiyonel ama konforludur)
        gun_entry.delete(0, 'end')
        event_entry.delete(0, 'end')
    except ValueError:
        pass # Gün kısmına sayı girilmezse hata vermesin diye önlem

cal_frame = ctk.CTkFrame(sekme_takvim); cal_frame.pack(pady=10)
nav = ctk.CTkFrame(sekme_takvim); nav.pack(pady=5)
ctk.CTkButton(nav, text="<", width=40, command=lambda: ay_degis(-1)).pack(side="left", padx=5)
ctk.CTkButton(nav, text=">", width=40, command=lambda: ay_degis(1)).pack(side="left", padx=5)

ctrl = ctk.CTkFrame(sekme_takvim); ctrl.pack(pady=10)
gun_entry = ctk.CTkEntry(ctrl, width=40, placeholder_text="Gün"); gun_entry.pack(side="left", padx=5)
event_entry = ctk.CTkEntry(ctrl, width=150, placeholder_text="Etkinlik"); event_entry.pack(side="left", padx=5)
ctk.CTkButton(ctrl, text="Ekle/Değiştir", command=etkinlik_ekle).pack(side="left", padx=5)


# ==========================================
# --- MEDYA (EKSİKSİZ) ---
# ==========================================
def medya_ekrani_guncelle():
    medya_textbox.configure(state="normal")
    medya_textbox.delete("1.0", "end")
    
    icerik = "📌 İZLENECEKLER:\n"
    for i, ad in enumerate(medya_verisi["izlenecekler"], 1):
        icerik += f"  {i}. {ad}\n"
        
    icerik += "\n▶️ İZLENİYOR:\n"
    for i, ad in enumerate(medya_verisi["izleniyor"], 1):
        icerik += f"  {i}. {ad}\n"
        
    icerik += "\n✅ BİTTİ:\n"
    for i, ad in enumerate(medya_verisi["bitti"], 1):
        icerik += f"  {i}. {ad}\n"
        
    medya_textbox.insert("end", icerik)
    medya_textbox.configure(state="disabled")

def medya_ekle():
    ad = medya_entry.get()
    if ad:
        medya_verisi["izlenecekler"].append(ad)
        veri_kaydet(MEDYA_DOSYASI, medya_verisi)
        medya_ekrani_guncelle()
        medya_entry.delete(0, 'end')

def izlemeye_basla():
    try:
        idx = int(medya_islem_entry.get()) - 1
        if 0 <= idx < len(medya_verisi["izlenecekler"]):
            ad = medya_verisi["izlenecekler"].pop(idx)
            medya_verisi["izleniyor"].append(ad)
            veri_kaydet(MEDYA_DOSYASI, medya_verisi)
            medya_ekrani_guncelle()
            medya_islem_entry.delete(0, 'end')
    except ValueError: pass

def bitir():
    try:
        idx = int(medya_islem_entry.get()) - 1
        if 0 <= idx < len(medya_verisi["izleniyor"]):
            ad = medya_verisi["izleniyor"].pop(idx)
            medya_verisi["bitti"].append(ad)
            veri_kaydet(MEDYA_DOSYASI, medya_verisi)
            medya_ekrani_guncelle()
            medya_islem_entry.delete(0, 'end')
    except ValueError: pass

def medya_sil():
    try:
        idx = int(medya_islem_entry.get()) - 1
        if 0 <= idx < len(medya_verisi["izlenecekler"]): medya_verisi["izlenecekler"].pop(idx)
        elif 0 <= idx < len(medya_verisi["izleniyor"]): medya_verisi["izleniyor"].pop(idx)
        elif 0 <= idx < len(medya_verisi["bitti"]): medya_verisi["bitti"].pop(idx)
        veri_kaydet(MEDYA_DOSYASI, medya_verisi)
        medya_ekrani_guncelle()
    except ValueError: pass

# Arayüz
medya_entry = ctk.CTkEntry(sekme_medya, placeholder_text="Yeni Dizi/Film...")
medya_entry.pack(pady=5)
ctk.CTkButton(sekme_medya, text="Listeye Ekle", command=medya_ekle).pack(pady=5)

medya_textbox = ctk.CTkTextbox(sekme_medya, height=450, width=400)
medya_textbox.pack(pady=10)

# İşlem Paneli
islem_frame = ctk.CTkFrame(sekme_medya)
islem_frame.pack(pady=10)
medya_islem_entry = ctk.CTkEntry(islem_frame, width=60, placeholder_text="No")
medya_islem_entry.pack(side="left", padx=5)

ctk.CTkButton(islem_frame, text="▶️ İzlemeye Başla", command=izlemeye_basla, width=120).pack(side="left", padx=5)
ctk.CTkButton(islem_frame, text="✅ Bitir", command=bitir, width=60, fg_color="green").pack(side="left", padx=5)
ctk.CTkButton(islem_frame, text="🗑️ Sil", command=medya_sil, width=60, fg_color="red").pack(side="left", padx=5)



# ==========================================
# --- VERTICAL HABIT TRACKER (AŞAĞI DOĞRU EXCEL) ---
# ==========================================
def aliskanlik_ekrani_guncelle():
    global aliskanlik_verisi, curr_month, curr_year
    
    # Ekranı temizle
    for widget in tracker_scroll.winfo_children():
        widget.destroy()

    import datetime, calendar
    
    # Tarihi güvenli al
    try:
        yil = curr_year
        ay = curr_month
    except NameError:
        yil = datetime.date.today().year
        ay = datetime.date.today().month
        
    gun_sayisi = calendar.monthrange(yil, ay)[1]
    ay_adi = calendar.month_name[ay]
    ay_key = f"{ay:02d}-{yil}"

    # JSON verisi bozuksa/boşsa onar
    if not isinstance(aliskanlik_verisi, dict):
        aliskanlik_verisi = {"aliskanliklar": [], "tarihler": {}}
    if "aliskanliklar" not in aliskanlik_verisi:
        aliskanlik_verisi["aliskanliklar"] = []
    if "tarihler" not in aliskanlik_verisi:
        aliskanlik_verisi["tarihler"] = {}

    # 1. ANA BAŞLIK
    baslik = ctk.CTkLabel(tracker_scroll, text=f"📊 {ay_adi} {yil} Matrix", font=("Arial", 16, "bold"), text_color="cyan")
    baslik.grid(row=0, column=0, columnspan=len(aliskanlik_verisi["aliskanliklar"])+1, pady=(10, 20), sticky="w")

    # 2. SÜTUN BAŞLIKLARI (ALIŞKANLIK İSİMLERİ YAN YANA)
    ctk.CTkLabel(tracker_scroll, text="Günler", font=("Arial", 12, "bold"), text_color="#aaa").grid(row=1, column=0, padx=10, pady=5)
    
    for c_idx, al_adi in enumerate(aliskanlik_verisi["aliskanliklar"], start=1):
        # Eğer isim çok uzunsa arayüzü bozmasın diye ilk 10 harfini alıp sonuna .. koyuyoruz
        gosterim_adi = al_adi[:10] + ".." if len(al_adi) > 12 else al_adi
        ctk.CTkLabel(tracker_scroll, text=gosterim_adi, font=("Arial", 11, "bold")).grid(row=1, column=c_idx, padx=10, pady=5)
        
        if al_adi not in aliskanlik_verisi["tarihler"][ay_key]:
            aliskanlik_verisi["tarihler"][ay_key][al_adi] = {}

    # 3. GÜNLER VE KUTUCUKLAR (AŞAĞI DOĞRU 30-31 SATIR)
    for g in range(1, gun_sayisi + 1):
        r_idx = g + 1 # Satır numarası
        gun_str = str(g)
        
        # Sol baştaki gün numarası (01, 02, 03...)
        ctk.CTkLabel(tracker_scroll, text=f"{g:02d}", font=("Arial", 10, "bold")).grid(row=r_idx, column=0, padx=10, pady=2)
        
        # O güne ait yan yana kutucuklar
        for c_idx, al_adi in enumerate(aliskanlik_verisi["aliskanliklar"], start=1):
            durum = aliskanlik_verisi["tarihler"][ay_key][al_adi].get(gun_str, False)
            var = ctk.BooleanVar(value=durum)
            
            def durum_kaydet(a_isim=al_adi, g_num=gun_str, v=var):
                aliskanlik_verisi["tarihler"][ay_key][a_isim][g_num] = v.get()
                veri_kaydet(ALISKANLIK_DOSYASI, aliskanlik_verisi)

            # Kutucukları gün satırına yan yana yerleştir
            cb = ctk.CTkCheckBox(tracker_scroll, text="", variable=var, command=durum_kaydet, width=20, checkbox_width=18, checkbox_height=18)
            cb.grid(row=r_idx, column=c_idx, padx=10, pady=2)

def yeni_aliskanlik_ekle():
    global aliskanlik_verisi
    yeni_al = aliskanlik_entry.get()
    if yeni_al and yeni_al not in aliskanlik_verisi.get("aliskanliklar", []):
        aliskanlik_verisi["aliskanliklar"].append(yeni_al)
        veri_kaydet(ALISKANLIK_DOSYASI, aliskanlik_verisi)
        aliskanlik_ekrani_guncelle()
        aliskanlik_entry.delete(0, 'end')

def aliskanlik_sil():
    global aliskanlik_verisi
    silinecek = aliskanlik_entry.get()
    if silinecek in aliskanlik_verisi.get("aliskanliklar", []):
        aliskanlik_verisi["aliskanliklar"].remove(silinecek)
        veri_kaydet(ALISKANLIK_DOSYASI, aliskanlik_verisi)
        aliskanlik_ekrani_guncelle()
        aliskanlik_entry.delete(0, 'end')

# --- ARAYÜZ ELEMANLARI ---
ctk.CTkLabel(sekme_aliskanlik, text="✨ Monthly Habit Matrix", font=("Arial", 18, "bold")).pack(pady=10)

al_frame = ctk.CTkFrame(sekme_aliskanlik)
al_frame.pack(pady=5)

aliskanlik_entry = ctk.CTkEntry(al_frame, placeholder_text="Habit name (Örn: Spor, Su)", width=200)
aliskanlik_entry.grid(row=0, column=0, padx=5)

ctk.CTkButton(al_frame, text="Ekle", command=yeni_aliskanlik_ekle, width=60, fg_color="green").grid(row=0, column=1, padx=5)
ctk.CTkButton(al_frame, text="Sil", command=aliskanlik_sil, width=50, fg_color="red").grid(row=0, column=2, padx=5)

# Normal aşağı kaydırma (Vertical)
tracker_scroll = ctk.CTkScrollableFrame(sekme_aliskanlik, width=600, height=350)
tracker_scroll.pack(pady=10, fill="both", expand=True)

# İlk tetikleme


# ==========================================
# --- SKINCARE (CİLT BAKIM ÇİZELGESİ) ---
# ==========================================
def cilt_ekrani_guncelle():
    global cilt_verisi
    
    # Otomatik Haftalık Sıfırlama Kontrolü
    mevcut_hafta = datetime.date.today().isocalendar()[1]
    if cilt_verisi.get("son_hafta") != mevcut_hafta:
        cilt_verisi["durum"] = {} # Tikleri sıfırla
        cilt_verisi["son_hafta"] = mevcut_hafta
        veri_kaydet(CILT_DOSYASI, cilt_verisi)

    # Ekranı temizle
    for widget in cilt_scroll.winfo_children():
        widget.destroy()

    gunler = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]

    for gun in gunler:
        # Gün için şık bir başlık çerçevesi
        gun_frame = ctk.CTkFrame(cilt_scroll, fg_color="#2b2b2b", corner_radius=10)
        gun_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(gun_frame, text=gun, font=("Arial", 14, "bold"), text_color="cyan").pack(anchor="w", padx=10, pady=5)
        
        # O güne ait rutinleri listele
        adımlar = cilt_verisi["rutin"].get(gun, [])
        for i, adim in enumerate(adımlar):
            # Her kutucuk için benzersiz bir ID oluştur (Örn: Pazartesi_0)
            tik_id = f"{gun}_{i}"
            durum = cilt_verisi.get("durum", {}).get(tik_id, False)
            
            var = ctk.BooleanVar(value=durum)
            
            # Tıklandığında kaydedecek fonksiyon
            def kaydet(t_id=tik_id, v=var):
                if "durum" not in cilt_verisi: cilt_verisi["durum"] = {}
                cilt_verisi["durum"][t_id] = v.get()
                veri_kaydet(CILT_DOSYASI, cilt_verisi)

            # Checkbox'u ekle
            cb = ctk.CTkCheckBox(gun_frame, text=adim, variable=var, command=kaydet, font=("Arial", 12))
            cb.pack(anchor="w", padx=20, pady=5)

# --- Arayüz Elemanları ---
baslik_frame = ctk.CTkFrame(sekme_cilt, fg_color="transparent")
baslik_frame.pack(pady=10, fill="x")

ctk.CTkLabel(baslik_frame, text="✨ Haftalık Cilt Bakım Çizelgesi", font=("Arial", 18, "bold")).pack()
ctk.CTkLabel(baslik_frame, text="* Tikler her Pazartesi otomatik sıfırlanır.", font=("Arial", 11, "italic"), text_color="gray").pack()

cilt_scroll = ctk.CTkScrollableFrame(sekme_cilt, width=600, height=500)
cilt_scroll.pack(pady=10, fill="both", expand=True)

# ==========================================
# --- 🏎️ F1 YARIŞ MERKEZİ & CANLI API SIRALAMASI ---
# ==========================================
suanki_yaris_index = 0

def f1_ilk_acilis():
    global suanki_yaris_index
    bugun = datetime.date.today().strftime("%Y-%m-%d")
    for i, yaris in enumerate(f1_verisi):
        if yaris["tarih"] >= bugun:
            suanki_yaris_index = i
            break
            
def f1_ekrani_guncelle():
    global suanki_yaris_index
    for widget in f1_takvim_frame.winfo_children(): widget.destroy()
        
    yaris = f1_verisi[suanki_yaris_index]
    bugun = datetime.date.today().strftime("%Y-%m-%d")
    gecmis_mi = yaris["tarih"] < bugun
    
    renk_baslik = "gray" if gecmis_mi else "cyan"
    durum_metni = "🏁 TAMAMLANDI" if gecmis_mi else "🏎️ YAKLAŞIYOR"
    renk_kutu = "#222222" if gecmis_mi else "#2b2b2b"
    kutu_yazi = "gray" if gecmis_mi else "white"
    
    # --- TAKVİM NAVİGASYONU ---
    nav_frame = ctk.CTkFrame(f1_takvim_frame, fg_color="transparent")
    nav_frame.pack(pady=10, fill="x")
    
    btn_prev = ctk.CTkButton(nav_frame, text="< Önceki", width=70, command=lambda: f1_degistir(-1))
    if suanki_yaris_index == 0: btn_prev.configure(state="disabled")
    btn_prev.pack(side="left", padx=20)
    
    baslik_lbl = ctk.CTkLabel(nav_frame, text=yaris["isim"], font=("Arial", 20, "bold"), text_color=renk_baslik)
    baslik_lbl.pack(side="left", expand=True)
    
    btn_next = ctk.CTkButton(nav_frame, text="Sonraki >", width=70, command=lambda: f1_degistir(1))
    if suanki_yaris_index == len(f1_verisi) - 1: btn_next.configure(state="disabled")
    btn_next.pack(side="right", padx=20)
    
    ctk.CTkLabel(f1_takvim_frame, text=f"{yaris['tarih']} | {durum_metni}", font=("Arial", 12, "bold"), text_color="gray" if gecmis_mi else "green").pack(pady=5)
    
    # --- GÜNLER KUTULARI ---
    gunler_frame = ctk.CTkFrame(f1_takvim_frame, fg_color="transparent")
    gunler_frame.pack(pady=10)
    
    for idx, gun in enumerate(["cuma", "cumartesi", "pazar"]):
        kutu = ctk.CTkFrame(gunler_frame, fg_color=renk_kutu, width=180, height=120)
        kutu.pack_propagate(False)
        kutu.grid(row=0, column=idx, padx=5)
        ctk.CTkLabel(kutu, text=gun.upper(), font=("Arial", 14, "bold"), text_color="red" if not gecmis_mi else "gray").pack(pady=5)
        ctk.CTkLabel(kutu, text=yaris[gun], font=("Arial", 12), text_color=kutu_yazi).pack()

def f1_degistir(yon):
    global suanki_yaris_index
    suanki_yaris_index += yon
    f1_ekrani_guncelle()

# --- INTERNETTEN CANLI VERİ ÇEKME İŞLEMİ (GÜVENLİ) ---
def canli_siralamayi_cek():
    # Önce listeyi temizle ve "yükleniyor" ekranı koy
    for widget in f1_siralama_frame.winfo_children(): widget.destroy()
    ctk.CTkLabel(f1_siralama_frame, text="⏳ İnternetten Canlı Veri Çekiliyor...", font=("Arial", 14), text_color="yellow").pack(pady=30)
    
    def api_istegi():
        try:
            # Dünyaca ünlü ücretsiz F1 Ergast API (Jolpi Mirror) - Her yarış sonrası otomatik güncellenir
            url = "https://api.jolpi.ca/ergast/f1/current/driverStandings.json"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                veri = json.loads(response.read().decode())
                
            standings = veri["MRData"]["StandingsTable"]["StandingsLists"][0]["DriverStandings"]
            
            # Uygulama çökmesin diye veriyi ana ekrana (main thread) güvenle gönderiyoruz
            app.after(0, lambda: siralama_ekrani_ciz(standings))
            
        except Exception:
            # İnternet yoksa programı KİTLEMİYORUZ. Hata ekranı çiziyoruz!
            app.after(0, lambda: siralama_hata_ciz())
            
    # Uygulamanın donmaması için indirmeyi arka planda başlat
    threading.Thread(target=api_istegi, daemon=True).start()

def siralama_ekrani_ciz(standings):
    for widget in f1_siralama_frame.winfo_children(): widget.destroy()
    
    baslik_frame = ctk.CTkFrame(f1_siralama_frame, fg_color="transparent")
    baslik_frame.pack(fill="x", pady=(5, 10))
    
    ctk.CTkLabel(baslik_frame, text="🌍 CANLI SÜRÜCÜLER ŞAMPİYONASI", font=("Arial", 15, "bold"), text_color="red").pack(side="left", padx=10)
    ctk.CTkButton(baslik_frame, text="🔄 Yenile", command=canli_siralamayi_cek, width=70, height=26).pack(side="right", padx=10)
    
    # Puanların akacağı liste tasarımı
    liste_scroll = ctk.CTkScrollableFrame(f1_siralama_frame, width=580, height=220)
    liste_scroll.pack(fill="both", expand=True, padx=10, pady=5)
    
    for surucu in standings:
        sira = surucu["position"]
        isim = f"{surucu['Driver']['givenName']} {surucu['Driver']['familyName']}"
        takim = surucu["Constructors"][0]["name"]
        puan = surucu["points"]
        
        satir = ctk.CTkFrame(liste_scroll, fg_color="transparent")
        satir.pack(fill="x", pady=2)
        
        ctk.CTkLabel(satir, text=f"{sira}.", font=("Arial", 14, "bold"), width=30, anchor="w").pack(side="left")
        ctk.CTkLabel(satir, text=isim, font=("Arial", 14, "bold")).pack(side="left", padx=10)
        ctk.CTkLabel(satir, text=takim, font=("Arial", 12), text_color="gray").pack(side="left", padx=10)
        ctk.CTkLabel(satir, text=f"{puan} Puan", font=("Arial", 14, "bold"), text_color="#016455").pack(side="right", padx=10)

def siralama_hata_ciz():
    for widget in f1_siralama_frame.winfo_children(): widget.destroy()
    ctk.CTkLabel(f1_siralama_frame, text="⚠️ İnternet bağlantısı yok veya F1 Sunucusu yanıt vermedi.", text_color="red", font=("Arial", 14, "bold")).pack(pady=20)
    ctk.CTkButton(f1_siralama_frame, text="🔄 Tekrar Dene", command=canli_siralamayi_cek).pack(pady=5)


# --- ANA GÖVDE ÇERÇEVELERİ ---
f1_takvim_frame = ctk.CTkFrame(sekme_f1, fg_color="transparent")
f1_takvim_frame.pack(fill="x", pady=(5, 0))

# Araya şık bir ayrım çizgisi
ctk.CTkFrame(sekme_f1, height=2, fg_color="#444").pack(fill="x", padx=20, pady=5)

# API Verisinin Çizileceği Çerçeve
f1_siralama_frame = ctk.CTkFrame(sekme_f1, fg_color="#1a1a1a", corner_radius=10)
f1_siralama_frame.pack(fill="both", expand=True, padx=10, pady=10)

# İlk tetiklemeler
f1_ilk_acilis()
f1_ekrani_guncelle()
canli_siralamayi_cek() # Uygulama açılır açılmaz internetten puanları çeker!





cilt_ekrani_guncelle()

aliskanlik_ekrani_guncelle()

medya_ekrani_guncelle()
takvim_ciz()
app.mainloop()

