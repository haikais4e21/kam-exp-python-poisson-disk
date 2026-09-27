import unittest
from poisson_disk import poisson_disk_sampling

class TestPoissonDiskSampling(unittest.TestCase):
    def test_sampling(self):
        points = poisson_disk_sampling(100, 100, 5)
        self.assertTrue(len(points) > 0)
        for point in points:
            self.assertTrue(0 <= point[0] < 100)
            self.assertTrue(0 <= point[1] < 100)

if __name__ == '__main__':
    unittest.main()