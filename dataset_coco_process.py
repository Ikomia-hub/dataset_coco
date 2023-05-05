# Copyright (C) 2021 Ikomia SAS
# Contact: https://www.ikomia.com
#
# This file is part of the IkomiaStudio software.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from ikomia import core, dataprocess
from ikomia.dnn import dataset, datasetio
import copy
import os

# --------------------
# - Class to handle the process parameters
# - Inherits core.CProtocolTaskParam from Ikomia API
# --------------------
class DatasetCocoParam(core.CWorkflowTaskParam):

    def __init__(self):
        core.CWorkflowTaskParam.__init__(self)
        # Place default value initialization here
        self.json_path = ""
        self.image_folder = ""
        self.task = "instance_segmentation"
        self.output_folder = ""

    def set_values(self, param_map):
        # Set parameters values from Ikomia application
        # Parameters values are stored as string and accessible like a python dict
        self.json_path = param_map["json_path"]
        self.image_folder = param_map["image_folder"]
        self.task = param_map["task"]
        self.output_folder = param_map["output_folder"]

    def get_values(self):
        # Send parameters values to Ikomia application
        # Create the specific dict structure (string container)
        param_map = {"json_path": self.json_path,
                     "image_folder": self.image_folder,
                     "task": self.task,
                     "output_folder": self.output_folder}
        return param_map


# --------------------
# - Class which implements the process
# - Inherits core.CProtocolTask or derived from Ikomia API
# --------------------
class DatasetCoco(core.CWorkflowTask):

    def __init__(self, name, param):
        core.CWorkflowTask.__init__(self, name)
        # Add input/output of the process here
        self.add_output(datasetio.IkDatasetIO("coco"))
        self.add_output(dataprocess.CNumericIO())

        # Create parameters class
        if param is None:
            self.set_param_object(DatasetCocoParam())
        else:
            self.set_param_object(copy.deepcopy(param))

    def get_progress_steps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        return 1

    def run(self):
        # Core function of your process
        # Call beginTaskRun for initialization
        self.begin_task_run()

        # Get parameters :
        param = self.get_param_object()

        # Set output folder:
        if param.task == "semantic_segmentation":
            if param.output_folder == "":
                param.output_folder =  os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                         "mask_semantic_seg")
                os.makedirs(param.output_folder, exist_ok=True)
            if param.output_folder != "":
                if not os.path.exists(param.output_folder):
                    os.makedirs(param.output_folder)

        # Get dataset output :
        output = self.get_output(0)
        output.data = dataset.load_coco_dataset(
                                            param.json_path,
                                            param.image_folder,
                                            param.task,
                                            param.output_folder
                                            )
        output.has_bckgnd_class = param.task == "semantic_segmentation"

        # Class labels output
        numeric_out = self.get_output(1)
        numeric_out.clear_data()
        numeric_out.set_output_type(dataprocess.NumericOutputType.TABLE)

        class_ids = []
        for i in range(len(output.data["metadata"]["category_names"])):
            class_ids.append(i)

        numeric_out.add_value_list(
                            class_ids,
                            "Id",
                            list(output.data["metadata"]["category_names"].values())
                            )

        # Step progress bar:
        self.emit_step_progress()

        # Call endTaskRun to finalize process
        self.end_task_run()


# --------------------
# - Factory class to build process object
# - Inherits dataprocess.CProcessFactory from Ikomia API
# --------------------
class DatasetCocoFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "dataset_coco"
        self.info.short_description = "Load COCO 2017 dataset"
        self.info.description = "Load COCO 2017 dataset. " \
                                "This plugin converts a given dataset in COCO 2017 format to Ikomia format. " \
                                "Once loaded, all images can be visualized with their respective annotations. " \
                                "Then, any training algorithms from the Ikomia marketplace can be connected " \
                                "to this converter."
        self.info.authors = "Ikomia team"
        self.info.license = "MIT License"
        self.info.documentation_link = "https://cocodataset.org/"
        self.info.repo = "https://github.com/Ikomia-dev"
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Dataset"
        self.info.icon_path = "icons/coco.jpg"
        self.info.version = "1.2.1"
        self.info.keywords = "coco,dataset,annotation,json,train,dnn"

    def create(self, param=None):
        # Create process object
        return DatasetCoco(self.info.name, param)
