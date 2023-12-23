#   Yapılanlar
#   LL yapısına geçildi
#   Seçili olan hekime göre randevu türleri yükleniyor
#   Randevu türü seçildiğinde randevu türü güncelleniyor

#   Yapılacaklar
#   Hekime göre randevuları listeleyen yapıyı yazıcam.
#   GUI'a Hekim fotoğraf'ı koyulacak 
#   GUI'ya kuoyulan 


import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta

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

class Doctor:
    def __init__(self, name, expertise):
        self.name = name
        self.expertise = expertise
        self.appointments = LinkedList() #  Doktor randevularını bağlamak için LL

class DentistAppointmentSystem:
    def __init__(self):
        self.appointments = LinkedList()
        self.doctors = [
            Doctor("Lütfen Doktor Seçiniz", []),
            Doctor("Dr. Ayşe", ["Diş Muayene", "Temel Diş Bakımı", "Dolgu Muayenesi"]),
            Doctor("Dr. Mehmet", ["Diş Çekimi", "Kanal Tedavisi", "Diş Protezi"]),
        ]
        
    def get_doctor_name(self, doctor_name):
        for doctor in self.doctors:
            if doctor.name == doctor_name:
                return doctor
        return None

    def get_doctor_expertise(self, doctor_name):
        doctor = self.get_doctor_name(doctor_name)
        return doctor.expertise if doctor else []

    def get_available_appointment_types(self, doctor_name):
        doctor_expertise = self.get_doctor_expertise(doctor_name)
        return doctor_expertise

    def is_valid_appointment_time(self, time, doctor):
        start_morning_time = datetime.strptime("09:00", "%H:%M")
        end_morning_time = datetime.strptime("11:20", "%H:%M")
        start_afternoon_time = datetime.strptime("13:00", "%H:%M")
        end_afternoon_time = datetime.strptime("16:50", "%H:%M")

        appointment_time = datetime.strptime(time, "%H:%M")

        if (
            (start_morning_time <= appointment_time <= end_morning_time)
            or (start_afternoon_time <= appointment_time <= end_afternoon_time)
        ):
            return True
        else:
            return False

    def schedule_appointment(self, patient_name, date, time, doctor_name, appointment_type):
        if not self.is_valid_appointment_time(time):
            return False

        new_appointment_time = datetime.strptime(
            f"{date} {time}", "%Y-%m-%d %H:%M"
        )

        current_node = self.appointments.head
        while current_node:
            existing_appointment = current_node.data
            existing_appointment_time = datetime.strptime(
                f"{existing_appointment['date']} {existing_appointment['time']}",
                "%Y-%m-%d %H:%M",
            )

            if (
                new_appointment_time > existing_appointment_time - timedelta(minutes=10)
                and new_appointment_time < existing_appointment_time + timedelta(minutes=10)
            ):
                return False

            current_node = current_node.next

        other_appointment_time = datetime.now() + timedelta(minutes=10)
        current_node = self.appointments.head
        while current_node:
            existing_appointment = current_node.data
            existing_appointment_time = datetime.strptime(
                f"{existing_appointment['date']} {existing_appointment['time']}",
                "%Y-%m-%d %H:%M",
            )

            if (
                existing_appointment_time > datetime.now()
                and existing_appointment_time <= other_appointment_time
            ):
                return False

            current_node = current_node.next

        new_data = {
            "patient_name": patient_name,
            "date": date,
            "time": time,
            "type": appointment_type,
            "doctor_name": doctor_name,
        }

        if not self.appointments.head:
            self.appointments.head = Node(new_data)
        else:
            current_node = self.appointments.head
            while current_node.next:
                current_node = current_node.next
            current_node.next = Node(new_data)

        return True

    def cancel_appointment(self, date, time):
        current_node = self.appointments.head
        prev_node = None

        while current_node:
            if (
                current_node.data["date"] == date
                and current_node.data["time"] == time
            ):
                if prev_node:
                    prev_node.next = current_node.next
                else:
                    self.appointments.head = current_node.next
                return True
            prev_node = current_node
            current_node = current_node.next

        return False

    def get_appointments(self):
        appointments_list = []
        current_node = self.appointments.head

        while current_node:
            appointments_list.append(current_node.data)
            current_node = current_node.next

        sorted_appointments = sorted(
            appointments_list,
            key=lambda x: datetime.strptime(
                f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"
            ),
        )
        return sorted_appointments

class DentistAppointmentSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Diş Hekimliği Randevu Sistemi")
        self.doctor_system = DentistAppointmentSystem()

        self.name_label = tk.Label(root, text="Hasta Adı:")
        self.name_entry = tk.Entry(root)

        self.date_label = tk.Label(root, text="Tarih: \nYYYY-MM-DD")
        self.date_entry = tk.Entry(root)

        self.time_label = tk.Label(root, text="Saat: \nHH:MM")
        self.time_entry = tk.Entry(root)

        self.doctor_label = tk.Label(root, text="Diş Hekimi Seçimi:")
        self.doctor_var = tk.StringVar()
        self.doctor_var.set("Lütfen Doktor Seçiniz")
        doctor_names = [doctor.name for doctor in self.doctor_system.doctors]
        self.doctor_menu = tk.OptionMenu(root, self.doctor_var, *doctor_names)

        self.type_label = tk.Label(root, text="Randevu Türü:")
        self.type_var = tk.StringVar()
        self.type_var.set("Lütfen Seçim Yapınız")
        self.type_options = []  # Boş bir liste ile başlatıyoruz
        self.type_menu = tk.OptionMenu(root, self.type_var, self.type_options)

        self.schedule_button = tk.Button(
            root, text="Randevu Al", command=self.schedule_appointment
        )
        self.cancel_button = tk.Button(
            root, text="Randevu İptali", command=self.cancel_appointment
        )
        self.display_button = tk.Button(
            root,
            text="Randevu Listesini Görüntüle",
            command=self.display_appointments,
        )

        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10)
        self.date_label.grid(row=1, column=0, padx=10, pady=10)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)
        self.time_label.grid(row=2, column=0, padx=10, pady=10)
        self.time_entry.grid(row=2, column=1, padx=10, pady=10)
        self.doctor_label.grid(row=3, column=0, padx=10, pady=10)
        self.doctor_menu.grid(row=3, column=1, padx=10, pady=10)
        self.type_label.grid(row=4, column=0, padx=10, pady=10)
        self.type_menu.grid(row=4, column=1, padx=10, pady=10)
        self.schedule_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        self.cancel_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        self.display_button.grid(row=7, column=0, columnspan=2, pady=10, padx=80)

        # Doktor seçildiğinde randevu türlerini güncelleyecek event bağlantısı
        self.doctor_menu.bind("<Configure>", self.update_appointment_types)

        # Son seçili doktoru saklamak için değişken
        self.last_selected_doctor = "Lütfen Doktor Seçiniz"
        
    def update_appointment_types(self, event):
        selected_doctor = self.doctor_var.get()
        
        if selected_doctor != self.last_selected_doctor:
            # Eğer doktor değiştiyse randevu tipini default yap
            self.type_var.set("Lütfen Seçim Yapınız")
            self.last_selected_doctor = selected_doctor

        doctor_expertise = self.doctor_system.get_doctor_expertise(selected_doctor)
        self.type_options = ["Lütfen Seçim Yapınız"] + doctor_expertise

        # Type menuyu güncelle
        self.type_menu['menu'].delete(0, 'end')  # Önceki seçenekleri temizle

        for option in self.type_options:
            self.type_menu['menu'].add_command(
                label=option,
                command=lambda value=option: self.type_var.set(value)
            )
            
    def schedule_appointment(self):
        patient_name = self.name_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        appointment_type = self.type_var.get()
        doctor_name = self.doctor_var.get()

        if not patient_name:
            messagebox.showerror(
                "Hata",
                "Hasta adı boş bırakılamaz. \nLütfen geçerli bir hasta adı girin!",
            )
            return
        elif not patient_name.isalpha():
            messagebox.showerror(
                "Hata",
                "Hasta adı sadece içermelidir! \nLütfen geçerli bir hasta adı girin!",
            )
            return

        if doctor_name == "Lütfen Seçim Yapınız":
            messagebox.showerror("Hata", "Lütfen bir doktor seçin!")
            return
        
        try:
            time_format = "%H:%M"
            if ":" not in time or len(time.split(":")) != 2:
                raise ValueError("Geçersiz saat formatı. Saati HH:MM biçiminde girin.")

            hour, minute = map(int, time.split(":"))
            time = f"{hour:02d}:{minute:02d}"
            
        except ValueError as e:
            messagebox.showerror("Hata", str(e))
            return

        try:
            appointment_datetime = datetime.strptime(
                f"{date} {time}", "%Y-%m-%d %H:%M"
            )
        except ValueError:
            messagebox.showerror(
                "Hata",
                "Lütfen geçerli bir tarih ve saat girin (örneğin, '2023-11-26 14:30').",
            )
            return

        if not self.doctor_system.is_valid_appointment_time(time):
            messagebox.showerror(
                "Hata", "Belirtilen saat aralığında randevu alınamaz!"
            )
            return

        if appointment_type == "Lütfen Seçim Yapınız":
            messagebox.showerror(
                "Hata", "Lütfen geçerli bir randevu türü seçin!"
            )
            return
        elif self.doctor_system.schedule_appointment(
            patient_name, date, time, doctor_name, appointment_type
        ):
            messagebox.showinfo("Başarılı", "Randevu başarıyla alındı!")
        else:
            messagebox.showerror(
                "Hata", "Randevu alınamadı. Lütfen uygun bir saat seçin!"
            )

    def cancel_appointment(self):
        date = self.date_entry.get()
        time = self.time_entry.get()
        if self.doctor_system.cancel_appointment(date, time):
            messagebox.showinfo("Başarılı", "Randevu başarıyla iptal edildi!")
        else:
            messagebox.showerror(
                "Hata",
                "Randevu iptal edilemedi! Belirtilen tarihte ve saatte randevu bulunamadı!",
            )

    def display_appointments(self):
        appointments = self.doctor_system.get_appointments()
        if not appointments:
            messagebox.showinfo("Bilgi", "Henüz randevu bulunmamaktadır!")
        else:
            appointment_str = "\n".join(
                [
                    f"Hasta: {appointment['patient_name']} | Muayene Tarihi: {appointment['date']} | Saat: {appointment['time']} | Muayene Türü: {appointment['type']} | Doktor: {appointment['doctor_name']}"
                    for appointment in appointments
                ]
            )

        
        messagebox.showinfo("Randevu Listesi", appointment_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = DentistAppointmentSystemUI(root)
    root.mainloop()
