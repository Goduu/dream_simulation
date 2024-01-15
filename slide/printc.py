from enum import Enum
import logging


class MColors(Enum):
    HEADER = ("[95m",)
    OKBLUE = ("[94m",)
    OKCYAN = ("[96m",)
    OKGREEN = ("[92m",)
    WARNING = ("[93m",)
    FAIL = ("[91m",)
    BOLD = ("[1m",)
    UNDERLINE = ("[4m",)
    YELLOW = ("[33m",)


logging.basicConfig(
    filename="./log.txt",
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)


class Emojis(Enum):
    NONE = ""
    FISH = "\U0001F41F"
    FISHING = "\U0001F3A3"
    ICE = "\U00002744"
    MOVE = "\U0001F3C3"
    PENGUIN = "\U0001F427"
    TURN = "\U0001F43E"
    COLLISION = "\U0001F4A5"
    PLUS = "\U00002795"
    MINUS = "\U00002796"
    CARD = "\U0001F3B4"
    START = "\U0001F680"
    WIN = "\U0001F3C6"
    NEW = "\U0001F195"
    ACTION = "\U0001F3AE"
    ERROR = "\U0000274C"


def printc(
    message: str = "",
    color: MColors = MColors.OKBLUE,
    emoji: Emojis = Emojis.NONE,
) -> None:
    # parsed_message = f"{emoji.value} {message}"
    # print(f"\033{color.value[0]}{parsed_message}\033[0m")
    # if color == MColors.FAIL:
    #     logging.error(parsed_message)
    # elif color == MColors.WARNING:
    #     logging.warning(parsed_message)

    # else:
    #     logging.info(message)
    pass


def printlog(message: str, color: MColors = MColors.OKBLUE) -> None:
    print(f"\033{color.value[0]}{message}\033[0m")
    if color == MColors.FAIL:
        logging.error(message)
    elif color == MColors.WARNING:
        logging.warning(message)

    else:
        logging.info(message)
    pass


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
    "win": "\U0001F3C6",
    "new": "\U0001F195",
    "action": "\U0001F3AE",
}
