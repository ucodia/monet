# NextDraw Python API Reference

- [Introduction](#introduction)
- [The Bantam Tools NextDraw](#the-bantam-tools-nextdraw)
- [Installation](#installation)
- [Quick start: Plotting SVG](#quick-start-plotting-svg)
- [Quick start: Interactive XY](#quick-start-interactive-xy)
- [Example scripts](#example-scripts)
- [Setting options](#setting-options)
- [Options (General)](#options-general)
    - [handling](#handling)
    - [speed_pendown](#speed_pendown)
    - [speed_penup](#speed_penup)
    - [accel](#accel)
    - [pen_pos_down](#pen_pos_down)
    - [pen_pos_up](#pen_pos_up)
    - [pen_rate_lower](#pen_rate_lower)
    - [pen_rate_raise](#pen_rate_raise)
    - [model](#model)
    - [penlift](#penlift)
    - [homing](#homing)
    - [port](#port)
    - [port_config](#port_config)
- [Options (Plot)](#options-plot)
    - [mode](#mode)
    - [utility_cmd](#utility_cmd)
    - [dist](#dist)
    - [layer](#layer)
    - [copies](#copies)
    - [page_delay](#page_delay)
    - [auto_rotate](#auto_rotate)
    - [preview](#preview)
    - [rendering](#rendering)
    - [reordering](#reordering)
    - [random_start](#random_start)
    - [hiding](#hiding)
    - [report_time](#report_time)
    - [digest](#digest)
    - [webhook](#webhook)
    - [webhook_url](#webhook_url)
- [Options (Interactive)](#options-interactive)
    - [units](#units)
- [Additional parameters](#additional-parameters)
- [Python variables](#python-variables)
- [Error handling](#error-handling)
    - [Keyboard interrupts](#keyboard-interrupts)
- [Functions: General](#functions-general)
    - [load_config](#load_config)
- [Functions: Plot](#functions-plot)
    - [plot_setup](#plot_setup)
    - [plot_run](#plot_run)
- [Functions: Interactive](#functions-interactive)
    - [interactive](#interactive)
    - [connect](#connect)
    - [disconnect](#disconnect)
    - [update](#update)
    - [goto](#goto)
    - [moveto](#moveto)
    - [lineto](#lineto)
    - [go](#go)
    - [move](#move)
    - [line](#line)
    - [penup](#penup)
    - [pendown](#pendown)
    - [draw_path](#draw_path)
    - [delay](#delay)
    - [block](#block)
    - [current_pos](#current_pos)
    - [turtle_pos](#turtle_pos)
    - [current_pen, turtle_pen](#current_pen-turtle_pen)
    - [usb_command, usb_query](#usb_command-usb_query)
- [Migrating from AxiDraw API](#migrating-from-axidraw-api)
- [API Changelog](#api-changelog)
- [Copyright](#copyright)

---

## Introduction

The Bantam Tools NextDraw Python library is an API for the [Bantam Tools NextDraw](https://www.bantamtools.com/nextdraw-series), designed to let you control the NextDraw from within your own Python scripts.

This Python module supports the NextDraw with two distinct control approaches:

- Plotting SVG files, and
- Interactive XY motion control through "moveto/lineto" type commands and vertex lists.

To distinguish between these two control methods, we refer to them as the **Plot** context and the **Interactive** context, for plotting SVG files or using XY motion control commands, respectively. Certain options and functions can only be used in one or the other context. Please see [Quick start: Plotting SVG](#quick-start-plotting-svg) and [Quick start: Interactive XY](#quick-start-interactive-xy) for more information.

If you wish to use the NextDraw from the command line interface or within shell scripts, please see the [separate API documentation](https://bantam.tools/nd_cli) for the Bantam Tools NextDraw CLI.

## The Bantam Tools NextDraw

The [Bantam Tools NextDraw](https://www.bantamtools.com/nextdraw-series) drawing and handwriting machine is a proven and reliable computer-controlled plotter that provides versatile solutions to artists, innovators, and educators.

The Bantam Tools NextDraw is designed and manufactured by [Bantam Tools](https://www.bantamtools.com/) in Peekskill, New York.

For general information about getting started and operating the machine, please see the PDF user guide available [here](https://bantam.tools/ndguide). Please also see the [central documentation site](http://bantam.tools/nddocs) for additional resources.

NextDraw owners may request support through the [contact form](https://support.bantamtools.com/hc/en-us/requests/new) or [Discord chat](https://discord.gg/axhTzmr).

## Installation

### One line install

If you already have Python installed (versions 3.9 - 3.13), use the following in a terminal:

```
python -m pip install https://software-download.bantamtools.com/nd/api/nextdraw_api.zip
```

This installs both the NextDraw Python library and the [NextDraw CLI](https://bantam.tools/nd_cli). The link is permanent and kept up to date. The current release version is 1.5.0.

You may also want to [download the zip file](https://software-download.bantamtools.com/nd/api/nextdraw_api.zip) conventionally, since the download includes example Python scripts, an example configuration file, an example SVG file, and instructions for uninstalling the software.

### Alternate install

Download the API [from this permanent link](https://software-download.bantamtools.com/nd/api/nextdraw_api.zip). The current release version is 1.5.0.

Please see `Installation.txt` included with the download for full installation instructions.

Abbreviated instructions: Install [Python 3](https://www.python.org/downloads/). Unzip the archive, move into the directory, and use `python -m pip install .` to install the software.

### Upgrading

If you already have this software installed, the recommended method to upgrade is:

```
python -m pip install https://software-download.bantamtools.com/nd/api/nextdraw_api.zip --upgrade --upgrade-strategy eager
```

## Quick start: Plotting SVG

Typical usage:

```python
from nextdraw import NextDraw   # Import the module
nd1 = NextDraw()                # Create class instance
nd1.plot_setup(FILE_NAME)       # Load file & configure plot context
            # Plotting options can be set, here after plot_setup().
nd1.plot_run()                  # Plot the file
```

**Example 1:** Plot a file named `NextDraw_trivial.svg`:

```python
from nextdraw import NextDraw
nd1 = NextDraw()
nd1.plot_setup("NextDraw_trivial.svg")
nd1.plot_run()
```

**Example 2:** Plot two copies of an SVG document contained within a string called `input_svg`, with full reordering enabled, and collect the output SVG as a string:

```python
from nextdraw import NextDraw
nd1 = NextDraw()
nd1.plot_setup(input_svg)
nd1.options.reordering = 2
output_svg = nd1.plot_run(True)
```

`plot_run(True)` will generate output SVG. `output_svg` is a string equivalent to the contents of an SVG file.

Four lines of code are needed: import the module, create a class instance, load a file and select the **Plot** context, and begin plotting.

The API includes the ability to set a wide range of configuration options and a number of utility functions. The options available in the **Plot** context include those described in the [Options: General](#options-general) and [Options: Plot](#options-plot) sections. Options may be set at any point after `plot_setup()` and before `plot_run()`.

An SVG input is required for most operations outside the **Interactive** context. This SVG input may be the name (or full path) of an SVG file or a string containing an SVG document.

By default, no output SVG is returned as part of the plotting process. However, `plot_run(True)` returns a string containing the contents of an SVG file. Keeping that output SVG allows the capability to pause and subsequently resume a plot in progress, or to preview a plot. See further discussion under [`res_plot`](#res_plot) and [`rendering`](#rendering).

## Quick start: Interactive XY

**Example:** Draw a single line in Interactive context:

```python
from nextdraw import NextDraw   # import module
nd1 = NextDraw()                # Initialize class
nd1.interactive()               # Enter interactive context
if not nd1.connect():           # Open serial port to NextDraw;
    quit()                      #   Exit, if no connection.
                                # Absolute moves follow:
nd1.moveto(1, 1)                # Pen-up move to (1 inch, 1 inch)
nd1.lineto(2, 1)                # Pen-down move, to (2 inch, 1 inch)
nd1.moveto(0, 0)                # Pen-up move, back to origin.
nd1.disconnect()                # Close serial port to NextDraw
```

The **Interactive** context is a separate mode of operation that accepts direct XY motion control commands. It does not use an SVG file as input.

Interactive control requires a persistent session and only works from within a Python script.

Once the module is imported, call `interactive()` to enter the **Interactive** context. Use `connect()` to establish a USB connection (returns `True` when successful). Use `disconnect()` at the end of your session to terminate the USB session.

Options may be specified at any point after the `interactive()` call and will be applied when you call `connect()`. If you change options after calling `connect()`, use the `update()` method to process the changes before calling additional motion commands.

The options available in the **Interactive** context include those in [Options: General](#options-general) and [Options: Interactive](#options-interactive). The options in [Options: Plot](#options-plot) do not apply in the **Interactive** context.

## Example scripts

Run an example script by calling the following from the command line:

```
python plot_inline.py
```

Note that example scripts are not installed system-wide. For Python to find the file, it is easiest to call this command from within the directory where the file is located.

The `examples_py_nextdraw` folder in the [API download](#installation) contains a number of example scripts:

- `plot.py` -- Demonstrate "plot" mode in the **Plot** context, to plot an SVG file.
- `estimate_time.py` -- Demonstrate "plot" mode, to estimate the time to plot an SVG file.
- `plot_inline.py` -- Demonstrate "plot" mode, to create and plot SVG elements without a separate SVG file.
- `toggle.py` -- Demonstrate the "toggle" utility command (still in **Plot** context).
- `interactive_xy.py` -- Demonstrate basic XY motion commands in **Interactive** context.
- `interactive_draw_path.py` -- Demonstrate drawing continuous paths from coordinate lists in **Interactive** context.
- `interactive_penheights.py` -- Demonstrate setting the pen to different heights in **Interactive** context.
- `turtle_pos.py` -- Demonstrate out-of-bounds motion handling and querying physical and turtle positions.
- `low_level_usb.py` -- Demonstrate advanced low-level USB command features in **Interactive** context.
- `interactive_usb_com.py` -- Second example of low-level USB command features in **Interactive** context.
- `report_pos_inch.py` -- Report and print the current XY position of the carriage (inches).
- `report_pos_mm.py` -- Report and print the current XY position of the carriage (mm).
- `connect_error.py` -- Demonstrate using the option to [raise an exception](#error-handling) when certain errors are detected.

## Setting options

One or more options may be specified with the following syntax:

```python
options.option_name = value
```

**Example 1:** Set the pen-up position to 70% height before plotting, using the Plot context:

```python
from nextdraw import NextDraw
nd1 = NextDraw()
nd1.plot_setup("file.svg")
nd1.options.pen_pos_up = 70
nd1.plot_run()
```

**Example 2:** Set the pen-up position to 70% height before plotting, using the Interactive context:

```python
from nextdraw import NextDraw
nd1 = NextDraw()
nd1.interactive()
nd1.options.pen_pos_up = 70
if not nd1.connect():
    quit()
nd1.moveto(1, 1)
nd1.lineto(0, 0)
nd1.disconnect()
```

Most plotting options can be set directly like variables within Python. For options that you do not directly specify, the default value will be used.

Options should be set after initialization into either the **Plot** context or the **Interactive** context, with `plot_setup` or `interactive()` respectively.

The default value of most options are set within the `nextdraw_conf.py` configuration file. Beyond the documented options, the configuration file includes additional defaults that can be overridden with the supplementary [`params`](#additional-parameters) syntax.

A few specific options (including pen heights and plotting speed) can also be set by encoding settings into the SVG file via [NextDraw Layer Control](https://support.bantamtools.com/hc/en-us/articles/29473928061971).

The order of preference for options and parameters is:

1. Options and values specified in the SVG file (by layer names) overrule those specified by your script or in `nextdraw_conf.py`.
2. Options and values specified by your script overrule those in `nextdraw_conf.py`.

If you also use Inkscape for plotting SVG files, note that option values selected from within the Inkscape GUI are NOT consulted and do not affect plotting from outside Inkscape.

## Options (General)

The following general options can be set in either the **Plot** or **Interactive** contexts.

|Option|Description|
|---|---|
|[`handling`](#handling)|Specify handling mode for motion|
|[`speed_pendown`](#speed_pendown)|Maximum XY speed when the pen is down (plotting)|
|[`speed_penup`](#speed_penup)|Maximum XY speed when the pen is up|
|[`accel`](#accel)|Relative acceleration/deceleration speed|
|[`pen_pos_down`](#pen_pos_down)|Pen height when the pen is down (plotting)|
|[`pen_pos_up`](#pen_pos_up)|Pen height when the pen is up|
|[`pen_rate_lower`](#pen_rate_lower)|Speed of lowering the pen-lift motor|
|[`pen_rate_raise`](#pen_rate_raise)|Speed of raising the pen-lift motor|
|[`model`](#model)|Select plotter model of NextDraw hardware|
|[`penlift`](#penlift)|Pen lift servo configuration|
|[`homing`](#homing)|Enable automatic homing (where supported)|
|[`port`](#port)|Specify a USB port or NextDraw to use|
|[`port_config`](#port_config)|Override how the USB ports are located|

### handling

_Select Handling mode for motion_

**Syntax:** `options.handling = value`

Select one of four general Handling modes. The choice controls the overall scales of precision, speed, and acceleration.

Allowed values (integers from 1 to 4):

- `1` -- Technical drawing. **(DEFAULT)** Moderate top speed, medium-high maximum acceleration, and high precision.
- `2` -- Handwriting. Moderate top speed, very high maximum acceleration, fast pen-up speeds, and relatively low precision. Great for stipple drawings and short/curvy movements.
- `3` -- Sketching. High top speed, moderate maximum acceleration, fast pen-up speeds, and moderate precision. Good for long strokes.
- `4` -- Constant speed. Disables acceleration and moves the pen at a constant speed when down. Constant speed applies only when the pen is down; acceleration is used during pen-up travel.

**Default:** `1` (Technical drawing), set in `nextdraw_conf.py`.

Changing handling modes can cause a loss of relative position, reset the homed state, and lose track of local position offsets. Best practice is to use a single handling mode, or note that re-homing may be required after changing modes.

### speed_pendown

_Pen-down Movement Speed_

**Syntax:** `options.speed_pendown = value`

Specify the speed limit for the XY carriage when the pen is down, expressed as a percentage of maximum travel speed. Increasing this tends to greatly affect behavior at corners and precision but has a lesser impact on average speed.

Allowed values: Integers from 1 to 100. **Default:** `25`.

### speed_penup

_Pen-up Movement Speed_

**Syntax:** `options.speed_penup = value`

Specify the speed limit for the XY carriage when the pen is up, expressed as a percentage of maximum travel speed. Increasing this tends to have a minor effect on plot quality but can significantly affect total plotting time.

Allowed values: Integers from 1 to 100. **Default:** `75`.

### accel

_Acceleration Factor_

**Syntax:** `options.accel = value`

Specify the relative acceleration/deceleration speed as a percentage of maximum acceleration rate. Does not affect top speed but influences how long it takes to get to different speeds.

Allowed values: Integers from 1 to 100. Values below 35 are not recommended; consider using a lower `speed_pendown` value instead. **Default:** `75`.

### pen_pos_down

_Pen-down Position_

**Syntax:** `options.pen_pos_down = value`

Specify the height of the pen when lowered (plotting), expressed as a percentage of vertical travel.

Allowed values: Integers from 0 to 100. **Default:** `40`.

### pen_pos_up

_Pen-up Position_

**Syntax:** `options.pen_pos_up = value`

Specify the height of the pen when raised (not plotting), expressed as a percentage of vertical travel.

Allowed values: Integers from 0 to 100. **Default:** `60`.

### pen_rate_lower

_Pen Lowering Rate_

**Syntax:** `options.pen_rate_lower = value`

Specify the rate at which the pen is lowered, expressed as a relative percentage.

Allowed values: Integers from 1 to 100. **Default:** `50`.

### pen_rate_raise

_Pen Raising Rate_

**Syntax:** `options.pen_rate_raise = value`

Specify the rate at which the pen is raised, expressed as a relative percentage.

Allowed values: Integers from 1 to 100. **Default:** `75`.

### model

_Select plotter model_

**Syntax:** `options.model = value`

Select which specific plotter model you are using. This sets limits of travel and configures model-specific parameters. Movements are clipped to occur within these limits.

Allowed values (integers from 1 to 10):

- `1` -- AxiDraw V2, V3, or SE/A4
- `2` -- AxiDraw V3/A3 or SE/A3
- `3` -- AxiDraw V3 XLX
- `4` -- AxiDraw MiniKit
- `5` -- AxiDraw SE/A1
- `6` -- AxiDraw SE/A2
- `7` -- AxiDraw V3/B6
- `8` -- Bantam Tools NextDraw 8511 **(Default)**
- `9` -- Bantam Tools NextDraw 1117
- `10` -- Bantam Tools NextDraw 2234

**Default:** `8`. Model-specific parameters can be overridden via `overrides` in your configuration file or with the [`params` syntax](#additional-parameters).

### penlift

_Pen lift servo configuration_

**Syntax:** `options.penlift = value`

Select the hardware configuration for the pen-lift servo mechanism. Generally not needed unless using an AxiDraw with a brushless pen-lift servo upgrade.

Allowed values (integers from 1 to 3):

- `1` -- Default for model
- `2` -- Reserved for future use
- `3` -- Brushless upgrade

**Default:** `1`.

### homing

_Enable automatic homing (where supported)_

**Syntax:** `options.homing = value`

Automatic homing is enabled by default when you have selected a Bantam Tools NextDraw with the [`model`](#model) option. Set to `False` to disable automatic homing and use a manual homing process instead.

Allowed values: `True`, `False`. **Default:** `True`.

### port

_Specify a USB port or named NextDraw to use_

**Syntax:** `options.port = value`

By default, the software works with the first available NextDraw on USB. You can specify a machine using the USB port enumeration (e.g., `COM6` on Windows or `/dev/cu.usbmodem1441` on Mac) or by an assigned USB nickname.

**Default:** `None`.

### port_config

_Override how the USB ports are located_

**Syntax:** `options.port_config = value`

Allowed values (integers 0 and 1):

- `0` -- Do not override; use standard "port" option behavior **(DEFAULT)**
- `1` -- Address only the first NextDraw located via USB

**Default:** `0`.

## Options (Plot)

The following options can be set in the **Plot** context only, and are not applicable in the **Interactive** context.

|Option|Description|
|---|---|
|[`mode`](#mode)|Specify general mode of operation|
|[`utility_cmd`](#utility_cmd)|Specify which utility-mode command to use|
|[`dist`](#dist)|Distance input for certain utility commands|
|[`layer`](#layer)|Specify which layer(s) to plot in layers mode|
|[`copies`](#copies)|Specify the number of copies to plot|
|[`page_delay`](#page_delay)|Specify delay between pages, for multiple copies|
|[`auto_rotate`](#auto_rotate)|Enable auto-rotate when plotting|
|[`preview`](#preview)|Perform offline simulation of plot only|
|[`rendering`](#rendering)|Render motion when using preview|
|[`reordering`](#reordering)|Optimize plot order before plotting|
|[`random_start`](#random_start)|Randomize start positions of closed paths|
|[`hiding`](#hiding)|Enable hidden-line removal|
|[`report_time`](#report_time)|Report time and distance after the plot|
|[`digest`](#digest)|Return plot digest instead of full SVG|
|[`webhook`](#webhook)|Enable webhook alerts|
|[`webhook_url`](#webhook_url)|URL for webhook alerts|

### mode

_General mode of operation_

**Syntax:** `options.mode = value`

|Value|Description|
|---|---|
|`"plot"`|Plot the file. **(DEFAULT)**|
|`"layers"`|Plot a single layer (or set of layers), selected by `layer` option|
|`"cycle"`|A setup mode: Lower and then raise the pen|
|`"align"`|A setup mode: Raise pen, disable XY stepper motors|
|`"find_home"`|A setup mode: Perform automatic homing sequence|
|`"utility"`|Execute a utility command, specified by `utility_cmd` option|
|`"sysinfo"`|Query EBB firmware version and report system information|
|`"version"`|Report NextDraw software version number|
|`"res_plot"`|Resume a plot in progress, using stored plot progress data|

**Default:** `'plot'`.

#### plot

Plot the SVG file. This is the default mode and generally does not need to be explicitly specified.

#### layers

Plot a single layer (or set of layers), selected by the [`layer`](#layer) option. Only visible layers with names beginning with the selected number will plot. Sublayers and other named groups are not considered layers; only top-level layers can be addressed.

See the [NextDraw Layer Control](https://support.bantamtools.com/hc/en-us/articles/29473928061971) documentation for more information.

#### cycle

Lower the pen, wait 0.5 seconds, then raise it. Useful for setup before inserting a pen. An SVG file input is allowed but not required.

#### align

Raise the pen and disable XY stepper motors. Allows manual carriage movement to the home corner. An SVG file input is allowed but not required.

#### find_home

Perform the automatic homing sequence. Not usually necessary since the machine performs homing automatically when needed. An SVG file input is allowed but not required.

#### utility

Execute a utility command specified with the `utility_cmd` argument. An SVG file input is allowed but not required.

#### sysinfo

Query firmware version and report system information. An SVG file input is allowed but not required.

#### version

Query and report NextDraw software version. You can also read `nd1.version_string` or `nextdraw.__version__` directly.

#### res_plot

Resume a paused plot. The input SVG must contain a stored record of the progress (generated automatically when a plot is paused). Use the output SVG from a paused `plot_run(True)` as the input to the next `plot_setup()`.

Certain settings that affect plot order (including `model`, `handling`, `reordering`, `random_start`, `auto_rotate`, and `hiding`) cannot be changed between pausing and resuming a plot.

```python
import time
from nextdraw import NextDraw
nd1 = NextDraw()
nd1.plot_setup("file.svg")
output_svg = nd1.plot_run(True)
time.sleep(5)
nd1.plot_setup(output_svg)
nd1.options.mode = "res_plot"
nd1.plot_run()
```

### utility_cmd

_Specify the utility command to execute_

**Syntax:** `options.utility_cmd = "command_name"`

This option is only used when `mode` is set to `"utility"`.

|Value|Description|
|---|---|
|`"lower_pen"`|Lower the pen|
|`"raise_pen"`|Raise the pen|
|`"toggle"`|Toggle pen between up and down|
|`"walk_x"`|Walk carriage in X (inches)|
|`"walk_y"`|Walk carriage in Y (inches)|
|`"walk_mmx"`|Walk carriage in X (mm)|
|`"walk_mmy"`|Walk carriage in Y (mm)|
|`"walk_home"`|Walk carriage to origin|
|`"set_home"`|Set current position as origin|
|`"enable_xy"`|Enable XY stepper motors|
|`"disable_xy"`|Disable XY stepper motors|
|`"res_read"`|Read resume position of paused plot|
|`"res_adj_in"`|Adjust resume position (inches)|
|`"res_adj_mm"`|Adjust resume position (mm)|
|`"strip_data"`|Strip plotter/preview data from file|
|`"list_names"`|List connected NextDraw units|
|`"read_name"`|Read USB nickname **(DEFAULT)**|
|`"write_name"`|Write USB nickname|
|`"bootload"`|Enter EBB bootloader mode|

**Default:** `'read_name'`.

The walk commands are relative to the current position and are NOT checked for safe range of motion. Use caution. For full interactive XY movement, use the **Interactive** context instead.

The `write_name` command concatenates the name with the option, e.g. `"write_nameNorth"`. Names can be up to 16 characters. Writing an empty string clears the nickname.

The `res_read`, `res_adj_in`, and `res_adj_mm` commands populate the `res_dist` Python variable (in millimeters). The `list_names` command populates the `name_list` Python list variable.

### dist

_Distance for Walk and Adjust Resume Position utility commands_

**Syntax:** `options.dist = value`

Floating point number, positive or negative. Units depend on the utility command: millimeters for `walk_mmx`/`walk_mmy`/`res_adj_mm`, inches for `walk_x`/`walk_y`/`res_adj_in`. No limit checking is performed.

**Default:** `1.0`.

### layer

_Select layer(s) to plot when in layers mode_

**Syntax:** `options.layer = value`

Specify a number which indicates which layers will be plotted. Only layers whose names begin with the selected number will plot. While only a single integer value may be given, that value may match multiple layer names.

Allowed values: Integers from 1 to 1000. **Default:** `1`.

### copies

_Number of copies to plot_

**Syntax:** `options.copies = value`

If `copies` has a value other than 0, the plot will be repeated that number of times. A value of 0 begins a continuous sequence until the pause button is pressed.

Allowed values: Integers from 0 to 9999. **Default:** `1`.

### page_delay

_Delay between copies_

**Syntax:** `options.page_delay = value`

Specify the delay in seconds between subsequent plots when plotting multiple copies.

Allowed values: Non-negative numbers. **Default:** `15`.

### auto_rotate

_Enable auto-rotate_

**Syntax:** `options.auto_rotate = value`

By default, if the SVG page is taller than it is wide, it will print in landscape mode. Set to `False` to preserve plot orientation.

Allowed values: `True`, `False`. **Default:** `True`.

### preview

_Plot Preview_

**Syntax:** `options.preview = value`

An offline simulation mode where the serial port is not used and the NextDraw does not move. Useful for estimating plot duration (with `report_time`), rendering graphical previews, and performing preflight checks.

Allowed values: `True`, `False`. **Default:** `False`.

### rendering

_Enable preview rendering_

**Syntax:** `options.rendering = value`

When Plot Preview is enabled and output is collected, a rendered preview of pen motion can be added to the output SVG. This option controls whether that rendering is generated.

Allowed values: `True`, `False`. **Default:** `True`.

### reordering

_Specify level of plot optimization_

**Syntax:** `options.reordering = value`

Re-order elements in the input SVG before plotting to reduce pen-up travel. The optimization is layer-aware and changes are ephemeral (not saved to the output SVG).

Allowed values (integers 0 to 4):

- `0` -- Least; only connect adjoining paths **(DEFAULT)**
- `1` -- Basic; also reorder paths for speed
- `2` -- Full; also allow path reversal
- `3` -- Reserved (currently same as 2)
- `4` -- None; strictly preserve file order

**Default:** `0`.

### random_start

_Randomize start positions of closed paths_

**Syntax:** `options.random_start = True`

Randomizes start locations of closed paths, which can help hide seam-like visual artifacts where pen marks line up on repeated shapes.

Allowed values: `True`, `False`. **Default:** `False`.

### hiding

_Enable hidden-line removal_

**Syntax:** `options.hiding = True`

When enabled, the NextDraw software will plot paths based on their fill and stroke properties and whether they are occluded behind other objects. Requires additional processing time and does not preserve stroke orientation. Consider using [`reordering`](#reordering) with full reordering (`options.reordering = 2`).

Allowed values: `True`, `False`. **Default:** `False`.

### report_time

_Report time and distance_

**Syntax:** `options.report_time = value`

When enabled, prints a report of time and distance after each plot finishes. Also populates five Python variables:

|Variable|Meaning|
|---|---|
|`time_elapsed`|Elapsed time (s)|
|`time_estimate`|Estimated time (s)|
|`distance_pendown`|Distance with pen down (m)|
|`distance_total`|Total distance (m)|
|`pen_lifts`|Number of pen lifts|

Allowed values: `True`, `False`. **Default:** `False`.

### digest

_Plot digest output option_

**Syntax:** `options.digest = value`

When greater than 0, `plot_run(True)` returns a "Plob" (plot digest object) instead of the full SVG. The Plob is a restricted-format subset of SVG generated after removing hidden objects, flattening structure, applying transformations, cropping, reordering, etc.

Generating the Plob is destructive. Keep a copy of your original SVG.

Allowed values (integers 0 to 2):

- `0` -- Disabled **(DEFAULT)**
- `1` -- Output Plob instead of full SVG
- `2` -- Disable plots and previews; generate digest only

**Default:** `0`.

### webhook

_Enable webhook alerts_

**Syntax:** `options.webhook = value`

If enabled and an URL is provided via `webhook_url`, the software will POST to that URL when a plot completes. Data posted (JSON): `value1` (document name), `value2` (elapsed time), `value3` (port, if provided).

Allowed values: `True`, `False`. **Default:** `False`.

### webhook_url

_URL for webhook alerts_

**Syntax:** `options.webhook_url = value`

The URL to post data to if `webhook` is enabled. See section "6.7 Notifications settings" of the [Bantam Tools NextDraw User Guide](https://bantam.tools/ndguide) for setup instructions.

**Default:** `None`.

## Options (Interactive)

One option, `units`, applies only in the **Interactive** context.

### units

_Plot units_

**Syntax:** `options.units = value`

Set the units for movement commands in the **Interactive** context. If you change units after calling `connect()`, use `update()` to process the change.

Allowed values (integers from 0 to 2):

- `0` -- Inches **(DEFAULT)**
- `1` -- Centimeters
- `2` -- Millimeters

**Default:** `0`.

## Additional parameters

**Syntax:** `params.parameter_name = value`

As a supplement to the documented options, there are additional parameters in `nextdraw_conf.py` that are not normally adjusted. For any parameter that has a default value defined in the configuration file and does not have a documented option name, you can set it using the `params` syntax.

An example configuration file is in the API download at: `examples_config/nextdraw_conf_copy.py`

Many default parameter values have carefully chosen values. Proceed with caution when overriding them.

## Python variables

Certain public variables are provided by the `NextDraw()` class:

|Variable|Meaning|
|---|---|
|`version_string`|Software version string|
|`connected`|True if connected|
|`fw_version_string`|Firmware version string|
|`nickname`|Nickname of the connected machine, if any|
|`time_elapsed`|Time elapsed in `plot_run()`|
|`time_estimate`|Estimated total time of a plot|
|`distance_pendown`|Real or estimated pen-down distance|
|`distance_total`|Real or estimated distance moved|
|`pen_lifts`|Real or estimated count of pen lifts|
|`res_dist`|Resume position|
|`name_list`|List of connected machines|

`version_string` is available as soon as the class instance is created. `connected` is available in the **Interactive** context. `fw_version_string` and `nickname` are available after `plot_run()` (**Plot**) or `connect()` (**Interactive**).

## Error handling

This API allows you to configure whether certain error conditions raise a Python error. Some actions will always raise a `RuntimeError`, but others can be configured.

Set these variables to `True` before `plot_run()` or `connect()`:

|Variable|Raise error:|
|---|---|
|`errors.connect`|On failure to connect (default: `False`)|
|`errors.button`|When pause button is pressed (default: `False`)|
|`errors.keyboard`|On keyboard interrupt, if enabled (default: `False`)|
|`errors.disconnect`|On loss of USB connection (default: `False`)|
|`errors.power`|On loss of power (default: `False`)|
|`errors.homing`|On homing failure (default: `False`)|

Raising an error may halt execution and prevent `plot_run(True)` from returning data. It may be preferable to check `errors.code` after the function returns:

|`errors.code`|Meaning|
|---|---|
|`0`|No error|
|`101`|Failed to connect|
|`102`|Stopped by pause button|
|`103`|Stopped by keyboard interrupt|
|`104`|Lost USB connectivity|
|`105`|Lost power|
|`106`|Homing failed|

### Keyboard interrupts

A more graceful interrupt can be enabled by setting `keyboard_pause = True` before `plot_run()` or `connect()`. A `Control+C` will then stop a plot similarly to pressing the pause button, potentially allowing the plot to be resumed later.

This approach is also useful for multi-threaded scripts where you can simulate a keyboard interrupt to programmatically initiate a pause.

## Functions: General

### load_config

_Load settings from NextDraw configuration file_

**Syntax:** `load_config(file_name_or_path)`

Reads an NextDraw configuration file and applies the settings. The argument is required and can be a file name or path.

Use `plot_setup()` or `interactive()` before calling `load_config()`.

This function can be used in both the **Plot** and **Interactive** contexts.

## Functions: Plot

|Function|Description|
|---|---|
|`plot_setup()`|Parse SVG file and initialize Plot context|
|`plot_run()`|Perform the specified Plot context action|

### plot_setup

_Initialize Plot context and Parse SVG input_

**Syntax:** `plot_setup(svg_input=None)`

Parses the input SVG and initializes configuration variables. The SVG argument is optional and may be a file name/path or a string containing SVG content.

If called without an argument (`plot_setup()` or `plot_setup(None)`), the **Plot** context is initialized without an SVG file. This is useful for modes that do not plot (e.g., `cycle`, `align`, `utility`, `sysinfo`, `version`).

### plot_run

_Perform the configured Plot context action_

**Syntax:** `plot_run(output=False)`

Performs the action set by configuration variables. Call `plot_run(True)` to generate SVG output:

```python
output_svg = nd1.plot_run(True)
```

The output is normally a string containing a serialized SVG file. If the [`digest`](#digest) option is enabled, the output will be in the restricted Plob format.

## Functions: Interactive

|Function|Description|
|---|---|
|`interactive()`|Initialize Interactive context|
|`connect()`|Open serial connection to NextDraw|
|`disconnect()`|Close serial connection to NextDraw|
|`update()`|Apply changes to options|
|`goto(x, y)`|Absolute move to (x,y) location|
|`moveto(x, y)`|Absolute pen-up move to (x,y)|
|`lineto(x, y)`|Absolute pen-down move to (x,y)|
|`go(dx, dy)`|Relative move by (dx,dy)|
|`move(dx, dy)`|Relative pen-up move by (dx,dy)|
|`line(dx, dy)`|Relative pen-down move by (dx,dy)|
|`penup()`|Raise the pen|
|`pendown()`|Lower the pen|
|`draw_path(vertex_list)`|Draw a path from a coordinate list|
|`delay(time_ms)`|Execute a hardware-timed delay|
|`block()`|Wait for all motion commands to complete|
|`current_pos()`|Query machine XY position|
|`turtle_pos()`|Query turtle XY position|
|`current_pen()`|Query physical pen state (up = `True`)|
|`turtle_pen()`|Query turtle pen state (up = `True`)|
|`usb_command(cmd)`|Low-level serial command|
|`usb_query(query)`|Low-level serial query|

### interactive

_Initialize Interactive context_

**Syntax:** `interactive()`

Must be called before setting any configuration options in the **Interactive** context.

### connect

_Open serial connection to NextDraw_

**Syntax:** `connect()`

Opens a USB serial connection, applies option values, raises the pen, enables XY stepper motors, performs automatic homing (if supported and enabled), and sets the current position to (0,0). Returns `True` on success, `False` on failure.

Port-related options (`port`, `port_config`) must be specified before calling `connect()`.

### disconnect

_Close serial connection to NextDraw_

**Syntax:** `disconnect()`

Closes the serial connection and sets `connected` to `False`.

### update

_Apply changes to options_

**Syntax:** `update()`

If you change options after calling `connect()`, use `update()` to process and apply those changes before calling additional motion commands. Port options cannot be adjusted once the port is open.

### goto

_Absolute move to (x,y) location_

**Syntax:** `goto(final_x, final_y)`

Moves the carriage to the specified position without changing pen state. Use with `penup()` and `pendown()`.

### moveto

_Absolute pen-up move to (x,y)_

**Syntax:** `moveto(final_x, final_y)`

Raises the pen (if not already raised) and performs an absolute move to the given position.

### lineto

_Absolute pen-down move to (x,y)_

**Syntax:** `lineto(final_x, final_y)`

Lowers the pen (if not already lowered) and performs an absolute move to the given position.

### go

_Relative move by (dx,dy)_

**Syntax:** `go(delta_x, delta_y)`

Moves the carriage by the specified distances relative to the current position without changing pen state.

### move

_Relative pen-up move by (dx,dy)_

**Syntax:** `move(delta_x, delta_y)`

Raises the pen and performs a relative move by the given distances.

### line

_Relative pen-down move by (dx,dy)_

**Syntax:** `line(delta_x, delta_y)`

Lowers the pen and performs a relative move by the given distances.

### penup

_Raise the pen_

**Syntax:** `penup()`

Only raises the pen if it was in the down or indeterminate state.

### pendown

_Lower the pen_

**Syntax:** `pendown()`

Only lowers the pen if it was in the up or indeterminate state. If the turtle position is outside travel limits, the physical pen will not be lowered until the turtle moves back within bounds.

### draw_path

_Draw a path from a list of vertices_

**Syntax:** `draw_path(vertex_list)`

Plots a continuous pen-down shape from a list of coordinate pairs. The argument is a Python list of `[x, y]` pairs (at least two). The function raises the pen, moves to the start, lowers the pen, traces the path, and raises the pen at the end.

Paths that exceed travel bounds are clipped automatically.

### delay

_Execute a hardware-timed delay_

**Syntax:** `delay(time_ms)`

Queues a zero-distance movement lasting `time_ms` milliseconds. Unlike Python's `sleep`, this is executed by the EBB control board in sequence with other motion commands.

### block

_Wait for all motion commands to complete_

**Syntax:** `block()`

Polls the NextDraw until all queued motion commands are completed. Useful when sequencing external equipment or using low-level USB commands.

### current_pos

_Query the last-known machine position_

**Syntax:** `current_pos()`

Returns a 2-element tuple `(x, y)` giving the last-known physical machine position in the currently active units. This may differ from `turtle_pos()` if motion has been clipped at travel limits.

### turtle_pos

_Query the last-known turtle XY position_

**Syntax:** `turtle_pos()`

Returns a 2-element tuple `(x, y)` giving the theoretical "turtle" position. The turtle is not constrained by hardware travel limits and represents the requested position.

### current_pen, turtle_pen

_Query pen state_

**Syntax:** `current_pen()` / `turtle_pen()`

Returns `True` if the pen is up, `False` if down. `current_pen()` reports the physical pen state; `turtle_pen()` reports the theoretical state. These may differ when the turtle is outside travel bounds.

### usb_command, usb_query

_Low-level serial command/query_

**Syntax:** `usb_command(command)` / `usb_query(query)`

Issue direct commands or queries to the EBB driver board over USB. These bypass all syntax, context, speed, position, and limit checks. The command/query string should follow the [EBB serial command set](http://evil-mad.github.io/EggBot/ebb.html) using "future syntax mode". Results from `usb_query` are stripped of whitespace.

Advanced feature; use with great care.

## Migrating from AxiDraw API

If you are updating from the AxiDraw CLI or Python API, please see the documentation on [migrating from AxiDraw APIs](https://bantam.tools/nd_migrate).

## API Changelog

### v 1.5 (2025-07)

Bug fix and compatibility update. [Archived release](https://software-download.bantamtools.com/nd/api/nd_api_150.zip).

### v 1.4 (2025-03)

- Change to homing behavior: Walk Carriage commands now trigger automatic homing if the carriage has not already been homed.
- Updates to manual homing and XY offset behavior.
- New `set_home` utility command.
- Removed Python 3.8 support, added Python 3.13 support (3.9 - 3.13 supported).

[Archived release](https://software-download.bantamtools.com/nd/api/nd_api_146.zip).

### v 1.3 (2024-07)

NextDraw Layer Control now supports different optimization levels by layer. [Archived release 1.3.0](https://software-download.bantamtools.com/nd/api/nd_api_130.zip). Bug fix update 1.3.2 (October 2024) [here](https://software-download.bantamtools.com/nd/api/nd_api_132.zip).

### v 1.1 (2024-06)

Initial public release. Python versions 3.8 - 3.12 supported. [Archived release](https://software-download.bantamtools.com/nd/api/nd_api_110.zip).

## Copyright

Documentation Copyright 2025 Windell H. Oskay, Bantam Tools. All rights reserved.