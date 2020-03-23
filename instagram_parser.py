import requests
import json

import structure
class IDataSource():
    def get_user(self, username):
       raise NotImplementedError("For correct working this method needs to be implemented")

    def get_post(self, shotrcode): # TODO 10: Check hash code for tag posts and user posts
       raise NotImplementedError("For correct working this method needs to be implemented")

    def get_tag(self, post):
       raise NotImplementedError("For correct working this method needs to be implemented")

    def get_location(self, id):
       raise NotImplementedError("For correct working this method needs to be implemented")

    def get_subscriptions(self, post):
       raise NotImplementedError("For correct working this method needs to be implemented")

    def get_followers(self, user):
       raise NotImplementedError("For correct working this method needs to be implemented")

    def get_post_list(self, post):
       raise NotImplementedError("For correct working this method needs to be implemented")


class InstaParser(IDataSource):
    def __init__(self, session):
        self.__post_url = 'https://instagram.com/p/{shortcode}/?__a=1'
        self.__user_url = 'https://instagram.com/{username}/?__a=1'
        self.__tag_url = 'https://instagram.com/explore/tags/{tag_name}/?__a=1'
        self.__location_url = 'https://instagram.com/explore/locations/{location_id}/?__a=1'
        self.__graphql_url = 'https://instagram.com/graphql/query/'
        self.__session = session
        self.__query_metadata = {
            'subscriptions': {
                'query_hash': 'd04b0a864b4b54837c0d870b0e77e076',
                'def': 'id'
            },
            'followers': {
                'query_hash': 'c76146de99bb02f6415203be841dd25a',
                'def': 'id'
            },
            'posts': {
                'query_hash': 'e769aa130647d2354c40ea6a439bfc08',
                'url': 'https://instagram.com/p/{shortcode}/?__a=1',
                'def': 'id'
            },
            'tagged': {
                'query_hash': 'ff260833edf142911047af6024eb634a'
            },
            'story': {
                'query_hash': '1ae3f0bfeb29b11f7e5e842f9e9e1c85'
            },
            'comments': {
                'query_hash': 'bc3296d1ce80a24b1b6e40b1e72903f5',
                'def': 'shortcode'
            },
            'likes': {
                'query_hash': 'd5d763b1e2acf209d62d22d184488e57',
                'def': 'shortcode'
            },
            'tag_post': {
                'query_hash': 'bd33792e9f52a56ae8fa0985521d141d',
                'def': 'tag_name'
            },
            'location_post': {
                'query_hash': '1b84447a4d8b6d6d0426fefb34514485',
                'def': 'id'
            }
        }

    def __get_single_json(self, url):
        scraped_json = self.__session.get(url)
        return json.loads(scraped_json.text)
    
    def __get_node_by_key(self, dictionary, target_node):
        if isinstance(dictionary, dict):
            result = None
            keys = list(dictionary.keys())
            for key in keys:
                if key == target_node:
                    result = dictionary.get(key)
                else:
                    result = result or self.__get_node_by_key(dictionary.get(key), target_node)
            return result
        else:
            return None

    def __get_multiple_json(self, id, query_metadata, records_count=240):
        variables = {
                query_metadata['def']: str(id),
                'include_reel': True,
                'fetch_mutual': True,
                'first': records_count
            }
        params = {
            'query_hash': query_metadata['query_hash'],
            'variables': json.dumps(variables)
        }

        edge_list = []
        has_next_page = True
        while has_next_page:
            response = json.loads(self.__session.get(self.__graphql_url, params=params).text)
            edges = self.__get_node_by_key(response, 'edges')
            edge_list.extend(edges)
            has_next_page = self.__get_node_by_key(response, 'has_next_page')
            variables['after'] = self.__get_node_by_key(response, 'end_cursor')
            params['variables'] = json.dumps(variables)

        return edge_list

    def get_user(self, username):
        user_json = self.__get_single_json(self.__user_url.format(username=username))
        #CHECK JSON
        base_node = user_json['graphql']['user']
        user = structure.User(
            id = base_node['id'],
            username = base_node['username'],
            biography = base_node['biography'],
            business_category_name = base_node['business_category_name'],
            full_name = base_node['full_name'],
            blocked_by_viewer = base_node['blocked_by_viewer'],
            followed_by_viewer = base_node['followed_by_viewer'],
            follows_viewer = base_node['follows_viewer'],
            external_url = base_node['external_url'],
            has_channel = base_node['has_channel'],
            has_requested_viewer = base_node['has_requested_viewer'],
            requested_by_viewer = base_node['requested_by_viewer'],
            is_business_account = base_node['is_business_account'],
            is_private = base_node['is_private'],
            is_verified = base_node['is_verified'],
            profile_pic_url = base_node['profile_pic_url_hd'],
            subscriptions_count = base_node['edge_follow']['count'],
            followers_count = base_node['edge_followed_by']['count'],
            mutual_users_count = base_node['edge_mutual_followed_by']['count'],
            posts_count = base_node['edge_owner_to_timeline_media']['count'],
            last_update = "datetime.now()" #LOOK AT ME
        )
        return user

    def get_post(self, shortcode):
        post_json = self.__get_single_json(self.__post_url.format(shortcode=shortcode))
        #TODO: CHECK JSON
        base_node = post_json['graphql']['shortcode_media']
        caption_edge = base_node['edge_media_to_caption']['edges']
        caption = "" if len(caption_edge) == 0 else caption_edge[0]['node']['text']
        post = structure.Post(
            id = base_node['id'],
            shortcode = base_node['shortcode'],
            caption = caption,
            likes_count = base_node['edge_media_preview_like']['count'],
            comments_count = base_node['edge_media_preview_comment']['count'],
            caption_is_edited = base_node['caption_is_edited'],
            has_ranked_comments = base_node['has_ranked_comments'],
            taken_at_timestamp = base_node['taken_at_timestamp'],
            viewer_has_liked = base_node['viewer_has_liked'],
            viewer_has_saved = base_node['viewer_has_saved'],
            viewer_can_reshare = base_node['viewer_can_reshare'],
            gating_info = base_node['gating_info'],
            fact_check_overall_rating = base_node['fact_check_overall_rating'],
            fact_check_information = base_node['fact_check_information'],
            comments_disabled = base_node['comments_disabled'],
            is_ad = base_node['is_ad'],
            display_url = base_node['display_url'],
            viewer_in_photo_of_you = base_node['viewer_in_photo_of_you']
        )
        return post

    def get_tag(self, tag_name):
        tag_json = self.__get_single_json(self.__tag_url.format(tag_name=tag_name))
        #TODO: JSON CHECKING
        base_node = tag_json['graphql']['hashtag']
        tag = structure.Tag(
           name = base_node['name'],
           is_following = base_node['is_following'],
           allow_following = base_node['allow_following'],
           count = base_node['edge_hashtag_to_media']['count']
        )
        return tag

    def get_location(self, location_id):
        location_json = self.__get_single_json(self.__location_url.format(location_id=location_id))
        base_node = location_json['qraphql']['location']
        location = structure.Location(
            id = base_node['id'],
            name = base_node['name'],
            has_public_page = base_node['has_public_page'],
            slug = base_node['slug'],
            website = base_node['website'],
            blurb = base_node['blurb'],
            phone = base_node['phone'],
            primary_alias_on_fb = base_node['primary_alias_on_fb'],
            lat = base_node['lat'],
            lng = base_node['lng'],
            street = base_node['address_json']['street_address'],
            zip_code = base_node['address_json']['zip_code'],
            posts_count = base_node['edge_location_to_media']['count'],
            country = base_node['directory']['country']['name'],
            city = base_node['directory']['city']['name']
        )
        return location

    def get_subscriptions(self, user):
        subs_json = self.__get_multiple_json(user.id, self.__query_metadata['subscriptions'])
        subscriptions = [self.get_user(self.__get_node_by_key(sub, 'username')) for sub in subs_json]
        return subscriptions

    def get_followers(self, user):
        followers_json = self.__get_multiple_json(user.id, self.__query_metadata['followers'])
        followers = [self.get_user(self.__get_node_by_key(follower, 'username')) for follower in followers_json]
        return followers

    def get_post_list(self, user):
        posts_json = self.__get_multiple_json(user.id, self.__query_metadata['posts'])
        posts = [self.get_post(self.__get_node_by_key(post, 'shortcode')) for post in posts_json]
        return posts
       

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


class InstaAnalyser():
    def __init__(self, data_source):
        self.__data_source = data_source
    
    def get_top_liked_post(self, user):
        pass

    def get_top_commented_post(self, user):
        pass

    def get_most_active_followers_by_like(self, user):
        pass


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


class InstaFacade():
    def __init__(self, username, password):
        self.current_session = InstaSession()
        self.current_session.set_default()

        print(self.current_session.authenticate("bedanatic", "Subscribe"))

        self.scraper = InstaParser(self.current_session)
        self.actions = InstaAction(self.current_session)
