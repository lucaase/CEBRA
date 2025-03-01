#
# CEBRA: Consistent EmBeddings of high-dimensional Recordings using Auxiliary variables
# © Mackenzie W. Mathis & Steffen Schneider (v0.4.0+)
# Source code:
# https://github.com/AdaptiveMotorControlLab/CEBRA
#
# Please see LICENSE.md for the full license document:
# https://github.com/AdaptiveMotorControlLab/CEBRA/blob/main/LICENSE.md
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import warnings

import numpy.typing as npt
import sklearn.utils.validation as sklearn_utils_validation
import torch

import cebra.helper


try:
    import torch_xla.core.xla_model as xm
    _HAS_TORCH_XLA = True
except ImportError:
    _HAS_TORCH_XLA = False

def update_old_param(old: dict, new: dict, kwargs: dict, default) -> tuple:
    """Handle deprecated arguments of a function until they are replaced.

    Note:
        If both the deprecated and new arguments are present, then an error is raised,
        else if only the deprecated argument is present, a warning is raised and the
        old argument is used in place of the new one.

    Args:
        old: A dictionary containing the deprecated arguments.
        new: A dictionary containing the new arguments.
        kwargs: A dictionary containing all the arguments.

    Returns:
        The updated ``kwargs`` set of arguments.

    """
    if kwargs[old] is None and kwargs[new] is None:  # none are present
        kwargs[new] = default
    elif kwargs[old] is not None and kwargs[new] is not None:  # both are present
        raise ValueError(
            f"{old} and {new} cannot be assigned simultaneously. Assign only {new}"
        )
    elif kwargs[old] is not None:  # old version is present but not the new one
        warnings.warn(f"{old} is deprecated. Use {new} instead")
        kwargs[new] = kwargs[old]

    return kwargs


def check_input_array(X: npt.NDArray, *, min_samples: int) -> npt.NDArray:
    """Check validity of the input data, using scikit-learn native function.

    Note:
        * Assert that the array is non-empty, 2D and containing only finite values.
        * Assert that the array has at least {min_samples} samples and 1 feature dimension.
        * Assert that the array is not sparse.
        * Check for the dtype of X and convert values to float if needed.

    Args:
        X: Input data array to check.
        min_samples: Minimum of samples in the dataset.

    Returns:
        The converted and validated array.
    """
    return sklearn_utils_validation.check_array(
        X,
        accept_sparse=False,
        accept_large_sparse=False,
        dtype=("float16", "float32", "float64"),
        order=None,
        copy=False,
        force_all_finite=True,
        ensure_2d=True,
        allow_nd=False,
        ensure_min_samples=min_samples,
        ensure_min_features=1,
    )


def check_label_array(y: npt.NDArray, *, min_samples: int):
    """Check validity of the labels, using scikit-learn native function.

    Note:
        * Assert that the array is non-empty and containing only finite values.
        * Assert that the array has at least {min_samples} samples.
        * Assert that the array is not sparse.
        * Check for the dtype of y and convert values to numeric if needed.

    Args:
        y: Labels array to check.
        min_samples: Minimum of samples in the label array.

    Returns:
        The converted and validated labels.
    """
    return sklearn_utils_validation.check_array(
        y,
        accept_sparse=False,
        accept_large_sparse=False,
        dtype="numeric",
        order=None,
        copy=False,
        force_all_finite=True,
        ensure_2d=False,
        allow_nd=False,
        ensure_min_samples=min_samples,
    )


def check_device(device: str) -> str:
    if isinstance(device, torch.device):
        device = device.type
    
    if device == "cuda_if_available":
        if torch.cuda.is_available():
            return "cuda"
        elif _HAS_TORCH_XLA:  # Check for XLA availability globally defined
            return "xla:0"  # Assuming the first XLA device if available
        else:
            return "cpu"
    elif device.startswith("cuda:") and len(device) > 5:
        # No changes needed here, assuming previous logic is correct
        pass
    elif device.startswith("xla:"):  # Explicitly checking for "xla:" devices
        if _HAS_TORCH_XLA:
            return device  # Directly return the device if "xla:" is specified
        else:
            raise ValueError("XLA device specified but torch_xla is not available.")
    elif device == "xla" and _HAS_TORCH_XLA:  # Check for generic "xla" device
        return "xla:0"  # Defaulting to the first XLA device
    elif device in ["cuda", "cpu", "mps"]:
        # Your existing conditions for handling "cuda", "cpu", and "mps"
        pass
    else:
        raise ValueError(f"Device needs to be cuda, cpu, xla, or mps, but got {device}.")


def check_fitted(model: "cebra.models.Model") -> bool:
    """Check if an estimator is fitted.

    Args:
        model: The model to assess.

    Returns:
        True if fitted.
    """
    return hasattr(model, "n_features_")
