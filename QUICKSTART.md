# Quick Start Guide

Get started with the Spectral Signatures Collection in 5 minutes!

## Installation

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd spectral_signatures_collection
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Basic Usage

### 1. Create Your First Signature

```python
from tools.signature_creator import create_signature_from_array
import numpy as np

# Your 18-band values (example)
band_values = np.array([
    0.234, 0.312, 0.289, 0.267, 0.245, 0.223,  # Bands 1-6
    0.189, 0.245, 0.201, 0.178, 0.156, 0.134,  # Bands 7-12
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0              # Bands 13-18 (indices)
])

# Gold pathfinder indices
index_values = np.array([0]*12 + [220, 180, 150, 250, 170, 140])

# Create signature
signature = create_signature_from_array(
    band_values=band_values,
    signature_id="my_first_signature",
    category="gold_exploration",
    location={"latitude": 48.75, "longitude": 82.15},
    source={"sensor": "ASTER", "scene_id": "AST_07_..."},
    index_values=index_values
)

# Save it
signature.save_csv("signatures/gold_exploration/my_first_signature.csv")
```

### 2. Load an Existing Signature

```python
from tools.spectral_signature_loader import SpectralSignatureLoader

loader = SpectralSignatureLoader()
signature = loader.load_csv("signatures/gold_exploration/my_first_signature.csv")

# Access band values
phyllic_value = signature.get_index_value(13)  # Band 13: Phyllic Sericite
composite_value = signature.get_index_value(16)  # Band 16: Composite Gold

print(f"Phyllic: {phyllic_value}, Composite: {composite_value}")
```

### 3. Compare Signatures

```python
from tools.signature_comparison import compare_signatures

sig1 = loader.load_csv("signatures/gold_exploration/high_gold_001.csv")
sig2 = loader.load_csv("signatures/background/barren_001.csv")

comparison = compare_signatures(sig1, sig2, focus_bands=[13, 16])
print(f"Separability: {comparison['separability']:.3f}")
```

### 4. Visualize Signatures

```python
from tools.signature_plotter import plot_signature, plot_gold_pathfinders

# Plot single signature
plot_signature(signature, show_indices=True, save_path="my_signature.png")

# Compare gold pathfinders
plot_gold_pathfinders(
    [sig1, sig2],
    labels=['High Gold', 'Background'],
    save_path="comparison.png"
)
```

### 5. Validate Signatures

```python
from tools.signature_validator import SignatureValidator

validator = SignatureValidator()
is_valid, errors = validator.validate_signature(signature)

if is_valid:
    print("✅ Signature is valid!")
else:
    print("❌ Errors:", errors)
```

## Next Steps

1. **Extract signatures** from your ASTER data using QGIS SCP plugin
2. **Add to collection** following the [Extraction Guide](docs/extraction_guide.md)
3. **Compare signatures** to identify patterns
4. **Use for classification** in your remote sensing workflows

## Examples

See `examples/example_usage.py` for complete examples of all functionality.

## Need Help?

- Read the [README.md](README.md) for detailed documentation
- Check [docs/](docs/) for guides
- Review example signatures in `examples/`

Happy exploring! 🚀

