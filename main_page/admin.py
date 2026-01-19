from django.contrib import admin
from .models import AcademyAchievements, AcademyInfrastructure, AcademyStatistics, aboutStatistics, AboutPhotos, Mission, Accreditation,  History

# Register your models here.
admin.site.register(aboutStatistics)
admin.site.register(History)
admin.site.register(AboutPhotos)
admin.site.register(Mission)
admin.site.register(Accreditation)
admin.site.register(AcademyStatistics)
admin.site.register(AcademyAchievements)
admin.site.register(AcademyInfrastructure)

admin.site.site_header = "Админ панель Физкультурной Академии"
admin.site.site_title = "Админ панель Физкультурной Академии"
admin.site.index_title = "Добро пожаловать в админ панель Физкультурной Академии"
