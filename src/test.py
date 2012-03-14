#!/usr/bin/env python2

import unittest
from eventmanager import EventManager

class TestEventManager(unittest.TestCase):
    def setUp(self):
        self.event_manager = EventManager();
        
    def test_subscribe(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'
        
        self.event_manager.subscribe(event_type,
                                     controller)

        self.assertIsNotNone(self.event_manager.subscriptions[event_type])
        self.assertEqual(self.event_manager.subscriptions[event_type][0],
                         controller)
        self.assertEqual(len(self.event_manager.subscriptions[event_type]), 1)

    def test_subscribe_multiple(self):
        event_type = 'test_event_type'
        controller = 'dummy_controller'
        
        self.event_manager.subscribe(event_type, controller)
        self.event_manager.subscribe(event_type, controller)
        self.assertEqual(len(self.event_manager.subscriptions[event_type]), 1)

if __name__ == '__main__':
    unittest.main()
