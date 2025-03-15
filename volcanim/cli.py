import os
import argparse
import sys
# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(script_dir, "..")))
from volcanim.plot import generate_volcano_plot

def main():
    parser = argparse.ArgumentParser(description="Generate an animated Enhanced Volcano plot using Manim.")
    parser.add_argument("input_file", help="Path to CSV/TSV file with 'log2FoldChange' and 'pvalue'.")
    parser.add_argument("output_file", help="Path to save the output video file.")
    parser.add_argument("--highlight", type=str, default="", help="Genes to highlight in the plot.")
    parser.add_argument("--resolution", type=str, default="480p", help="Resolution of the output video.")
    parser.add_argument("--pval", type=float, default=0.0001, help="p-value threshold for significance.")
    parser.add_argument("--lfc", type=float, default=1.0, help="Log2 fold change threshold for significance.")
    
    args = parser.parse_args()
    generate_volcano_plot(args.input_file, args.output_file, 
                          args.resolution, args.pval, 
                          args.lfc, args.highlight)

if __name__ == "__main__":
    main()


