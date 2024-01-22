#include <iostream>
#include <string>
#include <fstream>

extern "C" {
    long long int* getfiledist(char* fname);
}

long long int* getfiledist(char* fname)
{
    long long int* arr = new long long int[256];
    int count = 0;
    for (int i=0; i<256; i++)
    {
        arr[i] = 0;
    }
    std::fstream fs;
    int i;

    fs.open(fname, std::ios::binary | std::ios::in);

    char buffer[1024];
    // std::cout << fname << "\n";
    while (1)
    {
        fs.read(buffer, 1024);
        count = fs.gcount();
        for (int i=0; i<count; i++)
        {
            if (buffer[i] >= 0) arr[buffer[i]] += 1;
            else arr[127-buffer[i]] += 1;
        }
        if (count < 1024) break;
    }
    
    fs.close();
    return arr;
}

/*int main() {
    long long int *a = new long long int[256];
    a = getfiledist("C:\\Users\\Kurosaki_Ichigo\\Downloads\\MFC-7860DW-inst-C1-EU.EXE");
    for (int i=0; i<256; i++)
    {
        std::cout << a[i] << " ";
    }
    std::cout << "\n";
}*/