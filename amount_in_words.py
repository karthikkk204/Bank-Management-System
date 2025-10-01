#import openpyxl
#from openpyxl import load_workbook
#import xlrd
import pandas as pd

num_names={
    1: "One",
    2: "Two",
    3: "Three",
    4: "Four",
    5: "Five",
    6: "Six",
    7: "Seven",
    8: "Eight",
    9: "Nine",
    10: "Ten",
    11: "Eleven",
    12: "Twelve",
    13: "Thirteen",
    14: "Fourteen",
    15: "Fifteen",
    16: "Sixteen",
    17: "Seventeen",
    18: "Eighteen",
    19: "Ninteen",
    20:"Twenty",
    30:"Thirty",
    40:"Forty",
    50:"Fifty",
    60:"Sixty",
    70:"Seventy",
    80:"Eighty",
    90:"Ninty",
    100:"Hundred",
    1000:"Thousand",
    100000:"Lakh",
    10000000:"Crore"
}

def one(s):
    if( s == '0'):
        return ""
    return num_names[int(s)]
def two(s):
    if( s == "00"):
        return ''
    if( s[0] == '0'):
      
        return one(int(s[-1]))
    if( int(s) >9 and int(s) < 20 ):
        return num_names[int(s)]
    dec = int( s[0] + '0' )
    return num_names[dec] + " " + one(s[-1])
def three(s):
    if( s== "000"):
        return ""
    if( s[0] == '0'):
        return two(s[1:])
    return one(s[0]) + " Hundred " + two(s[1:])
def four_or_five(s):
    if( len(s) == 4 ):
        if( s == "0000"):
            return ''
        if( s[0] == '0' ):
            return three(s[1:])
        return one(s[0]) + " Thousand " + three(s[1:])
    if( len(s) == 5  ):
        if( s[0] == '0' ):
            return four_or_five(s[1:])
        return two(s[:2]) + " Thousand " + three(s[2:])
def six_or_seven(s):
    if( len(s) == 6 ):
        if( s[0] == '0' ):
            return four_or_five(s[1:])
        return one(s[0]) + " Lakh " + four_or_five(s[1:])
    if( len(s) == 7  ):
        if( s[0] == '0' ):
            return six_or_seven(s[1:])
        return two(s[:2]) + " Lakh " + four_or_five(s[2:])
def eight_and_more(s):
    if( len(s) == 8 ):
        return one(s[0]) + " Crore " + six_or_seven(s[1:])
    more = len(s) - 8
    if( more == 2):
        c = two(s[:2])
    if( more == 3):
        c = three(s[:3])
    if( more == 4):
        c =  four_or_five(s[:4]) 
    return c + " Crore " + six_or_seven(s[-7:])
def words(number):
    s = str(number)
    if( len(s) == 1):
        return "Rupees " + one(s) + " Only"
    if( len(s) == 2):
        return "Rupees " + two(s) + " Only"
    if( len(s) == 3):
        return "Rupees " + three(s) + " Only"
    if( len(s) == 4 or len(s) == 5):
        return "Rupees " + four_or_five(s) + " Only"
    if( len(s) == 6 or len(s) == 7):
        return "Rupees " + six_or_seven(s) + " Only"
    if( len(s) >= 8 ):
        return "Rupees " + eight_and_more(s) + " Only"

def splitTheAddress(address):
    wordList = address.split(",")
    #wordList = [item.strip() for item in wordList]
    wList = ["    " + wordList[indx].strip() for indx in range(len(wordList)) if indx > 0]
    wList.insert(0, wordList[0])
    addList = "\n".join(wList)
    print(addList)
    return addList

def readXls(file):
    # Load the xlsx file
    # Define variable to load the dataframe
    """
     dataframe = load_workbook(file)
    dataframe1 = dataframe.active
    return dataframe1
    
    py_file = (file)
    py_xlrd = xlrd.open_workbook(py_file)
    py_sheet = py_xlrd.sheet_by_index(0)
    return py_sheet
    """
    df = pd.read_excel(file)
    #df.dropna(inplace=True)
    return df
"""
print( words('1') )
print( words('7') )
print( words('89') )
print( words('63') )
print( words('123') )
print( words('347') )
print( words('047') )
print( words('08') )
print( words('0188') )
print( words('2897') )
print(words('12897') )
print(words('10807') )
print(words('100807') )
print(words('534567') )
print(words('1215387') )
print(words('51215387') )
print(words('2651215387') )
print(words('92651215387') )
print(words('892651215387') )
print(words('100000') )
print(words('10000') )
print(words('1000') )
print(words('100') )
"""