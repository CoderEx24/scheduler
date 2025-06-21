from kivy.properties import ListProperty
from kivy.app import App
import requests
from ui import *

from core.data_models import *

class MainApp(App):
    classrooms = ListProperty()

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

