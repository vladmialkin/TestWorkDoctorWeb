import copy


class Transaction:
    def __init__(self):
        self.values = {}
        self.history = []
        self.history_deleted = []

    def begin(self):
        self.history.append(self.values.copy())
        self.values = {}

    def commit(self):
        if not self.history:
            raise Exception("Нет активной транзакции.")
        if self.history_deleted:
            self.history_deleted.clear()

        for h_values in self.history:
            for key, value in h_values.items():
                if key not in self.values:
                    self.values[key] = value

        self.history.clear()

    def rollback(self):
        if not self.history:
            raise Exception("Нет активной транзакции.")
        if self.history_deleted:
            self.history = self.history_deleted.copy()
            self.history_deleted = []
        self.values = self.history.pop()

    def set_value(self, key, value):
        self.values[key] = int(value)

    def get_value(self, key):
        value = self.values.get(key)
        if value is None:
            for val in self.history[::-1]:
                old_value = val.get(key)
                if old_value is not None:
                    return old_value
            return "NULL"
        return value

    def counts_value(self, value):
        count = 0
        value = int(value)
        if self.history:
            for d in self.history:
                for val in d.values():
                    if value == val:
                        count += 1
        for val in self.values.values():
            if value == val:
                count += 1
        return count

    def find_keys(self, value):
        found_keys = []
        value = int(value)
        if self.history:
            for d in self.history:
                for key, val in d.items():
                    if val == value and key not in found_keys:
                        found_keys.append(key)
        for key, val in self.values.items():
            if val == value and key not in found_keys:
                found_keys.append(key)
        return found_keys

    def unset_value(self, key):
        self.history_deleted = copy.deepcopy(self.history)
        self.values.pop(key, None)
        if self.history:
            for d in self.history:
                d.pop(key, None)


def main():
    transaction = Transaction()
    while True:
        try:
            command = input(
                "Введите команду (BEGIN, COMMIT, ROLLBACK, GET, SET, UNSET, COUNTS, FIND): ").strip().upper()

            if command == 'BEGIN':
                transaction.begin()
            elif command.startswith('SET'):
                _, key, value = command.split()
                transaction.set_value(key, value)
            elif command.startswith('GET'):
                _, key = command.split()
                value = transaction.get_value(key)
                print(value)
            elif command == 'COMMIT':
                transaction.commit()
            elif command == 'ROLLBACK':
                transaction.rollback()
            elif command.startswith('COUNTS'):
                _, value = command.split()
                count = transaction.counts_value(value)
                print(count)
            elif command.startswith('FIND'):
                _, value = command.split()
                keys = transaction.find_keys(value)
                print(" ".join(keys) if keys else "NULL")
            elif command.startswith('UNSET'):
                _, key = command.split()
                transaction.unset_value(key)
            elif command == 'END':
                print("Закрытие приложения.")
                break
            else:
                print("Неверная команда.")
        except EOFError:
            print("Закрытие приложения.")
            break
        except Exception as e:
            print(f"Ошибка: {e}")


if __name__ == '__main__':
    main()
