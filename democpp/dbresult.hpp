#ifndef DBRESULT_HPP
#define DBRESULT_HPP

#include <string>
#include <memory>
#include <vector>

#include "dbconnection.hpp"

using namespace std;

namespace dbquery {

class DBResult
{
	public:
		DBResult(dbquery::DBConnection * connection);
		DBResult(dbquery::DBConnection * connection, const int primaryKey);
		~DBResult(void);
	public:
		//SELECT
		void selectRow(void);
		virtual void selectRowSQL(shared_ptr<pqxx::work> txn) = 0;
		//DELETE
		void deleteRow(int primaryKey);
		virtual void deleteRowSQL(shared_ptr<pqxx::work> txn, int primaryKey) = 0;
		//UPDATE
		void updateRow(void);
		virtual void updateRowSQL(shared_ptr<pqxx::work> txn) = 0;
		//INSERT
		void insertRow(void);
		virtual void insertRowSQL(shared_ptr<pqxx::work> txn) = 0;
	protected:
		int									pk;
	protected:
		dbquery::DBConnection *		m_connection;
};

}
#endif //DBRESULT_HPP
