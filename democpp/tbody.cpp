#include "tbody.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

tBody::tBody(DBConnection const * db):
	dbquery::DBResult(db)
{
}

tBody::tBody(DBConnection const * db, int primaryKey):
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
