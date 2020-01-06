from errors import (
    InvalidProbabilitiesError,
    LengthMismatchError,
    ValidationError
)
from random_gen import RandomGen

from collections import Counter
from typing import List

import random
import unittest


class TestRandomGenNextNum(unittest.TestCase):

    def test_returned_num_in_random_nums(self):
        """
        Test that `next_num` returns a number in `_random_nums`.
        """
        self._setup_random_gen([1.], [42])
        self.assertEqual(self._random_gen.next_num(), 42)

    def test_repeated_simuations_with_fixed_seed(self):
        """
        Test that `next_num` returns the correct sequence of numbers.
        To avoid a flaky test, we make the `random.random`
        function deterministic by fixing the seed of the RNG.
        """
        random.seed(175203)
        expected_results = {-1: 5, 0: 36, 1: 43, 2: 16}
        self._setup_random_gen([0.01, 0.3, 0.58, 0.1, 0.01], [-1, 0, 1, 2, 3])

        simulation_results = Counter()
        for _ in range(100):
            simulation_results[self._random_gen.next_num()] += 1

        self.assertDictEqual(simulation_results, expected_results)

    def test_error_when_length_mismatch(self):
        """
        Test that a `LengthMismatchError` is raised
        when lengths of probabilities and random_nums differ.
        """
        self._assert_raise_error(
            probabilities=[0.5, 0.5],
            random_nums=[0],
            error=LengthMismatchError,
            code=1
        )

    def test_error_when_probabilities_negative(self):
        """
        Test that an `InvalidProbabilitiesError` is raised
        when there is at least one negative probability.
        """
        self._assert_raise_error(
            probabilities=[0.5, 0.6, -0.1],
            random_nums=[0, 0, 0],
            error=InvalidProbabilitiesError,
            code=2
        )

    def test_error_when_probabilities_does_not_sum_to_one(self):
        """
        Test that an `InvalidProbabilitiesError` is raised
        when the probabilities do not sum approximately to 1.
        """
        self._assert_raise_error(
            probabilities=[0.5, 0.4],
            random_nums=[0, 0],
            error=InvalidProbabilitiesError,
            code=3
        )

    def _setup_random_gen(
        self,
        probabilities: List[float],
        random_nums: List[int]
    ) -> None:
        """
        Setup a RandomGen object to be tested.
        """
        RandomGen._probabilities = probabilities
        RandomGen._random_nums = random_nums
        self._random_gen = RandomGen()

    def _assert_raise_error(
        self,
        probabilities: List[float],
        random_nums: List[int],
        error: ValidationError,
        code: int
    ) -> None:
        """
        Check that a specified error is raised when instanciating `RandomGen`
        with specified probabilities and random_nums
        """
        with self.assertRaises(error) as context:
            self._setup_random_gen(probabilities, random_nums)
            self.assertEqual(context.exception.code, code)
