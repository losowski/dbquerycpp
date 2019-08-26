#include "neuronschema.hpp"
using namespace std;
namespace neuronSchema
{

neuronSchema::neuronSchema(DBConnection & connection, DBTransaction * transaction):
	DBSchemaBase(connection, transaction)
{
}

neuronSchema::~neuronSchema (void)
{
}

void neuronSchema::initialise(void)
{
	tbody::initialise(mdbconnection);
	tindividual::initialise(mdbconnection);
}

ptbody neuronSchema::gettbody(int id, string name)
{
	ptbody obj(new tbody(mdbconnection, id, name) );
	//Store Object by Primary key
	tbodyMap[obj->getId()] = obj;
	mtransaction->addInsertElement(obj);
	//Return object
	return obj;
}

ptbody neuronSchema::gtbody(int primaryKey)
{
//Attempt to find the object
	maptbody::iterator it = tbodyMap.find(primaryKey);
	ptbody ptr_tbody;
	// If cannot be found in cache, create a new object
	if (it == tbodyMap.end())
	{
		ptbody obj(new tbody(mdbconnection, primaryKey) );
		//Check data exists
		bool exists = obj->selectRow();
		if (true == exists)
		{
			//Store Object by Primary key
			tbodyMap[obj->getId()] = obj;
			//Copy pointer to return
			ptr_tbody = obj;
		}
	}
	//Found object, return that
	//TODO: What if data does not exist in DB?
	else
	{
		//Set return value as second
		ptr_tbody = it->second;
	}
	return ptr_tbody;
}

ptbody neuronSchema::inserttbody(string name)
{
	ptbody obj(new tbody(mdbconnection, name) );
	//Store Object by Primary key
	tbodyMap[obj->getId()] = obj;
	// Add object to insert Queue
	//TODO: figure out if we can insert this object!
	mtransaction->addInsertElement(obj);
	//Return object
	return obj;
}

paptbody neuronSchema::getMultipletbody(string & sqlWhereClause)
{
//Get objects to return
	paptbody objects;
	//Get new transaction
	pqxx::work txn(*mdbconnection);
	//Build the SQL statement
	string sql = tbody::SQL_SELECT + sqlWhereClause + ";";
	// Run the query
	pqxx::result res = txn.exec(sql);
	//Build the objects
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		//Local variables for the data
		int id;
		string name;

		//Set the data
		dbquery::DBSafeUtils::safeToInt(&id, res[i]["id"]);
		dbquery::DBSafeUtils::safeToString(&name, res[i]["name"]);

		//Build the actual object
		ptbody ptr_tbody = gettbody(id, name);
		//Store in returned list
		objects->push_back(ptr_tbody);

	}
	//Return objects
	return objects;
}

ptindividual neuronSchema::gettindividual(int body_id, int id, string name)
{
	ptindividual obj(new tindividual(mdbconnection, body_id, id, name) );
	//Store Object by Primary key
	tindividualMap[obj->getId()] = obj;
	mtransaction->addInsertElement(obj);
	//Return object
	return obj;
}

ptindividual neuronSchema::gtindividual(int primaryKey)
{
//Attempt to find the object
	maptindividual::iterator it = tindividualMap.find(primaryKey);
	ptindividual ptr_tindividual;
	// If cannot be found in cache, create a new object
	if (it == tindividualMap.end())
	{
		ptindividual obj(new tindividual(mdbconnection, primaryKey) );
		//Check data exists
		bool exists = obj->selectRow();
		if (true == exists)
		{
			//Store Object by Primary key
			tindividualMap[obj->getId()] = obj;
			//Copy pointer to return
			ptr_tindividual = obj;
		}
	}
	//Found object, return that
	//TODO: What if data does not exist in DB?
	else
	{
		//Set return value as second
		ptr_tindividual = it->second;
	}
	return ptr_tindividual;
}

ptindividual neuronSchema::inserttindividual(int body_id, string name)
{
	ptindividual obj(new tindividual(mdbconnection, body_id, name) );
	//Store Object by Primary key
	tindividualMap[obj->getId()] = obj;
	// Add object to insert Queue
	//TODO: figure out if we can insert this object!
	mtransaction->addInsertElement(obj);
	//Return object
	return obj;
}

paptindividual neuronSchema::getMultipletindividual(string & sqlWhereClause)
{
//Get objects to return
	paptindividual objects;
	//Get new transaction
	pqxx::work txn(*mdbconnection);
	//Build the SQL statement
	string sql = tindividual::SQL_SELECT + sqlWhereClause + ";";
	// Run the query
	pqxx::result res = txn.exec(sql);
	//Build the objects
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		//Local variables for the data
		int body_id;
		int id;
		string name;

		//Set the data
		dbquery::DBSafeUtils::safeToInt(&body_id, res[i]["body_id"]);
		dbquery::DBSafeUtils::safeToInt(&id, res[i]["id"]);
		dbquery::DBSafeUtils::safeToString(&name, res[i]["name"]);

		//Build the actual object
		ptindividual ptr_tindividual = gettindividual(body_id, id, name);
		//Store in returned list
		objects->push_back(ptr_tindividual);

	}
	//Return objects
	return objects;
}



}
