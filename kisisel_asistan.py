import customtkinter as ctk
import json
import os
import datetime
import calendar

# --- 1. DOSYA AYARLARI ---
BUTCE_DOSYASI = "butce.json"
AJANDA_DOSYASI = "Yillik_Ajanda.json"
MEDYA_DOSYASI = "Medya_Listesi.json"
ALISKANLIK_DOSYASI = "aliskanlik.json" 

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

# --- 2. ARAYÜZ KURULUMU ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x800") 
app.title("🚀 Kişisel Dijital Asistan v8.0 - Tam Çalışan Sürüm")

sekmeler = ctk.CTkTabview(app)
sekmeler.pack(padx=20, pady=20, fill="both", expand=True)

sekme_butce = sekmeler.add("💰 Bütçe")
sekme_ajanda = sekmeler.add("📓 Ajanda")
sekme_takvim = sekmeler.add("📅 Takvim")
sekme_medya = sekmeler.add("🎬 Medya")
sekme_aliskanlik = sekmeler.add("🎯 Habit Tracker")

# ==========================================
# --- BÜTÇE ---
# ==========================================
def butce_ekrani_guncelle():
    toplam_harcama = sum(h["tutar"] for h in butce_verisi["harcamalar"])
    kalan = butce_verisi["gelir"] - toplam_harcama
    ozet_metni = f"💵 Gelir: {butce_verisi['gelir']:.2f} TL\n💸 Gider: {toplam_harcama:.2f} TL\n------------------------\n📈 Kalan: {kalan:.2f} TL"
    butce_ozet_label.configure(text=ozet_metni, text_color="red" if kalan < 0 else "white")

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
    except: pass

butce_ozet_label = ctk.CTkLabel(sekme_butce, text="", font=("Courier", 16), justify="left")
butce_ozet_label.pack(pady=10)
kat_frame = ctk.CTkFrame(sekme_butce); kat_frame.pack(pady=5)
kat_entry = ctk.CTkEntry(kat_frame, placeholder_text="Yeni Kategori Adı"); kat_entry.pack(side="left", padx=5)
ctk.CTkButton(kat_frame, text="+", command=yeni_kategori_ekle, width=30).pack(side="left", padx=5)
gelir_entry = ctk.CTkEntry(sekme_butce, placeholder_text="Yeni Gelir Miktarı"); gelir_entry.pack(pady=5)
ctk.CTkButton(sekme_butce, text="Gelir Güncelle", command=gelir_ekle).pack(pady=5)
kategori_secim = ctk.CTkOptionMenu(sekme_butce, values=butce_verisi["kategoriler"]); kategori_secim.pack(pady=10)
aciklama_entry = ctk.CTkEntry(sekme_butce, placeholder_text="Açıklama"); aciklama_entry.pack(pady=5)
tutar_entry = ctk.CTkEntry(sekme_butce, placeholder_text="Tutar (TL)"); tutar_entry.pack(pady=5)
ctk.CTkButton(sekme_butce, text="Harcama Ekle", command=harcama_ekle, fg_color="red").pack(pady=10)
butce_ekrani_guncelle()

# ==========================================
# --- AJANDA ---
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

ajanda_textbox = ctk.CTkTextbox(sekme_ajanda, height=500, width=500)
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
aliskanlik_ekrani_guncelle()




medya_ekrani_guncelle()
takvim_ciz()
app.mainloop()
