from django.db import models

from members.models import PayGoUserManager, PayGoUser


class AgencyUserManager(PayGoUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(type=PayGoUser.TYPE_AGENCY)


class AgencyUser(PayGoUser):
    # agencies = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='franchisee_to_agency',
    #                              verbose_name='가맹점 소개 시킨 에이전트 목록', blank=True, null=True, help_text='에이전트')
    objects = AgencyUserManager()

    class Meta:
        proxy = True
        verbose_name = '에이전시'
        verbose_name_plural = f'{verbose_name} 목록'

    def save(self, *args, **kwargs):
        self.type = PayGoUser.TYPE_AGENCY
        super().save(*args, **kwargs)
