#include "dbsafeutils.hpp"

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

tBody::tBody(pqxx::connection * db, int id, const string & text):
	dbquery::DBResult(db, id),
	id(id),
	text(text)
{
}

tBody::~tBody(void)
{
}

//SELECT
void tBody::selectRowSQL(pqxx::work* txn)
{
	pqxx::result res = txn->exec("SELECT \
		id, \
		text, \
	FROM \
		neuron_schema.tBody \
	WHERE \
		id = " + txn->quote(pk) + ";");
	// Only get one result line (as we use the Primary Key
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		dbquery::DBSafeUtils::safeToInt(&this->id, res[i]["id"]);
		dbquery::DBSafeUtils::safeToString(&this->text, res[i]["text"]);
	}
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
