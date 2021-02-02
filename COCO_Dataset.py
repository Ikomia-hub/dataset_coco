from ikomia import dataprocess
import COCO_Dataset_process as processMod
import COCO_Dataset_widget as widgetMod


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits dataprocess.CPluginProcessInterface from Ikomia API
# --------------------
class COCO_Dataset(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        # Instantiate process object
        return processMod.COCO_DatasetProcessFactory()

    def getWidgetFactory(self):
        # Instantiate associated widget object
        return widgetMod.COCO_DatasetWidgetFactory()
