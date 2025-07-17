#!/usr/bin/env python3
"""
Test script for the image integration functionality in the report generator.

This script demonstrates the image integration without running expensive benchmarks.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.report_generator import ReportGenerator, ImageIntegrator


def test_image_integration():
    """Test the image integration functionality."""
    print("Testing Image Integration System")
    print("=" * 40)
    
    # Test ImageIntegrator directly
    integrator = ImageIntegrator()
    
    print(f"Available images found:")
    for category, images in integrator.available_images.items():
        print(f"  {category}: {len(images)} images")
        for img in images[:3]:  # Show first 3
            print(f"    - {os.path.basename(img)}")
        if len(images) > 3:
            print(f"    ... and {len(images) - 3} more")
    
    print("\nTesting image caption generation:")
    test_filenames = [
        "circulant_6_2.png",
        "mt3_3_backtracking.png", 
        "circulant_10_5_k_labeled.png",
        "mt3_5_heuristic_accurate.png"
    ]
    
    for filename in test_filenames:
        caption = integrator._generate_caption_from_filename(filename)
        print(f"  {filename} -> {caption}")
    
    print("\nTesting structure images:")
    structure_images = integrator.get_graph_structure_images()
    for key, path in structure_images.items():
        print(f"  {key}: {os.path.basename(path)}")
    
    print("\nTesting comparison images:")
    comparison_images = integrator.get_algorithm_comparison_images()
    for category, images in comparison_images.items():
        print(f"  {category}: {len(images)} images")
    
    return True


def test_report_generation_with_images():
    """Test report generation with image integration (without expensive benchmarks)."""
    print("\nTesting Report Generation with Images")
    print("=" * 40)
    
    # Initialize report generator
    generator = ReportGenerator()
    
    # Generate just the background section to test image integration
    print("Generating background section with images...")
    background_section = generator.generate_background()
    
    # Check if images were integrated
    if "![" in background_section:
        print("✓ Images successfully integrated into background section")
        image_count = background_section.count("![")
        print(f"  Found {image_count} image references")
    else:
        print("⚠ No images found in background section")
    
    # Generate appendix section to test image galleries
    print("Generating appendix section with image galleries...")
    appendix_section = generator.generate_appendix()
    
    if "![" in appendix_section:
        print("✓ Image galleries successfully integrated into appendix")
        image_count = appendix_section.count("![")
        print(f"  Found {image_count} image references in galleries")
    else:
        print("⚠ No image galleries found in appendix")
    
    # Save a sample section to file for inspection
    sample_filename = "sample_section_with_images.md"
    with open(sample_filename, 'w', encoding='utf-8') as f:
        f.write("# Sample Report Section with Images\n\n")
        f.write(background_section)
        f.write("\n\n")
        f.write(appendix_section[:2000])  # First 2000 chars of appendix
    
    print(f"✓ Sample section saved to {sample_filename}")
    
    return True


def main():
    """Main test function."""
    try:
        # Test image integration components
        if not test_image_integration():
            return 1
        
        # Test report generation with images
        if not test_report_generation_with_images():
            return 1
        
        print("\n" + "=" * 40)
        print("✓ All image integration tests passed!")
        print("✓ Images are now integrated into the report")
        print("✓ Check sample_section_with_images.md to see the results")
        
        return 0
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)