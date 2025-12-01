# Contributing to Spectral Signatures Collection

Thank you for your interest in contributing to this collection! This guide will help you add new spectral signatures.

## How to Contribute

### 1. Adding a New Signature

#### Step 1: Extract Signature
- Use QGIS SCP plugin or other extraction tools
- Follow the [Extraction Guide](extraction_guide.md)

#### Step 2: Format Signature
- Use templates from `templates/` directory
- Ensure all required fields are filled
- Follow naming conventions

#### Step 3: Validate Signature
```python
from tools.signature_validator import SignatureValidator

validator = SignatureValidator()
is_valid, errors = validator.validate_signature(signature)

if not is_valid:
    # Fix errors before submitting
    print(errors)
```

#### Step 4: Save to Appropriate Directory
- `signatures/gold_exploration/` - Gold pathfinder signatures
- `signatures/minerals/` - Mineral-specific signatures
- `signatures/vegetation/` - Vegetation signatures
- `signatures/background/` - Background/barren signatures

#### Step 5: Submit
- Create a pull request
- Include description of signature
- Reference source data if applicable

## Signature Quality Standards

### Required Information
- ✅ All 18 bands with values
- ✅ Signature ID (unique)
- ✅ Category classification
- ✅ Location metadata (lat/lon or UTM)
- ✅ Source information (sensor, scene ID, date)

### Recommended Information
- ⭐ Continuum-removed values
- ⭐ Index values for bands 13-18
- ⭐ Statistics (mean, std, min, max)
- ⭐ Notes and validation status

## Naming Conventions

### File Names
- Format: `{category}_{descriptor}_{number}.csv`
- Example: `gold_exploration_high_potential_001.csv`

### Signature IDs
- Use lowercase with underscores
- Be descriptive but concise
- Include category prefix

## Validation Checklist

Before submitting, ensure:
- [ ] Signature passes validation (`signature_validator.py`)
- [ ] All required fields are present
- [ ] Band values are in correct range
- [ ] Location metadata is accurate
- [ ] Source information is complete
- [ ] File follows naming conventions
- [ ] Both CSV and JSON formats are provided (optional but recommended)

## Code Contributions

### Code Style
- Follow PEP 8 for Python code
- Add docstrings to functions
- Include type hints where appropriate

### Testing
- Test new tools with example signatures
- Ensure backward compatibility
- Update documentation if needed

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Review example signatures
3. Open an issue for discussion

Thank you for contributing!

