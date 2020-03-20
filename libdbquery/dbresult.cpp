#include "dbresult.hpp"

using namespace std;

namespace dbquery {

DBResult::DBResult(pqxx::connection * connection):
	mDBConnection(connection),
	mModifiedTime(0),
	mLastSavedTime(0),
	mAccessedTime(0)
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

void DBResult::clockModified(void)
{
	mModifiedTime = clock();
}

void DBResult::clockSavedToDB(void)
{
	mLastSavedTime = clock();
}

bool DBResult::isUnSaved(void)
{
	bool returnValue = true;
	// If saved is bigger than modified, it was saved more recently than modified
	// Presume there is unsaved work (i.e modified is after saved)
	if (mLastSavedTime >= mModifiedTime)
	{
		returnValue = false;
	}
	return returnValue;
}

void DBResult::accessed(void)
{
	mAccessedTime = clock();
}

bool DBResult::canPurgeCache(clock_t & purgePastTime)
{
	bool val = false;
	if (false == isUnSaved())
	{
		if (purgePastTime >= mAccessedTime)
		{
			val = true;
		}
	}
	return val;
}

}
