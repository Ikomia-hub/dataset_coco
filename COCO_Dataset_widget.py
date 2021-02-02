from ikomia import utils, core, dataprocess
import COCO_Dataset_process as processMod
# PyQt GUI framework
from PyQt5.QtWidgets import *


# --------------------
# - Class which implements widget associated with the process
# - Inherits core.CProtocolTaskWidget from Ikomia API
# --------------------
class COCO_DatasetWidget(core.CProtocolTaskWidget):

    def __init__(self, param, parent):
        core.CProtocolTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = processMod.COCO_DatasetParam()
        else:
            self.parameters = param

        # Create layout : QGridLayout by default
        self.grid_layout = QGridLayout()

        self.browse_json = utils.append_browse_file(self.grid_layout, label="COCO json file",
                                                   path=self.parameters.json_path, filter="*.json")

        self.browse_img_folder = utils.append_browse_file(self.grid_layout, label="Image folder", filter="",
                                                         path=self.parameters.image_folder,
                                                         mode=QFileDialog.Directory)

        # PyQt -> Qt wrapping
        layout_ptr = utils.PyQtToQt(self.grid_layout)

        # Set widget layout
        self.setLayout(layout_ptr)

    def onApply(self):
        # Apply button clicked slot
        # Get parameters from widget
        self.parameters.json_path = self.browse_json.path
        self.parameters.image_folder = self.browse_img_folder.path

        # Send signal to launch the process
        self.emitApply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits dataprocess.CWidgetFactory from Ikomia API
# --------------------
class COCO_DatasetWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "COCO_Dataset"

    def create(self, param):
        # Create widget object
        return COCO_DatasetWidget(param, None)
