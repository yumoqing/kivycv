<<<<<<< HEAD
# -*- coding: utf-8 -*-
from kivycv.version import __version__
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

version = __version__
description = "kivy blocks components relative with opencv"
author = "yumoqing"
email = "yumoqing@icloud.com"

package_data = {
	"kivycv":[
		'imgs/*.png', 
		'imgs/*.gif',
		'imgs/*.jpg',
		'xcamera/xcamera.kv',
		'xcamera/data/*'
		'image_processing/cascades/haarcascade_frontalface_default.xml',
	],
}

setup(
    name="kivycv",
	# ext_modules= cythonize( [ ]),
	ext_modules= [],
    version=version,
    # uncomment the following lines if you fill them out in release.py
    description=description,
    author=author,
    author_email=email,
   
    install_requires=[
	"kivy",
	"kivyblocks",
	"appPublic"
    ],
    packages=[
		'kivycv',
		'kivycv.xcamera',
		'kivycv.image_processing'
	],
    package_data=package_data,
    keywords = [
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
	platforms= 'any'
)
=======
# -*- coding: utf-8 -*-
from kivycv.version import __version__
import codecs
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

# usage:
# python setup.py bdist_wininst generate a window executable file
# python setup.py bdist_egg generate a egg file
# Release information about eway

description = "kivy opencv related modules"
author = "yumoqing"
email = "yumoqing@icloud.com"
version = __version__
depandent_packages = []
with codecs.open('./requirements.txt', 'r', 'utf-8') as f:
	b = f.read()
	b = ''.join(b.split('\r'))
	depandent_packages = b.split('\n')

package_data = {
	"":[
		"*.txt"
	]
}

setup(
    name="kivycv",
	ext_modules= [
		],
    version=version,
    
    # uncomment the following lines if you fill them out in release.py
    description=description,
    author=author,
    author_email=email,
   
    install_requires=depandent_packages,
    packages=[ 'kivycv' ],
    package_data=package_data,
    keywords = [
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
	platforms= 'any'
)
>>>>>>> 46dd7593a6404ee7c8f4c0ad1ad0a8152404d49d
