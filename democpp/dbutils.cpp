#include "dbutils.hpp"

using namespace std;

namespace dbquery {

DBUtils::DBUtils(void)
{
}

DBUtils::~DBUtils(void)
{
}

void DBUtils::toInt(int * integer, const char * integerString)
{
	*integer = stoi(integerString);
}

}
