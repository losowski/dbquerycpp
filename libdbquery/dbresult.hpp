#ifndef DBRESULT_HPP
#define DBRESULT_HPP

#include <iostream>
#include <string>
#include <memory>
#include <vector>
#include <ctime>

//Libpxx
#include <pqxx/pqxx>
#include <pqxx/cursor>
#include <pqxx/transaction>
#include <pqxx/result>

using namespace std;

namespace dbquery {

class DBResult
{
	public:
		//TODO: Change constructors to using the pqxx types
		DBResult(pqxx::connection * connection);
		~DBResult(void);
	public:
		//SELECT
		bool selectRow(void);
		virtual void selectRowSQL(pqxx::work & txn) = 0;
		//DELETE
		void deleteRow(void);
		virtual void deleteRowSQL(pqxx::work & txn) = 0;
		//UPDATE
		void updateRow(void);
		virtual void updateRowSQL(pqxx::work & txn) = 0;
		//INSERT
		void insertRow(void);
		virtual void insertRowSQL(pqxx::work & txn) = 0;
	protected:
		void clockModified(void);
		void clockSavedToDB(void);
		bool isUnSaved(void);
	protected:
		pqxx::connection *		mDBConnection;
	private:
		time_t					mModifiedTime;
		time_t					mLastSavedTime;
};

typedef shared_ptr<DBResult> ptDBResult;

}
#endif //DBRESULT_HPP
