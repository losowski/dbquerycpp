#ifndef DBRESULT_HPP
#define DBRESULT_HPP

#include <string>
#include <memory>
#include <vector>

#include "dbconnection.hpp"
#include "dbexceptionNoData.hpp"

using namespace std;

namespace dbquery {

class DBResult
{
	public:
		//TODO: Change constructors to using the pqxx types
		DBResult(dbquery::DBConnection * connection);
		DBResult(dbquery::DBConnection * connection, const int primaryKey);
		~DBResult(void);
	public:
		//SELECT
		bool selectRow(void);
		virtual void selectRowSQL(shared_ptr<pqxx::work> txn) = 0;
		//DELETE
		void deleteRow(void);
		virtual void deleteRowSQL(shared_ptr<pqxx::work> txn) = 0;
		//UPDATE
		void updateRow(void);
		virtual void updateRowSQL(shared_ptr<pqxx::work> txn) = 0;
		//INSERT
		void insertRow(void);
		virtual void insertRowSQL(shared_ptr<pqxx::work> txn) = 0;
	public:
		int									pk;
	protected:
		dbquery::DBConnection *		m_connection;
};

typedef shared_ptr<DBResult> ptDBResult;

}
#endif //DBRESULT_HPP
