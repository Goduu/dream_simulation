from enum import Enum


class MColors(Enum):
    HEADER = ("[95m",)
    OKBLUE = ("[94m",)
    OKCYAN = ("[96m",)
    OKGREEN = ("[92m",)
    WARNING = ("[93m",)
    FAIL = ("[91m",)
    BOLD = ("[1m",)
    UNDERLINE = ("[4m",)


def printc(message: str, color: MColors = MColors.OKBLUE) -> None:
    print(f"\033{color.value[0]}{message}\033[0m")


emojis = {
    "fish": "\U0001F41F",
    "fishing": "\U0001F3A3",
    "ice": "\U00002744",
    "move": "\U0001F3C3",
    "penguin": "\U0001F427",
    "turn": "\U0001F43E",
    "collision": "\U0001F4A5",
    "plus": "\U00002795",
    "minus": "\U00002796",
    "card": "\U0001F3B4",
    "start": "\U0001F680",
}
