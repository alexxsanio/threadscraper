from __future__ import annotations
from datetime import datetime
from typing import Any, Dict, Optional
from .utils.logger import get_logger
import jmespath

logger = get_logger(__name__)
class ThreadsParser:

    def parse_thread(self, data: Dict) -> Dict:
        result = jmespath.search(
            """{
            text: post.caption.text,
            published_on: post.taken_at,
            id: post.id,
            pk: post.pk,
            code: post.code,
            username: post.user.username,
            user_pic: post.user.profile_pic_url,
            user_verified: post.user.is_verified,
            user_pk: post.user.pk,
            user_id: post.user.id,
            has_audio: post.has_audio,
            reply_count: post.text_post_app_info.direct_reply_count,
            like_count: post.like_count,
            reshare_count: post.text_post_app_info.reshare_count,
            repost_count: post.text_post_app_info.repost_count,
            images: post.carousel_media[].image_versions2.candidates[1].url,
            image_count: post.carousel_media_count,
            videos: post.video_versions[].url
        }""",
            data,
        )
        result["videos"] = list(set(result["videos"] or []))
        if result["reply_count"] and type(result["reply_count"]) != int:
            result["reply_count"] = int(result["reply_count"].split(" ")[0])
        result[
            "url"
        ] = f"https://www.threads.net/@{result['username']}/post/{result['code']}"
        return result

    def parse_profile(self, data: Dict) -> Dict:
        """Parse Threads profile JSON dataset for the most important fields"""
        result = jmespath.search(
            """{
            is_private: text_post_app_is_private,
            is_verified: is_verified,
            profile_pic: hd_profile_pic_versions[-1].url,
            username: username,
            full_name: full_name,
            bio: biography,
            bio_links: bio_links[].url,
            followers: follower_count
        }""",
            data,
        )
        result["url"] = f"https://www.threads.net/@{result['username']}"
        return result