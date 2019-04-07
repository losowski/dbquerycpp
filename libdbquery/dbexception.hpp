#ifndef DBEXCEPTION_HPP
#define DBEXCEPTION_HPP

#include <exception>

using namespace std;

namespace dbquery {

class DBException : public exception
{
	public:
		DBException(void);
		~DBException(void);
};

}
#endif //DBEXCEPTION_HPP
