# coding:utf-8

import datetime
import requests
import os
import shutil
from werkzeug.local import LocalProxy
from flask import current_app

import settings
from .core import mail, db
from .factory import create_celery_app
from .signals import artifact_asset_html5_url_update_signal, artifact_asset_boxview_url_update_signal
from .qinius import mk_image_thumbnail, rm_image_thumbnail, rm_key
from .boxview import boxview_client
from .errors import BoxViewError
from .utils import utc_to_localtime, unzip
from .es import es_client


celery = create_celery_app()

_logger = LocalProxy(lambda: current_app.logger)


@celery.task(bind=True)
def send_email(self,message):
    try:
        mail.send(message)
    except Exception as exc:
        _logger.error("send_mail error", exc)
        raise self.retry(exc=exc)


@celery.task(bind=True)
def gen_qiniu_thumbnail(self, key_or_url, image_sizes):
    try:
        mk_image_thumbnail(key_or_url=key_or_url, image_sizes=image_sizes)
    except Exception as exc:
        _logger.error("gen_qiniu_thumbnail error, key_or_url:" + key_or_url, exc)
        raise self.retry(exc=exc)

@celery.task(bind=True)
def remove_qiniu_thumbnail(self, key_or_url, image_sizes):
    try:
        rm_image_thumbnail(key_or_url=key_or_url, image_sizes=image_sizes)
    except Exception as exc:
        _logger.error("remove_qiniu_thumbnail, key_or_url:" + key_or_url, exc)
        raise self.retry(exc=exc)


@celery.task(bind=True)
def remove_qiniu_key(self, key_or_url):
    try:
        rm_key(key_or_url)
    except Exception as exc:
        _logger.error("remove_qiniu_key, key_or_url:" + key_or_url, exc)
        raise self.retry(exc=exc)


@celery.task(bind=True)
def gen_html5_file(self, media_file, artifact_id, dest_dir):
    if type(dest_dir) != unicode:
        dest_dir = dest_dir.decode('utf-8', 'ignore')
    try:
        local_filename = os.path.join(settings.tmp_dir, media_file.split('/')[-1])
        r = requests.get(media_file, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

        if local_filename.endswith('zip'):
            unzip(local_filename, dest_dir)
            os.remove(local_filename)
        
        dir_name = os.listdir(dest_dir)[0]
        if type(dir_name) != unicode:
            dir_name = dir_name.decode('utf-8', 'ignore')
        html5_qiniu_url = os.path.join(settings.qiniu_html5_prefix, dest_dir[len(settings.qiniu_sync_dir):], dir_name,
                                       "index.html")
        artifact_asset_html5_url_update_signal.send(current_app._get_current_object(), artifact_id=artifact_id,
                                                    media_file=media_file, view_url=html5_qiniu_url)
    except Exception as exc:
        _logger.error('gen_html_file error, media_file:%s, artifact_id: %s, dest_dir:%s' %(media_file, artifact_id, dest_dir) ,exc)
        raise self.retry(exc=exc)



@celery.task(bind=True)
def remove_html5_file(self, url, artifact_id, dest_dir):
    try:
        shutil.rmtree(dest_dir, ignore_errors=True)
        rm_key(url)
    except Exception as exc:
        _logger.error("remove_html5_file error, url:%s, artifact_id:%s, dest_dir:%s" %(url, artifact_id, dest_dir), exc)
        self.retry(exc=exc)


# @celery.task
# def gen_boxview_doc(artifact_id, url):
# print "task gen_boxview_doc", artifact_id, url
# from .models import BoxViewFile
#
# try:
#         document = boxview_client.upload_document(url).json()
#         print document
#         document_id = document.get("id", None)
#
#
#         if document_id:
#             created_at = utc_to_localtime(document.get("created_at"))
#             result = document.get("status")
#             boxview_file = BoxViewFile(document_id=document_id,
#                                        artifact_id=artifact_id,
#                                        media_file=url,
#                                        created_at=created_at,
#                                        result=result
#             )
#             db.session.add(boxview_file)
#             db.session.commit()
#     except BoxViewError, e:
#         _logger.exception(e)


@celery.task(bind=True)
def gen_boxview_doc(self, artifact_id, url):
    # print "task gen_boxview_doc", artifact_id, url
    from .models import BoxViewFile

    try:
        document = boxview_client.upload_document(url).json()
        document_id = document.get("id", None)
        if document_id:
            created_at = utc_to_localtime(document.get("created_at"))
            result = document.get("status")
            boxview_file = BoxViewFile(document_id=document_id,
                                       artifact_id=artifact_id,
                                       media_file=url,
                                       created_at=created_at,
                                       result=result
            )
            db.session.add(boxview_file)
            db.session.commit()
            gen_boxview_session_url.apply_async((artifact_id, url, document_id), countdown=120)

        # print "gen_boxview_doc end"
    except Exception as exc:
        _logger.error("gen_boxview_doc error, artifact_id:%s, url:%s" % (artifact_id,url), exc)
        self.retry(exc=exc)


@celery.task(bind=True)
def remove_boxview_doc(self, artifact_id, url):
    # print "task remove_boxview_doc", artifact_id, url
    from .models import BoxViewFile
    try:
        boxview_file = BoxViewFile.query.filter(BoxViewFile.artifact_id == artifact_id,
                                            BoxViewFile.media_file == url).first()
        if boxview_file:
            boxview_client.delete_document(boxview_file.document_id)
            db.session.delete(boxview_file)
            db.session.commit()
    except Exception as exc:
        _logger.error("remove_boxview_doc error, artifact_id:%s, url:%s" % (artifact_id,url), exc)
        self.retry(exc=exc)



# @celery.task
# def gen_boxview_session_url(artifact_id, media_file, boxview_document_id):
#     print "task gen_boxview_session_url", artifact_id, media_file, boxview_document_id
#     try:
#         api_response = boxview_client.create_session(boxview_document_id)
#         boxview_session = api_response.json()
#         boxview_session_url = boxview_client.create_session_url(boxview_session['id'])
#         artifact_asset_view_url_update_signal.send(current_app._get_current_object(), artifact_id=artifact_id,
#                                                    media_file=media_file, view_url=boxview_session_url)
#     except BoxViewError, e:
#         _logger.exception(e)


@celery.task
def gen_boxview_session_url(artifact_id, media_file, boxview_document_id):
    from .models import BoxViewFile

    # print "task gen_boxview_session_url", artifact_id, media_file, boxview_document_id
    try:
        status = boxview_client.get_document_status(boxview_document_id)
        if status == "done":
            api_response = boxview_client.create_session(boxview_document_id)
            boxview_session = api_response.json()
            boxview_session_url = boxview_client.create_session_url(boxview_session['id'])
            artifact_asset_boxview_url_update_signal.send(current_app._get_current_object(), artifact_id=artifact_id,
                                                       media_file=media_file, view_url=boxview_session_url)

        if status == "done" or status == "error":
            boxview_file = BoxViewFile.query.get(boxview_document_id)
            if boxview_file:
                boxview_file.result = status
                boxview_file.triggered_at = datetime.datetime.now()
                db.session.commit()
        else:
            gen_boxview_session_url.apply_async((artifact_id, media_file, boxview_document_id), countdown=120)

    except BoxViewError, e:
        _logger.exception(e)


@celery.task
def es_index_doc(doc_type, doc_id, doc, **kwargs):
    es_client.index_doc(doc_type, doc_id, doc, **kwargs)


@celery.task
def es_delete_doc(doc_type, doc_id):
    es_client.delete_doc(doc_type, doc_id)


