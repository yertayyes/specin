# Spectral Signature Format Specification

## Overview

This document describes the standardized format for storing relative spectral signatures in this collection.

## File Formats

### CSV Format

Each signature is stored as a CSV file with the following columns:

| Column | Type | Required | Description |
|--------|------|----------|-------------|
| `band_number` | Integer | Yes | Band number (1-18) |
| `band_name` | String | Yes | Standardized band name |
| `wavelength_um` | Float | Conditional | Wavelength in micrometers (for bands 1-12) |
| `reflectance_value` | Float | Yes | Reflectance value (0-1 scale) |
| `continuum_removed` | Float | No | Continuum-removed reflectance value |
| `index_value` | Float | No | Index value (for bands 13-18) |
| `notes` | String | No | Additional notes about the band |

### JSON Format

JSON format provides more structured metadata:

```json
{
  "signature_id": "unique_identifier",
  "category": "gold_exploration|minerals|vegetation|background",
  "location": {...},
  "source": {...},
  "bands": [...],
  "statistics": {...},
  "metadata": {...}
}
```

## Band Definitions

### Bands 1-6: Raw ASTER SWIR

| Band | Name | Wavelength (μm) | Description |
|------|------|------------------|-------------|
| 1 | ASTER_B04_1.66um_Clay_Carbonate | 1.656 | Clay-carbonate absorption |
| 2 | ASTER_B05_2.17um_AlOH_Sericite | 2.167 | Al-OH sericite absorption |
| 3 | ASTER_B06_2.21um_AlOH_Muscovite | 2.209 | Al-OH muscovite absorption |
| 4 | ASTER_B07_2.26um_MgOH_Chlorite | 2.262 | Mg-OH chlorite absorption |
| 5 | ASTER_B08_2.34um_Carbonate | 2.336 | Carbonate absorption |
| 6 | ASTER_B09_2.40um_Carbonate_Chlorite | 2.400 | Carbonate-chlorite absorption |

### Bands 7-12: Continuum Removed ASTER

Same as bands 1-6 but with continuum removal applied. Band names prefixed with `CR_`.

### Bands 13-18: Gold Pathfinder Indices

| Band | Name | Description |
|------|------|-------------|
| 13 | Gold_Phyllic_Sericite | Phyllic alteration indicator |
| 14 | Gold_Argillic_Kaolinite | Argillic alteration indicator |
| 15 | Gold_Propylitic_Chlorite | Propylitic alteration indicator |
| 16 | Gold_Composite_Best | Composite gold pathfinder |
| 17 | Gold_Hydrothermal_Intensity | Hydrothermal intensity |
| 18 | Gold_Advanced_Argillic | Advanced argillic alteration |

## Metadata Fields

### Location

```json
{
  "latitude": 48.75,
  "longitude": 82.15,
  "utm_zone": "44N",
  "easting": 456789,
  "northing": 5401234,
  "pixel_x": 1234,
  "pixel_y": 5678
}
```

### Source

```json
{
  "sensor": "ASTER",
  "scene_id": "AST_07_00405302002053830",
  "acquisition_date": "2002-05-02",
  "extraction_method": "SCP_ROI|SCP_Point|Manual",
  "extraction_tool": "QGIS_SCP_Plugin"
}
```

### Statistics

```json
{
  "mean_reflectance": 0.245,
  "std_reflectance": 0.089,
  "min_reflectance": 0.123,
  "max_reflectance": 0.456
}
```

### Metadata

```json
{
  "created_date": "2025-01-26",
  "created_by": "username",
  "validation_status": "validated|pending|rejected",
  "notes": "Additional information"
}
```

## Validation Rules

1. **Band Count**: Must have exactly 18 bands
2. **Band Numbers**: Must be sequential 1-18
3. **Reflectance Values**: Must be numeric, typically in range [0, 1]
4. **Required Fields**: `signature_id`, `category`, `bands`
5. **Category**: Must be one of: `gold_exploration`, `minerals`, `vegetation`, `background`, `other`

## Naming Conventions

### Signature Files

- Format: `{signature_id}.csv` or `{signature_id}.json`
- Example: `high_gold_potential_001.csv`

### Signature IDs

- Use lowercase with underscores
- Include category prefix: `{category}_{descriptor}_{number}`
- Examples:
  - `gold_exploration_high_potential_001`
  - `minerals_sericite_001`
  - `background_barren_001`

## Examples

See `examples/` directory for complete examples.

