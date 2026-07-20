#include <bits/stdc++.h> 
using namespace std; 

struct Node { 
    int val; 
    Node *prev; 
    Node *next; 
    
    Node(int val) { 
        this->val = val; 
        this->prev = nullptr; 
        this->next = nullptr; 
    } 
}; 

class DoublyLinkedListAppendOnlyMode { 
    Node *head; 
    Node *tail; 

public: 
    DoublyLinkedListAppendOnlyMode() { 
        head = nullptr; 
        tail = nullptr; 
    } 

    void append(int val) { 
        Node *newNode = new Node(val); 
        if (head == nullptr) { 
            head = newNode; 
            tail = newNode; 
        } else { 
            tail->next = newNode; 
            newNode->prev = tail; 
            tail = newNode; 
        } 
    } 

    void displayForward() { 
        Node *temp = head; 
        cout << "Forward: "; 
        while (temp != nullptr) { 
            cout << temp->val << " <-> "; 
            temp = temp->next; 
        } 
        cout << "nullptr" << endl; 
    } 

    void displayBackward() { 
        Node *temp = tail; 
        cout << "Backward: "; 
        while (temp != nullptr) { 
            cout << temp->val << " <-> "; 
            temp = temp->prev; 
        } 
        cout << "nullptr" << endl; 
    } 

    int size() { 
        int count = 0; 
        Node *temp = head; 
        while (temp != nullptr) { 
            count++; 
            temp = temp->next; 
        } 
        return count; 
    } 
}; 

int main() { 
    DoublyLinkedListAppendOnlyMode dll; 

    cout << "Enter the number of elements to append: ";
    int n;
    cin >> n;

    for (int i = 0; i < n; i++) {
        int val;
        cout << "Enter value " << (i + 1) << ": ";
        cin >> val;

        dll.append(val);
    }

    dll.displayForward(); 
    dll.displayBackward(); 
    cout << "List size: " << dll.size() << endl; 

    return 0; 
}
