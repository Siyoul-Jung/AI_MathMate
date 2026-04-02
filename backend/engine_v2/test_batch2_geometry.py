import sys
import math
import os
from pathlib import Path

# backend 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent))

from engine_v2.modules.geometry.geometry_lines_angles_triangles import GeometryLinesAnglesTrianglesModule
from engine_v2.modules.geometry.geometry_circle_properties import GeometryCirclePropertiesModule
from engine_v2.modules.geometry.geometry_circles_tangency import GeometryCirclesTangencyModule
from engine_v2.modules.geometry.geometry_quadrilaterals import GeometryQuadrilateralsModule
from engine_v2.modules.geometry.geometry_polygons_properties import GeometryPolygonsPropertiesModule
from engine_v2.modules.geometry.geometry_area_and_volume import GeometryAreaAndVolumeModule
from engine_v2.modules.geometry.geometry_coordinate_geometry import GeometryCoordinateGeometryModule
from engine_v2.modules.geometry.geometry_three_dimensional_geometry import GeometryThreeDimensionalGeometryModule
from engine_v2.modules.geometry.geometry_vectors_transformations import GeometryVectorsTransformationsModule
from engine_v2.modules.geometry.geometry_trigonometry_in_geometry import GeometryTrigonometryInGeometryModule
from engine_v2.modules.geometry.geometry_power_of_a_point import GeometryPowerOfAPointModule
from engine_v2.modules.geometry.geometry_stewarts_theorem import GeometryStewartsTheoremModule
from engine_v2.modules.geometry.geometry_ceva_menelaus import GeometryCevaMenelausModule
from engine_v2.modules.geometry.geometry_circumcircle_incircle import GeometryCircumcircleIncircleModule
from engine_v2.modules.geometry.geometry_geometry_logic_proof import GeometryGeometryLogicProofModule
from engine_v2.modules.geometry.geometry_conics_and_loci import GeometryConicsAndLociModule

modules = [
    GeometryLinesAnglesTrianglesModule(),
    GeometryCirclePropertiesModule(),
    GeometryCirclesTangencyModule(),
    GeometryQuadrilateralsModule(),
    GeometryPolygonsPropertiesModule(),
    GeometryAreaAndVolumeModule(),
    GeometryCoordinateGeometryModule(),
    GeometryThreeDimensionalGeometryModule(),
    GeometryVectorsTransformationsModule(),
    GeometryTrigonometryInGeometryModule(),
    GeometryPowerOfAPointModule(),
    GeometryStewartsTheoremModule(),
    GeometryCevaMenelausModule(),
    GeometryCircumcircleIncircleModule(),
    GeometryGeometryLogicProofModule(),
    GeometryConicsAndLociModule()
]

output_file = "backend/engine_v2/test_batch2_geometry_output.txt"

with open(output_file, "w", encoding="utf-8") as f:
    f.write("=== Batch 2 (Geometry) 16 Modules Full Test ===\n\n")
    for m in modules:
        f.write(f"[{m.META.name}] ({m.META.module_id})\n")
        try:
            for i in range(5):
                seed = m.generate_seed(difficulty_hint=10.0 + i)
                answer = m.execute(seed)
                valid_ans, reason_ans = m.validate_answer(answer)
                f.write(f"  Trial {i+1}: Seed={seed}, Ans={answer} ({'✅' if valid_ans else '❌'})\n")
            f.write("-" * 50 + "\n")
        except Exception as e:
            f.write(f"  ❌ ALERT: Error in module: {e}\n")
            f.write("-" * 50 + "\n")

print(f"Test completed. Results saved to {output_file}")
