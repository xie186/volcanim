# volcanim

Volcanim is a tool for creating animated volcano plots from DESeq2 results.

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