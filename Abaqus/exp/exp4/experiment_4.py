import os
clear = lambda: os.system('cls')
clear()

#importing modules
import part
from part import *
import material
from material import *
import section
from section import *
import assembly
from assembly import *
import step
from step import *
import interaction
from interaction import *
import load
from load import *
import mesh
from mesh import *
import job
from job import *
import sketch
from sketch import *
import visualization
from visualization import *
import connectorBehavior
from connectorBehavior import *
import customKernel
from customKernel import *
import amModule
from amModule import *
import amKernelInit
from amKernelInit import *
import amConstants
from amConstants import *
import copy
from copy import *
import os
from os import *
session.journalOptions.setValues(replayGeometry=COORDINATE,recoverGeometry=COORDINATE)

#Include paths
import sys
sys.path.append(r'C:\Users\kariln\Documents\GitHub\abagus_plugins\AM plugin\AMModeler\AMModeler')

#MODEL
thermal = mdb.Model(name= 'thermal')
mdb.models['thermal'].setValues(absoluteZero=-273.15, stefanBoltzmann=5.67E-08)

#PART
part1=thermal.Part(dimensionality =THREE_D , name= 'part1' , type = DEFORMABLE_BODY)
f, e = part1.faces, part1.edges #getting the edges and faces of the part

#extrusion of base
sketch_name = thermal.ConstrainedSketch(name='__profile__',sheetSize= 0.08000000000000002)
sketch_name.rectangle(point1=(-0.1, -0.1),point2=((0.1, 0.1)))
part1.BaseSolidExtrude(sketch=sketch_name,depth=0.02)
e = part1.edges
del thermal.sketches['__profile__']

substrate_top_plane = f.findAt(((0.0, 0.0, 0.02),))[0]
sketch_UpEdge = e.findAt(((0.0, 0.1, 0.02),))[0]
sketch_transform = part1.MakeSketchTransform(sketchPlane = substrate_top_plane,sketchUpEdge=sketch_UpEdge,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,origin=(0.0,0.0,0.02))
AM_sketch = thermal.ConstrainedSketch(name = '__profile__',sheetSize=0.08000000000000002,gridSpacing=0.14, transform=sketch_transform)
AM_sketch.rectangle(point1=(-0.04, -0.04),point2=(0.04, 0.04))
part1.SolidExtrude(depth=0.0092,sketchPlane=substrate_top_plane,sketchUpEdge=sketch_UpEdge,sketchPlaneSide=SIDE1,sketchOrientation=RIGHT,sketch = AM_sketch,flipExtrudeDirection=OFF)
del thermal.sketches['__profile__']
#partition AM into layers
nr_layers = 3
plane_offset = 0.02
for i in range(0,nr_layers):
	datum_id = part1.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=plane_offset).id
	plane = part1.datums[datum_id]
	plane_offset += 0.0030666666666666668
	part1_cells = part1.cells
	top_cell = part1_cells.findAt(((0.,0.,0.0292),))
	part1.PartitionCellByDatumPlane(datumPlane = plane,cells=top_cell)

#PROPERTY
AA2319 = thermal.Material(name='AA2319')
AA2319.Conductivity(temperatureDependency=ON,table=[(120.0, 3.39), (121.0, 6.79), (121.0, 10.2), (122.0, 13.6), (123.0, 17.0), (123.0, 20.4), (124.0, 23.8), (125.0, 27.1), (125.0, 30.5), (126.0, 33.9), (127.0, 37.3), (127.0, 40.7), (128.0, 44.1), (128.0, 47.5), (129.0, 50.9), (129.0, 54.3), (130.0, 57.7), (131.0, 61.1), (132.0, 64.5), (133.0, 67.9), (133.0, 71.3), (134.0, 74.7), (134.0, 78.1), (135.0, 81.4), (136.0, 84.8), (137.0, 88.2), (138.0, 91.6), (138.0, 95.0), (139.0, 98.4), (140.0, 102.0), (140.0, 105.0), (140.0, 109.0), (141.0, 112.0), (142.0, 115.0), (143.0, 119.0), (144.0, 122.0), (144.0, 126.0), (145.0, 129.0), (146.0, 132.0), (146.0, 136.0), (147.0, 139.0), (148.0, 143.0), (149.0, 146.0), (149.0, 149.0), (150.0, 153.0), (150.0, 156.0), (151.0, 160.0), (151.0, 163.0), (152.0, 166.0), (152.0, 170.0), (153.0, 173.0), (153.0, 176.0), (153.0, 180.0), (153.0, 183.0), (153.0, 187.0), (154.0, 190.0), (155.0, 193.0), (155.0, 197.0), (156.0, 204.0), (156.0, 207.0), (156.0, 210.0), (156.0, 214.0), (156.0, 217.0), (157.0, 221.0), (157.0, 224.0), (157.0, 227.0), (157.0, 231.0), (158.0, 238.0), (158.0, 241.0), (158.0, 244.0), (158.0, 251.0), (158.0, 255.0), (157.0, 261.0), (157.0, 265.0), (157.0, 268.0), (157.0, 275.0), (156.0, 278.0), (156.0, 282.0), (156.0, 288.0), (156.0, 295.0), (155.0, 299.0), (155.0, 305.0), (154.0, 309.0), (154.0, 312.0), (153.0, 316.0), (153.0, 319.0), (153.0, 322.0), (153.0, 326.0), (152.0, 329.0), (152.0, 336.0), (151.0, 339.0), (151.0, 343.0), (150.0, 350.0), (149.0, 356.0), (148.0, 360.0), (148.0, 367.0), (147.0, 373.0), (146.0, 377.0), (146.0, 383.0), (145.0, 390.0), (144.0, 397.0), (144.0, 404.0), (144.0, 407.0), (144.0, 411.0), (144.0, 417.0), (144.0, 424.0), (144.0, 431.0), (144.0, 438.0), (144.0, 445.0), (144.0, 455.0), (144.0, 462.0), (144.0, 468.0), (144.0, 475.0), (144.0, 485.0), (144.0, 492.0), (144.0, 495.0), (144.0, 499.0), (144.0, 506.0), (144.0, 516.0), (144.0, 519.0), (144.0, 526.0), (144.0, 529.0), (144.0, 540.0), (144.0, 546.0), (144.0, 550.0), (146.0, 553.0), (148.0, 557.0), (154.0, 560.0), (158.0, 563.0), (167.0, 570.0), (172.0, 574.0), (176.0, 577.0), (180.0, 580.0), (184.0, 584.0), (188.0, 587.0), (192.0, 590.0), (196.0, 594.0), (196.0, 597.0), (204.0, 601.0), (205.0, 604.0), (208.0, 607.0), (213.0, 611.0), (214.0, 614.0), (219.0, 618.0), (222.0, 621.0), (226.0, 624.0), (229.0, 628.0), (233.0, 631.0), (236.0, 635.0), (239.0, 638.0), (243.0, 641.0), (247.0, 645.0), (249.0, 648.0), (253.0, 652.0), (257.0, 655.0), (260.0, 658.0), (266.0, 665.0), (269.0, 669.0), (272.0, 672.0), (277.0, 675.0), (279.0, 679.0), (284.0, 682.0), (287.0, 686.0), (291.0, 689.0), (294.0, 692.0), (294.0, 696.0), (299.0, 699.0), (300.0, 702.0), (300.0, 706.0), (300.0, 709.0), (300.0, 713.0), (300.0, 716.0), (300.0, 723.0), (300.0, 730.0), (300.0, 743.0), (300.0, 753.0), (300.0, 760.0), (300.0, 770.0), (300.0, 787.0), (300.0, 808.0), (300.0, 821.0), (300.0, 835.0), (300.0, 842.0), (300.0, 848.0), (300.0, 852.0), (300.0, 862.0), (300.0, 865.0), (300.0, 872.0), (300.0, 882.0), (300.0, 889.0), (300.0, 899.0), (300.0, 910.0), (300.0, 920.0), (300.0, 930.0), (300.0, 940.0), (300.0, 950.0), (300.0, 964.0), (300.0, 974.0), (300.0, 984.0), (300.0, 994.0), (300.0, 1000.0), (300.0, 1010.0), (300.0, 1020.0), (300.0, 1030.0), (300.0, 1040.0), (300.0, 1050.0), (300.0, 1060.0), (300.0, 1070.0), (300.0, 1080.0), (300.0, 1090.0), (300.0, 1100.0), (300.0, 1110.0), (300.0, 1120.0), (300.0, 1130.0), (300.0, 1140.0), (300.0, 1150.0), (300.0, 1160.0), (300.0, 1170.0), (300.0, 1180.0), (300.0, 1190.0), (300.0, 1200.0), (300.0, 1210.0), (300.0, 1220.0), (300.0, 1230.0), (300.0, 1240.0), (300.0, 1250.0), (300.0, 1270.0), (300.0, 1280.0), (300.0, 1290.0), (300.0, 1300.0), (300.0, 1310.0), (300.0, 1320.0), (300.0, 1330.0), (300.0, 1340.0), (300.0, 1350.0), (300.0, 1360.0), (300.0, 1370.0), (300.0, 1380.0), (300.0, 1390.0), (300.0, 1400.0), (300.0, 1410.0), (300.0, 1420.0), (300.0, 1430.0), (300.0, 1440.0), (300.0, 1460.0), (300.0, 1470.0), (300.0, 1480.0), (300.0, 1490.0), (300.0, 1500.0)])
AA2319.Density(temperatureDependency=OFF,table=[(2823.0,)])
AA2319.Elastic(temperatureDependency=ON,table=[(73000000000.0, 0.3, 0.0), (73000000000.0, 0.3, 1.55), (73000000000.0, 0.3, 3.11), (73000000000.0, 0.3, 4.66), (73000000000.0, 0.3, 6.22), (73000000000.0, 0.3, 6.99), (72800000000.0, 0.3, 8.55), (72800000000.0, 0.3, 10.1), (72800000000.0, 0.3, 10.9), (72800000000.0, 0.3, 12.4), (72800000000.0, 0.3, 13.2), (72800000000.0, 0.3, 14.8), (72500000000.0, 0.3, 16.3), (72500000000.0, 0.3, 17.9), (72500000000.0, 0.3, 18.7), (72500000000.0, 0.3, 20.2), (72500000000.0, 0.3, 21.0), (72500000000.0, 0.3, 22.5), (72300000000.0, 0.3, 24.1), (72300000000.0, 0.3, 25.6), (72300000000.0, 0.3, 28.0), (72000000000.0, 0.3, 29.5), (72000000000.0, 0.3, 30.3), (72000000000.0, 0.3, 31.9), (72000000000.0, 0.3, 33.4), (72000000000.0, 0.3, 34.2), (72000000000.0, 0.3, 35.8), (72000000000.0, 0.3, 36.5), (72000000000.0, 0.3, 38.1), (72000000000.0, 0.3, 39.6), (71800000000.0, 0.3, 40.4), (71800000000.0, 0.3, 42.7), (71800000000.0, 0.3, 43.5), (71800000000.0, 0.3, 45.1), (71800000000.0, 0.3, 46.6), (71800000000.0, 0.3, 48.2), (71500000000.0, 0.3, 50.5), (71500000000.0, 0.3, 53.6), (71500000000.0, 0.3, 56.0), (71200000000.0, 0.3, 58.3), (71200000000.0, 0.3, 61.4), (71200000000.0, 0.3, 65.3), (71000000000.0, 0.3, 66.8), (71000000000.0, 0.3, 68.4), (71000000000.0, 0.3, 69.9), (71000000000.0, 0.3, 72.3), (71000000000.0, 0.3, 73.8), (70700000000.0, 0.3, 75.4), (70700000000.0, 0.3, 76.9), (70700000000.0, 0.3, 79.3), (70700000000.0, 0.3, 80.8), (70500000000.0, 0.3, 82.4), (70500000000.0, 0.3, 84.7), (70500000000.0, 0.3, 87.0), (70500000000.0, 0.3, 90.2), (70500000000.0, 0.3, 91.7), (70500000000.0, 0.3, 93.3), (70200000000.0, 0.3, 95.6), (70200000000.0, 0.3, 97.9), (70200000000.0, 0.3, 99.5), (70000000000.0, 0.3, 101.0), (70000000000.0, 0.3, 103.0), (69700000000.0, 0.3, 105.0), (69700000000.0, 0.3, 106.0), (69500000000.0, 0.3, 108.0), (69500000000.0, 0.3, 109.0), (69500000000.0, 0.3, 110.0), (69500000000.0, 0.3, 111.0), (69200000000.0, 0.3, 112.0), (69200000000.0, 0.3, 114.0), (69000000000.0, 0.3, 116.0), (69000000000.0, 0.3, 117.0), (68700000000.0, 0.3, 119.0), (68700000000.0, 0.3, 120.0), (68400000000.0, 0.3, 121.0), (68400000000.0, 0.3, 122.0), (68400000000.0, 0.3, 123.0), (68400000000.0, 0.3, 124.0), (68400000000.0, 0.3, 125.0), (68200000000.0, 0.3, 126.0), (68200000000.0, 0.3, 127.0), (67900000000.0, 0.3, 129.0), (67900000000.0, 0.3, 131.0), (67700000000.0, 0.3, 132.0), (67700000000.0, 0.3, 134.0), (67700000000.0, 0.3, 135.0), (67400000000.0, 0.3, 137.0), (67400000000.0, 0.3, 138.0), (67200000000.0, 0.3, 140.0), (66900000000.0, 0.3, 142.0), (66900000000.0, 0.3, 144.0), (66900000000.0, 0.3, 145.0), (66700000000.0, 0.3, 148.0), (66700000000.0, 0.3, 149.0), (66700000000.0, 0.3, 151.0), (66400000000.0, 0.3, 153.0), (66200000000.0, 0.3, 155.0), (66200000000.0, 0.3, 156.0), (65900000000.0, 0.3, 158.0), (65900000000.0, 0.3, 159.0), (65900000000.0, 0.3, 160.0), (65900000000.0, 0.3, 161.0), (65600000000.0, 0.3, 163.0), (65600000000.0, 0.3, 165.0), (65400000000.0, 0.3, 166.0), (65400000000.0, 0.3, 167.0), (65100000000.0, 0.3, 169.0), (64900000000.0, 0.3, 172.0), (64900000000.0, 0.3, 173.0), (64900000000.0, 0.3, 175.0), (64600000000.0, 0.3, 176.0), (64600000000.0, 0.3, 178.0), (64600000000.0, 0.3, 179.0), (64400000000.0, 0.3, 180.0), (64400000000.0, 0.3, 182.0), (64400000000.0, 0.3, 183.0), (64100000000.0, 0.3, 184.0), (63900000000.0, 0.3, 187.0), (63900000000.0, 0.3, 188.0), (63900000000.0, 0.3, 190.0), (63600000000.0, 0.3, 191.0), (63600000000.0, 0.3, 193.0), (63600000000.0, 0.3, 194.0), (63600000000.0, 0.3, 195.0), (63400000000.0, 0.3, 197.0), (63100000000.0, 0.3, 198.0), (63100000000.0, 0.3, 200.0), (62800000000.0, 0.3, 202.0), (62600000000.0, 0.3, 204.0), (62600000000.0, 0.3, 207.0), (62300000000.0, 0.3, 208.0), (62300000000.0, 0.3, 209.0), (62100000000.0, 0.3, 211.0), (62100000000.0, 0.3, 214.0), (61800000000.0, 0.3, 216.0), (61600000000.0, 0.3, 217.0), (61600000000.0, 0.3, 218.0), (61600000000.0, 0.3, 220.0), (61300000000.0, 0.3, 221.0), (61300000000.0, 0.3, 223.0), (61300000000.0, 0.3, 224.0), (61100000000.0, 0.3, 225.0), (61100000000.0, 0.3, 227.0), (60800000000.0, 0.3, 228.0), (60800000000.0, 0.3, 230.0), (60600000000.0, 0.3, 232.0), (60600000000.0, 0.3, 233.0), (60300000000.0, 0.3, 235.0), (60300000000.0, 0.3, 236.0), (60100000000.0, 0.3, 237.0), (59800000000.0, 0.3, 239.0), (59800000000.0, 0.3, 240.0), (59800000000.0, 0.3, 242.0), (59500000000.0, 0.3, 243.0), (59500000000.0, 0.3, 244.0), (59300000000.0, 0.3, 246.0), (59300000000.0, 0.3, 248.0), (59000000000.0, 0.3, 249.0), (59000000000.0, 0.3, 252.0), (58800000000.0, 0.3, 253.0), (58800000000.0, 0.3, 255.0), (58800000000.0, 0.3, 256.0), (58500000000.0, 0.3, 257.0), (58500000000.0, 0.3, 259.0), (58300000000.0, 0.3, 260.0), (58000000000.0, 0.3, 262.0), (58000000000.0, 0.3, 263.0), (58000000000.0, 0.3, 265.0), (57800000000.0, 0.3, 267.0), (57800000000.0, 0.3, 269.0), (57500000000.0, 0.3, 270.0), (57500000000.0, 0.3, 273.0), (57300000000.0, 0.3, 274.0), (57300000000.0, 0.3, 277.0), (57000000000.0, 0.3, 278.0), (56700000000.0, 0.3, 281.0), (56500000000.0, 0.3, 282.0), (56500000000.0, 0.3, 284.0), (56200000000.0, 0.3, 286.0), (56200000000.0, 0.3, 288.0), (56000000000.0, 0.3, 289.0), (56000000000.0, 0.3, 291.0), (55700000000.0, 0.3, 292.0), (55700000000.0, 0.3, 293.0), (55700000000.0, 0.3, 294.0), (55700000000.0, 0.3, 295.0), (55500000000.0, 0.3, 296.0), (55200000000.0, 0.3, 297.0), (55200000000.0, 0.3, 298.0), (55000000000.0, 0.3, 299.0), (55000000000.0, 0.3, 300.0), (54700000000.0, 0.3, 302.0), (54500000000.0, 0.3, 303.0), (53900000000.0, 0.3, 305.0), (53900000000.0, 0.3, 306.0), (53700000000.0, 0.3, 307.0), (53400000000.0, 0.3, 308.0), (53400000000.0, 0.3, 309.0), (53200000000.0, 0.3, 310.0), (53200000000.0, 0.3, 312.0), (52700000000.0, 0.3, 313.0), (52400000000.0, 0.3, 314.0), (52400000000.0, 0.3, 315.0), (52200000000.0, 0.3, 316.0), (51900000000.0, 0.3, 317.0), (51900000000.0, 0.3, 318.0), (51700000000.0, 0.3, 319.0), (51400000000.0, 0.3, 320.0), (51400000000.0, 0.3, 321.0), (51100000000.0, 0.3, 322.0), (50900000000.0, 0.3, 323.0), (50600000000.0, 0.3, 324.0), (50600000000.0, 0.3, 325.0), (50400000000.0, 0.3, 326.0), (50100000000.0, 0.3, 327.0), (50100000000.0, 0.3, 328.0), (49600000000.0, 0.3, 330.0), (49400000000.0, 0.3, 331.0), (49100000000.0, 0.3, 332.0), (49100000000.0, 0.3, 333.0), (48900000000.0, 0.3, 334.0), (48600000000.0, 0.3, 336.0), (48300000000.0, 0.3, 337.0), (48100000000.0, 0.3, 338.0), (48100000000.0, 0.3, 339.0), (47800000000.0, 0.3, 340.0), (47600000000.0, 0.3, 341.0), (47100000000.0, 0.3, 343.0), (47100000000.0, 0.3, 344.0), (46800000000.0, 0.3, 345.0), (46600000000.0, 0.3, 346.0), (46600000000.0, 0.3, 347.0), (46300000000.0, 0.3, 348.0), (46100000000.0, 0.3, 349.0), (46100000000.0, 0.3, 350.0), (45800000000.0, 0.3, 351.0), (45500000000.0, 0.3, 352.0), (45500000000.0, 0.3, 353.0), (45300000000.0, 0.3, 354.0), (45000000000.0, 0.3, 355.0), (44800000000.0, 0.3, 356.0), (44300000000.0, 0.3, 358.0), (44000000000.0, 0.3, 360.0), (44000000000.0, 0.3, 361.0), (43800000000.0, 0.3, 363.0), (43500000000.0, 0.3, 364.0), (43300000000.0, 0.3, 365.0), (43000000000.0, 0.3, 366.0), (43000000000.0, 0.3, 367.0), (42700000000.0, 0.3, 368.0), (42500000000.0, 0.3, 369.0), (42200000000.0, 0.3, 370.0), (42000000000.0, 0.3, 371.0), (41700000000.0, 0.3, 372.0), (41700000000.0, 0.3, 374.0), (41500000000.0, 0.3, 375.0), (41200000000.0, 0.3, 376.0), (41000000000.0, 0.3, 377.0), (40700000000.0, 0.3, 378.0), (40500000000.0, 0.3, 379.0), (40500000000.0, 0.3, 380.0), (40200000000.0, 0.3, 381.0), (39900000000.0, 0.3, 382.0), (39700000000.0, 0.3, 383.0), (39400000000.0, 0.3, 384.0), (39400000000.0, 0.3, 385.0), (39200000000.0, 0.3, 386.0), (38900000000.0, 0.3, 388.0), (38700000000.0, 0.3, 389.0), (38700000000.0, 0.3, 390.0), (38400000000.0, 0.3, 391.0), (37900000000.0, 0.3, 392.0), (37900000000.0, 0.3, 394.0), (37700000000.0, 0.3, 395.0), (37400000000.0, 0.3, 396.0), (37400000000.0, 0.3, 397.0), (37200000000.0, 0.3, 398.0), (36900000000.0, 0.3, 399.0), (36400000000.0, 0.3, 401.0), (35900000000.0, 0.3, 403.0), (35600000000.0, 0.3, 405.0), (35400000000.0, 0.3, 406.0), (35100000000.0, 0.3, 407.0), (34900000000.0, 0.3, 409.0), (34600000000.0, 0.3, 410.0), (34400000000.0, 0.3, 412.0), (34100000000.0, 0.3, 413.0), (33800000000.0, 0.3, 414.0), (33600000000.0, 0.3, 415.0), (33300000000.0, 0.3, 417.0), (33100000000.0, 0.3, 418.0), (32800000000.0, 0.3, 419.0), (32600000000.0, 0.3, 420.0), (32300000000.0, 0.3, 421.0), (32300000000.0, 0.3, 423.0), (32100000000.0, 0.3, 424.0), (31600000000.0, 0.3, 425.0), (31600000000.0, 0.3, 426.0), (31300000000.0, 0.3, 427.0), (31000000000.0, 0.3, 429.0), (30800000000.0, 0.3, 430.0), (30300000000.0, 0.3, 431.0), (30300000000.0, 0.3, 432.0), (30300000000.0, 0.3, 433.0), (29800000000.0, 0.3, 435.0), (29500000000.0, 0.3, 436.0), (29300000000.0, 0.3, 437.0), (29000000000.0, 0.3, 438.0), (29000000000.0, 0.3, 439.0), (28500000000.0, 0.3, 441.0), (28200000000.0, 0.3, 442.0), (28000000000.0, 0.3, 443.0), (28000000000.0, 0.3, 444.0), (27700000000.0, 0.3, 445.0), (27500000000.0, 0.3, 446.0), (27500000000.0, 0.3, 447.0), (27000000000.0, 0.3, 448.0), (27000000000.0, 0.3, 449.0), (26700000000.0, 0.3, 450.0), (26500000000.0, 0.3, 451.0), (26200000000.0, 0.3, 452.0), (26000000000.0, 0.3, 453.0), (25700000000.0, 0.3, 454.0), (25700000000.0, 0.3, 455.0), (25400000000.0, 0.3, 456.0), (25200000000.0, 0.3, 457.0), (24900000000.0, 0.3, 458.0), (24900000000.0, 0.3, 459.0), (24400000000.0, 0.3, 460.0), (24200000000.0, 0.3, 462.0), (23900000000.0, 0.3, 464.0), (23700000000.0, 0.3, 465.0), (23400000000.0, 0.3, 466.0), (23200000000.0, 0.3, 467.0), (22600000000.0, 0.3, 469.0), (22400000000.0, 0.3, 471.0), (22100000000.0, 0.3, 472.0), (21900000000.0, 0.3, 473.0), (21900000000.0, 0.3, 475.0), (21400000000.0, 0.3, 476.0), (21100000000.0, 0.3, 477.0), (20900000000.0, 0.3, 478.0), (20600000000.0, 0.3, 479.0), (20600000000.0, 0.3, 480.0), (20600000000.0, 0.3, 482.0), (19800000000.0, 0.3, 483.0), (19800000000.0, 0.3, 484.0), (19600000000.0, 0.3, 485.0), (19300000000.0, 0.3, 487.0), (19100000000.0, 0.3, 488.0), (18600000000.0, 0.3, 490.0), (18300000000.0, 0.3, 491.0), (18100000000.0, 0.3, 492.0), (17800000000.0, 0.3, 494.0), (17600000000.0, 0.3, 496.0), (17300000000.0, 0.3, 497.0), (16800000000.0, 0.3, 499.0), (16500000000.0, 0.3, 501.0), (16300000000.0, 0.3, 503.0), (16000000000.0, 0.3, 504.0), (15500000000.0, 0.3, 507.0), (15300000000.0, 0.3, 508.0), (15000000000.0, 0.3, 510.0), (14800000000.0, 0.3, 511.0), (14500000000.0, 0.3, 514.0), (14200000000.0, 0.3, 515.0), (14000000000.0, 0.3, 517.0), (13700000000.0, 0.3, 518.0), (13500000000.0, 0.3, 519.0), (13000000000.0, 0.3, 521.0), (13000000000.0, 0.3, 522.0), (12700000000.0, 0.3, 523.0), (12500000000.0, 0.3, 524.0), (12200000000.0, 0.3, 525.0), (12000000000.0, 0.3, 527.0), (11700000000.0, 0.3, 529.0), (11500000000.0, 0.3, 531.0), (11200000000.0, 0.3, 532.0), (10900000000.0, 0.3, 535.0), (10700000000.0, 0.3, 536.0), (10200000000.0, 0.3, 538.0), (9920000000.0, 0.3, 539.0), (9410000000.0, 0.3, 542.0), (9160000000.0, 0.3, 544.0), (9160000000.0, 0.3, 546.0), (8650000000.0, 0.3, 548.0), (8400000000.0, 0.3, 549.0), (8140000000.0, 0.3, 550.0), (7890000000.0, 0.3, 551.0), (7890000000.0, 0.3, 553.0), (7630000000.0, 0.3, 554.0), (7380000000.0, 0.3, 555.0), (7120000000.0, 0.3, 556.0), (6870000000.0, 0.3, 558.0), (6620000000.0, 0.3, 560.0), (6360000000.0, 0.3, 561.0), (6110000000.0, 0.3, 563.0), (5850000000.0, 0.3, 564.0), (5600000000.0, 0.3, 566.0), (5340000000.0, 0.3, 567.0), (5090000000.0, 0.3, 569.0), (4830000000.0, 0.3, 570.0), (4580000000.0, 0.3, 571.0), (4330000000.0, 0.3, 573.0), (4070000000.0, 0.3, 574.0), (4070000000.0, 0.3, 575.0), (3560000000.0, 0.3, 577.0), (3560000000.0, 0.3, 578.0), (3310000000.0, 0.3, 580.0), (3050000000.0, 0.3, 581.0), (2800000000.0, 0.3, 583.0), (2290000000.0, 0.3, 585.0), (2040000000.0, 0.3, 587.0), (1780000000.0, 0.3, 588.0), (1530000000.0, 0.3, 589.0), (1270000000.0, 0.3, 591.0), (1020000000.0, 0.3, 592.0), (1020000000.0, 0.3, 594.0), (509000000.0, 0.3, 595.0), (509000000.0, 0.3, 596.0), (254000000.0, 0.3, 597.0)])
AA2319.Expansion(temperatureDependency=ON,table=[(2.24e-05, 100.0), (2.25e-05, 103.0), (2.25e-05, 104.0), (2.25e-05, 105.0), (2.25e-05, 106.0), (2.25e-05, 107.0), (2.25e-05, 108.0), (2.25e-05, 109.0), (2.25e-05, 110.0), (2.26e-05, 111.0), (2.26e-05, 112.0), (2.26e-05, 113.0), (2.26e-05, 114.0), (2.26e-05, 115.0), (2.26e-05, 116.0), (2.26e-05, 117.0), (2.26e-05, 118.0), (2.27e-05, 119.0), (2.27e-05, 120.0), (2.27e-05, 121.0), (2.27e-05, 122.0), (2.27e-05, 123.0), (2.27e-05, 124.0), (2.27e-05, 125.0), (2.28e-05, 126.0), (2.28e-05, 127.0), (2.28e-05, 128.0), (2.28e-05, 129.0), (2.28e-05, 130.0), (2.28e-05, 131.0), (2.28e-05, 132.0), (2.29e-05, 133.0), (2.29e-05, 134.0), (2.29e-05, 135.0), (2.29e-05, 136.0), (2.29e-05, 137.0), (2.29e-05, 138.0), (2.29e-05, 139.0), (2.3e-05, 140.0), (2.3e-05, 141.0), (2.3e-05, 142.0), (2.3e-05, 143.0), (2.3e-05, 144.0), (2.3e-05, 145.0), (2.3e-05, 146.0), (2.31e-05, 147.0), (2.31e-05, 148.0), (2.31e-05, 149.0), (2.31e-05, 150.0), (2.31e-05, 151.0), (2.31e-05, 152.0), (2.31e-05, 153.0), (2.31e-05, 154.0), (2.31e-05, 155.0), (2.31e-05, 156.0), (2.31e-05, 157.0), (2.31e-05, 158.0), (2.32e-05, 159.0), (2.32e-05, 160.0), (2.32e-05, 161.0), (2.32e-05, 163.0), (2.32e-05, 164.0), (2.32e-05, 165.0), (2.33e-05, 166.0), (2.33e-05, 167.0), (2.33e-05, 168.0), (2.33e-05, 169.0), (2.33e-05, 170.0), (2.33e-05, 171.0), (2.33e-05, 172.0), (2.34e-05, 173.0), (2.34e-05, 174.0), (2.34e-05, 175.0), (2.34e-05, 176.0), (2.34e-05, 177.0), (2.34e-05, 178.0), (2.34e-05, 179.0), (2.34e-05, 180.0), (2.35e-05, 183.0), (2.35e-05, 184.0), (2.35e-05, 185.0), (2.35e-05, 186.0), (2.35e-05, 187.0), (2.36e-05, 188.0), (2.36e-05, 189.0), (2.36e-05, 190.0), (2.36e-05, 191.0), (2.36e-05, 192.0), (2.36e-05, 193.0), (2.37e-05, 194.0), (2.37e-05, 195.0), (2.37e-05, 196.0), (2.37e-05, 197.0), (2.37e-05, 198.0), (2.37e-05, 199.0), (2.37e-05, 200.0), (2.38e-05, 202.0), (2.38e-05, 205.0), (2.38e-05, 206.0), (2.38e-05, 207.0), (2.38e-05, 208.0), (2.38e-05, 209.0), (2.38e-05, 210.0), (2.38e-05, 211.0), (2.38e-05, 212.0), (2.38e-05, 213.0), (2.38e-05, 214.0), (2.38e-05, 215.0), (2.38e-05, 216.0), (2.39e-05, 217.0), (2.39e-05, 218.0), (2.39e-05, 220.0), (2.39e-05, 221.0), (2.39e-05, 222.0), (2.39e-05, 223.0), (2.39e-05, 225.0), (2.4e-05, 227.0), (2.4e-05, 228.0), (2.4e-05, 229.0), (2.4e-05, 230.0), (2.4e-05, 231.0), (2.4e-05, 232.0), (2.4e-05, 233.0), (2.4e-05, 234.0), (2.4e-05, 235.0), (2.4e-05, 236.0), (2.41e-05, 237.0), (2.41e-05, 238.0), (2.41e-05, 239.0), (2.41e-05, 240.0), (2.41e-05, 241.0), (2.41e-05, 242.0), (2.41e-05, 243.0), (2.41e-05, 244.0), (2.42e-05, 245.0), (2.42e-05, 246.0), (2.42e-05, 248.0), (2.42e-05, 249.0), (2.42e-05, 250.0), (2.42e-05, 251.0), (2.42e-05, 252.0), (2.42e-05, 253.0), (2.43e-05, 254.0), (2.43e-05, 255.0), (2.43e-05, 256.0), (2.43e-05, 257.0), (2.43e-05, 258.0), (2.43e-05, 259.0), (2.43e-05, 260.0), (2.43e-05, 262.0), (2.44e-05, 263.0), (2.44e-05, 264.0), (2.44e-05, 265.0), (2.44e-05, 266.0), (2.44e-05, 267.0), (2.44e-05, 268.0), (2.44e-05, 269.0), (2.44e-05, 270.0), (2.44e-05, 271.0), (2.44e-05, 272.0), (2.44e-05, 273.0), (2.44e-05, 274.0), (2.44e-05, 275.0), (2.44e-05, 277.0), (2.45e-05, 278.0), (2.45e-05, 279.0), (2.45e-05, 281.0), (2.45e-05, 282.0), (2.45e-05, 283.0), (2.45e-05, 284.0), (2.45e-05, 285.0), (2.45e-05, 288.0), (2.46e-05, 289.0), (2.46e-05, 290.0), (2.46e-05, 291.0), (2.46e-05, 292.0), (2.46e-05, 293.0), (2.46e-05, 294.0), (2.46e-05, 295.0), (2.46e-05, 297.0), (2.47e-05, 298.0), (2.47e-05, 299.0), (2.47e-05, 301.0), (2.47e-05, 303.0), (2.47e-05, 306.0), (2.47e-05, 308.0), (2.47e-05, 311.0), (2.47e-05, 315.0), (2.47e-05, 320.0), (2.47e-05, 325.0), (2.47e-05, 331.0), (2.47e-05, 337.0), (2.47e-05, 340.0), (2.47e-05, 342.0), (2.47e-05, 351.0), (2.47e-05, 357.0), (2.47e-05, 361.0), (2.47e-05, 366.0), (2.47e-05, 369.0), (2.47e-05, 374.0), (2.47e-05, 377.0), (2.47e-05, 383.0), (2.47e-05, 389.0), (2.47e-05, 394.0), (2.47e-05, 398.0), (2.47e-05, 403.0), (2.47e-05, 408.0), (2.47e-05, 414.0), (2.47e-05, 417.0), (2.47e-05, 419.0), (2.47e-05, 422.0), (2.47e-05, 425.0), (2.47e-05, 430.0), (2.47e-05, 434.0), (2.47e-05, 438.0), (2.47e-05, 443.0), (2.47e-05, 446.0), (2.47e-05, 451.0), (2.47e-05, 456.0), (2.47e-05, 459.0), (2.47e-05, 465.0), (2.47e-05, 470.0), (2.47e-05, 474.0), (2.47e-05, 480.0), (2.47e-05, 485.0), (2.47e-05, 489.0), (2.47e-05, 494.0), (2.47e-05, 499.0), (2.47e-05, 504.0), (2.47e-05, 511.0), (2.47e-05, 518.0), (2.47e-05, 523.0), (2.47e-05, 527.0), (2.47e-05, 530.0), (2.47e-05, 538.0), (2.47e-05, 544.0), (2.47e-05, 550.0), (2.47e-05, 554.0), (2.47e-05, 558.0), (2.47e-05, 564.0), (2.47e-05, 568.0), (2.47e-05, 573.0), (2.47e-05, 577.0), (2.47e-05, 582.0), (2.47e-05, 589.0), (2.47e-05, 594.0), (2.47e-05, 600.0)])
AA2319.LatentHeat(table=[(374000.0, 543.0, 643.0)])
AA2319.Plastic(temperatureDependency=ON,table=[(235000000.0, 0.0, 20.0), (254000000.0, 0.00676, 20.0), (117000000.0, 0.0, 316.0), (138000000.0, 0.007759, 316.0), (41000000.0, 0.0, 371.0), (61100000.0, 0.009024, 371.0), (4830000.0, 0.0, 550.0), (8040000.0, 0.00941, 550.0)])
AA2319.SpecificHeat(temperatureDependency=ON,table=[(862.0, 50.0), (864.0, 53.5), (865.0, 56.9), (870.0, 60.4), (873.0, 63.8), (879.0, 67.3), (882.0, 70.8), (884.0, 74.2), (890.0, 77.7), (892.0, 81.2), (893.0, 84.6), (899.0, 88.1), (903.0, 91.5), (907.0, 95.0), (909.0, 98.5), (913.0, 102.0), (917.0, 105.0), (918.0, 112.0), (920.0, 116.0), (921.0, 119.0), (923.0, 123.0), (926.0, 126.0), (927.0, 130.0), (929.0, 133.0), (931.0, 137.0), (934.0, 140.0), (937.0, 143.0), (938.0, 150.0), (940.0, 154.0), (941.0, 161.0), (943.0, 164.0), (943.0, 171.0), (945.0, 175.0), (946.0, 178.0), (948.0, 182.0), (948.0, 185.0), (949.0, 192.0), (952.0, 199.0), (954.0, 202.0), (955.0, 209.0), (957.0, 213.0), (959.0, 220.0), (962.0, 223.0), (962.0, 227.0), (962.0, 230.0), (963.0, 233.0), (963.0, 237.0), (963.0, 240.0), (963.0, 244.0), (962.0, 251.0), (962.0, 254.0), (960.0, 258.0), (959.0, 265.0), (959.0, 268.0), (957.0, 272.0), (955.0, 278.0), (955.0, 282.0), (957.0, 285.0), (959.0, 289.0), (963.0, 292.0), (968.0, 296.0), (969.0, 299.0), (973.0, 303.0), (976.0, 306.0), (980.0, 310.0), (982.0, 313.0), (988.0, 317.0), (990.0, 320.0), (993.0, 323.0), (999.0, 327.0), (1000.0, 330.0), (1010.0, 334.0), (1010.0, 337.0), (1020.0, 341.0), (1020.0, 344.0), (1030.0, 348.0), (1030.0, 351.0), (1040.0, 355.0), (1040.0, 358.0), (1050.0, 362.0), (1050.0, 365.0), (1050.0, 368.0), (1060.0, 372.0), (1060.0, 375.0), (1060.0, 379.0), (1060.0, 386.0), (1060.0, 389.0), (1060.0, 400.0), (1060.0, 413.0), (1060.0, 420.0), (1060.0, 431.0), (1060.0, 438.0), (1060.0, 448.0), (1060.0, 462.0), (1060.0, 476.0), (1060.0, 486.0), (1060.0, 493.0), (1060.0, 503.0), (1060.0, 510.0), (1060.0, 524.0), (1060.0, 535.0), (1060.0, 542.0), (1060.0, 555.0), (1060.0, 566.0), (1060.0, 573.0), (1060.0, 583.0), (1060.0, 593.0), (1060.0, 604.0), (1060.0, 614.0), (1060.0, 628.0), (1060.0, 638.0), (1060.0, 649.0), (1060.0, 656.0), (1060.0, 670.0), (1060.0, 680.0), (1060.0, 690.0), (1060.0, 701.0), (1060.0, 711.0), (1060.0, 722.0), (1060.0, 735.0), (1060.0, 746.0), (1060.0, 756.0), (1060.0, 767.0), (1060.0, 777.0), (1060.0, 798.0), (1060.0, 808.0), (1060.0, 818.0), (1060.0, 829.0), (1060.0, 836.0), (1060.0, 846.0), (1060.0, 857.0), (1060.0, 874.0), (1060.0, 891.0), (1060.0, 905.0), (1060.0, 919.0), (1060.0, 929.0), (1060.0, 943.0), (1060.0, 953.0), (1060.0, 964.0), (1060.0, 974.0), (1060.0, 981.0), (1060.0, 992.0), (1060.0, 1000.0), (1060.0, 1010.0), (1060.0, 1020.0), (1060.0, 1030.0), (1060.0, 1040.0), (1060.0, 1050.0), (1060.0, 1060.0), (1060.0, 1070.0), (1060.0, 1080.0), (1060.0, 1090.0), (1060.0, 1100.0), (1060.0, 1110.0), (1060.0, 1120.0), (1060.0, 1130.0), (1060.0, 1140.0), (1060.0, 1150.0), (1060.0, 1170.0), (1060.0, 1180.0), (1060.0, 1200.0), (1060.0, 1210.0), (1060.0, 1220.0), (1060.0, 1230.0), (1060.0, 1240.0), (1060.0, 1250.0), (1060.0, 1260.0), (1060.0, 1270.0), (1060.0, 1280.0), (1060.0, 1290.0), (1060.0, 1300.0), (1060.0, 1310.0), (1060.0, 1320.0), (1060.0, 1330.0), (1060.0, 1340.0), (1060.0, 1350.0), (1060.0, 1360.0), (1060.0, 1370.0), (1060.0, 1380.0), (1060.0, 1390.0), (1060.0, 1400.0)])

thermal.HomogeneousSolidSection(name='Part_Section', material='AA2319', thickness=None)
c = part1.cells
region = part1.Set(cells = c, name = "full_part")
part1.SectionAssignment(region=region, sectionName='Part_Section', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='', thicknessAssignment=FROM_SECTION)

#ASSEMBLY
a = thermal.rootAssembly
a.DatumCsysByDefault(CARTESIAN)
a.Instance(name='part1', part= part1, dependent=ON)

#STEP
thermal.HeatTransferStep(name='heat', previous='Initial', timePeriod=1000, initialInc=0.01, minInc=1e-08, maxInc=1,deltmx=1000,maxNumInc=10000)

#MESH
part1.seedPart(size=0.0025, deviationFactor=0.1, minSizeFactor=0.1)
e = part1.edges
part1.generateMesh()
elemType1 = mesh.ElemType(elemCode=DC3D8, elemLibrary=STANDARD)
elemType2 = mesh.ElemType(elemCode=DC3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=DC3D4, elemLibrary=STANDARD)
c = part1.cells
region = part1.Set(cells = c, name = "part")
part1.setElementType(regions=region, elemTypes=(elemType1,elemType2,elemType3))

#BOUNDARY CONDITION
n = part1.nodes
origo_node = n.getByBoundingSphere(center = (0.,0.,0.), radius = 0.00125)
part1.Set(nodes=origo_node, name="origo_node")
a = thermal.rootAssembly
region = a.instances["part1"].sets["origo_node"]
thermal.DisplacementBC(name="origo_BC", createStepName="Initial", region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName="", localCsys=None)

#PREDEFINED FIELDS
nodes1 = part1.nodes
part1.Set(nodes=nodes1, name="all_nodes")
a = thermal.rootAssembly
region = a.instances["part1"].sets["all_nodes"]
thermal.Temperature(name="room_temp", createStepName="Initial", region=region, distributionType=UNIFORM, crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, magnitudes=(20, ))

thermal.fieldOutputRequests['F-Output-1'].setValues(variables=('NT','TEMP'))

#AM PART
amModule.createAMModel(amModelName='AM_thermal', modelName1='thermal', stepName1='heat', analysisType1=HEAT_TRANSFER, isSequential=OFF, modelName2='', stepName2='', analysisType2=STRUCTURAL, processType=AMPROC_ABAQUS_BUILTIN)
a = thermal.rootAssembly
a.regenerate()
mdb.customData.am.amModels["AM_thermal"].assignAMPart(amPartsData=(("part1", "Build Part"), ("", ""), ("", ""), ("", ""), ("", "")))

#EVENT SERIES
mdb.customData.am.amModels["AM_thermal"].addEventSeries(eventSeriesName="material_path", eventSeriesTypeName='"ABQ_AM.MaterialDeposition"', timeSpan="TOTAL TIME", fileName="C:\Users\kariln\Documents\GitHub\Master\Abaqus\exp\exp4\material_path.txt", isFile=ON)
mdb.customData.am.amModels["AM_thermal"].addEventSeries(eventSeriesName="heat_path", eventSeriesTypeName='"ABQ_AM.PowerMagnitude"', timeSpan="TOTAL TIME", fileName="C:\Users\kariln\Documents\GitHub\Master\Abaqus\exp\exp4\heat_path.txt", isFile=ON)

#TABLE COLLECTIONS
mdb.customData.am.amModels["AM_thermal"].addTableCollection(tableCollectionName="ABQ_AM_Material")
mdb.customData.am.amModels["AM_thermal"].dataSetup.tableCollections["ABQ_AM_Material"].ParameterTable(name='_parameterTable_"ABQ_AM.MaterialDeposition.Advanced"_', parameterTabletype='"ABQ_AM.MaterialDeposition.Advanced"', parameterData=(('Full', 0.0, 0.0), ))
mdb.customData.am.amModels["AM_thermal"].dataSetup.tableCollections["ABQ_AM_Material"].ParameterTable(name = '_parameterTable_"ABQ_AM.MaterialDeposition.Bead"_', parameterTabletype='"ABQ_AM.MaterialDeposition.Bead"', parameterData=(('Z', 0.0030666666666666668,0.01,0.005, 'Below'), ))
mdb.customData.am.amModels["AM_thermal"].dataSetup.tableCollections["ABQ_AM_Material"].ParameterTable(name = '_parameterTable_"ABQ_AM.MaterialDeposition"_', parameterTabletype='"ABQ_AM.MaterialDeposition"', parameterData=(('material_path', 'Bead'), ))
mdb.customData.am.amModels["AM_thermal"].addTableCollection(tableCollectionName="ABQ_AM_Heat")
mdb.customData.am.amModels["AM_thermal"].dataSetup.tableCollections['ABQ_AM_Heat'].PropertyTable(name='_propertyTable_"ABQ_AM.AbsorptionCoeff"_', propertyTableType='"ABQ_AM.AbsorptionCoeff"', propertyTableData=((0.9, ), ), numDependencies=0, temperatureDependency=OFF)
mdb.customData.am.amModels["AM_thermal"].dataSetup.tableCollections['ABQ_AM_Heat'].ParameterTable(name='_parameterTable_"ABQ_AM.MovingHeatSource"_', parameterTabletype='"ABQ_AM.MovingHeatSource"', parameterData=(('heat_path', 'Goldak'), ))
mdb.customData.am.amModels["AM_thermal"].dataSetup.tableCollections['ABQ_AM_Heat'].ParameterTable(name='_parameterTable_"ABQ_AM.MovingHeatSource.Goldak"_', parameterTabletype='"ABQ_AM.MovingHeatSource.Goldak"', parameterData=(('9', '9', '9', 0.005,0.0030666666666666668, 0.002, 0.004, 0.6, 1.4, 1), ))
mdb.customData.am.amModels["AM_thermal"].dataSetup.tableCollections['ABQ_AM_Heat'].ParameterTable(name='_parameterTable_"ABQ_AM.MovingHeatSource.Advanced"_', parameterTabletype='"ABQ_AM.MovingHeatSource.Advanced"', parameterData=(('False', 'False', 'Relative', 0.0, 0.0, -1.0, 1.0), ))

#SIMULATION SETUP
a = thermal.rootAssembly
e = a.instances['part1'].elements
add_elements = e.getByBoundingBox(-0.04,-0.04,0.01875,0.04,0.04,0.03045)
a.Set(elements=add_elements, name="add_element")
f = a.instances["part1"].faces
basement_face = f.findAt(((0.0,0.0,0.0) ,))
a.Set(faces=basement_face, name = "basement")
c = a.instances["part1"].cells
film = c.findAt(((-0.04,-0.013333333333333334,0.021533333333333335), ), ((-0.04,-0.013333333333333334,0.0246), ),((-0.04,-0.013333333333333334,0.027666666666666666),  ), ((-0.04,-0.013333333333333334,0.02),  ))
a.Set(cells = film, name = "film")
mdb.customData.am.amModels["AM_thermal"].addMaterialArrival(materialArrivalName='Material Source -1', tableCollection='ABQ_AM_Material', followDeformation=OFF, useElementSet=ON, elementSetRegion=('add_element', ))
mdb.customData.am.amModels["AM_thermal"].addHeatSourceDefinition(heatSourceName='Heat Source -1', dfluxDistribution='Moving-UserDefined', dfluxMagnitude=1, tableCollection='ABQ_AM_Heat', useElementSet=OFF, elementSetRegion=())
mdb.customData.am.amModels["AM_thermal"].addCoolingInteractions(coolingInteractionName='Film', useElementSet=ON, elementSetRegion=('film', ), isConvectionActive=ON, isRadiationActive=OFF, filmDefinition='Embedded Coefficient', filmCoefficient=8.5, filmcoefficeintamplitude='Instantaneous', sinkDefinition='Uniform', sinkTemperature=20, sinkAmplitude='Instantaneous', radiationType='toAmbient', emissivityDistribution='Uniform', emissivity=0.8, ambientTemperature=20, ambientTemperatureAmplitude='Instanteneous')
mdb.customData.am.amModels["AM_thermal"].addCoolingInteractions(coolingInteractionName='Basement', useElementSet=ON, elementSetRegion=('basement', ), isConvectionActive=ON, isRadiationActive=ON, filmDefinition='Embedded Coefficient', filmCoefficient=167, filmcoefficeintamplitude='Instantaneous', sinkDefinition='Uniform', sinkTemperature=20, sinkAmplitude='Instantaneous', radiationType='toAmbient', emissivityDistribution='Uniform', emissivity=0.8, ambientTemperature=20, ambientTemperatureAmplitude='Instanteneous')
mdb.Job(name='experiment4_thermal', model='thermal', description='', type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=2, numDomains=2, numGPUs=0)
mdb.jobs['experiment4_thermal'].submit(consistencyChecking=OFF)
mdb.jobs['job' + str(j)].waitForCompletion()
