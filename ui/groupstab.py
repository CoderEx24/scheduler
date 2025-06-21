from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.app import App
from os import path

from core.data_models import Group

Builder.load_file(path.join(path.dirname(__file__), 'kv', 'groupstab.kv'))

class GroupPopupSessionEntry(RecycleDataViewBehavior, BoxLayout):
    session = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.session = data['session']
        self.ids.session_name.text = self.session.name
        return super(GroupPopupSessionEntry, self).refresh_view_attrs(rv, index, data)

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

    def add_session(self, session, session_type):
        session = list(filter(
            lambda d: d.name == session and d.session_type == session_type.lower(),
            App.get_running_app().sessions
        ))

        if len(session) != 1:
            return

        session = session[0]

        print(session)
        self.group.session_ids.append(session.id)
        self.ids.sessions.data.append({ 'session': session })

    def save(self):
        return True

class GroupEntry(RecycleDataViewBehavior, BoxLayout):
    group = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.group = data['group']
        self.ids.group_name.text = self.group.group_name
        return super(GroupEntry, self).refresh_view_attrs(rv, index, data)

    def delete_group(self):
        App.get_running_app().groups.remove(self.group)
        self.parent.parent.data.remove({ 'group': self.group })

class GroupsTab(BoxLayout):
    def create_group(self, group_name, section, size):
        new_group = Group(
                id=0.0,
                major='',
                year=0,
                specialization='',
                group_name=group_name,
                section=section,
                size=size,
                session_ids=[],
            )

        App.get_running_app().groups.append(new_group)
        self.ids.groups.data.append({ 'group': new_group })
