# coding:utf-8


from itsdangerous import text_type
import os
from ..tasks import gen_qiniu_thumbnail, remove_qiniu_thumbnail, remove_qiniu_key, gen_html5_file, remove_html5_file, \
    gen_boxview_doc, remove_boxview_doc
from .. import settings


def profile_image_add_handler(profile_image, user_id, artifact_id):
    if profile_image:
        gen_qiniu_thumbnail.delay(profile_image, ["200x200", "400x400", "800x800"])


def profile_image_remove_handler(profile_image, user_id, artifact_id):
    if profile_image:
        remove_qiniu_key.delay(profile_image)
        remove_qiniu_thumbnail.delay(profile_image, ["200x200", "400x400", "800x800"])


def media_image_add_handler(media_image, user_id, artifact_id):
    gen_qiniu_thumbnail.delay(media_image, ["400x300", "800x600", "1024x768"])


def media_image_remove_handler(media_image, user_id, artifact_id):
    remove_qiniu_key.delay(media_image)
    remove_qiniu_thumbnail.delay(media_image, ["400x300", "800x600", "1024x768"])


def boxview_add_handler(media_file, user_id, artifact_id):
    if media_file:
        gen_boxview_doc.delay(artifact_id, media_file)


def boxview_remove_handler(media_file, user_id, artifact_id):
    if media_file:
        remove_boxview_doc.delay(artifact_id, media_file)


def html5_add_handler(media_file, user_id, artifact_id):
    pass
    # if media_file:
    #     key = media_file[media_file.rindex('/') + 1:]
    #     artifact_html5_dir = os.path.join(settings.qiniu_sync_dir, str(user_id), str(artifact_id), key)
    #     gen_html5_file.delay(media_file, artifact_id, artifact_html5_dir)


def html5_remove_handler(media_file, user_id, artifact_id):
    if media_file:
        key = media_file[media_file.rindex('/') + 1:]
        artifact_html5_dir = os.path.join(settings.qiniu_sync_dir, str(user_id), str(artifact_id), key)
        remove_html5_file.delay(media_file, artifact_id, artifact_html5_dir)


def video_add_handler(media_file, user_id, artifact_id):
    pass


def video_remove_handler(media_file, user_id, artifact_id):
    if media_file:
        remove_qiniu_key.delay(media_file)


def video_link_add_handler(asset, user_id, artifact_id):
    pass


def video_link_remove_handler(media_file, user_id, artifact_id):
    pass


def d3_add_handler(media_file, user_id, artifact_id):
    pass


def d3_remove_handler(media_file, user_id, artifact_id):
    if media_file:
        remove_qiniu_key.delay(media_file)


def zip_add_handler(media_file, user_id, artifact_id):
    pass


def zip_remove_handler(media_file, user_id, artifact_id):
    if media_file:
        remove_qiniu_key.delay(media_file)


def flash_add_handler(media_file, user_id, artifact_id):
    pass


def flash_remove_handler(media_file, user_id, artifact_id):
    if media_file:
        remove_qiniu_key.delay(media_file)

def pdf_add_handler(media_file, user_id, artifact_id):
    pass


def pdf_remove_handler(media_file, user_id, artifact_id):
    if media_file:
        remove_qiniu_key.delay(media_file)



_asset_handlers = {
    "0": ("profile_image", profile_image_add_handler, profile_image_remove_handler),
    "1": ("image", media_image_add_handler, media_image_remove_handler),
    "2": ("ppt", boxview_add_handler, boxview_remove_handler),
    "4": ("video", video_add_handler, video_remove_handler),
    "8": ("video_link", video_link_add_handler, video_link_remove_handler),
    "16": ("3d", d3_add_handler, d3_remove_handler),
    "32": ("zip", zip_add_handler, zip_remove_handler),
    "64": ("flash", flash_add_handler, flash_remove_handler),
    "128": ("pdf", pdf_add_handler, pdf_remove_handler),
    "256": ("html5", html5_add_handler, html5_remove_handler),
}


def asset_add_handler(asset_type):
    handlers = _asset_handlers.get(str(asset_type), None)
    if handlers:
        return handlers[1]
    else:
        return None


def asset_remove_handler(asset_type):
    handlers = _asset_handlers.get(str(asset_type), None)
    if handlers:
        return handlers[2]
    else:
        return None
    


