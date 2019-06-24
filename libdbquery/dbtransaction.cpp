#include "dbtransaction.hpp"
#include <boost/foreach.hpp>

using namespace std;

namespace dbquery {

DBTransaction::DBTransaction(pqxx::connection * connection):
	m_connection(connection),
	transaction(new pqxx::work (*connection))
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
	// Destroy the transaction object
	transaction.reset();
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

// Transaction oriented commands
shared_ptr<pqxx::work> DBTransaction::newTransaction(void)
{
	transaction.reset();
	transaction = shared_ptr<pqxx::work> ( new pqxx::work(*m_connection) );
	return transaction;
}

//	Processing data
void DBTransaction::saveTransaction(void)
{
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

//	commitTransaction and abortTransaction purge the commit queue
void DBTransaction::commitTransaction(void)
{
	transaction->commit();
}

void DBTransaction::abortTransaction(void)
{
	transaction->abort();
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
