
from dataclasses import dataclass
from abc import ABC, abstractmethod
import re
import random
from parser import ParseCode

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
        for i in range(32):
            print(f"Pushed value from reg_{i}: {self.regs[i]}")

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
        



class ALU:
    def __init__(self) -> None:
        self.lockedUntillNextStep = False

        self.instr = {
            "ADD2": self.Add2,
            "SUB2": self.Sub2,
            "MUL2": self.Mul2
        }


    def lock(self):
        self.lockedUntillNextStep = True

    def unlock(self):
        self.lockedUntillNextStep = False

    def ValidateOps(self, rops: CPUCommandOps):
        if(len(rops.rvalues) != 2):
            raise TypeError('Add2() requires 2 or 3 values')
        if(self.lockedUntillNextStep == True):
            raise Exception('Cannot use ALU in block twice')

    def Add2(self, rops: CPUCommandOps):
        self.ValidateOps(rops)
        self.lock()
        #print(rops.rvalues[0].value)
        return CPUOperand(rops.rdest.bankName, rops.rdest.index, rops.rvalues[0].value + rops.rvalues[1].value)

    def Sub2(self, rops: CPUCommandOps):
        self.ValidateOps(rops)
        self.lock()
       # print(rops.rvalues[0].value)
        return CPUOperand(rops.rdest.bankName, rops.rdest.index, rops.rvalues[0].value - rops.rvalues[1].value)

    def Mul2(self, rops: CPUCommandOps):
        self.ValidateOps(rops)
        self.lock()
        return CPUOperand(rops.rdest.bankName, rops.rdest.index, rops.rvalues[0].value * rops.rvalues[1].value)
    

    def nextStep(self):
        self.unlock()
        



class CPU:
    def __init__(self, const, vals) -> None:
        self.RI = RIBank(vals)
        self.RC = RCBank(const)
        self.RO = ROBank()
        self.RGP = RGPBank()

        self.banks = {
        'RI': self.RI,
        'RC': self.RC,
        'RO': self.RO,
        'RG': self.RGP
        }

        self.ALUs = {
            'ALU0': ALU(),
            'ALU1': ALU(),
            'ALU2': ALU(),
            'ALU3': ALU(),
            'ALU4': ALU(),
            'ALU5': ALU(),
            'ALU6': ALU(),
            'ALU7': ALU(),
        }
        self.curLines = []

    def initInputs(self, vals):
        self.RI.__init__(vals)

    def step(self, cmd):

        if(isinstance(cmd, list)):
            self.ApplyBlock(cmd)
        elif(isinstance(cmd, str)):
            self.ApplyCommand(cmd)
        else:
            raise Exception("Incorrect cmd")
        for i in dict.items(self.ALUs):
            i[1].unlock()
        for i in dict.items(self.banks):
            i[1].step()

    def ApplyBlock(self, cmds: list):
        for i in cmds:
            self.Execute(i)
        self.commit()

    def Execute(self, cmd: str):
        strings = cmd.split()
        
        instr = strings[0]

        if(instr == "PUSH" or instr == "PUSHN"):
            self.Push()
        else:
            print(strings)
            alu = strings[1]
            rdest = strings[2]
            #print(rdest)
            rops = strings[3:]


            rops2 = []
            for i in rops:
                index = re.findall(r'\d+', i)
                bank = i[0:2]
                value = self.banks[bank].Read(int(index[0]))
                #print(value)

                rops2.append(value)

            a = CPUCommandOps(CPUOperand(rdest, int(re.findall(r'\d+', rdest)[0]), 0), rops2)
            b = self.ALUs[alu].instr[instr](a)
            self.curLines.append(b)

    def commit(self):
        for i in self.curLines:
            print(i)
            self.WriteToRegister(i)
        self.curLines.clear()


    def ApplyCommand(self, cmd: str):
        self.Execute(cmd)
        self.commit()

    def DecodeBank(self, op: CPUOperand):

        if op.bankName[0:2] not in self.banks:
            raise ValueError(f"Invalid bank: '{op.bankName}'")
        return self.banks[op.bankName[0:2]]

    def ProcessCommand(self, op: CPUCommandOps): pass

    def WriteToRegister(self, op: CPUOperand):
        self.DecodeBank(op).Write(op)

    def Push(self):
        self.RO.Push()

def main():
    constants = [i for i in range(32)]
    vals = [32 - i for i in range(32)]
    cpu = CPU(constants, vals)

    code = ParseCode("demo\\firFilter.asm")
    for i in code:
        cpu.step(i)    

if __name__ == "__main__":
    main()
        


