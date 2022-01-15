import t5
import os
import json
import seqio
import warnings
import argparse
import t5.models
import logging as py_logging
from src.createtask import init
import tensorflow.compat.v1 as tf
from contextlib import contextmanager
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Set up logging
tf.get_logger().propagate = False
py_logging.root.setLevel('INFO')
@contextmanager
def tf_verbosity_level(level):
    og_level = tf.logging.get_verbosity()
    tf.logging.set_verbosity(level)
    yield
    tf.logging.set_verbosity(og_level)

parser = argparse.ArgumentParser(description='Finetune T5')
parser.add_argument('-bucket', type=str, default="../datasets",
                    help='Name of google storage bucket or local dataset root directory')
parser.add_argument('-datasets', nargs='+', type=str, required=True,
                    help='Names of dataset(s) as defined in datasets.json')
parser.add_argument('-gpus', nargs='+', type=str, default=None,
                    help='Available GPUs. Input format: "-gpus gpu:0 gpu:1 "...')
parser.add_argument('-tpu_address', type=str, default=None,
                    help='TPU ip address. None if using GPU')
parser.add_argument('-tpu_topology', type=str, default=None, choices=["v2-8","v3-8", None],
                    help='TPU type. None if using GPU')
parser.add_argument('-in_len', type=int, default=2048,
                    help='Maximum length of input. Inputs will be padded to this length.')
parser.add_argument('-out_len', type=int, default=512,
                    help='Maximum length of output. Outputs will be padded to this length.')
parser.add_argument('-steps', type=int, default=50000,
                    help='Number of steps to train for')
parser.add_argument('-model_size', type=str, default="small", choices=["small", "t5.1.1.small", "base", "large", "3B", "11B"],
                    help='Model size. Small is generally reccomended.')
parser.add_argument('-save_after', type=int, default=2500,
                    help='How many steps before saving a checkpoint')

# There are already defaults for these values per model size. These are simply overrides.
parser.add_argument('-batch_size', type=int, default=None,
                    help='Batches per step')
parser.add_argument('-max_checkpoints', type=int, default=None,
                    help='The maximum number of checkpoints to save at once')
parser.add_argument('-storemode', type=str, default="gs", choices=["gs", "local"],
                    help='Whee is the dataset and checkpoint saved? Local or google cloud storage.')
parser.add_argument('-model_paralellism', type=int, default=None,
                    help='Contrary to data paralellism, model paralellism splits a model up into each accelerator, helping memory usage but reducing overall model efficiency.')
args = parser.parse_args()

if args.gpus: assert not args.tpu_address and not args.tpu_topology, "Cannot set TPU variables if using GPU"
if args.tpu_address and args.tpu_topology: assert not args.gpus, "Cannot set GPU variables if using TPU"

# Register dataset as a mixture
datasets=json.load(os.open("datasets.json"))
for dataset in args.datasets:
    if dataset in datasets:
        info=datasets[dataset]
        init(info["bucket_path"],info["train_path"], info["validation_path"], 
            dataset, info["compression_type"], info["store_mode"])
    else:
        warnings.warn(f"Dataset {} was not in datasets.json, and will not be included.")
        args.datasets.remove(dataset)

seqio.MixtureRegistry.add(
    "all_mix",
    args.datasets,
    default_rate=1.0
)

if args.tpu_address != None:
    args.tpu_address = f"grpc://{args.tpu_address}:8470"
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver(tpu=args.tpu_address)
    tf.enable_eager_execution()
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    print("All devices: ", tf.config.list_logical_devices('TPU'))
    tf.disable_v2_behavior()

MODEL_SIZE = args.model_size
if args.storemode=="gs": 
    MODELS_DIR = os.path.join("gs://"+args.dir, "models")
    # Public GCS path for T5 pre-trained model checkpoints
    BASE_PRETRAINED_DIR = "gs://t5-data/pretrained_models"
else: 
    MODELS_DIR = os.path.join(args.dir, "models")
    # Public GCS path for T5 pre-trained model checkpoints
    BASE_PRETRAINED_DIR = "pretrained_models"
PRETRAINED_DIR = os.path.join(BASE_PRETRAINED_DIR, MODEL_SIZE)
MODEL_DIR = os.path.join(MODELS_DIR, MODEL_SIZE)

# Set parallelism and batch size to fit on v2-8 TPU (if possible).
# Limit number of checkpoints to fit within 5GB (if possible).
try:
    model_parallelism, train_batch_size, keep_checkpoint_max = {
        "small": (1, 512, 4),
        "t5.1.1.small": (1, 512, 4),
        "base": (2, 256, 2),
        "large": (4, 128, 2),
        "3B": (8, 16, 1),
        "11B": (8, 4, 1)}[MODEL_SIZE]
except:
    model_parallelism, train_batch_size, keep_checkpoint_max=None,None,None
    assert args.model_paralellism and args.batch_size and args.max_checkpoints, "Model not found in supported list. Cannot determine model paralellism, batch size, and number of checkpoints to keep automatically."
if args.model_paralellism: model_paralellism=args.model_paralellism
if args.batch_size: train_batch_size=args.batch_size
if args.max_checkpoints: keep_checkpoint_max=args.max_checkpoints

tf.io.gfile.makedirs(MODEL_DIR)
# The models from our paper are based on the Mesh Tensorflow Transformer.
if args.tpu_address:
    model = t5.models.MtfModel(
        model_dir=MODEL_DIR,
        tpu=args.tpu_address,
        tpu_topology=args.tpu_topology,
        model_parallelism=model_parallelism,
        batch_size=train_batch_size,
        sequence_length={"inputs": args.in_len, "targets": args.out_len},
        learning_rate_schedule=0.001,
        save_checkpoints_steps=args.save_after,
        keep_checkpoint_max=keep_checkpoint_max,
        iterations_per_loop=500,
    )
elif args.gpus:
    model = t5.models.MtfModel(
        model_dir=MODEL_DIR,
        tpu=None,
        mesh_devices=args.gpus,
        mesh_shape=f'model:1,batch:{len(args.gpus)}',
        model_parallelism=model_parallelism,
        batch_size=train_batch_size,
        sequence_length={"inputs": args.in_len, "targets": args.out_len},
        learning_rate_schedule=0.001,
        save_checkpoints_steps=args.save_after,
        keep_checkpoint_max=keep_checkpoint_max,
        iterations_per_loop=500,
    )
else: raise NotImplementedError("Running with no accelerators is not a supported case.")
        
model.finetune(
    mixture_or_task_name="all_mix",
    pretrained_model_dir=PRETRAINED_DIR,
    finetune_steps=args.steps
)