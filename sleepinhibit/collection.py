#!/usr/bin/python3
# coding=utf-8
#
# Copyright © 2016 Scott Severance
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

class Collection(object):
    '''A class to hold arbitrary settings as properties.

    To initialize, pass in any desired settings as keyword arguments (you may
    use only keyword arguments). To use, simply access the keywords as properties.

    WARNING: If you add a property directly, without using the add_property
    method, it is your responsibility to ensure that there are no naming clashes
    with the class's methods.

    Example:
        foo = Collection(bar=1, baz='a')
        foo.bar                      # 1
        foo.baz                      # 'a'
        foo.other = 6                # add a new item
        foo.add_property('other', 6) # alternate way to add a new item
    '''
    def __init__(self, **kwargs):
        object.__setattr__(self, '_contained_items', set())
        for k, v in kwargs.items():
            self.add_property(k, v)
        #self.__dict__.update(kwargs)

    def __setattr__(self, name, value):
        if name in self._contained_items:
            object.__setattr__(self, name, value)
        else:
            self.add_property(name, value)

    def add_property(self, key, value):
        '''Adds a property with error-checking.

        Equivalant to self.key = value'''
        if key in (dir(self) or self._contained_items):
            raise ValueError('The key "{}" is already in use.'.format(key))
        object.__setattr__(self, key, value)
        self._contained_items.add(key)

    def rm(self, *args):
        '''Deletes the listed properties'''
        for i in args:
            if i in self._contained_items:
                del self.__dict__[i]
                self._contained_items.remove(i)
            else:
                raise AttributeError(
                    'The attribute "{}" doesn\'t exist or can\'t be removed.'.format(i)
                )

    def __repr__(self):
        return '{cls}({args})'.format(
            cls=type(self).__name__,
            args=', '.join(sorted(
                ['{}={}'.format(k, repr(v)) for k, v in self.__dict__.items() if not k.startswith('_')]
            ))
        )
