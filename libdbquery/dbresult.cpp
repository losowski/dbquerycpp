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
bool DBResult::selectRow(void)
{
	bool retvalue = false;
	try
	{
		shared_ptr<pqxx::work> txn = m_connection->getTransaction();
		selectRowSQL(txn);
		retvalue = true;
		//txn.commit(); //For changes only
	}
	catch (const pqxx::plpgsql_no_data_found & e)
	{
		//No Data found
		std::cerr << "SQL error: " << e.what() << std::endl;
		std::cerr << "Query was: " << e.query() << std::endl;
		//TODO: Maybe throw an exception? - Maybe not
		//throw DBExceptionNoData();
	}
	catch (const pqxx::sql_error & e)
	{
		//TODO: Handle the failure
		std::cerr << "SQL error: " << e.what() << std::endl;
		std::cerr << "Query was: " << e.query() << std::endl;
	}
	return retvalue;
}

//DELETE
void DBResult::deleteRow(void)
{
	try
	{
		shared_ptr<pqxx::work> txn = m_connection->getTransaction();
		deleteRowSQL(txn);
		txn->commit(); //For changes only
	}
	catch (const pqxx::sql_error & e)
	{
		//TODO: Handle the failure
		std::cerr << "SQL error: " << e.what() << std::endl;
		std::cerr << "Query was: " << e.query() << std::endl;
	}
}

//UPDATE
void DBResult::updateRow(void)
{
	try
	{
		shared_ptr<pqxx::work> txn = m_connection->getTransaction();
		updateRowSQL(txn);
		txn->commit(); //For changes only
	}
	catch (const pqxx::sql_error & e)
	{
		//TODO: Handle the failure
		std::cerr << "SQL error: " << e.what() << std::endl;
		std::cerr << "Query was: " << e.query() << std::endl;
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
	catch (const pqxx::sql_error & e)
	{
		//TODO: Handle the failure
		std::cerr << "SQL error: " << e.what() << std::endl;
		std::cerr << "Query was: " << e.query() << std::endl;
	}
}


}
