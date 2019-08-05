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
	for (set < ptDBResult >::iterator it = insertTxnObjects.begin(); it != insertTxnObjects.end(); it++)
	{
		(*it)->insertRowSQL(transaction);
	}
	// Update
	for (set < ptDBResult >::iterator it = updateTxnObjects.begin(); it != updateTxnObjects.end(); it++)
	{
		(*it)->updateRowSQL(transaction);
	}
	// Delete
	for (set < ptDBResult >::iterator it = deleteTxnObjects.begin(); it != deleteTxnObjects.end(); it++)
	{
		(*it)->deleteRowSQL(transaction);
	}
	//TODO: Implement this better!
	//Commit on Success
	transaction.commit();
	//Purge the transaction
	purgeTransaction();
}


void DBTransaction::purgeTransaction(void)
{
	// Destroy the objects we hold
	// Insert
	insertTxnObjects.clear();
	// Update
	updateTxnObjects.clear();
	// Delete
	deleteTxnObjects.clear();
}

// Data oriented commands - abort or commit will purge queue
void DBTransaction::addInsertElement (ptDBResult object)
{
	insertTxnObjects.insert(object);
}

void DBTransaction::addUpdateElement (ptDBResult object)
{
	updateTxnObjects.insert(object);
}

void DBTransaction::addDeleteElement (ptDBResult object)
{
	//TODO: Check if the insert has a delete action
	//	- If yes, remove the insert
	set < ptDBResult >::iterator insertIt = insertTxnObjects.find(object);
	if (insertIt != insertTxnObjects.end())
	{
		insertTxnObjects.erase(insertIt);
	}
	//TODO: Check if the update has a delete action
	//	- If yes, remove the update
	set < ptDBResult >::iterator updateIt = updateTxnObjects.find(object);
	if (updateIt != updateTxnObjects.end())
	{
		insertTxnObjects.erase(updateIt);
	}
	deleteTxnObjects.insert(object);
}


}
