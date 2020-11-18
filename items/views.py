# -*- coding: utf-8 -*-
import copy
import datetime
import json
import os
from datetime import timedelta

import requests
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from items.forms import SearchForm

option_items = {'mellee_sword': 'Мечи', 'range': 'Оружие дальнего боя', 'mellee_mace': 'Булавы',
                'mellee_staff': 'Шесты', 'mellee_hammer': 'Молоты', 'mellee_daggers': 'Кинжалы',
                'mellee_axe': 'Топоры', 'staff': 'Посохи/Магия', 'plate_shoes': 'Латные ботинки',
                'plate_head': 'Латные шлемы', 'plate_armor': 'Латные доспехи',
                'leather_shoes': 'Кожанные ботинки', 'leather_head': 'Кожанные капюшоны',
                'leather_armor': 'Кожанные доспехи', 'cloth_shoes': 'Тканевые ботинки',
                'cloth_armor': 'Тканевые доспехи', 'cloth_head': 'Тканевые колпаки', 'capes': 'Плащи',
                'bags': 'Сумки', 'luxury': 'Роскошь', 'resources':'Ресурсы'}

option_tier = ['T4', 'T5', 'T6', 'T7', 'T8']
quality_level = {1: 'Обычное', 2: 'Хорошее', 3: 'Потрясающее', 4: 'Превосходное', 5: 'Шедевр'}

API = 'https://www.albion-online-data.com/api/v2/stats/prices/'

with open(os.path.join(settings.BASE_DIR, 'items/static/items/json/items.json'), 'r') as f:
    full_name = json.load(f)

with open(os.path.join(settings.BASE_DIR, 'items/static/items/json/russia.json'), 'r', encoding='utf-8') as f:
    russia_name = json.load(f)


def index(request):
    form = SearchForm()
    return render(request, 'form.html', context={'form': form})


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def get_items(city, item, enchant, tiers, profit, hours, api=False, first_loc='Black Market'):
    """Fetch items with profit from albion data project


    Retrieves rows with the given parameters profits and current hours.


    Args:
        city: city for getting items.
        item: item category to select items.
        enchant: enchant for items.
        tiers: item ranks.
        profit: profit for a given parameter.
        hours: hours for a given parameter.
        api: fetch for json api.

    Returns:
        Json-like object for view in table on site.
        If items not found return empty list of dictionaries.
        Return HttpResponse with 'invalid parameters' if parameters are not correct.
        Return HttpResponse with 'Произошла ошибка попробуйте позже.' if albion data project return Error
    """
    query_items = []
    items_black = []
    items_white = []
    list_item_view = []
    items_view = {}
    items = full_name[item]
    item_name = ''
    price_market = 0
    for i in range(len(items)):
        for tir in range(len(tiers)):
            for chant in range(len(enchant)):
                if enchant[chant] == '0':
                    if item == 'luxury':
                        full_item = f'{items[i]}{int(tiers[tir][-1])-3}'
                    else:
                        full_item = f'{tiers[tir]}_{items[i]}'
                else:
                    if item == 'resources':
                        full_item = f'{tiers[tir]}_{items[i]}_LEVEL{enchant[chant][-1]}'
                    else:
                        full_item = f'{tiers[tir]}_{items[i]}{enchant[chant]}'
                query_items.append(full_item)
    url_json = API + ','.join(query_items[:350]) + '?locations=' + f'{first_loc},' + city
    response_api = requests.get(url_json)
    if response_api.status_code == 200:
        json_response = response_api.json()
    else:
        return HttpResponse('Произошла ошибка попробуйте позже.')
    for i in range(len(json_response)):
        qs_dict = json_response[i]
        if qs_dict['buy_price_min_date'] == "0001-01-01T00:00:00" \
                or qs_dict['sell_price_min_date'] == "0001-01-01T00:00:00" \
                or qs_dict['sell_price_max_date'] == "0001-01-01T00:00:00" \
                or qs_dict['buy_price_max_date'] == "0001-01-01T00:00:00":
            continue
        elif qs_dict['sell_price_min'] == 0 and qs_dict['buy_price_max'] == 0:
            continue
        else:
            if qs_dict['city'] != first_loc:
                item_name_white = qs_dict['item_id']
                quality_white = quality_level[qs_dict['quality']]
                price_market = qs_dict['sell_price_min']
                items_white.append([item_name_white, quality_white, price_market])
            else:
                quality = qs_dict['quality']
                item_name_img = qs_dict['item_id']
                price_black_order = qs_dict['sell_price_min']
                price_black_fast = qs_dict['buy_price_max']
                time_upd = datetime.datetime.strptime(qs_dict['buy_price_max_date'], '%Y-%m-%dT%H:%M:%S')
                now_date = datetime.datetime.utcnow()
                act_time = now_date - time_upd
                time_to_view = str(act_time).split(':')[0]
                items_black.append([item_name_img, quality_level[quality], price_black_order,
                                    price_black_fast, time_to_view])
    for i in range(len(items_black)):
        for ind in range(len(items_white)):
            if items_black[i][0] == items_white[ind][0] \
                    and items_black[i][1] == items_white[ind][1]:
                for k, v in russia_name.items():
                    if item == 'luxury':
                        if k == items_black[i][0]:
                            item_name = v[0]
                    else:
                        if k == items_black[i][0][3:]:
                            name = items_black[i][0]
                            item_name = name[:3] + v[0]
                price_black_order = items_black[i][2]
                price_black_fast = items_black[i][3]
                price_auction = items_white[ind][2]
                total_price_fast = price_black_fast - price_auction
                total_price_order = price_black_order - price_auction
                time = int(items_black[i][4])
                act_time = timedelta(hours=time)
                seconds = act_time.seconds
                hour = str(seconds // 3600)
                if api:
                    if '@' in items_white[ind][0]:
                        items_view['item_name'] = item_name + items_white[ind][0][-2:]
                    else:
                        items_view['item_name'] = item_name
                        items_view['quality'] = items_white[ind][1]
                        items_view['act_time'] = int(hour)
                        items_view['price_auction'] = price_auction
                        items_view['price_black_order'] = price_black_order
                        items_view['profit_black_order'] = total_price_order
                        items_view['price_black_fast'] = price_black_fast
                        items_view['profit_black_fast'] = total_price_fast
                else:
                    items_view['item_name'] = item_name
                    items_view['quality'] = items_white[ind][1]
                    items_view['act_time'] = hour + ' часов назад'
                    items_view['price_auction'] = '{:,}'.format(price_auction).replace(',', '.')
                    items_view['price_black_order'] = '{:,}'.format(price_black_order).replace(',', '.')
                    items_view['price_black_order'] = '{:,}'.format(price_black_order).replace(',', '.')
                    items_view['profit_black_order'] = '{:,}'.format(total_price_order).replace(',', '.')
                    items_view['price_black_fast'] = '{:,}'.format(price_black_fast).replace(',', '.')
                    items_view['profit_black_fast'] = '{:,}'.format(total_price_fast).replace(',', '.')
                    items_view['img_url'] = f'items/img/{items_white[ind][0]}.png'
                if not hours:
                    actual_hours = timedelta(hours=5)
                elif is_digit(hours):
                    actual_hours = timedelta(hours=int(hours))
                else:
                    return HttpResponse('Invalid parameters')
                if not profit:
                    profit = 1
                if total_price_order > int(profit) and price_market > 0 and act_time <= actual_hours \
                        and item_name != '':
                    list_item_view.append(copy.deepcopy(items_view))
                else:
                    pass
    return list_item_view


def search(request):
    error = False
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            first_city = request.GET.get('first_city')
            second_city = request.GET.get('second_city')
            item = request.GET.get('category_items')
            tiers = request.GET.getlist('tiers')
            charts = request.GET.getlist('chart')
            profit = request.GET.get('profit').strip()
            hours = request.GET.get('hours').strip()
            list_item_view = get_items(second_city, item, charts, tiers, profit, hours, first_loc=first_city)
            if list_item_view:
                pass
            else:
                error = True
            return render(request, 'search.html', context={'items': option_items,
                                                           'tiers': option_tier, 'town': f'{first_city}, {second_city}',
                                                           'list_item_view': list_item_view, 'form': form,
                                                           'error': error})
        else:
            form = SearchForm()
        return render(request, 'form.html', context={'items': option_items,
                                                     'tiers': option_tier, 'form': form}, status=500)


def info(request):
    return render(request, 'info.html')


def development(request):
    return render(request, 'api.html')


def changelog(request):
    return render(request, 'changelog.html')


@api_view(['GET'])
def two_city_compare(request):
    if request.GET.get('format') != 'json':
        return HttpResponse('invalid parameters')
    locations = request.GET.get('locations')
    item = request.GET.get('category_items')
    tiers = request.GET.getlist('tier')[0].split(',')
    charts = request.GET.getlist('chart')[0].split(',')
    profit = request.GET.get('profit')
    hours = request.GET.get('hours')
    first_city, second_city = locations.split(',')
    two_city_json_response = get_items(second_city, item, charts, tiers, profit, hours, api=True, first_loc=first_city)
    return Response(two_city_json_response)