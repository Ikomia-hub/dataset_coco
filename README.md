<div align="center">
  <img src="https://raw.githubusercontent.com/Ikomia-hub/dataset_coco/main/icons/coco.jpg" alt="Algorithm icon">
  <h1 align="center">dataset_coco</h1>
</div>
<br />
<p align="center">
    <a href="https://github.com/Ikomia-hub/dataset_coco">
        <img alt="Stars" src="https://img.shields.io/github/stars/Ikomia-hub/dataset_coco">
    </a>
    <a href="https://app.ikomia.ai/hub/">
        <img alt="Website" src="https://img.shields.io/website/http/app.ikomia.ai/en.svg?down_color=red&down_message=offline&up_message=online">
    </a>
    <a href="https://github.com/Ikomia-hub/dataset_coco/blob/main/LICENSE.md">
        <img alt="GitHub" src="https://img.shields.io/github/license/Ikomia-hub/dataset_coco.svg?color=blue">
    </a>    
    <br>
    <a href="https://discord.com/invite/82Tnw9UGGc">
        <img alt="Discord community" src="https://img.shields.io/badge/Discord-white?style=social&logo=discord">
    </a> 
</p>

Load any dataset in COCO format to Ikomia format. Then, any training algorithms from the Ikomia marketplace can be connected to this converter.

![Coco examples](https://cocodataset.org/images/coco-examples.jpg)

## :rocket: Use with Ikomia API

#### 1. Install Ikomia API

We strongly recommend using a virtual environment. If you're not sure where to start, we offer a tutorial [here](https://www.ikomia.ai/blog/a-step-by-step-guide-to-creating-virtual-environments-in-python).

```sh
pip install ikomia
```

#### 2. Create your workflow


```python
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="dataset_coco", auto_connect=False)

algo.set_parameters({"json_file": "path/to/annotations_file.json",
                     "image_folder": "path/to/image_folder",
                     "task": "detection"})

# Add your training algorithm. Choose it accordingly to the "task" parameter
train = wf.add_task(name="train_yolo_v8", auto_connect=True)

# Start training  
wf.run()
```

## :sunny: Use with Ikomia Studio

Ikomia Studio offers a friendly UI with the same features as the API.

- If you haven't started using Ikomia Studio yet, download and install it from [this page](https://www.ikomia.ai/studio).

- For additional guidance on getting started with Ikomia Studio, check out [this blog post](https://www.ikomia.ai/blog/how-to-get-started-with-ikomia-studio).

## :pencil: Set algorithm parameters

- **json_file** (str): Annotation file (.json) in COCO format. See [this page](https://cocodataset.org/#format-data) for
more information about the COCO format.
- **image_folder** (str): Folder containing images annotated in the annotation file.
- **task** (str) - Default "detection": Task of the dataset. It should be one of : "detection", "instance_segmentation",
"semantic_segmentation" or "keypoints".
- **output_folder** (str) - Default "": Only needed when task=="semantic_segmentation". COCO format does not support 
semantic segmentation so we need to compute semantic segmentation masks from instance segmentation masks, and store the 
computed masks in a folder determined by this parameter.


**Parameters** should be in **strings format**  when added to the dictionary.

```python
from ikomia.dataprocess.workflow import Workflow

# Init your workflow
wf = Workflow()

# Add algorithm
algo = wf.add_task(name="dataset_coco", auto_connect=True)

algo.set_parameters({"json_file": "path/to/annotations_file.json",
                     "image_folder": "path/to/image_folder",
                     "task": "detection",
                     "output_folder": ""})

```

