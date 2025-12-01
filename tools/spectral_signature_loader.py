#!/usr/bin/env python3
"""
Spectral Signature Loader
=========================
Load spectral signatures from CSV or JSON files
"""

import csv
import json
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Union


class SpectralSignature:
    """Represents a spectral signature with metadata"""
    
    def __init__(self, signature_id: str, category: str, bands: List[Dict], 
                 location: Optional[Dict] = None, source: Optional[Dict] = None,
                 statistics: Optional[Dict] = None, metadata: Optional[Dict] = None):
        self.signature_id = signature_id
        self.category = category
        self.bands = bands
        self.location = location or {}
        self.source = source or {}
        self.statistics = statistics or {}
        self.metadata = metadata or {}
    
    def get_band_value(self, band_number: int) -> Optional[float]:
        """Get reflectance value for a specific band number"""
        for band in self.bands:
            if band.get('band_number') == band_number:
                return band.get('reflectance_value')
        return None
    
    def get_band_by_name(self, band_name: str) -> Optional[Dict]:
        """Get band data by band name"""
        for band in self.bands:
            if band.get('band_name') == band_name:
                return band
        return None
    
    def get_index_value(self, band_number: int) -> Optional[float]:
        """Get index value for gold pathfinder bands (13-18)"""
        for band in self.bands:
            if band.get('band_number') == band_number:
                return band.get('index_value')
        return None
    
    def get_all_values(self, value_type: str = 'reflectance') -> np.ndarray:
        """Get all band values as numpy array
        
        Args:
            value_type: 'reflectance', 'continuum_removed', or 'index'
        """
        values = []
        for band in sorted(self.bands, key=lambda x: x.get('band_number', 0)):
            if value_type == 'reflectance':
                values.append(band.get('reflectance_value', 0.0))
            elif value_type == 'continuum_removed':
                values.append(band.get('continuum_removed', 0.0))
            elif value_type == 'index':
                values.append(band.get('index_value', 0.0))
            else:
                values.append(band.get('reflectance_value', 0.0))
        return np.array(values)
    
    def get_wavelengths(self) -> np.ndarray:
        """Get all wavelengths as numpy array"""
        wavelengths = []
        for band in sorted(self.bands, key=lambda x: x.get('band_number', 0)):
            wavelengths.append(band.get('wavelength_um', 0.0))
        return np.array(wavelengths)
    
    def to_dict(self) -> Dict:
        """Convert signature to dictionary"""
        return {
            'signature_id': self.signature_id,
            'category': self.category,
            'location': self.location,
            'source': self.source,
            'bands': self.bands,
            'statistics': self.statistics,
            'metadata': self.metadata
        }
    
    def save_csv(self, filepath: Union[str, Path]):
        """Save signature to CSV file"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', newline='') as f:
            fieldnames = ['band_number', 'band_name', 'wavelength_um', 
                          'reflectance_value', 'continuum_removed', 'index_value', 'notes']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for band in sorted(self.bands, key=lambda x: x.get('band_number', 0)):
                writer.writerow({
                    'band_number': band.get('band_number', ''),
                    'band_name': band.get('band_name', ''),
                    'wavelength_um': band.get('wavelength_um', ''),
                    'reflectance_value': band.get('reflectance_value', ''),
                    'continuum_removed': band.get('continuum_removed', ''),
                    'index_value': band.get('index_value', ''),
                    'notes': band.get('notes', '')
                })
    
    def save_json(self, filepath: Union[str, Path]):
        """Save signature to JSON file"""
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


class SpectralSignatureLoader:
    """Loader for spectral signature files"""
    
    # Standard ASTER band definitions
    ASTER_BANDS = [
        {'band_number': 1, 'band_name': 'ASTER_B04_1.66um_Clay_Carbonate', 'wavelength_um': 1.656},
        {'band_number': 2, 'band_name': 'ASTER_B05_2.17um_AlOH_Sericite', 'wavelength_um': 2.167},
        {'band_number': 3, 'band_name': 'ASTER_B06_2.21um_AlOH_Muscovite', 'wavelength_um': 2.209},
        {'band_number': 4, 'band_name': 'ASTER_B07_2.26um_MgOH_Chlorite', 'wavelength_um': 2.262},
        {'band_number': 5, 'band_name': 'ASTER_B08_2.34um_Carbonate', 'wavelength_um': 2.336},
        {'band_number': 6, 'band_name': 'ASTER_B09_2.40um_Carbonate_Chlorite', 'wavelength_um': 2.400},
        # Continuum removed bands (7-12)
        {'band_number': 7, 'band_name': 'CR_ASTER_B04_1.66um_Clay_Carbonate', 'wavelength_um': 1.656},
        {'band_number': 8, 'band_name': 'CR_ASTER_B05_2.17um_AlOH_Sericite', 'wavelength_um': 2.167},
        {'band_number': 9, 'band_name': 'CR_ASTER_B06_2.21um_AlOH_Muscovite', 'wavelength_um': 2.209},
        {'band_number': 10, 'band_name': 'CR_ASTER_B07_2.26um_MgOH_Chlorite', 'wavelength_um': 2.262},
        {'band_number': 11, 'band_name': 'CR_ASTER_B08_2.34um_Carbonate', 'wavelength_um': 2.336},
        {'band_number': 12, 'band_name': 'CR_ASTER_B09_2.40um_Carbonate_Chlorite', 'wavelength_um': 2.400},
        # Gold pathfinder indices (13-18)
        {'band_number': 13, 'band_name': 'Gold_Phyllic_Sericite', 'wavelength_um': None},
        {'band_number': 14, 'band_name': 'Gold_Argillic_Kaolinite', 'wavelength_um': None},
        {'band_number': 15, 'band_name': 'Gold_Propylitic_Chlorite', 'wavelength_um': None},
        {'band_number': 16, 'band_name': 'Gold_Composite_Best', 'wavelength_um': None},
        {'band_number': 17, 'band_name': 'Gold_Hydrothermal_Intensity', 'wavelength_um': None},
        {'band_number': 18, 'band_name': 'Gold_Advanced_Argillic', 'wavelength_um': None},
    ]
    
    def load_csv(self, filepath: Union[str, Path]) -> SpectralSignature:
        """Load signature from CSV file"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Signature file not found: {filepath}")
        
        bands = []
        signature_id = filepath.stem
        category = filepath.parent.name
        
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                band_data = {
                    'band_number': int(row.get('band_number', 0)),
                    'band_name': row.get('band_name', ''),
                    'wavelength_um': float(row.get('wavelength_um', 0)) if row.get('wavelength_um') else None,
                    'reflectance_value': float(row.get('reflectance_value', 0)) if row.get('reflectance_value') else 0.0,
                    'continuum_removed': float(row.get('continuum_removed', 0)) if row.get('continuum_removed') else None,
                    'index_value': float(row.get('index_value', 0)) if row.get('index_value') else None,
                    'notes': row.get('notes', '')
                }
                bands.append(band_data)
        
        # Calculate statistics
        reflectance_values = [b['reflectance_value'] for b in bands if b['reflectance_value']]
        statistics = {}
        if reflectance_values:
            statistics = {
                'mean_reflectance': np.mean(reflectance_values),
                'std_reflectance': np.std(reflectance_values),
                'min_reflectance': np.min(reflectance_values),
                'max_reflectance': np.max(reflectance_values)
            }
        
        return SpectralSignature(
            signature_id=signature_id,
            category=category,
            bands=bands,
            statistics=statistics
        )
    
    def load_json(self, filepath: Union[str, Path]) -> SpectralSignature:
        """Load signature from JSON file"""
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"Signature file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return SpectralSignature(
            signature_id=data.get('signature_id', filepath.stem),
            category=data.get('category', 'unknown'),
            bands=data.get('bands', []),
            location=data.get('location', {}),
            source=data.get('source', {}),
            statistics=data.get('statistics', {}),
            metadata=data.get('metadata', {})
        )
    
    def load_all(self, directory: Union[str, Path], file_format: str = 'csv') -> List[SpectralSignature]:
        """Load all signatures from a directory"""
        directory = Path(directory)
        signatures = []
        
        if file_format.lower() == 'csv':
            pattern = '*.csv'
            loader_func = self.load_csv
        else:
            pattern = '*.json'
            loader_func = self.load_json
        
        for filepath in directory.glob(pattern):
            try:
                signature = loader_func(filepath)
                signatures.append(signature)
            except Exception as e:
                print(f"Warning: Could not load {filepath}: {e}")
        
        return signatures


if __name__ == "__main__":
    # Example usage
    loader = SpectralSignatureLoader()
    
    # Example: Load a signature (when files exist)
    # signature = loader.load_csv("signatures/gold_exploration/example.csv")
    # print(f"Loaded signature: {signature.signature_id}")
    # print(f"Band 13 value: {signature.get_band_value(13)}")
    # print(f"Band 16 value: {signature.get_band_value(16)}")
    
    print("Spectral Signature Loader ready!")
    print("Use loader.load_csv() or loader.load_json() to load signatures")

