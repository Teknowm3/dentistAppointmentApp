# Version 0.14

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

class DentistAppointmentSystem:
    def __init__(self):
        self.appointments = []

    def schedule_appointment(self, patient_name, date, time, appointment_type):
        # Saat çakışmasını kontrol et
        new_appointment_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

        # Yeni randevunun saati, mevcut randevunun bitiş saatinden önce olmalıdır (örneğin, 10:30'dan önce)
        for appointment in self.appointments:
            existing_appointment_time = datetime.strptime(f"{appointment['date']} {appointment['time']}", "%Y-%m-%d %H:%M")
            if new_appointment_time >= existing_appointment_time and new_appointment_time < existing_appointment_time + timedelta(minutes=10):
                return False  # Saat çakışıyor

        # Yeni randevunun saati, mevcut saat + 10 dakika sonrasından önce olmalıdır
        appointment_limit_time = datetime.now() + timedelta(minutes=10)
        if new_appointment_time <= appointment_limit_time:
            return False  # 10 dakikadan önce randevu alınamaz

        # Yeni randevunun saati, mevcut saat - 10 dakika öncesinden de önce olmalıdır
        appointment_limit_time = datetime.now() + timedelta(minutes=-10)
        if new_appointment_time <= appointment_limit_time:
            return False  # 10 dakikadan önce randevu alınamaz

        # Başka bir randevu izni kontrolü
        other_appointment_time = datetime.now() + timedelta(minutes=10)  # Randevu bitiş tarihinden 10 dakika sonrasına yeni randevu alınabilir
        for appointment in self.appointments:
            existing_appointment_time = datetime.strptime(f"{appointment['date']} {appointment['time']}", "%Y-%m-%d %H:%M")
            if existing_appointment_time > datetime.now() and existing_appointment_time <= other_appointment_time:
                return False  # Randevu bitiş tarihinden 10 dakika sonrasına başka bir randevu izni var, bu randevu alınamaz

        # Yeni randevuyu ekle
        self.appointments.append({'patient_name': patient_name, 'date': date, 'time': time, 'type': appointment_type})
        return True

    def cancel_appointment(self, date, time):
        for appointment in self.appointments:
            if appointment['date'] == date and appointment['time'] == time:
                self.appointments.remove(appointment)
                return True
        return False  # Belirtilen tarihte ve saatte randevu bulunamadı

    def get_appointments(self):
        return self.appointments

class DentistAppointmentSystemUI:
    # İlk çağırılıcak eleman __iniit__
    def __init__(self, root):
        # Arayüzü görüntüleyebilmek için:
        self.root = root
        self.root.title("Diş Hekimliği Randevu Sistemi")

        self.dentist_system = DentistAppointmentSystem()

        # Arayüz elemanları
        self.name_label = tk.Label(root, text="Hasta Adı:")
        self.name_entry = tk.Entry(root)

        self.date_label = tk.Label(root, text="Tarih:")
        self.date_entry = tk.Entry(root)

        self.time_label = tk.Label(root, text="Saat:")
        self.time_entry = tk.Entry(root)

        self.type_label = tk.Label(root, text="Randevu Türü:")
        self.type_var = tk.StringVar()
        self.type_var.set("Lütfen Seçim Yapınız")  # Default olarak Diş Çekme seçili
        self.type_menu = tk.OptionMenu(root, self.type_var, "Diş Muayne", "Temel Diş Bakımı", "Dolgu Muayenesi", "Diş Çekimi" , "Kanal Tedavisi" , "Diş Protezi" , "Ortodontik Muayne" , "Estetik Diş Hekimliği" , "Ağız Cerrahisi" , "Periodontal Tedavi" , "Pedodontik Randevu (Çocuk Diş Hekimliği)"
        , "Temporomandibular Eklem (TMJ) Muayenesi")

        self.schedule_button = tk.Button(root, text="Randevu Al", command=self.schedule_appointment)
        self.cancel_button = tk.Button(root, text="Randevu Sil", command=self.cancel_appointment)
        self.display_button = tk.Button(root, text="Randevu Listesini Görüntüle", command=self.display_appointments)

        # Arayüz elemanlarını grid'e yerleştir
        self.name_label.grid(row=0, column=0, padx=40, pady=10)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)

        self.date_label.grid(row=1, column=0, padx=10, pady=10)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)

        self.time_label.grid(row=2, column=0, padx=10, pady=10)
        self.time_entry.grid(row=2, column=1, padx=10, pady=10)

        self.type_label.grid(row=3, column=0, padx=10, pady=10)
        self.type_menu.grid(row=3, column=1, padx=10, pady=10)

        self.schedule_button.grid(row=4, column=0, pady=10)
        self.cancel_button.grid(row=5, column=0, pady=10)
        self.display_button.grid(row=6, column=0, columnspan=2, pady=10, padx=80)

    def schedule_appointment(self):
        #   Girilen Bilgileri Al.
        patient_name = self.name_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        appointment_type = self.type_var.get()

        try:
            #   Tarih ve saat girişlerini doğru formatta kontrol et
            appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir tarih ve saat girin (örneğin, '2023-11-26 14:30').")
            return

        #   Randevu almak için gerekli kontrolleri yap
        if appointment_type == "Lütfen Seçim Yapınız":
            messagebox.showerror("Hata", "Lütfen geçerli bir randevu türü seçin.")
            return
        elif self.dentist_system.schedule_appointment(patient_name, date, time, appointment_type):
            messagebox.showinfo("Başarılı", "Randevu başarıyla alındı.")
        else:
            messagebox.showerror("Hata", "Randevu alınamadı. Lütfen uygun bir saat seçin.")

    def cancel_appointment(self):
        #   Girilen Bilgileri Al.
        date = self.date_entry.get()
        time = self.time_entry.get()

        if self.dentist_system.cancel_appointment(date, time):
            messagebox.showinfo("Başarılı", "Randevu başarıyla iptal edildi.")
        else:
            messagebox.showerror("Hata", "Randevu iptal edilemedi. Belirtilen tarihte ve saatte randevu bulunamadı.")

    def display_appointments(self):
        #   Girilen Bilgileri Al.
        appointments = self.dentist_system.get_appointments()
        if not appointments:
            messagebox.showinfo("Bilgi", "Henüz randevu bulunmamaktadır.")
        else:
            appointment_str = "\n".join([f"Hasta : {appointment['patient_name']} | Muayne Tarihi : {appointment['date']} | Saat : {appointment['time']} | Muayne Türü : {appointment['type']}" for appointment in appointments])
            messagebox.showinfo("Randevu Listesi", appointment_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = DentistAppointmentSystemUI(root)
    root.mainloop()
