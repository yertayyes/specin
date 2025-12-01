#!/usr/bin/env python3
"""
Spectral Signature Plotter
==========================
Visualize spectral signatures with matplotlib
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
from spectral_signature_loader import SpectralSignature


def plot_signature(signature: SpectralSignature, 
                   value_type: str = 'reflectance',
                   show_continuum_removed: bool = False,
                   show_indices: bool = False,
                   save_path: Optional[str] = None,
                   figsize: tuple = (12, 6)):
    """Plot a single spectral signature
    
    Args:
        signature: SpectralSignature to plot
        value_type: 'reflectance', 'continuum_removed', or 'index'
        show_continuum_removed: Whether to overlay continuum-removed values
        show_indices: Whether to show index values for bands 13-18
        save_path: Optional path to save figure
        figsize: Figure size tuple
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    band_numbers = [b['band_number'] for b in sorted(signature.bands, key=lambda x: x.get('band_number', 0))]
    
    if value_type == 'reflectance':
        values = signature.get_all_values('reflectance')
        ylabel = 'Reflectance'
        title = f'Spectral Signature: {signature.signature_id}'
    elif value_type == 'index':
        values = signature.get_all_values('index')
        ylabel = 'Index Value'
        title = f'Gold Pathfinder Indices: {signature.signature_id}'
    else:
        values = signature.get_all_values('continuum_removed')
        ylabel = 'Continuum Removed Reflectance'
        title = f'Continuum Removed Signature: {signature.signature_id}'
    
    # Plot main values
    ax.plot(band_numbers, values, 'o-', linewidth=2, markersize=8, label=value_type.title())
    
    # Overlay continuum removed if requested
    if show_continuum_removed and value_type == 'reflectance':
        cr_values = signature.get_all_values('continuum_removed')
        if np.any(~np.isnan(cr_values)):
            ax.plot(band_numbers, cr_values, 's--', linewidth=1.5, markersize=6, 
                   alpha=0.7, label='Continuum Removed')
    
    # Highlight gold pathfinder bands (13-18)
    if show_indices or value_type == 'index':
        index_values = []
        index_bands = []
        for band in sorted(signature.bands, key=lambda x: x.get('band_number', 0)):
            if band.get('band_number', 0) >= 13:
                idx_val = band.get('index_value')
                if idx_val is not None:
                    index_values.append(idx_val)
                    index_bands.append(band.get('band_number'))
        
        if index_values:
            ax2 = ax.twinx()
            ax2.bar(index_bands, index_values, alpha=0.3, color='gold', label='Gold Indices')
            ax2.set_ylabel('Index Value', color='gold')
            ax2.tick_params(axis='y', labelcolor='gold')
    
    # Add vertical lines separating band groups
    ax.axvline(x=6.5, color='gray', linestyle='--', alpha=0.3, linewidth=1)
    ax.axvline(x=12.5, color='gray', linestyle='--', alpha=0.3, linewidth=1)
    
    # Add labels
    ax.set_xlabel('Band Number')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best')
    
    # Add band group labels
    ax.text(3.5, ax.get_ylim()[1] * 0.95, 'Raw SWIR', ha='center', fontsize=9, alpha=0.7)
    ax.text(9.5, ax.get_ylim()[1] * 0.95, 'CR SWIR', ha='center', fontsize=9, alpha=0.7)
    ax.text(15.5, ax.get_ylim()[1] * 0.95, 'Gold Indices', ha='center', fontsize=9, alpha=0.7)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to: {save_path}")
    else:
        plt.show()


def plot_multiple_signatures(signatures: List[SpectralSignature],
                            value_type: str = 'reflectance',
                            labels: Optional[List[str]] = None,
                            save_path: Optional[str] = None,
                            figsize: tuple = (14, 8)):
    """Plot multiple signatures for comparison
    
    Args:
        signatures: List of SpectralSignature objects
        value_type: 'reflectance', 'continuum_removed', or 'index'
        labels: Optional list of labels (defaults to signature_id)
        save_path: Optional path to save figure
        figsize: Figure size tuple
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if labels is None:
        labels = [sig.signature_id for sig in signatures]
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(signatures)))
    
    for sig, label, color in zip(signatures, labels, colors):
        band_numbers = [b['band_number'] for b in sorted(sig.bands, key=lambda x: x.get('band_number', 0))]
        values = sig.get_all_values(value_type)
        ax.plot(band_numbers, values, 'o-', linewidth=2, markersize=6, 
               label=label, color=color, alpha=0.8)
    
    # Add vertical lines
    ax.axvline(x=6.5, color='gray', linestyle='--', alpha=0.3, linewidth=1)
    ax.axvline(x=12.5, color='gray', linestyle='--', alpha=0.3, linewidth=1)
    
    ylabel = value_type.replace('_', ' ').title()
    ax.set_xlabel('Band Number')
    ax.set_ylabel(ylabel)
    ax.set_title('Spectral Signature Comparison')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='best', fontsize=9)
    
    # Add band group labels
    ax.text(3.5, ax.get_ylim()[1] * 0.95, 'Raw SWIR', ha='center', fontsize=9, alpha=0.7)
    ax.text(9.5, ax.get_ylim()[1] * 0.95, 'CR SWIR', ha='center', fontsize=9, alpha=0.7)
    ax.text(15.5, ax.get_ylim()[1] * 0.95, 'Gold Indices', ha='center', fontsize=9, alpha=0.7)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to: {save_path}")
    else:
        plt.show()


def plot_gold_pathfinders(signatures: List[SpectralSignature],
                         labels: Optional[List[str]] = None,
                         save_path: Optional[str] = None,
                         figsize: tuple = (10, 6)):
    """Plot gold pathfinder indices (bands 13-18) for multiple signatures
    
    Args:
        signatures: List of SpectralSignature objects
        labels: Optional list of labels
        save_path: Optional path to save figure
        figsize: Figure size tuple
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    if labels is None:
        labels = [sig.signature_id for sig in signatures]
    
    colors = plt.cm.tab10(np.linspace(0, 1, len(signatures)))
    
    band_names = ['Phyllic\nSericite', 'Argillic\nKaolinite', 'Propylitic\nChlorite',
                  'Composite\nGold', 'Hydrothermal\nIntensity', 'Advanced\nArgillic']
    band_numbers = [13, 14, 15, 16, 17, 18]
    x_pos = np.arange(len(band_names))
    
    width = 0.8 / len(signatures)
    
    for i, (sig, label, color) in enumerate(zip(signatures, labels, colors)):
        values = [sig.get_index_value(bn) or 0 for bn in band_numbers]
        offset = (i - len(signatures)/2 + 0.5) * width
        ax.bar(x_pos + offset, values, width, label=label, color=color, alpha=0.8)
    
    ax.set_xlabel('Gold Pathfinder Index')
    ax.set_ylabel('Index Value')
    ax.set_title('Gold Pathfinder Indices Comparison')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(band_names, rotation=45, ha='right')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved plot to: {save_path}")
    else:
        plt.show()


if __name__ == "__main__":
    print("Spectral Signature Plotter")
    print("=" * 50)
    print("\nAvailable functions:")
    print("- plot_signature() - Plot single signature")
    print("- plot_multiple_signatures() - Compare multiple signatures")
    print("- plot_gold_pathfinders() - Focus on gold pathfinder indices")
    print("\nExample:")
    print("  plot_signature(signature, value_type='reflectance', show_indices=True)")
    print("  plot_multiple_signatures([sig1, sig2], labels=['High Gold', 'Background'])")

