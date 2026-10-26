// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

// 1. Store and retrieve an integer
contract StoreInteger {
    uint256 num;

    function setNum(uint256 _num) public {
        num = _num;
    }

    function getNum() public view returns (uint256) {
        return num;
    }
}

// 2. Add two numbers and return the result
contract AddNumbers {
    function add(uint256 a, uint256 b) public pure returns (uint256) {
        return a + b;
    }
}

// 3. Check whether a number is even or odd
contract EvenOdd {
    function checkEvenOdd(uint256 n) public pure returns (string memory) {
        if (n % 2 == 0) {
            return "Even";
        }
        return "Odd";
    }
}

// 4. Find the largest of two numbers
contract LargestOfTwo {
    function largest(uint256 a, uint256 b) public pure returns (uint256) {
        if (a > b) {
            return a;
        }
        return b;
    }
}

// 5. Calculate the factorial of a number
contract Factorial {
    function fact(uint256 n) public pure returns (uint256) {
        uint256 result = 1;
        for (uint256 i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }
}

// 6. Calculate simple interest -> SI = (P * R * T) / 100
contract SimpleInterest {
    function calculateSI(
        uint256 principal,
        uint256 rate,
        uint256 time
    ) public pure returns (uint256) {
        return (principal * rate * time) / 100;
    }
}

// 7. Store student details: roll number, name, marks
contract StudentDetails {
    uint256 public rollNumber;
    string public name;
    uint256 public marks;

    function setStudent(
        uint256 _roll,
        string memory _name,
        uint256 _marks
    ) public {
        rollNumber = _roll;
        name = _name;
        marks = _marks;
    }
}

// 8. Maintain a list of students using an array
contract StudentList {
    string[] students;

    function addStudent(string memory _name) public {
        students.push(_name);
    }

    function getStudent(uint256 index) public view returns (string memory) {
        return students[index];
    }

    function totalStudents() public view returns (uint256) {
        return students.length;
    }
}

// 9. Check the balance of the contract
contract CheckBalance {
    // lets the contract actually receive ETH, otherwise balance stays 0 forever
    receive() external payable {}

    function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}

// 10. Demonstrate msg.sender, msg.value, and address(this).balance
contract SenderValueDemo {
    address public lastSender;
    uint256 public lastValue;

    function deposit() public payable {
        lastSender = msg.sender;
        lastValue = msg.value;
    }

    function contractBalance() public view returns (uint256) {
        return address(this).balance;
    }
}
