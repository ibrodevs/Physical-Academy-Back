from rest_framework import serializers
from .models import BulletinYear, BulletinIssue


class SidebarIssueSerializer(serializers.ModelSerializer):
    
    number = serializers.IntegerField(source='issue_number')
    description = serializers.SerializerMethodField()

    class Meta:
        model = BulletinIssue
        fields = ['id', 'number', 'description']

    def get_description(self, obj):
        # Берём язык из контекста (передаётся из view)
        lang = self.context.get('lang', 'ru')
        if lang == 'en':
            return obj.description_en
        elif lang == 'kg':
            return obj.description_kg
        else:
            return obj.description_ru  # по умолчанию — русский


class SidebarYearSerializer(serializers.ModelSerializer):
    """
    Сериализатор года для сайдбара.
    Возвращает: year, и список выпусков внутри.
    """
    issues = serializers.SerializerMethodField()

    class Meta:
        model = BulletinYear
        fields = ['year', 'issues']

    def get_issues(self, obj):
        issues = obj.issues.all()
        # Передаём контекст (язык) в дочерний сериализатор
        return SidebarIssueSerializer(issues, many=True, context=self.context).data


class BulletinIssueSerializer(serializers.ModelSerializer):
   
    year = serializers.IntegerField(source='year.year')  # число, а не объект
    description = serializers.SerializerMethodField()

    class Meta:
        model = BulletinIssue
        fields = ['id', 'year', 'issue_number', 'description']

    def get_description(self, obj):
        lang = self.context.get('lang', 'ru')
        if lang == 'en':
            return obj.description_en
        elif lang == 'kg':
            return obj.description_kg
        else:
            return obj.description_ru