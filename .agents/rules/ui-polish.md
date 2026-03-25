# ui-polish: AI MathMate Design Guidelines

## Aesthetic Strategy
- **Style**: Modern Glassmorphism with high visual contrast.
- **Color Palette**: Dark theme using Zinc/Slate gradients and subtle border strokes.
- **Typography**: Clean, sans-serif fonts (Inter or similar) prioritized for readability.

## Math Rendering Excellence
- **KaTeX**: All mathematical content must be rendered via KaTeX. 
- **No Raw LaTeX**: Ensure no raw backslash sequences are visible to the user. Use the `ProblemViewer.tsx` rendering logic.
- **Layout**: Center block equations (`$$`) for complex derivations.

## Interaction Design
- **Micro-animations**: Use subtle hover effects on buttons and cards.
- **Scaffolding**: The "Drill Bridge" should feel like a premium transition, not a page jump.
- **Responsiveness**: Ensure math blocks wrap or scroll horizontally on mobile devices.
