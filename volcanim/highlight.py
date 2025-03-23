from manim import *

def homotopy(x, y, z, t):
    if t <= 0.25:
        progress = t / 0.25
        return (x, y + progress * 0.2 * np.sin(x), z)
    else:
        wave_progress = (t - 0.25) / 0.75
        return (x, y + 0.2 * np.sin(x + 10 * wave_progress), z)        
    
# Reference:
# https://stackoverflow.com/questions/76241182/in-manim-how-can-i-combine-fadein-and-fadeout-in-one-animation
def highlight_text(gene_name, dot):
    txt_3_start = MathTex(
                gene_name,
                color=WHITE,
                font_size = 16,
            ).set_opacity(1).next_to(dot, RIGHT, buff=0.1)
            
    txt_3_middle = MathTex(
                gene_name,
                color=GREEN,
                #stroke_width = f_z_stroke_width,
                font_size= 1 * 1.5,
            ).shift(RIGHT).set_opacity(1)
            
    txt_3_end = MathTex(
                gene_name,
                color=BLUE,
                font_size= 1 * 1.5 * 1.5,
            ).shift(2*RIGHT).set_opacity(1)
    return txt_3_start, txt_3_middle, txt_3_end

def repel_labels(labels, arrows, min_distance=0.5):
    for i, label1 in enumerate(labels):
        for j, label2 in enumerate(labels):
            if i != j:
                while np.linalg.norm(label1.get_center() - label2.get_center()) < min_distance:
                    direction = label1.get_center() - label2.get_center()
                    direction = direction / np.linalg.norm(direction)
                    label1.shift(direction * 0.1)
                    label2.shift(-direction * 0.1)
    # Update arrows
    for arrow, label in zip(arrows, labels):
        arrow.put_start_and_end_on(arrow.get_start(), label.get_left())


def draw_gene_dots(df, gene_list, plane, scene):
    if not gene_list:
        return # exit the function if no genes are provided
    gene_names = gene_list.split(",")
    labels = []
    arrows = []
    for gene_name in gene_names:
        gene_data = df[df['gene_id'] == gene_name].iloc[0]
        log2fc = gene_data['log2FoldChange']
        log10pval = gene_data['-log10pval']
        coords = plane.c2p(log2fc, log10pval)
        
        dot = Dot(coords, color=WHITE)
        txt_3_start, txt_3_middle, txt_3_end = highlight_text(gene_name, dot)
        
        # Position the text next to the dot
        txt_3_start.next_to(dot, RIGHT, buff=0.1)
        txt_3_middle.next_to(dot, RIGHT, buff=0.1)
        txt_3_end.next_to(dot, RIGHT, buff=0.1)
        
        # Add the dot and text to the scene
        scene.add(dot, txt_3_start, txt_3_middle, txt_3_end)
        labels.append(txt_3_start)
        # Create an arrow connecting the dot and the text
        arrow = Arrow(start=dot.get_right(), end=txt_3_start.get_left(), buff=0.1, color=WHITE)
        arrows.append(arrow)
        scene.add(arrow)
        # Animate the text
        scene.play(FadeIn(dot), FadeIn(txt_3_start), FadeIn(arrow))
    # Apply repel effect to labels
    repel_labels(labels, arrows)
        