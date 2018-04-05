import unittest
import data_sets
import os, shutil


class TestStringMethods(unittest.TestCase):
    def test_ready_too_small(self):

        with self.assertRaises(ValueError):
            data_sets.Data.ready_data(self, 0, 0, "unittest_data", True)




    def test_build(self):
        data_sets.Data.ready_data(self, 15, 15, "unittest_data", True)

        assert os.path.exists("unittest_data") == 1
        ttf=""
        for root, dirs, files in os.walk(r'fonts'):
            ttf=files[0]
            ttf=ttf[0:ttf.__len__() - 4]


        assert os.path.exists('unittest_data/'+ttf+'/'+ ttf+'_lower_a.png')
        shutil.rmtree("unittest_data")






    def build_data(self, ttf, W, H, path):
        data_sets.Data.build_data(self, ttf, W, H, path)



if __name__ == '__main__':
    unittest.main()