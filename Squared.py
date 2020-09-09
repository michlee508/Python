def square(x):
    # raise x to the second power
    runningtotal = 0
    for counter in range(x):
        runningtotal = runningtotal + x
        print(runningtotal)
    return runningtotal

toSquare = 10
squareResult = square(toSquare)
print("The result of", toSquare, "squared is", squareResult)


r"""
--- Sample run ---
10
20
30
40
50
60
70
80
90
100
The result of 10 squared is 100
"""