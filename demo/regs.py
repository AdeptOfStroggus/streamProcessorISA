from dataclasses import dataclass
from abc import ABC, abstractmethod
import re
import random
from parser import ParseCode
import argparse

@dataclass
class CPUOperand:
    bankName: str
    index: int
    value: int

@dataclass
class CPUCommandOps:
    rdest: CPUOperand
    rvalues: list 

class CPUBank:
    def __init__(self) -> None:
        self.regs = [0 for i in range(32)]
        self.locks = [False for i in range(32)]

    @abstractmethod
    def Write(self, ops: CPUOperand): pass
        
    @abstractmethod
    def Read(self, regIndex: int): pass

    def step(self):
        for i in range(len(self.locks)):
            self.locks[i] = False

class RIBank(CPUBank):
    def __init__(self, vals) -> None:
        super().__init__()
        for i in range(32):
            self.regs[i] = vals[i]
        
    def Read(self, regIndex: int):
        return CPUOperand("RI", regIndex, self.regs[regIndex])
    
    def Write(self, ops: CPUOperand):
        print('Cannot write to RI bank')

    def WriteSimValues(self, values:list):
        for i in range(32):
            self.regs[i] = values[i]


class RCBank(CPUBank):
    def __init__(self, const) -> None:
        super().__init__()
        for i in range(32):
            self.regs[i] = const[i]
        
    def Read(self, regIndex):
        return CPUOperand("RC", regIndex, self.regs[regIndex])
    
    def Write(self, ops: CPUOperand):
        print('Cannot write to RC bank')

    

class ROBank(CPUBank):
    def __init__(self) -> None:
        super().__init__()
        
    def Read(self, regIndex):
        print ("Cannot read from RO bank")
    
    def Write(self, ops: CPUOperand):
        if(self.locks[ops.index] == False):
            self.regs[ops.index] = ops.value
            self.locks[ops.index] = True
        else:
            raise Exception(f"RACE CONDITION ON RO{ops.index}") 
        
    def Push(self):
        #for i in range(32):
        #    print(f"Pushed value from reg_{i}: {self.regs[i]}")
        #print(self.regs)
        return self.regs

class RGPBank(CPUBank):
    def __init__(self) -> None:
        super().__init__()

    def Read(self, regIndex: int):
        return CPUOperand("RG", regIndex, self.regs[regIndex])
    
    def Write(self, ops: CPUOperand):
        if(self.locks[ops.index] == False):
            self.regs[ops.index] = ops.value
            self.locks[ops.index] = True
        else:
            raise Exception(f"RACE CONDITION ON RG{ops.index}") 
        