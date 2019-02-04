#include "dbresult.hpp"

using namespace std;

namespace dbquery {

DBResult::DBResult(DBConnection const * db):
	pk(0),
	m_db(db)
{
}

DBResult::DBResult(DBConnection const * db, int primaryKey):
	pk(primaryKey),
	m_db(db)
{
}

DBResult::~DBResult(void)
{
}

}
