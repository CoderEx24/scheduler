# timetable.py
import json
import os
from typing import List
from .data_models import Room, Instructor, Session, Group, Class, TimeRange

class TimeTable:
    def __init__(self, *, rooms=None, instructor=None, sessions=None, groups=None):
        self.rooms: List[Room] = rooms or []
        self.instructors: List[Instructor] = instructor or []
        self.sessions: List[Session] = sessions or []
        self.groups: List[Group] = groups or []
        self.classes: List[Class] = []

    def load_rooms_from_file(self, filename):
        with open(filename, 'r') as f:
            rooms_data = json.load(f)

        # Initialize Rooms
        for room in rooms_data:
            self.rooms.append(Room(
                id=room['id'],
                number=room['number'],
                capacity=room['capacity'],
                room_type=room['room_type']
            ))

    def load_instructors_from_file(self, filename):
        with open(instructors_file, 'r') as f:
            instructors_data = json.load(f)

        # Initialize Instructors
        instructor_objs = []
        for instr in instructors_data:
            availability_slots = {}
            for day_str, slots in instr['availability'].items():
                # slots are given as [1,2,3,4,5,6,7,8]
                # convert to zero-based [0..7]
                zero_based = [s-1 for s in slots]
                availability_slots[day_str] = zero_based
            instructor_objs.append(Instructor(
                id=instr['id'],
                name=instr['name'],
                type=instr['type'],
                availability_slots=availability_slots
            ))
        self.instructors = instructor_objs

    def load_sessions_from_file(self, filename):
        with open(sessions_file, 'r') as f:
            sessions_data = json.load(f)

        # Initialize Sessions
        for session in sessions_data:
            # duration given directly in slots, no conversion needed
            self.sessions.append(Session(
                id=session['id'],
                code=session['code'],
                name=session['name'],
                required_room_type=session['required_room_type'],
                allowed_instructors=session['allowed_instructors'],
                session_type=session['session_type'],
                duration=session['duration']  # already in slots
            ))


    def load_groups_from_file(self, filename):
        with open(groups_file, 'r') as f:
            groups_data = json.load(f)

        # Initialize Groups
        for group in groups_data:
            self.groups.append(Group(
                id=group['id'],
                major=group['major'],
                year=group['year'],
                specialization=group['specialization'],
                group_name=group['group_name'],
                section=group['section'],
                size=group['size'],
                session_ids=group['session_ids']
            ))

