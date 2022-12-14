#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      klimv
#
# Created:     22.07.2022
# Copyright:   (c) klimv 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import unittest

from  angles import Angle, AngleX, AngleT, AngleK, AngleSortament

class TestAngle(unittest.TestCase):
    def test_get_free_length(self):
        _sort = AngleSortament()
        _sort.findbyname('63*6')
        ang = Angle(_sort.getAngleParams())
        self.assertEqual(ang.get_free_length(), 1860)

    def test_iv(self):
        _sort = AngleSortament()
        _sort.findbyname('63*6')
        ang = Angle(_sort.getAngleParams())
        self.assertEqual(ang.iv, 1.24)

class TestAngleX(unittest.TestCase):
    def test_get_free_length(self):
        _sort = AngleSortament()
        _sort.findbyname('140*10')
        ang = AngleX(_sort.getAngleParams())
        self.assertEqual(ang.get_free_length(), 8190)

    def test_iv(self):
        _sort = AngleSortament()
        _sort.findbyname('90*7')
        ang = AngleX(_sort.getAngleParams())
        self.assertEqual(ang.iv, 3.49)

    def test_step(self):
        _sort = AngleSortament()
        _sort.findbyname('200*12')
        ang = AngleX(_sort.getAngleParams())
        self.assertEqual(ang.step, 2488)

class TestAngleK(unittest.TestCase):
    def test_get_free_length(self):
        _sort = AngleSortament()
        _sort.findbyname('90*7')
        ang = AngleK(_sort.getAngleParams())
        self.assertAlmostEqual(ang.iv, 3.48, delta=0.1)
        self.assertAlmostEqual(ang.get_free_length(), 34.8*150, delta=20)

    def test_get_paint_area(self):
        _sort = AngleSortament()
        _sort.findbyname('90*7')
        ang = AngleK(_sort.getAngleParams())
        self.assertEqual(ang.get_paint_area(1), 0.36)


if __name__ == '__main__':
    unittest.main()