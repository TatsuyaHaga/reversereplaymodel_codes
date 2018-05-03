// transform integer into string

#include <sstream>
#include <string>

std::string int2str(int Num)
{
    std::stringstream s;
    s << Num;
    return s.str();
}
