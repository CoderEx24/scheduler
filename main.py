from kivy.properties import ListProperty
from kivy.app import App
import requests
from ui import *

from core.data_models import *

class MainApp(App):
    classrooms = ListProperty()
    professors = ListProperty()
    sessions = ListProperty()

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
            self.classrooms = requests \
                .get('http://127.0.0.1:8000/api/classroom/dump') \
                .json()
        except:
            pass
        else:
            self.classrooms = list([
                {**clrm, 'name': f'{clrm['course']['title']} by {clrm['instructor']['first_name']} {clrm['instructor']['last_name']}' }
                for clrm in self.classrooms
            ])

            import random
            self.sessions.extend([
                Session(
                    id=random.randint(1, 10**6),
                    code='CODE',
                    name=clrm['name'],
                    required_room_type='classroom',
                    allowed_instructors=[clrm['instructor']['id']],
                    session_type='lecture',
                    duration=0,
                )
                for clrm in self.classrooms
            ])

    def build(self):
        self.fetch_professors()
        self.fetch_classrooms()

        return super(MainApp, self).build()

if __name__ == '__main__':
    MainApp().run()

