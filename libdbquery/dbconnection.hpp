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

using namespace std;

namespace dbquery {

class DBConnection
{
	public:
		DBConnection(const string & connection);
		~DBConnection(void);
	public:
		void connectDB(void);
		pqxx::connection * getConnection(void);
	private:
		string						m_connectionString;
	protected:
		pqxx::connection *			m_dbconnection;

};

typedef shared_ptr<DBConnection> ptDBConnection;

}
#endif //DBQUERY_CONNECTION_HPP
