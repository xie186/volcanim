from manim import *

def create_legend(plane):
    buff_var = 0.3
    dot_notsig = Dot(color=GRAY, radius=0.05).next_to(plane, UP, buff=buff_var)
    dot_notsig.shift(4*LEFT) 
    label_nosig = Text("Non-significant", font_size=24).scale(0.65).\
                rotate(0 * DEGREES).next_to(dot_notsig, RIGHT*1.2, buff=0.1)
    dot_high_lfc_non_sig = Dot(color=YELLOW, radius=0.05).\
                next_to(plane, UP, buff=buff_var + 0.2)
    dot_high_lfc_non_sig.shift(4*LEFT)
    label_high_lfc_non_sig = Text("Log2FC", font_size=24).scale(0.65).\
                rotate(0 * DEGREES).next_to(dot_high_lfc_non_sig, RIGHT, buff=0.1)
    dot_high_lfc_sig = Dot(color=RED, radius=0.05).next_to(plane, UP, buff=buff_var)
    label_high_lfc_sig = Text("p_val & Log2FC", font_size=24).scale(0.65).\
                rotate(0 * DEGREES).next_to(dot_high_lfc_sig, RIGHT, buff=0.1)
    dot_low_lfc_sig = Dot(color=GREEN, radius=0.05).next_to(plane, UP, buff=buff_var + 0.2)
    label_low_lfc_sig = Text("p_val", font_size=24).scale(0.65).\
                rotate(0 * DEGREES).next_to(dot_low_lfc_sig, RIGHT, buff=0.1)
    
    legend = VGroup(
        dot_notsig, label_nosig, dot_high_lfc_non_sig, label_high_lfc_non_sig,
        dot_high_lfc_sig, label_high_lfc_sig, dot_low_lfc_sig, label_low_lfc_sig
    )
    return legend