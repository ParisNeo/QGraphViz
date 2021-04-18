import setuptools
#with open("README.md", "r") as fh:
#    long_description = fh.read()
long_description="""
Project information here https://github.com/ParisNeo/QGraphViz
"""
setuptools.setup(
     name='QGraphViz',  
     version='0.0.55',
     author="Saifeddine ALOUI",
     author_email="aloui.saifeddine@gmail.com",
     description="A PyQt5 widget to manipulate (build, render, interact, load and save) Graphviz graphs",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/ParisNeo/QGraphViz",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )