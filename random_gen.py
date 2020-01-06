from errors import InvalidProbabilitiesError, LengthMismatchError

from typing import List, Tuple

import random


class RandomGen(object):
    # Values that may be returned by next_num()
    _random_nums = []
    # Probability of the occurence of random_nums
    _probabilities = []

    def next_num(self) -> int:
        """
        Returns one of the randomNums. When this method is called
        multiple times over a long period, it should return the
        numbers roughly with the initialized probabilities.
        """
        treshold = random.random()  # Get a random number between 0 and 1

        def binary_search(probas: List[float], treshold: float) -> int:
            """
            Find the smallest cumulative proba that is higher
            than treshold using a binary search algorithm,
            which has O(log n) time complexity.
            """
            left = 0
            right = len(probas)
            while left < right:
                middle = (left + right) // 2
                if treshold < probas[middle]:
                    right = middle
                else:
                    left = middle + 1
            return left

        index = binary_search(self._sorted_cumulative_probas, treshold)

        return self._sorted_random_nums[index]

    def __init__(self) -> None:
        """
        Perfom the feasability checks and compute the cumulative probabilities,
        to be executed once at instanciation to avoid repeating
        the same computations each time next_num is called
        """
        self._check_feasability()

        # Sorting the two lists to use a binary search algorithm later
        sorted_probabilities_to_num = sorted(
            zip(self._probabilities, self._random_nums),
            key=lambda tup: tup[0],
            reverse=True
        )

        (
            self._sorted_cumulative_probas,
            self._sorted_random_nums
        ) = self._compute_cumulative_probas(sorted_probabilities_to_num)

    @staticmethod
    def _compute_cumulative_probas(
        sorted_probabilities_to_num: List[Tuple[float, int]]
    ) -> Tuple[List[float], List[int]]:
        """
        Each num gets its cumulative sum of the probabilities.
        This basically computes the discrete cumulative distribution function.
        """
        sorted_cumulative_probas = [sorted_probabilities_to_num[0][0]]
        sorted_random_nums = [num for _, num in sorted_probabilities_to_num]
        for probability, _ in sorted_probabilities_to_num[1:]:
            sorted_cumulative_probas.append(
                sorted_cumulative_probas[-1] + probability
            )
        return sorted_cumulative_probas, sorted_random_nums

    @classmethod
    def _check_feasability(cls) -> None:
        """
        Perform basic checks on random_nums and probabilities
        to ensure numerical feasability.
        It is defined a class method to indicate that it deals exclusively
        with class attributes, even if a normal method would work as well.
        """
        cls._check_random_nums_length()
        cls._check_probabilities_all_positive()
        cls._check_probabilities_sum_to_one()

    @classmethod
    def _check_random_nums_length(cls) -> None:
        """
        Check that there is exactly one probability per random number.
        """
        if len(cls._random_nums) != len(cls._probabilities):
            raise LengthMismatchError(code=1)

    @classmethod
    def _check_probabilities_all_positive(cls) -> None:
        """
        Check that probabilities are all non negative.
        """

        if any(proba < 0 for proba in cls._probabilities):
            raise InvalidProbabilitiesError(
                "`RandomGen._probabilities` must be non negative.",
                code=2
            )

    @classmethod
    def _check_probabilities_sum_to_one(cls) -> None:
        """
        Check that probabilities sum (approximately) to 1,
        taking into account floating point precision with a small epsilon.
        """
        epsilon = 1e-6
        if abs(sum(cls._probabilities) - 1.) > epsilon:
            raise InvalidProbabilitiesError(
                "`RandomGen._probabilities` should sum to 1.",
                code=3
            )
