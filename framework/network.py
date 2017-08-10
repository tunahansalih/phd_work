import tensorflow as tf
from auxillary.dag_utilities import Dag
from auxillary.constants import ChannelTypes, GlobalInputNames, InitType, ActivationType, PoolingType, TreeType, \
    ProblemType, ShrinkageRegularizers
from framework.network_channel import NetworkChannel


class Network:
    def __init__(self, run_id, dataset, parameter_file, problem_type,
                 train_program,
                 loss_layer_init=InitType.xavier,
                 loss_activation=ActivationType.tanh,
                 activation_init=InitType.xavier,
                 shrinkage_regularizer=ShrinkageRegularizers.l2):
        self.nodes = {}
        self.leafNodes = []
        self.runId = run_id
        self.dataset = dataset
        self.parameterFile = parameter_file
        self.dag = Dag()
        self.topologicalSortedNodes = []
        self.problemType = problem_type
        self.lossLayerInit = loss_layer_init
        self.lossLayerActivation = loss_activation
        self.shrinkageRegularizer = shrinkage_regularizer
        self.indicatorText = None
        self.activationInit = activation_init
        self.accumulationNode = None
        self.trainProgram = train_program
        self.optimizer = None
        # Tensors to be used in training
        self.allLearnableParameterTensorsList = None
        self.objectiveLossTensors = None
        self.regularizationTensors = None
        self.nonDifferentiableLossTensors = None
        self.allLossTensorsDict = None
        self.totalObjectiveLossTensor = None
        self.totalRegularizationLossTensor = None
        self.objectiveGradientTensors = None
        self.regularizationGradientTensors = None
        self.trainingTensorsDict = {}
        self.trainingResults = None
        # Tensors to be used in evaluation
        self.evaluationTensorsList = []
        self.evaluationResults = None
        # Global input tensors and their drivers (Gaussian Parameter, Decaying Parameter, Fixed Parameter objects etc.)
        self.globalInputs = {}
        self.globalInputDrivers = {}

    # Methods to be overridden
    def build_network(self):
        pass

    def add_nodewise_input(self, producer_node, producer_channel, producer_channel_index, dest_node):
        pass

    def create_global_inputs(self):
        pass

    def create_global_input_drivers(self):
        pass

    def train(self):
        pass

    def get_outputs_for_single_loss(self, loss_object):
        pass

    def get_total_loss_output(self, loss_type):
        pass

    def get_gradient_for_parameter(self, parameter_object, loss_type):
        pass

    # Methods to be overridden

    def get_accumulation_node(self):
        if self.accumulationNode is None:
            candidates = []
            for node in self.nodes.values():
                if node.isAccumulation:
                    candidates.append(node)
            if len(candidates) != 1:
                raise Exception("There must be exactly one accumulation node in the network.")
            self.accumulationNode = candidates[0]
        return self.accumulationNode

    # All networkwise inputs are constant, and they will be placed into the accumulation node.
    def add_networkwise_input(self, name, tensor_type):
        if name in self.globalInputs:
            raise Exception("Input {0} already exists".format(name))
        self.globalInputs[name] = tf.placeholder(dtype=tensor_type, name=name)
        return self.globalInputs[name]

    def get_networkwise_input(self, name):
        return self.globalInputs[name]

    def get_networkwise_input_value(self, name):
        return self.globalInputDrivers[name].value

    def set_optimizer(self, optimizer):
        self.optimizer = optimizer
