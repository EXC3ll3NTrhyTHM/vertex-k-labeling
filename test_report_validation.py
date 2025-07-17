#!/usr/bin/env python3
"""
Test script for the report validation and output system.

This script demonstrates the complete report generation process with validation,
proper file organization, and generation summary.
"""

import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.report_generator import ReportGenerator


def main():
    """Test the complete report generation with validation system."""
    print("Testing K-Labeling Report Generation with Validation System")
    print("=" * 60)
    
    # Initialize report generator
    generator = ReportGenerator()
    
    # Generate complete report with validation
    try:
        output_results = generator.generate_complete_report_with_validation(
            filename="k_labeling_algorithms_report.md"
        )
        
        # Check if generation was successful
        if output_results['generation_successful']:
            print("\n✓ Report generation completed successfully!")
            print(f"✓ Main report: {output_results['main_report_file']}")
            print(f"✓ Validation report: {output_results['validation_report_file']}")
            print(f"✓ Summary: {output_results['summary_file']}")
            
            # Display validation summary
            validation = output_results['validation_results']
            print(f"\nValidation Summary:")
            print(f"  - Valid: {'Yes' if validation['is_valid'] else 'No'}")
            print(f"  - Errors: {len(validation['errors'])}")
            print(f"  - Sections: {validation['section_completeness']['completeness_score']:.1%} complete")
            
            return 0
        else:
            print("\n✗ Report generation failed!")
            if 'error' in output_results:
                print(f"Error: {output_results['error']}")
            return 1
            
    except Exception as e:
        print(f"\n✗ Unexpected error during report generation: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)