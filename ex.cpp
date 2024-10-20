#include <iostream>
using namespace std;

int main()
{
    int s1 = 2;
    int s2 = 2;
    bool val = s1 != s2;
    cout << val;
    while (s1 == s2)
    {
        cout << "Hacker";
        s1 = 5;
    }

    return 0;
}