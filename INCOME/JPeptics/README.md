# JPeptics Product & Photo Naming Conventions

## 1. Product Naming Conventions v1.0

### **Schema Format:**
```
{PRODUCT_CODE}-{STRENGTH}-{PACK_SIZE}
```

### **Component Definitions:**
- **PRODUCT_CODE:** 
  - `TZ` = Tirzepatide
  - `RT` = Retatrutide
- **STRENGTH:** 
  - `30` = 30mg (Tirzepatide)
  - `20` = 20mg (Retatrutide)
- **PACK_SIZE:**
  - `3PK` = 3-pack
  - `6PK` = 6-pack
  - `10PK` = 10-pack

### **Complete Product SKU List:**

| Product | Strength | Pack Size | **SKU Code** | Description |
|---------|----------|-----------|--------------|-------------|
| Tirzepatide | 30mg | 3-pack | `TZ-30-3PK` | Tirzepatide 30mg 3-pack |
| Tirzepatide | 30mg | 6-pack | `TZ-30-6PK` | Tirzepatide 30mg 6-pack |
| Tirzepatide | 30mg | 10-pack | `TZ-30-10PK` | Tirzepatide 30mg 10-pack |
| Retatrutide | 20mg | 3-pack | `RT-20-3PK` | Retatrutide 20mg 3-pack |
| Retatrutide | 20mg | 6-pack | `RT-20-6PK` | Retatrutide 20mg 6-pack |
| Retatrutide | 20mg | 10-pack | `RT-20-10PK` | Retatrutide 20mg 10-pack |

---

## 2. Photo Naming Conventions v1.0

### **Schema Format:**
```
{PRODUCT_CODE}-{PACK_SIZE}-{IMAGE_TYPE}-{VARIANT}-{BATCH}.{ext}
```

### **Component Definitions:**
- **PRODUCT_CODE:** `TZ`, `RT` (consistent with product naming)
- **PACK_SIZE:** `3PK`, `6PK`, `10PK`, `SINGLE` (for individual vial shots)
- **IMAGE_TYPE:**
  - `PACK` = Package/box shots
  - `VIAL` = Individual vial shots
  - `LABEL` = Label close-ups
  - `HERO` = Main marketing images
  - `LIFESTYLE` = In-use/context shots
- **VARIANT:** `A`, `B`, `C` (for multiple angles/variations)
- **BATCH:** `JP-TIRZ-0925`, `JP-RITA-0925` (links to lab results)

### **Photo Examples:**

#### **Tirzepatide 10-pack:**
- `TZ-10PK-PACK-A-JP-TIRZ-0925.png` (package front view)
- `TZ-10PK-PACK-B-JP-TIRZ-0925.png` (package back view)
- `TZ-10PK-VIAL-A-JP-TIRZ-0925.png` (individual vial from pack)
- `TZ-10PK-HERO-A-JP-TIRZ-0925.png` (main marketing shot)

#### **Retatrutide 6-pack:**
- `RT-6PK-PACK-A-JP-RITA-0925.png` (package front view)
- `RT-6PK-PACK-B-JP-RITA-0925.png` (package back view)
- `RT-6PK-VIAL-A-JP-RITA-0925.png` (individual vial from pack)
- `RT-6PK-HERO-A-JP-RITA-0925.png` (main marketing shot)

#### **Individual Components:**
- `TZ-SINGLE-LABEL-A-JP-TIRZ-0925.png` (Tirzepatide label detail)
- `RT-SINGLE-LABEL-A-JP-RITA-0925.png` (Retatrutide label detail)
- `BACT-SINGLE-VIAL-A-BATCH001.jpeg` (Bacteriostatic water)

---

## 3. File Migration Plan for `/Active` Folder

### **Current → New Mapping:**

| Current File          | New File Name                        | Batch Code   | Notes             |
| --------------------- | ------------------------------------ | ------------ | ----------------- |
| `TZ-10pk-A.png`       | `TZ-10PK-PACK-A-JP-TIRZ-0925.png`    | JP-TIRZ-0925 | Package front     |
| `TZ-10pk-B.png`       | `TZ-10PK-PACK-B-JP-TIRZ-0925.png`    | JP-TIRZ-0925 | Package back      |
| `TZ-Label.png`        | `TZ-SINGLE-LABEL-A-JP-TIRZ-0925.png` | JP-TIRZ-0925 | Label detail      |
| `TZ-Vile.jpeg`        | `TZ-SINGLE-VIAL-A-JP-TIRZ-0925.jpeg` | JP-TIRZ-0925 | Individual vial   |
| `RT-10pk-A.png`       | `RT-10PK-PACK-A-JP-RITA-0925.png`    | JP-RITA-0925 | Package front     |
| `RT-10pk-B.png`       | `RT-10PK-PACK-B-JP-RITA-0925.png`    | JP-RITA-0925 | Package back      |
| `RT-Label.png`        | `RT-SINGLE-LABEL-A-JP-RITA-0925.png` | JP-RITA-0925 | Label detail      |
| `RT-Vile.png`         | `RT-SINGLE-VIAL-A-JP-RITA-0925.png`  | JP-RITA-0925 | Individual vial   |
| `BACTERIOSTATIC.jpeg` | `BACT-SINGLE-VIAL-A-BATCH001.jpeg`   | BATCH001     | Companion product |
| `JPeptics-Logo.png`   | `JPEPTICS-LOGO-MAIN-A.png`           | N/A          | Brand asset       |

### **Migration Steps:**
1. **Backup** current `/Active` folder
2. **Create batch tracking spreadsheet** with current assignments
3. **Rename files** using new convention
4. **Update** any references in existing code
5. **Test** image loading on website

---

## Batch Tracking System

### **Batch Code Format:**
```
JP-{PRODUCT_CODE}-{MMYY}
```

**Current Batches:**
- `JP-TIRZ-0925` (Tirzepatide September 2025)
- `JP-RITA-0925` (Retatrutide September 2025)

### **Photo-to-Batch Linking:**
Every product photo includes the batch code to ensure traceability to:
- Certificate of Analysis (COA)
- Lab testing results
- Manufacturing date
- Quality control documentation

---

## Usage Notes

- **SKU codes are internal only** - not displayed to customers
- **Batch codes link directly to lab results** for compliance
- **Photo naming enables automated batch tracking** for quality assurance
- **System scales for future products** and different strengths
- **All files maintain consistent naming** across folders and systems