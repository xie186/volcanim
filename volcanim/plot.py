import argparse
import pandas as pd
import numpy as np
from manim import *
import logging
from .highlight import draw_gene_dots
from .legend import create_legend

def plot_w_PMobject(df, plane, pval_threshold=0.05, lfc_threshold=1.0):
    # # Create points in a vectorized way
    points_data = np.array([[row['log2FoldChange'], row['-log10pval'], 0] for _, row in df.iterrows()])
    is_significant = (df['pvalue'] < pval_threshold) & (abs(df['log2FoldChange']) > lfc_threshold)
    # Use PMobject for much faster rendering
    non_sig_points = PMobject()
    sig_points = PMobject()
    for i, point in enumerate(points_data):
        coords = plane.c2p(*point)
        #logging.info(f'point: {point}')
        if is_significant.iloc[i]:
            sig_points.add_points([coords], color=RED)
        else:
            non_sig_points.add_points([coords], color=BLUE)
    return non_sig_points, sig_points

def plot_w_PMobject_batch(df, plane, pval_threshold=0.05, lfc_threshold=2.0, batch_size=1000):
    points_data = np.array([[row['log2FoldChange'], row['-log10pval'], 0] for _, row in df.iterrows()])
    pvalues = df['pvalue']
    log2fc = df['log2FoldChange']
    
    # Store PMobject batches for animation
    non_sig_batches = []
    high_lfc_non_sig_batches = []
    high_lfc_sig_batches = []
    low_lfc_sig_batches = []
    
    for i in range(0, len(points_data), batch_size):
        batch_points = points_data[i:i+batch_size]
        batch_pvalues = pvalues.iloc[i:i+batch_size]
        batch_log2fc = log2fc.iloc[i:i+batch_size]
        
        non_sig_pm = PMobject()
        high_lfc_non_sig_pm = PMobject()
        high_lfc_sig_pm = PMobject()
        low_lfc_sig_pm = PMobject()
        
        for j, point in enumerate(batch_points):
            coords = plane.c2p(*point)
            if batch_pvalues.iloc[j] >= pval_threshold and abs(batch_log2fc.iloc[j]) < lfc_threshold:
                non_sig_pm.add_points([coords], color=GRAY)
            elif abs(batch_log2fc.iloc[j]) >= lfc_threshold and batch_pvalues.iloc[j] > pval_threshold:
                high_lfc_non_sig_pm.add_points([coords], color=YELLOW)
            elif abs(batch_log2fc.iloc[j]) >= lfc_threshold and batch_pvalues.iloc[j] <= pval_threshold:
                high_lfc_sig_pm.add_points([coords], color=RED)
            elif abs(batch_log2fc.iloc[j]) < lfc_threshold and batch_pvalues.iloc[j] <= pval_threshold:
                low_lfc_sig_pm.add_points([coords], color=GREEN)
        
        non_sig_batches.append(non_sig_pm)
        high_lfc_non_sig_batches.append(high_lfc_non_sig_pm)
        high_lfc_sig_batches.append(high_lfc_sig_pm)
        low_lfc_sig_batches.append(low_lfc_sig_pm)
    
    return non_sig_batches, high_lfc_non_sig_batches, high_lfc_sig_batches, low_lfc_sig_batches

def plot_w_VGroup(df, plane, pval_threshold=0.05, lfc_threshold=1.0):
    # # Create points in a vectorized way
    points_data = np.array([[row['log2FoldChange'], row['-log10pval'], 0] for _, row in df.iterrows()])
    is_significant = (df['pvalue'] < pval_threshold) & (abs(df['log2FoldChange']) > lfc_threshold)
    # Use PMobject for much faster rendering
    non_sig_points = VGroup()
    sig_points = VGroup()
    for i, point in enumerate(points_data):
        coords = plane.c2p(*point)
        if is_significant.iloc[i]:
            sig_points.add(Dot(coords, color=RED))
        else:
            non_sig_points.add(Dot(coords, color=BLUE))
    
    return non_sig_points, sig_points


class EnhancedVolcano(Scene):
    def __init__(self, data_file, output_file, resolution, 
                 pval_threshold=0.05, lfc_threshold=1.0, highlight_genes=""):
        self.data_file = data_file
        self.output_file = output_file
        self.resolution = resolution
        self.pval_threshold = pval_threshold
        self.lfc_threshold = lfc_threshold
        self.highlight_genes = highlight_genes
        super().__init__()
    
    def construct(self):
        self.renderer.file_writer.output_filename = self.output_file
        self.renderer.file_writer.resolution = self.resolution
        self.renderer.file_writer.disable_caching = True
        df = pd.read_csv(self.data_file, sep="\t" if self.data_file.endswith(".tsv") else ",")
        df = df.dropna()  # Remove rows with NA values
        df['-log10pval'] = -np.log10(df['pvalue'])
        
        # Get the 10th highest -log10(pvalue)
        top_10_pvals = df['-log10pval'].nlargest(10)
        max_y_value = top_10_pvals.iloc[-1]
        
        # Cap -log10(pvalue) values at max_y_value
        df['-log10pval'] = df['-log10pval'].clip(upper=max_y_value)
        
        plane = NumberPlane(
            x_range = (-4, 4),
            y_range = (0, max_y_value, 10),
            x_length = 10,
            y_length = 6,
            axis_config={"include_numbers": True},
            y_axis_config={"numbers_to_exclude": [-2], "include_tip": False, 
                           #"numbers_to_include": [0, max_y_value], 
                           "decimal_number_config": {"num_decimal_places": 0}, 
                           "unit_size": 0.5, "include_numbers": False, 
                           "label_direction": LEFT, "stroke_opacity": 0},
             background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.3
            }
        )
        plane.shift(LEFT)
        #plane.center()
        # Create a new y-axis line and position it at the leftmost point
        new_y_axis = Line(
            start=plane.coords_to_point(-4, 0),
            end=plane.coords_to_point(-4, max_y_value),
            color=WHITE
        )
        # Add numbers to the new y-axis
        y_axis_numbers = VGroup()
        for y in range(0, int(max_y_value) + 1, 10):
            y_label = Text(str(y), font_size=24).next_to(plane.coords_to_point(-4, y), LEFT, buff=0.1)
            y_axis_numbers.add(y_label)
        #new_y_axis.add_numbers(direction=LEFT)
        y_axis_label = Tex("\\text{-log10(p-value)}").scale(0.65).rotate(90 * DEGREES).next_to(new_y_axis, LEFT*1.2, buff=0.4)

        #y_axis_shift = plane.coords_to_point(-4, max_y_value/2) - plane.y_axis.get_center()
        #plane.y_axis.shift(y_axis_shift)
        #plane.y_axis.move_to(plane.coords_to_point(-4, max_y_value/2))
        plane.x_axis.add_numbers([0])
        y_label = plane.get_y_axis_label(Tex("\\text{Voltage [V]}").scale(0.65).rotate(90 * DEGREES),
                                         edge=LEFT, direction=LEFT, buff=0.4)
        x_label = plane.get_x_axis_label("\\text{Log2FC}", edge=DOWN, direction=DOWN, buff=0.4)


        self.play(Create(plane), Create(new_y_axis), Create(y_axis_label), 
                  Create(y_axis_numbers), Write(x_label))
        legend = create_legend(plane)
        self.play(FadeIn(legend))
        #non_sig_points, sig_points = plot_w_PMobject_batch(df, plane, self.pval_threshold, self.lfc_threshold)  
        # Use LaggedStart for animating points
        #self.play(LaggedStart(*[FadeIn(p) for p in non_sig_points], lag_ratio=0.01))
        non_sig_batches, high_lfc_non_sig_batches, high_lfc_sig_batches, low_lfc_sig_batches = plot_w_PMobject_batch(df, plane, self.pval_threshold, self.lfc_threshold)  
        # Use LaggedStart for animating points
        self.play(LaggedStart(*[FadeIn(p) for p in non_sig_batches], lag_ratio=0.017))

        for batch in high_lfc_non_sig_batches:
            self.play(FadeIn(batch), run_time=0.017)
        for batch in low_lfc_sig_batches:
            self.play(FadeIn(batch), run_time=0.017)   
        for batch in high_lfc_sig_batches:
            self.play(FadeIn(batch), run_time=0.22)
        # 'MT2A,ADAMTS1,FGD4'
        #highlight_genes = 'MT2A,ADAMTS1,FGD4'
        draw_gene_dots(df, self.highlight_genes, plane, self)
        
        self.wait(2)
        
        

def generate_volcano_plot(input_file, output_file, 
                          resolution, pval_threshold=0.05, 
                          lfc_threshold=1.0, highlight_genes=""):
    scene = EnhancedVolcano(input_file, output_file, 
                            resolution, pval_threshold, 
                            lfc_threshold, highlight_genes)
    scene.render()