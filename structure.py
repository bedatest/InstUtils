from datetime import datetime
from dataclasses import dataclass
import json
import re 


@dataclass
class User():
    id: str = ''
    username: str = ''
    biography: str = ''
    business_category_name: str = ''
    full_name: str = ''
    blocked_by_viewer: bool = False
    followed_by_viewer: bool = False
    follows_viewer: bool = False
    external_url: str = ''
    has_channel: bool = False
    has_requested_viewer: bool = False
    requested_by_viewer: bool = False
    is_business_account: bool = False
    is_private: bool = False
    is_verified: bool = False
    profile_pic_url: str = ''
    subscriptions_count: int = 0
    followers_count: int = 0
    mutual_users_count: int = 0
    posts_count: int = 0
    last_update = datetime.now()
 
    def __repr__(self):
        return f'<User: {self.username} with name "{self.full_name}">'


@dataclass
class Post():
    id: str = ''
    shortcode: str = ''
    caption: str = ''
    likes_count: int = 0
    comments_count: int = 0
    caption_is_edited: bool = False
    has_ranked_comments: bool = False
    taken_at_timestamp: str = ''
    viewer_has_liked: bool = False
    viewer_has_saved: bool = False
    viewer_can_reshare: bool = False
    gating_info: str = ''
    fact_check_overall_rating: any = ''
    fact_check_information: any = ''
    comments_disabled: bool = False
    is_ad: bool = False
    display_url: str = ''
    accessibility_caption: str = ''
    viewer_in_photo_of_you: bool = False

    def __repr__(self):
        return f'<Post with id {self.id}>'


@dataclass
class Tag():
    id: str = ''
    name: str = ''
    is_following: bool = False
    allow_following: bool = False
    count: int = 0
        
    def __repr__(self):
        return f'<{self.name} with id {self.id}>'


@dataclass
class Location():
    id: str = ''
    name: str = ''
    has_public_page: bool = False
    slug: str = ''
    website: str = ''
    blurb: any = ''
    phone: str = ''
    primary_alias_on_fb: str = ''
    lat: any = ''
    lng: any = ''
    street: str = ''
    zip_code: str = ''
    posts_count: int = 0
    country: str = ''
    city: str = ''
    last_update = datetime.now()
        
    def __repr__(self):
        return f'<{self.name} with id {self.id}>'
