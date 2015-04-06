ShapeOpGHPython
================

Implementation of the [ShapeOp C++ geometry processing library](http://shapeop.org/) in [Rhino/Grasshopper](http://www.grasshopper3d.com/) 64 Bit using [GHPython](http://www.food4rhino.com/project/ghpython) and the Python standard foreign function library [ctypes](https://docs.python.org/2/library/ctypes.html). The implementation has the following dependencies which will need to be installed on your system (see dependencies folder):

ghpython.gha <br/>
ShapeOp.dll <br/>
vcomp120.dll <br/>

**Installing ghpython.gha**<br/>
1) Move the file to the Grasshopper Libraries folder "%appdata%\Grasshopper\Libraries". <br/>
2) Unblock it "Right-click the file -> Properties -> Unblock -> Ok". <br/>

**Installing  ShapeOp.dll and vcomp120.dll**<br/>
You can either place these files in the default Windows folder (C:\Windows) or the Grasshopper Libraries folder. Remember to unblock the files in both cases. If you place the files in the Grasshopper libraries folder you need to do the following:

Add the Grasshopper Libraries folder path to the Windows path:

1) Navigate to "Control Panel\System and Security\System".<br/>
2) Click "Advanced System Settings".<br/>
3) Click "Environment Variables".<br/>
4) Append the Grasshopper Libraries folder path to the Path variable (in the System variables list).<br/>
5) Restart Rhino.<br/>

Add the Grasshopper Libraries folder path to the RhinoPython paths list:

1) In Rhino type in the command "EditPythonScript".<br/>
2) In this Python editor go "Tools -> Options -> Files".<br/>
3) Here you will see an overview of the directories which are currently referenced.<br/>
4) Add a reference to the Grasshopper Libraries folder (it may be hidden, of so unhide it).<br/>


**Video Demo**<br/>
https://www.youtube.com/watch?v=3XlfwB4OYGw
