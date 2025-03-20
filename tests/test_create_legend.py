import os
import sys
import pytest
from manim import *
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from volcanim.legend import create_legend

def test_create_legend():
    # Create a NumberPlane for the legend
    plane = NumberPlane(
        x_range=(-4, 4),
        y_range=(0, 10),
        x_length=10,
        y_length=6,
        axis_config={"include_numbers": True},
        y_axis_config={"include_tip": False, "decimal_number_config": {"num_decimal_places": 0}}
    )
    
    # Call the create_legend function
    legend = create_legend(plane)
    
    # Check if the legend is a VGroup
    assert isinstance(legend, VGroup), "Legend should be a VGroup"
    
    # Check if the legend contains the correct number of elements (8 elements: 4 dots and 4 labels)
    assert len(legend) == 8, "Legend should contain 8 elements (4 dots and 4 labels)"
    
    # Check if the elements in the legend are of the correct type
    for i in range(0, len(legend), 2):
        assert isinstance(legend[i], Dot), f"Element {i} should be a Dot"
        assert isinstance(legend[i+1], Text), f"Element {i+1} should be a Text"

    # Check the colors of the dots
    assert legend[0].color == GRAY, "First dot should be gray (Non-significant)"
    assert legend[2].color == YELLOW, "Second dot should be yellow (Log2FC)"
    assert legend[4].color == RED, "Third dot should be red (p_val & Log2FC)"
    assert legend[6].color == GREEN, "Fourth dot should be green (p_val)"

    # Check the labels of the legend
    assert legend[1].text == "Non-significant", "First label should be 'Non-significant'"
    assert legend[3].text == "Log2FC", "Second label should be 'Log2FC'"
    assert legend[5].text == "p_val&Log2FC", "Third label should be 'p_val & Log2FC'"
    assert legend[7].text == "p_val", "Fourth label should be 'p_val'"

# Run the test
if __name__ == "__main__":
    pytest.main()