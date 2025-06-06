class FileNotSelectedException(Exception):
    """Исключение, выбрасываемое, когда файл не был выбран пользователем.

    Атрибуты:
        message (str): Сообщение об ошибке.
        dialog (str): Строка, описывающая, в каком контексте возникла ошибка.
    """

    def __init__(self, message="Файл не выбран", dialog="Диалог сохранения файла не был завершён пользователем"):
        self.message = message
        self.dialog = dialog
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} - {self.dialog}"

class EmptyIpynbFileException(Exception):
    """Исключение, выбрасываемое, когда загружается пустой Jupyter Notebook без ячеек."""

    def __init__(self, message="Файл пустой. В нем нет ни одной ячейки. Выберите файл, содержащий хотя бы одну ячейку"):
        self.message = message
        super().__init__(self.message)