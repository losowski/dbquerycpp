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
		DBResult(pqxx::connection * db);
		DBResult(pqxx::connection * db, const int primaryKey);
		~DBResult(void);
	public:
		//SELECT
		void selectRow(void);
		virtual void selectRowSQL(pqxx::work* txn) = 0;
		//DELETE
		void deleteRow(int primaryKey);
		virtual void deleteRowSQL(pqxx::work* txn, int primaryKey) = 0;
		//UPDATE
		void updateRow(void);
		virtual void updateRowSQL(pqxx::work* txn) = 0;
		//INSERT
		void insertRow(void);
		virtual void insertRowSQL(pqxx::work* txn) = 0;
	protected:
		int						pk;
	protected:
		pqxx::connection*		m_db;
};

}
#endif //DBRESULT_HPP
