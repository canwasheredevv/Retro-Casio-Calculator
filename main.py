import tkinter as tk
import math

class CasioHesapMakinesi:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("Casio Retro Hesap Makinesi")
        self.pencere.geometry("350x480")
        self.pencere.configure(bg="#2d3130")
        
        self.sonuc_ekranda = False
        self.arayuz_olustur()
        
        
        self.pencere.bind("<Return>", lambda e: self.hesapla())
        self.pencere.bind("<Escape>", lambda e: self.temizle())
        self.pencere.bind("<BackSpace>", lambda e: self.klavyeden_sil(e))

    def arayuz_olustur(self):
        
        self.gecmis_etiket = tk.Label(self.pencere, text="", font=("Courier", 10, "bold"), bg="#8b958f", fg="#2a302c", anchor="e")
        self.gecmis_etiket.pack(fill=tk.X, padx=20, pady=(20, 0))

        
        vcmd = (self.pencere.register(self.karakter_kontrol), '%S')

        
        self.ekran = tk.Entry(self.pencere, font=("Courier", 32, "bold"), bg="#8b958f", fg="#1a201c", 
                              bd=0, justify="right", validate="key", validatecommand=vcmd,
                              insertbackground="#1a201c")
        self.ekran.pack(fill=tk.X, padx=20, pady=(0, 20), ipady=10)
        self.ekran.focus_set()

        
        self.buton_cerceve = tk.Frame(self.pencere, bg="#2d3130")
        self.buton_cerceve.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        
        butonlar = [
            ['C', '←', '%', '/'],
            ['(', ')', 'x²', '√'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', 'SKIP', '.', '=']
        ]

        for satir_idx, satir in enumerate(butonlar):
            for sutun_idx, sembol in enumerate(satir):
                if sembol == 'SKIP': continue 
                
                
                bg_renk = "#3e4241"
                fg_renk = "#ffffff"
                
                if sembol in ['/', '*', '-', '+']:
                    bg_renk = "#575c5b"
                elif sembol in ['C', '←']:
                    bg_renk = "#a63a3a"
                elif sembol == '=':
                    bg_renk = "#2a5c4d"

                columnspan = 2 if sembol == '0' else 1

                btn = tk.Button(self.buton_cerceve, text=sembol, font=("Courier", 14, "bold"), 
                                bg=bg_renk, fg=fg_renk, bd=1, relief="raised",
                                command=lambda s=sembol: self.buton_tikla(s))
                
                btn.grid(row=satir_idx, column=sutun_idx, columnspan=columnspan, sticky="nsew", padx=3, pady=3)

        for i in range(6): self.buton_cerceve.rowconfigure(i, weight=1)
        for i in range(4): self.buton_cerceve.columnconfigure(i, weight=1)

    def karakter_kontrol(self, metin):
        
        izin_verilenler = "0123456789+-*/().%"
        if metin in izin_verilenler:
            if self.sonuc_ekranda and metin.isdigit():
                self.pencere.after(1, self.temizle)
            self.sonuc_ekranda = False
            return True
        return False

    def buton_tikla(self, sembol):
        mevcut = self.ekran.get()
        
        if self.sonuc_ekranda and sembol not in ['+', '-', '*', '/', '%', 'x²', '√', '=', '←']:
            self.temizle()
            self.sonuc_ekranda = False

        if sembol == "C": self.temizle()
        elif sembol == "←": self.tek_sil()
        elif sembol == "=": self.hesapla()
        elif sembol == "x²": self.ust_al(mevcut, 2)
        elif sembol == "√": self.ust_al(mevcut, 0.5)
        else:
            self.ekran.insert(tk.END, sembol)

    def temizle(self):
        self.ekran.delete(0, tk.END)
        self.gecmis_etiket.config(text="")
        self.sonuc_ekranda = False

    def tek_sil(self):
        
        if self.sonuc_ekranda:
            self.temizle()
        else:
            self.ekran.delete(len(self.ekran.get())-1, tk.END)

    def klavyeden_sil(self, event):
        self.tek_sil()
        return "break"

    def ust_al(self, mevcut, us):
        try:
            sayi = float(mevcut) if mevcut else 0.0
            if us == 0.5 and sayi < 0: raise ValueError
            sonuc = math.sqrt(sayi) if us == 0.5 else sayi ** 2
            if isinstance(sonuc, float): sonuc = round(sonuc, 6)
            
            
            self.ekran.config(validate="none")
            self.ekran.delete(0, tk.END)
            self.ekran.insert(tk.END, str(sonuc))
            self.ekran.config(validate="key")
            
            self.gecmis_etiket.config(text=f"√({mevcut})" if us == 0.5 else f"({mevcut})²")
            self.sonuc_ekranda = True
        except Exception: self.hata_goster()

    def hesapla(self):
        try:
            if not self.ekran.get(): return
            formül = self.ekran.get()
            düzenlenmiş_formül = formül.replace('%', '/100')
            sonuc = eval(düzenlenmiş_formül)
            if isinstance(sonuc, float): sonuc = round(sonuc, 6)
            
            self.gecmis_etiket.config(text=formül + " =")
            
            
            self.ekran.config(validate="none")
            self.ekran.delete(0, tk.END)
            self.ekran.insert(tk.END, str(sonuc))
            self.ekran.config(validate="key")
            
            self.sonuc_ekranda = True
        except ZeroDivisionError: self.hata_goster("Sıfıra Bölünemez")
        except Exception: self.hata_goster()

    def hata_goster(self, mesaj="Hata"):
        self.ekran.config(validate="none")
        self.ekran.delete(0, tk.END)
        self.ekran.insert(tk.END, mesaj)
        self.ekran.config(validate="key")
        self.sonuc_ekranda = True

if __name__ == "__main__":
    kok = tk.Tk()
    uygulama = CasioHesapMakinesi(kok)
    kok.mainloop()
