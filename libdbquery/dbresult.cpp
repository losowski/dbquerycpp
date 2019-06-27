#include "dbresult.hpp"

using namespace std;

namespace dbquery {

DBResult::DBResult(pqxx::connection * connection):
	pk(0),
	mDBConnection(connection)
{
}

DBResult::DBResult(pqxx::connection * connection, const int primaryKey):
	pk(primaryKey),
	mDBConnection(connection)
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
		pqxx::work txn(*mDBConnection);
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
		pqxx::work txn(*mDBConnection);
		deleteRowSQL(txn);
		txn.commit(); //For changes only
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
		pqxx::work txn(*mDBConnection);
		updateRowSQL(txn);
		txn.commit(); //For changes only
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
		pqxx::work txn(*mDBConnection);
		//pqxx::result res = txn.exec("SELECT \)
		txn.commit(); //For changes only
	}
	catch (const pqxx::sql_error & e)
	{
		//TODO: Handle the failure
		std::cerr << "SQL error: " << e.what() << std::endl;
		std::cerr << "Query was: " << e.query() << std::endl;
	}
}


}
