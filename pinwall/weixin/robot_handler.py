# coding:utf-8

from werobot.reply import ArticlesReply, Article

from ..core import robot
from ..es import es_client
from ..resultproxy import ArtifactResultProxy
from .. import settings
from . import _logger


@robot.subscribe
def on_subscribe(message):
    return u'欢迎关注图钉墙,请在图钉墙中尽情发挥吧,:-D'


@robot.unsubscribe
def on_unsubscribe(message):
    return u"感觉不再被爱了, T_T"


@robot.text
def on_text(message):
    content = message.content
    try:
        content = content.lower()
        total, artifact_ids = es_client.search_artifact(content)
        if total == 0:
            return "找不到你要的的内容,请换个关键词吧.(×_×)"
        else:
            reply = ArticlesReply(message=message)
            if artifact_ids:
                for artifact_id in artifact_ids:
                    artifact_result = ArtifactResultProxy(artifact_id, show_topic=False, show_user=False).result()
                    artifact = artifact_result.get("artifact")
                    title = artifact.get("name")
                    description = artifact.get("description")
                    profile_image = artifact.get("profile_image")
                    if "." in profile_image:
                        last_dot = profile_image.rindex('.')
                    else:
                        last_dot = len(profile_image)
                    profile_image = profile_image[:last_dot] + "-200x200" + profile_image[last_dot:]
                    url = settings.domain_name + "/projects/" + str(artifact.get("id"))
                    reply.add_article(Article(title=title, description=description, img=profile_image, url=url))

            return reply
    except Exception, e:
        _logger.exception(e)
        return "系统出错了,X﹏X"

@robot.image
@robot.link
@robot.location
@robot.voice
def on_other(message):
    return "⊙﹏⊙‖∣°,系统暂时还不能处理这些类型的消息,请试试发送文本消息吧."


