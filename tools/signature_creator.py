#!/usr/bin/env python3
"""
Spectral Signature Creator
===========================
Create spectral signatures from various input formats
"""

import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

from spectral_signature_loader import SpectralSignature, SpectralSignatureLoader


def create_signature_from_array(
    band_values: np.ndarray,
    signature_id: str,
    category: str,
    location: Optional[Dict] = None,
    source: Optional[Dict] = None,
    continuum_removed: Optional[np.ndarray] = None,
    index_values: Optional[np.ndarray] = None,
    metadata: Optional[Dict] = None
) -> SpectralSignature:
    """Create a spectral signature from numpy array of band values
    
    Args:
        band_values: Array of reflectance values (18 bands expected)
        signature_id: Unique identifier for the signature
        category: Category (e.g., 'gold_exploration', 'minerals', 'background')
        location: Dictionary with location info (lat, lon, utm_zone, etc.)
        source: Dictionary with source info (sensor, scene_id, acquisition_date, etc.)
        continuum_removed: Optional array of continuum-removed values
        index_values: Optional array of index values (for bands 13-18)
        metadata: Additional metadata dictionary
    
    Returns:
        SpectralSignature object
    """
    loader = SpectralSignatureLoader()
    
    if len(band_values) != 18:
        raise ValueError(f"Expected 18 bands, got {len(band_values)}")
    
    bands = []
    for i, band_def in enumerate(loader.ASTER_BANDS):
        band_data = {
            'band_number': band_def['band_number'],
            'band_name': band_def['band_name'],
            'wavelength_um': band_def.get('wavelength_um'),
            'reflectance_value': float(band_values[i]),
            'continuum_removed': float(continuum_removed[i]) if continuum_removed is not None and i < len(continuum_removed) else None,
            'index_value': float(index_values[i]) if index_values is not None and i < len(index_values) else None,
            'notes': ''
        }
        bands.append(band_data)
    
    # Calculate statistics
    reflectance_values = [b['reflectance_value'] for b in bands if b['reflectance_value'] is not None]
    statistics = {}
    if reflectance_values:
        statistics = {
            'mean_reflectance': float(np.mean(reflectance_values)),
            'std_reflectance': float(np.std(reflectance_values)),
            'min_reflectance': float(np.min(reflectance_values)),
            'max_reflectance': float(np.max(reflectance_values))
        }
    
    # Add creation metadata
    if metadata is None:
        metadata = {}
    metadata['created_date'] = datetime.now().strftime('%Y-%m-%d')
    metadata['created_by'] = metadata.get('created_by', 'unknown')
    
    return SpectralSignature(
        signature_id=signature_id,
        category=category,
        bands=bands,
        location=location or {},
        source=source or {},
        statistics=statistics,
        metadata=metadata
    )


def create_signature_from_scp_export(
    scp_filepath: Union[str, Path],
    signature_id: str,
    category: str,
    location: Optional[Dict] = None,
    source: Optional[Dict] = None
) -> SpectralSignature:
    """Create signature from SCP (QGIS) exported file
    
    Args:
        scp_filepath: Path to SCP exported signature file
        signature_id: Unique identifier for the signature
        category: Category classification
        location: Location metadata
        source: Source metadata
    
    Returns:
        SpectralSignature object
    """
    scp_filepath = Path(scp_filepath)
    
    # SCP exports can be CSV or TXT format
    # This is a basic implementation - may need adjustment based on actual SCP format
    if scp_filepath.suffix.lower() == '.csv':
        loader = SpectralSignatureLoader()
        signature = loader.load_csv(scp_filepath)
        signature.signature_id = signature_id
        signature.category = category
        if location:
            signature.location = location
        if source:
            signature.source = source
        return signature
    else:
        raise ValueError(f"Unsupported SCP export format: {scp_filepath.suffix}")


def create_signature_from_qgis_pixel(
    band_values: List[float],
    pixel_coords: Dict,
    signature_id: str,
    category: str,
    source: Optional[Dict] = None
) -> SpectralSignature:
    """Create signature from QGIS pixel values
    
    Args:
        band_values: List of 18 band values from QGIS Identify tool
        pixel_coords: Dictionary with 'x' and 'y' coordinates (or lat/lon)
        signature_id: Unique identifier
        category: Category classification
        source: Source metadata
    
    Returns:
        SpectralSignature object
    """
    band_array = np.array(band_values)
    
    location = {
        'pixel_x': pixel_coords.get('x'),
        'pixel_y': pixel_coords.get('y'),
        'latitude': pixel_coords.get('latitude'),
        'longitude': pixel_coords.get('longitude')
    }
    
    return create_signature_from_array(
        band_values=band_array,
        signature_id=signature_id,
        category=category,
        location=location,
        source=source
    )


def create_signature_template(
    signature_id: str,
    category: str,
    output_dir: Union[str, Path],
    location: Optional[Dict] = None,
    source: Optional[Dict] = None
) -> SpectralSignature:
    """Create an empty signature template for manual filling
    
    Args:
        signature_id: Unique identifier
        category: Category classification
        output_dir: Directory to save template
        location: Location metadata template
        source: Source metadata template
    
    Returns:
        Empty SpectralSignature with default values
    """
    # Create array of zeros for template
    band_values = np.zeros(18)
    
    signature = create_signature_from_array(
        band_values=band_values,
        signature_id=signature_id,
        category=category,
        location=location or {},
        source=source or {}
    )
    
    # Save template
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    signature.save_csv(output_dir / f"{signature_id}.csv")
    signature.save_json(output_dir / f"{signature_id}.json")
    
    return signature


if __name__ == "__main__":
    # Example usage
    print("Spectral Signature Creator")
    print("=" * 50)
    
    # Example: Create from array
    example_values = np.random.rand(18) * 0.3 + 0.1  # Random values between 0.1-0.4
    example_index_values = np.array([0] * 12 + [150, 120, 100, 180, 110, 90])  # Example gold indices
    
    signature = create_signature_from_array(
        band_values=example_values,
        signature_id="example_signature_001",
        category="gold_exploration",
        location={
            'latitude': 48.75,
            'longitude': 82.15,
            'utm_zone': '44N'
        },
        source={
            'sensor': 'ASTER',
            'scene_id': 'AST_07_00405302002053830',
            'acquisition_date': '2002-05-02'
        },
        index_values=example_index_values,
        metadata={'notes': 'Example signature for testing'}
    )
    
    print(f"Created signature: {signature.signature_id}")
    print(f"Category: {signature.category}")
    print(f"Band 13 (Phyllic): {signature.get_index_value(13)}")
    print(f"Band 16 (Composite): {signature.get_index_value(16)}")
    
    # Save example
    output_dir = Path("examples")
    output_dir.mkdir(exist_ok=True)
    signature.save_csv(output_dir / "example_signature_001.csv")
    signature.save_json(output_dir / "example_signature_001.json")
    print(f"\nSaved to: {output_dir}/")

