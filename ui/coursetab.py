from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from os import path

Builder.load_file(path.join(path.dirname(__file__), 'kv', 'coursetab.kv'))

class ClassroomEntry(RecycleDataViewBehavior, BoxLayout):
    data = StringProperty()

class CoursesTab(BoxLayout):
    selected_classroom = StringProperty()
    session_type = StringProperty()
    room_type = StringProperty()
    classrooms = ListProperty()

    def on_parent(self, *args):
        if len(self.classrooms) > 0:
            return

        self.classrooms = [
            f'Classroom {i}' for i in range(10)
        ]

        self.ids.classrooms.data = [
            { 'data': c } for c in self.classrooms
        ]

        for classroom in self.classrooms:
            new_button = Button(
                text=classroom,
                size_hint_y=None,
                height='48dp',
            )

            from copy import deepcopy
            new_button.bind(on_release=lambda btn: self.ids.classroom.select(btn.text))
            self.ids.classroom.add_widget(new_button)

    def filter_classrooms(self, text):
        text = text.strip()
        if len(text) == 0:
            self.ids.classrooms.data = [
                { 'data': c } for c in self.classrooms
            ]
        else:
            filtered_data = filter(
                lambda d: text in d,
                self.classrooms
            )

            self.ids.classrooms.data = [
                { 'data': c } for c in filtered_data
            ]

