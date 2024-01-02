#   Olcay ALKAN 
#   Aciklama: LinkedList ve Sözluk yapisi kullanilarak Disciler icin bir randevu sistemi tasarlandi. 

import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk

# Node sinif tanimlanir
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# LL sinifi tanimlanmasi
class LinkedList:
    def __init__(self):
        self.head = None

    # Yeni bir randevu eklemek icin kullanilan fonksiyon
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next: 
            last_node = last_node.next
        last_node.next = new_node
    # Randevulari tarih ve saat sirasina gore siralayarak donduren fonksiyon
    def get_appointments(self):
        appointments_list = []
        current_node = self.head

        # Node oldugu surece her node verisi listeye eklenir, sonraki node'a gecilir
        while current_node:
            appointments_list.append(current_node.data)
            current_node = current_node.next

        # Zamana gore siralanmis hali liste  gonderilir
        sorted_appointments = sorted(
            appointments_list,
            key=lambda x: datetime.strptime(
                f"{x['date']} {x['time']}", "%Y-%m-%d %H:%M"
            ),
        )
        return sorted_appointments

# Doktor sinifinin tanimlanmasi
class Doctor:
    def __init__(self, name, expertise):
        self.name = name
        self.expertise = expertise
        self.appointments = LinkedList()

class DentistAppointmentSystem:
    def __init__(self):
        # Doktorlar ve uzmanliklarinin olusturulmasi
        self.doctors = [
            Doctor("Lutfen Doktor Seciniz", []),
            Doctor("Dr. Ayse", ["Dis Muayene", "Temel Dis Bakimi", "Dolgu Muayenesi"]),
            Doctor("Doc.Dr.İlos", ["Cocuk Dis Hekimligi","Temel Dis Bakimi"]),
            Doctor("Dr. Mehmet", ["Dis cekimi", "Kanal Tedavisi", "Dis Protezi"]),
            Doctor("Prof.Dr.Seyfullah", ["Dis Beyazlatma","Protetik Dis Tedavisi","Restoratif Dis Tedavisi","Genel Dis Hekimligi"])
        ]

    # Doktor nesnesini getiren fonksiyon
    def get_doctor_name(self, doctor_name):
        for doctor in self.doctors:
            if doctor.name == doctor_name:
                return doctor
        return None

    # Verilen doktor'a gore uzmanliklarini getiren fonksiyon
    def get_doctor_expertise(self, doctor_name):
        doctor = self.get_doctor_name(doctor_name)
        return doctor.expertise if doctor else []

    # Uygun saat araligini kontrol eder
    def is_valid_appointment_time(self, time):
        start_morning_time = datetime.strptime("09:00", "%H:%M")
        end_morning_time = datetime.strptime("11:20", "%H:%M")
        start_afternoon_time = datetime.strptime("13:00", "%H:%M")
        end_afternoon_time = datetime.strptime("16:50", "%H:%M")

        # Input olarak alinan zaman  datetime nesnesine donusturulur.
        appointment_time = datetime.strptime(time, "%H:%M")

        # 09:00 - 11:20  ve  13:00 - 16:50 arasindaki saat araliklarina randevu alinabilir oldugunu kontrol eder.  | Son randevular 11:30'a ve 17:00'a kadar surmesi icin 11:20 ve 16:50 secilmistir.
        if (
            (start_morning_time <= appointment_time <= end_morning_time)
            or (start_afternoon_time <= appointment_time <= end_afternoon_time)
        ):
            return True
        else:
            return False

    # Randevu alma islemi icin kullanilan fonksiyon
    def schedule_appointment(self, patient_name, date, time, doctor_name, appointment_type):
        # Doktor bilgisi alinir
        doctor = self.get_doctor_name(doctor_name)
        # Doktor bilgisi yoksa veya randevu saati uygun degilse False doner 
        if not doctor or not self.is_valid_appointment_time(time):
            return False

        # Yeni randevu icin datetime nesnesi olusturulur
        new_appointment_time = datetime.strptime(
            f"{date} {time}", "%Y-%m-%d %H:%M"
        )
        # Ayni doktor'un mevcut randevularina bakilir.
        for existing_appointment in doctor.appointments.get_appointments():
            existing_appointment_time = datetime.strptime(
                f"{existing_appointment['date']} {existing_appointment['time']}",
                "%Y-%m-%d %H:%M",
            )
            # Eger mevcut randevu yeni randevuyla cakisiyorsa +- 10 dakika (Ornek 10:00 alinmis mevcut randevu varsa 09:51 - 10:09 arasina randevu alinmasi engellenir. 09:50 ve 10:10'a alinabilir)
            if (
                new_appointment_time > existing_appointment_time - timedelta(minutes=10)
                and new_appointment_time < existing_appointment_time + timedelta(minutes=10)
            ):
                return False
        
        # Mevcut randevular arasinda 10 dakika icinde baska bir randevu var mi yok mu o arastirilir (cakisma kontrolu)
        other_appointment_time = datetime.now() + timedelta(minutes=10)
        for existing_appointment in doctor.appointments.get_appointments():
            existing_appointment_time = datetime.strptime(
                f"{existing_appointment['date']} {existing_appointment['time']}",
                "%Y-%m-%d %H:%M",
            )

            if (
                existing_appointment_time > datetime.now()
                and existing_appointment_time <= other_appointment_time
            ):
                return False

        # Randevu bilgileri iceren bir sozluk yapisi olusturulur
        new_data = {
            "patient_name": patient_name,
            "date": date,
            "time": time,
            "type": appointment_type,
        }

        # Bu sozluk yapisi Doktor ustundeki Linked list icine aktarilir
        doctor.appointments.append(new_data)
        return True
    
    # Randevu iptali
    def cancel_appointment(self, date, time, doctor_name):
        # Doktor nesnesine ulasilir
        doctor = self.get_doctor_name(doctor_name)
        if not doctor:
            return False

        # Doktor'un randevulari arasinda gezinilir
        current_node = doctor.appointments.head
        prev_node = None

        # Eger randevu bulunursa iptal edilir
        while current_node:
            # Iptal edilmek istenen tarih ve saat eslesiyorsa
            if (
                current_node.data["date"] == date
                and current_node.data["time"] == time
            ):
                # Eger randevu iptal edilecekse
                if prev_node:
                    # Bir önceki node ile bir sonraki node birbirine baglanir 
                    prev_node.next = current_node.next
                else:
                    # İlk node iptal edilmek istenen randevunun ardindaki node ile degisir
                    doctor.appointments.head = current_node.next
                return True
            # Mevcut node bir onceki node olur
            prev_node = current_node
            # Bir sonraki node su anki node olur
            current_node = current_node.next

        return False
    # Doktor ismine gore randevulari getirir
    def get_appointments(self, doctor_name):
        doctor = self.get_doctor_name(doctor_name)
        # Doktorun randevulari olmamasi durumunda bos bir liste dondurur
        return doctor.appointments.get_appointments() if doctor else []

class DentistAppointmentSystemUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Dis Hekimligi Randevu Sistemi")
        self.doctor_system = DentistAppointmentSystem()

        # Pencere boyutu
        root.geometry("750x450")

        # Pencere arkaplan resmi
        image_path = "background.png"
        self.background_image = Image.open(image_path)                      # Arka plan resmini ayarla
        
        # Arkaplan fotografinin yeniden boyutlandirir
        resized_image = self.background_image.resize((750,450))
        self.background_photo = ImageTk.PhotoImage(resized_image)           # GUI'a resim eklenmesi icin kullanilir
        self.background_label = tk.Label(root, image=self.background_photo) # Arka plani yerlestirmek icin etiketlenir arka plan fotografi 
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)      # GUI'in 0 , 0 noktasindan baslayarak arka plan yerslestirilir 1-1 oranla frame buyutuldukce arka planin sabit kalmasi saglanir

        # Pencerenin opakligini ayarlama
        root.attributes("-alpha", 0.90)  # Opaklik Seviyesi 1.0 - 0.0
        
        self.name_label = tk.Label(root, text="Hasta Adi:", bg="#f1f1f1")           # Hasta adi GUI
        self.name_entry = tk.Entry(root)

        self.date_label = tk.Label(root, text="Tarih: \nYYYY-MM-DD", bg="#f1f1f1")  # Tarih GUI
        self.date_entry = tk.Entry(root)

        self.time_label = tk.Label(root, text="Saat: \nHH:MM", bg="#f1f1f1")        # Saat GUI
        self.time_entry = tk.Entry(root)

        self.doctor_label = tk.Label(root, text="Dis Hekimi Secimi:", bg="#f1f1f1") # Dis Hekimi GUI
        self.doctor_var = tk.StringVar()                                            # Secilen degeri tutar GUI
        self.doctor_var.set("Lutfen Doktor Seciniz")                                # İlk GUI'da bu ifade secili olsun
        doctor_names = [doctor.name for doctor in self.doctor_system.doctors]
        self.doctor_menu = tk.OptionMenu(root, self.doctor_var, *doctor_names)      # *doctor_names kullanilmasinin sebebi listedeki randevu tiplerini randevu seceneklerine teker teker ayirmak

        self.type_label = tk.Label(root, text="Randevu Turu:", bg="#f1f1f1")
        self.type_var = tk.StringVar()
        self.type_var.set("Lutfen Secim Yapiniz")                               # Randevu turunu default olarak "Lutfen Secim Yapiniz" yapiyoruz
        self.type_options = []                                                  # Bos bir liste ile baslatiyoruz
        self.type_menu = tk.OptionMenu(root, self.type_var, self.type_options)  # Secimler Doktora göre degisiklik göstericek  

        self.schedule_button = tk.Button(                                       # Randevu alma butonu
            root, text="Randevu Al", command=self.schedule_appointment
        )
        self.cancel_button = tk.Button(                                         # Randevu iptal etme butonu
            root, text="Randevu İptali", command=self.cancel_appointment
        )
        self.display_button = tk.Button(                                        # Randevulari gosterme butonu
            root,
            text="Randevu Listesini Göruntule",
            command=self.display_appointments,
        )

        # Pencereye yerlestirme (Widgetlar) Satir / Sutun /x kaydirma / y kaydirma 
        self.name_label.grid(row=0, column=0, padx=(30,10), pady=(40,10))       # Gui'a yazdirilan orn: Hasta Adi:
        self.name_entry.grid(row=0, column=1, padx=(30,10), pady=(40,10))       # Input yeri "Hasta Adi:" karsisindaki doldurma yer 
        self.date_label.grid(row=1, column=0, padx=(30,10), pady=10)
        self.date_entry.grid(row=1, column=1, padx=(30,10), pady=10)
        self.time_label.grid(row=2, column=0, padx=(30,10), pady=10)
        self.time_entry.grid(row=2, column=1, padx=(30,10), pady=10)
        self.doctor_label.grid(row=3, column=0, padx=(30,10), pady=10)
        self.doctor_menu.grid(row=3, column=1, padx=(30,10), pady=10)
        self.type_label.grid(row=4, column=0, padx=(30,10), pady=10)
        self.type_menu.grid(row=4, column=1, padx=(30,10), pady=10)
        # Pencereye yerlestirme (Widgetlar) Satir / Sutun /kac sutunluk yere sahip olmali /x kaydirma /y kaydirma /x yonunde sol sag kenarlarin icerik ile arasinda kaplicagi alan / y ekseninde asagi yukari kenarlarin icerik ile arasinda kaplayacagi alan
        self.schedule_button.grid(row=5, column=0, columnspan=2, padx=(30,10), pady=10, ipadx=115, ipady=0)
        self.cancel_button.grid(row=6, column=0, columnspan=2, padx=(30,10), pady=10, ipadx=110, ipady=0)
        self.display_button.grid(row=7, column=0, columnspan=2, padx=(30,10), pady=10, ipadx=75, ipady=0)

        # Doktor secildiginde randevu turlerini guncelleyecek event baglantisi
        self.doctor_menu.bind("<Configure>", self.update_appointment_types)

        # Son secili doktoru saklamak icin degisken
        self.last_selected_doctor = "Lutfen Doktor Seciniz"
    
    # Randevu turlerini guncelleme
    def update_appointment_types(self, event):
        # Secili olan doktoru sakla
        selected_doctor = self.doctor_var.get()
        
        # Eger doktor degistiyse randevu tipini default deger yap
        if selected_doctor != self.last_selected_doctor:
            self.type_var.set("Lutfen Secim Yapiniz")
            self.last_selected_doctor = selected_doctor

        # Doktor'un uzmanliklarini cagir
        doctor_expertise = self.doctor_system.get_doctor_expertise(selected_doctor)
        # Lutfen secim yapiniz tipi + doktor uzmanliklarini seceneklere ekle
        self.type_options = ["Lutfen Secim Yapiniz"] + doctor_expertise

        # Type menuyu guncelle
        self.type_menu['menu'].delete(0, 'end')  # Önceki secenekleri temizle

        # Secenekler option'a eklenir ve secilen randevu tipine gore bir self_type.var yani gui'a atanir
        for option in self.type_options:
            self.type_menu['menu'].add_command(
                label=option,
                command=lambda value=option: self.type_var.set(value)
            )

    def schedule_appointment(self):
        # Gerekli bilgilerin atanmasi
        patient_name = self.name_entry.get()
        date = self.date_entry.get()
        time = self.time_entry.get()
        appointment_type = self.type_var.get()
        doctor_name = self.doctor_var.get()

        # Hasta adi bos birakilirsa 
        if not patient_name:
            messagebox.showerror(
                "Hata",
                "Hasta adi bos birakilamaz! \nLutfen gecerli bir hasta adi girin.",
            )
            return
        elif not patient_name.isalpha():
            messagebox.showerror(
                "Hata",
                "Hasta adi sadece icermelidir! \nLutfen gecerli bir hasta adi girin.",
            )
            return
        
        # Hasta adi 100 karakterden fazla olursa
        if len(patient_name) > 100:
            messagebox.showerror(
                "Hata",
                "Hasta adi 100 karakterden uzun olamaz! \nLutfen gecerli bir hasta adi girin.",
            )
            return

        # Doktor secimi yapilmadiysa
        if doctor_name == "Lutfen Secim Yapiniz":
            messagebox.showerror("Hata", "Lutfen bir doktor secin!")
            return

        # Saat eksik girilirse / hatali girilirse
        try:    # 10    :   30
            time_format = "%H:%M"
            if ":" not in time or len(time.split(":")) != 2:
                raise ValueError("Gecersiz saat formati! \nSaati HH:MM biciminde girin.")
            # 10     30    şeklinde int olarak bol ve zamana eşitle
            hour, minute = map(int, time.split(":"))
            time = f"{hour:02d}:{minute:02d}"

        except ValueError as e:
            # raise'lanan hata gosterilir
            messagebox.showerror("Hata", str(e))
            return

        # Tarih eksik girilirse / hatali girilirse
        try:
            appointment_datetime = datetime.strptime(
                f"{date} {time}", "%Y-%m-%d %H:%M"
            )
        except ValueError:
            messagebox.showerror(
                "Hata",
                "Lutfen gecerli bir tarih ve saat girin! \n(Ornegin, '2023-11-26 14:30').",
            )
            return
        
        # Randevu alinabilir saatlerin disinda bir zaman girilirse
        if not self.doctor_system.is_valid_appointment_time(time):
            messagebox.showerror(
                "Hata", "Belirtilen saat araliginda randevu alinamaz!"
            )
            return
        
        # Bugunun tarihinde bir randevu alinacasak saatleri karsilastirilir
        today = datetime.now()
        if (
            appointment_datetime.date() == today.date()
                                and 
            appointment_datetime.time() < today.time()
            ):
            messagebox.showerror(
                "Hata",
                "Gecmiş bir saat icin randevu alinamaz! \nLutfen ileri bir tarih ve saat girin.",
                )
            return
        
        # Gecmis bir tarihe randevu alinamaz
        today = datetime.now()
        if appointment_datetime < today:
            messagebox.showerror(
                "Hata",
                "Girilen tarih gecmis bir tarih olamaz!"
            )
            return

        # Randevu tipi secilmediyse
        if appointment_type == "Lutfen Secim Yapiniz":
            messagebox.showerror(
                "Hata", "Lutfen gecerli bir randevu turu secin!"
            )
            return
        # Randevu alinabilir
        elif self.doctor_system.schedule_appointment(
            patient_name, date, time, doctor_name, appointment_type
        ):
            messagebox.showinfo("Basarili", "Randevu basariyla alindi!")
        else:
        # Randevu alinamadi            
            messagebox.showerror(
                "Hata", "Randevu alinamadi! \nLutfen uygun bir saat secin."
            )

    # Randevu Iptali
    def cancel_appointment(self):
        date = self.date_entry.get()
        time = self.time_entry.get()
        doctor_name = self.doctor_var.get()
        if self.doctor_system.cancel_appointment(date, time, doctor_name):
            messagebox.showinfo("Basarili", "Randevu basariyla iptal edildi!")
        else:
            messagebox.showerror(
                "Hata",
                "Randevu iptal edilemedi! \nBelirtilen tarihte ve saatte randevu bulunamadi.",
            )

    # Randevu Gosterme
    def display_appointments(self):
        doctor_name = self.doctor_var.get()
        appointments = self.doctor_system.get_appointments(doctor_name)
        # Randevu yoksa bilgi mesaj kutusu yolla
        if not appointments:
            messagebox.showinfo("Bilgi", "Henuz randevu bulunmamaktadir!")
        else:
            # Sirayla ekle Hasta: ... | Muayne Tarihi: ... | Saat: ... | Doktor: ... | Muayne Turu: ... |
            appointment_str = "\n".join(
                [
                    f"Hasta: {appointment['patient_name']} | Muayene Tarihi: {appointment['date']} | Saat: {appointment['time']} | Doktor: {doctor_name} | Muayene Turu: {appointment['type']}"
                    for appointment in appointments
                ]
            )
            # Listeyi Goster
            messagebox.showinfo("Randevu Listesi", appointment_str)

if __name__ == "__main__":
    root = tk.Tk()                          # Tkinter penceresi oluşturur
    app = DentistAppointmentSystemUI(root)  # GUI'nin olusturulmasi ve Tkinter'a erisimi saglar
    root.mainloop()                         # Pencere kapatilana kadar calismasini saglar
