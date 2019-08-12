#ifndef NEURON_SCHEMA_TBODY_HPP
#define NEURON_SCHEMA_TBODY_HPP
#include "dbresult.hpp"
#include "dbsafeutils.hpp"
#include "dbutils.hpp"
#include "dbconnection.hpp"
using namespace std;
using namespace dbquery;
namespace neuronSchema
{

class tbody;

typedef shared_ptr<tbody> ptbody;
typedef vector < ptbody > aptbody;
typedef shared_ptr < aptbody> paptbody;
class tbody : public dbquery::DBResult
{
	public:
		static const string	SQL_SELECT;
	public:
		tbody (pqxx::connection * connection);
		tbody (pqxx::connection * connection, const int id);
		tbody (pqxx::connection * connection, string & name);
		tbody (pqxx::connection * connection, int & id, string & name);
	public:
		~tbody (void);

	public:
		//Prepare Initailise
		static void initialise(pqxx::connection * connection);
		void selectRowSQL(pqxx::work & txn);
		void deleteRowSQL(pqxx::work & txn);
		void updateRowSQL(pqxx::work & txn);
		void insertRowSQL(pqxx::work & txn);
		int getId(void );
		string getName(void );
		void setId(int id);
		void setName(string name);
	public:
		int			id;
		string			name;
};


}
#endif //NEURON_SCHEMA_TBODY_HPP
