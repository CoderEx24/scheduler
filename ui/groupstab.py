from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.app import App
from os import path

Builder.load_file(path.join(path.dirname(__file__), 'kv', 'groupstab.kv'))

class GroupEntry(RecycleDataViewBehavior, BoxLayout):
    def refreash_view_attrs(self, rv, index, data):
        return super(GroupEntry, self).refresh_view_attrs(rv, index, data)

    def edit_group(self):
        pass

    def delete_group(self):
        pass

class GroupsTab(BoxLayout):
    def create_group(self, group_name, section):
        pass
