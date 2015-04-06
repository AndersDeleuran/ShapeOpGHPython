"""
Make a ShapeOp solver and solve a whole bunch of constraints!
-
Authors: Anders Holden Deleuran (CITA/KADK), Mario Deuss (LGG/EPFL) 
Github: github.com/AndersDeleuran/ShapeOpGHPython
Updated: 150402
    Args:
        ConstraintSigs: Signatures used for adding and editing constaints.
        Points: Points which the solver will operate on. ConstraintSigs should be constructed using the indices of this list.
        Settings: A list of settings which will be used to set up and run the solver..
    Returns:
        Iterations: The number of iterations the solver has run.
        ConstraintCount: The total number of contraints which are being solved.
        Points: The constrained points after solving.
"""

import Rhino as rc
import ctypes as ct
import Grasshopper as gh
from scriptcontext import sticky as st
so = ct.cdll.LoadLibrary("ShapeOp.0.1.0.dll")

# Set component name
ghenv.Component.Name = "ShapeOpConstraintSolver"
ghenv.Component.NickName = "SOSolver"

def makeSoSolver(points):
    
    """ Make ShapeOp solver and returns its ID and points coordinates ID """
    
    solver = so.shapeop_create()
    
    # Make ctypes double array containing points coordinates
    ptCoords = (ct.c_double * (len(points)*3))()
    for i in range(len(points)):
        b = 3*i
        ptCoords[b] = float(points[i].X)
        ptCoords[b+1] = float(points[i].Y)
        ptCoords[b+2] = float(points[i].Z)
        
   # Add points coordinates to solver
    so.shapeop_setPoints(solver,ct.byref(ptCoords),len(points))
    
    return solver,ptCoords

def addSoConstraint(solver,constraintType,pointIndices,weight):
    
    """ Add a constraint: The solver is ID of shapeop solver, constraintType
    is name of constraint type to apply, pointIndices is list of points indices
    to operate on, weight is a float """
    
    t = ct.c_char_p(constraintType)
    ptIds = (ct.c_int * len(pointIndices))()
    for i,v in enumerate(pointIndices):
        ptIds[i] = v
        
    id = so.shapeop_addConstraint(solver,t,ct.byref(ptIds),len(pointIndices),weight)
    if id < 0 :
        raise LookupError("addSoConstraint failed adding a constraint of type "+constraintType)
    
    return id

def editSoConstraint(solver,constraintType,constraintId,scalars):
    
    """ Edit a constraint: solver is ID of shapeop solver, constraintType
    is name of constraint type to edit, constraintId is ID if the constraint.
    scalars is list of floats """
    
    t = ct.c_char_p(constraintType)
    scalarsC = (ct.c_double * len(scalars))()
    for i,s in enumerate(scalars):
        scalarsC[i] = s
        
    errCode = so.shapeop_editConstraint(solver,t,constraintId,ct.byref(scalarsC),len(scalars))
    if errCode != 0 :
        raise LookupError("editSoConstraint failed editing constraint. Check that SOGSig scalars are correctly defined.")

def addUnaryForce(solver,vector):
    
    """ Add a unary force to all points in the solver, only works dynamically """
    
    fv = (ct.c_double * 3)()
    fv[0] = float(vector.X)
    fv[1] = float(vector.Y)
    fv[2] = float(vector.Z)
    
    so.shapeop_addGravityForce(solver,fv)

def runSoSolverStatic(constraintSigs,points,settings):
    
    """ Run the ShapeOp solver statically and return the points """
    
    # Make ShapeOp solver
    solver,ptCoords = makeSoSolver(points)
    
    # Add constraints to the solver from the constraint signatures dictionary
    csCount = 0
    for csd in constraintSigs:
        for i in range(len(csd["pointIndices"])):
            csid = addSoConstraint(solver,csd["type"],csd["pointIndices"][i],csd["weights"][i])
            csCount += 1
            if csd["scalars"]:
                editSoConstraint(solver,csd["type"],csid,csd["scalars"][i])
                
    # Initialize and solve
    err_code = so.shapeop_init(solver)
    if err_code != 0 :
        raise LookupError("ShapeOp initialization failed.")
    err_code = so.shapeop_solve(solver,settings["iterations"])
    if err_code != 0 :
        raise LookupError("ShapeOp solve failed.")
    
    # Update and return the points list
    so.shapeop_getPoints(solver,ct.byref(ptCoords),len(points))
    for i in range(len(points)):
        b = i*3
        points[i] = rc.Geometry.Point3d(ptCoords[b],ptCoords[b+1],ptCoords[b+2])
        
    # Delete solver
    so.shapeop_delete(solver)
    
    return points,settings["iterations"],csCount

def runSoSolverLive(ghenv,constraintSigs,points,settings):
    
    """ Run the ShapeOp solver cyclically (live) and return the points """
    
    # Get GH component guid and make unique variable names for sticky keys
    guid = str(ghenv.Component.InstanceGuid) + str(ghdoc.Path)
    solver = "solver_" + guid
    ptCoords = "vCoords_" + guid
    count = "count_" + guid
    editableCS = "editableCS" + guid
    csCount = "csCount_" + guid
    
    if settings["reset"]:
        
        # Delete old solver
        if solver in st:
            so.shapeop_delete(st[solver])
            
        # Make ShapeOp solver
        st[solver],st[ptCoords] = makeSoSolver(points)
        
        # Add constraints to the solver from the constraint signatures dictionary
        st[editableCS] = []
        st[csCount] = 0
        for i,csd in enumerate(constraintSigs):
            for j in range(len(csd["pointIndices"])):
                csid = addSoConstraint(st[solver],csd["type"],csd["pointIndices"][j],csd["weights"][j])
                st[csCount] += 1
                if csd["scalars"]:
                    editSoConstraint(st[solver],csd["type"],csid,csd["scalars"][j])
                    st[editableCS].append((i,j,csid))
                    
        # Add unary force
        if settings['unaryVector']:
            addUnaryForce(st[solver],settings['unaryVector'])
        
        # Initialize solver
        err_code = 0
        if settings["dynamic"]:
            err_code = so.shapeop_initDynamic(st[solver],settings["mass"],settings["damping"],settings["timeStep"])
        else:
            err_code = so.shapeop_init(st[solver])
        if err_code != 0 :
            raise LookupError("ShapeOp init failed. Check that each point is constrained.")
        
        # Reset count
        st[count] = 0
        
        # Set component message
        ghenv.Component.Message = None
        
    else:
        
        # Update editable constraints
        for l in st[editableCS]:
            csdIndex,scalarsIndex,csid = l[0],l[1],l[2]
            scalars = constraintSigs[csdIndex]["scalars"]
            t = constraintSigs[csdIndex]["type"]
            editSoConstraint(st[solver],t,csid,scalars[scalarsIndex])
            
        # Solve and update the Grasshopper component (ie. update cyclically)
        err_code = so.shapeop_solve(st[solver],settings["iterations"])
        if err_code != 0 :
            raise LookupError("ShapeOp solve failed.")
        ghComponentTimer(ghenv,settings["pause"],10)
        
        # Increment count
        st[count] += 1*settings["iterations"]
        
        # Set component message
        message = "Solver is Running Live"
        if settings["pause"]:
            message = "Solver is Paused"
        ghenv.Component.Message = message
        
    # Update and return the points list
    so.shapeop_getPoints(st[solver],ct.byref(st[ptCoords]),len(points))
    for i in range(len(points)):
        b = i*3
        points[i] = rc.Geometry.Point3d(st[ptCoords][b],st[ptCoords][b+1],st[ptCoords][b+2])
        
    return points,st[count],st[csCount]

def ghComponentTimer(ghenv,pause,interval):
    
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
    if not pause:
        ghDoc.ScheduleSolution(interval,gh.Kernel.GH_Document.GH_ScheduleDelegate(callBack))

# Check GH input parameters
if ConstraintSigs and Points and Settings:
    
    # Run solver statically (i.e. only one GH iteration)
    if Settings["mode"] == "static":
        Points,Iterations,ConstraintCount = runSoSolverStatic(ConstraintSigs,Points,Settings)
        
    # Run solver live (i.e. the solver component will cyclically update)
    elif Settings["mode"] == "live":
        Points,Iterations,ConstraintCount = runSoSolverLive(ghenv,ConstraintSigs,Points,Settings)