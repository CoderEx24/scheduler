from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ListProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App
from os import path

from core.data_models import Session

Builder.load_file(path.join(path.dirname(__file__), 'kv', 'coursetab.kv'))

class ClassroomEntry(RecycleDataViewBehavior, BoxLayout):
    def refresh_view_attrs(self, rv, index, data):
        self.ids.session_type.text = data['session'].session_type
        self.ids.session_name.text = data['session'].name
        return super(ClassroomEntry, self).refresh_view_attrs(rv, index, data)

class CoursesTab(BoxLayout):
    selected_classroom = ObjectProperty(allownone=True)
    session_type = StringProperty()
    room_type = StringProperty()

    def refresh_classrooms(self):
        for classroom in App.get_running_app().classrooms:
            new_button = Button(
                text=classroom['name'],
                size_hint_y=None,
                height='48dp',
            )

            new_button.bind(on_release=lambda btn, c=classroom: self.ids.classroom.select(c))
            self.ids.classroom.add_widget(new_button)

    def refresh_sessions(self):
        self.ids.sessions.data = [
            { 'session': s } for s in App.get_running_app().sessions
        ]

    def filter_sessions(self, text):
        sessions = App.get_running_app().sessions
        text = text.strip()

        if len(text) == 0:
            self.ids.sessions.data = [
                { 'session': c } for c in sessions
            ]
        else:
            filtered_data = filter(
                lambda d: text in d.name,
                sessions
            )

            self.ids.sessions.data = [
                { 'session': c } for c in filtered_data
            ]


    def add_session(self):
        if not (self.selected_classroom and self.session_type and self.room_type):
            return

        import random
        new_session = Session(
            id=random.randint(1, 10**6),
            code='CODE',
            name=self.selected_classroom['name'],
            session_type=self.session_type,
            required_room_type=self.room_type,
            allowed_instructors=[],
            duration=0,
        )

        App.get_running_app().sessions.append(new_session)
        self.refresh_sessions()

