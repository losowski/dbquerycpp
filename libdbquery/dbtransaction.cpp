#include "dbtransaction.hpp"
#include <boost/foreach.hpp>

using namespace std;

namespace dbquery {

DBTransaction::DBTransaction(dbquery::DBConnection * connection):
	m_connection(connection),
	transaction(connection->getTransaction())
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
	for (vector < ptDBResult >::iterator it = txnObjects.begin(); it != txnObjects.end(); it++)
	{
		it->reset();
	}
}

// Transaction oriented commands
void DBTransaction::newTransaction(void)
{
	transaction.reset();
	transaction = m_connection->getTransaction();
}

//	Processing data
void DBTransaction::bulkUpdate(void)
{
	for (vector < ptDBResult >::iterator it = txnObjects.begin(); it != txnObjects.end(); it++)
	{
		(*it)->updateRowSQL(transaction);
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
void DBTransaction::addElement (ptDBResult object)
{
	txnObjects.push_back(object);
}

}
