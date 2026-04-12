from typing import ClassVar


class Console:
    _previous_percentage: ClassVar[int] = -1

    @classmethod
    def progress_bar(cls, message: str, current: int, total: int) -> None:
        percentage = (current + 1) * 100 // total
        if percentage == cls._previous_percentage:
            return

        print(f"\r[{percentage}%] {message}", end="")

        if percentage == 100:
            print()
            cls._previous_percentage = -1
        else:
            cls._previous_percentage = percentage

    @staticmethod
    def ask_integer(message: str):
        while True:
            try:
                return int(input(f"[????] {message}: "))
            except ValueError:
                pass

    @staticmethod
    def question(message: str) -> bool:
        while True:
            answer = input(f"[????] {message} [Y/n] ").lower()
            if not answer:
                return True

            if answer in "ny":
                break

        return bool("ny".index(answer))


if __name__ == "__main__":
    Console.ask_integer("Please, type any integer")

    for i in range(1000):
        Console.progress_bar("Test progress bar", i, 1000)
