import json
import sqlite3
import importlib.util
import sys
import os
import time
import re
import random
import hashlib

# 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.append(project_root)

# 공통 프롬프트 & 생성기 임포트
from amc_engine.config.prompt_config import SYSTEM_BASE_PROMPT
from amc_engine.generators.generator_llm import generate_variant_with_gemini
from amc_engine.verifier import run_all_stages
from amc_engine.utils.latex_cleaner import LatexCleaner
from amc_engine.config.themes import AIME_THEME_REGISTRY, DNA_THEME_MAPPING

# ─────────────────────────────────────────────────────────────
# 파이프라인 설정
# ─────────────────────────────────────────────────────────────
MAX_LLM_RETRIES = 3   # LLM 생성 재시도 최대 횟수 (실패 원인 피드백 포함)
MAX_SEED_SEARCH_ATTEMPTS = 10 # 중복되지 않는 시드 탐색 최대 횟수
API_COOLDOWN_SECONDS = 15 # API 통신 오류 시 냉각 시간

DIFFICULTY_BANDS = ["CHALLENGER", "EXPERT", "MASTER"]
MODE_MOCK = "MOCK"
MODE_DRILL = "DRILL"

FLOAT_TOLERANCE = 1e-6
DEFAULT_DB_NAME = "amc_factory.db"



def load_solver_dynamically(year, exam, p_id):
    # New P-Centric structure: exams/{year}/{exam}/{band}/{p_id}/solver.py
    for band in DIFFICULTY_BANDS:
        path = os.path.join(current_dir, "exams", str(year), exam, band, p_id, "solver.py")
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location(f"solver_{p_id}", path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module.Solver
    
    # Fallback to legacy path
    legacy_path = os.path.join(current_dir, "solvers", "modules", str(year), exam, f"{p_id}.py")
    if os.path.exists(legacy_path):
        spec = importlib.util.spec_from_file_location(f"solver_{p_id}", legacy_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module.Solver
        
    raise FileNotFoundError(f"Solver for {p_id} not found in any band or legacy path.")


class ProblemFactory:
    def __init__(self, db_name=DEFAULT_DB_NAME):
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
        self._create_table()

    def _get_engine_id(self, year, exam, p_id):
        return f"{exam}-{year}-{p_id}"

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # V3 Schema: engines table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS engines (
                    engine_id TEXT PRIMARY KEY,
                    dna_tag TEXT,
                    category TEXT,
                    difficulty_band TEXT,
                    has_image_support BOOLEAN,
                    reference_note TEXT
                )
            """)
            # V3 Schema: variants table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS variants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    engine_id TEXT,
                    mode TEXT,
                    drill_level INTEGER,
                    drill_focus TEXT,
                    narrative TEXT,
                    variables_json TEXT,
                    solution_json TEXT,
                    correct_answer TEXT,
                    theme_name TEXT,
                    image_url TEXT,
                    seed_key TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (engine_id) REFERENCES engines(engine_id)
                )
            """)
            # Legacy table (for backward compatibility during transition)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS generated_problems (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_year TEXT,
                    exam_type TEXT,
                    problem_num TEXT,
                    narrative TEXT,
                    variables TEXT,
                    solution_steps TEXT,
                    correct_answer REAL,
                    theme TEXT,
                    seed_key TEXT,
                    attempt_count INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    problem_mode TEXT DEFAULT 'MOCK',
                    drill_level INTEGER
                )
            """)
            # seed_key 컬럼이 없는 기존 DB에도 안전하게 추가
            try:
                cursor.execute("ALTER TABLE generated_problems ADD COLUMN seed_key TEXT")
            except Exception:
                pass
            try:
                cursor.execute("ALTER TABLE generated_problems ADD COLUMN attempt_count INTEGER DEFAULT 1")
            except Exception:
                pass
            try:
                cursor.execute("ALTER TABLE generated_problems ADD COLUMN problem_mode TEXT DEFAULT 'MOCK'")
            except Exception:
                pass
            try:
                cursor.execute("ALTER TABLE generated_problems ADD COLUMN drill_level INTEGER")
            except Exception:
                pass
            conn.commit()

    def _seed_is_duplicate(self, seed_key: str) -> bool:
        """동일 시드가 이미 DB에 있는지 확인 (Legacy Deprecated)"""
        return False

    def get_supported_levels(self, year, exam, p_id):
        try:
            Solver = load_solver_dynamically(year, exam, p_id)
            levels = getattr(Solver, 'DRILL_LEVELS', [1, 2, 3])
            band = getattr(Solver, 'DIFFICULTY_BAND', None)
            
            # Fallback based on folder structure if metadata is missing
            if band is None:
                for b in DIFFICULTY_BANDS:
                    if os.path.exists(os.path.join(current_dir, "exams", year, exam, b, p_id)):
                        band = b
                        break

            # Secondary fallback based on problem number
            if band is None:
                try:
                    num = int(p_id[1:])
                    if num <= 5: band = "CHALLENGER"
                    elif num <= 10: band = "EXPERT"
                    else: band = "MASTER"
                except:
                    band = "CHALLENGER"
                    
            metadata = self.get_problem_metadata(year, exam, p_id)
            return {"levels": levels, "band": band, "metadata": metadata}
        except Exception:
            return {"levels": [1, 2, 3], "band": "UNKNOWN", "metadata": None}

    def get_problem_metadata(self, year, exam, p_id):
        """Loads metadata.json from the P-Centric folder."""
        for band in DIFFICULTY_BANDS:
            path = os.path.join(current_dir, "exams", str(year), exam, band, p_id, "metadata.json")
            if os.path.exists(path):
                import json
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        return None

    def _load_template(self, year, exam, p_id):
        """MD 템플릿 로드 (P-Centric 구조 우선, 레거시 지원)"""
        md_text = None
        for band in DIFFICULTY_BANDS:
            path = os.path.join(current_dir, "exams", str(year), exam, band, p_id, "template.md")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
        
        legacy_md_path = os.path.join(current_dir, "datasets", str(year), exam, f"{p_id}.md")
        if os.path.exists(legacy_md_path):
            with open(legacy_md_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        raise FileNotFoundError(f"Template for {p_id} not found.")

    def _generate_seed(self, TargetSolver, year, exam, p_id, mode, drill_level):
        """중복되지 않는 시드를 생성"""
        for _ in range(MAX_SEED_SEARCH_ATTEMPTS):
            if mode == MODE_DRILL and drill_level is not None:
                if not hasattr(TargetSolver, "generate_drill_seed"):
                    print(f"[{year} {exam} {p_id}] 드릴 모드 미지원.")
                    return None, None
                candidate = TargetSolver.generate_drill_seed(drill_level)
            else:
                candidate = TargetSolver.generate_seed()
            
            candidate_key = json.dumps(sorted(candidate.items()))
            
            if mode == MODE_DRILL or not self._seed_is_duplicate(candidate_key):
                seed_key = candidate_key + f"_v{int(time.time()*1000)}" if mode == MODE_DRILL else candidate_key
                return candidate, seed_key
        
        return None, None

    def _build_prompt(self, md_text, perfect_seed, TargetSolver, metadata, mode, drill_level, drill_intent=None):
        """DNA 기반 프롬프트 조립"""
        if mode == MODE_DRILL:
            # 기본 instruction 가져오기
            narrative_instruction = TargetSolver.get_drill_instruction(perfect_seed, drill_level or 1)
            
            # 천만 단위 이상의 큰 숫자는 mod 1000 규칙 강제 적용
            if 'expected_t' in perfect_seed and isinstance(perfect_seed['expected_t'], (int, float)) and perfect_seed['expected_t'] >= 1_000_000:
                perfect_seed['expected_t'] = int(perfect_seed['expected_t']) % 1000
                auto_pedagogy_rule = (
                    '\n\n[CRITICAL PEDAGOGY RULE]:\n'
                    'The total deterministic number of valid arrangements/schedules is '
                    'astronomically large (exceeding 1,000,000). To test the student\'s mathematical logic '
                    'and strictly adhere to AIME orthodox Number Theory styling, you MUST clearly append '
                    'the following explicit instruction at the very end of your problem text: '
                    '"Find the remainder when the total number of valid ways is divided by 1000." '
                    'Do not ask for the full unsimplified integer.'
                )
                narrative_instruction += auto_pedagogy_rule
            
            md_content = narrative_instruction
        else:
            narrative_instruction = TargetSolver.get_narrative_instruction(perfect_seed)
            md_content = md_text.replace("{NARRATIVE_INSTRUCTION}", narrative_instruction)

        for key, value in perfect_seed.items():
            md_content = md_content.replace(f"{{{key}}}", str(value))

        metadata_context = ""
        if metadata:
            domain = metadata.get('domain', 'Mathematics')
            tags = ", ".join(metadata.get('dna_tags', []))
            
            metadata_context = f"\n\n[DNA-AWARE PEDAGOGY CONTEXT]\n- Core Domain: {domain}\n- Concept Tags: {tags}\n"
            
            # Intelligent Drill Intent Logic
            if mode == MODE_DRILL:
                if drill_intent:
                    # 분석된 단계 정보가 있는 경우 최우선 적용
                    metadata_context += f"- [ANALYZED DRILL FOCUS]: {drill_intent.get('concept', 'N/A')}\n"
                    metadata_context += f"- [STEP GOAL]: {drill_intent.get('goal', 'N/A')}\n"
                    metadata_context += f"- [INSTRUCTION]: {drill_intent.get('description', 'Provide a focused sub-problem.')}\n"
                else:
                    # 레거시 Solver 기반 Intent
                    intent = TargetSolver.get_drill_intent(drill_level or 1)
                    drill_focus = metadata.get('drill_config', {}).get(f"L{drill_level}", "")
                    if intent:
                        metadata_context += f"- Level {drill_level} Pedagogical Focus: {intent.get('focus', 'N/A')}\n"
                        metadata_context += f"- Step Goal: {intent.get('goal', 'N/A')}\n"
                        metadata_context += f"- [DYNAMIC INSTRUCTION]: {intent.get('details', drill_focus)}\n"
            
            metadata_context += "\nPlease ensure the generated problem narrative strictly adheres to this mathematical DNA and pedagogical intent.\n"
        
        # [Phase 16]: Logic Steps Injection (Pedagogical Backbone)
        logic_steps = TargetSolver.get_logic_steps(perfect_seed)
        if logic_steps:
            metadata_context += "\n[MATHEMATICAL LOGIC STEPS (STRICT GUIDELINE)]\n"
            for step in logic_steps:
                metadata_context += f"Step {step.get('step')}: {step.get('title')} - {step.get('description')}\n"
            metadata_context += "The generated step-by-step solution MUST strictly follow this mathematical roadmap to ensure accuracy.\n"
        
        # Theme Injection Logic
        dna = getattr(TargetSolver, 'DNA', {})
        # Support both 'category' (legacy) and 'categories' (list)
        categories = dna.get('categories', [dna.get('category', 'Mathematics')])
        
        # [Phase 13]: Drill Context Logic
        # LV1 drills are strictly abstract. Others inherit from DNA.
        context_type = dna.get('context_type', 'narrative')
        if mode == MODE_DRILL and drill_level == 1:
            context_type = 'abstract'
        
        # Pick a random theme from appropriate categories
        if context_type == 'abstract':
            selected_cat = "ABSTRACT"
            selected_theme = random.choice(AIME_THEME_REGISTRY["ABSTRACT"])
            theme_hint = f"\n\n[NARRATIVE STYLE HINT]\n- Categories: {', '.join(categories)}\n- Style: Minimalist / Pure Mathematics\n"
            theme_hint += "This is an abstract mathematical problem. State the logic directly without additional scenario layers. Focus on formal academic notation.\n"
        else:
            # Aggregate all allowed theme categories for all math categories
            all_allowed_cats = []
            for cat in categories:
                all_allowed_cats.extend(DNA_THEME_MAPPING.get(cat, ["ABSTRACT"]))
            
            # Unique categories
            all_allowed_cats = list(set(all_allowed_cats))
            
            selected_cat = random.choice(all_allowed_cats)
            selected_theme = random.choice(AIME_THEME_REGISTRY[selected_cat])
            theme_hint = f"\n\n[NARRATIVE STYLE HINT]\n- Categories: {', '.join(categories)}\n- Selected Context: {selected_cat}\n- Theme: {selected_theme}\n"
            theme_hint += "Please use this theme to frame the mathematical core logic. Ensure the vocabulary remains academic and professional.\n"

        selected_log_theme = selected_theme if context_type == 'narrative' else "Abstract Math"
        base_prompt = f"{SYSTEM_BASE_PROMPT}\n\n{md_content}{metadata_context}{theme_hint}"
        
        return base_prompt, selected_log_theme

    def _run_llm_generation_loop(self, base_prompt, perfect_seed, seed_key, dna_tag, year, exam, p_id, mode, drill_level, has_image_dna=False):
        """LLM 생성 + 검증 (Retry-with-Feedback 루프)"""
        feedback = ""
        for attempt in range(1, MAX_LLM_RETRIES + 1):
            current_prompt = base_prompt + feedback
            raw_response = generate_variant_with_gemini(current_prompt)

            try:
                search_result = re.search(r'\{.*\}', raw_response, re.DOTALL)
                if not search_result:
                    raise ValueError("No JSON block found in response")
                new_data = json.loads(search_result.group())
            except Exception as e:
                feedback = f"\n\n[RETRY {attempt}/{MAX_LLM_RETRIES}] JSON 파싱 실패: {e}. Return ONLY a valid JSON object, no markdown."
                print(f"  ↳ 시도 {attempt}: ❌ JSON 파싱 실패")
                continue

            new_data['4_solver_payload'] = perfect_seed
            # Normalize BEFORE verification to remove recoverable artifacts (like \t)
            self._normalize_latex_in_response(new_data)
            
            narrative = new_data.get('3_presentation', {}).get('problem_statement', '')
            ok, failed_stage, reason = run_all_stages(narrative, perfect_seed, dna_tag, has_image_dna)
            if ok:
                print(f"  ↳ 시도 {attempt}: ✅ 검증 통과")
                return new_data, attempt
            else:
                feedback = f"\n\n[RETRY {attempt}/{MAX_LLM_RETRIES}] Stage {failed_stage} 검증 실패: {reason} 이 부분을 정확히 수정하세요."
                print(f"  ↳ 시도 {attempt}: ❌ Stage {failed_stage} — {reason}")
                
                # New: Detailed logging for REJECTED variants
                self._save_to_db(new_data, year, exam, p_id, "NONE", seed_key, attempt, mode, drill_level, status='REJECTED', failed_stage=failed_stage, reason=reason)

        return None, MAX_LLM_RETRIES

    def _verify_solver_solution(self, TargetSolver, new_data, perfect_seed):
        """Solver 실행 최종 검증"""
        payload = new_data.get('4_solver_payload', {})
        solver_instance = TargetSolver(payload, {})
        return abs(solver_instance.execute() - perfect_seed['expected_t']) <= FLOAT_TOLERANCE

    def _handle_image_generation(self, TargetSolver, perfect_seed, seed_key, year, exam, p_id, new_data):
        """이미지 생성 및 임베딩 + 스마트 감지"""
        has_image_dna = getattr(TargetSolver, 'DNA', {}).get('has_image', False)
        
        # Check if narrative mentions figures regardless of DNA
        narrative = new_data.get('3_presentation', {}).get('problem_statement', '')
        figure_keywords = ['figure', 'graph', 'diagram', 'triangle', 'circle', 'parabola', 'coordinate plane', 'plot']
        mentions_figure = any(kw in narrative.lower() for kw in figure_keywords)

        if not has_image_dna:
            if mentions_figure:
                print(f"  ↳ ⚠️ WARNING: Figure referenced in text but Solver lacks image-DNA.")
                new_data['validation_warnings'] = new_data.get('validation_warnings', []) + ["Figure mentioned but no graph DNA found"]
            return

        img_dir = os.path.join(os.path.dirname(__file__), 'images', str(year), exam, p_id)
        os.makedirs(img_dir, exist_ok=True)
        
        hash_suffix = hashlib.md5(seed_key.encode('utf-8')).hexdigest()[:8]
        img_filename = f"{p_id}_{hash_suffix}.png"
        img_path = os.path.join(img_dir, img_filename)
        
        # public/images relative path for frontend
        public_url = f"images/{year}/{exam}/{p_id}/{img_filename}"
        
        try:
            TargetSolver.generate_image(perfect_seed, img_path)
            new_data['image_url'] = public_url
            print(f"  ↳ 🖼️ 이미지 생성 성공 ({img_filename})")
        except Exception as e:
            print(f"  ↳ ⚠️ 이미지 생성 실패: {e}")
            new_data['validation_warnings'] = new_data.get('validation_warnings', []) + [f"Image generation failed: {e}"]

    def _validate_latex(self, text):
        return LatexCleaner.validate(text)

    def _normalize_latex(self, text):
        # 4. Math-Text Redundancy: "$r$ $r$", "$s$ $s$"
        text = re.sub(r'\$([a-zA-Z])\$\s+\$\1\$', r'$\1$', text)
        text = re.sub(r'\b([a-zA-Z])\b\s+\$\1\$', r'$\1$', text) # "r $r$" -> "$r$"
        text = re.sub(r'\$([a-zA-Z])\$\s+\b\1\b', r'$\1$', text) # "$r$ r" -> "$r$"
        
        # 5. Fix duplicated units/words: "units units", "ways ways"
        text = re.sub(r'\b(\w{3,})\b\s+\1\b', r'\1', text) 

        return text.strip()
        
        # 4. Fix 'times' mangling (often becomes imes or  imes)
        text = text.replace(' imes', ' \\times ')
        text = re.sub(r'(\d)\s*imes\s*(\d)', r'\1 \\times \2', text)
        text = text.replace('\\ imes', ' \\times ')
        text = text.replace('  times', ' \\times ')
        
        # Cleanup redundant carets or spaces around carets
        text = re.sub(r'\^+\s*\\circ', r'^\\circ', text)
        text = text.replace('^^', '^')
        text = text.replace('^ ^', '^')
        
        return text

    def _normalize_latex_in_response(self, new_data):
        """응답 데이터 내 모든 LaTeX 표현식을 정규화"""
        if '3_presentation' in new_data and 'problem_statement' in new_data['3_presentation']:
            new_data['3_presentation']['problem_statement'] = self._normalize_latex(new_data['3_presentation']['problem_statement'])
        
        if '5_solution' in new_data and 'step_by_step' in new_data['5_solution']:
            solution = new_data['5_solution']['step_by_step']
            if isinstance(solution, list):
                new_data['5_solution']['step_by_step'] = [self._normalize_latex(s) for s in solution]
            else:
                new_data['5_solution']['step_by_step'] = self._normalize_latex(solution)

    def process_new_variant(self, year, exam, p_id, mode=MODE_MOCK, drill_level=None, drill_intent=None):
        """문제 생성 파이프라인 전체를 조율"""
        # 1. 리소스 로드
        md_text = self._load_template(year, exam, p_id)
        TargetSolver = load_solver_dynamically(year, exam, p_id)
        metadata = self.get_problem_metadata(year, exam, p_id)

        # 2. 시드 생성
        perfect_seed, seed_key = self._generate_seed(TargetSolver, year, exam, p_id, mode, drill_level)
        if not perfect_seed:
            print(f"⏭  [{year} {exam} {p_id}] 새로운 시드 생성 실패 — 시드 공간 포화")
            return False

        # 3. 프롬프트 빌드 및 LLM 실행
        base_prompt, selected_log_theme = self._build_prompt(md_text, perfect_seed, TargetSolver, metadata, mode, drill_level, drill_intent)
        dna_tag = getattr(TargetSolver, 'DNA', {}).get('specific_tag', '')
        has_image_dna = getattr(TargetSolver, 'DNA', {}).get('has_image', False)
        print(f"🎲 [{year} {exam} {p_id}] DNA: {dna_tag} | 시드: {perfect_seed}")
        
        new_data, attempt = self._run_llm_generation_loop(base_prompt, perfect_seed, seed_key, dna_tag, year, exam, p_id, mode, drill_level, has_image_dna)
        if not new_data:
            print(f"❌ [{p_id}] {MAX_LLM_RETRIES}회 재시도 후 생성 실패")
            return False

        # 4. 최종 검증 및 후처리
        if not self._verify_solver_solution(TargetSolver, new_data, perfect_seed):
            print("❌ Solver 실행 결과 불일치")
            return False

        self._handle_image_generation(TargetSolver, perfect_seed, seed_key, year, exam, p_id, new_data)
        # (Normalization already handled in generation loop before verification)

        # --- Validation & Quality Audit ---
        narrative = new_data.get('3_presentation', {}).get('problem_statement', '')
        latex_errors = self._validate_latex(narrative)
        warnings = new_data.get('validation_warnings', [])
        
        if latex_errors or warnings:
            print(f"  ↳ 🔍 Quality Alert for {p_id}:")
            for err in latex_errors: print(f"    - [LATEX ERROR] {err}")
            for wrn in warnings: print(f"    - [WARNING] {wrn}")
        else:
            print(f"  ↳ ⭐ Quality Check Passed (Perfect)")

        # 5. DB 저장
        self._save_to_db(new_data, year, exam, p_id, selected_log_theme, seed_key, attempt, mode, drill_level)
        new_data['engine_id'] = self._get_engine_id(year, exam, p_id)
        print(f"✅ 생성 성공 (정답: {perfect_seed['expected_t']})")
        return new_data

    def _save_to_db(self, data, year, exam, p_id, theme_name, seed_key, attempt_count, mode, drill_level, status='VERIFIED', failed_stage=0, reason=None):
        if mode == MODE_MOCK:
            drill_level = None
        engine_id = self._get_engine_id(year, exam, p_id)
        
        if data is None: data = {} # Handle REJECTED case where data might be sparse
        pres = data.get('3_presentation', {})
        payload = data.get('4_solver_payload', seed_key) # Use seed_key as fallback if data is sparse
        if isinstance(payload, str) and not payload.startswith('{'): # If it's the raw key
             payload = {} # Placeholder
             
        sol = data.get('5_solution', {})
        meta_theme = data.get('2_generation_metadata', {}).get('problem_style', theme_name)
        drill_focus = data.get('2_generation_metadata', {}).get('drill_focus')

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 1. Engine Auto-Registration
            metadata = self.get_problem_metadata(year, exam, p_id) or {}
            dna_path = f"exams/{year}/{exam}/{p_id}/solver.py" # Heuristic
            cursor.execute("""
                INSERT INTO engines (engine_id, dna_tag, category, difficulty_band, has_image_support, dna_path)
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(engine_id) DO UPDATE SET
                dna_tag=excluded.dna_tag, category=excluded.category, difficulty_band=excluded.difficulty_band,
                has_image_support=excluded.has_image_support, dna_path=excluded.dna_path
            """, (
                engine_id, 
                metadata.get('dna_tag'), 
                metadata.get('category'), 
                metadata.get('difficulty_band'),
                metadata.get('has_image_support', False),
                dna_path
            ))
            
            # 2. Save variant (New V4 Schema)
            query_v4 = """
                INSERT INTO variants
                (engine_id, mode, drill_level, drill_focus, narrative, variables_json,
                 solution_json, correct_answer, theme_name, image_url, seed_key, status, raw_variables)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query_v4, (
                engine_id, mode, drill_level, drill_focus,
                pres.get('problem_statement'),
                json.dumps(payload),
                json.dumps(sol.get('step_by_step')),
                str(payload.get('expected_t', '0')),
                meta_theme,
                data.get('image_url'),
                seed_key,
                status,
                json.dumps(payload) # Preservation of Source of Truth
            ))
            variant_id = cursor.lastrowid
            
            # 3. Log errors if REJECTED
            if status == 'REJECTED':
                cursor.execute("""
                    INSERT INTO verification_logs (variant_id, error_type, details)
                    VALUES (?, ?, ?)
                """, (variant_id, f"STAGE_{failed_stage}", reason))
            
            conn.commit()

    def get_random_variant(self, year, exam, p_id, mode=MODE_MOCK, drill_level=None):
        """DB에서 조건에 맞는 무작위 변형 문항 하나를 가져옵니다 (V3 Schema)."""
        engine_id = self._get_engine_id(year, exam, p_id)
        query = """
            SELECT engine_id, narrative, variables_json, solution_json, correct_answer, theme_name, image_url, seed_key
            FROM variants
            WHERE engine_id = ? AND mode = ? AND status = 'VERIFIED'
        """
        params = [engine_id, mode]
        if drill_level is not None:
            query += " AND drill_level = ?"
            params.append(drill_level)
        else:
            query += " AND drill_level IS NULL"
        
        if mode == MODE_DRILL:
            query += " ORDER BY id ASC LIMIT 1"
        else:
            query += " ORDER BY RANDOM() LIMIT 1"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            
            if not row:
                return None
            
            solution_steps = row["solution_json"]
            try:
                solution_steps = json.loads(solution_steps)
            except (json.JSONDecodeError, TypeError):
                pass

            return {
                "engine_id": row["engine_id"],
                "2_generation_metadata": {"problem_style": row["theme_name"]},
                "3_presentation": {"problem_statement": row["narrative"]},
                "4_solver_payload": json.loads(row["variables_json"]),
                "5_solution": {"step_by_step": solution_steps},
                "image_url": row["image_url"],
                "seed_key": row["seed_key"]
            }

    def get_verification_stats(self):
        """Returns statistics on VERIFIED vs REJECTED variants."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT status, COUNT(*) as count FROM variants GROUP BY status")
            return {row["status"]: row["count"] for row in cursor.fetchall()}

    def get_recent_failures(self, limit=10):
        """Returns the most recent verification failures."""
        query = """
            SELECT v.id, v.engine_id, v.seed_key, l.error_type, l.details, l.created_at
            FROM variants v
            JOIN verification_logs l ON v.id = l.variant_id
            ORDER BY l.created_at DESC
            LIMIT ?
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, (limit,))
            return [dict(row) for row in cursor.fetchall()]

    def get_all_mission_counts(self):
        """Returns a dict of engine_id -> count of VERIFIED variants."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT engine_id, COUNT(*) as count FROM variants WHERE status = 'VERIFIED' GROUP BY engine_id")
            return {row["engine_id"]: row["count"] for row in cursor.fetchall()}

    def analyze_logic_steps(self, explanation):
        """
        Uses LLM to analyze a solution and extract meaningful, non-trivial logic steps.
        This provides the architectural backbone for 'Analysis-First' drill generation.
        """
        if isinstance(explanation, list):
            explanation = "\n".join(explanation)

        prompt = f"""
        [SYSTEM ROLE: AIME PEDAGOGY ANALYST]
        Analyze the following AIME solution and extract a sequence of SUBSTANTIVE mathematical logic steps.
        
        [STRICT RULES]
        1. EXCLUDE TRIVIAL FINAL STEPS: Do not create a separate step for "Calculate the final answer modulo 1000" or simple arithmetic formatting.
        2. REDUCTIVE SUB-PROBLEMS: Each step must be a standalone mathematical bridge that simplifies the core problem.
        3. PEDAGOGICAL VALUE: Each step should be suitable for an 'Isolated Drill' focused on one core concept.
        
        [SOLUTION]
        {explanation}
        
        [OUTPUT FORMAT (JSON)]
        {{
          "summary": "Brief summary of solution strategy",
          "logic_steps": [
            {{ 
              "step_id": 1, 
              "description": "Pedagogical description of the target step", 
              "concept": "Core mathematical concept (e.g. Legendre's Formula, Symmetry)",
              "goal": "Specific goal for the student to solve in this isolated drill"
            }}
          ]
        }}
        """
        from amc_engine.generators.generator_llm import generate_variant_with_gemini
        try:
            result_raw = generate_variant_with_gemini(prompt)
            # Find JSON block
            import re
            search_result = re.search(r'\{.*\}', result_raw, re.DOTALL)
            if not search_result:
                return []
            import json
            analysis_data = json.loads(search_result.group())
            return analysis_data.get('logic_steps', [])
        except Exception as e:
            print(f"⚠️ Logic analysis failed: {e}")
            return []


def run_factory(year, exam, p_id, target=100, mode=MODE_MOCK, level=None):
    factory = ProblemFactory()
    success = 0
    attempts = 0
    print(f"\n🚀 [AI MathMate Factory] 타겟: {year} {exam} {p_id} | 목표: {target}개 | 모드: {mode} (LVL {level})")
    print("=" * 70)

    while success < target:
        attempts += 1
        print(f"\n--- [{success + 1}/{target}] 생성 중 (시도: {attempts}) ---")
        try:
            if factory.process_new_variant(year, exam, p_id, mode, drill_level=level):
                success += 1
                time.sleep(1.5)
            else:
                time.sleep(2)
        except Exception as e:
            print(f"⚠️ API 통신 오류: {e}")
            print(f"⏳ {API_COOLDOWN_SECONDS}초 냉각 후 재가동...")
            time.sleep(API_COOLDOWN_SECONDS)

    print(f"\n🎉 완료: {success}개 생성 (총 시도 {attempts}회)")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI MathMate Problem Generator")
    parser.add_argument("--year", default="2025")
    parser.add_argument("--category", default="AIME1")
    parser.add_argument("--pid", default="P10")
    parser.add_argument("--target", type=int, default=1)
    parser.add_argument("--mode", default=MODE_DRILL, choices=[MODE_MOCK, MODE_DRILL])
    parser.add_argument("--level", type=int, default=3)
    
    args = parser.parse_args()
    run_factory(args.year, args.category, args.pid, target=args.target, mode=args.mode, level=args.level)