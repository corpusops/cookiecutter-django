ARG SPHINX_IMAGE=sphinxdoc/sphinx
FROM $SPHINX_IMAGE
ARG SPHINX_PYTHON=python
ADD docs/ docs/
ADD local/ local/
ADD *py *md *txt ./
ADD src/ src/
RUN ( [ -e docs/requirements.txt ] && python -m pip install -r docs/requirements.txt )
