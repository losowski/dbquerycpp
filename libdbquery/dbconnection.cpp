#include "dbconnection.hpp"


using namespace std;

namespace dbquery {

DBConnection::DBConnection(const string & connection):
	m_connectionString(connection),
	m_dbconnection(NULL),
	m_transaction(nullptr)
{
}

DBConnection::~DBConnection(void)
{
	//Hopefully Clean the m_dbconnection object
	if (this->m_dbconnection != NULL)
	{
		delete this->m_dbconnection;
	}
}

void DBConnection::connectDB(void)
{
	try
	{
		// Connect to the database
		m_dbconnection = new pqxx::connection(this->m_connectionString);
		//Setup the transaction
		m_transaction = shared_ptr<DBTransaction> ( new DBTransaction(m_dbconnection) );		
	}
	catch (const pqxx::sql_error &e)
	{
		std::cerr << "SQL error: " << e.what() << std::endl;
		std::cerr << "Query was: " << e.query() << std::endl;
		exit(EXIT_FAILURE);
	}
	catch (const std::exception &e)
	{
		std::cerr << "Error: " << e.what() << std::endl;
		exit(EXIT_FAILURE);
	}
}

pqxx::connection * DBConnection::getDBConnection(void)
{
	return m_dbconnection;
}

// Transaction oriented Functionality
void DBConnection::saveTransactions(void)
{
	m_transaction->saveTransaction();
}

void DBConnection::purgeTransactions(void)
{
	m_transaction->purgeTransaction();
}


//Transaction Entries
shared_ptr<pqxx::work> DBConnection::getTransaction(void)
{
	shared_ptr<pqxx::work> txn( new pqxx::work (*m_dbconnection) );
	return txn;
}

void DBConnection::commit(shared_ptr<pqxx::work> transaction)
{
	transaction->commit();
}


}
