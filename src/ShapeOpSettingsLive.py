"""
Select the settings for running the ShapeOpConstraintSolver live (i.e
it will iteratively update itself). All of the settings except Reset are optional.
When Reset is set to True to solver will reset and intialize, when it is set to
False the solver will iteratively run the solve step.
-
Authors: Anders Holden Deleuran (CITA/KADK), Mario Deuss (LGG/EPFL) 
Github: github.com/AndersDeleuran/ShapeOpGHPython
Updated: 150330
    Args:
        Iterations: The number of iterations to run each time the component updates (default = 5)
        Mass: The mass of the points (default = 1.00)
        Damping: Velocity damping (default = 1.00)
        TimeStep: The physics simulation time step (default = 0.10)
        UnaryVector: A vector which will apply a force to all points in its direction and magnitude (default = None).
        Dynamic: True to initialize the solver with dynamics (default = True).
        Pause: True to pause, False to unpause (default = False).
        Reset: True to Reset, False to run the solver live.
    Returns:
        Settings: A Python dictionary wrapping the settings.
"""


# Set component name
ghenv.Component.Name = "ShapeOpSettingsLive"
ghenv.Component.NickName = "SOSL"

# Check/set inputs
if Iterations is None:
    Iterations = 5
if Mass is None:
    Mass = 1.00
if Damping is None:
    Damping = 1.0
if TimeStep is None:
    TimeStep = 0.1
if Dynamic is None:
    Dynamic = True
if Reset is None:
    Reset = True
if Pause is None:
    Pause = False

# Wrap all settings in a dict
Settings = [{"mode":"live","iterations":Iterations,"mass":Mass,"damping":Damping,"timeStep":TimeStep,"dynamic":Dynamic,"reset":Reset,"pause":Pause,"unaryVector":UnaryVector},]

