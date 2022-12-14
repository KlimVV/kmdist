#This file was originally generated by PyScripter's unit test wizard

import unittest
from channels import Channel, ChannelT, ChannelK, ChannelSortament

class TestChannel(unittest.TestCase):

    def testget_free_length(self):
        _sort = ChannelSortament()
        _sort.findbyname('18')
        chl = Channel(_sort.getChannelParams())
        self.assertEqual(chl.get_free_length(), 3060)


class TestChannelT(unittest.TestCase):

    def test_Jz(self):
        _sort = ChannelSortament()
        _sort.findbyname('18')
        chl = ChannelT(_sort.getChannelParams())
        self.assertEqual(chl.Jy, 2180)
        self.assertAlmostEqual(chl.Jz, 370, delta=2)

    def testget_free_length(self):
        _sort = ChannelSortament()
        _sort.findbyname('18')
        chl = ChannelT(_sort.getChannelParams())
        self.assertAlmostEqual(chl.iz, 3, places=1)
        self.assertAlmostEqual(chl.get_free_length(), 4500, delta=10)


class TestChannelK(unittest.TestCase):

    def setUp(self):
        _sort = ChannelSortament()
        _sort.findbyname('14')
        self.chl = ChannelK(_sort.getChannelParams())

    def testget_paint_area(self):
        self.assertEqual(self.chl.get_paint_area(1), 0.512)

    def testJy(self):
        self.assertEqual(self.chl.Jy, 982)

    def testJz(self):
        self.assertAlmostEqual(self.chl.Jz, 622.98, delta=1)

    def test_iy(self):
        self.assertEqual(self.chl.iy, 5.6)

    def test_iz(self):
        self.assertAlmostEqual(self.chl.iz, 4.47, delta=1)

    def testget_free_length(self):
        self.assertAlmostEqual(self.chl.get_free_length(), 6705, delta=5)

if __name__ == '__main__':
    unittest.main()
