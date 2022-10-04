class HexCoordinates:

    def __init__(self, q: int, r: int, s: int) -> None:
        self.q = q
        self.r = r
        self.s = s

    def __repr__(self):
        return f"<HexCoordinates q:{self.q} r:{self.r} s:{self.s}>"

    def __eq__(self, other):
        if isinstance(other, HexCoordinates):
            return self.q == other.q and \
                self.r == other.r and \
                self.s == other.s
        return NotImplemented

    def __sub__(self, other):
        return HexCoordinates(self.q - other.q, self.r - other.r,
                              self.s - other.s)

    def __add__(self, other):
        return HexCoordinates(self.q + other.q, self.r + other.r,
                              self.s + other.s)
