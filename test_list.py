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

from  lists import List, get_paintarea_by_mass

class TestList(unittest.TestCase):
    def test_massa(self):
        "перервірка маси листа 10 мм 1м х 1м"
        listObj = List(10, 1000, 1000)
        self.assertEqual(listObj.massa, 78.5)

    def test_paint_area(self):
        "площа фарбування листа 1м х 1м"
        listObj = List(10, 1000, 1000)
        self.assertEqual(listObj.paint_area, 2)

    def test_paint_area_by_mass(self):
        "площа фарбування листа 10 вагой 78,5кг тобто 1м х 1м"
        self.assertEqual(get_paintarea_by_mass(10, 78.5), 2)

if __name__ == '__main__':
    unittest.main()
