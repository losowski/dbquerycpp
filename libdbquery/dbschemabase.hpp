#ifndef DBSCHEMABASE_HPP
#define DBSCHEMABASE_HPP

#include "dbconnection.hpp"
#include "dbtransaction.hpp"

#include <ctime>

using namespace std;
namespace dbquery
{


class DBSchemaBase
{
	public:
		DBSchemaBase(DBConnection & connection, DBTransaction * transaction);
	public:
		~DBSchemaBase (void);
	public:
		pqxx::connection * getConnection(void);
		//Prepare Initailise
		virtual void initialise(void) = 0;
		//Cache Setup
		void setCacheTimeout(int interval);
		time_t getCacheExpiry(void);
	protected:
		DBTransaction *				mtransaction;
		pqxx::connection *			mdbconnection;
		int							mCacheInterval;
	protected:
		static const int 			CACHE_INTERVAL;
};


}
#endif //DBSCHEMABASE_HPP
