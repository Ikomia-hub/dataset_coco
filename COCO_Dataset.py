from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits dataprocess.CPluginProcessInterface from Ikomia API
# --------------------
class COCO_Dataset(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        from COCO_Dataset.COCO_Dataset_process import COCO_DatasetProcessFactory
        # Instantiate process object
        return COCO_DatasetProcessFactory()

    def getWidgetFactory(self):
        from COCO_Dataset.COCO_Dataset_widget import COCO_DatasetWidgetFactory
        # Instantiate associated widget object
        return COCO_DatasetWidgetFactory()
