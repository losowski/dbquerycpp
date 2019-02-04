#include "dbresult.hpp"

using namespace std;

namespace dbquery {

DBResult::DBResult(pqxx::connection * db):
	pk(0),
	m_db(db)
{
}

DBResult::DBResult(pqxx::connection * db, const int primaryKey):
	pk(primaryKey),
	m_db(db)
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
		pqxx::work txn(*m_db);
		//pqxx::result res = txn.exec("SELECT \)
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
		pqxx::work txn(*m_db);
		//pqxx::result res = txn.exec("SELECT \)
		txn.commit(); //For changes only
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
		pqxx::work txn(*m_db);
		//pqxx::result res = txn.exec("SELECT \)
		txn.commit(); //For changes only
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
		pqxx::work txn(*m_db);
		//pqxx::result res = txn.exec("SELECT \)
		txn.commit(); //For changes only
	}
	catch (const pqxx::sql_error &e)
	{
		//TODO: Handle the failure
	}
}


}
