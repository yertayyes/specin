#!/usr/bin/env python3
"""
Spectral Signature Comparison
=============================
Compare multiple spectral signatures and calculate separability metrics
"""

import numpy as np
from typing import Dict, List, Tuple
from spectral_signature_loader import SpectralSignature


def calculate_euclidean_distance(sig1: SpectralSignature, sig2: SpectralSignature, 
                                  value_type: str = 'reflectance') -> float:
    """Calculate Euclidean distance between two signatures
    
    Args:
        sig1: First spectral signature
        sig2: Second spectral signature
        value_type: 'reflectance', 'continuum_removed', or 'index'
    
    Returns:
        Euclidean distance
    """
    values1 = sig1.get_all_values(value_type)
    values2 = sig2.get_all_values(value_type)
    
    return float(np.linalg.norm(values1 - values2))


def calculate_correlation(sig1: SpectralSignature, sig2: SpectralSignature,
                          value_type: str = 'reflectance') -> float:
    """Calculate correlation coefficient between two signatures
    
    Args:
        sig1: First spectral signature
        sig2: Second spectral signature
        value_type: 'reflectance', 'continuum_removed', or 'index'
    
    Returns:
        Correlation coefficient (-1 to 1)
    """
    values1 = sig1.get_all_values(value_type)
    values2 = sig2.get_all_values(value_type)
    
    # Remove any NaN values
    mask = ~(np.isnan(values1) | np.isnan(values2))
    if np.sum(mask) < 2:
        return 0.0
    
    values1_clean = values1[mask]
    values2_clean = values2[mask]
    
    correlation = np.corrcoef(values1_clean, values2_clean)[0, 1]
    return float(correlation) if not np.isnan(correlation) else 0.0


def calculate_separability(sig1: SpectralSignature, sig2: SpectralSignature,
                          value_type: str = 'reflectance') -> float:
    """Calculate Jeffries-Matusita separability (0-2, higher is better)
    
    Args:
        sig1: First spectral signature
        sig2: Second spectral signature
        value_type: 'reflectance', 'continuum_removed', or 'index'
    
    Returns:
        Separability value (0-2)
    """
    values1 = sig1.get_all_values(value_type)
    values2 = sig2.get_all_values(value_type)
    
    # Remove NaN values
    mask = ~(np.isnan(values1) | np.isnan(values2))
    if np.sum(mask) < 2:
        return 0.0
    
    values1_clean = values1[mask]
    values2_clean = values2[mask]
    
    # Calculate means and covariances
    mean1 = np.mean(values1_clean)
    mean2 = np.mean(values2_clean)
    std1 = np.std(values1_clean)
    std2 = np.std(values2_clean)
    
    # Simplified separability (Bhattacharyya distance approximation)
    if std1 == 0 or std2 == 0:
        return 0.0
    
    separability = 2 * (1 - np.exp(-0.125 * ((mean1 - mean2) ** 2) / ((std1 + std2) / 2) ** 2))
    return float(min(separability, 2.0))


def compare_signatures(sig1: SpectralSignature, sig2: SpectralSignature,
                      focus_bands: List[int] = None) -> Dict:
    """Comprehensive comparison of two signatures
    
    Args:
        sig1: First spectral signature
        sig2: Second spectral signature
        focus_bands: Optional list of band numbers to focus on (e.g., [13, 16] for gold)
    
    Returns:
        Dictionary with comparison metrics
    """
    comparison = {
        'euclidean_distance': calculate_euclidean_distance(sig1, sig2),
        'correlation': calculate_correlation(sig1, sig2),
        'separability': calculate_separability(sig1, sig2),
        'key_differences': []
    }
    
    # Focus on specific bands if provided (e.g., gold pathfinders)
    if focus_bands:
        differences = []
        for band_num in focus_bands:
            val1 = sig1.get_band_value(band_num) or sig1.get_index_value(band_num)
            val2 = sig2.get_band_value(band_num) or sig2.get_index_value(band_num)
            
            if val1 is not None and val2 is not None:
                diff = abs(val1 - val2)
                band_name = sig1.get_band_by_name(f"Band_{band_num}") or {}
                differences.append({
                    'band_number': band_num,
                    'band_name': band_name.get('band_name', f'Band_{band_num}'),
                    'value1': val1,
                    'value2': val2,
                    'difference': diff,
                    'percent_difference': (diff / max(abs(val1), abs(val2), 0.001)) * 100
                })
        
        comparison['key_differences'] = differences
    else:
        # Compare all bands
        differences = []
        for i in range(1, 19):
            val1 = sig1.get_band_value(i) or sig1.get_index_value(i)
            val2 = sig2.get_band_value(i) or sig2.get_index_value(i)
            
            if val1 is not None and val2 is not None:
                diff = abs(val1 - val2)
                if diff > 0.01:  # Only report significant differences
                    band = sig1.get_band_by_name(f"Band_{i}") or {}
                    differences.append({
                        'band_number': i,
                        'band_name': band.get('band_name', f'Band_{i}'),
                        'value1': val1,
                        'value2': val2,
                        'difference': diff
                    })
        
        comparison['key_differences'] = sorted(differences, key=lambda x: x['difference'], reverse=True)[:10]
    
    return comparison


def find_similar_signatures(target_sig: SpectralSignature, 
                           signature_list: List[SpectralSignature],
                           threshold: float = 0.8) -> List[Tuple[SpectralSignature, float]]:
    """Find signatures similar to target signature
    
    Args:
        target_sig: Target signature to match
        signature_list: List of signatures to search
        threshold: Minimum correlation threshold
    
    Returns:
        List of tuples (signature, correlation) sorted by similarity
    """
    similar = []
    
    for sig in signature_list:
        if sig.signature_id == target_sig.signature_id:
            continue
        
        correlation = calculate_correlation(target_sig, sig)
        if correlation >= threshold:
            similar.append((sig, correlation))
    
    # Sort by correlation (highest first)
    similar.sort(key=lambda x: x[1], reverse=True)
    
    return similar


def compare_multiple_signatures(signatures: List[SpectralSignature],
                               focus_bands: List[int] = None) -> Dict:
    """Compare multiple signatures and create similarity matrix
    
    Args:
        signatures: List of signatures to compare
        focus_bands: Optional list of band numbers to focus on
    
    Returns:
        Dictionary with similarity matrix and statistics
    """
    n = len(signatures)
    similarity_matrix = np.zeros((n, n))
    separability_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i+1, n):
            comparison = compare_signatures(signatures[i], signatures[j], focus_bands)
            similarity_matrix[i, j] = comparison['correlation']
            similarity_matrix[j, i] = comparison['correlation']
            separability_matrix[i, j] = comparison['separability']
            separability_matrix[j, i] = comparison['separability']
    
    # Set diagonal to 1.0 (perfect self-similarity)
    np.fill_diagonal(similarity_matrix, 1.0)
    
    return {
        'similarity_matrix': similarity_matrix.tolist(),
        'separability_matrix': separability_matrix.tolist(),
        'signature_ids': [sig.signature_id for sig in signatures],
        'mean_similarity': float(np.mean(similarity_matrix[similarity_matrix != 1.0])),
        'mean_separability': float(np.mean(separability_matrix[separability_matrix != 0.0]))
    }


if __name__ == "__main__":
    print("Spectral Signature Comparison Tools")
    print("=" * 50)
    print("\nAvailable functions:")
    print("- calculate_euclidean_distance()")
    print("- calculate_correlation()")
    print("- calculate_separability()")
    print("- compare_signatures()")
    print("- find_similar_signatures()")
    print("- compare_multiple_signatures()")
    print("\nExample usage:")
    print("  comparison = compare_signatures(sig1, sig2, focus_bands=[13, 16])")
    print("  print(f'Separability: {comparison[\"separability\"]:.3f}')")

