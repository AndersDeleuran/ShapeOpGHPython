"""
Demonstration example of how to implement the ShapeOp C++ library (shapeop.org)
in Grasshopper using Python and the foreign function library ctypes (docs.python.org/2/library/ctypes).
Uses the Plankton mesh library (github.com/Dan-Piker/Plankton).
-
Name: ShapeOpGHPython_Dynamic_PlanarityAndCircle
Updated: 140924
Author: Anders Holden Deleuran (CITA/KADK)
Copyright: Mozilla Public License Version 2.0
Contact: adel@kadk.dk

    Args:
        Mesh: Mesh to optimize/form find.
        Anchors: List of points which to anchor.
        AnchorsT: List of points which to anchor to.
        AnchorW: Anchor constraint weight (0.0-2000-ish).
        LaplacianW: Laplacian constraint weight (0.0-2000-ish).
        PlanarityW: Planarity constraint weight (0.0-2000-ish).
        CircleW: Circle constraint weight (0.0-2000-ish).
        SubIterations: Amount of sub-iterations to run at each solve step (1-20-ish).
        Mass: Particle mass value (0.0-1.0).
        Damping: Particle damping value (0.0-1.0).
        TimeStep: TODO
        Dynamic: It True the solver is initialized using Mass and Damping.
        Run: Toggle the solver on/off.
        Reset: Resets the mesh and updates all constraints.
    Returns:
        Iterations: Number of iterative solve steps.
        Mesh: The optimized/form found mesh.
"""

import clr
import time
import Rhino as rc
import ctypes as ct
import Grasshopper as gh
from scriptcontext import sticky as st
so = ct.cdll.LoadLibrary("ShapeOp.dll")
clr.AddReferenceToFile("Plankton.gha")
import PlanktonGh as plgh


def addMeshVertexCoordinates(solver,mesh):
    
    """ Convert a Rhino mesh to a Plankton mesh and add its verticesto a ShapeOp solver """
    
    # Make plankton mesh and get its vertices and count
    pMesh = plgh.RhinoSupport.ToPlanktonMesh(Mesh)
    vertices = pMesh.Vertices
    vCount = vertices.Count
    
    # Make ctypes double array containing vertex coordinates
    vCoords = (ct.c_double * (vCount*3))()
    for i in range(vCount):
        b = 3*i
        vCoords[b] = float(vertices[i].X)
        vCoords[b+1] = float(vertices[i].Y)
        vCoords[b+2] = float(vertices[i].Z)
        
    # Add vertex coordinates to solver
    so.shapeop_setPoints(solver,ct.byref(vCoords),vCount)
    
    return pMesh,vCoords

def addAnchorConstraints(solver,pMesh,anchorsPts,weight):
    
    """ Add anchor/point closeness constraints to a Plankton mesh """
    
    if anchorsPts and weight > 0:
        
        anchorIds = (ct.c_int*len(anchorsPts))()
        for i,apt in enumerate(anchorsPts):
            for j in range(pMesh.Vertices.Count):
                vtxC = pMesh.Vertices[j].ToXYZ()
                vtxPt = rc.Geometry.Point3d(vtxC.X,vtxC.Y,vtxC.Z)
                if apt.DistanceTo(vtxPt) < 0.01:
                    aid = so.shapeop_addClosenessConstraint(solver,j,weight)
                    anchorIds[i] = aid
                    
        return anchorIds

def addLaplacianConstraints(solver,pMesh,weight):
    
    """ Add Laplacian constraints to a Plankton mesh """
    
    if weight > 0:
        
        for i in range(pMesh.Vertices.Count):
            
            # Get neighbour indices and amount
            neighboursPy = [i] + list(pMesh.Vertices.GetVertexNeighbours(i))
            amount = len(neighboursPy)
            
            # Make ctype integer array
            neighbours = (ct.c_int*amount)()
            for i,v in enumerate(neighboursPy):
                neighbours[i] = v
                
            # Add constraint
            so.shapeop_addUniformLaplacianConstraint(solver,ct.byref(neighbours),amount,1,weight)

def addPlanarityConstraints(solver,pMesh,weight):
    
    """ Add planarity constraints to a Plankton mesh """
    
    if weight > 0:
    
        faceList = pMesh.Faces
        for i in range(faceList.Count):
            
            # Get face vertices and amount
            faceVerticesPy = faceList.GetFaceVertices(i)
            amount = len(faceVerticesPy)
            
            # Convert to ctypes integer array
            faceVertices = (ct.c_int*amount)()
            for i,v in enumerate(faceVerticesPy):
                faceVertices[i] = v
                
            # Add constraints
            so.shapeop_addPlaneConstraint(solver,ct.byref(faceVertices),amount,weight)

def addCircleConstraints(solver,pMesh,weight):
    
    """ Add circle constraints to a Plankton mesh """
    
    if weight > 0:
        
        faceList = pMesh.Faces
        for i in range(faceList.Count):
            
            # Get face vertices and amount
            faceVerticesPy = faceList.GetFaceVertices(i)
            amount = len(faceVerticesPy)
            
            # Convert to ctypes integer array
            faceVertices = (ct.c_int*amount)()
            for i,v in enumerate(faceVerticesPy):
                faceVertices[i] = v
                
            # Add constraints
            so.shapeop_addCircleConstraint(solver,ct.byref(faceVertices),amount,weight)

def ghComponentTimer(run,interval):
    
    """ Update the component at the interval like using a GH timer """
    
    # Ensure interval is larger than zero
    if interval <= 0:
        interval = 1
        
    # Get the Grasshopper document and component that owns this script
    ghComp = ghenv.Component
    ghDoc = ghComp.OnPingDocument()
    
    # Define the callback function
    def callBack(ghDoc):
        ghComp.ExpireSolution(False)
        
    # Update the solution
    if run:
        ghDoc.ScheduleSolution(interval,gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack))

if Mesh:
    
    # Get GH component guid and make unique variable names for sticky keys
    guid = str(ghenv.Component.InstanceGuid)
    solver = "solver_" + guid
    pMesh = "pMesh_" + guid
    vCoords = "vCoords_" + guid
    anchors = "anchors_" + guid
    iterations = "iterations_" + guid
    
    # Make solver and add constraints
    if solver not in st:
        
        # Make ShapeOp solver
        st[solver] = so.shapeop_create()
        
        # Make plankton mesh and add its vertex coordinates to the solver
        st[pMesh],st[vCoords] = addMeshVertexCoordinates(st[solver],Mesh)
        
        # Add anchor closeness constraints which can be edited live
        st[anchors] = addAnchorConstraints(st[solver],st[pMesh],Anchors,AnchorW)
        
        # Add non-live editable constraints
        addLaplacianConstraints(st[solver],st[pMesh],LaplacianW)
        addPlanarityConstraints(st[solver],st[pMesh],PlanarityW)
        addCircleConstraints(st[solver],st[pMesh],CircleW)
        
        # Initialize the solver
        if Dynamic:
            so.shapeop_initDynamic(st[solver],Mass,Damping,TimeStep)
        else:
            so.shapeop_init(st[solver])
            
        # Make iteration counter
        st[iterations] = 0
        
    # Run solver live
    if Run:
        
        # Set new target anchor points
        if AnchorsT and st[anchors]:
            for i,id in enumerate(st[anchors]):
                apt = AnchorsT[i]
                apt = (ct.c_double*3)(apt.X,apt.Y,apt.Z)
                so.shapeop_editClosenessConstraint(st[solver],id,ct.byref(apt))
            
        # Solve and get the vertex coordinates
        startTime = time.time()
        so.shapeop_solve(st[solver],SubIterations)
        st[iterations] += 1
        so.shapeop_getPoints(st[solver],ct.byref(st[vCoords]),st[pMesh].Vertices.Count)
        print "SolveTime:",int((time.time()-startTime)*1000),'ms'
        
    # Set plankton mesh vertices
    for i in range(st[pMesh].Vertices.Count):
        b = i*3
        st[pMesh].Vertices.SetVertex(i,st[vCoords][b],st[vCoords][b+1],st[vCoords][b+2])
        
    # Convert plankton mesh to Rhino mesh and compute normals
    Mesh = plgh.RhinoSupport.ToRhinoMesh(st[pMesh])
    Mesh.FaceNormals.ComputeFaceNormals()
    Mesh.Normals.ComputeNormals()
    
    # Increment iterations
    Iterations = st[iterations]*SubIterations
    
    # Reset model
    if Reset:
        del st[solver]
        del st[pMesh]
        del st[vCoords]
        del st[anchors]
        del st[iterations]
        
    # Update the component
    ghComponentTimer(Run,5)