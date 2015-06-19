import unittest
import weather_loading as wl
import numpy as np

class TestSets(unittest.TestCase):
    
    def test_1Station_validTime(self):
        """
    
        """
        test_id = '00044'
        df = wl.load_dataframe(test_id,'20140101','20150101')
        station_id = np.unique(df[test_id]['Station ID'])
        
        self.assertEqual(len(station_id),1)
        self.assertEqual(station_id[0],int(test_id))

if __name__ == '__main__':
    unittest.main()