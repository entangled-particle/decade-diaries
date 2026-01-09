from django.contrib import admin
from .models import Diary, Question, Answer


class DiaryAdmin(admin.ModelAdmin):
    list_display = ('title', 'month', 'year', 'locked', 'created_at', 'updated_at')
    list_filter = ('locked', 'month', 'year', 'created_at', 'updated_at')
    search_fields = ('title',)
    list_per_page = 10


admin.site.register(Diary, DiaryAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('diary', 'user_first_name', 'question', 'answer',
                    'file', 'created_at', 'updated_at')
    list_filter = ('diary', 'user', 'question')
    search_fields = ('diary__title', 'user__email',
                     'question__question', 'answer')
    list_per_page = 10

    @admin.display(description="User")
    def user_first_name(self, obj):
        return obj.user.first_name or obj.user.email


admin.site.register(Answer, AnswerAdmin)


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('number', 'question')
    search_fields = ('question',)
    list_per_page = 10


admin.site.register(Question, QuestionAdmin)
