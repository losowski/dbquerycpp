#include "dbresult.hpp"

using namespace std;

namespace dbquery {

DBResult::DBResult(void):
	pk(0)
{
}

DBResult::DBResult(int primaryKey):
	pk(primaryKey)
{
}

DBResult::~DBResult(void)
{
}

}
