class MemoryStorage:
    MAX_MESSAGES = 10

    def __init__(self):
        self.messages = []

    def add_message(self,duration,content):
        if len(self.messages) >= self.MAX_MESSAGES:
            return False, "Память заполнена"

        msg_id=len(self.messages) + 1
        self.messages.append({
            "id":msg_id,
            "duration":duration,
            "content":content
        })
        return True, f"Запись{msg_id} сохранена"

    def delete_message(self, msg_id):
        for m in self.messages:
            if m["id"] == msg_id:
                self.messages.remove(m)
                return True, f"Запись{msg_id} удалена"
        return False, "Запись не найдена"

    def get_message(self,msg_id):
        for m in self.messages:
            if m["id"] == msg_id:
                return m
            return None

    def list_messages(self):
        return self.messages