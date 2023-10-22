import logging

class CustomFormatter(logging.Formatter):
    
    ansi_colors = {
            "Black": "\033[30m",
            "Red": "\033[31m",
            "Green": "\033[32m",
            "Yellow": "\033[33m",
            "Blue": "\033[34m",
            "Magenta": "\033[35m",
            "Cyan": "\033[36m",
            "White": "\033[37m",
            "Reset": "\033[0m"
            }
    
    DEBUG_FMT = ansi_colors["White"]+'%(asctime)s - %(name)s - %(levelname)s - %(message)s'+ansi_colors["Reset"]
    ERROR_FMT = ansi_colors["Red"]+'%(asctime)s - %(name)s - %(levelname)s - %(message)s'+ansi_colors["Reset"]
    WARNING_FMT = ansi_colors["Yellow"]+'%(asctime)s - %(name)s - %(levelname)s - %(message)s'+ansi_colors["Reset"]
    
    def __init__(self, fmt):
        super().__init__(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", style='%')  
        self.user_fmt = fmt
        
    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = CustomFormatter.DEBUG_FMT

        elif record.levelno == logging.INFO:
            self._style._fmt = self.user_fmt

        elif record.levelno == logging.ERROR:
            self._style._fmt = CustomFormatter.ERROR_FMT

        elif record.levelno == logging.WARNING:
            self._style._fmt = CustomFormatter.WARNING_FMT
        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result
          

def setup_logger(name, color = "Reset", level=logging.INFO):
    """To setup as many loggers as you want"""
    
    ansi_colors = CustomFormatter.ansi_colors
    
    formatter = CustomFormatter(ansi_colors[color]+'%(asctime)s - %(name)s - %(levelname)s - %(message)s'+ansi_colors["Reset"])
    
    handler = logging.StreamHandler()     
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propegate = False
    
    return logger