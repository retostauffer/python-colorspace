

def logger(name):

    import logging



    FORMAT = "[%(levelname)s %(name)s]  %(message)s"
    logging.basicConfig(format = FORMAT)

    logger = logging.getLogger(name)


    # Logging level, can be controlled by setting
    # an environment variable CSLOGLEVEL.
    import os
    if "CSLOGLEVEL" in os.environ.keys():
        level = getattr(logging, os.environ["CSLOGLEVEL"].upper())
    else:
        level = logging.WARNING

    logger.setLevel(level)


    return logger
