# WCAG 2.1 AA Accessibility Audit Report

## Date: May 6, 2026
## Target: ISL Glossary Platform

### Executive Summary
This report documents accessibility findings during the initial audit of the modernized ISL Glossary Platform. Audit scope covers key pages: organisation list, organisation home, sign detail, staff dashboard, and manager dashboard.

---

## 1. Color Contrast Issues (WCAG AA requires 4.5:1 for normal text)

### Critical Issues Found:
- **Muted text on light backgrounds**: `--muted: #59656f` on `--bg: #f6f8fb` = ~5.2:1 ✓ PASS
- **Body text**: `--ink: #17201c` on `--bg: #f6f8fb` = ~15:1 ✓ PASS  
- **Link color**: `#075985` on `--bg: #f6f8fb` = ~7:1 ✓ PASS
- **Muted link text**: May fail at smaller sizes. Needs remediation.
- **Dark mode**: Out of scope for the thesis prototype.

### Recommended Fixes:
✓ Current palette meets AA standards for normal text
- Ensure all text meets 4.5:1 at 14px minimum

---

## 2. Focus Indicators & Keyboard Navigation

### Current Implementation:
```css
a:focus-visible,
button:focus-visible {
  outline: 3px solid color-mix(in srgb, var(--accent) 55%, white);
  outline-offset: 3px;
}
```

### Issues:
- ❌ Outline color may not have sufficient contrast against all backgrounds
- ✓ 3px outline width is good (WCAG recommends 3px minimum)
- ✓ outline-offset provides good visibility

### Required Fixes:
1. Ensure focus outline has 3:1 contrast with background in all contexts
2. Test on dark backgrounds and light backgrounds
3. Verify all interactive elements are keyboard-focusable

---

## 3. Semantic HTML & ARIA Labels

### Current Issues Found:
- ✓ Skip link present: `<a class="skip-link" href="#main">`
- ✓ Semantic landmarks: `<header>`, `<main>`, `<nav>`
- ✓ Headings: Proper hierarchy (h1, h2, h3)
- ⚠ Unnamed regions: Some divs with class="grid three-col" lack aria-label
- ⚠ Icon buttons: ♡ and ♥ buttons need aria-label attributes
- ⚠ Details/summary: Nav menu uses `<details><summary>Menu</summary>` but may confuse screen reader users

### Required Fixes:
1. Add aria-label to all icon-only buttons
2. Add aria-label to grid regions if they don't have headings
3. Test details/summary element with NVDA and VoiceOver

---

## 4. Form Accessibility

### Current Issues Found:
- ✓ Forms use proper `<label>` elements
- ✓ Form inputs have associated labels
- ❌ Error messages: Not explicitly associated with form fields via aria-describedby
- ⚠ Required indicators: Use text "* required" but no aria-required attribute

### Required Fixes:
1. Add aria-required="true" to required form fields
2. Use aria-describedby to link error messages to inputs
3. Add aria-invalid="true" to fields with errors

---

## 5. Images & Alt Text

### Current Issues Found:
- ✓ Logo images have alt text: `alt="{{ organisation.name }} logo"`
- ✓ Decorative dividers use aria-hidden="true"
- ✓ Screenshot/example images would need alt text (if added)

### Required Fixes:
- None currently; alt text strategy is good

---

## 6. Video Accessibility

### Current Issues Found:
- ⚠ ISL videos (core content) do not yet have hosted captions.
- ⚠ Video placeholder just shows URL: `<a href="{{ sign.video_url }}">{{ sign.video_url }}</a>`
- ✓ Transcript model exists for optional text transcripts linked to signs.

### Required Fixes:
- Embed video player that supports captions
- Render available transcripts on sign detail pages
- Add alt text description for sign video context

---

## 7. Animations & Motion

### Current Implementation:
- ✓ `@media (prefers-reduced-motion: reduce)` is in base CSS
- ✓ Animations are disabled for users preferring reduced motion
- ✓ Transitions use standard timing (150-250ms)

### Status:
✓ COMPLIANT - No changes needed

---

## 8. Page Structure & Landmarks

### Current Implementation:
- ✓ `<header>` with navigation
- ✓ `<main id="main">` as primary content
- ✓ Skip link targets `#main`
- ✓ Each section has heading

### Required Fixes:
- Add `role="complementary"` or `<aside>` for sidebar video panels
- Consider adding `role="contentinfo"` to footer when added

---

## 9. Focus Management

### Current Implementation:
- ✓ Skip link positioned absolutely off-screen, visible on focus
- ✓ All buttons and links keyboard-focusable
- ⚠ Modal/form focus trapping not implemented yet

### Required Fixes:
- Test Tab order on all pages (should be logical top-to-bottom)
- Implement focus trapping in modals (Phase 5)

---

## 10. Text Resizing & Zoom

### Current Implementation:
- ✓ `font-size` is in `rem` units (responsive to user zoom)
- ✓ `line-height` is unitless ratio (responsive)
- ✓ Viewport meta tag allows zoom: `maximum-scale=5.0`

### Status:
✓ COMPLIANT

---

## Priority Remediation Plan

### P0 (Critical - Must Fix):
1. Add aria-label to icon-only buttons (♡/♥)
2. Add aria-required and aria-describedby to forms
3. Verify focus outline contrast (especially on blue buttons)
4. Render available transcripts on sign detail pages
5. Test keyboard navigation on all pages

### P1 (High - Should Fix):
1. Add aria-label to grid regions without headings
2. Keep colour contrast documented for each organisation theme
3. Test with screen reader (NVDA or VoiceOver)
4. Document focus order in README

### P2 (Medium - Nice to Have):
1. Add aria-live="polite" to form validation feedback
2. Implement ARIA tabs for tabbed content
3. Add breadcrumb schema.org markup
4. Create Accessibility Statement in footer

### P3 (Low - Future):
1. Add captions to ISL videos
2. Implement ARIA live regions for async updates
3. Create high-contrast theme option
4. User testing with Deaf/disabled users

---

## Testing Checklist

- [ ] axe DevTools scan: 0 violations
- [ ] WAVE browser extension: 0 errors
- [ ] Keyboard-only navigation: Tab through entire page, all interactive elements reachable
- [ ] Screen reader test: NVDA (Windows), VoiceOver (Mac), TalkBack (Android)
- [ ] Color contrast: All text meets 4.5:1 (AA) or 7:1 (AAA where critical)
- [ ] Focus indicators: Visible on all interactive elements
- [ ] Resize text to 200%: No content loss, readable layout
- [ ] Zoom page to 200%: No horizontal scroll, content still accessible

---

## Next Steps

1. Implement P0 fixes (this phase)
2. Run automated accessibility scans
3. Perform manual keyboard and screen reader testing
4. Document findings in README
5. Schedule user testing with Deaf/blind participants if possible

