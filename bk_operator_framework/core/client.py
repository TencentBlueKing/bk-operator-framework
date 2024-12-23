from kubernetes import config

config.load_kube_config(config_file="config_file", context="context")
config.load_incluster_config()
