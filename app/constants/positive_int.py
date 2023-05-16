from pydantic import ConstrainedInt


class PositiveInt(ConstrainedInt):
    gt = 0
