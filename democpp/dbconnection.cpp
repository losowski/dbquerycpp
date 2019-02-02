#include "dbconnection.hpp"

using namespace std;

namespace dbquery {

DBConnection::DBConnection(string username, string password):
	username(username),
	password(password)
{
}

DBConnection::~DBConnection(void)
{
}

void DBConnection::connect(void)
{
}


}
