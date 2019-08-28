#ifndef DBSCHEMABASE_HPP
#define DBSCHEMABASE_HPP

#include "dbconnection.hpp"
#include "dbtransaction.hpp"


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
	protected:
		DBTransaction *				mtransaction;
		pqxx::connection *			mdbconnection;
};


}
#endif //DBSCHEMABASE_HPP
