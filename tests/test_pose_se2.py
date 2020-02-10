"""Unit tests for the pose/pose_r2.py module.

"""


import unittest

import numpy as np

from graphslam.pose.se2 import PoseSE2


class TestPoseSE2(unittest.TestCase):
    """Tests for the ``PoseSE2`` class.

    """

    def test_constructor(self):
        """Test that a ``PoseSE2`` instance can be created.

        """
        r2a = PoseSE2([1, 2], 3)
        r2b = PoseSE2(np.array([3, 4]), 5)
        self.assertIsInstance(r2a, PoseSE2)
        self.assertIsInstance(r2b, PoseSE2)

    def test_to_array(self):
        """Test that the ``to_array`` method works as expected.

        """
        r2 = PoseSE2([1, 2], 1)
        arr = r2.to_array()

        self.assertIsInstance(arr, np.ndarray)
        self.assertNotIsInstance(arr, PoseSE2)
        self.assertAlmostEqual(np.linalg.norm(arr - np.array([1, 2, 1])), 0.)

    def test_to_compact(self):
        """Test that the ``to_compact`` method works as expected.

        """
        r2 = PoseSE2([1, 2], 1)
        arr = r2.to_compact()

        self.assertIsInstance(arr, np.ndarray)
        self.assertNotIsInstance(arr, PoseSE2)
        self.assertAlmostEqual(np.linalg.norm(arr - np.array([1, 2, 1])), 0.)

    def test_to_matrix_from_matrix(self):
        """Test that the ``to_matrix`` and ``from_matrix`` methods work as expected.

        """
        p1 = PoseSE2([1, 2], 1)
        p2 = PoseSE2([3, 6], np.pi / 3.)

        p1b = PoseSE2.from_matrix(p1.to_matrix())
        p2b = PoseSE2.from_matrix(p2.to_matrix())

        self.assertAlmostEqual(np.linalg.norm(p1.to_array() - p1b.to_array()), 0.)
        self.assertAlmostEqual(np.linalg.norm(p2.to_array() - p2b.to_array()), 0.)

    def test_position(self):
        """Test that the ``position`` property works as expected.

        """
        r2 = PoseSE2([1, 2], 3)
        pos = r2.position

        true_pos = np.array([1, 2])
        self.assertIsInstance(pos, np.ndarray)
        self.assertNotIsInstance(pos, PoseSE2)
        self.assertAlmostEqual(np.linalg.norm(true_pos - pos), 0.)

    def test_orientation(self):
        """Test that the ``orientation`` property works as expected.

        """
        r2 = PoseSE2([1, 2], 1.5)

        self.assertEqual(r2.orientation, 1.5)

    def test_inverse(self):
        """Test that the ``inverse`` property works as expected.

        """
        np.random.seed(0)

        for _ in range(10):
            p = PoseSE2(np.random.random_sample(2), np.random.random_sample())

            expected = np.linalg.inv(p.to_matrix())
            self.assertAlmostEqual(np.linalg.norm(p.inverse.to_matrix() - expected), 0.)

    def test_add(self):
        """Test that the overloaded ``__add__`` method works as expected.

        """
        np.random.seed(0)

        for _ in range(10):
            p1 = PoseSE2(np.random.random_sample(2), np.random.random_sample())
            p2 = PoseSE2(np.random.random_sample(2), np.random.random_sample())

            expected = PoseSE2.from_matrix(np.dot(p1.to_matrix(), p2.to_matrix()))
            self.assertAlmostEqual(np.linalg.norm((p1 + p2).to_array() - expected.to_array()), 0.)

    def test_sub(self):
        """Test that the overloaded ``__sub__`` method works as expected.

        """
        np.random.seed(0)

        for _ in range(10):
            p1 = PoseSE2(np.random.random_sample(2), np.random.random_sample())
            p2 = PoseSE2(np.random.random_sample(2), np.random.random_sample())

            expected = np.dot(np.linalg.inv(p2.to_matrix()), p1.to_matrix())
            self.assertAlmostEqual(np.linalg.norm((p1 - p2).to_matrix() - expected), 0.)


if __name__ == '__main__':
    unittest.main()
