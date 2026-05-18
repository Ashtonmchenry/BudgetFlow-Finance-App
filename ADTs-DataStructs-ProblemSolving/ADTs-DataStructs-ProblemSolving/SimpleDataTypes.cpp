#include <iostream>

using namespace std;

int main() {
	// Simple data types in C++ include:
	// 1. int: Represents integer values (e.g., 1, -5, 42).
	// 2. float: Represents single-precision floating-point numbers (e.g., 3.14, -0.001).
	// 3. double: Represents double-precision floating-point numbers (e.g., 3.14159, -0.00001).
	// 4. char: Represents a single character (e.g., 'A', 'b', '1').
	// 5. bool: Represents boolean values (true or false).
	int myInt = 42; // Example of an integer
	float myFloat = 3.14f; // Example of a float
	double myDouble = 3.14159; // Example of a double
	char myChar = 'A'; // Example of a character


	bool myBool = true; // Example of a boolean
	bool myBoolFalse = false;
	bool myBoolInt = 1;
	bool myBoolIntFalse = 0;


	cout << "Integer: " << myInt << endl;
	cout << "Float: " << myFloat << endl;
	cout << "Double: " << myDouble << endl;
	cout << "Character: " << myChar << endl;
	cout << "Boolean: " << boolalpha << myBool << endl;

	cout << "INT_MIN = " << INT_MIN << endl;
	cout << "Min size of integer variables: " << sizeof(INT_MIN) << " bytes" << endl;
	cout << "INT_MAX = " << INT_MAX << endl;
	cout << "Max size of integer variables: " << sizeof(INT_MAX) << " bytes" << endl;

	cout << myBool << endl;
	cout << myBoolFalse << endl;
	cout << myBoolInt << endl;
	cout << myBoolIntFalse << endl;

	return 0;
}