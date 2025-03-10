import argparse
import pandas as pd
import numpy as np
from manim import *

class EnhancedVolcano(Scene):
    def __init__(self, data_file, output_file, resolution, pval_threshold=0.05, lfc_threshold=1.0):
        self.data_file = data_file
        self.output_file = output_file
        self.resolution = resolution
        self.pval_threshold = pval_threshold
        self.lfc_threshold = lfc_threshold
        super().__init__()
    
    def construct(self):
        df = pd.read_csv(self.data_file, sep="\t" if self.data_file.endswith(".tsv") else ",")
        df['-log10pval'] = -np.log10(df['pvalue'])
        
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, max(df['-log10pval']) + 1, 2],
            axis_config={"include_tip": False},
        ).add_coordinates()
        
        labels = axes.get_axis_labels("Log2 Fold Change", "-log10(p-value)")
        
        self.play(Create(axes), Write(labels))
        
        points = VGroup()
        significant = VGroup()
        
        for _, row in df.iterrows():
            dot = Dot(axes.c2p(row['log2FoldChange'], row['-log10pval']), color=BLUE, radius=0.05)
            points.add(dot)
            
            if row['pvalue'] < self.pval_threshold and abs(row['log2FoldChange']) > self.lfc_threshold:
                dot.set_color(RED)
                significant.add(dot)
        
        self.play(LaggedStart(*[FadeIn(dot) for dot in points], lag_ratio=0.05))
        
        if significant:
            self.play(LaggedStart(*[dot.animate.scale(1.5) for dot in significant], lag_ratio=0.1))
        
        # Add Legend
        legend = VGroup(
            Dot(color=BLUE, radius=0.05).next_to(axes, RIGHT, buff=1),
            Text("Non-significant", font_size=24).next_to(axes, RIGHT, buff=1.5),
            Dot(color=RED, radius=0.05).next_to(axes, RIGHT, buff=2.5),
            Text("Significant", font_size=24).next_to(axes, RIGHT, buff=3)
        )
        
        self.play(FadeIn(legend))
        
        self.wait(2)
        
        self.renderer.file_writer.output_filename = self.output_file
        self.renderer.file_writer.resolution = self.resolution

def generate_volcano_plot(input_file, output_file, resolution, pval_threshold=0.05, lfc_threshold=1.0):
    scene = EnhancedVolcano(input_file, output_file, resolution, pval_threshold, lfc_threshold)
    scene.render()