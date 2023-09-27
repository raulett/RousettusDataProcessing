from datetime import datetime

# datetime format project constants
datetime_format = '%Y-%m-%dT%H:%M:%S,%f'
default_datetime = datetime(1900, 1, 1).strftime(datetime_format)

# general data
geometry_types = {'Point': 'Point', 'PointZ': 'PointZ', 'LineString': 'LineString', 'Polygon': 'Polygon'}

# general data group path
data_group_path = ['data']

# GPS layer groups and filepath constants.
gps_group_path = data_group_path[:] + ['gps']
gps_layer_name = 'gps_data'
gps_filepath = ['data']
gps_filename = 'gps_data'
