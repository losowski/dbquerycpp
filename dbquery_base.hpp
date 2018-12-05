#ifndef DBQUERY_BASE_HPP
#define DBQUERY_BASE_HPP

#include <string>
#include <list>
#include <map>
#include <set>
#include <tuple>

using namespace std;

namespace dbquery {


//TYPES
typedef set<std::string> tKeys;
typedef map<std::string, std::string> tDataMap;
typedef std::string	tSQL;

class DBQuery
{
	public:
		DBQueryBase(void);
		~DBQueryBase(void);
	public:
		void initialise(void);
	protected:
		tKey									mRequired;
		tKey									mOptional;
		tDataMap								mDataMap;
		tSQL									mSQL;
};
}
#endif //DBQUERY_BASE_HPP
