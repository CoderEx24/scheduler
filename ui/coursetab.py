from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App
from os import path
from weakref import proxy

Builder.load_file(path.join(path.dirname(__file__), 'kv', 'coursetab.kv'))

class ClassroomEntry(RecycleDataViewBehavior, BoxLayout):
    def refresh_view_attrs(self, rv, index, data):
        self.ids.classroom_name.text = data['classroom'].name
        return super(ClassroomEntry, self).refresh_view_attrs(rv, index, data)

class CoursesTab(BoxLayout):
    selected_classroom = ObjectProperty(allownone=True)
    session_type = StringProperty()
    room_type = StringProperty()

    def on_parent(self, *args):
        if len(self.ids.classrooms.data) > 0:
            return

        for i, classroom in enumerate(App.get_running_app().classrooms):
            new_button = Button(
                text=classroom.name,
                size_hint_y=None,
                height='48dp',
            )

            new_button.bind(on_release=lambda btn, c=classroom: self.ids.classroom.select(c))
            self.ids.classroom.add_widget(new_button)

    def filter_classrooms(self, text):
        classrooms = App.get_running_app().classrooms
        text = text.strip()

        if len(text) == 0:
            self.ids.classrooms.data = [
                { 'classroom': c } for c in classrooms
            ]
        else:
            filtered_data = filter(
                lambda d: text in d.name,
                classrooms
            )

            self.ids.classrooms.data = [
                { 'classroom': c } for c in filtered_data
            ]


    def add_classroom(self):
        if not (self.selected_classroom and self.session_type and self.room_type):
            return

        self.selected_classroom.session_type = self.session_type
        self.selected_classroom.room_type = self.room_type
        self.ids.classrooms.data.append(
            { 'classroom': self.selected_classroom }
        )

        self.ids.classroom.select(None)
        self.ids.session_type.select('')
        self.ids.room_type.select('')

