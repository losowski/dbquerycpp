#include "tbody.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

tBody::tBody(pqxx::connection * db):
	dbquery::DBResult(db)
{
}

tBody::tBody(pqxx::connection * db, const int primaryKey):
	dbquery::DBResult(db, primaryKey)
{
}

tBody::~tBody(void)
{
}

//SELECT
void tBody::selectRowSQL(pqxx::work* txn)
{
}

//DELETE
void tBody::deleteRowSQL(pqxx::work* txn, int primaryKey)
{
}

//UPDATE
void tBody::updateRowSQL(pqxx::work* txn)
{
}

//INSERT
void tBody::insertRowSQL(pqxx::work* txn)
{
}

}
