from datetime import datetime
from rcon.source import Client
import json
import logging

logger = logging.getLogger("ServerHandler")
logging.basicConfig()
logger.setLevel("INFO")


class Server:
    rcon_address: str
    rcon_port: int
    rcon_password: str
    sdr_address: str | None
    server_name: str


    def __init__(
        self, rcon_address: str, rcon_port: int, rcon_password: str, server_name: str
    ):
        self.rcon_address = rcon_address
        self.rcon_port = rcon_port
        self.rcon_password = rcon_password
        self.server_name = server_name
        self.sdr_address = None


    def set_sdr_ip(self, new_sdr_address: str | None) -> bool:
        old_ip = self.sdr_address

        self.sdr_address = new_sdr_address

        if new_sdr_address != old_ip:
            return True
        return False

    def __repr__(self):
        return f"{self.server_name}_[{self.rcon_address}:{self.rcon_port}]"


class ServersInfo:
    __servers: list[Server]
    no_response = int

    def __init__(self):
        self.__servers = []
        self.no_response = 0
        self.load_config()

    def load_config(self):
        logger.info("Cargando información de los servidores")
        self.__servers = []
        with open("servers.json", "r", encoding="utf-8") as config_file:
            configs = json.load(config_file)
            logger.info(f"Encontradas {len(configs)} configuraciones")
            for sv in configs:
                server = Server(
                    rcon_address=sv["rcon_address"],
                    rcon_password=sv["rcon_password"],
                    rcon_port=sv["rcon_port"],
                    server_name=sv["server_name"],
                )
                self.__servers.append(server)

    def get_configs(self) -> list:
        return self.__servers

    def get_ips(self) -> bool:
        responses = []
        self.no_response = 0

        for server in self.__servers:
            logger.info(
                f"Obteniendo la IP del SDR del servidor {server}"
            )
            try:
                with Client(
                    server.rcon_address,
                    passwd=server.rcon_password,
                    port=server.rcon_port,
                ) as client:
                    response = client.run("status")

                address_part = response.split("\n")[2].split(" ")
                if len(address_part) == 13:  # Es SDR
                    logger.info("Found SDR")
                    expose_address = address_part[3]
                else:
                    expose_address = "Sin SDR disponible"

                responses.append(server.set_sdr_ip(expose_address))
            except Exception as e:
                self.no_response += 1
                responses.append(server.set_sdr_ip(None))
                logger.error("No se pudo obtener la IP del servidor")

        
        return any(responses)

    def check_for_changes(self)->bool:
        return self.get_ips()


    def get_servers_info(self) -> str:
        msg = []

        for server in self.__servers:
            server_name = server.server_name
            server_ip = server.sdr_address
            if server_ip and server_ip != "Sin SDR disponible":
                msg += [
                    f"### {server_name}",
                    f"IP: {server_ip}",
                    f"In-game: `connect {server_ip}`",
                    f"Navegador: `steam://connect/{server_ip}`"
                ]
            else:
                msg += [f"### {server_name}", "No Disponible/Sin Información ❌"]

        msg += [
            f"> ⏱️ Última actualización: { datetime.now().strftime('%d-%m-%Y a las %H:%M:%S') }"
        ]

        if self.no_response > 0:
            msg += [f"> 🔻 { self.no_response } sin respuesta"]

        return "\n".join(msg)
