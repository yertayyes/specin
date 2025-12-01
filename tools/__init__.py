"""
Spectral Signature Collection Tools
===================================
Python tools for working with spectral signatures
"""

from .spectral_signature_loader import SpectralSignature, SpectralSignatureLoader
from .signature_creator import create_signature_from_array, create_signature_from_scp_export
from .signature_comparison import compare_signatures, find_similar_signatures
from .signature_validator import SignatureValidator
from .signature_plotter import plot_signature, plot_multiple_signatures, plot_gold_pathfinders

__all__ = [
    'SpectralSignature',
    'SpectralSignatureLoader',
    'create_signature_from_array',
    'create_signature_from_scp_export',
    'compare_signatures',
    'find_similar_signatures',
    'SignatureValidator',
    'plot_signature',
    'plot_multiple_signatures',
    'plot_gold_pathfinders'
]

