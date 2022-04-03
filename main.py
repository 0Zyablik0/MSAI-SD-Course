class User:
    def __init__(self, user_id: int, user_login: str, password: str):
        self.id = user_id
        self.chats = set()
        self.messages = set()
        self.friends = []
        self.login = user_login
        self.password_hash = hash(password)
        self.phone = ''

    def add_message(self, message_id: int) -> None:
        self.messages.add(message_id)

    def add_chat(self, chat_id: int) -> None:
        self.chats.add(chat_id)

    def set_phone(self, phone: str):
        self.phone = phone

    def get_phone(self) -> str:
        return self.phone

    def __str__(self):
        return f"User {self.login} with {len(self.chats)} chats and {len(self.messages)} messages"


class Message:
    def __init__(self, message_id: int, from_id: int, to_id: int, chat_id: int, date: str, text: str):
        self.id = message_id
        self.chat_id = chat_id
        self.sender_id = from_id
        self.receiver_id = to_id
        self.text = text
        self.date = date

    def find_pattern(self, pattern: str) -> int:
        return self.text.find(pattern)


class Chat:
    def __init__(self, chat_id: int):
        self.id = chat_id
        self.messages = []
        self.users = set()

    def add_user(self, user_id: int) -> int:
        self.users.add(user_id)
        return len(self.users)

    def add_message(self, message_id: int) -> None:
        self.messages.append(message_id)

    def __str__(self):
        return f"Chat #{self.id} with {len(self.users)} users and {len(self.messages)} messages"


class Messenger:
    def __init__(self):
        self.users = []
        self.chats = []
        self.messages = []

    def __str__(self):
        return f"Messanger  with {len(self.users)} users, {len(self.chats)} chats " \
               f"and  {len(self.messages)} messages"

    def create_chat(self, chat_id: int) -> None:
        if chat_id in self.chats:
            raise RuntimeError("Char already exists")
        self.chats[chat_id] = Chat(chat_id)

    def create_user(self, login: str, password: str) -> None:
        user_id = len(self.users)
        self.users.append(User(user_id, login, password))

    def add_user_to_chat(self, chat_id: int, user_id: int) -> None:
        if user_id not in self.users:
            raise RuntimeError("Wrong user id")
        if chat_id not in self.chats:
            raise RuntimeError("Wrong chat id")
        self.chats[chat_id].add_user(user_id)

    def write_message(self, from_: int, to_: int, chat_id: int, date: str, text: str) -> None:
        if from_ not in self.users:
            raise RuntimeError("Wrong receiver id")

        if to_ not in self.users:
            raise RuntimeError("Wrong sender id")

        if chat_id not in self.chats:
            raise RuntimeError("Wrong chat id")

        message_id = len(self.messages)
        self.chats[chat_id].add_message(message_id)
        message = Message(message_id, from_, to_, chat_id, date, text)
        self.messages.append(message)

    def find_pattern(self, pattern: str) -> list[Message]:
        return [message for message in self.messages if message.find_pattern(pattern) != -1]

    def shared_chats(self, users):
        result = set(self.chats)
        for user in users:
            result.intersection(user.chats)
        return result

    def score(self) -> float:
        return len(self.users) * 0.6 + len(self.messages) * 0.3 + len(self.chats) * 0.1

    def __lt__(self, other) -> bool:
        return self.score() < other.score()

    def __le__(self, other) -> bool:
        return self.score() <= other.score()

    def __eq__(self, other) -> bool:
        return self.score() == other.score()

    def __sub__(self, other) -> set[str]:
        left_set = set(user.get_phone for user in self.users)
        right_set = set(user.get_phone for user in other.users)
        return left_set - right_set

    def __or__(self, other) -> set[str]:
        left_set = set(user.get_phone for user in self.users)
        right_set = set(user.get_phone for user in other.users)
        return left_set | right_set

    def __and__(self, other) -> set[str]:
        left_set = set(user.get_phone for user in self.users)
        right_set = set(user.get_phone for user in other.users)
        return left_set & right_set


msg1 = Messenger()
msg2 = Messenger()
print(msg1 > msg2)
