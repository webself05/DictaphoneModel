import sys

class Menu:
    def __init__(self, recorder, memory, battery, power):
        self.recorder = recorder
        self.memory = memory
        self.battery = battery
        self.power = power

        self.options =[
            "Показать список записей",
            "Записать новую запись",
            "Воспроизвести запись",
            "Удалить запись",
            "Показать заряд батареи",
            "Выход"
        ]

    def show(self):
        while True:
            print("\n Меню")
            for i, opt in enumerate(self.options, start = 1):
                print(f"{i}.{opt}")
            choice = input("Выберите пункт: ")

            self.power.reset_idle()

            if choice == "1":
                msgs = self.memory.list_messages()
                print("Записи:")
                for m in msgs:
                    print(f"ID {m['id']} - {m['duration']} сек")
            elif choice == "2":
                print(self.recorder.start_recording())
                input("Нажмите Enter чтобы остановить запись...")
                print(self.recorder.stop_recording())
            elif choice == "3":
                while True:
                    msg_id_str = input("Введите ID Записи: ").strip()
                    if msg_id_str.isdigit():
                        msg_id = int(msg_id_str)
                        break
                    print("Ошибка: введите число!")

                msg_id = int(input("Введите ID Записи: "))
                print(self.recorder.start_playback((msg_id)))
            elif choice == "4":
                msg_id = int(input("Введите ID Записи"))
                ok, msg = self.memory.delete_message(msg_id)
                print(msg)
            elif choice == "5":
                print(f"Батарея: {self.battery.level}%")
            elif choice == "6":
                print("Выход")
                self.recorder.stop()
                sys.exit(0)
            else:
                print("Такой команды нет")

