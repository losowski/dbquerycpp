#ifndef DBQUERY_CONNECTION_HPP
#define DBQUERY_CONNECTION_HPP

#include <string>
#include <list>
#include <map>
#include <set>
#include <tuple>

using namespace std;

namespace dbquery {

class DBConnection
{
	public:
		DBConnection(string username, string password);
		~DBConnection(void);
	public:
		void connect(void);
	private:
		string		username;
		string		password;

};
}
#endif //DBQUERY_CONNECTION_HPP
