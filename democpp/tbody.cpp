#include "tbody.hpp"
using namespace std;
using namespace dbquery;
namespace neuronSchema
{

const string	tbody::SQL_SELECT ("SELECT id, name FROM neuron_schema.tbody WHERE");

tbody::tbody (pqxx::connection * connection):
	dbquery::DBResult (connection)
{
}

tbody::tbody (pqxx::connection * connection, const int id):
	dbquery::DBResult (connection),
	id (id)
{
}

tbody::tbody (pqxx::connection * connection, string & name):
	dbquery::DBResult (connection),
	name (name)
{
}

tbody::tbody (pqxx::connection * connection, int & id, string & name):
	dbquery::DBResult (connection),
	id (id),
	name (name)
{
}

tbody::~tbody (void)
{
}

void tbody::selectRowSQL(pqxx::work & txn)
{

	pqxx::result res = txn.exec(SQL_SELECT + " id = " + txn.quote(id) + ";");
	// Only get one result line (as we use the Primary Key
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		dbquery::DBUtils::toInt(&this->id, res[i]["id"]);
		dbquery::DBUtils::toString(&this->name, res[i]["name"]);

	}
	
}

void tbody::deleteRowSQL(pqxx::work & txn)
{

	pqxx::result res = txn.exec("DELETE FROM \
		neuron_schema.tbody \
	WHERE \
		id = " + txn.quote(id) + \
	";");
	
}

void tbody::updateRowSQL(pqxx::work & txn)
{

	pqxx::result res = txn.exec("UPDATE \
		neuron_schema.tbody \
	SET \
		name  = " + txn.quote(name) + " \
	WHERE \
		id = " + txn.quote(id) + \
	";");

}

void tbody::insertRowSQL(pqxx::work & txn)
{

	pqxx::result res = txn.parameterized("neuron_schema.pInstbody")(txn.quote(name)).exec();
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		dbquery::DBSafeUtils::safeToInt(&this->id, res[i]["neuron_schema.pInstbody"]);
	}

}

int tbody::getId(void )
{
	return id;
}

string tbody::getName(void )
{
	return name;
}

void tbody::setId(int id)
{
	id = id;
	//TODO: Need to add this to the dbTransaction class as an update
	
}

void tbody::setName(string name)
{
	name = name;
	//TODO: Need to add this to the dbTransaction class as an update
	
}



}
