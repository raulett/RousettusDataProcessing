from typing import List, Tuple

from .VectorLayerSaverGPKG import VectorLayerSaverGPKG

from ...tools import constants

from qgis.core import QgsVectorLayer, QgsCoordinateReferenceSystem, QgsField, QgsFeatureRequest, QgsFeature
from PyQt5.QtCore import QVariant


class GpsLayerSaverGPKG(VectorLayerSaverGPKG):
    def __init__(self, main_window):
        self.uav_id_fieldname = 'UAV_ID'
        self.field_list = ['DATETIME', 'LON', 'LAT', 'ALT', self.uav_id_fieldname, 'IS_SERVICE', 'FILENAME']
        layer = QgsVectorLayer(constants.geometry_types['PointZ'], constants.gps_layer_name, "memory")
        layer.setCrs(QgsCoordinateReferenceSystem("EPSG:4326"))
        VectorLayerSaverGPKG.__init__(self, main_window, constants.gps_group_path,
                                      constants.gps_filepath, constants.gps_filename, layer)
        self._init_gps_layer_fields()

    def _init_gps_layer_fields(self):
        fields_list = [QgsField('DATETIME', QVariant.String),
                       QgsField('LON', QVariant.Double),
                       QgsField('LAT', QVariant.Double),
                       QgsField('ALT', QVariant.Double),
                       QgsField(self.uav_id_fieldname, QVariant.String),
                       QgsField('IS_SERVICE', QVariant.Bool),
                       QgsField('FILENAME', QVariant.String)]
        fields_to_add = []
        layer_fields_names = [field.name() for field in self.layer.fields().toList()]
        for field in fields_list:
            if field.name() not in layer_fields_names:
                fields_to_add.append(field)
        if len(fields_to_add) > 0:
            self.layer.startEditing()
            self.layer.dataProvider().addAttributes(fields_to_add)
            self.layer.updateFields()
            self.layer.commitChanges()

    def get_uav_id_fieldname(self):
        return self.uav_id_fieldname

    def add_features_to_layer(self, features: List[QgsFeature], filename: str, uav_id: str) -> Tuple[int, int]:
        if not self.layer.isValid():
            print("Layer invalid error")
            return 0, 0
        else:
            request = QgsFeatureRequest().setFilterExpression(
                f'"FILENAME" = \'{filename}\' OR "UAV_ID" = \'{uav_id}\'')
            chosen_features_time = [feature.attribute('DATETIME') for feature in self.layer.getFeatures(request)]
            features_to_add = [feature for feature in features
                               if feature.attribute('DATETIME') not in chosen_features_time]
            print("features_to_add: ", len(features_to_add))
            self.layer.startEditing()
            self.layer.dataProvider().addFeatures(features_to_add)
            self.layer.updateExtents()
            self.layer.commitChanges()
            self.layer.triggerRepaint()
            return len(features_to_add),  len(features)-len(features_to_add)
