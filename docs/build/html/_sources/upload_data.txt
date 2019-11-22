How to upload your dataset
==========================

A `Upload file support will be added to Alchemy <https://github.com/paulozip/alchemy/issues/4>`_, but you can use the Alchemy REST API to send your dataset. Here's an example of how you can use it using cURL:

.. code-block:: bash

    curl -X POST \
      http://SERVER_ADDRESS:5000/upload_file \
      -H 'content-type: multipart/form-data' \       
      -F file=@PATH_TO_YOUR_FILE

**Example**

.. code-block:: bash

    curl -X POST \
      http://0.0.0.0:5000/upload_file \
      -H 'content-type: multipart/form-data' \       
      -F file=@/home/my_user/Downloads/dataset.csv