ShapeOp_GHPython
================

Demonstration example of how to implement the ShapeOp C++ library (shapeop.org) in Grasshopper using Python and the foreign function library ctypes (docs.python.org/2/library/ctypes). Implements the Plankton mesh library (github.com/Dan-Piker/Plankton).

Assembly Dependecies:

ghpython.gha <br />
Plankton.dll <br />
Plankton.gha <br />
ShapeOp.dll <br />
vcomp120.dll <br />

Note that the folder where the ShapeOp.dll and vcomp120.dll are located needs to be added to the Window path. We suggest placing them in the Grasshopper libraries folder and doing the following:

1) Navigate to "Control Panel\System and Security\System".
2) Click "Advanced System Settings".
3) Click "Environment Variables".
4) Append the Grasshopper libraries folder path to the Path variable (in the System variables list).
5) Restart Rhino.

The planarity rendering cluster uses a Kangaroo component. You will need to install Kangaroo to use this. This is not a critical feature to the ShapeOp implementation.
