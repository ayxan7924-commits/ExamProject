import customtkinter as ctk
from tkinter import messagebox
import random

# --- Global dəyişənlər ---
window = None
index = 0
btns = []
lbl = None
mukafat_labels = []
joker_5050_used = False
joker_call_used = False
joker_zal_used = False
oyuncu_ad = ""
oyuncu_soyad = ""

# --- Suallar ---
suallar = [
    ("Azərbaycanın paytaxtı hansıdır?", ["Bakı", "Gəncə", "Sumqayıt", "Şəki"], "A"),
    ("Dünyanın ən böyük okeanı hansıdır?", ["Atlantik", "Hind", "Sakit", "Şimal Buzlu"], "C"),
    ("Azərbaycan hansı qitədə yerləşir?", ["Asiya", "Afrika", "Avropa", "Amerika"], "A"),
    ("Neftlə zəngin şəhər hansıdır?", ["Şamaxı", "Bakı", "Lənkəran", "Quba"], "B"),
    ("İlk kompüter nə vaxt yaradılıb?", ["1940", "1950", "1936", "1925"], "C"),
    ("Ən uzun çay hansıdır?", ["Nil", "Amazon", "Volqa", "Kür"], "B"),
    ("Qarabağ Azərbaycanın hansı bölgəsindədir?", ["Şimal", "Cənub", "Qərb", "Şərq"], "C"),
    ("Azərbaycan Respublikasının prezidenti kimdir?", ["İlham Əliyev", "Heydər Əliyev", "Rəcəb Ərdoğan", "Vladimir Putin"], "A"),
    ("Şahmat fiqurlarından biri hansıdır?", ["Qala", "Piyada", "Meymun", "Dovşan"], "B"),
    ("Hansı planet Günəşə ən yaxındır?", ["Merkuri", "Jupiter", "Saturn", "Mars"], "A")
]

# --- Mükafatlar ---
mukafatlar = [
    "2 000", "4 000", "8 000", "16 000", "32 000",
    "64 000", "125 000", "250 000", "500 000", "1 000 000"
]

# --- Pəncərə yaradılır ---
def arxaplan():
    global window
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk(fg_color="#4B0082")  
    window.title("Kim Milyoner Olmaq İstəyir?")
    window.geometry("900x600+300+80")
    window.resizable(False, False)

    window.main_frame = ctk.CTkFrame(window, width=880, height=580,
                                     corner_radius=10,
                                     fg_color="transparent")
    window.main_frame.place(x=10, y=10)

# --- Başlanğıc ekran ---
def basla_ekrani():
    temizle_sual_panel()
    global joker_5050_used, joker_call_used, joker_zal_used
    joker_5050_used = False
    joker_call_used = False
    joker_zal_used = False

    lbl_ad = ctk.CTkLabel(window, text="Adınızı daxil edin:", font=("Arial", 14))
    lbl_ad.place(x=50, y=80)
    entry_ad = ctk.CTkEntry(window, width=250, height=30, font=("Arial", 14))
    entry_ad.place(x=50, y=110)

    lbl_soyad = ctk.CTkLabel(window, text="Soyadınızı daxil edin:", font=("Arial", 14))
    lbl_soyad.place(x=50, y=160)
    entry_soyad = ctk.CTkEntry(window, width=250, height=30, font=("Arial", 14))
    entry_soyad.place(x=50, y=190)

    def oyuna_basla():
        global oyuncu_ad, oyuncu_soyad
        oyuncu_ad = entry_ad.get()
        oyuncu_soyad = entry_soyad.get()
        if oyuncu_ad == "" or oyuncu_soyad == "":
            messagebox.showwarning("Xəta", "Zəhmət olmasa ad və soyad daxil edin!")
            return
        basla_oyun()

    btn_start = ctk.CTkButton(window, text="Başla", width=180, height=45, fg_color="#32CD32",
                              hover_color="#2eb82e", text_color="white",
                              font=("Arial", 18, "bold"), command=oyuna_basla)
    btn_start.place(x=50, y=240)

# --- Oyunu başlat ---
def basla_oyun():
    global index
    index = 0
    temizle_sual_panel()
    mukafat_paneli_yarat()
    suallarigoster()

# --- Mükafat paneli ---
def mukafat_paneli_yarat():
    global mukafat_labels
    for lbl in mukafat_labels:
        try: lbl.destroy()
        except: pass
    mukafat_labels = []
    for i, val in enumerate(mukafatlar):
        lbl = ctk.CTkLabel(window, text=val, width=120, height=30, font=("Arial", 12, "bold"))
        lbl.place(x=750, y=40 + i*40)
        mukafat_labels.append(lbl)

# --- Xoş gəldiniz yazısı ---
def xos_geldiniz():
    lbl_xos = ctk.CTkLabel(window, text=f"Xoş gəldiniz: {oyuncu_ad} {oyuncu_soyad}",
                           font=("Arial", 12, "italic"))
    lbl_xos.place(x=20, y=560)

# --- Təbrik pəncərəsi ---
# --- Təbrik pəncərəsi ---
def tebrik_ekrani(mesaj, reng="#228B22"):
    top = ctk.CTkToplevel(window)
    top.title("Təbriklər!")
    top.geometry("500x300")
    top.resizable(False, False)
    top.configure(fg_color=reng)

    # Əsas pəncərənin koordinatlarını götür
    window.update_idletasks()
    main_x = window.winfo_x()
    main_y = window.winfo_y()
    main_w = window.winfo_width()

    # Sağ tərəfə yerləşdiririk
    new_x = main_x + main_w + 20
    new_y = main_y + 50

    top.geometry(f"500x300+{new_x}+{new_y}")

    lbl = ctk.CTkLabel(top, text=mesaj,
                       font=("Impact", 22, "bold"),
                       text_color="white",
                       wraplength=450, justify="center")
    lbl.pack(pady=40)

    btn = ctk.CTkButton(top, text="Yenidən Oyna", fg_color="#FFD700",
                        text_color="black", width=150, height=40,
                        font=("Arial", 14, "bold"),
                        command=lambda:[top.destroy(), basla_oyun()])
    btn.pack(pady=20)

    btn2 = ctk.CTkButton(top, text="Çıxış", fg_color="#FF0000",
                         text_color="white", width=150, height=40,
                         font=("Arial", 14, "bold"),
                         command=lambda: window.destroy())
    btn2.pack()


# --- Oyunu dayandırmaq funksiyası ---
def dayandir():
    qerar = messagebox.askokcancel("Dayandırmaq", "Pulu götürüb oyunu dayandırmaq istəyirsiniz?")
    if qerar:
        qazanc = mukafatlar[index-1] if index > 0 else "0"
        tebrik_ekrani(f"Siz {qazanc} AZN qazandınız!", reng="#1E90FF")
        return True
    return False

# --- Sualları göstər ---
def suallarigoster():
    global index, btns, lbl, joker_5050_btn, joker_call_btn, joker_zal_btn
    temizle_sual_panel()

    lbl = ctk.CTkLabel(window, text=suallar[index][0], font=("Impact", 16, "bold"),
                       wraplength=580, justify="left")
    lbl.place(x=20, y=20)

    cavablar = suallar[index][1]
    btns = []
    for i in range(4):
        btn = ctk.CTkButton(window, text=cavablar[i], width=360, height=40,
                            font=("Arial", 12, "bold"), command=lambda x=i: yoxla(x))
        btn.place(x=20, y=80 + i*60)
        btns.append(btn)

    joker_5050_btn = ctk.CTkButton(window, text="50/50", width=120, height=40,
                                   font=("Arial", 12, "bold"), command=joker_5050)
    joker_5050_btn.place(x=20, y=340)

    joker_call_btn = ctk.CTkButton(window, text="Dostuna zəng", width=140, height=40,
                                   font=("Arial", 12, "bold"), command=joker_call)
    joker_call_btn.place(x=160, y=340)

    joker_zal_btn = ctk.CTkButton(window, text="Zal köməyi", width=140, height=40,
                                  font=("Arial", 12, "bold"), command=joker_zal)
    joker_zal_btn.place(x=320, y=340)

    xos_geldiniz()
    update_mukafat_panel()

# --- Cavabı yoxla ---
def yoxla(secilen_index):
    global index
    duzgun_harf = suallar[index][2]
    cavab_harfi = ["A", "B", "C", "D"][secilen_index]

    if cavab_harfi == duzgun_harf:
        index += 1
        if index == 7:  # 7-ci suala çatanda dayandırma sualı
            if dayandir():
                return
        if index < len(suallar):
            suallarigoster()
        else:
            tebrik_ekrani("Təbriklər! Siz 1 000 000 AZN qazandınız! 🎉", reng="#228B22")
    else:
        tebrik_ekrani("Oyununuz başa çatdı! Təəssüf, cavab yanlışdır. 😔", reng="#8B0000")

    update_mukafat_panel()

# --- 50/50 Joker ---
def joker_5050():
    global joker_5050_used
    if joker_5050_used:
        messagebox.showinfo("Joker", "50/50 artıq istifadə olunub!")
        return
    joker_5050_used = True

    duzgun_harf = suallar[index][2]
    duzgun_idx = ["A","B","C","D"].index(duzgun_harf)

    hide_count = 0
    while hide_count < 2:
        rand_idx = random.randint(0,3)
        if rand_idx != duzgun_idx and btns[rand_idx].winfo_viewable():
            btns[rand_idx].place_forget()
            hide_count += 1

# --- Dostuna zəng Joker ---
def joker_call():
    global joker_call_used
    if joker_call_used:
        messagebox.showinfo("Joker", "Dostuna zəng artıq istifadə olunub!")
        return
    joker_call_used = True
    duzgun_harf = suallar[index][2]
    messagebox.showinfo("Dostuna zəng", f"Dostunuz deyir ki, doğru cavab: {duzgun_harf}")

# --- Zal köməyi Joker ---
def joker_zal():
    global joker_zal_used
    if joker_zal_used:
        messagebox.showinfo("Joker", "Zal köməyi artıq istifadə olunub!")
        return
    joker_zal_used = True
    duzgun_harf = suallar[index][2]
    messagebox.showinfo("Zal köməyi", f"Zal deyir ki, doğru cavab: {duzgun_harf}")

# --- Paneli təmizlə ---
def temizle_sual_panel():
    for widget in window.winfo_children():
        if widget not in mukafat_labels and widget is not getattr(window,'main_frame',None):
            try: widget.destroy()
            except: pass

# --- Mükafat panelini yenilə ---
def update_mukafat_panel():
    for i, lbl in enumerate(mukafat_labels):
        try:
            if i == index:
                lbl.configure(fg_color="#2ecc71")
            else:
                lbl.configure(fg_color=None)
        except: pass
