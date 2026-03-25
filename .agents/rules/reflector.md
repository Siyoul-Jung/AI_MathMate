# reflector: AI MathMate Coding Standards

## Python Standards
- Use **Type Hints** for all function signatures.
- Prefer **Asynchronous** functions (`async def`) for API-related logic.
- Use absolute paths for database operations when running standalone scripts to avoid CWD issues.

## LaTeX Standards (CRITICAL)
Consistency in math rendering is paramount.
- **Degrees**: Always use `^\circ`. Do NOT use `\text{circ}` or `extcirc`.
- **Multiplication**: Always use `\times`. Avoid `*` or implicit spacing.
- **Symbols**:
  - Triangle: `\triangle`
  - Theta: `\theta`
  - Bullet: `\bullet`
- **Formatting**: Ensure math is wrapped in `$` (inline) or `$$` (block) based on content depth.

## Frontend (React/TS) Standards
- Use **Functional Components** with explicit `FC` types.
- **Tailwind CSS**: Use consistent spacing and color palettes (Slate/Zinc for dark mode).
- **Icons**: Use `lucide-react`.
- **State Management**: Use React Hooks (useState, useEffect) and Context API if needed.
