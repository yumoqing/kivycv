# -*- coding: utf-8 -*-
from kivycv.version import __version__
import codecs
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

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
	"kivycv":[
		"*.txt",
		'xcamera/data/*.ttf',
		'xcamera/data/*.wav',
		'xcamera/xcamera.kv',
		'image_processing/cascades/*.xml'
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
