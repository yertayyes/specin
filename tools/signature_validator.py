#!/usr/bin/env python3
"""
Spectral Signature Validator
============================
Validate spectral signatures for format compliance and quality
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from spectral_signature_loader import SpectralSignature, SpectralSignatureLoader


class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass


class SignatureValidator:
    """Validator for spectral signatures"""
    
    REQUIRED_FIELDS = ['signature_id', 'category', 'bands']
    REQUIRED_BAND_FIELDS = ['band_number', 'band_name', 'reflectance_value']
    VALID_CATEGORIES = ['gold_exploration', 'minerals', 'vegetation', 'background', 'other']
    EXPECTED_BAND_COUNT = 18
    
    def validate_signature(self, signature: SpectralSignature) -> Tuple[bool, List[str]]:
        """Validate a spectral signature
        
        Args:
            signature: SpectralSignature object to validate
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check required fields
        if not signature.signature_id:
            errors.append("Missing signature_id")
        
        if not signature.category:
            errors.append("Missing category")
        elif signature.category not in self.VALID_CATEGORIES:
            errors.append(f"Invalid category: {signature.category}. Must be one of {self.VALID_CATEGORIES}")
        
        # Check band count
        if len(signature.bands) != self.EXPECTED_BAND_COUNT:
            errors.append(f"Expected {self.EXPECTED_BAND_COUNT} bands, found {len(signature.bands)}")
        
        # Check band structure
        band_numbers = []
        for i, band in enumerate(signature.bands):
            # Check required fields
            if 'band_number' not in band:
                errors.append(f"Band {i+1}: Missing band_number")
            else:
                band_num = band['band_number']
                if band_num in band_numbers:
                    errors.append(f"Duplicate band_number: {band_num}")
                band_numbers.append(band_num)
            
            if 'band_name' not in band or not band['band_name']:
                errors.append(f"Band {band_num}: Missing or empty band_name")
            
            if 'reflectance_value' not in band:
                errors.append(f"Band {band_num}: Missing reflectance_value")
            else:
                val = band['reflectance_value']
                if val is None:
                    errors.append(f"Band {band_num}: reflectance_value is None")
                elif not isinstance(val, (int, float)):
                    errors.append(f"Band {band_num}: reflectance_value must be numeric")
                elif val < 0 or val > 1:
                    # Warn but don't error (values might be scaled differently)
                    pass
        
        # Check band number sequence
        if len(band_numbers) == self.EXPECTED_BAND_COUNT:
            expected_numbers = list(range(1, self.EXPECTED_BAND_COUNT + 1))
            if sorted(band_numbers) != expected_numbers:
                errors.append(f"Band numbers should be 1-{self.EXPECTED_BAND_COUNT}, found: {sorted(band_numbers)}")
        
        # Check statistics if present
        if signature.statistics:
            stats = signature.statistics
            if 'mean_reflectance' in stats:
                mean = stats['mean_reflectance']
                if mean < 0 or mean > 1:
                    errors.append(f"mean_reflectance out of valid range [0, 1]: {mean}")
        
        return len(errors) == 0, errors
    
    def validate_file(self, filepath: Path, file_format: str = 'csv') -> Tuple[bool, List[str]]:
        """Validate a signature file
        
        Args:
            filepath: Path to signature file
            file_format: 'csv' or 'json'
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        loader = SpectralSignatureLoader()
        
        try:
            if file_format.lower() == 'csv':
                signature = loader.load_csv(filepath)
            else:
                signature = loader.load_json(filepath)
            
            return self.validate_signature(signature)
        except Exception as e:
            return False, [f"Error loading file: {str(e)}"]
    
    def validate_directory(self, directory: Path, file_format: str = 'csv') -> Dict[str, Tuple[bool, List[str]]]:
        """Validate all signature files in a directory
        
        Args:
            directory: Directory containing signature files
            file_format: 'csv' or 'json'
        
        Returns:
            Dictionary mapping filename to (is_valid, errors)
        """
        results = {}
        
        pattern = '*.csv' if file_format.lower() == 'csv' else '*.json'
        
        for filepath in directory.glob(pattern):
            is_valid, errors = self.validate_file(filepath, file_format)
            results[filepath.name] = (is_valid, errors)
        
        return results
    
    def check_quality(self, signature: SpectralSignature) -> Dict[str, any]:
        """Check signature quality metrics
        
        Args:
            signature: SpectralSignature to check
        
        Returns:
            Dictionary with quality metrics
        """
        quality = {
            'has_location': bool(signature.location),
            'has_source': bool(signature.source),
            'has_statistics': bool(signature.statistics),
            'has_metadata': bool(signature.metadata),
            'has_continuum_removed': False,
            'has_index_values': False,
            'data_completeness': 0.0
        }
        
        # Check for continuum removed values
        cr_count = sum(1 for b in signature.bands if b.get('continuum_removed') is not None)
        quality['has_continuum_removed'] = cr_count > 0
        
        # Check for index values (bands 13-18)
        index_count = sum(1 for b in signature.bands if b.get('index_value') is not None)
        quality['has_index_values'] = index_count > 0
        
        # Calculate data completeness
        total_fields = len(signature.bands) * 4  # reflectance, cr, index, notes
        filled_fields = sum(
            1 for b in signature.bands
            for field in ['reflectance_value', 'continuum_removed', 'index_value', 'notes']
            if b.get(field) is not None and b.get(field) != ''
        )
        quality['data_completeness'] = filled_fields / total_fields if total_fields > 0 else 0.0
        
        return quality


if __name__ == "__main__":
    validator = SignatureValidator()
    
    print("Spectral Signature Validator")
    print("=" * 50)
    print("\nUsage:")
    print("  validator = SignatureValidator()")
    print("  is_valid, errors = validator.validate_signature(signature)")
    print("  quality = validator.check_quality(signature)")
    print("\nExample:")
    print("  results = validator.validate_directory(Path('signatures/gold_exploration'))")
    print("  for filename, (is_valid, errors) in results.items():")
    print("      print(f'{filename}: {\"VALID\" if is_valid else \"INVALID\"}')")

