class PowerManager:
    MODE_NORMAL = "normal"
    MODE_SAVE = "power_save"

    def __init__(self, battery):
        self.battery = battery
        self.mode = self.MODE_NORMAL
        self.idle_seconds = 0

    def update_idle(self,seconds):
        self.idle_seconds += seconds
        if self.idle_seconds >= 30:
            self.enter_save_mode()

    def reset_idle(self):
        self.idle_seconds = 0

    def enter_save_mode(self):
        self.mode = self.MODE_SAVE

    def exit_save_mode(self):
        if not self.battery.is_low():
            self.mode = self.MODE_NORMAL
            self.reset_idle()

    def is_save_mode(self):
        return self.mode == self.MODE_SAVE