#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#   Debian Changes Bot
#   Copyright (C) 2008 Chris Lamb <chris@chris-lamb.co.uk>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from DebianDevelChangesBot.mailparsers import BugClosedParser as p

class TestMailParserBugClosed(unittest.TestCase):
    def setUp(self):
        self.headers = {
            'List-Id': '<debian-bugs-closed.lists.debian.org>',
            'Subject': 'Bug#123456: marked as done (binary-package: description here)',
            'X-Debian-PR-Source': 'source-package',
            'X-Debian-PR-Package': 'binary-package',
        }

        self.body = []

    def testSimple(self):
        self.headers.update({
            'From': 'From <from@email.com>',
            'To': 'somewhere@email.com',
        })

        msg = p.parse(self.headers, self.body)
        self.assert_(msg)
        self.assertEqual(msg.bug_number, 123456)
        self.assertEqual(msg.package, 'binary-package')
        self.assertEqual(msg.by, u'somewhere@email.com')
        self.assertEqual(msg.title, 'description here')

    def testTwoEntriesInTo(self):
        self.headers.update({
            'From': 'From <from@email.com>',
            'To': 'To <to@email.com>, 123456-done@bugs.debian.org',
        })

        msg = p.parse(self.headers, self.body)
        self.assert_(msg)
        self.assertEqual(msg.bug_number, 123456)
        self.assertEqual(msg.package, 'binary-package')
        self.assertEqual(msg.by, u'From <from@email.com>')
        self.assertEqual(msg.title, 'description here')

    def testDone(self):
        self.headers.update({
            'From': u'From <from@email.com>',
            'To': u'123456-done@bugs.debian.org',
        })
        msg = p.parse(self.headers, self.body)
        self.assert_(msg)
        self.assertEqual(msg.by, u'From <from@email.com>')

if __name__ == "__main__":
    unittest.main()
