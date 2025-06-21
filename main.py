from kivy.properties import ListProperty
from kivy.app import App
import requests
from ui import *

from core.data_models import *

class MainApp(App):
    classrooms = ListProperty()
    professors = ListProperty()

    def fetch_professors(self):
        try:
            professors = requests \
                .get('http://127.0.0.1:8000/api/schedule/preference/dump') \
                .json()
        except:
            pass
        else:
            self.professors = [
                Instructor(
                    id=p['id'],
                    name=p['name'],
                    type=p['type'],
                    availability_slots=p['availability'],
                )
                for p in professors
            ]


    def fetch_classrooms(self):
        try:
            classrooms = requests \
                            .get('http://127.0.0.1:8000/api/classroom/dump') \
                            .json()
        except:
            pass
        else:
            self.classrooms = [
                Course(
                    id=i,
                    code='',
                    name=c['course']['title'],
                    required_room_type='',
                    allowed_instructors=[],
                    session_type='',
                    duration=0,
                )
                for i, c in enumerate(classrooms)
            ]

if __name__ == '__main__':
    MainApp().run()

