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
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.decorators import api_view
from rest_framework.response import Response

option_city = {'3008': 'Martlock', '0007': 'Thetford', '2004': 'Bridgewatch', '3005': 'Caerleon',
               '1002': 'Lymhurst', '4002': 'Fort Sterling'}
option_items = {'mellee_sword': 'Мечи', 'range': 'Оружие дальнего боя', 'mellee_mace': 'Булавы',
                'mellee_staff': 'Шесты', 'mellee_hammer': 'Молоты', 'mellee_daggers': 'Кинжалы', 'mellee_axe': 'Топоры',
                'staff': 'Посохи/Магия', 'plate_shoes': 'Латные ботинки', 'plate_head': 'Латные шлемы',
                'plate_armor': 'Латные доспехи', 'leather_shoes': 'Кожанные ботинки',
                'leather_head': 'Кожанные капюшоны', 'leather_armor': 'Кожанные доспехи',
                'cloth_shoes': 'Тканевые ботинки', 'cloth_armor': 'Тканевые доспехи', 'cloth_head': 'Тканевые колпаки',
                'capes': 'Плащи', 'bags': 'Сумки'}
option_tier = ['T4', 'T5', 'T6', 'T7', 'T8']
quality_level = {1: 'Обычное', 2: 'Хорошее', 3: 'Потрясающее', 4: 'Превосходное', 5: 'Шедевр'}

API = 'https://www.albion-online-data.com/api/v2/stats/prices/'

with open(os.path.join(settings.BASE_DIR, 'items/static/items/json/items.json'), 'r') as f:
    full_name = json.load(f)
with open(os.path.join(settings.BASE_DIR, 'items/static/items/json/russia.json'), 'r', encoding='utf-8') as f:
    russia_name = json.load(f)


def index(request):
    return render(request, 'index.html', context={'cities': option_city, 'items': option_items, 'tiers': option_tier, })


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


def get_items(city, item, charts, tiers, profit, hours, api=False):
    query_items = []
    items_view = {}
    list_item_view = []
    items = full_name[item]
    item_name = ''
    price_market = 0
    for i in range(0, len(items)):
        for tir in range(0, len(tiers)):
            for chart in range(0, len(charts)):
                if charts[chart] == '0':
                    full_item = f'{tiers[tir]}_{items[i]}'
                else:
                    full_item = f'{tiers[tir]}_{items[i]}{charts[chart]}'
                query_items.append(full_item)
    url_json = API + ','.join(query_items) + '?locations=' + 'Black Market,' + option_city[city]
    response_api = requests.get(url_json)
    if response_api.status_code == 200:
        json_response = response_api.json()
    else:
        return HttpResponse('Произошла ошибка попробуйте позже.')
    for i in range(0, len(json_response)):
        qs_dict = json_response[i]
        if qs_dict['buy_price_min_date'] == "0001-01-01T00:00:00" \
                or qs_dict['sell_price_min_date'] == "0001-01-01T00:00:00" \
                or qs_dict['sell_price_max_date'] == "0001-01-01T00:00:00" \
                or qs_dict['buy_price_max_date'] == "0001-01-01T00:00:00":
            continue
        else:
            if qs_dict['city'] != 'Black Market':
                price_market = qs_dict['sell_price_min']
                if not api:
                    items_view['price_auction'] = '{:,}'.format(price_market).replace(',', '.')
            else:
                for k, v in russia_name.items():
                    if k == qs_dict['item_id'][3:]:
                        item_name = v[0]
                quality = qs_dict['quality']
                items_view['quality'] = quality_level[quality]
                items_view['item_name'] = item_name
                item_name_img = qs_dict['item_id']
                price_black_order = qs_dict['sell_price_min']
                total_price_order = price_black_order - price_market
                price_black_fast = qs_dict['buy_price_max']
                total_price_fast = price_black_fast - price_market
                time_upd = datetime.datetime.strptime(qs_dict['buy_price_max_date'], '%Y-%m-%dT%H:%M:%S')
                now_date = datetime.datetime.utcnow()
                act_time = now_date - time_upd
                time_to_view = str(act_time).split(':')[0]
                items_view['act_time'] = time_to_view + " часов назад"
                if api:
                    items_view['act_time'] = int(time_to_view)
                    items_view['lease'] = price_market
                    items_view['black_order'] = price_black_order
                    items_view['current_rate'] = price_black_fast
                    items_view['profit_black_order'] = total_price_order
                    items_view['profit_black_rate'] = total_price_fast
                else:
                    items_view['price_black_order'] = '{:,}'.format(price_black_order).replace(',', '.')
                    items_view['profit_black_order'] = '{:,}'.format(total_price_order).replace(',', '.')
                    items_view['price_black_fast'] = '{:,}'.format(price_black_fast).replace(',', '.')
                    items_view['profit_black_fast'] = '{:,}'.format(total_price_fast).replace(',', '.')
                    items_view['img_url'] = f'items/img/{item_name_img}.png'
                if not hours:
                    actual_hours = timedelta(hours=5)
                elif is_digit(hours):
                    actual_hours = timedelta(hours=int(hours))
                else:
                    return HttpResponse('Invalid parameters')
                if not profit:
                    profit = 1
                if total_price_order > int(profit) and price_market > 0 and act_time < actual_hours \
                        and item_name != '':
                    list_item_view.append(copy.deepcopy(items_view))
                else:
                    pass
    return list_item_view


def search(request):
    city = request.POST.get('city')
    item = request.POST.get('item')
    tiers = request.POST.getlist('tier')
    charts = request.POST.getlist('chart')
    profit = request.POST.get('profit').strip()
    hours = request.POST.get('hours').strip()
    list_item_view = get_items(city, item, charts, tiers, profit, hours)
    error = False
    return render(request, 'index.html', context={'cities': option_city, 'items': option_items, 'tiers': option_tier,
                                                  'town': option_city[city], 'error': error,
                                                  'list_item_view': list_item_view})


@api_view(['GET'])
def black_albion_api(request):
    if request.GET.get('format') != 'json':
        return HttpResponse('invalid parameters')
    city = request.GET.get('city')
    item = request.GET.get('item')
    tiers = request.GET.getlist('tier')
    tiers_api = tiers[0].split(',')
    charts = request.GET.getlist('chart')
    charts_api = charts[0].split(',')
    profit = request.GET.get('profit')
    hours = request.GET.get('hours')
    json_response = get_items(city, item, charts_api, tiers_api, profit, hours, api=True)
    return Response(json_response)


@api_view(['GET'])
def two_city_compare(request):
    try:
        response_format = request.GET['format']
        if response_format != 'json':
            return HttpResponse('Invalid parameters')
        category = request.GET['category']
        values_category = full_name[category]
        locations = request.GET['locations'].split(',')
        common_city = locations[0]
        black_city = locations[1]
        expected_profit = int(request.GET['profit'])
    except (MultiValueDictKeyError, IndexError, ValueError, KeyError):
        return HttpResponse('Invalid parameters')
    cities = [common_city, black_city]
    url_json = API + ','.join(values_category) + '?locations=' + ','.join(cities)
    response_api = requests.get(url_json).json()
    items_black = []
    items_value_black = {}
    items_common = []
    items_value_common = {}
    for i in range(len(response_api)):
        if response_api[i]['city'] == cities[1]:
            items_value_black['name'] = response_api[i]['item_id']
            items_value_black['price'] = response_api[i]['sell_price_min']
            items_black.append(copy.deepcopy(items_value_black))
        elif response_api[i]['city'] == cities[0]:
            items_value_common['name'] = response_api[i]['item_id']
            items_value_common['price'] = response_api[i]['sell_price_min']
            items_common.append(copy.deepcopy(items_value_common))
    profits = []
    items_profit = {}
    for i in range(len(items_common)):
        try:
            if items_black[i]['price'] > 0:
                price_common = items_common[i]['price']
                price_black = items_black[i]['price']
                name_item = items_common[i]['name']
                profit = price_common - price_black
                if profit >= expected_profit:
                    items_profit['item_id'] = name_item
                    items_profit['city'] = ','.join(cities)
                    items_profit['price_first'] = price_common
                    items_profit['price_second'] = price_black
                    items_profit['profit'] = profit
                    profits.append(copy.deepcopy(items_profit))
        except IndexError:
            return HttpResponse('Invalid city')
    return Response(profits)
