from regs import *
from alu import *
        



class CPU:
    def __init__(self, const, vals) -> None:
        self.RI = RIBank(vals)
        self.RC = RCBank(const)
        self.RO = ROBank()
        self.RGP = RGPBank()
        self.history = []

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
            #print(strings)
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
            #print(i)
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
        data = self.RO.Push()
        self.history.append(data.copy())
        

    def Dump(self):
        #print(self.history)
        return self.history
    
    def inputValues(self, vals):
        self.RI.WriteSimValues(vals)


