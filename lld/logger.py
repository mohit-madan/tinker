import threading
from abc import ABC, abstractmethod
from enum import IntEnum
from datetime import datetime

# --- 1. Model & Enums ---
class LogLevel(IntEnum):
    """Derived from LogLevel.java"""
    DEBUG = 1
    INFO = 2
    WARN = 3
    ERROR = 4
    FATAL = 5

class LogMessage:
    """Matches LogMessage.java"""
    def __init__(self, level: LogLevel, message: str):
        self.level = level #
        self.message = message #
        self.timestamp = int(datetime.now().timestamp() * 1000) # Long timestamp

# --- 2. Formatters (Strategy Pattern) ---
class LogFormatter(ABC):
    """Matches LogFormatter.java"""
    @abstractmethod
    def format(self, message: LogMessage) -> str:
        pass

class PlainTextFormatter(LogFormatter):
    """Matches PlainTextFormatter.java"""
    def format(self, message: LogMessage) -> str:
        dt = datetime.fromtimestamp(message.timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")
        return f"{dt} [{message.level.name}] - {message.message}" #

class JsonFormatter(LogFormatter):
    """Matches JsonFormatter.java"""
    def format(self, message: LogMessage) -> str:
        dt = datetime.fromtimestamp(message.timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")
        return f'{{"timestamp": "{dt}", "level": "{message.level.name}", "message": "{message.message}"}}' #

# --- 3. Appenders (Observer Pattern) ---
class LogAppender(ABC):
    """Base for ConsoleAppender and FileAppender"""
    def __init__(self, formatter: LogFormatter):
        self.formatter = formatter

    @abstractmethod
    def append(self, message: LogMessage):
        pass

class ConsoleAppender(LogAppender):
    def append(self, message: LogMessage):
        print(f"CONSOLE: {self.formatter.format(message)}")

class FileAppender(LogAppender):
    def __init__(self, formatter: LogFormatter, file_name: str):
        super().__init__(formatter)
        self.file_name = file_name

    def append(self, message: LogMessage):
        # In production, this would write to self.file_name
        print(f"FILE ({self.file_name}): {self.formatter.format(message)}")

# --- 4. Log Handlers (Chain of Responsibility + Thread Safety) ---
class LogHandler(ABC):
    """Matches LogHandler.java"""
    def __init__(self):
        self.next = None #
        self.appenders = [] # Matches ArrayList/CopyOnWriteArrayList
        self._lock = threading.Lock() # To handle concurrency safely like CopyOnWriteArrayList

    def set_next(self, next_handler):
        """Setter for the chain"""
        self.next = next_handler
        return next_handler

    def subscribe(self, observer: LogAppender):
        """Thread-safe subscribe"""
        with self._lock:
            self.appenders.append(observer) #

    def notify_observers(self, message: LogMessage):
        """Thread-safe iteration using a snapshot"""
        with self._lock:
            # We take a snapshot of the list to mimic CopyOnWriteArrayList behavior
            current_appenders = list(self.appenders)
        
        for appender in current_appenders:
            appender.append(message) #

    def handle(self, message: LogMessage):
        """Core CoR logic"""
        if self.can_handle(message.level): #
            self.notify_observers(message) #
        
        if self.next:
            self.next.handle(message) #

    @abstractmethod
    def can_handle(self, level: LogLevel) -> bool:
        pass

class InfoHandler(LogHandler):
    def can_handle(self, level: LogLevel): return level == LogLevel.INFO

class WarnHandler(LogHandler):
    """Matches WarnHandler.java"""
    def can_handle(self, level: LogLevel): return level == LogLevel.WARN #

class ErrorHandler(LogHandler):
    """Matches ErrorHandler.java"""
    def can_handle(self, level: LogLevel): return level == LogLevel.ERROR #

# --- 5. Configuration & Entry Point ---
class LogHandlerConfiguration:
    """Matches LogHandlerConfiguration.java"""
    _debug = InfoHandler() # Placeholder for Debug
    _info = InfoHandler()
    _warn = WarnHandler()
    _error = ErrorHandler()

    @classmethod
    def build(cls):
        """Builds the chain"""
        cls._info.set_next(cls._warn).set_next(cls._error) #
        return cls._info

    @classmethod
    def add_appender_for_level(cls, level: LogLevel, appender: LogAppender):
        """Assigns appender to specific level"""
        if level == LogLevel.INFO: cls._info.subscribe(appender)
        elif level == LogLevel.WARN: cls._warn.subscribe(appender)
        elif level == LogLevel.ERROR: cls._error.subscribe(appender)

class Logger:
    """Singleton Logger Entry Point"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.handler_chain = LogHandlerConfiguration.build()
        return cls._instance

    def log(self, level: LogLevel, message: str):
        log_msg = LogMessage(level, message)
        self.handler_chain.handle(log_msg)

# --- 6. Main Execution ---
if __name__ == "__main__":
    # Setup as per Main.java
    logger = Logger()

    LogHandlerConfiguration.add_appender_for_level(
        LogLevel.INFO, ConsoleAppender(PlainTextFormatter()) #
    )
    LogHandlerConfiguration.add_appender_for_level(
        LogLevel.ERROR, ConsoleAppender(PlainTextFormatter()) #
    )
    LogHandlerConfiguration.add_appender_for_level(
        LogLevel.ERROR, FileAppender(PlainTextFormatter(), "logs.txt") #
    )

    print("--- Test INFO ---")
    logger.log(LogLevel.INFO, "System heartbeat is normal.")

    print("\n--- Test ERROR ---")
    logger.log(LogLevel.ERROR, "Database connection failed!")