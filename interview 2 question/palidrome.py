
def checkPalindrome(number) :
    reversedNumber = ''

    for i in range(len(number)-1, -1, -1) :
        reversedNumber += number[i];

    if number == reversedNumber :
        return True;
    else : return False;
    
    
number = input("Enter the number ");

print(checkPalindrome(number));