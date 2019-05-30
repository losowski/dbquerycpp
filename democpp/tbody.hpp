#ifndef NEURON_SCHEMA_TBODY_HPP
#define NEURON_SCHEMA_TBODY_HPP

#include <memory>
#include <vector>

#include "dbresult.hpp"
#include "dbsafeutils.hpp"


using namespace std;
using namespace dbquery;

namespace neuronSchema {

class tBody;

typedef shared_ptr<tBody> ptBody;
typedef vector < ptBody >  aptBody;
typedef shared_ptr < aptBody>  paptBody;

class tBody : public DBResult
{
	public:
		static const string SQL_SELECT;
	public:
		tBody(dbquery::DBConnection * connection);
		tBody(dbquery::DBConnection * connection, const int primaryKey);
		tBody(dbquery::DBConnection * connection, int id, const string & text);
		~tBody(void);
	public:
		//SELECT
		void selectRowSQL(shared_ptr<pqxx::work> txn);
		//DELETE
		void deleteRowSQL(shared_ptr<pqxx::work> txn);
		//UPDATE
		void updateRowSQL(shared_ptr<pqxx::work> txn);
		//INSERT
		void insertRowSQL(shared_ptr<pqxx::work> txn);
		//Schema Functions
		//TODO: Figure out how to implement SQL to go down hierarchy
	public:
		int 		id;
		string		name;
};

}
#endif //NEURON_SCHEMA_TBODY_HPP
