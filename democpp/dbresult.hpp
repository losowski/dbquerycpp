#ifndef DBRESULT_HPP
#define DBRESULT_HPP

#include "dbconnection.hpp"

using namespace std;

namespace dbquery {

class DBResult
{
	public:
		DBResult(pqxx::connection const * db);
		DBResult(pqxx::connection const * db, const int primaryKey);
		~DBResult(void);
	public:
		//SELECT
		virtual void getRow(void) = 0;
		//DELETE
		virtual void deleteRow(int primaryKey) = 0;
		//UPDATE
		virtual void saveRow(void) = 0;
		//INSERT
		virtual void addRow(void) = 0;
	protected:
		int						pk;
	private:
		pqxx::connection const *	m_db;
};

}
#endif //DBRESULT_HPP
