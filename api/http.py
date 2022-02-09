# -*- coding: utf-8 -*-
import requests, json

class arknights_http():
    class request_http():
        def get(url):
            r = requests.get(url)
            if r.status_code == 200:
                return r.content
            return 'ERROR'

        def post(url, data):
            r = requests.post(url, data=data)
            if r.status_code == 200:
                return r.content
            return 'ERROR'

    url_user_info = 'https://as.hypergryph.com/u8/user/info/v1/basic'
    url_cards_record = 'http://ak.hypergryph.com/user/api/inquiry/gacha'

    def __init__(self, token):
        self.token = token

    def get_user_info(self):
        payload = '''
        {{
            "appId":1,
            "channelMasterId":1,
            "channelToken":{{
                "token":"{}"
            }}
        }}    
        '''.format(self.token)
        source_from_server = self.request_http.post(self.url_user_info, payload)
        if source_from_server == 'ERROR':
            print('ERROR: arknights_api::get_user_info, token: {}'.format(self.token))
            exit(1)
        user_info_source = json.loads(source_from_server).get('data')
        user_info_dict = {
            'uid': user_info_source.get('uid'),
            'nickName': user_info_source.get('nickName')
        }
        return user_info_dict

    def get_cards_record(self, last_timestamp=None):
        def get_cards_record_by_page(page):
            url_cards_record_page = '{}?page={}&token={}'.format(self.url_cards_record, page, self.token)
            source_from_server = self.request_http.get(url_cards_record_page)
            if source_from_server == 'ERROR':
                print('ERROR: arknights_api::get_cards_record::get_cards_record_by_page, page: {}, token: {}'.format(page, self.token))
                exit(1)
            cards_record_page_source = json.loads(source_from_server)
            cards_record_page_data_list = cards_record_page_source.get('data').get('list')
            return cards_record_page_data_list

        cards_record_data_list = []
        flag_outdate = False
        for page in range(1, 75):
            if flag_outdate == True:
                break
            cards_record_page_data_list = get_cards_record_by_page(page)
            if cards_record_page_data_list == []:
                break
            if last_timestamp == None:
                cards_record_data_list.extend(cards_record_page_data_list)
            else:
                for cards_record_page_data_item in cards_record_page_data_list:
                    if int(cards_record_page_data_item['ts']) > int(last_timestamp):
                        cards_record_data_list.append(cards_record_page_data_item)
                    else:
                        flag_outdate = True
                        break

        cards_record_data_list = reversed(cards_record_data_list)
        return cards_record_data_list
