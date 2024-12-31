from typing import Optional

from loguru import logger

from async_worker_svc.types import IncomingMessage, OutgoingMessage


class Processor:
    def process(self, msg: IncomingMessage) -> OutgoingMessage:
        logger.info(f"Processing <{msg.command}> command (#{msg.id}) with args: {msg.args}")
        if msg.command == "ADD":
            num1, num2 = msg.args
            return OutgoingMessage(id=msg.id, result=num1 + num2)
        elif msg.command == "SUB":
            num1, num2 = msg.args
            return OutgoingMessage(id=msg.id, result=num1 - num2)
        elif msg.command == "MUL":
            num1, num2 = msg.args
            return OutgoingMessage(id=msg.id, result=num1 * num2)
        elif msg.command == "DIV":
            num1, num2 = msg.args
            if num2 == 0:
                return OutgoingMessage(id=msg.id, result=None, error="Division by zero")
            return OutgoingMessage(id=msg.id, result=num1 / num2)

        return OutgoingMessage(id=msg.id, result=None, error=f"Unexpected command type: {msg.command}")
