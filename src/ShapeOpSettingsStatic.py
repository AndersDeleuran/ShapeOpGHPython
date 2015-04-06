"""
Select the settings for running the ShapeOpConstraintSolver statically (i.e
it will run all the iterations in one go). In this case the solver is always
initalized without dynamics.
-
Authors: Anders Holden Deleuran (CITA/KADK), Mario Deuss (LGG/EPFL) 
Github: github.com/AndersDeleuran/ShapeOpGHPython
Updated: 150330
    Args:
        Iterations: The amount of iterations to run.
    Returns:
        Settings: A Python dictionary wrapping the settings.
"""


# Set component name
ghenv.Component.Name = "ShapeOpSettingsStatic"
ghenv.Component.NickName = "SOSS"


# Check/set inputs
if Iterations is None:
    Iterations = 50

# Wrap all settings in dict and output to GH
Settings = [{"mode":"static","iterations":Iterations},]