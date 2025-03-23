# Volcanim

Volcanim is a tool for creating animated volcano plots from DESeq2 results using Manim. It can be used both as a command-line tool and as a library.

## Features

- Generate animated volcano plots from DESeq2 results.
- Highlight specific genes in the plot.
- Create legends to explain different categories of points in the plot.

## Installation

To install Volcanim, clone the repository and install the required dependencies:

```
git clone https://github.com/yourusername/volcanim.git
cd volcanim
pip install -r requirements.txt
```

## Usage 

```
 python volcanim/cli.py \
         data/DESeq2_airway_results.csv \
         test.mp4 \
         --highlight MT2A,ADAMTS1,FGD4
```