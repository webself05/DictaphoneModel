from storage import MemoryStorage
from battery import Battery
from power_manager import PowerManager
from recorder import Recorder
from menu import Menu

def main():
    memory = MemoryStorage()
    battery = Battery(level=100)
    power = PowerManager(battery)
    recorder = Recorder(memory,battery,power)
    menu = Menu(recorder,memory,battery,power)

    menu.show()

if __name__ == "__main__":
    main()