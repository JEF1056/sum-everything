.PHONY : install tpu

install:
	sudo apt update
	sudo apt upgrade -y
	sudo apt install -y python3-pip unzip
	sudo -H pip3 install -y --upgrade pip
	sudo -H pip3 install -r data/requirements.txt
	sudo -H pip3 install -r train/requirements.txt

tpu:
	install
	sudo -H pip3 install --upgrade $(ls /usr/share/tpu/*.whl)

compress.datasets:
	tar -czvf datasets.tar.gz datasets