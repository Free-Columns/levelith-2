# Levelith Tools

This directory contains standalone tools for the Levelith project.

## Color Visualizer

**File:** `color-visualizer.html`

### Overview

An interactive, standalone HTML tool for visualizing and editing the ONETRUTH.ts color configuration. This tool allows developers and designers to:

- View all colors from the ONETRUTH configuration in an organized, visual interface
- Edit colors using multiple methods (RGB, HSL, or Hex)
- See real-time updates as colors change
- Export modified configurations back to TypeScript format

### Features

#### 🎨 Complete Color Coverage
- **Main Colors** (26 colors): Primary, secondary, accent, backgrounds, text, status, borders
- **Gamification Levels** (6 colors): Beginner through legend progression
- **Gamification Achievements** (5 colors): Bronze, silver, gold, platinum, diamond
- **Gamification Progress** (3 colors): Low, medium, high
- **NAICS Industries** (8 colors): Industry-specific color coding

#### 🎚️ Multiple Control Methods
Each color can be adjusted using:
- **RGB Sliders**: Red (0-255), Green (0-255), Blue (0-255)
- **HSL Sliders**: Hue (0-360°), Saturation (0-100%), Lightness (0-100%)
- **Hex Input**: Direct hex color code entry (#RRGGBB)

All three methods stay synchronized - changing one updates the others automatically.

#### 📤 Export Options
- **Download .ts File**: Export the complete ONETRUTH.ts file with your modifications
- **Copy to Clipboard**: Copy the TypeScript code to paste into your editor

### How to Use

1. **Open the Tool**
   ```bash
   # From the project root
   open tools/color-visualizer.html
   # Or simply double-click the file in your file browser
   ```

2. **Edit Colors**
   - Scroll to find the color you want to modify
   - Use any of the three control methods (RGB sliders, HSL sliders, or Hex input)
   - The color swatch updates in real-time
   - All three control types stay synchronized

3. **Export Your Changes**
   - Click "📥 Download .ts File" to download ONETRUTH.ts
   - Or click "📋 Copy to Clipboard" to copy the code
   - Replace the original file at `frontend/src/config/ONETRUTH.ts`

### Testing Checklist

#### Manual Testing
- [ ] All 48 colors display correctly with accurate hex values
- [ ] RGB sliders (R, G, B) update the color in real-time
- [ ] HSL sliders (H, S, L) update the color in real-time
- [ ] Hex input accepts valid hex codes and updates color
- [ ] All three control methods stay synchronized
- [ ] Color swatch reflects current color value
- [ ] "Download .ts File" exports valid TypeScript
- [ ] "Copy to Clipboard" copies valid TypeScript code
- [ ] Exported TypeScript matches ONETRUTH.ts structure
- [ ] Toast notifications appear on export actions

#### Browser Compatibility
Tested in:
- [ ] Chrome/Edge (Chromium)
- [ ] Firefox
- [ ] Safari
- [ ] Mobile browsers (responsive design)

### Technical Details

#### Color Conversion
The tool includes conversion utilities between:
- Hex ↔ RGB
- RGB ↔ HSL
- HSL ↔ Hex

All conversions are performed in real-time with no external dependencies.

#### File Structure
```
color-visualizer.html
├── HTML Structure
│   ├── Header
│   ├── Export Controls
│   └── Color Categories (dynamically generated)
├── CSS Styling
│   ├── Gradient backgrounds
│   ├── Card layouts
│   ├── Slider styling
│   └── Responsive design
└── JavaScript Logic
    ├── ONETRUTH data structure
    ├── Color conversion utilities
    ├── UI update functions
    ├── Export functionality
    └── Clipboard API integration
```

#### Dependencies
**Zero dependencies!** This is a completely standalone HTML file with embedded CSS and JavaScript.

### Troubleshooting

#### Colors don't match ONETRUTH.ts
- The color values are hardcoded into the HTML file
- If ONETRUTH.ts is updated, the HTML file needs to be regenerated with new values

#### Export doesn't work
- Check browser permissions for downloads
- For clipboard copy, ensure HTTPS or localhost (clipboard API requirement)

#### Sliders don't update
- Check browser console for JavaScript errors
- Ensure JavaScript is enabled in your browser

### Development

To modify or enhance the color visualizer:

1. The ONETRUTH data structure is embedded at line ~290
2. Color conversion functions start at line ~350
3. UI rendering starts at line ~650
4. Export functions are at line ~800

### Future Enhancements

Potential improvements:
- [ ] Color picker UI for visual selection
- [ ] Undo/redo functionality
- [ ] Color palette presets
- [ ] A11y contrast checker
- [ ] Dark mode toggle
- [ ] Import from existing ONETRUTH.ts
- [ ] Color scheme generator (complementary, analogous, etc.)

---

**Created for:** Seymour Media Group's Levelith Project
**Version:** 1.0
**Last Updated:** 2025-11-18
