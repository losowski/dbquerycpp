/*
	Class to standardise the schema class
 */

#include "dbschemabase.hpp"

using namespace std;

namespace dbquery {

DBSchemaBase::DBSchemaBase (DBConnection & connection, DBTransaction * transaction):
	mtransaction(transaction),
	mdbconnection(connection.getConnection())
{
}

DBSchemaBase::~DBSchemaBase (void)
{
}

pqxx::connection * DBSchemaBase::getConnection(void)
{
	return mdbconnection;
}

}
