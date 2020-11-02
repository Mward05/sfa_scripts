import logging

import random
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds


log = logging.getLogger(__name__)


def maya_main_window():
    """"Return the maya main window widget"""
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartScatterUI(QtWidgets.QDialog):
    """Smart Scatter UI Class"""

    def __init__(self):
        super(SmartScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter UI")
        self.setMinimumWidth(500)
        self.setMaximumHeight(300)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.create_ui()
        self.create_connections()



    def create_ui(self):
        self.title_lbl = QtWidgets.QLabel("Scatter Tool")
        self.title_lbl.setStyleSheet("font: bold 20px")
        self.title_lbl_two = QtWidgets.QLabel("Select Geometry to be "
                                              "Scattered, then shift "
                                              "select Vertex")
        self.title_lbl_two.setStyleSheet("font: italic 18px")
        layout = self._create_scatter_btn_ui()
        self.main_lay = QtWidgets.QVBoxLayout()
        self.main_lay.addWidget(self.title_lbl)
        self.main_lay.addWidget(self.title_lbl_two)
        self.main_lay.addStretch()
        self.main_lay.addLayout(layout)
        self.setLayout(self.main_lay)
        

    def _create_scatter_btn_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        return layout


    def create_connections(self):
        """Connect Signals and Slots"""
        self.scatter_btn.clicked.connect(self.scatter_objects)


    @QtCore.Slot()
    def scatter_objects(self):
        """ Takes current selection and adds it to second selection verts """
        rand_trans = [0, 1, 2, 3]
        rand_rot = [0, 1, 2, 3]
        rand_scale = [0, 1, 2, 3]
        selection = cmds.ls(orderedSelection=True, flatten=True)
        vertex_names = cmds.filterExpand(selection, selectionMask=31,
                                         expand=True)

        """ Create a group """
        scatter_grp = cmds.group(em=True, n='scatter_grp')

        object_to_instance = selection[0]
        if cmds.objectType(object_to_instance) == 'transform':
            for ver in vertex_names:
                new_instance = cmds.instance(object_to_instance)
                position = cmds.pointPosition(ver, world=True)

                """ Apply the random offset to the position. """
                new_position = [
                    x + random.uniform(rand_trans[0], rand_trans[1]) for x
                    in position]
                new_rotation = [random.uniform(rand_rot[0], rand_rot[1])
                                for _ in range(3)]
                new_scale = [random.uniform(rand_scale[0], rand_scale[1])
                             for _ in range(3)]

                """ Set the position """
                cmds.move(new_position[0],
                          new_position[1],
                          new_position[2],
                          new_instance,
                          absolute=True,
                          worldSpace=True)

                """ Set the rotation """
                cmds.rotate(new_rotation[0],
                            new_rotation[1],
                            new_rotation[2],
                            new_instance,
                            relative=True,
                            objectSpace=True)

                """ Set the scale """
                cmds.scale(new_scale[0],
                           new_scale[1],
                           new_scale[2],
                           new_instance,
                           relative=True)

                """ Parent into the group """
                cmds.parent(new_instance, scatter_grp)

        else:
            print("Make sure to select object you want scattered. "
                  "Then shift select verts on the object you want scattered on")












