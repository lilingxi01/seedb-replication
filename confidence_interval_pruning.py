import numpy as np


# Hyperparameters
delta = 0.01


def epsilon_m(m: int, N: int):
    """
    Calculate the epsilon value for the confidence interval pruning method.

    Parameters
    ----------
    m : int
        The number of items in the sample.
    N : int
        The number of items in the population.
    """
    upper_left = 1 - (m - 1) / N
    upper_right = 2 * np.log(np.log(m)) + np.log(np.pi ** 2 / (3 * delta))
    bottom = 2 * m
    return np.sqrt(upper_left * upper_right / bottom)


def confidence_interval_pruning(views: list[np.ndarray], k: int):
    """
    Prune the views based on the confidence interval pruning method.

    Parameters
    ----------
    views : np.ndarray
        Each item is an 1-D numpy array, which represents the utility of each items in a view.
    k : int
        The number of top lower bounds to keep when comparing the upper bounds.
    """

    upper_bounds = []
    lower_bounds = []

    for view in views:
        N = len(view)
        m = N // 2  # For now, we always let m = floor(N/2). This can be changed.
        mu = np.mean(view)
        epsilon = epsilon_m(m, N)
        upper_bound = mu + epsilon
        lower_bound = mu - epsilon
        upper_bounds.append(upper_bound)
        lower_bounds.append(lower_bound)

    # Get the k-th highest lower bounds.
    lower_bounds = np.array(lower_bounds)
    top_k_lower_bound = np.partition(lower_bounds, -k)[-k]

    pruned_flags = np.zeros(len(views), dtype=bool)
    for i, upper_bound in enumerate(upper_bounds):
        if upper_bound < top_k_lower_bound:
            pruned_flags[i] = True

    return pruned_flags
