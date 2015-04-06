"""
Extract vertex indices from a mesh using various patterns.
-
Authors: Anders Holden Deleuran (CITA/KADK), Mario Deuss (LGG/EPFL) 
Github: github.com/AndersDeleuran/ShapeOpGHPython
Updated: 150401
    Args:
        Pattern:
            The vertex indices pattern to extract from the mesh:
                -
                faceVertices = vertex indices for each face.
                vertexNeighbours = neighbour vertex indices for each vertex.
                edgeVertices = vertex indices for each edge.
                verticesAll = vertex indices for each vertex (flat list).
                verticesEach = vertex indices for each vertex (datatree).
                edgeFaceVertices = neighbour face-vertex indices for each edge.
                faceAngleVertices = neighbour vertices for each vertex corner for each face.
                nakedVertices = vertices on the perimeter of the mesh, sorted by closed loops.
        Mesh: The mesh to extract vertex indices from.
    Returns:
        PointIndices: The vertex indices pattern.
"""

import Grasshopper as gh

# Set component name
ghenv.Component.Name = "ShapeOpMeshIndexer"
ghenv.Component.NickName = "SOMI"

def getFaceVertices(mesh):
    
    """ Get datatree with the face vertex indices for each face in a mesh """
    
    faceVertices = gh.DataTree[int]()
    
    for i in range(Mesh.Faces.Count):
        fl = Mesh.Faces.Item[i]
        if fl.IsQuad:
            fIDs = (fl.A,fl.B,fl.C,fl.D)
        else:
            fIDs = (fl.A,fl.B,fl.C)
        faceVertices.AddRange(fIDs,gh.Kernel.Data.GH_Path(i))
        
    return faceVertices

def getVertexNeighbours(mesh):
    
    """ Get datatree with the vertex plus vertex neighbour indices
    for each vertex in a mesh """
    
    vertexNeighbours = gh.DataTree[int]()
    
    for i in range(Mesh.Vertices.Count):
        vnIDs = [i] + list(Mesh.Vertices.GetConnectedVertices(i))
        vertexNeighbours.AddRange(vnIDs,gh.Kernel.Data.GH_Path(i))
        
    return vertexNeighbours

def getEdgeVertices(mesh):
    
    """ Get datatree with the edge vertex indices for each edge in mesh """
    
    # Get edge vertices
    edges = []
    for i in range(Mesh.Vertices.Count):
        neighbours = Mesh.Vertices.GetConnectedVertices(i)
        for n in neighbours:
            if n > i:
                edges.append((i,n))
                
    # Make datatree
    edgeVertices = gh.DataTree[int]()
    for i,e in enumerate(edges):
        edgeVertices.AddRange(e,gh.Kernel.Data.GH_Path(i))
        
    return edgeVertices

def getVerticesEach(mesh):
    
    """ Get datatree with the index of each vertex in a mesh """
    
    verticesEach = gh.DataTree[int]()
    for i in range(Mesh.Vertices.Count):
        verticesEach.AddRange([i],gh.Kernel.Data.GH_Path(i))
        
    return verticesEach

def getVerticesAll(mesh):
    
    """ Get a list with all the vertex indices of a mesh """
    
    verticesAll = range(mesh.Vertices.Count)
    
    return verticesAll

def getEdgeFaceVertices(mesh):
    
    """ Get datatree with the four/six face vertex indices for each mesh edge, 
    which is used to construct the shapeop bending constraint signature """
    
    # Make GH datatree
    edgeFaceVerticesPtIDs = gh.DataTree[int]()
    
    for i in range(mesh.TopologyEdges.Count):
        
        p = gh.Kernel.Data.GH_Path(i)
        
        if len(mesh.TopologyEdges.GetConnectedFaces(i)) == 2:
            
            # Get edge vertex indices
            tVts = mesh.TopologyEdges.GetTopologyVertices(i)
            eVtA = mesh.TopologyVertices.MeshVertexIndices(tVts.I)[0]
            eVtB = mesh.TopologyVertices.MeshVertexIndices(tVts.J)[0]
            eVts = set((eVtA,eVtB))
            
            # Get edge face vertex index
            fA,fB = mesh.TopologyEdges.GetConnectedFaces(i)
            fVtsA = mesh.Faces.GetTopologicalVertices(fA)
            fVtsB = mesh.Faces.GetTopologicalVertices(fB)
            fVtsA = [mesh.TopologyVertices.MeshVertexIndices(i)[0] for i in fVtsA]
            fVtsB = [mesh.TopologyVertices.MeshVertexIndices(i)[0] for i in fVtsB]
            fVts = set(fVtsA + fVtsB)
            
            # Get the face indices which are not part of the edge
            fVts = list(fVts - eVts)
            
            # Make the bending constraint point indices list
            eFVIDs = list(eVts) + fVts
            edgeFaceVerticesPtIDs.AddRange(eFVIDs,p)
            
            
    return edgeFaceVerticesPtIDs

def getFaceAngleVertices(mesh):
    
    """ Get datatree with the face angle vertex indices for each face in a mesh """
    
    faceVertices = gh.DataTree[int]()
    
    n = 0
    for i in range(Mesh.Faces.Count):
        fl = Mesh.Faces.Item[i]
        if fl.IsQuad:
            faceVertices.AddRange((fl.A,fl.B,fl.D),gh.Kernel.Data.GH_Path(n+0))
            faceVertices.AddRange((fl.B,fl.C,fl.A),gh.Kernel.Data.GH_Path(n+1))
            faceVertices.AddRange((fl.C,fl.D,fl.B),gh.Kernel.Data.GH_Path(n+2))
            faceVertices.AddRange((fl.D,fl.A,fl.C),gh.Kernel.Data.GH_Path(n+3))
            n += 4
        else:
            faceVertices.AddRange((fl.A,fl.B,fl.C),gh.Kernel.Data.GH_Path(n+0))
            faceVertices.AddRange((fl.B,fl.C,fl.A),gh.Kernel.Data.GH_Path(n+1))
            faceVertices.AddRange((fl.C,fl.A,fl.B),gh.Kernel.Data.GH_Path(n+2))
            n += 3
            
    return faceVertices

def getNakedVertices(mesh):
    
    """ Get datatree with indices of naked vertices, sorted by closed loops """
    
    # Get naked edges as polylines and naked edge status
    npl = list(mesh.GetNakedEdges())
    nvts = mesh.GetNakedEdgePointStatus()
    
    # Sort the naked vertices by which polyline they belong to
    nakedVertices = gh.DataTree[int]()
    for i,v in enumerate(nvts):
        if v:
            for j,pl in enumerate(npl):
                p = gh.Kernel.Data.GH_Path(j)
                if pl.Contains(mesh.Vertices.Item[i]):
                    nakedVertices.Add(i,p)
                    
    return nakedVertices

if Mesh and Pattern:
    
    if Pattern == "faceVertices":
        PointIndices = getFaceVertices(Mesh)
        
    elif Pattern == "edgeVertices":
        PointIndices = getEdgeVertices(Mesh)
        
    elif Pattern == "vertexNeighbours":
        PointIndices = getVertexNeighbours(Mesh)
        
    elif Pattern == "verticesEach":
        PointIndices = getVerticesEach(Mesh)
        
    elif Pattern == "verticesAll":
        PointIndices = getVerticesAll(Mesh)
        
    elif Pattern == "edgeFaceVertices":
        PointIndices = getEdgeFaceVertices(Mesh)
        
    elif Pattern == "faceAngleVertices":
        PointIndices = getFaceAngleVertices(Mesh)
        
    elif Pattern == "nakedVertices":
        PointIndices = getNakedVertices(Mesh)
else:
    PointIndices = []