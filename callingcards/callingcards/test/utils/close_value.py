import random


def close_value(value: float,
                min_diff:float=0.0001,
                max_diff:float=0.01) -> float:
    """
    Generate a value close to the input value within a specified range.

    Args:
        value (float): The input value to generate a close value for.
        min_diff (float, optional): The minimum difference between the
          input value and the generated value. Defaults to 0.0001.
        max_diff (float, optional): The maximum difference between the
          input value and the generated value. Defaults to 0.01.

    Returns:
        float: A value within the specified range of the input value.
    """
    # Generate a random difference within the range [min_diff, max_diff]
    diff = random.uniform(min_diff, max_diff)

    # Randomly choose the sign of the difference (-1 or 1)
    sign = random.choice([-1, 1])

    # Calculate and return the new value within the specified range of the
    # input value
    return round(value + sign * diff, 5)
