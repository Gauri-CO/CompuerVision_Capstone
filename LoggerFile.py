import logging

def my_logger():
        # Gets or creates a logger
        logger = logging.getLogger(__name__)
        # logger = logging.getLogger(self.name)

        # set log level
        logger.setLevel(logging.INFO)

        # define handler
        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler('logfile.log')
        file_handler.setLevel(logging.ERROR)
        stream_handler.setLevel(logging.INFO)

        # Create formatters and add it to handlers
        stream_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler.setFormatter(stream_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)
        return logger
