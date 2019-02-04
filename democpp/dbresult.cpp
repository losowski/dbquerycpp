#include "dbresult.hpp"

using namespace std;

namespace dbquery {

DBResult::DBResult(pqxx::connection const * db):
	pk(0),
	m_db(db)
{
}

DBResult::DBResult(pqxx::connection const * db, const int primaryKey):
	pk(primaryKey),
	m_db(db)
{
}

DBResult::~DBResult(void)
{
}

}
