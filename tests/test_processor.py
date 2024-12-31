from async_worker_svc.processor import Processor
from async_worker_svc.types import IncomingMessage


class TestProcessor:
    def test_add_command(self):
        msg = IncomingMessage(id="1", command="ADD", args=[10, 20])
        proc = Processor()
        res = proc.process(msg)
        assert res is not None
        assert res.id == msg.id
        assert res.result == 30

    def test_sub_command(self):
        msg = IncomingMessage(id="1", command="SUB", args=[10, 20])
        proc = Processor()
        res = proc.process(msg)
        assert res is not None
        assert res.id == msg.id
        assert res.result == -10

    def test_mul_command(self):
        msg = IncomingMessage(id="1", command="MUL", args=[10, 20])
        proc = Processor()
        res = proc.process(msg)
        assert res is not None
        assert res.id == msg.id
        assert res.result == 200

    def test_div_command(self):
        msg = IncomingMessage(id="1", command="DIV", args=[10, 20])
        proc = Processor()
        res = proc.process(msg)
        assert res is not None
        assert res.id == msg.id
        assert res.result == 0.5

    def test_div_command_error(self):
        msg = IncomingMessage(id="1", command="DIV", args=[10, 0])
        proc = Processor()
        res = proc.process(msg)
        assert res is not None
        assert res.id == msg.id
        assert res.result is None
        assert res.error == "Division by zero"

    def test_unexpected_command_error(self):
        msg = IncomingMessage(id="1", command="MULTIPLY", args=[10, 0])
        proc = Processor()
        res = proc.process(msg)
        assert res is not None
        assert res.id == msg.id
        assert res.result is None
        assert res.error == "Unexpected command type: MULTIPLY"
