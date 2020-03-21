import requests
import json

import structure

class InstaSession(requests.Session):
    __auth_page_url = 'https://instagram.com/accounts/login/'
    __auth_url = 'https://instagram.com/accounts/login/ajax/'
    __default_headers = {
            'authority': 'www.instagram.com',
            'origin': 'https://www.instagram.com',
            'x-ig-www-claim': 'hmac.AR36IPRJfr73424ue2ZSk-zrEPGPYMeS9MAmUUyHmWWBNp71',
            'x-instagram-ajax': 'a51d664a936c',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 YaBrowser/19.12.3.332 (beta) Yowser/2.5 Safari/537.36',
            'x-csrftoken': 'Elm4zr4OlCOYBPLOJWAEawrHwoe4gMV4',
            'dnt': '1',
            'x-ig-app-id': '936619743392459',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://www.instagram.com/accounts/login/?source=auth_switcher',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'ru,en;q=0.9,la;q=0.8',
        }

    def authenticate(self, username, password):
        auth_data = {
            'username': username,
            'password': password,
            'queryParams': '{"source":"auth_switcher"}',
            'optIntoOneTap': 'false'
            }
        self.set_default()
        page_with_csrf_token = self.get(InstaSession.__auth_page_url)
        self.headers.update({'x-csrftoken': page_with_csrf_token.cookies.get('csrftoken')})
        return self.post(InstaSession.__auth_url, data=auth_data).status_code

    def set_default(self):
        self.headers.update(InstaSession.__default_headers)


class InstaScraper():
    def __init__(self, session):
        self.__post_data_url = 'https://instagram.com/p/{shortcode}/?__a=1'
        self.__user_data_url = 'https://instagram.com/{username}/?__a=1'
        self.__tag_data_url = 'https://instagram.com/explore/tags/{tag_name}/?__a=1'
        self.__location_data_url = 'https://instagram.com/explore/locations/{location_id}/?__a=1'
        self.__graphql_query_url = 'https://instagram.com/graphql/query/'
        self.__session = session
        self.__QUERY_HASH = {
            'subscriptions': 'd04b0a864b4b54837c0d870b0e77e076',
            'followers': 'c76146de99bb02f6415203be841dd25a',
            'posts': 'e769aa130647d2354c40ea6a439bfc08',
            'tagged': 'ff260833edf142911047af6024eb634a',
            'story': '1ae3f0bfeb29b11f7e5e842f9e9e1c85',
            'comments': 'bc3296d1ce80a24b1b6e40b1e72903f5',
            'likes': 'd5d763b1e2acf209d62d22d184488e57',
            'tag_post': 'bd33792e9f52a56ae8fa0985521d141d',
            'location_post': '1b84447a4d8b6d6d0426fefb34514485'
        }

    def __get_single_entity_json(self, url):
        scraped_json = self.__session.get(url)
        return scraped_json
    
    def __get_json_value_by_key(self, scraped_json, target_node):
        if isinstance(scraped_json, dict):
            keys = list(scraped_json.keys())
            for key in keys:
                if key == target_node:
                    result = scraped_json.get(key)
                else:
                    result = self.__get_json_value_by_key(scraped_json.get(key), target_node)
                if result != None: 
                    return result #I CAN FUCKING MAKE YIELD
            raise Exception('Бля, братан, заебал')

    def __get_multiple_entity_json(self, id, query_hash, records_count=25):
        type_def_by_query_hash = {
            self.__QUERY_HASH['subscriptions']: 'id',
            self.__QUERY_HASH['followers']: 'id',
            self.__QUERY_HASH['location_post']: 'id',
            self.__QUERY_HASH['posts']: 'id',
            self.__QUERY_HASH['tag_post']: 'tag_name',
            self.__QUERY_HASH['likes']: 'shortcode',
            self.__QUERY_HASH['comment']: 'shortcode'
        }
        type_var = type_def_by_query_hash[query_hash]
        variables = '"{type_var}":"{user_id}",'.format(type_var=type_var, user_id=id)
        params = {
            'query_hash': query_hash,
            'variables':"{" + variables + "}"
        }

        after_value = ''
        entity_list = []
        has_next_page = True

        while has_next_page:
            response = self.__session.get(self.__graphql_query_url, params=params)
            entity_list.extend(self, self.__get_json_value_by_key(response, 'edges'))
            after_value = self.__get_json_value_by_key(response, 'end_cursor')
            params['variables'] = '{' + variables + f',"after":"{after_value}"' + '}'
            has_next_page = self.__get_json_value_by_key(response, 'has_next_page')

        return entity_list

    def get_user_json(self, username):
        user_json = self.__get_single_entity_json(self.__user_data_url.format(username=username))
        return user_json

    def get_post_json(self, shortcode):
        post_json = self.__get_single_entity_json(self.__post_data_url.format(shortcode=shortcode))
        return post_json

    def get_tag_json(self, tag_name):
        tag_json = self.__get_single_entity_json(self.__tag_data_url.format(tag_name=tag_name))
        return tag_json

    def get_location_json(self, location_id):
        location_json = self.__get_single_entity_json(self.__location_data_url.format(location_id=location_id))
        return location_json

    def get_user_subscribers(self, user):
        subs_json = self.__get_multiple_entity_json(user, self.__QUERY_HASH['subscriptions'])
        subscriptions = [self.get_user_json(self.__get_json_value_by_key(sub, 'username')) for sub in subs_json]
        return subscriptions

    def get_user_followers(self, user):
        followers_json = self.__get_multiple_entity_json(user, id , self.__QUERY_HASH['followers'])
        followers = [self.get_user_json(self.__get_json_value_by_key(follower, 'username')) for follower in followers_json]
        return followers

    def get_user_posts(self, user):
        users_posts_json = self.__get_multiple_entity_json(user, id, self.__QUERY_HASH['posts'])
        posts = [self.get_post_json(self.__get_json_value_by_key(post, 'shortcode')) for post in users_posts_json]
        return posts
       

class JSONParser():
    def __init__(self):
        pass
    
    def parse_user(self, json):
        pass

    def parse_tag(self, json):
        pass

    def parse_location(self, json):
        pass

    def parse_post(self, json):
        pass

    def parse_user_list(self, json_list):
        pass

    def parse_posts_list(self, json_list):
        pass


class InstaAction():
    def __init__(self, session):
        self.__sessioin = session

        # self.GRAPHQL_QUERY_URL = BASE_URL + 'graphql/query/'
        # self.LIKE_QUERY_URL = BASE_URL + 'web/likes/{media_id}/like/'
        # self.UNLIKE_QUERY_URL = BASE_URL + 'web/likes/{media_id}/unlike/'
        # self.SAVE_MEDIA_QUERY_URL = BASE_URL + 'web/save/{media_id}/save/'
        # self.COMMENT_QUERY_URL = BASE_URL + 'web/comments/{media_id}/add/'
        # self.FOLLOW_QUERY_URL = BASE_URL + 'web/friendships/{user_id}/follow/'
        # self.UNFOLLOW_QUERY_URL = BASE_URL + 'web/friendships/{user_id}/unfollow/'

    def like(self, shortcode):
        pass

    def unlike(self, shortcode):
        pass

    def follow(self, username):
        pass

    def unfollow(self, username):
        pass

    def leave_comment(self, shortcode, comment_text):
        pass


class InstaFacade():
    def __init__(self, username, password):
        self.current_session = InstaSession()
        self.current_session.set_default()

        print(self.current_session.authenticate(username, password))

        self.scraper = InstaScraper(self.current_session)
        self.actions = InstaAction(self.current_session)
        self.parser = JSONParser()
