class TemplateRegistry:
    """
    카테고리별로 템플릿 마스터 인스턴스를 관리하는 전역 레지스트리
    """
    _templates = {}

    @classmethod
    def register(cls, category, template_master):
        if category not in cls._templates:
            cls._templates[category] = []
        cls._templates[category].append(template_master)

    @classmethod
    def get_by_category(cls, category):
        return cls._templates.get(category, [])