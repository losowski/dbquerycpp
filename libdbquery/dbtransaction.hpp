#ifndef DBQUERY_TRANSACTION_HPP
#define DBQUERY_TRANSACTION_HPP

#include <vector>

#include "dbresult.hpp"
#include "dbconnection.hpp"

//Libpxx
#include <pqxx/pqxx>
#include <pqxx/cursor>
#include <pqxx/transaction>
#include <pqxx/result>

using namespace std;

namespace dbquery {

class DBTransaction;

class DBTransaction
{
	public:
		DBTransaction(dbquery::DBConnection * connection);
		//DBTransaction(const DBTransaction & transaction);
		~DBTransaction(void);
	public:
		// Transaction oriented commands
		void newTransaction(void);
		//	Processing data
		void bulkUpdate(void);
		//	commitTransaction and abortTransaction purge the commit queue
		void commitTransaction(void);
		void abortTransaction(void);
		// Data oriented commands - abort or commit will purge queue
		void addElement (ptDBResult object);
	private:
		dbquery::DBConnection *				m_connection;
		shared_ptr<pqxx::work>				transaction;
		vector < ptDBResult > 				txnObjects;
};
}
#endif //DBQUERY_TRANSACTION_HPP
