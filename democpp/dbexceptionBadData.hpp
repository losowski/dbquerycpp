#ifndef DBEXCEPTION_BADDATA_HPP
#define DBEXCEPTION_BADDATA_HPP

#include "dbexception.hpp"

using namespace std;

namespace dbquery {

class DBExceptionBadData : public DBException
{
	public:
		DBExceptionBadData(void);
		~DBExceptionBadData(void);
};

}
#endif //DBEXCEPTION_BADDATA_HPP
