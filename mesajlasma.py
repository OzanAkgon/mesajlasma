import pypyodbc
import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QTextEdit, QPushButton, \
    QLabel, QLineEdit


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Giriş Ekranı")

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        form_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)

        username_layout = QHBoxLayout()
        form_layout.addLayout(username_layout)

        username_label = QLabel("Kullanıcı Adı:")
        username_layout.addWidget(username_label)

        self.username_input = QLineEdit()
        self.username_input.setFixedWidth(150)
        username_layout.addWidget(self.username_input)

        password_layout = QHBoxLayout()
        form_layout.addLayout(password_layout)

        password_label = QLabel("Şifre:")
        password_layout.addWidget(password_label)

        self.password_input = QLineEdit()
        self.password_input.setFixedWidth(150)
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_input)

        # Giriş ve Üye Ol butonları layout'u
        button_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)

        login_button = QPushButton("Giriş Yap")
        login_button.clicked.connect(self.login)
        button_layout.addWidget(login_button)

        register_button = QPushButton("Üye Ol")
        register_button.clicked.connect(self.register)
        button_layout.addWidget(register_button)




    def login(self):
        # Üye girişi kod alanı



        # Burada sadece mesajlaşma uygulamasını başlatttım
        self.chat_app = ChatApp()
        self.chat_app.show()
        self.close()

    def register(self):
        # Üye olma işlemi için gerekli kod buraya gelecek
        pass


class ChatApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Mesajlaşma Uygulaması")
        self.showFullScreen()  # Tam ekran modunda başlat
        self.setStyleSheet("font-size: 18px;")  # Yazı boyutunu büyüt



        # Ana widget oluştur
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Ana layout oluştur
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Kime gönderileceğini belirtme alanı
        to_layout = QHBoxLayout()
        main_layout.addLayout(to_layout)

        to_label = QLabel("Kime:")
        to_layout.addWidget(to_label)

        self.receiver_input = QLineEdit()
        to_layout.addWidget(self.receiver_input)

        self.kullaniciadi="tikishere"

        # Mesaj gösterme alanı
        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        main_layout.addWidget(self.message_display)

        # Mesaj yazma alanı ve gönderme düğmesi
        input_layout = QHBoxLayout()
        main_layout.addLayout(input_layout)

        self.message_input = QLineEdit()
        input_layout.addWidget(self.message_input)

        send_button = QPushButton("Gönder")
        send_button.clicked.connect(self.send_message)
        input_layout.addWidget(send_button)

#######################################VERİ TABANI İŞLEMLERİ

        server = 'DESKTOP-8LK58RE\SQLEXPRESS'
        database = 'astronaut'

        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database}'

        try:
            # Veritabanına bağlan
            conn = pypyodbc.connect(connection_string)

            cursor = conn.cursor()


            kadi = self.kullaniciadi
            veri2 = (kadi,kadi)
            query = f"SELECT mesaj FROM Mesajlars WHERE kadi = ? OR alici = ?"
            qu = f"SELECT kadi FROM Mesajlars WHERE kadi = ? OR alici = ?"

            cursor.execute(query,veri2)
            mesajlar = cursor.fetchall()

            cursor.execute(qu,veri2)
            kullaniciadlari = cursor.fetchall()
            for kullanici, mesaj in zip(kullaniciadlari, mesajlar):
                self.message_display.append(f"{kullanici[0]} : {mesaj[0]}")



            conn.commit()
            conn.close()



        except Exception as e:
            # Bağlantı hatası durumunda hata mesajını göster
            print("Bağlantı hatası:", e)



################################################Veri tabanı işlemleri

    def send_message(self):
        # Veritabanı bağlantısı
        server = 'DESKTOP-8LK58RE\SQLEXPRESS'
        database = 'astronaut'



        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database}'

        try:
            # Veritabanına bağlan
            conn = pypyodbc.connect(connection_string)

            cursor = conn.cursor()

            kadi = self.kullaniciadi
            alici = self.receiver_input.text()
            mesaj = self.message_input.text()
            veriler = (kadi,alici,mesaj)
            veri2 = (kadi,kadi)
            sql_query = "INSERT INTO Mesajlars (kadi, alici, mesaj) VALUES (?, ?, ?)"
            q = f"SELECT TOP 1 mesaj FROM Mesajlars WHERE kadi = ? OR alici = ? ORDER BY MesajID DESC"

            cursor.execute(sql_query, veriler)
            cursor.execute(q,veri2)

            sonmesaj = cursor.fetchall()
            for mesajss in sonmesaj:
                self.message_display.append(f"{self.kullaniciadi} : {mesajss[0]}")
            if mesaj:
                self.message_input.clear()

            # Bağlantı başarılı olduğunda mesaj göster
            print("Veritabanına başarıyla bağlandı.")
            conn.commit()
            conn.close()



        except Exception as e:
            # Bağlantı hatası durumunda hata mesajını göster
            print("Bağlantı hatası:", e)







if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
