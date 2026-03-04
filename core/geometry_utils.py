import math

class GeometryUtils:
    """기하 문제에 필요한 SVG 이미지를 생성하는 유틸리티"""

    @staticmethod
    def create_number_line_svg(a, b, highlight_points=None):
        """
        수직선 SVG 생성
        a, b: 수직선 표시 범위 (min, max)
        highlight_points: {좌표: 라벨} 딕셔너리 (예: {-2: 'A', 3: 'B'})
        """
        if highlight_points is None:
            highlight_points = {}
            
        width = 500
        height = 100
        padding = 50
        
        # 범위 보정 (여유 공간 확보)
        points = list(highlight_points.keys()) + [a, b]
        min_val = min(points) - 1
        max_val = max(points) + 1
        range_len = max_val - min_val
        
        # 좌표 변환 함수 (값 -> 픽셀 x좌표)
        def get_x(val):
            return padding + (val - min_val) / range_len * (width - 2 * padding)

        svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        
        # 메인 라인 및 화살표
        y = height / 2
        svg += f'<line x1="{padding-10}" y1="{y}" x2="{width-padding+10}" y2="{y}" stroke="black" stroke-width="2" marker-end="url(#arrow)" marker-start="url(#arrow-rev)" />'
        svg += f'<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="black" /></marker></defs>'
        svg += f'<defs><marker id="arrow-rev" markerWidth="10" markerHeight="10" refX="1" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M9,0 L9,6 L0,3 z" fill="black" /></marker></defs>'

        # 눈금 및 숫자 (정수 단위)
        step = 1 if range_len <= 20 else 5 # 범위가 넓으면 5단위로 표시
        for i in range(int(min_val), int(max_val) + 1):
            if i % step == 0:
                x = get_x(i)
                svg += f'<line x1="{x}" y1="{y-5}" x2="{x}" y2="{y+5}" stroke="black" stroke-width="1" />'
                svg += f'<text x="{x}" y="{y+25}" font-size="12" text-anchor="middle" fill="#666">{i}</text>'

        # 강조 점 (빨간색 점 및 라벨)
        for val, label in highlight_points.items():
            x = get_x(val)
            svg += f'<circle cx="{x}" cy="{y}" r="5" fill="#ef4444" />'
            svg += f'<text x="{x}" y="{y-15}" font-size="16" font-weight="bold" fill="#ef4444" text-anchor="middle">{label}</text>'

        svg += '</svg>'
        return svg

    @staticmethod
    def create_cube_svg():
        """정육면체 SVG 생성 (겨냥도)"""
        width = 300
        height = 250
        
        # 꼭짓점 좌표 정의 (A~H)
        # 앞면: A(TopL), B(TopR), C(BotR), D(BotL)
        # 뒷면: E(TopL), F(TopR), G(BotR), H(BotL)
        v = {
            'A': (50, 80),  'B': (150, 80),  'C': (150, 180), 'D': (50, 180),
            'E': (100, 40), 'F': (200, 40),  'G': (200, 140), 'H': (100, 140)
        }
        
        svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: bold 16px sans-serif; fill: #333; } .solid { stroke: black; stroke-width: 2; fill: none; } .dashed { stroke: black; stroke-width: 2; stroke-dasharray: 5,5; fill: none; }</style>'
        
        # 실선 (Visible Lines)
        # 앞면 사각형 ABCD
        svg += f'<path d="M{v["A"][0]},{v["A"][1]} L{v["B"][0]},{v["B"][1]} L{v["C"][0]},{v["C"][1]} L{v["D"][0]},{v["D"][1]} Z" class="solid" />'
        # 뒷면 연결 (B-F, C-G, F-G, E-F, A-E) - H는 숨겨짐
        svg += f'<path d="M{v["B"][0]},{v["B"][1]} L{v["F"][0]},{v["F"][1]} L{v["G"][0]},{v["G"][1]} L{v["C"][0]},{v["C"][1]}" class="solid" />'
        svg += f'<path d="M{v["F"][0]},{v["F"][1]} L{v["E"][0]},{v["E"][1]} L{v["A"][0]},{v["A"][1]}" class="solid" />'
        
        # 점선 (Hidden Lines - H 연결)
        svg += f'<path d="M{v["E"][0]},{v["E"][1]} L{v["H"][0]},{v["H"][1]} L{v["G"][0]},{v["G"][1]}" class="dashed" />'
        svg += f'<path d="M{v["D"][0]},{v["D"][1]} L{v["H"][0]},{v["H"][1]}" class="dashed" />'
        
        # 라벨 표시
        for label, (x, y) in v.items():
            # 라벨 위치 미세 조정
            dx, dy = -15, -5
            if label in ['B', 'C', 'F', 'G']: dx = 10
            if label in ['C', 'D', 'G', 'H']: dy = 15
            svg += f'<text x="{x+dx}" y="{y+dy}" class="label">{label}</text>'
            
        svg += '</svg>'
        return svg

    @staticmethod
    def create_congruent_triangles_svg(a, b, c, labels1=None, labels2=None):
        """
        합동인 두 삼각형 SVG 생성 (나란히 배치)
        """
        if labels1 is None: labels1 = {'A': 'A', 'B': 'B', 'C': 'C'}
        if labels2 is None: labels2 = {'D': 'D', 'E': 'E', 'F': 'F'}
        
        try:
            cosC = (a**2 + b**2 - c**2) / (2 * a * b)
            sinC = math.sqrt(1 - cosC**2)
        except ValueError:
            return None

        # 두 개를 그려야 하므로 스케일 조정 (조금 작게)
        scale = 150 / max(a, b, c)
        
        # Triangle 1 (Left)
        cx1, cy1 = 0, 0
        bx1, by1 = a * scale, 0
        ax1, ay1 = b * scale * cosC, b * scale * sinC
        
        # Triangle 2 (Right) - x축으로 이동
        offset_x = a * scale + 80 # 간격 확보
        cx2, cy2 = offset_x, 0
        bx2, by2 = offset_x + a * scale, 0
        ax2, ay2 = offset_x + b * scale * cosC, b * scale * sinC
        
        padding_x, padding_y = 40, 180
        width = int(offset_x + a * scale + padding_x * 2)
        
        svg = f'<svg width="{width}" height="220" viewBox="0 0 {width} 220" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: bold 16px sans-serif; fill: #333; }</style>'
        
        # Draw T1
        p1 = {
            'C': (padding_x + cx1, padding_y - cy1),
            'B': (padding_x + bx1, padding_y - by1),
            'A': (padding_x + ax1, padding_y - ay1)
        }
        svg += f'<polygon points="{p1["A"][0]},{p1["A"][1]} {p1["B"][0]},{p1["B"][1]} {p1["C"][0]},{p1["C"][1]}" fill="none" stroke="black" stroke-width="2" />'
        
        # Draw T2
        p2 = {
            'F': (padding_x + cx2, padding_y - cy2),
            'E': (padding_x + bx2, padding_y - by2),
            'D': (padding_x + ax2, padding_y - ay2)
        }
        svg += f'<polygon points="{p2["D"][0]},{p2["D"][1]} {p2["E"][0]},{p2["E"][1]} {p2["F"][0]},{p2["F"][1]}" fill="none" stroke="black" stroke-width="2" />'
        
        # Labels Helper
        def draw_labels(points, lbls):
            res = ""
            center_x = sum(pt[0] for pt in points.values()) / 3
            center_y = sum(pt[1] for pt in points.values()) / 3
            for key, (x, y) in points.items():
                label = lbls.get(key, key)
                dx = (x - center_x) * 0.35
                dy = (y - center_y) * 0.35
                res += f'<text x="{x+dx}" y="{y+dy}" class="label" text-anchor="middle" dominant-baseline="middle">{label}</text>'
            return res

        svg += draw_labels(p1, labels1)
        svg += draw_labels(p2, labels2)

        svg += '</svg>'
        return svg

    @staticmethod
    def create_triangle_svg(a, b, c, labels=None):
        """
        세 변의 길이 a, b, c로 삼각형 SVG 생성
        labels: {'A': 'A', 'B': 'B', 'C': 'C'} 형태의 꼭짓점 라벨
        """
        if labels is None:
            labels = {'A': 'A', 'B': 'B', 'C': 'C'}
            
        # 코사인 법칙으로 좌표 계산 (A를 원점으로 가정했다가 이동)
        # C = (0, 0), B = (a, 0)
        # A = (b*cosC, b*sinC)
        # cosC = (a^2 + b^2 - c^2) / (2ab)
        
        try:
            cosC = (a**2 + b**2 - c**2) / (2 * a * b)
            sinC = math.sqrt(1 - cosC**2)
        except ValueError:
            return None # 삼각형 성립 안함
            
        # 좌표 설정 (화면 중앙 배치를 위해 스케일링 및 이동)
        scale = 200 / max(a, b, c)
        cx, cy = 0, 0
        bx, by = a * scale, 0
        ax, ay = b * scale * cosC, b * scale * sinC
        
        # SVG 좌표계 (y축 반전) 및 여백
        padding_x, padding_y = 50, 200
        points = {
            'C': (padding_x + cx, padding_y - cy),
            'B': (padding_x + bx, padding_y - by),
            'A': (padding_x + ax, padding_y - ay)
        }
        
        svg = f'<svg width="300" height="250" viewBox="0 0 300 250" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: bold 16px sans-serif; fill: #333; }</style>'
        svg += f'<polygon points="{points["A"][0]},{points["A"][1]} {points["B"][0]},{points["B"][1]} {points["C"][0]},{points["C"][1]}" fill="none" stroke="black" stroke-width="2" />'
        
        # 라벨
        for p, (x, y) in points.items():
            label = labels.get(p, p)
            # 라벨 위치 미세 조정 (중심에서 바깥쪽으로)
            center_x = (points['A'][0] + points['B'][0] + points['C'][0]) / 3
            center_y = (points['A'][1] + points['B'][1] + points['C'][1]) / 3
            dx = (x - center_x) * 0.2
            dy = (y - center_y) * 0.2
            svg += f'<text x="{x+dx}" y="{y+dy}" class="label" text-anchor="middle" dominant-baseline="middle">{label}</text>'
            
        svg += '</svg>'
        return svg

    @staticmethod
    def create_regular_polygon_svg(num_sides, radius=80, center_x=150, center_y=125, labels=None):
        """
        정N각형 SVG 생성
        num_sides: 변의 개수 (3 이상)
        radius: 외접원의 반지름
        center_x, center_y: 중심 좌표
        labels: 꼭짓점 라벨 (예: ['A', 'B', 'C'])
        """
        if num_sides < 3:
            return ""

        points_str = ""
        vertices = []
        for i in range(num_sides):
            angle = 2 * math.pi * i / num_sides - math.pi / 2 # 위쪽 꼭짓점부터 시작
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            vertices.append((x, y))
            points_str += f"{x},{y} "

        svg = f'<svg width="300" height="250" viewBox="0 0 300 250" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: bold 16px sans-serif; fill: #333; } .solid { stroke: black; stroke-width: 2; fill: none; }</style>'
        
        # 다각형 그리기
        svg += f'<polygon points="{points_str.strip()}" class="solid" />'
        
        # 꼭짓점 라벨
        if labels:
            for i, (x, y) in enumerate(vertices):
                if i < len(labels):
                    label = labels[i]
                    # 라벨 위치 미세 조정 (꼭짓점에서 약간 바깥쪽으로)
                    dx = (x - center_x) * 0.15
                    dy = (y - center_y) * 0.15
                    svg += f'<text x="{x+dx}" y="{y+dy}" class="label" text-anchor="middle" dominant-baseline="middle">{label}</text>'

        svg += '</svg>'
        return svg

    @staticmethod
    def create_coordinate_plane_svg(points=None, lines=None, polygons=None, x_range=None, y_range=None, width=300, height=300, grid=True):
        """
        좌표평면 SVG 생성
        points: [(x, y, label), ...] or {'label': (x, y)}
        lines: [((x1, y1), (x2, y2)), ...]
        polygons: [[(x1, y1), (x2, y2), ...], ...]
        """
        if points is None: points = []
        if lines is None: lines = []
        if polygons is None: polygons = []
        
        # Normalize points list
        point_list = []
        if isinstance(points, dict):
            for label, coord in points.items():
                point_list.append((coord[0], coord[1], label))
        elif isinstance(points, list):
            for p in points:
                if len(p) == 3: point_list.append(p)
                else: point_list.append((p[0], p[1], ""))
        
        # Auto-range if not provided
        all_x = [p[0] for p in point_list] + [p[0] for l in lines for p in l] + [p[0] for poly in polygons for p in poly]
        all_y = [p[1] for p in point_list] + [p[1] for l in lines for p in l] + [p[1] for poly in polygons for p in poly]
        
        if not all_x: all_x = [0]
        if not all_y: all_y = [0]
        
        if x_range is None:
            x_min, x_max = min(all_x), max(all_x)
            margin_x = max(1, (x_max - x_min) * 0.2)
            x_range = (x_min - margin_x, x_max + margin_x)
            
        if y_range is None:
            y_min, y_max = min(all_y), max(all_y)
            margin_y = max(1, (y_max - y_min) * 0.2)
            y_range = (y_min - margin_y, y_max + margin_y)

        svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.axis { stroke: black; stroke-width: 2; } .grid { stroke: #eee; stroke-width: 1; } .label { font: bold 14px sans-serif; fill: #333; } .point { fill: #ef4444; } .poly { fill: rgba(59, 130, 246, 0.2); stroke: #3b82f6; stroke-width: 2; } .line { stroke: #3b82f6; stroke-width: 2; }</style>'
        
        x_min, x_max = x_range
        y_min, y_max = y_range
        
        # Ensure 0 is included for axes
        if x_min > 0: x_min = -1
        if x_max < 0: x_max = 1
        if y_min > 0: y_min = -1
        if y_max < 0: y_max = 1
        
        padding = 20
        draw_width = width - 2 * padding
        draw_height = height - 2 * padding
        
        def map_x(x): return padding + (x - x_min) / (x_max - x_min) * draw_width
        def map_y(y): return height - (padding + (y - y_min) / (y_max - y_min) * draw_height)

        # Grid & Axes
        origin_x, origin_y = map_x(0), map_y(0)
        
        svg += f'<line x1="0" y1="{origin_y}" x2="{width}" y2="{origin_y}" class="axis" />'
        svg += f'<text x="{width-15}" y="{origin_y+15}" class="label">x</text>'
        svg += f'<line x1="{origin_x}" y1="0" x2="{origin_x}" y2="{height}" class="axis" />'
        svg += f'<text x="{origin_x+5}" y="15" class="label">y</text>'
        svg += f'<text x="{origin_x-15}" y="{origin_y+15}" class="label">O</text>'
        
        for poly in polygons:
            points_str = " ".join([f"{map_x(p[0])},{map_y(p[1])}" for p in poly])
            svg += f'<polygon points="{points_str}" class="poly" />'

        for p1, p2 in lines:
            svg += f'<line x1="{map_x(p1[0])}" y1="{map_y(p1[1])}" x2="{map_x(p2[0])}" y2="{map_y(p2[1])}" class="line" />'

        for x, y, label in point_list:
            svg += f'<circle cx="{map_x(x)}" cy="{map_y(y)}" r="4" class="point" />'
            if label: svg += f'<text x="{map_x(x)+5}" y="{map_y(y)-5}" class="label">{label}</text>'

        svg += '</svg>'
        return svg

    @staticmethod
    def create_sector_svg(radius=80, angle=60, center_x=150, center_y=125, labels=None):
        """
        부채꼴(또는 원) SVG 생성
        angle: 중심각 (도). 360이면 원.
        """
        if labels is None: labels = {}
        
        svg = f'<svg width="300" height="250" viewBox="0 0 300 250" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: bold 16px sans-serif; fill: #333; } .solid { stroke: black; stroke-width: 2; fill: rgba(59, 130, 246, 0.1); } .line { stroke: black; stroke-width: 2; }</style>'
        
        # 중심점
        svg += f'<circle cx="{center_x}" cy="{center_y}" r="3" fill="black" />'
        svg += f'<text x="{center_x-15}" y="{center_y+5}" class="label">O</text>'
        
        if angle >= 360:
            # 전체 원
            svg += f'<circle cx="{center_x}" cy="{center_y}" r="{radius}" class="solid" />'
        else:
            # 부채꼴 (0도(3시 방향)에서 시작하여 반시계 방향으로 angle만큼)
            # SVG 좌표계: y가 아래로 증가하므로, 반시계 방향은 y좌표 계산 시 -sin 사용
            start_rad = 0
            end_rad = math.radians(angle)
            
            start_x = center_x + radius
            start_y = center_y
            
            end_x = center_x + radius * math.cos(-end_rad)
            end_y = center_y + radius * math.sin(-end_rad)
            
            large_arc_flag = 1 if angle > 180 else 0
            
            # 부채꼴 경로: 중심 -> 시작점 -> 아크 -> 끝점 -> 중심
            d = f"M {center_x} {center_y} L {start_x} {start_y} A {radius} {radius} 0 {large_arc_flag} 0 {end_x} {end_y} Z"
            svg += f'<path d="{d}" class="solid" />'
            
            # 라벨 표시 (반지름 r, 각도 x)
            if 'r' in labels:
                svg += f'<text x="{center_x + radius/2}" y="{center_y + 20}" class="label" text-anchor="middle">{labels["r"]}</text>'
            if 'x' in labels:
                # 각도 라벨 위치 (각의 이등분선 방향)
                mid_rad = -end_rad / 2
                lx = center_x + 30 * math.cos(mid_rad)
                ly = center_y + 30 * math.sin(mid_rad)
                svg += f'<text x="{lx}" y="{ly}" class="label" text-anchor="middle" dominant-baseline="middle">{labels["x"]}</text>'

        svg += '</svg>'
        return svg

    @staticmethod
    def create_cylinder_svg(radius=60, height=120, center_x=150, center_y=125, labels=None):
        """원기둥 SVG 생성"""
        if labels is None: labels = {}
        
        svg = f'<svg width="300" height="250" viewBox="0 0 300 250" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: 14px sans-serif; fill: #333; } .face { stroke: black; stroke-width: 1.5; fill: #fff; fill-opacity: 0.8; } .line { stroke: black; stroke-width: 1.5; fill: none; } .dashed { stroke: black; stroke-width: 1.5; stroke-dasharray: 4,4; fill: none; } .dim { stroke: #666; stroke-width: 1; } .center { fill: black; } .angle { fill: none; stroke: #ef4444; stroke-width: 2; }</style>'
        
        top_y = center_y - height/2
        bottom_y = center_y + height/2
        ry = radius / 3
        
        # 아랫면 (반타원 점선 - 뒤쪽)
        svg += f'<path d="M {center_x-radius} {bottom_y} A {radius} {ry} 0 0 1 {center_x+radius} {bottom_y}" class="dashed" />'
        
        # 아랫면 (반타원 실선 - 앞쪽)
        svg += f'<path d="M {center_x-radius} {bottom_y} A {radius} {ry} 0 0 0 {center_x+radius} {bottom_y}" class="line" />'
        
        # 옆면 (직선)
        svg += f'<line x1="{center_x-radius}" y1="{top_y}" x2="{center_x-radius}" y2="{bottom_y}" class="line" />'
        svg += f'<line x1="{center_x+radius}" y1="{top_y}" x2="{center_x+radius}" y2="{bottom_y}" class="line" />'
        
        # 윗면 (타원)
        svg += f'<ellipse cx="{center_x}" cy="{top_y}" rx="{radius}" ry="{ry}" class="face" />'
        
        # 중심점
        svg += f'<circle cx="{center_x}" cy="{top_y}" r="2" class="center" />'
        
        # 라벨 (높이 h)
        if 'h' in labels:
            dim_x = center_x + radius + 20
            # 보조선
            svg += f'<line x1="{center_x+radius}" y1="{top_y}" x2="{dim_x+5}" y2="{top_y}" class="dim" stroke-dasharray="2,2" />'
            svg += f'<line x1="{center_x+radius}" y1="{bottom_y}" x2="{dim_x+5}" y2="{bottom_y}" class="dim" stroke-dasharray="2,2" />'
            # 수직선 (화살표 대신 끝에 짧은 가로선)
            svg += f'<line x1="{dim_x}" y1="{top_y}" x2="{dim_x}" y2="{bottom_y}" class="dim" />'
            svg += f'<line x1="{dim_x-3}" y1="{top_y}" x2="{dim_x+3}" y2="{top_y}" class="dim" />'
            svg += f'<line x1="{dim_x-3}" y1="{bottom_y}" x2="{dim_x+3}" y2="{bottom_y}" class="dim" />'
            
            svg += f'<text x="{dim_x+5}" y="{center_y+5}" class="label">{labels["h"]}</text>'
            
        # 라벨 (반지름 r)
        if 'r' in labels:
            # 반지름 표시 (중심에서 오른쪽 끝까지)
            svg += f'<line x1="{center_x}" y1="{top_y}" x2="{center_x+radius}" y2="{top_y}" class="dim" />'
            # 양 끝 점
            svg += f'<circle cx="{center_x}" cy="{top_y}" r="2" class="center" />'
            svg += f'<text x="{center_x+radius/2}" y="{top_y-5}" class="label" text-anchor="middle">{labels["r"]}</text>'
            
        svg += '</svg>'
        return svg

    @staticmethod
    def create_cone_svg(radius=60, height=120, center_x=150, center_y=125, labels=None):
        """원뿔 SVG 생성"""
        if labels is None: labels = {}
        
        svg = f'<svg width="300" height="250" viewBox="0 0 300 250" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: 14px sans-serif; fill: #333; } .line { stroke: black; stroke-width: 1.5; fill: none; } .dashed { stroke: black; stroke-width: 1.5; stroke-dasharray: 4,4; fill: none; } .dim { stroke: #666; stroke-width: 1; } .center { fill: black; }</style>'
        
        # 꼭짓점 및 밑면 중심
        top_y = center_y - height/2
        bottom_y = center_y + height/2
        ry = radius / 3
        
        # 옆면 (삼각형 형태)
        svg += f'<line x1="{center_x}" y1="{top_y}" x2="{center_x-radius}" y2="{bottom_y}" class="line" />'
        svg += f'<line x1="{center_x}" y1="{top_y}" x2="{center_x+radius}" y2="{bottom_y}" class="line" />'
        
        # 밑면 (반타원 점선 - 뒤쪽)
        svg += f'<path d="M {center_x-radius} {bottom_y} A {radius} {ry} 0 0 1 {center_x+radius} {bottom_y}" class="dashed" />'
        
        # 밑면 (반타원 실선 - 앞쪽)
        svg += f'<path d="M {center_x-radius} {bottom_y} A {radius} {ry} 0 0 0 {center_x+radius} {bottom_y}" class="line" />'
        
        # 라벨
        if 'h' in labels:
            # 높이 표시 (내부 점선)
            svg += f'<line x1="{center_x}" y1="{top_y}" x2="{center_x}" y2="{bottom_y}" class="dashed" />'
            # 직각 표시
            svg += f'<polyline points="{center_x},{bottom_y-10} {center_x+10},{bottom_y-10} {center_x+10},{bottom_y}" class="dim" fill="none"/>'
            svg += f'<text x="{center_x+5}" y="{center_y}" class="label">{labels["h"]}</text>'
            
        if 'r' in labels:
            # 중심점
            svg += f'<line x1="{center_x}" y1="{bottom_y}" x2="{center_x+radius}" y2="{bottom_y}" class="dim" />'
            svg += f'<circle cx="{center_x}" cy="{bottom_y}" r="2" class="center" />'
            svg += f'<text x="{center_x+radius/2}" y="{bottom_y-5}" class="label" text-anchor="middle">{labels["r"]}</text>'
            
        svg += '</svg>'
        return svg

    @staticmethod
    def create_sphere_svg(radius=80, center_x=150, center_y=125, labels=None):
        """구 SVG 생성 (겨냥도)"""
        if labels is None: labels = {}
        
        svg = f'<svg width="300" height="250" viewBox="0 0 300 250" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: 14px sans-serif; fill: #333; } .line { stroke: black; stroke-width: 1.5; fill: none; } .dashed { stroke: black; stroke-width: 1.5; stroke-dasharray: 4,4; fill: none; } .center { fill: black; }</style>'
        
        # 구의 외곽선 (원)
        svg += f'<circle cx="{center_x}" cy="{center_y}" r="{radius}" class="line" />'
        
        # 입체감을 위한 타원 (적도)
        rx = radius
        ry = radius / 3
        
        # 뒤쪽 (점선)
        svg += f'<path d="M {center_x-rx} {center_y} A {rx} {ry} 0 0 1 {center_x+rx} {center_y}" class="dashed" />'
        # 앞쪽 (실선)
        svg += f'<path d="M {center_x-rx} {center_y} A {rx} {ry} 0 0 0 {center_x+rx} {center_y}" class="line" />'
        
        # 라벨 (반지름 r)
        if 'r' in labels:
            # 중심점
            svg += f'<circle cx="{center_x}" cy="{center_y}" r="2" fill="black" />'
            svg += f'<text x="{center_x-15}" y="{center_y+5}" class="label">O</text>'
            # 반지름 선 (실선으로 변경하여 명확하게)
            svg += f'<line x1="{center_x}" y1="{center_y}" x2="{center_x+radius}" y2="{center_y}" class="dim" />'
            # 라벨 위치 (선 위쪽)
            svg += f'<text x="{center_x+radius/2}" y="{center_y-5}" class="label" text-anchor="middle">{labels["r"]}</text>'
            
        svg += '</svg>'
        return svg

    @staticmethod
    def create_hemisphere_svg(radius=80, center_x=150, center_y=150, labels=None):
        """반구 SVG 생성 (겨냥도)"""
        if labels is None: labels = {}
        
        svg = f'<svg width="300" height="250" viewBox="0 0 300 250" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: 14px sans-serif; fill: #333; } .line { stroke: black; stroke-width: 1.5; fill: none; } .dashed { stroke: black; stroke-width: 1.5; stroke-dasharray: 4,4; fill: none; } .center { fill: black; }</style>'
        
        ry = radius / 3
        
        # 밑면 (뒤쪽 점선)
        svg += f'<path d="M {center_x-radius} {center_y} A {radius} {ry} 0 0 1 {center_x+radius} {center_y}" class="dashed" />'
        # 밑면 (앞쪽 실선)
        svg += f'<path d="M {center_x-radius} {center_y} A {radius} {ry} 0 0 0 {center_x+radius} {center_y}" class="line" />'
        
        # 위쪽 둥근 부분 (반원 아크)
        svg += f'<path d="M {center_x-radius} {center_y} A {radius} {radius} 0 0 1 {center_x+radius} {center_y}" class="line" />'
        
        # 중심점
        svg += f'<circle cx="{center_x}" cy="{center_y}" r="2" class="center" />'
        svg += f'<text x="{center_x-15}" y="{center_y+5}" class="label">O</text>'
        
        # 라벨 (반지름 r)
        if 'r' in labels:
            svg += f'<line x1="{center_x}" y1="{center_y}" x2="{center_x+radius}" y2="{center_y}" class="dim" />'
            svg += f'<text x="{center_x+radius/2}" y="{center_y-5}" class="label" text-anchor="middle">{labels["r"]}</text>'
            
        svg += '</svg>'
        return svg

    @staticmethod
    def create_hollow_cylinder_svg(r_out=80, r_in=40, height=120, center_x=150, center_y=125, labels=None):
        """구멍 뚫린 원기둥 SVG 생성"""
        if labels is None: labels = {}
        
        svg = f'<svg width="300" height="250" viewBox="0 0 300 250" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: 14px sans-serif; fill: #333; } .face { stroke: black; stroke-width: 1.5; fill: #fff; fill-opacity: 0.9; } .line { stroke: black; stroke-width: 1.5; fill: none; } .dashed { stroke: black; stroke-width: 1.5; stroke-dasharray: 4,4; fill: none; } .dim { stroke: #666; stroke-width: 1; } .center { fill: black; }</style>'
        
        top_y = center_y - height/2
        bottom_y = center_y + height/2
        ry_out = r_out / 3
        ry_in = r_in / 3
        
        # 아랫면 (바깥쪽 반타원 점선 - 뒤쪽)
        svg += f'<path d="M {center_x-r_out} {bottom_y} A {r_out} {ry_out} 0 0 1 {center_x+r_out} {bottom_y}" class="dashed" />'
        # 아랫면 (바깥쪽 반타원 실선 - 앞쪽)
        svg += f'<path d="M {center_x-r_out} {bottom_y} A {r_out} {ry_out} 0 0 0 {center_x+r_out} {bottom_y}" class="line" />'
        
        # 안쪽 구멍 바닥 (점선 - 전체 타원)
        svg += f'<ellipse cx="{center_x}" cy="{bottom_y}" rx="{r_in}" ry="{ry_in}" class="dashed" />'
        
        # 옆면 (직선)
        svg += f'<line x1="{center_x-r_out}" y1="{top_y}" x2="{center_x-r_out}" y2="{bottom_y}" class="line" />'
        svg += f'<line x1="{center_x+r_out}" y1="{top_y}" x2="{center_x+r_out}" y2="{bottom_y}" class="line" />'
        
        # 윗면 (도넛 모양)
        # path를 사용하여 구멍 뚫린 면을 표현 (fill-rule="evenodd")
        path_outer = f"M {center_x-r_out} {top_y} A {r_out} {ry_out} 0 1 0 {center_x+r_out} {top_y} A {r_out} {ry_out} 0 1 0 {center_x-r_out} {top_y} Z"
        path_inner = f"M {center_x-r_in} {top_y} A {r_in} {ry_in} 0 1 1 {center_x+r_in} {top_y} A {r_in} {ry_in} 0 1 1 {center_x-r_in} {top_y} Z"
        
        svg += f'<path d="{path_outer} {path_inner}" class="face" fill-rule="evenodd" />'
        
        # 안쪽 구멍의 내려가는 선 (점선)
        svg += f'<line x1="{center_x-r_in}" y1="{top_y}" x2="{center_x-r_in}" y2="{bottom_y}" class="dashed" />'
        svg += f'<line x1="{center_x+r_in}" y1="{top_y}" x2="{center_x+r_in}" y2="{bottom_y}" class="dashed" />'
        
        # 라벨
        if 'h' in labels:
            dim_x = center_x + r_out + 20
            svg += f'<line x1="{center_x+r_out}" y1="{top_y}" x2="{dim_x+5}" y2="{top_y}" class="dim" stroke-dasharray="2,2" />'
            svg += f'<line x1="{center_x+r_out}" y1="{bottom_y}" x2="{dim_x+5}" y2="{bottom_y}" class="dim" stroke-dasharray="2,2" />'
            svg += f'<line x1="{dim_x}" y1="{top_y}" x2="{dim_x}" y2="{bottom_y}" class="dim" />'
            svg += f'<text x="{dim_x+5}" y="{center_y+5}" class="label">{labels["h"]}</text>'
            
        if 'r_out' in labels:
            svg += f'<line x1="{center_x}" y1="{top_y}" x2="{center_x+r_out}" y2="{top_y}" class="dim" />'
            svg += f'<text x="{center_x+r_out/2 + 10}" y="{top_y-5}" class="label" text-anchor="middle">{labels["r_out"]}</text>'

        if 'r_in' in labels:
            # 안쪽 반지름은 왼쪽으로 표시하여 겹침 방지
            svg += f'<line x1="{center_x}" y1="{top_y}" x2="{center_x-r_in}" y2="{top_y}" class="dim" />'
            svg += f'<text x="{center_x-r_in/2}" y="{top_y-5}" class="label" text-anchor="middle">{labels["r_in"]}</text>'
            
        # 중심점
        svg += f'<circle cx="{center_x}" cy="{top_y}" r="2" class="center" />'
            
        svg += '</svg>'
        return svg

    @staticmethod
    def create_parallel_bent_line_svg(angle_a, angle_b):
        """평행선과 꺾인 선 SVG"""
        width = 300
        height = 200
        svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.label { font: 14px sans-serif; fill: #333; } .line { stroke: black; stroke-width: 2; fill: none; } .aux { stroke: #666; stroke-width: 1; stroke-dasharray: 4,4; } .angle { fill: none; stroke: #ef4444; stroke-width: 2; }</style>'
        
        svg += f'<line x1="20" y1="50" x2="280" y2="50" class="line" /><text x="290" y="55" class="label">l</text>'
        svg += f'<line x1="20" y1="150" x2="280" y2="150" class="line" /><text x="290" y="155" class="label">m</text>'
        
        px, py = 150, 100
        tx = px - (50 / math.tan(math.radians(angle_a))) if angle_a != 90 else px
        bx = px - (50 / math.tan(math.radians(angle_b))) if angle_b != 90 else px
        
        svg += f'<line x1="{tx}" y1="50" x2="{px}" y2="{py}" class="line" /><line x1="{bx}" y1="150" x2="{px}" y2="{py}" class="line" />'
        svg += f'<text x="{tx+20}" y="70" class="label">{angle_a}°</text><text x="{bx+20}" y="140" class="label">{angle_b}°</text>'
        svg += f'<text x="{px+10}" y="{py+5}" class="label">P</text><circle cx="{px}" cy="{py}" r="3" fill="black" /><text x="{px-30}" y="{py+5}" class="label" fill="red">x</text>'
            
        svg += '</svg>'
        return svg

    @staticmethod
    def create_histogram_svg(data, x_labels=None, width=400, height=300, y_label="도수", x_label="계급", show_polygon=False):
        """
        히스토그램 SVG 생성
        data: [도수1, 도수2, ...]
        x_labels: ['0~10', '10~20', ...] (계급 구간)
        show_polygon: 도수분포다각형(꺾은선) 표시 여부
        """
        if not data: return ""
        
        max_val = max(data)
        # Y축 최대값 설정 (5의 배수 등으로 깔끔하게)
        y_max = math.ceil(max_val / 5) * 5 if max_val > 0 else 5
        
        padding_left = 50
        padding_right = 20
        padding_top = 30
        padding_bottom = 40
        
        graph_width = width - padding_left - padding_right
        graph_height = height - padding_top - padding_bottom
        
        bar_width = graph_width / len(data)
        
        svg = f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">'
        svg += '<style>.bar { fill: rgba(59, 130, 246, 0.5); stroke: #3b82f6; stroke-width: 1; } .axis { stroke: black; stroke-width: 1; } .label { font: 12px sans-serif; fill: #333; text-anchor: middle; } .grid { stroke: #eee; stroke-width: 1; } .title { font: bold 14px sans-serif; text-anchor: middle; } .polygon-line { fill: none; stroke: #ef4444; stroke-width: 2; } .polygon-point { fill: #ef4444; }</style>'
        
        # Y축 그리드 및 라벨
        num_ticks = 5
        for i in range(num_ticks + 1):
            val = y_max * i / num_ticks
            y = padding_top + graph_height - (val / y_max * graph_height)
            svg += f'<line x1="{padding_left}" y1="{y}" x2="{width-padding_right}" y2="{y}" class="grid" />'
            svg += f'<text x="{padding_left-5}" y="{y+4}" text-anchor="end" class="label">{int(val)}</text>'
            
        # Bars
        for i, val in enumerate(data):
            bar_h = (val / y_max) * graph_height
            x = padding_left + i * bar_width
            y = padding_top + graph_height - bar_h
            
            svg += f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_h}" class="bar" />'
            
            # X축 라벨 (계급)
            if x_labels and i < len(x_labels):
                svg += f'<text x="{x + bar_width/2}" y="{height-15}" class="label">{x_labels[i]}</text>'
        
        # 도수분포다각형 (꺾은선 그래프)
        if show_polygon:
            zero_y = padding_top + graph_height
            poly_points = []
            
            # 시작점 (가상의 이전 계급, 도수 0)
            poly_points.append((padding_left - bar_width/2, zero_y))
            
            # 각 막대의 중점
            for i, val in enumerate(data):
                bar_h = (val / y_max) * graph_height
                x = padding_left + i * bar_width + bar_width / 2
                y = padding_top + graph_height - bar_h
                poly_points.append((x, y))
                
            # 끝점 (가상의 다음 계급, 도수 0)
            poly_points.append((padding_left + len(data) * bar_width + bar_width/2, zero_y))
            
            # 선 그리기
            points_str = " ".join([f"{x},{y}" for x, y in poly_points])
            svg += f'<polyline points="{points_str}" class="polygon-line" />'
            
            # 점 찍기
            for x, y in poly_points:
                if 0 <= x <= width: # 화면 밖으로 너무 나가는 점은 제외
                    svg += f'<circle cx="{x}" cy="{y}" r="3" class="polygon-point" />'
                
        # Axes lines
        svg += f'<line x1="{padding_left}" y1="{padding_top}" x2="{padding_left}" y2="{height-padding_bottom}" class="axis" />' # Y axis
        svg += f'<line x1="{padding_left}" y1="{height-padding_bottom}" x2="{width-padding_right}" y2="{height-padding_bottom}" class="axis" />' # X axis
        
        # 축 이름
        svg += f'<text x="{width/2}" y="{height-2}" class="label" font-weight="bold">{x_label}</text>'
        svg += f'<text x="{padding_left}" y="{padding_top-10}" class="label" font-weight="bold">{y_label}</text>'
        
        svg += '</svg>'
        return svg