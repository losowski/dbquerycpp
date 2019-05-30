#include "neuron_schema.hpp"

using namespace std;

namespace neuronSchema {

NeuronSchema::NeuronSchema(const string & connection):
	dbquery::DBConnection(connection),
	transaction(this)
{
}

NeuronSchema::~NeuronSchema(void)
{
}

//tBody
ptBody NeuronSchema::gtBody(int primaryKey)
{
	//Attempt to find the object
	maptBody::iterator it = tBodyMap.find(primaryKey);
	ptBody ptr_tbody;
	// If cannot be found in cache, create a new object
	if (it == tBodyMap.end())
	{
		ptBody obj(new tBody(this, primaryKey) );
		//Check data exists
		if (obj->selectRow() == true)
		{
			obj->selectRow();
			//Store Object by Primary key
			tBodyMap[obj->id] = obj;
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

ptBody NeuronSchema::gtBody(int id, const string & text)
{
	ptBody obj(new tBody(this, id, text) );
	//Store Object by Primary key
	tBodyMap[obj->id] = obj;
	// Add object to insert Queue
	//TODO: figure out if we can insert this object!
	transaction.addInsertElement(obj);
	//Return object
	return obj;
}

paptBody NeuronSchema::gtBodyName(string & name)
{
	//Get objects to return
	paptBody objects;
	//Get new transaction
	shared_ptr<pqxx::work> txn = transaction.newTransaction();
	//Build the SQL statement
	string sql = tBody::SQL_SELECT + " name = " + txn->quote(name) + ";";
	// Run the query
	pqxx::result res = txn->exec(sql);
	//Build the objects
	for (pqxx::result::size_type i = 0; i != res.size(); ++i)
	{
		//Local variables for the data
		int id = 0;
		string name;
		//Set the data
		dbquery::DBSafeUtils::safeToInt(&id, res[i]["id"]);
		dbquery::DBSafeUtils::safeToString(&name, res[i]["name"]);
		//Build the actual object
		ptBody ptr_tbody = gtBody( id, name);
		//Store in returned list
		objects->push_back(ptr_tbody);

	}
	//Return objects
	return objects;
}

//tIndividual
ptIndividual NeuronSchema::gtIndividual(int primaryKey)
{
	//Attempt to find the object
	maptIndividual::iterator it = tIndividualMap.find(primaryKey);
	ptIndividual ptr_tindividual;
	// If cannot be found in cache, create a new object
	if (it == tIndividualMap.end())
	{
		ptIndividual obj(new tIndividual(this, primaryKey) );
		//Check data exists
		if (obj->selectRow() == true)
		{
			//Store Object by Primary key
			tIndividualMap[obj->id] = obj;
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

ptIndividual NeuronSchema::gtIndividual(int id, int body_id, string & name)
{
	ptIndividual obj(new tIndividual(this, id, body_id, name) );
	//Store Object by Primary key
	tIndividualMap[obj->id] = obj;
	// Add object to insert Queue
	//TODO: figure out if we can insert this object!
	transaction.addInsertElement(obj);
	//Return object
	return obj;
}



paptIndividual NeuronSchema::gtIndividualbytBody(const tBody & body)
{
	return tIndividual::gtIndividualsFromBody(this, body);

}

}
