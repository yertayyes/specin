# Relative Spectral Signatures Collection

A comprehensive collection of relative spectral signatures for remote sensing applications, particularly focused on mineral exploration, geological mapping, and ASTER SWIR analysis.

## 📋 Overview

This repository contains standardized spectral signatures extracted from ASTER SWIR data and other remote sensing sources. Signatures are stored in a consistent format that enables easy comparison, analysis, and reuse across different projects.

## 🗂️ Repository Structure

```
spectral_signatures_collection/
├── signatures/              # Spectral signature data files
│   ├── gold_exploration/   # Gold pathfinder signatures
│   ├── minerals/           # Mineral-specific signatures
│   ├── vegetation/         # Vegetation signatures
│   └── background/         # Background/barren signatures
├── tools/                   # Python utilities for working with signatures
├── docs/                    # Documentation and guides
├── examples/                # Example usage scripts
└── templates/              # Signature templates and schemas
```

## 📊 Spectral Signature Format

### CSV Format
Each signature is stored as a CSV file with the following structure:

```csv
band_number,band_name,wavelength_um,reflectance_value,continuum_removed,index_value,notes
1,ASTER_B04_1.66um_Clay_Carbonate,1.656,0.234,0.189,0.0,Clay-carbonate absorption
2,ASTER_B05_2.17um_AlOH_Sericite,2.167,0.312,0.245,0.0,Sericite absorption feature
...
```

### JSON Format
For programmatic access, signatures are also available in JSON:

```json
{
  "signature_id": "high_gold_potential_001",
  "category": "gold_exploration",
  "subcategory": "phyllic_alteration",
  "description": "High gold potential signature with strong sericite features",
  "location": {
    "latitude": 48.75,
    "longitude": 82.15,
    "utm_zone": "44N",
    "easting": 456789,
    "northing": 5401234
  },
  "source": {
    "sensor": "ASTER",
    "scene_id": "AST_07_00405302002053830",
    "acquisition_date": "2002-05-02",
    "extraction_method": "SCP_ROI"
  },
  "bands": [
    {
      "band_number": 1,
      "band_name": "ASTER_B04_1.66um_Clay_Carbonate",
      "wavelength_um": 1.656,
      "reflectance_value": 0.234,
      "continuum_removed": 0.189,
      "index_value": 0.0
    },
    ...
  ],
  "statistics": {
    "mean_reflectance": 0.245,
    "std_reflectance": 0.089,
    "min_reflectance": 0.123,
    "max_reflectance": 0.456
  },
  "metadata": {
    "created_date": "2025-01-26",
    "created_by": "user",
    "validation_status": "validated",
    "notes": "Extracted from confirmed gold occurrence"
  }
}
```

## 🚀 Quick Start

### Loading a Signature

```python
from tools.spectral_signature_loader import SpectralSignatureLoader

loader = SpectralSignatureLoader()
signature = loader.load_csv("signatures/gold_exploration/high_gold_potential_001.csv")
# or
signature = loader.load_json("signatures/gold_exploration/high_gold_potential_001.json")

# Access band values
band_13_value = signature.get_band_value(13)  # Phyllic Sericite index
band_16_value = signature.get_band_value(16)  # Composite Gold index
```

### Comparing Signatures

```python
from tools.signature_comparison import compare_signatures

sig1 = loader.load_csv("signatures/gold_exploration/high_gold_potential_001.csv")
sig2 = loader.load_csv("signatures/background/barren_001.csv")

comparison = compare_signatures(sig1, sig2)
print(f"Separability: {comparison['separability']:.3f}")
print(f"Key differences: {comparison['key_differences']}")
```

### Creating a New Signature

```python
from tools.signature_creator import create_signature_from_array

# From numpy array (18 bands)
band_values = np.array([...])  # Your 18-band values
signature = create_signature_from_array(
    band_values=band_values,
    signature_id="my_signature_001",
    category="gold_exploration",
    location={"latitude": 48.75, "longitude": 82.15},
    source={"sensor": "ASTER", "scene_id": "..."}
)

# Save to repository
signature.save_csv("signatures/gold_exploration/my_signature_001.csv")
signature.save_json("signatures/gold_exploration/my_signature_001.json")
```

## 📚 Band Information

### ASTER SWIR Bands (Bands 1-6)
- **Band 1**: ASTER_B04_1.66um_Clay_Carbonate (1.656 μm)
- **Band 2**: ASTER_B05_2.17um_AlOH_Sericite (2.167 μm)
- **Band 3**: ASTER_B06_2.21um_AlOH_Muscovite (2.209 μm)
- **Band 4**: ASTER_B07_2.26um_MgOH_Chlorite (2.262 μm)
- **Band 5**: ASTER_B08_2.34um_Carbonate (2.336 μm)
- **Band 6**: ASTER_B09_2.40um_Carbonate_Chlorite (2.400 μm)

### Continuum Removed Bands (Bands 7-12)
- Same as above but with continuum removal applied

### Gold Pathfinder Indices (Bands 13-18)
- **Band 13**: Gold_Phyllic_Sericite ⭐ MOST IMPORTANT
- **Band 14**: Gold_Argillic_Kaolinite
- **Band 15**: Gold_Propylitic_Chlorite
- **Band 16**: Gold_Composite_Best ⭐ BEST OVERVIEW
- **Band 17**: Gold_Hydrothermal_Intensity
- **Band 18**: Gold_Advanced_Argillic

## 🎯 Use Cases

### Gold Exploration
- Identify high-potential targets based on phyllic alteration signatures
- Compare signatures from known deposits vs. exploration targets
- Validate remote sensing results with field data

### Mineral Mapping
- Map alteration zones (phyllic, argillic, propylitic)
- Identify specific minerals (sericite, kaolinite, chlorite)
- Characterize hydrothermal systems

### Classification
- Use signatures as training data for supervised classification
- Create spectral libraries for automated mapping
- Validate classification results

## 📖 Documentation

- [Signature Format Specification](docs/signature_format.md)
- [Extraction Guide](docs/extraction_guide.md)
- [Validation Guidelines](docs/validation_guide.md)
- [Contributing Guidelines](docs/contributing.md)

## 🔧 Tools

- `spectral_signature_loader.py` - Load signatures from CSV/JSON
- `signature_comparison.py` - Compare multiple signatures
- `signature_creator.py` - Create new signatures programmatically
- `signature_validator.py` - Validate signature format and quality
- `signature_plotter.py` - Visualize signatures

## 📝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/contributing.md) for guidelines.

### Adding a New Signature

1. Extract signature using SCP or other tools
2. Use the template in `templates/` directory
3. Fill in all required metadata
4. Validate using `signature_validator.py`
5. Submit a pull request

## 📄 License

[Specify your license here]

## 🙏 Acknowledgments

- ASTER data provided by NASA/METI
- SCP Plugin for QGIS
- USGS Spectral Library for reference

## 📧 Contact

[Your contact information]

