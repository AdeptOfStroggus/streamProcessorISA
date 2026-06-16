from regs import *
class ALU:
    def __init__(self) -> None:
        self.lockedUntillNextStep = False

        self.instr = {
            "ADD2": self.Add2,
            "SUB2": self.Sub2,
            "MUL2": self.Mul2,
            "MAC3": self.Mac3,
            "MOV1": self.Mov1
        }


    def lock(self):
        self.lockedUntillNextStep = True

    def unlock(self):
        self.lockedUntillNextStep = False

    def ValidateOps(self, rops: CPUCommandOps):
        if(len(rops.rvalues) < 1 and len(rops.rvalues) > 3):
            raise TypeError('Add2() requires 1 to 3 values')
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
    
    def Mov1(self, rops: CPUCommandOps):
        self.ValidateOps(rops)
        self.lock()
        return CPUOperand(rops.rdest.bankName, rops.rdest.index, rops.rvalues[0].value)
    
    def Mac3(self, rops: CPUCommandOps):
        self.ValidateOps(rops)
        self.lock()
        return CPUOperand(rops.rdest.bankName, rops.rdest.index, rops.rvalues[0].value * rops.rvalues[1].value + rops.rvalues[2].value)

    def nextStep(self):
        self.unlock()