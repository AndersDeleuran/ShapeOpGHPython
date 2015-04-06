"""
Gets the vertex indices of the mesh which corresponds to the points of the AnchorGeo.
If the AnchorGeo is a curve/polyline/line its start-point will be used to identify 
which mesh vertex should be anchored and its end-point will be used to determine
which point to anchor the vertex to. If the AnchorGeo is point this will be used
as both identifier and anchor point. Use curve-types to interactively manipulate
anchoring positions and points for static positions.
-
Authors: Anders Holden Deleuran (CITA/KADK), Mario Deuss (LGG/EPFL) 
Github: github.com/AndersDeleuran/ShapeOpGHPython
Updated: 150401
    Args:
        Mesh: The mesh to extract vertex indices from.
        AnchorGeo: Geometry to use for anchoring mesh vertices (points or curve-type).
    Returns:
        PointIndices: The mesh with vertices to anchor.
        AnchorPts: The anchor points.
"""

import Rhino as rc
import Grasshopper as gh

# Set component name
ghenv.Component.Name = "ShapeOpAnchorsIndexer"
ghenv.Component.NickName = "SOAI"

if AnchorGeo and Mesh and not None in AnchorGeo:
    
    # Make output datatrees
    PointIndices = gh.DataTree[int]()
    AnchorPts = gh.DataTree[rc.Geometry.Point3d]()
    
    # Make mesh vertices point search list
    ptsList = rc.Collections.Point3dList(Mesh.Vertices.ToPoint3dArray())
    
    for i,ag in enumerate(AnchorGeo):
        
        # Make datatree path
        p = gh.Kernel.Data.GH_Path(i)
        
        # Get anchor start and end points
        if isinstance(ag,rc.Geometry.Curve):
            aPtS = ag.PointAtStart
            aPtE = ag.PointAtEnd
        elif isinstance(ag,rc.Geometry.Point3d):
            aPtS = ag
            aPtE = ag
            
        # Get index of points to anchor and add to PointIndices datatree
        aPtId = ptsList.ClosestIndex(aPtS)
        PointIndices.AddRange((aPtId,),p)
        
        # Add anchor end points to datatree
        AnchorPts.Add(aPtE,p)
        
else:
    PointIndices = []
    AnchorPts = []