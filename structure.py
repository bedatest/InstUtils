from datetime import datetime
import json
import re 

#TODO: -Add decorator Ban Protection
#TODO: -Add action with media(like/unlike/comment) and user(follow/unfollow) 
class User():
    def __init__(self, raw_json):
        base_node = raw_json['graphql']['user']

        self.id = base_node['id']
        self.username = base_node['username']
        self.biography = base_node['biography']
        self.business_category_name = base_node['business_category_name']
        self.full_name = base_node['full_name']
        self.blocked_by_viewer = base_node['blocked_by_viewer']
        self.followed_by_viewer = base_node['followed_by_viewer']
        self.follows_viewer = base_node['follows_viewer']
        self.external_url = base_node['external_url']
        self.has_channel = base_node['has_channel']
        self.has_requested_viewer = base_node['has_requested_viewer']
        self.requested_by_viewer = base_node['requested_by_viewer']
        self.is_business_account = base_node['is_business_account']
        self.is_private = base_node['is_private']
        self.is_verified = base_node['is_verified']
        self.profile_pic_url = base_node['profile_pic_url_hd']
        self.subscriptions_count = base_node['edge_follow']['count']
        self.followers_count = base_node['edge_followed_by']['count']
        self.mutual_users_count = base_node['edge_mutual_followed_by']['count']
        self.posts_count = base_node['edge_owner_to_timeline_media']['count']
        self.last_update = datetime.now()

        self.posts = []
        self.associated_tags = []

        self.raw = raw_json

    #show all data about user
    #TODO: fill posts, tags
    def extract_tag_from_biography():
        pass

    def __repr__(self):
        return f'<User: {self.username} with name "{self.full_name}">'



class Post():

    def __init__(self, raw_json):
        base_node = raw_json['graphql']['shortcode_media']

        self.id = base_node['id']
        self.shortcode = base_node['shortcode']
        self.caption = base_node['edge_media_to_caption']['edges'][0]['node']['text']
        self.likes_count = base_node['edge_media_preview_like']['count']
        self.comments_count = base_node['edge_media_preview_comment']['count']
        self.caption_is_edited = base_node['caption_is_edited']
        self.has_ranked_comments = base_node['has_ranked_comments']
        self.taken_at_timestamp = base_node['taken_at_timestamp']
        self.viewer_has_liked = base_node['viewer_has_liked']
        self.viewer_has_saved = base_node['viewer_has_saved']
        self.viewer_can_reshare = base_node['viewer_can_reshare']
        self.gating_info = base_node['gating_info']
        self.fact_check_overall_rating = base_node['fact_check_overall_rating']
        self.fact_check_information = base_node['fact_check_information']
        self.comments_disabled = base_node['comments_disabled']
        self.is_ad = base_node['is_ad']
        self.display_url = base_node['display_url']
        self.accessibility_caption = base_node['accessibility_caption']
        self.viewer_in_photo_of_you = base_node['viewer_in_photo_of_you']

        self.owner = None
        self.location = None
        self.comments = []
        self.tagged_users = []
        self.tags = []
        
        self.raw = raw_json
    
    def extract_tag_from_descriptioin(description):
        pass
    def __repr__(self):
        return f'<Post with id {self.id}>'


class Tag():

    def __init__(self, raw_json):
        base_node = raw_json['graphql']['hashtag']
        self.id = base_node['id']
        self.name = base_node['name']
        self.is_following = base_node['is_following']
        self.allow_following = base_node['allow_following']
        self.count = base_node['edge_hashtag_to_media']['cout']
        self.related_tags = []
        
    def __repr__(self):
        return f'<{self.name} with id {self.id}>'


class Location():

    def __init__(self, raw_json):
        base_node = raw_json['qraphql']['location']
        address_json = json.loads(base_node['address_json'])

        self.id = base_node['id']
        self.name = base_node['name']
        self.has_public_page = base_node['has_public_page']
        self.slug = base_node['slug']
        self.website = base_node['website']
        self.blurb = base_node['blurb']
        self.phone = base_node['phone']
        self.primary_alias_on_fb = base_node['primary_alias_on_fb']
        self.coord = {
            'lat': base_node['lat'], 
            'lng': base_node['lng']
            }
        self.street = address_json['street_address']
        self.zip_code = address_json['zip_code']
        self.posts_count = base_node['edge_location_to_media']['count']
        self.country = base_node['directory']['country']['name']
        self.city = base_node['directory']['city']['name']
        self.last_update = datetime.now()
        self.raw = raw_json
        
    def __repr__(self):
        return f'<{self.name} with id {self.id}>'

class Comment():
    def __init__(self):
        self.author = None #Author must be here
        self.text = ''
        self.likes_count = 0
        self.count_of_reply = 0