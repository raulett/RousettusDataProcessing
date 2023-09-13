from lib.gpxpy import gpxpy

file = r"D:\YandexDisk\Work\QgsPrj\20200628_Эргелях\flights\rawData\20200828\1-6\log\00000002.BIN.gpx"
with open(file, 'r') as gpx_file:
    gpx_data = gpxpy.parse(gpx_file)
