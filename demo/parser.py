def ParseCode(code_path):
    lines = []
    with open(code_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    #print(lines)

    cleanedLines = []
    for i in range(len(lines)):
        line = lines[i].strip()

        if("//" in line):
            line = line.split("//")[0].strip()

        if line:  
            cleanedLines.append(line)

    #print(cleanedLines)
    
    #Поиск блоков

    codeBlocks = []
    blockStarted = False
    blockStartPos = -1
    for i in range(len(cleanedLines)):
        if(cleanedLines[i] == "BLOCK"):
            if(blockStarted == False):
                blockStarted = True
                blockStartPos = i
            else:
                raise Exception("Incorrect syntax")
        elif(cleanedLines[i] == "ENDBLOCK"):
            if(blockStarted == True):
                blockStarted = False
                codeBlocks.append(cleanedLines[blockStartPos+1:i])
                #print(blockStartPos)
                #print(i)
            else:
                raise Exception("Incorrect syntax")
        elif(blockStarted == False):
            codeBlocks.append(cleanedLines[i])
    print(codeBlocks)
    return codeBlocks





