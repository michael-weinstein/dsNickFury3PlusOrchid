import os

pj = lambda *paths: os.path.abspath(os.path.join(*paths))

root_dir = os.path.abspath(os.path.dirname(__file__))

network_root = '/home/jake/repos/'

anaconda_root = network_root + r"dsNickFury/dependencies/anaconda2"
python_site_packages = anaconda_root + r"/envs/dsNickFury/pkgs"
python_bin = pj(anaconda_root, "envs/dsNickFury/bin/python")
python3_bin = pj(anaconda_root, "envs/dsNickFury/bin/python")
python3_lib = pj(anaconda_root, "envs/dsNickFury/Library/bin")

python2_bin = pj(anaconda_root, "bin/python")
python2_lib = pj(anaconda_root, "Library/bin")

azimuth_path = network_root + r"dsNickFury/dependencies/azimuth_public"
elevation_path = network_root + r"dsNickFury/dependencies/elevation"
aggregation_model_filename = network_root + r"dsNickFury/dependencies/elevation/elevation/saved_models/aggregation_model.pkl"

azure_url = ''

results_dir = pj(root_dir, "results")
commands_dir = pj(root_dir, "commands")
