import random
from statistics import median, mean


FORMULAS = {
    "x × 1.25 + 10": lambda value: value * 1.25 + 10,
    "x × 0.80": lambda value: value * 0.8,
    "x + 15": lambda value: value + 15,
}


def generate_values(count=50, rng=None):
    if count < 1:
        raise ValueError("Počet hodnôt musí byť aspoň 1.")
    generator = rng if rng is not None else random
    return [generator.randint(10, 100) for _ in range(count)]


def transform_values(values, formula_name):
    try:
        formula = FORMULAS[formula_name]
    except KeyError as error:
        raise ValueError(f"Neznámy vzorec: {formula_name}") from error
    return [formula(value) for value in values]


def summarize(values):
    if not values:
        raise ValueError("Pole hodnôt nesmie byť prázdne.")
    return {
        "minimum": min(values),
        "maximum": max(values),
        "average": mean(values),
        "median": median(values),
        "ordered": tuple(sorted(values)),
    }
