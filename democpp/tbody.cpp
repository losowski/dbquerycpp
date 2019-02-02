#include "tbody.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

tBody::tBody(void):
	dbquery::DBResult()
{
}

tBody::tBody(int primaryKey):
	dbquery::DBResult(primaryKey)
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
