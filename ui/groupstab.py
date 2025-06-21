from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.app import App
from os import path
import random

from core.data_models import Group

Builder.load_file(path.join(path.dirname(__file__), 'kv', 'groupstab.kv'))

class GroupPopupGroupSessionEntry(RecycleDataViewBehavior, BoxLayout):
    session = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.session = data['session']
        self.ids.session_name.text = self.session.name
        return super(GroupPopupGroupSessionEntry, self).refresh_view_attrs(rv, index, data)

class GroupPopup(Popup):
    group = ObjectProperty()

    def __init__(self, group, **kwargs):
        super(GroupPopup, self).__init__(**kwargs)
        self.group = group
        self.ids.session.values = [
            c['name'] for c in App.get_running_app().classrooms
        ]

        self.ids.sessions.data= [
            { 'session': session } \
                for session in App.get_running_app().sessions \
                if session.id in self.group.session_ids
        ]

    def add_lecture_session(self, session_name):
        session = list(filter(
            lambda d: d.name == session_name and d.session_type == 'lecture',
            App.get_running_app().sessions
        ))

        if len(session) != 1:
            return

        session = session[0]

        self.group.session_ids.append(session.id)
        self.ids.sessions.data.append({ 'session': session })
        self.ids.session.values.remove(session_name)

class GroupEntry(RecycleDataViewBehavior, BoxLayout):
    group = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.group = data['group']
        self.ids.group_name.text = self.group.group_name
        return super(GroupEntry, self).refresh_view_attrs(rv, index, data)

    def delete_group(self):
        groups_to_be_removed = [self.group]
        groups_to_be_removed.extend(filter(
            lambda g: int(g.id) == int(self.group),
            App.get_running_app().groups,
        ))

        for g in groups_to_be_removed:
            App.get_running_app().groups.remove(g)

        self.parent.parent.data.remove({ 'group': self.group })

class GroupsTab(BoxLayout):
    def create_group(self, group_name):
        new_group = Group(
                id=float(random.randint(1, 10**6)),
                major='',
                year=0,
                specialization='',
                group_name=group_name,
                section=0,
                size=0,
                session_ids=[],
            )

        App.get_running_app().groups.append(new_group)
        self.ids.groups.data.append({ 'group': new_group })
