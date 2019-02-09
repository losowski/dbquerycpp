/*
 * Utilities to intepret the DB input
*/

#include "dbutils.hpp"

using namespace std;

namespace dbquery {

DBUtils::DBUtils(void)
{
}

DBUtils::~DBUtils(void)
{
}

void DBUtils::toInt(int * integer, const pqxx::field & fieldValue)
{
	*integer = stoi(fieldValue.c_str());
}

void DBUtils::toString(string * str, const pqxx::field & fieldValue)
{
	(*str).assign(fieldValue.c_str());
}

}
