.PHONY: install tpu

install:
	sudo apt update
	sudo apt upgrade -y
	sudo apt autoremove -y
	sudo apt install -y python3-pip unzip python-is-python3
	sudo -H pip3 install --upgrade pip
	sudo -H pip3 install -r data/requirements.txt
	sudo -H pip3 install -r train/requirements.txt

tpu: install
	sudo -H pip3 install --upgrade --force-reinstall $(shell echo /usr/share/tpu/*.whl)

	sudo apt install apt-transport-https curl gnupg
	curl -fsSL https://bazel.build/bazel-release.pub.gpg | gpg --dearmor > bazel.gpg
	sudo mv bazel.gpg /etc/apt/trusted.gpg.d/
	echo "deb [arch=amd64] https://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list
	sudo apt update && sudo apt install bazel-3.7.2

	git clone https://github.com/tensorflow/text.git
	cd text && git checkout 2.7b && ./oss_scripts/run_build.sh
	sudo -H pip3 install --upgrade --force-reinstall $(shell echo text/tensorflow_text*.whl)
	sudo rm -r text

compress.datasets:
	tar -czvf datasets.tar.gz datasets