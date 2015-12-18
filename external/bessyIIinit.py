from copy import copy, deepcopy
import numpy as np
mode = 'ONLINE'

ao = dict()
bpm= [
['BPM1RES8R',   'DUMMY:rdX    ', 0 ,'BPM1RES8R', 'DUMMY:rdY    ', 0, [ 3, 8],   0       , 32   , 1   , 1   , 0   ],   #% 10Hz                     %Beamlost
['BPM2RES8R',   'DUMMY:rdX    ', 0 ,'BPM2RES8R', 'DUMMY:rdY    ', 0, [ 3, 9],   0       , 64   , 1   , 1   , 1   ],   #% 71Hz Ref   
['BPM3RES8R',   'DUMMY:rdX    ', 0 ,'BPM3RES8R', 'DUMMY:rdY    ', 0, [ 3,10],   0       , 72   , 1   , 1   , 2   ],
['BPM4RES8R',   'DUMMY:rdX    ', 0 ,'BPM4RES8R', 'DUMMY:rdY    ', 0, [ 3,11],   0       , 112  , 1   , 1   , 3   ],   # Manuela PSs HFBPD5R VFBPD5R
['BPM5RES8R',   'DUMMY:rdX    ', 0 ,'BPM5RES8R', 'DUMMY:rdY    ', 0, [ 3,12],   0       , 120  , 1   , 1   , 4   ],
['BPMZ43D1R',	'BPMZ43D1R:rdX', 0 ,'BPMZ43D1R', 'BPMZ43D1R:rdY', 0, [ 1, 7],	1.582   , 16   , 1   , 1   , 5   ],
['BPMZ44D1R',	'BPMZ44D1R:rdX', 0 ,'BPMZ44D1R', 'BPMZ44D1R:rdY', 0, [ 1, 8],	1.785   , 24   , 1   , 1   , 6   ],
['BPMZ5D1R ',	'BPMZ5D1R:rdX ', 0 ,'BPMZ5D1R', 'BPMZ5D1R:rdY ', 0, [ 1, 9],	2.736   , 1    , 1   , 1   , 7   ],
['BPMZ6D1R',	'BPMZ6D1R:rdX ', 1 ,'BPMZ6D1R', 'BPMZ6D1R:rdY ', 1, [ 1,10],	3.995   , 2    , 1   , 1   , 8   ],
['BPMZ7D1R ',	'BPMZ7D1R:rdX ', 1 ,'BPMZ7D1R', 'BPMZ7D1R:rdY ', 1, [ 1,11],	6.474   , 3    , 1   , 1   , 9   ],
['BPMZ1T1R',	'BPMZ1T1R:rdX ', 1 ,'BPMZ1T1R', 'BPMZ1T1R:rdY ', 1, [ 2,01],	7.675   , 4    , 1   , 1   , 10  ],
['BPMZ2T1R',	'BPMZ2T1R:rdX ', 1 ,'BPMZ2T1R', 'BPMZ2T1R:rdY ', 1, [ 2,02],	8.591   , 5    , 1   , 1   , 11  ],
['BPMZ3T1R',	'BPMZ3T1R:rdX ', 1 ,'BPMZ3T1R', 'BPMZ3T1R:rdY ', 1, [ 2,03],	11.005  , 6    , 1   , 1   , 12  ],
['BPMZ4T1R',	'BPMZ4T1R:rdX ', 1 ,'BPMZ4T1R', 'BPMZ4T1R:rdY ', 1, [ 2,04],	12.639  , 7    , 1   , 1   , 13  ],
['BPMZ43T1R',	'BPMZ43T1R:rdX', 0 ,'BPMZ43T1R', 'BPMZ43T1R:rdY', 0, [ 2,05],	15.9296 , 56   , 1   , 1   , 14  ],    #%->Inj. Trigger  
['BPMZ5T1R',	'BPMZ5T1R:rdX ', 1 ,'BPMZ5T1R', 'BPMZ5T1R:rdY ', 1, [ 2,06],	17.361  , 9    , 1   , 1   , 15  ],
['BPMZ6T1R',	'BPMZ6T1R:rdX ', 1 ,'BPMZ6T1R', 'BPMZ6T1R:rdY ', 1, [ 2,07],	18.995  , 10   , 1   , 1   , 16  ],
['BPMZ7T1R',	'BPMZ7T1R:rdX ', 1 ,'BPMZ7T1R', 'BPMZ7T1R:rdY ', 1, [ 2, 8],	21.474  , 11   , 1   , 1   , 17  ],
['BPMZ1D2R',	'BPMZ1D2R:rdX ', 1 ,'BPMZ1D2R', 'BPMZ1D2R:rdY ', 1, [ 3,01],	22.675  , 12   , 1   , 1   , 18  ],
['BPMZ2D2R',	'BPMZ2D2R:rdX ', 1 ,'BPMZ2D2R', 'BPMZ2D2R:rdY ', 1, [ 3,02],	23.591  , 13   , 1   , 1   , 19  ],
['BPMZ3D2R',	'BPMZ3D2R:rdX ', 1 ,'BPMZ3D2R', 'BPMZ3D2R:rdY ', 1, [ 3,03],	26.005  , 14   , 1   , 1   , 20  ],
['BPMZ4D2R',	'BPMZ4D2R:rdX ', 1 ,'BPMZ4D2R', 'BPMZ4D2R:rdY ', 1, [ 3,04],	27.264  , 15   , 0.3 , 1   , 21  ],
['BPMZ5D2R',	'BPMZ5D2R:rdX ', 1 ,'BPMZ5D2R', 'BPMZ5D2R:rdY ', 1, [ 3,05],	32.736  , 17   , 1   , 1   , 22  ],
['BPMZ6D2R',	'BPMZ6D2R:rdX ', 1 ,'BPMZ6D2R', 'BPMZ6D2R:rdY ', 1, [ 3,06],	33.995  , 18   , 1   , 1   , 23  ],
['BPMZ7D2R',	'BPMZ7D2R:rdX ', 1 ,'BPMZ7D2R', 'BPMZ7D2R:rdY ', 1, [ 3,07],	36.474  , 19   , 1   , 1   , 24  ],
['BPMZ1T2R',	'BPMZ1T2R:rdX ', 1 ,'BPMZ1T2R', 'BPMZ1T2R:rdY ', 1, [ 4,01],	37.675  , 20   , 1   , 1   , 25  ],
['BPMZ2T2R',	'BPMZ2T2R:rdX ', 1 ,'BPMZ2T2R', 'BPMZ2T2R:rdY ', 1, [ 4,02],	38.591  , 21   , 1   , 1   , 26  ],
['BPMZ3T2R',	'BPMZ3T2R:rdX ', 1 ,'BPMZ3T2R', 'BPMZ3T2R:rdY ', 1, [ 4,03],	41.005  , 22   , 1   , 1   , 27  ],
['BPMZ4T2R',	'BPMZ4T2R:rdX ', 1 ,'BPMZ4T2R', 'BPMZ4T2R:rdY ', 1, [ 4,04],	42.639  , 23   , 1   , 1   , 28  ],
['BPMZ5T2R',	'BPMZ5T2R:rdX ', 1 ,'BPMZ5T2R', 'BPMZ5T2R:rdY ', 1, [ 4,05],	47.361  , 25   , 1   , 1   , 29  ],
['BPMZ6T2R',	'BPMZ6T2R:rdX ', 1 ,'BPMZ6T2R', 'BPMZ6T2R:rdY ', 1, [ 4,06],	48.995  , 26   , 1   , 1   , 30  ],
['BPMZ7T2R',	'BPMZ7T2R:rdX ', 1 ,'BPMZ7T2R', 'BPMZ7T2R:rdY ', 1, [ 4,07],	51.474  , 27   , 1   , 1   , 31  ],
['BPMZ1D3R',	'BPMZ1D3R:rdX ', 1 ,'BPMZ1D3R', 'BPMZ1D3R:rdY ', 1, [ 5,01],	52.675  , 28   , 1   , 1   , 32  ],
['BPMZ2D3R',	'BPMZ2D3R:rdX ', 1 ,'BPMZ2D3R', 'BPMZ2D3R:rdY ', 1, [ 5,02],	53.591  , 29   , 1   , 1   , 33  ],
['BPMZ3D3R',	'BPMZ3D3R:rdX ', 1 ,'BPMZ3D3R', 'BPMZ3D3R:rdY ', 1, [ 5,03],	56.005  , 30   , 1   , 1   , 34  ],
['BPMZ4D3R',	'BPMZ4D3R:rdX ', 1 ,'BPMZ4D3R', 'BPMZ4D3R:rdY ', 1, [ 5,04],	57.264  , 31   , 1   , 1   , 35  ],
['BPMZ5D3R',	'BPMZ5D3R:rdX ', 1 ,'BPMZ5D3R', 'BPMZ5D3R:rdY ', 1, [ 5,05],	62.736  , 33   , 1   , 1   , 36  ],
['BPMZ6D3R',	'BPMZ6D3R:rdX ', 1 ,'BPMZ6D3R', 'BPMZ6D3R:rdY ', 1, [ 5,06],	63.995  , 34   , 1   , 1   , 37  ],
['BPMZ7D3R',	'BPMZ7D3R:rdX ', 1 ,'BPMZ7D3R', 'BPMZ7D3R:rdY ', 1, [ 5,07],	66.474  , 35   , 1   , 1   , 38  ],
['BPMZ1T3R',	'BPMZ1T3R:rdX ', 1 ,'BPMZ1T3R', 'BPMZ1T3R:rdY ', 1, [ 6,01],	67.675  , 36   , 1   , 1   , 39  ],
['BPMZ2T3R',	'BPMZ2T3R:rdX ', 0 ,'BPMZ2T3R', 'BPMZ2T3R:rdY ', 0, [ 6,02],	68.591  , 37   , 1   , 1   , 40  ],
['BPMZ3T3R',	'BPMZ3T3R:rdX ', 1 ,'BPMZ3T3R', 'BPMZ3T3R:rdY ', 1, [ 6,03],	71.005  , 38   , 1   , 1   , 41  ],
['BPMZ4T3R',	'BPMZ4T3R:rdX ', 1 ,'BPMZ4T3R', 'BPMZ4T3R:rdY ', 1, [ 6,04],	72.639  , 39   , 1   , 1   , 42  ],
['BPMZ41T3R',	'BPMZ41T3R:rdX', 0 ,'BPMZ41T3R', 'BPMZ41T3R:rdY', 0, [ 6,05],	74.1275 , 40   , 1   , 1   , 43  ],
['BPMZ42T3R',	'BPMZ42T3R:rdX', 0 ,'BPMZ42T3R', 'BPMZ42T3R:rdY', 0, [ 6,06],	75.3795 , 48   , 1   , 1   , 44  ],
['BPMZ5T3R',	'BPMZ5T3R:rdX ', 1 ,'BPMZ5T3R', 'BPMZ5T3R:rdY ', 1, [ 6,07],	77.361  , 41   , 1   , 1   , 45  ],
['BPMZ6T3R',	'BPMZ6T3R:rdX ', 1 ,'BPMZ6T3R', 'BPMZ6T3R:rdY ', 1, [ 6, 8],	78.995  , 42   , 1   , 1   , 46  ],
['BPMZ7T3R',	'BPMZ7T3R:rdX ', 1 ,'BPMZ7T3R', 'BPMZ7T3R:rdY ', 1, [ 6, 9],	81.474  , 43   , 1   , 1   , 47  ],
['BPMZ1D4R',	'BPMZ1D4R:rdX ', 1 ,'BPMZ1D4R', 'BPMZ1D4R:rdY ', 1, [ 7,01],	82.675  , 44   , 1   , 1   , 48  ],
['BPMZ2D4R',	'BPMZ2D4R:rdX ', 1 ,'BPMZ2D4R', 'BPMZ2D4R:rdY ', 1, [ 7,02],	83.591  , 45   , 1   , 1   , 49  ],
['BPMZ3D4R',	'BPMZ3D4R:rdX ', 1 ,'BPMZ3D4R', 'BPMZ3D4R:rdY ', 1, [ 7,03],	86.005  , 46   , 1   , 1   , 50  ],
['BPMZ4D4R',	'BPMZ4D4R:rdX ', 1 ,'BPMZ4D4R', 'BPMZ4D4R:rdY ', 1, [ 7,04],	87.264  , 47   , 1   , 1   , 51  ],
['BPMZ5D4R',	'BPMZ5D4R:rdX ', 1 ,'BPMZ5D4R', 'BPMZ5D4R:rdY ', 1, [ 7,05],	92.736  , 49   , 1   , 1   , 52  ],
['BPMZ6D4R',	'BPMZ6D4R:rdX ', 1 ,'BPMZ6D4R', 'BPMZ6D4R:rdY ', 1, [ 7,06],	93.995  , 50   , 1   , 1   , 53  ],
['BPMZ7D4R',	'BPMZ7D4R:rdX ', 0 ,'BPMZ7D4R', 'BPMZ7D4R:rdY ', 0, [ 7,07],	96.474  , 51   , 1   , 1   , 54  ],
['BPMZ1T4R',	'BPMZ1T4R:rdX ', 1 ,'BPMZ1T4R', 'BPMZ1T4R:rdY ', 1, [ 8,01],	97.675  , 52   , 1   , 1   , 55  ],
['BPMZ2T4R',	'BPMZ2T4R:rdX ', 1 ,'BPMZ2T4R', 'BPMZ2T4R:rdY ', 1, [ 8,02],	98.591  , 53   , 1   , 1   , 56  ],
['BPMZ3T4R',	'BPMZ3T4R:rdX ', 1 ,'BPMZ3T4R', 'BPMZ3T4R:rdY ', 1, [ 8,03],	101.005 , 54   , 1   , 1   , 57  ],
['BPMZ4T4R',	'BPMZ4T4R:rdX ', 1 ,'BPMZ4T4R', 'BPMZ4T4R:rdY ', 1, [ 8,04],	102.639 , 55   , 1   , 1   , 58  ],
['BPMZ5T4R',	'BPMZ5T4R:rdX ', 1 ,'BPMZ5T4R', 'BPMZ5T4R:rdY ', 1, [ 8,05],	107.361 , 57   , 1   , 1   , 59  ],
['BPMZ6T4R',	'BPMZ6T4R:rdX ', 1 ,'BPMZ6T4R', 'BPMZ6T4R:rdY ', 1, [ 8,06],	108.995 , 58   , 1   , 1   , 60  ],
['BPMZ7T4R',	'BPMZ7T4R:rdX ', 1 ,'BPMZ7T4R', 'BPMZ7T4R:rdY ', 1, [ 8,07],	111.474 , 59   , 1   , 1   , 61  ],
['BPMZ1D5R',	'BPMZ1D5R:rdX ', 1 ,'BPMZ1D5R', 'BPMZ1D5R:rdY ', 1, [ 9,01],	112.675 , 60   , 1   , 1   , 62  ],
['BPMZ2D5R',	'BPMZ2D5R:rdX ', 1 ,'BPMZ2D5R', 'BPMZ2D5R:rdY ', 1, [ 9,02],	113.591 , 61   , 1   , 1   , 63  ],
['BPMZ3D5R',	'BPMZ3D5R:rdX ', 1 ,'BPMZ3D5R', 'BPMZ3D5R:rdY ', 1, [ 9,03],	116.005 , 62   , 1   , 1   , 64  ],
['BPMZ4D5R',	'BPMZ4D5R:rdX ', 1 ,'BPMZ4D5R', 'BPMZ4D5R:rdY ', 1, [ 9,04],	117.6933, 63   , 1   , 1   , 65  ],
['BPMZ5D5R',	'BPMZ5D5R:rdX ', 1 ,'BPMZ5D5R', 'BPMZ5D5R:rdY ', 1, [ 9,05],	122.3067, 65   , 1   , 1   , 66  ],
['BPMZ6D5R',	'BPMZ6D5R:rdX ', 1 ,'BPMZ6D5R', 'BPMZ6D5R:rdY ', 1, [ 9,06],	123.995 , 66   , 1   , 1   , 67  ],
['BPMZ7D5R',	'BPMZ7D5R:rdX ', 1 ,'BPMZ7D5R', 'BPMZ7D5R:rdY ', 1, [ 9,07],	126.474 , 67   , 1   , 1   , 68  ],
['BPMZ1T5R',	'BPMZ1T5R:rdX ', 1 ,'BPMZ1T5R', 'BPMZ1T5R:rdY ', 1, [10,01],	127.675 , 68   , 1   , 1   , 69  ],
['BPMZ2T5R',    'BPMZ2T5R:rdX ', 1 ,'BPMZ2T5R', 'BPMZ2T5R:rdY ', 1, [10,02],	128.591 , 69   , 1   , 1   , 70  ],
['BPMZ3T5R',	'BPMZ3T5R:rdX ', 1 ,'BPMZ3T5R', 'BPMZ3T5R:rdY ', 1, [10,03],	131.005 , 70   , 1   , 1   , 71  ],
['BPMZ4T5R',	'BPMZ4T5R:rdX ', 1 ,'BPMZ4T5R', 'BPMZ4T5R:rdY ', 1, [10,04],	132.639 , 71   , 1   , 1   , 72  ],
['BPMZ5T5R',	'BPMZ5T5R:rdX ', 1 ,'BPMZ5T5R', 'BPMZ5T5R:rdY ', 1, [10,05],	137.361 , 73   , 1   , 1   , 73  ],
['BPMZ6T5R',	'BPMZ6T5R:rdX ', 1 ,'BPMZ6T5R', 'BPMZ6T5R:rdY ', 1, [10,06],	138.995 , 74   , 1   , 1   , 74  ],
['BPMZ7T5R',	'BPMZ7T5R:rdX ', 1 ,'BPMZ7T5R', 'BPMZ7T5R:rdY ', 1, [10,07],	141.474 , 75   , 1   , 1   , 75  ],
['BPMZ1D6R',	'BPMZ1D6R:rdX ', 1 ,'BPMZ1D6R', 'BPMZ1D6R:rdY ', 1, [11,01],	142.675 , 76   , 1   , 1   , 76  ],
['BPMZ2D6R',	'BPMZ2D6R:rdX ', 1 ,'BPMZ2D6R', 'BPMZ2D6R:rdY ', 1, [11,02],	143.591 , 77   , 1   , 1   , 77  ],
['BPMZ3D6R',	'BPMZ3D6R:rdX ', 1 ,'BPMZ3D6R', 'BPMZ3D6R:rdY ', 1, [11,03],	146.005 , 78   , 1   , 1   , 78  ],
['BPMZ4D6R',	'BPMZ4D6R:rdX ', 1 ,'BPMZ4D6R', 'BPMZ4D6R:rdY ', 1, [11,04],	147.264 , 79   , 1   , 1   , 79  ],
['BPMZ41D6R',	'BPMZ41D6R:rdX', 0 ,'BPMZ41D6R', 'BPMZ41D6R:rdY', 0, [11,05],	147.7291, 80   , 1   , 1   , 80  ],
['BPMZ42D6R',	'BPMZ42D6R:rdX', 0 ,'BPMZ42D6R', 'BPMZ42D6R:rdY', 0, [11,06],	149.5804, 88   , 1   , 1   , 81  ],
['BPMZ43D6R',	'BPMZ43D6R:rdX', 0 ,'BPMZ43D6R', 'BPMZ43D6R:rdY', 0, [11,07],	150.2976, 96   , 1   , 1   , 82  ],
['BPMZ44D6R',	'BPMZ44D6R:rdX', 0 ,'BPMZ44D6R', 'BPMZ44D6R:rdY', 0, [11, 8],	152.3250, 104  , 1   , 1   , 83  ],
['BPMZ5D6R',    'BPMZ5D6R:rdX ', 0 ,'BPMZ5D6R ', 'BPMZ5D6R:rdY ', 0, [11, 9],   152.736 , 81   , 1   , 1   , 84  ],   #existiert nicht mehr
['BPMZ6D6R',	'BPMZ6D6R:rdX ', 1 ,'BPMZ6D6R', 'BPMZ6D6R:rdY ', 1, [11,10],	153.995 , 82   , 1   , 1   , 85  ],
['BPMZ7D6R',	'BPMZ7D6R:rdX ', 1 ,'BPMZ7D6R', 'BPMZ7D6R:rdY ', 1, [11,11],	156.474 , 83   , 1   , 1   , 86  ],
['BPMZ1T6R',	'BPMZ1T6R:rdX ', 1 ,'BPMZ1T6R', 'BPMZ1T6R:rdY ', 1, [12,01],	157.675 , 84   , 1   , 1   , 87  ],
['BPMZ2T6R',	'BPMZ2T6R:rdX ', 1 ,'BPMZ2T6R', 'BPMZ2T6R:rdY ', 1, [12,02],	158.591 , 85   , 1   , 1   , 88  ],
['BPMZ3T6R',	'BPMZ3T6R:rdX ', 1 ,'BPMZ3T6R', 'BPMZ3T6R:rdY ', 1, [12,03],	161.005 , 86   , 1   , 1   , 89  ],
['BPMZ4T6R',	'BPMZ4T6R:rdX ', 1 ,'BPMZ4T6R', 'BPMZ4T6R:rdY ', 1, [12,04],	162.639 , 87   , 1   , 1   , 90  ],
['BPMZ5T6R',	'BPMZ5T6R:rdX ', 1 ,'BPMZ5T6R', 'BPMZ5T6R:rdY ', 1, [12,05],	167.361 , 89   , 1   , 1   , 91  ],
['BPMZ6T6R',	'BPMZ6T6R:rdX ', 1 ,'BPMZ6T6R', 'BPMZ6T6R:rdY ', 1, [12,06],	168.995 , 90   , 1   , 1   , 92  ],
['BPMZ7T6R',	'BPMZ7T6R:rdX ', 1 ,'BPMZ7T6R', 'BPMZ7T6R:rdY ', 1, [12,07],	171.474 , 91   , 1   , 1   , 93  ],
['BPMZ1D7R',	'BPMZ1D7R:rdX ', 1 ,'BPMZ1D7R', 'BPMZ1D7R:rdY ', 1, [13,01],	172.675 , 92   , 1   , 1   , 94  ],
['BPMZ2D7R',	'BPMZ2D7R:rdX ', 1 ,'BPMZ2D7R', 'BPMZ2D7R:rdY ', 1, [13,02],	173.591 , 93   , 1   , 1   , 95  ],
['BPMZ3D7R',	'BPMZ3D7R:rdX ', 1 ,'BPMZ3D7R', 'BPMZ3D7R:rdY ', 1, [13,03],	176.005 , 94   , 1   , 1   , 96  ],
['BPMZ4D7R',	'BPMZ4D7R:rdX ', 1 ,'BPMZ4D7R', 'BPMZ4D7R:rdY ', 1, [13,04],	177.264 , 95   , 1   , 1   , 97  ],
['BPMZ5D7R',	'BPMZ5D7R:rdX ', 1 ,'BPMZ5D7R', 'BPMZ5D7R:rdY ', 1, [13,05],	182.736 , 97   , 1   , 1   , 98  ],
['BPMZ6D7R',	'BPMZ6D7R:rdX ', 1 ,'BPMZ6D7R', 'BPMZ6D7R:rdY ', 1, [13,06],	183.995 , 98   , 1   , 1   , 99  ],
['BPMZ7D7R',	'BPMZ7D7R:rdX ', 1 ,'BPMZ7D7R', 'BPMZ7D7R:rdY ', 1, [13,07],	186.474 , 99   , 1   , 1   , 100 ],
['BPMZ1T7R',	'BPMZ1T7R:rdX ', 1 ,'BPMZ1T7R', 'BPMZ1T7R:rdY ', 1, [14,01],	187.675 , 100  , 1   , 1   , 101 ],
['BPMZ2T7R',	'BPMZ2T7R:rdX ', 1 ,'BPMZ2T7R', 'BPMZ2T7R:rdY ', 1, [14,02],	188.591 , 101  , 1   , 1   , 102 ],
['BPMZ3T7R',	'BPMZ3T7R:rdX ', 1 ,'BPMZ3T7R', 'BPMZ3T7R:rdY ', 1, [14,03],	191.005 , 102  , 1   , 1   , 103 ],
['BPMZ4T7R',	'BPMZ4T7R:rdX ', 1 ,'BPMZ4T7R', 'BPMZ4T7R:rdY ', 1, [14,04],	192.639 , 103  , 1   , 1   , 104 ],
['BPMZ5T7R',	'BPMZ5T7R:rdX ', 1 ,'BPMZ5T7R', 'BPMZ5T7R:rdY ', 1, [14,05],	197.361 , 105  , 1   , 1   , 105 ],
['BPMZ6T7R',	'BPMZ6T7R:rdX ', 1 ,'BPMZ6T7R', 'BPMZ6T7R:rdY ', 1, [14,06],	198.995 , 106  , 1   , 1   , 106 ],
['BPMZ7T7R',	'BPMZ7T7R:rdX ', 1 ,'BPMZ7T7R', 'BPMZ7T7R:rdY ', 1, [14,07],	201.474 , 107  , 1   , 1   , 107 ],
['BPMZ1D8R',	'BPMZ1D8R:rdX ', 1 ,'BPMZ1D8R', 'BPMZ1D8R:rdY ', 1, [15,01],	202.675 , 108  , 1   , 1   , 108 ],
['BPMZ2D8R',	'BPMZ2D8R:rdX ', 1 ,'BPMZ2D8R', 'BPMZ2D8R:rdY ', 1, [15,02],	203.591 , 109  , 1   , 1   , 109 ],
['BPMZ3D8R',	'BPMZ3D8R:rdX ', 1 ,'BPMZ3D8R', 'BPMZ3D8R:rdY ', 1, [15,03],	206.005 , 110  , 1   , 1   , 110 ],
['BPMZ4D8R',	'BPMZ4D8R:rdX ', 1 ,'BPMZ4D8R', 'BPMZ4D8R:rdY ', 1, [15,04],	207.264 , 111  , 1   , 1   , 111 ],
['BPMZ5D8R',	'BPMZ5D8R:rdX ', 1 ,'BPMZ5D8R', 'BPMZ5D8R:rdY ', 1, [15,05],	212.736 , 113  , 1   , 1   , 112 ],
['BPMZ6D8R',	'BPMZ6D8R:rdX ', 1 ,'BPMZ6D8R', 'BPMZ6D8R:rdY ', 1, [15,06],	213.995 , 114  , 1   , 1   , 113 ],
['BPMZ7D8R',	'BPMZ7D8R:rdX ', 1 ,'BPMZ7D8R', 'BPMZ7D8R:rdY ', 1, [15,07],	216.474 , 115  , 1   , 1   , 114 ],
['BPMZ1T8R',	'BPMZ1T8R:rdX ', 1 ,'BPMZ1T8R', 'BPMZ1T8R:rdY ', 1, [16,01],	217.675 , 116  , 1   , 1   , 115 ],
['BPMZ2T8R',	'BPMZ2T8R:rdX ', 1 ,'BPMZ2T8R', 'BPMZ2T8R:rdY ', 1, [16,02],	218.591 , 117  , 1   , 1   , 116 ],
['BPMZ3T8R',	'BPMZ3T8R:rdX ', 1 ,'BPMZ3T8R', 'BPMZ3T8R:rdY ', 1, [16,03],	221.005 , 118  , 1   , 1   , 117 ],
['BPMZ4T8R',	'BPMZ4T8R:rdX ', 1 ,'BPMZ4T8R', 'BPMZ4T8R:rdY ', 1, [16,04],	222.639 , 119  , 1   , 1   , 118 ],
['BPMZ5T8R',	'BPMZ5T8R:rdX ', 1 ,'BPMZ5T8R', 'BPMZ5T8R:rdY ', 1, [16,05],	227.361 , 121  , 1   , 1   , 119 ],
['BPMZ6T8R',	'BPMZ6T8R:rdX ', 1 ,'BPMZ6T8R', 'BPMZ6T8R:rdY ', 1, [16,06],	228.995 , 122  , 1   , 1   , 120 ],
['BPMZ7T8R',	'BPMZ7T8R:rdX ', 1 ,'BPMZ7T8R', 'BPMZ7T8R:rdY ', 1, [16,07],	231.474 , 123  , 1   , 1   , 121 ],
['BPMZ1D1R',	'BPMZ1D1R:rdX ', 1 ,'BPMZ1D1R', 'BPMZ1D1R:rdY ', 1, [01,01],	232.675 , 124  , 1   , 1   , 122 ],
['BPMZ2D1R',	'BPMZ2D1R:rdX ', 1 ,'BPMZ2D1R', 'BPMZ2D1R:rdY ', 1, [01,02],	233.591 , 125  , 1   , 1   , 123 ],
['BPMZ3D1R',	'BPMZ3D1R:rdX ', 1 ,'BPMZ3D1R', 'BPMZ3D1R:rdY ', 1, [01,03],	236.005 , 126  , 1   , 1   , 124 ],
['BPMZ4D1R',	'BPMZ4D1R:rdX ', 1 ,'BPMZ4D1R', 'BPMZ4D1R:rdY ', 1, [01,04],	237.264 , 127  , 1   , 1   , 125 ],
['BPMZ41D1R',	'BPMZ41D1R:rdX', 0 ,'BPMZ41D1R', 'BPMZ41D1R:rdY', 0, [01,05],	238.215 , 8    , 1   , 1   , 126 ],
['BPMZ42D1R',	'BPMZ42D1R:rdX', 0 ,'BPMZ42D1R', 'BPMZ42D1R:rdY', 0, [01,06],	238.418 , 128  , 1   , 1   , 127 ],
];
bpm = map(list,zip(*bpm))
ao['BPMx'] = {}
ao['BPMy'] = {}
ao['BPMx']['CommonNames']                    = np.array(bpm[0])
ao['BPMy']['CommonNames']                    = np.array(bpm[3])
ao['BPMx']['Monitor'] = {}
ao['BPMy']['Monitor'] = {}
ao['BPMx']['Monitor']['Mode']               = 'Special'
ao['BPMy']['Monitor']['Mode']               = 'Special'
ao['BPMx']['Monitor']['HWUnits']            = 'mm'
ao['BPMy']['Monitor']['PhysicalUnits']      = 'meter'
ao['BPMx']['Monitor']['ChannelNames']        = np.array(bpm[1])
ao['BPMy']['Monitor']['ChannelNames']        = np.array(bpm[4])
ao['BPMx']['Monitor']['SpecialFunctionGet'] = 'getBPMFromIOC-BESSYII.py'
ao['BPMy']['Monitor']['SpecialFunctionGet'] = 'getBPMFromIOC-BESSYII.py'
ao['BPMx']['Monitor']['MetaGain']           = np.array(bpm[9])
ao['BPMy']['Monitor']['MetaGain']           = np.array(bpm[10])
ao['BPMx']['Status']                        = np.array(bpm[2])
ao['BPMy']['Status']                        = np.array(bpm[5])
ao['BPMx']['DeviceList']                  = np.array(bpm[6])
ao['BPMy']['DeviceList']                  = np.array(bpm[6])
ao['BPMx']['Element']                       = np.array(bpm[11])
ao['BPMy']['Element']                       = np.array(bpm[11])
ao['BPMx']['Pos']                           = np.array(bpm[7])
ao['BPMy']['Pos']                           = np.array(bpm[7])
ao['BPMx']['Offset']                        = np.zeros(len(ao['BPMy']['Status']))
ao['BPMy']['Offset']                        = np.zeros(len(ao['BPMy']['Status']))
ao['BPMx']['WaveRecordIndex']               = np.array(bpm[8])
ao['BPMy']['WaveRecordIndex']               = np.array(bpm[8])+128


cb     = 9.065778423065872e-04
cb_fs1 = 0.00471624/2
cb_fs2 = -0.00494618/2
cb_fs3 = 0.00471624/2
bend=[
['BM2D1R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,01],  1,  cb      , 004.755 ],
['BM1T1R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,11],  2,  cb      , 009.39  ],
['BM2T1R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,11],  3,  cb      , 019.755 ],
['BM1D2R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,02],  4,  cb      , 024.39  ],
['BM2D2R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,02],  5,  cb      , 034.755 ],
['BM1T2R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,12],  6,  cb      , 039.39  ],
['BM2T2R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,12],  7,  cb      , 049.755 ],
['BM1D3R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,03],  8,  cb      , 054.39  ],
['BM2D3R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,03],  9,  cb      , 064.755 ],
['BM1T3R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,13], 10,  cb      , 069.39  ],
['BM2T3R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,13], 11,  cb      , 079.755 ],
['BM1D4R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,04], 12,  cb      , 084.39  ],
['BM2D4R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,04], 13,  cb      , 094.755 ],
['BM1T4R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,14], 14,  cb      , 099.39  ],
['BM2T4R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,14], 15,  cb      , 109.755 ],
['BM1D5R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,05], 16,  cb      , 114.39  ],
['BM2D5R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,05], 17,  cb      , 124.755 ],
['BM1T5R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,15], 18,  cb      , 129.39  ],
['BM2T5R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,15], 19,  cb      , 139.755 ],
['BM1D6R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,06], 20,  cb      , 144.39  ],
['B1ID6R', 'PB1ID6R:rdbk' , 'PB1ID6R:set' , 1 ,[10,06], 21,  cb_fs1  , 147.3580],
['B2ID6R', 'PB2ID6R:rdbk' , 'PB2ID6R:set' , 1 ,[20,06], 22,  cb_fs2  , 149.6581],
['B3ID6R', 'PB3ID6R:rdbk' , 'PB3ID6R:set' , 1 ,[30,06], 23,  cb_fs3  , 152.4344],
['BM2D6R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,06], 24,  cb      , 154.755 ],
['BM1T6R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,16], 25,  cb      , 159.39  ],
['BM2T6R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,16], 26,  cb      , 169.755 ],
['BM1D7R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,07], 27,  cb      , 174.39  ],
['BM2D7R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,07], 28,  cb      , 184.755 ],
['BM1T7R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,17], 29,  cb      , 189.39  ],
['BM2T7R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,17], 30,  cb      , 199.755 ],
['BM1D8R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01, 8], 31,  cb      , 204.39  ],
['BM2D8R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02, 8], 32,  cb      , 214.755 ],
['BM1T8R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,18], 33,  cb      , 219.39  ],
['BM2T8R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[02,18], 34,  cb      , 229.755 ],
['BM1D1R', 'BPR:rdbk    ' , 'BPR:set    ' , 1 ,[01,01], 35,  cb      , 234.39  ],
]
bend = map(list,zip(*bend))
ao['BEND'] = {}
ao['BEND']['CommonNames']              = np.array(bend[0])
ao['BEND']['Status']                   = np.array(bend[3])
ao['BEND']['DeviceList']             = np.array(bend[4])
ao['BEND']['Element']                  = np.array(bend[5])
ao['BEND']['Pos']                      = np.array(bend[6])
ao['BEND']['Monitor']                  = {}
ao['BEND']['Monitor']['Mode']          = mode
ao['BEND']['Monitor']['HWUnits']       = 'ampere'
ao['BEND']['Monitor']['PhysicalUnits'] = 'radian'
ao['BEND']['Setpoint'] = deepcopy(ao['BEND']['Monitor'])
ao['BEND']['Monitor']['ChannelNames']  = np.array(bend[1])
ao['BEND']['Setpoint']['ChannelNames'] = np.array(bend[2])


hbm = -0.00159919;
hs1 = -0.00553438;
hs4 = -0.0044502;
ihbm = 0.14/2; #Nutzeroptik
ihs  = 0.07/6.; #14.06.10
hcm_r_type = 'rohrer     ';
hcm_w_type = 'wme        ';
hcm_b_type = 'commingsoon';
hcm=[
['HS4M2D1R', 'HS4P2D1R:rdbk', 'HS4P2D1R:set', 1, [01,04],  1, 2.806    ,hs4, ihs	,hcm_r_type],
['HBM2D1R ', 'HBP2D1R:rdbk ', 'HBP2D1R:set ', 1, [01,05],  2, 4.755    ,hbm, ihbm	,hcm_b_type],
['HS1MT1R ', 'HS1PT1R:rdbk ', 'HS1PT1R:set ', 1, [02,01],  3, 7.395    ,hs1, ihs	,hcm_r_type],
['HBM1T1R ', 'HBP1T1R:rdbk ', 'HBP1T1R:set ', 1, [02,02],  4, 9.39     ,hbm, ihbm	,hcm_b_type],
['HS4M1T1R', 'HS4P1T1R:rdbk', 'HS4P1T1R:set', 1, [02,03],  5, 12.034   ,hs4, ihs	,hcm_w_type],
['HS4M2T1R', 'HS4P2T1R:rdbk', 'HS4P2T1R:set', 1, [02,04],  6, 17.806   ,hs4, ihs	,hcm_r_type],
['HBM2T1R ', 'HBP2T1R:rdbk ', 'HBP2T1R:set ', 1, [02,05],  7, 19.755   ,hbm, ihbm	,hcm_b_type],
['HS1MD2R ', 'HS1PD2R:rdbk ', 'HS1PD2R:set ', 1, [03,01],  8, 22.395   ,hs1, ihs	,hcm_r_type],
['HBM1D2R ', 'HBP1D2R:rdbk ', 'HBP1D2R:set ', 1, [03,02],  9, 24.39    ,hbm, ihbm	,hcm_b_type],
['HS4M1D2R', 'HS4P1D2R:rdbk', 'HS4P1D2R:set', 1, [03,03], 10, 27.034   ,hs4, ihs	,hcm_r_type],
['HS4M2D2R', 'HS4P2D2R:rdbk', 'HS4P2D2R:set', 1, [03,04], 11, 32.806   ,hs4, ihs	,hcm_r_type],
['HBM2D2R ', 'HBP2D2R:rdbk ', 'HBP2D2R:set ', 1, [03,05], 12, 34.755   ,hbm, ihbm	,hcm_b_type],
['HS1MT2R ', 'HS1PT2R:rdbk ', 'HS1PT2R:set ', 1, [04,01], 13, 37.395   ,hs1, ihs	,hcm_w_type],
['HBM1T2R ', 'HBP1T2R:rdbk ', 'HBP1T2R:set ', 1, [04,02], 14, 39.39    ,hbm, ihbm	,hcm_b_type],
['HS4M1T2R', 'HS4P1T2R:rdbk', 'HS4P1T2R:set', 1, [04,03], 15, 42.034   ,hs4, ihs	,hcm_w_type],
['HS4M2T2R', 'HS4P2T2R:rdbk', 'HS4P2T2R:set', 1, [04,04], 16, 47.806   ,hs4, ihs	,hcm_r_type],
['HBM2T2R ', 'HBP2T2R:rdbk ', 'HBP2T2R:set ', 1, [04,05], 17, 49.755   ,hbm, ihbm	,hcm_b_type],
['HS1MD3R ', 'HS1PD3R:rdbk ', 'HS1PD3R:set ', 1, [05,01], 18, 52.395   ,hs1, ihs	,hcm_r_type],
['HBM1D3R ', 'HBP1D3R:rdbk ', 'HBP1D3R:set ', 1, [05,02], 19, 54.39    ,hbm, ihbm	,hcm_b_type],
['HS4M1D3R', 'HS4P1D3R:rdbk', 'HS4P1D3R:set', 1, [05,03], 20, 57.034   ,hs4, ihs	,hcm_r_type],
['HS4M2D3R', 'HS4P2D3R:rdbk', 'HS4P2D3R:set', 1, [05,04], 21, 62.806   ,hs4, ihs	,hcm_r_type],
['HBM2D3R ', 'HBP2D3R:rdbk ', 'HBP2D3R:set ', 1, [05,05], 22, 64.755   ,hbm, ihbm	,hcm_b_type],
['HS1MT3R ', 'HS1PT3R:rdbk ', 'HS1PT3R:set ', 1, [06,01], 23, 67.395   ,hs1, ihs	,hcm_r_type],
['HBM1T3R ', 'HBP1T3R:rdbk ', 'HBP1T3R:set ', 1, [06,02], 24, 69.39    ,hbm, ihbm	,hcm_b_type],
['HS4M1T3R', 'HS4P1T3R:rdbk', 'HS4P1T3R:set', 1, [06,03], 25, 72.034   ,hs4, ihs	,hcm_r_type],
['HS4M2T3R', 'HS4P2T3R:rdbk', 'HS4P2T3R:set', 1, [06,04], 26, 77.806   ,hs4, ihs	,hcm_r_type],
['HBM2T3R ', 'HBP2T3R:rdbk ', 'HBP2T3R:set ', 1, [06,05], 27, 79.755   ,hbm, ihbm	,hcm_b_type],
['HS1MD4R ', 'HS1PD4R:rdbk ', 'HS1PD4R:set ', 1, [07,01], 28, 82.395   ,hs1, ihs	,hcm_r_type],	
['HBM1D4R ', 'HBP1D4R:rdbk ', 'HBP1D4R:set ', 1, [07,02], 29, 84.39    ,hbm, ihbm	,hcm_b_type],
['HS4M1D4R', 'HS4P1D4R:rdbk', 'HS4P1D4R:set', 1, [07,03], 30, 87.034   ,hs4, ihs	,hcm_r_type],
['HS4M2D4R', 'HS4P2D4R:rdbk', 'HS4P2D4R:set', 1, [07,04], 31, 92.806   ,hs4, ihs	,hcm_r_type],
['HBM2D4R ', 'HBP2D4R:rdbk ', 'HBP2D4R:set ', 1, [07,05], 32, 94.755   ,hbm, ihbm	,hcm_b_type],
['HS1MT4R ', 'HS1PT4R:rdbk ', 'HS1PT4R:set ', 1, [ 8,01], 33, 97.395   ,hs1, ihs	,hcm_r_type],
['HBM1T4R ', 'HBP1T4R:rdbk ', 'HBP1T4R:set ', 1, [ 8,02], 34, 99.39    ,hbm, ihbm	,hcm_b_type],
['HS4M1T4R', 'HS4P1T4R:rdbk', 'HS4P1T4R:set', 1, [ 8,03], 35, 102.034  ,hs4, ihs	,hcm_r_type],
['HS4M2T4R', 'HS4P2T4R:rdbk', 'HS4P2T4R:set', 1, [ 8,04], 36, 107.806  ,hs4, ihs	,hcm_r_type],
['HBM2T4R ', 'HBP2T4R:rdbk ', 'HBP2T4R:set ', 1, [ 8,05], 37, 109.755  ,hbm, ihbm	,hcm_b_type],
['HS1MD5R ', 'HS1PD5R:rdbk ', 'HS1PD5R:set ', 1, [ 9,01], 38, 112.395  ,hs1, ihs	,hcm_r_type],
['HBM1D5R ', 'HBP1D5R:rdbk ', 'HBP1D5R:set ', 1, [ 9,02], 39, 114.39   ,hbm, ihbm	,hcm_b_type],
['HS4M1D5R', 'HS4P1D5R:rdbk', 'HS4P1D5R:set', 1, [ 9,03], 40, 117.034  ,hs4, ihs	,hcm_r_type],
['HS4M2D5R', 'HS4P2D5R:rdbk', 'HS4P2D5R:set', 1, [ 9,04], 41, 122.806  ,hs4, ihs	,hcm_r_type],
['HBM2D5R ', 'HBP2D5R:rdbk ', 'HBP2D5R:set ', 1, [ 9,05], 42, 124.755  ,hbm, ihbm	,hcm_b_type],
['HS1MT5R ', 'HS1PT5R:rdbk ', 'HS1PT5R:set ', 1, [10,01], 43, 127.395  ,hs1, ihs	,hcm_r_type],
['HBM1T5R ', 'HBP1T5R:rdbk ', 'HBP1T5R:set ', 1, [10,02], 44, 129.39   ,hbm, ihbm	,hcm_b_type],
['HS4M1T5R', 'HS4P1T5R:rdbk', 'HS4P1T5R:set', 1, [10,03], 45, 132.034  ,hs4, ihs	,hcm_r_type],
['HS4M2T5R', 'HS4P2T5R:rdbk', 'HS4P2T5R:set', 1, [10,04], 46, 137.806  ,hs4, ihs	,hcm_r_type],
['HBM2T5R ', 'HBP2T5R:rdbk ', 'HBP2T5R:set ', 1, [10,05], 47, 139.755  ,hbm, ihbm	,hcm_b_type],
['HS1MD6R ', 'HS1PD6R:rdbk ', 'HS1PD6R:set ', 1, [11,01], 48, 142.395  ,hs1, ihs	,hcm_r_type],
['HBM1D6R ', 'HBP1D6R:rdbk ', 'HBP1D6R:set ', 1, [11,02], 49, 144.39   ,hbm, ihbm	,hcm_b_type],
['HS4M1D6R', 'HS4P1D6R:rdbk', 'HS4P1D6R:set', 1, [11,03], 50, 147.034  ,hs4, ihs	,hcm_r_type],
['HS4M2D6R', 'HS4P2D6R:rdbk', 'HS4P2D6R:set', 1, [11,04], 51, 152.806  ,hs4, ihs	,hcm_r_type],
['HBM2D6R ', 'HBP2D6R:rdbk ', 'HBP2D6R:set ', 1, [11,05], 52, 154.755  ,hbm, ihbm	,hcm_b_type],
['HS1MT6R ', 'HS1PT6R:rdbk ', 'HS1PT6R:set ', 1, [12,01], 53, 157.395  ,hs1, ihs	,hcm_r_type],
['HBM1T6R ', 'HBP1T6R:rdbk ', 'HBP1T6R:set ', 1, [12,02], 54, 159.39   ,hbm, ihbm	,hcm_b_type],
['HS4M1T6R', 'HS4P1T6R:rdbk', 'HS4P1T6R:set', 1, [12,03], 55, 162.034  ,hs4, ihs	,hcm_r_type],
['HS4M2T6R', 'HS4P2T6R:rdbk', 'HS4P2T6R:set', 1, [12,04], 56, 167.806  ,hs4, ihs	,hcm_r_type],
['HBM2T6R ', 'HBP2T6R:rdbk ', 'HBP2T6R:set ', 1, [12,05], 57, 169.755  ,hbm, ihbm	,hcm_b_type],
['HS1MD7R ', 'HS1PD7R:rdbk ', 'HS1PD7R:set ', 1, [13,01], 58, 172.395  ,hs1, ihs	,hcm_r_type],
['HBM1D7R ', 'HBP1D7R:rdbk ', 'HBP1D7R:set ', 1, [13,02], 59, 174.39   ,hbm, ihbm	,hcm_b_type],
['HS4M1D7R', 'HS4P1D7R:rdbk', 'HS4P1D7R:set', 1, [13,03], 60, 177.034  ,hs4, ihs	,hcm_r_type],
['HS4M2D7R', 'HS4P2D7R:rdbk', 'HS4P2D7R:set', 1, [13,04], 61, 182.806  ,hs4, ihs	,hcm_r_type],
['HBM2D7R ', 'HBP2D7R:rdbk ', 'HBP2D7R:set ', 1, [13,05], 62, 184.755  ,hbm, ihbm	,hcm_b_type],
['HS1MT7R ', 'HS1PT7R:rdbk ', 'HS1PT7R:set ', 1, [14,01], 63, 187.395  ,hs1, ihs	,hcm_r_type],
['HBM1T7R ', 'HBP1T7R:rdbk ', 'HBP1T7R:set ', 1, [14,02], 64, 189.39   ,hbm, ihbm	,hcm_b_type],
['HS4M1T7R', 'HS4P1T7R:rdbk', 'HS4P1T7R:set', 1, [14,03], 65, 192.034  ,hs4, ihs	,hcm_w_type],
['HS4M2T7R', 'HS4P2T7R:rdbk', 'HS4P2T7R:set', 1, [14,04], 66, 197.806  ,hs4, ihs	,hcm_r_type],
['HBM2T7R ', 'HBP2T7R:rdbk ', 'HBP2T7R:set ', 1, [14,05], 67, 199.755  ,hbm, ihbm	,hcm_b_type],
['HS1MD8R ', 'HS1PD8R:rdbk ', 'HS1PD8R:set ', 1, [15,01], 68, 202.395  ,hs1, ihs	,hcm_r_type],
['HBM1D8R ', 'HBP1D8R:rdbk ', 'HBP1D8R:set ', 1, [15,02], 69, 204.39   ,hbm, ihbm	,hcm_b_type],
['HS4M1D8R', 'HS4P1D8R:rdbk', 'HS4P1D8R:set', 1, [15,03], 70, 207.034  ,hs4, ihs	,hcm_r_type],
['HS4M2D8R', 'HS4P2D8R:rdbk', 'HS4P2D8R:set', 1, [15,04], 71, 212.806  ,hs4, ihs	,hcm_r_type],
['HBM2D8R ', 'HBP2D8R:rdbk ', 'HBP2D8R:set ', 1, [15,05], 72, 214.755  ,hbm, ihbm 	,hcm_b_type],
['HS1MT8R ', 'HS1PT8R:rdbk ', 'HS1PT8R:set ', 1, [16,01], 73, 217.395  ,hs1, ihs	,hcm_r_type],
['HBM1T8R ', 'HBP1T8R:rdbk ', 'HBP1T8R:set ', 1, [16,02], 74, 219.39   ,hbm, ihbm	,hcm_b_type],
['HS4M1T8R', 'HS4P1T8R:rdbk', 'HS4P1T8R:set', 1, [16,03], 75, 222.034  ,hs4, ihs	,hcm_r_type],
['HS4M2T8R', 'HS4P2T8R:rdbk', 'HS4P2T8R:set', 1, [16,04], 76, 227.806  ,hs4, ihs	,hcm_r_type],
['HBM2T8R ', 'HBP2T8R:rdbk ', 'HBP2T8R:set ', 1, [16,05], 77, 229.755  ,hbm, ihbm	,hcm_b_type],
['HS1MD1R ', 'HS1PD1R:rdbk ', 'HS1PD1R:set ', 1, [01,01], 78, 232.395  ,hs1, ihs	,hcm_r_type],
['HBM1D1R ', 'HBP1D1R:rdbk ', 'HBP1D1R:set ', 1, [01,02], 79, 234.39   ,hbm, ihbm	,hcm_b_type],
['HS4M1D1R', 'HS4P1D1R:rdbk', 'HS4P1D1R:set', 1, [01,03], 80, 237.034  ,hs4, ihs	,hcm_r_type],
]
hcm = map(list,zip(*hcm))
ao['HCM'] = {}
ao['HCM']['CommonNames']                 = np.array(hcm[0])
ao['HCM']['Status']                      = np.array(hcm[3])
ao['HCM']['DeviceList']                = np.array(hcm[4])
ao['HCM']['Element']                     = np.array(hcm[5])
ao['HCM']['Pos']                         = np.array(hcm[6])
ao['HCM']['Monitor']                     = {}
ao['HCM']['Monitor']['Mode']             = mode
ao['HCM']['Monitor']['HWUnits']          = 'ampere'
ao['HCM']['Monitor']['PhysicalUnits']    = 'radian'
ao['HCM']['Setpoint'] = deepcopy(ao['HCM']['Monitor'])
ao['HCM']['Monitor']['ChannelNames']     = np.array(hcm[1])
ao['HCM']['Setpoint']['ChannelNames']    = np.array(hcm[2])

vs2 = 0.00297607;
vs3 = 0.00297607;
ivs = 0.07/2; #Nutzer Optik 14.06.10
vcm_r_type = 'rohrer';
vcm_w_type = 'wme   ';
vcm = [
['VS3M2D1R', 'VS3P2D1R:rdbk', 'VS3P2D1R:set', 1, [ 1, 3],   1, 3.772    ,vs3  , ivs   , vcm_r_type],
['VS2M2D1R', 'VS2P2D1R:rdbk', 'VS2P2D1R:set', 1, [ 1, 4],   2, 6.537    ,vs2  , ivs   , vcm_r_type],
['VS2M1T1R', 'VS2P1T1R:rdbk', 'VS2P1T1R:set', 1, [ 2, 1],   3, 8.303    ,vs2  , ivs   , vcm_r_type],
['VS3M1T1R', 'VS3P1T1R:rdbk', 'VS3P1T1R:set', 1, [ 2, 2],   4, 11.068   ,vs3  , ivs   , vcm_r_type],
['VS3M2T1R', 'VS3P2T1R:rdbk', 'VS3P2T1R:set', 1, [ 2, 3],   5, 18.772   ,vs3  , ivs   , vcm_r_type],
['VS2M2T1R', 'VS2P2T1R:rdbk', 'VS2P2T1R:set', 1, [ 2, 4],   6, 21.537   ,vs2  , ivs   , vcm_r_type],
['VS2M1D2R', 'VS2P1D2R:rdbk', 'VS2P1D2R:set', 1, [ 3, 1],   7, 23.303   ,vs2  , ivs   , vcm_r_type],
['VS3M1D2R', 'VS3P1D2R:rdbk', 'VS3P1D2R:set', 1, [ 3, 2],   8, 26.068   ,vs3  , ivs   , vcm_r_type],
['VS3M2D2R', 'VS3P2D2R:rdbk', 'VS3P2D2R:set', 1, [ 3, 3],   9, 33.772   ,vs3  , ivs   , vcm_r_type],
['VS2M2D2R', 'VS2P2D2R:rdbk', 'VS2P2D2R:set', 1, [ 3, 4],  10, 36.537   ,vs2  , ivs   , vcm_r_type],
['VS2M1T2R', 'VS2P1T2R:rdbk', 'VS2P1T2R:set', 1, [ 4, 1],  11, 38.303   ,vs2  , ivs   , vcm_r_type],
['VS3M1T2R', 'VS3P1T2R:rdbk', 'VS3P1T2R:set', 1, [ 4, 2],  12, 41.068   ,vs3  , ivs   , vcm_r_type],
['VS3M2T2R', 'VS3P2T2R:rdbk', 'VS3P2T2R:set', 1, [ 4, 3],  13, 48.772   ,vs3  , ivs   , vcm_r_type],
['VS2M2T2R', 'VS2P2T2R:rdbk', 'VS2P2T2R:set', 1, [ 4, 4],  14, 51.537   ,vs2  , ivs   , vcm_r_type],
['VS2M1D3R', 'VS2P1D3R:rdbk', 'VS2P1D3R:set', 1, [ 5, 1],  15, 53.303   ,vs2  , ivs   , vcm_r_type],
['VS3M1D3R', 'VS3P1D3R:rdbk', 'VS3P1D3R:set', 1, [ 5, 2],  16, 56.068   ,vs3  , ivs   , vcm_w_type],
['VS3M2D3R', 'VS3P2D3R:rdbk', 'VS3P2D3R:set', 1, [ 5, 3],  17, 63.772   ,vs3  , ivs   , vcm_r_type],
['VS2M2D3R', 'VS2P2D3R:rdbk', 'VS2P2D3R:set', 1, [ 5, 4],  18, 66.537   ,vs2  , ivs   , vcm_r_type],
['VS2M1T3R', 'VS2P1T3R:rdbk', 'VS2P1T3R:set', 1, [ 6, 1],  19, 68.303   ,vs2  , ivs   , vcm_r_type],
['VS3M1T3R', 'VS3P1T3R:rdbk', 'VS3P1T3R:set', 1, [ 6, 2],  20, 71.068   ,vs3  , ivs   , vcm_r_type],
['VS3M2T3R', 'VS3P2T3R:rdbk', 'VS3P2T3R:set', 1, [ 6, 3],  21, 78.772   ,vs3  , ivs   , vcm_r_type],
['VS2M2T3R', 'VS2P2T3R:rdbk', 'VS2P2T3R:set', 1, [ 6, 4],  22, 81.537   ,vs2  , ivs   , vcm_r_type],
['VS2M1D4R', 'VS2P1D4R:rdbk', 'VS2P1D4R:set', 1, [ 7, 1],  23, 83.303   ,vs2  , ivs   , vcm_r_type],
['VS3M1D4R', 'VS3P1D4R:rdbk', 'VS3P1D4R:set', 1, [ 7, 2],  24, 86.068   ,vs3  , ivs   , vcm_r_type],
['VS3M2D4R', 'VS3P2D4R:rdbk', 'VS3P2D4R:set', 1, [ 7, 3],  25, 93.772   ,vs3  , ivs   , vcm_r_type],
['VS2M2D4R', 'VS2P2D4R:rdbk', 'VS2P2D4R:set', 1, [ 7, 4],  26, 96.537   ,vs2  , ivs   , vcm_r_type],
['VS2M1T4R', 'VS2P1T4R:rdbk', 'VS2P1T4R:set', 1, [ 8, 1],  27, 98.303   ,vs2  , ivs   , vcm_r_type],
['VS3M1T4R', 'VS3P1T4R:rdbk', 'VS3P1T4R:set', 1, [ 8, 2],  28, 101.068  ,vs3  , ivs   , vcm_r_type],
['VS3M2T4R', 'VS3P2T4R:rdbk', 'VS3P2T4R:set', 1, [ 8, 3],  29, 108.772  ,vs3  , ivs   , vcm_r_type],
['VS2M2T4R', 'VS2P2T4R:rdbk', 'VS2P2T4R:set', 1, [ 8, 4],  30, 111.537  ,vs2  , ivs   , vcm_r_type],
['VS2M1D5R', 'VS2P1D5R:rdbk', 'VS2P1D5R:set', 1, [ 9, 1],  31, 113.303  ,vs2  , ivs   , vcm_r_type],
['VS3M1D5R', 'VS3P1D5R:rdbk', 'VS3P1D5R:set', 1, [ 9, 2],  32, 116.068  ,vs3  , ivs   , vcm_w_type],
['VS3M2D5R', 'VS3P2D5R:rdbk', 'VS3P2D5R:set', 1, [ 9, 3],  33, 123.772  ,vs3  , ivs   , vcm_r_type],
['VS2M2D5R', 'VS2P2D5R:rdbk', 'VS2P2D5R:set', 1, [ 9, 4],  34, 126.537  ,vs2  , ivs   , vcm_r_type],
['VS2M1T5R', 'VS2P1T5R:rdbk', 'VS2P1T5R:set', 1, [10, 1],  35, 128.303  ,vs2  , ivs   , vcm_r_type],
['VS3M1T5R', 'VS3P1T5R:rdbk', 'VS3P1T5R:set', 1, [10, 2],  36, 131.068  ,vs3  , ivs   , vcm_r_type],
['VS3M2T5R', 'VS3P2T5R:rdbk', 'VS3P2T5R:set', 1, [10, 3],  37, 138.772  ,vs3  , ivs   , vcm_r_type],
['VS2M2T5R', 'VS2P2T5R:rdbk', 'VS2P2T5R:set', 1, [10, 4],  38, 141.537  ,vs2  , ivs   , vcm_r_type],
['VS2M1D6R', 'VS2P1D6R:rdbk', 'VS2P1D6R:set', 1, [11, 1],  39, 143.303  ,vs2  , ivs   , vcm_r_type],
['VS3M1D6R', 'VS3P1D6R:rdbk', 'VS3P1D6R:set', 1, [11, 2],  40, 146.068  ,vs3  , ivs   , vcm_w_type],
['VS3M2D6R', 'VS3P2D6R:rdbk', 'VS3P2D6R:set', 1, [11, 3],  41, 153.772  ,vs3  , ivs   , vcm_r_type],
['VS2M2D6R', 'VS2P2D6R:rdbk', 'VS2P2D6R:set', 1, [11, 4],  42, 156.537  ,vs2  , ivs   , vcm_r_type],
['VS2M1T6R', 'VS2P1T6R:rdbk', 'VS2P1T6R:set', 1, [12, 1],  43, 158.303  ,vs2  , ivs   , vcm_r_type],
['VS3M1T6R', 'VS3P1T6R:rdbk', 'VS3P1T6R:set', 1, [12, 2],  44, 161.068  ,vs3  , ivs   , vcm_r_type],
['VS3M2T6R', 'VS3P2T6R:rdbk', 'VS3P2T6R:set', 1, [12, 3],  45, 168.772  ,vs3  , ivs   , vcm_r_type],
['VS2M2T6R', 'VS2P2T6R:rdbk', 'VS2P2T6R:set', 1, [12, 4],  46, 171.537  ,vs2  , ivs   , vcm_r_type],
['VS2M1D7R', 'VS2P1D7R:rdbk', 'VS2P1D7R:set', 1, [13, 1],  47, 173.303  ,vs2  , ivs   , vcm_r_type],
['VS3M1D7R', 'VS3P1D7R:rdbk', 'VS3P1D7R:set', 1, [13, 2],  48, 176.068  ,vs3  , ivs   , vcm_r_type],
['VS3M2D7R', 'VS3P2D7R:rdbk', 'VS3P2D7R:set', 1, [13, 3],  49, 183.772  ,vs3  , ivs   , vcm_r_type],
['VS2M2D7R', 'VS2P2D7R:rdbk', 'VS2P2D7R:set', 1, [13, 4],  50, 186.537  ,vs2  , ivs   , vcm_r_type],
['VS2M1T7R', 'VS2P1T7R:rdbk', 'VS2P1T7R:set', 1, [14, 1],  51, 188.303  ,vs2  , ivs   , vcm_r_type],
['VS3M1T7R', 'VS3P1T7R:rdbk', 'VS3P1T7R:set', 1, [14, 2],  52, 191.068  ,vs3  , ivs   , vcm_r_type],
['VS3M2T7R', 'VS3P2T7R:rdbk', 'VS3P2T7R:set', 1, [14, 3],  53, 198.772  ,vs3  , ivs   , vcm_r_type],
['VS2M2T7R', 'VS2P2T7R:rdbk', 'VS2P2T7R:set', 1, [14, 4],  54, 201.537  ,vs2  , ivs   , vcm_r_type],
['VS2M1D8R', 'VS2P1D8R:rdbk', 'VS2P1D8R:set', 1, [15, 1],  55, 203.303  ,vs2  , ivs   , vcm_r_type],
['VS3M1D8R', 'VS3P1D8R:rdbk', 'VS3P1D8R:set', 1, [15, 2],  56, 206.068  ,vs3  , ivs   , vcm_w_type],
['VS3M2D8R', 'VS3P2D8R:rdbk', 'VS3P2D8R:set', 1, [15, 3],  57, 213.772  ,vs3  , ivs   , vcm_r_type],
['VS2M2D8R', 'VS2P2D8R:rdbk', 'VS2P2D8R:set', 1, [15, 4],  58, 216.537  ,vs2  , ivs   , vcm_r_type],
['VS2M1T8R', 'VS2P1T8R:rdbk', 'VS2P1T8R:set', 1, [16, 1],  59, 218.303  ,vs2  , ivs   , vcm_r_type],
['VS3M1T8R', 'VS3P1T8R:rdbk', 'VS3P1T8R:set', 1, [16, 2],  60, 221.068  ,vs3  , ivs   , vcm_r_type],
['VS3M2T8R', 'VS3P2T8R:rdbk', 'VS3P2T8R:set', 1, [16, 3],  61, 228.772  ,vs3  , ivs   , vcm_r_type],
['VS2M2T8R', 'VS2P2T8R:rdbk', 'VS2P2T8R:set', 1, [16, 4],  62, 231.537  ,vs2  , ivs   , vcm_r_type],
['VS2M1D1R', 'VS2P1D1R:rdbk', 'VS2P1D1R:set', 1, [ 1, 1],  63, 233.303  ,vs2  , ivs   , vcm_r_type],
['VS3M1D1R', 'VS3P1D1R:rdbk', 'VS3P1D1R:set', 1, [ 1, 2],  64, 236.068  ,vs3  , ivs   , vcm_r_type],
]
vcm = map(list,zip(*vcm))
ao['VCM'] = {}
ao['VCM']['CommonNames']              = np.array(vcm[0])
ao['VCM']['Status']                   = np.array(vcm[3])
ao['VCM']['DeviceList']             = np.array(vcm[4])
ao['VCM']['Element']                  = np.array(vcm[5])
ao['VCM']['Pos']                      = np.array(vcm[6])
ao['VCM']['Monitor']                  = {}
ao['VCM']['Monitor']['Mode']          = mode
ao['VCM']['Monitor']['HWUnits']       = 'ampere'
ao['VCM']['Monitor']['PhysicalUnits'] = 'radian'
ao['VCM']['Setpoint'] = deepcopy(ao['VCM']['Monitor'])
ao['VCM']['Monitor']['ChannelNames']  = np.array(vcm[1])
ao['VCM']['Setpoint']['ChannelNames'] = np.array(vcm[2])


cqs=[
['CQS3M1T1R', 'CQS3P1T1R:rdbk', 'CQS3P1T1R:set', 1, [ 2, 1], 1 ,11.068 ,0.188],
['CQS3M2T1R', 'CQS3P2T1R:rdbk', 'CQS3P2T1R:set', 1, [ 2, 2], 2 ,18.772 ,0.188],
['CQS2M2D2R', 'CQS2P2D2R:rdbk', 'CQS2P2D2R:set', 1, [ 3, 1], 3 ,36.537 ,0.188],
['CQS3M1T2R', 'CQS3P1T2R:rdbk', 'CQS3P1T2R:set', 1, [ 4, 1], 4 ,41.068 ,0.188],
['CQS3M1T3R', 'CQS3P1T3R:rdbk', 'CQS3P1T3R:set', 1, [ 6, 1], 5 ,71.068 ,0.188],
['CQS3M2T3R', 'CQS3P2T3R:rdbk', 'CQS3P2T3R:set', 1, [ 6, 2], 6 ,78.772 ,0.188],
['CQS3M2T4R', 'CQS3P2T4R:rdbk', 'CQS3P2T4R:set', 1, [ 8, 1], 7 ,108.772,0.188], 
['CQS3M2D5R', 'CQS3P2D5R:rdbk', 'CQS3P2D5R:set', 1, [10, 1], 8 ,123.772,0.188],
['CQS2M2T5R', 'CQS2P2T5R:rdbk', 'CQS2P2T5R:set', 1, [11, 1], 9 ,141.537,0.188],
['CQS3M1D6R', 'CQS3P1D6R:rdbk', 'CQS3P1D6R:set', 1, [12, 1],10 ,146.068,0.188],
['CQS3M2D6R', 'CQS3P2D6R:rdbk', 'CQS3P2D6R:set', 1, [12, 2],11 ,153.772,0.188],
['CQS2M2D6R', 'CQS2P2D6R:rdbk', 'CQS2P2D6R:set', 1, [12, 3],12 ,156.537,0.188],
['CQS3M2T6R', 'CQS3P2T6R:rdbk', 'CQS3P2T6R:set', 1, [13, 1],13 ,168.772,0.188],
['CQS3M1T7R', 'CQS3P1T7R:rdbk', 'CQS3P1T7R:set', 1, [14, 1],14 ,191.068,0.188],
['CQS3M2T7R', 'CQS3P2T7R:rdbk', 'CQS3P2T7R:set', 1, [14, 2],15 ,198.772,0.188],
]
cqs = map(list,zip(*cqs))
ao['CQS'] = {}
ao['CQS']['CommonNames']              = np.array(cqs[0])
ao['CQS']['Status']                   = np.array(cqs[3])
ao['CQS']['DeviceList']             = np.array(cqs[4])
ao['CQS']['Element']                  = np.array(cqs[5])
ao['CQS']['Pos']                      = np.array(cqs[6])
ao['CQS']['Monitor']                  = {}
ao['CQS']['Monitor']['Mode']          = mode
ao['CQS']['Monitor']['HWUnits']       = 'ampere'
ao['CQS']['Monitor']['PhysicalUnits'] = 'radian'
ao['CQS']['Setpoint'] = deepcopy(ao['CQS']['Monitor'])
ao['CQS']['Monitor']['ChannelNames']  = np.array(cqs[1])
ao['CQS']['Setpoint']['ChannelNames'] = np.array(cqs[2])




quad1=[
['Q1M2D1R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [ 1, 2],        1,    6.985], 
['Q1M1T1R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [ 2, 1],        2,    7.765], 
['Q1M2T1R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [ 2, 2],        3,   21.985], 
['Q1M1D2R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [ 3, 1],        4,   22.765], 
['Q1M2D2R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [ 3, 2],        5,   36.985], 
['Q1M1T2R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [ 4, 1],        6,   37.765], 
['Q1M2T2R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [ 4, 2],        7,   51.985], 
['Q1M1D3R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [ 5, 1],        8,   52.765], 
['Q1M2D3R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [ 5, 2],        9,   66.985], 
['Q1M1T3R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [ 6, 1],        10,  67.765], 
['Q1M2T3R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [ 6, 2],        11,  81.985], 
['Q1M1D4R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [ 7, 1],        12,  82.765], 
['Q1M2D4R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [ 7, 2],        13,  96.985], 
['Q1M1T4R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [ 8, 1],        14,  97.765], 
['Q1M2T4R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [ 8, 2],        15, 111.985], 
['Q1M1D5R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [ 9, 1],        16, 112.765], 
['Q1M2D5R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [ 9, 2],        17, 126.985], 
['Q1M1T5R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [10, 1],        18, 127.765], 
['Q1M2T5R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [10, 2],        19, 141.985], 
['Q1M1D6R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [11, 1],        20, 142.765], 
['Q1M2D6R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [11, 2],        21, 156.985], 
['Q1M1T6R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [12, 1],        22, 157.765], 
['Q1M2T6R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [12, 2],        23, 171.985], 
['Q1M1D7R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [13, 1],        24, 172.765], 
['Q1M2D7R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [13, 2],        25, 186.985], 
['Q1M1T7R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [14, 1],        26, 187.765], 
['Q1M2T7R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [14, 2],        27, 201.985], 
['Q1M1D8R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [15, 1],        28, 202.765], 
['Q1M2D8R',     'Q1PDR:rdbk',   'Q1PDR:set',    1,      [15, 2],        29, 216.985], 
['Q1M1T8R',     'Q1PTR:rdbk',   'Q1PTR:set',    1,      [16, 1],        30, 217.765], 
['Q1M2T8R',     'Q1PTR:rdbk',   'Q1PTR:set',    0,      [16, 2],        31, 231.985], 
['Q1M1D1R',     'Q1PDR:rdbk',   'Q1PDR:set',    0,      [ 1, 1],        32, 232.765], 
]
quad1 = map(list,zip(*quad1))
ao['Q1'] = {}
ao['Q1']['CommonNames']              = np.array(quad1[0])
ao['Q1']['Status']                   = np.array(quad1[3])
ao['Q1']['DeviceList']             = np.array(quad1[4])
ao['Q1']['Element']                  = np.array(quad1[5])
ao['Q1']['Pos']                      = np.array(quad1[6])
ao['Q1']['Monitor']                  = {}
ao['Q1']['Monitor']['Mode']          = mode
ao['Q1']['Monitor']['HWUnits']       = 'ampere'
ao['Q1']['Monitor']['PhysicalUnits'] = 'meter^-2'
ao['Q1']['Setpoint'] = deepcopy(ao['Q1']['Monitor'])
ao['Q1']['Monitor']['ChannelNames']  = np.array(quad1[1])
ao['Q1']['Setpoint']['ChannelNames'] = np.array(quad1[2])

cq2t = -0.065656;
cq2d = -0.065656;
quad2=[
['Q2M2D1R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [ 1, 2],  1, 6.03   ,cq2d],
['Q2M1T1R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [ 2, 1],  2, 8.77   ,cq2t],
['Q2M2T1R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [ 2, 2],  3, 21.03  ,cq2t],
['Q2M1D2R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [ 3, 1],  4, 23.77  ,cq2d],
['Q2M2D2R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [ 3, 2],  5, 36.03  ,cq2d],
['Q2M1T2R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [ 4, 1],  6, 38.77  ,cq2t],
['Q2M2T2R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [ 4, 2],  7, 51.03  ,cq2t],
['Q2M1D3R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [ 5, 1],  8, 53.77  ,cq2d],
['Q2M2D3R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [ 5, 2],  9, 66.03  ,cq2d],
['Q2M1T3R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [ 6, 1], 10, 68.77  ,cq2t],
['Q2M2T3R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [ 6, 2], 11, 81.03  ,cq2t],
['Q2M1D4R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [ 7, 1], 12, 83.77  ,cq2d],
['Q2M2D4R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [ 7, 2], 13, 96.03  ,cq2d],
['Q2M1T4R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [ 8, 1], 14, 98.77  ,cq2t],
['Q2M2T4R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [ 8, 2], 15, 111.03 ,cq2t],
['Q2M1D5R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [ 9, 1], 16, 113.77 ,cq2d],
['Q2M2D5R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [ 9, 2], 17, 126.03 ,cq2d],
['Q2M1T5R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [10, 1], 18, 128.77 ,cq2t],
['Q2M2T5R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [10, 2], 19, 141.03 ,cq2t],
['Q2M1D6R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [11, 1], 20, 143.77 ,cq2d],
['Q2M2D6R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [11, 2], 21, 156.03 ,cq2d],
['Q2M1T6R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [12, 1], 22, 158.77 ,cq2t],
['Q2M2T6R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [12, 2], 23, 171.03 ,cq2t],
['Q2M1D7R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [13, 1], 24, 173.77 ,cq2d],
['Q2M2D7R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [13, 2], 25, 186.03 ,cq2d],
['Q2M1T7R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [14, 1], 26, 188.77 ,cq2t],
['Q2M2T7R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [14, 2], 27, 201.03 ,cq2t],
['Q2M1D8R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [15, 1], 28, 203.77 ,cq2d],
['Q2M2D8R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [15, 2], 29, 216.03 ,cq2d],
['Q2M1T8R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [16, 1], 30, 218.77 ,cq2t],
['Q2M2T8R', 'Q2PTR:rdbk', 'Q2PTR:set', 1, [16, 2], 31, 231.03 ,cq2t],
['Q2M1D1R', 'Q2PDR:rdbk', 'Q2PDR:set', 1, [01, 1], 32, 233.77 ,cq2d],
]
quad2 = map(list,zip(*quad2))
ao['Q2'] = {}
ao['Q2']['CommonNames']              = np.array(quad2[0])
ao['Q2']['Status']                   = np.array(quad2[3])
ao['Q2']['DeviceList']             = np.array(quad2[4])
ao['Q2']['Element']                  = np.array(quad2[5])
ao['Q2']['Pos']                      = np.array(quad2[6])
ao['Q2']['Monitor']                  = {}
ao['Q2']['Monitor']['Mode']          = mode
ao['Q1']['Monitor']['HWUnits']       = 'ampere'
ao['Q2']['Monitor']['PhysicalUnits'] = 'meter^-2'
ao['Q2']['Setpoint'] = deepcopy(ao['Q2']['Monitor'])
ao['Q2']['Monitor']['ChannelNames']  = np.array(quad2[1])
ao['Q2']['Setpoint']['ChannelNames'] = np.array(quad2[2])


cq3t = -0.062940;
cq3d = -0.063430;
quad3=[
['Q3M2D1R', 'Q3PD1R:rdbk ', 'Q3PD1R:set ', 1, [ 1, 2],  1, 4.085     , cq3d],
['Q3M1T1R', 'Q3P1T1R:rdbk', 'Q3P1T1R:set', 1, [ 2, 1],  2, 10.665    , cq3t],
['Q3M2T1R', 'Q3P2T1R:rdbk', 'Q3P2T1R:set', 1, [ 2, 2],  3, 19.085    , cq3t],
['Q3M1D2R', 'Q3PD2R:rdbk ', 'Q3PD2R:set ', 1, [ 3, 1],  4, 25.665    , cq3d],
['Q3M2D2R', 'Q3PD2R:rdbk ', 'Q3PD2R:set ', 1, [ 3, 2],  5, 34.085    , cq3d],
['Q3M1T2R', 'Q3PT2R:rdbk ', 'Q3PT2R:set ', 1, [ 4, 1],  6, 40.665    , cq3t],
['Q3M2T2R', 'Q3PT2R:rdbk ', 'Q3PT2R:set ', 1, [ 4, 2],  7, 49.085    , cq3t],
['Q3M1D3R', 'Q3PD3R:rdbk ', 'Q3PD3R:set ', 1, [ 5, 1],  8, 55.665    , cq3d],
['Q3M2D3R', 'Q3PD3R:rdbk ', 'Q3PD3R:set ', 1, [ 5, 2],  9, 64.085    , cq3d],
['Q3M1T3R', 'Q3PT3R:rdbk ', 'Q3PT3R:set ', 1, [ 6, 1], 10, 70.665    , cq3t],
['Q3M2T3R', 'Q3PT3R:rdbk ', 'Q3PT3R:set ', 1, [ 6, 2], 11, 79.085    , cq3t],
['Q3M1D4R', 'Q3PD4R:rdbk ', 'Q3PD4R:set ', 1, [ 7, 1], 12, 85.665    , cq3d],
['Q3M2D4R', 'Q3PD4R:rdbk ', 'Q3PD4R:set ', 1, [ 7, 2], 13, 94.085    , cq3d],
['Q3M1T4R', 'Q3PT4R:rdbk ', 'Q3PT4R:set ', 1, [ 8, 1], 14, 100.665   , cq3t],
['Q3M2T4R', 'Q3PT4R:rdbk ', 'Q3PT4R:set ', 1, [ 8, 2], 15, 109.085   , cq3t],
['Q3M1D5R', 'Q3PD5R:rdbk ', 'Q3PD5R:set ', 1, [ 9, 1], 16, 115.665   , cq3d],
['Q3M2D5R', 'Q3PD5R:rdbk ', 'Q3PD5R:set ', 1, [ 9, 2], 17, 124.085   , cq3d],
['Q3M1T5R', 'Q3PT5R:rdbk ', 'Q3PT5R:set ', 1, [10, 1], 18, 130.665   , cq3t],
['Q3M2T5R', 'Q3PT5R:rdbk ', 'Q3PT5R:set ', 1, [10, 2], 19, 139.085   , cq3t],
['Q3M1D6R', 'Q3PD6R:rdbk ', 'Q3PD6R:set ', 1, [11, 1], 20, 145.665   , cq3d],
['Q3M2D6R', 'Q3PD6R:rdbk ', 'Q3PD6R:set ', 1, [11, 2], 21, 154.085   , cq3d],
['Q3M1T6R', 'Q3P1T6R:rdbk', 'Q3P1T6R:set', 1, [12, 1], 22, 160.665   , cq3t],
['Q3M2T6R', 'Q3P2T6R:rdbk', 'Q3P2T6R:set', 1, [12, 2], 23, 169.085   , cq3t],
['Q3M1D7R', 'Q3PD7R:rdbk ', 'Q3PD7R:set ', 1, [13, 1], 24, 175.665   , cq3d],
['Q3M2D7R', 'Q3PD7R:rdbk ', 'Q3PD7R:set ', 1, [13, 2], 25, 184.085   , cq3d],
['Q3M1T7R', 'Q3PT7R:rdbk ', 'Q3PT7R:set ', 1, [14, 1], 26, 190.665   , cq3t],
['Q3M2T7R', 'Q3PT7R:rdbk ', 'Q3PT7R:set ', 1, [14, 2], 27, 199.085   , cq3t],
['Q3M1D8R', 'Q3PD8R:rdbk ', 'Q3PD8R:set ', 1, [15, 1], 28, 205.665   , cq3d],
['Q3M2D8R', 'Q3PD8R:rdbk ', 'Q3PD8R:set ', 1, [15, 2], 29, 214.085   , cq3d],
['Q3M1T8R', 'Q3P1T8R:rdbk', 'Q3P1T8R:set', 1, [16, 1], 30, 220.665   , cq3t],
['Q3M2T8R', 'Q3P2T8R:rdbk', 'Q3P2T8R:set', 1, [16, 2], 31, 229.085   , cq3t],
['Q3M1D1R', 'Q3PD1R:rdbk ', 'Q3PD1R:set ', 1, [01, 1], 32, 235.665   , cq3d],
]
quad3 = map(list,zip(*quad3))
ao['Q3'] = {}
ao['Q3']['CommonNames']              = np.array(quad3[0])
ao['Q3']['Status']                   = np.array(quad3[3])
ao['Q3']['DeviceList']             = np.array(quad3[4])
ao['Q3']['Element']                  = np.array(quad3[5])
ao['Q3']['Pos']                      = np.array(quad3[6])
ao['Q3']['Monitor']                  = {}
ao['Q3']['Monitor']['Mode']          = mode
ao['Q3']['Monitor']['HWUnits']       = 'ampere'
ao['Q3']['Monitor']['PhysicalUnits'] = 'meter^-2'
ao['Q3']['Setpoint'] = deepcopy(ao['Q3']['Monitor'])
ao['Q3']['Monitor']['ChannelNames']  = np.array(quad3[1])
ao['Q3']['Setpoint']['ChannelNames'] = np.array(quad3[2])

cq4t = 0.059339;
cq4d = 0.060633;
quad4=[
['Q4M2D1R', 'Q4PD1R:rdbk ', 'Q4PD1R:set ', 1, [ 1, 2],   1, 3.119  , cq4d],
['Q4M1T1R', 'Q4P1T1R:rdbk', 'Q4P1T1R:set', 1, [ 2, 1],   2, 11.381 , cq4t],
['Q4M2T1R', 'Q4P2T1R:rdbk', 'Q4P2T1R:set', 1, [ 2, 2],   3, 18.119 , cq4t],
['Q4M1D2R', 'Q4PD2R:rdbk ', 'Q4PD2R:set ', 1, [ 3, 1],   4, 26.381 , cq4d],
['Q4M2D2R', 'Q4PD2R:rdbk ', 'Q4PD2R:set ', 1, [ 3, 2],   5, 33.119 , cq4d],
['Q4M1T2R', 'Q4PT2R:rdbk ', 'Q4PT2R:set ', 1, [ 4, 1],   6, 41.381 , cq4t],
['Q4M2T2R', 'Q4PT2R:rdbk ', 'Q4PT2R:set ', 1, [ 4, 2],   7, 48.119 , cq4t],
['Q4M1D3R', 'Q4PD3R:rdbk ', 'Q4PD3R:set ', 1, [ 5, 1],   8, 56.381 , cq4d],
['Q4M2D3R', 'Q4PD3R:rdbk ', 'Q4PD3R:set ', 1, [ 5, 2],   9, 63.119 , cq4d],
['Q4M1T3R', 'Q4PT3R:rdbk ', 'Q4PT3R:set ', 1, [ 6, 1],  10, 71.381 , cq4t],
['Q4M2T3R', 'Q4PT3R:rdbk ', 'Q4PT3R:set ', 1, [ 6, 2],  11, 78.119 , cq4t],
['Q4M1D4R', 'Q4PD4R:rdbk ', 'Q4PD4R:set ', 1, [ 7, 1],  12, 86.381 , cq4d],
['Q4M2D4R', 'Q4PD4R:rdbk ', 'Q4PD4R:set ', 1, [ 7, 2],  13, 93.119 , cq4d],
['Q4M1T4R', 'Q4PT4R:rdbk ', 'Q4PT4R:set ', 1, [ 8, 1],  14, 101.381, cq4t],
['Q4M2T4R', 'Q4PT4R:rdbk ', 'Q4PT4R:set ', 1, [ 8, 2],  15, 108.119, cq4t],
['Q4M1D5R', 'Q4PD5R:rdbk ', 'Q4PD5R:set ', 1, [ 9, 1],  16, 116.381, cq4d],
['Q4M2D5R', 'Q4PD5R:rdbk ', 'Q4PD5R:set ', 1, [ 9, 2],  17, 123.119, cq4d],
['Q4M1T5R', 'Q4PT5R:rdbk ', 'Q4PT5R:set ', 1, [10, 1],  18, 131.381, cq4t],
['Q4M2T5R', 'Q4PT5R:rdbk ', 'Q4PT5R:set ', 1, [10, 2],  19, 138.119, cq4t],
['Q4M1D6R', 'Q4PD6R:rdbk ', 'Q4PD6R:set ', 1, [11, 1],  20, 146.381, cq4d],
['Q4M2D6R', 'Q4PD6R:rdbk ', 'Q4PD6R:set ', 1, [11, 2],  21, 153.119, cq4d],
['Q4M1T6R', 'Q4P1T6R:rdbk', 'Q4P1T6R:set', 1, [12, 1],  22, 161.381, cq4t],
['Q4M2T6R', 'Q4P2T6R:rdbk', 'Q4P2T6R:set', 1, [12, 2],  23, 168.119, cq4t],
['Q4M1D7R', 'Q4PD7R:rdbk ', 'Q4PD7R:set ', 1, [13, 1],  24, 176.381, cq4d],
['Q4M2D7R', 'Q4PD7R:rdbk ', 'Q4PD7R:set ', 1, [13, 2],  25, 183.119, cq4d],
['Q4M1T7R', 'Q4PT7R:rdbk ', 'Q4PT7R:set ', 1, [14, 1],  26, 191.381, cq4t],
['Q4M2T7R', 'Q4PT7R:rdbk ', 'Q4PT7R:set ', 1, [14, 2],  27, 198.119, cq4t],
['Q4M1D8R', 'Q4PD8R:rdbk ', 'Q4PD8R:set ', 1, [15, 1],  28, 206.381, cq4d],
['Q4M2D8R', 'Q4PD8R:rdbk ', 'Q4PD8R:set ', 1, [15, 2],  29, 213.119, cq4d],
['Q4M1T8R', 'Q4P1T8R:rdbk', 'Q4P1T8R:set', 1, [16, 1],  30, 221.381, cq4t],
['Q4M2T8R', 'Q4P2T8R:rdbk', 'Q4P2T8R:set', 1, [16, 2],  31, 228.119, cq4t],
['Q4M1D1R', 'Q4PD1R:rdbk ', 'Q4PD1R:set ', 1, [01, 1],  32, 236.381, cq4d],
]
quad4 = map(list,zip(*quad4))
ao['Q4'] = {}
ao['Q4']['CommonNames']              = np.array(quad4[0])
ao['Q4']['Status']                   = np.array(quad4[3])
ao['Q4']['DeviceList']             = np.array(quad4[4])
ao['Q4']['Element']                  = np.array(quad4[5])
ao['Q4']['Pos']                      = np.array(quad4[6])
ao['Q4']['Monitor']                  = {}
ao['Q4']['Monitor']['Mode']          = mode
ao['Q4']['Monitor']['HWUnits']       = 'ampere'
ao['Q4']['Monitor']['PhysicalUnits'] = 'meter^-2'
ao['Q4']['Setpoint'] = deepcopy(ao['Q4']['Monitor'])
ao['Q4']['Monitor']['ChannelNames']  = np.array(quad4[1])
ao['Q4']['Setpoint']['ChannelNames'] = np.array(quad4[2])

cq5 =  -0.064795;
quad5=[
['Q5M1T1R', 'Q5P1T1R:rdbk', 'Q5P1T1R:set', 1, [ 2, 2],  1, 12.347   , cq5 ],
['Q5M2T1R', 'Q5P2T1R:rdbk', 'Q5P2T1R:set', 1, [ 2, 1],  2, 17.453   , cq5 ],
['Q5M1T2R', 'Q5PT2R:rdbk ', 'Q5PT2R:set ', 1, [ 4, 2],  3, 42.347   , cq5 ],
['Q5M2T2R', 'Q5PT2R:rdbk ', 'Q5PT2R:set ', 1, [ 4, 1],  4, 47.453   , cq5 ],
['Q5M1T3R', 'Q5PT3R:rdbk ', 'Q5PT3R:set ', 1, [ 6, 2],  5, 72.347   , cq5 ],
['Q5M2T3R', 'Q5PT3R:rdbk ', 'Q5PT3R:set ', 1, [ 6, 1],  6, 77.453   , cq5 ],
['Q5M1T4R', 'Q5PT4R:rdbk ', 'Q5PT4R:set ', 1, [ 8, 2],  7, 102.347  , cq5 ],
['Q5M2T4R', 'Q5PT4R:rdbk ', 'Q5PT4R:set ', 1, [ 8, 1],  8, 107.453  , cq5 ],
['Q5M1T5R', 'Q5PT5R:rdbk ', 'Q5PT5R:set ', 1, [10, 2],  9, 132.347  , cq5 ],
['Q5M2T5R', 'Q5PT5R:rdbk ', 'Q5PT5R:set ', 1, [10, 1], 10, 137.453  , cq5 ],
['Q5M1T6R', 'Q5P1T6R:rdbk', 'Q5P1T6R:set', 1, [12, 2], 11, 162.347  , cq5 ],
['Q5M2T6R', 'Q5P2T6R:rdbk', 'Q5P2T6R:set', 1, [12, 1], 12, 167.453  , cq5 ],
['Q5M1T7R', 'Q5PT7R:rdbk ', 'Q5PT7R:set ', 1, [14, 2], 13, 192.347  , cq5 ],
['Q5M2T7R', 'Q5PT7R:rdbk ', 'Q5PT7R:set ', 1, [14, 1], 14, 197.453  , cq5 ],
['Q5M1T8R', 'Q5P1T8R:rdbk', 'Q5P1T8R:set', 1, [16, 2], 15, 222.347  , cq5 ],
['Q5M2T8R', 'Q5P2T8R:rdbk', 'Q5P2T8R:set', 1, [16, 1], 16, 227.453  , cq5 ],
]
quad5 = map(list,zip(*quad5))
ao['Q5'] = {}
ao['Q5']['CommonNames']             = np.array(quad5[0])
ao['Q5']['Status']                   = np.array(quad5[3])
ao['Q5']['DeviceList']             = np.array(quad5[4])
ao['Q5']['Element']                  = np.array(quad5[5])
ao['Q5']['Pos']                      = np.array(quad5[6])
ao['Q5']['Monitor']                  = {}
ao['Q5']['Monitor']['Mode']          = mode
ao['Q5']['Monitor']['HWUnits']       = 'ampere'
ao['Q5']['Monitor']['PhysicalUnits'] = 'meter^-2'
ao['Q5']['Setpoint'] = deepcopy(ao['Q5']['Monitor'])
ao['Q5']['Monitor']['ChannelNames']  = np.array(quad5[1])
ao['Q5']['Setpoint']['ChannelNames'] = np.array(quad5[2])

cs1 = .318756;
sext1=[
['S1MT1R ', 'S1PR:rdbk', 'S1PR:set', 1, [ 2, 1], 7.395   , cs1],
['S1MD2R ', 'S1PR:rdbk', 'S1PR:set', 1, [ 3, 1], 22.395  , cs1],
['S1MT2R ', 'S1PR:rdbk', 'S1PR:set', 1, [ 4, 1], 37.395  , cs1],
['S1MD3R ', 'S1PR:rdbk', 'S1PR:set', 1, [ 5, 1], 52.395  , cs1],
['S1MT3R ', 'S1PR:rdbk', 'S1PR:set', 1, [ 6, 1], 67.395  , cs1],
['S1MD4R ', 'S1PR:rdbk', 'S1PR:set', 1, [ 7, 1], 82.395  , cs1],
['S1MT4R ', 'S1PR:rdbk', 'S1PR:set', 1, [ 8, 1], 97.395  , cs1],
['S1MD5R ', 'S1PR:rdbk', 'S1PR:set', 1, [ 9, 1], 112.395 , cs1],
['S1MT5R ', 'S1PR:rdbk', 'S1PR:set', 1, [10, 1], 127.395 , cs1],
['S1MD6R ', 'S1PR:rdbk', 'S1PR:set', 1, [11, 1], 142.395 , cs1],
['S1MT6R ', 'S1PR:rdbk', 'S1PR:set', 1, [12, 1], 157.395 , cs1],
['S1MD7R ', 'S1PR:rdbk', 'S1PR:set', 1, [13, 1], 172.395 , cs1],
['S1MT7R ', 'S1PR:rdbk', 'S1PR:set', 1, [14, 1], 187.395 , cs1],
['S1MD8R ', 'S1PR:rdbk', 'S1PR:set', 1, [15, 1], 202.395 , cs1],
['S1MT8R ', 'S1PR:rdbk', 'S1PR:set', 1, [16, 1], 217.395 , cs1],
['S1MD1R ', 'S1PR:rdbk', 'S1PR:set', 1, [01, 1], 232.395 , cs1],
]
sext1 = map(list,zip(*sext1))
ao['S1'] = {}
ao['S1']['CommonNames']              = np.array(sext1[0])
ao['S1']['Status']                   = np.array(sext1[3])
ao['S1']['DeviceList']             = np.array(sext1[4])
ao['S1']['Element']                  = np.array(sext1[5])
ao['S1']['Pos']                      = np.array(sext1[6])
ao['S1']['Monitor']                  = {}
ao['S1']['Monitor']['Mode']          = mode
ao['S1']['Monitor']['HWUnits']       = 'ampere'
ao['S1']['Monitor']['PhysicalUnits'] = 'meter^-3'
ao['S1']['Setpoint'] = deepcopy(ao['S1']['Monitor'])
ao['S1']['Monitor']['ChannelNames']  = np.array(sext1[1])
ao['S1']['Setpoint']['ChannelNames'] = np.array(sext1[2])

cs2 = -.251049;
sext2=[
['S2M2D1R', 'S2PDR:rdbk',  'S2PDR:set', 1, [ 1, 2], 6.537   ,cs2],
['S2M1T1R', 'S2PTR:rdbk',  'S2PTR:set', 1, [ 2, 1], 8.303   ,cs2],
['S2M2T1R', 'S2PTR:rdbk',  'S2PTR:set', 1, [ 2, 2], 21.537  ,cs2],
['S2M1D2R', 'S2PDR:rdbk',  'S2PDR:set', 1, [ 3, 1], 23.303  ,cs2],
['S2M2D2R', 'S2PDR:rdbk',  'S2PDR:set', 1, [ 3, 2], 36.537  ,cs2],
['S2M1T2R', 'S2PTR:rdbk',  'S2PTR:set', 1, [ 4, 1], 38.303  ,cs2],
['S2M2T2R', 'S2PTR:rdbk',  'S2PTR:set', 1, [ 4, 2], 51.537  ,cs2],
['S2M1D3R', 'S2PDR:rdbk',  'S2PDR:set', 1, [ 5, 1], 53.303  ,cs2],
['S2M2D3R', 'S2PDR:rdbk',  'S2PDR:set', 1, [ 5, 2], 66.537  ,cs2],
['S2M1T3R', 'S2PTR:rdbk',  'S2PTR:set', 1, [ 6, 1], 68.303  ,cs2],
['S2M2T3R', 'S2PTR:rdbk',  'S2PTR:set', 1, [ 6, 2], 81.537  ,cs2],
['S2M1D4R', 'S2PDR:rdbk',  'S2PDR:set', 1, [ 7, 1], 83.303  ,cs2],
['S2M2D4R', 'S2PDR:rdbk',  'S2PDR:set', 1, [ 7, 2], 96.537  ,cs2],
['S2M1T4R', 'S2PTR:rdbk',  'S2PTR:set', 1, [ 8, 1], 98.303  ,cs2],
['S2M2T4R', 'S2PTR:rdbk',  'S2PTR:set', 1, [ 8, 2], 111.537 ,cs2],
['S2M1D5R', 'S2PDR:rdbk',  'S2PDR:set', 1, [ 9, 1], 113.303 ,cs2],
['S2M2D5R', 'S2PDR:rdbk',  'S2PDR:set', 1, [ 9, 2], 126.537 ,cs2],
['S2M1T5R', 'S2PTR:rdbk',  'S2PTR:set', 1, [10, 1], 128.303 ,cs2],
['S2M2T5R', 'S2PTR:rdbk',  'S2PTR:set', 1, [10, 2], 141.537 ,cs2],
['S2M1D6R', 'S2PDR:rdbk',  'S2PDR:set', 1, [11, 1], 143.303 ,cs2],
['S2M2D6R', 'S2PDR:rdbk',  'S2PDR:set', 1, [11, 2], 156.537 ,cs2],
['S2M1T6R', 'S2PTR:rdbk',  'S2PTR:set', 1, [12, 1], 158.303 ,cs2],
['S2M2T6R', 'S2PTR:rdbk',  'S2PTR:set', 1, [12, 2], 171.537 ,cs2],
['S2M1D7R', 'S2PDR:rdbk',  'S2PDR:set', 1, [13, 1], 173.303 ,cs2],
['S2M2D7R', 'S2PDR:rdbk',  'S2PDR:set', 1, [13, 2], 186.537 ,cs2],
['S2M1T7R', 'S2PTR:rdbk',  'S2PTR:set', 1, [14, 1], 188.303 ,cs2],
['S2M2T7R', 'S2PTR:rdbk',  'S2PTR:set', 1, [14, 2], 201.537 ,cs2],
['S2M1D8R', 'S2PDR:rdbk',  'S2PDR:set', 1, [15, 1], 203.303 ,cs2],
['S2M2D8R', 'S2PDR:rdbk',  'S2PDR:set', 1, [15, 2], 216.537 ,cs2],
['S2M1T8R', 'S2PTR:rdbk',  'S2PTR:set', 1, [16, 1], 218.303 ,cs2],
['S2M2T8R', 'S2PTR:rdbk',  'S2PTR:set', 1, [16, 2], 231.537 ,cs2],
['S2M1D1R', 'S2PDR:rdbk',  'S2PDR:set', 1, [01, 1], 233.303 ,cs2],
]
sext2 = map(list,zip(*sext2))
ao['S2'] = {}
ao['S2']['CommonNames']              = np.array(sext2[0])
ao['S2']['Status']                   = np.array(sext2[3])
ao['S2']['DeviceList']             = np.array(sext2[4])
ao['S2']['Element']                  = np.array(sext2[5])
ao['S2']['Pos']                      = np.array(sext2[6])
ao['S2']['Monitor']                  = {}
ao['S2']['Monitor']['Mode']          = mode
ao['S2']['Monitor']['HWUnits']       = 'ampere'
ao['S2']['Monitor']['PhysicalUnits'] = 'meter^-3'
ao['S2']['Setpoint'] = deepcopy(ao['S2']['Monitor'])
ao['S2']['Monitor']['ChannelNames']  = np.array(sext2[1])
ao['S2']['Setpoint']['ChannelNames'] = np.array(sext2[2])

cs3t = -0.250245;
cs3d = -0.251652;
sext3=[
['S3M2D1R', 'S3PD1R:rdbk', 'S3PD1R:set', 1, [ 1, 2], 3.772   ,cs3d],
['S3M1T1R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [ 2, 1], 11.068  ,cs3t],
['S3M2T1R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [ 2, 2], 18.772  ,cs3t],
['S3M1D2R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [ 3, 1], 26.068  ,cs3d],
['S3M2D2R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [ 3, 2], 33.772  ,cs3d],
['S3M1T2R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [ 4, 1], 41.068  ,cs3t],
['S3M2T2R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [ 4, 2], 48.772  ,cs3t],
['S3M1D3R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [ 5, 1], 56.068  ,cs3d],
['S3M2D3R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [ 5, 2], 63.772  ,cs3d],
['S3M1T3R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [ 6, 1], 71.068  ,cs3t],
['S3M2T3R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [ 6, 2], 78.772  ,cs3t],
['S3M1D4R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [ 7, 1], 86.068  ,cs3d],
['S3M2D4R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [ 7, 2], 93.772  ,cs3d],
['S3M1T4R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [ 8, 1], 101.068 ,cs3t],
['S3M2T4R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [ 8, 2], 108.772 ,cs3t],
['S3M1D5R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [ 9, 1], 116.068 ,cs3d],
['S3M2D5R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [ 9, 2], 123.772 ,cs3d],
['S3M1T5R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [10, 1], 131.068 ,cs3t],
['S3M2T5R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [10, 2], 138.772 ,cs3t],
['S3M1D6R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [11, 1], 146.068 ,cs3d],
['S3M2D6R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [11, 2], 153.772 ,cs3d],
['S3M1T6R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [12, 1], 161.068 ,cs3t],
['S3M2T6R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [12, 2], 168.772 ,cs3t],
['S3M1D7R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [13, 1], 176.068 ,cs3d],
['S3M2D7R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [13, 2], 183.772 ,cs3d],
['S3M1T7R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [14, 1], 191.068 ,cs3t],
['S3M2T7R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [14, 2], 198.772 ,cs3t],
['S3M1D8R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [15, 1], 206.068 ,cs3d],
['S3M2D8R', 'S3PDR:rdbk ', 'S3PDR:set ', 1, [15, 2], 213.772 ,cs3d],
['S3M1T8R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [16, 1], 221.068 ,cs3t],
['S3M2T8R', 'S3PTR:rdbk ', 'S3PTR:set ', 1, [16, 2], 228.772 ,cs3t],
['S3M1D1R', 'S3PD1R:rdbk', 'S3PD1R:set', 1, [01, 1], 236.068 ,cs3d],
]
sext3 = map(list,zip(*sext3))
ao['S3'] = {}
ao['S3']['CommonNames']              = np.array(sext3[0])
ao['S3']['Status']                   = np.array(sext3[3])
ao['S3']['DeviceList']             = np.array(sext3[4])
ao['S3']['Element']                  = np.array(sext3[5])
ao['S3']['Pos']                      = np.array(sext3[6])
ao['S3']['Monitor']                  = {}
ao['S3']['Monitor']['Mode']          = mode
ao['S3']['Monitor']['HWUnits']       = 'ampere'
ao['S3']['Monitor']['PhysicalUnits'] = 'meter^-3'
ao['S3']['Setpoint'] = deepcopy(ao['S3']['Monitor'])
ao['S3']['Monitor']['ChannelNames']  = np.array(sext3[1])
ao['S3']['Setpoint']['ChannelNames'] = np.array(sext3[2])

cs4t = .249787;
cs4d = .253355;
sext4=[
['S4M2D1R', 'S4PD1R:rdbk', 'S4PD1R:set', 1, [ 1, 2], 2.806   ,cs4d],
['S4M1T1R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [ 2, 1], 12.034  ,cs4t],
['S4M2T1R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [ 2, 2], 17.806  ,cs4t],
['S4M1D2R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [ 3, 1], 27.034  ,cs4d],
['S4M2D2R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [ 3, 2], 32.806  ,cs4d],
['S4M1T2R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [ 4, 1], 42.034  ,cs4t],
['S4M2T2R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [ 4, 2], 47.806  ,cs4t],
['S4M1D3R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [ 5, 1], 57.034  ,cs4d],
['S4M2D3R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [ 5, 2], 62.806  ,cs4d],
['S4M1T3R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [ 6, 1], 72.034  ,cs4t],
['S4M2T3R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [ 6, 2], 77.806  ,cs4t],
['S4M1D4R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [ 7, 1], 87.034  ,cs4d],
['S4M2D4R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [ 7, 2], 92.806  ,cs4d],
['S4M1T4R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [ 8, 1], 102.034 ,cs4t],
['S4M2T4R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [ 8, 2], 107.806 ,cs4t],
['S4M1D5R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [ 9, 1], 117.034 ,cs4d],
['S4M2D5R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [ 9, 2], 122.806 ,cs4d],
['S4M1T5R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [10, 1], 132.034 ,cs4t],
['S4M2T5R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [10, 2], 137.806 ,cs4t],
['S4M1D6R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [11, 1], 147.034 ,cs4d],
['S4M2D6R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [11, 2], 152.806 ,cs4d],
['S4M1T6R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [12, 1], 162.034 ,cs4t],
['S4M2T6R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [12, 2], 167.806 ,cs4t],
['S4M1D7R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [13, 1], 177.034 ,cs4d],
['S4M2D7R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [13, 2], 182.806 ,cs4d],
['S4M1T7R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [14, 1], 192.034 ,cs4t],
['S4M2T7R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [14, 2], 197.806 ,cs4t],
['S4M1D8R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [15, 1], 207.034 ,cs4d],
['S4M2D8R', 'S4PDR:rdbk ', 'S4PDR:set ', 1, [15, 2], 212.806 ,cs4d],
['S4M1T8R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [16, 1], 222.034 ,cs4t],
['S4M2T8R', 'S4PTR:rdbk ', 'S4PTR:set ', 1, [16, 2], 227.806 ,cs4t],
['S4M1D1R', 'S4PD1R:rdbk', 'S4PD1R:set', 1, [ 1, 1], 237.034 ,cs4d],
]
sext4 = map(list,zip(*sext4))
ao['S4'] = {}
ao['S4']['CommonNames']              = np.array(sext4[0])
ao['S4']['Status']                   = np.array(sext4[3])
ao['S4']['DeviceList']             = np.array(sext4[4])
ao['S4']['Element']                  = np.array(sext4[5])
ao['S4']['Pos']                      = np.array(sext4[6])
ao['S4']['Monitor']                  = {}
ao['S4']['Monitor']['Mode']          = mode
ao['S4']['Monitor']['HWUnits']       = 'ampere'
ao['S4']['Monitor']['PhysicalUnits'] = 'meter^-3'
ao['S4']['Setpoint'] = deepcopy(ao['S4']['Monitor'])
ao['S4']['Monitor']['ChannelNames']  = np.array(sext4[1])
ao['S4']['Setpoint']['ChannelNames'] = np.array(sext4[2])

ao['DCCT'] = {}
ao['DCCT']['CommonNames'] = 'DCCT'
ao['DCCT']['Status'] = np.array([1])
ao['DCCT']['DeviceList'] = [1,1]
ao['DCCT']['Element'] = np.array([ 1 ])
ao['DCCT']['Pos'] = 23.2555
ao['DCCT']['Monitor'] = {}
ao['DCCT']['Monitor']['ChannelNames'] = 'MDIZ3T5G:current'
ao['DCCT']['Monitor']['HWUnits']      = 'milli-ampere'
ao['DCCT']['Monitor']['PhysicsUnits'] = 'milli-ampere'


 
