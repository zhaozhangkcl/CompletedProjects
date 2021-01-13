#ifndef ROMAN_H
#define ROMAN_H

#include <string>
using std::string;

// TODO: your code goes here
/* a table of roman character corresponding to its integer value */
 int value(char letter) {

  switch (letter) {
    case 'I':
    return 1;

    case 'V' :
    return 5;

    case 'X':
    return 10;

    case 'L':
    return 50;

    case 'C':
    return 100;

    case 'D':
    return 500;

    case 'M':
    return 1000;
  }
}








/* a function that coverts a roman letter in string format to integer */
 int romanToInteger(string input) {
  /*declare a varialbe for storing result and declare a separte variable to
  keep track previous value*/
  int result = 0;
  int previous = 0;
  //use a for loop to loop through the character array from right to left
  for(int i = input.length()-1; i>=0; i--) {
  //check if current corresponding value is greater than previous
    if(value(input[i]) >= previous) {
  //add the value to result
  result += value(input[i]);
}
  //else if the value is smaller than previous
else {
  //subtract the value from resulting
  result -= value(input[i]);
}
  //update previous before next iteration
  previous = value(input[i]);
}
  //return result
  return result;
}




// Do not edit below this line

#endif
