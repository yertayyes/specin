# Repository Structure

```
spectral_signatures_collection/
│
├── README.md                    # Main documentation
├── QUICKSTART.md                # Quick start guide
├── STRUCTURE.md                  # This file
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── signatures/                  # Spectral signature data files
│   ├── gold_exploration/       # Gold pathfinder signatures
│   ├── minerals/                # Mineral-specific signatures
│   ├── vegetation/              # Vegetation signatures
│   └── background/              # Background/barren signatures
│
├── tools/                       # Python utilities
│   ├── __init__.py             # Package initialization
│   ├── spectral_signature_loader.py    # Load signatures from CSV/JSON
│   ├── signature_creator.py            # Create new signatures
│   ├── signature_comparison.py         # Compare signatures
│   ├── signature_validator.py          # Validate signatures
│   └── signature_plotter.py           # Visualize signatures
│
├── docs/                        # Documentation
│   ├── signature_format.md      # Format specification
│   ├── extraction_guide.md     # How to extract signatures
│   └── contributing.md         # Contribution guidelines
│
├── examples/                    # Example code and signatures
│   └── example_usage.py         # Complete usage examples
│
└── templates/                  # Signature templates
    ├── signature_template.csv   # CSV template
    └── signature_template.json  # JSON template
```

## File Descriptions

### Core Files
- **README.md**: Main documentation with overview, usage examples, and API reference
- **QUICKSTART.md**: 5-minute quick start guide
- **requirements.txt**: Python package dependencies (numpy, matplotlib)

### Tools (`tools/`)
- **spectral_signature_loader.py**: Load and save signatures in CSV/JSON formats
- **signature_creator.py**: Create signatures from arrays, SCP exports, or QGIS pixels
- **signature_comparison.py**: Compare signatures, calculate separability, find similar signatures
- **signature_validator.py**: Validate signature format and quality
- **signature_plotter.py**: Visualize signatures with matplotlib

### Documentation (`docs/`)
- **signature_format.md**: Detailed format specification
- **extraction_guide.md**: Step-by-step guide for extracting signatures
- **contributing.md**: Guidelines for contributing signatures

### Templates (`templates/`)
- **signature_template.csv**: CSV template with all 18 bands
- **signature_template.json**: JSON template with full metadata structure

## Usage Workflow

1. **Extract** signature from ASTER data (QGIS SCP plugin)
2. **Create** signature using `signature_creator.py`
3. **Validate** using `signature_validator.py`
4. **Save** to appropriate category directory
5. **Compare** with existing signatures
6. **Visualize** using `signature_plotter.py`

## Adding New Signatures

1. Use template from `templates/` directory
2. Fill in band values and metadata
3. Validate using `signature_validator.py`
4. Save to appropriate category in `signatures/`
5. Follow naming conventions (see CONTRIBUTING.md)

