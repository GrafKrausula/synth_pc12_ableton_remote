from __future__ import absolute_import, print_function, unicode_literals
from .FaderfoxSurface import FaderfoxSurface

def create_instance(c_instance):
    return FaderfoxSurface(c_instance)
