import cebra.data.datatypes
import cebra.models.layers as cebra_layers
class Model(nn.Module):
    """Base model for CEBRA experiments.

    The model is a pytorch ``nn.Module``. Features can be computed by
    calling the ``forward()`` or ``__call__`` method. This class should not be
    directly instantiated, and instead used as the base class for CEBRA
    models.

    Args:
        num_input: The number of input dimensions. The tensor passed to
            the ``forward`` method will have shape ``(batch, num_input, in_time)``.
        num_output: The number of output dimensions. The tensor returned
            by the ``forward`` method will have shape ``(batch, num_output, out_time)``.
            the signal due to the network's receptive field. The offset specifies the

    Attributes:
        num_input: The input dimensionality (of the input signal). When calling
            ``forward``, this is the dimensionality expected for the input
            argument. In typical applications of CEBRA, the input dimension
            corresponds to the number of neurons for neural data analysis, number
            of keypoints for kinematik analysis, or can also be the dimension
            of a feature space in case preprocessing happened before feeding the
            data into the model.
        num_output: The output dimensionality (of the embedding space).
            This is the feature dimension of value returned by
            ``forward``. Note that for models using normalization,
            the output dimension should be at least 3D, and 2D without
            normalization to learn meaningful embeddings. The output
            dimensionality is typically smaller than :py:attr:`num_input`,
            but this is not enforced.
    """

        super().__init__()
        if num_input < 1:
            raise ValueError(
                f"Input dimension needs to be at least 1, but got {num_input}.")
        if num_output < 1:
            raise ValueError(
                f"Output dimension needs to be at least 1, but got {num_output}."
            )
        self.num_input: int = num_input
        self.num_output: int = num_output
    def get_offset(self) -> cebra.data.datatypes.Offset:
        """Offset between input and output sequence caused by the receptive field.

        The offset specifies the relation between the length of the input and output
        time sequences. The output sequence is ``len(offset)`` steps shorter than the
        input sequence. For input sequences of shape ``(*, *, len(offset))``, the model
        should return an output sequence that drops the last dimension (which would be 1).

        Returns
            The offset of the network. See :py:class:`cebra.data.datatypes.Offset` for full
            documentation.
        """
        raise NotImplementedError()

    """Mixin for models that support operating on a time-series.
    The input for convolutional models should be ``batch, dim, time``
    and the convolution will be applied across the last dimension.
    """
    pass


    """Mixin for models that re-sample the signal over time."""

    @property
    def resample_factor(self) -> float:
        """The factor by which the signal is downsampled."""
        return NotImplementedError()

    """Networks with an explicitly defined feature encoder."""

    @property
    def feature_encoder(self) -> nn.Module:
        return self.net


class ClassifierModel(Model, HasFeatureEncoder):
    """Base model for classifiers.

    Adds an additional :py:attr:`classifier` layer to the model which is lazily

    Args:
        num_input: The number of input units
        num_output: The number of output units
        offset: The offset introduced by the model's receptive field

    Attributes:
        features_encoder: The feature encoder to map the input tensor (2d or 3d depending
            on the exact model implementation) into a feature space of same dimension
        classifier: Map from the feature space to class scores
    """

        super().__init__(num_input=num_input, num_output=num_output)
        self.classifier: nn.Module = None

    @abc.abstractmethod
    def get_offset(self) -> cebra.data.datatypes.Offset:
        raise NotImplementedError

    def set_output_num(self, label_num: int, override: bool = False):
        """Set the number of output classes.

        Args:
            label_num: The number of labels to be added to the classifier layer.
            override: If `True`, override an existing classifier layer. If you
                passed the parameters of this model to an optimizer, make sure
                to correctly handle the replacement of the classifier there.
        """
        if self.classifier is None or override:
            self.classifier = nn.Linear(self.num_output, label_num)
        else:
            raise RuntimeError("classifier is already initialized.")

    def forward(self, inputs: torch.Tensor) -> torch.Tensor:
        """See :py:class:`ClassifierModel`."""
        features = self.feature_encoder.forward(inputs)
        features = F.relu(features)
        prediction = self.classifier(features)
        return features, prediction


class _OffsetModel(Model, HasFeatureEncoder):

        super().__init__(num_input=num_input, num_output=num_output)

        self.net = nn.Sequential(*layers)
        # TODO(stes) can this layer be removed? it is already added to
        # the self.net

    def forward(self, inp):
        """Compute the embedding given the input signal.

        Args:
            inp: The input tensor of shape `num_samples x self.num_input x time`

        Returns:
            The output tensor of shape `num_samples x self.num_output x (time - receptive field)`.

        Based on the parameters used for initializing, the output embedding
        is normalized to the hypersphere (`normalize = True`).
        """
        return self.net(inp)


class ParameterCountMixin:
    def num_parameters(self) -> int:
    def num_trainable_parameters(self) -> int:
class Offset10Model(_OffsetModel, ConvolutionalModelMixin):
    """CEBRA model with a 10 sample receptive field."""
        if num_units < 1:
            raise ValueError(
            )

    def get_offset(self) -> cebra.data.datatypes.Offset:
        return cebra.data.Offset(5, 5)

    """Symmetric model with 10 sample receptive field, without normalization.

    Suitable for use with InfoNCE metrics for Euclidean space.
    """



class Offset5Model(_OffsetModel, ConvolutionalModelMixin):
    """CEBRA model with a 5 sample receptive field and output normalization."""
    def get_offset(self) -> cebra.data.datatypes.Offset:
class Offset0ModelMSE(_OffsetModel):
    """CEBRA model with a single sample receptive field, without output normalization."""
    def get_offset(self) -> cebra.data.datatypes.Offset:
class Offset0Model(_OffsetModel):
    """CEBRA model with a single sample receptive field, with output normalization."""
        if num_units < 2:
            raise ValueError(
                f"Number of hidden units needs to be at least 2, but got {num_units}."
            )
    def get_offset(self) -> cebra.data.datatypes.Offset:

@register("offset1-model-v2")
class Offset0Modelv2(_OffsetModel):
    """CEBRA model with a single sample receptive field, with output normalization.

    This is a variant of :py:class:`Offset0Model`.
    """

        if num_units < 2:
            raise ValueError(
                f"Number of hidden units needs to be at least 2, but got {num_units}."
            )

    def get_offset(self) -> cebra.data.datatypes.Offset:
        return cebra.data.Offset(0, 1)


@register("offset1-model-v3")
class Offset0Modelv3(_OffsetModel):
    """CEBRA model with a single sample receptive field, with output normalization.

    This is a variant of :py:class:`Offset0Model`.
    """

        if num_units < 2:
            raise ValueError(
                f"Number of hidden units needs to be at least 2, but got {num_units}."
            )

    def get_offset(self) -> cebra.data.datatypes.Offset:
        return cebra.data.Offset(0, 1)


@register("offset1-model-v4")
class Offset0Modelv4(_OffsetModel):
    """CEBRA model with a single sample receptive field, with output normalization.

    This is a variant of :py:class:`Offset0Model`.
    """

        if num_units < 2:
            raise ValueError(
                f"Number of hidden units needs to be at least 2, but got {num_units}."
            )

    def get_offset(self) -> cebra.data.datatypes.Offset:
        return cebra.data.Offset(0, 1)


@register("offset1-model-v5")
class Offset0Modelv5(_OffsetModel):
    """CEBRA model with a single sample receptive field, with output normalization.

    This is a variant of :py:class:`Offset0Model`.
    """

        if num_units < 2:
            raise ValueError(
                f"Number of hidden units needs to be at least 2, but got {num_units}."
            )

    def get_offset(self) -> cebra.data.datatypes.Offset:
        return cebra.data.Offset(0, 1)

@register("resample-model",
          deprecated=True)  # NOTE(stes) deprecated name for compatibility
@register("offset40-model-4x-subsample")
class ResampleModel(_OffsetModel, ConvolutionalModelMixin, ResampleModelMixin):
    """CEBRA model with 40 sample receptive field, output normalization and 4x subsampling."""


    @property
    def resample_factor(self):
        return 4
    def get_offset(self) -> cebra.data.datatypes.Offset:
@register("resample5-model", deprecated=True)
@register("offset20-model-4x-subsample")
class Resample5Model(_OffsetModel, ConvolutionalModelMixin, ResampleModelMixin):
    """CEBRA model with 20 sample receptive field, output normalization and 4x subsampling."""

    ##120Hz

    @property
    def resample_factor(self):
        return 4
    def get_offset(self) -> cebra.data.datatypes.Offset:
@register("resample1-model", deprecated=True)
@register("offset4-model-2x-subsample")
class Resample1Model(_OffsetModel, ResampleModelMixin):
    """CEBRA model with 4 sample receptive field, output normalization and 2x subsampling.

    This model is not convolutional, and needs to be applied to fixed ``(N, d, 4)`` inputs.
    """

    @property
    def resample_factor(self):
        return 2

    def get_offset(self) -> cebra.data.datatypes.Offset:
class SupervisedNN10(ClassifierModel):
    """A supervised model with 10 sample receptive field."""
        super(SupervisedNN10, self).__init__(num_input=num_neurons,
                                             num_output=num_output)
            cebra_layers._Skip(nn.Conv1d(num_units, num_units, 3), nn.GELU()),
            cebra_layers._Skip(nn.Conv1d(num_units, num_units, 3), nn.GELU()),
            cebra_layers._Skip(nn.Conv1d(num_units, num_units, 3), nn.GELU()),
    def get_offset(self) -> cebra.data.datatypes.Offset:
class SupervisedNN1(ClassifierModel):
    """A supervised model with single sample receptive field."""
        super(SupervisedNN1, self).__init__(num_input=num_neurons,
                                            num_output=num_output)
    def get_offset(self) -> cebra.data.datatypes.Offset:
