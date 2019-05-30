#ifndef DBEXCEPTION_NODATA_HPP
#define DBEXCEPTION_NODATA_HPP

#include "dbexception.hpp"

/*
 * Exception for throwing in the event someone puts in a bad data format into the DB
 * Intention is to stop any database vulnerability with server side testing of inputs
*/

using namespace std;

namespace dbquery {

class DBExceptionNoData : public DBException
{
	public:
		DBExceptionNoData(void);
		~DBExceptionNoData(void);
};

}
#endif //DBEXCEPTION_NODATA_HPP
