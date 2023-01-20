#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2023 Lorenzo Carbonell <a.k.a. atareao>

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import sqlite3

class Database:
    def __init__(self, app, db):
        self.app = app
        self.db = db
        self.logger = self.app.logger

    def execute(self, sqlquery, data=None):
        lastrowid = None
        conn = None
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            self.logger.info(sqlquery)
            if data:
                lastrowid = cursor.execute(sqlquery, data).lastrowid
            else:
                lastrowid = cursor.execute(sqlquery).lastrowid
            conn.commit()
        except Exception as exception:
            self.logger.error(exception)
            lastrowid = None
        finally:
            if conn:
                conn.close()
        return lastrowid

    def select(self, sqlquery):
        conn = None
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            self.logger.info(sqlquery)
            cursor.execute(sqlquery)
            return cursor.fetchall()
        except Exception as exception:
            self.logger.error(exception)
        finally:
            if conn:
                conn.close()
        return []
