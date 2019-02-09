#ifndef DBEXCEPTION_BADDATA_HPP
#define DBEXCEPTION_BADDATA_HPP

#include "dbexception.hpp"

/*
 * Exception for throwing in the event someone puts in a bad data format into the DB
 * Intention is to stop any database vulnerability with server side testing of inputs
*/

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
