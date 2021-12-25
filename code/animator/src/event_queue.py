# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 18:26:37 2021

@author: richa
"""
import argparse
import functools
from collections import defaultdict

# pylint: disable=too-few-public-methods
class Event:
    """Event class"""

    def __init__(self, name, args, kwargs):
        self.name = name
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}


class EventQueue:
    """Event queue class that contains events. Events can be subscribed to call a callback"""

    def __init__(self):
        self.events = []
        self.subscribers = defaultdict(list)

    def subscribe(self, event_name: str, function: callable):
        """Subscribes the passed function to the event. Whenever the named event
        occurs, the passed function will be executed.
        """
        self.subscribers[event_name].append(function)

    def pump(self, event_name: str, args=None, kwargs=None):
        """Adds an event to the end of the events list"""
        event = Event(event_name, args, kwargs)
        self.events.append(event)

    def update(self):
        """Calls all subscriber functions for all pumped events, then removes all pumped events."""
        for event in self.events:
            for function in self.subscribers[event.name]:
                function(*event.args, **event.kwargs)
        self.events = []


class ParseEvent(argparse.Action):
    """Parse Event class, to be used as an action for the argparse.ArgumentParser"""

    def __init__(self, event_queue, event_name, *args, **kwargs):
        self.event_queue = event_queue
        self.event_name = event_name
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        self.event_queue.pump(self.event_name, args=[values])


def get_action(event_queue, event_name):
    """Utility function that returns a pre-filled function (not-called yet)
    that returns a ParseEvent.
    """
    return functools.partial(ParseEvent, event_queue, event_name)
