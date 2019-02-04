#include "tbody.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

tBody::tBody(pqxx::connection const * db):
	dbquery::DBResult(db)
{
}

tBody::tBody(pqxx::connection const * db, const int primaryKey):
	dbquery::DBResult(db, primaryKey)
{
}

tBody::~tBody(void)
{
}

//SELECT
void tBody::getRow(void)
{
}

//DELETE
void tBody::deleteRow(int primaryKey)
{
}

//UPDATE
void tBody::saveRow(void)
{
}

//INSERT
void tBody::addRow(void)
{
}

}
