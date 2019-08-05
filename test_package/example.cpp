#include <iostream>
#include <quickfix/FixFields.h>

int main() {
    FIX::BeginString string("Hello World!");
    std::cout << string << std::endl;
}
