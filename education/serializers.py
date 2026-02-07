from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import  Master,CollegeDepartmentInfo, CollegeManagement, CollegeTabCategory, MasterStuff, Phd, PhdStuff



class MultilingualSerializerMixin:
    """
    Mixin для поддержки мультиязычности в сериализаторах.
    
    Использование:
    class MySerializer(MultilingualSerializerMixin, serializers.ModelSerializer):
        class Meta:
            multilingual_fields = ['name', 'description']  # поля с суффиксами _ru, _en, _kg
            ...
    """
    
    def get_multilingual_field(self, obj, field_name):
        """Получить значение поля на нужном языке"""
        language = self.context.get('language', 'ru')
        method_name = f'get_{field_name}'
        
        if hasattr(obj, method_name):
            return getattr(obj, method_name)(language)
            # flow: 1. getattr(obj, method_name) -> returns needed method. 2) (language) -> calls this method with argument called name. 3) return -> returns the result of method_name(language)
        
        # Fallback: прямое получение поля с суффиксом
        return getattr(obj, f'{field_name}_{language}', # -> this get's field without method. 
                    getattr(obj, f'{field_name}_ru', None)) # -> this is like fallback if it could find field with lang it will return field_name with _ru suffix   

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Добавляем поля для мультиязычных атрибутов
        multilingual_fields = getattr(self.Meta, 'multilingual_fields', [])
        
        for field_name in multilingual_fields:
            self.fields[field_name] = serializers.SerializerMethodField()



class CollegeManagementSerializer(serializers.ModelSerializer):
    """Сериализатор для руководства факультета"""

    name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()

    class Meta:
        model = CollegeManagement
        fields = ["id", "name", "role", "photo", "phone", "email", "order"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_name(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_role(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_role(language)

    @extend_schema_field(OpenApiTypes.STR)
    def get_photo(self, obj) -> str | None:
        img = getattr(obj, "photo", None)
        if not img:
            return None
        try:
            return img.url
        except Exception:
            return str(img)


class CollegeDepartmentInfoSerializer(serializers.ModelSerializer):
    """Сериализатор для описания кафедры"""

    description = serializers.SerializerMethodField()

    class Meta:
        model = CollegeDepartmentInfo
        fields = ["id", "description"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_description(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_description(language)


class CollegeDepartmentCategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категории кафедры"""

    name = serializers.SerializerMethodField()

    class Meta:
        model = CollegeTabCategory
        fields = ["id", "name"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_name(language)



class CollegeDepartmentCategoryDetailSerializer(serializers.ModelSerializer):
    """Детальный сериализатор категории с полной информацией"""

    name = serializers.SerializerMethodField()
    info = serializers.SerializerMethodField()
    management = serializers.SerializerMethodField()

    class Meta:
        model = CollegeTabCategory
        fields = ["id", "name", "color", "order", "info", "management"]

    @extend_schema_field(OpenApiTypes.STR)
    def get_name(self, obj) -> str:
        language = self.context.get("language", "ru")
        return obj.get_name(language)

    @extend_schema_field(CollegeDepartmentInfoSerializer)
    def get_info(self, obj):
        try:
            info = obj.info
            if info.is_active:
                return CollegeDepartmentInfoSerializer(info, context=self.context).data
        except Exception:
            return None
        return None

    @extend_schema_field(CollegeManagementSerializer(many=True))
    def get_management(self, obj):
        items = obj.management.filter(is_active=True).order_by("order")
        return CollegeManagementSerializer(items, many=True, context=self.context).data





class MasterStuffSerializer(serializers.ModelSerializer, MultilingualSerializerMixin):
    fio = serializers.SerializerMethodField()
    pos = serializers.SerializerMethodField()

    class Meta:
        model = MasterStuff
        fields = ('id', 'fio', 'pos')

    def get_fio(self, obj):
        return self.get_multilingual_field(obj, 'fio')
    
    def get_pos(self, obj):
        return self.get_multilingual_field(obj, 'pos')
    



class MasterSerializer(serializers.ModelSerializer, MultilingualSerializerMixin):
    info = serializers.SerializerMethodField()
    stuff = serializers.SerializerMethodField()

    class Meta:
        model = Master
        fields = ('id', 'info', 'study_plan', 'disciplines', 'stuff')

    def get_info(self, obj):
        return obj.get_info(self.context.get('language', 'ru'))
    
    @extend_schema_field(MasterStuffSerializer(many=True))
    def get_stuff(self, obj):
        staff = obj.masterstuff_set.all()
        return MasterStuffSerializer(staff, many=True, context=self.context).data
    
    

class PhdStuffSerializer(serializers.ModelSerializer, MultilingualSerializerMixin):
    fio = serializers.SerializerMethodField()
    pos = serializers.SerializerMethodField()

    class Meta:
        model = PhdStuff
        fields = ('id', 'fio', 'pos')

    def get_fio(self, obj):
        return self.get_multilingual_field(obj, 'fio')
    
    def get_pos(self, obj):
        return self.get_multilingual_field(obj, 'pos')
    


class PhdSerializer(serializers.ModelSerializer, MultilingualSerializerMixin):
    info = serializers.SerializerMethodField()
    stuff = serializers.SerializerMethodField()

    class Meta:
        model = Phd
        fields = ('id', 'info', 'study_plan', 'disciplines', 'stuff')

    def get_info(self, obj):
        return obj.get_info(self.context.get('language', 'ru'))
    
    @extend_schema_field(PhdStuffSerializer(many=True))
    def get_stuff(self, obj):
        staff = obj.phdstuff_set.all()
        return PhdStuffSerializer(staff, many=True, context=self.context).data
    
