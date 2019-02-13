#include "dbsafeutils.hpp"

#include "tindividual.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

tIndividual::tIndividual(pqxx::connection * db):
	dbquery::DBResult(db)
{
}

tIndividual::tIndividual(pqxx::connection * db, const int primaryKey):
	dbquery::DBResult(db, primaryKey)
{
}

tIndividual::tIndividual(pqxx::connection * db, int id, int body_id, const string & name):
	dbquery::DBResult(db, id),
	id(id),
	body_id(body_id),
	name(name)
{
}

tIndividual::~tIndividual(void)
{
}

//SELECT
void tIndividual::selectRowSQL(pqxx::work* txn)
{
	pqxx::result res = txn->exec("SELECT \
		id, \
		body_id, \
		name, \
	FROM \
		neuron_schema.tIndividual \
	WHERE \
		id = " + txn->quote(pk) + ";");
	// Only get one result line (as we use the Primary Key
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		dbquery::DBSafeUtils::safeToInt(&this->id, res[i]["id"]);
		dbquery::DBSafeUtils::safeToInt(&this->body_id, res[i]["body_id"]);
		dbquery::DBSafeUtils::safeToString(&this->name, res[i]["name"]);
	}
}

//DELETE
void tIndividual::deleteRowSQL(pqxx::work* txn, int primaryKey)
{
}

//UPDATE
void tIndividual::updateRowSQL(pqxx::work* txn)
{
}

//INSERT
void tIndividual::insertRowSQL(pqxx::work* txn)
{
}

}
