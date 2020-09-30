from django import forms


class SearchForm(forms.Form):
    city_choices = (
        ('3008', 'Martlock'),
        ('0007', 'Thetford'),
        ('2004', 'Bridgewatch'),
        ('3005', 'Caerleon'),
        ('1002', 'Lymhurst'),
        ('4002', 'Fort Sterling')
    )
    items_choices = (
        ('mellee_sword', 'Мечи'),
        ('range', 'Оружие дальнего боя'),
        ('mellee_mace', 'Булавы'),
        ('mellee_staff', 'Шесты'),
        ('mellee_hammer', 'Молоты'),
        ('mellee_daggers', 'Кинжалы'),
        ('mellee_axe', 'Топоры'),
        ('staff', 'Посохи/Магия'),
        ('plate_shoes', 'Латные ботинки'),
        ('plate_head', 'Латные шлемы'),
        ('plate_armor', 'Латные доспехи'),
        ('leather_shoes', 'Кожанные ботинки'),
        ('leather_head', 'Кожанные капюшоны'),
        ('leather_armor', 'Кожанные доспехи'),
        ('cloth_shoes', 'Тканевые ботинки'),
        ('cloth_armor', 'Тканевые доспехи'),
        ('cloth_head', 'Тканевые колпаки'),
        ('capes', 'Плащи'),
        ('bags', 'Сумки'),
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
    city = forms.ChoiceField(required=False, label='', choices=city_choices,
                             widget=forms.Select(attrs={'class': 'form-control',
                                                        'id': 'city'}))
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
                                                                                        'placeholder': 'Прибыль от'}),
                                max_value=100000000)
    hours = forms.IntegerField(required=False, label='', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                       'id': 'hours_limit',
                                                                                       'placeholder': 'Актуальность до'}),
                               max_value=99)
