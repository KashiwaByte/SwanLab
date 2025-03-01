"""
Docs: https://docs.swanlab.cn/zh/guide_cloud/integration/integration-huggingface-transformers.html
"""
from typing import Optional, Any
from typing_extensions import deprecated

import swanlab

class SwanLabCallback(swanlab.integration.transformers.SwanLabCallback):
    @deprecated(
        "`swanlab.integration.huggingface.SwanLabCallback` is deprecated. "
        "Please use `swanlab.integration.transformers.SwanLabCallback` instead.",
        category=FutureWarning,
    )
    def __init__(self,
        project: Optional[str] = None,
        workspace: Optional[str] = None,
        experiment_name: Optional[str] = None,
        description: Optional[str] = None,
        logdir: Optional[str] = None,
        mode: Optional[str] = None,
        **kwargs: Any,):
        """
        To use the `SwanLabCallback`, pass it into the `callback` parameter when initializing the `transformers.Trainer`.
        This allows the Trainer to utilize SwanLab's logging and monitoring functionalities during the training process.
        Parameters same with `swanlab.init`. Finds more informations 
        [here](https://docs.swanlab.cn/api/py-init.html#swanlab-init)

        Parameters
        ----------
        project : str, optional
            The project name of the current experiment, the default is None,
            which means the current project name is the same as the current working directory.
        workspace : str, optional
            Where the current project is located, it can be an organization or a user (currently only supports yourself).
            The default is None, which means the current entity is the same as the current user.
        experiment_name : str, optional
            The experiment name you currently have open. If this parameter is not provided,
            SwanLab will generate one for you by default.
        description : str, optional
            The experiment description you currently have open,
            used for a more detailed introduction or labeling of the current experiment.
            If you do not provide this parameter, you can modify it later in the web interface.
        logdir : str, optional
            The folder will store all the log information generated during the execution of SwanLab.
            If the parameter is None,
            SwanLab will generate a folder named "swanlog" in the same path as the code execution to store the data.
            If you want to visualize the generated log files,
            simply run the command `swanlab watch` in the same path where the code is executed
            (without entering the "swanlog" folder).
            You can also specify your own folder, but you must ensure that the folder exists and preferably does not contain
            anything other than data generated by Swanlab.
            In this case, if you want to view the logs,
            you must use something like `swanlab watch -l ./your_specified_folder` to specify the folder path.
        mode : str, optional
            Allowed values are 'cloud', 'cloud-only', 'local', 'disabled'.
            If the value is 'cloud', the data will be uploaded to the cloud and the local log will be saved.
            If the value is 'cloud-only', the data will only be uploaded to the cloud and the local log will not be saved.
            If the value is 'local', the data will only be saved locally and will not be uploaded to the cloud.
            If the value is 'disabled', the data will not be saved or uploaded, just parsing the data.
        """
        super().__init__(project=project,
                         workspace=workspace,
                         experiment_name=experiment_name,
                         description=description,
                         logdir=logdir,
                         mode=mode,
                         **kwargs)
