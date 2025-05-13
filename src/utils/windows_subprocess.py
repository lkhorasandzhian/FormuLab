from subprocess import Popen as _Popen, CREATE_NO_WINDOW, STARTUPINFO, STARTF_USESHOWWINDOW

# Monkey-патч для subprocess.Popen, чтобы скрыть окна подпроцессов Windows.
# Это нужно, чтобы при вызове внешних консольных программ (например, pandoc)
# не появлялись мерцающие окна терминала.
def popen_hidden(*args, **kwargs):
    # noinspection GrazieInspection
    """
    Обёртка для subprocess.Popen, позволяющая скрыть консольное окно
    в дочерних процессах на Windows.

    :param args: Позиционные аргументы, передаваемые оригинальному Popen
    :param kwargs: Именованные аргументы; сюда будет добавлен 'creationflags' и 'startupinfo'
    :return: Экземпляр Popen, запущенный с настройками скрытия окна
    """
    # Устанавливаем флаг CREATE_NO_WINDOW, если он ещё не задан.
    # Это предотвращает появление консольного окна.
    kwargs.setdefault("creationflags", CREATE_NO_WINDOW)

    # Инициализируем или получаем существующий startupinfo для процесса.
    si = kwargs.get("startupinfo", STARTUPINFO())
    # Добавляем флаг SHOWWINDOW в startupinfo, чтобы окно было скрыто.
    si.dwFlags |= STARTF_USESHOWWINDOW
    # Сохраняем обновлённый объект startupinfo в аргументы.
    kwargs["startupinfo"] = si

    # Вызываем оригинальный Popen с нашими модификациями.
    return _Popen(*args, **kwargs)