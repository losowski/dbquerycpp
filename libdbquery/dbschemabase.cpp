/*
	Class to standardise the schema class
 */

#include "dbschemabase.hpp"
#include <ctime>

using namespace std;

namespace dbquery {

const int DBSchemaBase::CACHE_INTERVAL (120 * CLOCKS_PER_SEC);

DBSchemaBase::DBSchemaBase (DBConnection & connection, DBTransaction * transaction):
	mtransaction(transaction),
	mdbconnection(connection.getConnection()),
	mCacheInterval(CACHE_INTERVAL)
{
}

DBSchemaBase::~DBSchemaBase (void)
{
}

pqxx::connection * DBSchemaBase::getConnection(void)
{
	return mdbconnection;
}

//Cache Setup
void DBSchemaBase::setCacheTimeout(int interval)
{
	mCacheInterval = interval;
}

time_t DBSchemaBase::getCacheExpiry(void)
{
	return std::time(nullptr) + mCacheInterval;
}


}
