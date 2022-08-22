# CLICSViz: Package for the Creation of Interactive Visualizations with the help of JavaScript and D3

## Getting Started

To start this project, just install the requirements:

```shell
$ pip install -r requirements.txt
```

Then you should select one or more CLDF datasets to be used to compute yoru colexifications. These should be cloned in the folder called `cldf-datasets`.

This can be done as follows:

```shell

$ cd cldf-datasets
$ git clone https://github.com/intercontinental-dictionary-series/ids
$ git clone https://github.com/intercontinental-dictionary-series/yuchinese
```

## Compute the Colexifications

Having installed all dependencies and cloned the two repositories, just type:

```shell
$ python clicsviz.py
```

## View in Browser

The best way to view colexifications in the browser is to make your own server with Python:

```shell
$ cd app
$ python http.server 8000
```

When opening now your browser at http://localhost:8000 you will be able to select individual networks and inspect them interactively.

# How to Cite

This code has been introduce as part of a blog post from August 24, 2022, which you should quote as follows:

> List, Johann-Mattis (2022): How to Visualize Colexification Networks with JavaScript and D3 (How to do X in Linguistics 12). Computer-Assisted Language Comparison in Practice 5.8. https://calc.hypotheses.org/4351
