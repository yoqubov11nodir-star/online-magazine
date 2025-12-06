import random
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import qrcode

class Product:
    def __init__(self, name, price, start_year, finish_year, count):
        self.name = name
        self.price = price
        self.start_year = start_year
        self.finish_year = finish_year
        self.count = count

    def __str__(self):
        return f"{self.name} | Price: {self.price} | Count: {self.count}"

class SuperMarket:
    def __init__(self, balance):
        self.balance = balance
        self.products = []

class User:
    def __init__(self, username, password, balance):
        self.username = username
        self.password = password
        self.balance = balance
        self.bag = {}
        self.product_history = []

class Admin:
    def __init__(self, password):
        self.password = password

    def add_product(self, market):
        name = input("Maxsulot nomi: ").capitalize()
        price = int(input("Narxi: "))
        start_year = int(input("Ishlab chiqarilgan tili: "))
        finish_year = int(input("Yaroqlilik muddati: "))
        count = int(input("Miqdori: "))

        product = Product(name, price, start_year, finish_year, count)
        market.products.append(product)
        print("Maxsulot qo'shildi")

    def edit_product(self, market):
        name = input("Tahrirlash uchun maxsulot nomini kiriting: ").capitalize()
        for product in market.products:
            if product.name == name:
                product.name = input("Yangi nomi: ").capitalize()
                product.price = int(input("Yangi narx: "))
                product.count = int(input("Yangi miqdor: "))
                return
        print("Mahsulot topilmadi")

    def delete_product(self, market):
        name = input("O'chirish uchun maxsulot nomi: ").capitalize()
        for product in market.products:
            if product.name == name:
                market.products.remove(product)
                print("O'chirildi")
                return
        print("Maxsulot topilmadi")

    def add_user(self, users):
        username = input("User nomi: ").capitalize()
        password = input("User paroli: ")
        balance = int(input("User Balansi: "))

        new_user = User(username, password, balance)
        users.append(new_user)
        print("User qo'shildi")

# ================= CHeck window =========================

def check_window(order_id, items, total):
    win = tk.Tk()
    win.title("CHECK")
    win.geometry("260x380")
    win.configure(bg="white")

    header = "   SUPER MARKET\n"
    header += "     ----------------\n"
    header += f"Order ID: {order_id}\n"
    header += "-------------------------\n\n"

    body = ""
    for name, amount, price in items:
        body += f"{name}\n  {amount} x {price} = {amount * price}\n"

    footer = f"\nTOTAL: {total} so'm\n"
    footer += "-------------------------\n"

    text = header + body + footer

    label = tk.Label(win, text=text, font=("Arial", 9), bg="white", justify="left")
    label.pack(pady=5)

    qr = qrcode.make(str(order_id))
    qr_path = "qr_check.png"
    qr.save(qr_path)

    qr_img = Image.open(qr_path)
    qr_img = qr_img.resize((130, 130))
    qr_photo = ImageTk.PhotoImage(qr_img)

    qr_label = Label(win, image=qr_photo, bg="white")
    qr_label.image = qr_photo
    qr_label.pack(pady=5)

    win.mainloop()

# ======================= User ===========================

def add_to_cart(user, market):
    print("\nMahsulotlar: ")

    if not market.products:
        print("Maxsulot yo'q")
        return

    for i, product in enumerate(market.products, start=1):
        print(f"{i}. {product.name} | Price: {product.price} | Count: {product.count}")

    try:
        index = int(input("\nMahsulot raqami: ")) - 1
        amount = int(input("Miqdori: "))
    except ValueError:
        print("Faqat raqam kiriting!")
        return

    if index < 0 or index >= len(market.products):
        print("Noto‘g‘ri raqam kiritildi!")
        return

    p = market.products[index]

    if p.count >= amount:
        if p.name in user.bag:
            user.bag[p.name]["amount"] += amount
        else:
            user.bag[p.name] = {"product": p, "amount": amount}

        print("Savatga qo‘shildi!")
    else:
        print("Yetarli miqdor mavjud emas!")

def checkout(user, market):
    if not user.bag:
        print("Savat bo'sh")
        return

    total = 0
    items_for_history = []

    for pname, data in user.bag.items():
        p = data["product"]
        amount = data["amount"]
        total += p.price * amount
        items_for_history.append((p.name, amount, p.price))

    if user.balance < total:
        print("Balance yetarli emas")
        return

    user.balance -= total
    market.balance += total

    for name, data in user.bag.items():
        data["product"].count -= data["amount"]

    order_id = random.randint(10000, 99999)

    user.product_history.append({
        "order_id": order_id,
        "items": items_for_history,
        "total": total
    })

    check_window(order_id, items_for_history, total)

    user.bag.clear()
    print("Harid muvafaqiyatli amalga oshirildi")

def show_history(users):
    print("\n===== Barcha haridlar =====")
    for u in users:
        print(f"\nUsers: {u.username}")
        if u.product_history:
            for p in u.product_history:
                print(f"   Order ID: {p['order_id']}")
                for name, amount, price in p["items"]:
                    print(f"   {name} x {amount} = {amount * price}")
                print(f"   Jami: {p['total']}")
        else:
            print(" --- Hechnarsa xarid qilinmagan")

def show_product(market):
    has_products = False
    for p in market.products:
        if p.count > 0:
            print(p)
            has_products = True
    if not has_products:
        print("Maxsulot yo'q")

def user_menu(user, market):
    while True:
        print(f"\nUser: {user.username} | Balance: {user.balance}")
        print("1. Mahsulotlarni ko'rish")
        print("2. Savatga qo'shish")
        print("3. Savatni ko'rish")
        print("4. Savatni tozalash")
        print("5. Harid qilish")
        print("6. Pul qo'shish")
        print("0. Chiqish")

        kod = input("Tanlang: ")

        if kod == "1":
            show_product(market)

        elif kod == "2":
            add_to_cart(user, market)

        elif kod == "3":
            print("\n--- Savat ---")
            for name, d in user.bag.items():
                print(f"{name} x {d['amount']}")

        elif kod == "4":
            user.bag.clear()

        elif kod == "5":
            checkout(user, market)

        elif kod == "6":
            money = int(input("Kiritmoqchi bo'lgan summangizni kiriting: "))

            if money < 0:
                print("Summa manfiy bo'lishi mumkunmas")
                continue
            else:
                user.balance += money

        elif kod == "0":
            break

def admin_menu(admin, market, users):
    while True:
        print("\n--- ADMIN PANEL ---")
        print("1. Mahsulot qo'shish")
        print("2. Mahsulot tahrirlash")
        print("3. Mahsulot o'chirish")
        print("4. Mahsulotlarni ko‘rish")
        print("5. User qo‘shish")
        print("6. Xaridlar tarixi")
        print("0. Chiqish")

        kod = input("Tanlang: ")

        if kod == "1":
            admin.add_product(market)

        elif kod == "2":
            admin.edit_product(market)

        elif kod == "3":
            admin.delete_product(market)

        elif kod == "4":
            show_product(market)

        elif kod == "5":
            admin.add_user(users)

        elif kod == "6":
            show_history(users)

        elif kod == "0":
            break

def login_system(admin, users, market):
    while True:
        print("\n--- Login ---")
        password = input("Parolni kiriting: ")

        if password == admin.password:
            print("Admin sifatida kirdingiz")
            admin_menu(admin, market, users)
            continue

        for u in users:
            if str(u.password) == password:
                print(f"Xush kelibiz: {u.username}")
                user_menu(u, market)
                break
        else:
            print("Bunday parol topilmadi")
            registration = input("Ro'yhat dan o'tishni hohlaysizmi ha/yo'q\n")

            if registration.lower() == "ha":
                username = input("User nomi: ").capitalize()
                new_password = input("Parol: ")
                balance = int(input("Balance: "))

                new_user = User(username, new_password, balance)
                users.append(new_user)

                print("Ro'yhatdan o'tildi")
            else:
                print("Qayta urinib ko'ring")

def main():
    market = SuperMarket(balance=1000000)
    admin = Admin(password="7777")
    users = []

    market.products.append(Product("Non", 5000, 2023, 2025, 100))

    login_system(admin, users, market)

main()