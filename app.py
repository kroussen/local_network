from typing import List, Optional, Dict


class Server:
    """
    Класс Server представляет собой сервер с возможностью отправки и получения данных через роутер.

    Attributes:
        _id_counter (int): Статический счетчик для генерации IP адресов серверов.
        ip (int): Уникальный IP адрес сервера.
        buffer (List[Data]): Буфер для хранения данных, ожидающих отправки.
        router (Optional[Router]): Ссылка на объект класса Router для установления связи.
    """

    _id_counter: int = 1

    def __init__(self) -> None:
        """
        Инициализирует новый экземпляр сервера с уникальным IP адресом и пустым буфером данных.
        """
        self.ip: int = Server._id_counter
        Server._id_counter += 1

        self.buffer: List[Data] = []
        self.router: Optional[Router] = None

    def send_data(self, data: 'Data') -> None:
        """
        Отправляет данные через подключенный роутер.

        Args:
            data (Data): Данные для отправки.

        """
        if self.router:
            self.router.buffer.append(data)

    def get_data(self) -> List['Data']:
        """
        Получает данные из буфера сервера и очищает его.

        Returns:
            List[Data]: Список полученных данных.

        """
        received_data: List[Data] = self.buffer[:]
        self.buffer.clear()
        return received_data

    def get_ip(self) -> int:
        """
        Возвращает IP адрес сервера.

        Returns:
            int: IP адрес сервера.

        """
        return self.ip

    def connect_router(self, obj_router: 'Router') -> None:
        """
        Устанавливает соединение с указанным роутером.

        Args:
            obj_router (Router): Объект класса Router для установления связи.

        """
        self.router = obj_router


class Router:
    """
    Класс Router представляет собой роутер для управления соединениями с серверами.

    Attributes:
        buffer (List[Data]): Буфер для хранения данных, ожидающих отправки.
        servers (Dict[int, Server]): Словарь для хранения серверов с ключами по их IP адресам.

    """

    def __init__(self) -> None:
        """
        Инициализирует новый экземпляр роутера с пустым буфером данных и пустым словарем серверов.

        """
        self.buffer: List[Data] = []
        self.servers: Dict[int, Server] = {}

    def link(self, server: Server) -> None:
        """
        Устанавливает соединение с указанным сервером.

        Args:
            server (Server): Объект класса Server для установления связи.

        """
        self.servers[server.get_ip()] = server
        server.connect_router(self)

    def unlink(self, server: Server) -> None:
        """
        Разрывает соединение с указанным сервером.

        Args:
            server (Server): Объект класса Server для разрыва связи.

        """
        if server.get_ip() in self.servers:
            del self.servers[server.get_ip()]
            server.connect_router(None)

    def send_data(self) -> None:
        """
        Отправляет данные серверам из буфера, если они доступны для доставки.

        """
        for data in self.buffer:
            if self.servers.get(data.ip):
                self.servers[data.ip].buffer.append(data)
        self.buffer.clear()


class Data:
    """
    Класс Data представляет данные для отправки с указанием IP адреса назначения.

    Attributes:
        data (str): Строка данных для отправки.
        ip (int): IP адрес сервера, к которому данные будут отправлены.

    """

    def __init__(self, data: str, ip: int) -> None:
        """
        Инициализирует новый экземпляр данных с указанной строкой данных и IP адресом назначения.

        Args:
            data (str): Строка данных для отправки.
            ip (int): IP адрес сервера, к которому данные будут отправлены.

        """
        self.data: str = data
        self.ip: int = ip
