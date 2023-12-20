import os
import logging
from app.configurations.development.config_parser import args


class CustomConsoleFormatter(logging.Formatter):
    """
    Modify the way DEBUG messages are displayed.
    """

    def __init__(
        self,
        fmt="%(asctime)s [%(levelname).1s] [%(userIdKey)s: %(userId)s] [%(sessionIdKey)s: %(sessionId)s] %(message)s",
    ):
        logging.Formatter.__init__(self, fmt=fmt, datefmt="%Y-%m-%d %H:%M:%S")

    def format(self, record):
        # Remember the original format
        format_orig = self._fmt
        info_fmt = "%(asctime)s [%(levelname)s] [%(userIdKey)s: %(userId)s] [%(sessionIdKey)s: %(sessionId)s] %(message)s"
        debug_fmt = "%(asctime)s [%(levelname)s] [%(userIdKey)s: %(userId)s] [%(sessionIdKey)s: %(sessionId)s] {%(module)s:%(funcName)s:%(lineno)d} %(message)s"

        if record.levelno == logging.INFO:
            if args.verbose:
                print(record.getMessage())
            self._fmt = info_fmt
        else:
            self._fmt = debug_fmt
            logging.Formatter._fmt = debug_fmt
        result = logging.Formatter.format(self, record)
        self._fmt = format_orig
        return result


class Logger:
    def __init__(self, user_id, session_id, log_file=None):
        self.log_file = log_file
        self.user_id = user_id
        self.session_id = session_id
        self.extra = self._get_extra
        self.formatter = CustomConsoleFormatter()
        self.logger = self.init_logger()

    @property
    def _get_extra(self):
        return {
            "userIdKey": "U",
            "userId": str(self.user_id),
            "sessionIdKey": "S",
            "sessionId": str(self.session_id),
        }

    @property
    def _set_stream_handler(self):
        if args.streamlog:
            self.handler = logging.StreamHandler()
        else:
            if self.log_file:
                self.handler = logging.FileHandler(self.log_file)
            else:
                self.handler = logging.StreamHandler()

    def _is_log_folder_exists(self, folder_path):
        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
                if args.verbose:
                    print("The 'logs' folder has been created.")
            except OSError as e:
                # TODO: Add this exception in logging
                self.logger.error(
                    f"Error: Unable to create the 'sessions' folder - {e}"
                )
                return

    def update_logger_session(self, user_id, session_id):
        self.user_id = user_id
        self.session_id = session_id
        self.extra = self._get_extra
        self.logger = logging.LoggerAdapter(self.logger_with_handler, self.extra)

    def init_logger(self):
        self._is_log_folder_exists(os.path.dirname(self.log_file))

        # Set up a logger
        self.logger_with_handler = logging.getLogger("logger")
        self.logger_with_handler.setLevel(logging.DEBUG)

        self._set_stream_handler

        self.handler.setFormatter(self.formatter)
        self.logger_with_handler.addHandler(self.handler)
        logger = logging.LoggerAdapter(self.logger_with_handler, self.extra)

        return logger

    # Example usage
    # logger = Logger("app.log")
    # logger.log("This is an informational message")
    # logger.log("This is a warning message", level=logging.WARNING)
