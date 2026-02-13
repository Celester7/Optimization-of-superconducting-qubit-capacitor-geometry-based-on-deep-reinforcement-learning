import win32com.client
from datetime import datetime

def get_Q3D(a,y_smooth1,y_smooth2,y_smooth3,y_smooth4,width,dir_path): 
    pointx=[]
    pointy=[]
    pointyy=[]
    oAnsoftApp=win32com.client.Dispatch('AnsoftHfss.HfssScriptInterface')
    oDesktop=oAnsoftApp.GetAppDesktop()
    oProject=oDesktop.NewProject("P")
    oProject.InsertDesign("Q3D Extractor", "Qubit1_q3d", "Q3D", "")
    oDesign=oProject.SetActiveDesign("Qubit1_q3d")
    oModule=oDesign.GetModule("AnalysisSetup")
    oModule.InsertSetup("Matrix", 
        [
            "NAME:Setup",
            "AdaptiveFreq:="	, "5GHz",
            "SaveFields:="		, False,
            "Enabled:="		, True,
            [
                "NAME:Cap",
                "MaxPass:="		, 15,
                "MinPass:="		, 1,
                "MinConvPass:="		, 1,
                "PerError:="		, 0.1,
                "PerRefine:="		, 30,
                "AutoIncreaseSolutionOrder:=", True,
                "SolutionOrder:="	, "High",
                "Solver Type:="		, "Iterative"
            ]
        ])
    oEditor=oDesign.SetActiveEditor('3D Modeler')
    oEditor.CreatePolyline( 
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, False,
            [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="			, "0.0007875",
                    "Y:="			, "0.00187",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.0007625",
                    "Y:="			, "0.00187",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.00068",
                    "Y:="			, "0.001805",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.000595",
                    "Y:="			, "0.001805",
                    "Z:="			, "0"
                ]
            ],
            [
                "NAME:PolylineSegments",
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 0,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 1,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 2,
                    "NoOfPoints:="		, 2
                ]
            ],
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "None",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "0mm",
                "XSectionTopWidth:="	, "0mm",
                "XSectionHeight:="	, "0mm",
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Corner"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Polyline1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty( 
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Polyline1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "readout_wire_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreatePolyline( 
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, False,
            [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="			, "0.0007875",
                    "Y:="			, "0.001865",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.0007875",
                    "Y:="			, "0.001875",
                    "Z:="			, "0"
                ]
            ],
            [
                "NAME:PolylineSegments",
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 0,
                    "NoOfPoints:="		, 2
                ]
            ],
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "None",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "0mm",
                "XSectionTopWidth:="	, "0mm",
                "XSectionHeight:="	, "0mm",
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Corner"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Polyline1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0.9,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "readout_wire_Q1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "readout_wire_Q1_path"
                    ]
                ]
            ]
        ])
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Polyline1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "readout_wire_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.SweepAlongPath(
        [
            "NAME:Selections",
            "Selections:="		, "readout_wire_Q1,readout_wire_Q1_path",
            "NewPartsModelFlag:="	, "UseSourcePart"
        ], 
        [
            "NAME:PathSweepParameters",
            "DraftAngle:="		, "0deg",
            "DraftType:="		, "Round",
            "CheckFaceFaceIntersection:=", False,
            "TwistAngle:="		, "0deg"
        ])
    oEditor.CreatePolyline( 
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, False,
            [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="			, "0.0007875",
                    "Y:="			, "0.00187",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.0007625",
                    "Y:="			, "0.00187",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.00068",
                    "Y:="			, "0.001805",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.000585",
                    "Y:="			, "0.001805",
                    "Z:="			, "0"
                ]
            ],
            [
                "NAME:PolylineSegments",
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 0,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 1,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 2,
                    "NoOfPoints:="		, 2
                ]
            ],
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "None",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "0mm",
                "XSectionTopWidth:="	, "0mm",
                "XSectionHeight:="	, "0mm",
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Corner"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Polyline1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Polyline1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "readout_wire_sub_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreatePolyline( 
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, False,
            [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="			, "0.0007875",
                    "Y:="			, "0.001859",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.0007875",
                    "Y:="			, "0.001881",
                    "Z:="			, "0"
                ]
            ],
            [
                "NAME:PolylineSegments",
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 0,
                    "NoOfPoints:="		, 2
                ]
            ],
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "None",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "0mm",
                "XSectionTopWidth:="	, "0mm",
                "XSectionHeight:="	, "0mm",
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Corner"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Polyline1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0.9,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "readout_wire_sub_Q1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "readout_wire_sub_Q1_path"
                    ]
                ]
            ]
        ])
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Polyline1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "readout_wire_sub_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.SweepAlongPath(
        [
            "NAME:Selections",
            "Selections:="		, "readout_wire_sub_Q1,readout_wire_sub_Q1_path",
            "NewPartsModelFlag:="	, "UseSourcePart"
        ], 
        [
            "NAME:PathSweepParameters",
            "DraftAngle:="		, "0deg",
            "DraftType:="		, "Round",
            "CheckFaceFaceIntersection:=", False,
            "TwistAngle:="		, "0deg"
        ])
   
    for i in range(len(a)):
        pointx.append(0.0007875 + (a[i]+width/2)/1000000)
        pointy.append(0.002015 + y_smooth1[i]/1000000)
        pointyy.append(0.002015 + y_smooth2[i]/1000000)
    polylinepoints=["NAME:PolylinePoints"]
    for i in range(len(a)):
        add=["NAME:PLPoint"]
        add.append("X:=")
        add.append(str(pointx[i]))
        add.append("Y:=")
        add.append(str(pointy[i]))
        add.append("Z:=")
        add.append("0")    
        polylinepoints.append(add)
    for i in range(len(a)-1,-1,-1):
        add=["NAME:PLPoint"]
        add.append("X:=")
        add.append(str(pointx[i]))
        add.append("Y:=")
        add.append(str(pointyy[i]))
        add.append("Z:=")
        add.append("0")    
        polylinepoints.append(add)
    add=["NAME:PLPoint"]
    add.append("X:=")
    add.append(str(pointx[0]))
    add.append("Y:=")
    add.append(str(pointy[0]))
    add.append("Z:=")
    add.append("0")    
    polylinepoints.append(add)
    polylinesegments=["NAME:PolylineSegments"]
    for i in range(len(a)*2):
        add=["NAME:PLSegment"]
        add.append("SegmentType:=")
        add.append("Line")
        add.append("StartIndex:=")
        add.append(i)
        add.append("NoOfPoints:=")
        add.append(2)
        polylinesegments.append(add)

    oEditor.CreatePolyline( 
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, True,
            polylinepoints,
            polylinesegments,
            
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "None",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "0mm",
                "XSectionTopWidth:="	, "0mm",
                "XSectionHeight:="	, "0mm",
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Corner"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Rectangle1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    type(oEditor.CreatePolyline)
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Rectangle1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "pad_top_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
            
    pointx=[]
    pointy=[]
    pointyy=[]
    for i in range(len(a)):
        pointx.append(0.0007875 + (a[i]+width/2)/1000000) 
        pointy.append(0.002015 + y_smooth3[i]/1000000) 
        pointyy.append(0.002015 + y_smooth4[i]/1000000) 
    polylinepoints=["NAME:PolylinePoints"]
    for i in range(len(a)):
        add=["NAME:PLPoint"]
        add.append("X:=")
        add.append(str(pointx[i]))
        add.append("Y:=")
        add.append(str(pointy[i]))
        add.append("Z:=")
        add.append("0")    
        polylinepoints.append(add)
    for i in range(len(a)-1,-1,-1):
        add=["NAME:PLPoint"]
        add.append("X:=")
        add.append(str(pointx[i]))
        add.append("Y:=")
        add.append(str(pointyy[i]))
        add.append("Z:=")
        add.append("0")    
        polylinepoints.append(add)
    add=["NAME:PLPoint"]
    add.append("X:=")
    add.append(str(pointx[0]))
    add.append("Y:=")
    add.append(str(pointy[0]))
    add.append("Z:=")
    add.append("0")    
    polylinepoints.append(add)
    polylinesegments=["NAME:PolylineSegments"]
    for i in range(len(a)*2):
        add=["NAME:PLSegment"]
        add.append("SegmentType:=")
        add.append("Line")
        add.append("StartIndex:=")
        add.append(i)
        add.append("NoOfPoints:=")
        add.append(2)
        polylinesegments.append(add)


    oEditor.CreatePolyline( 
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, True,
            polylinepoints,
            polylinesegments,
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "None",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "0mm",
                "XSectionTopWidth:="	, "0mm",
                "XSectionHeight:="	, "0mm",
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Corner"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Rectangle1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Rectangle1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "pad_bot_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:="		, True,
            "XStart:="		, "0.000675",
            "YStart:="		, "0.001675",
            "ZStart:="		, "0",
            "Width:="		, "0.00065",
            "Height:="		, "0.00065",
            "WhichAxis:="		, "Z"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Rectangle1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Rectangle1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "rect_pk_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:="		, True,
            "XStart:="		, "0.0007875",
            "YStart:="		, "0.001865",
            "ZStart:="		, "0",
            "Width:="		, "0.0001",
            "Height:="		, "1e-05",
            "WhichAxis:="		, "Z"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Rectangle1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Rectangle1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "readout_connector_pad_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreatePolyline( 
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, True,
            [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001417",
                    "Y:="			, "0.00194",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001347",
                    "Y:="			, "0.00194",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001347",
                    "Y:="			, "0.00193",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001337",
                    "Y:="			, "0.00193",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001337",
                    "Y:="			, "0.00194",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001337",
                    "Y:="			, "0.00195",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001347",
                    "Y:="			, "0.00195",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001417",
                    "Y:="			, "0.00195",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001417",
                    "Y:="			, "0.00194",
                    "Z:="			, "0"
                ]
            ],
            [
                "NAME:PolylineSegments",
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 0,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 1,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 2,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 3,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 4,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 5,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 6,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 7,
                    "NoOfPoints:="		, 2
                ]
            ],
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "None",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "0mm",
                "XSectionTopWidth:="	, "0mm",
                "XSectionHeight:="	, "0mm",
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Corner"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Polyline1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Polyline1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "cl_metal_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreatePolyline(
        [
            "NAME:PolylineParameters",
            "IsPolylineCovered:="	, True,
            "IsPolylineClosed:="	, True,
            [
                "NAME:PolylinePoints",
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001423",
                    "Y:="			, "0.001934",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001353",
                    "Y:="			, "0.001934",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001353",
                    "Y:="			, "0.001924",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001331",
                    "Y:="			, "0.001924",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001331",
                    "Y:="			, "0.001956",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001423",
                    "Y:="			, "0.001956",
                    "Z:="			, "0"
                ],
                [
                    "NAME:PLPoint",
                    "X:="			, "0.001423",
                    "Y:="			, "0.001934",
                    "Z:="			, "0"
                ]
            ],
            [
                "NAME:PolylineSegments",
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 0,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 1,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 2,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 3,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 4,
                    "NoOfPoints:="		, 2
                ],
                [
                    "NAME:PLSegment",
                    "SegmentType:="		, "Line",
                    "StartIndex:="		, 5,
                    "NoOfPoints:="		, 2
                ]
            ],
            [
                "NAME:PolylineXSection",
                "XSectionType:="	, "None",
                "XSectionOrient:="	, "Auto",
                "XSectionWidth:="	, "0mm",
                "XSectionTopWidth:="	, "0mm",
                "XSectionHeight:="	, "0mm",
                "XSectionNumSegments:="	, "0",
                "XSectionBendType:="	, "Corner"
            ]
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "Polyline1",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.ChangeProperty(
        [
            "NAME:AllTabs",
            [
                "NAME:Geometry3DAttributeTab",
                [
                    "NAME:PropServers", 
                    "Polyline1"
                ],
                [
                    "NAME:ChangedProps",
                    [
                        "NAME:Name",
                        "Value:="		, "cl_etcher_Q1"
                    ]
                ]
            ]
        ])
    oEditor = oDesign.SetActiveEditor("3D Modeler")
    oEditor.CreateRectangle(
        [
            "NAME:RectangleParameters",
            "IsCovered:="		, True,
            "XStart:="		, "0.000385",
            "YStart:="		, "0.001475",
            "ZStart:="		, "0",
            "Width:="		, "0.001238",
            "Height:="		, "0.00105",
            "WhichAxis:="		, "Z"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "ground_main_plane",
            "Flags:="		, "",
            "Color:="		, "(143 175 143)",
            "Transparency:="	, 0,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"aluminum\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor.CreateBox(
        [
            "NAME:BoxParameters",
            "XPosition:="		, "0.000385",
            "YPosition:="		, "0.001475",
            "ZPosition:="		, "-0.00075",
            "XSize:="		, "0.001238",
            "YSize:="		, "0.00105",
            "ZSize:="		, "0.00075"
        ], 
        [
            "NAME:Attributes",
            "Name:="		, "main",
            "Flags:="		, "",
            "Color:="		, "(186 186 205)",
            "Transparency:="	, 0.2,
            "PartCoordinateSystem:=", "Global",
            "UDMId:="		, "",
            "MaterialValue:="	, "\"silicon\"",
            "SurfaceMaterialValue:=", "\"\"",
            "SolveInside:="		, False,
            "ShellElement:="	, False,
            "ShellElementThickness:=", "0mm",
            "IsMaterialEditable:="	, True,
            "UseMaterialAppearance:=", False,
            "IsLightweight:="	, False
        ])
    oEditor.Subtract(
        [
            "NAME:Selections",
            "Blank Parts:="		, "ground_main_plane",
            "Tool Parts:="		, "readout_wire_sub_Q1,cl_etcher_Q1,rect_pk_Q1"
        ], 
        [
            "NAME:SubtractParameters",
            "KeepOriginals:="	, False
        ])
    oModule = oDesign.GetModule("BoundarySetup")
    oModule.AssignThinConductor(
        [
            "NAME:ThinCond1",
            "Objects:="		, ["readout_wire_Q1","pad_top_Q1","pad_bot_Q1","readout_connector_pad_Q1","cl_metal_Q1","ground_main_plane"],
            "Material:="		, "pec",
            "Thickness:="		, "200nm"
        ])
    oModule.AutoIdentifyNets()
    oModule = oDesign.GetModule("AnalysisSetup")
    oModule.InsertSetup("Matrix", 
        [
            "NAME:QubitTune",
            "AdaptiveFreq:="	, "5GHz",
            "SaveFields:="		, False,
            "Enabled:="		, True,
            [
                "NAME:Cap",
                "MaxPass:="		, 15,
                "MinPass:="		, 1,
                "MinConvPass:="		, 1,
                "PerError:="		, 0.1,
                "PerRefine:="		, 30,
                "AutoIncreaseSolutionOrder:=", True,
                "SolutionOrder:="	, "High",
                "Solver Type:="		, "Iterative"
            ]
        ])
    oModule = oDesign.GetModule("MeshSetup")
    oModule.InitialMeshSettings(
        [
            "NAME:MeshSettings",
            [
                "NAME:GlobalSurfApproximation",
                "CurvedSurfaceApproxChoice:=", "UseSlider",
                "SliderMeshSettings:="	, 5
            ],
            [
                "NAME:GlobalModelRes",
                "UseAutoLength:="	, True
            ],
            "MeshMethod:="		, "Auto",
            "UseLegacyFaceterForTauVolumeMesh:=", False,
            "DynamicSurfaceResolution:=", False,
            "UseFlexMeshingForTAUvolumeMesh:=", False,
            "EnablePrime:="		, False
        ])
    oProject.AnalyzeAll()
    oDesign = oProject.SetActiveDesign("Qubit1_q3d")
    now = datetime.now()
    formatted_now = now.strftime("%Y%m%d-%H_%M_%S")
    path = dir_path+'/'+str(formatted_now)+'.txt'
    path_conv = dir_path+'/'+str(formatted_now)+'.conv'
    oDesign.ExportConvergence("Setup", "", "CG", path_conv)
    oDesign.ExportMatrixData(path, "C", "", "Setup:LastAdaptive", "Original", "ohm", "nH", "farad", "mSie", 5000000000, "Maxwell", 0, False, 15, 20, 1)
    oDesktop.CloseProject(oProject.GetName())
    return path