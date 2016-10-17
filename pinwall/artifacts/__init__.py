# coding: utf-8

from flask import current_app
from .models import Artifact, Term, ArtifactAsset, ArtifactComment, ArtifactScore, Topic
from ..core import db, cache, cache_registry, Service
from ..signals import *
from .asset_handlers import asset_add_handler, asset_remove_handler
from ..utils import AttrDict
from ..settings import cache_timeout


class ArtifactService(Service):
    __model__ = Artifact

    @cache.memoize(timeout=cache_timeout)
    def artifact_by_id(self, artifact_id):
        artifact = self.get(artifact_id)
        if artifact:
            return artifact.to_cache_dict()
        else:
            return None

    @cache.memoize(timeout=cache_timeout)
    def artifact_by_userid(self, user_id):
        user_artifact = {"artifact_ids": [], "honor_sum": 0}
        artifact_ids = Artifact.query.with_entities(Artifact.id).filter(Artifact.user_id == user_id) \
            .order_by(db.desc(Artifact.created_at)).all()
        if artifact_ids:
            honor_sum = Artifact.query.join(ArtifactScore,
                                            db.and_(Artifact.id == ArtifactScore.artifact_id,
                                                    Artifact.user_id == user_id, ArtifactScore.score == 1)) \
                .with_entities(db.func.count(ArtifactScore.artifact_id)).scalar()

            user_artifact['artifact_ids'] = map(lambda x: x[0], artifact_ids)
            user_artifact['honor_sum'] = honor_sum

        return user_artifact

    @cache.memoize(timeout=cache_timeout)
    def artifact_praised_by_userid(self, artifact_id, user_id):
        artifact_score = ArtifactScore.query.filter(ArtifactScore.artifact_id == artifact_id,
                                                    ArtifactScore.scorer_id == user_id).first()
        if artifact_score:
            return 1
        else:
            return 0

    def list_artifact_id(self, last_artifact_id=0, page_size=10):
        query = Artifact.query.with_entities(Artifact.id)
        if last_artifact_id:
            query = query.filter(Artifact.id < last_artifact_id)
        return map(lambda row: row[0], query.order_by(db.desc(Artifact.id)).limit(page_size).all())


    def create_artifact(self, **kwargs):
        artifact = self.create(**kwargs)
        artifact_create_signal.send(current_app._get_current_object(), artifact=artifact)
        user_top_10_artifacts_signal.send(current_app._get_current_object(), user_id=artifact.user_id)
        post_create_artifact(artifact)

    def update_artifact(self, artifact, post_update=True, **kwargs):

        # if pre_update:
        # pre_update_artifact(artifact, kwargs)
        artifact_dict = _artifact_dict_from_cache(artifact.id)
        self.update(artifact, **kwargs)
        artifact_update_signal.send(current_app._get_current_object(), artifact=artifact)
        if post_update:
            post_update_artifact(artifact_dict, kwargs)

    def delete_artifact(self, artifact):
        artifact_dict = _artifact_dict_from_cache(artifact.id)
        self.delete(artifact)
        artifact_delete_signal.send(current_app._get_current_object(), artifact=artifact)
        user_top_10_artifacts_signal.send(current_app._get_current_object(), user_id=artifact.user_id)
        if artifact.topic_id is not None and artifact.topic_id > 0:
            topic = topicService.get_or_404(artifact.topic_id)
            topic_update_signal.send(current_app._get_current_object(), topic=topic)

        post_remove_artifact(AttrDict(artifact_dict))

    def append_comment(self, artifact_id, comment):
        artifact = self.get_or_404(artifact_id)
        artifact.comment_query.append(comment)
        self.save(artifact)
        artifact_update_signal.send(current_app._get_current_object(), artifact=artifact)
        artifact_comment_append_signal.send(current_app._get_current_object(), comment=comment)

    def remove_comment(self, artifact_id, comment):
        artifact = self.get_or_404(artifact_id)
        artifact.comment_query.remove(comment)
        self.save(artifact)
        artifact_update_signal.send(current_app._get_current_object(), artifact=artifact)
        artifact_comment_remove_signal.send(current_app._get_current_object(), comment=comment)

    def append_score(self, artifact_id, score):
        artifact = self.get_or_404(artifact_id)
        artifact.score_query.append(score)
        self.save(artifact)
        artifact_update_signal.send(current_app._get_current_object(), artifact=artifact)
        artifact_praised_signal.send(current_app._get_current_object(), artifact_id=artifact.id,
                                     scorer_id=score.scorer_id)
        if score.score == 1:
            user_top_10_artifacts_signal.send(current_app._get_current_object(), user_id=artifact.user_id)

    def remove_score(self, artifact_id, score):
        artifact = self.get_or_404(artifact_id)
        artifact.score_query.remove(score)
        self.save(artifact)
        artifact_update_signal.send(current_app._get_current_object(), artifact=artifact)
        artifact_praised_signal.send(current_app._get_current_object(), artifact_id=artifact.id,
                                     scorer_id=score.scorer_id)
        if score.score == 1:
            user_top_10_artifacts_signal.send(current_app._get_current_object(), user_id=artifact.user_id)


    def __repr__(self):
        return "pinwall.artifacts.ArtifactService"


class TopicService(Service):
    __model__ = Topic

    @cache.memoize(timeout=cache_timeout)
    def topic_by_id(self, topic_id):
        topic = self.get(topic_id)
        if topic:
            return topic.to_cache_dict()
        else:
            return None

    @cache.memoize(timeout=cache_timeout)
    def topic_ids_by_userid(self, user_id):
        topic_ids = Topic.query.with_entities(Topic.id).filter(Topic.user_id == user_id). \
            order_by(db.desc(Topic.created_at)).all()
        if topic_ids:
            return topic_ids
        else:
            return []

    @cache.memoize(timeout=cache_timeout)
    def first_load_artifact_ids(self, topic_id, limit=10):
        topic = self.get(topic_id)
        if topic:
            return topic.first_load_artifact_id(limit)
        else:
            return None

    def list_topic_id(self, last_topic_id=0, page_size=10, *filter_conditions):
        filter_conditions = list(filter_conditions)
        if last_topic_id:
            filter_conditions.append(Topic.id < last_topic_id)
        query = Topic.query.with_entities(Topic.id)
        for _filter in filter_conditions:
            query = query.filter(_filter)
        return map(lambda row: row[0], query.order_by(db.desc(Topic.id)).limit(page_size).all())

    def list_artifact_id(self, topic_id, last_artifact_id=0, page_size=10):
        topic = self.get_or_404(topic_id)
        query = topic.artifact_query.with_entities(Artifact.id)
        if last_artifact_id:
            query = query.filter(Artifact.id < last_artifact_id)
        return map(lambda row: row[0], query.order_by(db.desc(Artifact.id)).limit(page_size).all())

    def create_topic(self, **kwargs):
        topic = self.create(**kwargs)
        topic_create_signal.send(current_app._get_current_object(), topic=topic)

    def update_topic(self, topic, **kwargs):
        self.update(topic, **kwargs)
        topic_update_signal.send(current_app._get_current_object(), topic=topic)

    def delete_topic(self, topic):
        artifact_id_subquery = topic.artifact_query.with_entities(Artifact.id).subquery()
        Artifact.query.filter(Artifact.id.in_(artifact_id_subquery)).delete(synchronize_session=False)
        self.delete(topic)
        topic_delete_signal.send(current_app._get_current_object(), topic=topic)

    def append_artifact(self, topic, artifact):
        topic.artifact_query.append(artifact)
        self.save(topic)
        topic_update_signal.send(current_app._get_current_object(), topic=topic)
        artifact_create_signal.send(current_app._get_current_object(), artifact=artifact)
        user_top_10_artifacts_signal.send(current_app._get_current_object(), user_id=artifact.user_id)
        post_create_artifact(artifact)

    def remove_artifact(self, topic, artifact_id):
        artifact = Artifact.query.get_or_404(artifact_id)
        artifact_dict = _artifact_dict_from_cache(artifact_id)
        topic.artifact_query.remove(artifact)
        db.session.delete(artifact)
        db.session.commit()
        topic_update_signal.send(current_app._get_current_object(), topic=topic)
        artifact_delete_signal.send(current_app._get_current_object(), artifact=artifact)
        user_top_10_artifacts_signal.send(current_app._get_current_object(), user_id=artifact.user_id)
        post_remove_artifact(AttrDict(artifact_dict))

    def __repr__(self):
        return "pinwall.artifacts.TopicService"


artifactService = ArtifactService()
cache_registry.register("pinwall.artifacts.ArtifactService.artifact_by_id", artifactService.artifact_by_id)
cache_registry.register("pinwall.artifacts.ArtifactService.artifact_by_userid", artifactService.artifact_by_userid)
cache_registry.register("pinwall.artifacts.ArtifactService.artifact_praised_by_userid",
                        artifactService.artifact_praised_by_userid)

topicService = TopicService()
cache_registry.register("pinwall.artifacts.TopicService.topic_by_id", topicService.topic_by_id)
cache_registry.register("pinwall.artifacts.TopicService.topic_ids_by_userid", topicService.topic_ids_by_userid)
cache_registry.register("pinwall.artifacts.TopicService.first_load_artifact_ids", topicService.first_load_artifact_ids)


def post_create_artifact(artifact):
    user_id = artifact.user_id
    artifact_id = artifact.id
    artifact_add_resources, qiniu_keys = collect_artifact_resource(artifact)
    for _type, _res in artifact_add_resources:
        handler = asset_add_handler(_type)
        if handler:
            handler(_res, user_id, artifact_id)

    qiniu_unregister_key_signal.send(current_app._get_current_object(), qiniu_keys=qiniu_keys)


def post_update_artifact(artifact_dict, update_artifact_dict):
    artifact = AttrDict(artifact_dict)
    update_artifact = AttrDict(update_artifact_dict)
    user_id = artifact.user_id
    artifact_id = artifact.id
    artifact_original_resources, _ = collect_artifact_resource(artifact)
    artifact_update_resources, qiniu_keys = collect_artifact_resource(update_artifact)
    remove_resource = artifact_original_resources - artifact_update_resources
    for _type, _res in remove_resource:
        handler = asset_remove_handler(_type)
        if handler:
            handler(_res, user_id, artifact_id)

    add_resources = artifact_update_resources - artifact_original_resources
    for _type, _res in add_resources:
        handler = asset_add_handler(_type)
        if handler:
            handler(_res, user_id, artifact_id)
    qiniu_unregister_key_signal.send(current_app._get_current_object(), qiniu_keys=qiniu_keys)


def post_remove_artifact(artifact):
    user_id = artifact.user_id
    artifact_id = artifact.id
    artifact_remove_resources, _ = collect_artifact_resource(artifact)
    for _type, _res in artifact_remove_resources:
        handler = asset_remove_handler(_type)
        if handler:
            handler(_res, user_id, artifact_id)


def collect_artifact_resource(artifact, with_qiniu_keys=False):
    qiniu_keys = []
    artifact_resources = set()
    if with_qiniu_keys:
        qiniu_keys.append(artifact.profile_image)
    artifact_resources.add((0, artifact.profile_image))
    for asset in artifact.assets:
        if with_qiniu_keys:
            qiniu_keys.append(asset.profile_image)
        artifact_resources.add((1, asset.profile_image))
        if asset.media_file:
            if with_qiniu_keys:
                qiniu_keys.append(asset.media_file)
            artifact_resources.add((asset.type, asset.media_file))

    return artifact_resources, qiniu_keys


def _artifact_dict_from_cache(artifact_id):
    artifact_dict = artifactService.artifact_by_id(artifact_id)
    artifact_dict["assets"] = map(lambda asset_dict: ArtifactAsset(**asset_dict), artifact_dict.get("assets"))
    return artifact_dict
