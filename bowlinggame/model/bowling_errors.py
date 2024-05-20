class BowlingError(Exception):
    pass


class FramePinsExceededError(BowlingError):
    pass


class ExtraRollWithOpenTenthFrame(BowlingError):
    pass


class TenthFrameWithMoreThanThreeRolls(BowlingError):
    pass