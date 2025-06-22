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

class GroupPopupSectionSessionEntry(RecycleDataViewBehavior, BoxLayout):
    section_session = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.section_session = data['section_session']
        self.ids.section_session_type.text = self.section_session.session_type
        self.ids.section_session_name.text = self.section_session.name
        return super(GroupPopupSectionSessionEntry, self).refresh_view_attrs(rv, index, data)

class GroupPopupSectionEntry(RecycleDataViewBehavior, BoxLayout):
    group_section = ObjectProperty()
    popup = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.group_section = data['group_section']
        self.popup = data['popup']
        self.ids.section_name.text = self.group_section.group_name
        self.ids.section_size.text = str(self.group_section.size)
        return super(GroupPopupSectionEntry, self).refresh_view_attrs(rv, index, data)

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
        self.ids.group_session.values = [
            c['name'] for c in App.get_running_app().classrooms
        ]

        self.ids.group_sessions.data = [
            { 'session': session } \
                for session in App.get_running_app().sessions \
                if session.id in self.group.session_ids
        ]

        self.ids.section_session.values = [
            f'{s.session_type}: {s.name}' \
            for s in App.get_running_app().sessions \
            if s.session_type != 'lecture'
        ]

        self.ids.sections.data = [
            { 'group_section': gs, 'popup': self } \
            for gs in App.get_running_app().groups \
            if int(gs.id) == int(self.group.id) and gs.section != '0'
        ]

        self.ids.section.values = [
            gs.group_name \
            for gs in App.get_running_app().groups \
            if int(gs.id) == int(self.group.id) and gs.section != '0'
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
        self.ids.group_sessions.data.append({ 'session': session })
        self.ids.group_session.values.remove(session_name)

    def add_section(self, section_name, section_size):
        section_id = random.randint(1, 1000)
        compound_id = f'{int(self.group.id)}.{section_id}'

        new_section = Group(
            id=float(compound_id),
            major=0,
            year=0,
            specialization='',
            group_name=f'{self.group.group_name} - {section_name}',
            section=compound_id,
            session_ids=[],
            size=int(section_size),
        )

        self.group.size += int(section_size)
        App.get_running_app().groups.append(new_section)
        self.ids.sections.data.append({ 'group_section': new_section, 'popup': self })
        self.ids.section.values.append(new_section.group_name)

    def add_session_to_section(self, section_name, selection):
        session_type, session_name = selection.split(': ')
        section = list(filter(
            lambda s: s.group_name == section_name,
            App.get_running_app().groups
        ))

        session = list(filter(
            lambda s: s.name == session_name and s.session_type == session_type.lower(),
            App.get_running_app().sessions
        ))

        if len(section) != 1 or len(session) != 1:
            return

        session, section = session[0], section[0]

        section.session_ids.append(session.id)

    def select_section(self, section_name):
        section = list(filter(
            lambda s: s.group_name == section_name,
            App.get_running_app().groups
        ))

        self.ids.section_sessions_label.text = f'{section_name} - Sessions'
        self.ids.section_sessions.data = [
            { 'section_session': s } \
            for s in App.get_running_app().sessions \
            if s.session_type != 'lecture'
        ]

class GroupEntry(RecycleDataViewBehavior, BoxLayout):
    group = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.group = data['group']
        self.ids.group_name.text = self.group.group_name
        return super(GroupEntry, self).refresh_view_attrs(rv, index, data)

    def delete_group(self):
        groups_to_be_removed = [self.group]
        groups_to_be_removed.extend(filter(
            lambda g: int(g.id) == int(self.group.id),
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
                section='0',
                size=0,
                session_ids=[],
            )

        App.get_running_app().groups.append(new_group)
        self.ids.groups.data.append({ 'group': new_group })

    def refresh_groups(self):
        filtered_data = list(filter(
            lambda g: g.section == '0',
            App.get_running_app().groups
        ))

        self.ids.groups.data = [{ 'group': g } for g in filtered_data ]
