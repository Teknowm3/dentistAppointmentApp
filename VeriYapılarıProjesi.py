# Version 0.2
# Yapılacaklar 
# Diş Hekimleri yarat onlara göre randevular alınsın.  X -- >   !!-- Oncelikli --!!
# Zaman kisminda 10:3 seklinde girilirse bir bug oluyor onu duzelt.  X -- > Oncelikli

# Yapılanlar
# 10 dakika aralıklı alınan saat aralığını çıkartmışım geri ekledim.

import tkinter as tk
from tkinter import messagebox
from datetime import datetime , timedelta

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

class DentistAppointmentSystem:
    def __init__(self):
        self.appointments = LinkedList()

    def is_valid_appointment_time(self, time):
        #   Istenilen saat araliklari.
        start_morning_time = datetime.strptime("09:00", "%H:%M")
        end_morning_time = datetime.strptime("11:20", "%H:%M")
        start_afternoon_time = datetime.strptime("13:00", "%H:%M")
        end_afternoon_time = datetime.strptime("16:50", "%H:%M")

        #   Verilen saat bilgisini datetime nesnesine cevir.
        appointment_time = datetime.strptime(time, "%H:%M")

        #                           09:00 - 11:30                                                   13:00 - 17:00
        if (start_morning_time <= appointment_time <= end_morning_time) or (start_afternoon_time <= appointment_time <= end_afternoon_time):
            return True    #  Uygun Saat
        else:
            return False   #  Uygun Olmayan Saat

    #   Randevu Ekleme 
    def schedule_appointment(self, patient_name, date, time, appointment_type):
        if not self.is_valid_appointment_time(time):
            return False

        new_appointment_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")  # new_appointment_time tanımlandı

        # Alınan Randevu Saati 10 dk öncesi ve 10 dk sonrasını alınamaz yapar.
        current_node = self.appointments.head
        while current_node:
            existing_appointment = current_node.data
            existing_appointment_time = datetime.strptime(f"{existing_appointment['date']} {existing_appointment['time']}", "%Y-%m-%d %H:%M")

            if new_appointment_time > existing_appointment_time - timedelta(minutes=10) and new_appointment_time < existing_appointment_time + timedelta(minutes=10):
                return False  # Saat çakışıyor

            current_node = current_node.next

        # Başka bir randevu izni kontrolü
        other_appointment_time = datetime.now() + timedelta(minutes=10)  # Randevu bitiş tarihinden 10 dakika sonrasına yeni randevu alınabilir
        current_node = self.appointments.head
        while current_node:
            existing_appointment = current_node.data
            existing_appointment_time = datetime.strptime(f"{existing_appointment['date']} {existing_appointment['time']}", "%Y-%m-%d %H:%M")

            if existing_appointment_time > datetime.now() and existing_appointment_time <= other_appointment_time:
                return False  # Randevu bitiş tarihinden 10 dakika sonrasına başka bir randevu izni var, bu randevu alınamaz

            current_node = current_node.next

        # Yeni Randevu Oluştur.
        new_data = {'patient_name': patient_name, 'date': date, 'time': time, 'type': appointment_type}

        if not self.appointments.head:
            self.appointments.head = Node(new_data)
        else:
            current_node = self.appointments.head
            while current_node.next:
                current_node = current_node.next
            current_node.next = Node(new_data)

        return True


    #   Randevu Silme
    def cancel_appointment(self, date, time):
        current_node = self.appointments.head
        prev_node = None

        while current_node:
            if current_node.data['date'] == date and current_node.data['time'] == time:
                if prev_node:
                    prev_node.next = current_node.next
                else:
                    self.appointments.head = current_node.next
                return True
            prev_node = current_node
            current_node = current_node.next

        return False

    #   Randevu Bilgilerini Toplama
    def get_appointments(self):
        appointments_list = []
        current_node = self.appointments.head

        while current_node:
            appointments_list.append(current_node.data)
            current_node = current_node.next
            
        #   Randevuları tarih ve saate göre sırala
        sorted_appointments = sorted(appointments_list, key=lambda x: datetime.strptime(f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"))
        return sorted_appointments
class DentistAppointmentSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Diş Hekimliği Randevu Sistemi")
        self.dentist_system = DentistAppointmentSystem()

        self.name_label = tk.Label(root, text="Hasta Adı:")
        self.name_entry = tk.Entry(root)

        self.date_label = tk.Label(root, text="Tarih: \nYYYY-MM-DD")
        self.date_entry = tk.Entry(root)

        self.time_label = tk.Label(root, text="Saat: \nHH:MM")
        self.time_entry = tk.Entry(root)

        self.type_label = tk.Label(root, text="Randevu Türü:")
        self.type_var = tk.StringVar()
        self.type_var.set("Lütfen Seçim Yapınız")
        self.type_menu = tk.OptionMenu(root, self.type_var, 
                                       "Lütfen Seçim Yapınız", "Diş Muayene", "Temel Diş Bakımı", 
                                       "Dolgu Muayenesi", "Diş Çekimi", "Kanal Tedavisi", "Diş Protezi", 
                                       "Ortodontik Muayene", "Estetik Diş Hekimliği", "Ağız Cerrahisi", 
                                       "Periodontal Tedavi", "Pedodontik Randevu (Çocuk Diş Hekimliği)", 
                                       "Temporomandibular Eklem (TMJ) Muayenesi")

        self.schedule_button = tk.Button(root, text="Randevu Al", command=self.schedule_appointment)
        self.cancel_button = tk.Button(root, text="Randevu İptali", command=self.cancel_appointment)
        self.display_button = tk.Button(root, text="Randevu Listesini Görüntüle", command=self.display_appointments)

        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.date_label.grid(row=1, column=0, padx=10, pady=10)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)
        self.time_label.grid(row=2, column=0, padx=10, pady=10)
        self.time_entry.grid(row=2, column=1, padx=10, pady=10)
        self.type_label.grid(row=3, column=0, padx=10, pady=10)
        self.type_menu.grid(row=3, column=1, padx=10, pady=10)
        self.schedule_button.grid(row=4, column=0,  columnspan=2, padx=10, pady=10)
        self.cancel_button.grid(row=5, column=0,  columnspan=2, padx=10, pady=10)
        self.display_button.grid(row=6, column=0, columnspan=2, pady=10, padx=80)

    def schedule_appointment(self):
        patient_name = self.name_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        appointment_type = self.type_var.get()

        if not patient_name:
            messagebox.showerror("Hata", "Hasta adı boş bırakılamaz. \nLütfen geçerli bir hasta adı girin!")
            return
        elif not patient_name.isalpha():
            messagebox.showerror("Hata", "Hasta adı sadece içermelidir! \nLütfen geçerli bir hasta adı girin!")
            return

        try:
            appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Hata", "Lütfen geçerli bir tarih ve saat girin (örneğin, '2023-11-26 14:30').")
            return

        if not self.dentist_system.is_valid_appointment_time(time):
            messagebox.showerror("Hata", "Belirtilen saat aralığında randevu alınamaz!")
            return

        if appointment_type == "Lütfen Seçim Yapınız":
            messagebox.showerror("Hata", "Lütfen geçerli bir randevu türü seçin!")
            return
        elif self.dentist_system.schedule_appointment(patient_name, date, time, appointment_type):
            messagebox.showinfo("Başarılı", "Randevu başarıyla alındı!")
        else:
            messagebox.showerror("Hata", "Randevu alınamadı. Lütfen uygun bir saat seçin!")

    def cancel_appointment(self):
        date = self.date_entry.get()
        time = self.time_entry.get()
        if self.dentist_system.cancel_appointment(date, time):
            messagebox.showinfo("Başarılı", "Randevu başarıyla iptal edildi!")
        else:
            messagebox.showerror("Hata", "Randevu iptal edilemedi! Belirtilen tarihte ve saatte randevu bulunamadı!")

    def display_appointments(self):
        appointments = self.dentist_system.get_appointments()
        if not appointments:
            messagebox.showinfo("Bilgi", "Henüz randevu bulunmamaktadır!")
        else:
            appointment_str = "\n".join([f"Hasta: {appointment['patient_name']} | Muayene Tarihi: {appointment['date']} | Saat: {appointment['time']} | Muayene Türü: {appointment['type']}" for appointment in appointments])
            messagebox.showinfo("Randevu Listesi", appointment_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = DentistAppointmentSystemUI(root)
    root.mainloop()
