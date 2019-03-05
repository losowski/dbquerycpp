#include "dbsafeutils.hpp"

#include "tbody.hpp"

using namespace std;
using namespace dbquery;

namespace neuronSchema {

tBody::tBody(dbquery::DBConnection * connection):
	dbquery::DBResult(connection)
{
}

tBody::tBody(dbquery::DBConnection * connection, const int primaryKey):
	dbquery::DBResult(connection, primaryKey)
{
}

tBody::tBody(dbquery::DBConnection * connection, int id, const string & name):
	dbquery::DBResult(connection, id),
	id(id),
	name(name)
{
}

tBody::~tBody(void)
{
}

//SELECT
void tBody::selectRowSQL(shared_ptr<pqxx::work> txn)
{
	pqxx::result res = txn->exec("SELECT \
		id, \
		name, \
	FROM \
		neuron_schema.tBody \
	WHERE \
		id = " + txn->quote(pk) + ";");
	// Only get one result line (as we use the Primary Key
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		dbquery::DBSafeUtils::safeToInt(&this->id, res[i]["id"]);
		dbquery::DBSafeUtils::safeToString(&this->name, res[i]["name"]);
	}
}

//DELETE
void tBody::deleteRowSQL(shared_ptr<pqxx::work> txn, int primaryKey)
{
	pqxx::result res = txn->exec("DELETE FROM \
		neuron_schema.tBody \
	WHERE \
		id = " + txn->quote(id) + "\
	AND \
		name  = " + txn->quote(name) + ";");
}

//UPDATE
void tBody::updateRowSQL(shared_ptr<pqxx::work> txn)
{
	pqxx::result res = txn->exec("UPDATE \
		neuron_schema.tBody \
	SET \
		name  = " + txn->quote(name) + "\
	WHERE \
		id = " + txn->quote(id) + ";");
}

//INSERT
void tBody::insertRowSQL(shared_ptr<pqxx::work> txn)
{
	pqxx::result res = txn->exec("INSERT INTO \
		neuron_schema.tBody \
	(id, name) \
	VALUES (" +\
		txn->quote(id) + " + " + txn->quote(name) + ");");
}

}
