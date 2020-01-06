## MAN Pre-interview test

### Algorithms

Implement the method `nextNum()` and a minimal but effective set of unit tests. Implement in the language of your choice, Python is preferred, but Java and other languages are completely fine. Make sure your code is exemplary, as if it was going to be shipped as part of a production system.

As a quick check, given Random Numbers are `[-1, 0, 1, 2, 3]` and Probabilities are `[0.01, 0.3, 0.58, 0.1, 0.01]` if we call `nextNum()` 100 times we may get the following results. As the results are random, these particular results are unlikely.

-1: 1 times
0: 22 times
1: 57 times
2: 20 times
3: 0 times

#### Languages
##### Python
You may use `random.random()` which returns a pseudo random number between 0 and 1.

```python
import random


class RandomGen(object):
    # Values that may be returned by next_num()
    _random_nums = []
    # Probability of the occurence of random_nums
    _probabilities = []

    def next_num(self):
        """
        Returns one of the randomNums. When this method is called
        multiple times over a long period, it should return the
        numbers roughly with the initialized probabilities.
        """
        pass
```

See `random_gen.py` for implementation, and `test_random_gen.py` for unit tests (Python >= 3.6).

##### Please describe how you might implement this more "pythonically"

Assuming I have to keep the same OO template, I would first pass `random_nums` and `probabilities` as arguments to the `__init__` method. And checking these arguments would be more coherent than testing class attributes at initialization.

Having them as class attributes is just bad style, because we can assume that we may want to have different `RandomGen` objects for different sets of `probabilities` and `random_nums`, and class attributes are generally constants across all instances. What is even more dangerous is that these class attributes are mutable (being Python's lists), so we cannot even change the values for just one instance:

```python
>>> RandomGen._probabilities = [0.1, 0.9]
>>> RandomGen._random_values = [1, 10]

>>> random_gen_1 = RandomGen()
>>> random_gen_2 = RandomGen()

>>> random_gen_1._probabilities[0], random_gen_1._probabilities[-1] = (
        random_gen_1._probabilities[-1],
        random_gen._probabilities[0]
    )  # swap values

>>> print(random_gen_2._probabilities)
[0.9, 0.1]

```


Moreover, it is a convention that if an attribute starts with and underscore, it is semi-private in Python and should not be accessed outside the class. So, to be absolutely clean, I should have defined a setter just to avoid accessing these attributes in `test_random_gen.py`.

If I could use external libraries, I would just go for numpy's [random.choice](https://docs.scipy.org/doc/numpy-1.16.0/reference/generated/numpy.random.choice.html):

```python
import numpy as np

def get_num(random_nums, probabilities):
    return np.random.choice(random_nums, p=probabilities)

```