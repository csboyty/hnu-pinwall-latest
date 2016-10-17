# coding:utf-8
from datetime import datetime
from ..core import db
from ..caching import CacheableMixin, cached_property
from ..jsoning import JsonSerializer


artifact_term_table = db.Table("artifact_term",
                               db.Column("artifact_id", db.Integer(), db.ForeignKey("artifacts.id", ondelete="cascade"),
                                         primary_key=True),
                               db.Column("term_id", db.Integer(), db.ForeignKey("terms.id", ondelete="cascade"),
                                         primary_key=True))


class Term(db.Model):
    __tablename__ = "terms"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __eq__(self, other):
        return self.name == other or self.name == getattr(other, "name", None)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class ArtifactCacheableMixin(CacheableMixin):
    __cache_properties__ = ["id", "user_id", "name", "description", "profile_image", "visible",
                            "comment_count", "praise_count", "honor_count", "assets", "created_at", "terms", "topic_id"]


class Artifact(ArtifactCacheableMixin, db.Model):
    __tablename__ = "artifacts"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="cascade"))
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text())
    profile_image = db.Column(db.String(256), nullable=False)
    visible = db.Column(db.Boolean(), nullable=False, default=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime(), nullable=True, default=datetime.now)

    user = db.relationship("User", backref=db.backref("artifact_query", lazy="dynamic", passive_deletes=True))
    _terms = db.relationship("Term", secondary=artifact_term_table, passive_deletes=True)
    assets = db.relationship("ArtifactAsset", order_by="asc(ArtifactAsset.pos)", passive_deletes=True,
                             cascade="all, delete-orphan")

    @property
    def terms(self):
        return [term.name for term in self._terms]

    @terms.setter
    def terms(self, value):
        self._terms = []
        terms = Term.query.filter(Term.name.in_(value)).all()
        for term_name in value:
            if term_name not in terms:
                terms.append(Term(name=term_name))
        self._terms.extend(terms)


    @cached_property
    def comment_count(self):
        return self.comment_query.count()

    @cached_property
    def praise_count(self):
        return self.score_query.filter_by(score=0).count()

    @cached_property
    def honor_count(self):
        return self.score_query.filter_by(score=1).count()

    @cached_property
    def topic_id(self):
        return self.topics[0].id if self.topics else None

    def __eq__(self, other):
        if isinstance(other, Artifact):
            return self.id == getattr(other, "id", None)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class ArtifactAssetCacheableMixin(CacheableMixin):
    __cache_properties__ = ["pos", "name", "description", "type", "profile_filename", "profile_image", "media_file",
                            "filename", "view_url"]


class ArtifactAsset(ArtifactAssetCacheableMixin, db.Model):
    __tablename__ = "artifact_assets"

    artifact_id = db.Column(db.Integer(), db.ForeignKey("artifacts.id", ondelete="cascade"), primary_key=True)
    pos = db.Column(db.SmallInteger(), primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text())
    type = db.Column(db.SmallInteger(), nullable=False)
    profile_filename = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(256), nullable=False)
    filename = db.Column(db.String(128), nullable=True)
    media_file = db.Column(db.String(256), nullable=True)
    view_url = db.Column(db.String(256))

    def __eq__(self, other):
        if isinstance(other, ArtifactAsset):
            return self.artifact_id == getattr(other, "artifact_id", None) and self.pos == getattr(other, "pos", None)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s:%s)" % (self.__class__.__name__, self.artifact_id, self.pos)


class ArtifactCommentJsonSerializer(JsonSerializer):
    __json_public__ = ["id", "content", "commented_at"]


class ArtifactComment(ArtifactCommentJsonSerializer, db.Model):
    __tablename__ = "artifact_comments"

    id = db.Column(db.Integer(), primary_key=True)
    artifact_id = db.Column(db.Integer(), db.ForeignKey("artifacts.id", ondelete="cascade"))
    commenter_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="cascade"))
    content = db.Column(db.Text(), nullable=False)
    commented_at = db.Column(db.DateTime(), default=datetime.now)
    visible = db.Column(db.Boolean(), default=True)

    artifact = db.relationship("Artifact", backref=db.backref("comment_query", lazy="dynamic", passive_deletes=True,
                                                              cascade="all, delete-orphan"))
    commenter = db.relationship("User", backref=db.backref("comment_query", lazy="dynamic", passive_deletes=True,
                                                           cascade="all, delete-orphan"))


class ArtifactScore(db.Model):
    __tablename__ = "artifact_scores"

    artifact_id = db.Column(db.Integer(), db.ForeignKey("artifacts.id", ondelete="cascade"), primary_key=True)
    scorer_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="cascade"), primary_key=True)
    score = db.Column(db.SmallInteger())
    scored_at = db.Column(db.DateTime(), default=datetime.now)

    artifact = db.relationship("Artifact", backref=db.backref("score_query", lazy="dynamic", passive_deletes=True,
                                                              cascade="all, delete-orphan"))
    scorer = db.relationship("User", backref=db.backref("score_query", lazy="dynamic", passive_deletes=True,
                                                        cascade="all, delete-orphan"))


topic_artifact_table = db.Table("topic_artifact",
                                db.Column("topic_id", db.Integer(), db.ForeignKey("topics.id", ondelete="cascade"),
                                          primary_key=True),
                                db.Column("artifact_id", db.Integer(),
                                          db.ForeignKey("artifacts.id", ondelete="cascade"),
                                          primary_key=True))

topic_term_table = db.Table("topic_term",
                            db.Column("topic_id", db.Integer(), db.ForeignKey("topics.id", ondelete="cascade"),
                                      primary_key=True),
                            db.Column("term_id", db.Integer(), db.ForeignKey("terms.id", ondelete="cascade"),
                                      primary_key=True))


class TopicCacheableMixin(CacheableMixin):
    __cache_properties__ = ["id", "user_id", "name", "description", "status", "terms", "created_at", "artifact_count"]


class Topic(TopicCacheableMixin, db.Model):
    __tablename__ = "topics"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="cascade"))
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text())
    status = db.Column(db.SmallInteger(), default=0)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.now)

    _terms = db.relationship("Term", secondary=topic_term_table, passive_deletes=True)
    user = db.relationship("User", backref=db.backref("topic_query", lazy="dynamic", passive_deletes=True))
    artifact_query = db.relationship("Artifact", secondary=topic_artifact_table, lazy="dynamic", passive_deletes=True,
                                     backref=db.backref("topics"))

    @property
    def terms(self):
        return [term.name for term in self._terms]

    @terms.setter
    def terms(self, value):
        self._terms = []
        terms = Term.query.filter(Term.name.in_(value)).all()
        for term_name in value:
            if term_name not in terms:
                terms.append(Term(name=term_name))
        self._terms.extend(terms)


    @cached_property
    def artifact_count(self):
        return self.artifact_query.count()

    def first_load_artifact_id(self, limit=10):
        sql = """ select artifacts.id from
                (   select topic_artifact.artifact_id,sum(case artifact_scores.score when 1 then 1 else 0 end) as scores
                    from topics inner join topic_artifact on topics.id=topic_artifact.topic_id
                    inner join artifacts on topic_artifact.artifact_id=artifacts.id
                    left join artifact_scores on artifacts.id=artifact_scores.artifact_id
                    where topics.id=:topic_id group by topic_artifact.artifact_id
                ) t
                inner join artifacts on t.artifact_id=artifacts.id
                order by t.scores desc,artifacts.created_at desc limit :limit;
                """
        cursor = db.session.execute(sql, {"topic_id": self.id, "limit": limit})
        return map(lambda row: row[0], cursor)

    def __eq__(self, other):
        if isinstance(other, Topic):
            return self.id == getattr(other, "id", None)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, self.id)


class BoxViewFile(db.Model):
    __tablename__ = "boxview_files"

    document_id = db.Column(db.String(32), primary_key=True)
    artifact_id = db.Column(db.Integer(), nullable=False)
    media_file = db.Column(db.String(), nullable=False)
    result = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False)
    triggered_at = db.Column(db.DateTime(), nullable=True)


    def __eq__(self, other):
        if isinstance(other, BoxViewFile):
            return self.document_id == getattr(other, "document_id", None)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)











