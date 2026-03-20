import json
import sqlite3
import importlib.util
import sys
import os
import time
import re
import random

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
        path = os.path.join(current_dir, "exams", year, exam, band, p_id, "solver.py")
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location(f"solver_{p_id}", path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module.Solver
    
    # Fallback to legacy path
    legacy_path = os.path.join(current_dir, "solvers", "modules", year, exam, f"{p_id}.py")
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
        """동일 시드가 이미 DB에 있는지 확인"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM generated_problems WHERE seed_key = ? LIMIT 1",
                (seed_key,)
            )
            return cursor.fetchone() is not None

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
            return {"levels": [], "band": "UNKNOWN", "metadata": None}

    def get_problem_metadata(self, year, exam, p_id):
        """Loads metadata.json from the P-Centric folder."""
        for band in DIFFICULTY_BANDS:
            path = os.path.join(current_dir, "exams", year, exam, band, p_id, "metadata.json")
            if os.path.exists(path):
                import json
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        return None

    def _load_template(self, year, exam, p_id):
        """MD 템플릿 로드 (P-Centric 구조 우선, 레거시 지원)"""
        md_text = None
        for band in DIFFICULTY_BANDS:
            path = os.path.join(current_dir, "exams", year, exam, band, p_id, "template.md")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()
        
        legacy_md_path = os.path.join(current_dir, "datasets", year, exam, f"{p_id}.md")
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

    def _build_prompt(self, md_text, perfect_seed, TargetSolver, metadata, mode, drill_level):
        """DNA 기반 프롬프트 조립"""
        if mode == MODE_DRILL and drill_level is not None:
            narrative_instruction = TargetSolver.get_drill_instruction(perfect_seed, drill_level)
            
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
            drill_focus = metadata.get('drill_config', {}).get(f"L{drill_level}", "") if mode == MODE_DRILL and drill_level is not None else ""
            
            metadata_context = f"\n\n[DNA-AWARE PEDAGOGY CONTEXT]\n- Core Domain: {domain}\n- Concept Tags: {tags}\n"
            if drill_focus:
                metadata_context += f"- Level {drill_level} Pedagogical Focus: {drill_focus}\n"
            metadata_context += "Please ensure the generated problem narrative strictly adheres to this mathematical DNA.\n"
        
        dna = getattr(TargetSolver, 'DNA', {})
        context_type = dna.get('context_type', 'narrative')
        selected_log_theme = "Abstract Math" if context_type == 'abstract' else "Narrative"
        base_prompt = f"{SYSTEM_BASE_PROMPT}\n\n{md_content}{metadata_context}"
        
        return base_prompt, selected_log_theme

    def _run_llm_generation_loop(self, base_prompt, perfect_seed, dna_tag):
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
            narrative = new_data.get('3_presentation', {}).get('problem_statement', '')

            ok, failed_stage, reason = run_all_stages(narrative, perfect_seed, dna_tag)
            if ok:
                print(f"  ↳ 시도 {attempt}: ✅ 검증 통과")
                return new_data, attempt
            else:
                feedback = f"\n\n[RETRY {attempt}/{MAX_LLM_RETRIES}] Stage {failed_stage} 검증 실패: {reason} 이 부분을 정확히 수정하세요."
                print(f"  ↳ 시도 {attempt}: ❌ Stage {failed_stage} — {reason}")

        return None, MAX_LLM_RETRIES

    def _verify_solver_solution(self, TargetSolver, new_data, perfect_seed):
        """Solver 실행 최종 검증"""
        payload = new_data.get('4_solver_payload', {})
        solver_instance = TargetSolver(payload, {})
        return abs(solver_instance.execute() - perfect_seed['expected_t']) <= FLOAT_TOLERANCE

    def _handle_image_generation(self, TargetSolver, seed_key, year, exam, p_id, new_data):
        """이미지 생성 및 임베딩"""
        if not getattr(TargetSolver, 'DNA', {}).get('has_image', False):
            return

        img_dir = os.path.join(os.path.dirname(__file__), 'images', str(year), exam)
        os.makedirs(img_dir, exist_ok=True)
        
        import hashlib
        hash_suffix = hashlib.md5(seed_key.encode('utf-8')).hexdigest()[:8]
        img_filename = f"{p_id}_{hash_suffix}.png"
        img_path = os.path.join(img_dir, img_filename)
        
        try:
            TargetSolver.generate_image(perfect_seed, img_path)
            image_md = f"\n\n![Graph](images/{year}/{exam}/{img_filename})\n\n"
            if '3_presentation' in new_data and 'problem_statement' in new_data['3_presentation']:
                new_data['3_presentation']['problem_statement'] += image_md
            print(f"  ↳ 🖼️ 이미지 임베딩 성공 ({img_filename})")
        except Exception as e:
            print(f"  ↳ ⚠️ 이미지 생성 실패: {e}")

    def _normalize_latex(self, text):
        if not text: return text
        text = re.sub(r'\\\((.*?)\\\)', r'$\1$', text)
        text = re.sub(r'\\\[(.*?)\\\]', r'$$\1$$', text, flags=re.DOTALL)
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

    def process_new_variant(self, year, exam, p_id, mode=MODE_MOCK, drill_level=None):
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
        base_prompt, selected_log_theme = self._build_prompt(md_text, perfect_seed, TargetSolver, metadata, mode, drill_level)
        dna_tag = getattr(TargetSolver, 'DNA', {}).get('specific_tag', '')
        print(f"🎲 [{year} {exam} {p_id}] DNA: {dna_tag} | 시드: {perfect_seed}")
        
        new_data, attempt = self._run_llm_generation_loop(base_prompt, perfect_seed, dna_tag)
        if not new_data:
            print(f"❌ [{p_id}] {MAX_LLM_RETRIES}회 재시도 후 생성 실패")
            return False

        # 4. 최종 검증 및 후처리
        if not self._verify_solver_solution(TargetSolver, new_data, perfect_seed):
            print("❌ Solver 실행 결과 불일치")
            return False

        self._handle_image_generation(TargetSolver, seed_key, year, exam, p_id, new_data)
        self._normalize_latex_in_response(new_data)

        # 5. DB 저장
        self._save_to_db(new_data, year, exam, p_id, selected_log_theme, seed_key, attempt, mode, drill_level)
        print(f"✅ 생성 성공 (정답: {perfect_seed['expected_t']})")
        return new_data

    def _save_to_db(self, data, year, exam, p_id, theme_name, seed_key, attempt_count, mode, drill_level):
        engine_id = self._get_engine_id(year, exam, p_id)
        pres = data.get('3_presentation', {})
        payload = data.get('4_solver_payload', {})
        sol = data.get('5_solution', {})
        meta_theme = data.get('2_generation_metadata', {}).get('problem_style', theme_name)
        
        # Extract focus for drills if available
        drill_focus = data.get('2_generation_metadata', {}).get('drill_focus')

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 1. Ensure engine exists or at least has a placeholder
            cursor.execute("INSERT OR IGNORE INTO engines (engine_id) VALUES (?)", (engine_id,))
            
            # 2. Save to V3 variants table
            query_v3 = """
                INSERT INTO variants
                (engine_id, mode, drill_level, drill_focus, narrative, variables_json,
                 solution_json, correct_answer, theme_name, seed_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query_v3, (
                engine_id, mode, drill_level, drill_focus,
                pres.get('problem_statement'),
                json.dumps(payload),
                json.dumps(sol.get('step_by_step')),
                str(payload.get('expected_t')),
                meta_theme,
                seed_key
            ))
            
            # 3. Save to Legacy table (optional, for safety)
            query_legacy = """
                INSERT INTO generated_problems
                (exam_year, exam_type, problem_num, narrative, variables,
                 solution_steps, correct_answer, theme, seed_key, attempt_count, problem_mode, drill_level)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(query_legacy, (
                year, exam, p_id,
                pres.get('problem_statement'),
                json.dumps(payload),
                json.dumps(sol.get('step_by_step')),
                payload.get('expected_t'),
                meta_theme,
                seed_key,
                attempt_count,
                mode,
                drill_level
            ))
            conn.commit()

    def get_random_variant(self, year, exam, p_id, mode=MODE_MOCK, drill_level=None):
        """DB에서 조건에 맞는 무작위 변형 문항 하나를 가져옵니다 (V3 Schema)."""
        engine_id = self._get_engine_id(year, exam, p_id)
        query = """
            SELECT narrative, variables_json, solution_json, correct_answer, theme_name, seed_key
            FROM variants
            WHERE engine_id = ? AND mode = ?
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
                "2_generation_metadata": {"problem_style": row["theme_name"]},
                "3_presentation": {"problem_statement": row["narrative"]},
                "4_solver_payload": json.loads(row["variables_json"]),
                "5_solution": {"step_by_step": solution_steps}
            }


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
            if factory.process_new_variant(year, exam, p_id, mode, level):
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