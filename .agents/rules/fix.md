# fix: AI MathMate Troubleshooting Patterns

## LaTeX Hallucinations
If the LLM generates incorrect LaTeX (e.g., `text{circ}`), use or refer to the logic in `backend/fix_all_latex.py`.
- **Pattern**: `re.sub(r'60\s*\^?(\^|\\| )*text\{circ\}', r'60^\\circ', text)`

## Database Path Issues
When scripts fail to find the `.db` files, check if an absolute path is required.
- **Reference**: `db_path = r'c:\AI_MathMate\backend\amc_engine\amc_factory.db'`

## JSON Parsing Errors
LLMs sometimes add markdown code blocks (```json) around their responses. Always strip these before parsing.
- **Strategy**: Use regex to extract `{...}` or `[...]` if direct parsing fails.

## Image Path Resolution
Ensure problem images are resolved correctly relative to the static storage directory configured in FastAPI.
