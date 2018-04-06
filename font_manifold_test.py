
# coding=utf-8
import sys
import unittest
import font_manifold
from sklearn import (manifold)
import os, shutil
from pathlib import Path

class TestStringMethods(unittest.TestCase):
    def test_info(self):
        df, ds=font_manifold.info('test_data',  'test_output')
        shutil.rmtree("test_output")
        if (df is None or ds is None):
            assert False
        else:
            assert True

    def test_embeding(self):
        df, ds = font_manifold.info('test_data', 'test_output')
        tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
        font_manifold.embed( df, ds, 'lower', 97, tsne, "test_output", False)
        shutil.rmtree("test_output")

    def test_plot(self):
        df, ds = font_manifold.info('test_data', 'test_output')
        tsne = manifold.TSNE(n_components=2, init='pca', random_state=0)
        font_manifold.embed( df, ds, 'lower', 97, tsne, "test_output", True)
        shutil.rmtree("test_output")

if __name__ == '__main__':
    unittest.main()