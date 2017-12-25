from .base import MarathonResource, assert_valid_id
from .app import MarathonApp


class MarathonGroup(MarathonResource):

    """Marathon group resource.

    See: https://mesosphere.github.io/marathon/docs/rest-api.html#groups

    :param apps:
    :type apps: list[:class:`marathon.models.app.MarathonApp`] or list[dict]
    :param list[str] dependencies:
    :param groups:
    :type groups: list[:class:`marathon.models.group.MarathonGroup`] or list[dict]
    :param str id:
    :param pods:
    :type pods: list[:class:`marathon.models.pod.MarathonPod`] or list[dict]
    :param str version:
    """

    def __init__(self, apps=None, dependencies=None,
                 groups=None, id=None, pods=None, version=None):
        self.apps = [
            a if isinstance(a, MarathonApp) else MarathonApp().from_json(a)
            for a in (apps or [])
        ]
        self.dependencies = dependencies or []
        self.groups = [
            g if isinstance(g, MarathonGroup) else MarathonGroup().from_json(g)
            for g in (groups or [])
        ]
        self.pods = []
        # ToDo: Create class MarathonPod
        # self.pods = [
        #     p if isinstance(p, MarathonPod) else MarathonPod().from_json(p)
        #     for p in (pods or [])
        # ]
        self.id = assert_valid_id(id)
        self.version = version
