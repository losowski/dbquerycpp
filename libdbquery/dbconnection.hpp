#ifndef DBQUERY_CONNECTION_HPP
#define DBQUERY_CONNECTION_HPP

#include <string>
#include <iostream>
//Libpxx
#include <pqxx/pqxx>
#include <pqxx/cursor>
#include <pqxx/transaction>
#include <pqxx/result>

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
	protected:
		pqxx::connection *			m_dbconnection;
	private:
		string						m_connection;

};
}
#endif //DBQUERY_CONNECTION_HPP