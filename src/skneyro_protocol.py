# Реализация протокола обмена сообщениями
from logger import Logger
from config_models import Settings

logger_obj = Logger()

class SkNeuroProtocol:
    """Утилиты для формирования и разбора команд."""

    def __init__(self, config: Settings):
        self.config = config

    def calculate_crc8(self, message):
        """Расчёт CRC8 для строки."""
        crc = 0
        poly = 0x07
        for byte in message.encode('utf-8'):
            crc ^= byte
            for _ in range(8):
                crc = ((crc << 1) ^ poly) if (crc & 0x80) else (crc << 1)
                crc &= 0xFF
        return format(crc, '02X')

    def format_command(self, cmd_type, typ, obj, params, front_hider='$', back_hider='$'):
        """Формирование строки команды по протоколу."""
        cmd_str = f"{cmd_type}|{typ}|{obj}|" + "|".join(map(str, params))
        crc = self.calculate_crc8(cmd_str)
        full_cmd = f"{front_hider}{cmd_str}|{crc}{back_hider}"
        logger_obj.log(f"Formatted command: {full_cmd}", "DEBUG")
        return full_cmd

    def parse_message(self, message):
        """Разбор входящих сообщений и проверка CRC."""
        if not message:
            return None
        if message[0] not in ['$', '€', '#'] or message[-1] not in ['$', '€', '#']:
            logger_obj.log("Invalid message format", "ERROR")
            return None
        content = message[1:-1]
        parts = content.split('|')
        crc_received = parts[-1]
        data_str = "|".join(parts[:-1])
        crc_calculated = self.calculate_crc8(data_str)
        if crc_received != crc_calculated:
            logger_obj.log("CRC check failed", "ERROR")
            return None
        return parts[:-1]

    def get_status_message(self):
        """Создание сообщения о состоянии детектора."""
        typ = self.config.ndc.type_id
        obj = self.config.ndc.id
        message = f"#MST|{typ}|{obj}|0|Detector OK|TXT"
        crc = self.calculate_crc8(message[1:])
        full_msg = f"#MST|{typ}|{obj}|0|Detector OK|TXT|{crc}#"
        return full_msg

    def restart_command(self):
        """Формирование команды перезапуска."""
        typ = self.config.ndc.type_id
        obj = self.config.ndc.id
        params = [0, 0, "On"]
        return self.format_command("€RES", typ, obj, params, front_hider="€", back_hider="€")