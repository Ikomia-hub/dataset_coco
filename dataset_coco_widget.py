# PyQt GUI framework
from PyQt6.QtWidgets import *

from ikomia import utils, core, dataprocess
from ikomia.utils import pyqtutils, qtconversion

from dataset_coco.dataset_coco_process import DatasetCocoParam



# --------------------
# - Class which implements widget associated with the process
# - Inherits core.CProtocolTaskWidget from Ikomia API
# --------------------
class DatasetCocoWidget(core.CWorkflowTaskWidget):

    def __init__(self, param, parent):
        core.CWorkflowTaskWidget.__init__(self, parent)

        if param is None:
            self.parameters = DatasetCocoParam()
        else:
            self.parameters = param

        # Create layout : QGridLayout by default
        self.grid_layout = QGridLayout()

        self.browse_json = pyqtutils.append_browse_file(self.grid_layout,
                                                        label="COCO json file",
                                                        path=self.parameters.json_file,
                                                        file_filter="*.json")

        self.browse_img_folder = pyqtutils.append_browse_file(self.grid_layout,
                                                              label="Image folder",
                                                              file_filter="",
                                                              path=self.parameters.image_folder,
                                                              mode=QFileDialog.FileMode.Directory)
        self.combo_task = pyqtutils.append_combo(self.grid_layout, "Task")
        self.combo_task.addItems(["detection", "instance_segmentation", "semantic_segmentation", "keypoints"])
        self.combo_task.setCurrentText(self.parameters.task)
        self.browse_output_folder = pyqtutils.append_browse_file(self.grid_layout,
                                                                 label="Output folder (sem. segm.)",
                                                                 file_filter="",
                                                                 path=self.parameters.output_folder,
                                                                 mode=QFileDialog.FileMode.Directory)
        self.combo_task.currentTextChanged.connect(self.on_combo_task_changed)
        self.browse_output_folder.setVisible(self.combo_task.currentText() == "semantic_segmentation")

        # PyQt -> Qt wrapping
        layout_ptr = qtconversion.PyQtToQt(self.grid_layout)

        # Set widget layout
        self.set_layout(layout_ptr)

    def on_combo_task_changed(self, s):
        self.browse_output_folder.setVisible(self.combo_task.currentText() == "semantic_segmentation")

    def on_apply(self):
        # Apply button clicked slot
        # Get parameters from widget
        self.parameters.json_file = self.browse_json.path
        self.parameters.image_folder = self.browse_img_folder.path
        self.parameters.task = self.combo_task.currentText()
        self.parameters.output_folder = self.browse_output_folder.path

        # Send signal to launch the process
        self.emit_apply(self.parameters)


# --------------------
# - Factory class to build process widget object
# - Inherits dataprocess.CWidgetFactory from Ikomia API
# --------------------
class DatasetCocoWidgetFactory(dataprocess.CWidgetFactory):

    def __init__(self):
        dataprocess.CWidgetFactory.__init__(self)
        # Set the name of the process -> it must be the same as the one declared in the process factory class
        self.name = "dataset_coco"

    def create(self, param):
        # Create widget object
        return DatasetCocoWidget(param, None)
