#include "tindividual.hpp"
using namespace std;
using namespace dbquery;
namespace neuronSchema
{

const string	tindividual::SQL_SELECT ("SELECT body_id, id, name FROM neuron_schema.tindividual WHERE");

tindividual::tindividual (pqxx::connection * connection):
	dbquery::DBResult (connection)
{
}

tindividual::tindividual (pqxx::connection * connection, const int id):
	dbquery::DBResult (connection),
	id (id)
{
}

tindividual::tindividual (pqxx::connection * connection, int & body_id, string & name):
	dbquery::DBResult (connection),
	body_id (body_id),
	name (name)
{
}

tindividual::tindividual (pqxx::connection * connection, int & body_id, int & id, string & name):
	dbquery::DBResult (connection),
	body_id (body_id),
	id (id),
	name (name)
{
}

tindividual::~tindividual (void)
{
}

void tindividual::initialise(pqxx::connection * connection)
{
	connection->prepare("neuron_schema.pinstindividual", "SELECT * FROM neuron_schema.pinstindividual($1, $2)");
}

void tindividual::selectRowSQL(pqxx::work & txn)
{

	pqxx::result res = txn.exec(SQL_SELECT + " id = " + txn.quote(id) + ";");
	// Only get one result line (as we use the Primary Key
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		dbquery::DBUtils::toInt(&this->body_id, res[i]["body_id"]);
		dbquery::DBUtils::toInt(&this->id, res[i]["id"]);
		dbquery::DBUtils::toString(&this->name, res[i]["name"]);

	}
	
}

void tindividual::deleteRowSQL(pqxx::work & txn)
{

	pqxx::result res = txn.exec("DELETE FROM \
		neuron_schema.tindividual \
	WHERE \
		id = " + txn.quote(id) + \
	";");
	clockSavedToDB();
	
}

void tindividual::updateRowSQL(pqxx::work & txn)
{

	pqxx::result res = txn.exec("UPDATE \
		neuron_schema.tindividual \
	SET \
		body_id  = " + txn.quote(body_id) + ", \
		name  = " + txn.quote(name) + " \
	WHERE \
		id = " + txn.quote(id) + \
	";");
	clockSavedToDB();

}

void tindividual::insertRowSQL(pqxx::work & txn)
{

	pqxx::result res = txn.prepared("neuron_schema.pinstindividual")(txn.quote(body_id))(txn.quote(name)).exec();
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		dbquery::DBSafeUtils::safeToInt(&this->id, res[i][0]);
	}
	clockSavedToDB();

}

int tindividual::getBody_Id(void )
{
	accessed();
	return body_id;
}

int tindividual::getId(void )
{
	accessed();
	return id;
}

string tindividual::getName(void )
{
	accessed();
	return name;
}

void tindividual::setBody_Id(int body_id)
{
	if (this->body_id != body_id)
	{
		this->body_id = body_id;
		clockModified();
		//TODO: Need to add this to the dbTransaction class as an update
	}
}

void tindividual::setId(int id)
{
	if (this->id != id)
	{
		this->id = id;
		clockModified();
		//TODO: Need to add this to the dbTransaction class as an update
	}
}

void tindividual::setName(string name)
{
	if (this->name != name)
	{
		this->name = name;
		clockModified();
		//TODO: Need to add this to the dbTransaction class as an update
	}
}

int tindividual::getSequencetindividual_id_seq(void)
{
	int nextValue = 0;
	pqxx::work txn(*mDBConnection);
	pqxx::result res = txn.exec("SELECT NEXTVAL('tindividual_id_seq');");
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		nextValue = stoi(res[i]["nextval"].c_str());
	}
	return nextValue;
}

}
