# Version 0.14.6
# Yapilacaklar 
# Diş Hekimleri yarat onlara göre randevular alınsın.  X -- > !-- Oncelikli --!
# Tarih 2023:10:10 cinsinden veya 20231010 seklinde girilebilir olacak.  X | uzerinde çalışıyorum. -- > Oncelikli
# Zaman kisminda 10:3 seklinde girilirse bir bug oluyor onu duzelt.  X -- > Oncelikli
# Hashmap ile yapilmis versiyonuyla arasindaki farki ogren. X

# NELER YAPILDI
# Belirli saatlerde 09:00 - 11:30 | 13.00 - 17.00 arası randevu alınabiliyor    
# Randevu Seçenekleri Var DEFAULT Değer Gelirse HATA veriyor
# Randevular 10'ar Dakika aralıklarla alınabilir
# Tarih Ve Saate Göre Randevu Alınıyor
# Yapılan Randevular TARIHE SAATE Göre sıralanıp geliyor .sorted metodu kullandık
# Alınabilecek Tarih Ve Saatler Bilgisayar'ın Saatine Göre Referans Alınıyor               V0.14.5
# Fazlalıklık Kodlar Kaldırıldı                                                            V0.14.5
# Açıklamalar ve yapılacaklar eklendi                                                      V0.14.6
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

class DentistAppointmentSystem:
    def __init__(self):
        self.appointments = []

    def is_valid_appointment_time(self, time):
        #   Istenilen saat araliklari
        start_morning_time = datetime.strptime("09:00", "%H:%M")
        end_morning_time = datetime.strptime("11:20", "%H:%M")
        start_afternoon_time = datetime.strptime("13:00", "%H:%M")
        end_afternoon_time = datetime.strptime("16:50", "%H:%M")

        #   Verilen saat bilgisini datetime nesnesine cevir
        appointment_time = datetime.strptime(time, "%H:%M")

        #                           09:00 - 11:30                                                   13:00 - 17:00
        if (start_morning_time <= appointment_time <= end_morning_time) or (start_afternoon_time <= appointment_time <= end_afternoon_time):
            return True  #  Uygun Saat
        else:
            return False #  Uygun Olmayan Saat
        
    #   Randevu Ekleme
    def schedule_appointment(self, patient_name, date, time, appointment_type):
        #   Saat cakismasini kontrol et
        new_appointment_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        #   Yeni randevunun saati, belirtilen saat aralıklarında mı kontrol et
        if not self.is_valid_appointment_time(time):
            return False  # Belirtilen saat aralığında randevu alınamaz.
        
        # Yeni randevunun saati, mevcut randevunun bitis saatinden önce olmalidir.
        for appointment in self.appointments:                                                                                                                               #   appointment olarak self.appointments arasinda gezin
            existing_appointment_time = datetime.strptime(f"{appointment['date']} {appointment['time']}", "%Y-%m-%d %H:%M")                                                 #   Saat kontrolu yapilir
            if new_appointment_time > existing_appointment_time + timedelta(minutes=-10) and new_appointment_time < existing_appointment_time + timedelta(minutes=10):      #   Alinan Randevu Saati 10 dk oncesi ve 10 dk sonrasini alinamaz yapar.
                return False  # Saat cakisiyor

        # Baska bir randevu izni kontrolu
        other_appointment_time = datetime.now() + timedelta(minutes=10)  # Randevu bitis tarihinden 10 dakika sonrasina yeni randevu alinabilir
        for appointment in self.appointments:
            existing_appointment_time = datetime.strptime(f"{appointment['date']} {appointment['time']}", "%Y-%m-%d %H:%M")
            if existing_appointment_time > datetime.now() and existing_appointment_time <= other_appointment_time:
                return False  # Randevu bitis tarihinden 10 dakika sonrasina baska bir randevu izni var, bu randevu alinamaz

        # Yeni randevuyu ekle
        self.appointments.append({'patient_name': patient_name, 'date': date, 'time': time, 'type': appointment_type})
        return True

    #   Randevu Iptali
    def cancel_appointment(self, date, time):
        for appointment in self.appointments:
            if appointment['date'] == date and appointment['time'] == time:
                self.appointments.remove(appointment)
                return True
        return False  # Belirtilen tarihte ve saatte randevu bulunamadi

    #   Randevuları Cagirma
    def get_appointments(self):
        # Randevulari TARIH Ve SAAT'E Göre Sırala
        sorted_appointments = sorted(self.appointments, key=lambda x: (x['date'], x['time']))
        return sorted_appointments

class DentistAppointmentSystemUI:
    def __init__(self, root):
        # Arayuzu göruntuleyebilmek icin:
        self.root = root
        self.root.title("Dis Hekimliği Randevu Sistemi")    #   Arayuz basligi
        self.dentist_system = DentistAppointmentSystem()

        # Arayuz Elemanlari (Etiketler Ve Giris Metinleri)
        self.name_label = tk.Label(root, text="Hasta Adi:")
        self.name_entry = tk.Entry(root)

        self.date_label = tk.Label(root, text="Tarih: \nYYYY-MM-DD")
        self.date_entry = tk.Entry(root)

        self.time_label = tk.Label(root, text="Saat: \nHH:MM")
        self.time_entry = tk.Entry(root)

        self.type_label = tk.Label(root, text="Randevu Turu:")
        self.type_var = tk.StringVar()
        self.type_var.set("Lutfen Secim Yapiniz")  # Default olarak Lutfen Secim Yapiniz kismi secili
        self.type_menu = tk.OptionMenu(root, self.type_var, 
                                       "Lutfen Secim Yapiniz", "Dis Muayne", "Temel Dis Bakimi", 
                                       "Dolgu Muayenesi", "Dis Cekimi", "Kanal Tedavisi", "Dis Protezi", 
                                       "Ortodontik Muayne", "Estetik Dis Hekimligi", "Agiz Cerrahisi", 
                                       "Periodontal Tedavi", "Pedodontik Randevu (Cocuk Dis Hekimligi)", 
                                       "Temporomandibular Eklem (TMJ) Muayenesi")
        #   Randevu al buttonu
        self.schedule_button = tk.Button(root, text="Randevu Al", command=self.schedule_appointment)
        #   Randevuyu Iptal Et Buttonu
        self.cancel_button = tk.Button(root, text="Randevu Iptali", command=self.cancel_appointment)
        #   Randevulari Göster Buttonu
        self.display_button = tk.Button(root, text="Randevu Listesini Göruntule", command=self.display_appointments)

        #       Arayuz Elemanlarini grid'e Yerlestir
        #   Etiketler Ve Giris Kutulari yerlestirmeleri
        #   1. input'un      Asagi  Sag-Sol Sol bosluk Yukari bosluk
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        #   2. input'un
        self.date_label.grid(row=1, column=0, padx=10, pady=10)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)
        #   3. input'un
        self.time_label.grid(row=2, column=0, padx=10, pady=10)
        self.time_entry.grid(row=2, column=1, padx=10, pady=10)
        #   4. Secim Menusu
        self.type_label.grid(row=3, column=0, padx=10, pady=10)
        self.type_menu.grid(row=3, column=1, padx=10, pady=10)
        
        #   Button'larin yerlestirmeleri
        #     Randevu al'in 
        self.schedule_button.grid(row=4, column=0,  columnspan=2, padx=10, pady=10)
        #     Randevu'yu Sil'in   
        self.cancel_button.grid(row=5, column=0,  columnspan=2, padx=10, pady=10)
        #     Randevulari Listele'nin
        self.display_button.grid(row=6, column=0, columnspan=2, pady=10, padx=80)

    def schedule_appointment(self):
        #   Girilen Bilgileri Al.
        patient_name = self.name_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        appointment_type = self.type_var.get()

        #   Hasta Adi Kismi Isimsiz Kalirsa Hata Ver.
        if not patient_name:
            messagebox.showerror("Hata\n", "Lutfen gecerli bir hasta adi girin!")
            return
        
        #   Eğer Hasta Ismi Harf Disi Bir Karakter Ise Hata Ver.
        if not isinstance(patient_name, str) or not patient_name.isalpha():
            messagebox.showerror("Hata", "Hasta adi harf disinda bir yapi icermemelidir!")
            return False
        
        try:
            #   Tarih Ve Saat Girislerini Doğru Formatta mi Olduğunu Kontrol Et.
            appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            #   ValueError Hatası Alınması Durumunda Yeni Bir Format Deniyoruz. 
        except ValueError:
            #   !----------- ANLIK OLARAK ÇALIŞMIYOR 2. TRY YAPISINDA DONUSUMLE ILGILI BIR PROBLEM VAR HARICINDE HATAYA ULASABILIRIZ -----------!
            try:
                #   Tarih Ve Saat Girislerini Doğru Formatta mi Olduğunu Kontrol Et.
                appointment_datetime = datetime.strptime(f"{date} {time}", "%Y%m%d %H:%M") # ÇÖZEMEYE ÇALIŞICAM TAM OLARAK DOĞRU ÇALIŞMIYOR %Y-%m-%d formatına sokmam lazım.
            except ValueError:                
                #   Hata Pencersesinde Tarih Veya Zamanin Hatali Olduğuna Dair Bir Hata Mesaji Yolla. 
                messagebox.showerror("Hata", "Lutfen gecerli bir tarih ve saat girin (örneğin, '2023-11-26 14:30').")
                return
 
        #   17.01 - 08.59 + 11.30 - 13.00 Randevu Alinamaz Olan Aralik Kontrolu
        if not self.dentist_system.is_valid_appointment_time(time):
            messagebox.showerror("Hata", "Belirtilen saat araliğinda randevu alinamaz!")
            return
        
        #   Randevu Almak Icin Gerekli Kontrolleri Yap.
        #   Default Secimdeyse Hata Ver.
        if appointment_type == "Lutfen Secim Yapiniz":
            messagebox.showerror("Hata", "Lutfen gecerli bir randevu turu secin!")
            return
        #   Randevu Olustu.
        elif self.dentist_system.schedule_appointment(patient_name, date, time, appointment_type):
            messagebox.showinfo("Basarili", "Randevu basariyla alindi!")
        else:
            messagebox.showerror("Hata", "Randevu alinamadi. Lutfen uygun bir saat secin!")

    def cancel_appointment(self):
        #   Girilen Bilgileri Al.
        date = self.date_entry.get()
        time = self.time_entry.get()
        #   Varsa Randevuyu iptal if Et / else Etme.
        if self.dentist_system.cancel_appointment(date, time):
            messagebox.showinfo("Basarili", "Randevu basariyla iptal edildi!")
        else:
            messagebox.showerror("Hata", "Randevu iptal edilemedi! \nBelirtilen tarihte ve saatte randevu bulunamadi!")

    def display_appointments(self):
        #   Girilen Bilgileri Al.
        appointments = self.dentist_system.get_appointments()
        #   Randevu Kontrolu
        if not appointments:
            messagebox.showinfo("Bilgi", "Henuz randevu bulunmamaktadir!")
        #   Randevuyu Göster
        else:
            #   .join() ile tüm bilgileri birlestirip appointment_str'ye aktariyoruz.
            appointment_str = "\n".join([f"Hasta : {appointment['patient_name']} | Muayne Tarihi : {appointment['date']} | Saat : {appointment['time']} | Muayne Turu : {appointment['type']}" for appointment in appointments])
            #   
            messagebox.showinfo("Randevu Listesi", appointment_str)

#   Calistirma islemi
if __name__ == "__main__":                  #   Dogrudan calistirmak icin kullanıyoruz.
    root = tk.Tk()                          #   Pencere oluşumu root'a atanır.
    app = DentistAppointmentSystemUI(root)  #   GUI'a root'un yerlestirilecegi arayuz olusturulur.
    root.mainloop()                         #   GUI kapanana kadar calismasını saglar.
