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

tIndividual::tIndividual(pqxx::connection * db, int id, int body_id, string & name):
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
	pqxx::result res = txn->exec("DELETE FROM \
		neuron_schema.tIndividual \
	WHERE \
		id = " + txn->quote(id) + "\
	AND \
		body_id = " + txn->quote(body_id) + "\
	AND \
		name = " + txn->quote(name) + ";");
	txn->commit();
}

//UPDATE
void tIndividual::updateRowSQL(pqxx::work* txn)
{
	pqxx::result res = txn->exec("UPDATE \
		neuron_schema.tIndividual \
	SET \
		body_id = " + txn->quote(body_id) + "\
	AND \
		name = " + txn->quote(name)
	WHERE \
		id = " + txn->quote(pk) + ";");
	txn->commit();
}

//INSERT
void tIndividual::insertRowSQL(pqxx::work* txn)
{
	pqxx::result res = txn->exec("INSERT INTO \
		neuron_schema.tIndividual \
	(id, body_id, name) \
	VALUES (" +\
		txn->quote(id) + " + " + txn->quote(body_id) + " + " + txn->quote(name) + ");");
	txn->commit();
}

//Schema Functions
shared_ptr<tBody> tIndividual::gtBody(void)
{
	shared_ptr<tBody> obj(new tBody(this->m_db, this->body_id) );
	obj->selectRow();
	return obj;
}

paptIndividual tIndividual::gtIndividualsFromBody(pqxx::connection* db, const tBody & body)
{
	paptIndividual obj (new aptIndividual());
	pqxx::work txn(*db);
	pqxx::result res = txn.exec("SELECT \
		id, \
		body_id, \
		name, \
	FROM \
		neuron_schema.tIndividual \
	WHERE \
		body_id = " + txn.quote(body.id) + ";");
	// Only get one result line (as we use the Primary Key
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		int tid = 0;
		int tbody_id = 0;
		string tname;	//default constructor means no constructor brackets
		//Store the values
		dbquery::DBSafeUtils::safeToInt(&tid, res[i]["id"]);
		dbquery::DBSafeUtils::safeToInt(&tbody_id, res[i]["body_id"]);
		dbquery::DBSafeUtils::safeToString(&tname, res[i]["name"]);
		//Create an object
		ptIndividual pt(new tIndividual(db, tid, tbody_id, tname) );
		//Store the object
		obj->push_back(pt);
	}
	return obj;
}

}
