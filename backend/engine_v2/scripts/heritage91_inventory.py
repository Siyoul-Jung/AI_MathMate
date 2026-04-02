"""
AI_MathMate V2 — Heritage 91 Inventory (Standardized)
파일 시스템 정밀 감사 결과(deep_audit)를 반영하여 실제 파일 내 ID와 1:1 매핑된 91개 리스트입니다.
"""

# Batch 1~4 (기존 55개 모듈 - 실제 파일 내 ID 적용)
BATCH_EXISTING = [
    # Algebra (15)
    ("algebra_absolute_value", "algebra/algebra_absolute_value.py"),
    ("algebra_basic_manipulation", "algebra/algebra_basic_manipulation.py"),
    ("algebra_binomial_theorem", "algebra/algebra_binomial_theorem.py"),
    ("algebra_complex_numbers", "algebra/algebra_complex_numbers.py"),
    ("algebra_floor_ceiling_functions", "algebra/algebra_floor_ceiling_functions.py"),
    ("algebra_functions_and_properties", "algebra/algebra_functions_and_properties.py"),
    ("algebra_inequalities", "algebra/algebra_inequalities.py"),
    ("algebra_kinematics", "algebra/algebra_kinematics.py"),
    ("algebra_logarithms_exponents", "algebra/algebra_logarithms_exponents.py"),
    ("algebra_matrices_determinants", "algebra/algebra_matrices_determinants.py"),
    ("algebra_polynomials_vieta", "algebra/algebra_polynomials_vieta.py"),
    ("algebra_sequences_series_recurrence", "algebra/algebra_sequences_series_recurrence.py"),
    ("algebra_statistics", "algebra/algebra_statistics.py"),
    ("algebra_systems_of_equations", "algebra/algebra_systems_of_equations.py"),
    ("algebra_trigonometry", "algebra/algebra_trigonometry.py"),
    
    # Geometry (16)
    ("geometry_angle_bisector_theorem", "geometry/geometry_angle_bisector_theorem.py"),
    ("geometry_area_and_volume", "geometry/geometry_area_and_volume.py"),
    ("geometry_circles_tangency", "geometry/geometry_circles_tangency.py"),
    ("geometry_circle_theorems", "geometry/geometry_circle_theorems.py"),
    ("geometry_complex_numbers_in_geometry", "geometry/geometry_complex_numbers_in_geometry.py"),
    ("geometry_coordinate_analytic", "geometry/geometry_coordinate_analytic.py"),
    ("geometry_cyclic_quadrilaterals", "geometry/geometry_cyclic_quadrilaterals.py"),
    ("geometry_locus", "geometry/geometry_locus.py"),
    ("geometry_polygons", "geometry/geometry_polygons.py"),
    ("geometry_power_of_a_point", "geometry/geometry_power_of_a_point.py"),
    ("geometry_solid_3d", "geometry/geometry_solid_3d.py"),
    ("geometry_transformations", "geometry/geometry_transformations.py"),
    ("geometry_triangle_centers", "geometry/geometry_triangle_centers.py"),
    ("geometry_triangle_properties", "geometry/geometry_triangle_properties.py"),
    ("geometry_trigonometry_laws", "geometry/geometry_trigonometry_laws.py"),
    ("geometry_vectors", "geometry/geometry_vectors.py"),

    # Number Theory (10)
    ("nt_base_representation_and_digits", "number_theory/nt_base_representation_and_digits.py"),
    ("nt_chinese_remainder_theorem", "number_theory/nt_chinese_remainder_theorem.py"),
    ("nt_diophantine_equations", "number_theory/nt_diophantine_equations.py"),
    ("nt_divisibility_and_primes", "number_theory/nt_divisibility_and_primes.py"),
    ("nt_divisor_functions", "number_theory/nt_divisor_functions.py"),
    ("nt_frobenius_coin_problem", "number_theory/nt_frobenius_coin_problem.py"),
    ("nt_gcd_lcm", "number_theory/nt_gcd_lcm.py"),
    ("nt_modular_arithmetic", "number_theory/nt_modular_arithmetic.py"),
    ("nt_order_and_primitive_roots", "number_theory/nt_order_and_primitive_roots.py"),
    ("nt_perfect_powers", "number_theory/nt_perfect_powers.py"),

    # Combinatorics (14)
    ("comb_basic_counting", "combinatorics/comb_basic_counting.py"),
    ("comb_constrained_arrangements", "combinatorics/comb_constrained_arrangements.py"),
    ("comb_distributions_partitions", "combinatorics/comb_distributions_partitions.py"),
    ("comb_expected_value", "combinatorics/comb_expected_value.py"),
    ("comb_game_theory", "combinatorics/comb_game_theory.py"),
    ("comb_geometric_probability", "combinatorics/comb_geometric_probability.py"),
    ("comb_graph_theory", "combinatorics/comb_graph_theory.py"),
    ("comb_inclusion_exclusion", "combinatorics/comb_inclusion_exclusion.py"),
    ("comb_pigeonhole_principle", "combinatorics/comb_pigeonhole_principle.py"),
    ("comb_probability", "combinatorics/comb_probability.py"),
    ("comb_recursion_dp", "combinatorics/comb_recursion_dp.py"),
    ("comb_set_theory_and_subsets", "combinatorics/comb_set_theory_and_subsets.py"),
    ("comb_symmetry_and_burnside", "combinatorics/comb_symmetry_and_burnside.py"),
    ("comb_path_counting", "combinatorics/comb_path_counting.py"),
]

# Batch 5: Meta-Logic (8)
BATCH_5 = [
    ("meta_trace_removal", "meta/meta_trace_removal.py"),
    ("meta_symmetry_breaker", "meta/meta_symmetry_breaker.py"),
    ("meta_logic_concealer", "meta/meta_logic_concealer.py"),
    ("meta_rosetta_mapping", "meta/meta_rosetta_mapping.py"),
    ("meta_rationale_layering", "meta/meta_rationale_layering.py"),
    ("meta_invariant_design", "meta/meta_invariant_design.py"),
    ("meta_extremal_construction", "meta/meta_extremal_construction.py"),
    ("meta_anonymization", "meta/meta_anonymization.py"),
]

# Batch 6: Advanced Math (28)
BATCH_6 = [
    ("algebra_poly_vieta_newton", "algebra/algebra_poly_vieta_newton.py"),
    ("algebra_poly_complex_roots", "algebra/algebra_poly_complex_roots.py"),
    ("algebra_func_symmetry", "algebra/algebra_func_symmetry.py"),
    ("algebra_func_equations_cauchy", "algebra/algebra_func_equations_cauchy.py"),
    ("algebra_seq_characteristic_eq", "algebra/algebra_seq_characteristic_eq.py"),
    ("algebra_telescoping_sum", "algebra/algebra_telescoping_sum.py"),
    ("algebra_roots_unity_filter", "algebra/algebra_roots_unity_filter.py"),
    
    ("geometry_sim_spiral", "geometry/geometry_sim_spiral.py"),
    ("geometry_sim_homothety", "geometry/geometry_sim_homothety.py"),
    ("geometry_center_euler_ninepoint", "geometry/geometry_center_euler_ninepoint.py"),
    ("geometry_circle_isogonal_symmedian", "geometry/geometry_circle_isogonal_symmedian.py"),
    ("geometry_circle_radical", "geometry/geometry_circle_radical.py"),
    ("geometry_circle_ptolemy", "geometry/geometry_circle_ptolemy.py"),
    ("geometry_transform_inversion", "geometry/geometry_transform_inversion.py"),
    
    ("nt_mod_order_primitive", "number_theory/nt_mod_order_primitive.py"),
    ("nt_mod_lte_lemma", "number_theory/nt_mod_lte_lemma.py"),
    ("nt_diophantine_pell", "number_theory/nt_diophantine_pell.py"),
    ("nt_diophantine_vieta_jumping", "number_theory/nt_diophantine_vieta_jumping.py"),
    ("nt_floor_legendre", "number_theory/nt_floor_legendre.py"),
    ("nt_discrete_log", "number_theory/nt_discrete_log.py"),
    ("nt_quadratic_residue", "number_theory/nt_quadratic_residue.py"),
    
    ("comb_gen_func_snake_oil", "combinatorics/comb_gen_func_snake_oil.py"),
    ("comb_prob_absorbing_markov", "combinatorics/comb_prob_absorbing_markov.py"),
    ("comb_prob_transition_matrix", "combinatorics/comb_prob_transition_matrix.py"),
    ("comb_count_double", "combinatorics/comb_count_double.py"),
    ("comb_catalan", "combinatorics/comb_catalan.py"),
    ("comb_derangement", "combinatorics/comb_derangement.py"),
    ("comb_graph_coloring_chromatic", "combinatorics/comb_graph_coloring_chromatic.py"),
]

ALL_HERITAGE_91 = BATCH_EXISTING + BATCH_5 + BATCH_6

if __name__ == "__main__":
    print(f"Total: {len(ALL_HERITAGE_91)}")
