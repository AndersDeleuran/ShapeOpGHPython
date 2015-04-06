"""
Construct signatures which are used by the ShapeOpConstraintSolver
component to add and edit ShapeOp constraints.
-
Authors: Anders Holden Deleuran (CITA/KADK), Mario Deuss (LGG/EPFL) 
Github: github.com/AndersDeleuran/ShapeOpGHPython
Updated: 150330
    Args:
        ConstraintType:
            A string containing one of the following constraint types (see documentation for more info):
                -
                EdgeStrain = takes 2 indices forming an edge.
                TriangleStrain = takes 3 indices forming a triangle.
                TetrahedronStrain = takes 4 indices forming a tetrahedron.
                Area = takes 3 indices forming a triangle.
                Volume = takes 4 indices forming a tetrahedron.
                Bending = takes 4 indices of two neighboring triangles sharing an edge.
                Closeness = takes 1 index.
                Line = takes 2 or more indices.
                Plane = takes 3 or more indices.
                Circle = takes 3 or more indices.
                Sphere = takes 4 or more indices.
                Similarity = takes 1 or more indices.
                Rigid = takes 1 or more indices.
                Rectangle = takes 4 indices.
                Parallelogram = takes 4 indices.
                Laplacian = takes 2 or more indices, center vertex first, then the one ring neighborhood.
                LaplacianDisplacement = takes 2 or more indices, center vertex first, then the one ring neighborhood.
                AngleConstraint = takes 3 indices forming two consecutive edges.
        PointIndices:
            A datatree of indices of the points subject to the constraints.
        Weights:
            A list of weights of the constraints to be added relative to the other constraints in the ShapeOpSolver (if a single value is provided the same weight will be used).
        Scalars:
            A datatree of floats used to edit certain constraints after they have been created, rangeMin/rangeMax are multipliers (if a single list is provided the same scalars will be used).
                -
                EdgeStrain = The scalars have 3 entries: (1) the desired distance between the two constrained vertices; (2) rangeMin; (3) rangeMax.
                TriangleStrain = The scalars have 2 entries: (1) rangeMin; (2) rangeMax.
                TetrahedronStrain = The scalars have 2 entries: (1) rangeMin; (2) rangeMax.
                Area = The scalars have 2 entries: (1) rangeMin; (2) rangeMax.
                Volume = The scalars have 2 entries: (1) rangeMin; (2) rangeMax.
                Bending = The scalars have 2 entries: (1) rangeMin; (2) rangeMax.
                Closeness = The scalars have 3 entries, which are the desire coordinates of constrained vertex.
                Similarity = The scalars have 3 * n * m entries, where m is the number of candidate shapes that the constrained vertices should be similar to,and n is the number of points in each candidate shape (the same as the number of constrained vertices). Each block of 3 * n scalars provides the point coordinates of a candidate shape.
                Rigid = Same as for "Similarity", see above.
                AngleConstraint =The scalars have 2 entries: (1) minAngle; (2) maxAngle.
    Returns:
        ConstraintSigs: A Python dictionary which wraps all the data for constructing the constraints.
"""

import Rhino as rc

# Set component name
ghenv.Component.Name = "ShapeOpConstraintSignature"
ghenv.Component.NickName = "SOCSig"

if PointIndices.DataCount and ConstraintType and len(Weights):    
    
    # Make dict for storing shapeop constraint signature
    ConstraintSigs = {"type":ConstraintType, "pointIndices":[], "weights":[], "scalars":[]}
    
    # Convert PointIndices datatree to nested Python list and add to dict
    ConstraintSigs["pointIndices"] = [list(i) for i in PointIndices.Branches]
    
    # Add Scalars to dict if there are any
    if Scalars.DataCount:
        
        # Convert datatree to python list and ensure that length matches PointIndices
        scalars = [list(i) for i in Scalars.Branches]
        if len(scalars) != PointIndices.BranchCount:
            scalars = [list(Scalars.Branches[0]) for i in range(PointIndices.BranchCount)]
            
        # Case for point scalars datatree
        if isinstance(scalars[0][0],rc.Geometry.Point3d):
            for l in scalars:
                coords = []
                for pt in l:
                    coords.append(pt.X)
                    coords.append(pt.Y)
                    coords.append(pt.Z)
                ConstraintSigs["scalars"].append(coords)
                
        # Case for simple float datatree
        else:
            ConstraintSigs["scalars"] = scalars
            
    # Add weights to dict
    if len(Weights) != PointIndices.BranchCount:
        ConstraintSigs["weights"] = [Weights[0] for i in range(PointIndices.BranchCount)]
    else:
        ConstraintSigs["weights"] = Weights

    # Output to GH (wrap in list to send as one item)
    ConstraintSigs = [ConstraintSigs,]
    
else:
    ConstraintSigs = []