#ifndef DBQUERY_CONNECTION_HPP
#define DBQUERY_CONNECTION_HPP

#include <memory>
#include <string>
#include <iostream>
//Libpxx
#include <pqxx/pqxx>
#include <pqxx/cursor>
#include <pqxx/transaction>
#include <pqxx/result>

#include "dbtransaction.hpp"

using namespace std;

namespace dbquery {

class DBConnection
{
	public:
		DBConnection(const string & connection);
		~DBConnection(void);
	public:
		void connectDB(void);
		//Transaction Entries
		shared_ptr<pqxx::work> getTransaction(void);
		void commit(shared_ptr<pqxx::work> transaction);
	private:
		string						m_connectionString;
	protected:
		pqxx::connection *			m_dbconnection;
		DBTransaction				transaction;

};
}
#endif //DBQUERY_CONNECTION_HPP
