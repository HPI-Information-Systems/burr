

class Log:
    def __init__(self):
        """
        Initialize the Log class with a QTextEdit logger.
        Define text formats for different log.
        """
        
        #self.logger = logger

        # Define text formats for different log levels

        # Set the text color for each log level

        # Create a dictionary to map log levels to their corresponding text formats
        

    def append_log(self, message, level="info", end="\n"):
        """
        Append a log message with the specified level to the logger.
        The message will be formatted with the corresponding text format.
        The logger will then scroll to the bottom to ensure the latest message is visible.
        """
        print(message)
        # Move the cursor to the end of the logger
        # self.logger.moveCursor(QtGui.QTextCursor.End)

        # # Set the current char format to the format corresponding to the log level
        # self.logger.setCurrentCharFormat(self.text_format[level])

        # # Insert the message into the logger
        # self.logger.insertPlainText(message + end)

        # # Scroll to the bottom of the logger
        # self.logger.verticalScrollBar().setValue(self.logger.verticalScrollBar().maximum())