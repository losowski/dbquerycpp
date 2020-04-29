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

void tbody::initialise(pqxx::connection * connection)
{
	connection->prepare("neuron_schema.pinstbody", "SELECT * FROM neuron_schema.pinstbody($1)");
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
	clockSavedToDB();

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
	clockSavedToDB();

}

void tbody::insertRowSQL(pqxx::work & txn)
{

	pqxx::result res = txn.prepared("neuron_schema.pinstbody")(txn.quote(name)).exec();
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		dbquery::DBSafeUtils::safeToInt(&this->id, res[i][0]);
	}
	clockSavedToDB();

}

int tbody::getId(void )
{
	accessed();
	return id;
}

string tbody::getName(void )
{
	accessed();
	return name;
}

void tbody::setId(int id)
{
	if (this->id != id)
	{
		this->id = id;
		clockModified();
		//TODO: Need to add this to the dbTransaction class as an update
	}
}

void tbody::setName(string name)
{

	if (this->name != name)
	{
		this->name = name;
		clockModified();
		//TODO: Need to add this to the dbTransaction class as an update
	}
}

int tbody::getSequencetbody_id_seq(void)
{
	int nextValue = 0;
	pqxx::work txn(*mDBConnection);
	pqxx::result res = txn.exec("SELECT NEXTVAL('tbody_id_seq');");
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		nextValue = stoi(res[i]["nextval"].c_str());
	}
	return nextValue;
}


}
