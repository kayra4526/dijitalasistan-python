import customtkinter as ctk
import json
import os
import datetime

# --- 1. VERİ İŞLEMLERİ ---
BUTCE_DOSYASI = "butce.json"
AJANDA_DOSYASI = "Yillik_Ajanda.json"

def veri_yukle(dosya_adi, varsayilan):
    if os.path.exists(dosya_adi):
        with open(dosya_adi, "r", encoding="utf-8") as dosya:
            return json.load(dosya)
    return varsayilan

def veri_kaydet(dosya_adi, veri):
    with open(dosya_adi, "w", encoding="utf-8") as dosya:
        json.dump(veri, dosya, indent=4, ensure_ascii=False)

# Verileri belleğe al
butce_verisi = veri_yukle(BUTCE_DOSYASI, {"gelir": 0.0, "kategoriler": ["Genel", "Market", "Fatura", "Eğlence"], "harcamalar": []})
ajanda_verisi = veri_yukle(AJANDA_DOSYASI, {})

# --- 2. ARAYÜZ (GUI) KURULUMU ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("500x700")
app.title("🚀 Kişisel Dijital Asistan")

# Sekme (Tab) Yöneticisini Oluştur
sekmeler = ctk.CTkTabview(app)
sekmeler.pack(padx=20, pady=20, fill="both", expand=True)

sekme_butce = sekmeler.add("💰 Bütçe Takibi")
sekme_ajanda = sekmeler.add("📓 Ajanda & Görevler")

# ==========================================
# --- 3. BÜTÇE SEKMESİ (Sekme 1) ---
# ==========================================

def butce_ekrani_guncelle():
    toplam_harcama = sum(h["tutar"] for h in butce_verisi["harcamalar"])
    kalan = butce_verisi["gelir"] - toplam_harcama
    ozet_metni = f"💵 Gelir: {butce_verisi['gelir']:.2f} TL\n💸 Gider: {toplam_harcama:.2f} TL\n------------------------\n📈 Kalan: {kalan:.2f} TL"
    butce_ozet_label.configure(text=ozet_metni, text_color="red" if kalan < 0 else "white")

def gelir_ekle():
    try:
        butce_verisi["gelir"] = float(gelir_entry.get())
        veri_kaydet(BUTCE_DOSYASI, butce_verisi)
        butce_ekrani_guncelle()
        gelir_entry.delete(0, 'end')
        butce_durum_label.configure(text="✅ Gelir güncellendi!", text_color="green")
    except ValueError:
        butce_durum_label.configure(text="❌ Geçersiz sayı!", text_color="red")

def harcama_ekle():
    try:
        tutar = float(tutar_entry.get())
        aciklama = aciklama_entry.get()
        if not aciklama: return
        butce_verisi["harcamalar"].append({"kategori": kategori_secim.get(), "aciklama": aciklama, "tutar": tutar})
        veri_kaydet(BUTCE_DOSYASI, butce_verisi)
        butce_ekrani_guncelle()
        tutar_entry.delete(0, 'end')
        aciklama_entry.delete(0, 'end')
        butce_durum_label.configure(text=f"✅ Harcama eklendi!", text_color="green")
    except ValueError:
        butce_durum_label.configure(text="❌ Geçersiz tutar!", text_color="red")

# Bütçe Arayüz Elemanları
butce_ozet_label = ctk.CTkLabel(sekme_butce, text="", font=("Courier", 16), justify="left")
butce_ozet_label.pack(pady=10)

ctk.CTkLabel(sekme_butce, text="Yeni Gelir (TL):").pack()
gelir_entry = ctk.CTkEntry(sekme_butce)
gelir_entry.pack(pady=5)
ctk.CTkButton(sekme_butce, text="Gelir Kaydet", command=gelir_ekle).pack(pady=5)

ctk.CTkLabel(sekme_butce, text="--- Harcama Ekle ---", font=("Arial", 14, "bold")).pack(pady=15)
kategori_secim = ctk.CTkOptionMenu(sekme_butce, values=butce_verisi["kategoriler"])
kategori_secim.pack(pady=5)
aciklama_entry = ctk.CTkEntry(sekme_butce, placeholder_text="Açıklama")
aciklama_entry.pack(pady=5)
tutar_entry = ctk.CTkEntry(sekme_butce, placeholder_text="Tutar (TL)")
tutar_entry.pack(pady=5)
ctk.CTkButton(sekme_butce, text="Harcama Ekle", command=harcama_ekle, fg_color="red").pack(pady=10)

butce_durum_label = ctk.CTkLabel(sekme_butce, text="", font=("Arial", 12))
butce_durum_label.pack(pady=5)

butce_ekrani_guncelle()

# ==========================================
# --- 4. AJANDA SEKMESİ (Sekme 2) ---
# ==========================================

def ajanda_ekrani_guncelle():
    tarih = tarih_entry.get()
    ajanda_textbox.configure(state="normal")
    ajanda_textbox.delete("1.0", "end") # Ekranı temizle
    
    if tarih in ajanda_verisi:
        veri = ajanda_verisi[tarih]
        icerik = f"📅 TARİH: {tarih}\n" + "="*30 + "\n"
        icerik += f"📖 GÜNLÜK:\n{veri.get('gunluk', 'Kayıt yok.')}\n\n"
        icerik += "📝 GÖREVLER:\n"
        for i, gorev in enumerate(veri.get("gorevler", []), 1):
            durum = "✅" if gorev["tamamlandi"] else "⬜"
            icerik += f"  {i}. {durum} {gorev['tanim']}\n"
        ajanda_textbox.insert("end", icerik)
    else:
        ajanda_textbox.insert("end", f"ℹ️ {tarih} için henüz kayıt yok.")
    ajanda_textbox.configure(state="disabled")

def gunluk_ekle():
    tarih = tarih_entry.get()
    metin = gunluk_entry.get()
    if not metin: return
    
    if tarih not in ajanda_verisi: ajanda_verisi[tarih] = {"gunluk": "", "gorevler": []}
    
    ajanda_verisi[tarih]["gunluk"] += metin + "\n"
    veri_kaydet(AJANDA_DOSYASI, ajanda_verisi)
    ajanda_ekrani_guncelle()
    gunluk_entry.delete(0, 'end')

def gorev_ekle():
    tarih = tarih_entry.get()
    tanim = gorev_entry.get()
    if not tanim: return
    
    if tarih not in ajanda_verisi: ajanda_verisi[tarih] = {"gunluk": "", "gorevler": []}
    
    ajanda_verisi[tarih]["gorevler"].append({"tanim": tanim, "tamamlandi": False})
    veri_kaydet(AJANDA_DOSYASI, ajanda_verisi)
    ajanda_ekrani_guncelle()
    gorev_entry.delete(0, 'end')

# YENİ EKLENENLER: Görev Tamamlama ve Silme
def gorev_tamamla():
    tarih = tarih_entry.get()
    try:
        gorev_no = int(islem_entry.get()) - 1
        if tarih in ajanda_verisi and 0 <= gorev_no < len(ajanda_verisi[tarih]["gorevler"]):
            ajanda_verisi[tarih]["gorevler"][gorev_no]["tamamlandi"] = True
            veri_kaydet(AJANDA_DOSYASI, ajanda_verisi)
            ajanda_ekrani_guncelle()
            islem_entry.delete(0, 'end')
    except ValueError:
        pass # Hatalı girişte bir şey yapma

def gorev_sil():
    tarih = tarih_entry.get()
    try:
        gorev_no = int(islem_entry.get()) - 1
        if tarih in ajanda_verisi and 0 <= gorev_no < len(ajanda_verisi[tarih]["gorevler"]):
            ajanda_verisi[tarih]["gorevler"].pop(gorev_no)
            veri_kaydet(AJANDA_DOSYASI, ajanda_verisi)
            ajanda_ekrani_guncelle()
            islem_entry.delete(0, 'end')
    except ValueError:
        pass

# Ajanda Arayüz Elemanları
bugun = datetime.date.today().strftime("%d-%m-%Y")
ctk.CTkLabel(sekme_ajanda, text="Tarih (GG-AA-YYYY):").pack()
tarih_entry = ctk.CTkEntry(sekme_ajanda)
tarih_entry.insert(0, bugun)
tarih_entry.pack(pady=5)
ctk.CTkButton(sekme_ajanda, text="Tarihi Getir", command=ajanda_ekrani_guncelle).pack(pady=5)

ajanda_textbox = ctk.CTkTextbox(sekme_ajanda, height=200, width=400)
ajanda_textbox.pack(pady=10)

# Günlük ve Görev Ekleme Kutuları
girdi_frame = ctk.CTkFrame(sekme_ajanda)
girdi_frame.pack(pady=5)

gunluk_entry = ctk.CTkEntry(girdi_frame, width=200, placeholder_text="Günlük notu...")
gunluk_entry.grid(row=0, column=0, padx=5, pady=5)
ctk.CTkButton(girdi_frame, text="Not Ekle", command=gunluk_ekle, width=100).grid(row=0, column=1, padx=5, pady=5)

gorev_entry = ctk.CTkEntry(girdi_frame, width=200, placeholder_text="Yeni görev...")
gorev_entry.grid(row=1, column=0, padx=5, pady=5)
ctk.CTkButton(girdi_frame, text="Görev Ekle", command=gorev_ekle, width=100).grid(row=1, column=1, padx=5, pady=5)

# YENİ EKLENEN: Tamamlama ve Silme Arayüzü
islem_frame = ctk.CTkFrame(sekme_ajanda)
islem_frame.pack(pady=10)

islem_entry = ctk.CTkEntry(islem_frame, width=60, placeholder_text="No (1,2..)")
islem_entry.pack(side="left", padx=5)

ctk.CTkButton(islem_frame, text="✅ Tamamla", command=gorev_tamamla, width=90, fg_color="green", hover_color="darkgreen").pack(side="left", padx=5)
ctk.CTkButton(islem_frame, text="🗑️ Sil", command=gorev_sil, width=60, fg_color="red", hover_color="darkred").pack(side="left", padx=5)

ajanda_ekrani_guncelle()

# Uygulamayı başlat
app.mainloop()