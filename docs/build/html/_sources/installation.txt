Installation
============

Alchemy can be used in three different ways:

Web
^^^
| If you are just curious about what you can do with Alchemy, `you can refer to this website <https://project-alchemy.herokuapp.com>`_.
| This version contains some example datasets that you can use to check how Alchemy works.

**Please note that this version is a Heroku's free tier instance**. Due to high traffic, you may experience some poor performance

Docker
^^^^^^
Run the following commands to use Alchemy with Docker (requires **Docker and Docker-compose**)

.. code-block:: bash

    # Run the docker compose
    docker-compose up --build

Local installation
^^^^^^^^^^^^^^^^^^
**Tip**: we recommend you to use Anaconda environments 

.. code-block:: bash

    # Clone the repository
    git clone https://github.com/paulozip/alchemy.git
    cd alchemy

    # If you're using Anaconda
    conda create --name alchemy_env
    conda activate alchemy_env

    # Install dependencies
    pip install requirements.txt

    # Run Streamlit
    streamlit run run.py