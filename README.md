# Simple Lattice Mirror

## Overview

Simple Lattice Mirror is a Blender add-on that applies symmetry to selected lattice control points. This add-on provides functionality to mirror lattice object control points along a specified axis.

### Compatibility

This add-on is compatible with Blender 3.x.

### Key Features

- **SimpleLatticeMirrorPanel**: Adds a new panel to Blender's UI, allowing users to select the axis and toggle for mirroring.
- **SimpleLatticeMirrorPreferences**: Manages add-on settings, including the threshold for identifying symmetric points and enabling debug logging.
- **Properties**:
  - `simple_lattice_mirror_axis`: Property to select the axis for mirroring (X, Y, Z).
  - `simple_lattice_mirror_toggle`: Property to toggle mirroring on or off (ON, OFF).

### File Structure

- `simple_lattice_mirror/__init__.py`: Entry point of the add-on, containing functions to register the add-on with Blender.
- `simple_lattice_mirror/SimpleLatticeMirrorPanel.py`: Defines the class that adds a new panel to Blender's UI.
- `simple_lattice_mirror/SimpleLatticeMirrorPreferences.py`: Defines the class that manages the add-on's settings.
- `simple_lattice_mirror/main.py`: Contains the logic to perform mirroring of lattice control points.
- `simple_lattice_mirror/point_utils.py`: Contains utility functions related to lattice control point operations.
- `simple_lattice_mirror/log.py`: Provides functionality related to debugging and logging.


