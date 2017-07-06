# EProctorX

A Proctoring layer that can be integrated into any EdX exam (preferably in timed exams). Also saves the images of cheating instances to some directory to allow future reference and cross - validation. Implemented as an Internship project as a part of IITBombayX team.

### Installation steps :-


1) OpenCV 2.4.9
```
	sudo apt-get install libopencv-dev python-opencv
```
Copy cv.py,cv.pyc, cv2.x86 64-linux-gnu.so from local to virtual environment site packages


2) dlib
Github proxy settings:
```
	- git config –global http.proxy http://proxyuser:proxypwd@proxy.server.com:8080
	- git config –global https.proxy https://proxyuser:proxypwd@proxy.server.com:8080
	- git config –global ftp.proxy ftp://proxyuser:proxypwd@proxy.server.com:8080	
	- git config –global url.”https://”.insteadOf git://
```

Wget proxy settings:
```
	- Open /.wegtrc file
	- use proxy=on
	- http proxy= proxyuser:proxypwd@proxy.server.com:8080
	- https proxy= proxyuser:proxypwd@proxy.server.com:8080
	- ftp proxy= proxyuser:proxypwd@proxy.server.com:8080
```

Install dlib:
```
	- clone dlib repository in proctor folder
	- sudo apt-get cmake
	- cd dlib-18.16/python examples
	- mkdir build
	- cd build
	- cmake ../../tools/python
	- cmake –build . –config Release
	- sudo cp dlib.so /usr/local/lib/python2.7/dist-packages
	- Copy dlib.so virtual environment site packages
```


3) Torch (to be installed in desktop environment without using sudo)
if trying to install second time due to some failure for first time remove cache of luarocks

```
	- sudo rm -rf /.cache/luarocks
	- git clone https://github.com/torch/distro.git /torch –recursive
```
Change permissions of torch folder by sudo chmod 777 torch

```
	- cd /torch; bash install-deps;
	- ./install.sh
	- source /.bashrc
	- ln -s /root/torch/install/bin/th /usr/local/bin/th
```

4) Dependencies of neural networks :
```
	luarocks install dpnn
	luarocks install nn
	luarocks install optim
	luarocks install csvigo
	luarocks install tds
	luarocks install torchx
	luarocks install optnet
```

5) Openface (to be installed in desktop environment)
```
	- git clone https://github.com/cmusatyalab/openface.git
	- Inside Openface folder - sudo python2 setup.py install
	- Copy openface from /usr/local/lib/python2.7/dist-packages to venv/lib/python2.7
	- In openface folder run - sudo models/get-models.sh
```

## Contributors

- Pranav Dixit (https://github.com/prnvdixit)
- Siva Donkada (https://github.com/sivadonkada)
- Hemanth Katari
