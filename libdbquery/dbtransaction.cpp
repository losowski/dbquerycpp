#include "dbtransaction.hpp"
#include <boost/foreach.hpp>

using namespace std;

namespace dbquery {

DBTransaction::DBTransaction(pqxx::connection * connection):
	mDBConnection(connection)
{
}

/*
DBTransaction(const DBTransaction & transaction)
{
	//TODO: Add copy constructor
}
*/

DBTransaction::~DBTransaction(void)
{
	//Purge the transaction queue
	purgeTransaction();
}

// Transaction oriented commands
shared_ptr<pqxx::work> DBTransaction::newTransaction(void)
{
	return shared_ptr<pqxx::work> ( new pqxx::work(*mDBConnection) );
}

//	Processing data
void DBTransaction::saveTransaction(void)
{
	//Make the transaction
	//TODO: Make this tolerate bad changes:
	//	i.e have a failed transaction register
	// Or remove good transactions
	pqxx::work transaction(*mDBConnection);
	// Insert
	for (vector < ptDBResult >::iterator it = insertTxnObjects.begin(); it != insertTxnObjects.end(); it++)
	{
		(*it)->insertRowSQL(transaction);
	}
	// Update
	for (vector < ptDBResult >::iterator it = updateTxnObjects.begin(); it != updateTxnObjects.end(); it++)
	{
		(*it)->updateRowSQL(transaction);
	}
	// Delete
	for (vector < ptDBResult >::iterator it = deleteTxnObjects.begin(); it != deleteTxnObjects.end(); it++)
	{
		(*it)->deleteRowSQL(transaction);
	}
}


void DBTransaction::purgeTransaction(void)
{
	// Destroy the objects we hold
	// Insert
	for (vector < ptDBResult >::iterator it = insertTxnObjects.begin(); it != insertTxnObjects.end(); it++)
	{
		it->reset();
	}
	// Update
	for (vector < ptDBResult >::iterator it = updateTxnObjects.begin(); it != updateTxnObjects.end(); it++)
	{
		it->reset();
	}
	// Delete
	for (vector < ptDBResult >::iterator it = deleteTxnObjects.begin(); it != deleteTxnObjects.end(); it++)
	{
		it->reset();
	}
}

// Data oriented commands - abort or commit will purge queue
void DBTransaction::addInsertElement (ptDBResult object)
{
	insertTxnObjects.push_back(object);
}

void DBTransaction::addUpdateElement (ptDBResult object)
{
	updateTxnObjects.push_back(object);
}

void DBTransaction::addDeleteElement (ptDBResult object)
{
	//TODO: Check if the insert has a delete action
	//	- If yes, remove the insert
	//TODO: Check if the update has a delete action
	//	- If yes, remove the update
	deleteTxnObjects.push_back(object);
}


}
