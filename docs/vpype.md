# *vpype*

## What is *vpype*?

In a nutshell, *vpype* is an extensible CLI pipeline utility which aims to be the Swiss Army knife for creating, modifying and/or optimizing plotter-ready vector graphics. Let's break this down:

- CLI: *vpype* is a command-line utility, so it is operated from a terminal

- Pipeline: *vpype* operates by assembling 'commands' in sequences in which each command generates or process geometries before passing them on to the next command. Here is an example:

      $ vpype read input.svg scale 2 2 linesort write output.svg

  Here the geometries are loaded from a file (`read input.svg`), their size is doubled in both directions (`scale 2 2`), paths are reordered to minimize plotting time (`linesort`), and an SVG file is created with the result (`write output.svg`).

- Extensible: new commands can easily be added to *vpype* with plug-ins. This allows anyone to extend *vpype* with new commands or to write their own generative algorithm.

- Plotter vector graphics: *vpype* focuses on the niche of vector graphics for plotters (such as the [Axidraw](https://www.axidraw.com)) rather than being a general purpose vector processing utility.

- Swiss Army knife: *vpype* is flexible, contains many tools and its author is Swiss.

## Download and install

*vpype* can be installed from the [Python Package Index](https://pypi.org) using pipx:

``` bash
$ pipx install "vpype[all]"
```

Check the `installation instruction <install>` for step-by-step explanations.

## Using this documentation

If you are of the straight-to-action type, the list of available commands is available in the `reference <reference>` section. You may also jump to the `cookbook <cookbook>` section to find a recipe that matches your need.

For a deep understanding of *vpype*, take a dive in the section on `fundamentals <fundamentals>`.

Developers can learn more about extending *vpype* in the `Creating plug-ins <plugins>` section and the `API reference <api>`.

## Documentation


## Reference


## Miscellaneous Pages


---

# Installation

This page explain how to install *vpype* for end-users. If you intend to develop on *vpype*, refer to the the `contributing` section.

> **Note**
>
> The recommended Python version is 3.13. *vpype* is also compatible with Python 3.11 and 3.12.

> **Warning**
>
> *vpype* is not yet compatible with Python 3.13.

## macOS

### Installing Python

The official installer is the recommended way to install Python on your computer. It can be downloaded [here](https://www.python.org/downloads/).

> **Caution**
>
> When install Python, make sure to select version that is compatible with *vpype*. See the `top of this page <install>` for more information.

You can ensure that the installed Python interpreter is properly installed by running this command:

``` bash
python3 --version
```

It should produce an output similar to:

``` bash
Python 3.13.2
```

The version number should match the installer you used.

Note that installing Python from [Homebrew](https://brew.sh) or [MacPorts](https://www.macports.org) is possible as well.

### Installing pipx

[pipx](https://pypa.github.io/pipx) is a tool that allows you to install Python applications in isolated environments. It is the recommended way to install *vpype* on macOS. It can be installed with the following commands:

``` bash
python3 -m pip install pipx
python3 -m pipx ensurepath
```

After this, restart your terminal and ensure that pipx is properly installed by running this command:

``` bash
pipx --version
```

It should print out the current version of pipx without error:

``` bash
1.2.0
```

### Installing *vpype*

Once pipx is properly installed, you can install *vpype* with the following command:

``` bash
pipx install "vpype[all]"
```

*vpype* should now be installed and ready to use. You may check that it is fully functional by checking its version or displaying some random lines:

``` bash
vpype --version
vpype random show
```

## Windows

### Installing using pipx

First, install Python. The official Python distribution for Windows can be [downloaded here](https://www.python.org/downloads/) or installed from the [App Store](https://www.microsoft.com/en-us/p/python-310/9pjpw5ldxlz5). When installing Python, make sure you enable adding Python to the path.

> **Caution**
>
> When install Python, make sure to select version that is compatible with *vpype*. See the `top of this page <install>` for more information.

Then, install pipx:

``` bat
python -m pip install --user pipx
pipx ensurepath
```

In the first command, replace `python` by `python3` if you installed Python from the App Store. The second command above ensures that both pipx and the software it will install are available the terminal. You may need to close and re-open the terminal for this to take effect.

Finally, install *vpype*:

``` bat
pipx install "vpype[all]"
```

*vpype* should now be installed and ready to use. You may check that it is fully functional by checking its version and displaying some random lines:

``` bat
vpype --version
vpype random show
```

## Linux

First, install [pipx](https://pypa.github.io/pipx) with your system's package manager. On Debian/Ubuntu flavored installation, this is typically done as follows:

``` bash
sudo apt-get install pipx
```

Then run the following command to ensure your path variable is properly set:

``` bash
pipx ensurepath
```

You may need to close and re-open the terminal window for this to take effect.

Finally, install *vpype*:

``` bash
pipx install "vpype[all]"
```

*vpype* should now be installed and ready to use. You may check that it is fully functional by checking its version and displaying some random lines:

``` bash
vpype --version
vpype random show
```

## Raspberry Pi

Full installation including the viewer on the Raspberry Pi is no longer supported. Expert users may succeed with `pipx install "vpype[all]"`. Also, the new viewer requires OpenGL 3.3, which the Raspberry Pi does not support. The classic viewer should work correctly:

``` bash
vpype [...] show --classic
```

Installing the CLI-only version described in the next section is easier and should be favored whenever possible. Here are the recommended steps to do so.

Some packages and their dependencies are easier to install at the system level:

``` bash
sudo apt-get install python3-shapely python3-numpy python3-scipy
```

Then, install pipx:

``` bash
sudo apt-get install pipx
pipx ensurepath
```

Finally, install and run *vpype*:

``` bash
pipx install vpype
vpype --version
```

## CLI-only install

For special cases where the `cmd_show` is not needed and dependencies such as matplotlib, PySide6, or ModernGL are difficult to install, a CLI-only version of *vpype* can be installed using this command:

``` bash
pipx install vpype
```

Note the missing `[all]` compared the instructions above.


---

# Fundamentals

## Pipeline

To use *vpype*, you compose "pipelines" of "commands". In a given pipeline, geometries are passed from command to command, starting with the first all the way to the last.

![image](images/pipeline.svg)

Pipelines are created by passing *vpype* the first command name together with its options and arguments, then the next command name, and so on.:

``` bash
$ vpype command1 [--option X [...]] [ARG [...]] command2 [--option X [...]] [ARG [...]] ...
```

The list of every command is available by running the help option on the core vpype command:

``` bash
$ vpype --help
Usage: vpype [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  -v, --verbose
  -I, --include PATH  Load commands from a command file.
  -H, --history       Record this command in a `vpype_history.txt` in the
                      current directory.
  -s, --seed INTEGER  Specify the RNG seed.
  --help              Show this message and exit.
    ...
```

Help on each command is also available by running the help option on that command, for example:

``` bash
$ vpype circle --help
Usage: vpype circle [OPTIONS] X Y R

  Generate lines approximating a circle.

  The circle is centered on (X, Y) and has a radius of R.

Options:
  -q, --quantization LENGTH  Maximum length of segments approximating the
                             circle.
  -l, --layer LAYER          Target layer or 'new'.
  --help                     Show this message and exit.
```

## Lines and layers

<figure>
<img src="images/layers.svg" class="align-right" alt="images/layers.svg" />
</figure>

The geometries passed from command to command are organised as a collection of layers, each containing a collection of paths.

The primary purpose of layers in *vpype* is to create or process files for multicolored plots, where each layer contains geometries to be drawn with a specific pen or color. In *vpype*, layers are identified by a non-zero, positive integer (e.g. 1, 2,...). You can have as many layers as you want, memory permitting.

Each layer consists of an ordered collection of paths. In *vpype*, paths are so-called "polylines", meaning lines made of one or more straight segments. Each path is therefore described by a sequence of 2D points. Internally, these points are stored as complex numbers (this is invisible to the user but relevant to `plugin <plugins>` writers).

Curved paths are not supported *per se*. Instead, curves are converted into linear segments that are small enough to approximate curvature in a way that is invisible in the final plot. For example, the `cmd_read` command transforms all curved SVG elements (such as circles or bezier paths) into paths made of segments, using a maximum segment size that can be set by the user (so-called "quantization"). This design choice makes *vpype* very flexible and easy to develop, with no practical impact on final plot quality, but is the primary reason why *vpype* is not fit to be (and is not meant as) a general-purpose vector graphics processing tool.

> **Note**
>
> One downside of using polylines to approximate curved element is a potential increase in output file size. For example, three numbers are sufficient to describe a circle, but 10 to 100 segments may be needed to approximate it sufficiently well for plotting. When this becomes an issue, tuning the quantization parameters with the `-q` option or using the `cmd_linesimplify` command can help.

## Command taxonomy

Commands come in four different types: *generators*, *layer processors*, *global processors*, and *block processors*. The first three are covered in this section. The block processors are different in the sense they act on the flow of execution of the pipeline. They are covered in the `fundamentals_blocks` section below.

<img src="images/command_types.svg" width="600" alt="image" />

### Generators

Generators add new geometries to a target layer, preserving any content already existing in the layer. The content of the other layers is not affected. They accept a `--layer TARGET` option to control which layer should receive the new geometries. By default, the target layer of the previous generator command is used, or layer 1 for the first generator of the pipeline. Here's an example:

``` bash
$ vpype line --layer 3 0 0 1cm 1cm circle 0.5cm 0.5cm 0.3cm
```

This pipeline will first draw a `cmd_line` on layer 3 from the point (0,0) to the point at (1cm, 1cm), then it will draw a `cmd_circle` also on layer 3 centred on the point (0.5cm, 0.5cm), with a radius of 0.3cm.

For generators, `--layer new` can be used to generate geometries in a new, empty layer with the lowest possible number identifier.

The following commands are further examples of generators:

- `cmd_rect`: generates a rectangle, with optional rounded angles
- `cmd_ellipse`: generates lines approximating an ellipse
- `cmd_arc`: generates lines approximating a circular arc
- `cmd_frame`: generates a single-line frame around the existing geometries

### Layer processors

Layer processor operate on a layer-by-layer basis, modifying, complementing, or otherwise processing their content. The way a layer processor changes one layer's content has no bearing on how it will affect another layer. For example, the `cmd_linemerge` command looks for paths whose ends are close to one another (according to some tolerance) and merges them to avoid unnecessary pen-up/pen-down operations by the plotter. It does this within strictly within each layer and will not merge paths from different layers.

Like generators, layer processors accept a `--layer` option, but, in this case, multiple layers may be specified. Also, if the `--layer` option is omitted, they default to processing all existing layers. Here are some examples:

``` bash
$ vpype [...] crop --layer 1 0 0 10cm 10cm      # crop layer 1 only
$ vpype [...] crop --layer 1,2,4 0 0 10cm 10cm  # crop layers 1, 2 and 4
$ vpype [...] crop --layer all 0 0 10cm 10cm    # crop all layers
$ vpype [...] crop 0 0 10cm 10cm                # crop all layers
```

All these commands crop the specified layers to a 10cm x 10cm rectangle with a top-left corner at (0,0). Note that if you provide a list of layers, they must be comma separated without any whitespace.

Here are a few more examples of layer processors:

- `cmd_translate`: apply a translation to the geometries (i.e. move them)
- `cmd_linesort`: sort paths within the layer in such a way that the distance travelled by the plotter in pen-up position is minimized
- `cmd_linesimplify`: reduce the number of points in paths while ensuring a specified precision, in order to minimize output file size

### Global processors

Unlike layer processors, which are executed once for each target layer, global processors are executed once only, and apply to all layers.

For examples, the `cmd_write` command uses all layers in the pipeline to generate a multi-layer SVG file. Likewise, the `cmd_layout` command considers all layers when laying out geometries on a given page format. Finally, the layer operations commands, such as `cmd_lmove` or `cmd_lcopy`, have effects on multiple layers at once.

## Units

Like the SVG format, the default unit used by *vpype* is the CSS pixel, which is defined as 1/96th of an inch. For example, the following command will generate a 1-inch-radius circle centered on coordinates (0, 0):

``` bash
$ vpype circle 0 0 96
```

Because the pixel is not the best unit to use with physical media, most commands understand other CSS units (). The 1-inch-radius circle can therefore also be generated like this:

``` bash
$ vpype circle 0 0 1in
```

Note that there must be no whitespace between the number and the unit, otherwise they would be considered as different command-line arguments.

Internally, units other than CSS pixels are converted as soon as possible and pixels are used everywhere in the code (see `LengthType`).

Likewise, angles are interpreted as degrees by default but alternative units may be specified, including `deg`, `rad`, `grad` and `turn`. The following examples all rotate a rectangle by 45 degrees:

``` bash
$ vpype rect 0 0 50 100 rotate 45
$ vpype rect 0 0 50 100 rotate 50grad
$ vpype rect 0 0 50 100 rotate 0.125turn
$ vpype rect 0 0 50 100 rotate 0.785398rad
```

## Properties

In addition to geometries, the *vpype* pipeline carries metadata, i.e. data that provides information about geometries. This metadata takes the form of *properties* that are either global to the pipeline, or attached to a given layer. Properties are identified by a name, their value can be of arbitrary type (e.g. integer, floating point, color, etc.) and there can be any number of them.

How properties are created, modified, or deleted is up to the commands used in the pipeline. For example, the `cmd_read` command creates properties based on the input SVG's contents and the `cmd_write` command considers some properties when writing the output file.

### System properties

Although there is in general no constraint on the number, name, and type of properties, some do have a special meaning for *vpype*. They are referred to as *system properties* and their name is prefixed with `vp_`. Currently, the following system properties are defined:

> - `vp_color` (`vpype.Color`): the color of a layer (layer property)
> - `vp_pen_width` (`float`): the pen width of a layer (layer property)
> - `vp_name` (`str`): the name of a layer (layer property)
> - `vp_page_size` (two-`tuple` of `float`): the page size (global property)
> - `vp_source` (`pathlib.Path`): the input file from which the geometries are created (global and/or layer property)
> - `vp_sources` (`set` of `pathlib.Path`): list of all input files from which geometries are created (global property)

Many commands act on these properties. For example, the `cmd_read` command sets these properties according to the imported SVG file's content. The `cmd_color`, `cmd_alpha`, `cmd_penwidth`, `cmd_name`, and `cmd_pens` commands can set these properties to arbitrary values. In particular, the `cmd_pens` commands can apply a predefined set of values on multiple layers at once, for example to apply a CMYK color scheme (see `faq_custom_pen_config` for more information). The page size global property is set by the `cmd_pagesize` and `cmd_layout` commands, and used by the `cmd_write` command.

> **Note**
>
> The `vp_source` and `vp_sources` properties are somewhat different from the other properties. They exist as a standard way for file-based commands and plug-ins to record the source file(s) from which geometries originate.

The `vp_source` property contains the last input file used, and may be overwritten if subsequent file-based commands are used. For example, the `cmd_read` command stores the input SVG path in `vp_source` as layer property if the `--layer` option is used, or as global property otherwise. If multiple `cmd_read` commands are used, the last one may overwrite the value from the earlier ones.

To address this limitation, the `cmd_read` command also *appends* the input SVG path to the `vp_sources` global property. The `vp_sources` property therefore is a set of *all* source files involved. Third-party developers are strongly encouraged to implement a similar behavior in their file-based plug-ins.

### SVG attributes properties

In addition to setting system properties, the `cmd_read` command identifies SVG attributes common to all geometries in a given layer and store their value as layer property with a `svg_` prefix. For example, if all geometries in a given layer share a `stroke-dasharray="3 1"` SVG attribute (either because it is set at the level of the group element, or because it is set in every single geometry elements), a property named `svg_stroke-dasharray` with a value of `"3 1"` is added to the layer.

These properties are set for informational and extension purposes, and are mostly ignored by built-in commands. The notable exception is the `cmd_write` command, which can optionally restore these attributes in the exported SVG file.

An example of future extension could be a plug-in which detects the `svg_stroke-dasharray` property and turns the corresponding layer's lines into their dashed equivalent. Another example would be a plug-in looking for a `svg_fill` property and adding the corresponding hatching patterns to reproduce the filled area.

### Interacting with properties

High-level commands such as `cmd_penwidth` are not the only means of interacting with properties. *vpype* includes a set of low-level commands to inspect and modify global and layer properties:

> - `cmd_propget`: reads the value of a single global or layer property
> - `cmd_proplist`: lists all the global or layer properties
> - `cmd_propset`: sets the value of a given global or layer property
> - `cmd_propdel`: deletes a given global or layer property
> - `cmd_propclear`: deletes all global or layer properties

### Property substitution

Most arguments and options passed to commands via the *vpype* CLI apply property substitution on the user input. For example, this command will draw the name of the layer:

``` bash
$ vpype [...] text --layer 1 "{vp_name} layer" [...]
```

The curly braces mark a property substitution pattern which should be substituted by the content of the property they refer to. In this case, if layer 1 is named "red", the text "red layer" is drawn by the `cmd_text` command. Note the use of double quotes. They are needed because curly braces are typically used by shell interpreters such as `bash` or `zsh`. In this case, they are also needed to escape the whitespace between `{vp_name}` and `layer`.

To avoid substitution, curly braces can be escaped by doubling them:

``` bash
$ vpype [...] text --layer 1 "{{hello}}" [...]   # the text '{hello}' will be drawn
```

Numeric arguments and options also support substitutions (though they may result in an error if the substituted text is not a number). For example, the following command fills the entire page with random lines:

``` bash
$ vpype pagesize a4 random -n 200 -a "{vp_page_size[0]}" "{vp_page_size[1]}" show
```

Internally, the substitution is performed using the `str.format` Python function, which supports a number of customisation options for numerical values. Here are some examples to illustrate the possibilities:

``` none
{vp_pen_width}          -> 2.5
{vp_pen_width:.3f}      -> 2.500
{vp_pen_width:06.2f}    -> 002.50
{vp_page_size}          -> (793.7007874015749, 1122.5196850393702)
{vp_page_size[0]:.2f}   -> 793.70
{vp_color}              -> #ff0000
{vp_color.red}          -> 255
{vp_color.red:#02x}     -> 0xff
```

See the [Python documentation](https://docs.python.org/3/library/string.html#format-string-syntax) for a complete description of the formatting mini-language.

## Expression substitution

### Overview

Most arguments and options passed via the CLI may contain so-called "expressions", which are Python-like bits of code which *vpype* evaluates and replaces by what they evaluate to. Expressions are marked by enclosing percent characters (`%`).

Let us consider the following simple example:

``` bash
$ vpype text %3+4% show
```

The argument passed to the `cmd_text` command, namely `%3+4%`, is enclosed with percent character and thus evaluated as an expression. The expression, namely `3+4`, evaluates to 7, and thus the number 7 is drawn and displayed by the `cmd_show` command.

Expressions do not need to span the entirety of an argument. They can be mixed with regular text, and multiple expressions may be used in a single argument:

``` bash
$ vpype read input.svg layout %3+4%x%7+2%cm write output.svg
```

There are two distinct expressions here (`%3+4%` and `%7+2%`). Considering the text around them, they collectively evaluate to `7x9cm`, which happens to be a valid input for the `cmd_layout` command.

Most shells (e.g. `bash`, `zsh`, etc.) will interpret characters found in all but the simplest expressions. For example, the multiplication operator `*` is interpreted as a wildcard by the shell. Parentheses, brackets, and curly braces all have meanings to the shell too. As a result, arguments and options containing expression must often be escaped with quotes, for example:

``` bash
$ vpype text "%round(4**3.2)%" show
```

(Here, the function `round()` converts its argument to the nearest integer, and `**` is the exponentiation operator. This expression thus evaluates to 84.)

The `cmd_eval` command is often useful when using expressions. It does nothing but evaluate the expression it is passed. For example, this pipeline draws and displays the text "hello world":

``` bash
$ vpype eval "%txt='hello world'%" text %txt% show
```

Since `cmd_eval` has no other purpose than evaluating an expression, the expression markers `%` may be omitted. This is a valid variant of the same pipeline:

``` bash
$ vpype eval "txt='hello world'" text %txt% show
```

Finally, the expression marker `%` may be escaped by doubling it. The following example draws and displays a single percent character:

``` bash
$ vpype text %% show
```

### Basic syntax

The syntax of expressions is a sub-set of Python, and is interpreted by the [asteval](https://github.com/newville/asteval) library. Its [documentation](https://newville.github.io/asteval/) states:

> While the primary goal is evaluation of mathematical expressions, many features and constructs of the Python language are supported by default. These features include array slicing and subscripting, if-then-else conditionals, while loops, for loops, try-except blocks, list comprehension, and user-defined functions. All objects in the asteval interpreter are truly Python objects, and all of the basic built-in data structures (strings, dictionaries, tuple, lists, sets, numpy arrays) are supported, including the built-in methods for these objects.

There is no shortage of online material covering the basics of Python syntax, which we will not repeat here. The context in which expressions are used in *vpype* is however unusual. This leads to some peculiarities which are discussed in the next few sections.

### Scope and variables

Multiple expressions may be scattered across several commands in a single *vpype* pipeline. They are all evaluated in the same scope. This means that a variable created in one expression is available to subsequent expressions. This is often used in combination with the `cmd_eval` command to set or compute values which are used multiple times in the pipeline. For example:

``` bash
$ vpype \
    read input.svg \
    eval "m=2*cm; w,h=prop.vp_page_size; w-=2*m;h-=2*m" \
    crop "%m%" "%m%" "%w%" "%h%" \
    rect "%m%" "%m%" "%w%" "%h%" \
    write output.svg
```

Here, the expression used with the `cmd_eval` command creates a variable `m` to store the margin size, unpacks the page size property (`vp_page_size`) into two variables (`w` and `h`), amd corrects them for the margin. These variables are then used multiple times to crop the geometries and draw a rectangular frame with the given margin. Note that `cm` and `prop` are built-in symbols, as explained in the next section.

### Built-in symbols

This section lists and describes the symbols (functions and variables) which are built-in to *vpype* expressions.

The following standard Python symbols available:

- Most the Python [built-in](https://docs.python.org/3/library/functions.html) classes and functions:

  `abs`, `all`, `any`, `bin`, `bool`, `bytearray`, `bytes`, `chr`, `complex`, `dict`, `dir`, `divmod`, `enumerate`, `filter`, `float`, `format`, `frozenset`, `hash`, `hex`, `id`, `input`, `int`, `isinstance`, `len`, `list`, `map`, `max`, `min`, `oct`, `ord`, `pow`, `range`, `repr`, `reversed`, `round`, `set`, `slice`, `sorted`, `str`, `sum`, `tuple`, `type`, `zip`

- Functions and constants from the `math` module:

  `acos() <math.acos>`, `acosh() <math.acosh>`, `asin() <math.asin>`, `asinh() <math.asinh>`, `atan() <math.atan>`, `atan2() <math.atan2>`, `atanh() <math.atanh>`, `ceil() <math.ceil>`, `copysign() <math.copysign>`, `cos() <math.cos>`, `cosh() <math.cosh>`, `degrees() <math.degrees>`, `e() <math.e>`, `exp() <math.exp>`, `fabs() <math.fabs>`, `factorial() <math.factorial>`, `floor() <math.floor>`, `fmod() <math.fmod>`, `frexp() <math.frexp>`, `fsum() <math.fsum>`, `hypot() <math.hypot>`, `isinf() <math.isinf>`, `isnan() <math.isnan>`, `ldexp() <math.ldexp>`, `log() <math.log>`, `log10() <math.log10>`, `log1p() <math.log1p>`, `modf() <math.modf>`, `pi() <math.pi>`, `pow() <math.pow>`, `radians() <math.radians>`, `sin() <math.sin>`, `sinh() <math.sinh>`, `sqrt() <math.sqrt>`, `tan() <math.tan>`, `tanh() <math.tanh>`, `trunc() <math.trunc>`

- Some of the function from the `os.path` module:

  `abspath() <os.path.abspath>`, `basename() <os.path.basename>`, `dirname() <os.path.dirname>`, `exists() <os.path.exists>`, `expanduser() <os.path.expanduser>`, `isfile() <os.path.isfile>`, `isdir() <os.path.isdir>`, `splitext() <os.path.splitext>`

- The `stdin <sys.stdin>` stream from the `sys` module.

In addition, the following *vpype*-specific symbols are available:

- The `prop`, `lprop`, and `gprop` property-access objects.

  These special objects provide access to the global or current-layer properties. Properties may be accessed by attribute (e.g. `%prop.vp_name%`) or indexation (e.g. `%prop['vp_name']%`). The `gprop` object provides access to global properties. The `lprop` object provides access to the current layer's properties if available (i.e. within `generator <fundamentals_generators>` and `layer processor <fundamentals_layer_processors>` commands). The `prop` object looks first for current-layer properties, if any, and then for global properties.

- The `lid` variable (in supported commands).

  This variable contains the layer ID of the currently processed layer. It is available only for `generator <fundamentals_generators>` and `layer processor <fundamentals_layer_processors>` commands.

  > **Caution**
>
> This variable should not be confused with the `_lid` variable set by the `cmd_forlayer` block processor.

- Units constants ().

  These variables may be used to convert values to CSS pixels unit, which *vpype* uses internally. For example, the expression `%(3+4)*cm%` evaluates to the pixel equivalent of 7 centimeters (e.g. ~264.6 pixels). (Note that expressions may overwrite these variables, e.g. to use the `m` variable for another purpose.)

  > **Note**
>
>   Since `in` is a reserved keyword in Python, `inch` must be used instead to convert a length into inches.

- The `glob(pattern)` function.

  This function creates a list of paths (of type [pathlib.Path](https://docs.python.org/3/library/pathlib.html#module-pathlib)) by expending the provided pattern. In addition to the usual wildcards (`*` and `**`), this function also expends the home directory (`~`) and environment variables (`$var` or `${var}`), similarly to what shells typically do. See `fundamentals_using_paths` for more info on using paths in expressions.

- The `convert_length() <vpype.convert_length>`, `convert_angle() <vpype.convert_angle>`, and `convert_page_size() <vpype.convert_page_size>` functions.

  These functions convert string representations of lengths, angles, respectively page sizes to numerical values. For example, `%convert_length('4in')%` evaluates to the pixel equivalent of 4 inches, and `%convert_page_size('a4')%` evaluates to the tuple `(793.70..., 1122.52...)`, which corresponds to the A4 format in pixels.

- The `Color <vpype.Color>` class.

  This class can be used to create color structure from various input such as CSS-compatible strings or individual component (e.g. `Color("red")`, `Color("#ff0000)`, and `Color(255, 0, 0)` are equivalent). A `Color <vpype.Color>` instance evaluates to a string that is compatible with the `cmd_color` command.

In addition to the above, block processors define additional variables for expressions used in nested commands. These variables are prefixed by a underscore character `_` to distinguish them from symbols that are always available. See `fundamentals_block_processor_commands` for a list.

### Using paths

Some properties (such a `vp_source`, see `fundamentals_system_properties`) and expression variables (such as `_path`, set by the `cmd_forfile` block processor) are instances of `pathlib.Path` from the Python standard library. When evaluated, these objects behave like a string containing the file path and can be directly used with, e.g., the `cmd_read` command. The following command borrowed from the `faq_files_to_layer` recipe illustrates this:

``` bash
$ vpype \
    forfile "*.svg" \
      read --layer %_i+1% %_path% \
    end \
    write output.svg
```

Here, the `_path` variable set by the `cmd_forfile` block processor is directly used as file path argument for the `cmd_read` command.

There is however much more that instances of `pathlib.Path` are capable of. The [Python documentation](https://docs.python.org/3/library/pathlib.html) covers this extensively, but here is a summary for convenience:

> - `path.name` is the full name of the file.
> - `path.stem` is the base name of the file, excluding any file extension.
> - `path.suffix` is the file extension of the file.
> - `path.parent` is another `pathlib.Path` instance corresponding to the directory containing the file.
> - `path.with_stem(s)` is another `pathlib.Path` instance with the stem (i.e. file name excluding extension) replaced by `s`.
> - Path objects can be composited with the `/` operator. For example, `path.parent / "dir" / "file.svg"` is a `pathlib.Path` instance pointing at a file named "file.svg" in a directory "dir" next to the original file.

The `faq_pipeline_in_shell_script` recipe provides a real-world example relying on `pathlib.Path` capabilities.

### Single-line hints

The Python syntax is known for its heavy reliance on line break and indentation (contrary to, e.g., C-derived languages). For *vpype* expressions, this is a disadvantage, as expressions must fit a single line. This section provides a few hints on how useful tasks may be achieved using single-line expressions.

#### Statement separator

A single line of Python may contain multiple statements if they are separated with a semicolon (`;`). For example, this can be used to declare multiple variables in a single `cmd_eval` command:

``` bash
$ vpype eval "a=3; b='hello'" [...]
```

The expression evaluates to the last statement. For example, this pipeline draws and displays the number 4:

``` bash
$ vpype eval "a=2" text "%a+=2;a%" show
```

#### Conditional expressions

In most cases, [conditional expressions](https://docs.python.org/3/reference/expressions.html#conditional-expressions) (also called "ternary operator") are a good replacement for conditional block:

``` bash
$ vpype eval %b=True% text "%'I win' if b else 'I lose'%" show
```

This technique is used by the `faq_merge_to_grid` recipe.

#### Single-line conditionals and loops

Although conditional and loop statements typically require line breaks and indentation, they *can*, in their simpler form, be used on a single line. For examples, these are syntactically valid and can be used as *vpype* expression:

> ``` python
> if cond: n += 1
> while cond: n += 1
> for i in range(4): n += i
> ```

It is important to note that, formally, these are Python *statement* (as opposed to *expression*). They thus evaluate to `None` regardless of the actual run-time branching behavior. For example, this draws and displays "None":

``` bash
$ vpype text "%if True: 'hello'%" show
```

These constructs are instead typically used to assign variables which are used in subsequent expressions.

Another limitation is that single-line conditionals and loops cannot be juxtaposed with other statements using the statement separator (see `fundamental_statement_separator`). In particular, `a=3; if True: b=4` is invalid and `if False: a=3; b=4` is valid but `b=4` is part of the `if`-clause and is thus never executed in this case.

Despite their limitations, these constructs can still be useful in real-world situations. For example, the `faq_merge_layers_by_name` recipe makes use of them.

## Blocks

### Overview

Blocks refer to a portion of the pipeline which starts with a `cmd_begin` (optional) command followed by a *block processor* command, and ends with an `cmd_end` command. The commands in between the block processor and the matching `cmd_end` are called *nested commands* or, collectively, the *nested pipeline*. The block processor command "executes" the nested pipeline one or more times and combines the results in one way or the other. How exactly depends on the exact block processor command.

Let us consider an example:

``` none
command              command
┌─────────┴────────┐┌──────────┴──────────┐

$ vpype  begin  grid -o 2cm 2cm 2 2  circle 1cm 1cm 8mm  line 1cm 2mm 1cm 18mm  end  show

└──┬──┘└─────────┬─────────┘└────────────────────┬────────────────────┘└─┬─┘
block         block                           nested                  block
start       processor                        pipeline                  end
```

Here, the block starts with the `cmd_begin` command and the `cmd_grid` block processor, and ends with the `cmd_end` command. The nested pipeline is made of the `cmd_circle` and `cmd_line` commands. (As of *vpype* 1.9, the `cmd_begin` command is optional since the use of a block processor command implies the beginning of a block. It is included here for clarity, but most examples in this documentation omit it.)

Here is how the pipeline above could be schematize and the output it produces:

<img src="images/grid_example_schema.svg" style="width:59.0%" alt="image" />

<img src="images/grid_example_result.png" style="width:40.0%" alt="image" />

<figure>
<img src="images/grid_example_zoom.svg" class="align-right" alt="images/grid_example_zoom.svg" />
</figure>

How does the `cmd_grid` command use the nested pipeline? How many times is it executed? The diagram on the right illustrates the answer. It executes the nested pipeline once for each "cell". In the example above, there are 4 cells because it is passed the arguments `2` and `2` for the number of columns and rows. The nested pipeline is thus executed 4 times. Each time, the nested pipeline is initialised empty of any geometries. Then, after it is executed, the resulting geometries are translated by an offset corresponding to the cell being rendered. Finally, the translated geometries are merged into the outer pipeline.

### Block processor commands

This section provides an overview of the available block processors. In particular, the variables created by block processors are listed. Using these variables, prefixed with the underscore character `_`, is needed by most real-world application of block processors.

Note that, as usual, a complete documentation on each block processors is available using the `--help` command-line option:

``` bash
$ vpype grid --help
Usage: vpype grid [OPTIONS] NX NY

  Creates a NX by NY grid of geometry

  The number of column and row must always be specified. By default, 10mm
  offsets are used in both directions. Use the `--offset` option to override
  these values.

  [...]
```

#### `grid <cmd_grid>`

As amply illustrated in the previous sections, the `cmd_grid` block processor is used to create grid layout. It defines the following variables:

- `_nx`: the total number of columns (NX)
- `_ny`: the total number of rows (NY)
- `_n`: the total number of cells (NX\*NY)
- `_x`: the current column (0 to NX-1)
- `_y`: the current row (0 to NY-1)
- `_i`: the current cell (0 to \_n-1)

The `faq_merge_to_grid` recipe provides a real-world example with the `cmd_grid` command.

#### `repeat <cmd_repeat>`

<figure>
<img src="images/repeat_example.png" class="align-right" alt="images/repeat_example.png" />
</figure>

The `cmd_repeat` block processor executes the nested pipeline N times, where N is passed as argument. The nested pipeline is initialised without any geometries and, like the `cmd_grid` command, its output is merged to the outer pipeline.

The following example creates four layers, each populated with random lines:

``` bash
$ vpype repeat 4 random -l new -a 10cm 10cm -n 30 \
    end pens cmyk show
```

The `cmd_repeat` command defines the following variables:

- `_n`: number of repetitions (N)
- `_i`: counter (0 to N-1)

#### `forlayer <cmd_forlayer>`

The `cmd_forlayer` block processor executes the nested pipeline once per pre-existing layer. The nested pipeline is initialised with empty geometry *except* for the layer being processed. After the pipeline is executed, the corresponding layer is replaced in the outer pipeline and the other ones, if any, merged.

It defines the following variables:

- `_lid` (`int`): the current layer ID
- `_name` (`str`): the name of the current layer
- `_color` (`vpype.Color`): the color of the current layer
- `_pen_width` (`float`): the pen width of the current layer
- `_prop`: the properties of the current layer (accessible by item and/or attribute)
- `_i` (`int`): counter (0 to \_n-1)
- `_n` (`int`): number of layers

> **Note**
>
> The `_prop` object set by `cmd_forlayer` should not be mistaken with the `lprop` built-in object (see `fundamentals_expr_builtins`). `_prop` provides access to the properties of the layer currently iterated on by `cmd_forlayer`. In contrast, `lprop` provides access to the properties of the layer targeted by the current (nested) command. Both layers do not need to be, and often are not, the same.

The `faq_export_by_layers` and `faq_merge_layers_by_name` recipes provide real-world examples of the `cmd_forlayer` command.

#### `forfile <cmd_forfile>`

The `cmd_forfile` block processor specializes with processing multiple input files. It takes a file path pattern as input (e.g. `*.svg`), expends it as a list of files, and executes the nested pipeline once per file in the list. The nested pipeline is initialized with empty geometries and, after it is executed, its content is merged into the outer pipeline.

It defines the following variables:

- `_path` (`pathlib.Path`): the file path (see `fundamentals_using_paths`)
- `_name` (`str`): the file name (e.g. `"input.svg"`)
- `_parent` (`pathlib.Path`): the parent directory (see `fundamentals_using_paths`)
- `_ext` (`str`): the file extension (e.g. `".svg"`)
- `_stem` (`str`): the file name without extension (e.g. `"input"`)
- `_n` (`int`): the total number of files
- `_i` (`int`): counter (0 to \_n-1)

The `faq_files_to_layer` and `faq_merge_layers_by_name` recipes provide real-world examples with the `cmd_forfile` command.

### Nested blocks

<figure>
<img src="images/random_grid.png" class="align-right" alt="images/random_grid.png" />
</figure>

Blocks can be nested to achieve more complex compositions. Here is an example:

``` bash
$ vpype \
    grid --offset 8cm 8cm 2 3 \
      grid --offset 2cm 2cm 3 3 \
        random --count 20 --area 1cm 1cm \
        frame \
      end \
      frame --offset 0.3cm \
    end \
    layout a4 \
    show
```

## Command files

Pipelines be quite complex, especially when using blocks, which can become cumbersome to include in the command-line. To address this, all or parts of a pipeline of commands can be stored in so-called "command files" which *vpype* can then refer to. A command file is a text file whose content is interpreted as if it was command-line arguments. Newlines and indentation are ignored and useful only for readability. Everything to the right of a `#` character is considered a comment and is ignored.

The nested block example from the previous section could be converted to a command file with the following content:

``` bash
# command_file.vpy - example command file
begin
  grid --offset 8cm 8cm 2 3
    begin
      grid --offset 2cm 2cm 3 3
      random --count 20 --area 1cm 1cm
      frame
    end
  frame --offset 0.3cm
end
show
```

The command file can then be loaded as an argument using the <span class="title-ref">-I</span> or <span class="title-ref">--include</span> option:

``` bash
$ vpype -I command_file.vpy
```

Regular arguments and command files can be mixed in any combination:

``` bash
$ vpype -I generate_lines.vpy write -p a4 -c output.svg
```

Finally, command files can also reference other command files:

``` bash
# Example command file
begin
  grid --offset 1cm 1cm 2 2
  -I sub_command.vpy
end
show
```


---


# Cookbook

## SVG reading and writing recipes

### Wrapping a *vpype* pipeline in a shell script

Optimizing a SVG file is quite possibly the most common use of *vpype*. It usually is done with a pipeline similar to this example:

``` bash
$ vpype read my_file.svg linemerge linesort reloop linesimplify write my_file_optimized.svg
```

In particular, it is rather common to name the output file after the input file, maybe with a `_processed` suffix.

Such a *vpype* invocation can easily be packaged in a shell script using some simple path expression. Here is the content of such a shell script:

``` bash
#!/bin/sh

vpype read "$1" linemerge linesort reloop linesimplify \
   write "%prop.vp_source.with_stem(prop.vp_source.stem + '_processed')%"
```

(Shell scripts are typically named with a `.sh` extension and should be marked as "executable" to be used. This can be done with the `chmod +x my_script.sh` command.)

The script might be used as follows:

``` bash
$ ./my_script.sh /path/to/my_file.svg
```

The argument passed to the script is forwarded to *vpype* through the use of `$1`. Then, the output path provided to the `cmd_write` command corresponds to the input path, with a `_processed` suffix added (e.g. `/path/to/my_file_processed.svg` in this case). This is achieved by the `prop.vp_source.with_stem(prop.vp_source.stem + '_processed')` expression.

### Preserve color (or other attributes) when reading SVG

By default, the `cmd_read` command sorts geometries into layers based on the input SVG's top-level groups, akin to Inkscape's layers. Stroke color is preserved *only* if it is identical for every geometries within a layer.

When preserving the color is desirable, the `cmd_read` command can sort geometries by colors instead of by top-level groups. This is achieved by using the `--attr <read --attr>` option:

``` bash
$ vpype read --attr stroke input.svg [...]
```

Here, we tell the `cmd_read` command to sort geometry by `stroke`, which is the SVG attribute that defines the color of an element. As a result, a layer will be created for each different color encountered in the input SVG file.

The same applies for any SVG attributes, even those not explicitly supported by *vpype*. For example, `--attr stroke-width` will sort layers by stroke width and `--attr stroke-dasharray` by type of stroke dash pattern.

Multiple attributes can even be provided:

``` bash
$ vpype read --attr stroke --attr stroke-width input.svg [...]
```

In this case, a layer will be created for each unique combination of color and stroke width.

### Merge multiple SVGs into a multilayer file

This command will `cmd_read` two SVG files onto two different layers, then `cmd_write` them into a single SVG file:

``` bash
$ vpype \
    forfile "*.svg" \
      read --layer %_i+1% %_path% \
    end \
    write output.svg
```

### Load multiple files, merging their layers by name

Let us consider a collection of SVG files, each with one or more named layer(s). It could be for example a collection of CMYK SVGs, some of which with all four layers, but other with a sub-set of the layers (say, only "yellow" and "black"). This recipe shows how to load these files, making sure identically-named layers are properly merged.

Here is the full pipeline:

``` bash
$ vpype \
    eval "names={};n=100" \
    forfile "*.svg" \
        read %_path% \
        forlayer \
            eval "%if _name not in names: names[_name] = n; n = n+1%" \
            lmove %_lid% "%names[_name]%" \
        end \
    end \
    write combined.svg
```

This pipeline makes use of two nested blocks and some clever expressions. Let us break down how it works.

The core idea is to build a dictionary `names` which maps "destination" layer IDs to layer name. Destination layer IDs is where geometries will be merged, and we choose a starting layer ID value `n` of 100 to avoid interfering with the input file layers. At the beginning, `names` is an empty dictionary (`{}`). Here is how it could look at the end of a typical run:

> ``` python
> names = {
>    'cyan': 100,
>    'magenta': 101,
>    'yellow': 102,
>    'black': 103
> }
> ```

The outer block, marked by the `forfile "*.svg"` command, iterates over SVG files in the current directory. Each file is first read using `read %_path%`. Then, we iterate over its layers using the `forlayer` block processor.

This is where it becomes interesting. For each layer, we first test whether its name exists in the `names` dictionary. If not, we create a new item in the dictionary with the layer name, and assign the value of `n`. This is the layer ID at which identically-named layers must lend. Since the layer ID `n` is now assigned, we increment its value for the next time an "unknown" layer name is encountered.

Now that we made sure we have a destination layer ID for the current layer's name, we can move it using the `lmove %_lid% "%names[_name]%"` command. Here, `_lid` is the current layer ID as set by `forlayer` and `names[_name]` the destination layer.

This recipe can be further augmented to arrange each file on a grid. This is covered in the `faq_merge_to_grid` recipe.

### Saving each layer as a separate file

Some plotter workflows require a different file for each layer, as opposed to a single, multi-layer SVG file. For example, this is often the case for gcode input using the [vpype-gcode](https://github.com/plottertools/vpype-gcode/) plug-in.

This can be achieved using the `cmd_forlayer` command:

``` bash
$ vpype read input.svg forlayer write "output_%_name or _lid%.svg" end
```

Here, we construct the output file name either based on the layer name if available (which `cmd_forlayer` stores in the `_name` variable), or on the layer ID (`_lid`) otherwise.

### Make a previsualisation SVG

The SVG output of `cmd_write` can be used to previsualize and inspect a plot. By default, paths are colored by layer. It can be useful to color each path differently to inspect the result of `cmd_linemerge`:

``` bash
$ vpype read input.svg linemerge write --color-mode path output.svg
```

Likewise, pen-up trajectories can be included in the SVG to inspect the result of `cmd_linesort`:

``` bash
$ vpype read input.svg linesort write --pen-up output.svg
```

Note that `write --pen-up` should only be used for previsualization purposes as the pen-up trajectories may end-up being plotted otherwise. The Axidraw software will ignore the layer in which the pen-up trajectories are written, so it is safe to keep them in this particular case.

## Layout recipes

### Basic layout examples

There are two ways to layout geometries on a page. The preferred way is to use commands such as `cmd_layout`, `cmd_scale`, `cmd_scaleto`, `cmd_translate`. In particular, `cmd_layout` handles most common cases by centering the geometries on page and optionally scaling them to fit specified margins. These commands act on the pipeline and their effect can be previewed using the `cmd_show` command. The following examples all use this approach.

Alternatively, the `cmd_write` commands offers option such as `--page-size <write --page-size>` and `--center <write --center>` which can also be used to layout geometries. It must be understood that these options *only* affect the output file and leave the pipeline untouched. Their effect cannot be previewed by the `cmd_show` command, even if it is placed after the `cmd_write` command.

This command will `cmd_read` a SVG file, and then `cmd_write` it to a new SVG file sized to A4 in landscape orientation, with the design centred on the page:

``` bash
$ vpype read input.svg layout --landscape a4 write output.svg
```

The `cmd_layout` command implicitly centers the geometries on the page. The `cmd_pagesize` command can be used to choose the page size without changing the geometries:

``` bash
$ vpype read input.svg pagesize --landscape a4 write output.svg
```

This command will `cmd_read` a SVG file and lay it out to 3cm margin with a top vertical alignment (a generally pleasing arrangement for square designs on the portrait-oriented page), and then `cmd_write` it to a new SVG:

``` bash
$ vpype read input.svg layout --fit-to-margins 3cm --valign top a4 write output.svg
```

This command will `cmd_read` a SVG file, `cmd_scale` it down to 80% of its original size, and then `cmd_write` it to a new A5-sized SVG, centred on the page:

``` bash
$ vpype read input.svg scale 0.8 0.8 layout a5 write output.svg
```

This command will `cmd_read` a SVG file, scale it down to a 5x5cm square (using the `cmd_scaleto` command), and then `cmd_write` it to a new A5-sized SVG, centred on the page:

``` bash
$ vpype read input.svg scaleto 5cm 5cm layout a5 write output.svg
```

This command will `cmd_read` a SVG file, `cmd_crop` it to a 10x10cm square positioned 57mm from the top and left corners of the design, and then `cmd_write` it to a new SVG whose page size will be identical to the input SVG:

``` bash
$ vpype read input.svg crop 57mm 57mm 10cm 10cm write output.svg
```

This command will `cmd_read` a SVG file, add a single-line `cmd_frame` around the design, 5cm beyond its bounding box, and then `cmd_write` it to a new SVG:

``` bash
$ vpype read input.svg frame --offset 5cm write output.svg
```

### Cropping and framing geometries

The following pipeline can be used to crop geometries and frame them with a given margin:

``` bash
$ vpype \
    read input.svg \
    eval "m=2*cm; w, h = prop.vp_page_size" \
    crop %m% %m% "%w-2*m%" "%h-2*m%" \
    rect %m% %m% "%w-2*m%" "%h-2*m%" \
    write output.svg
```

### Laying out multiple SVGs on a grid

The `cmd_grid` command can be used to layout multiple SVGs onto a regular grid. This recipe shows how.

The basic idea is covered by the following pipeline:

``` bash
$ vpype \
    eval "files=glob('*.svg')" \
    eval "cols=3; rows=ceil(len(files)/cols)" \
    grid -o 10cm 15cm "%cols%" "%rows%" \
        read --no-fail "%files[_i] if _i < len(files) else ''%" \
        layout -m 0.5cm 10x15cm \
    end \
    write combined.svg
```

Here are the key insights to understand how this pipeline works:

- An expression with the `glob()` function (see `fundamentals_expr_builtins`) is used to create a list of files to include on the grid.
- Another expression computes the number of rows needed to include all files, given a number of column (hard-coded to 3 in this case).
- The `cmd_grid` command uses expressions again as argument to use the previously computed column and row count.
- For the `cmd_read` command, multiple tricks are used. The variable `_i` is set by the `cmd_grid` command and corresponds to the cell counter. We use it to look up the file path to read from our file list. We must however handle the last row, which might be incomplete. This is done with a conditional expression (see `fundamentals_conditional_expr`) which returns an empty path `''` if the cell index is beyond the end of the file list. Normally, the `cmd_read` would fail when passed a non-existing path. This is avoided by using the `--no-fail` option.
- Finally, the `cmd_layout` command fits the SVGs in the cell with a margin.

One limitation of the pipeline above is that it will merge layers by their ID, disregarding properties such as layer name or color. In some cases, this may be an issue. Depending on the nature of the input SVGs, this can be addressed by reading each file in a different layer, like in `faq_files_to_layer`. This can be done by simply adding the `--layer %_i+1%` option to the `cmd_read` command.

When input SVGs have layer names, they can be used to merge similarly named layers together. This is done by the following pipeline:

``` bash
$ vpype \
   eval "files=glob('*.svg')" \
   eval "cols=3; rows=ceil(len(files)/cols)" \
   eval "names={};n=100" \
   grid -o 10cm 15cm "%cols%" "%rows%" \
       read --no-fail "%files[_i] if _i < len(files) else ''%" \
       layout -m 0.5cm 10x15cm \
       forlayer \
           eval "%if _name not in names: names[_name] = n; n = n+1%" \
           lmove %_lid% "%names[_name]%" \
       end \
   end \
   write combined.svg
```

See `faq_merge_layers_by_name` for an explanation on how this works.

Given the number of parameters involved, it may be useful to make these pipelines interactive (see `faq_interactive_pipelines`). Using a `command file <fundamentals_command_files>` is also a nice way to make easy to reuse. Here is an example of command file:

``` bash
# Content of file grid.vpy
# Ask user for some information, using sensible defaults.
eval "files=glob(input('Files [*.svg]? ') or '*.svg')"    # glob() creates a list of file based on a pattern
eval "cols=int(input('Number of columns [3]? ') or 3)"
eval "rows=ceil(len(files)/cols)"  # the number of rows depends on the number of files
eval "col_width=convert_length(input('Column width [10cm]? ') or '10cm')"  # convert_length() converts string like '3cm' to pixels
eval "row_height=convert_length(input('Row height [10cm]? ') or '10cm')"
eval "margin=convert_length(input('Margin [0.5cm]? ') or '0.5cm')"
eval "output_path=input('Output path [output.svg]? ') or 'output.svg'"

# Create a grid with provided parameters.
grid -o %col_width% %row_height% %cols% %rows%

    # Read the `_i`-th file. The last row may be incomplete so we use an empty path and `--no-fail`.
    read --no-fail "%files[_i] if _i < len(files) else ''%"

    # Layout the file in the cell.
    layout -m %margin% %col_width%x%row_height%
end

# wWrite the output file.
write "%output_path%"
```

It can be used as follows:

``` bash
$ vpype -I grid.vpy
Files [*.svg]?
Number of columns [3]? 4
Column width [10cm]?
Row height [10cm]? 15cm
Margin [0.5cm]?
Output path [output.svg]?
```

The various parameters are queried and if nothing is provided as input, sensible defaults are used.

## Processing recipes

### Optimizing a SVG for plotting

This command will `cmd_read` a SVG file, merge any lines whose endings are less than 0.5mm from each other with `cmd_linemerge`, and then `cmd_write` a new SVG file:

``` bash
$ vpype read input.svg linemerge --tolerance 0.5mm write output.svg
```

In some cases such as densely connected meshes (e.g. a grid where made of touching square paths), `cmd_linemerge` may not be able to fully optimize the plot by itself. Using `cmd_splitall` before `cmd_linemerge` breaks geometries into their constituent segments and enables `cmd_linemerge` to perform a more aggressive optimization, at the cost of an increased processing time:

``` bash
$ vpype read input.svg splitall linemerge --tolerance 0.5mm write output.svg
```

This command will `cmd_read` a SVG file, simplify its geometry by reducing the number of segments in a line until they're a maximum of 0.1mm from each other using `cmd_linesimplify`, and then `cmd_write` a new SVG file:

``` bash
$ vpype read input.svg linesimplify --tolerance 0.1mm write output.svg
```

This command will `cmd_read` a SVG file, randomise the seam location for paths whose beginning and end points are a maximum of 0.03mm from each other with `cmd_reloop`, and then `cmd_write` a new SVG file:

``` bash
$ vpype read input.svg reloop --tolerance 0.03mm write output.svg
```

This command will `cmd_read` a SVG file, extend each line with a mirrored copy of itself three times using `cmd_multipass`, and then `cmd_write` a new SVG file. This is useful for pens that need a few passes to get a good result:

``` bash
$ vpype read input.svg multipass --count 3 write output.svg
```

This command will `cmd_read` a SVG file, use `cmd_linesort` to sort the lines to minimise pen-up travel distance, and then `cmd_write` a new SVG file:

``` bash
$ vpype read input.svg linesort write output.svg
```

### Filtering out small lines

In some cases (for example when using Blender's freestyle renderer), SVG files can contain a lot of tiny lines which significantly increase the plotting time and may be detrimental to the final look. These small lines can easily be removed thanks to the `cmd_filter` command:

``` bash
$ vpype read input.svg filter --min-length 0.5mm write output.svg
```

### Splitting layers by drawing distance

Certain medium such as paintbrush or [Posca](https://www.posca.com) pens require manual intervention after a certain drawing distance. One way to achieve this is to ensure that the cumulative distance of the lines within each layer remains below that drawing distance. This can be achieved using the `cmd_splitdist` command:

``` bash
$ vpype read input.svg splitdist 50cm write output.svg
```

A finer-grained approach consists of splitting all lines into their constituent segments using the `cmd_splitall` command and subsequently using the `cmd_linemerge` to put everything back together:

``` bash
$ vpype read input.svg splitall splitdist 50cm linemerge write output.svg
```

### Inserting regular "dipping" patterns for plotting with paint

Plotting with paint is a tricky process where the brush must be regularly dipped in a paint bucket. This can be achieved by using the `cmd_splitdist` command:

``` bash
$ vpype \
    read input.svg \
    forlayer \
      lmove %_lid% 1 \
      splitdist 1m \
      forlayer \
        lmove %_lid% "%_lid*2%" \
        read -l "%_lid*2-1%" dip_%_name%.svg \
      end \
    lmove all %_lid% \
    name -l %_lid% %_name% \
    color -l %_lid% %_color% \
  end \
  write output.svg
```

For this to work, the layers in `input.svg` must be named after their respective color and, for each such color, a file named `dip_COLORNAME.svg` must exist. For example, if `input.svg` has two layers named "red" and "blue", then the `dip_red.svg` and `dip_blue.svg` files must exist.

The output file will have the same layers as the input file, but they will start with the corresponding dipping pattern, which will also be interspersed regularly based on the cumulative drawing distance provided to the `cmd_splitdist` command.

## HPGL export recipes

### Converting a SVG to HPGL

For vintage plotters, the `cmd_write` command is capable of generating HPGL code instead of SVG. HPGL output format is automatically selected if the output path file extension is `.hpgl`. Since HPGL coordinate systems vary widely from plotter to plotter and even for different physical paper format, the plotter model must be provided to the `cmd_write` command:

``` bash
$ vpype read input.svg write --device hp7475a output.hpgl
```

The plotter paper size will be inferred from the current page size (as set by the input SVG or using either the `cmd_pagesize` or `cmd_layout` commands). The plotter type/paper format combination must exist in the built-in or user-provided configuration file. See `faq_custom_hpgl_config` for information on how to create one. If a matching plotter paper size cannot be found, an error will be generated. In this case, the paper size must manually specified with the `--page-size <write --page-size>` option:

``` bash
$ vpype read input.svg write --device hp7475a --page-size a4 --landscape output.hpgl
```

Here the `--landscape <write --landscape>` is also used to indicate that landscape orientation is desired. As for SVG output, the `--center <write --center>` is often use to center the geometries in the middle of the page.

It is typically useful to optimize the input SVG during the conversion. The following example is typical of real-world use:

``` bash
$ vpype read input.svg linesimplify reloop linemerge linesort layout a4 write --device hp7475a output.hpgl
```

### Defining a default HPGL plotter device

If you are using the same type of plotter regularly, it may be cumbersome to systematically add the `--device
<write --device>` option to the `cmd_write` command. The default device can be set in a configuration file (see `faq_custom_config_file`) by adding the following section:

> ``` toml
> [command.write]
> default_hpgl_device = "hp7475a"
> ```

### Creating a custom configuration file for a HPGL plotter

The configuration for a number of HPGL plotter is bundled with *vpype* (run `vpype write --help` for a list). If your plotter is not included, it is possible to define your own plotter configuration in a custom configuration file (see `faq_custom_config_file`).

The configuration file must first include a plotter section with the following format:

> ``` toml
> [device.my_plotter]
> name = "My Plotter"                 # human-readable name for the plotter
> plotter_unit_length = "0.02488mm"   # numeric values in pixel or string with units
> pen_count = 6                       # number of pen supported by the plotter
>
> info = "Plot configuration..."      # (optional) human-readable information on how
>                                     # the plotter must be configured for this
>                                     # configuration to work as expected
> ```

In the configuration file, all numerical values are in CSS pixel unit (1/96th of an inch). Alternatively, strings containing the numerical value with a unit can be used and will be correctly interpreted.

Then, the configuration file must include one `paper` section for each paper format supported by the plotter:

> ``` toml
> [[device.my_plotter.paper]]
> name = "a"                          # name of the paper format
>
> paper_size = ["11in", "8.5in"]      # (optional) physical paper size / CAUTION: order must
>                                     # respect the native X/Y axis orientation of the plotter
>                                     # unless paper_orientation is specified
>                                     # Note: may be omitted if the plotter support arbitrary
>                                     # paper size
>
> paper_orientation = "portrait"      # (optional) "portrait" or "landscape"
>                                     # specify the orientation of the plotter  coordinate
>                                     # system on the page ("landscape" means the X axis is
>                                     # along the long edge)
>
> origin_location = [".5in", "8in"]   # physical location from the page's top-left corner of
>                                     # the (0, 0) plotter unit coordinates
>
> origin_location_reference = "topleft"
>                                     # (optional) reference used for origin_location
>                                     # "topleft" (default) or "botleft"
>
> x_range = [0, 16640]                # (optional) admissible range in plotter units along
>                                     # the X axis
> y_range = [0, 10365]                # (optional) admissible range in plotter units along
>                                     # the Y axis
> y_axis_up = true                    # set to true if the plotter's Y axis points up on
>                                     # the physical page
> rotate_180 = true                   # (optional) set to true to rotate the geometries by
>                                     # 180 degrees on the page
>
> aka_names = ["ansi_a", "letter"]    # (optional) name synonyms that will be recognised by
>                                     # the `--paper-format` option of the `write` command
>
> set_ps = 0                          # (optional) if present, a PS command with the
>                                     # corresponding value is generated
>
> final_pu_params = "0,0"             # (optional) if present, specifies parameter to pass
>                                     # to the final `PU;` command
>
> info = "Paper loading..."           # (optional) human-readable information on how the
>                                     # paper must be loaded for this configuration to work
>                                     # as expected
> ```

While most of the parameters above are self-explanatory or easy to understand from the comments, there are several aspects that require specific caution:

- `paper_size` *must* be defined in the order corresponding to the plotter's native X/Y axis orientation. In the example above, the long side is specified before the short side because the plotter's native coordinate system has its X axis oriented along the long side and the Y axis oriented along the short side of the page.
- `origin_location` defines the physical location of (0, 0) plotter unit coordinate on the page, with respect to the top-left corner of the page in the orientation implied by `paper_size`. In the example above, since the long edge is defined first, `origin_location` is defined based on the top-left corner in landscape orientation.
- `y_axis_up` defines the orientation of the plotter's native Y axis. Note that a value of `true` does **not** imply that `origin_location` is measured from the bottom-left corner, unless `origin_location_reference` is set to `"botleft"`.

### Using arbitrary paper size with HPGL output

Some plotters such as the Calcomp Designmate support arbitrary paper sizes. Exporting HPGL with arbitrary paper size requires a specific paper configuration. *vpype* ships with the `flex` and `flexl` configurations for the Designmate, which can serve as examples to create configurations for other plotters.

For arbitrary paper size, the paper configuration must omit the `paper_size` parameter and specify a value for `paper_orientation`. Here is the `flexl` configuration for the Designmate when paper is loaded in landscape orientation in the plotter:

> ``` toml
> [[device.designmate.paper]]
> name = "flexl"
> y_axis_up = true
> paper_orientation = "landscape"
> origin_location = ["15mm", "15mm"]
> origin_location_reference = "botleft"
> rotate_180 = true
> final_pu_params = "0,0"
> ```

Note the missing `paper_size`, as well as the values for `paper_orientation` and `origin_location_reference`.

When using arbitrary paper size, the paper size is assumed to be identical to the current page size as set by the `cmd_read`, `cmd_pagesize`, or `cmd_layout` commands. Here is a typical example of use:

``` bash
$ vpype read input.svg layout --fit-to-margins 3cm 30x50cm write -d designmate -p flexl output.hpgl
```

In this case, the page size is set by the `cmd_layout` command (30x50cm) and the `cmd_write` command is set to use the `flexl` paper configuration because the paper is loaded in landscape orientation in the plotter. If the input SVG is already sized and laid out according to the paper size, the `cmd_layout` command may be omitted.

## Customizing *vpype*

### Creating a custom configuration file

Some of *vpype*'s features (such as HPGL export) or plug-in (such as [vpype-gcode](https://github.com/plottertools/vpype-gcode)) can be customized using a configuration file using the [TOML](https://toml.io/en/) format. The documentation of the features or plug-in using such a configuration file explains what it should contain. This section focuses on how a custom config file is made available to *vpype*.

The most common way is to create a <span class="title-ref">.vpype.toml</span> file at the root of your user directory, e.g.:

- `C:\Users\username\.vpype.toml` on Windows
- `/Users/username/.vpype.toml` on Mac
- `/home/username/.vpype.toml` on Linux

If such a file exists, it will be automatically loaded by *vpype* whenever it is used.

> **Note**
>
> The `.` prefix in the file name will make the file **hidden** on most systems. This naming is typical for configuration files in the Unix world.

Alternatively, a configuration file may be provided upon invocation of *vpype* using the `--config` option (or `-c` for short), e.g.:

``` bash
(vpype_venv) $ vpype --config my_config_file.toml [...]
```

Note that *vpype* does not "remember" the provided configuration file. The `--config` option must thus be provided on each invocation.

> **Note**
>
> *vpype* is bundled with a [configuration file](https://github.com/abey79/vpype/blob/master/vpype/vpype_config.toml). It is strongly discouraged to edit this file as it will be overwritten each time *vpype* is installed or updated.

### Creating a custom pen configuration

Pen configurations associate names, colors, and/or pen widths to specific layers and are applied by the `cmd_pens` command. For example, the included `cmyk` pen configuration sets the name and color or layers 1 to 4 to cyan, magenta, yellow, resp. black, while leaving pen widths unchanged. New pen configurations can be defined in a custom config file (see `faq_custom_config_file`).

Pen configurations must conform to the following format to be valid:

> ``` toml
> [pen_config.my_pen_config]  # my_pen_config is this pen configuration's name
> layers = [
>     # for each layer, a layer_id must be provided, but name, color and
>     # pen_width are optional
>     { layer_id = 1, name = "black layer", color = "black", pen_width = "0.15mm" },
>
>     # any valid CSS color string and length unit may be used
>     { layer_id = 2, name = "red layer", color = "#e00", pen_width = "0.05in" },
>
>     # any attribute may be omitted, except layer_id
>     { layer_id = 4, color = "#00de00" },
>
>     # etc. (a pen configuration may have an arbitrary number of layers defined)
> ]
> ```

The above pen configuration can be used by referring to its name, in this case `my_pen_config`:

``` bash
$ vpype [...] pens my_pen_config [...]
```

## Miscellaneous recipes

### Batch renaming layers

The `cmd_name` command can be used to assign a new name to a given layer. It is typically used as follows:

``` bash
$ vpype [...] name --layer 3 "Layer 3" [...]
```

If the `--layer <name --layer>` option is omitted, the provided name is assigned to *all* layers. This behaviour can be useful when combined with the `lid` `expression built-in variable <fundamentals_expr_builtins>`:

``` bash
$ vpype random --layer 1 random --layer 3  name "Layer %lid%"  write output.svg
```

Here, two layers with IDs 1 and 3 are created with some random lines (e.g. to simulate loading a multi-layer file). Then, these layers are renamed with "Layer 1" and "Layer 3", respectively, and the result written to the `output.svg` file. The layer names can be verified by opening `output.svg` in Inkscape.

### Controlling the AxiDraw plotting process using layer names

See [this article](https://bylr.info/articles/2023/03/17/layer-names/).

### Create interactive scripts with `input()`

The Python `input` function is available in `expressions <fundamentals_expression_substitution>`. It can be used to interactively query the use for parameter values. For example, this pipeline asks the user for a margin value and uses it to layout a SVG:

``` bash
$ vpype \
    eval "margin = float(input('Margin in cm? '))" \
    read input.svg \
    layout --fit-to-margins %margin*cm% a4 \
    write output.svg
Margin in cm? 3
```

This pattern can be improved by providing a default value, allowing the user to simply type \<Enter\> to use it:

``` bash
$ vpype \
    eval "margin = float(input('Margin in cm [3cm]? ') or 3)" \
    ...
```

This works because of the particular way in which the `or` operator behaves. It evaluates to the first operand whose truthiness is `True`. When the user directly hits \<Enter\>, the first operand is an empty string, whose truthiness is `False`. The `or` expression thus evaluates to the second operand in this case.

See `faq_merge_to_grid` for a real-world example that makes use of this pattern.

### Batch processing multiple SVGs with `forfile`

The `cmd_forfile` block processor can be used to apply the same processing on multiple files using the following pattern:

``` bash
$ vpype forfile "*.svg" \
      read "%_path%" \
      linemerge linesort reloop linesimplify \
      write "%_path.parent / _path.stem%_processed.svg" \
    end
```

The basic idea is to enclose the desired pipeline, including the `cmd_read` and `cmd_write` commands, in a `cmd_forfile` block. The input path is the `_path` expression variable set by `cmd_forfile`. A suitable output path can be constructed by combining `_path.parent` (the directory the input file) and `_path.stem` (the input file name without extension) in an expression, and adding the `_processed.svg` suffix (see `fundamentals_using_paths`).

One of the drawbacks of this approach is that each file is processed sequentially without exploiting multiple CPU cores. For a large number of files, this may take some time. The next recipe introduces an alternative batch processing method which enables multi-core processing.

### Batch processing multiple SVGs with `parallel`

Computers offer endless avenues for automation, which depend on OS and the type of task at hand. Here is one way to easily process a large number of SVG with the same *vpype* pipeline. This approach relies on the [GNU Parallel](https://www.gnu.org/software/parallel/) software and is best suited to Unix/Linux/macOS computers. Thanks to `parallel`, this approach takes advantage of all available processing cores.

This is an example that illustrates the general idea:

``` bash
$ parallel --plus vpype read {} linemerge linesort write {/.svg/_processed.svg} ::: *.svg
```

Let's break down how this works:

> - `GNU parallel` will execute the command before the `:::` maker for each argument it finds after the marker. In this example, we used `*.svg` which expends to the list of SVG files in the current directory.
> - The marker `{}` is replaced by `GNU parallel` with the current item being processed (e.g. the current SVG file).
> - The marker `{/.svg/_processed.svg}` does the same but it replaces `.svg` by `_processed.svg`. This way, if one of the original SVG file is called `my_file.svg`, it will be saved as `my_file_processed.svg` once processed.
> - The `--plus` option to `GNU parallel` is required to enable the string replacement syntax.

The results can easily be customised by changing one or more of these elements. When designing your own command, it is best to start with the `--dry-run` option so that `GNU parallel` just prints the jobs instead of actually executing them:

``` bash
$ parallel --dry-run --plus vpype read {} linemerge linesort write {/.svg/_processed.svg} ::: *.svg
```

### External scripts

The `cmd_script` command is a very useful generator that relies on an external Python script to produce geometries. Its use is demonstrated by the <span class="title-ref">alien.sh</span> and <span class="title-ref">alien2.sh</span> examples. A path to a Python file must be passed as argument. The file must implement a <span class="title-ref">generate()</span> function which returns a Shapely <span class="title-ref">MultiLineString</span> object. This is very easy and explained in the [Shapely documentation](https://shapely.readthedocs.io/en/latest/manual.html#collections-of-lines).


---


# Plug-ins

## Why?

Thanks to the CLI library which underlies *vpype* ([Click](https://click.palletsprojects.com)), writing plug-ins is easy and makes it a compelling option for your next plotter project. Plug-ins directly benefit from *vpype*'s facilities, such as SVG export, line optimization and sorting, scaling and pagination, etc. Plug-ins also benefit from the Click-inherited facilities to easily create compelling CLI interfaces to parametrize your plug-in.

Here are a few existing plug-ins to illustrate the possibilities:

- [vpype-perspective](https://github.com/abey79/vpype-perspective): put your art in perspective

  <img src="https://raw.githubusercontent.com/abey79/vpype-perspective/main/examples/images/wobbley_cylinders_like_1_plotted.jpg" height="400" alt="image" />

  <img src="https://raw.githubusercontent.com/abey79/vpype-perspective/main/examples/images/boxes1_like_1_doubled_in_perspective.jpeg" height="400" alt="image" />

- [vpype-gcode](https://github.com/plottertools/vpype-gcode): flexible export to gcode or any other text-based format

- [vpype-embroidery](https://github.com/EmbroidePy/vpype-embroidery): convert to/from common embroidery file formats

- [vpype-dxf](https://github.com/tatarize/vpype-dxf): read from DXF

- [vpype-vectrace](https://github.com/tatarize/vpype-vectrace): trace from bitmap images

- [vpype-ttf](https://github.com/johnbentcope/vpype-ttf): create text outlines with TTF fonts

- [occult](https://github.com/LoicGoulefert/occult): perform hidden line removal with closed geometry

  <img src="https://raw.githubusercontent.com/LoicGoulefert/occult/master/img/example8.png" height="400" alt="image" />

- [deduplicate](https://github.com/LoicGoulefert/deduplicate): remove overlapping lines

- [vpype-flow-imager](https://github.com/serycjon/vpype-flow-imager): convert image to flow field line art

  <img src="https://raw.githubusercontent.com/serycjon/vpype-flow-imager/master/examples/coffee.jpg" width="300" alt="image" />

  <img src="https://raw.githubusercontent.com/serycjon/vpype-flow-imager/master/examples/coffee_out.png" width="300" alt="image" />

- [vpype-pixelart](https://github.com/abey79/vpype-pixelart): easy pixel art plotting

  <img src="https://i.redd.it/g1nv7tf20aw11.png" width="400" alt="image" />

  <img src="https://i.imgur.com/dAPqFGV.jpg" width="400" alt="image" />

  (original art by Reddit user [u/\_NoMansDream](https://www.reddit.com/user/_NoMansDream/))

- [hatched](https://github.com/abey79/hatched): convert images to hatched patterns

  <img src="https://i.imgur.com/QLlBpNU.png" width="300" alt="image" />

  <img src="https://i.imgur.com/fRIrPV2.jpg" width="300" alt="image" />

## How?

The easiest way to start a plug-in project is to use the [Cookiecutter](https://cookiecutter.readthedocs.io) template for *vpype* plug-ins. You will first need to install `cookiecutter` command (see the website for more info). Then, run the following command:

``` bash
$ cookiecutter gh:abey79/cookiecutter-vpype-plugin
```

Cookiecutter will ask you a few questions and create a project structure automatically. To make it operational, the plug-in and its dependencies (including *vpype* itself) must be installed in a local virtual environment:

``` bash
$ cd my-vpype-plugin/
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install --editable .
```

Note the use of the `--editable` flag when installing the plug-in. With this flag, the actual code in the plug-in project is used for the plug-in, which means you can freely edit the source of the plug-in and it is automatically used the next time *vpype* is run.

Let's check that that everything works as expected:

``` bash
$ vpype --help
Usage: vpype [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  -v, --verbose
  -I, --include PATH  Load commands from a command file.
  --help              Show this message and exit.

Commands:

  ...

  Plugins:
    my-vpype-plugin  Insert documentation here.

  ...
```

The cookiecutter project includes a single `generator <fundamentals_generators>` command with the `@vpype_cli.generator <vpype_cli.generator>` decorator:

``` python
import click
import vpype as vp
import vpype_cli

@click.command()
@vpype_cli.generator
def my_vpype_plugin():
    """Insert documentation here.
    """
    lc = vp.LineCollection()
    return lc

my_vpype_plugin.help_group = "Plugins"
```

Generator commands must return a `vpype.LineCollection` instance. Plug-in can also contain `layer processor <fundamentals_layer_processors>` or `global processor <fundamentals_global_processors>` command, respectively using the `@vpype_cli.layer_processor <vpype_cli.layer_processor>` and `@vpype_cli.global_processor <vpype_cli.global_processor>` decorators. Check the API reference for more information.

## Getting help

This being a rather young project, documentation may be missing and/or rough around the edges. The author is available for support on [Drawingbots](https://drawingbots.net)'s [Discord server](https://discordapp.com/invite/XHP3dBg).


---

# Contributing

## How can you help?

Contributions are most welcome and there are many ways you can help regardless of your fluency with software development:

- First and foremost, do provide feedback on what you do with *vpype* and how you do it, either on the [DrawingBots Discord server](https://discordapp.com/invite/XHP3dBg) or by filling an [issue](https://github.com/abey79/vpype/issues). This knowledge is critically important to improve *vpype*.
- Write an [issue](https://github.com/abey79/vpype/issues) for any problem or friction point you encounter during the installation or use of *vpype* or for any feature you feel is missing.
- Make the present documentation better by fixing typos and improve the quality of the text (English is *not* the main author's native language). [This issue](https://github.com/abey79/vpype/issues/400) maintains a list of possible improvements.
- Write cookbook recipes for new workflows.
- Improving the test coverage and contributing to CI/CD aspects is welcome — and a good way to become familiar with the code.
- Improve existing features or contribute entirely new ones with a [pull request](https://github.com/abey79/vpype/pulls). If you plan on creating new commands, consider making a `plugin <plugins>` first — it will be easy to integrate it into *vpype*'s codebase later on if it makes sense.

Development guidelines:

- Write tests for your code (this project uses [pytest](https://docs.pytest.org/)).
- Use [black](https://github.com/psf/black) for code formatting and [isort](https://pycqa.github.io/isort/) for consistent imports.

## Development environment

*vpype* uses [Poetry](https://python-poetry.org) for packaging and dependency management and its [installation](https://python-poetry.org/docs/#installation) is required to prepare the development environment. It can be installed either using an install script, or using pipx. Run this command to use the install script:

``` bash
curl -sSL https://install.python-poetry.org | python3 -
```

Run this command for a pipx install:

``` bash
pipx install poetry
```

See Poetry's [installation instructions](https://python-poetry.org/docs/#installation) for more information.

You can then download *vpype*, prepare a virtual environment and install all dependencies with a few commands:

``` bash
git clone https://github.com/abey79/vpype
cd vpype
poetry install -E all --with docs
```

You can execute *vpype* (which installed in the project's virtual environment managed by Poetry) with the `poetry run` command:

``` bash
poetry run vpype --help
```

Alternatively, you can activate the virtual environment and then directly use *vpype*:

``` bash
poetry shell
vpype --help
```

## Running the tests

You can run tests with the following command:

``` bash
poetry run pytest
```


---

# CLI reference


---

# API reference

**Modules**


---

# Change log

## 1.16.0

Release date: UNRELEASED

### New features and improvements

* ...

### Bug fixes

* ...

### Other changes

* No longer generate a Windows installer (#822) 


## 1.15.0

Release date: 2025-08-04

### New features and improvements

* Added a `lineshuffle` command to randomize the plotting order of lines in the current geometry (thanks to @gatesphere) (#715)
* Added a `cropcricle` command to crop the current geometry to a circle (#808)
* Added a `--orientation` option to the `pagerotate` command to conditionally rotate the page to a target orientation (thanks to @gatesphere) (#705)
* Added support for Python 3.13 and dropped support for Python 3.10 (#784)

### Bug fixes

* Fixed a crash when reading SVG with simplify active (via the `read --simplify` command or the read APIs with `simplify=True`) (thanks to @nataquinones) (#732)
* Fixed the formatting of many commands' help text and added a snapshot test to avoid future regressions (#810)
* Fixed erroneous mention of `--page-size` in `layout`'s inline help

### Other changes

* Use Ruff for code formatting (supersedes Black) (#737)


## 1.14.0

Release date: 2024-01-08

### New features and improvements

* Added support for Python 3.12 and dropped support for Python 3.9 (#681)
* Added a `--no-bbox` option to the `layout` command to use the pre-existing page size instead of the geometry bounding box as basis for layout (#682)
* Added a `--flip` option to the `reverse` command to also flip the line direction (#654)
* Added a `--hyphenate LANG` option to the `text` command (thanks to @pepijndevos) (#668)

### Bug fixes

* Fixed issue with `ImageRenderer` where the GL context wasn't released, ultimately causing a crash when running the test suite (which could involve many hundreds of context creation) (#616)
* Fixed CLI help for the `lreverse` command (#683)

### Other changes

* The project now uses [Ruff](https://github.com/astral-sh/ruff) for linting (supersedes isort) (#646)


## 1.13.0

Release date: 2023-03-13

[Annotated Release Notes](https://bylr.info/articles/2023/03/13/annotated-release-notes-vpype-1.13/)

### New features and improvements

* Added support for Python 3.11 and dropped support for Python 3.8 (#581)
* Added the `lid` built-in expression variable for generator and layer processor commands (#605)

### Bug fixes

* Fixed a design issue with the `read` command where disjoint groups of digits in layer names could be used to determine layer IDs. Only the first contiguous group of digits is used now, so a layer named "01-layer1" has layer ID of 1 instead of 11 (#606)
* Fixed an issue on Wayland-based Linux distributions where using the viewer (e.g. with the `show` command) would crash (#607)

### Known issue

* As of PySide 6.4.2, a refresh issue arises on macOS when the viewer window is resized by a window manager (#603)


## 1.12.1

Release date: 2022-11-12

**Note**: This is the last version of *vpype* to support Python 3.7.

### Bug fixes

* Pinned ModernGL to 5.7.0 or earlier to avoid an [issue](https://github.com/moderngl/moderngl/issues/525) introduced in 5.7.1 (2ce6aef780e8a280375cb230d732d092a0635ad3)


## 1.12.0

Release date: 2022-10-25

[Annotated Release Notes](https://bylr.info/articles/2022/10/25/annotated-release-notes-vpype-1.12/)

### New features and improvements

* The `layout` command now properly handles the `tight` special case by fitting the page size around the existing geometries, accommodating for a margin if provided (#556)
* Added new units (`yd`, `mi`, and `km`) (#541)
* Added `inch` unit as a synonym to `in`, useful for expressions (in which `in` is a reserved keyword) (#541)
* Migrated to PySide6 (from PySide2), which simplifies installation on Apple silicon Macs (#552, #559, #567)

### Bug fixes

* Fixed a viewer issue where page width/height of 0 would lead to errors and a blank display (#555)
* Fixed a viewer issue where fitting the view to the document would not adjust when page size changes (*vsketch* only) (#564)

### API changes

* Added `vpype.format_length()` to convert pixel length into human-readable string with units (#541)

### Other changes

* Updated [svgelements](https://github.com/meerk40t/svgelements) to 1.8.4, which fixes issue with some SVG constructs used by Matplotlib exports (#549)
* [Poetry](https://python-poetry.org) 1.2 or later is not required (developer only) (#541)
* A `justfile` is now provided for most common operations (install, build the documentation, etc.) (#541)
* Migrated to [Plausible.io](https://plausible.io) (from Google Analytics) for [vpype.readthedocs.io](https://vpype.readthedocs.io) (#546)


## 1.11.0

Release date: 2022-07-06

[Annotated Release Notes](https://bylr.info/articles/2022/07/06/annotated-release-notes-vpype-1.11/)

### New features and improvements

* Added the `splitdist` command to split layers by drawing distance (thanks to @LoicGoulefert) (#487, #501)
* Added `--keep-page-size` option to `grid` command (#506)
* Added meters (`m`) and feet (`ft`) to the supported units (#498, #508)
* Improved the `linemerge` algorithm by making it less dependent on line order (#496)
* Added HPGL configurations for the Houston Instrument DMP-161, HP7550, Roland DXY 1xxxseries and sketchmate plotters (thanks to @jimmykl and @ithinkido) (#472, #474)
* The `forfile` command now sorts the files by their name before processing them (#506)

### Bug fixes

* Fixed an issue with blocks where certain nested commands could lead totally unexpected results (#506)
* Fixed an issue with the `lmove` command where order would not be respected in certain cases such as `lmove all 2` (the content of layer 2 was placed before that of layer 1) (#506)
* Fixed an issue with expressions where some variable names corresponding to units (e.g. `m`) could not be used (expressions may now reuse these names) (#506)

### API changes

* Removed the faulty `temp_document()` context manager from `vpype_cli.State()` (#506)
* Added equality operator to `vpype.LineCollection` and `vpype.Document` (#506)

### Other changes

* Removed dependence on `setuptools` (#454, #468)
* Pinned Shapely to 1.8.2, which is the first release in a long time to have binaries for most platforms/Python release combination (including Apple-silicon Macs and Python 3.10) (#475)
* Removed deprecated API (#507)


## 1.10.0

Release date: 2022-04-07

[Annotated Release Notes](https://bylr.info/articles/2022/04/07/annotated-release-notes-vpype-1.10/)

### New features and improvements

* Added the `alpha` command to set layer opacity without changing the base color (#447, #451)
* Improved support for layer pen width and opacity in the viewer (#448)

  * The "Pen Width" and "Pen Opacity" menus are now named "Default Pen Width" and "Default Pen Opacity". 
  * The layer opacity is now used for display by default. It can be overridden by the default pen opacity by checking the "Override" item from the "Default Pen Opacity" menu.
  * The layer pen width is now used for display by default as well. Likewise, it can be overridden by checking the "Override" item from the "Default Pen Width" menu.

* Added HPGL configuration for the Calcomp Artisan plotter (thanks to Andee Collard and @ithinkido) (#418)
* Added the `--dont-set-date` option to the `write` command (#442)
* The `read` command now better handles SVGs with missing `width` or `height` attributes (#446)

  When the `width` or `height` attribute is missing or expressed as percent, the `read` command now attempts to use the `viewBox` attribute to set the page size, defaulting to 1000x1000px if missing. This behavior can be overridden with the `--display-size` and the `--display-landscape` parameters. 


### Bug fixes

* Fixed an issue with `forlayer` where the `_n` variable was improperly set (#443)
* Fixed an issue with `write` where layer opacity was included in the `stroke` attribute instead of using `stroke-opacity`, which, although compliant, was not compatible with Inkscape (#429)
* Fixed an issue with `vpype --help` where commands from plug-ins would not be listed (#444)
* Fixed a minor issue where plug-ins would be reloaded each time `vpype_cli.execute()` is called (#444)
* Fixed a rendering inconsistency in the viewer where the ruler width could vary by one pixel depending on the OpenGL driver/GPU/OS combination (#448)


### API changes

* Changed the parameter name of both `vpype_viewer.Engine()` and `vpype_viewer.render_image()` from `pen_width` and `pen_opacity` to `default_pen_width` and `default_pen_opacity` (breaking change) (#448)
* Added `override_pen_width` and `override_pen_opacity` boolean parameters to both `vpype_viewer.Engine()` and `vpype_viewer.render_image()` (#448)
* Added `vpype_cli.FloatType()`, `vpype_cli.IntRangeType()`, `vpype_cli.FloatRangeType()`, and `vpype_cli.ChoiceType()` (#430, #447)
* Changed `vpype.Document.add_to_sources()` to also modify the `vp_source` property (#431)
* Added a `set_date:bool = True` argument to `vpype.write_svg()` (#442)
* Changed the default value of `default_width` and `default_height` arguments of `vpype.read_svg()` (and friends) to `None` to allow `svgelement` better handle missing `width`/`height` attributes (#446)


### Other changes

* Added support for Python 3.10 and dropped support for Python 3.7 (#417)
* Miscellaneous code cleaning and fixes (#440, 906087b)
* Updated installation instructions to use pipx (#428)
* Updated the [documentation](https://vpype.readthedocs.io/en/latest/) template (#428)
* Updated code base with modern typing syntax (using [pyupgrade](https://github.com/asottile/pyupgrade)) (#427)


## 1.9.0

Release date: 2022-03-03

[Annotated Release Notes](https://bylr.info/articles/2022/03/03/annotated-release-notes-vpype-1.9/)

**Note**: This is the last version of *vpype* to support Python 3.7.

### New features and improvements

* Added support for global and per-layer [properties](https://vpype.readthedocs.io/en/latest/fundamentals.html#properties) (#359)
  
  This feature introduces metadata to the pipeline in the form of properties which may either be attached to specific layers (layer property) or all of them (global property). Properties are identified by a name and may be of arbitrary type (e.g. integer, floating point, color, etc.). A number of [system properties](https://vpype.readthedocs.io/en/latest/fundamentals.html#system-properties) with a specific name (prefixed with `vp_`) and type are introduced to support some of the new features.

* Layer color, pen width, and name are now customizable (#359, #376, #389)
  * The `read` commands now sets layer color, pen width, and name based on the input SVG if possible.
  * The new `color`, `penwdith`, and `name` commands can be used to modify layer color, pen width, and name.
  * The new `pens` command can apply a predefined or custom scheme on multiple layers at once. Two common schemes are built-in: `rgb` and `cmyk`. [Custom schemes](https://vpype.readthedocs.io/en/latest/cookbook.html#creating-a-custom-pen-configuration) can be defined in the configuration file.
  * The `show` and `write` commands now take into account these layer properties.

* The `read` command now records the source SVG paths in the `vp_source` and `vp_sources` system properties (see the [documentation](https://vpype.readthedocs.io/en/latest/fundamentals.html#system-properties)) (#397, #406, #408)

* Added [property substitution](https://vpype.readthedocs.io/en/latest/fundamentals.html#property-substitution) to CLI user input (#395)

  The input provided to most commands' arguments and options may now contain substitution patterns which will be replaced by the corresponding property value. Property substitution patterns are marked with curly braces (e.g. `{property_name}`) and support the same formatting capabilities as the Python's [`format()` function](https://docs.python.org/3/library/string.html#formatstrings).

* Added [expression substitution](https://vpype.readthedocs.io/en/latest/fundamentals.html#expression-substitution) to CLI user input (#397)

  The input provided to most command's arguments and options may now contain expression patterns which are evaluated before the command is executed. Expression patterns are marked with the percent symbol `%` (e.g. `%3+4%`) and support a large subset of the Python language. [A](https://vpype.readthedocs.io/en/latest/cookbook.html#load-multiple-files-merging-their-layers-by-name) [lot](https://vpype.readthedocs.io/en/latest/cookbook.html#cropping-and-framing-geometries) [of](https://vpype.readthedocs.io/en/latest/cookbook.html#laying-out-multiple-svgs-on-a-grid) [examples](https://vpype.readthedocs.io/en/latest/cookbook.html#create-interactive-scripts-with-input) were added in the [cookbook](https://vpype.readthedocs.io/en/latest/cookbook.html).

* Added the `--attr` option to the `read` command to (optionally) sort geometries by attributes (e.g. stroke color, stroke width, etc.) instead of by SVG layer (#378, #389)

* The `read` and `write` commands now preserve a sub-set of SVG attributes (experimental) (#359, #389)
  
  The `read` command identifies SVG attributes (e.g. `stroke-dasharray`) which are common in all geometries within each layer. These attributes are saved as layer properties with their name prefixed with `svg_` (e.g. `svg_stroke-dasharray`). The `write` command can optionally restore these attributes in the output SVG using the `--restore-attribs` option.

* Introduced new commands for low-level inspection and modification of properties (#359)

  * `propget`: gets the value of a given global or layer property
  * `proplist`: lists all global and/or layer properties and their value
  * `propset`: sets the value of a given global or layer property
  * `propdel`: deletes a given global or layer property
  * `propclear`: removes all global and/or layer properties

* Updated layer operation commands to handle properties (#359)

  * When a single source layer is specified and `--prob` is not used, the `lcopy` and `lmove` commands now copy the source layer's properties to the destination layer (possibly overwriting existing properties).
  * When `--prob` is not used, the `lswap` command now swaps the layer properties as well.
  * These behaviors can be disabled with the `--no-prop` option.

* Improved block processors (#395, #397)

  * Simplified and improved the infrastructure underlying block processors for better extensibility.
  * The `begin` marker is now optional and implied whenever a block processor command is encountered. *Note*: the `end` marker must always be used to mark the end of a block.
  * Commands inside the block now have access to the current layer structure and its metadata.

* Improved the `grid` block processor (#397)
  
  * The page size is now updated according to the grid size.
  * The command now sets expression variables for use in the nested pipeline.
  * Cells are now first iterated along rows instead of columns.

* The `repeat` block processor now sets expression variables for use in the nested pipeline (#397)
* Added `forfile` block processor to iterate over a list of file (#397)
* Added `forlayer` block processor to iterate over the existing layers (#397)
* Added the `eval` command as placeholder for executing expressions (#397)
* The `read` command now will ignore a missing file if `--no-fail` parameter is used (#397)
  
* Changed the initial default target layer to 1 (#395)
  
  Previously, the first generator command of the pipeline would default to create a new layer if the `--layer` option was not provided. This could lead to unexpected behaviour in several situation. The target layer is now layer 1. For subsequent generators, the existing behaviour of using the previous generator target layer as default remains.   

* Added `pagerotate` command, to rotate the page layout (including geometries) by 90 degrees (#404)
* Added `--keep` option to the `ldelete` command (to delete all layers but those specified) (#383)
* Providing a non-existent layer ID to any `--layer` parameter now generates a note (visible with `--verbose`) (#359, #382)

### Bug fixes

* Fixed an issue with the `random` command when using non-square area (#395)

### API changes

* Moved all CLI-related APIs from `vpype` to `vpype_cli` (#388)

  A number of CLI-related APIs remained in the `vpype` package for historical reasons. They are now located in the `vpype_cli` package for consistency and to allow for future extensions.

  * Moved the following decorators, classes, and functions from the `vpype` package to the `vpype_cli` package. Importing from `vpype` will now generate a deprecation warning:
    * `@block_processor`
    * `@generator`
    * `@global_processor`
    * `@layer_processor`
    * `@pass_state`
    * `AngleType`
    * `LayerType`
    * `LengthType`
    * `PageSizeType`
    * `multiple_to_layer_ids()`
    * `single_to_layer_id()`
  * Moved and renamed `vpype.VpypeState` to `vpype_cli.State`. Using the old name will generate a deprecation warning. 
  * Removed the following long-time deprecated aliases:
    * `vpype.Length` (alias to `vpype_cli.LengthType`) 
    * `vpype.VectorData` (alias to `vpype.Document`)
    * `vpype.convert()`(alias to `vpype.convert_length()`)
    * `vpype.convert_page_format()` (alias to `vpype.convert_page_size()`)
    * `vpype.PAGE_FORMATS` (alias to `vpype.PAGE_SIZES`)

* Added support for property substitution in Click type subclasses (#395)
  * Existing type classes (`AngleType`, `LengthType`, `PageSizeType`) now support property substitution.
  * Added `TextType` and `IntegerType` to be used instead of `str`, resp. `int`, when property substitution support is desired.
* Updated the block processor API (breaking change) (#395)
  
  Block processor commands (decorated with `@block_processor`) are no longer sub-classes of `BlockProcessor` (which has been removed). The are instead regular functions (like commands of other types) which take a `State` instance and a list of processors as first arguments.

* Added methods to `vpype_cli.State` to support expression and property substitution, deferred arguments/options evaluation and block processor implementations (#395, #397)
* `vpype.Document` and `vpype.LineCollection` have multiple, non-breaking additions to support metadata (in particular through the `vpype._MetadataMixin` mix-in class) (#359, #397)
* Renamed `vpype.Document.empty_copy()` to `vpype.Document.clone()` for coherence with `vpype.LineCollection` (the old name remains for backward compatibility) (#359, #380) 
* Added `vpype.read_svg_by_attribute()` to read SVG while sorting geometries by arbitrary attributes (#378)
* Added an argument to `vpype_cli.execute()` to pass global option such as `--verbose` (#378)

### Other changes

* Renamed the bundled config file to `vpype_config.toml` (#359)
* Pinned poetry-core to 1.0.8 to enable editable installs (#410)
* Changed dependencies to dataclasses (instead of attrs) and tomli (instead of toml) (#362)
* Removed dependency to click-plugin (#388)
* Improved documentation, in particular the [Fundamentals](https://vpype.readthedocs.io/en/latest/fundamentals.html) and [Cookbook](https://vpype.readthedocs.io/en/latest/cookbook.html) sections (#359, #363, #397)


## 1.8.1

Release date: 2022-01-13

### Security fix

* Updated Pillow to 9.0.0 due to vulnerabilities in previous versions (CVE-2022-22815, CVE-2022-22817, CVE-2022-22816)


## 1.8.0

Release date: 2021-11-25

### New features and improvements

* Added `lswap` command to swap the content of two layers (#300)
* Added `lreverse` command to reverse the order of paths within a layer (#300)
* Improved HPGL export (#253, #310, #316, #335)

  * Relative coordinates are now used by default to reduce file size. If absolute coordinates are needed, they a new `--absolute` option for the `write` command.
  * A homing command (as defined by the `final_pu_params` configuration parameter) is no longer emitted between layers.
* The viewer (`show` command) now catches interruptions from the terminal (ctrl-C) and closes itself (#321)
* The `read` command now accepts `-` as file path to read from the standard input (#322)

### Bug fixes

* Fixed issue with HPGL export where page size auto-detection would fail when using the default device from the config file (instead of specifying the device with `--device`) (#328)
* Fixed issue where the viewer would crash with empty layers (#339) 

### Other changes

* Updated to Shapely 1.8 (transition release toward 2.0) and fixed deprecation warnings (#325, #342)


## 1.7.0

Release date: 2021-06-10

**Important**: for a regular installation, *vpype* must now be installed/updated with the following command (see details below):
```
pip install -U vpype[all]
```

### New features and improvements

* Installing the viewer (`show` command) and its dependencies is now optional (#254)
  
  The `all` extra must now be provided to `pip` for a complete install:
  ```
  pip install -U vpype[all]  # the viewer is fully installed
  pip install -U vpype       # the viewer and its dependencies are NOT installed
  ```
  Forgoing the viewer considerably reduces the number of required dependencies and may be useful for embedded (e.g. Raspberry Pi) or server installs of *vpype*, when the `show` command is not necessary. Note that the Windows installer is not affected by this change.
* Added an optional, global optimization feature to `linesort` (#266, thanks to @tatarize)

  This feature is enabled by adding the `--two-opt` option. Since it considerably increases the processing time, it should primarily be used for special cases such as plotting the same file multiple times.

### Bug fixes

* Fixed broken Windows installer (#285)
* Fixed an issue where `read` would crash with empty `<polygon>` tags and similar degenerate geometries (#260)
* Fixed an issue where `linesimplify` would skip layers containing a single line (#280)
* Fixed an issue where floating point value could be generated for HPGL VS commands (#286)

### Other changes

* Updated to Click 8.0.1 (#282) 


## 1.6.0

Release date: 2021-03-10

### New features and improvements

* Added new `text` command  (#226, #227)
  
  This command renders text using Hershey fonts. It can create text blocks with wrapping, custom alignment, and optional justification. A set of Hershey fonts is included.

  **Notes**:
  * This feature was previously partially available via the [*vpype-text*](https://github.com/abey79/vpype-text) plug-in, which is now deprecated. The plug-in should no longer be used, and, if present, uninstalled.
  * The implementation of this feature as well as the set of Hershey font is based on the [axi project](https://github.com/fogleman/axi) -- thanks @fogleman!

* Added `squiggles` command for a "shaky hand" or "liquid-like" styling (#217)
* Added probabilistic mode to `lmove`, `lcopy`, and `ldelete` to enable various random coloring effects (#220)

### Bug fixes

* Fixed missing documentation for the `reverse` command (#217)

### API changes

* Added `vpype.FONT_NAMES`, `vpype.text_line`, and `vpype.text_block` for Hershey-font-based text rendering (#226, #227)

### Other changes

* Dropped support for Python 3.6 (#207)


## 1.5.1

Release date: 2021-02-19

### Bug fixes

* Fixed a shader compilation issue arising on some Windows configuration (#210)
* Fixed UI glitches when using both non-HiDPI and HiDPI (a.k.a Retina) monitors (#211)


## 1.5.0

Release date: 2021-02-16

**Note**: This is the last version of *vpype* to support Python 3.6.

### New features and improvements

* Viewer improvements:
  * Added rulers with dynamic scale to the display (can be optionally hidden) (#199)
  * Added metric and imperial unit system (in addition to pixels), used by the rulers and the mouse coordinates display (#199, #205)
  * Adjusted the size of the mouse coordinates text on Windows (#199)
  * Added support to adjust the scale of the UI via `~/.vpype.toml` (#203)
  
    This is achieved by adding the following lines to your `~/.vpype.toml` file:
    ```toml
    [viewer]
    ui_scale_factor = 1.5
    ```  
    A value of 1.5 may be useful on some Windows configurations where the default UI is very small.
  
### Bug fixes

* Fixed issue on Linux where `show` would revert to the classic viewer due to a `libX11` discovery issue (#206)

### API changes

* Renamed `vpype.CONFIG_MANAGER` in favour of `vpype.config_manager` (existing name kept for compatibility) (#202)


## 1.4.0

Release date: 2021-02-08

### New features and improvements

* Python 3.9.1 (or later) is finally supported and now is the recommended version (#115)
* Viewer improvements:
  * The viewer will now keep the page fitted to the window when resizing, until manually zoomed and/or panned (#193)
  * Significantly optimized launch and setting changes times (#184, #195)

### Bug fixes

* Various documentation fixes and improvements:
  * improved the `layout` command's help text
  * improved the cookbook section on using `GNU parallel` (#108)
  * fixed typos related to the `layout` command in the cookbook (#186, thanks to @f4nu)

### API changes

* Added support for a sidebar in the viewer (#194)


## 1.3.0

Release date: 2021-01-27

### New features and improvements

* Added new `layout` command (#168)
  
  This command automates the page layout process on a specified the page size by centering the geometries (with
  customizable horizontal and vertical alignment) and optionally fitting to specified margins. It intends to supersede
  `write`'s layout options (i.e. `--page-size` and `--center`) in more intuitive way. In particular this command
  acts on the pipeline rather than on the output file so its effect can be previewed with the `show` command.

* (Beta) Complete rewrite of the viewer underlying the `show` command (#163)
  * fully hardware-accelerated rendering engine
  * smooth zooming and panning, with touchpad and mouse support
  * preview mode with adjustable pen width and opacity
  * outline mode with optional colorful and point display
  * optional pen-up trajectories display
  * per-layer visibility control
  * interactively adjustable display settings
    
  **Note**: This new viewer is a beta feature and will evolve in future versions. Your feedback is welcome. The current, matplotlib-based viewer is still available using `show --classic`.

* Added support for arbitrary paper size to `write`'s HPGL output (configuration for the Calcomp Designmate included, check the documentation for details) (#178)
* Added large format paper sizes (A2, A1, A0) (#144)
* The `splitall` command will now filter out segments with identical end-points (#146)
* Minor loading time improvement (#133)

### Bug fixes

* Various documentation fixes (#170, #172, thanks to @theomega)

### API changes

* Added the new viewer engine and Qt-based GUI (#163)


## 1.2.1

Release date: 2020-12-26

### Hot fix

* Fixed systematic crash with `read` command due to bad dependency version (#140)


## 1.2.0

Release date: 2020-12-17

### New features and improvements

* A Windows installer is now available (#120)
* HPGL output: `--page-size` is no longer mandatory and `write` will try to infer which paper to use based on the current page size (#132)  
* Added `reverse` command (#129)

### Bug fixes

* Fixed crash for SVG with <desc> element (#127)
* Fixed an issue where output HPGL file could be empty (#132)


## 1.1.0
  
Release date: 2020-12-10

### New features and improvements
  
* Added `snap` command (#110)
* Invisible SVG elements are now discarded (#103)
* Add support for angle units (affects `rotate`, `skew`, and `arc` commands, `--radian` option is removed) (#111)

### Bug fixes
  
* Fixed installation issue on Windows ("Numpy sanity check RuntimeError") (#119)
* Fixed `write` to cap SVG width and height to a minimum of 1px (#102)
* Fixed grouping of `stat` command in `vpype --help`

### API changes
  
* Added `vpype_cli.execute()` to execute a vpype pipeline from Python (#104)
* Added `vpype.convert_angle()` and `vpype.AngleType` (#111)


## 1.0.0

Release date: 2020-11-29

* Initial release


---

# Licenses

## *vpype* license

```
MIT License

Copyright (c) 2019-2022 Antoine Beyeler & Contributors

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

```

## Third-party licenses

```
=============================================================================
Includes portions of click-plugins under the following license:
-----------------------------------------------------------------------------
New BSD License

Copyright (c) 2015-2019, Kevin D. Wurster, Sean C. Gillies
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither click-plugins nor the names of its contributors may not be used to
  endorse or promote products derived from this software without specific prior
  written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
=============================================================================
```


---

