import sys, os
import math
import random
import typing
import arcade
sys.path.append(os.getcwd() + r"\Project-Aries")
from characters.enemy import Enemy

class SpaceShip(Enemy):

    def __init__(self) -> None:
        """Initialize the class"""