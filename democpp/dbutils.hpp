#ifndef DBUTILS_HPP
#define DBUTILS_HPP

#include "dbconnection.hpp"

using namespace std;

namespace dbquery {

class DBUtils
{
	public:
		DBUtils(void);
		~DBUtils(void);
	public:
		void toInt(int * integer, const char * integerString);
};

}
#endif //DBUTILS_HPP
