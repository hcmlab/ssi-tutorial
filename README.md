# ssi-tutorial
A standalone tutorial introducing the SSI framework.

## Motivation

This is a good starting point for people interested in the [Social Signal Interpretation (SSI)](http://openssi.net) framework. It is meant to run standalone even if SSI is not installed on the computer. It is not as detailed as the [official documentation](https://rawgit.com/hcmlab/ssi/master/docs/index.html), so we encourage users to refer to it if more information is wished. However, the examples in this tutorial are generally more advanced than those in the official documentation and hence might be of interest even for advanced users, too.

## Installation

After cloning the repository run ``install.cmd``, which will download core binaries from the official [SSI Github](https://github.com/hcmlab/ssi/) project. You will also find a couple of directories with a trailing number (e.g. ``01_basics``). They include the examples featured by this tutorial and again include files ordered by a trailing number. Each example exists of a ``.pipeline`` file (the actual pipeline), which is accompanied by files ending on ``.html`` and ``.cmd``. The first one is automatically generated from the pipeline to highlight the most important pieces of the code. Just open it in your favourite browser to access this information. To see the pipeline in action, execute the batch file.

## HTML Generation

If you wish to add your own examples, you can use the Python script ``pipe2html.py`` in the root folder. It takes a ``.pipeline`` file and automatically converts it to a ``.html`` file. Therefore [Pandoc](https://pandoc.org/installing.html) is required, so please make sure you have installed it on your computer.

```
usage: pipe2html.py [-h] [--author author] [--bin bin] path

Convert pipeline to a html document.

positional arguments:
  path             path to pipeline

optional arguments:
  -h, --help       show this help message and exit
  --author author  name of author
  --bin bin        path to binaries
```

The parser will look for parts of the pipeline that are embedded in a comment of the following form (please note the trailing ``<!---->`` as otherwise the comment will be ignored):

```
<!-- comment -->
code
<!---->
```

The comment will be added to the html page followed by the code snippet. Obviously, you can markdown the comment with any tags supported by [Pandoc](https://pandoc.org/MANUAL.html).

Enjoy!

