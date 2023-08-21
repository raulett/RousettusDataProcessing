# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RousettusMain
                                 A QGIS plugin
 process geophysical data, collected with SibGis UAV platform

                             -------------------
        begin                : 2021-11-04
        copyright            : (C) 2021 by Vladimir Morozov
        email                : raulett@gmail.com
        git sha              : $Format:%H$

"""
import sys


def classFactory(iface):  # pylint: disable=invalid-name
    """Load RousettusProcessingMain class from file RousettusProcessingMain.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """

    import os
    current_plugin_path = os.path.dirname(os.path.realpath(__file__))
    if current_plugin_path not in sys.path:
        sys.path.append(current_plugin_path)
    os.environ['PYTHONPATH'] = f"{os.getenv('PYTHONPATH')}{os.path.dirname(os.path.realpath(__file__))};"
    print(os.getenv('PYTHONPATH'))

    from .RousettusProcessingMain import RousettusProcessingMain
    return RousettusProcessingMain(iface)
