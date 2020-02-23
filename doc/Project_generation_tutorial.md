# Project generation tutorial

## Create distribution

```bash
python setup.py sdist bdist_wheel
```

## Install it

To install QGraphViz locally without pushing it to pip do the following

```bash
python -m pip install --upgrade --force-reinstall dist/QGraphViz-*.*.*-py3-none-any.whl
```

replace * with the version you are using

## Publish it

python -m twine upload dist/*

## Update README.md

Do all updates in misc/unprocessed_README.md, then preprocess it using [pp](https://github.com/CDSoft/pp) :

```bash
pp doc/unprocessed_README.md > README.md
```

pp will process the unprocessed_README.md and apply special macros to generate the final README.md file.
