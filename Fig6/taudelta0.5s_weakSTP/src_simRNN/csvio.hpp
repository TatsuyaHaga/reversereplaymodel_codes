
#ifndef CSVIO_HPP

#define CSVIO_HPP

//Input from/Output to CSV file (default delimiter='\t')

#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>

/***********************************************************/

template <class T>
class readCSV
{
protected:
    std::ifstream fs;
public:
    readCSV();
    readCSV(const char *address);
    readCSV(const readCSV &obj);
    readCSV<T>& operator=(const readCSV<T> &obj);
    int open(const char *address);
    void close();
    std::vector<T> read1D();
    std::vector<std::vector<T> > read2D();
};

template <class T>
readCSV<T> :: readCSV()
{
}

template <class T>
readCSV<T> :: readCSV(const char *address)
{
    open(address);
}

template <class T>
readCSV<T> :: readCSV(const readCSV &obj)
{
}

template <class T>
readCSV<T>& readCSV<T> :: operator=(const readCSV<T> &obj)
{
    return (*this);
}

template <class T>
int readCSV<T> :: open(const char *address)
{
    int ret=0;
    fs.open(address);
    if(!fs)
    {
        std::cerr << "Error::could not open CSV file.\n" << std::endl;
        ret=-1;
    }

    return ret;
}

template <class T>
void readCSV<T> :: close()
{
    fs.close();
}

template <class T>
std::vector<T> readCSV<T> :: read1D()
{
    T val;
    std::vector<T> ret;
    char ch;
    std::stringstream ss;
    ret.resize(0);
    
    while(fs.get(ch))
    {
        if(ch=='\t' || ch==' ' || ch==',')
        {
            if(!ss.str().empty())
            {
                ss >> val;
                ret.push_back(val);
                ss.str("");
                ss.clear();
            }
        }
        else if(ch=='\n')
            break;
        else
            ss << ch;
    }

    if(!ss.str().empty())
    {
        ss >> val;
        ret.push_back(val);
    }
    
    return ret;
}

template <class T>
std::vector<std::vector<T> > readCSV<T> :: read2D()
{
    std::vector<T> temp;
    std::vector<std::vector<T> > ret;

    
    while(!fs.eof())
        if((temp=read1D()).size()!=0)
            ret.push_back(temp);
    
    return ret;
}

/***********************************************************/

template <class T>
class writeCSV
{
protected:
    std::ofstream fs;
    char delimiter;//default:'\t'
public:
    writeCSV();
    writeCSV(const char *address);
    writeCSV(const writeCSV<T> &obj);
    writeCSV<T>& operator=(const writeCSV<T> &obj);
    int open(const char *address);
    void close();
    void set_delimiter(char ch);
    void write1D(std::vector<T> &vec);
    void write2D(std::vector<std::vector<T> > &vec);
};

template <class T>
writeCSV<T> :: writeCSV()
{
    delimiter='\t';
}

template <class T>
writeCSV<T> :: writeCSV(const char *address)
{
    delimiter='\t';
    open(address);
}

template <class T>
writeCSV<T> ::writeCSV(const writeCSV<T> &obj)
{
    delimiter=obj.delimiter;
}

template <class T>
writeCSV<T>& writeCSV<T> :: operator=(const writeCSV<T> &obj)
{
    delimiter=obj.delimiter;
    return (*this);
}

template <class T>
int writeCSV<T> :: open(const char *address)
{
    int ret=0;
    fs.open(address);
    if(!fs)
    {
        std::cerr << "Error::could not open CSV file.\n" << std::endl;
        ret=-1;
    }

    return ret;
}

template <class T>
void writeCSV<T> :: close()
{
    fs.close();
}

template <class T>
void writeCSV<T> :: set_delimiter(char ch)
{
    delimiter=ch;
}

template <class T>
void writeCSV<T> :: write1D(std::vector<T> &vec)
{
    for(int i=0; i<(signed)vec.size(); i++)
    {
        fs << vec[i];
        if(i!=(signed)vec.size()-1)
            fs << delimiter;
    }
    fs << std::endl;
}

template <class T>
void writeCSV<T> :: write2D(std::vector<std::vector<T> > &vec)
{
    for(int i=0; i<(signed)vec.size(); i++)
        write1D(vec[i]);
}

/***********************************************************/

template <class T>
class readCSVstdin
{
public:
    std::vector<T> read1D();
    std::vector<std::vector<T> > read2D();
};

template <class T>
std::vector<T> readCSVstdin<T> :: read1D()
{
    T val;
    std::vector<T> ret;
    char ch;
    std::stringstream ss;
    ret.resize(0);
    
    while(std::cin.get(ch))
    {
        if(ch=='\t' || ch==' ' || ch==',')
        {
            if(!ss.str().empty())
            {
                ss >> val;
                ret.push_back(val);
                ss.str("");
                ss.clear();
            }
        }
        else if(ch=='\n')
            break;
        else
            ss << ch;
    }

    if(!ss.str().empty())
    {
        ss >> val;
        ret.push_back(val);
    }
    
    return ret;
}

template <class T>
std::vector<std::vector<T> > readCSVstdin<T> :: read2D()
{
    std::vector<T> temp;
    std::vector<std::vector<T> > ret;
    
    while(!std::cin.eof())
        if((temp=read1D()).size()!=0)
            ret.push_back(temp);
    
    return ret;
}

/***********************************************************/

template <class T>
class writeCSVstdout
{
protected:
    char delimiter;//default:'\t'
public:
    writeCSVstdout();
    void set_delimiter(char ch);
    void write1D(std::vector<T> &vec);
    void write2D(std::vector<std::vector<T> > &vec);
};

template <class T>
writeCSVstdout<T> :: writeCSVstdout()
{
    delimiter='\t';
}

template <class T>
void writeCSVstdout<T> :: set_delimiter(char ch)
{
    delimiter=ch;
}

template <class T>
void writeCSVstdout<T> :: write1D(std::vector<T> &vec)
{
    for(int i=0; i<(signed)vec.size(); i++)
    {
        std::cout << vec[i];
        if(i!=(signed)vec.size()-1)
            std::cout << delimiter;
    }
    std::cout << std::endl;
}

template <class T>
void writeCSVstdout<T> :: write2D(std::vector<std::vector<T> > &vec)
{
    for(int i=0; i<(signed)vec.size(); i++)
        write1D(vec[i]);
}


/***********************************************************/

template <class T>
std::vector<std::vector<T> > loadtxt(const char *address)
{
    readCSV<T> read(address);
    return read.read2D();
}

template <class T>
void savetxt(const char *address, std::vector<std::vector<T> > &x, char delimiter)
{
    writeCSV<T> write(address);
    write.set_delimiter(delimiter);
    write.write2D(x);
}

#endif
