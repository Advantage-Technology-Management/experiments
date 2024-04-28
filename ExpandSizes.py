outFile = open("Stage600kTestedDirectAllSizes.csv", 'w',encoding="utf-8")
inFile = open("Stage600kTestedDirect.csv",encoding="utf-8")
count = 0
sizes = ["32","70","80","120","140","160","195","300","320","340","380","390","400","580","600","640","680","760","800","1160","2000",
]
for line in inFile:
    count += 1
    print(count)
    #do something
    for size in sizes:
        outFile.writelines(line.rstrip("\n")+"?imWidth="+size+"\n")
inFile.close()
outFile.close()
