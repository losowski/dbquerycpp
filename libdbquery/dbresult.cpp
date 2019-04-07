#include "dbresult.hpp"

using namespace std;

namespace dbquery {

DBResult::DBResult(dbquery::DBConnection * connection):
	pk(0),
	m_connection(connection)
{
}

DBResult::DBResult(dbquery::DBConnection * connection, const int primaryKey):
	pk(primaryKey),
	m_connection(connection)
{
}

DBResult::~DBResult(void)
{
}

//SELECT
void DBResult::selectRow(void)
{
	try
	{
		shared_ptr<pqxx::work> txn = m_connection->getTransaction();
		selectRowSQL(txn);
		//txn.commit(); //For changes only
	}
	catch (const pqxx::sql_error &e)
	{
		//TODO: Handle the failure
	}
}

//DELETE
void DBResult::deleteRow(int primaryKey)
{
	try
	{
		shared_ptr<pqxx::work> txn = m_connection->getTransaction();
		//pqxx::result res = txn.exec("SELECT \)
		txn->commit(); //For changes only
	}
	catch (const pqxx::sql_error &e)
	{
		//TODO: Handle the failure
	}
}

//UPDATE
void DBResult::updateRow(void)
{
	try
	{
		shared_ptr<pqxx::work> txn = m_connection->getTransaction();
		//pqxx::result res = txn.exec("SELECT \)
		txn->commit(); //For changes only
	}
	catch (const pqxx::sql_error &e)
	{
		//TODO: Handle the failure
	}
}

//INSERT
void DBResult::insertRow(void)
{
	try
	{
		shared_ptr<pqxx::work> txn = m_connection->getTransaction();
		//pqxx::result res = txn.exec("SELECT \)
		txn->commit(); //For changes only
	}
	catch (const pqxx::sql_error &e)
	{
		//TODO: Handle the failure
	}
}


}
