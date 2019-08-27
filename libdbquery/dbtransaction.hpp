#ifndef DBQUERY_TRANSACTION_HPP
#define DBQUERY_TRANSACTION_HPP

#include <set>
#include <memory>

//Libpxx
#include <pqxx/pqxx>
#include <pqxx/cursor>
#include <pqxx/transaction>
#include <pqxx/result>

#include "dbconnection.hpp"
#include "dbresult.hpp"

using namespace std;

namespace dbquery {

class DBTransaction;

//TODO: Create method to identify errors for review

class DBTransaction
{
	public:
		DBTransaction(DBConnection * dbconnection);
		//DBTransaction(const DBTransaction & transaction);
		~DBTransaction(void);
	public:
		//	Processing data
		void saveTransaction(void);
		void purgeTransaction(void);
		// Data oriented commands - abort or commit will purge queue
		void addInsertElement (ptDBResult object);
		void addUpdateElement (ptDBResult object);
		void addDeleteElement (ptDBResult object);
	private:
		DBConnection *					mDBConnection;
		//Transaction Lists
		set < ptDBResult > 				insertTxnObjects;
		set < ptDBResult > 				updateTxnObjects;
		set < ptDBResult > 				deleteTxnObjects;
};

typedef shared_ptr<DBTransaction> ptDBTransaction;

}
#endif //DBQUERY_TRANSACTION_HPP
