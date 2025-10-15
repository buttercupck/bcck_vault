---
request_id: CR-<% tp.date.now("YYYYMMDD") %>-<% tp.file.cursor(1) %>
date_created: <% tp.date.now("YYYY-MM-DD") %>
status: <% tp.system.suggester(["DRAFT", "SUBMITTED", "IN_PROGRESS", "COMPLETED"], ["DRAFT", "SUBMITTED", "IN_PROGRESS", "COMPLETED"]) %>
---
## LOCATION
**File/Page:** [filename.php or page name]
**Section Identifier:** [specific section, component, or element]
- Parent container: [if nested]
- Element type: [header, hero-banner, product-card, footer, etc.]

---
## CURRENT STATE
**What exists now:**
[Describe what's currently there - can include code snippets, current copy, or visual description]

**Issues/Problems:**
- [Why this needs to change]

---

## DESIRED STATE

### Action Type: [REPLACE | ADJUST | ENHANCE | DELETE]
### Change Category: [VISUAL | FUNCTIONAL | CONTENT | PERFORMANCE]

**What should it become:**

#### For VISUAL changes:
- Colors: [hex codes or brand color names]
- Typography: [font, size, weight, alignment]
- Spacing: [margins, padding, layout]
- Effects: [shadows, gradients, animations]

#### For FUNCTIONAL changes:
- Button behavior: [link destinations, hover states]
- Form actions: [submission endpoints, validation]
- Navigation: [menu links, routing]
- Interactive elements: [click handlers, toggles]

#### For CONTENT changes:
- **Title:** [new heading text]
- **Subheading:** [new subheading text]
- **Body:** [new paragraph text - use <br> for line breaks]
- **Images:** [new image URLs with descriptive names]
- **Buttons:** [button text + link destination]
  ```html
  <button class="[class-names]" href="[destination]">[Button Text]</button>
  ```

#### For PERFORMANCE changes:
- Issue: [what's slow/broken]
- Expected improvement: [load time, functionality fix]

## 5. VERIFICATION CHECKLIST
-[ ] Changes match provided references/specifications
- [ ]  All requested changes completed
- [ ]  No out-of-scope modifications made
- [ ]  Functionality tested and working
- [ ]  Visual elements render correctly
- [ ]  Performance metrics acceptable
- [ ]  Cross-browser/device compatibility checked (if applicable)
## 6. REPORT OUT
**Files Modified:**
**Sections Changed:**
**Deviations from Request:**
**Downstream Dependencies:**
**Additional Notes:**

---

## TEMPLATE USAGE NOTES:

- Chavvo will complete sections 5-6 after implementation
- Reference README.md if needed.
