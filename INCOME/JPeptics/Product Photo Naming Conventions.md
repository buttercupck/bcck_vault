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
{PRODUCT_CODE}-{PK_SIZE}-{IMAGE_TYPE}-{VARIANT}
```

### **Component Definitions:**
- **PRODUCT_CODE:** `TZ`, `RT` (consistent with product naming)
- **PK_SIZE:** `3PK`, `6PK`, `10PK`, `SINGLE` (for individual vial shots)
- **IMAGE_TYPE:**
  - `PACK` = Package/box shots
  - `VIAL` = Individual vial shots
  - `LABEL` = Label close-ups
  - `HERO` = Main marketing images
  - `LIFESTYLE` = In-use/context shots
- **VARIANT:** `A`, `B`, `C` (for multiple angles/variations)

### **Photo Examples:**

#### **Tirzepatide 10-pack:**
- `TZ-10PK-PACK-A` (package front view)
- `TZ-10PK-PACK-B` (package back view)
- `TZ-10PK-VIAL-A (individual vial from pack)
- `TZ-10PK-HERO-A` (main marketing shot)

#### **Retatrutide 6-pack:**
- `RT-6PK-PACK-A` (package front view)
- `RT-6PK-PACK-B (package back view)
- `RT-6PK-VIAL-A` (individual vial from pack)
- `RT-6PK-HERO-A` (main marketing shot)

#### **Individual Components:**
- `TZ-SINGLE-LABEL-A` (Tirzepatide label detail)
- `RT-SINGLE-LABEL-A` (Retatrutide label detail)
- `BACT-SINGLE-VIAL-A` (Bacteriostatic water)

---

## Batch Tracking System

### **Batch Code Format:**
```
{PRODUCT_CODE}-{BATCH NUMBER}
```

**Current Batches:**
- `TIRZ-001` (Tirzepatide First Batch)
- `RITA-001` (Retatrutide First Batch)

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