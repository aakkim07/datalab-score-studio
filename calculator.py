import random
from statistics import mean


FORMULA_LABEL = "y = 2x + 10"


def calculate(value):
    return 2 * value + 10


def transform_values(values):
    return [calculate(value) for value in values]


def generate_values(count=50, rng=None):
    if count < 1:
        raise ValueError("Počet hodnôt musí byť aspoň 1.")
    generator = rng if rng is not None else random
    return [generator.randint(10, 100) for _ in range(count)]


def summarize(values):
    if not values:
        raise ValueError("Pole hodnôt nesmie byť prázdne.")
    return {
        "minimum": min(values),
        "maximum": max(values),
        "average": mean(values),
        "ordered": tuple(sorted(values)),
    }
