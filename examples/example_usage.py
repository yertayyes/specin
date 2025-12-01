#!/usr/bin/env python3
"""
Example Usage of Spectral Signature Tools
==========================================
Demonstrates how to use the spectral signature collection tools
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))

from spectral_signature_loader import SpectralSignatureLoader
from signature_creator import create_signature_from_array
from signature_comparison import compare_signatures, plot_multiple_signatures
from signature_validator import SignatureValidator
from signature_plotter import plot_signature, plot_gold_pathfinders
import numpy as np


def example_create_signature():
    """Example: Create a new signature"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Creating a New Signature")
    print("="*60)
    
    # Simulate high gold potential signature
    # High values in phyllic (band 13) and composite (band 16)
    reflectance_values = np.array([
        0.234, 0.312, 0.289, 0.267, 0.245, 0.223,  # Raw SWIR (1-6)
        0.189, 0.245, 0.201, 0.178, 0.156, 0.134,  # CR SWIR (7-12)
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0              # Placeholder for indices
    ])
    
    index_values = np.array([
        0, 0, 0, 0, 0, 0,  # No indices for raw bands
        0, 0, 0, 0, 0, 0,  # No indices for CR bands
        220, 180, 150, 250, 170, 140  # Gold pathfinder indices (13-18)
    ])
    
    signature = create_signature_from_array(
        band_values=reflectance_values,
        signature_id="example_high_gold_001",
        category="gold_exploration",
        location={
            "latitude": 48.75,
            "longitude": 82.15,
            "utm_zone": "44N"
        },
        source={
            "sensor": "ASTER",
            "scene_id": "AST_07_00405302002053830",
            "acquisition_date": "2002-05-02",
            "extraction_method": "SCP_ROI"
        },
        index_values=index_values,
        metadata={
            "notes": "Example high gold potential signature",
            "created_by": "example_script"
        }
    )
    
    print(f"Created signature: {signature.signature_id}")
    print(f"Category: {signature.category}")
    print(f"Band 13 (Phyllic): {signature.get_index_value(13)}")
    print(f"Band 16 (Composite): {signature.get_index_value(16)}")
    
    # Save example
    output_dir = Path(__file__).parent.parent / "examples"
    output_dir.mkdir(exist_ok=True)
    signature.save_csv(output_dir / "example_high_gold_001.csv")
    signature.save_json(output_dir / "example_high_gold_001.json")
    print(f"\nSaved to: {output_dir}/")
    
    return signature


def example_load_signature():
    """Example: Load an existing signature"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Loading a Signature")
    print("="*60)
    
    loader = SpectralSignatureLoader()
    
    # Try to load the example we just created
    example_file = Path(__file__).parent / "example_high_gold_001.csv"
    
    if example_file.exists():
        signature = loader.load_csv(example_file)
        print(f"Loaded signature: {signature.signature_id}")
        print(f"Category: {signature.category}")
        print(f"Location: {signature.location}")
        print(f"\nBand values:")
        for i in [1, 2, 13, 16]:
            val = signature.get_band_value(i) or signature.get_index_value(i)
            band_name = signature.get_band_by_name(f"Band_{i}") or {}
            print(f"  Band {i} ({band_name.get('band_name', 'N/A')}): {val}")
        
        return signature
    else:
        print(f"Example file not found: {example_file}")
        print("Run example_create_signature() first")
        return None


def example_compare_signatures():
    """Example: Compare two signatures"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Comparing Signatures")
    print("="*60)
    
    # Create two example signatures
    loader = SpectralSignatureLoader()
    
    # High gold signature
    high_gold_values = np.array([0.234] * 12 + [0, 0, 0, 0, 0, 0])
    high_gold_indices = np.array([0] * 12 + [220, 180, 150, 250, 170, 140])
    
    sig1 = create_signature_from_array(
        band_values=high_gold_values,
        signature_id="high_gold_example",
        category="gold_exploration",
        index_values=high_gold_indices
    )
    
    # Background signature
    background_values = np.array([0.156] * 12 + [0, 0, 0, 0, 0, 0])
    background_indices = np.array([0] * 12 + [45, 35, 40, 50, 30, 25])
    
    sig2 = create_signature_from_array(
        band_values=background_values,
        signature_id="background_example",
        category="background",
        index_values=background_indices
    )
    
    # Compare focusing on gold pathfinders
    comparison = compare_signatures(sig1, sig2, focus_bands=[13, 14, 15, 16, 17, 18])
    
    print(f"Euclidean Distance: {comparison['euclidean_distance']:.3f}")
    print(f"Correlation: {comparison['correlation']:.3f}")
    print(f"Separability: {comparison['separability']:.3f}")
    print(f"\nKey Differences:")
    for diff in comparison['key_differences']:
        print(f"  {diff['band_name']}: {diff['value1']:.1f} vs {diff['value2']:.1f} "
              f"(diff: {diff['difference']:.1f})")


def example_validate_signature():
    """Example: Validate a signature"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Validating a Signature")
    print("="*60)
    
    # Create example signature
    sig = example_create_signature()
    
    validator = SignatureValidator()
    is_valid, errors = validator.validate_signature(sig)
    
    if is_valid:
        print("✅ Signature is VALID")
    else:
        print("❌ Signature is INVALID")
        print("Errors:")
        for error in errors:
            print(f"  - {error}")
    
    # Check quality
    quality = validator.check_quality(sig)
    print(f"\nQuality Metrics:")
    print(f"  Has location: {quality['has_location']}")
    print(f"  Has source: {quality['has_source']}")
    print(f"  Has statistics: {quality['has_statistics']}")
    print(f"  Has continuum removed: {quality['has_continuum_removed']}")
    print(f"  Has index values: {quality['has_index_values']}")
    print(f"  Data completeness: {quality['data_completeness']:.1%}")


def example_plot_signature():
    """Example: Plot a signature"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Plotting a Signature")
    print("="*60)
    
    sig = example_create_signature()
    
    output_dir = Path(__file__).parent
    output_dir.mkdir(exist_ok=True)
    
    # Plot reflectance
    plot_signature(
        sig,
        value_type='reflectance',
        show_indices=True,
        save_path=str(output_dir / "example_signature_reflectance.png")
    )
    
    # Plot gold pathfinders
    sig2 = example_create_signature()
    sig2.signature_id = "background_example"
    # Modify to create background signature
    for band in sig2.bands:
        if band['band_number'] >= 13:
            band['index_value'] = band.get('index_value', 0) * 0.2
    
    plot_gold_pathfinders(
        [sig, sig2],
        labels=['High Gold', 'Background'],
        save_path=str(output_dir / "example_gold_pathfinders.png")
    )
    
    print(f"\nPlots saved to: {output_dir}/")


def main():
    """Run all examples"""
    print("\n" + "="*60)
    print("SPECTRAL SIGNATURE COLLECTION - EXAMPLES")
    print("="*60)
    
    try:
        example_create_signature()
        example_load_signature()
        example_compare_signatures()
        example_validate_signature()
        example_plot_signature()
        
        print("\n" + "="*60)
        print("✅ All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

