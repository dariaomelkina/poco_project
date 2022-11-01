#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Assembly Simulator project 2020
# GNU General Public License v3.0
import os
import unittest
from bitarray.util import ba2hex

from modules.processor import CPU
from modules.assembler import Assembler

# This module tests the basic functionality of the processor module, including
# its initialization (registers, program text, memory etc.)
# and the correct behaviour of all assembly instructions


class TestCPU(unittest.TestCase):
    def setUp(self):
        """ Loads the common programs for testing """
        test_programs = [('stack', os.path.join("modules", "demos", "stack", 'alphabet_printout.asm')),
                         ('stack', os.path.join("modules", "demos", "stack", "helloworld.asm")),
                         ('risc', os.path.join("modules", "demos", "risc", "helloworld.asm")),
                         ('risc', os.path.join("modules", "demos", "risc", "alphabet_printout.asm")),
                         ('risc', os.path.join("modules", "program_examples", "assembly_test6.asm")),
                         ('risc', os.path.join("modules", "program_examples", "complete_risc.asm")),
                         ('stack', os.path.join("modules", "program_examples", "complete_stack.asm")),
                         ('accumulator', os.path.join("modules", "demos", "accumulator", "helloworld.asm")),
                         ('accumulator', os.path.join("modules", "demos", "accumulator", "alphabet_printout.asm")),
                         ('accumulator', os.path.join("modules", "program_examples", "complete_accumulator.asm")),
                         ('cisc', os.path.join("modules", "program_examples", "complete_cisc.asm")),
                         ('stack', os.path.join("modules", "program_examples", "label_test_stack.asm")),
                         ('accumulator', os.path.join("modules", "program_examples", "label_test_accumulator.asm")),
                         ('risc', os.path.join("modules", "program_examples", "label_test_risc.asm")),
                         ('cisc', os.path.join("modules", "program_examples", "label_test_cisc.asm")),
                         ('cisc', os.path.join("modules", "program_examples", "directive_test_cisc.asm"))]

        output_files = self.reassemble(test_programs)

        with open(output_files[0], "r") as file:
            self.stack_alphabet = file.read()

        with open(output_files[1], "r") as file:
            self.stack_hello_world = file.read()

        with open(output_files[2], "r") as file:
            self.risc_hello_world = file.read()

        with open(output_files[3], "r") as file:
            self.risc_alphabet = file.read()

        with open(output_files[4], "r") as file:
            self.risc_program_text = file.read()

        with open(output_files[5], "r") as file:
            self.complete_risc = file.read()

        with open(output_files[6], "r") as file:
            self.complete_stack = file.read()

        with open(output_files[7], "r") as file:
            self.accumulator_hello_world = file.read()

        with open(output_files[8], "r") as file:
            self.accumulator_alphabet = file.read()

        with open(output_files[9], "r") as file:
            self.complete_accumulator = file.read()

        with open(output_files[10], "r") as file:
            self.complete_cisc = file.read()

        with open(output_files[11], "r") as file:
            self.label_stack = file.read()

        with open(output_files[12], "r") as file:
            self.label_accumulator = file.read()

        with open(output_files[13], "r") as file:
            self.label_risc = file.read()

        with open(output_files[14], "r") as file:
            self.label_cisc = file.read()

        with open(output_files[15], "r") as file:
            self.directives_cisc = file.read()

    @staticmethod
    def reassemble(programs):
        """ Reassembles all the test programs """
        output_files = []
        for program in programs:
            with open(program[1], 'r') as file:
                program_text = file.read()
            binary_program = Assembler(program[0], program_text).binary_code
            output_path = os.path.join(os.path.dirname(program[1]),
                                       os.path.splitext(os.path.basename(program[1]))[0] + ".bin")
            output_files.append(output_path)
            with open(output_path, "w") as file:
                file.write(binary_program)
        return output_files

    def test_program_loading(self):
        """ Tests the correct program loading in the memory """
        cpu_neumann = CPU("risc", "neumann", "special", self.risc_program_text)
        cpu_harvard = CPU("risc", "harvard", "special", self.risc_program_text)

        # Testing Neumann architecture
        self.assertEqual(ba2hex(cpu_neumann.program_memory.slots[512*8:512*8 + 16*8]), "184119011a5b5500680488080c0263fc")
        self.assertEqual(ba2hex(cpu_neumann.data_memory.slots[512*8:512*8 + 16*8]), "184119011a5b5500680488080c0263fc")

        # Testing Harvard architecture
        self.assertEqual(ba2hex(cpu_harvard.data_memory.slots), "0"*2048)
        self.assertEqual(ba2hex(cpu_harvard.program_memory.slots[512*8:512*8 + 16*8]), "184119011a5b5500680488080c0263fc")

    def test_program_loading_offset(self):
        """ Tests the correct byte program_start for each architecture """
        cpu_stack = CPU("stack", "neumann", "special", self.stack_alphabet, program_start=512)
        self.assertEqual(ba2hex(cpu_stack.program_memory.slots[512*6:512*6 + 22*6]),
                         "8810479816e90061eb00188004ea3fe5c")

        cpu_accumulator = CPU("accumulator", "neumann", "special", self.accumulator_alphabet, program_start=512)
        self.assertEqual(ba2hex(cpu_accumulator.program_memory.slots[512*8:512*8 + 16*8]), "81004185005b8800048f00010f87fffc")

        cpu_risc = CPU("risc", "neumann", "special", self.risc_program_text, program_start=512)
        self.assertEqual(ba2hex(cpu_risc.program_memory.slots[512*8:512*8 + 16*8]), "184119011a5b5500680488080c0263fc")

    def test_labels(self):
        """ Tests correct workflow of labels """
        cpu_stack = CPU("stack", "neumann", "special", self.label_stack)
        cpu_accumulator = CPU("accumulator", "neumann", "special", self.label_accumulator)
        cpu_risc = CPU("risc", "neumann", "special", self.label_risc)
        cpu_cisc = CPU("cisc", "neumann", "special", self.label_cisc)
        cpu_directives_cisc = CPU("cisc", "neumann", "special", self.directives_cisc)

        for cpu in [cpu_stack, cpu_accumulator]:
            for _ in range(4):
                cpu.web_next_instruction()
            self.assertEqual(ba2hex(cpu.registers['IP']._state), '0200')

        for cpu in [cpu_risc, cpu_cisc]:
            for _ in range(5):
                cpu.web_next_instruction()
            self.assertEqual(ba2hex(cpu.registers['R00']._state), '000f')

        for _ in range(14):
            cpu_directives_cisc.web_next_instruction()
        self.assertEqual(str(cpu_directives_cisc.ports_dictionary['1']), '              animea')

    def test_alphabet(self):
        """ Tests the correct alphabet printout for Stack and RISC architecture """
        cpu_stack = CPU("stack", "harvard", "special", self.stack_alphabet)
        cpu_accumulator = CPU("accumulator", "harvard", "special", self.accumulator_alphabet)
        cpu_risc = CPU("risc", "neumann", "special", self.risc_alphabet)

        # Skipping the needed amount of instructions
        for _ in range(50):
            cpu_stack.web_next_instruction()
        for _ in range(30):
            cpu_accumulator.web_next_instruction()
        for _ in range(35):
            cpu_risc.web_next_instruction()

        alphabet_check = ["              ABCDEF", "GHIJKLMNOPQRSTUVWXYZ"]

        self.assertEqual(str(cpu_stack.ports_dictionary["1"]), alphabet_check[0])
        self.assertEqual(str(cpu_accumulator.ports_dictionary["1"]), alphabet_check[0])
        self.assertEqual(str(cpu_risc.ports_dictionary["1"]), alphabet_check[0])

        # Skipping the needed amount of instructions
        for _ in range(165):
            cpu_stack.web_next_instruction()
        for _ in range(100):
            cpu_accumulator.web_next_instruction()
        for _ in range(100):
            cpu_risc.web_next_instruction()

        self.assertEqual(str(cpu_stack.ports_dictionary["1"]), alphabet_check[1])
        self.assertEqual(str(cpu_accumulator.ports_dictionary["1"]), alphabet_check[1])
        self.assertEqual(str(cpu_risc.ports_dictionary["1"]), alphabet_check[1])

    def test_hello_world(self):
        """ Tests the correct 'Hello world' workflow for Stack and RISC architecture """
        cpu_stack = CPU("stack", "harvard", "special", self.stack_hello_world)
        cpu_accumulator = CPU("accumulator", "harvard", "special", self.accumulator_hello_world)
        cpu_risc = CPU("risc", "neumann", "special", self.risc_hello_world)

        # Skipping the needed amount of instructions
        for _ in range(73):
            cpu_stack.web_next_instruction()
        for _ in range(84):
            cpu_accumulator.web_next_instruction()
        for _ in range(95):
            cpu_risc.web_next_instruction()

        self.assertEqual(ba2hex(cpu_risc.program_memory.slots[-192:]),
                         "00480065006c006c006f00200077006f0072006c00640021")

        self.assertEqual(str(cpu_stack.ports_dictionary["1"]), "        Hello world!")
        self.assertEqual(str(cpu_accumulator.ports_dictionary["1"]), "        Hello world!")
        self.assertEqual(str(cpu_risc.ports_dictionary["1"]), "        Hello world!")

    def test_stack_complete(self):
        """ Tests all of the instructions of Stack ISA """
        cpu = CPU("stack", "neumann", "special", self.complete_stack)
        cpu.web_next_instruction()

        # Checking the mov $1022 instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(tos_val*8 - 16, tos_val*8).to01(), '0000001111111110')

        # Checking the mov $5 instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8).to01(), '0000000000000101')

        # Checking the push instruction
        cpu.web_next_instruction()
        self.assertEqual(cpu.data_memory.read_data(1024 * 8 - 16, 1024 * 8).to01(), '0000000000000101')

        # Checking the load instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8).to01(), '0000000000000101')

        # Checking the loadf instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8).to01(), '0000000000000000')

        # Checking the load $1022 instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8).to01(), '0000000000000101')

        # Checking the mov $0 instruction
        cpu.web_next_instruction()

        # Checking the store $128 instruction
        cpu.web_next_instruction()
        self.assertEqual(cpu.data_memory.read_data(0, 16).to01(), '0000000010000000')

        # Skipping the mov $128 instruction
        cpu.web_next_instruction()

        # Checking the storef instruction
        cpu.web_next_instruction()
        self.assertEqual(cpu.registers['FR']._state.to01(), '0000000010000000')

        # Checking the pushf instruction
        cpu.web_next_instruction()
        stack_frame = int(cpu.registers['SP']._state.to01(), 2)
        self.assertEqual(cpu.registers['FR']._state.to01(),
                         cpu.data_memory.read_data(stack_frame*8, stack_frame*8+16).to01())

        # Skipping through mov $12, mov $15 instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the swap instruction
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(tos_val*8 - 32, tos_val*8 - 16).to01(), '0000000000001100')
        self.assertEqual(cpu.data_memory.read_data(tos_val*8 - 16, tos_val * 8).to01(), '0000000000001111')
        cpu.web_next_instruction()
        self.assertEqual(cpu.data_memory.read_data(tos_val*8 - 32, tos_val*8 - 16).to01(), '0000000000001111')
        self.assertEqual(cpu.data_memory.read_data(tos_val*8 - 16, tos_val*8).to01(), '0000000000001100')

        # Checking the dup2 instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(tos_val*8 - 48, tos_val*8 - 32).to01(),
                         cpu.data_memory.read_data(tos_val*8 - 16, tos_val*8).to01())

        # Checking the dup instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(tos_val * 8 - 32, tos_val * 8 - 16).to01(),
                         cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8).to01())

        # Checking the push instruction
        cpu.web_next_instruction()
        stack_frame = int(cpu.registers['SP']._state.to01(), 2)
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(stack_frame * 8, stack_frame * 8 + 16).to01(),
                         cpu.data_memory.read_data(tos_val * 8, tos_val * 8 + 16).to01())

        # Skipping through mov $1 instruction
        cpu.web_next_instruction()

        # Checking the pop instruction
        cpu.web_next_instruction()
        stack_frame = int(cpu.registers['SP']._state.to01(), 2)
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(stack_frame * 8 - 16, stack_frame * 8).to01(),
                         cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8).to01())

        # Skipping through the push instruction
        cpu.web_next_instruction()

        # Checking the popf instruction
        cpu.web_next_instruction()
        stack_frame = int(cpu.registers['SP']._state.to01(), 2)
        self.assertEqual(cpu.registers['FR']._state.to01(),
                         cpu.data_memory.read_data(stack_frame * 8 - 16, stack_frame*8).to01())

        # Skipping through mov $1 and mov $2 instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the add instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(cpu.data_memory.read_data(tos_val*8 - 16, tos_val*8).to01(), '0000000000000011')

        # Skipping through mov $3, mov $2 instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the sub instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val*8-16, tos_val*8)), 'ffff')

        # Skipping through two mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the mul instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val*8-16, tos_val*8)), 'fffd')

        # Skipping through two mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the div instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), '0003')

        # Skipping through two mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the and instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val*8 - 16, tos_val*8)), '0002')

        # Skipping through two mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the or instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), '0007')

        # Skipping through two mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the xor instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), '0005')

        # Skipping through mov $15 instruction
        cpu.web_next_instruction()

        # Checking the not instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), 'fff0')

        # Skipping through mov $2 instruction
        cpu.web_next_instruction()

        # Checking the lsh instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), '0004')

        # Checking the rsh instruction
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), '0002')

        # Checking the call $2 instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0265')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0269')

        # Checking the call instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '026d')

        # Checking the ret instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '026a')

        # Checking the call $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '026e')

        # Skipping through two mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking a cmpe instruction, should have pushed ffff on to the tos
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), 'ffff')

        # Skipping through two more mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking a cmpe instruction, should have pushed 0000 on tos
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), '0000')

        # Checking two cmpe instructions
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), 'ffff')

        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), '0000')

        # Skipping through two more mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking two cmpb instructions, should have pushed ffff and 0000 on tos (2 > 1) (5 < ffff)
        cpu.web_next_instruction()
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val * 8 - 16, tos_val * 8)), 'ffff')

        # Checking a conditional jump
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '028e')

        # Skipping a mov $0 instruction
        cpu.web_next_instruction()

        # Checking that the conditional jump does not occur
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0294')

        # Checking that an unconditional jump occurs
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0298')

        # Skipping a mov instruction
        cpu.web_next_instruction()

        # Checking the out $1 instruction
        cpu.web_next_instruction()
        self.assertEqual(str(cpu.ports_dictionary['1']), '                   E')

        # Checking the in $1 instruction
        cpu.web_next_instruction()
        cpu.input_finish(bin(69)[2:])
        tos_val = int(cpu.registers['TOS']._state.to01(), 2)
        self.assertEqual(ba2hex(cpu.data_memory.read_data(tos_val*8 - 16, tos_val*8)), '0045')

    def test_accumulator_complete(self):
        """ Tests all of the instructions of Accumulator ISA """
        cpu = CPU("accumulator", "neumann", "special", self.complete_accumulator)
        cpu.web_next_instruction()

        # Testing the mov $512 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '0200')

        # Testing the storei instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers["IR"]._state), ba2hex(cpu.registers['ACC']._state))

        # Testing the load instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512*8, 512*8+16)), ba2hex(cpu.registers['ACC']._state))

        # Testing the inc and dec instructions
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '8103')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '8102')

        # Testing the loadf instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), ba2hex(cpu.registers['FR']._state))

        # Testing the loadi instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), ba2hex(cpu.registers['IR']._state))

        # Testing the store instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512*8, 512*8+16)), ba2hex(cpu.registers['ACC']._state))

        # Testing the store $228 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512 * 8, 512 * 8 + 16)), '00e4')

        # Testing the storef instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), ba2hex(cpu.registers['ACC']._state))

        # Skipping through the mov instruction
        cpu.web_next_instruction()

        # Testing the push instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(1024*8-16, 1024*8)), ba2hex(cpu.registers['ACC']._state))

        # Testing the pushf instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(1024*8-32, 1024*8-16)), ba2hex(cpu.registers['FR']._state))

        # Testing the pushi instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(1024*8-48, 1024*8-32)), ba2hex(cpu.registers['IR']._state))

        # Testing the popf instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(1024*8-48, 1024*8-32)), ba2hex(cpu.registers['FR']._state))

        # Testing the pop instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(1024*8-32, 1024*8-16)), ba2hex(cpu.registers['ACC']._state))

        # Testing the popi instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(1024*8-16, 1024*8)), ba2hex(cpu.registers['IR']._state))

        # Skipping through two preparation instructions...
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the add instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '02e4')

        # Checking the sub instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '0200')

        # Skipping the store and mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the mul instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '0400')

        # Checking the div instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '0002')

        # Skipping three preparation instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the bitwise and instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '0001')

        # Skipping the mov instruction
        cpu.web_next_instruction()

        # Checking the bitwise or instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '0007')

        # Skipping the mov instruction
        cpu.web_next_instruction()

        # Checking the bitwise xor instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '0006')

        # Checking the bitwise not instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), 'fff9')

        # Checking the bitwise rsh instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '7ffc')

        # Checking the bitwise lsh instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), 'fff8')

        # Skipping the mov instruction
        cpu.web_next_instruction()

        # Checking the call instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '023d')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0240')

        # Checking the call instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0246')

        # Checking the return instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0243')

        # Checking the jmp instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0247')

        # Skipping the mov instruction
        cpu.web_next_instruction()

        # Checking the jmp instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '024a')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '024d')

        # Skipping the mov, store instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the cmp instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0004')

        # Checking the je instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0254')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0258')

        # Checking the cmp instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0001')

        # Checking the je instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '025b')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '025c')

        # Checking the cmp instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0001')

        # Checking the jne instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '025f')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0261')

        # Checking the jne instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0265')

        # Checking the test instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0002')

        # Checking the test instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0006')

        # Checking the in instruction
        cpu.web_next_instruction()
        cpu.input_finish(bin(ord("a"))[2:])
        self.assertEqual(ba2hex(cpu.registers['ACC']._state), '0061')

        # Checking the out $1 instruction
        cpu.web_next_instruction()
        cpu.web_next_instruction()
        self.assertEqual(str(cpu.ports_dictionary['1']), '                   E')

    def test_risc_complete(self):
        """ Tests all of the instructions of RISC ISA """
        cpu = CPU("risc", "neumann", "special", self.complete_risc)
        cpu.web_next_instruction()

        # Check the mov_high %R00, $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(cpu.registers['R00']._state.to01(), '0000001000000000')

        # Check the mov_low %R00, $-1 instruction
        cpu.web_next_instruction()
        self.assertEqual(cpu.registers['R00']._state.to01(), '0000000011111111')

        # Checking the mov_high %R00, $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(cpu.registers['R00']._state.to01(), '0000001011111111')

        # Checking the mov %R01, %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(cpu.registers['R00']._state.to01(), cpu.registers['R01']._state.to01())

        # Checking the mov_low %R01, $0 instruction
        cpu.web_next_instruction()
        self.assertEqual(cpu.registers['R01']._state.to01(), '0'*16)

        # Checking the mov_high %R01, $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(cpu.registers['R01']._state.to01(), '0000001000000000')

        # Checking the load %R00, [%R01] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '2002')

        # Checking the mov_low %R01, $0 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '0000')

        # Checking the store [%R01], %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.slots[0:16]), ba2hex(cpu.registers['R00']._state))

        # Checking the push %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.slots[-16:]), ba2hex(cpu.registers['R00']._state))

        # Checking the pop %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.slots[-16:]), ba2hex(cpu.registers['R01']._state))

        # Checking the add %R00, %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '4004')

        # Checking the sub %R00, %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '2002')

        # Checking the mov_low %R02, $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R02']._state), '0002')

        # Checking the mul %R01, %R01, %R02 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '4004')

        # Checking the div %R01, %R01, %R02 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '2002')

        # Checking the mov_low %R02, $5 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R02']._state), '0005')

        # Checking the and %R00, %R01, %R02 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0000')

        # Checking the or %R00, %R01, %R02 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '2007')

        # Checking the xor %R00, %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0005')

        # Checking the not %R00, %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), 'fffa')

        # Checking the mov_low %R00, $5 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0005')

        # Checking the mov_low %R02, $1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R02']._state), '0001')

        # Checking the rsh %R00, %R00, %R02 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0002')

        # Checking the lsh %R00, %R00, %R02 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0004')

        # Checking the call $5 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '023c')

        # Checking the call $-3 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0236')

        # Checking the call %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '023e')

        # Checking the ret instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0238')

        # Checking the nop instruction
        self.assertEqual(cpu.instruction.to01(), '1000110000000000')
        cpu.web_next_instruction()

        # Checking the jmp $3 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0240')

        # Checking the jmp %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0248')

        # Checking the mov_low %R00, $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0002')

        # Checking the cmp %R00, %R02 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0000')

        # Checking the je $-2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '024e')

        # Checking the jne $-6 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0242')

        # Checking the cmp %R00, $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0004')

        # Checking the je $6 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0250')

        # Checking the cmp %R00, $6 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0001')

        # Checking the jg $5 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0254')

        # Checking the nop instruction
        self.assertEqual(cpu.instruction.to01(), '1000110000000000')
        cpu.web_next_instruction()

        # Checking the jge $5 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0258')

        # Checking the jl $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '025c')

        # Checking the jle $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0260')

        # Checking the cmp %R00, $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0004')

        # Checking the jle $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0266')

        # Checking the jl $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0268')

        # Checking the mov_low %R00, $64 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0040')

        # Checking the out $1, %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(str(cpu.ports_dictionary['1']), '                   @')

        # Checking the in %R00, $1 instruction
        cpu.web_next_instruction()
        cpu.input_finish(bin(ord("a"))[2:])
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0061')

    def test_cisc_complete(self):
        """ Tests all of the instructions of CISC ISA """
        cpu = CPU("cisc", "neumann", "special", self.complete_cisc)
        cpu.web_next_instruction()

        # Check the mov %R00, $5 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0200')

        # Check the mov %R01, %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), ba2hex(cpu.registers['R00']._state))

        # Check the mov %R00, [%R01] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '8000')

        # Check the mov %R00, [%R01+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0200')

        # Check the mov [%R01], %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512*8, 512*8 + 16)), ba2hex(cpu.registers['R00']._state))

        # Check the mov [%R01], $666 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512*8, 512*8 + 16)), '029a')

        # Check the mov %R01, $128 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '0080')

        # Check the mov [%R01+$2], %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(130*8, 132*8)), '0080')

        # Check the mov [%R01+$2], $512 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(130*8, 132*8)), '0200')

        # Check the push %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(1024*8-16, 1024*8)), ba2hex(cpu.registers['R01']._state))

        # Check the push $512 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(1024*8-32, 1024*8-16)), '0200')

        # Check the pop %R01 instruction
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '0080')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '0200')

        # Check the enter $5 instruction
        self.assertEqual(ba2hex(cpu.registers['SP']._state), '03fe')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['BP']._state), '03fc')
        self.assertEqual(ba2hex(cpu.registers['SP']._state), '03f7')

        # Check the leave instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['BP']._state), '0400')
        self.assertEqual(ba2hex(cpu.registers['SP']._state), '03fe')

        # Check the add %R00, [%R00] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '049a')

        # Check the add %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '069a')

        # Check the add %R01, [%R01+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '0400')

        # Skipping a mov instruction
        cpu.web_next_instruction()

        # Checking the add [%R00], %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512*8, 512*8+16)), '049a')

        # Skipping a mov instruction
        cpu.web_next_instruction()

        # Checking the sub %R01, [%R01] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '0002')

        # Checking the sub %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '01fe')

        # Checking the sub %R00, [%R00+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), 'fd64')

        # Skipping through a mov instruction
        cpu.web_next_instruction()

        # Checking a sub %R00, [%R00+$-2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), 'fd68')

        # Checking a inc %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), 'fd69')

        # Checking a inc [%R01] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(16, 32)), '0001')

        # Checking a inc [%R01+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(32, 48)), '0001')

        # Checking a dec %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), 'fd68')

        # Checking a dec [%R01] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(16, 32)), '0000')

        # Checking a dec [%R01+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(32, 48)), '0000')

        # Skipping through two mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the mul %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '000c')

        # Checking the div %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0002')

        # Checking the mul %R00, [%R02] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0400')

        # Checking the div %R00, [%R02] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0002')

        # Checking the mul [%R02], %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(514*8, 516*8)), '0400')

        # Checking the div [%R02], %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(514*8, 516*8)), '0200')

        # Checking the mul %R01, $3 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '0012')

        # Checking the div %R01, $3 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R01']._state), '0006')

        # Skipping a mov instruction
        cpu.web_next_instruction()

        # Checking the mul %R00, [%R02+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0400')

        # Checking the div %R00, [%R02+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0002')

        # Checking the and %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0002')

        # Skip a mov instructiom
        cpu.web_next_instruction()

        # Checking the or %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0007')

        # Checking the and %R00, [%R02] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0002')

        # Checking the or %R00, [%R02] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '049a')

        # Skipping two mov instructions
        cpu.web_next_instruction()
        cpu.web_next_instruction()

        # Checking the xor %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0007')

        # Checking the xor %R00, [%R02] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '049d')

        # Checking the not %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), 'fb62')

        # Checking the not [%R02] instruction
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512 * 8, 514 * 8)), '049a')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512 * 8, 514 * 8)), 'fb65')

        # Skipping the mov instruction
        cpu.web_next_instruction()

        # Checking the lsh %R00, $1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0008')

        # Checking the rsh %R00, $1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0004')

        # Checking the rsh [%R02], $1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512 * 8, 514 * 8)), '7db2')

        # Checking the lsh [%R02], $1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512 * 8, 514 * 8)), 'fb64')

        # Checking the rsh [%R02+$2], $1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(514 * 8, 516 * 8)), '0100')

        # Checking the lsh [%R02+$2], $1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(514 * 8, 516 * 8)), '0200')

        # Checking the call $2 instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02c5')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02c9')

        # Checking the call %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02d3')

        # Checking the ret instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02cb')

        # Checking the call %R00+$1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02d5')

        # Checking the ret instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02cf')

        # Checking the jmp $5 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02d6')

        # Checking the nop instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02d7')

        # Checking the jmp %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02e1')

        # Checking the mov %R00, $-5 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), 'fffb')

        # Checking the jmp %R00+$1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02d9')

        # Checking the cmp %R00, $-5 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0004')

        # Checking the je $4 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02e9')

        # Checking the cmp %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0001')

        # Checking the jne $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02ef')

        # Checking the cmp %R00, [%R02] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0002')

        # Checking the jg $5 instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02f1')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02f4')

        # Checking the jl $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '02f8')

        # Checking the mov %R00, $512 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0200')

        # Checking the cmp %R00, [%R02+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0004')

        # Checking the jl $2 instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0300')
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0303')

        # Checking the jge $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0309')

        # Checking the jle $-1 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0306')

        # Checking the jmp $2 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '030c')

        # Checking the test %R00, %R01 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0006')

        # Checking the test %R00, [%R02] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0002')

        # Checking the test %R00, [%R02+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['FR']._state), '0002')

        # Checking the in %R00, $1 instruction
        cpu.web_next_instruction()
        cpu.input_finish(bin(69)[2:])
        self.assertEqual(ba2hex(cpu.registers['R00']._state), '0045')

        # Checking the in [%R02], $1 instruction
        cpu.web_next_instruction()
        cpu.input_finish(bin(70)[2:])
        self.assertEqual(ba2hex(cpu.data_memory.read_data(512*8, 514*8)), '0046')

        # Checking the in [%R02+$2], $1 instruction
        cpu.web_next_instruction()
        cpu.input_finish(bin(71)[2:])
        self.assertEqual(ba2hex(cpu.data_memory.read_data(514*8, 516*8)), '0047')

        # Checking the out $1, %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(str(cpu.ports_dictionary['1']), '                   E')

        # Checking the out $1, [%R02] instruction
        cpu.web_next_instruction()
        self.assertEqual(str(cpu.ports_dictionary['1']), '                  EF')

        # Checking the out $1, [%R02+$2] instruction
        cpu.web_next_instruction()
        self.assertEqual(str(cpu.ports_dictionary['1']), '                 EFG')

        # Skipping a mov instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.registers['R02']._state), '0200')

        # Checking the load4 [%R02] instruction
        self.assertEqual(ba2hex(cpu.registers['IP']._state), '0334')
        cpu.web_next_instruction()
        test_str = ba2hex(cpu.data_memory.read_data(512*8, 520*8))
        self.assertEqual(ba2hex(cpu.registers['R00']._state), test_str[0:4])
        self.assertEqual(ba2hex(cpu.registers['R01']._state), test_str[4:8])
        self.assertEqual(ba2hex(cpu.registers['R02']._state), test_str[8:12])
        self.assertEqual(ba2hex(cpu.registers['R03']._state), test_str[12:16])

        # Skipping a mov instruction
        cpu.web_next_instruction()

        # Checking the store4 [%R02] instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(256 * 8, 264 * 8)), '0046004701006104')

        # Skipping a mov instruction
        cpu.web_next_instruction()

        # Checking the add4 [%R02], %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(256 * 8, 264 * 8)), '0047004801016105')

        # Checking the sub4 [%R02], %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(256 * 8, 264 * 8)), '0046004701006104')

        # Skipping a mov instruction
        cpu.web_next_instruction()

        # Checking the mul4 [%R02], %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(256 * 8, 264 * 8)), '008c008e02003df8')

        # Checking the div4 [%R02], %R00 instruction
        cpu.web_next_instruction()
        self.assertEqual(ba2hex(cpu.data_memory.read_data(256 * 8, 264 * 8)), '0046004701001efc')


if __name__ == '__main__':
    unittest.main()
