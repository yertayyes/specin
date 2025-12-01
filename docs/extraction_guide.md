# Spectral Signature Extraction Guide

## Overview

This guide explains how to extract spectral signatures from ASTER data and add them to this collection.

## Extraction Methods

### Method 1: QGIS SCP Plugin (Recommended)

1. **Load 18-band composite in QGIS**
   - File → Add Raster Layer
   - Select `qgis_interactive_spectral_composite.tif`

2. **Set up SCP Band Set**
   - Plugins → Semi-Automatic Classification Plugin → SCP dock
   - Band set tab → Click "+"
   - Select your 18-band file

3. **Extract Signature**
   - **Point Signature**: Click pixel → Right-click plot → Save signature
   - **ROI Signature**: Create ROI polygon → Mean signature calculated
   - **Transect**: Draw line → Profile along line

4. **Export Signature**
   - Right-click plot → Export
   - Save as CSV

5. **Convert to Standard Format**
   ```python
   from tools.signature_creator import create_signature_from_scp_export
   
   signature = create_signature_from_scp_export(
       scp_filepath="exported_signature.csv",
       signature_id="high_gold_potential_001",
       category="gold_exploration",
       location={"latitude": 48.75, "longitude": 82.15},
       source={"sensor": "ASTER", "scene_id": "..."}
   )
   signature.save_csv("signatures/gold_exploration/high_gold_potential_001.csv")
   ```

### Method 2: Direct Pixel Extraction

If you have pixel coordinates and band values:

```python
from tools.signature_creator import create_signature_from_qgis_pixel

band_values = [0.234, 0.312, 0.289, ...]  # 18 values
signature = create_signature_from_qgis_pixel(
    band_values=band_values,
    pixel_coords={"x": 1234, "y": 5678},
    signature_id="my_signature_001",
    category="gold_exploration",
    source={"sensor": "ASTER", "scene_id": "..."}
)
```

### Method 3: From NumPy Array

```python
from tools.signature_creator import create_signature_from_array
import numpy as np

band_values = np.array([...])  # 18-element array
signature = create_signature_from_array(
    band_values=band_values,
    signature_id="my_signature_001",
    category="gold_exploration",
    location={"latitude": 48.75, "longitude": 82.15},
    source={"sensor": "ASTER", "scene_id": "..."}
)
```

## Best Practices

### 1. Target Selection

**For Gold Exploration:**
- Focus on areas with high Band 13 (Phyllic Sericite) values
- Look for combined high Band 13 + Band 16 (Composite Gold)
- Avoid vegetation-covered areas (check NDVI if available)
- Collect multiple signatures from different alteration zones

### 2. Signature Quality

- **Point Signatures**: Use for specific pixel analysis
- **ROI Signatures**: Use for representative area signatures (mean ± std)
- **Multiple Samples**: Collect 5-10 signatures per target type

### 3. Metadata

Always include:
- Location (lat/lon or UTM coordinates)
- Source scene ID and acquisition date
- Extraction method
- Validation status

### 4. Validation

Before adding to collection:

```python
from tools.signature_validator import SignatureValidator

validator = SignatureValidator()
is_valid, errors = validator.validate_signature(signature)

if not is_valid:
    print("Errors:", errors)
else:
    quality = validator.check_quality(signature)
    print("Quality metrics:", quality)
```

## Workflow Checklist

- [ ] Extract signature from ASTER data
- [ ] Convert to standard format
- [ ] Add location metadata
- [ ] Add source metadata
- [ ] Validate signature format
- [ ] Check quality metrics
- [ ] Save to appropriate category directory
- [ ] Update collection index (if maintained)

## Common Issues

### Issue: Missing Band Values

**Solution**: Ensure all 18 bands are present. Use template if needed.

### Issue: Values Out of Range

**Solution**: Check if values are scaled (0-255 vs 0-1). Normalize if needed.

### Issue: Missing Metadata

**Solution**: Use template files in `templates/` directory to ensure all fields are present.

## Next Steps

After extraction:
1. Validate signature
2. Compare with existing signatures
3. Visualize signature
4. Add to collection
5. Document in collection index

