import unittest
import pygame as pg
from project.views.buttons import Button, \
    MasterButton, \
    RegionMasterButton, \
    MeasureMasterButton, \
    MeasureButton


class MyTestCase(unittest.TestCase):
    def test_button(self):
        button = Button(10, 20, 50, 60)
        self.assertEqual(pg.Rect(-15, 20, 50, 60), button.rect)
        self.assertEqual((10, 20), button.rect.midtop)
        self.assertEqual((255, 255, 255), button.return_color())

    def test_measure_button(self):
        measure_button = MeasureButton(0, 0, 20, 20)
        self.assertEqual((255, 0, 0), measure_button.return_color())
        self.assertFalse(measure_button.active)
        measure_button.clicked()
        self.assertEqual((0, 255, 0), measure_button.return_color())
        self.assertTrue(measure_button.active)
        measure_button.clicked()
        self.assertEqual((255, 0, 0), measure_button.return_color())
        self.assertFalse(measure_button.active)

    def test_master_buttons(self):
        # start with init and color
        measure_master = MeasureMasterButton(100, 100, 20, 20)
        region_master = RegionMasterButton(200, 100, 20, 20)
        master_button = MasterButton(300, 100, 20, 20)
        self.assertEqual((255, 255, 255), measure_master.return_color())
        self.assertEqual((255, 255, 255), region_master.return_color())
        self.assertEqual((255, 255, 255), master_button.return_color())

        # 2*3 matrix of buttons (2 rows, 3 columns)
        measure_button1 = MeasureButton(0, 0, 20, 20)
        measure_button2 = MeasureButton(0, 40, 20, 20)
        measure_button3 = MeasureButton(40, 0, 20, 20)
        measure_button4 = MeasureButton(40, 40, 20, 20)
        measure_button5 = MeasureButton(80, 0, 20, 20)
        measure_button6 = MeasureButton(80, 40, 20, 20)
        measure_buttons = [measure_button1, measure_button2, measure_button3,
                           measure_button4, measure_button5, measure_button6]
        # Note: actual shape looks like [1, 3, 5] in display
        #                               [2, 4, 6]

        # set button 2 and 3 to active
        measure_button2.clicked()
        measure_button3.clicked()

        # set parameters
        num_regions = 3
        num_measures = 2
        # master buttons first row
        MeasureMasterButton.clicked(measure_buttons, 0, num_measures, num_regions)
        self.assertTrue(measure_button1.active)
        self.assertTrue(measure_button3.active)
        self.assertTrue(measure_button5.active)

        # master buttons first column
        RegionMasterButton.clicked(measure_buttons, 0, num_measures)
        self.assertFalse(measure_button1.active)
        self.assertFalse(measure_button2.active)

        # master buttons first column again
        RegionMasterButton.clicked(measure_buttons, 0, num_measures)
        self.assertTrue(measure_button1.active)
        self.assertTrue(measure_button2.active)

        # master buttons first row
        MeasureMasterButton.clicked(measure_buttons, 0, num_measures, num_regions)
        self.assertFalse(measure_button1.active)
        self.assertFalse(measure_button3.active)
        self.assertFalse(measure_button5.active)

        # main master button
        MasterButton.clicked(measure_buttons)
        self.assertTrue(measure_button1.active)
        self.assertTrue(measure_button2.active)
        self.assertTrue(measure_button3.active)
        self.assertTrue(measure_button4.active)
        self.assertTrue(measure_button5.active)
        self.assertTrue(measure_button6.active)

        MasterButton.clicked(measure_buttons)
        self.assertFalse(measure_button1.active)
        self.assertFalse(measure_button2.active)
        self.assertFalse(measure_button3.active)
        self.assertFalse(measure_button4.active)
        self.assertFalse(measure_button5.active)
        self.assertFalse(measure_button6.active)

    def test_turn_button(self):
        turn_button = Button(0, 0, 20, 20, color=(255, 255, 255))
        self.assertEqual((255, 255, 255), turn_button.return_color())

    def test_end_button(self):
        end_button = Button(0, 0, 20, 20, color=(0, 0, 0))
        self.assertEqual((0, 0, 0), end_button.return_color())


if __name__ == '__main__':
    unittest.main()
