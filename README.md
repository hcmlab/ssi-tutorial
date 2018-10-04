# ssi-tutorial
A standalone tutorial introducing the SSI framework.

## Motivation

This is a good starting point for people interested in the [Social Signal Interpretation (SSI)](http://openssi.net) framework. It is meant to run standalone even if SSI is not installed on the computer. It is not as detailed as the [official documentation](https://rawgit.com/hcmlab/ssi/master/docs/index.html), so we encourage users to refer to it if more information is wished. However, the examples in this tutorial are generally more advanced than those in the official documentation and hence might be of interest even for advanced users, too.

## Installation

After cloning the repository run `install.cmd`, which will download core binaries from the official [SSI Github](https://github.com/hcmlab/ssi/) project and install embedded [Python](https://www.python.org/). Tutorials are organized in directories with a trailing number (e.g. `01_basics`). A tutorial may consist of several examples, which are again orded by a trailing number. Each example exists of a `.pipeline` file (the actual pipeline), which is accompanied by files ending on `.html` and `.cmd` (generated during installation). You can open the `html` file in a browser of your choice, which will highlight the most important pieces of the code. Then, execute the batch file to actually run the pipeline.

## HTML Generation

If you wish to add new examples, you can use the Python script `pipe2html.py` in the root folder. It takes a `.pipeline` file and automatically converts it to a `.html` file. Therefore [Pandoc](https://pandoc.org/installing.html) is required, so please make sure you have installed it on your computer.

```
usage: pipe2html.py [-h] [--author author] [--bin bin] path

Convert pipeline to a html document.

positional arguments:
  path         path to pipeline or a folder with pipelines

optional arguments:
  -h, --help   show this help message and exit
  --logo logo  path to logo
  --bin bin    path to binaries
```

The parser will look for parts of the pipeline that are embedded in a comment of the following form (please note the trailing `<!---->` as otherwise the comment will be ignored):

```
<!-- comment -->
code
<!---->
```

The comment will be added to the html page followed by the code snippet. Obviously, you can markdown the comment with any tags supported by [Pandoc](https://pandoc.org/MANUAL.html).

If you wish to insert code from another file, you can use the following syntax:

```
\input{path=name.ext;lines=[4,5,6];type=xml}
```

The parameter `lines` will be evaluated as Python expression, i.e. you can do things like `lines=[1,4] + list(range(12,15))`. If it is missing, the whole file will be inserted. The parameter `type` will be used to apply proper syntax highlighting and can be omitted, too. If the input file is a Python file, you can replaces `lines=...` with `function=fun_name`.

Enjoy!

