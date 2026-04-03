import qrcode
import time

qr_list = []

def animation(text,x,delay):
    print(text, end="", flush=True) 
    for _ in range(x):      
        time.sleep(delay)     
        print(".", end="", flush=True) 
        time.sleep(0.1)
    print()

def qr_builder():
    color_list = ("black","green","yellow","blue","red")
    running = True 
    while running:
        qr_link = input("Введите ссылку или текст, который нужно зашифровать: ")
        filename = input("Введите название для сохранения файла (без .png): ")
        while True:
            color = input("Выберите цвет кода (black, green, yellow, blue, red): ")
            if color in color_list:
                break
            else:
                print("Ошибка: данного цвета нет в списке доступных.")

        qr_code = {
            "link": qr_link,
            "filename": filename,
            "color": color,
        }

        qr_list.append(qr_code)
        print(f"Объект успешно добавлен в очередь: {qr_code}")

        while True:
            print("-" * 15)
            again = input("Добавить еще один QR-код в список? (y/n): ").lower()
            print("-" * 15)
            if again == 'n':
                print("Сбор данных окончен, переходим к генерации.")
                print("-" * 15)
                running = False
                break
            elif again == "y":
                break 
            else:
                print("Пожалуйста, используйте только символы 'y' (да) или 'n' (нет)")

qr_builder()      

for item in qr_list:
    animation(f"Процесс создания файла {item['filename']}",3,0.25)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(item["link"])
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=item["color"], back_color="white")
    img.save(item["filename"] + ".png")
    print(f"Файл '{item['filename']}.png' успешно сохранен в папку с проектом.")