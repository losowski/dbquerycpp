#ifndef DBUTILS_HPP
#define DBUTILS_HPP

/*
 * Utilities to intepret the DB input
*/

using namespace std;

namespace dbquery {

class DBUtils
{
	public:
		DBUtils(void);
		~DBUtils(void);
	public:
		static void toInt(int * integer, const pqxx::field & fieldValue);
		static void toString(string * str, const pqxx::field & fieldValue);
};

}
#endif //DBUTILS_HPP
