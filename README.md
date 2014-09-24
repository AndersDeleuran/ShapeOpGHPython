ShapeOpGHPython
================

Demonstration example of how to implement the [ShapeOp C++ geometry processing library](http://shapeop.org/) in [Rhino/Grasshopper](http://www.grasshopper3d.com/) 64 Bit using [GHPython](http://www.food4rhino.com/project/ghpython) and the Python standard foreign function library [ctypes](https://docs.python.org/2/library/ctypes.html). The examples in these demos implement the [Plankton mesh library](https://github.com/Dan-Piker/Plankton). The planarity rendering cluster uses a Kangaroo component. You will need to install Kangaroo to use this. This is not a critical feature to the ShapeOp implementation.

 The implementation thus has the following assembly dependencies which will need to be installed on your system:

ghpython.gha <br/>
Plankton.dll <br/>
Plankton.gha <br/>
ShapeOp.dll <br/>
vcomp120.dll <br/>

**Installing ghpython.gha, Plankton.dll and Plankton.gh**<br/>
1) Move the files to the Grasshopper Libraries folder "%appdata%\Grasshopper\Libraries". <br/>
2) Unblock them "Right-click the files individually -> Properties -> Unblock -> Ok". <br/>

**Adding Grasshopper Libraries folder to Python**<br/>
To use Plankton in a Python script you have to add the Grasshopper Libraries folder path to the list of directories which Python can access. You can do this [in the script itself](http://www.grasshopper3d.com/forum/topics/python-module-search-path?commentId=2985220%3AComment%3A1104512) or hardcode it via the Rhino Python script editor:

1) In Rhino type in the command "EditPythonScript". <br/>
2) In this Python editor go "Tools -> Options -> Files". <br/>
3) Here you will see an overview of the directories which are currently referenced. <br/>
4) Add a reference to the Grasshopper Libraries folder. <br/>

**Installing  ShapeOp.dll and vcomp120.dll**<br/>
You can either place these files in the default Windows folder (C:\Windows) or the Grasshopper Libraries folder (remember to unblock the files). In the latter case you will have to add the Grasshopper Libraries folder path to the Window path:

1) Navigate to "Control Panel\System and Security\System".<br/>
2) Click "Advanced System Settings".<br/>
3) Click "Environment Variables".<br/>
4) Append the Grasshopper Libraries folder path to the Path variable (in the System variables list).<br/>
5) Restart Rhino.<br/>
