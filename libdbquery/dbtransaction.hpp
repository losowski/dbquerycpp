#ifndef DBQUERY_TRANSACTION_HPP
#define DBQUERY_TRANSACTION_HPP

#include <vector>
#include <memory>

#include "dbresult.hpp"

//Libpxx
#include <pqxx/pqxx>
#include <pqxx/cursor>
#include <pqxx/transaction>
#include <pqxx/result>

using namespace std;

namespace dbquery {

class DBTransaction;

//TODO: Create method to identify errors for review

class DBTransaction
{
	public:
		DBTransaction(pqxx::connection * connection);
		//DBTransaction(const DBTransaction & transaction);
		~DBTransaction(void);
	public:
		// Transaction oriented commands
		shared_ptr<pqxx::work> newTransaction(void);
		//	Processing data
		void saveTransaction(void);
		//	commitTransaction and abortTransaction purge the commit queue
		void commitTransaction(void);
		void abortTransaction(void);
		// Data oriented commands - abort or commit will purge queue
		void addInsertElement (ptDBResult object);
		void addUpdateElement (ptDBResult object);
		void addDeleteElement (ptDBResult object);
	private:
		pqxx::connection *					mDBConnection;
		//Transaction Lists
		vector < ptDBResult > 				insertTxnObjects;
		vector < ptDBResult > 				updateTxnObjects;
		vector < ptDBResult > 				deleteTxnObjects;
};


}
#endif //DBQUERY_TRANSACTION_HPP
