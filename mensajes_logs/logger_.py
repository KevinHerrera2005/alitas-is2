import logging
import os
import traceback

from flask import has_request_context, session


class _UsuarioFilter(logging.Filter):
    def filter(self, record):
        usuario = "anonimo"
        try:
            if has_request_context():
                usuario = session.get("inicio_sesion_de_la_persona", "anonimo")
        except Exception:
            usuario = "anonimo"

        record.usuario = usuario
        return True


class Logger:

    def __set_logger(self, nombre, fecha):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        log_directory = os.path.join(base_dir, "logs")
        os.makedirs(log_directory, exist_ok=True)

        log_filename = f"{nombre}-{fecha}.log"
        log_path = os.path.join(log_directory, log_filename)

        logger = logging.getLogger(log_filename)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        if logger.hasHandlers():
            logger.handlers.clear()

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.addFilter(_UsuarioFilter())

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(usuario)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    @classmethod
    def add_to_log(cls, level, message, nombre, fecha):
        try:
            logger = cls().__set_logger(nombre, fecha)

            if level == "critical":
                logger.critical(message)
            elif level == "debug":
                logger.debug(message)
            elif level == "error":
                logger.error(message)
            elif level == "info":
                logger.info(message)
            elif level == "warn":
                logger.warning(message)
        except Exception as ex:
            print(traceback.format_exc())
            print(ex)