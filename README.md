ShapeOpGHPython
================

Demonstration example of how to implement the [ShapeOp C++ library](http://shapeop.org/) in [Rhino/Grasshopper](http://www.grasshopper3d.com/) 64 Bit using [GHPython](http://www.food4rhino.com/project/ghpython) and the Python standard foreign function library [ctypes](https://docs.python.org/2/library/ctypes.html). The examples in these demos implement the [Plankton mesh library](https://github.com/Dan-Piker/Plankton). The implementation has the following assembly dependencies which will need to be installed on your system:

ghpython.gha <br/>
Plankton.dll <br/>
Plankton.gha <br/>
ShapeOp.dll <br/>
vcomp120.dll <br/>

**Installing ghpython.gha, Plankton.dll and Plankton.gh:**
1) Move the files to the Grasshopper Libraries folder (Grasshopper -> File -> Special Folders -> Components Folder).
2) Unblock them (Right-click the files individually -> Properties -> Unblock -> Ok ).


Note that the folder where the ShapeOp.dll and vcomp120.dll are located needs to be added to the Window path. We suggest placing them in the Grasshopper libraries folder and doing the following:

1) Navigate to "Control Panel\System and Security\System".<br/>
2) Click "Advanced System Settings".<br/>
3) Click "Environment Variables".<br/>
4) Append the Grasshopper libraries folder path to the Path variable (in the System variables list).<br/>
5) Restart Rhino.<br/>

The planarity rendering cluster uses a Kangaroo component. You will need to install Kangaroo (food4rhino.com/project/kangaroo) to use this. This is not a critical feature to the ShapeOp implementation.
