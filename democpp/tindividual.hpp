#ifndef NEURON_SCHEMA_TINDIVIDUAL_HPP
#define NEURON_SCHEMA_TINDIVIDUAL_HPP
#include "dbresult.hpp"
#include "dbsafeutils.hpp"
#include "dbutils.hpp"
#include "dbconnection.hpp"
using namespace std;
using namespace dbquery;
namespace neuronSchema
{

class tindividual;

typedef shared_ptr<tindividual> ptindividual;
typedef vector < ptindividual > aptindividual;
typedef shared_ptr < aptindividual> paptindividual;
class tindividual : public dbquery::DBResult
{
	public:
		static const string	SQL_SELECT;
	public:
		tindividual (pqxx::connection * connection);
		tindividual (pqxx::connection * connection, const int id);
		tindividual (pqxx::connection * connection, int & body_id, string & name);
		tindividual (pqxx::connection * connection, int & body_id, int & id, string & name);
	public:
		~tindividual (void);

	public:
		void selectRowSQL(pqxx::work & txn);
		void deleteRowSQL(pqxx::work & txn);
		void updateRowSQL(pqxx::work & txn);
		void insertRowSQL(pqxx::work & txn);
		int getBody_Id(void );
		int getId(void );
		string getName(void );
		void setBody_Id(int body_id);
		void setId(int id);
		void setName(string name);
	public:
		int			body_id;
		int			id;
		string			name;
};


}
#endif //NEURON_SCHEMA_TINDIVIDUAL_HPP
