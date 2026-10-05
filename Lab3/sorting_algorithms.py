""" 
ENGR 221 Lab 3 - Sorting Algorithms
Author: Huiwon Choi
This file contains implementations of s0election sort, insertion sort, and bubble sort.
"""

import random
import time

from preferences import Preferences


class SortingAlgorithms:
    def __init__(self):
        # the algorithm to sort
        self.array = []

        # any indices to highlight
        self.inner_idx = -1
        self.outer_idx = -1

        # a string representing the current sorting algorithm
        self.current_alg = None

        # store the method of the sorting algorithm being run
        self.alg_method = None

    def create_new_array(self, length=Preferences.NUM_ELEMENTS) -> list:
        """Create a new array to sort."""
        return [random.randint(0, Preferences.MAX_VAL)
                for _ in range(length)]

    def get_next_step(self) -> None:
        """Updates the selected indices whenever we reach a yield statement."""

        try:
            # treats the current sorting algorithm as an iterator
            # and gets the next pair of indices
            self.outer_idx, self.inner_idx = next(self.alg_method)

        # clear the selected index values when the algorithm finishes
        except StopIteration:
            self.outer_idx, self.inner_idx = -1, -1

    def restart(self, new_alg, length=Preferences.NUM_ELEMENTS) -> None:
        """Restart the sorting process with the new algorithm."""

        self.current_alg = new_alg
        self.alg_method = {
            "selection": self.selection_sort,
            "insertion": self.insertion_sort,
            "bubble": self.bubble_sort
        }[self.current_alg]()

        self.array = self.create_new_array(length)
        self.outer_idx, self.inner_idx = -1, -1

    def selection_sort(self):
        """Sort the array using the Selection Sort algorithm.

        This generator yields the indices currently being examined
        so that the GUI can display each step of the algorithm.
        """

        # get the number of elements in the array.
        n = len(self.array)

        # move through each position in the array.
        for i in range(n):

            # highlight the current position.
            yield -1, i

            # assume the first unsorted element is the smallest.
            min_idx = i

            # search the remaining unsorted portion of the array.
            for j in range(i + 1, n):

                # highlight the current element being compared.
                yield min_idx, j

                # if the current element is smaller,
                # remember its index.
                if self.array[j] < self.array[min_idx]:
                    min_idx = j

            # swap the smallest element with the first
            # element in the unsorted portion.
            self.array[i], self.array[min_idx] = (
                self.array[min_idx],
                self.array[i]
            )

            # show the completed swap.
            yield i, min_idx

    def insertion_sort(self):
        """Sort the array using the Insertion Sort algorithm.

        The algorithm builds the sorted portion of the array one
        element at a time. The array is modified in-place.
        """

        n = len(self.array)

        # start with the second element because the first
        # element is already considered sorted.
        for i in range(1, n):

            # start comparing the current element with the
            # element immediately before it.
            j = i

            # move the current element toward the beginning
            # while it is smaller than the previous element.
            while j > 0:

                # show the two elements being compared.
                yield j - 1, j

                # stop if the elements are already in order.
                if self.array[j - 1] <= self.array[j]:
                    break

                # swap the two elements.
                self.array[j - 1], self.array[j] = (
                    self.array[j],
                    self.array[j - 1]
                )

                # move one position to the left.
                j -= 1

                # show the position after the swap.
                yield j, j + 1

    def bubble_sort(self):
        """Sort the array using the Bubble Sort algorithm.

        Bubble Sort repeatedly compares neighboring elements and
        swaps them if they are in the wrong order. The largest
        unsorted element moves toward the end of the array after
        each pass.
        """

        n = len(self.array)

        # each pass places one more large element at the end
        # of the unsorted portion of the array.
        for i in range(n - 1):

            # The last i elements are already sorted, so they
            # do not need to be checked again.
            for j in range(n - 1 - i):

                # show the two neighboring elements being compared.
                yield j, j + 1

                # swap if the elements are in the wrong order.
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = (
                        self.array[j + 1],
                        self.array[j]
                    )

                    # show the result of the swap.
                    yield j, j + 1

    def get_runtime(self) -> float:
        """Returns the length of time that the algorithm takes to sort."""

        # get the time before running
        start_time = time.time()

        # sort the given list
        for _ in self.alg_method:
            pass

        # get the time after running
        end_time = time.time()

        # r eturn the difference
        return end_time - start_time


if __name__ == "__main__":
    s = SortingAlgorithms()
    s.restart("bubble", 10000)
    print(s.get_runtime())