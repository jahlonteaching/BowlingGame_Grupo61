from abc import ABC, abstractmethod
from dataclasses import dataclass

from bowlinggame.model.bowling_errors import FramePinsExceededError, ExtraRollWithOpenTenthFrame, \
    TenthFrameWithMoreThanThreeRolls


@dataclass
class Roll:
    pins: int


class Frame(ABC):
    def __init__(self):
        self.rolls: list[Roll] = []
        self.next_frame: Frame | None = None

    @abstractmethod
    def add_roll(self, pins: int):
        raise NotImplementedError

    @abstractmethod
    def score(self) -> int:
        raise NotImplementedError

    @property
    def total_pins(self) -> int:
        return sum(roll.pins for roll in self.rolls)

    def is_spare(self) -> bool:
        return len(self.rolls) == 2 and self.rolls[0].pins + self.rolls[1].pins == 10

    def is_strike(self) -> bool:
        return len(self.rolls) > 0 and self.rolls[0].pins == 10

    def is_complete(self) -> bool:
        return len(self.rolls) == 2

    def __str__(self) -> str:
        if len(self.rolls) == 0:
            return ""
        elif len(self.rolls) == 1:
            if self.is_strike():
                return "X"
            else:
                return f"{self.rolls[0].pins} | "
        elif len(self.rolls) == 2:
            if self.is_spare():
                return f"{self.rolls[0].pins} | /"
            else:
                return f"{self.rolls[0].pins} | {self.rolls[1].pins}"


class NormalFrame(Frame):

    def __init__(self):
        super().__init__()

    def add_roll(self, pins: int):
        if pins + self.total_pins > 10:
            raise FramePinsExceededError("A frame's rolls cannot exceed 10 pins")

        if len(self.rolls) < 2:
            self.rolls.append(Roll(pins))

    def score(self) -> int:
        points = self.total_pins
        if self.is_strike():
            if len(self.next_frame.rolls) == 2:
                points += self.next_frame.total_pins
            elif len(self.next_frame.rolls) == 1:
                points += self.next_frame.rolls[0].pins
                if self.next_frame.next_frame is not None and len(self.next_frame.next_frame.rolls) > 0:
                    points += self.next_frame.next_frame.rolls[0].pins
        elif self.is_spare():
            if len(self.next_frame.rolls) > 0:
                points += self.next_frame.rolls[0].pins

        return points


class TenthFrame(Frame):

    def __init__(self):
        super().__init__()
        self.extra_roll: Roll | None = None

    def add_roll(self, pins: int):
        if len(self.rolls) < 2 and pins + self.total_pins > 20:
            raise FramePinsExceededError("The tenth frame's rolls cannot exceed 20 pins")

        if len(self.rolls) < 2:
            self.rolls.append(Roll(pins))
        elif self.extra_roll is None:
            if self.is_strike() or self.is_spare():
                self.extra_roll = Roll(pins)
            else:
                raise ExtraRollWithOpenTenthFrame("Can't throw bonus roll with an open tenth frame")
        else:
            raise TenthFrameWithMoreThanThreeRolls("Can't add more than three roll to tenth frame")

    def score(self) -> int:
        points = self.total_pins
        if self.extra_roll is not None:
            points += self.extra_roll.pins
        return points


class BowlingGame:

    def __init__(self):
        self.frames: list[Frame] = []
        self.__init_frames()
        self.current_frame_index: int = 0
        self.roll_count: int = 0

    def __init_frames(self):
        frame = NormalFrame()

        for i in range(9):
            if i < 8:
                next_frame = NormalFrame()
            else:
                next_frame = TenthFrame()

            frame.next_frame = next_frame
            self.frames.append(frame)
            frame = next_frame

        self.frames.append(frame)

    def roll(self, pins: int):
        self.roll_count += 1
        self.frames[self.current_frame_index].add_roll(pins)
        if self.current_frame_index < 9:
            if self.frames[self.current_frame_index].is_strike():
                self.current_frame_index += 1
            elif self.frames[self.current_frame_index].is_complete():
                self.current_frame_index += 1

    def score(self) -> int:
        return sum(frame.score() for frame in self.frames)

    def restart(self):
        self.frames.clear()
        self.__init_frames()
        self.current_frame_index = 0
        self.roll_count = 0

    def __len__(self):
        return self.roll_count

