import re

import util.riddle_reader as riddle_reader

import logging

MODULE_REGEX = re.compile(r"^(%|&|broadcaster|)([^\s]+)*? -> ([a-z,\s]+)+$")

LOW_PULSE = "low"
HIGH_PULSE = "high"

# module name string vs. actual module
MODULES = {}


class Module:

    def __init__(self, name: str, outputs: list[str]):
        self.name = name
        self.outputs = outputs

    def process_input(self, input_name: str, pulse_type: str, beam_queue: list[tuple[str, str, str]]):
        pass

    def is_initial_state(self) -> bool:
        pass

    def __repr__(self):
        return f"{type(self).__name__}: name: {self.name}, outputs: {self.outputs}"


class Broadcaster(Module):
    SYMBOL = "broadcaster"

    def __init__(self, outputs: list[str]):
        super().__init__(Broadcaster.SYMBOL, outputs)

    def process_input(self, input_name: str, pulse_type: str, beam_queue: list[tuple[str, str, str]]):
        for output in self.outputs:
            beam_queue.append((output, self.name, pulse_type))

    def is_initial_state(self) -> bool:
        return True


class FlipFlop(Module):
    SYMBOL = "%"

    OFF = "off"
    ON = "on"

    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.power_state = FlipFlop.OFF

    def process_input(self, input_name: str, pulse_type: str, beam_queue: list[tuple[str, str, str]]):
        if pulse_type == HIGH_PULSE:
            return

        if self.power_state == FlipFlop.OFF:
            self.power_state = FlipFlop.ON

            for output in self.outputs:
                beam_queue.append((output, self.name, HIGH_PULSE))
        else:
            self.power_state = FlipFlop.OFF

            for output in self.outputs:
                beam_queue.append((output, self.name, LOW_PULSE))

    def is_initial_state(self) -> bool:
        return self.power_state == FlipFlop.OFF

    def __repr__(self):
        return super().__repr__() + f", power state: {self.power_state}"


class Conjunction(Module):
    SYMBOL = "&"

    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        #
        self.inputs = {}

    def process_input(self, input_name: str, pulse_type: str, beam_queue: list[tuple[str, str, str]]):
        self.inputs[input_name] = pulse_type
        for key, last_pulse in self.inputs.items():
            # send low pulse if all previous states are high
            if last_pulse == LOW_PULSE:
                for output in self.outputs:
                    beam_queue.append((output, self.name, HIGH_PULSE))
                return

        for output in self.outputs:
            beam_queue.append((output, self.name, LOW_PULSE))

    def is_initial_state(self) -> bool:
        for key, last_pulse in self.inputs.items():
            if last_pulse == HIGH_PULSE:
                return False

        return True

    def add_input(self, input_name: str):
        self.inputs[input_name] = LOW_PULSE

    def __repr__(self):
        return super().__repr__() + f", inputs: {self.inputs}"


def is_initial_state():
    for module in MODULES.values():
        if not module.is_initial_state():
            return False

    return True


def run_sequence(repetition: int) -> bool:
    beam_queue = [(Broadcaster.SYMBOL, "", LOW_PULSE)]
    while len(beam_queue) > 0:
        next_module_name, sender_name, pulse_type = beam_queue.pop(0)
        if next_module_name not in MODULES:
            # logging.info(f"module {next_module_name} does not exist")

            if pulse_type == LOW_PULSE:
                return True
            continue
        next_module = MODULES[next_module_name]
        # logging.info(f"{repetition}., {next_module_name}, sender_name = {sender_name}, {beam_queue}")
        next_module.process_input(sender_name, pulse_type, beam_queue)
        # logging.info(next_module)
    return False


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

logging.info("Read input")
lines = riddle_reader.read_file(riddle_reader.RIDDLE_FILE)
for line in lines:
    match = MODULE_REGEX.match(line)
    outputs = re.split(r",\s", match.group(3))
    name = match.group(2)
    if match.group(1) == Broadcaster.SYMBOL:
        MODULES[Broadcaster.SYMBOL] = Broadcaster(outputs)
    elif match.group(1) == FlipFlop.SYMBOL:
        MODULES[name] = FlipFlop(name, outputs)
    elif match.group(1) == Conjunction.SYMBOL:
        MODULES[name] = Conjunction(name, outputs)

conjunctions = [conjunction for conjunction in list(filter(lambda module: isinstance(module, Conjunction), MODULES.values()))]
for conjunction in conjunctions:
    for module in MODULES.values():
        if conjunction.name in module.outputs:
            conjunction.add_input(module.name)

number_of_repetitions = 1000
repetition = 0
is_low_pulse_on_rx = False
while not is_low_pulse_on_rx:
    repetition += 1
    is_low_pulse_on_rx = run_sequence(repetition)
    if is_initial_state():
        logging.info(f"Cycle found after {repetition} repetitions")
        break

    if repetition % 1_000_000 == 0:
        logging.info(f"{repetition} repetitions tested")

logging.info(f"{repetition} repetitions were required to send a low pulse to rx.")
