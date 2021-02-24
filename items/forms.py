from django import forms
from django.utils.translation import ugettext_lazy as _

class SearchForm(forms.Form):
    first_city_choices = (
        ('Martlock', 'Martlock'),
        ('Thetford', 'Thetford'),
        ('Bridgewatch', 'Bridgewatch'),
        ('Caerleon', 'Caerleon'),
        ('Lymhurst', 'Lymhurst'),
        ('Fort Sterling', 'Fort Sterling'),
    )
    city_choices = (
        ('Black Market', 'Black Market'),
        ('Martlock', 'Martlock'),
        ('Thetford', 'Thetford'),
        ('Bridgewatch', 'Bridgewatch'),
        ('Caerleon', 'Caerleon'),
        ('Lymhurst', 'Lymhurst'),
        ('Fort Sterling', 'Fort Sterling'),
    )
    items_choices = (
        ('mellee_sword', _('Мечи')),
        ('range', _('Оружие дальнего боя')),
        ('mellee_mace', _('Булавы')),
        ('mellee_staff', _('Шесты')),
        ('mellee_hammer', _('Молоты')),
        ('mellee_daggers', _('Кинжалы')),
        ('mellee_axe', _('Топоры')),
        ('staff', _('Посохи/Магия')),
        ('plate_shoes', _('Латные ботинки')),
        ('plate_head', _('Латные шлемы')),
        ('plate_armor', _('Латные доспехи')),
        ('leather_shoes', _('Кожанные ботинки')),
        ('leather_head', _('Кожанные капюшоны')),
        ('leather_armor', _('Кожанные доспехи')),
        ('cloth_shoes', _('Тканевые ботинки')),
        ('cloth_armor', _('Тканевые доспехи')),
        ('cloth_head', _('Тканевые колпаки')),
        ('capes', _('Плащи')),
        ('bags', _('Сумки')),
        ('luxury', _('Роскошь')),
        ('resources', _('Ресурсы')),
    )
    tiers_choices = (
        ('T4', 'T4'),
        ('T5', 'T5'),
        ('T6', 'T6'),
        ('T7', 'T7'),
        ('T8', 'T8'),
    )
    enchant_choices = (
        ('0', '0'),
        ('@1', '1'),
        ('@2', '2'),
        ('@3', '3'),
    )
    first_city = forms.ChoiceField(required=False, label='', choices=first_city_choices,
                                   widget=forms.Select(attrs={'class': 'form-control',
                                                              'id':'first_city'}))
    second_city = forms.ChoiceField(required=False, label='', choices=city_choices,
                             widget=forms.Select(attrs={'class': 'form-control',
                                                        'id': 'second_city'}))
    category_items = forms.ChoiceField(required=False, label='', choices=items_choices,
                                       widget=forms.Select(attrs={'class': 'form-control',
                                                                  'id': 'items'}))
    tiers = forms.MultipleChoiceField(required=True, label='', choices=tiers_choices, widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'tier'})
                                      )
    chart = forms.MultipleChoiceField(required=True, label='', choices=enchant_choices, widget=forms.SelectMultiple(
        attrs={'class': 'form-control',
               'id': 'chart'})
                                      )
    profit = forms.IntegerField(required=False, label='', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                        'id': 'profit_limit',
                                                                                        'placeholder': _('Прибыль от')}),
                                max_value=100000000)
    hours = forms.IntegerField(required=False, label='', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                       'id': 'hours_limit',
                                                                                       'placeholder': _('Актуальность до')}),
                               max_value=99)
