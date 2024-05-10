# -*- coding: utf-8 -*-
"""
/***************************************************************************
 IrmisJsonLoaderDialog
                                 A QGIS plugin
 This plugin imports IRMIS Json files into QGIS
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-04-04
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Marco Lechner / Bundesamt für Strahlenschutz
        email                : mlechner@bfs.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from datetime import datetime, timedelta
from requests.models import PreparedRequest
import urllib
from urllib.parse import quote

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'irmis_json_loader_dialog_base.ui'))


class IrmisJsonLoaderDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(IrmisJsonLoaderDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.textBrowser_latest.setHtml(self.get_irmis_iec_iaea_url('latest'))
        self.textBrowser_maximum.setHtml(self.get_irmis_iec_iaea_url('maximum'))


    def get_irmis_iec_iaea_url(self, valueTypeParam):
        irmis_iec_iaea_url = "https://iec.iaea.org/IRMIS/Visualisation/api/GetAggregatedMeasurements"
        url_params = {
            'eventId': '255059cb-2c86-43b5-85cf-197694578554',
            'startDate': datetime.strftime(datetime.utcnow() - timedelta(days=90), '%Y-%m-%d %H:%M'),
            'endDate': datetime.strftime(datetime.utcnow(), '%Y-%m-%d %H:%M'),
            'valueType': 'latest',
            'minimumConfidentiality': 2,
            'measurementTypeId': 1,
            'measurementSubTypeId': 1,
            'surveyTypeIds': 5,
            'includeRoutineData': 'true',
            'includeEmergencyData': 'true'
        }
        irmisreq = PreparedRequest()
        url_params['valueType'] = str(valueTypeParam)
        irmisreq.prepare_url(irmis_iec_iaea_url, urllib.parse.urlencode(url_params, quote_via=quote))
        irmishtml = '<a href="' +  irmisreq.url + '"<span style=" text-decoration: underline; color:#0000ff;">' + irmisreq.url + '</span></a>'
        return irmishtml
